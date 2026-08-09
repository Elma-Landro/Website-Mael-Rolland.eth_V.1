/**
 * ═══════════════════════════════════════════════════════════════════════════
 *  GRC-20 Conversion & Publication Pipeline
 *  Thèse "Au-delà des codes" — Maël Rolland (EHESS, 2024)
 *  mael-rolland.eth · https://mael-rolland.eth.limo
 * ═══════════════════════════════════════════════════════════════════════════
 *
 *  Ce script convertit le format JSON snapshot local (v2/v3/v4/v5)
 *  en ops GRC-20 wire format, publie sur IPFS et ancre onchain dans
 *  un Personal Space Geo Genesis.
 *
 *  PRÉREQUIS
 *  ─────────
 *    node >= 18
 *    npm install @graphprotocol/grc-20 viem
 *
 *  USAGE
 *  ─────
 *    # 1. Dry run — génère les ops sans rien publier
 *    npm run dry-run          # TOUJOURS avant testnet/mainnet
 *
 *    # 2. Publish — publie sur IPFS testnet, ancre onchain
 *    GEO_PRIVATE_KEY=... GEO_SPACE_ID=... GEO_NETWORK=... \
 *      GEO_INPUT=./grc20-these-mael-rolland-v113.json node grc20-publish.mjs
 *          --network TESTNET
 *
 *    # 3. Mainnet (après validation sur testnet)
 *    GEO_PRIVATE_KEY=... GEO_SPACE_ID=... GEO_NETWORK=... \
 *      GEO_INPUT=./grc20-these-mael-rolland-v113.json node grc20-publish.mjs
 *          --network MAINNET
 *
 *    # 4. Créer un nouveau Space (première fois seulement)
 *    GEO_PRIVATE_KEY=... GEO_SPACE_ID=... GEO_NETWORK=... \
 *      GEO_INPUT=./grc20-these-mael-rolland-v113.json node grc20-publish.mjs
 *          --network TESTNET --create-space
 *
 *  VARIABLES D'ENVIRONNEMENT (alternative aux flags)
 *  ──────────────────────────────────────────────────
 *    GEO_PRIVATE_KEY=0x...
 *    GEO_SPACE_ID=ton-space-id-après-création
 *    GEO_NETWORK=TESTNET|MAINNET
 *
 *  SÉCURITÉ
 *  ────────
 *    ⚠️  Ne jamais committer la clé privée dans git.
 *    Utiliser un fichier .env ou la variable d'environnement.
 *    La clé est exportable depuis https://www.geobrowser.io/export-wallet
 *
 * ═══════════════════════════════════════════════════════════════════════════
 */

import { readFileSync, writeFileSync, existsSync } from 'fs';
import { resolve, basename, dirname } from 'path';

// ─────────────────────────────────────────────────────────────────────────────
//  IMPORTS CONDITIONNELS (SDK GRC-20 + viem)
//  On charge dynamiquement pour donner un message d'erreur clair si absent
// ─────────────────────────────────────────────────────────────────────────────
async function loadDeps() {
  try {
    const grc20 = await import('@graphprotocol/grc-20');
    return grc20;
  } catch {
    console.error('\n❌  SDK manquant. Installez-le avec :\n');
    console.error('    npm install @graphprotocol/grc-20 viem\n');
    process.exit(1);
  }
}

// ─────────────────────────────────────────────────────────────────────────────
//  LECTURE DES ARGUMENTS
// ─────────────────────────────────────────────────────────────────────────────
function parseArgs(argv) {
  const args = {};
  for (let i = 2; i < argv.length; i++) {
    const arg = argv[i];
    if (arg.startsWith('--')) {
      const key = arg.slice(2);
      const next = argv[i + 1];
      if (!next || next.startsWith('--')) {
        args[key] = true; // flag booléen
      } else {
        args[key] = next;
        i++;
      }
    }
  }
  return args;
}

const args = parseArgs(process.argv);

const INPUT_FILE   = args['input']       || process.env.GEO_INPUT;
const PRIVATE_KEY  = args['private-key'] || process.env.GEO_PRIVATE_KEY;
const SPACE_ID     = args['space-id']    || process.env.GEO_SPACE_ID;
const NETWORK      = (args['network']    || process.env.GEO_NETWORK || 'TESTNET').toUpperCase();
const DRY_RUN      = !!args['dry-run'];
const CREATE_SPACE = !!args['create-space'];
const BATCH_SIZE   = parseInt(args['batch-size'] || '200');  // ops par Edit IPFS
const AUTHOR_ADDR  = args['author']      || process.env.GEO_AUTHOR; // adresse 0x si dry-run

