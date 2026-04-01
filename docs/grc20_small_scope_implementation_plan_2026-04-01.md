# GRC20 Small-Scope Implementation Plan (from existing audits only)

Inputs used:
- `docs/grc20_story_system_audit_2026-04-01.md`
- `docs/grc20_coverage_fidelity_audit_2026-04-01.md`

Scope policy:
- Implementation mode only (no re-audit).
- Single-PR-sized batches.
- Derived strictly from already identified findings.

---

## Batch 1 — Canonicalize story focus nodes (highest-value unblocker)

### Exact objective
Resolve unresolved story focus labels in current presets so steps reliably target existing graph entities (especially `monetisation-cryptos`, `qui-gouverne-reellement`, `structure-these`).

### Files likely to change
- `story-presets.mjs` (focus node names/IDs normalization)
- `grc20-these-mael-rolland-v96.json` (only if a minimal alias/canonical entity is required for strict mapping)
- `docs/grc20_story_system_audit_2026-04-01.md` (optional short “implemented” note)

### Expected impact
- Immediate story reliability increase (fewer empty/partial steps).
- Enables later story architecture work without UX dead-ends.
- Directly addresses the largest measured blocker from both audits.

### Risk level
**Low** (mostly label-mapping and validation; minimal ontology change).

---

## Batch 2 — Add a compact Thesis Backbone story (Intro -> I -> II -> III -> Conclusion)

### Exact objective
Introduce one default thesis-legibility narrative path (7–8 steps) that prevents crisis-first misreading and enforces chapter order.

### Files likely to change
- `story-presets.mjs` (new `thesis-backbone` story + step transitions)
- `narrative-anchors.json` (attach existing anchors to each backbone step)
- `graphe.html` / story UI config consumer files (only if selector/default story wiring is needed)

### Expected impact
- Stronger argument legibility for first-time users.
- Rebalances chapter sequencing without large ontology edits.
- Makes existing anchor set more visible and useful.

### Risk level
**Medium** (requires careful step design and anchor-step fit; minor UI wiring risk).

---

## Batch 3 — Chapter II monetization spine (minimal narrative + relation support)

### Exact objective
Implement the smallest Chapter II upgrade identified by audits: a dedicated story slice for monetization-through-uses and payment-community logic, with minimal relation reinforcement.

### Files likely to change
- `story-presets.mjs` (new or expanded Chapter II story)
- `grc20-these-mael-rolland-v96.json` (minimal additions for missing canonical node(s), especially `Communauté de paiement`, plus a few relations)
- `section_entities_map.json` / `entity_section_map.json` (only if section anchoring metadata must be aligned)

### Expected impact
- Addresses the most important under-modeled thesis area (Chapter II).
- Improves theoretical continuity between Chapter I infrastructure and Chapter III crises.

### Risk level
**Medium-High** (touches ontology + relations; risk of over-expansion if not tightly scoped).

---

## Recommended first batch
**Implement Batch 1 first**.

Reason: it is the smallest, lowest-risk, highest-leverage unblocker and is a prerequisite for credible evaluation of any subsequent story-architecture improvements.
