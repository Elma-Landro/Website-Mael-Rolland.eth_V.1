/**
 * generate_corrective_patch_batch3.mjs
 *
 * Applique les relations STRONGLY_SUPPORTED_ADD et SAFE_ADD
 * de Migration/grc20_relations_batch3.json.
 *
 * Stratégie : chaque `proposed_relation` est mappé au type de relation
 * existant le plus sémantiquement proche dans le graphe.
 * Les PROPOSED_REVIEW sont ignorés (à valider manuellement).
 *
 * Usage :
 *   node scripts/generate_corrective_patch_batch3.mjs
 * Produit :
 *   patch_batch3_relations.json
 *   grc20-these-mael-rolland-vN+1.json
 */

import { readFileSync, writeFileSync, readdirSync } from 'fs';
import { randomUUID } from 'crypto';

// ── Auto-detect latest vN.json ────────────────────────────────────────────────
const vFiles = readdirSync('.').filter(f => /^grc20-these-mael-rolland-v\d+\.json$/.test(f));
if (!vFiles.length) { console.error('No grc20-these-mael-rolland-vN.json found.'); process.exit(1); }
vFiles.sort((a, b) => parseInt(a.match(/v(\d+)/)[1]) - parseInt(b.match(/v(\d+)/)[1]));
const latestFile = vFiles[vFiles.length - 1];
const latestVer  = parseInt(latestFile.match(/v(\d+)/)[1]);
const GRAPH_OUT  = `grc20-these-mael-rolland-v${latestVer + 1}.json`;
const PATCH_OUT  = 'patch_batch3_relations.json';
console.log(`Input: ${latestFile}  →  Output: ${GRAPH_OUT}`);

// ── ThesisSection anchor IDs (for isElaboratedIn → appears_in_section) ────────
const CHAPTER_SECTION = {
  'Chap.I':   '93f13f18c6da412292eba80dcd630ac7', // I.2.1
  'Chap.II':  'd622d318825741cda43212d7831a88c7', // II.3
  'Chap.III': '89663a261c1545c1941ab7f871314a53', // III.2
};

// ── Relation type mapping ─────────────────────────────────────────────────────
// proposed_relation → { rtId, swap? }
// swap: true means create relation from target → source (reverse direction)
const REL_MAP = {
  // concept / structural
  'isElaboratedIn':   { rt: '__appears_in_section__' },        // handled specially
  'structures':       { rt: 'fad545e7a45346ee87ab2a8ca4b4e9e4' }, // supports concept
  'supportsConcept':  { rt: 'fad545e7a45346ee87ab2a8ca4b4e9e4' }, // supports concept
  // analytic
  'reveals':          { rt: '42c57b249283416ba8264e2beaf76cd5' }, // demonstrates
  'isAnalysedThrough':{ rt: 'd780ba68b69f4c688026fb2ff1e8fade' }, // applied to
  'isClarifiedBy':    { rt: '42c57b249283416ba8264e2beaf76cd5', swap: true }, // demonstrates (reversed)
  // participation / location
  'takesPlaceIn':     { rt: 'd3b2d5c9c2194536be63dc04dfa1daf8' }, // occurs in
  'involves':         { rt: 'f13ff5887b7c4997ab84ac27e1b2d3a3' }, // mentions actor
  'participatesIn':   { rt: '792a1e3ebc88405cac19b9941ef2d55f' }, // participates in
  'takesPartIn':      { rt: '792a1e3ebc88405cac19b9941ef2d55f' }, // participates in
  // phases
  'isPhaseOf':        { rt: '96e52d48d61148f694f43493aeb0a934' }, // phase of
  // illustration / composition
  'isIllustratedBy':  { rt: '1835fb8b1f0c47ff9af190c66034c4b8' }, // exemplified by
  'includes':         { rt: 'b1f2fdfb5c254687b5adbc8a6f947a09', swap: true }, // part of (reversed)
  // support / dependency
  'supports':         { rt: 'ZtFNaPDxmjHXKRCduNHV4A' },          // supports
  'isSupportedBy':    { rt: 'ZtFNaPDxmjHXKRCduNHV4A', swap: true }, // supports (reversed)
  'requires':         { rt: 'faba7c426c0540969c894b7921a1ad83', swap: true }, // enables (reversed)
  // temporal / causal
  'precedes':         { rt: '416b8ae38b544f23a37b41a16093cf36' }, // followed by
  'leadsTo':          { rt: '27844aaa5e6a4f3096ff045d291a61ca' }, // triggers
  'emergeFrom':       { rt: '27844aaa5e6a4f3096ff045d291a61ca', swap: true }, // triggers (reversed)
  'emergesWith':      { rt: 'a40201eade73431b9631c4e9d8e1c979' }, // coincides with
  // opposition
  'opposes':          { rt: '26adc3a0d25f4754a9e241139902923f' }, // opposes
  // category / instantiation
  'isInstantiatedBy': { rt: '7378742efe9149c2b27d5c85105ae42f', swap: true }, // instanceOfCategory (reversed)
  'isRepresentedBy':  { rt: '96a7a99187db45aa8918a049a0e19e97', swap: true }, // manifests (reversed)
};

