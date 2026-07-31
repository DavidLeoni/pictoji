"""Text -> terms -> text.  Graphemes, lexing, s-expressions, parsing, printing.

Terms are plain tuples: `("seq", a, b, c)`, `("group", x)`, `("pow", b, e)`,
`("atom", "웃")`.  A child is a tuple; anything else is a literal.  Hashing,
structural equality and immutability come free, and form-is-substance falls out
of tuple equality: `("seq",A,A) != ("group",("seq",A,A))` with no axiom.

The printer may never insert parentheses, because parentheses are FENCES.  So
`parse(show(t)) == t` is not cosmetic - it is a check that nothing fabricates a
term with no surface form.  `("seq", A, ("+", B, C))` has no spelling: writing
`A (B + C)` would add a fence and change the meaning.
"""

from __future__ import annotations

import unicodedata
from decimal import Decimal
from fractions import Fraction
from pathlib import Path

ZWJ = "‍"


# --------------------------------------------------------------------------
# graphemes
# --------------------------------------------------------------------------

def _extend(ch):
    """Glues onto the cluster to its left.  `unicodedata.category` misses
    variation selectors, skin tones and tag chars, hence the explicit ranges."""
    if unicodedata.category(ch) in ("Mn", "Me", "Mc"):
        return True
    c = ord(ch)
    return (0xFE00 <= c <= 0xFE0F or 0xE0100 <= c <= 0xE01EF
            or 0x1F3FB <= c <= 0x1F3FF or 0xE0020 <= c <= 0xE007F)


def _ri(ch):
    return 0x1F1E6 <= ord(ch) <= 0x1F1FF


def normalize(text):
    return unicodedata.normalize("NFC", text)


def graphemes(text):
    """Split NFC text into grapheme clusters.

    A faithful subset of UAX#29: ZWJ sequences, variation selectors, combining
    marks, skin tones, keycaps, regional-indicator pairs, tag sequences, CRLF.
    Prepend and Indic conjuncts are omitted; test_terms asserts the corpus
    cannot reach them.
    """
    out, i, n = [], 0, len(text)
    while i < n:
        start, ch = i, text[i]
        if ch == "\r" and i + 1 < n and text[i + 1] == "\n":
            out.append("\r\n"); i += 2; continue
        if _ri(ch):                       # flags pair strictly two at a time
            step = 2 if (i + 1 < n and _ri(text[i + 1])) else 1
            out.append(text[i : i + step]); i += step; continue
        i += 1
        while i < n:
            c = text[i]
            if _extend(c):
                i += 1
            elif c == ZWJ and i + 1 < n and unicodedata.category(text[i + 1])[0] != "C":
                i += 2                    # consume the joiner and what it joins
            else:
                break
        out.append(text[start:i])
    return out


def read_spec(path):
    """BOM-aware and NFC-normalized.  Every .md in this repo carries a BOM."""
    return normalize(Path(path).read_text(encoding="utf-8-sig").replace("\r\n", "\n"))


def describe(cluster):
    return "%s (%s)" % (cluster, " ".join("U+%04X" % ord(c) for c in cluster))


# --------------------------------------------------------------------------
# lexing
# --------------------------------------------------------------------------

# NOT contiguous ranges: superscript 1/2/3 are Latin-1 leftovers and subscript
# letters span three blocks.  A range check silently mangles `웃²` and `웃ᵢ`.
SUPER = dict(zip("⁰¹²³⁴⁵⁶⁷⁸⁹", "0123456789"), **{"⁺": "+", "⁻": "-"})
SUB = dict(zip("₀₁₂₃₄₅₆₇₈₉", "0123456789"))
SUB.update({"ₐ": "a", "ₑ": "e", "ₒ": "o", "ₓ": "x", "ₕ": "h", "ₖ": "k", "ₗ": "l",
            "ₘ": "m", "ₙ": "n", "ₚ": "p", "ₛ": "s", "ₜ": "t", "ᵢ": "i", "ᵣ": "r",
            "ᵤ": "u", "ᵥ": "v", "ⱼ": "j"})
DIGITS = set("0123456789")

