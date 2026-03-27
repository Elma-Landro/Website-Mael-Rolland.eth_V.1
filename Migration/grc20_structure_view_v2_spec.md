# GRC-20 — Vue « Structure de la thèse » V2

## Objet
Cette spécification complète la vue actuelle « Structure de la thèse » sans la détruire. Elle conserve :
- la logique narrative par chapitres ;
- l'effet archipel / nébuleuse ;
- les couleurs de chapitre ;
- la sensation visuelle de manuscrit structuré.

Mais elle remplace la lecture trop plate « chapitres × types » par une lecture :

**chapitres × strates ontologico-analytiques**

L'objectif est double :
1. rendre la nouvelle ontologie lisible dans la carte ;
2. éviter que les personnes stratégiques soient rejetées dans une colonne terminale indistincte de « références / sources ».

---

## Problème à corriger
Dans la vue actuelle, plusieurs entités de type `Person` tendent à être lues comme des éléments terminaux, proches de la zone des références. Cette logique fonctionne pour :
- les auteurs cités ;
- les références bibliographiques ;
- les producteurs de cadres théoriques.

Mais elle devient fausse pour des personnes qui sont des **acteurs empiriques structurants** du graphe, par exemple :
- Peter Wuille ;
- Adam Back ;
- W.J. van der Laan ;
- Gregory Maxwell ;
- Jihan Wu ;
- Vitalik Buterin ;
- Gavin Wood ;
- etc.

Ces personnes ne doivent pas apparaître « en bout de chaîne » comme de simples références. Elles doivent rester **au voisinage ontologique** de :
- leur protocole ;
- leur organisation ;
- leur groupe d'acteurs ;
- leur arène de gouvernance ;
- leur cas empirique.

---

## Principe général
Chaque chapitre conserve une bande verticale / nuage coloré propre.
À l'intérieur de cette bande, on introduit **7 strates horizontales ou pseudo-colonnes internes**.

### Strates proposées
1. `core_concepts`
   - Concepts centraux de la thèse
   - Ex. monétisation, gouvernance polycentrique, développement carnavalesque, mise en crise / remise en ordre

2. `analytic_frameworks`
   - Cadres théoriques, concepts secondaires, catégories analytiques
   - Ex. STS, IMF, nominalisme monétaire non étatiste, catégories d'acteurs

3. `protocol_infra_objects`
   - Protocoles, objets monétaires, domaines infrastructurels, capacités, segments, changements protocolaires

4. `collective_structures`
   - Institutions, organisations, groupes d'acteurs, arènes de gouvernance, processus de gouvernance

5. `empirical_cases`
   - Crises, phases de crise, événements infrastructurels, séquences de développement, cas emblématiques

6. `embedded_persons`
   - Personnes empiriques rattachées à des groupes, institutions, protocoles ou cas
   - Ex. Peter Wuille près de Bitcoin Core / Core Devs / Bitcoin

7. `reference_authors`
   - Auteurs, références, citations, sources, travaux académiques, corpus, matériaux de méthode

Important :
- `embedded_persons` et `reference_authors` sont deux usages visuels différents du type `Person`.
- On ne change pas nécessairement le type ontologique `Person` dans le JSON principal ; on ajoute une **classification d'affichage** (`displayRole`, `displayStratum`).

---

## Nouvelle règle clé : bifurcation visuelle des personnes

### 1. Persons empiriques / incarnées
Une personne doit aller dans `embedded_persons` si au moins une des conditions suivantes est satisfaite :
- liée à un `Protocol` par contribution, maintenance, proposition, gouvernance, conflit ;
- liée à un `ActorGroup` ou futur `StakeholderGroup` ;
- liée à une `Institution` ou `Organization` jouant un rôle empirique dans le récit ;
- liée à un `CrisisEvent`, `GovernanceArena`, `ProtocolProposal`, `InfrastructureEvent` ;
- centralité empirique supérieure à sa centralité bibliographique.

Exemples visés :
- Peter Wuille
- Adam Back
- W.J. van der Laan
- Gregory Maxwell
- Jihan Wu
- Vitalik Buterin
- Gavin Wood
- Vlad Zamfir
- Roger Ver
- Andreas Antonopoulos (selon rôle contextuel)

### 2. Persons de référence / théorie
Une personne va dans `reference_authors` si sa fonction principale dans le graphe est :
- auteur cité ;
- cadre théorique ;
- référence secondaire ;
- producteur d'ouvrage ou d'article ;
- personne non engagée comme acteur des cas empiriques.

Exemples visés :
- Susan Leigh Star
- Geoffrey Bowker
- Michel Aglietta
- André Orléan
- Bruno Théret
- Viviana Zelizer

### 3. Persons hybrides
Certaines personnes peuvent être hybrides. Dans ce cas :
- définir `displayRole = hybrid_person` ;
- calculer un `anchorCluster` principal ;
- les placer côté `embedded_persons` si elles sont engagées dans le récit empirique ;
- afficher, au survol, leur double statut.

---

