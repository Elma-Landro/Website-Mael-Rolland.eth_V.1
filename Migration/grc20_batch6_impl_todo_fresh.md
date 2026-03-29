# Batch 6 — Todo implémenteur par vue et par cellule

Ce document convertit la matrice analytique en **plan d’action opérationnel**.

Chaque entrée suit quatre verbes simples :
- **créer / backfill** : ajouter ou faire réapparaître la matière pertinente
- **rerouter** : déplacer la présence vers la bonne vue/cellule
- **multi-affecter** : autoriser une présence secondaire utile dans une autre vue
- **dédensifier** : calmer les zones trop lourdes visuellement

## Structure de la thèse

### Chap. I × Objets
- **Action** : rerouter + backfill
- **Pourquoi** : Le développement infrastructural de Bitcoin et l’émergence d’Ethereum sont sous-représentés dans cette cellule.
- **Entités candidates** : Bitcoin Faucet; BitcoinMarket; MyBitcoin; Bitcoin Foundation; Migration du code Bitcoin vers GitHub; WordPress accepte les paiements en Bitcoin; eBay/PayPal intègre Bitcoin; Casascius; Colored Coins; Mastercoin/Omni; Counterparty; Namecoin; Litecoin; Peercoin; BTCC; Kraken; Paymium; Ether Genesis Sale; Frontier; Lancement d’Ethereum
- **Règle d’implémentation** : Réancrer en priorité vers Chap. I / Objets tout événement d’infrastructure, de service, d’accès, de métaprotocole ou d’émergence Ethereum actuellement absorbé par Chap. II ou III.
- **Contrôle de rendu** : La colonne Objets du Chap. I doit devenir l’un des gros pôles de la vue, sans ressembler à un mur compact.
- **Priorité** : P1

### Chap. I × Acteurs
- **Action** : backfill + rerouter
- **Pourquoi** : Le chapitre I mobilise bien plus de personnes, organisations et entrepreneurs d’infrastructure que ce que la vue laisse voir.
- **Entités candidates** : Satoshi Nakamoto; Gavin Andresen; Martti Malmi; Mike Hearn; Charlie Shrem; Roger Ver; Jesse Powell; Bobby Lee; Vitalik Buterin; Gavin Wood; Mihai Alisie; Joseph Poon; Thaddeus Dryja; Coinbase; BitPay; Kraken; Ethereum Foundation
- **Règle d’implémentation** : Rapprocher les acteurs pionniers des objets/services qu’ils portent, au lieu de les laisser finir en bruit terminal ou dans Réf./Sources.
- **Contrôle de rendu** : La colonne Acteurs du Chap. I doit faire apparaître une socio-histoire du développement, pas seulement quelques noms isolés.
- **Priorité** : P1

### Chap. II × Objets
- **Action** : backfill + multi-affectation
- **Pourquoi** : La monétisation y passe par des objets, médiations, marchés et dispositifs concrets encore trop peu présents.
- **Entités candidates** : UCN BTC; UCN ETH; Passerelle fiat; Bourse d’échange avec passerelle fiat; Découverte du prix; Liquidité du marché Bitcoin; Offre des UCN BTC; Demande des UCN BTC; WBTC; Stablecoin; services de prêts/DEX/collatéralisation; wallets custodial/non-custodial
- **Règle d’implémentation** : Autoriser une double présence contrôlée des objets qui relèvent à la fois de Chap. I comme développement infrastructural et de Chap. II comme mécanismes de monétisation.
- **Contrôle de rendu** : Chap. II × Objets doit cesser d’être maigre ; il doit montrer les médiations monétaires concrètes.
- **Priorité** : P1

### Chap. II × Gouvern.
- **Action** : rerouter + nettoyage
- **Pourquoi** : Cette cellule doit montrer la clarification de gouvernance, pas être polluée par les cas de crise.
- **Entités candidates** : Scaling Debate; Guerre des blocs; Gouvernance polycentrique; Gouvernance duale; stakeholders/shareholders; Bitcoin-dev Mailing List; GitHub Bitcoin Core; Bitcointalk; Conférences Scaling Bitcoin; BIP family; UASF; SegWit2X
- **Règle d’implémentation** : Exclure par défaut les CVE et autres crises détaillées ; garder ici les conflits, processus, arènes et concepts de gouvernance du chapitre II.
- **Contrôle de rendu** : En focus Chap. II → Gouvern., on doit voir le bloc polycentric governance / scaling / arenas, pas la CVE.
- **Priorité** : P1

