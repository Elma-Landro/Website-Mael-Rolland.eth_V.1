# GRC-20 — Favier 2021 Label Correction Lab v1

**Date** : 2026-08-11
**Graphe de référence** : `grc20-these-mael-rolland-v114.json` (canonique, **inchangé**)
**Mécanisme rejouable** : `scripts/build_favier_2021_label_correction.py` (`--csv`, `--check`)
**Données probantes** : `docs/audits/data/favier-2021-label-correction-v114.csv` — 9 lignes
**Patch candidat** : `patch_candidate_favier_2021_label_correction_v1.json` — **1 op, NON APPLIQUÉ**

**Aucun graphe modifié. Aucune v115. Aucune relation, aucun `authored`, aucun autre auteur, aucun nœud, aucune fusion, aucune `SourceQuote`, aucun runtime.** Phase d'instruction seulement.

---

## 1. Le constat

`7f0f9cc4` s'appelle **« Favier 2021 — Bitcoin et la religion (La voie du Bitcoin) »**.

L'unique entrée Favier 2021 de la bibliographie donne un **podcast** :

> `07_bibliographie.md:472` — FAVIER Jacques, 2021, « Le Bitcoin, la religion du XXIe siècle née des mathématiques et d'Internet ? », *Jacques Favier - Partie I - PB16*, `https://parlonsbitcoin.com/podcasts/bitcoin-et-religion`, 14 juillet 2021.

Et « La voie du Bitcoin » est l'éditeur d'une **autre** entrée :

> `:474` — FAVIER Jacques, 2017, « Tulipes », `http://blog.lavoiedubitcoin.info/post/Tulipes`, 19 septembre 2017.

Le support de deux entrées distinctes a été recopié sur la mauvaise fiche.

---

## 2. Ce qui n'est **pas** en cause : l'identité de l'œuvre

C'est le point que la revue hostile impose de vérifier avant tout, parce qu'une correction de libellé peut masquer une fiche qui désigne carrément autre chose. Quatre indices convergents, aucun tiré d'une ressemblance de nom :

1. **`:472` est l'unique entrée Favier 2021** de toute la bibliographie — vérifié sur les cinq entrées `FAVIER` du fichier. Il n'y a pas de second candidat.
2. **Le titre concorde** : « Bitcoin et la religion » ↔ « Le Bitcoin, la religion du XXIe siècle ».
3. **L'URL le confirme indépendamment du titre** : le slug de l'enregistrement est `bitcoin-et-religion`.
4. **La thèse cite l'item deux fois**, `01_chapitre_I.md:107`, sous « (Favier 2021) » — dans un passage sur l'« Immaculée Conception » de Bitcoin : « *Il est apparu... sans autre forme de procès* » (Favier 2021).

**La fiche désigne bien la bonne œuvre. Seul son support est faux.**

## 3. Le témoin de non-inversion

L'hypothèse symétrique — les deux entrées inversées, et ce serait `b84f59ac` qui aurait tort — est **réfutée** : `b84f59ac` « Favier 2017 — Tulipes (blog La voie du Bitcoin) » porte cet éditeur **jusque dans son attribut `title`**, et l'entrée `:474` donne bien `blog.lavoiedubitcoin.info`.

Corriger des deux côtés détruirait l'information au lieu de la réparer. Cette fiche figure au CSV avec le verdict **« NE PAS TOUCHER — correct »**, et dans `_meta.skipped` du patch.

Le script refuse d'ailleurs de conclure si l'inversion se présentait : il échoue si `:472` porte « La voie du Bitcoin », si `:474` perd `lavoiedubitcoin`, ou si `:472` perd `parlonsbitcoin`. Éprouvé.

## 4. Sur quel champ la correction peut porter

Les six champs nommants du dépôt ont été **inspectés un par un**, pas supposés :

| Champ | État sur `7f0f9cc4` |
|---|---|
| `name` | **« … (La voie du Bitcoin) »** — le seul à corriger |
| `nameEn`, `labelFr`, `labelEn`, `aliases`, `title` | **absents** |

La fiche ne porte **aucun attribut** — ni `title`, ni `year`, contrairement à ses deux sœurs `b84f59ac` et `e19babe5` qui portent les deux. Son seul appui nommant est `name`. **La correction ne peut donc porter que sur `name`**, et c'est un résultat de la mesure, pas une simplification.

> **Dette séparée, signalée et non traitée** : cette fiche est la seule des trois sans `title` ni `year`. Les lui ajouter serait une *création* d'attributs, hors périmètre de ce chantier.

