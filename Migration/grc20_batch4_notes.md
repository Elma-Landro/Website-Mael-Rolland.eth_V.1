# Batch 4 — dataviz, focus, densité, labels et budgets visuels

Ce batch est consacré à la **qualité de lecture visuelle** du graphe, sans abandonner les corrections analytiques précédentes.

## Fichiers
- `grc20_dataviz_overrides_batch4.*`
- `grc20_focus_presets_batch4.json`

## Nombre de règles
42

## Objet du batch
Répondre au problème identifié sur les dernières captures :
- certaines vues sont devenues plus lourdes, plus rigides, plus “briques” ;
- l’explode circulaire devient vite illisible ;
- les labels restent insuffisamment lisibles sur mobile ;
- la nouvelle ontologie manque encore de traduction visuelle équilibrée.

## Axes principaux
1. **Budget visuel par cellule**
   - ne pas tout afficher avec la même intensité ;
   - distinguer premier plan / arrière-plan / agrégation légère.

2. **Nuages contenus plutôt que blocs pleins**
   - restaurer une texture plus poreuse et organique ;
   - éviter les murs compacts.

3. **Éclatement structuré**
   - abandon du simple paquet circulaire pour les sélections denses ;
   - micro-clusters / sous-zones / packing local.

4. **Labels utiles**
   - toujours visibles pour les nœuds-clés ;
   - plus nombreux dans les focus ;
   - troncature intelligente ;
   - nom complet au tap/click.

5. **Mobile-first**
   - focus compact ;
   - chips de résumé ;
   - bounding box locale ;
   - densité contrôlée.

6. **Présets**
   - ensembles de focus utiles pour corriger rapidement le graphe.

## Consignes d’usage
- appliquer d’abord les règles `priority = high`
- ensuite régler les budgets de largeur / densité par vue
- enfin tester en mobile :
  - Structure de la thèse
  - Monétisation des CM
  - Qui gouverne réellement ?

## Point de doctrine
L’objectif n’est pas de revenir à l’ancien graphe.
L’objectif est de récupérer son **souffle visuel** tout en gardant la **rigueur ontologique** nouvelle.
