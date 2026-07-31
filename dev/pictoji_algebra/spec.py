"""Markdown -> rules + assertions, then findings, bisection and reporting.

The axioms live in the spec file, not in Python: bisection works over the
markdown rule set, so behaviour hidden in Python is invisible to the bisector.

Statement forms (one relation per line):

    LHS -> RHS            oriented rule          LHS ~> RHS   normalizes-to
    LHS =  RHS            oriented rule          LHS == RHS   must be provable
    LHS -> RHS , COND     rule with a condition  LHS != RHS   CANARY: must not be

Directives inside the trailing `# ...`: `[rule]` promotes `==` to an axiom,
`[builtin=]` binds an n-ary step, `[ladder=]` marks an ordered case ladder,
`[id=]`/`[tags=]`, `[expect=fail]`, `[off]`.  Rules also inherit tags from their
markdown headings, so `--disable fusion` works unannotated.
"""

from __future__ import annotations

import fnmatch
import os
import re
from dataclasses import dataclass, field
from typing import Callable, FrozenSet, List, Optional, Sequence, Set

from .engine import (
    BUILTINS, Budget, EQUIV, EXHAUSTED, REDUCE, normal_forms, normalize, prove,
)
from .terms import LexError, ParseError, graphemes, parse, read_spec, show

RELATIONS = ["k->", "¬==", "!=", "¬=", "==", "~>", "->", "="]
OPEN, CLOSE = set("([{"), set(")]}")
DIRECTIVE = re.compile(r"\[(\w+)(?:=([^\]]*))?\]")


# --------------------------------------------------------------------------
# rules
# --------------------------------------------------------------------------

@dataclass(frozen=True)
class Rule:
    id: str
    kind: str
    lhs: Optional[tuple]
    rhs: Optional[tuple]
    tags: FrozenSet[str]
    source: str
    text: str
    condition: Optional[str] = None
    builtin: Optional[str] = None
    ladder: Optional[str] = None
    holds: bool = False

    def describe(self):
        cond = "  if %s" % self.condition if self.condition else ""
        return "%s  |  %s%s  [%s]  %s" % (self.id, self.text.strip(), cond,
                                          ",".join(sorted(self.tags)), self.source)


class RuleSet:
    def __init__(self, rules):
        self.rules = list(rules)
        self._by_id = {r.id: r for r in self.rules}

    def __len__(self):
        return len(self.rules)

    def __iter__(self):
        return iter(self.rules)

    def get(self, rule_id):
        return self._by_id.get(rule_id)

    @property
    def ids(self):
        return [r.id for r in self.rules]

    @property
    def tags(self):
        return frozenset().union(*[r.tags for r in self.rules]) if self.rules else frozenset()

    def matching(self, selector):
        """An exact id, a tag, or a glob over either."""
        if selector in self._by_id:
            return [self._by_id[selector]]
        hit = [r for r in self.rules if selector in r.tags]
        return hit or [r for r in self.rules
                       if fnmatch.fnmatch(r.id, selector)
                       or any(fnmatch.fnmatch(t, selector) for t in r.tags)]

    def unresolved(self, selectors):
        return [s for s in selectors if not self.matching(s)]

    def disable(self, selectors):
        drop = {r.id for s in selectors for r in self.matching(s)}
        return RuleSet([r for r in self.rules if r.id not in drop])

    def enable_only(self, selectors):
        keep = {r.id for s in selectors for r in self.matching(s)}
        return RuleSet([r for r in self.rules if r.id in keep])

    def subset(self, ids):
        want = set(ids)
        return RuleSet([r for r in self.rules if r.id in want])


@dataclass(frozen=True)
class Assertion:
    id: str
    kind: str                      # 'eq' | 'neq' | 'nf'
    left: tuple
    right: tuple
    tags: FrozenSet[str]
    source: str
    text: str
    expect_fail: bool = False

    @property
    def is_canary(self):
        return self.kind == "neq"


@dataclass
class SpecFile:
    rules: RuleSet
    assertions: List[Assertion]
    problems: List[tuple] = field(default_factory=list)   # (source, text, reason)


# --------------------------------------------------------------------------
# loading
# --------------------------------------------------------------------------

def split_top_level(text, needles):
    """Find `needles` at bracket depth zero.

    Bracket-aware because v7 writes `X / D  (grade(D) ¬= 0)  ->  X ** D^-1`,
    where the `¬=` is inside a condition and is emphatically not the relation.
    """
    gs, hits, depth, i = graphemes(text), [], 0, 0
    while i < len(gs):
        g = gs[i]
        if g in OPEN:
            depth += 1
        elif g in CLOSE:
            depth -= 1
        elif depth == 0:
            for needle in needles:
                ng = graphemes(needle)
                if gs[i:i + len(ng)] == ng:
                    hits.append((i, needle))
                    i += len(ng)
                    break
            else:
                i += 1
            continue
        i += 1
    return hits


