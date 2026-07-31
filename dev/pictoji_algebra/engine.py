"""Matching, rewriting, and the bidirectional prover.

Two tiers.  Tier 1 normalizes with oriented `->` rules to a fixpoint.  Tier 2
proves `==` goals by breadth-first search outward from both sides using `==`
rules in both directions, meeting in the middle - necessary because
form-is-substance makes `==` a proof obligation rather than a comparison.

Three outcomes, never two: PROVED, CLOSED (not derivable), and EXHAUSTED (budget
ran out - unknown).  Reporting EXHAUSTED as a disproof would make an
inconsistency hunter lie about the one thing it exists to detect.
"""

from __future__ import annotations

import ast
import operator
from dataclasses import dataclass, field
from fractions import Fraction
from typing import List, Optional, Set, Tuple

from .terms import (
    add, base_symbol, grade, is_seg, is_typed_one, is_typed_zero, is_var, kids,
    num, numeric, rebuild, replace, segvar, seq, show, size, walk,
)

REDUCE, EQUIV = "reduce", "equiv"
PROVED, EXHAUSTED, CLOSED = "PROVED", "EXHAUSTED", "CLOSED"


# --------------------------------------------------------------------------
# matching
# --------------------------------------------------------------------------

def match(p, s, env=None):
    """Yield every binding under which pattern `p` matches subject `s` wholly."""
    env = {} if env is None else env
    if is_var(p):
        if not _admits(p[2], s):
            return
        if p[1] in env:
            if env[p[1]] == s:
                yield env
        else:
            e = dict(env); e[p[1]] = s; yield e
        return
    if not isinstance(p, tuple) or not isinstance(s, tuple):
        if p == s:
            yield env
        return
    if p[0] != s[0] or _lits(p) != _lits(s):
        return
    pk, sk = kids(p), kids(s)
    if p[0] == "+":
        yield from _ac(pk, sk, env)
    elif any(is_seg(x) for x in pk):
        yield from _seg(pk, sk, env)
    elif len(pk) == len(sk):
        yield from _all(pk, sk, env)


def _lits(t):
    return [x for x in t[1:] if not isinstance(x, tuple)]


def _admits(kind, s):
    if kind in ("num", "scalar"):
        return s[0] in ("num", "atom", "?") or numeric(s) is not None
    return True


def _all(ps, ss, env):
    if not ps:
        yield env
        return
    for e in match(ps[0], ss[0], env):
        yield from _all(ps[1:], ss[1:], e)


def _seg(ps, ss, env):
    """Segment variables bind a (possibly empty) run of siblings."""
    if not ps:
        if not ss:
            yield env
        return
    p, rest = ps[0], ps[1:]
    if is_seg(p):
        for take in range(len(ss) + 1):
            bound = tuple(ss[:take])
            if p[1] in env and env[p[1]] != bound:
                continue
            e = dict(env); e[p[1]] = bound
            yield from _seg(rest, ss[take:], e)
    elif ss:
        for e in match(p, ss[0], env):
            yield from _seg(rest, ss[1:], e)


def _ac(ps, ss, env):
    """`+` is associative and commutative, so a pattern can match a sum several
    ways.  Exponential in principle; sums here have a handful of terms."""
    if not ps:
        if not ss:
            yield env
        return
    if len(ps) > len(ss):
        return
    for i, s in enumerate(ss):
        for e in match(ps[0], s, env):
            yield from _ac(ps[1:], ss[:i] + ss[i + 1:], e)


def subst(p, env):
    if is_var(p):
        return env[p[1]]
    if not isinstance(p, tuple):
        return p
    out = [p[0]]
    for x in p[1:]:
        if is_seg(x):
            bound = env[x[1]]
            if p[0] == "seq":
                out.extend(bound)
            elif bound:
                # A segment used as a single operand (`A.. B + A..`) becomes one
                # sequence rather than splicing its members into the parent.
                out.append(seq(bound))
            else:
                raise KeyError("empty segment %r in operand position" % x[1])
        elif isinstance(x, tuple):
            out.append(subst(x, env))
        else:
            out.append(x)
    return seq(out[1:]) if p[0] == "seq" else tuple(out)


