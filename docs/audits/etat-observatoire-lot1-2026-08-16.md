# Observatoire du catalogue — lot visible 1 : la page-labo — 16/08/2026

Premier lot du chantier « Observatoire du catalogue événementiel ». Il livre le poste de lecture : chronologie codée, filtres, distributions, anomalies. **Aucun graphe touché, aucun catalogue modifié, aucune page existante du site modifiée.**

| livrable | empreinte |
|---|---|
| `catalogue-lab.html` (nouvelle page, racine) | `8f59c08447fc09f5e144e67904395487b3c6e786` |
| `scripts/build_properties_registry.py` (exclusion, +17 lignes) | `2c7e4be6dd479f6a979fb0d45dfe97acd2053e3f` |

## 1. Le principe : la donnée est verrouillée, la page ne l'est pas

**La page ne contient aucune donnée d'événement.** Elle lit en direct `catalogue-evenements-v3-3.csv` (345 lignes × 33 colonnes) et `catalogue-roles-v0.csv` (76 lignes de rôle) par `fetch` relatif. Conséquence voulue : rien n'est dupliqué, donc rien ne peut périmer en silence — le jour où une v3-4 remplace la v3-3, la page suit sans être retouchée. C'est la règle maison appliquée à l'affichage : *une vue est un produit, jamais la source*.

Symétriquement, **aucune décision scientifique n'est prise par la page** : les vocabulaires gelés (statut D4, effets Q7 v1, rôles v0) y sont recopiés pour *lire*, jamais pour trancher. Les anomalies sont des requêtes sur la donnée versée, chacune affichant sa règle en clair ; aucune n'émet de verdict.

## 2. Ce que la page donne à voir

- **État du corpus** — 7 tuiles : 345 événements, 95 `validee`, 223 `chantier`, 26 `douteuse`, 1 `a_arbitrer`, 47 lignes à effet Q7 codé, 44 événements porteurs de rôles.
- **Chronologie codée** — barres empilées par année × statut, 1998 → 2024, total au-dessus de chaque barre, infobulle au survol et au clavier.
- **Filtres** (10) — statut, système, phase, domaine, arène, type d'acte, crise, effet Q7, acteur principal, origine, plus une recherche libre (id, intitulé, note, CVE). Chaque option affiche son effectif.
- **Distributions de la sélection** (8 cartes) — système, phase, domaine (les 8 de la thèse), arène, type d'acte, effets Q7 par dimension×signe, rôles posés, types d'acteurs aux rôles.
- **Table** — 13 colonnes triables, statut en pastille **+ libellé** (jamais la couleur seule).
- **Anomalies** — 10 familles calculées + un encadré des incohérences déjà instruites ailleurs.

## 3. Les anomalies, et ce qu'elles ont trouvé

| famille | n | règle |
|---|---:|---|
| lignes douteuses | 26 | `statut_ligne = douteuse` |
| à arbitrer | 1 | `statut_ligne = a_arbitrer` (E004) |
| chantier déjà très codé | 15 | chantier mais ≥ 4 champs analytiques remplis — **candidates à validation** |
| validées à champs manquants | 0 | validee sans acteur principal, arène ou type d'acte |
| doublons probables | 50 lignes / **26 paires** | même mois + ≥ 2 mots longs communs — indice, jamais verdict |
| sans identifiant de graphe | 138 | `gid` vide : la ligne n'est reliée à aucune entité |
| effets ambivalents (±) | 18 | convention r2 : le `±` exige une note |
| multi-effets | 2 | convention A4 (G006, G016) |
| **hors périmètre déclaré** | **4** | règle R3 : 18/07/2008 → début 2020 — **G122 (1998), G127 (2004), G170 (2022), G113 (2024)** |
| marqueurs `[CHANTIER` résiduels | 13 | un marqueur subsiste dans une colonne |

Deux résultats méritent ton œil. **Les 4 lignes hors périmètre** : la règle R3 de la grille v1 borne le catalogue au 18/07/2008 → début 2020, or G122 (ICANN, 1998), G127 (RipplePay, 2004), G170 (The Merge, 2022) et G113 (Figure 5, 2024) sortent de ces bornes — les quatre sont `chantier`. Soit ce sont des antécédents et des post-bornes assumés qu'il faut documenter comme tels, soit R3 doit être élargie, soit ces lignes sortent du corpus actif (`exclue`, l'ensemble vide depuis D4). C'est une décision : je ne l'ai pas prise.

