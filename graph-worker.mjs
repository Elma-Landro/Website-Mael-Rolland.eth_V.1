/**
 * ═══════════════════════════════════════════════════════════════════════════
 *  Cloudflare Worker — GRC-20 Graph API avec x402
 *  Thèse "Au-delà des codes" — Maël Rolland (EHESS, 2024)
 * ═══════════════════════════════════════════════════════════════════════════
 *
 *  DÉPLOIEMENT
 *  ───────────
 *    1. Installer Wrangler :  npm install -g wrangler
 *    2. Se connecter :        wrangler login
 *    3. Configurer wrangler.toml (voir bas du fichier)
 *    4. Déployer :            wrangler deploy
 *
 *  VARIABLES D'ENVIRONNEMENT (wrangler.toml ou dashboard CF)
 *  ───────────────────────────────────────────────────────────
 *    IPFS_CID          CID IPFS de votre graphe publié (ex: bafyrei...)
 *    WALLET_ADDRESS    Adresse ENS/Ethereum pour recevoir les paiements x402
 *    PRICE_USDC        Prix par requête en USDC (défaut: "0.001")
 *    GRAPH_URL_FALLBACK URL fallback si IPFS indisponible (GitHub raw)
 *    MODE              "free" | "x402" | "x402-optional" (défaut: free)
 *
 *  ENDPOINTS
 *  ─────────
 *    GET  /               Info sur le graphe + liens
 *    GET  /graph          Graphe GRC-20 complet (JSON)
 *    GET  /graph?entity=  Entité unique + voisinage
 *    GET  /graph?type=    Toutes les entités d'un type
 *    GET  /graph?search=  Recherche full-text sur les noms
 *    GET  /graph?depth=2  Contrôle la profondeur du voisinage
 *    GET  /stats          Statistiques du graphe (public, gratuit)
 *    GET  /types          Liste des types d'entités (public, gratuit)
 *
 *  COMPORTEMENT x402
 *  ─────────────────
 *    MODE "free"           → toujours 200, aucun paiement requis
 *    MODE "x402-optional"  → 200 sans paiement, header x402 présent pour info
 *    MODE "x402"           → 402 si pas de paiement, débloquer avec USDC
 *
 * ═══════════════════════════════════════════════════════════════════════════
 */

// ─────────────────────────────────────────────────────────────────────────────
//  CONFIGURATION PAR DÉFAUT
// ─────────────────────────────────────────────────────────────────────────────
const DEFAULTS = {
  PRICE_USDC:   '0.001',
  MODE:         'free',
  CACHE_TTL:    3600,   // secondes — le graphe change peu souvent
  MAX_DEPTH:    3,      // profondeur max de voisinage pour éviter les timeouts
  CORS_ORIGIN:  '*',
};

// Passerelles IPFS publiques (fallback en cascade)
const IPFS_GATEWAYS = [
  'https://ipfs.io/ipfs/',
  'https://cloudflare-ipfs.com/ipfs/',
  'https://gateway.pinata.cloud/ipfs/',
];

// ─────────────────────────────────────────────────────────────────────────────
//  HEADERS COMMUNS
// ─────────────────────────────────────────────────────────────────────────────
function commonHeaders(env) {
  const priceUsdc = env.PRICE_USDC || DEFAULTS.PRICE_USDC;
  const walletAddr = env.WALLET_ADDRESS || '0x0000000000000000000000000000000000000000';

  return {
    'Content-Type':                'application/json',
    'Access-Control-Allow-Origin': DEFAULTS.CORS_ORIGIN,
    'Access-Control-Allow-Methods':'GET, OPTIONS',
    'Access-Control-Allow-Headers':'Authorization, X-Payment, Content-Type',
    // Header x402 informatif (toujours présent)
    'X-Payment-Info':  JSON.stringify({
      scheme:   'exact',
      network:  'eip155:8453',          // Base
      maxAmountRequired: String(Math.round(parseFloat(priceUsdc) * 1e6)),
      resource: 'GRC-20 Knowledge Graph — Au-delà des codes',
      description: 'Accès au graphe de connaissances de la thèse de Maël Rolland (EHESS 2024)',
      mimeType:    'application/json',
      payTo:       walletAddr,
      asset:       '0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913', // USDC Base
    }),
    'X-Graph-Standard':   'GRC-20',
    'X-Graph-Author':     'mael-rolland.eth',
    'X-Graph-ENS':        'https://mael-rolland.eth.limo',
  };
}

