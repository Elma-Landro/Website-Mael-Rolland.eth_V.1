# État de chantier — Catalogue d'événements v3 (figure V2.8 décodée + chap. II) — 05/08/2026

## Fait cette session

**1. Le `.bin` V2.8 uploadé par Elma a été décodé** avec `scripts/decode_chronologie.py` du dépôt (produit par Claude Code entre-temps), complété localement d'une couleur absente de sa table : le **rose `255,240,91,155` = domaine (vii) Altcoins** — c'est l'« altcoin addition » de la V2.8, invisible depuis la V2.5 du dépôt. 146 événements extraits, 144 avec domaine par couleur ; les 2 restants sont les jalons à fond blanc/liseré rouge (Genesis → vi, Lancement d'Ethereum → vii, domaine posé par le texte). Répartition : i 28 · ii 10 · iii 12 · iv 16 · v 16 · vi 13 · **vii 27** · viii 22.
→ **À reporter au dépôt** : une ligne à ajouter dans `COULEURS` de `decode_chronologie.py` (patch trivial pour Claude Code).

**2. Croisement figure × catalogue** en assignation globale (plus de capture par ordre de parcours) : 54 lignes appariées → astérisques levés, domaines complétés, **1 CHANTIER de date résolu** (Tether : 06/10/2014, fig.). **Règle maintenue : un domaine sourcé texte n'est jamais écrasé par la figure** — conflit noté `[CHANTIER domaine : texte X / figure Y]` (cas E004, client Bitcoin-Qt : texte iii l.269 / figure iv). 4 doublons F→E fusionnés à la main (Litecoin, PCWorld, WeUseCoins, SatoshiDice — les deux derniers datés par la figure, « date texte non donnée »). Bitcoin Magazine : **deux actes distincts** conservés (création/rapprochement 2011, l.391 ; première parution 01/05/2012, fig.).

**3. 88 lignes figure ajoutées** (`origine=figure`, F001–F088) : BTC-E, LocalBitcoin, Ripple, premier ASIC Avalon, Colored Coins, premiers services de conformité, les HF d'Ethereum (Byzantium, Constantinople), la migration de Tether vers Ethereum… **Convention détectée : les dates « au 01 » de la frise sont des précisions mois** encodées en jour (ex. rapport BCE au 01/10/2012 pour « octobre 2012 ») → 23 lignes passées `precision=mois` avec note.

**4. Chap. II, Encadré n°4 (l.399–407) intégré** — le « §II.3.3 » du renvoi de chap. III est en réalité cet encadré de II.3.3 « Caractériser la gouvernance… » : E079 première proposition d'augmentation de la limite (2013) · E080 lancement Bitcoin XT, Andresen & Hearn, 8 Mo (août 2015) · E081 abandon de XT (janvier 2016, type `[CHANTIER]` — retrait/échec, même trou typologique que E019) · E082 Unlimited et Classic « connaîtront le même sort » (date indicative). Recensement seul, analyse → E&I 2017. **MtGox (faillite) et Tether n'ont pas de localisation texte en ch.II** non plus : MtGox reste sourcée figure seule ; Tether n.62 l.583 (émission via Omni) sans date — date désormais fixée par la figure.

**5. Corrections validées appliquées** (vérif. externe du 02/08) : Litecoin **07/10/2011** (note : fig. 13/10 = réseau actif) · Frontier **30/07/2015** (texte l.399 à corriger) · Bitcointalk **22/11/2009** (le « janvier 2009 » de l.113 vise prob. le canal SourceForge, fig. 10/12/2008) · NewLibertyStandard **dédoublé** (F001 premier taux 05/10 ; E007 première transaction 12/10).

## Le livrable
`catalogue-evenements-v3.csv` — **345 lignes** : 82 calibrage (50 + 32 enrichies graphe) · 175 graphe · 88 figure. 22 seuils, 58 crises (39 numérotées). `chrono-v28-decodee.csv` = la frise décodée, jointe comme pièce de référence.

## Reste ouvert — [CHANTIER], rien de tranché
1. **Codage analytique : 251 lignes** sans `acteur_principal` (et arène/type d'acte à l'avenant). Prochaine séance : par lots de ~40, en commençant par crises numérotées puis domaine (ii).
2. **Q7** — vocabulaire des effets, toujours provisoire (25 lignes codées seulement).
3. **11 notes [CHANTIER]** dans le CSV, dont E004 (conflit domaine texte/figure), E082 (date indicative), BitLaundry (ni 09 ni 12/2010 confirmés).
4. **13 paires A_VERIFIER** du dédoublonnage graphe (inchangées) + doublons G↔F possibles à examiner (le graphe et la figure décrivent parfois le même fait sous des libellés éloignés — non fusionnés par prudence).
5. **80 lignes sans domaine** : presque toutes `origine=graphe` hors frise (crises du wiki, événements chap. III) — domaine à coder à la main, la figure ne peut pas aider.
6. Chronologies **Altcoin V0.1** et **HF d'Ethereum V1** présentes dans le dépôt (`docs/research/chronologies/`), non décodées ici : gisement pour une v4 si tu veux la profondeur Ethereum/altcoins.

## Passation dépôt (Claude Code)
(a) ajouter la couleur vii au décodeur ; (b) archiver le `.bin` V2.8 dans `docs/research/chronologies/` (le dépôt n'a que la V2.5) ; (c) verser `catalogue-evenements-v3.csv` + `chrono-v28-decodee.csv` dans `docs/research/catalogue-evenements/` ; (d) le `patch_11` (v98) reste compatible — aucune des 6 entités qu'il ajoute n'entre en collision avec les F.