def open_seq(lhs, rhs):
    """Let a short `seq` pattern match a run inside a longer one.

    `X^0 X -> X` should fire inside `🌳 X^0 X 🐶` without a rule per context, so
    a seq pattern carrying no explicit segment variables is wrapped in two.
    This is the *only* sequence-matching mechanism: an author who needs the
    context can name it (`A.. X B..`), and everyone else gets it implicitly.
    """
    if lhs[0] != "seq" or any(is_seg(x) for x in kids(lhs)):
        return lhs, rhs
    l, r = segvar("\x00L"), segvar("\x00R")
    body = list(rhs[1:]) if rhs[0] == "seq" else [rhs]
    return ("seq", l) + lhs[1:] + (r,), ("seq", l, *body, r)


# --------------------------------------------------------------------------
# side conditions
# --------------------------------------------------------------------------

_CMP = {ast.Eq: operator.eq, ast.NotEq: operator.ne, ast.Lt: operator.lt,
        ast.LtE: operator.le, ast.Gt: operator.gt, ast.GtE: operator.ge}
_ARITH = {ast.Add: operator.add, ast.Sub: operator.sub,
          ast.Mult: operator.mul, ast.Div: operator.truediv}
_FUNCS = {
    "abs": abs,
    "sgn": lambda x: (x > 0) - (x < 0),
    "grade": lambda t: grade(t) if isinstance(t, tuple) else t,
    "is_int": lambda x: isinstance(x, Fraction) and x.denominator == 1,
    "typed_one": is_typed_one,
    "typed_zero": is_typed_zero,
    "same_base": lambda a, b: base_symbol(a) == base_symbol(b),
}


class Hold(Exception):
    """The condition needs something not statically known: do not fire."""


def prep_condition(text):
    out = (text.replace("¬==", "!=").replace("¬=", "!=").replace("≠", "!=")
               .replace("≤", "<=").replace("≥", ">="))
    while "|" in out:                       # |a| < 1  ->  abs(a) < 1
        a = out.index("|")
        b = out.index("|", a + 1)
        out = out[:a] + "abs(" + out[a + 1:b] + ")" + out[b + 1:]
    return out


def _eval(node, env):
    if isinstance(node, ast.Expression):
        return _eval(node.body, env)
    if isinstance(node, ast.BoolOp):
        vals = [_eval(v, env) for v in node.values]
        return all(vals) if isinstance(node.op, ast.And) else any(vals)
    if isinstance(node, ast.UnaryOp):
        v = _eval(node.operand, env)
        return -v if isinstance(node.op, ast.USub) else not v
    if isinstance(node, ast.BinOp):
        return _ARITH[type(node.op)](_eval(node.left, env), _eval(node.right, env))
    if isinstance(node, ast.Compare):
        left = _eval(node.left, env)
        for op, comp in zip(node.ops, node.comparators):
            right = _eval(comp, env)
            if left is None or right is None:
                raise Hold()
            if not _CMP[type(op)](left, right):
                return False
            left = right
        return True
    if isinstance(node, ast.Call):
        return _FUNCS[node.func.id](*[_eval(a, env) for a in node.args])
    if isinstance(node, ast.Name):
        if node.id not in env:
            raise Hold()
        t = env[node.id]
        n = numeric(t) if isinstance(t, tuple) else None
        return n if n is not None else t
    if isinstance(node, ast.Constant):
        return Fraction(node.value) if isinstance(node.value, (int, float)) else node.value
    raise Hold()


def check_condition(text, env):
    if not text:
        return True
    try:
        return bool(_eval(ast.parse(prep_condition(text), mode="eval"), env))
    except (Hold, KeyError, TypeError):
        return False


# --------------------------------------------------------------------------
# builtins - only what is genuinely n-ary or arithmetic
# --------------------------------------------------------------------------

def contract_run(t):
    """`(웃 웃 웃) -> 웃^3`.  Only a FENCED uniform run contracts; a bare run
    does not, which is the whole point of the notation.  `(웃)` is a held form."""
    if t[0] != "group" or t[1][0] != "seq":
        return None
    items = t[1][1:]
    if len(items) < 2 or any(x != items[0] for x in items):
        return None
    return ("pow", items[0], num(len(items)))


