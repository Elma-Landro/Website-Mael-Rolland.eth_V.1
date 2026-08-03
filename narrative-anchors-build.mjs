#!/usr/bin/env node
/**
 * narrative-anchors-build.mjs
 *
 * Derives NarrativeAnchor objects from the GRC-20 knowledge graph JSON.
 *
 * A NarrativeAnchor binds together:
 *   - a SourceQuote (paginated, verbatim)
 *   - the entity/entities it supports (via "quote supports" relations)
 *   - the thesis section it appears in (via "appears in section" relations)
 *   - a graph scene definition (focusNodes, camera, edge mode)
 *   - reader and story labels
 *
 * The output (narrative-anchors.json) is consumed by:
 *   - lecteur.html  — shows quote in entity panel, links to graph
 *   - graphe.html   — drives anchor sub-sections in scrollytelling
 *   - story-presets.mjs — can reference anchors by ID in story steps
 *
 * Usage:
 *   node narrative-anchors-build.mjs [--input ./grc20-these-mael-rolland-v106.json] [--out ./narrative-anchors.json]
 */

import fs from 'fs';
import path from 'path';

// ── CLI args ──────────────────────────────────────────────────────────────────
const args = process.argv.slice(2);
const inputFlag  = args.indexOf('--input');
const outputFlag = args.indexOf('--out');
const INPUT  = inputFlag  !== -1 ? args[inputFlag + 1]  : './grc20-these-mael-rolland-v106.json';
const OUTPUT = outputFlag !== -1 ? args[outputFlag + 1] : './narrative-anchors.json';

console.log(`Reading ${INPUT}…`);
const raw = JSON.parse(fs.readFileSync(INPUT, 'utf-8'));

// ── Indexes ───────────────────────────────────────────────────────────────────
const typeById     = Object.fromEntries(raw.types.map(t => [t.id, t.name]));
const rtByName     = Object.fromEntries(raw.relation_types.map(rt => [rt.name, rt.id]));
const entityById   = Object.fromEntries(raw.entities.map(e => [e.id, e]));

// Index relations by source entity
const relsFrom = {};
for (const r of raw.relations) {
  if (!relsFrom[r.from]) relsFrom[r.from] = [];
  relsFrom[r.from].push(r);
}

const SQ_TYPE_ID       = raw.types.find(t => t.name === 'SourceQuote')?.id;
const QUOTE_SUPPORTS   = rtByName['quote supports'];
const APPEARS_IN       = rtByName['appears in section'];

if (!SQ_TYPE_ID)     throw new Error('SourceQuote type not found in input JSON');
if (!QUOTE_SUPPORTS) throw new Error('"quote supports" relation type not found');
if (!APPEARS_IN)     throw new Error('"appears in section" relation type not found');

// Entity types that cannot serve as primary narrative entities
const SKIP_PRIMARY = new Set([
  'SourceQuote', 'Reference', 'DoctoralThesis',
  'Chapter', 'ThesisSection', 'AcademicWork',
  'GreyLiterature', 'IndigenousLiterature',
]);

// ── Chapter key normalisation ─────────────────────────────────────────────────
// The `chapter` attribute in SourceQuotes uses varied naming conventions.
// Normalise to canonical keys used in graphe.html chapter IDs.
const CHAPTER_CANONICAL = {
  'introduction générale': 'intro',
  'introduction':          'intro',
  'intro':                 'intro',
  'chapitre i':            'ch1',
  'chapitre 1':            'ch1',
  'chap1':                 'ch1',
  'chapitre ii':           'ch2',
  'chapitre 2':            'ch2',
  'chap2':                 'ch2',
  'chapitre iii':          'ch3',
  'chapitre 3':            'ch3',
  'chap3':                 'ch3',
  'conclusion générale':   'ccl',
  'conclusion':            'ccl',
};

function normaliseChapter(raw) {
  if (!raw) return null;
  const key = raw.toLowerCase().trim();
  return CHAPTER_CANONICAL[key] || null;
}

// ── Chapter entity IDs (from graphe.html CHAPTER_IDS constant) ───────────────
const CHAPTER_ENTITY_IDS = {
  'intro': 'df405dcd975b406486a260da72f1ad4a',
  'ch1':   'a2c452a77b394a9d836eed0e16ed5851',
  'ch2':   '5b5935bc3ede49028b7dfbdaa4f34b6d',
  'ch3':   '444d654ce38c41c7a277d883c77ba41b',
  'ccl':   '6b64e26836434471917262334655952c',
};

// ── Attribute helper ──────────────────────────────────────────────────────────
function attrVal(attrs, key) {
  if (!attrs) return null;
  const v = attrs[key];
  if (!v) return null;
  if (typeof v === 'object' && 'value' in v) return v.value;
  return String(v);
}

// ── Build anchors ─────────────────────────────────────────────────────────────
const allAnchors = [];

