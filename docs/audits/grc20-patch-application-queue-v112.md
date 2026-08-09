# GRC-20 Patch Application Queue — Master Triage v1

**Date** : 2026-08-09
**Graphe de référence** : `grc20-these-mael-rolland-v112.json` (canonique)
**Branche** : `claude/file-upload-branch-check-jw4cng`
**Mécanisme rejouable** : `scripts/build_patch_queue_inventory.py` (`--csv`, `--check`)
**Données probantes** : `docs/audits/data/patch-application-queue-v113.csv` — 30 artefacts

> **Note de lecture.** Le triage a été fait sur v112 et ses chiffres ci-dessous sont ceux de v112. Le CSV, lui, est une **file vivante** : son nom suit le graphe de référence, et il a été régénéré sur v113 dans la même PR. Un seul statut change — `patch_candidate_bibliographie_retypes_v1.json` passe de `stale_source_graph_but_preconditions_intact` à `already_applied`, ce qui est précisément l'effet de v113. Le CSV se régénère par `--csv` et se vérifie par `--check` contre le graphe courant.

**Aucun graphe modifié par ce triage lui-même.** Il n'a rien appliqué : il a mesuré, classé, et posé quatre arbitrages. La v113 qui suit est un acte distinct, décidé par l'auteur au vu de ce triage, et documentée séparément dans `grc20-v113-bibliography-retypes-application.md`.

> Rappel de la charte : un agent est un rôle de travail, pas une autorité scientifique. Le § 4 pose quatre arbitrages ; ils ont été posés **directement dans le fil de discussion**, pas seulement ici.

---

## 1. Le principe qui a guidé le classement

**Le statut d'un patch ne se lit jamais dans le patch.** Il se mesure dans le graphe courant : pour chaque opération lisible, l'effet est-il déjà là ?

C'est ce qui permet de trancher un cas que la lecture naïve rate. `patch_candidate_section_page_start_v1.json` et `patch_candidate_chronology_dates_v1.json` portent tous deux, en toutes lettres, `CANDIDATE — NOT APPLIED — AUTHOR ARBITRATION REQUIRED`. **Ils sont pourtant appliqués** — le premier par `make_v111`, le second par `make_v112`. La mention survit parce que la convention du dépôt l'exige : le contrôle C03 de `preflight_candidate_patches.py` la vérifie, et les applicateurs refusent un patch qui ne la porte pas. Un agent qui lirait la `policy` conclurait que ces deux patchs attendent un arbitrage. L'inventaire mesure 16/16 et 2/2 opérations déjà réalisées, et tranche.

---

## 2. Inventaire — 30 artefacts

| Statut | n | Ce que cela veut dire |
|---|---:|---|
| `already_applied` | 20 | toutes les ops lisibles ont déjà leur effet dans v112 |
| `indetermine` | 7 | état mixte, ou dialecte illisible — **statut non établi** |
| `stale_source_graph_but_preconditions_intact` | 2 | rien n'est appliqué, la source déclarée est périmée, mais les cibles portent encore leur valeur d'origine |
| `blocked_by_missing_applicator` | 1 | 38 `CREATE_ENTITY` qu'aucun applicateur du dépôt ne consomme |

### Les deux patchs déjà mangés — prouvés, pas supposés

| Patch | Appliqué par | Preuve mesurée |
|---|---|---|
| `patch_candidate_section_page_start_v1.json` | `make_v111` | **16/16** ops réalisées dans v112 |
| `patch_candidate_chronology_dates_v1.json` | `make_v112` | **2/2** ops réalisées dans v112 |

