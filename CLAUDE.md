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
├── grc20-these-mael-rolland-v110.json          # Current authoritative knowledge graph (canonical)
│
├── entity_section_map.json                     # Entity ID → thesis subsection mapping
├── section_entities_map.json                   # Thesis section → entity list mapping
├── section_overrides.json                      # Manual overrides for section assignments
├── new_relations_patch.json                    # Batch of new relations to inject
├── patch_1a_fix_cited_in.json                  # Fix cited_in chapter assignments
├── patch_1b_missing_cited_in.json              # Add missing cited_in relations
├── patch_2a_sourcequote_subsections.json       # SourceQuote → subsection relations
├── patch_2b_central_arguments.json             # Central argument node relations
├── patch_2c_definitions.json                   # Definition node patches
├── patch_3a_intro_subsections.json             # Introduction subsection relations
│
├── anomalies_report.md                         # Entity/section mapping QA report (v71 base)
├── package.json                                # Node.js dependencies + npm scripts
├── update-swarm-urls.sh                        # Swarm/IPFS deployment helper
├── sitemap.xml
├── LICENSE                                     # Apache-2.0
├── README.md
├── favicon_32x32.png / favicon_16x16.png
├── placeholder.svg
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
    │   └── 06_resume.md
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

---

## GRC-20 Knowledge Graph

The file `grc20-these-mael-rolland-v110.json` is the current authoritative knowledge graph (v110, 2,293 entities, 20,207 relations). Snapshots v96 through v110 are kept in the repo; only the most recent is blocking in CI.

### Entity Types (v110 — 55 types)

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

The graph has evolved across 110 versions. Key milestones: v72 added the `ThesisSection` layer (23 subsection nodes, 11,884 `appears_in_section` relations); v88–v90 added `appears_in_section` relations for frameworks, arguments, and concepts; v97 repaired 15 truncated relation endpoints; v98–v99 added missing chronology events and wired the maturation phase; v100 renumbered the chapter I sections onto the thesis's own numbering; v101 dropped 19 orphan ops; v102 restored the thesis's 8 development domains; v103 wired events to domains from the v2 catalogue; v104 added Ethereum's hard forks; v105 applied the event dedup patch; v106 completed the section migration for chapters II and III (13 renumbered, 11 created), after which all 48 table-of-contents entries in `graphe.html` resolve to a graph node. v107 wired the four chapter I sections that had stayed outside the `section of` / `has section` tree. v108 realigned 3,970 `section_key` attributes carried by `appears in section` relations, which still named the pre-migration key of their own target. v109 (« voie C ») rewired 3,970 of those relations to the section whose text their anchoring charge actually describes — 18 keys had been shifted one block over by the v100/v106 migrations, which made 8 table-of-contents entries look empty while their content sat under the neighbour's key. v110 corrected one bibliographic typo (Danezis), retyped 21 bibliography-confirmed author cards from Reference to Person, and applied 384 mechanical attribute normalisations described by `grc20-properties-registry-v1.json` — now a CI invariant. **v110 is the current canonical snapshot.**

### Patch Files

Several JSON patch files in the root apply corrections and enrichments to the base graph:

| File | Purpose |
|------|---------|
| `patch_1a_fix_cited_in.json` | Fix incorrect chapter assignments in `cited_in` |
| `patch_1b_missing_cited_in.json` | Add missing `cited_in` relations |
| `patch_2a_sourcequote_subsections.json` | Link `SourceQuote` nodes to subsections |
| `patch_2b_central_arguments.json` | Argument node relations |
| `patch_2c_definitions.json` | Definition node enrichment |
| `patch_3a_intro_subsections.json` | Introduction subsection links |
| `new_relations_patch.json` | Batch of new graph relations |

### Mapping Files

| File | Purpose |
|------|---------|
| `entity_section_map.json` | Maps entity IDs to their thesis subsections |
| `section_entities_map.json` | Maps section IDs to their entity lists |
| `section_overrides.json` | Manual overrides for ambiguous assignments |

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
1. Edit the latest `grc20-these-mael-rolland-vN.json` (increment version in the filename/metadata)
2. Run `npm run dry-run` (update the script path or pass `--input` explicitly)
3. Run `npm run testnet` to test on-chain
4. Run `npm run mainnet` to publish (requires `GEO_PRIVATE_KEY`)
5. Update `IPFS_CID` in the Cloudflare Worker environment after publishing
6. Update `entity_section_map.json` / `section_entities_map.json` if section structure changed

### Applying patch files
Patch files are applied by merging their entity/relation data into the base graph JSON. They are not auto-applied — the publishing pipeline must be run after merging.

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
- The knowledge graph JSON (`grc20-these-mael-rolland-v110.json`) is derived from these texts

Do not modify thesis text content unless explicitly asked — these are archival academic documents.

---

## What This Project Is Not

- It is **not** a React/Vue/Next.js app — do not suggest adding a framework
- It is **not** server-rendered — all pages are static HTML
- It is **not** configured for npm-based frontend builds — `package.json` is only for the Node.js publication scripts
- There is **no test suite** — manual testing via browser and `npm run dry-run`
- There is **no CI/CD pipeline** — deployments are manual
