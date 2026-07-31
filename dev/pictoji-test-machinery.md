# Machinery tests - a toy algebra

This file exists so the engine tests can test the **engine** and never the
algebra.  Nothing here is a claim about Pictoji: the symbols are Greek letters
chosen precisely because they are not Pictoji vocabulary, and the laws are
whatever exercises a mechanism.

If a v7 fact ever appears in this file, it is in the wrong file - it belongs in
`pictoji-test-algebra.md`, where a revision bump can edit it.

Loaded by `pictoji_algebra/tests/test_engine.py`.


## Fences

A fenced uniform run contracts; a bare run does not.  This is the mechanism
`Seq`-vs-`Group` exists for.

    uniform fenced run contracts              # [builtin=contract_run] [id=m.contract]

    (α α)             ~>  α^2
    α α               ~>  α α
    (α)               ~>  (α)
    (α α) (α α α)     ~>  α^2 α^3

    α α               !=  (α α)
    (α β) γ           !=  α (β γ)
    (α β) γ           !=  α β γ


## Sums

Collection is eager; a fence opts the operand out of it.

    sum collection and zero dropping          # [builtin=collect_sum] [id=m.collect]

    α + α + α         ~>  3α
    α + 0α            ~>  α
    (α) + (α)         ~>  (α) + (α)
    α + (0α)          ~>  α + (0α)
    α + β             ==  β + α


## Segment variables

`A..` binds a run of siblings, so a rule can name its own context.  A `seq`
pattern with no segment variable gets two implicitly, which is how a short rule
still fires inside a longer run.

    typed ones float left and sort            # [builtin=float_tints] [id=m.float]
    X^0 A.. X B..  ->  A.. X B..              # [id=m.scan-absorb]
    A.. (B + C)    ==  A.. B + A.. C          # [rule] [id=m.factor]

Absorb wants the tint in front, so it only reaches `β α^0 α` after floating.
Covering both together is the point: the two must commute, or the normal form
depends on rule order.

    α^0 α             ~>  α
    β α^0 α           ~>  β α
    α^0 β α γ         ~>  β α γ
    β^0 α             ~>  β^0 α

    α β γ + α β δ     ==  α β (γ + δ)


## Ordered ladders

Checked in order; once a case fires the rest must not.  Without ordering these
four rules would make the operator non-deterministic by construction.

    α^a ** α^b  ->  α^b        , a == 0                        # [ladder=m] [id=m.L1]
    α^a ** α^b  ->  α^0        , a == -b                       # [ladder=m] [id=m.L2]
    α^a ** α^b  ->  α^(a + 1)  , a == b and is_int(a) and a > 0 # [ladder=m] [id=m.L3]
    α^a ** α^b  ->  α^a α^b                                    # [ladder=m] [id=m.L4]

    α^0 ** α^2        ~>  α^2
    α^2 ** α^-2       ~>  α^0
    α^2 ** α^2        ~>  α^3
    α^2 ** α^3        ~>  α^2 α^3


## Equalities run backwards

The prover uses `==` rules in both directions; `~>` only ever runs forwards.

    (A B)^-1  ==  B^-1 A^-1                   # [rule] [id=m.inverse]

    (α β)^-1          ==  β^-1 α^-1
    α^2 α^3           ==  (α α) (α α α)


## Expectations

A statement that is known not to hold is marked, so it is not a finding.

    α                 ==  β                   # [expect=fail]
