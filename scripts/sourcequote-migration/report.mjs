#!/usr/bin/env node

/**
 * PR-07: consolidated report builder.
 */

export function buildSourceQuoteReport(partialReport = {}, options = {}) {
  const dryRun = options.dryRun !== false;

  const result = {
    stage: 'report',
    dryRun,
    status: 'ok',
    totals: {
      operations_read: partialReport.operations_read ?? 0,
      operations_normalized: partialReport.operations_normalized ?? 0,
      created: partialReport.created ?? 0,
      updated: partialReport.updated ?? 0,
      skipped: partialReport.skipped ?? 0,
      partial: partialReport.partial ?? 0,
      ambiguous_supports: partialReport.ambiguous_supports ?? 0,
      unresolved_sections: partialReport.unresolved_sections ?? 0,
      duplicate_seed_ids: partialReport.duplicate_seed_ids ?? 0,
    },
    phase_summaries: partialReport.phase_summaries ?? [],
    logs: [
      {
        level: 'info',
        code: 'SOURCEQUOTE_REPORT_CONSOLIDATED',
        message: 'consolidated report generated',
      },
    ],
  };

  console.log(JSON.stringify(result));
  return result;
}
