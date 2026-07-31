# Pictoji Algebra v7 core - executable

Executable transcription of `pictoji_algebra_v7.md`, **core layer only**.
Amendments A and B are deliberately NOT loaded: they contradict v7 and each
other, and mixing layers before the machinery is trusted would confuse a
tooling bug with an algebra bug.  They are the next experiment, not this one.

Read by `dev/pictoji_algebra`.  Statement forms:

```text
LHS  ->  RHS              oriented rule (reduction)
LHS  =   RHS              oriented rule (law definition)
LHS  ~>  RHS              ASSERTION: LHS must NORMALIZE to exactly RHS
LHS  ==  RHS              ASSERTION: the prover must derive it
LHS  !=  RHS              CANARY: the prover must NOT derive it
LHS  ->  RHS , COND       rule with a side condition
```

`# ...` is a comment.  Directives inside it: `[rule]` promotes an `==` to a
bidirectional axiom, `[builtin=name]` binds an n-ary or arithmetic step,
`[equiv]` lets a builtin run backwards, `[ladder=name]` marks an ordered case
ladder (first match wins), `[id=]`/`[tags=]` name things, `[off]` disables.

Rules inherit tags from their headings, so `--disable fusion` works unannotated.

Uppercase single letters (`S A B X T E`) are term metavariables in rules;
lowercase `a b n r` are numeric ones and `c d` are scalars.  In assertions they
are ground constants - testing a universally quantified law on a generic
instance.

`~>` and `==` are different obligations.  `~>` is one-way and structural, so it
catches rules that fire when they should not; `(웃) + (웃) ~> (웃) + (웃)` is a
real test that nothing collects, where the same line as `==` would be vacuous.

**This file is expected to fail.**  v7's own closing section admits no machine
check of termination or confluence has ever been run.  The failures are the
output, not a defect in the run.


## Sequences

Juxtaposition is the hierarchy constructor: n-ary, ordered, non-associative.
Non-associativity is structural in the interpreter (`Seq` and `Group` are
different node types), so it needs no axiom - these check that the
representation really does refuse to conflate them.

    웃 (웃 웃)  !=  (웃 웃) 웃
    (웃 웃) 웃  !=  웃 웃 웃
    웃 (웃 웃)  !=  웃 웃 웃
    (A B) C    !=  A (B C)
    A (B C)    !=  A B C
    (A B) C    !=  A B C

Addition is associative and commutative.

    (🌳 + 웃) + 🐶  ==  🌳 + (웃 + 🐶)   # [expect=fail]
    🐶 + 🏠         ==  🏠 + 🐶

Distribution and factoring are free `==` moves, usable in both directions.

    A.. (B + C)  ==  A.. B + A.. C            # [rule] [id=seq.factor]
    A.. (B + 1)  ==  A.. B + A..              # [rule] [id=seq.factor-unit]

    🌳 웃 🐶 + 🌳 웃 🏠  ==  🌳 웃 (🐶 + 🏠)
    🌳 웃 🐶 + 🌳 웃 🐶  ==  2 🌳 웃 🐶
    🌳 웃 🐶 + 🌳 웃     ==  🌳 웃 (🐶 + 1)

Inverse reverses sequences (the matrix law).

    (A B)^-1  ==  B^-1 A^-1                   # [rule] [id=seq.inverse]

    (🌳 🏠)^-1  ==  🏠^-1 🌳^-1


## Reduction strategy

Eager reduction, fenced by round parens.  A *fenced* uniform run contracts to
power form; a bare run does not, which is the entire point of the notation.

    uniform fenced run contracts to a power   # [builtin=contract_run] [id=red.contract]

There is deliberately no global `S^1 -> S`.  Oriented, it rewrites
`웃^1 ** 웃^-1` to `웃 ** 웃^-1` before the fusion ladder can see it and
annihilation never fires; bidirectional, its left side matches every term and
the prover's frontier explodes.  Exponent-1 collapse belongs to `(> <)` value
semantics, where v7 actually uses it.

    (웃 웃)             ~>  웃^2
    (웃 웃) (웃 웃 웃)   ~>  웃^2 웃^3
    웃 웃 (웃 웃 웃)     ~>  웃 웃 웃^3

