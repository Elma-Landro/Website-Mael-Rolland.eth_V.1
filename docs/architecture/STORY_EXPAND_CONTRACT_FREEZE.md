# STORY_EXPAND_CONTRACT_FREEZE

## Status
- **Type:** contract freeze (planning only)
- **Runtime impact:** none
- **Purpose:** lock seam contract before any expand runtime spike

## 1) Frozen candidate event names

### 1.1 Required
- `story:expand-from-node-requested`

### 1.2 Optional (shadow diagnostics only)
- `story:expand-from-node-resolved`

### 1.3 Existing downstream event (unchanged)
- `story:focus-requested`

> Freeze rule: no additional expand event names are introduced during the first shadow-mode spike.

---

## 2) Frozen payload schema — `story:expand-from-node-requested`

```ts
type StoryExpandNodeRole =
  | 'primary'
  | 'secondary'
  | 'bridge'
  | 'muted'
  | 'hidden'
  | 'unknown';

type StoryExpandEdgeDescriptor = {
  edgeId: string;
  sourceId: string;
  targetId: string;
  otherNodeId: string; // relative to selected nodeId
  relationTypeCanonical: string;
  otherNodeRole: StoryExpandNodeRole;
};

type StoryExpandFromNodeRequested = {
  eventVersion: 1;
  storyId: string | null;
  stepIndex: number;
  nodeId: string;
  nodeRole: StoryExpandNodeRole;
  selectionContext?: {
    from: 'tap' | 'click';
  };
  expandOptionsSnapshot: {
    expandOnClick: boolean;
    expandFromPrimary: boolean;
    maxAutoEdges: number;
    allowedRelationTypes: string[]; // canonicalized
  };
  runtimeSnapshot: {
    phase: string;
    expandedSecondaryIds: string[];
    expandedEdgeIds: string[];
  };
  candidateEdges: StoryExpandEdgeDescriptor[];
};
```

### 2.1 Freeze notes
- `eventVersion` is required and frozen to `1` for first spike.
- `candidateEdges` is the only permitted edge universe for expand policy in shadow mode.
- `allowedRelationTypes` must be canonicalized before emission.

---

## 3) Required field meanings (normative)

- `storyId`: active story identifier at selection time; `null` if none.
- `stepIndex`: active step index at selection time.
- `nodeId`: selected entity/node id.
- `nodeRole`: explicit role snapshot replacing class-based eligibility checks.
- `expandOptionsSnapshot`: immutable decision inputs for expand policy.
- `runtimeSnapshot`: pre-expansion runtime state snapshot before any add/mutate.
- `candidateEdges`: pre-filterable edge descriptors derived from current graph state and tied to `nodeId`.

> Freeze rule: handlers must treat payload as immutable input and must not depend on external Cytoscape objects.

---

## 4) Current Graph-applied class reads that must be replaceable from payload

The following current class reads are explicitly targeted for replacement:
- `node.hasClass('story-secondary')`
- `node.hasClass('story-primary')` (with `expandFromPrimary` gate)
- `other.hasClass('story-muted')`

Replacement mapping during seam spike:
- node eligibility -> `nodeRole`
- opposite endpoint promotion decision -> `otherNodeRole`

---

## 5) Minimum edge descriptor shape (frozen)

Each `candidateEdges[]` element must include:
- `edgeId`
- `sourceId`
- `targetId`
- `otherNodeId`
- `relationTypeCanonical`
- `otherNodeRole`

No field in this minimum shape may be removed in first spike.

---

## 6) Required ordering invariants (must hold)

1. `UI.renderPanel` still executes before expand seam request handling.
2. Expand runtime sets are mutated before re-applying focus.
3. `updateStoryPanel` executes after expansion-triggered focus recomputation.
4. If no expansion delta is admitted, focus and panel update side effects do not run.

---

## 7) Required parity invariants (must hold)

1. `applyStoryStep` continues resetting step runtime expansion sets.
2. `toggleStoryReveal` preserves expansion sets; reveal toggle does not clear them.
3. Downstream visual execution remains through existing focus path (`story:focus-requested`).
4. Relation filtering parity remains based on canonical relation type matching.
5. Max expansion cap parity remains tied to `maxAutoEdges`.
6. Step/story identity used for expand decisions must match current active story/step at selection time.

---

## 8) Intentionally out of scope for this freeze

- Any runtime implementation changes.
- Any refactor of `maybeExpandFromNode` algorithm.
- Any change to scrolly observer wiring.
- Any edits to `applyStoryFocus` execution semantics.
- Any class taxonomy rewrite (`story-primary`, `story-secondary`, etc.).
- Any canonical graph data, package, or deployment changes.

---

## 9) What must NOT change in future shadow-mode spike

- `handleNodeSelect` ordering around panel render.
- Existing direct expand path behavior (must remain authoritative until parity proven).
- `applyStoryStep` lifecycle/reset behavior.
- `toggleStoryReveal` lifecycle behavior.
- `story:focus-requested` fallback behavior.

Shadow mode may observe and compare; it must not alter user-visible expand behavior.

---

## 10) Acceptance rule to move from planning -> runtime spike

Runtime shadow-mode spike is allowed only when all are true:
1. This contract document is approved without open schema/invariant questions.
2. Payload producer can emit all required fields deterministically.
3. A parity checklist exists mapping each invariant above to an observable check.
4. Spike plan explicitly states that direct path remains source-of-truth during shadow comparisons.

If any criterion is unmet, runtime expand seam work must remain blocked.
