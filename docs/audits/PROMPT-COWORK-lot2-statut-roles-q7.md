# PROMPT COWORK — Lot 2 : statut_ligne × grille de rôles v0 × passe d'épreuve Q7

Version du 15/08/2026. Le BLOC C est le verbatim des arbitrages de Maël (fait autorité). Les BLOCS A, B et D sont la traduction opérationnelle héritée de la session du 15/08, qui a livré le lot 1 (page d'architecture + dépôt du chantier, 16 fichiers en ligne). **Rien du lot 1 n'est à refaire** : cette session reprend au lot 2.

---

## BLOC A — Environnement, accès, leçons du canal [HÉRITÉ, VÉRIFIÉ LE 15/08]

Dépôt : `Elma-Landro/Website-Mael-Rolland.eth_V.1` — branche de travail : `codex/create-expand-from-node-planning-documents`.
Do NOT create a new branch. Stay on the current branch only. Pas de PR.

**Lecture** : clone HTTPS anonyme autorisé (`git clone --branch codex/create-expand-from-node-planning-documents https://github.com/Elma-Landro/Website-Mael-Rolland.eth_V.1`). Lire `CLAUDE.md` et `agents/README.md` AVANT toute action : la charte du dépôt fait loi (un agent est un rôle de travail, pas une autorité scientifique ; data is not fact — cela vaut aussi pour les chiffres du présent prompt : REMESURER sur les fichiers avant de citer).

**Écriture — le seul canal qui marche** : le connecteur MCP GitHub officiel (déjà installé sur le compte, `https://api.githubcopilot.com/mcp/x/all`). L'ACTIVER DANS LE CHAT dès le début (menu des connecteurs de la conversation), charger les outils via ToolSearch, vérifier l'authentification par `get_me` (doit répondre Elma-Landro).

Leçons du canal, payées cher le 15/08 — ne pas les redécouvrir :
1. **`git push` est bloqué par le proxy de session** (403 « not in this session's authorized repository set »). Ne pas essayer, ne pas réessayer, ne pas chercher à contourner.
2. **Un appel d'outil plafonne** : ~55 Ko de contenu passent, 143 Ko échouent physiquement (plafond de sortie par réponse). Un gros fichier par appel `push_files`, jamais deux.
3. **Fichiers CRLF** : les CSV du catalogue finissent chaque ligne (dernière comprise) par `\r\n`. Le tool Read n'affiche pas les `\r` — ils existent. Les reproduire, sinon l'empreinte diverge.
4. **Vérifier CHAQUE envoi** : blob sha local (`git hash-object`) vs distant (`get_file_contents`, fields `["name","sha"]`). Aucun envoi n'est réputé bon sans cette comparaison.
5. **Ne JAMAIS pousser de fichier sous `.github/workflows/`** : refusé par le garde-fou de Cowork (légitime — code auto-exécutant), et le refus contamine ensuite toute la conversation. Si un assemblage côté serveur semble nécessaire, c'est le signe qu'il faut passer par l'upload web de Maël.
6. **Fichiers trop gros ou binaires** (> ~100 Ko, .xlsx, .bin) : upload web par Maël — c'est son canal habituel et il est fidèle à l'octet. Lui fournir le fichier par SendUserFile + le lien d'upload du bon dossier, puis vérifier l'empreinte après coup.

**Ouverture de session — trois vérifications avant tout travail :**
a. Les 4 empreintes des uploads du 15/08 (jamais formellement vérifiées) : `docs/research/catalogue-evenements/catalogue-evenements-v3-1.csv` → `19e788a303c9d74b0feb8c069245fe66db49462b` · `catalogue-evenements-v3.csv` → `43ec19ff3cbaaea2dad575c4434d7e6acab24388` · `catalogue-evenements-LECTURE.xlsx` → `520d9952a45842efde20038e44e57b14c183f00d` · `docs/research/chronologies/Chrono_Bitcoin_institutionnalisation_V2_8__altcoin_addition_.bin` → `be5f006474284a52bffc21457af79fe5f6f90ff4`. Écart → STOP, le signaler à Maël avant tout.
b. Aucun dossier `_bootstrap/` à la racine (il ne doit pas exister).
c. `.github/workflows/bootstrap-catalogue-0508.yml` : échafaudage mort du 15/08, à supprimer. Tenter `delete_file` UNE fois ; si refusé par le garde-fou, demander à Maël de le supprimer via l'interface web (fichier → ⋯ → Delete file) et continuer sans attendre.

## BLOC B — Fichiers joints et à produire

Joint à la conversation :
- `grille-roles-v0.md` → déposer TEL QUEL en `docs/research/catalogue-evenements/grille-roles-v0.md` (livrable 1 du lot, déjà validé sur le fond par D6).
- le présent prompt → déposer en `docs/audits/PROMPT-COWORK-lot2-statut-roles-q7.md` (provenance, comme le prompt du lot 1).

À produire dans la session :
- `scripts/add_statut_ligne.py` — voir BLOC D §1 (le CSV maître ne se modifie JAMAIS à la main) ;
- `docs/research/catalogue-evenements/catalogue-evenements-v3-2.csv` — v3-1 + colonne `statut_ligne` (~150 Ko → **upload web Maël**, pas le connecteur) ;
- `docs/research/catalogue-evenements/catalogue-roles-v0.csv` — en-tête + les seules lignes du lot d'épreuve ;
- `docs/research/catalogue-evenements/q7-epreuve-lot.csv` — le lot d'épreuve codé (fichier séparé, le maître n'est pas touché) ;
- `docs/audits/etat-lot2-<date>.md` — le rapport court (BLOC D §3).

## BLOC C — Arbitrages de Maël du 15/08/2026 (verbatim, fait autorité)

Je valide que la suite attend des arbitrages, pas du code massif. Voici les décisions pour les quatre points bloquants.

**D4 — colonne `statut_ligne`.** Je valide l'ajout d'une colonne obligatoire `statut_ligne`. Vocabulaire fermé v0 : `validee` (ligne suffisamment sourcée et codée pour être utilisée dans les exports, les matrices, le site ou un article) ; `chantier` (ligne conservée dans le catalogue mais incomplète, à ne pas exporter comme donnée stabilisée) ; `a_arbitrer` (ligne bloquée par une décision Maël) ; `douteuse` (ligne dont la validité empirique ou le rattachement reste incertain) ; `exclue` (ligne documentée pour mémoire mais sortie du corpus actif). Règle : aucune ligne sans `statut_ligne`. Par défaut, une ligne nouvelle ou incertaine est `chantier`, jamais `validee`.

**D6 — forme de la grille de rôles.** Je refuse une grille trop pauvre de type attaquant / résolveur. Je valide une grille de rôles non morale, multi-acteurs et multi-rôles. Rôles v0 : `initiateur` (déclenche ou lance l'acte) ; `exploiteur` (tire parti d'une faille, d'un conflit ou d'une opportunité) ; `affecte` (subit directement l'événement) ; `revelateur` (rend visible, documente ou signale) ; `correcteur` (produit ou propose la correction) ; `validateur` (valide, accepte, confirme ou ratifie) ; `coordinateur` (organise, relaie, synchronise) ; `opposant` (conteste, bloque, refuse ou critique) ; `observateur` (commente, mesure, documente sans agir directement) ; `non_applicable` ; `incertain`. Forme recommandée : ne pas écraser cela dans une seule colonne plate. Utiliser une table ou un bloc secondaire de type `event_id / actor_id ou actor_name / role / confidence / note`. Une vue pivotée pourra être produite ensuite pour les articles ou le site, mais la donnée maîtresse doit permettre plusieurs acteurs et plusieurs rôles par événement.

**D7 — acteur principal dans les crises exploitées-puis-résolues.** Je refuse de faire automatiquement de l'attaquant ou de l'exploiteur l'acteur principal. Règle : pour une crise agrégée « exploitée puis résolue », l'acteur principal est l'entité affectée / gouvernée / mise en crise : protocole, infrastructure, collectif ou écosystème concerné. Les exploiteurs, découvreurs, mainteneurs, correcteurs et validateurs sont codés dans la grille de rôles. Exception : si la ligne n'est pas une crise agrégée mais un acte ponctuel — par exemple une attaque, une publication, un patch, une annonce — alors l'acteur principal peut être l'initiateur de cet acte. Mais cette exception doit dépendre du niveau de granularité de la ligne, pas d'un jugement moral. Donc : crise agrégée → principal = entité affectée / système en crise ; acte ponctuel → principal = initiateur de l'acte ; doute → `acteur_principal = a_arbitrer`.

**D11 — lancement de la passe d'épreuve Q7.** Oui, je valide le lancement de la passe d'épreuve Q7. Mais ce n'est pas encore un gel définitif du vocabulaire. Périmètre : un lot représentatif court, pas un codage massif. Le lot test doit couvrir : Bitcoin et Ethereum ; vulnérabilité et évolution ; huis clos et public ; exploitation / révélation / correction / validation ; au moins un cas où attaquant/résolveur serait trompeur. Sortie attendue : lignes codées ; problèmes rencontrés ; rôles insuffisants ou ambigus ; propositions d'ajustement ; recommandation de vocabulaire v0 gelable ou non. Règle : si la passe Q7 révèle une ambiguïté structurante, on ne force pas le gel. On me pose l'arbitrage.

**Consignes générales.** Pas de génération automatique vers le graphe. Pas de patch vers le graphe dans ce lot. Pas de modification du site. Pas de codage massif. Pas de fusion silencieuse catalogue / graphe. La sortie attendue du lot 2 est : 1. une grille de rôles v0 documentée ; 2. la colonne `statut_ligne` installée dans le modèle ; 3. une passe d'épreuve Q7 limitée ; 4. un rapport court indiquant si le vocabulaire peut être gelé ; 5. les nouveaux arbitrages éventuels à me poser. Le catalogue devient un référentiel scientifique de codage, mais le graphe reste la couche canonique publiée. Toute synchronisation future passera par patch candidat, audit et validation.

## BLOC D — Traduction opérationnelle

### 1. `statut_ligne` — table de passage, par précédence (la première règle qui matche gagne)

Écrire `scripts/add_statut_ligne.py` : lit `catalogue-evenements-v3-1.csv`, écrit `catalogue-evenements-v3-2.csv`, avec `--dry-run`, et ses propres contrôles d'arrivée (346 lignes ; les 29 colonnes d'origine octet pour octet inchangées, comparées champ à champ ; une seule colonne ajoutée ; CRLF conservé ; aucune ligne sans statut ; distribution des statuts affichée). Modèle maison : les `make_vNNN` du dépôt.

1. `exclue` — aucune ligne aujourd'hui (la préhistoire est hors fichier ; la décision D5 de la page d'architecture reste ouverte).
2. `a_arbitrer` — E004 (conflit domaine texte iii / figure iv, note `[CHANTIER domaine…]`) ; plus toute divergence de dates de `table-divergences-dates.csv` NON résolue par les corrections validées du 02/08 (résolues d'après `docs/audits/etat-catalogue-v3-2026-08-05.md` §5 : Litecoin, Frontier, Bitcointalk, NewLibertyStandard — vérifier ligne à ligne avant de classer).
3. `douteuse` — les 21 lignes membres des 13 paires `A_VERIFIER` de `docs/audits/data/doublons-verifies.csv`, jointes par `gid` (attendu : E001, E035, E041, E049 + 17 lignes G — recompter) ; plus BitLaundry (aucune des deux dates confirmée).
4. `chantier` — toute ligne restante portant un marqueur `[CHANTIER` dans N'IMPORTE QUELLE colonne (attention : E019 et E081 le portent dans `type_acte`, pas dans `notes` — le filtre sur `notes` seul en manque 2) ; toute ligne à `codage_statut` vide ; toute ligne `propose(lot1)` — avec, pour ces 40, la mention en rapport : « à re-coder sous D7, hors périmètre lot 2 ».
5. `validee` — le reste, c'est-à-dire les lignes `valide(calibrage)` non happées plus haut (D4 : « sourcée ET codée » — seules les lignes de calibrage y répondent aujourd'hui).

