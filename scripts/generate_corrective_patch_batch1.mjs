/**
 * generate_corrective_patch_batch1.mjs
 *
 * Applique les corrections SAFE_FIX de Migration/grc20_entity_overrides_batch1.json :
 * ajoute des relations `appears_in_section` pour ancrer les entités nommées
 * dans leur chapitre d'élaboration analytique principal.
 *
 * Usage :
 *   node scripts/generate_corrective_patch_batch1.mjs
 * Produit :
 *   patch_batch1_anchoring.json
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
const PATCH_OUT  = 'patch_batch1_anchoring.json';
console.log(`Input: ${latestFile}  →  Output: ${GRAPH_OUT}`);

// ── ThesisSection anchor IDs ──────────────────────────────────────────────────
const SECTIONS = {
  I_1:    '7a59f028c1014c42bf49e60cf08c4e4b', // I.1 — émergence du protocole Bitcoin
  I_2:    '7fd11e1f8b1f482ba5df7e8b3d92dd7b', // I.2 — développement infrastructural Bitcoin
  I_2_1:  '93f13f18c6da412292eba80dcd630ac7', // I.2.1 — improvisations carnavalesques
  I_2_2:  '97eb62676b0052c4ab3652fc2bd15535', // I.2.2 — régulations transactionnelles
  I_3:    '5bf01b7c03a642db8e07bab25b7e27ef', // I.3 — Ethereum et altcoins
  I_3_2:  'ed2c565cbede474da7b6144bcb22d753', // I.3.2 — Ethereum : conditions d'émergence
  II_3:   'd622d318825741cda43212d7831a88c7', // II.3 — Au-delà de l'absence de gouvernance
  II_3_3: '7b3312fed875cffb74320f0a579763c7', // II.3.3 — Les CM réactivent un débat monétaire ancien
  III_1:  '5a5684979bf84b37af3771f915f677e2', // III.1 — Crise Bitcoin CVE 2018-17144
  III_1_1:'ac859fd14006e379e55373d31090b6c6', // III.1.1 — mise en crise longue et silencieuse
  III_1_2:'0420e53c4c8fd12fef6dcee451a50f61', // III.1.2 — remise en ordre rapide
  III_2:  '89663a261c1545c1941ab7f871314a53', // III.2 — politique de crises
};

// ── Chapter-level section mapping ─────────────────────────────────────────────
// Maps proposed_primaryChapter → most specific available section for anchoring
const CHAPTER_TO_SECTION = {
  'Chap.I':   SECTIONS.I_2,
  'Chap.II':  SECTIONS.II_3,
  'Chap.III': SECTIONS.III_1,
};

// ── Name-based correction rules (batch1 SAFE_FIX entries) ────────────────────
// Each rule: { match(name) → boolean, sections: [sectionId, ...], label: string }
const NAME_RULES = [
  // CVE-2018-17144 cluster → Chap. III.1
  { match: n => n.includes('CVE-2018-17144'),
    sections: [SECTIONS.III_1_1, SECTIONS.III_1_2],
    label: 'CVE-2018-17144 → III.1' },
  { match: n => n === 'Bitcoin CVE 2018-17144',
    sections: [SECTIONS.III_1],
    label: 'Bitcoin CVE 2018-17144 → III.1' },

  // Scaling Debate cluster → Chap. II.3
  { match: n => n.includes('Scaling Debate'),
    sections: [SECTIONS.II_3_3],
    label: 'Scaling Debate → II.3.3' },
  { match: n => n === 'Guerre des blocs (Blocksize War)',
    sections: [SECTIONS.II_3_3],
    label: 'Guerre des blocs (Blocksize War) → II.3.3' },
  { match: n => n === 'Guerre des blocs',
    sections: [SECTIONS.II_3_3],
    label: 'Guerre des blocs → II.3.3' },

  // Ethereum emergence → Chap. I.3
  { match: n => n === 'Campagne de financement Ethereum (ICO 2014)',
    sections: [SECTIONS.I_3_2],
    label: 'Campagne de financement Ethereum → I.3.2' },
  { match: n => n.includes('Ether Genesis Sale'),
    sections: [SECTIONS.I_3_2],
    label: 'Ether Genesis Sale → I.3.2' },
  { match: n => n.includes('Frontier') && n.toLowerCase().includes('ethereum'),
    sections: [SECTIONS.I_3_2],
    label: 'Frontier Ethereum → I.3.2' },
  { match: n => n.includes('Lancement') && n.toLowerCase().includes('ethereum'),
    sections: [SECTIONS.I_3_2],
    label: 'Lancement Ethereum → I.3.2' },
  { match: n => (n.includes('Levée de fonds') || n.includes('Levee de fonds')) && n.toLowerCase().includes('ethereum'),
    sections: [SECTIONS.I_3_2],
    label: 'Levée de fonds Ethereum → I.3.2' },

  // Bitcoin foundational events → Chap. I.2
  { match: n => n.includes('Publication du WP Bitcoin'),
    sections: [SECTIONS.I_2_1],
    label: 'Publication WP Bitcoin → I.2.1' },
  { match: n => n.includes('Publication du code Bitcoin'),
    sections: [SECTIONS.I_2_1],
    label: 'Publication code Bitcoin → I.2.1' },
  { match: n => n.includes('Bitcoin-QT') && n.includes('2009'),
    sections: [SECTIONS.I_2_1],
    label: 'Bitcoin-QT 2009 → I.2.1' },

  // Bitcoin infrastructural development → Chap. I.2
  { match: n => n === 'BitcoinMarket exchange launch',
    sections: [SECTIONS.I_2_1],
    label: 'BitcoinMarket exchange launch → I.2.1' },
  { match: n => n.includes('BitcoinMarket') && n.toLowerCase().includes('plateforme'),
    sections: [SECTIONS.I_2_1],
    label: 'BitcoinMarket plateforme → I.2.1' },
  { match: n => n.includes('Bitcoin Foundation creation') || n.includes('Bitcoin Foundation'),
    sections: [SECTIONS.I_2_2],
    label: 'Bitcoin Foundation → I.2.2' },
  { match: n => n.includes('Fondation Bitcoin') && n.includes('2012'),
    sections: [SECTIONS.I_2_2],
    label: 'Fondation Bitcoin 2012 → I.2.2' },
  { match: n => n.includes('Migration du code Bitcoin vers GitHub'),
    sections: [SECTIONS.I_2_1],
    label: 'Migration Bitcoin vers GitHub → I.2.1' },
  { match: n => n.includes('Bitcoin Improvement Proposals standardization') || n.includes('BIP-0001'),
    sections: [SECTIONS.I_2_2],
    label: 'BIP standardisation → I.2.2' },
  { match: n => n.includes('Bitcoin Faucet'),
    sections: [SECTIONS.I_2_1],
    label: 'Bitcoin Faucet → I.2.1' },
  { match: n => n.includes('MyBitcoin'),
    sections: [SECTIONS.I_2_1],
    label: 'MyBitcoin → I.2.1' },
  { match: n => n.includes('Nakamoto crée le forum Bitcointalk'),
    sections: [SECTIONS.I_2_1],
    label: 'Nakamoto Bitcointalk → I.2.1' },
  { match: n => n.includes('Nakamoto réserve le nom de domaine'),
    sections: [SECTIONS.I_2_1],
    label: 'Nakamoto bitcoin.org → I.2.1' },
  { match: n => n.includes('WordPress accepte les paiements en Bitcoin'),
    sections: [SECTIONS.I_2_1],
    label: 'WordPress Bitcoin → I.2.1' },
  { match: n => n.includes('eBay') && n.includes('PayPal') && n.includes('Bitcoin'),
    sections: [SECTIONS.I_2_1],
    label: 'eBay/PayPal Bitcoin → I.2.1' },
  { match: n => n.includes('Casascius'),
    sections: [SECTIONS.I_2_1],
    label: 'Casascius → I.2.1' },
  { match: n => n.includes('métaprotocole Bitcoin') || n.includes('Innovations de métaprotocole'),
    sections: [SECTIONS.I_2_1],
    label: 'Métaprotocole Bitcoin → I.2.1' },
  { match: n => n.includes('Colored Coins') && n.includes('Bitcoin'),
    sections: [SECTIONS.I_2_1],
    label: 'Colored Coins Bitcoin → I.2.1' },

  // DevelopmentPhase → Chap. I
  { match: n => n === 'Phase de preuve de concept',
    sections: [SECTIONS.I_2_1],
    label: 'Phase de preuve de concept → I.2.1' },
  { match: n => n === 'Phase de péché',
    sections: [SECTIONS.I_2_2],
    label: 'Phase de péché → I.2.2' },

  // Governance concepts → Chap. III
  { match: n => n === 'Politique de crise',
    sections: [SECTIONS.III_2],
    label: 'Politique de crise → III.2' },
  { match: n => n === 'Politique de crises',
    sections: [SECTIONS.III_2],
    label: 'Politique de crises → III.2' },
  { match: n => n === 'Mise en crise / Remise en ordre',
    sections: [SECTIONS.III_1, SECTIONS.III_2],
    label: 'Mise en crise/Remise en ordre → III.1-III.2' },
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
  if (!toSectionId) return false;
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
