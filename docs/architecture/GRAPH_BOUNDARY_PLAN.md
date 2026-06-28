# Graph Boundary Plan

**Branch:** `feat/research-architecture-vnext-graph-boundary-plan`  
**Date:** 2026-04-05  
**Depends on:** `GRAPH_CROSS_CALL_AUDIT.md` (read that first)  
**Scope:** Boundary design and extraction sequencing only. No runtime changes in this document.

---

## 1. Current Graph responsibility zones

The Graph IIFE (lines 2267–4428, ~2,160 lines) currently owns the following distinct concerns. These are logical zones, not yet separated files.

### Zone A — Bootstrap / init
- **Lines:** 2362–2451
- **Functions:** `init()`
- **Responsibilities:** Creates the Cytoscape instance, attaches the `#cy` container, applies `getCyStyle()`, registers all `cy.on()` event handlers (`tap node`, `click node`, `mouseover`, `zoom`, `viewport`).
- **Cross-boundary calls originate here:** `UI.renderPanel` (line 2384), `UI.clearPanel` (lines 2417, 2425), `StoryMode.maybeExpandFromNode` (line 2387).
- **Extraction blocker:** The event handlers that call `UI.*` cannot be extracted until an event bus or callback injection pattern is in place.

### Zone B — Cytoscape style configuration
- **Lines:** 2453–2822
- **Functions:** `getCyStyle()`
- **Responsibilities:** Returns the full Cytoscape stylesheet as an array (~120 style rules). Includes node size, label visibility, color rules by type, `show-label`/`show-major-label` classes, edge styles, story-mode classes (`story-primary`, `story-secondary`, `story-muted`, `story-hidden`, `story-bridge`, `story-backbone`), highlight classes (`highlighted`, `faded`, `hop2`), scrolly classes (`scrolly-hidden`, `scrolly-active`).
- **Coupling:** References `TYPE_COLORS` (global constant defined earlier in graphe.html). References `isMobileViewport` local variable.
- **Extraction note:** This is a pure configuration function with no side effects. It can be extracted as `graphe.graph-styles.js` once `TYPE_COLORS` is also externalized or passed as a parameter.

### Zone C — Data binding / element construction
- **Lines:** ~2267–2362 (IIFE preamble, `entityToNode`, `relationToEdge`, `buildElements`, helper closures before `init`)
- **Functions:** `entityToNode(entity)`, `relationToEdge(rel, idx)`, `buildElements()`
- **Responsibilities:** Converts GRC-20 entity/relation JSON objects to Cytoscape element descriptors. Reads `State.data`, `State.maps`, `TYPE_COLORS`, `_chapterMap`, `_stratumMap`, `_displayStratumMap` (globals).
- **Coupling:** Depends on `State.maps` for neighbor lookups. References global `TYPE_COLORS`, `TYPE_SHAPES`, `STRATUM_ALWAYS_VISIBLE_NAMES`, `_chapterMap`.
- **Extraction note:** Can be extracted as a stateless factory once the globals it reads are passed as parameters. No DOM or Cytoscape dependency.

### Zone D — Core render / layout dispatch
- **Lines:** 2824–2968
- **Functions:** `render()`, `applyLayout(name)`, `applyFilters()`, `highlightNeighbors(id)`, `resetHighlight()`, `addNode()`, `removeNode()`, `updateNode()`, `addEdge()`, `removeEdge()`, `fit()`
- **Responsibilities:** Rebuilds Cytoscape elements from State, dispatches to the appropriate layout engine, applies type/search filters, manages highlight state, handles incremental CRUD updates.
- **Coupling:** `render()` reads `document.getElementById('layout-select')` to dispatch layout. `applyFilters()` calls `updateStats()` (internal, updates DOM counter). `highlightNeighbors()` calls `cy.animate()` (Cytoscape API).
- **Extraction note:** This is the core rendering API. `applyFilters()` and `highlightNeighbors()` both require `cy` — they must stay co-located with the Cytoscape instance or receive it as a parameter.

