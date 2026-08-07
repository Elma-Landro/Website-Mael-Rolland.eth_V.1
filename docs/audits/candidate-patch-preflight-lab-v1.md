# Candidate Patch Preflight Lab v1 — l'infrastructure de préflight construite, trois candidats mesurés, aucun appliqué

**Date** : 2026-08-07
**Graphe** : `grc20-these-mael-rolland-v110.json` (**inchangé** par ce chantier)
**Branche** : `claude/file-upload-branch-check-jw4cng`
**Mode agent** : A (préflight) — **aucun patch appliqué, aucun graphe écrit**, aucun fichier de patch modifié ni créé
**Outils** : `scripts/preflight_candidate_patches.py` (validateur, lecture seule, déterministe)
**Données** : `docs/audits/data/candidate-patch-inventory-v1.csv` (32 lignes) · `docs/audits/data/candidate-patch-preflight-report-v1.json` (simulation à blanc)
**Prédécesseurs** : `grc20-bibliographie-reconciliation-lab-v1.md` (2026-08-07, producteur des 3 candidats), `grc20-candidate-patch-contract-v1.md` (2026-08-07, le contrat de forme)

> Contrôle de recoupement : avant intégration, les chiffres suivants ont été
> re-vérifiés directement contre les livrables commités — 32 lignes de
> l'inventaire dont 11 `applique` / 14 `historique` / 7 `candidat-non-applique`
> (recomptage du CSV) ; 2 293 entités et 20 207 relations dans v110 (recomptage
> du graphe) ; 338 entrées au registre, `duplicateOf` et `reviewStatus` à
> `count` 3 et `domain` `[CrisisEvent, InfrastructureEvent]`, `source_entry`
> absente, `_meta.source_graph` = v109 (lecture de
> `grc20-properties-registry-v1.json`) ; 156 / 38 / 10 ops dans les trois
> candidats (recomptage des fichiers) ; verdict **42 OK / 4 AVERTISSEMENT /
> 0 BLOQUANT, code de sortie 0** (ré-exécution du validateur dans son état
> final, après les durcissements de revue — les décomptes antérieurs, 36
> puis 39 OK, correspondaient aux états intermédiaires du validateur : le
> nombre de contrôles OK croît avec chaque contrôle ajouté, le verdict
> 4 AVERTISSEMENT / 0 BLOQUANT est, lui, invariant) ;
> 11 677 relations porteuses de `page_approx` dans v110 (recomptage) ; les
> 3 porteurs `duplicateOf` de v110 sont bien `ee7277…`, `7f8009…`, `22c507…`
> (recomptage). Les seize cas négatifs de l'inventaire du § 4 ont tous été
> prouvés en code de sortie 1 (ou 2 pour l'invocation illisible).

---

## 1. Le problème

Trois patchs candidats issus du Bibliographie Reconciliation Lab (PR #112)
attendent l'arbitrage de l'auteur :
`patch_candidate_bibliographie_retypes_v1.json` (10 ops),
`patch_candidate_bibliographie_duplicates_v1.json` (156 ops),
`patch_candidate_bibliographie_missing_nodes_v1.json` (38 ops). Tous trois
portent la policy `CANDIDATE — NOT APPLIED — AUTHOR ARBITRATION REQUIRED` et
aucun de leurs effets n'est dans v110 (vérifié : 0/10, 0/156, 0/38 —
inventaire, lignes des trois candidats).

Mais avant même de pouvoir instruire ces trois-là, le dépôt manquait de tout
ce qui permet d'instruire un patch en général :

- **aucun inventaire fiable** des fichiers de patch — le seul existant,
  `workshop/patches/PATCH_AUDIT.md` + `patch-inventory.json` (2026-04-04),
  était prudentiel par construction : statut `unknown` par défaut, aucune
  vérification empirique d'application ;
- **aucun contrat de forme** — six dialectes incompatibles coexistent, et un
  patch a déjà été émis dans un hybride ne correspondant à aucun (incident C3,
  `grc20-dedup-events-audit-v1.md`) ;
- **aucun validateur** — chaque applicateur `make_vNNN` recodait sa propre
  validation, avec des sévérités divergentes ;
- **aucune mesure d'impact** — personne ne savait dire ce que l'application
  des candidats ferait au graphe, au registre des propriétés, à la CI ou au
  runtime avant de l'avoir tentée.

Ce chantier construit cette **infrastructure de préflight** — inventaire,
contrat, validateur, simulation, analyse registre/CI — et s'arrête là :
l'application elle-même n'en fait pas partie. Cinq lots de travail ont livré ;
le présent document les intègre.

## 2. L'inventaire — 32 artefacts, trois statuts prouvés

`docs/audits/data/candidate-patch-inventory-v1.csv` recense **32 artefacts de
patch** (26 `patch*.json` de racine, `new_relations_patch.json`, 2 fichiers de
`patches/`, 3 zips de `Migration/`), chacun classé sur preuve :

| Classement | Nombre | Preuve exigée |
|---|---:|---|
| `applique` | 11 | script applicateur + note de space + vérification empirique effet par effet dans v110 |
| `historique` | 14 | contenu intégré de longue date à v110 (triplets/attributs retrouvés), sans script de traçabilité pour la plupart |
| `candidat-non-applique` | 7 | zéro effet retrouvé dans v110 |

Les 7 candidats : les 3 bibliographiques de la PR #112, les 3 zips SourceQuote
de `Migration/`, et `patches/grc20_anchor_overrides_targeted.json`.

**Découvertes de l'inventaire** (colonnes `justification` du CSV) :

- **Trois zips SourceQuote dans `Migration/`**
  (`sourcequote_effective_patch_phase1/2/3.zip`) : 18 + 10 + 13 = **41 ops
  `ADD_SOURCEQUOTE_WITH_SECTION_LINKS`** dans un dialecte ad hoc à résolution
  par noms (aucun `entityId`), préparés hors dépôt avec pour cible déclarée
  v96+. Il n'existe **aucun applicateur** pour ces zips :
  `scripts/apply-sourcequote-phases.mjs` est un **outil de simulation et
  d'inspection** — même avec `--write`, il simule en mémoire et imprime un
  rapport, sans jamais écrire de graphe (aucun `writeFile` dans le script
  ni ses modules, établi par la revue hostile). **Un véritable applicateur
  en écriture devra exister avant toute application des trois zips** — et
  traiter le risque de doublon ci-dessous.
  Aucune trace en v110 (0 titre, 0 `seed_id` retrouvés) — **sauf** en
  phase 3, où **3 extraits coïncident avec des citations déjà présentes** :
  risque de doublon si appliqué tel quel. Citations à vérifier contre le PDF
  avant toute injection.
- **`patches/grc20_anchor_overrides_targeted.json`** : 10 entrées
  (9 `safe_fix` + 1 `proposed_review`) dans une structure **hors de tous les
  dialectes** du dépôt, base déclarée **v93**, posant des clés
  (`primaryChapter`, `secondaryChapters`) inconnues du registre et de v110
  (0 porteur). Le réancrage par attribut qu'il propose est antérieur et
  concurrent au mécanisme de charges réaligné en v108–v109 : **probablement
  périmé**, à réévaluer entièrement avant toute application.
- **12 patchs non répertoriés par le brief initial** du chantier ont été
  trouvés et classés (dont les 3 zips, les 2 fichiers de `patches/`, les
  lots `batch1-3` et les sorties de `generate_*.mjs`).
- **`entityIds` morts dans les historiques, sans incidence** : quelques
  entités cibles ont disparu depuis l'application (1 pour `patch_1b`, 7 pour
  `patch_2b`, 6 pour `patch_4`, 6 pour `patch_5`) — le contenu restant est
  intégré, rien à corriger, mais tout rejeu naïf échouerait.
