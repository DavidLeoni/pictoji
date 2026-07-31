"""Rules, tags, and rule-set selection.

Every rule carries a stable `id`, a set of `tags` (auto-derived from the
markdown chapter it was read from, plus anything explicit), and a `source`
pointing back at `file:line`.  All three exist for one reason: when a canary
trips, the bisector must be able to name the guilty axioms in terms the spec
author recognizes.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, FrozenSet, Iterable, List, Optional, Sequence

from .terms import Term

REDUCE = "reduce"      # `->` : oriented, drives normalization
EQUIV = "equiv"        # `==` : bidirectional, drives the prover


@dataclass(frozen=True)
class Rule:
    id: str
    kind: str                            # REDUCE | EQUIV
    lhs: Optional[Term]
    rhs: Optional[Term]
    tags: FrozenSet[str]
    source: str                          # "file.md:123"
    text: str                            # the original line, for reports
    condition: Optional[str] = None
    builtin: Optional[str] = None
    ladder: Optional[str] = None         # ordered case ladders: first match wins
    holds: bool = False                  # RHS == LHS: an explicit "does not fire"

    def __repr__(self) -> str:
        return "<%s %s>" % (self.id, self.text)

    def describe(self) -> str:
        bits = [self.id, self.text.strip()]
        if self.condition:
            bits.append("if %s" % self.condition)
        return "%s  |  %s  [%s]  %s" % (
            bits[0], bits[1], ",".join(sorted(self.tags)), self.source)


class RuleSet:
    """An ordered, filterable collection of rules."""

    def __init__(self, rules: Sequence[Rule]):
        self.rules: List[Rule] = list(rules)
        self._by_id: Dict[str, Rule] = {r.id: r for r in self.rules}

    def __len__(self) -> int:
        return len(self.rules)

    def __iter__(self):
        return iter(self.rules)

    def get(self, rule_id: str) -> Optional[Rule]:
        return self._by_id.get(rule_id)

    @property
    def ids(self) -> List[str]:
        return [r.id for r in self.rules]

    @property
    def tags(self) -> FrozenSet[str]:
        out = set()
        for r in self.rules:
            out |= r.tags
        return frozenset(out)

    # -- selection ---------------------------------------------------------
    def matching(self, selector: str) -> List[Rule]:
        """Resolve a selector to rules: an exact id, a tag, or a `*` glob."""
        import fnmatch
        hit = self._by_id.get(selector)
        if hit is not None:
            return [hit]
        out = [r for r in self.rules if selector in r.tags]
        if out:
            return out
        return [r for r in self.rules
                if fnmatch.fnmatch(r.id, selector)
                or any(fnmatch.fnmatch(t, selector) for t in r.tags)]

    def disable(self, selectors: Iterable[str]) -> "RuleSet":
        drop = set()
        for s in selectors:
            drop |= {r.id for r in self.matching(s)}
        return RuleSet([r for r in self.rules if r.id not in drop])

    def enable_only(self, selectors: Iterable[str]) -> "RuleSet":
        keep = set()
        for s in selectors:
            keep |= {r.id for r in self.matching(s)}
        return RuleSet([r for r in self.rules if r.id in keep])

    def subset(self, ids: Iterable[str]) -> "RuleSet":
        """Used by the bisector; preserves the original rule order."""
        wanted = set(ids)
        return RuleSet([r for r in self.rules if r.id in wanted])

    def of_kind(self, kind: str) -> List[Rule]:
        return [r for r in self.rules if r.kind == kind]

    def unresolved_selectors(self, selectors: Iterable[str]) -> List[str]:
        """Selectors that match nothing - a typo'd `--disable` must not pass silently."""
        return [s for s in selectors if not self.matching(s)]
