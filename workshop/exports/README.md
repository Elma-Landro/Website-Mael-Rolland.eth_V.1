# workshop/exports

This folder stores **dry-run export reports** for the workshop architecture.

- `export-policy.json`: manifest-driven policy for object-family visibility and status gating.
- `export-dry-run.json`: machine-readable report generated from policy + current workshop artifacts.
- `EXPORT_DRY_RUN.md`: human-readable dry-run summary.

Scope note: this layer is documentary only in current phase. It does not mutate canonical graph files, publish assets, or runtime loaders.
