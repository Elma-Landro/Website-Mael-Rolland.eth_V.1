# Les 8 domaines de développement infrastructurel — rétablissement et câblage

**Date** : 2026-08-03
**Graphe** : `v101` → **`v102`** (rétablissement) → **`v103`** (câblage)
**Branche** : `agent/grc20-section-migration-ch2-v1`
**Source d'autorité** : thèse, chapitre I, l. 251 (verbatim) + `docs/audits/grille-codage-catalogue-v1.md`

---

## Le défaut, et pourquoi il était invisible

La thèse définit **8 domaines de développement infrastructurel de Bitcoin**,
avec un code couleur porté par la chronologie n° 6 :

| | domaine | couleur | segments de Rauchs (2016, p. 118-119) |
|---|---|---|---|
| (i) | sphère d'usage réelle et financière | vert | 14 segments |
| (ii) | **traitement des transactions** | jaune | « minage » |
| (iii) | portefeuilles et paiements | orange | « portefeuille », « mixage » |
| (iv) | information et connaissance | bleu foncé | médias, données, outils de dév. |
| (v) | conformité aux réglementations nationales | bleu clair | conformité, autres services |
| (vi) | protocole Bitcoin | rouge | — |
| (vii) | Altcoins | rose | — |
| (viii) | autres | violet | — |

Le graphe comptait bien **huit** `InfrastructureDomain`. Le compte était juste,
la liste ne l'était pas : **(ii) n'y figurait pas**, et un intrus occupait la
huitième place — « De la confidentialité et de l'anonymisation », que la thèse
range *dans* (iii) comme le segment « mixage ».

C'est ce qui a permis au défaut de survivre : tout contrôle qui compte les
domaines trouve 8 et se déclare satisfait.

## Le domaine (ii) n'avait pas disparu — il était mal typé

Le diagnostic initial, ici comme dans la passation du 03/08, était que le
graphe n'avait « aucun domaine correspondant à (ii) ». **C'est inexact, et il
faut corriger ce constat.**

Le nœud `8fc8b0d7…` « Traitement des transactions » existe et remplit déjà
toutes les fonctions d'un domaine :

- **30 relations `belongs to domain`** entrantes — *Mining pools*, *GHash.io*,
  *GPU mining emergence*, *ASIC mining introduction*, *InfrastructureEvent —
  Mining pools (coopératives de minage)*…
- `contains segment` → **« Minage »**, exactement le segment que la thèse lui
  assigne ;
- un `drives demand` reçu de « Sphère d'usage » ;
- 31 `appears in section`.

Il portait simplement le type `Concept` au lieu d'`InfrastructureDomain`.

**Conséquence pratique** : la conclusion de la passation — « les événements de
minage ne peuvent pas être rattachés depuis le graphe seul, c'est une lacune
de l'ontologie » — tombe. Les rattachements étaient là, invisibles parce que
leur cible n'était pas reconnue comme domaine.

Une première tentative avait créé un **nouveau** nœud pour (ii). Elle a été
jetée avant tout commit : elle aurait fabriqué un doublon vide à côté d'un
nœud portant 67 relations.

## v102 — rétablissement

1. **Retypage** de `8fc8b0d7…` : ajout du type `InfrastructureDomain`, avec
   `domain_index = ii` et `color = jaune`. Le type `Concept` est **conservé** —
   ce nœud est bien les deux, et le retirer casserait toute vue filtrant sur
   les concepts. Les sept autres domaines ne portent qu'`InfrastructureDomain` ;
   l'hétérogénéité est signalée, pas corrigée de force.
2. **Fusion** de « De la confidentialité et de l'anonymisation » dans (iii) :
   8 relations rebranchées, 2 doublons écartés, le nœud disparaît.

Les 8 domaines de la thèse, avec leur charge réelle :

```
Sphère d'usage                            134
Protocole et couche de base               110
Traitement des transactions                67
Services de portefeuille et de paiement    50
Conformité réglementaire                   33
Information et connaissance                32
Altcoins, tokens et surcouches             24
[Résiduel — à reclasser]                    8
```

## v103 — câblage depuis le catalogue v2

