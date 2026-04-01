export const STORY_PRESETS = {
  viewToStoryId: {
    monetisation: 'chapitre-ii-monetisation',
    'qui-gouverne': 'qui-gouverne-reellement',
    matrice: 'structure-these',
    'these-backbone': 'thesis-backbone',
    'gouvernance-ordinaire': 'gouvernance-ordinaire',
    'gouvernance-crise': 'gouvernance-crise'
  },
  stories: [
    {
      id: 'gouvernance-ordinaire',
      label: 'Gouvernance ordinaire (sur le protocole)',
      layoutTarget: 'qui-gouverne',
      intro: "Comment la gouvernance fonctionne en régime ordinaire : acteurs, dispositifs et arènes hors moment de crise ouverte.",
      defaultStepOptions: {
        edgeMode: 'strict',
        includeNeighbors: false,
        secondaryDepth: 0,
        hideBackbone: true,
        fitTargets: 'primary'
      },
      steps: [
        {
          id: 'go1',
          title: 'Gouverner sur l’infrastructure',
          body: 'La gouvernance ordinaire passe par le travail des mainteneurs, des revues de code et des accès de publication.',
          focusNodes: ["Gouvernance sur l'infrastructure", 'Développeurs Core (mainteneurs avec accès commit)', 'Pull Request (PR)', 'Bitcoin Core (repo)'],
          cameraPreset: 'cluster'
        },
        {
          id: 'go2',
          title: 'Arènes de coordination',
          body: 'Les arènes de discussion distribuent la production de consensus en dehors des épisodes critiques.',
          focusNodes: ['GitHub Bitcoin Core', 'Bitcoin-dev Mailing List', 'Bitcointalk Forum', 'All Core Dev Meetings (Ethereum)'],
          cameraPreset: 'cluster'
        },
        {
          id: 'go3',
          title: 'Règle et discrétion en pratique',
          body: 'La gouvernance ordinaire combine règles codées et marges discrétionnaires de coordination.',
          focusNodes: ['Règle contre discrétion (Rules vs Discretion)', 'Discretion contrainte', 'Quote — consensus social (discrétion) prime sur la règle'],
          cameraPreset: 'tight',
          sourceQuoteId: 'anchor-4934a3d8'   // intro · p.25
        },
        {
          id: 'go4',
          title: 'Sortie : vers la gouvernance de crise',
          body: 'Ce régime ordinaire sert de base, mais les crises rendent visibles des arbitrages autrement implicites.',
          focusNodes: ['Gouvernance duale', 'Crises comme épreuves d’explicitation', 'Bitcoin CVE 2018-17144'],
          cameraPreset: 'wide',
          sourceQuoteId: 'anchor-c6fadcf4'   // ch2 · p.50
        }
      ]
    },
    {
      id: 'gouvernance-crise',
      label: 'Gouvernance de crise (huis clos vs publique)',
      layoutTarget: 'matrice',
      intro: "Comparer la gouvernance de huis clos et la gouvernance publique d’exception à travers CVE et DAO.",
      defaultStepOptions: {
        edgeMode: 'strict',
        includeNeighbors: false,
        secondaryDepth: 0,
        hideBackbone: true,
        fitTargets: 'primary'
      },
      steps: [
        {
          id: 'gc1',
          title: 'Huis clos (CVE)',
          body: "La CVE 2018 illustre une coordination discrète, restreinte et séquencée.",
          focusNodes: ['Bitcoin CVE 2018-17144', 'Gouvernance de huis clos', 'Divulgation responsable', 'Bitcoin Core (repo)'],
          cameraPreset: 'cluster',
          sourceQuoteId: 'anchor-0b39eeba'   // ch3 · p.225
        },
        {
          id: 'gc2',
          title: 'Public d’exception (DAO)',
          body: "The DAO transforme la crise en controverse publique sur le devenir du protocole.",
          focusNodes: ['Attaque de The DAO', 'Ethereum Hard Fork (juillet 2016)', 'Carbon Vote (DAO Fork, juin-juillet 2016)', 'Secession Ethereum Classic'],
          cameraPreset: 'cluster',
          sourceQuoteId: 'anchor-37716e6b'   // ch3 · p.299
        },
        {
          id: 'gc3',
          title: 'Contraste de modes de consensus',
          body: "Les deux cas révèlent des modalités différentes de production du consensus et de gestion du dissensus.",
          focusNodes: ['Gouvernance duale', 'Gouvernance polycentrique', 'Argument — Les crises comme révélateurs de la gouvernance duale et polycentrique'],
          cameraPreset: 'tight',
          sourceQuoteId: 'anchor-5efd9565'   // ch3 · p.223
        },
        {
          id: 'gc4',
          title: 'Boucle de retour théorique',
          body: "La gouvernance de crise confirme la thèse d’une gouvernance sur l’infrastructure conflictuelle et polycentrique.",
          focusNodes: ['Quote — gouvernance sur l’infrastructure conflictuelle et polycentrique', 'Conclusion générale', 'Gouvernance polycentrique'],
          cameraPreset: 'wide',
          sourceQuoteId: 'anchor-fb610652'   // conclusion · p.336
        }
      ]
    },
    {
      id: 'chapitre-ii-monetisation',
      label: 'Chapitre II — Statut & monétisation',
      layoutTarget: 'monetisation',
      intro: "Parcours théorique du Chapitre II : statut monétaire, usages, communauté de paiement et articulation règle/discrétion.",
      defaultStepOptions: {
        edgeMode: 'strict',
        includeNeighbors: false,
        secondaryDepth: 0,
        hideBackbone: true,
        fitTargets: 'primary'
      },
      steps: [
        {
          id: 'cm1',
          title: 'Point d’entrée : controverse de statut',
          body: "Le chapitre s'ouvre sur la controverse du statut monétaire des CM et le besoin d'un cadre non réducteur.",
          focusNodes: ['Statut monétaire des cryptomonnaies', 'Controverse statut monétaire des cryptomonnaies'],
          cameraPreset: 'tight',
          sourceQuoteId: 'anchor-ee9ea714'   // ch2 · p.142
        },
        {
          id: 'cm2',
          title: 'Pivot institutionnaliste',
          body: "La thèse déplace l'analyse vers un institutionnalisme intéressé aux usages effectifs.",
          focusNodes: ['Institutionnalisme intéressé aux usages', 'Monétisation des cryptomonnaies', 'II.2 « Pourtant, elles font monnaie ! » : à l\'aune d\'un nominalisme « non étatiste » attentif aux usages'],
          cameraPreset: 'cluster',
          sourceQuoteId: 'anchor-dce8efe4'   // ch2 · p.142
        },
        {
          id: 'cm3',
          title: 'Monnaie comme système de paiement',
          body: "La monétisation est lue comme processus socio-institutionnel, via dispositifs de paiement et liquidité.",
          focusNodes: ['II.2.2 — La monnaie comme système de paiement : monétisation et liquidité de dettes hétérogènes', 'Concept — Liquidité du marché Bitcoin', 'Communaute de paiement / Groupe monetaire'],
          cameraPreset: 'cluster'
        },
        {
          id: 'cm4',
          title: 'Épreuve d’explicitation',
          body: "Les cryptomonnaies servent d’épreuve d’explicitation de la monnaie et de ses conditions institutionnelles.",
          focusNodes: ['Crises comme épreuves d’explicitation', 'Monétisation des cryptomonnaies', 'Statut monétaire des cryptomonnaies'],
          cameraPreset: 'tight',
          sourceQuoteId: 'anchor-c6fadcf4'   // ch2 · p.50
        },
        {
          id: 'cm5',
          title: 'Règle versus discrétion',
          body: "Le chapitre réarticule la controverse règle/discrétion à l’aune des pratiques de gouvernance monétaire.",
          focusNodes: ['Règle contre discrétion (Rules vs Discretion)', 'Discretion contrainte', 'Quote — consensus social (discrétion) prime sur la règle'],
          cameraPreset: 'tight',
          sourceQuoteId: 'anchor-4934a3d8'   // intro · p.25 (référence théorique structurante)
        },
        {
          id: 'cm6',
          title: 'Sortie vers la gouvernance',
          body: "La clarification monétaire prépare l’entrée en Chapitre III : qui gouverne, comment, et dans quelles arènes.",
          focusNodes: ['Gouvernance duale', 'Gouvernance polycentrique', 'Argument — Les crises comme révélateurs de la gouvernance duale et polycentrique'],
          cameraPreset: 'wide',
          sourceQuoteId: 'anchor-5efd9565'   // ch3 · p.223 (pont II -> III)
        }
      ]
    },
    {
      id: 'monetisation-cryptos',
      label: 'Monétisation des cryptomonnaies',
      layoutTarget: 'monetisation',
      intro: 'Comment les cryptomonnaies font monnaie dans des communautés de paiement.',
      defaultStepOptions: {
        edgeMode: 'strict',
        includeNeighbors: false,
        secondaryDepth: 0,
        hideBackbone: true,
        fitTargets: 'primary'
      },
      steps: [
        {
          id: 'm1',
          title: 'Une monnaie ne naît pas seule',
          body: 'Les cryptomonnaies ne deviennent pas monnaie par simple existence technique. Leur monétisation dépend d’usages, d’infrastructures d’accès et de circuits de circulation.',
          focusNodes: ['Monétisation des cryptomonnaies', 'UCN BTC', 'UCN ETH', 'Communaute de paiement / Groupe monetaire'],
          cameraPreset: 'cluster'
        },
        {
          id: 'm2',
          title: 'Émettre une unité native',
          body: 'Bitcoin et Ethereum encadrent l’émission de leurs unités natives par des règles de monnayage qui organisent le système de paiement.',
          focusNodes: ['UCN BTC', 'UCN ETH', 'Proof of Work (PoW)', 'Halving / Monnayage programmatique', 'Ether Genesis Sale (ICO Ethereum 2014)'],
          cameraPreset: 'tight'
        },
        {
          id: 'm3',
          title: 'Circuler via des passerelles',
          body: 'La diffusion dépend de marchés, de paires d’échange et de passerelles qui rendent la commensurabilité concrète.',
          focusNodes: ['NewLibertyStandard', 'InfrastructureEvent — Première plateforme d’échange BTC (BitcoinMarket.com)', 'Coinbase', 'Kraken', 'Services Marchands & Passerelles'],
          cameraPreset: 'cluster',
          edgeMode: 'neighbors',
          includeNeighbors: true,
          secondaryDepth: 1,
          maxSecondaryPerTarget: 3,
          fitTargets: 'primary+secondary'
        },
        {
          id: 'm4',
          title: 'Accéder et conserver',
          body: 'Wallets, custodians et processeurs de paiement rendent l’usage praticable. L’accès est déjà une forme d’institution.',
          focusNodes: ['Electrum wallet', 'MyBitcoin', 'Ledger', 'Trezor', 'BitPay'],
          cameraPreset: 'cluster',
          edgeMode: 'neighbors',
          includeNeighbors: true,
          secondaryDepth: 1,
          maxSecondaryPerTarget: 3,
          fitTargets: 'primary+secondary'
        },
        {
          id: 'm5',
          title: 'Monétisation et gouvernance',
          body: 'La monétisation durable suppose des institutions et une gouvernance capables de maintenir la capacité d’usage collective.',
          focusNodes: ['Gouvernance polycentrique', 'Bitcoin Core (repo)', 'Core Developers (Bitcoin)', "Bourses d'échange (exchanges)"],
          cameraPreset: 'wide',
          edgeMode: 'neighbors',
          includeNeighbors: true,
          secondaryDepth: 1,
          maxSecondaryPerTarget: 4,
          hideBackbone: true,
          fitTargets: 'primary+secondary'
        }
      ]
    },
    {
      id: 'qui-gouverne-reellement',
      label: 'Qui gouverne réellement ?',
      layoutTarget: 'qui-gouverne',
      intro: 'Déconstruire le mythe du code seul et montrer la gouvernance distribuée.',
      defaultStepOptions: {
        edgeMode: 'neighbors',
        includeNeighbors: true,
        secondaryDepth: 1,
        maxSecondaryPerTarget: 4,
        hideBackbone: true,
        fitTargets: 'primary+secondary'
      },
      steps: [
        {
          id: 'q1',
          title: 'Le mythe du code seul',
          body: 'Le récit coiner radical présente un système régulé uniquement par le code, sans gouvernance humaine légitime.',
          focusNodes: ['Code is Law', 'II.3 Au‑delà de la revendication d’une absence de gouvernance !', 'Neutralité de la monnaie'],
          cameraPreset: 'tight',
          edgeMode: 'strict',
          includeNeighbors: false,
          fitTargets: 'primary'
        },
        {
          id: 'q2',
          title: 'Gouverner sur l’infrastructure',
          body: 'Maintenance, publication, hiérarchie des accès et arbitrages structurent une gouvernance sur l’infrastructure.',
          focusNodes: ['Bitcoin Core (repo)', 'Core Developers (Ethereum)', 'Développeurs Core (mainteneurs avec accès commit)', 'Pull Request (PR)'],
          cameraPreset: 'cluster',
          hideRelationTypes: ['partOf', 'source']
        },
        {
          id: 'q3',
          title: 'Les arènes',
          body: 'La gouvernance se distribue dans des arènes multiples : forges, mailing lists, forums et réunions.',
          focusNodes: ['GitHub Bitcoin Core', 'Bitcoin-dev Mailing List', 'Bitcointalk Forum', 'All Core Dev Meetings (Ethereum)', 'Carbon Vote (DAO Fork, juin-juillet 2016)'],
          cameraPreset: 'cluster',
          hideRelationTypes: ['partOf', 'source', 'citedIn']
        },
        {
          id: 'q4',
          title: 'La thèse',
          body: 'La vraie question n’est pas de savoir s’il y a gouvernance, mais sous quelle forme, avec quels acteurs et quelle légitimité.',
          focusNodes: ['Gouvernance duale', 'Gouvernance polycentrique', 'Algorithme de consensus'],
          cameraPreset: 'wide',
          edgeMode: 'strict',
          includeNeighbors: false,
          fitTargets: 'primary'
        }
      ]
    },
    {
      id: 'crises',
      label: 'Crises',
      layoutTarget: 'matrice',
      intro: 'Les crises rendent visible la gouvernance discrète en régime ordinaire.',
      defaultStepOptions: {
        edgeMode: 'strict',
        includeNeighbors: false,
        secondaryDepth: 0,
        hideBackbone: true,
        fitTargets: 'primary'
      },
      steps: [
        {
          id: 'c1',
          title: 'Deux types de crise',
          body: 'La thèse distingue les crises de vulnérabilité et les crises d’évolution.',
          focusNodes: ["III.2 Des marques d'une politique de crises : une gouvernance de huis clos routinière", 'III.3 Une gouvernance publique d’exception : le hard fork d’Ethereum consécutif à l’attaque de “The DAO”'],
          cameraPreset: 'tight'
        },
        {
          id: 'c2',
          title: 'La CVE 2018',
          body: "Bitcoin CVE 2018-17144 illustre une gestion discrète, routinière, dans un petit cercle d'acteurs.",
          focusNodes: ['Bitcoin CVE 2018-17144', 'Awemany', 'Responsible Disclosure', 'Bitcoin Core (repo)'],
          cameraPreset: 'cluster',
          edgeMode: 'neighbors',
          includeNeighbors: true,
          secondaryDepth: 1,
          maxSecondaryPerTarget: 3,
          fitTargets: 'primary+secondary',
          sourceQuoteId: 'anchor-0b39eeba',   // Gouvernance de huis clos · p. 225
        },
        {
          id: 'c3',
          title: 'The DAO',
          body: 'Avec The DAO, la crise devient publique et controversée : la question n’est plus seulement technique, elle devient politique.',
          focusNodes: ['The DAO', 'Ethereum Hard Fork (juillet 2016)', 'Hack et faillite MtGox (février 2014)', 'Soft Fork', 'Hard Fork'],
          cameraPreset: 'cluster',
          edgeMode: 'neighbors',
          includeNeighbors: true,
          secondaryDepth: 1,
          maxSecondaryPerTarget: 4,
          fitTargets: 'primary+secondary'
        },
        {
          id: 'c4',
          title: 'Scission et thèse',
          body: 'Le hard fork majoritaire n’éteint pas le dissensus : Ethereum Classic naît de la rupture. Les crises révèlent la forme réelle de la gouvernance.',
          focusNodes: ['Ethereum', 'Ethereum Classic (ETHC)', 'Fork (general)', 'Gouvernance polycentrique'],
          cameraPreset: 'wide',
          edgeMode: 'strict',
          includeNeighbors: false,
          fitTargets: 'primary'
        }
      ]
    },
    {
      id: 'structure-these',
      label: 'Structure de la thèse',
      layoutTarget: 'matrice',
      intro: 'Suivre la logique démonstrative et non seulement le sommaire.',
      defaultStepOptions: {
        edgeMode: 'strict',
        includeNeighbors: false,
        secondaryDepth: 0,
        hideBackbone: true,
        fitTargets: 'primary',
        backboneRelationTypes: ['partOf', 'source', 'citedIn', 'relatedTo']
      },
      steps: [
        {
          id: 's1',
          title: 'Le problème initial',
          body: "La thèse part d'un imaginaire libéral-techniciste supposant des cryptomonnaies immunisées contre la gouvernance humaine.",
          focusNodes: ['Syllogisme libéral-techniciste', 'Règle contre discrétion (Rules vs Discretion)', 'Discretion contrainte'],
          cameraPreset: 'tight',
          hideRelationTypes: ['partOf', 'source', 'citedIn', 'relatedTo'],
          sourceQuoteId: 'anchor-4c007966',   // Syllogisme libéral-techniciste · p. 53
        },
        {
          id: 's2',
          title: 'Chapitre I et II',
          body: 'Bitcoin et Ethereum sont des infrastructures sociotechniques hybrides ; la question de la monétisation effective part des usages et de la communauté de paiement.',
          focusNodes: ["Chapitre I - L'émergence du phénomène des cryptomonnaies (CM) : Bitcoin et Ethereum comme infrastructures sociotechniques", 'Infrastructure sociotechnique', 'Chapitre II - Dépasser la controverse du statut monétaire des CM par un institutionnalisme intéressé aux usages', 'Monétisation des cryptomonnaies', "II.2 « Pourtant, elles font monnaie ! » : à l'aune d'un nominalisme « non étatiste » attentif aux usages"],
          cameraPreset: 'cluster',
          hideRelationTypes: ['partOf', 'source', 'citedIn', 'relatedTo']
        },
        {
          id: 's3',
          title: 'Gouvernance et crises',
          body: 'La gouvernance devient un enjeu politique, visible en crise : acteurs, arènes, dissensus et consensus.',
          focusNodes: ['Gouvernance duale', 'Gouvernance polycentrique', 'Chapitre III - Au‑delà des codes : la gouvernance discrète des CM, dévoilée par leurs crises', 'Bitcoin CVE 2018-17144', 'Ethereum Hard Fork (juillet 2016)'],
          cameraPreset: 'cluster',
          edgeMode: 'neighbors',
          includeNeighbors: true,
          secondaryDepth: 1,
          maxSecondaryPerTarget: 4,
          hideBackbone: true,
          fitTargets: 'primary+secondary'
        },
        {
          id: 's4',
          title: 'Conclusion',
          body: 'Les cryptomonnaies ne suppriment pas la politique monétaire : elles déplacent la souveraineté via des infrastructures et des formes polycentriques de gouvernance.',
          focusNodes: ['Conclusion générale', 'Gouvernance polycentrique', 'Règle contre discrétion (Rules vs Discretion)', 'Discretion contrainte'],
          cameraPreset: 'wide',
          hideRelationTypes: ['partOf', 'source', 'citedIn', 'relatedTo'],
          sourceQuoteId: 'anchor-fb610652',   // Gouvernance polycentrique · p. 336
        }
      ]
    },
    {
      id: 'thesis-backbone',
      label: 'Thèse — fil directeur',
      layoutTarget: 'matrice',
      intro: "Parcours argumentatif minimal de la thèse : de la problématisation à la conclusion, sans entrée crise-first.",
      defaultStepOptions: {
        edgeMode: 'strict',
        includeNeighbors: false,
        secondaryDepth: 0,
        hideBackbone: true,
        fitTargets: 'primary'
      },
      steps: [
        {
          id: 'tb1',
          title: 'Point de départ',
          body: "Le phénomène cryptomonnaie est posé comme objet monétaire et politique à expliquer.",
          focusNodes: ['cryptomonnaie', 'Code Source Ouvert'],
          cameraPreset: 'tight',
          sourceQuoteId: 'anchor-7c595e5b'   // intro · p.15
        },
        {
          id: 'tb2',
          title: 'Hypothèse à éprouver',
          body: "La thèse teste le syllogisme libéral-techniciste (code autonome, gouvernance absente).",
          focusNodes: ['Syllogisme libéral-techniciste', 'Code is Law', 'II.3 Au‑delà de la revendication d’une absence de gouvernance !'],
          cameraPreset: 'tight',
          sourceQuoteId: 'anchor-4c007966'   // ch1 · p.53
        },
        {
          id: 'tb3',
          title: 'Chapitre I — infrastructure',
          body: "Bitcoin et Ethereum sont saisis comme infrastructures sociotechniques, pas comme protocoles nus.",
          focusNodes: ['Infrastructure sociotechnique', 'Bitcoin', 'Ethereum'],
          cameraPreset: 'cluster'
        },
        {
          id: 'tb4',
          title: 'Chapitre II — statut et monétisation',
          body: "Le statut monétaire est éclairé par les usages et l'institutionnalisme monétaire.",
          focusNodes: ['Statut monétaire des cryptomonnaies', 'Monétisation des cryptomonnaies', "II.2 « Pourtant, elles font monnaie ! » : à l'aune d'un nominalisme « non étatiste » attentif aux usages"],
          cameraPreset: 'cluster',
          sourceQuoteId: 'anchor-ee9ea714'   // ch2 · p.142
        },
        {
          id: 'tb5',
          title: 'Règle vs discrétion',
          body: "Le débat monétaire classique est réarticulé par les dynamiques effectives de gouvernance des CM.",
          focusNodes: ['Règle contre discrétion (Rules vs Discretion)', 'Discretion contrainte', 'Gouvernance duale'],
          cameraPreset: 'tight',
          sourceQuoteId: 'anchor-c6fadcf4'   // ch2 · p.50
        },
        {
          id: 'tb6',
          title: 'Chapitre III — révélations par les crises',
          body: "Les crises rendent visibles les formes de gouvernance (CVE et DAO comme cas contrastés).",
          focusNodes: ['Bitcoin CVE 2018-17144', 'Attaque de The DAO', 'Crises comme épreuves d’explicitation'],
          cameraPreset: 'cluster',
          edgeMode: 'neighbors',
          includeNeighbors: true,
          secondaryDepth: 1,
          maxSecondaryPerTarget: 3,
          fitTargets: 'primary+secondary',
          sourceQuoteId: 'anchor-5efd9565'   // ch3 · p.223
        },
        {
          id: 'tb7',
          title: 'Conclusion — gouvernance polycentrique',
          body: "La conclusion établit une gouvernance sur l’infrastructure conflictuelle et polycentrique.",
          focusNodes: ['Conclusion générale', 'Gouvernance polycentrique', 'Quote — gouvernance sur l’infrastructure conflictuelle et polycentrique'],
          cameraPreset: 'wide',
          sourceQuoteId: 'anchor-fb610652'   // conclusion · p.336
        }
      ]
    },
    {
      // ── Histoire narrative ancrée sur SourceQuotes ────────────────────
      // Chaque étape est liée à un NarrativeAnchor : la citation est la
      // preuve primaire, l'entité est l'objet analytique, la scène de
      // graphe est la traduction visuelle.
      id: 'fil-de-preuves',
      label: 'Fil de preuves',
      layoutTarget: 'matrice',
      intro: 'Suivre la démonstration de la thèse à travers ses citations clés — chaque étape est ancrée sur une SourceQuote.',
      defaultStepOptions: {
        edgeMode: 'neighbors',
        includeNeighbors: true,
        secondaryDepth: 1,
        maxSecondaryPerTarget: 3,
        hideBackbone: true,
        fitTargets: 'primary+secondary'
      },
      steps: [
        {
          id: 'fp1',
          title: 'La cryptomonnaie comme phénomène',
          body: `« Avec lui commence le phénomène des cryptomonnaies, dont les codes sources sont ouverts. » — La thèse part du fait brut de l'existence des CM comme objets politiques et monétaires.`,
          focusNodes: ['cryptomonnaie', 'Code Source Ouvert', 'Communaute de paiement / Groupe monetaire'],
          cameraPreset: 'cluster',
          sourceQuoteId: 'anchor-7c595e5b',   // cryptomonnaie · intro p. 15
        },
        {
          id: 'fp2',
          title: 'Le syllogisme libéral-techniciste',
          body: `« Les ambitions technicistes des coiners qu'interroge cette thèse peuvent se traduire en un syllogisme. » — L'hypothèse réfutée : le code serait la loi, la gouvernance serait absente.`,
          focusNodes: ['Syllogisme libéral-techniciste', 'Code is Law', 'II.3 Au‑delà de la revendication d’une absence de gouvernance !'],
          cameraPreset: 'tight',
          edgeMode: 'strict',
          includeNeighbors: false,
          sourceQuoteId: 'anchor-4c007966',   // Syllogisme libéral-techniciste · ch1 p. 53
        },
        {
          id: 'fp3',
          title: 'Les crises comme épreuve',
          body: `« Les CM représentent une épreuve d'explicitation de la monnaie. » — Les crises révèlent ce que l'usage ordinaire laisse implicite.`,
          focusNodes: ['Crises comme épreuves d’explicitation', 'Bitcoin', 'Ethereum'],
          cameraPreset: 'cluster',
          sourceQuoteId: 'anchor-c6fadcf4',   // épreuves d'explicitation · ch2 p. 50
        },
        {
          id: 'fp4',
          title: 'Gouvernance de huis clos',
          body: `« Le processus de découverte et de divulgation a permis une résolution silencieuse. » — La CVE 2018 exemplifie la gouvernance discrète : correction sans dissensus public.`,
          focusNodes: ['Gouvernance de huis clos', 'Bitcoin CVE 2018-17144', 'Divulgation responsable', 'Core Developers (Bitcoin)'],
          cameraPreset: 'cluster',
          sourceQuoteId: 'anchor-0b39eeba',   // Gouvernance de huis clos · ch3 p. 225
        },
        {
          id: 'fp5',
          title: 'La divulgation responsable',
          body: `« Il s'engage dans une divulgation responsable : il limite l'accès à cette information. » — Pratique qui codifie la gestion discrète des crises.`,
          focusNodes: ['Divulgation responsable', 'Awemany', 'Bitcoin Core (repo)'],
          cameraPreset: 'tight',
          sourceQuoteId: 'anchor-acb5bee9',   // Divulgation responsable · ch3 p. 234
        },
        {
          id: 'fp6',
          title: 'La gouvernance polycentrique',
          body: `« La gouvernance sur l'infrastructure des CM est conflictuelle et polycentrique. » — Conclusion générale : la thèse réfute l'acéphalisme et nomme la forme réelle de gouvernance.`,
          focusNodes: ['Gouvernance polycentrique', 'Gouvernance duale', 'Infrastructure sociotechnique'],
          cameraPreset: 'wide',
          edgeMode: 'strict',
          includeNeighbors: false,
          fitTargets: 'primary',
          sourceQuoteId: 'anchor-fb610652',   // Gouvernance polycentrique · ccl p. 336
        }
      ]
    }
  ]
};
