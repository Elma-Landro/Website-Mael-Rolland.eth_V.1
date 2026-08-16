# Rôles — lot 5 de finition — 16/08/2026

Mini-lot de finition avant le chantier narratif « dossiers de crise ». **Une seule écriture : la ligne de rôle E060.** Tout le reste est diagnostic et preuve.

*Aucun graphe touché, aucun site touché, aucun vocabulaire gelé modifié, aucune cellule du catalogue maître modifiée, aucun doublon corrigé, aucune décision R3, aucun remplissage massif.*

## 1. Empreintes

| fichier | avant | après |
|---|---|---|
| `catalogue-roles-v0.csv` (81 → 82 lignes) | `b6e7deeaccc5280ec30eca2f73bc23e9b357c236` | **`a83570e9a87f93b9ff5ce5cfb665fdf6cf0c9bb5`** |
| `grille-roles-v0.md` | `fa2ee2d2353f5e708a35e04b25d74bd83df9b202` | *identique* |
| `vocabulaire-q7-v1-proposition.md` (Q7 v1 gelé) | `55bf8d9c5757bd096d9bbe77b78dfe402b61ba1b` | *identique* |
| `catalogue-evenements-v3-3.csv` (**maître**) | `7a87a37d9e05d7cbe096ece8d436506812ef68a4` | *identique* |

Le maître n'a pas bougé d'un octet — c'est ce qui distingue ce lot du précédent.

## 2. Point 1 — E060, une ligne, et rien d'autre

```
E060;institutions_financieres;;opposant;moyenne;opposition strategique « blockchain not
bitcoin » — l'idee emane d'acteurs de la finance traditionnelle (ch.I n.86 l.631, slogan
« Forget Bitcoin, embrace blockchain »), ils en « font leur publicite » et l'effet est
mesure : « nombreuses sont les entreprises de l'ecosysteme a pivoter » (ch.I l.289).
Arbitrage du 16/08/2026
```

**`statut_ligne` de E060 : `validee`, inchangé** — c'est un contrôle bloquant du script (`C4c`), pas une intention. Si le statut avait bougé depuis le diagnostic, l'applicateur aurait refusé d'écrire.

