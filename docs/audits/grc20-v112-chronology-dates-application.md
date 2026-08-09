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

```
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

L'applicateur porte lui-même ce contrôle : il compare le résultat à la source **entité par entité, attribut par attribut, relation par relation, type par type**, et refuse d'écrire si le diff complet ne vaut pas exactement deux valeurs de `date` changées.

### Les `options` sont préservées — choix déclaré

Le dialecte du dépôt n'exprime qu'un couple `{type, value}`, alors que les deux attributs visés portent un `options.language` (`fr` et `en`), sémantiquement vide sur une date. Les **retirer** aurait été une modification que personne n'a arbitrée, et aurait fait mentir la promesse « exactement deux valeurs changées ». L'applicateur réécrit donc la seule clé `value`. **Purger les `options.language` des dates est un chantier distinct**, non ouvert ici.

---

## 3. Ce que cette version refuse de faire

- **Aucun `duplicateOf`, aucun `reviewStatus`, aucune fusion.** La fiche `0d81bba0` a très probablement une jumelle, `06ac37fc`, qui porte déjà la bonne date. Marquer le doublon désignerait une canonique — or **`0d81bba0`, la fiche corrigée, a un degré de 24 contre 22** pour `06ac37fc` : la fiche fausse est la **mieux reliée**. C'est le piège **C5** de `grc20-dedup-events-audit-v1.md`, et le motif même pour lequel l'auteur refuse par ailleurs la fusion Mining pools. Corriger une date n'autorise pas à trancher une identité. L'applicateur refuse explicitement toute op portant ces deux clés.
- **Aucun nœud créé, aucune SourceQuote, aucun retypage, aucun renommage.**
- **Aucune autre date touchée** — ni les 28 valeurs ambiguës, ni les 86 sans source déclarée.

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

```
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

Aucune n'est refermée par cette version, et aucune ne doit être réputée l'être :

- **le doublon probable BitcoinTalk** (`0d81bba0` / `06ac37fc`) — dette entière, canonique non désignée ;
- **la grappe Mining pools à cinq fiches**, traversant les types, et les 3 fiches `duplicate-pending-merge` depuis v105 ;
- **`120e6fa2`** — perte wallet.dat 2010 contre vol Allinvain 2011 sur une même fiche, séparation arbitrée mais non exécutable en patch candidat ;
- **NewLibertyStandard** et les 6 autres `two_distinct_events_possible` ;
- **les 28 valeurs `NN/NN/AAAA` ambiguës** — convention JJ/MM confirmée, aucune réécriture ;
- **les 86 dates sans `dateSource`**, et les 37 renvois vers des figures absentes du dépôt ;
- **les 237 doubles descriptions** — chantier séparé ;
- **The DAO** — reste `non_verifie` ;
- **les 23 `doublon_probable`** et 13 `indetermine` du relevé d'identité ;
- **Casascius**, Istanbul, BitLaundry, l'écart 664/652 de la bibliographie.

---

## 8. Limite connue de cette version

`audit_chronology_dates.py --check` **échoue désormais**, et c'était prévu : il dérive le nom de son CSV du graphe le plus récent, donc il cherche `chronology-date-inventory-v112.csv`, absent. Ce comportement était **déclaré au § 10 de l'audit du chantier** avant même que v112 existe. Le CSV d'inventaire reste celui de v111 et le reste volontairement : il décrit v111, et le régénérer sur v112 mélangerait une mesure et une application dans la même PR. Le script n'est pas en CI, donc rien ne rougit. **La ligne à corriger est un `--source` déclaré plutôt qu'un « graphe le plus récent »** — chantier distinct, non ouvert ici.
