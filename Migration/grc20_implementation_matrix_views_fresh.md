# Matrice d’implémentation — rééquilibrage des vues du graphe

Cette matrice part de trois sources :
1. la logique de la thèse ;
2. les vues actuellement exposées dans le graphe live ;
3. le réservoir historique d’entités déjà visibles dans l’inventaire et les matériaux de migration.

Elle sert à guider un **backfill sélectif** et un **reroutage par vue**, pas à produire une symétrie artificielle.

## Structure de la thèse

### Chap. I × Objets → Objets
- **Diagnostic** : Sous-alimenté par rapport à I.2 et I.3.
- **Familles attendues** : InfrastructureEvent, PlatformService, SoftwareClient, Marketplace, HardwareDevice, Protocol, DevelopmentPhase, InfrastructureSegment
- **Entités candidates à injecter / rerouter** : Bitcoin Faucet; BitcoinMarket; MyBitcoin; Bitcoin Foundation; Migration du code Bitcoin vers GitHub; WordPress accepte les paiements en Bitcoin; eBay/PayPal intègre Bitcoin; Casascius; Colored Coins; Mastercoin/Omni; Counterparty; Namecoin; Litecoin; Peercoin; BTCC; Kraken; Paymium; Ether Genesis Sale; Frontier; Lancement d’Ethereum
- **Priorité** : P1

### Chap. I × Acteurs → Acteurs
- **Diagnostic** : Trop faible pour un chapitre aussi peuplé en concepteurs, entrepreneurs et intermédiaires.
- **Familles attendues** : Person, Organization, StakeholderGroup
- **Entités candidates à injecter / rerouter** : Satoshi Nakamoto; Gavin Andresen; Martti Malmi; Mike Hearn; Charlie Shrem; Roger Ver; Jesse Powell; Bobby Lee; Vitalik Buterin; Gavin Wood; Mihai Alisie; Joseph Poon; Thaddeus Dryja; Coinbase; BitPay; Kraken; Ethereum Foundation
- **Priorité** : P1

### Chap. I × Concepts → Concepts
- **Diagnostic** : Plutôt riche, mais le noyau analytique pourrait être plus visible que les concepts techniques dispersés.
- **Familles attendues** : CoreConcept, SecondaryConcept, TechnicalConcept
- **Entités candidates à injecter / rerouter** : Infrastructure sociotechnique; Développement carnavalesque; Logique de consensus distribué; Réintermédiation; Régulations transactionnelles; UCN / unité de compte native
- **Priorité** : P2

### Chap. II × Objets → Objets
- **Diagnostic** : Sous-rempli alors que la monétisation repose sur des médiations et mécanismes concrets.
- **Familles attendues** : MonetaryObject, PlatformService, Marketplace, Capability, InfrastructureDomain, InfrastructureSegment
- **Entités candidates à injecter / rerouter** : UCN BTC; UCN ETH; Passerelle fiat; Bourse d’échange avec passerelle fiat; Découverte du prix; Liquidité du marché Bitcoin; Offre des UCN BTC; Demande des UCN BTC; WBTC; Stablecoin; services de prêts/DEX/collatéralisation; wallets custodial/non-custodial
- **Priorité** : P1

### Chap. II × Gouvern. → Gouvern.
- **Diagnostic** : Doit devenir le vrai cœur de la clarification de gouvernance, sans pollution CVE.
- **Familles attendues** : GovernanceProcess, GovernanceConflict, GovernanceArena, ProtocolProposal, CoreConcept
- **Entités candidates à injecter / rerouter** : Scaling Debate; Guerre des blocs; Gouvernance polycentrique; Gouvernance duale; stakeholders/shareholders; Bitcoin-dev Mailing List; GitHub Bitcoin Core; Bitcointalk; Conférences Scaling Bitcoin; BIP family; UASF; SegWit2X
- **Priorité** : P1

### Chap. II × Acteurs → Acteurs
- **Diagnostic** : Correct mais peut être épaissi autour des camps, catégories et organisations de gouvernance.
- **Familles attendues** : StakeholderCategory, StakeholderGroup, Organization, Person
- **Entités candidates à injecter / rerouter** : Core Developers (Bitcoin); Big Blockers; Small Blockers; mineurs; full nodes; Blockstream; Bitmain; Adam Back; Jihan Wu; Shaolin Fry; Theymos
- **Priorité** : P1

### Chap. III × Crises → Crises
- **Diagnostic** : Normalement dense, mais à segmenter pour éviter la nappe CVE.
- **Familles attendues** : CrisisEvent, CrisisPhase, ProtocolProposal
- **Entités candidates à injecter / rerouter** : Bitcoin CVE 2018-17144; phases CVE; The DAO; Hard Fork Ethereum; Soft Fork DAO (abandon); Ethereum Classic; série de CVE Bitcoin; Value Overflow; Netsplit; BIP-50
- **Priorité** : P1

