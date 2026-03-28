# Overrides batch 2 — concepts, hiérarchie d’acteurs et canonisation

Ce batch complète le batch 1 avec une passe sur :
- les **concepts** centraux, secondaires, techniques et formules natives ;
- la **hiérarchie des acteurs** (Institution / Organization / StakeholderGroup / StakeholderCategory / Person) ;
- les **doublons** et variantes lexicales ;
- les **faux concepts** et **faux groupes**.

## Nombre de lignes
75

## Objectifs
1. Remonter les concepts vraiment structurants au rang de `CoreConcept`.
2. Déplacer les concepts principalement élaborés dans Chap. II ou Chap. III hors de l’Intro quand l’Intro n’est qu’un lieu d’annonce.
3. Transformer les titres de section déguisés en `Concept` en `ChapterSection`.
4. Reclasser les entreprises, institutions et coalitions actuellement écrasées dans `ActorGroup`.
5. Distinguer slogans / formules natives, conflits de gouvernance, propositions protocolaires et concepts analytiques.

## Règles de traitement
- `SAFE_FIX` : appliquer directement.
- `KEEP_CONFIRM` : garder mais documenter.
- `REVIEW` : vérifier dans le manuscrit / code avant commit définitif.
- `RETYPE_REVIEW` : retypage conseillé.
- `MERGE_REVIEW` : fusion / canonisation conseillée.

## Noyaux de ce batch
### Concepts
- `Monétisation`, `Développement carnavalesque`, `Infrastructure sociotechnique`, `Gouvernance polycentrique`, `Nominalisme monétaire non étatiste`, `Mise en crise / Remise en ordre` doivent former un noyau conceptuel plus clair.
- Les doublons accentués / non accentués doivent être fusionnés.
- `Code is Law`, `Not your keys, not your coins`, `Fiatsplaining` doivent sortir du grand sac `Concept` si possible.

### Acteurs
- les banques centrales, universités et centres de recherche doivent sortir de `ActorGroup` vers `Institution`.
- les entreprises / plateformes / fondations doivent sortir de `ActorGroup` vers `Organization`.
- les coalitions empiriques (`Core Developers`, `Whitehat Group`, etc.) doivent devenir `StakeholderGroup`.

### Vue
Ces corrections doivent améliorer particulièrement :
- `Structure de la thèse`
- `Qui gouverne réellement ?`
- les focus `Acteurs`, `Gouvern.` et `Concepts`.
