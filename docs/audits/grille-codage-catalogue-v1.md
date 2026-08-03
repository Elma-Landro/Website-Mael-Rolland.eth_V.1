# Grille de codage — Catalogue d'événements (pointillisme analytique) — v1
Validée par Elma le 19/07/2026 (Q1–Q8). Ancrages : catalogues d'événements (Tilly) ; séquences (Abbott). Base empirique : chronologie n°6 « L'institutionnalisation carnavalesque de l'infrastructure Bitcoin » (`01_chapitre_I.md`, l. 251–257) et chapitre III.

## Décisions actées
- Format : CSV maître (séparateur `;`) + extrait md de contrôle. [Q1]
- Grille complète : noyau + extension, 18 champs. [Q2]
- Seuils/indicateurs inclus, distingués par le champ `nature` — apport revendiqué au-delà du catalogue d'actions tillyen. [Q3]
- Préhistoire (avant le 18/07/2008, chronologie n°1) exclue. [Q4]
- 7e type d'acte ajouté : `innovation_infrastructurelle`. [Q5]
- Académiques/experts repliés dans `medias_connaissance` : le chercheur se traite comme producteur de connaissance indigène de même niveau (symétrie). [Q6]
- Vocabulaire « effets sur propriétés monétaires » : PROVISOIRE — [CHANTIER : à stabiliser par Elma]. Codage uniquement quand l'effet est énoncé par le texte de la thèse, sinon `nd`. [Q7]
- Mention retenue : les cinq premiers domaines recomposent les **22 segments** de Rauchs (2016, p. 118-119) — chap. I, l. 251. [Q8]

## Champs (ordre CSV)
`id ; date ; precision ; nature ; intitule ; phase ; domaine_8 ; systeme ; acteur_principal ; acteur_secondaire ; arene ; type_acte ; type_acte_2 ; effet_prop_monetaires ; crise ; fil ; source ; notes`

1. `id` — Exxx, ordre chronologique (support de séquences).
2. `date` — ISO (AAAA / AAAA-MM / AAAA-MM-JJ), jamais plus précise que la source.
3. `precision` — jour / mois / annee.
4. `nature` — acte / seuil. Pour `seuil` : `acteur_principal` et `type_acte` peuvent valoir `nd`.
5. `intitule` — ≤ 12 mots, au plus près du libellé de la chronologie.
6. `phase` — dérivée de la date : poc (07/2008–03/2012), peche (04/2012–10/2013), maturation (11/2013–début 2020) ; bornes chap. I l. 263, 275, 285.
7. `domaine_8` — i usage réel & financier (vert) · ii traitement des transactions (jaune) · iii portefeuilles & paiements (orange) · iv information & connaissance (bleu foncé) · v conformité aux réglementations nationales (bleu clair) · vi protocole (rouge) · vii Altcoins (rose) · viii autres (violet). Repris du codage de la thèse (l. 251) ; suffixe `*` = attribution par définition du domaine, couleur non vérifiée dans le texte/figure. La grille se superpose au codage Rauchs-Rolland, elle ne le remplace pas.
8. `systeme` — bitcoin / ethereum / altcoin / transversal.
9. `acteur_principal` (et 10. `acteur_secondaire`) — core_devs (développeurs de protocole, trans-protocole) · mineurs · entrepreneurs_exchanges · institutions_financieres · regulateurs_etats · medias_connaissance (presse + académiques/experts, cf. Q6) · communautes_forums. Règle : rôle tenu dans l'acte, pas biographie. Acteur hors typologie (ex. attaquant anonyme, retrait de concepteur) → `nd` ou [CHANTIER], jamais de catégorie créée en silence.
11. `arene` — on_chain · depots_de_code · listes_forums · reseaux_sociaux · marches_plateformes · presse_medias · instances_publiques · evenements_conferences · entreprises_services. Règle : lieu d'effectivité de l'acte.
12. `type_acte` (et 13. `type_acte_2`) —
   - innovation_protocolaire : création/modification de règles ou d'implémentations, surcouches et lancements de protocoles inclus ;
   - innovation_infrastructurelle : dispositifs organisationnels/techniques hors protocole et hors instruments financiers (pools, wallets, mixage, fondations, procédures) ;
   - qualification_publique : acte discursif qualifiant/déqualifiant sans effet juridique contraignant ;
   - regulation : production ou application de règles par des autorités publiques (frontière avec la précédente = effet contraignant) ;
   - adoption : extension de la sphère d'usage et d'accès ;
   - incident : défaillance subie (frontière avec innovation = subi vs délibéré) ;
   - financiarisation : instruments, marchés, bourses et acteurs financiers (ICO comprises).
14. `effet_prop_monetaires` — [PROVISOIRE, Q7] usage_paiement · valorisation (usage financier — jamais « réserve de valeur » comme fonction stricto sensu) · unite_compte_etalon · liquidite_convertibilite · conf_methodique / conf_hierarchique / conf_ethique · fongibilite ; direction (+/−/±) ; sinon `nd`. Codé uniquement sur effet énoncé par le texte.
15. `crise` — non / oui (+ n° de l'inventaire de la thèse quand le texte le donne, cf. chap. III l. 181–249). Si oui : recensement seul, aucune analyse (anti-redondance SASE).
16. `fil` — étiquette de séquence contrôlée (genese, acces-usage, portefeuilles, minage, marches, mediatisation, conformite, representation, altcoins, ico, ethereum, stablecoins, financiarisation, scaling, crises-protocolaires, dao, peche, gouvernance).
17. `source` — fichier + ligne(s) (ch.I l.XXX / ch.III l.XXX / n.XX pour note de bas de page) ; `fig. n°6` = donnée issue de la figure (PNG V2_8_1) ; obligatoire.
18. `notes` — ambiguïtés, [CHANTIER], renvois.

## Règles transversales
R1 unité d'événement : occurrence discrète, datée, attribuable, tracée (Tilly). R2 inclusion : présence dans chronologie n°6/voisines (chap. I) ou chap. III ; filtre de pertinence infrastructurelle de la thèse. R3 périmètre : 18/07/2008 → début 2020. R4 anti-invention : aucune date, aucun événement au-delà des sources ; divergences texte/figure signalées, jamais tranchées. R5 crises : flag + recensement (analyse = SASE) ; Scaling Debate : recensé via chap. I seulement, jalons fins au chap. II §II.3.3 hors périmètre de ce prompt. R6 séquences (Abbott) : id + date + precision garantissent l'ordonnançabilité ; `fil` permet la reconstruction d'enchaînements.

## Vigilances anti-redondance
Crises (CVE-2018, The DAO) → SASE ; Scaling Debate → Économie et institutions 2017 ; carnavalesque → Revue de la régulation ; principes de construction des figures → BMS. Le catalogue est un instrument, pas une prose : il recense, il n'analyse pas.
