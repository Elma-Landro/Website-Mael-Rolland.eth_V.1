# Spécification visuelle — Vue Monétisation (matrice processuelle)

## Principe général
Cette vue doit rendre intelligible le processus de monétisation décrit dans la thèse.
Elle n’est pas une vue par types d’entités.
Elle est une vue par étapes du processus et par niveaux d’incarnation analytique.

## Géométrie
- Matrice 6 colonnes × 6 lignes
- Marge latérale suffisante pour afficher les labels de lignes
- En-têtes de colonnes lisibles immédiatement
- Labels de lignes alignés à gauche
- Léger halo par colonne pour produire un flux visuel de gauche à droite

## Colonnes
1. Émission
2. Circulation
3. Accès
4. Usages
5. Valorisation
6. Stabilisation

## Lignes
1. Thèse
2. Mécanismes
3. Infrastructures
4. Acteurs
5. Cas
6. Figures

## Lisibilité mobile
- Police de titres de colonnes plus grande que celle des labels d’entités
- Interdire les titres obliques trop inclinés
- Préférer horizontal ou 10–15° max
- Les labels de lignes doivent rester visibles même si le nuage est dense

## Hiérarchie interne de la ligne Figures
Sous-zone A : Figures agissantes
Sous-zone B : Références théoriques
Différences visuelles :
- figures agissantes : plus saturées, plus proches des colonnes d’action
- références : opacité réduite, dérive légère vers le bord droit ou bas

## Hiérarchie interne de la ligne Acteurs
Ordre vertical interne recommandé :
- catégories analytiques
- organisations / institutions
- groupes empiriques
Ne pas mélanger sans structure.

## Hiérarchie interne de la ligne Infrastructures
Ordre vertical interne recommandé :
- dispositifs natifs
- services / médiations
- arènes de coordination / maintenance

## Règles de densité
- Ligne Thèse : très faible densité
- Ligne Mécanismes : faible à moyenne
- Ligne Infrastructures : moyenne
- Ligne Acteurs : moyenne
- Ligne Cas : moyenne à forte
- Ligne Figures : forte, mais structurée

## Couleurs
Palette recommandée par colonne :
- Émission : #f2b84b
- Circulation : #ffd166
- Accès : #21d4fd
- Usages : #45d483
- Valorisation : #b56cff
- Stabilisation : #ff7b54

## Animation / interaction
- Hover : faire ressortir la case de la matrice et les liens directs
- Focus sur un nœud : surligner sa colonne principale et sa ligne principale
- Filtres : permettre de restreindre par colonne, par ligne, et par protocole

## Placement transversaux
Les entités transversales gardent une case principale et peuvent avoir :
- secondaryColumn
- secondaryRow
Le rendu doit rester dominé par la case principale.

## Résultat attendu
Au premier coup d’œil, on doit comprendre :
1. que la monnaie se fabrique par étapes ;
2. que chaque étape mobilise concepts, mécanismes, infrastructures, acteurs, cas et figures ;
3. que la stabilisation n’est pas secondaire mais constitutive de la monétisation.
