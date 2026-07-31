"""Tokens -> terms.

Recursive descent.  Precedence, loosest to tightest:

    ⊆ / ¬⊆
    + -                      (addition: AC)
    / //                     (division, left-assoc)
    **                       (fusion: RIGHT-assoc - v7 "binary and right-headed")
    juxtaposition            (the hierarchy constructor)
    postfix ^ [ ] ᛠ _        (powers, filters, adjectives, instance indices)
    atoms ( ) (> <)

Exponents get their own sub-grammar, because inside `^(...)` the operators mean
different things: `**` and `++` build structure and never fold, while `+ - * /`
are value arithmetic and fold eagerly.  v7 is explicit that `웃^(2+1) == 웃^3`
but `웃^(2 ** 3) != 웃^6`.
"""

from __future__ import annotations

from decimal import Decimal
from fractions import Fraction
from typing import List, Optional

from .lexer import Token, tokenize
from .terms import (
    Adj, Angled, Atom, Coeff, Div, Empty, ExpOp, Filter, Fusion, Group,
    Neg, Num, Pow, Subset, Term, TypeOf, Var, add, seq,
)

# Uppercase single letters are term metavariables; a few lowercase ones are
# numeric/scalar metavariables.  Everything else (emoji, multi-letter words) is
# a ground atom.
TERM_VARS = set("SABCDEFGHTXYZPQRUVWNM")
NUM_VARS = {"a", "b", "n", "m", "k", "r", "g", "h", "i", "j", "p", "q"}
SCALAR_VARS = {"c", "d"}


class ParseError(Exception):
    def __init__(self, message: str, token: Optional[Token], source: str):
        self.message = message
        self.token = token
        self.source = source
        where = "at end of input" if token is None else "at %r (grapheme %d)" % (
            token.value, token.index)
        super().__init__("%s %s in: %s" % (message, where, source))


def _to_fraction(text: str) -> Fraction:
    """Exact conversion, scientific notation included.  Never float."""
    return Fraction(Decimal(text))


