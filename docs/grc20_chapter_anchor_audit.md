# GRC20 — Audit des ancrages chapitraux (Sous-agent C)

## Règle appliquée
**Primary textual anchoring overrides relational propagation.**

## Vérifications prioritaires

### 1) CVE-2018-17144
- Constat manuscrit: traité dans **Chapitre III** (III.1–III.2).
- Risque technique: dérive de placement via propagation relationnelle ou heuristique infra.
- Correction appliquée (vue): les entités infra liées à crise ne sont plus ré-aspirées mécaniquement vers Chap. I.

### 2) Scaling Debate
- Ancrage principal: **Chapitre II** (II.3, gouvernance et clarification des camps).
- Règle: conserver extension secondaire possible en crise, sans changer le principal.

### 3) InfrastructureEvent aspirés vers Chap. III
- Correction: stricte séparation entre événements infra ordinaires (Chap. I) et événements infra connectés à `CrisisEvent`/`CrisisPhase`.

### 4) Émergence Ethereum
- Ancrage principal: **Chapitre I.3**.
- Les overrides nominatifs existants ont été conservés et documentés.

## SAFE FIX implémentés
- Correction BFS des exclusions de type (bug empêchant la protection contre propagation).
- Garde-fou dans la matrice structure: ne pas forcer vers Chap. I les nœuds infra reliés à des crises.

## Overrides ciblés (proposés)
Voir `patches/grc20_anchor_overrides_targeted.json`.

- `classification`: SAFE_FIX / STRONGLY_SUPPORTED / PROPOSED_REVIEW
- Aucun ajout inventé: seulement des IDs existants + chapitre cible.