// ─────────────────────────────────────────────────────────────────────────────
//  CORRESPONDANCE : nom de propriété GRC-20 standard → ID
//  Ces IDs sont les IDs canoniques du Space "System" de Geo Genesis.
//  Source : documentation Geo + SDK examples (constantes connues).
//  Si votre espace définit des types custom, complétez cette map.
// ─────────────────────────────────────────────────────────────────────────────
const SYSTEM_PROPERTY_IDS = {
  // Propriétés natives du standard GRC-20
  name:        'LuBWqZAu6fERECeBI9DZ',   // Name property (system)
  description: 'LA1DqP5v6QAdsgLPqqNH',   // Description property (system)
  types:       'type',                    // Types attribute (système interne)
  // Ajouter ici les IDs de vos types/propriétés après création du Space
};

// ─────────────────────────────────────────────────────────────────────────────
//  CONVERTISSEUR : snapshot JSON → tableau d'ops GRC-20
// ─────────────────────────────────────────────────────────────────────────────

/**
 * Convertit un objet snapshot GRC-20 local en tableau d'ops wire-format.
 *
 * Le format snapshot (notre JSON) est :
 *   { entities: [...], relations: [...], types: [...], relation_types: [...] }
 *
 * Le format wire GRC-20 est une liste plate d'opérations :
 *   { type: 'SET_TRIPLE', triple: { entity, attribute, value: { type, value } } }
 *   { type: 'CREATE_RELATION', relation: { from_entity, to_entity, relation_type } }
 *
 * @param {Object} snapshot  - le JSON local parsé
 * @param {Object} sdk       - le module @graphprotocol/grc-20
 * @returns {{ ops: Array, manifest: Object }}
 */
function convertSnapshotToOps(snapshot, sdk) {
  const { Graph } = sdk;
  const ops = [];
  const manifest = {
    space_name:   snapshot.space?.name || 'Au-delà des codes',
    converted_at: new Date().toISOString(),
    entity_count: snapshot.entities.length,
    relation_count: snapshot.relations.length,
    id_map: {},          // snapshot_id → grc20_id (si différent)
    property_map: {},    // relation_type_id → property_id
    skipped: [],         // entités/relations ignorées avec raison
  };

  // ── 1. Construire les maps de lookup ──────────────────────────────────────
  const typeMap    = Object.fromEntries(snapshot.types.map(t => [t.id, t]));
  const relTypeMap = Object.fromEntries(snapshot.relation_types.map(r => [r.id, r]));
  const entityIds  = new Set(snapshot.entities.map(e => e.id));

  // ── 2. Créer les entités ──────────────────────────────────────────────────
  for (const entity of snapshot.entities) {

    // SET_TRIPLE : name
    if (entity.name) {
      ops.push({
        type: 'SET_TRIPLE',
        triple: {
          entity:    entity.id,
          attribute: SYSTEM_PROPERTY_IDS.name,
          value: {
            type:  'TEXT',
            value: entity.name,
            options: { language: 'fr' },
          },
        },
      });
    }

    // SET_TRIPLE : description
    if (entity.description?.value) {
      ops.push({
        type: 'SET_TRIPLE',
        triple: {
          entity:    entity.id,
          attribute: SYSTEM_PROPERTY_IDS.description,
          value: {
            type:  'TEXT',
            value: entity.description.value,
            options: entity.description.options || { language: 'fr' },
          },
        },
      });
    }

    // SET_TRIPLE : type(s) — référence vers le type d'entité
    for (const typeId of (entity.types || [])) {
      const typeObj = typeMap[typeId];
      if (!typeObj) {
        manifest.skipped.push({ id: entity.id, reason: `type_id inconnu: ${typeId}` });
        continue;
      }
      ops.push({
        type: 'SET_TRIPLE',
        triple: {
          entity:    entity.id,
          attribute: SYSTEM_PROPERTY_IDS.types,
          value: {
            type:  'RELATION',
            value: typeId,
          },
        },
      });
    }

    // SET_TRIPLE : attributs supplémentaires
    for (const [attrKey, attrVal] of Object.entries(entity.attributes || {})) {
      const rawVal = typeof attrVal === 'object' ? attrVal : { type: 'TEXT', value: String(attrVal) };

      // Détecter le type de valeur GRC-20 à partir du type déclaré
      let grcType = rawVal.type || 'TEXT';
      let grcValue = rawVal.value || '';

      // Normalisation : TIME → vérification ISO-8601
      if (grcType === 'TIME') {
        try {
          new Date(grcValue).toISOString(); // valide
        } catch {
          grcType  = 'TEXT';
          manifest.skipped.push({ id: entity.id, attr: attrKey, reason: 'date invalide, conservée en TEXT' });
        }
      }

      // Normalisation : URL → vérification basique
      if (grcType === 'URL') {
        if (!grcValue.startsWith('http')) {
          grcType = 'TEXT';
        }
      }

      ops.push({
        type: 'SET_TRIPLE',
        triple: {
          entity:    entity.id,
          attribute: attrKey,   // l'attribut custom — à mapper vers un ID de propriété si défini dans le Space
          value: {
            type:  grcType,
            value: grcValue,
            ...(rawVal.options ? { options: rawVal.options } : {}),
          },
        },
      });
    }
  }

  // ── 3. Créer les relations ────────────────────────────────────────────────
  let skippedRels = 0;
  for (const rel of snapshot.relations) {
    // Validation : source et cible existent
    if (!entityIds.has(rel.from)) {
      manifest.skipped.push({ rel, reason: `source inconnue: ${rel.from}` });
      skippedRels++;
      continue;
    }
    if (!entityIds.has(rel.to)) {
      manifest.skipped.push({ rel, reason: `cible inconnue: ${rel.to}` });
      skippedRels++;
      continue;
    }
    // Validation : type de relation connu
    if (!relTypeMap[rel.type]) {
      manifest.skipped.push({ rel, reason: `relation_type inconnu: ${rel.type}` });
      skippedRels++;
      continue;
    }

    ops.push({
      type: 'CREATE_RELATION',
      relation: {
        from_entity:   rel.from,
        to_entity:     rel.to,
        relation_type: rel.type,
        ...(rel.index ? { index: rel.index } : {}),
      },
    });
  }

  manifest.ops_count     = ops.length;
  manifest.skipped_count = manifest.skipped.length;
  manifest.relation_skips = skippedRels;

  return { ops, manifest };
}

