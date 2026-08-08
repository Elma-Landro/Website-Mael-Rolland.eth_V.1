# docs/audits/data — données probantes des audits

Ces CSV/JSON sont les **données probantes** des audits de `docs/audits/`.
Chaque fichier se lit avec l'audit qui l'a produit — jamais seul : les
définitions, baselines simulées et mises en garde vivent dans l'audit, pas
dans le CSV.

| Fichier | Audit d'origine |
|---|---|
| `panel-policy-impact-v110.csv` | `grc20-panel-policy-lab-v1.md` (baseline = simulation fidèle du lecteur : parentes agrégées, tri stable sans bris d'égalité) |
| `poids-ancrage-diagnostic-v110.csv` | `grc20-poids-ancrage-v2.md` |
| `anchoring-baseline.json` | `scripts/check_anchoring.py` (régressions acceptées, motivées) |
| `bibliographie-reconciliation-v109.csv` | `grc20-bibliographie-reconciliation-v1.md` |
| `bibliographie-18-fiches-douteuses-v1.csv` | `grc20-bibliographie-reconciliation-lab-v1.md` (tri alphabétique stable, aucun horodatage ; contient **22** fiches malgré le « 18 » du nom, hérité du périmètre du patch_18 — 18 douteuses + 4 homonymie/multi-auteurs) |
| `bibliographie-doublons-familles-v1.csv` | `grc20-bibliographie-reconciliation-lab-v1.md` (tri par famille_id ; cible de fusion ≠ libellé final — lire § 3) |
| `bibliographie-entrees-sans-noeud-v1.csv` | `grc20-bibliographie-reconciliation-lab-v1.md` (tri par patronyme_annee ; lignes NAKAMOTO 2010F et ORLEAN 2002 corrigées par la revue hostile du 2026-08-07) |
| `bibliographie-parasites-et-jamais-cites-v1.csv` | `grc20-bibliographie-reconciliation-lab-v1.md` (tri par nom) |
| `catalogue-evenements-v2-fusion.csv`, `chronologie-domaines-decodee.csv`, `chronology-events-*.csv`, `added-events-from-chronology.csv`, `rejected-or-ambiguous-chronology-events.csv`, `dates-verification-externe.csv` | `grc20-chronologie-domaines-decodage.md`, `grc20-add-missing-events/`, `grc20-dedup-events-audit-v1.md` |
| `domaines-divergences.csv` | `grc20-domaines-developpement-v1.md` |
| `doublons-verifies.csv` | `grc20-dedup-events-audit-v1.md` |
| `maturation-phase-wiring.csv` | `grc20-maturation-phase-wiring.md` |
| `section-migration.csv`, `section-tree.csv` | `grc20-section-migration-chapitre-I.md`, `grc20-section-migration-chapitres-II-III.md` |
| `identity-debt-fr-en-v1.csv` | `grc20-sourcequote-migration-verification-v1.md` (§ découvertes annexes — relevé des 25 couples de fiches désignant un même référent apparent sous deux libellés, de part et d'autre de la frontière FR/EN ; une ligne par couple, tri par `paire_id` (ordre alphabétique de `name_fr`), types et degrés recomptés sur v110). **Ce relevé est une dette consignée, pas un plan de fusion** : aucune des 25 paires n'est arbitrée, la colonne `arbitrage_requis` pose une question et n'y répond pas. Les 5 lignes `nature=conflit-de-types` (dont `Pools de minage` / `Mining pools`, ActorGroup contre InfrastructureEvent) exigent un **arbitrage sémantique de l'auteur** avant toute action — jamais de fusion automatique. Les lignes `voisinage-non-doublon` et `indetermine` sont des refus de conclure, pas des candidats faibles. Ne jamais fusionner sur la seule foi de `preuve_correspondance` : c'est une trace de libellé, pas une preuve de référent. |
| `entity-alias-table-v1.csv` | `grc20-sourcequote-migration-verification-v1.md` (table d'alias EN→FR et variantes de libellés sur v110, une ligne par couple entité/alias, tri par `canonical_name` puis `alias`). **Une table d'alias n'est pas une autorisation de fusion** : elle sert à empêcher qu'un résolveur *recrée* en double une entité déjà présente sous un autre libellé — la décision d'identité (fusionner, renommer, créer) reste à l'auteur. Les alias `confidence=basse` ne doivent **jamais** servir à une résolution automatique : ils couvrent les chaînes ambiguës (un même alias pour plusieurs entités), les collisions (`collision_with` non vide — la chaîne est déjà le nom d'une autre fiche) et les traductions interprétatives. |

Mises en garde permanentes :

- **`direct_anchor_count` est une mesure pauvre** — occurrences littérales
  du nom en limites de mots ; elle sous-compte les noms forgés, traduits ou
  bilingues. Ne jamais la lire seule, toujours croiser avec
  `snippet_status` (grc20-poids-ancrage-v2.md § 5-6).
- **`snippet_status` n'est pas un certificat** — il atteste qu'un extrait
  de la carte contient le nom ou sa base de citation, rien de plus ; les
  clés de section des extraits sont elles-mêmes partiellement périmées.
- **Les baselines simulées sont documentées dans leur audit respectif** —
  par exemple, la baseline `legacy` de `panel-policy-impact-v110.csv`
  reproduit le pipeline réel de `lecteur.html` (agrégation des parentes,
  tri stable) et ses limites (ex æquo flottants inter-langages) sont
  déclarées dans `grc20-panel-policy-lab-v1.md` § 5.
