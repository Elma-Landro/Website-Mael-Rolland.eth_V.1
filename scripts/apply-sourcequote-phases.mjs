#!/usr/bin/env node

import { execSync } from 'child_process';
import { readFileSync, readdirSync } from 'fs';
import { normalizeSourceQuoteOperations } from './sourcequote-migration/normalize.mjs';
import { resolveSourceQuoteTargets } from './sourcequote-migration/resolve.mjs';
import { applySourceQuoteOperations } from './sourcequote-migration/apply.mjs';
import { buildSourceQuoteReport } from './sourcequote-migration/report.mjs';

const PHASES = [
  {
    phase: 'phase1',
    zip: 'Migration/sourcequote_effective_patch_phase1.zip',
    json: 'PATCH_SOURCEQUOTE_EFFECTIVE_PHASE1.json',
  },
  {
    phase: 'phase2',
    zip: 'Migration/sourcequote_effective_patch_phase2.zip',
    json: 'PATCH_SOURCEQUOTE_EFFECTIVE_PHASE2.json',
  },
  {
    phase: 'phase3',
    zip: 'Migration/sourcequote_effective_patch_phase3.zip',
    json: 'PATCH_SOURCEQUOTE_EFFECTIVE_PHASE3.json',
  },
];

function findLatestGraph() {
  const candidates = readdirSync('.').filter((name) => /^grc20-these-mael-rolland-v\d+\.json$/.test(name));
  if (candidates.length === 0) return null;

  candidates.sort((a, b) => {
    const versionA = Number(a.match(/v(\d+)\.json$/)?.[1] ?? 0);
    const versionB = Number(b.match(/v(\d+)\.json$/)?.[1] ?? 0);
    return versionA - versionB;
  });

  return candidates[candidates.length - 1];
}

function readPatchFromZip(zipPath, jsonFileName) {
  const stdout = execSync(`unzip -p "${zipPath}" "*/${jsonFileName}"`, { encoding: 'utf8' });
  return JSON.parse(stdout);
}

function findDuplicateSeedIds(operations) {
  const counts = new Map();
  for (const operation of operations) {
    const seedId = operation.seed_id;
    if (!seedId) continue;
    counts.set(seedId, (counts.get(seedId) ?? 0) + 1);
  }

  return [...counts.entries()]
    .filter(([, count]) => count > 1)
    .map(([seed_id, count]) => ({ seed_id, count }));
}

function main() {
  const dryRun = !process.argv.includes('--write');

  const latestGraphPath = findLatestGraph();
  const graph = latestGraphPath ? JSON.parse(readFileSync(latestGraphPath, 'utf8')) : { entities: [], types: [], relations: [], relation_types: [] };

  const phaseRuns = [];
  const normalizedGlobal = [];

  for (const phaseConfig of PHASES) {
    const patch = readPatchFromZip(phaseConfig.zip, phaseConfig.json);
    const operations = Array.isArray(patch.operations) ? patch.operations : [];

    const normalized = normalizeSourceQuoteOperations(operations, {
      dryRun,
      sourcePhase: phaseConfig.phase,
    });

    phaseRuns.push({
      phase: phaseConfig.phase,
      operations_read: operations.length,
      normalized,
    });

    normalizedGlobal.push(...normalized.operations);
  }

  const duplicateSeedIds = findDuplicateSeedIds(normalizedGlobal);
  const duplicateSeedLogs = duplicateSeedIds.map((item) => ({
    level: 'warning',
    code: 'SOURCEQUOTE_GLOBAL_DUPLICATE_SEED_ID',
    seed_id: item.seed_id,
    count: item.count,
  }));

  const phaseSummaries = [];
  let created = 0;
  let updated = 0;
  let skipped = 0;
  let partial = 0;
  let ambiguousSupports = 0;
  let unresolvedSections = 0;

  for (const phaseRun of phaseRuns) {
    const resolved = resolveSourceQuoteTargets(phaseRun.normalized.operations, { dryRun, graph });
    const applied = applySourceQuoteOperations(resolved.operations, {
      dryRun,
      graph,
      normalizedOperations: phaseRun.normalized.operations,
    });

    const phaseAmbiguousSupports = resolved.operations.reduce(
      (sum, operation) => sum + operation.supports.filter((item) => item.status === 'ambiguous').length,
      0
    );

    const phaseUnresolvedSections = applied.operations.reduce(
      (sum, operation) => sum + operation.unresolved_sections.length,
      0
    );

    created += applied.created ?? 0;
    updated += applied.updated ?? 0;
    skipped += applied.skipped_idempotent ?? 0;
    partial += applied.partial ?? 0;
    ambiguousSupports += phaseAmbiguousSupports;
    unresolvedSections += phaseUnresolvedSections;

    phaseSummaries.push({
      phase: phaseRun.phase,
      operations_read: phaseRun.operations_read,
      operations_normalized: phaseRun.normalized.normalized_operations ?? 0,
      created: applied.created ?? 0,
      updated: applied.updated ?? 0,
      skipped: applied.skipped_idempotent ?? 0,
      partial: applied.partial ?? 0,
      ambiguous_supports: phaseAmbiguousSupports,
      unresolved_sections: phaseUnresolvedSections,
    });
  }

  const consolidated = buildSourceQuoteReport(
    {
      operations_read: phaseRuns.reduce((sum, item) => sum + item.operations_read, 0),
      operations_normalized: normalizedGlobal.length,
      created,
      updated,
      skipped,
      partial,
      ambiguous_supports: ambiguousSupports,
      unresolved_sections: unresolvedSections,
      duplicate_seed_ids: duplicateSeedIds.length,
      phase_summaries: phaseSummaries,
    },
    { dryRun }
  );

  if (duplicateSeedLogs.length > 0) {
    console.log(JSON.stringify({ stage: 'orchestrator', logs: duplicateSeedLogs }));
  }

  console.log(
    JSON.stringify({
      stage: 'orchestrator',
      status: 'ok',
      dryRun,
      phases_applied_in_order: PHASES.map((item) => item.phase),
      consolidated_totals: consolidated.totals,
    })
  );
}

main();