Le catalogue `docs/audits/data/catalogue-evenements-v2-fusion.csv` (253 lignes)
porte une colonne **`gid`** : la jointure vers le graphe est explicite. Les
113 lignes joignables (`gid` + `domaine_8`) **résolvent toutes** dans le
graphe — aucun identifiant inconnu.

**Aucun appariement par similarité de libellé n'est employé.** Celui du dépôt
produit des faux positifs visibles — « Premier achat de 2 pizzas » apparié à
« Bitcoin Faucet », « Crise chypriote » à « Crise BIP-0016 » — et le score ne
les distingue pas des bons appariements. Un rattachement au mauvais domaine
serait pire que pas de rattachement.

Ce que les 113 lignes apportent réellement :

| n | statut | traitement |
|---:|---|---|
| 81 | `origine=graphe` : le domaine **vient** du graphe | écarté — le réécrire serait circulaire |
| 17 | confirment un domaine déjà posé | écarté — validation croisée, rien à écrire |
| 6 | **contredisent** le graphe | **signalés, non tranchés** |
| **9** | l'entité n'a **aucun** domaine, le catalogue en code un | **retenus** |

**L'apport net est donc de 9 rattachements, pas de 113.** C'est peu, et c'est
la mesure honnête de ce que le catalogue ajoute au graphe aujourd'hui.

Les 9 :

| domaine | événement | source |
|---|---|---|
| (vii) | Lancement Litecoin (LTC) | ch. I l. 359 |
| (i) \* | Attaque DDoS MtGox (mai 2013) | ch. I l. 281 |
| (vii) | Première ICO : Mastercoin | ch. I l. 373 |
| (vii) | Ether Genesis Sale (ICO Ethereum 2014) | ch. I l. 399 |
| (vii) | Lancement d'Ethereum (Frontier) | ch. I l. 399 |
| (vii) | The DAO ICO | ch. III l. 553-557 |
| (vii) | Attaque de The DAO | ch. III l. 561 + 565 |
| (ii) \* | Congestion du mempool et hausse des frais | ch. I l. 293 |
| (vi) | Bitcoin CVE 2018-17144 | ch. III l. 11 + 39 + 476 |

`*` = attribution par définition, sans vérification du code couleur de la
figure. Le marqueur est conservé dans le motif de chaque relation posée, pour
que la provenance reste lisible.

À noter : « Congestion du mempool » atterrit dans **(ii)** — le domaine qu'on
vient de rétablir reçoit immédiatement du contenu.

## Les 6 divergences — à arbitrer

Consignées dans `docs/audits/data/domaines-divergences.csv`. Le catalogue et
le graphe se contredisent ; ni l'un ni l'autre n'a été retenu d'office.

| entité | catalogue | graphe | attribution |
|---|---|---|---|
| Publication du code Bitcoin | (iii) | (ii) + (vi) | codé à la main |
| Service de séquestre | (iii) | (i) | par définition |
| Service d'anonymisation | (iii) | (v) + (viii) | codé à la main |
| Fondation Bitcoin | (viii) | (v) | par définition |
| Hack et faillite MtGox (février 2014) | (viii) | (i) | par définition |
| Ethereum Hard Fork (juillet 2016) | (vii) | (i) + (vi) | codé à la main |

Deux d'entre elles méritent l'œil en premier : « Publication du code Bitcoin »
codé (iii) alors que le graphe dit (ii) + (vi) semble peu probable, et
« Service d'anonymisation » en (iii) est cohérent avec la thèse — le mixage
relève de (iii) — contre un graphe qui dit (v) + (viii).

## Ce qui reste

**101 des 219 événements du graphe n'ont aucun domaine.** Le catalogue n'en
couvre que 9, parce que **94 de ses lignes n'ont pas encore de `domaine_8`** —
et la passation est explicite : ce codage est **humain**, la grille définit des
vocabulaires fermés qu'aucune inférence ne peut deviner.

Les 175 lignes issues du graphe arrivent aussi avec `acteur_principal`, `arene`
et `type_acte` vides. C'est le chantier de codage restant, hors périmètre d'un
agent.
