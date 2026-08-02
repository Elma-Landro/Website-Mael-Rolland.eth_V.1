# 03 — Appariement CSV × graphe, et sa vérification adverse

**Date** : 2026-08-02
**Mécanisme** : `scripts/match_chronology_events.py`
**Sorties** : `docs/audits/data/chronology-events-classification.csv` (mécanique), `docs/audits/data/chronology-events-arbitration.csv` (vérification)
**Mode agent** : A

## Le résultat qui compte

**Le mécanisme lexical s'est trompé dans 10 cas sur 12.** C'est le principal enseignement de ce chantier, et il conditionne la confiance à accorder au reste.

La première version du script comparait chaque ligne du CSV aux seuls 213 `InfrastructureEvent` et `CrisisEvent`, par similarité de libellé et compatibilité de date. Elle a produit 12 `CONFIRMED_MISSING`. Une passe adverse — dont la consigne était de **réfuter** chaque candidat, en tenant l'ajout d'un doublon pour plus coûteux qu'une omission — en a invalidé dix.

## Les quatre modes de défaillance

### 1. La barrière de langue

Le CSV est en français non accentué, le graphe est bilingue. « Enregistrement de genèse » et « Genesis Block / lancement du protocole » désignent le même fait, à la même date, sans partager un seul token.

### 2. L'acronyme développé

« Comité interprofessionnel DATA créé » contre « Digital Asset Transfer Authority (juillet 2013) ». L'acronyme du CSV est développé dans le graphe ; sa description contient littéralement « Comité interprofessionnel créé en juillet 2013 ». Aucune similarité de surface.

### 3. La variation typographique

« BIP16 » contre « BIP 16 ». **Un espace suffisait à faire échouer l'appariement.** Corrigé par une ancre « préfixe + numéro » recollée, qui normalise les deux formes vers `BIP16`.

### 4. Le fait porté par un autre type — le mode dominant

C'est la cause majoritaire. **Sept candidats sur douze existaient dans le graphe sous un type non événementiel** : `PriceWindow` pour les paliers de cours, `Concept` pour les régimes transactionnels, `Reference` pour les livres blancs, `Organization` et `MediaOutlet` pour les entreprises, et jusqu'à une simple **valeur d'attribut** pour la PR 9049.

Ne comparer qu'aux événements revenait à déclarer manquant ce qui était présent ailleurs.

## Ce que le mécanisme fait maintenant

Deux index, pas un :

