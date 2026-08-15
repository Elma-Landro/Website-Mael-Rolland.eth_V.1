# Arbitrages de Maël Rolland — réponses au rapport du lot 2 (A1-A5) — 15/08/2026

Verbatim du message reçu en session Cowork le 15/08/2026, en réponse à `docs/audits/etat-lot2-2026-08-15.md`. **Fait autorité** — même statut que le BLOC C de `docs/audits/PROMPT-COWORK-lot2-statut-roles-q7.md`. Traduction opérationnelle : `docs/research/catalogue-evenements/vocabulaire-q7-v1-proposition.md` et `q7-epreuve-lot-v2.csv`.

---

Réponses Maël — Lot 2 / passe d’épreuve Q7

Merci, lot 2 validé comme chantier d’épreuve. Je retiens la recommandation principale : la grille de rôles v0 est gelable en l’état, mais le vocabulaire Q7 ne doit pas encore être gelé.

Arbitrages :

A1 — Acteur principal quand D7 désigne l’entité affectée

Je retiens l’option (c) : colonne dédiée.

Ne pas utiliser un simple nom libre, trop fragile.
Ne pas utiliser seulement `systeme_protocole`, trop abstrait et trop pauvre.

Ajouter une colonne dédiée permettant de coder l’entité principale affectée / gouvernée / mise en crise, idéalement sous forme stable :
- `acteur_principal_id` si une entité du graphe existe ;
- `acteur_principal_nom` si nécessaire ;
- `acteur_principal_mode` ou équivalent pour distinguer `initiateur`, `entite_affectee`, `systeme_protocole`, `a_arbitrer`.

Règle :
pour une crise agrégée, l’acteur principal est l’entité affectée / système mis en crise ; les attaquants, découvreurs, correcteurs, validateurs restent dans la grille de rôles.

A2 — Incident subi sans initiateur

Oui, étendre la règle “entité affectée” aux incidents ponctuels lorsqu’il n’y a pas d’initiateur pertinent.

Règle affinée :
- acte ponctuel avec initiateur clair : acteur principal = initiateur ;
- crise agrégée : acteur principal = entité affectée / système en crise ;
- incident ponctuel subi, sans initiateur pertinent : acteur principal = entité affectée ;
- doute : `acteur_principal = a_arbitrer`.

Donc le flash crash MtGox ne doit pas forcer un initiateur artificiel.

A3 — Dimension Q7 manquante sur émission / intégrité du monnayage

Créer une nouvelle dimension Q7 : `integrite_monnayage`.

Ne pas rabattre automatiquement le monnayage sur `conf_methodique`.

Motif :
l’émission monétaire, l’intégrité du monnayage, la quantité de monnaie créée, détruite ou falsifiée ne sont pas seulement des questions de méthode ou de confiance procédurale. C’est une dimension monétaire substantielle, centrale pour mon travail.

Définition v0 :
`integrite_monnayage` = l’événement affecte ou met en cause l’émission, la création, la destruction, la falsification, la conservation ou l’intégrité quantitative de l’unité monétaire.

À tester sur E015, E077, G069 avant gel.

A4 — Convention multi-effets

Oui, je ratifie la convention multi-effets `dim1(+) dim2(-)`.

Mais elle doit rester contrôlée :
- pas de prose libre ;
- dimensions issues du vocabulaire Q7 ;
- signe obligatoire `+`, `-` ou éventuellement `±` si l’effet est ambivalent ;
- plusieurs effets autorisés si l’événement produit réellement plusieurs effets analytiques.

Cette convention est nécessaire : un événement peut renforcer une dimension tout en fragilisant une autre.

A5 — Frontière `conf_ethique` / `conf_methodique`

Oui, documenter explicitement la frontière avant gel.

Règle de départ :
- `conf_ethique` : conflits de valeurs, justice, légitimité, responsabilité, restitution, acceptabilité normative, “que fallait-il faire ?”
- `conf_methodique` : fiabilité des procédures, preuves, méthodes de coordination, validation technique, capacité à établir ce qui s’est passé ou ce qui doit être appliqué.

Pour le fork DAO :
ne pas choisir une seule dimension par principe. Le cas peut légitimement porter plusieurs effets.
Par défaut :
- débat immutabilité / restitution / légitimité du fork = `conf_ethique` ;
- incertitude sur la procédure, la coordination, l’activation ou la validation technique = `conf_methodique`.

Donc DAO sert de cas-test de frontière, pas de prétexte à écraser les deux dimensions.

Décision générale

- Grille de rôles v0 : gelable.
- Vocabulaire Q7 : non gelé.
- Ajouter `integrite_monnayage`.
- Documenter la règle acteur principal affinée.
- Documenter la frontière `conf_ethique` / `conf_methodique`.
- Lancer une mini-passe Q7 révisée sur les 14 lignes, pas un codage massif.
- Si les 14 lignes passent avec ces corrections, proposer ensuite un vocabulaire Q7 v1 gelable.
