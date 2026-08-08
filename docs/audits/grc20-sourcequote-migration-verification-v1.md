# SourceQuote Migration Verification Lab v1 — 41 citations vérifiées contre la thèse, aucune gravée

**Date** : 2026-08-07 · **révisé le 2026-08-07 après revue hostile** (cf. § 0) · **arbitrages de Maël inscrits le 2026-08-07** (cf. encadré ci-dessous et § 7)
**Graphe** : `grc20-these-mael-rolland-v110.json` (**inchangé** par ce chantier, révision et inscription des arbitrages comprises)
**Branche** : `claude/file-upload-branch-check-jw4cng`
**Mode agent** : A (vérification probatoire — **aucune création, aucune application**, aucun fichier de patch modifié ni créé)
**Outils** : extraction des zips `Migration/` + vérification pypdf contre les PDF canoniques (`assets/pdf/4_Introduction_generale.pdf`, `5_Chapitre_1.pdf`, `6_Chapitre_2.pdf`, `7_Chapitre_3.pdf`, `8_Conclusion_Generale.pdf`, complétés ponctuellement par `1_Premières_pages.pdf` et `2_Tables_des_matieres.pdf`) ; repli MD (`assets/MD/`) non nécessité — utilisé une seule fois en recoupement (`06_resume.md`, § 5.4)
**Données** : `docs/audits/data/sourcequote-migration-verification-v1.csv` (41 lignes, 18 champs)
**Prédécesseurs** : `candidate-patch-preflight-lab-v1.md` § 9.2 (arbitrage Q8 : « vérifier d'abord »), `docs/audits/data/candidate-patch-inventory-v1.csv` (lignes 1-3), inventaire brut du sous-agent A (scratchpad, `sourcequote-inventory-raw.json`)

> ## Arbitrages rendus
>
> **Maël a répondu aux huit questions du § 7 le 2026-08-07.** Ce dossier les
> inscrit, sans les réinterpréter ; il **n'applique toujours rien**.
>
> - **Q1 — (a), conditionné à Q8.** Les 5 recentrages sont validés sur la foi
>   du texte imprimé (P1-14 → II.3.1, P1-15 → II.3.1.b, P2-4 → II.3.2,
>   P2-5 → II.3.2, P2-9 → III.3.4) : « le texte tranche contre la carte de
>   renumérotation quand ils divergent ». Mais les rattachements ne seront pas
>   gravés tant que les `page_start` incohérents ne sont pas réparés.
> - **Q2 — (a).** Les 6 sous-sections jamais existées sont **rabattues sur
>   leurs parentes** pour ce chantier. Aucun nœud de niveau 3 n'est créé :
>   « la création éventuelle du niveau `###` doit devenir un chantier
>   structurel séparé, pas un effet de bord de cette migration ».
> - **Q3.1 — (a).** Les 4 supersets stricts (P1-8, P3-0, P3-7, P3-11) :
>   compléter les SourceQuote existantes avec le texte plus long.
>   **Q3.2 — (a).** P3-6 : réécrire l'existante `68d8c0d5…` sur le candidat —
>   « la fidélité au PDF prime sur la condensation antérieure ».
>   **Q3.3 — (b).** P3-2 : réparer d'abord `47dfac14…`, puis décider —
>   « ne pas greffer un candidat propre sur une SourceQuote déjà corrompue
>   sans réparation préalable ».
> - **Q4 — (b).** P3-10 n'est retenue que si elle est localisée honnêtement
>   comme résumé liminaire (p. 4 de `1_Premières_pages.pdf`), pas comme
>   conclusion ; aucun nœud de section créé pour elle ; pas de rattachement à
>   `conclu_resume` si ce n'est pas le même texte.
> - **Q5 — (a).** P2-0 est gardée, rattachée à l'introduction du chapitre II ;
>   le `quote supports` vers `38e637cc…` est **supprimé** — « cela doublerait
>   le lien d'ancrage et confondrait une section avec une entité de soutien ».
> - **Q6 — (a) + table d'alias.** Ne rien créer ; les `quote supports` vers
>   les 6 entités réellement absentes sont abandonnés. Une table d'alias
>   EN→FR est commandée : `docs/audits/data/entity-alias-table-v1.csv`.
> - **Q7 — (d).** Restaurer les marques de coupe `[…]` **partout** (18 ops) ;
>   pour P2-6, conserver la coquille imprimée « médiatisées des dispositifs »
>   et la signaler `[sic]`. Principe : « **une citation peut être abrégée,
>   mais jamais coupée sans marque ; et une correction silencieuse du texte
>   original est à proscrire.** »
> - **Q8 — (a).** Réparer les `page_start` incohérents **d'abord**, dans un
>   chantier distinct et mesurable, puis seulement graver les SourceQuote :
>   « je ne veux pas installer des citations p. 191 dans une section que le
>   graphe dit commencer p. 202 ».
>
> **Condition générale**
>
> **Toute action applicative de cette migration est désormais conditionnée à
> la réparation préalable des `page_start` (Q8).** Les 41 lignes du CSV
> portent cette mention. Aucun arbitrage ci-dessus n'autorise une gravure
> immédiate : ils fixent *ce qu'il faudra graver*, pas *quand*. Trois points
> restent hors de leur portée et sont signalés comme tels (§ 7, encadré
> « Ce que les arbitrages ne couvrent pas »).

---

> Contrôle de recoupement : les chiffres de ce document ont été re-vérifiés
> par recomptage direct du CSV commité — 41 lignes de données, 18 champs
> partout ; 14 `exact-match` / 14 `minor-normalization` / 7 `wrong-section` /
> 6 `duplicate-existing` ; 0 `paraphrase-only`, 0 `not-found` (au sens : les
> 41 textes existent dans la thèse) ; 169 références d'entités
> (**105 uniques / 53 fuzzy / 5 résolues par synonyme ou traduction /
> 6 réellement introuvables**) et 57 cibles de section
> (40 existantes / 11 renumérotées / 6 jamais existées). La calibration de
> page est exacte : chaque page des PDF porte son numéro imprimé « — NN — »
> dans la pagination de la thèse ; aucun décalage de bloc à estimer.
>
> **Recommandations après inscription des arbitrages** (recomptées sur le CSV
> révisé) : **25 `retenir` / 9 `retenir-avec-correction-de-section` /
> 5 `completer-l-existante` / 2 `arbitrage`** — contre 24 / 5 / 4 / 8 avant
> arbitrage. Six lignes ont changé de recommandation (§ 7, tableau
> récapitulatif). La colonne `needs_mael_arbitration` est laissée en
> l'état — **34 `oui` / 7 `non`** : elle enregistre *quelles ops ont été
> soumises à Maël*, pas leur état après réponse. Ce sont `recommendation` et
> `notes` qui portent les verdicts.
>
> **Sémantique des valeurs de `recommendation`** (inchangée sauf mention) :
> `retenir` = op récupérable telle qu'annoncée, sous réserve des corrections
> éditoriales de Q6/Q7 ; `retenir-avec-correction-de-section` = op récupérable
> après changement de cible sectionnelle (recentrage prouvé de Q1 **ou**
> rabattement sur la parente de Q2) ; `completer-l-existante` = ne pas créer
> de nœud, agir sur la SourceQuote v110 déjà présente — **cette valeur couvre
> désormais deux gestes distincts** : le *complément* de Q3.1 (4 ops, le texte
> long contient le texte court) et la *réécriture* de Q3.2 (P3-6 seule, le
> texte court n'est pas une sous-chaîne du long) ; `arbitrage` = op dont la
> décision reste ouverte après le 2026-08-07.

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
classées `non` et P2-6, cf. § 0). **Cette colonne n'a pas été retouchée après
les arbitrages** : elle dit quelles ops ont été *soumises* à Maël, ce qui
reste vrai. Les 7 ops restées à `non` (P1-0, P1-6, P1-10, P1-16, P2-1, P2-7,
P3-1) sont celles où le texte est verbatim, la section confirmée par la page,
et où aucune coupe ni aucune entité litigieuse n'intervient.

Recommandations — **état après inscription des arbitrages du § 7** :

| `recommendation` | Avant arbitrage | **Après arbitrage** | Ce qui a bougé |
|---|---|---|---|
| `retenir` | 24 | **25** | P2-0 y entre (Q5 (a)) |
| `retenir-avec-correction-de-section` | 5 | **9** | + P3-3, P3-4, P3-8, P3-9, rabattues sur leur parente (Q2 (a)) |
| `completer-l-existante` | 4 | **5** | + P3-7 (Q3.1 (a)) ; P3-6 y reste mais au titre d'une *réécriture* (Q3.2 (a)) |
| `arbitrage` | 8 | **2** | ne restent que P3-2 (Q3.3 (b) : réparation préalable) et P3-10 (Q4 (b) : impasse signalée) |
| **Total** | **41** | **41** | 6 lignes changées |

Les deux axes se croisent toujours : **19 ops portent une correction
éditoriale à faire avant gravure** au titre de Q7 (les 18 coupes non
signalées + la coquille P2-6), et **12 portent une décision d'entité** au
titre de Q6 (6 liens abandonnés, 5 résolutions par synonyme/traduction,
1 référence `fuzzy-only` laissée sans politique). Une recommandation
`retenir` ne signifie donc pas « gravable en l'état » : elle signifie
« récupérable, une fois les corrections de Q6/Q7 appliquées et les
`page_start` réparés (Q8) ».

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

**Arbitré (Q3).** Les trois lots reçoivent trois réponses distinctes :
**Q3.1 (a)** — les 4 supersets stricts (P1-8, P3-0, P3-7, P3-11) sont
**complétés** sur l'existante ; **Q3.2 (a)** — P3-6 est **réécrite** sur le
candidat, « la fidélité au PDF prime sur la condensation antérieure » ;
**Q3.3 (b)** — P3-2 attend la **réparation préalable** de `47dfac14…`, « ne
pas greffer un candidat propre sur une SourceQuote déjà corrompue sans
réparation préalable ». Dans les trois cas, aucun nœud SourceQuote nouveau
n'est créé. La version courte n'est retenue nulle part.

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
> de `47dfac14…` est un chantier distinct de la migration. **C'est la voie
> retenue par Q3.3 (b)** : réparer d'abord, décider ensuite.

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
>
> **Arbitré (Q1 (a) + Q8 (a)).** Maël valide les 5 recentrages **sur la foi
> du texte imprimé** — « le texte tranche contre la carte de renumérotation
> quand ils divergent » — et **gèle leur gravure** jusqu'à réparation des
> `page_start`. Le § 5.1 fait donc foi pour la *cible* ; il ne fait pas foi
> pour le *moment*.

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

**Arbitré (Q2 (a)).** Les 6 ops sont **rabattues sur leur section parente**
pour ce chantier, et **aucun nœud de niveau 3 n'est créé** : « la création
éventuelle du niveau `###` doit devenir un chantier structurel séparé, pas un
effet de bord de cette migration ». Rabattements nommés, tels qu'inscrits au
CSV (`target_section` conserve la clé visée, `recommendation` et `notes`
portent le rabattement) :

| Op | Clé visée (jamais existée) | Parente de rabattement | Id v110 |
|---|---|---|---|
| P3-2 | `I.2.1b` | **I.2.1** | `9cee8e18…` |
| P3-3 | `I.2.1c` | **I.2.1** | `9cee8e18…` |
| P3-4 | `I.2.2a` | **I.2.2** (pp. 100-108) | `93f13f18…` |
| P3-7 | `I.3.2b` | **I.3.2** | `ed2c565c…` |
| P3-8 | `I.3.3a` | **I.3.3** (titre p. 128) | `46111186…` |
| P3-9 | `I.3.3c` | **I.3.3** | `46111186…` |

Conséquence sur les recommandations : P3-3, P3-4, P3-8 et P3-9, qui ne
butaient que sur la section, passent de `arbitrage` à
`retenir-avec-correction-de-section` ; P3-7 passe à `completer-l-existante`
(son second motif est tranché par Q3.1) ; P3-2 reste à `arbitrage`, son
second motif étant renvoyé par Q3.3.

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

#### Le faux négatif était évitable sans aucune traduction — la donnée était déjà dans le graphe

La construction de la table d'alias (arbitrage Q6) a établi un fait plus
sévère encore, **vérifié directement dans v110** : l'entité `a444085b…`
porte l'attribut **`nameEn = "Polycentric Governance"`** — *exactement*
la chaîne que le patch déclarait introuvable. La correspondance ne
demandait ni traduction, ni synonymie, ni jugement : une simple lecture
d'un attribut existant suffisait.

Le graphe v110 porte **115 attributs `nameEn`, 77 `labelEn` et
30 `aliases`** (recomptés). Le résolveur employé par la migration n'a
interrogé que le champ `name` : il a ignoré 222 désignations alternatives
déjà déclarées par le graphe lui-même. Même mécanisme sur `6baa8059…`
« Infrastructure », dont le `nameEn` est « Seamless Infrastructure » — la
chaîne laissée en `fuzzy-only` quatre fois.

**Conséquence pour la suite** : le correctif prioritaire n'est pas la
table d'alias, c'est **la règle de résolution** — tout résolveur futur
doit interroger `name`, `nameEn`, `labelEn`, `labelFr` et `aliases` avant
de conclure à une absence. La table d'alias
(`docs/audits/data/entity-alias-table-v1.csv`, 400 alias sur 271 entités)
couvre ce que le graphe ne déclare pas ; elle ne dispense pas de lire ce
qu'il déclare déjà.

**Découverte annexe, à instruire séparément** : trois doublons FR/EN sont
**déjà réalisés** dans v110 — « Divulgation responsable » (`2f54deb5…`,
deg 17) / « Responsible Disclosure » (`018cb3c5…`, deg 5) ; « Logique de
consensus distribué » (`eccebadf…`, deg 23) / « Distributed Consensus
Fiduciary Logic » (`cae0d43b…`, deg 9) ; « Pools de minage »
(`5f7f718b…`, `ActorGroup`, deg 41) / « Mining pools » (`ee727747…`,
`InfrastructureEvent`, deg 7 — même référent sous **deux types
incompatibles**, anomalie de typage plutôt que fusion évidente). Une
quatrième paire probable : `2e24bde0…` / `53983b53…`
(« Institutionnalisme Monétaire Francophone », `TheoreticFramework` vs
`Concept`). Le risque que ce chantier a évité **s'est donc déjà
matérialisé ailleurs** — aucune fusion n'est proposée ici, c'est un
chantier d'arbitrage distinct.

Restent **6 références réellement absentes** de v110 : « Individualisme
méthodologique », « Sociologie économique », « Travail invisible »,
« Littérature indigène », « Terrain hors ligne », « Labélisation indigène ».
Ce sont elles, et elles seules, qui poseraient une question de création
(§ 7, Q6) — **arbitrée en (a) : ne rien créer, les six `quote supports`
correspondants sont abandonnés**, y compris pour les trois qui ont un voisin
non homonyme. Trois d'entre elles ont un voisinage sans être des synonymes — et
la nuance importe : « Terrain hors ligne » côtoie la `Method`
`b3af43b8…` « Observation participante (hors ligne) » et la `ThesisSection`
C.2.e ; « Labélisation indigène » n'a pour voisin que la `ThesisSection`
III.1.2.b « …labélisations indigènes… » ; « Littérature indigène » côtoie le
`Corpus` `1e5246b5…` « Corpus sources indigènes ». Aucun de ces voisins n'est
un concept homonyme : les rattacher serait un choix, pas une résolution.

Les 53 `fuzzy-only` (dont « Gouvernance », « STS », « Crise »…) demandent un
choix de rattachement au cas par cas ; une au moins (« Objets monétaires non
identifiés », P1-0) ne résout que vers la section de thèse homonyme, pas vers
un concept. **Cette sous-question de second rideau n'a pas été tranchée** :
Q6 (a) porte sur les 6 absentes et commande la table d'alias, pas sur la
politique des `fuzzy-only`. Le CSV la signale telle quelle sur P1-0.

**Table d'alias : commandée.** La sous-question de Q6 — « faut-il inscrire
ces correspondances EN→FR et synonymiques dans une table réutilisable ? » —
est répondue **oui**. La table est produite en parallèle sous
`docs/audits/data/entity-alias-table-v1.csv` ; ce dossier ne l'écrit pas et
ne s'en sert pas comme prémisse. Elle a vocation à empêcher que le prochain
résolveur reproduise le faux négatif de la prise P1.

**Une résolution `unique` ne garantit pas que la cible soit du bon genre
(P6).** Cas vérifié : dans P2-0, la référence « II.2 "Pourtant, elles font
monnaie" ! : à l'aune d'un nominalisme "non étatiste" attentif aux usages »
résout en `unique` vers `38e637cc…` — qui est un nœud de type
**`ThesisSection`** (`section_key` = II.2), et non un concept. Un
`quote supports` posé vers cette cible **ferait doublon** avec le
`appears in section` que la même op produit déjà vers II.2. Le contrôle du
**type** de la cible doit donc être ajouté à toute résolution de
`quote_supports_entity_names`, indépendamment du niveau de confiance du
matching de nom. **Arbitré (Q5 (a))** : ce `quote supports` est **supprimé**
— « cela doublerait le lien d'ancrage et confondrait une section avec une
entité de soutien ».

### 5.4 Le cas P3-10 : une citation exacte… du mauvais document

`sq_phase3_CONCL_01` (« Un protocole ne devient CM qu'en tant
qu'infrastructure… ») est **verbatim** — mais dans le « Résumé et mots
clés » liminaire de la thèse (`1_Premières_pages.pdf`, p. 4 imprimée ;
recoupé dans `assets/MD/06_resume.md`), pas dans la conclusion. La cible
`conclu_resume` (« Conclusion — Résumé de la thèse », pp. 332-334) est un
**autre texte**, où cette phrase n'apparaît pas ; le `page_thesis: 5` du
patch trahissait déjà la source liminaire quand la fiche de section annonçait
« p. 332 ». Aucun nœud de section n'existe pour le résumé liminaire.

**Arbitré (Q4 (b)), avec une impasse à signaler.** Maël retient l'op
**seulement** si elle est « localisée honnêtement comme résumé liminaire /
premières pages (p. 4 de `1_Premières_pages.pdf`), pas comme conclusion » ;
il exclut explicitement de **créer un nœud de section** pour elle, et de la
**rattacher à `conclu_resume` si ce n'est pas le même texte**. Or la
vérification ci-dessus établit précisément que **ce n'est pas le même
texte**. Les trois clauses du verdict, prises ensemble, ne laissent donc
aucune cible d'ancrage admissible en v110 : la citation est vraie, sa
localisation est connue, et rien dans le graphe ne peut la porter sans
enfreindre l'une des trois. **Ce point n'est pas tranché ici** — P3-10 reste
à `arbitrage` dans le CSV et retourne à Maël.

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

**Arbitré (Q8 (a)).** Maël choisit la réparation d'abord, « dans un chantier
distinct et mesurable », puis seulement la gravure : « je ne veux pas
installer des citations p. 191 dans une section que le graphe dit commencer
p. 202 ». **C'est la condition générale de tout ce dossier** : aucune action
applicative de cette migration — pas même les 25 `retenir` — n'est autorisée
avant que les `page_start` incohérents ne soient réparés ou, au minimum,
instruits proprement. Le relevé exhaustif des 35 pages de titre reste à faire
et fait partie de ce chantier distinct.

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

Décompte **après inscription des arbitrages** (§ 7). Les libellés ci-dessous
sont ceux du CSV révisé.

**Récupérables sur le fond (25 `retenir`)** : textes vérifiés, sections
existantes et confirmées par la page ; P2-0 les rejoint par Q5 (a). Attention
toutefois : **19 de ces 25 portent une retouche à faire avant gravure**, non
pas sur leur section mais sur la lettre du texte cité ou sur un lien
d'entité. Répartition des motifs (deux ops, P1-13 et P2-2, en cumulent
deux) : **9** pour une coupe non signalée à marquer `[…]` (Q7), **1** pour la
coquille P2-6 à conserver et signaler `[sic]` (Q7), **6** pour une entité
réellement absente dont le `quote supports` est abandonné (Q6), **4** pour
une entité résolue par synonyme ou traduction (Q6), **1** pour la référence
`fuzzy-only` de P1-0 laissée sans politique (Q6, non tranchée). Seules **6
ops** — P1-6, P1-10, P1-16, P2-1, P2-7, P3-1 — sont récupérables sans aucune
retouche de texte ni d'entité ; encore restent-elles soumises au gel de Q8.
(La version précédente comptait P1-0 parmi elles : sa référence
`fuzzy-only` la range désormais du côté des cas à instruire.)

**Récupérables avec correction de section (9 `retenir-avec-correction-de-section`)**,
en deux familles désormais :

- les **5 recentrages prouvés** validés par Q1 (a) — P1-14 → II.3.1 ;
  P1-15 → II.3.1.b ; P2-4 et P2-5 → II.3.2 ; P2-9 → III.3.4. La correction
  est **prouvée par la page et la TOC** et Maël la valide, mais elle est
  **explicitement gelée** tant que les `page_start` du § 5.6 ne sont pas
  réparés ou instruits (P2-4/P2-5 sont le cas qu'il nomme) ;
- les **4 rabattements sur la parente** décidés par Q2 (a) — P3-3 → I.2.1 ;
  P3-4 → I.2.2 ; P3-8 → I.3.3 ; P3-9 → I.3.3. Ces quatre ops ne butaient que
  sur une section jamais existée : le rabattement les sort d'`arbitrage`.

**À faire porter par une SourceQuote existante (5 `completer-l-existante`)** :
P1-8, P3-0, P3-7 et P3-11 par **complément** (Q3.1 (a) — inclusion stricte
vérifiée, l'id et les relations de l'existante sont conservés) ; **P3-6 par
réécriture** (Q3.2 (a)). **Correction de la version initiale (P4)**, toujours
valable : l'inclusion stricte n'est vérifiée que pour P1-8, P3-0, P3-7 et
P3-11. **P3-6 n'en fait pas partie** — l'existante `68d8c0d5…` porte sa
propre condensation (« protocole » pour « protocole de base », « l'équipe »
pour « l'équipe de développement ») et n'est donc pas une sous-chaîne du
candidat ; Maël tranche pour la **réécriture** sur le candidat, « la fidélité
au PDF prime sur la condensation antérieure ». P3-7 rejoint cette catégorie :
son second motif de blocage (section I.3.2b jamais existée) est levé par
Q2 (a).

**Encore ouvertes (2 `arbitrage`)** : **P3-2**, dont Q3.3 (b) impose la
réparation préalable de `47dfac14…` avant toute décision de fusion ; et
**P3-10**, dont les trois clauses de Q4 (b) ne laissent, en l'état du graphe,
aucune cible d'ancrage admissible (§ 5.4).

**À ne graver en aucun cas tels quels** : aucune op n'est fausse sur le
texte, mais **aucune n'est appliquable mécaniquement** : par construction
(résolution par nom, base v96), chaque op passe par au moins une résolution
que ce chantier a dû trancher à la main — et **aucune n'est gravable
maintenant**, le gel de Q8 (a) portant sur les 41.

## 7. Arbitrages rendus par Maël (2026-08-07)

Les huit questions de la version précédente ont reçu une réponse. Elles sont
reproduites ici sous forme de **verdicts**, chacun cité fidèlement puis suivi
de ce qu'il implique pour les ops concernées et de ce qui a changé dans le
CSV. **Ce dossier n'applique rien** : il inscrit. Rappel de la condition qui
domine toutes les autres — **Q8 (a) : aucune action applicative avant
réparation des `page_start`**.

### Q1 — Les 5 recentrages de section prouvés → **(a), conditionné à Q8**

**Verdict.** Les cinq corrections sont validées **sur la foi du texte
imprimé** : P1-14 → `II.3.1`, P1-15 → `II.3.1.b`, P2-4 → `II.3.2`,
P2-5 → `II.3.2`, P2-9 → `III.3.4`. « **Le texte tranche contre la carte de
renumérotation quand ils divergent.** » Mais, dans le même mouvement :
« **je ne veux pas graver ces rattachements tant que les `page_start`
incohérents n'ont pas été réparés ou au moins instruits proprement.** »

**Ce que cela implique.** La carte de renumérotation cesse d'être une
autorité : là où elle diverge du texte, elle a tort, et c'est le relevé
page-à-page du § 5.1 qui fait foi pour la cible. En revanche, la validation
ne vaut pas autorisation de gravure — c'est un **gel conditionnel**, pas un
feu vert.

**Dans le CSV.** Les 5 lignes **conservent** `recommendation =
retenir-avec-correction-de-section` (aucun changement de valeur) ; leurs
`notes` portent désormais la cible validée avec son id v110 et la mention
explicite `GEL CONDITIONNEL ( Q1 + Q8 )`. P2-4 porte en outre la phrase que
Maël a nommée : « je ne veux pas installer des citations p. 191 dans une
section que le graphe dit commencer p. 202 ».

| Op | Cible validée | Id v110 | Ce que disait la carte |
|---|---|---|---|
| P1-14 | `II.3.1` | `d493c4ac…` | II.3.1.a (faux) |
| P1-15 | `II.3.1.b` | `d93cb2ce…` | II.3.1.a (faux) |
| P2-4 | `II.3.2` | `7b3312fe…` | II.3.1.b (faux) |
| P2-5 | `II.3.2` | `7b3312fe…` | II.3.1.b (faux) |
| P2-9 | `III.3.4` | `83985da6…` | — (section annoncée III.3.3, fausse) |

### Q2 — Les 6 sous-sections jamais existées → **(a)**

**Verdict.** Rabattre les 6 ops sur leurs **sections parentes** pour ce
chantier. Ne pas créer les nœuds de niveau 3 maintenant : « **La création
éventuelle du niveau `###` doit devenir un chantier structurel séparé, pas un
effet de bord de cette migration.** »

**Ce que cela implique.** Le sommaire de `graphe.html` et
`section_entities_map.json` ne sont pas touchés par cette migration ; le sort
du nœud orphelin `3ce505bc…` (§ 5.5) reste dans le chantier structurel, pas
ici. Aucune des 6 ops n'est perdue : elles s'ancrent une strate plus haut.

**Dans le CSV.** `target_section` **conserve la clé visée** (`I.2.1b`, etc.,
avec `section_status = not-found`) — c'est la trace de ce que le patch
demandait. Ce sont `recommendation` et `notes` qui portent le rabattement,
avec le parent nommé pour chacune : P3-2 → **I.2.1** (`9cee8e18…`) ;
P3-3 → **I.2.1** ; P3-4 → **I.2.2** (`93f13f18…`) ; P3-7 → **I.3.2**
(`ed2c565c…`) ; P3-8 → **I.3.3** (`46111186…`) ; P3-9 → **I.3.3**.
Quatre d'entre elles quittent `arbitrage` pour
`retenir-avec-correction-de-section` (P3-3, P3-4, P3-8, P3-9) ; P3-7 passe à
`completer-l-existante` (Q3.1) ; P3-2 reste à `arbitrage` (Q3.3).

### Q3 — Les 6 doublons, en trois lots

#### Q3.1 — Les 4 supersets stricts → **(a)**

**Verdict.** P1-8, P3-0, P3-7, P3-11 : **compléter les SourceQuote existantes
avec le texte plus long**.

**Ce que cela implique.** Aucune création de nœud pour ces quatre ops ; l'id
et les relations des existantes `a5278302…`, `8f150b5d…`, `6b1a40ec…` et
`fb610652…` sont conservés, seul leur `quoteText` s'allonge. Le texte
allongé devra porter les marques de coupe exigées par Q7 (les quatre
candidats coupent sans marque).

**Dans le CSV.** P1-8, P3-0 et P3-11 étaient déjà à `completer-l-existante` :
valeur inchangée, notes précisées. **P3-7 passe de `arbitrage` à
`completer-l-existante`** — son second motif de blocage, la section I.3.2b
jamais existée, est levé par Q2 (a).

#### Q3.2 — P3-6 → **(a)**

**Verdict.** Réécrire l'existante `68d8c0d5…` sur le candidat, plus fidèle au
PDF : « **la fidélité au PDF prime sur la condensation antérieure.** »

**Ce que cela implique.** C'est une **réécriture**, non un complément :
l'existante porte sa propre condensation (« protocole » pour « protocole de
base », « l'équipe » pour « l'équipe de développement ») et n'est pas une
sous-chaîne du candidat. Son `quoteText` est remplacé, pas prolongé ; son id
et ses relations restent.

**Dans le CSV.** `recommendation` reste `completer-l-existante` — la valeur
existante couvre le geste « ne pas créer, agir sur l'existante ». **La
sémantique de cette valeur est donc étendue et documentée en tête du
document** (encadré « Sémantique des valeurs de `recommendation` ») : elle
recouvre désormais le *complément* de Q3.1 (4 ops) **et** la *réécriture* de
Q3.2 (P3-6 seule). Les `notes` de P3-6 disent explicitement « RÉÉCRIRE …
( réécriture, pas simple complément ) » pour qu'aucun applicateur ne
confonde les deux gestes.

#### Q3.3 — P3-2 → **(b)**

**Verdict.** Réparer d'abord `47dfac14…` — montage silencieux de **2 146
caractères sautés** entre ses deux fragments, et texte **préfixé du titre de
section** « La phase de "péché" (d'avril 2012 à octobre 2013) » — car il faut
« **ne pas greffer un candidat propre sur une SourceQuote déjà corrompue sans
réparation préalable** ». La décision de fusion vient **ensuite**.

**Ce que cela implique.** Deux chantiers en séquence, pas un : (1) réparation
de `47dfac14…`, qui relève de la relecture des 245 SourceQuotes v110 jamais
re-vérifiées ; (2) alors seulement, décider si le candidat fusionne, coexiste
ou est abandonné. Le chevauchement sans inclusion (seul cas des six) rend de
toute façon impossible toute fusion mécanique.

**Dans le CSV.** `recommendation` **reste `arbitrage`** — la décision de
fusion n'est pas rendue. Les `notes` portent l'exigence de réparation
préalable, la description exacte du défaut de l'existante, et le rabattement
sur I.2.1 décidé par Q2 (a).

### Q4 — P3-10, le résumé liminaire → **(b)**, avec une impasse à signaler

**Verdict.** L'op n'est retenue **que si** elle est localisée honnêtement
comme **résumé liminaire / premières pages** (p. 4 de
`1_Premières_pages.pdf`), **pas comme conclusion** ; **ne pas créer** de nœud
de section pour elle ; **ne pas la rattacher à `conclu_resume`** si ce n'est
pas le même texte.

**Ce que cela implique — et ce qui coince.** Les trois clauses sont
compatibles entre elles, mais pas avec l'état du graphe. Le § 5.4 établit que
`conclu_resume` (« Conclusion — Résumé de la thèse », pp. 332-334) porte un
**autre texte** : la troisième clause interdit donc ce rattachement. La
deuxième interdit d'en créer un. Il ne reste **aucune cible d'ancrage
admissible** en v110. **Ce point n'est pas tranché ici** : l'arbitrage pose
une condition que le graphe ne peut pas satisfaire aujourd'hui, et il
appartient à Maël, non à ce dossier, de dire ce qui l'emporte (abandon de
l'op, ou levée de l'interdiction de créer un nœud).

**Dans le CSV.** `recommendation` **reste `arbitrage`** ; les `notes`
reproduisent les trois clauses du verdict puis signalent l'impasse en toutes
lettres (`IMPASSE SIGNALÉE, NON TRANCHÉE ICI`).

### Q5 — P2-0, l'annonce de II.2 depuis l'intro du chapitre II → **(a)**

**Verdict.** Garder l'op, rattachée à l'introduction du chapitre II ; et
**supprimer le lien `quote supports` vers la section II.2** (`38e637cc…`),
car « **cela doublerait le lien d'ancrage et confondrait une section avec une
entité de soutien** ».

**Ce que cela implique.** Le point technique du § 5.3 (P6) est tranché : une
résolution `unique` ne suffit pas, le **type** de la cible doit être contrôlé.
Ici la cible est un `ThesisSection`, pas un concept ; le `quote supports` est
donc retiré, et l'ancrage passe par le seul `appears in section`.

**Ce que le verdict ne dit pas exactement.** L'option (a) de la question
portait sur « garder le rattachement à **II.2** en tant qu'ancre d'annonce » ;
la formulation retenue parle de « l'**introduction du chapitre II** ». Or
**aucun nœud de section n'existe en v110 pour l'introduction du chapitre II** :
la seule entité disponible à cet endroit est le nœud `Chapter`
« Chapitre II — Dépasser la controverse… » (`5b5935bc…`), qui n'est pas une
`ThesisSection`. Deux lectures restent ouvertes — (i) « introduction du
chapitre II » décrit *où se trouve le texte* et l'ancre reste `II.2` ;
(ii) l'ancre doit changer de cible, ce qui suppose une entité qui n'existe
pas. **Ce dossier ne tranche pas** : il retient la lettre de (a), garde
`target_section = II.2`, et signale le point.

**Dans le CSV.** **P2-0 passe de `arbitrage` à `retenir`** ; les `notes`
portent la suppression du `quote supports` vers `38e637cc…`, la citation du
motif, la localisation p. 146, et le point non couvert ci-dessus.

### Q6 — Les 6 références d'entités réellement absentes → **(a)**, et **table d'alias : oui**

**Verdict.** Ne rien créer ; abandonner les liens de soutien vers les six
entités réellement absentes de v110 : « Individualisme méthodologique »,
« Sociologie économique », « Travail invisible », « Littérature indigène »,
« Terrain hors ligne », « Labélisation indigène ». La sous-question de la
table d'alias reçoit un **oui** : une table EN→FR est commandée, produite en
parallèle sous `docs/audits/data/entity-alias-table-v1.csv`.

**Ce que cela implique.** Les six `quote supports` correspondants
disparaissent des ops, qui restent par ailleurs valides — c'est un
appauvrissement assumé du réseau de soutien, pas un rejet de la citation.
L'option (c) (rattacher au voisin non homonyme) est **écartée** : ni
`b3af43b8…` « Observation participante (hors ligne) », ni `1e5246b5…`
« Corpus sources indigènes », ni la `ThesisSection` III.1.2.b ne reçoivent
ces liens. La table d'alias, elle, doit empêcher que le prochain résolveur
reproduise le faux négatif de la prise P1 (§ 5.3).

**Ce que le verdict ne dit pas exactement.** Deux points restent ouverts.
(i) Les **5 références résolues par synonyme ou traduction** (P1-1, P1-4,
P2-2, P3-11, P3-12 → `a444085b…` et `758e9ca9…`) : la commande de la table
d'alias implique que la correspondance soit **reconnue**, mais Maël n'a pas
dit explicitement si le `quote supports` doit être **posé vers le nœud
français** ou **omis**. (ii) La question de « second rideau » sur les **53
`fuzzy-only`** — rattachement au meilleur candidat ou omission — **n'a pas
été abordée**. Les deux points sont signalés dans les `notes` des lignes
concernées, non tranchés.

**Dans le CSV.** Aucune `recommendation` ne change (les 6 ops porteuses
restent `retenir`) ; 12 lignes portent une mention `Q6 ( a )` : 6 pour un
lien abandonné, 5 pour une résolution par synonyme/traduction, 1 pour la
référence `fuzzy-only` de P1-0.

### Q7 — Politique de fidélité du texte cité → **(d)**

**Verdict.** Restaurer les marques de coupe `[…]` **partout** où le texte est
coupé — les **18 ops** concernées ; ne pas corriger silencieusement la
thèse ; et pour **P2-6**, conserver la coquille imprimée
(« médiatisées **des** dispositifs ») et la signaler `[sic]` si la citation
est gardée. Principe, à citer tel quel :

> « **une citation peut être abrégée, mais jamais coupée sans marque ; et une
> correction silencieuse du texte original est à proscrire.** »

**Ce que cela implique.** C'est la seule décision qui touche la **lettre** du
texte à graver, et elle s'applique à toutes les ops sans distinction de
recommandation — y compris à l'intérieur des `quoteText` allongés ou réécrits
de Q3.1 et Q3.2. Le cas le plus lourd reste **P2-8**, dont la coupe
silencieuse supprimait « et sans être à l'époque formellement encadré » — une
réserve de fond — et perdait les guillemets de « huis clos » : les deux sont
à rétablir. Le principe, énoncé en termes généraux, s'applique aussi à la
seconde coquille imprimée relevée par la vérification (« de leur critiques »,
p. 191, dans P2-4), pour laquelle le CSV note la conservation `[sic]` **au
titre du principe**, Maël n'ayant nommé que P2-6.

**Dans le CSV.** Aucune `recommendation` ne change. **19 lignes** portent une
mention `Q7 ( d )` : les 18 ops à coupe non signalée (P1-2, P1-7, P1-8,
P1-12, P1-13, P2-0, P2-2, P2-3, P2-4, P2-8, P2-9, P3-3, P3-5, P3-6, P3-7,
P3-8, P3-9, P3-11) et P2-6 pour la coquille. P1-16, dont la coupure était
déjà marquée `[...]`, est notée conforme.

### Q8 — Les `page_start` incohérents de v110 → **(a)**

**Verdict.** Réparer les `page_start` incohérents **d'abord**, dans un
**chantier distinct et mesurable**, puis seulement graver les SourceQuote :
« **Je ne veux pas installer des citations p. 191 dans une section que le
graphe dit commencer p. 202.** »

**Ce que cela implique — conséquence majeure.** **Toute action applicative de
cette migration est désormais conditionnée à la réparation préalable des
`page_start`.** Cela vaut pour les 41 ops, y compris les 25 `retenir` et les
6 récupérables sans retouche : le gel ne porte pas sur la qualité des
citations, qui est établie, mais sur la lisibilité de leur ancrage. L'ordre
imposé est donc :

1. réparation (ou instruction documentée) des `page_start` — chantier
   distinct, à mener comme v108/v109, avec le **relevé exhaustif des 35 pages
   de titre** encore à faire (16 incohérences sont un plancher, pas un
   plafond, § 5.6) ;
2. réparation de `47dfac14…` (Q3.3) ;
3. réécriture éventuelle des zips en patch candidat conforme, intégrant les
   huit verdicts ;
4. préflight ;
5. gravure.

**Dans le CSV.** Les **41 lignes** portent la mention
`Q8 ( a ) : gravure gelée jusqu'à réparation des page_start`. Les 5 lignes de
Q1 portent en outre `GEL CONDITIONNEL ( Q1 + Q8 )`.

### Ce que les arbitrages ne couvrent pas

Trois cas du CSV ne sont pas exactement couverts par les verdicts. Ils sont
signalés dans les `notes` par la mention `Non couvert` ou `IMPASSE` et **ne
sont pas tranchés ici** :

1. **P3-10 (Q4)** — les trois clauses du verdict, appliquées à l'état réel du
   graphe, ne laissent aucune cible d'ancrage admissible. Voir Q4 ci-dessus.
2. **P2-0 (Q5)** — « rattachée à l'introduction du chapitre II » ne
   correspond à aucun nœud `ThesisSection` de v110 ; l'ancre reste `II.2`
   comme le dit la lettre de l'option (a), à confirmer.
3. **Les liens de soutien vers les nœuds résolus par synonyme (Q6)** — la
   table d'alias est commandée, mais le sort du `quote supports` lui-même
   (posé vers le nœud français, ou omis) n'est pas dit ; et la politique des
   **53 `fuzzy-only`** n'a pas été abordée.

S'y ajoutent deux points hérités que les arbitrages ne mentionnent pas :
la **triple cible sectionnelle de P1-11** (C.2 + C.2.a + C.2.b), laissée en
l'état ; et la **seconde cible erronée de P3-11** (`conclu_aceph`, alors que
le passage est entièrement dans `conclu_infra`), qui ne figure pas parmi les
5 recentrages de Q1 et n'a donc reçu aucun arbitrage.

### Tableau récapitulatif — les 6 recommandations qui changent

| Op | Avant | Après | Motif |
|---|---|---|---|
| P2-0 | `arbitrage` | **`retenir`** | Q5 (a) : op gardée, `quote supports` vers `38e637cc…` supprimé |
| P3-3 | `arbitrage` | **`retenir-avec-correction-de-section`** | Q2 (a) : rabattue sur I.2.1 |
| P3-4 | `arbitrage` | **`retenir-avec-correction-de-section`** | Q2 (a) : rabattue sur I.2.2 |
| P3-7 | `arbitrage` | **`completer-l-existante`** | Q3.1 (a) : compléter `6b1a40ec…` ; Q2 (a) lève le blocage de section |
| P3-8 | `arbitrage` | **`retenir-avec-correction-de-section`** | Q2 (a) : rabattue sur I.3.3 |
| P3-9 | `arbitrage` | **`retenir-avec-correction-de-section`** | Q2 (a) : rabattue sur I.3.3 |

Les 35 autres lignes gardent leur valeur ; seules leurs `notes` changent, pour
porter le verdict qui les gouverne.

## 8. Le sort des zips — après arbitrage

Trois issues étaient posées par le préflight. Les arbitrages du § 7 ne
tranchent **pas** le sort des zips eux-mêmes : Maël n'a pas dit d'écrire le
patch candidat maintenant. Ce qu'ils font, c'est **fixer le contenu que
devrait avoir une réécriture éventuelle**, et **en repousser le moment**.

- **Les zips restent archivés comme source.** Cette issue est justifiée dans
  tous les cas et les arbitrages ne la remettent pas en cause : même si leur
  contenu est repris, les zips ne doivent plus jamais servir de source
  d'application directe (4 misroutes de sections sur 6 clés sensibles,
  6 cibles inexistantes, 18 coupes silencieuses, 1 correction de coquille —
  toutes désormais documentées et arbitrées). Le zip `foundation`, sans ops,
  n'a que valeur documentaire. **À archiver au même titre : l'idée
  d'appliquer ces ops avec l'outillage existant** —
  `scripts/apply-sourcequote-phases.mjs` et ses modules ne détecteraient
  aucun des 6 doublons et ne verraient pas III.3 (§ 5.7).
