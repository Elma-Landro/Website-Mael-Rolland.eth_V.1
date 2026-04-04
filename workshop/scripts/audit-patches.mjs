#!/usr/bin/env node

import fs from 'fs';
import path from 'path';

const ROOT = process.cwd();

const readTextSafe = (p, n = 12000) => {
  try {
    return fs.readFileSync(p, 'utf8').slice(0, n);
  } catch {
    return '';
  }
};

const rel = (p) => path.relative(ROOT, p);
const exists = (p) => fs.existsSync(path.join(ROOT, p));

function listFiles(dir, predicate = () => true) {
  const full = path.join(ROOT, dir);
  if (!fs.existsSync(full)) return [];
  return fs.readdirSync(full)
    .map((name) => path.join(full, name))
    .filter((p) => fs.statSync(p).isFile() && predicate(path.basename(p)));
}

function detectVersionHints(text) {
  const set = new Set();
  for (const m of text.matchAll(/v\d+(?:\s*[→>-]+\s*v\d+)?/gi)) set.add(m[0].replace(/\s+/g, ''));
  return [...set].slice(0, 6);
}

function referencedVersionForPath(fileRel, text) {
  const ext = path.extname(fileRel).toLowerCase();
  if (ext === '.zip' || ext === '.docx') return ['unknown'];
  const hints = detectVersionHints(text);
  return hints.length ? hints : ['unknown'];
}

function scopeFromName(name) {
  const n = name.toLowerCase();
  if (n.includes('sourcequote')) return 'sourcequote anchoring/migration';
  if (n.includes('cited_in') || n.includes('cited')) return 'chapter citation repair';
  if (n.includes('intro')) return 'intro section anchoring';
  if (n.includes('chapter_attribution') || n.includes('anchoring')) return 'section/chapter anchoring';
  if (n.includes('definitions')) return 'definition attributes enrichment';
  if (n.includes('central_arguments')) return 'thesis section central arguments';
  if (n.includes('relations')) return 'relation augmentation';
  if (n.includes('migration_report')) return 'migration reporting';
  if (n.includes('overrides')) return 'targeted anchor overrides';
  return 'unknown';
}

function statusHeuristic(fileRel, text) {
  const n = fileRel.toLowerCase();
  if (n.includes('migration_report')) return { status: 'candidate_applied', confidence: 'medium', note: 'report artifact indicates a migration run occurred' };
  if (text.includes('PATCH documentaire') || text.includes('prochaine injection contrôlée')) return { status: 'candidate_pending', confidence: 'high', note: 'explicitly documented as planned/controlled future injection' };
  if (text.includes('NEEDS_CREATION:')) return { status: 'candidate_pending', confidence: 'medium', note: 'contains unresolved placeholders' };
  if (text.match(/source_graph"\s*:\s*"grc20-these-mael-rolland-v(7|8)\d+/)) return { status: 'superseded_possible', confidence: 'medium', note: 'targets an older graph baseline' };
  return { status: 'unknown', confidence: 'low', note: 'no grounded application evidence found in this pass' };
}

function relatedScriptsFor(fileRel) {
  const name = path.basename(fileRel);
  const map = {
    'patch_4a_chapter_attribution.json': ['scripts/generate_chapter_patch.mjs'],
    'patch_5a_corrective_anchoring.json': ['scripts/generate_corrective_patch.mjs'],
    'patch_batch1_anchoring.json': ['scripts/generate_corrective_patch_batch1.mjs'],
    'patch_batch2_anchoring.json': ['scripts/generate_corrective_patch_batch2.mjs'],
    'patch_batch3_relations.json': ['scripts/generate_corrective_patch_batch3.mjs'],
  };
  if (map[name]) return map[name].filter(exists);
  if (name.includes('sourcequote')) {
    return [
      'scripts/apply-sourcequote-phases.mjs',
      'scripts/sourcequote-migration/normalize.mjs',
      'scripts/sourcequote-migration/resolve.mjs',
      'scripts/sourcequote-migration/apply.mjs',
      'scripts/sourcequote-migration/report.mjs'
    ].filter(exists);
  }
  if (name.includes('v91_migration_report')) return ['apply_v91_migration.py'].filter(exists);
  return [];
}

