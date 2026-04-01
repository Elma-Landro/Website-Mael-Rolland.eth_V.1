# Thesis Story-System Audit (Graph Interface)

Date: 2026-04-01  
Scope: `story-presets.mjs` + `narrative-anchors.json` vs thesis architecture (Intro, I, II, III, Conclusion).

## Verification protocol
- Primary reference target: thesis PDF (`assets/pdf/ROLLAND_Mael_These_Complete.pdf`, split chapter PDFs).
- Fast cross-check: extracted corpus `assets/MD/*.md`.
- Anchor evidence: `narrative-anchors.json` (115 anchors with chapter/page/quoteText).
- Runtime limitation: direct PDF text extraction is unavailable in this environment; references below rely on page-tagged anchor quotes + extracted corpus cross-check.

---

## Existing story presets — teaser vs robust

### Story robustness criteria used
- **Robust**: >=5 steps, >=70% focus nodes resolvable, >=2 chapter transitions, >=2 source-anchored steps.
- **Teaser-level**: <5 steps OR >30% unresolved focus nodes OR mostly slogan-level abstractions.

### Classification of current presets
1. `fil-de-preuves` -> **Most robust current story** (6 steps, 15/19 nodes resolved, 6 source-anchored steps).
2. `crises` -> **Robust for Chapter III only** (4 steps, strong crisis arc, but thesis-wide balance weak).
3. `monetisation-cryptos` -> **Teaser-level** (11/23 unresolved focus nodes).
4. `qui-gouverne-reellement` -> **Teaser-level** (10/15 unresolved focus nodes, conceptual but under-grounded in nodes).
5. `structure-these` -> **Teaser-level** (10/17 unresolved focus nodes; good intent, weak node anchoring).

### Quantitative evidence
- Story focus-node missingness: monetisation `11/23`, qui-gouverne `10/15`, crises `7/15`, structure-these `10/17`, fil-de-preuves `4/19`.
- Crisis-intensity (step text/focus scan): crises `4/4`, structure-these `1/4`, fil-de-preuves `3/6`, vs monetisation `0/5`, qui-gouverne `0/4`.
- Anchor underuse: only a small subset of available anchors is currently used by story steps.

---

## Top 5 priority story improvements (small PR batches)

### P1 — Canonicalize story focus nodes before adding new arcs
- Problem: unresolved focus nodes block narrativity and trust.
- Action: normalize preset focus labels to canonical entity IDs/names.
- Batch size: 1 PR, no new ontology.

### P2 — Promote one thesis backbone story (not crisis-first)
- Problem: users can enter via crisis drama without reading the argument chain.
- Action: create a backbone story ordered Intro -> I -> II -> III -> Conclusion.
- Batch size: 1 PR, 7–8 steps, anchor-backed.

### P3 — Upgrade Chapter II from teaser to robust
- Problem: monetization/institutionalist logic is central in thesis but underpowered in stories.
- Action: add a dedicated Chapter II story family (uses/payment community/rule-discretion).
- Batch size: 1 PR, 6 steps.

### P4 — Split governance story into ordinary vs crisis governance
- Problem: governance-by/governance-over and closed-door/public governance are conflated.
- Action: two linked stories with explicit transition edge.
- Batch size: 1 PR, 4 + 4 steps.

### P5 — Add methodological inquiry story (currently missing)
- Problem: thesis method and fieldwork architecture are barely narrativized.
- Action: 4-step method story (terrain access, materials, emic/etic tension, evidentiary method).
- Batch size: 1 PR, 4 steps.

---

## Proposed complete story architecture (thesis-legibility-first)

## Arc 0 — Thesis Backbone (new default)
**Purpose**: make argument legible before case drama.

Step order:
1) Problematisation (liberal-technicist syllogism).  
2) Infrastructure claim (bare protocol != money).  
3) Carnavalesque phased development (Bitcoin -> Ethereum differentiations).  
4) Monetization via uses/payment communities.  
5) Rule vs discretion reframing.  
6) Governance by vs over protocol.  
7) Crisis contrast (CVE vs DAO).  
8) Polycentric conclusion.