- **`page_approx` hors registre, à bon droit** : l'attribut est porté par
  **11 677 relations** de v110 (recompté), et le registre des propriétés ne
  décrit que les attributs **d'entités** — ce n'est pas un trou du registre,
  c'est son périmètre. La CI ne lit pas non plus les attributs de relations
  (§ 6).

Cet inventaire **remplace** l'inventaire prudentiel de `workshop/patches/`
comme référence : là où celui-ci s'interdisait de conclure (`unknown` par
défaut), le CSV tranche chaque ligne sur vérification empirique.

## 3. Le contrat — six dialectes constatés, un seul prescrit

`docs/audits/grc20-candidate-patch-contract-v1.md` fait le recensement des
dialectes (six, nommés A à F, avec trois formes incompatibles du seul
`ADD_RELATION`) et huit incohérences de forme constatées, puis prescrit un
contrat minimal dont chaque clause est déjà satisfaite par au moins un patch
du dépôt. Le cœur en cinq points :

1. **Enveloppe** : exactement `_meta` + `ops` ; `_meta` porte `patch_id`
   unique dans le dépôt, `source_graph`, `generated`, `description`, `policy`
   (pour un candidat : `CANDIDATE — NOT APPLIED — AUTHOR ARBITRATION
   REQUIRED` en tête), `skipped` + `skipped_count` motivés, et des comptes
   recomptables mécaniquement.
2. **Dialecte d'ops unique** : celui de `patch_18`/`patch_19` consommé par
   `make_v110` (`ops`, clé `type`, `entityId`/`attributeId`, valeurs typées
   `{type, value}`) — c'est aussi celui que le graphe journalise nativement
   dans sa clé de tête `ops` (274 entrées dans v110).
3. **Validation au dépôt** : tout `entityId` et tout id de type doivent
   exister dans `source_graph` ; toute clé d'attribut nouvelle ou hors domaine
   doit déclarer son statut registre dans `_meta` (`registry_note`).
4. **Interdits** : s'auto-appliquer, mélanger les dialectes (leçon C3),
   préassigner des `entityId` en `CREATE_ENTITY`, toucher aux relations sous
   couvert de marquage, se dire conforme à un `source_graph` non vérifié.
5. **Portée** : les patchs **futurs** seulement. Les patchs historiques
   dérogatoires sont des archives de ce qui a été appliqué — les réécrire
   falsifierait l'histoire du dépôt sans changer un octet du graphe.

Nuance de lecture à conserver : le contrat déclare
`patch_candidate_bibliographie_missing_nodes_v1.json` **conforme** au titre de
patch *descriptif* — conforme ne veut pas dire applicable, et le validateur le
rappelle (C09, § 4).