// ── Name aliases (batch3 names → actual graph entity names) ──────────────────
const NAME_ALIASES = {
  // Concepts (short names → canonical graph names)
  'Monétisation':                       'Monétisation des cryptomonnaies',
  'Nominalisme monétaire non étatiste': 'Nominalisme monetaire non etatiste',
  'Politique de crises':                'Politique de crise',
  'Découverte du prix':                 'Concept — Découverte du prix (price discovery) de Bitcoin',
  'Liquidité du marché':                'Concept — Liquidité du marché Bitcoin',
  // Persons
  'De Filippi':   'Primavera De Filippi',
  'Peter Wuille': 'Pieter Wuille',
  // Actor groups
  'Développeurs core': 'Développeurs Core (mainteneurs avec accès commit)',
  'Mineurs':           'Mineurs Bitcoin',
  // Events (prefixed in graph with "InfrastructureEvent — ")
  'Bitcoin Foundation creation':
    'InfrastructureEvent — Bitcoin Foundation creation',
  'WordPress accepte les paiements en Bitcoin (2012)':
    'InfrastructureEvent — WordPress accepte les paiements en Bitcoin (2012)',
  'eBay / PayPal intègre Bitcoin (2014-2015)':
    'InfrastructureEvent — eBay / PayPal intègre Bitcoin (2014-2015)',
  'Lancement Casascius Physical Bitcoins (Mike Caldwell, 2011)':
    'InfrastructureEvent — Lancement Casascius Physical Bitcoins (Mike Caldwell, 2011)',
  'Innovations de métaprotocole Bitcoin (2012-2014)':
    'InfrastructureEvent — Innovations de métaprotocole Bitcoin (2012-2014)',
  'Colored Coins (protocole méta-token sur Bitcoin, 2012)':
    'InfrastructureEvent — Colored Coins (protocole méta-token sur Bitcoin, 2012)',
  // Arenas / entities with different exact names
  'All Core Dev Meetings': 'All Core Dev Meetings (Ethereum)',
  'Ethereum Hard Fork':    'Ethereum Hard Fork (juillet 2016)',
  // Apostrophe variants (curly ' in batch3 vs straight ' in graph)
  "Gouvernance publique d\u2019exception": "Gouvernance publique d\u2019exception",
  "Gouvernance publique d'exception":      "Gouvernance publique d\u2019exception",
};

// ── Load data ─────────────────────────────────────────────────────────────────
const graph    = JSON.parse(readFileSync(latestFile, 'utf8'));
const batch3   = JSON.parse(readFileSync('Migration/grc20_relations_batch3.json', 'utf8'));

// Build entity name → ID index
const nameToId = {};
for (const e of (graph.entities || [])) {
  if (e.name) nameToId[e.name.trim()] = e.id;
}

// Apply aliases
function resolve(name) {
  const n = name?.trim() || '';
  if (NAME_ALIASES[n] !== undefined) return NAME_ALIASES[n]; // null = intentionally skip
  return n;
}

// Build relation type name → ID index
const rtByName = {};
const rtById   = new Set();
for (const rt of (graph.relation_types || [])) {
  rtByName[rt.name] = rt.id;
  rtById.add(rt.id);
}
const APPEARS_RT = rtByName['appears in section'];
if (!APPEARS_RT) { console.error('ERROR: "appears in section" not found.'); process.exit(1); }

// Build existing relation index: set of "fromId|typeId|toId"
const existingSet = new Set();
for (const rel of (graph.relations || [])) {
  existingSet.add(`${rel.from}|${rel.type}|${rel.to}`);
}

// ── Process batch3 relations ──────────────────────────────────────────────────
const newRelations = [];
const stats = { added: 0, skipped_review: 0, skipped_no_entity: 0, skipped_no_rt: 0,
                skipped_dup: 0, skipped_chapter_target: 0 };

