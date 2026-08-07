# Bibliographie Reconciliation Lab v1 — quatre dettes instruites jusqu'à la décision, aucune prise

**Date** : 2026-08-07
**Graphe** : `grc20-these-mael-rolland-v110.json` (**inchangé** par ce chantier)
**Branche** : `claude/file-upload-branch-check-jw4cng`
**Mode agent** : A (comparatif/instruction) — **aucune application**, aucun nœud créé, aucune fusion, aucun retypage effectué
**Données** : `docs/audits/data/bibliographie-18-fiches-douteuses-v1.csv` (22 lignes) · `docs/audits/data/bibliographie-doublons-familles-v1.csv` (89 familles) · `docs/audits/data/bibliographie-entrees-sans-noeud-v1.csv` (60 entrées) · `docs/audits/data/bibliographie-parasites-et-jamais-cites-v1.csv` (11 lignes)
**Patchs candidats produits** (racine, **NON APPLIQUÉS**, `_meta.policy` = « CANDIDATE — NOT APPLIED — AUTHOR ARBITRATION REQUIRED ») : `patch_candidate_bibliographie_retypes_v1.json` · `patch_candidate_bibliographie_duplicates_v1.json` · `patch_candidate_bibliographie_missing_nodes_v1.json`
**Prédécesseur** : `grc20-bibliographie-reconciliation-v1.md` (2026-08-06, PR #108, avec son addendum du 2026-08-07)

> Rappel de la charte : un agent est un rôle de travail, pas une autorité scientifique. Ce document **instruit** chaque dette bibliographique jusqu'au point où il ne reste qu'une décision d'auteur à prendre — et s'arrête là. Toute affirmation corrective ci-dessous cite le CSV qui la porte et est re-vérifiable contre `grc20-these-mael-rolland-v110.json` et `assets/MD/07_bibliographie.md`.

---

## 1. Le problème — l'état bibliographique après la PR #108

La PR #108 a converti la bibliographie du PDF (652 entrées, portées à **664** par l'addendum qui a scindé 12 entrées concaténées par l'extraction), réconcilié les 770 nœuds bibliographiques de v109, et appliqué dans v110 le seul lot indiscutable : **21 retypages** de fiches d'auteur sans millésime `Reference` → `Person` plus une coquille de nom (Danezis), via `patch_18_bibliography_fixes.json`. Tout le reste a été explicitement laissé en dette, avec quatre chantiers d'instruction ouverts :

| Dette | Volume (audit source) | Diagnostic produit |
|---|---|---|
| Fiches d'auteur douteuses exclues du patch_18 | 22 fiches | `bibliographie-18-fiches-douteuses-v1.csv` |
| Familles de doublons (≥ 2 nœuds, même entrée PDF) | 89 familles, 99 nœuds excédentaires | `bibliographie-doublons-familles-v1.csv` |
| Entrées du PDF sans aucun nœud | 60 entrées | `bibliographie-entrees-sans-noeud-v1.csv` |
| Nœuds datés « jamais cités » (zéro `cited in`) | 11 nœuds | `bibliographie-parasites-et-jamais-cites-v1.csv` |

Ce chantier est l'intégrateur de ces quatre diagnostics : il en fait la synthèse, consigne les points où ils **corrigent** l'audit source, matérialise en trois patchs candidats tout ce qui est mécanisable sans décision d'auteur — et liste au § 8 chaque décision qui reste, avec sa donnée d'appui. **Il n'en prend aucune.** Le graphe v110, ses cartes et son runtime sont identiques avant et après ce chantier (`scripts/check_graph_integrity.py` vert, aucun fichier existant modifié).

## 2. Diagnostic 1 — les 22 fiches douteuses

Répartition des 22 lignes du CSV (recomptée) : **2 `retyper`** (sûrs), **4 `renommer-puis-retyper`**, **14 `arbitrage-auteur`**, **2 `laisser-reference`**, **0 `supprimer`**.

**Prises qui corrigent l'audit source** (données re-vérifiables, CSV lignes « Shinobi (pseudonyme) » et « Laura DeNardis ») :

- La raison d'exclusion du patch_18 (« prénom contredit par le PDF ou sans entrée d'auteur ») est **factuellement fausse pour 2 des 22 fiches**. « Shinobi (pseudonyme) » (`b332ace807b84fe4ab2373b8dc8f4856`) : l'entrée d'auteur SHINOBI 2022 existe au PDF et un pseudonyme n'a pas de prénom à contredire. « Laura DeNardis » (`5fc4278b78704f6c92c3744e2654518a`) : l'entrée DENARDIS Laura et MUSIANI Francesca 2014 confirme exactement patronyme et prénom. Ces deux retypages sont au patch candidat.
- **4 fiches portent un prénom inventé** que l'unique entrée d'auteur du PDF contredit : Audrey → **Adli** Takkal Bataille, Gregor → **Andreas** Loibl, Guillaume → **Gérard** Dréan, Jérôme → **Jacques** Favier. Aucun homonyme `Person` dans v110 (vérifié). Le renommage-puis-retypage est au patch candidat.

