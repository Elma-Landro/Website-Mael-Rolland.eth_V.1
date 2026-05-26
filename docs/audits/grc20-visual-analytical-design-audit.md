# Audit visuel analytique GRC-20 — Batch 001

## 1. Scope

- **Objet** : consolider les constats visuels/analytiques existants sur la visualisation GRC-20, sans patch runtime.
- **Sources lues** : `docs/grc20_views_audit.md`, `docs/grc20_relations_audit.md`, `docs/grc20_ontology_audit.md`, `docs/architecture/GRAPH_MODULARIZATION_AUDIT.md`, documents `docs/architecture/*STORY*`, `grc20-these-mael-rolland-v96.json`.
- **Limite** : pas de test navigateur/mobile exécuté dans cette mission ; les constats runtime restent à valider dans une PR dédiée.

## 2. Mesures structurelles utiles au diagnostic visuel

- Entités : 2263 ; relations : 20057.
- Relations cassées structurellement invisibles/non résolubles : 16.
- `Reference` : 760 entités ; relations incidentes à des références : 8509 (42.42 % des relations).
- `SourceQuote` : 245 entités ; relations incidentes à des SourceQuotes : 1556 (7.76 % des relations).
- Types relationnels dominants : `appears in section` 12425, `cited in` 2694, `quote supports` 392, `part of` 374, `source of` 366, `belongs to domain` 342.

### Hubs principaux par degré relationnel

| Degré | Entité | Type | in | out | Lecture visuelle |
|---:|---|---|---:|---:|---|
| 611 | `0fcc7028560c47cc9b82309f469b700c` — A. La gouvernance des cryptomonnaies : construction de notre objet de recherche | ThesisSection | 606 | 5 | hub structurel susceptible d’écraser les nœuds analytiques voisins |
| 602 | `21ff5747290e4951a3b0b601ddbbe9d6` — B. La gouvernance des CM dévoilée par leurs crises : un institutionnalisme articulé à une sociologie des sciences et techniques | ThesisSection | 598 | 4 | hub structurel susceptible d’écraser les nœuds analytiques voisins |
| 594 | `a2c452a77b394a9d836eed0e16ed5851` — Chapitre I - L'émergence du phénomène des cryptomonnaies (CM) : Bitcoin et Ethereum comme infrastructures sociotechniques | Chapter | 561 | 33 | hub structurel susceptible d’écraser les nœuds analytiques voisins |
| 563 | `018c87f7337246b99ab36add53a537e3` — C. Une démarche ethnographique, pour un terrain d'enquête multi-niveau | ThesisSection | 560 | 3 | hub structurel susceptible d’écraser les nœuds analytiques voisins |
| 492 | `0b521ac19a2f5ee0cdd07d7460ebdfd0` — II.2.3 — La monnaie à l'épreuve : dettes, confiance et souveraineté | ThesisSection | 490 | 2 | hub structurel susceptible d’écraser les nœuds analytiques voisins |
| 484 | `9c72c7227c3e0cee55b8b4820e7492d8` — Conclusion — Résumé de la thèse | ThesisSection | 483 | 1 | hub structurel susceptible d’écraser les nœuds analytiques voisins |
| 473 | `df405dcd975b406486a260da72f1ad4a` — Introduction générale | Chapter | 464 | 9 | hub structurel susceptible d’écraser les nœuds analytiques voisins |
| 449 | `711fe2aa7c734731bccb42ccd5843924` — A. Décrypter la crypto par l’approche infrastructurelle | ThesisSection | 448 | 1 | hub structurel susceptible d’écraser les nœuds analytiques voisins |
| 440 | `b5386fe92a5b4cac94888ffc298469bf` — B. Les CM, comme “en plus” dans la théorie monétaire et l’analyse des systèmes monétaires | ThesisSection | 439 | 1 | hub structurel susceptible d’écraser les nœuds analytiques voisins |
| 435 | `a078b1b274f74818a8c7f1abcfb3097f` — Au-dela des codes | DoctoralThesis | 157 | 278 | hub structurel susceptible d’écraser les nœuds analytiques voisins |
| 435 | `93f13f18c6da412292eba80dcd630ac7` — I.2.1 Un protocole deborde de carnavalesques improvisations d acteurs | ThesisSection | 400 | 35 | hub structurel susceptible d’écraser les nœuds analytiques voisins |
| 427 | `5b5935bc3ede49028b7dfbdaa4f34b6d` — Chapitre II - Dépasser la controverse du statut monétaire des CM par un institutionnalisme intéressé aux usages | Chapter | 414 | 13 | hub structurel susceptible d’écraser les nœuds analytiques voisins |

