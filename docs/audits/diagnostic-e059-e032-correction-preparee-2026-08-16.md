# E059 et E032 — corrections préparées, non appliquées — 16/08/2026

Suite des arbitrages Maël du 16/08/2026, points 2 et 3 du mini-lot de finition. Complète `diagnostic-e060-e059-e032-2026-08-16.md`, qui posait les citations ; ce document-ci ajoute la résolution au graphe et **la spécification exacte de ce qui serait écrit**.

**Aucune cellule du catalogue maître n'a été modifiée. Aucun rôle n'a été posé sur E059 ni sur E032. Aucun graphe touché, aucun doublon corrigé.** Les sorties attendues de ce lot ne comprenaient pas d'écriture au maître : la correction est donc **préparée et documentée**, pas appliquée.

---

## E059 — « Levée record Coinbase (75 M $) », 2015

### 1. L'entité graphe existe

Recherche menée sur **tous** les champs de nom que le dépôt impose de croiser — `name`, `nameEn`, `labelEn`, `labelFr`, `aliases` — dans le graphe courant **v115** :

| identifiant | type | nom | ce que c'est |
|---|---|---|---|
| **`8991d9f05d234b6d876d16334f60af63`** | `Organization` | **Coinbase** | **l'acteur** — « Exchange et wallet Bitcoin fondé en 2012. Indicateur de l'adoption grand public. Source: Chap. I. » |
| `c660948f388a48109a791a6a00e1dc3a` | `ActorNonHuman` | Coinbase Commerce | le **service de paiement marchand** de Coinbase — autre objet, à ne pas confondre |
| `7cda4562e3ee4e9c8bf969bdf639994a` | `InfrastructureEvent` | Coinbase : croissance et levée de fonds 75M$ (2015) | **l'événement**, pas l'acteur |

**L'identifiant d'acteur à retenir est `8991d9f05d234b6d876d16334f60af63`.** Les deux autres sont des homonymes de famille : l'un est un service, l'autre est l'événement lui-même. Confondre l'acteur et l'événement dans `acteur_principal_id` produirait exactement le genre d'erreur que la colonne est censée éviter.

`8991d9f0…` n'est référencé par **aucune ligne** du catalogue à ce jour.

### 2. Ce que la correction écrirait, cellule par cellule

| colonne | avant | après |
|---|---|---|
| `acteur_principal` | `institutions_financieres` | **`entrepreneurs_exchanges`** |
| `acteur_secondaire` | `entrepreneurs_exchanges` | **`institutions_financieres`** |
| `acteur_principal_mode` | *(vide)* | **`initiateur`** |
| `acteur_principal_id` | *(vide)* | **`8991d9f05d234b6d876d16334f60af63`** |
| `acteur_principal_nom` | *(vide)* | **`Coinbase`** |

Tout le reste est inchangé — `statut_ligne` reste `validee`, `nature`, `date`, `type_acte`, `arene`, `effet_prop_monetaires` ne bougent pas.

Fondement : note 90, ch.I l.639 — « **L'entreprise Coinbase réalise** la plus grande levée de fonds d'alors avec 75 millions de dollars. » L'agent est Coinbase ; les financeurs ne sont pas nommés. La règle A2/D7 donne alors `acteur_principal` = initiateur de l'acte, et le mode `initiateur` du vocabulaire A1.

**Effet mesuré si la correction est appliquée** : `institutions_financieres` passe de **7 à 6** lignes en acteur principal, `entrepreneurs_exchanges` de **16 à 17**. La matrice acteurs × rôles en tiendra compte automatiquement — elle lit le CSV.

### 3. Ce que j'ai trouvé en cherchant l'identifiant, et qui doit être connu avant de corriger

**E059 a un jumeau : G110.**

| | E059 | G110 |
|---|---|---|
| intitulé | Levée record Coinbase (75 M dollars) | Coinbase : croissance et levée de fonds 75M$ (2015) |
| date | 2015 (année) | 2015 (année) |
| origine | `catalogue` | `graphe` |
| `statut_ligne` | **`validee`** | **`chantier`** |
| `gid` | *(vide)* | **`7cda4562e3ee4e9c8bf969bdf639994a`** |
| `acteurs_graphe` | *(vide)* | `Coinbase` |
| `acteur_principal` | `institutions_financieres` | *(vide)* |

