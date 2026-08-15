# État de chantier — Dédoublonnage vérifié + patch GRC20 — 02/08/2026

## Mécanisme de vérification des doublons

Trois **vetos** (bloquants, aucune fusion possible) puis deux **confirmations** (il en faut au moins une). Décision par conjonction, jamais par score unique.

**Vetos**
1. `type_compatible` — deux entités de types différents (`InfrastructureEvent` vs `CrisisEvent`) ne fusionnent jamais.
2. `date_compatible` — deux dates renseignées qui se contredisent bloquent. Les précisions emboîtées (`2012-11` ⊂ `2012-11-28`) passent.
3. `ids_compatibles` — divergence de `cveId`, de `crisisNumber`, ou d'identifiants distinctifs extraits du libellé (acronymes 2–6 majuscules, nombres à 3–6 chiffres hors années). C'est ce test qui bloque CBOE/CME et CVE-2018-20586/20587.

**Confirmations**
4. `test_structure` — recouvrement des cibles de relations (`belongs to domain`, `appears in section`, `occurs in`).
5. `test_description` — recouvrement lexical des descriptions.

**Règle de décision**
`FUSION_SURE` exige : aucun veto **et** similarité de nom ≥ 0,60 **et** au moins une confirmation **et** (dates strictement identiques au jour près **ou** aucune des deux datée). Tout le reste tombe en `A_VERIFIER`. Le seuil de candidature est bas (0,28) exprès : le mécanisme est conçu pour rater peu et proposer peu.

**Résultat sur 73 paires candidates** : 4 `FUSION_SURE` · 13 `A_VERIFIER` · 56 `REJET_AUTO` (chacun avec son motif écrit).

## Le patch — non destructif par construction

`patch_10_dedup_events.json`, **10 opérations, toutes `SET_ATTRIBUTE`**. La convention du dépôt (`patch_1a`, `patch_1b`, `patch_2b`, `patch_2c`) ne comporte que `SET_ATTRIBUTE`, `ADD_RELATION`, `REMOVE_RELATION` — aucune opération de suppression d'entité. Le patch s'y tient et n'en invente pas.

Chaque doublon reçoit `duplicateOf` (id de l'entité canonique) et `reviewStatus = duplicate-pending-merge`. **Rien n'est effacé** : les deux entités restent dans le graphe et restent interrogeables ; la fusion effective demeure une décision humaine ultérieure. La canonique est l'entité la mieux dotée (attributs, puis relations).

Contenu : 3 paires « mining pools » (4 opérations ×2) + Scaling Debate + la correction de date Litecoin.

## Vérifications externes des 5 conflits de dates

| Conflit | Statut | Conclusion |
|---|---|---|
| **Litecoin** | CONFIRMÉ | Client publié sur GitHub et bloc de genèse minés le **07/10/2011**, réseau actif le 13/10. **La thèse a raison** (l.359, « début octobre ») ; le graphe (19/11/2011) est faux → **corrigé dans le patch**. |
| **Frontier** | CONFIRMÉ | Billet de la Fondation Ethereum daté du **30/07/2015** annonçant le bloc de genèse ; CoinDesk même jour. **Le graphe a raison** ; c'est le texte de la thèse (l.399, 20/07) qui est à corriger. Aucun patch graphe. |
| **Bitcointalk** | CONFIRMÉ | Premier message de Nakamoto le **22/11/2009**. Le graphe a raison. Le « janvier 2009 » du ch.I l.113 vise probablement le **forum SourceForge antérieur**, aujourd'hui perdu, qui a précédé Bitcointalk — ce sont deux objets distincts. |
| **NewLibertyStandard** | DEUX ÉVÉNEMENTS | Les deux dates sont exactes et désignent des actes différents : **05/10/2009** publication du premier taux BTC/USD (1 $ = 1 309,03 BTC, formule au coût de production) ; **12/10/2009** première transaction BTC contre fiat (Malmi vend 5 050 BTC pour 5,02 $ via PayPal). Recommandation : dédoubler l'événement, ne pas arbitrer. |
| **BitLaundry** | NON TRANCHÉ | Aucune source externe précise : « autour de 2010 », fiche Bitcoin Wiki datée 2011. Ni 09/2010 (graphe) ni 12/2010 (thèse n.74 l.607) ne sont confirmés → **validation manuelle**. |

## Anomalies détectées en cours de route

1. **`BitcoinTalk forum` daté 2010-11-22** dans le graphe, alors qu'une autre entité porte 2009-11-22 pour le même fait. Même jour, même mois, un an d'écart : très probable coquille d'année. La vérification externe confirme 2009. **Non patché** — signalé pour validation.
2. **7 paires bloquées par « types différents »** (Op_Return War, Genesis Block, Silk Road, Bitcoin-Qt, Scaling Bitcoin). Ce n'est pas forcément un faux positif : il se peut que le même fait soit modélisé deux fois sous deux types. Catégorie à examiner séparément.
3. Les 13 `A_VERIFIER` incluent des cas nets (halving 2012-11-28 vs 2012-11 ; « Nakamoto réserve » vs « Dépôt du nom de domaine ») et des cas parasites (Bitcoin-Qt sans date, apparié à trois entités différentes).

## Livrables
- `patch_10_dedup_events.json` — patch, 10 opérations, format du dépôt
- `doublons-verifies.csv` — 73 paires, statut + motif de chaque décision
- `dates-verification-externe.csv` — les 5 conflits avec preuve et statut
- `verif_doublons.py` — mécanisme rejouable

## Prochaine étape
(a) Application du patch sur une branche + PR ; (b) arbitrage des 13 `A_VERIFIER` et des 7 « types différents » ; (c) décision sur le dédoublement NewLibertyStandard et sur BitLaundry ; (d) correction du texte de la thèse pour Frontier (20→30/07/2015) et clarification l.113 (forum SourceForge ≠ Bitcointalk).
