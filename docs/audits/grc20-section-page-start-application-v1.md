# Application du patch `page_start` — v111, 16 corrections et rien d'autre

**Date** : 2026-08-08
**Graphe produit** : `grc20-these-mael-rolland-v111.json` (2 293 entités, 20 207 relations — **inchangés**)
**Graphe source** : `grc20-these-mael-rolland-v110.json`
**Branche** : `claude/file-upload-branch-check-jw4cng`
**Mode agent** : application contrôlée — première écriture de graphe de cette série
**Applicateur** : `scripts/make_v111_apply_section_page_start_patch.py` (avec `--dry-run`)
**Patch appliqué** : `patch_candidate_section_page_start_v1.json` (16 ops, 49 `skipped`)
**Prédécesseur** : `docs/audits/grc20-section-page-start-repair-lab-v1.md` (PR #116) — arbitrages **P1 (a), P2 (a), P3 (b), P4 (a), P5 (a)** rendus par Maël Rolland le 2026-08-08

---

## 1. Ce qui a été fait

Le patch candidat produit par le *page_start repair lab* a été appliqué après
l'arbitrage de l'auteur. Il contient **16 `SET_ATTRIBUTE` sur la seule clé
`page_start`**, et le graphe v111 en porte exactement 16 conséquences.

Les 16 valeurs corrigées sont les 16 nœuds que le diagnostic classait
`incoherent` : leur `page_start` était la page imprimée de la clé que ce même
nœud portait en v96, avant les renumérotations v100/v106. La valeur avait suivi
le **nœud**, la renumérotation avait changé la **section** que la clé désigne.

| Clé | Avant | Après | Écart | Entité |
|---|---:|---:|---:|---|
| I.1.1.a   |  58 |  59 |  −1 | `4ec3224a` |
| I.1.1.b   |  68 |  65 |  +3 | `43978230` |
| I.1.2     |  78 |  68 | +10 | `1168d4e0` |
| I.2.2.b   | 100 | 106 |  −6 | `97eb6267` |
| II.1.1.b  | 154 | 151 |  +3 | `eda05ae2` |
| II.2.2.a  | 161 | 167 |  −6 | `f8a8acbf` |
| II.2.2.b  | 165 | 168 |  −3 | `f34ad8e3` |
| II.2.2.c  | 173 | 170 |  +3 | `0b521ac1` |
| II.3.1.a  | 186 | 187 |  −1 | `515088f0` |
| II.3.1.b  | 190 | 188 |  +2 | `d93cb2ce` |
| II.3.2    | 202 | 190 | +12 | `7b3312fe` |
| III.1.1.a | 225 | 227 |  −2 | `ac859fd1` |
| III.1.1.b | 241 | 235 |  +6 | `0420e53c` |
| III.1.2.a | 255 | 242 | +13 | `9fbdbbc3` |
| III.1.2.b | 265 | 243 | +22 | `5a82e90b` |
| III.2.1   | 277 | 255 | +22 | `da7e8dda` |

*(« Écart » = ancienne valeur − page imprimée : ce que le graphe déclarait en
trop ou en moins.)*

## 2. Ce qui n'a **pas** été fait

- **Aucune complétion.** Les **49 `skipped`** du patch restent exactement dans
  l'état où v110 les laisse : 48 nœuds ne portent toujours **aucun**
  `page_start`, et `conclu_boucs` (`d9f534f9`, seul cas `ambigu`) garde ses 338.
  C'est l'arbitrage **P4 (a)** : « ici on répare ce qui est faux ; on ne mélange
  pas réparation et complétion ». L'applicateur ne s'en remet pas à la bonne
  volonté : une op qui viserait un nœud sans `page_start` le fait **échouer**
  (testé).
- **Aucune SourceQuote créée**, aucun lien posé ou retiré, aucune fusion, aucun
  renommage, aucun retypage, aucune clé de section touchée, aucune dette
  d'identité corrigée. Le doublon `97eb6267` / `3ce505bc` reste ouvert
  (arbitrage **P2 (a)** : la page 106 est démontrée, le doublon ne bloque pas la
  réparation d'une valeur fausse, et `3ce505bc` — qui ne porte aucun
  `page_start` — n'a pas été rempli).
- **Aucun dégel automatique des 41 ops SourceQuote.** L'arbitrage **P5 (a)**
  prévoit un dégel **op par op**, à trois conditions posées par l'auteur : (1) la
  section cible a une page vérifiée ou ne présente aucune contradiction
  détectée ; (2) les arbitrages Q1–Q8 sont inscrits ; (3) les coupes, coquilles,
  doublons et mauvais rattachements sont traités conformément aux arbitrages
  déjà rendus. « Le patch `page_start` ne dégèle pas automatiquement les 41 ops.
  Il lève seulement la contradiction structurelle qui empêchait d'avancer. »
  **Ce chantier n'a gravé aucune citation et n'en autorise aucune.**
- **`narrative-anchors.json` n'a pas été régénéré.** v109 et v110 l'avaient fait
  par habitude ; ici ce serait du bruit : `narrative-anchors-build.mjs` ne lit
  **jamais** `page_start` (vérifié — 0 occurrence dans le fichier), et le mandat
  interdit de toucher au runtime au-delà des pointeurs de version. Le fichier
  garde donc `"generated_from": "…v110.json"` : c'est exact, il *a* été généré
  depuis v110. **Mesuré plutôt que supposé** : une régénération depuis v111
  (exécutée hors dépôt, sortie en `/tmp`) donne un fichier dont **les 120 ancres
  sont identiques octet pour octet** ; seuls diffèrent `generated_from` et
  l'horodatage `generated_at`. Régénérer aurait donc produit un diff de deux
  lignes de métadonnées, dont une horloge.
- **Aucune carte d'ancrage modifiée**, aucun patch réécrit. Le patch appliqué
  garde sa `policy` `CANDIDATE — NOT APPLIED — AUTHOR ARBITRATION REQUIRED` : le
  réécrire falsifierait l'archive. Son statut réel est consigné ici.

## 3. Pourquoi aucune vérification navigateur n'était requise

**Aucun fichier runtime ne lit le `page_start` du graphe.** Vérifié
indépendamment : sur tout le dépôt (`*.html`, `*.js`, `*.mjs`, hors
`node_modules`), la chaîne `page_start` n'apparaît **qu'une fois**, à
`lecteur.html:1347` — et cette valeur-là vient de `section_entities_map.json`
(chargé ligne 1233), pas du graphe. Elle est recopiée dans l'entrée agrégée
d'une section parente et **n'est jamais affichée** : aucune autre ligne du
runtime ne la relit.

La réparation n'a donc **aucun effet visible** sur le site. Elle répare ce que
lisent les outils d'audit et ce que publiera GRC-20, pas ce que voit un lecteur.

## 4. La corroboration indépendante : la carte d'ancrage avait raison

`section_entities_map.json` porte un `page_start` sur **48 de ses 54 clés**. Sur
les **23 clés où le graphe et la carte en portaient un tous les deux**, v110
comptait **20 accords et 3 désaccords** :

| Clé | Graphe v110 | Carte | Correction v111 |
|---|---:|---:|---:|
| I.1.2   |  78 |  68 |  68 |
| II.3.2  | 202 | 190 | 190 |
| III.2.1 | 277 | 255 | 255 |

Ces 3 désaccords sont **exactement 3 des 16 corrections**, et la carte tenait à
chaque fois la valeur que le patch allait écrire. **La carte d'ancrage était
juste ; c'est le graphe qui était périmé.** Après application, l'accord est de
**23/23** (mesuré).

Cette corroboration est indépendante de la mesure PDF : elle ne vient ni du CSV
de diagnostic, ni de l'audit, mais d'un artefact produit par une autre chaîne.

### 4.1 Deux symptômes structurels que personne n'avait mesurés — et qui disparaissent

La revue hostile a cherché ce que la réparation aurait pu **casser**. Elle a
trouvé l'inverse : deux pathologies internes au graphe, jamais mesurées jusqu'ici,
s'effondrent.

- **Pages revendiquées par deux sections : 13 → 1.** En v110, treize numéros de
  page (58, 78, 148, 154, 161, 165, 173, 186, 202, 225, 241, 265, 277) étaient
  déclarés chacun par **deux** sections distinctes — c'est la signature même du
  défaut : la valeur restait sur le nœud pendant que la clé changeait de section,
  et venait doublonner la page d'une section voisine. En v111 il n'en reste
  **qu'un** (148), qui ne fait partie ni des 16 corrections ni de leurs voisins :
  dette préexistante, non touchée. **Aucun doublon de page n'a été créé.**
- **Parente postérieure à son enfant : 1 → 0.** v110 portait une inversion —
  `II.2.2` (p. 165) commençait *après* son premier enfant `II.2.2.a` (p. 161).
  Après réparation la famille s'ordonne : `II.2.2` 165 < `II.2.2.a` 167 <
  `II.2.2.b` 168 < `II.2.2.c` 170. `II.2.2` (`42f154e6`, statut `correct`,
  p. 165) n'a pas été touché : c'est le déplacement des enfants qui résout
  l'inversion. **Aucune inversion nouvelle.**

Ces deux mesures n'ont été demandées par personne : elles valent parce qu'elles
pouvaient contredire la réparation et ne l'ont pas fait.

## 5. Ce que l'applicateur vérifie avant d'écrire

`scripts/make_v111_apply_section_page_start_patch.py` refuse — il n'ignore pas —
toute op qui n'est pas un `SET_ATTRIBUTE` sur `page_start` visant une entité
vivante et typée section. Surtout, **la valeur ancienne est vérifiée, pas
supposée** : pour chacune des 16 ops, il exige la concordance de **trois sources
indépendantes** — la valeur réellement portée par le graphe, la valeur ancienne
inscrite dans le `_comment` de l'op (« page_start 202 -> 190 »), et la colonne
`page_start_actuel` du CSV de diagnostic (dont `page_imprimee_verifiee` doit par
ailleurs égaler la valeur cible, et `statut` valoir `incoherent`). Si le graphe
avait dérivé depuis la rédaction du patch, les trois ne concorderaient plus et
le script refuserait d'écrire.

Les vérifications d'après sont **exhaustives** : le résultat est comparé au
source entité par entité, attribut par attribut, relation par relation. Le
script n'écrit que si le diff complet vaut **exactement 16 valeurs de
`page_start` changées** — 0 clé créée, 0 supprimée, 0 nom, 0 type, 0 relation,
0 op, `types` / `relation_types` / `ops` identiques — et que les 49 `skipped`
sont inchangés.

Les chemins de refus ont été **testés** (sur copies, hors dépôt) : graphe dérivé,
op `SET_NAME`, op sur un autre attribut, entité inconnue, complétion d'un
`page_start` absent. Les cinq échouent, et **aucun** n'écrit de fichier.

## 6. Validations exécutées

| Contrôle | Résultat |
|---|---|
| `py_compile` de l'applicateur | OK |
| `--dry-run` | 16 corrections annoncées, **rien écrit** (vérifié : pas de fichier v111) |
| Application réelle | `grc20-these-mael-rolland-v111.json` écrit |
| JSON valide (v111, registre, `package.json`) | OK |
| Comparaison v110/v111 **par script indépendant** | mêmes entités (2 293, mêmes ids, même ordre), mêmes relations (20 207, identiques), `types` / `relation_types` / `ops` identiques, 0 clé créée ou supprimée, **16 valeurs `page_start` changées et rien d'autre** ; `space` : seuls `version` et `note` modifiés |
| `check_graph_integrity.py` | 0 — v111 courant : 0 endpoint cassé, 0 id dupliqué, 0 orphelin, version OK, 0 clé hors registre |
| `check_anchoring.py` | 0 — 46 problèmes, **aucune régression** (baseline inchangée) |
| `build_anchor_weights.py --check` | 0 — la carte est à jour (12 374 lignes) |
| `build_properties_registry.py` puis `--check` | 0 — registre régénéré depuis v111, 338 entrées, à jour |
| `preflight_candidate_patches.py` | 0 — **0 BLOQUANT** (53 OK / 8 avertissements, cf. § 7) |
| `audit_section_page_start.py --check` | **0 — plus aucune divergence** (36 vérifiés, 1 non établi) |
| Accord graphe / carte d'ancrage | **23/23** (était 20/23) |
| `node --check` sur les 4 `.mjs` modifiés | OK |

Le contrôle décisif est le dernier bloc : `audit_section_page_start.py --check`
**re-mesure les pages imprimées dans les PDF** (pypdf est disponible dans cet
environnement, le repli sur le CSV n'a pas été utilisé). Il sortait 1 avec
16 `DIVERGENCE` avant application ; il sort **0** après. Le mode `--check` avait
été écrit pour ce moment.

## 7. Écarts entre l'attendu et le constaté

Trois effets méritent d'être signalés plutôt que tus.

**(a) Le registre change — mais pas là où l'on regardait.** `page_start` garde
son `id`, son `valueType` (`NUMBER`), son `domain` (`[ThesisSection]`), son
`count` (**37**) et son `status` : mêmes porteurs, mêmes types, 16 valeurs
écrasées, 0 posée, 0 supprimée. Le seul champ modifié est `readBy`, qui gagne
`scripts/make_v111_apply_section_page_start_patch.py`. Le même effet touche 5
autres entrées (`section_key`, `status`, `note`, `type`, `source`) : le
générateur balaie les scripts du dépôt et y voit ces mots. C'est le comportement
établi de la maison — `make_v110` figure de la même façon dans le `readBy` de
`source`, `type`, `status`, `note` — et le registre le dit lui-même : pour ces
clés génériques, « `readBy` surestime son usage réel ». **Aucune extension de
domaine, aucune clé ajoutée ou retirée : 338 entrées avant, 338 après.**

**(b) Le préflight passe de 4 à 8 avertissements — sans blocage.** Les quatre
patchs candidats déclarent `source_graph = …v110.json` ; le graphe le plus
récent est désormais v111, et le contrôle C04 le signale pour chacun. C'est la
conséquence mécanique de tout changement de version (v110 l'avait produite pour
les patchs écrits contre v109), non un défaut introduit ici. **0 BLOQUANT, sortie
0, CI verte.** Les 3 candidats bibliographiques restent non appliqués et leurs
cibles existent toujours (C06 OK).

**(c) `anchoring-baseline.json` n'a pas été rafraîchi**, alors que les commits
v109 et v110 le faisaient. Vérifié avant de s'en abstenir : son champ `graph`
est **informatif** — `check_anchoring.py` ne lit que la liste `known`, et n'écrit
la baseline qu'avec `--write-baseline`. Le contrôle passe sans régression avec
la baseline telle quelle. La rafraîchir aurait modifié un fichier hors mandat
pour un champ que rien ne lit.

**(d) Le repli sans `pypdf` de `audit_section_page_start.py --check` est
indisponible pour v111.** Le script dérive le nom du CSV de la **version du
graphe audité** ; il cherche donc `section-page-start-diagnostic-v111.csv`, qui
n'existe pas. Mesuré en simulant l'absence de `pypdf` : sortie **2
(invocation)**, « CSV de diagnostic introuvable » — pas un faux « OK », pas un
faux échec de données. C'est le comportement voulu, documenté dans la docstring
de `csv_defaut` : mieux vaut refuser de conclure que comparer v111 à une preuve
établie pour v110. **Sans effet sur la CI** — les 8 étapes de
`.github/workflows/check.yml` n'appellent pas ce script — et sans effet ici, où
`pypdf` 6.14.2 est présent et où `--check` a **re-mesuré les PDF** et renvoyé 0.
Reste que le repli documenté est inopérant tant que le CSV v111 n'est pas
produit (`--csv`, qui exige `pypdf`). Le régénérer sortait du périmètre de ce
commit ; **c'est une dette ouverte, pas un oubli.**

**(e) `CLAUDE.md` n'a pas été mis à jour** et annonce toujours v110 comme
instantané canonique (le commit v110 avait, lui, retouché ce fichier). Hors
périmètre du mandat, qui énumère les fichiers autorisés. **À traiter avant le
merge** : la description du graphe, le compte de versions et la mention « v110
est l'instantané canonique » sont désormais faux.

## 8. Périmètre du commit

| Fichier | Nature |
|---|---|
| `grc20-these-mael-rolland-v111.json` | nouveau — le graphe |
| `scripts/make_v111_apply_section_page_start_patch.py` | nouveau — l'applicateur rejouable |
| `grc20-properties-registry-v1.json` | régénéré (même commit, comme l'exige la CI) |
| `package.json`, `these.html`, `graphe.html`, `lecteur.html`, `graph-worker.mjs`, `narrative-anchors-build.mjs`, `grc20-publish.mjs`, `export/scripts/export-workshop-to-public.mjs` | pointeurs de version — **16 occurrences, seul le numéro change** |
| ce rapport | nouveau |

Rien d'autre. `git diff` est vide sur les cartes d'ancrage, `Migration/`, les
patchs, et sur tout contenu non-version des fichiers runtime. Le commentaire de
`graphe.html:3218` qui mentionne « retypées … en v110 » a été **laissé tel
quel** : c'est un énoncé historique exact, pas un pointeur.

**Publication non faite** : `npm run dry-run` / `testnet` / `mainnet` et la mise
à jour d'`IPFS_CID` dans le Worker restent à la main de l'auteur.

---

## 9. Revue hostile — les neuf questions

Passée avant tout merge, conformément à la charte. Réponses avec leur preuve.

1. **Le script lit-il sa propre sortie ?** Non. `--source` est **codé en dur**
   sur v110 et l'applicateur exige `_meta.source_graph == basename(source)` : le
   relancer contre v111 échoue en invocation. Il n'est ancré nulle part sur « le
   graphe le plus récent ».
2. **Réécriture simultanée ou séquentielle ?** Sans objet : aucune table de
   correspondance, aucune clé n'est à la fois source et cible. 16 ops, 16
   `entityId` **distincts** (contrôlé par le script), chacune (entité, clé) →
   valeur. Aucun cycle possible.
3. **Le canonique retenu est-il le mieux relié ?** Sans objet : aucune fusion,
   aucun canonique désigné. Le doublon `97eb6267` / `3ce505bc` reste ouvert,
   conformément à P2 (a).
4. **Le compte mélange-t-il corps et notes ?** Sans objet : aucun comptage de
   mots. La mesure porte sur des numéros de page imprimés en pied de page.
5. **Le patch écrit-il hors de sa politique déclarée ?** Non — et c'est prouvé
   par le diff exhaustif : 16 valeurs `page_start`, rien d'autre dans 2 293
   entités et 20 207 relations. La liste blanche de l'applicateur (`page_start`
   seul) a été testée : une op sur `section_key` fait échouer le script.
6. **La vérification rejoue-t-elle la logique qu'elle vérifie ?** En partie, et
   c'est corrigé par l'extérieur : les contrôles internes de l'applicateur sont
   in-process, mais le verdict décisif vient d'un outil **indépendant** qui
   re-mesure les PDF (`audit_section_page_start.py --check`), d'un comparateur
   v110/v111 écrit séparément, et d'un artefact tiers (la carte d'ancrage,
   23/23). *Limite assumée* : ce comparateur a tourné hors dépôt et n'est pas
   rejouable en CI.
7. **Un renommage casse-t-il une table indexée par nom ?** Non : **aucun nom ne
   change**. Le diff exhaustif montre 0 modification de champ hors `attributes`.
   `STORY_FOCUS_ALIASES`, `story-presets.mjs` (`focusNodes`, `centralNode`) et
   `narrative-anchors.json` — qui référencent des entités par leur nom — sont
   donc structurellement hors d'atteinte.
8. **La branche est-elle rattachée à une PR encore ouverte ?** **Non — point de
   vigilance.** `HEAD` est exactement `c10c69c`, le commit de merge de la PR
   #116, elle-même close. Cette branche est réutilisée d'une PR à l'autre (#106
   → #116, base `codex/create-expand-from-node-planning-documents`, **pas**
   `main`) : le présent travail exige donc une **PR #117**, il n'apparaîtra pas
   dans #116.
9. **Ce correctif en cache-t-il un autre ?** Non : un objet, un effet. Le
   registre régénéré et les 8 pointeurs ne sont pas des effets distincts mais la
   convention de version du dépôt (mesurée sur les commits v109 et v110), et la
   CI exige le registre dans le **même** commit.

**Pièges du dépôt, vérifiés :** les deux types de section (`ThesisSection` /
`ChapterSection`) sont pris ensemble via `grc20_commun.TYPES_SECTION` —
`III.3`, seule `ChapterSection`, ne peut pas être tenue pour absente ; aucune
conclusion ne repose sur `occurrence_count` ; l'orpheline Ostrom n'est pas
signalée comme une découverte ; v96 et ses 15 endpoints cassés restent gelés en
rapport seul.

**Ce que la revue n'a pas pu attaquer :** (a) la **règle de preuve** elle-même —
que la page imprimée du titre soit le bon `page_start` d'une section est une
convention posée par le chantier précédent et validée par l'auteur, non
re-démontrée ici ; (b) les **16 pages imprimées** n'ont pas été relues à l'œil
dans les PDF : elles ont été re-mesurées par le même outil que celui qui les a
établies, ce qui n'est pas une source indépendante — la carte d'ancrage n'en
corrobore que 3 sur 16 ; (c) l'effet réel d'un `page_start` juste sur une
**publication GRC-20**, jamais exécutée ici.
