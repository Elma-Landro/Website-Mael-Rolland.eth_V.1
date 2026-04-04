# workspace/decisions/ — Decision Traces

This directory holds machine-readable records of significant architectural and editorial decisions.

## Why DecisionTrace exists

The audit documents in `docs/` capture analytical audit findings in Markdown.
DecisionTrace objects complement them with **structured, machine-readable records** of decisions
about graph construction, schema evolution, UI changes, and publication choices.

This enables future tooling to:
- Answer "why was this entity added?"
- Answer "why were these two nodes merged?"
- Answer "why was this relation type requalified?"
- Reconstruct the reasoning history of the knowledge graph

## File naming convention

```
YYYY-MM-DD_short-title.json
```

Example: `2026-04-04_research-infrastructure-restructure.json`

## Decision types

| `decisionType` | Meaning |
|---|---|
| `entity_added` | A new entity was added to the graph |
| `entity_merged` | Two entities were merged into one |
| `entity_removed` | An entity was removed or deprecated |
| `relation_requalified` | A relation type was changed |
| `type_created` | A new entity type was added to the schema |
| `patch_applied` | A patch file was applied to the canonical graph |
| `ui_change` | A significant change to the visualization or reader UI |
| `schema_change` | A change to the workspace schema definitions |
| `narrative_change` | A change to a NarrativePreset or its steps |
| `architecture_decision` | A structural decision about the repository or pipeline |

## Decision status

| `status` | Meaning |
|---|---|
| `proposed` | Decision is documented but not yet enacted |
| `applied` | Decision has been implemented |
| `reverted` | Decision was reversed with documented rationale |

## Schema

See `../schemas/decision-trace.schema.json` for the full JSON Schema definition.
