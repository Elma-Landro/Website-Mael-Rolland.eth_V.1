# workspace/narratives/ — Narrative Presets

This directory manages NarrativePreset and NarrativeStep objects for scrollytelling and guided graph views.

## Current state

`narrative-anchors.json` at the repository root is the **current published narrative system**.
It contains 115 NarrativeAnchor objects derived from the canonical graph by `narrative-anchors-build.mjs`.

NarrativePreset objects here are a higher-level layer: they define **curated guided sequences**
that orchestrate multiple anchors into a coherent narrative for a specific audience or purpose.

## Relationship to existing systems

```
workspace/narratives/presets/*.json  (NarrativePreset — curated sequences)
        ↓
narrative-anchors.json               (NarrativeAnchor — per-quote scenes, derived from graph)
        ↓
grc20-these-mael-rolland-v96.json    (canonical graph — SourceQuote → ThesisSection → Entity)
```

A NarrativePreset references NarrativeAnchor IDs from `narrative-anchors.json` (by anchor `id` field)
and adds: audience framing, sequence order, camera/view instructions, body text.

## Directory layout

- `presets/` — One JSON file per NarrativePreset

## Preset status lifecycle

```
draft → validated → published
```

Published presets are included in the public export snapshot via `build-export.mjs`.

## View modes available

| `viewMode` | Description |
|---|---|
| `matrice` | Matrix/grid layout with column halos (default) |
| `nebulae` | Chapter archipelago layout |
| `cose` | Force-directed physics layout |
| `arbre` | Hierarchical tree layout |

## Camera presets available

| `cameraPreset` | Description |
|---|---|
| `tight` | Close zoom on focused nodes |
| `wide` | Full graph visible |
| `archipelago` | Chapter islands in view |

## Schema

See `../schemas/narrative-preset.schema.json` and `../schemas/narrative-step.schema.json`.
