# 05 — Synthèse

**Date** : 2026-08-02
**Branche** : `agent/grc20-add-missing-chronology-events-v1`
**Mode agent** : C (patch appliqué à un graphe candidat, non fusionné)

## Le constat principal n'est pas celui qu'on cherchait

Le chantier partait d'un diagnostic visuel : le graphe donne une image trop pauvre des phases « péché » et « maturation ». L'hypothèse était qu'il manquait des événements. **Elle est fausse pour l'essentiel.**

Comptage des arêtes `occurs in` vers les nœuds de phase :

| Cible | Arêtes |
|---|---:|
| `DevelopmentPhase` — Phase de preuve de concept | 64 |
| `DevelopmentPhase` — Phase de péché | 45 |
| `Concept` — Phase de maturation / Phase 3 Bitcoin | 25 |
| **`DevelopmentPhase` — Phase de maturation** | **1** |

Or **le graphe contient déjà 63 événements datés de 2014 ou après** (2014 : 20, 2015 : 11, 2016 : 8, 2017 : 12, 2018 : 6, 2019 : 4), **dont 38 ne sont reliés à aucune phase**.

Deux défauts se cumulent :

1. **La phase de maturation est dédoublée.** Une `DevelopmentPhase` (1 usage) et un `Concept` homonyme (25 usages) se partagent le rôle. Le nœud qui structure la chronologie est le moins utilisé des deux.
2. **38 événements de la période ne sont câblés à aucune phase.** Ils existent, ils sont datés, ils sont simplement invisibles à toute vue organisée par phase.

**Ajouter six nœuds ne corrige pas un déséquilibre de 1 contre 64.** La pauvreté visuelle de la maturation est un problème de câblage et de doublon de vocabulaire, pas un problème de contenu.

À noter au passage : la prémisse ne tient pas pour « péché ». Avec 45 arêtes et 53 événements datés 2012-2013, cette phase est correctement représentée.

**Ce chantier ne corrige pas ce défaut** : relier 38 entités existantes à un nœud de phase, et arbitrer le doublon `DevelopmentPhase`/`Concept`, sont des opérations sur l'existant, d'une autre nature que l'ajout d'événements manquants. Les mélanger dans la même PR serait précisément le mélange de chantiers qu'il fallait éviter. C'est la **recommandation prioritaire** pour la suite, et elle a plus d'effet visuel que tout ce qui suit.

## Ce que cette PR fait

**6 événements ajoutés sur 78 lignes de chronologie examinées.** Le graphe passe de 2 263 à 2 269 entités et de 20 042 à 20 067 relations. `InfrastructureEvent` : 158 → 164. `CrisisEvent` : inchangé.

| id | Événement | Date | Phase | Valeur |
|---|---|---|---|---|
| E069 | PR 9049 : insémination du bogue CVE-2018-17144 | 2016-10 | maturation | **forte** |
| E040 | Publication du WP d'Ethereum (Buterin) | 2013-11 | maturation | **forte** |
| E061 | Testnet Olympic, neuvième itération | 2015-05-09 | maturation | **forte** |
| E060 | Pivot « blockchain sans les UCN » | 2015 | maturation | moyenne |
| E034 | Coinbase : fondation | 2012 | péché | moyenne |
| E036 | Publication de « The Second Bitcoin Whitepaper » | 2012-01 | poc | moyenne |

Cinq des six relèvent des phases prioritaires. E036 est en phase `poc` : ajouté parce qu'il est réellement absent et appuyé par une citation verbatim, en dépit de sa phase.

Chaque entité est câblée : `occurs in` vers sa phase, `belongs to domain` vers un ou deux domaines, `appears in section` vers une ou deux sections avec `section_key` et `page_approx`. S'y ajoutent 2 `source of` depuis les `Reference` des livres blancs, et 2 `precursor of` — dont PR 9049 → CVE-2018-17144.

## Ce que cette PR ne fait pas

- Aucune fusion, aucune suppression, **aucune entité existante modifiée**.
- `patch_10_dedup_events.json` n'est pas appliqué.
- `grc20-these-mael-rolland-v97.json` est intact — vérifié par `git diff`.
- `graphe.html`, `story-presets.mjs`, `narrative-anchors.json` et les assets ne sont pas touchés. Aucune convention du dépôt n'impose de référencer le dernier graphe : `package.json` pointe encore sur v96 et `CLAUDE.md` déclare v96 canonique — deux déclarations déjà périmées avant ce chantier, signalées sans être corrigées ici.
- v98 est un **graphe candidat**. Il n'est publié nulle part.

