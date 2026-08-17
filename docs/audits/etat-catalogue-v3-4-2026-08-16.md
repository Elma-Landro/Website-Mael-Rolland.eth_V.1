# Catalogue v3-4 — les trois arbitrages de clôture — 16/08/2026

Lot de clôture avant le chantier « dossiers de crise ». Il applique les trois arbitrages Maël du 16/08/2026 : la canonisation E059 / G110, la correction d'acteur principal sur E059, et le marquage de seuil sur E032.

**Neuf cellules, sur trois lignes.** *Aucun graphe touché, aucune v116, aucun patch graphe, aucune fusion, aucun rôle posé, aucun recodage massif, aucune crise remplie, aucune décision R3.*

## 1. Empreintes

| fichier | avant | après |
|---|---|---|
| `catalogue-evenements-v3-3.csv` (**source, conservée**) | `7a87a37d9e05d7cbe096ece8d436506812ef68a4` | *identique* |
| `catalogue-evenements-v3-4.csv` (**produite**) | — | **`85d275da1ae7d672646268ab57d43273921b9d73`** |
| `catalogue-roles-v0.csv` | `a83570e9a87f93b9ff5ce5cfb665fdf6cf0c9bb5` | *identique* |
| `grille-roles-v0.md` | `fa2ee2d2353f5e708a35e04b25d74bd83df9b202` | *identique* |
| `vocabulaire-q7-v1-proposition.md` (Q7 v1 gelé) | `55bf8d9c5757bd096d9bbe77b78dfe402b61ba1b` | *identique* |

**Pourquoi une v3-4 plutôt qu'une modification sur place.** C'est la règle maison : `add_statut_ligne.py` a produit v3-2 depuis v3-1, `make_v3_3_catalogue.py` a produit v3-3 depuis v3-2, sans jamais écraser la source. Elle existe pour que les preuves déjà écrites restent vraies : plusieurs rapports de `docs/audits/` citent l'empreinte de v3-3 comme preuve que rien n'a bougé. Modifier v3-3 sur place aurait invalidé ces citations rétroactivement. **v3-3 est intacte**, et le script refuse d'écrire si `catalogue-evenements-v3-4.csv` existe déjà.

Conséquence mécanique : les deux pages de l'Observatoire ont été repointées de v3-3 vers v3-4 — une constante par page, vérifiée au navigateur.

## 2. Les neuf cellules

Applicateur : `scripts/make_v3_4_catalogue.py`. Lot figé dans le code, `--dry-run`, **diff recalculé cellule à cellule et comparé au lot déclaré** — le script refuse d'écrire s'il diverge d'un seul élément.

### E059 — acteur principal corrigé vers Coinbase (5 cellules)

| colonne | avant | après |
|---|---|---|
| `acteur_principal` | `institutions_financieres` | **`entrepreneurs_exchanges`** |
| `acteur_secondaire` | `entrepreneurs_exchanges` | **`institutions_financieres`** |
| `acteur_principal_mode` | *(vide)* | **`initiateur`** |
| `acteur_principal_id` | *(vide)* | **`8991d9f05d234b6d876d16334f60af63`** |
| `acteur_principal_nom` | *(vide)* | **`Coinbase`** |

`statut_ligne` reste `validee`. Aucun rôle posé, conformément à ton arbitrage — « *réalise la levée de fonds* » suffit à identifier le porteur, pas à coder un rôle sans surinterpréter.

**Deux points que tu n'avais pas listés dans la forme attendue, et que j'ai tranchés — dis-moi si l'un des deux te gêne, chacun est un aller-retour d'une cellule.**

**(a) L'inversion du secondaire.** Tu demandais que les financeurs anonymes ne restent pas acteur principal. Laisser `entrepreneurs_exchanges` en secondaire pendant qu'il devient principal aurait mis le même type deux fois sur la même ligne — le script a d'ailleurs un contrôle qui l'interdit (`C3d`). J'ai donc permuté : les financeurs descendent en secondaire, ce qui conserve leur présence dans l'événement sans leur laisser le premier rôle.

**(b) Le mode `initiateur`.** Ta forme attendue listait `nom` et `id`, pas `mode`. Je l'ai rempli quand même, pour la raison exacte que tu donnes à propos d'E032 : *« le champ `nd` est préférable à un vide ambigu »*. Un `id` et un `nom` posés à côté d'un `mode` vide auraient créé précisément ce vide-là. La valeur `initiateur` ne relève pas d'une interprétation nouvelle : c'est la branche que la règle A2/D7 désigne mécaniquement pour un acte ponctuel à agent identifié, et c'est le mot du texte source.

### G110 — doublon non canonique (2 cellules)

