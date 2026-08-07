# GRC-20 Bibliographie — conversion du PDF et réconciliation avec le graphe v109

**Date** : 2026-08-06  
**Graphe audité** : `grc20-these-mael-rolland-v109.json` (770 nœuds bibliographiques : types `Reference`/`AcademicWork`/`GreyLiterature`/`IndigenousLiterature`, hors `PrimarySource`)  
**Mode agent** : A (audit documentaire, avec production d'un patch **non appliqué**)  
**Source de vérité** : `assets/MD/07_bibliographie.md` — conversion de `assets/pdf/9_Bibliographie.pdf` (42 pages, p. 341–382 du PDF de la thèse), produite dans le cadre de ce même audit  
**Données probantes** : `docs/audits/data/bibliographie-reconciliation-v109.csv` (les 770 nœuds, un par ligne, avec appariement et compte de `cited in`)  
**Patch associé** : `patch_18_bibliography_fixes.json` (racine, **non appliqué**)

> Rappel de la charte : un agent est un rôle de travail, pas une autorité scientifique. Aucune fusion de doublons n'est opérée ni proposée en op ; les tables ci-dessous préparent l'arbitrage de Maël Rolland, elles ne le remplacent pas.

## 1. Conversion du PDF (étape 1)

- **42 pages** extraites (pypdf), **652 entrées** reconstituées, une par paragraphe, dans `assets/MD/07_bibliographie.md`.
- La bibliographie du PDF est une **liste alphabétique unique**, sans sections internes (pas de séparation académique / indigène / presse) — il n'y a donc pas de titres `##` à reproduire.
- Fidélité : le contenu des entrées est reproduit tel qu'extrait, coquilles comprises ; seuls les retours à la ligne internes ont été fusionnés et les suites d'espaces réduites. Aucune entrée inventée, corrigée ou reformatée.
- Contrôles effectués : ordre alphabétique intègre sur les 652 entrées (0 rupture), aucune entrée fusionnée détectée par motif « NOM Prénom, année » interne, 12 cas limites de découpage arbitrés à la main (auteurs multiples sur deux lignes, entrées sans millésime, entrées anonymes commençant par « guillemet »).

### Anomalies internes du PDF (constatées, non corrigées)
- **Doublon interne** : Star & Ruhleder 2010 (« Vers une écologie de l'infrastructure ») figure **deux fois** (sous « LEIGH STAR Susan et RUHLEDER Karen » p. 363 et sous « STAR Susan Leigh et RUHLEDER, K aren » p. 376).
- **Doublon interne** : l'interview Friedman 1999 (Land value tax, même URL YouTube) figure sous « FRIEDMAN Milton., 1999 » et une seconde fois en entrée anonyme de fin de liste.
- Coquilles d'origine conservées : « KINDELBERGER » (pour Kindleberger), « DEMIRGÜÇ-KUNTASLI Asli » (nom et prénom collés), « LEE Charli » (pour Charlie Lee), « JEVONS Willian », « Nakamoto Satoshi, 2010 g » (casse et espace).
- 5 entrées sont **sans millésime** (BITCOIN WIKI, BITCOIN.FR, ETHHUB s.d., NEWBERY & ROCHARD, PEERCOIN).

## 2. Réconciliation avec les 770 nœuds (étape 2)

Méthode d'appariement : clé (premier auteur normalisé, millésime), avec repli sur les co-auteurs et l'attribut `authors`, départage par recouvrement de titre et par suffixe de millésime (2010a…2010g), 14 appariements manuels documentés (acronymes CJUE/ECB/IETF, entrées anonymes, « SECURITIES AND EXCHANGES COMMISSION », etc.). Détail nœud par nœud dans le CSV.

### Chiffres
| Mesure | Valeur |
|---|---|
| Nœuds bibliographiques v109 | **770** (760 `Reference`, 143 `AcademicWork`, 87 `GreyLiterature`, 53 `IndigenousLiterature`, avec multi-typage) |
| Entrées du PDF | **652** |
| Entrées du PDF ayant ≥ 1 nœud | **592** (90,8 %) |
| Entrées du PDF sans aucun nœud | **60** |
| Nœuds appariés à une entrée du PDF | **691** (89,7 %) |
| Nœuds sans entrée au PDF | **79** = 33 datés + 46 sans millésime |
| Familles de doublons (≥ 2 nœuds sur la même entrée du PDF) | **89**, soit **99 nœuds excédentaires** |
| Nœuds datés avec zéro relation `cited in` | **11** |

Conventions de nommage constatées sur les 770 nœuds (l'audit précédent en comptait 4) :
`« Auteur Année — Titre »` : 502 · `« Auteur Année »` nu : 160 · `« Auteur Année Titre »` sans tiret : 55 · `« Auteur Année (Intro) »` : 4 · sans millésime (fiches d'auteur, titres seuls, pages de sites) : 49.

### Écarts avec l'audit précédent
L'audit antérieur (~74 familles de doublons / ~77 excédentaires, 48 fiches d'auteur, 17 « jamais cités ») n'a pas laissé de liste nominative dans le dépôt ; ses chiffres n'ont donc pas pu être reproduits à l'identique. Le présent comptage, adossé au PDF converti, donne **89 familles / 99 excédentaires**, **43 fiches d'auteur** et **11 datés jamais cités** (définition : zéro relation `cited in` sortante). Les définitions diffèrent probablement à la marge ; les listes nominatives ci-dessous font foi pour v109.

### 2.a Les 33 nœuds datés absents de la bibliographie (imports parasites potentiels)

Aucune entrée du PDF ne porte le même (auteur, millésime). Neuf d'entre eux ont une correspondance *probable mais non conforme* (écart de millésime ou de titre), signalée ci-dessous ; les autres sont sans trace dans la bibliographie.

| Nœud | Types | `cited in` | Observation |
|---|---|---|---|
| « Binance 2017 — Whitepaper Binance Token » (`5aab53cf…`) | Reference | 1 | absent de la bibliographie |
| « Bradbury 2013 » (`6a5e27f6…`) | GreyLiterature,Reference | 1 | le PDF n'a que « BRADBURY Danny, 2014 » (Bitcoin Transaction Fees To Be Slashed Tenfold) — écart de millésime à arbitrer |
| « Croman et al. 2016 » (`ce26299c…`) | AcademicWork,Reference | 2 | absent de la bibliographie |
| « Cuny 2013 » (`05ad44df…`) | GreyLiterature,Reference | 2 | absent de la bibliographie |
| « D'Lola 2020 — Namecoin and decentralized DNS history » (`79ef1b65…`) | Reference | 1 | absent de la bibliographie |
| « Danzeis et Meiklejohn 2015 » (`05338358…`) | AcademicWork,Reference | 3 | aucune entrée Danezis/Meiklejohn 2015 dans le PDF (le SoK Bano et al. 2017 est la seule entrée où ces auteurs apparaissent) — la coquille du nom est corrigée par patch_18, l'absence bibliographique reste à arbitrer |
| « Demirgüç-Kunt & Detragiache 1998 — The determinants of banking crises in developing countries » (`0e1b15a0…`) | Reference | 1 | le PDF a « DEMIRGÜÇ-KUNTASLI Asli et DETRAGIACHE Enrica, 1998, Financial Liberalization and Financial Fragility » — mêmes auteurs et année, mais autre article de 1998 |
| « Dwork & Noar 1992 » (`6981af03…`) | AcademicWork | 1 | absent de la bibliographie |
| « Estrada 2014 » (`144d0cb9…`) | GreyLiterature,Reference | 2 | absent de la bibliographie |
| « Gandal et al. 2018 » (`bc199c17…`) | AcademicWork,Reference | 1 | absent de la bibliographie |
| « Golumbia 2016 Politics of Bitcoin » (`3416740e…`) | Reference | 6 | le PDF n'a que « GOLUMBIA David, 2015, Bitcoin as Politics: Distributed Right-Wing Extremism » — même auteur, millésime et titre divergents |
| « Haber et Stornetta 1991 » (`ee37e054…`) | AcademicWork | 1 | absent de la bibliographie |
| « Halaburda et Gandal 2014 » (`dd7e8024…`) | Reference | 1 | absent de la bibliographie |
| « Hayek 1976 » (`34ea55da…`) | Reference | 1 | absent de la bibliographie |
| « I3Nikolai 2016a — DAO hack analysis and response » (`8d23ca79…`) | Reference | 1 | absent de la bibliographie |
| « Karlstrøm 2014 — Do libertarians dream of electric coins » (`26fdb252…`) | AcademicWork,Reference | 2 | absent de la bibliographie |
| « Kubát 2015 — Virtual currency Bitcoin in the scope of money definition » (`8ec6dc5b…`) | Reference | 6 | absent de la bibliographie |
| « NewLibertyStandard 2009 — Bitcoin exchange rate post » (`04dd36dc…`) | IndigenousLiterature,Reference | 5 | absent de la bibliographie |
| « O'Brien 2014 » (`780f2dd6…`) | GreyLiterature,Reference | 1 | absent de la bibliographie |
| « O'Brien 2014 — Multisig and Bitcoin transaction standards (BIP16) » (`44177b20…`) | Reference | 5 | absent de la bibliographie |
| « O'Leary 2018 » (`2e1ae899…`) | GreyLiterature,Reference | 1 | absent de la bibliographie |
| « O'Leary 2018 — ASICs and Ethereum mining centralization » (`61feb8a1…`) | Reference | 5 | absent de la bibliographie |
| « Philosophie de l'argent (Simmel 1900) » (`a11d118b…`) | AcademicWork | 1 | le PDF n'a que la traduction « SIMMEL Georg, 2009, Philosophie de l'argent » — même œuvre, édition différente |
| « Poon & Dryja 2015 LN » (`a2d58ccd…`) | Reference | 1 | absent de la bibliographie |
| « Renaud H. 2020 — Hal Finney: le premier utilisateur de Bitcoin » (`006e1228…`) | Reference | 0 | absent de la bibliographie |
| « Star & Griesemer 1989 » (`99fade02…`) | Reference | 2 | le PDF n'a ni Star 1989 ni Griesemer ; seuls « STAR 1999 » et « STAR/LEIGH STAR & RUHLEDER 2010 » figurent |
| « The Economist 2015 » (`6a327686…`) | GreyLiterature,Reference | 1 | absent de la bibliographie |
| « Theymos 2015 » (`9c6092d4…`) | IndigenousLiterature,Reference | 4 | le PDF n'a que « THEYMOS, 2018 » (The duplicate input vulnerability…) — autre texte |
| « Timón 2015 — Consensus rule changes in Bitcoin: BIPs and soft forks » (`60d2f0da…`) | Reference | 5 | absent de la bibliographie |
| « Torpey 2018 » (`54491adc…`) | GreyLiterature,Reference | 2 | le PDF n'a que « TORPEY Kyle, 2016 » (Checks and Balances of Bitcoin Governance) |
| « TraFin 2014 — Rapport sur les monnaies virtuelles » (`6b3c8ba8…`) | Reference | 1 | le PDF n'a que « MINISTÈRE DE L'ÉCONOMIE ET DES FINANCES, 2011 (Rapport d'activité Tracfin) » et « 2017 (Traitement du Renseignement…) » — pas de rapport Tracfin 2014 |
| « Whitebbit1111 2022 » (`4cf78036…`) | GreyLiterature,Reference | 1 | absent de la bibliographie |
| « Whiterabbit1111 2022 — Bitcoin NFTs and ordinal inscriptions » (`f1ef1301…`) | Reference | 0 | absent de la bibliographie |

Cas particulier : « Whitebbit1111 2022 » et « Whiterabbit1111 2022 — Bitcoin NFTs… » coexistent (et une entité `Person` « Whitebbit1111 » existe aussi) — vraisemblablement deux graphies du même pseudonyme, aucune des deux dans le PDF. Arbitrage auteur requis, non traité par le patch.

### 2.b Les 60 entrées du PDF sans aucun nœud

Séries les plus touchées : les billets « Moneyness » de J.P. Koning (11 entrées, alors que la fiche d'auteur « J.P. Koning » existe côté graphe), les billets de Stephan Tual 2016a–f sur The DAO (6), les posts Bitcointalk de Nakamoto 2010c–f et 2008b/2009b/2009c (7).

- BIER Jonathan, 2018, « BitMEX Research Sponsors Fork Monitoring Website », https://blog.bitmex.com/bitmex-research-sponsors-Fork-m…
- BITMEX RESEARCH, 2020a, « Who Funds Bitcoin Development? », BitMEX Blog , https://blog.bitmex.com/who-funds-bitcoin-development/, …
- BITMEX RESEARCH, 2018a, « The bitcoin flash crash to $0.01 in June 2011 », BitMEX Blog , https://blog.bitmex.com/the-june-2011-fla…
- BUTERIN Vitalik, 2021, « Why sharding is great: demystifying the technical properties », https://vitalik.ca/general/2021/04/07/sha…
- BUTERIN Vitalik, 2013d, « Ethereum Whitepaper ». (trad en fr. https://ethereum.org/fr/whitepaper/) consulté le 21 octobre 2019.…
- CLASSIC Ethereum et ARVICCO (PSEUDONYME), 2016, « La déclaration d’indépendance d’Ethereum Classic », https://ethereumclassic.org/…
- DAI Wei, 1998, « B-money », https://nakamotoinstitute.org/library/b-money/, consulté le 12 février 2016.…
- DEMIRGÜÇ-KUNTASLI Asli et DETRAGIACHE Enrica, 1998, Financial Liberalization and Financial Fragility, World Bank, Development Rese…
- FELIXA pseudonyme, 2016b, « Update3: The DAO is under attack — but Vitalik saved us », https://blog.daohub.org/the-dao-is-under-at…
- GÜN SIRER Emin, 2016, « Thoughts on The DAO Hack », http://hackingdistributed.com/2016/06/17/thoughts-on-the-dao-hack/, 17 juin 20…
- INGHAM Geoffrey, 2007, « The Specificity of Money », European Journal of Sociology, 2007, vol. 48, no 02, p. 265‑272.…
- INSIDER Coin, 2021, « The story of the DAO, and how it shaped Ethereum », https://www.coininsider.com/what-happened-to-the-dao/, 9…
- KONING J.P, 2019b, « The life and death of an internet monetary meme », https://jpkoning.blogspot.com/, 18 septembre 2019, consult…
- KONING J.P, 2019c, « Moneyness: Classifying cryptocurrencies », https://jpkoning.blogspot.com/2019/07/classifying-cryptocurrencies…
- KONING J.P, 2018a, « Moneyness: Can lottery tickets become money? », https://jpkoning.blogspot.com/2018/12/can-lottery-tickets-bec…
- KONING J.P, 2018b, « Moneyness: Bitcoin and the bubble theory of money », https://jpkoning.blogspot.com/2018/10/bitcoin-and-bubble…
- KONING J.P, 2018c, « Play Bitcoin : Remember, it’s just a game », https://breakermag.com/play - bitcoin-remember-its-just-a-game/,…
- KONING J.P, 2018d, « Moneyness: Tainted money », https://jpkoning.blogspot.com/2018/07/tainted- money.html, 31 juillet 2018, consu…
- KONING J.P, 2018e, « Moneyness: A case for bitcoin », https://jpkoning.blogspot.com/2018/05/the- case-for-bitcoin.html, 10 mai 201…
- KONING J.P, 2018f, « Moneyness: Fiatsplainin’ », https://jpkoning.blogspot.com/2018/03/fiatsplainin.html, 21 mars 2018, consulté l…
- KONING Jp, 2017, « Moneyness: The evolution of the Federal Reserve’s promises as recorded on their banknotes », https://jpkoning.b…
- KONING J.P, 2013, « Moneyness: Why the Fed is more likely to adopt bitcoin technology than kill it off », https://jpkoning.blogspo…
- KONING J.P, 2012, « Moneyness: Bitcoin steps on the toes of a few popular monetary theories », https://jpkoning.blogspot.com/2012/…
- KRUGMAN Paul, 2013, « Bitcoin is Evil », https://krugman.blogs.nytimes.com/2013/12/28/bitcoin-is- evil/?_r=1&, 28 décembre 2013, c…
- LATOUR Bruno, 2000, « La fin des moyens », Réseaux, 2000, vol. 18, no 100, p. 39‑58.…
- LEIGH STAR Susan et RUHLEDER Karen, 2010, « Vers une écologie de l’infrastructure : Conception et accès aux grands espaces d’infor…
- MANGOLTE Pierre-André, 2013b, « Une innovation institutionnelle, la constitution des communs du logiciel libre », Revue de la régu…
- MINISTÈRE DE L ’ÉCONOMIE ET DES FINANCES, 2019b, « BNC - Champ d’application - Activités et revenus imposables - Généralités - Exp…
- MINISTÈRE DE L’ÉCONOMIE ET DES FINANCES , 2017, Traitement du Renseignement et Action contre les Circuits FINanciers clandestins.,…
- MINISTÈRE DE L’ÉCONOMIE ET DES FINANCES, 2011, Rapport d’activité 2011, Tracfin, s.l.…
- NAKAMOTO Satoshi, 2010c, « [PATCH] increase block size limit », https://bitcointalk.org/index.php?topic=1347.msg15139#msg15139, co…
- NAKAMOTO Satoshi, 2010d, « They want to delete the Wikipedia article », https://bitcointalk.org/index.php?topic=342.msg4508#msg450…
- NAKAMOTO Satoshi, 2010e, « Transactions and Scripts: DUP HASH160 ... EQUALVERIFY CHECKSIG », https://bitcointalk.org/index.php?top…
- NAKAMOTO Satoshi, 2010f, « Re: Wikileaks contact info? / Satoshi Nakamoto Institute », https://bitcointalk.org/index.php?topic=173…
- NAKAMOTO Satoshi, 2009 b, « Bitcoin open source implementation of P2P currency », http://p2pfoundation.ning.com/forum/topics/bitco…
- NAKAMOTO Satoshi, 2009 c, « Bitcoin v0.1 released », https://www.metzdowd.com/pipermail/cryptography/2009-January/014994.html, con…
- NAKAMOTO Satoshi, 2008b, « Bitcoin P2P e -cash paper », https://www.metzdowd.com/pipermail/cryptography/2008-November/014815.html,…
- ORLÉAN A., 2002, « La monnaie contre la marchandise », L’Homme, 2002, no 2, p. 27‑48.…
- PEERCOIN, « Peercoin Docs - Documentation of Peercoin Cryptocurrency », https://www.peercoin.net/docs/proof-of-stake, consulté le …
- POLROT Simon, 2016b, « Slock.it : la promesse des objets connectés sur la blockchain », https://www.ethereum-france.com/blog/slock…
- POLROT Simon, 2016c, « The DAO mortem », https://www.ethereum-france.com/blog/the-dao-post- mortem/, consulté le 7 mai 2021.…
- POPPER Nathaniel, 2016b, « A Venture Fund With Plenty of Virtual Capital, but No Capitalist », The New York Times, 22 mai 2016.…
- ROUSSEL Alexis, 2017 b, « The Whitehat Withdrawal Contract has been extended for 2 months », http://blog.bity.com/2017/01/30/the-w…
- SCHNEIDER Nathan, 2015, « En cavale avec le voleur de banque Enric Duran », https://www.vice.com/fr/article/ppnxg8/devenez-la-banq…
- SONG Jimmy, 2018a, « Lord Keynes Would Be Proud », Medium, https://medium.com/@jimmysong/lord-keynes-would-be-proud-a225fec9cf6a, …
- SONG Jimmy, 2018b, « Crypto-Keynesian Lunac y », Medium, https://medium.com/@jimmysong/crypto-keynesian-lunacy-16bb9193a58, 18 jui…
- TERUZZI David, 2016b, « Les consensus: Proof of work vs Proof of stake », blogchain café , https://blogchaincafe.com/les-consensus…
- THE INTERNAL REVENUE SERVICE (IRS), 2014, « Guidance on the Application of FinCEN’s Regulations to Persons Administering, Exchangi…
- THEYMOS, 2018, « The duplicate input vulnerability shouldn’t be forgotten », https://bitcointalk.org/index.php?topic=5035144.0, 22…
- TUAL Stephan, 2016a, « The DAO Creation is now Live », Slock.it Blog, https://archive.is/wOiUZ, 30 avril 2016, consulté le 3 mai 2…
- TUAL Stephan, 2016b, « Daohub.org gets a facelift, full scope of The DAO is revealed », Medium, https://medium.com/ursium-blog/dao…
- TUAL Stephan, 2016c, « A Primer to Decentralized Autonomous Organizations (DAOs) », https://blog.slock.it/a-primer-to-the-decentra…
- TUAL Stephan, 2016d, « Vitalik Buterin, Gavin Wood, Alex van De Sande, Vlad Zamfir announced amongst exceptional DAO Curators », M…
- TUAL Stephan, 2016e, « Announcing DAO.LINK, the bridge between blockchain and brick -and- mortar companies », Slock.it Blog , http…
- TUAL Stephan, 2016f, « No DAO funds at risk following the Ethereum smart contract ‘recursive call’ bug discovery », Slock.it Blog …
- VAN WIRDUM Aaron, 2018, « The Genesis Files: How David Chaum’s eCash Spawned a Cypherpunk Dream », Bitcoin Magazine, https://bitco…
- WOOD Gavin, 2014a, « Gav’s Ethereum Ð ΞV Update II », Blog Etheruum , https://blog.ethereum.org/2014/11/01/gavs-ethereum-d%ce%bev-…
- ZAMFIR Vlad, 2016, « (2) Vlad Zamfir sur X : « @simondlr would the community hard Fork ethereum if there was a critical bug in the…
- ZELIZER Viviana, 2005, « Argent, circuits, relations intimes », Enfances, Familles, Générations, 2005, no 2.…
- « Milton Friedman, Land value tax and internet currencies », 1999, https://www.youtube.com/watch?v=j2mdYX1nF_Y, consulté le 26 mai…

### 2.c Les nœuds datés « jamais cités » (zéro `cited in`)

Recomptage v109 : **11** nœuds datés n'ont aucune relation `cited in` (tous ont par ailleurs au moins une relation `appears in section` — aucun nœud bibliographique n'est totalement orphelin de relations). La liste des « 17 » de l'audit précédent n'étant pas dans le dépôt, c'est cette liste-ci qui est vérifiable :

| Nœud | Dans la bibliographie ? | Verdict proposé |
|---|---|---|
| « Chen 2011 » | OUI | légitime (au fonds bibliographique, sans citation câblée — câblage à compléter ou référence de contexte) |
| « Balakrishnan 2020 — Ethereum history » | OUI | légitime (au fonds bibliographique, sans citation câblée — câblage à compléter ou référence de contexte) |
| « Ethereum Foundation 2021 — Client ecosystem update » | OUI | légitime (au fonds bibliographique, sans citation câblée — câblage à compléter ou référence de contexte) |
| « Renaud H. 2020 — Hal Finney: le premier utilisateur de Bitcoin » | NON | candidat import parasite (ni cité, ni au fonds) |
| « Koning 2020 — Bitcoin as monetary system analysis » | OUI | légitime (au fonds bibliographique, sans citation câblée — câblage à compléter ou référence de contexte) |
| « SEC 2017 — Report of Investigation Pursuant to Section 21(a) of the Securities Exchange Act of 1934: The DAO » | OUI | légitime (au fonds bibliographique, sans citation câblée — câblage à compléter ou référence de contexte) |
| « Swissinfo 2016 — Zug becomes first municipality to accept Bitcoin » | OUI | légitime (au fonds bibliographique, sans citation câblée — câblage à compléter ou référence de contexte) |
| « Van Wirdum 2017 — Extension blocks proposal for Bitcoin scaling » | OUI | légitime (au fonds bibliographique, sans citation câblée — câblage à compléter ou référence de contexte) |
| « Voell 2020 — Ethereum Classic double-spend attack » | OUI | légitime (au fonds bibliographique, sans citation câblée — câblage à compléter ou référence de contexte) |
| « Whiterabbit1111 2022 — Bitcoin NFTs and ordinal inscriptions » | NON | candidat import parasite (ni cité, ni au fonds) |
| « Chainalysis Team 2019 — Crypto Crime Report » | OUI | légitime (au fonds bibliographique, sans citation câblée — câblage à compléter ou référence de contexte) |

Deux seulement cumulent absence de citation **et** absence de la bibliographie : « Renaud H. 2020 » et « Whiterabbit1111 2022 ». « Chainalysis Team 2019 — Crypto Crime Report » est un doublon non cité d'un nœud cité (« Chainalysis Team 2019 », cited_in=1) — la fusion réglerait le cas.

### 2.d Les 89 familles de doublons — forme à garder d'après le PDF (proposition)

Deux nœuds sont dans la même famille lorsqu'ils s'apparient à la **même entrée du PDF**. La colonne « forme à garder » est une **proposition** fondée sur le recouvrement avec l'entrée du PDF (titre réel de l'œuvre) et la richesse du typage ; **aucune fusion n'est opérée ni mise en op** — arbitrage auteur.

| # | Entrée du PDF (tronquée) | Nœuds de la famille | Forme correspondant au PDF (proposition) |
|---|---|---|---|
| 1 | AGLIETTA Michel et CARTELIER Jean, 1998, « Ordre monétaire des économies de marché » dans … | « Aglietta & Cartelier 1998 — Ordre monétaire » (`4568cc43…`, cited_in=6)<br>« Aglietta et Cartelier 1998 » (`78c9029a…`, cited_in=5) | « Aglietta & Cartelier 1998 — Ordre monétaire » |
| 2 | AGLIETTA Michel et ORLÉAN André, 2002, La monnaie entre violence et confiance, Odile Jacob… | « Aglietta & Orleans 2002 » (`02e004e0…`, cited_in=4)<br>« Aglietta & Orléan 2002 — Violence et confiance » (`dfeba626…`, cited_in=4)<br>« Aglietta et Orléan 2002 » (`3b34cd1c…`, cited_in=4) | « Aglietta & Orléan 2002 — Violence et confiance » |
| 3 | AGLIETTA Michel, PONSOT Jean-François et OULD-AHMED Pepita, 2014, « La monnaie, la valeur … | « Aglietta Ponsot Ould-Ahmed 2014 — Entretien » (`7e9c5d90…`, cited_in=1)<br>« Aglietta, Ponsot et Ould-Ahmed 2014 » (`d1a9cf84…`, cited_in=1) | « Aglietta Ponsot Ould-Ahmed 2014 — Entretien » |
| 4 | AKRICH Madeleine, 1989, « La construction d’un système socio -technique – Esquisse pour un… | « Akrich 1989 » (`2528eba9…`, cited_in=8)<br>« Akrich 1989 — Construction d'un système socio-technique » (`750fdaa2…`, cited_in=7) | « Akrich 1989 — Construction d'un système socio-technique » |
| 5 | ANDRESEN Gavin, 2016, « One-dollar lulz • Gavin Andresen », http://gavinandresen.ninja/One… | « Andresen 2016 » (`f8d9b4f1…`, cited_in=2)<br>« Andresen 2016 — One-dollar lulz » (`63ed4d1a…`, cited_in=3) | « Andresen 2016 — One-dollar lulz » |
| 6 | ANDRESEN Gavin, 2012, « Blockchain Rule Update Process », https://gist.github.com/gavinand… | « Andresen 2012 BIP Process » (`65b4ab9b…`, cited_in=2)<br>« Andresen 2012 — Blockchain Rule Update Process » (`f8fb83d5…`, cited_in=1) | « Andresen 2012 — Blockchain Rule Update Process » |
| 7 | ANDRESEN Gavin, 2011, « Bitcoin / [bitcoin-list] Bitcoin version 0.3.20.01 released ».… | « Andresen 2011 » (`aff449b2…`, cited_in=2)<br>« Andresen 2011 — Bitcoin v0.3.20.01 released » (`74f91343…`, cited_in=6) | « Andresen 2011 — Bitcoin v0.3.20.01 released » |
| 8 | BANO Shehar, ALBERTO Sonnino, AL-BASSAM Mustafa, AZOUVI Sarah, MCCORRY; Patrick, MEIKLEJOH… | « Bano et al. 2017 » (`206f2add…`, cited_in=5)<br>« Bano et al. 2017 (Intro) » (`30dca256…`, cited_in=4) | « Bano et al. 2017 » |
| 9 | BARTOLETTI Massimo et POMPIANU Livio, 2017, « An analysis of Bitcoin OP RETURN metadata »,… | « Bartoletti & Pompianu 2017 » (`ae73f326…`, cited_in=2)<br>« Bartoletti et Pompianu 2017 » (`b4b693b0…`, cited_in=2) | « Bartoletti & Pompianu 2017 » |
| 10 | BITCOIN CORE, 2018a, « CVE-2018-17144 Full Disclosure », https://bitcoincore.org/en/2018/0… | « Bitcoin Core 2018 Rapport divulgation » (`3d0cbcef…`, cited_in=2)<br>« Bitcoin Core 2018a — CVE-2018-17144 Full Disclosure » (`dd3e2896…`, cited_in=5) | « Bitcoin Core 2018a — CVE-2018-17144 Full Disclosure » |
| 11 | BITMEX RESEARCH, 2017b, « Revisiting “The DAO” », BitMEX Blog , https://blog.bitmex.com/re… | « Bitmex Research 2017 DAO Hard Fork » (`02ecb7bc…`, cited_in=2)<br>« Bitmex Research 2017b — Revisiting The DAO » (`a42a1798…`, cited_in=5) | « Bitmex Research 2017b — Revisiting The DAO » |
| 12 | BITMEXRESEARCH, 2022, « The OP_Return Wars of 2014 - Dapps Vs Bitcoin Transactions », http… | « BitMEXResearch 2022 » (`20c955b4…`, cited_in=3)<br>« BitMEXResearch 2022 — The OP_Return Wars » (`9131cfdb…`, cited_in=3) | « BitMEXResearch 2022 — The OP_Return Wars » |
| 13 | BLANC Jérôme, 2009a, « Contraintes et choix organisationnels dans les dispositifs de monna… | « Blanc 2009 IMF » (`38ffe351…`, cited_in=6)<br>« Blanc 2009a — Monnaies sociales contraintes organisationnelles » (`4df197e4…`, cited_in=3) | « Blanc 2009a — Monnaies sociales contraintes organisationnelles » |
| 14 | BLANC Jérôme, 1998a, « Les monnaies parallèles. Approches historiques et théoriques », Uni… | « Blanc 1998 Monnaies paralleles » (`7094b286…`, cited_in=7)<br>« Blanc 1998a — Les monnaies parallèles approches historiques » (`a906b883…`, cited_in=3)<br>« Blanc 1998a » (`c1ac22eb…`, cited_in=1) | « Blanc 1998a — Les monnaies parallèles approches historiques » |
| 15 | BÖHME Rainer, CHRISTIN Nicolas, EDELMAN Benjamin et MOORE Tyler, 2015, « Bitcoin: Economic… | « Bohme et al 2015 Bitcoin Economics » (`56dc412f…`, cited_in=6)<br>« Böhme et al. 2015 — Bitcoin Economics Technology Governance » (`5c2cf7a5…`, cited_in=3) | « Böhme et al. 2015 — Bitcoin Economics Technology Governance » |
| 16 | BONNEAU Joseph, MILLER Andrew, CLARK Jeremy, NARAYANAN Arvind, KROLL Joshua A, FELTEN Edwa… | « Bonneau et al. 2015 » (`762e6813…`, cited_in=4)<br>« Bonneau et al. 2015 — SoK Bitcoin Cryptocurrencies » (`85ea3fbf…`, cited_in=4) | « Bonneau et al. 2015 — SoK Bitcoin Cryptocurrencies » |
| 17 | BOWKER Geoffrey C, 1996, « The history of information infrastructures: The case of the int… | « Bowker 1996 Infrastructure Inversion » (`1fd79ed6…`, cited_in=7)<br>« Bowker 1996 — History of Information Infrastructures » (`f420ad44…`, cited_in=6) | « Bowker 1996 — History of Information Infrastructures » |
| 18 | BRITO B Y Jerry et CASTILLO Andrea, 2013, « Bitcoin A Primer for Policymakers », Mercatus … | « Brito & Castillo 2013 — Bitcoin: A Primer for Policymakers » (`d55f8993…`, cited_in=2)<br>« Brito et Castillo 2013 » (`7dd91d45…`, cited_in=1) | « Brito & Castillo 2013 — Bitcoin: A Primer for Policymakers » |
| 19 | BUTERIN Vitalik, 2017a, « The very earliest versions of ETH protocol were a counterparty -… | « Buterin 2017 » (`c0f588f7…`, cited_in=4)<br>« Buterin 2017a — On settlement finality (OP_RETURN) » (`7dc37a6c…`, cited_in=1) | « Buterin 2017a — On settlement finality (OP_RETURN) » |
| 20 | BUTERIN Vitalik, 2014j, « Ethereum: A Next -Generation Cryptocurrency and Decentralized Ap… | « Buterin 2014j — A next-generation smart contract and decentralized application platform » (`48d2ab7c…`, cited_in=1)<br>« Buterin 2014j — On altcoins limits » (`280036a1…`, cited_in=1) | « Buterin 2014j — A next-generation smart contract and decentralized application platform » |
| 21 | BUTERIN Vitalik, 2013a, « Ethereum: The Ultimate Smart Contract and Decentralized Applicat… | « Buterin 2013 Ethereum Whitepaper » (`12c586ca…`, cited_in=4)<br>« Buterin 2013a » (`7be95456…`, cited_in=1) | « Buterin 2013 Ethereum Whitepaper » |
| 22 | BUTERIN Vitalik, 2013b, « Mastercoin: A Second-Generation Protocol on the Bitcoin Blockcha… | « Buterin 2013b » (`876698e2…`, cited_in=1)<br>« Buterin 2013b — Mastercoin: A Second-Generation Protocol » (`da969e43…`, cited_in=1) | « Buterin 2013b — Mastercoin: A Second-Generation Protocol » |
| 23 | BUTERIN Vitalik, 2013c, « The Bitcoin Gambling Diaspora », https://bitcoinmagazine.com/art… | « Buterin 2013c » (`31a81419…`, cited_in=1)<br>« Buterin 2013c — Bootstrapping a decentralized autonomous corporation (gambling diaspora) » (`50f03e74…`, cited_in=1) | « Buterin 2013c — Bootstrapping a decentralized autonomous corporation (gambling diaspora) » |
| 24 | BUTERIN Vitalik, 2013e, « Dagger: A Memory-Hard to Compute, Memory -Easy to Verify Scrypt … | « Buterin 2013e » (`3ceaf75a…`, cited_in=1)<br>« Buterin 2013e — Dagger: A memory-hard proof of work algorithm » (`4412476d…`, cited_in=5) | « Buterin 2013e — Dagger: A memory-hard proof of work algorithm » |
| 25 | CARTELIER Jean, 1996, La monnaie, Dominos. Flammarion, Paris, 125 p.… | « Cartelier 1996 La monnaie » (`a8810712…`, cited_in=6)<br>« Cartelier 1996 — La monnaie » (`2165a0e1…`, cited_in=5)<br>« Cartelier 1996 (Intro) » (`a1c09792…`, cited_in=4) | « Cartelier 1996 — La monnaie » |
| 26 | CASTILLO Michael del, 2013, « Dark Wallet: A Radical Way to Bitcoin », https://www.newyork… | « Castillo 2013 » (`81049b38…`, cited_in=4)<br>« Castillo 2013 — Dark Wallet and Amir Taaki anarchist Bitcoin » (`7a1b6b2b…`, cited_in=4) | « Castillo 2013 — Dark Wallet and Amir Taaki anarchist Bitcoin » |
| 27 | CHAINALYSIS TEAM, 2019, « Chainalysis Crypto Crime Report (2019) », https://go.chainalysis… | « Chainalysis Team 2019 » (`0e225413…`, cited_in=1)<br>« Chainalysis Team 2019 — Crypto Crime Report » (`2e155d6c…`, cited_in=0) | « Chainalysis Team 2019 — Crypto Crime Report » |
| 28 | DASHJR Luke, 2019, « CVE-2018–20587 Advisory and Full Disclosure (Bitcoin Core & Knots, on… | « Dashjr 2019 CVE History » (`45c4a100…`, cited_in=4)<br>« Dashjr 2019 — CVE-2018-20587 Advisory » (`713a81a4…`, cited_in=3) | « Dashjr 2019 — CVE-2018-20587 Advisory » |
| 29 | DE FILIPPI Primavera, 2013, « Bitcoin: a regulatory nightmare to a libertarian dream », In… | « De Filippi 2013 — Bitcoin: a regulatory nightmare to a libertarian dream » (`5febe612…`, cited_in=2)<br>« De Filippi 2013 » (`0b7bd88a…`, cited_in=1) | « De Filippi 2013 — Bitcoin: a regulatory nightmare to a libertarian dream » |
| 30 | DE FILIPPI Primavera et LOVELUCK Benjamin, 2016, « The invisible politics of Bitcoin: gove… | « De Filippi & Loveluck 2016 — Invisible politics of Bitcoin » (`ceabad5e…`, cited_in=5)<br>« De Filippi et Loveluck 2016 (Intro) » (`6cf3e50b…`, cited_in=1) | « De Filippi & Loveluck 2016 — Invisible politics of Bitcoin » |
| 31 | DENARDIS Laura et MUSIANI Francesca, 2014, « Governance by Infrastructure: Introduction, “… | « DeNardis et Musiani 2014 » (`2272e5b8…`, cited_in=4)<br>« DeNardis & Musiani 2014 — Governance by Infrastructure » (`e0b40d91…`, cited_in=1) | « DeNardis & Musiani 2014 — Governance by Infrastructure » |
| 32 | DODD Nigel, 2017, « The Social Life of Bitcoin », Theory, Culture & Society, 2017, p. 1‑27… | « Dodd 2017 Social Life Bitcoin » (`a03d6533…`, cited_in=7)<br>« Dodd 2017 — The Social Life of Bitcoin » (`cde365ff…`, cited_in=7)<br>« Dodd 2017 (Intro) » (`47b8d7b7…`, cited_in=5) | « Dodd 2017 — The Social Life of Bitcoin » |
| 33 | DUPONT Quinn, 2018, « 8. Experiments in algorithmic governance: A history and ethnography … | « DuPont 2018 DAO Experiment » (`3199c265…`, cited_in=6)<br>« Dupont 2018 — DAO Experiments in algorithmic governance » (`4137356d…`, cited_in=4) | « Dupont 2018 — DAO Experiments in algorithmic governance » |
| 34 | DUPRÉ Denis, PONSOT Jean-François et SERVET Jean-Michel, 2015, « Le bitcoin contre la révo… | « Dupre Ponsot Servet 2015 » (`38639c7e…`, cited_in=1)<br>« Dupré Ponsot Servet 2015 — Bitcoin contre la révolution des communs » (`1716ed6b…`, cited_in=3)<br>« Dupré, Ponsot et Servet 2015 » (`67f3f453…`, cited_in=4) | « Dupré Ponsot Servet 2015 — Bitcoin contre la révolution des communs » |
| 35 | EDWARDS Paul, BOWKER Geoffrey, JACKSON Steven et WILLIAMS Robin, 2009, « Introduction: An … | « Edwards et al. 2009 » (`c14637f5…`, cited_in=7)<br>« Edwards et al. 2009 — Agenda for Infrastructure Studies » (`2c3733ba…`, cited_in=7) | « Edwards et al. 2009 — Agenda for Infrastructure Studies » |
| 36 | EUROPEAN CENTRAL BANK, 2012, Virtual Currency Scheme, s.l.… | « European Central Bank 2012 » (`117c1b4f…`, cited_in=3)<br>« BCE 2012 — Virtual Currency Schemes » (`896f386e…`, cited_in=1)<br>« BCE 2012b — Virtual Currency Schemes (original report) » (`443e78b5…`, cited_in=3) | « BCE 2012 — Virtual Currency Schemes » |
| 37 | FRIEDMAN Benjamin M., 2008, « Quels doivent être les objectifs de la politique monétaire. … | « Friedman Benjamin M. 2008 — Les objectifs de la politique monétaire » (`d49e7200…`, cited_in=4)<br>« Friedman 2008 » (`cfc5ccfe…`, cited_in=3) | « Friedman Benjamin M. 2008 — Les objectifs de la politique monétaire » |
| 38 | FRIEDMAN Milton., 1999, “Land value tax and internet currencies ”, interview with Nobel La… | « Friedman Milton 1999 — Interview sur internet et monnaies privées » (`a7683381…`, cited_in=2)<br>« Friedman Milton 1999 — Video interview on internet and private currencies (land value tax) » (`8a86eb7f…`, cited_in=2) | « Friedman Milton 1999 — Video interview on internet and private currencies (land value tax) » |
| 39 | GALBRAITH John Kenneth, 1976, L’argent, Paris, Gallimard . (coll. « idée, Gallimard »), co… | « Galbraith 1976 » (`ecfda0e5…`, cited_in=6)<br>« Galbraith 1976 — L'argent » (`569ea730…`, cited_in=6) | « Galbraith 1976 — L'argent » |
| 40 | GARZIK Jeff, 2014a, « [ANN][XCP] Counterparty - Pioneering Peer -to-Peer Finance - Officia… | « Garzik 2014a » (`644de7a8…`, cited_in=1)<br>« Garzik 2014a — Counterparty and metacoins analysis » (`9e20ed50…`, cited_in=1) | « Garzik 2014a — Counterparty and metacoins analysis » |
| 41 | GARZIK Jeff, 2014b, « [Bitcoin-development] On OP_RETURN in upcoming 0.9 release ».… | « Garzik 2014b » (`fdafe6e1…`, cited_in=1)<br>« Garzik 2014b — OP_RETURN and metadata in Bitcoin » (`a7d3cc7c…`, cited_in=5) | « Garzik 2014b — OP_RETURN and metadata in Bitcoin » |
| 42 | GILBERT David, 2014, « \’Most Valuable Tweet in History\’ Donates $11,000 Worth of Dogecoi… | « David Gilbert 2014 » (`be56089c…`, cited_in=1)<br>« Gilbert David 2014 — Dogecoin cryptocurrency community » (`1d8a4c4a…`, cited_in=2) | « Gilbert David 2014 — Dogecoin cryptocurrency community » |
| 43 | HUGHES Eric, 1993, « A Cypherpunk’s Manifesto », https://www.activism.net/cypherpunk/manif… | « Hughes 1993 Cypherpunk Manifesto » (`51061825…`, cited_in=3)<br>« Hughes 1993 — A Cypherpunk's Manifesto » (`c76bb3ae…`, cited_in=3) | « Hughes 1993 — A Cypherpunk's Manifesto » |
| 44 | JEONG Sarah, 2013, « The Bitcoin Protocol as Law, and the Politics of a Stateless Currency… | « Jeong 2013 — The Bitcoin Protocol as Law » (`ba4fb228…`, cited_in=5)<br>« Jeong 2013 » (`17498d46…`, cited_in=4) | « Jeong 2013 — The Bitcoin Protocol as Law » |
| 45 | KAVANAGH Donncha et MISCIONE Gianluca, 2017, « Infrastructures and Their Invisible Carniva… | « Kavanagh & Miscione 2017 » (`6d3ccfa0…`, cited_in=7)<br>« Kavanagh et Miscione 2017 » (`2986a9e1…`, cited_in=3) | « Kavanagh & Miscione 2017 » |
| 46 | KING Sunny et NADAL Scott, 2012, « PPCoin: Peer-to-Peer Crypto-Currency with Proof-of-Stak… | « King & Nadal 2012 Peercoin » (`b9b474c9…`, cited_in=3)<br>« Sunny King et Nadal 2012 » (`8ba11b69…`, cited_in=1)<br>« King Nadal 2012 — PPCoin Peer-to-Peer Crypto-Currency » (`6649a875…`, cited_in=2) | « King & Nadal 2012 Peercoin » |
| 47 | KNAPP G F, 1924, « The state theory of money », History of Economic Thought Books, 1924.… | « Knapp 1924 State Theory Money » (`4e7c7974…`, cited_in=5)<br>« Knapp 1924 — The State Theory of Money » (`573d8b42…`, cited_in=4)<br>« Knapp 1924 » (`db4e7b89…`, cited_in=3) | « Knapp 1924 — The State Theory of Money » |
| 48 | LARS Ludovic, 2021, « Bitcoin, quand la révolution de la monnaie vire à la religion », htt… | « Lars 2021 — Bitcoin and religious metaphors (bitcoin-histoire.fr) » (`32f91ac4…`, cited_in=6)<br>« Lars 2021 » (`c1ebf64c…`, cited_in=2) | « Lars 2021 — Bitcoin and religious metaphors (bitcoin-histoire.fr) » |
| 49 | LARS Ludovic, 2019a, « Des jetons sur Bitcoin : colored coins et autres procédés », https:… | « Lars 2019a » (`e318cea2…`, cited_in=1)<br>« Lars 2019a — Colored Coins: early tokenization on Bitcoin » (`8add087a…`, cited_in=5) | « Lars 2019a — Colored Coins: early tokenization on Bitcoin » |
| 50 | LEE Charli, 2011, « Lite Coin White Paper », 7 octobre 2011, 6 p.… | « Charli Lee 2011 » (`6c31f72f…`, cited_in=1)<br>« Lee 2011 — Litecoin launch announcement » (`fa4fa618…`, cited_in=3) | « Charli Lee 2011 » |
| 51 | LOPP Jameson, 2021, « A History of Bitcoin Transaction Dust & Spam Storms », https://blog.… | « Lopp 2021 Spam Storms » (`78aaaaee…`, cited_in=7)<br>« Lopp 2021 — History Bitcoin Transaction Dust Spam Storms » (`a4a15c4d…`, cited_in=6) | « Lopp 2021 — History Bitcoin Transaction Dust Spam Storms » |
| 52 | LOPP Jameson, 2018, « Who Controls Bitcoin Core? », Medium, https://medium.com/@lopp/who- … | « Lopp 2018 GitHub Bitcoin Core » (`304579e3…`, cited_in=6)<br>« Lopp 2018 — Who Controls Bitcoin Core » (`b95feb4b…`, cited_in=6) | « Lopp 2018 — Who Controls Bitcoin Core » |
| 53 | LUSTIG Caitlin et NARDI Bonnie, 2015, « Algorithmic authority: The case of Bitcoin », Proc… | « Lustig & Nardi 2015 Algorithmic Authority » (`6c21ae38…`, cited_in=3)<br>« Lustig & Nardi 2015 — Algorithmic authority Bitcoin » (`59cad7f5…`, cited_in=4) | « Lustig & Nardi 2015 — Algorithmic authority Bitcoin » |
| 54 | MAUSS Marcel, 1914, « Les origines de la notion de monnaie » dans Oeuvres 2. Représentatio… | « Mauss 1914 — Les origines de la notion de monnaie » (`ff9f99ae…`, cited_in=4)<br>« Mauss 1914 » (`73ec82f5…`, cited_in=3) | « Mauss 1914 — Les origines de la notion de monnaie » |
| 55 | MÖSER Malte et BÖHME Rainer, 2015, « Trends, Tips, Tolls: A Longitudinal Study of Bitcoin … | « Moser et Bohme 2015 » (`51cd9218…`, cited_in=2)<br>« Möser & Böhme 2015 — Towards Bitcoin payment networks » (`8a6aba8e…`, cited_in=6) | « Möser & Böhme 2015 — Towards Bitcoin payment networks » |
| 56 | MUSIANI Francesca, MALLARD Alexandre et MÉADEL Cécile, 2018, « 7 Governing what wasn’t mea… | « Musiani 2018 CM Gouvernance » (`11ca4986…`, cited_in=3)<br>« Musiani Mallard Meadel 2018 » (`ad474c17…`, cited_in=2)<br>« Musiani Mallard Méadel 2018 — Governing what wasn't meant to be governed » (`9d026d51…`, cited_in=3) | « Musiani Mallard Méadel 2018 — Governing what wasn't meant to be governed » |
| 57 | NAKAMOTO Satoshi, 2008c, « Bitcoin: A Peer -to-Peer Electronic Cash System », https://bitc… | « Nakamoto 2008 Bitcoin WP » (`45106324…`, cited_in=11)<br>« Nakamoto 2008c — Bitcoin: A Peer-to-Peer Electronic Cash System » (`e324660d…`, cited_in=5) | « Nakamoto 2008c — Bitcoin: A Peer-to-Peer Electronic Cash System » |
| 58 | NARAYANAN Arvind et CLARK Jeremy, 2017, « Bitcoin’s academic pedigree », Communications of… | « Narayanan & Clark 2017 » (`c5391132…`, cited_in=5)<br>« Narayanan et Clark 2017 » (`d41e873a…`, cited_in=5) | « Narayanan & Clark 2017 » |
| 59 | ORLÉAN André, 1998, « La monnaie autoréférentielle: reflexion sur les évolution monétaire … | « Orleans 1998 La monnaie entre violence et confiance » (`2ae1182d…`, cited_in=1)<br>« Orléan 1998 — La monnaie autoréférentielle » (`206ffb42…`, cited_in=8)<br>« Orléan 1998 » (`a9340f8c…`, cited_in=6) | « Orléan 1998 — La monnaie autoréférentielle » |
| 60 | OSTROM Elinor, 1990, Governing the Commons, New York, Cambridge University Press, 1990.… | « Ostrom 1990 » (`e3b7d915…`, cited_in=3)<br>« Ostrom 1990 — Governing the Commons » (`b86c5ec8…`, cited_in=3) | « Ostrom 1990 — Governing the Commons » |
| 61 | POLANYI Karl, 2011, La subsistance de l’homme : La place de l’économie dans l’histoire et … | « Polanyi 2011 — La subsistance de l'homme » (`24d1f1fe…`, cited_in=5)<br>« Polanyi 2011 » (`d59d4daf…`, cited_in=4) | « Polanyi 2011 — La subsistance de l'homme » |
| 62 | POLANYI Karl, 1944, La grande transformation : aux origines politiques et économiques de n… | « Polanyi 1944 / 2011 » (`f4bf1b02…`, cited_in=3)<br>« Polanyi 1944 — La grande transformation » (`1782b07f…`, cited_in=2) | « Polanyi 1944 — La grande transformation » |
| 63 | POULIOT Francis, 2018, « Catallaxy: the origins of Bitcoin and innovation », https://mediu… | « Pouliot 2018 — Bitcoin: l'histoire cachée » (`c7bab4b2…`, cited_in=7)<br>« Pouliot 2018 » (`a605c562…`, cited_in=3) | « Pouliot 2018 — Bitcoin: l'histoire cachée » |
| 64 | RANDALL WRAY L, 2010, « Alternative Approaches to Money », Theoretical Inquiries in Law, 2… | « Randall Wray 2010 — Modern Monetary Theory and the origins of money » (`9014e9b2…`, cited_in=1)<br>« Wray 2010 » (`7ebabc5d…`, cited_in=3) | « Randall Wray 2010 — Modern Monetary Theory and the origins of money » |
| 65 | RASKIN Max et YERMACK David, 2016, « Digital currencies, decentralized ledgers, and the fu… | « Raskin & Yermack 2016 — Digital currencies, decentralized ledgers, and the future of central banking » (`4f8f09e6…`, cited_in=3)<br>« Raskin et Yermack 2016 » (`a97e6731…`, cited_in=2) | « Raskin & Yermack 2016 — Digital currencies, decentralized ledgers, and the future of central banking » |
| 66 | RAUCHS Michel, 2016, « Cryptocurrencies meeting business ecosystems : the case of bitcoin … | « Rauchs 2016 » (`4ed01f75…`, cited_in=4)<br>« Rauchs 2016 — Cryptocurrencies meeting business ecosystems » (`9531cc48…`, cited_in=3) | « Rauchs 2016 — Cryptocurrencies meeting business ecosystems » |
| 67 | RAUCHS Michel, GLIDDEN Andrew, GORDON Brian, PIETERS Gina, RECANATINI Martino, ROSTAND Fra… | « Rauchs et al. 2018 » (`9984b392…`, cited_in=7)<br>« Rauchs et al. 2018 — Distributed Ledger Systems Conceptual Framework » (`c9045960…`, cited_in=7) | « Rauchs et al. 2018 — Distributed Ledger Systems Conceptual Framework » |
| 68 | REDMAN Jamie, 2019b, « The “Wrapped Bitcoin ” Project Has Now Officially Launched on Ether… | « Redman 2019b » (`db27994d…`, cited_in=1)<br>« Redman 2019b — Wrapped Bitcoin (WBTC) launch on Ethereum » (`6e2f338b…`, cited_in=5) | « Redman 2019b — Wrapped Bitcoin (WBTC) launch on Ethereum » |
| 69 | ROLLAND Maël et SLIM Assen, 2017, « Économie politique du Bitcoin : l’institutionnalisatio… | « Rolland & Slim 2017 » (`0ea689b1…`, cited_in=4)<br>« Rolland & Slim 2017 — Économie politique du Bitcoin » (`708e681a…`, cited_in=8) | « Rolland & Slim 2017 — Économie politique du Bitcoin » |
| 70 | ROSENFELD Meni, 2012, « Overview of Colored Coins », https://allquantor.at/blockchainbib/p… | « Rosenfeld 2012 » (`3737dd82…`, cited_in=1)<br>« Rosenfeld 2012 — Colored Coins » (`b911a98b…`, cited_in=1) | « Rosenfeld 2012 — Colored Coins » |
| 71 | RUSSO Camila, 2020, The Infinite Machine: How an Army of Crypto -Hackers Is Building the N… | « Russo 2020 Infinite Machine » (`e70690b6…`, cited_in=7)<br>« Russo 2020 — The Infinite Machine Ethereum » (`bcb6224c…`, cited_in=7) | « Russo 2020 — The Infinite Machine Ethereum » |
| 72 | SELGIN George, 2013, « Quasi-Commodity Money », SSRN Electronic Journal, 10 avril 2013.… | « Selgin 2013 Synthetic Commodity Money » (`adc1a4d0…`, cited_in=5)<br>« Selgin 2013 — Quasi-Commodity Money » (`5680ab9e…`, cited_in=4) | « Selgin 2013 — Quasi-Commodity Money » |
| 73 | SERVET Jean Michel et DUFRÊNE Nicolas, 2021, « Le bitcoin devient un danger pour le systèm… | « Servet Dufresne 2021 » (`1f8cc3ad…`, cited_in=1)<br>« Servet & Dufrêne 2021 — Monnaie et société numérique » (`a6d5a701…`, cited_in=1) | « Servet Dufresne 2021 » |
| 74 | SHIN Laura, 2022, The Cryptopians: Idealism, Greed, Lies, and the Making of the First Big … | « Shin 2022 Cryptopians » (`2461f0fb…`, cited_in=7)<br>« Shin 2022 — The Cryptopians » (`89e4b248…`, cited_in=6) | « Shin 2022 — The Cryptopians » |
| 75 | STAR Susan Leigh, 1999, « Ethnography of infrastructure », American Behavioral Scientist ,… | « Star 1999 Ethnography Infrastructure » (`f9dffa75…`, cited_in=8)<br>« Star 1999 — Ethnography of Infrastructure » (`e054a841…`, cited_in=9) | « Star 1999 — Ethnography of Infrastructure » |
| 76 | STAR Susan Leigh et RUHLEDER, K aren. (2010) . « Vers une écologie de l'infrastructure Con… | « Star & Ruhleder 2010 » (`940fa052…`, cited_in=3)<br>« Star & Ruhleder 2010 — Vers une écologie de l'infrastructure » (`a5f0ee04…`, cited_in=2) | « Star & Ruhleder 2010 — Vers une écologie de l'infrastructure » |
| 77 | THÉRET Bruno, 2008, « Les trois états de la monnaie », Revue économique, 2008, vol. 59, no… | « Theret 2008 Etats de la monnaie » (`a5deed89…`, cited_in=6)<br>« Théret 2008 — Les trois états de la monnaie » (`22c9a993…`, cited_in=7) | « Théret 2008 — Les trois états de la monnaie » |
| 78 | TIROLE Jean, 2017, « There are many reasons to be cautious about bitcoin », https://www.ft… | « Tirole 2017 Enigma Bitcoin » (`f1923475…`, cited_in=5)<br>« Tirole 2017 — Many reasons to be cautious about bitcoin » (`2f1fca7a…`, cited_in=4) | « Tirole 2017 — Many reasons to be cautious about bitcoin » |
| 79 | VERGNE Jean Philippe et SWAIN Gautam, 2017, « Categorical Anarchy in the U.K. The British … | « Vergne & Swain 2017 Anarchic Categories » (`354839e9…`, cited_in=1)<br>« Vergne & Swain 2017 — Categorical Anarchy Bitcoin British Media » (`b84ba933…`, cited_in=2) | « Vergne & Swain 2017 — Categorical Anarchy Bitcoin British Media » |
| 80 | VON MISES Ludwig, 1912, The theory of money and credit, New Haven, Yale University Press, … | « Von Mises 1912 — The Theory of Money and Credit » (`aa7f6593…`, cited_in=1)<br>« Von Mises 1912 » (`74866215…`, cited_in=1) | « Von Mises 1912 — The Theory of Money and Credit » |
| 81 | WALCH Angela, 2017a, « The Path of the Blockchain Lexicon (and the Law) », 36 Rev. Banking… | « Walch 2017a — Path of the Blockchain Lexicon » (`21d453b1…`, cited_in=3)<br>« Walch 2017 » (`d24f408b…`, cited_in=3) | « Walch 2017a — Path of the Blockchain Lexicon » |
| 82 | WALCH Angela, 2017b, « Open Source Operational Risk : Should Public Blockchains Serve as F… | « Walch 2017 Governance Blockchain » (`9d1b623c…`, cited_in=4)<br>« Walch 2017b — Open Source Operational Risk Blockchains » (`8640638b…`, cited_in=2) | « Walch 2017b — Open Source Operational Risk Blockchains » |
| 83 | WILCKE Jeffrey, 2016, « To Fork or not to Fork », https://blog.ethereum.org/2016/07/15/to-… | « Wilcke 2016 Hard Fork » (`5b4b67bb…`, cited_in=3)<br>« Wilcke 2016 — To Fork or not to Fork » (`b4c29d75…`, cited_in=2) | « Wilcke 2016 — To Fork or not to Fork » |
| 84 | WIRDUM Aaron van, 2019, « Stratum V2 Could Overhaul Pooled Bitcoin Mining », Bitcoin Magaz… | « Wirdum 2019 » (`e57bb736…`, cited_in=3)<br>« Van Wirdum 2019 — Stratum V2: next generation mining protocol » (`e000d518…`, cited_in=2) | « Van Wirdum 2019 — Stratum V2: next generation mining protocol » |
| 85 | WIRDUM Aaron van, 2014, « Why Bitcoin Really Does Represent the Democratization of Money »… | « Van Wirdum 2014 — The democratization of finance through Bitcoin » (`eee5305b…`, cited_in=5)<br>« Wirdum 2014 » (`dd5827d0…`, cited_in=1) | « Van Wirdum 2014 — The democratization of finance through Bitcoin » |
| 86 | WOOD Gavin, 2014b, « “Yellow paper” : Ethereum: A Secure Decentralised Generalised Transac… | « Wood 2014 Yellow Paper » (`462ca3c2…`, cited_in=4)<br>« Yellow Paper (Ethereum, Gavin Wood 2014) » (`4d5634d4…`, cited_in=5) | « Wood 2014 Yellow Paper » |
| 87 | YERMACK David, 2013, « Is bitcoin a real currency? An economic appraisal », National Burea… | « Yermack 2013 Real Currency » (`0dca90d7…`, cited_in=2)<br>« Yermack 2013 — Is Bitcoin a real currency » (`cd4ebb49…`, cited_in=2) | « Yermack 2013 — Is Bitcoin a real currency » |
| 88 | ZELIZER Viviana A ., 1989, « The Social Meaning of Money : “Special Monies” », The America… | « Zelizer 1989 » (`c89bf937…`, cited_in=4)<br>« Zelizer 1989 — Social Meaning of Money Special Monies » (`bc136198…`, cited_in=4) | « Zelizer 1989 — Social Meaning of Money Special Monies » |
| 89 | « Bitcoin ‘Ought to Be Outlawed,’ Nobel Prize Winner Stiglitz Says - Bloomberg », 29 novem… | « Stiglitz 2017 — Bitcoin ought to be outlawed (Bloomberg) » (`9aa951e4…`, cited_in=4)<br>« Stiglitz 2017 » (`e030d16a…`, cited_in=3) | « Stiglitz 2017 — Bitcoin ought to be outlawed (Bloomberg) » |

Réserves d'appariement à vérifier avant toute fusion :
- famille Buterin 2017a : le nœud « Buterin 2017a — On settlement finality (OP_RETURN) » porte un titre qui ne recoupe pas l'entrée 2017a du PDF (tweet « very earliest versions of ETH… ») ;
- famille Buterin 2014j : « On altcoins limits » vs « next-generation … platform » — deux textes possibles derrière le même suffixe ;
- ECB : les suffixes 2015a/2015b du graphe **contredisent** ceux du PDF (« ECB 2015a — a further analysis » décrit l'œuvre que le PDF indexe 2015b) ; l'appariement au niveau lettre est donc incertain pour cette famille ;
- famille « Orléan 1998 » : le nœud « Orleans 1998 La monnaie entre violence et confiance » mélange le titre d'Aglietta & Orléan (2002) avec le millésime 1998 — probablement un doublon *mal étiqueté* plutôt qu'une simple variante.

## 3. Fiches d'auteur sans millésime (étape 3, périmètre du patch)

**43 fiches** (et non 48) : nœuds typés `Reference`, sans millésime, au nom d'une personne — jamais citables en (auteur, année). Les 6 autres nœuds sans millésime ne sont pas des fiches d'auteur : « Bit2Me Academy — … » (×2), « Bitcoin Wiki — Common Vulnerabilities… », « Bitcoin.fr — Histoire de Bitcoin », « EthHub — Ethereum monetary policy » (ces trois derniers correspondent aux entrées *sans date* du PDF) et « The General Theory of Employment, Interest and Money » (titre seul, `AcademicWork`, sans entrée Keynes au PDF).

`patch_18_bibliography_fixes.json` retype **39** fiches `Reference` → `Person` (id du type `Person` : `ed738791205548e4b4c187c58be227dc`), après vérification d'absence d'homonyme `Person` dans v109. **4 fiches sont exclues du patch** (fusion/arbitrage, listées aussi dans `_meta.skipped`) :

| Fiche exclue | Motif |
|---|---|
| « Martti Malmi (Sirius) » | l'entité `Person` « Martti Malmi » existe déjà — fusion à arbitrer |
| « Marco Corallo » | l'entité `Person` « Matt Corallo » existe (même patronyme ; « Marco » est vraisemblablement une erreur pour Matt Corallo) — fusion à arbitrer |
| « Desmedt et Lakomski-Laguerre » | fiche à **deux** auteurs ; « Mathieu Desmedt » et « Odile Lakomski-Laguerre » existent déjà en `Person` — arbitrage (NB : le co-auteur de Lakomski-Laguerre dans la littérature monétaire est Ludovic Desmedt ; le prénom « Mathieu » du nœud `Person` est lui-même douteux) |
| « De Boyer des Roches et Rosales » | fiche à **deux** auteurs — ne peut pas devenir une entité `Person` unique |

Le patch contient aussi l'unique `SET_NAME` : « Danzeis et Meiklejohn 2015 » → « Danezis et Meiklejohn 2015 » (`05338358f9d7485dbef4110be604c4f8`). L'attribut `author` (« Danzeis Meiklejohn ») porte la même coquille et n'est pas touché ; et l'entrée est de toute façon **absente du PDF** (§ 2.a).

## 4. Ce qui n'a pas pu être établi

- La **liste nominative des « 17 jamais cités »** et des « ~74 familles » de l'audit précédent : introuvable dans le dépôt, non reproductible ; seuls mes recomptages (11 ; 89) sont vérifiables ici.
- L'**appariement fin au niveau des suffixes** a/b/c pour quelques familles où le graphe et le PDF numérotent différemment (ECB 2015, Buterin 2016–2017) : l'appariement par famille (auteur, année) est sûr, la lettre ne l'est pas.
- Le **statut réel des 33 nœuds datés absents** : absents de la *bibliographie*, mais je n'ai pas vérifié s'ils sont mobilisés dans le corps de la thèse (`assets/MD/`) sans être bibliographiés — ce tri (parasite vs référence omise par la bibliographie du PDF) demande une passe texte dédiée.
- La conversion repose sur l'extraction pypdf : la ponctuation fine (espaces insécables, tirets de justification « Sharding -Based ») reflète l'extraction, pas la mise en page originale ; le **compte de 652 entrées** dépend du découpage documenté ci-dessus (12 cas limites arbitrés à la main).
