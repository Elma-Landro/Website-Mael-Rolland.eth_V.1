# Argos V0.1 — Dossier d'intervention Hermès : Next Actions

**Date** : 23 juin 2026
**Branche** : `codex/create-expand-from-node-planning-documents`
**Graphe audité** : `grc20-these-mael-rolland-v96.json` (non modifié)
**Script Argos** : `scripts/audit_graph.py` — commits `6e4f8c4` (V0) + `e91f82e` (V0.1)
**Mode** : Audit en lecture seule — aucune correction appliquée

---

## 1. Résumé exécutif

Argos V0.1 détecte **16 relations cassées** (endpoint `from` manquant), **37 pseudo-orphelins** (connectés uniquement via `appears in section`), **23 relation types définis mais jamais utilisés**, **26 relation types utilisés ≤ 2 fois**, et **341 entités sans description**. Le graphe est techniquement connexe (0 orphelin strict) mais la centralité est artificiellement garantie par 12 425 relations `appears in section` (61,9 % du total).

**Découverte majeure** : l'analyse approfondie des 16 relations cassées révèle que **15 d'entre elles proviennent d'un bug de troncature d'UUID** — le champ `from` a été écrit avec seulement 16 des 32 caractères hex de l'UUID réel. Pour chacune de ces 15, une **relation valide identique existe déjà** dans le graphe (même type, même `to`, `from` complet). Ce sont donc des **doublons orphelins** supprimables sans perte. La 16ᵉ relation (`contributes to` → Ostrom 1990) est un orphelin véritable nécessitant une revue humaine.

**Problèmes certains** : 15 relations tronquées supprimables, `relatedTo` référencé dans `story-presets.mjs` mais inexistant dans le schéma, `space.id` placeholder.

**Problèmes nécessitant validation humaine** : la relation `contributes to` → Ostrom 1990, les 4 potentiels doublons d'entités, la décision sur les 23 relation types inutilisés.

**Ordre recommandé** : (1) supprimer les 15 relations tronquées → (2) créer le script d'audit stories → (3) corriger `relatedTo` + résoudre focus nodes → (4) doctrine ontologique Ariane → (5) export public allégé.

---

## 2. Validation Argos V0.1

| Vérification | Résultat |
|---|---|
| Hash commit Argos V0.1 | `e91f82e` |
| Commande exécutée | `python3 scripts/audit_graph.py` |
| Relations cassées détectées | **16** ✓ |
| `broken_relations_details` dans le JSON | **16 entrées** ✓ |
| Toutes classées `missing_from` | ✓ |
| Tous les `to` existent | ✓ |
| Exit code | **1** (problèmes critiques) ✓ |

---

## 3. Analyse des 16 relations cassées

### 3.1 Découverte principale : bug de troncature d'UUID

Tous les IDs d'entités valides font **32 caractères hex**. Les 16 `from` cassés font **16 caractères hex**. Pour 15 d'entre eux, ce préfixe de 16 caractères correspond **exactement** au début d'un UUID complet d'une entité réelle existante. Pour chacune de ces 15, une **relation valide identique** (même `type`, même `to`, `from` complet à 32 chars) existe déjà dans le graphe.

**Cause probable** : bug de double insertion lors d'une passe de migration — la même relation écrite deux fois, dont une copie au `from` tronqué à 16 caractères.

### 3.2 Tableau détaillé

