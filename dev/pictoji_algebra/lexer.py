"""Graphemes -> tokens.

Consumes `graphemes.graphemes()` output, never a bare `str`, so a ZWJ emoji is
one SYMBOL rather than five.

Superscript and subscript digits are folded to canonical `^n` / `_n` here, at
lex time, so `웃²` and `웃^2` produce identical token streams and therefore
identical terms.  This is deliberate and is *not* a form-is-substance violation:
they are two spellings of one exponent, and `pictoji-test.md:47-48` asserts them
equal.  The original spelling survives on `Token.raw` for error messages.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import List, Optional

from .graphemes import describe, graphemes, normalize

# --- superscripts -----------------------------------------------------------
# NOT a contiguous range: 1/2/3 are Latin-1 leftovers (U+00B9/B2/B3) while the
# rest live in U+2070..2079.  A range check here silently mangles `웃²`.
SUPERSCRIPT_DIGITS = {
    "⁰": "0", "¹": "1", "²": "2", "³": "3", "⁴": "4",
    "⁵": "5", "⁶": "6", "⁷": "7", "⁸": "8", "⁹": "9",
}
SUPERSCRIPT_SIGNS = {"⁺": "+", "⁻": "-"}

# --- subscripts -------------------------------------------------------------
SUBSCRIPT_DIGITS = {chr(0x2080 + d): str(d) for d in range(10)}
# Subscript letters are scattered across three blocks; another place a range
# check would quietly do the wrong thing.
SUBSCRIPT_LETTERS = {
    "ₐ": "a", "ₑ": "e", "ₒ": "o", "ₓ": "x",
    "ₕ": "h", "ₖ": "k", "ₗ": "l", "ₘ": "m",
    "ₙ": "n", "ₚ": "p", "ₛ": "s", "ₜ": "t",
    "ᵢ": "i", "ᵣ": "r", "ᵤ": "u", "ᵥ": "v",
    "ⱼ": "j",
}

DIGITS = set("0123456789")

# Multi-grapheme operators, longest first so `**` never lexes as two `*`.
OPERATORS = [
    ("k->", "KARROW"),
    ("~>", "NARROW"),
    ("¬==", "NEQ"),
    ("¬⊆", "NSUBSET"),
    ("¬=", "NEQ"),
    ("!=", "NEQ"),
    ("==", "EQ"),
    ("->", "ARROW"),
    ("<-", "COND"),
    ("(>", "LANGLE"),
    ("<)", "RANGLE"),
    ("//", "DSLASH"),
    ("**", "STARSTAR"),
    ("++", "PLUSPLUS"),
    ("--", "MINUSMINUS"),
    ("=", "DEF"),
    ("(", "LPAREN"),
    (")", "RPAREN"),
    ("[", "LBRACK"),
    ("]", "RBRACK"),
    ("{", "LBRACE"),
    ("}", "RBRACE"),
    ("^", "CARET"),
    ("_", "USCORE"),
    ("+", "PLUS"),
    ("-", "MINUS"),
    ("*", "STAR"),
    ("/", "SLASH"),
    ("⊆", "SUBSET"),
    ("¬", "NOT"),
    ("ᛠ", "ADJ"),
    ("°", "DEGREE"),
    (",", "COMMA"),
    ("|", "PIPE"),
    (".", "DOT"),
]


class LexError(Exception):
    def __init__(self, message: str, index: int, cluster: str = ""):
        detail = " at grapheme %d" % index
        if cluster:
            detail += ": %s" % describe(cluster)
        super().__init__(message + detail)
        self.message = message
        self.index = index
        self.cluster = cluster


@dataclass(frozen=True)
class Token:
    kind: str
    value: str
    index: int                      # grapheme offset in the source line
    raw: str = ""                   # what the user actually typed
    space_before: bool = False      # see note in `tokenize`

    def __repr__(self) -> str:      # keeps pytest failure output readable
        return "%s(%r)" % (self.kind, self.value)


def _scan_number(gs: List[str], i: int) -> Optional[int]:
    """Return the end index of a numeric token starting at `i`, else None.

    Grammar per `pictoji.md:906`: `[0-9]+(\\.[0-9]+)?([eE][-+]?[0-9]+)?`.
    The leading sign is deliberately NOT consumed - the parser builds negation,
    which keeps `a -1` and `a - 1` from lexing differently.
    """
    n = len(gs)
    if i >= n or gs[i] not in DIGITS:
        return None
    j = i
    while j < n and gs[j] in DIGITS:
        j += 1
    if j < n and gs[j] == "." and j + 1 < n and gs[j + 1] in DIGITS:
        j += 1
        while j < n and gs[j] in DIGITS:
            j += 1
    if j < n and gs[j] in ("e", "E"):
        k = j + 1
        if k < n and gs[k] in ("+", "-"):
            k += 1
        if k < n and gs[k] in DIGITS:
            while k < n and gs[k] in DIGITS:
                k += 1
            j = k
    return j


def tokenize(source: str, strict: bool = True) -> List[Token]:
    """Lex one Pictoji statement.

    `space_before` is recorded but not otherwise used yet.  `pictoji.md:4875`
    makes concatenation (`웃웃`) meaningful in the natural-language layer, while
    algebra v7 writes every sequence spaced and never contrasts the two - so the
    algebra treats `웃웃` and `웃 웃` alike, and the flag is what a future rule
    would need to stop doing that.  Recording it now costs nothing; recovering
    it later would mean re-lexing.
    """
    gs = graphemes(normalize(source))
    out: List[Token] = []
    i, n = 0, len(gs)
    pending_space = False

    while i < n:
        g = gs[i]

        if g.isspace():
            pending_space = True
            i += 1
            continue

        if g == "#":                                   # comment to end of line
            break

        start = i
        space, pending_space = pending_space, False

        # --- superscript run -> CARET + signed number ----------------------
        if g in SUPERSCRIPT_DIGITS or g in SUPERSCRIPT_SIGNS:
            digits, j = "", i
            while j < n and (gs[j] in SUPERSCRIPT_DIGITS or gs[j] in SUPERSCRIPT_SIGNS):
                digits += SUPERSCRIPT_DIGITS.get(gs[j]) or SUPERSCRIPT_SIGNS[gs[j]]
                j += 1
            raw = "".join(gs[i:j])
            body = digits.lstrip("+-")
            if not body:
                raise LexError("superscript sign with no digits", i, raw)
            out.append(Token("CARET", "^", start, raw, space))
            if digits[0] == "-":
                out.append(Token("MINUS", "-", start, raw))
            out.append(Token("NUMBER", body, start, raw))
            i = j
            continue

        # --- subscript run -> USCORE + index -------------------------------
        if g in SUBSCRIPT_DIGITS or g in SUBSCRIPT_LETTERS:
            body, j = "", i
            while j < n and (gs[j] in SUBSCRIPT_DIGITS or gs[j] in SUBSCRIPT_LETTERS):
                body += SUBSCRIPT_DIGITS.get(gs[j]) or SUBSCRIPT_LETTERS[gs[j]]
                j += 1
            raw = "".join(gs[i:j])
            out.append(Token("USCORE", "_", start, raw, space))
            kind = "NUMBER" if body[0] in DIGITS else "SYMBOL"
            out.append(Token(kind, body, start, raw))
            i = j
            continue

        # --- numbers -------------------------------------------------------
        end = _scan_number(gs, i)
        if end is not None:
            value = "".join(gs[i:end])
            if strict and end < n and gs[end] == ",":
                raise LexError("grouping separator not allowed in numbers", i, value)
            out.append(Token("NUMBER", value, start, value, space))
            i = end
            continue

        if strict and g == "." and i + 1 < n and gs[i + 1] in DIGITS:
            raise LexError("bare decimal is invalid; write 0.5 not .5", i, g)

        # --- operators (longest match) -------------------------------------
        matched = False
        for text, kind in OPERATORS:
            width = len(graphemes(text))
            if gs[i : i + width] == list(graphemes(text)):
                out.append(Token(kind, text, start, text, space))
                i += width
                matched = True
                break
        if matched:
            continue

        # --- anything else is a symbol: emoji, letter, geometric shape ------
        out.append(Token("SYMBOL", g, start, g, space))
        i += 1

    return out