// ─────────────────────────────────────────────────────────────────────────────
//  DÉCOUPAGE EN BATCHES
//  L'API IPFS de Geo accepte des Edits de taille raisonnable.
//  On découpe en batches de BATCH_SIZE ops pour éviter les timeouts.
// ─────────────────────────────────────────────────────────────────────────────
function splitIntoBatches(ops, size) {
  const batches = [];
  for (let i = 0; i < ops.length; i += size) {
    batches.push(ops.slice(i, i + size));
  }
  return batches;
}

// ─────────────────────────────────────────────────────────────────────────────
//  PUBLICATION IPFS + ANCRAGE ONCHAIN
// ─────────────────────────────────────────────────────────────────────────────
async function publish(ops, sdk, privateKey, spaceId, network, snapshotName) {
  const { Ipfs, Graph, getSmartAccountWalletClient, getWalletClient } = sdk;

  // Obtenir le wallet client
  let walletClient;
  try {
    walletClient = await getSmartAccountWalletClient({ privateKey });
  } catch {
    // Fallback sur le wallet client standard
    walletClient = await getWalletClient({ privateKey, network });
  }

  const { privateKeyToAccount } = await import('viem/accounts');
  const { address } = privateKeyToAccount(privateKey);

  const batches  = splitIntoBatches(ops, BATCH_SIZE);
  const cids     = [];
  const txHashes = [];

  console.log(`\n📡  Publication de ${ops.length} ops en ${batches.length} batch(es) sur ${network}…\n`);

  for (let i = 0; i < batches.length; i++) {
    const batch = batches[i];
    const editName = `${snapshotName} · batch ${i + 1}/${batches.length}`;

    process.stdout.write(`  Batch ${i + 1}/${batches.length} (${batch.length} ops)… `);

    // 1. Publier sur IPFS
    const { cid } = await Ipfs.publishEdit({
      name:    editName,
      ops:     batch,
      author:  address,
      network: network,
    });
    cids.push(cid);
    process.stdout.write(`IPFS ✓ (${cid})… `);

    // 2. Obtenir le calldata depuis l'API Geo
    const apiOrigin = network === 'MAINNET'
      ? Graph.MAINNET_API_ORIGIN
      : Graph.TESTNET_API_ORIGIN;

    const calldataRes = await fetch(`${apiOrigin}/space/${spaceId}/edit/calldata`, {
      method:  'POST',
      headers: { 'Content-Type': 'application/json' },
      body:    JSON.stringify({ cid }),
    });

    if (!calldataRes.ok) {
      const err = await calldataRes.text();
      console.error(`\n❌  Erreur calldata: ${calldataRes.status} — ${err}`);
      throw new Error(`Calldata fetch failed for batch ${i + 1}`);
    }

    const { to, data } = await calldataRes.json();

    // 3. Signer et envoyer la transaction
    const txHash = await walletClient.sendTransaction({
      to,
      value: 0n,
      data,
    });
    txHashes.push(txHash);
    console.log(`TX ✓ (${txHash})`);

    // Délai court entre les batches pour éviter le rate limiting
    if (i < batches.length - 1) {
      await new Promise(r => setTimeout(r, 1200));
    }
  }

  return { cids, txHashes, address };
}

