# GRC-20 — Patch lifecycleStatus Implementation Lab v1

**Date** : 2026-08-10
**Graphe de référence** : `grc20-these-mael-rolland-v113.json` (canonique, **inchangé**)
**Branche** : `claude/file-upload-branch-check-jw4cng`
**Arbitrage appliqué** : Maël Rolland, 2026-08-09, Q2 (PR #121)
**Mécanisme rejouable** : `scripts/build_patch_lifecycle_status.py` (`--write`, `--check`)

**Aucun graphe modifié. Aucune v114. Aucun patch appliqué. Aucune op, aucune `value`, aucune `policy` touchée.** Ce chantier n'écrit que des métadonnées, et uniquement dans les cinq patchs candidats de la racine.

---

## 1. Quels patchs ont reçu un `lifecycleStatus`

Les **cinq** `patch_candidate_*.json` de la racine — exactement le périmètre que balaie C03, ni plus ni moins.

| Patch | `lifecycleStatus` | `measuredStatus` | Appliqué par |
|---|---|---|---|
| `patch_candidate_section_page_start_v1.json` | `candidate_applied` | `already_applied` | `make_v111`, PR #117 → v111 |
| `patch_candidate_chronology_dates_v1.json` | `candidate_applied` | `already_applied` | `make_v112`, PR #119 → v112 |
| `patch_candidate_bibliographie_retypes_v1.json` | `candidate_applied` | `already_applied` | `make_v113`, PR #120 → v113 |
| `patch_candidate_bibliographie_duplicates_v1.json` | `blocked_author_arbitration` | `stale_source_graph_but_preconditions_intact` | — |
| `patch_candidate_bibliographie_missing_nodes_v1.json` | `blocked_missing_applicator` | `blocked_by_missing_applicator` | — |

Champs écrits, selon le cas : `lifecycleStatus`, `lifecycleGeneratedBy`, `measuredAgainstGraph`, `measuredStatus`, et — pour les trois appliqués — `appliedBy`, `appliedInGraph`, `appliedInPR`, `ledgerEntry`. Tous portent un `noteForAgents`.

**Aucun patch hors racine n'est touché.** Les patchs historiques (`patch_1a`…`patch_19`, `new_relations_patch.json`, `patches/**`) ne sont pas soumis à C03 : leur écrire un cycle de vie serait réécrire une archive, ce que la charte interdit. La question ne s'est donc pas posée, et il n'y a rien à arbitrer sur ce point.

---

## 2. Pourquoi

Le contrôle **C03** exige que la `policy` d'un candidat commence par `CANDIDATE — NOT APPLIED — AUTHOR ARBITRATION REQUIRED`. Les applicateurs refusent un patch qui ne la porte pas. **Trois de ces patchs ont été appliqués et portent toujours cette phrase**, en toutes lettres, au présent.

Ce n'est pas un défaut : c'est la convention, et elle a une raison — la policy dit ce que le patch *était au moment de sa rédaction*, pas ce qu'il est devenu. Mais un agent qui lit la policy conclut l'inverse de la vérité, et rien dans le fichier ne le détrompe. Le chantier a consisté à **poser la vérité à côté**, sans toucher à la phrase que C03 protège.

---

## 3. Ce que cela ne change pas

- **Aucune op, aucune `value`.** Prouvé, pas affirmé : le script calcule une signature JSON canonique du patch privé des seules clés de cycle de vie, avant et après, et **refuse d'écrire** si elle diffère. La signature énumère toutes les clés de tête et toutes les clés de `_meta` — une signature qui ne regarderait que ce qu'on pense avoir touché ne prouverait rien (défaut déjà rencontré sur `make_v112`).
- **Aucune `policy`.** Vérifié champ par champ après écriture.
- **Aucun statut mesuré.** L'inventaire et la table de gouvernance sont identiques avant et après : ils lisent les ops, qui n'ont pas bougé. Les deux CSV et le ledger sont inchangés dans ce commit.
- **Aucune autorisation.** Un `blocked_author_arbitration` reste bloqué ; écrire son statut ne l'instruit pas.
- **Le résultat du preflight** : 67 OK / 9 AVERTISSEMENT / 0 BLOQUANT, à l'identique.

---

## 4. Pourquoi C03 reste intact

C03 n'est ni modifié ni contourné. Il teste une seule chose — `policy.startswith(PREFIXE_POLICY)` — et la `policy` n'est pas touchée. Le script ne sait pas écrire dans `policy` : `CLES_LIFECYCLE` est la liste close des clés qu'il peut poser, et tout le reste est verrouillé par la signature.

C'est le sens de l'arbitrage Q4 de #121 (« ne pas modifier C03 maintenant ») : **la contradiction entre la policy et la réalité n'est pas résolue en supprimant la policy, mais en la rendant lisible pour ce qu'elle est.** Un lecteur qui trouve `"policy": "CANDIDATE — NOT APPLIED"` et, quinze lignes plus bas, `"lifecycleStatus": "candidate_applied"` avec l'applicateur, la version et la PR, n'est plus trompé — il apprend en plus que la première phrase est une exigence de forme.

---

## 5. Pourquoi la mesure graphe reste l'autorité finale

C'est le point qui décide si ce chantier est utile ou dangereux, et il est **mécanique, pas déclaratif** :

1. `lifecycleStatus` **n'est jamais saisi à la main.** Il est recopié de `recommended_governance_status`, lui-même dérivé du statut mesuré dans le graphe par `build_patch_queue_inventory.py`. Le script n'expose aucun moyen d'écrire une valeur choisie.
2. **`--check` rougit dès que la déclaration s'écarte de la mesure.** Vérifié en falsifiant à la main `blocked_author_arbitration` → `candidate_active` sur le patch doublons : sortie 1, patch nommé. Une déclaration qui ne peut pas devenir fausse sans qu'on le voie n'est pas une source de vérité concurrente.
3. **Le contrôle est câblé en CI, et il est DUR** — contrairement à l'étape de file, souple par arbitrage Q5. La différence est délibérée : un CSV périmé se régénère et n'autorise rien ; une mention de cycle de vie périmée est exactement le défaut que le chantier corrige.
4. **Le vocabulaire est fermé.** Un statut mesuré hors des sept valeurs arrêtées par l'auteur fait échouer le script au lieu d'être traduit d'office. Si un candidat racine se mesurait un jour `archive_historical`, ce serait une anomalie à instruire, pas une valeur à recopier.
5. **Ledger et file ne peuvent pas se contredire en silence, dans les deux sens.** Un patch mesuré `candidate_applied` mais absent de `patch-application-ledger.json` fait échouer le script plutôt que de produire un bloc d'apparence complète. **Et réciproquement** — c'est un retour de revue : la garde était d'abord asymétrique, elle refusait « appliqué sans ledger » mais acceptait « ledger sans appliqué ». Or c'est ce second cas qui est dangereux : un patch mesuré **bloqué** aurait reçu `appliedBy` et `appliedInPR`, c'est-à-dire les marques extérieures d'une application, sur un fichier que personne n'a le droit d'appliquer. Le désaccord n'est jamais tranché d'office : le script s'arrête et renvoie au graphe.
6. **`appliedInGraph` est résolu, jamais fabriqué.** Construire le nom par interpolation produisait un champ d'apparence juste même si le fichier n'existait pas. Il est désormais cherché parmi les graphes réels du dépôt, et une version introuvable fait échouer le script. De même, le chemin de la table de gouvernance est demandé à `gouv.sortie_pour()` — le seul endroit du dépôt qui décide de ce nom — plutôt que recopié : c'est ce choix, non fait ailleurs, qui avait laissé un pointeur mort vers `…-v113.csv` dans `CLAUDE.md`.

L'ordre de lecture reste celui de #121, et les `noteForAgents` l'écrivent dans chaque fichier : **graphe → file vivante → ledger. Jamais la policy, jamais `lifecycleStatus`.**

---

## 6. Quels patchs restent bloqués

- **`patch_candidate_bibliographie_duplicates_v1.json`** — 156 ops `duplicateOf`, 71 familles, 78 membres. Préconditions intactes, cibles vivantes : **techniquement applicable, scientifiquement non mûr**. Il touche au canonique d'une famille de doublons, c'est-à-dire au piège C5 (« le canonique retenu est-il le mieux relié ? ») et à des affirmations sur des personnes. Son propre `_meta` signale déjà que dans 8 familles le degré du canonique est à égalité avec un autre membre. **À réauditer avant tout chantier d'application** (arbitrage Q7).
- **`patch_candidate_bibliographie_missing_nodes_v1.json`** — 38 `CREATE_ENTITY`. Aucun applicateur du dépôt ne consomme ce type d'op, et le contrat interdit de pré-assigner un `entityId`. Deux verrous distincts : écrire l'applicateur est un chantier technique, décider de créer 38 nœuds bibliographiques est une décision d'auteur. Le premier ne débloque pas le second.

---

## 7. Quels patchs ne doivent pas être rejoués

**Les trois `candidate_applied`.** Leurs ops ont déjà leur effet dans v113 ; un rejeu est au mieux sans effet, au pire écrit à côté si une migration ultérieure a déplacé les cibles. C'est ce que dit leur `noteForAgents`, en toutes lettres et dans le fichier.

Au-delà de la racine — hors périmètre de ce chantier mais dans la même file — la table de gouvernance porte 7 `archive_partial` dont **un rejeu écrirait à côté** (état mixte, ou cibles mortes), et un `indetermine` dont l'effet est inconnu. Ils n'ont pas reçu de `lifecycleStatus` : ce sont des archives, et leur statut se lit dans `patch-queue-governance-cases-current.csv`.

---

## 8. Limites connues

- **La déclaration est une copie, et une copie peut être vieille d'un commit.** `--check` la rattrape en CI, jamais avant. Entre l'écriture et la CI, le fichier peut mentir — brièvement, et jamais sans être vu.
- **Le vocabulaire arrêté compte sept valeurs ; trois seulement sont employées aujourd'hui.** `candidate_active`, `candidate_superseded`, `dangerous_do_not_replay` et `indetermine` n'ont **aucun porteur** et donc aucune note rédigée : le script échouera proprement le jour où l'un d'eux se présentera, plutôt que d'écrire un champ vide. C'est voulu, mais cela veut dire que ces quatre valeurs ne sont pas encore éprouvées.
- **`measuredAgainstGraph` date la mesure, il ne la fige pas.** Il dit contre quel graphe la lecture a été faite, ce qui permet de repérer une déclaration écrite sous une version antérieure — mais seul `--check` tranche.
