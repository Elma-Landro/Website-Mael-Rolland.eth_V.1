# GRC-20 v98 Representation Patch Specification

**Date** : 2026-06-28  
**Branche** : `agent/grc20-v98-representation-spec`  
**Mode agent** : A → B (spécification de patch, aucune application)  
**Graph source** : `grc20-these-mael-rolland-v97.json`  
**Décisions de base** : arbitrages E1–E7 de Maël Rolland (tous option B, avec nuances)

## Objet

Transformer les arbitrages scientifiques E1–E7 en une spécification de patch précise, exploitable pour une future implémentation en v98. **Aucun patch n'est appliqué dans cette mission.** Chaque modification proposée désigne les entités, types et relation_types existants à utiliser.

## Décisions intégrées

| Q | Décision | Nuance |
|---|---|---|
| E1 | Option B | Expliciter les cinq contributions de la conclusion sans refonte globale |
| E2 | Option B renforcé | Créer/renforcer un concept central autour de la distinction gouvernance par / sur l'infrastructure |
| E3 | Option B | Représenter la traduction (Callon) par une entité ou un lien ciblé |
| E4 | Option B prudent | Question des boucs émissaires comme `open_question` si le schéma le permet |
| E5 | Option B | Annoter le rôle analytique de CVE-2018 comme révélateur de gouvernance discrète |
| E6 | Option B conditionnel | Renforcer la gouvernance ordinaire seulement si appui explicite dans la thèse |
| E7 | Option B | Relation prudente à Ostrom, sans en faire une clé totalisante |

---

## E1 — Cinq contributions de la conclusion

### Problème

Le graphe contient 1 `Argument` synthétique « Thèse centrale (infrastructures, crises, gouvernance polycentrique) » (`a4bbdf3c6539`). La conclusion de la thèse présente explicitement cinq contributions distinctes (5 sous-sections titrées). Aucune n'est modélisée comme argument séparé.

### Entités existantes concernées

| Entité | ID (préfixe) | Type | Rôle |
|---|---|---|---|
| Thèse centrale (infrastructures, crises, gouvernance polycentrique) | `a4bbdf3c6539` | `Argument` | Argument synthétique à conserver |
| Conclusion générale | `6b64e2683643` | `Chapter` | Cible des nouvelles relations |
| Conclusion — Résumé de la thèse | `9c72c7227c3e` | `ThesisSection` | Section où les contributions sont énoncées |
| Infrastructure sociotechnique | `e1a7b0683940` | `CoreConcept` | Concept pivot de la contribution 1 |
| Mise en crise / Remise en ordre | `586e00d1ca15` | `CoreConcept` | Concept pivot de la contribution 2 |
| Nominalisme monetaire non etatiste | `c4ff6f8bb34a` | `CoreConcept` | Concept pivot de la contribution 3 |
| Effort de traduction chercheur | `e277c6d62d8a` | `Concept` | Concept pivot de la contribution 4 (existe déjà) |
| Paradoxe des CM comme bouc emissaire | `ae7be15c2dd7` | `Concept` | Concept pivot de la contribution 5 (existe déjà) |

### Types existants utilisables

- `Argument` (type déjà utilisé pour 7 entités)
- `AnalyticClaim` (type existant, utilisé 1 fois)

### Relation_types existants utilisables

- `contributes to` (déjà utilisé : `Effort de traduction chercheur` → `Conclusion générale`)
- `supports` / `supports concept`
- `sub argument of` (existe dans le schéma)
- `central thesis`

### Modifications proposées

Créer 5 entités `Argument`, une par contribution. Toutes reliées à l'`Argument` synthétique existant par `sub argument of`, et au `Chapter` Conclusion par `contributes to`.

