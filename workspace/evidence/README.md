# workspace/evidence/ — Working Evidence Objects

This directory holds working evidence objects and sample templates.

## What is an evidence object?

Evidence objects are workspace-layer records that document **why a graph entity, relation, or claim exists**.
They are distinct from `SourceQuote` entities in the canonical graph: evidence objects here may be
pre-validation candidates, enriched metadata records, or analytical annotations not yet promoted to the graph.

## Relationship to canonical SourceQuote entities

The canonical graph (`grc20-these-mael-rolland-v96.json`) already contains **245 SourceQuote entities**
with fields: `quoteText`, `page`, `chapter`, `thesisLocation`, `language`, `sourceFormat`, `evidenceStatus`.

Working evidence objects in this directory are:
- Pre-publication candidates awaiting review
- Enriched versions of existing SourceQuote entities (e.g., adding `sectionKey` or `exactnessStatus`)
- Cross-references not yet incorporated into the graph

## Directory layout

- `samples/` — Template JSON files showing the expected structure of each evidence type

## Status lifecycle for evidence objects

```
raw → extracted → linked → needs_review → validated → published
```

Once validated, evidence objects are promoted to the canonical graph as SourceQuote entities via a versioned patch.

## Gaps in current SourceQuote coverage (from evidence audit, 2026-04-01)

The evidence audit (`docs/grc20_evidence_audit.md`) identifies the following areas needing additional quotes:
- Gouvernance polycentrique (II.3)
- Clarification stakeholders/shareholders
- Articulation règle/discrétion
- Comparaison CVE (huis clos) vs DAO (public)

See `docs/grc20_coverage_fidelity_audit_2026-04-01.md` for detailed coverage analysis.