Les deux lignes décrivent **le même fait**. La ligne validée n'est pas reliée au graphe ; la ligne reliée au graphe n'est pas validée et n'a pas d'acteur principal. C'est la configuration exacte déjà rencontrée en lot 3 sur E015 ↔ G001, tranchée alors par l'arbitrage M2 en désignant une canonique.

**Je ne l'ai pas traitée** : la consigne de ce lot dit de ne pas corriger les doublons. Mais corriger l'acteur principal de E059 sans savoir que G110 existe reviendrait à stabiliser une ligne en ignorant sa jumelle — et c'est précisément le genre d'angle mort que le dépôt paie cher. **La question du doublon devrait être tranchée avant, ou en même temps que, la correction d'acteur.**

> **Questions, dans l'ordre où elles se posent.**
> **(a)** E059 et G110 sont-elles la même ligne ? Si oui, laquelle est canonique ?
> **(b)** Ratifies-tu l'inversion d'acteur principal sur E059 telle qu'elle est spécifiée au §2 ?
> Une fois (a) et (b) tranchées, j'écris l'applicateur borné — et les rôles suivront, dans un lot distinct.

---

## E032 — « Entrée du capital-risque (2,1 M $) », 2012

### 1. Traitement retenu : seuil / mesure agrégée

Conformément à ton arbitrage : **pas de rôle, ni maintenant ni forcé plus tard**. La ligne mesure un flux annuel, elle ne raconte pas un acte à agent identifiable.

Rappel de la source, note 90 ch.I l.639 : les 2,1 M $ sont le premier terme d'une **série annuelle** — 2012 : 2,1 M ; 2013 : 93 M dans 38 entreprises ; 2014 : 369 M dans 69 ; 2015 : 448 M dans 96 (Rauch 2016, p. 70-71). Aucun agent n'est nommé : « les premiers fonds de capital-risque » est une catégorie.

### 2. Les colonnes A1 n'ont pas été touchées — donc rien n'a été écrit

Ton arbitrage dit : `acteur_principal_mode = nd` **si les colonnes A1 sont touchées**. Mesure faite : sur E032, `acteur_principal_mode`, `acteur_principal_id` et `acteur_principal_nom` sont **toutes les trois vides** — cette ligne n'était pas dans les 40 du lot 3, seul lot où ces colonnes ont été remplies. La condition n'est donc pas remplie et **rien n'a été écrit**.

Si tu veux que le seuil soit *marqué* dans la donnée plutôt que seulement documenté ici, l'écriture serait d'une seule cellule :

| colonne | avant | après |
|---|---|---|
| `acteur_principal_mode` | *(vide)* | **`nd`** |

C'est la convention **r1** du gel du 15/08/2026 — « `mode nd` admis pour les seuils et états agrégés ». Elle n'exige aucun changement de `nature`, qui resterait `acte`. Un mot de ta part et je l'écris par applicateur.

### 3. La note conservée, et la scission signalée

**Conservé au registre, comme demandé :** l'intitulé de E032 mélange deux choses de nature différente — un **fait daté** (« En 2012, les premiers fonds de capital-risque **font leur entrée** ») et une **série annuelle agrégée** (le montant de 2,1 M $, premier terme d'une suite). La ligne porte `nature = acte` alors que sa charge informative principale est une mesure.

**Scission possible, signalée et non faite :** on pourrait séparer l'entrée du capital-risque (acte de 2012, initiateur = catégorie anonyme, donc `incertain` ou pas de rôle) de la série d'investissement (seuil, `mode nd`, aucun rôle). Ce serait une décision de **granularité du catalogue**, pas une correction — elle créerait une ligne, changerait les comptes, et se répercuterait sur les matrices. Elle n'est pas faite, et elle n'est pas recommandée dans ce lot.

La note existante de la ligne — « *année à cheval poc/pêche - phase indicative* » — est **inchangée** ; rien n'y a été ajouté.

---

## Périmètre tenu

Aucune écriture sur E059 ni sur E032. Aucun rôle posé sur ces deux lignes. Aucun statut modifié. Aucun doublon corrigé ni fusionné — E059 ↔ G110 est **signalé**, pas tranché. Aucun graphe touché, aucune version de graphe, aucun patch. Aucun vocabulaire gelé modifié. Les quatre lignes de la file de diagnostic (E039, E066, E068, E069) n'ont pas été approchées.
