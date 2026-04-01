# Coverage Fidelity Audit — Thesis Architecture vs Graph (v96)

Date: 2026-04-01  
Graph: `grc20-these-mael-rolland-v96.json`  
Stories: `story-presets.mjs`

## Verification protocol (applied)

- **Authority target**: thesis PDF (`assets/pdf/ROLLAND_Mael_These_Complete.pdf` + split chapter PDFs).
- **Search/cross-check support**: extracted thesis corpus in `assets/MD/*.md` (used for fast locating chapter structure and candidate quotes).
- **Operational limitation**: direct PDF text extraction is unavailable in this runtime; page-anchored wording was therefore validated through:
  1) thesis-derived markdown chapter corpus, and  
  2) graph `SourceQuote` entities carrying thesis page metadata.

---


## Coverage balance snapshot (explicit)

- **Well-covered section(s)**: **Chapter I** (infrastructure events and sociohistorical development), **Chapter III** (CVE/The DAO crisis process and actors).
- **Under-modeled section(s)**: **Chapter II** relation spine (monetization + institutionalist chain), **Conclusion** synthesis layer, **Introduction** handoff scaffold.
- **Over-modeled section(s)**: **Chapter III crisis narration** relative to Chapter I/II explanatory sequencing.
- **Concepts present in thesis but weakly represented in graph/story layer**: `Communauté de paiement`, monetization primitives (`usage`, `liquidité`, settlement framing), explicit Intro -> I/II architecture transitions.


## Quantitative evidence snapshot (graph/story)

- Chapter-tagged entities in graph attributes: `I=296`, `II=51`, `III=38`, `Intro=73`, `Conclusion=1`.
- Chapter-tagged `SourceQuote` entities: `I=116`, `II=12`, `III=26`, `Intro=69`, `Conclusion=1`.
- Story focus-node resolution:  
  `monetisation-cryptos 11/23 missing`, `qui-gouverne-reellement 10/15 missing`, `crises 7/15 missing`, `structure-these 10/17 missing`, `fil-de-preuves 4/19 missing`.

These counts support the diagnosis that Chapter II and synthesis layers are narratively weaker and that story coverage quality is constrained by unresolved focus targets.

## Top 5 priority coverage problems (for iterative PRs)

### 1) Story-layer mismatch with graph entities (critical)
**Status type**: **absent from graph (story target labels)** + **present but poorly narrativized**.

- `42` story focus labels do not resolve to existing entity names (e.g., `Monétisation`, `Communauté de paiement`, `Règle`, `Discrétion`, `Bitcoin Core repo`, `Ethereum DAO Hard Fork`).
- By story: `monetisation-cryptos 11/23 missing`, `qui-gouverne-reellement 10/15`, `crises 7/15`, `structure-these 10/17`, `fil-de-preuves 4/19`.
- Impact: chapter I/II concepts exist partially in ontology but are not reliably narratable.

### 2) Chapter II theory chain is weak in graph storytelling
**Status type**: **weakly represented in graph**.

- The thesis’ Chapter II logic (monetary status -> monetization -> institutionalist framework -> rule/discretion) is not represented as a coherent relation/story chain.
- Key missing canonical entity in practice: **`Communauté de paiement`** (used in thesis logic and story text, unresolved as focus node).

### 3) Crisis narrative over-weighting vs thesis balance
**Status type**: **over-emphasized relative to thesis**.

- Story design foregrounds Chapter III crisis dramatization while Introduction/Chapter I/Chapter II explanatory infrastructure is less sequentially explicit.
- Net effect: users can enter “crisis-first” interpretation without passing through infrastructure + monetization theory scaffolding.

### 4) Introduction is concept-rich but scaffold-poor
**Status type**: **present but poorly narrativized**.

- Intro motifs (syllogisme libéral-techniciste, rule/discretion framing, case selection) are present in quotes/entities.
- Missing explicit intro relations that hand off to Chapters I and II before Chapter III.

### 5) Conclusion synthesis is under-modeled
**Status type**: **under-modeled**.

- Conclusion appears mostly as isolated quote-level representation rather than a synthesis subgraph joining I+II+III outputs.

---

## Diagnostic by major thesis section

## A. Introduction

### Current graph strengths
- Rule/discretion framing present through quote entities.
- Case-selection bridge to Chapter III present.

### Missing entities
- Canonical node: `Communauté de paiement` (intro/II bridge usage).
- Intro-level node for “thesis architecture handoff” (Intro -> Ch I -> Ch II -> Ch III).

### Missing relations
- `Introduction -> frames -> Chapitre I`.
- `Introduction -> frames -> Chapitre II`.
- `Syllogisme libéral-techniciste -> tested by -> infrastructure evidence + monetary institutionalism + crises`.

### Missing stories
- 1 short intro story that ends in explicit branch to Chapter I and Chapter II before crisis exploration.

### Recommended visualization focus
- “Intro scaffold lane” (3 cards): problematization / theoretical apparatus / chapter pathway.

### Supporting thesis references
- chapterOrSection: **Introduction générale**.  
  page: **34**.  
  SourceQuote: “**le bogue CVE 2018 #17144 pour Bitcoin et la crise ouverte par l'attaque de « The DAO »**”.
- chapterOrSection: **Introduction**.  
  page: **25**.  
  SourceQuote: “**un espace controversé entre la « Règle » (...) et la « Discrétion »**”.

## B. Chapter I — sociotechnical infrastructures / Bitcoin-Ethereum development

### Current graph strengths
- High graph density on infrastructure events, actors, and development episodes.
- Strong modeling of Bitcoin sociohistorical construction.

