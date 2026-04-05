# Graph Cross-Call Audit

**Branch:** `feat/research-architecture-vnext-graph-boundary-plan`  
**Date:** 2026-04-05  
**File audited:** `graphe.html` (6,555 lines)  
**Scope:** Enumerate every cross-boundary call between Graph, UI, Editor, FocusMode, StoryMode, Scrolly, and DOMContentLoaded. No code changes.

---

## 1. Graph IIFE → UI calls

The Graph IIFE (`const Graph = (() => {...})();`, line 2267) contains `handleNodeSelect`, registered as the Cytoscape tap/click handler. This is the only location inside the Graph IIFE that calls outward to `UI`.

| Call | Location | Trigger | Notes |
|------|----------|---------|-------|
| `UI.renderPanel(id)` | line 2384 | node tap or click | Inside `handleNodeSelect()`. Fires on every node selection event. |
| `UI.clearPanel()` | line 2417 | background tap (canvas) | Inside `cy.on('tap', e => {...})` — fires when user taps empty canvas. |
| `UI.clearPanel()` | line 2425 | background click (canvas) | Inside `cy.on('click', e => {...})` — desktop fallback for the above. |

**Conclusion:** Graph calls `UI` in exactly three locations, all inside `init()`. Two of the three are identical and could be unified. The entry point of the bidirectional coupling is `handleNodeSelect` at line 2374 → `UI.renderPanel` at line 2384.

---

## 2. Graph IIFE → StoryMode call

| Call | Location | Trigger | Notes |
|------|----------|---------|-------|
| `StoryMode.maybeExpandFromNode(id, e.target)` | line 2387 | node tap or click | Inside `handleNodeSelect()`, guarded by `typeof StoryMode !== 'undefined'`. Called after `UI.renderPanel`. |

This is a **one-way** call: Graph → StoryMode. StoryMode does not call back into Graph from `maybeExpandFromNode` directly — it only reads `Graph.cy` to traverse edges and calls `applyStoryFocus` internally.

---

## 3. Graph IIFE cy.on() event registrations

All registered inside `Graph.init()` (line 2362).

| Event | Line | Handler | Cross-boundary call |
|-------|------|---------|---------------------|
| `cy.on('tap', 'node', handleNodeSelect)` | 2391 | `handleNodeSelect` | → `UI.renderPanel`, → `StoryMode.maybeExpandFromNode` |
| `cy.on('click', 'node', handleNodeSelect)` | 2392 | `handleNodeSelect` | Same as above (desktop fallback) |
| `cy.on('mouseover', 'node', ...)` | 2396 | inline tooltip handler | No cross-boundary call; only manipulates `#cy-tooltip` DOM directly |
| `cy.on('mousemove', 'node', ...)` | 2406 | inline tooltip handler | No cross-boundary call; tooltip position only |
| `cy.on('mouseout', 'node', ...)` | 2410 | inline tooltip handler | No cross-boundary call |
| `cy.on('tap', e => {...})` | 2412 | background tap | → `UI.clearPanel()` |
| `cy.on('click', e => {...})` | 2420 | background click | → `UI.clearPanel()` |
| `cy.on('zoom', syncLabels)` | 2448 | zoom change | No cross-boundary call; `syncLabels()` is a Graph-internal function |
| `cy.on('viewport', _scheduleHaloDraw)` | 4412 | viewport pan/zoom | No cross-boundary call; fires `_drawHalos()` which reads canvas DOM only |

**The two coupling-bearing events are `tap node` / `click node` (lines 2391–2392).** All other `cy.on` registrations are self-contained.

---

## 4. UI IIFE → Graph calls

The UI IIFE (`const UI = (() => {...})();`, line 4982) calls Graph in exactly one function: `selectEntity`.

### `selectEntity(id)` — lines 5030–5040

