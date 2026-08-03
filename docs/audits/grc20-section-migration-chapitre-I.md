# Migration des sections — chapitre I

**Date** : 2026-08-03
**Graphe source** : `grc20-these-mael-rolland-v99.json` → **`v100`**
**Branche** : `agent/grc20-section-migration-v1`
**Mode agent** : C (patchs déposés **et appliqués**, graphe candidat produit)
**Patchs** : `patch_13` — 22 opérations, 12 sections · `patch_14` — 3 entités,
12 relations, 6 rebranchements

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

## Pourquoi le lot est indivisible

Le patch de renumérotation **seul** dégraderait le site. Trois pièces
doivent voyager ensemble, et une quatrième s'impose par voie de conséquence.

### 1. Trois sections canoniques n'avaient aucun nœud — `patch_14`

| clé | markdown | titre | page (sommaire) |
|---|---|---|---|
| `I.1.1` | `##` l. 105 | Du terreau matériel et idéel aux racines de Bitcoin | 58 |
| `I.1.3` | `##` l. 177 | Le fonctionnement de Bitcoin suivant le script original de Nakamoto | 78 |
| `I.2.1` | `##` l. 259 | Un développement infrastructurel au-delà du protocole Bitcoin | 89 |

Ce sont exactement trois entrées du sommaire de `graphe.html`. Avant, elles
surlignaient un nœud — le mauvais. Après la renumérotation seule, elles n'en
surligneraient aucun : on troquerait une erreur silencieuse contre un trou
visible. `patch_14` les crée.

Ce que ces nœuds portent : titre FR et EN depuis les markdown, page depuis le
sommaire, place dans l'arborescence. **Ni `summary` ni `central_argument`** —
les rédiger serait écrire à la place de l'auteur. Ils n'ont **aucune relation
de contenu**, et c'est un constat d'audit à part entière : le chapitre I
compte trois sections dont le texte n'est pas représenté dans le graphe.

#### Un défaut que la création rend visible

Les sous-sections de second rang — `I.1.1.a`, `I.1.1.b`, `I.2.2.b` — portaient
`section of` vers `I.1` / `I.2`, leur **grand-parent**, faute de parente
existante. Créer les parentes en aurait fait les sœurs du nœud dont elles sont
filles. `patch_14` les rebranche : 6 relations redirigées, seule chose qu'il
modifie d'existant, et conséquence directe de la création.

L'arborescence du chapitre I est désormais close :

```
I.1 ── I.1.1 ── I.1.1.a        I.2 ── I.2.1          I.3 ── I.3.1
       │        I.1.1.b               I.2.2 ── I.2.2.b      I.3.2
       ├─ I.1.2                                             I.3.3
       └─ I.1.3                                       I.4
```

### 2. Les cartes satellites remappées dans le même mouvement

`section_key` est la clé de jointure de trois fichiers que le lecteur charge :

| clé | → | `section_entities_map.json` | `entity_section_map.json` |
|---|---|---|---|
| `I.1.1` | `I.1.1.a` | 1 entrée | 1 398 épinglages |
| `I.1.2` | `I.1.1.b` | 1 entrée | 55 épinglages |
| `I.1.3` | `I.1.2` | 1 entrée | 123 épinglages |
| `I.2.1` | `I.2.2` | 1 entrée | 469 épinglages |
| `I.2.2` | `I.2.2.b` | 1 entrée | 195 épinglages |

Soit **2 245 remappages**, appliqués par `scripts/remap_section_keys.py`. Le
remappage est **simultané**, jamais séquentiel : appliquer `I.2.1 → I.2.2`
puis `I.2.2 → I.2.2.b` déplacerait deux fois le même lot. Le script détecte
ces deux chaînes de lui-même et les signale.

La table de correspondance n'est pas saisie à la main : elle est **dérivée de
`patch_13`**, seule source de vérité.