# Longest first, so `**` never lexes as two `*`.
OPS = [("k->", "ARROW"), ("~>", "NARROW"), ("¬==", "NEQ"), ("¬⊆", "NSUBSET"),
       ("¬=", "NEQ"), ("!=", "NEQ"), ("==", "EQ"), ("->", "ARROW"), ("<-", "COND"),
       ("(>", "LANGLE"), ("<)", "RANGLE"), ("..", "DOTDOT"), ("//", "SLASH"),
       ("**", "STARSTAR"), ("++", "PLUSPLUS"), ("--", "MINUSMINUS"), ("=", "DEF"),
       ("(", "LPAREN"), (")", "RPAREN"), ("[", "LBRACK"), ("]", "RBRACK"),
       ("{", "LBRACE"), ("}", "RBRACE"), ("^", "CARET"), ("_", "USCORE"),
       ("+", "PLUS"), ("-", "MINUS"), ("*", "STAR"), ("/", "SLASH"),
       ("⊆", "SUBSET"), ("¬", "NOT"), ("ᛠ", "ADJ"), ("°", "DEGREE"),
       (",", "COMMA"), ("|", "PIPE"), (".", "DOT")]
OPS = [(graphemes(t), t, k) for t, k in OPS]


class LexError(Exception):
    pass


def _number_end(gs, i):
    """`[0-9]+(\\.[0-9]+)?([eE][-+]?[0-9]+)?` per pictoji.md:906.  The sign is
    left to the parser so `a -1` and `a - 1` cannot lex differently."""
    n = len(gs)
    if i >= n or gs[i] not in DIGITS:
        return None
    j = i
    while j < n and gs[j] in DIGITS:
        j += 1
    if j + 1 < n and gs[j] == "." and gs[j + 1] in DIGITS:
        j += 1
        while j < n and gs[j] in DIGITS:
            j += 1
    if j < n and gs[j] in "eE":
        k = j + 1 + (1 if j + 1 < n and gs[j + 1] in "+-" else 0)
        if k < n and gs[k] in DIGITS:
            while k < n and gs[k] in DIGITS:
                k += 1
            j = k
    return j


def tokenize(source, strict=True):
    """Lex one statement into `(kind, value)` pairs.

    Superscripts and subscripts fold to canonical `^n` / `_n` here, so `웃²` and
    `웃^2` produce identical tokens.  Two spellings of one exponent are one
    term; pictoji-test.md:47-48 asserts exactly that.
    """
    gs, out, i = graphemes(normalize(source)), [], 0
    n = len(gs)
    while i < n:
        g = gs[i]
        if g.isspace():
            i += 1; continue
        if g == "#":
            break

        if g in SUPER:                                   # 웃² -> 웃 ^ 2
            j = i
            body = ""
            while j < n and gs[j] in SUPER:
                body += SUPER[gs[j]]; j += 1
            digits = body.lstrip("+-")
            if not digits:
                raise LexError("superscript sign with no digits: %s" % describe(g))
            out.append(("CARET", "^"))
            if body[0] == "-":
                out.append(("MINUS", "-"))
            out.append(("NUMBER", digits))
            i = j; continue

        if g in SUB:                                     # 웃ᵢ -> 웃 _ i
            j, body = i, ""
            while j < n and gs[j] in SUB:
                body += SUB[gs[j]]; j += 1
            out.append(("USCORE", "_"))
            out.append(("NUMBER" if body[0] in DIGITS else "SYMBOL", body))
            i = j; continue

        end = _number_end(gs, i)
        if end is not None:
            value = "".join(gs[i:end])
            if strict and end < n and gs[end] == ",":
                raise LexError("grouping separator not allowed in numbers: %s" % value)
            out.append(("NUMBER", value)); i = end; continue

        if strict and g == "." and i + 1 < n and gs[i + 1] in DIGITS:
            raise LexError("bare decimal is invalid; write 0.5 not .5")

        for pat, text, kind in OPS:
            if gs[i : i + len(pat)] == pat:
                out.append((kind, text)); i += len(pat); break
        else:
            out.append(("SYMBOL", g)); i += 1
    return out


# --------------------------------------------------------------------------
# terms
# --------------------------------------------------------------------------

def kids(t):
    return [x for x in t[1:] if isinstance(x, tuple)]


def rebuild(t, new):
    out, it = [t[0]], iter(new)
    return tuple(out + [next(it) if isinstance(x, tuple) else x for x in t[1:]])


def atom(name):
    return ("atom", name)


