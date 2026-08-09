# CLAUDE.md — AI Assistant Guide for Website-Mael-Rolland.eth_V.1

This file provides context and conventions for AI assistants (Claude Code and others) working in this repository.

---

## Project Overview

Personal academic website and Web3 infrastructure for **Maël Rolland** (`mael-rolland.eth`), a PhD researcher at EHESS (École des Hautes Études en Sciences Sociales). The site presents a dissertation titled *"Au-delà des codes : infrastructure et gouvernance discrète et polycentrique des crypto-monnaies Bitcoin et Ethereum dévoilée par leurs crises"* (defended December 13, 2024, advisor: Ève Chiapello).

The project uniquely bridges traditional academic publishing with Web3-native distribution:
- Static HTML/CSS/JS frontend (no framework)
- On-chain knowledge graph publication via GRC-20 protocol
- Cloudflare Worker API with x402 micro-payment support
- IPFS/Swarm decentralized hosting via ENS (`mael-rolland.eth.limo`)

There is also an applied research lab identity: **TheDyorLab** (`thedyorlab.eth`).

---

## Repository Structure

```
/
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
├── atelier.html / workshop.html
├── rare-pepe.html / rare-pepe-fr.html
├── graphe.html                                 # Interactive GRC-20 knowledge graph (matrix viz)
├── lecteur.html                                # Markdown thesis reader
├── 404.html / 404-fr.html
├── sitemap.html / plan-du-site.html
│
├── style.css                                   # Main stylesheet (1,515 lines)
├── grc20-publish.mjs                           # GRC-20 publication pipeline (Node.js ES module)
├── graph-worker.mjs                            # Cloudflare Worker API (Node.js ES module)
│
├── sections.helpers.js                         # Shared section-tree helpers (graphe.html + lecteur.html)
│
├── grc20-these-mael-rolland-v112.json          # Current authoritative knowledge graph (canonical)
├── grc20-properties-registry-v1.json           # Attribute-key registry — CI invariant, GENERATED
│
├── entity_section_map.json                     # Entity ID → thesis subsection mapping
├── section_entities_map.json                   # Thesis section → entity list mapping (+ anchoring fields)
├── section_overrides.json                      # Manual overrides for section assignments
├── section-headings-map.json                   # Heading line → section key (positional resolution)
│
├── new_relations_patch.json                    # v72 lot: 11,884 appears_in_section (historical)
├── patch_1a … patch_3a_*.json                  # Historical patches, integrated (see Patch Files)
├── patch_10 … patch_19_*.json                  # Patches applied by their make_vNNN script
├── patch_candidate_bibliographie_*.json        # 3 CANDIDATES — NOT APPLIED, awaiting arbitration
│
├── anomalies_report.md                         # Entity/section mapping QA report (v71 base)
├── package.json                                # Node.js dependencies + npm scripts
├── update-swarm-urls.sh                        # Swarm/IPFS deployment helper
├── sitemap.xml
├── LICENSE                                     # Apache-2.0
├── README.md
├── favicon_32x32.png / favicon_16x16.png
├── placeholder.svg
│
├── .github/workflows/check.yml                 # CI: 8 steps, no install (Node + Python 3 only)
├── agents/                                     # Agent charter and roles (README.md = the rules)
├── .claude/skills/                             # Invocable skills (hostile review, archivist, …)
├── scripts/                                    # 46 files — see "Scripts and controls" below
├── patches/                                    # Receipts + archive/ (retired patches, with motive)
├── Migration/                                  # External SourceQuote bundles (zips, NOT applied)
├── docs/audits/                                # 27 audit reports — the repo's memory
│   └── data/                                   # 26 evidence files (CSV/JSON) — read with their audit
└── assets/
    ├── MD/                                     # Thesis chapters in Markdown (bilingual FR/EN)
    │   ├── INDEX.md                            # Agent-readable entry point for thesis content
    │   ├── style.css                           # Stylesheet for lecteur.html reader
    │   ├── 00_introduction.md / 00_introduction_EN.md
    │   ├── 01_chapitre_I.md / 01_chapitre_I_EN.md
    │   ├── 02_chapitre_II.md / 02_chapitre_II_EN.md
    │   ├── 03_chapitre_III.md / 03_chapitre_III_EN.md
    │   ├── 04_conclusion.md / 04_conclusion_EN.md
    │   ├── 05_glossaire_annexes.md / 05_glossary_appendix_en.md
    │   ├── 06_resume.md
    │   └── 07_bibliographie.md                 # 664 entries converted from the PDF (2026-08)
    ├── Mael_Rolland_CV_Court2026.html          # Standalone HTML CV for print/PDF export
    ├── img/                                    # Photos and images
    ├── figures/                                # Research diagrams and visualizations
    ├── icons/                                  # Social media and UI icons (20 files)
    └── pdf/                                    # Thesis PDFs and related documents
```

