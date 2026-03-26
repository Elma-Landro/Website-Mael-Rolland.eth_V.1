
# Implementer prompt — GRC-20 v91 migration

You are given:
- `grc20-these-mael-rolland-v90.json` (or equivalent v90 graph JSON)
- `grc20_v91_name_based_patch.json`
- `grc20_v91_migration_table.csv`

Your task is to produce a **v91 graph JSON** by applying the patch conservatively.

## Required behavior
1. Resolve every `old_entity` and `new_entity` by exact label match first.
2. If exact match fails, try normalized matching:
   - lowercase
   - trim spaces
   - remove accents
   - collapse repeated spaces
3. Never silently discard an unmatched item. Put it in a `manual_review` section of the output report.
4. For `merge_into`:
   - keep the target entity
   - move old label into aliases
   - redirect relations from old entity to target
   - preserve provenance notes if present
5. For `retype`:
   - change type only if the current label matches the intended referent
6. For `rename_retype`:
   - preserve label unless schema requires canonical renaming
   - change type
7. For `flag_split` and `flag_attribute`:
   - do not transform automatically unless the codebase already supports it
   - emit them in `manual_review`
8. Add the `new_relations` if both endpoints exist after merges/retypes.
9. Emit:
   - `grc20-these-mael-rolland-v91.json`
   - `grc20_v91_application_report.json`
   - summary counts: merges applied, retypes applied, unmatched entities, manual review items

## Ontological intent
The goal is not cosmetic cleanup. The goal is to:
- distinguish analytical categories from empirical collectives
- separate institutions/organizations from loose actor groups
- split non-human entities by ontology
- elevate monetization as the central organizing layer of the graph

## Manual review expected
Some items need human arbitration:
- co-author strings like `Desmedt et Lakomski-Laguerre`
- claims disguised as concepts
- section-title concepts
- borderline cases between Organization / Institution / PlatformService
