# Story Helpers Checkpoint

**Branch target:** `feat/research-architecture-vnext-story-boundary-plan`  
**Date:** 2026-04-05  
**Checkpoint type:** Stabilization (documentation-only)

---

## 1) What low-risk Story helpers are now extracted

The branch now includes `graphe.story-helpers.js`, and `graphe.html` delegates Story helper logic through `window.GrapheStoryHelpers` (with local compatibility fallbacks).

### Extracted helper groups

1. **Registry/data loading + alias/focus resolution**
   - `loadStoryRegistry`
   - `normalizeStoryText`
   - `resolveStoryFocusNodes`
   - `STORY_FOCUS_ALIASES`

2. **Pure step option/state assembly**
   - `mergeStoryStepOptions`

3. **Pure panel text/render content helpers**
   - `getStoryRevealButtonLabel`
   - `formatStoryCitationText`
   - `formatStoryCitationPage`
   - `buildStoryBridgeHintHtml`
   - `getStoryPanelEmptyStateText`
   - `formatStoryStepMetaText`
   - `shouldShowStoryBridgeHint`

This matches the low-risk extraction sequence documented in `STORY_BOUNDARY_PLAN.md` checkpoints (passes 1–3).

---

## 2) What remains intentionally inline

The following remains inline in `graphe.html` by design:

- `StoryMode.applyStoryFocus` and direct `Graph.cy`-dependent Story focus behavior.
- `StoryMode.maybeExpandFromNode` callback path (Graph node-select seam).
- Story panel DOM querying and DOM mutation flow (only pure value assembly is extracted).
- Scrolly / anchored-scrolly observer wiring and scene activation path.
- Graph layout/mode orchestration wiring.

---

## 3) Why high-coupling Story paths were not touched

These paths are explicitly deferred because they are runtime-critical coupling points:

- `applyStoryFocus` is tightly coupled to Cytoscape class semantics, fit/zoom/camera behavior, and reveal-phase transitions.
- `maybeExpandFromNode` is a live Graph-event callback seam and is sensitive to click semantics and expansion side effects.
- Scrolly observer wiring crosses DOM observer lifecycle, anchor state, and Story scene activation timing.

Changing these in a helper pass would exceed low-risk scope and risks behavior drift.

---

## 4) What this branch now demonstrates

This branch now demonstrates that:

- Progressive, behavior-preserving Story helper extraction is feasible.
- Story data/alias/step/text helper logic can be separated without refactoring Graph-coupled runtime paths.
- A stable helper seam exists (`graphe.story-helpers.js`) for low-risk logic reuse and future test harnessing.

---

## 5) What this branch does *not* demonstrate yet

This branch does **not** yet demonstrate:

- A Graph façade replacing direct `Graph.cy` usage for Story focus/exploration.
- An event seam replacing direct cross-IIFE callback coupling.
- A decoupled Story module boundary for `applyStoryFocus` / `maybeExpandFromNode`.
- A split of anchored-scrolly orchestration from Story activation.

---

## 6) Why helper extraction should stop here

Helper extraction should stop here because the remaining candidates are no longer low-risk pure helpers; they are coupling seams between Story, Graph, and scrolly orchestration.

Continuing “helper extraction” beyond this point would become disguised runtime refactoring and violate the conservative scope of this branch.

---

## 7) Next future frontier (not in this branch)

The next safe frontier is seam planning/implementation in a future branch:

1. Introduce a minimal **Graph façade seam** for Story-required operations.
2. Define/validate a small **Story event seam** (e.g., graph-node expansion and scrolly scene apply events).
3. Only after seam stability, evaluate extraction of `applyStoryFocus` / `maybeExpandFromNode` behind adapters.

This checkpoint therefore marks the current branch as a stable planning/helper milestone, not an extraction branch for high-coupling runtime behavior.