```javascript
function selectEntity(id) {
  State.selectedId = id;          // State mutation — no Graph call
  renderPanel(id);                // Internal UI call
  const n = Graph.cy && Graph.cy.$id(id);   // line 5033 — Graph.cy getter
  if (n && n.length) {
    Graph.cy.animate(             // line 5035 — Graph.cy.animate()
      { center: { eles: n }, zoom: Math.max(Graph.cy.zoom(), 1.2) },
      { duration: 300 }
    );
    n.select();                   // Cytoscape node selection
  }
  Graph.highlightNeighbors(id);   // line 5038 — Graph method call
}
```

| Call | Line | Notes |
|------|------|-------|
| `Graph.cy` (getter) | 5033 | Reads the live Cytoscape instance. Not a method call — accesses the `get cy()` accessor. |
| `Graph.cy.animate(...)` | 5035 | Triggers animated pan+zoom to center the selected node. |
| `Graph.cy.zoom()` | 5035 | Reads current zoom level inside the animate call. |
| `Graph.highlightNeighbors(id)` | 5038 | Applies `highlighted`/`faded`/`hop2` CSS classes on Graph elements. |

**This is the half of the bidirectional loop that prevents `selectEntity` from being extracted.** `selectEntity` requires `Graph.cy` to animate, and `Graph.cy` is only available as an accessor on the inline Graph IIFE.

### Guided overlay (inside `showGuidedOverlay()`, lines 5155–5268)

These are called from within the guided overlay setup function which is invoked from `onDataLoaded()` / DOMContentLoaded — not strictly the `UI` IIFE, but co-located UI logic.

| Call | Line | Context |
|------|------|---------|
| `Graph.applyFilters()` | 5188 | After hiding types from semantic family click |
| `UI.selectEntity(e.id)` | 5216 | After search suggestion click in guided overlay |
| `Graph.applyFilters()` | 5228 | After "Matrice" CTA click |
| `Graph.applyMatriceLayout()` | 5229 | After "Matrice" CTA click |
| `Graph.applyFilters()` | 5239 | After "Monétisation" CTA click |
| `Graph.restoreTypeColors()` | 5240 | After "Monétisation" CTA click |
| `Graph.applyMonetisationLayout()` | 5241 | After "Monétisation" CTA click |
| `Graph.applyNebulaLayout()` | 5250 | After "Archipel" CTA click |
| `Graph.applyFilters()` | 5261 | After "Moyen" filter click |

---

## 5. Editor IIFE → Graph calls

The Editor IIFE (`const Editor = (() => {...})();`, line 4819) mutates State and then calls Graph to sync the visual layer.

| Call | Line | Method | Trigger |
|------|------|--------|---------|
| `Graph.addNode(entity)` | 4841 | `addNode(entity)` | After `addEntity()` creates a new entity |
| `Graph.updateNode(entity)` | 4863 | `updateNode(entity)` | After `editEntity()` modifies an entity |
| `Graph.removeNode(id)` | 4885 | `removeNode(id)` | After `deleteEntity()` removes an entity |
| `Graph.addEdge(rel, idx)` | 4903 | `addEdge(rel, idx)` | After `addRelation()` creates a new relation |
| `Graph.render()` | 4930 | `render()` | After `deleteRelation()` — full re-render needed (edge IDs shift) |
| `Graph.applyFilters()` | 4953 | `applyFilters()` | Inside `refreshUI()` after any CRUD |

---

## 6. Editor IIFE → UI calls

| Call | Line | Trigger |
|------|------|---------|
| `UI.renderPanel(id)` | 4865 | After `editEntity()` — refresh panel with updated data |
| `UI.clearPanel()` | 4888 | After `deleteEntity()` — entity no longer exists |
| `UI.renderPanel(State.selectedId)` | 4904 | After `addRelation()` — refresh panel if adding rel from selected entity |
| `UI.renderPanel(State.selectedId)` | 4931 | Inside `refreshUI()` — refresh if selection still valid |

---

## 7. FocusMode IIFE → Graph calls

The FocusMode IIFE (`const FocusMode = (() => {...})();`, line 4432) accesses Graph.cy exclusively via a private helper.

| Call | Line | Notes |
|------|------|-------|
| `function _cy() { return Graph.cy; }` | 4513 | Private accessor; FocusMode uses `_cy()` internally whenever it needs the Cytoscape instance. No Graph method calls other than via this accessor. |

