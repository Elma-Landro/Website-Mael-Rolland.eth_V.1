#!/usr/bin/env node

import { randomUUID } from 'crypto';

/**
 * PR-06: applier with conservative support links and phase-3 hierarchy preservation.
 */

function normalizeForSignature(value) {
  return String(value ?? '')
    .normalize('NFD')
    .replace(/[\u0300-\u036f]/g, '')
    .toLowerCase()
    .replace(/\s+/g, ' ')
    .trim();
}

function firstTargetSectionKey(operation = {}) {
  return operation?.targetSections?.[0]?.section_key ?? '';
}

export function buildSecondarySignature(operation = {}) {
  const quote = normalizeForSignature(operation.quoteText ?? '');
  const page = Number.isInteger(operation.page) ? operation.page : '';
  const sectionKey = firstTargetSectionKey(operation);
  return `${quote}::${page}::${sectionKey}`;
}

function getAttributeValue(entity, key) {
  const attr = entity?.attributes?.[key];
  if (!attr) return null;
  if (typeof attr.value === 'string') return attr.value;
  if (typeof attr.value === 'number') return String(attr.value);
  return null;
}

function setTextAttribute(entity, key, value) {
  if (!entity.attributes) entity.attributes = {};
  entity.attributes[key] = { type: 'TEXT', value: String(value) };
}

function setArrayAsJsonTextAttribute(entity, key, values) {
  if (!entity.attributes) entity.attributes = {};
  entity.attributes[key] = { type: 'TEXT', value: JSON.stringify(values) };
}

function buildGraphIndexes(graph = {}) {
  const entities = Array.isArray(graph.entities) ? graph.entities : [];
  const types = Array.isArray(graph.types) ? graph.types : [];
  const relationTypes = Array.isArray(graph.relation_types) ? graph.relation_types : [];
  const relations = Array.isArray(graph.relations) ? graph.relations : [];

  const typeById = new Map(types.map((type) => [type.id, type.name]));
  const relationTypeByName = new Map(relationTypes.map((type) => [type.name, type.id]));
  const appearsInSectionTypeId = relationTypeByName.get('appears in section') ?? null;

  const sectionKeyByEntityId = new Map();
  for (const entity of entities) {
    const typeNames = (entity.types ?? []).map((typeId) => typeById.get(typeId));
    if (!typeNames.includes('ThesisSection')) continue;
    const sectionKey = getAttributeValue(entity, 'section_key');
    if (sectionKey) sectionKeyByEntityId.set(entity.id, sectionKey);
  }

  const sourceQuoteEntities = entities.filter((entity) => {
    const names = (entity.types ?? []).map((typeId) => typeById.get(typeId));
    return names.includes('SourceQuote');
  });

  const bySeedId = new Map();
  const bySignature = new Map();

  for (const entity of sourceQuoteEntities) {
    const seedId = getAttributeValue(entity, 'seed_id');
    if (seedId) bySeedId.set(seedId, entity);

    const quoteText = getAttributeValue(entity, 'quoteText');
    const pageRaw = getAttributeValue(entity, 'page');
    const page = pageRaw && /^\d+$/.test(pageRaw) ? Number(pageRaw) : '';

    const firstSectionRelation = appearsInSectionTypeId
      ? relations.find((rel) => rel.from === entity.id && rel.type === appearsInSectionTypeId)
      : null;
    const sectionKey = firstSectionRelation ? sectionKeyByEntityId.get(firstSectionRelation.to) ?? '' : '';

    const signature = `${normalizeForSignature(quoteText ?? '')}::${page}::${sectionKey}`;
    if (quoteText) bySignature.set(signature, entity);
  }

  const relationKeys = new Set(relations.map((rel) => `${rel.from}::${rel.type}::${rel.to}`));
  const sourceQuoteTypeId = types.find((type) => type.name === 'SourceQuote')?.id ?? null;

  return {
    entities,
    relations,
    bySeedId,
    bySignature,
    relationKeys,
    relationTypeByName,
    sourceQuoteTypeId,
  };
}

function dedupResolvedIds(items = []) {
  const ids = items
    .filter((item) => item.status === 'resolved' && typeof item.resolved_entity_id === 'string')
    .map((item) => item.resolved_entity_id);
  return [...new Set(ids)];
}

function applyEssentialAttributes(entity, operation) {
  const updatedFields = [];
  const essentials = {
    seed_id: operation.seed_id,
    title: operation.title,
    quoteText: operation.quoteText,
    page: Number.isInteger(operation.page) ? String(operation.page) : operation.page,
    source_phase: operation.source_phase,
  };

  for (const [key, value] of Object.entries(essentials)) {
    if (value === undefined || value === null || value === '') continue;
    const existing = getAttributeValue(entity, key);
    if (!existing) {
      setTextAttribute(entity, key, value);
      updatedFields.push(key);
    }
  }

  if (!entity.name && operation.title) entity.name = operation.title;
  return updatedFields;
}

function preserveSupportHierarchyAttributes(entity, operation) {
  const updated = [];
  const primary = Array.isArray(operation.primary_entity_names) ? operation.primary_entity_names : [];
  const secondary = Array.isArray(operation.secondary_entity_names) ? operation.secondary_entity_names : [];
  const bridge = Array.isArray(operation.bridge_entity_names) ? operation.bridge_entity_names : [];

  if (primary.length === 0 && secondary.length === 0 && bridge.length === 0) return updated;

  if (!getAttributeValue(entity, 'primary_entity_names')) {
    setArrayAsJsonTextAttribute(entity, 'primary_entity_names', primary);
    updated.push('primary_entity_names');
  }
  if (!getAttributeValue(entity, 'secondary_entity_names')) {
    setArrayAsJsonTextAttribute(entity, 'secondary_entity_names', secondary);
    updated.push('secondary_entity_names');
  }
  if (!getAttributeValue(entity, 'bridge_entity_names')) {
    setArrayAsJsonTextAttribute(entity, 'bridge_entity_names', bridge);
    updated.push('bridge_entity_names');
  }

  return updated;
}

