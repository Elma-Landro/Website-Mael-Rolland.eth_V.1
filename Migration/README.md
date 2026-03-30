# Story mode hierarchy fix pack

Ce pack vise un problème précis du `Story mode` actuel : les étapes de récit révèlent trop d'arêtes à la fois, ce qui aplatit la hiérarchie visuelle et fait remonter des liaisons structurelles peu utiles pendant le parcours narratif.

Le pack contient :

- `01_DIAGNOSTIC.md` : diagnostic court du problème et principe de correction
- `02_IMPLEMENTATION_SPEC.md` : spécification technique de la correction
- `story-mode-focus.patch.js` : patch JS prêt à adapter dans `graphe.html`
- `story-mode-styles.patch.css` : styles Cytoscape à injecter / fusionner
- `story-presets.hierarchy.seed.mjs` : enrichissement suggéré des presets narratifs

Ordre conseillé pour l'implémenteur :

1. Lire `01_DIAGNOSTIC.md`
2. Lire `02_IMPLEMENTATION_SPEC.md`
3. Intégrer `story-mode-styles.patch.css`
4. Remplacer la logique `applyStoryFocus()` / `clearStoryFocus()` par `story-mode-focus.patch.js`
5. Enrichir les presets via `story-presets.hierarchy.seed.mjs`

Objectif attendu :

- moins de nœuds visibles par étape
- moins d'arêtes parasites
- hiérarchie visuelle claire : primaire / secondaire / arrière-plan
- disparition du sentiment de "tout est encore là" dans le récit
