/**
 * State layer extracted from graphe.html.
 * Keeps the same API contract as the inlined State IIFE.
 */
(function attachGrapheStateFactory(globalObj) {
  function createGrapheState() {
    let _data = null;          // current working data
    let _original = null;      // snapshot at load time
    let _version = 2;
    let _dirty = false;
    let _selectedId = null;
    let _hiddenTypes = new Set();
    let _searchQ = '';
    let _undoStack = [];
    let _errors = [];

    const maps = {
      entities: {},   // id → entity
      types: {},      // id → type obj
      typeName: {},   // name → type obj
      relTypes: {},   // id → relType obj
      relTypeName:{}, // name → relType obj
      outgoing: {},   // entityId → [relation …]
      incoming: {},   // entityId → [relation …]
    };

    function buildMaps(data) {
      maps.entities = {};
      maps.types = {};
      maps.typeName = {};
      maps.relTypes = {};
      maps.relTypeName = {};
      maps.outgoing = {};
      maps.incoming = {};
      for (const t of data.types) {
        maps.types[t.id] = t;
        maps.typeName[t.name] = t;
      }
      for (const r of data.relation_types) {
        maps.relTypes[r.id] = r;
        maps.relTypeName[r.name] = r;
      }
      for (const e of data.entities) {
        maps.entities[e.id] = e;
        maps.outgoing[e.id] = [];
        maps.incoming[e.id] = [];
      }
      for (const rel of data.relations) {
        if (maps.outgoing[rel.from]) maps.outgoing[rel.from].push(rel);
        if (maps.incoming[rel.to])   maps.incoming[rel.to].push(rel);
      }
    }

    function load(data) {
      _original = JSON.parse(JSON.stringify(data));
      _data = JSON.parse(JSON.stringify(data));
      _version = parseInt((data.space && data.space.version) || 2) || 2;
      _dirty = false;
      _undoStack = [];
      _errors = [];
      _selectedId = null;
      buildMaps(_data);
    }

    function snapshot() {
      _undoStack.push(JSON.parse(JSON.stringify(_data)));
      if (_undoStack.length > 40) _undoStack.shift();
      _dirty = true;
    }

    function undo() {
      if (!_undoStack.length) return false;
      _data = _undoStack.pop();
      buildMaps(_data);
      return true;
    }

    function getEntityTypeName(entity) {
      if (!entity.types || !entity.types.length) return 'Unknown';
      const tid = entity.types[0];
      return maps.types[tid] ? maps.types[tid].name : 'Unknown';
    }

    function getEntityDesc(entity) {
      if (!entity.description) return '';
      return entity.description.value || '';
    }

    return {
      get data() { return _data; },
      get version() { return _version; },
      get dirty() { return _dirty; },
      get selectedId() { return _selectedId; },
      set selectedId(v) { _selectedId = v; },
      get hiddenTypes() { return _hiddenTypes; },
      get searchQ() { return _searchQ; },
      set searchQ(v) { _searchQ = v; },
      get errors() { return _errors; },
      set errors(v) { _errors = v; },
      maps,
      load, snapshot, undo,
      getEntityTypeName, getEntityDesc,
      get undoCount() { return _undoStack.length; },
      bumpVersion() { _version++; },
    };
  }

  globalObj.createGrapheState = createGrapheState;
})(window);
