"""Human-readable output.

Written for someone trying to find a bug in an algebra, so a finding always
shows the derivation that produced it, not just a verdict.
"""

from __future__ import annotations

from typing import List, Optional

from .diagnose import (
    CANARY, CYCLE, FAILED_EQ, FAILED_NF, Finding, NONCONFLUENT, Report,
    UNPARSED, UNPROVED,
)
from .rules import RuleSet

BAR = "=" * 74
DASH = "-" * 74

HEADLINE = {
    CANARY: "CANARY TRIPPED - asserted inequality was DERIVED",
    CYCLE: "NON-TERMINATION - normalization cycled",
    NONCONFLUENT: "NON-CONFLUENCE - more than one normal form",
    FAILED_EQ: "FAILED - asserted equality not derivable",
    FAILED_NF: "FAILED - normalized to the wrong form",
    UNPROVED: "UNKNOWN - search budget exhausted",
    UNPARSED: "UNPARSED - statement could not be read",
}


def render_finding(f: Finding, rules: Optional[RuleSet] = None, verbose: bool = False) -> str:
    lines = [DASH, "%s" % HEADLINE.get(f.kind, f.kind), "  %s" % f.title, "  %s" % f.source]
    if f.detail:
        lines += ["  " + ln for ln in f.detail.split("\n")]

    if f.forms:
        lines.append("  normal forms reached:")
        lines += ["    %r" % t for t in f.forms]

    if f.culprits is not None:
        if f.culprits:
            lines.append("  MINIMAL CULPRIT SET (%d rules):" % len(f.culprits))
            for rule_id in f.culprits:
                rule = rules.get(rule_id) if rules else None
                lines.append("    %s" % (rule.describe() if rule else rule_id))
        else:
            lines.append("  bisection found no reproducing subset (check the budget)")

    if f.normalization and (verbose or f.kind in (CYCLE, FAILED_NF)):
        lines.append("  derivation:")
        lines += ["  " + ln for ln in f.normalization.render().split("\n")]

    if f.proof and (verbose or f.kind == CANARY):
        lines.append("  derivation:")
        lines += ["  " + ln for ln in f.proof.render().split("\n")]

    return "\n".join(lines)


def render(report: Report, rules: Optional[RuleSet] = None,
           verbose: bool = False, show_dead: bool = True) -> str:
    out: List[str] = [BAR, "ㄕICTOji ALGEBRA - CONSISTENCY REPORT", BAR, ""]

    counts = {}
    for f in report.findings:
        counts[f.kind] = counts.get(f.kind, 0) + 1

    out.append("  rules loaded      %d" % report.rule_count)
    out.append("  assertions run    %d" % report.checked)
    out.append("  passed            %d" % report.passed)
    for kind in (CANARY, CYCLE, NONCONFLUENT, FAILED_EQ, FAILED_NF, UNPROVED, UNPARSED):
        if counts.get(kind):
            out.append("  %-17s %d" % (kind, counts[kind]))
    out.append("")

    if show_dead and rules is not None:
        dead = [r for r in rules if r.id not in report.rules_used]
        if dead:
            out.append("  rules that never fired (%d) - dead axioms, or missing coverage:" % len(dead))
            for r in dead:
                out.append("    %s  %s" % (r.id.ljust(24), r.text))
            out.append("")

    for f in report.sorted_findings():
        out.append(render_finding(f, rules, verbose))

    if not report.findings:
        out.append("No findings.  Every assertion held and no canary tripped.")

    out.append(BAR)
    return "\n".join(out)