def num(v):
    return ("num", Fraction(v))


def var(name, kind="term"):
    return ("?", name, kind)


def segvar(name):
    return ("?..", name)


def is_var(t):
    return isinstance(t, tuple) and t[0] == "?"


def is_seg(t):
    return isinstance(t, tuple) and t[0] == "?.."


def seq(items):
    """A one-element sequence is that element; nothing else collapses."""
    items = tuple(items)
    return items[0] if len(items) == 1 else ("seq",) + items


def add(terms):
    """Sums flatten and sort.  The one place order is not substance - v7 states
    outright that `+` is associative and commutative."""
    flat = []
    for t in terms:
        flat.extend(t[1:] if isinstance(t, tuple) and t[0] == "+" else [t])
    return flat[0] if len(flat) == 1 else ("+",) + tuple(sorted(flat, key=show))


def walk(t, path=()):
    yield path, t
    for i, c in enumerate(kids(t)):
        for p, s in walk(c, path + (i,)):
            yield p, s


def replace(t, path, new):
    if not path:
        return new
    ks = kids(t)
    ks[path[0]] = replace(ks[path[0]], path[1:], new)
    return rebuild(t, ks)


def size(t):
    return 1 + sum(size(c) for c in kids(t))


def numeric(t):
    """The exact value of a numeric term, else None."""
    if isinstance(t, tuple):
        if t[0] == "num":
            return t[1]
        if t[0] == "neg" and t[1][0] == "num":
            return -t[1][1]
    return None


def grade(t):
    """Structural level, or None when not statically known.  Drives division's
    dispatch (`grade(D) != 0` picks fusion, 0 picks removal)."""
    h = t[0]
    if h == "atom":
        return Fraction(1)
    if h in ("num", "adj"):
        return Fraction(0)
    if h == "pow":
        return numeric(t[2])
    if h in ("group", "angle"):
        return grade(t[1])
    if h == "coeff":
        return grade(t[2])
    if h == "seq":
        parts = [grade(x) for x in t[1:]]
        return None if any(p is None for p in parts) else sum(parts)
    return None


def is_typed_one(t):
    return t[0] == "pow" and numeric(t[2]) == 0


def is_typed_zero(t):
    return t[0] == "coeff" and numeric(t[1]) == 0


def base_symbol(t):
    """The base a power is taken over.  `S^n` -> `S`; a fenced compound is its
    own base."""
    if t[0] == "pow":
        return t[1]
    if t[0] in ("atom", "group"):
        return t
    if t[0] == "coeff":
        return base_symbol(t[2])
    return None


# --------------------------------------------------------------------------
# printing
# --------------------------------------------------------------------------

def _frac(v):
    return str(v.numerator) if v.denominator == 1 else "%d/%d" % (v.numerator, v.denominator)


def show(t):
    if not isinstance(t, tuple):
        return str(t)
    h = t[0]
    if h == "atom":
        return t[1]
    if h == "num":
        return _frac(t[1])
    if h == "?":
        return t[1]
    if h == "?..":
        return t[1] + ".."
    if h == "empty":
        return "{}"
    if h == "seq":
        return " ".join(show(x) for x in t[1:])
    if h == "group":
        return "(%s)" % show(t[1])
    if h == "angle":
        return "(> %s <)" % show(t[1])
    if h == "+":
        return " + ".join(show(x) for x in t[1:])
    if h == "coeff":
        return "%s %s" % (show(t[1]), show(t[2]))
    if h == "pow":
        return "%s^%s" % (show(t[1]), _exp(t[2]))
    if h == "exp":
        return "%s %s %s" % (_nest(t[2]), t[1], _nest(t[3]))
    if h == "fuse":
        return "%s ** %s" % (show(t[1]), show(t[2]))
    if h == "div":
        return "%s / %s" % (show(t[1]), show(t[2]))
    if h == "neg":
        return "-%s" % show(t[1])
    if h == "adj":
        return "%sᛠ" % show(t[1])
    if h == "filter":
        return "%s[%s]" % (show(t[1]), show(t[2]))
    if h == "type":
        return "%s^" % show(t[1])
    if h == "subset":
        return "%s %s %s" % (show(t[1]), "¬⊆" if t[2] else "⊆", show(t[3]))
    raise ValueError("no surface form for %r" % (t,))


