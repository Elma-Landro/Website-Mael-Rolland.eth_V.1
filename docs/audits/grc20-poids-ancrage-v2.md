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

| `snippet_status` | lignes | % | ce que ça veut dire |
|---|---:|---:|---|
| **`proxy`** | **9 899** | **80,0 %** | des extraits existent, ni le nom ni sa base de citation n'y figurent |
| `self` | 1 121 | 9,1 % | le nom complet figure dans un extrait, en limites de mots |
| `self-base` | 436 | 3,5 % | la base de citation du nom y figure (« Théret 2008 » pour « Théret 2008 — Les trois états ») — références réellement citées |
| `no-snippet` | 918 | 7,4 % | aucun extrait — **mais 576 de ces lignes ont une présence textuelle mesurée** (`direct_anchor_count` ≥ 1) : la catégorie n'est pas homogène |

La revue hostile de ce chantier a corrigé la première version de cette
classification, et les trois prises sont intégrées : le test par extrait est
passé **en limites de mots** (la sous-chaîne validait « Entretien n°2 » par
« Entretien n°24 » — 86 faux `self`) ; la **base de citation** est testée
(436 références passaient pour proxy alors que leur clé de citation est dans
l'extrait) ; et `snippet_status` **n'est pas un certificat** : les clés de
section des extraits d'`entity_section_map.json` sont elles-mêmes
partiellement périmées — les clés terminales de fichier (`I.4`, `II.4`,
`III.4`, `intro_E`) ont avalé l'appareil de notes entier (dette v1 § 7,
non réparée ici, déclarée comme découverte de ce chantier) — d'où des
lignes `self` à `direct_anchor_count` = 0. **Croiser toujours les deux
champs.**

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
`direct_anchor_count` (présence textuelle mesurée) :

- **survie du top-12 actuel : 294 places sur 648 (45 %)** — chiffre produit
  par `build_anchor_weights.py --impact`, **déterministe** (bris d'égalité
  explicite par `entity_id` : avec ~10 000 lignes à mesure nulle, un tri sans
  bris d'égalité dépendrait de l'ordre d'insertion JSON et le chiffre ne
  serait pas rejouable — la première version de cet audit annonçait 296, non
  reproductible, retirée) ;
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
| **`snippet_status`** (classification self/self-base/proxy/no-snippet) | donnée SUR la donnée : aucune mesure nouvelle, dérivée des extraits que la carte porte déjà | rien — aucun affichage ne change | **retenu** |
| **`direct_anchor_count`** (présence textuelle, limites de mots) | mesure minimale, règle écrite dans le script, rejouable | `null` là où la plage n'est pas dérivable ; ne mesure PAS l'importance analytique | **retenu comme compagne**, pas comme classement |
| Remplacer `occurrence_count` (voie A) | destructif | listes divisées par ~5, panneaux vidés (§ 2) | rejeté ici — décision d'auteur |
| Score composé (mixte présence/degré/df) | interprétatif | inventerait une importance que rien n'atteste | rejeté — « ne pas inventer de score scientifique » |
| Classement par relations (voie B) | non interprétatif | prouvé dégénéré (multiplicité 1 partout, v1 § 3) | rejeté sur preuve |

**Noms des champs, justifiés — et corrigés par la revue** : la première
version disait `weightStatus`, mais le champ qualifie la **preuve par
extrait d'une ligne**, pas le poids — il s'appelle donc `snippet_status`.
`direct_anchor_count` compte des occurrences d'ancrage directes du nom,
rien de plus. Graphies en snake_case, comme `occurrence_count` et
`entity_id` qui les entourent. Les candidats `anchorWeightV1` (promet un
poids officiel qu'on ne décrète pas) et `sectionLocalRank` (un rang est un
choix d'affichage, pas une donnée) mentiraient sur leur contenu. Limite
assumée : les champs ne sont documentés que dans le script, cet audit et le
CSV — pas dans le JSON lui-même, car une clé `_meta` dans
`section_entities_map.json` deviendrait une fausse section pour le lecteur
(`Object.keys` y compte ses sections).

## 4. Ce qui est appliqué — et ce qui ne l'est pas

**Appliqué** : les deux champs sur chacune des 12 374 lignes de
`section_entities_map.json`. `occurrence_count` est **intact partout**
(vérifié). Aucun graphe touché — la dette vit dans la carte ; un
`patch_20`/v111 l'aurait **importée dans le graphe** au lieu de la réparer,
c'est le motif de l'absence de patch de graphe. Le script est idempotent et
porte un `--check` (rejouer sans `--apply` compare) — **appelé par la CI** depuis ce chantier, pour que les champs ne puissent pas périmer en silence.

**Non appliqué, délibérément** : tout changement de classement. Le lecteur
affiche aujourd'hui la même chose qu'hier. Basculer le tri — vers
`direct_anchor_count`, vers un filtre `self` d'abord, ou vers la voie A
complète — est un **choix éditorial de l'auteur**, désormais instruit par
des chiffres au lieu d'une intuition.

## 5. La règle de mesure, écrite pour être attaquée

`direct_anchor_count` = occurrences du **nom littéral** de l'entité,
normalisé (casse, accents, apostrophes), en **limites de mots**, dans le
**corps du bloc de la section plus les définitions des notes qui y sont
appelées** (les notes vivent en bloc terminal — les inclure en bloc
compterait celles des autres sections, les exclure amputerait l'appareil).
Divergence assumée avec la règle historique § 1.3 (sous-chaîne) : la
sous-chaîne comptait « Mist » dans « administration ». Conséquence à ne pas
oublier en lecture : un nom que la thèse n'écrit jamais tel quel
(`InfrastructureEvent — …`, libellés bilingues) compte 0 **sans que l'objet
soit absent** — c'est ce que `snippet_status` existe pour distinguer.

## 6. Risques restants

- `direct_anchor_count` sous-compte les entités aux noms forgés ou traduits ;
  il ne doit jamais être lu seul, toujours avec `snippet_status` — et
  réciproquement. Les entités analytiquement centrales aux noms jamais
  écrits tels quels (« Proposition de Soft Fork — The DAO (abandon) »,
  l'appareil `Quote —` du chapitre III, la grappe carnavalesque)
  tomberaient à zéro sous tout classement naïf par cette mesure : c'est
  l'argument chiffré CONTRE un tel basculement, pas un dommage de ce
  chantier (aucun classement ne change).
- Les 918 lignes `no-snippet` ne sont invérifiables que PAR EXTRAIT :
  576 d'entre elles ont une présence textuelle mesurée.
- `null` (plage non dérivable : glossaire, 99 lignes) n'est PAS 0 : un
  tiers qui confond les deux raye le glossaire.
- Une occurrence située dans une sous-section compte dans le
  `direct_anchor_count` de sa parente ET de la sous-section — cohérent avec
  l'agrégation du lecteur, à savoir en lisant.
- La carte des poids doit être **régénérée** si les MD, la carte des titres
  ou les noms d'entités changent (`--check` le détecte).
- Le partage de signature (571 entités) est une preuve de mandat plus forte
  que le test par extrait ; le CSV permet de croiser les deux.

## 7. Décisions réservées à Maël

1. **Le classement du panneau** : garder l'actuel, filtrer `self` d'abord,
   basculer sur `direct_anchor_count`, ou voie A complète — avec le § 2 comme
   étude d'impact.
2. Le sort des **9 899 lignes `proxy`** : les garder comme contexte
   assumé (elles disent « cette section parle de Bitcoin ») ou les purger.
3. Les **918 `no-snippet`**.
4. L'affichage éventuel du statut dans le lecteur (badge « vérifié » ?).