| Index | Relation ID | Type | From manquant (16 chars) | Entité réelle correspondante (32 chars) | To valide | Action | Classification |
|---|---|---|---|---|---|---|---|
| 19455 | `d65f6831…` | appears in section | `0170870141524d46` | Black Hat (Concept) | III.2 Des marques… | Supprimer (doublon valide existant) | **DELETE_CANDIDATE_CERTAIN** |
| 19456 | `0c0b8086…` | appears in section | `c0c1bec510f54099` | White Hat (Concept) | III.2 Des marques… | Supprimer (doublon valide) | **DELETE_CANDIDATE_CERTAIN** |
| 19457 | `bd4b971b…` | appears in section | `f87e9246cf2b407b` | Consensus distribué (Concept) | Chapitre I | Supprimer (doublon valide) | **DELETE_CANDIDATE_CERTAIN** |
| 19458 | `…` | appears in section | `f07878254e144095` | Logique de sceau (Concept) | Chapitre I | Supprimer (doublon valide) | **DELETE_CANDIDATE_CERTAIN** |
| 19459 | `…` | appears in section | `f07878254e144095` | Logique de sceau (Concept) | II.2 « Pourtant… » | Supprimer (doublon valide) | **DELETE_CANDIDATE_CERTAIN** |
| 19460 | `…` | appears in section | `71908f95dad74d9a` | Logique de signature (Concept) | Chapitre I | Supprimer (doublon valide) | **DELETE_CANDIDATE_CERTAIN** |
| 19461 | `…` | appears in section | `71908f95dad74d9a` | Logique de signature (Concept) | II.2 « Pourtant… » | Supprimer (doublon valide) | **DELETE_CANDIDATE_CERTAIN** |
| 19462 | `…` | appears in section | `2af42270c40746e2` | OP_RETURN (TechnicalConcept) | Chapitre I | Supprimer (doublon valide) | **DELETE_CANDIDATE_CERTAIN** |
| 19463 | `…` | contributes to | `72d182705407492c` | **AUCUNE** correspondance trouvée | Ostrom 1990 | **Revue humaine** | **HUMAN_REVIEW_REQUIRED** |
| 19464 | `…` | appears in section | `571934eb6d074fb8` | Auryn Macmillan (Person) | III.2 Des marques… | Supprimer (doublon valide) | **DELETE_CANDIDATE_CERTAIN** |
| 19465 | `…` | appears in section | `633ccadaea354e76` | Bill Shihara (Person) | Chapitre I | Supprimer (doublon valide) | **DELETE_CANDIDATE_CERTAIN** |
| 19466 | `…` | appears in section | `20b8c4f053744b01` | Tristan D'Agosta (Person) | Chapitre I | Supprimer (doublon valide) | **DELETE_CANDIDATE_CERTAIN** |
| 19467 | `…` | cited in | `53525938440543a5` | Jérôme Favier (Reference) | Introduction générale | Supprimer (doublon valide) | **DELETE_CANDIDATE_CERTAIN** |
| 19468 | `…` | cited in | `53525938440543a5` | Jérôme Favier (Reference) | Chapitre II | Supprimer (doublon valide) | **DELETE_CANDIDATE_CERTAIN** |
| 19469 | `…` | cited in | `fb692ce5f716443f` | Primavera De Filippi (Reference) | Section B | Supprimer (doublon valide) | **DELETE_CANDIDATE_CERTAIN** |
| 19470 | `2b000439…` | cited in | `a985149b43e34a43` | The Filter / Griff Green 2016 (Reference) | III.2 Des marques… | Supprimer (doublon valide) | **DELETE_CANDIDATE_CERTAIN** |

### 3.3 Le cas spécial : `contributes to` → Ostrom 1990

L'ID `72d182705407492c` ne correspond au préfixe d'**aucune** entité existante. Il ne s'agit pas d'une troncature mais d'un véritable orphelin. La cible « Ostrom 1990 » possède déjà deux relations `contributes to` valides (Social Ecological System, Common Pool Resources). Le lien cassé suggère un troisième contributeur disparu — probablement un concept d'analyse institutionnelle (polycentricity, action arena, IAD framework) supprimé ou régénéré lors d'une migration.

**Hypothèses** : (a) un concept lié au cadre IAD d'Ostrom qui aurait été fusionné avec un autre ; (b) un ID régénéré. Sans journal de suppression (`ops` ne contient que des `SET_ATTRIBUTE`), impossible de déterminer l'entité originelle.

**Recommandation** : ne pas supprimer aveuglément. Demander à Maël s'il reconnaît un concept qui aurait dû être lié à Ostrom 1990. Si aucune réponse, supprimer la relation cassée lors du même patch.

### 3.4 Notes sur `ops`

Les 293 entrées `ops` sont **toutes de type `SET_ATTRIBUTE`**. Aucune suppression (`DELETE_ENTITY`, `DELETE_RELATION`) n'est journalisée. Aucun des 13 IDs fantômes n'apparaît dans `ops`. La section `ops` n'est donc pas un journal d'audit complet des changements.

---

## 4. Proposition de patch Héphaïstos pour les 16 relations cassées

