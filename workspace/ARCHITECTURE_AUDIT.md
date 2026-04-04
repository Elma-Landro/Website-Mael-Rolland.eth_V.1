# Architecture Audit — Research Infrastructure
## Date: 2026-04-04
## Scope: grc20-these-mael-rolland v96 + website-mael-rolland.eth_V.1

---

## 1. Current Repository Structure

```
/ (repository root)
├── [30+ HTML files]               — Public website (EN/FR bilingual pairs)
├── style.css                      — Main stylesheet (1,515 lines, CSS custom properties)
├── grc20-these-mael-rolland-v96.json  — Canonical knowledge graph (6.8MB)
├── narrative-anchors.json         — Derived narrative anchor objects (115 anchors, 181KB)
├── narrative-anchors-build.mjs    — Script that derives narrative-anchors.json from graph
├── grc20-publish.mjs              — GRC-20 on-chain publication pipeline
├── graph-worker.mjs               — Cloudflare Worker API for graph serving
├── apply_v91_migration.py         — Python: v90 → v91 migration script (last used migration)
├── grc20_v91_migration_report.json — Migration tracking report (v91)
├── package.json                   — Node.js package (scripts for grc20-publish.mjs)
├── entity_section_map.json        — Entity ID → ThesisSection mapping (5MB)
├── section_entities_map.json      — ThesisSection → entity list mapping
├── section_overrides.json         — Manual overrides for per-section entity pinning
│
├── [13 patch JSON files at root]  — Unorganized, unapplied patches
│   patch_1a_fix_cited_in.json
│   patch_1b_missing_cited_in.json
│   patch_2a_sourcequote_subsections.json
│   patch_2b_central_arguments.json
│   patch_2c_definitions.json
│   patch_3a_intro_subsections.json
│   patch_4_intro_key_entities.json
│   patch_4a_chapter_attribution.json
│   patch_5_missing_sections.json
│   patch_5a_corrective_anchoring.json
│   patch_batch1_anchoring.json
│   patch_batch2_anchoring.json
│   patch_batch3_relations.json
│   new_relations_patch.json       (3MB — largest patch)
│
├── docs/                          — 9 informal audit documents (Markdown)
│   grc20_ontology_audit.md
│   grc20_evidence_audit.md
│   grc20_relations_audit.md
│   grc20_views_audit.md
│   grc20_coverage_fidelity_audit_2026-04-01.md
│   grc20_chapter_anchor_audit.md
│   grc20_narrative_matrix.md
│   grc20_home_cards_editorial_doc.md
│   grc20_final_change_report.md
│   sourcequote-migration-runbook.md
│
├── Migration/                     — Migration ZIPs + agent instructions
│   APPLY_WITH_AGENT.md
│   sourcequote_migration_foundation.zip
│   sourcequote_effective_patch_phase1.zip
│   sourcequote_effective_patch_phase2.zip
│   sourcequote_effective_patch_phase3.zip
│   grc20_v91_patch_seed.json      (referenced by apply_v91_migration.py)
│   ... other migration materials
│
├── assets/
│   ├── MD/                        — Thesis chapters in Markdown (FR + EN)
│   ├── figures/                   — Research diagrams and visualizations
│   ├── img/                       — Photos and images
│   ├── icons/                     — Social media and UI icons
│   └── pdf/                       — Thesis PDFs
```

**No `scripts/` directory exists at repository root**, despite being referenced in `docs/sourcequote-migration-runbook.md`.

---

## 2. Current Graph Architecture

### Canonical graph: grc20-these-mael-rolland-v96.json

| Metric | Value |
|---|---|
| Format | GRC-20 v0.1.0 |
| Total entities | 2,263 |
| Total relations | 20,057 |
| Entity types defined | 55 |
| Relation types defined | 129 |
| Generated at | 2026-03-28 |

**Top entity types by count:**

| Type | Count |
|---|---|
| Reference | 760 |
| Concept | 391 |
| SourceQuote | 245 |
| InfrastructureEvent | 158 |
| AcademicWork | 143 |
| Person | 138 |
| GreyLiterature | 87 |
| PrimarySource | 71 |
| ThesisSection | 70 |
| CrisisEvent | 55 |

**SourceQuote field coverage (245 entities):**

| Attribute | Present | Coverage |
|---|---|---|
| `quoteText` | 236 | 96% |
| `page` | 231 | 94% |
| `chapter` | 230 | 94% |
| `thesisLocation` | 194 | 79% |
| `language` | 192 | 78% |
| `sourceFormat` | 191 | 78% |
| `evidenceStatus` | 99 | 40% |
| `source` | 55 | 22% |
| `speaker` | 11 | 4% |

**Relations on SourceQuote:**

| Relation | Direction | Count |
|---|---|---|
| `appears in section` | FROM SourceQuote | 867 |
| `quote supports` | FROM SourceQuote | 390 |
| `cited in` | FROM SourceQuote | 133 |
| `supported by quote` | TO SourceQuote | 122 |

