# Story Seam Frontier Plan

**Branch context:** `feat/research-architecture-vnext-story-boundary-plan`  
**Date:** 2026-04-05  
**Status:** Planning only (no runtime implementation)

---

## 1) Current branch baseline (what already exists)

This branch already provides:

- Story coupling audit: `STORY_CROSS_CALL_AUDIT.md`
- Story boundary/risk sequencing: `STORY_BOUNDARY_PLAN.md`
- Story helper-phase freeze checkpoint: `STORY_HELPERS_CHECKPOINT.md`
- Low-risk helper seam: `graphe.story-helpers.js` (pure helper extraction complete)

Given this baseline, the next work frontier is **not more helper extraction**, but seam planning around Graph and Story interactions.

---

## 2) Problem statement for next phase

Story runtime behavior still depends on high-coupling interfaces in `graphe.html`:

- Story focus engine uses direct `Graph.cy` behavior paths (`applyStoryFocus`).
- Graph node-select path calls Story callback path (`maybeExpandFromNode`).
- Scrolly observer path applies Story scenes directly.

These are coupling seams, not helper candidates.

---

## 3) Target seam outcome (future branch)

A future seam-focused branch should validate **one minimal interaction contract** that allows Story behavior to stop depending on direct cross-IIFE calls.

Two compatible options:

### Option A — Graph façade seam (preferred gateway)
Define a small Story-facing Graph adapter surface (read-only + command endpoints) and route Story calls through that adapter.

### Option B — Event seam (complementary)
Define explicit events for key Story interactions and move direct callback invocation to event emission/consumption.

A combined approach is acceptable, but should start minimal.

---

## 4) Minimal seam contract sketch (planning-only)

### 4.1 Story-facing Graph façade capabilities

Proposed minimal commands (conceptual, not implemented here):

- `graphStory.beginFocusSession(stepConfig)`
- `graphStory.applyFocusTargets(targetIds, runtimeState)`
- `graphStory.clearFocusSession()`
- `graphStory.expandFromNode(nodeId, expansionConfig)`
- `graphStory.applyLayout(layoutTarget)`

Design intent:
- Encapsulate direct Cytoscape access and class operations inside Graph-owned code.
- Preserve Story-mode semantics while reducing Graph internals leakage.

### 4.2 Event seam candidates

Proposed events (conceptual, not implemented here):

- `story:open` / `story:close`
- `story:step-changed`
- `story:expand-from-node-requested`
- `story:scene-apply-requested` (from scrolly anchor activation)

Design intent:
- Replace direct cross-IIFE call edges with explicit payload contracts.
- Allow Story/Graph/scrolly orchestration to evolve independently.

---

## 5) Explicit non-goals for this seam frontier document

- No runtime extraction or implementation in this branch.
- No edits to `applyStoryFocus`.
- No edits to `maybeExpandFromNode`.
- No edits to scrolly observer wiring.
- No edits to Graph/layout methods.

This document only prepares scope for a future seam branch.

---

## 6) Suggested future execution sequence (after this branch)

1. **Pre-flight mapping update**
   - Reconfirm active callsites from `STORY_CROSS_CALL_AUDIT.md` and `GRAPH_BOUNDARY_PLAN.md`.
2. **Seam spike (smallest vertical slice)**
   - Introduce one seam path only (either node-expand request or scrolly scene request).
3. **Stability validation**
   - Verify runtime parity across active story flows and layout modes.
4. **Incremental seam extension**
   - Expand seam coverage only after first seam path is stable.
5. **Only then consider high-coupling extraction**
   - `applyStoryFocus` / `maybeExpandFromNode` behind validated façade/events.

---

## 7) Why this is the correct next frontier

The helper phase is complete and intentionally capped. Remaining complexity is no longer in pure helper code; it is in coupling boundaries among Story, Graph, and scrolly orchestration.

Therefore, the next safe progress is seam planning + seam spike validation, not additional helper extraction.

---

## 8) Seam spike note — Story layout request mediation (2026-04-05)

Implemented in this spike (minimal, behavior-preserving):
- `StoryMode.maybeSwitchLayout(layoutTarget)` now emits `layout:apply-requested` via `GrapheEventBus`.
- Graph registers one listener for `layout:apply-requested` and dispatches to existing layout methods:
  - `applyMonetisationLayout`
  - `applyQuiGouverneLayout`
  - `applyMatriceLayout`
- Existing layout methods were not refactored.
- Added fallback in Story emitter path: if no listener is registered, Story keeps the previous direct-call behavior.

Still intentionally direct/out of scope in this spike:
- Story focus path (`applyStoryFocus`) and Story expansion path (`maybeExpandFromNode`).
- Scrolly observer scene-apply path.
- Any additional event mediation beyond this single Story layout-request path.
