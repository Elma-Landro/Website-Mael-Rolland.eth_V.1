# GRC-20 v113 — retypages bibliographiques

**Date** : 2026-08-09
**Graphe source** : `grc20-these-mael-rolland-v112.json`
**Graphe produit** : `grc20-these-mael-rolland-v113.json` — **canonique**
**Applicateur** : `scripts/make_v113_apply_bibliography_retypes.py` — `--dry-run` pour valider sans écrire, invocation nue (`python3 scripts/make_v113_apply_bibliography_retypes.py`) pour produire le graphe
**Patch appliqué** : `patch_candidate_bibliographie_retypes_v1.json` — 10 ops
**Instruction** : Patch Application Queue Master Triage v1, `docs/audits/grc20-patch-application-queue-v112.md`
**Arbitrage** : Maël Rolland, 2026-08-09, questions 1 à 4 — toutes positives

Deuxième application de la file. Un lot borné, une famille de correction, une version.

---

## 1. Ce que v113 change — six fiches, rien d'autre

| Entité | v112 | v113 |
|---|---|---|
| `53525938…` | **Jérôme** Favier · `Reference` | **Jacques** Favier · `Person` |
| `7cd4cfe4…` | **Guillaume** Dréan · `Reference` | **Gérard** Dréan · `Person` |
| `be8ac286…` | **Gregor** Loibl · `Reference` | **Andreas** Loibl · `Person` |
| `ec901513…` | **Audrey** Takkal Bataille · `Reference` | **Adli** Takkal Bataille · `Person` |
| `5fc4278b…` | Laura DeNardis · `Reference` | Laura DeNardis · `Person` |
| `b332ace8…` | Shinobi (pseudonyme) · `Reference` | Shinobi (pseudonyme) · `Person` |

**Le graphe attribuait un prénom inventé à quatre auteurs réels et vivants.** Les quatre prénoms corrigés sont attestés mot pour mot dans `assets/MD/07_bibliographie.md`, vérifiés à la ligne :

```text
l.476  FAVIER Jacques et TAKKAL BATAILLE Adli, 2017, Bitcoin, la monnaie acephale
l.756  LOIBL Andreas, 2014, « Namecoin »
l.414  DREAN Gerard, 2013, « Au-dela de Bitcoin (5) »
l.472  FAVIER Jacques, 2021
l.394  DENARDIS Laura et MUSIANI Francesca, 2014   (nom deja juste)
l.1128 SHINOBI, 2022                                (pseudonyme, nom deja juste)
```

Les six fiches sont le **reliquat du lot `patch_18`**, qui avait retypé 21 fiches d'auteur et laissé celles-ci de côté.

**Écrire un nom de personne est une décision d'auteur.** La charte le réserve à Maël Rolland, et le dépôt en porte le précédent : un patch a failli graver « Florence Dufy », nom soudé de deux co-auteurs réels. Les six opérations ont été arbitrées explicitement, questions 1 et 2 du triage. L'applicateur n'a rien décidé : il exécute un lot figé et refuse tout ce qui s'en écarte.

---

## 2. Preuve qu'aucune autre donnée n'a bougé

Comparaison v112 / v113 refaite **indépendamment de l'applicateur** :

```text
entites 2293 -> 2293        relations 20207 -> 20207   (identiques)
types / relation_types / ops : identiques
memes ids d entites : True   creations : 0   suppressions : 0
cles d attributs identiques (noms ET effectifs) : True
entites modifiees : 6        attributs des 6 fiches : INCHANGES
space : seules `version` et `note` changent      note : 1191 caracteres
```

Aucune relation posée, aucun nœud créé, aucune fusion, aucun attribut touché, aucune SourceQuote.

L'applicateur porte le même contrôle : il compare le résultat à la source **champ de tête par champ de tête, attribut par attribut, relation par relation**, sans liste de champs écrite à la main — la leçon de v112, où une projection ratait les trois entités portant une clé `type` au singulier. Il n'écrit que si le diff vaut exactement 6 `types` et 4 `name` modifiés.

---

## 3. Le lot est figé dans le script, valeurs comprises

`LOT_APPROUVE` reproduit pour chaque fiche le **nom actuel, les types actuels, le nom cible et les types cibles**. Figer les seuls identifiants laisserait un patch retouché réécrire la cible — défaut trouvé par la revue de v112 et corrigé ici dès l'écriture.

Deux garde-fous propres à ce lot :

