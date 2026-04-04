/**
 * Validator + Exporter extracted from graphe.html.
 * Keeps existing behavior and public call surface.
 */
(function attachValidationExporter(globalObj) {
  function createGrapheValidator({ State, document }) {
    function run() {
      const data = State.data;
      if (!data) return [];
      const errors = [];
      // Broken relations
      for (let i = 0; i < data.relations.length; i++) {
        const r = data.relations[i];
        if (!State.maps.entities[r.from]) {
          errors.push({ type: 'broken_rel', msg: `Relation #${i}: source introuvable (${r.from})`, relIdx: i });
        }
        if (!State.maps.entities[r.to]) {
          errors.push({ type: 'broken_rel', msg: `Relation #${i}: cible introuvable (${r.to})`, relIdx: i });
        }
      }
      // Duplicate names within same type
      const nameByType = {};
      for (const e of data.entities) {
        const typeName = State.getEntityTypeName(e);
        const key = typeName + '|' + e.name.toLowerCase().trim();
        if (!nameByType[key]) nameByType[key] = [];
        nameByType[key].push(e);
      }
      for (const [key, ents] of Object.entries(nameByType)) {
        if (ents.length > 1) {
          errors.push({ type: 'duplicate', msg: `Doublon : « ${ents[0].name} » (${ents.length}× dans ${key.split('|')[0]})`, ids: ents.map((e) => e.id) });
        }
      }
      // Empty types
      for (const t of data.types) {
        const count = data.entities.filter((e) => e.types && e.types.includes(t.id)).length;
        if (count === 0) errors.push({ type: 'empty_type', msg: `Type « ${t.name} » vide (aucune entité)` });
      }
      State.errors = errors;
      return errors;
    }

    function updateBadge() {
      const errs = State.errors.length;
      const badge = document.getElementById('error-badge');
      const statErr = document.getElementById('stat-errors');
      badge.textContent = errs + (errs === 1 ? ' erreur' : ' erreurs');
      if (errs === 0) {
        badge.className = 'badge-error badge-ok';
      } else {
        badge.className = 'badge-error' + (errs > 5 ? '' : ' badge-warn');
      }
      badge.classList.remove('hidden');
      statErr.textContent = errs;
    }

    return { run, updateBadge };
  }

  function createGrapheExporter({ State, document, toast, BlobCtor = Blob, URLApi = URL }) {
    function exportJSON() {
      const data = State.data;
      if (!data) return;
      State.bumpVersion();
      const out = JSON.parse(JSON.stringify(data));
      out.space = out.space || {};
      out.space.version = String(State.version);
      out.space.exported = new Date().toISOString();
      const blob = new BlobCtor([JSON.stringify(out, null, 2)], { type: 'application/json' });
      const url = URLApi.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = `grc20-these-mael-rolland-v${State.version}.json`;
      a.click();
      URLApi.revokeObjectURL(url);
      document.getElementById('export-version').textContent = State.version;
      toast(`Exporté : v${State.version}`, 'success');
    }

    return { exportJSON };
  }

  globalObj.createGrapheValidator = createGrapheValidator;
  globalObj.createGrapheExporter = createGrapheExporter;
})(window);
