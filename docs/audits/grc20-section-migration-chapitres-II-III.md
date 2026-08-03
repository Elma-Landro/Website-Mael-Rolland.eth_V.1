# Migration des sections — chapitres II et III

**Date** : 2026-08-03
**Graphe audité** : `grc20-these-mael-rolland-v105.json` → **`v106`**
**Branche** : `claude/file-upload-branch-check-jw4cng`
**Mode agent** : A
**Patchs** : `patch_15_section_migration_chap23.json`, `patch_16_section_creation_chap23.json`

Second et dernier palier de la migration entamée en v100 pour le chapitre I.
Même arbitrage, même mécanisme, mêmes scripts.

---

## Ce que la migration corrige

Avant v106, le sommaire de `graphe.html` annonçait 48 sections. Sur les 25
que portent les chapitres II et III :

- **13 entrées chargeaient la mauvaise section.** `II.1.1` du sommaire
  désignait un nœud dont le titre est en réalité un `###` du markdown — donc
  une sous-partie de `II.1.1`, pas `II.1.1`. Le lecteur voyait un graphe
  cohérent, mais pas celui de la section qu'il lisait. C'est l'erreur la plus
  coûteuse du lot, parce qu'elle est **silencieuse**.
- **11 entrées ne chargeaient rien** : la section canonique existait dans la
  thèse et dans le sommaire, mais aucun nœud ne la portait.

Après v106, **les 48 entrées du sommaire résolvent toutes vers un nœud du
graphe**, vérifié :

```
sommaire graphe.html : 48 entrées, 48 distinctes
  sans nœud dans v106      : 0
```

---

## Renumérotations appliquées (13)

Le décalage a partout la même cause : des titres de **niveau 3** du markdown
ont été numérotés comme des sous-sections de **niveau 2**. Chaque nœud
retrouve sa place réelle, en second rang subordonné (`II.1.1.a`).

| Clé avant | Clé après | Titre (thèse) |
|---|---|---|
| `II.1.1` | `II.1.1.a` | Les critiques instrumentales fondées sur des fonctions monétaires canoniques |
| `II.1.2` | `II.1.1.b` | Une monnaie « créature de l'État » : les critiques nominalistes et chartalistes |
| `II.2.1` | `II.2.2.a` | Au-delà de la monnaie, l'argent : questionner la monétisation |
| `II.2.2` | `II.2.2.b` | La monnaie comme système de paiement : monétisation et liquidité |
| `II.2.3` | `II.2.2.c` | La monnaie à l'épreuve : quand dettes, confiance et souveraineté se confrontent |
| `II.3.1` | `II.3.1.a` | Du concept de gouvernance et de sa polysémie |
| `II.3.2` | `II.3.1.b` | Retournement positif du concept : réintégrer le pouvoir et la politique |
| `II.3.3` | `II.3.2` | Quand les CM réactivent un débat monétaire ancien |
| `III.1.1` | `III.1.1.a` | Une mise en crise longue et silencieuse |
| `III.1.2` | `III.1.1.b` | Une remise en ordre rapide |
| `III.2.1` | `III.1.2.a` | De la diversité des crises aux crises protocolaires |
| `III.2.2` | `III.1.2.b` | Enjeux des crises Bitcoin : labélisations indigènes |
| `III.2.3` | `III.2.1` | Des acteurs au cœur de la gouvernance sur le protocole |

Deux d'entre elles **franchissent la frontière de partie** : `III.2.1` et
`III.2.2` du graphe relevaient en réalité de `III.1.2`, pas de `III.2`. Le
sommaire les rangeait donc sous la mauvaise partie du chapitre.

`III.3.4` était classé « à arbitrer » par le plan : à tort. Le `##` de la
ligne 721 — « Fork You ?! » : une scission surprise fondatrice et ses
enseignements — lui correspond exactement. Seul son **libellé** avait dérivé,
pas son rang. Clé conservée, libellé réaligné.

## Sections créées (11)

Elles existent dans la thèse et dans le sommaire, jamais dans le graphe :
`II.1.1`, `II.1.2`, `II.2.1`, `II.2.2`, `II.2.3`, `II.3.1`, `II.3.3`,
`III.1.1`, `III.1.2`, `III.2.2`, `III.2.3`.

Chacune porte ce qui se dérive du texte, **rien d'autre** : titre français et
anglais depuis les markdown, page depuis le sommaire, place dans
l'arborescence (`section of` / `has section`, motif réciproque déjà employé
par le graphe). Aucun résumé, aucun argument central : les écrire serait
écrire à la place de l'auteur.

Elles portent aussi, dans la donnée et non dans un seul rapport :

```
evidenceStatus = "thesis section — structure only, content not yet anchored"
```

**22 relations rebranchées** en corollaire direct : les sous-sections de
second rang pointaient `section of` vers leur *grand-parent*, faute de parente
existante. `II.1.1.a` visait `II.1` ; elle vise désormais `II.1.1`.

---

## Ce que cette migration coûte, et pourquoi c'est le bon prix

Les 11 sections créées n'ont **pas de liste d'entités** dans
`section_entities_map.json`. Dans le lecteur, leur panneau graphe est vide.

