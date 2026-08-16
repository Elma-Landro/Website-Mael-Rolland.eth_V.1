# Observatoire — retour à la charte maison et vue « validées sans rôle » — 16/08/2026

Application des décisions Maël du 16/08/2026 prises après le lot visible 2. Trois points sur quatre touchent les pages ; le quatrième (diagnostic des 8 lignes) fait l'objet de son propre rapport, `diagnostic-roles-institutions-regulateurs-2026-08-16.md`.

*Aucun graphe touché, aucun catalogue modifié, aucun vocabulaire gelé touché, aucun rôle versé, aucune ligne hors périmètre tranchée.*

## 1. Périmètre R3 — rien à faire, et c'est vérifié

Décision : ne pas trancher, conserver les 4 lignes comme anomalies visibles, statut inchangé, pas de passage en `exclue`, pas d'élargissement, pas de recodage.

C'est exactement l'état livré au lot 2, et il est resté tel quel. Contrôle rejoué : les 4 lignes (G122, G127, G170, G113) sont toujours `chantier`, toujours listées et marquées « R3 » dans le panneau de périmètre, le bouton bascule fonctionne dans les deux sens, et les totaux des quatre matrices sont inchangés (76 / 49 / 345 / 49). **Aucune écriture n'a été faite sur ces lignes, à aucun moment.**

## 2. Couleur — retour à la charte maison

Décision : stopper les explorations de palette ; rouge vin / bordeaux / doré / noir ; la validation de contraste reste utile mais **ne doit pas créer une esthétique autonome**.

### Ce qui a été retiré

Les quatre teintes de statut du lot 1 (`#199e70` sarcelle, `#c98500` ambre, `#d55181` rose, `#3987e5` bleu) et les trois teintes de signe du lot 2 (`#008300`, `#e66767`, `#9085e9`) sont **sorties des deux pages**. Contrôle automatisé ajouté à la vérification : la liste des hexadécimaux de chaque page est comparée à la liste blanche de la charte, et **toute teinte étrangère fait échouer le contrôle**. Résultat : zéro teinte hors charte sur les deux pages.

### Ce qui les remplace, et la contrainte qui l'impose

Il faut le dire franchement : **dans la charte maison, quatre teintes séparables n'existent pas.** C'était déjà la mesure du lot 1 — or ↔ orange à ΔE 7.9 en vision normale, sous le plancher de 15. On ne peut donc pas coder quatre statuts par quatre couleurs sans sortir de la charte. La conséquence est structurelle, pas cosmétique : **la couleur cesse d'être le canal des catégories.**

| ce qu'il faut coder | comment, désormais | contrôle mesuré |
|---|---|---|
| **effectif** (matrices de comptage) | rampe mono-teinte dans l'**or maison**, 5 pas, dernier pas `#ffcc64` — l'or du site | `--ordinal`, 2 surfaces : **0 échec** ; écarts de clarté ≥ 0.06 ; pas le plus sombre à 3.70:1 (bordeaux) et 4.87:1 (noir), plancher 2:1 |
| **statut de ligne** (les deux pages) | rampe mono-teinte dans le **vert maison** (teinte de `--text-accent`), ordre d'incertitude croissante | `--ordinal`, 2 surfaces : **0 échec** ; pas le plus sombre à 3.11:1 et 4.09:1 |
| **signe d'effet Q7** (`+` `−` `±`) | **aucune teinte propre** : plein / contour épais / contour pointillé hachuré, plus le glyphe écrit | sans objet — il n'y a pas de teinte à confondre, donc pas de risque de daltonisme par construction |

Le texte des cellules est en **noir** sur les cinq pas de la rampe d'effectif : 4.87 / 6.48 / 8.53 / 11.02 / 14.07:1, tous au-dessus de 4.5:1. Le blanc, qui n'est pas dans la charte, a disparu — la rampe a été resserrée exprès pour qu'il devienne inutile.

### Ce que ça coûte, et pourquoi c'est le bon échange

Quatre nuances d'un même vert se distinguent moins bien que quatre couleurs franches. C'est réel, et c'est assumé : la séparation est reportée sur ce qui ne ment pas — **le libellé est écrit à côté de chaque pastille**, les segments empilés de la chronologie sont séparés par 2 px de surface, et l'effectif est écrit dans chaque case. Aucune information n'est portée par la couleur seule, ni avant ni maintenant.

