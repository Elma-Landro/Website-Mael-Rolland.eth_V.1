# Prompt agent implémenteur — correction du focus `Gouvern.` / distinction `Crises`

Tu dois corriger le comportement actuel du mode `Focus` dans le graphe, en particulier pour les vues :
- `Structure de la thèse`
- `Qui gouverne réellement ?`

## Diagnostic du problème actuel
Quand l’utilisateur sélectionne par exemple :
- `Chap. III`
- `Gouvern.`
- mode `Éclater`

la sélection remonte actuellement trop d’éléments hétérogènes :
- infrastructures
- infrastructure events
- protocol changes
- longues séries de CVE
- événements techniques fins
- objets du chapitre I

Résultat :
la vue devient illisible et ne correspond pas à l’intention analytique.

Le problème n’est donc pas seulement visuel.
C’est un problème de **mapping sémantique** :
la colonne `Gouvern.` agrège aujourd’hui des objets qui devraient être distingués.

## Objectif de la correction
Quand l’utilisateur choisit `Gouvern.`, il doit voir **la gouvernance en tant que telle** :
- processus de gouvernance
- conflits de gouvernance
- propositions / procédures de gouvernance
- concepts gouvernants
- arènes gouvernantes si explicitement liées au pilotage et à la décision

Mais il ne doit pas récupérer automatiquement :
- tous les `InfrastructureEvent`
- tous les `ProtocolChange`
- toutes les CVE détaillées
- tous les objets techniques relevant plutôt de l’infrastructure ou des crises

## Changement conceptuel demandé
Tu dois distinguer au minimum **deux familles séparées** :

### 1. `Gouvern.`
Pour tout ce qui relève de la gouvernance au sens strict :
- GovernanceProcess
- GovernanceConflict
- ProtocolProposal
- GovernanceArena (quand l’arène est vraiment gouvernante)
- concepts directement gouvernants :
  - gouvernance polycentrique
  - gouvernance duale
  - gouvernance par le protocole
  - gouvernance sur le protocole
  - politique de crises
  - mise en crise
  - remise en ordre
- sections de thèse explicitement dédiées à la gouvernance

### 2. `Crises`
Nouvelle catégorie / nouvelle colonne / ou nouveau sous-filtre obligatoire
pour éviter que la gouvernance soit noyée par les détails événementiels.

`Crises` doit accueillir :
- CrisisEvent
- CrisisPhase
- CVE
- DAO
- forks de crise
- épisodes de révélation / divulgation / remédiation
- crises de scalabilité si elles sont traitées comme crises
- objets “encyclopédiques” de crise

L’idée est :
- `Gouvern.` = gouvernement, arbitrage, coordination, conflictualité, décision
- `Crises` = cas révélateurs, épisodes, séquences, événements de crise

## Consigne majeure
**Ne plus faire remonter automatiquement tous les objets de crise dans `Gouvern.`.**

Les crises peuvent être liées à la gouvernance, mais elles ne doivent pas être absorbées par elle dans le focus.

## Ce que doit donner le focus

### Cas 1
Si utilisateur choisit :
- `Chap. III`
- `Gouvern.`

la sélection doit privilégier :
- GovernanceProcess
- GovernanceConflict
- ProtocolProposal
- GovernanceArena
- concepts gouvernants
- sections gouvernance du chapitre III
- personnes / groupes directement impliqués dans la décision

et **exclure par défaut** :
- CrisisEvent détaillés
- CrisisPhase détaillées
- longues séries de CVE
- InfrastructureEvent
- InfrastructureDomain
- Capability
- ProtocolChange purement technique
- événements du chapitre I hors rattachement direct

### Cas 2
Si utilisateur choisit :
- `Chap. III`
- `Crises`

la sélection doit alors faire remonter :
- The DAO
- CVE-2018-17144
- Scaling Debate si classé comme crise
- phases de crise
- forks de crise
- divulgation / révélation / remédiation
- citations et sources de crise
- acteurs de crise associés

### Cas 3
Si utilisateur veut une lecture croisée
prévoir éventuellement un preset :
- `Gouvernance par les crises`
qui mélange les deux volontairement, mais seulement comme preset distinct.

## Recommandation de structure

