# Panel Policy Lab v1 — cinq politiques d'affichage, mesurées, aucune choisie

**Date** : 2026-08-07 (révisé le 2026-08-07 après revue hostile — voir § 0)
**Graphe** : `grc20-these-mael-rolland-v110.json` (inchangé par ce chantier)
**Branche** : `claude/file-upload-branch-check-jw4cng`
**Mode agent** : A (comparatif) — aucun classement public modifié
**Outil** : `scripts/compare_panel_policies.py` · **Données** : `docs/audits/data/panel-policy-impact-v110.csv` (275 lignes : 55 panneaux × 5 politiques), `docs/audits/data/poids-ancrage-diagnostic-v110.csv` (12 374 lignes)
**Prédécesseur** : `grc20-poids-ancrage-v2.md` (2026-08-07)

---

## 0. Révision — la première baseline ne simulait pas le site

La première version de ce document simulait les panneaux sur les **lignes
brutes** de `section_entities_map.json`, avec bris d'égalité par `entity_id`
partout, y compris pour `legacy`. La revue hostile a montré que ce n'était
**pas l'affichage réel** : `lecteur.html` (1) **agrège les sections
parentes** — les dix clés `I.1` … `III.3` et `conclu_theo`, en sommant les
`occurrence_count` de leurs descendantes et en recalculant leur TF-IDF sur
le df brut — et (2) trie **sans bris d'égalité** : le tri de JavaScript est
stable, les ex æquo gardent l'ordre de construction de la liste.
Contre-exemple mesuré : sur `I.2` (parente agrégée), `hybrid-cautious`
conserve réellement **7 places sur 12**, là où la première version
annonçait 0. Au total, sur les 54 clés brutes, l'ancien top-12 « legacy »
différait de l'affichage réel en **ordre sur 48 sections** et en
**composition sur 30** — et le panneau agrégé `conclu_theo` (433 entités,
clé absente de la carte brute) manquait entièrement au CSV.