for (const e of raw.entities) {
  if (!(e.types || []).includes(SQ_TYPE_ID)) continue;

  const attrs     = e.attributes || {};
  const quoteText = attrVal(attrs, 'quoteText');
  if (!quoteText || quoteText.length < 60) continue;

  // Parse page number
  const rawPage = attrVal(attrs, 'page') || '';
  let page = parseInt(String(rawPage).replace(/[^\d].*$/, '').trim(), 10);
  if (isNaN(page)) page = null;

  const chapter      = attrVal(attrs, 'chapter') || '';
  const thesisLoc    = attrVal(attrs, 'thesisLocation') || '';
  const chapterKey   = normaliseChapter(chapter);

  // Supported entities (primary + secondary)
  const supportRels  = (relsFrom[e.id] || []).filter(r => r.type === QUOTE_SUPPORTS);
  const supported    = supportRels
    .map(r => entityById[r.to])
    .filter(s => s && !SKIP_PRIMARY.has(typeById[(s.types || [])[0]]));

  if (supported.length === 0) continue;

  // Section entity
  const secRels      = (relsFrom[e.id] || []).filter(r => r.type === APPEARS_IN);
  const secEntity    = secRels.length ? entityById[secRels[0].to] : null;
  const sectionKey   = secEntity?.name || null;

  const primary      = supported[0];
  const secondary    = supported.slice(1, 3);
  const primaryType  = typeById[(primary.types || [])[0]] || 'Unknown';

  const focusNodes   = [primary.name, ...secondary.map(s => s.name)];

  allAnchors.push({
    id:               `anchor-${e.id.slice(0, 8)}`,
    sourceQuoteId:    e.id,
    chapterKey:       chapterKey,
    chapterEntityId:  chapterKey ? CHAPTER_ENTITY_IDS[chapterKey] : null,
    sectionKey:       sectionKey,
    page:             page,
    chapter:          chapter,
    thesisLocation:   thesisLoc,
    quoteText:        quoteText,
    primaryEntityId:  primary.id,
    primaryEntityName: primary.name,
    primaryEntityType: primaryType,
    secondaryEntityIds:   secondary.map(s => s.id),
    secondaryEntityNames: secondary.map(s => s.name),
    bridgeEntityIds:  [],
    readerLabel:      primary.name,
    storyTitle:       primary.name,
    // storyBody is the quote itself — consumers may truncate as needed
    storyBody:        quoteText,
    featured:         false,   // set to true for scrolly-featured anchors below
    graphScene: {
      id:              `scene-${e.id.slice(0, 8)}`,
      focusNodes,
      cameraPreset:   secondary.length > 1 ? 'cluster' : 'tight',
      edgeMode:       'neighbors',
      includeNeighbors: true,
      secondaryDepth: 1,
    },
  });
}

// ── Sort by page (narrative order) ───────────────────────────────────────────
allAnchors.sort((a, b) => (a.page ?? 9999) - (b.page ?? 9999));

// ── Deduplicate by primaryEntityId (keep first = earliest page) ──────────────
const seenPrimary = new Set();
const dedupedAnchors = [];
for (const a of allAnchors) {
  if (!seenPrimary.has(a.primaryEntityId)) {
    seenPrimary.add(a.primaryEntityId);
    dedupedAnchors.push(a);
  }
}

// ── Select featured anchors (2–3 per chapter for scrollytelling) ──────────────
// Selection criteria: long quoteText + multi-entity support + core types
const FEATURED_TYPES = new Set([
  'Concept', 'TheoreticFramework', 'Argument', 'GovernanceProcess',
  'GovernanceArena', 'Protocol', 'CrisisEvent', 'NarrativeCluster',
  'InfrastructureDomain', 'GovernanceConflict',
]);

const FEATURED_PER_CHAPTER = { intro: 2, ch1: 3, ch2: 3, ch3: 3, ccl: 2 };

const featuredByChapter = { intro: [], ch1: [], ch2: [], ch3: [], ccl: [] };

// Score anchors: prefer longer quotes, core entity types, more secondary entities
function anchorScore(a) {
  let s = Math.min(a.quoteText.length, 400) / 400;   // 0–1 based on quote length
  if (FEATURED_TYPES.has(a.primaryEntityType)) s += 0.5;
  s += a.secondaryEntityIds.length * 0.2;
  return s;
}

const sorted = [...dedupedAnchors].sort((a, b) => anchorScore(b) - anchorScore(a));

for (const a of sorted) {
  if (!a.chapterKey || !featuredByChapter[a.chapterKey]) continue;
  const bucket = featuredByChapter[a.chapterKey];
  if (bucket.length < FEATURED_PER_CHAPTER[a.chapterKey]) {
    bucket.push(a.id);
  }
}

// Mark featured + re-sort by page within each chapter group
const featuredIds = new Set(Object.values(featuredByChapter).flat());
for (const a of dedupedAnchors) {
  if (featuredIds.has(a.id)) a.featured = true;
}

// ── Stats ─────────────────────────────────────────────────────────────────────
const byChapter = {};
for (const a of dedupedAnchors) {
  byChapter[a.chapterKey || 'unknown'] = (byChapter[a.chapterKey || 'unknown'] || 0) + 1;
}

console.log(`\nGenerated ${dedupedAnchors.length} NarrativeAnchors from ${raw.entities.filter(e => (e.types || []).includes(SQ_TYPE_ID)).length} SourceQuotes`);
console.log('Distribution by chapter:');
for (const [k, n] of Object.entries(byChapter)) {
  const feat = dedupedAnchors.filter(a => a.chapterKey === k && a.featured).length;
  console.log(`  ${k}: ${n} total, ${feat} featured`);
}

// ── Write output ──────────────────────────────────────────────────────────────
const output = {
  version:        '1',
  generated_from: path.basename(INPUT),
  generated_at:   new Date().toISOString(),
  total:          dedupedAnchors.length,
  featured_ids:   [...featuredIds],
  anchors:        dedupedAnchors,
};

fs.writeFileSync(OUTPUT, JSON.stringify(output, null, 2), 'utf-8');
console.log(`\nWritten to ${OUTPUT}`);