### Zone E — Layout engines
- **Lines:** 2969–4333
- **Functions:** `applyNebulaLayout()` (line 2969, ~108 lines), `zoomToChapter()` (3077), `zoomToArchipelago()` (3095), `applyMatriceLayout(useStrata)` (3106, ~458 lines), `restoreTypeColors()` (3564), `applyArbreLayout()` (3629, ~137 lines), `applyMonetisationLayout()` (3766, ~283 lines), `applyQuiGouverneLayout()` (4049, ~285 lines)
- **Responsibilities:** Each layout engine positions nodes in a distinct semantic arrangement. Some engines also apply Cytoscape stylesheet overrides (e.g., `applyMatriceLayout` applies chapter/type color rules via `cy.style()`). Several engines activate the canvas halo overlay via `_startHaloOverlay()`.
- **Coupling:**
  - All engines read `State.data`, `State.maps`, globals (`TYPE_COLORS`, `_chapterMap`, `_stratumMap`, `_displayStratumMap`, `_focusState`).
  - `applyMatriceLayout` and `applyMonetisationLayout` call `_startHaloOverlay(config)` to activate canvas glows.
  - `applyNebulaLayout` maintains internal state flags (`_nebulaActive`, `_nebulaZoomDepth`, `_nebulaPositions`).
  - `restoreTypeColors()` is called when leaving `monetisation` layout; it reverses per-type color overrides.
- **Extraction note:** The layout engines are the highest-risk zone. `applyMatriceLayout` alone is 458 lines with 80+ dynamic `cy.style()` rules. Extraction requires a layout adapter interface that receives `cy`, `State`, `TYPE_COLORS`, and chapter/stratum maps as explicit parameters.

### Zone F — Canvas overlay / halo rendering
- **Lines:** 4334–4428
- **Functions:** `_drawHalos()` (line 4334), `_scheduleHaloDraw()` (4403), `_startHaloOverlay(config)` (4409), `_stopHaloOverlay()` (4417)
- **Responsibilities:** Draws gradient halo overlays on a `<canvas>` element (`#matrix-halo-canvas`) to color-code chapter rows and entity type columns. Uses `cy.extent()`, `cy.zoom()`, `cy.pan()` to project model coordinates to screen pixels.
- **Coupling:** Reads `cy` from closure. Reads `#matrix-halo-canvas` from DOM. Receives configuration object from layout engines (column/row positions, colors). Lifecycle tied to `cy.on('viewport', ...)` and `window.addEventListener('resize', ...)`.
- **Extraction note:** Can become `graphe.canvas-overlays.js` if it receives `(cy, config, canvasId)` as parameters. It is the cleanest sub-zone for early extraction once layout engines are parameterized.

---

## 2. Proposed conceptual sub-zones for future extraction

Listed in extraction-feasibility order (easiest → hardest).

| Sub-zone | Proposed file | Key dependency | Risk |
|----------|--------------|----------------|------|
| Cytoscape style config | `graphe.graph-styles.js` | `TYPE_COLORS` (parameter) | Low |
| Data binding (entityToNode, buildElements) | `graphe.graph-data.js` | `State`, `TYPE_COLORS`, chapter maps (parameters) | Low–Medium |
| Canvas overlay / halo rendering | `graphe.canvas-overlays.js` | `cy` reference, config (parameters) | Medium |
| Core render / filter / highlight | `graphe.graph-core.js` | `cy`, `State` (parameters + event bus) | Medium–High |
| Layout engines (each as a plugin) | `graphe.layout-*.js` | `cy`, `State`, maps, canvas overlay API | High |
| Bootstrap / init (event registration) | `graphe.graph-init.js` | Event bus (must be in place first) | **Highest** |

---

## 3. Proposed event bus contract

A minimal pub/sub event bus (`graphe.event-bus.js`) would decouple the two critical bidirectional paths (Graph→UI and UI→Graph).

### Proposed interface

```javascript
// graphe.event-bus.js (≤30 lines)
const GrapheEventBus = (() => {
  const listeners = {};
  function on(event, cb) {
    if (!listeners[event]) listeners[event] = [];
    listeners[event].push(cb);
  }
  function off(event, cb) {
    if (listeners[event]) listeners[event] = listeners[event].filter(f => f !== cb);
  }
  function emit(event, data) {
    (listeners[event] || []).forEach(cb => cb(data));
  }
  return { on, off, emit };
})();
window.GrapheEventBus = GrapheEventBus;
```

### Required event names and contracts

| Event name | Direction | Emitter | Listener(s) | Payload |
|------------|-----------|---------|-------------|---------|
| `entity:selected` | Graph → UI | Graph `handleNodeSelect` | UI (opens panel, animates) | `{ id: string }` |
| `entity:deselected` | Graph → UI | Graph background tap/click | UI (clears panel) | `{}` |
| `entity:focused` | UI → Graph | UI `selectEntity` | Graph (animate + highlight) | `{ id: string }` |
| `entity:story-expand` | Graph → StoryMode | Graph `handleNodeSelect` | StoryMode (expand on click) | `{ id: string, cyNode: CytoscapeNode }` |
| `filters:changed` | UI/DOMContentLoaded → Graph | filter/search handlers | Graph `applyFilters` | `{ hiddenTypes: Set, searchQ: string }` |
| `layout:apply` | DOMContentLoaded → Graph | layout-select change | Graph layout dispatcher | `{ name: string }` |
| `data:loaded` | Bootstrap → Graph, UI | `onDataLoaded` | Graph `render`, UI `renderTypeFilters` | `{ data: GRC20Data }` |

