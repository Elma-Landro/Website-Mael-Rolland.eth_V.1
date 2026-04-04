#!/usr/bin/env node

import fs from 'fs';
import path from 'path';

const ROOT = process.cwd();
const WORKSHOP = path.join(ROOT, 'workshop');
const EXPORT_DIR = path.join(WORKSHOP, 'exports');
const POLICY_PATH = path.join(EXPORT_DIR, 'export-policy.json');
const PATCH_INVENTORY_PATH = path.join(WORKSHOP, 'patches', 'patch-inventory.json');

function rel(p) {
  return path.relative(ROOT, p) || '.';
}

function safeJsonRead(file) {
  try {
    return { ok: true, value: JSON.parse(fs.readFileSync(file, 'utf8')) };
  } catch (err) {
    return { ok: false, error: err.message };
  }
}

function listJsonFiles(dir) {
  if (!fs.existsSync(dir)) return [];
  return fs.readdirSync(dir)
    .filter((name) => name.endsWith('.json'))
    .map((name) => path.join(dir, name));
}

function loadExportPolicy() {
  if (!fs.existsSync(POLICY_PATH)) {
    return {
      found: false,
      path: rel(POLICY_PATH),
      notes: 'Export policy file not found. Dry-run cannot apply manifest-driven rules.',
      statusPolicy: {
        exportableInPrinciple: ['unknown'],
        reviewOrDispute: ['unknown'],
        workshopOnlyInternal: ['unknown']
      },
      families: []
    };
  }

  const parsed = safeJsonRead(POLICY_PATH);
  if (!parsed.ok) {
    return {
      found: true,
      path: rel(POLICY_PATH),
      notes: `Export policy exists but failed to parse (${parsed.error}).`,
      statusPolicy: {
        exportableInPrinciple: ['unknown'],
        reviewOrDispute: ['unknown'],
        workshopOnlyInternal: ['unknown']
      },
      families: []
    };
  }

  const policy = parsed.value;
  return {
    found: true,
    path: rel(POLICY_PATH),
    notes: 'Manifest-driven policy loaded for dry-run analysis only.',
    version: policy.version || 'unknown',
    mode: policy.mode || 'unknown',
    statusPolicy: policy.statusPolicy || {
      exportableInPrinciple: ['unknown'],
      reviewOrDispute: ['unknown'],
      workshopOnlyInternal: ['unknown']
    },
    families: Array.isArray(policy.families) ? policy.families : []
  };
}

function findCanonicalGraphSource() {
  const candidates = fs.readdirSync(ROOT)
    .filter((name) => /^grc20-these-mael-rolland-v\d+\.json$/i.test(name))
    .map((name) => {
      const match = name.match(/-v(\d+)\.json$/i);
      const version = match ? Number(match[1]) : -1;
      return { file: path.join(ROOT, name), version };
    })
    .sort((a, b) => b.version - a.version);

  if (!candidates.length) {
    return {
      found: false,
      path: null,
      version: null,
      entityCount: null,
      relationCount: null,
      notes: 'No canonical graph file matching grc20-these-mael-rolland-v*.json found at repo root.'
    };
  }

  const selected = candidates[0];
  const parsed = safeJsonRead(selected.file);
  if (!parsed.ok) {
    return {
      found: true,
      path: rel(selected.file),
      version: `v${selected.version}`,
      entityCount: null,
      relationCount: null,
      notes: `Canonical source found but JSON could not be parsed (${parsed.error}).`
    };
  }

  const doc = parsed.value;
  const entityCount = Array.isArray(doc.entities) ? doc.entities.length : null;
  const relationCount = Array.isArray(doc.relations) ? doc.relations.length : null;

  return {
    found: true,
    path: rel(selected.file),
    version: `v${selected.version}`,
    entityCount,
    relationCount,
    notes: 'Selected highest detected canonical graph version at repository root.'
  };
}

