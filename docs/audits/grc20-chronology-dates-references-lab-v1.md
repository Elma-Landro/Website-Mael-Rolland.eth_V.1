# GRC-20 Chronology, Dates & References Verification Lab v1

**Date** : 2026-08-09
**Graphe audité** : `grc20-these-mael-rolland-v111.json` (2 293 entités, 20 207 relations)
**Branche** : `claude/file-upload-branch-check-jw4cng`
**Mode agent** : audit documentaire — **aucun graphe modifié, aucune v112, aucun patch appliqué, aucune fusion, aucun retypage, aucun runtime touché**
**Mécanismes rejouables** : `scripts/audit_chronology_dates.py` (`--csv`, `--check`) et `scripts/classify_date_evidence.py` (`--write`, `--check`). **Les trois autres CSV sont construits à la main et ne sont pas rejouables** — voir § 10.
**Patch candidat** : `patch_candidate_chronology_dates_v1.json` — 2 ops, **NON APPLIQUÉ**
**Arbitrages de l'auteur** : rendus le 2026-08-09, reportés au § 7 bis

**Données probantes** (à lire *avec* cet audit, jamais seules) :

| Fichier | Produit par |
|---|---|
| `data/chronology-date-inventory-v111.csv` | inventaire mécanique des 948 valeurs datées |
| `data/chronology-thesis-crosscheck-v111.csv` | recoupement de 260 dates avec le texte de la thèse |
| `data/chronology-external-verification-v111.csv` | vérification externe ciblée de 40 dates |
| `data/chronology-event-identity-debt-v111.csv` | 50 paires événementielles instruites |
| `data/chronology-reference-support-v111.csv` | adossement probatoire, 608 lignes, + 3 colonnes de régime de preuve (arbitrage 10) |
| `patch_candidate_chronology_dates_v1.json` | 2 corrections de `date`, **candidat, non appliqué** |

> Rappel de la charte (`agents/README.md`) : **un agent est un rôle de travail, pas une autorité scientifique.** Aucune décision scientifique n'est prise par l'agent. Les onze questions ★ du § 8 ont été posées à Maël Rolland et **ont toutes reçu réponse le 2026-08-09** (§ 7 bis) ; les points non marqués ★ restent ouverts.

---

## 1. Ce que ce chantier a cherché, et ce qu'il n'a pas cherché

Il a cherché à répondre à trois questions distinctes, souvent confondues :

1. **Combien de dates, sous quelles formes ?** — inventaire mécanique.
2. **D'où viennent-elles ?** — adossement probatoire. *Une date sourcée n'est pas une date juste.*
3. **Sont-elles justes ?** — recoupement avec la thèse, puis vérification externe.

Il n'a **pas** cherché à réparer de sa propre autorité. Un seul patch candidat est émis — **2 opérations, non appliqué** — et uniquement sur les deux points qui réunissent les deux conditions posées par l'auteur : *arbitrage rendu* **et** *preuve forte*. Le § 7 explique ce qui a été écarté, et pourquoi.

---

## 2. L'inventaire — et deux corrections de cadrage

**948 couples (entité × clé datée) sur 729 entités distinctes**, 24 clés. Recompté indépendamment du script avant versement.

Deux clés du périmètre **ne portent pas de date**, et le dire change la lecture de tout le reste :

- `dateSource` (95) porte une **référence bibliographique** (« Sedgwick 2018e », « Banque de France 2013, p. 4 ») ;
- `dateAuthority` (49) porte un **niveau de preuve** (`TIMELINE_FIGURE`, `AUTHOR_VERIFIED`, `EXTERNAL_VERIFICATION`).

Elles pèsent **144 des 158** valeurs non normalisables. Le taux réel de valeurs illisibles est donc **1,5 % (14/948)**, non 17 %. Elles sont conservées dans le CSV avec une note qui nomme leur nature, plutôt que retirées en silence : un inventaire qui ne correspond plus à son périmètre déclaré n'est plus une preuve.

`page_start` est **exclue explicitement** (constante nommée, pas omission) : c'est la page imprimée d'une section, pas une date. Une regex naïve sur « start » la ramasse et fabrique 37 fausses anomalies.

**Aucune date future. Aucune année hors plage** (min 1892, max 2024). **Aucun conflit intra-entité** sur les 26 couples `year`+`date` — résultat vérifié, non code mort : un graphe synthétique altéré fait bien remonter la détection.

Signalements : 30 valeurs `dmy_ambiguous=oui` — **28 sur `date` en forme `NN/NN/AAAA`, plus 2 sur `dateRange`** (famille `libre`), et non 30 valeurs à barres · 652 lignes où une même clé est déclarée tantôt `TEXT` tantôt `TIME` (cinq clés : `year`, `date`, `launchYear`, `dateStart`, `dateEnd`) · 17 descriptions citant une année différente de la date portée.

---

## 3. Le format des dates à barres : une convention JJ/MM établie, et une valeur aberrante

> **Cette section a été réécrite après revue hostile.** Sa première version concluait que « `date` mélange deux conventions de format ». **C'était une surinterprétation**, et la preuve du contraire était dans l'inventaire de ce chantier même, non exploitée. La conclusion erronée figure dans le message du commit `03c5921` ; elle est corrigée ici. Le compte-rendu de cette correction est au § 11.