Core focus nodes:
`Syllogisme libéral-techniciste`, `Infrastructure sociotechnique`, `Développement carnavalesque`, `Monétisation`, `Communauté de paiement` (to add), `Règle contre discrétion`, `Gouvernance duale`, `Gouvernance polycentrique`, `Bitcoin CVE 2018-17144`, `The DAO`.

Transition policy:
- hard transition Intro->I and I->II required;
- III only after II step completion.

Evidence anchors:
- I p.53 (syllogism), I p.54 (infrastructure), II p.50 (explicitation), III p.225/p.234, Conclusion p.336.

## Arc 1 — Liberal-technicist syllogism (mandatory family)
Status: **partly present**, needs expansion.

Steps:
1) Syllogism statement.  
2) Why it is attractive (neutrality promise).  
3) Where it fails empirically (infra complexity + governance).

Focus nodes:
`Syllogisme libéral-techniciste`, `Neutralité technique`, `Absence de gouvernance`, `Gouvernance duale`.

UX recommendations:
- Use “claim -> test -> falsification” card framing.

References:
- chapterOrSection: Chapitre I, p.53.  
  SourceQuote: “... syllogisme ... « libéral-techniciste » ...”.

## Arc 2 — A bare protocol does not make money (mandatory family)
Status: **weakly represented**.

Steps:
1) Protocol design baseline.  
2) Necessary off-chain complements.  
3) Why monetary status requires social/institutional uptake.

Focus nodes:
`Bitcoin`, `Ethereum`, `Infrastructure sociotechnique (CM)`, `Passerelles fiat`, `Portefeuilles`, `Usages`.

UX recommendations:
- Layered view toggle: protocol layer / infrastructure layer / monetary-use layer.

References:
- chapterOrSection: Chapitre I, p.54.  
  SourceQuote: “les CM sont des infrastructures sociotechniques...”.
- chapterOrSection: Chapitre I (infra sections).  
  SourceQuote: “Un nu protocole ne fait pas monnaie”.

## Arc 3 — Bitcoin carnavalesque infrastructural development by phases (mandatory family)
Status: **present but fragmented**.

Steps:
1) Proof-of-concept phase.  
2) Maturation/reintermediation phase.  
3) Institutionalization and scaling conflicts.  
4) Ethereum divergence.

Focus nodes:
`Preuve de concept / Phase 1 Bitcoin`, `Phase de maturation / Phase 3 Bitcoin`, `Développement carnavalesque`, `Bitcoin Scaling Debate`, `Ethereum`.

UX recommendations:
- timeline-first with event density controls.

References:
- chapterOrSection: Chapitre I (phase sections).  
  page markers around p.54 and later phase sections.

## Arc 4 — Monetization through uses and payment communities (mandatory family)
Status: **under-modeled**.

Steps:
1) Status controversy baseline.  
2) Institutionalist pivot to uses.  
3) Payment community concept.  
4) Monetization indicators in practice.

Focus nodes:
`Statut monétaire des cryptomonnaies`, `Institutionnalisme intéressé aux usages`, `Monétisation`, `Communauté de paiement` (to add), `Usage en paiement`.

UX recommendations:
- matrix cards: emission / circulation / access / usage / stabilization.

References:
- chapterOrSection: Chapitre II, p.142.  
  SourceQuote: “Dépasser la controverse ... institutionnalisme intéressé aux usages”.
- chapterOrSection: Chapitre II, p.144.  
  SourceQuote: “unité de compte, réserve de valeur, moyen d’échange”.

## Arc 5 — Rule versus discretion (mandatory family)
Status: **present, poorly narrativized**.

Steps:
1) Classical controversy.  
2) Crypto radicalization of rule.  
3) Empirical return of discretion.

Focus nodes:
`Règle contre la discrétion`, `Currency School`, `Banking School`, `Consensus social (discrétion)`, `Gouvernance de crise`.

UX recommendations:
- side-by-side dual panel with synchronized examples.

References:
- chapterOrSection: Introduction / Chapitre II.  
  pages: 25 (intro quote), 62/64 (Chapter II sections).

