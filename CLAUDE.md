# CLAUDE.md — AI Assistant Guide for Website-Mael-Rolland.eth_V.1

This file provides context and conventions for AI assistants (Claude Code and others) working in this repository.

---

## Project Overview

Personal academic website and Web3 infrastructure for **Maël Rolland** (`mael-rolland.eth`), a PhD researcher at EHESS (École des Hautes Études en Sciences Sociales). The site presents a dissertation titled *"Au-delà des codes : infrastructure et gouvernance discrète et polycentrique des crypto-monnaies Bitcoin et Ethereum dévoilée par leurs crises"* (defended December 13, 2024, advisor: Ève Chiapello).

The project bridges traditional academic publishing with Web3-native distribution:
- Static HTML/CSS/JS frontend (no framework, no build step)
- A doctoral thesis rendered as a traceable **GRC-20 knowledge graph** (~2,269 entities / ~20,104 relations)
- Cloudflare Worker API with x402 micro-payment support
- IPFS/Swarm decentralized hosting via ENS (`mael-rolland.eth.limo`)

There is also an applied research lab identity: **TheDyorLab** (`thedyorlab.eth`).

> **Read this first.** This repository is a *scientific object*, not a conventional web app. The graph encodes verifiable claims about a 465-page thesis. **Traceability and evidence integrity outrank speed and coverage.** Never invent entities, relations, quotes, page numbers, or chapter attributions. A smaller verified change always beats a richer speculative one.

---

## ⚠️ Critical facts to know before editing

1. **There is no `main` or `master` branch.** The repository default branch is
   `codex/create-expand-from-node-planning-documents`. Detect the default branch
   dynamically (`git ls-remote --symref origin HEAD`); never hardcode `main`.