Les 14 `arbitrage-auteur` se décomposent en sous-familles distinctes (le § 8 les décline en décisions) : 7 identités notoires **sans entrée d'auteur admissible au PDF** (Desan, Keynes, Stiglitz, Robbins, Croman, Gandal, Macron — retyper sur notoriété serait sortir de la règle de preuve du patch_18) ; 1 attesté par le corps mais pas par la bibliographie (Tyler Winklevoss) ; 3 conflations ou doublons de personnes réelles (Florence Dufy, Marco Corallo, Martti Malmi (Sirius)) ; 1 pseudonyme soudé à un autre par une relation `authored` erronée (« "The Madhatter" » → GameKyuubi) ; 1 prénom faux à preuve hors bibliographie (Alain → Jérôme Maucourant) ; 1 équivalence pseudonyme/patronyme non attestée avec ancrage de chapitre incohérent (Felix Albert, cité chap. III, `cited in` chap. I). Les 2 `laisser-reference` sont des fiches à **deux auteurs** (De Boyer des Roches et Rosales ; Desmedt et Lakomski-Laguerre) : aucun retypage possible, chacune double par ailleurs un nœud daté existant (fusions à l'arbitrage).

## 3. Diagnostic 2 — les 89 familles de doublons

Classes recomptées : **71 `fusion-sure`**, **6 `doublon-probable`**, **12 `homonymie-risque`**. Les 71 familles sûres comptent **78 membres non canoniques** (64 familles à 2 membres, 7 à 3 membres).

**La distinction qui structure tout ce diagnostic : cible de fusion ≠ libellé final.** La colonne `canonique_propose` du CSV désigne le membre de plus haut **degré** dans v110 (le meilleur receveur de relations si l'on fusionne). L'audit source (§ 2.d) propose, lui, une « forme à garder d'après le PDF » — un **libellé**. Recomptage exact par croisement des deux fichiers : sur les 71 familles fusion-sure, **41** ont un canonique par degré dont le nom **n'est pas** la forme à garder de l'audit (44 en incluant les doublon-probable dotés d'un canonique). L'estimation de travail du chantier (~26) était donc en dessous du compte réel. Exemples : famille 1, canonique « Aglietta & Orleans 2002 » (deg=13) vs forme à garder « Aglietta & Orléan 2002 — Violence et confiance » ; famille 4, « Akrich 1989 » (deg=15) vs « Akrich 1989 — Construction d'un système socio-technique ». Le motif est systématique : le nœud le plus **connecté** est souvent le plus **anciennement importé**, au libellé court, tandis que l'audit préfère le libellé titré. Les deux questions sont non tranchées et **séparables** : on peut fusionner vers le nœud le plus connecté puis le renommer. Le patch candidat ne marque que la cible ; il ne propose aucun `SET_NAME`.

Réserves reconduites telles quelles : les 6 doublon-probable ont une convergence forte mais un titre ou une lettre d'édition à confirmer (ECB 2012, Polanyi 1944/2011, Pouliot 2018, Servet & Dufrêne 2021, Tirole 2017, Wray 2010) ; les 12 homonymie-risque recouvrent de **vraies paires de références distinctes** du PDF (Blanc 1998a/b et 2009a/b, Buterin 2013a/2013d, 2013c, 2014j, 2017a/b/c, Lee 2011, Möser 2015, Orléan 1998, Selgin 2013/2014b, Walch 2017a/b ×2) — fusionner là reviendrait à écraser une référence réelle.