FocusMode reads/writes Cytoscape element classes directly (`.addClass`, `.data()`, `.forEach`, etc.) but does not call any named Graph methods. It bypasses the Graph API entirely by holding a live `cy` reference.

---

## 8. StoryMode IIFE → Graph calls

The StoryMode IIFE (`const StoryMode = (() => {...})();`, line 5271) accesses Graph exclusively via `Graph.cy`.

| Call | Line | Function | Notes |
|------|------|----------|-------|
| `const cy = Graph.cy;` | 5457 | `applyStoryFocus()` | Used to query and classify all nodes/edges for story focus rendering |
| `const cy = Graph.cy;` | 5601 | `clearStoryFocus()` | Used to remove all story CSS classes |
| `const cy = Graph.cy;` | 5709 | `maybeExpandFromNode()` | Used to traverse connected edges and expand secondary nodes on click |
| `Graph.applyMonetisationLayout()` | 5756 | `maybeSwitchLayout()` | Called by `openStory()` when a story requires a specific layout |
| `Graph.applyQuiGouverneLayout()` | 5757 | `maybeSwitchLayout()` | Same |
| `Graph.applyMatriceLayout()` | 5758 | `maybeSwitchLayout()` | Same |

StoryMode does **not** call any Graph helper methods (`highlightNeighbors`, `applyFilters`, etc.). It bypasses the Graph API by holding the `cy` reference directly and manipulating classes via `cy.nodes().forEach(...)` and `cy.edges().forEach(...)`.

---

## 9. StoryMode IIFE → UI calls

StoryMode does **not** call `UI.*` directly. Instead:

- StoryMode is triggered FROM Graph via `handleNodeSelect` → `StoryMode.maybeExpandFromNode` (line 2387)
- StoryMode is triggered FROM DOMContentLoaded via `StoryMode.applyStoryFocus()` (line 6437) and `StoryMode.closeStory()` (line 6504)
- StoryMode is initialized via `StoryMode.init()` (line 6550) in DOMContentLoaded

**There are no `UI.*` call sites inside the StoryMode IIFE.** StoryMode manages its own panel (`#story-mode-panel`) and DOM elements independently from the entity detail panel managed by `UI`.

---

## 10. Scrolly functions → Graph calls

The scrollytelling functions (lines 6220–6370, inline below DOMContentLoaded) access Graph.cy directly.

| Call | Line | Function | Notes |
|------|------|----------|-------|
| `const cy = Graph.cy;` | 6230 | `applyScrollyFocus(visibleNodeIds)` | Classifies all nodes as highlighted/scrolly-hidden |
| `const cy = Graph.cy;` | 6249 | `highlightByTypes(types)` | Filters nodes by type name via `cy.nodes().forEach()` |
| `const cy = Graph.cy;` | 6270 | `highlightByChapter(chapterId)` | Finds relations to chapter, calls `applyScrollyFocus()` |
| `const cy = Graph.cy;` | 6287 | `highlightBySection(sectionKey)` | Finds section entity, calls `applyScrollyFocus()` |
| `Graph.cy.resize()` | 6468 | DOMContentLoaded resize handler | Window resize → Cytoscape resize |
| `Graph.cy.resize()` | 6495 | Sidebar toggle | After sidebar open/close, canvas needs resize |
| `Graph.cy.resize()` | 6514 | Panel toggle | After panel open/close |
| `Graph.cy.elements().removeClass(...)` | 6539 | Scrolly mode toggle OFF | Removes all scrolly CSS classes when leaving scrolly mode |
| `Graph.cy.resize()` | 6540 | Scrolly mode toggle OFF | Canvas resize after layout change |
| `Graph.fit()` | 6541 | Scrolly mode toggle OFF | Re-fit the view after leaving scrolly mode |

---

## 11. DOMContentLoaded → Graph calls (lines 5873–6555)

Key Graph calls in the event-wiring block, not counting scrolly or resize handlers above.

