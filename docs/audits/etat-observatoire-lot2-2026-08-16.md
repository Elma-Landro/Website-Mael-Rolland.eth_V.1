# Observatoire du catalogue — lot visible 2 : les matrices — 16/08/2026

Deuxième lot du chantier « Observatoire du catalogue événementiel ». Il livre les quatre croisements demandés et, sur le périmètre R3, **une mesure au lieu d'une décision**. *Aucun graphe touché, aucun catalogue modifié, aucun vocabulaire gelé touché, aucun recodage, aucun hors-périmètre tranché.*

| livrable | empreinte | commit |
|---|---|---|
| `catalogue-matrices.html` (nouvelle page, racine) | `3b7bda37b8590c52f0396e0d6d38d74cd293035a` | `8949ca5` |
| `catalogue-lab.html` (+1 ligne : lien croisé) | `a0e82105edde90e7cdfeb77660123442e559d914` | `8949ca5` |
| `scripts/build_properties_registry.py` (exclusion) | `b8380cd8365317ae6b4eccbd733f66a71671c569` | `770feb0` |

CI verte sur les deux commits (`31939488120`, `31939825792`). Les trois empreintes distantes sont identiques aux locales, vérifiées deux fois.

## 1. La règle du chantier, tenue

La page ne contient **aucune donnée d'événement**. Elle lit en direct les deux mêmes fichiers que la page-labo — `catalogue-evenements-v3-3.csv` (345 lignes × 33 colonnes) et `catalogue-roles-v0.csv` (76 lignes de rôle) — par `fetch` relatif. Les vocabulaires gelés y sont recopiés **pour lire, jamais pour trancher** : les 11 rôles de la grille v0 et les 9 dimensions de Q7 v1 sont tous en colonne, **y compris ceux que le codage n'emploie jamais** — une colonne vide est un résultat, pas un trou d'affichage.

Les deux pages se renvoient l'une à l'autre. Aucune dépendance externe, aucun CDN : analyseur CSV et tables écrits à la main, la page fonctionne hors ligne (IPFS/Swarm compris). `noindex` conservé.

## 2. Le périmètre R3 : la réponse est mesurée, et elle est nulle

Consigne tenue à la lettre : les quatre lignes hors bornes ne sont **ni exclues, ni corrigées, ni changées de statut**. Elles sont marquées (hachure + mention « R3 » écrite), un bouton bascule *inclure / exclure* — **inclure par défaut, parce qu'exclure serait déjà décider** — et un tableau mesure l'écart matrice par matrice, recalculé à chaque filtre.

| matrice | unité comptée | hors périmètre inclus | exclu | **écart** |
|---|---|---:|---:|---:|
| 1 · acteurs × rôles | lignes de rôle | 76 | 76 | **0** |
| 2 · événements × effets Q7 | signes posés | 49 | 49 | **0** |
| 3 · phases × types d'actes | événements croisés | 133 | 133 | **0** |
| 4 · arènes × effets Q7 | couples (événement, effet) | 49 | 49 | **0** |
| — corpus | lignes | 345 | 341 | +4 |

**Le résultat, c'est l'écart nul.** G122 (ICANN, 1998), G127 (RipplePay, 2004), G170 (The Merge, 2022) et G113 (Figure 5, 2024) ne portent **aucun** des axes croisés : pas d'arène, pas de type d'acte, pas d'effet Q7, pas de rôle, pas d'acteur principal. Elles portent une phase, rien d'autre. Les inclure ou les exclure ne déplace pas une seule case des quatre matrices ; elles ne pèsent que sur les dénominateurs de couverture, où elles comptent comme non codées. Concrètement : **les quatre lignes n'apparaissent que dans la colonne de contexte « (type non codé) » de la matrice 3**, deux cases, marquées R3 — cette colonne est placée en tête de table précisément pour que le marquage soit visible sans défilement.

Ce que cela veut dire pour la décision à venir : le coût analytique de leur sortie est aujourd'hui **nul**, et le bénéfice de leur maintien l'est tout autant tant qu'elles restent non codées. La question n'est donc pas « faussent-elles les distributions ? » — elles ne les touchent pas — mais « ces quatre objets doivent-ils être codés, ou sortir ? ». Je ne l'ai pas tranchée.

**Vérification de la règle elle-même** : la lecture par année (`< 2008` ou `> 2020`) et la lecture stricte de R3 (`< 18/07/2008` ou `> 31/12/2020`) désignent **exactement les mêmes quatre lignes**. Le marquage ne dépend donc pas de l'interprétation de la borne. Les 18 lignes **sans date** ne sont ni dedans ni dehors : elles ne sont jamais marquées, comme au lot 1.

