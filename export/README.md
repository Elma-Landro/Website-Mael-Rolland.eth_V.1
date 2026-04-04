# Export pipeline scaffold

Purpose: define deterministic export from workshop state to canonical public static data.

Target flow:
1. Read canonical baseline + workshop overlays.
2. Apply status gating and promotion rules.
3. Emit publication-ready JSON under `public-data/`.

See `scripts/export-workshop-to-public.mjs` for scaffold logic and TODO points.