// ─────────────────────────────────────────────────────────────────────────────
//  CRÉATION D'UN NOUVEAU PERSONAL SPACE
// ─────────────────────────────────────────────────────────────────────────────
async function createSpace(sdk, privateKey, spaceName, network) {
  const { Graph, getWalletClient } = sdk;
  const { privateKeyToAccount } = await import('viem/accounts');
  const { address } = privateKeyToAccount(privateKey);

  console.log(`\n🌐  Création du Personal Space "${spaceName}" sur ${network}…`);

  const space = await Graph.createSpace({
    editorAddress: address,
    name:          spaceName,
    network:       network,
  });

  console.log(`✅  Space créé : ${space.id}`);
  console.log(`    → https://www.geobrowser.io/space/${space.id}\n`);
  console.log(`⚠️   Sauvegardez cet ID ! Ajoutez-le en variable d'env :\n`);
  console.log(`    export GEO_SPACE_ID="${space.id}"\n`);

  return space.id;
}

// ─────────────────────────────────────────────────────────────────────────────
//  RAPPORT
// ─────────────────────────────────────────────────────────────────────────────
function printReport(manifest, result) {
  const sep = '─'.repeat(60);
  console.log(`\n${sep}`);
  console.log('  RAPPORT DE CONVERSION GRC-20');
  console.log(sep);
  console.log(`  Espace          : ${manifest.space_name}`);
  console.log(`  Entités         : ${manifest.entity_count}`);
  console.log(`  Relations       : ${manifest.relation_count}`);
  console.log(`  Ops générées    : ${manifest.ops_count}`);
  console.log(`  Ignorées        : ${manifest.skipped_count}`);

  if (manifest.skipped.length > 0 && manifest.skipped.length <= 20) {
    console.log('\n  Éléments ignorés :');
    for (const s of manifest.skipped.slice(0, 20)) {
      console.log(`    ⚠️  ${JSON.stringify(s)}`);
    }
  }

  if (result) {
    console.log('\n  Publication :');
    console.log(`    Adresse wallet : ${result.address}`);
    console.log(`    CIDs IPFS      : ${result.cids.join(', ')}`);
    console.log(`    Transactions   : ${result.txHashes.join(', ')}`);
    console.log(`    GeoBrowser     : https://www.geobrowser.io/space/${SPACE_ID}`);
  }
  console.log(sep + '\n');
}

