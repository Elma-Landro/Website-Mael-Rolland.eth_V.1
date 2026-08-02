# 02 — Inventaire du graphe : conventions à respecter

**Date** : 2026-08-02
**Graphe** : `grc20-these-mael-rolland-v97.json` (2 263 entités, 20 042 relations, 55 types, 130 types de relations)
**Mode agent** : A (lecture seule)

Objet : relever les conventions auxquelles une entité ajoutée doit se conformer pour être indiscernable des 213 événements existants.

## Population événementielle

**158 `InfrastructureEvent`** (type `49a98b36b4a94099a4d35ee6ca46f629`) et **55 `CrisisEvent`** (type `60d73f836afb4d6ebcccea0d0491ac87`). Tous les événements sont **mono-typés** : aucun ne porte deux types. Aucun n'est orphelin — chaque `InfrastructureEvent` a au moins 2 relations sortantes (médiane 7,5, maximum 32).

## Forme d'une entité

```json
{
  "id": "70d79dda054d462086a5472657b011a7",
  "name": "InfrastructureEvent — Genesis Block / lancement du protocole",
  "description": {"type": "TEXT", "value": "…", "options": {"language": "fr"}},
  "types": ["49a98b36b4a94099a4d35ee6ca46f629"],
  "attributes": { "date": …, "dateSource": …, "description": …, "chapter": … }
}
```

Points structurants :

- `types` est une **liste d'identifiants de type**, jamais de noms.
- `description` existe **deux fois** : une forme courte au niveau racine et une forme longue dans `attributes`. 158/158 `InfrastructureEvent` portent la racine, 141/158 portent celle des attributs.
- La `description` racine est un **objet de valeur**, pas une chaîne nue.
- L'ordre des clés varie d'une entité à l'autre : il n'est pas porteur de sens.

## Identifiants

**Les 2 263 identifiants d'entité sont des chaînes de 32 caractères hexadécimaux minuscules. Zéro exception.** Pas de préfixe, pas de tiret, pas de majuscule. Environ 2 030 sont des `uuid4().hex` ; le reste est de l'aléatoire hexadécimal uniforme.

Les identifiants de **relation**, en revanche, sont hétérogènes : 32 hex, base58 sur 22–23 caractères, UUID à tirets sur 36 caractères, et 3 identifiants tronqués à 16 caractères (dette connue, documentée dans `patches/grc20_v97_remove_15_truncated_broken_relations.json`). Ils ne sont **pas** dérivés du contenu : aucune correspondance trouvée entre md5 de `from|type|to` et les 3 001 identifiants hexadécimaux testés. Pour une relation neuve, la forme 32 hex est la majoritaire et celle des patches récents.

## Attributs des événements — fréquence

| Attribut | Total | IE | CE |
|---|---:|---:|---:|
| `date` | 181 | 139 | 42 |
| `description` | 141 | 141 | 0 |
| `dateSource` | 75 | 75 | 0 |
| `chapter` | 69 | 65 | 4 |
| `crisisType` | 46 | 0 | 46 |
| `crisisNumber` | 42 | 0 | 42 |
| `dateAuthority` | 37 | 37 | 0 |
| `cveId` | 31 | 0 | 31 |
| `thesisLocation` | 9 | 9 | 0 |

**Six attributs seulement comptent pour un `InfrastructureEvent` neuf** : `date`, `description`, `dateSource`, `chapter`, et optionnellement `dateAuthority` et `thesisLocation`. Les attributs `crisisType`, `crisisNumber`, `cveId`, `severity`, `exploited` sont **exclusivement** portés par des `CrisisEvent` : les employer sur un `InfrastructureEvent` serait une faute de typage.

## Forme des valeurs — règle stricte

- **`TEXT` porte toujours `options.language`**, valant `fr` ou `en`. Aucune autre langue n'existe.
- **`URL`, `NUMBER` et `TIME` n'ont jamais de clé `options`.**

Répartition des langues : `description` 100 % fr, `dateSource` 100 % fr, `chapter` 100 % fr, `dateAuthority` 100 % en, `crisisNumber` 100 % en. `date` est mixte (135 fr / 45 en) ; le lot le plus récent, celui issu de la chronologie, emploie `en`.

Formats de `date` sur les `InfrastructureEvent` : `YYYY-MM-DD` (50), `YYYY` (41), `YYYY-MM` (26), `DD/MM/YYYY` (20), plus 2 valeurs en prose. Aucune normalisation n'est imposée par le graphe.

## Nommage

**139 `InfrastructureEvent` sur 158, soit 88 %, portent le préfixe littéral `InfrastructureEvent — `** (tiret cadratin, espaces des deux côtés). Aucune variante n'existe : ni tiret demi-cadratin, ni deux-points, ni tiret simple. C'est la convention majoritaire, et les 19 exceptions sont un lot ancien.

**Aucun `CrisisEvent` ne porte de préfixe** — 0/55. Leurs noms sont nus, en trois familles : style CVE, style BIP, et prose.

## Relations sortantes des événements

2 481 relations partent des 213 événements. Les plus fréquentes :

