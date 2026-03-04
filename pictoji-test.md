# ㄕICTO<i>ji</i> TESTS ([PICTOJI.VERSION])


DO NOT PLACE FANCY TYPOGRAPHICS LIKE “” HERE. 

- to test expressions, prefer using ==, ?>, <? over arrows
- if ==, <?, ?> is already part of a pictoji expression, quote the expression.
- If you need to quote, use: " ", ' ', or block quotes """ """, '''  ''' in this preference order.


## Smoke tests - literal decoding

**NOTE:** these tests have awkward English _on purpose_ to test decoding is actually literal as it should be.  

```
▪ ⌖ ∈ ▣ ☟ == the place in this here

👤 ⇗ ⚭ 👤👤 ↦ ⌖ == I will with we to place

우 ◉ ◐¬ ㉦ ⚇ ? == you can do not ask who ?  *(odd but literal; tests negation attach to aux)*
⚇ ⸮ ◐ ㉦ 山 ? == who if do ask what ?
```

### Noun pluralization and types

🐶🐶 == dogs
📖📖 == books
웃² == people/crowd

1 == 1   <!-- 11 == ones ??? TODO REAL BAD 1s == ones ??? SEEMS 1 sec    -->

웃² ⚒ ∈ ▫ 웃³  -> people work in a society
▫ 웃³ ⊶ ↶⚒ 웃² -> a society of working people
우 ∧ 👤⁀ -> you and me
웃³ ⟡ 🛠 ⨯ 👤👤⁀ -> society is made by us

<!-- possibly others
? -> society is made by people   
? -> a person in a society
? -> society is us
? -> a person in a group
? -> our society 
-->


웃웃 == persons
웃^2 == (network of) people
웃² == (network of) people
웃^ == Person
웃웃^ == Persons
(웃^2)^ == People     # type operator ^ applied to query variable


🏠 == house
🏠^ == House
🏠🏠 == houses
🏠🏠^ == Houses
🏠^2 == houses group == village
(🏠^2)^ == Houses


☉[웃^] == object filtered by Person  
☉[웃^]^ == Object filtered by Person  

☉[웃^]^n == object n-ry relation filtered by Person
(☉[웃^]^n)^ == Object n-ry relation filtered by Person


'People' proposals: TODO REVIEW
(웃^)^2 -> People  ??
웃^² -> People   ??
웃^ ⨯ 웃^ -> People  ??



### Cardinalities and autoboxing TODO REVIEW

[setting=formal-story]

    {웃} + {웃} ?s> {웃_i} + {웃_j}   # explicit story mode -> 웃 is assumed singleton, already boxed  
                                     # -> doesn't autobox -> assigns i ¬= j for story mode
               ?k> {웃_i, 웃_j}      # same grade, unionize  
    i ¬== j

[setting=formal-x] ∧ x ¬= story
    {웃} + {웃} ?> 2{웃}    # no story mode -> 웃 is _not_ assumed singleton, explicit {} is kept 
               ?> 2{웃}    # no further rewrites


### Comparatives & superlatives

▲⬣ ⊳ ▽ == more big than far
▲▲᠅ == most small
▼▼⬣ == least big

### Tense / aspect combos

👤 ↶⚒ == I worked
👤 ⊸ ⚒ == I have work *(literal)*
👤 ⊸ ↶⟡ ↻⚒ == I have been working
👤 ↶⇗ ⊸ ↶⟡ ↻⚒ == I would have been working
👤 ↶⬈ ⊸ ↶⟡ ↻⚒ == I should have been working

### Modals & negation

👤 ◉ ⏢ == I can help
👤 ◉¬ ⏢ == I cannot help
👤 ↶◉ ⏢ == I could help
👤 ↶◉¬ ⏢ == I couldn't help
👤 ⇗¬ 🏃 == I will not go
👤 ↶◐¬ ㉦ 山 ? == I did not ask what ?

### Prepositions & compounds

👤 👐 ☉ ∈↦ ⌖ == I give thing into place
👤 ✊ ☉ ◙↦ ⌖ == I take thing onto place
👤 ⚭∈ ⌖ == I within place
👤 ⚭⁐ ⌖ == I without place

### Questions