---

## Tech Stack

### Frontend
- **Pure static HTML/CSS/JS** — no build system, no bundler, no framework (React/Vue/etc.)
- **CSS custom properties** for theming (light/dark mode via JS toggle)
- **Google Fonts**: "Press Start 2P" (primary), "VT323" (monospace secondary) — retro/pixelated aesthetic
- **Bilingual**: Every page has an EN and FR counterpart with language switcher links

### Backend / Infrastructure
- **Node.js ≥ 18** with ES Modules (`"type": "module"`)
- **GRC-20 protocol** (`@graphprotocol/grc-20`) for knowledge graph publishing
- **Viem 2.x** for Ethereum/Web3 interactions
- **Cloudflare Workers** (via Wrangler 3.x) for the graph API
- **x402 payment protocol** for USDC micro-payments on Base network
- **IPFS** for decentralized storage (cascading gateway fallback)
- **Swarm** as alternative decentralized hosting

### Deployment
- Primary: `https://mael-rolland.eth.limo` (ENS contenthash → IPFS/Swarm)
- Cloudflare Worker for the Graph API

---

## npm Scripts

```bash
npm run dry-run          # Test GRC-20 pipeline locally (no on-chain writes)
npm run testnet          # Publish to GRC-20 testnet
npm run mainnet          # Publish to GRC-20 mainnet (requires GEO_PRIVATE_KEY)
npm run new-space        # Create new GRC-20 space on testnet
npm run worker-dev       # Local dev server for Cloudflare Worker
npm run worker-deploy    # Deploy Worker to Cloudflare
```

> **Note**: `package.json` scripts reference the current canonical graph. When publishing a new snapshot, increment the filename **and** update `package.json`, `these.html`, `graphe.html`, `lecteur.html`, `graph-worker.mjs`, `narrative-anchors-build.mjs` — `scripts/check_graph_integrity.py` verifies that each graph's `space.version` matches its filename, but not that the site points at the right one.

---

## Key Source Files

### `grc20-publish.mjs` — Knowledge Graph Pipeline

Converts the JSON snapshot to GRC-20 wire format and publishes it on-chain.

**CLI flags:**
| Flag | Description |
|------|-------------|
| `--input <file>` | Path to GRC-20 JSON snapshot |
| `--private-key <key>` | Ethereum private key (prefer env var) |
| `--network TESTNET\|MAINNET` | Target network |
| `--dry-run` | Validate without publishing |
| `--create-space` | Create a new GRC-20 space |
| `--batch-size <n>` | Ops per IPFS edit (default: 200) |
| `--author <ens>` | ENS address for authorship |

**Environment variables (preferred over CLI flags):**
```
GEO_PRIVATE_KEY     # Ethereum private key — NEVER commit this
GEO_SPACE_ID        # Target GRC-20 space
GEO_NETWORK         # TESTNET or MAINNET
GEO_INPUT           # Path to input JSON
GEO_AUTHOR          # ENS address
```

