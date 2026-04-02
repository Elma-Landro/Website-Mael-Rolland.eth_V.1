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
      intro: 'Du statut monétaire controversé à la gouvernance : une démonstration progressive du chapitre II.',
      defaultStepOptions: {
        edgeMode: 'strict',
        includeNeighbors: false,
        secondaryDepth: 0,
        initialState: 'nodesOnly',
        revealMode: 'staged',
        expandOnClick: true,
        maxAutoEdges: 3,
        maxPrimaryEdges: 6,
        maxSecondaryEdges: 4,
        hideBackbone: true,
        fitTargets: 'primary',
        allowedRelationTypes: ['hasConcept', 'monetaryObject', 'governance', 'relatedTo', 'demonstrates', 'opposedTo', 'refutedBy', 'source']
      },
      steps: [
        {
          id: 'm1',
          title: 'Pourquoi le statut monétaire est controversé',
          body: 'Les cryptomonnaies sont d’abord saisies comme des objets monétaires problématiques. Beaucoup de critiques les rejettent hors de la monnaie, soit parce qu’elles rempliraient mal les fonctions monétaires classiques, soit parce qu’elles n’auraient pas d’ancrage institutionnel légitime.',
          centralNode: 'Statut monétaire des cryptomonnaies',
          focusNodes: ['cryptomonnaie', 'Statut monétaire des cryptomonnaies', 'Fonctions monétaires', 'Critiques instrumentales', 'Critiques chartalistes'],
          cameraPreset: 'tight'
        },
        {
          id: 'm2',
          title: 'L’épreuve d’explicitation de la monnaie',
          body: 'La thèse ne traite pas les cryptomonnaies comme un simple échec monétaire. Elle les prend comme une épreuve d’explicitation : elles obligent à rendre visibles les présupposés des théories dominantes de la monnaie.',
          centralNode: 'Épreuve d’explicitation de la monnaie',
          focusNodes: ['Épreuve d’explicitation de la monnaie', 'cryptomonnaie', 'Monnaie', 'Nominalisme non étatiste', 'Monetary Institutionalism FR (IMF)'],
          cameraPreset: 'tight'
        },
        {
          id: 'm3',
          title: 'Pourtant, elles font monnaie',
          body: 'Le point de bascule du chapitre II est là : malgré les critiques, les cryptomonnaies font monnaie dans certains usages. L’enjeu n’est donc plus de leur dénier abstraitement tout caractère monétaire, mais de comprendre comment se fabrique leur monétisation.',
          centralNode: 'Monétisation',
          focusNodes: ['Usages monétaires', 'Monétisation', 'UCN BTC', 'UCN ETH', 'Usage en compte', 'Usage en paiement'],
          cameraPreset: 'cluster'
        },
        {
          id: 'm4',
          title: 'La monétisation n’est pas donnée, elle se construit',
          body: 'La monétisation n’est ni automatique ni purement protocolaire. Elle dépend d’un travail de mise en forme, d’équipement, de convertibilité, de liquidité et de reconnaissance par des acteurs dispersés.',
          centralNode: 'Monétisation',
          focusNodes: ['Monétisation', 'Liquidité', 'Convertibilité', 'Passerelles', 'Infrastructures de marché', 'Intermédiation'],
          cameraPreset: 'cluster'
        },
        {
          id: 'm5',
          title: 'La communauté de paiement comme pivot',
          body: 'La monnaie n’existe pas seulement comme objet technique ou comme actif coté. Elle existe parce qu’une communauté de paiement se forme, accepte des unités, les compte, les échange et les reconnaît dans des usages situés.',
          centralNode: 'Communauté de paiement',
          focusNodes: ['Communauté de paiement', 'Usages monétaires', 'UCN BTC', 'UCN ETH', 'Paiement', 'Dette', 'Confiance'],
          cameraPreset: 'cluster'
        },
        {
          id: 'm6',
          title: 'Institutions, usages et souveraineté',
          body: 'La monétisation renvoie alors à des institutions, à des attentes collectives et à des formes de souveraineté. Ce déplacement permet de sortir du faux choix entre pure autonomie technique et pure garantie étatique.',
          centralNode: 'Institutions',
          focusNodes: ['Institutions', 'Souveraineté monétaire', 'Confiance', 'Monetary Institutionalism FR (IMF)', 'Nominalisme non étatiste', 'Gouvernance polycentrique'],
          cameraPreset: 'wide'
        },
        {
          id: 'm7',
          title: 'Ce que ce récit doit prouver',
          body: 'Le récit doit se conclure clairement : les cryptomonnaies ne sont ni de simples actifs sans monde social, ni de parfaites monnaies déjà données. Elles relèvent de processus de monétisation situés, socialement équipés et politiquement encadrés.',
          centralNode: 'Monétisation',
          focusNodes: ['Monétisation', 'Communauté de paiement', 'Gouvernance polycentrique', 'cryptomonnaie', 'Monnaie', 'Thèse centrale (infrastructures, crises, gouvernance polycentrique)'],
          cameraPreset: 'wide'
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
