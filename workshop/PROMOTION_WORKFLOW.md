# Workshop Promotion Workflow (Phase: documentary + dry-run only)

This workflow defines how workshop artifacts are interpreted and reviewed **without** mutating canonical graph data.

## Scope and non-goals

- Scope: document review and promotion conditions for workshop objects (Claim, ValidationEvent, NarrativePreset, etc.).
- Non-goals in this phase:
  - no automated promotion pipeline,
  - no canonical graph mutation,
  - no runtime/public behavior changes.

## Legacy canonical interpretation

In this phase, legacy canonical content (for example `grc20-these-mael-rolland-v96.json`) is treated as:

- authoritative baseline for currently published graph structure,
- immutable reference input for workshop interpretation,
- eligible to be referenced by workshop objects using explicit IDs/provenance notes.

No workshop script in this phase writes back into canonical graph files.

## Status meanings

The workshop status vocabulary is interpreted conservatively:

- `raw`: source material captured, not normalized.
- `extracted`: structured extraction performed, but links/review incomplete.
- `linked`: object linked to graph/evidence IDs, still pending review.
- `needs_review`: candidate object drafted, requires explicit validation.
- `validated`: reviewed and accepted for potential publication consideration.
- `published`: reserved target state for a later explicit publication step (not executed here).

## Promotion preconditions (for future phases)

Before any workshop object could be promoted in a future implementation, all should be true:

1. Object is schema-valid and parse-valid.
2. Provenance is explicit (author/date/method and referenced IDs where applicable).
3. Linked IDs resolve against known workshop/canonical context.
4. Object has passed validation and carries `validated` status (or family-specific equivalent gating).
5. Export-policy family visibility and status gates allow public eligibility.
6. Human review approves promotion intent.

## Operational rule for this phase

Promotion is **not automated** in this phase.

- Dry-run reports may classify artifacts as workshop-only, public-eligible in principle, or not export-ready.
- Classification is advisory only.
- No patching, no canonical mutation, and no deployment/public export action occurs from this workflow.