`section_overrides.json` n'est pas concerné (sa seule clé de chapitre I est
`I.1`, inchangée). Vérification d'après : les épinglages ont suivi leurs
sections — 1 398 sur `I.1.1.a`, 55 sur `I.1.1.b`, 123 sur `I.1.2`, 469 sur
`I.2.2`, 195 sur `I.2.2.b` — et le remappage n'a introduit **aucun** nouveau
problème d'ancrage.

### 3. Le site devait basculer sur le graphe migré — le « dernier mètre »

C'est la contrainte qui rend le lot indivisible. Les cartes sont **partagées**
entre le graphe servi et les clés de section. Le site servait **v96** partout
(`graphe.html`, `lecteur.html`, `graph-worker.mjs`, `narrative-anchors-build.mjs`,
`grc20-publish.mjs`), alors que v99 existait — et les clés de section de v96 et
v99 sont identiques, donc l'ensemble était cohérent.

Remapper les cartes sans basculer le site aurait cassé le lecteur
immédiatement : il aurait cherché dans v96 des sections renumérotées. Il n'y a
pas d'état intermédiaire cohérent — seulement `v96 + anciennes clés`, ou
`v100 + nouvelles clés`. Cette PR livre le second.

Effet de bord bienvenu : le site cessait de servir **le pire des trois
graphes**. v96 porte 15 endpoints cassés, corrigés dès v97.

**Laissé en v96, délibérément** : `export/scripts/export-workshop-to-public.mjs`
(valeur par défaut de `--canonical`). C'est un pipeline de publication publique
avec ses propres règles de visibilité ; changer sa source sans les examiner
serait imprudent.

### 4. Un nœud vide reste en l'état

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
- **`check_anchoring.py`** — 67 problèmes, baseline portée de 64 à **67**.
  Les 3 ajoutés sont les 3 sections créées sans contenu rattaché : pas des
  régressions, un constat consigné dans la donnée. Les 64 autres sont
  inchangés — le remappage de 2 245 clés n'en a introduit aucun.
- **CI, intégrité structurelle** — v100 : 0 endpoint cassé, 0 doublon,
  0 orphelin. Le câblage d'arborescence était nécessaire : sans lui, les
  3 nouveaux nœuds étaient orphelins et la CI refusait le graphe, à juste
  titre.

## Reproduire

```bash
python3 scripts/derive_section_tree.py --csv docs/audits/data/section-tree.csv
python3 scripts/plan_section_migration.py --csv docs/audits/data/section-migration.csv
python3 scripts/make_section_migration_patch.py --chapitre chap1
python3 scripts/make_section_creation_patch.py  --chapitre chap1
python3 scripts/make_v100_section_migration.py --dry-run
python3 scripts/make_v100_section_migration.py
python3 scripts/remap_section_keys.py --dry-run
python3 scripts/check_anchoring.py
```

Trois garde-fous, chacun ayant servi au moins une fois pendant ce chantier :

- le générateur **refuse d'écrire** en cas de collision sur l'état final, et
  nomme les clés en conflit ;
- l'applicateur **vérifie l'état de départ** de chaque relation rebranchée —
  rebrancher une relation déjà déplacée serait écraser en aveugle — et refuse
  de laisser une entité sans arête ;
- `check_anchoring.py` **a signalé de lui-même** les 3 sections vides.

## Reste à traiter

Chapitres II et III, introduction, conclusion — 58 sections écartées ici par
`--chapitre chap1`. Quatre placements de niveau 3 y restent à désigner à la
main (`II.1.1`, `II.1.2`, `II.2.3`, `III.3.4` — voir `GROUPE_C` dans le
générateur, valeurs à `None`).

Signalé, non traité — **dette antérieure, pas conséquence de ce lot** :
`I.2.2`, `I.3.1`, `I.3.2` et `I.3.3` n'ont pas de relation `section of` vers
leur section parente, seulement vers le chapitre. Huit relations la
combleraient. Ce lot ne rebranche que ce que la création des parentes rend
incohérent ; corriger au-delà élargirait une PR déjà dense.