La présente version simule le **pipeline exact du lecteur**
(`loadGraph()` : df/dfd/TF-IDF sur lignes brutes, puis agrégation des
parentes ; `updateGraph()` : épinglés, tri, troncature à 12) et a été
**validée contre le navigateur** (Chromium, bibliothèques servies
localement) sur 4 sections — 2 parentes agrégées (`I.2`, `conclu_theo`) et
2 brutes (`II.2.1`, `I.3.3`) : top-12 `legacy` sans `?panelLab` identique
liste à liste à la simulation, panneaux `verified-first` et
`hybrid-cautious` sous `?panelLab=1` identiques, à une exception près
déclarée en § 5 (ex æquo flottant inter-langages, rangs 11-12 de
`II.2.1`). Les chiffres de la première version ne sont **plus courants
nulle part** ; ceux qui suivent sont les seuls valides. La révision a aussi
aligné le rang du statut inconnu (`?? 4` partout, fusion et comparateur —
l'incohérence était latente : les 12 374 lignes portent toutes un statut)
et neutralisé les couleurs des badges du mode laboratoire (§ 4.d).

## 1. Le problème, en une page

Le panneau de chaque section du lecteur (`lecteur.html`) affiche un top-12
d'entités classées par `occurrence_count` × log(N/df), épinglées de
`section_overrides.json` d'abord. Le lecteur affiche **55 panneaux** : les
54 clés brutes de la carte, plus la parente `conclu_theo` reconstituée par
agrégation (les neuf autres parentes — `I.1` … `III.3` — existent comme
clés brutes mais sont **remplacées** au chargement par leur agrégat, qui
somme les occurrences de leurs descendantes). Or `occurrence_count` est,
pour l'essentiel, un **compte de mandat** : le diagnostic ligne à ligne de
la PR #110 (`poids-ancrage-diagnostic-v110.csv`) classe **9 899 lignes sur
12 374 (80,0 %) en `proxy`** — des extraits existent, mais ni le nom de
l'entité ni sa base de citation n'y figurent. S'y ajoutent 1 121 lignes
`self`, 436 `self-base` et 918 `no-snippet` (dont **576 ont pourtant
`direct_anchor_count` ≥ 1** : la catégorie n'est pas homogène). Les 55
panneaux du lecteur sont affectés, sans exception.

La PR #110 a doté chaque ligne de la carte des deux champs qui permettent
d'en juger (`snippet_status`, `direct_anchor_count`) — mais elle n'a rien
changé à l'affichage, en renvoyant explicitement le choix du classement à
l'auteur (v2 § 7.1). Le présent chantier instruit ce choix : il **simule**
cinq politiques d'affichage possibles, mesure ce que chacune ferait au
top-12 de chaque panneau par rapport à la politique en vigueur, et consigne
les résultats. Il ne choisit **aucune** politique, ne modifie aucun
classement public, ne touche ni la carte ni le graphe.

## 2. Les cinq politiques, définies précisément

Les définitions normatives sont celles du script
`scripts/compare_panel_policies.py`, qui reproduit le pipeline du lecteur.
Invariants communs : les **épinglés** de `section_overrides.json` viennent
toujours en tête, hors classement ; **l'agrégation des parentes fait partie
de la baseline** (elle a lieu avant tout classement, pour les cinq
politiques) ; « score legacy » désigne `occurrence_count` × log(N/df),
N = 54 clés **brutes** de la carte (df et dfd sont comptés sur les lignes
brutes, avant agrégation — comme dans le lecteur) ; pour les parentes, le
score est recalculé après agrégation sur l'`occurrence_count` sommé, avec
le df brut.

Le bris d'égalité, lui, n'est **pas** un invariant commun : `legacy` — le
lecteur réel — trie **sans bris d'égalité** (tri stable de JavaScript,
reproduit par le tri stable de Python sur le même ordre de construction) ;
seuls les modes **expérimentaux** (`verified-first`, `direct-count`,
`hybrid-cautious`, comparateurs de `panelLabComparateur` dans
`lecteur.html`) cassent les égalités par `entity_id` croissant.

| Politique | Définition | Nature |
|---|---|---|
| `legacy` | épinglés, puis score legacy décroissant, tri stable sans bris d'égalité | l'affichage actuel — sert de référence |
| `diagnostic-only` | ordre strictement identique à `legacy` ; les badges de statut sont une affaire d'interface | témoin — survie 100 % par construction |
| `verified-first` | épinglés ; puis les lignes `snippet_status` ∈ {`self`, `self-base`} par score legacy ; puis toutes les autres par score legacy | pur réordonnancement, personne n'est exclu |
| `direct-count` | épinglés ; puis les lignes `direct_anchor_count` ≥ 1 triées par `direct` × log(N/dfd) (dfd = nombre de sections brutes où l'entité a `direct` ≥ 1) ; puis **fallback** des restantes (`direct` 0 ou `null`) par score legacy — le panneau ne se vide jamais | classement par mesure, filet legacy |
| `hybrid-cautious` | épinglés ; puis classe de statut croissante (`self` = 0, `self-base` = 1, `proxy` = 2, `no-snippet` = 3, inconnu = 4), à l'intérieur d'une classe par score legacy | réordonnancement par strates, personne n'est exclu |

Sur les panneaux agrégés, les champs de qualification sont fusionnés comme
dans le lecteur (`panelLabFusionneLigne`) : somme des
`direct_anchor_count` non `null`, meilleur `snippet_status` retenu.

Une sixième variante sert d'auto-contrôle, hors CSV : **direct strict**
(candidats mesurés seuls, sans fallback, sur les **lignes brutes** avec
bris `entity_id`) — c'est la formule de `build_anchor_weights.py --impact`,
et le script vérifie à chaque exécution qu'il en reproduit exactement le
chiffre (294/648). Cet auto-contrôle valide la **formule** TF-IDF partagée
entre les deux scripts, **pas** la baseline lecteur — il est étiqueté comme
tel dans la sortie.

## 3. Matrice comparative

Survie = places du top-12 actuel conservées, sur les **660 places des 55
panneaux** (source : `panel-policy-impact-v110.csv`, colonne
`survivors_vs_legacy`, sommée ; sections et types : synthèse du script).

| Politique | Survie /660 | Sections vidées ou quasi vidées (survivants ≤ 3) | Types pénalisés (top 5, places perdues) | Risque d'interprétation principal |
|---|---:|---|---|---|
| `legacy` | 660 (100 %) | — | — | maintient un classement dont 80 % des lignes sont des mandats non signalés |
| `diagnostic-only` | 660 (100 %) | — | — | un badge « vérifié » peut être lu comme une validation scientifique (§ 4.d) |
| `verified-first` | 477 (72 %) | intro_D (1), I.3.2 (2), III.1.2 (3), conclu_resume (3) | Reference 96, Concept 33, CrisisEvent 18, Protocol 10, SourceQuote 10 | le lecteur peut croire que l'ordre reflète l'importance, alors qu'il reflète la preuve par extrait |
| `hybrid-cautious` | 372 (56 %) | I.3.3 (0), intro_D (1), I.3.2 (2), III.1.2 (2), III.1.1 (3), conclu_resume (3) | Reference 198, Concept 33, CrisisEvent 18, Protocol 10, SourceQuote 10 | des panneaux transformés sans qu'aucune entité soit exclue (§ 4.b) |
| `direct-count` | 352 (53 %) | I.3.3 (0), I.3.2 (2), III.1.2 (2), II.2.2 (3), II.4 (3), III.1.1 (3), conclu_resume (3) | Reference 205, Concept 43, CrisisEvent 18, SourceQuote 10, PrimarySource 5 | `direct_anchor_count` est une mesure pauvre (§ 4.a) érigée en critère principal |
| *direct strict* (repère hors CSV, lignes brutes) | *294/648 (45 %)* | *viderait glossaire_preamble, amputerait conclu_traduction et intro_E (§ 3.1)* | *non mesuré ici* | *seul cas où des panneaux se vident réellement* |

Le repère *direct strict* reproduit exactement le chiffre de
`build_anchor_weights.py --impact` (auto-contrôle imprimé par le script à
chaque exécution) — les deux outils se valident l'un l'autre sur la
formule ; sa base (648 places, 54 clés brutes) n'est **pas** comparable
ligne à ligne aux 660 places de la simulation lecteur.

Sur la baseline fidèle, l'ordre des politiques change par rapport à la
première version : `hybrid-cautious` (372) passe **devant** `direct-count`
(352), et toutes les survies remontent — l'agrégation des parentes stabilise
les panneaux de niveau 2, où les entités à forte présence textuelle cumulée
dominent déjà le classement legacy. Les dix panneaux agrégés survivent entre
4/12 (`I.3`, `II.1`, `II.2` sous `direct-count` ou `hybrid-cautious`) et
12/12 (`III.3` sous `verified-first`) — aucun ne tombe à 0.

### 3.1 Sections pauvres en candidats mesurés

Trois sections ont moins de 3 lignes à `direct_anchor_count` ≥ 1 (colonne
`measured_candidates` du CSV) : **glossaire_preamble (0** — sa plage de
texte n'est pas dérivable, `direct` est `null` partout —**),
conclu_traduction (2), intro_E (2)**. Le panneau agrégé `conclu_theo` n'a
que 6 candidats mesurés (hérités de `conclu_theo_mon`, sa seule
contributrice). Sous `direct-count`, le fallback legacy remplit ces
panneaux ; la variante stricte les vidait. C'est la raison d'être du
fallback, pas un détail d'implémentation.

## 4. Lectures et risques

**(a) Les Reference dominent les pertes partout — mais la mesure qui les
sanctionne est pauvre.** Sous les trois politiques qui réordonnent, le type
qui perd le plus de places est `Reference` (205 sous `direct-count`, 198
sous `hybrid-cautious`, 96 sous `verified-first`), suivi de `Concept` puis
`CrisisEvent` (18 sous les trois politiques). C'est cohérent avec le
gonflement mandataire établi par les audits précédents : les références
héritent d'occurrences qui comptent la section, pas elles. **Mais** une
Reference peut être analytiquement centrale sans que son nom littéral
figure dans le texte de la section : `direct_anchor_count` compte le nom
exact en limites de mots (v2 § 5), donc les noms forgés, les libellés
bilingues et l'appareil « Quote — » du chapitre III comptent 0 **sans être
absents**. Une perte de place n'est pas une preuve de non-pertinence ;
c'est une absence de preuve littérale.

**(b) `hybrid-cautious` ne vide plus les panneaux que la première version
disait vidés — mais un panneau tombe bien à 0.** La baseline fidèle
contredit le § 4.b initial : `I.2`, `I.3` et `II.3`, annoncés à 0
survivant, conservent réellement 7, 4 et 7 places sur 12 — parce que ce
sont des parentes agrégées, dont le top-12 réel est dominé par des entités
au statut mesurable une fois les descendantes cumulées. Ce qui reste vrai :
**`I.3.3` (clé brute) tombe à 0 survivant** sous `hybrid-cautious` comme
sous `direct-count`, et `intro_D` à 1 sous `hybrid-cautious` et
`verified-first`, alors que ces politiques n'excluent personne. Le
mécanisme est inchangé : le tri par classe de statut fait passer **toutes**
les lignes `self` et `self-base` — y compris celles au score legacy
modeste — devant **toutes** les lignes `proxy`, où vit l'essentiel du
top-12 actuel. Le panneau reste rempli à 12, mais par des entités que le
lecteur d'aujourd'hui n'y voit pas : rempli, donc, mais méconnaissable —
le phénomène est simplement moins étendu que la simulation sur lignes
brutes le laissait croire.

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
l'entité ou de son rattachement. La révision a appliqué ce principe au mode
laboratoire lui-même : les badges `self`/`no-snippet` étaient colorés en
vert succès / rouge danger, ce qui constituait exactement la validation
visuelle que ce paragraphe proscrit (576 des 918 `no-snippet` ont une
présence textuelle mesurée) — la palette est désormais neutre (ors et
orangés du thème, bordure pointillée pour `no-snippet`), distincte mais
sans sémantique de jugement. Si une voie à badges est retenue pour
l'affichage public, la formulation d'interface devra dire ce que le champ
mesure (« nom attesté dans un extrait »), pas ce qu'il ne mesure pas.

## 5. Ce que les chiffres permettent de dire — et ce qu'ils ne permettent pas

**Permis par les données :**

- `diagnostic-only` est sans risque pour l'affichage : survie 660/660 par
  construction, aucun réordonnancement — seul le risque de formulation du
  badge (§ 4.d) subsiste, et il est d'interface, pas de données.
- Parmi les réordonnancements, `verified-first` est le moins destructif
  mesuré : 477/660 (72 %), aucune section sous 1 survivant, et les pertes
  par type sont environ moitié de celles de `direct-count`.
- `hybrid-cautious` (372/660) et `direct-count` (352/660) transforment
  fortement plusieurs panneaux — jusqu'à 0 survivant sur `I.3.3` (les
  deux politiques). Un basculement vers l'une ou l'autre exigerait une
  **relecture par panneau** des sections listées en § 3 (≤ 3 survivants),
  précisément parce que la mesure qui pilote le changement est pauvre
  (§ 4.a).
- Le fallback de `direct-count` est nécessaire : sans lui, trois sections
  n'ont pas de quoi remplir un panneau (§ 3.1).

**Limites de la simulation :**

- **Ex æquo flottants inter-langages.** Python et V8 peuvent arrondir
  `log` différemment au dernier ulp : deux scores exactement égaux côté
  Python peuvent différer de ~4 × 10⁻¹⁶ côté navigateur, et
  réciproquement. Cas observé et vérifié lors de la validation croisée :
  rangs 11-12 de `II.2.1` sous `verified-first` (scores 2.1972245773362196
  vs 2.197224577336219 dans V8, exactement égaux en Python — l'égalité
  tient à 4,4 × 10⁻¹⁶ près, l'ordre des deux entités s'inverse). La
  composition des panneaux n'en est affectée que si l'ex æquo chevauche la
  coupe du top-12 ; aucun autre écart n'a été observé sur les 4 sections ×
  3 politiques validées au navigateur.
- **Le CSV pris seul ne porte pas les mises en garde.** Les colonnes
  `measured_candidates` et les survies par politique ne disent ni que
  `direct_anchor_count` est une mesure pauvre, ni que `snippet_status`
  n'est pas un certificat, ni ce que la baseline simule exactement — ces
  réserves vivent dans le présent document (§ 2, § 4) et dans
  `docs/audits/data/README.md`. Ne pas citer le CSV sans elles.

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
(`lecteur.html` sans paramètre affiche aujourd'hui la même chose qu'hier —
prouvé par comparaison navigateur des ordres de panneau avant/après sur
`I.2` et `II.2.1`, identiques au commit précédent), aucun graphe touché,
pas de v111, aucune modification de la carte ni des overrides. Les
modifications de `lecteur.html` se limitent au mode laboratoire opt-in
(`?panelLab=1`), inerte par défaut : alignement du rang du statut inconnu
(`?? 4`) et neutralisation des couleurs de badges (§ 4.d). Le script est
une simulation déterministe, rejouable (deux exécutions produisent un CSV
identique), dont la seule écriture est le CSV d'impact — nommé d'après la
version du graphe détecté (`panel-policy-impact-v110.csv` pour v110), pour
qu'une future v111 n'écrase pas silencieusement les données v110.
