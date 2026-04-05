# GRAPH_EXTRACT_SPIKE_CHECKPOINT

Date: 2026-04-05  
Branch: `feat/research-architecture-vnext-graph-extract`

## Scope of this checkpoint
This document freezes what was *actually* completed in the current graph-extract spike phase (Steps 1–4) and what remains intentionally out of scope.

## What has been extracted so far

### Step 1 — Graph styles
- `getCyStyle()` in `graphe.html` now delegates to `window.createGrapheGraphStyles(...)`.
- Extracted module: `graphe.graph-styles.js`.
- Scope extracted: Cytoscape style-array construction only.

### Step 2 — Graph data construction
- `entityToNode()`, `relationToEdge()`, and `buildElements()` in `graphe.html` now delegate to `window.createGrapheGraphData(...)`.
- Extracted module: `graphe.graph-data.js`.
- Scope extracted: pure element/data descriptor construction only.

### Step 3 — Canvas halo overlays
- `_drawHalos()`, `_startHaloOverlay()`, and `_stopHaloOverlay()` in `graphe.html` now delegate to `window.createGrapheCanvasOverlays(...)`.
- Extracted module: `graphe.canvas-overlays.js`.
- Scope extracted: canvas halo lifecycle and draw loop only (with lazy `getCy` access).

### Step 4 — Minimal event-bus spike
- Added tiny bus module `graphe.event-bus.js` (`on`, `off`, `emit`).
- Graph creates a local bus instance and uses it on one narrow path only.

## What the event-bus spike covers exactly
Covered path:
1. `cy.on('tap', 'node', ...)` in Graph
2. emits `entity:selected`
3. local Graph listener receives `entity:selected`
4. applies existing selection behavior (`State.selectedId`, `UI.renderPanel`, neighbor highlight, optional StoryMode expansion)

No additional event types were introduced in this spike.

## What remains intentionally direct
- `cy.on('click', 'node', ...)` remains direct (desktop fallback path).
- Other Graph handlers remain direct (canvas tap/click clear, hover tooltip, zoom-label sync, etc.).
- `selectEntity()` remains unchanged.
- StoryMode and FocusMode modules remain unchanged.
- DOMContentLoaded orchestration remains unchanged.
- Layout methods remain unchanged.

## Why click remains direct while tap is mediated
- This spike is deliberately constrained to one source path to prove the event-bus pattern without widening risk.
- Keeping click direct preserves a fallback path and keeps the diff reversible.
- This allows behavior comparison between mediated tap and direct click under the same branch state before broader migration.

## What this spike successfully demonstrates
- Graph extraction can proceed in small, reversible slices.
- A lazy/dependency-injected module pattern works for style, data, and canvas overlay helpers without broad runtime rewiring.
- EventBus mediation can be introduced for selection flow in a narrowly scoped way without forcing immediate migration of all callers.

## What this spike does NOT demonstrate yet
- It does **not** validate a full event-driven boundary for Graph/UI integration.
- It does **not** migrate `selectEntity() -> Graph.cy.*` coupling.
- It does **not** externalize Graph init/event registration as its own module.
- It does **not** prove listener registration strategy across full DOMContentLoaded orchestration.
- It does **not** cover layout extraction risk.

## Criteria before extending EventBus to more paths
Before extending beyond this spike, confirm all of the following:
1. Manual parity check passes for mediated tap vs mediated click node selection across key layouts.
2. No regression in panel opening, neighbor highlight, and StoryMode optional expansion side effects.
3. Clear decision on next single path to migrate (recommended: `selectEntity() -> Graph.cy.*`).
4. Listener registration order is explicit and documented before first event emission.
5. Extension remains one-path-at-a-time and reversible.

## Freeze assessment
This branch is at a stable checkpoint boundary for the current spike phase.
- **Freeze-ready now:** Yes, if the intent is to pause after validating the conservative extraction + one-path event-bus viability.
- **Continue-ready later:** Yes, with next work constrained to one additional path and explicit parity checks.


## Second narrow spike update (2026-04-05)
- Added one additional event path: `selectEntity(id)` now emits `entity:focused` for Graph-facing effects.
- Graph handles `entity:focused` by applying the same focus side effects previously triggered directly from `selectEntity()` (`cy.animate`, `n.select` when present, and `highlightNeighbors`).
- `selectEntity()` itself remains in place and continues to set `State.selectedId` and render the panel directly.
- Selection parity is now aligned: both tap and click node handlers emit `entity:selected` through the same Graph handler.
- `StoryMode.maybeExpandFromNode(...)` remains a direct call inside `handleNodeSelect`; no `entity:story-expand` event was added in this branch.
- `entity:story-expand` is intentionally out of scope for this checkpoint and remains deferred until StoryMode extraction work.


## Final stabilization update (2026-04-05)
- Kept the second spike (`entity:focused`) and preserved `selectEntity()` in place, but retained only Graph-facing side effects behind the bus.
- Restored tap/click parity by routing both node interactions through the same mediated `entity:selected` path.
- Applied three low-risk cleanups:
  1. `buildElements()` resolves chapter map once and passes it into `entityToNode(...)`.
  2. Canvas overlay logs a warning when `.grc-canvas-wrap` is missing.
  3. Removed unused `TYPE_COLORS` parameter from graph style factory API.
