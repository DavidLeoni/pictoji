"""Computational rewrite steps that cannot be written as markdown patterns.

Kept deliberately small.  Every axiom that *can* be a pattern rule lives in the
spec markdown, because bisection works over the markdown rule set - moving
behaviour into Python hides it from the bisector.  What is left here is
genuinely n-ary or arithmetic:

    contract_run   (웃 웃 웃) -> 웃^3        arity is unbounded
    collect_sum    웃 + 웃 + 웃 -> 3웃        field arithmetic over a sum
    float_tints    웃 🫀^0 -> 🫀^0 웃         a canonical ordering, not a rewrite
    scan_absorb    🌳 웃^0 웃 -> 🌳 웃        scans past foreign symbols
    angled_eval    (> 웃^2 웃^3 <) -> 웃^5   contiguous-run summing

Each is still *declared* in the markdown (`[builtin=name]`) so it carries an id
and tags and can be disabled and bisected like any other rule.

Every function takes a term and returns a rewritten term, or None if it does
not apply.
"""

from __future__ import annotations

from fractions import Fraction
from typing import List, Optional

from .terms import (
    Add, Angled, Atom, Coeff, Group, Num, Pow, Seq, Term, add,
    base_symbol, is_typed_one, seq, sort_key,
)


def _coeff_parts(t: Term):
    """Split `3 웃` into (3, 웃); a bare term is (1, term)."""
    if isinstance(t, Coeff) and t.numeric is not None:
        return t.numeric, t.body
    return Fraction(1), t


def _with_coeff(c: Fraction, body: Term) -> Term:
    return body if c == 1 else Coeff(Num(c), body)


def _exponent_of(t: Term):
    """(base, exponent) for a power-form term, else None."""
    if isinstance(t, Pow) and isinstance(t.exp, Num):
        return t.base, t.exp.value
    if isinstance(t, (Atom, Group)):
        return t, Fraction(1)
    return None


# --------------------------------------------------------------------------

def contract_run(t: Term) -> Optional[Term]:
    """`(웃 웃 웃) -> 웃^3`.

    Only a *fenced* uniform run contracts.  A bare run does not: v7 is explicit
    that `웃 웃 웃 != 웃^3`, which is the whole point of the notation.
    A singleton group `(웃)` also does not contract - it is a held form.
    """
    if not isinstance(t, Group) or not isinstance(t.body, Seq):
        return None
    items = t.body.items
    if len(items) < 2 or any(x != items[0] for x in items):
        return None
    return Pow(items[0], Num(Fraction(len(items))))


def collect_sum(t: Term) -> Optional[Term]:
    """`웃 + 웃 + 웃 -> 3웃`, and drop unfenced zero terms.

    Fenced operands are skipped entirely.  That is the fence principle, and it
    is what makes v7's `(웃) + (웃)` hold and `웃 + (0웃)` survive while the
    unfenced `웃 + 0웃` drops.
    """
    if not isinstance(t, Add):
        return None

    fenced: List[Term] = []
    totals = {}
    order: List[Term] = []

    for term in t.terms:
        coeff, body = _coeff_parts(term)
        if isinstance(body, Group) or isinstance(term, Group):
            fenced.append(term)          # a fence opts out of collection
            continue
        if body not in totals:
            totals[body] = Fraction(0)
            order.append(body)
        totals[body] += coeff

    collected = [_with_coeff(totals[b], b) for b in order if totals[b] != 0]
    result = collected + fenced
    if not result:
        return Num(Fraction(0))
    new = add(result) if len(result) > 1 else result[0]
    return new if new != t else None


def float_tints(t: Term) -> Optional[Term]:
    """Typed ones float left into a sorted coefficient prefix.

    Implemented as a canonical *ordering* rather than a swap rule.  A swap rule
    (`X Y^0 -> Y^0 X`) is permutative and would let the normalizer cycle
    forever; extract-sort-prepend is idempotent, so it cannot.
    """
    if not isinstance(t, Seq):
        return None
    tints = [x for x in t.items if is_typed_one(x)]
    rest = [x for x in t.items if not is_typed_one(x)]
    if not tints or not rest:
        return None
    ordered = sorted(tints, key=sort_key) + rest
    new = seq(ordered)
    return new if new != t else None


def scan_absorb(t: Term) -> Optional[Term]:
    """`🌳 웃^0 웃 -> 🌳 웃`  (v7 scan-absorb).

    A prefix `X^0` absorbs into the FIRST X-typed element to its right, passing
    over foreign symbols.  v7 imports this so that floating and absorbing
    commute - without it the two rules race and the normal form depends on
    rule order.
    """
    if not isinstance(t, Seq):
        return None
    items = list(t.items)
    for i, tint in enumerate(items):
        if not is_typed_one(tint):
            continue
        for j in range(i + 1, len(items)):
            if is_typed_one(items[j]):
                continue
            if base_symbol(items[j]) == tint.base:
                return seq(items[:i] + items[i + 1 :])
    return None


