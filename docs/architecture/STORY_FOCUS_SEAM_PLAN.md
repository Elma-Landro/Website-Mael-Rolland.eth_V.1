# Story Focus Seam Plan

**Branch:** `feat/research-architecture-vnext-story-focus-seam-plan`  
**Date:** 2026-04-05  
**Scope:** Planning only (no runtime implementation)

---

## 1) Objective for next phase

Prepare a future seam branch that can reduce direct Story focus coupling (`Graph.cy` + direct callback calls) **without** refactoring layout internals, scrolly observer internals, or Story focus algorithms in the first seam step.

---

## 2) What must remain unchanged in this planning branch

- No code extraction of `applyStoryFocus`
- No code extraction of `maybeExpandFromNode`
- No scrolly observer wiring edits
- No Graph/layout method refactors
- No new runtime event path implementation in this branch

This document is only a pre-implementation seam blueprint.

---

## 3) Candidate seam boundaries (conceptual)

### Boundary A — Focus apply request seam
Concept:
- Story emits a focus-apply request with resolved target IDs + step/runtime payload.
- Graph-owned adapter performs Cytoscape class/fit work.

Purpose:
- remove direct `Graph.cy` access from Story focus entrypoint over time.

### Boundary B — Expand-from-node request seam
Concept:
- Graph node-select emits “story expand request” payload.
- Story expansion policy decides state update and requests a re-apply focus.

Purpose:
- make Graph→Story callback explicit and contract-driven.

### Boundary C — Anchor scene apply seam
Concept:
- Scrolly anchor activation emits “story scene apply request”.
- Story/Graph adapter executes focus application.

Purpose:
- decouple observer code from direct Story function call.

---

## 4) Safest sequencing (future branch)

1. **Contract-only step**
   - Define event names + payload contracts in docs/tests first.
2. **Single-path spike**
   - Mediate one path only (recommended first: anchor scene apply OR expand-from-node request, not both).
3. **Parity gate**
   - Verify no behavior drift on focus classes, edge reveal states, and camera fit behavior.
4. **Incremental extension**
   - Add next focus seam path only after first path parity is confirmed.

---

## 5) Parity invariants a future seam branch must preserve

- Story focus class semantics stay identical (`story-primary`, `story-secondary`, `story-muted`, etc.)
- Reveal-phase behavior remains identical (`nodesOnly` vs `primaryEdges`)
- Expansion behavior remains identical (`expandOnClick`, edge limits, allowed relation filters)
- Camera fit/zoom behavior remains identical for each story step

If any invariant changes, treat as regression.

---

## 6) Explicit out-of-scope for first focus seam implementation

- Rewriting `applyStoryFocus` algorithm
- Reworking layout engines
- Removing `Graph.cy` globally in one pass
- Broad DOM/scrolly re-architecture

---

## 7) Decision checkpoint

This branch should end at planning artifacts only.

A future dedicated implementation branch should pick **one** focus seam path, enforce parity checks, and stop before broadening scope.

---

## 8) Seam spike note — Story focus request mediation (2026-04-08)

Implemented in this spike:
- `applyStoryFocus(...)` still computes story focus targets/options in StoryMode.
- Graph-execution portion is now mediated by `story:focus-requested`:
  - Story emits `GrapheEventBus.emit('story:focus-requested', request)`.
  - Graph listens and runs `executeStoryFocusRequest(request)`.
- Compatibility fallback is kept: if no listener handles the event, Story calls `Graph.executeStoryFocusRequest(request)` directly.

Intentionally unchanged in this spike:
- `clearStoryFocus` remains direct.
- `maybeExpandFromNode` remains direct.
- Scrolly observer wiring remains direct.
- No additional focus seam path was introduced.