function summarizePatchInventory() {
  if (!fs.existsSync(PATCH_INVENTORY_PATH)) {
    return {
      found: false,
      path: rel(PATCH_INVENTORY_PATH),
      notes: 'Patch inventory not found. Run workshop/scripts/audit-patches.mjs first.',
      totals: null,
      statusBreakdown: []
    };
  }

  const parsed = safeJsonRead(PATCH_INVENTORY_PATH);
  if (!parsed.ok) {
    return {
      found: true,
      path: rel(PATCH_INVENTORY_PATH),
      notes: `Patch inventory exists but failed to parse (${parsed.error}).`,
      totals: null,
      statusBreakdown: []
    };
  }

  const inventory = parsed.value;
  const artifacts = Array.isArray(inventory.artifacts) ? inventory.artifacts : [];
  const statusMap = new Map();
  for (const a of artifacts) {
    const status = typeof a?.probableStatus === 'string' ? a.probableStatus : 'unknown';
    statusMap.set(status, (statusMap.get(status) || 0) + 1);
  }

  return {
    found: true,
    path: rel(PATCH_INVENTORY_PATH),
    notes: 'Using documentary patch inventory as context only. No patch application is performed in dry-run mode.',
    totals: inventory.totals || null,
    statusBreakdown: Array.from(statusMap.entries())
      .map(([status, count]) => ({ status, count }))
      .sort((a, b) => a.status.localeCompare(b.status))
  };
}

function collectFamilyStatus(policy) {
  const familyReports = [];

  for (const family of policy.families) {
    const sourcePath = typeof family.sourcePath === 'string' ? family.sourcePath : '';

    // Guard: an empty sourcePath would resolve to ROOT, scanning the entire repo.
    // Skip such families and log them clearly rather than producing misleading counts.
    if (!sourcePath) {
      console.warn(`[dry-run] skipping family "${family.id || 'unknown'}": sourcePath is empty or missing`);
      familyReports.push({
        id: family.id || 'unknown',
        objectFamily: family.label || family.id || 'unknown',
        path: 'unknown',
        fileCount: 0,
        parseErrors: 0,
        statusField: typeof family.statusField === 'string' ? family.statusField : 'status',
        statusBreakdown: [],
        allowedStatusesForExportInPrinciple: Array.isArray(family.allowedStatusesForExportInPrinciple) ? family.allowedStatusesForExportInPrinciple : [],
        visibility: family.visibility || 'unknown',
        expectedOutput: family.expectedOutput || 'unknown',
        notes: 'skipped: sourcePath is empty or missing — configure family.sourcePath to enable scanning',
        eligibleCount: 0,
        readiness: 'no_artifacts_detected'
      });
      continue;
    }

    const sourceDir = path.join(ROOT, sourcePath);
    const files = listJsonFiles(sourceDir);

    const statusField = typeof family.statusField === 'string' ? family.statusField : 'status';
    const allowed = Array.isArray(family.allowedStatusesForExportInPrinciple)
      ? family.allowedStatusesForExportInPrinciple
      : [];

    const statusCounts = new Map();
    let parseErrors = 0;

    for (const file of files) {
      const parsed = safeJsonRead(file);
      if (!parsed.ok) {
        parseErrors += 1;
        continue;
      }
      const doc = parsed.value;
      const statusValue = typeof doc?.[statusField] === 'string' ? doc[statusField] : 'unknown';
      statusCounts.set(statusValue, (statusCounts.get(statusValue) || 0) + 1);
    }

    const statusBreakdown = Array.from(statusCounts.entries())
      .map(([status, count]) => ({ status, count }))
      .sort((a, b) => a.status.localeCompare(b.status));

    const eligibleCount = statusBreakdown
      .filter((item) => allowed.includes(item.status))
      .reduce((sum, item) => sum + item.count, 0);

    const visibility = family.visibility || 'unknown';
    const readiness = visibility === 'workshop_only'
      ? 'not_exportable_in_public_bundle'
      : eligibleCount > 0
        ? 'candidate_exportable_items_present'
        : files.length > 0
          ? 'present_but_not_export_ready'
          : 'no_artifacts_detected';

    familyReports.push({
      id: family.id || 'unknown',
      objectFamily: family.label || family.id || 'unknown',
      path: sourcePath || 'unknown',
      fileCount: files.length,
      parseErrors,
      statusField,
      statusBreakdown,
      allowedStatusesForExportInPrinciple: allowed,
      visibility,
      expectedOutput: family.expectedOutput || 'unknown',
      notes: family.notes || '',
      eligibleCount,
      readiness
    });
  }

  return familyReports;
}

