"""Loader, diagnostics, and bisection.

The bisection and detector tests inject *known* defects and check the tool finds
them.  Without those, a clean report is indistinguishable from a broken
detector - which for an inconsistency hunter is the failure mode that matters.
"""

import pytest

from pictoji_algebra.engine import normal_forms
from pictoji_algebra.spec import (
    CANARY, CYCLE, NONCONFLUENT, UNEXPECTED_PASS, UNPARSED, bisect_canary,
    bisect_report, check, ddmin, load_text, split_top_level,
)
from pictoji_algebra.terms import parse

SPEC = """\
# Title

## Grouping

Prose is ignored, including inline `A == B`.

```text
LHS == RHS   a format legend, not a statement
```

    α α  !=  (α α)
    X^a ** X^b -> X^0 , a == -b               # [ladder=f] [id=annihilate]
    X / D -> X ** D^-1 , grade(D) != 0        # [id=div]
    (A B)^-1 == B^-1 A^-1                     # [rule] [id=inv]
    α^2 == (α α)
    dead -> letter                            # [off]
"""


@pytest.fixture(scope="module")
def spec():
    return load_text(SPEC, "spec.md")


# -- the two splitting traps ----------------------------------------------

def test_relation_split_ignores_brackets():
    """v7:366 writes `X / D  (grade(D) ¬= 0)  ->  X ** D^-1`."""
    ops = [op for _, op in split_top_level(
        "X / D   (grade(D) ¬= 0)   ->   X ** D^-1", ["¬=", "->", "=="])]
    assert ops == ["->"]


def test_a_condition_containing_a_relation_is_still_one_statement(spec):
    """The condition must be split off BEFORE the relation is counted, or every
    conditional rule in a file gets rejected as a chain."""
    assert spec.problems == []
    assert spec.rules.get("annihilate").condition == "a == -b"
    assert spec.rules.get("div").condition == "grade(D) != 0"


def test_chained_relations_are_rejected_loudly():
    """One statement, one relation.  Silently mis-parsing would corrupt it."""
    bad = load_text("## S\n\n    α != β != γ\n", "s.md")
    assert bad.assertions == []
    assert len(bad.problems) == 1
    assert "1 top-level relation" in bad.problems[0][2]


# -- loading --------------------------------------------------------------

def test_prose_and_tagged_fences_are_not_statements(spec):
    assert all("legend" not in a.text for a in spec.assertions)
    assert all("legend" not in r.text for r in spec.rules)


def test_equalities_are_assertions_unless_marked_rule(spec):
    assert spec.rules.get("inv") is not None
    assert any(a.text.startswith("α^2") for a in spec.assertions)


def test_tags_come_from_headings_and_exclude_the_title(spec):
    assert "grouping" in spec.rules.tags and "title" not in spec.rules.tags


def test_off_disables(spec):
    assert all("dead" not in r.text for r in spec.rules)


def test_unparseable_line_is_reported_not_dropped():
    bad = load_text("## S\n\n    α (((  ==  α\n", "s.md")
    assert len(bad.problems) == 1 and bad.problems[0][0] == "s.md:3"
    assert check(bad, bad.rules).findings[0].kind == UNPARSED


def test_selectors_by_id_tag_and_glob(spec):
    r = spec.rules
    assert [x.id for x in r.matching("inv")] == ["inv"]
    assert len(r.matching("grouping")) == len(r)
    assert r.unresolved(["nope"]) == ["nope"]
    assert r.disable(["inv"]).get("inv") is None
    assert r.enable_only(["inv"]).ids == ["inv"]


# -- expectations ---------------------------------------------------------

def test_expect_fail_is_not_a_finding():
    s = load_text("## S\n\n    α == β   # [expect=fail]\n", "s.md")
    rep = check(s, s.rules)
    assert rep.findings == [] and rep.expected_failures == 1


def test_expect_fail_that_starts_passing_is_reported():
    """A stale expectation is a finding: the marker has to be removed."""
    s = load_text("## S\n\n    α == α   # [expect=fail]\n", "s.md")
    assert [f.kind for f in check(s, s.rules).findings] == [UNEXPECTED_PASS]


# -- canaries and bisection -----------------------------------------------

# `bad` equates a fenced run with a bare one - exactly what form-is-substance
# forbids - so the canary below must trip.
POISONED = """\
## Core

    fenced run contracts             # [builtin=contract_run] [id=good.contract]
    sum collection                   # [builtin=collect_sum] [id=good.collect]
    (A B)^-1 == B^-1 A^-1            # [rule] [id=good.inverse]
    (X^a)^b == X^(a ** b)            # [rule] [id=good.replicate]
    (S S) == S S                     # [rule] [id=bad.fence-collapse]

    α α  !=  (α α)
"""


@pytest.fixture(scope="module")
def poisoned():
    return load_text(POISONED, "poisoned.md")


def test_the_canary_trips(poisoned):
    rep = check(poisoned, poisoned.rules, confluence=False)
    assert len(rep.canaries) == 1 and rep.canaries[0].proof.proved


def test_bisection_isolates_exactly_the_bad_rule(poisoned):
    canary = [a for a in poisoned.assertions if a.is_canary][0]
    assert bisect_canary(canary, poisoned.rules) == ["bad.fence-collapse"]


def test_bisection_is_wired_into_the_report(poisoned):
    rep = check(poisoned, poisoned.rules, confluence=False)
    bisect_report(rep, poisoned, poisoned.rules)
    assert rep.canaries[0].culprits == ["bad.fence-collapse"]


def test_disabling_the_culprit_silences_the_canary(poisoned):
    rep = check(poisoned, poisoned.rules.disable(["bad.fence-collapse"]),
                confluence=False)
    assert rep.canaries == []


def test_ddmin_finds_a_minimal_subset():
    calls = []

    def reproduces(subset):
        calls.append(tuple(subset))
        return "c" in subset and "e" in subset

    assert sorted(ddmin(list("abcdefgh"), reproduces)) == ["c", "e"]
    assert len(calls) < 60          # not a brute-force power-set search


def test_ddmin_keeps_everything_when_nothing_can_be_dropped():
    assert sorted(ddmin(list("abc"), lambda s: len(s) == 3)) == ["a", "b", "c"]


# -- the other detectors --------------------------------------------------

def test_non_confluence_is_detected():
    s = load_text("## C\n\n    α -> β   # [id=r1]\n    α -> γ   # [id=r2]\n\n    α ~> β\n",
                  "d.md")
    assert len(normal_forms(parse("α"), s.rules)) == 2
    assert NONCONFLUENT in [f.kind for f in check(s).findings]


def test_non_termination_is_reported_with_its_cycle():
    s = load_text("## C\n\n    α -> β   # [id=a]\n    β -> α   # [id=b]\n\n    α ~> α\n",
                  "c.md")
    found = [f for f in check(s, confluence=False).findings if f.kind == CYCLE]
    assert found and found[0].norm.cycle is not None
