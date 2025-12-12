# Pictoji Tests (v0.2.11)

## Smoke tests — literal decoding

1. `👤 ⊸ ↶: ↻⚒` → I have been working
2. `🫵 🞋 ◐¬ ⸮ ☻ ?` → you can do not ask who ?  *(odd but literal; tests negation attach to aux)*
3. `◙ ⌖ ∈ ▣ ☟` → the place in this here
4. `👤 ⇗ ⚭ 👤👤 ↦ ⌖` → I will with we to place
5. `☻ ⟹ ◐ ⸮ □ ?` → who if…then do ask what ?

## Noun pluralization

1. `🐶🐶` → dogs
2. `📖📖` → books
3. `웃²` → people/crowd

## Comparatives & superlatives

1. `▲⬣ ⊳ ▽` → more big than far
2. `▲▲◘` → most small
3. `▼▼⬣` → least big

## Tense / aspect combos

1. `👤 ↶⚒` → I worked
2. `👤 ⊸ ⚒` → I have work *(literal)*
3. `👤 ⊸ ↶: ↻⚒` → I have been working
4. `👤 ↶⇗ ⊸ ↶: ↻⚒` → I would have been working
5. `👤 ↶⭧ ⊸ ↶: ↻⚒` → I should have been working

## Modals & negation

1. `👤 🞋 🤝` → I can help
2. `👤 🞋¬ 🤝` → I cannot help
3. `👤 ↶🞋 🤝` → I could help
4. `👤 ↶🞋¬ 🤝` → I couldn't help
5. `👤 ⇗¬ 🏃` → I will not go
6. `👤 ↶◐¬ ⸮ □ ?` → I did not ask what ?

## Prepositions & compounds

1. `👤 👐 ☉ ∈↦ ⌖` → I give thing into place
2. `👤 ✊ ☉ 🟗↦ ⌖` → I take thing onto place
3. `👤 ⚭∈ ⌖` → I within place
4. `👤 ⚭⁐ ⌖` → I without place

## Questions

1. `📍 ◙ ⌖ ?` → where the place ?
2. `❖ ☉ ◕ ⊳ ◔ ?` → which thing most than some ? *(form test)*
3. `∵ 👤 ◐ ⸮ 🗣 ?` → why I do ask speak ? *(order test)*

Time

1. `↦📅` → today
2. `⏭️📅` → tomorrow
3. `⏮️📅` → yesterday
4. `⏪⏳` → early
5. `⏩⏳` → late

Edge cases / unknowns

1. `👤 [🧪] ⚒` → unknown symbol preserved
2. `👤 ⟹ ⚡ ⤳ 👌` → if…then happen so ok/yes

## Ambiguity guard

1. `📍` → where
2. `⌖` → place
3. `📍 ⊶ ☉` → where of thing

## Being

↻: = being
𑁍 ↻: = sentient being (add 𑁍 = “sentient” to vocab, or pick 🧠 if you prefer)
↻:↻: = beings

## Gerund

↻: ☹ = being sad (add ☹ = “sad”)
↻: ⚒ = being working (literal, by design)

## Passive progressive

: ↻: ↶🧪 = is being tested (add 🧪 = “test”)
↶: ↻: ↶🧪 = was being tested
↻: ↶👀 = being watched
↻: ↶🏗 = being built (add 🏗 = “build”)
↻: ↶❤ = being loved

## Perfect

⊸ ↶: 🙂 = have been happy
↶⊸ ↶: 🙂 = had been happy
👤 ⊸ ↶: ↻⚒ = I have been working
👩 ↶⊸ ↶: ↶❤ = she had been loved

## Future and modals

👤 ⇗ : ↻⚒ = I will be working
👤 ⇗ ⊸ ↶: ↻⚒ = I will have been working
👤 ⭧ ⊸ ↶: ↻⚒ = I should have been working
👤👤👤 ◆ ⊸ ↶: ↻🏃 = they might have been going


## Coverage gaps & suggestions

- Consider an intensifier (e.g., VERY). For now, use repetition (e.g., `⬣⬣`) or leave unmarked.
- Add discourse particles: ALSO, ONLY, EVEN (EVEN exists: `‖`). Propose: `＋` = also; `⊘` = only.
- Consider quotation delimiters for literal names/text.
- Numbers: allow 0–9 as cardinals; suggest `#` as a prefix for ordinals if you later define them.