### Patch futur recommandé : `patch_remove_broken_relations_v97.json`

| Champ | Détail |
|---|---|
| **Nom** | `patch_remove_broken_relations_v97.json` |
| **Objectif** | Supprimer les 15 relations tronquées (doublons orphelins) + décision sur la 16ᵉ |
| **Fichier à modifier** | `grc20-these-mael-rolland-v97.json` (création d'une nouvelle version) |
| **Méthode** | Supprimer les 15 relations par leur index dans `relations[]` (index 19455–19470 sauf 19463). Pour la relation 19463 (`contributes to` → Ostrom 1990) : soit supprimer après validation humaine, soit laisser en l'état avec un flag `[UNVERIFIED]` |
| **Critères d'acceptation** | (1) `python3 scripts/audit_graph.py` → exit 0 (ou 1 si la 16ᵉ est conservée) ; (2) `broken_from` = 0 (ou 1) ; (3) aucune entité n'a perdu de relation sémantique (les doublons valides sont conservés) ; (4) le nombre total de relations passe de 20 057 à 20 042 (ou 20 041) |
| **Rollback** | Le fichier v96 reste intact. Pour annuler : `git checkout grc20-these-mael-rolland-v96.json` |
| **Vérification Argos** | `python3 scripts/audit_graph.py --input grc20-these-mael-rolland-v97.json` → exit 0 |

**Ne crée pas ce fichier maintenant.**

---

## 5. Analyse des 37 pseudo-orphelins

Les pseudo-orphelins sont connectés au graphe **uniquement** via `appears in section` — ils n'ont aucune relation sémantique (conceptuelle, argumentative, citationnelle). Ils sont « dans le graphe » mais sans valeur analytique relationnelle.

### Classification

| Classification | Nombre | Description |
|---|---:|---|
| `LOW_VALUE_INDEX_ONLY` | 16 | Concepts/Personnes sans description, indexés dans une section mais sans valeur relationnelle |
| `REFERENCE_ONLY` | 10 | Références bibliographiques légitimes mais non reliées sémantiquement |
| `NEEDS_SEMANTIC_RELATION` | 7 | Entités substantielles qui mériteraient des relations sémantiques |
| `POTENTIAL_DUPLICATE` | 4 | Probables doublons avec des entités existantes |

### Tableau détaillé (sélection)

| Entité | Type | Classification | Risque | Action recommandée |
|---|---|---|---|---|
| BIP-91 — Compromise SegWit activation | ProtocolProposal | NEEDS_SEMANTIC_RELATION | Concept structurant non relié | Devrait avoir `alternative proposal` / `fork of` vers Bitcoin |
| BitLaundry | ActorNonHuman | NEEDS_SEMANTIC_RELATION | Service de mixage mentionné dans la thèse | Devrait avoir `part of` / `operates in segment` |
| Controverse Taproot activation (2021) | GovernanceConflict | NEEDS_SEMANTIC_RELATION | Conflit de gouvernance non relié | Devrait avoir `debated in` / `governance` |
| Logique de sceau | Concept | POTENTIAL_DUPLICATE | Peut être un doublon avec un concept combiné | Examiner si fusion avec « Logique de signature » |
| Logique de signature | Concept | POTENTIAL_DUPLICATE | Idem | Examiner si fusion |
| Consensus distribué | Concept | POTENTIAL_DUPLICATE | Doublon possible avec « Logique de consensus distribué » | Examiner |
| White Hat | Concept | POTENTIAL_DUPLICATE | Doublon possible avec « Whitehat DAO » | Examiner |
| SEC 2017 — The DAO Report | Reference | REFERENCE_ONLY | Référence légitime mais isolée | Lier via `cited in` si pertinent |
| Tristan D'Agosta | Person | LOW_VALUE_INDEX_ONLY | Sans description | Enrichir ou marquer `[UNVERIFIED]` |
| *(+ 28 autres)* | | | | |

**Ne propose aucune relation sans preuve.** L'objectif est de préparer le travail futur d'Argos/Thot/Mnémosyne, pas d'enrichir automatiquement.

### 4 potentiels doublons à examiner en priorité

1. **« Logique de sceau » vs « Logique de signature »** — deux concepts adjacents qui pourraient être fusionnés ou distingués plus explicitement.
2. **« Consensus distribué » vs « Logique de consensus distribué »** — l'un semble être la version courte de l'autre.
3. **« White Hat » vs « Whitehat DAO »** — confusion possible entre le concept éthique et l'événement.
4. **Auryn Macmillan** apparaît comme pseudo-orphelin mais son ID tronqué est aussi dans les relations cassées — suggérant une double trace.

---

## 6. Analyse des 23 relation types inutilisés

| Relation type (ID résolu) | Classification | Commentaire |
|---|---|---|
| **`governs`** | **POTENTIALLY_IMPORTANT_UNUSED** | 🔴 Signal fort : une thèse sur la gouvernance polycentrique n'utilise jamais la relation « governs ». Pourrait coder la distinction gouvernance par/sur l'infrastructure. |
| **`aliasOf`** | **POTENTIALLY_IMPORTANT_UNUSED** | 🔴 La déduplication n'est pas résolue — coïncide avec les 4 potentiels doublons détectés. Activer `aliasOf` permettrait de les traiter sans fusion destructive. |
| **`revealedBy`** | **NEEDS_ONTOLOGY_DECISION** | Conceptuellement pertinent pour les crises (révélées par les événements), mais non implémenté. |
| **`splits_community`** | **NEEDS_ONTOLOGY_DECISION** | Pertinent pour The DAO (sécession Ethereum Classic). |
| **`phaseOfCrisis`** | **NEEDS_ONTOLOGY_DECISION** | Pertinent pour la périodisation des crises (CrisisPhase existe déjà comme type). |
| `phaseOfDevelopment` | NEEDS_ONTOLOGY_DECISION | Pertinent pour DevelopmentPhase (3 entités existantes). |
| `produces decision` | NEEDS_ONTOLOGY_DECISION | Pertinent pour GovernanceProcess. |
| `derivedFromConcept` | NEEDS_ONTOLOGY_DECISION | Pertinent pour la hiérarchie conceptuelle. |
| `partOfMonetizationProcess` | NEEDS_ONTOLOGY_DECISION | Pertinent pour la chaîne de monétisation. |
| `instantiatedInProtocol` | NEEDS_ONTOLOGY_DECISION | Pertinent pour Capability/Protocol. |
| `enablesCapability` | NEEDS_ONTOLOGY_DECISION | Pertinent pour Capability/Protocol. |
| `implementsProtocol` | KEEP_AS_RESERVED | Réserve technique. |
| `operatesOnProtocol` | KEEP_AS_RESERVED | Réserve technique. |
| `clientFor` | KEEP_AS_RESERVED | Réserve technique. |
| `repositoryFor` | KEEP_AS_RESERVED | Réserve technique. |
| `serviceFor` | KEEP_AS_RESERVED | Réserve technique. |
| `belongsToCategory` | KEEP_AS_RESERVED | Redondant avec `belongs to category` (qui existe et est utilisé). |
| `mediatesAccessTo` | KEEP_AS_RESERVED | Réserve conceptuelle. |
| `participatesInArena` | KEEP_AS_RESERVED | Redondant avec `participates in` (qui existe). |
| `participates_in` | REMOVE_CANDIDATE | Redondant — `participates in` (avec espaces) existe et est utilisé (29 occurrences). |
| `circulates as` | KEEP_AS_RESERVED | Réserve conceptuelle. |
| `sloganOf` | KEEP_AS_RESERVED | Réserve pour les labels indigènes. |
| `occurs during` | REMOVE_CANDIDATE | Aucune description, aucune utilisation. |

**Recommandation** : ne pas supprimer automatiquement. Les deux REMOVE_CANDIDATE (`participates_in`, `occurs during`) peuvent être retirés lors d'un patch ontologique. Les POTENTIALLY_IMPORTANT_UNUSED (`governs`, `aliasOf`) méritent une décision de conception avant activation.

---

## 7. Analyse des 26 relation types utilisés ≤ 2 fois

| Relation type | Occ. | Classification | Action recommandée |
|---|---:|---|---|
| `develops` | 2 | **À fusionner** | → `develops concept` (19 occ.) — chevauchement réel |
| `increases demand` | 1 | **À fusionner** | → `increases` (2 occ.) ou `drives demand` (9 occ.) |
| `triggers escalation of` | 1 | **À fusionner** | → `triggers` (23 occ.) |
| `increases transaction volume` | 2 | **Redondante** | Chevauchement avec `increases` |
| `implements` | 1 | **Redondante** | Chevauchement avec `implementsProtocol` (inutilisé) — choisir |
| `mediates` | 1 | **Redondante** | Chevauchement avec `mediatesAccessTo` (inutilisé) |
| `founded by` | 2 | **Légitime mais rare** | Peu d'organisations fondées dans le corpus |
| `central thesis` | 2 | **Légitime mais rare** | Relation structurelle pour le nœud thèse |
| `rapporteur of` | 2 | **Légitime mais rare** | Métadonnée de soutenance |
| `jury member of` | 2 | **Légitime mais rare** | Métadonnée de soutenance |
| `thesis committee` | 2 | **Légitime mais rare** | Métadonnée de soutenance |
| `directed by` | 1 | **Légitime mais rare** | Métadonnée de direction de thèse |
| `member of lab` | 1 | **Légitime mais rare** | Affiliation institutionnelle |
| `introduces concept` | 2 | **Légitime mais rare** | Chevauchement possible avec `develops concept` |
| `accelerates` | 2 | **Légitime mais rare** | Relation causale économique |
| `monetary object` | 2 | **À documenter** | Type hybride entity/relation — clarifier |
| `losing proposal` | 2 | **Légitime mais rare** | BIP/EIP rejetés |
| `losing proposal` | — | *(déjà listé)* | |
| `used in` | 1 | **Légitime mais rare** | Mention d'usage |
| `encourages` | 1 | **À documenter** | Relation causale faible |
| `evidences` | 1 | **À documenter** | Chevauchement avec `evidenced by` (63 occ.) |
| `manifests` | 1 | **À documenter** | Relation d'expression |
| `spreads` | 1 | **À documenter** | Relation de diffusion |
| `extends` | 1 | **À documenter** | Relation d'extension |
| `modification resolves crisis (BIP)` | 1 | **Légitime mais rare** | Relation spécifique aux crises BIP |
| `increases` | 2 | **Légitime mais rare** | Relation causale |

**Recommandation** : 3 fusions certaines (`develops`, `increases demand`, `triggers escalation of`). Le reste demande une décision ontologique (Ariane).

---

## 8. Surpoids `appears in section`

### Pourquoi ce n'est pas un bug technique

Les 12 425 relations `appears in section` sont structurellement valides : leurs endpoints existent, elles ne sont pas dupliquées, elles servent à indexer les entités dans les sections de la thèse. Le graphe les a ajoutées intentionnellement (v72 a introduit la couche `ThesisSection`).

### Pourquoi c'est une dette de lisibilité

- **62 % des arêtes** sont des arêtes d'indexation, pas des arêtes sémantiques.
- Dans une vue force-directed, ces arêtes créent un « effet nuage » qui masque les relations argumentatives.
- Les nœuds les plus centraux (ThesisSection, degré 384–611) sont des conteneurs d'indexation, pas des objets analytiques.
- Le sizing proportionnel au degré écrase les concepts sous les sections.

### Pourquoi il ne faut pas supprimer ces relations

Elles servent à la navigation chapternaire, au filtrage par section, et aux ancres narratives. Les supprimer casserait le story mode et la matrice chapter × type.

### Pistes Dédale

1. **Toggle « masquer relations d'indexation »** dans l'UI — filtre sur `appears in section` + `cited in`.
2. **Centralité analytique** — Argos pourrait calculer un degré hors `appears in section` pour révéler la véritable hiérarchie analytique.
3. **Export public allégé** — créer `public-data/grc20-public-vN.json` sans les 990 entités bibliographiques inactives (Reference/AcademicWork/GreyLiterature sans description) et sans `appears in section`.

---

## 9. Audit story minimal

### 9.1 `relatedTo` — bug certain confirmé

`relatedTo` apparaît dans les `allowedRelationTypes` de **3 stories** :
- `monetisation-cryptos` (ligne 25)
- `structure-these` → étapes s6, s7, s8, s9 (lignes 366, 377, 389, 401)
- `fil-de-preuves` (ligne 425)

**Le type `relatedTo` n'existe pas** dans les 130 `relation_types` du graphe v96. C'est une **référence morte** : le filtre story ne peut jamais matcher ce type. Les arêtes `relatedTo` sont silencieusement ignorées.

De plus, les stories utilisent un mélange de conventions de nommage incohérentes : `hasConcept` (camelCase), `opposedTo` (camelCase), `relatedTo` (camelCase) vs `has crisis` (avec espaces), `refuted by` (avec espaces). Or le graphe utilise majoritairement la convention « avec espaces » (`appears in section`, `cited in`, `quote supports`). Les noms camelCase dans les stories doivent être normalisés via `normalizeRelationName` dans `graphe.helpers.js`.

### 9.2 Résolution des focus nodes

Le mécanisme `resolveStoryFocusNodes` dans `graphe.story-helpers.js` :
1. Cherche d'abord dans `STORY_FOCUS_ALIASES` (40 entrées manuelles label→nom d'entité).
2. Puis cherche par ID exact, puis par nom exact.
3. Puis normalise (NFD, lowercase) et cherche par nom normalisé.
4. Si non trouvé → `console.warn('[story-mode] focusNode introuvable')` et le nœud est **silencieusement ignoré**.

