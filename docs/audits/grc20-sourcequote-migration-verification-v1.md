# SourceQuote Migration Verification Lab v1 — 41 citations vérifiées contre la thèse, aucune gravée

**Date** : 2026-08-07 · **révisé le 2026-08-07 après revue hostile** (cf. § 0)
**Graphe** : `grc20-these-mael-rolland-v110.json` (**inchangé** par ce chantier, révision comprise)
**Branche** : `claude/file-upload-branch-check-jw4cng`
**Mode agent** : A (vérification probatoire — **aucune création, aucune application**, aucun fichier de patch modifié ni créé)
**Outils** : extraction des zips `Migration/` + vérification pypdf contre les PDF canoniques (`assets/pdf/4_Introduction_generale.pdf`, `5_Chapitre_1.pdf`, `6_Chapitre_2.pdf`, `7_Chapitre_3.pdf`, `8_Conclusion_Generale.pdf`, complétés ponctuellement par `1_Premières_pages.pdf` et `2_Tables_des_matieres.pdf`) ; repli MD (`assets/MD/`) non nécessité — utilisé une seule fois en recoupement (`06_resume.md`, § 5.4)
**Données** : `docs/audits/data/sourcequote-migration-verification-v1.csv` (41 lignes, 18 champs)
**Prédécesseurs** : `candidate-patch-preflight-lab-v1.md` § 9.2 (arbitrage Q8 : « vérifier d'abord »), `docs/audits/data/candidate-patch-inventory-v1.csv` (lignes 1-3), inventaire brut du sous-agent A (scratchpad, `sourcequote-inventory-raw.json`)

> Contrôle de recoupement : les chiffres de ce document ont été re-vérifiés
> par recomptage direct du CSV commité — 41 lignes de données, 18 champs
> partout ; 14 `exact-match` / 14 `minor-normalization` / 7 `wrong-section` /
> 6 `duplicate-existing` ; 0 `paraphrase-only`, 0 `not-found` (au sens : les
> 41 textes existent dans la thèse) ; **34 `needs_mael_arbitration=oui` /
> 7 `non`** ; recommandations 24 `retenir` / 5 `retenir-avec-correction-de-section` /
> 4 `completer-l-existante` / 8 `arbitrage` ; 169 références d'entités
> (**105 uniques / 53 fuzzy / 5 résolues par synonyme ou traduction /
> 6 réellement introuvables**) et 57 cibles de section
> (40 existantes / 11 renumérotées / 6 jamais existées). La calibration de
> page est exacte : chaque page des PDF porte son numéro imprimé « — NN — »
> dans la pagination de la thèse ; aucun décalage de bloc à estimer.

---

## 0. Révision du 2026-08-07 après revue hostile

La version initiale de ce dossier (commit `4e21547`) a été soumise à la
skill `grc20-reviewer-hostile`. Le **cœur probatoire a passé** : cinq
`exact-match` tirés au sort ont été re-vérifiés contre le PDF sans écart,
la couverture verbatim des 41 textes a été re-mesurée, les 6 doublons ont
été reconfirmés (aucun septième), et les décomptes du CSV ont été jugés
justes. La revue a en revanche rendu un **verdict bloquant sur ce que le
dossier tirait de ces constats**. Chacune de ses huit prises a été
re-vérifiée à la main avant révision ; voici leur sort.

| # | Prise de la revue | Statut après contre-vérification | Traitement dans cette version |
|---|---|---|---|
| P1 | Les 11 références d'entités dites « introuvables » ne le sont pas toutes | **Confirmée** — 5 ont un nœud v110 sous un autre libellé (synonyme ou traduction) ; 6 seulement sont réellement absentes | § 5.3 réécrit ; CSV : 5 lignes passées à `resolved-by-synonym` avec l'id trouvé ; Q6 reformulée (elle invitait à créer un doublon anglais d'un nœud central existant) |
| P2 | `scripts/apply-sourcequote-phases.mjs` « écrirait dès `--write` » | **Réfutée sur le point central** — aucune primitive d'écriture disque dans le script ni dans `scripts/sourcequote-migration/*.mjs` (seuls `readFileSync`/`readdirSync` sont importés) ; la conclusion de la PR #113 tient. **Mais ses trois observations de code sont exactes** | Nouvelle sous-section § 5.7 « L'outillage existant et ses pièges », qui corrige explicitement l'erreur de la revue et consigne les pièges vérifiés |
| P3 | Les `page_start` de v110 contredisent la conclusion du § 5.1 sur les recentrages | **Confirmée** — 16 nœuds de section sur 35 portent un `page_start` incohérent avec la page imprimée de leur titre | Nouvelle sous-section § 5.6 ; **nouvelle question Q8** ; § 5.1 et § 7-Q1 assortis d'un préalable |
| P4 | P3-6 rangé à tort parmi les supersets à inclusion stricte | **Confirmée** — inclusion stricte vérifiée pour P1-8, P3-0, P3-7, P3-11 seulement | § 4 et § 6 corrigés |
| P5 | Pour P3-2, l'existante v110 `47dfac14` est elle-même fautive | **Confirmée** — elle saute 2 146 caractères sans marque entre ses deux fragments et son texte est préfixé du titre de section « La phase de "péché" (d'avril 2012 à octobre 2013) » | § 4 et Q3 précisés : fusionner greffe du texte vérifié sur une citation déjà fautive |
| P6 | Une résolution `unique` vise une section, pas un concept | **Confirmée** — P2-0 → `38e637cc` (`ThesisSection`, `section_key` II.2) | § 5.3 et notes CSV de P2-0 |
| P7 | P2-6 n'est pas une coupe mais une insertion | **Confirmée** — le candidat ajoute « par » là où la thèse porte « médiatisées des dispositifs » (coquille d'auteur) | P2-6 passe `needs_mael_arbitration=oui` ; Q7 devient « 18 coupes non signalées **et une correction de coquille** » |
| P8 | 6 ops à coupe non signalée étaient à `needs_mael_arbitration=non` alors que Q7 laisse la politique des coupes ouverte | **Confirmée** | P1-2, P1-7, P1-12, P2-3, P2-8, P3-5 passent à `oui` en renvoyant à Q7 ; avec P2-6, l'arbitrage passe de 27/14 à **34 oui / 7 non** |