// ─────────────────────────────────────────────────────────────────────────────
//  VÉRIFICATION DE PAIEMENT x402
// ─────────────────────────────────────────────────────────────────────────────
async function checkPayment(request, env) {
  const mode = env.MODE || DEFAULTS.MODE;
  if (mode === 'free') return { paid: true };

  const paymentHeader = request.headers.get('X-Payment') || request.headers.get('Authorization');

  if (!paymentHeader) {
    if (mode === 'x402-optional') return { paid: true, optional: true };
    return { paid: false };
  }

  // En production : vérifier la signature USDC via un facilitateur x402.
  // Ici implémentation simplifiée — remplacer par l'appel au facilitateur Coinbase CDP.
  // Voir : https://docs.cdp.coinbase.com/x402/welcome
  //
  // const facilitatorRes = await fetch('https://api.developer.coinbase.com/rpc/v1/base/verify-payment', {
  //   method: 'POST',
  //   headers: { 'Content-Type': 'application/json' },
  //   body: JSON.stringify({ payment: paymentHeader, ... }),
  // });
  // const { valid } = await facilitatorRes.json();
  // return { paid: valid };

  // Pour l'instant : accept tout header de paiement présent (à remplacer)
  return { paid: true, payment: paymentHeader };
}

// ─────────────────────────────────────────────────────────────────────────────
//  RÉPONSE 402 PAYMENT REQUIRED
// ─────────────────────────────────────────────────────────────────────────────
function paymentRequiredResponse(env) {
  const priceUsdc  = env.PRICE_USDC || DEFAULTS.PRICE_USDC;
  const walletAddr = env.WALLET_ADDRESS || '0x0000000000000000000000000000000000000000';

  const body = {
    x402Version: 1,
    accepts: [{
      scheme:             'exact',
      network:            'eip155:8453',
      maxAmountRequired:  String(Math.round(parseFloat(priceUsdc) * 1e6)),
      resource:           'https://api.mael-rolland.eth.limo/graph',
      description:        'GRC-20 Knowledge Graph — Au-delà des codes (EHESS, 2024)',
      mimeType:           'application/json',
      payTo:              walletAddr,
      maxTimeoutSeconds:  300,
      asset:              '0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913',
      extra: {
        name:   'USDC',
        version:'2',
      },
    }],
    error: 'Payment required to access this knowledge graph',
  };

  return new Response(JSON.stringify(body, null, 2), {
    status:  402,
    headers: {
      ...commonHeaders(env),
      'Content-Type': 'application/json',
    },
  });
}

// ─────────────────────────────────────────────────────────────────────────────
//  CHARGEMENT DU GRAPHE DEPUIS IPFS (avec cache KV si disponible)
// ─────────────────────────────────────────────────────────────────────────────
async function loadGraph(env, ctx) {
  const cid      = env.IPFS_CID;
  const cacheKey = `graph:${cid || 'fallback'}`;

  // 1. Tentative cache KV (Cloudflare KV binding "GRAPH_CACHE")
  if (env.GRAPH_CACHE && cid) {
    const cached = await env.GRAPH_CACHE.get(cacheKey, 'json');
    if (cached) return cached;
  }

  // 2. Tentative IPFS (cascade de gateways)
  let data = null;
  if (cid) {
    for (const gateway of IPFS_GATEWAYS) {
      try {
        const res = await fetch(`${gateway}${cid}`, {
          headers: { 'Accept': 'application/json' },
          cf: { cacheTtl: DEFAULTS.CACHE_TTL },
        });
        if (res.ok) {
          data = await res.json();
          break;
        }
      } catch {
        // Essayer la prochaine gateway
      }
    }
  }

  // 3. Fallback GitHub raw (si configuré)
  if (!data && env.GRAPH_URL_FALLBACK) {
    try {
      const res = await fetch(env.GRAPH_URL_FALLBACK, {
        cf: { cacheTtl: DEFAULTS.CACHE_TTL },
      });
      if (res.ok) data = await res.json();
    } catch {}
  }

  // 4. Mise en cache KV pour les prochaines requêtes
  if (data && env.GRAPH_CACHE && cid) {
    ctx.waitUntil(
      env.GRAPH_CACHE.put(cacheKey, JSON.stringify(data), { expirationTtl: DEFAULTS.CACHE_TTL })
    );
  }

  return data;
}