## 3. Ce que les quatre matrices donnent à voir

Couverture réelle, affichée en tête de chaque matrice — c'est la première chose à lire :

| matrice | lignes portant les deux axes | part du corpus |
|---|---:|---:|
| acteurs × rôles | 44 événements | 13 % |
| événements × effets Q7 | 47 événements | 14 % |
| phases × types d'actes | 133 événements | 39 % |
| arènes × effets Q7 | 47 événements | 14 % |

Six résultats méritent ton œil.

**Le codage des rôles est mono-acteur.** 48 des 76 lignes de rôle portent sur `core_devs` (63 %), et **34 sur le seul rôle `correcteur`**. La matrice donne à voir un catalogue qui, pour l'instant, raconte surtout des développeurs qui réparent.

**Deux types d'acteurs n'ont jamais reçu de rôle** — `institutions_financieres` et `regulateurs_etats` — alors que le catalogue leur attribue le rôle d'acteur principal sur 11 lignes, dont **8 sont `validee`**. Ce n'est pas un effet de la règle D4 : ce sont des lignes validées sans rôle posé. Plus largement, **58 des 95 lignes validées ne portent aucun rôle**.

**`exploiteur` n'est jamais attribué à un acteur identifié** : ses 4 occurrences portent toutes `actor_id = nd`. Cohérent avec D7 (incident subi sans initiateur pertinent), mais il faut le savoir : la matrice ne montre aucun exploitant nommé.

**La grille v0 n'a aucun rôle mort — mais une queue mince.** Les 11 rôles sont employés au moins une fois ; `opposant`, `incertain` et `non_applicable` ne tiennent chacun qu'à un seul cas.

**Deux dimensions Q7 sur neuf sont vides** : `unite_compte_etalon` et `conf_ethique`, zéro ligne. À l'autre bout, `conf_methodique` capte 21 des 49 signes (43 %), **dont 14 en `±`** : la convention r2 (mise en cause non activée, note obligatoire) porte à elle seule 29 % de tout le codage d'effets.

**Les arènes se spécialisent nettement.** `on_chain` concentre 22 des 49 couples, dont 17 sur `conf_methodique` ; `marches_plateformes` en porte 14, dont 8 sur `valorisation` ; `depots_de_code` 4, dont 3 sur `integrite_monnayage`. Trois arènes, trois registres d'effet distincts — c'est le résultat le plus structurant de ce lot, et il est lisible d'un coup d'œil sur la matrice 4.

Accessoirement, la matrice 3 montre que `incident` domine les trois phases (11 / 18 / 19) et que la maturation porte en plus **18 `nd`** : un tiers de son codage de type d'acte reste indéterminé.

## 4. Couleur : calculée, pas choisie — deux encodages, deux validations

| encodage | où | validation `scripts/validate_palette.js` (skill dataviz), **contre les deux surfaces du site** |
|---|---|---|
| rampe d'effectif, or, 5 pas | matrices 1, 3, 4 | mode `--ordinal` : **0 échec** sur `#4d0000` et `#000000` ; écarts de clarté tous ≥ 0.06 ; pas le plus sombre à 2.84:1 (bordeaux) et 3.74:1 (noir), au-dessus du plancher de 2:1 |
| signes `+` / `−` / `±` | matrices 2 et 4 | `--pairs all` : **0 échec** ; pire paire CVD ΔE 8.6 (cible ≥ 8) ; vision normale ΔE 22.5 (plancher ≥ 15) ; contraste ≥ 3:1 partout |

Trois décisions, toutes mesurées et non supposées :

- **Le pas le plus sombre devait rester distinct d'une case vide.** Une rampe séquentielle a le droit de laisser son pas le plus bas se fondre dans le fond ; ici « 1 » et « aucune co-occurrence » sont deux faits différents, donc la rampe est tenue au gate **ordinal**, plus strict. Les premières rampes essayées échouaient (1.45:1) ; celle qui est livrée passe.
- **Les trois teintes de signe sont prises hors de la palette de statut du lot 1** (`#008300`, `#e66767`, `#9085e9` contre `#199e70`, `#c98500`, `#d55181`, `#3987e5`), pour qu'aucune couleur n'ait deux sens sur une même page.
- **L'échelle est ancrée aux deux bouts** : l'effectif 1 tombe toujours au pas 1, le maximum au pas 5. La progression logarithmique est nécessaire — une case à 34 contre une majorité à 1 ou 2 — mais sans ancrage le premier pas restait inemployé et l'échelle mentait d'un cran. La légende affiche les **bornes réelles** de chaque pas, recalculées à chaque rendu ; un pas qu'aucune valeur n'atteint n'est pas affiché.