### 9.3 `STORY_FOCUS_ALIASES` — 40 alias manuels fragiles

Le fichier contient 40 correspondances label→entityname codées à la main. Fragilités :
- Certains alias pointent vers des noms d'entités avec accents/diacritiques qui peuvent diverger.
- Ex : `'Nominalisme non étatiste'` → `'Nominalisme monetaire non etatiste'` (les accents ont été retirés dans la cible mais pas dans la clé).
- Aucun test automatisé ne vérifie que les cibles des alias existent réellement.

### 9.4 Focus nodes non résolus — analyse croisée

En confrontant les ~80 focusNodes/centralNodes déclarés dans les 5 stories avec les 2 263 entités du graphe :

**Risques certains identifiés** :
- `relatedTo` : référence morte (bug certain).
- Plusieurs focusNodes ne matchent aucune entité et ne sont pas dans `STORY_FOCUS_ALIASES`.
- La convention de nommage des `allowedRelationTypes` mélange camelCase et espaces — le filtre peut perdre des arêtes.

### 9.5 Risques et vérifications à automatiser

| Risque | Niveau | Vérification à automatiser |
|---|---|---|
| `relatedTo` inexistant | **Bug certain** | Script vérifie que tout `allowedRelationType` existe dans `relation_types` |
| Focus nodes non résolus | **Bug certain** | Script vérifie que tout `focusNode`/`centralNode`/`bridgeEntityId` résout vers une entité |
| Alias cassés | **Hypothèse probable** | Script vérifie que toute cible d'alias existe |
| Convention nommage | **Dette** | Script vérifie la cohérence camelCase vs espaces |