- **Réécriture en patch candidat canonique : non décidée, mais désormais
  spécifiée.** Les chiffres la soutiennent — **39 des 41 ops** sont
  aujourd'hui déterminées (25 `retenir` + 9 `retenir-avec-correction-de-section`
  + 5 `completer-l-existante`), les 2 restantes étant P3-2 et P3-10. Une
  réécriture conforme au contrat (`grc20-candidate-patch-contract-v1.md`)
  résorberait d'un coup les trois vices de forme rédhibitoires des zips :
  dialecte hors contrat, résolution par nom, base v96 avec clés
  pré-migration. **Mais Maël n'a pas demandé d'écrire ce patch**, et ce
  dossier ne le fait pas. Si elle est décidée, cette réécriture devra
  intégrer les huit verdicts :
  1. les **5 recentrages** de Q1 (a), aux ids v110 du tableau du § 7 ;
  2. les **6 rabattements** sur section parente de Q2 (a), sans création
     d'aucun nœud de niveau 3 ;
  3. les **4 compléments** et la **1 réécriture** de Q3.1/Q3.2, opérés sur
     les SourceQuote existantes (aucun nœud nouveau), P3-2 restant hors
     patch tant que `47dfac14…` n'est pas réparée (Q3.3) ;
  4. les **marques de coupe `[…]`** restaurées dans les 18 `quoteText`
     concernés et la coquille de P2-6 conservée avec `[sic]` (Q7) — y compris
     à l'intérieur des textes allongés ou réécrits du point 3 ;
  5. les **6 `quote supports` abandonnés** vers les entités absentes (Q6) et
     le **`quote supports` retiré** vers `38e637cc…` dans P2-0 (Q5) ;
  6. les trois points **non couverts** du § 7, qui doivent revenir à Maël
     avant et non pendant la réécriture.
