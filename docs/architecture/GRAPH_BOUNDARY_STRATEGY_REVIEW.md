# Graph Boundary Strategy Review

**Branch:** `feat/research-architecture-vnext-graph-boundary-plan`  
**Date:** 2026-04-04  
**Milestone parent:** `feat/research-architecture-vnext-panel-deeper` (frozen)  
**Scope:** Planning-only review — no runtime changes in this document.

---

## 1. Is panel-deeper complete enough to freeze?

**Yes. panel-deeper is complete and should be frozen.**

The three extraction passes achieved exactly their declared scope:

| Pass | File | Contract |
|------|------|----------|
| 1 | `graphe.ui-panel.js` | Pure HTML builder, no DOM writes, no Graph calls |
| 2 | `graphe.ui-panel-actions.js` | Post-render event wiring, all Graph/Editor coupling injected as callbacks |
| 3 | `graphe.ui-entity-forms.js` | Modal form population and attr-editor helpers, no State mutation |

The `UI` IIFE now contains only its irreducible coordination core:

- `renderPanel` — 10-line coordinator (DOM show/hide + PanelController + delegate calls)
- `selectEntity` — inline by necessity (calls `Graph.cy.animate()` and `Graph.highlightNeighbors()`)
- `clearPanel` — 3-line DOM reset (too small to extract independently)
- Stubs for all extracted concerns (delegates, not logic)

The CodeRabbit security hardening was applied (`e08ce0d`) and the export artifacts regenerated (`a92c2fb`). The checkpoint document (`GRAPH_PANEL_DEEPER_CHECKPOINT.md`) is accurate. No further work in this branch is warranted without touching the `Graph` module or `DOMContentLoaded`.

**Verdict:** Freeze panel-deeper. Create the next branch from its head.

---

## 2. Best next branch target

**Option 3 — Graph boundary planning.**

Not an implementation branch. A planning and constraint-mapping branch that produces:

1. A complete audit of every `Graph ↔ UI` and `UI ↔ Graph` call site (there are exactly two critical bidirectional paths and several unidirectional ones — map them all with line numbers).
2. A proposed event bus contract: what events are emitted, what listeners register, what data flows in each direction.
3. A `graphe.graph-facade.js` interface sketch: which Graph methods become public API, which stay internal to the module.
4. A dependency injection map for the layout engines: how `applyMatriceLayout`, `applyNebulaLayout`, etc. will receive `State`, `TYPE_COLORS`, chapter data, and canvas context — without closing over global `State`.
5. A canvas overlay contract: whether halo rendering stays inside the Graph module or splits into a `graphe.canvas-overlays.js` concern.
6. A spike: one minimal event bus module (≤30 lines, IIFE, zero behavior change) integrated at exactly one interaction — the Cytoscape `tap node` → `UI.selectEntity` path — as proof that the pattern works at runtime.

The spike must be the last item, not the first. The planning artifacts gate the spike.

---

## 3. Why the other options should wait

**Option 1 — Story/Scrolly planning:**

`StoryMode.focusStory()` calls `UI.selectEntity()`, which calls `Graph.cy.animate()` and `Graph.highlightNeighbors()`. This is the same bidirectional coupling that keeps `selectEntity` inline. Extracting StoryMode first would require injecting either the full `Graph.cy` reference or an unresolved callback that still points at the inline `selectEntity`. The Graph boundary must be defined before StoryMode can be cleanly extracted — the event bus unlocks both at once.

**Option 2 — Cleanup branch (`clearPanel` / `PanelController.reset`):**

`clearPanel` is 3 lines:
```javascript
function clearPanel() {
  document.getElementById('panel-empty').classList.remove('hidden');
  document.getElementById('panel-body').classList.add('hidden');
}
```
This could fold into `PanelController.reset()` in a future update to `graphe.panels.js`. It is not worth a dedicated branch. The effort of creating, reviewing, documenting, and freezing a branch exceeds the value of moving 3 lines. Defer indefinitely or absorb into a future Graph boundary implementation pass.

**Option 4 — Workshop expansion with a second real sample lot:**

Workshop expansion is content and research work. The monolithic structure of `graphe.html` is not a blocker for adding workshop content — that belongs in the `workshop/` directory or standalone HTML pages. Do this on a content branch at any time, independently of architecture work.

---

## 4. Main risks of Graph-boundary work

Listed in descending severity:

