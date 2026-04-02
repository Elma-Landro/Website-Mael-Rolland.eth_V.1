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
      intro: 'Un récit concret des acteurs, arènes, dispositifs et asymétries qui structurent les chaînes réelles de décision.',
      defaultStepOptions: {
        edgeMode: 'strict',
        includeNeighbors: false,
        secondaryDepth: 0,
        initialState: 'nodesOnly',
        revealMode: 'staged',
        expandOnClick: true,
        maxAutoEdges: 4,
        maxPrimaryEdges: 7,
        maxSecondaryEdges: 6,
        allowedRelationTypes: [
          'governance',
          'has governance process',
          'used in',
          'debated in',
          'demonstrates',
          'opposed to',
          'refuted by'
        ],
        hideBackbone: true,
        fitTargets: 'primary'
      },
      steps: [
        {
          id: 'q1',
          title: 'Le mythe de l’absence de gouvernance',
          body: 'Le récit doit commencer par la thèse adverse : beaucoup de discours coiners présentent les cryptomonnaies comme gouvernées par le code seul. Le récit doit immédiatement montrer que cette affirmation est un point de départ polémique, pas un constat descriptif.',
          centralNode: 'Absence de gouvernance',
          focusNodes: ['Absence de gouvernance', 'Code is Law', 'cryptomonnaie', 'Bitcoin', 'Ethereum'],
          cameraPreset: 'tight',
          maxPrimaryEdges: 5
        },
        {
          id: 'q2',
          title: 'Gouverner par l’infrastructure / sur l’infrastructure',
          body: 'La première distinction à rendre visible est celle entre gouvernance par l’infrastructure et gouvernance sur l’infrastructure. Le code contraint, mais il est lui-même administré, discuté, modifié, relu et contesté.',
          centralNode: 'Gouvernance duale',
          focusNodes: ['Gouvernance par l’infrastructure', 'Gouvernance sur l’infrastructure', 'Gouvernance duale', 'Code source', 'Protocole', 'Infrastructure'],
          cameraPreset: 'cluster',
          maxPrimaryEdges: 6
        },
        {
          id: 'q3',
          title: 'Les acteurs centraux de la maintenance',
          body: 'La gouvernance réelle passe par des acteurs souvent discrets : core developers, maintainers, opérateurs de nœuds et intermédiaires de maintenance. Ce sont eux qui filtrent les propositions, arbitrent les priorités et rendent certaines trajectoires techniques plus probables que d’autres.',
          centralNode: 'Développeurs Core (mainteneurs avec accès commit)',
          focusNodes: ['Développeurs Core (mainteneurs avec accès commit)', 'Core Developers (Ethereum)', 'Bitcoin Core (repo)', 'Pull Request (PR)', 'Opérateurs de nœuds', 'Mineurs Bitcoin'],
          cameraPreset: 'cluster',
          maxPrimaryEdges: 7
        },
        {
          id: 'q4',
          title: 'Les arènes où se décident les arbitrages',
          body: 'Les décisions ne sortent pas d’un point unique. Elles se fabriquent dans des arènes hétérogènes : dépôts de code, mailing lists, forums, réunions de coordination et dispositifs de consultation. Le récit doit montrer le passage entre ces arènes.',
          centralNode: 'GitHub Bitcoin Core',
          focusNodes: ['GitHub Bitcoin Core', 'Bitcoin-dev Mailing List', 'Bitcointalk Forum', 'All Core Dev Meetings (Ethereum)', 'BIP (Bitcoin Improvement Proposal)', 'EIP (Ethereum Improvement Proposal)', 'Carbon Vote (DAO Fork, juin-juillet 2016)'],
          cameraPreset: 'cluster',
          maxPrimaryEdges: 7
        },
        {
          id: 'q5',
          title: 'Dispositifs et asymétries effectives de pouvoir',
          body: 'La gouvernance réelle n’est pas une égalité abstraite entre pairs. Les droits d’écriture, la capacité de review, la maîtrise des canaux de coordination et la possibilité d’imposer un tempo produisent des asymétries effectives de pouvoir.',
          centralNode: 'Gouvernance de maintenance (huis clos routinier)',
          focusNodes: ['Gouvernance de maintenance (huis clos routinier)', 'Gouvernance publique et ouverte', 'Pull Request (PR)', 'BIP (Bitcoin Improvement Proposal)', 'EIP (Ethereum Improvement Proposal)', 'Consensus social'],
          cameraPreset: 'tight',
          maxPrimaryEdges: 6
        },
        {
          id: 'q6',
          title: 'Ce que ce récit doit démontrer',
          body: 'La question pertinente n’est pas “décentralisé ou centralisé”, mais : qui peut proposer, qui peut bloquer, qui peut décider et dans quelles arènes ? Le récit doit conclure que la gouvernance des cryptomonnaies est située, processuelle, conflictuelle et polycentrique.',
          centralNode: 'Gouvernance polycentrique',
          focusNodes: ['Visibilisation de la gouvernance', 'Gouvernance duale', 'Gouvernance polycentrique', 'Consensus social', 'Bitcoin', 'Ethereum'],
          cameraPreset: 'wide',
          maxPrimaryEdges: 7
        }
      ]
    },
    {
      id: 'crises',
      label: 'Crises',
      layoutTarget: 'matrice',
      intro: 'Un récit comparatif et processuel : mise en crise, qualification, dispositifs, remise en ordre et forme de gouvernance révélée.',
      defaultStepOptions: {
        edgeMode: 'strict',
        includeNeighbors: false,
        secondaryDepth: 0,
        initialState: 'nodesOnly',
        revealMode: 'staged',
        expandOnClick: true,
        maxAutoEdges: 4,
        maxPrimaryEdges: 8,
        maxSecondaryEdges: 6,
        allowedRelationTypes: [
          'has crisis',
          'demonstrates',
          'debated in',
          'used in',
          'governance',
          'has governance process',
          'opposed to',
          'refuted by'
        ],
        hideBackbone: true,
        fitTargets: 'primary'
      },
      steps: [
        {
          id: 'c1',
          title: 'Pourquoi passer par les crises',
          body: 'Les crises ne sont pas un supplément spectaculaire à la thèse. Elles sont le moment où l’infrastructure, la gouvernance et les hiérarchies deviennent visibles. Le récit doit faire comprendre d’emblée que les crises sont une méthode d’accès à la structure réelle des cryptomonnaies.',
          centralNode: 'Crises',
          focusNodes: [
            'Crises',
            'Mise en crise',
            'Remise en ordre',
            'Gouvernance des cryptomonnaies',
            'Thèse centrale (infrastructures, crises, gouvernance polycentrique)'
          ],
          cameraPreset: 'tight'
        },
        {
          id: 'c2',
          title: 'Deux types de crises',
          body: 'Le récit doit expliciter la distinction entre crises de vulnérabilité et crises d’évolution. Cette typologie est décisive pour comprendre pourquoi toutes les défaillances, controverses ou conflits ne produisent pas la même forme de gouvernance.',
          centralNode: 'Gouvernance duale',
          focusNodes: ['Crise de vulnérabilité', "Crise d’évolution", 'Gouvernance duale', 'Bitcoin', 'Ethereum'],
          cameraPreset: 'cluster',
          maxPrimaryEdges: 6
        },
        {
          id: 'c3',
          title: 'Bitcoin CVE 2018 : une crise de vulnérabilité',
          body: 'La crise Bitcoin CVE-2018 doit être montrée comme un cas de gouvernance de huis clos, marquée par la responsible disclosure, l’évaluation discrète, la correction silencieuse et la formation d’un consensus local. Il faut faire sentir qu’il ne s’agit pas d’une absence de gouvernance, mais d’une gouvernance routinière, resserrée et discrète.',
          centralNode: 'Bitcoin CVE 2018-17144',
          focusNodes: [
            'Bitcoin CVE 2018-17144',
            'Gouvernance de huis clos',
            'Responsible disclosure',
            'Bitcoin Core (repo)',
            'Consensus local',
            'Patch'
          ],
          cameraPreset: 'cluster',
          maxPrimaryEdges: 7
        },
        {
          id: 'c4',
          title: 'The DAO : une crise publique et conflictuelle',
          body: 'The DAO doit apparaître comme l’autre grand modèle : crise publique, controverse ouverte, stratégies concurrentes, débat sur les moyens légitimes de remise en ordre, puis hard fork et sécession. Il faut rendre visible le passage du désaccord technique au dissensus politique.',
          centralNode: 'The DAO',
          focusNodes: ['The DAO', 'Ethereum DAO Hard Fork', 'Gouvernance publique', 'Hard Fork', 'Ethereum Classic', 'Consensus global'],
          cameraPreset: 'cluster',
          maxPrimaryEdges: 7
        },
        {
          id: 'c5',
          title: 'Ce que les crises révèlent',
          body: 'Les crises rendent visibles les écarts entre la lettre du code et l’esprit communautaire. Elles montrent que le consensus technique ne suffit pas toujours et que la décision revient aussi à des médiations sociales et politiques. Cette étape doit être clairement interprétative, pas seulement descriptive.',
          centralNode: 'Space of Rule / Space of Discretion',
          focusNodes: [
            'Code is Law',
            'Esprit communautaire',
            'Space of Rule / Space of Discretion',
            'Consensus social',
            'Gouvernance duale'
          ],
          cameraPreset: 'tight',
          maxPrimaryEdges: 6
        },
        {
          id: 'c6',
          title: 'Comparer CVE 2018 et The DAO',
          body: 'Le récit doit contenir une vraie étape comparative, pas deux cas simplement juxtaposés. Elle doit faire ressortir : type de crise, degré de publicité, temporalité, acteurs centraux, dispositifs de décision, forme de consensus, type de sortie, et forme de gouvernance rendue visible.',
          centralNode: 'Gouvernance duale',
          focusNodes: [
            'Bitcoin CVE 2018-17144',
            'Ethereum DAO Hard Fork',
            'Gouvernance de huis clos',
            'Gouvernance publique',
            'Consensus local',
            'Consensus global'
          ],
          cameraPreset: 'wide',
          maxPrimaryEdges: 8
        },
        {
          id: 'c7',
          title: 'Ce que ce récit doit prouver',
          body: 'Le récit doit finir sur une thèse forte : les crises ne sont pas des anomalies extérieures aux cryptomonnaies ; elles révèlent la structure ordinaire de leur reproduction, la présence de médiations décisives et la nature conflictuelle, discrète et polycentrique de leur gouvernance.',
          centralNode: 'Thèse centrale (infrastructures, crises, gouvernance polycentrique)',
          focusNodes: [
            'Crises',
            'Gouvernance duale',
            'Gouvernance polycentrique',
            'Bitcoin',
            'Ethereum',
            'Thèse centrale (infrastructures, crises, gouvernance polycentrique)'
          ],
          cameraPreset: 'wide',
          maxPrimaryEdges: 8
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
      id: 'fil-de-preuves',
      label: 'Fil de preuves',
      layoutTarget: 'matrice',
      intro: 'Un récit démonstratif : plusieurs lignes de preuve distinctes qui convergent vers la thèse centrale.',
      defaultStepOptions: {
        edgeMode: 'strict',
        includeNeighbors: false,
        secondaryDepth: 0,
        initialState: 'nodesOnly',
        revealMode: 'staged',
        expandOnClick: true,
        maxAutoEdges: 4,
        maxPrimaryEdges: 7,
        maxSecondaryEdges: 6,
        allowedRelationTypes: ['hasConcept', 'demonstrates', 'source', 'relatedTo', 'refutedBy', 'opposedTo', 'governance', 'hasCrisis'],
        hideBackbone: true,
        fitTargets: 'primary'
      },
      steps: [
        {
          id: 'fp1',
          title: 'Le problème initial à éprouver',
          body: 'La thèse part d’un syllogisme libéral-techniciste : si la technique est neutre et si les cryptomonnaies sont purement techniques, alors elles seraient sans gouvernance humaine et meilleures que les monnaies nationales. Le fil de preuves doit montrer comment ce syllogisme est déconstruit pas à pas.',
          centralNode: 'Syllogisme libéral-techniciste',
          focusNodes: ['Syllogisme libéral-techniciste', 'Bitcoin', 'cryptomonnaie', 'Thèse centrale (infrastructures, crises, gouvernance polycentrique)'],
          cameraPreset: 'tight',
          maxPrimaryEdges: 5
        },
        {
          id: 'fp2',
          title: 'Première ligne de preuve : la conception n’est pas neutre',
          body: 'Les choix architecturaux, les inspirations idéelles et les compromis techniques montrent déjà que les protocoles ne naissent pas hors du monde social. La preuve commence donc avant même les usages ou les crises.',
          centralNode: 'Satoshi Nakamoto',
          focusNodes: ['Satoshi Nakamoto', 'Bitcoin', 'Conception politique', 'Choix architecturaux', 'STS'],
          cameraPreset: 'cluster',
          maxPrimaryEdges: 6
        },
        {
          id: 'fp3',
          title: 'Deuxième ligne de preuve : l’infrastructure déborde le protocole',
          body: 'Le développement infrastructurel, les passerelles, les intermédiaires, les usages et les recompositions d’acteurs montrent qu’un protocole nu ne fait pas monnaie à lui seul. Cette ligne de preuve déplace l’analyse du design vers le monde socio-technique effectivement constitué.',
          centralNode: 'Développement infrastructurel carnavalesque',
          focusNodes: ['Développement infrastructurel carnavalesque', 'Passerelles', 'Intermédiation', 'Usages', 'Bitcoin', 'Ethereum'],
          cameraPreset: 'cluster',
          maxPrimaryEdges: 7
        },
        {
          id: 'fp4',
          title: 'Troisième ligne de preuve : la monétisation se construit',
          body: 'La monnaie n’apparaît pas ici comme une essence, mais comme un processus de monétisation soutenu par des usages, une communauté de paiement, des équipements et des institutions. Cette étape doit montrer comment l’infrastructure devient argument monétaire.',
          centralNode: 'Monétisation',
          focusNodes: ['Monétisation', 'Communauté de paiement', 'Usages monétaires', 'UCN BTC', 'UCN ETH', 'Monetary Institutionalism FR (IMF)'],
          cameraPreset: 'cluster',
          maxPrimaryEdges: 7
        },
        {
          id: 'fp5',
          title: 'Quatrième ligne de preuve : les crises révèlent la gouvernance',
          body: 'Les crises montrent que le code ne clôt jamais entièrement la décision. Quand les tensions deviennent manifestes, les formes de gouvernance, les arènes, les hiérarchies et les dispositifs de consensus apparaissent à découvert. Cette étape doit condenser la force probatoire de CVE 2018 et de The DAO.',
          centralNode: 'Gouvernance duale',
          focusNodes: ['Bitcoin CVE 2018-17144', 'Ethereum DAO Hard Fork', 'Gouvernance duale', 'Space of Rule / Space of Discretion', 'Consensus social'],
          cameraPreset: 'cluster',
          maxPrimaryEdges: 7
        },
        {
          id: 'fp6',
          title: 'Ce que l’ensemble prouve',
          body: 'Le fil de preuves doit finir sur une conclusion pleinement démonstrative : les cryptomonnaies sont des infrastructures socio-techniques dont la monétisation et la reproduction passent par des formes de gouvernance discrètes, conflictuelles et polycentriques. Il faut que cette dernière étape fasse sentir la convergence des preuves, pas une simple récapitulation.',
          centralNode: 'Thèse centrale (infrastructures, crises, gouvernance polycentrique)',
          focusNodes: ['Thèse centrale (infrastructures, crises, gouvernance polycentrique)', 'Monétisation', 'Gouvernance polycentrique', 'Crises', 'Bitcoin', 'Ethereum'],
          cameraPreset: 'wide',
          maxPrimaryEdges: 7
        }
      ]
    }
  ]
};
