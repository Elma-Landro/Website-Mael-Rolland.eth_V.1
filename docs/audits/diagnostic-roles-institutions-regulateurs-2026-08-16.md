# Diagnostic — les lignes validées sans rôle sur `institutions_financieres` et `regulateurs_etats` — 16/08/2026

Mini-lot de **diagnostic**, ouvert par la décision Maël du 16/08/2026 après le lot visible 2. Il instruit, il ne corrige pas : **aucune ligne de rôle n'a été créée, aucune cellule du catalogue maître n'a été touchée, aucun rôle n'a été versé.** Sortie : ce rapport et son fichier de preuve.

| pièce | empreinte |
|---|---|
| `docs/audits/data/roles-institutions-regulateurs-diagnostic-v1.csv` (8 lignes) | voir §7 |

## 1. La question, et sa réponse

> *Quand ces acteurs sont `acteur_principal`, sont-ils vraiment sans rôle, ou bien la grille n'a pas encore été appliquée ?*

**La grille n'a pas été appliquée.** Ce n'est pas une hypothèse de lecture : c'est un croisement, et il ne laisse pas de place au doute.

| `codage_statut` | lignes | validées | **validées portant un rôle** |
|---|---:|---:|---:|
| `valide(lot3)` | 30 | 30 | **30 — soit 100 %** |
| `valide(calibrage)` | 82 | 65 | **7 — soit 11 %** |
| `propose(lot1)` | 10 | 0 | 0 |
| *(vide)* | 223 | 0 | 0 |

Toute ligne passée par une **passe de rôles** en porte un : les 30 lignes du lot 3, sans exception. Les 7 lignes de calibrage qui en portent sont exactement les lignes de la **passe d'épreuve Q7 du lot 2** (E015, E029, E044, E052, E064, E065, E077). Aucune passe de rôles n'a jamais couvert les 58 autres lignes validées par le calibrage.

Les **8 lignes** que tu vises appartiennent toutes à ce groupe : toutes `valide(calibrage)`, toutes antérieures à la grille v0 — qui n'existait pas encore, ayant été **gelée le 15/08/2026**. Il n'y a donc aucun « acteur sans rôle » à expliquer : il y a un périmètre de codage qui ne les a pas encore atteintes.

Corollaire à ne pas perdre de vue : la matrice acteurs × rôles du lot 2 ne montre pas que les institutions financières et les régulateurs ne jouent aucun rôle dans la thèse. Elle montre **où la grille est passée**. C'est une carte du codage avant d'être une carte du terrain, et il faut la lire comme telle tant que la couverture est de 13 %.

## 2. Les huit lignes, et ce que la grille permet d'en dire

Les rôles proposés ci-dessous sont **des propositions à arbitrer, pas des codages**. Chacune est ancrée soit sur le libellé gelé de la grille v0, soit sur un précédent **déjà codé** dans le catalogue — jamais sur une intuition.

| id | date | intitulé | acteur principal | source | rôle possible v0 | conf. | recommandation |
|---|---|---|---|---|---|---|---|
| E073 | 2017 | Futures Bitcoin (CBOE et CME) | institutions_financieres | ch.I l.289 | `initiateur` | haute | **rôle à ajouter** |
| E042 | 2013 | Nasdaq publie des cotations agrégées | institutions_financieres | ch.I l.289 | `validateur` | moyenne | **rôle à ajouter** |
| E058 | 2015 | NYSE publie des cotations | institutions_financieres | ch.I l.289 | `validateur` | moyenne | **rôle à ajouter** |
| E027 | 2011-06-04 | PayPal retire de Bitcoinmarket.com | institutions_financieres | ch.I n.75 l.609 | `opposant` | moyenne | **rôle à ajouter** |
| E037 | 2012-10-29 | Rapport BCE *Virtual Currency Schemes* | regulateurs_etats | ch.I l.281 + fig. n°6 | `revelateur` | moyenne | **rôle à ajouter** |
| E060 | 2015 | Pivot blockchain sans les UCN | institutions_financieres | ch.I l.289 | `opposant` *ou* `observateur` | basse | **arbitrage requis** |
| E059 | 2015 | Levée record Coinbase (75 M $) | institutions_financieres | ch.I n.90 l.639 | `validateur` | basse | **ligne à revoir** |
| E032 | 2012 | Entrée du capital-risque (2,1 M $) | institutions_financieres | ch.I n.90 l.639 | `non_applicable` | moyenne | **ligne à revoir** |

Le motif de chacune, en clair :

