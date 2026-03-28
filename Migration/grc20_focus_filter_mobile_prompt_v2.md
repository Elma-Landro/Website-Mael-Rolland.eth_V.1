# Prompt agent implémenteur — mode filtre / éclatement mobile-first + labels lisibles

Tu dois implémenter un **mode transversal de filtre ciblé / éclatement** utilisable dans les vues du graphe, avec une contrainte absolue :

## CONTRAINTE ABSOLUE
Le dispositif doit être **lisible sur mobile** sans prendre trop de place sur le graphe lui-même.

Le mobile n’est pas un cas secondaire : c’est un **test principal**.
Le système doit donc être :
- visible quand on en a besoin ;
- discret quand on n’en a pas besoin ;
- compréhensible au premier coup d’œil ;
- non envahissant.

---

## 1. Objectif fonctionnel
Permettre de sélectionner finement une partie du graphe pour la voir isolée ou éclatée.

Exemples :
- voir seulement les **acteurs du chapitre I**
- voir seulement les **concepts de la conclusion**
- voir seulement les **arènes de gouvernance du chapitre III**
- voir seulement les **cas de stabilisation** dans la vue Monétisation
- voir seulement une **cellule précise** (ligne + colonne)

Le but est aussi la **correction éditoriale** du graphe :
- repérer les entités mal classées
- repérer les trous
- repérer les colonnes trop denses ou trop vides
- vérifier visuellement la cohérence des placements

---

## 2. Principe général
Ne pas créer une vue totalement séparée.
Créer un **mode transversal** activable depuis les vues existantes :
- Structure de la thèse
- Monétisation des CM
- Qui gouverne réellement ?

Ajouter un bouton global discret du type :
- `Focus`
- ou `Filtrer`
- ou `Isoler`

Ce bouton ouvre un **panneau léger** ou un **drawer compact**.

---

## 3. Contraintes UX mobile-first

### 3.1 Le graphe doit rester central
Éviter :
- gros panneaux fixes
- gros blocs de formulaires visibles en permanence
- overlays opaques qui masquent le graphe
- menus qui prennent la moitié de la hauteur en continu

### 3.2 Le panneau filtre doit être discret
Sur mobile :
- utiliser un **drawer repliable**
- ou un **bottom sheet compact**
- ou une **rangée de chips/filtres escamotable**

Comportement recommandé :
- état fermé : seulement un bouton discret `Focus`
- état ouvert : panneau compact avec filtres essentiels
- état appliqué : résumé visuel minimal sous forme de chips

Exemple de résumé :
`Chap. I` · `Acteurs` · `Éclater`

### 3.3 Le panneau ne doit pas monopoliser l’écran
Hauteur recommandée :
- fermé : 1 ligne / bouton
- ouvert : 20 à 35 % de la hauteur max
- jamais plein écran par défaut

### 3.4 Priorité à la manipulation simple
Préférer :
- menus déroulants courts
- chips sélectionnables
- toggles
- boutons radio simples
- presets

---

## 4. Filtres à proposer

### 4.1 Vue
Champ :
- `Vue`

Valeurs :
- Structure de la thèse
- Monétisation des CM
- Qui gouverne réellement ?

### 4.2 Bande / chapitre / zone principale
Pour Structure de la thèse :
- Intro.
- Chap. I
- Chap. II
- Chap. III
- Concl.
- Multi.

### 4.3 Colonne
Toujours proposer un filtre `Colonne`.

Pour Structure de la thèse :
- Chap.
- Struct.
- Objets
- Gouvern.
- Acteurs
- Concepts
- Réf./Sources

Pour Monétisation :
- Noyau
- Émission
- Circulation
- Accès
- Usages
- Valorisation
- Stabilisation

Pour Qui gouverne réellement ? :
- Struct.
- Gouvern.
- Catégories
- Organisations
- Groupes
- Arènes
- Personnes
- Cas / Réf.

