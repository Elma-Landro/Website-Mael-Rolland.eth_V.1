# 04 — Contrôle sémantique : typage et cohérence avec la thèse

**Date** : 2026-08-02
**Sources lues** : `assets/MD/01_chapitre_I.md` (l. 275, 279, 281, 287, 289, 293, 373, 391, 393, 399), `assets/MD/03_chapitre_III.md` (l. 87, 219, 223, 449)
**Mode agent** : A

Objet : vérifier que chaque ajout est cohérent avec la démonstration de la thèse, et lui attribuer le bon type. Le risque à écarter est l'erreur de catégorie — transformer un état de marché en acte infrastructurel, ou un acte de maintenance en crise protocolaire.

## Les lignes `nature=seuil` — ne pas ajouter

Dix lignes du CSV sont des `seuil` : cinq paliers de cours, deux statistiques d'activité illicite, trois autres. La question était de savoir si elles pouvaient devenir des `InfrastructureEvent`. **Non, pour deux raisons distinctes.**

### Les paliers de cours : le graphe a déjà un type pour ça

Quatre des cinq existent comme `PriceWindow`, avec un attribut `priceUSD`. Les ajouter comme `InfrastructureEvent` dupliquerait le contenu **et** casserait la convention.

Et le typage serait faux sur le fond. La phrase qui ouvre le passage de la l.293 tranche : « Au développement matériel de ces infrastructures **répond** celui de la valeur de leurs UCN ». Le cours est le terme **dépendant** — la réponse, pas l'acte. La l.281 fait le même geste : le cours « permet de démontrer encore sa dépendance aux aléas infrastructurels exogènes ». Il est l'indicateur d'événements infrastructurels, jamais l'un d'eux.

Le CSV le dit d'ailleurs lui-même : toutes ses lignes `seuil` portent `type_acte=nd`.

**Seul E070 est réellement absent** (franchissement durable des 1000 $ début 2017), et la thèse l'appuie mot pour mot en l.293 : « son cours stagne en dessous des 1000 $, seuil qu'il ne dépasse qu'en début d'année 2017 ». Son type correct est **`PriceWindow`**, pas `InfrastructureEvent` — donc **hors du périmètre déclaré de cette PR**. Signalé, non ajouté.

### Les statistiques d'activité illicite : refus plus ferme

E038 (51 % on-chain, 2013) et E043 (< 1 %, fin 2013-2018) ne sont pas des événements du tout : ce sont des **caractérisations d'un régime transactionnel**, c'est-à-dire des propriétés définitionnelles des phases elles-mêmes. Le graphe les porte déjà comme telles, sur deux `Concept` sourcés Tasca & Liu 2018 et Chainalysis 2019.

S'y ajoute une raison proprement rollandienne. La l.281 contient un avertissement méthodologique explicite :

> « **Attention aux effets loupe**, pendant que Bitcoin sert à des activités illégales, s'en développent d'autres à visées légales, dont l'essor on chain éclipse les premières. »

Promouvoir « 51 % de l'activité on-chain est pécheresse » au rang de nœud autonome dans un graphe visuel produirait exactement la distorsion que l'auteur signale. Si ces chiffres doivent gagner en visibilité, leur place est en attribut ou en `SourceQuote` sur les concepts de régime existants — pas en événement.

## Typage des six ajouts

Aucun n'est un `CrisisEvent`. Tous sont des `InfrastructureEvent`.

| id | Type | Justification | Confiance |
|---|---|---|---|
| **E069** PR 9049 | `InfrastructureEvent` | voir ci-dessous | Élevée |
| **E040** WP Ethereum | `InfrastructureEvent` | Acte fondateur du second terrain. l.**393** : « Buterin rédige la première version du WP d'Ethereum fin novembre 2013 » — plus précis que la l.399 citée par le CSV. Seule une `Reference` bibliographique existait. | Élevée |
| **E061** Testnet Olympic | `InfrastructureEvent` | l.399 verbatim : « "Olympic", dénomination de la neuvième itération du testnet, en date du 9 mai 2015, établit la dernière preuve de concept avant le lancement ». Jalon de développement, ni crise ni controverse. | Élevée |
| **E036** Second Bitcoin WP | `InfrastructureEvent` | l.373 verbatim : « fait suite à la publication par J.R. Willet, dès janvier 2012, du WP modestement intitulé "The Second Bitcoin Whitepaper" ». Origine de la chaîne métaprotocole → ICO → OP_RETURN War déjà présente. | Élevée |
| **E060** Pivot blockchain | `InfrastructureEvent` | l.289 : « L'année 2015 est bien charnière… l'important ne serait pas les UCN… mais une "technologie de blockchain"… Nombreuses sont les entreprises de l'écosystème à pivoter ». Portée matérielle, pas seulement discursive. Le CSV le classe `type_acte=qualification_publique` : c'est un acte de qualification, pas une crise. | Moyenne |
| **E034** Coinbase | `InfrastructureEvent` | La réintermédiation est le contenu définitionnel de la phase de péché (l.275). Kraken, Ripple, Binance et MtGox ont leur événement de fondation ; Coinbase, non. **Réserve** : la date vient de la figure n°6 ; le texte ne narre pas la fondation, il ne cite Coinbase que comme indicateur (l.287, « le nombre de comptes ouverts »). | Moyenne sur le type, moyenne sur la date |