### Pour `Structure de la thèse`
Au lieu de garder seulement :
- Chap.
- Struct.
- Objets
- Gouvern.
- Acteurs
- Concepts
- Réf./Sources

ajouter une distinction plus propre :
- Chap.
- Struct.
- Objets
- Gouvern.
- Crises
- Acteurs
- Concepts
- Réf./Sources

Si l’ajout d’une colonne casse trop la mise en page,
alors faire au minimum :
- un sous-filtre interne à `Gouvern.` :
  - `Gouvernance stricte`
  - `Crises`

Mais la meilleure option reste une vraie séparation visuelle.

### Pour `Qui gouverne réellement ?`
Même logique :
si une colonne terminale `Cas / Réf.` existe, il faut distinguer en interne :
- `Cas de crise`
- `Réf.`

et surtout ne pas mélanger cela avec `Gouvern.`.

## Mapping sémantique recommandé

### Va dans `Gouvern.`
- GovernanceProcess
- GovernanceConflict
- ProtocolProposal
- GovernanceArena
- Concept directement gouvernant
- sections gouvernance
- groupes décisionnels
- personnes agissantes de gouvernement

### Va dans `Crises`
- CrisisEvent
- CrisisPhase
- CVE-*
- The DAO
- forks de crise
- divulgation responsable
- épisodes de remédiation
- labels/qualifications de crise

### Ne va ni dans `Gouvern.` ni dans `Crises` par défaut
- InfrastructureEvent ordinaires
- InfrastructureDomain
- Capability
- objets purement techniques
- événements historiques de développement sans dimension de crise ni de gouvernance directe

## Règles de filtrage à implémenter

### Règle 1 — filtrage strict par colonne
Quand une colonne est sélectionnée, ne pas ramener automatiquement toutes les entités liées par proximité sémantique.
Filtrer d’abord par :
- colonne assignée
- vue active
- bande / chapitre
- ligne éventuelle

### Règle 2 — propagation limitée
Autoriser un léger voisinage contextuel, mais très limité.
Exemple :
si `Gouvern.` est sélectionné,
on peut garder un peu de contexte :
- groupes
- personnes
- arènes
mais pas toutes les crises détaillées ni les objets techniques.

### Règle 3 — seuil anti-invasion CVE
Si plus de X CVE ou phases de crise remontent dans une vue non-`Crises`,
les masquer automatiquement derrière une agrégation légère :
- `Crises techniques (12)` au lieu de 12 lignes de CVE

### Règle 4 — agrégation encyclopédique de crise
Créer un comportement d’agrégation :
- une entité mère ou pseudo-cluster `Crises techniques`
- une entité mère `Crises de gouvernance`
- ou regroupement par cas principal

L’utilisateur peut ensuite éclater ce cluster s’il veut le détail.

## Presets à ajouter

### Structure de la thèse
- `Gouvernance du Chap. III`
- `Crises du Chap. III`
- `Gouvernance par les crises`
- `Acteurs du Chap. I`

### Qui gouverne réellement ?
- `Décision sans crises`
- `Crises révélatrices`
- `Personnes de la maintenance`
- `Arènes de décision`

## Contraintes visuelles
- sur mobile, éviter la liste interminable de labels CVE
- privilégier des clusters ou agrégats quand la densité est trop forte
- conserver lisibilité des labels
- conserver code couleur :
  - chapitre = famille chromatique
  - colonne = nuance / modulation

Si `Crises` devient une colonne propre, lui donner une nuance distincte mais cohérente :
- rouge / rose / corail
sans absorber la palette des chapitres

## Deliverables attendus
1. correction du mapping de `Gouvern.`
2. création d’une séparation nette `Gouvern.` / `Crises`
3. correction du focus pour éviter l’invasion des infrastructure events et CVE
4. logique d’agrégation légère pour les crises trop nombreuses
5. presets distincts
6. maintien de la lisibilité mobile

## Critère de réussite
Quand l’utilisateur clique :
`Focus -> Chap. III -> Gouvern. -> Éclater`

il doit voir principalement :
- gouvernance polycentrique
- gouvernance duale
- politique de crises
- BIP/EIP si pertinents
- arènes de gouvernance
- groupes et personnes de décision
- sections structurantes de gouvernance

et non pas une avalanche de :
- CVE détaillées
- infrastructure events
- objets du chapitre I
- listes techniques illisibles
