
# Patch de refonte ontologique — GRC20 thesis graph v90 → v91

## Objet

Ce document prépare un patch pour l’agent implémenteur chargé de corriger la couche entités du graphe v90.  
Il ne s’agit **pas** d’un nettoyage cosmétique, mais d’une **refonte contrôlée de l’ontologie appliquée**, visant à rendre le graphe plus lisible, plus fidèle à la thèse, et plus stable pour les relations futures.

## 1. Diagnostic de départ

L’inventaire v90 contient **2 303 entités** et **19 901 relations**. L’export montre une prolifération des catégories et un aplatissement ontologique : 428 `Concept`, 151 `Person`, 60 `ActorGroup`, 47 `ActorNonHuman`, 38 `Capability`, 30 `StakeholderCategory`, 16 `InfrastructureDomain`, ainsi que des types récemment introduits (`NarrativeCluster`, `GovernanceArena`, `GovernanceProcess`, `CrisisPhase`, etc.).  
L’inventaire montre notamment :
- des doublons nominaux (`Mastercoin / Omni` et `Mastercoin / Omni Layer`) ;
- des erreurs de typage (`Bitmain` en `Person`, `Banque de France` en `ActorGroup`) ;
- une confusion entre collectifs empiriques et catégories analytiques (`Core Developers (Bitcoin)` vs `Développeurs Core`) ;
- un type `ActorNonHuman` devenu un conteneur trop hétérogène (logiciels, pools, places de marché, médias, plateformes, objets monétaires, smart contracts) ;
- des concepts de rang théorique très différents mis au même niveau (`Monnetisation`, `Monnaie parallèle`, `Nonce`, `OP_RETURN`, slogans, titres, notes d’analyse).  
Ces problèmes sont documentés directement dans l’inventaire. Par exemple, `Bitmain` et `CEX.io` figurent dans `Person`, tandis que `Banque de France`, `CNRS`, `EHESS`, `Ethereum Foundation`, `Coinbase`, `Kraken`, `Ledger`, `MtGox`, `Slock.it` ou `Tether Limited` sont tous rangés ensemble dans `ActorGroup`.  
Le graphe initial JSON, lui, était beaucoup plus resserré, avec seulement 12 types : `AcademicWork`, `Person`, `Institution`, `Concept`, `TheoreticFramework`, `CrisisEvent`, `Protocol`, `ActorNonHuman`, `MethodDevice`, `MonetaryObject`, `Reference`, `ActorGroup`.

## 2. Principe directeur de la refonte

Le graphe doit être réorganisé autour d’un centre analytique clair :

**MONÉTISATION DES CRYPTOMONNAIES**

Autour de ce centre doivent s’ordonner :
1. les protocoles ;
2. les objets monétaires ;
3. les domaines et segments infrastructurels ;
4. les médiations d’accès, de conversion et d’usage ;
5. les catégories d’acteurs ;
6. les collectifs empiriques ;
7. les organisations et institutions ;
8. les crises, controverses et arènes de gouvernance ;
9. les concepts analytiques de haut niveau.

Le patch proposé cherche donc à faire passer le graphe :
- d’un **inventaire foisonnant**,
- à une **ontologie hiérarchisée**,
- fidèle à la logique de la thèse : développement infrastructurel, monétisation, gouvernance duale, crises comme épreuves d’explicitation.

## 3. Décisions ontologiques proposées

### 3.1 Types à conserver sans changement de principe
- `Person`
- `Protocol`
- `MonetaryObject`
- `CrisisEvent`
- `TheoreticFramework`
- `Reference`

### 3.2 Types à rétablir ou à réaffirmer
- `Institution` : entités académiques, banques centrales, organismes publics, organisations internationales, laboratoires, fondations de recherche.
- `ActorGroup` : collectifs empiriques identifiables, factions, coalitions, communautés, groupes de développeurs, groupes de détenteurs, mouvements.
- `MethodDevice` : remplacer `Method` par le type canonique du JSON initial.