def collect_sum(t):
    """`웃 + 웃 + 웃 -> 3웃`, dropping unfenced zero terms.

    Fenced operands opt out entirely - that is the fence principle, and it is
    why `(웃) + (웃)` holds while the unfenced `웃 + 0웃` drops."""
    if t[0] != "+":
        return None
    fenced, totals, order = [], {}, []
    for term in t[1:]:
        if term[0] == "coeff" and numeric(term[1]) is not None:
            c, body = numeric(term[1]), term[2]
        else:
            c, body = Fraction(1), term
        if body[0] == "group" or term[0] == "group":
            fenced.append(term)
            continue
        if body not in totals:
            totals[body] = Fraction(0); order.append(body)
        totals[body] += c
    kept = [b if totals[b] == 1 else ("coeff", num(totals[b]), b)
            for b in order if totals[b] != 0]
    result = kept + fenced
    if not result:
        return num(0)
    new = add(result) if len(result) > 1 else result[0]
    return new if new != t else None


def float_tints(t):
    """Typed ones float left into a sorted coefficient prefix.

    A canonical ordering, not a swap rule: `X Y^0 -> Y^0 X` is permutative and
    would let the normalizer cycle forever, while extract-sort-prepend cannot."""
    if t[0] != "seq":
        return None
    tints = [x for x in t[1:] if is_typed_one(x)]
    rest = [x for x in t[1:] if not is_typed_one(x)]
    if not tints or not rest:
        return None
    new = seq(sorted(tints, key=show) + rest)
    return new if new != t else None


def angled_eval(t):
    """`(> ... <)`: value semantics, contiguous same-symbol runs sum.

    The brackets DISSOLVE once evaluated - `(> <)` yields a value, it is not a
    fence.  Exponent 1 collapses here and only here: as a global `S^1 -> S` it
    would fire inside `웃^1 ** 웃^-1` before the fusion ladder could see it,
    destroying the shape annihilation matches on.

    Fires innermost-first (see `rewrites`), so nested `**` and inner groups are
    already resolved by the time we get here - v7's stated evaluation order.
    """
    if t[0] != "angle":
        return None
    body = t[1]
    if body[0] != "seq":
        return contract_run(body) or body if body[0] == "group" else body

    merged = []
    for item in (contract_run(x) or x for x in body[1:]):
        cur = _power(item)
        if cur and merged:
            prev = _power(merged[-1])
            if prev and prev[0] == cur[0]:
                merged[-1] = ("pow", cur[0], num(prev[1] + cur[1]))
                continue
        merged.append(item)
    # Only `("pow", b, 1)` collapses to its base.  Guarding on `_power` instead
    # would also match a bare atom, whose `[1]` is its *name string* - which
    # silently puts a str where a term belongs.
    return seq([x[1] if x[0] == "pow" and numeric(x[2]) == 1 else x for x in merged])


def _power(t):
    if t[0] == "pow" and numeric(t[2]) is not None:
        return t[1], numeric(t[2])
    return (t, Fraction(1)) if t[0] in ("atom", "group") else None


BUILTINS = {"contract_run": contract_run, "collect_sum": collect_sum,
            "float_tints": float_tints, "angled_eval": angled_eval}


# --------------------------------------------------------------------------
# rewriting
# --------------------------------------------------------------------------

def fold_values(t):
    """Fold numeric exponent arithmetic after substitution, so a markdown rule
    can write `S^a ** S^b -> S^(a + 1)` and get a number out.

    `S^-n` in an RHS builds `("neg", var n)`, which substitution turns into
    `("neg", num 3)` - while the literal `웃^-3` parses straight to `num(-3)`.
    Without folding those are different terms with the same value, and every
    rule that negates an exponent silently stops matching."""
    ks = kids(t)
    if ks:
        t = rebuild(t, [fold_values(k) for k in ks])
    if t[0] == "neg" and t[1][0] == "num":
        return num(-t[1][1])
    if t[0] == "exp" and t[1] in "+-*/":
        a, b = numeric(t[2]), numeric(t[3])
        if a is not None and b is not None and not (t[1] == "/" and b == 0):
            return num({"+": a + b, "-": a - b, "*": a * b, "/": b and a / b}[t[1]])
    return t


