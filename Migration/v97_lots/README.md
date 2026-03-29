# v97 rollout en 6 lots (task-by-task)

Base: `grc20-these-mael-rolland-v96.json`.

Objectif: éviter un diff massif en poussant **lot par lot**.

## Ordre de merge recommandé
1. `lot-1-concept-hierarchy.json` — hiérarchie de concepts (hors fusions reportées)
2. `lot-2-actornonhuman-split.json` — split ActorNonHuman restant
3. `lot-3-stakeholder-groups.json` — compléter 6+ StakeholderGroup
4. `lot-4-infrastructure-domain-canon.json` — 9 domaines canoniques
5. `lot-5-relations.json` — nouvelles relations (`instanceOfCategory`, `organizes`, `partOfMonetizationProcess`)
6. `lot-6-missing-merges.json` — fusions manquées (Nominalisme, EVM, Politique de crise[s])

## Tailles générées
- LOT-1: **26 opérations**
- LOT-2: **8 opérations**
- LOT-3: **6 opérations**
- LOT-5: **13 relations**
- LOT-6: **3 opérations**

## État restant (avant application)
- Entités encore typées `Concept` en v96: **391**.