| # | Action | Cible exacte | Justification (thèse) | Type | Relation vers synthétique | Relation vers Chapter | Confiance | Validation |
|---|---|---|---|---|---|---|---|---|
| E1.1 | **Créer** | Argument — Approche infrastructurelle des CM | Conclusion, sous-section « Décrypter la Crypto par l'approche infrastructurelle » | `Argument` | `sub argument of` → `a4bbdf3c6539` | `contributes to` → `6b64e2683643` | Élevée | Libellé à valider |
| E1.2 | **Créer** | Argument — Sociologie des crises et acéphalisme | Conclusion, sous-section « De l'acéphalisme apolitique des CM à l'épreuve d'une sociologie des crises » | `Argument` | `sub argument of` → `a4bbdf3c6539` | `contributes to` → `6b64e2683643` | Élevée | Libellé à valider |
| E1.3 | **Créer** | Argument — Intégration des CM dans la théorie monétaire | Conclusion, sous-section « Une intégration cohérente des CM dans le champ de la théorie monétaire » | `Argument` | `sub argument of` → `a4bbdf3c6539` | `contributes to` → `6b64e2683643` | Élevée | Libellé à valider |
| E1.4 | **Créer** | Argument — Effort de traduction entre coiners et professionnels de l'argent | Conclusion, sous-section « Un effort de traduction attentif aux et à l'attention des acteurs » | `Argument` | `sub argument of` → `a4bbdf3c6539` | `contributes to` → `6b64e2683643` | Élevée | Libellé à valider |
| E1.5 | **Créer** | Argument — CM comme boucs émissaires d'un système monétaire en crise | Conclusion, sous-section « Les CM : boucs émissaires commodes d'un système monétaire en crise ? » | `Argument` | `sub argument of` → `a4bbdf3c6539` | `contributes to` → `6b64e2683643` | Élevée | Voir E4 pour le statut `open_question` |

### Relations supplémentaires vers les concepts pivots

| # | Action | From → To | Relation_type |
|---|---|---|---|
| E1.1a | **Relier** | E1.1 → `e1a7b0683940` (Infrastructure sociotechnique) | `demonstrates` |
| E1.2a | **Relier** | E1.2 → `586e00d1ca15` (Mise en crise / Remise en ordre) | `demonstrates` |
| E1.3a | **Relier** | E1.3 → `c4ff6f8bb34a` (Nominalisme non étatiste) | `demonstrates` |
| E1.4a | **Relier** | E1.4 → `e277c6d62d8a` (Effort de traduction chercheur) | `demonstrates` |
| E1.5a | **Relier** | E1.5 → `ae7be15c2dd7` (Paradoxe des CM comme bouc emissaire) | `demonstrates` |

### Risques de surinterprétation

- **Faible**. Les cinq contributions sont explicitement titrées dans la conclusion. Les libellés doivent rester fidèles aux titres de sous-sections, pas être reformulés.
- L'argument synthétique existant est conservé : pas de perte.

### Alternative plus prudente

Créer seulement 3 Arguments sur 5 (infrastructurelle, monétaire, crises) et laisser traduction et boucs émissaires comme Concepts sans promotion au rang d'Argument.

---

## E2 — Gouvernance par / sur l'infrastructure

### Problème

La distinction la plus décisive de la thèse — gouvernance *par* l'infrastructure (règles protocolaires exécutoires) vs *sur* l'infrastructure (acteurs humains qui modifient ou contournent) — n'existe pas comme entité nommée. Elle est impliquée par `Space of Rule / Space of Discretion` mais pas explicitée.

### Entités existantes concernées

| Entité | ID (préfixe) | Type |
|---|---|---|
| Space of Rule / Space of Discretion | `fba623af0764` | `Concept` |
| Gouvernance polycentrique | `a444085b9b2d` | `CoreConcept` |
| Gouvernance duale | `a432cc76f9ea` | `CoreConcept` |
| Infrastructure sociotechnique | `e1a7b0683940` | `CoreConcept` |
| Gouvernance discrète des cryptomonnaies | `538e905c19fc` | `CoreConcept` |
| Conclusion générale | `6b64e2683643` | `Chapter` |

### Types existants utilisables

- `CoreConcept` (8 existants)
- `Concept` (391 existants)

### Relation_types existants utilisables

- `in tension with`
- `governance`
- `demonstrates`
- `applied to`

### Modifications proposées

**Option B renforcé** : créer un couple de `CoreConcept` reliés par `in tension with`.

| # | Action | Cible exacte | Justification (thèse) | Type | Confiance | Validation |
|---|---|---|---|---|---|---|
| E2.1 | **Créer** | Gouvernance par l'infrastructure (régulation protocolaire exécutoire) | Conclusion p. 336 : « gouvernance *par* l'infrastructure » | `CoreConcept` | Élevée | Libellé à valider |
| E2.2 | **Créer** | Gouvernance sur l'infrastructure (médiation socio-politique sur le code) | Conclusion p. 336 : « gouvernance *sur* l'infrastructure [...] conflictuelle et polycentrique » | `CoreConcept` | Élevée | Libellé à valider |