C'est un échange assumé, le même qu'en v100 : on troque **une erreur
silencieuse** — une entrée de sommaire qui affiche le graphe d'une autre
section, sans que rien ne le signale — contre **un trou visible**. Un trou se
voit, se compte, et se comble ; une erreur silencieuse ne se voit pas.

Pour qu'il se voie vraiment, `lecteur.html` affiche désormais, au lieu d'un
panneau muet :

> Contenu de cette section pas encore rattaché au graphe

Les 11 codes correspondants sont inscrits dans
`docs/audits/data/anchoring-baseline.json`, avec leur motif. Ils rejoignent
`I.1.1`, `I.1.3` et `I.2.1`, de même nature depuis v100.

---

## Deux défauts trouvés en chemin, hors périmètre initial

### 1. `III.3` est l'unique `ChapterSection` du graphe

73 sections portent le type `ThesisSection`. Une seule — `III.3`, « Une
gouvernance publique d'exception : le hard fork d'Ethereum » — porte
`ChapterSection`, type dont elle est la seule occurrence.

Conséquence : **`make_section_creation_patch.py` s'apprêtait à la recréer**,
à côté d'un nœud existant et déjà relié. C'est exactement l'incident du
domaine (ii) : un doublon vide posé à côté d'un nœud vivant.

Corrigé en rendant les outils aveugles au nom du type
(`grc20_commun.est_section`), pas en retypant le nœud — **retyper serait un
arbitrage, pas une correction**. Trois scripts en bénéficient :
`make_section_creation_patch.py`, `make_v100_section_migration.py`,
`check_anchoring.py`. Effet de bord : le code `B:sem:III.3` de la baseline
disparaît, réellement corrigé.

**À porter à l'arbitrage** : faut-il retyper `III.3` en `ThesisSection` ? Un
type à une seule occurrence est plus probablement un accident qu'une
distinction voulue — mais c'est à l'auteur de le dire.

### 2. Le libellé aurait reçu la clé technique en préfixe

`libelle()` construisait `« clé + titre »`. Correct pour `II.2.2.a` ; absurde
pour les clés opaques : la conclusion allait recevoir le nom
**`conclu_aceph De l'acéphalisme apolitique…`**, soit un jeton technique
affiché à un lecteur. Le préfixe n'est désormais posé que si la clé est une
numérotation de la thèse.

### 3. L'introduction n'avait pas besoin de cette migration

Le plan proposait de renuméroter 10 nœuds de l'introduction. À tort : ses clés
(`intro_B_1a`) sont **déjà** subordonnées, et leurs libellés affichent déjà
`B.1.a.`. Le préfixe `intro_` est un marqueur de namespace, pas une erreur de
rang. Les migrer aurait cassé un namespace cohérent pour rien.

Elle est donc **hors périmètre**, explicitement. Reste, pour elle seule, une
dérive de libellé (« cryptomonnaies » là où le texte écrit « CM »), purement
cosmétique, et quatre nœuds — `intro_C_2c` à `intro_C_2f` — qui aplatissent
les niveaux 3 et 4 du markdown en une seule séquence lettrée. Aucun des deux
n'affecte ce que le lecteur charge.

---

## Effets sur les artefacts d'ancrage

| Fichier | Effet |
|---|---|
| `entity_section_map.json` | 4 892 clés remappées |
| `section_entities_map.json` | 13 clés remappées |
| `section_overrides.json` | **0** — aucune clé épinglée ne bougeait |
| `narrative-anchors.json` | reconstruit sur v106 (8 `sectionKey` portaient des noms morts) |
| `graphe.story-helpers.js` | 2 alias de récit pointaient l'ancien nom de `II.1.1` |
| `story-presets.mjs` | 2 `focusNodes` pointaient l'ancien nom de `II.3` |

Le remappage est **simultané, jamais séquentiel** : `II.3.3 → II.3.2` et
`II.3.2 → II.3.1.b` se chevauchent, et les appliquer l'un après l'autre
déplacerait deux fois le même lot.

Les quatre références mortes de `graphe.story-helpers.js` et
`story-presets.mjs` n'ont été trouvées qu'en comparant **tous** les noms
changés entre v105 et v106 à **tous** les fichiers du runtime : le contrôle
d'ancrage n'en voyait que deux. Ces tables d'alias sont indexées par **nom
d'entité**, donc cassables par tout renommage — fragilité connue, non corrigée
ici (les indexer par identifiant est un chantier distinct).

---

## Vérifications

Les quatre étapes de la CI, rejouées en local :

```
Syntaxe JavaScript          26 fichiers  OK
Validité JSON               tous         OK
Intégrité structurelle      v106 : 0 endpoint cassé · 0 doublon · 0 orphelin
                                   · 0 op orpheline · version OK
Cohérence de l'ancrage      46 problèmes connus — aucune régression
```

Et le contrôle qui donne son sens à tout le chantier :

```
48 entrées de sommaire → 48 nœuds résolus dans v106 (0 manquant)
84 section_key uniques — aucun doublon
```

`space.version` est désormais **dérivée du nom du fichier écrit** par
l'applicateur, et non recopiée de la source : c'est ce qui avait laissé v100 à
v104 annoncer « v99 ».
