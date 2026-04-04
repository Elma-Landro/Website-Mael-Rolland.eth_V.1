# workspace/audits/ — Audit Documents

This directory is the **target location** for audit documents currently in `docs/` at the repository root.

## Phase 2 migration

In Phase 2, the following files will be moved from `docs/` to this directory:

| Current location | Document | Content |
|---|---|---|
| `docs/grc20_ontology_audit.md` | Ontology audit (v93 base) | Entity type analysis, confusion risks, corrective table |
| `docs/grc20_evidence_audit.md` | Evidence/citations audit | SourceQuote coverage, SUPPORTED/TODO_VERIFY/UNRESOLVED grid |
| `docs/grc20_relations_audit.md` | Relations audit | Relation type usage, gaps |
| `docs/grc20_views_audit.md` | Views audit | Visualization view analysis |
| `docs/grc20_coverage_fidelity_audit_2026-04-01.md` | Coverage/fidelity audit | Detailed coverage analysis |
| `docs/grc20_chapter_anchor_audit.md` | Chapter anchor audit | Chapter assignment rules and fixes |
| `docs/grc20_narrative_matrix.md` | Narrative matrix | Narrative structure analysis |
| `docs/grc20_home_cards_editorial_doc.md` | Home cards editorial | UI editorial decisions |
| `docs/grc20_final_change_report.md` | Final change report | Summary of changes |
| `docs/sourcequote-migration-runbook.md` | SourceQuote migration runbook | Step-by-step migration instructions |

Do not move these files until Phase 2 is planned and reviewed. Leave `docs/` intact for now.

## Relationship to DecisionTrace objects

Audit documents capture analytical findings.
DecisionTrace objects (`../decisions/traces/`) capture the resulting decisions.
Both are needed: the audit is the evidence, the trace is the record of action taken.
