# Brouillon — politique de cycle de vie de la file de patchs

**Statut au 2026-08-09 : ARBITRÉ, partiellement en vigueur.** Les huit questions ont reçu réponse. Les règles 1, 2 bis, 3, 5, 6 et 7 sont **appliquées** par cette PR ; la règle 4 (`lifecycleStatus` sur les patchs existants) est **acceptée mais renvoyée à un chantier dédié**, et rien dans le dépôt ne s'y conforme encore.

**Le vocabulaire de statuts retenu par l'auteur** : `candidate_active`, `candidate_applied`, `candidate_superseded`, `archive_partial`, `archive_historical`, `blocked_author_arbitration`, `blocked_missing_applicator`, `blocked_identity_model`, `dangerous_do_not_replay`, `indetermine`.

---

## Règle 1 — Le statut se mesure, il ne se déclare pas

Le statut d'un patch se lit **dans le graphe courant**, jamais dans sa `policy`, son `patch_id` ou sa description. Un patch dont toutes les opérations lisibles ont déjà leur effet est appliqué, quoi qu'il proclame.

C'est la règle qui rend les autres possibles, et elle est déjà appliquée par `build_patch_queue_inventory.py`.

## Règle 2 — Quatre natures, quatre traitements

| Nature | Exemple | Régénération | `--check` |
|---|---|---|---|
| **preuve figée** | `chronology-date-inventory-v111.csv` | **jamais** — elle décrit une version passée | contre son graphe déclaré |
| **inventaire vivant** | la file de patchs | après chaque version | contre le graphe courant |
| **archive historique** | `patch_1b`, `new_relations_patch.json` | sans objet | sans objet |
| **candidat actif** | `patch_candidate_bibliographie_duplicates_v1.json` | sans objet | preflight |

**Règle 2 bis — un artefact que l'outil ne sait pas lire est `indetermine`, jamais `archive_historical`.** Sur les quatre statuts, « archive historique » est le **moins** conservateur : il autorise à ne plus rien instruire. Le retomber par défaut a déjà classé « lot intégré » un patch appliqué à 0/10.

Un fichier ne peut pas être les deux. En cas de doute, c'est une preuve figée : on perd de la fraîcheur, jamais de la vérité.

## Règle 3 — Nommage : le suffixe dit la nature

- inventaire vivant → `…-current.csv` ;
- preuve figée → `…-vNN.snapshot.csv`.

Le suffixe `.snapshot` n'est pas décoratif : `-vNNN.csv` est déjà la forme des CSV produits avant l'arbitrage, donc il ne distinguerait pas une preuve figée d'un fichier simplement périmé. C'est la forme que `sortie_pour()` écrit dans les deux générateurs.

Conséquence directe : un `--check` sur un fichier `-current` ne casse jamais au bump de version, et un `--check` sur un `-vNN.snapshot` doit nommer son graphe (`--graph`), jamais « le plus récent ». Corollaire appliqué : viser un graphe qui n'est pas le courant **écrit un snapshot** au lieu d'écraser le vivant.

## Règle 4 — Un patch appliqué le dit dans son propre fichier

`_meta.lifecycleStatus` serait ajouté à l'application, sans toucher `policy`. **Accepté par l'auteur, mais pas appliqué ici** : il vaut pour les patchs *nouveaux*, et pour les patchs existants seulement lors d'un chantier dédié. Il **ne remplace pas la mesure** — il aide la lecture humaine.

```json
"lifecycleStatus": {
  "state": "applied",
  "applied_by": "scripts/make_v113_apply_bibliography_retypes.py",
  "produced": "grc20-these-mael-rolland-v113.json",
  "date": "2026-08-09"
}
```

`policy` reste inchangée — C03 continue de passer. La contradiction apparente est **assumée et expliquée** par le champ lui-même : la `policy` décrit ce que le patch était au moment de sa rédaction, `lifecycleStatus` ce qu'il est devenu.

## Règle 5 — Un patch historique partiel ne se rejoue pas

Les artefacts en état mixte portent `archive_partial` et **ne sont jamais des candidats**. Sept sont concernés, dont `new_relations_patch.json` (6 246/11 884) et `patch_2b_central_arguments.json` (49/49 lisibles, mais 7 cibles mortes).

Le mot `already_applied` leur est **interdit** : il sur-promet dès qu'une cible manque.

## Règle 6 — La CI ne garde que ce qui peut encore bouger

La CI vérifie que l'outil de file **tourne** ; elle n'exige pas que le CSV soit à jour. Motif : au 2026-08-09, **deux artefacts sur 31 sont encore applicables**, tous deux gelés par arbitrage. Un contrôle strict rougirait à chaque bump de version pour les protéger.

**Cette règle est la seule des sept qui dépende d'un chiffre, et ce chiffre est mobile.** Il ne compte que ce qui est applicable sans écrire de code : il exclut le patch de créations (38 ops) que seul un applicateur manquant bloque, et les 4 archives `Migration/*.zip` hors périmètre. À revoir dès que le nombre de candidats actifs remonte.

## Règle 7 — Adopter la politique impose une transition, qui doit être écrite

Le jour de son adoption, la Règle 5 rendrait `build_patch_queue_inventory.py` non conforme : le CSV d'inventaire versé écrit `already_applied` pour `patch_2b_central_arguments.json`, qui porte 7 cibles mortes. Une politique qui ne dit pas comment on y arrive n'est pas applicable. La transition — quel outil corrige quoi, dans quel ordre, et ce que CLAUDE.md doit pointer — reste à écrire.
