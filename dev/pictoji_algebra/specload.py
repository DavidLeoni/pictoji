"""Markdown -> (RuleSet, assertions).

The axioms live in the spec file, not in Python.  A statement is an indented or
fenced line of the form:

    LHS  ->  RHS                  # oriented rule
    LHS  =   RHS                  # oriented rule (law definition)
    LHS  ==  RHS                  # assertion to prove   ([rule] makes it an axiom)
    LHS  !=  RHS                  # CANARY: must NOT be provable
    LHS  ->  RHS , COND           # rule with a side condition

Trailing `# ...` is a comment, and `[id=]`, `[tags=]`, `[rule]`, `[off]`,
`[builtin=]`, `[ladder=]` inside it are directives.  Every rule also inherits
tags from its enclosing markdown headings, so `--disable grouping-and-powers`
works with no annotation at all.

Chained relations are expanded pairwise: `A != B != C` is two assertions.  The
splitter is bracket-aware, because v7 writes conditions like
`X / D  (grade(D) ¬= 0)  ->  X ** D^-1` where a `¬=` sits *inside* parentheses
and is emphatically not the statement's relation.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Dict, FrozenSet, List, Optional, Sequence, Tuple

from .graphemes import graphemes, read_spec
from .lexer import LexError
from .parser import ParseError, parse
from .rules import EQUIV, REDUCE, Rule, RuleSet
from .terms import Term

# Longest first: `->` must win over `-`, `==` over `=`, `¬==` over `¬=`.
RELATIONS = ["k->", "¬==", "!=", "¬=", "==", "~>", "->", "="]
OPEN, CLOSE = {"(", "[", "{"}, {")", "]", "}"}

DIRECTIVE = re.compile(r"\[(\w+)(?:=([^\]]*))?\]")


@dataclass(frozen=True)
class Assertion:
    id: str
    kind: str                 # 'eq' | 'neq'
    left: Term
    right: Term
    tags: FrozenSet[str]
    source: str
    text: str

    @property
    def is_canary(self) -> bool:
        return self.kind == "neq"


@dataclass(frozen=True)
class LoadProblem:
    source: str
    text: str
    reason: str


@dataclass
class SpecFile:
    rules: RuleSet
    assertions: List[Assertion]
    problems: List[LoadProblem]


def slug(text: str) -> str:
    out = re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")
    return out or "section"


def split_top_level(text: str, needles: Sequence[str]) -> List[Tuple[int, str]]:
    """Find `needles` occurring at bracket depth zero, left to right."""
    gs = graphemes(text)
    hits: List[Tuple[int, str]] = []
    depth, i = 0, 0
    while i < len(gs):
        g = gs[i]
        if g in OPEN:
            depth += 1
            i += 1
            continue
        if g in CLOSE:
            depth -= 1
            i += 1
            continue
        if depth == 0:
            for needle in needles:
                ng = graphemes(needle)
                if gs[i : i + len(ng)] == ng:
                    hits.append((i, needle))
                    i += len(ng)
                    break
            else:
                i += 1
            continue
        i += 1
    return hits


def _slice(text: str, start: int, end: Optional[int] = None) -> str:
    gs = graphemes(text)
    return "".join(gs[start:end] if end is not None else gs[start:])


def _strip_comment(line: str) -> Tuple[str, str]:
    """Split a statement from its trailing comment, respecting brackets."""
    hits = split_top_level(line, ["#"])
    if not hits:
        return line, ""
    at = hits[0][0]
    return _slice(line, 0, at), _slice(line, at + 1)


def _directives(comment: str) -> Dict[str, str]:
    return {m.group(1): (m.group(2) or "") for m in DIRECTIVE.finditer(comment)}


def _statement_lines(text: str):
    """Yield `(lineno, statement)` for indented and fenced lines only.

    Prose is ignored.  Headings are consumed to build the tag stack.
    """
    stack: List[str] = []
    in_fence = False
    fence_is_prose = False

    for lineno, raw in enumerate(text.split("\n"), start=1):
        stripped = raw.strip()

        if stripped.startswith("```"):
            if in_fence:
                in_fence, fence_is_prose = False, False
            else:
                # A fence with a language tag is documentation, not statements.
                # This is what keeps the file's own ```text format legend from
                # being loaded as a pile of nonsense rules.
                info = stripped[3:].strip()
                in_fence = True
                fence_is_prose = bool(info) and info != "pictoji"
            continue

        if not in_fence and stripped.startswith("#"):
            level = len(stripped) - len(stripped.lstrip("#"))
            title = stripped[level:].strip()
            del stack[level - 1 :]
            stack.append(slug(title))
            continue

        if not stripped or fence_is_prose:
            continue

        indented = raw.startswith("    ") or raw.startswith("\t")
        if in_fence or indented:
            # Level-1 headings are the document title; tagging every rule with
            # it would add a tag that selects everything and distinguishes
            # nothing.
            yield lineno, stripped, tuple(stack[1:])


def load_text(text: str, filename: str = "<spec>") -> SpecFile:
    rules: List[Rule] = []
    assertions: List[Assertion] = []
    problems: List[LoadProblem] = []
    counters: Dict[str, int] = {}

    for lineno, line, stack in _statement_lines(text):
        source = "%s:%d" % (filename, lineno)
        body, comment = _strip_comment(line)
        body = body.strip()
        if not body:
            continue

        opts = _directives(comment)
        if "off" in opts:
            continue

        chapter = stack[-1] if stack else "spec"
        tags = set(stack) or {"spec"}
        if opts.get("tags"):
            tags |= {t.strip() for t in opts["tags"].split(",") if t.strip()}

        counters[chapter] = counters.get(chapter, 0) + 1
        default_id = "%s.%02d" % (chapter, counters[chapter])
        ident = opts.get("id") or default_id

        # A builtin rule's text is documentation, not a parseable pattern:
        # `(S S ... S) = S^n` has an ellipsis on purpose.
        if "builtin" in opts:
            # `[equiv]` marks a builtin the prover may also run backwards
            # (factoring/distribution); without it the builtin only normalizes.
            rules.append(Rule(
                id=ident, kind=EQUIV if "equiv" in opts else REDUCE,
                lhs=None, rhs=None,
                tags=frozenset(tags), source=source, text=body,
                builtin=opts["builtin"], ladder=opts.get("ladder") or None))
            continue

        # Side condition: a top-level comma splits it off, and it must be taken
        # before the relation split so its own `==` is not mistaken for one.
        condition = None
        commas = split_top_level(body, [","])
        if commas:
            at = commas[-1][0]
            condition = _slice(body, at + 1).strip()
            body = _slice(body, 0, at).strip()

        hits = split_top_level(body, RELATIONS)
        if not hits:
            problems.append(LoadProblem(source, line, "no relation operator"))
            continue

        pieces, prev = [], 0
        for at, op in hits:
            pieces.append(_slice(body, prev, at).strip())
            prev = at + len(graphemes(op))
        pieces.append(_slice(body, prev).strip())

        try:
            terms = [parse(p, pattern=True) for p in pieces]
            plain = [parse(p, pattern=False) for p in pieces]
        except (ParseError, LexError) as exc:
            problems.append(LoadProblem(source, line, str(exc)))
            continue

        for idx, (_, op) in enumerate(hits):
            step_id = ident if len(hits) == 1 else "%s.%d" % (ident, idx + 1)
            lhs_p, rhs_p = terms[idx], terms[idx + 1]
            lhs_c, rhs_c = plain[idx], plain[idx + 1]
            snippet = "%s %s %s" % (pieces[idx], op, pieces[idx + 1])

            if op == "~>":
                # "normalizes to": a Tier-1 assertion.  Distinct from `==`
                # because it also catches rules firing when they should not -
                # `(웃) + (웃) ~> (웃) + (웃)` is a real test, whereas the same
                # line written with `==` would be trivially true.
                assertions.append(Assertion(
                    step_id, "nf", lhs_c, rhs_c, frozenset(tags), source, snippet))
            elif op in ("->", "k->", "="):
                rules.append(Rule(
                    id=step_id, kind=REDUCE, lhs=lhs_p, rhs=rhs_p,
                    tags=frozenset(tags), source=source, text=snippet,
                    condition=condition, ladder=opts.get("ladder") or None,
                    holds=(lhs_p == rhs_p)))
            elif op == "==":
                if "rule" in opts:
                    rules.append(Rule(
                        id=step_id, kind=EQUIV, lhs=lhs_p, rhs=rhs_p,
                        tags=frozenset(tags), source=source, text=snippet,
                        condition=condition, ladder=opts.get("ladder") or None))
                else:
                    assertions.append(Assertion(
                        step_id, "eq", lhs_c, rhs_c, frozenset(tags), source, snippet))
            else:                                     # != / ¬= / ¬==
                assertions.append(Assertion(
                    step_id, "neq", lhs_c, rhs_c, frozenset(tags), source, snippet))

    return SpecFile(RuleSet(rules), assertions, problems)


def load(path) -> SpecFile:
    import os
    return load_text(read_spec(path), os.path.basename(str(path)))
