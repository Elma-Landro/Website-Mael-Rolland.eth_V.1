# Workshop Layer (authoring/validation, non-public by default)

This folder is the vNext scaffold for research-workshop operations.

- `raw/`: immutable source ingests.
- `normalized/`: cleaned/segmented source material.
- `working-graph/`: tentative graph objects and candidate links.
- `evidence/`: first-class evidence artifacts (SourceQuote, etc.).
- `claims/`: explicit analytical propositions.
- `decision-traces/`: editorial/modeling decisions with rationale.
- `validations/`: validation events and review logs.
- `narratives/`: workshop narrative presets and steps.
- `db/`: optional local indexes (SQLite or equivalent).
- `logs/`: processing traces.
- `templates/`: JSON templates for new object families.

Public static pages should **not** directly depend on this folder.

## Current minimal evidence linkage (phase note)

- SourceQuote ↔ Claim linkage is currently represented by object-level ID references (for example `claim.linkedEvidenceIds` and optional `sourceQuote.linkedClaimIds`).
- This is a workshop-layer convention for traceability in dry-run mode; it does not mutate canonical graph relations.