## 5. L'effet collatéral que rien ne détecte

C'est la découverte qui doit peser dans l'arbitrage. `section_entities_map.json` et `entity_section_map.json` portent `entity_name` **à côté** de `entity_id` — **19 lignes** dans la première, **1** dans la seconde.

Un renommage dans le graphe seul les laisserait porter le libellé faux. Et — vérifié en renommant réellement dans une copie du graphe, puis restauré — **aucun contrôle du dépôt ne le détecte** : `check_anchoring.py`, `build_anchor_weights.py --check` et `check_graph_integrity.py` restent **verts** tous les trois.

La raison est dans `build_anchor_weights.py:189` : `noms.get(eid) or ent.get('entity_name', '')`. L'outillage **préfère le nom du graphe** et ne se rabat sur la carte qu'à défaut. Il ne serait donc pas trompé — mais un lecteur humain, si, et le dépôt porterait une chaîne fausse dans deux fichiers versionnés sans que rien ne l'annonce.

**La régénération des cartes doit appartenir au même lot, ou être explicitement exclue.** C'est l'arbitrage 3.

## 6. Les trois formes possibles

Aucune n'est retenue ici. Le patch candidat porte la **A**, en tant que proposition.

| | Forme | Ce qu'elle fait |
|---|---|---|
| **A** | `Favier 2021 — Bitcoin et la religion (podcast Parlons Bitcoin)` | **Correction minimale** : ne change que le support, garde le titre court, et calque la structure de la fiche sœur « … (blog La voie du Bitcoin) ». |
| **B** | `Favier 2021 — Le Bitcoin, la religion du XXIe siècle (podcast Parlons Bitcoin)` | Colle au titre bibliographique, mais **rallonge** et s'écarte du style abrégé des autres fiches. |
| **C** | `Favier 2021 — Bitcoin et la religion` | Supprime le support au lieu de le corriger. **Ne ment plus**, mais **perd** une information que les fiches sœurs portent. |

Mon avis, clairement séparé : **A**, parce qu'elle répare exactement ce qui est faux sans rien décider d'autre. Mais un libellé désigne une œuvre et son support — c'est ta décision, pas la mienne.

---

## 7. Ce que ce chantier ne fait pas

Il n'applique rien, ne crée aucune v115, ne touche aucune relation ni aucun `authored` — y compris ceux posés en v114 sur cette fiche même. Il ne touche pas au doublon DeNardis (`e0b40d91` / `2272e5b8`), ni aux `SourceQuote`, ni aux autres auteurs retypés, ni au runtime. Il ne fusionne rien et ne crée aucun nœud.

**Il ne corrige pas non plus la thèse.** Le chapitre II cite « Favier 1981 » et « Favier 2018 » sans qu'aucune entrée correspondante figure à la bibliographie — et « Favier 1981 » désigne selon toute vraisemblance **Jean** Favier, le médiéviste, pas Jacques Favier. **Le graphe est indemne** : aucune fiche Favier 1981 ni Favier 2018 n'existe, et `53525938` ne porte que ses trois `authored` légitimes. Le risque d'homonymie a donc été cherché et **écarté par mesure**. `assets/MD/` est archivistique : l'écart est signalé, jamais corrigé.

## 8. Arbitrages posés à Maël

1. **Corriger le nom de `7f0f9cc4`** ? **oui / non**
2. **Quelle forme exacte** — A, B, C, ou une autre ?
3. **Créer une v115 strictement bornée à cette correction** ? **oui / non** — et si oui, **la régénération des 20 lignes de cartes appartient-elle au même lot** ?
4. **Garder le doublon DeNardis, les `SourceQuote`, les `authored`, les fusions et les créations hors périmètre** ? **oui / non**

**Aucune application avant réponse.**

## 9. Limites connues

- **La preuve est bibliographique, pas éditoriale.** Le script vérifie que `:472` nomme un podcast `parlonsbitcoin.com`. Il ne vérifie pas que l'URL répond encore, ni que « Parlons Bitcoin » est le libellé que l'éditeur se donne aujourd'hui — les accès réseau sortants ne le permettent pas ici, et une vérification de mémoire ne s'inscrit pas.
- **La forme A imite la fiche sœur**, qui écrit « (blog La voie du Bitcoin) ». Si cette convention devait changer, les deux fiches devraient changer ensemble — ce chantier n'en instruit qu'une.
- **Le CSV est une preuve figée sur v114** : le script refuse tout autre graphe plutôt que d'y écrire des mesures d'une version qu'il ne décrit pas.
