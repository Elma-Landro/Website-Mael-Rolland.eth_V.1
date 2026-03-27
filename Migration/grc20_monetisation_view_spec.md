# Vue « Monétisation » — spécification produit / design / données

## Intention
Créer une **nouvelle vue parallèle** à la vue existante **« Structure de la thèse »**.

- **On conserve intacte** la vue actuelle chapitres × types, parce qu’elle fonctionne bien visuellement et narrativement.
- On ajoute une vue **« Monétisation »** qui ne range plus d’abord les entités par chapitre, mais par **rôle dans le processus de monétisation** décrit dans la thèse.
- Cette vue doit améliorer la lecture analytique du graphe sans casser l’esthétique « nébuleuse / archipel » déjà obtenue.

## Principe général
La vue « Monétisation » doit montrer un **dégradé analytique descendant** :

1. **Noyau analytique**
2. **Mécanismes de monétisation**
3. **Arènes / médiations / infrastructures**
4. **Catégories d’acteurs**
5. **Cas empiriques / crises / protocoles / organisations**
6. **Personnes / références / citations**

Autrement dit :
- en haut / au centre : les concepts qui expliquent le phénomène,
- autour : les mécanismes qui rendent la monétisation possible,
- ensuite : les dispositifs, arènes, passerelles, infrastructures,
- ensuite : les groupes et catégories d’acteurs,
- ensuite : les cas empiriques,
- en périphérie : les individus et matériaux secondaires.

## Pourquoi cette vue est pertinente
La structure actuelle par chapitres est belle et utile, mais elle produit plusieurs effets de lecture :
- elle **sur-indexe le chapitre principal** d’apparition d’un concept ;
- elle rend moins lisible la **transversalité** des concepts majeurs ;
- elle fait apparaître parfois trop tôt ou trop directement certains concepts depuis l’introduction ;
- elle ne donne pas immédiatement la logique : **comment Bitcoin / Ethereum deviennent-ils monnaie ?**

La vue « Monétisation » répond précisément à cela.

## Nom affiché
Bouton / entrée de menu :
- **Monétisation**
- sous-titre possible : `Vue thématique · processus de monétisation`

## Philosophie visuelle
Il ne faut **pas** faire une vue trop géométrique ou scolaire.
La vue doit rester :
- organique,
- lumineuse,
- nébuleuse,
- lisible sur mobile,
- cohérente avec la DA actuelle.

### Consigne importante
Ne pas remplacer le caractère « vivant » du graphe par un diagramme rigide.
Il faut une **composition semi-guidée** :
- bandes / strates invisibles,
- sous-amas lumineux,
- respiration entre niveaux,
- petits écarts aléatoires pour éviter l’effet tableau Excel.

## Architecture de la vue

### Strate 1 — Noyau analytique
Contient les concepts les plus structurants de la thèse.

Exemples prioritaires :
- Monétisation
- Infrastructure sociotechnique
- Développement carnavalesque
- Gouvernance polycentrique
- Gouvernance duale
- Mise en crise
- Remise en ordre
- Logique de consensus distribué
- Nominalisme monétaire non étatiste
- Hétérogénéité des monnaies

### Strate 2 — Mécanismes de monétisation
Concepts et objets qui décrivent les conditions de possibilité de la monétisation.

Exemples :
- UCN BTC
- UCN ETH
- Passerelle / Gateway
- Intermédiation
- Infrastructure de paiement
- Infrastructure d’échange
- Usage marchand
- Réserve de valeur
- Unité de compte
- Qualités monétaires désirables
- Hyper-bitcoinisation
- Processus de monétisation progressive de Bitcoin

### Strate 3 — Arènes / médiations / infrastructures
Objets intermédiaires entre théorie et monde empirique.

Exemples :
- InfrastructureDomain
- GovernanceArena
- GovernanceProcess
- Capability
- ProtocolLineage
- ProtocolProposal
- InfrastructureSegment
- PlatformService
- Marketplace
- SoftwareClient
- CodeRepository

