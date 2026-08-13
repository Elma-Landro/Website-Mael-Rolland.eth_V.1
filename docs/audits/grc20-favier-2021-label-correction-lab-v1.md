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

> **Formulation à ne pas confondre — le § 8 bis l'a mesurée.** Ces cartes **ne sont pas désynchronisées malgré un pipeline de synchronisation** : elles portent **un champ dénormalisé sans aucun mécanisme de synchronisation**. La nuance décide de tout, parce que la première formulation suggère une réparation par régénération, et la seconde dit qu'il n'y a rien à relancer.

**La correction des 20 lignes doit appartenir au même lot que la correction canonique, ou être explicitement exclue.** C'est l'arbitrage 3. *Par quel mécanisme*, en revanche, ne se décide pas ici : le § 8 bis établit qu'aucune régénération ne le fait.

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

## 8. Arbitrages — posés, puis **rendus le 2026-08-11**

Les quatre questions ont reçu réponse, et l'auteur a ajouté une cinquième rubrique : les contraintes d'application. Le tout est inscrit dans `_meta.arbitrage` du patch candidat, **jamais dans sa `policy`**.

| # | Question | Réponse |
|---|---|---|
| 1 | Corriger le nom de `7f0f9cc4` ? | **OUI** |
| 2 | Quelle forme ? | **A** — correction minimale |
| 3 | Créer une v115 bornée ? | **OUI**, + **les 20 lignes de cartes dans le même lot** |
| 4 | Garder DeNardis, `SourceQuote`, `authored`, fusions, créations hors périmètre ? | **OUI** |

**1 — la dette est reconnue et son périmètre confirmé.** La fiche désigne bien la bonne œuvre ; c'est le support qui est faux. On corrige le nom, **pas** l'identité de la fiche, **pas** les relations, **pas** les `authored`.

**2 — forme A, avec les motifs de rejet des deux autres.** `Favier 2021 — Bitcoin et la religion (podcast Parlons Bitcoin)`. B est écartée comme trop large — elle importerait tout le titre bibliographique. C est écartée comme trop pauvre : *le support est précisément ce qui est faux et ce que la correction doit réparer*. **Ne pas ajouter `title` ni `year`** dans ce lot ; c'est une dette séparée.

**3 — les 20 lignes de cartes appartiennent au même lot.** C'est la réponse au § 5 de cet audit, et le motif est explicite : elles sont une **conséquence mécanique** du renommage, et ne pas les corriger laisserait le dépôt porter une chaîne fausse versionnée *alors même que la fiche canonique est corrigée*. La v115 reste une **PR séparée**.

> **Le mot « régénérer », employé ici et à l'arbitrage 5, supposait un mécanisme qui n'existe pas.** Le § 8 bis l'a mesuré : la correction se fera par **substitution ciblée**, arbitrée le 2026-08-11 après le test à blanc.

**4 — périmètre exclu, en creux** : doublon DeNardis (`e0b40d91` / `2272e5b8`), `SourceQuote`, `authored`, fusions, créations, `title`/`year` manquants, Favier 1981, Favier 2018, et toute correction bibliographique plus large.

### Ce que la PR v115 devra prouver — séparément

L'auteur exige **trois preuves distinctes**, et le mot compte : le changement **canonique** sur la fiche, les changements **dénormalisés** dans les cartes, et **l'absence de tout autre effet**. Les mélanger dans un seul diff global masquerait précisément ce que ce chantier a mis au jour — que les deux couches peuvent diverger sans que rien ne le signale.

Douze contraintes encadrent l'application : créer uniquement `grc20-these-mael-rolland-v115.json` ; ne corriger que `7f0f9cc4` ; aucune relation modifiée ; aucun attribut autre que le champ de nom, **et seulement si c'est bien lui qui porte la chaîne fautive** ; aucun nœud créé ; aucune fusion ; aucune `SourceQuote` ; aucun `authored` ; corriger **seulement** les 20 lignes portant l'ancien nom — le texte d'origine disait « régénérer », mot que le § 8 bis a rendu impropre ; prouver que `b84f59ac` reste intact ; prouver que l'inversion avec `:474` est impossible ; prouver que le slug `bitcoin-et-religion` rattache bien `7f0f9cc4` à l'entrée `:472`.

**Rien n'est appliqué ici.** Le présent chantier reste une instruction et un patch candidat.

## 8 bis. Régénération à blanc des cartes — **la voie 2 est inapplicable**

Arbitrage du 2026-08-11 : voie 2 (régénération complète + preuve de confinement), **mais régénération à blanc d'abord**, avec pour consigne de s'arrêter si le diff révélait autre chose que les 20 lignes attendues.

**Il révèle autre chose — et par le bas, pas par le haut.**

| Mesure | Résultat |
|---|---|
| `build_anchor_weights.py --apply` sur l'état courant | **0 champ posé ou mis à jour** |
| Diff de `section_entities_map.json` | **0 ligne** |
| Diff de `entity_section_map.json` | **0 ligne** |
| Occurrences de l'ancien libellé **après** régénération | **19 + 1 = 20, inchangées** |

La régénération par le chemin normal est un **no-op sur le champ concerné**. Vérifié en copiant les deux cartes, en lançant le générateur, en comparant, puis en restaurant — cartes rendues à l'identique, `--check` vert.

### Pourquoi

`build_anchor_weights.py` **n'écrit jamais `entity_name`**. Son `--apply` ne pose que deux champs — `snippet_status` et `direct_anchor_count` — plus la suppression de deux clés héritées (lignes 218 et 303-312). Le nom, il ne fait que le **lire**, et en préférant celui du graphe : `noms.get(eid) or ent.get('entity_name', '')`.