### Relations

| # | Action | From → To | Relation_type | Justification |
|---|---|---|---|---|
| E2.3 | **Relier** | E2.1 → E2.2 | `in tension with` | La thèse montre la tension dynamique entre les deux |
| E2.4 | **Relier** | E2.2 → `a444085b9b2d` (Gouvernance polycentrique) | `demonstrates` | La gouvernance *sur* l'infrastructure *démontre* la polycentricité |
| E2.5 | **Relier** | E2.1 → `fba623af0764` (Space of Rule / Discretion) | `applied to` | La distinction par/sur est l'application infrastructurelle de la tension règle/discrétion |
| E2.6 | **Relier** | E2.2 → `6b64e2683643` (Conclusion générale) | `appears in section` | Ancrage textuel |

### Risques de surinterprétation

- **Faible**. Citation explicite p. 336.
- La distinction par/sur ne doit pas être confondue avec règle/discrétion : par/sur est au niveau infrastructurel, règle/discrétion au niveau monétaire/gouvernemental. Les relations doivent préserver cette distinction.

### Alternative plus prudente

Créer une seule entité `CoreConcept` « Gouvernance par/sur l'infrastructure » (concept dual) au lieu d'un couple tensionnel.

---

## E3 — Travail de traduction (Callon)

### Problème

Le travail de traduction est identifié comme contribution dans la conclusion, mais sa visibilité dans le graphe est faible. Or, l'entité existe déjà.

### Entités existantes concernées

| Entité | ID (préfixe) | Type | État |
|---|---|---|---|
| **Effort de traduction chercheur** | `e277c6d62d8a` | `Concept` | **Existe déjà** — relié à Conclusion et Callon 1986 |
| Sociologie de la traduction | `83f9ceb540d0` | `TheoreticFramework` | Framework source |
| Callon 1986 Traduction | `64d68c318565` | `Reference` | Référence primaire |
| Michel Callon | `b685ac7b6c29` | `Person` | Auteur |
| C. Le travail de traduction : prolongements | `11fe6aacd1c4` | `ThesisSection` | Section conclusion (annexe C) |
| Conclusion générale | `6b64e2683643` | `Chapter` | — |

### Relations existantes vers `Effort de traduction chercheur`

- `has concept` ← `Au-dela des codes`
- `source of` → `Callon 1986 Traduction`
- `supports concept` ← `Conclusion générale`
- `contributes to` → `Conclusion générale`
- `evidenced by` → `Entretien n°24`
- `appears in section` → `C. Une démarche ethnographique...`

### Types et relation_types utilisables

- Type : `Concept` (existant) — pas de changement de type nécessaire.
- `uses method` (relation_type existant)
- `mobilizes` (relation_type existant)

### Modifications proposées

L'entité existe et est déjà bien reliée. La correction est **minimale** :

| # | Action | Cible exacte | Justification | Confiance | Validation |
|---|---|---|---|---|---|
| E3.1 | **Relier** | `e277c6d62d8a` → `83f9ceb540d0` (Sociologie de la traduction) | `uses method` ou `mobilizes` | Actuellement relié seulement à la Reference, pas au Framework | Élevée | Non requise |
| E3.2 | **Relier** | `e277c6d62d8a` → `11fe6aacd1c4` (Section annexe C) | `appears in section` | La section conclu_traduction est l'ancrage textuel principal | Élevée | Non requise |

### Risques de surinterprétation

- **Très faible**. L'entité existe, les relations sont des compléments d'ancrage.

### Alternative plus prudente

Ne rien changer. L'entité est déjà suffisamment reliée. La promotion en `Argument` (E1.4) donnera sa visibilité.

---

## E4 — Question des boucs émissaires

### Problème

La question politique ouverte en conclusion (boucs émissaires) doit être représentée comme question non résolue. Or, l'entité existe déjà.

### Entités existantes concernées

| Entité | ID (préfixe) | Type | État |
|---|---|---|---|
| **Paradoxe des CM comme bouc emissaire** | `ae7be15c2dd7` | `Concept` | **Existe déjà** |
| Conclusion — Les CM : boucs émissaires... | `d9f534f9f849` | `ThesisSection` | **Existe déjà** |
| Souverainete monetaire | `f018e4490ac2` | `Concept` | Concept adjacent |
| Shadow Banking | `75cf13aa0a3e` | `Concept` | Concept adjacent |

### Types et relation_types utilisables

