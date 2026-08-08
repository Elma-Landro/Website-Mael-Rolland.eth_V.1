# Section `page_start` Repair Lab v1 — 16 pages fausses, une cause unique, un patch candidat non appliqué

**Date** : 2026-08-07
**Graphe** : `grc20-these-mael-rolland-v110.json` (**inchangé** par ce chantier — aucun octet écrit dans aucun graphe)
**Branche** : `claude/file-upload-branch-check-jw4cng`
**Mode agent** : A — diagnostic + patch candidat, **aucune application**
**Outil** : `scripts/audit_section_page_start.py` (lecture seule ; n'écrit que son CSV, et seulement avec `--csv`)
**Données** : `docs/audits/data/section-page-start-diagnostic-v110.csv` (90 lignes, 13 colonnes)
**Livrables** : ce rapport + `patch_candidate_section_page_start_v1.json` (16 ops, **non appliqué**)
**Prédécesseur** : `docs/audits/grc20-sourcequote-migration-verification-v1.md`, § arbitrage **Q8**

---

## 1. Le mandat

Q8, rendu par Maël le 2026-08-07, conditionne tout le dégel de la migration
SourceQuote :

> **Q8 — (a).** Réparer les `page_start` incohérents **d'abord**, dans un
> chantier distinct et mesurable, puis seulement graver les SourceQuote :
> « je ne veux pas installer des citations p. 191 dans une section que le
> graphe dit commencer p. 202 ».

Q1 en dépend explicitement (« les rattachements ne seront pas gravés tant que
les `page_start` incohérents ne sont pas réparés »). Le présent chantier est ce
chantier distinct. Il **mesure** et **prépare**, il n'engrave rien : la
réparation elle-même reste suspendue à l'arbitrage de l'auteur, parce qu'elle
touche 16 nœuds du graphe.

Ce que ce chantier devait produire : l'ampleur exacte de l'écart, sa cause, un
patch candidat conforme au contrat, et une réponse honnête à la question « une
fois réparé, le dégel est-il possible ? ».

---

## 2. Méthode et calibration

### 2.1 La règle de preuve

Une seule source remplit la colonne `page_imprimee_verifiee` : **un titre
imprimé dans le corps de la thèse**, en égalité exacte de forme réduite entre
une fenêtre de 1 à 4 lignes consécutives d'une page et une dénomination du
nœud (`name`, `labelFr`, `title`, chacune aussi privée de son préfixe de
numérotation). C'est une égalité, pas une approximation.

**Aucune page n'est déduite d'un offset de fichier PDF.** Les PDF du dépôt sont
découpés par bloc ; l'offset d'une page dans son fichier n'a aucun rapport avec
sa pagination dans la thèse. Le script lit le numéro **imprimé** au pied de
chaque page — la marque `— NN — ` — et ne travaille qu'en pages imprimées.

### 2.2 Calibration constatée (re-mesurée à la rédaction de ce rapport)

| Fichier | Pages imprimées |
|---|---|
| `1_Premières_pages.pdf` | 1-5 |
| `2_Tables_des_matieres.pdf` | 6-12 — **exclu** de la recherche de titres |
| `3_Precautions_ecriture.pdf` | 13-14 |
| `4_Introduction_generale.pdf` | 15-51 |
| `5_Chapitre_1.pdf` | 52-141 |
| `6_Chapitre_2.pdf` | 142-219 |
| `7_Chapitre_3.pdf` | 220-331 |
| `8_Conclusion_Generale.pdf` | 332-340 |

**Suite imprimée 1-340 : continue, sans trou** — dans le **périmètre indexé**,
qui est le corps de la thèse. La pagination imprimée continue au-delà (la
bibliographie va jusqu'à 382, les annexes suivent) : ces blocs sont
délibérément hors index, et la revue hostile a vérifié qu'aucun des 16 titres
n'y apparaît (0 occurrence sur les 72 pages d'annexes et sur la
bibliographie), donc le test d'unicité n'est pas contourné. Une seule page du
périmètre est écartée faute de numéro imprimé exploitable : l'offset 0 de
`1_Premières_pages.pdf`, c'est-à-dire la couverture — signalée, jamais devinée.

**Corroboration indépendante par la table des matières imprimée : accord
80 / désaccord 0 / non déclaré 0**, sur les 80 titres localisés. La TDM ne
remplit jamais la colonne de preuve — elle porte ses propres erreurs, la thèse
y numérotant deux fois « I.2.1 » et écrivant « II.2.3 » pour III.2.3 — mais un
accord de 80 sur 80 avec une source qui se trompe ailleurs est un contrôle
sérieux.

### 2.3 Les trois pièges méthodologiques, et comment chacun a été écarté

**Piège 1 — page imprimée ≠ offset PDF.** Écarté par la calibration ci-dessus :
la lecture se fait sur le pied de page imprimé, page par page, et la continuité
1-340 sans trou prouve que la lecture n'a pas dérivé. Aucune page de ce dossier
n'a été obtenue en ajoutant un décalage à un numéro d'offset.

**Piège 2 — une section parente commence légitimement avant ses enfants.**
`II.3` p. 185 et `II.3.1` p. 186 n'est pas une incohérence. Le script ne compare
donc **jamais** un `page_start` à celui d'une autre section : il le compare à la
page où le titre de *cette* section est imprimé, et à rien d'autre. Les colonnes
`parent` / `page_start_parent` sont là pour la lecture humaine, pas pour le
verdict. Contrôle : le diagnostic porte **5 notes « parente légitimement
antérieure »** (I.1.1, II.2.2, II.3.1, III.1.1, III.1.2) et **0 note « parente
POSTÉRIEURE à son premier enfant »** — le cas réellement suspect ne se présente
nulle part. Vérifié par comptage sur le CSV : `0` occurrence de `POSTERIEURE`.

**Piège 3 — la pagination n'est jamais dictée par ce qui arrangerait les
SourceQuote.** Le dossier `sourcequote-migration-verification-v1.csv` n'est lu
que pour remplir la colonne `concernee_sourcequote` (oui/non). Il n'intervient
dans **aucune** décision de page, ne pondère aucun candidat, et n'est même pas
chargé en mode `--check`. **Le dossier SourceQuote n'a orienté aucune page de ce
rapport.** Et le résultat le montre : sur les 5 nœuds `incohérent` visés par le
lot, aucune correction ne va dans le sens qui « arrangerait » les 41 ops —
II.3.2 recule de 12 pages, III.1.2.b de 22, tandis que II.3.1.a avance d'une.
Si le texte imprimé contrarie le lot, c'est le texte qui a raison.

### 2.4 Ce qui n'est jamais promu en preuve

Trois sources sont lues, rapportées dans `note` sous le marqueur explicite
`PISTE`, et n'entrent dans aucun verdict : la table des matières imprimée, le
quasi-titre (difflib ≥ 0.82) et le préfixe commun (≥ 16 caractères réduits). Une
reformulation plausible n'est pas une preuve — c'est la leçon « Florence Dufy »
du dépôt, où le rapprochement vraisemblable de deux noms avait failli graver une
personne qui n'existe pas.

---

## 3. Le diagnostic chiffré

**90 nœuds** de section audités dans v110 ; **37** portent un `page_start`.

| Statut | Nombre | Ce que ça veut dire |
|---|---:|---|
| `correct` | 20 | `page_start` présent, égal à la page imprimée |
| **`incoherent`** | **16** | `page_start` présent, **différent** de la page imprimée |
| `absent` | 48 | aucun `page_start` — une donnée, pas un vide |
| `ambigu` | 1 | `page_start` présent, page imprimée non établie |
| `hors-perimetre` | 5 | nœuds de type `Chapter` (page de garde ≠ première page de contenu) ; aucun ne porte de `page_start` |

20 + 16 + 1 = 37 : le compte des porteurs se referme.

### Les 16 incohérences

| Clé v110 | Déclaré | Imprimé | Écart | Preuve | Visé SourceQuote |
|---|---:|---:|---:|---|:--:|
| I.1.1.a | 58 | **59** | −1 | `5_Chapitre_1.pdf` p.59 | non |
| I.1.1.b | 68 | **65** | +3 | `5_Chapitre_1.pdf` p.65 | non |
| I.1.2 | 78 | **68** | +10 | `5_Chapitre_1.pdf` p.68 | non |
| I.2.2.b | 100 | **106** | −6 | `5_Chapitre_1.pdf` p.106 | **oui** |
| II.1.1.b | 154 | **151** | +3 | `6_Chapitre_2.pdf` p.151 | non |
| II.2.2.a | 161 | **167** | −6 | `6_Chapitre_2.pdf` p.167 | non |
| II.2.2.b | 165 | **168** | −3 | `6_Chapitre_2.pdf` p.168 | non |
| II.2.2.c | 173 | **170** | +3 | `6_Chapitre_2.pdf` p.170 | non |
| II.3.1.a | 186 | **187** | −1 | `6_Chapitre_2.pdf` p.187 | **oui** |
| II.3.1.b | 190 | **188** | +2 | `6_Chapitre_2.pdf` p.188 | **oui** |
| II.3.2 | 202 | **190** | +12 | `6_Chapitre_2.pdf` p.190 | **oui** |
| III.1.1.a | 225 | **227** | −2 | `7_Chapitre_3.pdf` p.227 | non |
| III.1.1.b | 241 | **235** | +6 | `7_Chapitre_3.pdf` p.235 | non |
| III.1.2.a | 255 | **242** | +13 | `7_Chapitre_3.pdf` p.242 | non |
| III.1.2.b | 265 | **243** | +22 | `7_Chapitre_3.pdf` p.243 | **oui** |
| III.2.1 | 277 | **255** | +22 | `7_Chapitre_3.pdf` p.255 | non |

Écarts de −6 à +22 pages, dans les deux sens, sans régularité arithmétique.
C'est déjà un fait : **ce n'est pas un décalage de pagination**. Un décalage
aurait un signe et un pas.

---

## 4. La cause : unique, et prouvée

### 4.1 Ce que la comparaison des snapshots établit

Le dépôt conserve v96 à v110. Trois mesures, faites indépendamment du CSV :

1. **Aucun `page_start` n'a jamais été modifié.** Sur les 2 262 entités communes
   à v96 et v110, **23** portent un `page_start` dans l'un ou l'autre : les 23
   valeurs sont **identiques** dans les deux. **0 modification, 0 apparition,
   0 disparition.** v110 en compte 37 : les 14 de plus sont portés par des nœuds
   qui **n'existaient pas en v96**.
2. **Les 16 valeurs fausses sont les pages imprimées des clés d'avant la
   migration.** Pour chacun des 16 nœuds, sa clé v96 a été relue dans
   `grc20-these-mael-rolland-v96.json`, et la valeur déclarée comparée à la page
   imprimée du nœud qui porte **aujourd'hui** cette clé : **16 égalités exactes
   sur 16**.
3. **Les 14 nœuds créés après v96 et porteurs d'un `page_start` sont tous
   `correct`** (I.1.1, I.1.3, I.2.1, II.1.1, II.1.2, II.2.1, II.2.2, II.2.3,
   II.3.1, II.3.3, III.1.1, III.1.2, III.2.2, III.2.3). Ce sont exactement les
   clés que les 16 nœuds ont libérées.

Autrement dit : **la valeur a suivi le NŒUD ; la renumérotation v100/v106 a
changé la SECTION que la clé désigne ; personne n'a jamais déplacé une page.**
Les nœuds créés à la migration ont reçu la bonne page ; les nœuds renumérotés
ont gardé l'ancienne.

Contrôle de complétude : **18** nœuds de section communs à v96 et v110 ont changé
de `section_key`. 16 sont les incohérents. Le 17ᵉ (`f07c8415`, ex-`II.1.1`,
aujourd'hui `II.1.1.a`) est `correct` — mais **par coïncidence** : II.1.1 et
II.1.1.a commencent tous deux p. 148. Le 18ᵉ (`93f13f18`, ex-`I.2.1`,
aujourd'hui `I.2.2`) ne porte aucun `page_start` : rien à comparer. **Aucun nœud
renuméroté n'échappe à l'explication.**

### 4.2 Les deux cas emblématiques

**`7b3312fe` — « Quand les CM réactivent un débat monétaire ancien… »**
Portait la clé `II.3.3` en v96, avec `page_start` 202. `II.3.3` est bien imprimé
p. 202 (`6_Chapitre_2.pdf`) — c'était juste. La migration v106 a renuméroté ce
nœud en `II.3.2`, et créé un **nouveau** nœud pour `II.3.3` (avec, lui, p. 202).
Le titre de `7b3312fe` est imprimé p. **190**. Sa valeur 202 n'est donc pas une
erreur de pagination : c'est la page, exacte, d'une section qu'il ne désigne
plus. Écart apparent : +12.

**`5a82e90b` — « Enjeux des crises Bitcoin : labélisations indigènes… »**
Portait `III.2.2` en v96, `page_start` 265. `III.2.2` est imprimé p. 265 —
juste. Renuméroté en `III.1.2.b` ; son titre est imprimé p. **243**. Écart
apparent : +22. C'est le cas que la PR #115 avait signalé, et l'un des deux qui
ont gelé la migration SourceQuote.

### 4.3 Ce que la cause exclut

- **Ce n'est pas v108/v109.** Ces deux versions ont réaligné des `section_key`
  **portées par des relations** `appears in section` et le câblage des charges
  d'ancrage ; l'attribut `page_start` **des nœuds** n'y a pas bougé d'une unité
  (mesure 1 ci-dessus).
- **Ce n'est pas une pagination diffuse.** Les 20 `correct` et les 14 nœuds
  créés après v96 sont indemnes ; seuls les nœuds renumérotés sont touchés.
- **Ce n'est pas une erreur d'extraction PDF.** La suite imprimée est continue,
  et la TDM corrobore 80/80.

---

## 5. Le patch candidat

`patch_candidate_section_page_start_v1.json` — **16 ops, 0 appliquée.**

### 5.1 Ce qu'il contient

- Enveloppe `_meta` + `ops`, dialecte `patch_18`/`patch_19` (celui que
  `make_v110` consomme et que le graphe journalise nativement) :
  `type: "SET_ATTRIBUTE"`, `entityId`, `attributeId: "page_start"`,
  `value: {type: "NUMBER", value: <entier>}`.
- `_meta.policy` commence par la chaîne exacte
  `CANDIDATE — NOT APPLIED — AUTHOR ARBITRATION REQUIRED`.
- `op_count: 16`, `entities_touched: 16`, `skipped_count: 49` — tous
  recomptables mécaniquement, et recomptés par
  `scripts/preflight_candidate_patches.py` (C05).
- Un `_comment` par op citant **la clé v96 d'origine** et **la preuve** (fichier
  PDF + page imprimée + accord TDM).
- `_meta.value_type_note` : la forme `{type: "NUMBER", value: <int>}` n'est pas
  un choix mais un constat — les 16 valeurs actuelles ont été inspectées une par
  une dans v110, toutes `{type: NUMBER, value: int}` depuis que `patch_19` a
  retypé les `"58"` textuels en `58`. **Le patch ne change que le nombre, jamais
  le type.**
- `_meta.registry_note` : `page_start` existe déjà au registre
  (id `9a51004e4755b22b82877f5d55d59a7c`, `valueType` NUMBER, `domain`
  `[ThesisSection]`, `count` 37). Les 16 cibles sont toutes `ThesisSection` et
  **seulement** `ThesisSection` (vérifié) : ni extension de registre, ni
  extension de domaine, ni changement de `count` — 16 valeurs modifiées, 0
  posée, 0 supprimée.

### 5.2 Ce qu'il ne contient pas

Aucun autre attribut. Aucun `SET_NAME`, aucun `SET_TYPES`, aucun
`CREATE_ENTITY`, aucun `DELETE_ATTRIBUTE`. Aucune relation posée ni retirée,
aucune fusion, aucune `section_key` touchée, aucune `SourceQuote`. **Aucun des
48 nœuds `absent` n'est rempli** : réparer une valeur fausse et créer une valeur
absente sont deux actes différents, et le second est un arbitrage (§ 7d).

Les 49 entrées `skipped` motivent une par une les 48 `absent` et le seul
`ambigu` — chacune avec son id, sa clé, sa page imprimée quand elle est établie,
et la raison précise de son exclusion. 16 + 49 + 20 `correct` (rien à corriger)
+ 5 `hors-perimetre` (aucun `page_start`) = 90 : le compte se referme.

### 5.3 Le cas I.2.2.b — inclus, et pourquoi

Le nœud `97eb6267` (I.2.2.b) partage son titre réduit avec `3ce505bc`, un nœud
**hors de l'arbre** `section of` / `has section`, nommé « I.2.1b Un protocole
Bitcoin qui s'adapte… ». Le CSV avertit qu'« une réparation mécanique leur
donnerait la même page ». L'op est retenue quand même, pour trois raisons
vérifiables :

1. elle ne touche **que** `97eb6267`. `3ce505bc` ne porte aucun `page_start` et
   n'est dans aucune op de ce patch : **aucune page partagée n'est créée** ;
2. p. 106 est la page imprimée de **ce titre**, quel que soit le nœud que
   l'auteur tiendra pour canonique. La valeur n'anticipe aucune fusion et n'en
   empêche aucune ;
3. laisser 100 serait laisser une valeur **démontrée fausse** sur l'un des 5
   nœuds `incohérent` que le lot SourceQuote vise — c'est-à-dire ne pas lever le
   gel pour un cinquième des cas qui le motivent.

Le doublon `97eb6267` / `3ce505bc` reste ouvert : § 7(b).

### 5.4 Ce que son application exigerait

Le patch **ne s'applique pas lui-même** et n'est accompagné d'aucun applicateur.
Le graver demanderait, dans cet ordre :

1. un **script dédié `scripts/make_v111_*.py`**, sur le modèle de
   `make_v110_apply_bib_and_attribute_patches.py` : lit v110, mute, écrit v111,
   supporte `--dry-run`, et porte **ses propres contrôles d'après** (les 16
   entités existent ; elles portent bien un `page_start` avant ; le nombre total
   de `page_start` reste 37 ; aucun autre attribut ne bouge ; aucune relation
   n'est touchée) ;
2. `space.version` aligné sur le nom de fichier (`check_graph_integrity.py`
   bloque sinon) et `space.note` borné ;
3. **la régénération du registre dans le MÊME commit** :
   `python3 scripts/build_properties_registry.py` — ici sans changement attendu
   (`page_start` reste NUMBER, domaine `[ThesisSection]`, count 37), mais l'état
   intermédiaire est CI-rouge par construction, donc graphe et registre voyagent
   ensemble ;
4. **le contrôle d'après spécifique de ce chantier** :
   `python3 scripts/audit_section_page_start.py --check`, qui doit passer de
   « 16 divergences » à **vert**. Ce mode existe déjà — il a été écrit pour que
   la réparation soit *prouvable*, pas seulement annoncée ;
5. les contrôles locaux habituels (`check_graph_integrity.py`,
   `check_anchoring.py`, `build_anchor_weights.py --check`,
   `build_properties_registry.py --check`, `preflight_candidate_patches.py`) ;
6. la mise à jour de **tous** les pointeurs vers le nom du graphe —
   `package.json`, `these.html`, `graphe.html`, `lecteur.html`,
   `graph-worker.mjs`, `narrative-anchors-build.mjs` — que la CI ne vérifie pas ;
7. une **revue hostile** (`grc20-reviewer-hostile`) avant PR.

État du preflight aujourd'hui : `python3 scripts/preflight_candidate_patches.py`
→ **15 OK / 0 AVERTISSEMENT / 0 BLOQUANT** sur ce patch, exit 0 ; le lot complet
(4 candidats) sort à 57 OK / 4 AVERTISSEMENT / 0 BLOQUANT.

---

## 6. Effet attendu sur le dégel des 41 SourceQuote

Les 41 ops des zips `Migration/` désignent leurs cibles par un champ
`target_section` qui mélange trois écritures (clé simple, `avant->apres`,
`cible1 | cible2`). Après éclatement : **49 jetons distincts**, qui résolvent
vers **40 nœuds** du graphe.

| État des 40 nœuds visés | Nombre | Ce que la réparation change |
|---|---:|---|
| `incoherent` | **5** | **réparés** par ce patch : I.2.2.b (100→106), II.3.1.a (186→187), II.3.1.b (190→188), II.3.2 (202→190), III.1.2.b (265→243) |
| `correct` | 5 | rien à faire : I.2.1 (89), II.3.1 (186), III.2.2 (265), III.3.3 (314), `conclu_resume` (332) |
| `absent` | **30** | **inchangés** — ce patch ne remplit aucun `page_start` absent |

**Ce que la réparation lève.** Exactement l'obstacle nommé par Q8 : « installer
des citations p. 191 dans une section que le graphe dit commencer p. 202 ». Les
5 nœuds incohérents visés sont précisément ceux qui produisaient ce
contresens — dont II.3.2 (202→190) et III.1.2.b (265→243), les deux cas qui ont
motivé le gel. Après application, **aucune des 41 citations ne serait attachée à
une section dont le `page_start` contredit le texte imprimé** — à une condition
que la revue hostile a mise au jour et qu'il faut énoncer : cette conclusion
**suppose l'arbitrage Q1 (a)**. Sans lui, P1-14 (citation p. 186) resterait
rattachée à `II.3.1.a`, dont la page corrigée devient **187** : la réparation
créerait elle-même une citation antérieure au début déclaré de sa section. Q1
recentre précisément cette op sur `II.3.1` (p. 186, `correct`), ce qui lève le
cas — mais le recentrage vit dans les `notes` du dossier SourceQuote, pas dans
la colonne `target_section`. Un applicateur qui ne lirait que la colonne
reproduirait le contresens. Noter au passage que `II.3.1.a` **recule** de 186 à
187, donc *défavorise* cette op : c'est une preuve de plus que la pagination
n'a pas été orientée pour arranger le lot. Les 5 recentrages
validés en Q1 (P1-14 → II.3.1, P1-15 → II.3.1.b, P2-4 et P2-5 → II.3.2,
P2-9 → III.3.4) portent tous sur des nœuds désormais soit corrigés, soit déjà
corrects.

**Ce que la réparation ne lève pas.** Trois choses, et il faut le dire :

1. **30 des 40 nœuds visés n'ont toujours aucun `page_start`.** Une citation
   attachée à `intro_C_2` ou à `conclu_aceph` restera rattachée à une section
   qui ne déclare aucune page de début. Ce n'est pas une *contradiction* — c'est
   un silence — mais si le critère de dégel est « la section sait où elle
   commence », il n'est rempli que pour 10 nœuds sur 40. Le remplissage des 48
   `absent` est l'arbitrage § 7(d)-(e).
2. **9 jetons du lot ne correspondent à aucun nœud du graphe** : `I.2.1c`,
   `I.2.2a`, `I.2.2b`, `I.3.2b`, `I.3.3a`, `I.3.3c`, `conclusion_crises`,
   `conclusion_infrastructure`, `conclusion_resume`. Certains sont des variantes
   orthographiques d'un jeton qui, lui, résout (`I.2.2b` sans point à côté de
   `I.2.2.b`, `conclusion_resume` à côté de `conclu_resume`) ; d'autres visent
   des sous-sections de niveau 3 que Q2 a décidé de **rabattre sur leurs
   parentes**. Aucune réparation de page ne les fait exister. C'est un travail
   de résolution de cibles, distinct de celui-ci.
3. **Les autres blocages de la migration restent entiers** : 18 des 41 ops
   coupent du texte sans le marquer (Q7 exige la restauration des `[…]`), 7 sont
   mal rattachées, 6 dupliquent une `SourceQuote` existante. Ce chantier ne
   touche à rien de tout cela.

En un mot : la réparation lève **le** blocage nommé par Q8, pas **les** blocages
de la migration.

---

## 7. Les cas réservés à l'arbitrage de Maël

Ces cinq questions sont posées en parallèle dans le fil de discussion. Elles
sont écrites ici **sans réponse** : aucune n'est tranchable par un agent.

**(a) `conclu_boucs` — le seul `ambigu`.** Le nœud `d9f534f9` déclare
`page_start` 338. Aucun titre imprimé ne correspond exactement à son libellé :
la thèse imprime « LES CM : BOUCS ÉMISSAIRES **COMMODES** D'UN SYSTÈME MONÉTAIRE
EN CRISE ? » (`8_Conclusion_Generale.pdf` p. 338), le graphe écrit « Les CM :
boucs émissaires d'un système monétaire en crise ? » — sans « commodes ». Les
trois pistes (quasi-titre 0.92, préfixe commun, table des matières) **convergent
toutes vers 338**, donc il n'y a probablement rien à corriger. Mais valider ce
rapprochement de titre, c'est décider que le graphe reformule le titre de la
thèse — et une reformulation plausible n'est pas une preuve. **Le rapprochement
est-il validé (et faut-il aligner le libellé du graphe sur le titre imprimé),
ou le nœud reste-t-il `ambigu` ?**

**(b) La collision de titre `I.2.2.b` / `3ce505bc`.** Deux nœuds portent le même
titre réduit — « Un protocole Bitcoin qui s'adapte : des régulations
transactionnelles très politiques » — imprimé une seule fois, p. 106. L'un
(`97eb6267`) est dans l'arbre des sections sous la clé `I.2.2.b` ; l'autre
(`3ce505bc`) est hors arbre, nommé « I.2.1b … », sans `page_start`, et **les
deux sont visés par le lot SourceQuote** (sous les jetons `I.2.2.b` et
`I.2.1b`). Ce patch corrige la page du premier et ne touche pas au second.
**Sont-ce deux nœuds pour une seule section (donc un doublon à fusionner ou à
marquer `duplicateOf`), ou deux objets distincts ? Et si l'on fusionne, lequel
est canonique ?**

**(c) `I.2.2` — deux sections numérotées « I.2.1 » dans la thèse.** Le nœud
`93f13f18` porte la clé `I.2.2`, mais son titre est **imprimé sous le numéro
« I.2.1 »** p. 100 — alors qu'une autre section est déjà imprimée « I.2.1 »
p. 89. La table des matières reproduit fidèlement les deux. Ce n'est pas une
erreur du graphe : **c'est une erreur de numérotation dans la thèse imprimée**.
Le script ne tranche pas, et ce patch ne touche aucune clé. **La clé `I.2.2`
est-elle conservée (le graphe corrige silencieusement la thèse), ou faut-il
suivre l'impression et documenter la collision ?**

**(d) Les 48 nœuds `absent` — remplir ou non ?** Aucun ne porte de
`page_start`. **39** ont une page imprimée établie par preuve exacte : les
remplir serait mécanique et sûr. **9** n'en ont pas — 6 parce que le graphe
reformule ou raccourcit le titre imprimé (`intro_A`, `intro_C_2a` à
`intro_C_2e`), 1 parce que le titre exact est imprimé sur **deux** pages
(`intro_C_2f`, « Entretiens », p. 41 et p. 46), et **2 sans aucune piste** :
`conclu_theo_mon` (« B. Les CM, comme "en plus" dans la théorie monétaire… ») et
`conclu_traduction` (« C. Le travail de traduction… »), dont le libellé n'a
aucun répondant dans le corps de la thèse. **Faut-il remplir les 39 prouvés
(chantier séparé), et que faire des 9 autres — laisser vide, ou instruire les
libellés ?**

**(e) L'extension aux `absent` créerait des pages partagées parent/enfant.** Si
les 39 prouvés étaient remplis, **4 nœuds recevraient exactement la page de leur
parente** : `intro_B_1` = `intro_B` (p. 24), `intro_B_3a` = `intro_B_3` (p. 32),
`intro_C_1` = `intro_C` (p. 34), `intro_C_1a` = `intro_C_1` (p. 34). C'est
parfaitement **légitime** — une section commence à la page de son premier
enfant, et le diagnostic porte déjà 5 notes « parente légitimement antérieure »
pour dire que ce n'est pas une anomalie. Mais cela produirait des doublons de
valeur visibles dans le graphe et dans `lecteur.html`. **Est-ce accepté tel
quel, ou faut-il une convention (par exemple : ne pas remplir un enfant dont la
page est celle de sa parente) ?**

---

## 8. Ce que ce chantier n'a pas fait

- **Aucun graphe n'a été modifié.** `grc20-these-mael-rolland-v110.json` est
  inchangé, et aucun v111 n'existe. `git diff` est vide sur tous les
  `grc20-these-*.json`.
- **Aucune carte d'ancrage n'a été touchée** : `entity_section_map.json`,
  `section_entities_map.json`, `section_overrides.json`,
  `section-headings-map.json` sont inchangés.
- **Aucun runtime n'a été touché** : `graphe.html`, `lecteur.html`,
  `graph-worker.mjs`, `sections.helpers.js` sont inchangés.
- **Aucun applicateur n'a été écrit.** Pas de `make_v111_*.py`. Le patch est un
  fichier de données ; l'application est un acte séparé, relu, arbitré.
- **Aucune `SourceQuote` n'a été créée, aucun lien de section posé, aucune
  fusion, aucun renommage, aucun retypage.**
- **Aucun `page_start` absent n'a été rempli** — les 48 `absent` restent vides,
  et la question de les remplir est posée, pas résolue (§ 7d-e).
- **Aucune `section_key` n'a été corrigée**, y compris là où la thèse imprime un
  autre numéro que la clé (I.2.2, III.2.3, `intro_B`/`C`/`D`/`E`). Le piège
  connu du dépôt reste entier : trois clés (`II.3.1`, `II.3.2`, `III.2.2`)
  existent toujours mais désignent d'autres sections depuis v106 — et ce
  chantier, en corrigeant les pages, ne corrige pas les clés.
- **Aucune décision de fusion ou d'identité** : le doublon `97eb6267` /
  `3ce505bc` est signalé, pas tranché.
- **Le CSV de diagnostic n'a pas été régénéré en place** : il a été re-produit à
  la rédaction pour vérifier qu'il est reproductible (même répartition
  20/16/48/1/5, mêmes 16 écarts, même calibration, même corroboration 80/80),
  mais le fichier commité n'a pas été réécrit.

