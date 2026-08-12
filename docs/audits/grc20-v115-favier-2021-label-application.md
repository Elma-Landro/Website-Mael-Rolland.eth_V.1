# GRC-20 v115 — correction du libellé de la fiche Favier 2021

**Date** : 2026-08-11
**Graphe produit** : `grc20-these-mael-rolland-v115.json` (**canonique**)
**Source** : `grc20-these-mael-rolland-v114.json` (**inchangée**)
**Patch appliqué** : `patch_candidate_favier_2021_label_correction_v1.json` — **le seul**
**Applicateur** : `scripts/make_v115_apply_favier_2021_label_correction.py`
**Arbitrages** : Maël Rolland, 2026-08-11 (forme A ; substitution ciblée après test à blanc)
**Instruction** : `grc20-favier-2021-label-correction-lab-v1.md` (PR #125)

**Un seul nom change, à 21 endroits, et rien d'autre.**

> « Favier 2021 — Bitcoin et la religion **(La voie du Bitcoin)** »
> → « Favier 2021 — Bitcoin et la religion **(podcast Parlons Bitcoin)** »

---

## 1. Les trois preuves, séparées

L'auteur les a exigées distinctes, et le motif compte : les mélanger dans un diff global masquerait précisément ce que le chantier d'instruction a mis au jour — que la couche canonique et la couche dénormalisée peuvent diverger sans qu'aucun signal ne l'annonce.

### Preuve 1 — le changement canonique

| Bloc | v114 | v115 |
|---|---:|---:|
| entités | 2 293 | 2 293 |
| relations | 20 211 | 20 211 |
| `relations`, `types`, `relation_types`, `ops` | — | **identiques** |

**Une seule entité diffère** — `7f0f9cc4` — et **un seul de ses champs** : `name`. L'ordre des identifiants est inchangé. `b84f59ac`, la fiche témoin, est **identique octet pour octet**.

### Preuve 2 — les 20 libellés dénormalisés

| Fichier | Champ | Lignes changées |
|---|---|---:|
| `entity_section_map.json` | `name` | **1** |
| `section_entities_map.json` | `entity_name` | **19** |

`git diff` sur les deux cartes : **+20 / −20**, et **zéro ligne ne portant pas la substitution**. Les 19 emplacements sont figés dans l'applicateur par leur clé de section ; il n'y a aucun remplacement global.

### Preuve 3 — l'absence de tout autre effet

- **12 355 lignes de `section_entities_map.json` intactes** sur 12 374.
- Ancien libellé restant dans tout le dépôt hors archives de versions : **0**.
- Diff runtime : **8 fichiers, 16 lignes, uniquement des pointeurs `v114 → v115`**.

---

## 2. Le contrôle exhaustif — et ce qu'il a révélé

Demandé par l'auteur : comparer, pour **chaque** entrée résoluble des deux cartes, le nom dénormalisé au nom canonique du graphe. `scripts/check_map_entity_names.py`, lecture seule, sans correctif.

| | Avant v115 | Après v115 |
|---|---:|---:|
| `entity_section_map.json` (1 171 entrées) | 0 divergence | 0 |
| `section_entities_map.json` (12 374 entrées) | 0 divergence | 0 |
| **Total sur 13 545 entrées résolues** | **0** | **0** |

**Le résultat mérite d'être lu correctement, car il n'est pas celui qu'on attendait.** Avant v115 la dérive n'était pas de 20 : elle était de **zéro**. Les cartes reflétaient fidèlement un graphe qui était lui-même faux. Les « 20 cas » n'étaient pas une désynchronisation existante — c'étaient les 20 endroits qui *allaient* diverger dès que le graphe serait corrigé, et que ce lot corrige dans le même mouvement.

**Réponse à la question posée** : oui, les 20 constituent bien l'ensemble — il n'existe aucun autre cas de divergence `entity_name`, ni avant ni après.

### Une découverte hors périmètre, signalée et non traitée

Le contrôle exhaustif a fait apparaître un **second champ dénormalisé** dans `entity_section_map.json` : `type`, présent sur les 1 171 entrées. **44 d'entre elles divergent du graphe** — par exemple `5d620327` porte `ActorNonHuman` dans la carte contre `CodeRepository` dans le graphe, `a444085b` porte `Concept` contre `CoreConcept`.

Ce sont de **vraies divergences actuelles**, sans rapport avec Favier. Elles ne sont **pas** traitées ici : hors périmètre v115, et matière du chantier séparé sur l'architecture de cet artefact. Aucune correction automatique n'a été faite.

---

## 3. Pourquoi une substitution ciblée, et non une régénération

Le test à blanc du 2026-08-11, demandé par l'auteur avant toute écriture, a établi que **la régénération est un no-op sur ce champ** : `build_anchor_weights.py --apply` produit 0 changement, et les 20 libellés fautifs restent.

La cause est structurelle. `build_anchor_weights.py` n'écrit que `snippet_status` et `direct_anchor_count` ; `fix_dead_ids_in_section_map.py` ne touche le nom qu'en réparant un identifiant mort ; et `entity_section_map.json` **n'a aucun script écrivain** dans le dépôt.

**Ces cartes ne sont pas désynchronisées malgré un pipeline de synchronisation : elles portent un champ dénormalisé sans aucun mécanisme de synchronisation.** La nuance décide de la méthode — il n'y a rien à relancer.

---

## 4. Ce que l'applicateur refuse

Le lot est figé : identifiant, ancien nom, nouveau nom, et **les 19 clés de section** énumérées une à une. Refus vérifiés :

| Ce qui est refusé |
|---|
| op autre qu'un `SET_NAME` |
| op visant une autre entité |
| op posant une autre valeur que la forme A arbitrée |
| `currentValue` déclarée ≠ ancien nom |
| `policy` ne portant pas le marquage CANDIDATE |
| `_meta.arbitrage` absent |
| nom cible déjà porté par une autre fiche (homonyme) |
| carte dont le nom n'est pas l'ancien |
| **une autre entité portant le même ancien libellé** — la substitution ciblée refuse de choisir |
| sections trouvées ≠ les 19 attendues |
| cardinalité ≠ 1 et 19 |
| diff du graphe ≠ exactement le renommage |
| une ligne de carte changée ne portant pas la substitution |
| nombre de lignes d'une carte modifié |

### Deux défauts corrigés en cours de route

**Un saut de ligne parasite.** La première exécution ajoutait un `\n` final aux deux cartes, qui n'en portaient pas — le diff faisait alors +2/−2 et +20/−20 au lieu de +1/−1 et +19/−19. Minuscule, mais c'est une modification collatérale, et la consigne dit « rien d'autre que les substitutions ». L'applicateur préserve désormais la terminaison d'origine. Les cartes ont été restaurées et le lot rejoué depuis un état propre.

**Un message trompeur après application.** Rejoué sur un dépôt déjà corrigé, l'applicateur disait « la carte a dérivé, ré-instruire » — alors que la carte porte simplement la valeur cible. C'est le même défaut que C13 en v114 : *un contrôle juste avant l'application devient faux après*. Il dit désormais « ce lot est DÉJÀ APPLIQUÉ ».

---

## 5. Ce qui n'a pas été fait

- **`b84f59ac` n'est pas touchée** — c'est là que « La voie du Bitcoin » est **juste**. Vérifié identique entre v114 et v115.
- **Aucun `title` ni `year` ajouté** à `7f0f9cc4`, qui reste la seule des trois fiches Favier sans attribut. Dette séparée, hors périmètre par l'arbitrage 2.
- **Aucun `--refresh-names` écrit.** L'auteur a renvoyé le mécanisme de synchronisation à un chantier distinct ; ce lot n'en construit aucun. `check_map_entity_names.py` **constate** et ne répare rien.
- Aucun nœud, aucune relation, aucun `authored`, aucune fusion, aucun `duplicateOf`, aucune `SourceQuote`, aucun retypage.
- **Le doublon DeNardis** (`e0b40d91` / `2272e5b8`), Favier 1981 et Favier 2018 restent hors périmètre.

---

## 6. Le chantier suivant, tel que l'auteur l'a cadré

À ouvrir séparément, sur l'architecture de `entity_section_map.json` :

- qui possède et génère cet artefact ?
- quelle est la source de vérité de `entity_name` ?
- faut-il réellement persister ce nom dénormalisé ?
- si oui, quel mécanisme assure sa synchronisation ?
- faut-il câbler un `--check` de cohérence `entity_id → entity_name` en CI ?
- faut-il un vrai générateur, ou seulement un rafraîchisseur déterministe ?

Les **44 divergences de `type`** relevées au § 2 lui appartiennent aussi : elles montrent que la question dépasse le seul champ `name`.

`scripts/check_map_entity_names.py` sort en code 1 s'il reste une divergence — de quoi le câbler le jour où l'auteur décidera que la cohérence est un invariant. Il ne l'est pas aujourd'hui.

---

## 7. Limites connues

- **Aucune vérification navigateur.** Le diff runtime est borné aux pointeurs, mais un libellé change ce que l'écran affiche : `graphe.html` et `lecteur.html` étiquettent leurs nœuds avec `name`. L'effet attendu est un libellé corrigé sur une fiche, et rien d'autre ; ce n'est pas prouvé ici.
- **La preuve reste bibliographique, pas éditoriale.** Le nom « Parlons Bitcoin » vient de l'URL et du contexte de l'entrée `:472` ; l'accès réseau ne permet pas de vérifier que l'éditeur se désigne ainsi aujourd'hui.
- **Le CSV d'instruction est figé sur v114 et le reste.** Ses deux lignes de cartes portent désormais les comptes **au diagnostic** (19 et 1), figés : les recompter aurait effacé la trace du problème que le relevé documente, puisqu'ils valent 0 depuis v115.
