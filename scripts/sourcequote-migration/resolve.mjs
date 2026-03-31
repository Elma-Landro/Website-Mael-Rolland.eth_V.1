#!/usr/bin/env node

/**
 * PR-03: read-only resolution stage.
 * - resolveSectionByKey(section_key)
 * - resolveEntityName(name): exact > normalized > alias
 */

function normalizeName(value) {
  return String(value ?? '')
    .normalize('NFD')
    .replace(/[\u0300-\u036f]/g, '')
    .toLowerCase()
    .replace(/\s+/g, ' ')
    .trim();
}

function getAttributeValue(entity, key) {
  const attr = entity?.attributes?.[key];
  if (!attr) return null;
  return typeof attr.value === 'string' ? attr.value : null;
}

function withStatus(matches = []) {
  if (matches.length === 1) return { status: 'resolved', matches };
  if (matches.length > 1) return { status: 'ambiguous', matches };
  return { status: 'unresolved', matches: [] };
}

function buildResolverIndexes(graph = {}, aliasMap = {}) {
  const entities = Array.isArray(graph.entities) ? graph.entities : [];
  const types = Array.isArray(graph.types) ? graph.types : [];
  const typeById = new Map(types.map((type) => [type.id, type.name]));

  const sectionByKey = new Map();
  const entitiesByExactName = new Map();
  const entitiesByNormalizedName = new Map();

  for (const entity of entities) {
    const name = entity?.name;
    if (typeof name === 'string' && name.length > 0) {
      if (!entitiesByExactName.has(name)) entitiesByExactName.set(name, []);
      entitiesByExactName.get(name).push(entity);

      const normalized = normalizeName(name);
      if (!entitiesByNormalizedName.has(normalized)) entitiesByNormalizedName.set(normalized, []);
      entitiesByNormalizedName.get(normalized).push(entity);
    }

    const typeNames = (entity?.types ?? []).map((typeId) => typeById.get(typeId));
    if (!typeNames.includes('ThesisSection')) continue;

    const sectionKey = getAttributeValue(entity, 'section_key');
    if (!sectionKey) continue;
    if (!sectionByKey.has(sectionKey)) sectionByKey.set(sectionKey, []);
    sectionByKey.get(sectionKey).push(entity);
  }

  const normalizedAliasMap = {};
  for (const [alias, targetName] of Object.entries(aliasMap ?? {})) {
    normalizedAliasMap[normalizeName(alias)] = targetName;
  }

  return {
    sectionByKey,
    entitiesByExactName,
    entitiesByNormalizedName,
    aliasMap: normalizedAliasMap,
  };
}

export function resolveSectionByKey(section_key, indexes) {
  const sectionMatches = indexes?.sectionByKey?.get(section_key) ?? [];
  const { status, matches } = withStatus(sectionMatches);

  return {
    input: section_key,
    status,
    resolved_entity_id: matches[0]?.id ?? null,
    candidates: matches.map((entity) => ({ id: entity.id, name: entity.name })),
  };
}

export function resolveEntityName(name, indexes) {
  const exactMatches = indexes?.entitiesByExactName?.get(name) ?? [];
  if (exactMatches.length > 0) {
    const { status, matches } = withStatus(exactMatches);
    return {
      input: name,
      strategy: 'exact',
      status,
      resolved_entity_id: matches[0]?.id ?? null,
      candidates: matches.map((entity) => ({ id: entity.id, name: entity.name })),
    };
  }

  const normalizedInput = normalizeName(name);
  const normalizedMatches = indexes?.entitiesByNormalizedName?.get(normalizedInput) ?? [];
  if (normalizedMatches.length > 0) {
    const { status, matches } = withStatus(normalizedMatches);
    return {
      input: name,
      strategy: 'normalized',
      status,
      resolved_entity_id: matches[0]?.id ?? null,
      candidates: matches.map((entity) => ({ id: entity.id, name: entity.name })),
    };
  }

  const aliasTarget = indexes?.aliasMap?.[normalizedInput];
  if (aliasTarget) {
    const aliasMatches = indexes?.entitiesByExactName?.get(aliasTarget) ?? [];
    const { status, matches } = withStatus(aliasMatches);
    return {
      input: name,
      strategy: 'alias',
      status,
      resolved_entity_id: matches[0]?.id ?? null,
      candidates: matches.map((entity) => ({ id: entity.id, name: entity.name })),
    };
  }

  return {
    input: name,
    strategy: 'none',
    status: 'unresolved',
    resolved_entity_id: null,
    candidates: [],
  };
}

function collectSupportTargets(operation = {}) {
  const primary = (operation.primary_entity_names ?? []).map((name) => ({ name, support_level: 'primary' }));
  const secondary = (operation.secondary_entity_names ?? []).map((name) => ({ name, support_level: 'secondary' }));
  const bridge = (operation.bridge_entity_names ?? []).map((name) => ({ name, support_level: 'bridge' }));

  if (primary.length > 0 || secondary.length > 0 || bridge.length > 0) {
    return [...primary, ...secondary, ...bridge];
  }

  return (operation.quote_supports_entity_names ?? []).map((name) => ({
    name,
    support_level: 'flat',
  }));
}

export function resolveSourceQuoteTargets(normalizedOperations, options = {}) {
  const dryRun = options.dryRun !== false;
  const inputOperations = Array.isArray(normalizedOperations) ? normalizedOperations : [];
  const indexes = buildResolverIndexes(options.graph, options.aliasMap);

  let resolvedCount = 0;
  let ambiguousCount = 0;
  let unresolvedCount = 0;

  const operations = inputOperations.map((operation) => {
    const sectionResolutions = (operation.targetSections ?? []).map((section) =>
      resolveSectionByKey(section.section_key, indexes)
    );

    const supportResolutions = collectSupportTargets(operation).map((support) => {
      const resolution = resolveEntityName(support.name, indexes);
      return {
        ...resolution,
        support_level: support.support_level,
      };
    });

    for (const item of [...sectionResolutions, ...supportResolutions]) {
      if (item.status === 'resolved') resolvedCount += 1;
      else if (item.status === 'ambiguous') ambiguousCount += 1;
      else unresolvedCount += 1;
    }

    return {
      seed_id: operation.seed_id ?? null,
      source_phase: operation.source_phase ?? null,
      sections: sectionResolutions,
      supports: supportResolutions,
    };
  });

  const warningLogs = [];
  for (const operation of operations) {
    for (const support of operation.supports) {
      if (support.status === 'ambiguous') {
        warningLogs.push({
          level: 'warning',
          code: 'SOURCEQUOTE_RESOLVE_SUPPORT_AMBIGUOUS',
          seed_id: operation.seed_id,
          support_name: support.input,
        });
      }
    }
  }

  const result = {
    stage: 'resolve',
    dryRun,
    status: 'ok',
    operations_read: inputOperations.length,
    operations,
    report: {
      resolved: resolvedCount,
      ambiguous: ambiguousCount,
      unresolved: unresolvedCount,
    },
    logs: [
      {
        level: 'info',
        code: 'SOURCEQUOTE_RESOLVE_READONLY',
        message: 'resolution completed without creating entities or relations',
      },
      ...warningLogs,
    ],
  };

  console.log(JSON.stringify(result));
  return result;
}
