# workspace/schemas/ — JSON Schema Definitions

This directory contains JSON Schema definitions for workspace-layer object types.
These schemas define the canonical field set for objects that live in `workspace/`
and may eventually be promoted to the canonical GRC-20 graph.

## Schema files

| File | Object type | Graph entity equivalent | Status |
|---|---|---|---|
| `status-model.json` | Status/lifecycle model | n/a (cross-cutting) | Authoritative |
| `source-quote.schema.json` | SourceQuote | `SourceQuote` type (245 instances in v96) | Formalizes existing v96 attributes |
| `claim.schema.json` | Claim | `AnalyticClaim` type (0 instances in v96) | Workspace-layer first |
| `decision-trace.schema.json` | DecisionTrace | None (workspace metadata only) | Workspace-layer only |
| `narrative-preset.schema.json` | NarrativePreset | None (workspace metadata only) | Workspace-layer first |
| `narrative-step.schema.json` | NarrativeStep | None (workspace metadata only) | Workspace-layer first |
| `validation-event.schema.json` | ValidationEvent | None (workspace metadata only) | Workspace-layer first |

## Key design decisions

**SourceQuote schema** does not define a new format. It formalizes what already exists in
`grc20-these-mael-rolland-v96.json` — the 245 existing SourceQuote entities already carry
`quoteText`, `page`, `chapter`, `thesisLocation`, `language`, `sourceFormat`, and (for 40%
of entities) `evidenceStatus`. The schema is fully backward-compatible: new optional fields
(`sectionKey`, `exactnessStatus`, `status`) are additive.

**Claim vs AnalyticClaim**: The `AnalyticClaim` entity type is already defined in the v96
graph schema (added in v91 migration) but has zero instantiated entities. New Claim objects
live in `workspace/` first. When validated, they are promoted to the graph as `AnalyticClaim`
entities via a versioned patch.

**DecisionTrace, NarrativePreset, NarrativeStep, ValidationEvent** are workspace-internal
objects. They are NOT wired to canonical graph `relation_types`. This is intentional —
Phase 1 keeps the canonical graph untouched.

## Read status-model.json first

`status-model.json` is the entry point. It defines the `legacy_canonical → validated → published`
lifecycle and the mapping from existing v96 `evidenceStatus` values to the new status vocabulary.
All other schemas reference it via the `status` field.
