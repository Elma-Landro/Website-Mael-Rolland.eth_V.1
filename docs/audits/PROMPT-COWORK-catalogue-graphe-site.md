# PROMPT COWORK — Catalogue d'événements × graphe GRC-20 × site
Version complétée le 05/08/2026. Le texte de Maël (Elma) est intégral en BLOC C ; les BLOCS A, B et D sont des ajouts de la session claude.ai pour l'environnement, les fichiers et la traduction opérationnelle.

---

## BLOC A — Environnement et connexions [AJOUT]

Répertoire de travail : "Website-Mael-Rolland.eth_V.1" (clone local existant, le même que celui utilisé par Claude Code)
Dépôt GitHub : "Elma-Landro/Website-Mael-Rolland.eth_V.1"
Branche par défaut de travail : "codex/create-expand-from-node-planning-documents"

Do NOT create a new branch.
Stay on the current branch only.

Accès :
- **Git local** : utiliser les identifiants git déjà configurés sur la machine (les mêmes que Claude Code — `gh auth` / clés existantes). Commits directs sur la branche de travail ci-dessus.
- **MCP GitHub officiel** (opérations distantes : suivi, issues, PR existantes) : connecteur personnalisé, URL `https://api.githubcopilot.com/mcp/`. Si un jeton est demandé : PAT à granularité fine, permissions minimales — Contents et Pull requests (lecture-écriture) sur ce seul dépôt.
- **Primauté** : les contraintes du BLOC C priment sur `PASSATION-claude-code-dedup-events.md` §5 — donc PAS de branche `agent/grc20-dedup-events-v1`, PAS d'ouverture de PR ; le reste de la passation (destinations des fichiers, points à ne pas trancher) reste valable.

## BLOC B — Fichiers fournis (zip `chantier-catalogue-2026-08-05.zip`) [AJOUT]

