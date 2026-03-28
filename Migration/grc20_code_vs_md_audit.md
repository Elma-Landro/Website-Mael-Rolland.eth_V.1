# Audit ciblé — écarts entre code, rendu et inventaire MD

## Objet
Cette note synthétise les écarts les plus importants entre :
1. la structure textuelle de la thèse telle qu’affichée dans `graphe.html`,
2. l’inventaire d’entités `entities_inventory_v90.md`,
3. le comportement observé des vues / focus.

## Constat central
Le graphe souffre de deux familles d’erreurs distinctes :

### A. Erreurs de données / d’ancrage
Certaines entités sont ancrées dans le mauvais chapitre ou la mauvaise bande.

### B. Erreurs de rendu / de filtrage
Le mode `Focus` propage trop fortement les voisins relationnels, ce qui écrase l’ancrage textuel principal.

---

## 1. Structure de vérité tirée de la thèse

### Chapitre I
Lieu principal de :
- l’émergence de Bitcoin et Ethereum comme infrastructures sociotechniques ;
- I.2 : développement infrastructural au-delà du protocole Bitcoin ;
- improvisations d’acteurs, médiations, services, constellation d’altcoins ;
- I.3 : rupture Ethereum / altcoins / recompositions d’alliances.

### Chapitre II
Lieu principal de :
- la controverse monétaire ;
- le nominalisme non étatiste attentif aux usages ;
- la clarification de la gouvernance hors normativité ;
- la gouvernance polycentrique ;
- les stakeholders / shareholders ;
- le Scaling Debate comme scène de clarification des camps et de la gouvernance.

### Chapitre III
Lieu principal de :
- la gouvernance discrète dévoilée par les crises ;
- Bitcoin CVE 2018-17144 ;
- politique de crises ;
- huis clos routinier ;
- The DAO ;
- hard fork / remise en ordre / scission.

---

## 2. Écarts repérés dans l’inventaire MD

## 2.1 CVE-2018-17144 mal ancrée
L’inventaire assigne :
- `Bitcoin CVE 2018-17144` en `Chap.II` (`CrisisEvent`)
alors que la structure de thèse fait de cette crise un objet central du chapitre III.

Même problème pour :
- `GovernanceProcess — CVE-2018-17144 résolution` : pas d’ancrage chapitral explicite.

## 2.2 Scaling Debate incohérent selon les types
Le corpus montre :
- `GovernanceProcess — Bitcoin Scaling Debate (2015-2017)` en `Chap.II`
- `Scaling Debate (2015-2017)` comme conflit/gouvernance plutôt chapitre II
- mais `Scaling Debate` apparaît aussi en `Chap.III` parmi les `CrisisEvent`

=> incohérence de traitement : clarification de gouvernance (Chap.II) vs crise (Chap.III).

## 2.3 Ethereum émergence / lancement mal aspirés vers Chap.III
Plusieurs `InfrastructureEvent` liés à l’émergence d’Ethereum sont ancrés en `Chap.III`, alors que la structure du manuscrit situe l’émergence d’Ethereum dans `Chap. I`, surtout I.3 :
- `Ether Genesis Sale (ICO Ethereum 2014)`
- `Frontier (lancement mainnet Ethereum, juillet 2015)`
- `Lancement d'Ethereum (Frontier, 30 juillet 2015)`
- `Levee de fonds Ethereum en BTC (2014)`

## 2.4 Développement infrastructural de Bitcoin dispersé hors Chap.I / I.2
Le chapitre I.2 est explicitement le lieu du développement infrastructural au-delà du protocole Bitcoin.
Or de nombreux `InfrastructureEvent` comparables sont assignés à `Chap.II` ou sans chapitre :
- `BitcoinMarket exchange launch`
- `Bitcoin Foundation creation`
- `Migration du code Bitcoin vers GitHub (2011)`
- `Bitcoin Improvement Proposals standardization`
- `WordPress accepte les paiements en Bitcoin (2012)`
- `eBay / PayPal intègre Bitcoin (2014-2015)`
- `Lancement Casascius Physical Bitcoins (2011)`
- `Innovations de métaprotocole Bitcoin (2012-2014)`