function buildReport() {
  const policy = loadExportPolicy();
  const canonicalSource = findCanonicalGraphSource();
  const patchInventory = summarizePatchInventory();
  const families = collectFamilyStatus(policy);

  const workshopOnlyFamilies = families
    .filter((f) => f.visibility === 'workshop_only')
    .map((f) => f.objectFamily);

  const publicExportEligibleFamilies = families
    .filter((f) => f.visibility === 'public_eligible')
    .map((f) => f.objectFamily);

  const readyFamilies = families
    .filter((f) => f.visibility === 'public_eligible' && f.eligibleCount > 0)
    .map((f) => ({ objectFamily: f.objectFamily, eligibleCount: f.eligibleCount }));

  return {
    generatedAt: new Date().toISOString(),
    mode: 'dry_run_documentary_only',
    nonDestructiveGuarantee: [
      'No canonical graph file is modified.',
      'No new canonical graph version is generated.',
      'No patch is applied.',
      'No runtime/public loader path is changed.'
    ],
    canonicalSource,
    patchInventory,
    exportPolicy: {
      found: policy.found,
      path: policy.path,
      version: policy.version || 'unknown',
      mode: policy.mode || 'unknown',
      notes: policy.notes
    },
    statusPolicy: {
      exportableInPrinciple: Array.isArray(policy.statusPolicy?.exportableInPrinciple)
        ? policy.statusPolicy.exportableInPrinciple
        : ['unknown'],
      reviewOrDispute: Array.isArray(policy.statusPolicy?.reviewOrDispute)
        ? policy.statusPolicy.reviewOrDispute
        : ['unknown'],
      workshopOnlyInternal: Array.isArray(policy.statusPolicy?.workshopOnlyInternal)
        ? policy.statusPolicy.workshopOnlyInternal
        : ['unknown'],
      note: 'Status policy comes from workshop/exports/export-policy.json. Dry-run only; no promotion occurs.'
    },
    objectFamilies: families,
    workshopOnlyObjectFamiliesDetected: workshopOnlyFamilies,
    publicExportEligibleObjectFamiliesDetected: publicExportEligibleFamilies,
    workshopArtifactsReadyForExportNow: readyFamilies,
    exportReadinessSummary: readyFamilies.length > 0
      ? 'Some public-eligible families contain artifacts with statuses allowed by the manifest policy.'
      : 'No workshop artifacts are currently evidenced as export-ready under the manifest policy.',
    futurePipelineOutputsWouldInclude: families
      .map((f) => f.expectedOutput)
      .filter((value, index, arr) => value && arr.indexOf(value) === index),
    unresolvedBlockersOrUnknowns: [
      'Manifest policy is conservative and may keep families workshop-only until explicit publication criteria are approved.',
      'Patch inventory statuses are heuristic and documentary, not proof of apply-state.',
      'Missing/empty family directories are treated as no artifacts detected, not as errors.',
      'This script does not execute canonical export; it only reports policy-based readiness.'
    ]
  };
}

