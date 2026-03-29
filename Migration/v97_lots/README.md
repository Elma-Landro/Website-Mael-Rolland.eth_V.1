# v97 rollout en 6 lots (task-by-task)

Base: `grc20-these-mael-rolland-v96.json`.

Objectif: éviter le dépassement de taille de diff en poussant **lot par lot**.

## Ordre de merge recommandé
1. `lot-1-concept-hierarchy.json` — hiérarchie des concepts (gros backlog)
2. `lot-2-actornonhuman-split.json` — ActorNonHuman résiduels
3. `lot-3-stakeholder-groups.json` — compléter 6+ StakeholderGroup
4. `lot-4-infrastructure-domain-canon.json` — 9 domaines canoniques
5. `lot-5-relations.json` — nouvelles relations (`instanceOfCategory`, `organizes`, `partOfMonetizationProcess`)
6. `lot-6-missing-merges.json` — fusions manquées finales

## Notes
- Chaque lot est indépendant et volontairement petit.
- Les champs `*_exists_v96` servent à vérifier rapidement la présence des labels dans la base v96.
