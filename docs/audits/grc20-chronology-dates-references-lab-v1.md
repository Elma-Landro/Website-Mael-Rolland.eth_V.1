# GRC-20 Chronology, Dates & References Verification Lab v1

**Date** : 2026-08-09
**Graphe audité** : `grc20-these-mael-rolland-v111.json` (2 293 entités, 20 207 relations)
**Branche** : `claude/file-upload-branch-check-jw4cng`
**Mode agent** : audit documentaire — **aucun graphe modifié, aucune v112, aucun patch appliqué, aucune fusion, aucun retypage, aucun runtime touché**
**Mécanisme rejouable** : `scripts/audit_chronology_dates.py` (`--csv`, `--check`)

**Données probantes** (à lire *avec* cet audit, jamais seules) :

| Fichier | Produit par |
|---|---|
| `data/chronology-date-inventory-v111.csv` | inventaire mécanique des 948 valeurs datées |
| `data/chronology-thesis-crosscheck-v111.csv` | recoupement de 260 dates avec le texte de la thèse |
| `data/chronology-external-verification-v111.csv` | vérification externe ciblée de 40 dates |
| `data/chronology-event-identity-debt-v111.csv` | 50 paires événementielles instruites |
| `data/chronology-reference-support-v111.csv` | adossement probatoire, 608 lignes |

> Rappel de la charte (`agents/README.md`) : **un agent est un rôle de travail, pas une autorité scientifique.** Rien n'est tranché ici. Les questions posées au § 8 attendent l'arbitrage de Maël Rolland.

---

## 1. Ce que ce chantier a cherché, et ce qu'il n'a pas cherché

Il a cherché à répondre à trois questions distinctes, souvent confondues :

1. **Combien de dates, sous quelles formes ?** — inventaire mécanique.
2. **D'où viennent-elles ?** — adossement probatoire. *Une date sourcée n'est pas une date juste.*
3. **Sont-elles justes ?** — recoupement avec la thèse, puis vérification externe.

Il n'a **pas** cherché à réparer. Aucun patch candidat n'est émis, et le § 7 explique pourquoi c'eût été prématuré.

---

## 2. L'inventaire — et deux corrections de cadrage

**948 couples (entité × clé datée) sur 729 entités distinctes**, 24 clés. Recompté indépendamment du script avant versement.

Deux clés du périmètre **ne portent pas de date**, et le dire change la lecture de tout le reste :

- `dateSource` (95) porte une **référence bibliographique** (« Sedgwick 2018e », « Banque de France 2013, p. 4 ») ;
- `dateAuthority` (49) porte un **niveau de preuve** (`TIMELINE_FIGURE`, `AUTHOR_VERIFIED`, `EXTERNAL_VERIFICATION`).

Elles pèsent **144 des 158** valeurs non normalisables. Le taux réel de valeurs illisibles est donc **1,5 % (14/948)**, non 17 %. Elles sont conservées dans le CSV avec une note qui nomme leur nature, plutôt que retirées en silence : un inventaire qui ne correspond plus à son périmètre déclaré n'est plus une preuve.

`page_start` est **exclue explicitement** (constante nommée, pas omission) : c'est la page imprimée d'une section, pas une date. Une regex naïve sur « start » la ramasse et fabrique 37 fausses anomalies.

**Aucune date future. Aucune année hors plage** (min 1892, max 2024). **Aucun conflit intra-entité** sur les 26 couples `year`+`date` — résultat vérifié, non code mort : un graphe synthétique altéré fait bien remonter la détection.

Signalements : 30 valeurs `NN/NN/AAAA` indécidables · 652 lignes où une même clé est déclarée tantôt `TEXT` tantôt `TIME` (cinq clés : `year`, `date`, `launchYear`, `dateStart`, `dateEnd`) · 17 descriptions citant une année différente de la date portée.

---

## 3. La découverte principale : `date` mélange deux conventions de format

C'est le résultat le plus conséquent du chantier, et il est **démontré, non soupçonné**. Trois fiches consécutives, **issues de la même figure** (« Chronologie n° 4 », chapitre III), crises n° 24, 25 et 26 :

| Fiche | Valeur brute | Lecture vraie | Convention |
|---|---|---|---|
| BIP-42 — inflation bug (`3952cb54`) | `01/04/2014` | 1er avril 2014 — c'est un poisson d'avril de Pieter Wuille | **JJ/MM** |
| CVE-2014-0160 Heartbleed (`ca278d21`) | `04/07/2014` | 7 avril 2014 | **MM/JJ** |
| BIP-66 — chain split (`d1961d60`) | `04/07/2015` | 4 juillet 2015 | **JJ/MM** |