### 3.3 Types à introduire ou officialiser
- `Organization` : entreprises, plateformes, fondations opératrices, associations, bourses, prestataires, fabricants, médias, ONG opérationnelles.
- `StakeholderCategory` : catégories analytiques transversales (mineurs, développeurs, nœuds complets, marchands, régulateurs, médias, fournisseurs de portefeuilles, etc.).
- `SoftwareClient`
- `CodeRepository`
- `SmartContract`
- `PlatformService`
- `MediaOutlet`
- `Marketplace`
- `HardwareDevice`
- `InfrastructureService`
- `ConceptCore`
- `ConceptSecondary`
- `ConceptTechnical`
- `NativeFormula`
- `ChapterSection` (uniquement si l’on souhaite conserver certains titres comme objets documentaires ; sinon suppression)
- `GovernanceArena`
- `GovernanceProcess`
- `GovernanceConflict`
- `CrisisPhase`
- `InfrastructureDomain`
- `InfrastructureSegment`
- `InfrastructureEvent`
- `ProtocolChange`
- `ProtocolProposal`
- `DevelopmentPhase`
- `Argument`
- `NarrativeCluster`

### 3.4 Types à éviter comme fourre-tout
- `ActorNonHuman` ne doit plus accueillir indifféremment logiciel, pool, wallet, média, smart contract, site, place de marché, protocole ou service.  
Deux options :
1. **Option stricte** : éclater complètement `ActorNonHuman` dans les types spécialisés ci-dessus.
2. **Option transitoire** : conserver `ActorNonHuman` comme super-classe abstraite, sans nouvelles créations directes.

## 4. Relations nouvelles recommandées

Le schéma relationnel actuel ne suffit pas pour distinguer catégories, instances, alias et sous-types. Il faut ajouter :

- `aliasOf`
- `canonicalNameOf` ou stockage `aliases[]` au niveau entité
- `instanceOfCategory`
- `belongsToCategory`
- `operatesOnProtocol`
- `implementsProtocol`
- `repositoryFor`
- `clientFor`
- `serviceFor`
- `governs`
- `participatesInArena`
- `phaseOfCrisis`
- `phaseOfDevelopment`
- `instantiatedInProtocol`
- `partOfMonetizationProcess`
- `mediatesAccessTo`
- `enablesCapability`
- `sloganOf`
- `derivedFromConcept`

## 5. Règles générales de transformation

### R1 — Canonicalisation des noms
Chaque entité doit porter :
- `canonicalName`
- `aliases[]`
- `normalizedLabel`

On fusionne les variantes orthographiques, pseudonymiques ou contextuelles dans une seule entité canonique.

### R2 — Une seule entité par référent
Une organisation ou personne ne doit pas exister sous plusieurs formes si la variation ne change pas le référent.

### R3 — Distinction stricte entre :
- **acteur collectif empirique** (`ActorGroup`)
- **catégorie analytique** (`StakeholderCategory`)
- **organisation nommée** (`Organization`)
- **institution** (`Institution`)

### R4 — Les types documentaires et analytiques ne doivent pas être confondus
Un titre de partie, une note d’analyse ou un label de sous-section n’est pas un `Concept`.

### R5 — Les concepts doivent être hiérarchisés
Un concept théorique central ne doit pas être au même niveau qu’un terme technique élémentaire.

### R6 — Les domaines infrastructurels doivent être canoniques
On crée des domaines génériques, puis on les relie aux protocoles au lieu de dupliquer le domaine par protocole.

### R7 — Les crises doivent être modélisées de manière homogène
Même granularité, même structure, même articulation entre `CrisisEvent`, `CrisisPhase`, `GovernanceArena`, `GovernanceProcess`, `GovernanceConflict`.

## 6. Patch opérationnel — Fusions prioritaires

