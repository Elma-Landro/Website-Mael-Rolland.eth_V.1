# Panel Policy Lab v1 — cinq politiques d'affichage, mesurées, aucune choisie

**Date** : 2026-08-07
**Graphe** : `grc20-these-mael-rolland-v110.json` (inchangé par ce chantier)
**Branche** : `claude/file-upload-branch-check-jw4cng`
**Mode agent** : A (comparatif) — aucun classement public modifié
**Outil** : `scripts/compare_panel_policies.py` · **Données** : `docs/audits/data/panel-policy-impact-v110.csv` (270 lignes : 54 sections × 5 politiques), `docs/audits/data/poids-ancrage-diagnostic-v110.csv` (12 374 lignes)
**Prédécesseur** : `grc20-poids-ancrage-v2.md` (2026-08-07)

---

## 1. Le problème, en une page

Le panneau de chaque section du lecteur (`lecteur.html`) affiche un top-12
d'entités classées par `occurrence_count` × log(N/df), épinglées de
`section_overrides.json` d'abord. Or `occurrence_count` est, pour l'essentiel,
un **compte de mandat** : le diagnostic ligne à ligne de la PR #110
(`poids-ancrage-diagnostic-v110.csv`) classe **9 899 lignes sur 12 374
(80,0 %) en `proxy`** — des extraits existent, mais ni le nom de l'entité ni
sa base de citation n'y figurent. S'y ajoutent 1 121 lignes `self`, 436
`self-base` et 918 `no-snippet` (dont **576 ont pourtant
`direct_anchor_count` ≥ 1** : la catégorie n'est pas homogène). Les 54
panneaux du lecteur sont affectés, sans exception.

La PR #110 a doté chaque ligne de la carte des deux champs qui permettent
d'en juger (`snippet_status`, `direct_anchor_count`) — mais elle n'a rien
changé à l'affichage, en renvoyant explicitement le choix du classement à
l'auteur (v2 § 7.1). Le présent chantier instruit ce choix : il **simule**
cinq politiques d'affichage possibles, mesure ce que chacune ferait au
top-12 de chaque section par rapport à la politique en vigueur, et consigne
les résultats. Il ne choisit **aucune** politique, ne modifie aucun
classement public, ne touche ni la carte ni le graphe.

## 2. Les cinq politiques, définies précisément

Les définitions normatives sont celles du script
`scripts/compare_panel_policies.py`. Invariants communs : les **épinglés**
de `section_overrides.json` viennent toujours en tête, hors classement ;
toutes les égalités sont cassées par `entity_id` croissant (convention du
dépôt, cf. `build_anchor_weights.py --impact`) ; « score legacy » désigne
`occurrence_count` × log(N/df), N = 54 clés de la carte.

| Politique | Définition | Nature |
|---|---|---|
| `legacy` | épinglés, puis score legacy décroissant | l'affichage actuel — sert de référence |
| `diagnostic-only` | ordre strictement identique à `legacy` ; les badges de statut sont une affaire d'interface | témoin — survie 100 % par construction |
| `verified-first` | épinglés ; puis les lignes `snippet_status` ∈ {`self`, `self-base`} par score legacy ; puis toutes les autres par score legacy | pur réordonnancement, personne n'est exclu |
| `direct-count` | épinglés ; puis les lignes `direct_anchor_count` ≥ 1 triées par `direct` × log(N/dfd) (dfd = nombre de sections où l'entité a `direct` ≥ 1) ; puis **fallback** des restantes (`direct` 0 ou `null`) par score legacy — le panneau ne se vide jamais | classement par mesure, filet legacy |
| `hybrid-cautious` | épinglés ; puis classe de statut croissante (`self` = 0, `self-base` = 1, `proxy` = 2, `no-snippet` = 3), à l'intérieur d'une classe par score legacy | réordonnancement par strates, personne n'est exclu |

Une sixième variante sert d'auto-contrôle, hors CSV : **direct strict**
(candidats mesurés seuls, sans fallback) — c'est la formule de
`build_anchor_weights.py --impact`, et le script vérifie à chaque exécution
qu'il en reproduit exactement le chiffre.

## 3. Matrice comparative

Survie = places du top-12 actuel conservées, sur les 648 places des 54
panneaux (source : `panel-policy-impact-v110.csv`, colonne
`survivors_vs_legacy`, sommée ; sections et types : synthèse du script).

| Politique | Survie /648 | Sections vidées ou quasi vidées (survivants) | Types pénalisés (top 5, places perdues) | Risque d'interprétation principal |
|---|---:|---|---|---|
| `legacy` | 648 (100 %) | — | — | maintient un classement dont 80 % des lignes sont des mandats non signalés |
| `diagnostic-only` | 648 (100 %) | — | — | un badge « vérifié » peut être lu comme une validation scientifique (§ 4.d) |
| `verified-first` | 443 (68 %) | intro_D (1), I.2 (2), I.3.2 (2), III.1 (2), II.2 (3), III.1.2 (3), conclu_resume (3), I.2.2 (4) | Reference 102, Concept 35, Protocol 14, Person 9, InfrastructureEvent 6 | le lecteur peut croire que l'ordre reflète l'importance, alors qu'il reflète la preuve par extrait |
| `direct-count` | 364 (56 %) | I.3.3 (0), I.3.2 (2), III.1.2 (2), I.2.2 (3), II.2.1 (3), II.4 (3), III.1.1 (3), conclu_resume (3) | Reference 191, Concept 37, InfrastructureEvent 6, SourceQuote 5, CrisisEvent 5 | `direct_anchor_count` est une mesure pauvre (§ 4.a) érigée en critère principal |
| `hybrid-cautious` | 337 (52 %) | I.2 (0), I.3 (0), I.3.3 (0), II.3 (0), intro_D (1), I.3.2 (2), III.1 (2), III.1.2 (2) | Reference 181, Concept 50, Protocol 18, Person 9, CrisisEvent 6 | des panneaux remplis mais méconnaissables (§ 4.b) |
| *direct strict* (repère hors CSV) | *294 (45 %)* | *viderait glossaire_preamble, amputerait conclu_traduction et intro_E (§ 3.1)* | *non mesuré ici* | *seul cas où des panneaux se vident réellement* |

Le repère *direct strict* reproduit exactement le chiffre de
`build_anchor_weights.py --impact` (auto-contrôle imprimé par le script à
chaque exécution) — les deux outils se valident l'un l'autre.

### 3.1 Sections pauvres en candidats mesurés

Trois sections ont moins de 3 lignes à `direct_anchor_count` ≥ 1 (colonne
`measured_candidates` du CSV) : **glossaire_preamble (0** — sa plage de
texte n'est pas dérivable, `direct` est `null` partout —**),
conclu_traduction (2), intro_E (2)**. Sous `direct-count`, le fallback
legacy les remplit ; la variante stricte les vidait. C'est la raison d'être
du fallback, pas un détail d'implémentation.

## 4. Lectures et risques

**(a) Les Reference dominent les pertes partout — mais la mesure qui les
sanctionne est pauvre.** Sous les trois politiques qui réordonnent, le type
qui perd le plus de places est `Reference` (191 sous `direct-count`, 181
sous `hybrid-cautious`, 102 sous `verified-first`), suivi de `Concept`.
C'est cohérent avec le gonflement mandataire établi par les audits
précédents : les références héritent d'occurrences qui comptent la section,
pas elles. **Mais** une Reference peut être analytiquement centrale sans que
son nom littéral figure dans le texte de la section : `direct_anchor_count`
compte le nom exact en limites de mots (v2 § 5), donc les noms forgés, les
libellés bilingues et l'appareil « Quote — » du chapitre III comptent 0
**sans être absents**. Une perte de place n'est pas une preuve de
non-pertinence ; c'est une absence de preuve littérale.

**(b) `hybrid-cautious` vide quatre panneaux de leur top-12 actuel sans
exclure personne.** I.2, I.3, I.3.3 et II.3 tombent à 0 survivant (et
intro_D à 1) alors que la politique est un pur réordonnancement : personne
n'est filtré. Le mécanisme : le tri par classe de statut fait passer
**toutes** les lignes `self` et `self-base` — y compris celles au score
legacy modeste — devant **toutes** les lignes `proxy`, où vit l'essentiel du
top-12 actuel. Le panneau reste rempli à 12, mais par des entités que le
lecteur d'aujourd'hui n'y voit pas : rempli, donc, mais méconnaissable.
Quiconque compare l'avant et l'après sur ces quatre sections verra un
changement aussi violent qu'un remplacement de classement, sans qu'aucune
entité n'ait été « supprimée ».

**(c) Aucun de ces classements n'est une mesure d'importance analytique.**
`legacy` classe des mandats ; `verified-first` et `hybrid-cautious` classent
une preuve par extrait ; `direct-count` classe une présence littérale. Rien
dans ces données ne dit quelle entité est importante pour l'argument de la
section — c'est la limite déjà déclarée en v2 (§ 3, « ne pas inventer de
score scientifique »), et elle vaut pour les cinq politiques.

**(d) Le badge « vérifié » de `diagnostic-only` n'est pas neutre non
plus.** `snippet_status` atteste qu'un extrait de la carte contient le nom
ou sa base de citation — rien de plus. Affiché tel quel, un badge
« vérifié » risquerait de passer pour une validation scientifique de
l'entité ou de son rattachement. Si cette voie est retenue, la formulation
d'interface devra dire ce que le champ mesure (« nom attesté dans un
extrait »), pas ce qu'il ne mesure pas.

## 5. Ce que les chiffres permettent de dire — et ce qu'ils ne permettent pas

**Permis par les données :**

- `diagnostic-only` est sans risque pour l'affichage : survie 648/648 par
  construction, aucun réordonnancement — seul le risque de formulation du
  badge (§ 4.d) subsiste, et il est d'interface, pas de données.
- Parmi les réordonnancements, `verified-first` est le moins destructif
  mesuré : 443/648 (68 %), aucune section sous 1 survivant, et les pertes
  par type sont environ moitié de celles de `direct-count`.
- `direct-count` (364/648) et `hybrid-cautious` (337/648) transforment
  fortement plusieurs panneaux — jusqu'à 0 survivant sur I.3.3
  (`direct-count`) et sur I.2, I.3, I.3.3, II.3 (`hybrid-cautious`). Un
  basculement vers l'une ou l'autre exigerait une **relecture par panneau**
  des sections listées en § 3, précisément parce que la mesure qui pilote le
  changement est pauvre (§ 4.a).
- Le fallback de `direct-count` est nécessaire : sans lui, trois sections
  n'ont pas de quoi remplir un panneau (§ 3.1).

**Non permis par les données :** dire quelle politique est la bonne. Les
cinq classements mesurent des choses différentes (mandat, preuve par
extrait, présence littérale) et aucune n'est l'importance analytique.
Choisir, c'est décider ce que le panneau **doit** montrer au lecteur — une
décision éditoriale d'auteur, pas une conclusion de mesure. Ce document
n'en formule aucune.

## 6. Décisions réservées à Maël

1. **La politique d'affichage** : conserver `legacy`, passer à
   `diagnostic-only`, `verified-first`, `direct-count` ou `hybrid-cautious`
   — avec la matrice du § 3 comme étude d'impact.
2. En cas de bascule vers `direct-count` ou `hybrid-cautious` : la
   **relecture panneau par panneau** des sections listées en § 3 (0 à 3
   survivants), avant toute mise en ligne.
3. En cas de badge (`diagnostic-only` ou combiné) : la **formulation
   d'interface** du statut, pour qu'elle ne passe pas pour une validation
   scientifique (§ 4.d).
4. Le sort des trois sections pauvres en candidats mesurés
   (glossaire_preamble, conclu_traduction, intro_E) si une politique fondée
   sur `direct_anchor_count` est retenue.
5. L'opportunité de **combiner** les politiques (par exemple badges +
   réordonnancement) — combinaison non simulée ici.

**Ce que ce chantier n'a pas fait** : aucun changement de classement public
(`lecteur.html` affiche aujourd'hui la même chose qu'hier), aucun graphe
touché, pas de v111, aucune modification de la carte, des overrides ni
d'aucun fichier existant. Le script est une simulation déterministe,
rejouable, dont la seule écriture est le CSV d'impact.
