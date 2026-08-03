# Migration des sections — chapitre I

**Date** : 2026-08-03
**Graphe audité** : `grc20-these-mael-rolland-v98.json`
**Branche** : `agent/grc20-safety-net-v1`
**Mode agent** : C (patch déposé, non appliqué)
**Patch** : `patch_13_section_migration.json` — 22 opérations, 12 sections

---

## Le défaut corrigé

Les `ThesisSection` du graphe numérotent comme sous-sections de niveau 2 des
titres qui sont, dans le markdown, de niveau 3. Un cran de décalage, répété.
Conséquence : cinq clés du chapitre I désignent autre chose que ce qu'annonce
leur numéro, et deux sections réelles n'ont aucun nœud.

## Deux sources indépendantes, un même arbre

La numérotation canonique n'est pas une reconstruction de ma part. Elle est
attestée deux fois :

1. **Le corps de la thèse la dit.** Chapitre I, l. 99 : « (sect. I.1.1) …
   (sect. I.1.2) … (sect. I.1.3) », qui désigne les trois `##` placés sous
   `# I.1`. Le niveau canonique est donc `##`.
2. **Le sommaire de `graphe.html` la porte déjà**, avec les numéros de page
   (l. 1271-1282). Ses douze entrées correspondent exactement aux `##` du
   markdown — y compris `I.1.3 Le fonctionnement de Bitcoin…` et
   `I.2.1 Un développement infrastructural…`, que le graphe ignore.

Le site avait donc raison depuis le début. C'est le graphe qui s'en écarte.
**`graphe.html` n'a pas à être modifié** — après migration, ses clés et
celles du graphe coïncident enfin.

## Ce que le patch fait

| clé actuelle | clé cible | titre retenu (celui de la thèse) |
|---|---|---|
| `I.1.1` | `I.1.1.a` | Une monnaie frappée au coin de philosophies politiques et d'expériences pratiques |
| `I.1.2` | `I.1.1.b` | Une création hétérodoxe, entre recherche académique et recherche appliquée |
| `I.1.3` | `I.1.2` | Bitcoin : une chimère théorico-pratique très politique |
| `I.2.1` | `I.2.2` | Un protocole débordé de « carnavalesques » improvisations d'acteurs |
| `I.2.2` | `I.2.2.b` | Un protocole Bitcoin qui s'adapte : des régulations transactionnelles très politiques |

Sept autres sections (`I.1`, `I.2`, `I.3`, `I.3.1`, `I.3.2`, `I.3.3`, `I.4`)
conservent leur clé ; seul leur libellé est réaligné sur celui de la thèse,
conformément à l'arbitrage rendu — les reformulations du graphe sont
abandonnées. `labelEn` est réaligné sur `01_chapitre_I_EN.md` là où il
existe ; il n'est pas créé là où il manque.

**Le patch ne crée, ne fusionne ni ne supprime aucune entité, et ne touche
aucune relation.** Les 20 057 relations `appears_in_section` suivent leurs
nœuds : elles pointent des identifiants, que la migration ne change pas.

### Deux placements qui méritent d'être relus

- **`I.2.2` → `I.2.2.b`.** Le libellé du graphe (« qui s'adapte :
  régulations… ») et celui de la thèse (« qui s'adapte : **des**
  régulations… ») divergent d'un mot inséré au 34ᵉ caractère : aucun
  appariement automatique ne les rapproche. La cible est donc désignée à la
  main — `###` l. 321, second de son parent `##` l. 297, lui-même `I.2.2`.
- **`I.3.3`.** Le nœud portait « Ethereum : différences architecturales et
  normativité politique des designs » ; la thèse écrit « Ethereum, des
  recompositions d'alliances contre les rigidités de Bitcoin ». Clé
  conservée, libellé réaligné.

## Le patch est atomique

