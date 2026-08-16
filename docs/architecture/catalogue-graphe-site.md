# Architecture — Catalogue d'événements × graphe GRC-20 × site × articles

**Statut : page de cadrage. Elle décrit l'existant, propose des conventions, et ne tranche rien.**
Chaque proposition est marquée `[À ARBITRER]` et reprise en §10. Aucune ligne du catalogue n'a été
recodée pour produire cette page ; aucun patch n'a été généré ; le graphe n'a pas été touché.

- Rédigée le : 2026-08-15
- Cadrage d'autorité : BLOC C du prompt de session (verbatim de Maël Rolland), archivé en
  `docs/audits/PROMPT-COWORK-catalogue-graphe-site.md`
- Mesures : catalogue `docs/research/catalogue-evenements/catalogue-evenements-v3-1.csv` (345 lignes)
  et graphe `grc20-these-mael-rolland-v115.json` (canonique au 2026-08-15), relevées le 2026-08-15
- Charte applicable : `agents/README.md` — « un agent est un rôle de travail, pas une autorité
  scientifique »

---

## 1. Les quatre couches

Le principe posé en BLOC C §1 est que **le catalogue n'efface pas le graphe**. Les deux objets
existent déjà, ils ont des propriétés différentes, et la confusion des deux est le risque que cette
page a pour fonction d'écarter.

