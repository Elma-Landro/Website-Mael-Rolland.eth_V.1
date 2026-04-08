# Story Expand Seam Plan

**Branch:** `codex/create-child-branch-for-story-boundary-planning-g24stw`
**Date:** 2026-04-08
**Scope:** Planning only (no runtime implementation)

---

## 1) Objective

Define a safe future path to mediate the `handleNodeSelect → StoryMode.maybeExpandFromNode`
direct callback without breaking expand-from-node behavior. This document does not implement
code.

Prior art: the same event-mediation pattern has been validated for `layout:apply-requested`
(layout switching) and `story:focus-requested` (focus execution). The expand seam follows
the same model.

---

## 2) Current responsibility zones

| Zone | Current owner | What it does |
|------|---------------|-------------|
| Node-selection intake | Graph | `cy.on('tap'/'click')`, guards, `State.selectedId`, `UI.renderPanel`, `highlightNeighbors` |
| Expansion eligibility decision | Story (via Graph.cy) | reads `story-secondary` / `story-primary` classes from cy node |
| Edge traversal + filtering | Story (via Graph.cy) | `node.connectedEdges()`, type/count filters, `story-muted` neighbor check |
| Story state mutation | Story | `expandedSecondaryIds.add()`, `expandedEdgeIds.add()` |
| Focus re-apply | Story→Graph (mediated ✓) | `applyStoryFocus` → `story:focus-requested` → `executeStoryFocusRequest` |
| Panel update | Story | `updateStoryPanel()` direct DOM calls |

The seam target is the boundary between **Graph node-selection intake** and **Story expansion
decision + mutation**.

---

## 3) Candidate seam vocabulary

### Primary event (the seam)

```
story:expand-from-node-requested
  Emitted by:   Graph, inside handleNodeSelect (replacing the direct StoryMode call)
  Consumed by:  Story expansion policy listener
  Payload:      { nodeId, nodeClasses, connectedEdges: EdgeDescriptor[] }
```

`EdgeDescriptor` shape:
```js
{
  id:            string,   // edge Cytoscape id
  sourceId:      string,   // edge.source().id()
  targetId:      string,   // edge.target().id()
  relationType:  string,   // canonicalizeRelationName(getEdgeType(edge))
  sourceClasses: string[], // snapshot of edge.source().classes() at tap time
  targetClasses: string[]  // snapshot of edge.target().classes() at tap time
}
```

`nodeClasses` replaces: `node.hasClass('story-secondary')`, `node.hasClass('story-primary')`
`sourceClasses`/`targetClasses` replace: `other.hasClass('story-muted')`

### Optional observability event (not behavioral)

```
story:expand-from-node-applied
  Emitted by:   Story, after state mutation, before re-apply (shadow/debug use only)
  Payload:      { nodeId, addedSecondaryIds: string[], addedEdgeIds: string[] }
```

### Optional signal event (future)

```
story:step-advanced
  Emitted by:   goToStoryStep (signals expansion state reset)
  Payload:      { storyId, stepIndex }
```

---

## 4) Risk classification

### Low-risk — plan first (done in this document)

- Event name + payload contract definition
- Seam vocabulary freeze

### Medium-risk — shadow-mode spike (authorized by contract freeze)

- Graph emits `story:expand-from-node-requested` in `handleNodeSelect` **alongside** the
  existing direct call (shadow mode only)
- Story registers a read-only shadow listener to compare expansion output
- No behavior change until parity is confirmed

### High-risk — not yet

- Removing the direct `StoryMode.maybeExpandFromNode(id, e.target)` call (requires parity)
- Mediating `updateStoryPanel` via events
- Mediating `clearStoryFocus`

### Must not touch in expand seam work

- `applyStoryFocus` internals (already mediated, stable)
- `executeStoryFocusRequest` (Graph side, stable)
- `toggleStoryReveal` (shares runtime, separate concern)
- Scrolly observer wiring

### Must wait for further Graph façade work

- Full removal of `Graph.cy` from `maybeExpandFromNode`
- Anchor scene apply seam (Boundary C from `STORY_FOCUS_SEAM_PLAN.md`)
- Mediating `clearStoryFocus`

---

## 5) Safest sequencing for a future expand seam spike

1. **Contract freeze** (this branch) — freeze event + payload + parity invariants
2. **Shadow-mode spike (new branch)** — Graph emits event + keeps direct call; Story
   listener is read-only comparison only
3. **Parity gate** — confirm identical `expandedSecondaryIds` + `expandedEdgeIds` across
   story presets with `expandOnClick: true`
4. **Promotion (separate pass)** — replace direct call with event-only path once parity
   is confirmed
5. **Observability (optional)** — add `story:expand-from-node-applied` for diagnostics

Each step is a separate branch. Do not combine steps 2 and 4.

---

## 6) Parity invariants a future expand seam must preserve

- Same node ids in `expandedSecondaryIds` for the same tap event
- Same edge ids in `expandedEdgeIds` for the same tap event
- **Dual-set rule preserved**: edge always enters `expandedEdgeIds`; neighbor enters
  `expandedSecondaryIds` only if it had `story-muted` at tap time
- `updateStoryPanel()` called exactly once after expansion (no double-render)
- No expansion when `expandOnClick` is false (guard preserved)
- No expansion when node has neither `story-secondary` nor `story-primary`
- Expansion state survives `toggleStoryReveal` (not reset by phase toggle)
- Expansion state IS reset by step navigation via `applyStoryStep` (hard boundary preserved)
- `UI.renderPanel` and `highlightNeighbors` complete before expansion logic runs

---

## 7) Which parts could later move behind a Graph façade

- Edge traversal (`node.connectedEdges()`) is a natural Graph façade candidate: Graph
  knows its own topology and could return pre-computed edge descriptors on request
- Class reads (`hasClass`) could be replaced by Graph providing node status snapshots
- Neither extraction is needed for the shadow-mode spike; payload construction covers both

---

## 8) Which parts might be better served by an event seam vs. a Graph façade

| Concern | Better via event seam | Better via Graph façade |
|---------|----------------------|------------------------|
| Graph→Story callback | ✓ event seam | — |
| cy traversal in Story | — | ✓ façade provides snapshot |
| Story state mutation | stays in Story | — |
| Focus re-apply | already event seam ✓ | — |

The shadow-mode spike uses the event seam; façade work can follow if needed.

---

## 9) What absolutely must not be touched first

- The `maybeExpandFromNode` function body — unchanged until parity confirmed
- The `applyStoryFocus` → `story:focus-requested` seam — already stable, do not layer
  another change on top
- The `handleNodeSelect` guard logic (chapter-label, archipelago zoom) — unrelated to seam

---

## 10) Explicit out-of-scope for first expand seam implementation

- Rewriting `maybeExpandFromNode` algorithm
- Reworking Graph layout engines
- Removing `Graph.cy` globally
- Broad DOM/scrolly re-architecture
- Mediating `clearStoryFocus` in the same pass