@dataclass(frozen=True)
class Step:
    rule_id: str
    direction: str
    path: Tuple[int, ...]
    before: tuple            # the subterm rewritten
    after: tuple
    # ...and the enclosing terms, so a trace shows the whole expression
    # evolving.  A derivation read as a list of detached subterms is close to
    # useless when the interesting part is where the rewrite landed.
    whole_before: tuple = None
    whole_after: tuple = None

    def flipped(self):
        return Step(self.rule_id, "<-" if self.direction == "->" else "->",
                    self.path, self.after, self.before,
                    self.whole_after, self.whole_before)

    def render(self):
        where = "root" if not self.path else "@" + ".".join(map(str, self.path))
        shown = self.whole_after if self.whole_after is not None else self.after
        return "  = %s  [%s %s %s]" % (show(shown), self.rule_id,
                                       self.direction, where)


@dataclass
class Budget:
    max_normalize_steps: int = 200
    max_nodes: int = 4000
    max_depth: int = 6
    max_size: int = 60


def apply_rule(rule, sub, backward=False):
    """Every way `rule` rewrites the whole of `sub`."""
    if rule.builtin:
        if backward:
            return
        out = BUILTINS[rule.builtin](sub)
        if out is not None and out != sub:
            yield out
        return
    if rule.lhs is None:
        return
    lhs, rhs = open_seq(*((rule.rhs, rule.lhs) if backward else (rule.lhs, rule.rhs)))
    for env in match(lhs, sub):
        if not backward and not check_condition(rule.condition, env):
            continue
        try:
            out = fold_values(subst(rhs, env))
        except KeyError:
            continue          # RHS names a variable the LHS never binds
        if out != sub:
            yield out


def rewrites(term, ruleset, kinds=(REDUCE,), backward=False):
    """Every single-step rewrite of `term`, with its trace record.

    Innermost-first: `walk` is outermost-first, so it is reversed.  Subterms
    must settle before their parents, which is what makes v7's `(> <)`
    evaluation order ("resolve ** first, then contract, then sum") come out
    without special-casing it.
    """
    cands = [r for r in ruleset if r.kind in kinds and not r.holds]
    for path, sub in reversed(list(walk(term))):
        spent = set()
        for rule in cands:
            # v7's fusion is "a sequential case ladder (checked in order)", so
            # once one case fires the rest must not.
            if rule.ladder and rule.ladder in spent:
                continue
            for out in apply_rule(rule, sub, backward):
                spent.add(rule.ladder)
                whole = replace(term, path, out)
                yield whole, Step(rule.id, "<-" if backward else "->", path,
                                  sub, out, term, whole)


@dataclass
class Normalization:
    start: tuple
    result: tuple
    steps: List[Step] = field(default_factory=list)
    cycle: Optional[List[tuple]] = None
    exhausted: bool = False

    def render(self):
        return "\n".join([show(self.start)] + [s.render() for s in self.steps])


def normalize(term, ruleset, budget=None):
    budget = budget or Budget()
    out = Normalization(term, term)
    seen, trail, cur = {term: 0}, [term], term
    for n in range(budget.max_normalize_steps):
        nxt = next(iter(rewrites(cur, ruleset)), None)
        if nxt is None:
            out.result = cur
            return out
        cur, step = nxt
        out.steps.append(step)
        if cur in seen:
            out.cycle = trail[seen[cur]:] + [cur]
            out.result = cur
            return out
        seen[cur] = n + 1
        trail.append(cur)
    out.result, out.exhausted = cur, True
    return out


