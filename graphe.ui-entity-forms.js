// graphe.ui-entity-forms.js
// Entity form/modal helpers — Add Entity, Edit Entity, attr-editor rows.
// Extracted from the inline UI IIFE in graphe.html (Pass 3).
//
// Consumed by: UI (graphe.html inline IIFE) via EntityForms.* stubs
// Dependencies: document, State, Modals, escHtml
//
// What this module does NOT do (kept in graphe.html by design):
//   - openAddRelationModal — already delegated to uiRelationsModal (graphe.ui-relations-modal.js)
//   - selectEntity / renderPanel / clearPanel — coordinate Graph; untouched
//   - Editor CRUD calls — Editor IIFE not yet extracted
//   - DOMContentLoaded wiring — composition root untouched
//
// Note on UI.addAttrRow onclick strings:
//   Static modal HTML (lines ~1387, ~1454) and the openAddEntityModal innerHTML template
//   all call onclick="UI.addAttrRow(...)". The UI.addAttrRow stub in graphe.html delegates
//   here, so those onclick strings require no modification.

(function () {
  'use strict';

  function createGrapheUiEntityForms({ document, State, Modals, escHtml }) {

    // ── Attr-editor: append a key/value row ───────────────────────────────
    function addAttrRow(editorId, key, val) {
      if (key === undefined) key = '';
      if (val === undefined) val = '';
      const editor = document.getElementById(editorId);
      const row = document.createElement('div');
      row.className = 'attr-edit-row';
      row.innerHTML = `
      <input type="text" class="field-input" placeholder="clé" value="${escHtml(key)}" style="max-width:120px">
      <input type="text" class="field-input" placeholder="valeur" value="${escHtml(val)}">
      <button class="btn-danger btn-sm" onclick="this.parentElement.remove()">–</button>
    `;
      editor.appendChild(row);
    }

    // ── Attr-editor: read all key/value rows ──────────────────────────────
    function getAttrRows(editorId) {
      const rows = document.querySelectorAll(`#${editorId} .attr-edit-row`);
      const result = [];
      rows.forEach(row => {
        const inputs = row.querySelectorAll('input');
        if (inputs.length >= 2) result.push([inputs[0].value, inputs[1].value]);
      });
      return result;
    }

    // ── Add Entity modal: populate and open ───────────────────────────────
    function openAddEntityModal() {
      const sel = document.getElementById('ae-type');
      sel.innerHTML = '';
      for (const t of State.data.types) {
        const opt = document.createElement('option');
        opt.value = t.id; opt.textContent = t.name;
        sel.appendChild(opt);
      }
      document.getElementById('ae-name').value = '';
      document.getElementById('ae-desc').value = '';
      // UI.addAttrRow resolved at click time via the UI stub; UI is a global const.
      document.getElementById('ae-attrs-editor').innerHTML = `
      <div class="attr-edit-row">
        <input type="text" class="field-input" placeholder="clé" style="max-width:110px">
        <input type="text" class="field-input" placeholder="valeur">
        <button class="btn-secondary btn-sm" onclick="UI.addAttrRow('ae-attrs-editor')">+</button>
      </div>`;
      Modals.open('modal-add-entity');
    }

    // ── Edit Entity modal: populate and open ──────────────────────────────
    function openEditModal(id) {
      const entity = State.maps.entities[id];
      if (!entity) return;
      document.getElementById('ee-id').value = id;

      const sel = document.getElementById('ee-type');
      sel.innerHTML = '';
      for (const t of State.data.types) {
        const opt = document.createElement('option');
        opt.value = t.id; opt.textContent = t.name;
        if (entity.types && entity.types.includes(t.id)) opt.selected = true;
        sel.appendChild(opt);
      }

      document.getElementById('ee-name').value = entity.name || '';
      const desc = entity.description;
      document.getElementById('ee-desc').value = desc ? (desc.value || '') : '';
      document.getElementById('ee-lang').value = desc && desc.options ? (desc.options.language || 'fr') : 'fr';

      const attrsEditor = document.getElementById('ee-attrs-editor');
      attrsEditor.innerHTML = '';
      const attrs = entity.attributes || {};
      for (const [k, v] of Object.entries(attrs)) {
        const val = typeof v === 'object' ? (v.value || '') : String(v);
        addAttrRow('ee-attrs-editor', k, val);
      }
      if (Object.keys(attrs).length === 0) addAttrRow('ee-attrs-editor');

      Modals.open('modal-edit-entity');
    }

    return { openAddEntityModal, openEditModal, addAttrRow, getAttrRows };
  }

  window.createGrapheUiEntityForms = createGrapheUiEntityForms;
})();
