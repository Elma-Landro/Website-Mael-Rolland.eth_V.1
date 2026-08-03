# La couche d'ancrage : `occurrence_count` n'est pas reproductible, et ne mesure pas ce qu'il annonce

**Date** : 2026-08-03
**Graphe** : `grc20-these-mael-rolland-v106.json`
**Branche** : `claude/file-upload-branch-check-jw4cng`
**Mode agent** : A — audit. **Aucun fichier de données n'est modifié.**
**Chantier** : dette d'ancrage, étape 1 de la séquence de
`docs/agents/grc20-agent-skills-architecture-v1.md` § 5

---

## Verdict

**Le chantier est arrêté à l'étape 1, comme prévu.** L'étape 1 était posée
comme un verrou : *« si `occurrence_count` n'est pas reproductible, on
s'arrête, on ne l'approxime pas. »* Il ne l'est pas.

Et l'audit a trouvé plus que ce qu'on lui demandait. La question était : *peut-on
calculer `occurrence_count` pour 8 nouvelles sections ?* La réponse est non. Mais
en cherchant la règle, on a établi ce que le champ mesure réellement pour les
54 sections **déjà** peuplées — et ce n'est pas ce que son nom annonce.

---

## 1. Ce qui est établi

Trois constats, tous vérifiés deux fois : une première par l'instance
d'archéologie, une seconde indépendamment, en relisant les fichiers. Conformément
à la règle 3 de la charte, les chiffres ci-dessous sont ceux du second passage.

### 1.1 `section_entities_map.json` est un index inversé

`occurrence_count` **n'est pas un comptage de texte**. C'est le nombre
d'enregistrements de l'entité dans `entity_section_map.json`, qui est
l'artefact primaire :

```
11 452 lignes exactes · 4 divergentes · 918 sans contrepartie   (sur 12 374)
```

Les 918 sans contrepartie viennent d'une reconstruction partielle ultérieure.
Les 4 divergentes sont les doublons fusionnés au maximum en août 2026.

### 1.2 Deux entités sur trois portent le poids d'un mot qui n'est pas le leur

`entity_section_map.json` conserve un `snippet` par occurrence : les 50
caractères de part et d'autre du terme apparié. En regroupant les entités par
**signature d'occurrences** — l'ensemble exact de leurs couples (section,
snippet) :

```
63 groupes · 571 entités sur 1 171 partagent leur signature avec au moins une autre
```

Le plus gros groupe compte **230 entités portant les 39 mêmes occurrences**,
celles du mot « Bitcoin » :

| Type | Entité | ses 39 occurrences sont celles de… |
|---|---|---|
| `Protocol` | Bitcoin | *(le terme lui-même)* |
| `Institution` | Bitcoin Foundation | « Bitcoin » |
| `Protocol` | Bitcoin Cash | « Bitcoin » |
| `Concept` | Preuve de concept / Phase 1 Bitcoin | « Bitcoin » |
| `Concept` | Phase de péché / Phase 2 Bitcoin | « Bitcoin » |
| `Concept` | Phase de maturation / Phase 3 Bitcoin | « Bitcoin » |

Trois autres groupes du même ordre : 40 entités sur « BTC/Bitcoin », 39 puis 27
sur « Ethereum ». **`Bitcoin Foundation` ne pèse pas parce que la thèse parle de
la Bitcoin Foundation, mais parce qu'elle parle de Bitcoin.**

C'est ce qui rend l'extension impossible : on ne peut pas reconstituer une
table d'alias qu'on n'a pas, et la reconstituer approximativement produirait des
poids **non comparables** d'une section à l'autre.

### 1.3 Le noyau qui obéit à une règle est le petit tiers

Pour les seules entités appariées sur leur propre nom, la règle est simple et
tient à 82,3 % (897 couples exacts sur 1 090) :

> nombre d'occurrences de la **sous-chaîne littérale du `name`**, **insensible
> à la casse**, sur **tout le texte de la section, titres et notes inclus**,
> **sans plafond**.

Le balayage de 64 variantes établit que **la casse est le seul paramètre
décisif** : normaliser accents, apostrophes ou espaces ne change rien du tout
(0 couple gagné, 0 perdu) ; retirer les notes ou les titres dégrade jusqu'à
34 %. Les 193 écarts résiduels vont **tous** dans le même sens — le texte
compte plus que la carte — et sont de la troncature à valeur arbitraire, sans
facteur ni décalage constant.

Proportions, en lignes de `section_entities_map.json` :

| Classe | Entités | Lignes |
|---|---:|---:|
| appariée sur son propre nom | 366 (31 %) | 1 463 |
| **appariée sur un mot-clé tiers** | **770 (66 %)** | **10 411** |
| mixte | 35 | — |
| hors `entity_section_map` | — | 500 |

Sur `II.1.1.a` (409 entités listées), **16 seulement se retrouvent dans le texte
par leur nom**. Les 393 autres y figurent parce que « Bitcoin » ou « Ethereum »
y figure.