### Chap. III × Gouvern. → Gouvern.
- **Diagnostic** : Doit montrer les processus et concepts de gouvernement de crise, pas seulement les cas.
- **Familles attendues** : GovernanceProcess, GovernanceArena, CoreConcept, GovernanceConflict
- **Entités candidates à injecter / rerouter** : Politique de crises; Gouvernance de huis clos; Responsible disclosure; Mise en crise / Remise en ordre; Esprit du code vs Lettre du code; repo Bitcoin Core; All Core Dev Meetings; Carbon Vote
- **Priorité** : P1

### Chap. III × Acteurs → Acteurs
- **Diagnostic** : Encore trop faible pour des chapitres aussi peuplés en intervenants, équipes et coalitions.
- **Familles attendues** : Person, StakeholderGroup, Organization
- **Entités candidates à injecter / rerouter** : Awemany; Matt Corallo; Wladimir van der Laan; Peter Wuille; Greg Maxwell; Cory Fields; Whitehat Group; Core Developers (Ethereum); Ethereum Foundation; Vitalik Buterin; Gavin Wood; Vlad Zamfir; Stephan Tual
- **Priorité** : P1

### Multi. × Concepts → Concepts
- **Diagnostic** : Sous-exploité pour les concepts réellement transversaux.
- **Familles attendues** : CoreConcept, TheoreticFramework
- **Entités candidates à injecter / rerouter** : Infrastructure sociotechnique; Monétisation; Gouvernance duale; Gouvernance polycentrique; Crises comme épreuves d’explicitation; Règle / discrétion; Hétérogénéité des monnaies; Syllogisme libéral-techniciste; STS; IMF
- **Priorité** : P1

### Multi. × Gouvern. → Gouvern.
- **Diagnostic** : Peut porter les mécanismes transversaux plutôt que de tout surcharger l’Intro.
- **Familles attendues** : CoreConcept, GovernanceProcess
- **Entités candidates à injecter / rerouter** : Gouvernance par l’infrastructure; Gouvernance sur l’infrastructure; Gouvernance duale; Mise en crise / Remise en ordre; Politique de crises
- **Priorité** : P2

### Toutes bandes × Réf./Sources → Réf./Sources
- **Diagnostic** : Trop dominante visuellement.
- **Familles attendues** : Reference, PrimarySource, SourceQuote, AcademicWork
- **Entités candidates à injecter / rerouter** : Conserver l’existant mais réduire la présence simultanée; réserver les labels persistants aux références structurantes
- **Priorité** : P2

## Monétisation des CM

### Thèse × Noyau → Noyau
- **Diagnostic** : Doit être beaucoup plus affirmé conceptuellement.
- **Familles attendues** : CoreConcept, MonetaryObject
- **Entités candidates à injecter / rerouter** : Monétisation; Monnayage; UCN BTC; UCN ETH; Communauté de paiement / groupe monétaire; nominalisme non étatiste
- **Priorité** : P1

### Mécanismes × Émission → Émission
- **Diagnostic** : Sous-rempli au regard de la diversité des modes d’émission et de distribution.
- **Familles attendues** : TechnicalConcept, Capability, InfrastructureEvent
- **Entités candidates à injecter / rerouter** : Block reward; halving; distribution initiale de bitcoins; premine; ICO; genesis sale; Proof of Work; Proof of Stake; issuance programmatique
- **Priorité** : P1

### Mécanismes × Circulation → Circulation
- **Diagnostic** : Trop maigre si l’on veut montrer l’entrée en circulation effective des UCN.
- **Familles attendues** : Capability, Concept, InfrastructureEvent
- **Entités candidates à injecter / rerouter** : transactions; paires de trading BTC/$; NewLibertyStandard; marché BTC/$; liquidité; volume; exchange liquidity; Bitcoin comme paire pivot
- **Priorité** : P1

### Infrastructures × Accès → Accès
- **Diagnostic** : Doit devenir l’un des gros pôles de la vue.
- **Familles attendues** : PlatformService, Marketplace, HardwareDevice, SoftwareClient, InfrastructureSegment
- **Entités candidates à injecter / rerouter** : wallet custodial; wallet non-custodial; hardware wallet; Coinbase; Kraken; Paymium; BTCC; ATM; BitPay; passerelles fiat; Ledger; Trezor
- **Priorité** : P1

### Cas × Usages → Usages
- **Diagnostic** : Sous-rempli alors que c’est là que la thèse tranche le débat monétaire.
- **Familles attendues** : InfrastructureEvent, Marketplace, ActorNonHuman, Concept
- **Entités candidates à injecter / rerouter** : Silk Road; Satoshi Dice; WordPress; WikiLeaks; eBay/PayPal; usages en compte et en paiement; usages de réserve de valeur; usages de collatéralisation
- **Priorité** : P1