### Current wiring to replace (Phase C spike target)

The minimal viable spike replaces exactly these two lines:

**Before (lines 2384 and 5033–5038):**
```javascript
// In Graph.handleNodeSelect (line 2384):
UI.renderPanel(id);

// In UI.selectEntity (lines 5033–5038):
const n = Graph.cy && Graph.cy.$id(id);
if (n && n.length) {
  Graph.cy.animate({ center: { eles: n }, zoom: Math.max(Graph.cy.zoom(), 1.2) }, { duration: 300 });
  n.select();
}
Graph.highlightNeighbors(id);
```

**After (Phase C spike only — no structural changes):**
```javascript
// In Graph.handleNodeSelect:
GrapheEventBus.emit('entity:selected', { id });

// In DOMContentLoaded (new listener):
GrapheEventBus.on('entity:selected', ({ id }) => {
  UI.renderPanel(id);
});

// In UI.selectEntity:
GrapheEventBus.emit('entity:focused', { id });

// In DOMContentLoaded (new listener):
GrapheEventBus.on('entity:focused', ({ id }) => {
  const n = Graph.cy && Graph.cy.$id(id);
  if (n && n.length) {
    Graph.cy.animate({ center: { eles: n }, zoom: Math.max(Graph.cy.zoom(), 1.2) }, { duration: 300 });
    n.select();
  }
  Graph.highlightNeighbors(id);
});
```

The spike must be validated on all five layout modes with the v96 canonical graph before being committed. If the spike works, it validates the pattern but does **not** extract the Graph module — that is Phase D work (a future `graph-extract` branch).

---

## 4. Graph facade interface sketch

Once the event bus is in place, the Graph module should expose this minimal public API. Internal helpers (`getCyStyle`, `buildElements`, `entityToNode`, `_drawHalos`, etc.) should be private.

```
Graph (proposed facade)
├── init()                    — boot Cytoscape; register event handlers via EventBus
├── render()                  — full rebuild from State
├── fit()                     — fit all elements in viewport
├── applyLayout(name)         — dispatch to layout engine by name
├── applyFilters()            — apply type/search filters
├── addNode(entity)           — incremental node add
├── removeNode(id)            — incremental node remove
├── updateNode(entity)        — incremental node update
├── addEdge(rel, idx)         — incremental edge add
├── removeEdge(edgeId)        — incremental edge remove
├── highlightNeighbors(id)    — apply hop-1/hop-2 CSS classes
├── resetHighlight()          — clear all highlight classes
├── stopHaloOverlay()         — deactivate canvas overlay (for layout transitions)
├── restoreTypeColors()       — reset after monetisation layout exit
└── (removed from API: get cy())  — no longer exposed; callers use EventBus instead
```

**The key change:** `get cy()` is removed from the public API. Callers that currently hold a direct `cy` reference (`FocusMode._cy()`, `StoryMode.applyStoryFocus`, all Scrolly functions) would need to receive `cy` via callback or subscribe to a new `graph:cy-ready` event. This is the work for the `graph-extract` branch, not this planning branch.

**New methods to add for decoupling:**
- `Graph.resize()` — wraps `cy.resize()` so DOMContentLoaded resize handlers don't need `cy` directly (lines 6468, 6495, 6514, 6540)
- `Graph.clearScrollyClasses()` — wraps `cy.elements().removeClass('highlighted faded scrolly-hidden scrolly-active')` (lines 6539) so Scrolly exit handler doesn't need `cy`

---

## 5. What should remain inline after this planning branch

The following must **not** be moved in the graph-extract branch or in any interim branch. They are listed in priority order (most dangerous to touch first).

1. **`selectEntity(id)` in the UI IIFE** — Cannot move until `entity:focused` event bus listener is in place and tested. This is the upstream half of the bidirectional coupling.

2. **`handleNodeSelect()` and its `cy.on()` registrations** (lines 2374–2392) — Cannot move until `entity:selected` event bus emitter is in place and tested. This is the downstream half.

3. **`applyMatriceLayout(useStrata)` (line 3106, 458 lines)** — Most complex layout. 80+ dynamic `cy.style()` rules, canvas halo activation, chapter/type grid positioning. Must not be touched until layout adapter interface is defined and the style/class contract is documented.

