# Runbook — SourceQuote migration (PR-08)

## 1) Prérequis

- Repository à jour avec les scripts:
  - `scripts/apply-sourcequote-phases.mjs`
  - `scripts/sourcequote-migration/*.mjs`
- Fichiers patch disponibles:
  - `Migration/sourcequote_effective_patch_phase1.zip`
  - `Migration/sourcequote_effective_patch_phase2.zip`
  - `Migration/sourcequote_effective_patch_phase3.zip`
- Un graphe local disponible au format:
  - `grc20-these-mael-rolland-v*.json`

L’orchestrateur charge les phases dans l’ordre strict:
1. phase1
2. phase2
3. phase3

## 2) Dry-run (obligatoire avant run réel)

Commande:

```bash
node scripts/apply-sourcequote-phases.mjs
```

Effet attendu:
- aucune mutation (dry-run)
- logs JSON par étape (`normalize`, `resolve`, `apply`, `report`, `orchestrator`)
- rapport consolidé final

Vérifications minimales:
- `duplicate_seed_ids` dans le rapport final
- `unresolved_sections`
- `ambiguous_supports`

## 3) Run réel

Commande:

```bash
node scripts/apply-sourcequote-phases.mjs --write
```

Comportement attendu:
- même ordre d’exécution phase1 -> phase2 -> phase3
- idempotence appliquée (`seed_id` puis signature secondaire)
- déduplication des relations avant création

## 4) Rollback logique

Le pipeline ne fournit pas de rollback automatique transactionnel.

Rollback logique recommandé:
1. conserver une copie de référence du graphe avant run réel
2. exécuter le run réel
3. en cas de divergence, restaurer la copie de référence
4. corriger les causes (sections/supports ambigus, mapping alias, etc.)
5. relancer en dry-run puis en write

## 5) Structure du rapport final

Le rapport final consolidé (stage `report`) contient:

- `totals.operations_read`
- `totals.operations_normalized`
- `totals.created`
- `totals.updated`
- `totals.skipped`
- `totals.partial`
- `totals.ambiguous_supports`
- `totals.unresolved_sections`
- `totals.duplicate_seed_ids`
- `phase_summaries[]` avec la même granularité par phase

## 6) Relancer sans doublons

Principes:
- clé idempotente principale: `seed_id`
- signature secondaire: `normalize(quoteText)::page::firstTargetSectionKey`
- déduplication des liens `appears in section` et `quote supports`

Procédure:
1. relancer en dry-run
2. vérifier `duplicate_seed_ids = 0` (ou comprendre les collisions)
3. vérifier les items `unresolved_sections` / `ambiguous_supports`
4. relancer en write

Résultat attendu:
- les éléments déjà appliqués passent en `skipped_idempotent`
- pas de doublons relationnels