### `graph-worker.mjs` — Cloudflare Worker API

Serves the GRC-20 knowledge graph over HTTP with optional x402 payment gating.

**Endpoints:**
| Path | Description |
|------|-------------|
| `GET /` | Graph metadata + navigation links |
| `GET /graph` | Full GRC-20 graph (paginated) |
| `GET /graph?entity=<id>` | Single entity + neighborhood |
| `GET /graph?type=<name>` | All entities of a type |
| `GET /graph?search=<query>` | Full-text search on entity names |
| `GET /graph?depth=<n>` | Control neighborhood depth (max 3) |
| `GET /stats` | Public graph statistics (free) |
| `GET /types` | Public entity type list (free) |

**Environment variables:**
```
IPFS_CID              # IPFS hash of the published graph
WALLET_ADDRESS        # Payment recipient (mael-rolland.eth)
PRICE_USDC            # Per-request price (default: 0.001)
GRAPH_URL_FALLBACK    # Fallback URL if IPFS unavailable
MODE                  # "free" | "x402" | "x402-optional"
```

### `style.css` — Design System

CSS custom properties define the design tokens:

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

Image rendering uses `image-rendering: pixelated` for the retro aesthetic.

### `graphe.html` — Interactive Knowledge Graph Viewer

A fully client-side force-directed + matrix visualization of the GRC-20 knowledge graph. Significant features:

- **Matrix layout**: Entities arranged in a chapter×type grid with canvas-based halos per cell
- **Vertical column halos**: Type-colored glowing backgrounds for each entity category column
- **Chapter-row halos**: Canvas overlays for each thesis chapter row
- **Node sizing**: Proportional on mobile, adaptive zoom-based label reveal (threshold ≥ 1.8×)
- **Label coloring**: By entity type, matching column halo colors
- Fetches graph data from the Cloudflare Worker API or local JSON fallback
- Its counters come from **relations**, not from `occurrence_count` — the
  anchoring-weight debt does not affect this page

### `lecteur.html` — Markdown thesis reader

Scrollytelling reader: renders the thesis Markdown, highlights entity mentions,
and drives a contextual graph panel per section.

- **Panel ranking**: pinned entities from `section_overrides.json` first, then
  a top-12 by `occurrence_count × log(N/df)`. **Parent sections are aggregated**
  (ten keys, `conclu_theo` included — it exists only as an aggregate), and the
  canonical sort is *stable with no tie-break*. Any simulation of this panel
  must reproduce both, or it is not simulating the site.
- **Positional heading resolution** via `section-headings-map.json`, with
  `sections.helpers.js` shared with `graphe.html`.
- **`?panelLab=1`** — opt-in laboratory mode: banner, `snippet_status` /
  `direct_anchor_count` badges, and a selector comparing four ranking policies.
  **Inert without the parameter**; the choice is never persisted. Do not let it
  leak into the public default.

---

## GRC-20 Knowledge Graph

The file `grc20-these-mael-rolland-v112.json` is the current authoritative knowledge graph (v112, 2,293 entities, 20,207 relations). Snapshots v96 through v112 are kept in the repo; only the most recent is blocking in CI.

### Entity Types (v112 — 55 types)

