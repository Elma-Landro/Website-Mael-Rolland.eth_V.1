# Workshop Export Dry-Run (manifest-driven, non-destructive)

Generated: 2026-04-04T19:49:08.192Z

## Guarantees
- No canonical graph file is modified.
- No new canonical graph version is generated.
- No patch is applied.
- No runtime/public loader path is changed.

## Export manifest used
- Path: workshop/exports/export-policy.json
- Found: yes
- Version: 1.0.0-dry-run
- Mode: documentary_only
- Note: Manifest-driven policy loaded for dry-run analysis only.

## Canonical source inspected
- Path: grc20-these-mael-rolland-v96.json
- Version: v96
- Entities: 2263
- Relations: 20057
- Note: Selected highest detected canonical graph version at repository root.

## Patch inventory context (read-only)
- Inventory path: workshop/patches/patch-inventory.json
- Found: yes
- Note: Using documentary patch inventory as context only. No patch application is performed in dry-run mode.
- Artifact total: 34
- Status breakdown:
  - candidate_applied: 1
  - candidate_pending: 2
  - superseded_possible: 2
  - unknown: 29

## Status policy from manifest
- Exportable in principle: legacy_canonical, validated
- Review/dispute statuses: needs_review, contested
- Workshop-only internal statuses: raw, extracted, linked
- Note: Status policy comes from workshop/exports/export-policy.json. Dry-run only; no promotion occurs.

## Object families detected (manifest-driven)
- SourceQuote (workshop/evidence/sourcequotes)
  - files: 1; parseErrors: 0; visibility: public_eligible
  - statusField: status; allowedStatusesForExportInPrinciple: validated
  - statuses: needs_review:1
  - expectedOutput: public-data/evidence.public.json
  - readiness: present_but_not_export_ready
- Claim (workshop/claims)
  - files: 1; parseErrors: 0; visibility: public_eligible
  - statusField: status; allowedStatusesForExportInPrinciple: validated
  - statuses: validated:1
  - expectedOutput: public-data/claims.public.json
  - readiness: candidate_exportable_items_present
- DecisionTrace (workshop/decisions/traces)
  - files: 1; parseErrors: 0; visibility: workshop_only
  - statusField: status; allowedStatusesForExportInPrinciple: none
  - statuses: validated:1
  - expectedOutput: workshop/decisions/traces/*.json
  - readiness: not_exportable_in_public_bundle
- ValidationEvent (workshop/validations)
  - files: 1; parseErrors: 0; visibility: workshop_only
  - statusField: result; allowedStatusesForExportInPrinciple: none
  - statuses: approved:1
  - expectedOutput: workshop/validations/*.json
  - readiness: not_exportable_in_public_bundle
- NarrativePreset (workshop/narratives/presets)
  - files: 1; parseErrors: 0; visibility: public_eligible
  - statusField: status; allowedStatusesForExportInPrinciple: validated
  - statuses: needs_review:1
  - expectedOutput: public-data/narratives.public.json
  - readiness: present_but_not_export_ready

## Public-export-eligible families
- SourceQuote, Claim, NarrativePreset

## Workshop-only families
- DecisionTrace, ValidationEvent

## Are any workshop artifacts export-ready now?
- Claim: 1 item(s) allowed by manifest
- Summary: Some public-eligible families contain artifacts with statuses allowed by the manifest policy.

## Future pipeline outputs referenced by manifest (not generated now)
- public-data/evidence.public.json
- public-data/claims.public.json
- workshop/decisions/traces/*.json
- workshop/validations/*.json
- public-data/narratives.public.json

## Unresolved blockers / unknowns
- Manifest policy is conservative and may keep families workshop-only until explicit publication criteria are approved.
- Patch inventory statuses are heuristic and documentary, not proof of apply-state.
- Missing/empty family directories are treated as no artifacts detected, not as errors.
- This script does not execute canonical export; it only reports policy-based readiness.
