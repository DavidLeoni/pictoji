"""Pattern matching and side conditions.

`match()` is whole-term only: a pattern matches a subject or it does not.
Sub-sequence ("this adjacent pair anywhere inside a longer run") matching is the
rewriter's job in `engine.py`, because only the rewriter knows how to splice a
result back into the surrounding sequence.

Matching is non-deterministic in general (`Add` is AC, so a pattern can match a
sum several ways) and therefore yields *all* matches.  The normalizer takes the
first; the prover takes them all.
"""

from __future__ import annotations

import ast
import operator
from fractions import Fraction
from typing import Dict, Iterator, Optional

from .terms import (
    Add, Atom, Num, Seq, Term, Var, grade, is_typed_one, is_typed_zero,
)

Binding = Dict[str, Term]


# --------------------------------------------------------------------------
# matching
# --------------------------------------------------------------------------

def _var_admits(v: Var, subject: Term) -> bool:
    """Kind restrictions.  A 'num' var only binds numeric-ish things."""
    if v.kind == "num":
        return isinstance(subject, (Num, Atom, Var)) or _is_neg_num(subject)
    if v.kind == "scalar":
        return isinstance(subject, (Num, Atom, Var))
    return True


def _is_neg_num(t: Term) -> bool:
    from .terms import Neg
    return isinstance(t, Neg) and isinstance(t.body, Num)


def match(pattern: Term, subject: Term, env: Optional[Binding] = None) -> Iterator[Binding]:
    """Yield every binding under which `pattern` matches `subject` wholly."""
    env = {} if env is None else env

    if isinstance(pattern, Var):
        if not _var_admits(pattern, subject):
            return
        bound = env.get(pattern.name)
        if bound is None:
            new = dict(env)
            new[pattern.name] = subject
            yield new
        elif bound == subject:          # non-linear pattern: S^n / S^n
            yield env
        return

    if type(pattern) is not type(subject):
        return

    # Leaves compare by value.
    if isinstance(pattern, (Atom, Num)):
        if pattern == subject:
            yield env
        return

    if isinstance(pattern, Add):
        yield from _match_ac(pattern.terms, list(subject.terms), env)
        return

    if isinstance(pattern, Seq):
        if len(pattern.items) != len(subject.items):
            return
        yield from _match_all(pattern.items, subject.items, env)
        return

    pk, sk = pattern.children(), subject.children()
    if len(pk) != len(sk):
        return
    # Non-child fields (ExpOp.op, Subset.negated) must agree too.
    if pattern.rebuild(sk) != subject:
        return
    yield from _match_all(pk, sk, env)


def _match_all(pats, subs, env: Binding) -> Iterator[Binding]:
    """Match a fixed-arity sequence of patterns, threading the binding."""
    if not pats:
        yield env
        return
    for e in match(pats[0], subs[0], env):
        yield from _match_all(pats[1:], subs[1:], e)


def _match_ac(pats, subs, env: Binding) -> Iterator[Binding]:
    """AC matching for `Add`: try each pattern against each unused operand.

    Exponential in the worst case, but sums in this algebra have a handful of
    terms, and `Add` is stored sorted so the search order is stable.
    """
    if not pats:
        if not subs:
            yield env
        return
    if len(pats) > len(subs):
        return
    for i, s in enumerate(subs):
        rest = subs[:i] + subs[i + 1 :]
        for e in match(pats[0], s, env):
            yield from _match_ac(pats[1:], rest, e)


def subst(pattern: Term, env: Binding) -> Term:
    """Instantiate a right-hand side against a binding."""
    if isinstance(pattern, Var):
        if pattern.name not in env:
            raise KeyError("unbound metavariable %r in rule RHS" % pattern.name)
        return env[pattern.name]
    kids = pattern.children()
    if not kids:
        return pattern
    return pattern.rebuild([subst(k, env) for k in kids])


# --------------------------------------------------------------------------
# side conditions
# --------------------------------------------------------------------------

class ConditionError(Exception):
    pass