## 3. Arêtes invisibles ou faiblement lisibles

- **Cassure référentielle sûre** : 16 relations ne peuvent pas être dessinées correctement si le renderer exige deux endpoints existants. Elles deviennent invisibles, filtrées ou sources d’anomalies selon le runtime.
- **Invisibilité intentionnelle** : Story mode utilise `edgeMode: strict`, `hideBackbone`, `hideRelationTypes` et des plafonds `max*Edges`. Ce n’est pas un bug en soi ; c’est une stratégie de lisibilité qui doit être explicitement documentée pour éviter l’impression de relations absentes.
- **Risque analytique** : si les arêtes cachées ne sont pas signalées, l’utilisateur peut confondre absence visuelle et absence de preuve.
- **Patch sûr futur** : ajouter un compteur “relations masquées / relations affichées” dans les états Focus/Story, sans changer les données.

## 4. Hiérarchie visuelle des hubs

- Les plus hauts degrés sont majoritairement des `Chapter` ou `ThesisSection`. C’est structurellement cohérent, mais visuellement dangereux : ces hubs attirent les layouts et peuvent transformer une lecture argumentative en simple sommaire radial.
- La thèse visuelle doit distinguer trois niveaux : ossature textuelle, concepts/cas analytiques, preuve bibliographique. Si les sections et références ont le même poids que les concepts, le graphe devient un index plutôt qu’un instrument d’analyse.
- **Hypothèse de design** : utiliser des zones/bandes pour chapitres/sections et réserver la centralité visuelle aux concepts, crises, processus et acteurs dans les vues analytiques.

## 5. Poids excessif des références et SourceQuotes

- Les `Reference` représentent la classe la plus nombreuse et touchent plus de 40 % des relations. Leur affichage indifférencié peut dominer les vues.
- Les `SourceQuote` sont indispensables comme preuve, mais ne devraient pas être des nœuds macro permanents : elles fonctionnent mieux comme cartes de preuve, hover/click ou couche à la demande.
- **Patch sûr futur** : layer “preuve” désactivé par défaut dans les vues macro, avec accès explicite depuis le panneau détail.
- **Validation scientifique nécessaire** : toute réduction de visibilité des sources doit préserver la traçabilité et ne jamais affaiblir le lien citation → claim.

## 6. Mobile

- Les audits existants recommandent déjà le renforcement du contraste, la taille adaptative et la rotation des labels de colonnes.
- Risque principal : sur mobile, la densité des labels et des hubs de section transforme la matrice en texture, pas en lecture.
- **Patch runtime à tester** : seuils de labels par zoom/densité, labels prioritaires, légende compacte, et test sur Structure / Monétisation / Qui gouverne réellement.

## 7. Mode Éclater / hairball

- Le mode Éclater est utile pour l’exploration locale, mais devient un hairball dès qu’il expose trop de nœuds secondaires non labellisés.
- Les constats existants recommandent de plafonner explicitement les nœuds non labellisés par sous-cluster.
- **Patch sûr sous condition UX** : plafonnement + indicateur “+N nœuds masqués”, avec recherche/focus permettant de récupérer ce qui est caché.

## 8. Distinguer patchs sûrs et hypothèses de design

| Catégorie | Élément | Statut |
|---|---|---|
| Patch sûr | Corriger les 15 endpoints tronqués | mécanique, hors runtime |
| Patch sûr | Compteur de relations masquées/affichées | runtime léger à tester |
| Patch sûr | Plafond en mode Éclater avec indicateur `+N` | runtime à tester |
| Hypothèse de design | Transformer chapitres/sections en bandes plutôt qu’en hubs de même poids | nécessite prototype |
| Hypothèse de design | Passer SourceQuotes en couche preuve à la demande | nécessite test de traçabilité |
| Validation scientifique | Décider du sort de `Common Pool Resources (CPR)` / `72d…` | hors design, décision d’ontologie |
