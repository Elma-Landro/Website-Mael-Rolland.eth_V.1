export const STORY_PRESETS = {
  viewToStoryId: {
    monetisation: 'monetisation-cryptos',
    'qui-gouverne': 'qui-gouverne-reellement',
    matrice: 'structure-these'
  },
  stories: [
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
          focusNodes: ['NewLibertyStandard', 'InfrastructureEvent — Première plateforme d’échange BTC (BitcoinMarket.com)', 'Coinbase', 'Kraken', 'Services de paiement'],
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
          focusNodes: ['Gouvernance duale', 'Gouvernance polycentrique', 'Consensus social'],
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
          focusNodes: ['Crise de vulnérabilité', "Crise d'évolution"],
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
          focusNodes: ['The DAO', 'Ethereum Hard Fork (juillet 2016)', 'Attaquant 2016 — An Open Letter (DAO hacker statement)', 'Soft Fork', 'Hard Fork'],
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
        initialState: 'nodesOnly',
        revealMode: 'staged',
        expandOnClick: true,
        maxAutoEdges: 5,
        hideBackbone: true,
        fitTargets: 'primary',
        backboneRelationTypes: ['partOf', 'source', 'citedIn', 'relatedTo']
      },
      steps: [
        {
          id: 's1',
          title: 'Pourquoi cette thèse commence',
          body: 'Bitcoin surgit comme une contestation monétaire radicale. La thèse ne part pas d’un simple objet technique, mais d’un problème : comment des cryptomonnaies prétendant supprimer la gouvernance peuvent-elles malgré tout produire de la monnaie, durer et traverser des crises ? Cette entrée pose déjà le cœur du conflit entre imaginaire techniciste et réalité socio-politique.',
          centralNode: 'Thèse centrale (infrastructures, crises, gouvernance polycentrique)',
          focusNodes: ['Thèse centrale (infrastructures, crises, gouvernance polycentrique)', 'Bitcoin', 'cryptomonnaie', 'A. La gouvernance des cryptomonnaies : construction de notre objet de recherche', 'Syllogisme libéral-techniciste'],
          cameraPreset: 'tight',
          allowedRelationTypes: ['hasConcept', 'mobilizes', 'studiesCase', 'source', 'opposedTo']
        },
        {
          id: 's2',
          title: 'L’objet réel de la recherche',
          body: 'L’objet n’est pas “la blockchain” en général, ni une simple histoire des cryptos. L’objet, c’est la gouvernance des cryptomonnaies, telle qu’elle se révèle quand on quitte les slogans de neutralité pour regarder les controverses, les médiations, les dispositifs et les crises.',
          centralNode: 'A. La gouvernance des cryptomonnaies : construction de notre objet de recherche',
          focusNodes: ['A. La gouvernance des cryptomonnaies : construction de notre objet de recherche', 'Bitcoin', 'Ethereum', 'Sociology of Science & Technology (STS)', 'Institutionnalisme Monetaire Francophone (IMF)'],
          cameraPreset: 'cluster',
          allowedRelationTypes: ['hasConcept', 'mobilizes', 'studiesCase', 'source', 'opposedTo']
        },
        {
          id: 's3',
          title: 'L’introduction fabrique l’outil d’analyse',
          body: 'L’introduction articule deux appuis : un institutionnalisme monétaire attentif aux usages, et une sociologie des sciences et techniques attentive aux infrastructures, aux dispositifs et aux controverses. Elle ajoute une méthode ethnographique multi-niveaux pour suivre à la fois acteurs, artefacts et arènes.',
          centralNode: 'A. La gouvernance des cryptomonnaies : construction de notre objet de recherche',
          focusNodes: ['A. La gouvernance des cryptomonnaies : construction de notre objet de recherche', 'Institutionnalisme Monetaire Francophone (IMF)', 'Sociology of Science & Technology (STS)', 'Ethnographie', "C.2. Stratégie d'accès et matériaux de terrain récoltés"],
          cameraPreset: 'cluster',
          allowedRelationTypes: ['hasConcept', 'mobilizes', 'studiesCase', 'source', 'opposedTo']
        },
        {
          id: 's4',
          title: 'Chapitre I : Bitcoin n’est pas un pur protocole',
          body: 'Le premier chapitre démonte l’idée d’un objet purement technique. Il montre d’abord que Bitcoin est déjà politiquement configuré dans sa conception. Puis il suit la façon dont le monde redéfinit Bitcoin de manière carnavalesque : nouveaux acteurs, nouvelles passerelles, nouvelles médiations, nouveaux usages.',
          centralNode: 'Bitcoin',
          focusNodes: ['Bitcoin', 'Satoshi Nakamoto', 'Développement carnavalesque', 'Services Marchands & Passerelles', "Chaîne d'intermédiation sociotechnique", 'Altcoins'],
          cameraPreset: 'cluster',
          allowedRelationTypes: ['created', 'inspiredBy', 'partOf', 'layerAbove', 'forkOf', 'precursorOf']
        },
        {
          id: 's5',
          title: 'Chapitre I : d’un monde Bitcoin à une bifurcation Ethereum',
          body: 'Le chapitre I ne s’arrête pas à Bitcoin. Il montre aussi qu’Ethereum naît à la fois dans sa continuité et contre ses rigidités : l’écosystème crypto n’est pas un bloc homogène, mais un espace de recompositions socio-techniques.',
          centralNode: 'Ethereum',
          focusNodes: ['Ethereum', 'Bitcoin', 'Altcoins', 'Vitalik Buterin', 'Smart Contracts', 'The DAO'],
          cameraPreset: 'cluster',
          allowedRelationTypes: ['created', 'inspiredBy', 'partOf', 'layerAbove', 'forkOf', 'precursorOf']
        },
        {
          id: 's6',
          title: 'Chapitre II : la vraie charnière de la thèse',
          body: 'Le deuxième chapitre pose la question décisive : ces objets font-ils monnaie ? La thèse répond oui, mais pas au sens orthodoxe. Elle déplace l’analyse vers les usages, la communauté de paiement, la monétisation, les frais, les dettes et les formes de souveraineté impliquées. C’est ici que l’infrastructure devient argument monétaire.',
          centralNode: 'Monétisation des cryptomonnaies',
          focusNodes: ['Monétisation des cryptomonnaies', 'Communaute de paiement / Groupe monetaire', 'UCN BTC', 'UCN ETH', 'Institutionnalisme Monetaire Francophone (IMF)', 'Institutionnalisme intéressé aux usages', 'Gouvernance polycentrique'],
          cameraPreset: 'wide',
          allowedRelationTypes: ['monetaryObject', 'governance', 'hasConcept', 'opposedTo', 'refutedBy', 'relatedTo', 'demonstrates']
        },
        {
          id: 's7',
          title: 'Chapitre II : du statut monétaire à la gouvernance',
          body: 'Le chapitre II ne dit pas seulement que les cryptomonnaies font monnaie. Il montre que leur singularité tient à une gouvernance ni absente ni centralisée, mais polycentrique, débattue et contestée. C’est là que revient, sous une autre forme, le vieux conflit entre règle et discrétion.',
          centralNode: 'Gouvernance polycentrique',
          focusNodes: ['Gouvernance polycentrique', 'Règle comme cristallisation normative située', 'Discretion contrainte', 'Gouvernance duale', 'Règle contre discrétion (Rules vs Discretion)', 'Space of Rule / Space of Discretion'],
          cameraPreset: 'wide',
          allowedRelationTypes: ['monetaryObject', 'governance', 'hasConcept', 'opposedTo', 'refutedBy', 'relatedTo', 'demonstrates']
        },
        {
          id: 's8',
          title: 'Chapitre III : les crises rendent visible l’invisible',
          body: 'Le troisième chapitre fait passer la démonstration à l’épreuve. Avec Bitcoin CVE-2018 et The DAO, la thèse montre que la gouvernance des cryptomonnaies n’est jamais purement codée. Quand le code cesse d’incarner l’esprit communautaire, le consensus social revient au premier plan.',
          centralNode: 'Gouvernance duale',
          focusNodes: ['Gouvernance duale', 'Bitcoin CVE 2018-17144', 'Ethereum Hard Fork (juillet 2016)', 'Gouvernance de huis clos', 'Gouvernance publique et ouverte', 'Bitcoin Core (repo)'],
          cameraPreset: 'cluster',
          allowedRelationTypes: ['hasCrisis', 'demonstrates', 'debatedIn', 'usedIn', 'governance', 'relatedTo']
        },
        {
          id: 's9',
          title: 'Conclusion : ce que la thèse prouve',
          body: 'La conclusion referme la boucle : les cryptomonnaies ne sont ni acéphales ni purement techniques. Elles relèvent d’infrastructures socio-techniques, de processus de monétisation situés et de formes de gouvernance discrètes et polycentriques, révélées avec netteté dans les crises.',
          centralNode: 'Thèse centrale (infrastructures, crises, gouvernance polycentrique)',
          focusNodes: ['Thèse centrale (infrastructures, crises, gouvernance polycentrique)', 'Bitcoin', 'Ethereum', 'Monétisation des cryptomonnaies', 'Gouvernance polycentrique', 'Crises comme épreuves d’explicitation', 'Space of Rule / Space of Discretion'],
          cameraPreset: 'wide',
          allowedRelationTypes: ['hasCrisis', 'demonstrates', 'debatedIn', 'usedIn', 'governance', 'relatedTo']
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
          focusNodes: ["Crises comme épreuves d’explicitation", 'Bitcoin', 'Ethereum'],
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