**Status coverage:** Only 13 entities have any status-like attribute (`evidenceStatus`). No uniform `status` field across entity types.

### Entity types defined but with zero instances (notable):
- `Argument` (type defined; planned for dialectical layer)
- `AnalyticClaim` (type defined in v91 migration)
- `NarrativeCluster` (type defined)
- `DoctoralThesis` (type defined — surprisingly absent)

### Working knowledge layers: absent
The current architecture has no separation between:
- canonical (stable, reviewable) knowledge
- working/candidate (extracting, annotating, tentative) knowledge

All content is in the single canonical JSON file.

---

## 3. Public Site Architecture

### graphe.html (313KB)
- Interactive Cytoscape.js force-directed graph (+ matrix, archipelago, tree modes)
- Loads `grc20-these-mael-rolland-v96.json` directly via `fetch()`
- Also loads `narrative-anchors.json` for story mode
- No dynamic backend required; runs 100% in browser
- Entity display uses: `name`, `type_id`, computed `color`/`shape`/`size`
- Current visualization does NOT display `evidenceStatus`, `quoteText`, or provenance data

### lecteur.html (95KB)
- Markdown thesis reader with side-by-side graph (Cytoscape instance)
- Loads chapter Markdown from `assets/MD/`
- Has an annotation system that can create/link entities — but output is not persisted back to canonical graph
- Entity mentions in Markdown text are detected and linked to graph nodes

### graph-worker.mjs
- Cloudflare Worker API serving graph data with optional x402 micro-payment gating
- Endpoints: `/graph`, `/graph?entity=<id>`, `/graph?search=<q>`, `/stats`, `/types`
- Consumes IPFS-hosted graph snapshot (via `IPFS_CID` env var)

### grc20-publish.mjs
- CLI pipeline for publishing the canonical graph to GRC-20 protocol on-chain
- `--dry-run` flag available
- Reads the canonical JSON, batches operations, publishes to IPFS then on-chain

---

## 4. Pain Points

### P1: No authoring/workshop layer separation
Everything lives at repository root. The public website files (`graphe.html`, `index.html`) sit alongside
migration scripts, patch JSON files, and audit documents with no organizational separation.

### P2: Unclear scripts boundary
`docs/sourcequote-migration-runbook.md` references `scripts/apply-sourcequote-phases.mjs`
and `scripts/sourcequote-migration/*.mjs`. These scripts **do exist** at `scripts/` in the
repository root (along with `generate_corrective_patch.mjs`, `generate_chapter_patch.mjs`,
and three batch variants). However, the `scripts/` directory has no README, no description of
what each script does, and no documented relationship to the canonical graph version lifecycle.
The boundary between graph-generation scripts (root `scripts/`) and the new build/export/lint
pipeline (planned at `workspace/scripts/`) must be made explicit — see `workspace/scripts/README.md`.

### P3: Untracked patch status
13+ patch JSON files exist at root. It is unknown which are already incorporated into v96
and which are pending application. The v96 graph already has 245 SourceQuote entities,
suggesting many patches ARE applied — but no merge log exists.

### P4: Status model is embryonic
Only 13/2,263 entities have an `evidenceStatus` attribute. No uniform, schema-defined status
lifecycle applies to entities, relations, or evidence objects. The `legacy_canonical` /
`validated` / `needs_review` distinction does not exist in the data.

### P5: DecisionTrace is absent
Significant decisions (entity merges in v91, type additions in v91, section assignment corrections)
are recorded only in informal Markdown audit docs and the `grc20_v91_migration_report.json`.
No machine-readable decision log exists.

### P6: No export pipeline
There is no script that takes the canonical graph, applies validated pending patches,
and produces a clean versioned public snapshot. The publish pipeline (`grc20-publish.mjs`)
sends directly on-chain but does not produce a local clean export artifact.

### P7: NarrativePreset management is incomplete
`narrative-anchors.json` is derived from the canonical graph by `narrative-anchors-build.mjs`.
But NarrativePresets (higher-level curated narrative sequences) are not managed.
There is no schema, no registry, no workflow for creating/updating presets.

### P8: Evidence layer not surfaced in UI
`graphe.html` does not display `quoteText`, `evidenceStatus`, page/section attribution,
or provenance data for any node — despite this data existing for 245 SourceQuote entities.

---

## 5. Proposed Target Architecture

```
/
├── workspace/           ← NEW: authoring/workshop layer (Layer A)
│   ├── schemas/         ← JSON Schema definitions for all workspace types
│   ├── scripts/         ← build-export, lint, apply-patches scripts
│   ├── patches/         ← organized patch files (pending/ vs applied/)
│   ├── evidence/        ← working evidence candidates
│   ├── decisions/       ← machine-readable DecisionTrace objects
│   ├── narratives/      ← NarrativePreset and NarrativeStep objects
│   └── audits/          ← Phase 2: consolidate docs/ here
│
├── public/exports/      ← NEW: static export target (Layer B output)
│   ├── graph-snapshot.json     ← canonical + validated patches
│   ├── narrative-anchors.json  ← regenerated from snapshot
│   └── export-manifest.json    ← metadata, timestamps, checksums
│
├── [all existing files]   ← UNCHANGED (zero breakage)
│   graphe.html
│   lecteur.html
│   grc20-these-mael-rolland-v96.json  ← still canonical (read-only)
│   ...
```

