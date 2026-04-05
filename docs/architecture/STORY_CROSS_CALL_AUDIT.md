# Story Cross-Call Audit

**Branch:** `feat/research-architecture-vnext-story-boundary-plan`  
**Date:** 2026-04-05  
**Scope:** Audit only (no runtime code changes).  
**Target:** V2 GitHub Pages graph/thesis-reader lab (`graphe.html` + `story-presets.mjs`).

---

## 1. StoryMode → Graph calls (concrete map)

StoryMode is defined in `graphe.html` lines **5271–5836** and calls Graph in two patterns:

1) **Direct `Graph.cy` access** (live Cytoscape instance)
- `applyStoryFocus()` → `const cy = Graph.cy` (line **5457**) 
- `clearStoryFocus()` → `const cy = Graph.cy` (line **5601**) 
- `maybeExpandFromNode()` → `const cy = Graph.cy` (line **5709**)

2) **Layout switch hooks (Graph public layout functions)**
- `maybeSwitchLayout(layoutTarget)`:
  - `Graph.applyMonetisationLayout()` (line **5756**)
  - `Graph.applyQuiGouverneLayout()` (line **5757**)
  - `Graph.applyMatriceLayout()` (line **5758**)

### What this confirms
- StoryMode currently depends on Graph as both a **data-plane** (`Graph.cy`) and **command-plane** (`Graph.apply*Layout`) provider.
- StoryMode does **not** call Graph highlight/filter helpers directly; it manipulates Cytoscape classes itself after obtaining `Graph.cy`.

---

## 2. StoryMode → UI calls

### Result: **No direct `UI.*` calls from inside StoryMode**

Within the StoryMode IIFE (5271–5836), there is no callsite for `UI.renderPanel`, `UI.selectEntity`, `UI.clearPanel`, or any other `UI.*` method.

### Important nuance
- StoryMode manipulates its own DOM panel (`#story-mode-panel`, `#story-meta`, `#story-step-title`, etc.) in `updateStoryPanel()` and `init()`.
- It is therefore **UI-coupled via DOM ownership**, not via UI module calls.

---

## 3. StoryMode → DOM dependencies

StoryMode has broad direct DOM coupling (hard IDs/classes), including:

- Story panel and controls:
  - `#story-mode-panel`, `#btn-story-mode`, `#btn-story-close`, `#btn-story-quit`, `#btn-story-next`, `#btn-story-prev`, `#btn-story-reveal`, `#story-select` (lines **5798–5818**)
- Story content targets:
  - `#story-meta`, `#story-step-title`, `#story-step-body`, `#story-citation`, `#story-citation-text`, `#story-citation-page`, `#story-bridge-hint` (lines **5608–5663**)
- Layout/scrolly integration:
  - `#layout-select` (5775, 5823)
  - `.grc-root` + `#btn-scrolly` for force-leaving scrolly mode (5779–5784)

### What this confirms
- StoryMode is not UI-IIFE dependent, but it is **template-structure dependent** (DOM IDs/classes are treated as fixed API).

---

## 4. StoryMode async / data-loading dependencies

StoryMode data path is asynchronous and externalized:

- `loadRegistry()` performs dynamic import of `./story-presets.mjs` (line **5332**).
- `init()` awaits `loadRegistry()` before rendering select options (5795–5798).
- `inferStoryIdFromView()` depends on `storyRegistry.viewToStoryId` (5774–5777).

StoryMode also has runtime data dependencies:

- `resolveFocusNodes()` reads `State.data.entities` (5342–5351).
- Citation rendering in `updateStoryPanel()` reads `window._narrativeAnchors?.anchors` (5633).

### Related loader coupling outside StoryMode
- In DOMContentLoaded auto-bootstrap, `narrative-anchors.json` is fetched and assigned to `window._narrativeAnchors`, then `initAnchoredScrolly(anchorData)` is called (6130, 6138–6141).

---

## 5. Graph → StoryMode calls

Graph node selection handler calls StoryMode directly:

- `handleNodeSelect()` in Graph IIFE invokes  
  `StoryMode.maybeExpandFromNode(id, e.target)` (line **2387**) after `UI.renderPanel` and `highlightNeighbors`.

Registered on:
- `cy.on('tap', 'node', handleNodeSelect)` (2391)
- `cy.on('click', 'node', handleNodeSelect)` (2392)

### What this confirms
- There is a runtime callback chain **Graph event → Story behavior**, not an event-bus seam.

---

## 6. UI → StoryMode calls

No direct `UI.* → StoryMode.*` calls were found in the UI IIFE.

However, there is a **co-located orchestration coupling** in DOMContentLoaded scrolly toggle:

- Entering scrolly mode executes `StoryMode.closeStory()` (line **6504**) to ensure modes are exclusive.

This is not via UI IIFE API, but it is a practical UI/Story coupling in composition-root wiring.