Contraste du texte dans les cases, mesuré : blanc sur le pas 1 (5.62:1), noir sur les pas 2 à 5 (5.03 / 6.62 / 8.58 / 11.00:1) — tous au-dessus de 4.5:1. **L'effectif et le signe sont toujours écrits dans la case** : la couleur ne porte jamais seule, et le marquage R3 est une hachure **plus** une mention écrite.

L'esthétique du dépôt est prolongée, pas modernisée : Press Start 2P, VT323, palette bordeaux/or, thème sombre commutable, aucune dépendance.

## 5. Vérification navigateur (exigée par la charte)

Chromium local, page servie en HTTP, polices distantes coupées pour simuler le hors-ligne. **32 contrôles, 0 échec, 0 `pageerror`** ; seule erreur console : le blocage volontaire des polices du test.

La vérification a été rejouée **sur une extraction propre de la branche distante** après les deux pushs — mêmes 32 contrôles au vert : ce qui est vérifié est bien ce qui est versé.

Ce qui est contrôlé, entre autres : totaux des quatre matrices comparés à des comptages Python indépendants (76 / 49 / 345 / 49) ; somme des totaux de ligne égale au total général ; 11 colonnes de rôle et 9 colonnes de dimension ; les 4 lignes R3 listées et les 2 cases marquées ; la bascule R3 dans les deux sens ; les quatre bascules propres aux matrices (acteurs nommés, confiance haute = 60, type d'acte secondaire = +36, signes regroupés = 7 colonnes) ; le tiroir de cellule (34 lignes sur la plus grosse case) ; l'ouverture au clavier ; le filtre `système = ethereum` = 33 lignes propagé à la matrice ; la réinitialisation ; le lien croisé et l'intégrité de la page-labo.

**Un défaut rattrapé avant livraison** : cinq octets `NUL` s'étaient glissés dans le fichier à la place d'espaces, dans les clés de colonnes de la matrice 4. La page fonctionnait — les clés étaient cohérentes entre elles — mais le fichier était invalide et `file` le classait « data » au lieu de HTML. Détecté parce que `grep` a refusé de lire le fichier comme du texte, corrigé au niveau de l'octet, et **un contrôle d'octets a été ajouté à la vérification** (zéro `NUL`, décodable UTF-8, sur les deux pages) pour que le prochain lot ne puisse pas le refaire silencieusement.

## 6. Effet de bord traité — dans l'ordre, et sans faire bouger le registre

Le générateur du registre scanne `**/*.html`. Sans précaution, `catalogue-matrices.html` ajoutait **7 `readBy`** — `date`, `phase` (colonnes du CSV catalogue), `note`, `role` (colonnes du CSV de rôles), `description` (balise `<meta>`), `status` (`role="status"` et le code HTTP d'un `fetch`), `type` (la valeur d'une option de menu). Aucune n'est une lecture d'attribut du graphe : **cette page ne lit aucun graphe**. Occurrences vérifiées une à une, comme l'exclusion du lot 1.

L'exclusion est **poussée dans un commit séparé, avant la page** : dans l'autre ordre, la CI aurait été rouge le temps d'un commit. Résultat mesuré : `--check` reste vert **sans régénérer le registre** — le fichier versé est strictement inchangé (338 entrées, `_meta` identique).

## 7. Périmètre tenu, et ce qui reste ouvert

Aucun patch graphe, aucune version de graphe, aucune fusion catalogue/graphe, aucune modification d'une page existante du site autre que la ligne de lien ajoutée à `catalogue-lab.html`, aucun vocabulaire gelé touché, aucun recodage, aucune correction de doublons, aucune ligne hors périmètre tranchée.

Dettes connues, inchangées et non traitées ici : 26 paires de doublons probables ; Mt. Gox typé `InfrastructureEvent` dans le graphe ; `add_statut_ligne.py` et `make_v3_3_catalogue.py` encore en `readBy` du registre. La page reste **en français seul**, comme la page-labo — la contrepartie anglaise se fera quand l'Observatoire deviendra public.

Deux questions que ce lot pose et ne tranche pas, dans l'ordre où elles se poseront : **(a)** faut-il coder ou sortir les quatre lignes hors bornes, maintenant qu'on sait que le choix ne déplace rien ? **(b)** les 58 lignes `validee` sans aucun rôle, dont les 7 lignes validées sur `institutions_financieres`, appellent-elles une passe de rôles ciblée — ou est-ce le propre d'une ligne validée de ne pas toujours porter de rôle ?

## 8. Suite

Lot 3 (dossiers de crise : CVE-2018, The DAO, Genèse, MtGox, monnayage), lot 4 (export article). Rien de tout cela ne touchera au graphe.