### 4.4 Ligne
Toujours proposer un filtre `Ligne` si la vue active en a une structure lisible.

Pour Monétisation :
- Thèse
- Dispositifs
- Arènes
- Acteurs
- Cas
- Réf.

Pour Qui gouverne réellement ? :
- Problématisation
- Coordination
- Décision
- Conflit
- Maintenance
- Sources

### 4.5 Type (optionnel)
Filtre facultatif :
- Person
- StakeholderCategory
- StakeholderGroup
- Institution
- Organization
- GovernanceArena
- GovernanceProcess
- CrisisEvent
- Concept
- Reference

Ce filtre doit rester dans une zone “plus d’options”.

---

## 5. Modes d’affichage de la sélection

### 5.1 Mode `Isoler`
N’afficher nettement que la sélection.
Le reste devient très pâle.

### 5.2 Mode `Éclater`
La sélection est recentrée et espacée.
Les nœuds sélectionnés :
- augmentent légèrement de taille
- s’écartent davantage
- deviennent plus lisibles
- peuvent afficher plus facilement leurs labels

### 5.3 Mode `Contexte`
La sélection est mise en avant, mais le reste reste visible en arrière-plan à opacité réduite.

---

## 6. EXIGENCE SUPPLÉMENTAIRE CRUCIALE : labels des nœuds

### 6.1 À l’œil nu, il faut pouvoir voir un peu ce que c’est
Chaque nœud ou au moins une partie significative des nœuds doit pouvoir donner **un aperçu visuel de son nom**.

On ne veut pas seulement des points colorés.
On veut que l’utilisateur puisse, d’un coup d’œil, reconnaître au moins partiellement ce qu’il regarde.

### 6.2 En mode normal
- garder un affichage sobre
- afficher les labels seulement pour les nœuds les plus structurants ou suffisamment isolés
- éviter la bouillie textuelle

### 6.3 En mode `Éclater`
C’est ici que les labels doivent devenir vraiment utiles :
- afficher davantage de labels
- priorité aux nœuds sélectionnés
- si nécessaire, afficher :
  - nom complet pour les nœuds majeurs
  - nom tronqué intelligent pour les autres
- éviter les chevauchements

### 6.4 Stratégie recommandée
Prévoir un système hiérarchique :
1. labels toujours visibles pour les nœuds-clés
2. labels contextuels pour les nœuds sélectionnés
3. labels partiels/tronqués si la densité est forte
4. labels complets au tap / hover / clic

### 6.5 Le bon éclatement est central
Le mode `Éclater` ne doit pas seulement espacer les nœuds.
Il doit permettre **une lecture minimale des noms**.

Donc :
- augmenter l’espacement
- optimiser la collision des labels
- autoriser une légère redistribution locale
- privilégier la lisibilité à la pure symétrie géométrique

---

## 7. Couleurs : double logique obligatoire

La couleur ne doit pas être arbitraire.
Elle doit continuer à encoder deux choses :

### 7.1 Couleur principale = chapitre / bande
Comme d’habitude, chaque nœud doit garder une couleur principale liée à son chapitre ou à sa bande principale.

### 7.2 Nuance / modulation = colonne
À l’intérieur de cette couleur chapitrale, il faut une variation liée à la colonne.

Exemple :
- même famille de couleur pour `Chap. II`
- mais nuances distinctes entre `Acteurs`, `Concepts`, `Gouvern.`, `Réf./Sources`

Autrement dit :
- **chapitre = famille chromatique**
- **colonne = variante / teinte / intensité / modulation**

### 7.3 Objectif
Au premier coup d’œil, on doit comprendre :
- d’où vient le nœud dans la thèse
- dans quelle famille de la vue il se situe

---

## 8. Rendu visuel recommandé

### 8.1 Résumé minimal toujours visible
Quand un filtre est actif, afficher un résumé ultra léger :
`Focus : Chap. I · Acteurs · Éclater`

