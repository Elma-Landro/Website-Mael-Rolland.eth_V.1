# GRAPH_MODULARIZATION_AUDIT

Date: 2026-04-04  
Scope: **audit + extraction planning only** (no runtime refactor in this pass).

## 1) Current graph app structure

The current V2 graph app is implemented as a single-page document with large inline CSS + JS in `graphe.html`.

- `graphe.html` is the application shell (header, menus, sidebar, Cytoscape canvas, detail panel, scrolly panel, modals).【F:graphe.html†L979-L1221】
- Styling is largely inline in the same file (`<style>` block) with substantial component/state CSS (sidebar, panel, story/scrolly, mobile behavior).【F:graphe.html†L11-L1006】
- Runtime logic is in one large inline `<script>` block with module-like IIFEs (`State`, `Graph`, `Editor`, `UI`, `StoryMode`, etc.).【F:graphe.html†L1479-L7125】
- Data bootstrap currently auto-fetches canonical graph `grc20-these-mael-rolland-v96.json` and optionally `narrative-anchors.json`.【F:graphe.html†L6699-L6711】
- External graph dependencies are loaded by CDN (Cytoscape + dagre).【F:graphe.html†L8-L10】

## 2) Responsibilities currently concentrated in `graphe.html`

### A. App shell + navigation + layout chrome
- Header controls, dropdown menus, layout selector, and mode toggles are defined and wired in the same file.【F:graphe.html†L979-L1060】【F:graphe.html†L6443-L6533】

### B. Presentation layer (CSS)
- Page-level and component-level styles coexist in one block (layout, panel, toolbars, scrolly, story mode, responsive behaviors).【F:graphe.html†L11-L1006】

### C. Data state + indexes + undo/versioning
- `State` owns working copy, maps/indexes (`entities`, `types`, `relation_types`, incoming/outgoing adjacency), undo stack, selected node, hidden types, search query, errors.【F:graphe.html†L2223-L2327】

### D. Graph rendering + layout engine glue
- `Graph` encapsulates Cytoscape init/style/elements, label visibility strategy, filters, highlighting, and multiple custom layouts (`nebula`, `matrice`, `monetisation`, `qui-gouverne`, etc.).【F:graphe.html†L2342-L4501】
- Graph rebuild + layout + filters are orchestrated in `Graph.render()`.【F:graphe.html†L2899-L2911】

### E. Editing workflow
- Entity/relation CRUD and UI refresh orchestration are embedded in `Editor` and related listeners in the same file.【F:graphe.html†L4894-L5032】【F:graphe.html†L6578-L6631】

### F. Validation + export
- Validation rules (`broken_rel`, duplicate names, empty type) and export-to-file version bump logic live inline here.【F:graphe.html†L5037-L5117】

### G. Detail panel + interaction UI
- Node detail rendering (attributes/sources/relations/actions), panel state/drag/resize, type filter rendering, and modal helpers are in-file (`PanelController`, `UI`, `Modals`).【F:graphe.html†L5119-L5440】

### H. Story mode / scrollytelling / anchored narrative
- `StoryMode` imports `story-presets.mjs` dynamically and controls narrative step focusing, reveal phases, bridge hints, and panel state.【F:graphe.html†L5833-L6409】
- Scrolly behavior, chapter/section highlighting, IntersectionObserver lifecycle, anchor-section injection from `narrative-anchors.json`, and deep-link anchor support are in the same script body.【F:graphe.html†L6699-L6711】【F:graphe.html†L6895-L7052】

### I. Event wiring
- Most app events are wired in a single `DOMContentLoaded` block (menus, layout, filters, CRUD, keyboard shortcuts, drag/drop, bootstrap fetch, scrolly mode).【F:graphe.html†L6443-L7123】

### J. Persistence behavior
- There is currently no `localStorage`/`sessionStorage` persistence logic in `graphe.html`; state is in-memory during session. (Only URL query parsing for `?anchor=` is used.)【F:graphe.html†L6961-L6973】

## 3) External files already helping modularity

- `story-presets.mjs`: externalized narrative registry (`viewToStoryId`, story sequences, step options), already consumed by `StoryMode` via dynamic import.【F:story-presets.mjs†L1-L20】【F:graphe.html†L5896-L5904】
- `narrative-anchors-build.mjs`: build-time generator for `narrative-anchors.json`, including chapter normalization and anchor scene metadata consumed by `graphe.html`/`lecteur.html`.【F:narrative-anchors-build.mjs†L2-L19】【F:narrative-anchors-build.mjs†L151-L193】
- `graph-worker.mjs`: separate worker/API surface for hosted graph access and filtering; useful for future boundary thinking, but not directly wired by `graphe.html` in current runtime path.【F:graph-worker.mjs†L1-L38】

## 4) Coupling / pain points

