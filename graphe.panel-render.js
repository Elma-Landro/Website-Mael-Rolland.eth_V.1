/**
 * Tiny panel-render helpers extracted from UI.renderPanel in graphe.html.
 * Scope intentionally limited to pure/local attribute formatting helpers.
 */
(function attachPanelRenderHelpers(globalObj) {
  function splitPanelAttributes(attrs = {}, escHtml) {
    const sourceLinks = [];
    const regularAttrs = [];

    for (const [k, v] of Object.entries(attrs)) {
      const val = typeof v === 'object' ? (v.value || '') : String(v);
      if (/^(sourcePage|pdfPage|page|pageRef|pdfQuote)$/i.test(k)) {
        const pageNum = parseInt(val, 10);
        if (!Number.isNaN(pageNum)) {
          sourceLinks.push(`<a class="panel-source-link" href="these-mael-rolland.pdf#page=${pageNum}" target="_blank" rel="noopener">📄 p.${pageNum}</a>`);
        } else if (val.trim()) {
          sourceLinks.push(`<span class="panel-source-link" style="cursor:default">${escHtml(val)}</span>`);
        }
      } else {
        const isUrl = k.toLowerCase().includes('url')
          || k.toLowerCase().includes('website')
          || k.toLowerCase().includes('link')
          || val.startsWith('http');
        regularAttrs.push({ k, val, isUrl });
      }
    }

    return { sourceLinks, regularAttrs };
  }

  function buildAttrsHtml(regularAttrs = [], escHtml) {
    if (!regularAttrs.length) return '';
    return `<details class="panel-details-block">
           <summary>Attributs (${regularAttrs.length})</summary>
           ${regularAttrs.map(({ k, val, isUrl }) => `
             <div class="attr-row-inline">
               <span class="attr-key-inline">${escHtml(k)}</span>
               <span class="attr-val-inline">${isUrl ? `<a href="${escHtml(val)}" target="_blank" rel="noopener">${escHtml(val)}</a>` : escHtml(val)}</span>
             </div>`).join('')}
         </details>`;
  }

  globalObj.GraphePanelRender = {
    splitPanelAttributes,
    buildAttrsHtml,
  };
})(window);
