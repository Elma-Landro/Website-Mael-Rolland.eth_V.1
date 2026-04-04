# workspace/scripts/ — Build, Export, and Lint Pipeline

This directory will hold build, export, and lint scripts for the workspace/publication pipeline.

## Important: two scripts/ locations

This repository has **two** script directories with different purposes:

| Location | Purpose | Status |
|---|---|---|
| `scripts/` (repository root) | Graph generation and patch creation. Reads thesis Markdown and patch sources to generate GRC-20 patch JSON files. Includes `apply-sourcequote-phases.mjs`, `generate_corrective_patch.mjs`, batch generators, and SourceQuote migration utilities. | Pre-existing, functional |
| `workspace/scripts/` (this directory) | Build, export, and lint pipeline for the two-layer architecture. Reads the canonical graph, validates pending patches, and produces public export snapshots. | Phase 2 — to be created |

**Root `scripts/` is for graph authoring.** It produces patch files (input to the canonical graph).
**`workspace/scripts/` is for the export pipeline.** It consumes the canonical graph and produces public output.

Do not place graph-generation scripts here. Do not place export/lint scripts in root `scripts/`.

## Planned scripts (Phase 2)

| Script | Purpose | Mode |
|---|---|---|
| `lint-graph.mjs` | Validate canonical graph for orphans, missing evidence, duplicate names, broken section links | `--dry-run` only |
| `build-export.mjs` | Load canonical graph + validated pending patches, write `public/exports/graph-snapshot.json` and `export-manifest.json` | `--dry-run` and real write |
| `validate-evidence.mjs` | Report SourceQuote coverage gaps (entities without supporting quotes) | Report only |

All scripts will default to `--dry-run` mode. Real writes require an explicit flag.
None of these scripts will modify `grc20-these-mael-rolland-v96.json` or any file under `assets/`, HTML, or CSS.

## Relationship to existing scripts

`scripts/apply-sourcequote-phases.mjs` applies SourceQuote phase patches to the graph.
This belongs in root `scripts/` because it *modifies* the canonical graph (it's an authoring operation).
`workspace/scripts/build-export.mjs` (when created) will *read* the canonical graph. The two are sequential:
```
scripts/apply-sourcequote-phases.mjs    →  produces updated canonical graph
workspace/scripts/build-export.mjs      →  exports canonical graph to public/exports/
```