2. **The canonical graph snapshot is `grc20-these-mael-rolland-v99.json`**, but the
   **runtime still loads v96** (see [Version lag](#version-lag-read-before-touching-graph-data)).
   Do not "fix" this by bumping loaders without an explicit instruction.
3. **Graph files are never edited in place.** Each change produces a new
   `grc20-these-mael-rolland-v<N+1>.json` via a generator script. See
   [Patch → version workflow](#patch--version-workflow).
4. **There is no `.gitignore`.** Be extremely careful never to `git add` a `.env`,
   a key file, or a local scratch artifact.
5. **No tests, no CI, no linter.** Validation is done by the audit scripts
   (`scripts/audit_graph.py`, `workshop/scripts/lint-workshop-artifacts.mjs`) and
   by `npm run dry-run`.

---

## Repository Structure

```
/
├── ── Public static site (root-level HTML) ──────────────────────────────
├── index.html / index-fr.html                  # Landing page (EN/FR)
├── these.html / these-fr.html                  # Thesis showcase + downloads
├── curriculum.html / curriculum-fr.html
├── cv.html / cv-fr.html                        # Detailed CV (EN/FR)
├── contact.html / contact-fr.html
├── collaborate.html / collaborate-fr.html
├── talks.html / talks-fr.html
├── crisis.html / crisis-fr.html                # Bitcoin CVE 2018 + DAO hard fork case studies
├── soutenance.html / soutenance-fr.html        # Defense presentation (EN/FR)
├── soutenance-edition.html / soutenance-edition-fr.html
├── atelier.html / workshop.html                # Workshop page (FR/EN pair)
├── rare-pepe.html / rare-pepe-fr.html
├── 404.html / 404-fr.html
├── sitemap.html / plan-du-site.html            # Human sitemap (EN/FR)
├── style.css                                   # Main stylesheet (1,515 lines)
│
├── ── Graph runtime ─────────────────────────────────────────────────────
├── graphe.html                                 # Interactive knowledge-graph viewer (6,696 lines)
├── graphe.*.js                                 # 14 extracted modules (see load order below)
├── lecteur.html                                # Markdown thesis reader (2,539 lines)
├── story-presets.mjs                           # Guided "story mode" scenarios (5 stories)
├── narrative-anchors.json                      # Derived quote↔entity↔section anchors
├── narrative-anchors-build.mjs                 # Generator for narrative-anchors.json
│
├── ── Canonical graph data ──────────────────────────────────────────────
├── grc20-these-mael-rolland-v99.json           # CANONICAL snapshot (v99)
├── grc20-these-mael-rolland-v98.json           # Retained history
├── grc20-these-mael-rolland-v97.json
├── grc20-these-mael-rolland-v96.json           # Still loaded by the runtime
├── entity_section_map.json                     # Entity ID → thesis subsection
├── section_entities_map.json                   # Thesis section → entity list
├── section_overrides.json                      # Manual overrides for section assignments
├── patch_*.json / new_relations_patch.json     # Historical + active patch payloads
│
├── ── Publication / API ─────────────────────────────────────────────────
├── grc20-publish.mjs                           # GRC-20 on-chain publication pipeline
├── graph-worker.mjs                            # Cloudflare Worker graph API (x402)
├── update-swarm-urls.sh                        # Swarm/IPFS deployment helper
├── package.json                                # Node deps + npm scripts (publish only)
│
├── ── Governance & process ──────────────────────────────────────────────
├── agents/                                     # Agent charter: roles, modes, genealogy
│   ├── README.md                               # ★ Charter — read before acting as an agent
│   ├── Agent_Creation_Rules.md
│   ├── Hermes.md                               # Orchestrator agent spec
│   └── Codex.md                                # Executor agent spec
│
├── ── Documentation ─────────────────────────────────────────────────────
├── docs/
│   ├── architecture/                           # Seam plans, boundary contracts, vNext design
│   ├── audits/                                 # Dated graph audits + supporting CSV data
│   ├── research/catalogue-evenements/          # Event catalogue research (CSV + fusion.py)
│   └── grc20_*.md                              # Ontology / relations / evidence / views audits
│
├── ── Workshop (authoring & validation layer) ───────────────────────────
├── workshop/                                   # ★ Canonical lab namespace
│   ├── schemas/                                # JSON Schemas: claim, source-quote, decision-trace…
│   ├── templates/                              # Blank templates per object family
│   ├── claims/ evidence/ validations/          # Workshop object instances
│   ├── decisions/traces/                       # Editorial decisions with rationale
│   ├── narratives/presets/
│   ├── patches/                                # Patch inventory + audit
│   ├── scripts/                                # lint-workshop-artifacts, audit-patches, export dry-run
│   ├── exports/                                # Export policy + dry-run output
│   └── PROMOTION_WORKFLOW.md                   # How workshop objects reach public status
│
├── ── Pipelines & scaffolds ─────────────────────────────────────────────
├── scripts/                                    # Patch generators & audit tooling (.mjs + .py)
│   └── sourcequote-migration/                  # SourceQuote migration orchestrator
├── patches/                                    # Structured patch payloads (v97+)
├── Migration/                                  # Historical migration bundles (.zip) + briefs
├── export/                                     # workshop → public-data export scaffold
├── public-data/                                # (reserved) generated public artifacts
├── schema/                                     # Schema layer pointer → docs/architecture/schema-vnext.md
├── workspace/                                  # DEPRECATED — marker only, use workshop/
│
└── assets/
    ├── MD/                                     # Full thesis text in Markdown (bilingual)
    │   ├── INDEX.md                            # ★ Agent-readable entry point for thesis content
    │   ├── 00_introduction.md / _EN.md
    │   ├── 01_chapitre_I.md / _EN.md
    │   ├── 02_chapitre_II.md / _EN.md
    │   ├── 03_chapitre_III.md / _EN.md
    │   ├── 04_conclusion.md / _EN.md
    │   ├── 05_glossaire_annexes.md / 05_glossary_appendix_en.md
    │   ├── 06_resume.md
    │   └── style.css                           # Stylesheet for lecteur.html
    ├── Mael_Rolland_CV_Court2026.html          # Standalone HTML CV for print/PDF
    ├── img/  figures/  icons/  pdf/
```

---

## Tech Stack

### Frontend
- **Pure static HTML/CSS/JS** — no bundler, no framework (React/Vue/etc.), no build step
- **CSS custom properties** for theming (light/dark via `data-theme` on `<html>`)
- **Google Fonts**: "Press Start 2P" (primary), "VT323" (monospace) — retro/pixel aesthetic
- **Cytoscape 3.28 + dagre** loaded from CDN in `graphe.html` (no npm dependency)
- **Bilingual**: every page has an EN and FR counterpart with a language switcher

### Node / infrastructure
- **Node.js ≥ 18** with ES Modules (`"type": "module"`)
- **GRC-20 protocol** (`@graphprotocol/grc-20`) for knowledge-graph publishing
- **Viem 2.x** for Ethereum/Web3 interactions
- **Cloudflare Workers** (Wrangler 3.x) for the graph API
- **x402 payment protocol** for USDC micro-payments on Base
- **IPFS** (cascading gateway fallback) and **Swarm** for decentralized hosting
- **Python 3 (stdlib only)** for graph audit and version-generator scripts — no external deps

### Deployment
- Primary: `https://mael-rolland.eth.limo` (ENS contenthash → IPFS/Swarm)
- Cloudflare Worker for the Graph API
- Deployment is **manual** — there is no CI/CD

---

## npm Scripts

```bash
npm run dry-run          # Test GRC-20 pipeline locally (no on-chain writes)
npm run testnet          # Publish to GRC-20 testnet
npm run mainnet          # Publish to GRC-20 mainnet (requires GEO_PRIVATE_KEY)
npm run new-space        # Create new GRC-20 space on testnet
npm run worker-dev       # Local dev server for Cloudflare Worker (localhost:8787)
npm run worker-deploy    # Deploy Worker to Cloudflare
```

> **Note**: all four GRC-20 scripts hardcode `--input ./grc20-these-mael-rolland-v96.json`.
> To act on the canonical snapshot, pass `--input ./grc20-these-mael-rolland-v99.json`
> explicitly, or run `node grc20-publish.mjs` directly.

Scripts that are **not** in `package.json` and must be invoked directly:

```bash
python3 scripts/audit_graph.py --input grc20-these-mael-rolland-v99.json   # read-only structural audit
node narrative-anchors-build.mjs --input ./grc20-these-mael-rolland-v99.json --out ./narrative-anchors.json
node workshop/scripts/lint-workshop-artifacts.mjs                          # validate workshop JSON objects
node workshop/scripts/audit-patches.mjs                                    # inventory patch artifacts
node workshop/scripts/build-export-dry-run.mjs                             # export dry-run report
node scripts/apply-sourcequote-phases.mjs [--write]                        # SourceQuote migration orchestrator
node export/scripts/export-workshop-to-public.mjs                          # workshop → public-data (scaffold)
```

---

## GRC-20 Knowledge Graph

### Version lag (read before touching graph data)

Four snapshots coexist, and **the canonical file is not the one the site loads**:

| File | Entities | Relations | Role |
|------|----------|-----------|------|
| `…-v99.json` | 2,269 | 20,104 | **Canonical.** +37 `occurs in` relations wiring maturation-phase events |
| `…-v98.json` | 2,269 | 20,067 | +6 chronology events missing from v97, +25 relations |
| `…-v97.json` | 2,263 | 20,042 | Removed 15 truncated/broken relations |
| `…-v96.json` | 2,263 | 20,057 | **Still loaded at runtime** by `graphe.html` and `lecteur.html` |

Consumers currently pinned to **v96**:
- `graphe.html:6270` — `fetch('grc20-these-mael-rolland-v96.json')`
- `lecteur.html:1029` — `const GRAPH_FILE = './grc20-these-mael-rolland-v96.json'`
- `package.json` — all four GRC-20 npm scripts
- `narrative-anchors.json` — `generated_from: grc20-these-mael-rolland-v96.json`
- `workshop/` sample objects and `PROMOTION_WORKFLOW.md`

This lag is deliberate in the current phase (the workshop workflow treats v96 as the
"authoritative baseline for currently published graph structure"). **Do not silently
promote the runtime to v99.** If asked to do so, update *all* consumers above together,
regenerate `narrative-anchors.json`, and re-run `scripts/audit_graph.py`.

### Graph JSON shape

```jsonc
{
  "space":          { "id", "name", "controller_ens", "version", "generated_at", "note" },
  "types":          [ { "id": "<32-hex>", "name": "Person", "description": { … } } ],   // 55 types
  "relation_types": [ { "id": "<32-hex>", "name": "cited in", … } ],                     // 130 types
  "entities":       [ { "id", "name", "description", "types": ["<typeId>"], "attributes": {} } ],
  "relations":      [ { "id", "type": "<relTypeId>", "from": "<entityId>", "to": "<entityId>", "attributes": [] } ],
  "ops":            [ … ]                                                                // 293 wire operations
}
```

Conventions that matter:
- Entity/type IDs are **32-char lowercase hex**; relation IDs are base58-ish 22-char strings.
- `description` and text attributes use the `{ type: "TEXT", value, options: { language } }` envelope — never a bare string.
- `types` is an **array** on entities (an entity may carry more than one type).
- The `space.note` field is an append-only changelog. Add a line for every new version.

### Entity types (55) — most populated

| Type | Count | Notes |
|------|-------|-------|
| `Reference` | 760 | Bibliographic references (deduplicated) |
| `Concept` | 391 | Theoretical and empirical concepts |
| `SourceQuote` | 245 | Verbatim thesis quotations with page numbers |
| `InfrastructureEvent` | 164 | Infrastructure milestones |
| `AcademicWork` | 143 | Papers, books |
| `Person` | 138 | Researchers, developers, interviewees |
| `GreyLiterature` | 87 | Non-academic sources |
| `PrimarySource` | 71 | Primary source documents |
| `ThesisSection` | 70 | Navigable subsections (I.1.1–III.3.4) |
| `CrisisEvent` | 55 | Bitcoin CVE 2018, DAO hard fork, etc. |
| `IndigenousLiterature` | 53 | Community-originated sources |
| `Capability` | 38 | Protocol capabilities |
| `StakeholderCategory` | 36 | Actor categories |

Remaining types include `ActorNonHuman`, `ActorGroup`, `Organization`, `Institution`,
`Protocol`, `TheoreticFramework`, `Argument`, `Method`, `Corpus`, `Chapter`,
`DoctoralThesis`, `CrisisPhase`, `DevelopmentPhase`, `MonetaryObject`, `NarrativeCluster`,
`GovernanceArena`, `GovernanceConflict`, `GovernanceProcess`, `ProtocolChange`,
`ProtocolProposal`, `InfrastructureDomain`, `InfrastructureSegment`, `PriceSeries`,
`PriceWindow`, `SoftwareClient`, `CodeRepository`, `SmartContract`, `PlatformService`,
`MediaOutlet`, `Marketplace`, `HardwareDevice`, `AnalyticClaim`, `NativeFormula`, and others.

> **Ontology debt** — the type list carries near-duplicate pairs from earlier migrations:
> `Institution`/`Organization`, `CoreConcept`/`ConceptCore`, `SecondaryConcept`/`ConceptSecondary`,
> `TechnicalConcept`/`ConceptTechnical`, `ChapterSection`/`ThesisSection`.
> Three types are currently unused: `InfrastructureService`, `ConceptCore`, `ConceptSecondary`.
> **Do not merge or delete these on your own initiative** — type consolidation is a
> scientific decision reserved for the author. See `docs/grc20_ontology_audit.md`.

### Relation types (130) — most used

| Relation | Count |
|----------|-------|
| `appears in section` | 12,422 |
| `cited in` | 2,690 |
| `quote supports` | 392 |
| `part of` | 374 |
| `source of` | 368 |
| `belongs to domain` | 349 |
| `contributes to` | 332 |
| `applied to` | 321 |
| `has concept` | 307 |
| `occurs in` | 207 |

`appears in section` dominates the graph (~62% of edges). Audit scripts flag entities
connected *only* by `appears in section` as "pseudo-orphans" — they are structurally
present but analytically unanchored.

### Mapping files

| File | Purpose |
|------|---------|
| `entity_section_map.json` | Entity ID → thesis subsection |
| `section_entities_map.json` | Section ID → entity list (loaded by `lecteur.html`) |
| `section_overrides.json` | Manual overrides for ambiguous assignments |

---

## Patch → version workflow

Graph changes follow a strict, reproducible, append-only pipeline. **The active graph file is
never mutated in place.**

1. **Audit** — produce a Markdown report under `docs/audits/`, with supporting CSVs in
   `docs/audits/data/`. Read-only. `python3 scripts/audit_graph.py` gives the deterministic
   structural baseline (exit 0 = clean, 1 = critical issue, 2 = fatal error).
2. **Author a patch payload** — `patch_<N>_<slug>.json` at root (or under `patches/` for
   v97+ payloads). A patch carries a `_meta` block plus the operations
   (`new_relations`, added entities, etc.).
3. **Write a generator script** — `scripts/make_v<N>_<slug>.py` (Python 3, stdlib only) that
   reads `v<N-1>.json` + the patch and writes `v<N>.json`. Generators must:
   - default their `--source` / `--patch` / `--target` paths,
   - support `--dry-run`,
   - **validate before writing** and fail loudly rather than emit a doubtful graph,
   - append a summary line to `space.note` and bump `space.version`.
4. **Re-audit** the produced version, then document the outcome in `docs/audits/`.
5. **Open a PR** for human review. No agent merges its own PR.

Reference implementations: `scripts/make_v97_remove_truncated_broken_relations.py`,
`scripts/make_v98_add_missing_chronology_events.py`,
`scripts/make_v99_wire_maturation_phase.py`, and the older `apply_v91_migration.py` at root.

Patch payloads currently at root (`patch_1a` … `patch_12`, `patch_batch1-3`,
`new_relations_patch.json`) are **historical artifacts** — they record how earlier versions
were produced. They are not re-applied automatically.

---

## Graph runtime architecture (`graphe.html`)

`graphe.html` is a client-side Cytoscape visualization of the knowledge graph. It has been
progressively modularized: pure/stateful logic is being extracted into sibling
`graphe.*.js` files, each an IIFE attaching a namespace to `window`.

**Load order matters** — scripts are plain `<script>` tags (not modules), so dependencies
resolve by ordering (`graphe.html:11-24`):

```
graphe.helpers.js          → GrapheHelpers        (escHtml, generateId, normalizeRelationName…)
graphe.event-bus.js        → GrapheEventBus       (on/emit — the seam between runtime layers)
graphe.story-helpers.js    → story step/scene resolution
graphe.state.js            → GrapheState          (data, undo stack, indexes: outgoing/incoming…)
graphe.validation-export.js
graphe.modals.js
graphe.panels.js
graphe.panel-render.js
graphe.ui-panel.js
graphe.ui-panel-actions.js
graphe.ui-entity-forms.js
graphe.ui-filters.js
graphe.ui-search.js
graphe.ui-relations-modal.js
```

`story-presets.mjs` is **lazy-imported** as an ES module at runtime
(`graphe.html:5460`), separate from the classic-script chain.

### Extraction conventions

The modularization is deliberately incremental and reversible:
- Each extracted module must be **behavior-preserving** — same API contract as the inlined code.
- Cross-layer calls go through `GrapheEventBus` where a seam has been established
  (e.g. `layout:apply-requested`), with an inline fallback preserved for the un-migrated path.
- Every seam extraction is documented in `docs/architecture/` as a
  *cross-call audit* → *seam plan* → *validation result* triple. Read the relevant
  `STORY_*` / `GRAPH_*` docs before moving code across a boundary.
- `docs/architecture/STORY_EXPAND_CONTRACT_FREEZE.md` records contracts that are frozen —
  do not change those signatures.

### Layouts and story mode

Three named layouts: `matrice` (chapter × type grid with canvas halos), `monetisation`,
`qui-gouverne`. Story presets bind to a layout via `layoutTarget`, and switching story
auto-switches layout.

`story-presets.mjs` defines five guided stories:
`monetisation-cryptos`, `qui-gouverne-reellement`, `crises`, `structure-these`, `fil-de-preuves`.
Each has ordered `steps` with `centralNode`, `focusNodes`, `cameraPreset`, `bridgeEntityIds`,
and reveal options (`edgeMode`, `maxAutoEdges`, `hideBackbone`…). Story text is **French** and
is editorial content — treat it like thesis prose, not UI copy.

### Narrative anchors

`narrative-anchors-build.mjs` derives `narrative-anchors.json` from the graph by joining:
a `SourceQuote` → the entities it supports (`quote supports`) → the section it appears in
(`appears in section`) → a graph scene definition. Consumed by `lecteur.html` (quote panel),
`graphe.html` (scrollytelling anchors), and referenceable by ID from `story-presets.mjs`.

**Regenerate it whenever SourceQuote or section relations change.**

---

## Agent governance model

`agents/README.md` is a binding charter for any automated contributor, including Claude.
Read it before making changes. Core rules:

**Three modes of intervention** — when the mode is ambiguous, **default to Mode A**:

| Mode | Name | Does | Does not |
|------|------|------|----------|
| **A** | Audit | Reads, inspects, compares graph claims to thesis evidence, writes a Markdown report | Modifies nothing |
| **B** | Proposal | Proposes changes with evidence, risks, expected impact | Modifies no files |
| **C** | Patch / PR | Branches, applies minimal verified changes, validates, writes a changelog, opens a PR | Never overwrites the active graph file; never merges without human review |

**Authority model** — Maël Rolland is the final scientific arbiter. He alone authorises schema
changes, entity merges, deletions, and ID renames. Agents execute bounded missions.

**Rule 3 (anti error-propagation)**: output produced by one agent and consumed by another
remains **annotated as data, not fact**, until a human validates it. Do not let an unverified
conclusion silently become a premise.

**Rule 4**: every agent file records *why* the agent exists (its genealogy).

Two agents are active: **Hermes** (orchestrator — audits, proposes, delegates) and
**Codex** (executor — bounded code tasks, patch generation, validation). Seven further
agents are deferred pending a documented, measured need (`agents/Agent_Creation_Rules.md`).

---

## Workshop layer

`workshop/` is the canonical namespace for authoring and validation work that is **not yet
public**. Public static pages must **not** depend on it.

Object families, each with a JSON Schema in `workshop/schemas/` and a blank template in
`workshop/templates/`: `SourceQuote` (evidence), `Claim`, `ValidationEvent`, `DecisionTrace`,
`NarrativePreset` / `NarrativeStep`.

**Status vocabulary** (defined in `workshop/PROMOTION_WORKFLOW.md`, gated in
`workshop/exports/export-policy.json`, shape in `workshop/schemas/status-model.json`):
`raw` → `extracted` → `linked` → `needs_review` → `validated` → `published`.

**Promotion is not automated in this phase** (`workshop/PROMOTION_WORKFLOW.md`):
no workshop script writes back into canonical graph files, and dry-run classifications are
advisory only. Evidence↔claim linkage is expressed by object-level ID references
(`claim.linkedEvidenceIds`, `sourceQuote.linkedClaimIds`), not by canonical graph relations.

`export/scripts/export-workshop-to-public.mjs` is the scaffold for the future
workshop → `public-data/` export. `public-data/` is currently empty by design.

`workspace/` is **deprecated** — a marker directory only. Everything moved to `workshop/`
(see `docs/architecture/STRUCTURE_CONSOLIDATION.md`).

---

## Key source files

### `grc20-publish.mjs` — publication pipeline

Converts a JSON snapshot to GRC-20 wire format and publishes it on-chain.

| Flag | Description |
|------|-------------|
| `--input <file>` | Path to GRC-20 JSON snapshot |
| `--private-key <key>` | Ethereum private key (prefer the env var) |
| `--network TESTNET\|MAINNET` | Target network |
| `--dry-run` | Validate without publishing |
| `--create-space` | Create a new GRC-20 space |
| `--batch-size <n>` | Ops per IPFS edit (default: 200) |
| `--author <ens>` | ENS address for authorship |

Environment variables (preferred over CLI flags):
`GEO_PRIVATE_KEY` (**never commit**), `GEO_SPACE_ID`, `GEO_NETWORK`, `GEO_INPUT`, `GEO_AUTHOR`.

### `graph-worker.mjs` — Cloudflare Worker API

| Path | Description |
|------|-------------|
| `GET /` | Graph metadata + navigation links |
| `GET /graph` | Full GRC-20 graph (paginated) |
| `GET /graph?entity=<id>` | Single entity + neighborhood |
| `GET /graph?type=<name>` | All entities of a type |
| `GET /graph?search=<query>` | Full-text search on entity names |
| `GET /graph?depth=<n>` | Neighborhood depth (max 3) |
| `GET /stats` | Public graph statistics (free) |
| `GET /types` | Public entity type list (free) |

Environment: `IPFS_CID`, `WALLET_ADDRESS`, `PRICE_USDC` (default 0.001),
`GRAPH_URL_FALLBACK`, `MODE` (`free` | `x402` | `x402-optional`).

### `lecteur.html` — thesis reader

Loads the graph snapshot, `section_entities_map.json`, `section_overrides.json`, and
`narrative-anchors.json` in parallel, then renders the Markdown chapters from `assets/MD/`
with an entity side-panel and local annotation export.

### `style.css` — design tokens

```css
/* Light theme (default) */
--bg-primary: #6a0000 → #4d0000   (dark burgundy)
--text-primary: #ffcc66            (golden)
--text-secondary: #ffaa33          (orange)
--text-accent: #33ff33             (neon green)
--button-bg: #8b0000               (dark red)
--button-border: #ffcc66

/* Dark theme */
--bg-primary: #000000              (black)
--text-primary: #ffd700            (brighter gold)
```

`image-rendering: pixelated` is used throughout — intentional, not a bug.

---

## HTML page conventions

Every page follows this pattern:

1. **`<head>`**: `charset="UTF-8"`, responsive viewport, SEO `<meta>` description,
   Open Graph + Twitter Card tags, `hreflang` links for the EN/FR counterpart,
   DNS prefetch for external domains, CSS `<link rel="preload">` before the stylesheet,
   Google Fonts preload.
2. **`<body>`**: fixed top-right theme toggle (sets `data-theme="dark"` on `<html>`),
   language switcher (EN ↔ FR), main content, shared social-icon section.
3. **Structured data**: JSON-LD `schema.org/Person` on the landing page.
4. **Forms**: [FormSubmit.co](https://formsubmit.co) — no backend required.

### Bilingual convention

- English: `page.html` — French: `page-fr.html`
- Exception: the workshop page pair is `workshop.html` (EN) / `atelier.html` (FR)
- Both versions are maintained in sync — **always update both when editing content**
- Assets (PDFs, images) are shared between languages

---

## Design aesthetic

Intentional retro/pixel-art style:
- Font "Press Start 2P" (8-bit arcade) — do not replace with a modern font
- Neon palette (gold, green, burgundy) — preserve these colors
- Pixelated image rendering and pixelated button borders

**Do not "modernize" the design unless explicitly asked.**

---

## Git & branching

- **The default branch is `codex/create-expand-from-node-planning-documents`** — there is no
  `main` or `master`. Detect it (`git ls-remote --symref origin HEAD`), never assume.
- Branch prefixes in use: `agent/*` (agent missions), `codex/*` (executor work),
  `claude/*` (Claude Code sessions), `feat/*` (feature work).
- One concern per branch and per commit. Do not mix unrelated changes.
- PRs target the detected default branch and are opened for human review.
  **No agent merges its own PR.**
- Graph-changing PRs should link the audit document that motivated them.

---

## Security notes

- **Never commit private keys.** `GEO_PRIVATE_KEY` and similar belong in environment
  variables or Cloudflare Worker secrets only.
- **There is no `.gitignore`** — nothing protects you from accidentally staging a `.env`,
  a key, or a local scratch file. Stage explicitly; never `git add -A` blindly.
- The x402 payment wallet address (`mael-rolland.eth`) must only be changed if explicitly
  instructed.
- Graph JSON files are large (6–10 MB each). Prefer streaming/`python3 -c` inspection over
  loading them into context.

---

## Common tasks

### Adding a new page
1. Create both `page.html` and `page-fr.html`
2. Copy the `<head>` structure from `index.html`
3. Add `hreflang` links in both files
4. Add the page to `sitemap.xml`, `sitemap.html`, and `plan-du-site.html`
5. Link it from the navigation in `index.html` / `index-fr.html`

### Changing the knowledge graph
Follow [Patch → version workflow](#patch--version-workflow). In short: audit → patch payload
→ `scripts/make_v<N>_*.py` → re-audit → PR. Never edit `grc20-these-mael-rolland-v*.json`
by hand, and never overwrite an existing version.

### Publishing the graph on-chain
1. Confirm which snapshot is being published (npm scripts default to v96)
2. `node grc20-publish.mjs --input ./grc20-these-mael-rolland-v99.json --dry-run`
3. `npm run testnet` to validate on-chain
4. `npm run mainnet` (requires `GEO_PRIVATE_KEY`)
5. Update `IPFS_CID` in the Cloudflare Worker environment afterwards

### Deploying the Worker
```bash
npm run worker-dev      # http://localhost:8787
npm run worker-deploy
```

### Updating Swarm/IPFS hosting
Run `./update-swarm-urls.sh` and follow its instructions to update the ENS contenthash.

### Testing the static site locally
No build step. Serve the repository root over HTTP (the graph pages `fetch()` JSON, so
`file://` will not work):
```bash
python3 -m http.server 8000
```

---

## Thesis content (`assets/MD/`)

The Markdown files in `assets/MD/` are the full text of the PhD thesis.

- `INDEX.md` is the authoritative entry point — read it first
- French originals: `01_chapitre_I.md`, … — English translations: `01_chapitre_I_EN.md`, …
- `assets/MD/style.css` styles the `lecteur.html` reader
- The knowledge graph is *derived from* these texts: they are the evidence base against
  which every entity, relation, quote and page reference must be checked

**Do not modify thesis text unless explicitly asked** — these are archival academic documents.
When quoting, preserve French punctuation and typography exactly (`« »`, `’`, non-breaking
spaces). Never paraphrase a `SourceQuote`.

---

## Working language

The thesis, the graph descriptions, the story presets, and most audit documents are in
**French**. Code, schemas, and architecture documentation are mixed FR/EN. When producing
academic or editorial content for this project, write in French with exact citations, in a
dense, precise, non-promotional register. Code comments follow the surrounding file.

---

## What this project is not

- **Not** a React/Vue/Next.js app — do not suggest adding a framework
- **Not** server-rendered — all pages are static HTML
- **Not** an npm-based frontend build — `package.json` exists only for the Node publication
  and Worker scripts; `npm install` is not needed to work on the site
- **No test suite** — validation is `scripts/audit_graph.py`,
  `workshop/scripts/lint-workshop-artifacts.mjs`, `npm run dry-run`, and manual browser testing
- **No CI/CD** — deployments are manual
- **No `.gitignore`** — stage files explicitly
