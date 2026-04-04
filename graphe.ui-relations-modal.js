/**
 * UI relation modal helper extracted from graphe.html.
 * Scope intentionally limited to openAddRelationModal.
 */
(function attachUiRelationsModalFactory(globalObj) {
  function createGrapheUiRelationsModal({ document, State, Modals }) {
    function openAddRelationModal(prefillFromId) {
      const sel = document.getElementById('ar-type');
      sel.innerHTML = '';
      for (const rt of State.data.relation_types) {
        const opt = document.createElement('option');
        opt.value = rt.id; opt.textContent = rt.name;
        sel.appendChild(opt);
      }
      document.getElementById('ar-from-id').value = '';
      document.getElementById('ar-to-id').value = '';
      document.getElementById('ar-from-preview').textContent = '';
      document.getElementById('ar-to-preview').textContent = '';
      document.getElementById('ar-from-search').value = '';
      document.getElementById('ar-to-search').value = '';
      if (prefillFromId && State.maps.entities[prefillFromId]) {
        const e = State.maps.entities[prefillFromId];
        document.getElementById('ar-from-id').value = prefillFromId;
        document.getElementById('ar-from-search').value = e.name;
        document.getElementById('ar-from-preview').textContent = `✓ ${e.name}`;
      }
      Modals.open('modal-add-relation');
    }

    return { openAddRelationModal };
  }

  globalObj.createGrapheUiRelationsModal = createGrapheUiRelationsModal;
})(window);
