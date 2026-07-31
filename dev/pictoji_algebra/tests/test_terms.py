"""Unicode, lexing, parsing, printing - plus the properties that guard them.

Uses ASCII and Greek placeholders, never Pictoji algebra content.  The emoji
that do appear are Unicode *machinery* cases (ZWJ, VS16, flags), not vocabulary.
"""

import random
import unicodedata
from pathlib import Path

import pytest

from pictoji_algebra.terms import (
    LexError, ParseError, graphemes, normalize, parse, read_spec, show, tokenize,
)

REPO = Path(__file__).resolve().parents[3]
DEV = REPO / "dev"


def g(text):
    return graphemes(normalize(text))


# -- graphemes ------------------------------------------------------------

@pytest.mark.parametrize("text", ["a", "á", "👩‍🚀", "❤", "❤️", "🇮🇹", "1️⃣", "👍🏽"])
def test_one_cluster(text):
    """pictoji.md:4863 lists these as 1 grapheme each; the shipped analyzer
    iterates per code point and counts 👩‍🚀 as 5 and ❤️ as 2."""
    assert len(g(text)) == 1


def test_multi_codepoint_clusters_really_are_multi_codepoint():
    assert len("👩‍🚀") == 3 and len("❤️") == 2


def test_flags_pair_two_at_a_time():
    assert len(g("🇮🇹🇫🇷")) == 2


def test_nfc_composes_and_is_idempotent():
    assert normalize("á") == "á" == normalize(normalize("á"))


def test_crlf_is_one_cluster():
    assert g("\r\n") == ["\r\n"]


def test_read_spec_strips_the_bom():
    path = REPO / "pictoji-test.md"
    assert path.read_bytes()[:3] == b"\xef\xbb\xbf"
    assert not read_spec(path).startswith("﻿")


def test_corpus_has_no_prepend_or_indic_clusters():
    """The segmenter omits those UAX#29 classes; assert they cannot arise."""
    for name in ("pictoji.md", "pictoji-test.md", "dev/pictoji-test-algebra.md"):
        for ch in read_spec(REPO / name):
            assert unicodedata.category(ch) != "Cf" or ch in "‍﻿", ch


def test_matches_regex_reference_when_available():
    regex = pytest.importorskip("regex", reason="optional oracle; pip install regex")
    for name in ("pictoji.md", "dev/pictoji-test-algebra.md"):
        text = read_spec(REPO / name)
        assert graphemes(text) == regex.findall(r"\X", text), name


# -- lexing ---------------------------------------------------------------

def test_superscript_folds_to_caret():
    assert tokenize("A²") == tokenize("A^2")
    assert tokenize("A⁻¹") == tokenize("A^-1")


def test_all_ten_superscripts():
    """1/2/3 are Latin-1 leftovers outside the U+2070 block."""
    for d, sup in enumerate("⁰¹²³⁴⁵⁶⁷⁸⁹"):
        assert tokenize("A" + sup)[-1] == ("NUMBER", str(d))


def test_subscripts_span_three_blocks():
    for sub, want in (("ₐ", "a"), ("ᵢ", "i"), ("ⱼ", "j")):
        assert tokenize("A" + sub)[-1] == ("SYMBOL", want)
    assert tokenize("A₂") == tokenize("A_2")


def test_longest_match_operators():
    assert [k for k, _ in tokenize("A ** B")] == ["SYMBOL", "STARSTAR", "SYMBOL"]
    assert [k for k, _ in tokenize("A .. B")] == ["SYMBOL", "DOTDOT", "SYMBOL"]


def test_scientific_notation_is_one_token():
    assert tokenize("6.02e23") == [("NUMBER", "6.02e23")]


def test_comment_is_dropped():
    assert tokenize("A # note") == [("SYMBOL", "A")]


@pytest.mark.parametrize("bad", [".5", "1,000"])
def test_strict_number_rules(bad):
    with pytest.raises(LexError):
        tokenize(bad)


# -- form is substance ----------------------------------------------------

def test_three_distinct_graphs():
    a, b, c = parse("(A B) C"), parse("A (B C)"), parse("A B C")
    assert len({a, b, c}) == 3


def test_fence_is_not_juxtaposition():
    assert parse("A A") != parse("(A A)")


def test_power_is_not_a_bare_run():
    assert parse("A^3") != parse("A A A")