def _exp(e):
    """An exponent is bare only if it is a single token.  A FRACTION is not:
    `웃^1/2` re-parses as `(웃^1)/2`, which silently corrupted every sub-unit
    fusion trace before this was fixed."""
    if e[0] in ("?", "atom") or (e[0] == "num" and e[1].denominator == 1):
        return show(e)
    if e[0] == "neg" and e[1][0] in ("atom", "?"):
        return show(e)
    return "(%s)" % show(e)


def _nest(e):
    """`(2 ++ 1) ** 2` and `2 ++ (1 ** 2)` are different exponents; a trace that
    printed both the same way would be actively misleading."""
    return "(%s)" % show(e) if e[0] == "exp" else show(e)


# --------------------------------------------------------------------------
# parsing
# --------------------------------------------------------------------------
#
# Precedence, loosest to tightest:
#     ⊆   +/-   / //   **(right)   juxtaposition   postfix ^ [] ᛠ _   atoms
#
# Inside `^(...)` the operators mean different things: `**` and `++` build
# structure and never fold, while `+ - * /` are value arithmetic and fold
# eagerly.  v7: `웃^(2+1) == 웃^3` but `웃^(2 ** 3) != 웃^6`.

TERM_VARS = set("SABCDEFGHTXYZPQRUVWNM")
NUM_VARS = set("abnmkrghijpq")
SCALAR_VARS = set("cd")


class ParseError(Exception):
    pass


