# GRC-20 Representation Audit v1

**Date** : 2026-06-28  
**Graph audité** : `grc20-these-mael-rolland-v97.json` (2 263 entités, 20 042 relations, 55 types, 130 types de relations)  
**Branche** : `agent/grc20-representation-audit-v1`  
**Mode agent** : A (audit documentaire, aucune modification de fichier de données, runtime, script ou déploiement)

## Question centrale

> Si un lecteur ne consultait que le graphe GRC-20, les vues narratives, les stories et les audits existants, comprendrait-il correctement la thèse, avec ses nuances, ses équilibres et ses limites ?

## Méthode

- Lecture du graphe v97 : analyse programmatique des types d'entités, des relations, des sections, des clusters narratifs, des concepts centraux, des arguments et des crises.
- Lecture de la thèse : `assets/MD/00_introduction.md` à `04_conclusion.md`, avec attention particulière aux arguments centraux, à la progression démonstrative et aux nuances explicites.
- Lecture des stories : `story-presets.mjs` (5 stories, 38 étapes, 167 focus nodes).
- Lecture des audits antérieurs : `grc20_coverage_fidelity_audit_2026-04-01.md` (v96), `grc20_evidence_audit.md`, `grc20_ontology_audit.md`, `grc20_views_audit.md`, `grc20_narrative_matrix.md`, `grc20-story-focus-resolution-audit.md`, `grc20-visual-analytical-design-audit.md`, `grc20-audit-batch-001-summary.md`.
- Lecture du cadre agentique : `agents/README.md`, `agents/Agent_Creation_Rules.md`.
- Aucun test runtime exécuté (pas de navigateur, pas de `graphe.html`).

---

## Diagnostic général

Le graphe GRC-20 v97 **représente globalement bien** l'architecture argumentative de la thèse : la triade infrastructure → monétisation → gouvernance polycentrique y est lisible, les crises y jouent leur rôle heuristique, et le fil conceptuel règle/discrétion est présent. Les 8 CoreConcepts et 7 Arguments explicites constituent une colonne vertébrale conceptuelle fidèle.

Cependant, le graphe souffre de **quatre déséquilibres structurels** qui risquent de déformer la compréhension d'un lecteur externe :

1. **La masse référentielle écrase l'architecture argumentative.** Les `Reference` (760 entités) représentent 33,6 % du graphe et génèrent 42 % des relations. Un lecteur qui explore le graphe sans filtre narratif voit d'abord une bibliographie, pas une démonstration.
2. **La densité événementielle des crises masque leur fonction analytique.** 55 `CrisisEvent` + une cinquantaine de CVE individualisées constituent un réservoir empirique riche, mais leur abondance risque de faire lire le graphe comme une chronologie de bugs Bitcoin plutôt que comme une démonstration sur la gouvernance discrète.
3. **Le chapitre II, bien que rééquilibré en v97, reste conceptuellement sous-chaîné.** La progression « statut monétaire → monétisation → communauté de paiement → gouvernance polycentrique » existe dans les entités, mais les relations qui l'articulent comme un parcours démonstratif cohérent sont moins denses que celles qui relient les crises entre elles.
4. **La conclusion est représentée comme un résumé, non comme un résultat analytique à cinq volets.** La thèse propose cinq contributions distinctes dans sa conclusion (approche infrastructurelle, sociologie des crises, théorie monétaire, effort de traduction, question politique des boucs émissaires), mais le graphe ne les distingue pas comme des arguments séparés.

La **transition v96 → v97 a corrigé le déséquilibre chapitrale** signalé dans le coverage audit d'avril 2026 (qui mesurait I=296, II=51, Conclusion=1). En v97, la distribution des `appears in section` par préfixe chapitrale est nettement plus équilibrée :

| Chapitre | Relations `appears in section` | Part |
|---|---|---|
| Chapitre II | 2 784 | 23,9 % |
| Conclusion | 2 487 | 21,3 % |
| Chapitre I | 2 294 | 19,7 % |
| Chapitre III | 2 174 | 18,6 % |
| Introduction | 1 930 | 16,5 % |

Cette correction est un gain structurel majeur. Le présent audit porte donc principalement sur la **qualité de la représentation argumentative**, non sur la quantité brute d'entités par chapitre.

---

## 1. Couverture argumentative

### Arguments centraux bien représentés