À déposer dans le dépôt :
- `catalogue-evenements-v3-1.csv` (maître, 345 lignes, colonnes codage_statut/codage_justif) + `catalogue-evenements-v2-fusion.csv` + `catalogue-evenements-v1.csv` → `docs/research/catalogue-evenements/`
- `chrono-v28-decodee.csv` + `Chrono_Bitcoin_institutionnalisation_V2_8__altcoin_addition_.bin` → `docs/research/chronologies/` (le dépôt n'a que la V2.5)
- `grille-codage-catalogue-v1.md`, `etat-*.md` (4 fichiers d'état), `doublons-verifies.csv`, `dates-verification-externe.csv`, `table-divergences-dates.csv`, `doublons-probables.csv` → `docs/audits/` (+ sous-dossier `data/` pour les CSV)
- `patch_10_dedup_events.json` → racine (convention `patch_*.json`)
- `fusion.py`, `verif_doublons.py` → `scripts/`
- `PASSATION-claude-code-dedup-events.md` → `docs/audits/`
- `catalogue-evenements-LECTURE.xlsx` et `lot1-crises-a-valider.csv` : documents de travail de Maël, à déposer dans `docs/research/catalogue-evenements/` sans autre traitement.

Correctif une ligne à faire dans `scripts/decode_chronologie.py` : ajouter la couleur `'255,240,91,155': ('vii', '#f05b9b', 'rose', 'altcoins, Ethereum, Tether, DAO')` à la table `COULEURS` (absente car calibrée sur la V2.5).

## BLOC C — Cadrage de Maël (verbatim, fait autorité)

Oui, je valide l'orientation générale : il faut éviter deux inventaires parallèles. Le catalogue événementiel doit devenir le référentiel scientifique des événements codés, utilisable à la fois pour les articles, les matrices analytiques et le site.

Mais je veux préciser l'architecture :

1. Le catalogue n'efface pas le graphe.
   Le catalogue devient la couche scientifique de codage des événements ; le graphe reste la couche canonique publiée, avec ses IDs, ses versions et ses contraintes. Toute synchronisation vers le graphe passe par patch candidat, audit et validation.

2. Le site ne consomme pas directement un tableur mouvant.
   Le site consomme le graphe public et, éventuellement, des exports dérivés/versionnés du catalogue. Pas de dépendance directe à un fichier de travail non stabilisé.

3. Les articles consomment des snapshots.
   Chaque article doit pouvoir citer un état figé du catalogue : version, date, lots inclus, colonnes gelées, exclusions, lignes CHANTIER.

4. Je valide la page d'architecture unique comme prochaine sortie.
   Elle doit cadrer :

- les couches : catalogue / graphe / site / articles ;
- les identifiants : event_id, graph_entity_id, source_id ;
- le statut des lignes : validé, chantier, douteux, exclu ;
- le circuit catalogue → patch → graphe ;
- ce qui relève de Maël et ce qui peut être codé en autonomie ;
- la règle anti-divergence entre catalogue et graphe.

5. Sur attaquant/résolveur : attention.
   Je ne veux pas une paire morale ou trop étroite. "Attaquant/résolveur" peut fonctionner pour certains événements de crise, mais pas pour tous. Il faut plutôt une convention de rôles :

- acteur déclencheur / initiateur ;
- acteur affecté ;
- acteur révélateur ;
- acteur correcteur ;
- acteur validateur ;
- acteur opposant ;
- acteur coordinateur ;
  avec possibilité "non applicable" et "incertain".

6. Sur Q7 / gel du vocabulaire :
   oui au gel d'un vocabulaire v0, mais seulement après une courte passe d'épreuve sur un lot représentatif. Une fois gelé, on ne renomme pas silencieusement : on ajoute une version ou une table de correspondance.

Prochaine sortie attendue :
une page d'architecture unique, pas encore un codage massif.

Contraintes :

- pas de fusion silencieuse catalogue/graphe ;
- pas de génération automatique vers le graphe sans patch ;
- pas de codage forcé des lignes incertaines : elles restent CHANTIER ;
- pas de création de branche ;
- rester sur "codex/create-expand-from-node-planning-documents".

## BLOC D — Traduction opérationnelle de la prochaine sortie [AJOUT]

Livrable unique de cette session Cowork : `docs/architecture/catalogue-graphe-site.md`, puis STOP (validation de Maël avant toute autre action). La page doit couvrir les six points du BLOC C §4, plus :

- **Identifiants** — proposer le mapping à partir de l'existant : `event_id` = colonne `id` du catalogue (E/G/F + numéro) ; `graph_entity_id` = colonne `gid` (207 lignes en portent un) ; `source_id` = colonne `source` (fichier + ligne, ou fig./graphe). Ne pas renommer les colonnes existantes sans table de correspondance.
- **Statuts** — unifier l'existant (`codage_statut` : valide(calibrage) / propose(lot1) ; notes [CHANTIER]) avec la typologie de Maël : validé / chantier / douteux / exclu. Proposer la table de passage, ne rien recoder.
- **Rôles (§5)** — spécifier la grille v2 : comment la convention de rôles (déclencheur, affecté, révélateur, correcteur, validateur, opposant, coordinateur, n.a., incertain) s'articule avec les colonnes actuelles `acteur_principal`/`acteur_secondaire` (7 types d'acteurs = QUI ; rôles = COMMENT il intervient). Le lot 1 déjà proposé n'est PAS recodé dans cette session : la page décrit la migration, Maël arbitre.
- **Q7 (§6)** — décrire le protocole d'épreuve : lot représentatif (~15 lignes multi-domaines dont effets énoncés par le texte), codage test avec le vocabulaire provisoire, rapport d'écarts, puis gel v0 avec numéro de version et règle de non-renommage.
- **Anti-divergence** — règle unique : le graphe n'est modifié que par `patch_*.json` généré depuis le catalogue, audité, validé ; le catalogue n'importe du graphe que par les scripts versionnés (`fusion.py`) ; toute divergence détectée devient une ligne d'audit, jamais une correction silencieuse.

Interdits reconduits : rien n'est tranché à la place de Maël ; les lignes incertaines restent CHANTIER ; aucun codage massif dans cette session.