**Les 26 paires de doublons probables** : le détecteur retrouve seul les cas connus (Genèse E003/G013/G063, E015 ↔ G001, les deux « First Bitcoin halving » G061 ↔ G069) et en propose d'autres non instruits (E002 ↔ G071 publication du WP, E004 ↔ G095 client Bitcoin-Qt, E012 ↔ G075 BitcoinMarket, G077 ↔ E013 pizzas, E032 ↔ G109 capital-risque…). Sur 14 paires inspectées à la main, **2 faux positifs** — le signal est bon, mais chaque paire reste à vérifier.

## 4. Couleur : calculée, pas choisie

Le statut de ligne est le seul encodage coloré. Quatre teintes, dans l'ordre d'incertitude croissante (`validee` → `chantier` → `douteuse` → `a_arbitrer`), **validées par `scripts/validate_palette.js` de la skill dataviz contre les DEUX surfaces du site** (bordeaux `#4d0000` et noir `#000000`) : zéro échec, pire paire adjacente CVD ΔE 8.4 (cible ≥ 8), vision normale ΔE 19.3 (plancher ≥ 15), contraste ≥ 3:1 partout.

Ce qui a été écarté en chemin, mesuré et non supposé : les teintes maison brutes (or, orange, vert néon) échouent — hors bande de luminosité, et or ↔ orange à ΔE 7.9, sous le plancher de vision normale. Quatre teintes en « toutes paires » sont hors d'atteinte, y compris pour la palette de référence de la skill : la validation porte donc sur la liste **adjacente** (usage réel : empilements ordonnés), et partout ailleurs **le statut est écrit en toutes lettres à côté de sa pastille**, de sorte que la couleur ne porte jamais seule.

L'esthétique du dépôt est respectée : Press Start 2P pour les titres, VT323 pour les données, palette bordeaux/or/vert, thème sombre commutable — le site n'est pas modernisé, il est prolongé. Aucune dépendance externe, aucun CDN : l'analyseur CSV et les graphiques SVG sont écrits à la main, la page fonctionne hors ligne (IPFS/Swarm compris).

## 5. Vérification navigateur (exigée par la charte)

Chromium local, page servie en HTTP, polices distantes coupées pour simuler le hors-ligne :

- **zéro `pageerror`** ; seule erreur console : le blocage volontaire des polices Google du test ;
- **les comptages de la page égalent les mesures Python indépendantes** — 345 lignes × 33 colonnes, 95/223/26/1 par statut, 47 effets, 44 événements à rôles, 76 lignes de rôle ;
- filtre « système = ethereum » → 33 lignes en table et en tuile, conforme à la mesure ;
- les deux thèmes rendus et inspectés ; tri, filtres, recherche et navigation par identifiant fonctionnels.

Deux défauts de lecture ont été trouvés à l'œil et corrigés : le tri par date ouvrait sur les 18 lignes sans date (les cellules vides vont désormais en fin de tri quel que soit le sens), et le « non codé » écrasait l'échelle des distributions (298 contre 14) — il est sorti de l'échelle et affiché comme contexte.

## 6. Effet de bord traité : le registre ne bougera plus

Le générateur du registre scanne `**/*.html`. Sans précaution, `catalogue-lab.html` ajoutait 6 `readBy` — sur `date`, `phase`, `source` (noms de colonnes CSV), `role` (attribut ARIA `role="img"`), `description` (balise `<meta>`) et `status` (`role="status"` et le code HTTP d'un `fetch`). Aucune n'est une lecture d'attribut du graphe : cette page ne lit aucun graphe.

L'exclusion est donc posée dans `EXCLUSIONS_READ_BY`, **vérifiée occurrence par occurrence** et commentée comme les précédentes. Résultat mesuré : `--check` reste vert **sans régénérer le registre** — le fichier versé est inchangé, et les prochaines pages de l'Observatoire n'y toucheront pas non plus. Reste, sans effet et non traité : `add_statut_ligne.py` et `make_v3_3_catalogue.py` figurent encore en `readBy` (état déjà versé) ; les en retirer ferait bouger le registre pour rien.

## 7. Un choix de périmètre à ratifier

La page est **en français seul**, alors que la convention du dépôt veut une contrepartie `-fr`/anglaise pour chaque page. Motif : c'est un instrument de travail sur un catalogue rédigé en français, et il est encore mouvant. La contrepartie anglaise se fera quand l'Observatoire deviendra public — d'un mot si tu préfères l'inverse. La page porte `noindex` en attendant.

## 8. Suite

Lot 2 (matrices acteurs × rôles, événements × Q7, phases × types d'actes, arènes × effets), lot 3 (dossiers de crise : CVE-2018, The DAO, Genèse, MtGox, monnayage), lot 4 (export article). Rien de tout cela ne touchera au graphe.