Preuve pour les deux dernières : les alertes versionnées de `bitcoin-dot-org/Bitcoin.org` portent `date: 2014-04-11` pour la réponse à Heartbleed — une réponse ne peut pas précéder de trois mois un événement du 4 juillet — et `2015-07-04` pour BIP-66.

**Deux chaînes identiques à l'année près se lisent en sens opposés.** Conséquences directes :

- les **54** valeurs `NN/NN/AAAA` ne sont pas normalisables par une convention unique ;
- le refus de l'inventaire de deviner un ordre jour/mois n'était pas de la pusillanimité : appliquer « dépôt français donc JJ/MM » aurait gravé au moins une date fausse ;
- **toute normalisation de format est désormais un arbitrage fiche par fiche**, pas une passe mécanique.

---

## 4. L'adossement : 36 % des dates événementielles ne reposent sur rien

Sur 239 dates événementielles : **81 `adosse_fort` (34 %) · 72 `adosse_faible` (30 %) · 86 `non_adosse` (36 %)**.

**Aucune `dateSource` du graphe ne contient d'URL** — 0 sur 95.

Le « fort » est plus fragile qu'il n'y paraît, et trois réserves le disent :

- les 28 renvois « Thèse — Chronologie (figure) Chapitre I.2 » et les 9 « Chronologie 2 (p.88) » pointent vers des **images absentes du dépôt** : `assets/MD/media/` n'existe pas, et aucun libellé « Chronologie 2 » ne figure dans le Markdown. Le pointeur résout ; la source ne se lit pas ;
- les 11 `AUTHOR_VERIFIED` citent une « Chronologie des HF d'Ethereum V1 » qui, **de son propre libellé**, n'est ni publiée, ni mobilisée dans la thèse, ni versée au dépôt : non consultable par un tiers ;
- l'adossement est déclaré sur la foi du pointeur, non sur lecture de la source.

**Correction d'une affirmation héritée de v97.** « `dateAuthority` est utilisé par 37 entités, toutes `TIMELINE_FIGURE` » était vrai en v97 et est **faux en v111** : 37 `TIMELINE_FIGURE`, 11 `AUTHOR_VERIFIED`, 1 `EXTERNAL_VERIFICATION`. Le nombre 37 survit exactement, mais comme *sous-ensemble* — ce qui rend l'ancienne formule trompeuse plutôt que simplement périmée. Un audit qui la reprendrait conclurait que le graphe n'a qu'un régime de preuve.

Côté bibliographie, les 369 `Reference` datées confrontées à `07_bibliographie.md` donnent **351 accords (95,1 %)**, 13 non-résolutions, 4 résolutions ambiguës, 1 désaccord d'année. Une non-résolution **n'est pas une erreur** : elle ne dit pas si l'entrée manque au Markdown (conversion incomplète du PDF) ou si la fiche est mal formée.

---

## 5. Le recoupement avec la thèse : la thèse se contredit plus souvent que le graphe

260 entités confrontées au texte, **222 citations verbatim** extraites programmatiquement puis revérifiées à la ligne indiquée.

**51 lignes (19,6 %) ne reposent que sur une figure de chronologie** — ni confirmation ni réfutation. Nuance qui compte : l'étiquette `TIMELINE_FIGURE` n'est pas synonyme de « invérifiable ». Sur les 37 fiches qui la portent, **19 sont en réalité reprises par le texte courant**.

Sur les 5 cas où le désaccord penche contre la thèse, **trois sont des contradictions internes à la thèse** :

| Objet | Le texte dit | Ailleurs dans le même texte | Le graphe |
|---|---|---|---|
| Frontier | 20 juillet 2015 (ch. I l.399, l.443) | 30 juillet 2015 (ch. III l.529 ; annexes l.337, l.569) | 30/07 — suit la majorité |
| Bitcoin-QT 0.1 | 9 janvier 2009 (ch. I l.269, l.305) | février 2009 (ch. III l.61) | 2009-01-09 |
| Bitcointalk | « janvier 2009 » (ch. I l.113) | note 12 (l.483) : remplace un forum « lancé en mai 2009 » — janvier devient impossible | 2009-11-22, cohérent avec la note |