Divergence de périmètre, documentée sans être tranchée : le contrat annonce
« 28 fichiers de patch en six dialectes » alors que sa propre table de
dialectes en liste 27 et que la racine compte 26 `patch*.json` +
`new_relations_patch.json` ; l'inventaire, lui, couvre 32 artefacts dont
plusieurs **hors** des six dialectes (les 3 zips au dialecte ad hoc,
`anchor_overrides_targeted` sans clé d'opération, le reçu v97 de `patches/`).
Les deux recensements sont justes chacun dans son périmètre ; le comptage
d'ensemble de référence est celui de l'inventaire (32).

## 4. Le validateur — douze contrôles, et la preuve qu'il refuse

`scripts/preflight_candidate_patches.py` (stdlib seule, lecture seule, sortie
déterministe) passe douze contrôles C01–C12 sur chaque
`patch_candidate_*.json`, chacun rendant OK / AVERTISSEMENT / BLOQUANT :
parse JSON (C01) ; `_meta` complet (C02) ; policy candidate correctement
marquée (C03) ; `source_graph` présent au dépôt et à jour (C04) ; comptes
déclarés = réels (C05) ; entités ciblées existantes (C06) ; ids de types
connus et cohérents avec `typeNames` (C07) ; clés d'attribut face au registre
— absence ou domaine trop étroit (C08) ; `CREATE_ENTITY` sans applicateur et
sans id préassigné (C09) ; collisions de noms, contre le graphe et dans le lot
(C10) ; invariants `duplicateOf` — cible existante, aucune chaîne, un seul
marquage (C11) ; croisements inter-patchs du lot (C12). Codes de sortie :
0 = aucun bloquant, 1 = au moins un bloquant, 2 = erreur d'invocation.

**Verdict sur les trois candidats réels** (ré-exécuté sur l'état final du
validateur, après durcissements de revue) : **42 OK / 4 AVERTISSEMENT /
0 BLOQUANT, sortie 0**. Les quatre avertissements ne sont pas des surprises : ce sont exactement
les préalables déjà documentés par les `_meta` des patchs et le prédécesseur —

- C08 ×2 (duplicates) : domaine du registre de `duplicateOf` et
  `reviewStatus` — `[CrisisEvent, InfrastructureEvent]` — à étendre aux
  4 types cibles (`AcademicWork`, `GreyLiterature`, `IndigenousLiterature`,
  `Reference`), 78 ops chacune ;
- C08 ×1 (missing_nodes) : `source_entry` absente du registre, extension
  requise avant application (38 ops) ;
- C09 ×1 (missing_nodes) : 38 `CREATE_ENTITY` non applicables en l'état —
  aucun `scripts/make_*.py` ne consomme `CREATE_ENTITY` (balayage dynamique).

**Seize cas négatifs prouvent que le script refuse** les patchs mal formés
(code de sortie 1, ou 2 quand c'est l'invocation qui est illisible) —
inventaire complet, accumulé sur les trois passes de revue :
policy absente, tronquée, en minuscules, ou de type liste (C03) ;
`entityId` mort (C06) ; compte déclaré faux (C05) ; collision `SET_NAME`
avec un nom déjà porté, y compris à espaces surnuméraires (C10 — le motif
d'échec historique de `make_v110`) ; chaîne `duplicateOf` A→B→C et cycle
A→B→A (C11 — l'incident « Mining pools » C4) ; `entityId` préassigné sur
`CREATE_ENTITY` (C09) ; patch vide `{}` (C02) ; op d'un type hors périmètre
ou sans type (C06) ; `ops` qui n'est pas une liste, ou dont un élément
n'est pas un objet (C01 structurel) ; champ `_meta` ou champ d'op mal typé
(C02/C06 forme) ; fichier en UTF-8 invalide (C01 en lot, sortie 2 via
`--graph`). Chaque cas a été fabriqué hors dépôt et rejoué : sortie non
nulle confirmée à chaque fois.

**Découverte du croisement (C12)** : aucune incohérence inter-patchs réelle
dans le lot. Le croisement pressenti autour de la famille Wood est au niveau
de la **famille** bibliographique, pas de l'entité : aucune entité n'est à la
fois retypée et marquée doublon, aucun canonique d'un patch n'est cible d'un
autre.

Deux choix de sévérité du validateur méritent d'être dits, car le contrat
(§ 2.6) montre que le dépôt a connu deux régimes : C04 rend un simple
AVERTISSEMENT quand `source_graph` n'est pas le graphe le plus récent (là où
`make_v110` refuse tout décalage), et C08 rend AVERTISSEMENT — jamais
BLOQUANT — pour une clé hors registre, parce qu'un **candidat** a le droit de
proposer une clé nouvelle ; c'est l'**application** qui, elle, serait bloquée
par la CI (§ 6). La sévérité de l'applicateur futur reste à arbitrer.

## 5. La simulation à blanc — ce que l'application ferait, mesuré sans l'avoir faite

`docs/audits/data/candidate-patch-preflight-report-v1.json` applique les trois
patchs **en mémoire** sur une copie de v110, séparément puis cumulativement.
Aucun graphe écrit : le rapport est la seule écriture.

**Les deltas** (clé `simulations.cumule`) :

| Mesure | Avant | Après | Delta |
|---|---:|---:|---:|
| Entités | 2 293 | 2 331 | **+38** (créations de missing_nodes seules) |
| Relations | 20 207 | 20 207 | **0** (aucun patch n'en pose) |
| Ops appliquées | — | 204 | 156 + 38 + 10 |
| Entités existantes touchées | — | 84 | 78 (duplicates) + 6 (retypes) |

Par type : `Person` +6 (les retypes), `Reference` +32 net (+38 créations,
−6 retypages), `GreyLiterature` +18, `IndigenousLiterature` +16,
`AcademicWork` +4 (co-typages des créations).

**Ce que la simulation n'a pas trouvé** — et qu'il fallait chercher :

- **aucune collision de nom** créée (`collisions_noms_creees` vide, patch par
  patch et en cumulé) ;
- **aucune chaîne `duplicateOf`** A→B→C, aucun porteur écrasé, et **aucun
  croisement** avec les 3 porteurs `duplicateOf` déjà présents dans v110
  (les entités patch_10 : `ee7277…`, `7f8009…`, `22c507…` — verdict « aucun
  croisement ») ;
- **zéro référence runtime par nom-clé** (formulation corrigée par la
  revue hostile) : grep des noms, ids et clés de citation des entités
  touchées dans `narrative-anchors`, `story-presets`,
  `graphe.story-helpers`, `graphe.html`, `lecteur.html` — aucune référence
  par identifiant ni par nom-clé (`primaryEntityName`, `focusNodes`).
  **Une occurrence en prose de citation existe** : « Kavanagh et
  Miscione 2017 » (`2986a9e1…`, marquée `duplicateOf` par le candidat)
  apparaît dans le `quoteText`/`storyBody` de `narrative-anchors.json`
  (ancre 35) — le marquage ne casse rien, mais une **fusion** future
  toucherait un nom présent dans du texte affiché au lecteur. Au passage :
  le canonique visé porte un espace final dans son nom v110
  (« Kavanagh & Miscione 2017␣ »), coquille à corriger lors de la fusion.

**Les deux chiffres registre** (clé `attributs_nouveaux`) :

1. `duplicateOf` et `reviewStatus` passeraient de **3 à 81 porteurs**
   chacun : le registre deviendrait **menteur de 78 sur `count` et de
   4 types sur `domain`** — et la **CI resterait silencieusement verte**,
   car elle ne vérifie ni l'un ni l'autre (§ 6) ;
2. `source_entry` passerait de **0 à 38 porteurs** : clé absente du registre,
   donc **CI bloquante** (`scripts/check_graph_integrity.py`) sur tout graphe
   la portant.

**Le risque de séquencement des 38 créations** : les 38 nœuds seraient créés
**orphelins de relations ET de citation** — le patch ne pose aucun `cited in`
ni `appears in section`, alors que la justification du CSV
`bibliographie-entrees-sans-noeud-v1.csv` atteste que les 38 œuvres sont
citées dans le corps de la thèse. Un graphe publié entre la création et la
pose des relations exposerait 38 nœuds isolés : **la pose des `cited in` doit
vivre dans le même `make_vNNN`** que la création.

**Vérifications d'exactitude** : les `_meta` des trois patchs sont exacts
(comptes, skipped) — le **tableau des prises est vide** (`"prises": []`).
Note technique pour l'applicateur réel : v110 encode « aucun attribut »
tantôt `[]`, tantôt clé absente — un applicateur devra normaliser, la
simulation l'a fait en mémoire.

Une hétérogénéité assumée à consigner : après application, `reviewStatus`
porterait deux vocabulaires (`duplicate-pending-merge` hérité de patch_10,
`pending-author` des candidats). La simulation la signale
(`heterogeneite: true`) ; l'analyse registre (§ 6.2) établit qu'elle ne crée
aucun conflit de code — les deux constats sont complémentaires, la
documentation du champ `vocabulary` régénéré ferait foi.

## 6. Registre / CI — ce que le registre déclare, ce que la CI vérifie vraiment

**État des lieux vérifié.** `grc20-properties-registry-v1.json` est un objet
`{_meta, entries}` de **338 entrées** ; chaque entrée porte `key`, `id`
(md5 de `'grc20-property-v1|'+key`), `valueType`, `language`, `domain`,
`count`, `status` (structural/editorial/deprecated), `readBy`, `vocabulary`,
`derivedFrom`, `notes` (+ `supersededBy` pour les 3 dépréciées). Son `_meta`
déclare `source_graph: grc20-these-mael-rolland-v109.json`, date 2026-08-06,
`generated_by: scripts/build_properties_registry.py` — `count` et `domain`
mesurés sur **v109 tel quel**, `valueType`/`language`/`vocabulary` calculés
après application **en mémoire** de patch_19. `CLAUDE.md` l'établit comme
invariant de CI.

**Ce que la CI contrôle réellement** (`scripts/check_graph_integrity.py`,
appelé par `check.yml`) : côté registre, **un seul contrôle bloquant** — toute
clé d'attribut d'entité du graphe **courant** absente du registre
(l. 172-176, 223-224). Les entrées du registre sans occurrence sont
signalées, jamais bloquantes ; les clés dépréciées encore présentes ne
bloquent pas. **`domain`, `count`, `valueType`, `vocabulary` ne sont JAMAIS
vérifiés.** Le contrôle ne lit que les attributs d'entités, jamais ceux des
relations. `check.yml` valide déjà la syntaxe JSON des
`patch_candidate_*.json` (glob `*.json` racine), rien d'autre les concernant.

### 6.1 Attributs déjà déclarés et suffisants : aucun

- **retypes** : aucun attribut posé ; impact indirect vérifié — les 6 entités
  retypées portent `chapter`, `communityRole`, `description`, et `Person`
  figure déjà dans le `domain` de ces trois entrées. Seul patch neutre pour
  le registre.
- **duplicates** : `duplicateOf` (78) + `reviewStatus` (78) — déclarés, mais
  domaine et count faux après application (§ 6.2).
- **missing_nodes** : `source_entry` ×38 — absente du registre (§ 6.3).

### 6.2 Déclarés mais domaine trop restreint : `duplicateOf` et `reviewStatus`

Entrées actuelles : `duplicateOf` (id `26a1cb779802d673fe8ed4e11c8b380e`),
`reviewStatus` (id `519fdfcc579905e7bab12918df1e6f2b`) — `domain`
`[CrisisEvent, InfrastructureEvent]`, `count` 3, `status` structural,
`readBy` `[make_v105_dedup_events.py, verif_doublons.py]`, `vocabulary`
`null`. Porteurs actuels dans v110 : les 3 entités patch_10 (Mining pools
`ee7277…`, Mining pools emergence `7f8009…`, Scaling Debate `22c507…`),
`reviewStatus` = `duplicate-pending-merge`.

Après application : 78 nouveaux porteurs (Reference 76, AcademicWork 24,
IndigenousLiterature 9, GreyLiterature 5, co-typages compris). Le registre
deviendrait faux sur `domain` (4 types manquants) et `count` (3 au lieu
de 81) ; `vocabulary` de `reviewStatus` deviendrait calculable
(`["duplicate-pending-merge", "pending-author"]`) en restant `null` au
fichier. **La CI ne casse pas : le mensonge est silencieux — le cas le plus
dangereux.**

Cohabitation `pending-author` / `duplicate-pending-merge` :
`verif_doublons.py` ne **lit** jamais ces clés depuis le graphe (générateur :
filtre sur les types événements l. 96, écrit patch_10 l. 251-256) — les
porteurs bibliographiques lui sont invisibles, aucun conflit. Son invariant
« un seul `duplicateOf` » (l. 206-209) est interne à sa génération. Réserves :
(a) les invariants « pas de chaîne » et « `duplicateOf` ⇒ `reviewStatus` » ne
sont vérifiés que par `make_v105` (l. 132-143), one-shot v104→v105 qui ne
sera pas rejoué — **les porteurs bibliographiques n'auront AUCUN contrôleur**
tant qu'on n'en ajoute pas ; vérifié sur le patch candidat : 78 marqués,
71 cibles, zéro chaîne, zéro écrasement, tous ids dans v110 ; (b) un rejeu de
`verif_doublons.py` écrase par défaut `patch_10_dedup_events.json`
(l. 34-35).

### 6.3 Absente : `source_entry` — et la régénération n'est pas presse-bouton

Absente des 338 keys — tout graphe courant la portant serait bloqué en CI.
`build_properties_registry.py` découvre les clés **depuis le graphe**
(l. 254-260, pas de liste blanche) : `source_entry` entrerait automatiquement
par régénération **après** application, avec `count` 38, `domain` = les
4 types des nœuds créés, id `4fafa2650e0b7f2a4bb2474b6669d3e6` (id_scheme),
`status` editorial tant qu'aucun code ne la nomme (`read_by` ne couvre que
`*.html`/`*.js`/`*.mjs` + `scripts/`) — structural dès que le futur
`make_vNNN` la nommera.

**Mais** la régénération n'est pas presse-bouton (non dit par les
`registry_note` des patchs) : `build_properties_registry.py` a
`SOURCE = 'grc20-these-mael-rolland-v109.json'` **codé en dur** (l. 39),
`DATE_AUDIT` figée (l. 42), exige patch_19 sous peine d'échec (l. 265-268)
alors que patch_19 est déjà appliqué depuis v110, et son `_meta.conventions`
décrit v109. Régénérer « tel quel » décrirait encore v109. **Révision du
script requise** (`SOURCE` → graphe courant ou `--source` ; sort des
3 entrées `deprecated` : construites depuis « avant », elles
**disparaîtraient** d'un registre régénéré sur v111 — inoffensif pour la CI,
perte d'historique documentaire à assumer). Décision d'édition = arbitrage.

### 6.4 À ne pas introduire : doublons sémantiques

Clés proches existantes au registre : `source` (144 porteurs, 15 lecteurs),
`sourceType` (66, PrimarySource), `sourceFormat` (197), `sourcePage` /
`sourcePages` (332), `sourceSection` (2), `sources` (1), `dateSource` (95),
`sourceChronologyCsvRow` (6). Aucune `sourceEntry` / `bibliography*` /
`bibEntry`.

- `source_entry` ne double aucune clé existante. Vigilance mineure : casse
  snake_case face à la famille camelCase `source*` — le registre porte déjà
  les deux conventions (`section_key`, `central_argument`), pas de précédent
  violé, mais l'uniformité est à trancher **avant** création (renommer
  après = nouvelle clé + migration).
- `duplicateOf` / `reviewStatus` : les réutiliser est le bon choix
  anti-doublon ; la cohabitation de vocabulaires est documentable par le
  champ `vocabulary` régénéré.

### 6.5 Plan futur proposé (proposition — rien n'est décidé)

Un « patch_20 registre » édité à la main est **déconseillé** : le registre
est un artefact généré (« rejouable : même sortie octet pour octet ») —
toute édition manuelle serait écrasée et casserait la reproductibilité. Le
« patch registre » = révision de `build_properties_registry.py` +
régénération.

Le dilemme d'ordre :

- **Scénario A — appliquer d'abord, régénérer ensuite (même commit)** :
  `make_vNNN` → réviser le générateur → régénérer → CI verte. Entre
  application et régénération le dépôt est incohérent (CI rouge), donc graphe
  vN **et** registre doivent voyager dans le **même commit** — l'état
  intermédiaire n'est jamais vu par la CI. Le registre reste vrai à tout
  instant committé ; `count`/`domain` mesurés, jamais estimés.
- **Scénario B — étendre par anticipation** : la CI ne bloquerait pas (entrée
  sans occurrence = signalée), mais le registre mentirait dans l'autre sens
  (déclaré > réel) et cesserait d'être reproductible par son générateur —
  mensonge structurel, pas transitoire. À réserver à une application
  longtemps différée, à documenter dans `notes`, en acceptant la perte du
  rejouable.
- Dans **tous** les scénarios : le mensonge silencieux du § 6.2 (la CI ne
  vérifie ni `domain` ni `count`) reste possible sans contrôle de
  fraîcheur — indépendant des patchs candidats.

**Trois contrôles CI proposés** : (1) **fraîcheur du registre** — un
`--check` de `build_properties_registry.py` (modèle :
`build_anchor_weights --check`, déjà en CI) qui régénère en mémoire et
compare : ferme le trou du § 6.2, contrôle le plus rentable ;
(2) **préflight des candidats en CI** — `entityIds` existants dans le graphe
courant (contrôle qui périmerait à la première fusion réelle), policy
contenant toujours « CANDIDATE — NOT APPLIED », tout `attributeId` posé au
registre **ou** nommé dans la `registry_note` (exception consciente), zéro
chaîne `duplicateOf` + co-présence `duplicateOf` ⇒ `reviewStatus` dans le
patch (reprend les invariants de `make_v105`, aujourd'hui orphelins) ;
(3) **après application** : porter l'invariant
pas-de-chaîne / `duplicateOf` ⇒ `reviewStatus` dans
`check_graph_integrity.py` pour qu'il survive à son applicateur one-shot.

### 6.6 Séquencement recommandé pour une application future

1. **Arbitrage de Maël** sur les 3 patchs — les policy restent CANDIDATE
   jusque-là.
2. (Optionnel, recommandé, indépendant) **Contrôle de fraîcheur du registre**
   (§ 6.5.1) — une CI verte sur v110 inchangé prouve que le registre actuel
   est la sortie exacte du générateur.
3. **Réviser `build_properties_registry.py`** (`SOURCE` paramétrable ;
   décision sur les 3 `deprecated` et l'étape patch_19 sans objet ;
   `DATE_AUDIT`) — régénération à blanc sur v110 + diff contre le registre
   commité pour mesurer ce qui change **avant** tout patch.
4. **Écrire le `make_vNNN` applicateur** (`CREATE_ENTITY` n'est consommé par
   aucun script — vérifié) — `--dry-run` sur le modèle `make_v105`, avec
   vérifications d'après.
5. **Appliquer → v111** (`space.version = 'v111'` sinon
   `check_graph_integrity` bloque, l. 128-131).
6. **Régénérer le registre depuis v111** — `source_entry` apparaît
   (`4fafa265…`), `duplicateOf`/`reviewStatus` à `count` 81 et domaine
   élargi, `vocabulary` de `reviewStatus` = liste close à 2 valeurs.
7. **`check_graph_integrity.py` en local** — 0 clé hors registre, version
   OK, avant tout push.
8. **Commit unique** graphe v111 + registre + pointeurs de site exigés par
   `CLAUDE.md` (`package.json`, `these.html`, `graphe.html`, `lecteur.html`,
   `graph-worker.mjs`, `narrative-anchors-build.mjs` — la CI ne vérifie
   **pas** que le site pointe le bon graphe) — CI complète, puis skills
   `grc20-reviewer-hostile` / `grc20-visual-coherence` avant PR.

Risques résiduels du séquencement : scénario A — oublier l'étape 3 fait
régénérer en silence un registre décrivant v109 ; scénario B — registre non
reproductible et menteur en surplus ; les deux — sans § 6.5.1, toute
divergence future `domain`/`count` reste invisible.

## 7. Blocages et préalables d'application — la synthèse ordonnée

Rien n'est bloquant au sens du validateur (0 BLOQUANT), mais **rien n'est
applicable en l'état** : les quatre avertissements de C08/C09 (§ 4) et les
constats registre (§ 6) désignent, dans l'ordre, ce qui **doit** arriver
avant toute application. Croisement du séquencement § 6.6 et des
avertissements du validateur :

| Ordre | Préalable | Source |
|---:|---|---|
| 0 | Arbitrage d'auteur sur chacun des 3 patchs — condition de tout le reste | policy des patchs, § 9.1 |
| 1 | Révision de `build_properties_registry.py` (`SOURCE` en dur v109, `DATE_AUDIT`, étape patch_19, sort des `deprecated`) — sinon toute régénération décrit v109 | § 6.3 |
| 2 | Décision de casse `source_entry` (snake_case vs camelCase) **avant** la création des 38 nœuds | § 6.4, § 9.8 |
| 3 | Écriture d'un applicateur `make_vNNN` dédié — lève l'avertissement C09 ; il doit consommer `CREATE_ENTITY` (ou traduire en dialecte D), assigner les ids, normaliser l'encodage `[]`/clé absente (§ 5), et poser les `cited in` des 38 créations **dans le même script** (§ 5) | C09, rapport de simulation |
| 4 | Application → v111, `space.version` incrémenté | § 6.6.5 |
| 5 | Régénération du registre depuis v111 — lève les trois avertissements C08 (`source_entry` entre au registre, domaines/counts de `duplicateOf`/`reviewStatus` redeviennent vrais) | § 6.2, § 6.3 |
| 6 | `check_graph_integrity.py` local, puis commit unique graphe + registre + pointeurs de site | § 6.6.7-8 |

Les contrôles CI proposés (§ 6.5) sont **indépendants** de cette chaîne : le
contrôle de fraîcheur du registre est utile dès aujourd'hui, application ou
pas.

## 8. Risques restants

1. **Le mensonge silencieux du registre** : tant que la CI ne vérifie ni
   `domain` ni `count` (§ 6), toute application — celle-ci ou une autre —
   peut rendre le registre faux sans qu'aucun voyant ne s'allume. C'est le
   risque le plus général mis au jour par ce chantier.
2. **Les invariants `duplicateOf` sans contrôleur pérenne** : « pas de
   chaîne » et « `duplicateOf` ⇒ `reviewStatus` » ne vivent que dans
   `make_v105` (one-shot) et dans le préflight (qui ne s'exécute pas en CI).
   Les 78 nouveaux porteurs n'auraient aucun gardien (§ 6.2.a).
3. **Le risque de doublon des zips SourceQuote** : 3 extraits de la phase 3
   coïncident avec des citations déjà en v110 (inventaire) — toute
   application future dupliquerait si elle ne dédoublonne pas d'abord
   (l'outil actuel n'écrit rien, § 2 ; un applicateur réel reste à écrire
   et devra traiter ce cas). La résolution par noms des 41 ops est de
   surcroît fragile.
4. **`anchor_overrides_targeted` en zone grise** : classé
   candidat-non-appliqué par l'inventaire mais probablement périmé (base v93,
   concurrent du mécanisme v108–v109) — tant qu'il n'est pas explicitement
   retiré ou réévalué, il reste un candidat apparent qu'aucun outil ne
   valide (structure hors dialectes, hors périmètre du préflight).
5. **La fusion future des doublons marqués** : le marquage des 78 fiches est
   réversible et sans risque ; la **fusion** qu'il prépare (choix des
   canoniques, redirection des relations) serait, elle, à risque élevé —
   l'inventaire le dit explicitement, et rien ici ne l'instruit.
6. **Péremption du préflight** : C06/C11 vérifient contre le graphe le plus
   récent — la première fusion réelle d'entités périmera les résultats et
   imposera de rejouer le préflight (limite déclarée du contrôle CI proposé
   § 6.5.2).
7. **Le vocabulaire double de `reviewStatus`** (`duplicate-pending-merge` /
   `pending-author`) : sans conflit de code aujourd'hui (§ 6.2), mais tout
   futur consommateur de la clé devra connaître les deux valeurs — à figer
   dans `vocabulary` à la régénération.
8. **Comptages divergents entre livrables** (§ 3) : 26 `patch*.json` de
   racine + `new_relations_patch.json` = 27 fichiers JSON côté contrat,
   32 artefacts côté inventaire (zips, reçus et fichiers hors dialecte
   compris) — sans conséquence sur le fond, mais à ne pas citer l'un pour
   l'autre ; l'inventaire est la référence.
9. **La simulation à blanc n'a pas de générateur committé** (relevé par la
   revue hostile) : ses chiffres sont recoupables un à un (et l'ont été),
   mais le rapport n'est pas rejouable par un script du dépôt — asymétrie
   assumée avec le registre et le préflight, qui le sont ; elle imite en
   outre une sémantique d'application qu'aucun applicateur n'implémente
   encore (note `[]`/clé absente, § 5).

## 9. Décisions réservées à Maël — arbitrages du lot 1 rendus

> **Arbitrages rendus par Maël le 2026-08-07** (phase « Arbitrage Queue »,
> lot 1 infrastructure, questions posées et répondues dans le chat de
> session). Chaque décision ci-dessous porte son verdict en gras ; les
> décisions 1 (fond des 3 patchs) restent ouvertes — elles relèvent des
> lots 2-3 de la file. Ce qui découle mécaniquement des verdicts est
> appliqué par la PR qui porte cette révision : générateur du registre
> révisé et registre régénéré sur v110 (Q2/Q5-a — aucune clé candidate
> ajoutée, Q1-A respecté), clé du patch missing-nodes renommée
> `sourceEntry` (Q3), note d'arbitrage dans le patch duplicates (Q4),
> deux contrôles ajoutés à la CI (Q5-a/b), `anchor_overrides_targeted`
> archivé avec sa note (Q7). Les mentions `source_entry` des § 6.3-6.4
> ci-dessus décrivent l'état AU MOMENT de l'analyse — la graphie retenue
> depuis est `sourceEntry`.

1. **Arbitrer les 3 patchs bibliographiques** — retypes (10 ops, risque
   faible, réversibles unitairement), duplicates (156 ops, marquage
   réversible sans fusion, risque faible), missing_nodes (38 créations de
   contenu inédit, risque moyen, validation d'auteur et contrôle anti-doublon
   requis). Données d'appui : colonne `risque_scientifique` de l'inventaire,
   simulation § 5, verdict préflight § 4.
2. **Le sort des 3 zips SourceQuote** de `Migration/` — appliquer (41 ops,
   applicateur existant), vérifier d'abord les citations contre le PDF, ou
   archiver ; en cas d'application, traiter les 3 doublons potentiels de la
   phase 3. Donnée d'appui : inventaire, lignes 1-3.
   **Arbitré (Q8) : vérifier d'abord** — les 41 citations seront vérifiées contre le PDF, sans aucune écriture dans le graphe ; ni applicateur ni application avant ce contrôle. « Une fausse citation gravée dans le graphe serait pire qu'un travail préparatoire laissé en attente. »
3. **Le sort de `patches/grc20_anchor_overrides_targeted.json`** —
   réévaluation complète ou retrait : base v93, structure hors dialectes,
   clés inconnues du registre, mécanisme concurrent de v108–v109. Donnée
   d'appui : inventaire, dernière ligne `patches/`.
   **Arbitré (Q7) : archivé** — déplacé vers `patches/archive/` avec sa note de motifs ; pas de réévaluation sauf preuve ultérieure que ces 10 entrées portaient un jugement d'auteur que v108/v109 n'a pas repris.
4. **Adopter ou amender le contrat de patch** (§ 3) — notamment la sévérité
   de l'applicateur futur (`source_graph` bloquant ou indicatif, § 4) et le
   sort de `CREATE_ENTITY` (le promouvoir en op consommable, ou rabattre les
   créations sur le dialecte D — le contrat § 5 renvoie ce choix). À savoir
   en décidant : le validateur committé **outille déjà** ce contrat (C02,
   C03, C09 en appliquent les règles) — l'amender implique de mettre à jour
   `preflight_candidate_patches.py` dans le même mouvement ; le préflight
   n'étant pas en CI, rien n'est verrouillé d'ici là.
   **Arbitré partiellement (Q6) : pour `CREATE_ENTITY`, pas d'applicateur tant que les 38 fiches ne sont pas arbitrées ; quand elles le seront, un `make_vNNN` dédié propre plutôt qu'un rabattement sur l'ancien dialecte D.** Le reste du contrat demeure en l'état, outillé par le validateur.
5. **Scénario A ou B pour le registre** (§ 6.5) — même-commit mesuré, ou
   extension anticipée avec perte de reproductibilité. Donnée d'appui :
   § 6.5 et les deux chiffres registre de la simulation (§ 5).
   **Arbitré (Q1) : scénario A** — appliquer les patchs arbitrés puis régénérer le registre, dans le même commit. « Je ne veux pas d'un registre étendu par anticipation qui décrive un état qui n'existe pas. »
6. **Réviser `build_properties_registry.py`** — `SOURCE` codé en dur v109
   (l. 39), `DATE_AUDIT` figée, exigence patch_19 obsolète, disparition des
   3 entrées `deprecated` à la régénération (perte d'historique à assumer ou
   à compenser). Donnée d'appui : § 6.3.
   **Arbitré (Q2) : révisé maintenant** — source paramétrable (défaut : graphe le plus récent), patch_19 conditionnel détecté par les données, et les 3 entrées dépréciées **conservées** via la liste d'historique explicite `HISTORIQUE_DEPRECIEES` (« une trace d'audit, pas un déchet »). Registre régénéré sur v110 : 338 entrées, 15 modifiées (comptes patch_19 intégrés, domaines des 21 retypages patch_18, readBy des scripts récents), dépréciées à count 0 avec comptes historiques v109 en notes.
