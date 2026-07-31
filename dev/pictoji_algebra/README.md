# pictoji_algebra - an interpreter for checking the algebra

Loads Pictoji algebra axioms from a markdown spec and checks the `==` / `!=`
test cases in it.  Stdlib only, four modules, no dependencies.

**It assumes the algebra is inconsistent.**  Its job is not to go green; it is
to say precisely what breaks and which axioms broke it.  v7's own closing
section concedes that no machine check of termination or confluence has ever
been run, and the amendments record seven further unmet obligations.

**Nothing about a particular algebra revision lives in Python.**  Axioms,
assertions and known failures are all markdown, so a v7 -> v8 bump edits
`pictoji-test-algebra.md` and nothing else.  `test_suite.py` enforces this.

Everything is under `dev/`, which `dev/README.md` marks as ignored by AI
parsers.  The installed `pictoji` package is untouched.


## Usage

```bash
cd dev

python3 -m pictoji_algebra check pictoji-test-algebra.md      # run the suite
python3 -m pictoji_algebra check ... --bisect                 # minimize any canary
python3 -m pictoji_algebra check ... --disable fusion         # drop a chapter
python3 -m pictoji_algebra rules                              # list rules + tags
python3 -m pictoji_algebra normalize "(웃 웃) (웃 웃 웃)"
python3 -m pictoji_algebra prove "웃^2 웃^3" "(웃 웃) (웃 웃 웃)"

python3 -m pytest pictoji_algebra/tests -v    # tests (preferred)
python3 run_tests.py                          # fallback when pytest is absent
```

Exit code is nonzero when a canary trips or an assertion fails, so it can be a
CI gate.  A selector matching nothing is an error, not a silent no-op.


## Statements

| | |
|---|---|
| `LHS -> RHS`, `LHS = RHS` | oriented rule |
| `LHS == RHS` | assertion the prover must derive (`[rule]` makes it an axiom) |
| `LHS ~> RHS` | assertion that LHS *normalizes* to exactly RHS |
| `LHS != RHS` | **canary**: the prover must NOT derive it |
| `LHS -> RHS , COND` | rule with a side condition |

One relation per line; chains are rejected rather than guessed at.  Directives
live in the trailing comment: `[rule]`, `[id=]`, `[tags=]`, `[ladder=]`,
`[builtin=]`, `[expect=fail]`, `[off]`.  Rules inherit tags from their markdown
headings, so `--disable fusion` works unannotated.

A tripped canary is a proof of inconsistency and is automatically delta-debugged
(`ddmin`) to a minimal subset of rules that still derives it.

Findings, worst first: `canary-tripped`, `non-terminating`, `non-confluent`,
`unprintable`, `failed-equality`, `failed-normalization`, `unexpected-pass`,
`unproved-budget`, `unparsed`.

Three proof outcomes, never two: `PROVED`, `CLOSED` (not derivable with these
axioms), `EXHAUSTED` (budget ran out - unknown).  Reporting EXHAUSTED as a
disproof would make the tool lie about the one thing it exists to detect.


## Design

**Terms are plain tuples** - `("seq", a, b)`, `("group", x)`, `("pow", b, e)`.
Form-is-substance is why no typed AST is needed: no node has behaviour of its
own, all behaviour is in the rules, and form equality *is* tuple equality.  So
`S S != (S S)` and `(A B) C != A (B C) != A B C` hold by construction.

`+` is the one exception: its operands are stored sorted, because v7 states
outright that addition is associative and commutative, so order is not
substance there.

**The printer may never insert parentheses, because parentheses are fences.**
`parse(show(t)) == t` is therefore not cosmetic - it is a check that nothing
fabricates a term with no surface form, and `unprintable` is a finding about the
algebra rather than a printer nit.  This property caught a real bug: `웃^(1/2)`
used to print as `웃^1/2`, which re-parses as `(웃^1)/2`, silently corrupting
every sub-unit fusion trace.

**Segment variables** (`A..`) bind a run of siblings, so context-sensitive laws
stay in markdown instead of becoming Python.  A `seq` pattern with no explicit
segment variables gets two implicitly, so `X^0 X -> X` still fires inside a
longer run without a rule per context.

**Unicode**: NFC-normalized and segmented by grapheme cluster, so `👩‍🚀` and `❤️`
are one token each - the shipped analyzer (`pictoji/cli/__init__.py:225`)
iterates per code point and counts them 5 and 2, contradicting
`pictoji.md:4861`.  Spec files are read `utf-8-sig`, since every `.md` here has
a BOM.  Superscripts and subscripts fold to `^n` / `_n` at lex time via explicit
tables: superscript 1/2/3 are Latin-1 leftovers and subscript letters span three
blocks, so a range check would silently mangle them.


## Layout

    terms.py     graphemes, lexing, s-expression terms, parsing, printing
    engine.py    matching (+segment vars), conditions, builtins, normalize, prove
    spec.py      markdown loader, rules/tags, findings, ddmin, report
    __main__.py  CLI

    pictoji-test-algebra.md            the axioms under test (v7 core)
    pictoji-test-machinery.md          toy algebra the engine tests run on
    pictoji-algebra-extraction-prompt.md   prompt for turning prose into rules

Only four builtins remain, the steps that are genuinely n-ary or arithmetic:
`contract_run`, `collect_sum`, `float_tints`, `angled_eval`.  Everything else is
a markdown rule, so the bisector can name it.


## Not covered yet

- **Amendments A and B.**  They contradict v7 and each other by design; loading
  them is the next experiment and is a markdown change, not a code change.
- **`pictoji.md`** (5126 lines).  The loader is file-agnostic - pointing it at
  the big spec is a CLI argument.
- **`pictoji-test.md`**, which holds natural-language *decoding* assertions - a
  different judgement than algebraic equality.
- The `R` relation layer, `ᛠ` classifiers and filter semantics get parsing and
  term representation but no reduction rules; v7 calls them placeholders.
