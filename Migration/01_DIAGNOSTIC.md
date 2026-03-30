# Diagnostic — pourquoi le récit paraît encore trop chargé

## 1. Problème observé

Le `Story mode` actuel met bien en place un focus narratif, mais il conserve trop de présence graphique autour des nœuds ciblés.

Le symptôme principal est le suivant :

- un petit noyau de nœuds est bien mis en avant
- mais de nombreuses arêtes restent visibles dès qu'elles touchent un nœud ciblé
- des liaisons structurelles répétitives (par exemple les liens de chapitre vers la thèse ou vers des nœuds centraux) réapparaissent presque à chaque étape
- le regard n'est donc pas assez contraint
- la hiérarchie primaire / secondaire / décor n'est pas assez lisible

## 2. Cause probable dans l'implémentation actuelle

La logique actuelle semble faire ceci :

- tous les nœuds ciblés reçoivent `highlighted`
- tous les autres nœuds reçoivent `faded`
- toute arête dont **la source OU la cible** appartient au set ciblé reçoit `highlighted`
- toutes les autres arêtes reçoivent `faded`

Conséquence : dès qu'un nœud central ou très connecté est ciblé, un éventail d'arêtes ressort immédiatement, y compris des liens peu utiles pour le récit en cours.

## 3. Pourquoi cela aplatit le récit

Le problème n'est pas seulement "trop d'arêtes". C'est surtout un problème de **niveau de lecture**.

Aujourd'hui, le système distingue seulement :

- mis en avant
- atténué

Mais un récit guidé a en réalité besoin d'au moins **quatre niveaux** :

1. **primaire** : ce qui constitue exactement l'étape
2. **secondaire** : voisinage utile, optionnel
3. **backbone** : structure générale gardée à peine visible
4. **masqué** : ce qui doit disparaître pour cette étape

Sans cela, chaque étape continue de montrer trop du graphe global.

## 4. Effet gênant typique

Sur `Structure de la thèse`, si un chapitre est focalisé mais que le nœud central de thèse reste relié visiblement à presque tout, on obtient :

- une répétition graphique des mêmes arêtes
- une sensation de redondance
- un récit moins net
- une impression que le zoom change, mais que la structure n'est jamais vraiment filtrée

## 5. Correction recommandée

Il faut passer d'un focus binaire à un **focus hiérarchisé** avec classes de récit dédiées :

- `story-primary`
- `story-secondary`
- `story-backbone`
- `story-muted`
- `story-hidden`

Et piloter le rendu de chaque étape avec des options par step :

- `edgeMode: 'strict' | 'neighbors' | 'context'`
- `includeNeighbors: boolean`
- `secondaryDepth: 1 | 2`
- `hideRelationTypes: []`
- `showRelationTypes: []`
- `hideBackbone: boolean`
- `maxSecondaryPerTarget`

## 6. Principe simple à retenir

Pour la plupart des étapes de récit :

- ne montrer **que** les nœuds ciblés
- ne montrer **que** les arêtes entre eux
- masquer presque totalement le reste

Puis n'autoriser le voisinage ou le contexte que pour certaines étapes où cela a un sens analytique.
