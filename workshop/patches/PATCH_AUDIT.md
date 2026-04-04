# Patch & Migration Audit (documentary, non-applying)

Generated: 2026-04-04T13:41:28.138Z

## Scope
- Root patch JSON artifacts (`patch*.json`, `new_relations_patch.json`, `grc20_v91_migration_report.json`)
- `workshop/patches/` JSON artifacts
- `Migration/` bundle and helper artifacts
- Root and sourcequote migration scripts under `scripts/` + `apply_v91_migration.py`

## Totals
- Artifacts: 34
- patch_json: 16
- migration_script: 11
- zip_bundle: 4
- helper_script: 2
- unknown: 1

## Key grounded findings
- `scripts/apply-sourcequote-phases.mjs` exists and references phase ZIP bundles in `Migration/`.
- Several patch files explicitly reference old graph baselines (e.g., v72/v73/v82-v83), so current applicability is uncertain without replay audit.
- `patches/grc20_anchor_overrides_targeted.json` explicitly describes itself as a documentary/controlled future injection candidate.
- No patch is declared "applied" here unless evidence is explicit (migration report artifact only is tagged candidate_applied).

## Status policy used in this pass
- `unknown`: default when no strong evidence of apply-state exists.
- `candidate_pending`: explicit placeholders/planned injection notes present.
- `superseded_possible`: artifact targets older version baseline.
- `candidate_applied`: migration report artifact suggests a run occurred, but full replay was not performed.

For machine-readable details, see `patch-inventory.json`.