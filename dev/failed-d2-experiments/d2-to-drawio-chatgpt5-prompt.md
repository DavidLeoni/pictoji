

## D2 to draw.io (Proper Containment Layout)

**Goal:**
Translate a D2 diagram into a `.drawio` file that preserves nesting, containment, and hierarchy, with all nodes properly placed inside their containers.



### 1. Containers

* Every D2 block `{ ... }` that groups nodes becomes a **swimlane or group** in draw.io.
  Example style:

  ```
  swimlane;rounded=1;html=1;startSize=28;
  ```
* Respect scope, not just names.
  - When converting from D2, treat each block as its own namespace.
  - A node name reused in another block is a different node, not the same one.
* IDs ≠ labels:
  - Keep internal IDs unique (e.g., qualified by scope), but keep visible labels simple.
  - Never merge or deduplicate nodes by label alone.
* Child nodes must have their `parent` set to that container, and their coordinates **relative to the parent**, not absolute.
* All children must fit entirely inside their parent (no overlap or overflow).

### 3. Edges

* All edges stay on the **top layer** (`parent="1"`) so they remain visible across containers.  
* For every group of identical edges (same source, target), create one edge per occurrence and make sure to offset them so arrows and labels do not visually overlap. Apply curvature if needed.


### 4. Layout rules

* Default relative margins for child nodes: `x ≈ 24`, `y ≈ 60`.
* Place sibling containers evenly spaced horizontally within their parent.
* Nodes without a parent container (e.g., `user`, `api server`, `logs`) should be placed **outside** the main containers with a clear gap.
* Minimize arrows crossing through elements, prefer instead routing around, below or above when possible: in particular, try avoiding lines that cross container headers or labels.
  * If necessary, add at most one "waypoint" to each edge's geometry. 
  * Avoid tortuous unnecessary paths.

### 5. Output

* Generate:

  * A valid `.drawio` XML file (`mxfile` root) that opens in diagrams.net.
  * Optionally, a `.svg` preview for quick inspection.
* Verify that when a parent container moves, all its children move with it.

### 6. Validation checklist

Before finishing, confirm:

* [ ] Each nested node has the correct `parent` according to D2 hierarchy.
* [ ] No node crosses outside its container.
* [ ] Multi-edges are visually distinct (curved and labeled separately).
* [ ] Edges shouldn't cross nodes / containers, especially labels.
* [ ] External nodes remain outside top-level groups.
* [ ] Edges connect correct sources/targets and remain visible.

7. Optional Rendering Checks

* Verify that moving a parent moves all children correctly.
* Check curved edges remain anchored after container movement.

HERE IS THE D2 GRAPH: 



### Example D2 input

https://d2lang.com/

```d2
network: {
  cell tower: {
    satellites: { shape: stored_data; style.multiple: true }
    transmitter
    satellites -> transmitter: send
    satellites -> transmitter: send
    satellites -> transmitter: send
  }
  online portal: {
    ui: { shape: hexagon }
  }
  data processor: {
    storage: { shape: cylinder; style.multiple: true }
  }
  cell tower.transmitter -> data processor.storage: phone logs
}
user: { shape: person }
user -> network.cell tower: make call
user -> network.online portal.ui: access { style.stroke-dash: 3 }
api server -> network.online portal.ui: display
api server -> logs: persist
logs: { shape: page; style.multiple: true }
network.data processor -> api server
```


https://d2lang.com/tour/containers/
```
server server.process 

im a parent.im a child 

apartment.Bedroom.Bathroom -> office.Spare Room.Bathroom: Portal
```


```
clouds: {
  aws: {
    load_balancer -> api
    api -> db
  }
  gcloud: {
    auth -> db
  }

  gcloud -> aws
}
```

```
```
christmas: {
  presents
}
birthdays: {
  presents
  _.christmas.presents -> presents: regift
  _.christmas.style.fill: "#ACE1AF"
}
---

### Optional enhancements

* `layout-engine: elk` → auto-arrange layout with spacing rules.
* `align-horizontally: true` → force sibling containers in one row.
* `use-icons: true` → replace standard shapes with draw.io icons (database, cloud, etc.).

---

Would you like me to make a short “starter snippet” you can prepend automatically to any D2 you send (so you don’t have to rewrite these rules each time)?