function toMarkdown(report) {
  const lines = [];
  lines.push('# Workshop Export Dry-Run (manifest-driven, non-destructive)');
  lines.push('');
  lines.push(`Generated: ${report.generatedAt}`);
  lines.push('');

  lines.push('## Guarantees');
  for (const g of report.nonDestructiveGuarantee) lines.push(`- ${g}`);
  lines.push('');

  lines.push('## Export manifest used');
  lines.push(`- Path: ${report.exportPolicy.path}`);
  lines.push(`- Found: ${report.exportPolicy.found ? 'yes' : 'no'}`);
  lines.push(`- Version: ${report.exportPolicy.version}`);
  lines.push(`- Mode: ${report.exportPolicy.mode}`);
  lines.push(`- Note: ${report.exportPolicy.notes}`);
  lines.push('');

  lines.push('## Canonical source inspected');
  lines.push(`- Path: ${report.canonicalSource.path || 'unknown'}`);
  lines.push(`- Version: ${report.canonicalSource.version || 'unknown'}`);
  lines.push(`- Entities: ${report.canonicalSource.entityCount ?? 'unknown'}`);
  lines.push(`- Relations: ${report.canonicalSource.relationCount ?? 'unknown'}`);
  lines.push(`- Note: ${report.canonicalSource.notes}`);
  lines.push('');

  lines.push('## Patch inventory context (read-only)');
  lines.push(`- Inventory path: ${report.patchInventory.path}`);
  lines.push(`- Found: ${report.patchInventory.found ? 'yes' : 'no'}`);
  lines.push(`- Note: ${report.patchInventory.notes}`);
  if (report.patchInventory.totals) lines.push(`- Artifact total: ${report.patchInventory.totals.artifacts}`);
  if (report.patchInventory.statusBreakdown.length) {
    lines.push('- Status breakdown:');
    for (const s of report.patchInventory.statusBreakdown) lines.push(`  - ${s.status}: ${s.count}`);
  }
  lines.push('');

  lines.push('## Status policy from manifest');
  lines.push(`- Exportable in principle: ${report.statusPolicy.exportableInPrinciple.join(', ')}`);
  lines.push(`- Review/dispute statuses: ${report.statusPolicy.reviewOrDispute.join(', ')}`);
  lines.push(`- Workshop-only internal statuses: ${report.statusPolicy.workshopOnlyInternal.join(', ')}`);
  lines.push(`- Note: ${report.statusPolicy.note}`);
  lines.push('');

  lines.push('## Object families detected (manifest-driven)');
  for (const f of report.objectFamilies) {
    const statuses = f.statusBreakdown.length
      ? f.statusBreakdown.map((s) => `${s.status}:${s.count}`).join(', ')
      : 'none';
    const allowed = f.allowedStatusesForExportInPrinciple.length
      ? f.allowedStatusesForExportInPrinciple.join(', ')
      : 'none';
    lines.push(`- ${f.objectFamily} (${f.path})`);
    lines.push(`  - files: ${f.fileCount}; parseErrors: ${f.parseErrors}; visibility: ${f.visibility}`);
    lines.push(`  - statusField: ${f.statusField}; allowedStatusesForExportInPrinciple: ${allowed}`);
    lines.push(`  - statuses: ${statuses}`);
    lines.push(`  - expectedOutput: ${f.expectedOutput}`);
    lines.push(`  - readiness: ${f.readiness}`);
  }
  lines.push('');

  lines.push('## Public-export-eligible families');
  lines.push(`- ${report.publicExportEligibleObjectFamiliesDetected.join(', ') || 'none'}`);
  lines.push('');

  lines.push('## Workshop-only families');
  lines.push(`- ${report.workshopOnlyObjectFamiliesDetected.join(', ') || 'none'}`);
  lines.push('');

  lines.push('## Are any workshop artifacts export-ready now?');
  if (report.workshopArtifactsReadyForExportNow.length) {
    for (const r of report.workshopArtifactsReadyForExportNow) {
      lines.push(`- ${r.objectFamily}: ${r.eligibleCount} item(s) allowed by manifest`);
    }
  } else {
    lines.push('- No grounded export-ready workshop artifacts were detected under current manifest policy.');
  }
  lines.push(`- Summary: ${report.exportReadinessSummary}`);
  lines.push('');

  lines.push('## Future pipeline outputs referenced by manifest (not generated now)');
  for (const p of report.futurePipelineOutputsWouldInclude) lines.push(`- ${p}`);
  lines.push('');

  lines.push('## Unresolved blockers / unknowns');
  for (const b of report.unresolvedBlockersOrUnknowns) lines.push(`- ${b}`);

  return lines.join('\n');
}

function main() {
  fs.mkdirSync(EXPORT_DIR, { recursive: true });

  const report = buildReport();
  const jsonPath = path.join(EXPORT_DIR, 'export-dry-run.json');
  const mdPath = path.join(EXPORT_DIR, 'EXPORT_DRY_RUN.md');

  fs.writeFileSync(jsonPath, JSON.stringify(report, null, 2));
  fs.writeFileSync(mdPath, `${toMarkdown(report)}\n`);

  console.log(`Wrote ${rel(jsonPath)}`);
  console.log(`Wrote ${rel(mdPath)}`);
  console.log('Dry-run only: no graph mutation, no patch apply, no runtime wiring.');
}

main();