// ─────────────────────────────────────────────────────────────────────────────
//  FILTRES ET REQUÊTES SUR LE GRAPHE
// ─────────────────────────────────────────────────────────────────────────────
function filterGraph(data, params) {
  if (!data) return null;

  const entityId = params.get('entity');
  const typeName = params.get('type');
  const search   = params.get('search')?.toLowerCase();
  const depth    = Math.min(parseInt(params.get('depth') || '1'), DEFAULTS.MAX_DEPTH);

  // Cas 1 : entité spécifique + voisinage
  if (entityId) {
    const entity = data.entities.find(e => e.id === entityId || e.name === entityId);
    if (!entity) return { error: `Entité "${entityId}" introuvable`, code: 404 };

    const visited = new Set([entity.id]);
    let frontier  = [entity.id];

    for (let d = 0; d < depth; d++) {
      const next = [];
      for (const rel of data.relations) {
        if (frontier.includes(rel.from) && !visited.has(rel.to)) {
          visited.add(rel.to); next.push(rel.to);
        }
        if (frontier.includes(rel.to) && !visited.has(rel.from)) {
          visited.add(rel.from); next.push(rel.from);
        }
      }
      frontier = next;
    }

    return {
      query:     { entity: entityId, depth },
      entities:  data.entities.filter(e => visited.has(e.id)),
      relations: data.relations.filter(r => visited.has(r.from) && visited.has(r.to)),
      types:     data.types,
      relation_types: data.relation_types,
    };
  }

  // Cas 2 : filtrer par type
  if (typeName) {
    const typeObj = data.types.find(t =>
      t.name.toLowerCase() === typeName.toLowerCase()
    );
    if (!typeObj) return { error: `Type "${typeName}" inconnu`, code: 404 };

    const entities = data.entities.filter(e => e.types?.includes(typeObj.id));
    const eIds     = new Set(entities.map(e => e.id));

    return {
      query:     { type: typeName },
      entities,
      relations: data.relations.filter(r => eIds.has(r.from) && eIds.has(r.to)),
      types:     data.types,
      relation_types: data.relation_types,
    };
  }

  // Cas 3 : recherche full-text
  if (search) {
    const entities = data.entities.filter(e =>
      e.name?.toLowerCase().includes(search) ||
      e.description?.value?.toLowerCase().includes(search)
    );
    const eIds = new Set(entities.map(e => e.id));

    return {
      query:     { search },
      entities,
      relations: data.relations.filter(r => eIds.has(r.from) && eIds.has(r.to)),
      types:     data.types,
      relation_types: data.relation_types,
    };
  }

  // Cas 4 : graphe complet
  return data;
}

