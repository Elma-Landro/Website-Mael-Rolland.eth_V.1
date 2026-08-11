# GRC-20 — Bibliography Authorship Support Lab v1

**Date** : 2026-08-10
**Graphe de référence** : `grc20-these-mael-rolland-v113.json` (canonique, **inchangé**)
**Branche** : `claude/file-upload-branch-check-jw4cng`
**Mécanisme rejouable** : `scripts/build_bibliography_authorship_support.py` (`--csv`, `--check`)
**Données probantes** : `docs/audits/data/bibliography-authorship-support-v113.csv` — 9 lignes
**Patch candidat** : `patch_candidate_bibliography_authorship_v1.json` — **4 ops, NON APPLIQUÉ**

**Aucun graphe modifié. Aucune v114. Aucun patch appliqué. Aucun nœud, aucune fusion, aucun retypage, aucun renommage, aucune `SourceQuote`, aucun attribut.**

---

## 1. Le constat, mesuré

Les six fiches retypées en `Person` par v113, avec leurs relations réelles :

| Entité | Nom | `authored` sortants | Autres relations |
|---|---|---:|---|
| `7cd4cfe4` | Gérard Dréan | **1** → Dréan 2013 | ← *mentions actor* |
| `be8ac286` | Andreas Loibl | **1** → Loibl 2014 | ← *mentions actor* |
| `5fc4278b` | Laura DeNardis | **1** → DeNardis et Musiani 2014 | ← *mentions actor* |
| `b332ace8` | Shinobi (pseudonyme) | **1** → Shinobi 2022 | ← *mentions actor* |
| `53525938` | **Jacques Favier** | **0** | 2 × *cited in* |
| `ec901513` | **Adli Takkal Bataille** | **0** | 1 × *cited in* |

La dette signalée est confirmée : deux auteurs sur six sont des `Person` sans lien vers leur propre œuvre, alors que leurs œuvres **existent** dans le graphe.

---

## 2. Ce que la vérification a écarté avant de proposer

Une paternité ne se déduit pas d'un nom proche — le dépôt en porte le précédent (« Florence Dufy », un nom soudé de deux co-auteurs réels, qu'un patch antérieur a failli graver). Chaque ligne a donc dû franchir **cinq** conditions, évaluées par le script et non supposées.

**Deux réserves structurelles ont été levées par la mesure, pas par le raisonnement :**

- **« Les `authored` existants visent une autre famille de fiches. »** Les quatre auteurs pourvus pointent vers des fiches portant un attribut `author` ; les œuvres de Favier appartiennent à une autre famille (`title` / `cited_in_chapters`, zéro relation entrante). Mesure : sur les **122** `authored` de v113, **91 visent déjà cette seconde famille**. Poser un `authored` vers une fiche « nouvelle famille » est donc la pratique **majoritaire**, pas une innovation.
- **« Il faudrait aussi poser le `mentions actor` réciproque. »** Les quatre auteurs pourvus le portent, ce qui suggérait une norme. Mesure : **13 `authored` sur 122** seulement ont ce retour. Ne pas le poser est conforme à la pratique dominante — et il est hors périmètre.

**Une mesure a aussi révélé une dette qui n'était pas cherchée** : quatre `authored` partent de `Aglietta & Orleans 2002`, qui est une fiche `Reference`, pas une `Person`. Le graphe ne tient donc pas uniformément `authored` pour une relation Personne → Œuvre. Signalé, non corrigé : hors périmètre.

---

## 3. Les quatre relations proposées — certaines

| Auteur | Œuvre | Preuve bibliographique |
|---|---|---|
| Jacques Favier `53525938` | `e19babe5` Favier & Takkal Bataille 2017 — Bitcoin la monnaie acéphale | `07_bibliographie.md:476` |
| Jacques Favier | `b84f59ac` Favier 2017 — Tulipes | `07_bibliographie.md:474` |
| Jacques Favier | `7f0f9cc4` Favier 2021 — Bitcoin et la religion | `07_bibliographie.md:472` |
| Adli Takkal Bataille `ec901513` | `e19babe5` (co-signature) | `07_bibliographie.md:476` |

