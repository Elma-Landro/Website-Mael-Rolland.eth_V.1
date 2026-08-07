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
| `catalogue-evenements-v2-fusion.csv`, `chronologie-domaines-decodee.csv`, `chronology-events-*.csv`, `added-events-from-chronology.csv`, `rejected-or-ambiguous-chronology-events.csv`, `dates-verification-externe.csv` | `grc20-chronologie-domaines-decodage.md`, `grc20-add-missing-events/`, `grc20-dedup-events-audit-v1.md` |
| `domaines-divergences.csv` | `grc20-domaines-developpement-v1.md` |
| `doublons-verifies.csv` | `grc20-dedup-events-audit-v1.md` |
| `maturation-phase-wiring.csv` | `grc20-maturation-phase-wiring.md` |
| `section-migration.csv`, `section-tree.csv` | `grc20-section-migration-chapitre-I.md`, `grc20-section-migration-chapitres-II-III.md` |

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