**Key architectural invariant:**
The canonical graph (`grc20-these-mael-rolland-v96.json`) is **read-only** from workspace scripts.
Workspace scripts write to `public/exports/` only.
The public site can be pointed to `public/exports/graph-snapshot.json` in Phase 4 (optional).

---

## 6. New Object Types (workspace-layer)

### Claim
Complements `AnalyticClaim` entity type (already defined in v96 types, zero instances).
A Claim is an explicit analytical proposition with evidence, confidence, and lineage.
Lives in `workspace/` until validated, then promoted to graph entity via patch.

### DecisionTrace
Machine-readable record of architectural/editorial decisions.
Lives in `workspace/decisions/traces/`.
NOT a graph entity type — purely workspace metadata.

### NarrativePreset
Higher-level narrative structure referencing NarrativeAnchor IDs.
Lives in `workspace/narratives/presets/`.
Published NarrativePresets are included in `public/exports/`.

### NarrativeStep
One step within a NarrativePreset.
References entity IDs from canonical graph and anchor IDs from `narrative-anchors.json`.

### ValidationEvent
Record of a validation action (human or agent review) on a graph entity or relation.
Provisional format; not yet wired to canonical graph.

---

## 7. Status and Trust Model

All graph objects are implicitly `legacy_canonical` unless otherwise annotated.

| Status | Objects | Transition |
|---|---|---|
| `legacy_canonical` | All v96 entities/relations | Manual review → `validated` |
| `raw` | Extracted candidates | Process → `extracted` |
| `extracted` | Processed, normalized | Link to graph → `linked` |
| `linked` | Connected to graph | Review → `needs_review` or `validated` |
| `needs_review` | Flagged | Review → `validated` or `contested` |
| `validated` | Confirmed | Include in export → `published` |
| `contested` | Unresolved ambiguity | Resolution → `validated` or `deprecated` |
| `published` | In public snapshot | — |
| `deprecated` | Superseded | — |

The status field is additive — existing entities are NOT bulk-rewritten.
New entities carry explicit status. Legacy entities are inferred as `legacy_canonical`.

---

## 8. Build Pipeline (Target)

```
workspace/scripts/lint-graph.mjs    → consistency report (no writes)
workspace/scripts/apply-patches.mjs → apply pending patches (dry-run first)
workspace/scripts/build-export.mjs  → compile public snapshot (dry-run first)

Pipeline order:
1. npm run lint            → identify issues
2. npm run apply-patches -- --dry-run   → preview patch application
3. npm run apply-patches               → apply patches (produces new graph version)
4. npm run export -- --dry-run         → preview export
5. npm run export                      → write public/exports/
6. [manual] Deploy public/exports/ to IPFS/Swarm
```

---

## 9. Migration Path

### Phase 1 (current, non-destructive)
- Introduce `workspace/` folder structure
- Create schema definitions and READMEs
- Create dry-run lint/export/apply-patches scripts
- Zero changes to public site or canonical graph

### Phase 2 (patch consolidation)
- Audit each root patch against v96
- Move patches to `workspace/patches/pending/` or `applied/`
- Move `docs/` to `workspace/audits/`
- Move `Migration/` to `workspace/migrations/`
- Produce v97 graph snapshot

### Phase 3 (evidence validation + agent workflows)
- Fill `evidenceStatus` gaps on SourceQuote entities (currently 40% coverage)
- Introduce `status` field standard across new entities
- Enable agent-assisted extraction of new SourceQuote candidates
- Populate `workspace/decisions/traces/` from historical audit records

### Phase 4 (UI improvements + optional SQLite)
- Update `graphe.html` entity panel to show evidence/provenance
- Optionally introduce SQLite index for fast authoring queries
- Point public site to `public/exports/graph-snapshot.json`

---

## 10. Risks and Trade-offs

| Risk | Severity | Mitigation |
|---|---|---|
| Patch merge conflicts (v96 already has applied patches) | Medium | Audit each patch against v96 before applying |
| SourceQuote pages unreliable (PDF pagination vs Markdown) | Low | Already noted in evidence audit; `evidenceStatus` field captures this |
| Large canonical JSON (6.8MB) is slow to process | Low | Index-building pattern from `narrative-anchors-build.mjs` works; keep it |
| Agent overwrite of canonical graph | Medium | Scripts never write to canonical JSON; export goes to `public/exports/` only |
| UI breakage if `graphe.html` is redirected to new snapshot | Medium | Phase 4 only; keep `graphe.html` pointing to v96 until snapshot is confirmed identical |
| `entity_section_map.json` (5MB) may be stale | Low | Document and regenerate from v97 when ready |