📍 ▪ ⌖ ? == where the place ?
❖ ☉ ◕ ⊳ ◔ ? == which thing most than some ? *(form test)*
Ϣ 👤 ◐ ㉦ 🗣 ? == why I do ask speak ? *(order test)*

## Time

↦📅 == today
⏭️📅 == tomorrow
⏮️📅 == yesterday
⏪⏳ == early
⏩⏳ == late

## Edge cases / unknowns

👤 [🧪] ⚒  # unknown symbol preserved TODO improve test
⸮ ⚡ ⤳ 👌 == if happens so ok/yes

## Ambiguity guard

📍 == where
⌖ == place
📍 ⊶ ☉ == where of thing

## Being

↻⟡ == being
𑁍 ↻⟡ == sentient being
↻⟡↻⟡ == beings

## Gerund

↻⟡ 🙁 == being sad
↻⟡ ↻⚒ == being working (literal, by design)

## Passive progressive

⟡ ↻⟡ ↶🧪 == is being tested 
↶⟡ ↻⟡ ↶🧪 == was being tested
↻⟡ ↶👀 == being watched
↻⟡ ↶🛠 == being made 
↻⟡ ↶❤️ == being loved

## Perfect

⊸ ↶⟡ 🙂 == have been happy
↶⊸ ↶⟡ 🙂 == had been happy
👤 ⊸ ↶⟡ ↻⚒ == I have been working
👩 ↶⊸ ↶⟡ ↶❤️ == she had been loved

## Future and modals

👤 ⇗ ⟡ ↻⚒ == I will be working
👤 ⇗ ⊸ ↶⟡ ↻⚒ == I will have been working
👤 ⬈ ⊸ ↶⟡ ↻⚒ == I should have been working
ƏƏ ◆ ⊸ ↶⟡ ↻🏃 == they might have been going


## Spacing

↦📅 == today
↦ 📅 == to day
◙↦ == onto
◙ ↦ ▪ ⌖ == on to the place

### Negation (aux-first)⟡

👤 ⟡¬ ↻⚒. == I am not working.

👩 ↶◐¬ ⚒. == She did not work.

### Articles overt⟡

👤 ↶👀 ▫ 🐶. == I saw a dog.
👤 ↶👀 ▪ 🐶. == I saw the dog.

### If (unary/binary)⟡

⸮ 👤 ⚒, 👤 ◐ 🍴. == If I work, I eat.

⸮ 👤 ⟡ ↻⚒, ⇨ 👤 ◐ 🍴. == If I am working, then I eat.

### Since (temporal vs causal) with your chosen split⟡

TODO this stuff is wrong, what's ∺ ?
- Temporal: ⟡ 👤 ⧇ ∺ ⏮️📅.
- Causal  : ⟡ 👤 ⧇ ⊣ ⚡.

### Possessive vs object

- Possessive clitic: 👤⎴ 📖 == my book

TODO don't understand this
- Object pronoun (true object, no ⎴): 👤 ↶👀 👩OBJ. (define the object series explicitly)

## Numbers

0 = zero
7 = seven
42 = forty-two
-3 = minus three

### Decimals (period only; no bare .5)

0.5 = zero point five
2.0 = two point zero
-3.75 = minus three point seven five

### Scientific notation (e inside the number only)

1e3 = one times ten to the three
6.02e23 = six point zero two times ten to the twenty-three
-5e-2 = minus five times ten to the minus two
1.2e-1 = one point two times ten to the minus one

### Coefficients (NL form vs algebraic form)

2 🏠🏠 = two houses
2🏠 = two houses (algebraic form)
2.5 웃웃 = two point five persons
2.5 웃 = two point five persons (algebraic form)
-3 📖📖 = minus three books
-3📖 = minus three books (algebraic form)

### Ordinals

1° = first
2° = second
10° = tenth

### Invalid 

Should be rejected by tokenizer/validator in STRICT mode:

.5 = INVALID (bare decimal; must be 0.5)
1,000 = INVALID (grouping separator not allowed)
1 000 = INVALID (space as thousands separator not allowed)

2e = INVALID (missing exponent digits)
2e+ = INVALID (missing exponent digits)
1.2.3 = INVALID (multiple decimals)
1°° = INVALID (double ordinal)  
2 e3 = INVALID (space inside number)
e3 = INVALID (missing leading digits)