**1. Visual regression with no automated detection.**  
There is no test suite. The Graph module has 5+ layout modes (`nebula`, `matrice`, `arbre`, `qui-gouverne`, `monetisation`), each with distinct positioning logic, Cytoscape stylesheet rules, and canvas halo overlays. Any structural change to the Graph IIFE can silently break one layout while others appear correct. Manual testing across all modes × the v96 canonical graph (2,263 entities, 20,057 relations) is the only safety net.

**2. Cytoscape `style()` chain fragility.**  
`applyMatriceLayout` dynamically generates 80+ `cy.style().selector(...)` rules based on computed class names (`chapter-0`, `type-Person`, etc.). These class names must match both Cytoscape selectors and CSS classes exactly. Moving the layout code to an external module requires passing the full Cytoscape `cy` instance — or exposing a style-registration API — without breaking the class/selector contract.

**3. Canvas overlay coupling inside layout methods.**  
The matrix layout generates canvas-based halo glows for chapter rows and type columns using the 2D canvas context directly from inside `applyMatriceLayout`. The canvas element, its dimensions, and the draw calls are not separate from the layout positioning logic. Extracting Graph without a clear canvas overlay seam would drag the canvas DOM reference into the extracted module, creating a new DOM coupling.

**4. Bidirectional initialization order at boot.**  
Currently: `Graph` IIFE declares itself → `UI` IIFE captures `Graph` reference inline. An event bus must be instantiated *before* both. This changes the boot sequence. Any error in the event bus boot position will silently prevent Graph rendering (Cytoscape tap events won't fire `node-selected`, panel never opens). The spike must validate this ordering before committing to the full extraction.

**5. `StoryMode` callback chain.**  
`StoryMode` calls `UI.selectEntity(id)` to focus narrative nodes. `selectEntity` calls `Graph.cy.animate()`. When Graph moves to a boundary, the `UI` object `selectEntity` exposes must still reach the extracted `Graph.cy` — either via the event bus (`emit('entity:selected', id)`) or via injected reference. The narrative callback chain must be audited and mapped before Graph moves.

**6. No incremental rollback path.**  
The Graph module is ~2,400 lines. Unlike the UI extraction passes (which moved 100–130 lines at a time with clear no-behavior-change contracts), Graph extraction cannot be done incrementally without a functioning event bus in place. A partial extraction leaves a broken app. The planning branch must define the full extraction boundary before any implementation commit touches the Graph IIFE.

---

## 5. Safest sequencing for a graph-boundary planning branch

This branch should produce documentation and one minimal code spike. No full extraction.

**Phase A — Audit (read-only, no code changes)**

1. Map every `Graph → UI` call site with file path and line number:
   - `cy.on('tap', 'node', ...)` → `UI.selectEntity(id)`
   - Any `Graph` method that calls `UI.*` internally

2. Map every `UI → Graph` call site:
   - `UI.selectEntity` → `Graph.cy.animate()`, `Graph.cy.$id()`, `Graph.highlightNeighbors()`
   - `UI.renderPanel` → `Graph.cy.$id()` (if present)
   - `uiFilters.renderTypeFilters()` → `Graph.applyFilters()`
   - `Editor.*` → `Graph.addNode()`, `Graph.removeNode()`, `Graph.updateNode()`, `Graph.addEdge()`, `Graph.removeEdge()`
   - `DOMContentLoaded` layout handlers → `Graph.applyLayout()`, `Graph.render()`, `Graph.fit()`

3. Map `StoryMode → Graph` and `StoryMode → UI` call sites.

4. List all methods the Graph module exposes that are called from outside the IIFE. This is the public API surface that must be preserved.

**Phase B — Design**

5. Define the event bus contract:

   | Event | Emitted by | Listened by | Payload |
   |-------|-----------|-------------|---------|
   | `entity:selected` | Graph (tap) | UI | `{ id }` |
   | `entity:focused` | UI.selectEntity | Graph (animate + highlight) | `{ id }` |
   | `filters:changed` | UI filters, search | Graph | `{ hiddenTypes, searchQ }` |
   | `layout:apply` | DOMContentLoaded | Graph | `{ name }` |
   | `data:loaded` | Bootstrap | Graph, UI | `{ data }` |

6. Define the Graph facade interface: which methods remain public after extraction, which become internal.

7. Define the canvas overlay seam: propose whether halo rendering stays inside Graph or becomes a `graphe.canvas-overlays.js` module receiving `(cy, chapterData, typeData)`.

8. Write `GRAPH_BOUNDARY_PLAN.md` in `docs/architecture/`.

**Phase C — Spike (minimal code, zero behavior change)**

9. Implement `graphe.event-bus.js` (≤30 lines, IIFE, `on(event, cb)` / `emit(event, data)` / `off(event, cb)`).

10. Wire exactly one interaction:
    - Replace `cy.on('tap', 'node', e => UI.selectEntity(e.target.id()))` with `cy.on('tap', 'node', e => EventBus.emit('entity:selected', { id: e.target.id() }))`.
    - Add `EventBus.on('entity:selected', ({ id }) => UI.selectEntity(id))` in DOMContentLoaded.
    - Verify no behavior change: tap node → panel opens → entity highlights. All layouts, all data sizes.

11. If the spike validates cleanly, document the pattern in `GRAPH_BOUNDARY_PLAN.md` as confirmed. Do not proceed to extract the full Graph IIFE in this branch.

**Phase D — Freeze**

12. Commit the planning docs and the spike as the branch milestone. The next branch (`feat/research-architecture-vnext-graph-extract`) can proceed with the full extraction using this plan as its contract.

---

## 6. What absolutely should not be touched first

**`selectEntity(id)`** — This function is the architectural keystone. It is the only bridge between Cytoscape tap events and the panel rendering + node animation. Do not move, rename, or split it until the event bus spike is validated and the Graph facade interface is written.

**`applyMatriceLayout` and `applyNebulaLayout`** — The most complex layout methods. `applyMatriceLayout` generates positions for a chapter×type grid, applies 80+ dynamic Cytoscape style rules, and draws canvas halos in the same function body. `applyNebulaLayout` uses a custom force-simulation variant outside the standard Cytoscape layout API. Both must remain frozen until a layout adapter interface is designed.

**`DOMContentLoaded` orchestration block** — The composition root. It wires all events, triggers the bootstrap fetch, initializes PanelController, and calls Graph.render() for the first time. Any change here before the event bus is in place amplifies the blast radius of a regression to the entire application boot sequence.

**`cy.on('tap', 'node', ...)` handler** — Do not modify this handler in any way except the spike described in Phase C above. This is the source of the bidirectional coupling and any premature change here silently breaks node selection.

**`StoryMode` internals** — StoryMode depends on both `UI.selectEntity` and `Graph.cy` remaining reachable with their current call signatures. Until the event bus validates the `entity:selected` / `entity:focused` contract, StoryMode must not be touched.

---

## 7. Small corrections only

**Asymmetric `uiFilters` instantiation:**  
`graphe.ui-filters.js` is loaded in the script tag order before the inline `<script>` block, but `Graph` is only declared inside that script block (as an IIFE). The factory `createGrapheUiFilters({ ..., Graph })` receives `Graph` at instantiation time — but `Graph` is declared earlier in the same inline script block as an IIFE, before the `UI` IIFE that calls the factory. This works, but is the one case where the factory receives a module reference that was declared in the same inline block rather than passed from DOMContentLoaded. It is not a bug, but worth noting in `GRAPH_BOUNDARY_PLAN.md` as a dependency ordering detail when Graph becomes an external module (it will need to be importable before `uiFilters` is instantiated).

**`onclick="UI.addAttrRow(...)"` in modal HTML:**  
Lines ~1,388 and ~1,455 of `graphe.html` contain static `onclick` string attributes that call `UI.addAttrRow(...)`. `UI.addAttrRow` is a stub that delegates to `EntityForms.addAttrRow`. This pattern is fragile: if the `UI` object is ever renamed or the stub is removed, these `onclick` strings fail silently. No change is needed now, but the `GRAPH_BOUNDARY_PLAN.md` should note this as a technical debt item for the `DOMContentLoaded` refactor phase.

No other corrections. The architecture is sound and the extraction pattern is consistent across all completed passes.

---

## Summary

| Question | Answer |
|----------|--------|
| Is panel-deeper frozen? | Yes — UI IIFE is at irreducible core, freeze it. |
| Best next branch | Graph boundary planning (audit + design + event bus spike) |
| Story/Scrolly wait? | Yes — blocked by same Graph↔UI coupling as selectEntity |
| Cleanup branch? | No — clearPanel is 3 lines, not worth a branch |
| Workshop expansion? | Independent content work, do on a separate content branch anytime |
| First thing to never touch | selectEntity, applyMatriceLayout, DOMContentLoaded |
| Planning output | GRAPH_BOUNDARY_PLAN.md + graphe.event-bus.js spike |
