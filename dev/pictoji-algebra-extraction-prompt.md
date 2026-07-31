# Prompt: extracting executable rules from a Pictoji spec

Give this to an AI together with a Pictoji algebra document (a version of
`pictoji_algebra_vN.md`, an amendment, or a chapter of `pictoji.md`).  Its job is
to turn prose laws into statements `dev/pictoji_algebra` can actually run, and to
say plainly which laws it cannot.

The output is a markdown chapter in the format of `dev/pictoji-test-algebra.md`.

---

## Your task

Read the document and produce, for each chapter:

1. **Rules** - the laws the algebra computes with.
2. **Assertions** - the worked examples, as claims the engine must derive.
3. **Canaries** - the distinctions the prose insists on, as `!=`.
4. **A gap list** - laws you could not make executable, and what is missing.

Do not invent laws.  If the prose implies a step it never states, put it in the
gap list rather than writing it as a rule - and say which two sections
disagree.

## Statement grammar

```text
LHS  ->  RHS              oriented rule (reduction)
LHS  =   RHS              oriented rule (law definition)
LHS  ~>  RHS              ASSERTION: LHS must NORMALIZE to exactly RHS
LHS  ==  RHS              ASSERTION: the prover must derive it
LHS  !=  RHS              CANARY: the prover must NOT derive it
LHS  ->  RHS , COND       rule with a side condition
```

Statements are indented four spaces.  Prose is ignored.  A fence with a language
tag (` ```text `) is documentation and is not read.

Directives go in a trailing `# ...` comment:

| directive | meaning |
|---|---|
| `[rule]` | promote an `==` from assertion to bidirectional axiom |
| `[id=name]` | stable id; otherwise `chapter.NN` by position |
| `[tags=a,b]` | extra tags (chapter headings are already tags) |
| `[ladder=name]` | ordered case ladder: first match wins |
| `[expect=fail]` | known not to hold; not reported as a finding |
| `[off]` | do not load |
| `[builtin=name]` | bind to a Python step; see the short list below |

Metavariables: uppercase single letters (`S A B X T E`) are terms, lowercase
`a b n r` are numeric, `c d` are scalars, and `A..` binds a *run* of siblings.
In assertions, letters are ground constants.

## Canaries are the most valuable thing you can write

A spec states what is true.  It rarely states what must *not* be derivable, and
that is exactly what catches an inconsistent axiom set.  Whenever the prose says
two forms "are different", "never collapse", "must not be confused", "is NOT",
or draws a contrast, write a `!=`.

    웃 웃      !=  (웃 웃)
    (웃^2)^3  !=  웃^6

If a canary you wrote turns out to be derivable, that is a real finding, not a
mistake in your transcription.

## Prefer `~>` for worked examples

`~>` asserts a normal form and is one-way, so it catches rules that fire when
they should not.  `(웃) + (웃) ~> (웃) + (웃)` is a genuine test that nothing
collects; the same line written `==` would be vacuously true.

## Traps

These are mistakes already made once.  Check each before you emit.

1. **One relation per line.**  Specs write chains (`A != B != C`); the loader
   rejects them.  Expand by hand - and note that `!=` is not transitive, so a
   three-term chain is *three* pairwise claims, not two.  The first-vs-last pair
   is often the interesting one.

2. **A relation inside a side condition is not the statement's relation.**
   `X / D  (grade(D) ¬= 0)  ->  X ** D^-1` has one relation, `->`.  Rewrite the
   condition into the `, COND` form: `X / D -> X ** D^-1 , grade(D) != 0`.

3. **Round parens are fences, not grouping.**  If the prose uses them for
   association - `웃^2 ** (웃^2 ** 웃^2)` for right-associativity, or
   `(A + B) + C` for associativity of `+` - flag it.  Under the spec's own fence
   rule those forms should not reduce.  Emit both the parenthesized and the
   bare form so the disagreement shows up as a finding.

4. **Structured exponents need parentheses.**  Write `웃^(2 ** 3)` and
   `웃^(1/2)`, never `웃^2 ** 3` or `웃^1/2` - a bare exponent is a single token,
   and `웃^1/2` means `(웃^1)/2`.

5. **Unstated steps.**  v7's Division section computes `S^n / S^n -> S^0` via
   `S^n ** S^-n`, which silently needs `(S^n)^-1 = S^-n` - a step its own
   Replication section forbids.  When a worked example needs a rule that is
   never stated, that belongs in the gap list.

6. **A rule that matches everything is a search bomb.**  `S^1 == S` has an
   unrestricted left side; as a bidirectional axiom it explodes the prover's
   frontier, and oriented it destroys shapes later rules match on.  If a law
   looks like that, say so instead of emitting it.

7. **Superscripts are fine.**  `웃²` and `웃^2` are the same term; keep whatever
   the source used.

## Builtins

Four steps cannot be written as patterns because they are n-ary or arithmetic:
`contract_run` (fenced uniform run to a power), `collect_sum` (coefficient
arithmetic and zero-dropping), `float_tints` (canonical ordering of the
coefficient lane), `angled_eval` (`(> <)` value semantics).  Reference them as
`# [builtin=name] [id=...]` with a one-line description as the statement text.

Everything else should be a pattern rule.  If you think a law needs a fifth
builtin, put it in the gap list and say why - the point of keeping rules in
markdown is that the bisector can name them when a canary trips.

## Ask rather than guess

When a law is ambiguous, stop and ask the owner.  Good questions look like:

- "§Fences says round parens never dissolve, but §Fusion writes
  `웃^2 ** (웃^2 ** 웃^2)` for associativity.  Which reading wins?"
- "Is `S^1` the same term as `S`, or is it `(S)`, a singleton group?"
- "§Division needs `(S^n)^-1 = S^-n`.  Should I add it as a rule, or does
  §Replication's `a ** b` recording forbid it?"

A wrong guess produces a green suite that proves nothing.  An unanswered
question costs one message.

## Output shape

```markdown
## <chapter name from the source>

<one or two lines of prose, only where a statement needs context>

    <rules>

    <assertions>

    <canaries>
```

Then, separately:

```markdown
## Gaps

- <law> - not executable because <reason>.  Needs: <what would make it so>.
- <law> - two sections disagree: <section A> says X, <section B> says Y.
```

Finally, report counts: rules, assertions, canaries, gaps.  If you produced no
canaries, say so explicitly - it almost always means the chapter's distinctions
were not transcribed.