- Type : `Concept` (existant) ou `AnalyticClaim` (existant, 1 occurrence).
- Attribut : `evidenceStatus` (déjà utilisé sur `11fe6aacd1c4` avec valeur `thesis section`).

### Modifications proposées

| # | Action | Cible exacte | Justification | Confiance | Validation |
|---|---|---|---|---|---|
| E4.1 | **Annoter** | `ae7be15c2dd7` | Ajouter attribut `evidenceStatus: open_question` | Marquer le caractère non résolu sans modifier le schéma | Élevée | Requise : valider le nom d'attribut |
| E4.2 | **Relier** | `ae7be15c2dd7` → `d9f534f9f849` (ThesisSection boucs émissaires) | `appears in section` | Ancrage textuel | Élevée | Non requise |
| E4.3 | **Relier** | `ae7be15c2dd7` → `f018e4490ac2` (Souveraineté monétaire) | `in tension with` | La question oppose la souveraineté bancaire à la souveraineté crypto | Élevée | Non requise |
| E4.4 | **Relier** | `ae7be15c2dd7` → `75cf13aa0a3e` (Shadow Banking) | `affects` | Le bouc émissaire masque le vrai shadow banking | Élevée | Non requise |

### Risques de surinterprétation

- **Modéré**. L'attribut `evidenceStatus: open_question` est crucial. Sans lui, l'entité est lue comme un argument assertif, ce qui contredit l'intention de la thèse.
- Si l'attribut `evidenceStatus` ne peut pas être ajouté (contrainte de schéma GRC-20), alternative : préfixer le nom de l'entité par « Question ouverte — » ou « [Ouvert] ».

### Alternative plus prudente

Ne pas créer d'`Argument` E1.5 pour les boucs émissaires. Garder seulement le `Concept` existant annoté `open_question`, sans le promouvoir au rang d'Argument. Cela évite de donner à une question ouverte le même statut assertif que les autres contributions.

---

## E5 — CVE-2018-17144 : annoter le rôle analytique

### Problème

CVE-2018-17144 est la crise la plus densément modélisée du graphe (CrisisEvent + 4 CrisisPhase + ~15 SourceQuotes + GovernanceProcess + ~15 References). Mais son rôle analytique — révélateur de gouvernance discrète et routinière — n'est pas annoté explicitement.

### Entités existantes concernées

| Entité | ID (préfixe) | Type |
|---|---|---|
| Bitcoin CVE 2018-17144 | `db9a125c4c7a` | `CrisisEvent` |
| CVE-2018-17144 — Signalement et divulgation responsable | `9c3c6d955246` | `CrisisPhase` |
| CVE-2018-17144 — Évaluation en huis clos | `143db183ec75` | `CrisisPhase` |
| CVE-2018-17144 — Remise en ordre par patch | `73712fc1060c` | `CrisisPhase` |
| CVE-2018-17144 — Révélation publique et consensus ex post | `896a139f0488` | `CrisisPhase` |
| GovernanceProcess — CVE-2018-17144 résolution | `44e842cde307` | `GovernanceProcess` |
| Gouvernance de huis clos | `a22f20aea49d` | `Concept` |
| Gouvernance de maintenance (huis clos routinier) | `82b2387dbb64` | `NarrativeCluster` |

### Modifications proposées

| # | Action | Cible exacte | Justification | Confiance | Validation |
|---|---|---|---|---|---|
| E5.1 | **Annoter** | `db9a125c4c7a` (CrisisEvent CVE-2018-17144) | Ajouter attribut `analyticRole: primary_case` | Distinguer le cas analytique principal des CVE contextuelles | Élevée | Non requise |
| E5.2 | **Relier** | `db9a125c4c7a` → `a22f20aea49d` (Gouvernance de huis clos) | `demonstrates` | La crise démontre la gouvernance de huis clos | Élevée | Non requise |
| E5.3 | **Relier** | `db9a125c4c7a` → `82b2387dbb64` (NarrativeCluster huis clos routinier) | `revealedBy` | La crise révèle la structure de gouvernance ordinaire | Élevée | Non requise |

### Risques de surinterprétation

- **Très faible**. Les relations existent conceptuellement, elles ne font que devenir explicites.

### Alternative plus prudente

Seulement E5.2 (relation vers Gouvernance de huis clos), sans attribut ni relation vers NarrativeCluster.

---

## E6 — Gouvernance ordinaire (conditionnel)

