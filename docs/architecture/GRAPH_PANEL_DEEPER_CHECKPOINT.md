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

## What Remains Inline in graphe.html — and Why

### `renderPanel` event wiring

The click handlers for `.panel-rel-row`, `#panel-btn-edit`, `#panel-btn-addrel`, `#panel-btn-delete` remain inside `UI.renderPanel` in `graphe.html`.

**Why:** These handlers call `selectEntity`, `confirmDeleteRelation`, `openEditModal`, `openAddRelationModal`, and `Editor.deleteEntity` — all of which are either:
- Part of the `UI` IIFE itself (circular if extracted together), or
- Part of the inline `Editor` IIFE (not yet extracted).

Extracting them would require either event delegation with a callback-injection pattern, or extracting `Editor` first. Both are deferred to a future sub-step.

### `selectEntity(id)`

Calls `Graph.cy.animate()` and `Graph.highlightNeighbors()` — a direct dependency on the inline `Graph` module. This bidirectional coupling (`Graph` → `UI.renderPanel` on node tap, `UI.selectEntity` → `Graph`) cannot be resolved until the Graph module is extracted or an event bus is introduced.

### `confirmDeleteRelation(relIdx)` / `openEditModal(id)` / `openAddEntityModal()`

Form population and delete confirmation functions that manipulate DOM elements for modal forms (`#ee-attrs-editor`, `#ae-attrs-editor`, `#confirm-delete-msg`, etc.) and call `Editor.deleteRelation` / `Editor.deleteEntity`. These belong to a future `graphe.ui-entity-forms.js` or similar. Deferred.

### `clearPanel()`

Simple 3-line function. Could move to `PanelController.reset()` in a future pass. Left inline for now — not worth a migration on its own.

### `DOMContentLoaded` composition root

Intentionally untouched. The 650-line initialization block is out of scope for this extraction pass.

---

## Script Load Order (post-extraction)

```
graphe.helpers.js
graphe.state.js
graphe.validation-export.js
graphe.modals.js
graphe.panels.js
graphe.panel-render.js
graphe.ui-panel.js          ← new, must come after panel-render and before ui-filters
graphe.ui-filters.js
graphe.ui-search.js
graphe.ui-relations-modal.js
```

**Dependency rule:** `graphe.ui-panel.js` depends on `window.GraphePanelRender` (from `graphe.panel-render.js`) and is itself consumed by the inline `UI` IIFE. It must remain in this ordinal position.

---

## Runtime Behavior

- **No behavioral change.** The HTML output of `buildPanelBodyHtml` is identical to the original inline template literal.
- Panel lifecycle (open, close, drag, resize) is unchanged.
- Event wiring is unchanged.
- Story mode node selection path (`StoryMode → Graph tap → UI.renderPanel`) is unchanged.
- All modal trigger paths are unchanged.

---

## Recommended Next Safe Sub-step

**Option A — Extract event wiring with callback injection**

Create `graphe.ui-panel-actions.js` with a factory:
```javascript
createGrapheUiPanelActions({
  document, State, Modals,
  onSelectEntity, onEditEntity, onAddRelation, onDeleteEntity, onDeleteRelation
})
```
This wires the panel button/row event listeners after `body.innerHTML` is set, using injected callbacks for the Editor and selectEntity dependencies. This resolves the remaining coupling without extracting `Editor` or `selectEntity` prematurely.

**Option B — Extract `openAddEntityModal` / `openEditModal` / `addAttrRow` / `getAttrRows` as `graphe.ui-entity-forms.js`**

Scope: form population helpers for the Add Entity and Edit Entity modals.  
Dependency: `State`, `Modals`, `escHtml`, `document`.  
No dependency on `Graph` or `selectEntity`.  
Safe, but smaller yield than Option A.

**Option A is recommended** — it completes the `renderPanel` extraction surface and creates a clean boundary for the Editor extraction that follows.
