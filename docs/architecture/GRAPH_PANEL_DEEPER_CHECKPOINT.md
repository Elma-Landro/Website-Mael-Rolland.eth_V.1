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

## Script Load Order (post Pass 2)

```
graphe.helpers.js
graphe.state.js
graphe.validation-export.js
graphe.modals.js
graphe.panels.js
graphe.panel-render.js
graphe.ui-panel.js              ← Pass 1: pure HTML builder
graphe.ui-panel-actions.js      ← Pass 2: action wiring
graphe.ui-filters.js
graphe.ui-search.js
graphe.ui-relations-modal.js
```

**Dependency rules:**
- `graphe.ui-panel-actions.js` depends on `window.createGrapheUiPanelActions` being available when the `UI` IIFE runs; it must load before the inline script block.
- It has no dependency on `graphe.ui-panel.js` (they are siblings).

---

## Runtime Behavior

- **No behavioral change across both passes.** HTML output, event responses, panel lifecycle, modal flows, and story-mode node selection are all identical to the pre-extraction state.
- `UI.confirmDeleteRelation` is still exported and still functions identically.
- The `UI.renderPanel` function signature and all external call sites are unchanged.

---

## Recommended Next Safe Sub-step

**Extract `openEditModal` / `openAddEntityModal` / `addAttrRow` / `getAttrRows` as `graphe.ui-entity-forms.js`**

Scope: form population and attr-editor helpers for the Add Entity and Edit Entity modals.  
Dependencies: `State`, `Modals`, `escHtml`, `document`.  
No dependency on `Graph`, `selectEntity`, or `PanelActions`.  
Risk: `UI.addAttrRow` is called from inline `onclick` attributes in modal HTML — those two `onclick` strings must be updated simultaneously (simple find/replace, low risk).

This pass would reduce the `UI` IIFE to its irreducible coordination core: `renderTypeFilters`, `renderPanel`, `clearPanel`, `selectEntity`, `setupEntitySearch`, and the module's return statement.
