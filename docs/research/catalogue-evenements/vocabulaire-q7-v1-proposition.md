# Vocabulaire Q7 v1 — effets sur propriétés monétaires — PROPOSITION DE GEL

**Statut : PROPOSITION, gel réservé à Maël.** Issue des arbitrages A1-A5 du 15/08/2026 (verbatim : `docs/audits/arbitrages-lot2-A1-A5-2026-08-15.md`) et de la mini-passe révisée sur les 14 lignes du lot d'épreuve, qui **passent toutes** (`q7-epreuve-lot-v2.csv` ; premier passage figé : `q7-epreuve-lot.csv`). Une fois gelé, ce vocabulaire devient v1 : aucun renommage silencieux, tout changement produit une v2 ou une table de correspondance versionnée (règle de la page d'architecture §7.3, par extension).

Remplace comme spécification le champ 14 `[PROVISOIRE, Q7]` de `docs/audits/grille-codage-catalogue-v1.md`, qu'il complète sans le réécrire.

## 1. Les neuf dimensions

| dimension | définition |
|---|---|
| `usage_paiement` | extension ou contraction de l'usage de l'UCN comme moyen de paiement |
| `valorisation` | usage financier, valeur d'échange — jamais « réserve de valeur » comme fonction stricto sensu |
| `unite_compte_etalon` | statut d'unité de compte, d'étalon ou de pivot |
| `liquidite_convertibilite` | capacité d'échange, conversion, profondeur des marchés, passerelles |
| `conf_methodique` | fiabilité des procédures, preuves, méthodes de coordination, validation technique, capacité à établir ce qui s'est passé ou ce qui doit être appliqué (A5) |
| `conf_hierarchique` | confiance dans les instances, autorités et hiérarchies reconnues |
| `conf_ethique` | conflits de valeurs, justice, légitimité, responsabilité, restitution, acceptabilité normative — « que fallait-il faire ? » (A5) |
| `fongibilite` | équivalence et interchangeabilité des unités |
| **`integrite_monnayage`** | **(nouvelle, A3, définition v0 verbatim)** l'événement affecte ou met en cause l'émission, la création, la destruction, la falsification, la conservation ou l'intégrité quantitative de l'unité monétaire. Ne se rabat jamais automatiquement sur `conf_methodique` : dimension monétaire substantielle |

## 2. Écriture et directions