| Argument de la thèse | Représentation dans le graphe | Jugement |
|---|---|---|
| Les CM sont des infrastructures sociotechniques, pas de purs protocoles | `CoreConcept`: « Infrastructure sociotechnique » ; `Argument`: « Thèse centrale » ; section I.2.1 (hub de degré 435) | **Fidèle** |
| La gouvernance des CM est polycentrique, pas absente | `CoreConcept`: « Gouvernance polycentrique » ; `CoreConcept`: « Gouvernance duale » ; `Argument`: « Polycentricité comme dynamique d'arènes et de légitimités » | **Fidèle** |
| Les crises révèlent la gouvernance ordinaire (fonction heuristique) | `CoreConcept`: « Mise en crise / Remise en ordre » ; `Argument`: « Crises comme épreuves d'explicitation (non téléologiques) » ; `NarrativeCluster`: « Crises comme épreuves d'explicitation » | **Fidèle** |
| Le débat règle/discrétion est réactivé par les CM | `CoreConcept`: « Gouvernance duale » ; concepts `Règle comme cristallisation normative située`, `Discrétion contrainte`, `Space of Rule / Space of Discretion`, `Règle contre discrétion (Rules vs Discretion)` | **Fidèle et bien relié** |
| Le syllogisme libéral-techniciste est réfuté | Entité dédiée `Syllogisme libéral-techniciste` ; story `fil-de-preuves` étape fp2 ; `Code is Law` comme objet-cible | **Fidèle** |
| Le nominalisme non étatiste déplace la question monétaire | `CoreConcept`: « Nominalisme monetaire non etatiste » ; `TheoreticFramework`: « Institutionnalisme Monetaire Francophone (IMF) » ; story `monetisation-cryptos` | **Fidèle** |

### Arguments absents, faibles ou trop implicites