def test_middle_group_changes_arity():
    assert len(parse("A A^2 A")) - 1 == 3
    assert len(parse("A A A A")) - 1 == 4


def test_replication_is_not_an_exponent_product():
    assert parse("(A^2)^3") != parse("A^6")
    assert parse("A^(2 ++ 1)") != parse("A^(1 ++ 2)")
    assert parse("A^((2 ++ 1) ** 2)") != parse("A^(2 ++ (1 ** 2))")


def test_two_spellings_of_one_exponent_are_one_term():
    assert parse("A²") == parse("A^2")


def test_addition_is_commutative():
    assert parse("A + B") == parse("B + A")


def test_bare_exponent_does_not_swallow_term_operators():
    """`A^2 ** B^3` must be a fusion, not `A^(2 ** B)^3`."""
    assert parse("A^2 ** B^3")[0] == "fuse"
    assert parse("A^2 / B^3")[0] == "div"
    assert parse("c A^0 + d B^0")[0] == "+"


def test_value_arithmetic_folds_in_exponents_but_form_does_not():
    assert parse("A^(2 + 1)") == parse("A^3")
    assert parse("A^(2 ** 3)") != parse("A^6")


def test_parse_error_is_reported_not_swallowed():
    with pytest.raises(ParseError):
        parse("A (((")


# -- properties -----------------------------------------------------------

ATOMS = ["α", "β", "γ", "A", "B"]


def random_source(rng, depth=0):
    """Generate random *source text*, not raw tuples.

    Generating tuples directly produces terms the grammar cannot express - e.g.
    `coeff(2, div(B, 1))`, which would have to print as `2 (B / 1)` and so needs
    a fence.  Those are worth detecting, but that is the interpreter's
    `unprintable` finding, not this property.  What this asserts is the
    guarantee traces actually depend on: **anything writable round-trips.**
    """
    if depth >= 2:
        return _prim(rng, depth)
    a, b = random_source(rng, depth + 1), random_source(rng, depth + 1)
    p, q = _prim(rng, depth + 1), _prim(rng, depth + 1)
    return rng.choice([
        _prim(rng, depth),
        "%s %s" % (p, q),
        "%s + %s" % (a, b),
        "%s^%s" % (p, rng.choice(["2", "0", "-1", "(1/2)", "(2 ** 3)", "(2 ++ 1)"])),
        "%s ** %s" % (p, q),
        "%s / %s" % (p, q),
        "%s %s" % (rng.choice(["2", "3", "0"]), p),
        "%s[%s]" % (p, q),
        "%sᛠ %s" % (p, q),
        "%s^" % p,
    ])


def _prim(rng, depth):
    if depth >= 2 or rng.random() < 0.55:
        return rng.choice(ATOMS)
    return rng.choice(["(%s)", "(> %s <)"]) % random_source(rng, depth + 1)


def test_print_parse_roundtrip():
    """The printer may not insert parentheses - parens are fences - so a term
    that needs them to print has no surface form at all."""
    rng = random.Random(20260731)
    for i in range(800):
        src = random_source(rng)
        t = parse(src)
        assert parse(show(t)) == t, (
            "seed 20260731 iteration %d: %r -> %s" % (i, src, show(t)))


def test_roundtrip_of_every_spec_term():
    from pictoji_algebra.spec import load
    for name in ("pictoji-test-algebra.md", "pictoji-test-machinery.md"):
        spec = load(DEV / name)
        for a in spec.assertions:
            for t in (a.left, a.right):
                assert parse(show(t)) == t, "%s: %s" % (a.source, show(t))


def test_fractional_exponents_need_their_parens():
    """`A^1/2` re-parses as `(A^1)/2`; this silently corrupted every sub-unit
    trace until the printer started parenthesizing fractions."""
    assert show(parse("A^(1/2)")) == "A^(1/2)"
    assert parse(show(parse("A^(1/2)"))) == parse("A^(1/2)")


def test_equal_terms_hash_equal():
    rng = random.Random(7)
    for _ in range(400):
        t = parse(random_source(rng))
        assert hash(parse(show(t))) == hash(t)


def test_graphemes_join_back_to_the_source():
    rng = random.Random(11)
    pool = ["a", "á", "👩‍🚀", "❤️", "🇮🇹", "웃", "\r\n", " ", "^", "2"]
    for _ in range(300):
        s = normalize("".join(rng.choice(pool) for _ in range(rng.randint(0, 12))))
        assert "".join(graphemes(s)) == s
