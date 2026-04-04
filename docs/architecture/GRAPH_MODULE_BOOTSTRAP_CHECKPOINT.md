# GRAPH_MODULE_BOOTSTRAP_CHECKPOINT

Date: 2026-04-04  
Scope: documentation-only checkpoint for extracted graph runtime modules and bootstrap assumptions.

## 1) Current extracted module list

UI/runtime modules currently loaded by `graphe.html`:

1. `graphe.helpers.js`
2. `graphe.state.js`
3. `graphe.validation-export.js`
4. `graphe.modals.js`
5. `graphe.panels.js`
6. `graphe.panel-render.js`
7. `graphe.ui-filters.js`

All of these expose global symbols on `window` (factory functions or helper namespaces).

## 2) Script load order (current)

`graphe.html` currently loads modules in this exact order, before the main inline script executes:

| Order | Script | Exposed global | Used by |
|---|---|---|---|
| 1 | `graphe.helpers.js` | `window.GrapheHelpers` | inline helper aliases (`escHtml`, `generateId`, relation-name helpers) |
| 2 | `graphe.state.js` | `window.createGrapheState` | `const State = window.createGrapheState();` |
| 3 | `graphe.validation-export.js` | `window.createGrapheValidator`, `window.createGrapheExporter` | `Validator`, `Exporter` initialization |
| 4 | `graphe.modals.js` | `window.createGrapheModals` | `Modals` initialization |
| 5 | `graphe.panels.js` | `window.createGraphePanelController` | `PanelController` initialization |
| 6 | `graphe.panel-render.js` | `window.GraphePanelRender` | `UIPanelRenderer.buildPanelBodyHtml` |
| 7 | `graphe.ui-panel.js` | `window.createGrapheUiPanel` | `UIPanelRenderer` init inside `UI` |
| 8 | `graphe.ui-panel-actions.js` | `window.createGrapheUiPanelActions` | `PanelActions` init inside `UI` |
| 9 | `graphe.ui-entity-forms.js` | `window.createGrapheUiEntityForms` | `EntityForms` init inside `UI` |
| 10 | `graphe.ui-filters.js` | `window.createGrapheUiFilters` | `uiFilters` init inside `UI` |
| 11 | `graphe.ui-search.js` | `window.createGrapheUiSearch` | `uiSearch` init inside `UI` |
| 12 | `graphe.ui-relations-modal.js` | `window.createGrapheUiRelationsModal` | `uiRelationsModal` init inside `UI` |

## 3) Dependency map (module-level)

## A. `graphe.helpers.js`
- Exposes pure helper namespace.
- Runtime dependency: none beyond browser globals (`window`, `crypto`).
- Consumed directly by inline aliases in `graphe.html`.

## B. `graphe.state.js`
- Exposes factory `createGrapheState()`.
- Runtime dependency: none beyond JS runtime.
- Consumed by inline `State` init.

## C. `graphe.validation-export.js`
- Exposes factories:
  - `createGrapheValidator({ State, document })`
  - `createGrapheExporter({ State, document, toast, BlobCtor, URLApi })`
- Explicit dependency injection for runtime collaborators.

## D. `graphe.modals.js`
- Exposes `createGrapheModals({ document })`.
- Adds backdrop-click listener when factory is called.

## E. `graphe.panels.js`
- Exposes `createGraphePanelController({ document, window, State })`.
- Depends on panel DOM ids, pointer events, and `State.selectedId`/`State.maps` for launcher visibility state.

## F. `graphe.panel-render.js`
- Exposes namespace `window.GraphePanelRender`:
  - `splitPanelAttributes(attrs, escHtml)`
  - `buildAttrsHtml(regularAttrs, escHtml)`
- Pure/local markup helpers intended for `UI.renderPanel` use.

## G. `graphe.ui-filters.js`
- Exposes `createGrapheUiFilters({ document, State, Graph, TYPE_COLORS })`.
- Depends on injected `Graph.applyFilters()` and `State.hiddenTypes` semantics.

## 4) `graphe.html` bootstrap assumptions still in force

1. **Script-order assumption is strict**: inline initialization expects all factories/namespaces to already exist on `window`.
2. **Mixed access pattern**:
   - factory-created modules: state, validator/exporter, modals, panels, ui-filters.
   - namespace helpers: `GrapheHelpers`, `GraphePanelRender`.
3. **Inline fallback exists only for some helpers** (`GrapheHelpers` aliases), not for all module factories.
4. **Inline script remains primary composition root** for module wiring and runtime orchestration.

## 5) Fragile points / implicit coupling

- If any extracted script fails to load, dependent inline initialization can fail early (except helper alias fallbacks).
- `graphe.ui-filters.js` and `graphe.panels.js` assume injected dependencies are initialized and stable (`State`, `Graph`, `TYPE_COLORS`, panel DOM structure).
- `UI.renderPanel` still mixes formatting, data mapping, and event wiring; extracted helpers reduce size but not orchestration coupling.
- DOMContentLoaded block remains a dense mixed-concern initializer; not touched in this checkpoint by design.

## 6) Safe for future extraction vs defer list

## Safe next targets
- Additional small UI-only boundaries with explicit dependency injection and compatibility shims (e.g., selected form/search helper boundaries).
- Pure formatter/helper moves from inline UI blocks where behavior is deterministic.

## Defer for now
- Story/scrolly orchestration extraction.
- Graph/layout extraction.
- Large DOMContentLoaded decomposition.

## 7) Should a lightweight bootstrap module exist later?

Yes — **document-only recommendation** (no implementation in this pass):

A future small bootstrap module could centralize:
- factory availability checks,
- deterministic init order,
- wiring of shared dependencies (`State`, `Graph`, `document`, `TYPE_COLORS`, `toast`),
- clearer error reporting when a script is missing.

This would reduce implicit assumptions in `graphe.html` without forcing a full bundler/runtime redesign.