### Chap. II × Acteurs
- **Action** : backfill + hiérarchisation
- **Pourquoi** : Les camps, catégories et organisations de la gouvernance y restent encore trop peu structurés.
- **Entités candidates** : Core Developers (Bitcoin); Big Blockers; Small Blockers; mineurs; full nodes; Blockstream; Bitmain; Adam Back; Jihan Wu; Shaolin Fry; Theymos
- **Règle d’implémentation** : Ordonner visuellement catégorie → organisation → groupe → personne à l’intérieur de la cellule.
- **Contrôle de rendu** : Cette cellule doit montrer une architecture de gouvernement distribué, pas une simple liste d’acteurs.
- **Priorité** : P1

### Chap. III × Crises
- **Action** : segmenter + dédensifier
- **Pourquoi** : La cellule est légitime comme pôle dense, mais elle devient vite une nappe illisible si toutes les crises et phases sortent en même temps.
- **Entités candidates** : Bitcoin CVE 2018-17144; phases CVE; The DAO; Hard Fork Ethereum; Soft Fork DAO (abandon); Ethereum Classic; série de CVE Bitcoin; Value Overflow; Netsplit; BIP-50
- **Règle d’implémentation** : Organiser en sous-clusters : cas majeurs / phases / CVE techniques / réponses / scissions.
- **Contrôle de rendu** : La cellule doit rester dense mais lisible ; les cas majeurs doivent dominer visuellement.
- **Priorité** : P1

### Chap. III × Gouvern.
- **Action** : backfill + rerouter
- **Pourquoi** : Cette cellule doit montrer les processus et concepts du gouvernement de crise, pas seulement des noms de cas.
- **Entités candidates** : Politique de crises; Gouvernance de huis clos; Responsible disclosure; Mise en crise / Remise en ordre; Esprit du code vs Lettre du code; repo Bitcoin Core; All Core Dev Meetings; Carbon Vote
- **Règle d’implémentation** : Faire remonter ici les concepts/processus, laisser les cas détaillés en Crises.
- **Contrôle de rendu** : On doit lire ici la grammaire du gouvernement de crise.
- **Priorité** : P1

### Chap. III × Acteurs
- **Action** : backfill + rerouter
- **Pourquoi** : Les acteurs effectifs des crises Bitcoin et Ethereum restent trop peu visibles.
- **Entités candidates** : Awemany; Matt Corallo; Wladimir van der Laan; Peter Wuille; Greg Maxwell; Cory Fields; Whitehat Group; Core Developers (Ethereum); Ethereum Foundation; Vitalik Buterin; Gavin Wood; Vlad Zamfir; Stephan Tual
- **Règle d’implémentation** : Rendre visibles les personnes et groupes agissants sans les envoyer mécaniquement tout à droite comme simples extrémités.
- **Contrôle de rendu** : Cette cellule doit être clairement plus peuplée que maintenant.
- **Priorité** : P1

### Multi. × Concepts
- **Action** : multi-affectation + backfill
- **Pourquoi** : Les concepts transversaux restent trop absorbés par l’Intro ou disséminés dans les chapitres.
- **Entités candidates** : Infrastructure sociotechnique; Monétisation; Gouvernance duale; Gouvernance polycentrique; Crises comme épreuves d’explicitation; Règle / discrétion; Hétérogénéité des monnaies; Syllogisme libéral-techniciste; STS; IMF
- **Règle d’implémentation** : Créer un vrai réservoir transversal : maintenir un primaryChapter, mais autoriser une présence Multi. pour les concepts structurants de l’ensemble.
- **Contrôle de rendu** : La bande Multi. doit devenir lisible et intellectuellement utile.
- **Priorité** : P1

### Toutes bandes × Réf./Sources
- **Action** : dédensifier
- **Pourquoi** : La colonne terminale domine trop visuellement et absorbe de l’attention au détriment des autres familles.
- **Entités candidates** : Conserver l’existant mais réduire labels persistants et opacité de fond
- **Règle d’implémentation** : Limiter les labels persistants aux références structurantes, garder le reste en arrière-plan ou sur interaction.
- **Contrôle de rendu** : Réf./Sources doit rester riche mais plus poreuse visuellement.
- **Priorité** : P2

## Monétisation des CM