## Arc 6 — Governance by vs over protocol (mandatory family)
Status: **partly represented**.

Steps:
1) Governance by protocol rules.  
2) Governance over protocol by actors/processes.  
3) Tensions and legitimacy.

Focus nodes:
`Gouvernance par l’infrastructure`, `Gouvernance sur l’infrastructure`, `Core Developers`, `Repo/PR process`, `Arènes de gouvernance`.

UX recommendations:
- always show relation legend separating by/over edges.

References:
- chapterOrSection: Intro + II + III connective argument.

## Arc 7 — Closed-door governance vs public governance (mandatory family)
Status: **present in Chapter III, needs explicit contrast story**.

Steps:
1) Closed-door governance pattern (CVE).  
2) Public governance pattern (DAO/fork controversy).  
3) Comparison and limits.

Focus nodes:
`CVE-2018-17144 (gouvernance de huis clos)`, `Divulgation responsable`, `The DAO`, `Hard Fork`, `Ethereum Classic`.

UX recommendations:
- mirrored layout (left: huis clos, right: public conflict).

References:
- chapterOrSection: Chapitre III, p.225 / p.234 / p.290.
- SourceQuote: “résolution silencieuse... off chain”, “divulgation responsable...”, “mise en crise ... remise en ordre”.

## Arc 8 — DAO and CVE as contrasted revelations (mandatory family)
Status: **robust candidate, currently partial**.

Steps:
1) CVE path (non-activation + confidentiality).  
2) DAO path (public conflict + fork).  
3) What each reveals about governance form.

Focus nodes:
`Bitcoin CVE 2018-17144`, `The DAO`, `Gouvernance duale`, `Gouvernance polycentrique`.

UX recommendations:
- comparison cards with same rubric (actors, devices, arenas, consensus mode).

References:
- chapterOrSection: Chapitre III; Conclusion p.336.

## Arc 9 — Who governs really? actors + devices + arenas (mandatory family)
Status: **teaser-level currently**.

Steps:
1) Actor categories.  
2) Devices (repo, clients, disclosure channels).  
3) Arenas (mailing lists, meetings, forums).  
4) Decision effects.

Focus nodes:
`Core Developers`, `Mainteneurs`, `GitHub Bitcoin Core`, `Bitcoin-dev Mailing List`, `All Core Dev Meetings`, `Carbon Vote`.

UX recommendations:
- tri-column lens: Actors / Devices / Arenas.

References:
- chapterOrSection: Chapitre III governance sections and crisis process sections.

## Arc 10 — Methodological story of the inquiry (mandatory family)
Status: **missing**.

Steps:
1) Why ethnography was required.  
2) Access strategy (online/offline + documents + immersion).  
3) Material corpus and triangulation.  
4) Positioning and limits.

Focus nodes:
`Démarche ethnographique`, `Immersion participante`, `Entretiens`, `Corpus documentaire`, `Stratégie d’accès`.

UX recommendations:
- include confidence badges (direct quote / inferred synthesis).

References:
- chapterOrSection: Introduction methodology subsections (page markers around 27/34/41).

---

## Current weaknesses summary
- Too many unresolved story focus nodes (core blocker).
- Chapter II story family remains thesis-central but graph-story peripheral.
- Governance stories over-index on crises without enough ordinary-governance bridge.
- No dedicated method story despite thesis methodological weight.
- Conclusion synthesis is not enacted as a narrative endpoint.

---

## Deferred queue (after top-5)
1. Add bilingual story labels/framing consistency pass.
2. Add mobile-optimized condensed story mode (3-step per arc).
3. Add “evidence mode” toggle showing anchor quote snippets per step.
4. Add story analytics hooks (drop-off by step, skipped transitions).
5. Add advanced comparative arc: Bitcoin vs Ethereum governance evolution over time.

---

## Inference markings
- Proposed Arc 10 (method story) is **strongly supported** by intro methodology sections but currently under-anchored in story presets.
- Some node names in proposed lists are **implementation inferences** where canonical labels are currently unresolved; these should be validated against entity namespace during implementation.
