// graphe.ui-panel-actions.js
// Post-render panel action wiring — event listeners for relation rows and action buttons.
// Extracted from the inline event-wiring block in UI.renderPanel (graphe.html).
//
// Consumed by: UI (graphe.html inline IIFE) via PanelActions.wirePanel / PanelActions.confirmDeleteRelation
//
// What this module does NOT do (kept in graphe.html by design):
//   - selectEntity() logic (depends on Graph.cy — circular coupling with Graph module)
//   - Editor CRUD operations (Editor not yet extracted; passed as execute callbacks)
//   - PanelController.open() / setMeta() (panel lifecycle stays in renderPanel coordinator)
//   - openEditModal / openAddRelationModal implementation (UI form-population logic, not yet extracted)
//   - DOMContentLoaded wiring (composition root untouched)
//
// Dependency injection rationale:
//   onSelectEntity        — avoids direct Graph coupling (selectEntity calls Graph.cy)
//   onEditEntity          — avoids depending on inline openEditModal form-population logic
//   onAddRelation         — avoids depending on inline openAddRelationModal / uiRelationsModal
//   onExecuteDeleteEntity — avoids importing inline Editor IIFE
//   onExecuteDeleteRelation — same

(function () {
  'use strict';

  function createGrapheUiPanelActions({
    document,
    State,
    Modals,
    onSelectEntity,
    onEditEntity,
    onAddRelation,
    onExecuteDeleteEntity,
    onExecuteDeleteRelation,
  }) {

    // ── Relation delete confirmation modal ────────────────────────────────
    function confirmDeleteRelation(relIdx) {
      const rel = State.data.relations[relIdx];
      if (!rel) return;
      const rt = State.maps.relTypes[rel.type];
      const from = State.maps.entities[rel.from];
      const to = State.maps.entities[rel.to];
      document.getElementById('confirm-delete-msg').textContent =
        `Supprimer la relation « ${rt ? rt.name : rel.type} » de « ${from ? from.name : rel.from} » vers « ${to ? to.name : rel.to} » ?`;
      document.getElementById('confirm-delete-btn').onclick = () => {
        onExecuteDeleteRelation(relIdx);
        Modals.close('modal-confirm-delete');
      };
      Modals.open('modal-confirm-delete');
    }

    // ── Wire all post-render action handlers on the panel body ────────────
    // Called by UI.renderPanel immediately after body.innerHTML is set.
    function wirePanel(body, entityId) {
      // Relation rows: navigate or delete
      body.querySelectorAll('.panel-rel-row').forEach(row => {
        row.addEventListener('click', e => {
          if (e.target.classList.contains('panel-rel-del')) {
            const idx = parseInt(e.target.dataset.relidx);
            confirmDeleteRelation(idx);
            e.stopPropagation();
            return;
          }
          const gotoId = row.dataset.goto;
          if (gotoId && State.maps.entities[gotoId]) {
            onSelectEntity(gotoId);
          }
        });
      });

      // Edit entity button
      document.getElementById('panel-btn-edit').addEventListener('click', () => onEditEntity(entityId));

      // Add relation button
      document.getElementById('panel-btn-addrel').addEventListener('click', () => onAddRelation(entityId));

      // Delete entity button — opens shared confirm modal
      document.getElementById('panel-btn-delete').addEventListener('click', () => {
        const entity = State.maps.entities[entityId];
        const rels = (State.maps.outgoing[entityId] || []).length + (State.maps.incoming[entityId] || []).length;
        document.getElementById('confirm-delete-msg').textContent =
          `Supprimer « ${entity ? entity.name : entityId} » ? Cette action supprimera aussi ${rels} relation(s) liée(s).`;
        document.getElementById('confirm-delete-btn').onclick = () => {
          onExecuteDeleteEntity(entityId);
          Modals.close('modal-confirm-delete');
        };
        Modals.open('modal-confirm-delete');
      });
    }

    return { wirePanel, confirmDeleteRelation };
  }

  window.createGrapheUiPanelActions = createGrapheUiPanelActions;
})();