- **Abandon partiel** : le périmètre s'est réduit. Les 6 doublons ne sont
  plus candidats à l'abandon (Q3.1 et Q3.2 les versent tous vers l'existante,
  Q3.3 met P3-2 en attente) ; ne reste discutable que **P3-10**, dont Q4 (b)
  laisse le sort ouvert. Un abandon total serait coûteux : 39 ops apportent
  des citations vérifiées verbatim sur des sections identifiées
  `CRITICAL_ZERO` par le patch d'origine, et ce travail de vérification page
  à page est maintenant fait, consigné et arbitré.

Dans tous les scénarios, l'arbitrage **Q8 du préflight** (à ne pas confondre
avec la Q8 du § 7 ci-dessus) demeure : **aucun applicateur avant les réponses
du § 7** — elles sont maintenant rendues, ce qui lève cette condition-là. La
condition qui la remplace est plus stricte : **Q8 (a) — aucune action
applicative, pas même un patch candidat gravé, avant réparation ou
instruction documentée des `page_start`** (§ 5.6). L'ordre arrêté est celui
du § 7-Q8 : `page_start` → `47dfac14…` → patch candidat → préflight →
gravure.

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
- pas de réécriture des zips en patch candidat — et **toujours pas**, après
  les arbitrages : Maël n'a pas demandé de l'écrire (§ 8).

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

