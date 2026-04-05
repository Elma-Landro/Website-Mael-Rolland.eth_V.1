# Story Boundary Plan

**Branch:** `feat/research-architecture-vnext-story-boundary-plan`  
**Date:** 2026-04-05  
**Depends on:** `STORY_CROSS_CALL_AUDIT.md`  
**Scope:** Planning and sequencing only (no runtime implementation in this branch).

---

## 1. Current StoryMode responsibility zones

Story-related behavior is currently split across StoryMode IIFE and adjacent scrolly/orchestration functions in `graphe.html`.

### Zone A — Story registry loading and story selection
- `loadRegistry()` dynamic import of `story-presets.mjs`.
- `renderStorySelect()`, `inferStoryIdFromView()`.
- `storyRegistry` shape assumptions (`stories`, `viewToStoryId`).

### Zone B — Focus target resolution and alias normalization
- `normalizeText`, `STORY_FOCUS_ALIASES`, `resolveFocusNodes()`.
- Name/ID fallback logic and ambiguity handling.

### Zone C — Story focus engine (graph classing + camera)
- `buildStoryFocusOptions`, `collectSecondaryNodes`, `applyStoryFocus`, `clearStoryFocus`.
- Responsible for node/edge class assignment and camera fit/zoom.

### Zone D — Runtime step state machine
- `storyState`, `applyStoryStep`, `goToStoryStep`, `nextStoryStep`, `prevStoryStep`, `toggleStoryReveal`.
- Tracks phase and expanded edges/nodes.

### Zone E — Expansion behavior
- `maybeExpandFromNode` (invoked by Graph node select callback).

### Zone F — Story panel rendering and controls
- `updateStoryPanel` and button/select listeners in `init`.
- Citation and bridge hint rendering.

### Zone G — Mode coordination
- `leaveScrollyIfNeeded`, `openStory`, `closeStory`, `maybeSwitchLayout`.
- Coordinates with layout select and scrolly mode.

### Zone H (adjacent, not in StoryMode IIFE) — Anchored scrolly bridge
- `initAnchoredScrolly`, `initScrollyObserver`, `highlightByChapter/Section/Types` in DOMContentLoaded block.
- This zone can trigger `StoryMode.applyStoryFocus` for anchor scenes.

---

## 2. Proposed conceptual sub-zones for future extraction

These are conceptual boundaries first, not immediate file moves.

1. **Story registry / data-loading zone**
   - Dynamic import + registry validation + story/view lookup.
2. **Alias resolution zone**
   - Text normalization and alias/canonical ID resolution.
3. **Focus/selection logic zone**
   - Option building, target classification, expansion sets.
4. **Graph interaction hooks zone**
   - Thin adapter layer for graph commands (`getCy`, `fit`, `layout`).
5. **DOM section lookup / scroll targeting zone**
   - Anchor section insertion, chapter lookup, deep-link anchor routing.
6. **Observer wiring zone**
   - IntersectionObserver setup and active-section arbitration.
7. **Chapter/story navigation helpers zone**
   - Step index transitions and story open/close semantics.
8. **UI text/render helpers zone**
   - Citation text truncation, bridge chips, panel text formatting.

---

## 3. Risk classification by extraction order

## 3.1 Low-risk first candidates

### Candidate L1 — Story registry reader wrapper (pure-ish)
- Isolate loading/shape-checking of `story-presets.mjs`.
- Keep existing runtime call sites unchanged.
- Why low risk: minimal coupling to Graph/DOM beyond writing select options.

### Candidate L2 — Alias resolver helper bundle
- Extract/encapsulate `normalizeText` + alias map + resolution heuristics.
- Why low risk: deterministic logic with limited side effects.

### Candidate L3 — Story step merge helper
- Extract step-option merge + defaulting into pure helper.
- Why low risk: no DOM and no direct Graph access if kept data-only.

## 3.2 Medium-risk candidates

### Candidate M1 — Story panel render helpers
- Split string/HTML formatting from DOM querying/mutation.
- Why medium: many hard DOM IDs and assumption-heavy rendering.

### Candidate M2 — Chapter/story navigation helpers
- Extract index/state transitions (`goToStoryStep` family).
- Why medium: still coupled to `updateStoryPanel` and `applyStoryStep` timings.

### Candidate M3 — Anchored scrolly DOM injection utilities
- Extract anchor sorting/grouping and section markup generation.
- Why medium: must preserve scroll observer lifecycle and exact CSS hooks.

## 3.3 Too entangled for now

### Candidate E1 — Core `applyStoryFocus`
- High coupling to `Graph.cy`, class contracts, animation semantics.
- Also coupled to runtime expansion sets and reveal-phase behavior.

### Candidate E2 — `maybeExpandFromNode` callback path
- Triggered from Graph node selection handler; sensitive to click semantics.

### Candidate E3 — Scrolly observer → Story scene activation
- Crosses DOM observer, anchor registry, and story focus engine.

## 3.4 Must not be touched first

1. `Graph.handleNodeSelect` → `StoryMode.maybeExpandFromNode` callback seam.
2. `applyStoryFocus` class semantics (`story-primary`, `story-secondary`, etc.).
3. Mode exclusivity sequence on scrolly entry (`FocusMode.close(); StoryMode.closeStory();`).
4. Layout switching side-effects in `maybeSwitchLayout`.

These are runtime-critical coupling points and should remain stable until a Graph façade seam is in place.

---

## 4. Dependencies that must wait for Graph façade advancement

Story extraction should wait for at least a minimal Graph façade evolution that provides:

- A non-leaky access pattern for Cytoscape (avoid direct `Graph.cy` in Story helpers).
- Stable wrapper commands for:
  - fit/center/zoom operations,
  - class reset/apply batches,
  - layout switching.
- Optional callback/event contracts for graph node selection events.

Until that exists, Story extraction risks becoming a disguised Graph extraction.

---

## 5. Event seam recommendation (future, not in this branch)

A small event seam would materially reduce coupling before extraction:

- `story:expand-from-node` (emitted by Graph node selection path)
- `story:apply-scene` (emitted by scrolly anchor observer)
- `story:closed` and `story:opened` (consumed by mode orchestration)

Why helpful:
- Replaces direct cross-IIFE calls with explicit contracts.
- Allows Story logic to become callable from observer and graph events without importing module internals.

This is a **future branch concern**, not a change for this planning branch.

---

## 6. Safest sequencing for a future `story-extract` branch

1. **Pre-step (no behavior change):** add lightweight instrumentation/comments/tests around current Story flows.
2. **Step 1 (low risk):** isolate registry loader + alias resolver helpers.
3. **Step 2 (low-medium):** isolate step-state transition helpers (pure data functions).
4. **Step 3 (medium):** isolate panel text/render helpers while keeping DOM hooks in place.
5. **Step 4 (gateway):** introduce/validate minimal Graph façade seam for Story needs.
6. **Step 5 (after seam):** move `applyStoryFocus`/`maybeExpandFromNode` behind façade adapter.
7. **Step 6 (last):** split anchored scrolly bridge only after observer + story scene seam is stable.

---

## 7. Explicit non-goals for this planning pass

- No StoryMode extraction implementation.
- No `graphe.html` runtime edits.
- No runtime JS behavior changes.
- No scope expansion into workshop milestones outside Story boundary planning.
- No repetition of graph-extract freeze-assessment material.

---

## 8. Decision summary

- Proceed with **progressive Story boundary planning**, not broad extraction.
- Start with **data/alias/state helpers** first.
- Defer graph-coupled focus engine and callback seams until Graph façade work advances.
- Keep scrolly/anchor orchestration intact until explicit event seam exists.