| Call | Line | Context |
|------|------|---------|
| `Graph.render()` | 5858 | Inside `onDataLoaded()` — first render after data load |
| `Graph.applyNebulaLayout()` | 5929 | Layout select change handler (`nebulae`) |
| `Graph.restoreTypeColors()` | 5931 | Layout select change handler (leaving `monetisation`) |
| `Graph.applyMatriceLayout()` | 5932 | Layout select change handler (`matrice`) |
| `Graph.applyArbreLayout()` | 5933 | Layout select change handler (`arbre`) |
| `Graph.applyQuiGouverneLayout()` | 5934 | Layout select change handler (`qui-gouverne`) |
| `Graph.applyLayout(v)` | 5935 | Layout select change handler (generic cose/dagre/etc.) |
| `Graph.fit()` | 5950 | Fit button click |
| `Graph.applyFilters()` | 5959 | Entity type filter toggle |
| `Graph.applyMatriceLayout()` | 5961 | Strata toggle (show strata variant) |
| `Graph.applyMatriceLayout(_matrixStrataMode)` | 5971 | Strata toggle (restore non-strata) |
| `Graph.applyFilters()` | 5977 | Search input |
| `Graph.applyFilters()` | 5982 | Show-relations-only toggle |
| `Graph.applyFilters()` | 5989 | Hide-isolated-nodes toggle |
| `Graph.applyFilters()` | 5995 | Type filter checkbox click |
| `Graph.render()` | 6001 | After undo |

---

## 12. The selectEntity callback chain (complete map)

### Path A: Cytoscape tap → panel render

```
user taps / clicks a node on canvas
  → cy.on('tap', 'node', handleNodeSelect)   [line 2391]
  → handleNodeSelect(e)                       [line 2374]
      State.selectedId = id                   [line 2383]
      UI.renderPanel(id)                      [line 2384] ← Graph → UI
      highlightNeighbors(id)                  [line 2385, internal to Graph]
      StoryMode.maybeExpandFromNode(id, …)   [line 2387] ← Graph → StoryMode
        StoryMode uses Graph.cy              [line 5709]
        may call applyStoryFocus()           [internal StoryMode]
          uses Graph.cy                      [line 5457]
```

### Path B: Guided overlay search result click → entity select

```
user clicks a search suggestion in guided overlay
  → item.addEventListener('click', ...)      [~line 5210]
      Graph.applyFilters()                   [line 5215]
      UI.selectEntity(e.id)                  [line 5216] ← DOMContentLoaded UI helper → UI
        → selectEntity(id)                   [line 5030]
            State.selectedId = id            [line 5031]
            renderPanel(id)                  [line 5032, internal UI]
            Graph.cy.$id(id)                 [line 5033] ← UI → Graph
            Graph.cy.animate(...)            [line 5035] ← UI → Graph
            Graph.highlightNeighbors(id)     [line 5038] ← UI → Graph
```

### Path C: After addEntity — deferred selectEntity

```
DOMContentLoaded confirm-add-entity handler
  → Editor.addEntity(...)                    [~line 6020]
      Graph.addNode(entity)                  [line 4841] ← Editor → Graph
  setTimeout(
    () => UI.selectEntity(newId), 100        [line 6028] ← DOMContentLoaded → UI → Graph
  )
```

**The Graph ↔ UI cycle in Path A is the primary extraction blocker.** Graph calls `UI.renderPanel` on tap; UI's `selectEntity` calls `Graph.cy.animate`. These two lines are the minimal cut that would need an event bus to separate.

---

## 13. Canvas overlay coupling points

The Graph IIFE contains a canvas-based halo drawing subsystem that is tightly coupled to both layout state and DOM.

| Element | Access point | Line | Notes |
|---------|-------------|------|-------|
| `#matrix-halo-canvas` | `document.getElementById(...)` | Inside `_drawHalos()`, ~line 4334 | Direct DOM access within Graph IIFE |
| `cy.extent()`, `cy.zoom()`, `cy.pan()` | Cytoscape API | Inside `_drawHalos()` | Converts model coordinates to screen coordinates for halo positioning |
| `cy.on('viewport', _scheduleHaloDraw)` | Cytoscape event | line 4412 | Fires `_drawHalos` on every pan or zoom (debounced via `requestAnimationFrame`) |
| `window.addEventListener('resize', _scheduleHaloDraw)` | Window event | Inside `_startHaloOverlay()` | Canvas must redraw on window resize |
| `cancelAnimationFrame(_haloRAF)` | Browser API | Inside `_stopHaloOverlay()` | Cleanup on layout change |

