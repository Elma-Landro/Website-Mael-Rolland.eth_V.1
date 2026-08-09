# GRC-20 Patch Queue Governance & CI Policy Lab v1

**Date** : 2026-08-09
**Graphe de référence** : `grc20-these-mael-rolland-v113.json` — **non modifié**
**Mécanisme rejouable** : `scripts/build_patch_queue_governance.py` (`--csv`, `--check`)
**Données probantes** : `docs/audits/data/patch-queue-governance-cases-v113.csv` — 31 artefacts
**Brouillon de politique** : `docs/audits/patch-queue-lifecycle-policy-draft.md` — **non appliqué**

**Aucun graphe modifié. Aucune v114. Aucun patch appliqué. Aucun nœud, aucune fusion, aucune relation, aucun retypage, aucune SourceQuote, aucun runtime touché. C03 n'est pas modifié.**

---

## 1. Le diagnostic tient en une mesure

**Sur 31 artefacts de patch, deux restent applicables.**

> **Corrigé après revue hostile.** Ce paragraphe annonçait « un seul ». La revue a montré que `patches/archive/grc20_anchor_overrides_targeted.json` était classé `archive_historical` — « lot intégré » — alors qu'il est appliqué à **0/10** : son dialecte `safe_fix` / `proposed_review` n'était pas dans la table des conteneurs, l'outil lisait 0 op et retombait sur un défaut. Mesure de contrôle : l'attribut `primaryChapter` que ce patch pose a **0 porteur** sur les 2 293 entités de v113. Le dialecte est désormais lu, et le statut est `candidate_active`. C'était l'inverse exact de la vérité, et le mot « prudent » que le § 6 employait était faux : sur quatre statuts, `archive_historical` est le **moins** conservateur.

| Statut de gouvernance proposé | n | Rejouable ? |
|---|---:|---|
| `archive_historical` | 18 | non — lot intégré, rejeu sans effet |
| `archive_partial` | 7 | **non — un rejeu écrirait à côté** |
| `candidate_applied` | 3 | non — appliqué par v111, v112, v113 |
| `blocked_missing_applicator` | 1 | non — aucun applicateur ne lit `CREATE_ENTITY` |
| **`candidate_active`** | **2** | **oui** |

Les deux candidats actifs sont `patch_candidate_bibliographie_duplicates_v1.json` (156 ops `duplicateOf`, famille explicitement mise hors périmètre par l'auteur) et `patches/archive/grc20_anchor_overrides_targeted.json` (10 ops, 0 réalisée).

**Le chiffre porte moins loin qu'il n'y paraît, et la revue hostile a eu raison de le dire.** Il compte ce qui est applicable *aujourd'hui, sans écrire une ligne de code*. Il exclut : `patch_candidate_bibliographie_missing_nodes_v1.json` (38 ops), non applicable seulement parce qu'**aucun applicateur ne lit `CREATE_ENTITY`** — écrire cet applicateur ferait trois ; et les **4 archives `Migration/*.zip`** (41 ops SourceQuote vérifiées par un lab antérieur, gelées par arbitrage), hors du glob comme du périmètre déclaré. Le chiffre est en outre **mobile** : mesuré sur v112, il vaut 2 également, mais rien ne garantit qu'il reste bas.

Énoncé honnête : **2 applicables, 1 bloqué faute d'applicateur, 4 hors périmètre déclaré.** Cela reste un argument contre une CI stricte — mais un argument, pas une démonstration.

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

Sept artefacts portent `archive_partial`, mais **pour deux raisons distinctes qu'il ne faut pas confondre** — la première rédaction de cet audit les amalgamait :

- **état mixte** — des ops lisibles ne sont pas réalisées : `new_relations_patch.json` (6 246/11 884), `patch_1b` (770/774), `patch_5` (141/147), `patch_4` (105/111), `patch_11` (27/31) ;
- **cibles mortes** — toutes les ops lisibles sont faites, mais des cibles ont disparu : `patch_2b` (49/49, 7 cibles absentes) ;
- `patch_2c` (248/274, 19 absentes) cumule les deux.

**Aucun ne doit être rejoué**, et aucun n'est un candidat.

**Une limite du compteur, signalée par la revue** : `ops_missing_targets` vaut **0 par construction** pour les patchs de relations — une op `ADD_RELATION` dont une extrémité est introuvable renvoie `False`, jamais `None`, et n'incrémente donc rien. Sur `new_relations_patch.json`, 428 ops visent une entité réellement disparue et 5 201 pointent vers des marqueurs `NEEDS_CREATION:` non résolus, sans que la colonne l'indique. Sans effet sur les statuts actuels, mais le compteur promet plus qu'il ne mesure.

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

La table de gouvernance dérive de l'inventaire : si l'heuristique de dialecte de `build_patch_queue_inventory.py` se trompe sur un artefact, la recommandation héritera de l'erreur. Un artefact reste à `0` op lisible (`patches/grc20_v97_remove_15_truncated_broken_relations.json`, un reçu d'opération plutôt qu'un patch) et retombe sur `archive_historical` par défaut. **Ce défaut n'est pas prudent** : sur les quatre statuts possibles, `archive_historical` est le moins conservateur, puisqu'il autorise à ne plus rien instruire. Le prudent serait `indetermine`. La revue hostile a démontré le coût de ce choix sur un autre fichier (voir § 1) ; il subsiste ici.

**Trois lignes `archive_historical` reposent par ailleurs sur 33 ops que l'outil ne lit pas** (`patch_14` 6, `patch_16` 22, `patch_3a` 5 — dialectes `rewire_relations` et `update_entities`). La revue les a mesurées à la main : **33/33 réalisées**. Le verdict est donc juste en fait, mais sans preuve produite par ce chantier.