## Ce que le chantier a appris sur la méthode

**Un appariement lexical seul se serait trompé dans 10 cas sur 12.** Le mécanisme déterministe a produit 12 candidats ; la vérification adverse en a invalidé dix — barrière de langue français/anglais, acronymes développés, variation typographique (« BIP16 » contre « BIP 16 »), et surtout faits portés par un type non événementiel.

Ce dernier mode est le dominant : le graphe possède un type **`PriceWindow`** qui portait déjà quatre des cinq paliers de cours, des `Concept` de régime transactionnel qui portaient les statistiques d'activité illicite, des `Reference` pour les livres blancs, une `Organization` pour Coinbase, un `MediaOutlet` pour Bitcoin Magazine. Et, pour PR 9049, **une simple valeur d'attribut**.

Le mécanisme a été corrigé — il indexe désormais les 2 263 entités tous types confondus, nom et description — mais il reste imparfait, et ses sorties sont conservées **séparément** des verdicts de vérification (`chronology-events-classification.csv` d'un côté, `chronology-events-arbitration.csv` de l'autre). L'ajuster jusqu'à ce qu'il retombe sur les verdicts serait du surajustement.

## Points ouverts — à ne pas trancher par un agent

1. **Le câblage des phases** (voir plus haut) : 38 événements à relier, et le doublon `DevelopmentPhase` / `Concept` « Phase de maturation » à arbitrer. **Priorité maximale pour l'effet visuel recherché.**
2. **La chaîne de `CrisisPhase` de CVE-2018-17144 n'a pas de phase d'insémination**, alors que l'attribut `phases` de l'entité en annonce une et que la séquence The DAO en possède une. PR 9049 est actuellement rattaché à la crise par `precursor of`, faute de phase à laquelle s'accrocher.
3. **PR 10195 et PR 10537** (avril-juin 2017), à l'origine de l'itération « faux monnayage », sont absentes du graphe **et du CSV**. Les ajouter serait inventer des événements hors source — non fait.
4. **E070**, franchissement durable des 1000 $ début 2017 : réellement absent, appuyé verbatim par la thèse, mais son type correct est `PriceWindow`, hors du périmètre déclaré ici.
5. **E022 Bitcoin Magazine** : fondation absente comme événement, mais **le graphe se contredit sur la date** — `MediaOutlet` et référence Castillo 2013 disent 2012, l'entité `Person` Mihai Alisie dit 2011, le CSV dit 2011. Non ajouté.
6. **Divergence de date E044** : le CSV date BIP16 de 2013-04, le graphe de 2012-04 avec source O'Brien 2014. Le graphe a raison ; **c'est le CSV qui est à corriger**.
7. **La date de fondation de Coinbase (E034) provient de la figure n°6**, non du texte, qui ne mentionne Coinbase que comme indicateur. Ajouté avec cette réserve consignée dans sa description.
8. **Doublons préexistants repérés sans être traités** : `Bitcoin Foundation creation` / `Fondation Bitcoin (fin 2012)`, et les deux BitPay. Ils montrent que la catégorie « fondation d'organisation » a déjà produit des doublons — raison de plus pour relire E034.

## Livrables

| Fichier | Nature |
|---|---|
| `docs/audits/grc20-add-missing-events/01-chronology-audit.md` | audit du CSV |
| `docs/audits/grc20-add-missing-events/02-graph-inventory.md` | conventions du graphe |
| `docs/audits/grc20-add-missing-events/03-matching-report.md` | appariement et vérification adverse |
| `docs/audits/grc20-add-missing-events/04-semantic-check.md` | typage et cohérence avec la thèse |
| `docs/audits/grc20-add-missing-events/05-final-synthesis.md` | ce document |
| `docs/audits/data/chronology-events-classification.csv` | 78 lignes, sortie mécanique |
| `docs/audits/data/chronology-events-arbitration.csv` | 19 lignes, verdicts de vérification |
| `docs/audits/data/added-events-from-chronology.csv` | 6 ajouts |
| `docs/audits/data/rejected-or-ambiguous-chronology-events.csv` | 13 écartés, avec motif |
| `scripts/match_chronology_events.py` | appariement rejouable |
| `scripts/make_v98_add_missing_chronology_events.py` | construction de v98, validante |
| `patch_11_add_missing_chronology_events.json` | patch, 6 entités + 25 relations |
| `grc20-these-mael-rolland-v98.json` | graphe candidat |
