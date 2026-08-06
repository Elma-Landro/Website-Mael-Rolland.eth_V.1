# CLAUDE.md — AI Assistant Guide for Website-Mael-Rolland.eth_V.1

This file provides context and conventions for AI assistants (Claude Code and others) working in this repository.

---

## Project Overview

Personal academic website and Web3 infrastructure for **Maël Rolland** (`mael-rolland.eth`), a PhD researcher at EHESS (École des Hautes Études en Sciences Sociales). The site presents a dissertation titled *"Au-delà des codes : infrastructure et gouvernance discrète et polycentrique des crypto-monnaies Bitcoin et Ethereum dévoilée par leurs crises"* (defended December 13, 2024, advisor: Ève Chiapello).

The project bridges traditional academic publishing with Web3-native distribution:
- Static HTML/CSS/JS frontend (no framework, no build step)
- A doctoral thesis rendered as a traceable **GRC-20 knowledge graph** (2,293 entities / 20,207 relations at v107)
- Cloudflare Worker API with x402 micro-payment support
- IPFS/Swarm decentralized hosting via ENS (`mael-rolland.eth.limo`)

There is also an applied research lab identity: **TheDyorLab** (`thedyorlab.eth`).

> **Read this first.** This repository is a *scientific object*, not a conventional web app. The graph encodes verifiable claims about a 465-page thesis. **Traceability and evidence integrity outrank speed and coverage.** Never invent entities, relations, quotes, page numbers, or chapter attributions. A smaller verified change always beats a richer speculative one.

---

## ⚠️ Critical facts to know before editing

1. **There is no `main` or `master` branch.** The default branch is
   `codex/create-expand-from-node-planning-documents`. Detect it
   (`git ls-remote --symref origin HEAD`); never hardcode `main`.
2. **The canonical graph is `grc20-these-mael-rolland-v107.json`.** Snapshots v96–v107
   are all kept in the repo; only the most recent is blocking in CI. Verify which is
   canonical before acting — this file has been out of date before.