| Type | Description |
|------|-------------|
| `AcademicWork` | Thesis, papers, books |
| `Person` | Researchers, developers, authors |
| `Institution` | Universities, foundations, organizations |
| `Concept` | Theoretical and empirical concepts |
| `TheoreticFramework` | Analytical frameworks (institutionalism, STS) |
| `CrisisEvent` | Bitcoin CVE 2018, Ethereum DAO hard fork |
| `Protocol` | Bitcoin, Ethereum, and related protocols |
| `ActorNonHuman` | Software, repositories, smart contracts |
| `ActorGroup` | Mining pools, exchanges, collectives |
| `GreyLiterature` | Non-academic sources |
| `IndigenousLiterature` | Community-originated sources |
| `ThesisSection` | Navigable subsections (I.1.1–III.3.4) |
| `Reference` | Bibliographic references (deduplicated) |
| `SourceQuote` | Verbatim PDF quotations with pagination |
| `GovernanceArena` | Forums, GitHub repos, governance venues |
| `GovernanceConflict` | Documented governance disputes |
| `GovernanceProcess` | Decision-making processes |
| `InfrastructureEvent` | Key infrastructure milestones |
| `InfrastructureDomain` | Infrastructure domains (layer 1/2, etc.) |
| `InfrastructureSegment` | Sub-segments within infrastructure |
| `Method` | Research methods used |
| `Corpus` | Data corpora (on-chain, quantitative) |
| `DoctoralThesis` | The thesis itself as an entity |
| `StakeholderCategory` | Categories of actors |
| `Argument` | Central arguments of the thesis |
| `Capability` | Protocol capabilities |
| `Chapter` | Thesis chapters as entities |
| `CrisisPhase` | Sub-phases of crisis events |
| `DevelopmentPhase` | Development history phases |
| `MonetaryObject` | Monetary instruments |
| `NarrativeCluster` | Narrative groupings |
| `PriceSeries` / `PriceWindow` | Quantitative price data |
| `PrimarySource` | Primary source documents |
| `ProtocolChange` / `ProtocolProposal` | Protocol evolution events |

### Knowledge Graph Versioning

