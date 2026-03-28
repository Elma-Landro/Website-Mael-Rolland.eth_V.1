# GRC20 — Audit ontologique (Sous-agent B)

## Périmètre
- Base audité: `grc20-these-mael-rolland-v93.json`.
- Objectif: détecter erreurs de typage, confusions de catégories, besoins de normalisation.

## Constats principaux
1. **Distribution dominante**: `Reference`, `Concept`, `SourceQuote`, `InfrastructureEvent` sont surreprésentés (normal pour un graphe thèse + preuves).
2. **Pas de doublons exacts de nom** détectés (normalisation stricte nominale OK).
3. **Risque de confusion fonctionnelle** entre:
   - `StakeholderCategory` vs `StakeholderGroup`
   - `Institution` vs `Organization`
   - `GovernanceConflict` vs `CrisisEvent`
   - `InfrastructureEvent` vs `CrisisPhase`
4. Plusieurs entités d'événements sont typées infrastructurellement alors qu'elles sont mobilisées en **cas de gouvernance de crise** (à traiter par attribut d'ancrage, pas forcément retypage massif).

## Table corrective (priorisée)

| Classe | Action | Catégorie | Statut |
|---|---|---|---|
| `CrisisPhase` mappée en colonne Gouvern. dans la vue QG | Replacer en "Cas/Réf." pour éviter pollution gouvernance | SAFE FIX (vue) | **Implémenté** |
| Exclusion BFS fondée sur `e.type` (champ absent) | Corriger vers lecture `e.types[]` + noms de type | SAFE FIX (algorithme) | **Implémenté** |
| `Institution`/`Organization` | Garder dualité mais documenter critère (ordre juridique vs entité opérante) | STRONGLY SUPPORTED | Documenté |
| `StakeholderCategory`/`StakeholderGroup` | Vérifier correspondances 1→n (catégorie vers groupes) | PROPOSED REVIEW | À faire en patch dédié |

## Critères de typage (doctrine)
- `CrisisEvent`: événement macroscopique de crise.
- `CrisisPhase`: sous-moment processuel interne à une crise.
- `GovernanceConflict`: conflictualité de gouvernance (peut exister hors crise).
- `GovernanceProcess`: procédure ou modalité décisionnelle.
- `InfrastructureEvent`: jalon de développement infra non réduit à la crise.
- `StakeholderCategory`: classe analytique.
- `StakeholderGroup`: collectif empirique situé.

## Liste de vigilance (non injectée)
- Entités candidates à enrichissement multi-typing (`InfrastructureEvent` + attribut crise).
- Entités frontières à annoter `isReusedLater` / `secondaryChapters`.
