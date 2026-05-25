# Audit documentaire initial du dépôt GRC-20

Date : 2026-05-25  
Mission : 002 — Audit documentaire initial du dépôt GRC-20  
Mode : documentation uniquement, sans correction

## 1. Dépôt et branches

Dépôt audité :

```text
/workspace/Website-Mael-Rolland.eth_V.1
```

Remote GitHub :

```text
https://github.com/Elma-Landro/Website-Mael-Rolland.eth_V.1.git
```

Branche locale observée au début de la Mission 002 :

```text
codex/reapply-story-expand-shadow-default
```

Branche par défaut distante détectée par Git :

```text
codex/create-expand-from-node-planning-documents
```

Branche documentaire créée pour cette mission :

```text
agent/grc20-initial-audit
```

Point de méthode : la branche `agent/grc20-initial-audit` a été créée depuis `origin/codex/create-expand-from-node-planning-documents`, conformément à la règle de ne pas supposer que `main` est la branche par défaut.

## 2. Graphe actif identifié

Fichier de graphe versionné actif identifié :

```text
grc20-these-mael-rolland-v96.json
```

Version déclarée dans `space.version` :

```text
v96
```

Nom d'espace déclaré :

```text
Mael Rolland -- Research
```

Description synthétique de l'espace : graphe de connaissances issu de la thèse EHESS 2024 de Maël Rolland sur la gouvernance des cryptomonnaies Bitcoin et Ethereum, les crises, l'institutionnalisme monétaire et les STS.

## 3. Comptages vérifiés du graphe actif

Comptages revalidés sur `grc20-these-mael-rolland-v96.json` :

| Objet | Nombre |
|---|---:|
| `entities` | 2 263 |
| `relations` | 20 057 |
| `types` | 55 |
| `relation_types` | 130 |
| `ops` | 293 |

Contrôles structurels rapides signalés pendant la Mission 001 puis revalidés :

| Contrôle | Résultat |
|---|---:|
| IDs d'entités dupliqués | 0 |
| Entités orphelines détectées | 0 |
| Relations avec endpoint manquant | 16 |

Ces contrôles ne constituent pas une validation complète GRC-20/Geo. Ils signalent seulement les risques prioritaires à reprendre dans une passe dédiée.

## 4. Fichiers d'architecture structurants

Le dépôt contient une couche documentaire d'architecture sous :

```text
docs/architecture/
```

Fichiers structurants repérés :

```text
docs/architecture/schema-vnext.md
docs/architecture/research-architecture-vnext.md
docs/architecture/STRUCTURE_CONSOLIDATION.md
docs/architecture/GRAPH_MODULARIZATION_AUDIT.md
docs/architecture/GRAPH_CROSS_CALL_AUDIT.md
docs/architecture/GRAPH_BOUNDARY_PLAN.md
docs/architecture/GRAPH_BOUNDARY_STRATEGY_REVIEW.md
docs/architecture/GRAPH_MODULE_BOOTSTRAP_CHECKPOINT.md
docs/architecture/GRAPH_PANEL_DEEPER_CHECKPOINT.md
docs/architecture/GRAPH_UI_BOUNDARY_CHECKPOINT.md
docs/architecture/STORY_CROSS_CALL_AUDIT.md
docs/architecture/STORY_BOUNDARY_PLAN.md
docs/architecture/STORY_HELPERS_CHECKPOINT.md
docs/architecture/STORY_SEAM_FRONTIER_PLAN.md
docs/architecture/STORY_LAYOUT_SEAM_VALIDATION_CHECKLIST.md
docs/architecture/STORY_LAYOUT_SEAM_VALIDATION_RESULT.md
docs/architecture/STORY_FOCUS_CROSS_CALL_AUDIT.md
docs/architecture/STORY_FOCUS_SEAM_PLAN.md
docs/architecture/STORY_FOCUS_SEAM_VALIDATION_RESULT.md
docs/architecture/STORY_EXPAND_CROSS_CALL_AUDIT.md
docs/architecture/STORY_EXPAND_SEAM_PLAN.md
docs/architecture/STORY_EXPAND_CONTRACT_FREEZE.md
docs/architecture/STORY_EXPAND_SEAM_VALIDATION_RESULT.md
```

Lecture synthétique issue de la Mission 001 :

- le graphe public reste static-first ;
- `graphe.html` demeure un point historique de concentration runtime, même si plusieurs modules `graphe.*.js` existent ;
- les seams Story/Graph sont documentés progressivement : layout, focus, expand-from-node ;
- la séparation `workshop/` vs publication publique est explicitement cadrée ;
- les documents récents privilégient des changements incrémentaux, instrumentés et compatibles avec le comportement existant.

## 5. État de la documentation de preuve

Aucun dossier `docs/audits/` n'existait avant cette mission ; il est créé ici pour accueillir ce rapport.

Audits et documents GRC-20 déjà présents sous `docs/` :