def _cut(text, start, end=None):
    gs = graphemes(text)
    return "".join(gs[start:end] if end is not None else gs[start:])


def _statements(text):
    """Yield `(lineno, statement, tagstack)` for indented and fenced lines.

    A fence carrying a language tag is documentation - that is what keeps the
    spec file's own ```text format legend from loading as nonsense rules.
    Level-1 headings are the document title and would tag everything.
    """
    stack, in_fence, prose = [], False, False
    for lineno, raw in enumerate(text.split("\n"), 1):
        s = raw.strip()
        if s.startswith("```"):
            if in_fence:
                in_fence = prose = False
            else:
                info = s[3:].strip()
                in_fence, prose = True, bool(info) and info != "pictoji"
            continue
        if not in_fence and s.startswith("#"):
            level = len(s) - len(s.lstrip("#"))
            del stack[level - 1:]
            stack.append(slug(s[level:].strip()))
            continue
        if s and not prose and (in_fence or raw.startswith(("    ", "\t"))):
            yield lineno, s, tuple(stack[1:])


def slug(text):
    return re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-") or "section"


def load_text(text, filename="<spec>"):
    rules, assertions, problems, counters = [], [], [], {}

    for lineno, line, stack in _statements(text):
        source = "%s:%d" % (filename, lineno)
        hits = split_top_level(line, ["#"])
        body = (_cut(line, 0, hits[0][0]) if hits else line).strip()
        comment = _cut(line, hits[0][0] + 1) if hits else ""
        if not body:
            continue

        opts = {m.group(1): (m.group(2) or "") for m in DIRECTIVE.finditer(comment)}
        if "off" in opts:
            continue

        chapter = stack[-1] if stack else "spec"
        tags = set(stack) | {t.strip() for t in opts.get("tags", "").split(",") if t.strip()}
        tags = tags or {"spec"}
        counters[chapter] = counters.get(chapter, 0) + 1
        ident = opts.get("id") or "%s.%02d" % (chapter, counters[chapter])

        if "builtin" in opts:
            if opts["builtin"] not in BUILTINS:
                problems.append((source, line, "unknown builtin %r; known: %s"
                                 % (opts["builtin"], ", ".join(sorted(BUILTINS)))))
                continue
            # The text of a builtin rule is documentation, not a pattern.
            rules.append(Rule(ident, EQUIV if "equiv" in opts else REDUCE, None, None,
                              frozenset(tags), source, body,
                              builtin=opts["builtin"], ladder=opts.get("ladder") or None))
            continue

        # Split the side condition FIRST.  Its own `==` / `!=` is not a relation,
        # and checking relation count before this rejects every ladder rule.
        condition = None
        commas = split_top_level(body, [","])
        if commas:
            condition = _cut(body, commas[-1][0] + 1).strip()
            body = _cut(body, 0, commas[-1][0]).strip()

        rel = split_top_level(body, RELATIONS)
        if len(rel) != 1:
            problems.append((source, line, "expected 1 top-level relation, found %d"
                                           " - one statement, one relation" % len(rel)))
            continue

        at, op = rel[0]
        lt, rt = _cut(body, 0, at).strip(), _cut(body, at + len(graphemes(op))).strip()
        snippet = "%s %s %s" % (lt, op, rt)
        is_rule = op in ("->", "k->", "=") or (op == "==" and "rule" in opts)

        # Parse once, in the mode this statement needs.  Rules read single
        # letters as metavariables and accept `A..`; assertions read them as
        # ground constants, which is the sound way to test a universally
        # quantified law on a generic instance.
        try:
            lhs, rhs = (parse(lt, is_rule), parse(rt, is_rule))
        except (ParseError, LexError) as exc:
            problems.append((source, line, str(exc)))
            continue

        if is_rule:
            rules.append(Rule(ident, REDUCE if op != "==" else EQUIV, lhs, rhs,
                              frozenset(tags), source, snippet, condition=condition,
                              ladder=opts.get("ladder") or None, holds=(lhs == rhs)))
        else:
            assertions.append(Assertion(ident, {"~>": "nf", "==": "eq"}.get(op, "neq"),
                                        lhs, rhs, frozenset(tags), source, snippet,
                                        opts.get("expect") == "fail"))

    return SpecFile(RuleSet(rules), assertions, problems)


def load(path):
    return load_text(read_spec(path), os.path.basename(str(path)))


# --------------------------------------------------------------------------
# findings
# --------------------------------------------------------------------------

