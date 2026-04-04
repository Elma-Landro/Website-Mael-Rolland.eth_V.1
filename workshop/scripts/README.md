# workshop/scripts

This directory is reserved for **workshop-layer utilities**.

## Script boundary (important)
- `scripts/` (repo root): existing project utilities for graph generation, patching, and sourcequote migration workflows.
- `workshop/scripts/`: future workshop-only helpers (linting, validation checks, export prep for workshop artifacts).

## Why both directories exist
- Root `scripts/` already supports canonical graph maintenance and should remain stable.
- `workshop/scripts/` allows iterative research-infrastructure tooling without coupling it to public runtime workflows.

## Phase guarantee
- This phase does **not** change runtime script paths.
- No public page or deployment path is redirected to `workshop/scripts/` yet.

## Current workshop scripts
- `lint-workshop-artifacts.mjs`: lightweight JSON + structural lint for workshop artifacts.
- `audit-patches.mjs`: documentary inventory of existing root patch/migration artifacts.
- `build-export-dry-run.mjs`: non-destructive dry-run report driven by `workshop/exports/export-policy.json`.
