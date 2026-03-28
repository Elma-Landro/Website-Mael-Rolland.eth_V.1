/**
 * generate_chapter_patch.mjs
 *
 * Génère patch_4a_chapter_attribution.json :
 * ajoute des relations `appears_in_section` pour ancrer les entités
 * CrisisEvent / CrisisPhase → Chap. III
 * InfrastructureEvent / DevelopmentPhase → Chap. I
 * qui n'ont actuellement aucune relation vers leur chapitre canonique.
 *
 * Usage :
 *   node scripts/generate_chapter_patch.mjs
 * Produit :
 *   patch_4a_chapter_attribution.json
 *   grc20-these-mael-rolland-v88.json
 */

import { readFileSync, writeFileSync } from 'fs';
import { randomUUID } from 'crypto';

// Auto-detect the latest vN.json in the current directory
import { readdirSync } from 'fs';
const vFiles = readdirSync('.').filter(f => /^grc20-these-mael-rolland-v\d+\.json$/.test(f));
if (!vFiles.length) { console.error('No grc20-these-mael-rolland-vN.json found.'); process.exit(1); }
vFiles.sort((a, b) => {
  const na = parseInt(a.match(/v(\d+)/)[1]), nb = parseInt(b.match(/v(\d+)/)[1]);
  return na - nb;
});
const latestFile  = vFiles[vFiles.length - 1];
const latestVer   = parseInt(latestFile.match(/v(\d+)/)[1]);
const GRAPH_PATH  = latestFile;
const SECTION_MAP = 'entity_section_map.json';
const PATCH_OUT   = 'patch_4a_chapter_attribution.json';
const GRAPH_OUT   = `grc20-these-mael-rolland-v${latestVer + 1}.json`;
console.log(`Input : ${GRAPH_PATH}  →  Output : ${GRAPH_OUT}`);

// ── ThesisSection anchor IDs ──────────────────────────────────────────────────
const SECTION_I_2_1   = '93f13f18c6da412292eba80dcd630ac7'; // I.2.1 — improvisations carnavalesques
const SECTION_III_1_1 = 'ac859fd14006e379e55373d31090b6c6'; // III.1.1 — CVE 2018, mise en crise longue
const SECTION_III_2_1 = '9fbdbbc3f81ee08fb89b5c5dfbcd2929'; // III.2.1 — diversité des crises Bitcoin
const SECTION_III_3_1 = 'cf7dfaf42b4f3caa74d2078a8eacc9e6'; // III.3.1 — The DAO, mise en crise brutale

// Mots-clés permettant de router certains CrisisEvent vers une section plus précise
const CVE_2018_PATTERNS = /CVE-2018-17144|2018-17144/i;
const DAO_PATTERNS      = /\bDAO\b|DAO\s|TheDAO|The DAO|\bEthereum.*fork\b|\bDAO.*hard\b|\bdao\b/i;

// ── Load data ─────────────────────────────────────────────────────────────────
const graph      = JSON.parse(readFileSync(GRAPH_PATH, 'utf8'));
const sectionMap = JSON.parse(readFileSync(SECTION_MAP, 'utf8'));

// Build type name lookup
const typeIdToName = {};
for (const t of (graph.types || [])) typeIdToName[t.id] = t.name;

// Find the `appears in section` relation type ID
const rtByName = {};
for (const rt of (graph.relation_types || [])) rtByName[rt.name] = rt.id;
const APPEARS_IN_SECTION_RT = rtByName['appears in section'];
if (!APPEARS_IN_SECTION_RT) {
  console.error('ERROR: relation type "appears in section" not found in graph.');
  process.exit(1);
}

// Target type groups
const CRISIS_TYPES   = new Set(['CrisisEvent', 'CrisisPhase']);
const INFRA_TYPES    = new Set(['InfrastructureEvent', 'DevelopmentPhase']);

// ── Build index of existing appears_in_section relations per entity ───────────
const existingRelTargets = {}; // entityId → Set of section IDs it already points to
for (const rel of graph.relations) {
  if (rel.type !== APPEARS_IN_SECTION_RT) continue;
  if (!existingRelTargets[rel.from]) existingRelTargets[rel.from] = new Set();
  existingRelTargets[rel.from].add(rel.to);
}

