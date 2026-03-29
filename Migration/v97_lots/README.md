# v97 rollout en lots (task-by-task)

Base: `grc20-these-mael-rolland-v96.json`.

## LOT-1 — Hiérarchie des concepts
- Fichier: `Migration/v97_lots/lot-1-concepts.json`
- Contenu: retypes `Concept` vers `CoreConcept`/`SecondaryConcept`/`TechnicalConcept`, slogans vers `NativeFormula`, titres de section vers `ChapterSection`, et fusions manquantes (Nominalisme, EVM, Politique de crise[s]).
- Taille: **31 opérations**.

## LOT-2 — ActorNonHuman + StakeholderGroup
- Fichier: `Migration/v97_lots/lot-2-actors-stakeholders.json`
- Contenu: éclatement d'acteurs non humains vers `InfrastructureService` / `SoftwareClient`, + retypes des groupes attendus vers `StakeholderGroup`.
- Taille: **16 opérations**.

## LOT-3 — InfrastructureDomain + nouvelles relations
- Fichier: `Migration/v97_lots/lot-3-infra-relations.json`
- Contenu: cible de 9 domaines canoniques + ajout des relations `instanceOfCategory`, `organizes`, `partOfMonetizationProcess`.
- Taille: **13 relations**.

## État restant (avant application)
- Entités avec type `Concept` encore non hiérarchisé: **391**.
- Les 3 lots sont conçus pour être mergés séparément afin d'éviter un diff massif.