// ─────────────────────────────────────────────────────────────────────────────
//  POINT D'ENTRÉE PRINCIPAL
// ─────────────────────────────────────────────────────────────────────────────
async function main() {
  console.log('\n◈  GRC-20 Publication Pipeline — Au-delà des codes\n');

  // ── Validation des args ──────────────────────────────────────────────────
  if (!INPUT_FILE) {
    console.error('❌  Fichier d\'entrée requis : --input chemin/vers/snapshot.json\n');
    process.exit(1);
  }
  if (!existsSync(INPUT_FILE)) {
    console.error(`❌  Fichier introuvable : ${INPUT_FILE}\n`);
    process.exit(1);
  }
  if (!DRY_RUN && !PRIVATE_KEY) {
    console.error('❌  Clé privée requise pour publier : --private-key 0x...\n');
    console.error('    Exportez-la depuis https://www.geobrowser.io/export-wallet\n');
    process.exit(1);
  }
  if (!DRY_RUN && !SPACE_ID && !CREATE_SPACE) {
    console.error('❌  Space ID requis : --space-id <id>\n');
    console.error('    Ou créez un nouveau space avec --create-space\n');
    process.exit(1);
  }

  // ── Lecture du snapshot ──────────────────────────────────────────────────
  console.log(`📂  Lecture de ${basename(INPUT_FILE)}…`);
  let snapshot;
  try {
    snapshot = JSON.parse(readFileSync(INPUT_FILE, 'utf-8'));
  } catch (err) {
    console.error(`❌  Erreur de lecture JSON : ${err.message}\n`);
    process.exit(1);
  }

  // Validation minimale
  if (!snapshot.entities || !snapshot.relations || !snapshot.types) {
    console.error('❌  Le fichier ne semble pas être un snapshot GRC-20 valide.\n');
    console.error('    Champs attendus : entities, relations, types, relation_types\n');
    process.exit(1);
  }

  console.log(`   → ${snapshot.entities.length} entités, ${snapshot.relations.length} relations`);
  console.log(`   → ${snapshot.types.length} types, ${snapshot.relation_types.length} types de relations`);

  // ── Chargement du SDK ────────────────────────────────────────────────────
  let sdk = null;
  if (!DRY_RUN) {
    console.log('\n📦  Chargement du SDK @graphprotocol/grc-20…');
    sdk = await loadDeps();
  }

  // ── Conversion ──────────────────────────────────────────────────────────
  console.log('\n🔄  Conversion snapshot → ops GRC-20…');
  const { ops, manifest } = convertSnapshotToOps(snapshot, sdk || { Graph: {} });

  // ── Sortie des ops en JSON (toujours, même sans dry-run) ─────────────────
  const outputBase = INPUT_FILE.replace(/\.json$/, '');
  const opsFile    = `${outputBase}.ops.json`;
  const opsOutput  = {
    meta: {
      source:       basename(INPUT_FILE),
      space_name:   manifest.space_name,
      converted_at: manifest.converted_at,
      ops_count:    ops.length,
      network:      NETWORK,
    },
    ops,
  };
  writeFileSync(opsFile, JSON.stringify(opsOutput, null, 2), 'utf-8');
  console.log(`✅  Ops écrites dans : ${opsFile}`);

  // ── Manifeste JSON ───────────────────────────────────────────────────────
  const manifestFile = `${outputBase}.manifest.json`;
  writeFileSync(manifestFile, JSON.stringify(manifest, null, 2), 'utf-8');
  console.log(`✅  Manifeste écrit dans : ${manifestFile}`);

  // ── Mode dry-run : on s'arrête ici ───────────────────────────────────────
  if (DRY_RUN) {
    printReport(manifest, null);
    console.log('🔍  Mode dry-run : aucune publication effectuée.');
    console.log(`    Inspectez ${basename(opsFile)} pour vérifier les ops.\n`);
    return;
  }

  // ── Création du Space si demandé ─────────────────────────────────────────
  let spaceId = SPACE_ID;
  if (CREATE_SPACE) {
    spaceId = await createSpace(sdk, PRIVATE_KEY, manifest.space_name, NETWORK);
  }

  // ── Publication ──────────────────────────────────────────────────────────
  const snapshotName = snapshot.space?.name || basename(INPUT_FILE, '.json');
  const result = await publish(ops, sdk, PRIVATE_KEY, spaceId, NETWORK, snapshotName);

  // ── Sauvegarder le résultat de publication ───────────────────────────────
  const pubFile = `${outputBase}.published.json`;
  writeFileSync(pubFile, JSON.stringify({
    space_id:   spaceId,
    network:    NETWORK,
    address:    result.address,
    cids:       result.cids,
    tx_hashes:  result.txHashes,
    published_at: new Date().toISOString(),
    batches:    splitIntoBatches(ops, BATCH_SIZE).length,
    ops_count:  ops.length,
  }, null, 2), 'utf-8');

  console.log(`\n✅  Résultat sauvegardé dans : ${basename(pubFile)}`);

  printReport(manifest, result);
}

main().catch(err => {
  console.error('\n❌  Erreur fatale :', err.message || err);
  if (process.env.DEBUG) console.error(err.stack);
  process.exit(1);
});