---

## 7. Callback-chain map (requested hotspots)

## 7.1 `selectEntity` chain (guided overlay path)

- Guided overlay search suggestion click
  - `UI.selectEntity(e.id)` (line **5216**)
  - `UI.selectEntity` uses `Graph.cy.$id(...)` + `Graph.cy.animate(...)` and `Graph.highlightNeighbors(id)` (5030–5038)

This chain is **UI helper → UI IIFE → Graph**.

## 7.2 `focusStory` status

- No function named `focusStory` is present in current runtime.
- Equivalent active focus entrypoint is `StoryMode.applyStoryFocus(...)` (5456).

## 7.3 `maybeExpandFromNode` chain

- Graph node tap/click → `handleNodeSelect` (2374–2392)
- `StoryMode.maybeExpandFromNode(id, node)` (2387)
- `maybeExpandFromNode` reads step config, inspects connected edges, updates runtime expansion sets, then re-calls `applyStoryFocus(...)` + `updateStoryPanel()` (5698–5728)

## 7.4 Scrolly observer chain

- `initScrollyObserver()` creates IntersectionObserver (6418–6449)
- If active section has `data-anchor-id`:
  - resolve anchor scene → `StoryMode.resolveFocusNodes(...)` (6436)
  - `StoryMode.applyStoryFocus(...)` (6437)
- Else if chapter section:
  - `highlightByChapter(...)` (6440)

## 7.5 Guided overlay coupling

- Guided overlay suggestion click calls `UI.selectEntity` (5216); this indirectly affects Story expansion only when graph node click occurs later (via Graph handler), not directly from guided overlay itself.

## 7.6 Chapter/story anchors chain

- Auto bootstrap fetches `narrative-anchors.json` (6130)
- `initAnchoredScrolly(anchorData)` injects `.story-section.anchor-section` DOM nodes (6325–6385)
- Re-initializes observer `initScrollyObserver()` (6388)
- Observer drives Story focus scenes via anchor metadata (6431–6438)

---

## 8. Direct `Graph.cy` usage inside StoryMode

Confirmed direct usage points:
- 5457 (`applyStoryFocus`)
- 5601 (`clearStoryFocus`)
- 5709 (`maybeExpandFromNode`)

This means StoryMode currently depends on Cytoscape object shape and classes directly (nodes/edges iteration, class mutation, animation).

---

## 9. Hardcoded alias/lookup maps and registry assumptions

### Inside StoryMode
- `STORY_FOCUS_ALIASES` static alias dictionary (5282–5324).
- Assumes `storyRegistry` has shape `{ stories: [], viewToStoryId: {} }` (5272).
- Assumes each story has `defaultStepOptions`, `steps`, optional `layoutTarget`.

### Outside StoryMode but story-coupled
- `CHAPTER_ID_TO_KEY` hardcoded map in `initAnchoredScrolly` (6341–6347), binding chapter entity IDs to `intro/ch1/ch2/ch3/ccl` keys.

### What this confirms
- Story runtime correctness depends on static naming/ID conventions that are not centrally validated.

---

## 10. Hidden cross-IIFE couplings (including FocusMode)

## 10.1 StoryMode ↔ Graph (hard)
- `Graph.cy` direct access (StoryMode side) and `StoryMode.maybeExpandFromNode` direct invocation (Graph side).

## 10.2 StoryMode ↔ DOMContentLoaded scrolly orchestration (hard)
- Scrolly toggle force-closes Story (`StoryMode.closeStory`, line 6504).
- Scrolly observer can activate Story focus scenes (`StoryMode.applyStoryFocus`, line 6437).

## 10.3 StoryMode ↔ FocusMode (indirect, DOM-state level)
- Scrolly entry does `FocusMode.close()` then `StoryMode.closeStory()` (6503–6504), creating implicit mode exclusivity in shared root state (`.grc-root`, active classes, class-based graph styling).
- No direct StoryMode→FocusMode function calls inside StoryMode IIFE; coupling is composition-root and shared Cytoscape class mutation.

## 10.4 FocusMode ↔ Graph direct cy coupling (context risk)
- FocusMode uses `function _cy() { return Graph.cy; }` (4513), same `Graph.cy` exposure pattern as StoryMode.
- This increases extraction risk because both modes co-own graph-class and viewport behaviors via live `cy` access.

---

## 11. Net audit conclusions (for boundary planning)

1. StoryMode has **zero direct UI API dependency**, but **high direct DOM dependency**.
2. StoryMode has **high Graph dependency** through `Graph.cy` and layout commands.
3. Story/scrolly/anchor orchestration is a shared runtime plane in DOMContentLoaded, not cleanly isolated.
4. Alias maps and chapter-key maps are hardcoded in runtime, creating brittle boundary seams.
5. Any extraction attempt without a façade/event seam will likely pull Graph and scrolly code with it.

