# GRC-20 Patch Queue Governance & CI Policy Lab v1

**Date** : 2026-08-09
**Graphe de référence** : `grc20-these-mael-rolland-v113.json` — **non modifié**
**Mécanisme rejouable** : `scripts/build_patch_queue_governance.py` (`--csv`, `--check`)
**Données probantes** : `docs/audits/data/patch-queue-governance-cases-v113.csv` — 31 artefacts
**Brouillon de politique** : `docs/audits/patch-queue-lifecycle-policy-draft.md` — **non appliqué**

**Aucun graphe modifié. Aucune v114. Aucun patch appliqué. Aucun nœud, aucune fusion, aucune relation, aucun retypage, aucune SourceQuote, aucun runtime touché. C03 n'est pas modifié.**

---

## 1. Le diagnostic tient en une mesure

**Sur 31 artefacts de patch, un seul reste applicable.**

| Statut de gouvernance proposé | n | Rejouable ? |
|---|---:|---|
| `archive_historical` | 19 | non — lot intégré, rejeu sans effet |
| `archive_partial` | 7 | **non — un rejeu écrirait à côté** |
| `candidate_applied` | 3 | non — appliqué par v111, v112, v113 |
| `blocked_missing_applicator` | 1 | non — aucun applicateur ne lit `CREATE_ENTITY` |
| **`candidate_active`** | **1** | **oui — et bloqué par arbitrage d'auteur** |

Ce seul candidat actif est `patch_candidate_bibliographie_duplicates_v1.json` — 156 ops `duplicateOf`, la famille que l'auteur a explicitement mise hors périmètre.

**Toute la question de la CI se joue donc sur un fichier.** Câbler un contrôle strict pour garder un artefact, au prix d'une CI qui rougit à chaque bump de version, est un mauvais échange. Ce chiffre n'est pas un détail de mise en forme : c'est l'argument.

---

## 2. Le problème que ce chantier doit résoudre

Trois patchs candidats ont été appliqués — page_start en v111, chronologie en v112, retypages en v113 — et **portent toujours** :

```text
CANDIDATE — NOT APPLIED — AUTHOR ARBITRATION REQUIRED
```

Ce n'est pas un oubli. Le contrôle **C03** de `preflight_candidate_patches.py` l'exige, et les applicateurs refusent un patch qui ne la porte pas. La phrase est donc **structurellement fausse et structurellement obligatoire**.

Deux précisions mesurées, qui bornent le problème plus qu'on ne le croit :

- **C03 ne balaie que `patch_candidate_*.json` à la racine** — cinq fichiers. Les 26 autres artefacts n'y sont pas soumis. Le problème est donc petit et bien délimité.
- **Le statut réel se mesure dans le graphe, jamais dans la policy.** L'inventaire mesure 16/16, 2/2 et 10/10 opérations réalisées pour les trois patchs appliqués. C'est la seule lecture qui ne trompe pas, et c'est la règle que tout ce chantier applique.

---

## 3. Une correction que ce chantier apporte au passage

L'inventaire classait `patch_2b_central_arguments.json` en `already_applied`. La table de gouvernance le rétrograde en **`archive_partial`**, et c'est mérité : ses 49 opérations *lisibles* sont bien réalisées, mais **7 de ses cibles n'existent plus dans le graphe**. « Appliqué » sur-promettait — la revue hostile de la PR #120 l'avait signalé, la colonne portait l'information, le mot la contredisait.

Sept artefacts sont dans ce cas, dont `new_relations_patch.json` (6 246 ops réalisées sur 11 884). **Aucun ne doit être rejoué**, et aucun n'est un candidat.

---

## 4. Les options, évaluées

### 4.1 Marquer un patch appliqué sans casser C03

