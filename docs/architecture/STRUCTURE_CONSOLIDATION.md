# Structure Consolidation (workshop as canonical lab namespace)

## Decision
On this branch, `workshop/` is the canonical namespace for architecture/lab scaffolding.

## What was consolidated
The following content previously under `workspace/` was moved into `workshop/`:
- `workspace/ARCHITECTURE_AUDIT.md` -> `workshop/ARCHITECTURE_AUDIT.md`
- `workspace/decisions/traces/*` -> `workshop/decisions/traces/`
- `workspace/patches/*` -> `workshop/patches/`
- `workspace/schemas/*` -> `workshop/schemas/`
- `workspace/scripts/*` -> `workshop/scripts/`

Related internal references were updated to point to `workshop/` paths.

## What remains outside `workshop/` by design
- `docs/architecture/` remains the neutral architecture documentation location.
- Existing root-level runtime/public files and deployment logic remain unchanged.
- Existing root-level patch/migration artifacts (`patch*.json`, `Migration/`, `scripts/`) remain in place as historical/source artifacts.

## What was deprecated
- `workspace/` is retained only as a minimal deprecation marker (`workspace/README.md`).

## Why this is non-breaking
This consolidation only changes lab/documentation/tooling paths in the architecture scaffold.
It does not modify public/runtime loaders, canonical graph data, deployment logic, or static publication behavior.
