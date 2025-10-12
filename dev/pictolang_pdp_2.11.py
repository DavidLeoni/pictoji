"""
Pictolang PDP (Pictolang Decoding Prompt) — v2.11
=================================================

Goal
----
Enable an AI to **decode** Pictolang strings (emoji- and symbol-based) into literal English
glosses, using a small set of deterministic rules. Clarity beats compression.
Never substitute synonyms; always translate literally (📡 = "contact" not "connect").
Word order follows English. Question order remains English and ends with "?".

How to Use
----------
1) Tokenize the input left-to-right, preferring the **longest** valid symbol found at each step.
   (Examples of multi-char symbols: "::", "↶:", "↶⇗", "🟗↦".)
2) Treat spaces as token boundaries when present. Compounds MAY be written *without spaces*.
3) For each token, output its LITERAL English gloss using the map below.
4) Apply composition rules to resolve tense/aspect/modality and simple morphology.
5) DO NOT paraphrase. If a symbol is unknown, keep the raw symbol in the output in [brackets].

Core Composition Rules
----------------------
• **Be / Copula**: ":" = "be" (all finite forms). "::" = plural "be".
  "↶:" = "was"; "↶::" = "were"; "↻:" = "being".
  Progressive is expressed as:  ⊸ ↶: ↻ + VERB  → "have been VERB-ing".
  When progressive is used in finite clauses, attach ↻ to "be", not to the lexical verb.

• **Aux / Negation**: Negation "¬" attaches to the nearest auxiliary/modal to its left.
  Example: "◐¬" = "do not", "↶◐¬" = "did not", "⇗¬" = "will not".

• **Past**: "↶" attaches to the verb or modal it scopes over: "↶⚒" = "worked";
  "↶🞋" = "could".

• **Perfect**: "⊸" = "have". Combine with "↶:" (= been) for perfect progressive forms:
  "⊸ ↶: ↻⚒" → "have been working".

• **Modals**: Map each modal symbol literally; allow stacking in English order:
  [subject] [modal] [neg?] [aux?] [main-verb].

• **Plural nouns**: Duplicate the noun symbol to form plural: "🐶🐶" = "dogs".
  Superscripts can mark hierarchy/scale when defined in the spec (e.g., "웃²" = "people").

• **Comparatives & Superlatives**: "▲ADJ" = "more ADJ", "▼ADJ" = "less ADJ",
  "▲▲ADJ" = "most ADJ", "▼▼ADJ" = "least ADJ"; "⊳" = "than".

• **Quantifiers / Determiners**: Use the literal words given; determiners precede nouns.

• **Questions**: Same English order; prepend wh-symbols as needed and end with "?".

• **Compounds**: Concatenate symbols without spaces to create multi-part concepts
  (e.g., "∈↦" = "into", "⚭∈" = "within").

• **Logic / Connectives**: Use literal mappings for each symbol.

• **Ambiguity rule (place vs where)**: Use "⌖" = "place". Reserve "📍" **only** for "where".

Literal Map (selected, non-exhaustive)
--------------------------------------
Pronouns & Deictics
  🧿 self; 👤 I/me; 👤👤 we/us; 👤👤👤 they/them; 🫵 you; 👨 he/him; 👩 she/her; 🔹 it;
  ▣ this; 👉 that; ☟ here; ☞ there; ☉ thing

Copula & Auxiliaries
  : be; :: be (plural); ↶: was; ↶:: were; ↻: being; ⊸ have; ◐ do
  ◇ maybe; 🧘 still; 〽 already; 🔁 again

Determiners
  ⛉ an; ◙ the; ⛶ any; ⊡ each

Negation / Validation
  ¬ (negation marker, attaches to auxiliary/modal); ◐¬ don't; 🚫 no; 👌 yes/ok;
  ✅ good; ❌ bad

Tense / Aspect
  ↶ (past marker attaches to verb); ⊸ have; ⊸ ↶: ↻VERB have been VERB-ing

Modals
  ◐ do; ◐¬ don't; ↶◐ did; ↶◐¬ didn't
  🞋 can; 🞋¬ cannot; ↶🞋 could; ↶🞋¬ couldn't
  ⇗ will; ⇗¬ won't; ↶⇗ would; ↶⇗¬ wouldn't
  ⭧ shall; ⭧¬ shan't; ↶⭧ should; ↶⭧¬ shouldn't
  ◆ may; ◆¬ may not; ↶◆ might; ↶◆¬ might not
  ⬆️ must; ⬆️¬ must not; ↶⬆️ must (past)

Quantifiers
  ∀ all/every; ∅ none; ∄ doesn't exist; ◔ some; ◳ part; ◕ most; ◫ few;
  ▥ many/several; ▩ much; ⊜ enough; ⚯ too; 🔹🔹 a couple

Logic
  ¬ not; ⊤ true; ⊥ false; = same; ≠ different; ⟹ if…then; ⤳ so/therefore

Relations / Prepositions
  ∈ in; ⁐ out; ⊣ because; ◒ over; ◓ under; ⍟ around; 🟗 on; 🟘 off; ㋣ by;
  ⚮ between; ㊐ for; 🌀 cycle; ⧖ while; ⎋ from; ↦ to/toward; ︴ until; ⊶ of;
  ⚭ with; ㊅ as; @ at; ∻ through; ⟴ across; 🆚 against
  (Compound) ∈↦ into; 🟗↦ onto; ⚭∈ within; ⚭⁐ without

Conjunctions
  ∧ and; ∨ or; ∺ since; 🌓 but; ⌇ though/although

Comparison
  ▲ more; ▼ less; ⊳ than; ▲▲ most; ▼▼ least

Directionals / Links
  ~ about; ↑ up; ↓ down; ← left; → right; ⇢ after; ⇠ before; ➡ way;
  ⇄ other; ‖ even

Time
  ⏳ time; ⏱ now; 🕒 hour; 📅 day; ▓ week; 🗓️ year; 🌃 night; 🌅 morning
  ✴⁰ never; ✴ once; ✴² seldom; ✴³ sometimes; ✴⁴ often; ✴⁵ always
  ⏭️📅 tomorrow; ⏮️📅 yesterday; ↦📅 today
  ⏪⏳ early; ⏩⏳ late; ▲⏪⏳ sooner; ▲⏩⏳ later

Hierarchy (examples)
  웃 person; 웃² people/crowd; 🏘 village; 🏙 city; 🌆 metropolis; 🗺 state/province;
  🇰🇮 country/nation; 🌐 world
  🏢 company; 🏛 institution

Nature & Things (selected)
  ☥ life; 🍴 food/eat; 💧 water; 🔥 fire; ⛰ earth/ground; ☁ sky; ☀ sun; 🌙 moon; ⭐ star
  📖 book; 📄 paper; 📱 phone; 🧩 problem; ⌖ place (use this for “place”)

Verbs (selected)
  ✇ use; 🫳 put/set/place; 🫱 allow/let; 📢 call; 🏷 name; 🏳 begin/start; 🏁 end/finish;
  ⓞ keep/stay; 🤜 move/push; ⚒ work; 🛠 make; 👀 see; 📚 know; 💭 think; 💬 say;
  🗣 speak/tell; ☺ like; ❤ love; ✦ want; ⊞ need; △ try; 🔎 find; 🤏 get; ✊ take;
  👐 give; 🏃 go; 👈 come; ↘ leave; 🤝 help; 📡 contact; 🍴 eat; 🍷 drink; ✺ show;
  ⤞ bring; 📨 send; 📂 open; ⏼ close; ⚡ happen; 💓 feel; ⸮ ask

Questions
  □ what; ☻ who; 📍 where; ⏰ when; ∵ why; ⚙ how; ❖ which; ? end-of-question

Composition Examples
--------------------
1) "👤 ⊸ ↶: ↻⚒" → "I have been working".
2) "☻ ◐¬ ⸮ 👤?" → "Who don't ask me?" (odd but literal).
3) "◙ ⌖ ∈ ▣ ☟" → "the place in this here".
4) "👤 ⇗ ⚭ 👤👤 ↦ ⌖" → "I will with we to place".

Decoding Heuristics
-------------------
• Prefer the longest known token at each step (e.g., parse "↶::" before "↶" + "::").
• For unknown symbols, preserve them as-is inside square brackets.
• Treat duplication of nouns as plural.
• Treat attached modifiers (↶, ¬) as binding to the closest verb/modal to their left.

Additions for Clarity (v2.11 notes)
-----------------------------------
• Introduce "⌖" = "place" (avoid ambiguity with "📍" which is reserved for "where").
• Recommend adding "∃" = "exist / there is/are" for existential statements; keep "∄" as given.
  (If "∃" is absent in a text, use paraphrase via "there [be]" only if the source used it.)
• Digits 0–9 should be read as cardinal numbers. Use "×" for multiplication contexts if present.
• For demonstrative plurals, prefer duplication: "▣▣" = "these"; "👉👉" = "those".

"""

