# Graph Panel Deeper — Extraction Checkpoint

**Branch:** `feat/research-architecture-vnext-panel-deeper`  
**Date:** 2026-04-04  
**Milestone parent:** `codex/create-restructuring-proposal-for-research-architecture` (frozen)

---

## What Was Extracted

### New file: `graphe.ui-panel.js`

Factory: `createGrapheUiPanel({ State, GraphePanelRender, escHtml, TYPE_COLORS })`  
Exported via: `window.createGrapheUiPanel`  
Instantiated as: `UIPanelRenderer` (before the inline `UI` IIFE in `graphe.html`)

**Exported method:** `buildPanelBodyHtml(id) → string`

Builds the complete HTML string for the panel body, including:
- Entity type badge (color, label)
- Entity name and description
- Summary grid (relation count, attribute count)
- Sources section (PDF page links) — delegates to `GraphePanelRender.splitPanelAttributes`
- Attributes section — delegates to `GraphePanelRender.buildAttrsHtml`
- Relations section grouped by type (outgoing and incoming)
- Action buttons bar (`panel-btn-edit`, `panel-btn-addrel`, `panel-btn-delete`)
- Entity ID footer

**Contract:** pure function — no DOM writes, no event listeners, no Graph calls, no Editor calls.  
Returns `''` if `State.maps.entities[id]` is undefined.

### Modified: `graphe.html`

Three changes, all minimal and reversible:

1. **Script load order** (line 17): added `<script src="graphe.ui-panel.js"></script>` after `graphe.panel-render.js` and before `graphe.ui-filters.js`.

2. **Instantiation** (after `PanelController`): added
   ```javascript
   const UIPanelRenderer = window.createGrapheUiPanel({
     State,
     GraphePanelRender: window.GraphePanelRender,
     escHtml,
     TYPE_COLORS,
   });
   ```

3. **`UI.renderPanel`**: replaced the ~70-line inline HTML building block with a single call:
   ```javascript
   body.innerHTML = UIPanelRenderer.buildPanelBodyHtml(id);
   ```
   The surrounding coordination logic (DOM show/hide, `PanelController.open/setMeta`, event listeners) is unchanged.

---

## Pass 2 — Action Wiring Extraction (2026-04-04)

### New file: `graphe.ui-panel-actions.js`

Factory: `createGrapheUiPanelActions({ document, State, Modals, onSelectEntity, onEditEntity, onAddRelation, onExecuteDeleteEntity, onExecuteDeleteRelation })`  
Exported via: `window.createGrapheUiPanelActions`  
Instantiated as: `PanelActions` inside the `UI` IIFE (top of IIFE, captures hoisted function declarations as arrow-function callbacks)

**Exported methods:**
- `wirePanel(body, entityId)` — attaches all post-render event listeners to relation rows and action buttons
- `confirmDeleteRelation(relIdx)` — exposed so the `UI` IIFE's `confirmDeleteRelation` stub can delegate to it (preserving the existing export on the `UI` object)

**What was extracted into this module:**
- `.panel-rel-row` click handler (navigate to entity or trigger relation delete)
- `#panel-btn-edit` click → `onEditEntity(id)`
- `#panel-btn-addrel` click → `onAddRelation(id)`
- `#panel-btn-delete` click → confirm modal setup + `onExecuteDeleteEntity(id)`
- `confirmDeleteRelation(relIdx)` logic (confirm modal setup + `onExecuteDeleteRelation(relIdx)`)

**Callbacks and why they are injected rather than direct references:**

| Callback | Injected because |
|---|---|
| `onSelectEntity` | `selectEntity` calls `Graph.cy` — Graph module not yet extracted |
| `onEditEntity` | `openEditModal` is inline UI form-population logic — UI IIFE not yet decomposed |
| `onAddRelation` | `openAddRelationModal` delegates to `uiRelationsModal` — internal to UI IIFE |
| `onExecuteDeleteEntity` | `Editor.deleteEntity` — Editor IIFE not yet extracted |
| `onExecuteDeleteRelation` | `Editor.deleteRelation` — same reason |

