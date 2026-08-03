/**
 * StoryMode helper utilities extracted from graphe.html.
 * Scope: low-risk, data-oriented helpers only.
 */
(function attachGrapheStoryHelpers(globalObj) {
  const DEFAULT_STORY_REGISTRY = { stories: [], viewToStoryId: {} };

  const STORY_FOCUS_ALIASES = {
    'Monétisation': 'Monétisation des cryptomonnaies',
    'Fonctions monétaires': 'II.1.1.a Les critiques instrumentales fondées sur des fonctions monétaires canoniques',
    'Critiques instrumentales': 'II.1.1.a Les critiques instrumentales fondées sur des fonctions monétaires canoniques',
    'Critiques chartalistes': 'Théorie chartaliste',
    'Épreuve d’explicitation de la monnaie': 'Quote — CM comme épreuve d’explicitation de la monnaie',
    'Nominalisme non étatiste': 'Nominalisme monetaire non etatiste',
    'Monetary Institutionalism FR (IMF)': 'Institutionnalisme Monetaire Francophone (IMF)',
    'Usages monétaires': 'Chapitre II - Dépasser la controverse du statut monétaire des CM par un institutionnalisme intéressé aux usages',
    'Usage en compte': 'Archetypal monetary functions',
    'Usage en paiement': 'Systeme de paiement',
    'Liquidité': 'Concept — Liquidité du marché Bitcoin',
    'Convertibilité': "Dilemme de la poule et de l'œuf (bootstrapping monétaire)",
    'Passerelles': 'Services Marchands & Passerelles',
    'Infrastructures de marché': 'Infrastructure monétaire crypto-monétaire',
    'Intermédiation': "Chaîne d'intermédiation sociotechnique",
    'Communauté de paiement': 'Communaute de paiement / Groupe monetaire',
    'Paiement': 'Systeme de paiement',
    'Dette': 'Monnaie dette / Monnaie crédit',
    'Confiance': 'Confiance monetaire',
    'Institutions': 'Institutionnalisme Monetaire Francophone (IMF)',
    'Souveraineté monétaire': 'Souverainete monetaire',
    'Crises': 'Crises comme épreuves d’explicitation',
    'Mise en crise': 'Mise en crise / Remise en ordre',
    'Remise en ordre': 'Mise en crise / Remise en ordre',
    'Gouvernance des cryptomonnaies': 'A. La gouvernance des cryptomonnaies : construction de notre objet de recherche',
    "Crise d’évolution": "Crise d'évolution",
    'Gouvernance publique': 'Gouvernance publique et ouverte',
    'Responsible disclosure': 'Responsible Disclosure',
    'Consensus local': 'Gouvernance de huis clos',
    'Consensus global': 'Gouvernance publique et ouverte',
    'Patch': 'CVE-2018-17144 — Remise en ordre par patch',
    'Esprit communautaire': 'Esprit du code vs Lettre du code',
    'Ethereum Classic': 'Ethereum Classic (ETHC)',
    'Ethereum DAO Hard Fork': 'Ethereum Hard Fork (juillet 2016)',
    // Designe par identifiant, et non par libelle : la migration des sections
    // (patch_13) renomme ce noeud. Un alias par nom serait casse le jour de
    // l'application du patch, et casse aujourd'hui si on l'ecrivait deja au
    // nom d'apres. L'identifiant vaut avant comme apres.
    // = I.3.3 « Ethereum, des recompositions d'alliances contre les rigidites de Bitcoin »
    'Conception politique': '46111186b53041829a0a98218f9611fe',
    'Choix architecturaux': "Normativité de l'architecture et des paramètres Bitcoin",
    'STS': 'Sociology of Science & Technology (STS)',
    'Développement infrastructurel carnavalesque': 'Dynamique carnavalesque du développement infrastructurel',
    'Usages': 'Institutionnalisme intéressé aux usages'
  };

  function normalizeStoryText(s) {
    return String(s || '')
      .normalize('NFD')
      .replace(/[\u0300-\u036f]/g, '')
      .toLowerCase()
      .trim();
  }

  async function loadStoryRegistry(importPath = './story-presets.mjs') {
    try {
      const mod = await import(importPath);
      if (mod && mod.STORY_PRESETS) return mod.STORY_PRESETS;
    } catch (err) {
      console.warn('[story-mode] registre non chargé, fallback vide', err);
    }
    return DEFAULT_STORY_REGISTRY;
  }

  function resolveStoryFocusNodes(stateData, focusNodes = [], aliases = STORY_FOCUS_ALIASES) {
    if (!stateData || !Array.isArray(focusNodes)) return [];
    const entities = stateData.entities || [];
    const byId = new Map(entities.map((e) => [e.id, e]));
    const byName = new Map(entities.map((e) => [e.name, e]));
    const byNorm = new Map();
    entities.forEach((e) => {
      const key = normalizeStoryText(e.name);
      if (!byNorm.has(key)) byNorm.set(key, []);
      byNorm.get(key).push(e);
    });

    const resolved = [];
    focusNodes.forEach((raw) => {
      const canonicalRaw = aliases[raw] || raw;
      let found = byId.get(canonicalRaw) || byName.get(canonicalRaw) || byId.get(raw) || byName.get(raw) || null;
      if (!found) {
        const candidates = byNorm.get(normalizeStoryText(canonicalRaw)) || byNorm.get(normalizeStoryText(raw));
        if (candidates && candidates.length) {
          found = candidates[0];
          if (candidates.length > 1) {
            console.warn('[story-mode] ambiguïté focusNode:', raw, '→', candidates.map((c) => c.name));
          }
        }
      }
      if (!found) {
        console.warn('[story-mode] focusNode introuvable:', raw);
        return;
      }
      resolved.push(found.id);
    });

    return [...new Set(resolved)];
  }

  function mergeStoryStepOptions(defaultStepOptions, step) {
    return {
      ...(defaultStepOptions || {}),
      ...(step || {})
    };
  }


  function getStoryRevealButtonLabel(phase) {
    return phase === 'nodesOnly' ? 'Révéler liens' : 'Masquer liens';
  }

  function formatStoryCitationText(anchor, maxLen = 210) {
    if (!anchor || !anchor.quoteText) return '';
    const rawQuote = String(anchor.quoteText);
    const clipped = rawQuote.length > maxLen
      ? rawQuote.slice(0, Math.max(0, maxLen - 3)) + '…'
      : rawQuote;
    return `« ${clipped} »`;
  }

  function formatStoryCitationPage(anchor) {
    return anchor && anchor.page ? `p. ${anchor.page}` : '';
  }

  function buildStoryBridgeHintHtml(bridges = [], escHtmlFn = (v) => String(v)) {
    const chips = (bridges || []).slice(0, 3).map((bridgeEntityLabel) => {
      const chipLabel = String(bridgeEntityLabel || '').split(' / ')[0];
      return `<span class="story-bridge-chip">${escHtmlFn(chipLabel)}</span>`;
    }).join('');
    return `<span style="opacity:0.5">→</span> ${chips}`;
  }


  function getStoryPanelEmptyStateText() {
    return {
      meta: 'Choisissez un récit pour démarrer.',
      title: '—',
      body: '—'
    };
  }

  function formatStoryStepMetaText(activeStoryStepIndex, totalSteps) {
    return `Étape ${activeStoryStepIndex + 1}/${totalSteps}`;
  }

  function shouldShowStoryBridgeHint(bridges, isLastStep) {
    return Boolean((bridges || []).length) && !isLastStep;
  }
  globalObj.GrapheStoryHelpers = {
    STORY_FOCUS_ALIASES,
    normalizeStoryText,
    loadStoryRegistry,
    resolveStoryFocusNodes,
    mergeStoryStepOptions,
    getStoryRevealButtonLabel,
    formatStoryCitationText,
    formatStoryCitationPage,
    buildStoryBridgeHintHtml,
    getStoryPanelEmptyStateText,
    formatStoryStepMetaText,
    shouldShowStoryBridgeHint,
  };
})(window);