### Problème

La thèse insiste sur le caractère *ordinaire et routinière* de la gouvernance de huis clos, mais le graphe modélise surtout les dispositifs de crise. La condition posée par Maël : renforcer seulement si les passages de thèse fournissent un appui explicite.

### Entités existantes concernées

| Entité | ID (préfixe) | Type |
|---|---|---|
| Gouvernance de huis clos | `a22f20aea49d` | `Concept` |
| Gouvernance de maintenance (huis clos routinier) | `82b2387dbb64` | `NarrativeCluster` |
| Core Developers (Bitcoin) | `7b29b0d2d840` | `StakeholderGroup` |
| Core Developers (Ethereum) | `c5f0d6a94454` | `StakeholderGroup` |
| Pull Request (PR) | `9e9eac4d98ca` | `Concept` |
| GitHub Bitcoin Core | `344699b95930` | `GovernanceArena` |
| III.2 Des marques d'une politique de crises | `89663a261c15` | `ThesisSection` |
| III.2.3 — Des acteurs au cœur de la gouvernance sur le protocole | `da7e8dda9cac` | `ThesisSection` |

### Appui textuel identifié

La thèse décrit explicitement (chap. III, section III.2.3) le rôle des mainteneurs Core, le processus de merge, et la coordination quotidienne. La section `III.2.3 — Des acteurs au cœur de la gouvernance sur le protocole` existe déjà dans le graphe.

**Condition remplie** : les passages de thèse fournissent un appui explicite.

### Modifications proposées (conditionnel)

| # | Action | Cible exacte | Justification | Type | Confiance | Validation |
|---|---|---|---|---|---|---|
| E6.1 | **Relier** | `82b2387dbb64` (NarrativeCluster) → `7b29b0d2d840` (Core Devs Bitcoin) | `mentions actor` | Le huis clos routinier implique les Core Devs | Élevée | Non requise |
| E6.2 | **Relier** | `82b2387dbb64` → `344699b95930` (GitHub Bitcoin Core) | `occurs in` | La maintenance se déroule sur GitHub | Élevée | Non requise |
| E6.3 | **Relier** | `82b2387dbb64` → `9e9eac4d98ca` (Pull Request) | `uses method` ou `has governance process` | La PR est l'unité de travail de la gouvernance ordinaire | Élevée | Non requise |
| E6.4 | **Relier** | `82b2387dbb64` → `89663a261c15` (section III.2) | `appears in section` | Ancrage textuel | Élevée | Non requise |

### Risques de surinterprétation

- **Faible**. Ces relations explicitent des liens déjà impliqués par la structure narrative de la thèse.

### Alternative plus prudente

Seulement E6.1 et E6.4 (acteurs + ancrage sectionnel), sans créer de nouveaux concepts pour les routines.

---

## E7 — Polycentricité et Ostrom

### Problème

Le concept de polycentricité est explicitement ostromien, mais le graphe ne relie pas `Gouvernance polycentrique` au cadre IAD/SES d'Ostrom.

### Entités existantes concernées

| Entité | ID (préfixe) | Type |
|---|---|---|
| Gouvernance polycentrique | `a444085b9b2d` | `CoreConcept` |
| Cadre IAD / SES (Ostrom) | `92b63798d91b` | `Concept` |
| IAD Framework | `65e028093291` | `TheoreticFramework` |
| Social Ecological System (SES) | `b65112a317f0` | `TheoreticFramework` |
| Elinor Ostrom | `2b513be78d20` | `Person` |
| Polycentricité comme dynamique d'arènes | `4a0561746724` | `Argument` |

### Relation_types utilisables

- `derivedFromConcept` (existe dans le schéma)
- `inspired by` (existe)
- `applied to` (existe)

### Modifications proposées

| # | Action | From → To | Relation_type | Justification | Confiance | Validation |
|---|---|---|---|---|---|---|
| E7.1 | **Relier** | `a444085b9b2d` (Gouv. polycentrique) → `92b63798d91b` (Cadre IAD/SES) | `derivedFromConcept` | La polycentricité de la thèse dérive du cadre ostromien | Élevée | Libellé de relation à valider |
| E7.2 | **Relier** | `92b63798d91b` → `65e028093291` (IAD Framework) | `applied to` ou `mobilizes` | Le cadre IAD/SES mobilise l'IAD Framework | Élevée | Non requise |

### Risques de surinterprétation

