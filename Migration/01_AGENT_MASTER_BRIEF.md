# Agent Master Brief — Story Mode for Graph Views

## Contexte

Tu travailles sur le repo `Website-Mael-Rolland.eth_V.1`, branche `claude/add-claude-documentation-EizOC`.

L’interface actuelle du graphe dispose déjà de modes d’exploration et d’outils de focus. L’objectif n’est donc pas de recréer un graphe narratif depuis zéro, mais d’ajouter un **moteur réutilisable de micro-récits** qui puisse guider la lecture de certaines vues existantes.

Le système doit être **maintenable**, **centralisé**, **sobre**, et **non destructif** vis-à-vis des fonctionnalités actuelles.

## Objectif principal

Implémenter un système de micro-récits pour plusieurs vues du graphe, avec navigation pas à pas, focus visuel, recentrage de caméra, et contenu textuel court.

## Objectifs secondaires

- améliorer la lisibilité du graphe pour des visiteurs non familiers du sujet ;
- transformer certaines vues analytiques en parcours de démonstration ;
- réutiliser autant que possible la logique existante de focus, de zoom et d’état d’interface ;
- permettre l’ajout futur de nouveaux récits sans refactor majeur.

## Vues prioritaires

1. `Monétisation des cryptomonnaies`
2. `Qui gouverne réellement ?`
3. `Crises`
4. `Structure de la thèse`

## Résultat attendu

Le résultat attendu est un système qui permet à un utilisateur de :

- lancer un récit adapté à la vue courante ;
- lire un court texte explicatif par étape ;
- voir le graphe se recentrer sur un nœud ou un petit cluster pertinent ;
- naviguer étape par étape ;
- quitter le récit et revenir à une exploration libre propre.

## Ce qu’il ne faut pas faire

- ne pas coder chaque récit directement dans plusieurs handlers UI dispersés ;
- ne pas écrire de longs pavés de texte ;
- ne pas introduire un système parallèle complètement séparé du focus existant ;
- ne pas modifier inutilement le JSON principal du graphe ;
- ne pas faire dépendre l’ensemble du dispositif d’identifiants fragiles sans fallback.

## Contraintes importantes

- aucune régression sur les modes existants ;
- aucun crash si un nœud demandé par un récit est absent ;
- architecture centralisée ;
- ajout futur d’un cinquième récit sans reconfiguration lourde.

## Livrables attendus

### A. Code

- système de registre central de récits ;
- intégration UI ;
- branchement au focus et à la caméra.

### B. Documentation minimale

- commentaires utiles dans le code ;
- mini rapport final décrivant les fichiers modifiés et les limites éventuelles.

### C. Vérification

- test manuel des 4 récits ;
- vérification des fallbacks ;
- vérification de l’absence de régression.

## Ordre d’implémentation recommandé

### Phase 1

- créer la structure de données des récits ;
- connecter cette structure à l’UI ;
- implémenter l’état narratif global.

### Phase 2

- brancher le focus de caméra ;
- ajouter les fallbacks ;
- vérifier la robustesse des transitions.

### Phase 3

- intégrer les récits `Monétisation` et `Qui gouverne réellement ?`.

### Phase 4

- intégrer les récits `Crises` et `Structure de la thèse`.

### Phase 5

- polir l’interface et documenter.

## Définition minimale du succès

Le travail est considéré comme réussi si :

- les 4 récits existent ;
- ils sont lisibles, navigables, stables ;
- ils déplacent effectivement le regard dans le graphe ;
- l’interface revient à un état propre lorsqu’on quitte un récit ;
- le système est réutilisable et non jetable.