Mixed with attachers/punctuation (number is one token)

☞ ⟡ 1 웃 ?> there is one person
☞ ⟡ 1 웃 <? there is one person
☞ ⟡ 1 웃 <? there is 1e0 person

☞ ↶⟡ 2.5 🏠🏠 ?> there were 2.5 houses
☞ ↶⟡ 2.5 🏠🏠 <? there were 2.5 houses
☞ ↶⟡ 2.5 🏠🏠 <? there were two point five houses

☞ ⟡¬ 10^3 📖📖 ?> there aren’t one thousand books
☞ ⟡¬ 1e3 📖📖 ?> there aren’t one thousand books
☞ ⟡¬ 10^3 📖📖 <? there aren’t one thousand books

6.02e23 ⚛⚛ ?> Avogadro constant atoms
6.02e23 ◈ ⚛⚛ ?> Avogadro constant atoms
6.02e23 ⚛⚛ <? Avogadro constant atoms


✊ 10^9 🐶🐶 ?> Take one billion dogs
✊ 10^9 🐶🐶 <? Take 1 000 000 000 dogs  
✊ 10^9 🐶🐶 <? Take one billion dogs 
✊ 10^9 🐶🐶 <? Take 1,000,000,000 dogs

✊ 5e18 ☉☉ == Take 5e18 things  
✊ 5e18 ☉☉ <? Take 5*10^18 things  

## There is / exists

### Setting-gated defaults

☞ ⟡ ▫ 🏠 ? <? is there a house?          # natural_language
∃ 🏠 <-? there exists a house           # formal

### Tense/negation (natural_language only with be)

☞ ↶⟡ ▫ 🏠 == there was a house
☞ ⟡¬ ▫ 🏠 == there is not a house

### Formal atemporality with explicit time adjunct
∃ 🏠 ➲ ⏰ == there exists a house now

### Deictic vs existential "there"
☞ ➲ ⌖ == there at the place
☞ ⟡ ➲ ⌖ == there is (something) at the place

### Interrogatives separated by setting
☞ ⟡ ▫ 🏠 ? == is there a house?
∃ 🏠 ? == does a house exist?

### Quantifier placement
☞ ⟡ ◔ 🏠🏠 == there are some houses
∃ (◔ 🏠) == there exists some house

### Formal negation scope
¬ (∃ 🏠) == there exists no house


## Types

## Unknowns and errors

Materialized runtime types:

(ↂ^[Bool])^ ¬= (ↂ^[Int])^


## Suspensions tests

⏸(⏸(x)) ?> ⏸(⏸(x))    # no idempotency
⏸(1 / 0) ?> ⏸(1 / 0)
⏸(ↂ) ?> ⏸(ↂ)
⏸(ↂ^2) ?> ⏸(ↂ^2)


▶(▶(x)) ?> ▶(▶(x))    # no idempotency
▶(⏸(🏠)) ?> 🏠
▶(⏸(⏸(🏠))) ?> ⏸(🏠)
▶(🏠) ?> ↂ[🏠]^1
▶(🏠^2) ?> ↂ[🏠]^2 
▶(ↂ) ?> ↂ
▶(ↂ^2) ?> ↂ^2


Put them here as given the specs they MUST be redundant 

⏸(◇) ?> ⏸(◇)          
⏸(◇[T]) ?>  ⏸(◇[T])       


⏸(🖥ↂ^k) , k < Ϟ  ?> ⏸(🖥ↂ^k)      
⏸(ↂ^k) ,   k < Ϟ  ?> ⏸(ↂ^k)

▶(⏸(◇)) ?> ◇

▶(🖥ↂ^k)     , k < Ϟ ?> 🖥ↂ^k
▶(ↂ^k)       , k < Ϟ ?> ↂ^k
▶(⏸(🖥ↂ^k)) , k < Ϟ ?> 🖥ↂ^k       
▶(⏸(ↂ^k))   , k < Ϟ ?> ↂ^k       