class Parser:
    def __init__(self, tokens: List[Token], source: str, pattern: bool = False):
        self.toks = tokens
        self.i = 0
        self.source = source
        # In `pattern` mode single letters become Vars.  Assertions parse with
        # pattern=False, so `S` there is an opaque constant - which is the sound
        # reading of a universally quantified equation tested on a generic
        # instance.
        self.pattern = pattern

    # -- token helpers ------------------------------------------------------
    def peek(self, ahead: int = 0) -> Optional[Token]:
        j = self.i + ahead
        return self.toks[j] if j < len(self.toks) else None

    def at(self, *kinds: str) -> bool:
        t = self.peek()
        return t is not None and t.kind in kinds

    def take(self, *kinds: str) -> Token:
        t = self.peek()
        if t is None or t.kind not in kinds:
            raise ParseError("expected %s" % "/".join(kinds), t, self.source)
        self.i += 1
        return t

    def accept(self, *kinds: str) -> Optional[Token]:
        if self.at(*kinds):
            t = self.toks[self.i]
            self.i += 1
            return t
        return None

    # -- entry point --------------------------------------------------------
    def parse(self) -> Term:
        t = self.expr()
        if self.peek() is not None:
            raise ParseError("trailing input", self.peek(), self.source)
        return t

    # -- grammar ------------------------------------------------------------
    def expr(self) -> Term:
        left = self.sum_()
        tok = self.accept("SUBSET", "NSUBSET")
        if tok:
            return Subset(left, self.sum_(), negated=(tok.kind == "NSUBSET"))
        return left

    def sum_(self) -> Term:
        parts = [self.division()]
        while True:
            tok = self.accept("PLUS", "MINUS")
            if not tok:
                break
            rhs = self.division()
            parts.append(Neg(rhs) if tok.kind == "MINUS" else rhs)
        return add(parts) if len(parts) > 1 else parts[0]

    def division(self) -> Term:
        left = self.fusion()
        while self.at("SLASH", "DSLASH"):
            self.take("SLASH", "DSLASH")
            left = Div(left, self.fusion())
        return left

    def fusion(self) -> Term:
        left = self.juxta()
        if self.accept("STARSTAR"):
            return Fusion(left, self.fusion())   # right-assoc, by v7's rule
        return left

    def juxta(self) -> Term:
        items = [self.postfix()]
        while self.starts_operand():
            items.append(self.postfix())
        if len(items) == 1:
            return items[0]
        # A leading scalar becomes a coefficient rather than a sequence member:
        # `3 웃` is 3-of-웃, not a juxtaposition of the number 3 with 웃.
        head = items[0]
        if isinstance(head, Num) or (isinstance(head, Var) and head.kind == "scalar"):
            return Coeff(head, seq(items[1:]))
        return seq(items)

    def starts_operand(self) -> bool:
        return self.at("SYMBOL", "NUMBER", "LPAREN", "LANGLE", "LBRACE")

    def postfix(self) -> Term:
        t = self.primary()
        while True:
            if self.at("CARET"):
                self.take("CARET")
                if self.starts_exponent():
                    t = Pow(t, self.exponent())
                else:
                    t = TypeOf(t)          # bare caret: `웃^` is the type of 웃
            elif self.at("LBRACK"):
                self.take("LBRACK")
                spec = self.expr()
                self.take("RBRACK")
                t = Filter(t, spec)
            elif self.at("ADJ"):
                self.take("ADJ")
                t = Adj(t)
            elif self.at("USCORE"):
                self.take("USCORE")
                idx = self.take("SYMBOL", "NUMBER")
                # An instance index makes a distinct ground symbol: 웃_i
                t = Atom("%r_%s" % (t, idx.value)) if not isinstance(t, Atom) \
                    else Atom("%s_%s" % (t.name, idx.value))
            else:
                return t

    def starts_exponent(self) -> bool:
        return self.at("NUMBER", "SYMBOL", "LPAREN", "MINUS")

    def primary(self) -> Term:
        tok = self.peek()
        if tok is None:
            raise ParseError("unexpected end of expression", None, self.source)

        if tok.kind == "LPAREN":
            self.take("LPAREN")
            if self.at("RPAREN"):                    # `T^()` - empty construction
                self.take("RPAREN")
                return Group(Empty())
            body = self.expr()
            self.take("RPAREN")
            return Group(body)

        if tok.kind == "LANGLE":
            self.take("LANGLE")
            body = self.expr()
            self.take("RANGLE")
            return Angled(body)

        if tok.kind == "LBRACE":
            self.take("LBRACE")
            if self.at("RBRACE"):
                self.take("RBRACE")
                return Empty()
            body = self.expr()
            self.take("RBRACE")
            return Group(body)

        if tok.kind == "NUMBER":
            self.take("NUMBER")
            return Num(_to_fraction(tok.value))

        if tok.kind == "MINUS":
            self.take("MINUS")
            return Neg(self.postfix())

        if tok.kind == "SYMBOL":
            self.take("SYMBOL")
            return self.symbol(tok.value)

        raise ParseError("unexpected token", tok, self.source)

    def symbol(self, name: str) -> Term:
        if self.pattern and len(name) == 1:
            if name in SCALAR_VARS:
                return Var(name, "scalar")
            if name in NUM_VARS:
                return Var(name, "num")
            if name in TERM_VARS:
                return Var(name, "term")
        return Atom(name)

    # -- exponent sub-grammar ----------------------------------------------
    def exponent(self) -> Term:
        """A bare exponent is a single atom; structured ones need parens.

        Without this restriction `S^2 ** S^3` would parse as `S^(2 ** S)^3`,
        because the exponent grammar would happily eat the term-level `**`.
        Same for `/` and `+`: `a 🫀^0 + b 🎭^0` would become `a 🫀^(0 + b) 🎭^0`.
        v7 parenthesizes every structured exponent it writes, so requiring the
        parens costs nothing and removes the ambiguity outright.
        """
        if self.at("LPAREN"):
            self.take("LPAREN")
            body = self.exp_tree()
            self.take("RPAREN")
            return body
        return self.exp_atom()

    def exp_tree(self) -> Term:
        left = self.exp_sum()
        while self.at("PLUSPLUS", "MINUSMINUS"):
            op = self.take("PLUSPLUS", "MINUSMINUS").value
            right = self.exp_sum()
            # `--` is sugar: `g -- h := g ++ (-h)` (v7).  Desugared here so the
            # rule set only ever has to talk about `++`.
            left = ExpOp("++", left, Neg(right) if op == "--" else right)
        return left

    def exp_sum(self) -> Term:
        left = self.exp_fuse()
        while self.at("PLUS", "MINUS"):
            op = self.take("PLUS", "MINUS").value
            right = self.exp_fuse()
            left = self.fold(left, right, op)
        return left

    def exp_fuse(self) -> Term:
        left = self.exp_mul()
        if self.accept("STARSTAR"):
            return ExpOp("**", left, self.exp_fuse())   # never folds
        return left

    def exp_mul(self) -> Term:
        left = self.exp_atom()
        while self.at("STAR", "SLASH"):
            op = self.take("STAR", "SLASH").value
            left = self.fold(left, self.exp_atom(), op)
        return left

    def exp_atom(self) -> Term:
        if self.accept("MINUS"):
            inner = self.exp_atom()
            return Num(-inner.value) if isinstance(inner, Num) else Neg(inner)
        if self.at("LPAREN"):
            self.take("LPAREN")
            body = self.exp_tree()
            self.take("RPAREN")
            return body
        tok = self.peek()
        if tok is not None and tok.kind == "NUMBER":
            self.take("NUMBER")
            return Num(_to_fraction(tok.value))
        if tok is not None and tok.kind == "SYMBOL":
            self.take("SYMBOL")
            return self.symbol(tok.value)
        raise ParseError("bad exponent", tok, self.source)

    @staticmethod
    def fold(left: Term, right: Term, op: str) -> Term:
        """Value arithmetic in exponent position, folded eagerly when possible."""
        if isinstance(left, Num) and isinstance(right, Num):
            a, b = left.value, right.value
            if op == "+":
                return Num(a + b)
            if op == "-":
                return Num(a - b)
            if op == "*":
                return Num(a * b)
            if op == "/" and b != 0:
                return Num(a / b)
        return ExpOp(op, left, right)


def parse(source: str, pattern: bool = False) -> Term:
    """Parse one Pictoji expression."""
    return Parser(tokenize(source), source, pattern=pattern).parse()
