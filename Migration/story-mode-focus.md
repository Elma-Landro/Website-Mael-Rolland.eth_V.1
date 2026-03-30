/*
PATCH TARGET
- Replace the current story-mode focus logic in graphe.html
- Keep resolveFocusNodes() as-is
- Add the helper functions below
- Replace applyStoryFocus() / clearStoryFocus() with the versions below

MAIN IDEA
- distinguish primary / secondary / backbone / hidden
- stop highlighting every edge touching a focused node
- allow per-step edge filtering
*/

function getEdgeType(edge) {
  return (
    edge.data('relation_type') ||
    edge.data('relationType') ||
    edge.data('type') ||
    edge.data('label') ||
    edge.data('name') ||
    ''
  ).toString();
}

function normalizeRelationName(v) {
  return (v || '').toString().trim().toLowerCase();
}

function buildStoryFocusOptions(step = {}) {
  return {
    cameraPreset: step.cameraPreset || 'cluster',
    edgeMode: step.edgeMode || 'strict',
    includeNeighbors: Boolean(step.includeNeighbors),
    secondaryDepth: Number.isFinite(step.secondaryDepth) ? step.secondaryDepth : 0,
    maxSecondaryPerTarget: Number.isFinite(step.maxSecondaryPerTarget) ? step.maxSecondaryPerTarget : 10,
    hideRelationTypes: Array.isArray(step.hideRelationTypes) ? step.hideRelationTypes.map(normalizeRelationName) : [],
    showRelationTypes: Array.isArray(step.showRelationTypes) ? step.showRelationTypes.map(normalizeRelationName) : [],
    hideBackbone: step.hideBackbone !== undefined ? Boolean(step.hideBackbone) : true,
    backboneRelationTypes: Array.isArray(step.backboneRelationTypes)
      ? step.backboneRelationTypes.map(normalizeRelationName)
      : ['partof', 'source', 'citedin', 'relatedto'],
    fitTargets: step.fitTargets || 'primary'
  };
}

function clearStoryFocusClasses(cy) {
  if (!cy) return;
  cy.elements().removeClass(
    'story-primary story-secondary story-muted story-hidden story-backbone highlighted faded'
  );
}

function collectSecondaryNodes(cy, primaryNodes, opts) {
  if (!cy || !primaryNodes || !primaryNodes.length) return cy.collection();
  if (!(opts.includeNeighbors || opts.edgeMode !== 'strict' || opts.secondaryDepth > 0)) return cy.collection();

  const secondary = cy.collection();
  const visited = new Set(primaryNodes.map(n => n.id()));
  const queue = primaryNodes.map(n => ({ node: n, depth: 0 }));

  while (queue.length) {
    const { node, depth } = queue.shift();
    if (depth >= Math.max(1, opts.secondaryDepth || 1)) continue;

    const connected = node.connectedEdges();
    let taken = 0;
    connected.forEach(edge => {
      if (taken >= opts.maxSecondaryPerTarget) return;
      const edgeType = normalizeRelationName(getEdgeType(edge));
      if (opts.hideRelationTypes.includes(edgeType)) return;
      if (opts.showRelationTypes.length && !opts.showRelationTypes.includes(edgeType)) return;
      if (opts.hideBackbone && opts.backboneRelationTypes.includes(edgeType)) return;

      const other = edge.source().id() === node.id() ? edge.target() : edge.source();
      if (visited.has(other.id())) return;
      visited.add(other.id());
      secondary.merge(other);
      queue.push({ node: other, depth: depth + 1 });
      taken += 1;
    });
  }

  return secondary;
}

function applyStoryFocus(targetIds = [], step = {}) {
  const cy = Graph.cy;
  if (!cy) return;

  const opts = buildStoryFocusOptions(step);
  clearStoryFocusClasses(cy);
  if (!targetIds.length) return;

  const primaryNodes = cy.nodes().filter(n => targetIds.includes(n.data('id')) || targetIds.includes(n.id()));
  const primaryIdSet = new Set(primaryNodes.map(n => n.id()));
  const secondaryNodes = collectSecondaryNodes(cy, primaryNodes, opts).filter(n => !primaryIdSet.has(n.id()));
  const secondaryIdSet = new Set(secondaryNodes.map(n => n.id()));

  cy.nodes().forEach(node => {
    const id = node.id();
    if (primaryIdSet.has(id)) node.addClass('story-primary');
    else if (secondaryIdSet.has(id)) node.addClass('story-secondary');
    else node.addClass('story-muted');
  });

  cy.edges().forEach(edge => {
    const s = edge.source().id();
    const t = edge.target().id();
    const edgeType = normalizeRelationName(getEdgeType(edge));
    const sP = primaryIdSet.has(s);
    const tP = primaryIdSet.has(t);
    const sS = secondaryIdSet.has(s);
    const tS = secondaryIdSet.has(t);

    if (opts.hideRelationTypes.includes(edgeType)) {
      edge.addClass('story-hidden');
      return;
    }
    if (opts.showRelationTypes.length && !opts.showRelationTypes.includes(edgeType)) {
      edge.addClass('story-hidden');
      return;
    }
    if (opts.backboneRelationTypes.includes(edgeType)) {
      edge.addClass(opts.hideBackbone ? 'story-hidden' : 'story-backbone');
      return;
    }

    if (opts.edgeMode === 'strict') {
      if (sP && tP) edge.addClass('story-primary');
      else edge.addClass('story-hidden');
      return;
    }

    if (opts.edgeMode === 'neighbors') {
      if (sP && tP) edge.addClass('story-primary');
      else if ((sP && tS) || (tP && sS)) edge.addClass('story-secondary');
      else edge.addClass('story-hidden');
      return;
    }

    // context mode
    if (sP && tP) edge.addClass('story-primary');
    else if ((sP && tS) || (tP && sS) || (sS && tS)) edge.addClass('story-secondary');
    else edge.addClass(opts.hideBackbone ? 'story-hidden' : 'story-backbone');
  });

  const fitEles = opts.fitTargets === 'primary+secondary'
    ? primaryNodes.union(secondaryNodes)
    : primaryNodes;

  const paddingByPreset = { tight: 42, cluster: 68, wide: 115 };
  const padding = paddingByPreset[opts.cameraPreset] || 68;
  if (fitEles.length) cy.animate({ fit: { eles: fitEles, padding } }, { duration: 430 });
}

function clearStoryFocus() {
  const cy = Graph.cy;
  if (!cy) return;
  clearStoryFocusClasses(cy);
}

/*
IMPORTANT
You must also update applyStoryStep(step) so that it calls:

  const resolvedTargets = resolveFocusNodes(step.focusNodes || []);
  applyStoryFocus(resolvedTargets, step);

instead of passing only cameraPreset.
*/