**Proposition documentaire, aucune suppression** : ces deux fichiers doivent rester en place et garder leur `policy` (la CI l'exige). Ce qui manque n'est pas dans le patch mais **autour** : `docs/audits/data/candidate-patch-inventory-v1.csv` est un instantané de v110 qui ignore ces deux applications. Le présent CSV le remplace de fait ; l'ancien n'est pas modifié.

### Les sept `indetermine` — et pourquoi ils le restent

Cinq sont des patchs **historiques en état mixte** : `patch_1b` (770/774), `patch_2c` (248/274), `patch_5` (141/147), `patch_4` (105/111), `patch_11` (27/31). Ils ont été absorbés il y a longtemps, et les quelques ops non réalisées visent des cibles mortes ou ont été remplacées par des migrations ultérieures. **Un rejeu naïf échouerait ou écrirait à côté.** Ce ne sont pas des candidats : ce sont des archives.

Deux ne portent aucune opération au sens du script — `patches/archive/grc20_anchor_overrides_targeted.json` (structure `safe_fix` / `proposed_review`) et `patches/grc20_v97_remove_15_truncated_broken_relations.json` (reçu d'opération, pas patch). Statut **non établi**, à instruire à la main.

### Deux pièges de lecture, corrigés dans le script

- Dans les dialectes `relations` / `new_relations`, la clé `type` ne porte **pas** un type d'opération mais l'**identifiant du type de relation**. La lire comme un type d'op rendait huit patchs illisibles — 0 op lisible sur ~500 — et les classait `indetermine` à tort.
- `page_start` et `type` entrent dans le `readBy` du registre par pur effet lexical : le premier n'est qu'un libellé de famille dans ce script, le second un champ d'op de patch. Déclarés dans `EXCLUSIONS_READ_BY` après vérification occurrence par occurrence.

---

## 3. Familles — ce qui est mûr, ce qui ne l'est pas

| Famille | Verdict | Motif |
|---|---|---|
| **A. Bibliographie — retypages** | **seul lot mûr** | 10 ops, préconditions intactes, aucune relation, aucun nœud, aucune fusion |
| B. Bibliographie — doublons | bloqué par arbitrage | 156 ops `duplicateOf` : canonique, degré, homonymies. Même piège C5 que Mining pools |
| C. Bibliographie — créations | bloqué par applicateur | 38 `CREATE_ENTITY` ; aucun applicateur ne consomme ce type, le contrat interdit de pré-assigner un `entityId` |
| D. SourceQuote | préparable, non applicable | 41 ops vérifiées, mais coupes non signalées, doublons, mauvais rattachements, P3-10 gelée |
| E. Chronologie | épuisée pour l'instant | Heartbleed et BitcoinTalk appliqués en v112 ; le reste dépend de `dateSource`, de l'identité BitcoinTalk, des figures absentes, de The DAO non vérifié |
| F. Identité / doubles descriptions / Mining pools | hors micro-version | chantier de modèle, pas un patch borné |

### Pourquoi A est mûr — vérifié sur v112, pas déduit de v110

`patch_candidate_bibliographie_retypes_v1.json` porte **10 ops sur 6 entités** : 6 `SET_TYPES` (Reference → Person) et 4 `SET_NAME`.

**Les 6 entités sont inchangées de v110 à v112** — nom, types et attributs identiques dans les trois versions, vérifié valeur par valeur. Les préconditions du patch tiennent donc malgré sa `source_graph` périmée. Aucune op ne crée de relation, de nœud ou de fusion.

**Deux retypages purs** — aucun renommage, la fiche porte déjà le bon nom :

| Entité | Nom | v112 | Cible |
|---|---|---|---|
| `5fc4278b` | Laura DeNardis | `Reference` | `Person` |
| `b332ace8` | Shinobi (pseudonyme) | `Reference` | `Person` |

**Quatre rename-then-retype** — et c'est là que la décision cesse d'être technique :

| Entité | Nom dans v112 | Nom proposé | Attesté par la thèse |
|---|---|---|---|
| `ec901513` | Audrey Takkal Bataille | **Adli** Takkal Bataille | `07_bibliographie.md` l.476 |
| `be8ac286` | Gregor Loibl | **Andreas** Loibl | l.756 |
| `7cd4cfe4` | Guillaume Dréan | **Gérard** Dréan | l.414 |
| `53525938` | Jérôme Favier | **Jacques** Favier | l.472, l.474, l.476 |

Les quatre noms proposés sont **confirmés mot pour mot par la bibliographie de la thèse**, vérifiée à la ligne. Autrement dit : **le graphe attribue aujourd'hui un prénom inventé à quatre auteurs réels et vivants.** Laura DeNardis (l.394) et SHINOBI (l.1128) sont également attestés.

**C'est précisément la classe d'écriture que la charte réserve à l'auteur** — « anything that would engrave a claim about a person ». Le dépôt en porte le précédent : un patch antérieur a failli graver « Florence Dufy », un nom soudé de deux co-auteurs réels. Le fait que la correction aille ici dans le bon sens ne change pas qui décide.

---

## 4. Arbitrages posés à l'auteur

Posés dans le fil de discussion le 2026-08-09, et reportés ici pour que ce document se suffise :

1. Appliquer les **2 retypages purs** (DeNardis, Shinobi) ? **oui / non**
2. Appliquer les **4 rename-then-retype** ? **oui / non / par cas**
3. Créer **v113 pour ce seul lot** ? **oui / non**
4. Garder **fusions, doublons et créations bibliographiques hors périmètre** ? **oui / non**

**Réponse rendue le 2026-08-09 : les quatre questions sont positives.** Les 2 retypages purs et les 4 rename-then-retype sont validés, v113 est créée pour ce seul lot, et fusions, doublons et créations restent hors périmètre. L'application est documentée dans `grc20-v113-bibliography-retypes-application.md`.

---

## 5. Ce que ce triage ne fait pas

- **Il ne supprime aucun fichier** et ne modifie aucun patch. Les propositions du § 2 sont documentaires.
- **Il ne rejoue rien.** Les cinq patchs historiques en état mixte sont signalés comme archives, pas comme candidats.
- **Il ne tranche pas les sept `indetermine`.** Un statut non établi est écrit comme tel, avec ce qui manque pour l'établir.
- **Il ne relance pas SourceQuote.** Aucun zip de `Migration/` n'est ouvert ; ils ne contiennent pas de patch au format du dépôt et leur vérification (41 ops) est déjà instruite ailleurs, gelée sur arbitrage.

## 6. Corrections apportées après revue hostile

- **Le périmètre annoncé était faux.** Le glob `patch*.json` ratait `new_relations_patch.json` — **3 Mo, 11 884 ops**, le plus gros artefact du dépôt, nommé dans CLAUDE.md — parce que son nom ne *commence* pas par « patch ». Le glob est désormais `*patch*.json`, et la file compte **31 artefacts**, non 30.
- **Et l'avoir raté masquait un défaut de lecture.** Ce fichier porte `type: "ADD_RELATION"` **et** `relation_type: "appears_in_section"` : le code prenait le type d'*opération* pour le type de *relation*, résolvait vers `None`, et aurait déclaré **0 op réalisée sur 11 884** — un lot intégré depuis v72 présenté comme candidat. Après correction : **6 246 réalisées**, statut `indetermine` (état mixte), geste « instruire op par op ». Le chiffre a été retrouvé indépendamment par la revue.
- **Le CSV portait le chemin absolu de la machine** dans 21 de ses 30 lignes, ce qui rendait `--check` rouge sur toute autre machine — donc impossible à câbler en CI, et un chemin local versionné. La preuve est désormais relative au dépôt.
- **`already_applied` sur-promet sur quatre lignes** : le statut est calculé sur les ops *lisibles*. `patch_2b_central_arguments.json` est ainsi classé `already_applied` alors que **7 de ses cibles n'existent plus**. La colonne `ops_cibles_absentes` porte l'information et la `preuve` dit « op(s) lisibles » — l'honnêteté est dans les colonnes, l'excès dans le mot. Un lecteur qui trie sur `statut` ne verra pas les 7.

## 7. Limite connue

Le script lit les six dialectes du dépôt par heuristique déclarée. Sur les artefacts sans champ de type et sans cible résoluble, il **refuse de conclure** plutôt que de deviner : c'est pourquoi deux fichiers restent à 0 op lisible. `--check` garantit que le CSV versé est bien la sortie du script sur le graphe courant ; il ne garantit pas que l'heuristique soit complète.