## 6.1 Person — fusions
| Canonique | Alias / doublons à fusionner | Action |
|---|---|---|
| Alex Mizrahi | Alex Mizrahi (ChromaWay) | fusion + alias |
| Greg Maxwell | Gregory Maxwell | fusion + alias |
| J.R. Willett | J.R. Willet | fusion + alias |
| Jeffrey Wilcke | Jeff Wilcke (Go Ethereum) | fusion + alias |
| Erik Voorhees | Eric Voorhees | fusion + alias |
| Shaolin Fry | Shaoling Fry | fusion + alias |
| Theymos | Theymos (administrateur BitcoinTalk) | fusion + alias |
| Luke Dashjr | Luke-Jr (Luke Dashjr) | fusion + alias |
| Sunny King | King Sunny / Scott Nadal ; Sunny King (pseudonyme) | fusion + alias |
| Leigh Star | Susan Leigh Star / Leigh Star si ultérieurement présent | préparer règle d’alias |

## 6.2 Protocol — fusions
| Canonique | Alias / doublons | Action |
|---|---|---|
| Omni Layer | Mastercoin / Omni ; Mastercoin / Omni Layer | fusion + alias historique |
| Ethereum Classic | Ethereum Classic (ETHC) ; ETHC si présent ailleurs | fusion + alias |
| Tether / USDT | attention à distinguer protocole/objet/service | voir retypage plus bas |

## 6.3 TheoreticFramework — fusions
| Canonique | Alias / doublons | Action |
|---|---|---|
| IAD Framework | IAD (Institutional Analysis and Development) Framework | fusion |
| STS | Sociology of Science & Technology (STS) ; si future variante française | fusion par alias |

## 6.4 Concept — fusions certaines
| Canonique | Doublons / variantes à fusionner |
|---|---|
| Discrétion contrainte | Discretion contrainte ; Discrétion contrainte (Constrained Discretion) |
| Disponibilité | Disponibilite (propriete DLT) |
| Double dépense | Double depense ; Double dépense (double spend) ; Problème de double dépense |
| Gouvernance duale | Gouvernance duale (CM) |
| Infrastructure sociotechnique | Infrastructure sociotechnique (CM) |
| OP_RETURN | OP_RETURN (opcode Bitcoin) |
| Politique de crise | Politique de crises |
| Objet-frontière | Objet-frontière (boundary object) ; Objets-frontieres (Boundary Objects) |
| Passerelle | Passerelle (gateway / on-off ramp) ; Passerelle / Gateway |
| Empreinte numérique / hash | Empreinte numerique / Hash ; Empreinte numérique |
| Limite de taille des blocs Bitcoin (1 Mo) | Limitation de taille des blocs (1 Mo, Bitcoin) ; Limite de taille des blocs Bitcoin (1 Mo) |
| Résistance à la censure | Resistance a la censure ; Résistance à la censure (censorship resistance) |
| Règle contre discrétion | Regle contre discretion (monetary policy) ; Règle contre discrétion (Rules vs Discretion) ; Règle contre la discrétion (politique monétaire) |
| Common Pool Resources | Common Pool Resource (CPR) ; Common Pool Resources ; Common Pool Resources (CPR) |
| Cadre IAD / SES | Cadre IAD / SES (Ostrom) ; Cadre IAD/SES |

## 6.5 CrisisEvent — fusions
| Canonique | Doublons / variantes | Action |
|---|---|---|
| Ethereum Hard Fork (juillet 2016) | Ethereum DAO Hard Fork | fusion |
| Scaling Debate (2015–2017) | Bitcoin Scaling Debate ; Scaling Debate | conserver un `GovernanceConflict` canonique + lier au `GovernanceProcess` et, si nécessaire, à un `CrisisEvent` distinct |

## 7. Patch opérationnel — Erreurs de typage manifestes

## 7.1 `Person` → autre type
| Entité actuelle | Type actuel | Type cible | Justification |
|---|---|---|---|
| Bitmain | Person | Organization | entreprise |
| CEX.io | Person | Organization | plateforme d’échange |
| De Boyer des Roches et Rosales | Person | Reference ou 2 Person | binôme d’auteurs, pas personne unique |
| Desmedt et Lakomski-Laguerre | Person | Reference ou 2 Person | binôme d’auteurs |
| NewLibertyStandard | Person | PlatformService ou pseudonyme à vérifier | probablement service/site plutôt que personne |