| Option | Compatible CI | Risque agent futur | Lisibilité | Maintenance |
|---|---|---|---|---|
| **A. Ne rien changer, documenter dans la file** | totale | **élevé** — la policy ment, et rien dans le fichier ne le dit | faible | nulle |
| **B. Ajouter `_meta.lifecycleStatus`** | totale (C03 lit `policy`, pas ce champ) | **faible** — le démenti est dans le fichier même | bonne | 1 ligne par application |
| C. Ledger externe `patch-application-ledger.json` | totale | moyen — il faut savoir qu'il existe | bonne | un fichier de plus à tenir |
| D. Modifier C03 | **rupture** — il faut réviser le contrôle et les 3 applicateurs | faible | bonne | élevée, et touche un invariant |
| E. Déplacer les appliqués dans `patches/archive/` | casse le glob du preflight | faible | très bonne | élevée, casse les chemins cités par les audits |

**Recommandation : B.** Un champ `_meta.lifecycleStatus` — par exemple `applied_by: make_v113` — ne touche ni `policy` ni C03, met le démenti **dans le fichier que l'agent lit**, et coûte une ligne. C'est aussi la seule option qui survit à un agent qui ne lirait ni la file, ni l'audit, ni CLAUDE.md.

### 4.2 La CI

| Modèle | Ce qui casse au bump v114 | Coût | Verdict |
|---|---|---|---|
| **1. Pas de CI** | rien | nul | tenable, mais rien ne signale une file périmée |
| 2. CI souple (le script tourne) | rien | faible | **attrape peu** — un CSV périmé passe |
| 3. CI stricte (CSV = graphe courant) | **la CI rougit** : le nom du CSV suit le graphe, `…-v114.csv` n'existe pas encore | faible | **piège avéré** — c'est déjà le cas d'`audit_chronology_dates.py --check` |
| 4. Double sortie : un CSV *courant* vérifié + des instantanés versionnés figés | rien | moyen | robuste, mais deux fichiers à comprendre |

**Recommandation : 2, ou 4 si l'on veut vraiment un garde-fou.** Le modèle 3 est disqualifié par le seul fait mesuré au § 1 : il ferait rougir la CI à chaque version pour protéger **un** artefact, lui-même gelé par arbitrage. Le modèle 2 garantit au moins que le script n'est pas cassé.

### 4.3 Le nommage

Le dépôt mélange aujourd'hui deux natures sous une même forme :

- **preuve figée** — `chronology-date-inventory-v111.csv` décrit v111 et **ne doit pas** être régénéré. C'est pour cela qu'`audit_chronology_dates.py --check` échoue depuis v112, ce qui est correct et documenté ;
- **inventaire vivant** — la file de patchs décrit *l'état courant* et doit suivre le graphe.

Trois conventions possibles : `-vNNN.csv` pour les deux (état actuel, ambigu) ; `-current.csv` pour le vivant et `-vNNN.csv` pour le figé (lisible, mais perd la trace historique) ; ou `-vNNN.snapshot.csv` pour le figé et `-current.csv` pour le vivant (explicite, deux suffixes à retenir).

**Recommandation : `-current.csv` pour tout inventaire vivant, `-vNNN.csv` réservé aux preuves figées.** Le suffixe dit alors la *nature* du fichier, pas seulement sa date — et un `--check` sur un fichier `-current` ne casse jamais au bump.

---

## 5. Ce que ce chantier ne fait pas

Il **ne modifie pas C03**, n'ajoute aucun `lifecycleStatus`, ne crée aucun ledger, ne renomme aucun CSV et ne câble aucune CI. Le brouillon `patch-queue-lifecycle-policy-draft.md` écrit la politique **telle qu'elle serait si elle était adoptée** ; il n'a aucun effet.

## 6. Limite connue

La table de gouvernance dérive de l'inventaire : si l'heuristique de dialecte de `build_patch_queue_inventory.py` se trompe sur un artefact, la recommandation héritera de l'erreur. Deux artefacts restent à `0` op lisible (`patches/archive/grc20_anchor_overrides_targeted.json`, `patches/grc20_v97_remove_15_truncated_broken_relations.json`) et sont classés `archive_historical` par défaut — un défaut prudent, mais un défaut.