### Modified: `graphe.html` (Pass 2)

1. **Script load order** (line 18): added `<script src="graphe.ui-panel-actions.js"></script>` after `graphe.ui-panel.js`.

2. **UI IIFE — PanelActions instantiation** (top of IIFE): `PanelActions` is created before `renderPanel`, using arrow-function callbacks so that hoisted function declarations (`selectEntity`, `openEditModal`, etc.) are safely captured even though they appear later in source order.

3. **`UI.renderPanel`** reduced to a 10-line coordinator:
   ```javascript
   function renderPanel(id) {
     const entity = State.maps.entities[id];
     if (!entity) { clearPanel(); return; }
     const typeName = State.getEntityTypeName(entity);
     document.getElementById('panel-empty').classList.add('hidden');
     const body = document.getElementById('panel-body');
     body.classList.remove('hidden');
     PanelController.open();
     PanelController.setMeta(entity.name, typeName);
     body.innerHTML = UIPanelRenderer.buildPanelBodyHtml(id);
     PanelActions.wirePanel(body, id);
   }
   ```

4. **`UI.confirmDeleteRelation`** reduced to a 1-line stub delegating to `PanelActions.confirmDeleteRelation(relIdx)`. Export on the `UI` object preserved unchanged.

---

## What Remains Inline in graphe.html — and Why

### `selectEntity(id)`

Calls `Graph.cy.animate()` and `Graph.highlightNeighbors()` — a direct dependency on the inline `Graph` module (~2,160 lines). This bidirectional coupling (`Graph` tap event → `UI.renderPanel`; `UI.selectEntity` → `Graph`) cannot be resolved until the Graph module is extracted or an event bus is introduced. **Do not touch.**

### `openEditModal(id)` / `openAddEntityModal()`

Form population helpers for entity edit/add modals. They manipulate inline DOM elements (`#ee-attrs-editor`, `#ae-attrs-editor`, etc.) and call `addAttrRow`. These belong together with `addAttrRow` / `getAttrRows` in a future `graphe.ui-entity-forms.js` pass. **Deferred.**

### `addAttrRow` / `getAttrRows`

Attr-editor DOM helpers used by `openEditModal` and `openAddEntityModal`. Also called externally as `UI.addAttrRow(...)` from inline `onclick` attributes in modal HTML. Moving them safely requires updating those HTML `onclick` strings. **Deferred (minor risk, self-contained).**

### `clearPanel()`

3-line DOM reset. Could be absorbed by `PanelController.reset()` in a future pass. Too small to warrant extraction on its own. **Deferred.**

### `DOMContentLoaded` composition root

Intentionally untouched. **Out of scope for this branch.**

---

## Pass 3 — Entity Form/Modal Extraction (2026-04-04)

### New file: `graphe.ui-entity-forms.js`

Factory: `createGrapheUiEntityForms({ document, State, Modals, escHtml })`  
Exported via: `window.createGrapheUiEntityForms`  
Instantiated as: `EntityForms` inside the `UI` IIFE (after `PanelActions`, before function declarations)

**Exported methods:**
- `openAddEntityModal()` — populates and opens `#modal-add-entity`
- `openEditModal(id)` — populates and opens `#modal-edit-entity`
- `addAttrRow(editorId, key, val)` — appends a key/value row to an attr-editor container
- `getAttrRows(editorId)` — reads all key/value pairs from an attr-editor container

**What was moved:**
All four function implementations, extracted verbatim. `openEditModal` internally calls `addAttrRow` directly (local reference, no `UI` indirection needed).

### Modified: `graphe.html` (Pass 3)

1. **Script load order** (line 19): added `<script src="graphe.ui-entity-forms.js"></script>` after `graphe.ui-panel-actions.js`.

