# Intégration v3-3 — rapport de diff et preuves — 16/08/2026

Lot d'intégration ouvert par le feu vert M4 du 15/08/2026, après résolution de #128. Il **intègre au catalogue maître** le recodage des 40 lignes `propose(lot1)` instruit au lot 3, sous les vocabulaires gelés et les arbitrages M1-M3. Rien d'autre.

Applicateur : `scripts/make_v3_3_catalogue.py` (lot figé dans le code, `--dry-run`, contrôles d'arrivée bloquants). Le catalogue ne se modifie jamais à la main.

| fichier | empreinte | taille |
|---|---|---|
| `catalogue-evenements-v3-2.csv` (source, **intacte**) | `1b4b3aa4f74df0829ffbb149d22814e11e4324d5` | 146 182 o |
| `catalogue-evenements-v3-3.csv` (**produite**) | `7a87a37d9e05d7cbe096ece8d436506812ef68a4` | 150 829 o |

## 1. Diff v3-2 → v3-3 : 99 cellules, 35 lignes, 3 colonnes ajoutées

Le script recalcule le diff **cellule à cellule** et refuse d'écrire s'il diverge d'un seul élément du lot figé. Résultat mesuré, puis contre-vérifié par un script indépendant :

| colonne | cellules | quoi |
|---|---:|---|
| `statut_ligne` | 34 | 30 `chantier` → `validee`, 4 → `douteuse` |
| `codage_statut` | 30 | `propose(lot1)` → `valide(lot3)` sur les seules lignes validées |
| `effet_prop_monetaires` | 22 | `nd` → effet Q7 v1 |
| `notes` | 4 | trace des corrections (cellules **vides** dans la source — rien n'est recouvert) |
| `date` | 2 | G032 `2014-07-04` → `2014-04-07` · G006 `2013` → `2013-03` |
| `codage_justif` | 2 | G011 et G013 : justifications du lot 1 contredites |
| `precision` | 1 | G006 `annee` → `mois` |
| `acteur_principal` | 1 | G011 `core_devs` → `regulateurs_etats` |
| `crise` | 1 | G013 `oui` → `non` (**M1**) |
| `type_acte` | 1 | G013 `incident` → `innovation_protocolaire` (**M1**) |
| `fil` | 1 | G013 `crises-protocolaires` → `genese` (**M1**, le fil que porte déjà E003) |

**Colonnes ajoutées (arbitrage A1)** : `acteur_principal_mode`, `acteur_principal_id`, `acteur_principal_nom` — **vides sur les 305 lignes hors lot** (contrôlé), remplies sur les 40 : 27 `systeme_protocole` (protocole Bitcoin `d35d720e`), 12 `initiateur`, 1 mode vide côté id pour G011/G038 (aucune entité graphe : nom seul, cas prévu par A1).

**Aucune ligne hors des 40 n'est modifiée, sur aucune colonne** — vérifié par balayage complet. 346 lignes, CRLF conservé, 30 → 33 colonnes.

## 2. Table des transitions de statut

| transition | n | lignes |
|---|---:|---|
| `chantier` → `validee` | 30 | G003, G006, G007, G010, G014-G031 (hors G013), G033-G037, G039, G040, G042 |
| `chantier` → `douteuse` | 4 | G001 (M2 : E015 canonique) · G008 (statut contesté) · G011 (doublon multiple) · **G013 (M1 : doublon Genesis signalé)** |
| `chantier` maintenu | 6 | G004, G005, G009, G032, G038, G041 |

Distribution du catalogue : `validee` 65 → **95** · `chantier` 257 → **223** · `douteuse` 22 → **26** · `a_arbitrer` 1 (E004, inchangée) · `exclue` 0.

**M1 appliqué intégralement** : G013 n'est plus une crise. Le doublon est **signalé, non fusionné** — E003 (texte, calibrage, `crise=non` depuis toujours) et G063 (graphe) décrivent le même bloc de genèse ; le dédoublonnage vérifié avait classé G013 ↔ G063 en `REJET_AUTO` (types différents). Aucun patch graphe, aucune fusion.

## 3. Table des effets Q7 ajoutés (22)

| effet | n | lignes |
|---|---:|---|
| `conf_methodique(±)` | 14 | 12 DOS (G014, G015, G019, G021-G024, G026, G029, G031, G034, G040) + G018, G020 (netsplits non réalisés) |
| `integrite_monnayage(±)` | 4 | G003, G028, G030, G039 |
| `conf_methodique(-)` | 1 | G033 (scission réalisée, BIP-66) |
| `conf_methodique(-) usage_paiement(-)` | 1 | G016 (DOS exploité) |
| `integrite_monnayage(-) conf_methodique(-)` | 1 | G006 (scission réalisée + double dépense) |
| `integrite_monnayage(+)` | 1 | G007 (BIP-0042 fixe le cap des 21 M) |

**Règle D4 tenue** : les lignes `chantier` et `douteuse` ne reçoivent **aucun** effet au maître — leurs effets proposés restent dans `lot3-recodage-propose-lot1.csv`, qui en garde la trace. Cela concerne G001 (effet riche, mais E015 est canonique) et G009 (Theft, système à éclaircir). Une ligne non validée n'exporte pas de donnée stabilisée.

**Bornage M3 vérifié ligne à ligne** sur les 4 `integrite_monnayage(±)` intégrés :

- G003 (Vol de clés privées) et G030 (Theft n°22) — la classe *Theft* est définie par la thèse comme « prendre le contrôle d'UCN en dehors des règles protocolaires consensuelles » (l.192, l.249) : **captation d'unités, explicite**.
- G028 (Fake Conf) et G039 (Preuve SPV falsifiée) — la justification ne passe pas par une captation directe mais par deux mots de la définition gelée : *falsification* (le nom même de la classe « Preuve SPV falsifiée ») et *intégrité quantitative*. Ancrage textuel : la thèse relie explicitement double dépense et production d'UCN surnuméraires — « le risque de production d'UCN surnuméraires résidait dans les mécanismes entourant la double dépense » (l.225). **Ce sont les deux cas les plus éloignés du bornage** : un mot suffit à les basculer en `conf_methodique(±)` si tu juges que c'est forcer.
- Les 14 `conf_methodique(±)` relèvent de la lecture (1) de M3, ratifiée : mise en cause non activée, note obligatoire — chaque ligne porte sa `codage_justif`, et le script refuse d'écrire un `±` sans note.

## 4. Table des rôles ajoutés (36 au maître, 7 écartés)

`catalogue-roles-v0.csv` : **40 → 76 lignes**, empreinte `14d1db05088efb9bf3c527a97fc2ab6c2a4ced5b`.

| rôle | n | acteurs |
|---|---:|---|
| `correcteur` | 30 | `core_devs` — correctif protocolaire énoncé, ligne à ligne |
| `initiateur` | 5 | `core_devs` — déploiement des soft forks BIP-0034, BIP-0042, BIP-65, BIP-66, BIP-68/112/113 |
| `exploiteur` | 1 | `nd` + nom — auteur non nommé de la double dépense OKPAY (G006) |

**Même règle que pour les effets** : seules les lignes `validee` versent au maître. Les 7 rôles restants (G004, G009, G011, G032, G038, G041) demeurent dans `roles-lot3-propose.csv`. Les 40 lignes antérieures de la table (épreuve Q7 du lot 2) sont **inchangées** — dont 7 sur des lignes non validées, ce qui était le propos de l'épreuve.

Rappel du périmètre : aucun rôle inventé, aucun `exploiteur` sur l'exploitation *involontaire* de G016, aucun rôle sur G001 (E015 canonique) ni sur G013 (doublon).

## 5. Preuve que les vocabulaires gelés n'ont pas bougé

Empreintes identiques à celles du gel du 15/08 :

| document gelé | empreinte, avant et après ce lot |
|---|---|
| `grille-roles-v0.md` (grille de rôles v0 **gelée**) | `00e720579f20031198bf2b4f8c2d12c939ab38d8` |
| `vocabulaire-q7-v1-proposition.md` (Q7 v1 **gelé**) | `55bf8d9c5757bd096d9bbe77b78dfe402b61ba1b` |
| `arbitrages-gel-q7v1-roles-v0-2026-08-15.md` (verbatim) | `b20acde7ef7136ef8ef7105ecdad5ac14fdabd91` |
| `catalogue-evenements-v3-2.csv` (source, conservée) | `1b4b3aa4f74df0829ffbb149d22814e11e4324d5` |

En outre, l'applicateur **recopie les vocabulaires gelés pour les vérifier** (9 dimensions Q7, 5 statuts D4, 5 modes A1) et refuse toute valeur hors liste, sur l'intégralité du fichier de sortie — pas seulement sur les lignes qu'il touche.

## 6. Effet de bord traité dans le même lot : fraîcheur du registre

`scripts/make_v3_3_catalogue.py` mentionne les mots `date`, `source` et `count` — **noms de colonnes du CSV et de variables**, pas des clés d'attribut du graphe (ce script ne lit aucun graphe). Le générateur du registre les indexe néanmoins en `readBy` : le registre commité devient donc obsolète dès que le script entre au dépôt. C'est exactement le manquement du lot 2, cette fois **anticipé et corrigé dans le même lot**, comme `CLAUDE.md` l'exige.

Registre régénéré par son propre script : **3 insertions `readBy`** sur les clés `count`, `date`, `source` ; **338 entrées, aucune clé ajoutée ni retirée, aucun autre champ modifié**, `_meta` inchangé. Nouvelle empreinte : `ef1a445eaf67fe0d150689c9edc055e22e14b05a` (143 036 o).

**Dette identifiée, non traitée ici** : la voie propre serait d'ajouter les scripts *catalogue* (`add_statut_ligne.py`, `make_v3_3_catalogue.py`) aux exclusions de faux positifs lexicaux de `build_properties_registry.py` — comme #128 l'a fait pour `build_applicator_inventory.py`. Je ne l'ai pas fait : ce fichier est précisément celui que modifie #128, et y toucher créerait le conflit que ce lot vient de résoudre. À reprendre après le merge, en une ligne.

## 7. Périmètre tenu

Aucun patch graphe, aucune v116, aucune fusion catalogue/graphe, aucune modification du site, aucun vocabulaire gelé touché, aucune correction opportuniste hors lot, aucun recodage au-delà des 40 lignes. Le graphe v115 est intact. La v3-2 est conservée telle quelle : la v3-3 ne l'écrase pas.