7. **Ajouter les contrôles CI proposés** (§ 6.5) — fraîcheur du registre
   (ferme le mensonge silencieux, utile indépendamment de tout patch),
   préflight des candidats en CI, invariants `duplicateOf` dans
   `check_graph_integrity.py` après application.
   **Arbitré (Q5) : (a) + (b) maintenant** — fraîcheur du registre (`build_properties_registry.py --check`) et préflight des candidats ajoutés à `check.yml` ; **(c) reporté** au moment où les annotations `duplicateOf` seront effectivement appliquées.
8. **La casse de `source_entry`** — snake_case (comme `section_key`) ou
   camelCase (comme la famille `source*`), à trancher **avant** la création
   des 38 nœuds : renommer après coup serait une nouvelle clé plus une
   migration. Donnée d'appui : § 6.4.

   **Arbitré (Q3) : `sourceEntry`** (camelCase, aligné sur la famille `source*` ; `source` écarté comme trop ambigu) — le patch candidat est modifié maintenant plutôt qu'une migration plus tard ; id de la future entrée : `e3f8b05adc0057677354bf5fb0f7c5e1`.
## 10. Ce que ce chantier n'a pas fait

Aucun patch appliqué, aucun graphe écrit, pas de v111 ; le registre des
propriétés est inchangé ; aucun fichier de patch n'a été modifié, créé ni
réécrit (les historiques dérogatoires restent des archives, § 3) ; aucun
applicateur `make_vNNN` n'a été écrit ; aucun contrôle CI n'a été ajouté
(les trois du § 6.5 sont des propositions) ; le runtime (`graphe.html`,
`lecteur.html`, presets) n'a pas été touché. Sur le fond scientifique : les
citations des zips SourceQuote n'ont **pas** été vérifiées contre le PDF, le
bien-fondé des 38 fiches à créer et le choix des canoniques des 78 doublons
n'ont **pas** été instruits — ce sont les objets mêmes de l'arbitrage
d'auteur (§ 9.1-9.2). Les écritures de ce chantier se limitent à : le
validateur (`scripts/preflight_candidate_patches.py`, lecture seule à
l'exécution), les deux fichiers de données
(`candidate-patch-inventory-v1.csv`,
`candidate-patch-preflight-report-v1.json`), le contrat
(`grc20-candidate-patch-contract-v1.md`) et le présent document.
