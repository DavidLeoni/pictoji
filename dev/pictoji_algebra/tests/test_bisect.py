"""Self-tests for the diagnostics.

These inject *known* defects and check the tool finds them.  Without this, a
clean report would be indistinguishable from a broken detector - which for an
inconsistency hunter is the failure mode that matters most.
"""

import pytest

from pictoji_algebra.diagnose import (
    CANARY, NONCONFLUENT, bisect_canary, bisect_report, check, ddmin,
)
from pictoji_algebra.engine import normal_forms
from pictoji_algebra.parser import parse
from pictoji_algebra.specload import load_text

# `bad.fence-collapse` equates a fenced run with a bare one, which is exactly
# what form-is-substance forbids.  The canary two lines down must then trip.
POISONED = """\
## Core

    fenced uniform run contracts     # [builtin=contract_run] [id=good.contract]
    sum collection                   # [builtin=collect_sum] [id=good.collect]
    tints float and sort             # [builtin=float_tints] [id=good.float]
    (A B)^-1 == B^-1 A^-1            # [rule] [id=good.inverse]
    (S S) == S S                     # [rule] [id=bad.fence-collapse]

    웃 웃  !=  (웃 웃)
"""


@pytest.fixture(scope="module")
def poisoned():
    return load_text(POISONED, "poisoned.md")


def test_the_canary_trips(poisoned):
    report = check(poisoned, confluence=False)
    assert len(report.canaries) == 1
    assert report.canaries[0].kind == CANARY
    assert report.canaries[0].proof.proved


def test_bisection_isolates_exactly_the_bad_rule(poisoned):
    canary = [a for a in poisoned.assertions if a.is_canary][0]
    culprits = bisect_canary(canary, poisoned.rules)
    assert culprits == ["bad.fence-collapse"]


def test_bisection_is_wired_into_the_report(poisoned):
    report = check(poisoned, confluence=False)
    bisect_report(report, poisoned, poisoned.rules)
    assert report.canaries[0].culprits == ["bad.fence-collapse"]


def test_disabling_the_culprit_silences_the_canary(poisoned):
    clean = poisoned.rules.disable(["bad.fence-collapse"])
    report = check(poisoned, clean, confluence=False)
    assert report.canaries == []


def test_ddmin_finds_a_minimal_subset():
    """Failure needs both 'c' and 'e'; ddmin must return exactly those."""
    calls = []

    def reproduces(subset):
        calls.append(tuple(subset))
        return "c" in subset and "e" in subset

    assert sorted(ddmin(list("abcdefgh"), reproduces)) == ["c", "e"]
    assert len(calls) < 60          # not a brute-force power-set search


def test_ddmin_returns_everything_when_nothing_can_be_dropped():
    assert sorted(ddmin(list("abc"), lambda s: len(s) == 3)) == ["a", "b", "c"]


# -- non-confluence -------------------------------------------------------

DIVERGENT = """\
## Core

    🐶 -> 🏠     # [id=r1]
    🐶 -> 🌳     # [id=r2]

    🐶 ~> 🏠
"""


def test_non_confluence_is_detected():
    spec = load_text(DIVERGENT, "d.md")
    forms = normal_forms(parse("🐶"), spec.rules)
    assert len(forms) == 2

    report = check(spec)
    kinds = [f.kind for f in report.findings]
    assert NONCONFLUENT in kinds


def test_non_termination_is_reported_with_its_cycle():
    spec = load_text("## C\n\n    🐶 -> 🏠   # [id=a]\n    🏠 -> 🐶   # [id=b]\n\n    🐶 ~> 🐶\n",
                     "c.md")
    report = check(spec, confluence=False)
    assert any(f.kind == "non-terminating" for f in report.findings)
    cycle = [f for f in report.findings if f.kind == "non-terminating"][0]
    assert cycle.normalization.cycle is not None