## 7.2 `ActorGroup` → `Institution`
| Entité actuelle | Type cible |
|---|---|
| Banque centrale européenne (BCE) | Institution |
| European Central Bank | Institution |
| Banque d'Angleterre | Institution |
| Banque de France | Institution |
| Banque mondiale | Institution |
| Banque des règlements internationaux (BRI) | Institution |
| Fonds Monetaire International (FMI) | Institution |
| EHESS | Institution |
| CEMS | Institution |
| CEMI | Institution |
| CNRS | Institution |
| Mines Paris / Centre de Sociologie de l'Innovation | Institution |
| Paris 1 Pantheon-Sorbonne | Institution |
| Paris School of Economics | Institution |
| Sciences Po Lyon | Institution |
| Université de Münster | Institution |
| École de Bloomington | TheoreticFramework ou Institution selon usage dominant |

## 7.3 `ActorGroup` → `Organization`
| Entité actuelle | Type cible |
|---|---|
| BTC-e | Organization |
| BitPay | Organization |
| Bitcoin Foundation | Organization |
| Bitfinex | Organization |
| Bitmain (Jihan Wu) | Organization |
| Bitsquare / Bisq | Organization ou PlatformService |
| Bitstamp | Organization |
| Blockstream | Organization |
| Butterfly Labs | Organization |
| Chaincode Labs | Organization |
| Coinbase | Organization |
| Dell | Organization |
| EthCore (entreprise de Gavin Wood) | Organization |
| Ethereum Foundation | Organization |
| Kraken | Organization |
| Ledger | Organization |
| MtGox | Organization |
| Overstock.com | Organization |
| Robinhood (plateforme de trading) | Organization |
| Slock.it | Organization |
| Tether Limited | Organization |

## 7.4 `ActorGroup` à conserver comme `ActorGroup`
| Entité | Motif |
|---|---|
| Core Developers (Bitcoin) | collectif empirique |
| Core Developers (Ethereum) | collectif empirique |
| Cypherpunk Movement | mouvement / collectif |
| Crypto-Anarchist Movement | mouvement / collectif |
| Mineurs Bitcoin | collectif empirique |
| Pools de minage | collectif empirique |
| Partisans Ethereum Classic | faction |
| Small Blockers / Bitcoin Core | coalition/faction |
| Whitehat Group (DAO crisis) | coalition circonstancielle |
| Robin Hood Group (DAO 2016) | coalition circonstancielle |
| Détenteurs de jetons DAO | collectif empirique |
| Utilisateurs (full nodes) | groupe empirique si conservé |
| Utilisateurs nœuds légers (SPV) | groupe empirique si conservé |

## 7.5 `ActorGroup` → `StakeholderCategory`
| Entité actuelle | Type cible |
|---|---|
| Bourses d'échange (exchanges) | StakeholderCategory |
| Fournisseurs de portefeuilles (wallet providers) | StakeholderCategory |
| Opérateurs de nœuds complets (full nodes) | StakeholderCategory |
| Processeurs de paiement (payment processors) | StakeholderCategory |
| Régulateurs nationaux et internationaux | StakeholderCategory |
| Médias crypto et grand public | StakeholderCategory |

## 8. Patch opérationnel — refonte de `ActorNonHuman`

## 8.1 `ActorNonHuman` → `CodeRepository`
- Bitcoin Core (repo)

## 8.2 `ActorNonHuman` → `SoftwareClient`
- Bitcoin-QT / Bitcoin Core (client)
- Bitcoin-Qt / Bitcoin Core Wallet
- Bitcoin ABC
- Bitcoin Knots
- Bitcoin Unlimited
- BTCD
- Bcoin
- Besu (Hyperledger Besu)
- Erigon
- Go-Ethereum (Geth)
- Mist
- Nethermind
- OpenEthereum / Parity
- Pyethereum
- cpp-ethereum (Aleth)
- Electrum wallet
- Wasabi Wallet (CoinJoin)
- Samourai Wallet (Whirlpool)
- BTCPay Server

## 8.3 `ActorNonHuman` → `PlatformService`
- Blockchain.info
- Coinbase Commerce
- Paymium
- ShapeShift
- MyBitcoin
- Bitcoin Fog
- BitLaundry
- Gavin Andresen Faucet
- Helix (by Grams)