Pour chacune, vérifié : nom d'auteur **unique** dans le graphe (aucun homonyme) ; œuvre existante ; **zéro** `authored` entrant sur l'œuvre ; **zéro** relation de quelque type entre la paire ; œuvre non identifiée comme doublon. `b84f59ac` et `7f0f9cc4` ont été comparées l'une à l'autre — années et titres distincts, 14 sections communes sur 24 et 25 : ce sont bien deux textes.

**Aucune relation « probable » ni « ambiguë » n'est proposée.** Le lot ne contient que des lignes `certaine` ; il n'y a donc rien à exclure au titre de l'arbitrage 4, et c'est un résultat, pas un oubli.

---

## 4. La ligne explicitement refusée

`5fc4278b` Laura DeNardis → `e0b40d91` « DeNardis & Musiani 2014 — Governance by Infrastructure » : **NON**.

Cette fiche décrit la **même entrée bibliographique** (`07_bibliographie.md:394`) que `2272e5b8`, qui porte déjà l'`authored` de DeNardis. Lui en poser un second graverait le doublon comme une œuvre distincte — c'est-à-dire qu'une opération de réparation aurait consolidé une erreur. La ligne figure au CSV avec `proposed_relation = NON` et au patch dans `_meta.skipped`, parce qu'un tableau qui ne montre que ce qu'il propose laisse croire que le reste n'a pas été regardé.

À instruire comme **doublon bibliographique**, chantier distinct.

---

## 5. Une dette d'attribut découverte, signalée et non corrigée

La fiche `7f0f9cc4` se nomme « Favier 2021 — Bitcoin et la religion **(La voie du Bitcoin)** ». Or l'entrée `:472` donne un **podcast `parlonsbitcoin.com`**, et « La voie du Bitcoin » est l'éditeur de l'entrée `:474` (Tulipes). **L'éditeur porté par le nom de la fiche est faux.**

La paternité, elle, ne l'est pas : c'est l'unique entrée Favier 2021 de la bibliographie. La relation `authored` est donc certaine, et l'erreur d'éditeur est une dette **séparée** — corriger un nom de fiche est un renommage, explicitement hors périmètre.

Ce point illustre pourquoi la preuve est figée au fragment près : c'est en vérifiant mot pour mot que l'écart est apparu.

---

## 6. Le point qui n'est pas technique : la forme de l'op

Le contrat de patch du dépôt est explicite (`grc20-candidate-patch-contract-v1.md` § 4) :

> « Aucun applicateur ne consomme `ADD_RELATION`/`REMOVE_RELATION` ; leurs trois formes historiques sont incompatibles. **Un futur patch candidat relationnel devra faire trancher la forme avant dépôt.** »

Ce chantier est ce patch relationnel. La forme est donc **une décision réservée à l'auteur**, et le patch la porte comme une proposition, jamais comme un fait acquis : dialecte C étendu (`_meta` + `ops`, camelCase, clé `type`), type de relation **par id** (`relationTypeId`) doublé d'un nom déclaré (`relationTypeName`) vérifié contre le graphe. Motif du choix : le dialecte C est celui que le graphe parle nativement, et les trois formes historiques donnent le type **par nom**, ce qui est ambigu.

**Conséquence assumée à dire clairement** : `preflight_candidate_patches.py` classait tout `ADD_RELATION` `BLOQUANT` — « type d'op hors périmètre, INVÉRIFIABLE ». Le message prescrit lui-même la conduite : « étendre le validateur ou corriger le patch ». Le validateur a donc été étendu d'un contrôle **C13**. **C03 n'est pas touché.** Mais reconnaître une forme dans le validateur la rend *de facto* validable : si l'auteur en préfère une autre, C13 doit être réécrit avec elle. C'est pourquoi la question est posée en arbitrage 5 plutôt que réglée en silence.

### Ce que C13 vérifie

Extrémités existantes et distinctes, `relationTypeId` connu du graphe, `relationTypeName` cohérent avec cet id, **aucune relation déjà portée par le graphe**, aucune relation proposée deux fois dans le lot ; et un AVERTISSEMENT structurel tant qu'aucun applicateur ne consomme `ADD_RELATION`.