// ── Determine which chapter each entity is already anchored to (via section IDs)
// We consider Chap I sections = any section starting with "I." and Chap III = "III."
// For this purpose we just check if the entity has ANY relation to a Chap I / Chap III section.
// We read the ThesisSection entities for this.
const sectionChapter = {}; // sectionId → 'chap1' | 'chap2' | 'chap3' | 'intro' | 'conclu'
for (const e of graph.entities) {
  const typeNames = (e.types || []).map(tid => typeIdToName[tid] || '');
  if (!typeNames.includes('ThesisSection')) continue;
  const name = e.name || '';
  if (/^I\.\d|Chapitre I/.test(name))   sectionChapter[e.id] = 'chap1';
  else if (/^II\.\d|Chapitre II/.test(name))  sectionChapter[e.id] = 'chap2';
  else if (/^III\.\d|Chapitre III/.test(name)) sectionChapter[e.id] = 'chap3';
  else if (/Introduction/i.test(name))  sectionChapter[e.id] = 'intro';
  else if (/Conclusion/i.test(name))    sectionChapter[e.id] = 'conclu';
}

function entityAnchoredToChap(entityId, chap) {
  const targets = existingRelTargets[entityId];
  if (!targets) return false;
  return [...targets].some(sid => sectionChapter[sid] === chap);
}

// ── Generate new relations ────────────────────────────────────────────────────
const newRelations = [];

function addRelation(fromId, toSectionId) {
  // Avoid duplicates
  if (existingRelTargets[fromId]?.has(toSectionId)) return;
  newRelations.push({
    id:   randomUUID(),
    from: fromId,
    type: APPEARS_IN_SECTION_RT,
    to:   toSectionId,
  });
  // Register to avoid double-adding in same run
  if (!existingRelTargets[fromId]) existingRelTargets[fromId] = new Set();
  existingRelTargets[fromId].add(toSectionId);
}

function pickCrisisSection(entity) {
  const name = entity.name || '';
  const desc = entity.attributes?.description?.value || '';
  const combined = name + ' ' + desc;
  if (CVE_2018_PATTERNS.test(combined)) return SECTION_III_1_1;
  if (DAO_PATTERNS.test(combined))      return SECTION_III_3_1;
  return SECTION_III_2_1; // default: catalogue des crises Bitcoin
}

let crisisFixed = 0, infraFixed = 0;

for (const entity of graph.entities) {
  const typeNames = (entity.types || []).map(tid => typeIdToName[tid] || '');

  if (typeNames.some(t => CRISIS_TYPES.has(t))) {
    // CrisisEvent / CrisisPhase → anchor to Chap III if not already
    if (!entityAnchoredToChap(entity.id, 'chap3')) {
      addRelation(entity.id, pickCrisisSection(entity));
      crisisFixed++;
    }
  } else if (typeNames.some(t => INFRA_TYPES.has(t))) {
    // InfrastructureEvent / DevelopmentPhase → anchor to Chap I if not already
    if (!entityAnchoredToChap(entity.id, 'chap1')) {
      addRelation(entity.id, SECTION_I_2_1);
      infraFixed++;
    }
  }
}

console.log(`New relations generated: ${newRelations.length}`);
console.log(`  CrisisEvent/Phase fixed: ${crisisFixed}`);
console.log(`  InfrastructureEvent/DevelopmentPhase fixed: ${infraFixed}`);

// ── Write patch file ──────────────────────────────────────────────────────────
const patch = { relations: newRelations };
writeFileSync(PATCH_OUT, JSON.stringify(patch, null, 2), 'utf8');
console.log(`Patch written to ${PATCH_OUT}`);

// ── Apply patch to produce v88 ────────────────────────────────────────────────
const v88 = JSON.parse(JSON.stringify(graph)); // deep clone
v88.relations = [...(v88.relations || []), ...newRelations];

// Update metadata
if (v88.space) {
  v88.space.version       = `v${latestVer + 1}`;
  v88.space.generated_at  = new Date().toISOString();
}

writeFileSync(GRAPH_OUT, JSON.stringify(v88), 'utf8');
const sizeKB = Math.round(readFileSync(GRAPH_OUT).length / 1024);
console.log(`v88 written to ${GRAPH_OUT} (${sizeKB} KB)`);
console.log('Done.');