Aucune de ces prises n'atteint le cœur probatoire : **les 41 textes existent
toujours dans la thèse, les 6 doublons restent 6, et les décomptes de
`match_status` sont inchangés**. Ce qui change, c'est la fiabilité de ce que
le dossier propose d'en faire — d'où deux nouvelles sous-sections de mise en
garde et une question supplémentaire.

---

## 1. Le mandat

Le Candidate Patch Preflight Lab (§ 9.2, décision Q8) a arbitré le sort des
trois zips SourceQuote de `Migration/` : **« vérifier d'abord »** — les 41
citations seront vérifiées contre le PDF, sans aucune écriture dans le
graphe ; ni applicateur ni application avant ce contrôle. « Une fausse
citation gravée dans le graphe serait pire qu'un travail préparatoire laissé
en attente. »

Ce chantier exécute ce contrôle, et rien que lui. Chaque op a été vérifiée
par recherche normalisée (casse, accents, apostrophes typographiques,
guillemets, espaces insécables, tirets, points de suspension, césures
d'extraction) : d'abord la chaîne entière en « squash » alphanumérique, puis
par fenêtres glissantes de 6-10 mots, enfin par alignement flou autour de la
page annoncée. La page annoncée a été confrontée à la page imprimée réelle,
et la section annoncée aux frontières de sections relevées dans
`2_Tables_des_matieres.pdf` et dans les titres courants du texte.

## 2. Inventaire vérifié

- **4 zips** dans `Migration/` : `sourcequote_effective_patch_phase1.zip`
  (18 ops), `phase2.zip` (10 ops), `phase3.zip` (13 ops) — soit **41 ops**,
  conforme au décompte du préflight — et `sourcequote_migration_foundation.zip`
  qui ne contient **aucune op** : uniquement de la documentation d'intention
  (spec de normalisation, comportement d'applicateur, plan d'orchestration,
  prompt d'implémentation).
- **Dialecte** : hors des six dialectes du dépôt et hors contrat
  (`grc20-candidate-patch-contract-v1.md`). Op unique
  `ADD_SOURCEQUOTE_WITH_SECTION_LINKS`, champs `seed_id` / `quote_text` /
  `page_thesis` / `target_sections` / `quote_supports_entity_names`,
  résolution **par nom** (aucun id v110), `authoring_mode` : « Prepared by
  ChatGPT from thesis PDF and current repo structure ».
- **Cible déclarée** : `graph_target` « v96+ » (phases 1-2) et
  `grc20-these-mael-rolland-v96.json` (phase 3). Les zips ont donc été écrits
  **avant** les migrations de sections v100/v106 — c'est la racine des clés
  dangereuses du § 5.1.

## 3. Bilan de vérification

Fait central : **les 41 textes existent dans la thèse**. Aucun
`not-found`, aucune `paraphrase-only` : ChatGPT n'a pas inventé de citation.
En revanche, il coupe silencieusement (appels de note, parenthèses de
citation, membres de phrase — 18 ops portent au moins une coupe non
signalée par « [...] »), il **corrige une fois une coquille d'auteur** sans
le dire (P2-6, § 7-Q7), et il se trompe de section plus souvent que de
texte.

| match_status | Phase 1 | Phase 2 | Phase 3 | Total |
|---|---|---|---|---|
| `exact-match` (verbatim, normalisation triviale près) | 9 | 2 | 3 | **14** |
| `minor-normalization` (coupes/typo seulement, texte verbatim) | 6 | 4 | 4 | **14** |
| `wrong-section` (texte retrouvé, section annoncée fausse) | 2 | 4 | 1 | **7** |
| `duplicate-existing` (recouvre une SourceQuote v110) | 1 | 0 | 5 | **6** |
| **Total** | **18** | **10** | **13** | **41** |

Pages : 33/41 ops sont à la page imprimée exacte ; 7 sont décalées d'une
page (33↔34, 185↔186, 186↔187, 128↔129, 335↔336, 336↔337, 4↔5) ; 1 est
décalée de trois pages (p. 109 réelle pour p. 106 annoncée — toujours dans
la même section I.2.2.b, dont c'est la fin). Aucun cas « page non
calibrée » : la numérotation imprimée a permis de tout calibrer.

`needs_mael_arbitration` : **34 oui / 7 non** (27/14 dans la version
initiale ; la révision P7-P8 y a versé les 6 ops à coupe non signalée encore
classées `non` et P2-6, cf. § 0). Recommandations, inchangées : 24
`retenir`, 5 `retenir-avec-correction-de-section`, 4 `completer-l-existante`,
8 `arbitrage`. Les deux axes se croisent : **17 des 24 `retenir` portent
désormais `arbitrage=oui`** — non parce que leur texte ou leur section est
douteux, mais parce qu'ils dépendent d'une politique éditoriale non encore
tranchée (Q7). Les 7 ops restées à `non` (P1-0, P1-6, P1-10, P1-16, P2-1,
P2-7, P3-1) sont celles où le texte est verbatim, la section confirmée par la
page, et où aucune coupe ni aucune entité litigieuse n'intervient.

## 4. Les 6 doublons v110 — nature exacte de chaque équivalence

Les six appariements `duplicate_risk=eleve` d'A sont tous **confirmés** ; la
PR #113 en soupçonnait 3, il y en a bien 6. Nature exacte :

| Op | Existante v110 | Équivalence vérifiée |
|---|---|---|
| P1-8 `sq_gap_intro_B3_02` | `a5278302…` « choix des deux crises » (p. 34) | L'existante est un **fragment strict** du candidat (« le bogue CVE 2018 #17144 … "The DAO" ») ; le candidat ajoute l'amont et l'aval, tous verbatim p. 33. |
| P3-0 `sq_phase3_I2_01` | `8f150b5d…` « dévoilant l'invisible carnavalesque » (p. 89) | Existante = 1re phrase **verbatim strict** ; candidat = superset (ajoute la 2e phrase, verbatim). |
| P3-2 `sq_phase3_I2_03` | `47dfac14…` « WikiLeaks accepte le BTC — p.93 » | **Chevauchement sans inclusion** : tronc commun verbatim (« Avec WikiLeaks … l'en priver »), puis l'existante poursuit sur les marchés noirs, le candidat sur le régime transactionnel. Seul cas où aucun des deux ne contient l'autre. **L'existante est elle-même fautive** (cf. encadré ci-dessous). |
| P3-6 `sq_phase3_I3_01` | `68d8c0d5…` « Buterin : peur que les règles changent » (p. 123) | L'existante porte le passage central (citation Buterin) **légèrement condensé par elle-même** (« protocole » pour « protocole de base », « l'équipe » pour « l'équipe de développement ») ; le candidat est plus long et plus fidèle au PDF, **mais l'existante n'en est pas une sous-chaîne** — sa condensation propre l'en exclut. Ce n'est donc **pas** un superset au sens strict. |
| P3-7 `sq_phase3_I3_02` | `6b1a40ec…` « dépendances au sentier (Russo 2020) » (p. 125) | Existante = 1re phrase verbatim strict ; candidat = superset (mais vise en plus une section jamais existée, I.3.2b). |
| P3-11 `sq_phase3_CONCL_02` | `fb610652…` « gouvernance conflictuelle et polycentrique » (p. 336) | Existante = 1re phrase verbatim strict ; candidat = superset qui saute sans marque une phrase intermédiaire (« Les infrastructures … idéologiques. ») et « (pour l'heure) ». |

Dans 5 cas sur 6 le candidat est **plus long et vérifié verbatim** ; mais
l'**inclusion stricte** de l'existante dans le candidat n'est vérifiée que
dans **4 cas** — P1-8, P3-0, P3-7, P3-11 (mesurée par comparaison
alphanumérique normalisée). P3-6 en est exclu par la condensation propre à
l'existante, P3-2 par la divergence. La question n'est donc pas « doublon ou
pas » mais « compléter l'existante, la remplacer, ou s'en tenir à la version
courte » — c'est un jugement d'auteur (§ 7, Q3), et pour P3-6 et P3-2 aucune
fusion mécanique n'est possible sans réécriture.

> **P3-2 : l'existante v110 est elle-même un montage silencieux.** Vérifié
> contre `5_Chapitre_1.pdf` p. 93 : le `quoteText` de `47dfac14…` (582
> caractères) juxtapose deux fragments séparés dans le texte imprimé par
> **2 146 caractères** — de « Sorti de son isolement relatif… » à « …des
> traders, des investisseurs et des entrepreneurs. » — **sans aucune marque
> de coupe**. Il est en outre **préfixé du titre de section** « La phase de
> "péché" (d'avril 2012 à octobre 2013) », qui est un intertitre du PDF et
> non une phrase de la citation. Le candidat, lui, est contigu p. 93.
> Conséquence pour Q3 : « fusionner » ne consoliderait pas deux citations
> saines — cela **grefferait du texte vérifié sur une citation déjà
> fautive**, et propagerait l'erreur au lieu de la corriger. La réparation
> de `47dfac14…` est un chantier distinct de la migration.

## 5. Les cas dangereux

### 5.1 Les 3 clés silencieusement fausses (II.3.1, II.3.2, III.2.2) — verdict par le texte

Les zips (écrits sur base v96) emploient trois clés qui existent **encore**
en v110 mais y désignent d'**autres** sections depuis v106. La carte de
renumérotation (II.3.1→II.3.1.a, II.3.2→II.3.1.b, III.2.2→III.1.2.b) devait
les sauver. Le verdict, page par page, est plus retors :

- **III.2.2 (P1-16, P1-17, pp. 243-244)** : la carte a **raison**. Les deux
  citations sont verbatim aux pages 243-244, dans « Enjeux des crises
  Bitcoin : labélisations indigènes » = III.1.2.b (titre p. 243, TOC à
  l'appui). Application mécanique de la carte : correcte.
- **II.3.1 (P1-14, P1-15)** : la carte a **tort deux fois, différemment**.
  P1-14 (p. 186) est le **chapeau** de II.3.1 « D'un concept de gouvernance
  problématique… » — c'est-à-dire la clé v110 `II.3.1` elle-même
  (`d493c4ac…`), la clé « dangereuse » qui se trouve être la bonne ; le
  sous-titre II.3.1.a ne commence qu'en p. 187. P1-15 (p. 190, « Retourné
  positivement… ») est dans **II.3.1.b** « Retournement positif du concept »
  (188-190), pas dans II.3.1.a.
- **II.3.2 (P2-4, P2-5, pp. 191 et 196)** : la carte a **tort deux fois,
  identiquement**. Les deux passages sont dans **II.3.2 v110** « Quand les CM
  réactivent un débat monétaire ancien » (titre en p. 190 ; le sous-titre
  « Pour les coiners… » de la p. 196 lui appartient), pas dans II.3.1.b. Là
  encore, la clé brute du patch — réputée dangereuse — pointait juste ; le
  patch avait seulement collé le mauvais **nom** de section sur la bonne clé.

Bilan : sur les 6 ops touchant ces clés, la renumérotation mécanique en
aurait **mal rangé 4** ; et pour 3 de ces 4, la clé « dangereuse » naïve
était correcte. Ni la clé brute ni la carte ne peut être appliquée en
aveugle : **seul le texte tranche**, op par op — c'est exactement ce que ce
chantier a fait, et ce que devra reprendre tout applicateur.

> **Réserve ajoutée en révision (cf. § 5.6).** Cette conclusion tient **par
> le texte imprimé** : la revue hostile a refait indépendamment le relevé des
> titres et confirme les positions intra-page. Mais les attributs
> `page_start` portés par les nœuds de section de v110 **disent le
> contraire** : `II.3.2` y porte `page_start=202` (son titre est p. 190) et
> `III.1.2.b` y porte `265` (son titre est p. 243). Un applicateur qui se
> fierait à ces attributs plutôt qu'au PDF conclurait donc l'inverse de ce
> § 5.1 — et graver P2-4/P2-5 dans `II.3.2` installerait une citation p. 191
> dans une section dont le graphe affirme qu'elle commence p. 202. **La
> réparation des `page_start` est un préalable à toute gravure** (Q8).

À ces 4 misroutes s'ajoutent **3 autres `wrong-section`** hors clés
dangereuses : P2-9 (p. 328 = III.3.4 « Fork You ?! », pas III.3.3 annoncée),
P2-0 (le passage annonçant II.2 est dans l'**introduction du chapitre II**,
p. 146, pas dans II.2 elle-même, ~160-184) et P3-10 (§ 5.4).

### 5.2 Les 6 sections jamais existées

`I.2.1b`, `I.2.1c`, `I.2.2a`, `I.3.2b`, `I.3.3a`, `I.3.3c` : clés de
niveau 3 (### de la thèse) présentes dans **aucune** version du graphe.
6 ops de la phase 3 les visent (P3-2, 3, 4, 7, 8, 9). Les textes de ces 6
ops sont pourtant tous vérifiés (4 verbatim/quasi verbatim, 2 étant en outre
des doublons partiels) et leurs pages tombent dans les parents existants
I.2.1 (89-99), I.2.2 (100-108), I.3.2 (123-127), I.3.3 (128-139). Rabattre
sur le parent est possible mécaniquement, mais créer ou non le niveau 3 est
une décision d'architecture du sommaire (§ 7, Q2).

### 5.3 Entités : 6 réellement absentes, 5 résolubles par synonyme, 53 fuzzy (sur 169 références)

> **Corrigé en révision (P1).** La version initiale annonçait « 11
> introuvables » et concluait que « "Polycentric Governance", concept central
> de la thèse, n'a pas de nœud propre en v110 ». **C'était faux, et c'est la
> prise la plus lourde de la revue.** Le résolveur employé ne testait ni le
> synonyme ni la traduction FR/EN : il produisait des faux négatifs.

Les `quote_supports_entity_names` résolvent à 105/169 en `unique`. Des 11
références classées `not-found` à l'inventaire, **5 ont en réalité un nœud
existant en v110 sous un autre libellé** — vérifié entité par entité :

| Nom du patch | Occurrences | Nœud v110 correspondant | Nature de l'écart |
|---|---|---|---|
| « Polycentric governance » / « Polycentric Governance » | **4** (P1-4, P2-2, P3-11, P3-12 — phases 1, 2 et 3, sous deux graphies) | `a444085b…` **« Gouvernance polycentrique »** (`CoreConcept`) | **Traduction** EN → FR. Voisin utile : `4a056174…` « Polycentricité comme dynamique d'arènes et de légitimités » (`Argument`) |
| « Controverse sur le statut monétaire » | **1** (P1-1) | `758e9ca9…` **« Controverse statut monétaire des cryptomonnaies »** (`Concept`) | **Synonyme** / reformulation. Ce nœud porte déjà une SourceQuote (`a1ee97b5…`) |

Le concept central de la thèse **a donc bien son nœud propre** ; c'est le
résolveur qui ne le voyait pas. Ces 5 références sont passées à
`entity_resolution_status = resolved-by-synonym` dans le CSV, avec l'id
trouvé en `resolved_entity_id`. **Aucune création n'est requise pour
elles** — et en créer une serait activement nuisible : cela doublerait un
nœud central du graphe d'un jumeau anglais.

Restent **6 références réellement absentes** de v110 : « Individualisme
méthodologique », « Sociologie économique », « Travail invisible »,
« Littérature indigène », « Terrain hors ligne », « Labélisation indigène ».
Ce sont elles, et elles seules, qui poseraient une question de création
(§ 7, Q6). Trois d'entre elles ont un voisinage sans être des synonymes — et
la nuance importe : « Terrain hors ligne » côtoie la `Method`
`b3af43b8…` « Observation participante (hors ligne) » et la `ThesisSection`
C.2.e ; « Labélisation indigène » n'a pour voisin que la `ThesisSection`
III.1.2.b « …labélisations indigènes… » ; « Littérature indigène » côtoie le
`Corpus` `1e5246b5…` « Corpus sources indigènes ». Aucun de ces voisins n'est
un concept homonyme : les rattacher serait un choix, pas une résolution.

Les 53 `fuzzy-only` (dont « Gouvernance », « STS », « Crise »…) demandent un
choix de rattachement au cas par cas ; une au moins (« Objets monétaires non
identifiés », P1-0) ne résout que vers la section de thèse homonyme, pas vers
un concept.

**Une résolution `unique` ne garantit pas que la cible soit du bon genre
(P6).** Cas vérifié : dans P2-0, la référence « II.2 "Pourtant, elles font
monnaie" ! : à l'aune d'un nominalisme "non étatiste" attentif aux usages »
résout en `unique` vers `38e637cc…` — qui est un nœud de type
**`ThesisSection`** (`section_key` = II.2), et non un concept. Un
`quote supports` posé vers cette cible **ferait doublon** avec le
`appears in section` que la même op produit déjà vers II.2. Le contrôle du
**type** de la cible doit donc être ajouté à toute résolution de
`quote_supports_entity_names`, indépendamment du niveau de confiance du
matching de nom.

### 5.4 Le cas P3-10 : une citation exacte… du mauvais document

`sq_phase3_CONCL_01` (« Un protocole ne devient CM qu'en tant
qu'infrastructure… ») est **verbatim** — mais dans le « Résumé et mots
clés » liminaire de la thèse (`1_Premières_pages.pdf`, p. 4 imprimée ;
recoupé dans `assets/MD/06_resume.md`), pas dans la conclusion. La cible
`conclu_resume` (« Conclusion — Résumé de la thèse », pp. 332-334) est un
**autre texte**, où cette phrase n'apparaît pas ; le `page_thesis: 5` du
patch trahissait déjà la source liminaire quand la fiche de section annonçait
« p. 332 ». Aucun nœud de section n'existe pour le résumé liminaire.

### 5.5 Découvertes annexes du sous-agent A (à instruire séparément)

- Nœud section **orphelin** `3ce505bc…` « I.2.1b Un protocole Bitcoin qui
  s'adapte… » sans `section_key`, doublon de titre avec I.2.2.b, portant
  **31 relations** ;
- **III.3** typée `ChapterSection` — unique occurrence de ce type dans v110
  (conséquence opératoire vérifiée en révision : elle est **invisible** à
  l'index de sections de l'outillage existant, § 5.7 (c)) ;
- **9 SourceQuotes v110 sans attribut `quoteText`** (citation portée par le
  nom seul) — aucune ne recoupe un candidat, mais leur fidélité n'a jamais
  été vérifiée ;
- `section_entities_map.json` ne connaît que les clés de niveau 1 : aucune
  sous-clé (intro_A_1, I.1.1, II.2.2.a…) n'y figure ;
- les clés de conclusion du patch (`conclusion_resume` /
  `conclusion_infrastructure` / `conclusion_crises`) sont un nommage propre à
  ChatGPT ; les clés réelles sont `conclu_resume` / `conclu_infra` /
  `conclu_aceph` (appariement par nom confirmé par le contenu, sauf P3-11 où
  la cible `conclu_aceph` est fausse : le passage est entièrement dans
  `conclu_infra`, avant le titre de l'acéphalisme).

### 5.6 Les `page_start` de v110 sont incohérents — préalable à toute gravure

Ajouté en révision (prise P3, confirmée). En v110, **37 nœuds de section
portent un attribut `page_start`** (35 sections numérotées + `conclu_resume`
et `conclu_boucs`). La revue hostile a mesuré que **16 de ces 35 sections
numérotées portent un `page_start` incohérent** avec la page imprimée de leur
titre. Le recomptage structural indépendant mené ici retrouve exactement ce
chiffre : **8 paires de sections partagent un `page_start` identique sans
être en relation parent/premier-enfant** — soit 16 nœuds :

| `page_start` partagé | Paire non hiérarchique |
|---|---|
| 78 | I.1.2 / I.1.3 |
| 154 | II.1.1.b / II.1.2 |
| 161 | II.2.2.a / II.2.1 |
| 173 | II.2.2.c / II.2.3 |
| 202 | **II.3.2** / II.3.3 |
| 241 | III.1.1.b / III.1.2 |
| 265 | **III.1.2.b** / **III.2.2** |
| 277 | III.2.1 / III.2.3 |

(Les cinq autres collisions — I.1.1/I.1.1.a à 58, II.1.1/II.1.1.a à 148,
II.2.2/II.2.2.b à 165, II.3.1/II.3.1.a à 186, III.1.1/III.1.1.a à 225 — sont
légitimes : une section-mère commence là où commence son premier
sous-titre.)

Confrontées au PDF, les valeurs contredisent frontalement le § 5.1 :

| Section | `page_start` v110 | Page réelle du titre (PDF) | Écart |
|---|---|---|---|
| II.3.1 | 186 | 186 | cohérent |
| II.3.1.a | 186 | 187 | 1 page |
| II.3.1.b | 190 | 188 | 2 pages |
| **II.3.2** | **202** | **190** | **12 pages** |
| III.1.2.a | 255 | < 243 (nécessairement) | **impossible** : III.1.2.b, qui la suit, a son titre p. 243 |
| **III.1.2.b** | **265** | **243** | **22 pages** |
| **III.2.2** | **265** | — | en collision avec III.1.2.b ; l'une des deux au plus peut être juste |
| I.2.2.b | 100 | 106 | 6 pages (hérité du parent I.2.2) |

Le motif est systématique : chaque nœud fautif porte le `page_start` de son
**voisin de bloc** — séquelle de même famille que les décalages de clés
réparés en v108/v109, mais sur un autre attribut. **16 est donc un plancher,
pas un plafond** : I.2.2.b, II.3.1.a, II.3.1.b et III.1.2.a sont décalés sans
être pris dans une collision, et n'entrent donc pas dans ce compte — le
relevé exhaustif des 35 pages de titre reste à faire (§ 9).

**Conséquence pour ce chantier.** La conclusion du § 5.1 — « la carte de
renumérotation a tort 4 fois » — **tient par le texte imprimé**, et la revue
l'a refaite indépendamment. Mais elle est **contredite par le graphe
lui-même** : graver P2-4/P2-5 dans `II.3.2` sur la foi du PDF installerait
une citation p. 191 dans une section dont v110 affirme qu'elle commence
p. 202 ; le lecteur du site, lui, verrait une citation « hors bornes » de sa
propre section. Réparer les `page_start` est un **chantier distinct** de la
migration SourceQuote — mais c'est un **préalable** si l'on veut que les
ancrages gravés soient lisibles. D'où la nouvelle question **Q8** au § 7.

### 5.7 L'outillage existant et ses pièges

Ajouté en révision (prise P2). Le dépôt contient déjà un embryon
d'applicateur : `scripts/apply-sourcequote-phases.mjs` et les quatre modules
`scripts/sourcequote-migration/{normalize,resolve,apply,report}.mjs`. Ce
chantier ne l'a **ni exécuté ni modifié**. Mais comme il servira
probablement de base à tout applicateur futur, ses propriétés vérifiées sont
consignées ici.

**Rectification d'abord : le script n'écrit rien.** La revue hostile a
affirmé qu'il « écrit dès `--write` ». **C'est faux**, et la conclusion de la
PR #113 (« n'écrit rien, même avec `--write` ») tient : `writeFile`,
`writeFileSync`, `appendFile`, `createWriteStream` et `fs.write` sont
**absents** du runner comme des quatre modules ; le seul import `fs` est
`import { readFileSync, readdirSync } from 'fs'`, deux primitives de lecture.
Rien n'est sérialisé sur disque, dans aucun mode. Cette prise est écartée.

**Mais quatre pièges sont réels, et vérifiés :**

- **(a) Le drapeau `--write` ment sur ce qu'il fait.** Ligne 60 :
  `const dryRun = !process.argv.includes('--write');` — un opérateur qui
  lit cette ligne, ou qui voit `--write` dans un `--help`, croira
  légitimement déclencher une écriture. En réalité `--write` ne fait que
  lever les gardes `if (!dryRun)` de `apply.mjs` (lignes 210, 226, 260), qui
  poussent les entités et relations construites dans les **tableaux en
  mémoire** du graphe chargé — jamais sur disque. Piège d'opérateur pur : le
  jour où quelqu'un ajoutera la sérialisation manquante, `--write` deviendra
  destructeur sans que sa signature ait changé. **Corollaire moins visible** :
  la branche « entité existante » d'`apply.mjs` appelle
  `applyEssentialAttributes` et `preserveSupportHierarchyAttributes`
  **sans garde `dryRun`** — le graphe en mémoire est donc muté même en
  dry-run (mutation additive seulement : ces fonctions ne remplissent que les
  attributs absents, `if (!existing)`). Inoffensif tant que rien n'est écrit ;
  fatal le jour où une sérialisation sera ajoutée « à la fin ».
- **(b) `findLatestGraph()` lirait la sortie de l'applicateur.** Lignes
  28-40 : la fonction liste les fichiers
  `grc20-these-mael-rolland-v<N>.json`, les trie par numéro et retourne **le
  plus grand**. Un applicateur bâti là-dessus qui produirait un `v111`
  relirait **sa propre sortie** au passage suivant, empilant les effets au
  lieu de repartir de la base arbitrée. Tout applicateur doit prendre son
  graphe d'entrée en argument explicite.
- **(c) L'index de sections de `resolve.mjs` est aveugle à III.3.** Ligne
  51 : `if (!typeNames.includes('ThesisSection')) continue;` — or **III.3 est
  typée `ChapterSection`** (`41e14735…`, seule occurrence de ce type dans
  v110, cf. § 5.5) et ne porte d'ailleurs pas de `page_start` mais un
  `sourcePage`. Sa clé `III.3` **n'entre jamais** dans `sectionByKey` : toute
  op la visant serait rapportée comme section non résolue, sans que la cause
  apparaisse. La même cécité frappe `buildGraphIndexes` dans `apply.mjs`
  (lignes 58-63, même test).
- **(d) La déduplication de l'applicateur ne verrait aucun des 6 doublons.**
  `apply.mjs` apparie un candidat à une SourceQuote existante par `seed_id`,
  puis par signature exacte `quoteText::page::section_key` normalisée. Or
  **aucune des 245 SourceQuotes de v110 ne porte d'attribut `seed_id`**
  (vérifié : 0/245), et les 6 existantes appariées ici diffèrent toutes du
  candidat par le texte — la signature ne peut donc pas matcher non plus.
  Résultat : les 6 doublons documentés au § 4 seraient **créés comme
  nouveaux nœuds**, et le rapport annoncerait 41 créations sans un seul
  doublon détecté. C'est le travail du § 4 qui les a trouvés, pas
  l'outillage.

Aucun applicateur ne doit être construit sur cette base sans traiter ces
quatre points — et, comme le rappelle le § 5.1, sans reprendre op par op
l'arbitrage de section que seul le texte permet.

## 6. Cas récupérables, cas à ne pas graver tels quels

**Récupérables sur le fond (24 `retenir`)** : textes vérifiés, sections
existantes et confirmées par la page. Attention toutefois : **17 de ces 24
portent `arbitrage=oui`** après révision, non pas sur leur texte ou leur
section mais parce qu'ils dépendent d'une politique éditoriale non tranchée.
Répartition des motifs (une op peut en cumuler deux) : **8** pour une coupe
non signalée (Q7), **6** pour une entité réellement absente (Q6), **3** pour
une entité résolue par synonyme ou traduction dont l'adoption reste à
confirmer (Q6), **1** pour la correction de coquille P2-6 (Q7). Seules **7
ops** — P1-0, P1-6, P1-10, P1-16, P2-1, P2-7, P3-1 — sont récupérables *sans
aucun jugement préalable*.

**Récupérables avec correction ciblée (5 + 4)** : les 5
`retenir-avec-correction-de-section` (P1-14 → II.3.1 ; P1-15 → II.3.1.b ;
P2-4 et P2-5 → II.3.2 ; P2-9 → III.3.4) — la correction est **prouvée par la
page et la TOC**, il ne reste qu'à la valider, **sous réserve du préalable
`page_start` du § 5.6** (P2-4/P2-5 sont directement concernées) ; et les 4
`completer-l-existante` (P1-8, P3-0, P3-6, P3-11). **Correction de la version
initiale (P4)** : cette dernière ligne les rangeait toutes quatre parmi les
cas « où le candidat est un superset vérifié ». C'est inexact. L'**inclusion
stricte** de l'existante dans le candidat n'est vérifiée que pour **P1-8,
P3-0, P3-7 et P3-11**. **P3-6 n'en fait pas partie** : l'existante
`68d8c0d5…` porte sa propre condensation (« protocole » pour « protocole de
base », « l'équipe » pour « l'équipe de développement ») et n'est donc pas
une sous-chaîne du candidat — la compléter suppose de **réécrire** son texte,
pas de le prolonger. (P3-7, qui est bien un superset strict, est classé
`arbitrage` pour une autre raison : sa section cible I.3.2b n'a jamais
existé.)

**À arbitrer avant tout (8 `arbitrage`)** : les 6 ops sur sections jamais
existées (dont 2 sont aussi des doublons partiels), le chevauchement sans
inclusion P3-2, l'annonce de section P2-0, et le résumé liminaire P3-10.

**À ne graver en aucun cas tels quels** : aucune op n'est fausse sur le
texte, mais **aucune n'est appliquable mécaniquement** : par construction
(résolution par nom, base v96), chaque op passe par au moins une résolution
que ce chantier a dû trancher à la main.

## 7. Questions pour Maël

1. **Les 5 recentrages de section prouvés** (P1-14 → II.3.1 ; P1-15 →
   II.3.1.b ; P2-4/P2-5 → II.3.2 ; P2-9 → III.3.4) : **(a)** valider les
   cinq corrections telles que prouvées par les pages ; **(b)** rabattre ces
   ops sur les sections-mères (II.3, III.3) pour éviter tout risque ;
   **(c)** abandonner ces 5 ops. *(Lié à Q8 : si (a), P2-4/P2-5 atterrissent
   dans une II.3.2 dont le graphe dit qu'elle commence p. 202 alors que la
   citation est p. 191.)*
2. **Les 6 sous-sections jamais existées** (I.2.1b, I.2.1c, I.2.2a, I.3.2b,
   I.3.3a, I.3.3c) : **(a)** rabattre les 6 ops sur les parents existants
   (I.2.1, I.2.2, I.3.2, I.3.3) ; **(b)** créer les 6 nœuds de niveau 3 —
   décision d'architecture qui touche le sommaire de `graphe.html` et
   `section_entities_map.json` ; **(c)** abandonner ces 6 ops. (Si (b) :
   régler d'abord le sort du nœud orphelin `3ce505bc…`, § 5.5.)
3. **Les 6 doublons**, en trois lots distincts (correction P4/P5) :
   **3.1 — les 4 supersets stricts** (P1-8, P3-0, P3-7, P3-11, inclusion
   vérifiée) : **(a)** compléter le `quoteText` de l'existante avec la
   version longue vérifiée (en gardant id et relations) ; **(b)** conserver
   l'existante courte et abandonner le candidat ; **(c)** au cas par cas.
   **3.2 — P3-6**, qui n'est *pas* un superset strict : l'existante
   `68d8c0d5…` porte une condensation propre (« protocole » pour « protocole
   de base », « l'équipe » pour « l'équipe de développement »), le candidat
   est plus fidèle au PDF mais ne la contient pas — **(a)** remplacer le
   `quoteText` de l'existante par la version longue fidèle (c'est une
   **réécriture**, pas un complément) ; **(b)** garder l'existante telle
   quelle ; **(c)** faire coexister les deux.
   **3.3 — P3-2**, chevauchement sans inclusion avec `47dfac14…`, sachant que
   **l'existante est elle-même fautive** (2 146 caractères sautés sans marque
   entre ses deux fragments, et texte préfixé de l'intertitre « La phase de
   "péché" (d'avril 2012 à octobre 2013) », § 4) : **(a)** fusionner en une
   seule citation longue p. 93 — mais ce serait greffer du texte vérifié sur
   une citation déjà fautive ; **(b)** réparer d'abord `47dfac14…` (chantier
   distinct), puis décider ; **(c)** faire coexister deux SourceQuotes
   distinctes ; **(d)** abandonner le candidat.
4. **P3-10 (résumé liminaire)** : **(a)** abandonner ; **(b)** rattacher à
   `conclu_resume` avec une localisation honnête (« Résumé et mots clés »,
   premières pages p. 4) ; **(c)** créer un nœud de section pour le résumé
   liminaire.
5. **P2-0 (annonce de II.2 depuis l'intro du chapitre II, p. 146)** :
   **(a)** garder le rattachement à II.2 en tant qu'ancre d'annonce ;
   **(b)** abandonner ; **(c)** rattacher au chapitre II lui-même.
   *(Point technique à trancher au passage : la première
   `quote_supports_entity_names` de cette op résout vers `38e637cc…`, qui est
   la **section** II.2 elle-même, pas un concept — le `quote supports`
   ferait doublon avec le `appears in section` de la même op et doit être
   omis quelle que soit l'option retenue, § 5.3.)*
6. **Les 6 références d'entités réellement absentes** — « Individualisme
   méthodologique », « Sociologie économique », « Travail invisible »,
   « Littérature indigène », « Terrain hors ligne », « Labélisation
   indigène » (§ 5.3) : **(a)** ne rien créer — les `quote supports`
   correspondants sont simplement omis ; **(b)** créer tout ou partie de ces
   6 concepts après passage par `grc20-semantic-classifier` ; **(c)** pour
   celles qui ont un voisin non homonyme, rattacher à ce voisin plutôt que
   créer (« Terrain hors ligne » → `b3af43b8…` `Method` « Observation
   participante (hors ligne) » ; « Littérature indigène » → `1e5246b5…`
   `Corpus` « Corpus sources indigènes » ; « Labélisation indigène » → la
   `ThesisSection` III.1.2.b) — c'est un choix d'auteur, pas une résolution ;
   **(d)** mixte, liste à cocher.
   > **Cette question a changé de nature en révision (P1).** Elle portait sur
   > « 11 introuvables » et proposait de créer en premier lieu un nœud
   > « Polycentric Governance ». **Ne pas le faire** : `a444085b…`
   > « Gouvernance polycentrique » (`CoreConcept`) existe déjà en v110 et est
   > la cible des 4 occurrences ; « Controverse sur le statut monétaire »
   > désigne de même `758e9ca9…`. Créer ces nœuds doublerait un concept
   > central du graphe d'un jumeau anglais. **Sous-question réelle** :
   > faut-il inscrire ces deux correspondances (EN→FR, synonyme) dans une
   > table d'alias réutilisable, pour que le prochain résolveur ne
   > reproduise pas le faux négatif ? Et, en second rideau : quelle politique
   > pour les 53 `fuzzy-only` — rattachement au meilleur candidat, ou
   > omission ?
7. **Politique de fidélité du texte cité** : 18 ops portent des **coupes non
   signalées** (citations, notes, membres de phrase, jusqu'à ~2 phrases
   entières) et **1 op porte une correction de coquille** — P2-6, où le
   candidat ajoute « par » (« médiatisées **par** des dispositifs ») là où la
   thèse imprime « médiatisées des dispositifs ». **(a)** restaurer des
   « [...] » aux points de coupe et **conserver la coquille de l'original**
   avant toute gravure (recommandé par la vérification : le texte gravé
   redevient défendable lettre à lettre) ; **(b)** graver tel quel ;
   **(c)** restaurer le texte PDF intégral ; **(d)** traiter séparément la
   coquille — la corriger avec un `[sic]` ou une note d'édition, ce qui est
   un choix d'auteur et non une normalisation.
   > Cas le plus net à examiner : **P2-8**, dont la coupe silencieuse
   > supprime « et sans être à l'époque formellement encadré » — une réserve
   > de fond, pas une parenthèse bibliographique — et perd les guillemets de
   > « huis clos ». Tant que cette question n'est pas tranchée, **aucune op à
   > coupe n'est "à retenir sans arbitrage"** : les 18 portent désormais
   > `needs_mael_arbitration=oui`, P2-6 comprise.
8. **Les 16 `page_start` incohérents de v110** (§ 5.6) — préalable technique,
   nouveau en révision : **(a)** réparer d'abord les `page_start` (chantier
   distinct, à mener comme v108/v109 : relevé des titres imprimés puis patch
   d'attributs), et ne graver les ancrages SourceQuote qu'ensuite ;
   **(b)** graver les ancrages sur la seule foi du texte imprimé, en laissant
   l'incohérence en place et en la consignant comme dette connue ;
   **(c)** différer l'ensemble de la migration SourceQuote jusqu'à ce que la
   question des `page_start` soit instruite.
   > L'enjeu concret : avec (b), P2-4 et P2-5 seraient gravées dans `II.3.2`
   > à la page 191, dans une section que le graphe déclare commencer p. 202.
   > Le § 5.1 a raison **par le texte**, le graphe dit le contraire **par ses
   > attributs** — et c'est le graphe que lit le site.

## 8. Le sort des zips — matière à décision (la décision est à Maël)

Trois issues étaient posées par le préflight ; les chiffres de ce chantier
les éclairent ainsi, sans trancher :

- **Réécriture en patch candidat canonique** : c'est l'issue que les
  chiffres soutiennent le mieux, et la révision **la renforce plutôt qu'elle
  ne l'affaiblit** — la prise P1 retire 5 créations d'entités de la liste des
  obstacles, et 33/41 ops (80 %) restent récupérables moyennant des
  corrections toutes **déjà déterminées** (24 retenir + 5 recentrages prouvés
  + 4 compléments d'existantes) ; les 8 restantes ont chacune une question
  fermée au § 7. Une réécriture conforme au contrat
  (`grc20-candidate-patch-contract-v1.md`) résorberait d'un coup les trois
  vices de forme rédhibitoires des zips : dialecte hors contrat, résolution
  par nom, base v96 avec clés pré-migration. **Nuance ajoutée en révision** :
  « récupérable » ne veut pas dire « gravable maintenant ». 17 des 24
  `retenir` attendent une politique éditoriale (Q6/Q7), et **l'ensemble des
  ancrages de chapitres II et III attend la réparation des `page_start`
  (Q8)**. L'ordre réaliste est donc : réponses du § 7 → réparation des
  `page_start` → réécriture en patch candidat → préflight → gravure.
- **Archive définitive des zips** : justifiée dans **tous** les cas pour les
  fichiers eux-mêmes — même si leur contenu est repris, les zips ne doivent
  plus jamais servir de source d'application directe (4 misroutes de
  sections sur 6 clés sensibles, 6 cibles inexistantes, 18 coupes
  silencieuses, 1 correction de coquille). Le zip `foundation`, sans ops, n'a
  que valeur documentaire. **À archiver au même titre : l'idée d'appliquer
  ces ops avec l'outillage existant** — `scripts/apply-sourcequote-phases.mjs`
  et ses modules ne détecteraient aucun des 6 doublons et ne verraient pas
  III.3 (§ 5.7).
- **Abandon partiel** : se défend uniquement pour un sous-ensemble — les 6
  doublons (si la politique est de garder les existantes courtes) et P3-10 ;
  soit au plus 7 ops. Un abandon total serait en revanche coûteux : 34 ops
  apportent des citations vérifiées verbatim sur des sections aujourd'hui
  identifiées `CRITICAL_ZERO` par le patch d'origine, et ce travail de
  vérification page à page est maintenant fait et consigné.

Dans tous les scénarios, l'arbitrage **Q8 du préflight** (à ne pas confondre
avec la Q8 nouvelle du § 7 ci-dessus) demeure : **aucun applicateur avant les
réponses du § 7**. La révision y ajoute un second verrou : **aucune gravure
d'ancrage de chapitre II ou III avant réparation des `page_start`** (§ 5.6).

## 9. Ce que ce chantier n'a pas fait

- **Aucune écriture dans le graphe**, aucune SourceQuote créée ni modifiée,
  aucun patch appliqué ni généré, aucun applicateur écrit ni exécuté ;
- pas de vérification des **9 SourceQuotes v110 sans `quoteText`** (§ 5.5) ni
  des SourceQuotes v110 existantes en général — seules les 6 appariées aux
  candidats ont été relues ;
- pas d'adjudication des **53 entités fuzzy** (le CSV consigne les statuts,
  pas les choix) ;
- pas de traitement du nœud orphelin `3ce505bc…`, du type `ChapterSection`
  de III.3, ni des sous-clés absentes de `section_entities_map.json` ;
- pas de comparaison avec les traductions EN de `assets/MD/` (les FR font
  foi, les PDF ont suffi) ;
- pas de contrôle visuel navigateur (`grc20-visual-coherence`) — rien n'a
  changé côté runtime ;
- pas de réécriture des zips en patch candidat : elle n'a de sens qu'après
  les arbitrages du § 7.

Ajouts de la révision du 2026-08-07 — ce que la révision n'a **pas** fait
non plus :

- **aucune réparation des `page_start`** (§ 5.6) : les 16 valeurs
  incohérentes sont documentées, pas corrigées ; le relevé exhaustif des
  pages de titre des 35 sections reste à faire (seules 8 ont été confrontées
  au PDF ici, les autres sont signalées par collision structurelle) ;
- **aucune exécution, aucune modification** de
  `scripts/apply-sourcequote-phases.mjs` ni de
  `scripts/sourcequote-migration/*.mjs` : le § 5.7 est une lecture de code,
  pas une intervention ;
- **aucune réparation de la SourceQuote `47dfac14…`** dont le § 4 établit
  qu'elle est un montage silencieux — c'est un chantier distinct, à instruire
  avec les 244 autres SourceQuotes v110 jamais re-vérifiées ;
- **aucune création d'alias** pour les correspondances EN→FR et synonymiques
  découvertes en § 5.3 : elles sont consignées dans le CSV, pas outillées
  (sous-question de Q6).