`actor_name` est laissé **vide**, délibérément. La source désigne une catégorie — « des acteurs de la finance traditionnelle » — et ne nomme Blythe Masters / JP Morgan qu'à titre d'exemple (« en l'espèce »). Écrire ce nom seul rétrécirait l'acteur au-delà de ce que dit le texte ; la typologie v1 suffit, et la note porte l'ancrage.

Confiance `moyenne` : les trois conditions de la règle sont textuellement remplies, mais l'acteur reste une catégorie et non un agent nommé.

## 3. Point 2 — E059 : l'identifiant graphe existe, la correction est spécifiée, elle n'est pas appliquée

Rapport détaillé : `docs/audits/diagnostic-e059-e032-correction-preparee-2026-08-16.md`.

**L'entité existe** : `8991d9f05d234b6d876d16334f60af63`, type `Organization`, nom `Coinbase`, dans le graphe v115. Recherche menée sur `name`, `nameEn`, `labelEn`, `labelFr` et `aliases` — les cinq champs que le dépôt impose de croiser. Deux homonymes de famille écartés explicitement : `Coinbase Commerce` (un service) et l'`InfrastructureEvent` « Coinbase : croissance et levée de fonds 75M$ » (l'événement, pas l'acteur).

La correction est spécifiée cellule par cellule dans le diagnostic — cinq colonnes, `statut_ligne` intact — et **n'est pas appliquée** : « Coinbase doit *probablement* devenir acteur principal » n'est pas une ratification, et les sorties attendues de ce lot ne comprenaient pas d'écriture au maître. Aucun rôle n'est posé tant que l'acteur principal n'est pas stabilisé, comme demandé.

**Ce que la recherche a fait apparaître, et qu'il faut savoir avant de corriger : E059 a un jumeau, G110.** Même fait, même année. E059 est `validee` et sans `gid` ; G110 est `chantier`, porte le `gid` de l'événement graphe et n'a aucun acteur principal. C'est la configuration E015 ↔ G001 du lot 3, tranchée alors par un arbitrage de canonique. Je ne l'ai pas traitée — la consigne interdit de corriger les doublons — mais stabiliser E059 en ignorant G110 reviendrait à consolider une ligne sans regarder sa jumelle.

## 4. Point 3 — E032 : traitée comme seuil, aucune écriture

Mesure faite : les trois colonnes A1 de E032 (`acteur_principal_mode`, `_id`, `_nom`) sont **vides** — la ligne n'était pas dans les 40 du lot 3, seul lot à les avoir remplies. Ta condition « `acteur_principal_mode = nd` **si les colonnes A1 sont touchées** » n'est donc pas remplie : **rien n'a été écrit**. Le diagnostic donne la cellule exacte à écrire si tu veux que le seuil soit marqué dans la donnée plutôt que seulement documenté.

La note demandée est conservée au registre : l'intitulé mélange un fait daté (« les premiers fonds de capital-risque font leur entrée ») et une série annuelle agrégée (2,1 M $ en 2012, puis 93, 369, 448 M). La scission possible est **signalée et non faite** — c'est une décision de granularité, pas une correction.

## 5. Preuves exigées

**Preuve A — les rôles du §2 sont inchangés.** L'applicateur ne fait pas confiance à sa propre constante : il **extrait les onze rôles du tableau du §2** de `grille-roles-v0.md` et les compare à la liste gelée à chaque exécution, avant toute écriture. Résultat de l'exécution :

```
initiateur · exploiteur · affecte · revelateur · correcteur · validateur
coordinateur · opposant · observateur · non_applicable · incertain
```

Empreinte SHA-1 du bloc §2 seul : `c10eb3f16cb1443cedc35a85985a004e19cb8017`. Le fichier de la grille n'a par ailleurs pas été rouvert par ce lot — son empreinte de blob est identique à celle du lot 4.

**Preuve B — les anciennes lignes de rôle sont intactes.** Vérifiée deux fois, indépendamment du script. *Cette preuve porte sur le fichier produit par l'applicateur ; le fichier **poussé** a subi un défaut de transport décrit au §8, qui l'a momentanément contredite sur le distant.*

- au niveau **octet** : le fichier produit *commence* par le fichier source, à l'octet près (`b.startswith(a)` → vrai) ; l'ajout fait exactement **384 octets**, et c'est la ligne E060 ;
- au niveau **enregistrement** : les 81 premières lignes se relisent à l'identique après écriture (comparaison champ à champ des 81 dictionnaires) ;
- **forme** : 83 CRLF, **zéro LF isolé**, zéro octet `NUL`, fin de fichier en CRLF.

C'est aussi un contrôle bloquant du script (`C5`, `C5c`, `C5f`, `C5g`) : il refuse d'écrire si l'un d'eux échoue.

**Preuve C — les gardes mordent.** Quatre scénarios de sabotage passés sur copie, depuis la racine du dépôt, tous refusés proprement avec code 1 :

| scénario | contrôle |
|---|---|
| déclarer E060 attendue en `a_arbitrer` | `C4c` — la ligne a bougé |
| inventer le rôle `contestataire` | `C3b` — hors grille v0 |
| viser E069 au lieu de E060 | `C3g` — ligne hors lot |
| falsifier l'empreinte du catalogue maître | `C1b` — le maître a bougé |

Le script vérifie en outre, en sortie, qu'**aucune** des six lignes interdites (E059, E032, E039, E066, E068, E069) n'a reçu de rôle (`C5h`).

## 6. État après lot

`catalogue-roles-v0.csv` : **82 lignes de rôle**, **50 événements** porteurs. La vue « validées sans rôle » de l'Observatoire descend mécaniquement de 53 à 52 lignes, et la file de diagnostic reste à **16** — E060 n'en faisait pas partie (elle n'a ni effet Q7 codé, ni crise, ni CVE : elle était en « grille non encore appliquée »).

## 7. Défaut de transport sur le CSV poussé — un octet, et ce qu'il faut faire

**Le fichier poussé n'est pas le fichier produit.** Le push du lot a altéré **une ligne ancienne** :

| | ligne 27 (E077, note du `coordinateur`) |
|---|---|
| produit par l'applicateur, local | `divulgation discrète inter-**implémentations** (ch.III n.19 l.801)` |
| effectivement poussé, distant | `divulgation discrète inter-**implementations** (ch.III n.19 l.801)` |

Un octet perdu — l'accent aigu de `é` (`c3 a9` → `e`). Distant : **10264 octets**, empreinte `0f380a208bf84ef833bd5c5935c9ed80e74a30bc`, au lieu de 10265 et `a83570e9…`. Les 83 CRLF, eux, sont intacts, et la ligne E060 ajoutée est exacte.

**C'est grave par ce que ça contredit** : le message du commit et la preuve B affirment que les 81 lignes antérieures sont intactes à l'octet. C'est vrai du fichier produit, faux du fichier versé. Une preuve qui ne tient pas sur la donnée réellement publiée ne vaut rien — d'où cette section.

**Pourquoi ce n'est pas réparé ici.** Le connecteur GitHub transmet le contenu **octet pour octet et sans interpréter les échappements** (vérifié : les `\r\n` littéraux de `make_roles_v0_lot5.py` sont arrivés intacts en tant que texte). Or l'octet CR (0x0D) **ne peut pas être émis** depuis cette session : un CR isolé placé entre deux caractères disparaît purement — ce n'est donc pas une normalisation de fins de ligne, c'est un filtrage. Un fichier CRLF ne peut par conséquent pas être re-transmis fidèlement par ce canal. Deux contournements ont été testés et sont fermés : `git push` direct est refusé par le proxy (403, dépôt hors de l'ensemble autorisé de la session) et l'API REST en base64 l'est aussi.

*J'avais d'abord affirmé qu'émettre `\r` en échappement JSON résoudrait le problème. C'était faux, et la vérification l'a montré avant tout push : la technique aurait injecté 83 backslash-r textuels dans le CSV — une corruption pire que l'accent manquant. Le garde-fou « empreinte vérifiée avant l'appel, jamais après » a fait exactement son travail.*

**Ce qui répare, en une action :** re-verser `catalogue-roles-v0.csv` **par upload web**, avec le fichier livré en pièce jointe de ce lot. C'est le canal documenté du dépôt pour la fidélité à l'octet. Le fichier attendu fait **10265 octets**, empreinte de blob **`a83570e9a87f93b9ff5ce5cfb665fdf6cf0c9bb5`**, 83 CRLF, 82 lignes de rôle. À vérifier après upload — si l'empreinte affichée par GitHub est bien celle-là, le défaut est clos.

En attendant, l'état publié reste **exploitable** : le seul écart est un accent dans une note de justification. Aucun identifiant, aucun rôle, aucun acteur, aucune confiance n'est touché — les 82 lignes se relisent et se comptent normalement, et l'Observatoire les affiche sans erreur.

## 8. Ce qui reste ouvert

1. **E059 ↔ G110** : même ligne ? laquelle est canonique ?
2. **E059** : ratifies-tu l'inversion d'acteur principal telle que spécifiée ?
3. **E032** : veux-tu que `acteur_principal_mode = nd` soit écrit, ou la documentation suffit-elle ?
4. La file de diagnostic — 16 lignes, dont E039, E066, E068, E069 — **explicitement non traitée dans ce lot**.