Le contrôle qui compte est l'avant-dernier. **Une relation déjà présente, reposée par un patch, est un doublon silencieux** : aucun nom ne collisionne, rien ne la signale, et le graphe se met à porter deux fois le même fait. C'est la variante relationnelle de l'incident d'homonymie qui a fait échouer `make_v110`, en plus discret. Les quatre gardes ont été éprouvées sur des patchs volontairement faussés : relation déjà présente, nom de type menteur, extrémité inexistante, relation vers soi-même — les quatre sortent `BLOQUANT`.

Effet sur les cinq patchs préexistants : **72 OK / 9 AVERTISSEMENT / 0 BLOQUANT** contre 67 / 9 / 0 avant. Les +5 sont exactement la ligne C13 « aucune op relationnelle », une par patch ; aucun AVERTISSEMENT ni BLOQUANT n'a changé.

C12 signale désormais que Favier et Takkal Bataille sont visés **à la fois** par le patch de retypages et par celui-ci. C'est exact et utile : le premier est appliqué (v113), le second ne l'est pas.

---

## 6 bis. Une mesure fausse, découverte en déposant le patch

Déposer ce patch a révélé un défaut dans la file elle-même, et il fallait le corriger avant de livrer.

`build_patch_queue_inventory.py` ne reconnaissait comme « bloqué faute d'applicateur » que les patchs faits de `CREATE_ENTITY`. Un patch tout en `ADD_RELATION` — également consommé par aucun applicateur — tombait dans `still_candidate`, dont la note de gouvernance dit **« TECHNIQUEMENT applicable »**. La file aurait donc affirmé qu'un *oui* de l'auteur suffirait à appliquer ce lot. C'est faux : il faudrait **aussi** écrire l'applicateur.

Extension de la détection à `ADD_RELATION`, **après avoir mesuré son effet** : tous les artefacts historiques porteurs d'`ADD_RELATION` ont déjà des ops réalisées, et la condition exige `0 op réalisée`. Vérification faite ligne à ligne — **exactement une ligne change dans la file, celle du nouveau patch**. Aucun artefact existant ne bouge.

Deuxième correctif, de même nature : la note `blocked_missing_applicator` disait *« le contrat interdit de pré-assigner un `entityId` »*, ce qui est vrai des créations et hors sujet pour un patch relationnel — elle aurait laissé croire que ce patch crée des nœuds. Le verrou est désormais **dérivé du type d'op** : `CREATE_ENTITY` reçoit la mention du contrat sur l'`entityId`, `ADD_RELATION` celle de la forme à arbitrer. Un type d'op sans verrou rédigé fait échouer le script plutôt que d'écrire une note vague.

**Conséquence à déclarer** : le fichier `patch_candidate_bibliographie_missing_nodes_v1.json` voit le **texte** de son `noteForAgents` changer — il gagne « CREATE_ENTITY » en toutes lettres. **Son `lifecycleStatus` ne change pas**, ni aucun autre champ. C'est la seule modification apportée à un patch préexistant, et elle rend sa note plus précise, pas différente.

---

## 7. Ce que ce chantier ne fait pas

Il n'applique rien, ne crée aucune v114, n'écrit aucun applicateur. Il ne touche ni aux fusions, ni aux doublons bibliographiques, ni aux créations de nœuds, ni aux `SourceQuote`, ni au runtime. Il ne corrige pas le nom de fiche fautif du § 5. Il ne modifie ni C03, ni les `lifecycleStatus`, ni le ledger, ni la file.

---

## 8. Arbitrages — posés, puis **rendus le 2026-08-10**

Les cinq questions ont été posées dans le fil de discussion et ont toutes reçu réponse. Elles sont reportées ici, avec leur réponse, pour que ce document se suffise — et inscrites dans `_meta.arbitrage` du patch, **jamais dans sa `policy`**.

