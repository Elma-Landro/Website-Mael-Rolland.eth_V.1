# GRC-20 Patch Queue Governance & CI Policy Lab v1

**Date** : 2026-08-09
**Graphe de référence** : `grc20-these-mael-rolland-v113.json` — **non modifié**
**Mécanisme rejouable** : `scripts/build_patch_queue_governance.py` (`--csv`, `--check`)
**Données probantes** : `docs/audits/data/patch-queue-governance-cases-current.csv` — 31 artefacts
**Ledger** : `patch-application-ledger.json` — mémoire d'application, 3 entrées
**Arbitrages** : Maël Rolland, 2026-08-09, questions 1 à 8 — **tous rendus**, § 5
**Brouillon de politique** : `docs/audits/patch-queue-lifecycle-policy-draft.md` — **non appliqué**

**Aucun graphe modifié. Aucune v114. Aucun patch appliqué. Aucun nœud, aucune fusion, aucune relation, aucun retypage, aucune SourceQuote, aucun runtime touché. C03 n'est pas modifié.**

---

## 1. Le diagnostic tient en une mesure

**Sur 31 artefacts de patch, deux restent applicables.**

> **Corrigé après revue hostile.** Ce paragraphe annonçait « un seul ». La revue a montré que `patches/archive/grc20_anchor_overrides_targeted.json` était classé `archive_historical` — « lot intégré » — alors qu'il est appliqué à **0/10** : son dialecte `safe_fix` / `proposed_review` n'était pas dans la table des conteneurs, l'outil lisait 0 op et retombait sur un défaut. Mesure de contrôle : l'attribut `primaryChapter` que ce patch pose a **0 porteur** sur les 2 293 entités de v113. Le dialecte est désormais lu, l'artefact se mesure à `still_candidate`, et l'arbitrage 7 le classe **`blocked_author_arbitration`** — techniquement applicable, scientifiquement non instruit. C'était l'inverse exact de la vérité, et le mot « prudent » alors employé pour `archive_historical` était faux : sur les statuts possibles, c'est le **moins** conservateur, puisqu'il autorise à ne plus rien instruire.

La colonne **« proposé »** est le diagnostic tel qu'il a été soumis à l'auteur ; la colonne **« après arbitrage 7 »** est ce que le CSV versé porte aujourd'hui (`patch-queue-governance-cases-current.csv`, régénérable par `--csv`, vérifiable par `--check`). Les deux sont montrées parce que l'arbitrage a déplacé deux lignes, et qu'un audit qui n'afficherait que le résultat effacerait ce qui a été décidé.

| Statut de gouvernance | proposé | après arbitrage 7 | Rejouable ? |
|---|---:|---:|---|
| `archive_historical` | 18 | **17** | non — lot intégré, rejeu sans effet |
| `archive_partial` | 7 | 7 | **non — un rejeu écrirait à côté** |
| `candidate_applied` | 3 | 3 | non — appliqué par v111, v112, v113 |
| `blocked_missing_applicator` | 1 | 1 | non — aucun applicateur ne lit `CREATE_ENTITY` |
| `indetermine` | 0 | **1** | **statut non établi** — l'outil ne lit aucune op |
| `candidate_active` → **`blocked_author_arbitration`** | **2** | **2** | techniquement **oui**, `ci_candidate` = **non** |

Deux déplacements, tous deux vers plus de prudence : l'artefact à 0 op lisible quitte `archive_historical` pour `indetermine` (§ 7), et les deux candidats actifs deviennent `blocked_author_arbitration` (§ 5). **Après arbitrage, `ci_candidate` vaut `non` sur les 31 lignes.**

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

## 5. Arbitrages rendus — 2026-08-09

Les huit questions ont reçu réponse. Ce que le chantier a **exécuté** en conséquence :

| # | Arbitrage | Effet dans cette PR |
|---|---|---|
| 1 | file = **les deux, mais séparés** — un inventaire vivant, des snapshots figés ; jamais le même fichier pour les deux rôles | `-current.csv` + `-vNN.snapshot.csv`, et viser un ancien graphe écrit un snapshot **au lieu** d'écraser le vivant |
| 2 | `lifecycleStatus` **oui**, mais *pas* comme source unique de vérité ; le statut réel reste **mesuré** | vocabulaire inscrit au brouillon ; **aucun patch existant modifié** — l'auteur a demandé un chantier dédié |
| 3 | ledger externe **oui** | `patch-application-ledger.json`, généré, `--check`. Chaque entrée porte un `measured` relu dans le graphe |
| 4 | C03 **non modifié** maintenant | intact. L'audit dit désormais où lire le vrai statut : **graphe → file vivante → ledger**, jamais la policy |
| 5 | CI **modèle 2 maintenant**, modèle 4 en cible | étape ajoutée : les trois outils tournent et leurs sorties sont **déterministes** ; aucune exigence de fraîcheur du CSV |
| 6 | nommage **current + snapshots** | appliqué aux deux CSV ; l'écrasement silencieux est structurellement impossible |
| 7 | statut **conservateur obligatoire** | `indetermine` quand l'outil ne lit pas tout ; `archive_historical` n'est plus un défaut de repli |
| 8 | PR de gouvernance **oui** | cette PR — aucun graphe, aucune v114, aucune application |

