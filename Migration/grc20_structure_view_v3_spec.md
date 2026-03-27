# GRC-20 — Structure de la thèse V3 (correction après retour utilisateur)

## Diagnostic du problème
La version précédente a dégradé deux qualités essentielles de la vue historique :
1. elle a supprimé les deux premières colonnes `Chap.` et `Struct.` / `Sections`, qui servaient d'ancrage immédiat ;
2. elle a affaibli la logique chromatique et la lisibilité "au premier coup d'oeil".

La nouvelle règle est simple :
**on ne remplace pas la vue historique ; on l'augmente.**

## Objectif
Conserver l'esthétique et l'intelligibilité immédiate de l'ancienne matrice, tout en intégrant la nouvelle ontologie.

## Principe général
La vue `Structure de la thèse` doit rester une matrice lisible en 1 seconde, avec les colonnes suivantes, dans cet ordre :
1. `Chap.`
2. `Struct.`
3. `Objets`
4. `Acteurs`
5. `Concepts`
6. `Evén.`
7. `Réf.`

Aucune de ces colonnes ne doit être supprimée.

## Règle essentielle
La nouvelle ontologie doit être **encodée à l'intérieur** des colonnes existantes, pas au prix d'une refonte qui casse la lecture historique.

---

## 1. Structure visuelle générale

### Colonnes conservées
- `Chap.` = chapitres / parties du manuscrit
- `Struct.` = sections, sous-sections, architecture argumentative
- `Objets` = protocoles, objets monétaires, dispositifs, infrastructures, repositories, software, smart contracts
- `Acteurs` = institutions, organisations, groupes, catégories d'acteurs, personnes empiriquement incarnées
- `Concepts` = core concepts, concepts secondaires, concepts techniques, formules natives
- `Evén.` = crises, phases, conflits, propositions, moments charnières
- `Réf.` = auteurs, academic works, corpus, citations, références théoriques ou documentaires

### Lignes conservées
- `Intro.`
- `Chap. I`
- `Chap. II`
- `Chap. III`
- `Concl.`
- `Multi.`

### Couleurs
Conserver strictement la logique colorée déjà appréciée :
- Intro = bleu clair / cyan
- Chap. I = orange / ambre
- Chap. II = vert
- Chap. III = violet
- Conclusion = rose / magenta
- Multi = halo atténué / gris coloré

### Glow / halos
Ne pas supprimer les halos chapitraux. Ils constituent une partie essentielle de l'esthétique et de la lisibilité.

---

## 2. Où intégrer la nouvelle ontologie

## Colonne `Acteurs`
La colonne `Acteurs` devient hiérarchisée **sans être éclatée**.

Ordre vertical interne à la colonne :
1. `StakeholderCategory` / catégories analytiques d'acteurs
2. `Institution` / `Organization`
3. `StakeholderGroup` / `ActorGroup`
4. `Person` empiriquement incarnées

### Règles de placement
- Les personnes ne vont dans `Réf.` que si elles sont **avant tout** des auteurs de référence.
- Les personnes fortement engagées dans l'empirie restent dans `Acteurs`.
- Une personne est dite "incarnée" si elle a des liens forts avec un protocole, un groupe, une institution, une crise ou une proposition technique.

### Exemples
Restent dans `Acteurs` :
- Peter Wuille
- Greg Maxwell
- Adam Back
- W.J. van der Laan
- Jihan Wu
- Vitalik Buterin
- Gavin Wood
- Vlad Zamfir

Basculent ou restent dans `Réf.` :
- Susan Leigh Star
- Geoffrey Bowker
- André Orléan
- Michel Aglietta
- Bruno Théret

## Colonne `Concepts`
La colonne `Concepts` conserve son identité visuelle mais devient stratifiée en interne :
1. `CoreConcept`
2. `SecondaryConcept`
3. `TechnicalConcept`
4. `NativeFormula`

Les `CoreConcept` doivent apparaître légèrement plus hauts et plus centraux dans la colonne.

## Colonne `Objets`
Regrouper ici :
- `Protocol`
- `MonetaryObject`
- `SoftwareClient`
- `CodeRepository`
- `SmartContract`
- `PlatformService`
- `InfrastructureService`
- `HardwareDevice`
- `Marketplace`
- `MediaOutlet` (si sa fonction est avant tout infrastructurelle dans la démonstration)