Trois fiches consécutives de la même figure (« Chronologie n° 4 », chapitre III), crises n° 24, 25 et 26, portent des lectures qui ne s'accordent pas :

| Fiche | Valeur brute | Lecture vraie | Ordre |
|---|---|---|---|
| BIP-42 — inflation bug (`3952cb54`) | `01/04/2014` | 1er avril 2014 — poisson d'avril de Pieter Wuille, `Assigned: 2014-04-01` dans `bip-0042.mediawiki` | JJ/MM |
| CVE-2014-0160 Heartbleed (`ca278d21`) | `04/07/2014` | 7 avril 2014 | **MM/JJ** |
| BIP-66 — chain split (`d1961d60`) | `04/07/2015` | 4 juillet 2015 | JJ/MM |

Preuve pour les deux dernières : les alertes versionnées de `bitcoin-dot-org/Bitcoin.org` portent `date: 2014-04-11` pour la réponse à Heartbleed — une réponse ne peut pas précéder de trois mois un événement du 4 juillet — et `2015-07-04` pour BIP-66.

**Mais le graphe tranche lui-même la question, et il fallait le lui demander.** Sur les 54 valeurs de la famille « barres », **26 sont décidables sans aucune convention** : l'un des deux groupes dépasse 12, donc l'ordre est établi mécaniquement. Recomptées :

```
26 valeurs décidables  →  JJ/MM : 26     MM/JJ : 0
```

Et elles sont substantiellement justes — `17/06/2016` = attaque de The DAO, `15/08/2010` = CVE-2010-5139, `30/07/2015` = Frontier.

**Bilan : 28 lectures JJ/MM établies (26 décidables + BIP-42 + BIP-66) contre 1 lecture MM/JJ (Heartbleed).** Deux explications restent compatibles avec la preuve :

- **(a)** le graphe pratique deux conventions ;
- **(b)** **une seule cellule est fausse** dans la figure « Chronologie n° 4 ».

**(b) est nettement plus parcimonieux**, et c'est le mode de défaillance que ce chantier documente par ailleurs : le § 5 établit que la thèse se trompe et se contredit à l'intérieur de ses propres chronologies. « Deux conventions dans trois lignes consécutives d'une même figure, faite par une seule main » n'est attesté nulle part.

Conséquences, corrigées :

- le lot à arbitrer est de **28 valeurs ambiguës**, non de 54 : les 26 décidables sont déjà normalisées par le script, sans convention et sans arbitrage ;
- le refus de l'inventaire de deviner un ordre jour/mois reste justifié — mais comme **prudence de méthode**, pas parce qu'une seconde convention serait établie ;
- la question à trancher n'est pas « fixer une convention fiche par fiche » mais **« confirmer JJ/MM et arbitrer la seule fiche `ca278d21` »**.

Ce qui n'a **pas** été fait et trancherait sans doute : croiser les 28 ambiguës avec leur `dateSource` et leur `crisisNumber`, pour voir si elles se concentrent sur une figure ou se dispersent.

---

## 4. L'adossement : 36 % des dates événementielles ne **déclarent** aucune source

> **Titre corrigé après revue hostile.** Il disait « ne reposent sur rien ». C'est plus fort que ce que la donnée porte, et le CSV frère le contredit — voir l'encadré ci-dessous.

Sur 239 dates événementielles : **81 `adosse_fort` (34 %) · 72 `adosse_faible` (30 %) · 86 `non_adosse` (36 %)**.

**`non_adosse` veut dire « le graphe ne déclare pas de source », pas « la date ne repose sur rien ».** Croisées avec le recoupement thèse, les 86 se répartissent ainsi :

| Statut dans le recoupement thèse | n |
|---|---:|
| `figure_non_verifiable_dans_le_MD` | 24 |
| `absent_du_texte` | 21 |
| **`accord`** | **16** |
| (absent du recoupement) | 11 |
| **`accord_granularite_differente`** | **10** |
| `desaccord_these_probablement_fausse` | 2 |
| `desaccord_non_arbitrable` | 2 |

**26 des 86 sont confirmées mot pour mot par le texte de la thèse** — elles ne sont pas « sans fondement », elles sont *non déclarées*. La distinction change la nature de la question posée au § 8, point 22.

**Aucune `dateSource` du graphe ne contient d'URL** — 0 sur 95.

Le « fort » est plus fragile qu'il n'y paraît, et trois réserves le disent :

- les 28 renvois « Thèse — Chronologie (figure) Chapitre I.2 » et les 9 « Chronologie 2 (p.88) » pointent vers des **images absentes du dépôt** : `assets/MD/media/` n'existe pas, et aucun libellé « Chronologie 2 » ne figure dans le Markdown. Le pointeur résout ; la source ne se lit pas ;
- les 11 `AUTHOR_VERIFIED` citent une « Chronologie des HF d'Ethereum V1 » qui, **de son propre libellé**, n'est ni publiée, ni mobilisée dans la thèse, ni versée au dépôt : non consultable par un tiers ;
- l'adossement est déclaré sur la foi du pointeur, non sur lecture de la source.