| colonne | avant | après |
|---|---|---|
| `statut_ligne` | `chantier` | **`douteuse`** |
| `notes` | *(description graphe)* | *(description graphe)* **+ mention du doublon** |

Convention du catalogue appliquée à l'identique de G011 et G013 au lot 3 : `douteuse` + note disant le doublon et la canonique. La note ajoutée : « *Doublon du même fait avec E059, qui est CANONIQUE (arbitrage du 16/08/2026) — signalé, non fusionné. Aucune fusion graphe, aucun patch, aucun rôle sur cette ligne.* » **La note existante n'est pas recouverte, elle est complétée.**

**Ce que G110 porte et que E059 n'a pas** — tu demandais que je le documente sans inverser la canonisation :

| information | E059 (canonique) | G110 |
|---|---|---|
| `gid` | *(vide)* | `7cda4562e3ee4e9c8bf969bdf639994a` — l'`InfrastructureEvent` du graphe |
| `acteurs_graphe` | *(vide)* | `Coinbase` |
| `source_graphe` | *(vide)* | `I.2.1 Un protocole débordé de carnavalesques improvisations d'acteurs` |
| `occurs_in` | *(vide)* | `Phase de maturation / Phase 3 Bitcoin [Concept]` |
| `domaine_8` | `i*` | `i` |
| lecture propre | la levée de 75 M $ comme **acte** | la levée **plus** la croissance de Coinbase comme plateforme |

Autrement dit, **G110 est la seule des deux à être reliée au graphe**. La canonique ne l'est pas. Ce n'est pas un motif d'inverser la canonisation — la source dit bien « l'entreprise Coinbase réalise » et c'est E059 qui porte cette lecture — mais c'est un rattachement qui manque à E059, et qui devra être décidé un jour : soit reporter le `gid` sur E059, soit assumer que la canonique du catalogue n'est pas la porte d'entrée du graphe. **Je ne l'ai pas fait** : reporter un `gid` est une opération de liaison catalogue/graphe, hors du périmètre de ce lot.

### E032 — seuil marqué (2 cellules)

| colonne | avant | après |
|---|---|---|
| `acteur_principal_mode` | *(vide)* | **`nd`** |
| `notes` | `annee a cheval poc/peche - phase indicative` | *(idem)* **+ la note de seuil** |

`acteur_principal_id` et `acteur_principal_nom` restent vides, comme demandé. Aucun rôle. La note ajoutée dit l'interprétation en clair : mélange d'un fait daté (entrée du capital-risque en 2012) et d'une série annuelle agrégée (2012-2015, ch.I n.90 l.639), le `mode nd` signalant que l'absence d'acteur principal est **interprétée, pas oubliée**, et la scission signalée comme possible et non faite.

**Une tension à connaître** : `acteur_principal` reste `institutions_financieres` à côté d'un `mode = nd`. Tu n'as pas demandé de vider ce champ et le vider perdrait l'information du codage v1. Cela se lit donc ainsi : la typologie v1 dit « institutions financières », et la forme A1 refuse de nommer un acteur principal parce que la ligne est un agrégat. C'est cohérent, mais c'est une cohabitation, pas une redondance.

## 3. Preuves

**Le diff est recalculé, pas déclaré.** Le script reconstruit le diff cellule à cellule entre v3-3 et sa sortie, puis le compare au lot figé dans son code ; toute divergence l'arrête. Mesure indépendante, faite après coup par un script séparé : **9 cellules, 3 lignes — E032, E059, G110 — et aucune autre**, sur un balayage des 345 lignes × 33 colonnes. Ordre des lignes inchangé, en-tête inchangé, 346 CRLF, zéro LF isolé, zéro octet `NUL`.

**Les vocabulaires gelés sont contrôlés sur tout le fichier**, pas seulement sur les trois lignes touchées : chaque `statut_ligne` de la sortie est dans D4, chaque `acteur_principal_mode` est dans A1. Distribution après lot : `validee` 95 · `chantier` **222** · `douteuse` **27** · `a_arbitrer` 1 ; modes A1 : vide 303 · `systeme_protocole` 32 · `initiateur` **9** · `nd` **1**.

**Cinq scénarios de sabotage** passés sur copie, tous refusés proprement avec code 1 :

| scénario | contrôle |
|---|---|
| déclarer une valeur « avant » fausse sur E059 | `C2d` — la cellule ne vaut pas ce que le lot attendait |
| inventer le mode `porteur` | `C3b` — hors vocabulaire A1 |
| inventer le statut `doublon` | `C3` — hors D4 |
| prétendre que E060 doit rester sans rôle | `C4` — E060 en porte un |
| annoncer 8 cellules au lieu de 9 | `C2` — compte déclaré faux |

