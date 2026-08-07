# Poids d'ancrage v2 — qualifier avant de corriger

**Date** : 2026-08-07
**Graphe** : `grc20-these-mael-rolland-v110.json` (inchangé par ce chantier)
**Branche** : `claude/file-upload-branch-check-jw4cng`
**Mode agent** : A (diagnostic) + C (champs de qualification dans la carte, sur données probantes)
**Outil** : `scripts/build_anchor_weights.py` · **Données** : `docs/audits/data/poids-ancrage-diagnostic-v110.csv`
**Prédécesseur** : `grc20-ancrage-poids-mandataires-v1.md` (v1, 2026-08-03)

---

## 1. Diagnostic, ligne à ligne cette fois

L'audit v1 avait établi le problème au niveau des entités (571 sur 1 171
partagent leur signature d'occurrences — chiffre **reproduit à l'identique**
par le présent outil, ce qui valide les deux mesures l'une par l'autre).
Le présent chantier descend au niveau de la **ligne de carte** — le couple
(section, entité) que le lecteur classe réellement :

| `weightStatus` | lignes | % | ce que ça veut dire |
|---|---:|---:|---|
| **`proxy`** | **10 249** | **82,8 %** | des extraits existent, aucun ne contient le nom de l'entité — le poids compte un autre terme |
| `self` | 1 207 | 9,8 % | le nom figure dans au moins un extrait — le poids compte bien l'entité |
| `no-snippet` | 918 | 7,4 % | aucun extrait (reconstruction v81, réparations) — invérifiable |

**Panneaux affectés : 54 sur 54.** Chaque panneau du lecteur contient au
moins un nœud non vérifié dans son top-12.

**Ce qui lit `occurrence_count`** (périmètre d'impact exact) :
`lecteur.html` — calcul TF-IDF (l. ~1197-1213) et agrégation des parentes
(l. ~1249-1265) — et `scripts/fix_dead_ids_in_section_map.py` (historique,
fusion de doublons). **`graphe.html` ne le lit pas** : ses compteurs viennent
des relations. Le problème est donc circonscrit au panneau du lecteur.

## 2. Ce qu'un classement corrigé changerait — mesuré, pas estimé

Top-12 par section, formule exacte du lecteur, épinglés d'abord, sous deux
classements : l'actuel (`occurrence_count`) et un classement par
`directAnchorCount` (présence textuelle mesurée) :

- **survie du top-12 actuel : 296 places sur 648 (45 %)** ;
- sections les plus bouleversées : `I.3.3`, `conclu_aceph`,
  `glossaire_preamble` (0 survivant), `intro_E`, `I.3.2`, `II.3.1`,
  `III.1.2`, `conclu_traduction` (2 survivants) ;
- les plus stables : `ch3_preamble` (11/12), `II.3` et `ch2_preamble`
  (10/12), `III.3.4` (9/12).

**Et le chiffre qui interdit un basculement immédiat** : sous classement
direct, `conclu_aceph` n'a que **3 candidats mesurables**,
`glossaire_preamble` **0** (sa plage de texte n'est pas dérivable — le
glossaire n'a pas de carte de titres), `intro_E` **2**. Remplacer le
classement viderait des panneaux. C'est la conclusion de la voie A simulée
(v1 § 5), confirmée sur les plages désormais justes.

## 3. Modèles comparés — et pourquoi le plus prudent gagne

| Modèle | Nature | Ce qu'il coûte | Verdict |
|---|---|---|---|
| **`weightStatus`** (classification self/proxy/no-snippet) | donnée SUR la donnée : aucune mesure nouvelle, dérivée des extraits que la carte porte déjà | rien — aucun affichage ne change | **retenu** |
| **`directAnchorCount`** (présence textuelle, limites de mots) | mesure minimale, règle écrite dans le script, rejouable | `null` là où la plage n'est pas dérivable ; ne mesure PAS l'importance analytique | **retenu comme compagne**, pas comme classement |
| Remplacer `occurrence_count` (voie A) | destructif | listes divisées par ~5, panneaux vidés (§ 2) | rejeté ici — décision d'auteur |
| Score composé (mixte présence/degré/df) | interprétatif | inventerait une importance que rien n'atteste | rejeté — « ne pas inventer de score scientifique » |
| Classement par relations (voie B) | non interprétatif | prouvé dégénéré (multiplicité 1 partout, v1 § 3) | rejeté sur preuve |

**Noms des champs, justifiés** : `weightStatus` dit ce que c'est — un statut
du poids existant, pas un poids. `directAnchorCount` dit exactement ce qu'il
compte — des occurrences d'ancrage directes du nom, rien de plus. Les noms
candidats `anchorWeightV1` (promet un poids officiel qu'on ne décrète pas)
et `sectionLocalRank` (un rang est un choix d'affichage, pas une donnée)
mentiraient sur leur contenu.

## 4. Ce qui est appliqué — et ce qui ne l'est pas

**Appliqué** : les deux champs sur chacune des 12 374 lignes de
`section_entities_map.json`. `occurrence_count` est **intact partout**
(vérifié). Aucun graphe touché — la dette vit dans la carte ; un
`patch_20`/v111 l'aurait **importée dans le graphe** au lieu de la réparer,
c'est le motif de l'absence de patch de graphe. Le script est idempotent et
porte un `--check` (rejouer sans `--apply` compare ; la CI peut l'appeler).

**Non appliqué, délibérément** : tout changement de classement. Le lecteur
affiche aujourd'hui la même chose qu'hier. Basculer le tri — vers
`directAnchorCount`, vers un filtre `self` d'abord, ou vers la voie A
complète — est un **choix éditorial de l'auteur**, désormais instruit par
des chiffres au lieu d'une intuition.

## 5. La règle de mesure, écrite pour être attaquée

`directAnchorCount` = occurrences du **nom littéral** de l'entité,
normalisé (casse, accents, apostrophes), en **limites de mots**, dans le
**corps du bloc de la section plus les définitions des notes qui y sont
appelées** (les notes vivent en bloc terminal — les inclure en bloc
compterait celles des autres sections, les exclure amputerait l'appareil).
Divergence assumée avec la règle historique § 1.3 (sous-chaîne) : la
sous-chaîne comptait « Mist » dans « administration ». Conséquence à ne pas
oublier en lecture : un nom que la thèse n'écrit jamais tel quel
(`InfrastructureEvent — …`, libellés bilingues) compte 0 **sans que l'objet
soit absent** — c'est ce que `weightStatus` existe pour distinguer.

## 6. Risques restants

- `directAnchorCount` sous-compte les entités aux noms forgés ou traduits ;
  il ne doit jamais être lu seul, toujours avec `weightStatus`.
- Les 918 lignes `no-snippet` restent invérifiables par cette voie.
- La carte des poids doit être **régénérée** si les MD, la carte des titres
  ou les noms d'entités changent (`--check` le détecte).
- Le partage de signature (571 entités) est une preuve de mandat plus forte
  que le test par extrait ; le CSV permet de croiser les deux.

## 7. Décisions réservées à Maël

1. **Le classement du panneau** : garder l'actuel, filtrer `self` d'abord,
   basculer sur `directAnchorCount`, ou voie A complète — avec le § 2 comme
   étude d'impact.
2. Le sort des **10 249 lignes `proxy`** : les garder comme contexte
   assumé (elles disent « cette section parle de Bitcoin ») ou les purger.
3. Les **918 `no-snippet`**.
4. L'affichage éventuel du statut dans le lecteur (badge « vérifié » ?).
