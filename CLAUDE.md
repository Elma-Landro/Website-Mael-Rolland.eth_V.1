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
├── index.html / index-fr.html          # Landing page (EN/FR)
├── these.html / these-fr.html          # Thesis showcase + downloads
├── curriculum.html / curriculum-fr.html
├── contact.html / contact-fr.html
├── collaborate.html / collaborate-fr.html
├── talks.html / talks-fr.html
├── crisis.html / crisis-fr.html        # Bitcoin CVE 2018 + DAO hard fork case studies
├── soutenance.html / soutenance-edition.html
├── atelier.html / workshop.html
├── rare-pepe.html / rare-pepe-fr.html
├── graphe.html                         # Interactive GRC-20 knowledge graph viewer
├── lecteur.html                        # Markdown thesis reader
├── 404.html / 404-fr.html
├── sitemap.html / plan-du-site.html
├── style.css                           # Main stylesheet (1,515 lines)
├── grc20-publish.mjs                   # GRC-20 publication pipeline (Node.js ES module)
├── graph-worker.mjs                    # Cloudflare Worker API (Node.js ES module)
├── grc20-these-mael-rolland-v70.json   # GRC-20 knowledge graph snapshot (3.2 MB)
├── package.json                        # Node.js dependencies + npm scripts
├── update-swarm-urls.sh                # Swarm/IPFS deployment helper
├── sitemap.xml
├── favicon_32x32.png / favicon_16x16.png
├── placeholder.svg
└── assets/
    ├── MD/                             # Thesis chapters in Markdown (bilingual FR/EN)
    │   ├── INDEX.md                    # Agent-readable entry point for thesis content
    │   ├── 00_introduction.md / 00_introduction_EN.md
    │   ├── 01_chapitre_I.md / 01_chapitre_I_EN.md
    │   ├── 02_chapitre_II.md / 02_chapitre_II_EN.md
    │   ├── 03_chapitre_III.md / 03_chapitre_III_EN.md
    │   ├── 04_conclusion.md / 04_conclusion_EN.md
    │   ├── 05_glossaire_annexes.md / 05_glossary_appendix_en.md
    │   └── 06_resume.md
    ├── img/                            # Photos and images
    ├── figures/                        # Research diagrams and visualizations
    ├── icons/                          # Social media and UI icons (17 files)
    └── pdf/                            # Thesis PDFs and related documents
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

---

## Key Source Files

### `grc20-publish.mjs` — Knowledge Graph Pipeline

Converts the JSON snapshot (`grc20-these-mael-rolland-v70.json`) to GRC-20 wire format and publishes it on-chain.

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

---

## GRC-20 Knowledge Graph

The file `grc20-these-mael-rolland-v70.json` is the current authoritative knowledge graph (v70). It contains:

**Entity Types:**
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
| `GreyLiterature` | Non-academic sources |
| `IndigenousLiterature` | Community-originated sources |

The v70 snapshot includes exact PDF quotations and confirmed pagination for evidence traceability.

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
1. Edit `grc20-these-mael-rolland-v70.json` (increment version in the filename/metadata)
2. Run `npm run dry-run` to validate
3. Run `npm run testnet` to test on-chain
4. Run `npm run mainnet` to publish (requires `GEO_PRIVATE_KEY`)
5. Update `IPFS_CID` in the Cloudflare Worker environment after publishing

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
- The knowledge graph JSON (`grc20-these-mael-rolland-v70.json`) is derived from these texts

Do not modify thesis text content unless explicitly asked — these are archival academic documents.

---

## What This Project Is Not

- It is **not** a React/Vue/Next.js app — do not suggest adding a framework
- It is **not** server-rendered — all pages are static HTML
- It is **not** configured for npm-based frontend builds — `package.json` is only for the Node.js publication scripts
- There is **no test suite** — manual testing via browser and `npm run dry-run`
- There is **no CI/CD pipeline** — deployments are manual