`dimension(signe)` — signe **obligatoire** : `+`, `-` (trait d'union ASCII) ou `±` seulement si l'effet est énoncé comme ambivalent. Codage **uniquement sur effet énoncé** par une source (texte de la thèse, figure, description sourcée du graphe) ; sinon `nd`. Règle inchangée depuis Q7 : on ne code que l'énoncé.

## 3. Multi-effets (A4, ratifiée)

Liste séparée par espaces : `conf_methodique(-) valorisation(-)`. Contrôlée : pas de prose libre ; dimensions issues du §1 exclusivement ; signe obligatoire sur chaque effet ; plusieurs effets **seulement** si l'événement produit réellement plusieurs effets analytiques (un événement peut renforcer une dimension tout en fragilisant une autre).

## 4. Frontière `conf_ethique` / `conf_methodique` (A5)

`conf_ethique` = valeurs, justice, légitimité, responsabilité, restitution, acceptabilité normative. `conf_methodique` = fiabilité des procédures, preuves, coordination, validation technique. Un même cas peut légitimement porter les deux — ne jamais choisir une seule dimension par principe. Défaut pour le fork The DAO (cas-test de frontière) : débat immutabilité / restitution / légitimité du fork → `conf_ethique` ; procédure, coordination, activation, validation technique → `conf_methodique`. Application F069 : `conf_ethique(±)` (restitution imposée ET sécession ETC) + `conf_methodique(+)` (signalement majoritaire, Carbon Vote, activation « comme programmé »).

## 5. Acteur principal — règle affinée (A2) et forme (A1)

Règle (remplace la formulation D7 initiale, qu'elle affine sans la contredire) :

1. acte ponctuel avec initiateur clair → acteur principal = **initiateur** ;
2. crise agrégée → acteur principal = **entité affectée / système en crise** ;
3. incident ponctuel subi, sans initiateur pertinent → acteur principal = **entité affectée** (jamais d'initiateur artificiel — cas E029) ;
4. doute → `a_arbitrer`.

Forme (option (c) retenue — colonnes dédiées, jamais un nom libre seul) :

- `acteur_principal_mode` — vocabulaire fermé : `initiateur` · `entite_affectee` · `systeme_protocole` (quand l'entité affectée est le protocole/système lui-même) · `a_arbitrer` (· `nd` pour `nature=seuil`, convention r1 ci-dessous) ;
- `acteur_principal_id` — id d'entité du graphe quand elle existe ;
- `acteur_principal_nom` — nom en précision ou à défaut d'entité.

Entités de référence résolues au graphe (v115, recherche name + nameEn + labelEn + labelFr + aliases) : protocole Bitcoin `d35d720e1fa2` · Core Developers (Bitcoin) `7b29b0d2d840` · Core Developers (Ethereum) `c5f0d6a94454` · Mt. Gox `6661cad88f91` *(fiche typée InfrastructureEvent — à examiner hors lot)* · Slock.it `ae97de14e40e` · Tether Limited `a3d5db5e8de7` · Sunny King `e4eba4cea732` · The DAO (SmartContract) `ed7b68eeb311`. Sans entité : nom seul (attaquant anonyme de The DAO, auteurs du papier d'alerte).

**Implémentation au maître = future v3-3, hors lot 2** (pas de codage massif) : ici, la forme est testée dans le seul fichier d'épreuve. La typologie v1 des 7 acteurs demeure la clé de la table de rôles ; ces colonnes ne la remplacent pas.

## 6. Résultats de la mini-passe (14/14 passent)

- **A3 testée sur les trois lignes prescrites** : E015 `nd → integrite_monnayage(-)` (émission surnuméraire énoncée, codée sans forçage) ; E077 `+ integrite_monnayage(±)` (mise en cause non activée — cf. r2) ; G069 `conf_methodique(+) → integrite_monnayage(+)` (le calendrier d'émission relève de la dimension propre, pas d'un rabattement).
- **A2** : E029 sort d'`a_arbitrer` → `entite_affectee` (MtGox). Plus aucun `a_arbitrer` dans le lot.
- **A1** : les 3 lignes `systeme_protocole` (E015, E077, G005) sont désormais exprimables ; 11 lignes portent un id graphe, 2 un nom seul, 1 seuil sans acteur.
- **A5** : F069 porte les deux dimensions sans écrasement.
- **A4** : 4 lignes multi-effets, toutes contrôlées (vocabulaire fermé, signes obligatoires).
- Les 6 `nd` d'effet restants (E055, E063, E064, G005, G143 — et rôles seuls) sont des `nd` d'énoncé, pas des trous de vocabulaire.

## 7. Conventions résiduelles — à fixer d'un mot au moment du gel (non bloquantes)

- **r1** — `acteur_principal_mode` pour `nature=seuil` : proposition — `nd` admis (cohérent avec la grille v1, Q3 : un seuil peut n'avoir ni acteur ni type d'acte).
- **r2** — direction d'une **mise en cause non activée** (vulnérabilité au monnayage jamais exploitée, cas E077) : proposition — `±` avec note obligatoire ; alternative : `-` sur la mise en cause, la préservation relevant de la résolution.

Remarque hors lot (graphe, aucun patch ici) : la fiche « Mt. Gox » `6661cad8` est typée InfrastructureEvent alors qu'elle nomme une organisation — à examiner un jour via le classifieur sémantique.

## 8. Ce que le gel engagerait

Geler ce document comme **Q7 v1** fige : les neuf dimensions du §1, l'écriture du §2, la convention multi-effets du §3, la frontière du §4, la règle et la forme acteur principal du §5, plus r1 et r2 tels que tranchés. La grille de rôles v0 (`grille-roles-v0.md`) est déjà déclarée **gelable** par l'arbitrage du 15/08 ; son passage formel à « gelée » se fait d'un mot, séparément. Après gel : re-codage des 40 `propose(lot1)` sous la règle du §5 (lot dédié), puis extension progressive — jamais de codage massif sans lot arbitré.

## Provenance

Arbitrages A1-A5 de Maël Rolland, 15/08/2026 (verbatim archivé). Épreuve : `q7-epreuve-lot.csv` (premier passage, figé) → arbitrages → `q7-epreuve-lot-v2.csv` (mini-passe révisée). Grille d'acteurs v1 : `docs/audits/grille-codage-catalogue-v1.md`. Grille de rôles : `grille-roles-v0.md`. Rapport du lot : `docs/audits/etat-lot2-2026-08-15.md`.