## 4. Diagnostic 3 — les 60 entrées du PDF sans nœud

Décompte du CSV (revérifié ligne à ligne) : **6 faux absents** (`vraiment_absente=non`), 54 vraiment absentes dont **38** cumulant `entree-complete` + `risque_ajout_inutile=faible` (candidates à création), **7** à risque **élevé** (jamais citées dans le corps — un nœud serait un orphelin), **6** à risque moyen (entrée complète), **2** entrées partielles, **1** douteuse. 6+38+7+6+2+1 = 60.

**Prise qui corrige l'audit source** : l'audit § 2.b présentait les 60 entrées comme « sans aucun nœud ». Le diagnostic montre que **6 en ont déjà un** — ce sont des artefacts de clé, pas des absences : BUTERIN 2013D (l'œuvre visée a le nœud `12c586ca…`, l'audit l'avait appariée à 2013a), FRIEDMAN 1999 entrée anonyme (doublon interne du PDF, même URL YouTube), LEIGH STAR & RUHLEDER 2010 (doublon interne du PDF), MANGOLTE 2013B (entrées 2013a/2013b strictement identiques au PDF), NAKAMOTO 2009B (même annonce P2P Foundation que 2009a, URL miroir), POPPER 2016B (le nœud étiqueté « 2016a » porte en réalité le titre de l'article 2016b). Créer ces six nœuds fabriquerait des doublons ; ils sont exclus du patch candidat avec ces raisons.

Autre donnée notable : les « jamais citées » du PDF existent aussi dans ce sens-ci — 7 entrées complètes du PDF (Koning 2013, Nakamoto 2010d/2010e, Orléan 2002, Song 2018a/2018b, Tual 2016c) n'ont **aucun appel dans le corps** : les créer peuplerait le graphe d'orphelins. Exclues aussi.

## 5. Diagnostic 4 — les 11 nœuds datés « jamais cités »

Verdict du CSV : **11/11 `legitime-confirmee`** — aucun parasite. C'est la confirmation, nœud par nœud avec ligne de bibliographie et ligne du corps, de ce que l'addendum de l'audit source avait établi in extremis (les deux « parasites » présumés, Renaud H. 2020 et Whiterabbit1111 2022, étaient cachés dans des entrées concaténées du PDF).

**Prises qui corrigent ou précisent l'audit source** (re-vérifiées sur v110 pour la première) :

1. **Chen 2011 (`72ad349cc28c4760a46521d685fca284`) n'a aucun câblage bibliographique**, contrairement à l'affirmation de l'audit § 2.c (« tous ont par ailleurs au moins une relation appears in section »). Revérification directe sur v110 dans le cadre du présent chantier : 5 relations au total, **zéro** `cited in`, **zéro** `appears in section` (sorties vers Silk Road et l'événement Ulbricht, entrée `authored` depuis Adrian Chen). L'article est pourtant cité dans le corps (`01_chapitre_I.md` l. 281).
2. **Trois titres de nœuds sont des paraphrases trompeuses** : « Balakrishnan 2020 — Ethereum history » (titre réel : attaque double dépense sur ETC), « Koning 2020 — Bitcoin as monetary system analysis » (titre réel : « The bitcoin-to-salvia divinorum trade route » ; et le corps cite « 2020b », suffixe que la bibliographie ne connaît pas), « Whiterabbit1111 2022 — Bitcoin NFTs and ordinal inscriptions » (titre réel : « The origin digital antiquities market (NFTs) »).
3. **La graphie fautive « Whitebbit1111 » est portée par un nœud jumeau** (`4cf7803656584b009ba11f1a99fdb6e8`, qui capte la citation du corps — elle-même fautive dans le texte) **et par une entité `Person`** (`11596aed3e4340fdb6811050176a3c74`), tandis que la graphie correcte « Whiterabbit1111 » est sur le nœud jamais cité. Fusion et normalisation de graphie à arbitrer ensemble.
4. « Chainalysis Team 2019 — Crypto Crime Report » (`2e155d6c…`, jamais cité) est le jumeau du nœud cité `0e225413…` : la famille 27 du diagnostic doublons le couvre — le marquage est dans le patch candidat, la fusion réglerait le cas.