**Un sixième contrôle a mordu sur son propre auteur.** Le garde-fou de non-contagion `C5` vérifie que deux lignes voisines n'ont pas bougé ; j'y avais déclaré E003 sans acteur principal, de mémoire. Le script a refusé de tourner : E003 porte `core_devs`. La constante a été corrigée par **mesure**, et le commentaire du script le dit. C'est la troisième fois de la journée qu'un contrôle attrape une supposition plutôt qu'une donnée — c'est exactement ce pour quoi ils sont là.

## 4. Vérification navigateur

Chromium, pages servies en HTTP, polices distantes coupées : **16 contrôles, 0 échec, 0 `pageerror`**. Les deux pages lisent bien `v3-4` (vérifié dans la ligne de provenance affichée), les totaux des quatre matrices sont inchangés (82 / 49 / 345 / 49), la file de diagnostic reste à 16, les quatre lignes hors périmètre R3 sont les mêmes.

Les compteurs suivent le lot sans intervention : `chantier` **223 → 222**, `douteuse` **26 → 27**. E059 et E032 restent listées en « validées sans rôle » ; **G110 en sort**, puisqu'elle n'est plus `validee`.

## 5. Périmètre tenu

Aucun graphe touché, aucune v116, aucun patch graphe, aucune fusion d'entités, aucun rôle posé — E059, E032, G110, E039, E066, E068 et E069 sont vérifiées sans rôle par un contrôle du script. Aucun recodage au-delà des trois lignes, aucune crise remplie, aucune décision sur le périmètre R3, aucun doublon fusionné.

Effet de bord traité dans le même lot : `count` ajouté aux exclusions du registre pour le nouvel applicateur (la méthode `bytes.count()`, deux occurrences vérifiées). `--check` reste vert **sans régénérer le registre**.

## 6. État de versement — ce lot arrive en deux temps

Ce lot n'a pas pu être versé d'un seul mouvement, et il faut savoir pourquoi. Voici l'ordre dans lequel il est arrivé — tout est en ligne.

| # | pièce | canal | trace |
|---|---|---|---|
| 1 | `scripts/build_properties_registry.py` (exclusion) | connecteur | `5894362` |
| 2 | `scripts/make_v3_4_catalogue.py` (applicateur) | connecteur | `3414316` |
| 3 | `catalogue-evenements-v3-4.csv` | **upload web** | empreinte vérifiée à l'arrivée : `85d275da…`, 151 341 octets, 346 CRLF, **identique octet pour octet** au fichier produit par l'applicateur |
| 4 | `catalogue-lab.html`, `catalogue-matrices.html`, ce rapport | connecteur | poussés **après** le CSV |

**Le motif du canal** : le CSV est en CRLF (346 séquences) et l'octet CR (0x0D) n'est pas émissible depuis la session qui a produit ce lot — un CR isolé placé entre deux caractères disparaît, ce qui n'est pas une normalisation de fins de ligne mais un filtrage, vérifié par sonde. Le connecteur transmet pourtant les octets sans les interpréter : il aurait donc déposé un fichier aux 346 CRLF aplatis en LF. Le `git push` direct est refusé par le proxy (403). L'upload web était le seul canal fidèle, et c'est celui que le dépôt documente déjà pour ce cas.

**Le motif de l'ordre** : les deux pages repointées cherchent `catalogue-evenements-v3-4.csv`. Poussées avant lui, elles auraient affiché leur panneau d'erreur — lisiblement, sans jamais montrer de fausse donnée, mais l'Observatoire aurait été hors service le temps de l'écart. Tant que le CSV n'était pas là, l'état distant restait **cohérent** : les pages y lisaient encore v3-3, qui existe et est juste. Attendre ne coûtait rien ; ne pas attendre coûtait un Observatoire cassé.

**Règle à retenir pour la suite** : tout fichier CRLF de ce dépôt — les CSV du catalogue et de la table de rôles — passe par l'upload web, et son empreinte se vérifie après coup. Le connecteur convient au reste.

## 7. Ce qui reste ouvert

1. Les deux points tranchés au §2 — l'inversion du secondaire sur E059, et le `mode = initiateur` — si l'un te gêne, c'est une cellule à revenir.
2. **Le `gid` de G110 manque à E059** : la canonique n'est pas reliée au graphe, la non-canonique l'est. À décider hors de ce lot.
3. La file de diagnostic, 16 lignes, dont les quatre crises E039, E066, E068, E069 — explicitement non traitées.

Les trois points de clôture étant réglés, **le chantier « dossiers de crise » peut s'ouvrir.**