**Écritures de ce chantier — cinq fichiers** (énoncé corrigé par la revue
hostile, qui a relevé que l'affirmation « deux fichiers, exactement » était
fausse) : `scripts/audit_section_page_start.py`,
`docs/audits/data/section-page-start-diagnostic-v110.csv`,
`patch_candidate_section_page_start_v1.json`, le présent rapport — et
**`grc20-properties-registry-v1.json`**, régénéré parce que le nouveau script
change le `readBy` de plusieurs clés d'attributs.

Sur ce dernier point, la revue a établi un fait qu'il faut consigner : le
balayage de `build_properties_registry.py` est **lexical**, et il compte comme
lecteurs des occurrences qui n'en sont pas. Le script d'audit lit réellement
quatre clés (`page_start`, `section_key`, `title`, `labelFr`) ; les trois
autres attribuées sont des **faux positifs** — `pages` vient de l'API pypdf
(`lecteur.pages`, `self.pages`), `note` et `type` des noms de colonnes du CSV.
Conséquence mesurable : la clé `pages` (domaine `Reference`, une plage de
pages **bibliographique**) a basculé `editorial` → `structural` sur la foi d'un
lecteur qui ne la lit pas. Le registre porte désormais un caveat explicite pour
`pages` et `note`, sur le modèle de celui qui existait déjà pour `type`. La CI
reste verte (le registre est régénéré dans le même commit, la discipline tient)
— mais un invariant qui déclare un lecteur fictif est un invariant un peu moins
vrai, et cela devait être écrit.
