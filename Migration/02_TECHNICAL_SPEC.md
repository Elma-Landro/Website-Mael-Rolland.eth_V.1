# Technical Specification — Reusable Story Mode

## 1. Principe général

Le story mode est un **surplomb narratif** appliqué à des vues existantes du graphe.

Il ne remplace ni le graphe, ni les modes actuels. Il ajoute une couche de lecture guidée.

Chaque récit est composé d’une séquence ordonnée d’étapes. Chaque étape comprend :

- un titre court ;
- un texte court ;
- un ou plusieurs nœuds à mettre en avant ;
- éventuellement des relations à mettre en avant ;
- éventuellement des filtres de vue ;
- un preset de caméra.

## 2. Architecture recommandée

## 2.1 Registre central

Créer un fichier dédié, par exemple :

- `story-presets.mjs`
- ou `story-presets.json`

Préférence : `story-presets.mjs` si la logique d’import/export et les commentaires doivent rester simples.

Le registre central doit contenir **tous** les récits.

## 2.2 Fichiers probables à modifier

- `graphe.html`
- `graph-worker.mjs` uniquement si réellement nécessaire
- nouveau fichier : `story-presets.mjs`

## 2.3 API interne suggérée

Le système doit disposer au minimum de fonctions logiques ou équivalents :

- `getStoryPresetById(storyId)`
- `openStory(storyId)`
- `closeStory()`
- `goToStoryStep(index)`
- `nextStoryStep()`
- `prevStoryStep()`
- `applyStoryStep(step)`
- `resolveFocusNodes(step.focusNodes)`
- `applyStoryFocus(resolvedTargets, cameraPreset)`
- `clearStoryFocus()`

Ces noms ne sont pas obligatoires, mais les responsabilités doivent exister.

## 3. Structure de données recommandée

```ts
export type StoryStep = {
  id: string
  title: string
  body: string
  focusNodes?: string[]
  focusRelations?: string[]
  cameraPreset?: "tight" | "cluster" | "wide"
  filters?: {
    column?: string
    row?: string
    band?: string
  }
  layoutOverride?: string
}

export type StoryPreset = {
  id: string
  label: string
  layoutTarget: string
  intro?: string
  steps: StoryStep[]
}
```

## 4. Gestion d’état

Le système doit maintenir un état narratif minimal et propre.

Structure suggérée :

```ts
const storyState = {
  activeStoryId: null,
  activeStoryStepIndex: -1,
  storyModeEnabled: false
}
```

## 4.1 À l’ouverture d’un récit

- définir `activeStoryId`
- définir `activeStoryStepIndex = 0`
- activer `storyModeEnabled`
- afficher le panneau du récit
- appliquer le focus de la première étape

## 4.2 À la fermeture d’un récit

- vider l’état narratif
- retirer les surbrillances spécifiques au récit
- retirer les atténuations spécifiques au récit
- préserver autant que possible la vue libre actuelle
- ne pas casser la sélection d’un nœud si elle existe indépendamment

## 5. Focus visuel

Le story mode doit réutiliser autant que possible les mécanismes de focus déjà présents.

À chaque étape :

- identifier les cibles ;
- recentrer la caméra ;
- mettre en avant les cibles ;
- atténuer le reste sans rendre le graphe illisible.

## 5.1 Presets de caméra

- `tight` : focalisation forte sur 1 nœud ou un mini cluster
- `cluster` : focus intermédiaire sur un petit ensemble cohérent
- `wide` : vue élargie, utile pour étapes de synthèse

## 6. Fallbacks obligatoires

## 6.1 Nœud absent

Si un nœud demandé n’existe pas :

- ne jamais planter ;
- faire un `console.warn` avec l’identifiant ou le nom manquant ;
- afficher quand même l’étape ;
- utiliser un focus de repli (vue actuelle ou vue cluster large).

## 6.2 Relation absente

- ne pas planter ;
- ignorer la relation absente ;
- logger un warning si utile.

## 6.3 Ambiguïté de matching

Prévoir une résolution robuste :

1. id exact
2. nom exact
3. nom normalisé (casse et accents neutralisés)
4. si plusieurs candidats restent possibles, prendre le premier résultat stable et logger un warning

## 7. UI minimale attendue

Le panneau récit doit être léger et fonctionnel.

Il doit afficher :

- le titre du récit ;
- éventuellement un petit intro ;
- le numéro d’étape ;
- le titre de l’étape ;
- le texte de l’étape ;
- boutons `Précédent`, `Suivant`, `Quitter`.

## 7.1 Règles UX

- ne pas créer une grosse modale lourde ;
- garder le graphe visible en permanence ;
- éviter le texte long ;
- permettre la lecture rapide.

## 8. Style éditorial des étapes

- titre court ;
- 2 à 4 phrases max ;
- une idée analytique par étape ;
- ton sobre, affirmatif, analytique.

## 9. Compatibilité et maintenance

Le système doit pouvoir accueillir facilement :

- un 5e récit ;
- un récit court temporaire ;
- des récits spécialisés par sous-vue.

L’ajout d’un récit ne doit pas nécessiter de modifier profondément l’UI ou l’état global.

## 10. Plan de commits conseillé

### Commit 1
`feat(graph): add reusable story preset registry`

### Commit 2
`feat(ui): add story state and navigation panel`

### Commit 3
`feat(focus): connect story steps to graph focus and camera transitions`

### Commit 4
`feat(stories): add monetisation and who-governs story presets`

### Commit 5
`feat(stories): add crises and thesis-structure story presets`

### Commit 6
`chore(ui): add fallbacks warnings and polish story mode`
