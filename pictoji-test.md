# ㄕICTO<i>ji</i> TESTS (v0.6.15)


DO NOT PLACE FANCY TYPOGRAPHICS LIKE “” HERE. 

- to test expressions, prefer using ==, ?>, <? over arrows
- if ==, <?, ?> is already part of a pictoji expression, quote the expression.
- If you need to quote, use: " ", ' ', or block quotes """ """, '''  ''' in this preference order.


## Smoke tests - literal decoding

NOTE: these tests have awkward English _on purpose_ to show literal decoding is actually working the way it's intended.  

```
👤 ⊸ ↶⟡ ↻⚒ == I have been working
◙ ⌖ ∈ ▣ ☟ == the place in this here

👤 ⇗ ⚭ 👤👤 ↦ ⌖ == I will with we to place

🫵 🞋 ◐¬ ㉦ ⚇ ? == you can do not ask who ?  *(odd but literal; tests negation attach to aux)*
⚇ ⸮ ◐ ㉦ 山 ? == who if do ask what ?
```

### Noun pluralization

🐶🐶 == dogs
📖📖 == books
웃² == people/crowd

### Comparatives & superlatives

▲⬣ ⊳ ▽ == more big than far
▲▲◘ == most small
▼▼⬣ == least big

### Tense / aspect combos

👤 ↶⚒ == I worked
👤 ⊸ ⚒ == I have work *(literal)*
👤 ⊸ ↶⟡ ↻⚒ == I have been working
👤 ↶⇗ ⊸ ↶⟡ ↻⚒ == I would have been working
👤 ↶⭧ ⊸ ↶⟡ ↻⚒ == I should have been working

### Modals & negation

👤 🞋 ⏢ == I can help
👤 🞋¬ ⏢ == I cannot help
👤 ↶🞋 ⏢ == I could help
👤 ↶🞋¬ ⏢ == I couldn't help
👤 ⇗¬ 🏃 == I will not go
👤 ↶◐¬ ㉦ 山 ? == I did not ask what ?

### Prepositions & compounds

👤 👐 ☉ ∈↦ ⌖ == I give thing into place
👤 ✊ ☉ 🟗↦ ⌖ == I take thing onto place
👤 ⚭∈ ⌖ == I within place
👤 ⚭⁐ ⌖ == I without place

### Questions

📍 ◙ ⌖ ? == where the place ?
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
↻⟡ ↶❤ == being loved

## Perfect

⊸ ↶⟡ 🙂 == have been happy
↶⊸ ↶⟡ 🙂 == had been happy
👤 ⊸ ↶⟡ ↻⚒ == I have been working
👩 ↶⊸ ↶⟡ ↶❤ == she had been loved

## Future and modals

👤 ⇗ ⟡ ↻⚒ == I will be working
👤 ⇗ ⊸ ↶⟡ ↻⚒ == I will have been working
👤 ⭧ ⊸ ↶⟡ ↻⚒ == I should have been working
ƏƏ ◆ ⊸ ↶⟡ ↻🏃 == they might have been going


## Spacing

↦📅 == today
↦ 📅 == to day
🟗↦ == onto
🟗 ↦ ◙ ⌖ == on to the place

### Negation (aux-first)⟡

👤 ⟡¬ ↻⚒. == I am not working.

👩 ↶◐¬ ⚒. == She did not work.

### Articles overt⟡

👤 ↶👀 ⚲ 🐶. == I saw a dog.

👤 ↶👀 ◙ 🐶. == I saw the dog.

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

☞ ⟡ ⚲ 🏠 ? <? is there a house?          # natural_language
∃ 🏠 <-? there exists a house           # formal

### Tense/negation (natural_language only with be)

☞ ↶⟡ ⚲ 🏠 == there was a house
☞ ⟡¬ ⚲ 🏠 == there is not a house

### Formal atemporality with explicit time adjunct
∃ 🏠 ⮊ ⏰ == there exists a house now

### Deictic vs existential "there"
☞ ⮊ ⌖ == there at the place
☞ ⟡ ⮊ ⌖ == there is (something) at the place

### Interrogatives separated by setting
☞ ⟡ ⚲ 🏠 ? == is there a house?
∃ 🏠 ? == does a house exist?

### Quantifier placement
☞ ⟡ ◔ 🏠🏠 == there are some houses
∃ (◔ 🏠) == there exists some house

### Formal negation scope
¬ (∃ 🏠) == there exists no house


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



DO NOT OUTPUT ANYTHING