### 9.6 Design du futur script `scripts/audit_stories.py`

```
scripts/audit_stories.py
  --input grc20-these-mael-rolland-v96.json
  --stories story-presets.mjs
  --helpers graphe.story-helpers.js

Vérifications :
1. Parser story-presets.mjs (regex ou AST léger)
2. Extraire tous les focusNodes, centralNode, bridgeEntityIds
3. Extraire tous les allowedRelationTypes et hideRelationTypes
4. Pour chaque focusNode :
   - Vérifier résolution par nom exact
   - Vérifier résolution par alias (parser STORY_FOCUS_ALIASES)
   - Vérifier résolution par normalisation NFD
   - Signaler les non-résolus
5. Pour chaque allowedRelationType :
   - Vérifier existence dans relation_types du graphe
   - Vérifier cohérence de nommage (camelCase vs espaces)
6. Rapport Markdown + JSON + exit code
```

---

## 10. Séquence des 5 prochains patchs

| Ordre | Nom | Objectif | Fichiers | Risque | Validation | Agent |
|---|---|---|---|---|---|---|
| **1** | Suppression 15 relations tronquées | 0 relation cassée (ou 1 si Ostrom conservé) | `grc20-these-mael-rolland-v97.json` | Faible | `python3 scripts/audit_graph.py` → exit 0 ou 1 | Héphaïstos |
| **2** | Script `audit_stories.py` | Détecter focus nodes non résolus + `relatedTo` mort | `scripts/audit_stories.py` (nouveau) | Nul (script seul) | `python3 scripts/audit_stories.py` → exit 1 si bugs | Argos/Calliope |
| **3** | Correction stories | Supprimer `relatedTo`, normaliser `allowedRelationTypes`, résoudre focus nodes | `story-presets.mjs`, `graphe.story-helpers.js` | Faible | `audit_stories.py` → exit 0 | Calliope |
| **4** | Doctrine ontologique | Documenter les 6 types conceptuels, décider des 23 types inutilisés, harmoniser nommage | `docs/grc20_ontology_doctrine.md` (nouveau) | Nul (doc seule) | Revue humaine | Ariane |
| **5** | Export public allégé | Graphe sans bibliographie inactive ni `appears in section` | `public-data/grc20-public-vN.json` | Moyen | Test de rendu navigateur | Dédale/Héphaïstos |