3. **Graph files are never edited in place.** Each change produces a new
   `grc20-these-mael-rolland-v<N+1>.json` via a generator script under `scripts/`.
   See [Patch → version workflow](#patch--version-workflow).
4. **Bumping the graph version means updating every consumer.** CI checks that a
   graph's `space.version` matches its filename — it does **not** check that the site
   points at the right graph. See [Version bump checklist](#version-bump-checklist).
5. **CI exists and is dependency-free** (`.github/workflows/check.yml`): JS syntax,
   JSON validity, `check_graph_integrity.py`, `check_anchoring.py`. All four are
   replayable locally — do that before pushing.
6. **Four project skills live in `.claude/skills/`** and are meant to be invoked
   before touching the graph, the anchoring maps, or the runtime. See
   [Project skills](#project-skills).

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
├── style.css                                   # Main stylesheet
│
├── ── Graph runtime ─────────────────────────────────────────────────────
├── graphe.html                                 # Interactive knowledge-graph viewer
├── graphe.*.js                                 # 14 extracted modules (load order matters)
├── lecteur.html                                # Markdown thesis reader
├── story-presets.mjs                           # Guided "story mode" scenarios (5 stories)
├── narrative-anchors.json                      # Derived quote↔entity↔section anchors
├── narrative-anchors-build.mjs                 # Generator for narrative-anchors.json
│
├── ── Canonical graph data ──────────────────────────────────────────────
├── grc20-these-mael-rolland-v107.json          # ★ CANONICAL
├── grc20-these-mael-rolland-v96…v106.json      # Frozen snapshots, kept as history
├── entity_section_map.json                     # Entity ID → thesis subsection
├── section_entities_map.json                   # Section → entity list (lecteur.html)
├── section_overrides.json                      # Entities pinned to a section
├── patch_*.json / new_relations_patch.json     # Historical patch payloads
│
├── ── Publication / API ─────────────────────────────────────────────────
├── grc20-publish.mjs                           # GRC-20 on-chain publication pipeline
├── graph-worker.mjs                            # Cloudflare Worker graph API (x402)
├── update-swarm-urls.sh                        # Swarm/IPFS deployment helper
├── package.json                                # Node deps + npm scripts (publish only)
│
├── ── Governance & process ──────────────────────────────────────────────
├── .claude/skills/                             # ★ Four project skills (see below)
├── agents/                                     # Agent charter: roles, modes, genealogy
│   ├── README.md                               # ★ Charter — read before acting as an agent
│   ├── Agent_Creation_Rules.md
│   ├── Hermes.md                               # Orchestrator agent spec
│   └── Codex.md                                # Executor agent spec
├── .github/workflows/check.yml                 # CI: syntax, JSON, graph integrity, anchoring
│
├── ── Documentation ─────────────────────────────────────────────────────
├── docs/
│   ├── agents/                                 # Agent/skill architecture proposals
│   ├── architecture/                           # Seam plans, boundary contracts, vNext design
│   ├── audits/                                 # Dated graph audits + supporting CSV data
│   ├── research/catalogue-evenements/          # Event catalogue research (CSV + fusion.py)
│   └── grc20_*.md                              # Ontology / relations / evidence / views audits
│
├── ── Workshop (authoring & validation layer) ───────────────────────────
├── workshop/                                   # ★ Canonical lab namespace
│   ├── schemas/  templates/                    # JSON Schemas + blank templates
│   ├── claims/ evidence/ validations/          # Workshop object instances
│   ├── decisions/traces/                       # Editorial decisions with rationale
│   ├── narratives/presets/  patches/  exports/
│   ├── scripts/                                # lint-workshop-artifacts, audit-patches, dry-run
│   └── PROMOTION_WORKFLOW.md                   # How workshop objects reach public status
│
├── ── Pipelines & scaffolds ─────────────────────────────────────────────
├── scripts/                                    # Audit tooling + version generators
│   └── sourcequote-migration/                  # SourceQuote migration orchestrator
├── patches/                                    # Structured patch payloads (v97+)
├── Migration/                                  # Historical migration bundles + briefs
├── export/                                     # workshop → public-data export scaffold
├── public-data/                                # (reserved) generated public artifacts
├── schema/                                     # Pointer → docs/architecture/schema-vnext.md
├── workspace/                                  # DEPRECATED — marker only, use workshop/
│
└── assets/
    ├── MD/                                     # Full thesis text in Markdown (bilingual)
    │   ├── INDEX.md                            # ★ Agent-readable entry point
    │   ├── 00_introduction.md / _EN.md … 04_conclusion.md / _EN.md
    │   ├── 05_glossaire_annexes.md / 05_glossary_appendix_en.md
    │   ├── 06_resume.md
    │   └── style.css                           # Stylesheet for lecteur.html
    ├── Mael_Rolland_CV_Court2026.html          # Standalone HTML CV for print/PDF
    ├── img/  figures/  icons/  pdf/
```

---

## Tech Stack

### Frontend
- **Pure static HTML/CSS/JS** — no bundler, no framework, no build step
- **CSS custom properties** for theming (light/dark via `data-theme` on `<html>`)
- **Google Fonts**: "Press Start 2P" (primary), "VT323" (monospace) — retro/pixel aesthetic
- **Cytoscape 3.28 + dagre** from CDN in `graphe.html` (no npm dependency)
- **Bilingual**: every page has an EN and FR counterpart with a language switcher

### Node / infrastructure
- **Node.js ≥ 18** with ES Modules (`"type": "module"`)
- **GRC-20 protocol** (`@graphprotocol/grc-20`) for knowledge-graph publishing
- **Viem 2.x** for Ethereum/Web3 interactions
- **Cloudflare Workers** (Wrangler 3.x) for the graph API
- **x402 payment protocol** for USDC micro-payments on Base
- **IPFS** (cascading gateway fallback) and **Swarm** for decentralized hosting
- **Python 3, standard library only** for audit scripts and version generators — no external deps

### Deployment
- Primary: `https://mael-rolland.eth.limo` (ENS contenthash → IPFS/Swarm)
- Cloudflare Worker for the Graph API
- Deployment is **manual**; CI validates but never deploys

---

## Validation & CI

`.github/workflows/check.yml` runs on every push and PR. It installs nothing —
Node and Python 3 suffice. Four steps:

| Step | What it checks |
|------|----------------|
| Syntaxe JavaScript | `node --check` on `*.mjs`, `*.js`, `scripts/*.mjs`, `export/scripts/*.mjs` |
| Validité JSON | Every root `*.json`, `docs/audits/data/*.json`, `patches/*.json` parses |
| Intégrité structurelle | `scripts/check_graph_integrity.py` — duplicate IDs, broken endpoints, orphans |
| Cohérence de l'ancrage | `scripts/check_anchoring.py` — anchoring maps vs. graph |

Each check exists because of a real incident: typographic apostrophes breaking
`story-presets.mjs`, 15 truncated relation endpoints surviving five graph versions,
26 dead IDs in `section_entities_map` passing through four versions, a committed
`__pycache__`.

**Run these locally before pushing:**

```bash
python3 scripts/check_graph_integrity.py
python3 scripts/check_anchoring.py
python3 scripts/check_anchoring.py --no-baseline   # includes known debt
python3 scripts/audit_graph.py --input grc20-these-mael-rolland-v107.json
```

Two design decisions worth knowing:

- **Only the most recent graph is blocking.** Earlier snapshots are frozen; v96 still
  carries 15 broken endpoints that were fixed in v97. Failing on them would keep CI red
  for a state nobody intends to repair. They are still verified and reported.
- **`check_anchoring.py` uses a baseline.** Known, documented debt is frozen so the
  script fails only on a *regression*. That is what makes an entity merge safe: it can
  no longer break a reference silently.

There is one **deliberately retained** broken relation: `9dee2daa…`, whose `from`
(`72d182705407492c`) is a truncated ID pointing at Ostrom 1990. It has been flagged
since May 2026 and is awaiting human arbitration. It is named explicitly as a tolerance
in both the workflow and the integrity script. **Do not "fix" it** — it is evidence of
conservatism, not a defect to hide.

Still absent: no test suite, no linter, no CD.

---

## Project skills

`.claude/skills/` contains four skills, all read-only, all in French. They encode
failures that actually happened in this repository. Invoke the relevant one *before*
writing, not after.

| Skill | Invoke before |
|-------|---------------|
| `grc20-reviewer-hostile` | Any commit touching a graph file, an anchoring map, the runtime, or a `patch_NN_*.json` — and before any PR. Nine questions drawn from real incidents. Produces no fix; only looks for what would make the reasoning wrong. |
| `grc20-thesis-archivist` | Citing the thesis, measuring a section's volume, realigning a label, checking an entity description is attested. Targets a file and line range instead of mobilizing 465 pages. Never fills a gap by invention. |
| `grc20-semantic-classifier` | Creating an entity, changing a type, introducing a new type. Every decision must be backed by a thesis passage; unresolvable cases return `TOO_AMBIGUOUS` rather than being forced. |
| `grc20-visual-coherence` | Any PR touching the graph, `graphe.html`, `lecteur.html`, `story-presets.mjs`, `graphe.story-helpers.js`, or `narrative-anchors.json`. **Requires opening pages in a browser** — a static check does not see what a reader sees. |

`docs/agents/grc20-agent-skills-architecture-v1.md` records why these four exist and
why seven other candidate instances were deferred or judged already covered.

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

The four GRC-20 scripts point at the current canonical graph. Keep them in sync on
every version bump.

Scripts **not** in `package.json`, invoked directly:

```bash
python3 scripts/audit_graph.py --input <graph>          # read-only structural audit
python3 scripts/check_graph_integrity.py                # CI check, replayable
python3 scripts/check_anchoring.py [--no-baseline]      # CI check, replayable
python3 scripts/derive_section_tree.py                  # section ground truth from assets/MD/
node narrative-anchors-build.mjs --input <graph> --out ./narrative-anchors.json
node scripts/dump_story_presets.mjs                     # ES-module reader for story presets
node workshop/scripts/lint-workshop-artifacts.mjs
node workshop/scripts/audit-patches.mjs
node workshop/scripts/build-export-dry-run.mjs
node scripts/apply-sourcequote-phases.mjs [--write]
node export/scripts/export-workshop-to-public.mjs       # scaffold
```

`scripts/grc20_commun.py` holds helpers shared by the Python scripts. Note it carries
**two** normalization functions on purpose — `normalise_doux` (lowercase + straight
apostrophe) and `normalise_appariement` (also strips punctuation, normalizes spaces).
They were once the same name doing different things. Do not merge them.

---

## GRC-20 Knowledge Graph

### Current state

`grc20-these-mael-rolland-v107.json` — 2,293 entities, 20,207 relations, 55 types,
130 relation types, 274 wire ops.

Snapshots v96 through v107 are retained as frozen history. Only v107 is blocking in CI.

### Version history (recent)

| Version | Change |
|---------|--------|
| v97 | Removed 15 truncated/broken relation endpoints |
| v98 | +6 chronology events missing from v97, +25 relations |
| v99 | +37 `occurs in` relations wiring maturation-phase events |
| v100 | Renumbered chapter I sections onto the thesis's own numbering |
| v101 | Dropped 19 orphan ops |
| v102 | Restored the thesis's 8 development domains |
| v103 | Wired events to domains from the v2 catalogue |
| v104 | Added Ethereum's hard forks from the author's chronology |
| v105 | Applied the event dedup patch (marks `duplicateOf`; **merges nothing**) |
| v106 | Completed section migration for chapters II–III; all 48 table-of-contents entries in `graphe.html` now resolve |
| v107 | Wired the four chapter I sections that had stayed outside the `section of` / `has section` tree |

Older milestones: v72 added the `ThesisSection` layer (23 subsection nodes,
11,884 `appears in section` relations); v88–v90 added `appears in section` relations
for frameworks, arguments, and concepts.

### Version bump checklist

CI verifies that each graph's `space.version` matches its filename. It does **not**
verify that the site points at the right graph. When producing v`<N+1>`, update all of:

- `package.json` (four GRC-20 scripts)
- `graphe.html` (the `fetch(…)` call **and** the loading-overlay message)
- `lecteur.html` (`GRAPH_FILE`)
- `these.html` (`<link rel="alternate">` and the `knowledge-graph` meta tag)
- `graph-worker.mjs` (`GRAPH_URL_FALLBACK` comment)
- `narrative-anchors-build.mjs` (default `--input`)

Then regenerate `narrative-anchors.json` and re-run the audit and CI scripts.

### Graph JSON shape

```jsonc
{
  "space":          { "id", "name", "controller_ens", "version", "generated_at", "note" },
  "types":          [ { "id": "<32-hex>", "name": "Person", "description": { … } } ],   // 55
  "relation_types": [ { "id": "<32-hex>", "name": "cited in", … } ],                     // 130
  "entities":       [ { "id", "name", "description", "types": ["<typeId>"], "attributes": {} } ],
  "relations":      [ { "id", "type": "<relTypeId>", "from": "<entityId>", "to": "<entityId>", "attributes": [] } ],
  "ops":            [ … ]
}
```

Conventions that matter:
- Entity/type IDs are **32-char lowercase hex**; relation IDs are base58-ish 22-char strings.
- `description` and text attributes use the `{ type: "TEXT", value, options: { language } }`
  envelope — never a bare string.
- `types` is an **array** on entities (an entity may carry more than one type).
- `space.note` is an append-only changelog. Add a line for every new version.

### Entity types (55) — most populated at v107

| Type | Count |
|------|-------|
| `Reference` | 760 |
| `Concept` | 392 |
| `SourceQuote` | 245 |
| `InfrastructureEvent` | 164 |
| `AcademicWork` | 143 |
| `Person` | 138 |
| `GreyLiterature` | 87 |
| `ThesisSection` | 84 |
| `PrimarySource` | 71 |
| `CrisisEvent` | 55 |
| `IndigenousLiterature` | 53 |
| `Capability` | 38 |
| `StakeholderCategory` | 36 |

Remaining types include `ActorNonHuman`, `ActorGroup`, `Organization`, `Institution`,
`Protocol`, `TheoreticFramework`, `Argument`, `Method`, `Corpus`, `Chapter`,
`DoctoralThesis`, `CrisisPhase`, `DevelopmentPhase`, `MonetaryObject`, `NarrativeCluster`,
`GovernanceArena`, `GovernanceConflict`, `GovernanceProcess`, `ProtocolChange`,
`ProtocolProposal`, `InfrastructureDomain`, `InfrastructureSegment`, `PriceSeries`,
`PriceWindow`, `SoftwareClient`, `CodeRepository`, `SmartContract`, `PlatformService`,
`MediaOutlet`, `Marketplace`, `HardwareDevice`, `AnalyticClaim`, `NativeFormula`.

> **Ontology debt** — near-duplicate pairs survive from earlier migrations:
> `Institution`/`Organization`, `CoreConcept`/`ConceptCore`,
> `SecondaryConcept`/`ConceptSecondary`, `TechnicalConcept`/`ConceptTechnical`,
> `ChapterSection`/`ThesisSection`. Three types are unused:
> `InfrastructureService`, `ConceptCore`, `ConceptSecondary`.
> **Do not merge or delete these on your own initiative** — type consolidation is a
> scientific decision reserved for the author. See `docs/grc20_ontology_audit.md`.

### Relation types (130) — most used

| Relation | Count |
|----------|-------|
| `appears in section` | 12,422 |
| `cited in` | 2,690 |
| `quote supports` | 392 |
| `part of` | 383 |
| `source of` | 368 |
| `belongs to domain` | 358 |
| `contributes to` | 332 |
| `applied to` | 321 |
| `has concept` | 307 |
| `occurs in` | 207 |

`appears in section` dominates (~61% of edges). Audit scripts flag entities connected
*only* by `appears in section` as "pseudo-orphans" — structurally present but
analytically unanchored.

### The anchoring layer

Four artifacts describe where entities sit in the thesis. Each is defensible in
isolation; `check_anchoring.py` is what verifies them **against each other and against
the graph**:

| File | Purpose |
|------|---------|
| `entity_section_map.json` | Entity ID → sections (+ excerpts) |
| `section_entities_map.json` | Section → entity list (consumed by `lecteur.html`) |
| `section_overrides.json` | Entities pinned to a section |
| `narrative-anchors.json` | Staged quotations (derived, regenerate — don't hand-edit) |

`story-presets.mjs` references entities **by name, not by ID**, so renaming an entity
can silently break a story. `check_anchoring.py` covers this via an alias table, and
delegates parsing to `scripts/dump_story_presets.mjs` rather than regex — French
typographic apostrophes defeat regex extraction.

`scripts/derive_section_tree.py` derives the canonical section tree from `assets/MD/`.
The thesis numbers its own sections, and the canonical heading level is `##`, not `###`.
Use it as ground truth before any renumbering.

---

## Patch → version workflow

Graph changes follow a strict, reproducible, append-only pipeline. **The active graph
file is never mutated in place.**

1. **Audit** — produce a Markdown report under `docs/audits/`, CSVs in
   `docs/audits/data/`. Read-only. `python3 scripts/audit_graph.py` gives the
   deterministic baseline (exit 0 = clean, 1 = critical, 2 = fatal).
2. **Author a patch payload** — `patch_<N>_<slug>.json` at root (or `patches/` for
   v97+). Carries a `_meta` block plus operations (`new_relations`, added entities…).
3. **Write a generator script** — `scripts/make_v<N>_<slug>.py` (Python 3, stdlib only)
   reading `v<N-1>.json` + patch, writing `v<N>.json`. Generators must:
   - default their `--source` / `--patch` / `--target` paths,
   - support `--dry-run`,
   - **validate before writing** and fail loudly rather than emit a doubtful graph,
   - append a summary line to `space.note` and bump `space.version`.
4. **Re-audit**, run the CI scripts locally, update every consumer
   ([checklist](#version-bump-checklist)), regenerate `narrative-anchors.json`.
5. **Open a PR** for human review. No agent merges its own PR.

Reference implementations: `make_v97_remove_truncated_broken_relations.py`,
`make_v100_section_migration.py`, `make_v105_dedup_events.py`,
`make_v107_wire_chapter_I_tree.py`.

Note how v105 handled duplicates: it **marks** `duplicateOf` and merges nothing.
Merging entities is an arbitration reserved for the author.

Root patch payloads (`patch_1a` … `patch_12`, `patch_batch1-3`,
`new_relations_patch.json`) are **historical artifacts** recording how earlier versions
were produced. They are not re-applied automatically.

---

## Graph runtime architecture (`graphe.html`)

`graphe.html` is a client-side Cytoscape visualization. Pure/stateful logic is being
extracted into sibling `graphe.*.js` files, each an IIFE attaching a namespace to
`window`.

**Load order matters** — these are plain `<script>` tags, not modules, so dependencies
resolve by ordering:

```
graphe.helpers.js          → GrapheHelpers    (escHtml, generateId, normalizeRelationName…)
graphe.event-bus.js        → GrapheEventBus   (on/emit — the seam between runtime layers)
graphe.story-helpers.js    → story step/scene resolution
graphe.state.js            → GrapheState      (data, undo stack, outgoing/incoming indexes)
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

`story-presets.mjs` is **lazy-imported** as an ES module at runtime, separate from the
classic-script chain.

### Extraction conventions

Modularization is deliberately incremental and reversible:
- Each extracted module must be **behavior-preserving** — same API contract as the
  inlined code.
- Cross-layer calls go through `GrapheEventBus` where a seam exists
  (e.g. `layout:apply-requested`), with an inline fallback for the un-migrated path.
- Every seam extraction is documented in `docs/architecture/` as a
  *cross-call audit* → *seam plan* → *validation result* triple. Read the relevant
  `STORY_*` / `GRAPH_*` docs before moving code across a boundary.
- `docs/architecture/STORY_EXPAND_CONTRACT_FREEZE.md` records frozen contracts — do not
  change those signatures.

### Layouts and story mode

Three named layouts: `matrice` (chapter × type grid with canvas halos), `monetisation`,
`qui-gouverne`. Story presets bind to a layout via `layoutTarget`; switching story
auto-switches layout.

`story-presets.mjs` defines five guided stories: `monetisation-cryptos`,
`qui-gouverne-reellement`, `crises`, `structure-these`, `fil-de-preuves`. Each has
ordered `steps` with `centralNode`, `focusNodes`, `cameraPreset`, `bridgeEntityIds`,
and reveal options (`edgeMode`, `maxAutoEdges`, `hideBackbone`…). Story text is
**French** editorial content — treat it like thesis prose, not UI copy.

The file uses French typographic apostrophes inside single-quoted JS strings; this has
broken syntax twice. `node --check story-presets.mjs` before committing.

### Narrative anchors

`narrative-anchors-build.mjs` derives `narrative-anchors.json` (115 anchors at v107) by
joining: a `SourceQuote` → the entities it supports (`quote supports`) → the section it
appears in (`appears in section`) → a graph scene definition. Consumed by `lecteur.html`
(quote panel) and `graphe.html` (scrollytelling anchors), and referenceable by ID from
`story-presets.mjs`.

**Regenerate it whenever SourceQuote or section relations change.**

---

## Agent governance model

`agents/README.md` is a binding charter for any automated contributor, including Claude.
Read it before making changes.

**Three modes of intervention** — when the mode is ambiguous, **default to Mode A**:

| Mode | Name | Does | Does not |
|------|------|------|----------|
| **A** | Audit | Reads, inspects, compares graph claims to thesis evidence, writes a Markdown report | Modifies nothing |
| **B** | Proposal | Proposes changes with evidence, risks, expected impact | Modifies no files |
| **C** | Patch / PR | Branches, applies minimal verified changes, validates, writes a changelog, opens a PR | Never overwrites the active graph file; never merges without human review |

**Authority model** — Maël Rolland is the final scientific arbiter. He alone authorises
schema changes, entity merges, deletions, and ID renames.

**Rule 1 — no agent without observed pain.** An agent or skill exists to address a
recurring, *measured* need, not an ideal org chart. This is why only four skills exist.

**Rule 2 — proposal ≠ application.** An agent may propose a change to its own spec;
it may never apply it.

**Rule 3 — data is not fact.** Output produced by one agent and consumed by another
stays **annotated as data** until a human validates it. Do not let an unverified
conclusion silently become a premise.

**Rule 4 — genealogy is mandatory.** Every agent file records *why* it exists.

Two agents are active: **Hermes** (orchestrator) and **Codex** (executor).

---

## Workshop layer

`workshop/` is the canonical namespace for authoring and validation work that is **not
yet public**. Public static pages must **not** depend on it.

Object families, each with a JSON Schema in `workshop/schemas/` and a blank template in
`workshop/templates/`: `SourceQuote` (evidence), `Claim`, `ValidationEvent`,
`DecisionTrace`, `NarrativePreset` / `NarrativeStep`.

**Status vocabulary** (defined in `workshop/PROMOTION_WORKFLOW.md`, gated in
`workshop/exports/export-policy.json`, shape in `workshop/schemas/status-model.json`):
`raw` → `extracted` → `linked` → `needs_review` → `validated` → `published`.

**Promotion is not automated in this phase.** No workshop script writes back into
canonical graph files; dry-run classifications are advisory only. Evidence↔claim linkage
is expressed by object-level ID references (`claim.linkedEvidenceIds`,
`sourceQuote.linkedClaimIds`), not by canonical graph relations.

Some workshop sample objects still reference v96 as their provenance baseline — that is
historical provenance, not a stale pointer.

`export/scripts/export-workshop-to-public.mjs` is the scaffold for the future
workshop → `public-data/` export. `public-data/` is empty by design.

`workspace/` is **deprecated** — a marker directory only. See
`docs/architecture/STRUCTURE_CONSOLIDATION.md`.

---

## Key source files

### `grc20-publish.mjs` — publication pipeline

| Flag | Description |
|------|-------------|
| `--input <file>` | Path to GRC-20 JSON snapshot |
| `--private-key <key>` | Ethereum private key (prefer the env var) |
| `--network TESTNET\|MAINNET` | Target network |
| `--dry-run` | Validate without publishing |
| `--create-space` | Create a new GRC-20 space |
| `--batch-size <n>` | Ops per IPFS edit (default: 200) |
| `--author <ens>` | ENS address for authorship |

Environment variables (preferred over CLI flags): `GEO_PRIVATE_KEY` (**never commit**),
`GEO_SPACE_ID`, `GEO_NETWORK`, `GEO_INPUT`, `GEO_AUTHOR`.

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
`narrative-anchors.json` in parallel, then renders the Markdown chapters from
`assets/MD/` with an entity side-panel and local annotation export.

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

1. **`<head>`**: `charset="UTF-8"`, responsive viewport, SEO `<meta>` description,
   Open Graph + Twitter Card tags, `hreflang` links for the EN/FR counterpart,
   DNS prefetch, CSS `<link rel="preload">` before the stylesheet, Google Fonts preload.
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

- **The default branch is `codex/create-expand-from-node-planning-documents`** — there is
  no `main` or `master`. Detect it, never assume.
- Branch prefixes: `agent/*` (agent missions), `codex/*` (executor work),
  `claude/*` (Claude Code sessions), `feat/*` (feature work).
- One concern per branch and per commit. Do not mix unrelated changes.
- PRs target the detected default branch and are opened for human review.
  **No agent merges its own PR.**
- Graph-changing PRs should link the audit document that motivated them.
- The branch moves fast. **Re-check the canonical graph version and the base branch
  before starting work** — several snapshots can land between two sessions.

---

## Security notes

- **Never commit private keys.** `GEO_PRIVATE_KEY` and similar belong in environment
  variables or Cloudflare Worker secrets only.
- `.gitignore` covers `.env`, `.env.*`, `*.pem`, `*.key`, `id_rsa*`, publication
  artifacts (`*.ops.json`, `*.manifest.json`, `*.published.json`), `__pycache__/`, and
  `node_modules/`. It is a safety net, not a substitute for staging explicitly.
- The x402 payment wallet address (`mael-rolland.eth`) must only be changed if
  explicitly instructed.
- Graph JSON files are large (6–10 MB each). Prefer streaming / `python3 -c` inspection
  over loading them into context.

---

## Common tasks

### Adding a new page
1. Create both `page.html` and `page-fr.html`
2. Copy the `<head>` structure from `index.html`
3. Add `hreflang` links in both files
4. Add the page to `sitemap.xml`, `sitemap.html`, and `plan-du-site.html`
5. Link it from the navigation in `index.html` / `index-fr.html`

### Changing the knowledge graph
Follow [Patch → version workflow](#patch--version-workflow): audit → patch payload →
`scripts/make_v<N>_*.py` → re-audit → update every consumer → regenerate anchors → PR.
Never edit a `grc20-these-mael-rolland-v*.json` by hand, and never overwrite an existing
version.

### Publishing the graph on-chain
1. Confirm which snapshot is canonical
2. `node grc20-publish.mjs --input ./grc20-these-mael-rolland-v107.json --dry-run`
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
The `grc20-visual-coherence` skill documents the full local test procedure, including
what to do when the CDN is blocked.

---

## Thesis content (`assets/MD/`)

The Markdown files in `assets/MD/` are the full text of the PhD thesis.

- `INDEX.md` is the authoritative entry point — read it first
- French originals: `01_chapitre_I.md`, … — English translations: `01_chapitre_I_EN.md`, …
- `assets/MD/style.css` styles the `lecteur.html` reader
- The knowledge graph is *derived from* these texts: they are the evidence base against
  which every entity, relation, quote and page reference must be checked
- When measuring a section's volume, count body and footnotes **separately**

**Do not modify thesis text unless explicitly asked** — these are archival academic
documents. When quoting, preserve French punctuation and typography exactly
(`« »`, `’`, non-breaking spaces). Never paraphrase a `SourceQuote`.

---

## Working language

The thesis, graph descriptions, story presets, skills, and most audit documents are in
**French**. Code, schemas, and architecture documentation are mixed FR/EN. When producing
academic or editorial content, write in French with exact citations, in a dense, precise,
non-promotional register. Code comments follow the surrounding file.

---

## What this project is not

- **Not** a React/Vue/Next.js app — do not suggest adding a framework
- **Not** server-rendered — all pages are static HTML
- **Not** an npm-based frontend build — `package.json` exists only for the Node
  publication and Worker scripts; `npm install` is not needed to work on the site
- **No test suite and no linter** — validation is the CI scripts above, plus manual
  browser testing
- **No CD** — CI validates, deployments are manual
