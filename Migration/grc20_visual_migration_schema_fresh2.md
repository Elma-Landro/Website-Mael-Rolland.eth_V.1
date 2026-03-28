# GRC-20 — Schéma de migration visuelle et ontologique
## Cible : vues `Structure de la thèse` et `Monétisation des CM`

Objectif : migrer depuis la logique actuelle vers une logique plus lisible, sans casser l’esthétique historique du site.

## Structure de la thèse
Colonnes :
- Chap.
- Struct.
- Objets
- Gouvern.
- Acteurs
- Concepts
- Réf./Sources

Lignes :
- Intro.
- Chap. I
- Chap. II
- Chap. III
- Concl.
- Multi.

Règles :
- conserver halos, couleurs chapitrales, ambiance pixel / nébuleuse ;
- ne pas supprimer `Chap.` ni `Struct.` ;
- ne pas comprimer `Gouvern.`, `Acteurs`, `Concepts`, `Réf./Sources` ;
- les personnes agissantes restent dans `Acteurs` ;
- les auteurs théoriques, citations, corpus et sources vont dans `Réf./Sources`.

## Monétisation des CM
Colonnes :
- Noyau
- Émission
- Circulation
- Accès
- Usages
- Valorisation
- Stabilisation

Lignes :
- Thèse
- Dispositifs
- Arènes
- Acteurs
- Cas
- Réf.

Règles :
- la vue doit montrer comment des UCN deviennent monnaie ;
- `Noyau` accueille les thèses structurantes ;
- `Émission` : block reward, halving, offre native ;
- `Circulation` : validation, transactions, consensus ;
- `Accès` : exchanges, wallets, passerelles fiat ;
- `Usages` : WordPress, WikiLeaks, Silk Road, marchands ;
- `Valorisation` : liquidité, découverte du prix, marchés ;
- `Stabilisation` : BIP/EIP, DAO Fork, CVE-2018-17144, routines de maintenance.

## Deliverables
- mapping type -> colonne
- mapping type -> ligne
- mécanisme d’overrides par entité
- JSON d’overrides initial