## 8.4 `ActorNonHuman` → `Marketplace`
- Silk Road
- SatoshiDice

## 8.5 `ActorNonHuman` → `MediaOutlet`
- Bitcoin Magazine
- WikiLeaks (si modélisé comme média/organisation éditoriale dans ce contexte)
- WordPress (plus probablement `PlatformService` si usage comme site/service)

## 8.6 `ActorNonHuman` → `HardwareDevice`
- Trezor
- Casascius Physical Bitcoins (ou `MonetaryArtifact` si type créé)

## 8.7 `ActorNonHuman` → `SmartContract`
- The DAO

## 8.8 `ActorNonHuman` → `InfrastructureService` / `MiningPool`
- AntPool
- BTC Guild
- F2Pool
- GHash.io
- Slush Pool

## 8.9 `ActorNonHuman` → autres corrections
- Mastercoin : ne doit pas coexister comme `ActorNonHuman` si référent principal = protocole.
- Omni Layer (meta-protocole Bitcoin) : doit rejoindre le protocole canonique `Omni Layer`.
- Ethereum Virtual Machine (EVM) : plutôt `ConceptTechnical` ou `SoftwareRuntime`, selon granularité retenue.
- Preuve de Travail (PoW) : ne doit pas être `ActorNonHuman`, mais `ConceptTechnical` ou `Capability`, selon logique choisie.
- chaîne de blocs : `ConceptTechnical`, pas `ActorNonHuman`.

## 9. Patch opérationnel — Concepts à reclasser

## 9.1 `Concept` → `NativeFormula`
- "Not your keys, not your coins"
- Être sa propre banque (be your own bank)
- Code is law (si présent plus loin)

## 9.2 `Concept` → `ConceptCore`
- Monétisation / Monnetisation
- Monnaie parallèle
- Monnaie communautaire
- Gouvernance duale
- Gouvernance polycentrique
- Infrastructure sociotechnique
- Développement carnavalesque
- Mise en crise / Remise en ordre
- Esprit du code vs Lettre du code
- Nominalisme monétaire non étatiste
- Crises comme épreuves d’explicitation
- Gouvernance discrète des cryptomonnaies
- Gouvernance par le protocole
- Gouvernance sur le protocole
- Gouvernance par l’infrastructure
- Gouvernance sur l’infrastructure
- Logique de consensus distribué

## 9.3 `Concept` → `ConceptSecondary`
- Hyper-bitcoinisation / Hyper-cryptomonétisation si ajoutée
- Interopérabilité de Bitcoin
- Délégation et recentralisation
- Ossification du protocole Bitcoin
- Institutionnalisation carnavalesque de l'infrastructure Bitcoin
- Régime transactionnel
- Forces centripètes et centrifuges
- Décentrement infrastructurel de Bitcoin
- Bitcoin comme paire pivot des marchés crypto
- Dollarisation de Bitcoin (stablecoin pivot)

## 9.4 `Concept` → `ConceptTechnical`
- UTXO
- Account-based model
- Nonce
- OP_RETURN
- SHA-256
- PoW
- PoS
- Algorithme de consensus
- Mempool
- EIP
- BIP
- EVM
- Block reward
- SegWit
- Multisig
- P2SH
- HTLC
- CoinJoin
- finalité de paiement
- block time
- arbre de Merkle
- hash / empreinte numérique

## 9.5 `Concept` → `StakeholderCategory`
Quand le terme désigne une catégorie d’acteurs générique plutôt qu’un concept :
- Investisseurs institutionnels
- Fabricant de matériel dédié (ASIC)
- Fournisseur de services de paiement
- Mineur solo
- Nœud complet / nœud léger / nœud mineur si usage catégoriel générique

## 9.6 `Concept` → `ChapterSection` ou suppression
Ces entrées ne doivent pas rester dans `Concept` :
- II.3 Au-delà de la revendication d’une absence de gouvernance !
- III.3 Une gouvernance publique d’exception : le hard fork d’Ethereum consécutif à l’attaque de “The DAO”
- W.J. van der Laan — style de mainteneur
- Médias spécialisés CM / Enseignements et formations
- Transcription d’entretien
- toute entrée purement rédactionnelle ou de note