class Parser:
    def __init__(self, toks, source, pattern=False):
        self.toks, self.i, self.source, self.pattern = toks, 0, source, pattern

    def peek(self):
        return self.toks[self.i] if self.i < len(self.toks) else (None, None)

    def at(self, *kinds):
        return self.peek()[0] in kinds

    def take(self, *kinds):
        k, v = self.peek()
        if k not in kinds:
            raise ParseError("expected %s, got %r in: %s"
                             % ("/".join(kinds), v, self.source))
        self.i += 1
        return v

    def accept(self, *kinds):
        return self.take(*kinds) if self.at(*kinds) else None

    def parse(self):
        t = self.expr()
        if self.peek()[0] is not None:
            raise ParseError("trailing input %r in: %s" % (self.peek()[1], self.source))
        return t

    def expr(self):
        left = self.sum_()
        if self.at("SUBSET", "NSUBSET"):
            neg = self.take("SUBSET", "NSUBSET") != "⊆"
            return ("subset", left, neg, self.sum_())
        return left

    def sum_(self):
        parts = [self.division()]
        while self.at("PLUS", "MINUS"):
            neg = self.take("PLUS", "MINUS") == "-"
            rhs = self.division()
            parts.append(("neg", rhs) if neg else rhs)
        return add(parts) if len(parts) > 1 else parts[0]

    def division(self):
        left = self.fusion()
        while self.at("SLASH"):
            self.take("SLASH")
            left = ("div", left, self.fusion())
        return left

    def fusion(self):
        left = self.juxta()
        return ("fuse", left, self.fusion()) if self.accept("STARSTAR") else left

    def juxta(self):
        items = [self.postfix()]
        while self.at("SYMBOL", "NUMBER", "LPAREN", "LANGLE", "LBRACE"):
            items.append(self.postfix())
        if len(items) == 1:
            return items[0]
        head = items[0]
        if head[0] == "num" or (is_var(head) and head[2] == "scalar"):
            return ("coeff", head, seq(items[1:]))
        return seq(items)

    def postfix(self):
        t = self.primary()
        while True:
            if self.at("CARET"):
                self.take("CARET")
                t = ("pow", t, self.exponent()) if self.at(
                    "NUMBER", "SYMBOL", "LPAREN", "MINUS") else ("type", t)
            elif self.at("LBRACK"):
                self.take("LBRACK")
                spec = self.expr()
                self.take("RBRACK")
                t = ("filter", t, spec)
            elif self.at("ADJ"):
                self.take("ADJ")
                t = ("adj", t)
            elif self.at("USCORE"):
                self.take("USCORE")
                idx = self.take("SYMBOL", "NUMBER")
                t = atom("%s_%s" % (t[1] if t[0] == "atom" else show(t), idx))
            elif self.at("DOTDOT") and is_var(t):
                self.take("DOTDOT")
                t = segvar(t[1])              # `A..` binds a run of siblings
            else:
                return t

    def primary(self):
        k, v = self.peek()
        if k is None:
            raise ParseError("unexpected end of expression in: %s" % self.source)
        if k == "LPAREN":
            self.take("LPAREN")
            if self.at("RPAREN"):
                self.take("RPAREN")
                return ("group", ("empty",))
            body = self.expr()
            self.take("RPAREN")
            return ("group", body)
        if k == "LANGLE":
            self.take("LANGLE")
            body = self.expr()
            self.take("RANGLE")
            return ("angle", body)
        if k == "LBRACE":
            self.take("LBRACE")
            if self.at("RBRACE"):
                self.take("RBRACE")
                return ("empty",)
            body = self.expr()
            self.take("RBRACE")
            return ("group", body)
        if k == "NUMBER":
            self.take("NUMBER")
            return num(Fraction(Decimal(v)))
        if k == "MINUS":
            self.take("MINUS")
            inner = self.postfix()
            # A negated literal folds, so `num(-1)` is the ONLY representation
            # of minus one.  Leaving `("neg", num(1))` around gives one value
            # two terms, which breaks structural equality and round-tripping.
            return num(-inner[1]) if inner[0] == "num" else ("neg", inner)
        if k == "SYMBOL":
            self.take("SYMBOL")
            return self.symbol(v)
        raise ParseError("unexpected %r in: %s" % (v, self.source))

    def symbol(self, name):
        if self.pattern and len(name) == 1:
            for s, kind in ((SCALAR_VARS, "scalar"), (NUM_VARS, "num"), (TERM_VARS, "term")):
                if name in s:
                    return var(name, kind)
        return atom(name)

    # -- exponents ---------------------------------------------------------
    def exponent(self):
        """A bare exponent is one atom; structured ones need parens.  Otherwise
        `S^2 ** S^3` parses as `S^(2 ** S)^3` - the exponent grammar eats the
        term-level operator.  v7 parenthesizes every structured exponent."""
        if self.at("LPAREN"):
            self.take("LPAREN")
            body = self.exp_tree()
            self.take("RPAREN")
            return body
        return self.exp_atom()

    def exp_tree(self):
        left = self.exp_sum()
        while self.at("PLUSPLUS", "MINUSMINUS"):
            # `--` is sugar: `g -- h := g ++ (-h)`, desugared so the rule set
            # only ever talks about `++`.
            sugar = self.take("PLUSPLUS", "MINUSMINUS") == "--"
            right = self.exp_sum()
            left = ("exp", "++", left, ("neg", right) if sugar else right)
        return left

    def exp_sum(self):
        left = self.exp_fuse()
        while self.at("PLUS", "MINUS"):
            left = fold(self.take("PLUS", "MINUS"), left, self.exp_fuse())
        return left

    def exp_fuse(self):
        left = self.exp_mul()
        return ("exp", "**", left, self.exp_fuse()) if self.accept("STARSTAR") else left

    def exp_mul(self):
        left = self.exp_atom()
        while self.at("STAR", "SLASH"):
            left = fold(self.take("STAR", "SLASH"), left, self.exp_atom())
        return left

    def exp_atom(self):
        if self.accept("MINUS"):
            inner = self.exp_atom()
            return num(-inner[1]) if inner[0] == "num" else ("neg", inner)
        if self.at("LPAREN"):
            self.take("LPAREN")
            body = self.exp_tree()
            self.take("RPAREN")
            return body
        k, v = self.peek()
        if k == "NUMBER":
            self.take("NUMBER")
            return num(Fraction(Decimal(v)))
        if k == "SYMBOL":
            self.take("SYMBOL")
            return self.symbol(v)
        raise ParseError("bad exponent %r in: %s" % (v, self.source))


def fold(op, a, b):
    """Value arithmetic in exponent position, folded when both sides are known.
    `**` and `++` never fold - v7 keeps those as form."""
    x, y = numeric(a), numeric(b)
    if x is not None and y is not None and not (op == "/" and y == 0):
        return num({"+": x + y, "-": x - y, "*": x * y, "/": y and x / y}[op])
    return ("exp", op, a, b)


def parse(source, pattern=False):
    return Parser(tokenize(source), source, pattern).parse()