**Aucun fichier de `assets/MD/` n'a été modifié.** Une erreur repérée dans la thèse est signalée, jamais corrigée : ce sont des documents archivistiques.

---

## 6. Les doublons ont une cause, et elle est mécanique

259 entités du périmètre événementiel, 881 paires candidates, **50 instruites en 31 familles** : 23 `doublon_probable`, 13 `indetermine`, 9 `homonymie_non_doublon`, 5 `two_distinct_events_possible`.

**La cause structurelle** : **8 des 9 fiches portant `dateSource = "Thèse — Chronologie 2 (p.88)"` ont une jumelle** parmi les 28 fiches « Chronologie (figure) Chapitre I.2 ». **Deux figures de chronologie ont été ingérées séparément.** Les doublons ne sont pas dispersés — ils ont une origine unique, ce qui rend leur traitement instruisible en lot plutôt qu'au cas par cas.

Preuves les plus fortes : attribut `description` **strictement identique** (Mining pools ×3, halving, Chypre, BitPay).

**Aucune chaîne de `duplicateOf` en v111** : l'invariant posé après l'incident C4 tient. Le **piège C5 est en revanche confirmé** — la canonique `15864ab2` (degré 4) est moins reliée que la fiche `ee727747` (degré 7) qu'elle canonise. Le CSV reporte les degrés et **ne désigne aucune canonique**.

Depuis v105, **3 fiches seulement sur 259** portent `duplicateOf` + `reviewStatus = duplicate-pending-merge`, et **aucune fusion n'a eu lieu**. La dette déclarée par le graphe est très inférieure à la dette mesurée.

### Deux actes distincts, jamais forcés en contradiction

Sept cas au total sont classés `two_distinct_events_possible` (5 côté identité, 3 côté vérification externe, 2 côté thèse — recoupements inclus). Le prototype reste **NewLibertyStandard**, et la thèse elle-même l'établit : la note 75 (ch. I l.609) date du **12 octobre 2009** le premier échange contre monnaie nationale (Malmi, 5 050 BTC pour 5,02 $), la note 78 (l.615) date de **février 2010** la modélisation du prix. Le graphe porte `2009-10-05` (publication du taux) et `2010-02` (modèle de prix) : **la date du 12 octobre n'est portée par aucune fiche**, et la fiche `66a59145` s'intitule « Premier échange BTC/$ » tout en portant la date d'une publication de taux.

Les autres : Frontier Thawing (annonce 04/08/2015 vs activation au bloc 200 000, 07/09/2015), BIP-148 (rédaction 12/03/2017 vs activation 01/08/2017), Ethereum Classic (dépôt GitHub 10/07/2016 vs fork 20/07/2016), soft fork du 28/07/2010 vs CVE-2010-5139 du 15/08/2010, WikiLeaks (annonce déc. 2010 vs adoption), Bitcoin-Qt.

---

## 7. Pourquoi ce chantier n'émet aucun patch candidat

Trois raisons, dans l'ordre de force :

1. **Le § 3 vient de disqualifier la passe mécanique.** Un patch de normalisation des 54 `NN/NN/AAAA` aurait été le livrable naturel de ce chantier. Il aurait encodé une convention que la preuve dément. Émettre un patch aujourd'hui reviendrait à graver un arbitrage que personne n'a pris.
2. **Presque chaque correction est intriquée à une décision d'identité.** Corriger l'année de `0d81bba0` (BitcoinTalk) sans décider de la fusion avec `06ac37fc` produit deux fiches justes et redondantes. Corriger l'année de `adc1a4d0` (Selgin) en 2014 produit un **doublon exact** de `3d76ab7f` — même titre, même année. Le « il n'y a qu'à corriger la date » est faux dans les deux cas.
3. **La charte réserve à l'auteur** les fusions, créations, retypages et tout ce qui engrave une affirmation sur une personne.

Ce que le chantier livre à la place : cinq relevés, un mécanisme rejouable, et des questions posées au point où seule une décision reste.

---

## 8. Points ouverts — à ne pas trancher

Reportés intégralement pour que ce document se suffise à lui-même. Les questions marquées **★** ont été posées directement à Maël dans le fil de discussion.

### Format et convention

