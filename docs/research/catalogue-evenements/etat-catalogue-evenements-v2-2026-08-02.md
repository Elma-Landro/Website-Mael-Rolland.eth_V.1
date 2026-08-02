# État de chantier — Catalogue d'événements v2 (fusion graphe GRC20 × calibrage) — 02/08/2026

## Source intégrée
Dépôt `Elma-Landro/Website-Mael-Rolland.eth_V.1`, branche par défaut `codex/create-expand-from-node-planning-documents` (HEAD, commit b4b0c8b du 28/06/2026). Fichier exploité : `grc20-these-mael-rolland-v97.json` (10 Mo — 2 263 entités, 20 042 relations, 55 types).

## Décision actée cette session
Les 8 domaines de référence sont **ceux de la thèse** (chap. I l.251, verbatim) et non ceux du graphe :
(i) sphère d'usage réelle et financière — vert · (ii) traitement des transactions — jaune · (iii) portefeuilles et paiements — orange · (iv) information et connaissance — bleu foncé · (v) conformité aux réglementations nationales — bleu clair · (vi) protocole Bitcoin — rouge · (vii) Altcoins — rose · (viii) autres — violet.
Correspondance appliquée depuis le graphe : « Sphère d'usage »→i · « Services de portefeuille et de paiement »→iii · « Information et connaissance »→iv · « Conformité réglementaire »→v · « Protocole et couche de base »→vi · « Altcoins, tokens et surcouches »→vii · « De la confidentialité et de l'anonymisation »→**iii** (le mixage relève du domaine (iii) selon l.251) · « [Résiduel — à reclasser] »→viii.
**Le graphe n'a aucun domaine correspondant à (ii) traitement des transactions** : les événements de minage arrivent donc sans domaine et sont à coder à la main.

## Livrables
1. `catalogue-evenements-v2-fusion.csv` — **253 lignes**, 27 colonnes, triées par date.
   - 78 issues du calibrage (`origine=catalogue`, dont 32 `catalogue+graphe` enrichies)
   - 175 issues du graphe (`origine=graphe`, id G001–G175)
   - 58 lignes `crise=oui`, dont 39 portant un `crisis_no` (recensement seul — analyse SASE)
   - colonnes ajoutées : `crisis_no`, `cve`, `source_graphe`, `acteurs_graphe`, `occurs_in`, `variantes`, `gid`
   - suffixe `~` sur `domaine_8` = attribution héritée du graphe (à contrôler) ; `*` = attribution par définition (calibrage)
2. `table-divergences-dates.csv` — 5 conflits texte/graphe, **non tranchés**.
3. `doublons-probables.csv` — 19 paires graphe↔calibrage, **non fusionnées**.
4. `fusion.py` — script rejouable.

## Traitements appliqués
- Normalisation des dates : 4 formats ramenés à l'ISO (`AAAA-MM-JJ`, `DD/MM/AAAA`, « 15 septembre », année seule) ; `precision` renseignée.
- Dédoublonnage interne au graphe : 213 → 207 (5 groupes fusionnés), avec garde-fou bloquant toute fusion entre entités portant des CVE, des n° de crise ou des acronymes distincts (a évité de fusionner CVE-2018-20586/20587 et CBOE/CME).
- Appariement calibrage↔graphe : 32/78, par similarité de Jaccard avec pénalité d'écart d'année ; les attributs du graphe (n° de crise, CVE, sections, acteurs) sont versés dans la ligne du calibrage.
- Résolution **Q10** : `crisisNumber` couvre 1→38 sans trou. C'est la numérotation de la thèse et la clé de jointure. Réserves : deux entités à `n°0`, un doublon sur `n°34`, 13 `CrisisEvent` sans numéro.

## [CHANTIER] — à arbitrer par Elma
1. **5 divergences de dates** (`table-divergences-dates.csv`) : Bitcointalk 01/2009 (l.113) vs 22/11/2009 · premier échange BTC/$ 12/10/2009 (n.75 l.609) vs 05/10 · BitLaundry 12/2010 (n.74 l.607) vs 09/2010 · Litecoin 10/2011 (l.359) vs 19/11/2011 · Frontier 20/07/2015 (l.399) vs 30/07/2015. Le graphe source plusieurs de ces dates sur « Thèse — Chronologie (figure) » : conflit texte/figure interne à la thèse.
2. **19 doublons probables** graphe↔calibrage (`doublons-probables.csv`). Deux faux positifs identifiés (G085 Namecoin↔E031 Litecoin ; G049 Bitcoin-Qt↔E073 futures) : à écarter. Les autres sont à confirmer un à un.
3. **18 lignes sans date** dans le graphe (G005, G012, G046-G053, G062, G160-G175…) — plusieurs semblent redoubler des lignes calibrées (Satoshi Dice, MyBitcoin, crise chypriote, Silk Road, Sénat US, NABC Miami, Frontier, ICO Ethereum).
4. **4 lignes hors périmètre 2008–2020** : G122 ICANN 1998, G127 RipplePay 2004 (préhistoire, exclue par Q4), G170 The Merge 2022, G113 « Figure 5 » 2024 (artefact de figure, pas un événement).
5. **Colonnes analytiques à coder : 175 lignes** pour `acteur_principal`, `arene`, `type_acte` ; 94 pour `domaine_8`. Le graphe fournit `acteurs_graphe` (36 `StakeholderCategory`, trois niveaux de granularité mêlés, doublons) et `occurs_in` (13 `GovernanceArena`, lieux nommés) : ces deux colonnes servent d'aide au codage, elles ne s'y substituent pas.
6. **Q7 toujours ouverte** : vocabulaire des effets sur les propriétés monétaires ; `effet_prop_monetaires=nd` sur les 175 lignes du graphe.
7. **Export SVG de la chronologie carnavalesque absent de cette branche** : seuls le PNG V2.8 et 4 SVG d'autres figures (mise en crise CVE 2018, PR, acteurs de gouvernance, deux procédures) sont présents. À pousser ou indiquer la branche.

## Prochaine étape proposée
(a) arbitrage des divergences (1) et des doublons (2-3) ; (b) codage analytique par lots de ~40 lignes, en commençant par les crises numérotées et le domaine (ii) minage absent du graphe ; (c) arbitrage Q7 ; (d) versement des 4 fichiers + `grille-codage-catalogue-v1.md` au projet.

## Anti-redondance (inchangé)
Crises = recensement pur (analyse → SASE) · Scaling = recensement (analyse → Économie et institutions 2017) · carnavalesque = Revue de la régulation · construction des figures = BMS. Le catalogue reste un instrument.