// ─────────────────────────────────────────────────────────────────────────────
//  HANDLER PRINCIPAL
// ─────────────────────────────────────────────────────────────────────────────
export default {
  async fetch(request, env, ctx) {
    const url    = new URL(request.url);
    const path   = url.pathname;
    const method = request.method;
    const params = url.searchParams;
    const headers = commonHeaders(env);

    // CORS preflight
    if (method === 'OPTIONS') {
      return new Response(null, { status: 204, headers });
    }

    // ── Route : / (index) ──────────────────────────────────────────────────
    if (path === '/' || path === '') {
      return new Response(JSON.stringify({
        name:        'GRC-20 Knowledge Graph API — Au-delà des codes',
        author:      'Maël Rolland (EHESS, 2024)',
        ens:         'mael-rolland.eth',
        site:        'https://mael-rolland.eth.limo',
        standard:    'GRC-20',
        ipfs_cid:    env.IPFS_CID || null,
        mode:        env.MODE || DEFAULTS.MODE,
        endpoints: {
          '/graph':          'Graphe complet',
          '/graph?entity=X': 'Entité + voisinage (depth=1..3)',
          '/graph?type=X':   'Entités par type',
          '/graph?search=X': 'Recherche full-text',
          '/stats':          'Statistiques (gratuit)',
          '/types':          'Types d\'entités (gratuit)',
        },
        x402: {
          enabled: (env.MODE || DEFAULTS.MODE) !== 'free',
          price_usdc: env.PRICE_USDC || DEFAULTS.PRICE_USDC,
          network:    'Base (eip155:8453)',
        },
      }, null, 2), { status: 200, headers });
    }

    // ── Route : /stats (toujours gratuite) ────────────────────────────────
    if (path === '/stats') {
      const data = await loadGraph(env, ctx);
      if (!data) {
        return new Response(JSON.stringify({ error: 'Graphe non disponible' }), { status: 503, headers });
      }
      const typeCounts = {};
      for (const e of data.entities) {
        for (const tid of (e.types || [])) {
          const t = data.types.find(t => t.id === tid);
          const name = t ? t.name : tid;
          typeCounts[name] = (typeCounts[name] || 0) + 1;
        }
      }
      return new Response(JSON.stringify({
        entities:       data.entities.length,
        relations:      data.relations.length,
        types:          data.types.length,
        relation_types: data.relation_types.length,
        by_type:        typeCounts,
        space:          data.space,
      }, null, 2), { status: 200, headers });
    }

    // ── Route : /types (toujours gratuite) ──────────────────────────────────
    if (path === '/types') {
      const data = await loadGraph(env, ctx);
      if (!data) {
        return new Response(JSON.stringify({ error: 'Graphe non disponible' }), { status: 503, headers });
      }
      return new Response(JSON.stringify({
        types:          data.types,
        relation_types: data.relation_types,
      }, null, 2), { status: 200, headers });
    }

    // ── Route : /graph (payante selon le mode) ────────────────────────────
    if (path === '/graph') {

      // Vérification paiement x402
      const { paid } = await checkPayment(request, env);
      if (!paid) {
        return paymentRequiredResponse(env);
      }

      // Chargement du graphe
      const data = await loadGraph(env, ctx);
      if (!data) {
        return new Response(JSON.stringify({
          error:    'Graphe non disponible',
          detail:   'IPFS_CID non configuré ou gateway inaccessible',
          fallback: env.GRAPH_URL_FALLBACK || null,
        }), { status: 503, headers });
      }

      // Filtrage selon les query params
      const result = filterGraph(data, params);
      if (result?.code) {
        return new Response(JSON.stringify({ error: result.error }), { status: result.code, headers });
      }

      return new Response(JSON.stringify(result, null, 2), {
        status: 200,
        headers: {
          ...headers,
          'X-Ops-Count': String(result.entities?.length || 0),
          'Cache-Control': `public, max-age=${DEFAULTS.CACHE_TTL}`,
        },
      });
    }

    // ── 404 ───────────────────────────────────────────────────────────────
    return new Response(JSON.stringify({ error: 'Endpoint inconnu', path }), { status: 404, headers });
  },
};

/**
 * ═══════════════════════════════════════════════════════════════════════════
 *  wrangler.toml — À placer à la racine du repo (ne pas committer les secrets)
 * ═══════════════════════════════════════════════════════════════════════════
 *
 * name = "grc20-graph-api"
 * main = "graph-worker.mjs"
 * compatibility_date = "2025-01-01"
 * 
 * [vars]
 * MODE = "free"
 * PRICE_USDC = "0.001"
 * 
 * # Après publication IPFS :
 * # IPFS_CID = "bafyrei..."
 * # WALLET_ADDRESS = "0x..."
 * # GRAPH_URL_FALLBACK = "https://raw.githubusercontent.com/Elma-Landro/Website-Mael-Rolland.eth_V.1/main/grc20-these-mael-rolland-v112.json"
 * 
 * # Cache KV (optionnel mais recommandé)
 * [[kv_namespaces]]
 * binding = "GRAPH_CACHE"
 * id = "votre-kv-namespace-id"
 * 
 * # Routes (si domaine custom)
 * [[routes]]
 * pattern = "api.mael-rolland.eth.limo/*"
 * zone_name = "mael-rolland.eth.limo"
 *
 * ═══════════════════════════════════════════════════════════════════════════
 *  Secrets (via wrangler secret put, jamais dans le toml)
 * ═══════════════════════════════════════════════════════════════════════════
 *
 * wrangler secret put GEO_PRIVATE_KEY
 * wrangler secret put WALLET_ADDRESS
 *
 * ═══════════════════════════════════════════════════════════════════════════
 */