CANARY = "canary-tripped"
FAILED_EQ = "failed-equality"
FAILED_NF = "failed-normalization"
NONCONFLUENT = "non-confluent"
CYCLE = "non-terminating"
UNPROVED = "unproved-budget"
UNPARSED = "unparsed"
UNPRINTABLE = "unprintable"
UNEXPECTED_PASS = "unexpected-pass"
SEVERITY = [CANARY, CYCLE, NONCONFLUENT, UNPRINTABLE, FAILED_EQ, FAILED_NF,
            UNEXPECTED_PASS, UNPROVED, UNPARSED]


@dataclass
class Finding:
    kind: str
    title: str
    source: str
    detail: str = ""
    proof: object = None
    norm: object = None
    culprits: Optional[List[str]] = None
    forms: Optional[List[tuple]] = None

    @property
    def rank(self):
        return SEVERITY.index(self.kind) if self.kind in SEVERITY else len(SEVERITY)


@dataclass
class Report:
    findings: List[Finding] = field(default_factory=list)
    passed: int = 0
    checked: int = 0
    expected_failures: int = 0
    rules_used: Set[str] = field(default_factory=set)
    rule_count: int = 0

    @property
    def failed(self):
        return len([f for f in self.findings
                    if f.kind in (CANARY, FAILED_EQ, FAILED_NF, UNEXPECTED_PASS)])

    @property
    def canaries(self):
        return [f for f in self.findings if f.kind == CANARY]

    def sorted(self):
        return sorted(self.findings, key=lambda f: (f.rank, f.source))


def check(spec, rules=None, budget=None, confluence=True):
    rules = spec.rules if rules is None else rules
    budget = budget or Budget()
    rep = Report(rule_count=len(rules))

    for source, text, reason in spec.problems:
        rep.findings.append(Finding(UNPARSED, text, source, reason))

    for a in spec.assertions:
        rep.checked += 1
        ok, finding = _check_one(a, rules, budget, rep)
        if a.expect_fail:
            # An expectation lives next to the statement it is about, so a
            # revision bump edits markdown rather than Python.
            rep.expected_failures += 1
            if ok:
                rep.findings.append(Finding(
                    UNEXPECTED_PASS, a.text, a.source,
                    "marked [expect=fail] but it now holds - remove the marker"))
            continue
        if ok:
            rep.passed += 1
        elif finding is not None:
            rep.findings.append(finding)

    if confluence:
        rep.findings.extend(_confluence(spec, rules, budget))
    rep.findings.extend(_printability(spec, rules, budget))
    return rep


def _check_one(a, rules, budget, rep):
    """Returns (held_as_asserted, finding_if_not)."""
    if a.kind == "nf":
        norm = normalize(a.left, rules, budget)
        rep.rules_used |= {s.rule_id for s in norm.steps}
        if norm.cycle:
            return False, Finding(CYCLE, a.text, a.source,
                                  "normalization cycled through %d terms" % len(norm.cycle),
                                  norm=norm)
        if norm.result == a.right:
            return True, None
        return False, Finding(FAILED_NF, a.text, a.source,
                              "normalized to  %s\n  expected      %s"
                              % (show(norm.result), show(a.right)), norm=norm)

    proof = prove(a.left, a.right, rules, budget)
    rep.rules_used |= proof.touched
    if a.kind == "eq":
        if proof.proved:
            return True, None
        if proof.status == EXHAUSTED:
            return False, Finding(UNPROVED, a.text, a.source,
                                  "search budget exhausted after %d nodes -"
                                  " unknown, not disproved" % proof.nodes, proof=proof)
        return False, Finding(FAILED_EQ, a.text, a.source,
                              "no derivation found (%d nodes explored)" % proof.nodes,
                              proof=proof)
    if proof.proved:
        return False, Finding(CANARY, a.text, a.source,
                              "the prover DERIVED an asserted inequality - the axiom"
                              " set is inconsistent here", proof=proof)
    return True, None


def _confluence(spec, rules, budget):
    out, seen = [], set()
    for a in spec.assertions:
        for term in (a.left, a.right):
            if term in seen:
                continue
            seen.add(term)
            forms = normal_forms(term, rules, budget)
            if len(forms) > 1:
                out.append(Finding(NONCONFLUENT, show(term), a.source,
                                   "%d distinct normal forms depending on rule order"
                                   % len(forms), forms=sorted(forms, key=show)))
    return out


def _printability(spec, rules, budget):
    """A term whose normal form has no surface spelling is a finding about the
    algebra, not a printer nit: the printer may not add parens, because parens
    are fences."""
    out, seen = [], set()
    for a in spec.assertions:
        for term in (a.left, a.right):
            if term in seen:
                continue
            seen.add(term)
            nf = normalize(term, rules, budget).result
            try:
                if parse(show(nf)) != nf:
                    raise ValueError("re-parses differently")
            except Exception as exc:
                out.append(Finding(UNPRINTABLE, show(term), a.source,
                                   "normal form has no faithful surface form: %s" % exc))
    return out


