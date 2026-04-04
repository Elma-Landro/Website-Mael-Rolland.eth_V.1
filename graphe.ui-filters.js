/**
 * UI filters helper extracted from graphe.html.
 * Scope intentionally limited to renderTypeFilters.
 */
(function attachUiFiltersFactory(globalObj) {
  function createGrapheUiFilters({ document, State, Graph, TYPE_COLORS }) {
    function renderTypeFilters() {
      const data = State.data;
      if (!data) return;
      const container = document.getElementById('type-filters');
      container.innerHTML = '';
      // Count entities by type
      const counts = {};
      for (const e of data.entities) {
        for (const tid of (e.types || [])) {
          counts[tid] = (counts[tid] || 0) + 1;
        }
      }
      for (const t of data.types) {
        const color = TYPE_COLORS[t.name] || '#64748b';
        const count = counts[t.id] || 0;
        const hidden = State.hiddenTypes.has(t.name);
        const item = document.createElement('div');
        item.className = 'type-filter-item';
        item.style.opacity = hidden ? '0.4' : '1';
        item.innerHTML = `
        <input type="checkbox" ${hidden ? '' : 'checked'} data-typename="${t.name}" style="display:none">
        <div class="type-dot" style="background:${color}"></div>
        <span class="type-label">${t.name}</span>
        <span class="type-count">${count}</span>
      `;
        item.addEventListener('click', () => {
          if (State.hiddenTypes.has(t.name)) State.hiddenTypes.delete(t.name);
          else State.hiddenTypes.add(t.name);
          renderTypeFilters();
          Graph.applyFilters();
        });
        container.appendChild(item);
      }
    }

    return { renderTypeFilters };
  }

  globalObj.createGrapheUiFilters = createGrapheUiFilters;
})(window);
