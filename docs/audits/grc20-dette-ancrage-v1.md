# Dette d'ancrage — diagnostic et premier lot de corrections

**Date** : 2026-08-03
**Graphe** : `grc20-these-mael-rolland-v100.json`
**Branche** : `agent/grc20-section-migration-ch2-v1`
**Mode agent** : audit (A) puis correctif (C), corrections prouvées seulement

---

## Ce que la « dette de 67 » recouvre réellement

Le chiffre agrégeait cinq choses de natures très différentes. Diagnostiquées,
elles se répartissent ainsi :

| n | catégorie | nature réelle |
|---:|---|---|
| 26 | entité de `section_entities_map` absente du graphe | **17 résolus**, 9 en arbitrage |
| 25 | `ThesisSection` sans entrée dans `section_entities_map` | **écart de granularité**, pas un défaut |
| 13 | entité épinglée hors de la liste de sa section | 9 listes incomplètes, 3 épinglages faux, 1 cas structurel |
| 2 | `story-presets` : `relation_type` inexistant | **jetons morts** — corrigés |
| 1 | clé de `section_entities_map` sans `ThesisSection` | `III.3`, section absente du graphe |

### Les 25 « sections sans entrée » n'en sont pas 25

- **3** sont celles que `patch_14` vient de créer (`I.1.1`, `I.1.3`, `I.2.1`),
  volontairement sans contenu rattaché — déjà documenté.
- **22** sont des sous-sections de l'**introduction** (`intro_A_1` …
  `intro_C_2f`), et elles sont inconnues des **deux** cartes, pas d'une seule.
  6 d'entre elles portent du contenu dans le graphe (38, 12, 3, 2, 2, 1
  relations `appears in section`), 16 sont vides.

Les cartes s'arrêtent au niveau `intro_A` / `intro_B` / `intro_C` ; le graphe
descend plus bas. Le sommaire du site ne descend pas non plus à ce niveau :
**rien n'est cassé côté lecteur**.

Résultat qui tranche : **les deux cartes sont parfaitement cohérentes là où
elles se recouvrent** — 48 sections, `entity_section_map ⊆
section_entities_map` partout, zéro incohérence. La couche d'ancrage n'est
pas abîmée, elle est incomplète.

### Les épinglages « hors liste » ne cassent pas l'affichage

`lecteur.html` (l. 1451-1461) construit `finalIds = [...overrideIds,
...byScore]` : une entité épinglée est injectée de force, et affichée à la
taille maximale, **même absente de la liste de sa section**. Le contrôle C
signale donc une incohérence documentaire, pas une régression visible.

C'est ce qui explique qu'un épinglage faux ait pu passer inaperçu longtemps :
il s'affiche quand même, et en gros.

