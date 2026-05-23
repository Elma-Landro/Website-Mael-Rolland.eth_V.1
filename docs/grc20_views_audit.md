# GRC20 — Audit des vues & dataviz (Sous-agent F)

## Vues auditées
- Structure de la thèse
- Monétisation
- Qui gouverne réellement ?
- Focus (Isoler / Éclater / Contexte)

## Problèmes constatés puis traités
1. **Propagation chapitrale indue** due à exclusion BFS inactive (bug de type).
2. **Pollution gouvernance/crise**: `CrisisPhase` placées en colonne Gouvern. dans QG.
3. **Lisibilité labels**: troncature trop agressive des noms en mode dense.
4. **Ancrage infra de crise**: forcing Chap. I trop agressif pour les objets infra connectés à des crises.

## Correctifs implémentés
- Fix BFS type-aware (tableau de types effectifs).
- QG: `CrisisPhase` retiré de la colonne Gouvern. (rebasculé vers Cas/Réf. par défaut).
- Labels: seuil de troncature élargi.
- Matrice structure: exception pour nœuds infra reliés à crises (non forcés Chap. I).

## Recommandations prochaines passes
- Ajouter un toggle explicite "Séparer gouvernance / crises" dans le panneau Focus.
- Mobile: renforcer contrastes des labels de colonnes (rotation + taille selon densité).
- Mode Éclater: plafonner explicitement les nœuds non-labellisés par sous-cluster.
