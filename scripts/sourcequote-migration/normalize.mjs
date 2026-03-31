#!/usr/bin/env node

/**
 * PR-02: normalizer implementation (multi-phases) with light validation.
 */

const ALLOWED_PHASES = new Set(['phase1', 'phase2', 'phase3']);

function isNonEmptyString(value) {
  return typeof value === 'string' && value.trim().length > 0;
}

function asStringArray(value) {
  if (!Array.isArray(value)) return [];
  return value.filter((item) => typeof item === 'string' && item.length > 0);
}

function normalizeTargetSections(inputSections = []) {
  if (!Array.isArray(inputSections)) return [];

  return inputSections
    .map((section) => {
      if (!section || typeof section !== 'object') return null;

      const section_key = section.section_key;
      const section_name = section.section_name;
      const thesis_location = section.thesis_location;

      if (!isNonEmptyString(section_key)) return null;

      const normalizedSection = { section_key };
      if (isNonEmptyString(section_name)) normalizedSection.section_name = section_name;
      if (isNonEmptyString(thesis_location)) normalizedSection.thesis_location = thesis_location;
      return normalizedSection;
    })
    .filter(Boolean);
}

export function normalizeOperation(op, phase) {
  const logs = [];

  if (!op || typeof op !== 'object') {
    return {
      operation: null,
      valid: false,
      logs: [
        {
          level: 'error',
          code: 'SOURCEQUOTE_NORMALIZE_INVALID_OPERATION',
          message: 'operation must be an object',
        },
      ],
    };
  }

  const source_phase = ALLOWED_PHASES.has(phase) ? phase : null;
  if (!source_phase) {
    logs.push({
      level: 'warning',
      code: 'SOURCEQUOTE_NORMALIZE_INVALID_PHASE',
      message: 'invalid source phase',
    });
  }

  const quoteText = op.quoteText ?? op.quote_text;
  const page = op.page ?? op.page_thesis;
  const targetSectionsRaw = op.targetSections ?? op.target_sections;
  const thesisLocation = op.thesisLocation ?? op.thesis_location;

  const primary_entity_names = asStringArray(op.primary_entity_names);
  const secondary_entity_names = asStringArray(op.secondary_entity_names);
  const bridge_entity_names = asStringArray(op.bridge_entity_names);

  const hasHierarchy =
    primary_entity_names.length > 0 ||
    secondary_entity_names.length > 0 ||
    bridge_entity_names.length > 0;

  let quote_supports_entity_names = asStringArray(op.quote_supports_entity_names);

  if (hasHierarchy && quote_supports_entity_names.length === 0) {
    quote_supports_entity_names = [
      ...primary_entity_names,
      ...secondary_entity_names,
      ...bridge_entity_names,
    ];
  }

  const targetSections = normalizeTargetSections(targetSectionsRaw);

  const normalized = {
    seed_id: op.seed_id,
    title: op.title,
    quoteText,
    page,
    chapter: op.chapter ?? null,
    thesisLocation: isNonEmptyString(thesisLocation) ? thesisLocation : null,
    targetSections,
    primary_entity_names,
    secondary_entity_names,
    bridge_entity_names,
    quote_supports_entity_names,
    rationale: op.rationale ?? null,
    implementation_note: op.implementation_note ?? null,
    source_phase,
  };

  if (!isNonEmptyString(normalized.seed_id)) {
    logs.push({ level: 'warning', code: 'SOURCEQUOTE_NORMALIZE_MISSING_SEED_ID', message: 'missing seed_id' });
  }
  if (!isNonEmptyString(normalized.title)) {
    logs.push({ level: 'warning', code: 'SOURCEQUOTE_NORMALIZE_MISSING_TITLE', message: 'missing title' });
  }
  if (!isNonEmptyString(normalized.quoteText)) {
    logs.push({ level: 'warning', code: 'SOURCEQUOTE_NORMALIZE_MISSING_QUOTE_TEXT', message: 'missing quoteText' });
  }
  if (!Number.isInteger(normalized.page)) {
    logs.push({ level: 'warning', code: 'SOURCEQUOTE_NORMALIZE_INVALID_PAGE', message: 'page must be an integer' });
  }
  if (normalized.targetSections.length === 0) {
    logs.push({ level: 'warning', code: 'SOURCEQUOTE_NORMALIZE_EMPTY_TARGET_SECTIONS', message: 'no valid target sections' });
  }

  const valid = logs.filter((item) => item.level === 'warning').length === 0;

  return {
    operation: normalized,
    valid,
    logs,
  };
}

export function normalizeSourceQuoteOperations(operations, options = {}) {
  const dryRun = options.dryRun !== false;
  const sourcePhase = options.sourcePhase;
  const inputOperations = Array.isArray(operations) ? operations : [];

  const normalizedOperations = [];
  const logs = [];

  for (const op of inputOperations) {
    const { operation, valid, logs: opLogs } = normalizeOperation(op, sourcePhase);
    if (operation) normalizedOperations.push(operation);
    logs.push(...opLogs, {
      level: valid ? 'info' : 'warning',
      code: 'SOURCEQUOTE_NORMALIZE_OPERATION_STATUS',
      seed_id: operation?.seed_id ?? null,
      valid,
    });
  }

  const result = {
    stage: 'normalize',
    dryRun,
    status: 'ok',
    source_phase: sourcePhase ?? null,
    operations_read: inputOperations.length,
    normalized_operations: normalizedOperations.length,
    valid_operations: normalizedOperations.length - logs.filter((l) => l.code === 'SOURCEQUOTE_NORMALIZE_OPERATION_STATUS' && !l.valid).length,
    operations: normalizedOperations,
    logs,
  };

  console.log(JSON.stringify(result));
  return result;
}