Addition is eager; coefficients collect and unfenced zero terms drop.

    sum collection and zero-term dropping     # [builtin=collect_sum] [id=red.collect]

    웃 + 웃 + 웃        ~>  3웃
    웃 + 0웃            ~>  웃

Fenced forms are preserved.  Each is an instance of the one fence principle:
the fenced object does not participate in exterior patterns.

    (웃) + (웃)         ~>  (웃) + (웃)
    웃 + (0웃)          ~>  웃 + (0웃)
    웃 + (웃 + 웃)      ~>  웃 + (2웃)

Typed ones float into a sorted coefficient prefix, then absorb into the first
element of matching type - scanning past foreign symbols, so that floating and
absorbing commute and there is a single normal form.

    typed ones float left and sort            # [builtin=float_tints] [id=red.float]
    X^0 A.. X B..  ->  A.. X B..              # [id=red.absorb]

    웃^0 웃            ~>  웃
    🌳 웃^0 웃         ~>  🌳 웃
    웃 🫀^0            ~>  🫀^0 웃
    🫀^0 웃            ~>  🫀^0 웃


## Grouping and powers

`^n` is the contracted display of a reified uniform run - a definition, not a
computation.

    웃^2      ==  (웃 웃)
    웃^3      ==  (웃 웃 웃)
    웃^4      ==  (웃 웃 웃 웃)
    웃^2 웃^3  ==  (웃 웃) (웃 웃 웃)
    웃 웃^2 웃  ==  웃 (웃 웃) 웃

The canaries: contraction must never cross the fence boundary.

    웃 웃      !=  (웃 웃)
    웃^3      !=  웃 웃 웃
    웃 웃^2 웃  !=  웃 웃 웃 웃


## Replication

Replication records itself as a non-commutative `**` in the exponent; it is
never an exponent product.

    (X^a)^b  ==  X^(a ** b)                   # [rule] [id=rep.record]

    (웃^2)^3       ==  웃^(2 ** 3)
    (웃^2)^3       !=  웃^6
    웃^(2 ++ 1)    !=  웃^(1 ++ 2)


## Fusion

`**` is the one nonlinear operator and must be invoked explicitly.  It is a
*recognizer*: it computes on structurally recognizable pairs and holds
everything else.  The cases below are a ladder checked in order - once one
fires, the rest must not.

    S^a ** S^b  ->  S^b            , a == 0                             # [ladder=fusion] [id=fus.1-left-zero]
    S^a ** S^b  ->  S^a            , b == 0                             # [ladder=fusion] [id=fus.2-right-zero]
    S^a ** S^b  ->  (> S^a S^b <)  , abs(a) < 1 and abs(b) < 1           # [ladder=fusion] [id=fus.3-subunit]
    S^a ** S^b  ->  S^0            , a == -b                            # [ladder=fusion] [id=fus.4-annihilate]
    S^a ** S^b  ->  S^(a + 1)      , a == b and is_int(a) and a > 0      # [ladder=fusion] [id=fus.5-succ-up]
    S^a ** S^b  ->  S^(a - 1)      , a == b and is_int(a) and a < 0      # [ladder=fusion] [id=fus.6-succ-down]
    S^a ** S^b  ->  S^a S^b                                             # [ladder=fusion] [id=fus.7-held]

Upward ladder:

    웃^2 ** 웃^2   ==  웃^3
    웃^3 ** 웃^3   ==  웃^4
    웃^2 ** 웃^3   ==  웃^2 웃^3

Downward ladder - the same formula, with the sign folding the cones:

    웃^-1 ** 웃^-1  ==  웃^-2
    웃^-2 ** 웃^-2  ==  웃^-3
    웃^-2 ** 웃^-3  ==  웃^-2 웃^-3

Annihilation lands on the typed one, never on bare zero:

    웃^1 ** 웃^-1   ==  웃^0
    웃^2 ** 웃^-2   ==  웃^0
    웃^2 ** 웃^-3   ==  웃^2 웃^-3

Absorption is same-symbol only, and symmetric.

    웃^0 ** 웃^2    ==  웃^2
    웃^2 ** 웃^0    ==  웃^2
    웃^0 ** 웃^0    ==  웃^0