1. **Single-file concentration risk**: structure, style, state, render, edit, narrative, and event orchestration are all in one document, increasing regression surface for any change.
2. **Large script lifecycle coupling**: many features depend on global ordering and shared mutable state (`State`, `Graph`, `StoryMode`), making extraction sensitive to initialization sequence.
3. **UI + domain logic mixed**: narrative semantics (focus resolution, relation filters, bridge behavior) are tightly mixed with DOM concerns.
4. **Layout complexity in one module**: specialized layouts (nebula/matrice/monetisation/qui-gouverne) and style class conventions are tightly coupled to Cytoscape class names.
5. **Event handler sprawl**: `DOMContentLoaded` central wiring block is long; difficult to test/trace feature boundaries.

## 5) Proposed target module boundaries (planning only)

Conservative module families for future extraction (no behavior change target):

- `graph-app/shell/*` — header/menu wiring and page mode toggles.
- `graph-app/state/*` — data state, maps, undo/versioning.
- `graph-app/graph/*` — Cytoscape adapter, element mapping, style/class rules, layout adapters.
- `graph-app/panel/*` — detail panel rendering + panel drag/resize controller.
- `graph-app/editor/*` — CRUD actions + validation/export helpers.
- `graph-app/story/*` — story preset orchestration and focus runtime.
- `graph-app/scrolly/*` — observer, chapter/section/anchor highlighting lifecycle.
- `graph-app/bootstrap/*` — canonical fetch + anchors fetch + load fallback logic.

## 6) Suggested future module names or families

Minimal naming proposal (low-friction, progressive):

- `graphe.state.mjs`
- `graphe.graph-core.mjs`
- `graphe.graph-layouts.mjs`
- `graphe.panel-ui.mjs`
- `graphe.editor.mjs`
- `graphe.story-mode.mjs`
- `graphe.scrolly.mjs`
- `graphe.bootstrap.mjs`
- `graphe.events.mjs`

## 7) Safe extraction order (step-by-step)

1. **Extract pure utility helpers** (string escaping, small normalizers, reusable constants).  
   Risk: **Low**.
2. **Extract state/index builder (`State`)** with unchanged API surface.  
   Risk: **Low–Medium**.
3. **Extract validation/export/editor helpers** (`Validator`, `Exporter`, CRUD methods) while keeping DOM calls in place.  
   Risk: **Low–Medium**.
4. **Extract panel rendering/controller** (`PanelController`, `UI.renderPanel`) with compatibility wrappers.  
   Risk: **Medium**.
5. **Extract story/scrolly orchestration** into separate modules, preserving class names and callback contracts.  
   Risk: **Medium–High**.
6. **Extract graph core/layouts last** (`Graph` + Cytoscape style/layout class contracts), since this is the highest coupling zone.  
   Risk: **High**.

## 8) What can be extracted first with lowest runtime risk

- Pure helper functions and constants (e.g., `escHtml`, relation name normalization helpers used in story focus).
- `State` map-building + undo/version utilities as a standalone module with same method names.
- `Validator` and `Exporter` as isolated modules (minimal dependency: `State`, DOM target ids for badges/version label).

These provide the best reduction in `graphe.html` complexity with minimal visual/runtime risk.

## 9) What should remain untouched until later

- Cytoscape style/class matrix and specialized layout implementations (`applyNebulaLayout`, `applyMatriceLayout`, monetisation/qui-gouverne variants) until wrappers and regression checks exist.【F:graphe.html†L3044-L3210】【F:graphe.html†L3841-L4501】
- Scrolly observer + anchor injection flow until module boundaries for `StoryMode` callbacks are stabilized.【F:graphe.html†L6895-L7052】
- Boot sequence ordering (`onDataLoaded` + `DOMContentLoaded` event registration + async fetch block) until extracted modules define explicit init contracts.【F:graphe.html†L6411-L6439】【F:graphe.html†L6443-L7123】

---

## Appendix — current zones → future module family

| Current zone in `graphe.html` | Future family | Risk |
|---|---|---|
| `State` IIFE | `graph-app/state/*` | Low–Medium |
| `Validator` + `Exporter` | `graph-app/editor/*` | Low |
| `PanelController` + `UI.renderPanel` | `graph-app/panel/*` | Medium |
| `StoryMode` | `graph-app/story/*` | Medium–High |
| Scrolly functions (`initAnchoredScrolly`, `initScrollyObserver`) | `graph-app/scrolly/*` | Medium–High |
| `Graph` IIFE + layout methods | `graph-app/graph/*` | High |

## Update — first extraction executed (2026-04-04)

- Extracted two pure helpers from `graphe.html` into `graphe.helpers.js`:
  - `escHtml`
  - `generateId`
- `graphe.html` now consumes these via `window.GrapheHelpers` with identical fallback logic to preserve runtime behavior if the helper script fails to load.

## Update — second extraction executed (2026-04-04)