---

## 2. Jusqu'où cela remonte au lecteur

`lecteur.html` classe les entités d'une section par TF-IDF calculé **sur
`occurrence_count`**, et n'en affiche que les 12 premières. Le poids mandataire
n'est donc pas une curiosité d'archive : il décide de ce qui s'affiche.

Mesure sur sept sections, avec le calcul exact du lecteur :

| Section | nœuds à poids mandataire | 3 premiers du panneau |
|---|---:|---|
| `I.3.2` | **10 / 12** | Buterin 2017 · Buterin 2017a · Buterin 2017c |
| `conclu_resume` | **9 / 12** | Gouvernance polycentrique · Altcoins · Hard Fork |
| `I.1.1.a` | 6 / 12 | Pouliot 2018 · Lars 2021 · Narayanan & Clark 2017 |
| `II.2.2.c` | 5 / 12 | Blanc 1998 · Blanc 1998a · Blanc 1998b |
| `intro_A` | 4 / 12 | Desmedt et Lakomski-Laguerre · Dupré, Ponsot et Servet · Neutralité de la monnaie |
| `II.1.1.a` | 2 / 12 | Yermack 2013 · Wray 2010 · Cartelier 2001 |
| `III.3.1` | 1 / 12 | Dupont 2018 · Entretien n°11 · Popper 2016a |

**37 des 84 nœuds affichés — 44 % — portent un poids mandataire.** Et la
dispersion compte autant que la moyenne : `III.3.1` est presque sain, `I.3.2`
presque entièrement mandataire. **Les panneaux ne sont pas également fiables, et
rien ne dit lequel l'est.**

---

## 3. Une hypothèse testée puis abandonnée

J'ai supposé que les poids mandataires expliquaient les panneaux à 12 nœuds et
0 lien relevés en navigateur le 03/08. **C'est faux, et la mesure le dit :**

| nœuds mandataires dans le top-12 | sections | liens moyens | panneaux sans lien |
|---|---:|---:|---:|
| 0 à 3 | 29 | 3,5 | 9 / 29 |
| 8 et plus | 6 | 5,2 | 3 / 6 |

Aucune relation, et plutôt l'inverse de celle attendue. La rareté des arêtes
dans les panneaux garde donc la cause déjà avancée — la sélection top-12 par
TF-IDF retient des entités distinctives, peu reliées entre elles — et **n'est
pas un symptôme de ce défaut-ci**. Consigné parce qu'une hypothèse séduisante
et fausse, si elle n'est pas écrite comme telle, revient.

---

## 4. Ce qu'il ne faut pas faire

> **Appliquer la règle du § 1.3 aux 8 sections neuves en laissant les 54
> anciennes sous l'ancien régime.**

Ce serait le pire des trois choix possibles. Les poids ne seraient plus
comparables : une entité mandataire pèserait 3 dans `intro_A` et 0 dans la
section neuve, sans que rien ne l'indique. On aurait remplacé **une dette
visible** — huit panneaux vides, comptés et documentés — par **une dette
invisible** : des chiffres d'apparence homogène dont la moitié ne mesure pas la
même chose que l'autre.

C'est exactement ce que l'étape 1 était là pour empêcher.

---

## 5. Deux voies honnêtes — à arbitrer

Aucune n'est prise ici. Les deux sont des décisions de l'auteur.

### Voie A — recalculer tout le fichier avec la règle du § 1.3

- **Ce qu'on gagne** : une règle simple, déterministe, rejouable, vérifiable, et
  applicable aux 8 sections comme aux 54 autres. Les poids redeviennent
  comparables.
- **Ce qu'on paie** : les listes rétrécissent massivement — de l'ordre de 12 374
  lignes à 1 500–2 500. Les panneaux du lecteur perdent la plupart de leurs
  nœuds. Ce n'est pas une perte d'information mais une perte d'**apparence**
  d'information ; elle sera néanmoins très visible.
- **Ce qu'il faut décider** : accepter que la couche d'ancrage devienne
  beaucoup plus maigre et beaucoup plus sûre.

### Voie B — cesser de traiter `occurrence_count` comme une mesure

- **Ce qu'on gagne** : rien n'est détruit, les panneaux gardent leur densité.
- **Ce qu'on paie** : il faut un autre signal pour classer — le nombre de
  relations `cited in` / `appears in section` est le candidat évident — et
  documenter `occurrence_count` pour ce qu'il est devenu : un poids d'affichage
  hérité, non reproductible.
- **Ce qu'il faut décider** : par quoi on classe, et si les 8 sections restent
  vides en attendant.

**Ma recommandation, à titre consultatif : la voie B d'abord**, parce qu'elle ne
détruit rien et se teste ; la voie A ensuite si l'auteur veut une couche
d'ancrage démontrable. La voie A appliquée tout de suite ferait perdre au
lecteur une densité qu'il faudrait des mois à reconstruire par des relations
attestées.

---

