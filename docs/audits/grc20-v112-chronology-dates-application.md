# GRC-20 v112 — application du patch chronologie minimal

**Date** : 2026-08-09
**Graphe source** : `grc20-these-mael-rolland-v111.json`
**Graphe produit** : `grc20-these-mael-rolland-v112.json` — **canonique**
**Branche** : `claude/file-upload-branch-check-jw4cng`
**Applicateur** : `scripts/make_v112_apply_chronology_dates_patch.py` (`--dry-run`)
**Patch appliqué** : `patch_candidate_chronology_dates_v1.json` — 2 ops
**Instruction** : chantier Chronology, Dates & References Verification Lab (PR #118), `docs/audits/grc20-chronology-dates-references-lab-v1.md`
**Arbitrage** : Maël Rolland, 2026-08-09, réponses 2 et 3

Première application de la phase « Patch Application Queue » : on cesse d'accumuler des patchs candidats, on en applique un, borné, déjà arbitré et déjà prouvé.

---

## 1. Ce que v112 change — deux valeurs, rien d'autre

| Entité | Attribut | v111 | v112 |
|---|---|---|---|
| `ca278d213d804294a2c5a672d52808e4` — CVE-2014-0160 Heartbleed | `date` | `04/07/2014` | `2014-04-07` |
| `0d81bba0461d49a5af8997a20663d630` — InfrastructureEvent — BitcoinTalk forum created | `date` | `2010-11-22` | `2009-11-22` |

**Heartbleed.** `04/07/2014` est la **seule** valeur du graphe à se lire MM/JJ. Sur les 54 valeurs à barres, 26 sont décidables sans convention (un groupe > 12) et donnent **JJ/MM 26 / MM/JJ 0**. L'alerte versionnée de Bitcoin.org (`_alerts/2014-04-11-heartbleed.html`, front-matter `date: 2014-04-11`) établit que la réponse est du 11 avril : elle ne peut pas précéder de trois mois un événement du 4 juillet. Arbitrage rendu : **cellule fausse** de la figure « Chronologie n° 4 », non seconde convention de format.

**BitcoinTalk.** Coquille d'année — même jour, même mois, un an d'écart. L'archive Nakamoto porte « Date: November 22, 2009 » pour le fil « Welcome to the new Bitcoin forum! », et **l'attribut `description` de cette fiche même dit « novembre 2009 »** : elle se contredit. Réserve déclarée dans le patch : les trois URL viennent d'un même dépôt d'archive, donc non indépendantes.

---

## 2. Preuve qu'aucune autre donnée n'a bougé

Comparaison v111 / v112 refaite **indépendamment de l'applicateur**, après écriture :

```text
entites   : 2293 -> 2293      relations : 20207 -> 20207
types            identiques : True      relation_types identiques : True
relations        identiques : True      ops            identiques : True
memes ids d entites : True
cles d attributs identiques (noms ET effectifs) : True  (335 cles)

changements TOTAUX hors `space` : 2
   ca278d21  date  04/07/2014 -> 2014-04-07   (options {language: fr} preservees)
   0d81bba0  date  2010-11-22 -> 2009-11-22   (options {language: en} preservees)

space : seules `version` et `note` changent
```

`entity_count` et `relation_count` de `space` sont réécrits mais retombent sur les mêmes valeurs, les effectifs étant inchangés.

**`space.note` est bornée à 1 200 caractères au total**, et non plus seulement sur sa partie héritée. La revue hostile a relevé que la note enflait de version en version — 1 513 (v110), 1 703 (v111), et 1 910 dans le premier jet de v112 — parce que le tronçage ne portait que sur l'héritage tandis que le préambule neuf s'ajoutait par-dessus. CLAUDE.md demande ~1 200 : l'applicateur borne désormais le total, et la note mesure exactement 1 200 caractères.

L'applicateur porte lui-même ce contrôle : il compare le résultat à la source **entité par entité, attribut par attribut, relation par relation, type par type**, et refuse d'écrire si le diff complet ne vaut pas exactement deux valeurs de `date` changées.

> **Corrigé après revue hostile.** Une première version de `signature()` projetait sur une liste de champs écrite à la main — `name`, `description`, `types`, `attributes` — et ratait donc les **3 entités du graphe qui portent en plus une clé `type` au singulier**. Un contrôle qui se dit exhaustif ne doit pas dépendre d'une liste qui vieillit dès qu'une entité gagne un champ. `signature()` énumère désormais **tous** les champs de tête, et `diff_exhaustif()` signale les créations et suppressions de champ. Sans effet ici — l'applicateur n'écrit que `attributes['date']['value']` — mais l'affirmation était plus large que le code.

### Les `options` sont préservées — choix déclaré

Le dialecte du dépôt n'exprime qu'un couple `{type, value}`, alors que les deux attributs visés portent un `options.language` (`fr` et `en`), sémantiquement vide sur une date. Les **retirer** aurait été une modification que personne n'a arbitrée, et aurait fait mentir la promesse « exactement deux valeurs changées ». L'applicateur réécrit donc la seule clé `value`. **Purger les `options.language` des dates est un chantier distinct**, non ouvert ici.

---

## 3. Ce que cette version refuse de faire

- **Aucun `duplicateOf`, aucun `reviewStatus`, aucune fusion.** La fiche `0d81bba0` a très probablement une jumelle, `06ac37fc`, qui porte déjà la bonne date. Marquer le doublon désignerait une canonique — or **`0d81bba0`, la fiche corrigée, a un degré de 24 contre 22** pour `06ac37fc` : la fiche fausse est la **mieux reliée**. C'est le piège **C5** de `grc20-dedup-events-audit-v1.md`, et le motif même pour lequel l'auteur refuse par ailleurs la fusion Mining pools. Corriger une date n'autorise pas à trancher une identité. L'applicateur refuse explicitement toute op portant ces deux clés.
- **Aucun nœud créé, aucune SourceQuote, aucun retypage, aucun renommage.**
- **Aucune autre date touchée** — ni les 27 valeurs ambiguës restantes, ni les 86 sans source déclarée. (27 et non 28 : `04/07/2014` faisait partie du lot ambigu, et l'op n° 1 en corrige une — voir § 7.)

---

## 3 bis. La conséquence que cette version produit — mesurée après revue hostile

> **Ajouté après revue hostile.** La première version de cet audit écrivait que « le doublon probable BitcoinTalk reste une dette ». **C'est faux tel quel : la dette a changé de nature**, et v112 en est la cause. Il fallait le mesurer avant d'écrire, pas après.

`scripts/verif_doublons.py` est l'instrument de dédoublonnage du dépôt. Exécuté sur les deux graphes, sorties redirigées hors du dépôt :

```text
v111 : 78 paires · FUSION_SURE 4 · A_VERIFIER 14 · REJET_AUTO 60
v112 : 78 paires · FUSION_SURE 4 · A_VERIFIER 15 · REJET_AUTO 59
```

Une seule paire bouge, et c'est la nôtre :

```text
v111  REJET_AUTO ; motif = « dates contradictoires (2010-11-22 / 2009-11-22) »
v112  A_VERIFIER ; motifs = « meme type ; dates identiques ; identifiants
                              compatibles ; 15 cible(s) commune(s) ;
                              chevauchement de description »
```

**La date fausse était le veto.** Tant que `0d81bba0` portait 2010, le mécanisme *refusait* d'examiner la paire. En la corrigeant, v112 supprime cette protection : la paire entre dans `A_VERIFIER`, et le CSV produit **désigne une canonique** — exactement ce que l'applicateur, le patch et cet audit s'interdisent tous les trois.

Corroboration indépendante, sur le graphe seul — entités partageant `(date, description, types)` :

```text
v111 : 0 collision
v112 : 1 collision  ->  0d81bba0 / 06ac37fc, date 2009-11-22
```

**v112 crée l'unique collision d'empreinte du graphe.** Elle n'existait pas avant.

L'énoncé juste n'est donc pas « la dette reste entière » mais : **v112 échange une contradiction visible contre une duplication invisible.** Avant, un lecteur voyait deux dates pour un même fait — un défaut criant. Maintenant il voit deux fois le même événement, à la même date, sans marqueur.

Ce n'est pas une raison de défaire v112 : la date corrigée est juste, et laisser une date fausse pour qu'elle serve de garde-fou serait absurde. Mais cela **déplace l'urgence** de l'arbitrage d'identité, et cela doit être écrit ici pour que le prochain agent qui relancera `verif_doublons.py` sache que la convergence des deux fiches est le produit d'un patch de date, non une découverte. Le degré 24/22 rend d'ailleurs la canonique proposée par l'automate *plausible* — donc convaincante, donc dangereuse.

**Dommage collatéral, non corrigé ici** : `docs/audits/data/doublons-verifies.csv` (base v97) porte encore `REJET_AUTO … « dates contradictoires (2010-11-22 / 2009-11-22) »`. Ce n'est plus seulement périmé : le **motif** qu'il invoque n'existe plus. Le régénérer sortirait du périmètre de cette PR.

---

## 3 ter. Arbitrages de l'auteur sur cette version — 2026-08-09

Rendus après lecture de la PR #119 et de la revue hostile. Ils ne modifient pas v112 ; ils fixent ce que v112 **signifie**, et ce qu'il laisse ouvert.

### `date` pour Heartbleed : une date de divulgation publique, et une dette de modélisation

**La sémantique générale de `date` n'est PAS tranchée ici.** Pour `ca278d21` seulement, `2014-04-07` doit se comprendre comme **la date publique pertinente de l'événement — la divulgation publique**, et non comme une date d'exploitation ou d'incident.

**Dette de modélisation inscrite** : l'attribut `date` mélange encore, selon les fiches, une date d'incident, une date de divulgation, une date d'activation et une date narrative. La revue hostile l'a mesuré sur les 4 fiches CVE portant les deux clés — `date` y précède systématiquement `publicDisclosure` de plusieurs semaines :

```text
CVE-2012-3789  date 12/05/2012  publicDisclosure 20/06/2012
CVE-2013-2293  date 09/01/2013  publicDisclosure 14/02/2013
```

Ce n'est **pas un blocage pour v112**. C'est un chantier de modélisation à ouvrir, qui devra dire ce que `date` désigne, fiche par famille.

### Format ISO isolé : maintenu, et signalé

`2014-04-07` est **maintenu**. Ne pas revenir à `07/04/2014`.

`ca278d21` devient de ce fait **la seule valeur ISO d'une cohorte de 31 fiches `cveId` dont 25 sont en `NN/NN/AAAA`**. Le signalement est requis, mais c'est préférable à réintroduire une date à barres ambiguë — elle appartenait au lot des 28 indécidables, et l'y remettre reconstituerait l'ambiguïté que cette version lève. **La normalisation globale des formats est un chantier distinct.**

### Provenance : aucune `dateSource` ajoutée, et une dette explicite

**Aucune `dateSource` n'est ajoutée dans ce patch**, faute de source externe vérifiée. `crisis.html` corrobore que le runtime affichait déjà `07/04/2014` avec `month: 4`, mais **un fichier du site n'est ni une source scientifique ni une source primaire** : il ne peut pas fonder une `dateSource`.

Donc, en toutes lettres :

- la correction de date est **conservée** ;
- `ca278d21` est désormais **une correction prouvée par convergence interne (les 26 valeurs décidables du graphe) et par le runtime**, mais **sans provenance externe déclarée** ;
- **dette inscrite** : ajouter une provenance Heartbleed lors du futur chantier `dateSource`. C'est la seule fiche du graphe dont on sait qu'elle diverge de sa source imprimée, et c'est aussi celle qui ne déclare aucune provenance — l'anomalie est nommée, non comblée.

### BitcoinTalk : pas de `duplicateOf`, pas de fusion, arbitrage d'identité prioritaire

L'effet découvert au § 3 bis **n'est pas une raison de garder la date fausse**. Mais il rend **prioritaire un futur arbitrage d'identité BitcoinTalk**. En attendant : aucun `duplicateOf`, aucune fusion.

---

## 4. Garde-fous de l'applicateur, testés un par un

Le lot est **figé dans le script**, pas seulement déclaré par le patch : un patch retouché entre l'arbitrage et l'application ne doit pas passer parce qu'il aurait mis à jour son propre `op_count`. Chaque refus a été provoqué :

| Situation | Attendu | Constaté |
|---|---|---|
| cible == source | refus | exit 2 |
| cible en `v113` | refus | exit 2 |
| patch élargi à 3 ops | refus | exit 1 |
| entité hors du lot figé | refus | exit 1 |
| op sur `duplicateOf` | refus | exit 1 |
| ancienne valeur non concordante | refus | exit 1 |
| `options` non concordantes | refus | exit 1 |
| même entité visée deux fois | refus | exit 1 |
| policy `CANDIDATE` retirée | refus | exit 1 |

**L'ancienne valeur est vérifiée, pas supposée.** Chaque op du patch porte un bloc `_expected` (type, value, options) lu dans v111. L'applicateur exige la concordance des trois champs avant d'écrire : si le graphe a dérivé depuis la rédaction du patch, il refuse. Écriture **atomique** (fichier temporaire puis `os.replace`).

---

## 5. Pointeurs de version et registre

Huit fichiers portaient le nom du graphe et ont été mis à jour, selon la convention mesurée sur v111 : `package.json` (4), `grc20-publish.mjs` (3), `graphe.html` (2), `these.html` (2), `narrative-anchors-build.mjs` (2), `lecteur.html` (1), `graph-worker.mjs` (1), `export/scripts/export-workshop-to-public.mjs` (1). Plus `CLAUDE.md`. `scripts/make_v111_apply_section_page_start_patch.py` cite v111 **et doit continuer de le faire** : c'est sa propre version.

Le registre est régénéré dans le même commit : `source_graph` passe à v112, **338 entrées, aucune clé ajoutée ni retirée, aucun changement de `status`**.

Deux entrées ont été ajoutées à `EXCLUSIONS_READ_BY` — `duplicateOf` et `reviewStatus` pour cet applicateur. Il ne les lit pas : il les nomme dans `CLES_INTERDITES` **pour les refuser**. Les y laisser aurait fait dire à `readBy` le contraire de ce que fait le script, et précisément sur les deux clés dont le non-écrit est l'objet de cette version. C'est la correction d'un faux positif présent, non une extension par anticipation — et elle reste réversible d'une ligne si l'auteur préfère la trace brute.

---

## 6. Validations exécutées

```text
JSON valide (v112, registre, package.json)          OK
py_compile applicateur + generateur de registre     OK
node --check des 4 .mjs modifies                    OK
--dry-run de l'applicateur                          OK
check_graph_integrity.py                            exit 0
check_anchoring.py                                  exit 0
build_anchor_weights.py --check                     exit 0
build_properties_registry.py --check                exit 0
preflight_candidate_patches.py                      exit 0
audit_chronology_dates.py --check                   voir § 8
classify_date_evidence.py --check                   exit 0
comparaison v111/v112 independante                  exactement 2 changements
```

---

## 7. Dettes explicitement NON traitées

Aucune n'est refermée par cette version — **à une exception près, signalée après revue hostile** : le lot des valeurs à barres ambiguës passe de 28 à 27, `04/07/2014` en ayant fait partie. Le `skipped` n° 1 du patch affirme « aucune de ces 28 valeurs n'est fausse sous JJ/MM » dans le fichier même dont l'op n° 1 en corrige une : contradiction interne du patch, recopiée ici sans être vue. Pour tout le reste :

- **le doublon probable BitcoinTalk** (`0d81bba0` / `06ac37fc`) — dette entière, canonique non désignée ;
- **la grappe Mining pools à cinq fiches**, traversant les types, et les 3 fiches `duplicate-pending-merge` depuis v105 ;
- **`120e6fa2`** — perte wallet.dat 2010 contre vol Allinvain 2011 sur une même fiche, séparation arbitrée mais non exécutable en patch candidat ;
- **NewLibertyStandard** et les 6 autres `two_distinct_events_possible` ;
- **les 27 valeurs `NN/NN/AAAA` ambiguës restantes** — et non 28 : `04/07/2014` en faisait partie (`dmy_ambiguous = oui` dans l'inventaire du chantier), et **v112 en a réécrit une**. Recompté : v111 en portait 28, v112 en porte 27, les 26 décidables restant inchangées. La convention JJ/MM est confirmée, aucune des 27 n'est réécrite ;
- **les 86 dates sans `dateSource`**, et les 37 renvois vers des figures absentes du dépôt ;
- **les 237 doubles descriptions** — chantier séparé ;
- **The DAO** — reste `non_verifie` ;
- **les 23 `doublon_probable`** et 13 `indetermine` du relevé d'identité ;
- **Casascius**, Istanbul, BitLaundry, l'écart 664/652 de la bibliographie.

---

## 8. Limites connues et exceptions acceptées

### `audit_chronology_dates.py --check` échoue — ce n'est PAS une régression du graphe

> **Note pour les agents futurs, à ne pas contourner de travers.** Cet échec **ne signale aucun défaut de v112**. Il vient uniquement du passage v111 → v112 face à une **preuve figée** : le script dérive le nom de son CSV du graphe le plus récent et cherche donc `chronology-date-inventory-v112.csv`, qui n'existe pas. Le CSV versé décrit v111 et **doit** rester tel quel : il est la donnée probante du chantier PR #118. Ne le régénérez pas pour faire taire le rouge — vous détruiriez la mesure sans rien mesurer.
>
> **Le contrôle reste faisable dès aujourd'hui**, avec l'option que le script porte réellement :
>
> ```text
> python3 scripts/audit_chronology_dates.py --graph grc20-these-mael-rolland-v111.json --check
> ```
>
> — vérifié, `exit 0`, « 948 lignes identiques ». `--graph` désigne le graphe que le CSV décrit, et `--check` compare au CSV versé. Le script **ne porte pas** d'option `--source` : ses arguments sont `--graph`, `--csv`, `--check` et `--aujourdhui`. La correction de fond — ancrer le nom du CSV sur un graphe déclaré plutôt que sur « le plus récent » — reste un chantier distinct.

**Vérifié** : `.github/workflows/check.yml` compte 8 étapes et **ce script n'y figure pas**. La CI ne rougit pas. Les cinq contrôles qui y sont, eux, passent.

### Vérification navigateur non faite — exception documentée

La charte exige une vérification navigateur pour tout changement de runtime, et `graphe.html` et `lecteur.html` sont modifiés. **Elle n'a pas pu être faite.**

- **Cause** : `node_modules/` est absent de l'arbre, `playwright` n'est pas résoluble, les CDN sont bloqués, et `playwright install` est interdit par la charte. La revue hostile s'est heurtée au même mur : le contrôle manque **des deux côtés**.
- **Pourquoi le risque est faible** : le diff runtime ne contient **que** des pointeurs de version — une constante de nom de fichier par fichier, rien d'autre. La cible existe, pèse 10,2 Mo et est du JSON valide.
- **Ce qui remplace le contrôle** : `node --check` sur les quatre `.mjs` modifiés, inspection intégrale du diff runtime (borné aux pointeurs, ligne à ligne), et les cinq validations de graphe vertes.

Exception **acceptée par l'auteur** le 2026-08-09, à condition qu'elle soit énoncée — ce qu'elle est ici et dans le corps de la PR #119.

### Détail technique de l'échec `--check`

`audit_chronology_dates.py --check` **échoue désormais**, et c'était prévu : il dérive le nom de son CSV du graphe le plus récent, donc il cherche `chronology-date-inventory-v112.csv`, absent. Ce comportement était **déclaré au § 10 de l'audit du chantier** avant même que v112 existe. Le CSV d'inventaire reste celui de v111 et le reste volontairement : il décrit v111, et le régénérer sur v112 mélangerait une mesure et une application dans la même PR. Le script n'est pas en CI, donc rien ne rougit. Contournement immédiat et vérifié : `--graph grc20-these-mael-rolland-v111.json --check` (exit 0). **Le fond à corriger est l'ancrage du nom de CSV sur « le graphe le plus récent » plutôt que sur un graphe déclaré** — chantier distinct, non ouvert ici.