Ces objets relèvent souvent davantage du développement infrastructural / monétisation / débordement du protocole que du seul chapitre II.

## 2.5 DéveloppementPhase manifestement incohérentes
Les phases sont distribuées ainsi :
- `Phase de maturatation` -> Chap.I
- `Phase de preuve de concept` -> Chap.III
- `Phase de péché` -> Conclu.

Cette répartition paraît structurellement incohérente et doit être réauditée.

## 2.6 BIP / standardisation : double traitement partiellement contradictoire
On trouve à la fois :
- `InfrastructureEvent — BIP-0001 : institutionnalisation du processus de développement Bitcoin` en `Chap.II`
- `ProtocolProposal | BIP-0001 — Standardisation des BIPs` en `Chap.III`

=> besoin de distinguer :
- institutionnalisation du processus (Chap.II, gouvernance clarifiée)
- usages / propositions en crise ou modification concrète (Chap.III)

---

## 3. Écarts repérés côté rendu / focus

## 3.1 Le focus `Gouvern.` remonte des objets non gouvernants
Le comportement observé fait remonter :
- infrastructure events
- CVE détaillées
- objets techniques
dans `Chap.II -> Gouvern.` ou `Chap.III -> Gouvern.`

=> le filtre ne respecte pas un mapping sémantique strict.

## 3.2 Le focus `Crises` devient une nappe illisible
L’éclatement circulaire :
- compacte trop fortement les CVE ;
- affiche trop de labels en tapis ;
- déborde sur d’autres bandes ;
- ne sépare pas cas majeurs, phases, CVE techniques, réponses, sources.

## 3.3 Le voisinage relationnel écrase l’ancrage principal
Des entités reviennent dans un chapitre simplement parce qu’elles sont liées à :
- une crise,
- un governance process,
- une arène,
- un proposal,
sans respecter leur `lieu d’élaboration analytique principal`.

---

## 4. Corrections prioritaires à faire

### Priorité 1 — ancrage principal
Introduire ou corriger :
- `primaryChapter`
- `primarySection`
- `secondaryChapters`
- `secondarySections`
- `isReusedLater`

### Priorité 2 — séparation nette des familles
Séparer au minimum :
- `Gouvern.`
- `Crises`
- `Objets / infrastructures`

### Priorité 3 — focus strict
Le focus doit d’abord obéir à :
- vue active
- chapitre / bande
- colonne
- ligne
- ancrage principal

et non à la seule densité relationnelle.

### Priorité 4 — agrégation de crise
Quand trop de CVE remontent :
- regrouper par cluster léger
- ou par pseudo-entité mère
pour éviter la saturation mobile.

---

## 5. Cas correctifs les plus urgents

### À réancrer vers Chap.III
- Bitcoin CVE 2018-17144
- GovernanceProcess — CVE-2018-17144 résolution
- CrisisPhase liées à CVE-2018-17144

### À maintenir / renforcer en Chap.II
- Gouvernance polycentrique
- stakeholders / shareholders
- Bitcoin Scaling Debate (comme processus / conflit de gouvernance)
- Bitcoin-dev Mailing List
- GitHub Bitcoin Core
- Bitcointalk Forum

### À réauditer vers Chap.I / I.2 ou I.3
- événements de développement infrastructural Bitcoin
- émergence Ethereum / ICO / Frontier / Genesis Sale
- phases de développement

---

## 6. Conclusion
Le problème n’est pas seulement un problème de layout.
Il y a un **écart entre la logique du manuscrit et la logique d’ancrage des entités**.

La correction doit donc articuler :
1. un **re-ancrage des données**,
2. un **filtrage plus strict**,
3. un **éclatement visuel plus structuré**.