2. **UI IIFE — EntityForms instantiation**: added after `PanelActions` declaration:
   ```javascript
   const EntityForms = window.createGrapheUiEntityForms({ document, State, Modals, escHtml });
   ```

3. **Four function bodies replaced with stubs** (~55 lines → 4 lines):
   ```javascript
   function openAddEntityModal()                 { EntityForms.openAddEntityModal(); }
   function openEditModal(id)                    { EntityForms.openEditModal(id); }
   function addAttrRow(editorId, key='', val='') { EntityForms.addAttrRow(editorId, key, val); }
   function getAttrRows(editorId)                { return EntityForms.getAttrRows(editorId); }
   ```

4. **Static modal HTML — NO CHANGE**: Lines ~1388 and ~1455 keep `onclick="UI.addAttrRow(...)"`. `UI.addAttrRow` is the stub that delegates to `EntityForms.addAttrRow`. Zero change to HTML.

---

## Current UI IIFE surface (post Pass 3)

The `UI` IIFE now contains only its irreducible coordination core:

| Function | Status | Reason kept inline |
|---|---|---|
| `renderTypeFilters` | Stub → `uiFilters` | Already delegated (Pass 1 ancestor) |
| `renderPanel` | Coordinator | DOM show/hide + PanelController calls |
| `clearPanel` | Inline | 3-line DOM reset; too small to extract alone |
| `selectEntity` | Inline | Calls `Graph.cy` — Graph not extracted |
| `openAddRelationModal` | Stub → `uiRelationsModal` | Already delegated |
| `openAddEntityModal` | Stub → `EntityForms` | ← Pass 3 |
| `openEditModal` | Stub → `EntityForms` | ← Pass 3 |
| `addAttrRow` | Stub → `EntityForms` | ← Pass 3 |
| `getAttrRows` | Stub → `EntityForms` | ← Pass 3 |
| `setupEntitySearch` | Stub → `uiSearch` | Already delegated |
| `confirmDeleteRelation` | Stub → `PanelActions` | ← Pass 2 |

---

## Script Load Order (post Pass 3)

```
graphe.helpers.js
graphe.state.js
graphe.validation-export.js
graphe.modals.js
graphe.panels.js
graphe.panel-render.js
graphe.ui-panel.js              ← Pass 1: pure HTML builder
graphe.ui-panel-actions.js      ← Pass 2: action wiring
graphe.ui-entity-forms.js       ← Pass 3: entity form/modal helpers
graphe.ui-filters.js
graphe.ui-search.js
graphe.ui-relations-modal.js
```

**Dependency rules:**
- `graphe.ui-entity-forms.js` has no dependency on other extracted modules. It only needs `State`, `Modals`, `escHtml`, `document` — all available at instantiation time inside the UI IIFE.
- It must load before the inline script block that runs the UI IIFE.

---

## Runtime Behavior

- **No behavioral change across all three passes.**
- `UI.addAttrRow` export is preserved; all three `onclick` callsites continue to work.
- `UI.openEditModal`, `UI.openAddEntityModal`, `UI.getAttrRows` exports are preserved and delegate correctly.
- `DOMContentLoaded` callsites (`UI.openAddEntityModal()`, `UI.getAttrRows(...)`) are unchanged.

---

## Recommended Next Safe Sub-step

The `UI` IIFE now contains only genuine coordination code. The only remaining extractable fragment is `clearPanel()` — but at 3 lines it is too small to warrant a standalone module. It could be folded into `PanelController.reset()` in a future `graphe.panels.js` update, or simply left as-is.

**The true next step is `selectEntity` — but this requires extracting or abstracting the `Graph` module first**, which is a separate, much larger effort. It is out of scope for this child branch.

This child branch (`feat/research-architecture-vnext-panel-deeper`) is now complete for its declared scope. The UI IIFE is reduced to its irreducible core. No further extractions in this branch are warranted without touching Graph or DOMContentLoaded.