Deux clés cibles — `I.1.2` et `I.2.2` — sont occupées avant application, par
des nœuds que le patch déplace lui-même. Appliqué en bloc : aucune collision
(vérifié sur l'état final, en comptant aussi les nœuds non traités).
Appliqué par morceaux : deux écrasements silencieux. **Il n'y a pas de
sous-ensemble sûr.**

## Ce que le patch ne fait pas — et qui doit suivre

### 1. Trois sections canoniques restent sans nœud

| clé | markdown | titre | page (sommaire) |
|---|---|---|---|
| `I.1.1` | `##` l. 105 | Du terreau matériel et idéel aux racines de Bitcoin | 58 |
| `I.1.3` | `##` l. 177 | Le fonctionnement de Bitcoin suivant le script original de Nakamoto | 78 |
| `I.2.1` | `##` l. 259 | Un développement infrastructurel au-delà du protocole Bitcoin | 89 |

Ce sont exactement trois entrées du sommaire de `graphe.html`. Aujourd'hui
elles surlignent un nœud — le mauvais. Après le patch seul, elles n'en
surligneraient aucun. **La migration doit donc être appliquée en même temps
que la création de ces trois nœuds**, sans quoi on troque une erreur
silencieuse contre un trou visible.

### 2. Les cartes satellites doivent être remappées dans le même mouvement

`section_key` est la clé de jointure de trois fichiers que le lecteur charge :

| clé | → | `section_entities_map.json` | `entity_section_map.json` |
|---|---|---|---|
| `I.1.1` | `I.1.1.a` | 1 entrée | 1 398 épinglages |
| `I.1.2` | `I.1.1.b` | 1 entrée | 55 épinglages |
| `I.1.3` | `I.1.2` | 1 entrée | 123 épinglages |
| `I.2.1` | `I.2.2` | 1 entrée | 469 épinglages |
| `I.2.2` | `I.2.2.b` | 1 entrée | 195 épinglages |

Soit **2 240 épinglages** à réécrire. Le remappage doit être **simultané**,
pas séquentiel : appliquer `I.2.1 → I.2.2` puis `I.2.2 → I.2.2.b` déplacerait
deux fois le même lot.

`section_overrides.json` n'est pas concerné (sa seule clé de chapitre I est
`I.1`, inchangée).

### 3. Un nœud vide reste en l'état

`I.2.1b Un protocole Bitcoin qui s'adapte : des régulations transactionnelles
très politiques` — aucune clé, aucune entité rattachée — vise le même titre
(l. 321) que le nœud `I.2.2`, qui en porte 177. Lui attribuer une clé ne
serait pas migrer mais affecter, et créerait le doublon que la migration
lève. Il relève de la passe de dédoublonnage, pas de celle-ci.

## Effets de bord vérifiés

- **`graphe.story-helpers.js`** — l'alias `'Conception politique'` désignait
  le nœud `I.3.3` **par son nom**, que le patch change. Il est désormais
  désigné par identifiant : valable avant comme après application. C'était
  la seule des 39 entrées de la table touchée par le chapitre I ; le
  chapitre II en touchera deux (`II.1.1`, citée deux fois).
- **`narrative-anchors.json`** — six noms renommés y figurent, dans le champ
  `sectionKey`. Ce champ est **écrit par `narrative-anchors-build.mjs` et lu
  par personne** : ni `lecteur.html` ni `graphe.html` ne le consultent. Le
  fichier est par ailleurs déjà périmé (`generated_from: v96`). Aucune action
  requise ici ; sa régénération est un chantier distinct.
- **`graphe.html`** — aucune modification. Voir plus haut.
- **`check_anchoring.py`** — 64 problèmes distincts, identiques à la
  baseline. Aucune régression.

## Reproduire

```bash
python3 scripts/derive_section_tree.py --csv docs/audits/data/section-tree.csv
python3 scripts/plan_section_migration.py --csv docs/audits/data/section-migration.csv
python3 scripts/make_section_migration_patch.py --chapitre chap1
python3 scripts/check_anchoring.py
```

Le générateur **refuse d'écrire un patch utile en cas de collision** sur
l'état final : il sort en code 1 et nomme les clés en conflit.

## Reste à traiter

Chapitres II et III, introduction, conclusion — 58 sections écartées ici par
`--chapitre chap1`. Trois placements de niveau 3 y restent à désigner à la
main (`II.1.1`, `II.1.2`, `II.2.3`, `III.3.4` — voir `GROUPE_C` dans le
générateur, valeurs à `None`).
