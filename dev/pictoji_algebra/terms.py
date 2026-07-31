"""The term algebra.

Design commitment: **form is substance**.  `Seq` and `Group` are different node
types, so `S S != (S S)` is true by construction and needs no axiom.  Likewise
`Seq` never flattens, so `(A B) C`, `A (B C)` and `A B C` are three distinct
terms - v7's "three distinct graphs".

The single deliberate exception is `Add`, which canonicalizes its operands into
sorted order.  v7 states outright that `+` is associative *and* commutative, so
ordering is not substance there; canonicalizing removes a whole class of
AC-matching search from the prover.  We deviate from "keep the form" exactly
where the spec says the form does not carry meaning, and nowhere else.

Terms are immutable and hash-cached: they are nodes in a search graph and get
hashed constantly during saturation.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from fractions import Fraction
from typing import Optional, Sequence, Tuple


class Term:
    """Base class.  Subclasses are frozen dataclasses with `eq=False`.

    We define `__eq__`/`__hash__` by hand so the hash can be cached; the
    dataclass-generated versions rehash the whole subtree on every call, which
    shows up badly once the prover is holding thousands of frontier nodes.
    """

    __slots__ = ()

    def _key(self) -> tuple:
        raise NotImplementedError

    def __hash__(self) -> int:
        return self._hash  # type: ignore[attr-defined]

    def __eq__(self, other) -> bool:
        if self is other:
            return True
        if type(self) is not type(other):
            return False
        return self._hash == other._hash and self._key() == other._key()

    # -- generic traversal, used by the rewriter to work at arbitrary paths --
    def children(self) -> Tuple["Term", ...]:
        return ()

    def rebuild(self, kids: Sequence["Term"]) -> "Term":
        return self


def _seal(obj: Term) -> None:
    object.__setattr__(obj, "_hash", hash((type(obj).__name__,) + obj._key()))


# --------------------------------------------------------------------------
# leaves
# --------------------------------------------------------------------------

@dataclass(frozen=True, eq=False, repr=False)
class Atom(Term):
    """An emoji or letter used as a ground symbol: 웃, 🏠, R."""
    name: str

    def __post_init__(self): _seal(self)
    def _key(self): return (self.name,)
    def __repr__(self): return self.name


@dataclass(frozen=True, eq=False, repr=False)
class Var(Term):
    """A pattern metavariable.

    `kind` restricts what it may bind: 'term' (S, A, B, E, X, T),
    'num' (a, b, n, r - exponents/numbers), 'scalar' (c).
    In *assertions* variables are treated as opaque constants, which is sound:
    an equation over a universally quantified variable is tested by its generic
    instance.
    """
    name: str
    kind: str = "term"

    def __post_init__(self): _seal(self)
    def _key(self): return (self.name, self.kind)
    def __repr__(self): return "?" + self.name


@dataclass(frozen=True, eq=False, repr=False)
class Num(Term):
    """A bare numeric value.  Exact: `Fraction`, never float."""
    value: Fraction

    def __post_init__(self):
        object.__setattr__(self, "value", Fraction(self.value))
        _seal(self)

    def _key(self): return (self.value,)

    def __repr__(self):
        v = self.value
        return str(v.numerator) if v.denominator == 1 else "%d/%d" % (v.numerator, v.denominator)


# --------------------------------------------------------------------------
# structure
# --------------------------------------------------------------------------

@dataclass(frozen=True, eq=False, repr=False)
class Seq(Term):
    """Juxtaposition `A B C`: n-ary, ordered, NON-associative.

    Never flattens.  A one-element Seq collapses to its element (there is no
    such thing as a sequence of one); everything else is preserved exactly.
    """
    items: Tuple[Term, ...]

    def __post_init__(self):
        object.__setattr__(self, "items", tuple(self.items))
        _seal(self)

    def _key(self): return (self.items,)
    def children(self): return self.items
    def rebuild(self, kids): return seq(kids)
    def __repr__(self): return " ".join(map(repr, self.items))


@dataclass(frozen=True, eq=False, repr=False)
class Group(Term):
    """Round parens: reify + FENCE.  Structurally distinct from Seq."""
    body: Term

    def __post_init__(self): _seal(self)
    def _key(self): return (self.body,)
    def children(self): return (self.body,)
    def rebuild(self, kids): return Group(kids[0])
    def __repr__(self): return "(%r)" % (self.body,)


@dataclass(frozen=True, eq=False, repr=False)
class Angled(Term):
    """`(> ... <)`: forced linear/value computation island."""
    body: Term

    def __post_init__(self): _seal(self)
    def _key(self): return (self.body,)
    def children(self): return (self.body,)
    def rebuild(self, kids): return Angled(kids[0])
    def __repr__(self): return "(> %r <)" % (self.body,)


@dataclass(frozen=True, eq=False, repr=False)
class Add(Term):
    """`A + B`: associative AND commutative, so operands are stored sorted."""
    terms: Tuple[Term, ...]

    def __post_init__(self):
        object.__setattr__(self, "terms", tuple(self.terms))
        _seal(self)

    def _key(self): return (self.terms,)
    def children(self): return self.terms
    def rebuild(self, kids): return add(kids)
    def __repr__(self): return " + ".join(map(repr, self.terms))


@dataclass(frozen=True, eq=False, repr=False)
class Coeff(Term):
    """Scalar coefficient `c X`.

    `scalar` is a Term - `Num` for the eager numeric case (`3 웃`, and `0 웃`
    which is the typed zero of X), or `Var` for the symbolic case v7's Frames
    section uses (`a 🫀^0 + b 🎭^0`).
    """
    scalar: Term
    body: Term

    def __post_init__(self):
        if isinstance(self.scalar, (int, Fraction)):
            object.__setattr__(self, "scalar", Num(Fraction(self.scalar)))
        _seal(self)

    def _key(self): return (self.scalar, self.body)
    def children(self): return (self.scalar, self.body)
    def rebuild(self, kids): return Coeff(kids[0], kids[1])
    def __repr__(self): return "%r %r" % (self.scalar, self.body)

    @property
    def numeric(self) -> Optional[Fraction]:
        """The coefficient as a number, or None when it is symbolic."""
        return self.scalar.value if isinstance(self.scalar, Num) else None


@dataclass(frozen=True, eq=False, repr=False)
class Pow(Term):
    """`S^e`.  `Pow(X, Num(0))` is the typed one of X."""
    base: Term
    exp: Term

    def __post_init__(self): _seal(self)
    def _key(self): return (self.base, self.exp)
    def children(self): return (self.base, self.exp)
    def rebuild(self, kids): return Pow(kids[0], kids[1])

    def __repr__(self):
        e = repr(self.exp)
        if not isinstance(self.exp, (Num, Var, Atom)):
            e = "(%s)" % e
        return "%r^%s" % (self.base, e)


@dataclass(frozen=True, eq=False, repr=False)
class ExpOp(Term):
    """A structured exponent: `2 ++ 1`, `2 ** 3`.

    Non-commutative and never folded to a value - v7 is explicit that
    `(웃^2)^3 == 웃^(2 ** 3)` but `!= 웃^6`, and `웃^(2 ++ 1) != 웃^(1 ++ 2)`.
    """
    op: str                        # '++' | '**' | '--'
    left: Term
    right: Term

    def __post_init__(self): _seal(self)
    def _key(self): return (self.op, self.left, self.right)
    def children(self): return (self.left, self.right)
    def rebuild(self, kids): return ExpOp(self.op, kids[0], kids[1])

    def __repr__(self):
        # Nested trees MUST show their parens: `(2 ++ 1) ** 2` and
        # `2 ++ (1 ** 2)` are different exponents, and a trace that printed both
        # as `2 ++ 1 ** 2` would be actively misleading.
        def side(t):
            return "(%r)" % (t,) if isinstance(t, ExpOp) else repr(t)
        return "%s %s %s" % (side(self.left), self.op, side(self.right))


@dataclass(frozen=True, eq=False, repr=False)
class Fusion(Term):
    """`A ** B` at term level: binary, right-headed."""
    left: Term
    right: Term

    def __post_init__(self): _seal(self)
    def _key(self): return (self.left, self.right)
    def children(self): return (self.left, self.right)
    def rebuild(self, kids): return Fusion(kids[0], kids[1])
    def __repr__(self): return "%r ** %r" % (self.left, self.right)


@dataclass(frozen=True, eq=False, repr=False)
class Div(Term):
    """`A / B`.  Dispatches on the grade of the divisor (v7 Division)."""
    num: Term
    den: Term

    def __post_init__(self): _seal(self)
    def _key(self): return (self.num, self.den)
    def children(self): return (self.num, self.den)
    def rebuild(self, kids): return Div(kids[0], kids[1])
    def __repr__(self): return "%r / %r" % (self.num, self.den)


@dataclass(frozen=True, eq=False, repr=False)
class Neg(Term):
    """Unary minus / the subtractive half of the dignity family."""
    body: Term

    def __post_init__(self): _seal(self)
    def _key(self): return (self.body,)
    def children(self): return (self.body,)
    def rebuild(self, kids): return Neg(kids[0])
    def __repr__(self): return "-%r" % (self.body,)


@dataclass(frozen=True, eq=False, repr=False)
class Adj(Term):
    """Adjective marker `Xᛠ`."""
    body: Term

    def __post_init__(self): _seal(self)
    def _key(self): return (self.body,)
    def children(self): return (self.body,)
    def rebuild(self, kids): return Adj(kids[0])
    def __repr__(self): return "%rᛠ" % (self.body,)


@dataclass(frozen=True, eq=False, repr=False)
class Filter(Term):
    """`D[spec]` - filter/qualification."""
    body: Term
    spec: Term

    def __post_init__(self): _seal(self)
    def _key(self): return (self.body, self.spec)
    def children(self): return (self.body, self.spec)
    def rebuild(self, kids): return Filter(kids[0], kids[1])
    def __repr__(self): return "%r[%r]" % (self.body, self.spec)


@dataclass(frozen=True, eq=False, repr=False)
class TypeOf(Term):
    """Bare postfix caret: `웃^`, the type/class of 웃."""
    body: Term

    def __post_init__(self): _seal(self)
    def _key(self): return (self.body,)
    def children(self): return (self.body,)
    def rebuild(self, kids): return TypeOf(kids[0])
    def __repr__(self): return "%r^" % (self.body,)


@dataclass(frozen=True, eq=False, repr=False)
class Subset(Term):
    left: Term
    right: Term
    negated: bool = False

    def __post_init__(self): _seal(self)
    def _key(self): return (self.left, self.right, self.negated)
    def children(self): return (self.left, self.right)
    def rebuild(self, kids): return Subset(kids[0], kids[1], self.negated)
    def __repr__(self): return "%r %s %r" % (self.left, "¬⊆" if self.negated else "⊆", self.right)


@dataclass(frozen=True, eq=False, repr=False)
class Empty(Term):
    """`{}` - the empty result set."""

    def __post_init__(self): _seal(self)
    def _key(self): return ()
    def __repr__(self): return "{}"


# --------------------------------------------------------------------------
# smart constructors
# --------------------------------------------------------------------------

def seq(items: Sequence[Term]) -> Term:
    """Build a sequence.  A single item is that item; nothing else collapses."""
    items = tuple(items)
    if len(items) == 1:
        return items[0]
    return Seq(items)


def add(terms: Sequence[Term]) -> Term:
    """Build a sum, flattened and canonically sorted (see module docstring)."""
    flat = []
    for t in terms:
        if isinstance(t, Add):
            flat.extend(t.terms)
        else:
            flat.append(t)
    if len(flat) == 1:
        return flat[0]
    return Add(tuple(sorted(flat, key=sort_key)))


# --------------------------------------------------------------------------
# helpers used by rules, side conditions and the prover's budgets
# --------------------------------------------------------------------------

def sort_key(t: Term) -> tuple:
    """A total order on terms, for `Add` canonicalization and tint sorting."""
    return (type(t).__name__, repr(t))


def size(t: Term) -> int:
    """Node count - the prover's size budget."""
    return 1 + sum(size(c) for c in t.children())


