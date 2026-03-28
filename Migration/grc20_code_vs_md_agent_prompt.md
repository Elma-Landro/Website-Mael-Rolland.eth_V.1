# Prompt agent implémenteur — correction conjointe données + rendu après audit code/MD

Tu dois partir de deux sources de vérité :
1. la structure textuelle de la thèse affichée dans `graphe.html`
2. l’inventaire `entities_inventory_v90.md`

Objectif :
corriger les écarts entre code, inventaire MD et rendu visuel.

## Ce qui a été audité
Le problème ne relève pas seulement du layout.
Il y a des erreurs de **données**, d’**ancrage chapitral** et de **filtrage sémantique**.

## Règle fondamentale
**Primary textual anchoring overrides relational propagation.**

Autrement dit :
- le chapitre principal d’une entité doit être déterminé d’abord par le lieu principal d’élaboration analytique dans la thèse ;
- les relations ultérieures ne doivent jamais déplacer l’entité dans une autre bande comme ancrage principal.

## Corrections obligatoires

### A. Corriger la structure de la vue `Structure de la thèse`
Colonnes cibles :
- Chap.
- Struct.
- Objets
- Gouvern.
- Crises
- Acteurs
- Concepts
- Réf./Sources

### B. Introduire / corriger les champs d’ancrage
Ajouter ou corriger :
- `primaryChapter`
- `primarySection`
- `secondaryChapters`
- `secondarySections`
- `isReusedLater`

### C. Règles d’ancrage
#### Chapitre I
- émergence Bitcoin/Ethereum comme infrastructures sociotechniques
- I.2 : développement infrastructural au-delà du protocole Bitcoin
- I.3 : émergence et recomposition Ethereum

#### Chapitre II
- controverse monétaire
- usages
- nominalisme non étatiste
- gouvernance polycentrique
- stakeholders / shareholders
- Scaling Debate comme scène de clarification de gouvernance

#### Chapitre III
- CVE-2018-17144
- politique de crises
- gouvernance de huis clos
- DAO
- hard fork / remise en ordre / scission

### D. Cas correctifs obligatoires
#### Réancrer vers Chap.III
- Bitcoin CVE 2018-17144
- GovernanceProcess — CVE-2018-17144 résolution
- CrisisPhase liées à CVE-2018-17144

#### Maintenir / renforcer en Chap.II
- Gouvernance polycentrique
- stakeholders / shareholders
- Bitcoin Scaling Debate
- Bitcoin-dev Mailing List
- GitHub Bitcoin Core
- Bitcointalk Forum

#### Réauditer vers Chap.I
- événements de développement infrastructural Bitcoin
- BitcoinMarket exchange launch
- Bitcoin Foundation creation
- Migration du code Bitcoin vers GitHub
- BIP standardization comme institutionnalisation du processus
- WordPress accepte les paiements en Bitcoin
- eBay / PayPal intègre Bitcoin
- Casascius
- innovations de métaprotocole Bitcoin

#### Réauditer vers Chap.I.3
- Ether Genesis Sale
- Frontier
- lancement d’Ethereum
- levée de fonds Ethereum

### E. Filtrage focus
#### Focus -> Chap. II -> Gouvern.
Inclure surtout :
- GovernanceProcess
- GovernanceConflict
- ProtocolProposal
- GovernanceArena
- StakeholderCategory
- StakeholderGroup
- Organization / Institution
- Person
Exclure par défaut :
- InfrastructureEvent
- InfrastructureDomain
- Capability
- CrisisEvent
- CrisisPhase

#### Focus -> Chap. III -> Gouvern.
Même logique :
- gouvernance stricte visible
- crises détaillées exclues par défaut

#### Focus -> Chap. III -> Crises
Autoriser :
- CrisisEvent
- CrisisPhase
- ProtocolProposal
- sources
- personnes / groupes associés
Mais structurer en sous-clusters :
- cas majeurs
- phases
- CVE techniques
- réponses / forks
- sources

### F. Éclatement
Ne plus utiliser un simple amas circulaire pour les sélections denses.
Prévoir un éclatement structuré local :
- micro-clusters
- packing léger
- sous-zones
- agrégation si trop dense

## Livrables attendus
1. correction des entités mal ancrées
2. correction des champs primary/secondary
3. mise à jour du mapping vue/chapitre/colonne
4. correction du focus
5. amélioration du layout `Éclater`
6. petit rapport des entités corrigées
