# Rôles — lot 4, amendement de la grille, file de diagnostic — 16/08/2026

Application des huit décisions Maël du 16/08/2026 rendues après le diagnostic des rôles. Un seul lot d'écriture, borné à cinq lignes ; tout le reste est de la documentation, de l'instruction et de l'affichage.

*Aucun graphe touché, aucune version de graphe, aucune fusion catalogue/graphe, aucune modification du catalogue maître, aucun statut changé, aucune ligne hors périmètre R3 tranchée.*

## 1. Empreintes — ce qui a bougé, ce qui n'a pas bougé

| fichier | avant | après |
|---|---|---|
| `catalogue-roles-v0.csv` (76 → 81 lignes) | `14d1db05088efb9bf3c527a97fc2ab6c2a4ced5b` | **`b6e7deeaccc5280ec30eca2f73bc23e9b357c236`** |
| `grille-roles-v0.md` (**ajout** §7, guide de codage) | `00e720579f20031198bf2b4f8c2d12c939ab38d8` | **`fa2ee2d2353f5e708a35e04b25d74bd83df9b202`** |
| `vocabulaire-q7-v1-proposition.md` (Q7 v1 **gelé**) | `55bf8d9c5757bd096d9bbe77b78dfe402b61ba1b` | *identique* |
| `catalogue-evenements-v3-3.csv` (catalogue maître) | `7a87a37d9e05d7cbe096ece8d436506812ef68a4` | *identique* |
| `arbitrages-gel-q7v1-roles-v0-2026-08-15.md` (verbatim du gel) | `b20acde7ef7136ef8ef7105ecdad5ac14fdabd91` | *identique* |

**L'empreinte de la grille de rôles change — il faut le dire avant tout le reste.** Un document gelé dont l'empreinte bouge est exactement le genre de chose qui ne doit jamais être découverte après coup. Ce qui a changé est un **ajout en fin de fichier** et rien d'autre : le §7 demandé au point 1. La preuve est mécanique et faite par le script du lot lui-même — le **§2, qui porte le vocabulaire gelé, est octet pour octet identique**, et ses onze rôles sont extraits du document puis comparés à la liste gelée à chaque exécution. Aucun rôle ajouté, renommé ni redéfini : l'amendement ne produit donc pas de v1, conformément à la règle du gel.

## 2. Point 1 — la règle de codage, inscrite

> **Le rôle qualifie la fonction tenue dans la situation, pas la grammaire de l'acte.**

Inscrite en `grille-roles-v0.md` §7, avec la table de correspondance que tu as fixée (`initiateur` / `revelateur` / `validateur` / `opposant` / `observateur`), et une précision : ce tableau ne remplace pas les définitions du §2, il dit dans quel ordre les lire quand plusieurs semblent convenir. **En cas de conflit, le §2 fait foi.**

Le §7 rappelle aussi comment la règle a été établie — lue dans les codages déjà versés (E064, E052, E063, E044), puis ratifiée — et donne l'ancrage textuel qui l'a rendue démontrable : la thèse elle-même oppose les deux fonctions, chapitre I l.289, à propos des mêmes acteurs.

> « de manière très indirecte d'abord, par **simple publication** de données de prix agrégées (Nasdaq fin 2013, suivi par le NYSE en 2015), plus directement ensuite, par la **création** de produit financier spécifique par des acteurs reconnus (marchés futurs par le *Chicago Board Option Exchange* ou le *Chicago Mercantile Exchange*, courant 2017). »

Le partage `validateur` / `initiateur` est **écrit dans le texte source**. Ce n'était pas le cas quand je te l'ai proposé la première fois : je l'avais alors déduit d'un précédent. La citation est venue après, en instruisant E060, et elle confirme la déduction. C'est plus solide, et c'est ce qui est versé.

## 3. Point 2 — la formulation, inscrite aux deux endroits

> **La matrice acteurs × rôles mesure l'état du codage avant de mesurer le terrain.**

Elle est désormais en tête de la matrice acteurs × rôles dans l'Observatoire, avec sa preuve chiffrée, et au §7 de la grille comme avertissement de lecture permanent. Une case vide dit « pas encore codé », jamais « ce rôle n'existe pas ».

## 4. Point 3 — le lot borné : cinq rôles versés

Applicateur : `scripts/make_roles_v0_lot4.py`. Lot figé dans le code, `--dry-run`, contrôles d'arrivée **et** de sortie bloquants. Le fichier de rôles ne se modifie jamais à la main.

| ligne | acteur | nom | rôle | conf. | fonction retenue |
|---|---|---|---|---|---|
| E073 | `institutions_financieres` | CBOE et CME | `initiateur` | haute | crée un produit qui n'existait pas |
| E042 | `institutions_financieres` | Nasdaq | `validateur` | moyenne | « simple publication » — acceptation, pas production |
| E058 | `institutions_financieres` | NYSE | `validateur` | moyenne | même acte, même phrase source que E042 |
| E027 | `institutions_financieres` | PayPal | `opposant` | moyenne | retrait de service = blocage agissant |
| E037 | `regulateurs_etats` | Banque centrale européenne | `revelateur` | moyenne | écrit dont l'effet aval est attesté |

