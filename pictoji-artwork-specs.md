# Design Guidelines


#### Meaning 𐒄 for users

For the graffity `g->` and story `s->` user: emojis are magnets on a whiteboard. Each one pulls nearby meanings toward it. Put two close together and they create something new in between.

For the philosophy `p->` user: Pictoji is a semantic physics engine. Place symbols and rules, and
meaning settles into shape - not because you calculated every point, but because the
structure and forces determine where everything has to be. The AI's understanding
of the world is like gravity; your expressions are the architecture.

TODO CHECK
For the nerd math `u->` user: Pictoji expressions define a variational problem over the AI's
embedding space. Each symbol contributes a potential well centered on its pretrained
semantic locus. Algebraic rules act as holonomic constraints. The decoded 𐒄 is the
minimum-energy configuration of the joint system. Non-determinism arises from
degenerate local minima; the PDP breaks these symmetries.

## Naming

- The Pictoji name MUST be written as `ㄕicto`_`ji`_ — with 'icto' lowercase.
- The title font MUST be simple. The name itself is already complex enough; do not add visual complexity with elaborate typefaces.


## Performance

- MUST load fast: vanilla JS, zero framework dependencies, single HTML file.
- MUST be responsive: interactive elements (sliders, buttons) MUST NOT lag.
- MUST keep CPU usage very low:
  - No persistent animation loops (`setInterval`, `requestAnimationFrame` running indefinitely).
  - All timers MUST be finite and self-clearing.
  - Slider updates MUST use targeted DOM patching (update specific element properties), never full innerHTML re-renders.


## Visual effects

- Static backgrounds only, no moving background symbols.
- No sunrise or ambient color-cycling animations.
- Slight CSS transitions are acceptable (opacity fades, height transitions, hover state changes).
- Easter eggs on hover/click are acceptable (e.g. header symbol interaction).


## Symbol portability

- All symbols used MUST be renderable on supported platforms as per Pictoji specs

## Power Hierarchy tab

### Progression order

- Levels MUST be displayed ascending: `^1` -> `^2` -> `^3` -> `^4`.
- Do NOT start from the highest grade; it spoils the progression.

### Special levels

- `^0` (essence) and `^-1` (genesis) MUST be separated from the main progression.
- Place them behind a toggle/button, phrased as: _"What about X^0 and X^-1 ?"_
- The toggle MUST NOT trigger a full re-render; use CSS transitions (e.g. `max-height`).

### Visual diagrams

Each power level MUST include an inline SVG diagram illustrating the structural concept:

- **^1 Individual**: Several isolated nodes (웃 faces for person, dots for other emoji). No connections between them.
- **^2 Collective**: Small groups of linked individuals. Internal connections within each cluster.
- **^3 Society**: Groups linked to each other. Topology MUST be non-linear (triangular or circular, NOT a chain). Every cluster should connect to every other cluster, not just neighbors. Use split layout (text left, diagram right) if needed to accommodate diagram size.
- **^4 Civilization**: MUST communicate hierarchical nature (tree structure with apex, tiers, leaf clusters). NOT a flat mesh or random network.

### Cluster differentiation

Clusters MUST be visually distinguishable from each other:
- Randomize node positions (jitter) so clusters don't look identical.
- Vary cluster sizes (different number of nodes per cluster).
- Use different colors per cluster (warm palette variations).


## Polynomial Forge tab

- Sliders update bars, formula text, and philosophy reading via direct DOM property writes.
- Preset buttons sync slider positions and update all displays.
- No full re-render on slider `input` events.


## Footer

- Include a link reading _"I want to believe"_ at the bottom.
- The link MUST look clickable: visible underline, appropriate cursor, hover state with color/spacing change.