def angled_eval(t: Term) -> Optional[Term]:
    """`(> ... <)` - value semantics: contiguous same-symbol runs sum.

    Order across symbols is still respected, so `(> 웃 🏠^2 웃^6 🏠^3 <)` holds
    as written: the 웃 terms are not contiguous and do not combine.
    """
    if not isinstance(t, Angled):
        return None

    body = t.body
    if not isinstance(body, Seq):
        # A single balanced group contracts; anything else is already a value.
        inner = contract_run(body) if isinstance(body, Group) else body
        return inner

    items = [contract_run(x) or x for x in body.items]

    merged: List[Term] = []
    for item in items:
        parts = _exponent_of(item)
        if parts and merged:
            prev = _exponent_of(merged[-1])
            if prev and prev[0] == parts[0]:
                merged[-1] = Pow(parts[0], Num(prev[1] + parts[1]))
                continue
        merged.append(item)

    # Exponent 1 collapses HERE and only here.  Inside `(> <)` we are in value
    # semantics, where `웃^1` is just 웃 - that is what makes v7's
    # `(> 웃^(1/2) 웃^(1/2) <) -> 웃` land on the bare symbol.  As a *global*
    # rule `S^1 -> S` would instead fire inside `웃^1 ** 웃^-1` before the
    # fusion ladder could see it, destroying the shape annihilation matches on;
    # and as a global equality it is a search bomb, since its left side matches
    # every term.
    merged = [x.base if (isinstance(x, Pow) and isinstance(x.exp, Num)
                         and x.exp.value == 1) else x for x in merged]

    # The angled parens DISSOLVE once evaluated: `(> <)` is a computation
    # island that yields a value, not a fence.  Every v7 example writes the
    # result without them, including the non-contiguous case that "holds"
    # (`(> 웃 🏠^2 웃^6 🏠^3 <) -> 웃 🏠^2 웃^6 🏠^3`) - there, "held" means the
    # runs did not combine, not that the brackets survive.
    #
    # This fires innermost-first (see `engine.rewrites`), so nested `**` and
    # inner groups are already resolved by the time we get here, which is v7's
    # stated evaluation order.
    return seq(merged)


def factor_prefix(t: Term) -> Optional[Term]:
    """`🌳 웃 🐶 + 🌳 웃 🏠 -> 🌳 웃 (🐶 + 🏠)`.

    Needs to be a builtin rather than a pattern rule because `Seq` is flat and
    n-ary: a pattern `A B + A C` cannot bind `A` to the two-element prefix
    `🌳 웃` without implicitly regrouping it, and an implicit regrouping would
    invent a fence.  Fences are substance, so the matcher refuses to do that and
    the prefix search happens here instead.

    A summand with no tail contributes the continuation identity `1`, which is
    what licenses v7's `🌳 웃 🐶 + 🌳 웃 == 🌳 웃 (🐶 + 1)`.
    """
    if not isinstance(t, Add) or len(t.terms) < 2:
        return None
    runs = []
    for term in t.terms:
        if isinstance(term, Seq):
            runs.append(list(term.items))
        else:
            return None

    shortest = min(len(r) for r in runs)
    common = 0
    while common < shortest - 1 and len({tuple(r[: common + 1]) for r in runs}) == 1:
        common += 1
    if common == 0:
        return None

    prefix = runs[0][:common]
    tails = []
    for r in runs:
        rest = r[common:]
        tails.append(seq(rest) if rest else Num(Fraction(1)))
    return seq(prefix + [Group(add(tails))])


def distribute(t: Term) -> Optional[Term]:
    """The reverse of `factor_prefix`: `A (B + C) -> A B + A C`."""
    if not isinstance(t, Seq):
        return None
    last = t.items[-1]
    if not isinstance(last, Group) or not isinstance(last.body, Add):
        return None
    prefix = list(t.items[:-1])
    if not prefix:
        return None
    out = []
    for summand in last.body.terms:
        if isinstance(summand, Num) and summand.value == 1:
            out.append(seq(prefix))          # the continuation identity
        elif isinstance(summand, Seq):
            out.append(seq(prefix + list(summand.items)))
        else:
            out.append(seq(prefix + [summand]))
    return add(out)


REGISTRY = {
    "contract_run": contract_run,
    "collect_sum": collect_sum,
    "float_tints": float_tints,
    "scan_absorb": scan_absorb,
    "angled_eval": angled_eval,
    "factor_prefix": factor_prefix,
    "distribute": distribute,
}

# Builtins that may also be run in reverse, for the equational prover.
INVERSE = {
    "factor_prefix": "distribute",
    "distribute": "factor_prefix",
}
