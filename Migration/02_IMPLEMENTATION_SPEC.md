# Implementation spec — story mode hierarchy / depth

## Goal

Refactor the current story focus so that each step can control:

- how many nodes are visible
- which edges remain visible
- whether structural backlinks remain visible
- whether one-hop context is shown
- how strongly non-target elements are suppressed

## A. New per-step options

Each `StoryStep` should accept the following optional fields:

```ts
edgeMode?: 'strict' | 'neighbors' | 'context'
includeNeighbors?: boolean
secondaryDepth?: 0 | 1 | 2
maxSecondaryPerTarget?: number
hideRelationTypes?: string[]
showRelationTypes?: string[]
hideBackbone?: boolean
backboneRelationTypes?: string[]
fitTargets?: 'primary' | 'primary+secondary'
```

### Recommended semantics

- `strict`
  - only primary nodes are visible as active
  - only edges where both endpoints are primary remain clearly visible
  - all other edges should be hidden or nearly hidden

- `neighbors`
  - show one-hop secondary nodes around the primaries
  - primary-primary edges = strong
  - primary-secondary edges = medium
  - other edges = hidden

- `context`
  - show primary and secondary nodes
  - preserve a tiny amount of global structure in the background
  - useful only for broad orientation steps

## B. New visual classes

### Nodes

- `story-primary`
- `story-secondary`
- `story-muted`
- `story-hidden`

### Edges

- `story-primary`
- `story-secondary`
- `story-backbone`
- `story-hidden`

## C. Suggested default rendering

### Nodes

- `story-primary`
  - opacity: 1
  - border-width: 3
  - border-color: accent
  - high z-index

- `story-secondary`
  - opacity: 0.42–0.60
  - border-width: 1.5
  - slightly warmer border

- `story-muted`
  - opacity: 0.06–0.12

- `story-hidden`
  - display: none OR opacity below 0.02

### Edges

- `story-primary`
  - opacity: 0.65–0.85
  - width: 1.0–1.4

- `story-secondary`
  - opacity: 0.12–0.22
  - width: 0.45–0.75

- `story-backbone`
  - opacity: 0.02–0.05
  - width: 0.2–0.35

- `story-hidden`
  - display: none

## D. Backbone relations

By default, story mode should suppress or heavily downrank structural relations that tend to clutter almost every step.

Recommended default backbone / low-priority relation types:

```js
[
  'partOf',
  'source',
  'citedIn',
  'relatedTo'
]
```

These should NOT necessarily disappear globally, but in story mode they should be either:

- hidden when `edgeMode = 'strict'`
- barely visible when `hideBackbone = false`
- fully hidden when `hideBackbone = true`

## E. Matching relation type robustly

Edge type names may live in different data keys. Implement a helper like:

```js
function getEdgeType(edge) {
  return (
    edge.data('relation_type') ||
    edge.data('relationType') ||
    edge.data('type') ||
    edge.data('label') ||
    edge.data('name') ||
    ''
  ).toString();
}
```

## F. Focus algorithm

### Step 1 — resolve primary nodes

Use the existing node resolution logic.

### Step 2 — build secondary set only if needed

If `includeNeighbors` or `edgeMode !== 'strict'`, collect one-hop neighbors from primary nodes.

Apply:

- relation allow/deny filters
- `maxSecondaryPerTarget`
- optional exclusion of known hub/backbone relations

### Step 3 — classify edges

For each edge:

1. compute edge type
2. detect if source/target are primary or secondary
3. decide class:
   - primary-primary => `story-primary`
   - primary-secondary => `story-secondary`
   - backbone relation => `story-backbone` or `story-hidden`
   - everything else => `story-hidden`

### Step 4 — classify nodes

- primary => `story-primary`
- secondary => `story-secondary`
- all others => `story-muted` or `story-hidden`

### Step 5 — camera fit

- `fitTargets = 'primary'` for most precise steps
- `fitTargets = 'primary+secondary'` for contextual steps

## G. Default policy by story type

### Structure de la thèse

Use:

- `edgeMode: 'strict'`
- `includeNeighbors: false`
- `hideBackbone: true`

This is the view where repeated chapter ↔ thesis backlinks are most visually annoying.

### Monétisation

Use mostly:

- `edgeMode: 'strict'` for analytic steps
- `edgeMode: 'neighbors'` only when showing infrastructures or gateways

### Qui gouverne réellement ?

Use:

- `edgeMode: 'neighbors'`
- `secondaryDepth: 1`
- `hideBackbone: false`

Because the point is to show arenas and distributed governance, but still with hierarchy.

### Crises

Use mixed modes:

- `strict` for exact event steps
n- `neighbors` for actor/arena steps

## H. Backward compatibility

If no extra story-step options are defined:

- `edgeMode = 'strict'`
- `includeNeighbors = false`
- `secondaryDepth = 0`
- `hideBackbone = true`
- `fitTargets = 'primary'`

This makes the default narrative cleaner than the current implementation.

## I. Acceptance tests

A step is successful if:

- the primary nodes are visually obvious
- at least 70–90% of irrelevant edges disappear visually
- repeated structural backlinks no longer dominate the stage
- moving to the next step feels like a genuine reframing, not merely a zoom change
