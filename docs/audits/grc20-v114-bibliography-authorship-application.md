# GRC-20 v114 — application des 4 relations `authored`

**Date** : 2026-08-11
**Graphe produit** : `grc20-these-mael-rolland-v114.json` (**canonique**)
**Source** : `grc20-these-mael-rolland-v113.json` (**inchangé**)
**Patch appliqué** : `patch_candidate_bibliography_authorship_v1.json` — **le seul**
**Applicateur** : `scripts/make_v114_apply_bibliography_authorship_relations.py`
**Arbitrage** : Maël Rolland, 2026-08-10, questions 1 à 5 (PR #123)
**Instruction** : `grc20-bibliography-authorship-support-lab-v1.md` · `docs/audits/data/bibliography-authorship-support-v113.csv`

**4 relations ajoutées, rien d'autre.** Aucune entité créée ni modifiée, aucun attribut, aucun type, aucun nom, aucune fusion, aucun `duplicateOf`, aucune `SourceQuote`, aucune relation existante touchée.

---

## 1. Ce qui est écrit

| Auteur | Œuvre | Preuve |
|---|---|---|
| `53525938` Jacques Favier | `e19babe5` Bitcoin, la monnaie acéphale | `07_bibliographie.md:476` |
| `53525938` Jacques Favier | `b84f59ac` Tulipes | `:474` |
| `53525938` Jacques Favier | `7f0f9cc4` Bitcoin et la religion | `:472` |
| `ec901513` Adli Takkal Bataille | `e19babe5` Bitcoin, la monnaie acéphale | `:476` |

Type de relation : `authored` (`2d3f43441ee747dda4172f0954a9fadd`), le même pour les quatre. Identifiants dérivés déterministes (md5 d'un sel dédié + les deux extrémités), donc l'applicateur est rejouable **à l'octet près** : deux exécutions produisent le même fichier, vérifié.

---

## 2. La preuve — comparaison indépendante v113/v114

Recomptée **sans passer par l'applicateur**, en relisant les deux fichiers.

| Bloc | v113 | v114 | Verdict |
|---|---:|---:|---|
| entités | 2 293 | 2 293 | **identiques octet pour octet**, même ordre d'ids |
| relations | 20 207 | 20 211 | **+4**, les 20 207 premières inchangées |
| types | 55 | 55 | identiques |
| relation_types | 130 | 130 | identiques |
| ops | 274 | 274 | identiques |
| `authored` | 122 | 126 | +4 |

- **`json.dumps(entities, sort_keys=True)` est identique** entre les deux graphes : aucune entité n'a bougé, ni son nom, ni ses types, ni un seul de ses attributs.
- **Le préfixe des relations est intact** : les 20 207 relations de v113 occupent les 20 207 premières positions de v114, avec le même contenu. Les 4 nouvelles sont ajoutées **à la fin**. Comparer des ensembles aurait laissé passer une réécriture compensée ; la comparaison est positionnelle.
- **Aucune paire disparue, aucune paire nouvelle hors des quatre.**
- **Les identifiants de relation restent uniques** dans v114.

`space` : `version` v113 → v114, `entity_count` 2 293 (inchangé), `relation_count` 20 207 → 20 211, `note` réécrite à 1 194 caractères pour un plafond de 1 200.

---

## 3. Ce qui n'a **pas** été fait, et qui aurait pu l'être

- **DeNardis → `e0b40d91` reste absente.** Cette cinquième paire, instruite en #123, est nommée dans `REFUSEES` de l'applicateur, qui échoue si un patch la contient. Motif : la fiche décrit la même entrée bibliographique (`:394`) que `2272e5b8`, qui porte déjà l'`authored` de DeNardis ; en poser un second aurait gravé le doublon en œuvre distincte. Vérifié absente de v114.
- **Le nom fautif de `7f0f9cc4` n'est pas corrigé.** La fiche s'annonce toujours « (La voie du Bitcoin) » alors que la bibliographie donne un podcast `parlonsbitcoin.com`. L'éditeur est faux, la paternité ne l'est pas. Corriger serait un **renommage**, hors périmètre par l'arbitrage 3. Vérifié : le nom est identique dans v113 et v114.
- **La `policy` du patch est intacte**, byte-identique, préfixe C03 compris — l'applicateur ouvre le patch en **lecture seule**. Le bloc `_meta.arbitrage` est intact lui aussi.

---

## 4. Ce que l'applicateur refuse — et qui a été éprouvé

Le lot est figé dans le script, **valeurs comprises** : ids des deux extrémités, **noms attendus** de chacune, id **et** nom du type de relation, preuve bibliographique, nombre exact d'opérations. Un patch retouché entre l'arbitrage et l'application ne peut donc pas faire écrire autre chose — c'est la leçon de la revue de v112, où figer les seuls identifiants laissait réécrire la valeur cible.

Chaque refus a été **déclenché** sur un patch volontairement faussé, pas seulement écrit :

| Ce qui est refusé | Vérifié |
|---|---|
| op autre que `ADD_RELATION` | `SET_NAME` → échec |
| `relationTypeId` autre que `authored` | échec |
| `relationTypeName` incohérent avec l'id | `cited in` → échec |
| extrémité absente du graphe | échec |
| extrémités identiques | échec |
| cinquième relation | 5 ops → échec |
| œuvre hors du lot | `2272e5b8` → échec |
| auteur hors du lot | DeNardis → échec |
| **paire recombinée** (auteur et œuvre du lot, mais pas ensemble) | Takkal → Tulipes → échec |
| paire explicitement REFUSÉE | DeNardis → `e0b40d91` → échec |
| relation déjà présente | échec |
| même paire deux fois | échec |
| `policy` réécrite | échec |
| bloc `_meta.arbitrage` retiré | échec |

Et le contrôle d'après est exhaustif : entités comparées champ de tête par champ de tête **et** attribut par attribut, relations comparées une par une. Le script n'écrit que si le diff complet vaut exactement 4 relations ajoutées, 0 supprimée, 0 modifiée, 0 changement d'entité. Une seconde exécution sur v114 est refusée à l'entrée (`space.version` ≠ v113).

---

## 5. Un défaut de conception révélé par l'application

**Un contrôle juste avant l'application est devenu faux après.** C13 — le contrôle relationnel ajouté en #123 — refusait toute relation déjà portée par le graphe, à juste titre : reposer une relation existante crée un doublon **silencieux**, sans collision de nom pour le signaler. Mais une fois v114 écrite, les quatre relations existent, et C13 criait au doublon sur un patch simplement **appliqué**.

Les trois candidats appliqués avant celui-ci n'avaient jamais posé le problème : leurs ops (`SET_*`) ne sont testées que sur l'existence de la cible, jamais sur « l'effet est-il déjà là ». C13 était le premier contrôle du preflight à mesurer un effet.

Le partage se fait désormais sur le **compte**, ce qui est plus juste que ce que j'avais écrit :

- **toutes** les relations présentes → AVERTISSEMENT : le patch est appliqué, un rejeu est sans effet ;
- **quelques-unes** → BLOQUANT : état mixte, le cas le plus dangereux, où un rejeu écrirait à côté ;
- **aucune** → OK : candidat intact.

Les deux branches ont été éprouvées : 4/4 → avertissement, 3/4 → bloquant.

---

## 6. File, ledger et cycle de vie

La mesure dans v114 donne **4/4 ops réalisées** → la file passe le patch de `blocked_by_missing_applicator` à `already_applied`, et la gouvernance de `blocked_missing_applicator` à **`candidate_applied`**. Ce n'est pas déclaré : c'est mesuré dans le graphe, comme tout le reste.

Le ledger enregistre v114 et le `lifecycleStatus` du patch suit. **Ordre inchangé, et il compte** : graphe → file vivante → ledger. Jamais la `policy`, qui continue de dire « NOT APPLIED » parce que C03 l'exige, et jamais `lifecycleStatus`, qui n'est qu'une copie datée de la mesure.

> **Séquence assumée.** Le ledger enregistre le **numéro de PR** qui a appliqué le patch — une information qui n'existe pas avant que la PR soit ouverte. L'entrée du ledger et le `lifecycleStatus` arrivent donc dans un **second commit**, après création de la PR. La garde qui l'impose n'est pas un accident : `build_patch_lifecycle_status.py` refuse d'écrire `candidate_applied` sur un patch absent du ledger, précisément pour qu'une application ne puisse pas rester non consignée.

---

## 7. Pointeurs de version

Mis à jour vers v114 : `package.json` (4), `these.html` (2), `graphe.html` (2), `lecteur.html` (1), `graph-worker.mjs` (1), `narrative-anchors-build.mjs` (2), `grc20-publish.mjs` (3), `export/scripts/export-workshop-to-public.mjs` (1). **Le runtime n'est touché que là** — aucune autre ligne de `graphe.html` ou `lecteur.html` ne change.

Le `source_graph` des patchs candidats n'est **pas** touché : c'est un enregistrement de ce contre quoi ils ont été construits, pas un pointeur.

Le registre des propriétés est régénéré dans le même commit (convention du dépôt). Seul changement : `make_v114…` rejoint les `readBy` de `type`, `source` et `note` — exactement comme chaque applicateur avant lui. **Aucune entrée, aucun domaine, aucun compte ne change** : 338 entrées avant comme après.

---

## 8. Limites connues

- **Aucune vérification navigateur.** Le diff runtime est borné aux pointeurs de version, mais 4 relations nouvelles *changent ce que l'écran montre* : `graphe.html` compte ses arêtes depuis les relations, et deux fiches `Person` isolées deviennent connectées. L'effet attendu est un gain de 4 arêtes et rien d'autre ; il n'est pas prouvé ici. C'est une exception au principe « vérification navigateur pour tout changement de runtime », et elle est plus mince qu'en v113 — aucun filtre par type n'est traversé — mais elle existe.
- **`mentions actor` n'est pas posé en retour.** Les quatre auteurs déjà pourvus portent cette réciproque ; la mesure de #123 a montré qu'elle ne vaut que pour **13 `authored` sur 122**. Ne pas la poser suit la pratique majoritaire, mais laisse les quatre nouvelles paires asymétriques comme 109 autres.
- **`authored` n'est pas uniformément Personne → Œuvre dans ce graphe** : quatre relations partent d'une fiche `Reference`. Dette signalée en #123, toujours ouverte, hors de ce lot.