| Couche | Objet | Fichier(s) faisant foi | Nature | Qui écrit |
|---|---|---|---|---|
| **A — Catalogue** | couche scientifique de codage des événements | `docs/research/catalogue-evenements/catalogue-evenements-v3-1.csv` | instrument de travail, mouvant, colonnes analytiques | Maël + agents en mode proposition |
| **B — Graphe** | couche canonique publiée | `grc20-these-mael-rolland-v115.json` | entités identifiées, versionnées, contraintes (CI, registre d'attributs) | uniquement un script `make_vNNN` appliquant un patch arbitré |
| **C — Site** | couche de consultation publique | `graphe.html`, `lecteur.html`, `graph-worker.mjs`, `public-data/` | statique, lit le graphe canonique | pipeline de publication |
| **D — Articles** | couche de valorisation | manuscrits hors dépôt | cite des états figés | Maël |

### 1.1 Ce que chaque couche a le droit de lire

```
   figure V2.8 (.bin)            texte de la thèse (assets/MD/)
          │                                │
          │ decode_chronologie.py          │ lecture humaine
          ▼                                ▼
   ┌──────────────────────────────────────────────────┐
   │  A — CATALOGUE  (CSV, 345 lignes, mouvant)       │◄── fusion.py ──┐
   └──────────────────────────────────────────────────┘                │
          │                                                            │
          │ patch candidat conforme au contrat                         │ lecture seule,
          │ + audit + ARBITRAGE DE MAËL + make_vNNN                    │ scripts versionnés
          ▼                                                            │
   ┌──────────────────────────────────────────────────┐                │
   │  B — GRAPHE CANONIQUE (v115)                     │────────────────┘
   └──────────────────────────────────────────────────┘
          │                                    │
          │ pointeurs de version               │ export dérivé versionné
          ▼                                    ▼
   ┌──────────────────┐              ┌──────────────────────┐
   │  C — SITE        │              │  D — ARTICLES        │
   │  lit B, jamais A │              │  citent un SNAPSHOT  │
   └──────────────────┘              └──────────────────────┘
```

Les deux règles de lecture, qui sont la traduction directe du BLOC C §2 et §3 :

- **Le site ne lit jamais A.** Il lit B (aujourd'hui : 15 occurrences du nom de
  fichier `grc20-these-mael-rolland-v115.json` dans 7 fichiers — `graphe.html`, `lecteur.html`, `these.html`,
  `graph-worker.mjs`, `grc20-publish.mjs`, `narrative-anchors-build.mjs`, `package.json`). Si un
  jour le site devait afficher un matériau issu du catalogue, il lit un **export dérivé versionné**
  déposé sous `public-data/`, jamais le CSV de travail. `[À ARBITRER — D1]`
- **Un article ne cite jamais « le catalogue ».** Il cite un **snapshot** (§6).

### 1.2 Ce que le catalogue apporte que le graphe n'a pas

Ce n'est pas une redondance : les deux couches ne portent pas la même information.

| | Graphe v115 | Catalogue v3-1 |
|---|---|---|
| Événements | 164 `InfrastructureEvent` + 55 `CrisisEvent` = **219** | **345 lignes** |
| Domaines de la thèse (ch. I l.251) | 8 `InfrastructureDomain`, **les 8, (ii) compris** (voir l'encadré ci-dessous) | `domaine_8` sur 265 lignes |
| Typologie d'acteurs de la grille | 36 `StakeholderCategory` — la passation du 03/08 les dit « de trois granularités mêlées, avec doublons » ; ce diagnostic n'a pas été remesuré ici | 7 types fermés, `acteur_principal` sur 134 lignes |
| Arènes | 13 `GovernanceArena`, lieux nommés | 9 types fermés, `arene` sur 134 lignes |
| Type d'acte | absent | 7 valeurs fermées, sur 134 lignes |
| Effets sur propriétés monétaires | absent | 25 lignes énoncées, 320 `nd` |
| Séquences (Abbott) | absent | `fil` sur 122 lignes |
| Source ligne à ligne dans le texte | partielle | `source` sur **345/345 lignes** (obligatoire) |

Le catalogue est donc bien la **couche de codage** : il ajoute des dimensions analytiques fermées
que l'ontologie GRC-20 ne porte pas, et il exige une source pour chaque ligne. Le graphe reste la
couche **canonique publiée** : identifiants stables, versions, contraintes de CI.

> ### ⚠ Constat périmé qui circule encore dans les fichiers versés
>
> **Quatre documents** du dépôt affirment que **« le graphe n'a aucun domaine correspondant à (ii)
> traitement des transactions »** : `PASSATION-claude-code-dedup-events.md` (§6.7 et §8),
> `docs/audits/grc20-dedup-events-audit-v1.md` (§7), `docs/research/catalogue-evenements/README.md`,
> `etat-catalogue-evenements-v2-2026-08-02.md` — et, jusqu'à cette correction, la première rédaction
> de la présente page, qui fait le cinquième.
>
> **C'est faux depuis v102.** Remesuré sur v115 le 2026-08-15 : le nœud `8fc8b0d7aa…`
> « Traitement des transactions » porte `InfrastructureDomain`, `domain_index = ii`,
> `color = jaune`, et **103 relations** (68 entrantes, 35 sortantes). Il existait déjà, mal typé
> (`Concept` seul) ; `scripts/make_v102_restore_domain_ii.py` l'a retypé et a fusionné l'intrus
> « De la confidentialité et de l'anonymisation » dans (iii).
> `docs/audits/grc20-domaines-developpement-v1.md` porte la rétractation explicite.
> *(Cet audit annonce 67 relations : c'est son chiffre d'époque, v102. Le remesurer sur v115 donne
> 103. Un chiffre d'audit ne se recopie pas, il se remesure — y compris ici : la première rédaction
> de cet encadré avait recopié 67.)*
>
> **Conséquence** : les événements de minage **sont** rattachables depuis le graphe seul. Ce n'était
> pas une lacune d'ontologie, c'était un défaut de typage invisible à tout contrôle qui se contente
> de compter huit domaines.
>
> **Leçon de méthode, applicable à toute cette page** : les états de chantier et passations versés
> sous `docs/audits/` sont des *données*, pas des *faits* (charte `agents/README.md`, règle 3). Ils
> doivent être remesurés sur le graphe courant avant d'être cités. Cette page a commis l'erreur et
> la consigne ici plutôt que de l'effacer.
> `[À ARBITRER — D13 : corriger les quatre documents, ou les laisser en l'état avec un renvoi ?]`

---

## 2. Identifiants

Proposition construite **à partir des colonnes existantes**, sans renommage (BLOC D).

| Rôle | Colonne actuelle | Forme | Couverture mesurée | Autorité |
|---|---|---|---|---|
| `event_id` | `id` | `E`/`G`/`F` + 3 chiffres | **345/345, tous distincts** | catalogue |
| `graph_entity_id` | `gid` | id GRC-20 (hex 32) | **207/345**, tous distincts | graphe |
| `source_id` | `source` | `ch.I l.XXX` / `n.XX` / `fig. n°6` | **345/345** | texte de la thèse ou figure |
| (auxiliaire) | `source_graphe` | provenance côté graphe | 207/345 | graphe |

**Sémantique des préfixes** (constatée, à figer) : `E` = relevé dans le texte (82 lignes),
`G` = importé du graphe (175), `F` = relevé sur la figure V2.8 (88). La colonne `origine` porte la
même information sous une autre forme (`catalogue` 50, `catalogue+graphe` 32, `graphe` 175,
`figure` 88). **Redondance à assumer ou à supprimer** — elle est aujourd'hui cohérente, mais deux
colonnes qui disent la même chose finissent par diverger. `[À ARBITRER — D2]`

### 2.1 Vérification effectuée — les `gid` n'ont pas dérivé

Les 207 `gid` du catalogue ont été prélevés sur le graphe **v97**. Ils ont été recontrôlés le
2026-08-15 contre **v115** :

> **207 `gid` sur 207 existent encore dans v115. Aucun identifiant mort, aucune dérive.**

C'est le fait empirique qui rend la jointure catalogue↔graphe viable, et c'est aussi ce qui doit
être **revérifié à chaque bump de version du graphe**. Ce n'est pas acquis : entre v97 et v115, le
dépôt a connu un retypage de domaine **et une fusion avec suppression de nœud** (v102), un câblage
des événements aux domaines (v103), une fusion marquée sans suppression (v105), des retypages
bibliographiques (v110, v113), deux corrections de dates (v112) et des corrections de libellés
(v114, v115). Qu'aucun des 207 `gid` n'ait été emporté est un résultat, pas une propriété.

### 2.2 Règles d'identifiants

1. **Un `event_id` n'est jamais réutilisé**, même après suppression ou exclusion d'une ligne.
2. **Un `event_id` n'est jamais renommé.** Une renumérotation impose une table de correspondance
   versionnée dans le même commit.
3. **Le `gid` n'est jamais inventé côté catalogue.** Il est soit issu d'un script d'import, soit
   absent. Un événement du catalogue sans contrepartie au graphe garde `gid` vide : c'est une
   information, pas un manque à combler.
4. **`source` est obligatoire et non dérivable.** Une ligne sans source ne peut pas exister.
   (Contrôle : aujourd'hui 345/345.)
5. Un `gid` peut porter **plusieurs** `event_id` (le graphe modélise parfois en un nœud ce que le
   catalogue distingue en deux actes — précédent : Bitcoin Magazine, création 2011 vs première
   parution 01/05/2012). La relation est donc **1 graphe → n catalogue**, jamais l'inverse.
   `[À ARBITRER — D3 : confirmer cette cardinalité]`

---

## 3. Statut des lignes

### 3.1 Le constat : deux axes sont aujourd'hui confondus en une colonne

La typologie de Maël (BLOC C §4) — **validé / chantier / douteux / exclu** — qualifie
**l'événement** : existe-t-il, est-il bien daté, appartient-il au périmètre ?

La colonne existante `codage_statut` qualifie **le codage analytique** de la ligne :

| `codage_statut` | Lignes | Ce que ça veut dire |
|---|---:|---|
| `valide(calibrage)` | 82 | codé à la lecture du texte, lot de calibrage |
| `propose(lot1)` | 40 | codage automatique proposé, **non arbitré** |
| *(vide)* | 223 | non codé |

Ce sont deux questions distinctes. Une ligne peut être un **événement validé** dont le **codage est
à faire** (c'est le cas des 175 lignes `origine=graphe`), ou un **événement douteux** déjà codé.
Écraser l'un par l'autre perdrait de l'information.

### 3.2 Proposition : deux colonnes, table de passage explicite

`[À ARBITRER — D4]` Ajouter une colonne **`statut_ligne`** portant la typologie de Maël, et
conserver `codage_statut` pour l'état du codage :

**Table de passage — état actuel → `statut_ligne` proposé**

| Situation actuelle mesurée | Lignes | `statut_ligne` proposé | Motif |
|---|---:|---|---|
| `codage_statut = valide(calibrage)` | 82 | `valide` | événement relevé et vérifié dans le texte |
| `origine = graphe`, sans note `[CHANTIER]` | ~175 | `valide` | l'événement existe au graphe canonique |
| `origine = figure`, sans note `[CHANTIER]` | ~88 | `valide` | l'événement est porté par la figure V2.8 |
| marqueur `[CHANTIER…]` dans une colonne quelconque | **13** | `chantier` | ambiguïté explicitement consignée |
| membre d'une des **13 paires `A_VERIFIER`** (`docs/audits/data/doublons-verifies.csv`) | **21** | `douteux` | identité d'événement non tranchée |
| ligne portant une des **5 divergences de dates** (`table-divergences-dates.csv`) | 5 | `douteux` | date texte ≠ date graphe, non arbitré |
| — | **0** | `exclu` | *aucune ligne n'est aujourd'hui marquée exclue* |

**Attention au critère de comptage.** Les 13 lignes `chantier` ne sont *pas* « les lignes dont
`notes` contient `[CHANTIER]` » : ce filtre-là n'en trouve que 11. **E019** et **E081** portent leur
marqueur dans `type_acte` (`[CHANTIER type]` — retrait d'un concepteur, abandon d'un projet), pas
dans `notes`. Le critère juste est : *marqueur `[CHANTIER` dans n'importe quelle colonne*. Les 13
sont E001, E004, E019, E022, E025, E034, E051, E055, E062, E063, E067, E081, E082. Les 21 lignes
`douteux` sont obtenues en joignant les 13 paires `A_VERIFIER` au catalogue par `gid` (E001, E035,
E041, E049, et 17 lignes `G…`) ; E001 est à la fois `chantier` et `douteux`, ce qui montre que les
deux qualifications ne s'excluent pas. `[À ARBITRER — D14 : `statut_ligne` est-il une valeur unique,
ou faut-il un champ multi-valué ?]`

**`codage_statut` — vocabulaire proposé** (renommage cosmétique, une table de correspondance
suffit) : `non_code` (vide, 223) · `propose` (`propose(lot1)`, 40) · `valide`
(`valide(calibrage)`, 82).

### 3.3 Trois points que cette table laisse ouverts

1. **`exclu` n'a pas de règle.** La préhistoire (avant le 18/07/2008, Q4 de la grille) est
   aujourd'hui *absente du fichier*, pas *marquée exclue*. Faut-il (a) garder les exclusions hors
   fichier, ou (b) les faire figurer avec `statut_ligne=exclu` et un motif ? L'option (b) rend le
   périmètre auditable ; l'option (a) garde le fichier propre. `[À ARBITRER — D5]`
2. **`propose(lot1)` ne devient pas `valide` par le temps qui passe.** Les 40 lignes du lot 1
   restent proposées tant que la convention de rôles (§4) n'est pas arrêtée : leur codage dépend
   directement de la décision attaquant/résolveur.
3. **Un `statut_ligne` n'est jamais dégradé en silence.** Passer `valide` → `douteux` est une
   information ; ça s'écrit dans `notes` avec sa date et sa raison.

---

## 4. Rôles — grille v2

### 4.1 Le point de méthode (BLOC C §5)

La paire attaquant/résolveur est écartée : trop morale, trop étroite, inapplicable hors crise. La
convention retenue distingue deux questions que les colonnes actuelles mélangent :

- **QUI intervient** → les 7 types d'acteurs de la grille v1 (`acteur_principal`,
  `acteur_secondaire`) : `core_devs` · `mineurs` · `entrepreneurs_exchanges` ·
  `institutions_financieres` · `regulateurs_etats` · `medias_connaissance` · `communautes_forums`
- **COMMENT il intervient** → les 7 rôles de la convention v2 : `declencheur` · `affecte` ·
  `revelateur` · `correcteur` · `validateur` · `opposant` · `coordinateur`, plus `na` (non
  applicable) et `incertain`

Les deux vocabulaires sont **orthogonaux** : `core_devs` peut être `correcteur` (CVE corrigée),
`declencheur` (changement protocolaire) ou `opposant` (rejet d'une proposition). C'est précisément
ce que la colonne `acteur_principal` seule ne peut pas dire.

### 4.2 Deux formes possibles, à arbitrer

**Forme 1 — colonnes appariées (additif, minimal).** Deux colonnes nouvelles,
`role_principal` et `role_secondaire`, en face des deux colonnes d'acteurs existantes. Aucun
renommage, le CSV reste lisible à plat, `fusion.py` continue de tourner.
*Limite* : plafonné à deux acteurs par événement.

**Forme 2 — table satellite en format long.** Un fichier `catalogue-roles-v1.csv` :
`event_id ; acteur ; role ; rang ; justif ; source`. Autant de lignes que d'acteurs impliqués.
*Limite* : plus lourd à annoter à la main, deux fichiers à tenir cohérents.

`[À ARBITRER — D6]` **Le dépôt ne peut pas trancher entre les deux formes, et il faut le dire.**
On serait tenté d'observer qu'aucune ligne du lot 1 ne code plus de deux acteurs : l'observation ne
vaut rien, puisque le CSV n'a que deux colonnes d'acteurs — elle mesure la contrainte du fichier,
pas la réalité des crises. La question est donc entièrement empirique et relève de la lecture :
*une crise du corpus demande-t-elle de nommer simultanément un déclencheur, un affecté, un
correcteur et un validateur ?* The DAO en est le candidat évident.

Seul point de méthode établi, qui ne présume pas de la réponse : **la forme 1 est un sous-cas
strict de la forme 2**, donc une migration 1 → 2 est mécanique et sans perte, alors que 2 → 1
perdrait de l'information. Commencer par la forme 1 n'est donc pas un pari irréversible.

### 4.3 Ce que la convention de rôles règle dans le lot 1 — et ce qu'elle ne règle pas

Le lot 1 (40 lignes, `docs/research/catalogue-evenements/lot1-crises-a-valider.csv`) achoppe sur
une question posée dans `docs/audits/etat-lot1-codage-2026-08-05.md` §1 : pour une crise exploitée
*puis* résolue, l'acteur principal est-il l'attaquant (`nd`, hors typologie — précédent E065) ou le
résolveur (`core_devs` — précédent E015) ? Deux précédents du calibrage coexistent.

Avec la convention de rôles, la question **change de nature** : l'attaquant est `declencheur`, les
développeurs sont `correcteur`, les porteurs de fonds sont `affecte`. Il n'y a plus à choisir un
« principal » entre deux fonctions incomparables.

Mais **elle ne se règle pas toute seule** : il reste à décider si `acteur_principal` doit accueillir
le déclencheur ou le correcteur quand la forme 1 (deux colonnes) est retenue.
`[À ARBITRER — D7]`

**Le lot 1 n'est pas recodé dans cette session.** La migration décrite ici est un plan ; son
exécution attend D6 et D7.

### 4.4 Trou typologique à ne pas combler par inférence

`nd` sert aujourd'hui à deux choses différentes : « acteur hors typologie » (attaquant anonyme,
E065) et « non renseigné ». La convention de rôles n'y touche pas. Si D6/D7 sont arbitrés, il
faudra distinguer `hors_typologie` de `nd`. Même remarque pour E019 et E081 (retrait d'un
concepteur, abandon d'un projet) : ces actes n'ont pas de `type_acte` dans la grille v1, et le lot 1
les laisse en `[CHANTIER]`. **Aucune catégorie n'est créée en silence** (grille v1, règle
transversale R4).

---

## 5. Le circuit catalogue → patch → graphe

### 5.1 Le circuit, étape par étape

```
 (1) OBSERVATION       une divergence ou un manque est constaté dans le catalogue
        ▼
 (2) AUDIT             un rapport docs/audits/*.md l'instruit, chiffres et sources à l'appui
        ▼                   → données probantes dans docs/audits/data/
 (3) PATCH CANDIDAT    patch_candidate_<objet>_v1.json, conforme au contrat
        ▼                   → _meta.policy commence par
                              « CANDIDATE — NOT APPLIED — AUTHOR ARBITRATION REQUIRED »
 (4) PREFLIGHT         python3 scripts/preflight_candidate_patches.py   (13 contrôles, C01..C13)
        ▼
 (5) REVUE HOSTILE     skill grc20-reviewer-hostile — 9 questions, aucun correctif
        ▼
 (6) ►► ARBITRAGE DE MAËL ◄◄   seule étape qui autorise le passage
        ▼
 (7) APPLICATEUR       scripts/make_vNNN_<objet>.py, avec --dry-run et ses after-checks
        ▼
 (8) CONTRÔLES         check_graph_integrity · check_anchoring · build_anchor_weights --check
        ▼              build_properties_registry --check · preflight_candidate_patches
 (9) POINTEURS         les 15 occurrences du nom de fichier du graphe (7 fichiers), ensemble
        ▼
(10) LEDGER            patch-application-ledger.json + queue régénérés
```

Les étapes 3, 4, 7, 8 et 10 sont **déjà en service dans le dépôt** ; le circuit ci-dessus ne les
invente pas, il les nomme comme le chemin unique.

### 5.2 Forme obligatoire d'un patch issu du catalogue

Fixée par `docs/audits/grc20-candidate-patch-contract-v1.md` §3, sans exception :

- enveloppe à exactement deux clés : `_meta` et `ops` ;
- `_meta` porte `patch_id` (préfixe `candidate-`, unique dans le dépôt), `source_graph` (nom de
  fichier exact vérifié), `generated`, `description` chiffrée avec ses sources, `policy`,
  `skipped` + `skipped_count` motivés un par un, et des comptes recomputables ;
- dialecte d'ops unique (`patch_18`/`19`) : clé `ops`, opération `type`, champs `entityId` /
  `attributeId`, `value` = `{type, value}` ;
- **jamais** d'auto-application, **jamais** de mélange de dialectes, **jamais** d'`entityId`
  préassigné sur `CREATE_ENTITY`.

**Un patch issu du catalogue déclare en plus, dans `_meta`, les `event_id` d'origine de chaque op.**
`[À ARBITRER — D8]` C'est ce qui rend la trace remontable dans les deux sens : sans cela, on sait
qu'une valeur a été posée mais plus quelle ligne du catalogue l'a motivée. Clé proposée :
`_meta.catalogue_source` = `{fichier, version, commit, event_ids}`.

### 5.3 Ce qui ne passe jamais par un patch

- **Le codage analytique.** `domaine_8`, `acteur_principal`, `arene`, `type_acte`,
  `effet_prop_monetaires`, `fil` sont des dimensions du catalogue. Les porter au graphe
  supposerait d'étendre l'ontologie GRC-20 — décision d'auteur, hors de ce circuit. `[À ARBITRER — D9]`
- **Les fusions d'entités.** Précédent `patch_10` : le patch **marque** (`duplicateOf` +
  `reviewStatus = duplicate-pending-merge`), il ne fusionne pas. Trois entités de v115 portent ces
  attributs aujourd'hui, formant **deux familles** (un triplet « Mining pools » vers `15864ab2…`,
  une paire « Scaling Debate » vers `e3742113…`) ; tous les membres restent interrogeables. La fusion
  effective est un acte humain ultérieur.
- **Les corrections « côté thèse ».** Quand la vérification externe donne raison au graphe contre le
  texte (Frontier `30/07/2015`, ch.I l.399), la correction relève du manuscrit, pas d'un patch.

---

## 6. Snapshots pour les articles

Un article ne cite pas « le catalogue » : il cite un **état figé**, identifiable et rejouable
(BLOC C §3).

### 6.1 Le descripteur de snapshot

Chaque snapshot est un fichier `docs/research/catalogue-evenements/snapshots/snapshot-<id>.md`
portant, au minimum :

| Champ | Exemple |
|---|---|
| `snapshot_id` | `cat-v3-1-2026-08-05` |
| `fichier` | `catalogue-evenements-v3-1.csv` |
| `commit` | SHA du dépôt (**c'est lui qui fait foi**, pas le nom de fichier) |
| `date` | 2026-08-05 |
| `lignes` | 345 |
| `lots inclus` | calibrage (82) · graphe v97 (175) · figure V2.8 (88) |
| `colonnes gelées` | les 29 colonnes de l'en-tête, énumérées |
| `colonnes non gelées` | `effet_prop_monetaires` (Q7 non figé, §7) |
| `exclusions` | préhistoire antérieure au 18/07/2008 (Q4) |
| `lignes CHANTIER` | **13**, énumérées par `event_id` (critère : marqueur `[CHANTIER` dans **n'importe quelle** colonne — cf. §3.2, le filtre sur `notes` seul en manque 2) |
| `lignes douteuses` | 21 lignes issues des 13 paires `A_VERIFIER` + 5 divergences de dates |
| `graphe de référence` | `grc20-these-mael-rolland-v115.json` |

### 6.2 Règles

1. **Un snapshot est immuable.** Une correction produit un nouveau snapshot, jamais une réécriture.
2. **Un article cite un `snapshot_id`**, jamais un chemin de fichier nu.
3. **Un snapshot déclare ses trous.** Les lignes `chantier` et `douteux` sont énumérées : un lecteur
   doit pouvoir savoir ce que le chiffre cité ne couvre pas.
4. Les vigilances anti-redondance de la grille v1 restent en vigueur : crises → SASE ; Scaling
   Debate → *Économie et institutions* 2017 ; carnavalesque → *Revue de la régulation* ;
   construction des figures → BMS. **Le catalogue recense, il n'analyse pas.**

`[À ARBITRER — D10]` Créer le dossier `snapshots/` et y déposer le descripteur du v3-1 comme
premier snapshot ? Cette page ne l'a pas fait — ce serait figer un état sans mandat.

---

## 7. Q7 — protocole d'épreuve avant gel du vocabulaire des effets

Le BLOC C §6 accorde le gel d'un vocabulaire v0, **mais après une passe d'épreuve**. État actuel :
`effet_prop_monetaires` est renseigné sur **25 lignes** (`valorisation(+)` 8, `usage_paiement(+)` 4,
`conf_methodique(+)` 3, `valorisation(-)` 3, `liquidite_convertibilite(+)` 2, `conf_hierarchique(+)` 1,
`conf_methodique(-)` 1, `fongibilite(+)` 1, `liquidite_convertibilite(-)` 1, `usage_paiement(-)` 1),
les 320 restantes portant `nd`.

### 7.1 Vocabulaire provisoire soumis à l'épreuve

`usage_paiement` · `valorisation` (usage financier — **jamais** « réserve de valeur » comme fonction
stricto sensu) · `unite_compte_etalon` · `liquidite_convertibilite` · `conf_methodique` /
`conf_hierarchique` / `conf_ethique` · `fongibilite`, avec direction `+` / `-` / `±` (trait d'union
ASCII, comme dans le CSV — jamais le signe moins typographique), et `nd`
sinon. **Règle inchangée : on ne code que l'effet énoncé par une source** (texte, figure, ou
description sourcée du graphe).

### 7.2 Le protocole, en quatre temps

1. **Constitution du lot d'épreuve — ~15 lignes.** Composition : les 25 lignes déjà codées servent
   de témoin ; le lot d'épreuve est tiré **hors** de ces 25, multi-domaines (au moins une ligne par
   domaine, les huit si possible — la composition exacte est à arrêter avec le lot, aucun domaine
   n'est exclu a priori), multi-`type_acte`, et **uniquement des lignes dont la
   source énonce un effet**. Une ligne dont la source n'énonce rien n'éprouve rien.
2. **Codage test à l'aveugle.** Le lot est codé une fois par Maël et une fois par un agent, sans se
   voir. Rien n'est écrit dans le CSV maître : le lot d'épreuve est un fichier séparé.
3. **Rapport d'écarts.** `docs/audits/grc20-q7-epreuve-vocabulaire-v0.md`, portant : les désaccords
   ligne à ligne ; les termes jamais mobilisés (candidats à la suppression) ; les effets énoncés par
   les sources qu'aucun terme ne capte (candidats à l'ajout) ; les frontières floues
   (`valorisation` vs `liquidite_convertibilite` est le couple le plus exposé).
4. **Gel v0.** Le vocabulaire arrêté est écrit dans `docs/research/catalogue-evenements/
   vocabulaire-effets-v0.md`, daté, avec un numéro de version.

### 7.3 Règle de non-renommage après gel

> **Une fois gelé, un terme n'est jamais renommé en silence.**
> Un changement produit soit un **incrément de version** (`vocabulaire-effets-v1.md`), soit une
> **table de correspondance** `v0 → v1` versionnée dans le même commit. Les snapshots antérieurs
> continuent de désigner la version sous laquelle ils ont été codés.

Corollaire pour les lignes déjà codées : si le gel v0 amende un terme utilisé par les 25 lignes
témoins, celles-ci sont **recodées par script avec la table de correspondance**, pas à la main.

`[À ARBITRER — D11]` Lancer la passe d'épreuve, ou geler tel quel le vocabulaire provisoire (option
proposée en `etat-lot1-codage-2026-08-05.md` §2) ? Le BLOC C §6 dit « oui au gel, mais après une
courte passe d'épreuve » — cette page suit le BLOC C.

---

## 8. Règle anti-divergence

### 8.1 La règle

> **Le graphe ne se modifie que par patch arbitré. Le catalogue n'importe du graphe que par script
> versionné. Toute divergence constatée devient une ligne d'audit, jamais une correction
> silencieuse.**

Ce qui se décline en quatre interdits et un flux de détection.

### 8.2 Les quatre interdits

| # | Interdit | Précédent qui le motive |
|---|---|---|
| **I1** | Éditer un JSON de graphe à la main | `CLAUDE.md` — l'applicateur `make_vNNN` possède l'opération |
| **I2** | Écrire au graphe une valeur du catalogue sans patch candidat arbitré | charte `agents/README.md`, mode C |
| **I3** | Écraser une valeur du catalogue sourcée par le texte avec une valeur du graphe ou de la figure | règle déjà appliquée en v3 : conflit noté `[CHANTIER domaine : texte X / figure Y]` (cas E004), jamais tranché |
| **I4** | Réconcilier une divergence en modifiant les deux côtés « pour qu'ils se rejoignent » | la divergence *est* la donnée : elle documente que deux sources ne disent pas la même chose |

### 8.3 Le flux de détection

Un contrôle de divergence — **à écrire**, `scripts/check_catalogue_graphe.py`
`[À ARBITRER — D12]` — parcourt les 207 paires `(event_id, gid)` et compare :

| Comparaison | Sortie attendue |
|---|---|
| `gid` encore vivant dans le graphe courant | **207/207 au 2026-08-15 contre v115** |
| `date` du catalogue vs `date` de l'entité | écarts → `docs/audits/data/divergences-catalogue-graphe-<vNNN>.csv` |
| `intitule` vs `name` (distance + identifiants distinctifs) | idem |
| `domaine_8` vs domaine du graphe | écarts → même CSV. **Précédent v103**, mesuré sur le catalogue **v2** (253 lignes), pas sur v3-1 : sur 113 lignes joignables, 81 tenaient leur domaine du graphe (réécriture circulaire, écartées), 17 le confirmaient, **6 le contredisaient — signalés, non tranchés** — et 9 seulement apportaient un domaine absent. L'apport net du catalogue au graphe est petit : c'est la mesure honnête |
| entités marquées `duplicateOf` dont un membre est au catalogue | 3 entités concernées en v115 |

**Le contrôle produit un CSV, jamais une correction.** Il tourne après chaque bump de version du
graphe et après chaque version du catalogue. Son résultat est lu **avec** son audit, jamais seul
(`docs/audits/data/README.md`).

### 8.4 Ordre d'autorité

En cas de contradiction entre deux artefacts du dépôt, l'ordre est déjà fixé par `CLAUDE.md` et
n'est pas rediscuté ici :

> **graphe → queue vivante → ledger.** Jamais la `policy` d'un patch, jamais son `lifecycleStatus`.

Faut-il un second ordre, entre les **sources** cette fois (texte de la thèse, figure V2.8, graphe,
catalogue) ? **Cette page ne le pose pas, parce que le dépôt le contredit.**
`[À ARBITRER — D15]`

Ce qui est établi, et seulement cela :

| Établi | Portée | Source |
|---|---|---|
| Le texte prime sur la figure | **uniquement pour `domaine_8`** | `etat-catalogue-v3-2026-08-05.md` §2 : « un domaine sourcé texte n'est jamais écrasé par la figure » — conflit noté `[CHANTIER domaine …]`, cas E004 |
| La figure tranche ce qu'elle seule porte | cas par cas | Tether : date fixée au 06/10/2014 par la figure, le texte (n.62 l.583) n'en donne aucune |
| Le graphe prime pour l'identité d'entité | ids, types, relations | c'est la définition de la couche canonique |
| Le catalogue ne prime sur rien | — | c'est un instrument, pas une source |

Et voici pourquoi la généralisation en un ordre unique serait fausse — les deux cas vont en sens
inverse, dans le même fichier (`docs/audits/data/dates-verification-externe.csv`) :

- **Frontier** : le graphe (`30/07/2015`) a raison, c'est le texte (ch.I l.399, `20/07/2015`) qui
  est à corriger ;
- **Litecoin** : le texte a raison contre le graphe.

Un ordre de priorité *entre sources* remplacerait donc la vérification externe par une règle
automatique, et se tromperait une fois sur deux sur ces deux cas. **La divergence se vérifie, elle
ne se hiérarchise pas.** Si Maël veut malgré tout un ordre par défaut — utile pour les cas où
aucune vérification externe n'est possible — c'est D15.

---

## 9. Partage des rôles — Maël / agents

### 9.1 Ce qui relève exclusivement de Maël

Reprise de la charte `agents/README.md` (« un agent est un rôle de travail, pas une autorité
scientifique »), appliquée au chantier catalogue :

1. Arbitrer toute divergence entre deux sources (texte / figure / graphe).
2. Geler un vocabulaire (Q7, rôles v2, `statut_ligne`) et autoriser tout renommage.
3. Fusionner deux entités du graphe, ou déclarer une entité canonique.
4. Valider un lot de codage — un lot reste `propose` jusqu'à son mot.
5. Autoriser l'application d'un patch (étape 6 du circuit §5.1).
6. Étendre l'ontologie GRC-20 (types, attributs, relations).
7. Décider qu'une ligne est `exclu`.
8. Corriger le manuscrit quand la vérification donne raison au graphe contre le texte.

### 9.2 Ce qu'un agent peut faire en autonomie

1. Décrire, mesurer, compter, produire un rapport d'audit chiffré et sourcé.
2. Rejouer un script versionné et vérifier qu'il reproduit son artefact à l'octet près.
3. Détecter des divergences et les consigner en CSV d'audit.
4. Produire un patch **candidat** conforme au contrat, jamais appliqué.
5. Proposer un codage en le marquant `propose`, avec sa justification ligne à ligne.
6. Déposer des fichiers, corriger un chemin, ajouter une couleur manquante à un décodeur —
   **avec preuve de non-régression**.
7. Poser une question fermée à Maël plutôt que de choisir à sa place.

### 9.3 Ce qu'un agent ne fait jamais, même autorisé par ailleurs

- Combler un trou par inférence, ni le déclarer sans l'avoir mesuré sur le graphe courant
  (précédent : le faux « domaine (ii) absent », §1.2).
- Traiter le rapport d'un autre agent comme un fait établi (charte, règle 3).
- Coder de force une ligne incertaine : elle reste `[CHANTIER]`.
- Créer une catégorie hors vocabulaire fermé sans le dire.
- Ouvrir une branche ou une PR quand le cadrage l'interdit.

---

## 10. Décisions en attente

Aucune n'est tranchée dans cette page. Les quatre premières bloquent la suite du codage.

| # | Question | Effet si non tranchée |
|---|---|---|
| **D6** | Rôles v2 : colonnes appariées (forme 1) ou table satellite (forme 2) ? | lot 2 impossible |
| **D7** | Qui va dans `acteur_principal` pour une crise exploitée puis résolue — déclencheur ou correcteur ? | les 40 lignes du lot 1 restent `propose` |
| **D11** | Q7 : lancer la passe d'épreuve, ou geler tel quel le vocabulaire provisoire ? | `effet_prop_monetaires` reste non gelable, donc non citable |
| **D4** | Ajouter `statut_ligne` à côté de `codage_statut` ? | pas de snapshot descriptible |
| D1 | Un export catalogue → `public-data/` est-il envisagé pour le site ? | — |
| D2 | `origine` et le préfixe d'`id` : garder les deux, ou supprimer l'un ? | — |
| D3 | Cardinalité 1 graphe → n catalogue : confirmée ? | — |
| D5 | Les lignes exclues figurent-elles au fichier avec un motif ? | — |
| D8 | Un patch issu du catalogue déclare-t-il ses `event_id` d'origine dans `_meta` ? | — |
| D9 | Le codage analytique a-t-il vocation à entrer au graphe (extension d'ontologie) ? | — |
| D10 | Créer `snapshots/` et y figer le v3-1 ? | — |
| D12 | Écrire `scripts/check_catalogue_graphe.py` ? | — |
| D13 | Corriger les 4 documents portant le faux « domaine (ii) absent », ou les laisser avec un renvoi vers §1.2 ? | le constat périmé continue de circuler |
| D14 | `statut_ligne` : valeur unique, ou champ multi-valué ? (E001 est `chantier` **et** `douteux`) | — |
| D15 | Faut-il un ordre de priorité par défaut entre texte / figure / graphe ? | chaque divergence reste à vérifier une par une |

### Chantiers ouverts, indépendants de ces décisions

Ils sont documentés ailleurs et ne sont pas rouverts ici :

- **211 lignes** sans codage analytique (`acteur_principal` / `arene` / `type_acte` renseignés sur
  134/345) — `etat-lot1-codage-2026-08-05.md`
- **80 lignes** sans `domaine_8`, **toutes** `origine=graphe` (mesuré : 80/80) hors frise : la figure
  ne peut pas aider — `etat-catalogue-v3-2026-08-05.md` §5
- **30 lignes** dont le `domaine_8` porte le suffixe `*` (attribution par définition, code couleur
  non vérifié)
- **13 paires `A_VERIFIER`** et **7 paires bloquées par types différents** —
  `PASSATION-claude-code-dedup-events.md` §6
- **6 lignes du catalogue contredisent le domaine porté par le graphe** (relevé de v103,
  `grc20-domaines-developpement-v1.md`) — signalées, non tranchées.
- Chronologies **Altcoin V0.1** et **HF d'Ethereum V1** présentes au dépôt, non décodées : gisement
  pour une v4.

---

## Sources de cette page

**Cadrage** — `docs/audits/PROMPT-COWORK-catalogue-graphe-site.md` (BLOC C, verbatim de Maël) ·
`agents/README.md` (charte) · `CLAUDE.md` (discipline de travail, ordre d'autorité).

**Grille et états** — `docs/audits/grille-codage-catalogue-v1.md` ·
`docs/audits/etat-catalogue-evenements-2026-07-19.md` ·
`docs/research/catalogue-evenements/etat-catalogue-evenements-v2-2026-08-02.md` ·
`docs/audits/etat-catalogue-v3-2026-08-05.md` · `docs/audits/etat-lot1-codage-2026-08-05.md` ·
`docs/audits/etat-dedup-patch-2026-08-02.md` · `docs/audits/PASSATION-claude-code-dedup-events.md`.

**Contrat et gouvernance des patchs** — `docs/audits/grc20-candidate-patch-contract-v1.md` ·
`docs/audits/data/patch-application-queue-current.csv` ·
`docs/audits/data/patch-queue-governance-cases-current.csv` · `patch-application-ledger.json` ·
`docs/audits/patch-queue-lifecycle-policy-draft.md`.

**Données mesurées le 2026-08-15** — `docs/research/catalogue-evenements/catalogue-evenements-v3-1.csv`
(345 lignes) · `grc20-these-mael-rolland-v115.json` (2 293 entités, 20 211 relations) ·
`docs/audits/data/doublons-verifies.csv` ·
`docs/research/catalogue-evenements/table-divergences-dates.csv`.

**Architecture existante** — `docs/architecture/research-architecture-vnext.md` ·
`docs/architecture/schema-vnext.md`.

---

## Annexe — écarts de documentation relevés au passage

Signalés, non corrigés (hors mandat de cette session) :

| Fichier | Ce qu'il dit | Mesuré le 2026-08-15 |
|---|---|---|
| `CLAUDE.md` | « v113 is the current canonical snapshot » | `space.version = v115` ; les 15 occurrences du nom de fichier, dans les 7 fichiers concernés, visent toutes v115 |
| `CLAUDE.md` (2 fois) | `preflight_candidate_patches.py` : « 12 checks » | **13** (`C01..C13`, le 13ᵉ couvre `ADD_RELATION`) |
| `PASSATION-…-dedup-events.md` §6.7 et §8 | « le graphe n'a aucun domaine (ii) » | faux depuis v102 (§1.2) |
| `docs/audits/grc20-dedup-events-audit-v1.md` §7 | idem | idem |
| `etat-catalogue-evenements-v2-2026-08-02.md` | idem | idem |
| `docs/research/catalogue-evenements/README.md` | idem | idem |
| `docs/audits/grc20-domaines-developpement-v1.md` | « 67 relations », « 30 `belongs to domain` » (v102) | 103 et 31 sur v115 — chiffres d'époque, non périmés au sens strict, mais à ne pas recopier |
| `docs/research/catalogue-evenements/README.md` | `fusion.py` « versé tel qu'il a été écrit », chemins hors dépôt | exact — `scripts/verif_doublons.py` a reçu une interface CLI, `fusion.py` non |

`[À ARBITRER — D13]` porte sur les quatre lignes « domaine (ii) ».