Chaque ligne porte dans sa `note` **la citation qui la fonde**, avec sa référence exacte au chapitre I. `catalogue-roles-v0.csv` passe de 76 à 81 lignes ; **les 76 antérieures sont conservées octet pour octet** (contrôle C5) ; 44 → **49 événements** portent désormais un rôle.

### Les gardes, et la preuve qu'elles mordent

Un applicateur dont on n'a pas vu refuser est un applicateur non testé. Cinq scénarios de sabotage ont été passés sur une copie, tous **refusés proprement**, message à l'appui et code de sortie 1 :

| scénario | contrôle déclenché |
|---|---|
| glisser E060 dans le lot | `C3h` — ligne explicitement hors lot |
| inventer le rôle `ratificateur` | `C3c` — rôle hors grille v0 |
| falsifier l'empreinte de la source | `C1` — le fichier de rôles a bougé |
| retirer `incertain` du vocabulaire | `C2` — le §2 de la grille diverge de la constante gelée |
| coder E027 sur `core_devs` | `C4d` — acteur du lot ≠ acteur principal du catalogue |

**Un premier jeu de tests négatifs était faux et a été refait.** Les copies avaient été placées dans `/tmp`, où le script résout ses chemins depuis sa propre position : les cinq cas plantaient sur un fichier introuvable, avant même d'atteindre le moindre contrôle — et sortaient tous en code 1, ce qui ressemblait à un succès. Un test qui échoue pour la mauvaise raison ne prouve rien ; refait depuis la racine du dépôt, il prouve.

Le script refuse aussi son propre rejeu (`C1` + `C4`) : c'est un lot à un coup, pas une opération idempotente.

## 5. Points 4, 5, 6 — les trois lignes écartées, instruites

Rapport dédié : `docs/audits/diagnostic-e060-e059-e032-2026-08-16.md`. **Aucune des trois n'a été modifiée, aucun rôle ne leur a été posé.** Résumé :

**E060 — la citation demandée est arrivée, et elle tranche dans le sens de `opposant`.** Le corps du texte (ch.I l.289) dit que des acteurs financiers « **font leur publicité** » d'une idée selon laquelle « l'important ne serait pas les UCN » ; la note 86 (l.631) précise que l'idée « **émane d'acteurs de la finance traditionnelle** », slogan à l'appui — « *Forget Bitcoin, embrace blockchain* » ; et l'effet est mesuré dans la même phrase : « **Nombreuses sont les entreprises de l'écosystème à pivoter** ». Contestation active, acteur à la source, effet direct sur le cours des choses : les trois conditions de ta règle. Le guide de `opposant` emploie d'ailleurs le mot « campagne ». **Une question de forme reste ouverte** : ta décision dit « conserver `a_arbitrer` », or E060 porte `statut_ligne = validee` et `a_arbitrer` est une valeur de statut. Je n'ai rien touché ; le rapport pose la question.

**E059 — ton hypothèse est confirmée par la source, qui dit même l'inverse du catalogue.** Note 90 (l.639) : « **L'entreprise Coinbase réalise** la plus grande levée de fonds d'alors avec 75 millions de dollars. » L'agent de l'acte est Coinbase ; les financeurs ne sont pas nommés. Le catalogue porte pourtant `acteur_principal = institutions_financieres` et Coinbase en secondaire — l'inverse de ce que pose la règle D7. C'est une anomalie d'acteur principal, à corriger par applicateur si tu la ratifies, et **avant** tout codage de rôle.

**E032 — les indices convergent vers le seuil.** La note 90 présente les 2,1 M $ comme le premier terme d'une **série annuelle agrégée** (2012 / 2013 / 2014 / 2015, avec nombres d'entreprises), produite par une source secondaire. Aucun agent nommé. `precision = annee`, note de ligne « année à cheval poc/pêche ». Une nuance est signalée et non escamotée : la même phrase contient un fait daté (« les premiers fonds de capital-risque **font leur entrée** ») que l'intitulé mélange avec la mesure — la ligne pourrait mériter d'être scindée, ce qui est une décision de granularité que je n'ai pas prise.

## 6. Point 7 — la file de diagnostic

Les quatre classes de la vue « validées sans rôle » portent désormais **ton vocabulaire** : `rôle non nécessaire` · `acteur non identifié` · `à instruire` · `grille non encore appliquée`. Chacune affiche toujours sa règle calculée, et une ligne tombe dans la première classe qui la retient.

Après le versement des cinq rôles : **53 lignes validées sans rôle** (au lieu de 58), réparties en 10 / **0** / **16** / 27.

La nouveauté est la **file de diagnostic** : les 16 lignes « à instruire », **ordonnées, les crises d'abord puis par date**, avec leur rang et le motif qui les rend portantes. C'est une file de travail, pas une file de correction — aucun rôle n'y est proposé, aucune case n'y est pré-remplie, et l'ordre est affiché en clair au-dessus de la table.

