# SourceQuote Migration Verification Lab v1 — 41 citations vérifiées contre la thèse, aucune gravée

**Date** : 2026-08-07
**Graphe** : `grc20-these-mael-rolland-v110.json` (**inchangé** par ce chantier)
**Branche** : `claude/file-upload-branch-check-jw4cng`
**Mode agent** : A (vérification probatoire — **aucune création, aucune application**, aucun fichier de patch modifié ni créé)
**Outils** : extraction des zips `Migration/` + vérification pypdf contre les PDF canoniques (`assets/pdf/4_Introduction_generale.pdf`, `5_Chapitre_1.pdf`, `6_Chapitre_2.pdf`, `7_Chapitre_3.pdf`, `8_Conclusion_Generale.pdf`, complétés ponctuellement par `1_Premières_pages.pdf` et `2_Tables_des_matieres.pdf`) ; repli MD (`assets/MD/`) non nécessité — utilisé une seule fois en recoupement (`06_resume.md`, § 5.4)
**Données** : `docs/audits/data/sourcequote-migration-verification-v1.csv` (41 lignes, 18 champs)
**Prédécesseurs** : `candidate-patch-preflight-lab-v1.md` § 9.2 (arbitrage Q8 : « vérifier d'abord »), `docs/audits/data/candidate-patch-inventory-v1.csv` (lignes 1-3), inventaire brut du sous-agent A (scratchpad, `sourcequote-inventory-raw.json`)

> Contrôle de recoupement : les chiffres de ce document ont été re-vérifiés
> par recomptage direct du CSV commité — 41 lignes de données, 18 champs
> partout ; 14 `exact-match` / 14 `minor-normalization` / 7 `wrong-section` /
> 6 `duplicate-existing` ; 0 `paraphrase-only`, 0 `not-found` (au sens : les
> 41 textes existent dans la thèse) ; 27 `needs_mael_arbitration=oui` /
> 14 `non` ; recommandations 24 `retenir` / 5 `retenir-avec-correction-de-section` /
> 4 `completer-l-existante` / 8 `arbitrage` ; 169 références d'entités
> (105 uniques / 53 fuzzy / 11 introuvables) et 57 cibles de section
> (40 existantes / 11 renumérotées / 6 jamais existées) recomptées depuis
> l'inventaire d'A. La calibration de page est exacte : chaque page des PDF
> porte son numéro imprimé « — NN — » dans la pagination de la thèse ;
> aucun décalage de bloc à estimer.

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
signalée par « [...] ») et il se trompe de section plus souvent que de texte.

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

`needs_mael_arbitration` : **27 oui / 14 non**. Recommandations : 24
`retenir`, 5 `retenir-avec-correction-de-section`, 4 `completer-l-existante`,
8 `arbitrage`.

## 4. Les 6 doublons v110 — nature exacte de chaque équivalence

Les six appariements `duplicate_risk=eleve` d'A sont tous **confirmés** ; la
PR #113 en soupçonnait 3, il y en a bien 6. Nature exacte :

