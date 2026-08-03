# Hard forks d'Ethereum — ajout au graphe

**Date** : 2026-08-03
**Graphe** : `v103` → **`v104`**
**Source** : `docs/research/chronologies/Chronologie_des_HF_dEthereum_V1.bin`
**Autorité** : **chronologie constituée et vérifiée par Maël Rolland**, non
mobilisée dans la thèse
**Script** : `scripts/make_v104_ethereum_hard_forks.py`

---

## Pourquoi ces événements ne sont pas dans la chronologie carnavalesque

**Et pourquoi c'est normal.** Ce point est répété dans la description de
chaque entité créée, dans ses attributs de provenance et ici, pour qu'aucun
audit ultérieur ne les signale comme une anomalie ou une lacune.

La chronologie n° 6, dite « carnavalesque », porte le **développement
infrastructurel de Bitcoin** (chapitre I, section I.2), sur la période
18/07/2008 → début 2020, avec le code couleur des 8 domaines. Les hard forks
d'Ethereum relèvent d'un autre objet, et **six des quatorze sont postérieurs
au périmètre de la thèse** (jusqu'au 09/12/2021).

Leur absence de la frise carnavalesque n'est **ni un oubli, ni un défaut du
graphe** : c'est une différence de périmètre, et la frise dont ils viennent
est une source distincte, que l'auteur a constituée et vérifiée sans la
mobiliser dans le texte.

## Marquage de provenance

Chaque entité créée porte :

| attribut | valeur |
|---|---|
| `dateAuthority` | `AUTHOR_VERIFIED` |
| `dateSource` | Chronologie des HF d'Ethereum V1 (M. Rolland) — constituée et vérifiée par l'auteur, non mobilisée dans la thèse |
| `source` | idem |
| `evidenceStatus` | `author-verified — hors chronologie n° 6, hors périmètre de la thèse` |
| `protocol` | `Ethereum` |

`AUTHOR_VERIFIED` est une valeur nouvelle : le graphe n'employait jusqu'ici
que `TIMELINE_FIGURE` (37 entités), qui renvoie à la figure de la thèse. La
distinction est voulue — ces dates ne viennent pas de la figure, elles
viennent de l'auteur.

## Ce qui a été ajouté

**11 entités `ProtocolChange` créées**, 3 forks déjà présents seulement
chaînés :

| | fork | date | statut |
|---|---|---|---|
| [0] | Olympic (testnet) | 2015-05-09 | déjà présent |
| [1] | Frontier | 2015-07-30 | déjà présent |
| [2] | Frontier Thawing | 2015-08-04 | **créé** |
| [3] | Homestead | 2016-03-14 | **créé** |
| [4] | DAO Fork | 2016-07-20 | déjà présent |
| [5] | Tangerine Whistle | 2016-10-18 | **créé** |
| [6] | Spurious Dragon | 2016-11-22 | **créé** |
| [7] | Byzantium | 2017-10-16 | **créé** |
| [8] | St. Petersburg | 2019-02-28 | **créé** |
| [9] | Istanbul | 2019-12-08 | **créé** |
| [10] | Muir Glacier | 2020-01-02 | **créé** |
| [11] | Berlin | 2021-04-15 | **créé** |
| [12] | London | 2021-08-05 | **créé** |
| [13] | Arrow Glacier | 2021-12-09 | **créé** |

Chaque description conserve le détail de la frise — numéro de bloc et EIPs.

**24 relations** : 11 `part of` vers le protocole Ethereum, et 13
`followed by` qui chaînent la frise entière, *y compris à travers les trois
forks déjà présents*. C'est ce qui en fait une chronologie et non une liste.

Une coquille de frappe est corrigée dans le **nom d'entité** — « Frontier
Thawind » → « Frontier Thawing », le nom officiel du fork. Le libellé source
reste intact dans la description : on ne réécrit pas la source, on lui donne
un nom d'entité juste.

## Ce que le script ne fait pas, délibérément

- **Aucune relation `appears in section`.** Ces événements ne figurent dans
  aucune section de la thèse ; leur en attribuer une serait une invention.
  C'est aussi pourquoi ils n'apparaîtront pas dans le lecteur par section —
  attendu, pas cassé.
- **Aucun rattachement aux 8 domaines.** Ceux-ci décrivent le développement
  infrastructurel de **Bitcoin** (ch. I l. 251), pas celui d'Ethereum.
  Les y forcer étendrait un cadre au-delà de ce que la thèse lui donne.
- **Aucune création pour les 3 forks déjà présents**, pour ne pas créer de
  doublon.

## Signalé, non traité

Le graphe porte **deux entités pour le lancement de Frontier** :
« InfrastructureEvent — Lancement d'Ethereum (Frontier, 30 juillet 2015) » et
« Frontier (lancement mainnet Ethereum, juillet 2015) ». Doublon antérieur à
ce lot ; le chaînage n'en accroche qu'une. Relève du chantier de
dédoublonnage (`patch_10`).
