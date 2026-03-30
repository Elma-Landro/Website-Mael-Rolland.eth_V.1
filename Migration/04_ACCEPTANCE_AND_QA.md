# Acceptance Criteria and QA Checklist

## 1. Critères d’acceptation

Le story mode est considéré comme correctement implémenté si les conditions suivantes sont remplies.

### 1.1 Ouverture et navigation

- un récit peut être lancé depuis la vue concernée ;
- le panneau narratif s’ouvre correctement ;
- l’utilisateur peut passer à l’étape suivante ;
- l’utilisateur peut revenir à l’étape précédente ;
- l’utilisateur peut quitter le récit.

### 1.2 Contenu affiché

Le panneau doit afficher au minimum :

- le titre du récit ;
- le numéro ou compteur d’étape ;
- le titre de l’étape ;
- le texte de l’étape.

### 1.3 Focus visuel

À chaque étape :

- la caméra se recentre clairement ;
- les nœuds ciblés sont mis en avant ;
- le reste du graphe est atténué de manière lisible ;
- le focus change réellement d’une étape à l’autre lorsque le contenu le justifie.

### 1.4 Robustesse

- aucun crash si un nœud ciblé est absent ;
- aucun crash si une relation ciblée est absente ;
- un warning console est émis en cas d’échec de résolution ;
- l’étape reste lisible même sans focus exact.

### 1.5 Non-régression

L’implémentation ne doit pas casser :

- le chargement du graphe ;
- la sélection libre de nœuds ;
- les outils de focus existants ;
- les autres vues principales ;
- les états d’interface hors story mode.

### 1.6 Maintenabilité

- les récits sont centralisés ;
- l’ajout d’un nouveau récit ne demande pas de toucher plusieurs blocs dispersés ;
- le code reste lisible et modulaire.

## 2. Checklist de test manuel

### Test 1 — Chargement général

- ouvrir la page du graphe ;
- vérifier que le graphe se charge normalement ;
- vérifier que l’interface reste réactive.

### Test 2 — Récit Monétisation

- basculer sur la vue Monétisation ;
- lancer le récit ;
- parcourir toutes les étapes ;
- vérifier qu’aucune étape n’est vide ;
- vérifier que quitter remet l’interface dans un état propre.

### Test 3 — Récit Qui gouverne réellement ?

- basculer sur la vue correspondante ;
- lancer le récit ;
- vérifier que le focus change réellement ;
- tester précédent / suivant plusieurs fois ;
- vérifier l’absence d’état bloqué.

### Test 4 — Récit Crises

- basculer sur la vue Crises ;
- lancer le récit ;
- vérifier que la distinction CVE 2018 / The DAO apparaît clairement ;
- vérifier que le passage à la synthèse fonctionne.

### Test 5 — Récit Structure de la thèse

- basculer sur la vue correspondante ;
- lancer le récit ;
- vérifier la cohérence avec la logique globale de la thèse ;
- vérifier que la conclusion du récit fonctionne.

### Test 6 — Cas de fallback

- modifier temporairement un focusNode pour le rendre faux ;
- lancer le récit ;
- vérifier qu’il n’y a pas de crash ;
- vérifier qu’un warning console est présent.

### Test 7 — Compatibilité d’état

- lancer un récit ;
- quitter ;
- utiliser Focus ;
- utiliser Strates V2 ;
- revenir à une vue libre ;
- vérifier qu’aucun état narratif résiduel ne subsiste.

## 3. Rapport final attendu de l’agent

Le rapport final doit mentionner :

- les fichiers modifiés ;
- les choix techniques structurants ;
- les points de fragilité éventuels ;
- les nœuds non trouvés si certains focus ont dû être adaptés ;
- les tests manuels réalisés.