| Op | Existante v110 | Équivalence vérifiée |
|---|---|---|
| P1-8 `sq_gap_intro_B3_02` | `a5278302…` « choix des deux crises » (p. 34) | L'existante est un **fragment strict** du candidat (« le bogue CVE 2018 #17144 … "The DAO" ») ; le candidat ajoute l'amont et l'aval, tous verbatim p. 33. |
| P3-0 `sq_phase3_I2_01` | `8f150b5d…` « dévoilant l'invisible carnavalesque » (p. 89) | Existante = 1re phrase **verbatim strict** ; candidat = superset (ajoute la 2e phrase, verbatim). |
| P3-2 `sq_phase3_I2_03` | `47dfac14…` « WikiLeaks accepte le BTC — p.93 » | **Chevauchement sans inclusion** : tronc commun verbatim (« Avec WikiLeaks … l'en priver »), puis l'existante poursuit sur les marchés noirs, le candidat sur le régime transactionnel. Seul cas où aucun des deux ne contient l'autre. |
| P3-6 `sq_phase3_I3_01` | `68d8c0d5…` « Buterin : peur que les règles changent » (p. 123) | L'existante porte le passage central (citation Buterin) **légèrement condensé par elle-même** (« protocole » pour « protocole de base », « l'équipe » pour « l'équipe de développement ») ; le candidat est un superset **plus fidèle au PDF**. |
| P3-7 `sq_phase3_I3_02` | `6b1a40ec…` « dépendances au sentier (Russo 2020) » (p. 125) | Existante = 1re phrase verbatim strict ; candidat = superset (mais vise en plus une section jamais existée, I.3.2b). |
| P3-11 `sq_phase3_CONCL_02` | `fb610652…` « gouvernance conflictuelle et polycentrique » (p. 336) | Existante = 1re phrase verbatim strict ; candidat = superset qui saute sans marque une phrase intermédiaire (« Les infrastructures … idéologiques. ») et « (pour l'heure) ». |

Dans 5 cas sur 6 le candidat est **plus long et vérifié verbatim** : la
question n'est pas « doublon ou pas » mais « compléter l'existante,
la remplacer, ou s'en tenir à la version courte » — c'est un jugement
d'auteur (§ 7, Q3).

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

### 5.3 Entités : 11 introuvables, 53 fuzzy (sur 169 références)

Les `quote_supports_entity_names` résolvent à 105/169 en `unique`. Les 11
introuvables (9 noms : « Controverse sur le statut monétaire »,
« Individualisme méthodologique », « Polycentric governance » ×3 sous deux
graphies, « Sociologie économique », « Travail invisible », « Littérature
indigène », « Terrain hors ligne », « Labélisation indigène ») exigeraient
des **créations de Concepts** — hors mandat d'un applicateur mécanique, et
notable : « Polycentric Governance », concept central de la thèse, n'a pas
de nœud propre en v110. Les 53 `fuzzy-only` (dont « Gouvernance »,
« STS », « Crise »…) demandent un choix de rattachement au cas par cas ; une
au moins (« Objets monétaires non identifiés », P1-0) ne résout que vers la
section de thèse homonyme, pas vers un concept.

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
- **III.3** typée `ChapterSection` — unique occurrence de ce type dans v110 ;
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

## 6. Cas récupérables, cas à ne pas graver tels quels

**Récupérables sans jugement de fond (24 `retenir`)** : textes vérifiés,
sections existantes et confirmées par la page. Réserves transversales :
restaurer les « [...] » sur les coupes silencieuses avant gravure, et
statuer sur les entités introuvables qui figurent dans 9 de ces 24 ops.

**Récupérables avec correction ciblée (5 + 4)** : les 5
`retenir-avec-correction-de-section` (P1-14 → II.3.1 ; P1-15 → II.3.1.b ;
P2-4 et P2-5 → II.3.2 ; P2-9 → III.3.4) — la correction est **prouvée par la
page et la TOC**, il ne reste qu'à la valider ; et les 4
`completer-l-existante` (P1-8, P3-0, P3-6, P3-11) où le candidat est un
superset vérifié d'une SourceQuote v110.

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
   **(c)** abandonner ces 5 ops.
2. **Les 6 sous-sections jamais existées** (I.2.1b, I.2.1c, I.2.2a, I.3.2b,
   I.3.3a, I.3.3c) : **(a)** rabattre les 6 ops sur les parents existants
   (I.2.1, I.2.2, I.3.2, I.3.3) ; **(b)** créer les 6 nœuds de niveau 3 —
   décision d'architecture qui touche le sommaire de `graphe.html` et
   `section_entities_map.json` ; **(c)** abandonner ces 6 ops. (Si (b) :
   régler d'abord le sort du nœud orphelin `3ce505bc…`, § 5.5.)
3. **Les 6 doublons** : pour les 5 supersets — **(a)** compléter le
   `quoteText` de l'existante avec la version longue vérifiée (en gardant
   id et relations) ; **(b)** conserver l'existante courte et abandonner le
   candidat ; **(c)** au cas par cas. Pour P3-2 (chevauchement sans
   inclusion avec `47dfac14…`) — **(a)** fusionner en une seule citation
   longue p. 93 ; **(b)** faire coexister deux SourceQuotes distinctes ;
   **(c)** abandonner le candidat.
4. **P3-10 (résumé liminaire)** : **(a)** abandonner ; **(b)** rattacher à
   `conclu_resume` avec une localisation honnête (« Résumé et mots clés »,
   premières pages p. 4) ; **(c)** créer un nœud de section pour le résumé
   liminaire.
5. **P2-0 (annonce de II.2 depuis l'intro du chapitre II, p. 146)** :
   **(a)** garder le rattachement à II.2 en tant qu'ancre d'annonce ;
   **(b)** abandonner ; **(c)** rattacher au chapitre II lui-même.
6. **Les 11 références d'entités introuvables** (9 noms, § 5.3) : **(a)** ne
   pas créer — les `quote supports` correspondants sont simplement omis ;
   **(b)** créer les concepts manquants après passage par la classification
   sémantique (au premier rang : « Polycentric Governance ») ; **(c)** mixte,
   liste à cocher. Même question, en second rideau, pour la politique sur
   les 53 fuzzy : rattachement au meilleur candidat ou omission ?
7. **Politique de fidélité des coupes** : 18 ops portent des coupes non
   signalées (citations, notes, membres de phrase). **(a)** restaurer des
   « [...] » aux points de coupe avant toute gravure (recommandé par la
   vérification : le texte gravé redevient défendable lettre à lettre) ;
   **(b)** graver tel quel ; **(c)** restaurer le texte PDF intégral.

## 8. Le sort des zips — matière à décision (la décision est à Maël)

Trois issues étaient posées par le préflight ; les chiffres de ce chantier
les éclairent ainsi, sans trancher :

- **Réécriture en patch candidat canonique** : c'est l'issue que les
  chiffres soutiennent le mieux. 33/41 ops (80 %) sont récupérables
  moyennant des corrections toutes **déjà déterminées** (24 retenir +
  5 recentrages prouvés + 4 compléments d'existantes) ; les 8 restantes ont
  chacune une question fermée au § 7. Une réécriture conforme au contrat
  (`grc20-candidate-patch-contract-v1.md`) résorberait d'un coup les trois
  vices de forme rédhibitoires des zips : dialecte hors contrat, résolution
  par nom, base v96 avec clés pré-migration.
- **Archive définitive des zips** : justifiée dans **tous** les cas pour les
  fichiers eux-mêmes — même si leur contenu est repris, les zips ne doivent
  plus jamais servir de source d'application directe (4 misroutes de
  sections sur 6 clés sensibles, 6 cibles inexistantes, 18 coupes
  silencieuses). Le zip `foundation`, sans ops, n'a que valeur documentaire.
- **Abandon partiel** : se défend uniquement pour un sous-ensemble — les 6
  doublons (si la politique est de garder les existantes courtes) et P3-10 ;
  soit au plus 7 ops. Un abandon total serait en revanche coûteux : 34 ops
  apportent des citations vérifiées verbatim sur des sections aujourd'hui
  identifiées `CRITICAL_ZERO` par le patch d'origine, et ce travail de
  vérification page à page est maintenant fait et consigné.

Dans tous les scénarios, l'ordre arbitré en Q8 demeure : **aucun
applicateur avant les réponses du § 7**.

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
