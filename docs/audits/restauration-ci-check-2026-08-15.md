# Restauration de la CI `check.yml` — note d'audit (tient lieu de note de PR) — 15/08/2026

Mission : restaurer le garde-fou CI supprimé par erreur, avant tout nouveau codage catalogue. Aucun autre chantier. Cette note documente ce qui est restauré, depuis où, ce qui ne l'est pas, ce qui tourne à nouveau, et pourquoi rien du runtime ne change.

## Ce qui a été supprimé, et ce qui est restauré

Le commit `12d7574` (« Delete .github/workflows directory », 15/08 22:18 UTC, interface web) a supprimé **un seul fichier** : `.github/workflows/check.yml` — 147 lignes, 7 290 octets, blob git `18c63716ff7c5eb26eed0b23d4c5fb819d165e97`. C'est la CI du dépôt : elle tournait sur chaque push et chaque PR.

**Version restaurée : l'état exact du parent `fb0f69d`** — octets identiques, blob `18c63716…`. C'est aussi la version la plus récente ayant jamais existé : l'historique du fichier (`4faef82` création → `d255d30` → `b58465a` → `aec851c` durcissement lot 1 → `cabad85` étape souple de file → `3e81332` retours de revue → `af5024a` contrôle dur lifecycleStatus) s'arrête là. **Aucun contrôle stabilisé postérieur n'existe : rien à ajouter, rien n'est inventé** (points 6-7 du mandat).

**Non restauré, volontairement** : `bootstrap-catalogue-0508.yml` — échafaudage mort du 15/08, supprimé délibérément le matin même (`67224b7`) ; il n'était d'ailleurs pas dans `12d7574`.

## Canal de restauration

Le garde-fou de la session Cowork interdit de pousser tout fichier sous `.github/workflows/` (leçon 5 du canal, BLOC A du prompt lot 2) — légitime : code auto-exécutant. Aucune tentative n'a donc été faite par le connecteur. La restauration passe par le **canal web de Maël, fidèle à l'octet** (fichier fourni par la session), avec vérification d'empreinte après dépôt : `check.yml` restauré doit porter le blob `18c63716ff7c5eb26eed0b23d4c5fb819d165e97`. Pas de nouvelle branche (règle du chantier) : la restauration est un commit direct dédié sur la branche de travail ; la présente note tient lieu de note de PR.

## Les contrôles qui tournent à nouveau (11 étapes, vérifiées une à une)

`checkout` · Syntaxe JavaScript (node --check) · Validité JSON · **Intégrité structurelle du graphe** (`check_graph_integrity.py`, seul le graphe courant est bloquant, tolérance nommée `9dee2daa…`) · **Cohérence de l'ancrage** (`check_anchoring.py`, baseline 46 connus) · **Poids d'ancrage à jour** (`build_anchor_weights.py --check`) · **Registre des propriétés à jour** (`build_properties_registry.py --check`) · **Preflight des patchs candidats** (`preflight_candidate_patches.py`) · **File de patchs, gouvernance, ledger** (étape souple : outils déterministes, artefacts comparés) · **lifecycleStatus = mesure du graphe** (contrôle dur, `build_patch_lifecycle_status.py --check`) · Récapitulatif. Déclencheurs : push (toutes branches), pull_request, workflow_dispatch. YAML validé (`yaml.safe_load`).

## Validation locale — chaque étape rejouée sur le clone à jour (tête `ccc6056`)

| étape | résultat |
|---|---|
| Syntaxe JavaScript | 27 fichiers, tous OK |
| Validité JSON | 63 fichiers, tous OK |
| Intégrité du graphe | OK — v115 bloquant : 0 partout ; 3 clés dépréciées attendues (post-patch_19) |
| Ancrage | OK — baseline 46, aucune régression |
| Poids d'ancrage | OK — carte à jour (75 clés) |
| Registre des propriétés | **ROUGE au moment de l'audit — voir ci-dessous, corrigé** |
| Preflight candidats | 97 OK · 18 avertissements · 0 bloquant |
| File/gouvernance/ledger | 3 artefacts régénérés deux fois, identiques ; fichiers restaurés |
| lifecycleStatus | OK — chaque déclaration égale la mesure |

## Le seul rouge, mesuré et corrigé : la fraîcheur du registre

Cause **mesurée** (diff complet) : `scripts/add_statut_ligne.py`, poussé au lot 2, lit cinq clés du graphe (`date`, `gid`, `notes`…) ; le générateur du registre l'indexe donc en `readBy`. Le registre commité prédatait ce script : la règle maison « régénérer le registre dans le même commit » (CLAUDE.md) n'a pas été suivie lors du push du script — manquement de la session lot 2, assumé ici. Correctif : **registre régénéré par son propre script** (`build_properties_registry.py`, jamais d'édition manuelle) — diff : **5 insertions `readBy`, zéro clé ajoutée ou retirée, zéro count, statut ou vocabulaire modifié** (338 entrées, source v115). Après régénération : `--check` vert, intégrité du graphe inchangée. Le fichier régénéré (142 910 octets, blob `1ff2dc5a2a2ec42afc3710df98f34c1d67efa41c`) dépasse le plafond du connecteur (~143 Ko échouent) : il passe par le même upload web, **avant** `check.yml`, pour que le premier run de la CI restaurée soit vert.

## Pourquoi aucun comportement runtime n'est modifié

Les deux fichiers touchés sont : un workflow CI (des contrôles en lecture seule, rien n'installe, rien n'écrit hors `/tmp` du runner) et un fichier **généré** (le registre, invariant de CI). Le graphe v115 est inchangé (aucun patch), le catalogue est inchangé (v3-1, v3-2, fichiers d'épreuve intacts), les vocabulaires gelés (Q7 v1, grille de rôles v0) sont intacts, le site est intact, aucune donnée du lot 2 n'est touchée.

## Empreintes attendues après restauration

| fichier | blob git attendu |
|---|---|
| `.github/workflows/check.yml` | `18c63716ff7c5eb26eed0b23d4c5fb819d165e97` |
| `grc20-properties-registry-v1.json` | `1ff2dc5a2a2ec42afc3710df98f34c1d67efa41c` |

Vérification faite par la session après dépôt (empreintes + run Actions vert), consignée en réponse.
