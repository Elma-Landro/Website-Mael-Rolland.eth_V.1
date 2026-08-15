# État — Codage analytique, Lot 1 (crises numérotées) — 05/08/2026

## Livré
- `catalogue-evenements-v3-1.csv` — maître, 345 lignes, **2 colonnes ajoutées** : `codage_statut` (`valide(calibrage)` / `propose(lot1)` / vide) et `codage_justif` (source + règle appliquée, ligne à ligne). Remplissage descriptif global : `systeme` complété sur 175 lignes (bitcoin/ethereum/altcoin par mots-clés — descriptif, pas analytique).
- `lot1-crises-a-valider.csv` — **40 lignes**, 38 crises numérotées (n°1→…) + 2 non numérotées, colonnes réduites pour annotation directe.

## Règles appliquées (chaque ligne cite la sienne dans `codage_justif`)
- `type_acte=incident` pour toute crise ; `type_acte_2=innovation_protocolaire` quand un correctif protocolaire est impliqué (scission, inflation, CVE).
- Crise **exploitée** (vol, attaque, DoS) → `acteur_principal=nd` (attaquant hors typologie, précédent E065), `acteur_secondaire=core_devs` (réponse) ; arène `on_chain`.
- Bogue **découvert et corrigé sans exploitation** → `acteur_principal=core_devs` (précédent E015) ; arène `depots_de_code`.
- Source de codage : wiki des crises (ch.III l.181–249) via graphe v97 (attributs `crisisType`, `exploited`) + intitulé.
- Rien de validé : tout le lot est `propose(lot1)`. Recensement seul — analyse des crises = SASE.

## Répartition du lot
18 nd/on_chain (exploitées) · 18 core_devs/depots_de_code (correctifs) · 4 core_devs/on_chain (scissions-inflation résolues par les devs, dont Value Overflow n°4, alignée sur le précédent E015 du calibrage).

## À trancher par Elma (2 décisions, puis intégration)
1. **Convention attaquant/résolveur** : pour une crise exploitée *puis* résolue, l'acteur principal est-il l'attaquant (`nd`, hors typologie — précédent E065) ou le résolveur (`core_devs` — précédent E015) ? Les deux précédents du calibrage coexistent ; le lot suit E065 sauf Value Overflow. Une règle unique est nécessaire avant le lot 2.
2. **Q7 (proposition de gel)** : figer le vocabulaire provisoire comme v1 — `usage_paiement · valorisation · unite_compte_etalon · liquidite_convertibilite · conf_methodique/hierarchique/ethique · fongibilite`, direction `+/−/±`, codage **uniquement sur effet énoncé** (texte, figure, ou description sourcée du graphe), `nd` sinon. Un mot suffit pour geler ou amender.

## Reste
211 lignes à coder après ce lot (lots 2+ : domaine (ii) minage, puis figure F, puis graphe résiduel). 80 lignes sans domaine (hors frise). 13 paires A_VERIFIER inchangées — le lot 1 en contient au moins une (G001 ↔ E015, même crise n°4 sous deux libellés).