4. **`DOMContentLoaded` block (lines 5873–6555)** — Composition root. Must stay intact until the event bus is validated and all listeners are wired correctly.

5. **`StoryMode` IIFE (lines 5271–5870)** — Calls `Graph.cy` in three internal functions and `Graph.apply*Layout` in `maybeSwitchLayout`. Must wait for the `get cy()` removal and the event bus to be in place.

---

## 6. What absolutely must not be extracted first

**Do not extract the Graph module before the event bus spike is validated.**

If the Graph IIFE is moved to an external file (`graphe.graph.js`) before the `get cy()` accessor is removed and the event bus is in place, the following callers will break silently:

| Caller | Line | Why it breaks |
|--------|------|---------------|
| `UI.selectEntity` | 5033–5038 | `Graph.cy` is now a property on a module that loads after the UI IIFE closes |
| `FocusMode._cy()` | 4513 | Same |
| `StoryMode.applyStoryFocus` | 5457 | `Graph.cy` is undefined at StoryMode evaluation time |
| `StoryMode.clearStoryFocus` | 5601 | Same |
| `StoryMode.maybeExpandFromNode` | 5709 | Same |
| All Scrolly functions | 6230–6541 | `Graph.cy` accessed before Graph script loads |

The safe extraction order is:  
**event bus spike first → Graph module extraction second.**

---

## 7. What can be extracted safely before the event bus

These sub-zones have no cross-boundary calls and can be extracted independently:

### A. `getCyStyle()` → `graphe.graph-styles.js`

**Why safe:** Pure configuration function. Returns a static array of style rules. No DOM manipulation, no State mutation, no event listeners.

**Required change:** Pass `TYPE_COLORS` and mobile breakpoint as parameters instead of reading from closure:
```javascript
// Before (inline):
function getCyStyle() {
  const isMobileViewport = window.innerWidth < 600;
  // ... uses TYPE_COLORS global ...
}

// After (extracted factory):
function createGrapheGraphStyles({ TYPE_COLORS, isMobileViewport }) {
  return getCyStyle();
}
```

**Risk:** Low. If the style array is returned verbatim, no visual change. The only risk is a load-order error if `graphe.graph-styles.js` is loaded before `TYPE_COLORS` is defined — prevent by loading it after `graphe.helpers.js` and `graphe.state.js`.

### B. `entityToNode()` / `relationToEdge()` / `buildElements()` → `graphe.graph-data.js`

**Why safe:** Pure data transformation functions. They convert JSON to Cytoscape descriptors. No DOM writes, no event listeners, no `cy` calls.

**Required change:** Pass `State`, `TYPE_COLORS`, `TYPE_SHAPES`, `_chapterMap`, `_stratumMap`, `_displayStratumMap` as factory parameters.

**Risk:** Low–Medium. `buildElements()` reads `State.maps` for node validity checks. Must ensure State factory is instantiated before this module. Regression test: entity and relation counts must match after extraction.

### C. `_drawHalos()` / `_startHaloOverlay()` / `_stopHaloOverlay()` → `graphe.canvas-overlays.js`

**Why safe:** Self-contained canvas rendering. Receives a `cy` reference and a config object. No calls to `UI.*` or `State.*`.

**Required change:** Extract as a factory receiving `{ cy, canvasId }`:
```javascript
function createGrapheCanvasOverlays({ getCy, canvasId }) {
  function _drawHalos() {
    const cy = getCy();         // lazy getter, called at draw time
    const canvas = document.getElementById(canvasId);
    // ...
  }
  return { startHaloOverlay, stopHaloOverlay, scheduleHaloDraw };
}
```

**Risk:** Medium. The halo draw reads `cy.extent()`, `cy.zoom()`, `cy.pan()` — these are live Cytoscape calls at draw time, not at init time. The `getCy` lazy getter pattern avoids the boot-order problem. The canvas element `#matrix-halo-canvas` must exist in the DOM before this module is initialized.

---

## 8. Safest sequencing for a future `graph-extract` branch

### Step 1 — Extract `getCyStyle()` (no event bus required)
Move Cytoscape style configuration to `graphe.graph-styles.js`. Pure function, no coupling. Validates the extraction pattern for the Graph sub-zone.

**Execution checkpoint (2026-04-05):** Completed conservatively in branch `feat/research-architecture-vnext-graph-extract`.
- `getCyStyle()` now delegates to `window.createGrapheGraphStyles({ TYPE_COLORS, isMobileViewport })`.
- The extracted module (`graphe.graph-styles.js`) contains only style-array construction (no events, no layouts, no buildElements/hydration).
- `graphe.html` script order now includes `graphe.graph-styles.js` before the inline Graph IIFE.