- Extracted two additional pure relation-name helpers into `graphe.helpers.js`:
  - `normalizeRelationName`
  - `canonicalizeRelationName`
- `graphe.html` now consumes these via `window.GrapheHelpers` with safe inline fallback behavior preserved.

## Update — state extraction executed (2026-04-04)

- Extracted the full `State` IIFE into `graphe.state.js` as `createGrapheState()`, preserving method names and the returned API contract (`data`, `version`, `dirty`, `selectedId`, `hiddenTypes`, `searchQ`, `errors`, `maps`, `load`, `snapshot`, `undo`, `getEntityTypeName`, `getEntityDesc`, `undoCount`, `bumpVersion`).
- `graphe.html` now initializes state via `const State = window.createGrapheState();`.
- Graph/layout, panel, and story/scrolly orchestration remain in `graphe.html` for later phases.

## Update — validator/exporter extraction executed (2026-04-04)

- Extracted `Validator` + `Exporter` logic into `graphe.validation-export.js` as:
  - `createGrapheValidator({ State, document })`
  - `createGrapheExporter({ State, document, toast, BlobCtor, URLApi })`
- `graphe.html` now wires these with:
  - `const Validator = window.createGrapheValidator({ State, document });`
  - `const Exporter = window.createGrapheExporter({ State, document, toast, BlobCtor: Blob, URLApi: URL });`
- Panel, story/scrolly, and graph/layout logic remain in `graphe.html`.

## Update — modals extraction executed (2026-04-04)

- Extracted `Modals` utility into `graphe.modals.js` as `createGrapheModals({ document })`.
- Preserved the same API contract in runtime usage:
  - `open(id)`
  - `close(id)`
  - `closeAll()`
- `graphe.html` now initializes with `const Modals = window.createGrapheModals({ document });`.
- Panel, story/scrolly, and graph/layout logic remain in `graphe.html`.

## Update — panel-controller extraction executed (2026-04-04)

- Extracted `PanelController` orchestration into `graphe.panels.js` as:
  - `createGraphePanelController({ document, window, State })`
- `graphe.html` now initializes with:
  - `const PanelController = window.createGraphePanelController({ document, window, State });`
- This pass extracts controller behavior (open/close/minimize/meta/drag/resize/init wiring) only.
- Detailed panel content rendering remains in `UI.renderPanel` inside `graphe.html`.

## Update — panel-render helper extraction executed (2026-04-04)

- Extracted a tiny pure/local helper subset for panel rendering into `graphe.panel-render.js`:
  - `GraphePanelRender.splitPanelAttributes(attrs, escHtml)`
- `UI.renderPanel` remains in `graphe.html`; only the attribute/source split loop moved out.
- Relation grouping/rendering, event handlers, and panel action wiring remain inline in `graphe.html`.

## Update — final tiny panel-render helper pass (2026-04-04)

- Extracted one additional pure/local formatter into `graphe.panel-render.js`:
  - `GraphePanelRender.buildAttrsHtml(regularAttrs, escHtml)`
- `UI.renderPanel` now delegates only the attributes-block HTML formatting to this helper.
- Relation rendering, sources wrapper HTML, and all panel event wiring remain inline in `graphe.html`.

## Update — renderTypeFilters extraction executed (2026-04-04)

- Extracted `renderTypeFilters` into `graphe.ui-filters.js` via:
  - `createGrapheUiFilters({ document, State, Graph, TYPE_COLORS })`
- `UI` now delegates with:
  - `const uiFilters = window.createGrapheUiFilters({ document, State, Graph, TYPE_COLORS });`
  - `function renderTypeFilters() { return uiFilters.renderTypeFilters(); }`
- Adjacent modal/form helpers and `UI.renderPanel` remain inline in `graphe.html` for a later phase.

## Update — setupEntitySearch extraction executed (2026-04-04)

- Extracted `setupEntitySearch` into `graphe.ui-search.js` via:
  - `createGrapheUiSearch({ document, State, TYPE_COLORS, escHtml })`
- `UI` now delegates with:
  - `const uiSearch = window.createGrapheUiSearch({ document, State, TYPE_COLORS, escHtml });`
  - `function setupEntitySearch(inputId, suggestId, hiddenId, previewId) { return uiSearch.setupEntitySearch(...); }`
- Add/Edit modal preparation and `UI.renderPanel` remain inline in `graphe.html`.

## Update — openAddRelationModal extraction executed (2026-04-04)

- Extracted `openAddRelationModal` into `graphe.ui-relations-modal.js` via:
  - `createGrapheUiRelationsModal({ document, State, Modals })`
- `UI` now delegates with:
  - `const uiRelationsModal = window.createGrapheUiRelationsModal({ document, State, Modals });`
  - `function openAddRelationModal(prefillFromId) { return uiRelationsModal.openAddRelationModal(prefillFromId); }`
- `openAddEntityModal`, `openEditModal`, and `UI.renderPanel` remain inline for later phases.
