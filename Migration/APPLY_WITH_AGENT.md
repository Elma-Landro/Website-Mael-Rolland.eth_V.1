# Apply with agent — minimal instructions

Read `PATCH_SOURCEQUOTE_EFFECTIVE_PHASE2.json` and implement it directly.

## Required behavior
1. For each `ADD_SOURCEQUOTE_WITH_SECTION_LINKS` operation:
   - create one new `SourceQuote` entity
   - set its display name from `title`
   - store the exact thesis quote in `quoteText`
   - store the exact thesis page in `page`
   - set `chapter` and `thesisLocation` consistently from the target section
2. Link the new `SourceQuote` to each `target_section` via `appears in section`.
3. Resolve each `quote_supports_entity_names` item against the current graph:
   - exact name first
   - normalized name second
   - if ambiguous, skip and log
4. Do **not** rewrite the quote.
5. Preserve French punctuation and typography.

## Expected deliverable
- a migration patch or direct graph update
- a short report listing:
  - SourceQuotes created
  - section links added
  - support links added
  - ambiguous names skipped

## Why this patch matters
These `SourceQuote` anchors are intended to be reused in:
- thesis reader / scrollytelling
- graph reader / story mode
- back-linking to concepts, actors, protocols, crises and references