# --------------------------------------------------------------------------
# bisection
# --------------------------------------------------------------------------

def ddmin(items: Sequence[str], reproduces: Callable[[List[str]], bool]) -> List[str]:
    """Delta debugging, then a 1-minimality sweep.

    Rule dependencies need no special handling: a subset missing a prerequisite
    simply fails to reproduce and is rejected."""
    cur, n = list(items), 2
    while len(cur) >= 2:
        size = max(1, len(cur) // n)
        chunks = [cur[i:i + size] for i in range(0, len(cur), size)]
        for chunk in chunks:
            if reproduces(chunk):
                cur, n = chunk, 2
                break
        else:
            for chunk in chunks:
                rest = [x for x in cur if x not in set(chunk)]
                if rest and reproduces(rest):
                    cur, n = rest, max(n - 1, 2)
                    break
            else:
                if n >= len(cur):
                    break
                n = min(2 * n, len(cur))
                continue
        continue
    changed = True
    while changed:
        changed = False
        for rid in list(cur):
            cand = [x for x in cur if x != rid]
            if cand and reproduces(cand):
                cur, changed = cand, True
                break
    return cur


def bisect_canary(assertion, rules, budget=None):
    budget = budget or Budget()

    def reproduces(ids):
        return prove(assertion.left, assertion.right, rules.subset(ids), budget).proved

    return ddmin(rules.ids, reproduces) if reproduces(rules.ids) else []


def bisect_report(report, spec, rules, budget=None):
    index = {(a.source, a.text): a for a in spec.assertions}
    for f in report.canaries:
        a = index.get((f.source, f.title))
        if a is not None:
            f.culprits = bisect_canary(a, rules, budget)


# --------------------------------------------------------------------------
# reporting
# --------------------------------------------------------------------------

BAR, DASH = "=" * 74, "-" * 74
HEADLINE = {
    CANARY: "CANARY TRIPPED - asserted inequality was DERIVED",
    CYCLE: "NON-TERMINATION - normalization cycled",
    NONCONFLUENT: "NON-CONFLUENCE - more than one normal form",
    UNPRINTABLE: "UNPRINTABLE - normal form has no surface spelling",
    FAILED_EQ: "FAILED - asserted equality not derivable",
    FAILED_NF: "FAILED - normalized to the wrong form",
    UNEXPECTED_PASS: "UNEXPECTED PASS - [expect=fail] no longer applies",
    UNPROVED: "UNKNOWN - search budget exhausted",
    UNPARSED: "UNPARSED - statement could not be read",
}


def render_finding(f, rules=None, verbose=False):
    out = [DASH, HEADLINE.get(f.kind, f.kind), "  %s" % f.title, "  %s" % f.source]
    out += ["  " + ln for ln in f.detail.split("\n")] if f.detail else []
    if f.forms:
        out.append("  normal forms reached:")
        out += ["    %s" % show(t) for t in f.forms]
    if f.culprits is not None:
        if f.culprits:
            out.append("  MINIMAL CULPRIT SET (%d rules):" % len(f.culprits))
            out += ["    %s" % (rules.get(c).describe() if rules and rules.get(c) else c)
                    for c in f.culprits]
        else:
            out.append("  bisection found no reproducing subset (check the budget)")
    if f.norm and (verbose or f.kind in (CYCLE, FAILED_NF)):
        out.append("  derivation:")
        out += ["  " + ln for ln in f.norm.render().split("\n")]
    if f.proof and (verbose or f.kind == CANARY):
        out.append("  derivation:")
        out += ["  " + ln for ln in f.proof.render().split("\n")]
    return "\n".join(out)


def render(report, rules=None, verbose=False):
    out = [BAR, "ㄕICTOji ALGEBRA - CONSISTENCY REPORT", BAR, ""]
    counts = {}
    for f in report.findings:
        counts[f.kind] = counts.get(f.kind, 0) + 1

    out.append("  rules loaded      %d" % report.rule_count)
    out.append("  assertions run    %d" % report.checked)
    out.append("  passed            %d" % report.passed)
    if report.expected_failures:
        out.append("  expected failures %d" % report.expected_failures)
    out += ["  %-17s %d" % (k, counts[k]) for k in SEVERITY if counts.get(k)]
    out.append("")

    if rules is not None:
        dead = [r for r in rules if r.id not in report.rules_used]
        if dead:
            out.append("  rules that never fired (%d) - dead axioms, or missing"
                       " coverage:" % len(dead))
            out += ["    %s  %s" % (r.id.ljust(24), r.text) for r in dead]
            out.append("")

    out += [render_finding(f, rules, verbose) for f in report.sorted()]
    if not report.findings:
        out.append("No findings.  Every assertion held and no canary tripped.")
    out.append(BAR)
    return "\n".join(out)