Publier la distribution obtenue dans le rapport. Note d'architecture : D4 impose une valeur UNIQUE par ligne — la précédence ci-dessus tranche de fait la décision D14 de la page d'architecture (E001 est à la fois marquée chantier et membre d'une paire douteuse : la précédence la classe `douteuse`).

### 2. Passe d'épreuve Q7 — protocole

Sélectionner 12 à 15 lignes couvrant les cinq exigences de D11, chacune ayant une source qui ÉNONCE un effet ou des rôles (règle intangible : on ne code que l'énoncé — texte de la thèse dans `assets/MD/`, figure, ou description sourcée du graphe ; sinon `nd`). Candidats à confirmer par lecture des sources — liste indicative, pas fermée : The DAO (crise agrégée Ethereum, LE cas exigé où attaquant/résolveur serait trompeur), CVE-2018-17144 (huis clos, Bitcoin), Value Overflow n°4 (E015), lancement de Frontier (évolution publique), Tether 06/10/2014 (effet énoncé), Peercoin/PoS (altcoin, évolution), halving 2012 (seuil), faillite MtGox (affecté), conflit BIP-16 (opposant).

Pour chaque ligne du lot : coder `effet_prop_monetaires` avec le vocabulaire provisoire (grille v1 Q7 : `usage_paiement · valorisation · unite_compte_etalon · liquidite_convertibilite · conf_methodique/hierarchique/ethique · fongibilite`, direction `+`/`-`/`±` en trait d'union ASCII) ; coder les rôles dans `catalogue-roles-v0.csv` ; poser `acteur_principal` sous la règle D7. Tout dans les fichiers d'épreuve — LE MAÎTRE N'EST PAS TOUCHÉ (la v3-2 n'ajoute que `statut_ligne`).

### 3. Rapport `etat-lot2-<date>.md`

Court : lignes codées ; problèmes rencontrés ; rôles insuffisants ou ambigus ; propositions d'ajustement ; **recommandation gel / pas gel du vocabulaire Q7 et de la grille de rôles** ; les arbitrages à poser à Maël (dont, s'ils surgissent : le vocabulaire de `confidence`, la clé `actor_id` vs `actor_name`, tout trou typologique). Si une ambiguïté structurante apparaît : ne pas forcer le gel, poser l'arbitrage — c'est la règle D11.

### 4. Livraison

Petits fichiers (grille, prompt, script, CSV de rôles, lot d'épreuve, rapport) : connecteur, un par appel, sha vérifié après chaque envoi. `catalogue-evenements-v3-2.csv` (~150 Ko) : SendUserFile à Maël + lien d'upload `https://github.com/Elma-Landro/Website-Mael-Rolland.eth_V.1/upload/codex/create-expand-from-node-planning-documents/docs/research/catalogue-evenements` — puis vérification d'empreinte après son dépôt. Messages de commit : préfixe `docs(catalogue):` ou `feat(scripts):`, corps chiffré, trailers Co-Authored-By et Claude-Session de la session.

### Interdits reconduits

Rien n'est tranché à la place de Maël au-delà de ses arbitrages du BLOC C. Pas de patch vers le graphe. Pas de modification du site. Pas de codage massif (le lot d'épreuve est borné à 15 lignes). Pas de fusion silencieuse catalogue/graphe. Pas de recodage du lot 1 hors lignes d'épreuve. Pas de nouvelle branche, pas de PR, pas de workflow CI. Les lignes incertaines restent `chantier` ou `incertain`, jamais forcées.