| Relation | Total | Identifiant |
|---|---:|---|
| `appears in section` | 1 638 | `f004d0e68f0964e8787d19b350e3ca24` |
| `belongs to domain` | 216 | `f7f1c5e7b4604f2cbecaca60e8dbada9` |
| `occurs in` | 151 | `d3b2d5c9c2194536be63dc04dfa1daf8` |
| `mentions actor` | 80 | `f13ff5887b7c4997ab84ac27e1b2d3a3` |
| `contributes to` | 52 | `e279d673d83443bc95f641070d3a012e` |
| `precursor of` | 11 | `98142520f9304dbea0a3027f375d97f7` |

Forme d'une relation : `{"id", "type", "from", "to", "attributes"}`, où `type`, `from` et `to` sont **toujours des identifiants**, jamais des noms. L'absence d'attributs se code `"attributes": []` — un **tableau vide**, pas un objet vide. Les relations `appears in section` portent en outre `section_key` (TEXT/fr) et `page_approx` (NUMBER nu).

Câblage minimal observé sur un événement issu de la chronologie : 1 `occurs in` vers une phase, 1 à 2 `belongs to domain`, 1 `appears in section`.

## Vocabulaires contrôlés

### `DevelopmentPhase` — cible de `occurs in`

| Identifiant | Nom | Usages |
|---|---|---:|
| `6414d87541f941a0b428c536ce72e032` | Phase de preuve de concept | 64 |
| `019689c1ce06489a84768c51637eb9ed` | Phase de péché | 45 |
| `eed0b89cd2e740718059c16591f9bfb7` | **Phase de maturation** | **1** |

**Ce déséquilibre est le constat central de ce chantier.** Il est traité dans `05-final-synthesis.md`. À noter aussi un doublon : le `Concept` « Phase de maturation / Phase 3 Bitcoin » (`645079ad66ee41b689112d383dd54798`) est employé 25 fois, en concurrence avec la `DevelopmentPhase` homonyme.

### `InfrastructureDomain` — cible de `belongs to domain`

Huit entités, dont sept servent effectivement de cible :

| Identifiant | Nom | Couleur |
|---|---|---|
| `d47c813a4d0c424cb80422ff6e6109f9` | Sphère d'usage | vert |
| `55b5215088664257819b56a918ec67fd` | Services de portefeuille et de paiement | orange |
| `d8b2aecc33714e7dbe6864d9c18b6763` | Information et connaissance | bleu foncé |
| `3960e7b3294c4364bca1b046734ef886` | Conformité réglementaire | bleu clair |
| `3b17f5b612b54376963e5aa7fe13fff8` | Protocole et couche de base | rouge |
| `bb565b2132f5430eac529b953711be41` | Altcoins, tokens et surcouches | rose |
| `273dcf0b4f784d78afc99c800c4a3be6` | [Résiduel — à reclasser] | violet |
| `f81356a445e6433a9b5f69a85178bae7` | De la confidentialité et de l'anonymisation | — |

Anomalie relevée sans être corrigée : `belongs to domain` vise aussi 30 fois un `Concept` (« Traitement des transactions ») et 24 fois une `ThesisSection` — cibles hors vocabulaire.

### `ThesisSection` — cible de `appears in section`

61 cibles distinctes, dont 42 déjà employées depuis des événements. La cible canonique pour un événement de chronologie est `93f13f18c6da412292eba80dcd630ac7` (I.2.1, 144 liens événementiels).

## Un type que le chantier a révélé : `PriceWindow`

Le graphe possède un type **`PriceWindow`** (10 entités) et un type `PriceSeries`, faits pour porter les paliers de cours :

| Identifiant | Nom | date | priceUSD |
|---|---|---|---|
| `4d2430ba5c22456387bea785f5b42a67` | PriceWindow — Pic décembre 2013 (~1000$) | 2013-12 | ~1000 |
| `ee7d24e80387457fb271f75f1db49446` | PriceWindow — Pic décembre 2017 (~20 000$) | 2017-12 | ~20000 |
| `951169948e214b3f97ee0515977010b0` | PriceWindow — Point bas 2018-2019 (~3300$) | 2018-2019 | ~3300 |
| `d7b4845bbc4448708a5f7113368ccce6` | PriceWindow — Stabilisation 2019-2020 (~8000$) | 2019-2020 | ~8000 |

**C'est la convention du graphe pour les cours, et elle interdit d'ajouter les paliers du CSV comme `InfrastructureEvent`.** Voir `04-semantic-check.md`.

## Le fichier lui-même

Clés de tête : `space`, `types`, `relation_types`, `entities`, `relations`, `ops`.

`ops` compte 293 entrées, **toutes de forme identique** `{type, entityId, attributeId, value}`, toutes des `SET_ATTRIBUTE` sur l'attribut `definition`. C'est un canal d'attribut différé, pas un journal de modifications : **une entité neuve n'a aucune entrée à y ajouter**.

`space` porte `version` (`"v97"`), `generated_at` et une `note` cumulative décrivant les versions successives — c'est là que la construction de v98 inscrit sa trace.