_BINOPS = {
    ast.Eq: operator.eq, ast.NotEq: operator.ne,
    ast.Lt: operator.lt, ast.LtE: operator.le,
    ast.Gt: operator.gt, ast.GtE: operator.ge,
}
_ARITH = {
    ast.Add: operator.add, ast.Sub: operator.sub,
    ast.Mult: operator.mul, ast.Div: operator.truediv,
}


def _numeric(t: Term) -> Optional[Fraction]:
    from .terms import Neg
    if isinstance(t, Num):
        return t.value
    if isinstance(t, Neg) and isinstance(t.body, Num):
        return -t.body.value
    return None


def _sgn(x) -> int:
    return (x > 0) - (x < 0)


_FUNCS = {
    "abs": abs,
    "sgn": _sgn,
    "grade": lambda t: grade(t) if isinstance(t, Term) else t,
    "int": lambda x: isinstance(x, Fraction) and x.denominator == 1,
    "is_int": lambda x: isinstance(x, Fraction) and x.denominator == 1,
    "typed_one": is_typed_one,
    "typed_zero": is_typed_zero,
    "same_base": lambda a, b: _base(a) == _base(b),
}


def _base(t: Term):
    from .terms import base_symbol
    return base_symbol(t)


def normalize_condition(text: str) -> str:
    """Rewrite the spec's notation into something Python's parser accepts."""
    out = text.replace("¬=", "!=").replace("¬==", "!=").replace("≠", "!=")
    out = out.replace("≤", "<=").replace("≥", ">=")
    # `|a| < 1` -> `abs(a) < 1`; the bars always come in pairs around one var.
    while "|" in out:
        first = out.index("|")
        second = out.index("|", first + 1)
        out = out[:first] + "abs(" + out[first + 1 : second] + ")" + out[second + 1 :]
    return out


class _Eval(ast.NodeVisitor):
    def __init__(self, env: Binding):
        self.env = env

    def visit_Expression(self, node): return self.visit(node.body)

    def visit_BoolOp(self, node):
        vals = [self.visit(v) for v in node.values]
        return all(vals) if isinstance(node.op, ast.And) else any(vals)

    def visit_UnaryOp(self, node):
        v = self.visit(node.operand)
        if isinstance(node.op, ast.USub):
            return -v
        if isinstance(node.op, ast.Not):
            return not v
        raise ConditionError("unsupported unary operator")

    def visit_BinOp(self, node):
        fn = _ARITH.get(type(node.op))
        if fn is None:
            raise ConditionError("unsupported arithmetic operator")
        return fn(self.visit(node.left), self.visit(node.right))

    def visit_Compare(self, node):
        left = self.visit(node.left)
        for op, comp in zip(node.ops, node.comparators):
            fn = _BINOPS.get(type(op))
            if fn is None:
                raise ConditionError("unsupported comparison")
            right = self.visit(comp)
            if left is None or right is None:
                raise ConditionError("condition needs a value that is not statically known")
            if not fn(left, right):
                return False
            left = right
        return True

    def visit_Call(self, node):
        if not isinstance(node.func, ast.Name) or node.func.id not in _FUNCS:
            raise ConditionError("unknown function in side condition")
        return _FUNCS[node.func.id](*[self.visit(a) for a in node.args])

    def visit_Name(self, node):
        if node.id not in self.env:
            raise ConditionError("side condition mentions unbound %r" % node.id)
        term = self.env[node.id]
        num = _numeric(term)
        return num if num is not None else term

    def visit_Constant(self, node):
        return Fraction(node.value) if isinstance(node.value, (int, float)) else node.value

    def generic_visit(self, node):
        raise ConditionError("unsupported syntax in side condition: %s" % type(node).__name__)


def check_condition(text: Optional[str], env: Binding) -> bool:
    """Evaluate a rule's side condition.

    Returns False (rule does not fire) when the condition mentions something not
    statically known - the conservative choice.  A malformed condition raises,
    because that is a bug in the spec file and must not be swallowed.
    """
    if not text:
        return True
    try:
        tree = ast.parse(normalize_condition(text), mode="eval")
    except SyntaxError as exc:
        raise ConditionError("cannot parse side condition %r: %s" % (text, exc))
    try:
        return bool(_Eval(env).visit(tree))
    except ConditionError:
        return False
