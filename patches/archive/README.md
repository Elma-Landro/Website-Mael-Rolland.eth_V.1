# patches/archive — patchs retirés de la circulation

## `grc20_anchor_overrides_targeted.json`

**Archivé le 2026-08-07 sur arbitrage de Maël Rolland** (Arbitrage Queue,
lot 1, Q7 — option A), sans application ni réévaluation.

Motifs, établis par l'inventaire `docs/audits/data/candidate-patch-inventory-v1.csv`
et l'audit `docs/audits/candidate-patch-preflight-lab-v1.md` (§ 2, § 8.4) :

- **probablement périmé** : base déclarée v93, antérieure aux réalignements
  d'ancrage v108–v109 qui ont refait ce travail par une autre voie
  (réalignement des `section_key` de relations puis des charges d'ancrage) ;
- **hors de tous les dialectes** du dépôt : 10 entrées `safe_fix` /
  `proposed_review` sans clé d'opération — aucun applicateur ni validateur
  ne sait le lire ;
- **attributs inconnus** : `primaryChapter` / `secondaryChapters` absents du
  registre des propriétés et de v110 (0 porteur).

Condition de réouverture, fixée par l'arbitrage : une preuve ultérieure que
ces 10 entrées portaient un jugement d'auteur que v108/v109 n'a pas repris.
Sans cette preuve, le fichier reste une archive.
