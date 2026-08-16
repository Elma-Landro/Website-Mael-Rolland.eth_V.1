# Passation → Claude Code : dédoublonnage des événements du graphe v97

**Origine** : session Claude.ai des 02–03/08/2026 (brief révisé le 03/08) (chantier « catalogue d'événements », valorisation de la thèse).
**Mode d'intervention** (charte `agents/README.md`) : **A — Audit**, avec production d'un patch non appliqué.
**Rappel de la charte** : un agent est un rôle de travail, pas une autorité scientifique. L'arbitrage reste à Maël. Rien de ce qui suit ne doit être tranché par l'agent.

---

## 1. Ce qui a été fait (hors dépôt, en lecture seule)

Le dépôt a été cloné en HTTPS anonyme, branche par défaut `codex/create-expand-from-node-planning-documents` (HEAD `b4b0c8b`). **Aucune écriture, aucun commit.** `git status` propre.

Analyse de `grc20-these-mael-rolland-v97.json` : 158 `InfrastructureEvent` + 55 `CrisisEvent` extraits, dates normalisées, doublons détectés par un mécanisme à vetos, conflits de dates vérifiés en sources externes.

## 2. Fichiers à intégrer

| Fichier | Destination proposée | Nature |
|---|---|---|
| `etat-dedup-patch-2026-08-02.md` | `docs/audits/grc20-dedup-events-audit-v1.md` | rapport d'audit (à renommer à la convention maison) |
| `patch_10_dedup_events.json` | racine (convention `patch_*.json` existante) | patch, **non appliqué** |
| `verif_doublons.py` | `tools/` ou racine (cf. `apply_v91_migration.py`) | mécanisme rejouable |
| `doublons-verifies.csv` | `docs/audits/data/` | 73 paires, statut + motif |
| `dates-verification-externe.csv` | `docs/audits/data/` | 5 conflits, preuves externes |
| `catalogue-evenements-v2-fusion.csv` | `docs/audits/data/` | **253 lignes — requis pour le rattachement aux domaines, cf. §8** |
| `grille-codage-catalogue-v1.md` | `docs/audits/` | grille de codage (définitions des 8 domaines, 7 types d'acte, 9 arènes) |

> **Correction du 03/08/2026.** La v1 de ce brief classait le CSV v2 « hors dépôt, ne concerne pas le graphe ». C'était une erreur : la v2 porte les 175 lignes issues du graphe avec leur `gid`, elle est donc la table de jointure indispensable à tout travail sur les domaines. Elle entre dans le dépôt.

## 3. Le patch

`patch_10_dedup_events.json` — **10 opérations, toutes `SET_ATTRIBUTE`**. Conforme aux conventions de `patch_1a`, `patch_1b`, `patch_2b`, `patch_2c` (aucune opération de suppression d'entité n'existe dans ce dépôt ; le patch n'en invente pas).

Chaque doublon reçoit `duplicateOf` (id canonique) + `reviewStatus = duplicate-pending-merge`. **Rien n'est effacé** ; les deux entités restent interrogeables. La fusion effective est une décision humaine ultérieure.

Contenu : 3 paires « mining pools », 1 paire « Scaling Debate », 1 correction de date (Litecoin → `2011-10-07`).

## 4. Le mécanisme de vérification

Trois **vetos** bloquants puis deux **confirmations**, décision par conjonction :

- V1 type différent (`InfrastructureEvent` vs `CrisisEvent`)
- V2 dates contradictoires (précisions emboîtées tolérées)
- V3 divergence de `cveId`, `crisisNumber`, ou identifiants distinctifs du libellé (acronymes 2–6 maj., nombres 3–6 chiffres hors années)
- C1 recouvrement des cibles de relations · C2 recouvrement des descriptions

`FUSION_SURE` = aucun veto + nom ≥ 0,60 + ≥ 1 confirmation + dates identiques au jour (ou aucune datée).
**Résultat : 4 sûres / 13 à vérifier / 56 rejetées** sur 73 candidates. V3 bloque correctement CBOE↔CME et CVE-2018-20586↔20587.

## 5. Tâches pour Claude Code

1. Créer la branche `agent/grc20-dedup-events-v1`.
2. Déposer les fichiers du §2, en alignant noms et en-têtes sur `docs/audits/grc20-representation-audit-v1.md`.
3. **Ne pas appliquer le patch** dans le même commit que le rapport : deux commits distincts, pour que l'application reste révocable seule.
4. Vérifier que `apply_v91_migration.py` (ou l'outil équivalent) sait consommer `SET_ATTRIBUTE` sur un attribut inexistant (`duplicateOf`, `reviewStatus`) ; si non, adapter l'applicateur **sans** modifier le patch.
5. Ouvrir la PR en listant les points ouverts du §6.

## 6. Points ouverts — à ne pas trancher

1. **13 paires `A_VERIFIER`** (`doublons-verifies.csv`) — dont halving `2012-11-28` vs `2012-11`, et « Nakamoto réserve le nom de domaine » vs « Dépôt du nom de domaine ».
2. **7 paires bloquées par « types différents »** (Op_Return War, Genesis Block, Silk Road, Bitcoin-Qt, Scaling Bitcoin) : possible double modélisation du même fait sous deux types. À examiner séparément.
3. **`BitcoinTalk forum` daté `2010-11-22`** alors qu'une autre entité porte `2009-11-22` pour le même fait. Même jour et mois, un an d'écart ; vérification externe confirme 2009. **Non patché**, coquille très probable.
4. **NewLibertyStandard** : les deux dates sont exactes et désignent deux actes distincts — `2009-10-05` publication du premier taux BTC/USD (1 $ = 1 309,03 BTC) ; `2009-10-12` première transaction contre fiat (Malmi, 5 050 BTC pour 5,02 $). Recommandation : dédoubler l'entité, ne pas arbitrer.
5. **BitLaundry** : aucune source externe précise. Ni `2010-09` (graphe) ni `2010-12` (thèse ch.I n.74 l.607). Validation manuelle.
6. **Corrections côté thèse, pas côté graphe** : Frontier `20/07/2015` (ch.I l.399) → le graphe a raison avec `30/07/2015` ; et ch.I l.113 « janvier 2009 » pour Bitcointalk vise probablement le forum SourceForge antérieur, distinct de Bitcointalk (22/11/2009).
7. **Domaines** : Maël a confirmé que les 8 domaines de référence sont ceux de la thèse (ch.I l.251). Le graphe n'a **aucun domaine correspondant à (ii) traitement des transactions** et comporte un `[Résiduel — à reclasser]`. Chantier distinct, non traité ici.

## 7. Ce qui n'a pas été fait

- Aucune écriture sur le dépôt, aucune PR.
- Aucune fusion effective d'entités.
- Aucun arbitrage sur les points du §6.
- L'export SVG de la chronologie carnavalesque est **absent de cette branche** (seuls le PNG V2.8 et 4 SVG d'autres figures sont présents).

## 8. État réel du catalogue v2 — à lire avant tout travail sur les domaines

**La v2 est en cours de codage, pas codée.** Composition : 46 lignes `origine=catalogue` + 32 `catalogue+graphe` (les 78 du calibrage) + **175 `origine=graphe`**. 207 lignes portent un `gid` (jointure vers le graphe v97).

| Colonne | Rempli | Vide |
|---|---|---|
| `domaine_8` | 159 | **94** |
| `acteur_principal` | 67 | 186 |
| `arene` | 78 | 175 |
| `type_acte` | 68 | 185 |
| `effet_prop_monetaires` | 25 | 228 |

Les colonnes analytiques ne sont renseignées que sur les lignes de calibrage. Les 175 lignes issues du graphe arrivent avec `acteur_principal`, `arene` et `type_acte` **vides** : c'est le travail de codage restant, et il est humain (la grille §grille-codage définit les vocabulaires fermés).

**Marqueurs de `domaine_8`** : le suffixe `*` (39 lignes) signale une attribution par définition faite au calibrage, sans vérification du code couleur de la figure. Il n'existe **aucun** marqueur distinguant les domaines hérités du graphe — la colonne `origine` fait cet office (`graphe` = domaine issu du mapping GRC-20, à contrôler).

**Aide au codage, non substituable** : les colonnes `acteurs_graphe` (36 `StakeholderCategory` du graphe, trois niveaux de granularité mêlés, doublons) et `occurs_in` (13 `GovernanceArena`, lieux nommés et non types) servent d'indices. Elles ne remplacent pas les 7 types d'acteurs ni les 9 arènes de la grille, qui sont des niveaux de regroupement.

**Point dur — domaine (ii) absent du graphe.** Maël a confirmé que les 8 domaines de référence sont ceux de la thèse (ch.I l.251). Le mapping appliqué est : « Sphère d'usage »→i · « Services de portefeuille et de paiement »→iii · « Information et connaissance »→iv · « Conformité réglementaire »→v · « Protocole et couche de base »→vi · « Altcoins, tokens et surcouches »→vii · « De la confidentialité et de l'anonymisation »→**iii** · « [Résiduel — à reclasser] »→viii.
Le graphe **n'a aucun domaine correspondant à (ii) traitement des transactions** (le jaune, le minage). Les événements de minage ne peuvent donc pas être rattachés depuis le graphe seul : c'est une lacune de l'ontologie GRC-20, pas du catalogue. À signaler dans la PR, à ne pas combler par inférence.