1. **★ Les 54 valeurs `NN/NN/AAAA`** : convention à fixer fiche par fiche (§ 3). Aucune passe globale n'est légitime.
2. **Les 5 clés à double type GRC-20** (`year`, `date`, `launchYear`, `dateStart`, `dateEnd`, déclarées tantôt `TEXT` tantôt `TIME`, 652 lignes) : harmoniser ou documenter l'hétérogénéité ?
3. **Les 14 valeurs en texte libre délibéré** (« fin 2013 — pression FinCEN », « 2017 surtout », « nov. 2013 – présent ») : bornage ou conservation comme expression ?

### Identité et doublons

4. **★ La cohorte des deux chronologies** (8 paires jumelles, § 6) : traitement en lot ou fiche par fiche ?
5. **★ BitcoinTalk** (`0d81bba0` 2010-11-22 / `06ac37fc` 2009-11-22) : coquille d'année **et** doublon. Réfuté en externe par l'archive Nakamoto (« Date: November 22, 2009 », fil « Welcome to the new Bitcoin forum! »), et la fiche se contredit elle-même — sa propre description dit « novembre 2009 ».
6. **★ Les 4 fiches Selgin** : `adc1a4d0` (« Synthetic Commodity Money », 2013, degré 13) duplique `3d76ab7f` (même titre, 2014, degré 6), tandis que `5680ab9e` porte le vrai 2013 (« Quasi-Commodity Money »). La fiche la mieux reliée porte l'année fausse — piège C5 à nouveau. Détail : George Selgin est relié à `adc1a4d0` par `created` et aux trois autres par `authored`.
7. **Les 3 fiches `duplicate-pending-merge`** depuis v105, dont le couple Mining pools déjà consigné comme conflit de types dans `identity-debt-fr-en-v1.csv` : fusionner, et vers quelle fiche, la canonique désignée étant la moins reliée ?
8. **Les 23 `doublon_probable` et 13 `indetermine`** du relevé d'identité.
9. **★ Les 7 `two_distinct_events_possible`** : dédoubler, renommer, ou laisser.
10. **Les doubles modélisations sous deux types** (Genesis Block, Op_Return War, Silk Road en `InfrastructureEvent` **et** `CrisisEvent`) : couche voulue ? **Retypage réservé à l'auteur.**

### Contenu et véracité

11. **★ `120e6fa2`** — la fiche s'intitule « Perte 9000 BTC (premier utilisateur, 10 août 2010) », porte `date = 2010-08-10`, et son attribut `description` concorde. Mais **son enveloppe `description`, seule version affichée par le site**, décrit un autre fait : « Allinvain annonce le vol de 25 000 BTC depuis son portefeuille en juin 2011 ». Deux événements réels et distincts collés sur une fiche, la version visible étant la mauvaise. La thèse (note 73, l.605) attribue en outre ce vol à un mineur, le graphe à MtGox.
12. **★ Les 237 doubles descriptions** (§ 9).
13. **Pizzas** : graphe `2010-05-21`, thèse (l.609) « Le 22 mai 2010 ».
14. **Phase de maturation** : graphe `2013-01-01 → 2015-12-31`, thèse (l.285) « de novembre de 2013 à aujourd'hui ». Le graphe se contredit : son `Concept` jumeau porte « nov. 2013 – présent ».
15. **CVE-2018-17144** : `2018-09-01` est exact au mois et factice au jour. Signalement 17/09, correctif 18/09, divulgation 20/09 (4 sources primaires). En outre la `CrisisPhase` `order=0` finit le 20/09 alors que la phase `order=1` finit le 18/09 — incohérence d'ordonnancement.
16. **Istanbul** : graphe `2019-12-08`, `ethereum/execution-specs` `2019-12-07`. Les 9 autres hard forks concordent exactement.
17. **BitLaundry** : trois valeurs incompatibles — graphe `2010-09-01`, thèse « fin 2010 », description « lancé en 2011 ». Aucune source externe atteignable.
18. **Split de chaîne** : ch. I l.267 dit « 15 mars 2011 », ch. III l.237 et la note 104 disent mars 2013. Le jour du graphe (15/03) n'est pas attesté non plus.
19. **Casascius** : la thèse l'attribue à Bobby Lee (l.359), le graphe à Mike Caldwell ; graphies divergentes (« Casacius », « Cascascius », « Casascius »). **Toute écriture ici engrave une affirmation sur une personne réelle** — décision d'auteur, sans exception.
20. **Audition Commission des Finances** : le nom porte « (2015) », l'attribut `date` porte `07/11/2014`.
21. **`adc1a4d0` Selgin** : année 2013 contre entrée bibliographique 2014b, mais voir le point 6 — ce n'est pas une année à corriger.

### Adossement

