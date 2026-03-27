# Prompt pour l’agent implémenteur — ajouter une vue « Monétisation »

Tu travailles sur la page graphe du site de thèse.

## Objectif
Ajouter une **nouvelle vue** nommée **« Monétisation »**, en plus de la vue actuelle **« Structure de la thèse »**.

## Contrainte clé
- **Ne pas modifier ni dégrader** la vue existante « Structure de la thèse ».
- La nouvelle vue doit être **compatible avec l’esthétique actuelle** : rétro, lumineuse, nébuleuse, dense mais lisible.
- Il faut penser **mobile-first**.

## Intention analytique
La nouvelle vue doit organiser les entités selon un **gradient analytique de monétisation** plutôt que selon les chapitres.

Ordre visuel souhaité :
1. Noyau analytique
2. Mécanismes de monétisation
3. Arènes / médiations / infrastructures
4. Catégories analytiques d’acteurs
5. Cas empiriques / protocoles / crises / organisations
6. Personnes / références / sources

## À faire côté données
Ajouter ou calculer pour chaque nœud les métadonnées suivantes :
- `displayViewMonetisation.stratum`
- `displayViewMonetisation.cluster`
- `displayViewMonetisation.priority`
- `displayViewMonetisation.transversalityScore`
- `displayViewMonetisation.primaryChapter`

## Mapping initial recommandé
- Concept -> strate 1/2/3 selon importance analytique
- TheoreticFramework -> 1/2
- MonetaryObject -> 2
- Capability -> 2/3
- InfrastructureDomain -> 3
- GovernanceArena -> 3
- GovernanceProcess -> 3
- StakeholderCategory -> 4
- ActorGroup ou StakeholderGroup -> 5
- Protocol -> 5
- CrisisEvent -> 5
- Institution / Organization -> 5
- Person -> 6
- Reference / AcademicWork / PrimarySource / SourceQuote -> 6

## Overrides manuels minimum
Forcer explicitement :
- Monétisation -> 1
- Développement carnavalesque -> 1
- Gouvernance polycentrique -> 1
- Gouvernance duale -> 1
- Infrastructure sociotechnique -> 1
- Mise en crise -> 1
- Remise en ordre -> 1
- Logique de consensus distribué -> 1
- UCN BTC -> 2
- UCN ETH -> 2
- Passerelle / Gateway -> 2
- Bitcoin -> 5
- Ethereum -> 5
- The DAO -> 5
- CVE-2018-17144 -> 5
- Développeurs Core -> 4
- Mineurs -> 4
- Bourses d’échange -> 4
- Fournisseurs de portefeuilles -> 4

## Layout
Créer une vue semi-guidée :
- strates invisibles horizontales ou concentriques,
- jitter organique,
- clustering doux,
- halos légers,
- labels hiérarchisés.

Éviter une grille trop rigide.

## Palette
- strate 1 : ambre / or / blanc chaud
- strate 2 : orange / cuivre
- strate 3 : cyan / turquoise
- strate 4 : vert
- strate 5 : violet / magenta / rouge selon sous-famille
- strate 6 : teintes plus désaturées

Conserver éventuellement un accent secondaire par chapitre.

## Labels
Toujours visibles au niveau de zoom initial :
- Monétisation
- Bitcoin
- Ethereum
- Gouvernance polycentrique
- Développement carnavalesque
- Infrastructure sociotechnique
- Mise en crise
- Remise en ordre

Les autres labels doivent dépendre du zoom ou du focus.

## Liens à mettre visuellement en avant
Si le système de pondération des liens le permet, accentuer :
- enables
- mediates
- monetizes
- governs
- participatesIn
- belongsToCategory
- appliedToProtocol
- implementedBy
- testedByCrisis

## UI
Ajouter un bouton ou une carte de vue :
- titre : `Monétisation`
- sous-titre : `Vue thématique`

Positionner cette entrée près de « Structure de la thèse ».

## Mobile
Sur mobile :
- réduire le nombre de labels visibles au chargement,
- prévoir une vue d’ensemble lisible sans zoom immédiat,
- privilégier quelques amas bien distincts plutôt qu’une dispersion trop large.

## Définition de réussite
La vue est bonne si un visiteur comprend rapidement :
- que la thèse porte sur la monétisation des cryptomonnaies,
- que les concepts centraux ne sont pas confondus avec les personnes,
- que les catégories analytiques servent de médiation,
- que Bitcoin, Ethereum, les crises et les intermédiaires sont visibles comme cas structurants.
