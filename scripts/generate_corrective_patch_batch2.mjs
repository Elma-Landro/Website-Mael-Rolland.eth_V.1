/**
 * generate_corrective_patch_batch2.mjs
 *
 * Applique les corrections SAFE_FIX de Migration/grc20_entity_overrides_batch2.json :
 * ajoute des relations `appears_in_section` pour ancrer les entités
 * (concepts, institutions, organisations, groupes d'acteurs) mal ancrées.
 *
 * Usage :
 *   node scripts/generate_corrective_patch_batch2.mjs
 * Produit :
 *   patch_batch2_anchoring.json
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
const PATCH_OUT  = 'patch_batch2_anchoring.json';
console.log(`Input: ${latestFile}  →  Output: ${GRAPH_OUT}`);

// ── ThesisSection anchor IDs ──────────────────────────────────────────────────
const SECTIONS = {
  // Intro
  INTRO:   '5c6a74e82e5d4b9a9f0d1e3c7a8b2f41', // Introduction générale (fallback — check graph)
  // Chap. I
  I_2_1:   '93f13f18c6da412292eba80dcd630ac7', // I.2.1 — improvisations carnavalesques
  I_2_2:   '97eb62676b0052c4ab3652fc2bd15535', // I.2.2 — régulations transactionnelles
  I_3_2:   'ed2c565cbede474da7b6144bcb22d753', // I.3.2 — Ethereum : conditions d'émergence
  // Chap. II
  II_3:    'd622d318825741cda43212d7831a88c7', // II.3 — Au-delà de l'absence de gouvernance
  II_3_3:  '7b3312fed875cffb74320f0a579763c7', // II.3.3 — Les CM réactivent un débat monétaire ancien
  // Chap. III
  III_2:   '89663a261c1545c1941ab7f871314a53', // III.2 — politique de crises
  III_3_1: 'cf7dfaf42b4f3caa74d2078a8eacc9e6', // III.3.1 — The DAO
};

// ── Name-based correction rules (batch2 SAFE_FIX entries) ────────────────────
const NAME_RULES = [
  // ── Concepts mal ancrés → Chap. I ──────────────────────────────────────────
  { match: n => n === 'Développement infrastructurel par phases',
    sections: [SECTIONS.I_2_1],
    label: 'Développement infrastructurel par phases → I.2.1' },

  // ── Concepts mal ancrés → Chap. II ─────────────────────────────────────────
  { match: n => n === 'Nominalisme monetaire non etatiste',
    sections: [SECTIONS.II_3],
    label: 'Nominalisme monétaire non étatiste → II.3' },

  // ── Institutions (banques, universités) mal ancrées → Chap. II ─────────────
  { match: n => n.includes('Banque centrale européenne'),
    sections: [SECTIONS.II_3],
    label: 'BCE → II.3' },
  { match: n => n === 'Banque de France',
    sections: [SECTIONS.II_3],
    label: 'Banque de France → II.3' },
  { match: n => n === 'Banque mondiale',
    sections: [SECTIONS.II_3],
    label: 'Banque mondiale → II.3' },
  { match: n => n.includes('Banque des règlements internationaux'),
    sections: [SECTIONS.II_3],
    label: 'BRI → II.3' },
  { match: n => n.includes('Fonds Monetaire International'),
    sections: [SECTIONS.II_3],
    label: 'FMI → II.3' },
  { match: n => n === 'Tether Limited',
    sections: [SECTIONS.II_3],
    label: 'Tether Limited → II.3' },
  { match: n => n === 'Robinhood (plateforme de trading)',
    sections: [SECTIONS.II_3],
    label: 'Robinhood → II.3' },
  { match: n => n === 'Dell',
    sections: [SECTIONS.II_3_3],
    label: 'Dell → II.3.3' },
  { match: n => n === 'Core Developers (Bitcoin)',
    sections: [SECTIONS.II_3],
    label: 'Core Developers Bitcoin → II.3' },

  // ── Acteurs infrastructurels mal ancrés → Chap. I ──────────────────────────
  { match: n => n === 'BitPay',
    sections: [SECTIONS.I_2_1],
    label: 'BitPay → I.2.1' },
  { match: n => n === 'Coinbase',
    sections: [SECTIONS.I_2_1],
    label: 'Coinbase → I.2.1' },
  { match: n => n === 'MtGox',
    sections: [SECTIONS.I_2_1],
    label: 'MtGox → I.2.1' },
  { match: n => n === 'BTC-e',
    sections: [SECTIONS.I_2_1],
    label: 'BTC-e → I.2.1' },

  // ── Acteurs de crises mal ancrés → Chap. III ───────────────────────────────
  { match: n => n === 'Partisans Ethereum Classic',
    sections: [SECTIONS.III_3_1],
    label: 'Partisans Ethereum Classic → III.3.1' },
  { match: n => n === 'Whitehat Group (DAO crisis)',
    sections: [SECTIONS.III_3_1],
    label: 'Whitehat Group → III.3.1' },
  { match: n => n === 'Core Developers (Ethereum)',
    sections: [SECTIONS.III_3_1],
    label: 'Core Developers Ethereum → III.3.1' },
  { match: n => n === 'Détenteurs de jetons DAO',
    sections: [SECTIONS.III_3_1],
    label: 'Détenteurs de jetons DAO → III.3.1' },
  { match: n => n === 'Slock.it',
    sections: [SECTIONS.III_3_1],
    label: 'Slock.it → III.3.1' },
  { match: n => n === 'Université de Münster',
    sections: [SECTIONS.III_3_1],
    label: 'Université de Münster → III.3.1' },
];

// ── Load graph ────────────────────────────────────────────────────────────────
const graph = JSON.parse(readFileSync(latestFile, 'utf8'));

const rtByName = {};
for (const rt of (graph.relation_types || [])) rtByName[rt.name] = rt.id;
const APPEARS_RT = rtByName['appears in section'];
if (!APPEARS_RT) { console.error('ERROR: "appears in section" relation type not found.'); process.exit(1); }

// Verify section IDs exist in graph (warn if not found)
const entityIds = new Set((graph.entities || []).map(e => e.id));
for (const [key, sid] of Object.entries(SECTIONS)) {
  if (!entityIds.has(sid)) console.warn(`  WARN: section ${key} (${sid}) not found in graph — relations to it will be skipped.`);
}

// Build existing appears_in_section index
const existingTargets = {};
for (const rel of (graph.relations || [])) {
  if (rel.type !== APPEARS_RT) continue;
  if (!existingTargets[rel.from]) existingTargets[rel.from] = new Set();
  existingTargets[rel.from].add(rel.to);
}

// ── Apply rules ───────────────────────────────────────────────────────────────
const newRelations = [];
const counters = {};

function addRel(fromId, toSectionId) {
  if (!toSectionId || !entityIds.has(toSectionId)) return false;
  if (existingTargets[fromId]?.has(toSectionId)) return false;
  newRelations.push({ id: randomUUID(), from: fromId, type: APPEARS_RT, to: toSectionId });
  if (!existingTargets[fromId]) existingTargets[fromId] = new Set();
  existingTargets[fromId].add(toSectionId);
  return true;
}

for (const entity of (graph.entities || [])) {
  const name = entity.name || '';
  for (const rule of NAME_RULES) {
    if (rule.match(name)) {
      let added = false;
      for (const sid of rule.sections) {
        if (addRel(entity.id, sid)) added = true;
      }
      if (added) {
        counters[rule.label] = (counters[rule.label] || 0) + 1;
        console.log(`  [${rule.label}] "${name}"`);
      }
      break;
    }
  }
}

// ── Summary ───────────────────────────────────────────────────────────────────
console.log(`\nNew relations generated: ${newRelations.length}`);
for (const [label, count] of Object.entries(counters)) {
  console.log(`  ${label}: ${count} entité(s)`);
}

if (newRelations.length === 0) {
  console.log('Nothing to patch — all target entities already correctly anchored.');
  process.exit(0);
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
