# GRAPH_UI_BOUNDARY_CHECKPOINT

Date: 2026-04-04  
Scope: documentation-only checkpoint after helper/state/validator/modals/panel-controller extractions.

## 1) Current remaining UI surface in `graphe.html`

This checkpoint focuses on UI-side logic still inline in `graphe.html` after module extractions.

### In-scope remaining UI blocks
- `UI.renderTypeFilters` (type counting + DOM rendering + click wiring to hidden types + filter apply).
- `UI.renderPanel` main body (panel content assembly, relation grouping, action button wiring, delete confirmations).
- UI utility methods still tied to modals/forms/search (`openAddEntityModal`, `openAddRelationModal`, `openEditModal`, `setupEntitySearch`, `confirmDeleteRelation`).
- Large DOMContentLoaded UI/event wiring block for menus, filters, form actions, validation modal rendering, and panel-triggered flows.

### Already extracted (context)
- Helpers: `graphe.helpers.js`
- State: `graphe.state.js`
- Validator/Exporter: `graphe.validation-export.js`
- Modals: `graphe.modals.js`
- Panel controller/orchestration: `graphe.panels.js`
- Tiny panel render helpers: `graphe.panel-render.js`

## 2) Boundary classification by extraction risk

## A. Low-risk extractable next

### A1. `renderTypeFilters` boundary (recommended next)
Why low risk:
- Small, self-contained rendering loop.
- Depends on known inputs (`State.data`, `State.hiddenTypes`, `TYPE_COLORS`) and one side effect (`Graph.applyFilters`).
- Already called from clear points (`onDataLoaded`, filter buttons, undo refresh) and has a clean UI purpose.

Extraction shape:
- Keep behavior identical.
- Move into a small `graphe.ui-filters.js` factory with explicit deps (`State`, `Graph`, `TYPE_COLORS`, `document`).
- Preserve same call pattern via `UI.renderTypeFilters()` shim if needed.

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

## 3) Recommended next step after this checkpoint

### Recommendation: extract **renderTypeFilters / UI filter boundary** next.

Reasoning:
1. It is the cleanest remaining UI-only surface with minimal coupling footprint.
2. It gives immediate reduction in `UI` inline size without entering story/scrolly or graph/layout internals.
3. It provides a stable pattern for future `UI` modularization (factory + dependency injection) before touching medium-risk panel rendering or search forms.

## 4) What to defer intentionally

- Full `UI.renderPanel` extraction (keep current in-place structure).
- DOMContentLoaded-wide extraction.
- Story/scrolly extraction.
- Graph/layout extraction.

This checkpoint is intended to gate the next code step conservatively, not to trigger broad refactors.
