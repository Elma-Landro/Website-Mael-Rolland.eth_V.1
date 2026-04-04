# workshop/schemas index

This folder contains lightweight schema references for workshop artifacts.

- `status-model.json` — Lists shared/public and workshop-only status vocabularies; **workshop-only for now**; **additive** to canonical graph policy.
- `source-quote.schema.json` — Shape for evidence quote records with provenance/status; **workshop-first for now**; intended to stay **additive** to canonical graph objects.
- `claim.schema.json` — Shape for explicit analytical Claim objects; **workshop-only for now**; intended to be **additive**.
- `decision-trace.schema.json` — Shape for DecisionTrace audit records (why decisions were made); **workshop-only for now**; intended to be **additive**.
- `narrative-preset.schema.json` — Shape for curated narrative preset metadata; **workshop-only for now**; intended to be **additive**.
- `narrative-step.schema.json` — Shape for ordered narrative steps used by presets; **workshop-only for now**; intended to be **additive**.
- `validation-event.schema.json` — Shape for validation logs and review results; **workshop-only for now**; intended to be **additive**.

These schemas do not alter current public runtime behavior in this phase.