| # | Question | Réponse |
|---|---|---|
| 1 | Valider les 4 relations `authored` certaines ? | **OUI**, les quatre |
| 2 | Créer v114 pour ce seul lot relationnel ? | **OUI sur le principe, NON dans cette PR** |
| 3 | Garder fusions, créations, doublons et `SourceQuote` hors périmètre ? | **OUI** |
| 4 | Exclure les relations probables/ambiguës ? | **OUI**, comme règle générale |
| 5 | La forme de l'op relationnelle ? | **Forme proposée validée** |

**1 — les quatre relations sont validées.** Motif retenu par l'auteur : auteur et œuvre nommés ensemble dans la bibliographie, auteurs uniques dans le graphe, œuvres existantes, aucune relation déjà sur la paire, aucune œuvre identifiée comme doublon.

**2 — la v114 est validée dans son principe, et explicitement refusée ici.** Elle doit faire l'objet d'une **PR séparée**, avec un **applicateur `ADD_RELATION` dédié**. Cette PR-ci reste ce qu'elle est : instruction et patch candidat non appliqué.

**3 — périmètre de la future v114, en creux.** Aucune fusion, aucun `duplicateOf`, aucune création de nœud, aucune `SourceQuote`, aucun renommage, aucun retypage, aucune correction de nom de fiche, et **aucune relation autre que ces quatre**. La dette du § 5 — l'éditeur erroné de `7f0f9cc4` — reste hors périmètre : elle sera instruite plus tard **comme renommage**, pas ici.

**4 — règle générale, au-delà de ce lot.** Seules les relations *certaines*, avec preuve bibliographique explicite nommant l'auteur **et** l'œuvre, peuvent entrer dans un lot applicatif. Ici il n'y a rien à retrancher : le lot n'en contient aucune autre.

**5 — la forme est arrêtée.** `ADD_RELATION`, extrémités par identifiants, type par `relationTypeId`, nom déclaré `relationTypeName` vérifié contre le graphe, **contrôle C13 obligatoire** (extrémités existantes et distinctes, `relationTypeId` connu, `relationTypeName` cohérent, aucune relation déjà présente, aucune proposée deux fois). C'est la forme retenue pour ce patch **et pour le futur applicateur v114**. Une autre forme relationnelle proposée plus tard devra être instruite séparément et **ne changera pas rétroactivement ce lot**. Le contrat de patch est mis à jour en conséquence (`grc20-candidate-patch-contract-v1.md` § 4 bis).

### Ce que la PR suivante devra prouver

L'arbitrage 2 pose une condition, pas une autorisation générale. La PR qui créera v114 devra **démontrer que ces quatre relations sont les seules ajoutées** — pas l'affirmer. Le motif de forme est déjà en place : compter les relations avant/après, vérifier le quadruplet `(from, to, type)` de chacune, et prouver qu'aucun autre champ du graphe n'a bougé, sur le modèle des applicateurs `make_vNNN` existants dont le lot approuvé fige les **valeurs**, pas seulement les identifiants.

**Rien n'est appliqué ici**, et l'arbitrage ne suffit pas à débloquer : aucun applicateur du dépôt ne consomme `ADD_RELATION`. L'écrire reste un chantier technique distinct — le `lifecycleStatus` mesuré du patch dit `blocked_missing_applicator`, et il continuera de le dire jusqu'à ce que l'applicateur existe.

---

## 9. Limites connues

- **La preuve est bibliographique, pas éditoriale.** Le script vérifie qu'une entrée nomme l'auteur et l'œuvre. Il ne vérifie pas que la fiche du graphe décrit *bien* cette édition-là — c'est précisément ce qui a laissé passer l'erreur d'éditeur du § 5, découverte à la lecture et non par le contrôle.
- **La recherche d'œuvres repose sur les champs nommants** (`name`, `nameEn`, `labelEn`, `labelFr`, `aliases`) et sur les patronymes. Une fiche qui ne nommerait ni l'auteur ni un mot du titre resterait invisible. Le risque est faible ici — les trois œuvres de Favier portent son nom — mais il n'est pas nul pour d'éventuelles fiches à venir.
- **C13 ne valide qu'une forme.** Les trois formes historiques d'`ADD_RELATION` restent invérifiables et continueront de sortir `BLOQUANT`. C'est voulu tant que l'arbitrage 5 n'a pas tranché.
