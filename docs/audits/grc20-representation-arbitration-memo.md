# Scientific Arbitration Memo — Representation Audit v1

**Date** : 2026-06-28  
**Source** : `docs/audits/grc20-representation-audit-v1.md` (PR #94, merged)  
**Graph audité** : `grc20-these-mael-rolland-v97.json`  
**Branche** : `agent/grc20-representation-arbitration-memo`  
**Mode agent** : A (audit documentaire, lecture seule)

## Objet

Ce mémo prépare l'arbitrage scientifique de Maël Rolland sur les sept questions ouvertes (E1–E7) identifiées dans le *Representation Audit v1*. Il ne propose aucun patch appliqué, ne crée aucune version du graphe, et ne modifie aucun fichier runtime, script, story ou déploiement.

Pour chaque question, il présente le problème diagnostiqué, l'enjeu scientifique, trois options d'action (A : ne rien changer, B : correction minimale, C : correction ambitieuse), les effets attendus sur le graphe, les risques de surinterprétation, les fichiers concernés si un patch futur est décidé, et la décision requise.

## Structure de décision

Les recommandations E1–E7 relèvent de quatre catégories de décision distinctes :

| Catégorie | Questions | Autorité |
|---|---|---|
| Décision scientifique (interprétation de la thèse) | E1, E2, E4 | Maël Rolland uniquement |
| Décision ontologique (modélisation du graphe) | E3, E5 | Maël Rolland, après consultation le cas échéant |
| Décision empirique (matériau disponible) | E6 | Maël Rolland (connaissance du terrain) |
| Décision théorique (explicitation du cadre) | E7 | Maël Rolland |

Toutes sont des **décisions scientifiques** au sens de la charte agentique (`agents/README.md`) : aucun agent ne peut les trancher.

---

## E1 — Cinq contributions de la conclusion : 5 Arguments distincts ou 1 synthétique ?

### Problème diagnostiqué

La conclusion de la thèse présente explicitement **cinq contributions distinctes** :

1. L'approche infrastructurelle (decrypter la crypto par les études infrastructurelles) ;
2. La sociologie des crises (de l'acéphalisme à la visibilisation de la gouvernance) ;
3. L'intégration à la théorie monétaire (CM comme épreuve d'explicitation de l'IMF) ;
4. Le travail de traduction (dialogue entre coiners et professionnels de l'argent) ;
5. La question politique ouverte (CM comme boucs émissaires d'un système en crise).

Le graphe v97 contient 7 entités de type `Argument`, dont une « Thèse centrale (infrastructures, crises, gouvernance polycentrique) » qui fusionne ces cinq dimensions en une seule proposition. Les cinq contributions ne sont pas différenciées comme des arguments distincts. Un lecteur du graphe ne voit pas que la thèse se positionne sur cinq fronts théoriques simultanés.

### Enjeu scientifique

La thèse est une démonstration **multi-fronts** : elle ne se contente pas de dire « les CM sont des infrastructures à gouvernance polycentrique », elle contribue simultanément à la sociologie des crises, à la théorie monétaire institutionnaliste, à la réflexivité épistémologique et au débat politique sur le système monétaire. Effacer cette pluralité revient à réduire la thèse à son résultat synthétique, en perdant sa portée contributive.

### Option A — Ne rien changer

Conserver l'`Argument` unique « Thèse centrale ». Les cinq contributions restent implicites dans les concepts et sections.

- **Avantage** : simplicité maximale, pas de risque de fragmentation argumentative.
- **Inconvénient** : la portée pluraliste de la thèse reste invisible dans le graphe. Le lecteur ne distingue pas les cinq apports.

### Option B — Correction minimale

Ajouter 5 entités `Argument` distinctes (une par contribution), reliées au `Chapter` Conclusion et à l'`Argument` existant « Thèse centrale » par une relation de type `contributes to` ou `part of`. Ne pas supprimer l'Argument synthétique.

- **Avantage** : la pluralité devient lisible sans détruire l'unité. L'Argument synthétique reste le point d'entrée.
- **Inconvénient** : 5 nouvelles entités + ~10 relations. Risque de confusion si les libellés des Arguments sont trop proches.

### Option C — Correction ambitieuse

Remplacer l'`Argument` unique par 5 `Argument` distincts, chacun relié non seulement à la Conclusion mais aussi au(x) `CoreConcept` et `TheoreticFramework` qu'il mobilise. Ajouter une entité `AnalyticClaim` « Thèse synthétique » qui agrège les cinq sans les fusionner.

- **Avantage** : chaque contribution devient un nœud argumentatif avec son propre réseau de preuves et de concepts. La structure devient un véritable graphe d'arguments, pas un graphe de concepts.
- **Inconvénient** : restructuration plus lourde. Risque de sur-découpage si les frontières entre contributions ne sont pas nettes dans le texte.

### Effets attendus sur le graphe

| Option | Nouvelles entités | Nouvelles relations | Impact structurel |
|---|---|---|---|
| A | 0 | 0 | Nul |
| B | +5 | +10–15 | Modéré : enrichissement local de la Conclusion |
| C | +5–6 | +20–30 | Fort : restructuration du sous-graphe argumentatif |

### Risques de surinterprétation

- Si les libellés des 5 Arguments sont formulés par l'agent sans validation stricte du texte de la conclusion, ils risquent de refléter une lecture analytique plutôt que l'intention explicite de l'auteur.
- Le découpage en 5 contributions est explicite dans la conclusion (5 sous-sections titrées), ce qui réduit ce risque. Mais la *formulation* de chaque Argument comme proposition assertive doit rester fidèle au texte.

### Fichiers probablement concernés si patch futur

- `grc20-these-mael-rolland-v98.json` (ou version suivante) — ajout d'entités et relations.
- `story-presets.mjs` — étape finale de `structure-these` (s9) à adapter si les Arguments sont différenciés.
- `docs/grc20_narrative_matrix.md` — matrice à mettre à jour.

### Décision requise de Maël

> Les cinq contributions de la conclusion doivent-elles être modélisées comme 5 `Argument` distincts (option B/C), ou l'Argument synthétique unique suffit-il (option A) ? Si oui, l'option B (enrichissement minimal) ou C (restructuration argumentative) ?

---

## E2 — Distinction gouvernance par / sur l'infrastructure : CoreConcept explicite ?

### Problème diagnostiqué

La distinction entre gouvernance **par** l'infrastructure (le protocole encode des règles exécutoires) et gouvernance **sur** l'infrastructure (des acteurs humains modifient, contournent ou renégocient ces règles) est **la distinction la plus décisive** de la conclusion. La thèse la formule explicitement :

> « Au-delà d'une gouvernance *par* l'infrastructure, la gouvernance *sur* l'infrastructure des CM est conflictuelle et polycentrique. » (p. 336)

Cette distinction n'existe pas comme entité dans le graphe. Elle est impliquée par `Space of Rule / Space of Discretion` et par `Gouvernance duale`, mais aucun nœud ne la nomme explicitement. Un lecteur qui n'a pas lu la thèse ne peut pas la reconstruire.

### Enjeu scientifique

Cette distinction est le **point de bascule** entre une lecture technique (le code gouverne) et une lecture socio-politique (des acteurs gouvernent le code) des CM. C'est elle qui transforme l'infrastructure d'objet neutre en lieu de pouvoir. Si le graphe ne la rend pas lisible, il perd l'apport théorique le plus original de la thèse sur le plan conceptuel.

### Option A — Ne rien changer

La distinction reste implicite dans `Space of Rule / Space of Discretion` et `Gouvernance duale`.

- **Avantage** : pas de redondance conceptuelle apparente.
- **Inconvénient** : le concept le plus original de la thèse n'est pas nommé. Le lecteur doit l'inférer.

### Option B — Correction minimale

Ajouter une entité `CoreConcept` « Gouvernance par l'infrastructure vs gouvernance sur l'infrastructure », reliée à `Gouvernance polycentrique`, `Space of Rule / Space of Discretion` et au `Chapter` Conclusion. Ne pas créer deux entités séparées.

- **Avantage** : la distinction est nommée et reliée, sans multiplier les entités.
- **Inconvénient** : une seule entité ne capture pas la tension dynamique entre les deux pôles.

### Option C — Correction ambitieuse

Créer un couple d'entités reliées : « Gouvernance par l'infrastructure » et « Gouvernance sur l'infrastructure », typées `CoreConcept`, reliées par une relation `opposedTo` ou `tensionWith`. Les relier à `Space of Rule / Space of Discretion` (par/sur ↔ règle/discrétion), à `Gouvernance polycentrique` et à la Conclusion.

- **Avantage** : la tension devient structurelle. Le graphe montre deux pôles en relation, pas un concept statique.
- **Inconvénient** : 2 entités au lieu d'1. Risque de confusion avec `Space of Rule / Space of Discretion` si les relations ne sont pas soigneusement typées.

### Effets attendus sur le graphe

| Option | Nouvelles entités | Nouvelles relations | Impact structurel |
|---|---|---|---|
| A | 0 | 0 | Nul |
| B | +1 | +3–4 | Faible : ajout d'un nœud-pivot |
| C | +2 | +6–8 | Modéré : création d'un couple conceptuel tensionnel |

### Risques de surinterprétation

- La distinction par/sur est **explicite dans la conclusion** (p. 336), ce qui élimine le risque de surinterprétation sur le concept lui-même.
- Le risque réside dans la **relation avec Space of Rule / Space of Discretion** : si le graphe relie trop étroitement par/sur et règle/discrétion, un lecteur peut les confondre, alors qu'ils opèrent à des niveaux analytiques différents (l'un infrastructurel, l'autre monétaire/gouvernemental).

### Fichiers probablement concernés si patch futur

- `grc20-these-mael-rolland-v98.json` — ajout d'entités et relations.
- `story-presets.mjs` — story `qui-gouverne-reellement` et étape s8 de `structure-these` à enrichir.
- `docs/grc20_ontology_audit.md` — mise à jour de la doctrine de typage.

### Décision requise de Maël

> La distinction gouvernance *par* / *sur* l'infrastructure doit-elle devenir un `CoreConcept` explicite (option B), un couple tensionnel (option C), ou rester implicite dans `Space of Rule / Space of Discretion` (option A) ?

---

## E3 — Travail de traduction (Callon) : entité dédiée ou note ?

### Problème diagnostiqué

La conclusion identifie le « travail de traduction » comme l'une des cinq contributions de la thèse. Maël mobilise explicitement la sociologie de la traduction (Callon, 1986) pour caractériser son propre positionnement : être l'entremetteur entre les coiners et les professionnels de l'argent, comme Callon entre les pêcheurs et les chercheurs. Cette dimension réflexive et dialogique — parler *aux* coiners, pas seulement *d'*eux — est totalement absente du graphe.

Le graphe contient `Theorie de l'acteur-reseau (ANT)` et `Sociologie de la traduction` comme `TheoreticFramework`, mais aucune entité ne modélise le travail de traduction comme *pratique réflexive du chercheur*.

### Enjeu scientifique

Le travail de traduction n'est pas un cadre théorique appliqué aux CM : c'est une **contribution méthodologique et éthique** de la thèse. Il exprime le refus de l'enquête purement extérieure (sociologisme) comme de l'adhésion purement indigène (technologisme). L'effacer du graphe, c'est rendre invisible le positionnement épistémologique qui donne à la thèse sa singularité dialogique.

### Option A — Ne rien changer

Le travail de traduction reste une note de positionnement dans la conclusion, non modélisée dans le graphe. `Sociologie de la traduction` et `ANT` restent comme frameworks.

- **Avantage** : pas de confusion entre un cadre théorique (Callon appliqué aux acteurs) et une pratique réflexive (Callon appliqué au chercheur lui-même).
- **Inconvénient** : la dimension la plus originale du positionnement de la thèse est invisible.

### Option B — Correction minimale

Ajouter une entité `Concept` ou `Argument` « Travail de traduction du chercheur », reliée à `Sociologie de la traduction`, au `Chapter` Conclusion et à l'entité `These` (ou `Argument` thèse centrale). Type : `Argument` ou `Method`.

- **Avantage** : la dimension réflexive devient visible comme un nœud distinct.
- **Inconvénient** : le graphe risque d'introduire un niveau méta (le chercheur sur lui-même) qui n'est pas représenté ailleurs.

### Option C — Correction ambitieuse

Créer un mini-sous-graphe réflexif : entité `Method` « Travail de traduction », reliée à `Sociologie de la traduction` (framework mobilisé), à un `Argument` « Dialogue avec les coiners » (contribution), et à un `Concept` « Positionnement emic/etic » (principe méthodologique). Relier l'ensemble à la Conclusion et au glossaire.

- **Avantage** : le positionnement épistémologique de la thèse devient un sous-graphe explorables, pas un nœud isolé.
- **Inconvénient** : introduit un niveau méta qui peut sembler déplacé dans un graphe qui modélise les CM, pas le chercheur.

### Effets attendus sur le graphe

| Option | Nouvelles entités | Nouvelles relations | Impact structurel |
|---|---|---|---|
| A | 0 | 0 | Nul |
| B | +1 | +3 | Très faible |
| C | +3–4 | +8–10 | Modéré : nouveau sous-graphe réflexif |

### Risques de surinterprétation

- La traduction callonienne est **explicite dans la conclusion** (citation de Callon en exergue, sous-section dédiée), ce qui réduit le risque.
- Le risque réside dans la **formulation** : l'agent ne doit pas reformuler le positionnement de Maël, mais s'en tenir à ses termes (dialogue, entremise, langage et́tique fondé sur le langage émique).

### Fichiers probablement concernés si patch futur

- `grc20-these-mael-rolland-v98.json` — ajout d'entités.
- `docs/grc20_ontology_audit.md` — clarification du type (`Method` vs `Argument`).

### Décision requise de Maël

> Le travail de traduction (Callon) mérite-t-il une entité dédiée dans le graphe (option B), un sous-graphe réflexif (option C), ou doit-il rester hors du périmètre de représentation comme note de positionnement (option A) ?

---

## E4 — Question politique ouverte (boucs émissaires) : entrer dans le graphe ?

### Problème diagnostiqué

La thèse se termine sur une **question politique délibérément ouverte** : les CM sont-elles des boucs émissaires commodes d'un système monétaire en crise ? Maël refuse explicitement de clore le débat normatif : il ne dit pas si les CM sont « bonnes » ou « mauvaises », mais souligne que les maux qu'on leur attribue (dérégulation, spéculation, consommation énergétique) existent dans le système traditionnel à une échelle incommensurablement plus grande.

Cette question est totalement absente du graphe. Aucune entité ne la porte. Le lecteur du graphe ne perçoit pas le refus délibéré de clore le débat, ni le positionnement citoyen qui sous-tend la thèse.

### Enjeu scientifique

L'absence de closure normative n'est pas un défaut de la thèse, c'est un **choix épistémologique assumé**. La sociologie des controverses et l'approche infrastructurenelle ne visent pas à dire le vrai ou le juste, mais à rendre visible la complexité. Représenter la question ouverte dans le graphe, c'est respecter ce choix. L'omettre, c'est transformer la thèse en une démonstration close, ce qu'elle refuse d'être.

Cependant, l'introduction d'une question non résolue dans un graphe d'arguments assertifs pose un **problème de typage** : comment modéliser une incertitude dans un système qui ne connaît que des faits, des concepts et des relations ?

### Option A — Ne rien changer

La question politique reste hors graphe. Elle est accessible dans le texte de la conclusion et le lecteur du site web.

- **Avantage** : le graphe reste un système d'arguments stabilisés, pas un espace de débat ouvert.
- **Inconvénient** : le refus de closure et le positionnement citoyen sont invisibles.

### Option B — Correction minimale

Ajouter une entité `AnalyticClaim` ou `Argument` « CM comme boucs émissaires d'un système monétaire en crise », reliée à la Conclusion, avec un attribut `status: open_question` ou `resolved: false`. La relier aux concepts pertinents (`Souverainete monetaire`, système monétaire traditionnel).

- **Avantage** : la question ouverte est nommée et marquée comme non résolue.
- **Inconvénient** : introduit un attribut nouveau (`status`) qui n'existe pas dans le schéma actuel.

### Option C — Correction ambitieuse

Créer un sous-graphe « Débat politique ouvert » avec 3–4 entités : (1) la question des boucs émissaires, (2) la comparaison consommation énergétique CM vs système traditionnel, (3) la question de la privatisation de la monnaie, (4) la reflexion sur les banques centrales comme technocrates. Relier à la Conclusion et aux concepts monétaires.

- **Avantage** : la dimension politique de la thèse devient un espace explorables.
- **Inconvénient** : risque de transformer une question ouverte en un ensemble d'arguments assertifs, ce qui contredit l'intention.

### Effets attendus sur le graphe

| Option | Nouvelles entités | Nouvelles relations | Impact structurel |
|---|---|---|---|
| A | 0 | 0 | Nul |
| B | +1 | +2–3 | Très faible |
| C | +4 | +8–10 | Modéré : nouveau sous-graphe politique |

### Risques de surinterprétation

- **Risque élevé**. La question des boucs émissaires est délibérément ouverte. La modéliser comme un Argument assertif (option B sans attribut `status`) la transformerait en prise de position, ce qui n'est pas l'intention de la thèse.
- Si l'option B est retenue, l'attribut `status: open_question` est **indispensable** pour éviter la surinterprétation.
- Si l'option C est retenue, chaque entité du sous-graphe doit être formulée comme une **question**, pas comme une affirmation.

### Fichiers probablement concernés si patch futur

- `grc20-these-mael-rolland-v98.json` — ajout d'entités et éventuellement d'un nouvel attribut.
- `docs/grc20_ontology_audit.md` — clarification du typage des questions ouvertes.

### Décision requise de Maël

> La question politique ouverte (boucs émissaires) doit-elle entrer dans le graphe comme question non résolue (option B/C), ou rester hors du périmètre de représentation (option A) ? Si oui, comment marquer son caractère non résolu ?

---

## E5 — CVE individualisées : réduire ou conserver la granularité ?

### Problème diagnostiqué

Le graphe v97 contient environ **45 entités CVE Bitcoin individualisées** (de CVE-2010-5137 à CVE-2018-20587), modélisées comme `InfrastructureEvent` ou `CrisisEvent`. Or la thèse n'étudie analytiquement qu'**une seule** d'entre elles : CVE-2018-17144. Les autres sont mentionnées dans le panorama historique du chapitre III pour contextualiser la politique de crise de Bitcoin, mais n'ont pas le même statut analytique.

Cette granularité crée un **bruit visuel** : un lecteur qui explore le graphe en mode matrice voit une masse de bugs, ce qui peut donner l'impression que la thèse est une histoire des vulnérabilités Bitcoin plutôt qu'une démonstration sur la gouvernance discrète.

### Enjeu scientifique

La question est de savoir si le graphe doit **représenter l'exhaustivité empirique** de la thèse (qui mentionne effectivement ces CVE) ou **hiérarchiser analytiquement** les entités (en distinguant le cas principal des cas contextuels). C'est un choix entre fidélité encyclopédique et lisibilité argumentative.

### Option A — Ne rien changer

Conserver les 45 CVE individualisées au même niveau.

- **Avantage** : exhaustivité maximale, fidélité au matériau brute.
- **Inconvénient** : bruit visuel, confusion entre cas analytique principal et cas contextuels.

### Option B — Correction minimale

Conserver les entités mais ajouter un attribut `analyticRole: primary_case` pour CVE-2018-17144 (et `The DAO`) et `analyticRole: context` pour les autres. Ne pas supprimer d'entités.

- **Avantage** : hiérarchisation analytique sans perte de données.
- **Inconvénient** : 43 entités à annoter. Le bruit visuel persiste si le runtime n'exploite pas l'attribut.

### Option C — Correction ambitieuse

Regrouper les CVE contextuelles sous une entité parent `InfrastructureEvent` « Crises historiques de Bitcoin (panorama) », reliée au chapitre III. Conserver CVE-2018-17144 et The DAO comme entités individuelles de premier niveau. Transformer les 43 autres en entités secondaires (relations `part of` vers le panorama).

- **Avantage** : le graphe devient lisible. Le cas principal est visuellement distinct du panorama.
- **Inconvénient** : restructuration de ~43 entités. Risque de perte d'informations si les CVE contextuelles ont des relations propres utiles.

### Effets attendus sur le graphe

| Option | Entités modifiées | Nouvelles relations | Impact structurel |
|---|---|---|---|
| A | 0 | 0 | Nul |
| B | +43 attributs | 0 | Faible (annotations) |
| C | ~43 restructurées | +43 | Fort : restructuration du sous-graphe CVE |

### Risques de surinterprétation

- Le risque de surinterprétation est **faible** : les CVE sont des faits techniques documentés, pas des interprétations.
- Le risque principal est de **perte d'information** (option C) si les CVE contextuelles ont des relations propres (acteurs, dates, dispositifs) qui seraient masquées par le regroupement.

### Fichiers probablement concernés si patch futur

- `grc20-these-mael-rolland-v98.json` — annotations ou restructuration.
- `graphe.html` — si le runtime doit exploiter un attribut `analyticRole` (option B).
- `docs/grc20_ontology_audit.md` — clarification du statut des entités contextuelles.

### Décision requise de Maël

> Faut-il réduire le bruit des CVE non mobilisées analytiquement au profit d'un panorama agrégé (option C), annoter leur rôle analytique sans les regrouper (option B), ou conserver la granularité actuelle (option A) ?

---

## E6 — Gouvernance ordinaire : modéliser ou respecter l'accès par les crises ?

### Problème diagnostiqué

La thèse insiste sur le fait que la gouvernance de huis clos est **ordinaire, routinière et consensuelle**, pas exceptionnelle. Les crises ne sont qu'un moyen d'y accéder heuristiquement. Mais le graphe modélise presqu'exclusivement les **crises et leurs dispositifs exceptionnels** (responsible disclosure, hard fork, Carbon Vote). La maintenance ordinaire, les reviews de code quotidiennes, la coordination routinière entre Core Devs sont faiblement représentées.

Le `NarrativeCluster` « Gouvernance de maintenance (huis clos routinier) » existe, mais il n'est pas activé dans les stories comme un argument central.

### Enjeu scientifique

La question est de savoir si le graphe reproduit légitimement le fait que la thèse accède à la gouvernance ordinaire *via* les crises (auquel cas la sous-représentation est fidèle au terrain), ou si le graphe devrait **compléter** la thèse en modélisant la gouvernance ordinaire de façon plus autonome (auquel cas la sous-représentation est un déficit).

C'est un choix entre **fidélité à la méthode d'enquête** (les crises comme point d'accès) et **fidélité à l'argument** (la gouvernance ordinaire comme objet réel).

### Option A — Ne rien changer

La gouvernance ordinaire reste accessible via les crises. Le `NarrativeCluster` existe mais n'est pas développé.

- **Avantage** : fidélité à la méthode d'enquête. Le graphe ne prétend pas représenter ce que la thèse n'a pas directement observé.
- **Inconvénient** : le « huis clos routinier » — argument central de la thèse — reste sous-modélisé.

### Option B — Correction minimale

Ajouter 3–5 entités pour les pratiques ordinaires documentées dans la thèse : `Review de code`, `Coordination entre Core Devs`, `Processus de merge`, `Maintenance des versions`. Les relier au `NarrativeCluster` existant et au chapitre III. Ajouter une étape à la story `qui-gouverne-reellement`.

- **Avantage** : la gouvernance ordinaire devient visible sans contredire la méthode d'enquête.
- **Inconvénient** : nécessite de vérifier que le matériau empirique (entretiens, observations) documente suffisamment ces pratiques.

### Option C — Correction ambitieuse

Créer un sous-graphe « Gouvernance ordinaire » avec des entités pour les arènes quotidiennes, les dispositifs de coordination, les routines de maintenance, les rôles (mainteneur, reviewer, contributeur), et les relier aux `GovernanceArena`, `StakeholderCategory` et `GovernanceProcess` existants. Activer ce sous-graphe dans une story dédiée ou comme étapes additionnelles de `qui-gouverne-reellement`.

- **Avantage** : la thèse selon laquelle « les crises révèlent la structure ordinaire » devient démontrable dans le graphe.
- **Inconvénient** : risque de modéliser des pratiques qui ne sont pas suffisamment documentées dans le matériau empirique de la thèse.

### Effets attendus sur le graphe

| Option | Nouvelles entités | Nouvelles relations | Impact structurel |
|---|---|---|---|
| A | 0 | 0 | Nul |
| B | +3–5 | +8–10 | Modéré : enrichissement local |
| C | +10–15 | +25–30 | Fort : nouveau sous-graphe |

### Risques de surinterprétation

- **Risque modéré à élevé**. Si les entités de gouvernance ordinaire sont créées sans ancrage dans le matériau empirique de la thèse (entretiens, observations participantes), elles risquent d'être des **modélisations génériques** de pratiques de développement logiciel, pas des données de terrain.
- La thèse documente la gouvernance ordinaire *à travers* les crises. Modéliser la gouvernance ordinaire de façon autonome nécessite de vérifier que les 27 entretiens et 27 observations en parlent directement.

### Fichiers probablement concernés si patch futur

- `grc20-these-mael-rolland-v98.json` — ajout d'entités.
- `story-presets.mjs` — étendre `qui-gouverne-reellement`.
- `docs/grc20_evidence_audit.md` — vérification de l'ancrage empirique.

### Décision requise de Maël

> La gouvernance ordinaire (maintenance, coordination routinière) est-elle suffisamment documentée dans le matériau empirique pour être modélisée de façon autonome (option B/C), ou le graphe reproduit-il légitimement le fait que la thèse y accède *via* les crises (option A) ?

---

## E7 — Polycentricité et Ostrom : expliciter le lien théorique ?

### Problème diagnostiqué

Le graphe contient `IAD Framework` et `Social Ecological System (SES)` comme `TheoreticFramework`, ce qui indique une mobilisation d'Ostrom. Mais le concept de **polycentricité** — qui est explicitement ostromien — n'est pas relié à ces frameworks dans le graphe. La thèse mobilise Ostrom (IAD/SES) pour caractériser la gouvernance des CM comme polycentrique, mais ce lien théorique est implicite.

Un lecteur qui voit « Gouvernance polycentrique » et « IAD Framework » dans le graphe ne sait pas qu'ils sont liés, à moins de connaître lui-même Ostrom.

### Enjeu scientifique

Le concept de polycentricité est l'un des apports théoriques les plus importants de la thèse (et l'un des plus visibles : il est dans le titre). Le détacher de sa source théorique ostromienne, c'est risquer de le transformer en un mot-valise, alors qu'il renvoie à une tradition institutionnaliste précise (Ostrom, 1990 ; McGinnis, 1999).

Cependant, la thèse ne fait pas de la polycentricité un concept purement ostromien : elle l'adapte, le redéfinit et l'applique à des objets (infrastructures numériques) qu'Ostrom n'a pas traités. Expliciter le lien à Ostrom ne doit pas enfermer le concept dans son cadre d'origine.

### Option A — Ne rien changer

La polycentricité reste un `CoreConcept` sans lien explicite à `IAD Framework` ou `SES`.

- **Avantage** : le concept reste ouvert, non enfermé dans un cadre théorique unique.
- **Inconvénient** : la généalogie théorique est invisible.

### Option B — Correction minimale

Ajouter une relation `appliedTo` ou `derivedFrom` entre `IAD Framework` et `Gouvernance polycentrique`, et entre `Social Ecological System (SES)` et `Gouvernance polycentrique`.

- **Avantage** : le lien théorique devient explicite sans alourdir le graphe.
- **Inconvénient** : la relation `derivedFrom` peut suggérer une dérivation directe, alors que la thèse adapte et transforme le concept.

### Option C — Correction ambitieuse

Ajouter une entité `Concept` intermédiaire « Polycentricité ostromienne (adaptée aux CM) », reliée à `IAD Framework` (source théorique), à `Gouvernance polycentrique` (concept de la thèse), et à un `Argument` « Adaptation de la polycentricité aux infrastructures numériques ».

- **Avantage** : la distinction entre concept-source (Ostrom) et concept-objet (thèse) devient claire.
- **Inconvénient** : complexification. Risque de sur-modélisation d'un lien qui pourrait être simple.

### Effets attendus sur le graphe

| Option | Nouvelles entités | Nouvelles relations | Impact structurel |
|---|---|---|---|
| A | 0 | 0 | Nul |
| B | 0 | +2 | Très faible |
| C | +2 | +4 | Faible à modéré |

### Risques de surinterprétation

- **Risque faible**. Le lien entre polycentricité et Ostrom est bien établi dans la littérature et attesté dans la thèse.
- Le risque réside dans la **nature de la relation** : `derivedFrom` peut suggérer une simple transposition, alors que la thèse *adapte* le concept à un domaine (infrastructures numériques) qu'Ostrom n'a pas traité. Une relation `adaptedFrom` ou `inspiredBy` serait plus juste.

### Fichiers probablement concernés si patch futur

- `grc20-these-mael-rolland-v98.json` — ajout de relations ou d'entités.
- `docs/grc20_ontology_audit.md` — clarification du type de relation.

### Décision requise de Maël

> Le lien entre polycentricité et Ostrom (IAD/SES) doit-il être explicité dans le graphe (option B/C), ou est-ce un rapprochement théorique qui reste à la charge du texte (option A) ?

---

## Synthèse des décisions attendues

| Question | Catégorie | Option recommandée par l'audit | Justification |
|---|---|---|---|
| E1 (5 contributions conclusion) | Scientifique | **B** | La pluralité est explicite dans le texte (5 sous-sections titrées). L'option B la rend visible sans restructuration lourde. |
| E2 (gouvernance par/sur) | Scientifique | **B ou C** | Le concept le plus décisif de la thèse doit être nommé. Le couple tensionnel (C) est préférable si l'on veut rendre la dynamique. |
| E3 (travail de traduction Callon) | Ontologique | **B** | Une entité dédiée suffit. Le sous-graphe réflexif (C) risque d'introduire un niveau méta disproportionné. |
| E4 (boucs émissaires) | Scientifique | **A ou B** | Si B, l'attribut `status: open_question` est obligatoire. L'option C risque de fermer une question que la thèse maintient ouverte. |
| E5 (CVE individualisées) | Ontologique | **B** | L'annotation du rôle analytique est le compromis le plus sûr entre exhaustivité et lisibilité. |
| E6 (gouvernance ordinaire) | Empirique | **A ou B** | Dépend du matériau empirique disponible. Si la thèse documente suffisamment la maintenance ordinaire, B est justifié. Sinon, A est fidèle à la méthode. |
| E7 (polycentricité/Ostrom) | Théorique | **B** | Une relation simple suffit. Le concept reste ouvert tout en étant rattaché à sa généalogie. |

> **Ces recommandations sont des avis argumentés, pas des décisions.** L'arbitrage final appartient à Maël Rolland. Certaines options recommandées (par exemple E1-B) peuvent être écartées si l'estimation de l'effort ou l'intention de représentation l'exige.

---

## Calendrier suggéré (indicatif)

| Phase | Action | Décisions requises | Mode agent |
|---|---|---|---|
| 1. Arbitrage | Maël tranche E1–E7 | Toutes | N/A (humain) |
| 2. Spécification | Rédiger un patch spec pour chaque décision positive | E1–E7 retenues | B (proposal) |
| 3. Implémentation | Appliquer les patches en v98 | E1–E7 retenues | C (patch/PR) |
| 4. Validation | Audit post-patch (representation audit v2) | Toutes | A (audit) |

---

## Non-actions de cette mission

- Aucune modification du JSON (`grc20-these-mael-rolland-v97.json`).
- Aucune création de v98.
- Aucune modification de `graphe.html`, `story-presets.mjs`, `narrative-anchors.json`.
- Aucune modification de scripts ou de déploiement.
- Aucun patch appliqué.
- Aucun merge.

## Source

- `docs/audits/grc20-representation-audit-v1.md` (PR #94, merged dans `codex/create-expand-from-node-planning-documents`).
