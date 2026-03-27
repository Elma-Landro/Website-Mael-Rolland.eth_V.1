# Prompt agent — Structure de la thèse V3

Objectif:
Implémenter une V3 de la vue « Structure de la thèse » pour le graphe GRC-20 de Maël Rolland.

Principe général:
- Conserver la beauté visuelle et la lisibilité immédiate de l’ancienne vue.
- Ne PAS remplacer la structure chapitrale existante.
- L’augmenter avec la nouvelle ontologie sans casser les repères historiques.

Contraintes impératives:
1. Restaurer les colonnes historiques visibles et lisibles:
   - Chap.
   - Struct.
   - Objets
   - Acteurs
   - Concepts
   - Evén.
   - Réf.
2. Conserver les couleurs chapitrales fortes.
3. Conserver les halos / brumes colorées par chapitre.
4. Ne jamais reléguer automatiquement toutes les personnes en « Réf. ».
5. Les personnes empiriquement agissantes doivent rester proches des protocoles, groupes, institutions, cas ou crises auxquels elles appartiennent.
6. « Réf. » doit surtout accueillir:
   - auteurs théoriques
   - références bibliographiques
   - corpus
   - citations / sources
7. La nouvelle ontologie doit se lire à l’intérieur des colonnes, pas à la place de la matrice historique.

Logique des colonnes:
- Chap. = ancrage chapitral
- Struct. = sections / sous-sections / charpente narrative
- Objets = protocoles, objets monétaires, clients, repos, dispositifs, services, domaines infrastructurels
- Acteurs = catégories analytiques, institutions, organisations, groupes empiriques, personnes agissantes
- Concepts = concepts centraux, concepts secondaires, concepts techniques, formules natives
- Evén. = crises, phases, événements infrastructurels, moments de gouvernance
- Réf. = auteurs théoriques, academic works, corpus, source quotes, références

Hiérarchie interne demandée:
- Acteurs: StakeholderCategory → Institution/Organization → StakeholderGroup/ActorGroup → Person (agissante)
- Concepts: CoreConcept → SecondaryConcept → TechnicalConcept → NativeFormula
- Objets: MonetaryObject → Protocol → infra logicielle → services / plateformes → domaines
- Evén.: CrisisEvent → CrisisPhase → GovernanceProcess → InfrastructureEvent / ProtocolChange
- Réf.: TheoreticFramework → AcademicWork → Corpus / SourceQuote → Person (référence)

Overrides obligatoires:
- Peter Wuille, Greg Maxwell, W.J. van der Laan, Adam Back, Jihan Wu, Vitalik Buterin, Gavin Wood, Vlad Zamfir -> Acteurs
- Susan Leigh Star, Geoffrey Bowker, André Orléan, Bruno Théret, Michel Aglietta -> Réf.

Critère de réussite:
- Au premier coup d’œil, on reconnaît toujours l’ancienne vue.
- La nouvelle ontologie se lit mieux.
- La beauté chromatique historique est conservée.