### Step 2 — Extract `entityToNode` / `buildElements` (no event bus required)
Move data binding to `graphe.graph-data.js`. Pure functions, no coupling. Validates parameterization of globals.

**Execution checkpoint (2026-04-05):** Completed conservatively in branch `feat/research-architecture-vnext-graph-extract`.
- `entityToNode()`, `relationToEdge()`, and `buildElements()` now delegate to `window.createGrapheGraphData(...)`.
- The extracted module (`graphe.graph-data.js`) is limited to element/data construction and reads injected dependencies (`State`, `TYPE_COLORS`, `TYPE_SHAPES`, `computeVisualNodeSize`, `getNodeLabel`, `STRATUM_ALWAYS_VISIBLE_NAMES`, `getChapterMap`).
- No Graph init/bootstrap, event wiring, filtering/highlighting, or layout logic was extracted in this pass.

### Step 3 — Extract canvas overlay (no event bus required)
Move halo system to `graphe.canvas-overlays.js` with lazy `getCy` getter. Validates canvas lifecycle separation from layout engines.

### Step 4 — Implement event bus spike (one interaction only)
Add `graphe.event-bus.js`. Replace `handleNodeSelect → UI.renderPanel` (line 2384) and `selectEntity → Graph.cy.*` (lines 5033–5038) with `entity:selected` / `entity:focused` events. Validate on all five layout modes.

### Step 5 — Extract `Graph.init()` events after spike is confirmed
With the event bus in place, move `handleNodeSelect` and `cy.on()` registrations into a `graphe.graph-init.js` module. The module emits `entity:selected` instead of calling `UI.renderPanel` directly.

### Step 6 — Add Graph facade resize helpers
Add `Graph.resize()` and `Graph.clearScrollyClasses()` to the public API. DOMContentLoaded resize handlers and Scrolly exit handler update to use these instead of `Graph.cy.resize()` / `Graph.cy.elements()`.

### Step 7 — Extract layout engines one at a time (highest risk)
Start with `applyArbreLayout` (line 3629, ~137 lines) — smallest and least coupled.  
Then `applyNebulaLayout` (line 2969, ~108 lines) — self-contained, internal state only.  
Then `applyQuiGouverneLayout` and `applyMonetisationLayout`.  
Leave `applyMatriceLayout` (458 lines, halo activation) last.

### Step 8 — Remove `get cy()` from public API
With all external callers migrated to EventBus or new facade methods, remove the `get cy()` accessor from the Graph return object. This is the final step that completes the Graph boundary.

### What not to do in the graph-extract branch
- Do not refactor `StoryMode` in the same branch as Graph extraction.
- Do not touch `DOMContentLoaded` except to wire EventBus listeners.
- Do not attempt to extract all layout engines in one commit.
- Do not remove `get cy()` before all callers are migrated.

---

## 9. Risk summary

| Risk | Severity | Mitigation |
|------|----------|-----------|
| Visual regression in layout modes | Very High | Manual test checklist: all 5 layouts × canonical v96 data before each commit |
| `cy.style()` rule breakage in applyMatriceLayout | High | Extract style rules as a named constant; validate class names match CSS |
| Boot order error (Graph.cy undefined) | High | Use lazy getter pattern; validate with empty state and full v96 data |
| StoryMode callback chain broken | High | Do not touch StoryMode until Graph boundary is complete |
| Canvas halo not rendering after extraction | Medium | Validate `_startHaloOverlay` lifecycle across matrice and monetisation layouts |
| EventBus listener registration order | Medium | Listeners must be registered in DOMContentLoaded before first `entity:selected` emission |
| `onclick="UI.addAttrRow(...)"` HTML fragility | Low | Unrelated to Graph extraction; note for DOMContentLoaded refactor phase |

---

## 10. uiFilters dependency ordering note

`graphe.ui-filters.js` is instantiated inside the `UI` IIFE and receives `Graph` as a factory parameter:
```javascript
const uiFilters = window.createGrapheUiFilters({ document, State, Graph, TYPE_COLORS });
```

Currently this works because `Graph` is declared as an IIFE earlier in the same inline script block, before the `UI` IIFE. When Graph becomes an external file (`graphe.graph.js`), the script load order must ensure `graphe.graph.js` loads **before** the inline script block that declares the `UI` IIFE. Add `<script src="graphe.graph.js"></script>` to the external script load list (currently lines 11–22 of `graphe.html`) before the main inline `<script>` block.

This is not an error today; it is a load-order constraint that must be respected when Graph is externalized.