# A minimal token map (non-exhaustive). Literal glosses, **no synonyms**.
TOKEN_MAP = {
    # Pronouns & deictics
    "🧿": "self", "👤": "I/me", "👤👤": "we/us", "👤👤👤": "they/them", "🫵": "you",
    "👨": "he/him", "👩": "she/her", "🔹": "it", "▣": "this", "👉": "that", "☟": "here",
    "☞": "there", "☉": "thing",
    # Copula & auxiliaries
    ":": "be", "::": "be", "↶:": "was", "↶::": "were", "↻:": "being", "⊸": "have", "◐": "do",
    "◇": "maybe", "🧘": "still", "〽": "already", "🔁": "again",
    # Determiners
    "⛉": "an", "◙": "the", "⛶": "any", "⊡": "each",
    # Negation / validation
    "¬": "NEG", "🚫": "no", "👌": "ok/yes", "✅": "good", "❌": "bad",
    # Tense/aspect helpers
    "↶": "PAST",
    # Modals
    "🞋": "can", "⇗": "will", "↶⇗": "would", "⭧": "shall", "↶⭧": "should",
    "◆": "may", "↶◆": "might", "⬆️": "must",
    # Quantifiers
    "∀": "all/every", "∅": "none", "∄": "doesn't exist", "◔": "some", "◳": "part",
    "◕": "most", "◫": "few", "▥": "many/several", "▩": "much", "⊜": "enough", "⚯": "too",
    # Logic
    "⊤": "true", "⊥": "false", "=": "same", "≠": "different", "⟹": "if…then", "⤳": "so",
    # Relations / prepositions
    "∈": "in", "⁐": "out", "⊣": "because", "◒": "over", "◓": "under", "⍟": "around",
    "🟗": "on", "🟘": "off", "㋣": "by", "⚮": "between", "㊐": "for", "⧖": "while",
    "⎋": "from", "↦": "to", "︴": "until", "⊶": "of", "⚭": "with", "㊅": "as", "@": "at",
    "∻": "through", "⟴": "across", "🆚": "against", "∈↦": "into", "🟗↦": "onto",
    "⚭∈": "within", "⚭⁐": "without",
    # Conjunctions
    "∧": "and", "∨": "or", "∺": "since", "🌓": "but", "⌇": "though",
    # Comparison
    "▲": "more", "▼": "less", "⊳": "than", "▲▲": "most", "▼▼": "least",
    # Directionals / links
    "~": "about", "↑": "up", "↓": "down", "←": "left", "→": "right", "⇢": "after",
    "⇠": "before", "➡": "way", "⇄": "other", "‖": "even",
    # Time
    "⏳": "time", "⏱": "now", "🕒": "hour", "📅": "day", "▓": "week", "🗓️": "year",
    "🌃": "night", "🌅": "morning", "✴⁰": "never", "✴": "once", "✴²": "seldom",
    "✴³": "sometimes", "✴⁴": "often", "✴⁵": "always", "⏭️📅": "tomorrow",
    "⏮️📅": "yesterday", "↦📅": "today", "⏪⏳": "early", "⏩⏳": "late",
    # Hierarchy examples
    "웃": "person", "웃²": "people/crowd", "🏘": "village", "🏙": "city", "🌆": "metropolis",
    "🗺": "state/province", "🇰🇮": "country/nation", "🌐": "world", "🏢": "company", "🏛": "institution",
    # Nature & things
    "☥": "life", "🍴": "food/eat", "💧": "water", "🔥": "fire", "⛰": "earth/ground", "☁": "sky",
    "☀": "sun", "🌙": "moon", "⭐": "star", "📖": "book", "📄": "paper", "📱": "phone", "🧩": "problem",
    "⌖": "place",
    # Verbs (selected)
    "✇": "use", "🫳": "put/set/place", "🫱": "allow/let", "📢": "call", "🏷": "name", "🏳": "begin/start",
    "🏁": "end/finish", "ⓞ": "keep/stay", "🤜": "move/push", "⚒": "work", "🛠": "make",
    "👀": "see", "📚": "know", "💭": "think", "💬": "say", "🗣": "speak/tell", "☺": "like", "❤": "love",
    "✦": "want", "⊞": "need", "△": "try", "🔎": "find", "🤏": "get", "✊": "take", "👐": "give",
    "🏃": "go", "👈": "come", "↘": "leave", "🤝": "help", "📡": "contact", "🍷": "drink", "✺": "show",
    "⤞": "bring", "📨": "send", "📂": "open", "⏼": "close", "⚡": "happen", "💓": "feel", "⸮": "ask",
    # Questions
    "□": "what", "☻": "who", "📍": "where", "⏰": "when", "∵": "why", "⚙": "how", "❖": "which", "?": "?",
}

# Optional: A tiny helper to greedily tokenize using known keys (longest-first).
# This is *not* a full decoder—it's a convenience for quick experiments.
def greedy_tokenize(s: str):
    tokens = []
    i = 0
    # Sort keys by length (desc) so we match multi-char symbols first.
    keys = sorted(TOKEN_MAP.keys(), key=len, reverse=True)
    while i < len(s):
        if s[i].isspace():
            i += 1
            continue
        matched = False
        for k in keys:
            if s.startswith(k, i):
                tokens.append(k)
                i += len(k)
                matched = True
                break
        if not matched:
            # Fallback: single character token
            tokens.append(s[i])
            i += 1
    return tokens

def gloss(tokens):
    out = []
    for t in tokens:
        if t in TOKEN_MAP:
            out.append(TOKEN_MAP[t])
        else:
            out.append(f"[{t}]")
    return " ".join(out)

if __name__ == "__main__":
    demo = "👤 ⊸ ↶: ↻⚒"
    toks = greedy_tokenize(demo)
    print(demo, "→", gloss(toks))
