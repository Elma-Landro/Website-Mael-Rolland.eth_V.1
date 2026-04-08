# Story Focus Cross-Call Audit

**Branch:** `feat/research-architecture-vnext-story-focus-seam-plan`  
**Date:** 2026-04-05  
**Scope:** Audit only (no runtime changes)

---

## 1) `applyStoryFocus` → Graph calls (concrete)

`applyStoryFocus(targetIds, step, runtime)` is directly Graph-coupled through `Graph.cy`:

- acquires Cytoscape instance via `const cy = Graph.cy`
- mutates node classes (`story-primary`, `story-secondary`, `story-bridge`, `story-muted`)
- mutates edge classes (`story-primary`, `story-secondary`, `story-tertiary`, `story-hidden`, `story-backbone`, `story-bridge`)
- computes fit target set and calls `cy.animate({ fit: ... })`
- optionally clamps zoom with follow-up `cy.animate({ center, zoom })`

Key implication:
- Story focus is currently a direct Cytoscape orchestration path, not mediated through a Graph façade.

---

## 2) `clearStoryFocus` → Graph calls

`clearStoryFocus()` is also direct:

- reads `const cy = Graph.cy`
- delegates class reset to `clearStoryFocusClasses(cy)`

Key implication:
- even “clear/reset focus” remains coupled to direct Cytoscape access.

---

## 3) `maybeExpandFromNode` → Graph calls

`maybeExpandFromNode(nodeId, node)` direct coupling points:

- reads `const cy = Graph.cy`
- traverses Cytoscape edges from clicked node (`node.connectedEdges()`)
- updates runtime expansion sets from Cytoscape identities (`edge.id()`, `other.id()`)
- re-enters focus pipeline by calling `applyStoryFocus(...)`

Graph-origin call-in path:
- Graph node-select handler calls `StoryMode.maybeExpandFromNode(id, e.target)` on tap/click.

Key implication:
- expansion behavior is a bidirectional Story↔Graph seam hotspot (Graph event in, Story focus out).

---

## 4) Story focus path → EventBus usage status

Current state:

- `layout:apply-requested` is mediated by `GrapheEventBus` (layout seam spike).
- **No Story focus event mediation exists yet** for:
  - `applyStoryFocus`
  - `clearStoryFocus`
  - `maybeExpandFromNode`

Focus-related calls remain direct function/callback wiring.

---

## 5) Scrolly and anchor interactions touching Story focus

Scrolly observer path currently calls Story focus directly:

- resolves anchor scene focus nodes via `StoryMode.resolveFocusNodes(...)`
- applies scene via `StoryMode.applyStoryFocus(...)`

This path is intentionally untouched and not seam-mediated in current baseline.

---

## 6) Focus-related coupling summary

### Direct Story→Graph coupling
- `applyStoryFocus` → `Graph.cy` heavy usage
- `clearStoryFocus` → `Graph.cy`
- `maybeExpandFromNode` → `Graph.cy`

### Direct Graph→Story coupling
- Graph node-select callback → `StoryMode.maybeExpandFromNode(...)`

### Direct Scrolly→Story coupling
- scrolly observer anchor scene → `StoryMode.applyStoryFocus(...)`

These are the concrete boundaries a future Story focus seam must address.