### Missing entities
- Canonical story-safe nodes for: maintenance work, off-chain infrastructuralization, re-intermediation sequence.

### Missing relations
- `Infrastructure development -> conditions -> monetization` (forward link to Chapter II).
- `Maintenance practices -> sustain -> governance capacity`.

### Missing stories
- A Chapter I-native narrative path (protocol design -> infrastructural expansion -> governance implications).

### Recommended visualization focus
- Phase timeline (proof of concept -> maturation -> institutionalization) with visible Chapter II outgoing links.

### Supporting thesis references
- chapterOrSection: **Chapitre I**.  
  page: **54**.  
  SourceQuote: “**les CM sont des infrastructures sociotechniques dont les formes et contenus incorporent des a priori sociaux et politiques**”.
- chapterOrSection: **Chapitre I**.  
  page range (MD indicators): around infrastructure-development sections.  
  SourceQuote: “**Un nu protocole ne fait pas monnaie**”.

## C. Chapter II — monetary status, monetization, institutionalist theory, rule vs discretion

### Current graph strengths
- Institutionalism/rule-discretion references exist in ontology.
- Monetary references (IFM, nominalisme non étatiste, Currency/Banking School) are present.

### Missing entities
- **Absent canonical label**: `Communauté de paiement`.
- Weak explicit nodes for monetization primitives as first-class chain: usage, liquidity, commensurability, settlement.

### Missing relations
- `Monetization -> depends on -> usages`.
- `Monetization -> depends on -> institutions`.
- `Monetization -> depends on -> communauté de paiement`.
- `Chapitre I findings -> support -> Chapitre II monetary-status claim`.

### Missing stories
- 1 Chapter II theory-first story from critique of status theories to institutionalist monetization demonstration.

### Recommended visualization focus
- Make “Monetization Matrix” the default pre-crisis interpretive path.

### Supporting thesis references
- chapterOrSection: **Chapitre II** (opening framing).  
  page: **142**.  
  SourceQuote: “**Dépasser la controverse du statut monétaire des CM par un institutionnalisme intéressé aux usages**”.
- chapterOrSection: **Chapitre II** (functionalist controversy baseline).  
  page: **144**.  
  SourceQuote: “**unité de compte, réserve de valeur, moyen d'échange**” (triptyque fonctionnel).
- chapterOrSection: **Chapitre II** (money as explicitation test).  
  page: **50** (quote anchor).  
  SourceQuote: “**Les CM représentent une épreuve d’explicitation de la monnaie**”.
- chapterOrSection: **Chapitre II** (rule/discretion framing in thesis architecture).  
  page range (ToC markers): **62 / 64**.


## D. Chapter III — crises and dual/polycentric governance

### Current graph strengths
- Strong coverage of CVE-2018-17144 and The DAO.
- Crisis process and actor-governance contrasts are well represented.

### Missing entities
- Comparative bridge entities linking Chapter III findings back to Chapter II theory terms.

### Missing relations
- `Crisis governance (huis clos/public) -> reveals -> ordinary governance`.
- `Crisis evidence -> requalifies -> rule/discretion claims`.

### Missing stories
- A dual-case comparative story that ends with explicit feedback links to Chapter II and Conclusion.

### Recommended visualization focus
- Keep crisis story but force a “theory feedback” final step.

### Supporting thesis references
- chapterOrSection: **Chapitre III** (chapter framing and section plan).  
  SourceQuote: “**mise en crise et de la remise en ordre**”.  
  page: **p. 290 (PDF p.291/455)**.
- chapterOrSection: **Chapitre III**.  
  SourceQuote: governance in two faces (huis clos vs publique) (chapter framing passages).

## E. Conclusion

### Current graph strengths
- Polycentric/conflictual governance thesis appears explicitly in quote layer.

### Missing entities
- Final synthesis nodes that explicitly join infrastructure + monetization + crisis-governance results.

### Missing relations
- `Chapitre I + Chapitre II + Chapitre III -> supports -> final thesis claim`.

### Missing stories
- 1 short conclusion synthesis story (4 steps max).

### Recommended visualization focus
- Dedicated synthesis panel, not only crisis endpoints.

### Supporting thesis references
- chapterOrSection: **Conclusion générale**.  
  page: **336**.  
  SourceQuote: “**la gouvernance sur l’infrastructure des CM est conflictuelle et polycentrique**”.

---

## Coverage classification (explicit)

### Absent from the graph
- Canonical story-resolvable node: `Communauté de paiement`.
- Multiple story focus labels unresolved against entity namespace.

### Weakly represented in the graph
- Chapter II monetization relation spine.
- Intro -> I/II pathway relations.
- Conclusion synthesis relation layer.

### Present but poorly narrativized
- Chapter I infrastructural argument chain.
- Introduction architecture and method bridge.
- Rule/discretion theory as narrative sequence.

### Over-emphasized relative to thesis
- Chapter III crises in story-layer attention compared with Chapter I/II preconditions and monetary theory.

---

## Deferred queue (later iterations)

1. Canonicalize story focus labels to existing entity IDs/names (remove unresolved focus nodes).
2. Add Intro scaffold relation bundle (Intro -> I -> II -> III).
3. Add Chapter II monetization spine (usage/liquidity/payment community/institutions).
4. Add Chapter III -> Chapter II theory-feedback relations.
5. Add compact Conclusion synthesis subgraph + short synthesis story.
6. Add chapter-balance KPI checks in CI (entity/relations/story-step parity).
