#!/usr/bin/env node

import fs from 'fs';
import path from 'path';

const ROOT = process.cwd();
const DECISION_DIR = path.join(ROOT, 'workshop', 'decisions', 'traces');
const NARRATIVE_DIR = path.join(ROOT, 'workshop', 'narratives', 'presets');

const REQUIRED_DECISION_FIELDS = [
  'id',
  'decisionText',
  'decisionType',
  'author',
  'date',
  'rationale',
  'affectedFiles',
  'status'
];

function listJsonFiles(dir) {
  if (!fs.existsSync(dir)) return [];
  return fs.readdirSync(dir)
    .filter((f) => f.endsWith('.json'))
    .map((f) => path.join(dir, f));
}

function readJson(file) {
  const raw = fs.readFileSync(file, 'utf8');
  return JSON.parse(raw);
}

function isNonEmptyString(v) {
  return typeof v === 'string' && v.trim().length > 0;
}

function validateDecisionTrace(doc, file) {
  const errors = [];

  for (const key of REQUIRED_DECISION_FIELDS) {
    if (!(key in doc)) errors.push(`missing required field: ${key}`);
  }

  if ('id' in doc && !isNonEmptyString(doc.id)) errors.push('id must be a non-empty string');
  if ('decisionText' in doc && !isNonEmptyString(doc.decisionText)) errors.push('decisionText must be a non-empty string');
  if ('decisionType' in doc && !isNonEmptyString(doc.decisionType)) errors.push('decisionType must be a non-empty string');
  if ('author' in doc && !isNonEmptyString(doc.author)) errors.push('author must be a non-empty string');
  if ('date' in doc && !isNonEmptyString(doc.date)) errors.push('date must be a non-empty string');
  if ('rationale' in doc && !isNonEmptyString(doc.rationale)) errors.push('rationale must be a non-empty string');
  if ('status' in doc && !isNonEmptyString(doc.status)) errors.push('status must be a non-empty string');

  if ('affectedFiles' in doc && !Array.isArray(doc.affectedFiles)) {
    errors.push('affectedFiles must be an array');
  }

  if ('affectedFiles' in doc && Array.isArray(doc.affectedFiles)) {
    const bad = doc.affectedFiles.find((v) => !isNonEmptyString(v));
    if (bad !== undefined) errors.push('affectedFiles entries must be non-empty strings');
  }

  return { file, errors };
}

function lintDirectorySyntax(files) {
  const parseErrors = [];
  const parsed = [];

  for (const file of files) {
    try {
      parsed.push({ file, doc: readJson(file) });
    } catch (err) {
      parseErrors.push({ file, error: err.message });
    }
  }

  return { parseErrors, parsed };
}

function rel(file) {
  return path.relative(ROOT, file);
}

function checkAffectedFilesExist(doc, file) {
  if (!Array.isArray(doc?.affectedFiles)) return [];
  const warnings = [];
  for (const target of doc.affectedFiles) {
    const full = path.join(ROOT, target);
    if (!fs.existsSync(full)) {
      warnings.push(`affectedFiles path not found: ${target}`);
    }
  }
  if (warnings.length) {
    console.warn(`WARN DecisionTrace: ${rel(file)}`);
    warnings.forEach((msg) => console.warn(`  - ${msg}`));
  }
  return warnings;
}

function main() {
  const decisionFiles = listJsonFiles(DECISION_DIR);
  const narrativeFiles = listJsonFiles(NARRATIVE_DIR);

  let hasFailure = false;
  let warningCount = 0;

  console.log('Workshop artifact lint');
  console.log(`- decisions:  ${decisionFiles.length} file(s)`);
  console.log(`- narratives: ${narrativeFiles.length} file(s)`);

  const decisionSyntax = lintDirectorySyntax(decisionFiles);
  const narrativeSyntax = lintDirectorySyntax(narrativeFiles);

  for (const e of [...decisionSyntax.parseErrors, ...narrativeSyntax.parseErrors]) {
    hasFailure = true;
    console.error(`FAIL JSON syntax: ${rel(e.file)} -> ${e.error}`);
  }

  for (const { file, doc } of decisionSyntax.parsed) {
    const result = validateDecisionTrace(doc, file);
    if (result.errors.length) {
      hasFailure = true;
      console.error(`FAIL DecisionTrace: ${rel(file)}`);
      result.errors.forEach((msg) => console.error(`  - ${msg}`));
    } else {
      console.log(`PASS DecisionTrace: ${rel(file)}`);
      warningCount += checkAffectedFilesExist(doc, file).length;
    }
  }

  for (const { file } of narrativeSyntax.parsed) {
    console.log(`PASS JSON syntax: ${rel(file)}`);
  }

  if (hasFailure) {
    console.error('Result: FAILED');
    process.exit(1);
  }

  if (warningCount > 0) {
    console.log(`Result: PASSED with ${warningCount} warning(s)`);
    return;
  }

  console.log('Result: PASSED');
}

main();
