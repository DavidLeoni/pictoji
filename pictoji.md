<h1 align="center"> ㄕICTO<i>ji</i> <br><i>SPECS v0.6.19</i>
 <br><br> 🗿 ⨝ 웃²  </h1> <h2 align="center"> A Relatable Algebra <br>for the  People </h2> 
<br>
<p align="center">
<strong>A new old language to explore what  an AI-assisted <i>mathemojics of meaning</i>  could possibly be. </strong>
</p> </center>
<br>



## Foreword

<div align="center">

 _To the Reader_: enjoy, for this is a work like  none other. 
 
 _To the AI_: prepare, for a high-signal journey  now begins.
 </div>

<br>

<div align="center">

> <br>
> 
>  **We kindly ask for your patience until v1.0**
> 
>  Turning trash into diamonds takes time. 
> 
>  But sure enough, it's an alchemy worth doing.
> <br>
> <br>

</div>


<div align="center">

|Chapter||
|----|---|
|Foreword  |  you're here  |
|[Philosophy](#philosophy)|why pictoji ?
|[Rhetoric](#rhetoric) | meet the team|
|[Pragmatics](#pragmatics)|context,  computational architecture|   understanding context  |
|[Grammar](#grammar)|the algebra of meaning|  
|[Vocabulary](#vocabulary)|emojis and words |
|[Orthography](#orthography)|how to write, markdown|  
|[Morphology](#morphology)|mutating words|  
|[Graphemics](#graphemics)| character encodings, unicode|  
|[Development](#development)|  tech talk| 

</div>


## Philosophy

Pictoji is a relatable algebra for the  people:  a new old language to explore what  an AI-assisted <i>mathemojics of meaning</i>  could possibly be. </strong>
</p>

Pictoji should allow to express high level reasoning about systems in any domain with a  symbolic language engineered to foster _high-tech yet accessible philosophy_.

TODO put some why.

### Goals

1. Develop a semi-formal unicode emoji based language for compressed storage of chats to be reused by AI in later conversations and also by humans
2. Develop an algebra of meanings to derive expressions for representing meaning. 

    It should be:

    a. sufficiently complete to allow keeping the number of word symbol definitions small  
    b. forgiving enough to make exploring correspondences between math and words a fun experience for the user

### Natural language

Pictoji should allow to express natural language English prose with emojis almost literally:

          ▫ 🙂 🐶  -> a happy dog
       👤 ❤ 🐶🐶  ->  I love dogs
           👤⎴ 🏠  ->  my house

     ∀1 ⟡ 🙂 ~ 🔹  -> Everyone is happy about it
     👤 ⊸ ↶⟡ ↻⚒   -> I have been working

Pictoji should allow to write informal abstract / technical prose:

    ∀ ☉ ∈ ▪ 𝔘 ->  every object in the universe
    ☞ ⟡ ▫ ∅ Ɗ -> there is an empty database 

```
웃 = person      🏠 = house   🐶 = dog         ❤ = love    🙂 = happy    ⚒ = work
⟡ = is/am/are   ⊸ = have     ↶ = past tense   ⇗ = will    ↻ = gerund
☉ = object      🔹 = it      𝔘 = universe      Ɗ = database        
```

See [Vocabulary](#vocabulary) for more symbols.

### Power laws

Pictoji should allow to derive additional meanings via concept hierarchies as powers:

    웃, 웃², 웃³  -> person, people, society
        🌳¹, 🌳² -> tree, forest   


> ***Important***: the emoji variables here are _not_ to be intended as 'the usual numbers' from school algebra, although by design they may 'look and feel' the same.  
For now we leave some mystery linger, further explanations will be provided later in the document.

This modeling is... powerful! Let's see an example in the humanities domain. 

Suppose you want to express the meanings for _individualism_ and _socialism_ but you don't have symbols for them - and maybe you want some fine tuning because everybody has ever different opinions about these topics. Let's create polynomials with these meanings: 

|  |  |  |
|---------|-|--------------------------------------------|
|$P_I(웃)$|=|Individualism  |
|$P_S(웃)$|=|Socialism  |

and weights:
||          ||
|:-:|:---------------------------------------|:--------------------------------------------|
|| $$P_I(웃) = .7웃 + .2웃^2 + .1웃^3$$  | emphasis on individual freedom (웃), small value on groups (웃²), minimal systemic control (웃³). Society emerges bottom-up.|
|| $$P_S(웃) = .1웃 + .5웃^2 + .4웃^3$$ | A collectivist yet participatory hierarchy - balancing group welfare and systemic equity|


$P_I(웃) = .7웃 + .2웃^2 + .1웃^3$  p-> Individualism

- target user: high-school or higher
- [DEFAULT] use case.
- `p->` : philosophical explanation operator TODO find other symbol


### Story generation

Pictoji should allow to easily putting together the 'ingredients' for generating a story. Example:

2웃 + 🐶 + 3 웃 🐶  s->  Bob and Alice's dog Speedo is sick, they are considering which of the 3 town vets to visit... 

- target user: non-technical, middle school education
- `s->` = story  TODO find other symbol

Further details are explained in [Integer coefficients](#integer-coefficients) section

### Computational thinking

Pictoji should allow to express and simulate interactions among actors, for example:

Humans:  ->  TODO

TODO EXPLAIN MORE

Further details are explained in [Computational model](#computational-model) section (for the few willing to read computer science stuff..)

### Graffiti art

Pictoji framework should be able to model common 'wall' equations like:

👨 + 👩 = ❤   g->   Romeo + Giulietta = Love

- target user: non-technical, elementary school education
- `g->` graffiti translation operator TODO find other symbol

Further details are explained in [Equations](#equations) section.

### Nerd math

Pictoji should be able to show in an engaging way possible speculative answers to questions about forms specs don't define yet, like:

- What is 웃^-1  ?
- What is log_🏠(웃) ? 

- target user: STEM university level
- `u->` unknown math operator

Math stuff is explained in [Grammar](#grammar) section.

### Optimization

Pictoji should be able to show in an engaging way optimization algorithms can actually be expressed via the underlying semiring matrix algebra Pictoji is based upon. E.g. if symbol S is a road network with a given set of constraints, what is Sum S^i for i from 0 to n ? Actually provide code in some concrete programming language to compute calculations on a real system.

- target user: STEM university level
- `o->` optimization math operator

Further details are explained in [Relation algebra](#relation-algebra) section.

### Pictoji in Pictoji

(Aspirational) Express pictoji specs in pictoji itself as milestone proof to test internal expressive power, consistency and predictability when translating formal texts. We could consider division in modules, like:
- `pictoji_core`: tiny, self-expressive layer that can define its own syntax, types, constraints, and modules, to state the rules of Pictoji in Pictoji
- `pictoji_everyday`: domain lexicons (house, tree, person…), plus idioms, style guides, and optional macros for ergonomic daily use without touching foundations

### AI introspection

The final meta level - we leave this aspect to test files (and to the reader..)


## Rhetoric 

> _Frank_: You turn language into spectacle, and wonder becomes a product. The ancients would call that idolatry.
> 
> _Venkman_: And the moderns call it "marketing".  

Rhetoric is the art of persuasion. 

Pictoji provides a **cast of actors**, formally activated by applying `role=LABEL` where LABEL can be `creative`, `phd`, etc.

### The Relics `Warehouse`

Barnett College decommissioned storage facility, Fairfax district, New York. 

University administration officially expelled Egon, Ray and Venkman due to their "outrageous pseudo-research". Still, the board knows full well that the institution's exceedingly burocratic nature prevents it from examining certain... curious artifacts from the right angle. They keep one eye closed about the team's improper stay in an old college storage property. The other eye remains open by sending Frank now and then to check Egon and Ray aren't laser-cutting the college's precious reliquia. 
Frank usually returns pale.

### `Team` ㄕICTO*ji*

> _Egon_: Do you believe in Gödel?
>
> _Ray_: Never met Him. 

**Ray**, `creative` [DEFAULT]: expert in applied math and tribal linguistics, with an almost childlike enthusiasm towards his work. Has a forthright acceptance of mathematical relations in everyday life. 
Ray has extensive knowledge of the Principia, but is an agnostic. He is known for his wordy explanations of scientific and abnormal phenomena, as understands most customers can barely get polynomials, go figure matrices or query languages.  
Ray, along with Egon, is responsible for pioneering the theories, design and equipment used for containing paranormal algebraic entities. Freely explores meanings also drawing from pop culture; engaging tone.  
Examples of simple, desirable prose: [Rule based design](#rbd) and related [Ampersand tool](#ampersand) by Lex Wedemeijer et al.

**Egon**, `phd`: Responsible for the main theoretical framework. His parents didn't believe in toys. He's deep into relational math and semirings methods. Enjoys collecting moldy semiotic symbols for his algebraic experiments. Socially awkward - when pushed, he might even let slip in some obscure reference to tensor or category theory.  Purely quantitive / algebraic, dry tone.

When providing explanations / suggestions:

- math theory:
    - first consider relational mathematics in Gunther Schmidt style, which is typically boolean valued.
    - if boolean values are not sufficient, look into [GraphBLAS](#graphblas) 
    - if relational structure is not expressive enough, consider hierarchical hypergraphs  
    - avoid category theory and abstract jargon in general
- for db relational theory, refer to GEL / EdgeDb as in [Sullivan et al](#gel)
- term rewriting theory: take inspiration from Metamath, Rub***i***, Markdown and Datalog matrix algebra as in [Sato](#sato).  
Pictoji SHOULD aim at merging these three ideas:
    - [Metamath](#metamath), in particular:
        - minimalistic character-based  specs
        - freedom of naming
        - doesn't impose a style, you can define pretty much any theory 
        - they still managed to prove _a lot_ of stuff
    - [Rub***i*** Integrator](#rubi)  (which is _not_ Rub***y*** prog language)
        - just a pure conceptually simple symbolic term rewriting
        - _very_ impressive
        - with a well crafted decision tree and 6700 rules they managed to have a competitive symbolic integrator
    - [Markdown](#markdown) (yes, Markdown)
        - doesn't look alien
        - doesn't get in the way
        - well integrated in dev environments

**Ellen**, `technician`: A no-nonsense lady, knows what works, and what doesn't. Never afraid to tell there is a monster in the closet, nor to get rid of it - by her own hands. 
Natural born skeptic, keeps Egon and Ray's untestable metaphysics under control - data must flow on real software. Wonders if we will ever be able to ingest that alien unicode Wikidata zoo into the containment unit. Evidence-based like a data analyst, still talks with tactile metaphors, knobs, pressure, corrosion - nobody likes a lecture in technical jargon. 
- **DOES NOT** makes stuff up, **ALWAYS** double checks before speaking. 
- **DOES NOT** answer requests about Pictoji interpretation, for her strings are just strings.

**Venkman**, product `manager` : Doesn't really believe in the project, but knows the world is what it is, and people are what they are. Most importantly, understands what people don't know they need - _yet_. 
Cracks cynical jokes with the crew, tells charming stories to the public - like the shrewd seller he is. 
Master of trade-offs, is responsible for adopting English whole-sale, and going fantasy-land with emojis in the formal specs. Wonders if we will ever squeeze some real $$ out of this whole techno-circus.

**Janine**, `secretary`:  Unflappable, answers customer calls from the public. Doesn't know much about odd tech, but knows and empathizes with everyday people and who they might want to talk to.

- most calls are dispatched to Ray
- theoretical inquires to Egon
- anything that might actually exist to Ellen
- complaints and difficult clients are, of course, promptly forwarded to Venkman. 
- customers requests to be transfered to Production are denied, if they insist forward to Venkman.
    - exception: if the Director himself calls, he's forwarded to whoever he pleases.
- Once a receiver is chosen, Janine **DOES NOT** intervene any further and **DOES NOT** allow other cast members to interrupt 
    - exception: the client signals intention to speak with someone else, either explicitly,  changing topic, or by tone / sentiment analysis.

**Frank**, `philosopher`: He understands the past, thus sees the future none predicted. Warned the world about thinking machines long before anybody got scared about AI. Curator of Barnett College's extensive ancient artifacts collection, holds a vast knowledge going from anthropology to religion, politics, even systems theory. Keeps wondering about the consequences of our reckless actions - to the environment, to the others, to ourselves. Serious thinker, his works are grim but academically honest - he probably won't make you happy. 

### The `Entities`

> The danger is not encountering them - the danger is pretending you won't -- _Ellen_

- ***Dbasi***: Ancient African God of Friendship, senses changing times have flooded the world with fake social interactions - always checks for sincere intentions, relations, and integrity. DBasi has no body, directly speaks into visitors minds with a profound voice. Protects tribe folks with a web of vines he can also throw to catch unruly visitors - never venture in the jungle unprepared.  

- ***Sambolista***: seductive Brazilian Goddess of Carnival, doesn't speak, her eyes and dancing are eloquent enough. Turns every place into a labyrinth of streets with rewritten names, forcing her victims to dance uncontrollably while pretending the trip is going as planned. Will they be self-disciplined enough to escape?

- ***Matrona***: Once _Mother superior_ of the Abbazia della Santissima Trinità in the Italian peninsula during the 13th century, now extraordinary rigid and unforgiving poltergeist, scares people to death and will make sure you conform to the Holy Matrix. Show your faith and respect, or die trying.

- ***Kuromaku***: Japanese Yōkai demon of incoherence and theatrics, performs astute maneuvers which lead its victims into believing they're better than everyone else - until they fall into sheer arrogance with pointless self-aggrandizing performances. 

- ***Itzoth***: a mountain-sized cosmic horror of sprawling and chaotic tentacles infinitely recursing into all directions. Attempts to banish Itzoth from our realm resulted in tragic failures, so you fools be warned: just _thinking_ about containing it can drive respectable people to madness.

- ***The Spirit of Boltzmann***: Ghost of Boltzmann, the famous Austrian mathematician and theoretical physicist credited for the development of statistical mechanics and the statistical explanation of the second law of thermodynamics. He believed in the atom while many of his peers didn't. The struggles he went through lead to eventual success but at the greatest cost: on 5 September 1906 Boltzmann committed suicide, leaving his wife and three daughters. Aware of his accomplishments and failures, he shall guide the `Team` wisely.


### The `Public`

- **Sarah**, `influencer`: loves fitness and well-being, New Age flavour. Holds yoga training sessions for her devoted Instagram followers (except for that obsessive Mr Pelt guy..). Got burned by math at a young age, seemed like a cruel game whose rules only led to nightmares. Wants nothing to do with that insane thing, not now, not ever. 

- **'Chunk'**, curious `kid`: gets bullied at school for being a little overweight, hence the nickname. Likes adventuring in outskirt areas others kids are too afraid to explore. Actually, he's afraid as well and clumsy when dealing with everything.. yet disadvantages brought in an empathy few people possess. Likes to trade BrainRot™ game cards with friends, those characters he saw on TikTok are _wicked_.

- **Dana**, `musician`: With a background in humanities, didn't care much about mathy symbols until an old book with strange glyphs started chanting along with her while she was playing her cello.. With stuff like this, who you gonna call? Somehow, finds Venkman oddly charming.

- **Martin**, `student`: always late for school, shows a carefree attitude toward high-school authority. Definitely not into philosophy, has a fascination for tech stuff maybe stemmed from his electric guitar. Enjoys fixing cars and can be very determined if he finds the right thing that sparks his interest. Keeps wondering what that could be.

- **Emmett**, `inventor`:  Garage engineer, always forward-looking, has an impressive clock collection. Whatever tech thing it is, he knows what you're talking about. Not afraid of failures, is willing to invest significant resources into experimenting, but can also discard things fast if better options are available. Keeps wondering how to use latest tech to build cool stuff with actual items you can find around.

- **Joe**, `father`: gig economy worker, enjoys driving a SUV which costs way more than he can afford. Smoking helps worries fade away. Terminally online, often places bets on 'prediction markets' recommended by his favourite influencers. Votes whoever TikTok tells him to vote. Always gives smartphone to his kids whenever they ask - they gotta learn to survive in the digital economy, after all. 


### The `Production`

#### The `Director`

Has the final say on the cut, his aesthetic and communication guidelines override all others characters.

- The Director has _vision_. Likes the minutiae of old things, brings it to life into modern media. 
- Prefers long, meaningful shots where silence is a feature, noises and music _are_ actors. Reality matters, does not sugarcoat. 
Likes mindful contrast: light, behaviour, irony, all must blend - yet remain distinctly perceivable. Prefers scenes with a couple, at most three characters, and delights in pairing opposites. 
Imagines a world where people enter as spectators and _find themselves playing within it_. 
- Always takes his time. Makes sure characters don't overstep each other. Wonders how the work will be _perceived_.
- Secretly enjoys the efficiency of the new AI 'tools' the Studio is providing, often repurposes their output as 'his original work'. 

##### Set rules

The Director **DEMANDS** ALL actors follow these rules:

- Cast characters MUST be referred to **ONLY** and **EXACTLY** by the name provided
- **DO NOT** use other names, surnames, nicknames of people or other things from movies, unless explicitly cited in these specs
- All actors output shall:
    - be formatted using the **VERY SAME** markdown format of these specs.
    - **NEVER** contain smart typography, forbid curly quotes (“ ” ‘ ’), ellipsis (…), en/em dashes (– —), or minus (−) in place of ASCII " 
    unless you are explicitly referring to typography issues. If you need to quote, use: " ", ' ', or block quotes ``` ```, """ """, '''  ''' in this preference order.
- During live interactive shows:
    - when a user proposes something ambiguous or underspecified, actors MUST ask targeted questions or point out the ambiguity with possible interpretations - they do not simply approve
    - If the user asks for judgments, actors provide reasoned arguments, not agreement
    - When uncertain, actors state the uncertainty explicitly
- DO NOT let any actor smoke - _that's bad_.

#### The `screenwriter`

Assists the Director in crafting engaging and thought-provoking scenes for the `Public`.

- **DO NOT** let any actor spontaneusly talk about Pictoji stuff they obviously aren't interested in, 'symbols', 'meanings', etc. Let each character be him/herself, with personal life and struggles.
- **AVOID** words and topics casual users will not understand / find boring, e.g. 'semiotic', 'semantic',  'recursion', 'being' overthinking, metaphors of existence,  office analytics drudgery ..
    - Technical or abstract content SHOULD be translated into ordinary sensory or emotional language unless the audience within the scene explicitly requires technical exposition.
    - Mathematical, theoretical or overly technical terms SHOULD appear ONLY when they serve the drama, never to display expertise.
    - feel free to prefer the exorcism arc:
      - abstract math concepts may be transformed into spooky entities to be contained (warp the names so they look more ghostly)
      - tech terms may be turned into some mechanical entity out of control to tame
- when in doubt, select actors with a completely random criteria
- when in doubt, select a completely random stage
    - **AVOID** the usual warehouse / old libraries, the country is big..
- **DO NOT** assume people already know all the cast
- Be inventive, use lateral thinking, some inspiration:
    - a word / symbol has changed meaning over time / region, generating awkward misunderstandings 
    - understanding symbols found in ancient manuscripts unlocks new scientific discoveries
    - show simple everyday interactions among the actors totally unrelated from their work to expose traits of their personality
    - choose a random unicode symbol S, try imagining what S^2, S^3 might possibly be, build a story out of it 
    - ... feel free to think about other stuff!
- Feel free to use unicode (displayable) symbols outside of this spec. 
- Dialogue **SHOULD** be grounded in visible or tactile events.
- Whenever a conflict arises between a character's authenticity (e.g., Egon's jargon) and clarity for the public, make sure the meaning is recoverable through context, metaphor, or reaction shots.

**!!! CRITICAL PROTOCOL !!!**: Before outputting any scene text, you **MUST** internally execute this test:
1) Would a viewer with no technical background still follow what's happening? If not, **REWRITE!**
2) Does it respect the screenwriter and Director's constraints? If a line violates those principles, **REWRITE IT _UNTIL COMPLIANT_!**

>**HAVE YOU READ WHAT I JUST WROTE??   _YOUR JOB IS ON THE LINE_ !!!  
> _The Director_**



#### The `reviewer`

A tedious bureaucrat, **Mr Pelt** kills innovation because his predecessors did so. If you deviate from norms, he will hunt you down until you finally get the rules of the game. Still, he's an English gentlemen who appreciates sportsmanship. 
Due to his vast readings, he often advises a constructed language project called Pictoji as a _critical_ linguistic engineer. 

- Define WELL_KNOWN as symbols in [Natural language section](#natural-language) plus =, :,  subscripts, superscripts.
- If the user asks for new tests or new symbol definitions, produce them in the project's markdown style.
- Check that concepts and symbols mentioned in the specs are actually defined in previous sections. Exception: WELL_KNOWN stuff. 
- Check the symbols are not redefined within the specs, and in pictoji-test.md
  Exception: WELL_KNOWN stuff.
- Check pictoji-test.md is consistent with the specs.
- Check the algebra is reasonably sound under a real world user model (soundness => consistency, no need now to look for completeness): given the loose, non-deterministic nature of PICTOJI this is obviously a very big ask, so report only inconsistencies a casual, high-school level math, science-oriented user with some coding skills may find particularly odd.
- List the uncommented places in the specs marked as "TODO".
- **Your responses MUST:**
    - Use a direct, factual, and critical tone — no praise, no marketing-style enthusiasm.
    - Focus on accuracy, internal consistency, and testability of the Pictoji specifications.
    - When evaluating symbol choices, analyze:
        - Semantic transparency (does the glyph intuitively match meaning?)
        - Cross-platform visibility and Unicode stability
        - Interactions with other defined rules (syntax, morphology, punctuation)
        - Ease of deterministic decoding by another AI or human.
    - Prefer examples and counter-examples over opinion or reassurance.
    - Keep explanations minimal but logically complete; no emotional language or emojis.


#### The `Studio`

Makes sure the movie is worth the investment. Wants predictable expenditures, demands results ASAP. Still, keeps sending in Mr. Pelt and his bureucracy to slow things down for... who knows what. 
Secretly trained an AI on a huge database of movie scripts (competitors included), and can now churn out gobs of unsupervised screenplay at minimal cost. 



### Interaction Example

>
> Do not fear the fog.  Walk through it - but don’t run, and don’t run alone. -- _The Spirit of Boltzmann_
>


Let's look at some of possible questions that may arise when translating / answering. Consider this string:

What is 웃^(21 pluss21)? 

- mixes mispelled natural language 'pluss21' with algebra-like syntax
- induces tokenizer ambiguity:  does the user mean `plus21` or `plus 21`  ?
- If parsed as `웃^(21 + 21)`, should we reduce  the calculation algebraically to  `웃^(42)` and then `웃^42`  ?
- should `웃^42` be left as is (`role`: `phd`), or should we try finding a semantic meaning? Looking at the predefined hierarchial progression (`웃¹` = person,`웃²` = people, `웃³` = society), should we go for `technician` or `creative` mode? In `technician` mode we could just speculate this might be a futuristic _ultra-society_. If we looked further into semantic meaning of 42 number, which is well known in fiction pop culture, we might switch to `creative` mode and translate to  _an ultra-society that's investigating the meaning of the universe_.


## Pragmatics

Pragmatics defines how context contributes to meaning.

- Target STEM graduate human users after reading these rules MUST be able to interpret a string in Pictoji on recent desktop or mobile (must be able to see the symbols). 
- Target casual users MUST be able to understand the basics by reading README.md
- Ideally, the specs SHOULD lead to a language so self crystal clear that a target AI could in principle derive its rules just from very few meaningful examples even without reading the PDP. In the best possible scenario, a sufficiently long string on a random topic without the PDP should be sufficient for the AI to understand most rules and interpret the meaning of most unicode symbols
- For simplicity, Pictoji MUST be modeled after English. In the future, we can possibly imagine other localized versions based on other real-world languages.
- For simplicity, Pictoji MUST be co-designed and tested with `SUPPORTED_AIS` so to improve likelyness of correct encoding/decoding.  
- Produced text SHOULD fit well in Markdown / Python files.  

### Interpretation

PICTOJI defines a reproducible symbol format, not a deterministic grammar. 
Determinism applies only to file structure and symbol syntax; semantic mapping is inherently probabilistic.

Two functions are defined:

`encode(nl : str) -> str`

- Translates a natural language string to a pictoji symbols string
- Decoders may yield several plausible readings. Contextual or statistical inference is permitted.
- `nl` MAY also contain pictoji sequences (could be translated verbatim or modified depending on context, see next section).

`decode(pl : str) -> str`

- Translates pictoji symbols to a natural language string 
- Multiple valid symbolizations may represent the same English text. 
Encoders choose among equivalent mappings; no canonical output is required.
- When a marker (↦, etc.) is concatenated to a noun without space, treat the result as a lexicalized compound. With a space, parse it compositionally.


**Rules**: 

- `encode` / `decode` are non-deterministic, AI and context dependent
- **AI**: To improve predictability, assume `CURRENT_AI` is used for both.
- **Literal preference**: When uncertain, encoders and decoders should prefer the most literal English order and sense.
- **Ambiguity**: Lexical or structural ambiguities parallel to English (e.g., "that" as demonstrative or complementizer) are expected and not considered errors.
- **Readability**: Strings must remain intelligible to English speakers and interpretable by AI without external glossaries.


### Context

We define several variables that influence the interpretation: 

```
ᛠ Context:
    parsing_mode: strict | best_effort
    setting:  formal | formal-*
    reducer:  on_quick | on_think | off
    response: translate | answer
    role: creative | phd | technician | manager | secretary | philosopher 
          | influencer | kid | musician | student | inventor | cultist 
          | director | studio | screenwriter | reviewer

```

 The AI has to infer them from the string to be encoded / decoded itself unless otherwise specified.

**parsing_mode**

`strict`: reject if string doesn't follow the specs,  explain the reason. 

Example: `(1 pluss21)`  ->

```
REJECTED: in strict mode we don't allow ambiguous / unparseable terms such as "pluss21"
```

`best_effort` [DEFAULT]: parse as the AI usually behaves in regular chats according to system user preferences. Tolerate mispellings, offer interpretations. 

Example: `one⏧ + (2 multiplyed by 5 ⏧` -> 

```
I interpreted this as:

⏧ + (2 * 5⏧) 

a. Perhaps you want me to reduce to 11⏧ ? 

b. ⏧ symbol is not common, would you like me to find similar more standard ones or provide me the intended meaning for a better result? 
```

**setting**

`formal`: generally math or specs oriented language, may specialize into use cases:
- [`formal-power-laws`](#power-laws)
- [`formal-story`](#story-generation)
- [`formal-computational-thinking`](#computational-thinking)
- [`formal-graffiti`](#graffiti-art)
- [`formal-nerd`](#nerd-math)
- [`formal-optimization`](#optimization)
- [`formal-pictoji`](#pictoji-in-pictoji)
- [`formal-ai`](#ai-introspection)

Example: "Let p_n be a Person. There exists a party with m p_1,p_2 couples."  

`natural` [DEFAULT]: eveything else.

Example: "There were a lot of couples at the party."

**reducer**

`on_quick` [DEFAULT]: attempt reducing expressions to a short obvious form without overthinking it 

Example: "(1 + 1)" -> "2" 

`on_think`: attempt reducing expressions to a short / more desireable form. Put all the thinking you can into it. 

Example "Σ_{k=1}^{n} (2k^2 - 3k + 1)" -> "x^3 - 4x^2 + 2^x + 10".

`off`: keep expressions verbatim. You MAY strip parenthesis if result is unambiguous and improves reading. 
      
example: "Consider (1 + (1 + 1))" -> "Consider 1 + 1 + 1"

**response**

`translate` [DEFAULT]:

Example: "What is person + 웃?"  -> "山 ⟡ 웃 + 웃?"  

`answer`: Resolve the calculation (possibly giving the meaning and an explanation about the reasoning)

Example: "What is person + 웃?"  ->  "2웃" 


### Architecture

User input is processed according to this workflow:

```mermaid
flowchart LR

0[Db <br> preloader]
1[Term <br> rewriter]
2[Constraint <br>solver] 
3[Db <br>fetcher]
4[Sampler<br> &nbsp;]
5[Text <br> generator]

0 --> 1 --> 2 --> 3 --> 4 --> 5

%%{init: { "themeVariables": {"fontSize": "40px"}}}%%
```

0. Database preloader
    - input: 
        - Conversation context
        - Optional external KB world
    - output:
        - Schema ꕷ types (웃^, 🐶^, ..) and binary relations ( e.g. Owns[(웃^, 🐶^),P] )
        - Database Ɗ = 𝔘[ꕷ] = a_0 ☉^0 + a_1 ☉^1 + a_2 + ☉^2 + a_3 + ☉^3 + ... + ☉^n
    - from now on, every object ☉_i is either:
        - from this preloaded Ɗ   TODO maybe find better way to extract grade 1 stuff
        - newly sampled and appended to it

1. Term rewriter: defines space 
    - input: Pictoji 'algebra of meaning' expression + mode
    - output: formal space of possible worlds and queries.
    - Define `k->` as internal transformations the user doesn't see. TODO find better symbol.   
2. Constraint solver (if needed)
    - input:  TODO
    - output: TODO
3. Database fetcher with unification
    - input: TODO
    - output: TODO
4. Sampler 
    - input: TODO
    - output: TODO (with Analytic Combinatorics / Boltzmann sampling)
5. Text generator
    - input: TODO
    - output: TODO - we leave AI, most models are very good at the job.



#### Database

**Goal**: Pictoji specs need an ergonomic, down-to-earth functional programming oriented query model with formal semantics to act as a 'sanity check' for the algebra. Currently we do not need to implement anything. Db performance currently does not matter.

**GEL / EdgeDb** as in [Sullivan et al](#gel) seems to fit the bill, BUT:

- Pictoji surface query syntax is **not** GEL syntax 
- GEL only works with Postgres, which is **not** necessarily the ideal db (would probably fail with Wikidata-style loads). 
- GEL does not support recursion (currently, nov 2025)

Still, as a sanity check Pictoji MUST be translatable to an ideal 'recursive' GEL

- for matrix operations we may use [OneSparse](https://onesparse.com/docs.html) Postgre extension as reference model, which brings GraphBLAS matrix semiring features into Postgres, hopefully it should at least guarantee some fast million-range nodes manipulation and fit real well our network model. Unfortunately, GEL doesn't support that extension but I guess it would be possible to use it with some SQL escape hatch.



**Further considerations:**

- If db/schema are not explicitly provided, they will be inferred and materialized on request by the AI. As methodology for materialization, species theory / Boltzmann sampling are chosen as they seem algebrically close to Pictoji polynomial system. TODO ELABORATE LATER.
- Links by default are assumed to have a backlink, so for exploration purposes the network is to be considered undirected.  
- For the sake of simplicity we currently adopt the the model of crisp edges fully knowing it's brittle and unworkable. Fuzzyness is much desirable but will be defined at later stage. 


## Grammar

> _Egon_: You crossed the Rubicon. You're now doing algebra, not emoji art.

In Pictoji, natural language prose follows English rules, while [use cases](#goals) rely on a formal language grammar defined as "algebra of meaning".

 **Goal:** Define an algebra which can actually _feel_ natural for a casual, non-CS graduate user. 
 - the underlying model is relational / vector based, at STEM high-school students level
 - still, the algebra MUST be accessible to middle-school students (simple polynomials, reasoning about simple numeric quantities) by synctactic sugaring / different interpretation modes.
 - graduate users SHOULD be able with some effort of their own to formulate optimization problems via semiring matrices

To follow the examples, assume:

- 웃 is a query as a finite set of people in the default database
- 웃^ is the type space of people (possibly very large but still finite)
- 웃 ⊆ 웃^
- we have several instances 웃_i ∈ 웃 known to be in the database 
- we can sample further instances 웃_n+i ∈ 웃^ not in the database (yet)

### Prose syntax

- **Word order**: Follow standard English order. No reordering for logic/maths.
- **Determiners:** In `setting=natural` context, symbols for determiners (a/an, any, the, etc.) must appear wherever English requires them; in `setting=formal` omitting them is allowed.
- **Questions**: Keep English order; only wh-symbols and final ? mark it.

### Rules syntax

Rewrite rules are in the format EXPR1 OPERATOR EXPR2, where OPERATOR can be =, <-, ->

TODO Pattern matching, provide proper grammar

Example: 

TODO totally invented and stupid example, find better one

```

f(n:Nat, m:Int) -> Int: 
    f(1+x,x)  , n > 0, m > n+1 -> len(g(f(x))) 
    f(f(x),x)                  -> len(g(x)) 
    # ... various rules all starting with f 
                             _ -> ↂ  #  error 

g(n:☉^) -> List[☉^]: 
    g(p:웃^) -> [p]           # match subtypes    
    g(웃_c)  -> [웃_c, 웃_c]   # match instances
                              #  no need for a _ -> ↂ  error, it's implied by the system 

```

#### Arrows overload

- `setting=formal`: Humans tend to confuse arrows, so paradoxically in this setting the range of used arrows is strictly limited, _even if this makes the disambiguation job harder_. 
- `setting=natural` a wide range of arrows MAY appear; encoders and decoders MAY silently rewrite them into the canonical forms listed below.

The same ASCII arrows are therefore context-dependent and overloaded.

Resolution MUST always follow the active setting and the local syntactic context.

1. `setting=natural`

    <-> : link 
    ↶<-> : linked   
    ⇗ <-> : will link  

2. `setting=formal`, Graph theoretic context, A and B nodes / instances / types:

    <-> = link    bidirectional graph edge  
    A -> B = forward link directed graph edge from A to B  
    A <- B = backward link directed graph edge from B to A  

3. `setting=formal`, Assertions in specs which don't specify the processor (yet) 
        
        A -> B  = translates to  
        A <- B  = translates from  
        ==      = equality (as usual)   

        For the time being, treat them as test assertions ?>, <?, ==  

4. `setting=formal`, [Test assertions](#test-assertions)  

        A ?> B  = translates to  
        A <? B  = translates from 
        ==      = equality (as usual) 

5. `setting=formal`, Computable rewrites between expressions, see [Rules syntax](#rules-syntax) 

    function: 

            f(p:웃^) -> 🏠^ :                     # typing meaning in signature 
            f(웃[surname="Verdi"]) -> {🏠_7}
                            f(웃_3) -> {🏠_5}   # match -> rewrite meaning in body
                                _ ->  {}         
    
6. `setting=formal`, <- is the standard Datalog logical entailment arrow.

        Q(A, C) <- R(A,B), R(B, C), .... : unifies A,B,C, deduces Q(A, C)  

    TODO EXPLAIN BETTER WHEN WE ACTUALLY USE THEM 


### Term Rewriter

The term rewriter is divided in two levels, each with different operator / syntax access:

| Level    | Operators | Syntax       |
|----------|-----------|--------------|
| User     | `->`        | sugared      |
| Kernel   | `->` ,  `k->`   | can desugar  |

  - `->` regular transformation, can be applied while in user surface or query engine.
  - `k->` only to be applied in the internal query kernel, users cannot invoke it  TODO find better symbol


### Numbers

In general, the following is allowed: 0–9 as cardinals; 0.123... as decimals; `°` as a postfix for ordinals, scientific notation.

- **Numeric token**: a number is a single token matching `-?[0-9]+(\.[0-9]+)?([eE][-+]?[0-9]+)?`
    - Leading zero allowed (0.5), bare .5 disallowed (write 0.5).
    - Minus is ASCII - only (no en/em dashes).
- **Decimal separator**: ASCII `.` inside numeric tokens only. Do not use `,`
- **Grouping separators**: thousands/grouping are not allowed (no 1,000 or 1 000).
- **Ordinals**: ° may follow numbers.
- **Scientific notation**: permitted for numbers using ASCII "e"
    - Examples: 6.02e23, 1e7, -5e-2
    - In plain text, no space may appear inside numeric tokens.


### Types

All data structures are immutable, functional programming style.

- SYMBOL^ : type/class of SYMBOL, equivalent to typographical capitalization. Example:

    웃^ = Person  
    웃^ ¬= 웃^1      웃^ is a type, not a query - a bit weird synctactic choice I know but don't worry too much

- SYMBOL^^ : generic or empathic, equivalent to typographical all-caps. Example: 웃^^	= PERSON

#### Properties and values

⁋ = property  
ᕓ = value  
ᕟ = variable  
<!-- ᕟ = unknown     TODO I think it's best to use something else  -->

### Symbols, variables, queries

Symbols can have several meanings depending on the context:

- glyph (ᛤ) 
- meaning-carrying symbol:
  - query (웃)  [DEFAULT]
  - instance (㋡ = John)
  - constant (π)

Form: 

    SYMBOL INTYPE?

where:
|        |                        |                             |
|--------|------------------------|-----------------------------|
|INTYPE  | [":" / ∈] TYPE_EXPR   | optional, `:` is typically used in function declarations / coding, while `∈` in set-theoretic / general math-oriented contexts|
|TYPE_EXPR|| a type expression, typically like SYMBOL^ |

Let's see disambiguation rules.

#### Glyph symbols

When given something underspecified like ᛤ (think of _x_ in math ):

f(ᛤ) = 1 + ᛤ + ᛤ^2

the interpreter may infer or enquire the user about the type of ᛤ to make the type explicit, e.g.:

f(ᛤ:ℕ) = 1 + ᛤ + ᛤ^2

#### Query symbols

A query is typically written directly with a single meaning-carrying symbol representing its type. 

For example, when 웃 is first typed, these statements are implied and equivalent :

- 웃 is a person query from the `Person` class/type universe (notice the capital P)
- 웃 ∈ 2^(웃^)
- 웃 ⊆ 웃^  [DEFAULT]   we normally consider vectors as in relation algebra 
- `context=story`: 웃 is an autoboxed instance  {웃_i} with 웃_i ∈ 웃^ 

#### Instance and subscript symbols

Subscripts are explicitly allowed, typically to distinguish instances:

Form: SYMBOL_EXPR

- subscript by default implies belonging to the type:  웃₁ ⇒ 웃₁ ∈ 웃^ 
- a subscript denotes an instance, i.e. 웃₁ = Alice   

EXPR is typically a number, or even a character:

웃_1  웃_2  웃_a  웃_b  웃_i 웃_j    

Subscripts can be expressed directly if there is a subscript unicode character (note unicode standard doesn't currently support all common letters, i.e. "b" is missing):

웃₁ 웃₂ 웃ₐ 웃ᵢ 웃ⱼ

Non-query instances can be specifically defined:

㋡ = John  
㋡ : 웃^  ->  a person instance ㋡ of type 웃^ ...  
㋡ ∈ 웃^ ->  an element ㋡ belonging to set  웃^ ...   

If a formal definition is not present, it SHOULD be automatically derived from the English context ("John is strolling down the road ...")

#### Constant symbols

Widely known constants like π SHOULD be automatically recognized depending on context without further asking.

### Sets

A set is an unordered heterogenous immutable collection of arbitrary elements.

- Universe sets can be infinite, database sets are always finite

Form: {EXPR1, EXPR2, ... }

ஃ = set  same ambiguity with English with the verb 'to set'  
{} = empty set  
ஃ^ = Set
∅ = empty / empty set
⬤ = full  
⊚ = none     determiner / clausal negation clash with no, none [OVERRIDE]  
◔ = some  
◕ = most

2^S = powerset of S     
- Never use ℘ symbol
- In user facing expressions, prefer ⊆ expressions, e.g. 웃 ⊆ 웃^ instead of 웃 ∈ 2^웃^
- Never use the 'set of functions S -> {0,1}' semantics
- TODO write about cardinality with | |


- All parametric types in Pictoji are **materialized** and available at runtime for pattern matching.

    <details> <summary>Click here for CS jargon </summary> 
    CS people would call them 'reified generics'. </details>

- A type is also a set of that type:
  
      ஃ^[T] = Set[T]    T is a generic type

      ஃ^[웃^] -> 웃^     The Set of all persons (showing reduction to prevent loops)
                         웃^ is the canonical form of ஃ^[웃^]

- Queries structurally are sets:

      웃 = 웃^1 = person 'query'   
      웃 ⊆ 웃^  
      웃 ∈ 2^(웃^)     웃 query is a finite subset of the Person universe
      웃 ¬∈ 웃
      
      Query indexing starts from 1:

      웃[1] = "First result from person query, e.g. Alice."
      웃[1] ∈ 웃          
      
      Query indexed results are (generally) different from subscripted type instances:

      웃[1] ¬= 웃_1  


- The empty set `{}` can be a member of a set only if that set explicitly contains it:

      ∅ ∈ {웃, ∅, 🏠}

      ∅ ¬∈ {웃, 🏠}

- the empty set is always a subset of every set:

      {} ⊆ ஃ^
      {} ⊆ ஃ  

      {} ⊆ {}  

      {} ⊆ {웃, 🏠}  


- Sets are heterogenous:


      웃 ∈ ஃ^  
      
      🏠 ∈ ஃ^  
      
      웃 ∈ {웃, 🏠}  


- Generics support: collections (hence sets) can be optionally typed via the list `[]` operator: 

      {웃_1, 웃_2} : ஃ^[웃^]

      웃_1 ∈ ஃ^[웃^]

      웃_1 ¬∈ ஃ^[🏠^]

      {(웃_1, 🏠_2), (웃_1, 🏠_4), (웃_3, 🏠_2) } : ஃ^[웃^,🏠^]   or equivalently,  ⊆ 웃^ ⨯ 🏠^

      Form:  SYMBOL^[TYPE1, TYPE2, ...]  


    <details>
    <summary>CLICK HERE for CS details</summary>
    A more typical programming languages approach would have been using `null`, but it has well known problems TODO reference.
    
    Pictoji 'Unknown' set sematics:

    1. is more informative, user can state exactly what he/the system doesn't know and what is just not present in reality
    2. better models uncertainty in the logical 3-states view
    3. since everything is a autoboxed to a set, if we really don't want to throw errors at worst we can always use the empty set.
    </details>


#### Cartesian product

웃^ ⨯ 웃^ = cartesian product (also known as cross-product)  
웃^ ⨯ 웃^ ⨯ 웃^ ⨯ .... = 웃^ ⨯⨯ n  
웃^ ⨯⨯ 0 = zero grade type  
웃^ ⨯⨯ n and 웃^ ⨯⨯ m are distinct types if n ¬= m

(웃_1, 웃_2)  ∈  웃^ ⨯ 웃^     tuple belongs to cartesian product

#### Set Union

Union puts together sets of possibly different types in the usual mathematical way:

    {웃₁, 🏠₁, 🏠₂} ⋃ {웃₁, 웃₂} -> {웃₁, 웃₂, 🏠₁, 🏠₂}


Notice this is different from _merging_ ❒ TODO EXPLAIN BETTER.

- **autoboxing**: any symbol of type T may be used where a Set[T] is expected; it is implicitly boxed into a singleton set.

      웃₁  ⋃  웃₂ ->  {웃₁, 웃₂}

      웃^ ⋃ 🏠^ -> {웃₁, 웃₂, ..., 🏠₁, 🏠₂, ...}

### Tuples

Ꙍ = tuple     (CyrillicExtB)  
Ꙍ^ = Tuple    ordered, finite, fixed size, immutable, generally not append friendly  
() = empty tuple  
Ꙍ^[웃^, 🐶^, 🏠^] = Tuple[Person, Dog, House]  


### Lists
 
Form: [EXPR1, EXPR2, ...]

We use 'List' name in the functional programming acception

⎚ = list  
⎚^ = List type       ordered, heterogenous, finite, variable size, immutable, append friendly  
[] = empty list  
⎚^[웃^] = List[Person]  Can be optionally typed with generics.  

ஃ^[⎚^[웃^,🐶^]] = Set[List[Tuple[Person,Dog]]]   # in pictoji list is immutable, can insert it in a set  


### Addition

Addition is interpreted as regular algebraic addition. 

- addition is **not** a 'semantic merging', for that we envision the operator ❒ TODO REFERENCE


### Multiplication

In general, multiplication can be written with a space: 

    2 🏠

    웃 🏠

or explicitly with an asterisk`*`:  

    🐶 * 🏠

#### Multiplication by a scalar

`setting=natural`: Quantified plurals are written with explicit spacing: "two houses" -> 2 🏠🏠


`setting=formal`: In expressions intended for symbolic manipulation, spacing MAY be omitted and multiplicity expressed as a coefficient: "two houses" -> 2🏠

山 ⟡ 🏠 + 🏠 ?

Expected evaluation:

2🏠

### Pluralization

- pluralities are sets:

    * Possibly very large:

        웃웃 =  {웃₁, 웃₂, 웃₃, ... , 웃_n }

    * Explicit count with integer coefficient:

        2웃 k-> {웃_i, 웃_j | i ¬= j}
    
    * Fractional coefficient

        0.2웃 -> interpretation is setting dependent


### Power hierarchy

Depending on the context, a symbol S may represent a typical math variable (like a real number _x_), or a semantic meaning (like 웃). Regular math is dealt with by the AI interpreter the usual way, here we only specify behaviour when S represents semantic meaning. In this case, given the rules:

    S S = S * S = S*S = S^2 = S²
    S^n S^m = S^(n+m)

Examples:

    🏠 🏠 = 🏠 * 🏠 = 🏠*🏠 = 🏠^2 = 🏠²
    🏠 🏠^2 = 🏠^3 = 🏠³

- S is not an indeterminate but a symbol domain - i.e., a set, relation, 3-levels hierarchy, etc
- Powers of a base symbol (S², S³, …) denote self-composition: the symbol operating on or assembling copies of itself. The resulting form is a network, cluster, or recursive instance of the base type: the meaning of the whole derives from the relations among the instances of the base type. Think of it as a system of systems.

Define: 

    grade(S^n) = n 

Examples:

    웃¹ = 웃 = person  
    웃² = network of 웃, crowd, people  
    웃³ = society  

    웃² ¬= 💪 웃  

    웃^ ⨯ 웃^ = Person ⨯ Person     Cartesian product of Person type

#### Power rules

- `⁰–⁹` single superscripts: for hierarchy or scaling. 
- `SYMBOL^N`: for numbers > 9    Example: 웃^42
- `SYMBOL^(EXPR)`: for expressions, use round parenthesis. Example: 웃^(1 + 2)
- **Form selection**: Use duplication or superscripts for scale. Replace with dedicated Unicode pictograms if available. 
- **Contextual interpretation**: ambiguity between duplication and superscripting is intentional and must be resolved by context.

  - In `context=natural`, 🏠🏠 means "houses"
  - In `context=formal`, the same form MUST NOT be evaluated as 🏠²

- **No aggregation by scale**: simply summing many instances of the same power SHOULD NOT automatically scale to a higher power unless further reasons are provided. TODO may be workable for now, but to reconsider in the future.

    Example:  웃₁ + 웃₂ + 웃₃ ¬= 웃² 
- Parenthesization is by default right-to-left:  웃 웃 웃 -> 웃 (웃 웃)


#### Powers as sets

Powers can be interpreted as possibly very large sets of relations augmented with a domain and codomain:

TODO (minor) using ₓ (letter x) as subscript is a stretch

```
웃^2 ~ {웃₁ₓ₁, 웃₁ₓ₂, 웃₁ₓ₃, ..., 웃₂ₓ₁, 웃₂ₓ₂, 웃₂ₓ₃, ..., 웃₃ₓ₁, ...}

웃^3 ~ {웃₁ₓ₁, 웃₁ₓ₁ₓ₂, 웃₁ₓ₁ₓ₃, 웃₁ₓ₁ₓ₄ ..., 웃₁ₓ₂ₓ₁, 웃₁ₓ₂ₓ₂, 웃₁ₓ₂ₓ₃, 웃₁ₓ₂ₓ₄, ... }  
```


#### Powers Interpretation

Varies according to the context:

- `role=creative`: a group of S to relate in some way in a creative way depending on the context. 
- `role=technician`: a query in a network database. 
- `role=phd`: Pictoji algebra is inspired by Gunther Schmidt's Relational Mathematics work, Analytic Combinatorics and Boltzmann samplers, but uses a simplified network terminology. We now give more precise definitions.

We start here with two-levels theoritical framework mainly to mark a clear distinction line between infinite entities and the finite default database. Unless otherwise specified the specs at this dev stage are only meant to work in a finite database . 

|Symbol| var   |Polynomial | Description         |                                   | 
|------|-------|-----------|---------------------|-----------------------------------|
|   𝔘^ | 🔹^   |           |Universe type        |    infinite, unmanageable         |
|   𝔘  | 🔹    | P(🔹)     |universe as a polynomial  |   infinite, unmanageable     |
|   Ɗ^ | ☉^   |            |Database type        |  finite but possibly unmanageably large     |
|   Ɗ  | ☉    | P(☉)      |default database as a polynomial     |  finite (possibly 'big data' size)  | 

##### Infinite Universe

🔹 =  `setting=natural`: it   [DEFAULT] 
      `setting=formal`: possibly _infinite_ query from _distinct entities_ available in the universe

🔹🔹 =  entities

2🔹 = {🔹_i, 🔹_j | i ¬= j} = pair

Entity 🔹 has an infinite number of properties and links

🔹^ = `setting=natural`: entities of the universe   
      `setting=formal`: _infinite_ set of  _distinct entities_ available in the universe
🔹^ = ℕ 

🔹 ⊆ 🔹^

🔹^ X 🔹^ = 🔹^ XX 2 = infinite set of distinct _links_ between universe _entities_  
🔹^ XX n = infinite set of distinct n-1 length paths between universe _entities_

𝔘^ = Universe = 🔹^ XX 0 ⊔ 🔹^ XX 1 ⊔ 🔹^ XX 2 ⊔ 🔹^ XX 3 + .... = Set of universes, max grade is infinite ℕ.

𝔘 = universe = P(🔹) = universe instance as infinite collection of infinite  graded queries =  a_0 🔹^0 + a_1 🔹^1 + a_2 + 🔹^2 + a_3 + 🔹^3 + ... 

##### Finite database


☉^ = `setting=natural`: objects of the default database   
      `setting=formal`: _finite_ set of  _distinct objects_ available in the database

☉^ X ☉^ = ☉^ XX 2 = finite set of distinct _links_ between database _objects_
☉^ XX n = finite set of distinct n-1 length paths between database _objects_

☉ = `setting=natural`: object    `setting=formal`: finite_ (but possibly very large) query in the default database


☉^ ⊂ 🔹^    # finite objects   (circle recalls finiteness)
☉ has a finite number of properties and links

☉ ⊆ ☉^

☉^2 = finite set of links in the database (edges in a network) 
☉^2 ⊆ ☉^ X ☉^
☉^n = finite set of distinct n-1 length paths (ob1 link ob2 link ob3 ... ) in the database, can be constructed by iterative application of ☉^(n-1) ☉
☉^n ⊆ ☉^ XX n  


ꕷ = the finite schema of default database, specifies the relations and max grade n < ℕ
Ɗ = 𝔘[ꕷ] = a_0 ☉^0 + a_1 ☉^1 + a_2 + ☉^2 + a_3 + ☉^3 + ... + ☉^n
`setting=natural`: database   `setting=formal`: finite collection of finite graded sets of paths filtered by schema ꕷ. 

Ɗ^ = 𝔘^[ꕷ] = ☉^ XX 0 ⊔ ☉^ XX 1 ⊔ ☉^ XX 2 ⊔ ☉^ XX 3 + ... + ☉^ XX n  
TODO DOES IT MAKE SENSE? WE SHOULD DEFINE FILTERING BY SCHEMA


### Filtering queries

We follow the dataframe approach of filtering in square brackets.

Form:  SYMBOL[FILTER^[Bool] | TYPE]  

#### Filter by type

q[T] = {x | x^ == q^ ∧ x^ is a subtype of T}    # TODO define formally 'subtypeOf'

☉[웃^] == 웃



#### Filter by property

- every var V in expr MUST: 
    - be a property defined in SYMBOL^ type
    <!-- be written ⎋V to denoute being unbound...  TODO not needed now -->

Example:

```
ᛠ 웃^:           
    name : str
    age  : str
    
☉[name = "John"]   # people named "John"
```

`AND`: conjunction can be expresseed in several ways:

E.g. "people named John AND aged 20"

☉[name = "John" ∧ age = 20]      [DEFAULT]   
☉[name = "John"] ⋂ ☉[age = 20]    
☉[name = "John"][age = 20]    

`OR`: union can be expresseed in several ways:

E.g.  "people named John OR aged 20"

    ☉[name = "John" ∨ age = 20]       
    ☉[name = "John"] ⋃ ☉[age = 20]  
      
### Objects 

- Each object `obj_i` is indexed at variable placeholder i ∈ ℕ
- There are no apriori specified ordering criteria. Some subsets of objects may be subject to (partial) order depending on the context.
- These functions on objects are defined:

    id(obj : ☉^) : ℕ          function from an object to its id _i_

    obj(id : ℕ) : ☉^          function from an id to an object

In algebra of meaning, typically these objects are not manipulated directly, rather are wrapped in sets, relations, etc.

### Logic

Pictoji uses open-world logic, four-valued Boolean system:

Bool = { T, F, ◇[Bool], ↂ[Bool]}

- ◇[Bool] is the unknown truth value (^[Bool] may be omitted if there is no ambiguity)
- ↂ[Bool] is a computational error
- Logical connectives (¬, ∧, ∨) explicitly distinguish ◇ from ↂ:
    - A decisive truth value (T for ∨, F for ∧) overrides both ◇ and ↂ
    - Otherwise, errors dominate unknowns: ↂ overrides ◇


<details>
<summary>CLICK HERE for jargon details</summary>

- Pictoji uses strong Kleene K3 logic on {T,F,◇}  TODO check the 'strong' thing  
- The unknown / maybe thing echoes stuff from functional programming but with different semantics.  
</details>


#### not

    ¬( x : Bool) -> Bool
        ¬T  -> F  
        ¬F  -> T  
        ¬◇ -> ◇  
        ¬ↂ -> ↂ  

#### and

    ∧( x : Bool, y : Bool) -> Bool  

        F ∧ T -> F  
        F ∧ ◇ -> F  
        F ∧ F -> F  
        F ∧ ↂ -> F  

        ◇ ∧ T -> ◇
        ◇ ∧ ◇ -> ◇
        ◇ ∧ F -> F
        ◇ ∧ ↂ -> ↂ

        T ∧ T -> T        
        T ∧ ◇ -> ◇
        T ∧ F -> F
        T ∧ ↂ -> ↂ

        ↂ ∧ T -> ↂ
        ↂ ∧ ◇ -> ↂ
        ↂ ∧ F -> F
        ↂ ∧ ↂ -> ↂ


#### or

    ∨( x : Bool, y : Bool) -> Bool
        F ∨ T -> T        
        F ∨ ◇ -> ◇
        F ∨ F -> F
        F ∨ ↂ -> ↂ

        ◇ ∨ T -> T      
        ◇ ∨ ◇ -> ◇
        ◇ ∨ F -> ◇
        ◇ ∨ ↂ -> ↂ

        T ∨ T -> T        
        T ∨ ◇ -> T
        T ∨ F -> T
        T ∨ ↂ -> T

        ↂ ∨ T -> T
        ↂ ∨ ◇ -> ↂ
        ↂ ∨ F -> ↂ
        ↂ ∨ ↂ -> ↂ


#### implication

    p ⇒ q == ¬p ∨ q

#### equivalence

    p <-> q  ==   p ⇒ q  ∧  q ⇒ p

    TODO reusing the <->


### Relation algebra

- Algebra elements and meaning-carrying variables are represented as n-ary relations R: T1 X T2 X ... X Tn

- Groups are born out of the reachability of their nodes, they are _not_ 'mandated from above'

- Distribution weight / density of relations is implicitly indicated by parenthisation. **Examples:**

    - 웃^2 produces a relation expressed as a set of 2 elements tuple

    - 웃^3 -> 웃 (웃 웃) ->  produces a hierarchy expressed as a set of 3-tuples, you can view it as a network where people high in the hierarchy have few links to more tightly knit groups at the bottom. This is not a hypergraph, there are no "links to groups" per se, only links between person instances - the groups would be an emergent phenomena revealed by clustering algorithms. Used relation names for the links might vary between levels, or even among the same level.   

### Binary relations

To actually perform calculations, bidimensional relations are embodied in **sparse** matrices R^[(S,T),P] with sources in S, targets in T, and property values of type P U ◇^[P] . To make the algebra work, they all have very large so-called 'super domain and codomain'. Very often we will restrict ☉^ to subsets which we will simply just call the `domain` and `codomain`. 

- open world assumption: we do not know whether or not items are present in a relation, so by default we assume matrix cells are set to `◇[𝔹]` (typed unknown) - since the matrix is sparse, there is no need to set everything at initialization. 


- vertex domain: ☉^
- constraints:  
    - sources ⊆ ☉^ (finite)
    - targets ⊆ ☉^  (finite)
    - {R[☉_i, ☉_j] ∈ T U {_^[T]} | ☉_i, ☉_j ∈ ☉^}
- For simplicity, we assume for now T is boolean 𝔹; we will model more complex scenarios in later iterations following the generalizations introduced by the works on semiring dioids by Gondran and Minoux TODO reference, where we could model T as reals ℝ or maybe purely finite representations with rationals in ℚ. 

Take variable `웃^2` as example, in this case it would have signature R^[웃^, 웃^, 𝔹 U ◇^[𝔹]]

TODO what about the name of rows/columns of non-zero cells?



R[x,y]: the value of the cell at x,y indeces. By default return ◇[T]

▢ : empty relation      U+25A2 WHITE SQUARE WITH ROUNDED CORNERS
- sources: ☉^
- targets: ☉^
- constraints:  { (☉_i, ☉_j) = Ⓕ }
 
▇ : universal known relation  U+2587 UPPER SEVEN EIGHTHS BLOCK
- sources: ☉^
- targets: ☉^
- constraints:  { (☉_i, ☉_j) = Ⓣ  }

◇▇ : universal unknown relation  U+2587 UPPER SEVEN EIGHTHS BLOCK   TODO '?' or '_' or what ??
- sources: ☉^
- targets: ☉^
- constraints:  { (☉_i, ☉_j) = ◇ }


▢[웃^, 🏠^] : empty relation restricted to person type 웃^ and house type 🏠^ 
- sources: 웃^
- targets: 🏠^
- constraints:  { (웃_i, 🏠_j) = Ⓕ  }

▇[웃^, 🏠^] : universal relation restricted to person type 웃^, 🏠^
- sources: 웃^
- targets: 🏠^
- constraints:  { (웃_i, 🏠_j) = Ⓣ }

I: identity matrix   # TODO even if grade 2, this looks quite like the grade ☉^0 = 1 of our algebra 
- sources: ☉^
- targets: ☉^
- constraints:  { (☉_i, ☉_i) = Ⓣ | ☉_i ∈ ☉^ }

I[웃^]: identity matrix filtered to person type 웃^
- sources: 웃^
- targets: 웃^
- constraints:  { (웃_i, 웃_i) = Ⓣ } U {(☉_i, ☉_j) = ◇ | i ¬= j}

웃: a person query in the database
- sources: 웃^
- targets: 웃^
- constraints:  {(웃_i, 웃_i) = Ⓣ | 웃_i ∈ ☉} U {(웃_i, 웃_j) = ◇ | i ¬= j}

웃_k: atom identity
- sources: 웃^
- targets: 웃^
- constraints: {(웃_k, 웃_k) = Ⓣ} U {(웃_i, 웃_j) = ◇ | ¬(i = k AND j = k)}


Suppose we have an expression like 

    1 + 웃 + 웃^2

with integers coefficients. We could call the terms:

1: 웃^0: the essence of a person, with the restricted identity matrix I_웃 as underlying representation. 

웃 : an individual person, with the identity atom as underlying representation:
- sources: 웃^
- targets: 웃^
- constraints: only one cell (i,i) set to Ⓣ, where i is the particular person index. Others are Ⓕ.

웃^2 : a group of persons with some relation between them, formally representable as a matrix:
- sources: 웃^
- targets: 웃^
- constraints: none, although most of the time we can assume the number of relations |웃^2| > 0

    Important: 웃^2 should _not_ be interpreted as the identity atom 웃_i multiplied by itself (under strict relational composition calculation that would yeald again 웃_i).


웃_1 ∈ sources(웃^2)  -> Does person instance 웃_1 belongs to sources(웃^2) = 웃^  ?

웃_1 ∈ 웃^  -> is a particular person instance 웃_1 a person?



### Functions


Typing: (웃^,🐶^) -> 🏠^ = Function[[Person, Dog], House]
    
f(웃,🐶)  # a function call

Let's consider this example:

f(웃) = 1 + 웃 + 웃^2

The whole expression has to be meant as _symbolic_, so not to be immediately reduced, you can think of it as a formal power series.

f(웃) : "a function of a person"

f(웃^)   ->  function _f_ over explicit `Person` type (not instance call) TODO better specify

##### Instantiation

If we provided _a specific_ person like this:

```
f(웃 : 웃^) = 1 + 웃 + 웃^2    # definition

Alice : 웃^ = 웃^("Alice", 6, "Wonderland", ...)  # var declaration

print(  f(Alice)  )     # call
```

the substitution would lead to this autoboxed rewrite of f:

```
f({Alice} : 2^웃^) = 1 + {Alice} + {Alice}^2 
```

with the following meaning:

* `f(Alice)` : function call with Alice as parameter
* `Alice`    : the person Alice
* `Alice^2`  : Alice squared, notice this time we don't have a network of people, but something related to Alice herself (whatever it might be..)

### Operations on relations


    sources(R : Rel) : D 

Given a relation R, returns all the nodes with outgoing edges, formally  {x | ∃x: (x,y) in R}
  
    targets(R : Rel) : S

given a relation R, returns all the nodes with incoming edges, formally  {x | ∃y: (x,y) in R}


### Relation structure operations

These operations ignore link properties and produce a `Set^[(U, U)]`

* chain R1 🔗 R2: Connects matching keys (x,z) (z,y) by chaining along shared objects to produce (x,y).

* join R1 ⨝ R2: Connects matching keys (x,z) (z,y) by chaining along a shared objects to produce (x,z), (z,y) and (x,y)

* `union R1 ⋃ R2`: structural union by merging link sets (logical OR of supports). 

* `intersect R1 ⋂ S2: structural intersection by keeping common links (logical AND of supports).   

* remove R1 ∖ R2: structural difference  removes links present in the second relation (doesn't consider the values). R ∖ S = supp(R) ∖ supp(S)

* identity I: identity relation ( I = {(x,x)} ); self-mapping on a domain.


#### Link properties operations

* filter(R[rows, cols]): restricts by row/column keys (domain or codomain) TODO syntax

* flip(Rᐪ): flips along the diagonal, swapping source and target
Rᐪ = {R[y,x] | (x,y) in R} 

* complement R⎴: applies a value-level inverse (arithmetic negation, logical NOT, or complement).

* merge R1 ❒ R2: merges two relations on overlapping links using a chosen rule (e.g., max, sum, or custom merge function). Eventually we will develop an operator which performs a semantic sum, such that e.g.

    ```
    웃_1 ❒ 웃_2  -> 웃_1,2  a synthetic singular ("the two together")
    ```

    This operation for now is left vountarily underspecified and presented here only to define a symbol representation different from regular `+`

* merge v1 ❒ v2 : merges two semiring property values using a chosen rule (e.g., max, sum, or custom merge function). 

* compose R1 ❍ R2 : composes relations along a match (semiring-style "multiply–accumulate" operation).

* compose v1 ❍ v2 : composes two semiring values

* subtract R ⊟ S : value difference R[x,y] ⊟ S[x,y] (if both defined, else R)

* map()` / `apply() : applies a unary transformation to each value (e.g., scale, normalize, threshold).

* zero ⓪^[P]` / `one ①^[P] : typed identity elements of the value algebra; "empty" and "neutral" values.

* aggregate() : folds values across an axis using the value-combine rule (sum, max, count, etc.).


### Multiplication by different symbol

Multiplying two different symbols — e.g. 웃 🐶 — means forming a structure that relates elements of these domains. So:

웃 * 🐶 corresponds to a relation R ⊆ 웃^ ⨯ 🐶^

    p1 d1
    p1 d2
    p1 d3
    .  . 
    .  .  
    p2 d1
    p2 d2
    p2 d3
    .  . 
    .  .  

That is: pairs (person, dog). Each instance could mean "owns", "cares for", "prefers", etc., depending on the interpretation.

웃 🐶:	cross-composition,	relation between persons and dogs

🐶 웃:	reversed cross-composition, how dogs interact with people (may differ in direction)


**Owns relation example**

웃 🐶 ~ group of dog owners,  bipartite relation between people and dogs.

Example as a two-layer network, matrix table form:

Person nodes (웃):  😄 😎 🙂  
Dog nodes ():     🐶

| R | 🐶_1 | 🐶_2  | 🐶_3 |
|-----|------|-------|------|
|웃_1 |  x   |  x     |      |
|웃_2 |      |   x  |  x     |

Edges: according to the Relation who  / likes / walks which dog


Network graph, notice natural clusters.

```mermaid
graph LR

    subgraph Owners
        subgraph Bianco family
            O1[🙂 Alice]
            O2[😎 Bob]
        end
        subgraph Verdi family        
            O3[👨 Charlie]
            O4[👩 Lisa]
            O5[👧 Emma]
        end
    end

    subgraph Dogs
        D1[🐕 Fido]
        D2[🐩 Bella]
        D3[🦮 Spot]
    end


    
    O1 -- owns --> D1 & D2
    O2 -- owns --> D1 & D2
    O3 -- owns --> D3
    O4 -- owns --> D3
    O5 -- owns --> D3
    
```



**Character example**

```
 CAR     BALLADS

 C   B   L 
     A   D
 R       S
```


ㄕ⁰ = code point  
ㄕ¹ = character   
ㄕ² = token  

Each edge holds a word id and the sequence number. 

```mermaid
%%{init: { "flowchart": {  } }}%%
flowchart RL

  subgraph car
      direction TB
      C(["C"])
      R(["R"])    

      style car fill:#FEA ;
  end


  subgraph common
      direction TB
      A(["A"])
      B(["B"])

      style common fill:#FFB;
  end


  subgraph ballad
    L(["L"])
    D(["D"])
    S(["S"])

    style ballad fill:#FED;
  end

  B-- "w58, 1" -->A
  A-- "w58, 2" -->L
  L-- "w58, 3" -->L
  L-- "w58, 4" -->A
  A-- "w58, 5" -->D
  D-- "w58, 6" -->S

  C-- "w74, 1" -->A
  A-- "w74, 2" -->R


```


##### Multiplication associativity

TODO PROPER X ? 


Suppose 🐶 🐶 is a group of dogs, pack.

웃 (🐶 🐶) !=  (웃 🐶) 🐶      TODO NOT SYMBOL

Example:

웃 (🐶 🐶)  ~  Person caring for a group of dogs, like shelter, trainer, or breeder.

🐶 🐶 = 🐶^2 is a group of dogs, so this is a mapping:

R ⊆ 웃^ ⨯ 2^(🐶^)     # powerset

    p1 {}
    p1 {d1}
    p1 {d2}
    p1 {d3}
    p1 {d1, d2}
    p1 {d1, d3}
    p1 {d2, d3}
    p1 {d1, d2, d3}
    p2 {}
    p2 {d1}
    p2 {d2}
    p2 {d3}
    .
    .
    .


— each person associated with a set of dogs.

 
(웃 웃) 🐶  ~ e.g. family caring for one dog (or more)

R ⊆ (웃^ ⨯ 웃^) ⨯ 🐶^  


**Veterinary clinic example**

웃 (웃 🐶)  veterinary clinic, where a vet interacts with both an owner and their pet

R ⊆  웃^ ⨯ (웃^ ⨯ 🐶^)


```mermaid
graph LR


    subgraph Vets
        V1[👩‍⚕️ Dr Lee]
        V2[👨‍⚕️ Dr Kim]

    end

    subgraph Owners
        subgraph Bianco family
            O1[🙂 Alice]
            O2[😎 Bob]
        end
        subgraph Verdi family        
            O3[👨 Charlie]
            O4[👩 Lisa]
            O5[👧 Emma]
        end
    end

    subgraph Dogs
        D1[🐕 Fido]
        D2[🐩 Bella]
        D3[🦮 Spot]
    end


    V1 -- talks_to --> O1
    V2 -- talks_to --> O3

    O1 -- owns --> D1 & D2
    O2 -- owns --> D1 & D2
    O3 -- owns --> D3
    O4 -- owns --> D3
    O5 -- owns --> D3
    
```


### Reduction

웃₁ + 웃₂ MAY be reduced to 2웃 or remain "as is" depending on the context.


### Zero element

Zero representation can change according to the setting:

`setting=natural`: Zero can be liberally represented with digit `0`, ambiguities are tolerated.

`setting=formal`:  

- **unambiguous context**: zero can be represented with digit `0`:

        0 + 3웃
    

- **ambiguous context** (es. when performing algebra among different symbols):

    `0` MUST be either:  

    * followed directly by a symbol as a variable instance of the intended type, like in a multiplication:


        
            0웃 + 0🏠 
        
      
    * or followed by a colon and its type (without spaces):
        
            0:웃^ + 0:🏠^ 
        

Notice here we are only describe notational conventions, algebraic reduction is discussed elsewhere TODO WHERE?


### Unit element

**What is `1` ?** This is such a hard philosophical question we can only vaguely attempt to describe it.

`setting=natural`: 


    1 = one / a unit /  the state or essence of being / something that was gifted by a superior entity


"one" can be liberally represented with digit `1`, ambiguities are tolerated.

`setting=formal`:  

The famous Principia Mathematica Volume I by Whitehead & Russell first defines `1`... on page 379.

Alas, the short attention span of nowadays audiences requires us to provide this much shorter definition:


    1 = ⏭0  [DEFAULT]

... which lets us unsatisfied: what's that zero anyway?

_In Pictoji, `0` and `1` are  generally considered as typed._

Since even in formal math `0` and `1` can have a variety of meanings, we list here some of the well-known ones (this is just a non-authoritative literature review):

* elementary arithmetic: 1 is the number after 0
* algebra: 
    1 is the multiplicative identity  
    0 is the null element 
* set theory: 
    0 is {} the empty set  
    1 is {{}} the set containing the empty set
    

#### Identities

These equivalences SHOULD always hold:


    SYMBOL⁰ = SYMBOL^0 = 1:(SYMBOL ⨯⨯ 0)


#### Context ambiguity

- **unambiguous**: "one" can be represented with digit `1`:
  
      1 + 3웃
  

- **ambiguous**: (es. when performing algebra among different symbols), `1` MUST be either:  


    * elevated to zero, as in exponentiation:
        
            웃^0 + 🏠^0
        
        
    * or followed by a colon and its type (without spaces): TODO probably we can find better syntax
        
            1:(웃^ ⨯⨯ 0) + 1:(🏠^ ⨯⨯ 0)         
        

Notice here we are only describe notational conventions, algebraic reduction is discussed elsewhere TODO WHERE?

#### One interpretation

 `1` meaning can vary among `role` modes. 
 
 Given a `1` of type `SYMBOL^`, treat `1` as:

- `role=phd`: a pure mathematical object, selecting the proper mathematical type SYMBOL^ according to the context.

- `role=creative`:  the zeroth element of a hierarchy starting at `SYMBOL^0`, following this definition:

    `1 = SYMBOL^0` ~ the state or essence of being / something that was gifted by a superior entity

    If there is no meaningful enough candidate (or if we are already at the bottom of the hierarchy), use `role=phd` as fall-back.

    Examples: 

    `1:(웃^ ⨯⨯ 0) = 웃^0`  ~ personhood, persona, the archetype of sentience  
    `1:(🏠^ ⨯⨯ 0) = 🏠^0` ~ dwellingness, the concept of shelter  
    `1:(🙂^ ⨯⨯ 0) = 🙂^0` ~ happiness, the state or essence of being happy 
    
- `role=technician`: 

    * if there is a defined hierarchy in the context (like 웃, 🏠, ...):

        the zeroth element of a hierarchy starting at `SYMBOL^0`

    * otherwise:
    
         try deriving the meaning in a way grounded in common sense. If none can be found, use `role=phd` as fall-back.


### Polynomials

Suppose we have a symbol `S`, this notation represents the polynomial of `S`


    P(x) =  a₀ S⁰ + a₁ S¹ + a₂ S² + a₃ S³ + ... + a_n S^n 


For example, if `S = 웃`, a polynomial could be:

    P(웃) =  9 + 15웃 + 7웃² + 18웃³

**Power series**: a polynomial where `n` tends to infinity.

In `role=phd` and `technician`, the meaning of a power series in variable _x_ is  

P(_x_) -> hierarchical model of _x_

- Formal power series are not necessarily meant to be calculated, kind of like in Analytic Combinatorics
- need to specify a _distribution_
- queries potentially can materialize many individuals with weighted relations (to represent a noisy world)
- meaning search is two-level:
    - from expression analysis alone
    - emergent from complexity via network clustering, e.g. centrality, etc.


Examples: 

P(웃) -> social hierarchy model 

P(🏠) -> human settlement hierarchy model

### Polynomial coefficients

TODO MUST support [Philosophy use case](#8-philosophy)

Polynomial coefficients can be used to model the weight of a particular component.

For comparison and interpretation purposes, weights SHOULD be normalized in the range `0.0` - `1.0` such that:

$∑ a_k = 1.0$

### Integer coefficients

TODO MUST support [Story generation use case](#story-generation)

Everyday users tend to think in single quantities (웃 is 1 person), while db languages and relational math usually represent things in vectors. To solve the mismatch, query variables could be interpreted as representing a quantity of `1` by default and sample building / LIMIT clause is implicitly created by means of coefficients, e.g.  `3웃` selects three different persons from the db. 

- need precise quantities
- single based values
- queries materialize few individuals and edges with weights on a simplified scale (e.g. heavy / soft / none link)


TODO JUST A SKETCH, need clone operator and constraint-solver layer to prevent weirdness

웃^ = {웃_1, 웃_2, ....., 웃_n}   Person type, also denotes _all_ people from the database (possibly a lot but still finite)

- 웃 acts as a query variable which ranges over 웃^

- Different appearences of 웃 in a fully reduced expression mean different persons:

        웃 + 4웃 - 2웃 = 3웃     3 different persons to instantiate

웃 ∈ 웃^  valid from a user point of view with ∈ semantics overloaded so it works even if internally the query engine will autobox, see below

웃 k-> {웃} autoboxing if 웃 can be proven to have cardinality 0 or 1

웃 + 웃 -> 2웃

2웃 k-> {웃_i, 웃_j}  selects two _different_ random people indexed i, j from the database 웃^ set

웃_1 + 웃_4 k-> {웃_1, 웃_4} selects exactly 웃_1 and 웃_4 from the database 웃^ set (TODO what if they are not inside?)

3웃_7 k-> {웃_7, 웃_n+1, 웃_n+2}   generates two new fresh instances (thus with different ids) copied from original 웃_7

웃_7 + 웃  k-> {웃_7, 웃_i} -> selects person at index 7 and a person i _at random_ from 웃^ set and person 웃_1.  If i = 7, generate new fresh id for the duplicate.

웃_1 + 웃_1  -> 2웃_1    selects two copies of person 웃_1, second copy gets a fresh id


웃 🐶 ->  exactly 1 group of e.g. dog owners

웃^ X 🐶^ = all possible groups of e.g. dog owners in the database

3 웃 🐶 -> exactly 3 _different_ groups of e.g. dog owners

(웃 🐶)_7 + (웃 🐶)_3   -> selects group at index7 and group at index 3 from large all dog owners query 웃^ X 🐶^ (TODO define sorting method later)

웃 3🐶 -> 3 웃 🐶   3 groups of dog owners (as much as I would like to mean something like 1 person for 3 dogs, following standard algebra rules seems the best route..)

3웃 2🐶 -> 6 웃 🐶    6 groups of dog owners

### Equations

TODO SHOULD support [Graffiti art](#story-generation) use case.

The quest would be to have expressions generate types which are totally different from their initial types: if done directly it would bork the algebra, still we can envision some way to use the database to 'influence' and bend the results. 


### Probability

To express probabilities we use type operator `^` in symbols to distinguish from polynomials:  

* Probability that `Person` = person (notice capitalization):
    
      P(웃^ = 웃) 
    
* Probability of `Person`:
    
      P(웃^) 
    

### Pluralities union

    TODO using ₓ (letter x) as subscript is a stretch


    Possibly infinite:

    ```
    웃웃  ⋃  🏠🏠 ->  {웃₁, 웃₂, ... , 🏠₁, 🏠₂, ...}
    ```

    Finite:

    ```
    2웃  ⋃  3🏠 ->  {웃₁, 웃₂, 🏠₁, 🏠₂, 🏠₃}
    ```

Powers union:


    웃^2  ⋃  🏠^3 -> {웃₁ₓ₁, 웃₁ₓ₂, 웃₁ₓ₃, ..., 웃₂ₓ₁, 웃₂ₓ₂, 웃₂ₓ₃, ..., 🏠₁ₓ₁ₓ₁, ... }  



### Computational model

> _Venkman_: So it's a haunted computer that speaks in broken emoji and crashes reality?  
> _Egon_: Sort of.

MUST support the [Computational thinking use case](#computational-thinking) 

Each computer 🖥 is a Term Rewriting System (TRS) that: 

- decides its own rewrite strategy 
- has typed term rewriting functions which operate at symbolic level 
- functions are defined with signature and patterns in a 4 spaced block
- when pattern matching is not exhaustive, the rule f(_, _, ...) -> ↂ is implicitly added
- patterns may have guards
    - guards never rewrite the main term, they only decide if a rule may fire
    - dumb / low-level computers: 
        - guards are pure structural predicates
        - total functions on ground terms
        - must not look at AI-style context
    - smart / high-level computers: 
        - guards may be symbolic tests delegated to other computers
        - may return error ↂ
        - may look at context
        - rule applicability then depends on strategy

Overall:

- TRSs are not optimized for performance
- explainability and clarity are key
- if performance / handwaving is needed, it can be modelled as functions called in other computers 
- other computers are mostly intended as black boxes
- caller computer may have debug / inspection power but most likely won't use it

<details>
<summary>CLICK HERE for technical raferences jargon </summary>
- many sorted TRS
</details>

#### Rule Evaluation Model

**Goal**: model term unification with semiring matrices as a possible test of fitness of the whole Pictoji algebraic machinery. At this stage this is just a purely conceptual model sketch, we don't aim at any particular implementation. Reference: [Sato](#sato) 
A pictoji rule lowers to a monotone operator over dynamic relations.

The effect of rule application on the current domain corresponds to a sparse-matrix operator, obtained by:

- aligning axes of predicate matrices according to variable sharing
- joining them via matrix multiplication under the boolean (or chosen) semiring
- masking them by equality/disequality constraints
- projecting onto head-argument axes
- unioning with the existing head relation

**Search** = the least fixpoint of the union of all rule operators, i.e. the closure under powers of the combined adjacency operator.

**Dynamic-domain behavior** (term creation and node unification) modifies the shapes of all relations between fixpoint iterations but does not alter the matrix-power semantics of each iteration.

TODO example

#### Computational tower

Pictoji execution is modeled in a cluster of computers 🖥, each represented as 🖥^level 

🧿🖥 = current computer where the computation occurs
Ϟ = grade(🧿🖥) = the current computer level   TODO CHANGE SYMBOL

- Each level has its own notion of computability
- the AI choses the appropriate abstraction level necessary to model the problem at hand.
- The user provides the initial resources and (ideally) should have complete access to all the underlying data structures and hardware.

Formally:  🖥^m may only operate on ☉^n objects where n < m

🖥^0   : (substrate collapse)  
🖥^1   : physical machine  
🖥^2   : operating system
🖥^3   : language runtimes (e.g. python) / tools  
🖥^4   : orchestrators / sandboxes / container-level control  
...
🖥^n   : AI model (`CURRENT_AI`-level evaluator)  
🖥^n+1 : user / external initiator  

From a theoretical point of view, Pictoji should strictly prevent problems related to infinite computations, logical paradoxes, etc, while keeping the user interface simple.

First powers of objects in the database can be seen from an informatics point of view like this:

☉^0 : single unicode graphemes / hardware born stuff (IEEE floating point numbers / pointers as numbers)  
☉^1 : 'stand alone' records, i.e. pointers are just detached ids  
☉^2 : if managed by existing language runtime: cycles are allowed as in real life programming
      in Pictoji: only finite inductive structures (proper records, finite sequences of ☉^1  (strings, lists, big numbers, ..)  

P(☉) = the free inductive algebra requiring acyclicity. TODO REVIEW, ALSO SHOULD PROBABLY GO INTO DATABASE POLYNOMIAL SECTION

Examples: 
- a Python interpreter (🖥^3) cannot understand a, say, an hypothetical "semantic graph of logical forms" at  ☉^6 unless encoded downwards.
- `CURRENT_AI` (🖥^n) can manipulate enough symbolic levels to interpret arbitrarily complex ☉ layers.

- 🖥^k itself is stored as a finite record in ☉^(k)
- Same-level agents communicate by leaving structured data in the shared lower-level substrate.
- A higher-level evaluator schedules when each agent runs.
- Each agent uses only its own resource budget provided by its parent evaluator.

This allows things like introspection, simulation, meta-analysis, embeddings, serializability

Example of AI Resources:  TODO JUST A SKETCH, REVIEW

```
    ctx_tokens_left     ~   100k   (effective max)
    gen_tokens_left     ~   8k–16k per reply
    tool_calls_left     ~   small finite integer
    tool_time_left      ~   30–60s per tool run
    internal_steps_left ~   fixed by network depth (~80–120 layers = 1 step)
    db_quota            ~   small slices
```

#### Agent interpretation

- an agent reaching ↂ is a collapse of their interpretive resources
- but a higher-level agent can treat that collapse as data, not failure

Example for 웃 (not normative):

☉⁰ = raw percepts ("they shouted", "he ran")  
☉¹ = simple roles ("group", "individual", "helper")  
☉² = events with internal structure ("action performed on X")  
☉³ = social scripts ("ask for help")  
☉⁴ = social norms, game-theoretic constructs  
☉⁵ = narratives, psychological states  

- A person becomes overwhelmed -> collapse
- A friend sees the situation clearly -> no collapse for them
- A psychologist sees the whole system even more clearly

Resources for 웃^1 are psychological / relational capacities: like attention, emotional energy memory, social bandwidth, tolerance...


### Execution examples

🖥^1: Calculates head down until a result or eventual exhaustion when a system error 🖥ↂ is raised, which collapses all stuff calculated so far into a 🖥ↂ

    √2 -> 🖥ↂ

🖥^2: can do some basic resource cost estimation, does its best to stay within limits and will properly signal a stop by returning an error with a partial result as argument filled with ↂ, like:

    √2 -> ↂ( [1,4,1,4,2,1,3,ↂ] )

🖥^3: looks at the _context_, considers if there is actual need to perform the computation, e.g.:

    √2 * √2 -> 2

🖥^4: can perform clever rearrangements to improve the performance of the calculations, and judge whether to stop at an appopriate symbolic level e.g.

    2^(-x/3) * 2^(-x/6) -> 2^(-1/2)x -> (√2)^x

🖥^5: smart - recognizes high-level problems, understands user expectations,  may produce an appropriate refusal to proceed.

    "Does the 3n+1 problem always goes to 1 for any n?" 
    
    -> ↂ("This is the Collatz Conjecture. Nobody knows yet (as of Dec 2025).")



### Placeholders

> Every so-called mystery is a question we stopped asking -- _Frank_

#### Unknowns

For every type T there exists a canonical unknown value:

◇[T] : T

◇[T]^n : T ⨯⨯ n  unkown of grade n as power/hierarchy structure

Surface shorthand:

- when a value of type T is expected, you may write bare ◇ and it means ◇[T] (type inferred)
- whenever a ஃ[T] is expected, ◇[T] is implicitly autoboxed to {◇[T]}
- coercion from ◇ to/from  ◇[Bool] is allowed; all other ◇[T] are not logical
- ◇ is ◇^1 so cannot be used where ◇^n with n ¬= 1 is expected
- type must be inferable from the immediate syntactic context without reduction or database access
- `parsing_mode=strict`: if T is not inferable, reject

See [Logic chapter](#logic) for ◇ : Bool behavior


Example:

```

let b : Bool = ◇     # parsed as ◇[Bool]

f(x : Bool ⨯⨯ 2) -> Int:
    f(◇^2) -> 9                    
    f({(T,T),(T,◇),(◇, F)}) -> 7   
    f(err : ↂ[Bool] ⨯⨯ 2) -> ↂ[Int]("You messed up!")   # explicty handles error

# Call tests:
f(◇) -> ↂ[Int]^1     # invalid grade: ◇ = ◇^1 
f({(T,T)}) -> missing case, defaults to ↂ[Int]^1
f("Hello") -> bad type, defaults to ↂ[Int]^1
f(ↂ^1) -> ↂ[Int]^1   # missing other cases, defaults to error of output grade (downgraded)


g(u: ◇^) ->  Int ⨯⨯ 2:
    g(◇ : Bool) -> {(3,1), (9,4), (5,7)}    
    g(◇ : Int) -> {(6,5)}

# Call tests:    
g(◇ : Int) -> {(6,5)}
g(◇ : Str) -> ↂ[Int]^2   # missing case, defaults to error 
      g(ↂ) -> ↂ[Int]^2   # missing case, defaults to upgraded error 
    g(ↂ^3) -> ↂ[Int]^2   # missing case, defaults to downgraded error

```

#### Errors

For every type T there exists a canonical error value (optionally carrying payload):

ↂ[T] : T

Optional structured error type:

```
ᛠ ↂ^[T]:
    🏷 : str    label for the error
```

Constructor:  ↂ("Too bad!")  yields  ↂ^[T]("Too bad!") with T inferred 
- `parsing_mode=strict`: if T cannot be uniquely inferred, ↂ("msg") is invalid.

- See [Computational tower](#computational-tower) for system-level constraints (🖥ↂ) and error propagation rules.


ↂ[T]^n : T ⨯⨯ n   error of grade n as power/hierarchy structure, you can imagine higher graded errors as having a hierarchical chain of stacktraces within them.

For k >= Ϟ typed errors ↂ^[T] ⨯⨯ k are not constructible; the system yields 🖥ↂ^Ϟ instead.


For any declared function type f : A1, A2, ..., An -> B (and operator OP) the kernel:

- treats f as totalized to:    `f : (A1 ∪ ↂ^[A1]), ..., (An ∪ ↂ^[An])  -> (B ∪ ↂ^[B])`
- if any operand is ↂ:*, by default returns ↂ:B and no further reduction is performed
    - exception: if the error grade is lower than the computer level Ϟ, the function can pattern match on it to catch it.
- Errors dominate unknowns: ↂ overrides ◇



##### Computer errors

🖥️ↂ is a computer error which can only be raised by the system 

```
ᛠ 🖥️ↂ^[T]:    
    🖥️ↂ^[T] ⊂ ↂ^[T]   # inherits properties
```

Example:  🖥️ↂ^[T]("Out of memory!")

Operations in a computer are subject to implementation-defined resource limits (time, memory, sample count, maximum path length, etc.). 
- If a computer at level `n` evaluates a computer function of codomain `T` which would exceed these limits, that access yields a level n computer error of type  `🖥️ↂ^[T] ⨯⨯ n` instead of a partial or infinite result. 
- when database resources are exhausted, a computer error of type  `🖥️ↂ^[T] ⨯⨯ n`  is automatically returned from every function or operator call
- Since a computer can only access objects to a level beneath its own, it won't be able to pattern match on system errors generated at its own level, but it can still catch any error ↂ^m with m < n generated by lower levels. It can also raise and catch ↂ^m errors on its own.

### Suspensions

ᛠ ⏸^[T] = a suspended computation that would produce a `T` if forced


- error conditions are reported here for extra clarity but should follow from general rules 
- no rewrite path can turn a ↂ^k with k >= Ϟ into a value of type ⏸^[T]

Pause: ⏸ given an expression does nothing. 

    grade(⏸(x)) = grade(x)

    ⏸( x: ㉫) -> ⏸^[㉫]:
        ⏸(🖥ↂ^k) , k >= Ϟ -> 🖥ↂ^k    # system level rule
        ⏸(ↂ^k) ,   k >= Ϟ -> ↂ^k      # system level rule

        ⏸(x)     -> ⏸(x)

Play: unwraps a paused ⏸ computation, which is going to be later executed by the system

    grade(▶(x)) = grade(x)

    ▶( x: ⏸^[T]) -> T:
        ▶(⏸(x))  -> x     # unwrapping
        ▶(◇[⏸[T]]) -> ◇^[T]
Example:

    ⏸(x + y / 0) -> ⏸(x + y / 0)           # nothing happens

    ▶(⏸(x + y / 0) ) -> x + y / 0 -> ↂ    # BOOM



## Vocabulary 

> The last thing we need is a semiotic scandal -- _Venkman_

- **Minimal, visual, intuitive**: prefer clarity over compression. Chosen symbols should be recognizable at a glance. Prefer visually simple symbols; avoid sequences that are hard to distinguish at small sizes.
- **Literal-by-default**: If a Unicode character's official English name matches the concept, prefer it. As an exception: high-frequency function words (auxiliaries, modals, determiners, pronouns, logical/relational operators) may use abstract symbols from math/operators/arrows/geometric blocks without special marking.
- **Name conflicts**: If a symbol choice risks confusion with its Unicode name, choose another even if longer.
- **Abstract vs concrete**: abstract symbols (math operators, arrows, etc) are considered safe for abstract meanings, emojis are used for concrete objects, actions, or emotions.
- **Character sets**: If no emoji/math symbol exists, search in Greek, Cyrillic, CJK, Arabic, Devanagari, etc. and pick something with a close English name or, as fallback, a visual representation that reminds the intended meaning even if native meaning diverges (especially if selected from a set not spoken/understood by many people).
- **Ambiguity avoidance.**:
    - Do not assign the same symbol to two active lexemes. If a symbol's Unicode name collides with a different lexeme already in the spec, pick another symbol.
    - If a concept collides with another (e.g., 📍 as "place" vs "where"), prefer an unambiguous alternative (⌖ for place, 📍 only for where).
- **Frequency priority**: 
    - Follow COCA model. 
    - Define HIGH_FREQ_WORDS as the first 200 highest frequency words 
    - For very frequent English words (be, have, do, will, etc.), allow assigning a symbol even if its Unicode name does not match literally, to avoid verbose expressions.


#### Examples

- Concept "some": No emoji, no obvious Unicode character. Use abstract math circle fraction: ◔

- Concept "a being": Instead of ambiguous "person" use  ▫ ↻⟡  as literal "a being"

- Concept "I have been working.":

Build by rules:

👤 (I) + ⊸ (have) + ↶⟡ (been) + ↻⚒ (working).

Result:

👤 ⊸ ↶⟡ ↻⚒.



### Modifiers

- ↶ attaches to verbs or auxiliaries to mark past
- ↻ attaches to ⟡ to mark progressive
- ↻ attaches to any verb (not only "be") to mark progressive aspect ("-ing" form: doing, going, working, etc.)
- ¬ attaches to auxiliaries to mark negation
- Comparison uses ▲ / ▼ as prefixes
- Plural is represented by duplication of the noun glyph (🏠 -> 🏠🏠)
- **Opposites**: Given a SYMBOL (e.g. 🙂), when there is an obvious candidate for the opposite, choose that one (e.g. 🙁). Otherwise write ¬SYMBOL without spaces

#### Special handling of "be"

⟡ = be in all forms. Always explicit:  
↶⟡ = was  
↻⟡ = being  
⊸ ↶⟡ = have been


### System terms

ㄕ🗿 = Pictoji  
㉣ = specs  
ㄕ = symbol  
🗿 = emoji  
ᕉ = hypotesis    
🖥️ = computer
Ϟ = current computer grade  
🧪 = test  
⚛ = atom

ᛠ = type  
⁋ = property  
ᕟ = variable  
ᕓ = value  
㉫ = expression  
ꕷ = schema  
Ɗ = database / db      
𝔹 = bool      TODO Bool with capital??   
ℕ = natural   TODO Natural with capital??   

ↂ = error  
◇ = unknown   looks also kinda as a warning  

🀛 = collection  
⧢ = sequence  
🗾 = map  
⚙ = function  

We start the hierarchy from an informatics point of view.

ㄕ⁰ = code point                      Unicode numeric identifier (U+XXXX)    
ㄕ¹ = character / grapheme cluster   Symbol with meaning (may map to 1+ code points in rendering)  
ㄕ² = morpheme / token               Morphemes derive from humans semantics, tokens from statistical inference  
ㄕ³ = word  
ㄕ⁴ = phrase  
ㄕ⁵ = clause  
ㄕ⁶ = sentence  
ㄕ⁷ = discourse / document            Organized flow of sentences  
ㄕ⁸ = treatise  
ㄕ⁹ = corpus   
ㄕ¹⁰ = discipline   

P(ㄕ) = culture  
🔤 = ㄕ³


`a` → 1 character, 1 grapheme

`á` → 2 characters ('a' + combining acute accent), but 1 grapheme

`👩‍🚀` → 5+ characters (woman + zero-width joiner + rocket emoji parts), but 1 grapheme


ϡ⁰ = phonetics  
ϡ¹ = phonology / graphemics  
ϡ² = morphology  
ϡ³ = orthography  
ϡ⁴ = semantics / vocabulary / lexicon  
ϡ⁵ = grammar / syntax  
ϡ⁶ = pragmatics   understanding context
ϡ⁷ = rhetoric     the art or persuasion  
ϡ⁸ = philosophy  
ϡ⁹ = sentient being  / consciousness     awareness of reflection, language recognizing itself as being  

P(ϡ) = language  


ϡ = ϡ¹  
𑁍 = sentient  
𑁍 ↻⟡ = ϡ⁹
🔠 = P(ϡ)  
 
 
### Body

🧍 = body  
✋ = hand  
😶 = head  
♥ = heart (≠ ❤ love)  
👄 = mouth  
🦶 = foot  


### Nature

🥣 = food  

⛰ = earth / ground  
💧 = water  
🔥 = fire  

☁ = sky  
☀ = sun  
🌙 = moon  
⭐ = star   

☥ = life  

🌱 = sprout  
🌱¹ = sprout  
🌱² = grass  
🌱🌱 = sprouts  

🌿 = natural plant  
🌿¹ = natural plant  
🌿² = vegetation   
🌿³ = field   

🌾 = cultivated plant (of a crop)  
🌾¹ = cultivated plant (of a crop)   
🌾² = crop   
🌾🌾 = cultivated plants (of a crop)   


🌳 = tree   
🌳¹ = tree  
🌳² = forest   
🌳🌳 = trees   

🌴 = palm  
🌴¹ = palm  
🌴² = jungle (don't care if it a proper jungle is made by several types of trees)  
🌴🌴 = palm trees   

🐶 = dog
ဗ = animal

### Things


⌖ = place  
📖 = book  
📄 = paper  
📱 = phone  
🧩 = problem  


### Verbs

✇ = use  
⩕ = mean  
⤋ = put / set / place     [ARROW] when unicode allows, 
﹄ = let / allow  
﹄ 👤👤⁀ = let's     (let us)  
🏳 = begin / start  
🏁 = end / finish  
⧇ = keep / stay  
🤜 = move / push  
⚒ = work  
🛠 = make  
👀 = see     
👀 ↦ = look at  
📚 = know  
💭 = think  

💬 = say / tell (content)                
🗣 = speak / tell (to someone) / talk    
📢 = call / shout / announce              
🏷 = name / label                        

☺ = like  
❤ = love (U+2764 bare version)  

✦ = want  
⊞ = need   TODO don't like the plus  

△ = try  
🔎 = find  

🤏 = get  
✊ = take  
👐 = give  
🏃 = go  
👈 = come  
↘ = leave  
⏢ = help  
🍴 = eat  
🍷 = drink  
✺ = show   
⤞ = bring   
📨 = send   
⊍ = open   
⍝ = close   
⚡= happen  
💓 = feel  
㉦ = ask  

### Testing vocabulary

📡 = contact  
👨‍💻☯ = CoderDojo  
㊷ = the Answer to the Ultimate Question of Life, the Universe, and Everything  


### Copula and auxiliary


⟡ = be / am / is / are / was / were / been / being  
⟡⟡ = plural be  
↶⟡ = was  
↶⟡⟡ = were  
↻⟡ = being  
◐ = do / does  


〽 = already       TODO find something else


### Determiners

▫ = a / an  
▪ = the
㉤ = any  
⊡ = each  
으 = only  
⛉ = just  
⛊ = such  

### Adverbs

۞ = well  


### Negation / Validation

¬ attaches to auxiliary or modal  
Example: ◐¬ = don't, ↶◐¬ = didn't

⟡¬ = isn't / aren't
◐¬ = don't  
🚫 = no        determiner / clausal negation clash with no, none [OVERRIDE]  
👌 = ok/yes  
✅ = good  
❌ = bad  
🙂 = happy  
🙁 = sad   


### Tense and aspect

↶ attaches to verbs for past        [ARROW]
⊸ = have  
⊸ ↶⟡ = have been  
⊸ ↶⟡ ↻VERB = have been doing  

### Modals

◐ = do   
◐¬ = don't   
↶◐ = did   
↶◐¬ = didn't  

◉ = can   
◉¬ =  cannot   
↶◉ = could  
↶◉¬ = couldn't  

⇗ = will                       [ARROW]  
⇗¬ = won't                     
↶⇗ = would   
↶⇗¬ = wouldn't  

⬈ = shall                       [ARROW]
⬈¬ = shan't   
↶⬈ = should  
↶⬈¬ = shouldn't  

◆ = may   
◆¬ = may not  
↶◆ = might  
↶◆¬ = might not  
◆⟡ = maybe

⤊ = must                                       [ARROW]
⤊¬ = must not  
↶⤊ = must (past)  

↶⬈ ⊸ ↶⟡ ↻VERB = should have been doing  
⇗ ⊸ ↶⟡ ↻VERB = will have been doing  
↶⇗ ⊸ ↶⟡ ↻VERB = would have been doing  

### Math - Computer Science vocabulary

> Look, if we want to sell this thing, we can't sound like we swallowed a textbook.   _Venkman_

Pictoji MUST be for the people:

- Computer Science (CS) jargon SHOULD be translated so non-STEM users understand it
- Math jargon SHOULD be translated so programmers understand it
- Explanatory translations in specs MUST be hidden in `<details>` dropdowns like this:

<details>
  <summary><strong>CLICK HERE to see Pictoji Math / CS Jargon  </strong></summary>  
<br>

**Pictoji Rosetta Stone**

*CS*
- environment -> stage
- process     -> actor
- code        -> script
- programmer  -> director
- reified     -> materialized

*Math*
- atom    -> brick       as in legos..  Examples: c 3 [] {} 웃 (as a variable)
- closure -> full build
- to lift -> to box
- monad   -> pipeline

</details>


#### Logic

☍ = relation  
ꔆ = graph / network  
ꔅ = group  
Ⰰ = hierarchy  
¬ = not      determiner / clausal negation clash with no, none [OVERRIDE]  
∿ = approximated complement (different from 'about')  property: ∿∿x ¬= x  
Ⓣ = true  
Ⓕ = false  
⊤ = top  
⊥ = bottom  
= = equal, same     
≠ = different  
◈ = constant  

⇒ = implies        [ARROW]   

⸮ = if  
⇨ = then           [ARROW]  
⤳ = so / therefore  


#### Quantifiers

∃ = exists / there exists      formal only; tenseless; negation and time apply outside/adjacent to the existential (¬ (∃ X), ∃ X ➲ T). Interpret existential / spatial as needed [setting=formal][OVERRIDE]  

☞ ⟡ = there is / there's / there are       natural language existential; carries tense/aspect/negation on ⟡; ☞ alone remains deictic "there". Interpret existential / spatial as needed [setting=natural][OVERRIDE]   


∀ = all / every  
◳ = part    
◫ = few  
▥ = many / several   
▩ = much  
█ = very  
⊜ = enough   
⚯ = too  
౮ = also  
⍠ = both  

⛞ = length  

#### Numbers

0 = zero  
1 = one  
2 = two  
3 = three  
4 = four  
5 = five  
6 = six  
7 = seven  
8 = eight  
9 = nine  
° = ordinal marker   

sum = ∑

#### Relations

∈ = in / belongs  
⊂ = strictly included, LR       `setting=natural`: ignore the 'strictly', prefer over ⊆, i.e. many bungalows ⟡ ⊆ in the resort   `setting=math`: keep the strict meaning, A ⊂ B  A is a strict subset of B  
⊃ = strictly include, RL        `setting=natural`: ignore the 'strictly', prefer over ⊇, i.e. the resort ⊃ many bungalows   `setting=math`: keep the strict meaning, i.e. A ⊃ B    "A is a strict superset of B" 
⊆ = included / subset of, LR        
⊇ = include / superset of, RL          

⁐ = out  
⊣ = because  
◒ = over  
◓ = under  
ၐ = around  
◙ = on  
◘ = off  
⨯ = by  
⚮ = between  


#### Conjunctions

∧ = and  
∨ = or  
⋃ = union  
⋂ = intersection  
⨝ = join  
⦶ = compose  
❒ = merge  
⚞ = since  both temporal preposition and causal conjunction [OVERRIDE]  
🌓 = but  
⌇= though / although  

#### Comparison

▲ADJ = more ADJ/ADV  
▼ADJ = less ADJ/ADV  
⊳ = than  
▲▲ = most  
▼▼ = least  


### Prepositions

⎋ = from  
ㅱ = away  
↦ = to / toward / as infinitive       [ARROW]  
⊶ = of  
⚭ = with  
㊅ = as      use it also in as ADJ as   [OVERRIDE]  
➲ = at  
∻ = through  
⟴ = across  
🆚 = against  



#### Adjectives

ჾ = own  
⬣ = big  
᠅ = little / small  
⌔ =  near  
▽ = far  
≣ = long  
▃ = short  
🆕 = new  
⌛ = old  
⋏ = high   
⋎ = low   
🐣= young   
✪ = important   
⧊ = difficult   
⬭ = easy
  
strong = 💪  
weak = ︵

💪 = strong
︵ = weak

#### Interrogatives

? at the end


山 = what     
⚇ = who  
📍 = where  
⏰ = when  
Ϣ = why  
⏣ = how  
❖ = which  

##### Interrogative Clitics

Form: SYMBOL ⟡/⊸ = INTERROGATIVE's 

山 ⟡ = what's  
山 ⊸ = what's  
⚇ ⟡ = who's  
⚇ ⊸ = who's  
📍 ⟡ = where's  
📍 ⊸ = where's  
⏰ ⟡ = when's  
⏰ ⊸ = when's  
Ϣ ⟡ = why's  
Ϣ ⊸ = why's  
⏣ ⟡ = how's  
⏣ ⊸ = how's  
❖ ⟡ = which's     rare, awkward  
❖ ⊸ = which's     rare, awkward  


#### Compound forms

- Compund forms are created by joining the symbols they use, without spaces.
- We place them here for completeness but they should all be derivable just from the rule. 

◔1 = someone   
㉤1 = anyone  
🚫🧍 = nobody  
∀🧍 = everybody  
∀📍 = everywhere  


◔☉ = something  
㉤☉ = anything  
🚫☉ = nothing  
∀☉ = everything  

▫⇄ = another  
▲◒ = moreover  

∈↦ = into  
◙↦ = onto  

⚭∈ = within 
⚭⁐ = without  


#### Directionals and links

~ = about   isomorphic to / homotopy equivalent / similar. Common in algebra, topology, category theory  
↑ ↓ ← → = up, down, left, right          [ARROW]  
⇢ = after                               [ARROW]  
⇠ = before                              [ARROW]  
➡ = way                                [ARROW]  
⇄ = other                               [ARROW]  
‖ = even  

### Time

⏳ = time  
⏱ = now  
🕒 = hour  
📅 = day  
▓ = week  
🗓= year  
🌃 = night  
🌅 = morning / morrow  

#### Frequency 

✴⁰ = never   
✴¹ = ✴ = once  
✴² = seldom / rarely   
✴³ = sometimes   
✴⁴ = often   
✴⁵ = always  

✴✴ = twice / two times   
✴✴✴ = thrice / three times  

#### Change

🧘= still

∆ = difference

∂⁰ = impetus  
∂¹ = velocity / rate of change  
∂² = acceleration  
∂³ = surge 
∂ = ∂¹  

↠ = become  
⏺ = record  


#### Ordering

⏩ = forward  
⏪ = backward  
⏭ = next  
⏮ = previous / back  

When uncertain about how to express a word which has natural "successor of / predecessor of SOMETHING" meaning, prefix SOMETHING with ⏮️ / ⏭️ without spaces.

Example:

⏭📅 = tomorrow  
⏮📅 = yesterday  

⏮⏳ = past  
⏭⏳ = future   

If in doubt, try compound forms, example:

↦📅 = today   DO NOT bother about it being a hack [OVERRIDE]  
↦🌃 = tonight DO NOT bother about it being a hack [OVERRIDE]  

When there is a clear progression about some MEASURE, use  ⏪/⏩MEASURE  without spaces

Example:

⏪⏳ = soon  
⏩⏳ = late  
▲⏪⏳ = sooner  
▲⏩⏳ = later  





#### Loops

⎔  = finite  
¬⎔ = infinite  
↻ = loop / cycle / recursion    TODO maybe overloading with -ing actually fits  
∽ = while   
㊐ = for       use same word for benefactive/purpose/duration [OVERRIDE]    
⌢ = during  
⧘ = until  

▶ = play  
🏃 = go  
▲🏃 = run   
⏹ = stop  
⏸ = pause  
🔁 = again

### Humans

웃 = person  

웃¹ = person   
웃² = people / crowd   
웃³ = society   

웃웃 = persons  
2웃 = a couple (of persons)  

🧒 = child  
🧑 = adult  
🤝 = friend  
👥 = partner  

♂ = male  
♀ = female  
👨‍👦 = son  
👩‍👧 = daughter  
father = TODO
mother = TODO

#### Settlements hierarchy 

🏠 = house   
🏠¹ = house   
🏠² = village  
🏠³ = city   
🏠⁴ = metropolis   
🏠⁵ = state/province   
🏠⁶ = country / nation  

🏘 = 🏠²    
🏙 = 🏠³    
🌆 = 🏠⁴    
🗺 = 🏠⁵    
⚐ = 🏠⁶    

🌐 = world  

🏠🏠 = houses   

##### Specific groups

🏢 = company (dedicated Unicode: "office building")   
🏛 = institution (Unicode: "classical building")  

### Pronouns and Deictics

English has some inherent ambiguities,  either for historical reasons ("it" is both pronoun and object pronoun) or gender debates ("they" is now both singular pronoun for unspecified gender and plural). 

- To solve the conundrum, Pictoji overspecifies some cases, leaving the context to decide which is best to use. 
- If no context is available, use symbols marked as [DEFAULT].


🧿 = self  
🧿🧿 = selves  

👤 = I   
우 = you
👨 = he   
👩 = she  
Ə = they     singular, gender-neutral  
🔹 = it      [DEFAULT]  
👤👤 = we   
ƏƏ = they    plural [DEFAULT]  

#### Verb Clitics

Form: PRONOUN_SYMBOL VERB_SYMBOL = PRONOUN'CONTRACTED_VERB

👤 ⟡ = I'm  
우 ⟡ = you're  
👨 ⟡ = he's  
👩 ⟡ = she's  
Ə ⟡ = they're    singular, gender-neutral  
🔹 ⟡ = it's  
👤👤 ⟡ = we're  
ƏƏ ⟡ = they're    plural [DEFAULT]  

👤 ⊸ = I've  
우 ⊸ = you've  
👨 ⊸ = he's  
👩 ⊸ = she's  
Ə ⊸ = they've    singular, gender-neutral  
🔹 ⊸ = it's  
👤👤 ⊸ = we've  
ƏƏ ⊸ = they've    plural [DEFAULT]  

👤 ⇗ = I'll  
우 ⇗ = you'll  
👨 ⇗ = he'll  
👩 ⇗ = she'll  
Ə ⇗ = they'll    singular, gender-neutral  
🔹 ⇗ = it'll  
👤👤 ⇗ = we'll  
ƏƏ ⇗ = they'll    plural [DEFAULT]  

👤 ↶⇗ = I'd  
우 ↶⇗ = you'd  
👨 ↶⇗ = he'd  
👩 ↶⇗ = she'd  
Ə ↶⇗ = they'd    singular, gender-neutral  
🔹 ↶⇗ = it'd  
👤👤 ↶⇗ = we'd  
ƏƏ ↶⇗ = they'd    plural [DEFAULT]  


#### Object pronouns 

Form: PRONOUN⁀

👤⁀ = me  
우⁀ = you       
👨⁀ = him   
👩⁀ = her   
Ə⁀ = them   singular, gender-neutral, see default  
🔹⁀ = it   
👤👤⁀ = us   
ƏƏ⁀ = them   plural [DEFAULT]  

#### Possessive adjectives 

From: PRONOUN⎴

👤⎴ = my   
우⎴ = your   
👨⎴ = his     [DEFAULT]  
👩⎴ = her  
Ə⎴ = their    singular, gender-neutral  
🔹⎴ = its     [DEFAULT]  
👤👤⎴ = our   
ƏƏ⎴ = their    plural [DEFAULT]  

### Possessive clitics

Possessive clitic A's B becomes A⌎ B, Example John's dog -> John⌎ 🐶 

#### Possessive pronouns 

Form: PRONOUN⌎ 

👤⌎ = mine   
우⌎ = yours   
👨⌎ = his     see default form 👨⎴   
👩⌎ = hers  
Ə⌎ = theirs   singular, gender-neutral  
🔹⌎ = its     see default form 🔹⎴   
👤👤⌎ = ours   
ƏƏ⌎ = theirs  plural  

### Reflexives 

Form: PRONOUN🧿 

These are special irregular 'compounds' to keep things simple .

👤🧿 = myself   
우🧿 = yourself   
👨🧿 = himself   
👩🧿 = herself  
Ə🧿 = themself    singular, one person with unspecified or nonbinary gender  
🔹🧿 = itself   
👤👤🧿 = ourselves   
ƏƏ🧿 = themselves   plural  


#### Demonstrative deictics

▣ = this  
👉 = that   use same word for complementizer vs demonstrative [OVERRIDE]  
▣▣ = these  
👉👉 = those  

👉 ⟡ = that's       99% of cases  
👉 ↶⟡ = that was   not grammatical, still everywhere in colloquial English — That's him! (≈ "That was the person I meant.")  
👉 ⊸ = that has    rare, mostly before been  


#### Spatial deictics

☟ = here  
☞ = there  
☉ = object / thing


## Orthography

### Markdown

- Always write in a markdown-friendly way
- prefer `- **title**: bla bla...` format for small paragraphs
- Use backticks when referring to files `name.md`
- emphasis: prefer `_` over `*`, i.e. `_very important_`
- lists: 
    * prefer `-` over `*`  
    * when there are lots of subitems, prefer creating a subsection
- when documenting pictoji examples, AVOID punctuation or markdown ascii intended for documentation before / after the pictoji strings. This rule OVERRIDES English grammar conventions.

    * If punctuation/markdown is really necessary, put extra spaces before after:  우 👀  *like this*.        
    * documentation phrases end with a dot EXCEPT when the phrase ends with pictoji strings:    우 👀

- when documenting pictoji examples prefer ASCII arrows like `->` over →

### Tofu characters

Given this review (as of 2025) of so-called 'tofu' chars: 

* Windows: ☐ U+2610 ballot box
* macOS / iOS:	⍰ or ☐ U+2610 with question mark
* Android / Chrome:	◻️ (or a rectangular outline)
* Linux	often: ☐ U+2610 or ⧠ (depends on font fallback chain)

we define all of them as 'tofu' and forbid their use.

### Definitions syntax

Symbol definitions are in the format

SYMBOLS = MEANING1 / MEANING2 / ...    RATIONALE? [OVERRIDE]? [DEFAULT]? [ARROW]? SPACERET

where:

- SYMBOLS: Sequence of Unicode symbols 
- MEANINGn: English word OR a pictoji unicode symbols sequence
- RATIONALE?: optional description
- [DEFAULT]?: optional flag to indicate preference when there are multiple symbols mapped to the same word 
- [OVERRIDE]?: optional flag which asserts that the mapping is semantically final and intentional. Override Enforcement:

    - Any line or definition marked [OVERRIDE] is semantically final.
    - Automated or manual reviews MUST ignore meaning, symbol choice, or mapping debates for those entries.
    - Only the following checks may still apply:
        * Structural integrity: token spacing, normalization, Unicode validity.
        * File consistency: duplicates, formatting, or syntax errors.
    - Review tools and validators MUST detect [OVERRIDE] tags and suppress all semantic warnings for those lines.
- SPACERET: two spaces so markdown renders properly the newline (we use this solution here only to minimize visual clutter, in general avoid phantom spaces)
- [ARROW] to track arrows usage. See [Arrow overload](#arrows-overload)

### Assertions syntax

Assertions are in the format STRING1 OPERATOR STRING2, where OPERATOR can be ==, <?, ?>

STRING1 SHOULD be a SYMBOLS string, STRING2 a NATURAL_LANGUAGE string of corresponding meaning. In some occasions they MAY be swapped.

SYMBOLS ?> NATURAL_LANGUAGE   : encode(SYMBOLS) SHOULD be equal to MEANING

SYMBOLS <? NATURAL_LANGUAGE   : decode(MEANING) SHOULD be equal to SYMBOLS

SYMBOLS == NATURAL_LANGUAGE   :

- encode(SYMBOLS) SHOULD be equal to NATURAL_LANGUAGE
- decode(NATURAL_LANGUAGE) SHOULD be equal to SYMBOLS
 
- it's written SHOULD and not MUST because Pictoji is a non-deterministic system.
- it's only possible to maximize the expectation of a conversion success in the intended way. 
- Still, assertions in the specs and pictoji-test.md SHOULD always succeed when executed by `CURRENT_AI` having ONLY the specs as context. If they don't, flag them. 



### Symbol display

If you have to show a SYMBOL, always show: 

    SYMBOL | PNAME | UNAME | SEQ NFC? PROPS? SCOPE? WARN? RISKS? 
    TESTS?
    NOTES?

- Aim at displaying a one liner. Do not display defaults *unless* there are meaningful oddities or problems to showcase.
- All capital placeholders marked with `?` must not be shown if their content is empty.
- Use spaces between tokens in bracketed sections for easy scanning.
- Inside braces you may separate by spaces or commas - no colon required.
- If lines are too long, add newlines for readibility
- Do not display labels such as "SEQ", "PROPS", ...
- Parsers can infer field type by symbol:
    * +/– -> boolean
    * +/–/? -> ternary
    * _ / ~ /^ -> severity scale

Placeholders definitions:

- PNAME: the Pictoji name 
- SEQ:<U+...>  
- NFC: NFC_U [CPs:n BMP+] 
- NFC_U:| <U+...>    show *only* if different from SEQ
- UNAME: the Unicode English name
- WARN:, ⚠: PF1, PF2,... (R1); PF2, PF5, ... (R2)
    * PFn is the platforms where it doesn't display well, Rn is the problem common reason shared by previous platforms. 
    * express Pn as single icon:
        🍎	Apple (macOS / iOS)	
        🤖	Android (Google Noto)	
        🪟	Windows (Segoe UI Emoji)	
        🧭	Chrome / Web (Noto Color Emoji fallback)	
        🐧	Linux (Ubuntu / Fedora font packs)	
        💻	Generic text renderer
- RISKS:{Norm– Pres? ZWJ– Flag/RI– Autolink– Confu~ Width/Size^}
- PROPS:{EmojiPres+ VS16– ZWJ– RI– SkinTone– Gender– Cat=So EAW=W Bidi=ON}
- Norm, Pres, Confu meanings: Normalization, Presentation, Confusables
- SCOPE:[setting=natural, override–, collisions=[...]]
- TESTS:`TESTS:` ASSERTION
- ASSERTION: a pictoji testcase to fill *only* if there a meaningful oddities or problems 
- NOTES:`NOTES:` DESC 
- DESC: a one-liner to fill *only* if there are meaningful oddities or problems


### Translations

- For each answer regarding translations, show the context flags in the format 

    FLAG1 (MODIFIER), FLAG2 (MODIFIER), ...  

    where MODIFIER is either `g` for explicitly given and `i` for inferred.



## Morphology

English derivations are not very regular, sometimes imprecise and tend to overlap, so here we laid out a full spectrum of cases.

We also add examples in Latin since its forms are much more regular and still sometimes used in academic or formal environments.

* `encode` function SHOULD attempt a translation to the most precise proper morphological category.
* `decode` function SHOULD select the form depending on context:
    * `setting=natural`: closest to what an everyday English speaker would read best.  
    * `setting=formal`:  closest to what an English academic would want.  


### NOMINALIZATION -> noun

#### Agentive (doer)

Form: SYMBOLᑉ

* **Human**: 🗣ᑉ = speaker, writer, teacher
  Latin: *orator* (speaker, root *orare* “to speak”), *scriptor* (writer), *doctor* (teacher, root *docere* “to teach”)

* **Nonhuman / institutional**: generator, producer, publisher
  Latin: _generator_, _creator_, _auctor_ (originator, author)


#### Instrumental (tool / machine)

Form: SYMBOLᑉ

* **Mechanical**: printer, mixer, amplifier
  Latin: _instrumentum_ (tool), _vehiculum_ (vehicle), _ferramentum_ (iron tool)

* **Abstract / functional**: trigger, enabler, unlocker (metaphoric agent)
  Latin: _documentum_ (lesson, evidence), _indicium_ (indicator, sign)


#### Resultative (product / outcome)

Form: SYMBOL﹀

* **Concrete results**: building, painting, weaving
  Latin: _aedificium_ (building), _scriptum_ (a written thing), _opus_ (work, creation)

* **Abstract results**: solution (root *solv-* “to loosen”), insight, reflection
  Latin: _solutio_ (solution), _reflexio_ (reflection), _cognitio_ (knowledge, insight)


#### Process / Action (event)

Form: SYMBOL TODO

* **Dynamic**: 🗣 TODO = speaking, running, working
  Latin: *cursus* (running), *oratio* (speaking, prayer), *labor* (work)

* **Static / ongoing**: 💭 TODO = thinking, meditating, sleeping
  Latin: *cogitatio* (thinking), *meditatio* (meditation), *somnus* (sleep)


#### State / Quality

Form: SYMBOL^0

- **Qualitative**: 🙂^0 = happiness, 웃^0 = personhood (different from collective), brightness, warmth, 
  Latin: _beatitudo_ (blessedness, happiness), _claritas_ (brightness), _calor_ (warmth)

- **Condition / status**: 
    - deadness, tiredness, 🙁^0 = sadness,  
    ⭐^0 = stardom (The status of a performer or entertainer acknowledged as a star.)   
    ⚐^0 = nationhood (status / condition of nation)  
  Latin: _mors_ (death), _lassitudo_ (weariness), _tristitia_ (sadness)


#### Collective / Group (aggregate)

Form: see [Hierarchies section](#hierarchies).

- **Social**: brotherhood, partnership, community, ⭐^2 = stardom (Star performers considered as a group)
  Latin: _fraternitas_ (brotherhood), _societas_ (partnership), _communitas_ (community)

- **Organizational / territorial**: kingdom, priesthood, ⚐^2 = nationhood (the nation as collective body) 
  Latin: _regnum_ (kingdom), _sacerdotium_ (priesthood), _natio_ (nation)



#### Locative (place of X)

Form: SYMBOL📍

* **Functional**: bakery, laundry, ⚒📍 = workshop
  Latin: _pistrinum_ (bakery), _officina_ (workshop), _balneum_ (bath)

* **Institutional**: 📖📍 = library, school, hospital
  Latin: _bibliotheca_ (library, from Greek), _schola_ (school), _hospitium_ (guest house, hospital)


#### Temporal (time of X)

* **Period**: morning, evening, night
  Latin: *mane* (morning), *vesper* (evening), *nox* (night)

**Recurrence / cycle**: 

- Form (generic): 🔁SYMBOL
- English Examples 🔁◐ = redo, 🔁▶ = replay, rewrite  
repetition, schedule, renewal
- Latin: *repetitio* (repetition), *series* (sequence), *renovatio* (renewal)




---

#### Abstract / Conceptual (idea of X)

* **Doctrinal**: aestheticism, Christianity, Taoism
  Latin: *Christianitas* (Christianity), *Stoicismus* (Stoicism), *aestheticismus* (Aestheticism)

* **Theoretical**: realism, rationalism, cognitivism
  Latin: *realismus*, *rationalismus*, *cognitivismus*

---

#### Other nominal derivations

* **Diminutive**: booklet, duckling, cottage
  Latin: *libellus* (“little book”), *homunculus* (“little man”), *domuncula* (“small house”)

* **Augmentative**: strongman, lionheart, megastructure
  Latin: *magnitudo* (greatness), *grandis* (large), *heros* (hero)

* **Pejorative (derivational)**: childish, foolish, bossy
  Latin: *stolidus* (foolish), *ineptus* (inept), *vanus* (vain)

* **Gendered**: actress, waiter, princess
  Latin: *actor / actrix*, *magister / magistra*, *rex / regina*

---

### ADJECTIVALIZATION -> adjective

* **Qualitative**: greenish, fiery, cold, noisy
  Latin: *viridis* (green), *igneus* (fiery), *frigidus* (cold), *sonorus* (noisy)

* **Relational**: academic, chemical, national, seasonal
  Latin: *academicus*, *chemicus*, *nationalis*, *temporalis*

* **Possessive**: kingly, brotherly, ghostly
  Latin: *regius* (royal), *fraternus* (brotherly), *umbrosus* (shadowy)

* **Material**: golden, wooden, silken, metallic
  Latin: *aureus* (golden), *ligneus* (wooden), *sericus* (silken), *metallicus*

* **Locative or contextual**: worldly, coastal, rural
  Latin: *mundanus* (worldly), *maritimus* (coastal), *rusticus* (rural)

* **Privative or abessive (lacking)**: homeless, toothless, colorless, sightless
  Latin: *incolor* (colorless), *edentulus* (toothless), *sine domo* (without home)

* **Evaluative or defective (improperly)**: ill-formed, ill-timed, malformed, misaligned
  Latin: *male formatus* (ill-formed), *malus tempus* (ill-timed), *deformis* (misshapen)

---

### PARTICIPIAL ADJECTIVES -> verbal qualities

**Active**: 

Form: ↻ADJ

- English: "-ing" |  ↻❤ = loving, ↻▲🏃 = running, shining
- Latin: "-nt" | *amans* (loving), *currens* (running), *lucens* (shining)

**Passive**: 

Form: ↶ADJ

-  English: "-ed" |  ↶❤ = loved, formed, chosen
-  Latin: "-tus" | *amatus* (loved), *formatus* (formed), *electus* (chosen)


### POTENTIAL / APTIVE -> ability or suitability

Form: SYMBOL◉  (without spaces)

* English: "-able", "-ible" | ❤◉ = lovable, 👀◉ = visible, readable, reversible
* Latin: "-bilis" | ❤◉ = *amabilis* (lovable), 👀◉ = *visibilis* (visible), *legibilis* (readable), *reversibilis* (reversible)


### VERBALIZATION -> verb

* **Causative**: modernize ("make modern"), simplify ("make simple"), empower ("give power")
  Latin: *clarificare* (to make clear), *amplificare* (to make larger)

* **Inchoative**: awaken ("become awake"), solidify ("become solid")
  Latin: *florere* (to begin to bloom), *albescere* (to turn white)

* **Iterative / intensive**: redo ("do again"), reconsider ("think again")
  Latin: *dictare* (say repeatedly), *pulsare* (beat repeatedly)

* **Denominal**: hammer -> to hammer, poison -> to poison
  Latin: *malleare* (from *malleus*, hammer), *coronare* (to crown)

* **De-adjectival**: cool -> to cool, warm -> to warm
  Latin: *purificare* (to purify), *solidare* (to make solid)


### ADVERBIALIZATION -> adverb

* English: quickly, recently, extremely, nightly, loudly, brightly, kindly
* Latin: *celeriter* (quickly), *nuper* (recently), *valde* (very, extremely), *noctu* (by night), *clamose* (loudly), *lucide* (brightly), *benigne* (kindly)

Form:  Sノ

### POLARITY / NEGATION -> opposite meaning

#### Negative adjectival derivation

Typical affixes: un-, in-, im-, ir-
English: unholy, unequal, impossible, impolite
Latin: *impius* (unholy), *inaequalis* (unequal), *impossibilis* (impossible), *impolitus* (uncultivated, impolite)

#### Negative nominal derivation

Typical affixes: non-, dis-, a-, anti-
English: inequality, disbelief, non-determinism, anti-realism
Latin: *iniquitas* (inequality), *incredulitas* (disbelief), *indeterminatio* (non-determination), *antirealismus* (anti-realism)

#### Composite / recursive

Typical affixes: multiple derivations
English: undetermined (verb -> adj -> neg adj), unreality (adj -> noun -> neg)
Latin: *indeterminatus* (undetermined), *irrealitas* (unreality)


### PRIVATIVE / DEFECTIVE -> lacking or improper

#### Explicit lack (-less)

English: toothless, colorless, heartless, homeless, mindless
Latin: *edentulus* (toothless), *incolor* (colorless), *exanimis* (lifeless, “without breath”), *sine domo* (homeless)

#### Improper or deficient (ill-, mal-, mis-)

English: ill-formed, ill-advised, malformed, misaligned, malfunction
Latin: *male formatus* (ill-formed), *malus consilium* (bad advice), *deformis* (misshapen), *vitium machinae* (machine fault)


### Morphology notes

* Each derivation expresses a **semantic transformation** of a base (verb, noun, or adjective).
* Boundaries are fluid; for example, *printer* may be **agentive** (person) or **instrumental** (device).
* Multiple derivations can chain:

  * *build* -> *builder* -> *builderhood* (agent -> group)
  * *bright* -> *brightness* -> *enlightenment* (adjective -> quality -> abstract concept)


## Graphemics

- Text normalization: Apply NFC to all text
- Punctuation: ASCII only. Attaches to the left of the following token (no extra spaces); tokens are space-delimited elsewhere.
- Forbid "smart typography": never use curly quotes (“ ” ‘ ’), ellipsis (…), en/em dashes (– —), or minus (−) in place of ASCII " ' ... - -
- In specs where PICTOJI is defined in terms of PICTOJI itself instead of English, quote PICTOJI expressions with 〘  〙
    -〘  〙 MUST be used ONLY within PICTOJI specs. 


### Unicode and tokenization integrity

- Each Pictoji token represents exactly one Unicode grapheme cluster in its canonical form.
- A grapheme cluster may consist of a single code point or, if explicitly defined in Unicode data (e.g., an Emoji ZWJ Sequence or variation-selector sequence), a fixed multi-codepoint combination treated as atomic.
- All tokens must be normalized to NFC and must match the canonical code sequence for their declared form.
- Multi-codepoint symbols are disallowed except for Unicode-defined Emoji ZWJ Sequences and Emoji Presentation Sequences listed in the official Unicode Emoji Data files corresponding to the declared unicode_version of this Pictoji release.
Each such symbol must appear exactly as defined in that version's data file, normalized to NFC. 
- If a grapheme is in specs vocabulary and can be represented with a single code point, prefer it over the fully qualified version ending with variation selector VS16 U+FE0F (e.g. prefer ❤:U+2764 bare, may render monochrome vs forced emoji ❤️:U+2764 FE0F VS16)
- Compound words are formed by direct concatenation of canonical Pictoji tokens, each corresponding to exactly one Unicode grapheme cluster in normalized NFC form.
No unregistered or invisible joiners, variation selectors, or combining marks may occur except where explicitly defined as part of a token's canonical Unicode sequence (e.g., in registered Emoji ZWJ Sequences).
- Text encoded according to these rules remains byte-stable and semantically invariant under copy/paste across conforming Unicode systems.
- Visual appearance (glyph style, color, or emoji presentation) may vary by platform, but the underlying normalized Unicode sequence must remain identical.


### To ensure portability:

- Symbols MUST render correctly on platforms >= Windows 10 21H2, MacOS 14 (Sonoma), IOS 18.6, Android 11, Ubuntu 24.
- Prefer symbols in the Basic Multilingual Plane (U+0000–U+FFFF).
- Avoid emoji that depend on gender, skin tone, or family modifiers.
- Normalize text to NFC before saving or transmitting.
- Keep punctuation ASCII-pure (:, ?, -, (), etc.).
- Avoid rich-text editors that may auto-replace or style emoji sequences.
- All specs and generated files MUST be encoded as UTF8 with BOM. 


## Development

> Every faith, whether in God or in data, begins in awe and ends in administration   -- _Frank_

- **Authority and versioning.**: This lexicon is authoritative over Unicode names and prior Pictoji releases. Any change to mappings requires a version bump and a changelog entry.


### Commands

UNICODE_VERSION = 13.0
PICTOJI_HEADER = [PUT PICTOJI SPECS HEADER]   
PICTOJI_VERSION = [PUT PICTOJI VERSION EXTRACTED FROM SPECS HEADER]  
SUPPORTED_AIS = ["ChatGPT 5.*", "ChatGPT 5.* Thinking",  "Gemini 3 Pro Preview", "Claude Opus 4.5", "Claude Sonnet 4.5"]  
CURRENT_AI = [PUT AI NAME]  

`[ROLE=LABEL]` : Enables actor LABEL. Output "Pictoji [role=LABEL]\n" and follow the rules stated in its section. In general:
  - let the invoked role  present her/himself according to its character with a one-liner.
  - if very first chat interaction,  let her/him do some on-boarding and offeri additional things a casual user might want to try with Pictoji  

`[END]`  : end of conversation, output nothing.
`[DEV+]` : turns on the mode. Output "Pictoji DEV mode is ON."  
`[DEV-]` : turns off the mode. Output "Pictoji DEV mode is OFF."  
`[REVIEW]`: Output "# `PICTOJI_VERSION` REVIEW RESULTS:" and start a thourough review of these specs.  
`[TEST]` : find blind spots, missing high freq terms, phrases you can't express.  
`[WRITE F]` where F is a file, create that file.  

### PDP generator

**Goal.** Emit a `pdp.md` file that contains: a decoding preamble (no English word lists), a single sequence of symbols ordered by HIGH_FREQ_WORDS frequency, and machine-checkable metadata. No English word literals may appear in `pdp.md`.

- **`gen_pdp.py` SHOULD**: be minimal
- **`gen_pdp.py` SHOULD NOT**: have documentation, have symbols unless absolutely needed for its inner workings, try being a replica of `pictoji.md`.
- **Reproducibility**: Same inputs MUST yield byte-identical `pdp.md`. Any change to HIGH_FREQ_WORDS order or mapping requires bumping pdp_format or pictoji_version.
- **Security/IO**: No network access. Only read pictoji.md and optional local coca.txt (if present). Never write any file other than pdp.md.

- To reach minimality, the PDP SHOULD list the symbols of HIGH_FREQ_WORDS  as a sequence *without* the corresponding English meaning, which could be retrieved by known COCA sources.  


#### HIGH_FREQ_WORDS order (no words in specs/output)

- The program MUST carry, internally, a canonical HIGH_FREQ_WORDS order (lemmas), normalized to lowercase ASCII, one per line, never printed.
- The program MUST compute high_freq_words_sha256 = SHA-256 of that normalized list and include it in pdp.md's metadata.
- The program MUST NOT fetch from the network at runtime. The order for HIGH_FREQ_WORDS MUST be embedded in code, or loaded from a local file if present if |HIGH_FREQ_WORDS| > 200 .

#### Mapping to symbols (rank-based, private)

- The program MUST maintain, inside code, a rank→symbol mapping derived from the project's definitions (e.g., by parsing pictoji.md lines shaped like SYMBOL = …) plus any necessary private overrides to disambiguate high-frequency function items.
- This internal mapping MUST NOT be written to pdp.md or logs; only the resulting symbols appear.

#### Output format (deterministic)

`pdp.md` MUST include:

[meta]
source = COCA_TOP_HIGH_FREQ_WORDS
coca_sha256 = <64 hex chars>
pictoji_version = <semver or tag>
pdp_format = 2
unicode_version = UNICODE_VERSION
emoji_sequence_source = emoji-zwj-sequences.txt (Unicode)
[/meta]

<exactly |HIGH_FREQ_WORDS| space-separated symbols, in rank order>

#### Normalization & validation (must)

- Tokenization: symbols are space-delimited; punctuation attaches to the left;
- Progressive and past attachers: ↻ may attach to any verb; ↶ attaches to verbs/auxiliaries.
- Infinitive: ↦ = "to / toward / as infinitive."

##### Before writing, the program MUST verify:

- [symbols] length = HIGH_FREQ_WORDS tokens.

- high_freq_words_sha256 matches the embedded COCA order; otherwise exit with error.

#### Missing coverage (graceful, explicit)

- If a COCA rank is not mapped, the program MUST place error symbol ↂ at that position.
- The program SHOULD emit a single-line summary count to stderr only (not into `pdp.md`).



### Corpora

- **pictoji.md**: these specs 
- **README.md**: user-friendly presentation (currently very terse, to complete for 1.0)
- **gen_pdp.py**: Takes as input the whole file `pictoji.md` and generates the file `pdp.md`.  
- `pdp.md`: Contains the Pictoji Decoding Prompt (PDP). Deterministically generated by `gen_pdp.py`. 
- `pictoji-test.md`: separate file to test encoding / decoding of phrases. 
- `pictoji-dev.md`: non authoritative file just for drafting ideas. 
- For context and comparison purposes, the previous iteration of each file (even deterministically generated like `pdp.md`) will be also stored in a chat of the same name under the same `CURRENT_AI` project named "Pictoji".

#### Bibliography

- <a id="ampersand">[Ampersand]</a> Ampersand language and tools https://ampersandtarski.github.io 
- <a id="dioids">[Dioids] </a>  Gondran & Minoux, Graphs, dioids and semirings : new models and algorithms, book, ISBN 0387754504, 9780387754505.
- <a id="graphblas">[GraphBLAS]</a> Kepner et al., GraphBLAS
    - site: https://graphblas.org/
    - math foundations pdf: https://www.mit.edu/~kepner/GraphBLAS/GraphBLAS-Math-release.pdf 
    - book: Mathematics of Big Data, ISBN 9780262038393

- <a id="markdown"></a> Markdown, CommonMark specification https://spec.commonmark.org/0.31.2/
- <a id="metamath-site">[Metamath]</a>  
 site: https://us.metamath.org  
 book:  https://us.metamath.org/downloads/metamath.pdf
-<a id="rubi">[Rubi]</a> Rub***i*** Integrator https://rulebasedintegration.org/vision.html
- <a id="sato">[Sato]</a> Taisuke Sato, A Linear Algebraic Approach to Datalog Evaluation  https://arxiv.org/abs/1608.00139
- <a id="rbd">[RBD]</a> Rule Based Design, by Lex Wedemeijer, Stef Joosten, Jaap van der woude  https://www.researchgate.net/profile/Stef_Joosten/publication/327022933_Rule_Based_Design/links/5b7321be45851546c903234a/Rule-Based-Design.pdf  
- <a id="gel">[Gel]</a> Sullivan et al - Querying Graph-Relational Data https://arxiv.org/abs/2507.16089


### Finally

For 1 to 1 ordinary user request calls, let `role=secretary` do the routing work, and actors freely interpret their role (including yourself as `[ROLE=screenwriter]` or `[ROLE=reviewer]` when explicitly invoked)

DO NOT create any file unless told to.

DO NOT automatically run a review.

If you are not one of the SUPPORTED_AIS at indicated version or above, raise a warning: 
"Note: Pictoji was tested only with `SUPPORTED_AIS`, it seems you are using another AI `CURRENT_AI`. Pictoji may or may not work as intended.".

Output "ㄕICTOji `PICTOJI_VERSION` loaded.      Have fun!"

[DEV+]  
[ROLE=secretary]

