# Synthèse — GRC-20 Audit Batch 001

## 1. Périmètre consolidé

Ce batch consolide les premières passes d’audit documentaire GRC-20 afin de limiter la multiplication des PR : audit initial, endpoints manquants v96, enquête sur `72d182705407492c`, résolution Story focus et audit visuel analytique.

Fichiers du batch :

- `docs/audits/grc20-initial-agent-audit.md`
- `docs/audits/grc20-v96-missing-endpoints-audit.md`
- `docs/audits/grc20-v96-endpoint-72d182705407492c-investigation.md`
- `docs/audits/grc20-story-focus-resolution-audit.md`
- `docs/audits/grc20-visual-analytical-design-audit.md`
- `docs/audits/grc20-audit-batch-001-summary.md`

## 2. Constats principaux

- Le graphe actif reste `grc20-these-mael-rolland-v96.json` : 2 263 entités, 20 057 relations, 55 types, 130 types de relations.
- 16 relations ont au moins un endpoint non résolu ; toutes ont un `from` manquant.
- 15 de ces relations correspondent probablement à des IDs tronqués à 16 caractères avec un candidat v96 unique.
- Le cas `72d182705407492c` est différent : il renvoie historiquement à `Common Pool Resources (CPR)`, présent en v81–v90 puis absent à partir de v91.
- Les focus nodes de `story-presets.mjs` résolvent tous avec la logique runtime actuelle : 167 occurrences inspectées, 0 non-résolue, 0 collision.
- La dette visuelle porte moins sur l’absence de données que sur la hiérarchie des couches : hubs de sections, références, SourceQuotes, arêtes cachées, mobile et mode Éclater.

## 3. A. Corrections sûres et mécaniques

| Priorité | Correction candidate | Justification | Future PR |
|---:|---|---|---|
| A1 | Remplacer les 15 endpoints `from` tronqués par l’ID complet v96 unique | correspondance préfixe → entité unique ; réparation référentielle sans création sémantique | v97 mécanique |
| A2 | Ajouter une validation d’intégrité référentielle avant export | empêche la réapparition de relations orphelines | PR script/test séparée |
| A3 | Documenter explicitement que Story focus résout actuellement tous les labels | évite une PR corrective inutile sur `story-presets.mjs` | documentation seulement |

## 4. B. Corrections nécessitant validation scientifique

| Priorité | Correction candidate | Décision requise | Risque |
|---:|---|---|---|
| B1 | Traiter `72d182705407492c` | restaurer `Common Pool Resources (CPR)` ou supprimer la relation legacy | réintroduire une entité supprimée ou effacer une intention analytique |
| B2 | Vérifier les relations `cited in` et `contributes to` autour des références théoriques | confirmer que les relations sont bien thèse-grounded | transformer un lien bibliographique en autorité théorique indue |
| B3 | Rééquilibrer la narration Chapitre II / Chapitre III | arbitrage scientifique sur monétisation, institutionnalisme et crises | surpondérer les crises au détriment de la thèse monétaire/infrastructurelle |
| B4 | Décider du statut visuel des SourceQuotes | preuve visible à la demande vs nœuds permanents | perdre la traçabilité ou saturer le graphe |

## 5. C. Corrections visuelles / runtime à tester

| Priorité | Correction candidate | Test minimal requis |
|---:|---|---|
| C1 | Compteur relations affichées/masquées en Story/Focus | vérifier sur Structure, Monétisation, Qui gouverne réellement |
| C2 | Plafonnement du mode Éclater avec indicateur `+N nœuds masqués` | comparaison avant/après sur hubs Chapitre I, II, III |
| C3 | Renforcement mobile des labels de colonnes | viewport mobile réel, contrôle contraste et densité |
| C4 | Couche SourceQuote à la demande | test de traçabilité citation → claim → section |
| C5 | Hiérarchie visuelle des hubs | prototype bandes chapitres/sections vs hubs radiaux |

## 6. Proposition de future PR v97

Créer une PR v97 distincte et limitée :

1. appliquer uniquement les 15 corrections mécaniques d’IDs tronqués ;
2. laisser `72d182705407492c` hors correction mécanique tant que la décision scientifique n’est pas prise ;
3. exécuter une validation JSON + endpoints + orphelins ;
4. produire un changelog v97 séparant clairement réparation technique et décisions ontologiques non appliquées.

## 7. Non-actions dans ce batch

- Aucun changement de `grc20-these-mael-rolland-v96.json`.
- Aucun `v97` créé.
- Aucun changement de `graphe.html`, `story-presets.mjs`, `narrative-anchors.json`, scripts ou déploiement.
- Aucun merge.