export function applySourceQuoteOperations(resolvedOperations, options = {}) {
  const dryRun = options.dryRun !== false;
  const normalizedOperations = Array.isArray(options.normalizedOperations) ? options.normalizedOperations : [];
  const graph = options.graph ?? { entities: [], relations: [], types: [], relation_types: [] };

  const indexes = buildGraphIndexes(graph);
  const operations = Array.isArray(resolvedOperations) ? resolvedOperations : [];
  const normalizedBySeed = new Map(normalizedOperations.map((op) => [op.seed_id, op]));

  let created = 0;
  let updated = 0;
  let skipped_idempotent = 0;
  const logs = [];

  const results = operations.map((resolvedOp) => {
    const normalizedOp = normalizedBySeed.get(resolvedOp.seed_id) ?? {};
    const signature = buildSecondarySignature(normalizedOp);

    let targetEntity = indexes.bySeedId.get(resolvedOp.seed_id) ?? null;
    if (!targetEntity) targetEntity = indexes.bySignature.get(signature) ?? null;

    const sectionIds = dedupResolvedIds(resolvedOp.sections);
    const unresolved_sections = (resolvedOp.sections ?? [])
      .filter((item) => item.status !== 'resolved')
      .map((item) => item.input);

    const unresolved_supports = (resolvedOp.supports ?? [])
      .filter((item) => item.status !== 'resolved')
      .map((item) => item.input);

    const appearsInSectionType = indexes.relationTypeByName.get('appears in section');
    const quoteSupportsType = indexes.relationTypeByName.get('quote supports');

    const updatedFields = [];
    const createdRelations = [];
    let wasCreated = false;

    if (!targetEntity) {
      if (!indexes.sourceQuoteTypeId) {
        throw new Error('SourceQuote type not found in graph');
      }

      targetEntity = {
        id: randomUUID(),
        name: normalizedOp.title ?? normalizedOp.seed_id ?? 'SourceQuote',
        types: [indexes.sourceQuoteTypeId],
        attributes: {},
      };

      applyEssentialAttributes(targetEntity, normalizedOp);
      preserveSupportHierarchyAttributes(targetEntity, normalizedOp);

      if (!dryRun) indexes.entities.push(targetEntity);
      created += 1;
      wasCreated = true;
    } else {
      updatedFields.push(...applyEssentialAttributes(targetEntity, normalizedOp));
      updatedFields.push(...preserveSupportHierarchyAttributes(targetEntity, normalizedOp));
    }

    if (appearsInSectionType) {
      for (const sectionId of sectionIds) {
        const relationKey = `${targetEntity.id}::${appearsInSectionType}::${sectionId}`;
        if (indexes.relationKeys.has(relationKey)) continue;

        const relation = { id: randomUUID(), from: targetEntity.id, type: appearsInSectionType, to: sectionId };
        indexes.relationKeys.add(relationKey);
        createdRelations.push(relation);
        if (!dryRun) indexes.relations.push(relation);
      }
    }

    const supports_linked = [];
    if (quoteSupportsType) {
      for (const support of resolvedOp.supports ?? []) {
        if (support.status === 'ambiguous') {
          logs.push({
            level: 'warning',
            code: 'SOURCEQUOTE_APPLY_AMBIGUOUS_SUPPORT_SKIPPED',
            seed_id: resolvedOp.seed_id ?? null,
            support_name: support.input,
          });
          continue;
        }
        if (support.status !== 'resolved' || !support.resolved_entity_id) continue;

        const relationKey = `${targetEntity.id}::${quoteSupportsType}::${support.resolved_entity_id}`;
        if (indexes.relationKeys.has(relationKey)) {
          supports_linked.push(support.resolved_entity_id);
          continue;
        }

        const relation = {
          id: randomUUID(),
          from: targetEntity.id,
          type: quoteSupportsType,
          to: support.resolved_entity_id,
        };

        indexes.relationKeys.add(relationKey);
        createdRelations.push(relation);
        supports_linked.push(support.resolved_entity_id);
        if (!dryRun) indexes.relations.push(relation);
      }
    }

    let status;
    if (wasCreated) {
      status = 'created';
    } else if (updatedFields.length > 0 || createdRelations.length > 0) {
      status = 'updated';
      updated += 1;
    } else {
      status = 'skipped_idempotent';
      skipped_idempotent += 1;
    }

    if (status === 'created') {
      indexes.bySeedId.set(resolvedOp.seed_id, targetEntity);
      if (signature !== '::::') indexes.bySignature.set(signature, targetEntity);
    }

    return {
      seed_id: resolvedOp.seed_id ?? null,
      status,
      sourcequote_entity_id: targetEntity?.id ?? null,
      sections_linked: sectionIds,
      supports_linked: [...new Set(supports_linked)],
      unresolved_sections,
      unresolved_supports,
    };
  });

  const result = {
    stage: 'apply',
    dryRun,
    status: 'ok',
    created,
    updated,
    skipped_idempotent,
    partial: 0,
    operations: results,
    logs: [
      {
        level: 'info',
        code: 'SOURCEQUOTE_APPLY_SUPPORTS_HIERARCHY',
        message: 'minimal SourceQuote apply completed with conservative support links',
      },
      ...logs,
    ],
  };

  console.log(JSON.stringify(result));
  return result;
}