La méthode a changé de sens, et c'est le point important : on **part** des teintes du site, on mesure, et là où la charte ne sépare pas, on passe au libellé et à la forme. On ne cherche plus une palette qui passe les contrôles. La validation est redevenue un contrôle.

## 3. Vue « validées sans rôle »

Décision : ne pas remplir automatiquement ; les rôles ne sont pas obligatoires pour toute ligne validée ; produire une vue qui distingue les cas.

Ajoutée comme section 3 de `catalogue-matrices.html`, entre la matrice acteurs × rôles et la matrice des effets. Elle s'ouvre sur le rappel de la règle gelée : « *aucun rôle n'est forcé ; une ligne sans rôle codable reste sans ligne de rôle* ». **Elle ne réclame donc aucun remplissage : elle sépare les raisons d'une absence.**

Quatre classes, chacune affichant **sa règle calculée**, une ligne tombant dans la **première** qui la retient. Ce sont des requêtes, jamais des verdicts — même discipline que les anomalies de la page-labo. Mesure sur le corpus entier : **58 lignes `validee` sans rôle, sur 95 validées (61 %)**.

| classe | n | règle |
|---|---:|---|
| seuil — l'absence est prévue | 10 | `nature = seuil` : la grille range explicitement certains seuils sous `non_applicable` |
| acteur non identifié | **0** | `acteur_principal` vide ou `nd` |
| **ligne portante sans rôle** | **17** | porte un effet Q7 codé, ou `crise = oui`, ou un CVE — **dont 4 marquées crise** |
| jamais passée en revue de rôles | 31 | le reste : validées par le calibrage, qu'aucune passe de rôles n'a couvertes |

Deux résultats à retenir.

**La classe « acteur non identifié » est vide.** Aucune ligne validée hors seuil ne manque d'acteur : quand un rôle manque, ce n'est jamais faute de savoir qui agit. Le cas existe dans la vue et y restera — une classe vide est un résultat.

**Les 17 lignes portantes sont le vrai sujet, et 4 d'entre elles sont des crises** : **E039** (scission de chaîne v0.8, crise n°19), **E066** et **E068** (dépôt puis ticker d'Ethereum Classic, la sécession), **E069** (PR 9049 — l'insémination de la CVE-2018). Ces quatre lignes servent l'analyse de la thèse et **personne n'y tient de rôle**. Ce n'est pas une anomalie de données : c'est le même mécanisme que celui établi dans le diagnostic — la passe de rôles ne les a pas atteintes. Mais ce sont, de loin, les premières à instruire si une passe est ouverte.

La vue suit les filtres et le bouton de périmètre R3, et porte son propre sélecteur de classe.

## 4. Vérification

Chromium, pages servies en HTTP, polices distantes coupées. **28 contrôles, 0 échec, 0 `pageerror`** ; seule erreur console : le blocage volontaire des polices du test.

Outre les totaux des quatre matrices (inchangés) et les comptages de la nouvelle vue (10 / 0 / 17 / 31, somme 58, comparés à une mesure Python indépendante), la vérification contrôle désormais **la charte elle-même** : aucun hexadécimal hors liste blanche, aucune encre courte autre que le noir, zéro octet `NUL`. Les trois formes de signe sont vérifiées par leur style calculé (rempli / contour 2 px / pointillé) et par leur glyphe.

**Un défaut de mon propre harnais, signalé pour mémoire** : cinq contrôles sont d'abord ressortis en « écart » alors que valeur obtenue et valeur attendue étaient identiques — le comparateur testait deux tableaux par identité de référence. Corrigé (comparaison par sérialisation) puis rejoué. Un contrôle qui échoue à tort est aussi grave qu'un contrôle qui passe à tort : il apprend à ignorer le rouge.

## 5. Effet de bord traité

La nouvelle vue lit la colonne `nature` du CSV, ce que le balayage lexical du registre compte comme une lecture d'attribut de graphe. Huitième faux positif de cette page, vérifié à l'occurrence près (une seule, `e.nature === 'seuil'`), ajouté aux exclusions. Mesure : `--check` reste vert **sans régénérer le registre**, qui ne bouge pas (338 entrées).

## 6. Ce qui reste ouvert

Les cinq questions du diagnostic (rapport dédié, §6), et la suite du chantier : lot 3 (dossiers de crise), lot 4 (export article).