### Strate 4 — Catégories analytiques d’acteurs
Ici on place les entités qui servent à penser le monde social crypto en classes analytiques.

Exemples :
- StakeholderCategory | Développeurs
- StakeholderCategory | Développeurs Core
- StakeholderCategory | Mineurs
- StakeholderCategory | Nœuds complets
- StakeholderCategory | Bourses d’échange
- StakeholderCategory | Fournisseurs de portefeuilles
- StakeholderCategory | Marchands
- StakeholderCategory | Investisseurs / spéculateurs
- StakeholderCategory | Utilisateurs
- StakeholderCategory | Régulateurs publics

### Strate 5 — Cas empiriques structurants
Ici on place les cas, organisations, protocoles, crises, collectifs empiriques.

Exemples :
- Bitcoin
- Ethereum
- The DAO
- CVE-2018-17144
- MtGox
- Coinbase
- Kraken
- Ethereum Foundation
- Blockstream
- Core Developers (Bitcoin)
- Core Developers (Ethereum)
- Whitehat Group
- Bitcoin Cash
- Ethereum Classic

### Strate 6 — Personnes / références / matériaux secondaires
Dernière couronne, la plus périphérique.

Exemples :
- personnes,
- références bibliographiques,
- academic works,
- source quotes,
- sources primaires,
- micro-objets secondaires.

## Logique de placement

### A. Placement principal par strate analytique
Chaque entité reçoit :
- `displayViewMonetisation.stratum`
- `displayViewMonetisation.weight`
- `displayViewMonetisation.anchor`
- `displayViewMonetisation.transversal`

### B. Placement secondaire par proximité thématique
À l’intérieur d’une même strate, les entités sont regroupées en **amas thématiques** :
- protocole Bitcoin,
- protocole Ethereum,
- infrastructures d’accès,
- médiations marchandes,
- crises,
- gouvernance,
- théories monétaires,
- catégories d’acteurs.

### C. Gestion des concepts transversaux
Pour éviter qu’un concept apparaisse « trop intro », on ne l’attache pas à un seul chapitre.
On calcule plutôt :
- un `primaryChapter`,
- un `chapterSpreadScore`,
- un `transversalityScore`.

Règle :
- si transversalité élevée, le concept monte d’un cran vers le noyau central ;
- s’il est surtout technique, il descend vers la strate 2 ou 3 ;
- s’il est surtout illustratif / casuel, il descend vers 5.

## Palette / ambiance
Conserver l’esthétique actuelle mais la réinterpréter par famille analytique.

### Proposition
- **Noyau analytique** : ambre / or clair / blanc chaud
- **Mécanismes de monétisation** : orange / cuivre
- **Arènes & infrastructures** : cyan / turquoise
- **Catégories d’acteurs** : vert / vert-jaune
- **Cas empiriques** : violet / magenta / rouge selon la famille
- **Personnes & matériaux secondaires** : rose pâle / gris chaud / bleu désaturé

Important :
- ne pas faire dépendre toute la couleur du chapitre,
- garder les couleurs de chapitre en **accent secondaire** ou en halo léger.

## Formes / glyphes
La vue gagnerait beaucoup à distinguer légèrement les strates sans casser l’esthétique existante.

### Suggestion légère
- Core concepts : losanges ou grands cercles lumineux
- Mécanismes : carrés arrondis / cercles moyens
- Catégories analytiques : hexagones ou cercles à contour
- Cas empiriques : carrés / formes déjà existantes
- Personnes : petits points / petits carrés sobres

Si c’est trop coûteux, garder les formes actuelles mais jouer sur :
- taille,
- halo,
- opacité,
- priorité de label.

## Hiérarchie des labels
Très important pour la lecture.

### Niveau 1 — toujours lisible
- Monétisation
- Bitcoin
- Ethereum
- Gouvernance polycentrique
- Développement carnavalesque
- Infrastructure sociotechnique
- Mise en crise
- Remise en ordre

