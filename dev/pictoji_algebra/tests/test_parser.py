"""Form-is-substance regression tests.

If any of these start passing as equalities, the representation has quietly
begun conflating forms the algebra says are distinct.
"""

import pytest

from pictoji_algebra.parser import parse
from pictoji_algebra.terms import Add, Angled, Coeff, Div, Fusion, Group, Pow, Seq


def test_the_three_distinct_graphs():
    a, b, c = parse("(A B) C"), parse("A (B C)"), parse("A B C")
    assert a != b and b != c and a != c
    assert len({hash(a), hash(b), hash(c)}) == 3


def test_bare_run_is_not_a_fenced_run():
    assert parse("웃 웃") != parse("(웃 웃)")
    assert isinstance(parse("웃 웃"), Seq)
    assert isinstance(parse("(웃 웃)"), Group)


def test_power_is_not_a_bare_run():
    assert parse("웃^3") != parse("웃 웃 웃")


def test_middle_group_changes_the_hierarchy():
    assert parse("웃 웃^2 웃") != parse("웃 웃 웃 웃")
    assert len(parse("웃 웃^2 웃").items) == 3
    assert len(parse("웃 웃 웃 웃").items) == 4


def test_replication_is_not_an_exponent_product():
    assert parse("(웃^2)^3") != parse("웃^6")


def test_exponent_trees_are_non_commutative():
    assert parse("웃^(2 ++ 1)") != parse("웃^(1 ++ 2)")


def test_nested_exponent_trees_stay_distinct():
    assert parse("웃^((2 ++ 1) ** 2)") != parse("웃^(2 ++ (1 ** 2))")


def test_exponent_tree_repr_keeps_its_parens():
    """A trace that printed both nestings the same way would mislead."""
    assert repr(parse("웃^((2 ++ 1) ** 2)")) == "웃^((2 ++ 1) ** 2)"


def test_superscript_and_caret_are_the_same_term():
    """Two spellings of one exponent - see pictoji-test.md:47-48."""
    assert parse("웃²") == parse("웃^2")


def test_addition_is_commutative():
    assert parse("🐶 + 🏠") == parse("🏠 + 🐶")


def test_addition_operands_are_sorted_canonically():
    assert parse("🌳 + 웃 + 🐶").terms == parse("🐶 + 🌳 + 웃").terms


def test_bare_exponent_does_not_swallow_term_operators():
    """`S^2 ** S^3` must be a Fusion, not `S^(2 ** S)^3`."""
    assert isinstance(parse("S^2 ** S^3"), Fusion)
    assert isinstance(parse("S^2 / S^3"), Div)
    assert isinstance(parse("a 🫀^0 + b 🎭^0"), Add)


def test_fusion_is_right_associative():
    assert parse("A ** B ** C") == parse("A ** (B ** C)").rebuild(
        [parse("A"), parse("(B ** C)").body])


def test_leading_number_becomes_a_coefficient():
    t = parse("3 웃")
    assert isinstance(t, Coeff) and t.numeric == 3


def test_angled_is_its_own_node():
    assert isinstance(parse("(> 웃^2 웃^3 <)"), Angled)
    assert parse("(> 웃 웃 <)") != parse("(웃 웃)")


def test_fractional_exponent_is_exact():
    assert parse("웃^(1/2)").exp.value == parse("웃^(1/4)").exp.value * 2
