# 01 — Audit de la chronologie CSV

**Date** : 2026-08-02
**Source** : `docs/research/catalogue-evenements/catalogue-evenements-v1.csv`
**Branche** : `agent/grc20-add-missing-chronology-events-v1`
**Mode agent** : A (lecture seule sur le CSV — aucune ligne modifiée)

## Provenance du fichier

Le CSV n'est **pas** présent sur la branche de développement `codex/create-expand-from-node-planning-documents`. Il provient de la PR #98 (`agent/catalogue-evenements-v2`), non mergée à ce jour.

Il est donc versé ici **au même chemin et avec les mêmes octets** que dans la PR #98 : `docs/research/catalogue-evenements/catalogue-evenements-v1.csv`. Deux ajouts identiques du même fichier au même chemin fusionnent sans conflit, quel que soit l'ordre de merge. Cette PR reste ainsi auto-portante — le script d'appariement s'exécute depuis la seule branche de base.

## Structure

**78 lignes, 18 colonnes**, séparateur `;`, encodage UTF-8.

```
id ; date ; precision ; nature ; intitule ; phase ; domaine_8 ; systeme ;
acteur_principal ; acteur_secondaire ; arene ; type_acte ; type_acte_2 ;
effet_prop_monetaires ; crise ; fil ; source ; notes
```

Identifiants `E001`–`E078`, séquentiels et stables. Bornes temporelles : **2008-07-18 → 2019**.

Colonnes exploitées pour l'appariement : `id`, `date`, `precision`, `intitule`, `phase`, `nature`, `crise`, `systeme`, `domaine_8`, `source`, `notes`. Les colonnes de codage analytique (`acteur_principal`, `arene`, `type_acte`, `effet_prop_monetaires`) ne sont pas mobilisées : elles relèvent du chantier catalogue, pas de la complétion du graphe.

## Répartition

### Par phase — c'est l'enjeu de cette PR

| Phase | Lignes | Part |
|---|---:|---:|
| `poc` — preuve de concept | 32 | 41 % |
| **`peche` — péché** | **13** | **17 %** |
| **`maturation`** | **33** | **42 %** |

Les deux phases prioritaires totalisent **46 lignes**, soit 59 % du catalogue.

### Par nature

| Nature | Lignes |
|---|---:|
| `acte` — un acte situé | 68 |
| `seuil` — un palier ou une statistique | 10 |

**La distinction est décisive pour cette PR.** Un `seuil` n'est pas un acte : « Cours proche de 1000 dollars » ou « Transactions illégales sous 1 pct » décrivent un état de marché ou une mesure, pas une intervention sur l'infrastructure. Les typer `InfrastructureEvent` serait une erreur de catégorie. Le traitement de ces 10 lignes est arbitré dans `04-semantic-check.md`.

### Par précision de date

| Précision | Lignes |
|---|---:|
| `jour` | 25 |
| `mois` | 20 |
| `annee` | 33 |

**33 lignes sur 78 ne sont datées qu'à l'année.** Aucune n'est vide. La normalisation ISO opérée par le script d'appariement (`AAAA`, `AAAA-MM`, `AAAA-MM-JJ`) **n'écrase pas la forme d'origine** : la colonne `date_csv` du fichier de classification conserve la valeur brute, et le patch reprendra la forme originale.

### Par système et par statut de crise

| Système | Lignes | | Crise | Lignes |
|---|---:|---|---|---:|
| `bitcoin` | 59 | | `non` | 67 |
| `ethereum` | 12 | | `oui` (toutes formes) | 11 |
| `altcoin` | 4 | | | |
| `transversal` | 3 | | | |

Les 11 lignes `crise=oui` portent une qualification hétérogène : `oui`, `oui (n 4)`, `oui (n 19)`, `oui (sequence DAO)`, `oui (post-fork)`, `oui (sequence CVE-2018)`. Le numéro de crise, quand il est présent, renvoie à la numérotation de la thèse — la même que l'attribut `crisisNumber` du graphe.

## Couverture des colonnes

Trois colonnes seulement sont incomplètes, et aucune n'est utilisée pour décider d'un ajout :

| Colonne | Rempli |
|---|---|
| `acteur_secondaire` | 13/78 |
| `type_acte_2` | 4/78 |
| `notes` | 60/78 |

Toutes les colonnes mobilisées pour l'appariement sont **remplies à 78/78**.

## Réserves déclarées par le CSV lui-même — 10 lignes

Le catalogue signale ses propres incertitudes par un marqueur `[CHANTIER]` en note. C'est un signal de qualité qu'il serait fautif d'ignorer : **une ligne dont le CSV dit lui-même que la date n'est pas établie ne satisfait pas le critère « suffisamment datée ou situable »**.

| id | Intitulé | Réserve déclarée |
|---|---|---|
| E001 | Dépôt du nom de domaine bitcoin.org | l.113 situe l'enregistrement en janv. 2009 |
| E022 | Création de Bitcoin Magazine | fig. situe la première publication en 2012 (CSV : 2011) |
| **E025** | **Création de la procédure BIP (Taaki)** | **date non donnée dans les fichiers autorisés** |
| E034 | Création de Coinbase | localisation texte de la création |
| E051 | Fixation effective du cap des 21 M | n° (24 ?) à confirmer |
| E052 | Tether (USDT) | date non donnée dans le texte |
| E055 | Faillite de MtGox | localisation texte hors fichiers autorisés |
| E062 | Lancement d'Ethereum Frontier | fig. indique 30/07, texte 20/07 |
| E063 | Mise en ligne de The DAO | date déduite, à vérifier |
| E067 | Hard Fork d'Ethereum | date exacte à relever |

Le script d'appariement remonte cette réserve dans une colonne `reserve_csv` du fichier de classification, et **déclasse en `TOO_AMBIGUOUS`** toute ligne dont la réserve porte sur la date ou la localisation textuelle. C'est ce mécanisme qui a écarté **E025** de la liste des ajouts : sa date « 2011 » n'est appuyée par aucune source autorisée.

## Problèmes de libellé relevés

- **Le CSV est en français, le graphe est bilingue.** C'est le principal risque d'erreur d'appariement : « Enregistrement de genèse » (E003) et « Genesis Block / lancement du protocole » désignent le même fait sans partager un seul token. Ce risque est traité dans `03-matching-report.md` par un mécanisme d'ancres et par une passe adverse.
- **Les identifiants techniques sont écrits de deux façons.** « BIP16 » (CSV) et « BIP 16 » (graphe) : un simple espace suffisait à faire échouer l'appariement. Corrigé par une ancre « préfixe + numéro » recollée.
- **Aucun accent ni caractère de contrôle problématique.** Le CSV est en texte non accentué (« genese », « pecheresses »), le graphe est accentué. La normalisation NFD règle ce point.

## Ce que cet audit ne fait pas

- Il ne corrige aucune ligne du CSV.
- Il ne tranche aucune des 10 réserves `[CHANTIER]`.
- Il ne se prononce pas sur les colonnes de codage analytique du catalogue.
