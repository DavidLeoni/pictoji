"""Engine mechanics, driven entirely by `dev/pictoji-test-machinery.md`.

Not one algebra fact lives here.  The toy file supplies the rules, so a v7
revision cannot break these tests and these tests cannot silently re-encode v7.
`test_machinery_file_is_green` is the real coverage: the ~24 statements in that
file exercise fences, ladders, segment variables and held forms, and this module
only adds the invariants a markdown statement cannot express.
"""

import random
from pathlib import Path

import pytest

from pictoji_algebra.engine import (
    Budget, CLOSED, EXHAUSTED, PROVED, match, normal_forms, normalize, open_seq,
    prove, subst,
)
from pictoji_algebra.spec import check, load, load_text
from pictoji_algebra.terms import atom, num, parse, show

MACHINERY = Path(__file__).resolve().parents[2] / "pictoji-test-machinery.md"


@pytest.fixture(scope="module")
def spec():
    return load(MACHINERY)


@pytest.fixture(scope="module")
def rules(spec):
    return spec.rules


def nf(src, rules):
    return normalize(parse(src), rules).result


def test_machinery_file_is_green(spec):
    """Every mechanism the engine has, asserted in markdown rather than Python."""
    report = check(spec, spec.rules)
    assert [f.title for f in report.findings] == []
    assert report.passed >= 20


def test_every_toy_rule_fires(spec):
    report = check(spec, spec.rules)
    assert [r.id for r in spec.rules if r.id not in report.rules_used] == []


# -- invariants a markdown statement cannot state -------------------------

def test_normalization_is_idempotent(rules):
    rng = random.Random(3)
    pool = ["(α α)", "α + α + α", "α^0 β α", "α^2 ** α^2", "β α^0 α γ",
            "(α) + (α)", "α α (α α α)", "α^2 ** α^-2", "α β γ + α β δ"]
    for _ in range(60):
        t = parse(rng.choice(pool))
        once = normalize(t, rules).result
        assert normalize(once, rules).result == once, show(t)


def test_normalization_terminates_and_records_a_trace(rules):
    norm = normalize(parse("(α α) (α α α)"), rules)
    assert norm.cycle is None and not norm.exhausted
    assert [s.rule_id for s in norm.steps] == ["m.contract", "m.contract"]


def test_float_and_absorb_commute(rules):
    """The two must reach one normal form or the result depends on rule order."""
    assert len(normal_forms(parse("β α^0 α γ"), rules)) == 1


def test_ladder_is_deterministic(rules):
    assert len(normal_forms(parse("α^0 ** α^2"), rules)) == 1


def test_prove_runs_an_equality_backwards(rules):
    assert prove(parse("(α β)^-1"), parse("β^-1 α^-1"), rules).status == PROVED


def test_unprovable_is_closed_not_proved(rules):
    proof = prove(parse("α α"), parse("(α α)"), rules)
    assert proof.status == CLOSED and not proof.proved


def test_budget_exhaustion_is_its_own_outcome(rules):
    """EXHAUSTED must never be reported as a disproof."""
    proof = prove(parse("α β γ + α β δ"), parse("α^99"), rules,
                  Budget(max_nodes=1, max_depth=1, max_size=4))
    assert proof.status in (EXHAUSTED, CLOSED) and not proof.proved


def test_proof_renders_a_chain(rules):
    proof = prove(parse("α^2"), parse("(α α)"), rules)
    assert proof.proved and "m.contract" in proof.render()


# -- matching -------------------------------------------------------------

def test_segment_variable_binds_a_run():
    lhs = parse("A.. X B..", pattern=True)
    subj = parse("α β γ")
    envs = list(match(lhs, subj))
    assert any(e["A"] == (atom("α"),) and e["X"] == atom("β") for e in envs)


def test_segment_variable_may_bind_nothing():
    envs = list(match(parse("A.. X B..", pattern=True), parse("α β")))
    assert any(e["A"] == () and e["B"] == (atom("β"),) for e in envs)


def test_a_one_element_sequence_is_that_element():
    """So a `seq` pattern cannot match a lone atom - there is no 1-run."""
    assert parse("α")[0] == "atom"
    assert not list(match(parse("A.. X", pattern=True), parse("α")))


def test_non_linear_pattern_needs_both_sides_equal():
    p = parse("X / X", pattern=True)
    assert list(match(p, parse("α / α")))
    assert not list(match(p, parse("α / β")))


def test_short_seq_pattern_is_opened_implicitly():
    """`X^0 X` should fire inside a longer run without a rule per context."""
    lhs, rhs = open_seq(parse("X^0 X", pattern=True), parse("X", pattern=True))
    env = next(match(lhs, parse("β α^0 α γ")))
    assert show(subst(rhs, env)) == "β α γ"


def test_a_pattern_with_its_own_segments_is_left_alone():
    lhs = parse("A.. X B..", pattern=True)
    assert open_seq(lhs, lhs)[0] == lhs


def test_segment_in_operand_position_becomes_one_sequence():
    """`A.. B + A..` - the lone `A..` is a summand, not two spliced siblings."""
    rules = load_text("## T\n\n    A.. (B + 1)  ==  A.. B + A..   # [rule] [id=u]\n",
                      "t.md").rules
    assert prove(parse("α β (γ + 1)"), parse("α β γ + α β"), rules).proved


def test_conditions_gate_a_rule():
    rules = load_text("## T\n\n    X^a -> X^0 , a > 5   # [id=c]\n", "t.md").rules
    assert nf("α^9", rules) == parse("α^0")
    assert nf("α^2", rules) == parse("α^2")


def test_condition_holds_when_a_value_is_not_statically_known():
    rules = load_text("## T\n\n    X^a -> X^0 , a > 5   # [id=c]\n", "t.md").rules
    assert nf("α^b", rules) == parse("α^b")


def test_negated_exponent_folds_to_a_literal():
    """`S^-n` after substitution must equal the literal `α^-3`."""
    rules = load_text("## T\n\n    X^n^-1 -> X^-n   # [id=i]\n", "t.md").rules
    assert nf("α^3^-1", rules) == parse("α^-3")
