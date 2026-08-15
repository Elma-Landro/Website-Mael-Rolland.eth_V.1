# Grille de rôles v0 — catalogue d'événements

**Statut : v0 validée par Maël Rolland le 15/08/2026 (arbitrage D6), gelable seulement après la passe d'épreuve Q7 (arbitrage D11).** Une fois gelée, aucun renommage silencieux : tout changement produit une v1 ou une table de correspondance versionnée (règle de la page d'architecture, §7.3, appliquée ici par extension).

Destination au dépôt : `docs/research/catalogue-evenements/grille-roles-v0.md`.
Document de référence : `docs/architecture/catalogue-graphe-site.md` §4 (grille de rôles v2 y était esquissée ; le présent document la remplace comme spécification, sur arbitrage D6).

---

## 1. Principe

La grille sépare deux questions que les colonnes actuelles du catalogue mélangent :

- **QUI intervient** — les 7 types d'acteurs de la grille de codage v1, inchangés : `core_devs` · `mineurs` · `entrepreneurs_exchanges` · `institutions_financieres` · `regulateurs_etats` · `medias_connaissance` · `communautes_forums` ;
- **COMMENT il intervient** — les rôles ci-dessous.

Les deux vocabulaires sont orthogonaux : `core_devs` peut être `correcteur` (CVE corrigée), `initiateur` (changement protocolaire) ou `opposant` (rejet d'une proposition). La grille est **non morale** (aucun rôle ne juge), **multi-acteurs** et **multi-rôles** : un événement peut porter plusieurs acteurs, un acteur peut cumuler plusieurs rôles sur le même événement.

La paire attaquant/résolveur est **refusée** (D6) : trop morale, trop étroite, inapplicable hors crise.

## 2. Les rôles (vocabulaire fermé v0 — verbatim de l'arbitrage D6)

| Rôle | Définition (D6) | Guide de codage — frontières |
|---|---|---|
| `initiateur` | déclenche ou lance l'acte | l'acte n'existerait pas sans lui ; ne pas confondre avec `exploiteur` : l'initiateur crée, l'exploiteur tire parti de ce qui existe |
| `exploiteur` | tire parti d'une faille, d'un conflit ou d'une opportunité | suppose un existant (vulnérabilité, ambiguïté, situation) ; l'attaquant de The DAO est `exploiteur`, pas « attaquant » |
| `affecte` | subit directement l'événement | directement : les porteurs de fonds de The DAO, le protocole en crise ; pas les commentateurs |
| `revelateur` | rend visible, documente ou signale | fait passer de l'invisible au visible (divulgation d'une CVE, signalement d'un bogue) ; se distingue d'`observateur` par l'effet : après lui, les autres savent |
| `correcteur` | produit ou propose la correction | produit le correctif, le patch, la procédure ; « propose » compte — la correction non adoptée reste un rôle tenu |
| `validateur` | valide, accepte, confirme ou ratifie | acte d'acceptation distinct de la production : les mineurs qui adoptent un fork, une communauté qui ratifie |
| `coordinateur` | organise, relaie, synchronise | tient la logistique de l'action collective (huis clos inter-implémentations de CVE-2018, orchestration d'un déploiement) |
| `opposant` | conteste, bloque, refuse ou critique | opposition agissante (veto, campagne, fork de refus) ; la simple critique publiée sans action relève d'`observateur` ou de `revelateur` selon l'effet |
| `observateur` | commente, mesure, documente sans agir directement | présence documentante sans prise sur le cours de l'événement (presse, académiques, données) |
| `non_applicable` | — | l'événement ne se prête pas à ce codage (certains seuils) |
| `incertain` | — | les sources ne permettent pas de trancher ; jamais de rôle forcé |

Règles transversales : aucun rôle n'est forcé (une ligne sans rôle codable reste sans ligne de rôle, ou porte `incertain`) ; aucun rôle n'est créé en silence (trou typologique → note + arbitrage) ; le vocabulaire est fermé jusqu'à la passe d'épreuve.

## 3. Forme de la donnée — table satellite (D6)

**La donnée maîtresse n'est pas une colonne plate.** Fichier dédié :

`docs/research/catalogue-evenements/catalogue-roles-v0.csv`, séparateur `;`, une ligne par (événement × acteur × rôle) :