## 6. Ce qu'il y avait à rattacher dans les 8 sections

Établi en parallèle, et qui reste vrai quelle que soit la voie retenue :
**aucune des huit n'est un cas de « thèse mince ».**

| Section | mots de corps | notes | entités détectées | verdict |
|---|---:|---:|---:|---|
| `II.2.3` | **6 924** | 1 843 | 30 | **la plus longue section de toute la thèse**, et elle est vide |
| `II.3.3` | 6 531 | 836 | 57 | gouvernance duale/polycentrique, Scaling Debate — tous déjà nœuds |
| `III.2.3` | 5 625 | 619 | 40 | cœur du cas CVE 2018 ; difficile à justifier vide |
| `III.2.2` | 5 485 | 569 | 11 | très descriptive ; appellerait de nouveaux nœuds |
| `I.2.1` | 5 000 | 2 438 | 71 | ses trois `###` sont les trois phases de développement |
| `II.1.2` | 2 877 | 1 272 | 10 | le graphe n'a presque pas de vocabulaire juridique |
| `I.1.3` | 2 534 | 531 | 19 | exposé technique du protocole |
| `II.2.1` | 2 066 | 727 | 14 | la plus courte des huit ; courte, pas vide |

Cinq des huit sont **au-dessus de la médiane** des sections (4 079 mots).

**Et le contenu ne vit pas dans leurs sous-parties.** La règle existe ailleurs
dans le dépôt — `I.1.1` porte 4 relations quand `I.1.1.a` en porte 381 — mais
les **22 titres `###`** de ces huit sections **n'existent comme nœuds nulle
part, sous aucune graphie**. Il n'y a aucun endroit où ce contenu pourrait se
trouver : le vide est bien un défaut d'outillage.

---

## 7. Constats collatéraux

1. **17 sections figurent comme *entités rattachées* à d'autres sections**, sur
   196 lignes de la carte — `I.3` 24 fois, `I.1` 22 fois, `III.3` 21 fois. Une
   section « apparaît dans » une section : conséquence directe du mécanisme
   mandataire, le titre contenant le mot apparié.
2. **Le nœud sans clé `3ce505bc…`**, « I.2.1b Un protocole Bitcoin qui
   s'adapte », porte **31 relations sortantes** — dont **19 `appears in
   section`**, c'est-à-dire qu'une section s'y comporte comme une entité citée
   dans 19 sections. Il porte un `summary` et un `central_argument` que son
   jumeau `I.2.2.b` (201 relations) n'a pas, et **aucune `section_key`**. Le
   générateur de migration l'écarte délibérément. *(Une instance d'audit l'a
   d'abord rapporté à 0 relation ; vérification faite, il en a 31.)*
3. **`I.2.2` a un enfant `.b` mais pas de `.a`** — seule famille incomplète du
   graphe.
4. **Le champ `type` de `entity_section_map.json` diverge du graphe** : il donne
   `Concept` pour l'entité `III.3`, que le graphe type `ChapterSection`.
5. **Six clés `*_preamble`** de la carte n'ont ni nœud ni bloc markdown
   correspondant, et rien ne les documente.
6. **Le sous-niveau de l'introduction est atteint du même mal, en pire** : 14
   clés `intro_*` n'ont **qu'une seule relation entrante** chacune, tout le
   contenu étant agrégé sur `intro_A/B/C` (606 / 597 / 560). Sans effet visible
   — ces clés ne sont pas au sommaire — mais le périmètre du problème dépasse
   les huit sections.

---

## 8. Ce que cet audit ne conclut pas

- Il ne dit pas que la couche d'ancrage est sans valeur. Un tiers des entités
  portent un poids exact, et le découpage en sections est, lui, entièrement
  reconstituable.
- Il ne dit pas que les panneaux du lecteur sont faux. Il dit qu'**on ne sait
  pas lesquels sont justes**, et que la proportion varie de 1/12 à 10/12 sans
  que rien ne l'indique.
- Il ne touche à aucune donnée : ni `entity_section_map.json`, ni
  `section_entities_map.json`, ni le graphe, ni le runtime.

---

## 9. Une note sur la méthode

Une des deux instances a conclu que `III.3` était une clé sans nœud. Le nœud
existe : `41e14735…`, typé **`ChapterSection`**. Elle n'avait cherché que
`ThesisSection`.

C'est **littéralement le piège** que
`docs/agents/grc20-agent-skills-architecture-v1.md` § 3.6 documente comme
généalogie du Semantic-Event-Classifier, et qui avait failli faire recréer
`III.3` en double le 03/08. Le document a prédit l'erreur qu'une instance a
commise le lendemain de sa rédaction.

Deuxième illustration de la même règle : l'hypothèse du § 3 était la mienne,
elle était plausible, et la mesure l'a démentie. **Aucun des deux garde-fous
n'était un contrôle automatique** — c'était, dans les deux cas, une
contre-vérification. C'est l'argument de l'architecture, vérifié sur elle-même.
