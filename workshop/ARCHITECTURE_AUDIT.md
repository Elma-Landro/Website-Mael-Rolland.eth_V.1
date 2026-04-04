# Architecture Audit (Follow-up)

## Correction log (2026-04-04)

### Corrected factual point
- `scripts/apply-sourcequote-phases.mjs` **exists** in the repository root.
- Previous wording that implied the script was missing was incorrect.

### Actual issue to track
- The current challenge is not file absence, but **boundary/visibility confusion** between:
  - `scripts/` at repository root (existing graph generation, patching, migration utilities), and
  - `workshop/scripts/` (new workshop-layer lint/validation/export helpers).

## Boundary note
- In this phase, both layers coexist intentionally.
- No runtime path has been switched from root `scripts/` to `workshop/scripts/`.
- Public runtime behavior remains unchanged.