### Thèse × Noyau
- **Action** : backfill
- **Pourquoi** : Le noyau conceptuel de la monétisation doit être beaucoup plus affirmé.
- **Entités candidates** : Monétisation; Monnayage; UCN BTC; UCN ETH; Communauté de paiement / groupe monétaire; nominalisme non étatiste
- **Règle d’implémentation** : Faire remonter explicitement les concepts pivots et les objets monétaires natifs dans cette cellule.
- **Contrôle de rendu** : Le noyau doit être immédiatement lisible au premier coup d’œil.
- **Priorité** : P1

### Mécanismes × Émission
- **Action** : backfill
- **Pourquoi** : La diversité des formes d’émission/distribution est sous-montrée.
- **Entités candidates** : Block reward; halving; distribution initiale de bitcoins; premine; ICO; genesis sale; Proof of Work; Proof of Stake; issuance programmatique
- **Règle d’implémentation** : Traiter ces mécanismes comme objets analytiques de monétisation, pas comme détails techniques isolés.
- **Contrôle de rendu** : La colonne Émission doit devenir dense mais claire.
- **Priorité** : P1

### Mécanismes × Circulation
- **Action** : backfill
- **Pourquoi** : La circulation effective des UCN n’est pas assez montrée.
- **Entités candidates** : transactions; paires de trading BTC/$; NewLibertyStandard; marché BTC/$; liquidité; volume; exchange liquidity; Bitcoin comme paire pivot
- **Règle d’implémentation** : Regrouper les mécanismes de circulation économique et de mise en marché dans cette cellule.
- **Contrôle de rendu** : Circulation doit cesser d’être une colonne maigre.
- **Priorité** : P1

### Infrastructures × Accès
- **Action** : backfill massif
- **Pourquoi** : L’accès est l’un des grands ressorts de la monétisation, mais il reste trop peu peuplé.
- **Entités candidates** : wallet custodial; wallet non-custodial; hardware wallet; Coinbase; Kraken; Paymium; BTCC; ATM; BitPay; passerelles fiat; Ledger; Trezor
- **Règle d’implémentation** : Y concentrer les dispositifs d’accès, conversion, détention et dépense.
- **Contrôle de rendu** : Accès doit devenir l’un des plus gros pôles de la vue.
- **Priorité** : P1

### Cas × Usages
- **Action** : backfill + rerouter
- **Pourquoi** : C’est ici que la thèse tranche le débat monétaire par les usages ; la cellule ne peut pas rester maigre.
- **Entités candidates** : Silk Road; Satoshi Dice; WordPress; WikiLeaks; eBay/PayPal; usages en compte et en paiement; usages de réserve de valeur; usages de collatéralisation
- **Règle d’implémentation** : Faire remonter les cas d’usage monétaire et non monétaire à forte portée démonstrative.
- **Contrôle de rendu** : Cette cellule doit être beaucoup plus parlante et empirique.
- **Priorité** : P1

### Mécanismes × Valorisation
- **Action** : backfill
- **Pourquoi** : La valorisation repose sur prix, liquidité, croyances et représentations, encore trop peu visibles.
- **Entités candidates** : Découverte du prix; Liquidité du marché Bitcoin; Offre des UCN BTC; Demande des UCN BTC; Preuve d’usage économique; Hyper-bitcoinisation; Vision 'or numérique'; Vision 'système de paiement'
- **Règle d’implémentation** : Montrer ensemble mécanismes de marché et cadres interprétatifs de valorisation.
- **Contrôle de rendu** : Valorisation doit devenir un vrai pôle analytique.
- **Priorité** : P1

### Acteurs × Stabilisation
- **Action** : backfill + multi-affectation
- **Pourquoi** : La monétisation n’est pas séparable des dispositifs de stabilisation, de maintenance et de gouvernance.
- **Entités candidates** : Bitcoin Core repo; Core Developers; BIP family; SegWit; UASF; Responsible disclosure; Gouvernance duale; Gouvernance polycentrique
- **Règle d’implémentation** : Autoriser une présence croisée avec les vues de gouvernance/crise, sans les noyer.
- **Contrôle de rendu** : Stabilisation doit devenir dense et structurée, pas périphérique.
- **Priorité** : P1

### Réf. × toutes colonnes
- **Action** : dédensifier
- **Pourquoi** : Les références sont utiles mais ne doivent pas dominer la vue processuelle.
- **Entités candidates** : Mallard et al.; Blanc; Théret; Orléan; citations sur usages en compte/paiement et monétisation
- **Règle d’implémentation** : Réserver les labels persistants aux références les plus structurantes.
- **Contrôle de rendu** : La ligne Réf. doit rester lisible mais légère.
- **Priorité** : P2

