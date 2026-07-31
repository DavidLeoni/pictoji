"""Markdown loading: chained relations, the bracket trap, tags, directives."""

from pictoji_algebra.specload import load_text, split_top_level

SPEC = """\
# Title

## Grouping and powers

Prose is ignored, including inline `A == B`.

```text
LHS == RHS   this is a format legend, not a statement
```

    웃 웃  !=  (웃 웃)
    A ¬= B ¬= C
    S^a ** S^b -> S^0 , a == -b               # [ladder=fusion] [id=fus.annihilate]
    X / D -> X ** D^-1  , grade(D) != 0
    (A B)^-1 == B^-1 A^-1                     # [rule] [id=inv]
    웃^2 == (웃 웃)
    dead -> letter                            # [off]
"""


def test_bracket_aware_split_ignores_nested_relations():
    """v7:366 writes `X / D  (grade(D) ¬= 0)  ->  X ** D^-1`."""
    line = "X / D   (grade(D) ¬= 0)   ->   X ** D^-1"
    ops = [op for _, op in split_top_level(line, ["¬=", "->", "=="])]
    assert ops == ["->"], "a ¬= inside parens is not the statement's relation"


def test_loads_without_problems():
    spec = load_text(SPEC, "spec.md")
    assert spec.problems == []


def test_prose_and_tagged_fences_are_not_statements():
    spec = load_text(SPEC, "spec.md")
    assert all("legend" not in a.text for a in spec.assertions)
    assert all("legend" not in r.text for r in spec.rules)


def test_chained_relations_expand_pairwise():
    spec = load_text(SPEC, "spec.md")
    chained = [a for a in spec.assertions if a.id.startswith("grouping-and-powers.02")]
    assert len(chained) == 2
    assert {repr(a.left) for a in chained} == {"A", "B"}


def test_relation_kinds():
    spec = load_text(SPEC, "spec.md")
    kinds = {a.kind for a in spec.assertions}
    assert "neq" in kinds and "eq" in kinds


def test_equalities_are_assertions_unless_marked_rule():
    spec = load_text(SPEC, "spec.md")
    assert spec.rules.get("inv") is not None                       # [rule]
    assert any(a.text.startswith("웃^2") for a in spec.assertions)  # plain ==


def test_side_condition_is_split_off_before_the_relation():
    spec = load_text(SPEC, "spec.md")
    rule = spec.rules.get("fus.annihilate")
    assert rule.condition == "a == -b"
    assert rule.ladder == "fusion"
    assert "**" in rule.text and "," not in rule.text


def test_tags_come_from_headings_and_exclude_the_title():
    spec = load_text(SPEC, "spec.md")
    assert "grouping-and-powers" in spec.rules.tags
    assert "title" not in spec.rules.tags


def test_off_directive_disables():
    spec = load_text(SPEC, "spec.md")
    assert all("dead" not in r.text for r in spec.rules)


def test_unparseable_line_is_reported_not_dropped():
    spec = load_text("## S\n\n    웃 ((( == 웃\n", "spec.md")
    assert len(spec.problems) == 1
    assert "spec.md:3" == spec.problems[0].source


def test_selectors_resolve_by_id_and_tag():
    rules = load_text(SPEC, "spec.md").rules
    assert [r.id for r in rules.matching("inv")] == ["inv"]
    assert len(rules.matching("grouping-and-powers")) == len(rules)
    assert rules.unresolved_selectors(["nope"]) == ["nope"]
    assert rules.disable(["inv"]).get("inv") is None
