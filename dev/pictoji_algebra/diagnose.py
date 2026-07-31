"""Findings, canaries, and automatic axiom bisection.

The tool's job is not to go green.  It is to say precisely what breaks and
which axioms broke it.

A **canary** is a spec-asserted `!=` that the prover nevertheless derives.  That
is a proof the axiom set is inconsistent, and it is the highest-value finding
here - so every tripped canary is automatically delta-debugged down to a
minimal subset of rules that still derives the bad equality.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Callable, List, Optional, Sequence, Set

from .engine import (
    Budget, EXHAUSTED, Normalization, Proof, normal_forms, normalize, prove,
)
from .rules import RuleSet
from .specload import Assertion, SpecFile
from .terms import Term

# Finding kinds, worst first.
CANARY = "canary-tripped"
FAILED_EQ = "failed-equality"
FAILED_NF = "failed-normalization"
NONCONFLUENT = "non-confluent"
CYCLE = "non-terminating"
UNPROVED = "unproved-budget"
UNPARSED = "unparsed"

SEVERITY = [CANARY, CYCLE, NONCONFLUENT, FAILED_EQ, FAILED_NF, UNPROVED, UNPARSED]


@dataclass
class Finding:
    kind: str
    title: str
    source: str
    detail: str = ""
    proof: Optional[Proof] = None
    normalization: Optional[Normalization] = None
    culprits: Optional[List[str]] = None      # filled in by bisection
    forms: Optional[List[Term]] = None        # for non-confluence

    @property
    def rank(self) -> int:
        return SEVERITY.index(self.kind) if self.kind in SEVERITY else len(SEVERITY)


@dataclass
class Report:
    findings: List[Finding] = field(default_factory=list)
    passed: int = 0
    checked: int = 0
    rules_used: Set[str] = field(default_factory=set)
    rule_count: int = 0

    @property
    def failed(self) -> int:
        return len([f for f in self.findings if f.kind in (CANARY, FAILED_EQ, FAILED_NF)])

    @property
    def canaries(self) -> List[Finding]:
        return [f for f in self.findings if f.kind == CANARY]

    def sorted_findings(self) -> List[Finding]:
        return sorted(self.findings, key=lambda f: (f.rank, f.source))


# --------------------------------------------------------------------------
# checking
# --------------------------------------------------------------------------

def check(spec: SpecFile, ruleset: Optional[RuleSet] = None,
          budget: Optional[Budget] = None,
          confluence: bool = True) -> Report:
    """Run every assertion in the spec and collect findings."""
    rules = ruleset if ruleset is not None else spec.rules
    budget = budget or Budget()
    report = Report(rule_count=len(rules))

    for problem in spec.problems:
        report.findings.append(Finding(
            UNPARSED, problem.text, problem.source, problem.reason))

    for a in spec.assertions:
        report.checked += 1

        if a.kind == "nf":
            norm = normalize(a.left, rules, budget)
            report.rules_used |= {s.rule_id for s in norm.steps}
            if norm.cycle:
                report.findings.append(Finding(
                    CYCLE, a.text, a.source,
                    "normalization cycled through %d terms" % len(norm.cycle),
                    normalization=norm))
            elif norm.result == a.right:
                report.passed += 1
            else:
                report.findings.append(Finding(
                    FAILED_NF, a.text, a.source,
                    "normalized to  %r\n  expected      %r" % (norm.result, a.right),
                    normalization=norm))
            continue

        proof = prove(a.left, a.right, rules, budget)
        report.rules_used |= proof.touched

        if a.kind == "eq":
            if proof.proved:
                report.passed += 1
            elif proof.status == EXHAUSTED:
                report.findings.append(Finding(
                    UNPROVED, a.text, a.source,
                    "search budget exhausted after %d nodes - unknown, not disproved"
                    % proof.nodes_explored, proof=proof))
            else:
                report.findings.append(Finding(
                    FAILED_EQ, a.text, a.source,
                    "no derivation found (%d nodes explored)" % proof.nodes_explored,
                    proof=proof))
        else:                                   # canary
            if proof.proved:
                report.findings.append(Finding(
                    CANARY, a.text, a.source,
                    "the prover DERIVED an asserted inequality - the axiom set "
                    "is inconsistent here", proof=proof))
            else:
                report.passed += 1

    if confluence:
        report.findings.extend(_confluence_findings(spec, rules, budget))

    return report


def _confluence_findings(spec: SpecFile, rules: RuleSet, budget: Budget) -> List[Finding]:
    """Terms with more than one normal form under different rule orders.

    v7 line 727 concedes that no confluence check has ever been run, so this is
    checking something genuinely unknown rather than re-testing a guarantee.
    """
    out: List[Finding] = []
    seen: Set[Term] = set()
    for a in spec.assertions:
        for term in (a.left, a.right):
            if term in seen:
                continue
            seen.add(term)
            forms = normal_forms(term, rules, budget)
            if len(forms) > 1:
                out.append(Finding(
                    NONCONFLUENT, repr(term), a.source,
                    "%d distinct normal forms depending on rule order" % len(forms),
                    forms=sorted(forms, key=repr)))
    return out


# --------------------------------------------------------------------------
# bisection
# --------------------------------------------------------------------------

def ddmin(items: Sequence[str], reproduces: Callable[[List[str]], bool]) -> List[str]:
    """Classic delta debugging, then a 1-minimality sweep.

    `reproduces(subset)` must be True when the failure still occurs with only
    those rules enabled.  Rule *dependencies* need no special handling: a subset
    missing a prerequisite simply fails to reproduce and is rejected.
    """
    current = list(items)
    n = 2
    while len(current) >= 2:
        size = max(1, len(current) // n)
        chunks = [current[i : i + size] for i in range(0, len(current), size)]
        reduced = False

        for chunk in chunks:                       # can we keep just one chunk?
            if reproduces(chunk):
                current, n, reduced = chunk, 2, True
                break

        if not reduced:                            # can we drop one chunk?
            for chunk in chunks:
                drop = set(chunk)
                complement = [x for x in current if x not in drop]
                if complement and reproduces(complement):
                    current, n, reduced = complement, max(n - 1, 2), True
                    break

        if not reduced:
            if n >= len(current):
                break
            n = min(2 * n, len(current))

    # 1-minimality: no single remaining rule can be dropped.
    changed = True
    while changed:
        changed = False
        for rule_id in list(current):
            candidate = [x for x in current if x != rule_id]
            if candidate and reproduces(candidate):
                current, changed = candidate, True
                break
    return current


def bisect_canary(assertion: Assertion, rules: RuleSet,
                  budget: Optional[Budget] = None) -> List[str]:
    """Minimal subset of rules that still derives a canary's bad equality."""
    budget = budget or Budget()

    def reproduces(ids: List[str]) -> bool:
        return prove(assertion.left, assertion.right, rules.subset(ids), budget).proved

    if not reproduces(rules.ids):
        return []
    return ddmin(rules.ids, reproduces)


def bisect_report(report: Report, spec: SpecFile, rules: RuleSet,
                  budget: Optional[Budget] = None) -> None:
    """Fill in `culprits` for every tripped canary, in place."""
    by_source = {(a.source, a.text): a for a in spec.assertions}
    for finding in report.canaries:
        a = by_source.get((finding.source, finding.title))
        if a is not None:
            finding.culprits = bisect_canary(a, rules, budget)