22. **★ Les 86 dates événementielles `non_adosse`** : exiger un `dateSource` avant publication, ou accepter cette strate de contexte non adossée ?
23. **Les 37 renvois vers des figures-images** : verser les figures, ou pointer les pages du PDF ?
24. **Les 11 hard forks `AUTHOR_VERIFIED`** : verser la chronologie citée, ou lui substituer une source publiée ?
25. **`94ce188e` Litecoin** : la date `2011-10-07` est corroborée jusque dans le bloc de genèse (`CreateGenesisBlock(1317972665, …)` = 2011-10-07T07:31:05Z), mais son `dateSource` — « Vérification externe 02/08/2026 » — n'est ni une URL, ni un auteur, ni un support.
26. **Les 4 `resolution_ambigue` et 13 non-résolutions bibliographiques** : doter les fiches d'un `title` ?
27. **Coquilles de libellé** : le graphe écrit `Whitebbit1111` là où le Markdown écrit `WHITERABBIT1111` ; le Markdown écrit `KINDELBERGER` là où le graphe écrit `KINDLEBERGER`. Archives intouchées ou corrigées ?
28. **Écart bibliographique** : `07_bibliographie.md` annonce « Total : 652 entrées » et en porte 664.

---

## 9. Découverte annexe : 237 doubles descriptions, aucune identique

Hors périmètre initial, trouvée en vérifiant un signalement de l'inventaire, et versée ici parce qu'elle conditionne la lecture de toute date.

**237 entités portent à la fois l'enveloppe GRC-20 `description` et un attribut homonyme `attributes.description`. Aucune des 237 paires n'est identique.** 171 ont une similarité < 0,35 ; 12 citent des années disjointes.

Le registre documente déjà la **collision de clé** (entrée `description`, `status: structural`, note explicite). Il ne documente pas la **divergence de contenu** — c'est la mesure neuve.

Qui lit quoi, vérifié dans le code :

| Consommateur | Lit |
|---|---|
| `lecteur.html:2575` | enveloppe |
| `graph-worker.mjs:271` (recherche) | enveloppe |
| `graphe.html:5021,5040` | enveloppe |
| `grc20-publish.mjs:172-185` puis boucle d'attributs | **les deux** |

`grc20-publish.mjs` émet l'enveloppe via `SYSTEM_PROPERTY_IDS.description`, **puis** parcourt `entity.attributes` **sans liste d'exclusion** : il émettrait un second triplet `description`. Autrement dit, **237 secondes descriptions sont invisibles sur le site et seraient gravées on-chain**.

Le cas `120e6fa2` (§ 8, point 11) montre que ce n'est pas qu'une redondance : les deux versions peuvent décrire deux faits différents, et la version visible peut être la fausse.

**Aucune action prise.** Le runtime n'a pas été touché ; la publication n'est pas de mon ressort.

---

## 10. Limites de ce chantier — à lire avant de s'appuyer dessus

- **Le réseau restreint la vérification externe.** Seuls `github.com`, `raw.githubusercontent.com` et `gitlab.com` sont joignables. NVD, `bitcoincore.org`, `en.bitcoin.it`, `blog.ethereum.org`, Wikipédia, CoinDesk et l'Internet Archive sont bloqués. D'où 24 `indice_unique` pour 4 `confirme` : c'est une contrainte d'accès, pas un défaut de recoupement.
- **La date de l'attaque The DAO reste `non_verifie`** — la plus célèbre de la thèse. Elle est connue de mémoire ; une date de mémoire ne s'inscrit pas. C'est la règle qui a fonctionné, pas une lacune à combler par complaisance.
- **Un piège de source documenté** : `ethereum-org-website/.../ethereum-forks/index.md` ne contient **aucune date** (seulement des balises `<NetworkUpgradeSummary />`). Une première lecture en a rendu un tableau de dates plausible et faux, détecté en redemandant le verbatim. **Ce fichier ne doit pas être cité comme source de dates.**
- **L'adossement n'est pas la véracité.** Le volet probatoire mesure d'où vient une date, jamais si elle est juste.
- **Les figures de chronologie n'ont pas été lues.** Elles sont des images absentes du dépôt ; les 51 lignes qui en dépendent restent indécidées, et ce n'est pas un défaut du graphe.
- **Les non-résolutions bibliographiques ne sont pas des erreurs.** Par construction, elles ne disent pas si l'entrée manque au Markdown ou si la fiche est mal formée.