**Principe directeur** : Argos détecte → rapport → patch réversible → validation humaine → correction → Argos confirme.

---

## 11. Prompt prêt pour le prochain agent GLM 5.2

```
CONTEXTE
Tu travailles sur le graphe GRC-20 de la thèse de Maël Rolland.
Dépôt : /workspace/Website-Mael-Rolland.eth_V.1
Branche par défaut : codex/create-expand-from-node-planning-documents
Graphe canonique : grc20-these-mael-rolland-v96.json (2 263 entités, 20 057 relations)

OBJECTIF
Supprimer les 15 relations cassées identifiées comme DELETE_CANDIDATE_CERTAIN
par l'audit Argos V0.1. Ces 15 relations sont des doublons orphelins issus
d'un bug de troncature d'UUID : le champ `from` contient seulement 16 des 32
caractères hex de l'UUID réel. Pour chacune, une relation valide identique
(même type, même `to`, `from` complet) existe déjà dans le graphe.

La 16ᵉ relation (index 19463, `contributes to` → Ostrom 1990, from `72d182705407492c`)
est un orphelin véritable sans doublon. NE LA SUPPRIME PAS dans ce patch.
Laisse-la en l'état — elle sera traitée séparément après revue humaine.

FICHIERS À LIRE
- grc20-these-mael-rolland-v96.json (graphe source, NE PAS MODIFIER)
- scripts/audit_graph.py (script d'audit, pour validation)

FICHIER À CRÉER
- grc20-these-mael-rolland-v97.json (copie de v96 avec les 15 relations
  supprimées)

MÉTHODE
1. Charger v96 en mémoire.
2. Identifier les 15 relations à supprimer : ce sont les relations dont
   le champ `from` fait exactement 16 caractères hex ET dont il existe
   déjà une relation avec le même `type` et le même `to` mais un `from`
   de 32 caractères qui commence par ces 16 caractères.
3. Supprimer exactement ces 15 relations du tableau `relations[]`.
4. NE PAS supprimer la relation index 19463 (from `72d182705407492c`).
5. Sauvegarder en v97.

CONTRAINTES
- Ne modifie aucune entité.
- Ne modifie aucun type ni relation_type.
- Ne modifie pas le v96.
- Ne modifie pas d'autres fichiers du dépôt.
- Python 3 stdlib uniquement pour le script de transformation.
- Conserve le formatage JSON (indentation, ensure_ascii=False).

INTERDITS
- Ne supprime PAS la relation `contributes to` vers Ostrom 1990.
- Ne corrige PAS les focus nodes ou les stories.
- Ne modifie PAS le schéma.
- Ne commit PAS sans autorisation.

VALIDATION
Après création du v97 :
1. python3 scripts/audit_graph.py --input grc20-these-mael-rolland-v97.json
   → doit détecter exactement 1 relation cassée (l'Ostrom),
   exit code 1.
2. Vérifier que le nombre de relations = 20 057 - 15 = 20 042.
3. Vérifier que le nombre d'entités = 2 263 (inchangé).

FORMAT DE RÉPONSE
- Confirmer la création du fichier v97.
- Donner la sortie d'Argos sur v97.
- Confirmer : 20 042 relations, 2 263 entités, 1 relation cassée.
- Donner git diff --stat.
- Ne pas committer.
```

---

*Fin du rapport. Ne pas committer ce fichier sans autorisation explicite.*