Balayage complet des scripts : **le seul qui écrive `entity_name` dans une carte est `fix_dead_ids_in_section_map.py:155`**, et uniquement comme effet de bord de la réparation d'un identifiant mort — `e = dict(e, entity_id=cible, entity_name=vivants[cible])`. Il ne réécrit le nom que des entités dont il répare l'id. Un renommage ne déclenche rien.

`entity_section_map.json`, lui, **n'a aucun script écrivain** dans le dépôt : sept fichiers le lisent, aucun ne le produit.

### Ce que cela change

Il n'existe pas de « chemin normal de génération » capable de rafraîchir `entity_name`. **La voie 2 ne peut donc pas prouver ce qu'elle devait prouver** : sa preuve de confinement serait un diff vide, et les 20 lignes fausses resteraient.

Ce n'est pas une dérive dormante qui contaminerait le lot — c'est l'inverse : **la couche dénormalisée n'a pas de mécanisme de rafraîchissement du tout.** Le § 5 s'en trouve précisé : non seulement aucun contrôle ne détecterait un écart, mais **aucun outil ne saurait le réparer**.

Conformément à l'arbitrage : **arrêt, documentation, nouvel arbitrage.** Rien n'est écrit, aucune v115 n'est créée.

### Corrigé par la mesure exhaustive ultérieure — le mot « désynchronisation » était faux

Ce paragraphe a d'abord décrit les 20 lignes comme une **désynchronisation** que rien ne détecte. La mesure exhaustive faite ensuite (`scripts/check_map_entity_names.py`, lecture seule sur les 13 545 entrées résolues des deux cartes) établit quelque chose de plus précis, et il faut le dire dans cet ordre :

| | `entity_name` |
|---|---:|
| **Avant v115** | **0 divergence** sur 13 545 entrées |
| **Après v115** | **0 divergence** |

- **Les 20 lignes ne constituaient pas une désynchronisation existante.** Elles portaient **fidèlement** le nom canonique du graphe — un nom qui était sémantiquement faux, mais que les cartes reflétaient exactement. La couche dénormalisée était en accord parfait avec la couche canonique ; c'est la couche canonique qui avait tort.
- **Un renommage du graphe seul aurait créé 20 divergences** — pas révélé 20 divergences préexistantes. Et **aucun mécanisme existant ne les aurait réparées**, puisqu'il n'y en a aucun.
- **Après v115, on retombe à 0** : les deux couches sont de nouveau d'accord, et cette fois sur la valeur juste.

La formulation exacte, celle à retenir : **ces cartes ne sont pas désynchronisées malgré un pipeline de synchronisation ; elles portent un champ dénormalisé sans mécanisme de synchronisation.**

### Découverte distincte, hors périmètre : `type`, 44 divergences réelles

La même mesure exhaustive a fait apparaître un **second champ dénormalisé** dans `entity_section_map.json` : `type`, présent sur les 1 171 entrées. **44 d'entre elles divergent réellement du graphe** — par exemple `5d620327` porte `ActorNonHuman` dans la carte contre `CodeRepository` dans le graphe, `a444085b` porte `Concept` contre `CoreConcept`.

Contrairement aux 20 lignes de `name`, **celles-ci sont de vraies divergences actuelles**, sans rapport avec Favier. **Aucune n'est corrigée** : hors périmètre, et matière du chantier séparé sur l'architecture de cet artefact. Elles montrent que la question dépasse le seul champ `name`.

### Nouvel arbitrage posé à Maël

La voie 2 étant hors d'atteinte, trois options restent — et la troisième n'est pas une esquive :

| | Option | Ce qu'elle implique |
|---|---|---|
| **1** | **Substitution ciblée** (voie 1, écartée précédemment) | L'applicateur v115 remplace la chaîne aux 20 emplacements. La preuve est directe — le diff *est* les 20 lignes. Coût : un second chemin d'écriture pour ces fichiers, ce que la voie 2 voulait éviter. Le motif de ce refus tombe en partie, puisqu'il n'y a pas de premier chemin pour ce champ. |
| **2** | **Écrire le rafraîchisseur manquant** | Un `--refresh-names` dans `build_anchor_weights.py`, qui réaligne `entity_name` sur le graphe pour **toutes** les lignes. Répare la cause, pas le symptôme — mais devient un chantier à part entière, et sortirait v115 de son périmètre : il toucherait potentiellement d'autres lignes que ces 20. |
| **3** | **Corriger le graphe seul en v115**, cartes renvoyées à un chantier dédié | v115 reste strictement bornée à `7f0f9cc4`. Les 20 lignes restent fausses le temps du chantier suivant — mais elles le sont déjà, et l'outillage ne s'en sert pas. |

Mon avis, clairement séparé : **option 1 pour v115**, puis **option 2 comme chantier distinct**. La substitution ciblée est bornée, prouvable ligne à ligne, et n'invente pas de mécanisme ; le rafraîchisseur, lui, mérite d'être écrit — mais pour la cause générale, pas au détour d'une correction de libellé.

**Aucune écriture avant réponse.**

---

## 9. Limites connues

- **La preuve est bibliographique, pas éditoriale.** Le script vérifie que `:472` nomme un podcast `parlonsbitcoin.com`. Il ne vérifie pas que l'URL répond encore, ni que « Parlons Bitcoin » est le libellé que l'éditeur se donne aujourd'hui — les accès réseau sortants ne le permettent pas ici, et une vérification de mémoire ne s'inscrit pas.
- **La forme A imite la fiche sœur**, qui écrit « (blog La voie du Bitcoin) ». Si cette convention devait changer, les deux fiches devraient changer ensemble — ce chantier n'en instruit qu'une.
- **Le CSV est une preuve figée sur v114** : le script refuse tout autre graphe plutôt que d'y écrire des mesures d'une version qu'il ne décrit pas.