### Mécanismes × Valorisation → Valorisation
- **Diagnostic** : Sous-rempli alors que la thèse insiste sur prix, liquidité et croyances de marché.
- **Familles attendues** : Concept, Capability, InfrastructureEvent
- **Entités candidates à injecter / rerouter** : Découverte du prix; Liquidité du marché Bitcoin; Offre des UCN BTC; Demande des UCN BTC; Preuve d’usage économique; Hyper-bitcoinisation; Vision 'or numérique'; Vision 'système de paiement'
- **Priorité** : P1

### Acteurs × Stabilisation → Stabilisation
- **Diagnostic** : Doit être plus dense : la monétisation n’est pas séparable des dispositifs de stabilisation/gouvernance.
- **Familles attendues** : StakeholderGroup, GovernanceProcess, GovernanceArena, ProtocolProposal
- **Entités candidates à injecter / rerouter** : Bitcoin Core repo; Core Developers; BIP family; SegWit; UASF; Responsible disclosure; Gouvernance duale; Gouvernance polycentrique
- **Priorité** : P1

### Réf. × toutes colonnes → Réf.
- **Diagnostic** : Utile, mais doit rester terminale et légère.
- **Familles attendues** : Reference, SourceQuote, AcademicWork
- **Entités candidates à injecter / rerouter** : Mallard et al.; Blanc; Théret; Orléan; citations sur usages en compte/paiement et monétisation
- **Priorité** : P2

## Qui gouverne réellement ?

### Problématisation × Catégories → Catégories
- **Diagnostic** : Doit mieux exposer les catégories analytiques avant les groupes empiriques.
- **Familles attendues** : StakeholderCategory, CoreConcept
- **Entités candidates à injecter / rerouter** : développeurs core; mineurs; full nodes; wallet providers; marchands; bourses d’échange; utilisateurs; régulateurs
- **Priorité** : P1

### Routine/Coordination × Arènes → Arènes
- **Diagnostic** : Colonne originale mais encore sous-exploitée.
- **Familles attendues** : GovernanceArena
- **Entités candidates à injecter / rerouter** : Bitcoin-dev Mailing List; GitHub Bitcoin Core; Bitcointalk; Reddit r/Bitcoin; All Core Dev Meetings; GitHub Ethereum; Carbon Vote; conférences Scaling Bitcoin
- **Priorité** : P1

### Conflit × Groupes → Groupes
- **Diagnostic** : Doit être l’un des grands pôles de la vue.
- **Familles attendues** : StakeholderGroup, GovernanceConflict
- **Entités candidates à injecter / rerouter** : Big Blockers; Small Blockers; Core Developers (Bitcoin); Core Developers (Ethereum); Whitehat Group; Partisans Ethereum Classic; détenteurs de jetons DAO
- **Priorité** : P1

### Décision/Maintenance × Personnes → Personnes
- **Diagnostic** : Encore trop faible : les personnes agissantes doivent apparaître comme telles.
- **Familles attendues** : Person
- **Entités candidates à injecter / rerouter** : Peter Wuille; Greg Maxwell; Wladimir van der Laan; Matt Corallo; Cory Fields; Adam Back; Jihan Wu; Vitalik Buterin; Gavin Wood; Vlad Zamfir; Stephan Tual; Awemany
- **Priorité** : P1

### Décision × Organisations → Organisations
- **Diagnostic** : Sous-rempli alors que les organisations structurent une partie du pouvoir effectif.
- **Familles attendues** : Organization, Institution
- **Entités candidates à injecter / rerouter** : Blockstream; Bitmain; Ethereum Foundation; exchanges majeures; Coinbase; Kraken; Slock.it
- **Priorité** : P2

### Exception × Cas / Réf. → Cas / Réf.
- **Diagnostic** : Doit séparer clairement cas empiriques et références terminales.
- **Familles attendues** : CrisisEvent, GovernanceProcess, Reference, SourceQuote
- **Entités candidates à injecter / rerouter** : Bitcoin CVE 2018-17144; The DAO; Scaling Debate (si affiché ici comme cas-limite); citations De Filippi & Loveluck; entretiens clés
- **Priorité** : P1

## Priorités globales
1. **Regonfler Chap. I × Objets et Chap. I × Acteurs**.
2. **Recomposer la vue Monétisation** autour des mécanismes, infrastructures, usages, valorisation et stabilisation.
3. **Renforcer Chap. III × Acteurs** pour que la gouvernance de crise soit portée par des personnes, groupes et arènes visibles.
4. **Muscler le bandeau Multi.** pour les concepts transversaux.
5. **Réduire la domination visuelle de Réf./Sources** sans supprimer les références.
