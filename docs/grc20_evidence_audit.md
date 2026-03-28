# GRC20 — Audit citations & preuves (Sous-agent D)

## Règles respectées
- Pas d'invention de citation.
- Pas d'invention de pagination.
- Distinction stricte: preuve présente / preuve manquante / à vérifier.

## Observations
1. Le graphe contient un volume important de `SourceQuote` (245) avec attributs de source.
2. De nombreuses preuves sont concentrées sur les crises (CVE, DAO), ce qui est cohérent avec la thèse.
3. Certaines relations structurantes (catégories d'acteurs ↔ groupes ↔ arènes) restent sous-justifiées par citation directe.

## Grille de statut
- **SUPPORTED**: relation appuyée par `SourceQuote`/`Reference` existante.
- **TODO_VERIFY**: source mentionnée mais ancrage citationnel incomplet.
- **UNRESOLVED**: relation plausible mais sans preuve textuelle explicite retrouvée.

## Compléments recommandés (non injectés)
- Ajouter quotes ciblées pour:
  - gouvernance polycentrique (II.3),
  - clarification stakeholders/shareholders,
  - articulation règle/discrétion,
  - comparaison CVE (huis clos) vs DAO (public).

## Limites
- Pagination parfois présente seulement dans sources PDF, pas toujours dans markdown.
- Les ajouts proposés restent en `PROPOSED_REVIEW` tant que la preuve n'est pas matérialisée.
