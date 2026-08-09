# Brouillon — politique de cycle de vie de la file de patchs

**NON APPLIQUÉ.** Ce document décrit la politique **telle qu'elle serait si elle était adoptée**. Aucune de ses règles n'est en vigueur ; rien dans le dépôt ne s'y conforme encore. Il n'a d'effet qu'après arbitrage de l'auteur.

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

Un fichier ne peut pas être les deux. En cas de doute, c'est une preuve figée : on perd de la fraîcheur, jamais de la vérité.

## Règle 3 — Nommage : le suffixe dit la nature

- inventaire vivant → `…-current.csv` ;
- preuve figée → `…-vNNN.csv`.

Conséquence directe : un `--check` sur un fichier `-current` ne casse jamais au bump de version, et un `--check` sur un `-vNNN` doit nommer son graphe (`--graph`), jamais « le plus récent ».

## Règle 4 — Un patch appliqué le dit dans son propre fichier

`_meta.lifecycleStatus` est ajouté à l'application, sans toucher `policy` :

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

La CI vérifie que l'outil de file **tourne** ; elle n'exige pas que le CSV soit à jour. Motif : au 2026-08-09, **un seul artefact sur 31 est encore applicable**, et il est gelé par arbitrage. Un contrôle strict rougirait à chaque bump de version pour protéger ce seul fichier.

Cette règle est à revoir si le nombre de candidats actifs remonte — c'est la seule des six qui dépende d'un chiffre.
