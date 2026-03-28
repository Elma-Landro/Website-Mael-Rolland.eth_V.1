# Overrides batch 1 — ancrages, types et colonnes

Ce paquet contient une première passe **conservative** d’overrides entité par entité.

## Structure des colonnes
- `entity` : libellé actuel
- `current_type` / `current_chapter` : état observé dans l’inventaire v90
- `proposed_type` : type cible si retypage conseillé
- `proposed_primaryChapter` : chapitre principal proposé
- `proposed_primarySection_hint` : indice de section principale
- `proposed_column` : colonne visuelle cible dans les vues matricielles
- `status` :
  - `SAFE_FIX` = correction quasi certaine
  - `KEEP_CONFIRM` = placement actuel jugé correct
  - `REVIEW` = forte présomption, mais à vérifier dans le manuscrit / code
  - `RETYPE_REVIEW` = retypage conseillé, à valider avant commit
  - `MERGE_REVIEW` = fusion / canonisation conseillée
  - `CANONICAL_RENAME_REVIEW` = normalisation de nom proposée

## Priorités de traitement
1. Appliquer d’abord tous les `SAFE_FIX`.
2. Vérifier ensuite les `RETYPE_REVIEW` et `MERGE_REVIEW`.
3. Garder trace des `secondaryChapters` quand une entité est réutilisée plus tard.
4. Ne pas laisser le voisinage relationnel déplacer le `primaryChapter`.

## Noyaux les plus importants de ce batch
- CVE-2018-17144 et sa séquence doivent être ancrées en **Chap. III**.
- Le **Scaling Debate** doit être ramené du côté **Chap. II / Gouvern.** comme clarification de gouvernance.
- Les `InfrastructureEvent` du développement infrastructural de Bitcoin doivent revenir vers **Chap. I / I.2**.
- L’émergence d’Ethereum (ICO / Frontier / Genesis Sale) doit revenir vers **Chap. I / I.3**.
- Les `DevelopmentPhase` doivent être réordonnées dans le chapitre de développement, pas entre Chap. III et Conclusion.
- Les faux concepts / faux acteurs (`Bitmain`, `CEX.io`, titres de sections dans Concept, etc.) doivent être retypés.

## Taille du batch
Nombre de lignes : 75
