# GRC-20 — Vue “Monétisation” (matrice processuelle)

Objectif
Créer une nouvelle vue de la page graphe intitulée :
**Monétisation des cryptomonnaies**
Sous-titre :
**Comment des UCN deviennent monnaie : architecture, circulation, accès, usages, valorisation, stabilisation**

Important
- Ne pas remplacer la vue existante “Structure de la thèse”.
- Ajouter une vue parallèle.
- Priorité absolue à la lisibilité immédiate sur mobile.
- Les titres de colonnes et de lignes doivent être lisibles au premier coup d’œil.
- Conserver l’esthétique du site : halos, palette chaude, contraste fort, rendu nébuleuse maîtrisé.
- Ne pas reléguer toutes les personnes dans une zone “références”.
- Distinguer dans la dernière ligne :
  - figures agissantes
  - auteurs/références théoriques

## 1. Structure de la matrice

### Colonnes (de gauche à droite)
1. Émission
2. Circulation
3. Accès
4. Usages
5. Valorisation
6. Stabilisation

### Lignes (de haut en bas)
1. Thèse
2. Mécanismes
3. Infrastructures
4. Acteurs
5. Cas
6. Figures

## 2. Sens analytique des colonnes

### Émission
Moment où l’UCN existe comme unité native créée par protocole.
Exemples :
- UCN BTC
- UCN ETH
- Monnayage programmatique
- Block reward
- Halving
- Offre des UCN
- PoW / PoS si pertinents à la création/distribution

### Circulation
Capacité à transférer, enregistrer, valider.
Exemples :
- Transaction
- Traitement des transactions
- Validation indépendante
- Full nodes
- Mempool
- Finalité
- Consensus distribué

### Accès
Passerelles entre protocole et monde monétaire élargi.
Exemples :
- Passerelle fiat
- Exchanges
- Wallets custodial / non-custodial
- Payment processors
- ATM
- Stablecoins
- Interopérabilité

### Usages
Monnaie en pratique, communauté de paiement, usages situés.
Exemples :
- Usages réels
- Preuve d’usage économique
- Marchands
- WordPress
- WikiLeaks
- Silk Road
- SatoshiDice
- tipping

### Valorisation
Formation du pouvoir d’achat et intégration marchande.
Exemples :
- Découverte du prix
- Liquidité du marché
- Volume
- Bitcoin comme paire pivot
- Marchés dérivés
- Classe d’actif
- Hyper-bitcoinisation

### Stabilisation
Maintenance, arbitrages, réparation, gouvernance.
Exemples :
- Gouvernance polycentrique
- Gouvernance sur / du protocole
- BIP / EIP
- Hard fork / soft fork
- Divulgation responsable
- CVE-2018-17144
- The DAO
- Mise en crise / Remise en ordre
- GitHub / mailing lists / All Core Dev Meetings

## 3. Sens analytique des lignes

### Thèse
Très peu de nœuds.
Réservé aux concepts directeurs.
Exemples :
- Monétisation
- Infrastructure sociotechnique
- Développement carnavalesque
- Gouvernance polycentrique
- Mise en crise
- Remise en ordre
- Nominalisme monétaire non étatiste

### Mécanismes
Mécanismes monétaires et techniques intermédiaires.
Exemples :
- Effet réseau
- Bootstrapping
- Logique de consensus distribué
- Preuve d’usage économique
- Découverte du prix
- Validation
- Rareté programmée

### Infrastructures
Dispositifs, médiations, arènes et services.
Exemples :
- Wallet infrastructure
- Exchange infrastructure
- Services de paiement
- GitHub Bitcoin Core
- Bitcoin-dev mailing list
- Infrastructure financière auxiliaire
- Conformité / traceabilité

### Acteurs
Catégories analytiques + organisations + groupes empiriques.
Exemples :
- Développeurs core
- Mineurs
- Exchanges
- Marchands
- Bitcoin Core
- Ethereum Foundation
- White Hats
- Big Blockers / Small Blockers

### Cas
Protocoles, événements, objets empiriques saillants.
Exemples :
- Bitcoin
- Ethereum
- The DAO
- CVE-2018-17144
- SegWit
- Silk Road
- WikiLeaks
- Omni / USDT

### Figures
Deux sous-zones visuelles obligatoires :
A. figures agissantes
B. auteurs / références

#### Figures agissantes
À garder proches de la colonne de leur action principale.
Exemples :
- Peter Wuille
- Greg Maxwell
- Adam Back
- W.J. van der Laan
- Jihan Wu
- Vitalik Buterin
- Gavin Wood
- Vlad Zamfir

#### Auteurs / références
Plus périphériques, opacité légèrement réduite.
Exemples :
- Susan Leigh Star
- Geoffrey Bowker
- André Orléan
- Bruno Théret
- Michel Aglietta

## 4. Règles de placement

1. Chaque entité reçoit :
- monetizationColumn
- monetizationRow
- monetizationSecondaryColumn (optionnel)
- monetizationWeight (0-1)
- monetizationRole (optionnel: active_figure, theoretical_reference, empirical_case, infrastructure_gateway, etc.)

2. Une entité transversale peut déborder légèrement sur une colonne voisine, mais doit garder une colonne principale.

3. Les concepts les plus centraux doivent être peu nombreux et bien espacés.
Ne pas faire un bandeau surchargé dans “Thèse”.

4. Les colonnes doivent être lisibles sans zoom.
Afficher les libellés horizontalement ou quasi-horizontalement.
Éviter les diagonales trop longues.

5. Les halos doivent aider la lecture du processus.
Recommandation chromatique par colonne :
- Émission : ambre
- Circulation : or clair
- Accès : cyan
- Usages : vert
- Valorisation : violet
- Stabilisation : rouge-orangé

6. La ligne “Figures” ne doit pas devenir une nappe blanche illisible.
Créer deux sous-bandes :
- Figures agissantes
- Références
Avec densité et opacité différenciées.

## 5. Exemples de placements obligatoires

- Monétisation -> colonne Stabilisation? Non. Ligne Thèse, colonne médiane entre Accès/Usages/Valorisation, avec centre principal sur Usages-Valorisation.
- Infrastructure sociotechnique -> Thèse x Circulation/Accès
- Développement carnavalesque -> Thèse x Accès/Usages
- UCN BTC -> Cas x Émission
- UCN ETH -> Cas x Émission
- Block reward -> Mécanismes x Émission
- Halving -> Cas ou Mécanismes x Émission
- Passerelle fiat -> Infrastructures x Accès
- Services de portefeuille et paiement -> Infrastructures x Accès
- Usages réels de Bitcoin -> Cas x Usages
- Liquidité du marché -> Mécanismes x Valorisation
- Découverte du prix -> Mécanismes x Valorisation
- Gouvernance polycentrique -> Thèse x Stabilisation
- BIP -> Infrastructures x Stabilisation
- EIP -> Infrastructures x Stabilisation
- CVE-2018-17144 -> Cas x Stabilisation
- The DAO -> Cas x Stabilisation
- Peter Wuille -> Figures agissantes x Stabilisation/Circulation
- Adam Back -> Figures agissantes x Émission/Stabilisation
- Vitalik Buterin -> Figures agissantes x Stabilisation
- Susan Leigh Star -> Références x Circulation/Accès (périphérie)
- André Orléan -> Références x Usages/Valorisation (périphérie)

## 6. Ce qu’il faut éviter absolument
- Une simple pile verticale de types.
- Une dernière ligne “Personnes/références” uniforme.
- Des libellés de colonnes illisibles.
- Une surcharge dans la ligne “Thèse”.
- Une vue qui confond types ontologiques et étapes de monétisation.
