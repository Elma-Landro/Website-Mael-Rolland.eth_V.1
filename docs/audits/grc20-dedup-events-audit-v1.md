# GRC-20 Dedup Events Audit v1 — dédoublonnage vérifié des événements

**Date** : 2026-08-02  
**Graphe audité** : `grc20-these-mael-rolland-v97.json` (213 événements : 158 `InfrastructureEvent` + 55 `CrisisEvent`)  
**Branche** : `agent/grc20-dedup-events-v1`  
**Mode agent** : A (audit documentaire, avec production d'un patch **non appliqué**)  
**Mécanisme rejouable** : `scripts/verif_doublons.py`  
**Données probantes** : `docs/audits/data/doublons-verifies.csv`, `docs/audits/data/dates-verification-externe.csv`  
**Patch associé** : `patch_10_dedup_events.json` (racine, **non appliqué**)

> Rappel de la charte (`agents/README.md`) : un agent est un rôle de travail, pas une autorité scientifique. Aucun des points ouverts ci-dessous n'est tranché ici ; l'arbitrage appartient à Maël Rolland.

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

---

## Points ouverts — à ne pas trancher

Report intégral, pour que ce document se suffise à lui-même :

1. **13 paires `A_VERIFIER`** (`docs/audits/data/doublons-verifies.csv`) — dont halving `2012-11-28` vs `2012-11`, et « Nakamoto réserve le nom de domaine » vs « Dépôt du nom de domaine ».
2. **7 paires bloquées par « types différents »** (Op_Return War, Genesis Block, Silk Road, Bitcoin-Qt, Scaling Bitcoin) : possible double modélisation du même fait sous deux types. À examiner séparément.
3. **`BitcoinTalk forum` daté `2010-11-22`** alors qu'une autre entité porte `2009-11-22` pour le même fait. Même jour et mois, un an d'écart ; la vérification externe confirme 2009. **Non patché**, coquille très probable.
4. **NewLibertyStandard** : les deux dates sont exactes et désignent deux actes distincts — `2009-10-05` publication du premier taux BTC/USD (1 $ = 1 309,03 BTC) ; `2009-10-12` première transaction contre fiat (Malmi, 5 050 BTC pour 5,02 $). Recommandation : dédoubler l'entité, ne pas arbitrer.
5. **BitLaundry** : aucune source externe précise. Ni `2010-09` (graphe) ni `2010-12` (thèse ch.I n.74 l.607). Validation manuelle.
6. **Corrections côté thèse, pas côté graphe** : Frontier `20/07/2015` (ch.I l.399) → le graphe a raison avec `30/07/2015` ; et ch.I l.113 « janvier 2009 » pour Bitcointalk vise probablement le forum SourceForge antérieur, distinct de Bitcointalk (22/11/2009).
7. **Domaines** : les 8 domaines de référence sont ceux de la thèse (ch.I l.251). Le graphe n'a **aucun domaine correspondant à (ii) traitement des transactions** et comporte un `[Résiduel — à reclasser]`. Chantier distinct, non traité ici.

---

## Annexe — vérifications faites côté dépôt (Claude Code, 02/08/2026)

Constats établis en lecture du dépôt au moment du versement, sur la branche `agent/grc20-dedup-events-v1` (base `b4b0c8b`). Conformément à la **Règle 3** de `agents/README.md` (« *data is not fact* »), ils sont consignés **comme données, pas comme faits**. Aucun n'est arbitré, et aucun n'a entraîné de modification du patch.

### Rejeu du mécanisme — concluant

`scripts/verif_doublons.py` a été réexécuté contre `grc20-these-mael-rolland-v97.json` depuis le dépôt. Il reproduit **73 paires candidates → 4 `FUSION_SURE` / 13 `A_VERIFIER` / 56 `REJET_AUTO`**, et régénère les deux CSV et le patch **octet pour octet identiques** aux fichiers versés. L'adaptation des chemins du script (cf. commit) n'a donc rien changé au fond, et le chantier est reproductible depuis le dépôt seul.

### C1 — Il n'existe aucun applicateur générique dans le dépôt

`apply_v91_migration.py` n'est pas un applicateur de patch : c'est un script v90→v91 à 10 phases, aux chemins codés en dur, qui ne connaît ni la clé `op` ni `SET_ATTRIBUTE` (le terme n'apparaît nulle part dans le fichier). Ses entrées (`Migration/grc20_v91_patch_seed.json`, `Migration/grc20_v91_name_based_patch.json`) **n'existent plus dans l'arbre** : il n'est plus exécutable. Aucun autre script ne consomme les `patch_*.json` de la racine ; la famille `scripts/generate_*` les *produit*. `CLAUDE.md` le confirme : « *Patch files are applied by merging their entity/relation data into the base graph JSON. They are not auto-applied.* »

**Conséquence** : la tâche « vérifier que l'applicateur sait consommer `SET_ATTRIBUTE` sur un attribut inexistant » est sans objet — il n'y a rien à adapter. Le motif maison pour appliquer ce patch serait un script dédié `scripts/make_v98_<objet>.py`, calqué sur `scripts/make_v97_remove_truncated_broken_relations.py` (lit vN, mute, écrit vN+1, dépose un reçu dans `patches/`). **Il n'a pas été écrit** : le patch reste non appliqué.

### C2 — Aucun attribut n'a besoin d'être déclaré

Le graphe v97 n'a **aucun registre d'attributs**. Ses clés de tête sont `space`, `types`, `relation_types`, `entities`, `relations`, `ops` ; `types` (55) et `relation_types` (130) ne portent que `{id, name, description}`. Plus de 88 clés d'attributs distinctes circulent dans les entités, toutes non déclarées. `duplicateOf` et `reviewStatus` sont absents du dépôt entier (0 entité) et ne coûtent aucune modification de schéma. À noter pour la publication : `grc20-publish.mjs` passe la clé brute en attribut de triplet, et sa table `SYSTEM_PROPERTY_IDS` ne couvre que `name`/`description`/`types` — elle est déjà incomplète pour tous les attributs personnalisés existants.

### C3 — Le format du patch hybride deux dialectes du dépôt

Le patch a été présenté comme conforme aux conventions de `patch_1a`, `patch_1b`, `patch_2b`, `patch_2c`. En réalité le dépôt porte **deux dialectes `SET_ATTRIBUTE` incompatibles** :

| | enveloppe | clés par opération |
|---|---|---|
| `patch_2c_definitions.json` | `schemaVersion` + `ops` | `type` / `entityId` / `attributeId` / `value:{type,value}` |
| `patch_2b_central_arguments.json` | `patch_id` + `description` + `operations` | `op` / `entity_id` / `attribute_name` / valeur nue |

`patch_10_dedup_events.json` combine l'enveloppe du premier dialecte (`operations`, clé `op`) avec les champs du second (`entityId` / `attributeId` / `value:{type,value}`). Il ne correspond exactement à aucun des deux. Sans conséquence tant qu'aucun applicateur ne le consomme (cf. C1), **mais à trancher avant toute application**.

### C4 — Deux opérations du patch se contredisent

L'entité `ee7277478ddc4c0886e8d73a4e2ce00d` (« Mining pools ») reçoit `duplicateOf` **deux fois, avec deux valeurs différentes** :

- opération 1 → `15864ab2cdcd41348eecc0daba8eb11d`
- opération 5 → `7f80094676fd44a785c6483dbee4f8c5`

En dernière écriture gagnante, la première est silencieusement écrasée. Le triplet « mining pools » produit alors une **chaîne** (`ee7277…` → `7f8009…` → `15864ab2…`) là où le patch semble viser un pointage direct vers un canonique unique. C'est la conséquence mécanique d'avoir traité trois entités par paires indépendantes sans réconciliation transitive.

### C5 — Le canonique retenu est parfois le moins relié

Le mécanisme choisit le canonique par tri sur (nombre d'attributs, nombre de relations) — les attributs d'abord. Sur le triplet « mining pools », cela retient `15864ab2…` (**degré 4**) comme canonique de `ee7277…` (**degré 7**) : l'entité la mieux reliée est marquée doublon de la moins reliée. Sur Scaling Debate le tri joue dans le bon sens (`e3742113…` degré 65 canonique, `22c507bd…` degré 3 doublon).

À signaler également : **4 autres entités « Scaling Debate » existent en v97** et n'ont pas été soumises au mécanisme — `238900a65cec44bcad171c31850bc611` (« Scaling Debate (2015-2017) »), `0c6543e3c0a74af5b0f004d4e44833e7` (« GovernanceProcess — Bitcoin Scaling Debate (2015-2017) »), plus une `SourceQuote` et l'événement New York Agreement. Le périmètre du dédoublonnage (types `InfrastructureEvent` et `CrisisEvent` uniquement) les exclut par construction.

### C6 — La correction Litecoin est corroborée à l'intérieur même du graphe

L'entité `94ce188ef0534c1e8601226fc60163dd` porte `date = "19/11/2011"` (format `DD/MM/YYYY`), alors que **sa propre `description` énonce « Lancement du Litecoin (LTC) par Charlie Lee le 7 octobre 2011 »**. La date `2011-10-07` retenue par le patch ne repose donc pas seulement sur la vérification externe : elle lève une contradiction interne au graphe. C'est l'opération la mieux étayée du patch.

**Réserve sur l'opération jointe** : `dateAuthority` est **déjà utilisé par 37 entités de v97, toutes avec la valeur `TIMELINE_FIGURE`**, systématiquement adossée à un `dateSource` du type « Thèse — Chronologie 2 (p.88) ». Le patch y écrit du texte libre (`"Verification externe 02/08/2026 ; these ch.I l.359"`), ce qui s'écarte de cet usage établi. Deux voies possibles, non tranchées : suivre la convention existante (valeur codée + `dateSource` séparé), ou assumer un second registre de valeurs pour cet attribut.

**Contexte de format** : sur les 219 entités portant une `date` en v97, 55 utilisent `DD/MM/YYYY`, 52 l'ISO `YYYY-MM-DD`, 33 `YYYY-MM`, 41 l'année nue, 38 autre chose. Les 37 entités `dateAuthority: TIMELINE_FIGURE` sont toutes dans le groupe ISO — l'attribut marque aujourd'hui des dates *déjà normalisées et sourcées*.
