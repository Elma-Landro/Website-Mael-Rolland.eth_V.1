# GRC-20 Agents Charter

## Purpose

This directory documents the **roles, permissions and genealogy** of the software agents that operate on the GRC-20 knowledge graph project. These agents are collaborators with narrowly defined responsibilities, not scientific authorities.

The project is a scientific object (a doctoral thesis rendered as a traceable knowledge graph), not a conventional software repository. **Traceability and evidence integrity outrank speed and coverage.** Agents make the work more systematic, more reproducible and more auditable; they do not replace the researcher's judgment.

## Guiding principle

> An agent is a **role of work**, not a **scientific authority**.

Scientific authority remains with Maël Rolland (thesis author). Agents extend his reach; they do not inherit his arbitrage.

## Modes of intervention

Every agent action falls into one of three modes, inherited from the graph-maintenance discipline:

| Mode | Name | What the agent does | What the agent does **not** do |
|------|------|---------------------|--------------------------------|
| **A** | Audit | Reads files, inspects structure, compares graph claims to thesis evidence, produces a Markdown report. | Does not modify the graph, the runtime, or any repository file. |
| **B** | Proposal | Proposes changes with evidence, risks and expected impact. | Does not modify files. |
| **C** | Patch / PR | Creates a branch, applies minimal verified changes, validates, writes a changelog, prepares a commit/PR. | Never overwrites the active graph file; never merges without human review. |

When the mode is ambiguous, the agent defaults to **Mode A (audit only)**.

## Authority model

- **Maël Rolland** is the final scientific arbiter. He validates evidence, resolves interpretive conflicts, and authorises schema changes, entity merges, entity deletions and ID renames.
- **Agents** execute bounded missions under explicit constraints. They can audit, propose, and (when authorised) apply minimal patches. They cannot unilaterally change the schema or the scientific direction of the project.
- No agent has the authority to merge its own PR. Every PR targets the repository default branch and is opened for human review.

## Rules

### Rule 1 — No agent without observed pain

An agent exists to address a **recurring, measured need** — a "pain" that has actually been encountered in the project. Agents are not created from an ideal organigram or a theoretical division of labour. A candidate agent that has no documented pain justifying its creation remains deferred.

This mirrors the graph discipline: *no entity without a relation that has been observed.* Agents obey the same conservatism.

### Rule 2 — Proposal ≠ application

An agent may **propose** a modification to its own prompt, its mission, or the charter. It may **never apply** that modification itself. All changes to agent specifications must be validated by a human.

This is the direct transposition of Mode B → Mode C at the organisational level.

### Rule 3 — Data is not fact (anti error-propagation)

Any output produced by one agent and consumed by another remains **annotated as data, not as fact**, until validated by a human. An unverified agent conclusion must not silently become the premise of another agent's reasoning. Otherwise the system degrades into traceable automated rumour.

### Rule 4 — Genealogy is mandatory

Every agent file must record *why* this agent exists: what audit, what repeated task, what observed friction motivated its creation. Without genealogy, the organisation is merely a description — not a reconstructible process.

## Current agents

| Agent | File | Status |
|-------|------|--------|
| Hermes (GRC-20 orchestrator) | [`Hermes.md`](Hermes.md) | Active |
| Codex (code/patch executor) | [`Codex.md`](Codex.md) | Active |

## Deferred candidates

The following agents are **not yet active**. Each has a plausible function, but none has a measured pain justifying creation today. They are listed in [`Agent_Creation_Rules.md`](Agent_Creation_Rules.md) with their potential function, the pain that would justify them, and the reason they are deferred.

- **Evidence** — verifies thesis fidelity
- **Schema** — validates JSON / GRC-20 schema compliance
- **Aeon** — event-driven GitHub surveillance
- **Story** — validates narrative runtime
- **Visual** — validates visualisation layer
- **Ontology** — checks conceptual coherence
- **Publisher** — prepares exports

## Reflexive note

The architecture described here — specialised agents with delimited scope, a hard boundary between proposal and execution, final human arbitrage, and full traceability of decisions — is an operational formalisation of **polycentric governance** (Ostrom) applied to a knowledge infrastructure. The method by which this graph is constructed *incarnates* the theoretical object of the thesis. Documenting the agents, their rules and their genealogy makes visible the distributed production of knowledge — not just the result.