function buildInventory() {
  const rootPatchFiles = listFiles('.', (n) => /^patch.*\.json$/.test(n) || n === 'new_relations_patch.json' || n === 'grc20_v91_migration_report.json');
  const patchesDirFiles = listFiles('patches', (n) => n.endsWith('.json'));
  const migrationFiles = listFiles('Migration');
  const scriptFiles = [
    ...listFiles('scripts', (n) => n.endsWith('.mjs')),
    ...listFiles('scripts/sourcequote-migration'),
    ...listFiles('.', (n) => n === 'apply_v91_migration.py')
  ];

  const artifacts = [];

  for (const full of [...rootPatchFiles, ...patchesDirFiles]) {
    const r = rel(full);
    const text = readTextSafe(full);
    const vers = detectVersionHints(text);
    const { status, confidence, note } = statusHeuristic(r, text);
    artifacts.push({
      filename: path.basename(r),
      path: r,
      artifactType: r.endsWith('.json') ? 'patch_json' : 'unknown',
      probableScope: scopeFromName(r),
      referencedVersion: vers.length ? vers : ['unknown'],
      probableStatus: status,
      relatedScripts: relatedScriptsFor(r),
      notes: note,
      confidence
    });
  }

  for (const full of migrationFiles) {
    const r = rel(full);
    const text = readTextSafe(full);
    const ext = path.extname(r).toLowerCase();
    let artifactType = 'unknown';
    if (ext === '.zip') artifactType = 'zip_bundle';
    else if (ext === '.md' || ext === '.docx') artifactType = 'helper_script';
    const { status, confidence, note } = statusHeuristic(r, text);
    artifacts.push({
      filename: path.basename(r),
      path: r,
      artifactType,
      probableScope: scopeFromName(r),
      referencedVersion: referencedVersionForPath(r, text),
      probableStatus: status,
      relatedScripts: r.includes('sourcequote') ? ['scripts/apply-sourcequote-phases.mjs'] : [],
      notes: note,
      confidence
    });
  }

  for (const full of scriptFiles) {
    const r = rel(full);
    if (r.startsWith('scripts/sourcequote-migration/README')) continue;
    const text = readTextSafe(full);
    artifacts.push({
      filename: path.basename(r),
      path: r,
      artifactType: 'migration_script',
      probableScope: scopeFromName(r),
      referencedVersion: referencedVersionForPath(r, text),
      probableStatus: 'unknown',
      relatedScripts: [],
      notes: 'script present; execution/applicability not asserted in this inventory pass',
      confidence: 'medium'
    });
  }

  artifacts.sort((a, b) => a.path.localeCompare(b.path));

  return {
    generatedAt: new Date().toISOString(),
    mode: 'documentary_inventory_only',
    caution: 'Statuses are heuristic. unknown/needs_audit preferred where evidence is weak.',
    totals: {
      artifacts: artifacts.length,
      patch_json: artifacts.filter((a) => a.artifactType === 'patch_json').length,
      migration_script: artifacts.filter((a) => a.artifactType === 'migration_script').length,
      zip_bundle: artifacts.filter((a) => a.artifactType === 'zip_bundle').length,
      helper_script: artifacts.filter((a) => a.artifactType === 'helper_script').length,
      unknown: artifacts.filter((a) => a.artifactType === 'unknown').length
    },
    artifacts
  };
}

function writeMarkdown(report) {
  const lines = [];
  lines.push('# Patch & Migration Audit (documentary, non-applying)');
  lines.push('');
  lines.push(`Generated: ${report.generatedAt}`);
  lines.push('');
  lines.push('## Scope');
  lines.push('- Root patch JSON artifacts (`patch*.json`, `new_relations_patch.json`, `grc20_v91_migration_report.json`)');
  lines.push('- `patches/` JSON artifacts');
  lines.push('- `Migration/` bundle and helper artifacts');
  lines.push('- Root and sourcequote migration scripts under `scripts/` + `apply_v91_migration.py`');
  lines.push('');
  lines.push('## Totals');
  lines.push(`- Artifacts: ${report.totals.artifacts}`);
  lines.push(`- patch_json: ${report.totals.patch_json}`);
  lines.push(`- migration_script: ${report.totals.migration_script}`);
  lines.push(`- zip_bundle: ${report.totals.zip_bundle}`);
  lines.push(`- helper_script: ${report.totals.helper_script}`);
  lines.push(`- unknown: ${report.totals.unknown}`);
  lines.push('');
  lines.push('## Key grounded findings');
  lines.push('- `scripts/apply-sourcequote-phases.mjs` exists and references phase ZIP bundles in `Migration/`.');
  lines.push('- Several patch files explicitly reference old graph baselines (e.g., v72/v73/v82-v83), so current applicability is uncertain without replay audit.');
  lines.push('- `patches/grc20_anchor_overrides_targeted.json` explicitly describes itself as a documentary/controlled future injection candidate.');
  lines.push('- No patch is declared "applied" here unless evidence is explicit (migration report artifact only is tagged candidate_applied).');
  lines.push('');
  lines.push('## Status policy used in this pass');
  lines.push('- `unknown`: default when no strong evidence of apply-state exists.');
  lines.push('- `candidate_pending`: explicit placeholders/planned injection notes present.');
  lines.push('- `superseded_possible`: artifact targets older version baseline.');
  lines.push('- `candidate_applied`: migration report artifact suggests a run occurred, but full replay was not performed.');
  lines.push('');
  lines.push('For machine-readable details, see `patch-inventory.json`.');

  return lines.join('\n');
}

function main() {
  const outDir = path.join(ROOT, 'workshop', 'patches');
  fs.mkdirSync(outDir, { recursive: true });

  const report = buildInventory();
  fs.writeFileSync(path.join(outDir, 'patch-inventory.json'), JSON.stringify(report, null, 2));
  fs.writeFileSync(path.join(outDir, 'PATCH_AUDIT.md'), writeMarkdown(report));

  console.log(`Wrote workshop/patches/patch-inventory.json (${report.totals.artifacts} artifacts)`);
  console.log('Wrote workshop/patches/PATCH_AUDIT.md');
}

main();