1. **les 213 événements** — cibles d'un ajout éventuel ;
2. **les 2 263 entités, tous types confondus** — pour détecter une couverture hors typage événementiel, en indexant **nom *et* description** (c'est la description qui rattrape le cas DATA).

Trois signaux, jamais un score unique : similarité de libellé (Jaccard hors mots-vides), compatibilité de date (emboîtement des précisions, ou même année), et ancres distinctives (noms propres, casse interne type `MtGox`, acronymes, identifiants numériques, « préfixe + numéro »). Une ancre partagée pèse autant qu'un fort recouvrement lexical ; une date contradictoire la tempère.

S'y ajoute la prise en compte des réserves `[CHANTIER]` que le CSV déclare lui-même : une ligne dont le catalogue dit que la date n'est pas établie ne satisfait pas le critère « suffisamment datée » et tombe en `TOO_AMBIGUOUS`. C'est ce qui a écarté E025.

### Classification après correction

| Statut | Lignes |
|---|---:|
| `ALREADY_IN_GRAPH` | 61 |
| `POSSIBLE_DUPLICATE` | 13 |
| `CONFIRMED_MISSING` | 3 |
| `TOO_AMBIGUOUS` | 1 |

Le mécanisme corrigé reste imparfait — ses 3 `CONFIRMED_MISSING` résiduels (E038, E051, E074) sont tous réfutés par la vérification. **Un appariement lexical ne remplace pas un jugement.** Il sert à produire une liste de candidats courte et traçable ; c'est la vérification qui tranche, et les deux sont consignées séparément :

- `chronology-events-classification.csv` — sortie **mécanique**, rejouable, sans intervention ;
- `chronology-events-arbitration.csv` — **verdicts de vérification**, avec pour chaque ligne le type de couverture, l'entité couvrante et le motif.

Ce cloisonnement est délibéré : ajuster le mécanisme jusqu'à ce qu'il retombe sur les verdicts serait du surajustement, et ferait perdre la trace de ce qu'un procédé automatique sait et ne sait pas faire.

## Verdicts de la vérification — 19 lignes examinées

### Déjà présents comme événements — 5

| id | Entité du graphe |
|---|---|
| E003 | `InfrastructureEvent — Genesis Block / lancement du protocole` |
| E025 | `BIP-0001 : institutionnalisation…` **et** `Standardisation des propositions protocolaires (BIP)` — déjà en double |
| E044 | `BIP 16 : Pay-to-Script-Hash (avril 2012)` |
| E047 | `Digital Asset Transfer Authority (juillet 2013)` |
| E051 | `BIP-0042 — Bitcoin Fixed Monetary Supply` (`CrisisEvent`) |

### Présents sous un autre type — 8

| id | Type couvrant | Entité |
|---|---|---|
| E038 | `Concept` | Changement de régime transactionnel (phase de péché) — « culmine à 51 % » |
| E043 | `Concept` | Régime transactionnel de la phase de maturation — attribut `illegalShare` |
| E050 | `PriceWindow` | Pic décembre 2013 (~1000 $) |
| E074 | `PriceWindow` | Pic décembre 2017 (~20 000 $) |
| E076 | `PriceWindow` | Point bas 2018-2019 (~3300 $) |
| E078 | `PriceWindow` | Stabilisation 2019-2020 (~8000 $) |
| E060 | `Concept` | Narrative « blockchain sans Bitcoin » (2015) |
| E022 | `MediaOutlet` | Bitcoin Magazine, `founded: 2012` |

### Présents comme document ou organisation, absents comme événement — 3

| id | Type couvrant | Entité |
|---|---|---|
| E034 | `Organization` | Coinbase, `foundedYear: 2012` |
| E036 | `Reference` | Willett 2012 Mastercoin WP |
| E040 | `Reference` | Buterin 2013 Ethereum Whitepaper |

### Absents sous toute forme — 2

| id | Reste |
|---|---|
| E061 | une seule `Reference` bibliographique (Slacknation 2017) |
| E070 | rien — aucune entité n'atteste le franchissement des 1000 $ début 2017 |

### Un cas à part — E069

La chaîne « 9049 » **existe** dans le graphe, mais uniquement à l'intérieur de valeurs d'attribut : `inseminationPR: "PR #9049 (inadvertently introduced the bug)"`, porté par l'entité `Bitcoin CVE 2018-17144` et par la section III.1. Aucune recherche par nom ne pouvait la voir.

Le fait est donc **consigné mais non navigable** : pas de nœud, pas de date, aucune relation vers Corallo, vers le dépôt, ni vers une phase. Distinction décisive pour ce chantier — une chaîne dans un attribut n'est pas une entité interrogeable.

## Divergences de dates relevées, non tranchées

| id | Date CSV | Date graphe | Constat |
|---|---|---|---|
| **E044** | 2013-04 | **2012-04** | Le graphe a raison, source O'Brien 2014, corroboré par un `GovernanceProcess` bornant 2012-01 → 2012-04. Le CSV confond probablement avec l'adoption par BitGo en août 2013. |
| **E022** | 2011 | **2012** | Le graphe se contredit lui-même : le `MediaOutlet` et la référence Castillo 2013 disent 2012, l'entité `Person` Mihai Alisie dit 2011. La valeur sourcée est 2012. |
| **E040** | 2013 | — | Le CSV cite ch.I l.399 ; la l.**393** est plus précise : « fin novembre 2013 ». Date retenue pour l'ajout : `2013-11`. |

## Faux positifs évités, à signaler

Trois entités du graphe portent un « 51 % » qui désigne le **hashrate de Ghash.io en 2014**, sans aucun rapport avec les 51 % de transactions illicites de 2013 (E038). Deux autres identifiants hexadécimaux contiennent « 9049 » par hasard. Un appariement moins prudent les aurait confondus.