▶(🖥ↂ^k)     , k >= Ϟ ?> 🖥ↂ^k    
▶(ↂ^k)       , k >= Ϟ ?> ↂ^k       
▶(⏸(🖥ↂ^k)) , k >= Ϟ ?> 🖥ↂ^k     
▶(⏸(ↂ^k))   , k >= Ϟ ?> ↂ^k       



## Famous phrases

👤 💭, ⤳ 👤 ⟡. == I think, therefore I am.

Natural language: literal difference matters (i.e. no / not):

    山^ ↶⟡, ⇗ ⟡. 山^ ⟡, ⇗ ⟡ 🚫 ⧁. == What was, will be. What is, will be no more. 
    -- Vigo the Carpathian


👤^ ⊸^ ▫ 😴💭^ == I Have a Dream        # the original, note unnecessary extra-caret emphasis on 👤^ 
👤 ⊸ ▫ 😴💭 == I have a dream 
👤👤, ▪ 웃²     == we, the people
👤👤^, ▪ 웃²^   == We, the People    

↦ ⟡, ∨ ¬ ↦ ⟡, 👉 ⟡ ▪ ㉦⧐ == to be, or not to be, that is the question

㉦ ¬ 山 우⎴ 🏠⁶ ◉ ◐ ㊐ 우 - ㉦ 山 우 ◉ ◐ ㊐ 우⎴ 🏠⁶ == ask not what your country can do for you - ask what you can do for your country

#### without capitalization:

I have a dream
we, the people
to be, or not to be, that is the question
ask not what your country can do for you - ask what you can do for your country

👤 ⊸ ▫ 😴💭   
👤👤, ▪ 웃²     
↦ ⟡, ∨ ¬ ↦ ⟡, 👉 ⟡ ▪ ㉦⧐
㉦ ¬ 山 우⎴ 🏠⁶ ◉ ◐ ㊐ 우 - ㉦ 山 우 ◉ ◐ ㊐ 우⎴ 🏠⁶


With labels, without capitalization:

MLK:I have a dream
US:we, the people
Sh:to be, or not to be, that is the question
JFK:ask not what your country can do for you - ask what you can do for your country


MLK:👤 ⊸ ▫ 😴💭 
US:👤👤, ▪ 웃² 
Sh:↦ ⟡, ∨ ¬ ↦ ⟡, 👉 ⟡ ▪ ㉦⧐ 
JFK:㉦ ¬ 山 우⎴ 🏠⁶ ◉ ◐ ㊐ 우 - ㉦ 山 우 ◉ ◐ ㊐ 우⎴ 🏠⁶


A B C DE
AA, F G²
H I, J K H I, L I F MN
M K O PQ R⁶ S T U P - M O P S T U PQ R⁶


#### With capitalization:

I Have a Dream
We, the People
To be, or not to be, that is the question
Ask not what your country can do for you - ask what you can do for your country

👤 ⊸^ ▫ 😴💭^   
👤👤^, ▪ 웃²^     
↦^ ⟡, ∨ ¬ ↦ ⟡, 👉 ⟡ ▪ ㉦⧐
㉦^ ¬ 山 우⎴ 🏠⁶ ◉ ◐ ㊐ 우 - ㉦ 山 우 ◉ ◐ ㊐ 우⎴ 🏠⁶

A B^ C DE^
AA^, F G²^
H^ I, J K H I, L I F MN
M^ K O PQ R⁶ S T U P - M O P S T U PQ R⁶

With labels and capitalization:

MLK:👤 ⊸^ ▫ 😴💭^ 
US:👤👤^, ▪ 웃²^ 
Sh:↦^ ⟡ ∨ ¬ ↦ ⟡, 👉 ⟡ ▪ ㉦⧐ 
JFK:㉦^ ¬ 山 우⎴ 🏠⁶ ◉ ◐ ㊐ 우 - ㉦ 山 우 ◉ ◐ ㊐ 우⎴ 🏠⁶



## Open interpretation

🟠⧏ = ?


## Pictoji in pictoji

The ultimate test (aspirational!!!)

∀ AI_i, AI_j ∈ SUPPORTED_AIS:
    emojis = encode(pictoji_specs_english | AI_i)
    deng = decode(emojis | AI_j)
    ∆𐒄(pictoji_specs_english, deng) ≤? ε(setting=formal)

DO NOT OUTPUT ANYTHING