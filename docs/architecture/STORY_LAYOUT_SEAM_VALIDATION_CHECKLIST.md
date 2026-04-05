# Story Layout Seam Validation Checklist

**Branch context:** `feat/research-architecture-vnext-story-layout-seam-spike`  
**Date:** 2026-04-05  
**Purpose:** Final validation gate for the completed Story→Graph layout-request seam spike.

---

## 1) Exact seam path under validation

Only this path is in scope:

1. `StoryMode.maybeSwitchLayout(layoutTarget)`
2. `GrapheEventBus.emit('layout:apply-requested', { name: layoutTarget, source: 'story-mode' })`
3. Graph listener receives `layout:apply-requested`
4. Graph dispatches to existing unchanged layout methods:
   - `applyMonetisationLayout`
   - `applyQuiGouverneLayout`
   - `applyMatriceLayout`
5. `#layout-select` value remains synchronized with active layout target

No other event path is in scope for this checklist.

---

## 2) Required parity checks

Perform all checks from Story-driven entry (opening a story whose `layoutTarget` matches each target):

### A. `monetisation`
- [ ] Story-triggered switch lands in monetisation layout.
- [ ] Visual arrangement matches pre-seam behavior.
- [ ] No console/runtime errors.

### B. `qui-gouverne`
- [ ] Story-triggered switch lands in qui-gouverne layout.
- [ ] Visual arrangement matches pre-seam behavior.
- [ ] No console/runtime errors.

### C. `matrice`
- [ ] Story-triggered switch lands in matrice layout.
- [ ] Visual arrangement matches pre-seam behavior.
- [ ] No console/runtime errors.

### D. `#layout-select` synchronization
- [ ] After each Story-triggered switch, `#layout-select` equals the target layout.
- [ ] No stale value remains from previous layout.

---

## 3) Expected observable behavior (before vs after seam)

Expected parity contract:

- Before seam: Story switched layout by direct calls to Graph layout methods.
- After seam: Story emits `layout:apply-requested`; Graph listener dispatches to the same layout methods.
- Observable user behavior should be unchanged for Story-driven layout switching.

Any observed delta should be treated as a regression until proven otherwise.

---

## 4) Intentionally direct (out of validation scope)

The following remain direct and are not part of this seam validation:

- `applyStoryFocus`
- `maybeExpandFromNode`
- Scrolly observer scene-apply flow
- Other Story→Graph and UI→Graph paths not related to `layout:apply-requested`

---

## 5) Must NOT change during validation

Validation pass constraints (hard stop):

- Do **not** modify runtime code.
- Do **not** add another seam/event path.
- Do **not** refactor Graph/layout internals.
- Do **not** touch `applyStoryFocus`, `maybeExpandFromNode`, or scrolly observer wiring.

This artifact is a validation gate, not an implementation phase.

---

## 6) Branch rule before any further seam work

No further seam path may be added on this branch until the parity checks above are completed and accepted.

If parity is not confirmed, fix/regression handling must remain strictly limited to this same layout-request seam path.