## Colonnes / ordonnancement recommandé
Au lieu d'envoyer mécaniquement toutes les personnes vers la droite, la structure interne recommandée pour chaque bande de chapitre devient :

- gauche : `core_concepts`
- gauche-centre : `analytic_frameworks`
- centre : `protocol_infra_objects`
- centre-droit : `collective_structures`
- droite-centre : `empirical_cases`
- droite : `embedded_persons`
- extrême droite / marge douce : `reference_authors`

Conséquence voulue :
- un chercheur-acteur comme Peter Wuille reste proche de Bitcoin / Bitcoin Core / Core Developers ;
- un auteur comme Star reste dans la zone théorie-références ;
- les personnes ne sont plus toutes traitées de la même manière.

---

## Classification d'affichage recommandée
Ajouter au pipeline de visualisation des champs dérivés :

- `displayStratum`
- `displayRole`
- `anchorCluster`
- `anchorChapter`
- `isTransversal`
- `chapterWeights`
- `sectionWeights`

### Valeurs suggérées pour `displayRole`
- `core_concept`
- `analytic_category`
- `theory_framework`
- `protocol_object`
- `collective_actor`
- `empirical_case`
- `embedded_person`
- `reference_author`
- `hybrid_person`
- `source_material`

---

## Règles de placement des personnes

### Peter Wuille / Greg Maxwell / W.J. van der Laan
- ancrage primaire : Bitcoin / Bitcoin Core / Core Developers
- strate : `embedded_persons`
- proche de `collective_structures` et `protocol_infra_objects`
- jamais rejeté en bout de chaîne bibliographique

### Adam Back
- ancrage primaire : Blockstream / Bitcoin / débats de gouvernance
- strate : `embedded_persons`

### Jihan Wu
- ancrage primaire : Bitmain / mining / gouvernance / conflits de scalabilité
- strate : `embedded_persons`

### Vitalik Buterin / Gavin Wood / Vlad Zamfir
- ancrage primaire : Ethereum / The DAO / gouvernance / protocol proposals
- strate : `embedded_persons`

### Star / Bowker / Orléan / Théret / Aglietta
- ancrage primaire : concepts / cadres théoriques / academic works
- strate : `reference_authors`

---

## Gestion des institutions et groupes
La nouvelle ontologie doit aussi se lire dans la vue.

### `Institution` / `Organization`
Doivent être affichées dans `collective_structures`, pas mélangées aux références.

### `StakeholderCategory`
Doit être affichée dans `analytic_frameworks`.
Exemple :
- Développeurs
- Mineurs
- Fournisseurs de portefeuilles
- Bourses d'échange

### `ActorGroup` ou `StakeholderGroup`
Doit être affiché dans `collective_structures`.
Exemple :
- Core Developers (Bitcoin)
- Core Developers (Ethereum)
- White Hat Group
- Small Blockers
- Pools de minage

La lecture visée est :

**catégorie analytique → collectif empirique → personnes incarnées**

Exemple :
- `StakeholderCategory: Développeurs core`
- `StakeholderGroup: Core Developers (Bitcoin)`
- `Person: Peter Wuille / Greg Maxwell / W.J. van der Laan`

---

## Gestion des concepts transversaux
Ne plus tout aspirer vers l'introduction.

Pour chaque concept majeur :
- conserver un `anchorChapter` principal ;
- stocker aussi `chapterWeights` et `sectionWeights` ;
- dans la vue « Structure de la thèse », afficher un halo ou rappel secondaire dans les autres chapitres pertinents.

Exemples :
- `Monétisation` : intro + chap. I + chap. II + conclusion
- `Gouvernance duale` : intro + chap. II + chap. III + conclusion
- `Mise en crise / Remise en ordre` : surtout chap. III, mais rappel intro + conclusion

---

## Améliorations UI minimales
1. Ajouter un sous-titre de vue :
   `Matrice chapitres × strates analytiques`

2. Ajouter une bascule :
   - `Types bruts`
   - `Strates analytiques`

3. Ajouter dans la légende une mini-explication :
   - Concepts
   - Catégories
   - Objets / protocoles
   - Collectifs
   - Cas
   - Personnes incarnées
   - Références

4. Au survol d'une personne, afficher :
   - rôle visuel (`embedded_person` ou `reference_author`)
   - ancre primaire (`Bitcoin Core`, `Ethereum Foundation`, `cadre STS`, etc.)

---

## Effet recherché
La vue doit permettre de lire immédiatement :
- les grands concepts de la thèse ;
- leurs médiations analytiques ;
- les organisations et collectifs qui les portent ;
- les cas empiriques qui les mettent à l'épreuve ;
- les personnes qui les incarnent effectivement.

La hiérarchie attendue n'est donc pas :
`abstrait → références`

mais :
`concepts → catégories → objets / protocoles → collectifs → cas → personnes incarnées`
avec, à part, une marge de `références / auteurs`.

---

## Compatibilité
Cette V2 doit rester compatible avec :
- la vue actuelle par chapitres ;
- la future vue `Monétisation` ;
- les futures vues thématiques (`Crises`, `Gouvernance`, `Infrastructure`, etc.).
