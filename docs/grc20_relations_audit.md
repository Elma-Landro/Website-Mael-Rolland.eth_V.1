# GRC20 — Audit des relations (Sous-agent E)

## Constat global
Le graphe est riche mais présente des asymétries:
- forte densité sur événements et références,
- densité hétérogène sur chaînes conceptuelles "acteur → arène → processus → conflit".

## Points de friction
1. Certaines vues confondent relations de gouvernance et relations de crise (effet de contamination visuelle).
2. Les liens entre catégories analytiques et groupes empiriques sont partiellement explicites.
3. Les processus de maintenance sont parfois absorbés par des clusters d'événements.

## Correctifs appliqués côté visualisation
- Découplage de la colonne Gouvern. et des `CrisisPhase` dans la vue "Qui gouverne réellement ?".
- Réduction des déplacements arbitraires infra→Chap. I quand l'entité est reliée à une crise.

## Backlog relations (proposé)
- `StakeholderCategory -> represented by -> StakeholderGroup` (là où prouvé)
- `GovernanceArena -> hosts -> GovernanceProcess`
- `GovernanceConflict -> revealed by -> CrisisEvent`
- `InfrastructureEvent -> conditions -> GovernanceConflict`

Statut: **PROPOSED_REVIEW** (nécessite sourcing explicite pour injection).
