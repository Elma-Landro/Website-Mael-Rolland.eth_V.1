# Workshop Real-Usage Checkpoint (minimal demonstrator)

Date: 2026-04-04  
Mode: lab-only, non-destructive, no runtime coupling

## 1) What the current sample lot demonstrates

The workshop now has one grounded object for each core family needed to demonstrate a minimal evidence chain:

- Claim: `claim-sample-thesis-scope-v96`
- SourceQuote: `sq-sample-thesis-description-v96`
- ValidationEvent: `validation-sample-claim-thesis-scope-v96`
- NarrativePreset: `narrative-preset-sample-thesis-entrypoint-v96`

All samples reference existing repository context (`grc20-these-mael-rolland-v96.json`) with explicit provenance fields and conservative semantics.

## 2) What the evidence chain currently covers

Current demonstrated chain:

1. A Claim is stated and linked to one canonical entity ID.
2. A SourceQuote is extracted from the canonical entity description and linked to the Claim.
3. A ValidationEvent records that the Claim ↔ SourceQuote linkage and locator were manually checked.
4. A NarrativePreset provides a minimal guided entrypoint around the same thesis root entity.

This is sufficient as a first traceability slice (claim + evidence + validation + narrative context), without claiming full migration or publication readiness.

## 3) How status/policy behaves on real samples

Under `workshop/exports/export-policy.json` and current statuses:

- `Claim` is public-eligible in principle and currently has one `validated` item.
- `SourceQuote` is public-eligible in principle but current sample status is `needs_review`.
- `NarrativePreset` is public-eligible in principle but current sample status is `needs_review`.
- `ValidationEvent` is workshop-only by policy in this phase.
- `DecisionTrace` remains workshop-only by policy in this phase.

Dry-run therefore reports:

- Claim: `candidate_exportable_items_present`
- SourceQuote: `present_but_not_export_ready`
- NarrativePreset: `present_but_not_export_ready`
- ValidationEvent: `not_exportable_in_public_bundle`

## 4) What remains workshop-only vs public-eligible in principle

Workshop-only (policy visibility):

- DecisionTrace
- ValidationEvent

Public-eligible in principle (policy visibility):

- SourceQuote
- Claim
- NarrativePreset

Important: "public-eligible in principle" here is policy classification only in dry-run mode; no publication action is performed.

## 5) What is still not export-ready

In the current mini-lot:

- SourceQuote is not export-ready (`needs_review`).
- NarrativePreset is not export-ready (`needs_review`).

Only the sample Claim currently meets status gating for "eligible in principle" in dry-run output.

## 6) Intentional out-of-scope boundaries (unchanged)

- No canonical graph mutation.
- No runtime/public loader changes.
- No deployment path changes.
- No patch application.
- No schema redesign in this checkpoint.

## 7) Checkpoint conclusion

For this phase, the workshop minimal demonstrator can be considered **established**:

- the smallest credible evidence chain is present,
- status/policy behavior is observable on real samples,
- and non-destructive boundaries remain intact.

This establishes a stable baseline for future, explicitly approved increments.