**The canvas overlay subsystem (`_drawHalos`, `_startHaloOverlay`, `_stopHaloOverlay`) is activated from within layout methods** (specifically `applyMatriceLayout` and `applyMonetisationLayout`). It reads `cy.extent()` / `cy.zoom()` / `cy.pan()` to project model-space column/row positions onto screen-space canvas pixels. It cannot be separated from the Graph module without either:
1. Passing a `cy` reference explicitly, or
2. Receiving model→screen projection callbacks

---

## 14. Graph module public API surface (complete)

The Graph IIFE return statement (end of Graph IIFE, ~line 4425):

```javascript
return {
  init,
  render,
  applyLayout,
  applyNebulaLayout,
  applyMatriceLayout,
  applyArbreLayout,
  applyMonetisationLayout,
  applyQuiGouverneLayout,
  zoomToChapter,
  zoomToArchipelago,
  restoreTypeColors,
  applyFilters,
  addNode,
  removeNode,
  updateNode,
  addEdge,
  removeEdge,
  fit,
  highlightNeighbors,
  resetHighlight,
  stopHaloOverlay: _stopHaloOverlay,
  get cy() { return cy; }        // ← live Cytoscape instance accessor
};
```

**The `get cy()` accessor is the root of most cross-boundary coupling.** Every external module that accesses `Graph.cy` directly is bypassing the Graph API and manipulating the Cytoscape instance without going through any abstraction layer. Modules that do this: `UI.selectEntity` (line 5033), `FocusMode._cy()` (line 4513), `StoryMode.applyStoryFocus` (line 5457), `StoryMode.clearStoryFocus` (line 5601), `StoryMode.maybeExpandFromNode` (line 5709), all four Scrolly functions (lines 6230, 6249, 6270, 6287), and DOMContentLoaded resize handlers (lines 6468, 6495, 6514, 6538–6541).

---

## 15. Summary: coupling severity matrix

| Caller | Callee | Call type | Line(s) | Severity |
|--------|--------|-----------|---------|----------|
| Graph.handleNodeSelect | UI.renderPanel | direct call | 2384 | **Critical** (bidirectional loop) |
| Graph (background tap) | UI.clearPanel | direct call | 2417, 2425 | High |
| Graph.handleNodeSelect | StoryMode.maybeExpandFromNode | direct call | 2387 | Medium |
| UI.selectEntity | Graph.cy (getter) | property access | 5033, 5035 | **Critical** (bidirectional loop) |
| UI.selectEntity | Graph.highlightNeighbors | direct call | 5038 | High |
| Editor.* | Graph.addNode/removeNode/updateNode/addEdge/removeEdge/render/applyFilters | direct calls | 4841–4953 | High |
| Editor.* | UI.renderPanel/clearPanel | direct calls | 4865–4931 | High |
| FocusMode | Graph.cy (getter) | property access | 4513 | Medium (contained via `_cy()`) |
| StoryMode.applyStoryFocus | Graph.cy (getter) | property access | 5457 | High |
| StoryMode.clearStoryFocus | Graph.cy (getter) | property access | 5601 | Medium |
| StoryMode.maybeExpandFromNode | Graph.cy (getter) | property access | 5709 | Medium |
| StoryMode.maybeSwitchLayout | Graph.applyMonetisationLayout/QuiGouverneLayout/MatriceLayout | direct calls | 5756–5758 | Medium |
| Scrolly functions | Graph.cy (getter) | property access | 6230–6287 | Medium |
| DOMContentLoaded | Graph.* (many methods) | direct calls | 5858–6001 | Medium (orchestration root) |
| DOMContentLoaded resize | Graph.cy.resize() | direct call | 6468–6541 | Low (safe to keep) |