## 10. InfrastructureDomain — canonisation

## 10.1 Domaines canoniques proposés
Créer une liste canonique unique :

1. `Protocole et couche de base`
2. `Traitement des transactions`
3. `Services de portefeuille et de paiement`
4. `Conformité réglementaire`
5. `Information et connaissance`
6. `Sphère d’usage`
7. `Confidentialité et anonymisation`
8. `Altcoins, tokens et surcouches`
9. `Interopérabilité et passerelles fiat/crypto`

## 10.2 Fusions proposées
| Canonique | Remplace |
|---|---|
| Conformité réglementaire | De conformité aux réglementations nationales ; De conformité aux réglementations nationales — Ethereum |
| Traitement des transactions | De l'activité de traitement des transactions ; De l'activité de traitement des transactions Ethereum |
| Information et connaissance | De l'information et de la connaissance ; De l'information et de la connaissance — Ethereum |
| Sphère d’usage | De la sphère d'usage (financière & réelle) ; De la sphère d'usage Ethereum (financière & réelle) |
| Services de portefeuille et de paiement | Des services de portefeuille et de paiements ; Des services de portefeuille et de paiements Ethereum |
| Protocole et couche de base | Du protocole Bitcoin (couche 1 et 2) ; Du protocole Ethereum (couche 1 et 2) |
| Altcoins, tokens et surcouches | Des "Altcoins" ; Des Altcoins et tokens — écosystème Ethereum |

Puis relier chaque domaine canonique aux protocoles concernés via `instantiatedInProtocol`.

## 11. Crises et gouvernance — normalisation

## 11.1 Séparer clairement les niveaux
- `CrisisEvent` = événement ou crise identifiée
- `GovernanceConflict` = controverse / antagonisme / conflit d’interprétation
- `GovernanceProcess` = séquence de décision, réparation, arbitrage
- `CrisisPhase` = moments internes d’un événement de crise
- `GovernanceArena` = lieux et dispositifs de discussion/coordination

## 11.2 DAO — modèle canonique
- `CrisisEvent` : Attaque de The DAO
- `GovernanceConflict` : Conflit DAO Fork (2016)
- `GovernanceProcess` : DAO Fork délibération (juin-juillet 2016)
- `GovernanceArena` : Carbon Vote ; GitHub Ethereum ; All Core Dev Meetings ; médias / forums si nécessaire
- `CrisisPhase` :
  - DAO — Déclenchement
  - DAO — Insémination / gestation
  - DAO — Remise en ordre
  - DAO — Bifurcation / stabilisation

Supprimer ou fusionner :
- `Ethereum DAO Hard Fork`
- `Ethereum Hard Fork (juillet 2016)`
- `Secession Ethereum Classic`
si ces entrées désignent simplement des moments ou conséquences du même processus ; sinon les relier explicitement comme sous-événements.

## 11.3 CVE-2018-17144 — modèle canonique
- `CrisisEvent` : Bitcoin CVE-2018-17144
- `GovernanceProcess` : CVE-2018-17144 résolution (septembre 2018)
- `GovernanceArena` : Bitcoin-dev Mailing List ; GitHub Bitcoin Core ; huis clos mainteneurs
- `CrisisPhase` :
  - Signalement et divulgation responsable
  - Évaluation en huis clos
  - Remise en ordre par patch
  - Révélation publique et consensus ex post

## 12. Monétisation comme pivot — recommandations de modélisation

Créer un nœud central canonique :
- `ConceptCore | Monétisation des cryptomonnaies`

Le relier à :
- `UCN BTC`
- `UCN ETH`
- `Bitcoin`
- `Ethereum`
- `InfrastructureDomain`
- `StakeholderCategory`
- `Organization`
- `PlatformService`
- `Marketplace`
- `Capability`
- `CrisisEvent`
- `GovernanceProcess`