**Correction d'une affirmation héritée de v97.** « `dateAuthority` est utilisé par 37 entités, toutes `TIMELINE_FIGURE` » était vrai en v97 et est **faux en v111** : 37 `TIMELINE_FIGURE`, 11 `AUTHOR_VERIFIED`, 1 `EXTERNAL_VERIFICATION`. Le nombre 37 survit exactement, mais comme *sous-ensemble* — ce qui rend l'ancienne formule trompeuse plutôt que simplement périmée. Un audit qui la reprendrait conclurait que le graphe n'a qu'un régime de preuve.

Côté bibliographie, les 369 `Reference` datées confrontées à `07_bibliographie.md` donnent **351 accords (95,1 %)**, 13 non-résolutions, 4 résolutions ambiguës, 1 désaccord d'année. Une non-résolution **n'est pas une erreur** : elle ne dit pas si l'entrée manque au Markdown (conversion incomplète du PDF) ou si la fiche est mal formée.

---

## 5. Le recoupement avec la thèse : trois contradictions internes au texte

> **Titre corrigé après revue hostile.** Il disait « la thèse se contredit plus souvent que le graphe ». Le CSV donne **4** `desaccord_graphe_probablement_faux` contre **3** contradictions internes au texte (sur 5 `desaccord_these_probablement_fausse`). Le titre inversait le rapport que le corps établit.

260 entités confrontées au texte, **222 citations verbatim** extraites programmatiquement puis revérifiées à la ligne indiquée.

**51 lignes (19,6 %) ne reposent que sur une figure de chronologie** — ni confirmation ni réfutation. Nuance qui compte : l'étiquette `TIMELINE_FIGURE` n'est pas synonyme de « invérifiable ». Sur les 37 fiches qui la portent, **19 sont en réalité reprises par le texte courant**.

Sur les 5 cas où le désaccord penche contre la thèse, **trois sont des contradictions internes à la thèse** :

| Objet | Le texte dit | Ailleurs dans le même texte | Le graphe |
|---|---|---|---|
| Frontier | 20 juillet 2015 (ch. I l.399, l.443) | 30 juillet 2015 (ch. III l.529 ; annexes l.337, l.569) | 30/07 — suit la majorité |
| Bitcoin-QT 0.1 | 9 janvier 2009 (ch. I l.269, l.305) | février 2009 (ch. III l.61) | 2009-01-09 |
| Bitcointalk | « janvier 2009 » (ch. I l.113) | note 12 (l.483) : remplace un forum « lancé en mai 2009 » — janvier devient impossible | 2009-11-22, cohérent avec la note |

**Aucun fichier de `assets/MD/` n'a été modifié.** Une erreur repérée dans la thèse est signalée, jamais corrigée : ce sont des documents archivistiques.

---

## 6. Les doublons ont une cause, et elle est mécanique

259 entités du périmètre événementiel, 881 paires candidates, **50 instruites en 31 familles** : 23 `doublon_probable`, 13 `indetermine`, 9 `homonymie_non_doublon`, 5 `two_distinct_events_possible`.

**Une cause partielle, et seulement partielle.**

> **Corrigé après revue hostile.** La première version affirmait que « 8 des 9 fiches "Chronologie 2 (p.88)" ont une jumelle **parmi les 28** "Chronologie (figure) Chapitre I.2" », et concluait à une **origine unique**. Recompté : c'est faux. La formule erronée figure aussi dans le message du commit `03c5921`.

**8 des 9 fiches** portant `dateSource = "Thèse — Chronologie 2 (p.88)"` ont bien une jumelle. Mais **4 seulement l'ont dans la cohorte des 28** :

| Fiche « Chronologie 2 (p.88) » | Jumelle | `dateSource` de la jumelle | Dans les 28 ? |
|---|---|---|---|
| `0d81bba0` BitcoinTalk | `06ac37fc` | Chronologie (figure) Chap. I.2 | oui |
| `5b8c5959` soft fork 2010 | `714f6de9` | Chronologie (figure) Chap. I.2 | oui |
| `4f7fd6dc` limite de bloc | `69aa91b1` | Chronologie (figure) Chap. I.2 | oui |
| `a494e3af` processus BIP | `008274f2` | Chronologie (figure) Chap. I.2 | oui |
| `45cd642a` halving | `3f908f24` | *(aucun)* | non |
| `db598117` Chypre | `a2202dfd` | *(aucun)* | non |
| `6c9b59cc` Fondation Bitcoin | `f9f289de` | `Rauchs 2016, p. 12` | non |
| `70d79dda` Genesis Block | `c8b77447` | *(aucun)* | non |

**Au moins trois origines distinctes**, donc, et non une. Le mécanisme « deux chronologies ingérées séparément » explique **4 paires**, pas 8 : c'est un lot réel et instruisible en bloc, mais il ne rend pas compte du reste. L'origine des 4 autres n'est pas établie par ce chantier.

Corollaire à ne pas manquer : les « preuves les plus fortes » citées juste après (Mining pools ×3, halving, Chypre, BitPay) ne relèvent **pas** de ce mécanisme. La cause commune ne couvre pas les cas les mieux étayés.

Preuves les plus fortes : attribut `description` **strictement identique** (Mining pools ×3, halving, Chypre, BitPay).

**Aucune chaîne de `duplicateOf` en v111** : l'invariant posé après l'incident C4 tient. Le **piège C5 est en revanche confirmé** — la canonique `15864ab2` (degré 4) est moins reliée que la fiche `ee727747` (degré 7) qu'elle canonise. Le CSV reporte les degrés et **ne désigne aucune canonique**.