## 6. Les trois patchs candidats — ce qu'ils contiennent, ce qu'ils excluent

Tous trois portent `_meta.source_graph = grc20-these-mael-rolland-v110.json`, `_meta.generated = 2026-08-07`, une `_meta.policy` commençant par « CANDIDATE — NOT APPLIED — AUTHOR ARBITRATION REQUIRED », et une `_meta.skipped` motivée ligne à ligne. Chaque `entityId` et chaque id de type cités ont été vérifiés dans v110 (existence + nom courant conforme au CSV).

### 6.a `patch_candidate_bibliographie_retypes_v1.json` — 10 ops, 16 skipped

- **Contient** : 2 `SET_TYPES` (Shinobi, DeNardis → `Person`, id de type `ed738791205548e4b4c187c58be227dc` repris à l'identique de patch_18) et 4 paires `SET_NAME` + `SET_TYPES` (Adli Takkal Bataille, Andreas Loibl, Gérard Dréan, Jacques Favier). 6 entités touchées.
- **Ne contient pas, et pourquoi** : les 14 `arbitrage-auteur` (aucune preuve bibliographique admissible, ou conflation à corriger d'abord — raison du CSV reprise dans chaque entrée `skipped`) et les 2 `laisser-reference` (fiches à deux auteurs, intyoables en une `Person`). Critère d'inclusion strict : seule une fiche dont l'entrée d'auteur du PDF confirme (ou corrige sans ambiguïté ni homonyme) le nom complet est retypée.

### 6.b `patch_candidate_bibliographie_duplicates_v1.json` — 156 ops, 18 skipped

- **Contient** : pour chacun des **78 membres non canoniques** des 71 familles fusion-sure, 2 `SET_ATTRIBUTE` — `duplicateOf` = entity_id du canonique par degré, `reviewStatus` = `pending-author` (convention non destructive de `patch_10_dedup_events.json` : rien n'est supprimé, rien n'est fusionné, tout reste interrogeable).
- **Ne contient pas, et pourquoi** : les 6 doublon-probable (vérification de titre/édition restante) et les 12 homonymie-risque (paires de références réelles possibles ; l'annotation `reviewStatus=homonym-check` du CSV est reprise dans `skipped` **à titre indicatif seulement**, aucune op émise).
- **Vérification registre, consignée dans `_meta.registry_note`** : contrairement à l'hypothèse de travail du chantier, `duplicateOf` (`26a1cb779802d673fe8ed4e11c8b380e`) et `reviewStatus` (`519fdfcc579905e7bab12918df1e6f2b`) **existent déjà** dans `grc20-properties-registry-v1.json` — posées par patch_10 sur 3 nœuds événements. Mais leur `domain` enregistré est `[CrisisEvent, InfrastructureEvent]` (count=3, status=**structural**, readBy `scripts/verif_doublons.py` et `scripts/make_v105_dedup_events.py`). `check_graph_integrity.py` ne bloque que les clés **absentes** du registre : appliquer ce patch ne casserait pas ce contrôle, mais rendrait le registre — invariant de CI d'après CLAUDE.md — factuellement faux (domain/count périmés). L'application exigerait donc de régénérer le registre dans le même mouvement, de vérifier `verif_doublons.py` (qui raisonne sur les doublons d'événements et pose l'invariant « un seul duplicateOf par entité »), et d'assumer la nouvelle valeur `pending-author` à côté du `duplicate-pending-merge` des 3 porteurs actuels.
- `_meta.canonical_semantics` documente la distinction cible-de-fusion / libellé du § 3 (41 contradictions).

### 6.c `patch_candidate_bibliographie_missing_nodes_v1.json` — 38 candidats, 22 skipped

- **Contient** : 38 `CREATE_ENTITY` **descriptifs** pour les entrées `vraiment_absente=oui` + `entree-complete` + risque `faible` uniquement. `name` = clé de citation du corps + titre court, sur la convention majoritaire des nœuds existants (« Auteur Année — Titre ») ; `types` = `type_propose` du CSV en ids **exacts** de v110 (`Reference` `51f53c59535b4e22b1dd0d83f6593fe1`, `GreyLiterature` `b6ff2981875a4027a8cbd56e26010732`, `IndigenousLiterature` `d62cf376f60449dfbdb1350c924231bc`, `AcademicWork` `9a2fd04e026a410281686e02a6de3dcd`) ; attribut `source_entry` = l'entrée **complète** (non tronquée) retrouvée dans `assets/MD/07_bibliographie.md` pour chacune des 38.
- **Ne contient pas, et pourquoi** : les 6 faux absents (créer = fabriquer un doublon), les 7 risque élevé (orphelins garantis), les 6 risque moyen (lettrage corps/bibliographie discordant — Nakamoto 2008b —, appel ambigu — Roussel 2017b —, collision de clé — Zelizer 2005 —, etc.), les 2 partielles (URL non pérenne, entrée sans millésime) et la douteuse (THE IRS 2014, titre de l'entrée = celui du guidance FinCEN 2013 déjà noué).
- **Limites d'applicabilité, consignées dans `_meta`** : (1) **aucun applicateur du dépôt ne consomme `CREATE_ENTITY`** — les applicateurs existants ne traitent que `SET_NAME`/`SET_TYPES`/`SET_ATTRIBUTE`/`DELETE_ATTRIBUTE` ; l'application exigerait un script dédié `make_vNNN` qui assigne les entityId (aucun n'est préassigné), pose les relations `cited in`/`appears in section`, sous arbitrage ; (2) la clé `source_entry` **n'existe pas** au registre des propriétés — en l'état, un graphe qui la porterait serait **bloqué** par `check_graph_integrity.py` (toute clé hors registre est bloquante) : ajout au registre requis d'abord.

## 7. Risques — ce que l'instruction a évité, ce qui reste dangereux

- **Conflations de personnes réelles évitées de justesse.** « Florence Dufy » n'existe pas : c'est la soudure du patronyme de DUFY Caroline et du prénom de WEBER Florence, co-autrices de *L'ethnographie économique* — la retyper en `Person` aurait gravé une personne fictive. « Marco Corallo » retypé aurait créé une **seconde** `Person` de Matt Corallo (`548ff3dd…`, déjà présente — la fiche porte même une relation `authored` vers elle) sous un prénom faux. « "The Madhatter" » retypé aurait entériné la relation `authored` qui le soude à GameKyuubi, pseudonyme distinct (l'auteur du post HODL). Aucun des trois n'est dans le patch retypes.
- **La distinction cible-de-fusion vs libellé** (§ 3) : appliquer les 71 fusions en croyant régler aussi le nommage laisserait 41 nœuds survivants au libellé que l'audit source juge non conforme au PDF. Deux décisions, pas une.
- **Orphelins potentiels** : les 7 entrées jamais citées du PDF (§ 4), mais aussi, côté inverse, tout retard de câblage des 38 créations candidates — un nœud créé sans ses `cited in` rejoindrait précisément la population « jamais cités » que le diagnostic 4 vient d'assainir.
- **Titres de nœuds trompeurs** : les trois paraphrases du § 5 (Balakrishnan, Koning 2020, Whiterabbit1111) et l'étiquette « Popper 2016a » qui porte le titre de 2016b sont des pièges pour tout futur appariement automatique — un correctif de libellés est un chantier propre, non couvert par les patchs candidats.
- **Créations à coordonner** : trois candidats du patch missing-nodes portent un avertissement `_comment` explicite parce qu'un nœud voisin embrouille la clé — Krugman 2013 (le nœud « Krugman 2018 » porte à tort le titre du billet de 2013), Demirgüç-Kunt & Detragiache 1998 (nœud existant, même duo, même année, autre article), Van Wirdum 2018 (le corps cite « (Van Wirdum 2018) » pour deux articles distincts, dont un absent du PDF). Ils satisfont les critères mécaniques d'inclusion mais leur application aveugle serait risquée.
- **Clés d'attribut** : `duplicateOf`/`reviewStatus` hors domaine enregistré et `source_entry` hors registre (§ 6.b, 6.c) — le premier cas passe la CI en la rendant menteuse, le second la casse.

## 8. Décisions réservées à Maël

Chaque décision est numérotée, actionnable, et adossée à sa donnée (CSV cité entre parenthèses).

**D1.** Appliquer ou non `patch_candidate_bibliographie_retypes_v1.json` : 2 retypages sûrs + 4 renommages-retypages, preuves = entrées d'auteur du PDF citées dans chaque op (fiches-douteuses CSV, lignes Shinobi, DeNardis, Takkal Bataille, Loibl, Dréan, Favier).
**D2.** Politique « notoriété vs preuve bibliographique » pour 7 identités mondialement univoques sans entrée d'auteur au PDF : Desan, Keynes, Stiglitz, Robbins, Croman, Gandal, Macron — retyper hors règle de preuve, ou laisser `Reference` (fiches-douteuses, `arbitrage-auteur`, risque faible).
**D3.** Tyler Winklevoss : retyper sur la foi du corps de la thèse (« Tyler Winklevoss, cité par Mullin 2013 », chap. I et III), seule la bibliographie ne l'attestant pas (fiches-douteuses).
**D4.** « "The Madhatter" » : corriger d'abord la relation `authored` → GameKyuubi (deux pseudonymes distincts), puis décider du retypage (fiches-douteuses, `9b9c6eb4…`).
**D5.** « Alain Maucourant » : renommer « Jérôme Maucourant » sur preuve **hors** bibliographie (l'économiste co-auteur de Plociniczak), ou laisser (fiches-douteuses, `4722e761…`).
**D6.** « Felix Albert » : trancher l'équivalence FelixA = Felix Albert (plausible, non attestée) et corriger l'ancrage `cited in` chap. I alors que les mentions sont au chap. III (fiches-douteuses, `4d583f06…`).
**D7.** « Florence Dufy » : renommer « Caroline Dufy », réattribuer à Florence Weber, ou laisser — la fiche actuelle soude deux autrices (fiches-douteuses, `4efa5d34…`).
**D8.** « Marco Corallo » : fusionner dans la `Person` « Matt Corallo » (en réaffectant la relation `mentions actor` de I.2.2) ou supprimer la fiche (fiches-douteuses, `f270bfdb…`).
**D9.** « Martti Malmi (Sirius) » : fusionner la fiche (sa quote, son `cited in` chap. I) dans la `Person` existante `e395c577…` (fiches-douteuses, `10973e59…`).
**D10.** Les deux fiches à deux auteurs : fusionner « De Boyer des Roches et Rosales » dans le nœud daté `4ccbb429…` et « Desmedt et Lakomski-Laguerre » dans `d80bed08…` ? Et ouvrir (ou non) le chantier distinct du renommage de la `Person` « Mathieu Desmedt » → Ludovic, prénom contredit par le PDF (fiches-douteuses, `laisser-reference`).
**D11.** Valider les **71 fusions sûres** — c'est-à-dire, pour chaque famille, confirmer la **cible** proposée (canonique par degré, colonne `canonique_propose`) ; le marquage candidat est prêt (doublons-familles CSV ; patch duplicates).
**D12.** Pour les **41 familles** où cible et « forme à garder » divergent (§ 3) : décider le **libellé final** du nœud survivant — garder le nom du canonique ou le renommer sur la forme à garder de l'audit source § 2.d (donnée : croisement CSV famille par famille, re-calculable).
**D13.** Les 6 doublon-probable : confirmer titre/édition avant fusion (ECB 2012 — lettre a/b contradictoire entre graphe et PDF —, Polanyi 1944/2011, Pouliot 2018, Servet & Dufrêne 2021, Tirole 2017, Wray 2010) (doublons-familles, classe `doublon-probable`).
**D14.** Les 12 homonymie-risque : vérifier référence par référence quel texte le corps cite (Blanc 1998a/b, Blanc 2009a/b, Buterin 2013a/d, 2013c, 2014j, 2017a/b/c, Lee 2011, Möser 2015, Orléan 1998 — probable doublon **mal étiqueté** d'Aglietta & Orléan 2002 à réaffecter —, Selgin 2013/2014b, Walch 2017a/b ×2) (doublons-familles, classe `homonymie-risque`).
**D15.** Si le patch duplicates est appliqué : régénérer le registre des propriétés (domain/count de `duplicateOf` et `reviewStatus`), statuer sur la coexistence des valeurs `pending-author` / `duplicate-pending-merge`, et vérifier `verif_doublons.py` (§ 6.b).
**D16.** Valider (ou élaguer) les **38 créations candidates** du patch missing-nodes — en particulier les trois cas à avertissement : Krugman 2013, Demirgüç-Kunt & Detragiache 1998, Van Wirdum 2018 (§ 7 ; entrees-sans-noeud CSV).
**D17.** Pour ces créations : choisir la clé d'attribut de provenance (`source_entry` à ajouter au registre, ou clé existante), et commander le script `make_vNNN` qui assignera les ids et posera les câblages `cited in` / `appears in section` (§ 6.c).
**D18.** Les 7 entrées complètes du PDF jamais citées dans le corps (Koning 2013, Nakamoto 2010d/e, Orléan 2002, Song 2018a/b, Tual 2016c) : renoncer à les créer, ou créer sciemment des nœuds de fonds non cités (entrees-sans-noeud, `risque_ajout_inutile=eleve`).
**D19.** Les 6 cas moyens ou ambigus : Bier 2018, Nakamoto 2008b (lettrage corps/biblio discordant), Nakamoto 2009c et 2010c (épisodes racontés sans appel), Roussel 2017b (l'appel semble viser 2017a), Zelizer 2005 (collision de clé avec le livre homonyme) — créer, différer, ou requalifier (entrees-sans-noeud, risque `moyen`).
**D20.** « THE IRS 2014 » : éclaircir l'attribution contradictoire du PDF (titre = guidance FinCEN 2013 déjà noué) avant toute création (entrees-sans-noeud, `douteuse`).
**D21.** « TraFin 2014 » (`6b3c8ba8…`) : millésime sans entrée au PDF, probable confusion avec les rapports 2011/2017 — requalifier ou fusionner, en coordination avec les créations Ministère 2011/2017 (entrees-sans-noeud, lignes MINISTERE ; audit source § 2.a).
**D22.** Chen 2011 : câbler `cited in` (chap. I) et `appears in section` — le nœud n'a aucun câblage bibliographique (§ 5.1 ; parasites CSV).
**D23.** Renommer (ou non) les trois nœuds aux titres paraphrasés trompeurs sur leur titre réel : Balakrishnan 2020, Koning 2020 (avec arbitrage du suffixe 2020/2020b), Whiterabbit1111 2022 (§ 5.2 ; parasites CSV).
**D24.** Le nid Whiterabbit1111/Whitebbit1111 : fusionner les deux nœuds `Reference`, corriger la graphie de la `Person` `11596aed…`, et choisir la graphie de référence alors que le corps de la thèse porte lui-même la faute (§ 5.3 ; parasites CSV).
**D25.** L'étiquette « Popper 2016a » (`37bcfcd5…`) qui porte le titre de l'article 2016b : réétiqueter le nœud et rouvrir (ou non) la création pour le vrai 2016a « Paper Points Up Flaws » (entrees-sans-noeud, ligne POPPER 2016B).

## 9. Ce que ce chantier n'a pas fait

- **Aucune application** : v110, les cartes, le runtime et le registre sont intacts ; les trois patchs sont candidats, leurs ops n'ont jamais été exécutées, même en mémoire, ailleurs que pour la validation de forme.
- **Aucune fusion, aucun nœud créé, aucun id assigné** aux créations candidates.
- **Pas de re-vérification indépendante des quatre CSV contre le PDF** : ils sont l'autorité du chantier ; seules leurs références à v110 (existence et nom de chaque entityId, ids de types) et leurs comptes internes ont été revérifiés — sans écart, hormis un artefact d'échappement CSV sur « "The Madhatter" » (guillemets littéraux du nom).
- **Pas d'arbitrage des tensions inter-diagnostics** : les cas où un candidat mécanique du diagnostic 3 croise un piège du diagnostic 2 ou 4 (Krugman 2013, Demirgüç-Kunt 1998, Van Wirdum 2018, Theymos 2018, familles Buterin) sont documentés en avertissements, pas tranchés.
- **Pas de proposition de libellés** pour les 41 familles à contradiction cible/forme (D12) ni de patch de renommage des titres trompeurs (D23) : ce serait choisir à la place de l'auteur.
- **Pas de passe navigateur** : aucun fichier lu par `graphe.html`/`lecteur.html` n'a changé, la vérification visuelle (`grc20-visual-coherence`) n'était pas due.