## Colonne `Evén.`
Regrouper ici :
- `CrisisEvent`
- `CrisisPhase`
- `GovernanceConflict`
- `ProtocolProposal`
- `GovernanceProcess`
- `InfrastructureEvent`

## Colonne `Réf.`
Réserver cette colonne à :
- `AcademicWork`
- `Reference`
- `Corpus`
- `SourceQuote`
- `PrimarySource`
- `Method`
- `Person` seulement si rôle principal = auteur / référence

---

## 3. Rétablissement de la clarté immédiate

### Titres de colonnes
Les titres doivent être grands, visibles et stables :
`Chap.`, `Struct.`, `Objets`, `Acteurs`, `Concepts`, `Evén.`, `Réf.`

### Orientation des labels
Tolérance pour une légère diagonale, mais pas au point de nuire à la lecture.
Préférence : angle faible ou horizontal.

### Densité
Ne pas chercher à faire voir toute la hiérarchie en un seul coup par des labels multipliés.
La hiérarchie doit se lire par :
- placement,
- densité,
- taille,
- opacité,
- voisinage.

---

## 4. Améliorations discrètes à ajouter

### 4.1 Micro-strates internes
Ajouter des sous-bandes discrètes dans les colonnes `Acteurs` et `Concepts`.
Ces sous-bandes peuvent être visibles seulement par un fin liseré, une légère variation de luminosité ou au hover.

### 4.2 Légendes secondaires au hover
Quand on survole la colonne `Acteurs`, on peut afficher :
`Catégories → institutions/orgs → groupes → personnes`

Quand on survole `Concepts` :
`Noyau → secondaires → techniques → formules`

### 4.3 Concepts transversaux
Les concepts transversaux ne doivent pas être aspirés visuellement par l'Intro.
Créer une ligne `Multi.` clairement visible en bas avec rappel lumineux, pour les entités véritablement transversales.

---

## 5. Vue Monétisation : correction
La vue `Monétisation` doit rester distincte, mais elle doit devenir lisible immédiatement.

### Colonnes obligatoires
1. `Noyau`
2. `Mécanismes`
3. `Médiations`
4. `Acteurs`
5. `Cas`
6. `Réf.`

### Labels lisibles
Titres grands, contrastés, lisibles sans zoom.
Aucun sigle ou label implicite.

### Palette
Conserver l'identité graphique générale du site, mais utiliser des couleurs stables par colonne.

### Règle de lecture
Au premier regard, on doit comprendre :
- en haut : concepts centraux de la monétisation
- au milieu : mécanismes et médiations
- ensuite : acteurs
- ensuite : cas empiriques
- enfin : références

---

## 6. Overrides prioritaires

### Colonne `Acteurs`
Forcer le placement dans `Acteurs` pour :
- Peter Wuille
- Greg Maxwell
- Gregory Maxwell
- Adam Back
- W.J. van der Laan
- Jihan Wu
- Vitalik Buterin
- Gavin Wood
- Vlad Zamfir
- Roger Ver
- Andreas Antonopoulos (si traité comme acteur médiateur empirique)

### Colonne `Réf.`
Forcer le placement dans `Réf.` pour :
- Susan Leigh Star
- Geoffrey Bowker
- Thomas Hughes
- André Orléan
- Michel Aglietta
- Bruno Théret
- Viviana Zelizer
- Keith Hart

### Colonne `Concepts`
Forcer en haut de colonne :
- Monétisation
- Infrastructure sociotechnique
- Gouvernance polycentrique
- Gouvernance duale
- Développement carnavalesque
- Mise en crise
- Remise en ordre
- Nominalisme monétaire non étatiste

---

## 7. Résumé opératoire
- Restaurer les colonnes `Chap.` et `Struct.`.
- Restaurer la logique colorée historique.
- Ne pas remplacer la vue historique par une ontologie abstraite.
- Encapsuler la nouvelle ontologie dans les colonnes existantes.
- Laisser les personnes empiriques dans `Acteurs` quand elles incarnent des groupes, institutions, propositions ou conflits.
- Réserver `Réf.` aux auteurs / sources / corpus / citations.
- Refaire la vue `Monétisation` avec de vrais titres de colonnes lisibles.