function addRel(fromId, rtId, toId, label) {
  const key = `${fromId}|${rtId}|${toId}`;
  if (existingSet.has(key)) { stats.skipped_dup++; return false; }
  if (!rtById.has(rtId) && rtId !== APPEARS_RT) { stats.skipped_no_rt++; return false; }
  newRelations.push({ id: randomUUID(), from: fromId, type: rtId, to: toId });
  existingSet.add(key);
  stats.added++;
  console.log(`  + [${label}] "${fromId.slice(0,8)}…" → "${toId.slice(0,8)}…"`);
  return true;
}

for (const row of batch3) {
  // Skip PROPOSED_REVIEW
  if (row.status === 'PROPOSED_REVIEW') { stats.skipped_review++; continue; }

  const srcRaw  = (row.source_entity || '').trim();
  const tgtRaw  = (row.target_entity || '').trim();
  const prop    = (row.proposed_relation || '').trim();

  // Resolve aliases
  const srcName = resolve(srcRaw);
  const tgtName = resolve(tgtRaw);
  if (srcName === null || tgtName === null) { stats.skipped_no_entity++; continue; }

  // Look up source entity
  const srcId = nameToId[srcName];
  if (!srcId) { stats.skipped_no_entity++; console.log(`  ? no entity: "${srcName}"`); continue; }

  const mapping = REL_MAP[prop];
  if (!mapping) { stats.skipped_no_rt++; console.log(`  ? unmapped relation: "${prop}"`); continue; }

  // Handle isElaboratedIn / structures targeting a Chapter
  if (mapping.rt === '__appears_in_section__') {
    const chap = row.chapter_hint?.replace(/\s/g, '') || '';
    // Sort by length descending so 'Chap.III' matches before 'Chap.II' before 'Chap.I'
    const chapKey = Object.keys(CHAPTER_SECTION).sort((a,b) => b.length - a.length).find(k => chap.includes(k));
    const secId = chapKey ? CHAPTER_SECTION[chapKey] : null;
    if (!secId) { stats.skipped_chapter_target++;
      console.log(`  ? isElaboratedIn: no section for hint "${row.chapter_hint}"`); continue; }
    addRel(srcId, APPEARS_RT, secId, `${prop}: ${srcName} → ${chapKey}`);
    continue;
  }

  // Look up target entity
  const tgtId = nameToId[tgtName];
  if (!tgtId) { stats.skipped_no_entity++; console.log(`  ? no entity: "${tgtName}"`); continue; }

  const rtId = mapping.rt;
  if (mapping.swap) {
    addRel(tgtId, rtId, srcId, `${prop}(↔): ${tgtName} → ${srcName}`);
  } else {
    addRel(srcId, rtId, tgtId, `${prop}: ${srcName} → ${tgtName}`);
  }
}

// ── Summary ───────────────────────────────────────────────────────────────────
console.log('\n=== Batch3 summary ===');
console.log(`  Added:              ${stats.added}`);
console.log(`  Skipped (review):   ${stats.skipped_review}`);
console.log(`  Skipped (no entity):${stats.skipped_no_entity}`);
console.log(`  Skipped (no rt):    ${stats.skipped_no_rt}`);
console.log(`  Skipped (dup):      ${stats.skipped_dup}`);
console.log(`  Skipped (chapter):  ${stats.skipped_chapter_target}`);

if (newRelations.length === 0) {
  console.log('Nothing to patch.'); process.exit(0);
}

// ── Write patch ───────────────────────────────────────────────────────────────
writeFileSync(PATCH_OUT, JSON.stringify({ relations: newRelations }, null, 2), 'utf8');
console.log(`\nPatch written to ${PATCH_OUT}`);

// ── Apply to graph ────────────────────────────────────────────────────────────
const newGraph = JSON.parse(JSON.stringify(graph));
newGraph.relations = [...(newGraph.relations || []), ...newRelations];
if (newGraph.space) {
  newGraph.space.version      = `v${latestVer + 1}`;
  newGraph.space.generated_at = new Date().toISOString();
}
writeFileSync(GRAPH_OUT, JSON.stringify(newGraph), 'utf8');
const sizeKB = Math.round(readFileSync(GRAPH_OUT).length / 1024);
console.log(`v${latestVer + 1} written to ${GRAPH_OUT} (${sizeKB} KB)`);
console.log('Done.');