Sous-concepts directement rattachés :
- Processus de monétisation progressive de Bitcoin
- Monnayage
- Monnaie parallèle
- Monnaie communautaire
- Interopérabilité
- Passerelle
- Réintermédiation
- Développement infrastructurel par phases
- Dollarisation via stablecoins
- Hyper-bitcoinisation / hyper-cryptomonétisation (si maintenu)
- Qualités monétaires désirables / luttes sur la bonne monnaie

## 13. Ordre d’implémentation recommandé

### Phase 1 — sûreté structurelle
1. sauvegarde snapshot v90
2. ajout des nouveaux types
3. ajout des nouvelles relations
4. introduction des champs `canonicalName`, `aliases`, `normalizedLabel`

### Phase 2 — anti-doublons
5. fusion des doublons `Person`
6. fusion des doublons `Protocol`
7. fusion des doublons `TheoreticFramework`
8. fusion des doublons `Concept` certains

### Phase 3 — retypage
9. corriger `Person`
10. éclater `ActorGroup` en `Institution` / `Organization` / `ActorGroup` / `StakeholderCategory`
11. éclater `ActorNonHuman`
12. reclasser les faux `Concept`

### Phase 4 — réorganisation analytique
13. canoniser les `InfrastructureDomain`
14. homogénéiser `CrisisEvent` / `CrisisPhase` / `GovernanceConflict` / `GovernanceProcess`
15. créer le pivot `Monétisation des cryptomonnaies`
16. relier les sous-ensembles au pivot

### Phase 5 — hygiène finale
17. recalculer les relations orphelines
18. supprimer les entités vides / titres / labels résiduels
19. vérifier la cohérence des comptages
20. produire un export v91 + rapport de migration

## 14. Instructions d’implémentation pour l’agent

### Contraintes
- Ne pas supprimer brutalement une entité sans d’abord remapper ses relations.
- Toute fusion doit :
  1. choisir un canonique,
  2. transférer toutes les relations entrantes/sortantes,
  3. stocker l’ancien label en alias,
  4. journaliser l’opération.

### Règle de priorité
- priorité absolue aux erreurs de typage manifestes ;
- puis fusions certaines ;
- puis reclassements conceptuels ;
- puis raffinements plus interprétatifs.

### Journal minimal à produire
Pour chaque opération :
- `op_id`
- `action` (`merge`, `retype`, `split`, `create_type`, `create_relation`, `delete_after_remap`)
- `old_entity`
- `new_entity`
- `old_type`
- `new_type`
- `confidence` (`certain`, `strong`, `interpretive`)
- `rationale`

## 15. Patch minimal garanti (sans choix interprétatifs risqués)

Le noyau de patch qui peut être appliqué immédiatement avec forte confiance est :
- fusion des doublons nominaux explicites ;
- retypage de `Bitmain`, `CEX.io`, `Desmedt et Lakomski-Laguerre`, `De Boyer des Roches et Rosales` ;
- reclassement des banques centrales, institutions académiques et organisations opérationnelles hors de `ActorGroup` ;
- reclassement des catégories d’acteurs génériques vers `StakeholderCategory` ;
- sortie de `Preuve de Travail (PoW)` et `chaîne de blocs` hors de `ActorNonHuman` ;
- fusion/canonisation des domaines infrastructurels BTC/ETH ;
- suppression ou reclassement des faux concepts documentaires.

## 16. Résultat attendu en v91

À l’issue du patch, le graphe doit permettre de lire immédiatement :

- quels sont les **protocoles** étudiés ;
- quels sont leurs **objets monétaires** ;
- comment se structure leur **développement infrastructurel** ;
- quelles **organisations**, **institutions**, **collectifs** et **catégories d’acteurs** y participent ;
- par quelles **passerelles** et infrastructures s’opère la **monétisation** ;
- comment les **crises** révèlent la **gouvernance duale** et la **polycentricité** ;
- quels sont les **concepts centraux** de la thèse, distincts des notions techniques secondaires.

En d’autres termes : le graphe doit devenir non seulement plus propre, mais plus explicitement **maël-rollandien** dans son architecture.