### Une convention qui autorise les événements de publication

Le livre blanc de Bitcoin existe **à la fois** comme `Reference` (Nakamoto 2008) et comme `InfrastructureEvent` (`Publication du WP Bitcoin (mailing list)`). Le graphe compte 8 événements de publication de ce genre, et une relation dédiée `source of` qui va de la `Reference` vers l'événement.

Ajouter les événements de publication des WP Willett et Ethereum **suit donc la convention au lieu de la casser**. Les deux `Reference` cibles existent déjà et sont câblées par `source of`.

## E069 — pourquoi c'est l'ajout le plus important

Ch.III l.87 ouvre toute l'étude de cas CVE-2018. Corallo propose de retirer une vérification « postulant à tort que la vérification redondante précédente existe encore (ce qui n'est plus le cas depuis la PR 2224) » ; les mesures montrent « environ 0,5-0,7 ms » de gain ; « l'optimisation est acceptée et fusionnée au répertoire logiciel principal. La première itération du bogue CVE 2018 dans les versions Bitcoin Core 0.14.0 est introduite ainsi. Désormais, **sans qu'aucun acteur n'y prête attention**, les nœuds fonctionnant sur cette version sont devenus vulnérables. »

C'est la charge démonstrative du chapitre : le bogue le plus grave de l'histoire de Bitcoin est produit par un travail de gouvernance **ordinaire, relu, mesuré, consensuellement accepté**. Sans PR 9049 comme nœud, le graphe affirme la crise mais ne peut pas montrer qu'elle a été *fabriquée par la maintenance courante*.

### `InfrastructureEvent`, pas `CrisisEvent` — trois raisons

1. **La thèse distingue les procédures.** Ch.III l.449 : la procédure **BIP** couvre des changements qui « sont en eux-mêmes des crises » ; la procédure **PR** est le dispositif emprunté au logiciel libre pour les modifications incrémentales. PR 9049 est une PR. La typer `CrisisEvent` effacerait une distinction que la thèse construit explicitement.
2. **Au moment de l'acte, il n'y a pas de crise.** La périodisation fait de l'insémination la phase où aucune crise n'existe socialement. Rétroprojeter la crise sur l'acte détruit la latence qui fait la valeur analytique du cas.
3. **Le type `CrisisEvent` est peuplé de crises manifestes** — 55 CVE, crises BIP et forks. PR 9049 y serait indiscernable d'une vulnérabilité divulguée.

### Le lien vers la crise

Pas une relation de déclenchement : le déclencheur est la divulgation responsable de septembre 2018, et le graphe le dit lui-même par son attribut `triggerMode: "divulgation responsable (huis clos)"`. Confondre la PR avec le déclencheur écraserait deux phases distinctes.

La sémantique juste est celle d'une **origination latente** — causale mais non manifeste, séparée de son effet par près de deux ans, sans conscience d'aucun acteur. La relation retenue est **`precursor of`**, de PR 9049 vers `Bitcoin CVE 2018-17144` : elle existe déjà dans le graphe (11 usages) et n'affirme ni déclenchement ni causalité directe.

## Recommandations non appliquées — hors périmètre

Trois pistes, sérieuses mais qui excèdent le mandat de cette PR et relèvent d'un arbitrage :

1. **La chaîne de `CrisisPhase` de CVE-2018-17144 n'a pas de phase d'insémination.** Elle commence à « Signalement et divulgation responsable » (`timeStart: 2018-09-17`), alors que l'attribut `phases` de l'entité annonce lui-même « 1. Insemination/gestation ». Le graphe ampute le cas central de la phase qui le rend démonstratif — la séquence The DAO, elle, s'ouvre correctement par « DAO — Insémination / gestation ». Le graphe date d'ailleurs déjà l'insémination d'autres CVE (CVE-2012-3789 porte `date: 12/05/2012`, « Date d'insémination »).
2. **PR 9049 n'a introduit que l'itération plantage/déni de service.** Ch.III l.87 poursuit : le faux monnayage par double dépense vient de « l'articulation de deux PR distinctes : les PR n° 10195 et n° 10537, discutées entre avril et juin 2017 ». L'asymétrie de relecture entre elles (14 participants / 10 relecteurs contre 5 / 2) est elle-même un matériau de l'argument sur la division du travail. **Ces deux PR ne figurent pas dans le CSV** : les ajouter serait inventer des événements hors source, ce que le mandat interdit.
3. **E070** mérite une `PriceWindow`, pour compléter une série qui en compte déjà quatre.
