# GRC-20 — Câblage de la phase de maturation

**Date** : 2026-08-02
**Graphe source** : `grc20-these-mael-rolland-v98.json`
**Graphe candidat** : `grc20-these-mael-rolland-v99.json`
**Branche** : `agent/grc20-wire-maturation-phase-v1`
**Mode agent** : C (patch appliqué à un graphe candidat, non fusionné)
**Patch** : `patch_12_wire_maturation_phase.json` — 37 relations, **aucune entité créée, modifiée ou supprimée**

## Le problème

Constat issu de `docs/audits/grc20-add-missing-events/05-final-synthesis.md` : la phase de maturation paraissait vide non parce qu'il lui manquait des événements, mais parce que ceux qui existaient n'étaient rattachés à aucune phase.

Arêtes `occurs in` vers les nœuds de phase, avant intervention :

| Cible | Type | Arêtes |
|---|---|---:|
| Phase de preuve de concept | `DevelopmentPhase` | 65 |
| Phase de péché | `DevelopmentPhase` | 46 |
| Phase de maturation / Phase 3 Bitcoin | `Concept` | 25 |
| **Phase de maturation** | **`DevelopmentPhase`** | **5** |

Toute vue organisée par phase montrait donc une maturation quasi vide, alors que les événements de la période étaient bien présents dans le graphe.

## Sur quel nœud câbler — la décision, et sa réserve

**Cible retenue : la `DevelopmentPhase` `eed0b89cd2e740718059c16591f9bfb7`.**

Motif : « preuve de concept » et « péché » sont toutes deux des `DevelopmentPhase`. Câbler la maturation sur la `DevelopmentPhase` homonyme est la seule façon de rendre les trois phases **comparables entre elles**. Câbler sur le `Concept` aurait laissé la `DevelopmentPhase` à 5 arêtes et maintenu l'asymétrie exactement là où elle gêne.

**Réserve à arbitrer, non tranchée ici** : le `Concept` « Phase de maturation / Phase 3 Bitcoin » (`645079ad66ee41b689112d383dd54798`) est un **doublon**. Il compte 25 usages et porte la périodisation (`dateRange: 01/11/2013 — 01/01/2020`), quand la `DevelopmentPhase` n'a aucune borne. Autrement dit, **le nœud le mieux typé n'est pas celui qui porte l'information, et inversement.** Le patch ne fusionne rien : la fusion des deux nœuds, et le transfert du `dateRange` vers la `DevelopmentPhase`, restent des décisions humaines. Après câblage, la répartition devient 42 contre 25 — le doublon reste visible et donc arbitrable.

## Critères de sélection

Est câblé tout événement qui remplit les quatre conditions :

1. typé `InfrastructureEvent` ou `CrisisEvent` ;
2. **non déjà rattaché à une phase**, quelle qu'elle soit — aucun événement ne reçoit un second rattachement ;
3. date normalisée comprise entre **2013-11** et **2020-12** ;
4. ce n'est pas un artefact de figure.

La borne basse `2013-11` n'est pas arbitraire : la `DevelopmentPhase` « Phase de péché » porte `dateRange: 01/04/2012 — 30/10/2013`, et le `Concept` de maturation porte `01/11/2013 — 01/01/2020`. Les deux se raccordent exactement.

## Résultat

**37 relations `occurs in` ajoutées.** Le graphe passe de 20 067 à 20 104 relations ; les 2 269 entités sont **strictement identiques** entre v98 et v99 (vérifié par comparaison directe).

| Cible | Avant | Après |
|---|---:|---:|
| Phase de preuve de concept | 65 | 65 |
| Phase de péché | 46 | 46 |
| **Phase de maturation (`DevelopmentPhase`)** | **5** | **42** |
| Phase de maturation (`Concept`, doublon) | 25 | 25 |

Les 37 rattachements couvrent 2013-12 → 2019-06 : crises protocolaires (CVE-2014-0160 Heartbleed, CVE-2018-17144, les soft forks BIP-65, BIP-66, BIP-148, SegWit), événements de marché et d'intermédiation (Binance, Coinbase 5 millions d'utilisateurs, BitGo, eBay/PayPal), matériel (Antminer S5 et S9), régulation (Chine 2013, France 2014), et Ethereum (Frontier, attaque de The DAO, Parity Multisig Freeze).

## 52 événements écartés, avec motif

| Motif | Nombre |
|---|---:|
| antérieur au 01/11/2013 — relève de « poc » ou « péché » | 30 |
| date absente — inclassable | 17 |
| année 2013 seule — indécidable entre péché et maturation | 3 |
| hors période de la thèse (2008-2020) | 2 |

Le détail ligne à ligne est dans `docs/audits/data/maturation-phase-wiring.csv`.

Trois cas méritent l'œil :

- **Les 3 « année 2013 seule »** — `CVE-2013-3220 (Netsplit BIP-0050)`, `Attaque DDoS MtGox (mai 2013)`, `Fermeture Silk Road par le FBI (octobre 2013)`. Leurs libellés indiquent mars, mai et octobre 2013 : ils relèvent tous de la **phase de péché**, pas de la maturation. Ils sont écartés ici parce que leur attribut `date` ne porte que l'année, et que le mécanisme refuse de déduire un mois depuis un libellé. **Ils sont câblables à « péché » dans un chantier suivant.**
- **Les 17 sans date** — leur rattachement suppose de leur en attribuer une, ce qui excède un patch de câblage.
- **Les 2 hors période** — `The Merge` (2022) et `Figure 5` (2024). Le second n'est d'ailleurs pas un événement mais un artefact de figure typé `InfrastructureEvent` : anomalie signalée, non corrigée.

## Une objection levée en chemin

Le `Concept` s'intitule « Phase de maturation / **Phase 3 Bitcoin** », ce qui laissait craindre une erreur de catégorie à y rattacher des événements Ethereum (Frontier, The DAO, Parity).

Vérification faite, **les phases sont déjà employées comme périodisation de l'écosystème entier**, pas du seul Bitcoin : Namecoin et RipplePay sont rattachés à « preuve de concept », Ripple Labs, Mastercoin et Kraken à « péché », Tether, CoinGecko, WBTC et une levée de fonds Ethereum à la maturation. Le suffixe « Phase 3 Bitcoin » est un artefact de nommage, pas une restriction de portée. Aucun obstacle, donc.

## Ce que ce chantier ne fait pas

- Il ne fusionne pas le doublon `DevelopmentPhase` / `Concept`.
- Il ne transfère aucun `dateRange`.
- Il ne câble pas la phase de péché (3 candidats identifiés).
- Il ne date aucun des 17 événements sans date.
- Il ne corrige pas l'artefact `Figure 5` typé `InfrastructureEvent`.
- Il ne modifie ni v97, ni v98, ni le runtime, ni aucune entité.
