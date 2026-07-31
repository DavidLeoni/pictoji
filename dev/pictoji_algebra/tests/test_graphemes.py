"""The spec's own Unicode examples, which the shipped analyzer gets wrong."""

import unicodedata
from pathlib import Path

import pytest

from pictoji_algebra.graphemes import graphemes, normalize, read_spec

REPO = Path(__file__).resolve().parents[3]


def g(text):
    return graphemes(normalize(text))


# The five examples listed at pictoji.md:4863-4869, all "1 grapheme".
@pytest.mark.parametrize("text", ["a", "á", "👩‍🚀", "❤", "❤️"])
def test_spec_examples_are_one_cluster(text):
    assert len(g(text)) == 1


def test_zwj_sequence_is_not_five_codepoints():
    # `pictoji/cli/__init__.py:225` iterates per code point and counts this 5.
    assert len("👩‍🚀") == 3
    assert len(g("👩‍🚀")) == 1


def test_vs16_attaches_to_its_base():
    assert len("❤️") == 2
    assert len(g("❤️")) == 1
    assert g("❤️")[0] == "❤️"


def test_nfc_composes_decomposed_input():
    decomposed = "á"
    assert normalize(decomposed) == "á"
    assert len(g(decomposed)) == 1


def test_flags_pair_two_at_a_time():
    assert len(g("🇮🇹")) == 1
    assert len(g("🇮🇹🇫🇷")) == 2


def test_keycap_and_skin_tone():
    assert len(g("1️⃣")) == 1
    assert len(g("👍🏽")) == 1


def test_crlf_is_one_cluster():
    assert g("\r\n") == ["\r\n"]


def test_hangul_syllable_is_precomposed_after_nfc():
    assert [hex(ord(c)) for c in normalize("웃")] == ["0xc6c3"]
    assert len(g("웃 웃")) == 3        # symbol, space, symbol


def test_read_spec_strips_bom():
    # Every .md in the repo is UTF-8 with BOM; `pictoji/cli/__init__.py:206`
    # opens with plain utf-8 and leaks the U+FEFF into its caller.
    path = REPO / "pictoji-test.md"
    assert path.read_bytes()[:3] == b"\xef\xbb\xbf"
    assert not read_spec(path).startswith("﻿")


def test_no_prepend_or_indic_clusters_in_the_corpus():
    """The segmenter omits UAX#29 Prepend and InCB; assert they cannot arise."""
    for name in ("pictoji.md", "pictoji-test.md", "dev/pictoji-test-algebra.md"):
        text = read_spec(REPO / name)
        for ch in text:
            assert unicodedata.category(ch) != "Cf" or ch in "‍﻿", (
                "%r (%s) is a format char the segmenter does not classify"
                % (ch, unicodedata.name(ch, "?")))


def test_matches_regex_reference_when_available():
    """Cross-check against UAX#29 proper, if `regex` happens to be installed."""
    regex = pytest.importorskip("regex", reason="optional oracle; pip install regex")
    for name in ("pictoji.md", "pictoji-test.md", "dev/pictoji-test-algebra.md"):
        text = read_spec(REPO / name)
        assert graphemes(text) == regex.findall(r"\X", text), name
