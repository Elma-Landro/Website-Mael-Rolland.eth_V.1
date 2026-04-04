# workspace/patches/ — Patch File Registry

This directory organizes patch files for the canonical GRC-20 graph.

## Directory layout

- `pending/` — patches that have NOT yet been applied to the canonical graph
- `applied/` — patches that HAVE been merged into the canonical graph snapshot

## Current patch status (as of 2026-04-04)

The following patch files currently live at the **repository root** and have not yet been moved here.
This table documents their status relative to the canonical graph `grc20-these-mael-rolland-v96.json`.

| Filename | Content | Applied to v96? | Notes |
|---|---|---|---|
| `patch_1a_fix_cited_in.json` | Fix 22 wrong-chapter `cited_in` relations | Unknown | Needs audit vs v96 |
| `patch_1b_missing_cited_in.json` | Add 213 multi-chapter `cited_in` relations | Unknown | Needs audit vs v96 |
| `patch_2a_sourcequote_subsections.json` | Link SourceQuote → ThesisSection (54+ ops) | Unknown | v96 has 245 SQ; partially applied? |
| `patch_2b_central_arguments.json` | Add `central_argument` attributes to ThesisSection entities | Unknown | Needs audit |
| `patch_2c_definitions.json` | Add definition TEXT attributes to 12 Concept entities | Unknown | Needs audit |
| `patch_3a_intro_subsections.json` | Create 17 new ThesisSection subsections | Unknown | v96 has 70 ThesisSection; may be applied |
| `patch_4_intro_key_entities.json` | Key intro entities | Unknown | Needs audit |
| `patch_4a_chapter_attribution.json` | Chapter attribution corrections | Unknown | Needs audit |
| `patch_5_missing_sections.json` | Missing section links | Unknown | Needs audit |
| `patch_5a_corrective_anchoring.json` | Corrective anchoring | Unknown | Needs audit |
| `patch_batch1_anchoring.json` | Batch 1 anchoring | Unknown | Needs audit |
| `patch_batch2_anchoring.json` | Batch 2 anchoring | Unknown | Needs audit |
| `patch_batch3_relations.json` | Batch 3 relations | Unknown | Needs audit |
| `new_relations_patch.json` | Large batch of new relations (3MB) | Unknown | Needs audit |

Also in `Migration/`:
- `sourcequote_effective_patch_phase1.zip` — SourceQuote Phase 1 (planned but not confirmed applied)
- `sourcequote_effective_patch_phase2.zip` — SourceQuote Phase 2
- `sourcequote_effective_patch_phase3.zip` — SourceQuote Phase 3
- `sourcequote_migration_foundation.zip` — Foundation migration

## Phase 2 actions

In Phase 2, each root patch will be:
1. Audited against v96 to determine if already applied
2. Moved to `pending/` (if unapplied) or `applied/` (if already merged)
3. Applied via `npm run apply-patches` to produce v97

Do not move patches here until audit is complete.

## Patch file format

Patches follow this structure:
```json
{
  "description": "Human-readable description",
  "graph_version": "version identifier",
  "operations": [
    {
      "op": "ADD_RELATION | REMOVE_RELATION | SET_ATTRIBUTE | ADD_ENTITY | ...",
      "from_entity_id": "...",
      "to_entity_id": "...",
      "relation_type": "...",
      "note": "rationale"
    }
  ]
}
```
