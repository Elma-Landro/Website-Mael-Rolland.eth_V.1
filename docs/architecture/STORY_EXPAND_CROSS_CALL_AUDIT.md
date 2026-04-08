# STORY_EXPAND_CROSS_CALL_AUDIT

## Scope
This audit maps the **current** expand-from-node behavior exactly as implemented on this branch, without proposing runtime edits.

## 1) Concrete call chain: `handleNodeSelect -> maybeExpandFromNode`

### Node selection entrypoint (Graph IIFE)
- `handleNodeSelect(e)` writes `State.selectedId`, then calls `UI.renderPanel(id)`, then `highlightNeighbors(id)`, and only then delegates to Story via `StoryMode.maybeExpandFromNode(id, e.target)`. This order is explicit and stable in the current implementation.
- Event bindings are `cy.on('tap', 'node', handleNodeSelect)` and `cy.on('click', 'node', handleNodeSelect)`.

### Immediate ordering invariant
1. `UI.renderPanel(id)` must run first (selection/panel coherence).
2. Story expansion hook is invoked after panel render and graph neighbor highlight.

This means expand-from-node currently executes as a **post-selection side effect**, not as the primary selector action.

## 2) Concrete chain inside `maybeExpandFromNode`

`maybeExpandFromNode(nodeId, node)` is guarded and short-circuits unless all of the following are true:
- active story + valid step runtime exist,
- step opts resolve to `expandOnClick === true`,
- clicked node has Graph-applied class eligibility:
  - `story-secondary`, or
  - `story-primary` when `expandFromPrimary` is enabled,
- `Graph.cy` is available.

When guards pass:
1. Iterates `node.connectedEdges()`.
2. Applies relation-type filtering (`allowedRelationTypes` canonicalized).
3. For each admitted edge (up to `maxAutoEdges`):
   - if opposite endpoint currently has `story-muted`, add node id to `storyState.currentStepRuntime.expandedSecondaryIds`,
   - always add edge id to `storyState.currentStepRuntime.expandedEdgeIds`.
4. If at least one edge was added:
   - calls `applyStoryFocus(...)` to recompute class map/camera using updated runtime sets,
   - calls `updateStoryPanel()` afterward.

### Ordering invariant inside expand path
- Expansion runtime mutations happen **before** `applyStoryFocus`.
- `updateStoryPanel()` happens **after** expansion mutations and focus re-application.

## 3) `maybeExpandFromNode -> Graph` coupling points

Even though `maybeExpandFromNode` itself performs limited Graph API calls, it is tightly coupled to Graph/Cytoscape shape:
- Direct Graph access: `const cy = Graph.cy`.
- Direct Cytoscape traversal from node handle: `node.connectedEdges()` and edge endpoint resolution (`edge.source()/target()`).
- Re-entry into focus pipeline via `applyStoryFocus(...)`, which emits `story:focus-requested` and falls back to `Graph.executeStoryFocusRequest(request)` when no handler claims the event.

So expand behavior is currently **hybrid**:
- direct Cytoscape reads and runtime writes in StoryMode,
- mediated focus execution via event bus (`story:focus-requested`) with Graph fallback.

## 4) Story state mutations performed by expand

`maybeExpandFromNode` mutates only step runtime collections:
- `storyState.currentStepRuntime.expandedSecondaryIds` (`Set`),
- `storyState.currentStepRuntime.expandedEdgeIds` (`Set`).

It does **not** alter:
- `activeStoryId`,
- `activeStoryStepIndex`,
- reveal phase directly (`phase` is unchanged here).

## 5) Direct DOM dependencies in the expand call chain

`maybeExpandFromNode` itself has no direct DOM query.
DOM coupling in the chain appears via surrounding calls:
- Pre-expand: `UI.renderPanel(id)` in `handleNodeSelect`.
- Post-expand: `updateStoryPanel()` mutates `#story-meta`, `#story-step-title`, `#story-step-body`, `#btn-story-reveal`, citation block elements, and bridge hint content/style.

Therefore, expand is not DOM-free at system level: it is bracketed by panel DOM writes before and after expansion.

## 6) Interaction with adjacent Story entry points

### `applyStoryStep`
- Re-initializes `storyState.currentStepRuntime` sets/phases and invokes `applyStoryFocus(...)`.
- This resets prior expand accumulations when step changes.

### `toggleStoryReveal`
- Flips `phase` between `nodesOnly` and `primaryEdges`, then calls `applyStoryFocus(...)` and `updateStoryPanel()`.
- Expand runtime sets persist across reveal toggles unless step is reset.

### `applyStoryFocus` / `story:focus-requested`
- Expand relies on focus recomputation to materialize added ids visually.
- `applyStoryFocus` emits `story:focus-requested`; Graph has a bound listener executing class assignment/camera (`executeStoryFocusRequest`).
- If no event handler claims the event, explicit fallback is `Graph.executeStoryFocusRequest(request)`.

### Scrolly `story:focus-requested` interaction surface
- Scrolly observer can independently trigger `StoryMode.applyStoryFocus(...)` for narrative anchor scenes.
- This can overwrite class state that expand previously produced, because expand parity depends on the same focus class contract.

## 7) Hidden dependency: Graph-applied Cytoscape classes

Expand eligibility and mutation semantics depend on classes produced by Graph focus execution:
- expand gate reads `node.hasClass('story-secondary')` / `'story-primary'`,
- expansion promotion checks opposite node `other.hasClass('story-muted')`.

Those classes are set inside Graph focus execution (`executeStoryFocusRequest`) from Story-provided sets. This creates a latent circular dependency:
- Story expand reads classes,
- Graph focus writes classes,
- Story expand writes ids that alter next Graph class write.

## 8) Current mediated vs direct paths (as-is)

### Direct paths
- Graph node events directly invoke Story callback (`StoryMode.maybeExpandFromNode`).
- Story expand directly inspects Cytoscape node/edge graph objects and Graph-applied classes.

### Mediated paths
- Focus application is mediated by `story:focus-requested` event and Graph listener/fallback executor.

### Net state
Expand-from-node is currently a **mixed seam**: direct on selection/traversal, mediated on focus rendering.