def normal_forms(term, ruleset, budget=None, cap=400):
    """All terminal forms reachable by any rule order.  More than one means the
    oriented rules are non-confluent here - something v7 concedes has never
    been checked."""
    budget = budget or Budget()
    finals, seen, stack = set(), {term}, [term]
    while stack and len(seen) < cap:
        cur = stack.pop()
        moved = False
        for nxt, _ in rewrites(cur, ruleset):
            moved = True
            if nxt not in seen and size(nxt) <= budget.max_size:
                seen.add(nxt); stack.append(nxt)
        if not moved:
            finals.add(cur)
    return finals


# --------------------------------------------------------------------------
# proving
# --------------------------------------------------------------------------

@dataclass
class Proof:
    status: str
    left: tuple
    right: tuple
    steps: List[Step] = field(default_factory=list)
    nodes: int = 0
    closest: Optional[Tuple[tuple, tuple]] = None
    touched: Set[str] = field(default_factory=set)

    @property
    def proved(self):
        return self.status == PROVED

    def render(self):
        if not self.proved:
            head = "%s: %s  vs  %s" % (self.status, show(self.left), show(self.right))
            if self.closest:
                head += "\n  closest pair reached:\n    %s\n    %s" % (
                    show(self.closest[0]), show(self.closest[1]))
            return head
        return "\n".join([show(self.left)] + [s.render() for s in self.steps])


def prove(left, right, ruleset, budget=None):
    """Meet-in-the-middle BFS over `==` rules, normalizing every frontier node."""
    budget = budget or Budget()
    nl, nr = normalize(left, ruleset, budget), normalize(right, ruleset, budget)
    touched = {s.rule_id for s in nl.steps} | {s.rule_id for s in nr.steps}

    if nl.result == nr.result:
        return Proof(PROVED, left, right,
                     nl.steps + [s.flipped() for s in reversed(nr.steps)],
                     nodes=2, touched=touched)

    fwd, bwd = {nl.result: []}, {nr.result: []}
    front_f, front_b = [nl.result], [nr.result]
    explored, stop = 2, False

    for _ in range(budget.max_depth):
        for forward in (True, False):
            frontier, seen, other = ((front_f, fwd, bwd) if forward
                                     else (front_b, bwd, fwd))
            nxt = []
            for node in frontier:
                for cand, step in _expand(node, ruleset, budget):
                    touched.add(step.rule_id)
                    norm = normalize(cand, ruleset, budget)
                    touched |= {s.rule_id for s in norm.steps}
                    cand = norm.result
                    if cand in seen:
                        continue
                    # Record the re-normalization too, or the rendered chain
                    # jumps to a normal form with no rule named for the gap.
                    seen[cand] = seen[node] + [step] + norm.steps
                    explored += 1
                    if cand in other:
                        return _stitch(left, right, cand, fwd, bwd, nl, nr,
                                       explored, touched)
                    nxt.append(cand)
                    if explored >= budget.max_nodes:
                        stop = True
                        break
                if stop:
                    break
            if forward:
                front_f = nxt
            else:
                front_b = nxt
            if stop:
                break
        if stop:
            break
        if not front_f and not front_b:
            return Proof(CLOSED, left, right, nodes=explored,
                         closest=_closest(fwd, bwd), touched=touched)

    status = EXHAUSTED if (stop or front_f or front_b) else CLOSED
    return Proof(status, left, right, nodes=explored,
                 closest=_closest(fwd, bwd), touched=touched)


def _expand(node, ruleset, budget):
    for backward in (False, True):
        for nxt, step in rewrites(node, ruleset, (EQUIV,), backward):
            if size(nxt) <= budget.max_size:
                yield nxt, step


def _stitch(left, right, meet, fwd, bwd, nl, nr, explored, touched):
    steps = list(nl.steps) + list(fwd[meet])
    steps += [s.flipped() for s in reversed(bwd[meet])]
    steps += [s.flipped() for s in reversed(nr.steps)]
    return Proof(PROVED, left, right, steps, nodes=explored, touched=touched)


def _closest(fwd, bwd):
    """The nearest the two frontiers got - usually points at the missing axiom."""
    best = pair = None
    for a in list(fwd)[:60]:
        for b in list(bwd)[:60]:
            d = abs(size(a) - size(b)) + (0 if a[0] == b[0] else 3)
            if best is None or d < best:
                best, pair = d, (a, b)
    return pair
