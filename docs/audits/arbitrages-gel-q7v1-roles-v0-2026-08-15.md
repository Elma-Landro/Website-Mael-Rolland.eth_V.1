# Arbitrage de gel — Q7 v1 et grille de rôles v0 — 15/08/2026

Verbatim du message reçu en session Cowork le 15/08/2026, en réponse à `docs/research/catalogue-evenements/vocabulaire-q7-v1-proposition.md` (§8) et à la mini-passe `q7-epreuve-lot-v2.csv`. **Fait autorité** — même statut que `arbitrages-lot2-A1-A5-2026-08-15.md`. Ce message ACTE LE GEL : le vocabulaire Q7 v1 et la grille de rôles v0 sont gelés à compter de cette date.

---

Réponses Maël — Gel Q7 v1 / grille de rôles v0

Fichier v3-2 :
`catalogue-evenements-v3-2.csv` est désormais en ligne.
Empreinte vérifiée : `1b4b3aa4f74df0829ffbb149d22814e11e4324d5`.
Taille : 146 182 octets.
Le point d’intendance est donc clos.

1. Gel Q7 v1

Je valide le gel du vocabulaire Q7 v1 tel que proposé.

Je valide aussi les deux conventions résiduelles :

r1 — `mode nd` admis pour les seuils.
Oui. Lorsque l’événement est un seuil, un état agrégé ou une mesure sans mode d’action clairement qualifiable, `mode nd` est acceptable. Il doit rester un codage contrôlé, pas une case paresseuse.

r2 — `±` avec note obligatoire pour une mise en cause non activée.
Oui. Je préfère `±` à `-` dans ces cas, parce qu’une mise en cause non activée n’a pas le même statut analytique qu’une dégradation effective. Le signe `±` doit toujours être accompagné d’une note expliquant l’ambivalence.

Donc :
- Q7 v1 est gelé ;
- `integrite_monnayage` entre dans le vocabulaire gelé ;
- la convention multi-effets est validée ;
- `±` est autorisé mais toujours justifié ;
- plus de renommage silencieux après ce gel.

Toute modification future devra passer par :
- Q7 v2 ;
- ou table de correspondance v1 → v2 ;
- ou arbitrage explicite.

2. Grille de rôles v0

Je ratifie formellement la grille de rôles v0 comme gelée.

Conséquence :
- plus de renommage silencieux des rôles ;
- ajout possible seulement par version ultérieure ;
- maintien des valeurs `non_applicable` et `incertain` ;
- conservation de la table longue `event_id / actor_id ou actor_name / role / confidence / note`.

La grille de rôles v0 devient donc stable pour le codage du catalogue.

3. Suite immédiate

Mettre à jour les documents de lot pour inscrire :
- Q7 v1 gelé ;
- grille de rôles v0 gelée ;
- fichier v3-2 présent et vérifié ;
- mini-passe Q7 réussie sur les 14 lignes ;
- aucun codage massif encore lancé.

Ne pas pousser vers le graphe.
Ne pas générer de patch graphe.
Ne pas modifier le site.
Ne pas fusionner catalogue et graphe.
Le prochain lot peut être un codage contrôlé, mais seulement sur la base des vocabulaires gelés.
