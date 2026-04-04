# Research Architecture vNext (Workshop + Public Static)

## 1) Repository audit (current state)

## 1.1 Canonical graph sources
- Main canonical snapshot: `grc20-these-mael-rolland-v96.json` (loaded by both `graphe.html` and `lecteur.html`).
- Patch/migration artifacts exist at root (`patch_*.json`, `patch_batch*.json`, `new_relations_patch.json`) and in `Migration/`.
- Narrative anchors are derived from the graph with `narrative-anchors-build.mjs` into `narrative-anchors.json`.

## 1.2 Public site structure
- Static HTML pages at repository root (`index*.html`, `these*.html`, `graphe.html`, `lecteur.html`, etc.).
- Shared styles in `style.css`.
- Public assets under `assets/` (PDF, figures, markdown corpus, icons/images).

## 1.3 Current graph loading logic
- `graphe.html` auto-fetches `grc20-these-mael-rolland-v96.json` and optionally `narrative-anchors.json` on startup.
- `lecteur.html` fetches in parallel:
  - graph snapshot
  - section maps (`section_entities_map.json`, `section_overrides.json`)
  - `narrative-anchors.json` when present.
- `story-presets.mjs` is lazy-imported by `graphe.html` for guided story mode.

## 1.4 Narrative / preset / story mechanisms
- `story-presets.mjs`: curated multi-step story scenarios (focus nodes, camera behavior, bridge entities, reveal rules).
- `narrative-anchors-build.mjs`: transforms SourceQuote evidence + section links into anchor scenes.
- `graphe.html`: has scrollytelling sections, story mode panel, and quote citation display logic.

## 1.5 Build / publish scripts
- `grc20-publish.mjs`: snapshot → GRC-20 operations + IPFS + chain anchoring workflow.
- `graph-worker.mjs`: Cloudflare Worker API for graph access with optional x402 payment gate.
- `update-swarm-urls.sh`: ENS/Swarm publication guidance helper.
- `package.json` scripts target publish/deploy actions, not a frontend build chain.

## 1.6 Static deployment assumptions
- Site is static-first (no required runtime backend for core browsing).
- JSON files are served as static assets.
- Optional Worker API can proxy graph access.
- IPFS/Swarm compatibility is already explicit in scripts/docs/UI copy.

## 1.7 Current data flow (observed)
1. Local canonical JSON snapshot is edited/migrated.
2. Optional narrative anchor derivation script generates `narrative-anchors.json`.
3. Static pages fetch the snapshot directly.
4. Optional publication pipeline pushes canonical snapshot to IPFS/GRC-20/ENS surface.

---

## 2) What must remain stable
- Public graph browsing and story mode in `graphe.html`.
- Current canonical graph semantics and availability.
- Static-hosting friendliness (no hard dependency on a live DB).
- Decentralized publication path (IPFS/Swarm/GRC-20 pipeline).

---

## 3) Gaps to address
Current repo already has SourceQuote entities, but lacks a dedicated architecture for:
- explicit **workshop vs canonical** separation,
- first-class **Claim** objects,
- first-class **DecisionTrace** objects,
- normalized **ValidationEvent** records,
- unified **status lifecycle** spanning legacy and new artifacts,
- explicit export boundary from workshop state to public static snapshot.

---

## 4) vNext target architecture

## 4.1 Layer A — Workshop / Authoring / Validation (non-public by default)
Purpose:
- ingest raw material,
- normalize and segment sources,
- create tentative graph objects,
- attach evidence and claims,
- log validation/editorial decisions,
- maintain audit trail.

Proposed workshop root: `workshop/`

## 4.2 Layer B — Public Static Publication
Purpose:
- expose only canonical-approved artifacts,
- keep static deployment intact,
- preserve lightweight graph UX.

Proposed publication roots:
- `public-data/` for export artifacts consumed by static pages,
- existing root static pages remain unchanged.

---

## 5) Status model (non-destructive)

### 5.1 Public-compatible statuses
- `legacy_canonical` (default for pre-existing accepted graph content)
- `needs_review`
- `validated`
- `contested`

### 5.2 Workshop-only transitional statuses
- `raw`
- `extracted`
- `linked`
- `published` (post-export bookkeeping)

### 5.3 Promotion principle
- Existing canonical entities/relations are **not reset**.
- Legacy objects keep `legacy_canonical` until explicitly reviewed.
- Promotion path example:
  `raw -> extracted -> linked -> needs_review -> validated -> published`
- `contested` can branch from any reviewed state and must keep prior provenance.

---

## 6) Object families in vNext
- Canonical graph objects (existing GRC-20 entities/relations/types).
- Working graph objects (candidate entities/relations, unresolved tensions, agent suggestions).
- Evidence objects (`SourceQuote` template + provenance metadata).
- Claim objects (analytical proposition + evidence links).
- DecisionTrace objects (why a modeling/UI/editorial decision happened).
- NarrativePreset / NarrativeStep (story curation with status).
- ValidationEvent objects (who validated what, when, result).

---

## 7) Relation extensions (documented, incremental)
Introduce semantic relations (initially in schema/docs/templates; runtime adoption can be phased):
- `supportedBy` (Claim/Entity -> SourceQuote)
- `derivedFrom` (WorkingObject -> Canonical/Evidence/Source)
- `validatedBy` (Object -> ValidationEvent)
- `contestedBy` (Object -> ValidationEvent/Claim)
- `decidedIn` (Object -> DecisionTrace)
- `includedInNarrative` (Entity/Claim/Quote -> NarrativePreset|NarrativeStep)
- `summarizes` (Claim/Narrative -> target set)
- `transformsInto` (working object promotion lineage)
- `dependsOn` (methodological/structural dependency)

---

## 8) Minimal migration phases

### Phase 1 — Audit + scaffold (this change set)
- add architecture docs,
- add workshop/public folders,
- add object templates,
- keep runtime untouched.

### Phase 2 — Status-aware model prep
- annotate legacy canonical export with `legacy_canonical` default,
- support explicit status fields for new object families.

### Phase 3 — Workshop/public split in pipeline
- implement export selection rules,
- emit canonical-only public JSON bundles under `public-data/`.

### Phase 4 — Optional safe runtime hooks
- optionally load additional metadata files in UI,
- keep fallback to current canonical graph path,
- no mandatory dynamic backend.

---

## 9) Trade-offs and risks
- **Trade-off:** file-first workshop keeps auditability, but requires discipline in schema/version governance.
- **Risk:** schema drift between workshop templates and graph runtime.
  - Mitigation: keep compatibility rules in `docs/architecture/schema-vnext.md` and add lint checks later.
- **Risk:** accidental leakage of non-validated artifacts to public layer.
  - Mitigation: explicit export allowlist and status gating.

---

## 10) IPFS / Swarm continuity
- Public export artifacts remain static JSON files.
- Existing `grc20-publish.mjs`/Worker flow can keep publishing canonical snapshots.
- vNext only adds an upstream workshop layer; it does not replace static publication targets.
