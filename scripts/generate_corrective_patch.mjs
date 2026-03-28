/**
 * generate_corrective_patch.mjs
 *
 * Applique la matrice corrective (grc20_code_vs_md_corrective_matrix.json) :
 * ajoute des relations `appears_in_section` pour ancrer les entités nommées
 * dans leur chapitre d'élaboration analytique principale.
 *
 * Principe : "Primary textual anchoring overrides relational propagation."
 *
 * Usage :
 *   node scripts/generate_corrective_patch.mjs
 * Produit :
 *   patch_5a_corrective_anchoring.json
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
const PATCH_OUT  = 'patch_5a_corrective_anchoring.json';
console.log(`Input: ${latestFile}  →  Output: ${GRAPH_OUT}`);

// ── ThesisSection anchor IDs (from ThesisSection entities in the graph) ───────
const SECTIONS = {
  // Chap. I — développement infrastructural
  I_2_1:  '93f13f18c6da412292eba80dcd630ac7', // I.2.1 — improvisations carnavalesques
  I_2_2:  '97eb62676b0052c4ab3652fc2bd15535', // I.2.2 — régulations transactionnelles
  I_3_1:  'c5eef5d754c64a30a9d163e59e1d5c88', // I.3.1 — constellation des Altcoins
  I_3_2:  'ed2c565cbede474da7b6144bcb22d753', // I.3.2 — Ethereum : conditions d'émergence
  I_3_3:  '46111186b53041829a0a98218f9611fe', // I.3.3 — différences architecturales Ethereum
  // Chap. II — gouvernance polycentrique / scaling debate
  II_3:   'd622d318825741cda43212d7831a88c7', // II.3 — Au-delà de l'absence de gouvernance
  II_3_2: 'd93cb2ceee6dea674fecc4f44d113643', // II.3.2 — Retournement positif du concept
  II_3_3: '7b3312fed875cffb74320f0a579763c7', // II.3.3 — Les CM réactivent un débat monétaire ancien
  // Chap. III — crises
  III_1:  '5a5684979bf84b37af3771f915f677e2', // III.1 — Crise Bitcoin CVE 2018-17144
  III_1_1:'ac859fd14006e379e55373d31090b6c6', // III.1.1 — mise en crise longue et silencieuse (CVE 2018)
  III_1_2:'0420e53c4c8fd12fef6dcee451a50f61', // III.1.2 — remise en ordre rapide (CVE 2018)
  III_2:  '89663a261c1545c1941ab7f871314a53', // III.2 — politique de crises
  III_2_1:'9fbdbbc3f81ee08fb89b5c5dfbcd2929', // III.2.1 — diversité des crises Bitcoin
  III_3_1:'cf7dfaf42b4f3caa74d2078a8eacc9e6', // III.3.1 — The DAO
};

// ── Name-based correction rules (corrective matrix v1) ───────────────────────
// Each rule: { match(name) → boolean, sections: [sectionId, ...] }
// Multiple sections can be given — typically the most specific one.
const NAME_RULES = [
  // CVE-2018-17144 cluster → Chap. III.1
  {
    match: n => n.includes('CVE-2018-17144'),
    sections: [SECTIONS.III_1_1, SECTIONS.III_1_2],
    label: 'CVE-2018-17144 → III.1',
  },
  // GovernanceProcess for CVE resolution → Chap. III.1
  {
    match: n => n.toLowerCase().includes('cve') && n.toLowerCase().includes('résolution'),
    sections: [SECTIONS.III_1_2],
    label: 'GovernanceProcess CVE résolution → III.1.2',
  },
  // Ethereum emergence events → Chap. I.3
  {
    match: n => n.includes('Ether Genesis Sale') || n.includes('Genesis Sale'),
    sections: [SECTIONS.I_3_2],
    label: 'Ether Genesis Sale → I.3.2',
  },
  {
    match: n => n.includes('Frontier') && n.toLowerCase().includes('ethereum'),
    sections: [SECTIONS.I_3_2],
    label: 'Frontier Ethereum → I.3.2',
  },
  {
    match: n => n.includes('Lancement') && n.toLowerCase().includes('ethereum'),
    sections: [SECTIONS.I_3_2],
    label: 'Lancement Ethereum → I.3.2',
  },
  {
    match: n => (n.includes('Levée de fonds') || n.includes('Levee de fonds')) && n.toLowerCase().includes('ethereum'),
    sections: [SECTIONS.I_3_2],
    label: 'Levée de fonds Ethereum → I.3.2',
  },
  {
    match: n => n.toLowerCase().includes('ethereum') && n.toLowerCase().includes('ico') && !n.toLowerCase().includes('dao'),
    sections: [SECTIONS.I_3_2],
    label: 'Ethereum ICO → I.3.2',
  },
  // Bitcoin infra / ecosystem events → Chap. I.2
  {
    match: n => n === 'BitcoinMarket exchange launch',
    sections: [SECTIONS.I_2_1],
    label: 'BitcoinMarket → I.2.1',
  },
  {
    match: n => n.includes('Bitcoin Foundation creation'),
    sections: [SECTIONS.I_2_2],
    label: 'Bitcoin Foundation creation → I.2.2',
  },
  {
    match: n => n.includes('Migration du code Bitcoin vers GitHub'),
    sections: [SECTIONS.I_2_1],
    label: 'Migration Bitcoin vers GitHub → I.2.1',
  },
  {
    match: n => n.includes('Bitcoin Improvement Proposals standardization') || n.includes('BIP-0001'),
    sections: [SECTIONS.I_2_2],
    label: 'BIP standardisation → I.2.2',
  },
  {
    match: n => n.includes('WordPress accepte les paiements en Bitcoin'),
    sections: [SECTIONS.I_2_1],
    label: 'WordPress Bitcoin → I.2.1',
  },
  {
    match: n => n.includes('eBay') && n.includes('PayPal') && n.includes('Bitcoin'),
    sections: [SECTIONS.I_2_1],
    label: 'eBay/PayPal Bitcoin → I.2.1',
  },
  {
    match: n => n.includes('Casascius'),
    sections: [SECTIONS.I_2_1],
    label: 'Casascius → I.2.1',
  },
  {
    match: n => n.includes('métaprotocole Bitcoin') || n.includes('metaprotocole Bitcoin'),
    sections: [SECTIONS.I_2_1],
    label: 'métaprotocole Bitcoin → I.2.1',
  },
  // Scaling Debate cluster → Chap. II.3
  {
    match: n => n.includes('Scaling Debate'),
    sections: [SECTIONS.II_3_3],
    label: 'Scaling Debate → II.3.3',
  },
  {
    match: n => n === 'Guerre des blocs',
    sections: [SECTIONS.II_3_3],
    label: 'Guerre des blocs → II.3.3',
  },
  {
    match: n => n === 'Big Blockers',
    sections: [SECTIONS.II_3_3],
    label: 'Big Blockers → II.3.3',
  },
  {
    match: n => n.includes('Small Blockers'),
    sections: [SECTIONS.II_3_3],
    label: 'Small Blockers → II.3.3',
  },
];

// ── Load graph ────────────────────────────────────────────────────────────────
const graph = JSON.parse(readFileSync(latestFile, 'utf8'));

const rtByName = {};
for (const rt of (graph.relation_types || [])) rtByName[rt.name] = rt.id;
const APPEARS_RT = rtByName['appears in section'];
if (!APPEARS_RT) { console.error('ERROR: "appears in section" relation type not found.'); process.exit(1); }

// Build existing appears_in_section index
const existingTargets = {}; // entityId → Set<sectionId>
for (const rel of (graph.relations || [])) {
  if (rel.type !== APPEARS_RT) continue;
  if (!existingTargets[rel.from]) existingTargets[rel.from] = new Set();
  existingTargets[rel.from].add(rel.to);
}

// ── Apply rules ───────────────────────────────────────────────────────────────
const newRelations = [];
const counters = {};

function addRel(fromId, toSectionId) {
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
      break; // first matching rule wins
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