Ajouts de l'inscription des arbitrages du 2026-08-07 — ce que cette passe n'a
**pas** fait non plus, et ce qu'elle interdit désormais :

- **rien n'a été appliqué.** Le graphe `grc20-these-mael-rolland-v110.json`
  est inchangé, aucune SourceQuote n'a été créée, complétée, réécrite ni
  supprimée, aucun lien de section ni `quote supports` n'a été posé ou
  retiré, aucun applicateur n'a été écrit ni exécuté, aucun patch n'a été
  généré. Les deux seuls fichiers touchés sont
  `docs/audits/data/sourcequote-migration-verification-v1.csv` et le présent
  document ;
- **aucun nœud de niveau 3 créé** (Q2 (a)), aucun nœud de section pour le
  résumé liminaire (Q4 (b)), aucune des 6 entités absentes créée (Q6 (a)) :
  les rabattements et abandons sont **inscrits**, pas opérés ;
- **aucune marque de coupe restaurée** : les 18 `quoteText` à corriger et la
  coquille de P2-6 sont désignés op par op dans le CSV, mais aucun texte n'a
  été réécrit — Q7 dit *quoi* faire, ce dossier ne le fait pas ;
- **gel explicite** : par Q8 (a), toute action applicative de cette migration
  est suspendue jusqu'à réparation — ou instruction documentée — des
  `page_start` incohérents. Le gel porte sur les **41 ops**, y compris celles
  dont la recommandation est `retenir`. Aucune des passes suivantes ne doit
  lire ce dossier comme une autorisation de graver ;
- **trois cas non tranchés** ont été signalés et laissés à Maël plutôt que
  décidés en son nom (§ 7, « Ce que les arbitrages ne couvrent pas ») : P3-10,
  la cible d'ancrage de P2-0, et le sort des `quote supports` vers les nœuds
  résolus par synonyme ainsi que la politique des 53 `fuzzy-only`. S'y
  ajoutent la triple cible de P1-11 et la seconde cible erronée de P3-11, que
  les arbitrages ne mentionnent pas ;
- **la table d'alias EN→FR n'a pas été écrite ici** : elle est commandée par
  Q6 et produite en parallèle sous
  `docs/audits/data/entity-alias-table-v1.csv` ; ce dossier la cite comme
  destination, sans s'en servir comme prémisse.
