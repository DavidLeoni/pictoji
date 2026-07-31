# pictoji_algebra - an interpreter for checking the algebra

A small, dependency-free Python interpreter that loads Pictoji algebra axioms
from a markdown spec and checks the `==` / `!=` test cases in it.

**It assumes the algebra is inconsistent.**  Its job is not to go green; it is
to say precisely what breaks and which axioms broke it.  v7's own closing
section concedes that no machine check of termination or confluence has ever
been run, and Amendments A and B record seven further unmet consistency
obligations.  This is that check.

Everything lives under `dev/`, which `dev/README.md` marks as ignored by AI
parsers.  Nothing in the installed `pictoji` package is touched.


## Usage

```bash
cd dev

python3 -m pictoji_algebra check pictoji-test-algebra.md      # run the suite
python3 -m pictoji_algebra check ... --bisect                 # minimize any canary
python3 -m pictoji_algebra check ... --disable fusion         # drop a chapter
python3 -m pictoji_algebra check ... --enable-only sequences
python3 -m pictoji_algebra rules                              # list rules + tags
python3 -m pictoji_algebra normalize "(웃 웃) (웃 웃 웃)"
python3 -m pictoji_algebra prove "웃^2 웃^3" "(웃 웃) (웃 웃 웃)"
```

Exit code is nonzero when a canary trips or an assertion fails, so it can be a
CI gate.  A `--disable`/`--enable-only` selector that matches nothing is an
error, not a silent no-op.

Tests:

```bash
python3 -m pytest pictoji_algebra/tests -v     # preferred
python3 run_tests.py                           # fallback when pytest is absent
```


## What it checks

| Statement | Meaning |
|---|---|
| `LHS -> RHS`, `LHS = RHS` | oriented rule |
| `LHS == RHS` | assertion the prover must derive (`[rule]` makes it an axiom instead) |
| `LHS ~> RHS` | assertion that LHS *normalizes* to exactly RHS |
| `LHS != RHS` | **canary**: the prover must NOT derive it |

A tripped canary is a proof of inconsistency, and is automatically
delta-debugged (`ddmin`) to a minimal subset of rules that still derives the bad
equality.  Non-confluence (one term, several normal forms) and non-termination
(a rewrite cycle) are first-class findings rather than crashes.

Three proof outcomes, never two: `PROVED`, `CLOSED` (not derivable with these
axioms), and `EXHAUSTED` (budget ran out - unknown).  Reporting EXHAUSTED as a
disproof would make the tool lie about the one thing it exists to detect.


## Design notes

**Form is substance.**  `Seq` and `Group` are different node types, so
`S S != (S S)` and `(A B) C != A (B C) != A B C` hold by construction, with no
axiom and no way for a rule to erode them.  The single exception is `Add`,
whose operands are stored canonically sorted - v7 states outright that `+` is
associative and commutative, so ordering is not substance there, and
canonicalizing removes a whole class of AC search from the prover.

**Unicode.**  Text is NFC-normalized and segmented by *grapheme cluster*, so
`👩‍🚀` is one token and `❤️` is one token.  The existing analyzer
(`pictoji/cli/__init__.py:225`) iterates per code point and counts them 5 and 2,
contradicting `pictoji.md:4861`; that bug is documented here but not fixed,
since it lives in the shipped package.  Spec files are read `utf-8-sig`, because
every `.md` in the repo carries a BOM.

Superscripts and subscripts are folded to canonical `^n` / `_n` at lex time, so
`웃²` and `웃^2` are one term.  The tables are explicit, not ranges: superscript
1/2/3 are Latin-1 leftovers (U+00B9/B2/B3) and subscript letters are scattered
over three blocks (`ₐ` U+2090, `ᵢ` U+1D62, `ⱼ` U+2C7C).

**Axioms live in markdown**, not in Python, because bisection works over the
markdown rule set - behaviour hidden in Python is invisible to the bisector.
The seven builtins (`builtins.py`) are the genuinely n-ary or arithmetic steps
that cannot be written as patterns; each is still declared in the markdown with
an id and tags, so it can be disabled and bisected like anything else.


## Layout

    graphemes.py   NFC + grapheme cluster segmentation
    lexer.py       graphemes -> tokens, superscript/subscript folding
    terms.py       the term ADT (immutable, hash-cached)
    parser.py      tokens -> terms
    specload.py    markdown -> rules + assertions
    patterns.py    matching, substitution, side conditions
    builtins.py    n-ary / arithmetic rewrite steps
    engine.py      normalizer + bidirectional prover
    diagnose.py    findings, canaries, ddmin bisection
    report.py      human-readable output
    rules.py       rule records, tags, selection


## Not covered yet

- **Amendments A and B.**  They contradict v7 and each other by design, so
  loading them is the next experiment; the tagging scheme makes it a one-flag
  change once the machinery is trusted.
- **`pictoji.md`** (5126 lines).  The loader is file-agnostic; pointing it at
  the big spec is a CLI argument, not a code change.
- **`pictoji-test.md`**, which holds natural-language *decoding* assertions
  (`웃² == people/crowd`) - a different judgement than algebraic equality.
- The `R` relation layer, `ᛠ` classifier inference, and filter semantics get
  parsing and term representation but no reduction rules; v7 calls them
  placeholders.
