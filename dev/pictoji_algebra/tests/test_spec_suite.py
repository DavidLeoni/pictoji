"""The real spec file, end to end.

Deliberately NOT asserting "everything passes".  The algebra is assumed
inconsistent, so this pins what is currently known and fails loudly when it
changes in either direction - a newly tripped canary is news, and so is a
finding that quietly disappears.
"""

from pathlib import Path

import pytest

from pictoji_algebra.diagnose import CANARY, bisect_report, check
from pictoji_algebra.specload import load

SPEC = Path(__file__).resolve().parents[2] / "pictoji-test-algebra.md"

# Equalities v7 asserts that its own rules do not support.  Both are the same
# defect: round parens used for association in a system where they are declared
# to be fences.  Listed explicitly so a fix shows up as a test failure.
KNOWN_FAILURES = {
    "웃^2 ** (웃^2 ** 웃^2) == 웃^2 웃^3",
    "(🌳 + 웃) + 🐶 == 🌳 + (웃 + 🐶)",
}


@pytest.fixture(scope="module")
def spec():
    assert SPEC.exists(), SPEC
    return load(SPEC)


@pytest.fixture(scope="module")
def report(spec):
    return check(spec, confluence=True)


def test_spec_file_parses_completely(spec):
    assert spec.problems == [], [p.reason for p in spec.problems]
    assert len(spec.rules) > 15
    assert len(spec.assertions) > 50


def test_no_canary_trips(report):
    """If this fails, v7 core is provably inconsistent - read the culprit set."""
    assert [f.title for f in report.canaries] == []


def test_only_the_known_failures_fail(report):
    failures = {f.title for f in report.findings
                if f.kind in ("failed-equality", "failed-normalization")}
    assert failures == KNOWN_FAILURES


def test_no_non_termination_or_non_confluence(report):
    surprises = [f.title for f in report.findings
                 if f.kind in ("non-terminating", "non-confluent")]
    assert surprises == []


def test_nothing_is_left_unknown(report):
    """An EXHAUSTED result means the budget hid an answer; that is not a pass."""
    unknown = [f.title for f in report.findings if f.kind == "unproved-budget"]
    assert unknown == []


def test_every_rule_fires_at_least_once(spec, report):
    dead = [r.id for r in spec.rules if r.id not in report.rules_used]
    assert dead == [], "dead axioms, or missing test coverage for them"


def test_canary_count_is_what_we_think_it_is(spec):
    assert len([a for a in spec.assertions if a.is_canary]) >= 9


def test_bisection_runs_on_the_real_file(spec, report):
    """Cheap when nothing trips; guards the wiring against bit-rot."""
    bisect_report(report, spec, spec.rules)
    assert all(f.culprits for f in report.canaries)