- **une fiche dont le nom est déjà juste ne peut pas être renommée.** `nom_cible = None` pour DeNardis et Shinobi : toute op `SET_NAME` les visant est refusée. Renommer une personne hors arbitrage est exactement ce que ce script existe pour empêcher.
- **aucun renommage ne peut créer un homonyme** : le nom cible est confronté à tous les noms du graphe avant écriture.

Neuf refus provoqués, aucun fichier écrit dans aucun cas :

| Situation | Constaté |
|---|---|
| cible == source | exit 2 |
| cible en v114 | exit 2 |
| source en v111 (mauvaise version) | exit 2 |
| entité hors lot figé | exit 1 |
| nom cible réécrit (« Jean Dupont ») | exit 1 |
| renommage d'une fiche à nom déjà juste | exit 1 |
| op `SET_ATTRIBUTE` ajoutée (11 ops) | exit 1 |
| types cibles réécrits | exit 1 |
| policy `CANDIDATE` retirée | exit 1 |

---

## 4. Hors périmètre, par arbitrage explicite (question 4)

Fusions, doublons (`patch_candidate_bibliographie_duplicates_v1.json`, 156 ops), créations de nœuds (`…missing_nodes…`, 38 `CREATE_ENTITY` qu'aucun applicateur ne consomme), familles bibliographiques et arbitrages de canonique : **tous restent hors v113**.

Restent également intouchés : SourceQuote, l'identité BitcoinTalk, Mining pools, les doubles descriptions, et les dettes chronologiques de v112.

---

## 5. Effet de bord mesuré sur la file de patchs

Le CSV de file se régénère sur le graphe courant. Après v113, **un seul statut change** : `patch_candidate_bibliographie_retypes_v1.json` passe de `stale_source_graph_but_preconditions_intact` à `already_applied` (21 au lieu de 20). C'est l'effet attendu. **Mais la file ne se tient pas à jour toute seule** : `build_patch_queue_inventory.py --check` **n'est pas dans les 8 étapes de la CI**, et rien ne s'apercevrait qu'elle est périmée. Il faut la régénérer à la main après chaque version.

Le fichier a été renommé `patch-application-queue-v113.csv` : son nom suit désormais le graphe de référence. Un CSV nommé v112 décrivant v113 aurait menti en silence — c'est le piège déjà constaté sur `audit_chronology_dates.py`.

> **Suite (2026-08-09, arbitrage Q6 du *Patch Queue Governance Lab*).** La règle ci-dessus a été conservée mais déplacée : renommer le CSV à chaque version obligeait à mettre à jour tous les pointeurs et laissait derrière soi des fichiers de versions mortes indiscernables des preuves figées. Le fichier vivant s'appelle désormais `patch-application-queue-current.csv` ; **seul** un lancement contre un graphe qui n'est pas le courant écrit un `patch-application-queue-vNN.snapshot.csv`. Le motif reste le même — un fichier ne doit pas pouvoir mentir sur ce qu'il décrit — mais l'écrasement silencieux d'un CSV de version par les données d'une autre est maintenant impossible plutôt que seulement déconseillé.

---

## 6. Limite connue

**Aucune vérification navigateur — et l'exception coûte plus cher ici qu'en v112.** Le *diff de fichiers* est borné aux pointeurs de version ; **le comportement ne l'est pas**. La revue hostile a mesuré que le retypage `Reference → Person` traverse quatre filtres par type : `NEBULA_LEAF_TYPES` (les six cessent d'être des points-feuilles périphériques), `REF_TYPES`/`getDepth` (bande « Références » → bande « Entités sémantiques »), la couleur/forme/taille, et `GRAPH_SKIP_TYPES` de `lecteur.html` (les six deviennent éligibles comme voisins à un saut — au plus six nœuds nouveaux, chacun tiré par sa seule référence). **Dire « borné aux pointeurs » était donc vrai du diff et faux de l'écran.**

Deux constats de la revue à porter au dossier, tous deux vérifiés : la colonne d'affichage **ne change pas** — le défaut `embedded_persons ? 5 : 7` maintient les six en colonne 7, aucune n'ayant de voisin empirique — mais `V3_PERSON_COL`, la table de rattrapage écrite lors du retypage v110, **n'a pas été étendue** à ces six noms : une seule relation future vers un `Protocol` ou une `Institution` ferait basculer Jacques Favier en colonne « Acteurs ». Et `narrative-anchors.json` régénéré sur v112 et v113 est **identique feuille pour feuille**. `node_modules` est absent, les CDN sont bloqués, `playwright install` est interdit par la charte. Remplacement : `node --check` sur les quatre `.mjs`, diff runtime inspecté et borné aux pointeurs, six validations de graphe vertes. Même exception que v112, acceptée par l'auteur à condition d'être énoncée.
