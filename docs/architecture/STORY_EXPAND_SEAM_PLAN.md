# STORY_EXPAND_SEAM_PLAN

## Scope and intent
This plan defines the safest future seam for expand-from-node behavior, based on current runtime coupling. This pass is planning-only and preserves current behavior assumptions.

## 1) Responsibility zones (future seam target model)

### Zone A — Graph selection boundary (keep first)
- Owns Cytoscape node tap/click capture (`handleNodeSelect`).
- Must keep existing ordering where panel selection render occurs before any Story expand request.

### Zone B — Story expand policy (candidate extraction zone)
- Owns step-option gating (`expandOnClick`, `expandFromPrimary`, relation filters, limits).
- Owns mutation policy for runtime expansion sets.
- Should not directly depend on Cytoscape classes/collections after seaming.

### Zone C — Focus render executor (already partially mediated)
- Owns mapping runtime sets into class application/camera.
- Already aligned to event mediation via `story:focus-requested` + Graph execution.

## 2) Candidate seam vocabulary

Recommended names for a minimal, explicit expand seam:
- `story:expand-from-node-requested` (Graph -> Story expand policy)
- `story:expand-from-node-resolved` (optional diagnostic/telemetry response)
- `story:focus-requested` (existing downstream render contract; unchanged initially)

Keep vocabulary intentionally narrow; avoid introducing generic graph traversal events in first spike.

## 3) Required payload for future `story:expand-from-node-requested`

Payload should carry all data currently read implicitly from Cytoscape class state and graph handles.

Minimum required fields:
- `nodeId`: selected node id.
- `stepIndex`: active step index (or sufficient story-step identity).
- `runtimeSnapshot`:
  - `phase`,
  - `expandedSecondaryIds[]`,
  - `expandedEdgeIds[]`.
- `expandOptionsSnapshot`:
  - `expandOnClick`, `expandFromPrimary`,
  - `maxAutoEdges`,
  - `allowedRelationTypes[]` (canonicalized).
- `nodeRole` (explicit role state replacing class read):
  - one of `primary | secondary | bridge | muted | hidden | unknown`.
- `candidateEdges[]` replacing direct `connectedEdges()` traversal:
  - `edgeId`, `sourceId`, `targetId`, `relationTypeCanonical`,
  - `otherNodeId` (relative to selected node),
  - `otherNodeRole` (explicit role snapshot).

Optional but useful:
- `selectionContext`: `{ from: 'tap' | 'click' | ... }`.
- `storyId` for telemetry and mismatch detection.

## 4) Why payload must replace class and `connectedEdges` reads

Current expand logic depends on:
- `node.hasClass('story-secondary'/'story-primary')` for eligibility,
- `other.hasClass('story-muted')` for promoted node collection,
- `node.connectedEdges()` for traversal universe.

These are high-coupling because they bind Story policy to:
- Graph’s current class naming semantics,
- Cytoscape object shape/lifecycle,
- timing of prior focus render passes.

Explicit payload snapshots decouple policy from renderer internals and make expand deterministic/testable without live `cy` objects.

## 5) Parity invariants to preserve

Any future seam spike must preserve all of these:
1. **Selection order invariant:** `UI.renderPanel` still runs before expand decision path.
2. **Runtime mutation ordering:** expansion sets mutate before focus re-application.
3. **Panel refresh ordering:** `updateStoryPanel` runs after successful expansion-driven focus recompute.
4. **No-op behavior:** if no eligible edge is added, no focus rerender/panel update side effect.
5. **Step/reset parity:** `applyStoryStep` continues to reset expansion sets.
6. **Reveal parity:** `toggleStoryReveal` still reuses current runtime sets and does not clear expansions.
7. **Focus mediation parity:** downstream focus execution still flows through existing `story:focus-requested` path.

## 6) Risk grading for first extraction moves

### Low-risk
- Add planning docs/checklists and payload schema docs.
- Add non-runtime audit instrumentation notes.
- Define seam event name and payload contract in docs.

### Medium-risk (acceptable first spike)
- Introduce event emission site in `handleNodeSelect` **without** removing existing direct call, guarded by feature flag or shadow mode.
- Build adapter that derives payload from current node/cy and invokes existing `maybeExpandFromNode` unchanged for comparison logging.

### Too entangled for first move
- Rewriting `maybeExpandFromNode` algorithm.
- Renaming/remapping story class semantics (`story-primary`, etc.).
- Changing scrolly observer focus wiring.
- Altering `applyStoryStep` or reveal lifecycle contracts.

## 7) What must not be touched first

Do **not** start by changing:
- `Graph.executeStoryFocusRequest` class/camera implementation,
- `applyStoryFocus` request construction and event fallback behavior,
- canonical graph data or relation normalization behavior,
- `handleNodeSelect` ordering around `UI.renderPanel`.

These are shared stability anchors for story, panel, and scrolly paths.

## 8) Safest sequencing for a future expand seam spike

1. **Contract freeze (docs/tests):** lock payload schema and parity checklist.
2. **Shadow event emit:** emit `story:expand-from-node-requested` from node-select path in parallel (no behavior switch).
3. **Adapter validation:** consume payload in a no-op/shadow handler and compare computed adds vs current direct path.
4. **Single-path switch:** route expand policy through seam handler while preserving existing `applyStoryFocus` + `updateStoryPanel` ordering.
5. **Cleanup pass:** only after parity proof, remove direct Cytoscape/class reads from Story expand policy.

This sequencing keeps behavioral risk bounded while incrementally reducing direct Graph coupling.