Both operands sub-unit: fusion is LINEAR there, routing to `(> <)`.  The
fractional cases agree with annihilation where they overlap - the sub-unit case
fires first and the linear sum lands on the same typed one.

    웃^(1/2) ** 웃^(1/2)    ==  웃
    웃^(1/4) ** 웃^(1/4)    ==  웃^(1/2)
    웃^(1/2) ** 웃^(-1/2)   ==  웃^0

Mixed sub-unit and large operands do NOT linearize - no case matches, so the
pair is held as a calculation artifact.

    웃^(1/2) ** 웃^3        ==  웃^(1/2) 웃^3

`**` is binary and right-headed, so chains parenthesize from the right.

    웃^2 ** 웃^2 ** 웃^2    ==  웃^2 웃^3

v7 line 335 writes that same chain as `웃^2 ** (웃^2 ** 웃^2)`, using round
parens for associativity.  But v7's Fences section declares round parens to be
structural fences that block the fenced object from exterior patterns - so on
v7's own terms the parenthesized form should NOT reduce.  Both are asserted
here; if they disagree, the notation is overloaded.

    웃^2 ** (웃^2 ** 웃^2)  ==  웃^2 웃^3   # [expect=fail]


## Division

`/` dispatches on the divisor.  A live divisor is sugar for an explicit fusion;
a typed-one divisor is removal, which is a different operation entirely.

    X / D  ->  X ** D^-1  , grade(D) != 0     # [id=div.live]

v7's worked division examples (`S^n / S^n -> S^n ** S^-n -> S^0`) need one more
step that the Division section never states: the inverse of a power is the
power of the negated exponent.  Without it, `웃^2 / 웃^2` gets stuck at
`웃^2 ** (웃^2)^-1` and the fusion ladder cannot recognize the pair.

Written unfenced, because that is the shape substitution actually produces:
`X ** D^-1` with `D = 웃^2` yields the caret chain `웃^2^-1`, not the fenced
`(웃^2)^-1`.  The distinction is exactly the fence principle doing its job.

    S^n^-1  ->  S^-n                          # [id=div.power-inverse]

This rule is in tension with Replication, which says outer exponents never
multiply through but record as `a ** b`.  `rep.record` gives
`(웃^2)^-1 == 웃^(2 ** -1)`; `div.power-inverse` gives `웃^-2`.  Both are
loaded on purpose - the canary below is what decides whether that is fatal.

    웃^2 / 웃^2   ==  웃^0
    웃^2 / 웃^3   ==  웃^2 웃^-3
    (웃^2)^-1    !=  웃^(2 ** 3)

Removal is partial: it holds when the tint is absent, and fires the moment a
matching tint appears.

    T^0 (X / T^0)  ->  X                      # [id=div.removal-fires]
    X / T^0 / T^0  ==  X / T^0                # [rule] [id=div.removal-idempotent]

    🫀^0 (웃 / 🫀^0)     ==  웃
    웃 / 🫀^0 / 🫀^0     ==  웃 / 🫀^0
    웃 / 🫀^0            ~>  웃 / 🫀^0

Removal is injective: the held form is a distinct term from the fired one, and
the tool must never fabricate a result for an absent tint.

    웃 / 🫀^0            !=  웃


## Angled parens

Inside `(> <)` the operands are intermediate calculations and their meaning is
not considered: form semantics switch to value semantics, and contiguous
same-symbol runs sum.  Order across symbols is still respected.

    contiguous same-symbol runs sum           # [builtin=angled_eval] [id=ang.eval]

    (> 웃^2 웃^3 <)              ==  웃^5
    (> 웃^2 웃^3 웃^-1 <)        ==  웃^4
    (> (웃 웃) (웃 웃 웃) <)      ==  웃^5
    (> 🏠^3 🏠^2 웃 웃^6 <)      ==  🏠^5 웃^7
    (> 웃 🏠^2 웃^6 🏠^3 <)      ~>  웃 🏠^2 웃^6 🏠^3

Fractional exponents are the natural home of `(> <)`.

    (> 웃^(1/2) 웃^(1/2) <)      ==  웃
    (> 웃^(1/4) 웃^(1/4) <)      ==  웃^(1/2)
    (> 웃^(1/2) 웃^(-1/2) <)     ==  웃^0