Ce résumé doit pouvoir être fermé rapidement avec un `×`.

### 8.2 Ne pas dupliquer les titres partout
Ne pas afficher de grands blocs de titres ni de longues phrases sur la carte.
L’information doit être condensée dans :
- le panneau repliable
- les chips
- le petit résumé d’état

### 8.3 Labels de nœuds
En mode normal :
- rester sobres

En mode `Éclater` :
- autoriser plus de labels
- mais seulement pour la sélection

### 8.4 Animation
Prévoir une transition douce entre :
- vue normale
- vue filtrée
- vue éclatée

Animation courte, pas envahissante.

---

## 9. Presets rapides

### Structure de la thèse
- Acteurs du Chap. I
- Concepts du Chap. II
- Gouvernance du Chap. III
- Références de la conclusion

### Monétisation
- Usages
- Stabilisation
- Acteurs de la valorisation
- Cas de la circulation

### Qui gouverne réellement ?
- Personnes en décision
- Arènes de maintenance
- Groupes en conflit
- Catégories du pouvoir distribué

---

## 10. Hiérarchie d’interface recommandée

### État fermé
Afficher seulement :
- un bouton `Focus`
- éventuellement une petite icône de filtre

### État ouvert compact
Afficher :
- Vue
- Bande / chapitre (si pertinent)
- Colonne
- Ligne
- Affichage
- boutons `Appliquer` et `Réinitialiser`

### État avancé
Zone repliable “Options avancées” :
- Type
- multi-sélection
- opacité du contexte
- taille de l’éclatement
- afficher/masquer labels
- niveau de densité des labels

---

## 11. Règles de conception

### 11.1 L’utilisateur doit pouvoir corriger vite
Le système doit permettre 2 à 4 gestes maximum pour obtenir une vue utile.

Exemple idéal :
`Focus` → `Chap. I` → `Acteurs` → `Éclater`

### 11.2 Pas d’effet gadget
Le mode filtre doit être un **outil de travail**.

### 11.3 Respecter l’esthétique existante
Conserver :
- halos
- palette
- ambiance rétro-pixel
- centralité du graphe

### 11.4 Accessibilité visuelle
Tester particulièrement sur petit écran :
- lisibilité des chips
- contraste des labels
- taille des zones tactiles
- clarté du bouton de fermeture / reset

---

## 12. Comportement technique attendu
Prévoir :
- un état global `focusMode`
- une sélection :
  - `activeView`
  - `selectedBand`
  - `selectedColumn`
  - `selectedRow`
  - `selectedType`
  - `displayMode`
- une fonction de filtrage des nœuds
- une fonction de rendu :
  - normal
  - isolé
  - éclaté
  - contexte

Prévoir aussi :
- persistance légère de la sélection tant que l’utilisateur reste sur la page
- reset rapide en un clic

Ajouter des paramètres de labels :
- `labelDensity`
- `showLabelsInExplodeMode`
- `alwaysLabelKeyNodes`
- `truncateLabelsSmartly`

Ajouter aussi une logique de double couleur :
- `chapterColor`
- `columnVariant`

---

## 13. Deliverables attendus
1. ajout du bouton / panneau de filtre mobile-first
2. logique de filtrage compatible avec les 3 vues
3. mode `Isoler`
4. mode `Éclater`
5. mode `Contexte`
6. presets rapides
7. résumé compact de la sélection active
8. gestion intelligente des labels
9. maintien du codage couleur chapitre + colonne
10. conservation de la lisibilité mobile et de l’esthétique du site

---

## 14. Critère de réussite
Sur mobile, un utilisateur doit pouvoir :
- ouvrir le focus en un geste
- sélectionner une sous-partie du graphe en quelques taps
- voir immédiatement une constellation plus lisible
- reconnaître au moins partiellement ce que sont les nœuds grâce aux labels
- fermer le focus sans perdre la vue globale

Le tout sans qu’un gros panneau mange l’écran.
