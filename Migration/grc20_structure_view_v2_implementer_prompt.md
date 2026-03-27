Tu modifies la vue « Structure de la thèse » sans casser son esthétique actuelle.

Objectif : conserver la matrice narrative par chapitres, mais remplacer la logique trop plate « chapitres × types » par une logique « chapitres × strates analytiques ».

Contraintes essentielles :
1. Garder l'effet archipel / nébuleuse et les couleurs par chapitre.
2. Ne pas supprimer la vue actuelle ; créer une V2 ou un mode `analytic strata` dans la vue `structure`.
3. Ne pas envoyer toutes les entités `Person` dans la même zone terminale.
4. Introduire deux usages visuels distincts pour les personnes :
   - `embedded_person` = acteur empirique ancré à un protocole, groupe, institution, crise ou arène.
   - `reference_author` = auteur cité / référence théorique / source.
5. Placer les `embedded_persons` près de leur cluster d'ancrage.
6. Laisser les `reference_authors` dans la marge droite / zone références.
7. Rendre lisible la chaîne :
   catégorie analytique → collectif empirique → personne incarnée.

Strates attendues :
- core_concepts
- analytic_frameworks
- protocol_infra_objects
- collective_structures
- empirical_cases
- embedded_persons
- reference_authors

Règles fortes :
- `StakeholderCategory` doit aller dans `analytic_frameworks`.
- `Institution`, `Organization`, `ActorGroup`, `StakeholderGroup`, `GovernanceArena`, `GovernanceProcess` doivent aller dans `collective_structures`.
- `Protocol`, `MonetaryObject`, `InfrastructureDomain`, `Capability`, `ProtocolChange` doivent aller dans `protocol_infra_objects`.
- `CrisisEvent`, `CrisisPhase`, `InfrastructureEvent`, `DevelopmentPhase` vont dans `empirical_cases`.
- `Concept` et `TheoreticFramework` sont séparés entre `core_concepts` et `analytic_frameworks` selon override.

Cas impératifs :
- Peter Wuille, Greg/Gregory Maxwell, W.J. van der Laan, Adam Back, Jihan Wu, Vitalik Buterin, Gavin Wood, Vlad Zamfir doivent apparaître comme `embedded_persons`.
- Star, Bowker, Orléan, Théret, Aglietta doivent apparaître comme `reference_authors`.

Implémentation recommandée :
- ajouter des champs dérivés : `displayStratum`, `displayRole`, `anchorCluster`, `anchorChapter`, `chapterWeights`, `sectionWeights`, `isTransversal` ;
- prévoir un fichier d'overrides manuel pour les entités stratégiques ;
- conserver une légère dispersion aléatoire locale pour préserver la beauté du nuage ;
- ajouter une bascule UI `Types bruts / Strates analytiques` dans la vue `Structure de la thèse`.

Livrable attendu :
- code modifié de la vue structure ;
- table d'overrides initiale ;
- règles de fallback pour les entités non overridees.
