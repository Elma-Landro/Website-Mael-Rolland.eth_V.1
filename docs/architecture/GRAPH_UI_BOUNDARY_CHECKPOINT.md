# GRAPH_UI_BOUNDARY_CHECKPOINT

Date: 2026-04-04  
Scope: documentation-only checkpoint after helper/state/validator/modals/panel-controller extractions.

## 1) Current remaining UI surface in `graphe.html`

This checkpoint focuses on UI-side logic still inline in `graphe.html` after module extractions.

### In-scope remaining UI blocks (at time of writing)
- `UI.renderTypeFilters` — **now extracted** to `graphe.ui-filters.js`; stub remains in `UI`.
- `UI.renderPanel` main body — **now extracted** (HTML builder to `graphe.ui-panel.js`, action wiring to `graphe.ui-panel-actions.js`); `renderPanel` is now a 10-line coordinator.
- UI form/modal helpers (`openAddEntityModal`, `openEditModal`, `addAttrRow`, `getAttrRows`) — **now extracted** to `graphe.ui-entity-forms.js`.
- `openAddRelationModal` — delegated to `graphe.ui-relations-modal.js`.
- `confirmDeleteRelation` — delegated to `graphe.ui-panel-actions.js`.
- `selectEntity` — remains inline; depends on `Graph.cy` (Graph not yet extracted).
- `clearPanel` — remains inline; 3-line DOM reset, too small to extract alone.
- Large DOMContentLoaded UI/event wiring block — intentionally untouched.

### Already extracted (context)
- Helpers: `graphe.helpers.js`
- State: `graphe.state.js`
- Validator/Exporter: `graphe.validation-export.js`
- Modals: `graphe.modals.js`
- Panel controller/orchestration: `graphe.panels.js`
- Tiny panel render helpers: `graphe.panel-render.js`

## 2) Boundary classification by extraction risk

## A. Low-risk extractable next (updated — prior items completed)

### A1. `renderTypeFilters` boundary — **DONE** (`graphe.ui-filters.js`)
Extracted with safe DOM construction; `UI.renderTypeFilters` is now a stub.

### A2. Validation report modal HTML formatter (optional low risk)
- The small inline formatter in the validate button handler can be pulled into a pure formatter helper.
- Keep modal open/close wiring in place.

## B. Medium-risk

### B1. `UI.renderPanel` relation grouping/rendering sub-block
- Relation grouping currently closes over `State.maps`, type colors, delete callbacks, and selection behavior.
- Extractable only if split into pure formatters + retained inline event bindings.

### B2. `setupEntitySearch`
- UI-focused but tightly event-driven and used by relation modal flow.
- Medium risk because behavior depends on exact DOM timing and hidden-id/preview synchronization.

### B3. Add/Edit modal preparation functions
- `openAddEntityModal`, `openAddRelationModal`, `openEditModal` are UI-only but coupled to live state maps and modal workflow.

## C. Too entangled for now

### C1. DOMContentLoaded orchestration block
- Contains mixed concerns: top-nav UI, file load, layout switching, filters, CRUD form submit wiring, validation modal rendering, keyboard shortcuts, drag/drop, auto-fetch, and scrolly mode toggles.
- Should not be extracted before a narrow UI boundary (filters/forms) is stabilized.

### C2. UI ↔ graph/layout coupling points
- `renderTypeFilters` and many handlers call `Graph.applyFilters()` / layout methods directly.
- Larger extraction here would collide with graph/layout boundary and is out of scope now.

### C3. UI ↔ story/scrolly coupling points
- Scrolly mode toggles and story panel interactions share runtime controls with toolbar and panel behavior.
- Deferred by design until story/scrolly phase.

## 3) Status after child branch `feat/research-architecture-vnext-panel-deeper`

All medium-risk UI surfaces have been extracted. The `UI` IIFE now contains only its irreducible coordination core.

Completed extractions (beyond original checkpoint scope):
- `graphe.ui-panel.js` — pure panel body HTML builder
- `graphe.ui-panel-actions.js` — post-render action wiring with callback injection
- `graphe.ui-entity-forms.js` — entity form/modal helpers

Remaining inline by design:
- `selectEntity` — calls `Graph.cy`; requires Graph extraction first.
- `clearPanel` — 3-line DOM reset; too small to extract alone.
- `DOMContentLoaded` wiring block — composition root; out of scope.

## 4) What to defer intentionally

- `selectEntity` extraction (requires Graph module boundary first).
- DOMContentLoaded-wide extraction.
- Story/scrolly extraction.
- Graph/layout extraction.

This checkpoint is intended to gate the next code step conservatively, not to trigger broad refactors.
