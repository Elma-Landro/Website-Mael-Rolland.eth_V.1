# Voie C — chaque charge d'ancrage rendue à la section dont elle décrit le texte

**Date** : 2026-08-06
**Graphe** : `grc20-these-mael-rolland-v108.json` → **`v109`** (oracle : v107)
**Branche** : `claude/file-upload-branch-check-jw4cng`
**Mode agent** : C — appliqué, sur arbitrage rendu par l'auteur (« c »)
**Script** : `scripts/make_v109_realign_anchoring_charges.py`

---

## Le constat, vérifié deux fois

Les listes d'ancrage décrivent des **plages de texte**, pas des nœuds. En
localisant les 20 056 extraits de `entity_section_map.json` ligne à ligne dans
`assets/MD/`, **18 clés se révèlent décalées d'un cran, en correspondance
une-pour-une** : la liste rangée sous `II.2.2.c` décrit à 100 % le bloc
`II.2.3` ; sous `I.2.2`, le bloc `I.2.1` ; sous `II.3.2`, le bloc `II.3.3`.
Sept cas sur huit vérifiés à 100 %, le huitième (`III.2.1`) à 99,6 % en
localisation fine.

**Corollaire : les 8 entrées du sommaire réputées vides ne l'étaient pas.**
Leur contenu existait, sous la clé de la voisine :

| entrée « vide » | sa charge vivait sous | lignes |
|---|---|---:|
| `II.2.3` | `II.2.2.c` | 458 |
| `II.1.2` | `II.1.1.b` | 399 |
| `II.2.1` | `II.2.2.a` | 318 |
| `I.2.1` | `I.2.2` | 265 |
| `II.3.3` | `II.3.2` | 186 |
| `III.2.3` | `III.2.1` | 162 |
| `I.1.3` | `I.1.2` | 75 |
| `III.2.2` | `III.1.2.b` | 17 |

## La cause — et elle est à l'outillage de migration, pas aux données d'origine

Avant v100/v106, ces clés étaient **justes** : la clé `II.2.3` couvrait le
bloc II.2.3. C'est le **nœud** qui était faux — il portait un titre de
niveau 3. Les migrations ont renommé les nœuds d'après leur titre (décision
défendable, conservée), et `remap_section_keys.py` **a fait suivre les
listes**. C'était l'erreur : une charge décrit un texte, elle n'avait pas à
suivre le renommage d'un nœud.

**v108 a aggravé la chose sans le savoir.** Il a réaligné l'attribut
`section_key` des relations sur la clé de leur cible — donc écrasé la seule
trace restante de la vérité : l'attribut nommait le bloc réel, c'était la
cible qui était fausse. v107 a servi d'oracle pour la retrouver ; la
bijection des 18 clés rendait de toute façon l'opération réversible.

## Ce que v109 fait

En une passe **simultanée** (5 des 18 clés sont à la fois source et cible) :

1. **3 970 relations `appears in section` rebranchées** vers le nœud qui porte
   la clé du bloc que leur attribut v107 nommait. Garde-fou : tout écart ne
   suivant pas la bijection aurait fait échouer le script — il y en a eu zéro.
2. **Les deux cartes réalignées** : 18 clés dans `section_entities_map.json`,
   7 132 enregistrements dans `entity_section_map.json`.
3. L'attribut des relations redevient exact **et** égal à la clé de la cible —
   les trois emplacements d'une clé de section disent enfin la même chose.

Ce que v109 **ne fait pas** : aucun poids recalculé. La question du poids
mandataire (66 % des entités portent les occurrences d'un mot qui n'est pas le
leur — voie A) reste entière, et se posera désormais sur des plages justes.

## Résultat, vérifié en navigateur

```
graphe.html   48 entrées de sommaire, 48 comptes — AUCUNE vide
              (première fois dans l'histoire du dépôt)
              I.1.3 (75) · I.2.1 (273) · II.1.2 (404) · II.2.1 (318)
              II.2.3 (463) · II.3.3 (187) · III.2.2 (17) · III.2.3 (165)
lecteur.html  II.2.3 : top 12/458 · I.2.1 : top 12/265 · aucune pageerror
CI            4 étapes vertes · baseline 46 codes, aucune régression
```

La baseline échange 14 codes : sortent les 8 entrées du sommaire (réellement
corrigées) et 6 autres ; entrent les 14 nœuds de rang subordonné (`I.1.1.a`,
`II.2.2.c`…) qui ont rendu leur charge au bloc `##`. Ils n'ont jamais eu de
charge propre mesurée, ne figurent pas au sommaire, et leur texte est un
sous-ensemble du bloc parent désormais correctement doté.

## Corrections à deux audits antérieurs — mes propres affirmations

1. `docs/audits/grc20-ancrage-poids-mandataires-v1.md` § 6 affirmait : *« le
   contenu ne vit pas dans leurs sous-parties […] le vide est bien un défaut
   d'outillage »*. **Faux sur le premier point** : le contenu vivait sous la
   clé de la voisine, déplacé par mon propre remappage. La conclusion
   pratique (défaut d'outillage) était juste, le diagnostic de localisation
   ne l'était pas.
2. Le message de v106 affirmait que les 11 sections créées n'avaient « pas de
   liste d'entités ». Exact au sens littéral, mais la liste existait — sous
   l'ancienne clé. L'échange « erreur silencieuse contre trou visible » était
   en réalité un déplacement de charge, pas un trou.

## Ce qui reste ouvert

- **Le poids mandataire** (voie A) : à trancher séparément, désormais sur des
  plages justes. La règle du § 1.3 de l'audit plafonne à 66,7 % de
  reproduction — il lui manque un paramètre pour être rejouable.
- **`headingToSectionKey()` de `lecteur.html`** n'attribue une clé qu'aux
  titres numérotés ; les `##` des chapitres n'en portent pas. Le lecteur
  n'active donc jamais une sous-section de chapitre au défilement — vérifié.
  Défaut indépendant, antérieur, non traité ici.
- Les 745 relations sans attribut v107 (sans provenance connue) : laissées en
  l'état.
- Les 4 clés terminales (`intro_E`, `I.4`, `II.4`, `III.4`) dont la charge est
  à 66–99 % l'appareil de notes du fichier entier.
