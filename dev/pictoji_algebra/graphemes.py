"""Unicode hygiene for Pictoji source text.

Two jobs, both of which the rest of the toolchain gets wrong today:

1. NFC normalization (`pictoji.md` "All tokens must be normalized to NFC").
2. Grapheme cluster segmentation ("Each Pictoji token represents exactly one
   Unicode grapheme cluster in its canonical form").

`pictoji/cli/__init__.py` iterates `for char in text`, i.e. per *code point*, so
it counts the spec's own examples wrong: `👩‍🚀` as 5 items and `❤️` as 2.  Every
layer above this module consumes `graphemes()` output and never a bare `str`.

Pure stdlib on purpose - the package has zero dependencies.  This is a faithful
subset of UAX#29, not the whole algorithm; see `SEGMENTATION_LIMITS`.
"""

from __future__ import annotations

import unicodedata
from pathlib import Path
from typing import List

ZWJ = "‍"

# Ranges that UAX#29 treats as Extend/SpacingMark but that Python's
# `unicodedata.category` does NOT report as a combining mark.
_VARIATION_SELECTORS = (0xFE00, 0xFE0F)
_VARIATION_SUPPLEMENT = (0xE0100, 0xE01EF)
_SKIN_TONE = (0x1F3FB, 0x1F3FF)          # EMOJI MODIFIER FITZPATRICK TYPE-1..6
_TAG_CHARS = (0xE0020, 0xE007F)          # tag sequences, e.g. subdivision flags
_REGIONAL_INDICATOR = (0x1F1E6, 0x1F1FF)

# Conjoining Hangul jamo.  `웃` (U+C6C3) is a *precomposed* syllable and NFC
# keeps it that way, so this only matters for decomposed input - which is
# exactly the input NFC is supposed to catch.
_HANGUL_L = (0x1100, 0x115F)
_HANGUL_V = (0x1160, 0x11A7)
_HANGUL_T = (0x11A8, 0x11FF)
_HANGUL_SYLLABLE = (0xAC00, 0xD7A3)

SEGMENTATION_LIMITS = """\
Not implemented (and asserted absent from the Pictoji corpus by the test suite):
UAX#29 Prepend (Cf format characters that attach rightward, e.g. Arabic number
sign U+0600) and Indic conjunct/linker clusters (InCB).  The Pictoji vocabulary
is emoji + Latin + geometric symbols + precomposed Hangul, none of which reach
those classes.  If either ever appears, `regex`'s \\X is the reference oracle -
see tests/test_graphemes.py."""


def _in(cp: int, rng) -> bool:
    return rng[0] <= cp <= rng[1]


def _is_extend(ch: str) -> bool:
    """Characters that glue onto the cluster to their left."""
    if unicodedata.category(ch) in ("Mn", "Me", "Mc"):
        return True
    cp = ord(ch)
    return (
        _in(cp, _VARIATION_SELECTORS)
        or _in(cp, _VARIATION_SUPPLEMENT)
        or _in(cp, _SKIN_TONE)
        or _in(cp, _TAG_CHARS)
    )


def _is_regional_indicator(ch: str) -> bool:
    return _in(ord(ch), _REGIONAL_INDICATOR)


def _hangul_class(ch: str) -> str:
    cp = ord(ch)
    if _in(cp, _HANGUL_L):
        return "L"
    if _in(cp, _HANGUL_V):
        return "V"
    if _in(cp, _HANGUL_T):
        return "T"
    if _in(cp, _HANGUL_SYLLABLE):
        # LV syllables sit at multiples of 28 from the block start; the rest are LVT.
        return "LV" if (cp - _HANGUL_SYLLABLE[0]) % 28 == 0 else "LVT"
    return ""


_HANGUL_JOINS = {
    "L": {"L", "V", "LV", "LVT"},
    "V": {"V", "T"},
    "LV": {"V", "T"},
    "T": {"T"},
    "LVT": {"T"},
}


def normalize(text: str) -> str:
    """NFC-normalize.  Idempotent; safe to call more than once."""
    return unicodedata.normalize("NFC", text)


def graphemes(text: str) -> List[str]:
    """Split NFC text into grapheme clusters.

    The caller is responsible for normalizing first - `read_spec` does both.
    Splitting un-normalized text is not wrong so much as meaningless, since the
    same visible string could cluster two different ways.
    """
    out: List[str] = []
    i, n = 0, len(text)

    while i < n:
        start = i
        ch = text[i]

        # CRLF is one cluster.
        if ch == "\r" and i + 1 < n and text[i + 1] == "\n":
            out.append("\r\n")
            i += 2
            continue

        # Regional indicators pair up strictly two at a time, so that a run of
        # four makes two flags rather than one blob.
        if _is_regional_indicator(ch):
            if i + 1 < n and _is_regional_indicator(text[i + 1]):
                out.append(text[i : i + 2])
                i += 2
            else:
                out.append(ch)
                i += 1
            continue

        i += 1

        # Hangul jamo chaining.
        cls = _hangul_class(ch)
        while cls and i < n:
            nxt = _hangul_class(text[i])
            if nxt and nxt in _HANGUL_JOINS.get(cls, ()):
                cls = nxt
                i += 1
            else:
                break

        # Trailing combining marks, variation selectors, skin tones, tags, and
        # ZWJ-joined continuations.
        while i < n:
            c = text[i]
            if _is_extend(c):
                i += 1
                continue
            if c == ZWJ and i + 1 < n and unicodedata.category(text[i + 1])[0] != "C":
                i += 2  # consume the joiner and whatever it joins
                continue
            break

        out.append(text[start:i])

    return out


def read_spec(path) -> str:
    """Read a Pictoji spec file: BOM-aware, NFC-normalized, newlines unified.

    `utf-8-sig` is not optional here.  `dev/README.md` and `.vscode/settings.json`
    make UTF-8-with-BOM a hard project rule, and every `.md` in the repo carries
    one - but `pictoji/cli/__init__.py:206` opens with plain `utf-8`, so it hands
    a stray U+FEFF to its caller.  We do not repeat that.
    """
    raw = Path(path).read_text(encoding="utf-8-sig")
    return normalize(raw.replace("\r\n", "\n"))


def describe(cluster: str) -> str:
    """`👩‍🚀 (U+1F469 U+200D U+1F680)` - for error messages and findings."""
    cps = " ".join("U+%04X" % ord(c) for c in cluster)
    return "%s (%s)" % (cluster, cps)
