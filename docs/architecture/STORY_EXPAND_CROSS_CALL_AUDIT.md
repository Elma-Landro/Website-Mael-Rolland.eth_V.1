# Story Expand Cross-Call Audit

**Branch:** `codex/create-child-branch-for-story-boundary-planning-g24stw`
**Date:** 2026-04-08
**Scope:** Audit only (no runtime changes)

---

## 1) Entry point: Graph node tap/click

```
cy.on('tap',   'node', handleNodeSelect)  // graphe.html:2417
cy.on('click', 'node', handleNodeSelect)  // graphe.html:2418
```

`handleNodeSelect` (graphe.html:2400–2415):

- Guard: `e.target.hasClass('chapter-label')` → return (ghost node, ignore)
- Guard: `!id` → return
- Guard: `_nebulaActive && !_matrixMode && _nebulaZoomDepth === 'archipelago'` → `zoomToChapter(idx); return`
- `State.selectedId = id` — State write
- `UI.renderPanel(id)` — panel DOM update (fires before expand)
- `highlightNeighbors(id)` — cy neighbor highlight (fires before expand)
- `StoryMode.maybeExpandFromNode(id, e.target)` — **direct Graph→Story callback (the seam target)**

---

## 2) `maybeExpandFromNode` (graphe.html:5687–5715)

### Guards (Story-internal state)

- `getStoryPresetById(storyState.activeStoryId)` must return a story
- `storyState.activeStoryStepIndex >= 0`
- `storyState.currentStepRuntime` must exist
- `opts.expandOnClick` must be `true` (from `buildStoryFocusOptions`)
- `node` argument must be present

### Eligibility check — direct cy-node reads

```js
const canExpandFromNode =
  node.hasClass('story-secondary') ||
  (opts.expandFromPrimary && node.hasClass('story-primary'));
if (!canExpandFromNode) return;
```

Reads `story-secondary` and `story-primary` CSS classes directly from the Cytoscape node
argument passed by `handleNodeSelect`. These classes are Graph-rendered state set by a
prior `executeStoryFocusRequest` call.

### Direct `Graph.cy` access

```js
const cy = Graph.cy;   // graphe.html:5695
if (!cy) return;
```

### Edge traversal — direct cy API calls

```js
node.connectedEdges().forEach(edge => {
  if (added >= opts.maxAutoEdges) return;
  const edgeTypeCanonical = canonicalizeRelationName(getEdgeType(edge));
  if (opts.allowedRelationTypes.length && !opts.allowedRelationTypes.includes(edgeTypeCanonical)) return;
  const other = edge.source().id() === node.id() ? edge.target() : edge.source();
  if (other.hasClass('story-muted')) {
    storyState.currentStepRuntime.expandedSecondaryIds.add(other.id());
  }
  storyState.currentStepRuntime.expandedEdgeIds.add(edge.id());
  added += 1;
});
```

Direct cy API calls in this path:
- `node.connectedEdges()` — Cytoscape graph traversal
- `edge.source().id()`, `edge.target().id()` — Cytoscape node identity reads
- `other.hasClass('story-muted')` — reads Graph-rendered CSS class on neighbor node

### Dual-set mutation rule (critical asymmetry)

| Set | Condition for membership |
|-----|--------------------------|
| `expandedEdgeIds` | **Every qualifying edge** (passes `maxAutoEdges` limit AND `allowedRelationTypes` filter) |
| `expandedSecondaryIds` | **Only neighbors** where `other.hasClass('story-muted')` is true at tap time |

These are **not the same set**. An edge to a `story-secondary` or `story-primary` node
still enters `expandedEdgeIds` but does NOT enter `expandedSecondaryIds`.

### Story state mutations

- `storyState.currentStepRuntime.expandedEdgeIds.add(edge.id())` — in-place Set mutation
- `storyState.currentStepRuntime.expandedSecondaryIds.add(other.id())` — in-place Set mutation, conditional

### Downstream calls (if `added > 0`)

- `applyStoryFocus(storyState.currentStepRuntime.resolvedTargets || [], step, storyState.currentStepRuntime)`
  → emits `story:focus-requested` via GrapheEventBus (**already mediated ✓**)
- `updateStoryPanel()` — DOM: `#story-meta`, `#story-step-title`, `#story-step-body`

---

## 3) Interactions with currently mediated event paths

| Event | Used in expand path? | How |
|-------|----------------------|-----|
| `layout:apply-requested` | No | Not involved |
| `story:focus-requested` | Yes (indirect) | `applyStoryFocus` emits it on re-apply after expansion |
| `entity:selected` | No | Not emitted or listened |
| `entity:focused` | No | Not emitted or listened |

The expand seam's own event (`story:expand-from-node-requested`) does **not yet exist**.

---

## 4) `applyStoryStep` interaction

`applyStoryStep` (graphe.html:5661–5676) always constructs a fresh `currentStepRuntime`:

```js
storyState.currentStepRuntime = {
  phase: mergedStep.initialState || 'primaryEdges',
  resolvedTargets,
  expandedSecondaryIds: new Set(),   // ← always empty
  expandedEdgeIds: new Set()         // ← always empty
};
```

**Hard boundary:** step navigation via `goToStoryStep → applyStoryStep` always resets all
expansion state. `maybeExpandFromNode` is not called by this path.

---

## 5) `toggleStoryReveal` interaction

`toggleStoryReveal` (graphe.html:5678–5684) re-calls `applyStoryFocus` with the **same
runtime object**:

```js
storyState.currentStepRuntime.phase = ... toggle ...;
applyStoryFocus(storyState.currentStepRuntime.resolvedTargets || [], step, storyState.currentStepRuntime);
updateStoryPanel();
```

Expansion state **persists** across reveal phase toggles. `expandedSecondaryIds` and
`expandedEdgeIds` are not cleared by `toggleStoryReveal`.

---

## 6) Hidden couplings

- `node.hasClass('story-secondary')` and `node.hasClass('story-primary')` depend on Graph
  having rendered focus classes via a prior `executeStoryFocusRequest`. If Graph class
  semantics change, `maybeExpandFromNode` silently breaks.
- `other.hasClass('story-muted')` reads Graph rendering state inside Story logic to gate
  secondary node inclusion — a hidden read of Graph's visual state.
- `UI.renderPanel(id)` fires before `maybeExpandFromNode` in `handleNodeSelect` — ordering
  is fixed by the current sequential call structure.

---

## 7) Panel state, step state, class toggling

- No `classList.add/remove` inside `maybeExpandFromNode` itself.
- All node/edge class mutations happen inside `executeStoryFocusRequest` on the Graph side,
  dispatched via the already-mediated `story:focus-requested` event.
- `updateStoryPanel()` uses `document.getElementById` — not event-driven.
- `UI.renderPanel` and `maybeExpandFromNode` are independent concerns sharing the same tap
  handler; panel render is not gated on expansion result.
