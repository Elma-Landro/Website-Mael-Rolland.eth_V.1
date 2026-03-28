# Évaluation Minutieuse : Graphe GRC-20 (Branche `add-claude-documentation-EizOC`)

Cette évaluation porte sur la dernière version du graphe interactif de la thèse "Au-delà des codes" (v91 des données GRC-20). L'analyse croise l'inspection du code source (`graphe.html`), l'audit des données ontologiques (`grc20_v91.json`), et le rendu visuel en direct.

---

## 1. Analyse du Fond (Données et Ontologie)

L'audit des données révèle une ontologie riche (55 types d'entités, 130 types de relations) mais met en lumière des déséquilibres structurels qui impactent directement la visualisation.

### 1.1. Distribution des entités par chapitre
La fonction `buildChapterMap` tente d'assigner chaque entité à un chapitre via les relations `appears in section` (12 224 occurrences) et par propagation sémantique (BFS). Cependant, l'analyse montre que **la répartition est extrêmement inégale** :
*   **Chapitre I :** 569 entités liées
*   **Chapitre II :** 414 entités liées
*   **Chapitre III :** 338 entités liées
*   **Introduction :** 466 entités liées
*   **Conclusion :** 211 entités liées

**Problème identifié :** La ligne "Multi." (ou non-assignée) regroupe encore des entités qui échappent à l'algorithme de propagation. De plus, certains types (comme `InfrastructureEvent` ou `CrisisEvent`) sont forcés arbitrairement dans des chapitres spécifiques (Chap. I et Chap. III) via le dictionnaire `TYPE_CHAPTER_DEFAULTS` dans le code, ce qui masque les lacunes du JSON mais crée une rigidité sémantique.

### 1.2. Entités orphelines et relations manquantes
L'audit Python a révélé que **toutes les entités sont désormais connectées** (degré 0 = 0), ce qui est une excellente amélioration par rapport aux versions précédentes. Les hubs principaux (ex: *Bitcoin*, *Ethereum*, *Gouvernance polycentrique*) ont des degrés de connexion très élevés (jusqu'à 383 relations), ce qui justifie pleinement l'approche de dimensionnement proportionnel.

---

## 2. Analyse de la Forme (Esthétique et Vues)

L'esthétique globale a fait un bond en avant spectaculaire, se rapprochant fortement de la cible "Geo Protocol".

### 2.1. La Vue Matrice (Structure de la thèse)
*   **Ce qui fonctionne très bien :**
    *   **Halos croisés :** L'implémentation du `<canvas>` en arrière-plan pour dessiner les halos horizontaux (lignes de chapitres) croisés avec les halos verticaux (colonnes de types) crée un effet "matrice lumineuse" très réussi.
    *   **Jitter organique :** L'ajout d'un décalage aléatoire (`±18px` sur desktop) casse l'aspect "code-barres" et donne un rendu d'essaim naturel.
    *   **Taille proportionnelle :** Les nœuds ont maintenant une taille dynamique (`msize`) basée sur leur degré, ce qui fait ressortir les hubs de manière évidente.
*   **Améliorations potentielles :**
    *   **Opacité des arêtes :** Actuellement, les arêtes sont masquées (`display: none`) dans la vue Matrice. Pour un effet réseau complet, il faudrait les réactiver avec une opacité ultra-faible (`opacity: 0.02` ou `0.03`) et une couleur neutre.
    *   **Glow des hubs :** Le `shadow-blur` est plafonné. Pour que les gros nœuds "irradient" vraiment, le blur devrait être proportionnel à la taille du nœud (ex: `shadow-blur: Math.max(15, n.data('size') * 1.5)`).

### 2.2. La Vue Strates (Monétisation)
La nouvelle vue "Strates V2" est une addition majeure. Elle réorganise le graphe selon 6 strates analytiques (Noyau, Mécanismes, Médiations, Acteurs, Cas, Réf.).
*   **Problème identifié :** Le code force un positionnement strict sur l'axe X basé sur un biais "BTC à gauche / ETH à droite" (`STRATUM_CLUSTER_X`). Cela crée des colonnes très denses et des espaces vides importants. Un algorithme de force dirigée contraint (comme `cose` avec des bounding boxes) donnerait un résultat plus organique.

---

## 3. Analyse de l'UI et de l'Expérience Mobile

L'interface a été considérablement enrichie (Scrollytelling, Focus, Strates), mais cela crée des frictions sur mobile.

### 3.1. Frictions Mobile (≤ 768px)
L'inspection des Media Queries CSS révèle plusieurs points de blocage :
1.  **Taille des nœuds bridée :** Sur mobile, le code force `NODE_H = 10` et limite la taille maximale des nœuds (`Math.min(size, 8)`). Cela détruit la hiérarchie visuelle sur smartphone ; les hubs ne se distinguent plus des nœuds périphériques.
2.  **Glow désactivé :** Le `shadow-blur` est écrasé à `6` sur mobile pour des raisons de performance supposées, ce qui éteint l'effet néon.
3.  **Menu Outils envahissant :** Le dropdown `.tools-menu` prend jusqu'à `50vh` de l'écran, masquant le graphe lors de son utilisation.

### 3.2. Le Mode Scrollytelling (Récit)
L'intégration du panneau de texte synchronisé avec le graphe est excellente pour la narration. Cependant, sur mobile, le panneau `.scrolly-text-panel` est purement et simplement masqué (`display: none;` ligne 533). L'utilisateur mobile perd donc tout l'apport narratif.

---

## 4. Recommandations d'Améliorations (Actionnables)

Voici les modifications précises recommandées pour atteindre l'esthétique cible et corriger les frictions :

### 4.1. Débrider l'esthétique sur Mobile
Dans la fonction `applyMatriceLayout()`, modifier le calcul de taille pour conserver la proportionnalité sur mobile :
```javascript
// Remplacer :
const msize = isMobile ? Math.min(n.data('size') || 22, 8) : (n.data('size') || 22);
// Par :
const msize = isMobile ? Math.min(n.data('size') || 22, 16) : (n.data('size') || 22);
```
Dans `getCyStyle()`, augmenter le glow mobile :
```javascript
// Remplacer :
'shadow-blur': 6, 'shadow-opacity': 0.65
// Par :
'shadow-blur': 12, 'shadow-opacity': 0.8
```

### 4.2. Réactiver la texture réseau (Arêtes)
Dans `getCyStyle()`, pour le sélecteur `edge.in-matrix` :
```css
/* Remplacer 'display': 'none' par : */
'display': 'element',
'opacity': 0.02,
'line-color': '#ffffff',
'width': 0.5
```

### 4.3. Adapter le Scrollytelling au Mobile
Au lieu de masquer le panneau de texte sur mobile, le positionner en bas de l'écran (bottom sheet) avec une hauteur fixe (ex: `30vh`), laissant `70vh` pour le graphe interactif au-dessus.

### 4.4. Affiner l'algorithme de Chapitrage
Pour vider la ligne "Multi.", il faut réduire la dépendance aux `TYPE_CHAPTER_DEFAULTS` et augmenter la profondeur du BFS (passer de `hops >= 1` à `hops >= 2` dans `buildChapterMap`) pour permettre aux entités périphériques d'être "aspirées" par la gravité sémantique des chapitres.
