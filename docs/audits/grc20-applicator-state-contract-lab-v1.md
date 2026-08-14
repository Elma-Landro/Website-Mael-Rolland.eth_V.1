# Contrat d'état PRE / POST / MIXTE des applicateurs — Lab v1

**Date** : 2026-08-14
**Graphe courant** : `grc20-these-mael-rolland-v115.json` (inchangé — ce chantier n'écrit aucun graphe)
**Branche** : `claude/file-upload-branch-check-jw4cng`
**Mode agent** : A (instruction, aucune application)
**Arbitrage cadre** : Maël, 2026-08-14 — inventaire **large**, tous les `make_vNNN*` présents

**Périmètre tenu.** Aucun graphe écrit, aucun patch appliqué, aucun applicateur
ancien modifié, aucune primitive partagée introduite. Ce document mesure,
reproduit, classe et propose. Il ne migre rien.

---

## 0. Ce que ce document appelle « mesuré »

Le dépôt a une règle : *une donnée n'est pas un fait*. Elle s'applique ici à
moi-même. Toutes les valeurs de cet audit viennent d'exécutions sur un **banc
isolé** (copie complète du dépôt en scratchpad, 213 Mo), jamais du dépôt réel.
Quatre colonnes de l'inventaire sont statiques (lues dans le source), le reste
est observé.

Trois de mes propres relevés se sont révélés faux en cours de route et sont
consignés comme tels, parce qu'ils illustrent précisément le défaut étudié :

| Relevé initial | Ce que la mesure a montré |
|---|---|
| « v109 lit v107 » | **v109 lit v108** ; v107 est un second intrant en lecture seule (l'*oracle*) |
| « v104 refuse : fichier `--frise` absent » | Mon banc n'avait pas copié `docs/research/`. Complété, v104 refuse pour une **collision d'identifiant** — une vraie garde |
| « v115 reproduit l'historique : IDENTIQUE » | **Faux.** v115 a détecté `POST` et n'a *rien écrit* ; ma sonde comparait le fichier versé à lui-même et appelait cela une reproduction |

Le troisième est le défaut même que ce chantier documente — « reconnaître un
effet déjà présent ne suffit pas pour conclure » — reproduit par l'outil chargé
de le mesurer. Une sonde de reproduction doit **effacer la cible avant de
lancer**, et traiter « rien écrit » comme distinct de « écrit à l'identique ».

---

## Phase A — Inventaire

**18 applicateurs** `make_vNNN*` dans `scripts/`, de v97 à v115.
Preuve : `docs/audits/data/applicator-inventory-current.csv` (20 colonnes),
généré par `scripts/build_applicator_inventory.py`.

### A.1 — Le trou : v106

**Le graphe `grc20-these-mael-rolland-v106.json` existe. Le script qui l'a
produit n'est pas dans le dépôt.** v106 est la migration des sections des
chapitres II et III (13 renumérotées, 11 créées) — la plus lourde de la série,
celle dont `CLAUDE.md` signale encore le piège des trois clés homonymes.

C'est le seul maillon de la chaîne v96 → v115 sans applicateur. Il n'est pas
« non rejouable » : il est **non rejouable et non inspectable**.

### A.2 — Les six familles

Établies **après** mesure, jamais depuis l'âge du script.

| Famille | Applicateurs | Trait déterminant |
|---|---|---|
| `reconstruction-integrale` | v97 | reconstruit la cible depuis la source, ne lit jamais sa propre sortie |
| `patch-declaratif` | v98, v99, v100, v105, v107, v110 | un patch versé porte `source_graph` ; l'applicateur le confronte |
| `transformation-directe` | v101, v102, v103, v104, v108 | la règle est dans le code, aucun patch |
| `lot-correle-multifichier` | **v109, v115** | écrit le graphe **et** les deux cartes d'ancrage |
| `patch-candidat-verrouille` | v111, v112, v113, v114 | patch candidat + lot figé + `space.version` de la source |
| *(absente)* | v106 | — |

### A.3 — Rejouabilité aujourd'hui, distincte de l'état historique

**Les 18 graphes sources sont présents** (v96 → v115). `source_graph_present`
vaut donc `oui` partout : aucun applicateur n'est orphelin de sa source.

`rejouable_now = non` pour **deux** applicateurs, et dans les deux cas **c'est
la garde qui fait son travail**, pas une avarie :

| | Motif mesuré |
|---|---|
| v109 | les cartes du dépôt sont déjà dans leur état d'après ; rejouer redéplacerait des charges déjà posées |
| v115 | `etat_du_lot()` détecte `POST` (cible absente → `MIXTE`) et refuse |

**Non rejouable ≠ inutile, et ≠ défectueux.** Ce sont les deux seuls lots
corrélés, et ce sont exactement les deux qui refusent : le lot corrélé et le
refus vont ensemble, ce n'est pas une coïncidence de calendrier.

### A.4 — Reproduction de l'historique : le vrai clivage

Sonde : relancer vN → vN+1 dans le banc, comparer au vN+1 versé.

| Résultat | Applicateurs |
|---|---|
| **IDENTIQUE** (octet pour octet) | v97, v98, v99, v107, v110, v111, v112, v113, v114 |
| **DIFFERENT** | v100, v101, v102, v103, v104, v105, v108 |
| **REFUSE / non rejoué** | v109, v115 |

Les écarts, caractérisés un par un — aucun n'est « champs internes » :

| | Écart mesuré | Portée |
|---|---|---|
| v100 | écrit `space.generated_at` là où le dépôt porte `space.generated_at_source` | clé renommée après coup |
| v101, v102, v103, v104 | **`space.version` reste celle de la source** | voir A.5 |
| v103 | en plus : `relation_count` 20 114 contre 20 123 versés | **9 relations du v103 versé ne viennent pas de ce script** |
| v105 | 117 entités diffèrent ; `space.description` désaccentuée (« these » pour « thèse ») | à instruire |
| v108 | `space.note` seule | accumulation d'historique, bénin |

### A.5 — Un défaut ancien, mesuré et non corrigé

**Neuf applicateurs n'écrivent pas la version de leur cible** : `space.version`
est hérité de la source. Mesuré, pas déduit — v101 relancé produit un fichier
nommé `…-v101.json` qui déclare `"version": "v100"`.

Ce fichier serait **refusé par `check_graph_integrity.py`**, qui exige que la
version déclarée corresponde au nom du fichier. C'est la même famille que le
défaut n° 2 de #126 (« `POST` vérifiait le contenu, jamais la version »), mais
côté écriture, et il existe dans le dépôt depuis v97.

Trois manières de fixer la version cohabitent :

| Manière | Applicateurs | Remarque |
|---|---|---|
| héritée de la source (donc fausse) | v97, v98, v99, v101–v105, v107 | 9 applicateurs |
| dérivée du **nom du fichier cible** | v108, v109 | version et nom ne peuvent pas diverger |
| **constante** `VERSION_CIBLE` | v110 → v115 | version et nom peuvent diverger — d'où le contrôle ajouté en #126 |

**Rien n'est corrigé.** Ces neuf applicateurs ont produit des graphes corrects
en leur temps (les fichiers versés portent la bonne version : quelqu'un l'a
écrite, mais pas eux). Les modifier n'aurait de sens que pour un rejeu réel.

---

## Phase B — Le contrat proposé

### B.1 — La forme minimale, et pourquoi elle ne suffit pas telle quelle

La forme de départ (chaque composant `PRE` / `POST` / `OTHER`, global `MIXTE`
dès qu'ils divergent) **couvre les deux lots corrélés et rien d'autre** : elle
suppose des composants comparables à un état attendu. Sur les 16 autres
applicateurs, il n'y a qu'un composant, et « `PRE` » y signifie seulement « la
source est la bonne ».

Elle demande trois amendements, tirés des mesures ci-dessus.

**1. Un troisième état de composant, `ABSENT`, distinct de `OTHER`.**
Une cible absente est l'état *normal* avant application ; une cible présente et
fausse est une anomalie. Les confondre rendrait `PRE` inatteignable. v115 le
fait déjà de fait (`cible_existe`), mais sans le nommer.

**2. Le composant se compare sur un couple `(contenu, identité)`.**
Le contenu est ce que le lot promet ; l'identité est ce qui rend le fichier
*lui-même* — son `space.version` et **son chemin canonique**. Les deux défauts
de #126 (version fausse, cible hors dépôt) sont des égalités de contenu avec
une identité fausse. Sans ce couple, le contrat les déclare `POST`.

**3. `POST` décrit l'état complet attendu, y compris les effets non-fichiers.**
Formuler `POST` comme « le fichier est égal à ceci » est trop faible pour un lot
dont l'après ne se résume pas à une égalité — v103 pose des relations sur des
entités *existantes*, v101 retire des ops. Pour ces cas, `POST` est un
**prédicat** (« aucune op orpheline ne subsiste »), pas une comparaison.

### B.2 — Le contrat, et les sept cas que tu as posés

| Situation | Verdict | Par quoi |
|---|---|---|
| cible absente | composant `ABSENT` → global `PRE` si les autres sont `PRE` | existence |
| cible présente mais incorrecte | `OTHER` → **`MIXTE`, bloquant** | prédicat de contenu |
| cible correcte, mauvais `space.version` | `OTHER` → **`MIXTE`** | volet *identité* du couple |
| bon contenu, hors chemin canonique | **refus en amont**, avant tout classement | le chemin est une précondition d'invocation, pas un état — v115 l'a appris en #126 : classer un fichier qui n'est pas celui du lot, c'est statuer à côté |
| plusieurs sorties, certaines en `POST` | `MIXTE` **bloquant**, avec le détail chiffré | agrégation |
| applicateur historiquement non idempotent | hors contrat — voir B.3 | — |
| `POST` non réductible à une égalité de fichier | `POST` comme **prédicat** | B.1 amendement 3 |

### B.3 — Le cas que le contrat ne doit pas prétendre couvrir

Un applicateur **non idempotent** ne peut pas être protégé par un contrat
d'état : la question « suis-je déjà passé ? » n'a pas de réponse lisible dans
la donnée quand l'opération est cumulative. Le dépôt en montre deux formes :

- **naturellement idempotent** — v101 (« rien à retirer »), v103 (écarte les
  domaines déjà posés), v107, v108 (« déjà conformes »), v105 (no-op sur des
  données déjà dédoublonnées). Ils acceptent le rejeu **et ne font rien**. Le
  contrat leur est un confort, pas une nécessité ;
- **protégé par accident** — v98 (échoue sur 31 problèmes de validation), v102
  (échoue parce que l'entité a été consommée), v104 (collision d'identifiant).
  Ils refusent, mais **par avarie, pas par garde**. Un changement de données
  peut lever l'avarie sans lever le danger.

**La distinction est mesurée, pas supposée** : la colonne
`mecanisme_deja_applique` nomme la cause observée, pas le verdict.

---

## Phase C — Les quatre familles de défauts, reproduites

Toutes sur banc isolé. Pour chaque famille : l'ancien comportement mesuré, puis
ce que le contrat proposé donnerait.

### C.1 — Effet principal présent, état `POST` incomplet

**Reproduit sur v115 avant #126.** La garde concluait « DÉJÀ APPLIQUÉ » dès la
*première* carte trouvée corrigée. Une carte corrigée et l'autre non se lisait
comme un succès, code 0.

**Toujours présent dans v109** : sa garde n'inspecte que les **clés témoin des
cartes**. Le graphe n'entre pas dans son verdict. Un v109 absent avec des cartes
converties est indistinguable, pour lui, d'une application réussie.

→ *Contrat* : le graphe est un composant du lot ; `MIXTE` bloquant.

### C.2 — Métadonnée d'identité fausse

**Reproduit sur l'ancien code de v115** : un fichier au contenu exact déclarant
`space.version = "v114"` recevait `POST` et **code 0**, alors que
`check_graph_integrity.py` le rejette. Le lot était déclaré sain et rouge en
même temps.

**Versant écriture, mesuré sur 9 applicateurs** : `space.version` héritée de la
source (A.5).

→ *Contrat* : volet *identité* du couple ; `MIXTE`.

### C.3 — Lot multifichier partiellement écrit

**Reproduit sur v109, aujourd'hui, et c'est le résultat le plus dur de ce
chantier.** Cartes ramenées en état pré-v109 (bijection inversée), écriture du
graphe sabotée :

```
code de sortie              : 1
graphe v109 écrit           : False
cartes modifiées quand même : True   (les deux)
dernière ligne              : IsADirectoryError: [Errno 21] Is a directory
rejeu pour réparer          : code=1
   « les cartes semblent DEJA converties (aucune cle temoin pre-conversion) »
```

Trois choses à la fois : l'échec n'est pas rattrapé (trace Python nue), les deux
cartes restent converties sans graphe, **et le rejeu destiné à réparer est
bloqué par sa propre garde**. La protection devient le verrou. L'état MIXTE est
irréversible sans intervention manuelle.

**v115, même provocation, après #126** : cartes restaurées octet pour octet,
cible retirée, aucun `.tmp` laissé, code 1 avec un message qui dit quoi faire.

→ *Contrat* : sérialisation complète avant toute mutation, bascule bornée,
restauration.

### C.4 — Cible détournée hors du périmètre

**Reproduit sur l'ancien code de v115**, en état `PRE`, `--target` hors dépôt :

| | code | graphe hors dépôt | cartes du dépôt corrigées |
|---|---:|---|---:|
| avant | **0** | oui | **20** |
| après | 2 | non | 0 |

L'applicateur **fabriquait lui-même** l'état MIXTE que sa classification existe
pour refuser. Atteignable seulement en `PRE` — c'est-à-dire exactement quand on
applique.

→ *Contrat* : précondition d'invocation, **avant** le classement.

---

## Phase D — Proposition d'architecture

### D.1 — Ce qui mérite une primitive partagée

Trois choses seulement, parce qu'elles sont identiques d'un lot à l'autre et
qu'elles ont chacune produit un défaut réel :

1. **`ecrire_lot(sorties)`** — sérialise **tout** (avec `fsync`), puis bascule,
   puis restaure si une bascule échoue. Aucune sémantique métier. C'est le code
   de v115 après #126, sans une ligne de Favier.
2. **`exiger_cible_canonique(chemin, attendu)`** — précondition d'invocation.
3. **`classer(composants) -> PRE | POST | MIXTE`** — agrégation pure, prenant
   en entrée une liste d'états déjà décidés par l'applicateur.

### D.2 — Ce qui doit rester propre à chaque applicateur

**Le prédicat `PRE` et le prédicat `POST` de chaque composant.** C'est là que
vit la sémantique du lot, et la mutualiser reviendrait à prétendre que « déjà
appliqué » veut dire la même chose pour un renommage de libellé (égalité de
chaîne), un retrait d'ops orphelines (« aucune ne subsiste ») et un
rebranchement de charges d'ancrage (« les clés témoin ont disparu »).

C'est le piège principal de ce chantier : une primitive trop ambitieuse
**cacherait les différences de sémantique** au lieu de les rendre explicites.
La primitive doit exiger les prédicats, pas les fournir.

### D.3 — Où elle vivrait

`scripts/grc20_commun.py`, qui porte déjà `REPO`, la recherche du graphe le plus
récent et l'analyse de version — et que la maison importe plutôt que de
redériver. Pas de nouveau module.

### D.4 — Stratégie d'écriture corrélée, minimale

Dans cet ordre, chacun justifié par un défaut reproduit ci-dessus :

1. valider **toutes** les préconditions, cible canonique comprise (C.4) ;
2. classer, refuser sur `MIXTE` (C.1, C.2) ;
3. sérialiser **toutes** les sorties en temporaires, `fsync` (C.3) ;
4. relire l'original de ce qui existe déjà ;
5. basculer par `os.replace` ;
6. sur échec de bascule : restaurer les fichiers déjà basculés, retirer les
   créations, nettoyer les temporaires, sortir en erreur explicite (C.3) ;
7. nettoyer.

POSIX ne rend pas un lot de N fichiers atomique. Ce protocole ne le prétend pas :
il réduit la fenêtre dangereuse à N renommages et rend la panne réversible.

### D.5 — Ce qui est testable automatiquement

| Propriété | Comment |
|---|---|
| `space.version` == nom du fichier produit | déjà fait par `check_graph_integrity.py` — mais **après** coup |
| cible canonique | assertion d'invocation |
| lot corrélé : aucun `.tmp` résiduel | après-contrôle |
| rollback effectif | provocation par `os.replace` sabotée, comme en C.3 |
| classement exhaustif | table de vérité des 2ⁿ combinaisons pour un lot à n composants |
| reproduction de l'historique | la sonde de cet audit, **cible effacée d'abord** |

### D.6 — Ce que je ne recommande pas

- **Migrer les 16 applicateurs mono-fichier.** Ils écrivent un fichier ; le
  protocole corrélé ne leur apporterait rien et réécrirait du code qui a produit
  des graphes justes.
- **Corriger les 9 `space.version` héritées** sans besoin de rejeu réel. Le
  défaut est mesuré ; il est sans effet tant qu'on ne rejoue pas.
- **Rendre le contrat obligatoire pour les idempotents naturels** (v101, v103,
  v107, v108). Il leur serait un confort, pas une protection.
- **Toucher à v109.** Son défaut est réel et reproduit, mais le corriger n'a
  d'intérêt que si l'on veut pouvoir le rejouer — ce qui n'est pas le cas.

---

## Ce qui attend une décision

1. **v106 n'a pas d'applicateur.** Le maillon le plus lourd de la chaîne est le
   seul non inspectable. Faut-il le reconstruire *a posteriori*, ou acter que
   v106 est un état historique dont seul le résultat fait foi ?
2. **v103 versé porte 9 relations que son script ne produit pas.** À instruire :
   soit un intrant a changé, soit une retouche hors applicateur.
3. **v105 : 117 entités divergent au rejeu, et la description se désaccentue.**
   Même question.
4. **La primitive de D.1 : la créer maintenant, ou au prochain lot corrélé ?**
   Aucun `make_v116` n'est prévu ; une primitive sans usage vieillit mal.