### Niveau 2 — labels au zoom moyen
- UCN BTC
- UCN ETH
- Passerelles
- Développeurs Core
- Mineurs
- Bourses d’échange
- The DAO
- CVE-2018-17144
- Bitcoin Core
- Ethereum Foundation

### Niveau 3 — labels au focus ou recherche
- personnes,
- références,
- entités secondaires.

## Relation avec la vue existante
La vue « Monétisation » ne doit pas être un remplacement de « Structure de la thèse ».
Elle doit être pensée comme une **vue sœur**.

### Formulation UI suggérée
Dans le bloc de navigation des vues :
- Structure de la thèse
- Monétisation
- Tout le graphe
- Essentiel

## Logique de sélection automatique

### Mapping initial par type
- `Concept` -> strate 1, 2 ou 3 selon score sémantique
- `TheoreticFramework` -> strate 1 ou 2
- `MonetaryObject` -> strate 2
- `Capability` -> strate 2 ou 3
- `InfrastructureDomain` -> strate 3
- `GovernanceArena` -> strate 3
- `GovernanceProcess` -> strate 3
- `StakeholderCategory` -> strate 4
- `ActorGroup` / futur `StakeholderGroup` -> strate 5
- `Protocol` -> strate 5
- `CrisisEvent` -> strate 5
- `Institution` / `Organization` -> strate 5
- `Person` -> strate 6
- `AcademicWork`, `Reference`, `PrimarySource`, `SourceQuote` -> strate 6

### Overrides manuels prioritaires
Forcer manuellement :
- `Monétisation` -> strate 1
- `Bitcoin` -> strate 5 avec centralité forte
- `Ethereum` -> strate 5 avec centralité forte
- `UCN BTC` -> strate 2
- `UCN ETH` -> strate 2
- `Développement carnavalesque` -> strate 1
- `Gouvernance duale` -> strate 1
- `Gouvernance polycentrique` -> strate 1
- `Infrastructure sociotechnique` -> strate 1
- `The DAO` -> strate 5
- `CVE-2018-17144` -> strate 5
- `Passerelle / Gateway` -> strate 2
- `Bourses d’échange` -> strate 4
- `Mineurs` -> strate 4
- `Développeurs Core` -> strate 4

## Comportement des liens
Tous les liens ne doivent pas être également visibles dans cette vue.

### Règle
Mettre visuellement en avant les liens de type :
- `enables`
- `mediates`
- `monetizes`
- `participatesIn`
- `governs`
- `belongsToCategory`
- `crystallizedIn`
- `testedByCrisis`
- `implementedBy`
- `appliedToProtocol`

Et atténuer :
- citations,
- mentions faibles,
- cooccurrences superficielles.

## Micro-récit possible
Cette vue doit raconter implicitement :

> des protocoles et UCN deviennent de la monnaie
> via des médiations, des infrastructures, des catégories d’acteurs et des crises
> selon une gouvernance polycentrique et des processus de monétisation historiquement situés.

## Mobile first
Vu tes captures, il faut penser mobile explicitement.

### Recommandations
- densité abaissée par défaut sur smartphone ;
- labels de niveau 1 seulement au premier affichage ;
- zoom guidé sur 4 ou 5 pôles cliquables ;
- possibilité de toucher :
  - Noyau analytique
  - Acteurs
  - Protocoles
  - Crises
  - Intermédiaires

## MVP implémentable vite
Si l’agent doit faire une première version rapide :
1. ajouter une entrée de vue `monetisation`
2. définir `displayStratum`
3. créer 6 bandes verticales ou horizontales invisibles
4. placer les nœuds par strate + jitter
5. appliquer 20 overrides manuels
6. réduire fortement l’affichage des labels périphériques

## Critère de réussite
La vue est réussie si, en 3 secondes, on comprend visuellement :
- qu’il s’agit d’un graphe sur **la monétisation des cryptomonnaies** ;
- que les concepts centraux sont distincts des cas ;
- que les catégories analytiques servent d’intermédiaires entre théorie et empirique ;
- que Bitcoin et Ethereum sont au cœur des cas étudiés sans écraser le noyau conceptuel.