The graph has evolved across 112 versions. Key milestones: v72 added the `ThesisSection` layer (23 subsection nodes, 11,884 `appears_in_section` relations); v88–v90 added `appears_in_section` relations for frameworks, arguments, and concepts; v97 repaired 15 truncated relation endpoints; v98–v99 added missing chronology events and wired the maturation phase; v100 renumbered the chapter I sections onto the thesis's own numbering; v101 dropped 19 orphan ops; v102 restored the thesis's 8 development domains; v103 wired events to domains from the v2 catalogue; v104 added Ethereum's hard forks; v105 applied the event dedup patch; v106 completed the section migration for chapters II and III (13 renumbered, 11 created), after which all 48 table-of-contents entries in `graphe.html` resolve to a graph node. v107 wired the four chapter I sections that had stayed outside the `section of` / `has section` tree. v108 realigned 3,970 `section_key` attributes carried by `appears in section` relations, which still named the pre-migration key of their own target. v109 (« voie C ») rewired 3,970 of those relations to the section whose text their anchoring charge actually describes — 18 keys had been shifted one block over by the v100/v106 migrations, which made 8 table-of-contents entries look empty while their content sat under the neighbour's key. v110 corrected one bibliographic typo (Danezis), retyped 21 bibliography-confirmed author cards from Reference to Person, and applied 384 mechanical attribute normalisations described by `grc20-properties-registry-v1.json` — now a CI invariant. v111 repaired 16 `page_start` attributes on section nodes:
they were not wrong but **stale** — no `page_start` had been touched since v96,
so the v100/v106 renumberings changed which section a node designated while its
page stayed glued to the node. Each of the 16 declared values proved to be the
printed page of the key that node carried in v96. Corroboration: the anchoring
map already held the corrected value wherever it had one (graph/map agreement
went from 20/23 to 23/23). v112 applied the minimal chronology patch from the
Chronology, Dates & References Lab (PR #118): exactly **two** `date` values —
Heartbleed `04/07/2014` → `2014-04-07` (the graph's only MM/DD reading against
26 decidable DD/MM values out of 26) and BitcoinTalk `2010-11-22` →
`2009-11-22` (a year typo its own description contradicted). Nothing else
moved: entity and relation counts, entity identifiers, `types`,
`relation_types`, `relations`, `ops` and the full set of attribute keys are
all unchanged, and so is every other field of every entity — the two date
values above are the only differences, with `space.version` and `space.note`
updated as the version record requires.
The probable BitcoinTalk duplicate stays a **debt** — no `duplicateOf` was
written, because the corrected card is the better-connected of the two
(degree 24 against 22) and naming a canonical remains the author's call.
**v112 is the current canonical snapshot.**

### Patch Files

**32 patch artefacts have been inventoried empirically** against v110
(`docs/audits/data/candidate-patch-inventory-v1.csv`, each line carrying its
proof of application or non-application). The inventory predates v111 and has
not been regenerated since: `patch_candidate_section_page_start_v1.json`,
applied by `make_v111`, is a 33rd, and
`patch_candidate_chronology_dates_v1.json`, applied by `make_v112`, a 34th.

**Both of those still carry the `CANDIDATE — NOT APPLIED` policy even though
they were applied.** That is the repo convention, not an oversight — check C03
of `preflight_candidate_patches.py` requires the string, and the applicators
refuse a patch that lacks it. But nothing yet records *that they were
applied*: read the inventory as a snapshot of v110, never as the current
state. Three statuses:

| Status | Count | What it means |
|---|---:|---|
| `applique` | 11 | A `make_vNNN` script applied it; effects verified one by one in v110 (`patch_10` … `patch_19`) |
| `historique` | 14 | Integrated long ago, mostly without a traceability script (`patch_1a`–`patch_3a`, `new_relations_patch.json`) — some target IDs are now dead, so a naive replay would fail |
| `candidat-non-applique` | 7 | The 3 `patch_candidate_bibliographie_*.json`, the 3 `Migration/` SourceQuote zips, and `patches/archive/grc20_anchor_overrides_targeted.json` |

**Six incompatible dialects** coexist in that history (three of them for
`ADD_RELATION` alone). Any *new* candidate patch must follow
`docs/audits/grc20-candidate-patch-contract-v1.md`: envelope `_meta` + `ops`,
the `patch_18`/`19` dialect (`type` / `entityId` / `attributeId`, values as
`{type, value}`), declared counts that can be recomputed, motivated `skipped`,
and — for a candidate — `_meta.policy` starting with the exact string
`CANDIDATE — NOT APPLIED — AUTHOR ARBITRATION REQUIRED`.

Three interdictions for candidates: never self-apply, never mix dialects,
never pre-assign an `entityId` on `CREATE_ENTITY` (no applicator consumes
that op type yet). **Historical patches are archives — do not rewrite them**,
it would falsify the record.

Validate any candidate with `python3 scripts/preflight_candidate_patches.py`
(12 checks, non-zero exit on a blocker; also wired into CI).

### Mapping Files

| File | Purpose |
|------|---------|
| `entity_section_map.json` | Maps entity IDs to their thesis subsections (20,056 snippets) |
| `section_entities_map.json` | Maps section IDs to their entity lists — plus `snippet_status` and `direct_anchor_count` on each of its 12,374 lines |
| `section_overrides.json` | Manual overrides for ambiguous assignments (pinned entities, always first in a panel) |
| `section-headings-map.json` | Heading line → section key; drives `lecteur.html`'s positional resolution and the anchoring-weight ranges |

**Reading `occurrence_count` honestly.** It is a *record count* from proxy
keyword matching, not a measure of importance: **80 % of the map's lines
(9,899/12,374) are `proxy`** — snippets exist but carry neither the entity's
name nor its citation base. Since the anchoring-weight work, every line also
carries `snippet_status` (`self` / `self-base` / `proxy` / `no-snippet`) and
`direct_anchor_count` (literal word-boundary count, `null` where the text
range is underivable). **Never read `direct_anchor_count` alone** — it is a
poor measure that under-counts forged, translated or bilingual names; and
`snippet_status` is evidence, not a certificate. Cross them, always
(`docs/audits/grc20-poids-ancrage-v2.md`).

### Work that deliberately did NOT bump the graph

Several chantiers landed between v110 and v111 **without producing a version**,
by design. Knowing this prevents both "why isn't this in the graph?" and the
temptation to bump a version to make something fit:

- **Anchoring qualification** — `snippet_status` / `direct_anchor_count` live
  in `section_entities_map.json`, *not* in the graph. Patching the graph would
  have **imported the proxy debt into it** instead of repairing it.
- **Panel Policy Lab** — five display policies for the reader's panels were
  measured (`docs/audits/grc20-panel-policy-lab-v1.md`); **the public ranking
  did not change**. A `?panelLab=1` opt-in mode in `lecteur.html` lets the
  author try them; it is inert without the parameter.
- **Bibliography Reconciliation Lab** — 22 doubtful author cards, 89 duplicate
  families, 60 PDF entries without a node and 11 "never cited" nodes were
  instructed to the point of decision, and materialised as **three candidate
  patches, none applied**.
- **Candidate Patch Preflight Lab** — inventory, contract, validator and a
  memory-only simulation; no patch applied, no graph written.
- **SourceQuote Migration Verification Lab** — the 41 ops of the `Migration/`
  zips verified line by line against the thesis PDFs. All 41 quotes exist in
  the thesis, but 18 cut text without marking it, 7 are mis-attached, 6
  duplicate an existing `SourceQuote`. **Frozen**: nothing may be engraved
  before the incoherent `page_start` attributes are repaired (author's
  arbitration).

**A standing trap** — three section keys (`II.3.1`, `II.3.2`, `III.2.2`) still
exist in v111 but designate *different* sections since the v106 migration. A
patch that resolves sections by raw key anchors silently to the wrong place.
The renumbering map is not reliable either: on four verified cases the printed
text proved the raw key right and the map wrong. **Only the thesis text
settles it.**

**Another one** — the graph carries 115 `nameEn`, 77 `labelEn`, 70 `labelFr`
and 30 `aliases`. A resolver that queries only `name` produces false negatives:
an external patch declared "Polycentric Governance" absent while `a444085b`
carries exactly that string in its `nameEn`. **Query `name`, `nameEn`,
`labelEn`, `labelFr` and `aliases` — all of them — before concluding an entity
is missing**; that is the order `scripts/resolve_entity_names.py` implements.
`docs/audits/data/entity-alias-table-v1.csv` covers what the graph does *not*
declare (and an alias table is never an authorisation to merge).

### Anomalies Report

`anomalies_report.md` (generated 2026-03-15, based on v71): documents 1,026 entities without MD occurrences, entities cited in wrong chapters, and multi-chapter entities with incomplete `cited_in` relations. Use as a QA reference when updating the graph.

---

## HTML Page Conventions

Every HTML page follows this pattern:

1. **`<head>`** includes:
   - `charset="UTF-8"` and responsive `viewport`
   - SEO: `<meta>` description, Open Graph, Twitter Card tags
   - `hreflang` links for EN/FR counterparts
   - DNS prefetch for external domains
   - CSS `<link rel="preload">` before `<link rel="stylesheet">`
   - Google Fonts preload

2. **`<body>`** includes:
   - Theme toggle button (fixed, top-right): toggles `data-theme="dark"` on `<html>`
   - Language switcher link (EN ↔ FR)
   - Main content
   - Social icon links section (consistent across pages)

3. **Structured data**: JSON-LD with `schema.org/Person` on the landing page.

4. **Forms**: Use [FormSubmit.co](https://formsubmit.co) (no backend required).

---

## Bilingual Convention

- English pages: `page.html`
- French pages: `page-fr.html`
- Each page links to its counterpart via a language switcher
- Both versions are maintained in sync — **always update both when editing content**
- Assets (PDFs, images) are shared between languages

---

## Design Aesthetic

This site uses an intentional retro/pixel-art style:
- Font: "Press Start 2P" (8-bit arcade font) — do not replace with a modern font
- Neon color palette (gold, green, burgundy) — preserve these colors
- Pixelated image rendering — intentional, not a bug
- Button styles use `image-rendering: pixelated` borders

Do not "modernize" the design unless explicitly asked.

---

## Working discipline (read this before touching the graph)

The charter is `agents/README.md`. Its rules are not decoration — each one
comes from a real incident in this repository.

**An agent is a work role, not a scientific authority.** Type changes, entity
merges, node creation, semantics of `appears in section`, and anything that
would engrave a claim about a person are **the author's decisions**. Instruct
them to the point where only a decision remains, then stop and ask. Put the
question to Maël directly — context, options, effects, an optional clearly
separated recommendation, and a closed question — rather than burying it in a
"decisions reserved for the author" section that no one will act on.

**Data is not fact.** A CSV, an audit or another agent's report is a claim to
be re-verified, not a premise. Several of this repo's worst near-misses came
from trusting a previous report: a patch would have engraved "Florence Dufy"
(a welding of two real co-authors' names), another a duplicate English twin of
a central concept, another a `SourceQuote` duplicating one already present.
Each was caught by re-checking, not by reasoning.

**Hostile review before any PR that touches the graph, the maps, the runtime
or a patch.** Invoke the `grc20-reviewer-hostile` skill: it asks nine
questions drawn from real incidents and produces no fix — only what would make
the reasoning wrong. It has issued blocking verdicts that were right, and at
least once been wrong itself and been corrected. Review the reviewer too.

**Browser verification for any runtime change.** A static check does not see
what a reader sees. Chromium lives at `/opt/pw-browsers/chromium`; never run
`playwright install`. CDNs are blocked — intercept them with Playwright's
`page.route` and serve `cytoscape`/`marked` from a local `node_modules`, and
serve the repo over `python3 -m http.server`. Expect zero `pageerror`, and
prove that the default behaviour is unchanged by comparing panel orders before
and after (`grc20-visual-coherence` skill has the recipe).

**Skills** live in `.claude/skills/`: `grc20-reviewer-hostile` (contradict
before committing), `grc20-thesis-archivist` (locate and verify a claim in the
thesis), `grc20-semantic-classifier` (decide an entity's type), and
`grc20-visual-coherence` (check what the site actually shows).

**`docs/audits/` is the repository's memory** — 27 reports and 26 evidence
files. Before opening a chantier, check whether it has already been
instructed; several questions look new and are already documented, with
figures. Read an evidence CSV *with* its audit, never alone: the definitions,
simulated baselines and caveats live in the audit
(`docs/audits/data/README.md` maps each file to its origin).

---

## Security Notes

- **Never commit private keys**. `GEO_PRIVATE_KEY` and similar must only be set in environment variables or Cloudflare Worker secrets.
- No `.gitignore` exists — be careful not to accidentally commit `.env` files or secrets.
- The x402 payment wallet address (`mael-rolland.eth`) should only be changed if explicitly instructed.

---

## Common Tasks

### Adding a new page
1. Create both `page.html` and `page-fr.html`
2. Follow the existing `<head>` structure (copy from `index.html`)
3. Add `hreflang` links in both files
4. Add the page to `sitemap.xml` and `sitemap.html` / `plan-du-site.html`
5. Link it from the navigation (usually `index.html` and `index-fr.html`)

### Updating the knowledge graph

**Never edit a graph JSON by hand.** The house pattern is a dedicated,
re-runnable applicator script:

1. Write `scripts/make_vNNN_<object>.py` on the model of
   `make_v110_apply_bib_and_attribute_patches.py`: reads vN, mutates, writes
   vN+1, supports `--dry-run`, and carries **its own after-checks** (counts
   unchanged unless intended, targets exist, no homonym created…).
2. `space.version` must match the output filename — `check_graph_integrity.py`
   blocks otherwise. Keep `space.note` bounded (~1200 chars); the full history
   lives here, not in the graph.
3. Regenerate the registry **in the same commit**:
   `python3 scripts/build_properties_registry.py` (defaults to the most recent
   graph). An intermediate state where the graph carries a key the registry
   ignores is CI-red, so graph and registry must travel together.
4. Run the local checks (below) before pushing.
5. Update every pointer to the graph filename — `package.json`, `these.html`,
   `graphe.html`, `lecteur.html`, `graph-worker.mjs`,
   `narrative-anchors-build.mjs`. **CI does not verify that the site points at
   the right graph.**
6. Only then publish: `npm run dry-run` → `npm run testnet` → `npm run mainnet`
   (requires `GEO_PRIVATE_KEY`), then update `IPFS_CID` in the Worker.

### Scripts and controls

`scripts/` holds 46 files (41 at the top level plus the
`sourcequote-migration/` module). The ones worth knowing:

| Script | Role |
|---|---|
| `check_graph_integrity.py` | Broken endpoints, duplicate IDs, orphans, version, attribute keys vs registry. **Only the newest graph is blocking**; older snapshots are frozen, reported not enforced |
| `check_anchoring.py` | Anchoring-layer coherence, against a baseline of 46 known problems — it catches *regressions*, not the existing debt |
| `build_anchor_weights.py` | Builds/refreshes `snippet_status` + `direct_anchor_count`; `--check` in CI; `--impact` runs a deterministic ranking simulation |
| `build_properties_registry.py` | **Generates** the registry (never hand-edit it); `--source` selectable, `--check` verifies freshness in CI |
| `preflight_candidate_patches.py` | 12 checks on candidate patches (policy, counts, live IDs, registry, name collisions, `duplicateOf` chains) |
| `compare_panel_policies.py` | Simulates the reader's panels under five display policies; reproduces the reader's real pipeline (parent aggregation, stable sort) |
| `grc20_commun.py` | Shared helpers (`REPO`, most-recent-graph lookup, version parsing) — import it rather than re-deriving |

Run before any push touching the graph, maps or patches:

```bash
python3 scripts/check_graph_integrity.py
python3 scripts/check_anchoring.py
python3 scripts/build_anchor_weights.py --check
python3 scripts/build_properties_registry.py --check
python3 scripts/preflight_candidate_patches.py
```

CI (`.github/workflows/check.yml`, 8 steps, no install) runs these plus JS
syntax and JSON validity, on every push and pull request.

### Applying patch files

Patches are **not** auto-applied and must never be applied by merging JSON by
hand: an applicator script owns the operation (see above). Check the patch's
status in the inventory first — a `historique` patch is already integrated and
replaying it would fail on dead IDs; a `candidat-non-applique` one is waiting
on the author's arbitration and must keep its `CANDIDATE` policy until then.

### Deploying the Worker
```bash
npm run worker-dev      # Test locally at http://localhost:8787
npm run worker-deploy   # Deploy to Cloudflare
```

### Updating Swarm/IPFS hosting
Run `./update-swarm-urls.sh` and follow its instructions to update the ENS contenthash record.

---

## Thesis Content (assets/MD/)

The Markdown files in `assets/MD/` are the full text of the PhD thesis. When working with thesis content:

- `INDEX.md` is the authoritative entry point — read it first for context
- French originals: `01_chapitre_I.md`, etc.
- English translations: `01_chapitre_I_EN.md`, etc.
- `style.css` in this directory styles the `lecteur.html` reader
- The knowledge graph JSON (`grc20-these-mael-rolland-v112.json`) is derived from these texts

Do not modify thesis text content unless explicitly asked — these are archival academic documents.

---

## What This Project Is Not

- It is **not** a React/Vue/Next.js app — do not suggest adding a framework
- It is **not** server-rendered — all pages are static HTML
- It is **not** configured for npm-based frontend builds — `package.json` is only for the Node.js publication scripts
- There is **no unit test suite** — but there *is* CI (see below), and browser
  verification is expected for any runtime change
- **Deployments** are manual; **checks** are not — `.github/workflows/check.yml`
  runs on every push and pull request