Les quatre premières sont les crises, et ce sont elles qui comptent : **E039** (scission de chaîne v0.8, crise n°19), **E066** et **E068** (dépôt puis ticker d'Ethereum Classic — la sécession), **E069** (PR 9049, l'insémination de la CVE-2018). Quatre lignes qui portent l'analyse de la thèse et sur lesquelles personne ne tient de rôle.

## 7. Point 8 — la charte couleur

Confirmée et déjà en place depuis le lot précédent : rouge vin / bordeaux / doré / noir, plus le vert néon du site. La vérification comprend désormais un contrôle de charte — **tout hexadécimal hors liste blanche fait échouer le run**, sur les deux pages. La couleur ne porte jamais seule : le statut est écrit, l'effectif est écrit dans la case, et le signe Q7 n'a aucune teinte propre (forme + glyphe).

## 8. Vérification

Chromium, pages servies en HTTP, polices distantes coupées : **22 contrôles, 0 échec, 0 `pageerror`**. Sont contrôlés, entre autres : le total de la matrice des rôles (81, comparé à une mesure Python indépendante), les quatre libellés de classe, les effectifs 10 / 0 / 16 / 27 et leur somme, **l'ordre exact de la file** (les 16 identifiants dans l'ordre attendu, crises en tête, rangs 1 à 16), la présence des deux formulations ratifiées dans la matrice, et la charte couleur.

Suite CI locale complète au vert. Effet de bord traité dans le même lot : trois faux positifs lexicaux du nouvel applicateur (`count`, `note`, `role` — la méthode `bytes.count()` et deux noms de colonnes) ajoutés aux exclusions du registre, vérifiés occurrence par occurrence ; `--check` reste vert **sans régénérer le registre**, qui ne bouge pas.

## 9. Correction au registre : l'historique distant de ce lot est en quatre commits, pas deux

Ce lot devait être poussé en **deux** commits — l'exclusion du registre, puis le reste. Il en compte **quatre** sur la branche. Le contenu est intact et vérifié (les sept empreintes de blob sont identiques aux locales, l'arbre distant égale l'arbre local, et **les quatre exécutions de CI sont vertes**, 12 étapes sur 12, aucune reprise), mais le découpage n'est pas celui annoncé :

| commit | contenu réel |
|---|---|
| `48f955f` | `scripts/build_properties_registry.py` — conforme au plan |
| `5b159b1` | **`catalogue-roles-v0.csv` seul** |
| `d6d1d0b` | l'applicateur, le §7 de la grille, les deux rapports |
| `3de1fc8` | `catalogue-matrices.html` |

**Le défaut à connaître : le message de `5b159b1` surdécrit son contenu.** Il porte le message complet du lot — applicateur, guide de codage, file de diagnostic — alors qu'il ne contient que le fichier de données. Cause : la charge utile des six fichiers dépassait la taille transmissible en un seul appel ; une première tentative a été tronquée (sans rien écrire, l'opération étant atomique), et la reprise n'a embarqué qu'un fichier tout en conservant le message d'origine.

Deux conséquences, énoncées plutôt que tues. D'abord, **`5b159b1` fait exister la donnée sans l'applicateur qui l'a produite** — l'ordre maison veut qu'ils voyagent ensemble. C'est un état transitoire d'un seul commit, la CI y est verte, et l'applicateur arrive au suivant ; mais qui lit l'historique commit par commit croisera 81 lignes de rôle sans le script qui les explique. Ensuite, **un message de commit qui ment est une atteinte à la mémoire du dépôt**, qui est précisément ce que `docs/audits/` sert à protéger.

**Pourquoi ce n'est pas réparé mais documenté** : réécrire l'historique demande un `force-push`, or le transport git direct est refusé par le proxy sur ce dépôt (403 — le dépôt n'est pas dans l'ensemble autorisé de la session) et le connecteur GitHub ne sait qu'ajouter des commits. Le seul remède disponible est celui-ci : **corriger le registre par un enregistrement postérieur**, pas par une réécriture. L'ordre essentiel, lui, est tenu — l'exclusion du registre précède bien l'arrivée de l'applicateur, ce qui était la raison d'être du découpage.

*Note de méthode, pour la même raison :* en préparant cette correction j'ai lancé un `git reset --hard` inutile qui a effacé une première rédaction de cette section. Sans conséquence — rien n'était poussé, et le texte a été réécrit — mais c'est le second geste de la journée dont l'effet dépassait l'intention.

## 10. Ce qui reste ouvert

Les quatre questions du rapport de diagnostic : le rôle d'E060 et le sens de « conserver `a_arbitrer` » ; l'inversion d'acteur principal sur E059 ; la nature d'E032 ; et, à terme, les 16 lignes de la file.

Dette inchangée et non traitée : `add_statut_ligne.py` et `make_v3_3_catalogue.py` figurent toujours en `readBy` du registre (état déjà versé — les en retirer ferait bouger le registre pour rien) ; 26 paires de doublons probables ; Mt. Gox typé `InfrastructureEvent` dans le graphe.
