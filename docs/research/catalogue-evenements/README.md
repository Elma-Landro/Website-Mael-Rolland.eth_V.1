# Catalogue d'événements — instrument de recherche

**Ce dossier ne fait pas partie du graphe GRC-20.** Il conserve un instrument de travail du chantier de valorisation de la thèse : un catalogue d'événements construit par croisement du graphe `grc20-these-mael-rolland-v97.json` avec un catalogue de calibrage établi à la lecture du texte.

Rien ici n'est une source d'autorité pour le graphe. Aucun fichier de ce dossier n'est consommé par le runtime, par les scripts de publication, ou par une quelconque chaîne de build.

## Contenu

| Fichier | Nature |
|---|---|
| `catalogue-evenements-v1.csv` | catalogue de calibrage, 78 événements relevés dans le texte de la thèse (ch. I et III), 18 colonnes analytiques |
| `fusion.py` | script de fusion graphe × calibrage |
| `table-divergences-dates.csv` | 5 divergences de dates texte/graphe, **non tranchées** |
| `etat-catalogue-evenements-v2-2026-08-02.md` | état de chantier du 02/08/2026, avec les points à arbiter |

## Le catalogue v2 n'est pas versionné — il se régénère

`catalogue-evenements-v2-fusion.csv` (253 lignes : 78 issues du calibrage dont 32 enrichies par le graphe, plus 175 issues du graphe) est un **artefact dérivé**. Il n'est pas versionné : il se reconstruit à partir des trois entrées présentes ici et dans le dépôt (le graphe v97, `catalogue-evenements-v1.csv`, `fusion.py`).

**Attention** : `fusion.py` est versé **tel qu'il a été écrit**, avec ses trois constantes de chemin d'origine, qui pointent hors du dépôt :

```python
GRAPH = '/home/claude/site/grc20-these-mael-rolland-v97.json'
CAL   = '/mnt/user-data/outputs/catalogue-evenements-v1.csv'
OUT   = '/mnt/user-data/outputs'
```

Il faut les repointer vers le dépôt pour le rejouer. Contrairement à `scripts/verif_doublons.py`, ce script n'a pas reçu d'interface en ligne de commande : ce n'est pas un outil du dépôt, c'est une pièce de chantier conservée en l'état.

Rejeu vérifié le 02/08/2026 avec les chemins repointés : **213 événements bruts → 207 après dédoublonnage interne (6 fusionnés, 5 groupes), 32/78 appariés au calibrage, 253 lignes au total, 5 divergences de dates**, et `table-divergences-dates.csv` régénéré **octet pour octet identique** au fichier versé ici.

## Chantiers ouverts

Ils sont listés dans `etat-catalogue-evenements-v2-2026-08-02.md`, section `[CHANTIER]`. Les principaux :

- les **5 divergences de dates** texte/graphe (`table-divergences-dates.csv`), non arbitrées ;
- **175 lignes** à coder sur `acteur_principal`, `arene`, `type_acte` ; **94** sur `domaine_8` ;
- le graphe **n'a aucun domaine correspondant à (ii) traitement des transactions** (ch. I l.251) : les événements de minage arrivent sans domaine.

## Relation avec l'audit de dédoublonnage

Le dédoublonnage des événements *du graphe* est un chantier distinct, versé séparément : voir `docs/audits/grc20-dedup-events-audit-v1.md` et son patch `patch_10_dedup_events.json`. Les deux chantiers partagent une origine (session du 02/08/2026) et un objet (les événements), mais pas leur portée : l'audit porte sur le graphe et produit un patch ; ce dossier-ci est un instrument de lecture qui ne touche pas au graphe.
