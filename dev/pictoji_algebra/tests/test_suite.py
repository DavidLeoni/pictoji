"""The real spec file, end to end.

Deliberately does NOT assert "everything passes" - the algebra is assumed
inconsistent.  What it asserts is that the report holds no *surprises*: known
failures are marked `[expect=fail]` in the markdown next to the statement they
are about, so a v7 -> v8 bump edits markdown and never this file.

The one Python-side rule: no algebra content here.  `test_no_algebra_symbols_
in_python` enforces it.
"""

import re
from pathlib import Path

import pytest

from pictoji_algebra.spec import bisect_report, check, load

DEV = Path(__file__).resolve().parents[2]
SPEC = DEV / "pictoji-test-algebra.md"


@pytest.fixture(scope="module")
def spec():
    return load(SPEC)


@pytest.fixture(scope="module")
def report(spec):
    return check(spec, spec.rules, confluence=True)


def test_spec_parses_completely(spec):
    assert spec.problems == [], [p[2] for p in spec.problems]
    assert len(spec.rules) > 15 and len(spec.assertions) > 60


def test_no_findings(report):
    """Every finding kind at once: canaries, failures, non-confluence,
    non-termination, unprintable normal forms, stale expectations."""
    assert [(f.kind, f.title) for f in report.findings] == []


def test_no_canary_trips(spec, report):
    """If this fails, v7 core is provably inconsistent - read the culprit set."""
    assert report.canaries == []
    assert len([a for a in spec.assertions if a.is_canary]) >= 10


def test_expectations_are_declared_in_markdown(spec):
    """The two known failures are v7's, not ours: round parens used for
    association in a system that declares them fences."""
    marked = [a.text for a in spec.assertions if a.expect_fail]
    assert len(marked) == 2


def test_every_rule_fires(spec, report):
    dead = [r.id for r in spec.rules if r.id not in report.rules_used]
    assert dead == [], "dead axioms, or missing coverage for them"


def test_bisection_runs_on_the_real_file(spec, report):
    bisect_report(report, spec, spec.rules)
    assert all(f.culprits for f in report.canaries)


def test_no_algebra_symbols_in_python():
    """Algebra content belongs in markdown, where a revision bump can edit it.

    Scoped to the algebra-facing test modules: `test_terms.py` legitimately
    carries emoji as Unicode *machinery* cases (ZWJ, VS16, flags).
    """
    # Built from escapes: writing the ranges literally would make this
    # module fail its own check.
    symbols = re.compile("[\U0001F300-\U0001FAFF\uac00-\ud7a3\u2600-\u27bf]")
    for name in ("test_engine.py", "test_spec.py", "test_suite.py"):
        text = (Path(__file__).parent / name).read_text(encoding="utf-8")
        found = symbols.findall(text)
        assert not found, "%s carries algebra symbols %r - put them in a .md" % (name, found)