- **Faible**. Le lien est bien établi dans la littérature et attesté dans la thèse.
- La relation `derivedFromConcept` ne doit pas suggérer une transposition directe : la thèse *adapte* la polycentricité à des objets (infrastructures numériques) qu'Ostrom n'a pas traités. Une formulation `inspired by` serait plus prudente si `derivedFromConcept` semble trop forte.

### Alternative plus prudente

Seulement E7.1 avec `inspired by` au lieu de `derivedFromConcept`, sans E7.2.

---

## Synthèse du patch v98

### Nouvelles entités

| # | Nom proposé | Type | Décision |
|---|---|---|---|
| E1.1 | Argument — Approche infrastructurelle des CM | `Argument` | E1 |
| E1.2 | Argument — Sociologie des crises et acéphalisme | `Argument` | E1 |
| E1.3 | Argument — Intégration des CM dans la théorie monétaire | `Argument` | E1 |
| E1.4 | Argument — Effort de traduction entre acteurs | `Argument` | E1 |
| E1.5 | Argument — CM comme boucs émissaires | `Argument` | E1 (+ E4) |
| E2.1 | Gouvernance par l'infrastructure | `CoreConcept` | E2 |
| E2.2 | Gouvernance sur l'infrastructure | `CoreConcept` | E2 |

**Total : 7 nouvelles entités** (5 Arguments + 2 CoreConcepts)

### Annotations d'entités existantes

| # | Entité | Attribut | Décision |
|---|---|---|---|
| E4.1 | `ae7be15c2dd7` (Paradoxe des CM comme bouc emissaire) | `evidenceStatus: open_question` | E4 |
| E5.1 | `db9a125c4c7a` (Bitcoin CVE 2018-17144) | `analyticRole: primary_case` | E5 |

### Nouvelles relations

| Catégorie | Count | Détail |
|---|---|---|
| E1 (sous-arguments → synthétique + Chapter + concepts) | ~15 | 5 × 3 |
| E2 (par/sur → tension + polycentricité + space of rule + conclusion) | ~4 | |
| E3 (traduction → framework + section) | ~2 | |
| E4 (boucs → section + souveraineté + shadow banking) | ~3 | |
| E5 (CVE → huis clos + narrative cluster) | ~2 | |
| E6 (maintenance → core devs + github + PR + section) | ~4 | |
| E7 (polycentricité → IAD/SES + IAD Framework) | ~2 | |
| **Total** | **~32** | |

### Récapitulatif

| Métrique | Valeur |
|---|---|
| Nouvelles entités | 7 |
| Entités existantes annotées | 2 |
| Nouvelles relations | ~32 |
| Types nouveaux nécessaires | 0 (tous existants) |
| Relation_types nouveaux nécessaires | 0 (tous existants) |
| Modifications de schéma | 0 (sauf si `evidenceStatus: open_question` nécessite validation) |

---

## Décisions scientifiques encore requises

| # | Question | Statut |
|---|---|---|
| D1 | Libellés exacts des 5 nouveaux Arguments E1 | À valider par Maël |
| D2 | Libellés exacts des 2 nouveaux CoreConcepts E2 | À valider par Maël |
| D3 | Attribut `evidenceStatus: open_question` : est-il compatible avec le schéma GRC-20 actuel ? | À vérifier techniquement |
| D4 | E4 alternative : promouvoir le concept « bouc émissaire » en Argument (E1.5) ou le laisser en Concept annoté ? | À décider |
| D5 | E7 : `derivedFromConcept` (dérivation) ou `inspired by` (inspiration) ? | À décider |
| D6 | E6 : créer de nouvelles entités pour les routines de maintenance, ou seulement relier le NarrativeCluster existant ? | À décider (recommandation : seulement relier) |

---

## Non-actions de cette mission

- Aucune modification du JSON (`grc20-these-mael-rolland-v97.json`).
- Aucune création de v98.
- Aucune modification de `graphe.html`, `story-presets.mjs`, `narrative-anchors.json`.
- Aucune modification de scripts ou de déploiement.
- Aucun patch appliqué.
- Aucun merge.

## Sources lues

- `grc20-these-mael-rolland-v97.json` (analyse programmatique exhaustive)
- `docs/audits/grc20-representation-audit-v1.md` (PR #94)
- `docs/audits/grc20-representation-arbitration-memo.md` (PR #95)
- Décisions E1–E7 communiquées par Maël Rolland