```text
docs/grc20_chapter_anchor_audit.md
docs/grc20_coverage_fidelity_audit_2026-04-01.md
docs/grc20_evidence_audit.md
docs/grc20_final_change_report.md
docs/grc20_home_cards_editorial_doc.md
docs/grc20_narrative_matrix.md
docs/grc20_ontology_audit.md
docs/grc20_relations_audit.md
docs/grc20_views_audit.md
```

Constats synthétiques repris de la Mission 001 :

- le graphe contient un volume important de `SourceQuote` ;
- la preuve est particulièrement dense autour des crises CVE 2018 et The DAO ;
- certaines relations structurantes entre catégories d'acteurs, groupes, arènes et processus de gouvernance restent à documenter plus explicitement ;
- les sources indigènes doivent rester traitées comme matériau empirique, non comme autorité théorique ;
- les documents vNext introduisent une couche atelier pour `SourceQuote`, `Claim`, `DecisionTrace`, `ValidationEvent`, `NarrativePreset` et `NarrativeStep`, sans modifier directement le snapshot canonique.

## 6. Risques prioritaires

| Priorité | Risque | Nature | Commentaire |
|---:|---|---|---|
| 1 | 16 relations avec endpoint manquant | Structure graphe | À auditer avant tout enrichissement ou publication prétendant à une validation complète. |
| 2 | Résolution incomplète des focus nodes Story | Runtime narratif | L'audit de couverture signale de nombreux labels de focus non résolus. |
| 3 | Chapitre II sous-narrativisé | Fidélité argumentative | La chaîne monétisation / institutionnalisme monétaire / règle-discrétion est plus faible que les récits de crise. |
| 4 | Surpondération visuelle et narrative du Chapitre III | Équilibre analytique | Risque d'entrée “crisis-first” au détriment de l'infrastructure et de la monétisation. |
| 5 | Validation de certains seams par inspection seulement | Technique | Les docs Story Expand indiquent que la validation runtime console n'a pas été directement observée dans l'environnement. |
| 6 | Lisibilité mobile et densité visuelle | Visualisation | Recommandations existantes : contraste des labels, plafonnement en mode Éclater, séparation gouvernance/crises. |
| 7 | Conformité Geo/GRC-20 incomplètement qualifiée | Publication | `space.id` placeholder et contraintes d'ID à vérifier avant publication. |

## 7. Séquence de 5 petites PR recommandées

### PR 1 — Audit des endpoints manquants de `v96`

Objectif : identifier précisément les 16 relations dont `from` ou `to` ne résout pas vers une entité existante.

Contraintes : audit seulement dans un premier temps ; ne pas supprimer ni recréer d'entité sans preuve.

Validation attendue : rapport reproductible listant relation ID, endpoint manquant, type de relation, hypothèse de cause et niveau de confiance.

### PR 2 — Rapport de résolution des focus nodes Story

Objectif : produire un rapport automatique ou semi-automatique des labels de `story-presets.mjs` qui résolvent ou non vers des entités du graphe.

Contraintes : aucune modification runtime ; aucune création d'entité pour combler un label absent.

Validation attendue : séparation entre alias évident, entité existante sous autre nom, concept absent du graphe, concept à vérifier dans la thèse.

### PR 3 — Lisibilité mobile des labels de colonnes

Objectif : appliquer la recommandation de `docs/grc20_views_audit.md` sur le contraste, la taille et la rotation des labels mobiles.

Contraintes : CSS / présentation uniquement ; aucun changement de graphe, de données ou de logique de layout.

Validation attendue : vérification des vues Structure, Monétisation et Qui gouverne réellement ? en viewport mobile.

### PR 4 — Plafonnement explicite en mode Éclater

Objectif : limiter les nœuds non labellisés par sous-cluster pour réduire l'effet hairball.

Contraintes : ne pas masquer silencieusement des entités sans indication ; conserver l'accès par recherche ou focus.

Validation attendue : comparaison avant/après sur clusters Chapitre I, Chapitre II et Chapitre III.

### PR 5 — Toggle visuel “Séparer gouvernance / crises”

Objectif : ajouter une option de vue permettant de distinguer visuellement les objets de crise et les objets de gouvernance.

Contraintes : option de visualisation uniquement ; ne pas retyper les entités ; ne pas modifier le JSON canonique.

Validation attendue : toggle off = comportement actuel ; toggle on = séparation visuelle explicite, sans modification des données.

## 8. Limites de ce rapport

Ce rapport est une synthèse documentaire initiale. Il ne corrige pas le graphe, ne valide pas les citations contre le PDF de thèse et ne modifie aucun comportement runtime.

Fichiers volontairement non touchés dans cette mission :

```text
grc20-these-mael-rolland-v96.json
graphe.html
scripts/*
workshop/scripts/*
graph-worker.mjs
fichiers de déploiement
```
