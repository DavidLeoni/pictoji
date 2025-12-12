# ㄕ🗿 PICTOJI DEV ARCHITECTURE 0.6.6

If we wanted to go operational, we realistically could:

    1. try loading some relations into GEL / Postgres with few toy examples
    2. try [OneSparse](https://onesparse.com/docs.html) Postgre extension which brings GraphBLAS matrix semiring features into Postgres, hopefully it should at least guarantee some fast million-range nodes manipulation and fit real well our network model. Unfortunately, GEL doesn't support that extension but I guess it would be possible to use it with some SQL escape hatch.


## Use Cases

We need to support two main use cases, with very different requirements

1. Pictoji development
2. Data exploration - (possibly much) later

### Pictoji development usecase

- target: PICTOJI dev
- at minimum: natural language documentation
- at best: define, even better adopt, a fully formal specification language 

#### NL documention desiderata

For the time being we only focus on Pictoji development.


- data: small examples (few nodes - edges)
- input: text statements in markdown, written in a concise way
    - should support node grouping possibly by just indentation 
- precise positioning is required
- don't expect magic from the layout solver
  - manual fixing may be needed in drawio (with vscode plugin) 
  - Drawio can already properly import mermaid Flowcharts (block charts are imported only as svgs)
- Need to be able to write statements ordered like:
        subject predicate object (+ metadata)
  (alas many systems resort to  subject object : label )
- little to zero style indication in specs: style should be in a separate file
- markdown support: needed
- querying support: no need  

**Graph charts review**:

As of Oct 2025, the panorama is grim:

|Feature| Mermaid.js | D2 | PlantUML |Turtle/N3|
|-------|------------|----|----------|---------|
|-- label --> format:| only in flowchart | no | no |n|
|indentation| depends on chart (!)|n|?|n| 
|Global ids          |  y | n | ?|y|
|complex flowchart   |bad|better|?|-|
|bipartite            |flowchart misaligns, block doesn't allow arrows inside same group| ?| ?|-
|online version? |y|y|slow|y|
|github support| y | n | n? | n|

- Mermaid: it's a patchwork of styles and buggy :-/
    - flowchart syntax seems decent..but viz somewhat buggy (especially with components with different direction than the global )
- D2: better thought, yet missing global nodes ids, don't like subject object label syntax
- PlantUML  online version slow (needs java emulator)
- Turtle/N3: only a data format. `:` fetish. Turtle seems the only universal data syntax, need to understand named graphs support as in TriG syntax.
- GraphQL: seems nice for querying, didn't understand if/how do joins. Has mutation support.
- GQL: crappy link syntax, useless `:`, `()`, `[]`
- GEL (previously EdgeDB): nice syntax


**Decision:**

Use Mermaid, when it doesn't deliver, convert to drawio as fallback.


#### Formalization desiderata

Idea: provide denotational semantics style rules in some (hopefully) executable formal language

Language SHOULD (ideally):
- be a immutable subset of an existing language
- support functional programming
- support match
- support full range of unicode 
- support math conventions, e.g. ^ for exponentiation 
- support redefinition of all operators and keywords into arbitrary single char unicodes
- exploit dot . chaining as meaning 'tensor composition' if needed
    - don't mind generating attributes dynamically
- be Python inspired (a plus)

Db SHOULD:
- support querying : needed, with good query ergonomics 
    1. data shaping?
    2. function calls (e.g. string concatenation?)
    3. propery a.b.c traversal
    4. recursive reach support: a plus
    5. recursive reduce support: a plus
- Good hierarchy modelling
- Constraints
- Support writing specs definition, rewrite rules within the system / db
    - can be only theoretical for 1:1 representation, does not need to be performant
    - recursive functions: a plus   
    - datalog style unification: a plus 
    - easily represent expr rewrite in the db itself   
    - formal semantics paper: a plus
    - Examples:  
        -   "show me all expressions where 웃 appears contracted with 🐶"
 
- Migrations support: a plus, could model a variety of use cases: 
    - treat Pictoji semantics (emoji types, relations, rules) as schema
    - let migrations track and version these meanings over time
    - users could install/export semantic packs via migrations
    - explanations reference the migration that changed a meaning
    - older semantics could be restored for "time-travel" evaluation


- System semantics def: I'd like to use just simple functions with match (no extra notation like  [[ ]], turnstyle |-, etc )
```
""" NOTE: PSEUDO LANGUAGE GARBAGE EXAMPLE"""
def meaning(expr, env):
    "X"     :    env[X]
    "A ⋈ B" :   meaning(A, env) ⋈ meaning(B, env)
    "∃x.E"  :   meaning(E, env) 🎯 drop x
```

**Conclusion**

Obviously, such a language may very well not exist, and even if it existed, most probably people wouldn't like to see a bunch of weird emojis anyway. So it's fine if we define a preprocessor of, say .pictoji files,  or even define our subset for the markdown specs as 'the language' (as we did so far). 
The important thing is that we piggiback to existing formally specified systems and explicitly define translation rules if needed so that the AI understands what we're talking about. 


### Data exploration use case

- target: casual user
- input: text statements in whatever syntax is best supported by target implementation OR a query language we MAY decide to develop
- data: potentially a lot, at least whole English vocab, plus real world instances. 
- schema:
    - sometimes toy schema with lots of generated data
    - ..or large taken from Wikidata project
        - schema, ids
- db requirements:
    - query language: see [Formalization desiderata](#formalization-desiderata)
    - unicode support
    - hackable python impl
    - async first: a plus
    - indexing starts from 1 (as in sql): a plus
    - multilingual labels: a plus
    - Metadata (link properties): a plus 
    - python compat: a big plus 
        - typing with dataclasses: a big plus 
    - I'm willing to rewrite a backend interface to big data engines if needed
- markdown support: nice to have, not sure it's needed
- viz system: cytoscape.js? 
    - maybe with webgl optimization
    - custom physics constraints layout with Box2D or even Bullet? (TODO how many nodes? WebCola (only 100 nodes)
- matrix view: maybe something like [Bertifier?](https://www.aviz.fr/Bertifier/Bertifier)



## Architecture

**Options:**

- adopt SPARQL / QLever? 
    - > Only as backend, SPARQL is just too verbose
    - can't expect users to write stuff like `?person_id wdt:P31 wd:Q5 .` (Wikidata example)
    - SPARQL is probably never going to become mainstream, 
      low learning value for users 

- adopt GEL (previously EdgeDB)?
    - pro: 
        - clean syntax, inspired from Python
        - strongly typed
        - fp style
        - good modeling capabilities
        - at least some business userbase        
        - [formal paper (Sullivan et al, 2025)](https://arxiv.org/pdf/2507.16089)
        - made by people with python background
        - no NULL
        - query analyzer is designed in Python, has python client
        - boasts one query per expression, could be almost the operational mirror of "expression has a single denotation"
        - versioning, migration support
        - inherits Postgres features

    - con: 
        - only supports Postgres
        - slow at joins
        - no recursive CTE (for now)
        - no recursive functions 
        - no matching 
        - indeces start with 0
        - niche, partially low learning value for users 
        - (currently) no OneSparse Postgres extension support

- adopt [OneSparse](https://onesparse.com/)?
    - Postgres extension for GraphBLAS, semiring algebra
    - pro: very relevant for this project
    - con: very young (as of nov 2025)
    - SQL syntax sucks 

- adopt a Python ORM
    - es. Piccolo, minimalistic and async 
    - con: apparently orms only support verbose annotations, not yet simple stuff like .  
    ```python
        class Person:
            owns : Dog
    ```
    - con: probably slower / less elegant than EdgeDB  

- invent minimalistic async Python ORM?
    - con: inventing -> time sink, for what?

- use some Datalog engine?
    TODO more review
    - pro: recursive stuff support, matching, reasoning
    - con: typically they're loosely typed

- TerminusDB
    - pro:
        - currently (nov 2025), poor GraphQL support

    - con:
        - 

    - relevant example: https://terminusdb.org/docs/cookbook-taxonomy-inheritance/
    
- DGraph
    - cardinalities:  limited expressivity


**Decision:**

- Basically: I want it all... and I will get nothing.

- Possible path to sanity:

    1. Write high-level custom pictoji lang in markdown specs
        - custom-made handy matching syntax, e.g.:   X X -> X^2
        - symbolic algebra system must be dealt with by AI anyway
    2. adopt GEL for db relations / semantics
        - do first GEL prototypes, small scale
        - can data fit into the db?
        - can even _theory_ fit into the db? 
    3a. hope they implement OneSparse support..  
    2b. ..or I will vibe code it later 

Worst scenario, we still can:

- model simple relations 
- generate a good amount of test edges
- learn a good framework for real apps
- keep the door open one day for the cool OneSparse thing

Super worst scenario, GEL shuts down in two years:

- uh... probably by then we just... ask AI to maintain. 



## GEL experiments

p^0 + p^1 + p^2 + p^3

p1 in p^   ->  "select person in Person" works in GEL
p1 in p^1
p_1 in p == p^ == p^1
p1 not in p

type p° = {
    name      :  ....
    surname :   ....
}

a p went h

select p := p°{ name, friends: {name} }

with p := (select p° filter .name = 'Alice')
select p in p°

ChatGPT says if type names are latin letters, they must start as capital, otherwise can be any letter.

type 웃 { property 名 -> str; } select 웃 { 名 }; 

type 웃° { property 名 -> str; } select 웃° { 名 }; 


### GEL Schema

**TODO CHECK THIS STUFF ACTUALLY MAKES SENSE / COMPILES**

```gel
# TODO pictoji module would better but I'm lazy

module default {  

  scalar type Emoji extending str;   # or an enum, or link to an Emoji table

  type Expr {
    # Root type, but we’ll really use subtypes:
  }

  # Leaves
  type Var extending Expr {
    required property name -> str;
  }

  type Const extending Expr {
    required property value -> str;    # or json, or union of scalars
  }

  type EmojiExpr extending Expr {
    required property symbol -> Emoji;
  }


  type JoinExpr extending Expr {
    required link left  -> Expr;
    required link right -> Expr;
  }

  type TensorExpr extending Expr {
    multi link factors -> Expr;
  }

  type RewriteRule {
    required link pattern     -> Expr;   # pattern to match
    required link replacement -> Expr;   # result of rewrite
    # maybe some flags, priorities...
  }

}
```

### GEL Example data

```
with
  # build ( (x ⨝ 1) ⨝ 1 ) as data
  x := (insert Var { name := 'x' }),
  one := (insert Const { value := '1' }),
  inner := (insert JoinOp {left  := x, right := one}),
  expr := (insert JoinOp {left  := inner, right := one }),
  rule := (insert RewriteRule {pattern := expr, replacement := x})
select expr;
```

### GEL rewrite example


Rule idea:  (e ⨝ 1) -> e


- pattern is a JoinExpr whose:
    - left is Var(name := "e")
    - right is Const(value := "1")
- replacement is just Var("e").

TODO INCOMPLETE

```
with ru := RewriteRule {}
select (p := ru.pattern, r := ru.replacement) 
```
