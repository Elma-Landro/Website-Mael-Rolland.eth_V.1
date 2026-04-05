# Story Layout Seam Validation Result

**Branch:** `feat/research-architecture-vnext-story-layout-seam-validation`  
**Date:** 2026-04-05  
**Validation source:** `docs/architecture/STORY_LAYOUT_SEAM_VALIDATION_CHECKLIST.md`

---

## 1) What was checked

Validated the exact seam path only:

1. `StoryMode.maybeSwitchLayout(layoutTarget)`
2. `GrapheEventBus.emit('layout:apply-requested', { name: layoutTarget, source: 'story-mode' })`
3. Graph listener `bindLayoutApplyRequested` receives event
4. Graph listener dispatches to unchanged methods:
   - `applyMonetisationLayout`
   - `applyQuiGouverneLayout`
   - `applyMatriceLayout`
5. `#layout-select` synchronization is maintained by listener/fallback assignment

Checked target parity coverage for:
- `monetisation`
- `qui-gouverne`
- `matrice`
- `#layout-select` value sync

---

## 2) Validation finding

**Result: parity holds by implementation inspection.**

- Event emit path and listener dispatch are wired for all three required layout targets.
- Listener updates `#layout-select` when dispatching.
- Story fallback path preserves previous direct behavior if no listener handles the event.
- No additional seam path was introduced in this validation pass.

---

## 3) Was any parity fix required?

**No.**

No runtime discrepancy requiring a code change was identified during this validation pass.

---

## 4) Intentionally out of scope (unchanged)

- `applyStoryFocus`
- `maybeExpandFromNode`
- Scrolly observer scene-apply behavior
- Graph/layout internals beyond the mediated request path
- Any new Story→Graph seam path

---

## 5) Validation status

The Story→Graph layout-request seam spike can be treated as **validated for the documented parity scope**.

This branch should stop here and remain constrained to validation-only evidence.
