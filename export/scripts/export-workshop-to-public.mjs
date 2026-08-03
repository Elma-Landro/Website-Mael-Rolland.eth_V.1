#!/usr/bin/env node
/**
 * Minimal scaffold: workshop -> public static export
 *
 * Non-breaking by design: this script does not alter existing runtime files.
 */

import fs from 'fs';
import path from 'path';

const args = process.argv.slice(2);
const getArg = (name, fallback) => {
  const idx = args.indexOf(name);
  return (idx >= 0 && args[idx + 1] !== undefined) ? args[idx + 1] : fallback;
};

const inputCanonical = getArg('--canonical', './grc20-these-mael-rolland-v108.json');
const outputDir = getArg('--out', './public-data');

const PUBLIC_ALLOWED = new Set(['legacy_canonical', 'validated']);

function readJson(file) {
  return JSON.parse(fs.readFileSync(file, 'utf8'));
}

function resolveStatus(entity) {
  const status = entity?.attributes?.status;
  if (!status) return 'legacy_canonical';
  if (typeof status === 'object' && 'value' in status) return String(status.value);
  return String(status);
}

function toPublicCanonical(snapshot) {
  const entities = (snapshot.entities || []).filter((e) => PUBLIC_ALLOWED.has(resolveStatus(e)));
  const entityIds = new Set(entities.map((e) => e.id));
  const relations = (snapshot.relations || []).filter((r) => entityIds.has(r.from) && entityIds.has(r.to));

  return {
    ...snapshot,
    entities,
    relations,
    export_meta: {
      exportedAt: new Date().toISOString(),
      sourceCanonical: path.basename(inputCanonical),
      rule: 'status in legacy_canonical|validated'
    }
  };
}

function main() {
  if (!fs.existsSync(inputCanonical)) {
    throw new Error(`Canonical file not found: ${inputCanonical}`);
  }

  const canonical = readJson(inputCanonical);
  const out = toPublicCanonical(canonical);

  fs.mkdirSync(outputDir, { recursive: true });
  const outputFile = path.join(outputDir, 'canonical-graph.public.json');
  fs.writeFileSync(outputFile, JSON.stringify(out, null, 2));

  console.log(`Exported ${out.entities.length} entities / ${out.relations.length} relations -> ${outputFile}`);
}

main();
