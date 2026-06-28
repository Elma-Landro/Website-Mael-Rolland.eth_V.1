/**
 * Graph styles helper extracted from graphe.html.
 * Scope intentionally limited to Cytoscape style construction.
 */
(function attachGraphStylesFactory(globalObj) {
  function createGrapheGraphStyles({ TYPE_COLORS, isMobileViewport }) {
    // Explicit DI kept for extraction boundary clarity (TYPE_COLORS reserved for style evolution).
    void TYPE_COLORS;

    const LABEL_FONT_SIZE_BASE = isMobileViewport ? '13px' : '11px';
    const LABEL_FONT_SIZE_MAJOR = isMobileViewport ? '15px' : '12px';
    const LABEL_FONT_SIZE_ALWAYS = isMobileViewport ? '16px' : '14px';
    const LABEL_MAX_WIDTH = isMobileViewport ? 220 : 190;
    const LABEL_WRAP_MAX_WIDTH = isMobileViewport ? 210 : 180;
    const LABEL_BG_COLOR = isMobileViewport ? 'rgba(8,10,16,0.86)' : 'rgba(0,0,0,0.74)';
    const LABEL_BG_OPACITY = isMobileViewport ? 0.96 : 0.92;
    const LABEL_BG_PADDING = isMobileViewport ? 5 : 4;
    const LABEL_OUTLINE_WIDTH = isMobileViewport ? 5 : 4;

    const buildLabelStyle = (overrides = {}) => ({
      'label': 'data(label)',
      'text-wrap': 'wrap',
      'text-overflow-wrap': 'anywhere',
      'text-background-shape': 'roundrectangle',
      ...overrides,
    });

    return [
      {
        selector: 'node',
        style: {
          'background-color': 'data(color)',
          'background-opacity': 0.85,
          'shape': 'data(shape)',
          'width': 'data(size)', 'height': 'data(size)',
          'label': '',
          'font-family': 'VT323, monospace',
          'font-size': LABEL_FONT_SIZE_BASE,
          'color': 'data(labelColor)',
          'text-valign': 'bottom', 'text-halign': 'center',
          'text-margin-y': 6,
          'text-outline-color': '#000000', 'text-outline-width': LABEL_OUTLINE_WIDTH,
          'border-width': 0,
          'overlay-padding': 6,
          'shadow-blur':     0,
          'shadow-opacity':  0,
          'shadow-offset-x': 0,
          'shadow-offset-y': 0,
        }
      },
      // ── Labels only visible when zoomed in (class toggled by zoom handler) ──
      {
        selector: 'node.show-label',
        style: buildLabelStyle({
          'font-size': LABEL_FONT_SIZE_BASE,
          'text-max-width': LABEL_WRAP_MAX_WIDTH,
          'text-outline-width': LABEL_OUTLINE_WIDTH,
          'text-background-color': LABEL_BG_COLOR,
          'text-background-opacity': LABEL_BG_OPACITY,
          'text-background-padding': LABEL_BG_PADDING
        })
      },
      // ── Progressive reveal: major names appear first ──
      {
        selector: 'node.show-major-label',
        style: buildLabelStyle({
          'font-size': LABEL_FONT_SIZE_MAJOR,
          'text-max-width': LABEL_MAX_WIDTH,
          'text-outline-width': LABEL_OUTLINE_WIDTH + 0.5,
          'text-background-color': LABEL_BG_COLOR,
          'text-background-opacity': Math.min(0.98, LABEL_BG_OPACITY + 0.02),
          'text-background-padding': LABEL_BG_PADDING
        })
      },
      // ── Always-visible labels (Vue Monétisation — key nodes) ──────────────
      {
        selector: 'node.always-label',
        style: buildLabelStyle({
          'font-size': LABEL_FONT_SIZE_ALWAYS, 'font-family': 'VT323, monospace',
          'text-outline-width': LABEL_OUTLINE_WIDTH + 1,
          'text-max-width': LABEL_MAX_WIDTH,
          'text-background-color': LABEL_BG_COLOR,
          'text-background-opacity': Math.min(0.99, LABEL_BG_OPACITY + 0.03),
          'text-background-padding': LABEL_BG_PADDING + 1
        })
      },
      // ── Chapter glow halos — override shadow color/opacity even sans in-nebula ──
      { selector: 'node.chapter-0', style: { 'shadow-color': '#00ccff', 'shadow-blur': 30, 'shadow-opacity': 0.62 } },
      { selector: 'node.chapter-1', style: { 'shadow-color': '#ff8800', 'shadow-blur': 30, 'shadow-opacity': 0.62 } },
      { selector: 'node.chapter-2', style: { 'shadow-color': '#33ff33', 'shadow-blur': 30, 'shadow-opacity': 0.62 } },
      { selector: 'node.chapter-3', style: { 'shadow-color': '#aa44ff', 'shadow-blur': 30, 'shadow-opacity': 0.62 } },
      { selector: 'node.chapter-4', style: { 'shadow-color': '#ff44aa', 'shadow-blur': 30, 'shadow-opacity': 0.62 } },
      // ── Archipelago: other islands fade when zoomed ───────
      { selector: 'node.chapter-faded', style: { 'opacity': 0.05 } },
      // ── Chapter label ghost nodes (floating title above each island) ──
      {
        selector: 'node.chapter-label',
        style: buildLabelStyle({
          'background-opacity': 0, 'border-opacity': 0,
          'width': 2, 'height': 2,
          'font-family': "'VT323', monospace",
          'font-size': 'data(labelSize)',
          'color': 'data(labelColor)',
          'text-valign': 'center', 'text-halign': 'data(labelHalign)',
          'text-outline-color': '#000', 'text-outline-width': 3.5,
          'text-max-width': 260,
          'text-background-color': 'rgba(0,0,0,0.62)',
          'text-background-opacity': 0.90,
          'text-background-padding': 3,
          'events': 'no',
        })
      },
      // ── Type column labels (matrice layout) ──────────────
      {
        selector: 'node.type-label',
        style: buildLabelStyle({
          'background-opacity': 0, 'border-opacity': 0,
          'width': 2, 'height': 2,
          'font-family': "'VT323', monospace",
          'font-size': 'data(labelSize)',
          'color': 'data(labelColor)',
          'text-rotation': 'data(labelRotation)',
          'text-valign': 'center', 'text-halign': 'center',
          'text-outline-color': '#000', 'text-outline-width': 3,
          'text-max-width': 260,
          'text-background-color': 'rgba(0,0,0,0.64)',
          'text-background-opacity': 0.90,
          'text-background-padding': 3,
          'events': 'no',
        })
      },
      {
        selector: 'node:selected',
        style: {
          'border-width': 3, 'border-color': '#ffcc66',
          'border-opacity': 1,
        }
      },
      {
        selector: 'node.highlighted',
        style: { 'border-width': 2, 'border-color': '#ffcc66', 'border-opacity': 1 }
      },
      {
        selector: 'node.story-primary',
        style: {
          'opacity': 1,
          'border-width': 3,
          'border-color': '#ffcc66',
          'border-opacity': 1,
          'z-index': 30
        }
      },
      {
        selector: 'node.story-secondary',
        style: {
          'opacity': 0.5,
          'border-width': 1.5,
          'border-color': '#ffb347',
          'border-opacity': 0.7,
          'z-index': 18
        }
      },
      {
        selector: 'node.story-muted',
        style: { 'opacity': 0.08, 'z-index': 1 }
      },
      {
        selector: 'node.story-hidden',
        style: { 'display': 'none' }
      },
      {
        selector: 'node.hop2',
        style: { 'border-width': 2, 'border-color': '#ff8800', 'border-opacity': 0.75, 'opacity': 0.70 }
      },
      // ── Matrix grid mode: tiny dots, subtle glow, labels appear on zoom ──────
      {
        selector: 'node.in-matrix',
        style: {
          'width': 'data(msize)', 'height': 'data(msize)', // msize = adaptatif mobile/desktop
          'shape': 'data(shape)', // conserve la différenciation morphologique des types
          // Glow dynamique proportionnel à la taille affichée (msize), y compris en mobile.
          'shadow-blur':    'mapData(msize, 7, 120, 10, 130)',
          'shadow-opacity': 'mapData(msize, 7, 120, 0.42, 0.96)',
          'shadow-color': 'data(color)',
          'shadow-offset-x': 0, 'shadow-offset-y': 0,
          'background-opacity': 0.85,
          'z-index': 2,
        }
      },
      // ── Arêtes matrix : cachées par défaut, révélées au clic ────────────
      // 19 000+ arêtes × opacity > 0 = fond solide par cumul → display:none obligatoire.
      // Au clic, edge.in-matrix.highlighted révèle les connexions directes.
      {
        selector: 'edge.in-matrix',
        style: { 'display': 'none' }
      },
      {
        selector: 'edge.in-matrix.highlighted',
        style: {
          'display': 'element',
          'opacity': 0.22,
          'line-color': 'source-data(color)',
          'target-arrow-color': 'source-data(color)',
          'target-arrow-shape': 'triangle',
          'width': 0.7,
        }
      },
      // ── Column halos: transparent color band per type column ──
      {
        selector: 'node.col-halo',
        style: {
          'shape': 'rectangle',
          'background-color': 'data(color)',
          'background-opacity': 0.028,
          'border-opacity': 0,
          'label': '',
          'events': 'no',
          'shadow-blur': 16, 'shadow-color': 'data(color)', 'shadow-opacity': 0.05,
          'z-index': 0,
        }
      },
      {
        selector: 'node.faded',
        style: { 'opacity': 0.20 }
      },
      {
        selector: 'node.hidden-type',
        style: { 'display': 'none' }
      },
      {
        selector: 'node.scrolly-hidden',
        style: { 'display': 'none' }
      },
      {
        selector: 'node.search-hidden',
        style: { 'display': 'none' }
      },
      {
        selector: 'edge',
        style: {
          'width': 0.5,
          'line-color': '#33ff33',
          'target-arrow-color': '#33ff33',
          'target-arrow-shape': 'triangle',
          'curve-style': 'bezier',
          'arrow-scale': 0.3,
          'opacity': 0.28,
        }
      },
      {
        selector: 'edge.highlighted',
        style: { 'line-color': '#ffcc66', 'target-arrow-color': '#ffcc66', 'opacity': 0.90, 'width': 1 }
      },
      {
        // Clic sur nœud en story mode : sélecteur double > priorité sur story-hidden (display:none)
        selector: 'edge.story-hidden.highlighted',
        style: { 'display': 'element', 'line-color': '#ffcc66', 'target-arrow-color': '#ffcc66', 'opacity': 0.82, 'width': 1.1, 'z-index': 30 }
      },
      {
        selector: 'edge.story-primary',
        style: {
          'display': 'element',
          'line-color': '#ffcc66',
          'target-arrow-color': '#ffcc66',
          'opacity': 0.78,
          'width': 1.2,
          'z-index': 24
        }
      },
      {
        // P→S : liaisons primaire-secondaire — modérément visibles
        selector: 'edge.story-secondary',
        style: {
          'display': 'element',
          'line-color': '#ffb347',
          'target-arrow-color': '#ffb347',
          'opacity': 0.11,
          'width': 0.42,
          'z-index': 12
        }
      },
      {
        // S→S : liaisons entre nœuds secondaires — quasi-invisibles (contexte seulement)
        selector: 'edge.story-tertiary',
        style: {
          'display': 'element',
          'line-color': '#886644',
          'target-arrow-color': '#886644',
          'opacity': 0.05,
          'width': 0.28,
          'z-index': 5
        }
      },
      {
        // Nœuds-ponts — couture visuelle entre scènes, tirets verts
        selector: 'node.story-bridge',
        style: {
          'opacity': 0.42,
          'border-width': 1.5,
          'border-color': '#33ff33',
          'border-opacity': 0.55,
          'border-style': 'dashed',
          'z-index': 12
        }
      },
      {
        // Arêtes-ponts — connexions vers les nœuds de couture, pointillés
        selector: 'edge.story-bridge',
        style: {
          'display': 'element',
          'line-color': '#33ff33',
          'target-arrow-color': '#33ff33',
          'opacity': 0.20,
          'width': 0.55,
          'line-style': 'dashed',
          'line-dash-pattern': [4, 6],
          'z-index': 8
        }
      },
      {
        selector: 'edge.story-backbone',
        style: {
          'display': 'element',
          'line-color': '#ffe2a8',
          'target-arrow-color': '#ffe2a8',
          'opacity': 0.035,
          'width': 0.24,
          'z-index': 3
        }
      },
      {
        selector: 'edge.story-hidden',
        style: { 'display': 'none' }
      },
      {
        selector: 'edge.hop2',
        style: { 'line-color': '#ff8800', 'target-arrow-color': '#ff8800', 'opacity': 0.07, 'width': 0.4 }
      },
      {
        selector: 'edge.faded',
        style: { 'opacity': 0.06 }
      },
      {
        selector: 'edge.scrolly-hidden',
        style: { 'display': 'none' }
      },
      {
        selector: 'edge.scrolly-active',
        style: { 'opacity': 0.95, 'width': 1.2, 'line-color': '#ffcc66', 'target-arrow-color': '#ffcc66' }
      },
      // ── Nébuleuse : glow fort sur chaque nœud → effet nuage ──
      {
        selector: 'node.in-nebula',
        style: {
          'shadow-blur':     60,
          'shadow-color':    'data(color)',
          'shadow-opacity':  0.76,
          'shadow-offset-x': 0,
          'shadow-offset-y': 0,
        }
      },
      // ── Nœuds "feuille" : petits points en périphérie des îles ──
      // Pyramide argumentative : Reference/SourceQuote/etc. = rang inférieur,
      // visibles mais discrets. Spirale de Fibonacci les place naturellement
      // en bordure (les moins connectés = les plus éloignés du centre).
      // ── Nebula : nœuds feuilles complètement cachés pour réduire le canvas ──
      {
        selector: 'node.nebula-leaf',
        style: { 'display': 'none' }  // exclut des bounds → zoom fit correct
      },
      // ── Nebula archipelago : arêtes complètement supprimées du rendu ──
      {
        selector: 'edge.nebula-arch',
        style: { 'display': 'none' }
      },
    ];
  }

  globalObj.createGrapheGraphStyles = createGrapheGraphStyles;
})(window);
