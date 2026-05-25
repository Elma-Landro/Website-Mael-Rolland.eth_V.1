# STORY_EXPAND_SEAM_VALIDATION_RESULT

## Validation mode
- **Type:** implementation-level validation (runtime UI instrumentation not executed in this environment).
- **Scope:** shadow-mode expand seam parity only.

## What was checked

1. **Selection path ordering**
   - `handleNodeSelect` still executes in this order:
     1) `UI.renderPanel(id)`
     2) `highlightNeighbors(id)`
     3) emit `story:expand-from-node-requested`
     4) direct `StoryMode.maybeExpandFromNode(id, e.target)`

2. **Payload builder contract alignment**
   - `buildExpandFromNodeRequestedPayload(...)` includes:
     - `nodeId`
     - node class snapshot
     - connected edge snapshot
     - frozen candidate edge descriptors (`edgeId/sourceId/targetId/otherNodeId/relationTypeCanonical/otherNodeRole`)
     - `expandOptionsSnapshot` and `runtimeSnapshot`

3. **Parity reconstruction logic**
   - Shadow comparator gate logic mirrors direct behavior gates:
     - `expandOnClick`
     - node-role eligibility (`secondary` or `primary` with `expandFromPrimary`)
   - `allowedRelationTypes` filtering is applied before acceptance.
   - `maxAutoEdges` cap is consumed only by accepted edges (filtered edges do not consume cap).

4. **No behavioral mutation from shadow listener**
   - Listener computes expectations and logs parity/mismatch only.
   - Listener does not mutate `storyState`.
   - Listener does not call `applyStoryFocus`.
   - Listener does not call `updateStoryPanel`.

5. **State-lifecycle parity surfaces**
   - Reveal toggle path remains direct (`toggleStoryReveal -> applyStoryFocus + updateStoryPanel`).
   - Step change remains direct reset path (`applyStoryStep` reinitializes runtime sets).
   - Panel update after expansion remains on direct path only (`maybeExpandFromNode` when `added > 0`).

## Validation outcome
- **Parity status by implementation inspection:** **holds** for inspected priority cases:
  - `expandOnClick` gating
  - `allowedRelationTypes` filtering
  - `maxAutoEdges` accepted-edge semantics
  - reveal/step lifecycle interaction surfaces
  - no shadow-side mutation or rendering calls

## Runtime observation status
- Runtime console validation (`[StoryExpandShadow]`) was **not directly observed** in this pass.
- This result is based on strongest available code-path inspection.

## Fixes required
- **No parity fix required** in this pass.

## Intentionally direct (unchanged)
- `StoryMode.maybeExpandFromNode(...)` remains authoritative source of truth.
- Shadow mode remains comparison-only instrumentation.
- No seam-authoritative switch introduced.

## Readiness / stop condition
- The shadow-mode spike is **ready to stop here**.
- Next work should be optional manual runtime parity sampling (developer-run console checks), not architecture broadening.
