# Schema vNext — Scholarly Graph Evolution (Compatibility-first)

## 1) Current model summary (observed)
Current canonical snapshot (`grc20-these-mael-rolland-v96.json`) follows a GRC-20-like shape:
- `space`
- `types`
- `relation_types`
- `entities` (typed, attributes map)
- `relations` (`from`, `to`, `type`, optional attrs)

The model already includes research-relevant entities (e.g., `SourceQuote`, `ThesisSection`, protocol/governance/crisis concepts).

---

## 2) Compatibility policy
1. Existing canonical files remain valid and loadable with no runtime break.
2. New object families are introduced as additive JSON artifacts in workshop/public-data layers.
3. Legacy graph content is preserved under `legacy_canonical` unless explicitly revised.
4. Public layer exports only approved/canonical-ready artifacts.

---

## 3) Status vocabulary

## 3.1 Shared/public statuses
- `legacy_canonical`
- `needs_review`
- `validated`
- `contested`

## 3.2 Workshop-only statuses
- `raw`
- `extracted`
- `linked`
- `published`

## 3.3 Applicability matrix (initial)
- Canonical entity/relation/type: shared/public statuses.
- Working graph object: workshop-only + `needs_review|validated|contested`.
- SourceQuote/Claim/DecisionTrace/ValidationEvent/NarrativePreset/NarrativeStep:
  all statuses allowed; export policy controls public exposure.

---

## 4) New object families (templates)

## 4.1 SourceQuote
```json
{
  "id": "sq-template-0001",
  "quoteText": "Exact quote text.",
  "sourceDocumentId": "doc-thesis-2024",
  "page": "p. 142",
  "chapter": "Chapitre II",
  "section": "II.1",
  "paragraph": "para-03",
  "locator": "pdf://ROLLAND_Mael_These_Complete.pdf#page=142",
  "quoteType": "verbatim",
  "speaker": null,
  "language": "fr",
  "exactnessStatus": "exact",
  "status": "needs_review",
  "provenance": {
    "createdBy": "workshop-agent",
    "createdAt": "2026-04-04T00:00:00Z",
    "method": "manual-extraction",
    "sourceHash": "sha256:..."
  }
}
```

## 4.2 Claim
```json
{
  "id": "claim-template-0001",
  "claimText": "Analytical proposition stated explicitly.",
  "claimType": "interpretive",
  "confidenceLevel": "medium",
  "status": "needs_review",
  "linkedEvidenceIds": ["sq-template-0001"],
  "linkedEntityIds": ["entity-id-placeholder"],
  "provenance": {
    "author": "researcher",
    "createdAt": "2026-04-04T00:00:00Z",
    "method": "close-reading"
  }
}
```

## 4.3 DecisionTrace
```json
{
  "id": "decision-template-0001",
  "decisionText": "Kept legacy section mapping to avoid breaking public narrative continuity.",
  "decisionType": "modeling",
  "author": "research-lead",
  "date": "2026-04-04",
  "rationale": "Preserve existing canonical readability while introducing review statuses.",
  "affectedEntities": ["entity-id-placeholder"],
  "affectedRelations": ["relation-id-placeholder"],
  "affectedFiles": ["grc20-these-mael-rolland-v96.json"],
  "status": "validated"
}
```

## 4.4 ValidationEvent
```json
{
  "id": "validation-template-0001",
  "validator": "editor-01",
  "date": "2026-04-04",
  "scope": "claim:claim-template-0001",
  "result": "approved",
  "comment": "Evidence link and wording are consistent with source quote.",
  "status": "validated"
}
```

## 4.5 NarrativePreset + NarrativeStep
```json
{
  "id": "narrative-template-0001",
  "title": "From Monetary Controversy to Governance",
  "goal": "Explain monétisation as socio-technical process.",
  "targetAudience": "public-academic",
  "orderedStepIds": ["step-template-0001"],
  "viewMode": "guided",
  "evidenceMode": "quoted",
  "status": "needs_review"
}
```

```json
{
  "id": "step-template-0001",
  "headline": "Monetary controversy is an epistemic test",
  "body": "Narrative step body text.",
  "bridgeEntityIds": ["entity-id-placeholder"],
  "anchorQuoteIds": ["sq-template-0001"],
  "graphAction": "focusNodes",
  "order": 1,
  "status": "needs_review"
}
```

---

## 5) Relation extensions (semantic layer)
Planned additive relation types:
- `supportedBy`
- `derivedFrom`
- `validatedBy`
- `contestedBy`
- `decidedIn`
- `includedInNarrative`
- `summarizes`
- `transformsInto`
- `dependsOn`

These can be represented either:
1. as new `relation_types` in the graph, or
2. as object-link fields in workshop artifacts,
then promoted to canonical relation types when stabilized.

---

## 6) Migration rules
1. **No destructive remap** of current `entities`/`relations`.
2. Additive metadata/status overlays should be preferred.
3. Legacy objects missing explicit status are interpreted as `legacy_canonical`.
4. Only statuses `legacy_canonical|validated` are exported by default to public canonical bundles.
5. `contested` may be exported only with explicit policy and annotation.

---

## 7) Export boundary rule (workshop -> public)
- Input: workshop artifacts + canonical baseline.
- Selection:
  - Include baseline canonical objects.
  - Include promoted objects with allowed statuses.
  - Exclude `raw|extracted|linked|needs_review` from default public export.
- Output:
  - static JSON bundle(s) in `public-data/`.

