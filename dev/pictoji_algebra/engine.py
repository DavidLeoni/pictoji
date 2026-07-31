"""The rewriter, the normalizer, and the bidirectional prover.

Two tiers:

* **Tier 1 - normalization.**  Oriented `->` rules applied to a fixpoint.  This
  is what "reduces to" means, and it is deterministic: the first applicable
  rewrite in rule order wins.
* **Tier 2 - saturation.**  For `==` goals, breadth-first search outward from
  *both* sides using `==` rules in both directions, normalizing every frontier
  node, meeting in the middle.

Tier 2 exists because form-is-substance makes `==` a real proof obligation
rather than a comparison: `웃^2` and `(웃 웃)` are different terms that the
algebra nonetheless equates.

Three outcomes, never two.  `PROVED`, `EXHAUSTED` (ran out of budget - we do
not know) and `CLOSED` (search space exhausted - not provable with these
axioms).  Collapsing EXHAUSTED into "not equal" would make an inconsistency
hunter lie about the one thing it exists to detect.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, Iterator, List, Optional, Sequence, Set, Tuple

from .builtins import INVERSE, REGISTRY
from .patterns import check_condition, match, subst
from .rules import EQUIV, REDUCE, Rule, RuleSet
from .terms import ExpOp, Neg, Num, Seq, Term, replace, seq, size, walk

PROVED = "PROVED"
EXHAUSTED = "EXHAUSTED"
CLOSED = "CLOSED"


# --------------------------------------------------------------------------
# derivation records
# --------------------------------------------------------------------------

@dataclass(frozen=True)
class Step:
    rule_id: str
    direction: str            # '->' forward, '<-' backward (an `==` run in reverse)
    path: Tuple[int, ...]
    before: Term              # the subterm that was rewritten
    after: Term               # what it became
    # The enclosing terms too, so a trace can show the whole expression
    # evolving.  Reading a derivation as a list of detached subterms is close
    # to useless when the interesting part is where the rewrite landed.
    whole_before: Optional[Term] = None
    whole_after: Optional[Term] = None

    def reversed_(self) -> "Step":
        return Step(self.rule_id, "<-" if self.direction == "->" else "->", self.path,
                    self.after, self.before, self.whole_after, self.whole_before)

    def render(self) -> str:
        where = "root" if not self.path else "@" + ".".join(map(str, self.path))
        shown = self.whole_after if self.whole_after is not None else self.after
        return "  = %r  [%s %s %s]" % (shown, self.rule_id, self.direction, where)


@dataclass
class Budget:
    """Search limits.  Hitting one yields EXHAUSTED, which is reported."""
    max_normalize_steps: int = 200
    max_nodes: int = 4000
    max_depth: int = 6
    max_size: int = 60          # node count; stops factoring rules exploding

    def copy(self) -> "Budget":
        return Budget(self.max_normalize_steps, self.max_nodes, self.max_depth, self.max_size)


# --------------------------------------------------------------------------
# right-hand side value folding
# --------------------------------------------------------------------------

def fold_values(t: Term) -> Term:
    """Fold numeric exponent arithmetic after substitution.

    Lets a markdown rule write `S^a ** S^b -> S^(a + 1)` and get a number out.
    Only `+ - * /` fold; `**` and `++` never do, since v7 keeps those as form.
    """
    kids = t.children()
    if kids:
        t = t.rebuild([fold_values(k) for k in kids])
    # `S^-n` in a rule RHS builds `Neg(Var n)`, which substitution turns into
    # `Neg(Num(3))` - while the literal `웃^-3` parses straight to `Num(-3)`.
    # Without this fold the two are different terms with the same value, and
    # every rule that negates an exponent silently stops matching.
    if isinstance(t, Neg) and isinstance(t.body, Num):
        return Num(-t.body.value)
    if isinstance(t, ExpOp) and t.op in ("+", "-", "*", "/"):
        if isinstance(t.left, Num) and isinstance(t.right, Num):
            a, b = t.left.value, t.right.value
            if t.op == "+":
                return Num(a + b)
            if t.op == "-":
                return Num(a - b)
            if t.op == "*":
                return Num(a * b)
            if t.op == "/" and b != 0:
                return Num(a / b)
    return t


# --------------------------------------------------------------------------
# single-step rewriting
# --------------------------------------------------------------------------

def _apply_at(rule: Rule, sub: Term, backward: bool) -> Iterator[Term]:
    """Every way `rule` rewrites the whole of `sub`."""
    if rule.builtin:
        name = rule.builtin
        if backward:
            # Most builtins are computational and one-way; the few that are
            # genuinely equational (factoring/distribution) declare an inverse.
            name = INVERSE.get(name)
            if name is None:
                return
        fn = REGISTRY.get(name)
        if fn is None:
            raise KeyError("rule %s names unknown builtin %r" % (rule.id, name))
        out = fn(sub)
        if out is not None and out != sub:
            yield out
        return

    lhs, rhs = (rule.rhs, rule.lhs) if backward else (rule.lhs, rule.rhs)
    if lhs is None or rhs is None:
        return

    for env in match(lhs, sub):
        if not backward and not check_condition(rule.condition, env):
            continue
        try:
            out = fold_values(subst(rhs, env))
        except KeyError:
            # RHS mentions a variable the LHS never binds.  Backward use of a
            # rule like `A / A == 1` is genuinely ill-defined, so skip rather
            # than invent a binding.
            continue
        if out != sub:
            yield out


def _window_rewrites(rule: Rule, sub: Seq, backward: bool) -> Iterator[Term]:
    """Match a short Seq pattern against a contiguous run inside a longer Seq.

    This is what makes `웃^0 웃 -> 웃` fire inside `🌳 웃^0 웃 🐶` without needing
    a separate rule per context.  Only contiguous windows are tried: matching a
    2-pattern against a 3-run by implicitly regrouping would invent a fence,
    and fences are substance.
    """
    lhs = rule.rhs if backward else rule.lhs
    if not isinstance(lhs, Seq):
        return
    k, n = len(lhs.items), len(sub.items)
    if k >= n:
        return
    for start in range(n - k + 1):
        window = Seq(sub.items[start : start + k])
        for out in _apply_at(rule, window, backward):
            spliced = list(sub.items[:start])
            spliced += list(out.items) if isinstance(out, Seq) else [out]
            spliced += list(sub.items[start + k :])
            yield seq(spliced)


def _ladder_filter(rules: Sequence[Rule], sub: Term, backward: bool) -> List[Rule]:
    """Enforce ordered case ladders: within a ladder, the first match wins.

    v7's fusion is "a sequential case ladder (checked in order)", so once
    `a == 0` matches, the later `a == b` case must not also fire.  Without this
    the ladder would be a set of unordered rules and fusion would be
    non-deterministic by construction.
    """
    out, spent = [], set()
    for r in rules:
        if r.ladder is None:
            out.append(r)
            continue
        if r.ladder in spent:
            continue
        applies = any(True for _ in _apply_at(r, sub, backward))
        if not applies and isinstance(sub, Seq):
            applies = any(True for _ in _window_rewrites(r, sub, backward))
        if applies:
            out.append(r)
            spent.add(r.ladder)
    return out


def rewrites(term: Term, ruleset: RuleSet, kinds=(REDUCE,),
             backward: bool = False) -> Iterator[Tuple[Term, Step]]:
    """Yield every single-step rewrite of `term`, with its trace record."""
    candidates = [r for r in ruleset if r.kind in kinds and not r.holds]
    # Innermost-first.  `walk` is outermost-first, so reverse it: subterms must
    # settle before their parents rewrite, which is what makes v7's stated
    # `(> <)` evaluation order ("resolve ** first, then contract, then sum")
    # come out right without special-casing it.
    for path, sub in reversed(list(walk(term))):
        for rule in _ladder_filter(candidates, sub, backward):
            outs = list(_apply_at(rule, sub, backward))
            if isinstance(sub, Seq):
                outs += list(_window_rewrites(rule, sub, backward))
            for out in outs:
                whole = replace(term, path, out)
                yield whole, Step(rule.id, "<-" if backward else "->", path,
                                  sub, out, term, whole)


# --------------------------------------------------------------------------
# tier 1: normalization
# --------------------------------------------------------------------------

@dataclass
class Normalization:
    start: Term
    result: Term
    steps: List[Step] = field(default_factory=list)
    cycle: Optional[List[Term]] = None      # non-termination, with the loop
    exhausted: bool = False

    def render(self) -> str:
        lines = [repr(self.start)]
        lines += [s.render() for s in self.steps]
        return "\n".join(lines)


def normalize(term: Term, ruleset: RuleSet, budget: Optional[Budget] = None) -> Normalization:
    """Apply oriented rules to a fixpoint, innermost-biased, first match wins."""
    budget = budget or Budget()
    out = Normalization(start=term, result=term)
    seen: Dict[Term, int] = {term: 0}
    trail: List[Term] = [term]
    current = term

    for n in range(budget.max_normalize_steps):
        nxt = None
        # `walk` is outermost-first; reversing biases toward innermost redexes,
        # which keeps subterms settled before their parents rewrite.
        for candidate, step in rewrites(current, ruleset):
            nxt = (candidate, step)
            break
        if nxt is None:
            out.result = current
            return out
        current, step = nxt
        out.steps.append(step)
        if current in seen:
            out.cycle = trail[seen[current]:] + [current]
            out.result = current
            return out
        seen[current] = n + 1
        trail.append(current)

    out.result = current
    out.exhausted = True
    return out


def normal_form(term: Term, ruleset: RuleSet, budget: Optional[Budget] = None) -> Term:
    return normalize(term, ruleset, budget).result


def normal_forms(term: Term, ruleset: RuleSet, budget: Optional[Budget] = None,
                 cap: int = 400) -> Set[Term]:
    """All terminal forms reachable by *any* rule order.

    More than one means the oriented rule set is non-confluent at this term -
    a real defect, and one v7 admits has never been checked.
    """
    budget = budget or Budget()
    finals: Set[Term] = set()
    seen: Set[Term] = {term}
    stack = [term]
    while stack and len(seen) < cap:
        cur = stack.pop()
        moved = False
        for nxt, _ in rewrites(cur, ruleset):
            moved = True
            if nxt not in seen and size(nxt) <= budget.max_size:
                seen.add(nxt)
                stack.append(nxt)
        if not moved:
            finals.add(cur)
    return finals


# --------------------------------------------------------------------------
# tier 2: bidirectional saturation
# --------------------------------------------------------------------------

@dataclass
class Proof:
    status: str                              # PROVED | EXHAUSTED | CLOSED
    left: Term
    right: Term
    steps: List[Step] = field(default_factory=list)
    meeting: Optional[Term] = None
    nodes_explored: int = 0
    closest: Optional[Tuple[Term, Term]] = None   # best near-miss, for diagnosis
    # Every rule that fired anywhere during the attempt, successful or not.
    # `steps` alone would under-report: a failed proof has no steps, so rules
    # that did fire during normalization would be miscounted as dead.
    touched: Set[str] = field(default_factory=set)

    @property
    def proved(self) -> bool:
        return self.status == PROVED

    def render(self) -> str:
        if not self.proved:
            head = "%s: %r  vs  %r" % (self.status, self.left, self.right)
            if self.closest:
                head += "\n  closest pair reached:\n    %r\n    %r" % self.closest
            return head
        lines = ["%r" % self.left]
        lines += [s.render() for s in self.steps]
        return "\n".join(lines)


def _expand(node: Term, ruleset: RuleSet, budget: Budget) -> Iterator[Tuple[Term, Step]]:
    """One equational step in either direction, then re-normalize."""
    for kinds, backward in ((( EQUIV,), False), ((EQUIV,), True)):
        for nxt, step in rewrites(node, ruleset, kinds=kinds, backward=backward):
            if size(nxt) <= budget.max_size:
                yield nxt, step


def prove(left: Term, right: Term, ruleset: RuleSet,
          budget: Optional[Budget] = None) -> Proof:
    """Try to prove `left == right`.  Meet-in-the-middle BFS over `==` rules."""
    budget = budget or Budget()

    nl = normalize(left, ruleset, budget)
    nr = normalize(right, ruleset, budget)
    ln, rn = nl.result, nr.result
    touched = {s.rule_id for s in nl.steps} | {s.rule_id for s in nr.steps}

    if ln == rn:
        return Proof(PROVED, left, right,
                     nl.steps + [s.reversed_() for s in reversed(nr.steps)],
                     meeting=ln, nodes_explored=2, touched=touched)

    # path[node] = (steps from that side's root to node)
    fwd: Dict[Term, List[Step]] = {ln: []}
    bwd: Dict[Term, List[Step]] = {rn: []}
    frontier_f, frontier_b = [ln], [rn]
    explored = 2
    exhausted = False

    for _ in range(budget.max_depth):
        for frontier, seen, other, is_forward in (
            (frontier_f, fwd, bwd, True),
            (frontier_b, bwd, fwd, False),
        ):
            nxt_frontier = []
            for node in frontier:
                for cand, step in _expand(node, ruleset, budget):
                    touched.add(step.rule_id)
                    norm = normalize(cand, ruleset, budget)
                    touched |= {s.rule_id for s in norm.steps}
                    cand = norm.result
                    if cand in seen:
                        continue
                    # Record the re-normalization too, or the rendered chain
                    # jumps from an expanded term straight to its normal form
                    # with no rule named for the gap.
                    seen[cand] = seen[node] + [step] + norm.steps
                    explored += 1
                    if cand in other:
                        return _stitch(left, right, cand, fwd, bwd, nl, nr,
                                       explored, touched)
                    nxt_frontier.append(cand)
                    if explored >= budget.max_nodes:
                        exhausted = True
                        break
                if exhausted:
                    break
            if is_forward:
                frontier_f = nxt_frontier
            else:
                frontier_b = nxt_frontier
            if exhausted:
                break
        if exhausted:
            break
        if not frontier_f and not frontier_b:
            return Proof(CLOSED, left, right, nodes_explored=explored,
                         closest=_closest(fwd, bwd), touched=touched)

    status = EXHAUSTED if (exhausted or frontier_f or frontier_b) else CLOSED
    return Proof(status, left, right, nodes_explored=explored,
                 closest=_closest(fwd, bwd), touched=touched)


def _stitch(left: Term, right: Term, meet: Term,
            fwd: Dict[Term, List[Step]], bwd: Dict[Term, List[Step]],
            nl: Normalization, nr: Normalization, explored: int,
            touched: Set[str]) -> Proof:
    """Join the two half-derivations into one top-to-bottom chain."""
    steps = list(nl.steps) + list(fwd[meet])
    steps += [s.reversed_() for s in reversed(bwd[meet])]
    steps += [s.reversed_() for s in reversed(nr.steps)]
    return Proof(PROVED, left, right, steps, meeting=meet,
                 nodes_explored=explored, touched=touched)


def _closest(fwd: Dict[Term, List[Step]], bwd: Dict[Term, List[Step]]):
    """The nearest pair the two frontiers got to each other.

    Purely diagnostic: when an asserted `==` will not go through, this usually
    points straight at the missing axiom.
    """
    best, pair = None, None
    for a in list(fwd)[:60]:
        for b in list(bwd)[:60]:
            d = abs(size(a) - size(b)) + (0 if type(a) is type(b) else 3)
            if best is None or d < best:
                best, pair = d, (a, b)
    return pair