- **E073 — `initiateur`, le seul cas net.** CBOE et CME créent un instrument qui n'existait pas. C'est le libellé exact de la grille : « *l'acte n'existerait pas sans lui* ». Précédent : E052, où Tether Ltd est `initiateur` pour l'émission du premier stablecoin dollar.
- **E042 et E058 — `validateur`.** Coter n'est pas produire. La grille définit `validateur` comme un « *acte d'acceptation distinct de la production* » ; une place de marché qui publie des cotations accepte institutionnellement un objet qu'elle n'a pas fabriqué. Précédent : E044, où BitGo et les services de portefeuilles sont `validateur` pour l'intégration de BIP16. Les deux lignes sont strictement parallèles — même acte, même arène, même source : **si E042 bascule, E058 bascule avec elle.**
- **E027 — `opposant`.** PayPal retire son service : un blocage, pas une création. La grille donne `opposant` = « *conteste, bloque, refuse* », opposition agissante. La ligne code elle-même `liquidite_convertibilite(-)`, effet d'un acte de refus.
- **E037 — `revelateur`.** La note de ligne enregistre un effet aval : « *pousse à l'émergence de services de conformité* ». C'est exactement le critère par lequel la grille sépare `revelateur` d'`observateur` — « *après lui, les autres savent* ». Précédent : E064, où les auteurs du papier d'alerte sur The DAO sont `revelateur`, et non `initiateur` de leur propre publication.
- **E060 — arbitrage.** La note dit « *disqualification des UCN* » : adopter la technique en récusant la monnaie est une prise de position, pas un commentaire. `opposant` si tu juges la manœuvre agissante, `observateur` sinon. La grille fait dépendre ce partage de **l'effet** — et l'effet n'est pas codé sur cette ligne (`nd`). Je ne peux pas trancher sans forcer.
- **E059 — ligne à revoir avant tout rôle.** L'agent de la levée est Coinbase, porté ici en acteur **secondaire** ; l'acteur principal désigné est le financeur. Si D7 est réappliquée et le principal corrigé, les deux rôles s'inversent (Coinbase `initiateur`, financeurs `validateur`). Poser un rôle avant de vérifier l'acteur principal reviendrait à graver l'ordre actuel.
- **E032 — ligne à revoir, question préalable.** Agrégat annuel sans agent identifié (2,1 M cumulés, note « *année à cheval poc/pêche* »). La ligne porte `nature = acte` mais se lit comme un seuil. **Acte ou seuil ?** Le rôle suit cette réponse, il ne la précède pas. En l'état, `non_applicable` au titre du §2 de la grille (« *certains seuils* »).

## 3. Ce que le diagnostic fait remonter, et qui dépasse ces huit lignes

En cherchant le rôle de ces huit lignes, une question de sémantique de la grille est apparue — et elle commande le codage de bien plus que huit lignes.

**Le rôle qualifie-t-il l'acteur relativement à l'acte codé, ou relativement à la situation gouvernée ?** Pris à la lettre de la grammaire, l'auteur d'une publication est toujours l'`initiateur` de sa publication — et alors `initiateur` deviendrait automatique sur toute ligne `qualification_publique`, sans rien apprendre.

**Le catalogue a déjà tranché en pratique, et je m'y suis conformé** : sur E064, les auteurs du papier d'alerte sont codés `revelateur`, pas `initiateur` ; sur E052 et E063, `initiateur` est réservé à qui crée quelque chose qui n'existait pas. La règle implicite, lisible dans les codages existants, est donc : **le rôle dit la fonction dans la situation, pas la grammaire de l'acte.** Elle n'est écrite nulle part. Elle mériterait une ligne dans la grille v0 — ce serait une précision de guide de codage, pas une modification du vocabulaire gelé, donc sans effet sur le gel.

## 4. Les trois lignes `douteuse` du même groupe, pour mémoire

Ta demande porte sur les 8 validées. Le même acteur principal `regulateurs_etats` porte 3 lignes supplémentaires, toutes `douteuse`, hors périmètre de ce diagnostic mais utiles à connaître : **E041** (Saisie de Silk Road, FBI) et **G011** (Fermeture Silk Road, doublon signalé de E041, G052, G054 et F021) — même fait, non fusionné ; **E049** (Audition au Sénat américain). Elles ne recevront de rôle qu'après résolution de leur statut : par la règle D4, une ligne non validée n'exporte rien au maître.

## 5. Ce que je n'ai pas fait

Aucun rôle ajouté à `catalogue-roles-v0.csv`. Aucune cellule modifiée dans `catalogue-evenements-v3-3.csv`. Aucun acteur principal corrigé, y compris sur E059 où je pense qu'il devrait l'être. Aucun statut changé. Aucune ligne hors périmètre R3 tranchée. Aucun vocabulaire gelé touché — et en particulier, la précision de sémantique du §3 est **proposée**, pas appliquée.

## 6. Ce qui reste à décider

1. **Les 5 rôles nets** (E073, E042, E058, E027, E037) : les verses-tu ? Ils passeraient par un applicateur, comme toute écriture au catalogue — jamais à la main.
2. **E060** : `opposant` ou `observateur` ?
3. **E059** : l'acteur principal doit-il être corrigé avant de poser un rôle ?
4. **E032** : acte ou seuil ?
5. **La sémantique du §3** doit-elle être écrite dans la grille v0 comme guide de codage ?

## 7. Fichier de preuve

`docs/audits/data/roles-institutions-regulateurs-diagnostic-v1.csv` — 8 lignes, séparateur `;`, CRLF, 14 colonnes : `id`, `date`, `intitule`, `statut_ligne`, `codage_statut`, `acteur_principal`, `arene`, `type_acte`, `source`, `role_possible_v0`, `confiance_proposee`, `precedent_invoque`, `recommandation`, `motif`. Aller-retour d'écriture et de relecture vérifié : les 8 lignes se relisent à l'identique.

À lire **avec ce rapport**, jamais seul : la colonne `role_possible_v0` est une proposition adossée à un précédent, pas un codage.
