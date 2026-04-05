/**
 * Graph data builder helper extracted from graphe.html.
 * Scope intentionally limited to pure Cytoscape element construction.
 */
(function attachGraphDataFactory(globalObj) {
  function createGrapheGraphData({
    State,
    TYPE_COLORS,
    TYPE_SHAPES,
    computeVisualNodeSize,
    getNodeLabel,
    STRATUM_ALWAYS_VISIBLE_NAMES,
    getChapterMap,
  }) {
    function entityToNode(entity) {
      const typeName = State.getEntityTypeName(entity);
      const color = TYPE_COLORS[typeName] || '#64748b';
      const shape = TYPE_SHAPES[typeName] || 'ellipse';
      const size = computeVisualNodeSize(entity);
      const degree = (State.maps.outgoing[entity.id] || []).length
                   + (State.maps.incoming[entity.id] || []).length;
      const isMajor = degree >= 10 || STRATUM_ALWAYS_VISIBLE_NAMES.has(entity.name);
      const chapterMap = getChapterMap();
      const chapterIdx = chapterMap[entity.id] !== undefined ? chapterMap[entity.id] : -1;
      return {
        data: {
          id: entity.id, label: getNodeLabel(entity),
          typeName, color, shape, size,
          fullName: entity.name,
          degree,
          isMajor,
          chapterIdx,
          labelColor: color,  // type color = same as node body and col-halo
        },
        classes: chapterIdx >= 0 ? 'chapter-' + chapterIdx : '',
      };
    }

    function relationToEdge(rel, idx) {
      const rtObj = State.maps.relTypes[rel.type];
      const label = rtObj ? rtObj.name : rel.type;
      return {
        data: {
          id: 'e_' + idx + '_' + rel.from + '_' + rel.to,
          source: rel.from, target: rel.to,
          relTypeId: rel.type, label,
          _relIdx: idx,
        }
      };
    }

    function buildElements() {
      const data = State.data;
      if (!data) return [];
      const nodes = data.entities.map(e => entityToNode(e));
      const edges = data.relations.map((r, i) => relationToEdge(r, i))
        .filter(e => {
          const s = e.data.source, t = e.data.target;
          return State.maps.entities[s] && State.maps.entities[t];
        });
      return [...nodes, ...edges];
    }

    return {
      entityToNode,
      relationToEdge,
      buildElements,
    };
  }

  globalObj.createGrapheGraphData = createGrapheGraphData;
})(window);
