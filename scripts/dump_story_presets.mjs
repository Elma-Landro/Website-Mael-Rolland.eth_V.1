#!/usr/bin/env node
// Emet en JSON ce que les recits guides referencent reellement.
//
// story-presets.mjs EST un module ES : Node peut l'importer. Deviner son
// contenu par expressions regulieres est inutilement fragile — et le prouve :
// les apostrophes typographiques des libelles francais cassent tout parsing
// naif a base de quotes simples. Ce fichier a d'ailleurs deja necessite deux
// commits de reparation de syntaxe pour cette raison exacte.
//
// graphe.story-helpers.js, lui, n'est pas un module : c'est une IIFE qui
// s'attache a `window`. On lui fournit un objet global factice et on le
// laisse s'enregistrer.
//
// Usage : node scripts/dump_story_presets.mjs [--repo <chemin>]
// Sortie : JSON sur stdout — { stories, steps, focusRefs, allowedRelationTypes, aliases }

import { readFileSync } from 'node:fs';
import { dirname, resolve } from 'node:path';
import { fileURLToPath, pathToFileURL } from 'node:url';
import { runInNewContext } from 'node:vm';

const ICI = dirname(fileURLToPath(import.meta.url));
const i = process.argv.indexOf('--repo');
const REPO = i !== -1 && process.argv[i + 1] ? resolve(process.argv[i + 1]) : resolve(ICI, '..');

function echec(message) {
  console.error(`ERREUR : ${message}`);
  process.exit(2);
}

// ---------- les presets ----------

let presets;
try {
  const mod = await import(pathToFileURL(resolve(REPO, 'story-presets.mjs')).href);
  presets = mod.STORY_PRESETS ?? mod.default;
} catch (err) {
  echec(`story-presets.mjs illisible : ${err.message}`);
}
if (!presets?.stories) echec('story-presets.mjs n\'expose pas STORY_PRESETS.stories');

const focusRefs = new Set();
const allowedRelationTypes = new Set();
let nbSteps = 0;

const collecte = (v) => {
  if (typeof v === 'string') focusRefs.add(v);
  else if (Array.isArray(v)) v.forEach(collecte);
};

for (const story of presets.stories) {
  collecte(story.centralNode);
  collecte(story.focusNodes);
  for (const rt of story.defaultStepOptions?.allowedRelationTypes ?? []) {
    allowedRelationTypes.add(rt);
  }
  for (const step of story.steps ?? []) {
    nbSteps += 1;
    collecte(step.centralNode);
    collecte(step.focusNodes);
    for (const rt of step.allowedRelationTypes ?? []) allowedRelationTypes.add(rt);
  }
}

// ---------- la table d'alias ----------

let aliases = {};
// Une table d'alias vide PAR ECHEC et une table vide PAR ABSENCE se
// ressemblent une fois serialisees — et la premiere transforme des
// references parfaitement resolues en fausses regressions. On distingue.
let aliasesOk = true;
try {
  const src = readFileSync(resolve(REPO, 'graphe.story-helpers.js'), 'utf8');
  const faux = { window: undefined, self: undefined, globalThis: undefined };
  faux.window = faux;
  faux.self = faux;
  faux.globalThis = faux;
  runInNewContext(src, faux, { timeout: 5000 });
  const table = faux.GrapheStoryHelpers?.STORY_FOCUS_ALIASES;
  if (!table) {
    aliasesOk = false;
    console.error("AVERTISSEMENT : graphe.story-helpers.js n'expose pas " +
                  'STORY_FOCUS_ALIASES — les references seront verifiees sans elle.');
  }
  aliases = table ?? {};
} catch (err) {
  aliasesOk = false;
  console.error(`AVERTISSEMENT : table d'alias illisible (${err.message}) — ` +
                'les references seront verifiees sans elle.');
}

process.stdout.write(JSON.stringify({
  stories: presets.stories.length,
  steps: nbSteps,
  focusRefs: [...focusRefs].sort(),
  allowedRelationTypes: [...allowedRelationTypes].sort(),
  aliases,
  aliasesOk,
}, null, 1) + '\n');
