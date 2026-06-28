# Agent Creation Rules

This document defines the criteria for creating, refusing and deferring agents in the GRC-20 project. It is the gatekeeping mechanism for the agent organisation described in [README.md](README.md).

---

## Criteria for creating a new agent

An agent may be created only when **all** of the following conditions are met:

1. **Observed pain.** A specific, recurring need has been encountered at least twice and documented (in an audit, a session, a bug report, or a repeated manual workaround). Theoretical elegance is not sufficient.

2. **No existing agent covers it.** No current agent (Hermes, Codex) can address the need within its current mission and perimeter without distortion or scope creep.

3. **Distinct competence.** The agent's mission is sufficiently distinct from existing agents that merging it would create an unfocused hybrid. A specialised agent must be better at one thing than a generalist.

4. **Evidence of value.** Creating the agent would measurably improve: evidence fidelity, schema safety, traceability, or human time saved. The improvement must be articulable, not speculative.

5. **Genealogy recorded.** The agent's file documents why it exists: what pain, what audit, what friction motivated its creation.

6. **Human validation.** Maël Rolland approves the creation and reviews the agent specification before it is activated.

### Creation checklist

- [ ] Pain documented (reference to audit, session, or bug report)
- [ ] No existing agent covers the need
- [ ] Mission distinct from Hermes and Codex
- [ ] Perimeter, forbidden perimeter, interfaces, metrics defined
- [ ] Genealogy written
- [ ] Human validation obtained

---

## Criteria for refusing a new agent

An agent proposal should be **refused** if any of the following apply:

1. **No observed pain.** The agent solves a problem that has not been encountered. It exists to fill an ideal organigram rather than a real need.

2. **Covered by an existing agent.** Hermes or Codex already handles the task within their current perimeters, or could do so with a minor perimeter extension.

3. **Speculative enrichment.** The agent's value is theoretical rather than measured.

4. **Maintenance cost exceeds value.** An agent that runs continuously on a stable, low-activity repository produces either silence or noise. The cost of maintaining it outweighs its benefit.

5. **Unclear mission.** If the agent's mission cannot be stated in one sentence, it is not ready to be created.

6. **Propagation risk.** The agent would consume unvalidated outputs from other agents as facts, creating an error-propagation chain.

---

## Mandatory rules

### Rule of genealogy

Every agent file must include a **Genealogy** section explaining why the agent exists. Acceptable genealogies reference:

- a specific audit that revealed a recurring need;
- a repeated manual workaround that became intractable;
- a measured bottleneck (time, error rate, coverage gap);
- a structural debt documented in `docs/` or in a project-state reference.

Unacceptable genealogies:

- "It would be logical to have one."
- "The organigram suggests it."
- "Other projects have one."

### Rule of human validation

- An agent may **propose** a modification to its own prompt, mission, or the charter.
- An agent may **never apply** that modification itself.
- All changes to agent specifications must be validated by a human (Maël Rolland).

This transposes Mode B to Mode C at the organisational level: proposal is always separated from application.

### Rule against error propagation

Any output produced by one agent and consumed by another remains **annotated as data, not as fact**, until validated by a human. Concretely:

- If Agent A produces a conclusion, and Agent B uses it as input, Agent B must treat it as an unverified assertion.
- Agent B's output that depends on Agent A's unverified conclusion must carry the `[UNVERIFIED]` flag inherited from the source.
- The system must never allow an unverified conclusion to dissolve into the graph as if it were a fact.

Without this rule, the multi-agent system degrades into traceable automated rumour.

---

## Deferred candidates

The following agents are candidates for future creation. None is active today. For each: its potential function, the pain that would justify its creation, and the reason it is deferred.

### Evidence

- **Potential function.** Verify that every entity description, relation, and quote in the graph is faithful to the thesis text. Cross-reference chapter/section/page citations against the PDF.
- **Pain that would justify creation.** Recurring manual cross-checking between graph claims and thesis passages; discovery of `[UNVERIFIED]` claims that accumulate without resolution; description drift after multiple patch rounds.
- **Why deferred.** Hermes already performs evidence verification as part of its audit mission (Mode A). A dedicated Evidence agent becomes justified only when the volume of evidence checks exceeds what Hermes can handle within a session, or when a systematic coverage audit (e.g. Mission 006: Coverage and Evidence Audit v2) reveals a persistent gap that warrants continuous monitoring.

### Schema

- **Potential function.** Validate JSON structure, ID format (base58 where required), relation-type vocabulary compliance, duplicate detection, orphan detection, endpoint resolution.
- **Pain that would justify creation.** Recurring schema violations introduced by patches; relation types used outside the vocabulary; ID format drift.
- **Why deferred.** The deterministic audit script (`scripts/audit_graph.py`) already performs structural validation. A dedicated Schema agent becomes justified only when schema violations become frequent enough that running the script reactively is insufficient, or when the schema itself evolves and requires continuous compliance checking during a transition.

### Aeon

- **Potential function.** Event-driven surveillance of the GitHub repository: trigger audits on PR opening, on commits touching the graph JSON, or on schema changes; detect regressions; open issues automatically.
- **Pain that would justify creation.** Regressions introduced by merged PRs that are discovered late; lack of continuous integrity checking between audit campaigns.
- **Why deferred.** The GRC-20 repository has an irregular commit rhythm driven by decisions, not a daily software development cadence. A continuous audit on a quasi-stable repository produces either silence or noise. Aeon should be calibrated on **events** (PR opened, graph-touched commit), not on a clock. It becomes justified when the repository reaches a commit frequency and PR throughput that makes manual review the bottleneck.

### Story

- **Potential function.** Validate that all focusNodes resolve, that narrative paths are coherent, and that the story runtime (`graphe.html`) renders correctly.
- **Pain that would justify creation.** Broken focusNodes, dead narrative paths, rendering regressions after graph patches.
- **Why deferred.** Audits have shown that all focusNodes currently resolve. The story runtime is stable. A dedicated Story agent becomes justified only when story-related patches become frequent or when a narrative restructuring introduces regression risk.

### Visual

- **Potential function.** Validate the visualisation layer: graph layout, panel rendering, interactive features, performance on large graphs.
- **Pain that would justify creation.** Rendering bugs, layout regressions, performance degradation after entity/relation additions.
- **Why deferred.** No visualisation regression has been observed or documented. The visualisation layer is stable. A dedicated Visual agent becomes justified only when the frontend undergoes active redesign or when graph growth causes measurable performance issues.

### Ontology

- **Potential function.** Check conceptual coherence: relation-type semantics, entity typing consistency, absence of conceptual duplication, taxonomy discipline.
- **Pain that would justify creation.** Conceptual drift (entities that should be typed differently); relation-type misuse (a relation used to express something its semantics do not support); taxonomy pollution.
- **Why deferred.** Ontological analysis is currently performed by Hermes as part of deep audits. A dedicated Ontology agent becomes justified only when the relation-type vocabulary grows, when `schema-vnext` introduces new types, or when conceptual conflicts are observed repeatedly.

### Publisher

- **Potential function.** Prepare exports: GeoJSON, static snapshots, publication-ready graph versions, companion data files.
- **Pain that would justify creation.** Repeated manual export preparation; inconsistency between published versions and the active graph; need for automated, reproducible export pipelines.
- **Why deferred.** No publication or export workflow is currently active or scheduled. A dedicated Publisher agent becomes justified only when the graph reaches a publication milestone and reproducible exports become a recurring need.
