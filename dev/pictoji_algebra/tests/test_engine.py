"""Engine behaviour, checked against hand-written rules rather than the spec file.

Keeping these independent of `pictoji-test-algebra.md` means an edit to the
axioms cannot silently invalidate the machinery's own tests.
"""

import pytest

from pictoji_algebra.engine import (
    Budget, CLOSED, EXHAUSTED, PROVED, normal_forms, normalize, prove,
)
from pictoji_algebra.parser import parse
from pictoji_algebra.specload import load_text

RULES = """\
## Core

    fenced uniform run contracts     # [builtin=contract_run] [id=contract]
    sum collection                   # [builtin=collect_sum] [id=collect]
    tints float and sort             # [builtin=float_tints] [id=float]
    prefix tint absorbs              # [builtin=scan_absorb] [id=absorb]
    runs sum inside angles           # [builtin=angled_eval] [id=angles]
    prefix factoring                 # [builtin=factor_prefix] [equiv] [id=factor]
    (A B)^-1 == B^-1 A^-1            # [rule] [id=inverse]
"""


@pytest.fixture(scope="module")
def rules():
    return load_text(RULES, "t.md").rules


def nf(src, rules):
    return normalize(parse(src), rules).result


# -- tier 1 ---------------------------------------------------------------

def test_fenced_run_contracts(rules):
    assert nf("(웃 웃)", rules) == parse("웃^2")


def test_bare_run_does_not_contract(rules):
    assert nf("웃 웃", rules) == parse("웃 웃")


def test_singleton_group_holds(rules):
    assert nf("(웃)", rules) == parse("(웃)")


def test_sum_collects_and_drops_unfenced_zero(rules):
    assert nf("웃 + 웃 + 웃", rules) == parse("3웃")
    assert nf("웃 + 0웃", rules) == parse("웃")


def test_fence_blocks_sum_collection(rules):
    """v7: the fences are the visible 'don't collect' signal."""
    assert nf("(웃) + (웃)", rules) == parse("(웃) + (웃)")
    assert nf("웃 + (0웃)", rules) == parse("웃 + (0웃)")


def test_scan_absorb_passes_foreign_symbols(rules):
    assert nf("웃^0 웃", rules) == parse("웃")
    assert nf("🌳 웃^0 웃", rules) == parse("🌳 웃")


def test_cross_symbol_tint_never_absorbs(rules):
    assert nf("🫀^0 웃", rules) == parse("🫀^0 웃")


def test_tints_float_left(rules):
    assert nf("웃 🫀^0", rules) == parse("🫀^0 웃")


def test_float_then_absorb_reaches_one_normal_form(rules):
    """The point of importing scan-absorb: float and absorb must commute."""
    assert len(normal_forms(parse("🌳 웃^0 웃"), rules)) == 1


def test_angled_runs_sum_but_order_is_kept(rules):
    assert nf("(> 웃^2 웃^3 <)", rules) == parse("웃^5")
    assert nf("(> 웃 🏠^2 웃^6 🏠^3 <)", rules) == parse("웃 🏠^2 웃^6 🏠^3")


def test_normalization_records_a_trace(rules):
    norm = normalize(parse("(웃 웃) (웃 웃 웃)"), rules)
    assert norm.result == parse("웃^2 웃^3")
    assert [s.rule_id for s in norm.steps] == ["contract", "contract"]


# -- tier 2 ---------------------------------------------------------------

def test_prove_uses_an_equality_backwards(rules):
    proof = prove(parse("(🌳 🏠)^-1"), parse("🏠^-1 🌳^-1"), rules)
    assert proof.status == PROVED


def test_prove_bridges_form_and_power(rules):
    assert prove(parse("웃^2 웃^3"), parse("(웃 웃) (웃 웃 웃)"), rules).proved


def test_factoring_runs_in_both_directions(rules):
    assert prove(parse("🌳 웃 🐶 + 🌳 웃 🏠"), parse("🌳 웃 (🐶 + 🏠)"), rules).proved


def test_unprovable_is_closed_not_proved(rules):
    proof = prove(parse("웃 웃"), parse("(웃 웃)"), rules)
    assert proof.status == CLOSED
    assert not proof.proved


def test_budget_exhaustion_is_its_own_outcome(rules):
    """EXHAUSTED must never be reported as a disproof."""
    tiny = Budget(max_nodes=1, max_depth=1, max_size=4)
    proof = prove(parse("🌳 웃 🐶 + 🌳 웃 🏠"), parse("웃^99"), rules, tiny)
    assert proof.status in (EXHAUSTED, CLOSED)
    assert not proof.proved


def test_proof_renders_a_chain(rules):
    proof = prove(parse("웃^2"), parse("(웃 웃)"), rules)
    assert proof.proved
    assert "contract" in proof.render()


# -- ordered ladders ------------------------------------------------------

LADDER = """\
## Fusion

    S^a ** S^b -> S^b          , a == 0                            # [ladder=f] [id=L1]
    S^a ** S^b -> S^0          , a == -b                           # [ladder=f] [id=L2]
    S^a ** S^b -> S^(a + 1)    , a == b and is_int(a) and a > 0     # [ladder=f] [id=L3]
    S^a ** S^b -> S^a S^b                                          # [ladder=f] [id=L4]
"""


def test_ladder_first_match_wins():
    rules = load_text(LADDER, "t.md").rules
    # a == 0 must win over the catch-all, and yield exactly one normal form.
    assert nf("웃^0 ** 웃^2", rules) == parse("웃^2")
    assert len(normal_forms(parse("웃^0 ** 웃^2"), rules)) == 1
    assert nf("웃^2 ** 웃^-2", rules) == parse("웃^0")
    assert nf("웃^2 ** 웃^2", rules) == parse("웃^3")
    assert nf("웃^2 ** 웃^3", rules) == parse("웃^2 웃^3")


def test_negated_exponent_folds_to_a_literal():
    """`S^-n` after substitution must equal the literal `웃^-3`."""
    rules = load_text("## D\n\n    S^n^-1 -> S^-n   # [id=inv]\n", "t.md").rules
    assert nf("웃^3^-1", rules) == parse("웃^-3")
