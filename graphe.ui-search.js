/**
 * UI entity search helper extracted from graphe.html.
 * Scope intentionally limited to setupEntitySearch.
 */
(function attachUiSearchFactory(globalObj) {
  function createGrapheUiSearch({ document, State, TYPE_COLORS, escHtml }) {
    function setupEntitySearch(inputId, suggestId, hiddenId, previewId) {
      const input = document.getElementById(inputId);
      const suggest = document.getElementById(suggestId);
      const hidden = document.getElementById(hiddenId);
      const preview = document.getElementById(previewId);

      input.addEventListener('input', () => {
        const q = input.value.toLowerCase().trim();
        suggest.innerHTML = '';
        if (!q) { suggest.style.display = 'none'; return; }
        const matches = State.data.entities.filter((e) => e.name.toLowerCase().includes(q)).slice(0, 12);
        if (!matches.length) { suggest.style.display = 'none'; return; }
        matches.forEach((e) => {
          const typeName = State.getEntityTypeName(e);
          const color = TYPE_COLORS[typeName] || '#64748b';
          const item = document.createElement('div');
          item.style.cssText = 'padding:6px 10px;cursor:pointer;font-size:0.82em;display:flex;gap:6px;align-items:center;';
          const dot = document.createElement('div');
          dot.style.cssText = `width:8px;height:8px;border-radius:50%;background:${color};flex-shrink:0`;
          item.appendChild(dot);
          item.appendChild(document.createTextNode(e.name));
          const typeSpan = document.createElement('span');
          typeSpan.style.cssText = 'color:var(--text2);font-size:0.85em';
          typeSpan.textContent = typeName;
          item.appendChild(typeSpan);
          item.addEventListener('mouseenter', () => { item.style.background = 'var(--bg2)'; });
          item.addEventListener('mouseleave', () => { item.style.background = ''; });
          item.addEventListener('click', () => {
            input.value = e.name;
            hidden.value = e.id;
            preview.textContent = `✓ ${e.name} [${typeName}]`;
            suggest.style.display = 'none';
          });
          suggest.appendChild(item);
        });
        suggest.style.display = 'block';
      });
      input.addEventListener('blur', () => setTimeout(() => { suggest.style.display = 'none'; }, 200));
    }

    return { setupEntitySearch };
  }

  globalObj.createGrapheUiSearch = createGrapheUiSearch;
})(window);