**Le point le plus important de l'arbitrage 7**, et il change un résultat : *« applicable techniquement ne veut pas dire mûr pour v114 »*. Les deux artefacts entiers dont les cibles existent — `patch_candidate_bibliographie_duplicates_v1.json` et `patches/archive/grc20_anchor_overrides_targeted.json` — passent de `candidate_active` à **`blocked_author_arbitration`**, et leur `ci_candidate` tombe à `non`.

**Conséquence directe : il ne reste plus AUCUN artefact que la CI aurait à surveiller.** L'argument contre la CI stricte n'est plus fondé sur un chiffre bas, il l'est sur un ensemble vide. Le § 1 ci-dessus, écrit avant l'arbitrage, disait « deux » ; c'est désormais **zéro applicable sans instruction préalable**.

---

## 6. Ce que ce chantier ne fait pas

Il **ne modifie pas C03** et n'ajoute aucun `lifecycleStatus` aux patchs existants — l'auteur a renvoyé ce point à un chantier dédié (arbitrage 2). Il ne modifie aucun graphe, ne crée aucune v114, n'applique aucun patch. **Les deux artefacts techniquement applicables ne sont pas appliqués** : ils sont classés `blocked_author_arbitration` et renvoyés à instruction. Le brouillon `patch-queue-lifecycle-policy-draft.md` écrit la politique **telle qu'elle serait si elle était adoptée** ; il n'a aucun effet.

## 7. Corrections apportées après revue hostile

**L'inventaire lisait la sortie de son propre outillage.** Le glob `*patch*.json` attrape `patch-application-ledger.json` — le registre d'applications créé par ce chantier même. La file en comptait donc **32** artefacts là où tout le reste du dépôt en annonce 31, et prescrivait au ledger, classé `indetermine` faute d'ops lisibles, « à instruire à la main, jamais à rejouer par défaut ». Autrement dit, le chantier a produit un fichier de comptabilité et son propre outil l'a rangé dans la file d'attente des patchs. C'est exactement la **question 1 de la revue hostile** — « ce script lit-il sa propre sortie ? » — et elle était réalisée.

Deux choses la rendaient difficile à voir. D'abord `--check` restait **vert** : le CSV versé avait été régénéré *avec* la ligne fautive, donc il collait à ce que le script recalculait. Un contrôle de cohérence entre un outil et sa propre sortie ne peut pas détecter que l'outil a tort. Ensuite l'écart 31/32 n'apparaissait dans aucune sortie lue de bout en bout : les vérifications passées n'affichaient que la queue du résumé.

Le correctif est une **exclusion nommée** (`NON_PATCHS`), pas un rétrécissement du glob : rétrécir avait déjà fait perdre `new_relations_patch.json` et ses 11 884 ops. Les deux CSV sont régénérés à 31 lignes, et le ledger n'y figure plus.

**Le § 6 décrivait comme subsistant un défaut que l'arbitrage 7 avait supprimé.** Il annonçait que `patches/grc20_v97_remove_15_truncated_broken_relations.json`, à 0 op lisible, « retombe sur `archive_historical` par défaut ». Depuis l'arbitrage 7 le code renvoie `indetermine` dans ce cas, et la mesure le confirme (`measured_status=indetermine`, `recommended_governance_status=indetermine`). La limite est levée ; elle est réécrite ci-dessous pour ce qu'elle est encore.

**La numérotation des sections était fausse** — § 7 s'intercalait entre § 4 et § 5. Corrigée.

## 8. Limite connue

La table de gouvernance dérive de l'inventaire : si l'heuristique de dialecte de `build_patch_queue_inventory.py` se trompe sur un artefact, la recommandation héritera de l'erreur, sans que rien ne le signale. C'est la limite structurante, et aucun contrôle du dépôt ne la couvre : `--check` compare l'outil à sa propre sortie, jamais à la réalité.

**Un artefact reste à 0 op lisible** — `patches/grc20_v97_remove_15_truncated_broken_relations.json`, un reçu d'opération plutôt qu'un patch. Il est désormais classé `indetermine`, ce qui est le statut prudent, mais `indetermine` **n'est pas un verdict** : c'est l'aveu qu'il n'y en a pas. Il faudra l'instruire à la main.

**Trois lignes `archive_historical` reposent sur 33 ops que l'outil ne lit pas** (`patch_14` 6, `patch_16` 22, `patch_3a` 5 — dialectes `rewire_relations` et `update_entities`). La revue les a mesurées à la main : **33/33 réalisées**. Le verdict est donc juste en fait, mais sans preuve produite par ce chantier — et un `archive_historical` non prouvé autorise à ne plus rien instruire.

**L'étape CI ajoutée compare des sorties, pas des fichiers.** Elle lance chaque outil deux fois et diffe leur `stdout`, qui ne porte que des compteurs. Une non-déterminisme qui n'affecterait qu'une colonne du CSV sans changer un total passerait au vert. C'est un test de déterminisme minimal, assumé comme tel par l'arbitrage 5 ; le modèle strict reste la cible.
