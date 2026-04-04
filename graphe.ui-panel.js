// graphe.ui-panel.js
// Pure panel body HTML builder — no DOM writes, no event listeners, no Graph calls.
// Extracted from the inline UI.renderPanel() in graphe.html.
//
// Consumed by: UI.renderPanel (graphe.html inline)
// Dependencies: State, GraphePanelRender (window.GraphePanelRender), escHtml, TYPE_COLORS
//
// What this module does NOT do (kept in graphe.html by design):
//   - DOM writes (body.innerHTML, classList)
//   - PanelController.open() / setMeta()
//   - Event listener wiring (.panel-rel-row, panel-btn-edit, etc.)
//   - selectEntity() calls (depends on Graph — circular)
//   - Editor action calls (deleteEntity, deleteRelation)
//   - confirmDeleteRelation / openEditModal / openAddRelationModal

(function () {
  'use strict';

  function createGrapheUiPanel({ State, GraphePanelRender, escHtml, TYPE_COLORS }) {

    // ── Single relation row ───────────────────────────────────────────────
    function _relRow(rel, dir) {
      const otherId = dir === 'out' ? rel.to : rel.from;
      const other = State.maps.entities[otherId];
      const otherName = other ? other.name : '⚠ ' + otherId.slice(0, 8);
      const otherType = other ? State.getEntityTypeName(other) : 'Unknown';
      const otherColor = TYPE_COLORS[otherType] || '#64748b';
      const relIdx = State.data.relations.indexOf(rel);
      const arrow = dir === 'out' ? '→' : '←';
      return `<div class="panel-rel-row" data-goto="${otherId}">
        <span class="panel-rel-dir">${arrow}</span>
        <span class="panel-rel-entity" style="color:${otherColor}">${escHtml(otherName)}</span>
        <span class="panel-rel-del" data-relidx="${relIdx}" title="Supprimer">×</span>
      </div>`;
    }

    // ── Full panel body HTML ──────────────────────────────────────────────
    // Returns an HTML string ready for body.innerHTML assignment.
    // Returns '' if the entity is not found.
    function buildPanelBodyHtml(id) {
      const entity = State.maps.entities[id];
      if (!entity) return '';

      const typeName = State.getEntityTypeName(entity);
      const color = TYPE_COLORS[typeName] || '#64748b';
      const desc = State.getEntityDesc(entity);
      const outgoing = State.maps.outgoing[id] || [];
      const incoming = State.maps.incoming[id] || [];

      // ── Separate sources from regular attributes ──────────────────────
      const attrs = entity.attributes || {};
      const { sourceLinks, regularAttrs } = GraphePanelRender.splitPanelAttributes(attrs, escHtml);

      const sourcesHtml = sourceLinks.length
        ? `<details class="panel-details-block" open>
           <summary>Sources (${sourceLinks.length})</summary>
           <div class="panel-sources-wrap">${sourceLinks.join('')}</div>
         </details>`
        : '';

      const attrsHtml = GraphePanelRender.buildAttrsHtml(regularAttrs, escHtml);

      // ── Relations groupées par type ───────────────────────────────────
      const totalRels = outgoing.length + incoming.length;
      let relsHtml;
      if (totalRels) {
        const grouped = {};
        const addToGroup = (rel, dir) => {
          const rtObj = State.maps.relTypes[rel.type];
          const rtName = rtObj ? rtObj.name : rel.type;
          const key = rtName + '|' + dir;
          if (!grouped[key]) grouped[key] = { rtName, dir, rows: [] };
          grouped[key].rows.push(_relRow(rel, dir));
        };
        outgoing.forEach(r => addToGroup(r, 'out'));
        incoming.forEach(r => addToGroup(r, 'in'));

        const groupsHtml = Object.values(grouped).map(g => `
        <div class="panel-rel-group">
          <div class="panel-rel-group-title">
            <span class="panel-rel-dir-label">${g.dir === 'out' ? '→' : '←'}</span>
            <span class="panel-rel-type">${escHtml(g.rtName)}</span>
            <span class="panel-rel-count">(${g.rows.length})</span>
          </div>
          ${g.rows.join('')}
        </div>`).join('');

        relsHtml = `<details class="panel-details-block">
           <summary>Relations (${totalRels})</summary>
           ${groupsHtml}
         </details>`;
      } else {
        relsHtml = `<details class="panel-details-block">
           <summary>Relations</summary>
           <span style="color:var(--text2);font-size:0.8em">Aucune relation</span>
         </details>`;
      }

      return `
      <div>
        <div class="panel-type-badge" style="background:${color}22;color:${color};border:1px solid ${color}44">
          <div class="type-dot" style="background:${color}"></div>${escHtml(typeName)}
        </div>
      </div>
      <div>
        <div class="panel-name">${escHtml(entity.name)}</div>
        <div class="panel-desc" style="margin-top:6px">${desc ? escHtml(desc) : '<em style="opacity:.5">Pas de description</em>'}</div>
      </div>
      <div class="panel-summary-grid">
        <div class="panel-summary-item"><span class="panel-summary-label">Relations</span><span class="panel-summary-value">${totalRels}</span></div>
        <div class="panel-summary-item"><span class="panel-summary-label">Attributs</span><span class="panel-summary-value">${regularAttrs.length}</span></div>
      </div>
      ${sourcesHtml}
      ${attrsHtml}
      ${relsHtml}
      <hr class="panel-hr">
      <div class="panel-actions">
        <button class="btn-secondary btn-sm" id="panel-btn-edit">✏️ Modifier</button>
        <button class="btn-secondary btn-sm" id="panel-btn-addrel">+ Relation</button>
        <button class="btn-danger btn-sm" id="panel-btn-delete">🗑 Supprimer</button>
      </div>
      <div style="font-size:0.68em;color:var(--text2);font-family:var(--mono);margin-top:4px">${entity.id}</div>
    `;
    }

    return { buildPanelBodyHtml };
  }

  window.createGrapheUiPanel = createGrapheUiPanel;
})();
