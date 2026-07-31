"""Superscript/subscript folding and numeric strictness."""

import pytest

from pictoji_algebra.lexer import LexError, tokenize


def kinds(src):
    return [(t.kind, t.value) for t in tokenize(src)]


def test_superscript_folds_to_caret():
    assert kinds("웃²") == kinds("웃^2")
    assert kinds("🏠⁶") == kinds("🏠^6")


def test_all_ten_superscript_digits():
    """U+00B9/B2/B3 sit outside the U+2070 block; a range check mangles them."""
    for digit, sup in enumerate("⁰¹²³⁴⁵⁶⁷⁸⁹"):
        assert kinds("웃" + sup) == [("SYMBOL", "웃"), ("CARET", "^"), ("NUMBER", str(digit))]


def test_negative_superscript():
    assert kinds("웃⁻¹") == kinds("웃^-1")


def test_subscript_folds_to_underscore():
    assert kinds("웃ᵢ") == kinds("웃_i")
    assert kinds("웃₂") == kinds("웃_2")


def test_subscript_letters_span_three_blocks():
    for sub, expect in (("ₐ", "a"), ("ᵢ", "i"), ("ⱼ", "j")):
        assert kinds("웃" + sub)[-1] == ("SYMBOL", expect)


def test_raw_spelling_is_preserved_for_error_messages():
    assert tokenize("웃²")[1].raw == "²"


def test_longest_match_operators():
    assert [k for k, _ in kinds("A ** B")] == ["SYMBOL", "STARSTAR", "SYMBOL"]
    assert [k for k, _ in kinds("A ++ B")] == ["SYMBOL", "PLUSPLUS", "SYMBOL"]
    assert [k for k, _ in kinds("(> A <)")] == ["LANGLE", "SYMBOL", "RANGLE"]


def test_scientific_notation_is_one_token():
    assert kinds("6.02e23") == [("NUMBER", "6.02e23")]
    assert kinds("-5e-2") == [("MINUS", "-"), ("NUMBER", "5e-2")]


def test_comment_is_dropped():
    assert kinds("웃 # a note") == [("SYMBOL", "웃")]


@pytest.mark.parametrize("bad", [".5", "1,000"])
def test_strict_mode_rejects_bad_numbers(bad):
    with pytest.raises(LexError):
        tokenize(bad)


def test_emoji_is_a_single_symbol_token():
    assert kinds("👩‍🚀 웃") == [("SYMBOL", "👩‍🚀"), ("SYMBOL", "웃")]