```
event_id;actor_id;actor_name;role;confidence;note
E065;nd;attaquant anonyme;exploiteur;haute;hors typologie v1, précédent E065
E065;core_devs;;correcteur;haute;réponse protocolaire
```

- `event_id` — id du catalogue (E/G/F), obligatoire ;
- `actor_id` — un des 7 types d'acteurs v1, ou `nd` si hors typologie *(recommandation : garder la typologie v1 comme clé, le nom propre en précision — à confirmer à l'usage)* ;
- `actor_name` — nom propre optionnel (personne, entité, protocole) quand il précise ;
- `role` — un rôle du §2, exactement ;
- `confidence` — `haute` / `moyenne` / `basse` *(vocabulaire proposé, non arbitré — la passe d'épreuve dira s'il suffit)* ;
- `note` — source ou justification courte, recommandée dès que `confidence` n'est pas `haute`.

Plusieurs lignes par événement sont la norme, pas l'exception. Une **vue pivotée** (une ligne par événement, rôles agrégés) pourra être dérivée par script pour les articles ou le site ; elle est un produit, jamais la source.

Compatibilité descendante : les colonnes `acteur_principal` / `acteur_secondaire` du CSV maître **demeurent** (elles portent la règle D7 ci-dessous) ; la table de rôles les complète, elle ne les remplace pas.

## 4. Articulation avec `acteur_principal` — règle D7

Pour le CSV maître, l'acteur principal ne revient **jamais automatiquement** à l'exploiteur :

- **crise agrégée** (« exploitée puis résolue », recensée comme un tout) → `acteur_principal` = **l'entité affectée / gouvernée / mise en crise** (protocole, infrastructure, collectif, écosystème) ; exploiteurs, découvreurs, correcteurs, validateurs vont dans la table de rôles ;
- **acte ponctuel** (une attaque datée, une publication, un patch, une annonce) → `acteur_principal` = **l'initiateur de l'acte** ;
- le partage crise agrégée / acte ponctuel dépend de la **granularité de la ligne**, jamais d'un jugement moral ;
- **doute** → `acteur_principal = a_arbitrer`.

Conséquence : les 40 lignes du lot 1 (codées sous l'ancienne convention E065) devront être re-passées sous cette règle — **hors périmètre du lot 2** (pas de codage massif), sauf celles qui entrent dans le lot d'épreuve Q7.

## 5. Trois exemples illustratifs (non codés au catalogue — l'épreuve D11 fera foi)

**The DAO, 2016 — crise agrégée.** `acteur_principal` = The DAO / écosystème Ethereum (affecté). Rôles : attaquant anonyme → `exploiteur` ; porteurs de parts → `affecte` ; communauté/développeurs → `revelateur` puis `correcteur` (fork correctif) ; mineurs et nœuds → `validateur` ; partisans d'ETC → `opposant`. C'est le cas exigé par D11 où attaquant/résolveur serait trompeur : cinq fonctions distinctes, aucune paire ne les capture.

**CVE-2018-17144 — crise agrégée, huis clos.** `acteur_principal` = protocole Bitcoin (mis en crise). Rôles : découvreur → `revelateur` ; core devs → `correcteur` ; coordination discrète inter-implémentations → `coordinateur` ; mineurs mettant à jour → `validateur`. Personne n'« attaque » : la paire refusée n'aurait rien su coder.

**Value Overflow, 2010 (crise n°4, précédent E015) — selon la granularité.** Recensée comme crise agrégée → principal = protocole Bitcoin (affecté), exploiteur au rôle. Recensée comme l'acte ponctuel d'exploitation → principal = initiateur de l'acte. La granularité de la ligne décide, pas la morale — c'est exactement l'arbitrage D7.

## 6. Provenance

Vocabulaire, forme de table et règle D7 : arbitrages de Maël Rolland du 15/08/2026 (verbatim intégral archivé dans `docs/audits/PROMPT-COWORK-lot2-statut-roles-q7.md`, BLOC C). Esquisse antérieure : `docs/architecture/catalogue-graphe-site.md` §4 (décisions D6/D7 alors ouvertes, désormais tranchées). Grille d'acteurs v1 : `docs/audits/grille-codage-catalogue-v1.md`.