## Qui gouverne réellement ?

### Problématisation × Catégories
- **Action** : backfill + hiérarchisation
- **Pourquoi** : Les catégories analytiques doivent apparaître avant les groupes empiriques.
- **Entités candidates** : développeurs core; mineurs; full nodes; wallet providers; marchands; bourses d’échange; utilisateurs; régulateurs
- **Règle d’implémentation** : Afficher d’abord les catégories, puis seulement les instanciations empiriques ailleurs dans la vue.
- **Contrôle de rendu** : Catégories doit devenir une vraie colonne d’entrée analytique.
- **Priorité** : P1

### Routine/Coordination × Arènes
- **Action** : backfill
- **Pourquoi** : Les arènes sont au cœur de ton approche mais restent encore visuellement sous-exploitées.
- **Entités candidates** : Bitcoin-dev Mailing List; GitHub Bitcoin Core; Bitcointalk; Reddit r/Bitcoin; All Core Dev Meetings; GitHub Ethereum; Carbon Vote; conférences Scaling Bitcoin
- **Règle d’implémentation** : Accentuer la colonne Arènes avec labels mieux prioritaires et halo plus lisible.
- **Contrôle de rendu** : Arènes doit devenir immédiatement reconnaissable comme colonne structurante.
- **Priorité** : P1

### Conflit × Groupes
- **Action** : backfill
- **Pourquoi** : Les conflits doivent être portés par des groupes/camps visibles, pas seulement par des concepts ou des cas.
- **Entités candidates** : Big Blockers; Small Blockers; Core Developers (Bitcoin); Core Developers (Ethereum); Whitehat Group; Partisans Ethereum Classic; détenteurs de jetons DAO
- **Règle d’implémentation** : Rendre les groupes empiriques plus massifs et plus lisibles dans cette cellule.
- **Contrôle de rendu** : Groupes en conflit doit être l’un des grands pôles de la vue.
- **Priorité** : P1

### Décision/Maintenance × Personnes
- **Action** : backfill + rerouter
- **Pourquoi** : Les personnes agissantes restent trop peu visibles alors qu’elles incarnent la gouvernance effective.
- **Entités candidates** : Peter Wuille; Greg Maxwell; Wladimir van der Laan; Matt Corallo; Cory Fields; Adam Back; Jihan Wu; Vitalik Buterin; Gavin Wood; Vlad Zamfir; Stephan Tual; Awemany
- **Règle d’implémentation** : Maintenir les personnes près des groupes, arènes et processus auxquels elles participent ; ne pas les rejeter comme simple bruit terminal.
- **Contrôle de rendu** : La colonne Personnes doit enfin montrer qui gouverne effectivement.
- **Priorité** : P1

### Décision × Organisations
- **Action** : backfill
- **Pourquoi** : Les organisations structurent une partie du pouvoir effectif et doivent apparaître plus clairement.
- **Entités candidates** : Blockstream; Bitmain; Ethereum Foundation; Coinbase; Kraken; Slock.it
- **Règle d’implémentation** : Faire ressortir les organisations comme intermédiaires de pouvoir, distincts des groupes et des personnes.
- **Contrôle de rendu** : Organisations doit cesser d’être une colonne secondaire vide.
- **Priorité** : P2

### Exception × Cas / Réf.
- **Action** : rerouter + split interne
- **Pourquoi** : Les cas empiriques et les références terminales se mélangent trop facilement.
- **Entités candidates** : Bitcoin CVE 2018-17144; The DAO; Scaling Debate (cas-limite); citations De Filippi & Loveluck; entretiens clés
- **Règle d’implémentation** : Scinder visuellement la cellule : partie haute pour les cas, partie basse pour les références/sources.
- **Contrôle de rendu** : Cas / Réf. doit être riche mais nettement lisible.
- **Priorité** : P1

## Ordre recommandé
1. Structure de la thèse — Chap. I × Objets / Acteurs
2. Structure de la thèse — Chap. II × Gouvern. / Objets
3. Structure de la thèse — Chap. III × Gouvern. / Acteurs / Crises
4. Monétisation des CM — Accès / Usages / Valorisation / Stabilisation
5. Qui gouverne réellement ? — Catégories / Arènes / Groupes / Personnes
6. Dédensification contrôlée de Réf./Sources
