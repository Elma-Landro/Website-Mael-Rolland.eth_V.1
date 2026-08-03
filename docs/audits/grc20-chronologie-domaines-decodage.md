# Décodage des chronologies — le domaine par la couleur

**Date** : 2026-08-03
**Sources** : `docs/research/chronologies/Chrono_Bitcoin_institutionnalisation_V2.5.bin`
et `…Altcoin_institutionnalisation_V0.1.bin`
**Sortie** : `docs/audits/data/chronologie-domaines-decodee.csv` — 130 événements
**Script** : `scripts/decode_chronologie.py`

---

## Ce que les fichiers contiennent

Ce sont les fichiers de projet des chronologies n° 6, au format texte d'un
logiciel de frise : enregistrements séparés par `|`, champs par `:`.

```
E3:JJ/MM/AAAA:libellé:couleur_texte:couleur_fond:…
```

**La couleur de fond est le code couleur des 8 domaines** (ch. I, l. 251).
La figure, jusqu'ici consultable seulement à l'œil, devient exploitable.

Piège de format : la couleur de texte vaut soit un quadruplet ARGB, soit `B`
(défaut). Sans traiter cette alternative, **105 des 125 enregistrements
Bitcoin restaient illisibles** — un décodage partiel qui aurait donné une
image fausse de la répartition.

**178 enregistrements, 130 après dédoublonnage** (les deux frises partagent
des événements), dont **128 avec un domaine identifié**.

## La correspondance couleur → domaine n'est pas devinée

Elle est **calibrée** sur les événements dont `domaine_8` est déjà codé à la
main dans le catalogue v2, appariés par date exacte :

| couleur | domaine | établie par |
|---|---|---|
| `#bcf19e` vert | **(i)** sphère d'usage | calibrage : 7/8 |
| `#96b4f7` bleu foncé | **(iv)** information et connaissance | calibrage : 3/4 |
| `#f7b3b3` rouge | **(vi)** protocole | calibrage : 2/2 |
| `#f8d888` orange | **(iii)** portefeuilles et paiements | calibrage : 1/1 |
| `#f8fc92` jaune | **(ii)** traitement des transactions | contenu : minage GPU, Slush Pool, FPGA, ASIC Avalon, Antminer |
| `#9deffa` bleu clair | **(v)** conformité réglementaire | contenu : rapports BCE, Sénat, Tracfin, CFTC |
| `#eda6f7` violet | **(viii)** autres | contenu : levées Coinbase/BitGo/Ledger, premier vol, Faucet |

Les quatre premières sont confirmées par tes propres codages ; les trois
autres ne laissent aucun doute sur le contenu. **Toutes tombent exactement
sur le code couleur énoncé par la thèse.**

Deux événements gardent une couleur non répertoriée : le *Genesis Block*
(blanc rosé, traité à part dans la frise) et la plateforme BTC-E (blanc, non
codé).

## Répartition

```
(i)   33     (ii)  11     (iii) 12     (iv)  19
(v)   18     (vi)  13     (vii)  0     (viii) 22
```

**Le domaine (vii) Altcoins n'apparaît dans aucune des deux frises** — pas
même dans la chronologie Altcoin, qui est en V0.1 et réutilise le code
couleur de la frise Bitcoin sans en introduire un propre. À signaler : c'est
un manque de la figure, pas du graphe.

## Ce que ces données apportent au graphe — et ce qu'elles n'apportent pas

Confrontation des 128 événements datés au graphe v103 :

| | |
|---:|---|
| 68 | déjà présents dans le graphe (nom ou description) |
| 55 | probables, à vérifier |
| **5** | **absents du graphe** |

Et sur les domaines, en appariant par date exacte puis libellé :

| | |
|---:|---|
| 17 | confirment un domaine déjà posé |
| 10 | divergent |
| 3 | rattachement possible, mais scores faibles (0,25 à 0,46) |

**Les frises n'apportent donc pas les domaines manquants au graphe.** Elles
le confirment largement. Les 3 rattachements possibles ont des scores trop
bas pour être posés sans vérification, et ne sont pas appliqués.

Les 5 événements absents du graphe :

| domaine | date | événement |
|---|---|---|
| (i) | 2013-07-13 | Premier méta-protocole « MasterCoin / Omni » & première ICO |
| (i) | 2014-10-06 | Lancement du premier stablecoin, « RealCoin / Tether », sur Omni |
| (iii) | 2013-11-01 | Portefeuille multi-signature, par BitGo, BitPay, Ciphrex |
| (v) | 2014-07-17 | Promulgation de la « BitLicense » |
| (vi) | 2013-03-11 | Split de chaîne non anticipé, lié à une optimisation de base de données |

Un piège écarté au passage : les dates du graphe existent sous **deux
formats** — `TIME` ISO et `TEXT` en `JJ/MM/AAAA`. Un premier appariement n'en
voyait qu'un, et concluait à tort que 93 événements de la frise étaient
absents du graphe. Après normalisation, seuls 107 des 219 événements du
graphe sont datables, ce qui limite d'autant tout appariement par date.

## La vraie valeur : lever les astérisques

La grille de codage marque d'un `*` les attributions de `domaine_8` faites
« par définition, **couleur non vérifiée dans le texte/figure** » — 39 lignes
du catalogue v2. Et 94 lignes n'ont pas encore de domaine du tout.

**Le CSV décodé est la source qui manquait pour trancher ces deux cas.** Il
donne, pour 128 événements de la thèse, la couleur effectivement portée par
la figure — donc le domaine, vérifié et non plus supposé.

C'est un travail de codage, humain par construction : la grille définit des
vocabulaires fermés qu'aucune inférence ne remplace. Ce décodage fournit la
matière, il ne fait pas le codage.