Ces 13 sont **antérieurs à la PR #103** : `git diff 9ac2995 HEAD --
section_overrides.json` ne rend aucune ligne, et le fichier ne contient
aucune clé touchée par la renumérotation du chapitre I.

---

## Ce qui est corrigé dans ce lot

### Deux épinglages faux, retirés

| entité | épinglée sur | preuve |
|---|---|---|
| Gouvernance de huis clos | `III.1` | **0 occurrence** de « huis clos » dans III.1 (l. 37-252) ; 7 dans III.2, dont son titre même, 7 dans III.3 |
| Robin Hood Group (DAO 2016) | `III.3.1` | aucune mention dans III.3.1 ; toutes les occurrences (« Robin Hood », « RHG », « chapeau blanc ») sont ≥ l. 607, donc en III.3.2 — où l'entité est déjà épinglée |

**Retirés, pas déplacés.** Retirer supprime un fait faux ; déplacer créerait
un choix éditorial nouveau — `III.2` n'a aucun épinglage aujourd'hui, et
décider d'en créer un relève de l'auteur.

### Deux jetons morts retirés de `allowedRelationTypes`

`relatedTo` et `source`, derniers survivants des 15 noms fantômes repérés en
avril. Ils restaient parce qu'aucun équivalent n'était évident. Mesuré :

- `graphe.html` compare après `canonicalizeRelationName` (minuscules puis
  suppression de tout non-alphanumérique). **Aucun des 130 `relation_types`
  de v100 ne canonicalise en `source` ni en `relatedto`** — 0 collision.
- `allowedRelationTypes` étant une liste **blanche**, retirer un jeton mort
  ne peut masquer aucune arête : la suppression est neutre par construction.
- Le seul candidat pour `source` serait `source of` (368 usages). Il est
  **directionnel** : 340 de ses 368 usages vont d'une `Reference` vers autre
  chose. Or les 75 nœuds focus des 5 récits ne comptent **aucune**
  `Reference`. Le remplacement afficherait **0 arête** sur les 20 étapes
  concernées. C'est ce qui bloquait l'arbitrage depuis avril ; c'est tranché.
- `relatedTo` n'a aucun équivalent, et le dépôt le proscrit lui-même :
  `scripts/audit_graph.py` (l. 33, 555) classe `relatedTo` parmi les
  « relations génériques » qu'il traque comme anti-pattern.

---

### Les 26 identifiants morts : 17 résolus, 9 en arbitrage

**L'origine est datée et unique.** `section_entities_map.json` a été généré
une fois, à partir d'un graphe ≤ v81, et **jamais régénéré**. Deux refontes
ont depuis fait disparaître les entités qu'il cite : v81→v82 (les doublons de
`ThesisSection`) et surtout **v90→v91**, la « refonte ontologique complète ».
**Aucun de ces 26 identifiants ne disparaît entre v96 et v100** : la migration
des sections n'y est pour rien.

Deux traitements, selon ce que devient l'ancrage — `scripts/fix_dead_ids_in_section_map.py` :

| traitement | n | critère |
|---|---:|---|
| **supprimer la ligne** | 8 | le jumeau vivant est **déjà présent dans chacune des mêmes sections**, compteurs identiques. Réécrire l'id créerait un doublon dans la même liste |
| **réécrire l'id** | 9 | le vivant est absent des sections concernées : supprimer perdrait l'ancrage |

Vérifié après application : **132 lignes supprimées, 75 identifiants
réécrits, 4 collisions fusionnées** (compteur maximum conservé), et surtout
**zéro entité vivante perdue**, 54 clés inchangées.

Les 9 réécritures sont des variantes orthographiques ou des formes longues
abandonnées par v91 : Eric → **Erik** Voorhees, Gregory → **Greg** Maxwell,
J.R. Willet → **Willett**, Shaoling → **Shaolin** Fry, Jeff → **Jeffrey**
Wilcke, plus Mastercoin / Omni Layer, OP_RETURN, Theymos, Empreinte
numérique.

#### Les 9 restants relèvent d'une décision de modélisation

- **6 domaines Ethereum.** v90 modélisait 16 `InfrastructureDomain` : des
  génériques et leurs jumeaux « … Ethereum ». v91 n'en garde que 8, en
  rendant les génériques agnostiques. Réécrire « Du protocole Ethereum » vers
  « Protocole et couche de base » revient à **effacer la partition
  Bitcoin/Ethereum** que v90 posait explicitement. Deux options défendables :
  réécrire en fusionnant les compteurs, ou supprimer les entrées puisque
  l'ontologie v100 ne porte plus de domaine par protocole. Le fait que ces
  lignes soient générées en bloc — rangs consécutifs, `occurrence_count` = 2
  uniforme — plaide pour la suppression, mais c'est ton choix.
- **2 sans successeur** : « De l'activité de traitement des transactions »
  (générique et Ethereum), seuls des domaines de v90 à n'avoir aucun
  survivant. Le `Concept` homonyme n'en est **pas** le successeur : les deux
  coexistaient déjà depuis v81.
- **1 ambigu** : « Omni Layer (meta-protocole Bitcoin) ». v90 comptait deux
  `Protocol` et deux `ActorNonHuman` sur ce thème, v91 n'en garde qu'un de
  chaque : impossible de dire lequel des morts va vers lequel des vivants.

## Deux angles morts découverts en réparant

**44 doublons préexistants** dans `section_entities_map.json` — un même
`entity_id` listé deux fois dans une même section, sur 35 sections. Mon
script les compte et **les laisse intacts** : les fusionner au passage
aurait effacé un défaut distinct sous couvert d'en réparer un autre. Le
contrôle ne les voit pas.

**19 opérations orphelines** dans le bloc `ops` de `grc20-these-mael-rolland-v100.json` :
des `SET_ATTRIBUTE` (`definition`) visant des entités inexistantes, héritées
de `patch_2c_definitions.json` et transportées de v96 à v100. `check_anchoring`
n'inspecte pas ce bloc, `audit_graph` non plus. Aucune relation pendante en
revanche : le dégât est confiné.

## Ce que le contrôle élargi a découvert

`check_anchoring` ne vérifiait que `allowedRelationTypes`. Il vérifie
désormais aussi `backboneRelationTypes`, `hideRelationTypes` et
`showRelationTypes` — **avec la normalisation qui leur est propre**, ce qui
est tout le sujet :

| liste | fonction de comparaison | effet |
|---|---|---|
| `allowedRelationTypes` | `canonicalizeRelationName` | minuscules **et** suppression des espaces → `partOf` = `part of` |
| ossature / masquage | `normalizeRelationName` | minuscules **sans** suppression → `partOf` ≠ `part of` |

Résultat : **7 jetons morts de plus**, invisibles jusqu'ici — `partOf`,
`citedIn`, `source`, `relatedTo` en ossature ; `partOf`, `citedIn`, `source`
en masquage.

Et le défaut **codé en dur** dans `graphe.html` l. 5502 est
`['partof', 'source', 'citedin', 'relatedto']`, passé par la même
normalisation : lui aussi entièrement mort.

**Conséquence : `hideBackbone: true` ne masque rien, et n'a jamais rien
masqué.** Deux récits le déclarent.

Ce n'est **pas corrigé ici**, délibérément : rétablir le masquage change ce
qui s'affiche à l'écran, dans un sens que personne n'a jamais vu. Le
remappage serait mécanique (`partOf` → `part of`, `citedIn` → `cited in`,
suppression de `source` et `relatedTo`), mais l'effet est éditorial.
**À arbitrer.**

---

## Ce qui reste, et pourquoi

### Non corrigé faute de donnée fiable — 9 listes incomplètes

Les 9 entités épinglées à juste titre mais absentes de la liste de leur
section demanderaient d'ajouter une entrée
`{entity_id, entity_name, occurrence_count}` à `section_entities_map.json`.
**`occurrence_count` ne se devine pas** : l'inventer fabriquerait de la
donnée. Et aucun script du dépôt ne génère cette carte — elle est produite
ailleurs.

Trois d'entre elles ne pourront de toute façon jamais être retrouvées par le
générateur, qui apparie des noms sur le texte français :
- **Responsible Disclosure** — le texte écrit « divulgation responsable » ;
- **Robin Hood Group** — ajoutée à la main après coup ;
- **Gouvernance polycentrique** — effet de frontière de page.

Il faut soit une table d'alias dans le générateur, soit une saisie manuelle.

### À arbitrer

1. **`hideBackbone`** (ci-dessus) — rétablir le masquage, ou retirer les
   jetons morts et assumer l'affichage actuel ?
2. **« Ethereum » épinglé dans `intro_A`** — les données sont unanimement
   négatives (0 mention dans le texte de A, aucune relation, aucune entrée de
   carte), mais afficher le duo Bitcoin/Ethereum en ouverture peut être un
   choix assumé.
3. **« Au-delà des codes »** (le nœud racine de la thèse) épinglé dans
   `intro_A` — il n'appartient à aucune liste de section et n'y appartiendra
   jamais. La correction n'est pas dans une carte mais dans le contrôle C,
   qui devrait exempter ce cas.
4. **« Proposition de Hard Fork — The DAO »** sur `III.3.2` — défendable,
   mais la section où la proposition est réellement débattue est III.3.3.
5. **Les récits `s6` et `s7`** (« la vraie charnière de la thèse »)
   n'affichent **aucune arête**. Le seul levier qui change quelque chose est
   d'ajouter `contributes to` (+15 arêtes sur 20 étapes, dont s6 : 0→3,
   s7 : 0→4). C'est un **élargissement éditorial**, pas un renommage :
   `contributes to` est directionnel et argumentatif, il ne « traduit » pas
   `relatedTo`. À ne pas faire passer pour une correction mécanique.

---

## Baseline

**67 → 70 → 53.**

| étape | effet |
|---|---|
| 2 jetons morts retirés, 2 épinglages faux retirés | −4 |
| contrôle F élargi aux listes d'ossature et de masquage | +7 |
| 17 identifiants morts résolus | −17 |

Un filet qui s'élargit fait monter le compteur avant de le faire baisser :
c'est le comportement attendu, pas une régression.

État restant : 25 sections sans entrée (dont 22 relèvent d'un écart de
granularité, pas d'un défaut), 11 épinglages hors liste (9 listes
incomplètes, 2 arbitrages), 9 identifiants morts en arbitrage, 7 jetons
d'ossature et de masquage, 1 section absente du graphe (`III.3`, qui se
réglera au chapitre III).

## Une mise en garde issue du diagnostic

`entity_section_map.json` est **bruité** et ne peut pas servir de preuve à
charge. Exemple mesuré : son entrée `intro_A` pour « Ethereum Classic (ETHC) »
porte un extrait qui ne contient ni « Ethereum » ni « Classic ». L'absence
d'une entité dans une liste ne prouve donc pas sa non-pertinence — d'où le
poids donné ici au markdown de la thèse plutôt qu'aux cartes.
