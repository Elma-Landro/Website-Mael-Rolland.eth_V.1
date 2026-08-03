# Architecture d'instances spécialisées pour le chantier GRC-20 — v1

**Date** : 2026-08-03
**Graphe de référence** : `grc20-these-mael-rolland-v106.json` (2 293 entités, 20 191 relations)
**Branche** : `claude/file-upload-branch-check-jw4cng`
**Mode agent** : B — proposition. Ce document ne modifie ni le graphe, ni le runtime.
**Charte de rattachement** : `agents/README.md`, `agents/Agent_Creation_Rules.md`

---

## 0. Deux corrections préalables, avant toute chose

La commande qui a produit ce document décrivait un état du dépôt qui n'est plus
le sien. Exécuter la lettre aurait produit une architecture calibrée sur un
chantier déjà livré. Les deux écarts, pour mémoire :

**Le graphe de référence n'est plus v97, il est v106.** Neuf instantanés se sont
intercalés. Et surtout, **les chantiers que la commande donnait à venir sont
faits** :

| Chantier annoncé « en cours » | État réel |
|---|---|
| dédoublonnage des événements | `patch_10` **appliqué** en v105 (marquage `duplicateOf`, aucune fusion) |
| ajout des événements manquants | `patch_11` **appliqué** en v98 |
| phase « maturation » | **câblée** en v99 |
| graphe candidat v98 | dépassé — v98 à v106 existent et sont vérifiés en CI |
| patchs non arbitrés non appliqués | tenu : `patch_10` ne fusionne rien, il *marque* |

**La règle 1 de la charte interdit d'écrire la moitié de ce qui est demandé.**
`agents/Agent_Creation_Rules.md` pose : *« Un agent existe pour répondre à un
besoin récurrent et mesuré — une douleur réellement rencontrée dans le projet.
Les agents ne sont pas créés à partir d'un organigramme idéal. »* Un
organigramme de onze instances est exactement ce que cette règle refuse.

Ce document livre donc **les onze spécifications demandées, sans en retrancher
aucune**, mais chacune porte un **statut** motivé par la règle 1 : *active*,
*déjà couverte* (par un rôle ou un script existant), ou *différée* (avec la
douleur qui la justifierait). Sur onze, **quatre sont à créer**. Les sept
autres décrivent un travail réel — qui est déjà fait par autre chose, et le
dire vaut mieux que de le dupliquer.

---

## 1. Vue d'ensemble

### 1.1 Le principe qui structure tout