Depuis v105, **3 fiches seulement sur 259** portent `duplicateOf` + `reviewStatus = duplicate-pending-merge`, et **aucune fusion n'a eu lieu**. La dette déclarée par le graphe est très inférieure à la dette mesurée.

### Deux actes distincts, jamais forcés en contradiction

Sept cas au total sont classés `two_distinct_events_possible` (5 côté identité, 3 côté vérification externe, 2 côté thèse — recoupements inclus). Le prototype reste **NewLibertyStandard**, et la thèse elle-même l'établit : la note 75 (ch. I l.609) date du **12 octobre 2009** le premier échange contre monnaie nationale (Malmi, 5 050 BTC pour 5,02 $), la note 78 (l.615) date de **février 2010** la modélisation du prix. Le graphe porte `2009-10-05` (publication du taux) et `2010-02` (modèle de prix) : **la date du 12 octobre n'est portée par aucune fiche**, et la fiche `66a59145` s'intitule « Premier échange BTC/$ » tout en portant la date d'une publication de taux.

Les autres : Frontier Thawing (annonce 04/08/2015 vs activation au bloc 200 000, 07/09/2015), BIP-148 (rédaction 12/03/2017 vs activation 01/08/2017), Ethereum Classic (dépôt GitHub 10/07/2016 vs fork 20/07/2016), soft fork du 28/07/2010 vs CVE-2010-5139 du 15/08/2010, WikiLeaks (annonce déc. 2010 vs adoption), Bitcoin-Qt.

---

## 7. Pourquoi ce chantier n'émet aucun patch candidat

Trois raisons, dans l'ordre de force :

1. **Le § 3 laisse une valeur aberrante non expliquée.** Un patch de normalisation des valeurs `NN/NN/AAAA` aurait été le livrable naturel de ce chantier. Les 26 décidables ne demandent rien ; les 28 ambiguës suivent très probablement la convention JJ/MM établie par les 26 — mais `ca278d21` (Heartbleed) y échappe, et tant que la cause de cette échappée n'est pas tranchée (cellule fausse de la figure, ou seconde convention), une passe globale graverait un arbitrage que personne n'a pris.
2. **Presque chaque correction est intriquée à une décision d'identité.** Corriger l'année de `0d81bba0` (BitcoinTalk) sans décider de la fusion avec `06ac37fc` produit deux fiches justes et redondantes. Corriger l'année de `adc1a4d0` (Selgin) en 2014 produit un **doublon exact** de `3d76ab7f` — même titre, même année. Le « il n'y a qu'à corriger la date » est faux dans les deux cas.
3. **La charte réserve à l'auteur** les fusions, créations, retypages et tout ce qui engrave une affirmation sur une personne.

Ce que le chantier livre à la place : cinq relevés, un mécanisme rejouable, et des questions posées au point où seule une décision reste.

---

## 7 bis. Arbitrages rendus par Maël Rolland — 2026-08-09

Les onze questions du § 8 marquées ★ ont été posées et **toutes ont reçu réponse**. Elles sont reportées ici *avant* la liste des points ouverts, parce qu'elles en referment une partie et en requalifient le reste. Les points du § 8 restent écrits tels quels : un point ouvert arbitré n'est pas effacé, il est daté.

| # | Question | Arbitrage | Effet dans ce chantier |
|---|---|---|---|
| 1 | Convention des 28 `NN/NN/AAAA` ambiguës | **JJ/MM confirmé** | Documenté. **Aucune réécriture** : confirmer une lecture n'est pas décider d'une normalisation |
| 2 | Heartbleed `ca278d21` | **Cellule fausse**, corriger vers `2014-04-07` ; ne pas préserver l'idée d'une seconde convention | **Op 1 du patch candidat** |
| 3 | BitcoinTalk `0d81bba0` | Coquille d'année **oui**, fusion probable, mais **pas de fusion automatique ici** — décision candidate + dette documentée | **Op 2 du patch candidat** (date seule). Aucun `duplicateOf` émis |
| 4 | Les 4 paires des deux chronologies | **Lot accepté**, à condition que chaque paire reste listée et justifiée individuellement ; pas de fusion silencieuse par appartenance au lot | Les 4 paires restent une ligne chacune dans le CSV d'identité |
| 5 | Les 3 fiches `duplicate-pending-merge` | **Ne pas fusionner.** La grappe réelle compte cinq fiches, la canonique est la moins reliée | Dette conservée, contradiction canonique/degré documentée, renvoi au chantier identité |
| 6 | Selgin | **Fiches distinctes pour l'instant** ; aucun des trois appariements n'est gravé | Les trois hypothèses consignées comme dette |
| 7 | Les 7 `two_distinct_events_possible` | **Dédoubler en principe**, au cas par cas selon preuve fine — mais **documenter seulement ici** | Aucune op ; preuve fine hors d'atteinte (réseau) |
| 8 | `120e6fa2` Allinvain / wallet.dat | **Séparer en deux fiches candidates** | Spécifié au § 8 point 11 ; **aucune op** — le contrat interdit `CREATE_ENTITY` avec `entityId` pré-assigné |
| 9 | Les 237 doubles descriptions | **Chantier de résorption, mais séparé** | Hors de ce chantier. Priorité fixée : inventaire, typologie, politique de choix, puis arbitrage |
| 10 | Les 86 dates sans source déclarée | **Exiger un `dateSource`** pour les dates prétendant à une autorité, en distinguant quatre régimes de preuve | **Implémenté** — voir ci-dessous |
| 11 | Figures et chronologie des HF | **Verser les sources**, ou marquer les dates comme insuffisamment sourcées | Point ouvert, hors périmètre d'un audit |