def depth(t: Term) -> int:
    kids = t.children()
    return 1 + (max(depth(c) for c in kids) if kids else 0)


def grade(t: Term) -> Optional[Fraction]:
    """Structural level, or None when it is not statically known.

    v7 uses this for division's dispatch (`grade(D) != 0` picks fusion,
    grade 0 picks removal) and for the typed-one/typed-zero distinction.
    """
    if isinstance(t, Atom):
        return Fraction(1)
    if isinstance(t, Num):
        return Fraction(0)
    if isinstance(t, Pow):
        return t.exp.value if isinstance(t.exp, Num) else None
    if isinstance(t, (Group, Angled, Coeff)):
        return grade(t.body)
    if isinstance(t, Seq):
        parts = [grade(x) for x in t.items]
        return None if any(p is None for p in parts) else sum(parts)
    if isinstance(t, Adj):
        return Fraction(0)
    return None


def is_typed_one(t: Term) -> bool:
    """`X^0` - the multiplicative identity of type X."""
    return isinstance(t, Pow) and isinstance(t.exp, Num) and t.exp.value == 0


def is_typed_zero(t: Term) -> bool:
    """`0 X` - the additive identity of type X."""
    return isinstance(t, Coeff) and t.numeric == 0


def base_symbol(t: Term) -> Optional[Term]:
    """The base a power is taken over, for same-symbol tests.

    Per Amendment A's settled definition, kept because v7 needs the same notion:
    the base of `S^n` is the atom `S`; the base of `(E)^n` is the fenced group.
    """
    if isinstance(t, Pow):
        return t.base
    if isinstance(t, (Atom, Group)):
        return t
    if isinstance(t, Coeff):
        return base_symbol(t.body)
    return None


def walk(t: Term, path: Tuple[int, ...] = ()):
    """Yield `(path, subterm)` for every position, outermost first."""
    yield path, t
    for i, c in enumerate(t.children()):
        for p, s in walk(c, path + (i,)):
            yield p, s


def at(t: Term, path: Tuple[int, ...]) -> Term:
    for i in path:
        t = t.children()[i]
    return t


def replace(t: Term, path: Tuple[int, ...], new: Term) -> Term:
    """Functional update of the subterm at `path`."""
    if not path:
        return new
    kids = list(t.children())
    kids[path[0]] = replace(kids[path[0]], path[1:], new)
    return t.rebuild(kids)