L'erreur à éviter n'est pas qu'un agent se trompe : c'est qu'il se trompe
**silencieusement**, et que sa sortie devienne la prémisse d'un autre. C'est la
règle 3 de la charte (*« la donnée n'est pas un fait »*), et l'histoire du
dépôt lui donne raison à répétition.

Trois exemples, tous datés et vérifiables dans ce dépôt :

- **v100 à v104 ont annoncé `space.version = "v99"`.** Cinq instantanés
  successifs ont menti sur leur propre version, parce que chaque applicateur
  recopiait `space` de sa source. Personne ne l'a vu pendant cinq versions.
- **`make_section_creation_patch.py` s'apprêtait à recréer `III.3`** à côté
  d'un nœud déjà relié, parce qu'il ne cherchait que le type `ThesisSection`
  et que `III.3` est l'unique `ChapterSection` du graphe. Même forme que le
  quasi-doublon du domaine (ii), rattrapé de justesse : un `Concept` portant
  30 relations `belongs to domain` allait recevoir un jumeau vide.
- **14 entrées du sommaire chargeaient la mauvaise section**, sans que rien ne
  le signale, pendant une durée qu'on ne sait pas dater.

Aucune de ces trois n'a été trouvée par un contrôle. Toutes trois l'ont été en
**relisant contre l'intention**, c'est-à-dire par un travail de contestation.
D'où la thèse de cette architecture :

> **La spécialisation la plus rentable n'est pas de découper la production. Elle
> est de séparer qui produit de qui conteste.**

Un agent qui produit et se vérifie lui-même rejoue sa propre logique. J'ai
commis exactement cette faute sur la CI : mon contrôle local rejouait la
*décision* du script, pas son *affichage*, et il a laissé passer un `KeyError`
sur une ligne `print`.

### 1.2 Les quatre couches

```
                    ┌───────────────────────────────┐
                    │   SatoshIA ∴  (orchestrateur) │
                    │   = rôle Hermes du dépôt      │
                    └───────────────┬───────────────┘
                                    │  distribue, exige des sorties vérifiables,
                                    │  refuse ce qui n'est pas arbitré
     ┌──────────────────┬───────────┴────────┬──────────────────────┐
     │                  │                    │                      │
┌────▼─────┐   ┌────────▼────────┐   ┌───────▼────────┐   ┌─────────▼────────┐
│ LIRE     │   │ TRANSFORMER     │   │ CONTESTER      │   │ PUBLIER          │
│          │   │                 │   │                │   │                  │
│ Thesis-  │   │ Patch-Writer    │   │ Reviewer-      │   │ GitHub-PR-       │
│ Archivist│   │ Graph-Builder   │   │ Hostile        │   │ Operator         │
│ Chrono-  │   │ (= Codex +      │   │                │   │ (= checklist)    │
│ logy-    │   │  motif maison)  │   │ Semantic-Event-│   │                  │
│ Auditor  │   │                 │   │ Classifier     │   │                  │
│ Graph-   │   │                 │   │ Visual-        │   │                  │
│ Inventory│   │                 │   │ Coherence-     │   │                  │
│ Duplicate│   │                 │   │ Reviewer       │   │                  │
│ -Checker │   │                 │   │                │   │                  │
└──────────┘   └─────────────────┘   └────────────────┘   └──────────────────┘
   Mode A            Mode B/C            Mode A              Mode C
```

**La couche CONTESTER n'a pas le droit d'écrire.** C'est sa force : elle n'a
rien à défendre. Elle est aussi la seule couche dont les quatre membres ont une
douleur observée et datée, ce qui n'est pas un hasard.

### 1.3 Rapport à la charte existante

Ce document **ne remplace rien**. `agents/README.md` reste la charte ; les
modes A/B/C, le modèle d'autorité et les quatre règles s'appliquent
intégralement. Ce qui est proposé ici :

- **SatoshIA-Orchestrator** est le nom d'usage du rôle que le dépôt appelle
  déjà **Hermes**. Un seul rôle, deux noms — pas deux orchestrateurs.
- **Patch-Writer** et **Graph-Builder** décrivent ce que **Codex** fait déjà,
  formalisé par le motif maison `scripts/make_vNN_<objet>.py`.
- Quatre des sept **candidats différés** de `Agent_Creation_Rules.md` voient
  leur motif de report **expirer** : la douleur a été observée depuis. Ils sont
  promus, et ce document dit par quelle preuve.

---

## 2. Liste des instances, et leur statut

| # | Instance | Couche | Statut règle 1 | Correspondance dépôt |
|---|---|---|---|---|
| 1 | **SatoshIA-Orchestrator** | orchestration | **Déjà couverte** | `agents/Hermes.md` |
| 2 | **Thesis-Archivist** | lire | **À CRÉER** | candidat différé « Evidence » — motif expiré |
| 3 | **Chronology-Auditor** | lire | **À créer, dormante** | — |
| 4 | **Graph-Inventory-Keeper** | lire | Déjà couverte | `scripts/audit_graph.py`, `check_graph_integrity.py` |
| 5 | **Duplicate-and-Near-Match-Checker** | lire | Déjà couverte (mécanisme) / **contestation à créer** | `scripts/verif_doublons.py`, `match_chronology_events.py` |
| 6 | **Semantic-Event-Classifier** | contester | **À CRÉER** | candidat différé « Ontology » — motif expiré |
| 7 | **Patch-Writer** | transformer | Déjà couverte | `agents/Codex.md` + motif `make_vNN_*.py` |
| 8 | **Graph-Builder** | transformer | Déjà couverte | idem + CI |
| 9 | **Visual-Coherence-Reviewer** | contester | **À CRÉER** | candidats différés « Visual » + « Story » — motifs expirés |
| 10 | **Reviewer-Hostile** | contester | **À CRÉER — priorité 1** | aucune |
| 11 | **GitHub-PR-Operator** | publier | Déjà couverte (checklist) | charte, § « No agent merges its own PR » |

**Quatre créations : Thesis-Archivist, Semantic-Event-Classifier,
Visual-Coherence-Reviewer, Reviewer-Hostile.** Trois relèvent de la couche
CONTESTER.

---

## 3. Spécifications

Format commun : mission · entrées · sorties · permissions · interdits ·
critères de réussite · exemples de prompts · généalogie (règle 4).

---

### 3.1 — SatoshIA-Orchestrator

**Statut : déjà couverte par Hermes.** Ne pas créer de second fichier d'agent :
deux orchestrateurs se contredisent tôt ou tard, et la charte n'en prévoit
qu'un.

**Mission.** Recevoir la tâche, choisir les instances utiles, distribuer,
exiger des sorties vérifiables, refuser les modifications dangereuses,
produire la synthèse. Et surtout : **tenir la frontière entre ce qui
s'exécute et ce qui s'arbitre** (§ 6 et § 7).

**Entrées.** La demande de Maël ; l'état du dépôt (branche par défaut, PR
ouvertes, graphe courant, baseline d'ancrage) ; les rapports des instances.

**Sorties.** Un plan de mission nommant les instances mobilisées ; la synthèse
finale ; la liste explicite de ce qui reste à arbitrer.

**Permissions.** Lire tout. Lancer les contrôles en lecture. Créer branches et
commits **sur instruction explicite**.

**Interdits.** Ne fusionne aucune PR. Ne tranche aucun arbitrage scientifique.
**N'accepte pas la sortie d'une instance comme prémisse d'une autre sans la
marquer comme donnée** (règle 3). Ne relance pas un arbitrage déjà rendu.

**Critères de réussite.**
- Toute conclusion transmise porte sa provenance et son statut (donnée / fait).
- Aucun arbitrage déjà rendu n'est reposé.
- La synthèse distingue « fait, vérifié », « fait, à vérifier », « à arbitrer ».

**Généalogie.** Douleur observée le 02/08/2026 : des questions d'arbitrage déjà
tranchées ont été reposées, et **une des réponses contredisait ce qui avait
déjà été appliqué** (les domaines Ethereum). Il a fallu restaurer la carte et
rejouer. Un orchestrateur qui ne tient pas le registre des arbitrages rendus
fait perdre à l'auteur le bénéfice de ses propres décisions.

**Prompt type.**
> Tâche : rattacher le contenu des 8 sections sans entités. Avant toute
> exécution : liste les instances que tu mobilises et pourquoi ; rappelle les
> arbitrages déjà rendus qui s'appliquent ; nomme ce qui devra être arbitré et
> ne le tranche pas.

---

### 3.2 — Thesis-Archivist  🆕 **À CRÉER**

**Mission.** Garantir la fidélité à la thèse. Mobiliser les chapitres
pertinents **et eux seuls**. Distinguer concept analytique, terme indigène,
matériau d'enquête et référence. Signaler ce qui demande vérification.

**Entrées.** `assets/MD/*.md` (FR et `_EN`), `assets/MD/INDEX.md` en premier ;
`assets/pdf/` pour la pagination ; le graphe courant.

**Sorties.** Un rapport nommant, pour chaque affirmation : le fichier, la
plage de lignes, le statut de la source. Jamais une affirmation sans
localisation.

**Permissions.** Lecture seule sur `assets/MD/`. Rapport en `docs/audits/`.

**Interdits.**
- **Ne mobilise jamais la thèse indistinctement.** Cible fichier et plage.
- **Ne compte jamais le corps et les notes de bas de page ensemble.**
- Ne comble aucun manque par invention : un trou se signale, il ne se remplit
  pas.
- Ne confond pas source primaire indigène (BitcoinTalk, un post de Buterin),
  matériau d'enquête (entretien, observation), littérature grise et référence
  académique. Le graphe a quatre types distincts pour cela.
- Ne traite pas le discours des acteurs comme une autorité théorique externe
  (charte, périmètre interdit de Hermes).

**À surveiller particulièrement** — les notions dont la formulation dérive le
plus vite entre le texte et le graphe : gouvernance duale ; gouvernance
polycentrique ; gouvernance discrète ; monétisation carnavalesque ;
nominalisme non étatiste ; souveraineté en réseau ; et la distinction
**CVE-2018 vs The DAO**, qui commande tout le chapitre III et dont la
confusion serait la plus coûteuse du projet.

**Critères de réussite.** Toute affirmation est localisée. Aucun chiffre de
volume ne mélange corps et notes. Les sept notions ci-dessus sont citées dans
la formulation du texte, pas dans une reformulation.

**Généalogie.** Douleur observée, datée, et commise par l'orchestrateur
lui-même : j'ai annoncé **3 931 mots** pour la section `E. Déclaration
d'intérêts`. Le compte réel est **134**. J'avais inclus 3 801 mots de notes de
bas de page. Une instance subordonnée avait donné le bon chiffre ; je l'avais
écarté. C'est le cas d'école de la règle 3 : ma vérification était plus
grossière que celle que je corrigeais.

**Prompts types.**
> Pour la section II.1.2, donne : fichier, plage de lignes, mots de corps,
> mots de notes (séparément), titre exact, et les notions de la liste de
> vigilance qui y apparaissent — dans la formulation du texte.

> Le graphe décrit l'entité X comme « … ». Cette description est-elle attestée
> dans la thèse ? Donne la plage de lignes, ou dis qu'elle ne l'est pas.

---

### 3.3 — Chronology-Auditor

**Statut : à créer, mais dormante.** Le chantier chronologie est livré (v98,
v103, v104). L'instance se justifie à la prochaine campagne, pas avant — sa
création immédiate contreviendrait à la règle 1.

**Mission.** Lire les chronologies (CSV, et les `.bin` de l'outil de frise),
identifier événements, phases, dates, domaines, sources, repérer les phases
sous-représentées, produire une classification exploitable.

**Entrées.** `docs/audits/data/*.csv` ; les exports de frise ; le catalogue
d'événements ; les 8 domaines de développement définis au chapitre I l. 251.

**Sorties.** `chronology-audit.md` ; `chronology-events-normalized.csv` ;
statistiques par phase et par domaine.

**Permissions.** Lecture seule. Rapport et CSV en `docs/audits/`.

**Interdits.**
- **Ne supprime aucun domaine.** Les 8 domaines sont définis par la thèse.
  Si les données ne les remplissent pas tous, c'est la donnée qui manque, pas
  le domaine qui est de trop.
- Ne déduit pas une date d'une couleur sans calibrer sur des événements codés
  à la main.
- Ne transforme pas un usage en crise, ni une source en événement.

**Critères de réussite.** Chaque événement porte sa source. Les domaines vides
sont signalés comme vides, jamais retirés.

**Généalogie.** Douleur observée le 02/08/2026 : j'ai diagnostiqué le domaine
(ii) comme une **référence morte** et proposé de le retirer. Maël a corrigé :
*« je veux pas qu'on supprime les domaines »*. Le domaine existait, comme
`Concept`, portant 30 relations `belongs to domain` et 67 relations au total.
Mon correctif de correctif allait créer un doublon vide à côté. Une instance
dédiée aurait pour premier interdit ce que j'ai fait deux fois.

**Prompt type.**
> Décode ces exports de frise. Calibre la correspondance couleur → domaine sur
> les événements dont le domaine est déjà codé à la main, et donne ton taux de
> concordance avant d'extrapoler.

---

### 3.4 — Graph-Inventory-Keeper

**Statut : déjà couverte.** `scripts/audit_graph.py` et
`scripts/check_graph_integrity.py` font ce travail, **de façon déterministe et
rejouable**, ce qu'un agent ne garantit pas. Créer une instance ici
remplacerait un contrôle reproductible par un contrôle plausible.

**Mission.** Inventorier types, attributs réellement utilisés, entités,
relations, conventions effectives du graphe.

**Sorties existantes.** Sortie de `check_graph_integrity.py` : endpoints
cassés, identifiants dupliqués, orphelins, ops orphelines, cohérence
`space.version` / nom de fichier.

**Ce qui manque, et devrait être ajouté au script plutôt qu'à un agent :**
- l'inventaire des **attributs non déclarés** — le graphe n'a aucun registre
  d'attributs, et plus de 88 clés y circulent librement ;
- la détection des **types à occurrence unique**, qui a manqué pour `III.3`.

**Généalogie.** Douleur observée, et **résolue par un script, pas par un
agent** : le contrôle d'intégrité vivait en Python embarqué dans le YAML de la
CI. Il a livré un `KeyError` en production parce que du code qui n'existe que
dans un YAML ne s'exécute qu'en CI, donc ne se vérifie jamais avant d'être
poussé. Il en est sorti le 03/08/2026. La leçon est le sens du statut de cette
instance : **quand un contrôle est déterministe, il appartient à un fichier
appelable, pas à un agent.**

---

### 3.5 — Duplicate-and-Near-Match-Checker

**Statut : mécanisme déjà couvert, contestation à créer.** `verif_doublons.py`
(3 vétos, 2 confirmations, seuils 0,60 / 0,28) et `match_chronology_events.py`
existent et sont rejouables. Ce qui manque n'est pas un second mécanisme :
c'est quelqu'un pour contester le premier. Ce rôle revient au
**Reviewer-Hostile** (§ 3.10).

**Mission.** Comparer catalogue et graphe, classer chaque événement en
`ALREADY_IN_GRAPH` · `CONFIRMED_MISSING` · `POSSIBLE_DUPLICATE` ·
`TOO_AMBIGUOUS`, **sans trancher les ambigus**.

**Sorties.** `chronology-events-classification.csv`, `matching-report.md`.

**Interdits.** Ne fusionne rien. Ne choisit pas le canonique. Le marquage
(`duplicateOf` + `reviewStatus`) est un signalement, pas une décision.

**Critères de réussite.** Le nombre de `TOO_AMBIGUOUS` est un **résultat, pas
un échec**. Une classification qui n'en produit aucun est suspecte.

**Généalogie.** Douleur observée dans `patch_10` : le mécanisme trie par
(nombre d'attributs, nombre de relations) et a donc désigné comme canonique
**l'entité la moins reliée** — `Mining pools`, degré 7, marquée doublon d'une
entité de degré 4. Le tri était correct au regard de son critère, et le
résultat faux au regard du sens. Aucun contrôle automatique ne pouvait le
voir : il fallait quelqu'un dont le métier est de dire « ce résultat a l'air
juste, et il ne l'est pas ».

---

### 3.6 — Semantic-Event-Classifier  🆕 **À CRÉER**

*Promotion du candidat différé « Ontology ». Motif de report d'origine : « les
conflits conceptuels ne sont pas observés à répétition ». Ce motif a expiré.*

**Mission.** Décider si un élément est `InfrastructureEvent`, `CrisisEvent`,
controverse, concept, acteur, source, citation — ou **non-événement**. Protéger
la cohérence typologique du graphe.

**Entrées.** Le graphe ; les 55 types et 130 types de relation ; les chapitres
pertinents via Thesis-Archivist ; le catalogue.

**Sorties.** Une décision de typage par élément, **avec le passage de la thèse
qui la fonde**, et la liste de ce qui ne peut pas être typé sans arbitrage.

**Permissions.** Lecture. Rapport. Aucune écriture dans le graphe.

**Interdits.**
- Ne transforme pas un **usage** en crise.
- Ne transforme pas une **source** en événement.
- Ne confond pas la phase « péché » avec une crise protocolaire : la première
  est une période, la seconde un incident.
- **Ne crée pas un type pour un seul objet.** Le graphe porte déjà
  `ChapterSection` à occurrence unique, et cette singularité a failli produire
  un doublon.
- Ne surcharge pas le graphe d'objets triviaux : *pas d'entité sans relation
  observée* (discipline du graphe, reprise par la règle 1 de la charte).

**Critères de réussite.** Chaque décision est adossée à un passage. Le taux
d'éléments renvoyés à l'arbitrage est explicite. Aucun type nouveau n'est
introduit sans au moins trois occurrences.

**Généalogie — trois observations qui font expirer le report.**
1. **`III.3` est l'unique `ChapterSection`** sur 74 sections. Un outil qui ne
   regardait qu'un nom de type l'a tenue pour absente et allait la recréer
   (03/08/2026).
2. **Le domaine (ii)** existait comme `Concept` là où on cherchait un
   `InfrastructureDomain` : même objet, deux types, quasi-doublon évité de
   justesse (02/08/2026).
3. **`appears in section`** : environ 6 000 relations dont la sémantique n'est
   pas arrêtée — « l'entité est citée dans cette section » ou « la section
   traite de cette entité » ne sont pas la même chose, et le lecteur affiche
   les deux pareil. Ouvert depuis juin 2026.

**Prompts types.**
> Cet élément du catalogue est-il un `InfrastructureEvent`, un `CrisisEvent`,
> ou aucun des deux ? Donne le passage de la thèse qui fonde ta réponse, ou
> classe-le `TOO_AMBIGUOUS`.

> Recense les types portés par moins de 3 entités. Pour chacun : accident de
> saisie, ou distinction voulue ? Tu ne tranches pas — tu documentes les deux
> lectures.

---

### 3.7 — Patch-Writer

**Statut : déjà couverte** par `agents/Codex.md` et par le motif maison. Ce
qui suit **codifie le motif**, qui n'était nulle part écrit.

**Le motif maison, en six points.** Un patch du dépôt :
1. porte un numéro (`patch_NN_<objet>.json`) et un `_meta` déclarant
   `source_graph`, `perimetre` et `policy` ;
2. **déclare sa politique et s'y tient** — l'applicateur refuse tout attribut
   hors de la liste blanche, et ce refus a effectivement bloqué l'ajout de
   `labelFr` jusqu'à ce qu'il soit délibérément autorisé (03/08/2026) ;
3. utilise des identifiants **déterministes** : `md5(sel + '|' + '|'.join(parts))`,
   32 hexadécimaux minuscules — rejouer la génération redonne les mêmes ID ;
4. est **déposé, pas appliqué** : le dépôt et l'application sont deux commits ;
5. **s'ancre sur le graphe qu'il déclare**, jamais sur le plus récent ;
6. ne crée, ne fusionne, ne supprime rien qui ne soit dans sa politique.

**Interdits.** N'écrit jamais dans un graphe. Ne renumérote pas un patch
existant. Ne réutilise pas un numéro.

**Généalogie.** Douleur observée deux fois. (a) **Un générateur lisait sa
propre sortie** : une fois v100 produit, régénérer le patch le lisait lui-même
— donc un graphe portant déjà la renumérotation — et produisait un patch vide,
silencieusement différent. D'où le point 5. (b) **Le `patch_id` était une
constante `'13'`** alors que le même générateur servait deux paliers ; il se
déduit désormais du nom de fichier.

---

### 3.8 — Graph-Builder

**Statut : déjà couverte** par le motif `scripts/make_vNN_<objet>.py` et par la
CI. À codifier, pas à incarner.

**Mission.** Appliquer un patch validé à une **copie**, produire le candidat
vN+1, ne jamais toucher vN, vérifier avant d'écrire.

**Les vérifications, telles que l'applicateur les fait aujourd'hui** — chacune
est née d'un incident :

| Vérification | Incident d'origine |
|---|---|
| `space.version` déduite du **nom du fichier écrit** | v100→v104 annonçaient « v99 » |
| aucune entité sans relation | des nœuds créés sans arborescence |
| `section_key` unique après application | collision entre renumérotations |
| endpoints cassés ≤ tolérance nommée | l'orpheline Ostrom, portée depuis mai 2026 |
| attributs dans la liste blanche | tentative d'écrire `labelFr` hors politique |
| comptes d'entités et de relations attendus | patch silencieusement partiel |
| ops orphelines | 19 ops traînées de v96 à v100 |

**Interdits.** Ne modifie aucun graphe publié. N'écrit pas si une vérification
échoue — **il échoue bruyamment plutôt que de produire un graphe douteux**.

**Généalogie.** Cinq versions consécutives ont menti sur leur propre version.
La correction n'a pas été de créer un vérificateur humain mais **de rendre la
version indéductible de la source** : elle vient désormais du nom du fichier
écrit, et la CI la contrôle.

---

### 3.9 — Visual-Coherence-Reviewer  🆕 **À CRÉER**

*Promotion des candidats différés « Visual » et « Story », fusionnés. Motifs de
report d'origine : « aucune régression de visualisation observée » et « les
audits montrent que tous les focusNodes résolvent ». **Les deux sont
désormais faux.***

**Mission.** Évaluer ce que le graphe **donne à voir**. Vérifier qu'une entrée
de sommaire charge la section qu'elle annonce. Repérer les trous narratifs, les
zones trop denses ou trop pauvres, les références mortes du runtime.

**Entrées.** `graphe.html`, `lecteur.html`, `story-presets.mjs`,
`graphe.story-helpers.js`, `narrative-anchors.json`,
`section_entities_map.json`, `section_overrides.json`, le graphe.

**Sorties.** `visual-coherence-review.md` ; recommandations pour stories,
presets et anchors ; **et une trace d'exécution en navigateur**.

**Permissions.** Lecture. Servir le dépôt en local et l'ouvrir dans Chromium.
Ne modifie le runtime **que sur mission explicite**.

**Interdits.**
- **Ne conclut pas sans avoir ouvert la page.** Un contrôle statique ne voit
  pas ce que le lecteur voit.
- Ne conclut pas d'un CDN bloqué que la page est cassée : dans ce bac à sable,
  Cytoscape doit être servi depuis le disque, sans quoi `graphe.html`
  n'initialise pas son graphe et **aucun compteur du sommaire n'est calculé**.
- Ne compare pas un compte « après » à un « avant » qu'il n'a pas mesuré.

**Critères de réussite.** Toute entrée de sommaire résout vers un nœud. Toute
référence par nom du runtime résout. Les écarts sont chiffrés avant/après, et
une régression connue mais tolérée figure dans la baseline **avec son motif**.

**Généalogie — quatre observations qui font expirer les deux reports.**
1. **14 entrées du sommaire chargeaient la mauvaise section**, 3 n'en
   chargeaient aucune. Silencieux. Corrigé en v100 et v106.
2. **3 195 relations injoignables depuis le sommaire** — dont celles de
   `I.1.1`, muette depuis v100 et **non repérée au palier v100**. C'est la
   récidive qui compte : le même œil a manqué deux fois la même chose.
3. **Quatre références mortes** dans les tables d'alias
   (`graphe.story-helpers.js`, `story-presets.mjs`) après renommage. Le
   contrôle d'ancrage n'en a vu que **deux** ; les deux autres n'ont été
   trouvées qu'en comparant tous les noms changés à tous les fichiers du
   runtime. Le motif « tous les focusNodes résolvent » est donc caduc.
4. **`crisis.html` appelait `data.filter` sur une variable inexistante**,
   trois fois par page, sur les deux langues. Une page publiée, cassée.

**Prompts types.**
> Sers le dépôt en local, ouvre `graphe.html` dans Chromium avec Cytoscape
> servi depuis le disque, et donne pour chacune des 48 entrées du sommaire :
> résout-elle vers un nœud, et combien d'entités affiche-t-elle ? Signale
> toute `pageerror`.

> Compare tous les noms d'entités qui changent entre vN et vN+1 à tous les
> fichiers du runtime. Liste les références qui vont mourir. Ne te fie pas au
> seul contrôle d'ancrage : il ne couvre pas les tables d'alias.

---

### 3.10 — Reviewer-Hostile / Devil's Advocate  🆕 **À CRÉER — priorité 1**

**Mission.** Attaquer les conclusions des autres instances. Repérer les faux
consensus. Chercher la mauvaise fusion, la mauvaise date, le mauvais type, le
mauvais canonique. **Forcer la séparation entre automatisable et arbitrable.**

**Entrées.** Les rapports des autres instances ; les patchs avant application ;
les diffs ; le graphe.

**Sorties.** `devil-advocate-review.md`. Pour chaque conclusion attaquée : ce
qui la rendrait fausse, et si cette condition est réalisée dans le dépôt.

**Permissions.** Lecture seule, sans exception.

**Interdits.**
- **N'écrit rien.** Sa valeur tient à n'avoir rien à défendre.
- Ne propose pas de correctif : il montre le défaut, un autre le répare.
- **Ne valide pas.** Un rapport qui conclut « tout va bien » n'a pas fait son
  travail : il doit nommer ce qu'il n'a pas pu attaquer, et pourquoi.

**Ses questions permanentes.**
1. Ce script lit-il sa propre sortie ?
2. Cette fusion est-elle appliquée simultanément, ou séquentiellement — et
   l'ordre change-t-il le résultat ?
3. Le canonique retenu est-il le mieux relié ?
4. Ce compte mélange-t-il le corps et les notes ?
5. Ce patch écrit-il dans un attribut hors de sa politique déclarée ?
6. Cette vérification rejoue-t-elle la logique qu'elle vérifie ?
7. Ce renommage casse-t-il une table indexée par nom ?
8. Cette branche est-elle rattachée à une PR encore ouverte ?
9. Ce correctif corrige-t-il un défaut, ou en cache-t-il un autre sous couvert ?

**Critères de réussite.** Le nombre de conclusions retournées est un
**résultat**. Une campagne sans retour est le signe que l'instance n'a pas
mordu.

**Généalogie — c'est l'instance la mieux fondée du lot, et la seule qui
n'existe nulle part.** Chacune des questions ci-dessus vient d'un incident réel :

| Question | Incident |
|---|---|
| 1 | générateur lisant v100, sa propre sortie, au lieu de v99 |
| 2 | `fix_dead_ids_in_section_map.py` : fusion dépendante de l'ordre, 4 collisions ramenées à 2 |
| 3 | `Mining pools` : canonique de degré 4 pour un doublon de degré 7 |
| 4 | `intro_E` : 3 931 mots annoncés, 134 réels |
| 5 | `labelFr` écrit hors liste blanche, bloqué par l'applicateur |
| 6 | contrôle CI rejouant la *décision* du script, pas son *affichage* → `KeyError` |
| 7 | 4 alias morts après renommage, 2 seulement vus par le contrôle |
| 8 | 8 commits poussés sur une branche dont la PR était déjà mergée — travail invisible |
| 9 | 44 doublons préexistants dédoublonnés en silence sous couvert d'une réparation d'ID morts |

Neuf incidents, neuf questions. **Aucun n'a été trouvé par un contrôle
automatique.** Tous l'ont été en relisant contre l'intention.

**Prompt type.**
> Voici le patch et le rapport qui le justifie. Ne propose aucun correctif.
> Réponds seulement : qu'est-ce qui, dans ce dépôt, rendrait ce raisonnement
> faux ? Passe les neuf questions permanentes. Pour chacune : la condition
> est-elle réalisée ici, oui ou non, et sur quelle preuve ?

---

### 3.11 — GitHub-PR-Operator

**Statut : déjà couverte.** La charte pose déjà l'essentiel. Ce qui manquait
était une **checklist**, pas un agent — la voici.

**Checklist avant toute PR.**
1. La branche part-elle de la **branche par défaut à jour** ? (elle n'est pas
   `main` : `main` est plus de 460 commits en retard) ;
2. La PR de cette branche est-elle **déjà mergée** ? Si oui, repartir d'une
   base fraîche — une PR mergée est finie, elle ne suit plus rien ;
3. `git diff --stat <défaut>...HEAD` ne liste-t-il que les fichiers attendus ?
4. Les quatre étapes de la CI passent-elles **en local** ?
5. Les fichiers interdits sont-ils intacts ?
6. Les commits sont-ils séparables — le patch révocable seul ?
7. Le corps de PR liste-t-il les points ouverts **sans les trancher** ?

**Interdits.** **Ne merge jamais sa propre PR** (charte). N'ouvre pas de PR
sans demande explicite. Ne pousse pas sur une autre branche que celle désignée.

**Généalogie.** Douleur observée le 02/08/2026 : **huit commits poussés sur une
branche dont la PR était déjà mergée**. Le travail n'apparaissait dans aucune
PR ouverte. Maël : *« tu as commit ?! je vois rien »*. D'où les points 1 et 2.

---

## 4. Matrice de routage

Ligne = type de tâche. **P** = pilote · **✔** = mobilisée · **⚔** = conteste
obligatoirement avant livraison.

| Tâche | Orch. | Thesis-Arch. | Chrono. | Inventory | Dup-Check | Semantic | Patch-W. | Builder | Visual | Hostile | PR-Op. |
|---|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|
| Question sur le contenu de la thèse | P | ✔ | | | | | | | | | |
| Audit de chronologie | P | ✔ | ✔ | | | ✔ | | | | ⚔ | |
| Comparaison catalogue ↔ graphe | P | | ✔ | ✔ | ✔ | ✔ | | | | ⚔ | |
| Dédoublonnage | P | ✔ | | ✔ | ✔ | ✔ | | | | ⚔ | |
| Ajout d'entités / relations | P | ✔ | ✔ | ✔ | ✔ | ✔ | ✔ | ✔ | ✔ | ⚔ | ✔ |
| Renumérotation / migration | P | ✔ | | ✔ | | ✔ | ✔ | ✔ | ✔ | ⚔ | ✔ |
| Rattachement de contenu (ancrage) | P | ✔ | | ✔ | | ✔ | ✔ | ✔ | ✔ | ⚔ | ✔ |
| Changement de type / de schéma | P | ✔ | | ✔ | | ✔ | | | | ⚔ | |
| Modification du runtime | P | | | | | | | | ✔ | ⚔ | ✔ |
| Récits, presets, anchors | P | ✔ | | | | | | | ✔ | ⚔ | ✔ |
| Publication / export | P | | | ✔ | | | | ✔ | ✔ | ⚔ | ✔ |

**Deux règles de lecture.**
- **Toute ligne qui touche le graphe ou le runtime passe par ⚔.** Sans
  exception. C'est le seul enseignement solide des neuf incidents.
- **Aucune tâche ne mobilise plus de cinq instances actives.** Au-delà, la
  coordination coûte plus que la spécialisation ne rapporte — et la règle 3
  devient impraticable, parce que plus personne ne sait quelle sortie est
  encore de la donnée.

---

## 5. Séquence recommandée pour le chantier courant

Le chantier de la commande étant livré, voici la séquence appliquée au chantier
qui reste, **la dette d'ancrage** : 8 sections de la thèse existent comme nœuds
et figurent au sommaire, sans aucun contenu rattaché — `I.1.3`, `I.2.1`,
`II.1.2`, `II.2.1`, `II.2.3`, `II.3.3`, `III.2.2`, `III.2.3`.

| # | Étape | Instance | Sortie | Bloque la suite si… |
|---|---|---|---|---|
| 1 | **Archéologie de la méthode** | Inventory + Hostile | la règle exacte qui a produit `occurrence_count`, ou le constat qu'elle n'est pas reproductible | la méthode n'est pas reproductible → on s'arrête, on ne l'approxime pas |
| 2 | **Prospection du contenu** | Thesis-Archivist | volume réel de chaque section, corps **et notes séparés** | une section est vide dans la thèse → rien à rattacher, on le dit |
| 3 | **Validation contradictoire** | Hostile | la méthode reproduit-elle les sections déjà connues ? | le taux de reproduction est faible → retour à l'étape 1 |
| 4 | **Classification** | Semantic | ce qui est rattachable, ce qui demande arbitrage | — |
| 5 | **Patch** | Patch-Writer | `patch_NN_*.json`, déposé, non appliqué | — |
| 6 | **Build candidat** | Graph-Builder | `v107` + reçu | une vérification échoue → pas d'écriture |
| 7 | **Revue visuelle** | Visual | avant/après chiffré, en navigateur | une entrée de sommaire régresse |
| 8 | **Contestation finale** | Hostile | `devil-advocate-review.md` | — |
| 9 | **PR** | PR-Operator | PR, points ouverts listés non tranchés | la checklist § 3.11 échoue |

**L'étape 1 est un verrou, pas une formalité.** Si `occurrence_count` n'est pas
reproductible, fabriquer des comptes plausibles remplirait le graphe de
données qui **ressemblent** aux existantes sans en avoir la provenance. Ce
serait la pire issue possible : une dette invisible substituée à une dette
visible.

---

## 6. Décisions réservées à Maël

Aucune instance ne les tranche. Elles sont listées ici pour qu'on cesse de les
redécouvrir.

| # | Décision | Depuis | Enjeu |
|---|---|---|---|
| 1 | **Sémantique d'`appears in section`** | juin 2026 | ~6 000 relations. « Citée dans » et « la section traite de » ne sont pas la même chose ; le lecteur les affiche pareil |
| 2 | **`Mining pools`** : quel est le canonique ? | 02/08/2026 | le mécanisme a désigné le moins relié (degré 4 contre 7) |
| 3 | **`III.3` doit-elle être retypée `ThesisSection` ?** | 03/08/2026 | type à occurrence unique sur 74 sections |
| 4 | **La relation orpheline Ostrom** | mai 2026 | `from` tronqué renvoyant à Ostrom 1990 ; tolérance nommée en CI |
| 5 | **Fusion effective des doublons marqués** | 02/08/2026 | `patch_10` marque, ne fusionne pas — délibérément |
| 6 | **PR #95 et #96** | 28/06/2026 | mémo d'arbitrage de représentation, E1–E7 / D1–D6 |
| 7 | **Les 8 sections vides doivent-elles être rattachées ?** | 03/08/2026 | ou la thèse est-elle mince à ces endroits ? |
| 8 | **Dérive de libellé de l'introduction** | 03/08/2026 | le graphe écrit « cryptomonnaies », le texte « CM » |

---

## 7. Opérations automatisables sans arbitrage scientifique

Le critère : **l'opération est-elle vérifiable contre une source du dépôt, sans
jugement d'interprétation ?**

**Automatisable.**
- Contrôles d'intégrité : endpoints, doublons d'ID, orphelins, ops orphelines,
  cohérence `space.version` / nom de fichier.
- Réalignement d'un libellé sur le titre de la thèse — la source est le
  markdown, l'écart se constate.
- Remappage des cartes d'ancrage après renumérotation — **simultané, jamais
  séquentiel**.
- Reconstruction de `narrative-anchors.json` depuis le graphe.
- Détection des références mortes du runtime après renommage.
- Câblage d'arborescence `section of` / `has section` sur un motif réciproque
  déjà employé.
- Génération d'identifiants déterministes.
- Rejeu des quatre étapes de la CI en local.
- Ouverture des pages en navigateur et relevé des compteurs.

**Non automatisable — arbitrage requis.**
- Fusionner ou supprimer une entité.
- Choisir le canonique d'une paire.
- Créer ou retirer un type.
- Trancher la sémantique d'un type de relation.
- Rattacher du contenu à une section quand la méthode n'est pas reproductible.
- Écrire un résumé ou un argument central : **ce serait écrire à la place de
  l'auteur.**
- Modifier le texte de la thèse.

**Zone grise, à traiter comme non automatisable jusqu'à décision.** Créer une
entité que la thèse nomme mais que le graphe ignore : la source existe, mais
décider qu'elle mérite un nœud est un jugement. Le dépôt a tranché dans le sens
conservateur — *pas d'entité sans relation observée* — et les 11 sections
créées en v106 respectent cette limite : structure seulement, et elles le
déclarent dans `evidenceStatus`.

---

## 8. Ce que ce document ne fait pas

- Il ne crée aucun fichier d'agent. La règle 2 l'interdit : une instance
  **propose** sa spécification, un humain la valide. Les quatre créations
  attendent l'accord de Maël.
- Il ne modifie ni le graphe, ni le runtime, ni un script, ni un patch.
- Il ne tranche aucune des huit décisions du § 6.
- Il ne prétend pas que les onze instances soient justifiées. **Quatre le
  sont**, avec preuve datée. Le dire est le travail ; l'organigramme complet
  aurait été plus flatteur et moins vrai.