### Ce que l'arbitrage 10 a produit

`scripts/classify_date_evidence.py` classe les 239 dates événementielles selon les quatre régimes demandés et écrit trois colonnes dans le CSV d'adossement (`regime_de_preuve`, `confirme_par_these`, `motif_regime`). Il porte `--check` pour la CI.

| Régime | n |
|---|---:|
| `source_primaire` | 4 |
| `these_verbatim` | 90 |
| `approximatif` | 35 |
| `infere` | 110 |

**92 dates au total sont confirmées par la thèse** (dont 2 qui relèvent d'un régime supérieur) ; **26 d'entre elles sont dans les 86 `non_adosse`** — non déclarées, mais pas sans fondement.

Deux choix de méthode sont déclarés dans le script plutôt que cachés :

- **La précédence** `source_primaire > these_verbatim > approximatif > infere` est un choix, non une évidence : une source externe l'emporte parce qu'elle est vérifiable par un tiers. Mais l'arbitrage exige que le statut « confirmé par la thèse » reste visible même quand il n'est pas retenu — d'où la colonne `confirme_par_these`, qui ne disparaît jamais derrière la précédence.
- **`these_verbatim` est explicitement provisoire.** La thèse est ici juge et partie, et ce chantier a montré qu'elle se contredit parfois elle-même (§ 5). Le champ `motif_regime` le dit sur chaque ligne concernée.

`infere` **n'est pas un reproche** : c'est l'aveu qu'on ne sait pas d'où vient la date. Et un régime ne dit rien de la véracité — une date `these_verbatim` peut être fausse ; Frontier, Bitcoin-QT et le split de chaîne le sont probablement.

### Défaut d'interopérabilité corrigé au passage

`chronology-external-verification-v111.csv` portait des `entity_id` **tronqués à 8 caractères**, là où les quatre autres CSV portent l'identifiant complet. La jointure retournait silencieusement zéro — c'est ce qui a fait afficher `source_primaire = 0` au premier essai. Les 40 préfixes ont été vérifiés comme résolvant chacun vers **exactement une** entité (et le graphe entier ne compte aucune collision de préfixe à 8 caractères) avant remplacement par la forme complète. Un identifiant tronqué dans une donnée probante est un piège : il casse les jointures sans erreur.

### Ce qui n'a délibérément pas été produit

Le patch candidat `patch_candidate_chronology_dates_v1.json` ne porte que **2 opérations**, et son bloc `skipped` motive cinq abstentions. La plus importante : **aucun `duplicateOf` n'est émis pour BitcoinTalk.** Assigner cet attribut désignerait une canonique, or `0d81bba0` — la fiche à l'année fausse — a un **degré de 24** contre **22** pour `06ac37fc`. C'est le piège C5, et c'est le motif même pour lequel l'arbitrage 5 refuse la fusion Mining pools. Corriger une date n'autorise pas à trancher une identité.

---

## 8. Points ouverts — à ne pas trancher

Reportés intégralement pour que ce document se suffise à lui-même. Les questions marquées **★** ont été posées directement à Maël dans le fil de discussion.

### Format et convention

1. **★ Les 28 valeurs `NN/NN/AAAA` ambiguës** (et non 54 : les 26 décidables sont déjà normalisées sans convention). Les 26 décidables donnent **JJ/MM 26 / MM/JJ 0**. La question est donc : confirmer JJ/MM pour les 28, et arbitrer séparément la seule fiche `ca278d21` (Heartbleed), dont la lecture MM/JJ est établie par une source primaire (§ 3).
2. **Les 5 clés à double type GRC-20** (`year`, `date`, `launchYear`, `dateStart`, `dateEnd`, déclarées tantôt `TEXT` tantôt `TIME`, 652 lignes) : harmoniser ou documenter l'hétérogénéité ?
3. **Les 14 valeurs en texte libre délibéré** (« fin 2013 — pression FinCEN », « 2017 surtout », « nov. 2013 – présent ») : bornage ou conservation comme expression ?

### Identité et doublons

4. **★ La cohorte des deux chronologies** : **4 paires**, non 8 (§ 6). Traitement en lot pour ces 4 ? Les 4 autres jumelles ont au moins trois origines distinctes et restent à instruire une par une.
5. **★ BitcoinTalk** (`0d81bba0` 2010-11-22 / `06ac37fc` 2009-11-22) : coquille d'année **et** doublon. Réfuté en externe par l'archive Nakamoto (« Date: November 22, 2009 », fil « Welcome to the new Bitcoin forum! »), et la fiche se contredit elle-même — sa propre description dit « novembre 2009 ».
6. **★ Les 4 fiches Selgin.** `adc1a4d0` porte le titre « Synthetic Commodity Money » avec l'année 2013 (degré 13) ; `3d76ab7f` porte **le même titre** avec 2014 (degré 6) ; `5680ab9e` porte « Quasi-Commodity Money », 2013 (degré 11). La bibliographie ne connaît que trois Selgin — 2014a, 2014b (Synthetic, JFS, juillet 2014) et 2013 (Quasi, SSRN, avril 2013) : **aucune entrée « Synthetic Commodity Money 2013 »**. L'appariement le plus parcimonieux est donc `adc1a4d0` ↔ `3d76ab7f`, mais **un troisième appariement n'a pas été testé** — que « Quasi- » et « Synthetic Commodity Money » soient deux titres d'un même texte SSRN renommé avant publication, auquel cas la paire serait `adc1a4d0` ↔ `5680ab9e`. Les trois fiches sont rattachées aux mêmes sections. **Ceci n'est donc pas un doublon établi mais un appariement à trancher** — et la fiche la mieux reliée porte l'année douteuse (piège C5). Détail : George Selgin est relié à `adc1a4d0` par `created` et aux trois autres par `authored`.
7. **Les 3 fiches `duplicate-pending-merge`** depuis v105, dont le couple Mining pools déjà consigné comme conflit de types dans `identity-debt-fr-en-v1.csv` : fusionner, et vers quelle fiche, la canonique désignée étant la moins reliée ?
8. **Les 23 `doublon_probable` et 13 `indetermine`** du relevé d'identité.
9. **★ Les 7 `two_distinct_events_possible`** : dédoubler, renommer, ou laisser.
10. **Les doubles modélisations sous deux types** (Genesis Block, Op_Return War, Silk Road en `InfrastructureEvent` **et** `CrisisEvent`) : couche voulue ? **Retypage réservé à l'auteur.**

### Contenu et véracité

11. **★ `120e6fa2`** — la fiche s'intitule « Perte 9000 BTC (premier utilisateur, 10 août 2010) », porte `date = 2010-08-10`, et son attribut `description` concorde. Mais **son enveloppe `description`, seule version affichée par le site**, décrit un autre fait : « Allinvain annonce le vol de 25 000 BTC depuis son portefeuille en juin 2011 ». Deux événements réels et distincts collés sur une fiche, la version visible étant la mauvaise. La thèse (note 73, l.605) attribue en outre ce vol à un mineur, le graphe à MtGox.
12. **★ Les 237 doubles descriptions** (§ 9).
13. **Pizzas** : graphe `2010-05-21`, thèse (l.609) « Le 22 mai 2010 ».
14. **Phase de maturation** : graphe `2013-01-01 → 2015-12-31`, thèse (l.285) « de novembre de 2013 à aujourd'hui ». Le graphe se contredit : son `Concept` jumeau porte « nov. 2013 – présent ».
15. **CVE-2018-17144** : `2018-09-01` est exact au mois et factice au jour. Signalement 17/09, correctif 18/09, divulgation 20/09 (4 sources primaires). Sur les `CrisisPhase` : `order=0` finit le 20/09 alors que `order=1` finit le 18/09. **Deux lectures se valent** — une incohérence d'ordonnancement, ou une phase-chapeau `order=0` (17→20) qui *contient* les phases 1 et 2 (17→18, 18→20). L'audit ne tranche pas ; les bornes réelles sont `9c3c6d95` 17→20, `143db183` 17→18, `73712fc1` 18→20, `896a139f` 20→25.
16. **Istanbul** : graphe `2019-12-08`, `ethereum/execution-specs` `2019-12-07`. Les 9 autres hard forks concordent exactement — **mais contre le même témoin unique**, la même source datant toute la série. Le CSV classe la ligne `indice_unique` et écrit « ne pas corriger sans une seconde source » : ce n'est pas un écart établi, c'est un écart constaté contre une seule autorité.
17. **BitLaundry** : trois valeurs divergentes — graphe `2010-09-01`, thèse « fin 2010 » (ch. I l.607, note 74), description « lancé en 2011 ». Le recoupement thèse classe `desaccord_non_arbitrable` et note que « septembre n'est pas "fin 2010" **sans être incompatible** » : le mot « incompatible » de la première version de cet audit dépassait son propre CSV. Aucune source externe atteignable.
18. **Split de chaîne** : ch. I l.267 dit « 15 mars 2011 », ch. III l.237 et la note 104 disent mars 2013. Le jour du graphe (15/03) n'est pas attesté non plus.
19. **Casascius** : la thèse l'attribue à Bobby Lee (l.359), le graphe à Mike Caldwell ; graphies divergentes (« Casacius », « Cascascius », « Casascius »). **Toute écriture ici engrave une affirmation sur une personne réelle** — décision d'auteur, sans exception.
20. **Audition Commission des Finances** : le nom porte « (2015) », l'attribut `date` porte `07/11/2014`.
21. **`adc1a4d0` Selgin** : année 2013 contre entrée bibliographique 2014b, mais voir le point 6 — ce n'est pas une année à corriger.

### Adossement

22. **★ Les 86 dates événementielles `non_adosse`** — c'est-à-dire **sans source déclarée**, non « sans fondement » : **26 des 86 sont confirmées verbatim par le texte de la thèse** (§ 4). Exiger un `dateSource` avant publication, ou accepter cette strate non déclarée ?
23. **Les 37 renvois vers des figures-images** : verser les figures, ou pointer les pages du PDF ?
24. **Les 11 hard forks `AUTHOR_VERIFIED`** : verser la chronologie citée, ou lui substituer une source publiée ?
25. **`94ce188e` Litecoin** : la date `2011-10-07` est corroborée par le bloc de genèse (`CreateGenesisBlock(1317972665, …)` = 2011-10-07T07:31:05Z) — **une seule source, la ligne reste `indice_unique`**. Son `dateSource` — « Vérification externe 02/08/2026 » — n'est ni une URL, ni un auteur, ni un support.
26. **Les 4 `resolution_ambigue` et 13 non-résolutions bibliographiques** : doter les fiches d'un `title` ?
27. **Coquilles de libellé** : le graphe écrit `Whitebbit1111` là où le Markdown écrit `WHITERABBIT1111` ; le Markdown écrit `KINDELBERGER` là où le graphe écrit `KINDLEBERGER`. Archives intouchées ou corrigées ?
28. **Écart bibliographique** : `07_bibliographie.md` annonce « Total : 652 entrées » et en porte 664.

---

## 9. Découverte annexe : 237 doubles descriptions, aucune identique

Hors périmètre initial, trouvée en vérifiant un signalement de l'inventaire, et versée ici parce qu'elle conditionne la lecture de toute date.

**237 entités portent à la fois l'enveloppe GRC-20 `description` et un attribut homonyme `attributes.description`. Aucune des 237 paires n'est identique.** Ces deux chiffres sont recomptables exactement et ont été reconfirmés par la revue hostile.

Les deux mesures de *degré* de divergence — 171 paires « très éloignées », 12 « années disjointes » — dépendent d'une métrique qui **n'était pas déclarée** dans la première version de cet audit ; la revue hostile, reconstruisant une autre métrique, a obtenu 220 et 13. Pour qu'elles soient falsifiables, voici la définition employée : `difflib.SequenceMatcher(None, enveloppe.lower(), attribut.lower()).ratio() < 0.35` pour la première, et pour la seconde l'absence d'intersection entre les millésimes extraits par `\b(19\d{2}|20[0-2]\d)\b` de chaque côté, chaque côté devant en contenir au moins un. **Ces deux chiffres sont indicatifs ; seuls 237 et 0 sont structurants.**

Le registre documente déjà la **collision de clé** (entrée `description`, `status: structural`, note explicite). Il ne documente pas la **divergence de contenu** — c'est la mesure neuve.

Qui fait quoi, vérifié dans le code :

| Fichier | Rôle |
|---|---|
| `lecteur.html:2575` | **lit** l'enveloppe (`e.description?.value`) |
| `graph-worker.mjs:271` (recherche) | **lit** l'enveloppe |
| `graphe.html:5021,5040` | **écrit** l'enveloppe (`Editor.addEntity` / `Editor.editEntity`) — chemin d'écriture, pas de lecture |
| `grc20-publish.mjs:172` puis boucle d'attributs (~207) | émet **les deux** |

**Aucun fichier du dépôt ne lit `attributes.description`** — recherché sous ses trois formes (`attributes.description`, `attributes['description']`, `attrs.description`), zéro occurrence. La conclusion « invisibles sur le site » est donc plus forte que prudente.

Que l'éditeur de `graphe.html` ne connaisse que l'enveloppe aggrave le cas plutôt qu'il ne l'atténue : toute édition faite depuis le site fait diverger un peu plus l'attribut homonyme, qui n'est jamais mis à jour.

`grc20-publish.mjs` émet l'enveloppe via `SYSTEM_PROPERTY_IDS.description`, **puis** parcourt `entity.attributes` **sans liste d'exclusion** : un second triplet serait bien émis. **Nuance à porter au dossier** : son champ `attribute` est la chaîne brute `'description'`, non l'identifiant système `LA1DqP5v6QAdsgLPqqNH`. Ce n'est donc pas une collision sur une même propriété, mais le défaut générique des clés non mappées — celui-là même que le registre existe pour traiter. Le risque n'est pas propre à `description`.

Le cas `120e6fa2` (§ 8, point 11) montre que ce n'est pas qu'une redondance : les deux versions peuvent décrire deux faits différents, et la version visible peut être la fausse.

**Aucune action prise.** Le runtime n'a pas été touché ; la publication n'est pas de mon ressort.

---

## 10. Limites de ce chantier — à lire avant de s'appuyer dessus

- **Le réseau restreint la vérification externe.** Seuls `github.com`, `raw.githubusercontent.com` et `gitlab.com` sont joignables. NVD, `bitcoincore.org`, `en.bitcoin.it`, `blog.ethereum.org`, Wikipédia, CoinDesk et l'Internet Archive sont bloqués. D'où 24 `indice_unique` pour 4 `confirme` : c'est une contrainte d'accès, pas un défaut de recoupement.
- **La date de l'attaque The DAO reste `non_verifie`** — la plus célèbre de la thèse. Elle est connue de mémoire ; une date de mémoire ne s'inscrit pas. C'est la règle qui a fonctionné, pas une lacune à combler par complaisance.
- **Un piège de source documenté** : `ethereum-org-website/.../ethereum-forks/index.md` ne contient **aucune date** (seulement des balises `<NetworkUpgradeSummary />`). Une première lecture en a rendu un tableau de dates plausible et faux, détecté en redemandant le verbatim. **Ce fichier ne doit pas être cité comme source de dates.**
- **L'adossement n'est pas la véracité.** Le volet probatoire mesure d'où vient une date, jamais si elle est juste.
- **Les figures de chronologie n'ont pas été lues.** Elles sont des images absentes du dépôt ; les 51 lignes qui en dépendent restent indécidées, et ce n'est pas un défaut du graphe.
- **Les non-résolutions bibliographiques ne sont pas des erreurs.** Par construction, elles ne disent pas si l'entrée manque au Markdown ou si la fiche est mal formée.
- **Trois des cinq CSV n'ont aucun générateur.** La rejouabilité se lit à trois niveaux, et les confondre serait trompeur :
  - `chronology-date-inventory-v111.csv` est **intégralement généré** par `audit_chronology_dates.py` et contrôlé par `--check` ;
  - `chronology-reference-support-v111.csv` est **construit à la main**, mais ses trois colonnes de régime de preuve (`regime_de_preuve`, `confirme_par_these`, `motif_regime`) sont générées et contrôlées par `classify_date_evidence.py --check` ;
  - `chronology-thesis-crosscheck-v111.csv`, `chronology-external-verification-v111.csv` et `chronology-event-identity-debt-v111.csv` — les trois relevés qui portent les conclusions les plus lourdes — sont **entièrement construits à la main : ni rejouables, ni contrôlables par `--check`**.
- **Le périmètre événementiel (259 entités) et les 881 paires candidates ne sont définis nulle part**, donc non reconstructibles : la revue hostile a essayé et n'est arrivée ni à 259 ni à la règle d'appariement. Le critère qui a écarté 831 des 881 paires n'est pas déclaré. **Les deux chiffres d'ouverture du § 6 sont à prendre comme des ordres de grandeur, pas comme des mesures vérifiables.**
- **`--check` deviendra faux en silence à la v112.** `audit_chronology_dates.py` dérive le nom de son CSV du graphe le plus récent, non d'un `source_graph` déclaré. Le jour où une v112 existe, `--check` cherchera `chronology-date-inventory-v112.csv`, absent, et sortira 1. Le script n'est pas en CI, donc rien ne rougira — mais la mention « vérifiable par `--check` » du `data/README.md` cessera d'être vraie.
- **`SCRIPTS_ENUMERANTS` offre une garantie plus faible que `EXCLUSIONS_READ_BY`.** L'exclusion se fait en bloc, par nom de fichier ; l'ancien mécanisme exigeait une vérification clé par clé. Rien n'atteste automatiquement qu'un script inscrit là est réellement énumérant. Effet de bord : `_meta.conventions` change, donc toute autre branche vivante qui régénère le registre divergera au merge.


---

## 11. Revue hostile — ce qu'elle a cassé

Conformément à la charte, ce chantier a été soumis à la compétence `grc20-reviewer-hostile` **avant toute PR**. Verdict : **RÉSERVES, dont deux bloquantes.** Les deux prises étaient justes, et elles portaient sur les affirmations les plus visibles de l'audit — celles-là mêmes qui avaient déjà été posées en arbitrage. Elles sont corrigées dans les §§ 3, 4, 5, 6 et 8 ci-dessus, et **subsistent, fausses, dans les messages des commits `03c5921` et `91a7c25`** : un message de commit est une archive, il ne se réécrit pas.

| Prise | Ce que l'audit disait | Ce que le recompte donne |
|---|---|---|
| **Bloquante** | « `date` mélange deux conventions », « 54 valeurs à arbitrer » | 26 valeurs décidables → **JJ/MM 26, MM/JJ 0**. Convention établie, **une** valeur aberrante. 28 à arbitrer, pas 54 |
| **Bloquante** | « 8 des 9 ont une jumelle parmi les 28 », « origine unique » | 8 ont une jumelle, **4 seulement dans les 28**. Au moins **trois** origines |
| Réserve | « 36 % ne reposent sur rien » | **26 des 86** sont confirmées verbatim par la thèse |
| Réserve | « la thèse se contredit plus souvent que le graphe » | 3 contradictions internes contre 4 `desaccord_graphe` |
| Réserve | « 171 similarité < 0,35 » | métrique non déclarée, donc non falsifiable ; désormais définie au § 9 |

La leçon est précise et vaut au-delà de ce chantier : **la preuve qui a renversé la conclusion principale était déjà dans le CSV du chantier**. Les 26 valeurs décidables étaient là, normalisées par mon propre script, dans la colonne `normalized_iso`. Je n'avais pas interrogé ma propre donnée avant de conclure — le défaut exact que cet audit reproche par ailleurs à `doublons-verifies.csv`.

**La revue s'est aussi trompée, et l'a retiré elle-même** : elle a d'abord accusé le chantier d'avoir contaminé le registre des propriétés, sur un état du dépôt déjà dépassé — le correctif (`SCRIPTS_ENUMERANTS`, commit `e3c4a46`) existait avant qu'elle ne conclue. Elle a également abandonné une objection sur le doublon Selgin après vérification bibliographique, tout en laissant une réserve réelle qui est reprise au § 8, point 6. Réviser la revue fait partie de la revue.

**Ce qu'elle n'a pas pu attaquer**, et qui reste donc non contre-vérifié : les 28 URL de la vérification externe (même réseau restreint), les 831 paires écartées, les figures de chronologie absentes du dépôt, et l'identité bibliographique réelle des deux textes de Selgin.
