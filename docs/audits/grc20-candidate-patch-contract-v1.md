# Contrat de patch candidat v1 — six dialectes constatés, un seul prescrit

**Date** : 2026-08-07
**Graphe** : `grc20-these-mael-rolland-v110.json` (inchangé par ce chantier)
**Branche** : `claude/file-upload-branch-check-jw4cng`
**Mode agent** : A — documentation ; aucun patch modifié, aucun patch créé, aucun graphe touché
**Sources** : les 26 `patch*.json` de la racine + `new_relations_patch.json`, les applicateurs `scripts/make_v98/v99/v100/v105/v107/v110*.py`, `docs/audits/grc20-dedup-events-audit-v1.md` (constat C3), `grc20-properties-registry-v1.json`, `scripts/check_graph_integrity.py`
**Portée** : ce contrat oblige les **futurs** patchs candidats. Il ne réécrit aucun patch existant (voir § 4).

---

## 0. Pourquoi un contrat, et pourquoi minimal

Le dépôt a produit 27 fichiers de patch JSON en six dialectes incompatibles (l'inventaire `candidate-patch-inventory-v1.csv` recense 32 artefacts en comptant les zips, reçus et fichiers hors dialecte). Ce n'est pas une
hypothèse : l'incident C3 de `grc20-dedup-events-audit-v1.md` (§ 2 ci-dessous) montre
qu'un patch a déjà été émis dans un **hybride de deux dialectes** qui ne correspondait
exactement à aucun, précisément parce qu'aucun document ne disait lequel suivre. Chaque
applicateur `make_vNNN` a dû recoder sa propre validation. Le présent contrat fixe le
minimum que doit respecter tout futur patch candidat — fondé sur ce qui existe et
fonctionne déjà (le dialecte consommé par `make_v110`), pas sur un format idéal.

---

## 1. Inventaire des dialectes existants

Chaque affirmation ci-dessous est vérifiée sur le fichier réel (clés exactes citées).

### 1.a Les six dialectes

| Dialecte | Enveloppe | Clé d'op | Champs d'op | Valeur | Fichiers | Applicateur dans le dépôt |
|---|---|---|---|---|---|---|
| **A — « 2b »** | `patch_id` + `description` + `operations` | `op` | `entity_id`, `entity_name`, `attribute_name` | **nue** (chaîne) | `patch_2b_central_arguments.json` (56 `SET_ATTRIBUTE`) | **aucun** |
| **B — relationnel à plat** | `description` + `source_graph` + `operations` + `summary` (1b ajoute `generated`, `chapter_entity_ids`, `cited_in_relation_type_id` ; 2a remplace par `graph_version`, `relation_type_id`, `relation_type_name`) | `op` | `from_entity_id`, `to_entity_id`, `relation_type` (**nom**, ex. `"cited_in"`) + annotations `note`, `entity_name`, `wrong_chapter`, `relation_id`, `correct_chapter` | — | `patch_1a_fix_cited_in.json` (22 `REMOVE_RELATION` + 22 `ADD_RELATION`), `patch_1b_missing_cited_in.json` (774 `ADD_RELATION`), `patch_2a_sourcequote_subsections.json` (207 `ADD_RELATION`, **sans** `relation_type` par op — porté par l'enveloppe) | **aucun** |
| **C — canonique « 2c »** | `_meta` + `ops` (2c : `schemaVersion` + `ops` ; 10 : provenance à plat + `ops`) | `type` | `entityId`, `attributeId` | `{type, value}` ou `{type, value, options}` ; `SET_NAME` : chaîne ; `SET_TYPES` : liste d'ids ; `DELETE_ATTRIBUTE` : sans `value` | `patch_2c_definitions.json` (293 `SET_ATTRIBUTE`), `patch_10` (9 `SET_ATTRIBUTE`), `patch_13` (12 `SET_ATTRIBUTE` + 10 `SET_NAME`), `patch_15` (26 + 20), `patch_18` (1 `SET_NAME` + 21 `SET_TYPES`), `patch_19` (358 `SET_ATTRIBUTE` + 26 `DELETE_ATTRIBUTE`), les 3 `patch_candidate_bibliographie_*_v1.json` | `make_v100` (13, et 15 via `--migration` : le script est paramétrable et a produit v106), `make_v105` (10), `make_v110` (18 + 19) ; `make_v101` purge des ops issues de 2c |
| **D — fragment de graphe** | `_meta` + `new_entities` / `new_relations` (+ `rewire_relations` pour 14/16 ; 3a : `description` + `graph_version` + `update_entities`) | — (déclaratif) | entités et relations **au format du graphe lui-même** : `{id, name, description:{type,value,options}, types, attributes}` ; relations `{id, type(id), from, to, attributes:[]}` | idem graphe | `patch_3a`, `patch_4`, `patch_5`, `patch_11`, `patch_12`, `patch_14`, `patch_16`, `patch_17` | `make_v98` (11), `make_v99` (12), `make_v100` (14, et 16 via `--creation`), `make_v107` (17) ; 3a/4/5 : aucun |
| **E — relations nues** | `{"relations": [...]}`, **aucune métadonnée** | — | `{id (UUID à tirets), from, type(id), to}` | — | `patch_4a_chapter_attribution.json`, `patch_5a_corrective_anchoring.json`, `patch_batch1/2/3_*.json` | aucun (ce sont des **sorties** de `scripts/generate_*.mjs`) |
| **F — liste nue** | tableau JSON de premier niveau, **zéro métadonnée** | `type` | `{type:"ADD_RELATION", from, to, relation_type (nom), attributes:{section_key, page_approx}}` | — | `new_relations_patch.json` (11 884 items, la couche `appears_in_section` de v72) | **aucun** |

### 1.b Types d'opérations observés dans le dépôt

| Type d'op | Où | Consommé par un applicateur ? |
|---|---|---|
| `SET_ATTRIBUTE` | 2b (graphie `op`), 2c, 10, 13, 15, 19, candidat duplicates | oui — `make_v100`, `make_v105`, `make_v110` |
| `DELETE_ATTRIBUTE` | 19 | oui — `make_v110` |
| `SET_NAME` | 13, 15, 18, candidat retypes | oui — `make_v100`, `make_v110` |
| `SET_TYPES` | 18, candidat retypes | oui — `make_v110` |
| `CREATE_ENTITY` | candidat missing_nodes (38 ops) | **non — purement descriptif.** Vérifié : aucun script de `scripts/` ni `.mjs` ne traite `CREATE_ENTITY` ; les créations historiques sont passées par le dialecte D (`new_entities`), chacune avec son applicateur dédié |
| `ADD_RELATION` | 1a, 1b, 2a (clé `op`) ; `new_relations_patch.json` (clé `type`) | non — aucun applicateur dans le dépôt |
| `REMOVE_RELATION` | 1a (clé `op`) | non |
| `UPDATE` | **n'existe nulle part** (grep sur tous les patchs : zéro occurrence). `patch_3a` porte une section `update_entities` (`{id, attribute, value}` nue), mais ce n'est pas un type d'op | non |

Le graphe v110 lui-même journalise dans sa clé de tête `ops` **274 opérations au
dialecte C exact** (`{type, entityId, attributeId, value}`) — reprise de `patch_2c`
moins les 19 ops orphelines purgées en v101. Le dialecte C n'est donc pas seulement le
plus récent : c'est celui que **le graphe parle nativement**.

---

## 2. Incohérences de forme constatées

1. **C3 — l'hybride historique** (`docs/audits/grc20-dedup-events-audit-v1.md`, § C3).
   La version initiale de `patch_10_dedup_events.json` combinait l'enveloppe du
   dialecte A (`operations`, clé `op`) avec les champs du dialecte C
   (`entityId` / `attributeId` / `value:{type,value}`) : il ne correspondait exactement
   à aucun des deux. Résolu en revue de PR par réémission au dialecte C. C'est
   l'incident fondateur de ce contrat.

2. **Même opération, deux graphies de champs.** `patch_2b_central_arguments.json` :
   `{"op": "SET_ATTRIBUTE", "entity_id": "0fcc7028…", "attribute_name": "central_argument", "value": "Les crypto-monnaies…"}`
   contre `patch_2c_definitions.json` :
   `{"type": "SET_ATTRIBUTE", "entityId": "a25fc6eb…", "attributeId": "definition", "value": {"type": "TEXT", "value": "…"}}`.
   Snake_case contre camelCase, valeur nue contre valeur typée — pour la même sémantique.

3. **`ADD_RELATION` existe en trois formes incompatibles.**
   `patch_1b` : `{"op": "ADD_RELATION", "from_entity_id": …, "relation_type": "cited_in", "to_entity_id": …}` (type par **nom**) ;
   `new_relations_patch.json` : `{"type": "ADD_RELATION", "from": …, "to": …, "relation_type": "appears_in_section", "attributes": {"section_key": "intro_C", …}}` (attributs en **dict**) ;
   dialecte D : `{"id": …, "type": "d3b2d5c9…", "from": …, "to": …, "attributes": []}` (type par **id**, attributs en **liste**).
   `patch_2a` va plus loin : ses ops n'ont **pas** de champ de type de relation du tout
   (porté par `relation_type_id` d'enveloppe).

4. **Provenance : de zéro à tout.** `new_relations_patch.json` est un tableau nu sans la
   moindre métadonnée ; `patch_4a`/`5a`/`batch1-3` n'ont que `relations` ; `patch_2c`
   n'a que `schemaVersion` ; `patch_10` porte sa provenance **à plat**
   (`description`, `source_graph`, `generated`, `author`, `policy`) ; `patch_11` à
   `patch_19` et les candidats la portent sous `_meta`. Et dans `_meta` même, `patch_4`
   et `patch_5` disent `"patch"` là où tous les autres disent `"patch_id"`.

5. **Identifiant de patch non unique.** `patch_16_section_creation_corps.json` a porté
   `patch_id: "14"` jusqu'au 03/08/2026, hérité de `patch_14` par copie — documenté dans
   `scripts/make_section_creation_patch.py` (lignes 306-307). Deux patchs distincts,
   même identité déclarée.

6. **Sévérité de validation divergente entre applicateurs.** `patch_10` déclare
   `source_graph: grc20-these-mael-rolland-v97.json` mais a été appliqué à v104 :
   `make_v105` a choisi de vérifier l'existence de chaque entité plutôt que le numéro de
   version (docstring du script). `make_v110`, lui, **refuse** tout patch dont
   `_meta.source_graph` ne correspond pas au graphe source. Le même champ est bloquant
   ici et indicatif là.

7. **Deux régimes d'identifiants.** Les relations de `patch_4a`/`5a`/`batch1-3` portent
   des UUID à tirets (`"2070c1ca-8be4-42e5-…"`) ; tout le reste du graphe et des patchs
   utilise 32 hexadécimaux condensés (`"c4070e12b06b4bf995229ff2df211a65"`).

8. **Dates absentes ou partielles.** `patch_13` et `patch_15` ont un `_meta` sans
   `generated` ; `patch_2c` n'a ni date, ni source, ni description.

---

## 3. Le contrat minimal pour tout futur patch candidat

Prescriptif mais minimal : chaque clause ci-dessous est déjà satisfaite par au moins un
patch existant du dépôt — rien n'est inventé.

### 3.1 Enveloppe obligatoire

Objet JSON de premier niveau à exactement deux clés : **`_meta`** et **`ops`**.
`_meta` porte au minimum :

| Clé | Exigence | Précédent |
|---|---|---|
| `patch_id` | **unique dans le dépôt** (leçon de l'incident patch_16/« 14 ») ; pour les candidats, préfixe `candidate-` | `patch_18`, candidats |
| `source_graph` | nom de fichier exact du graphe contre lequel chaque op a été vérifiée | `patch_18`/`19` |
| `generated` | date ISO (leçon de patch_13/15 qui n'en ont pas) | `patch_18` |
| `description` | ce que fait le patch, chiffré, avec ses sources (audit, CSV) | tous les `_meta` récents |
| `policy` | ce que le patch s'interdit ; **pour un candidat, la chaîne `CANDIDATE — NOT APPLIED — AUTHOR ARBITRATION REQUIRED` en tête de `policy`** | les 3 `patch_candidate_*_v1.json` |
| `skipped` + `skipped_count` | chaque cas examiné et écarté, **motivé un par un** — un patch qui ne dit pas ce qu'il n'a pas osé faire cache ses arbitrages | `patch_18._meta.skipped`, candidats |
| comptes déclarés | `op_count` et `entities_touched` (ou équivalents), **vérifiables mécaniquement** contre `ops` — un applicateur ou une CI doit pouvoir recompter | candidat retypes (`op_count: 10`, `entities_touched: 6`) |

### 3.2 Dialecte d'ops unique : celui de patch_18/19, consommé par `make_v110`

- Enveloppe d'ops : **`ops`** (jamais `operations`), clé d'opération **`type`** (jamais `op`).
- Champs : **`entityId`**, **`attributeId`** (jamais `entity_id` / `attribute_name`).
- `SET_ATTRIBUTE` : `value` = **`{type, value}`** ou `{type, value, options}` — jamais une valeur nue.
- `SET_NAME` : `value` = chaîne. `SET_TYPES` : `value` = liste d'**ids** de types. `DELETE_ATTRIBUTE` : pas de `value`.
- Les clés `_comment` par op sont admises et ignorables (précédent : `patch_13`, `patch_18`, audit dédup § « Format »).
- Justification : c'est le seul dialecte qu'un applicateur en service (`make_v110`)
  valide et applique, et c'est celui que le graphe journalise nativement dans sa clé de
  tête `ops` (274 entrées dans v110).

### 3.3 Règles de validation au dépôt du patch

1. **Tout `entityId` doit exister dans `source_graph`** au moment du dépôt (contrôle
   déjà codé dans `make_v105` et `make_v110` — le patch doit être vérifié *avant* de
   l'exiger de l'applicateur).
2. **Tout id de type** (`SET_TYPES`, `types` d'une création) **doit exister** dans la
   table `types` de `source_graph` (contrôle de `make_v110` sur patch_18).
3. **Toute clé d'attribut nouvelle** (absente de `grc20-properties-registry-v1.json`,
   invariant de CI via `scripts/check_graph_integrity.py`) **doit déclarer son statut
   registre dans `_meta`** : existante (id, domaine, et si le patch étend le domaine),
   ou nouvelle (à inscrire au registre à l'application). Précédent :
   `_meta.registry_note` des candidats duplicates et missing_nodes, qui a permis de
   découvrir que `duplicateOf`/`reviewStatus` existaient déjà au registre avec un
   domaine restreint à `['CrisisEvent', 'InfrastructureEvent']`.

### 3.4 Ce qu'un patch candidat NE DOIT PAS faire

- **S'auto-appliquer.** Un patch est un fichier de données ; l'application passe par un
  script `make_vNNN` dédié, relu, avec `--dry-run` (modèle :
  `scripts/make_v110_apply_bib_and_attribute_patches.py`).
- **Mélanger les dialectes.** Interdiction directe issue de C3 : pas d'enveloppe d'un
  dialecte avec les champs d'un autre.
- **Préassigner des `entityId` pour `CREATE_ENTITY`.** Précédent explicite :
  `patch_candidate_bibliographie_missing_nodes_v1.json` (« aucun id n'est préassigné
  ici ») ; l'assignation d'ids est un acte d'application, pas de candidature. (Les
  patchs D historiques préassignaient des ids, mais avec une `id_derivation` déclarée
  et un applicateur dédié livré en même temps — deux conditions qu'un candidat en
  attente d'arbitrage ne remplit pas.)
- **Toucher aux relations ou fusionner** en se présentant comme un marquage : la
  `policy` fait foi et l'applicateur doit pouvoir la vérifier (modèle : patch_10,
  « marque, ne fusionne pas »).
- **Se dire conforme à un `source_graph` sans avoir été vérifié dessus** : le décalage
  patch_10 (v97 déclaré, v104 appliqué) a été rattrapé par l'applicateur ; le contrat
  met la charge de la vérification côté patch.

---

## 4. Statut des patchs existants au regard du contrat

**Conformes** (dialecte C + `_meta` complet) :
`patch_18_bibliography_fixes.json`, `patch_19_attribute_normalisation.json`, et les
trois candidats `patch_candidate_bibliographie_{retypes,duplicates,missing_nodes}_v1.json`
— missing_nodes au titre de patch **descriptif** : ses 38 `CREATE_ENTITY` déclarent
eux-mêmes qu'aucun applicateur ne les consomme et ne préassignent aucun id.

**Quasi conformes** (dialecte C, provenance incomplète) : `patch_10` (provenance à plat,
pas de `_meta`), `patch_13`/`patch_15` (pas de `generated`), `patch_2c` (`schemaVersion`
seul — mais c'est la source du dialecte lui-même).

**Dérogent** : `patch_2b` (dialecte A), `patch_1a`/`1b`/`2a` (dialecte B),
`patch_3a`/`4`/`5`/`11`/`12`/`14`/`16`/`17` (dialecte D — distinct mais chacun servi
par un applicateur dédié ou une convention documentée), `patch_4a`/`5a`/`batch1-3`
(dialecte E, sorties de scripts sans métadonnées), `new_relations_patch.json`
(dialecte F, tableau nu).

**Pourquoi on ne les réécrit pas.** Tous les patchs dérogatoires sauf les candidats sont
**appliqués** : leur contenu est déjà dans v110 et leur fichier est l'**archive** de ce
qui a été fait, référencée par les audits (`grc20-dedup-events-audit-v1.md` cite le
dialecte de patch_10 tel qu'il est) et par les applicateurs historiques
(`make_v98`…`make_v110` ne rejoueraient plus sur des fichiers réécrits). Les réécrire au
format du contrat falsifierait l'histoire du dépôt sans changer un octet du graphe. Le
contrat oblige les patchs **futurs** ; les anciens restent tels quels, dérogation
documentée ici.

---

## 5. Ce que ce contrat ne décide pas

- **L'applicateur générique.** Chaque `make_vNNN` reste dédié. Un applicateur unique
  lisant le dialecte C est rendu *possible* par ce contrat, pas décidé — il faudra
  arbitrer sa politique de sévérité (le point 2 § 2 montre que le dépôt en a eu deux).
- **Le sort de `CREATE_ENTITY`.** Deux voies existent : promouvoir `CREATE_ENTITY` en
  op consommable (avec assignation d'ids par l'applicateur), ou rabattre les créations
  sur le dialecte D (`new_entities` au format graphe, ids dérivés déclarés). Renvoyé à
  l'arbitrage — le contrat exige seulement qu'un candidat créateur soit descriptif et
  sans ids préassignés en attendant.
- **Les opérations relationnelles au dialecte C.** Aucun applicateur ne consomme
  `ADD_RELATION`/`REMOVE_RELATION` ; leurs trois formes historiques sont incompatibles
  (§ 2.3). Un futur patch candidat relationnel devra faire trancher la forme avant dépôt.
- **La fusion effective des doublons** marqués `duplicateOf`/`reviewStatus` : décision
  humaine postérieure, hors patch (policy de patch_10 et du candidat duplicates).
- **L'extension du registre des propriétés** : le contrat exige la *déclaration* du
  statut registre d'une clé nouvelle, pas la décision de l'admettre — celle-ci
  appartient à l'arbitrage et à la mise à jour de `grc20-properties-registry-v1.json`.