| Argument ou nuance de la thèse | État dans le graphe | Impact |
|---|---|---|
| **Les cinq contributions distinctives de la conclusion** | Absentes comme arguments séparés. Le graphe a 7 `Argument`, mais aucun ne distingue : (1) l'approche infrastructurelle, (2) la sociologie des crises, (3) l'intégration théorie monétaire, (4) l'effort de traduction, (5) la question des boucs émissaires. | Un lecteur ne voit pas que la thèse se positionne sur cinq fronts théoriques simultanés. |
| **Le développement carnavalesque comme lecture analytique** | `CoreConcept`: « Développement carnavalesque » présent, mais le `Argument`: « Carnavalesque comme lecture analytique » est isolé et peu relié au chapitre I. | Le concept existe mais n'est pas mis en mouvement narrative. |
| **La distinction gouvernance par le protocole / sur le protocole** | Présente implicitement via `Space of Rule / Space of Discretion`, mais pas articulée comme un axe bimodal explicite dans les stories. | La distinction la plus décisive de la thèse (gouvernance *par* l'infrastructure vs *sur* l'infrastructure) n'est pas nommée comme telle dans le graphe. |
| **La communauté de paiement comme concept pivot** | `Communaute de paiement / Groupe monetaire` existe (résolu via alias dans les stories), mais sa centralité analytique — pivot entre monétisation et gouvernance — n'est pas rendue par des relations structurelles fortes. | Le concept existe mais ne fonctionne pas encore comme un hub argumentatif. |
| **Le travail de traduction (Callon)** | Mentionné dans la conclusion comme contribution, mais absent du graphe comme concept ou argument. | La dimension réflexive et dialogique de la thèse (parler *aux* coiners, pas seulement *d'*eux) est invisible. |
| **La question politique ouverte : CM comme boucs émissaires** | Absente du graphe. La conclusion termine sur une question ouverte sur le système monétaire et financier traditionnel, mais aucune entité ne la porte. | Le lecteur du graphe ne perçoit pas que la thèse refuse de clore le débat normatif. |
| **La critique symétrique des essentialismes monétaires** | `NarrativeCluster`: « Critique symétrique des ontologies monétaires substantielles » et `Argument`: « Critique symétrique des essentialismes monétaires » existent, mais ils sont faiblement connectés aux `TheoreticFramework` qu'ils critiquent. | La portée critique de la thèse (refuser *à la fois* le fonctionnalisme et le chartalisme) est présente en germe mais pas rendue visible. |

### Équilibre chapitrale

Le déséquilibre quantitatif v96 (I surreprésenté, II et Conclusion sous-représentés) est **corrigé en v97**. Le problème résiduel n'est pas quantitatif mais relationnel : le chapitre II contient les bons concepts mais ses chaînes démonstratives sont moins denses que les chaînes événementielles du chapitre III.

---

## 2. Proportion et hiérarchie

### Le graphe donne-t-il trop de poids aux crises ?

**Oui et non.**

- **Non au niveau des types d'entités** : les entités de type `CrisisEvent` (55) et `CrisisPhase` (8) ne représentent que 2,8 % des entités et 3,5 % des relations. Quantitativement, les crises ne dominent pas le graphe.
- **Oui au niveau de l'expérience narrative** : la story `crises` (7 étapes) est la plus élaborée après `structure-these` (9 étapes). De plus, la story `fil-de-preuves` (6 étapes) consacre 3 de ses 6 étapes aux crises (fp3, fp4, fp5). Un lecteur qui suit les stories dans l'ordre rencontre donc les crises avant la théorie monétaire complète.
- **Oui au niveau de la granularité événementielle** : le graphe contient ~45 CVE Bitcoin individualisées (de CVE-2010-5137 à CVE-2018-20587), ce qui crée une masse visuelle de « bugs » qui peut donner l'impression que la thèse est une histoire des vulnérabilités Bitcoin, alors qu'elle n'en étudie qu'une (CVE-2018-17144) comme cas principal.

**Risque** : un lecteur qui explore le graphe en mode matrice sans suivre de story peut percevoir Bitcoin comme un système constamment en panne, ce qui n'est pas l'argument de la thèse (qui montre au contraire la *routinisation* de la gestion de crise).

### Le chapitre II est-il assez visible ?

La visibilité **quantitative** est atteinte (23,9 % des relations `appears in section`). La visibilité **narrative** est améliorée par la story `monetisation-cryptos` (7 étapes bien articulées). Mais la visibilité **structurelle** reste faible : les concepts du chapitre II (`Statut monétaire`, `Monétisation`, `Communauté de paiement`, `Nominalisme non étatiste`) ne sont pas les hubs de plus haut degré. Les hubs dominants sont les `ThesisSection`, pas les concepts analytiques.

### La conclusion : clôture ou résultat analytique ?

**Sous-représentée comme résultat analytique.** La conclusion a une forte présence quantitative (21,3 % des `appears in section`), mais elle n'est pas modélisée comme un résultat à cinq composantes. La story `structure-these` lui consacre une seule étape finale (`s9`), qui résume la thèse en une phrase. Les cinq contributions distinctes — infrastructurelle, sociologie des crises, théorie monétaire, traduction, question politique — ne sont pas différenciées dans le graphe.

### Les références et SourceQuote soutiennent-elles ou écrasent-elles l'argument ?

**Les deux.**

- **Soutiennent** : les 245 `SourceQuote` avec attributs de pagination et de section constituent un appareil de preuve robuste, particulièrement fort sur les crises (CVE, DAO) et l'introduction. La story `fil-de-preuves` utilise correctement ces citations comme points d'ancrage.
- **Écrasent** : les 760 `Reference` (33,6 % des entités) et leurs 8 509 relations incidentes (42 % du total) dominent structurellement le graphe. Comme le note l'audit visuel analytique, leur affichage indifférencié transforme une lecture argumentative en index bibliographique. Ce problème est identifié mais non encore résolu au niveau runtime.

---

## 3. Fidélité narrative

### Les stories racontent-elles réellement l'argument de la thèse ?

**En grande partie oui**, avec des réserves.

La story `structure-these` (9 étapes, s1 → s9) est **la plus fidèle à l'architecture démonstrative**. Elle suit la progression : problématisation → construction de l'objet → cadre théorique → chapitre I (Bitcoin) → chapitre I (Ethereum) → chapitre II (charnière) → chapitre II (gouvernance) → chapitre III (crises) → conclusion. C'est un parcours démonstratif, pas un simple sommaire.

La story `monetisation-cryptos` (7 étapes) restitue bien le déplacement : controverse sur le statut → épreuve d'explicitation → reconnaissance des usages → construction de la monétisation → communauté de paiement → institutions et souveraineté → conclusion. C'est fidèle au chapitre II.

La story `qui-gouverne-reellement` (4 étapes) est plus courte et plus rhétorique que démonstrative. Elle déconstruit le mythe du code seul, mais ne montre pas suffisamment la *matérialité* de la gouvernance ordinaire (maintenance, commits, reviews, arènes).

### Lecture trop orientée « crises » ?

**Partiellement.** La story `crises` (7 étapes) est bien construite et inclut une étape comparative (c6) et une étape interprétative (c5), ce qui évite la pure juxtaposition. Mais elle est accessible directement depuis la vue `matrice`, avant qu'un lecteur ait passé par la théorie monétaire et infrastructurelle. Le coverage audit de v96 signalait ce risque (« crisis-first interpretation without passing through infrastructure + monetization theory scaffolding ») ; il n'est pas encore pleinement mitigé.

### La gouvernance discrète, routinière et polycentrique est-elle visible ?

**La gouvernance polycentrique est bien visible** (CoreConcept dédié, story `qui-gouverne-reellement`, présence dans `structure-these` s7).

**La gouvernance discrète et routinière est moins visible.** La thèse insiste sur le fait que la gouvernance de huis clos est *ordinaire, routinière et consensuelle*, pas exceptionnelle. Mais le graphe modélise surtout les crises et leurs dispositifs exceptionnels (responsible disclosure, hard fork, Carbon Vote). La maintenance ordinaire, les reviews de code quotidiennes, la coordination routinière entre Core Devs — le « huis clos » au sens de la pratique banale — sont faiblement représentées.

Le `NarrativeCluster` « Gouvernance de maintenance (huis clos routinier) » existe, mais il n'est pas activé dans les stories comme un argument central. La thèse dit que les crises révèlent la structure ordinaire ; le graphe montre surtout les crises.

---

## 4. Fidélité conceptuelle

### Les concepts centraux sont-ils correctement reliés ?

**Globalement oui**, avec des lacunes ciblées.

Les 8 `CoreConcept` (Gouvernance polycentrique, Gouvernance duale, Développement carnavalesque, Mise en crise/Remise en ordre, Nominalisme monétaire non étatiste, Infrastructure sociotechnique, Gouvernance discrète des CM, Monétisation des CM) forment un noyau conceptuel cohérent et fidèle à la thèse.

Les 14 `TheoreticFramework` couvrent bien les appuis théoriques explicites : IMF, STS, ANT, études infrastructurelles, IAD Framework (Ostrom), théorie de l'acteur-réseau, sociologie de la traduction, chartalisme, free banking, approche instrumentale/substantielle de la monnaie.

**Lacune** : l'IAD Framework et le SES (Social Ecological System) d'Ostrom sont présents comme frameworks, mais le concept de *polycentricité* lui-même n'est pas explicitement relié à Ostrom dans le graphe. La thèse mobilise Ostrom pour caractériser la gouvernance des CM ; ce lien théorique est implicite.

### La distinction gouvernance par le protocole / sur le protocole

**Présente mais non nommée.** Cette distinction — centrale dans la conclusion (« au-delà d'une gouvernance *par* l'infrastructure, la gouvernance *sur* l'infrastructure des CM est conflictuelle et polycentrique ») — n'existe pas comme entité ou comme couple conceptuel explicite dans le graphe. Elle est impliquée par `Space of Rule / Space of Discretion` et par `Gouvernance duale`, mais un lecteur externe ne peut pas la reconstruire sans avoir lu la thèse.

### La thèse institutionnaliste/monétaire est-elle suffisamment présente ?

**Oui au niveau conceptuel** (IMF, nominalisme non étatiste, communauté de paiement, monétisation). **Partiellement au niveau argumentatif** : la thèse affirme que les CM sont des monnaies parce qu'elles sont usées en compte et en paiement, et que leurs UCN sont des créances au porteur sur le protocole. Ces propositions spécifiques — qui constituent la contribution originale à la théorie monétaire — ne sont pas rendues comme des arguments distincts dans le graphe.

### Acteurs, infrastructures et arènes : équilibre ?

| Catégorie | Entités | Jugement |
|---|---|---|
| Personnes | 138 | Bonne couverture (Satoshi, Buterin, Awemany, Dashjr, etc.) |
| Organizations | 25 | Suffisant pour le périmètre |
| GovernanceArena | 13 | Bien représenté (GitHub, mailing lists, forums, All Core Devs, Carbon Vote) |
| StakeholderCategory | 36 | Bonne typologie analytique |
| ActorGroup | 12 | Cohérent |
| ActorNonHuman | 29 | Bonne inclusion STS |
| InfrastructureSegment | 25 | Présent |
| Protocol | 21 | Présent |

L'équilibre acteurs/infrastructures/arènes est satisfaisant et cohérent avec une approche STS de la thèse.

---

## 5. Preuve et confiance

### Zones fortement appuyées par SourceQuote

| Zone | Densité de preuve | Jugement |
|---|---|---|
| Crises (CVE-2018-17144, The DAO) | Élevée : citations de p. 225, 234, 290, 336 | **Forte confiance** |
| Introduction (problématisation, cadre théorique) | Élevée : citations p. 15, 25, 34, 53 | **Forte confiance** |
| Syllogisme libéral-techniciste | Citation p. 53 | **Forte confiance** |
| Gouvernance polycentrique (conclusion) | Citation p. 336 | **Forte confiance** |

### Zones plus inférentielles

| Zone | État des preuves | Risque |
|---|---|---|
| Monétisation comme processus (usage, liquidité, convertibilité) | Concepts présents, citations clairsemées | Le graphe peut donner une impression de solidité théorique là où la thèse s'appuie sur des pratiques empiriques finement décrites |
| Communauté de paiement | Concept présent, peu de citations directes | La centralité analytique du concept n'est pas prouvée par le graphe |
| Développement carnavalesque | Concept présent, citation implicite | La lecture bakhtinienne du développement de Bitcoin n'est pas étayée par citation dans le graphe |
| Maintenance ordinaire | Concept faible, pas de citation | Le « huis clos routinier » est argumenté dans la thèse mais à peine tracé dans le graphe |
| Critique symétrique des essentialismes | Argument présent, non relié aux frameworks critiqués | La portée critique est inférée, pas démontrée |

### Risques de certitude excessive

1. **Les CVE comme faits établis** : les 45 CVE individualisées sont présentées comme des `InfrastructureEvent` ou `CrisisEvent` sans distinction entre celles que la thèse mobilise analytiquement (CVE-2018-17144) et celles qu'elle mentionne pour contextualisation. Un lecteur peut croire que toutes ont le même statut analytique.
2. **Les relations `appears in section` comme preuves d'ancrage** : 12 414 relations de ce type créent une impression de traçabilité exhaustive, mais la résolution par `section_key` ne garantit pas que l'entité est *argumentée* dans cette section — elle peut y être seulement mentionnée.
3. **Les `Argument` comme conclusions stabilisées** : les 7 entités de type `Argument` sont formulées comme des propositions assertives. La thèse, surtout dans sa conclusion, maintient des zones d'incertitude (« Rien ne nous permet de dire que ces infrastructures arriveront à traverser toutes les crises »). Cette nuance probabiliste est absente du graphe.

---

## 6. Expérience lecteur

### Que comprendrait un lecteur externe ?

Un lecteur qui suivrait la story `structure-these` comprendrait **correctement l'architecture démonstrative** de la thèse : problème → cadre → infrastructure → monnaie → gouvernance → crises → synthèse. C'est un succès réel de la couche narrative.

Un lecteur qui explorerait le graphe en mode matrice sans story comprendrait **surtout la masse référentielle et événementielle** : beaucoup de références, beaucoup de CVE, des hubs de section. Il pourrait conclure qu'il s'agit d'une thèse encyclopédique sur les crises Bitcoin, en sous-estimant la portée théorique monétaire et institutionnaliste.

### Malentendus potentiels

| Malentendu possible | Origine dans le graphe |
|---|---|
| « La thèse est une histoire des bugs Bitcoin » | 45 CVE individualisées + prédominance visuelle des crises |
| « La thèse confirme que les CM sont des monnaies » | Le graphe ne montre pas que la thèse *déplace* la question plutôt qu'elle ne la tranche |
| « Les CM n'ont pas de gouvernance » → « elles en ont une, mais le graphe ne dit pas laquelle » | La story `qui-gouverne-reellement` est trop courte (4 étapes) pour montrer la matérialité de la gouvernance |
| « La conclusion est un résumé » | Pas de modélisation des cinq contributions comme arguments distincts |
| « Le statut monétaire est réglé par le protocole » | La distinction gouvernance *par* / *sur* l'infrastructure n'est pas nommée |

### Vues ou stories à renforcer en priorité

1. **Story `qui-gouverne-reellement`** : passer de 4 à 6-7 étapes pour inclure la matérialité de la gouvernance ordinaire (maintenance, commits, arènes de coordination routinière).
2. **Story `monetisation-cryptos`** : ajouter une étape sur la *critique symétrique* des approches instrumentale et chartaliste, pour rendre visible la portée théorique.
3. **Une nouvelle story ou étape de conclusion** qui distingue les cinq contributions, au lieu de les fusionner en une seule étape.

---

## Forces du graphe

1. **Colonne vertébrale conceptuelle fidèle** : les 8 CoreConcepts et 7 Arguments capturent correctement les propositions centrales de la thèse.
2. **Appareil de preuve robuste** : 245 SourceQuotes avec pagination et ancrage sectionnel, particulièrement fort sur les crises et l'introduction.
3. **Story `structure-these` excellente** : suit fidèlement la progression démonstrative de la thèse, avec des étapes articulées et des sourceQuoteIds.
4. **Correction du déséquilibre v96 → v97** : la distribution chapitrale est maintenant équilibrée, ce qui corrige le diagnostic du coverage audit d'avril 2026.
5. **Stories bien résolues** : 167/167 focus nodes résolus en v97 (0 non-résolu, 0 collision), selon l'audit de résolution.
6. **Typologie des crises fidèle** : distinction crise de vulnérabilité / crise d'évolution correctement modélisée.
7. **Cadre théorique complet** : 14 TheoreticFrameworks couvrant les appuis explicites de la thèse.
8. **Équilibre acteurs/non-humains/arènes** : cohérent avec l'approche STS de la thèse.

---

## Faiblesses de représentation

1. **Les cinq contributions de la conclusion ne sont pas différenciées** : le graphe fusionne ce que la thèse présente comme cinq apports distincts.
2. **La distinction gouvernance par / sur l'infrastructure n'est pas nommée** : elle est impliquée mais pas explicitée comme axe conceptuel.
3. **La gouvernance ordinaire et routinière est sous-modélisée** : le graphe montre les crises, pas la maintenance de tous les jours.
4. **Le travail de traduction (Callon) est absent** : la dimension réflexive et dialogique de la thèse est invisible.
5. **La question politique ouverte (boucs émissaires) est absente** : le lecteur ne perçoit pas le refus délibéré de clore le débat normatif.
6. **La critique symétrique des essentialismes est faible** : l'argument existe mais n'est pas relié aux frameworks qu'il critique.
7. **Les CVE sont sur-individualisées** : 45 entités pour un seul cas analytique crée du bruit visuel.

---

## Zones surreprésentées

| Zone | Degré de surreprésentation | Impact |
|---|---|---|
| `Reference` (760 entités, 42 % des relations) | Forte | Écrase la lecture argumentative sous la masse bibliographique |
| CVE Bitcoin individualisées (~45) | Modérée | Suggère une vocation encyclopédique des bugs |
| Relations `appears in section` (12 414) | Structurellement massive | Crée une illusion de traçabilité exhaustive sans garantie d'ancrage argumentatif |
| Hubs de ThesisSection (degré 400-611) | Forte | Les sections textuelles dominent visuellement les concepts analytiques |

---

## Zones sous-représentées

| Zone | Degré de sous-représentation | Impact |
|---|---|---|
| Gouvernance ordinaire / maintenance routinière | Forte | La thèse insiste sur le caractère *banal* du huis clos ; le graphe ne montre que les crises |
| Cinq contributions distinctes de la conclusion | Forte | La portée pluraliste de la thèse est effacée |
| Travail de traduction (Callon, reflexivity) | Totale | Dimension majeure de la thèse absente |
| Question politique ouverte (boucs émissaires, système monétaire) | Totale | Le positionnement citoyen de la thèse est invisible |
| Distinction gouvernance par / sur l'infrastructure | Forte | Concept central non nommé |
| Polycentricité ostromienne | Modérée | Le lien à Ostrom est implicite |
| Critique symétrique reliée aux frameworks | Modérée | L'argument existe en isolation |

---

## Risques de déformation

1. **Réduction technologiste** : un lecteur peut conclure que la thèse est principalement une étude technique des crises Bitcoin, sous-estimant sa portée théorique monétaire et institutionnaliste.
2. **Téléologie de la crise** : la richesse de la modélisation des crises peut donner l'impression que la thèse *valorise* les crises comme spectacle, alors qu'elle les utilise comme méthode d'accès heuristique à la gouvernance ordinaire.
3. **Faux consensus** : les `Argument` assertifs et l'absence de marquage d'incertitude peuvent donner une impression de closure théorique que la thèse, surtout en conclusion, refuse explicitement.
4. **Bibliographie comme argument** : la masse référentielle peut être lue comme la preuve elle-même, plutôt que comme le support d'une démonstration qui se joue ailleurs (dans le raisonnement institutionnaliste et infrastructurel).

---

## Current agentic workflow observed

Le projet dispose actuellement de deux agents actifs (Hermes en orchestrateur de Mode A/B/C, Codex en exécuteur de Mode C), encadrés par une charte (`agents/README.md`) qui formalise quatre règles (pas d'agent sans douleur observée ; proposition ≠ application ; une sortie d'agent reste une donnée tant qu'elle n'est pas validée ; généalogie obligatoire). Sept candidats sont différés (Evidence, Schema, Aeon, Story, Visual, Ontology, Publisher).

Le présent audit est produit en **Mode A** : lecture seule, rapport Markdown, aucune modification du graphe ou du runtime. Il s'inscrit dans la discipline de la maintenance traceable : l'audit est une donnée annotée, pas un fait établi, jusqu'à validation par Maël Rolland.

---

## Recommandations

### A. Corrections documentaires

| # | Recommandation | Priorité | Effort |
|---|---|---|---|
| A1 | Documenter dans un guide lecteur que le graphe doit idéalement être parcouru via les stories (ordre suggéré : `structure-these` → `monetisation-cryptos` → `qui-gouverne-reellement` → `crises` → `fil-de-preuves`), pas en mode matrice libre. | Haute | Faible |
| A2 | Ajouter une note méthodologique distinguant les CVE mobilisées analytiquement (CVE-2018-17144) de celles qui servent de contexte historique. | Moyenne | Faible |
| A3 | Documenter le passage v96 → v97 (rééquilibrage chapitrale) dans un changelog visible. | Moyenne | Faible |
| A4 | Créer un glossaire graphe-lecteur qui traduit les noms d'entités techniques (UCN, PoW, BIP, hard fork) en concepts analytiques de la thèse. | Basse | Moyen |

### B. Corrections du graphe

| # | Recommandation | Priorité | Risque |
|---|---|---|---|
| B1 | Créer 5 entités `Argument` distinctes pour les cinq contributions de la conclusion, reliées au `Chapter` Conclusion et au `CoreConcept` correspondant. | Haute | Modéré (interprétation) |
| B2 | Créer une entité conceptuelle explicite « Gouvernance par l'infrastructure vs gouvernance sur l'infrastructure » (ou un couple d'entités reliées), reliée à `Space of Rule / Space of Discretion` et à `Gouvernance polycentrique`. | Haute | Faible |
| B3 | Créer une entité `Concept` ou `Argument` pour le « Travail de traduction » (Callon), reliée à la conclusion et à `Theorie de l'acteur-reseau (ANT)`. | Moyenne | Faible |
| B4 | Créer une entité pour la « Question des boucs émissaires » ouverte en conclusion, typée comme `Argument` ou `AnalyticClaim`, marquée comme question ouverte (non résolue). | Moyenne | Faible |
| B5 | Renforcer les relations entre `Critique symétrique des essentialismes monétaires` et les `TheoreticFramework` qu'elle critique (approche instrumentale, chartalisme). | Moyenne | Faible |
| B6 | Ajouter des entités et relations pour la gouvernance ordinaire : review de code, coordination entre Core Devs, processus de publication, maintien quotidien. | Moyenne | Modéré (matériel empirique) |
| B7 | Réduire le bruit des CVE non mobilisées analytiquement : les grouper sous un `InfrastructureEvent` parent « Crises historiques de Bitcoin (panorama) » plutôt que de les individualiser au même niveau que CVE-2018-17144. | Basse | Modéré (restructuration) |

### C. Corrections narratives

| # | Recommandation | Priorité | Effort |
|---|---|---|---|
| C1 | Étendre la story `qui-gouverne-reellement` de 4 à 6-7 étapes, en ajoutant : (a) la matérialité de la gouvernance ordinaire (maintenance, arènes quotidiennes), (b) la distinction par/sur l'infrastructure, (c) un point final sur la polycentricité comme résultat, pas comme prémisse. | Haute | Moyen |
| C2 | Ajouter une étape à `monetisation-cryptos` sur la critique symétrique des approches instrumentale et chartaliste, pour rendre visible la portée théorique du chapitre II. | Moyenne | Faible |
| C3 | Remplacer l'étape finale unique de `structure-these` (s9) par 2 étapes : (a) les cinq contributions, (b) la question ouverte. | Moyenne | Faible |
| C4 | Ajouter une story ou une étape sur le travail de traduction et la dimension réflexive (Callon, dialogue avec les coiners). | Basse | Moyen |
| C5 | Documenter dans les intros de story que les crises sont une *méthode d'accès*, pas le *sujet* de la thèse. | Haute | Faible |

### D. Corrections visuelles

| # | Recommandation | Priorité | Test requis |
|---|---|---|---|
| D1 | Implémenter un layer « preuve » (`Reference` + `SourceQuote`) désactivé par défaut dans les vues macro, activable depuis le panneau détail. | Haute | Test de traçabilité citation → claim |
| D2 | Utiliser des bandes/zones pour les chapitres et sections dans la vue matrice, plutôt que des hubs de même poids que les concepts. | Moyenne | Prototype |
| D3 | Ajouter un compteur « relations affichées / masquées » dans les états Focus/Story pour éviter l'impression d'absence de preuve. | Moyenne | Validation runtime |
| D4 | Marquer visuellement les CVE mobilisées analytiquement (CVE-2018-17144, The DAO) par opposition aux CVE contextuelles. | Basse | Test de lisibilité |

### E. Questions scientifiques à arbitrer par Maël

| # | Question | Enjeu |
|---|---|---|
| E1 | Les cinq contributions de la conclusion doivent-elles être modélisées comme 5 `Argument` distincts, ou comme 5 facettes d'un seul argument synthétique ? | Détermine la granularité argumentative du graphe |
| E2 | La distinction gouvernance *par* / *sur* l'infrastructure doit-elle devenir un `CoreConcept` à part entière, ou rester implicite dans `Space of Rule / Space of Discretion` ? | Détermine la lisibilité du concept le plus décisif de la thèse |
| E3 | Le travail de traduction (Callon) mérite-t-il une entité dédiée, ou doit-il rester une note de positionnement épistémologique ? | Détermine la visibilité de la dimension réflexive |
| E4 | La question politique ouverte (boucs émissaires) doit-elle entrer dans le graphe comme question non résolue, ou rester hors du périmètre de représentation ? | Détermine si le graphe représente seulement les résultats ou aussi les limites assumées |
| E5 | Faut-il réduire le nombre de CVE individualisées au profit d'un panorama agrégé, ou conserver la granularité actuelle comme matériau brute ? | Détermine le rapport entre exhaustivité empirique et lisibilité analytique |
| E6 | La gouvernance ordinaire (maintenance, coordination routinière) est-elle suffisamment documentée dans le matériau empirique pour être modélisée, ou le graphe reproduit-il légitimement le fait que la thèse y accède *via* les crises ? | Détermine la frontière entre sous-représentation et fidélité au terrain |
| E7 | Le lien entre polycentricité et Ostrom (IAD/SES) doit-il être explicité dans le graphe, ou est-ce un rapprochement théorique qui reste à la charge du texte ? | Détermine le degré d'explicitation théorique du graphe |

---

## Non-actions de cette mission

- Aucune modification du JSON (`grc20-these-mael-rolland-v97.json`).
- Aucune création de nouvelle version du graphe.
- Aucune modification de `graphe.html`, `story-presets.mjs`, `narrative-anchors.json`.
- Aucune modification de scripts ou de déploiement.
- Aucun merge.

## Sources lues

- `grc20-these-mael-rolland-v97.json` (analyse programmatique complète)
- `assets/MD/00_introduction.md`, `04_conclusion.md` (arguments centraux)
- `story-presets.mjs` (5 stories, 38 étapes)
- `narrative-anchors.json` (référencé, non modifié)
- `docs/grc20_narrative_matrix.md`
- `docs/grc20_coverage_fidelity_audit_2026-04-01.md` (v96, pour comparaison v97)
- `docs/grc20_evidence_audit.md`
- `docs/grc20_ontology_audit.md`
- `docs/grc20_views_audit.md`
- `docs/audits/grc20-story-focus-resolution-audit.md`
- `docs/audits/grc20-visual-analytical-design-audit.md`
- `docs/audits/grc20-audit-batch-001-summary.md`
- `agents/README.md`, `agents/Agent_Creation_Rules.md`
