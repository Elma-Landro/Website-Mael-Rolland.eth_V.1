# Story Expand-from-Node Contract Freeze

**Branch:** `codex/create-child-branch-for-story-boundary-planning-g24stw`
**Date:** 2026-04-08
**Status:** Frozen — authorizes shadow-mode spike only

---

## 1) What this freeze authorizes

A future branch may implement a **shadow-mode spike only**:

- Graph emits `story:expand-from-node-requested` alongside the existing direct call to
  `StoryMode.maybeExpandFromNode(id, e.target)`.
- Story registers a **read-only** shadow listener to verify output parity.
- The direct call must **not** be removed until parity is confirmed.

This contract does **not** authorize:
- Removing the direct `StoryMode.maybeExpandFromNode` call
- Any behavior change in `maybeExpandFromNode`
- Any change to `applyStoryFocus`, `updateStoryPanel`, or `executeStoryFocusRequest`
- Combining shadow-mode spike and promotion into a single branch

---

## 2) Frozen event name

```
story:expand-from-node-requested
```

Consistent with existing vocabulary: `layout:apply-requested`, `story:focus-requested`.

---

## 3) Frozen payload shape

```js
{
  nodeId:         string,     // id = e.target.data('id') from handleNodeSelect

  nodeClasses:    string[],   // snapshot of e.target.classes() at tap time
                              // replaces: node.hasClass('story-secondary')
                              //           node.hasClass('story-primary')

  connectedEdges: [           // snapshot of node.connectedEdges() at tap time
    {
      id:            string,   // edge.id()
      sourceId:      string,   // edge.source().id()
      targetId:      string,   // edge.target().id()
      relationType:  string,   // canonicalizeRelationName(getEdgeType(edge))
      sourceClasses: string[], // snapshot of edge.source().classes() at tap time
      targetClasses: string[]  // snapshot of edge.target().classes() at tap time
                               // both replace: other.hasClass('story-muted')
    }
  ]
}
```

All class snapshots are taken at tap time by Graph, before any Story listener runs.

---

## 4) Frozen dual-set mutation rule

This is the most critical invariant. The Story shadow listener (and any future active
listener) **must** replicate the current `maybeExpandFromNode` logic exactly:

```
let added = 0
for each edge in connectedEdges:
  if added >= opts.maxAutoEdges: break            ← cap on QUALIFYING edges, not total visited

  if opts.allowedRelationTypes.length > 0
     AND edge.relationType NOT IN opts.allowedRelationTypes:
    continue                                      ← skip; does NOT increment added

  const isSource     = (edge.sourceId === nodeId)
  const otherId      = isSource ? edge.targetId      : edge.sourceId
  const otherClasses = isSource ? edge.targetClasses : edge.sourceClasses

  expandedEdgeIds.add(edge.id)                    ← ALWAYS (if qualifies)

  if otherClasses.includes('story-muted'):        ← ONLY IF muted
    expandedSecondaryIds.add(otherId)

  added += 1                                      ← increment only for qualifying edges
```

**Cap semantics note:** Type-filtered edges (`continue`) do not count toward
`opts.maxAutoEdges`. The cap limits qualifying edges added, not edges visited. A
mis-implementation that increments the counter before the type filter check will
add fewer edges than the current behavior when mixed-type connected edges are present.

**Key asymmetry:**
- `expandedEdgeIds` receives every qualifying edge regardless of the neighbor's class.
- `expandedSecondaryIds` receives only neighbors that had `story-muted` at tap time.
- These are not the same set. A mis-implementation that adds all neighbors to
  `expandedSecondaryIds` will produce visual regressions.

---

## 5) Frozen ordering invariant

Inside `handleNodeSelect`, the emit must occur at the **same position** as the current
direct call — after `UI.renderPanel(id)` and `highlightNeighbors(id)`:

```js
State.selectedId = id;
UI.renderPanel(id);           // must complete first
highlightNeighbors(id);       // must complete first
GrapheEventBus.emit(          // emit at this position
  'story:expand-from-node-requested',
  payload
);
StoryMode.maybeExpandFromNode(id, e.target);  // direct call stays in shadow mode
```

Note: `highlightNeighbors` adds `highlighted`/`faded` classes which are not used in
expansion eligibility checks (`story-secondary`, `story-primary`, `story-muted` only).
Class snapshot timing relative to `highlightNeighbors` does not affect parity, but must
be verified during the spike as a precaution.

---

## 6) Shadow-mode spike acceptance gate

The spike is complete when ALL of the following hold across at least two story presets
that include steps with `expandOnClick: true`:

- [ ] `expandedSecondaryIds` from shadow listener matches `expandedSecondaryIds` from direct call (same node ids, same count)
- [ ] `expandedEdgeIds` from shadow listener matches `expandedEdgeIds` from direct call (same edge ids, same count)
- [ ] No expansion occurs when `expandOnClick` is false (guard preserved)
- [ ] No expansion occurs when tapped node lacks both `story-secondary` and `story-primary` classes
- [ ] Shadow listener is read-only — `storyState` is NOT mutated by listener
- [ ] `updateStoryPanel()` called exactly once (no double-render triggered by shadow listener)
- [ ] Reveal toggle after expansion: expansion state unchanged by `toggleStoryReveal`
- [ ] Step navigation after expansion: expansion state cleared by `applyStoryStep`
- [ ] No console errors during shadow-mode operation
- [ ] No visual regression in focus classes or camera behavior

**The shadow listener must not call `applyStoryFocus`, `updateStoryPanel`, or modify
`storyState` in any way.** It must only compare and log.

---

## 7) What must not change in the shadow spike

| Item | Constraint |
|------|-----------|
| `maybeExpandFromNode` body | Unchanged |
| `applyStoryFocus` | Unchanged |
| `updateStoryPanel` | Unchanged |
| `handleNodeSelect` guard logic | Unchanged (only payload construction + emit added) |
| `executeStoryFocusRequest` | Unchanged |
| `GrapheEventBus` API | No new methods needed (`on` + `emit` are sufficient) |
| `toggleStoryReveal` | Unchanged |

---

## 8) Future path after parity confirmed

Only after the acceptance gate passes on the shadow-mode spike branch:

1. Story listener is promoted from shadow (read-only) to active (replaces direct call)
2. Direct `StoryMode.maybeExpandFromNode` call in `handleNodeSelect` is removed **or**
   kept as fallback using the same pattern as prior seams:
   ```js
   const handled = GrapheEventBus.emit('story:expand-from-node-requested', payload);
   if (!handled) StoryMode.maybeExpandFromNode(id, e.target);
   ```
3. Fallback kept until at least one complete story session confirms event listener fires

This promotion step is a separate branch from the shadow-mode spike.

---

## 9) Parity invariants summary

| Invariant | Testable signal |
|-----------|----------------|
| Correct expandedEdgeIds | Log both sets; diff must be empty |
| Correct expandedSecondaryIds | Log both sets; diff must be empty |
| Dual-set asymmetry | Count: `expandedSecondaryIds.size <= expandedEdgeIds.size` always |
| Guard: expandOnClick false | No expansion initiated |
| Guard: ineligible node class | No expansion initiated |
| Reveal toggle preserves expansion | Sets unchanged after toggleStoryReveal |
| Step navigation clears expansion | Sets empty after applyStoryStep |
| Single panel update | updateStoryPanel call count = 1 per tap |
