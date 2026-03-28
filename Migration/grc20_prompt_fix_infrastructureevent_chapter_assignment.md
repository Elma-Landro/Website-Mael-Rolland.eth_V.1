# Prompt agent implémenteur — correction du mauvais ancrage chapitral des `InfrastructureEvent`

Tu dois corriger un bug de fond dans le graphe :
de nombreux `InfrastructureEvent` apparaissent actuellement comme s’ils relevaient du **chapitre III**, alors qu’ils viennent en réalité du **chapitre I, section I.2** sur le développement infrastructurel de Bitcoin.

## Diagnostic fondé sur la structure du manuscrit

La structure de la thèse affichée dans l’application montre clairement que :

- **Chapitre I** est consacré à l’émergence des CM comme infrastructures sociotechniques ;
- **I.2** est la séquence sur le développement infrastructural / carnavalesque de Bitcoin ;
- **Chapitre III** est consacré à la gouvernance révélée par les crises, notamment :
  - Bitcoin CVE 2018-17144
  - The DAO
  - politiques de crise
  - gouvernance de huis clos / publique d’exception

Donc :
- un `InfrastructureEvent` de type émergence d’acteurs, services, couches, dispositifs, passerelles, usages ou extensions du monde Bitcoin doit être **ancré en priorité dans Chap. I**, surtout I.2 ;
- il ne doit pas migrer vers **Chap. III** simplement parce qu’il est relié à une crise, à une proposition de protocole, à un conflit de gouvernance ou à un rappel ultérieur dans le texte.

---

## Problème à corriger

Le comportement actuel semble utiliser une logique trop relationnelle ou trop tardive :

- si un `InfrastructureEvent` est relié à des objets de crise ou de gouvernance du chapitre III,
- alors il remonte dans `Chap. III`,
- ce qui écrase son **lieu d’élaboration analytique principal**.

C’est faux du point de vue de la thèse.

Il faut distinguer :
- **lieu principal d’analyse**
- **réemplois / rappels ultérieurs**

---

## Règle de vérité à implémenter

### Règle 1 — priorité à l’ancrage textuel principal
Pour les types suivants :
- `InfrastructureEvent`
- `InfrastructureDomain`
- `InfrastructureSegment`
- `DevelopmentPhase`
- `PriceWindow`
- `Capability`
- objets analogues de développement infrastructurel

l’ancrage chapitral doit être déterminé d’abord par :
1. la **section source principale**
2. le **chapitre d’élaboration analytique principal**
3. les **preuves textuelles principales**
4. seulement ensuite, de manière secondaire, les relations avec d’autres entités

### Règle 2 — ne pas utiliser le voisinage relationnel comme critère dominant
Une entité ne doit pas passer en `Chap. III` simplement parce qu’elle est :
- reliée à un `CrisisEvent`
- reliée à un `GovernanceProcess`
- reliée à un `ProtocolProposal`
- réévoquée dans une section tardive
- reliée à un conflit étudié plus loin

Les relations secondaires ne doivent jamais écraser le chapitre principal.

### Règle 3 — distinction obligatoire entre ancrage principal et réemploi
Ajouter ou corriger les champs/logiques suivants :
- `primaryChapter`
- `primarySection`
- `secondaryChapters`
- `secondarySections`
- `isReusedLater`

### Règle 4 — rendu visuel
- `primaryChapter` détermine la **position principale**
- `secondaryChapters` peuvent seulement produire :
  - contexte faible
  - halo secondaire discret
  - lien
  - ghost node optionnel
- mais pas un déplacement principal de bande

---

## Règle spéciale pour `InfrastructureEvent`

Par défaut :
- `InfrastructureEvent` => **Chap. I**
- si possible **I.2** comme ancrage préférentiel quand il s’agit du développement infrastructural / carnavalesque de Bitcoin

Exemples typiques :
- émergence de pools de minage
- apparition de services
- passerelles, wallets, processeurs de paiement
- extensions extra-protocolaires
- couches de médiation
- événements de développement du monde Bitcoin
- improvisations d’acteurs au-delà du protocole

Ces objets ne doivent aller en **Chap. III** que dans des cas exceptionnels :
- si l’événement est en réalité une **crise**
- ou un **épisode de gouvernance** traité principalement dans le chapitre III
- ou s’il a été mal typé et doit être reclassé comme `CrisisEvent` ou `GovernanceProcess`

---

## Séparation ontologique à renforcer

Tu dois empêcher la confusion entre :
- `InfrastructureEvent`
- `CrisisEvent`
- `GovernanceProcess`

### `InfrastructureEvent`
Développement, extension, improvisation, constitution progressive du monde socio-technique.

### `CrisisEvent`
Épisode de rupture, vulnérabilité, attaque, scandale, crise ouverte.

### `GovernanceProcess`
Coordination, arbitrage, décision, maintenance, traitement de désaccord, procédure de modification.

Un `InfrastructureEvent` relié à un `CrisisEvent` ne devient pas pour autant une crise.
Un `InfrastructureEvent` relié à une arène de décision ne devient pas pour autant un processus de gouvernance.

---

## Correction attendue dans les vues

### 1. `Structure de la thèse`
Quand on filtre :
- `Chap. I`
- `Objets`
ou
- `Chap. I`
- `Struct.` / `Objets`

on doit retrouver prioritairement les `InfrastructureEvent` issus de I.2.

Quand on filtre :
- `Chap. III`
- `Gouvern.`
ou `Crises`

on ne doit pas voir remonter en masse les `InfrastructureEvent` de I.2, sauf comme contexte secondaire très atténué.

### 2. `Focus`
Si utilisateur choisit :
`Focus -> Chap. III -> Gouvern. -> Éclater`

ne pas faire remonter automatiquement :
- `InfrastructureEvent`
- `InfrastructureDomain`
- `DevelopmentPhase`
issus du chapitre I

### 3. `Qui gouverne réellement ?`
Ne pas absorber les `InfrastructureEvent` historiques dans la gouvernance.
Ils peuvent être reliés, mais pas placés comme nœuds principaux de gouvernement.

---

## Procédure de correction demandée

### Étape A — audit ciblé
Faire une passe sur toutes les entités de type :
- `InfrastructureEvent`
- types voisins de développement infrastructurel

et détecter :
- celles dont `primaryChapter` est actuellement `Chap. III`
- alors que leur intitulé, leur description ou leur source textuelle renvoie à I.2

### Étape B — reclassification / re-anchoring
Pour chaque cas détecté :
- corriger `primaryChapter` vers `Chap. I`
- corriger `primarySection` vers `I.2` si pertinent
- conserver éventuellement `secondaryChapter = Chap. III` si l’entité est réutilisée plus tard

### Étape C — exceptions
Si un soi-disant `InfrastructureEvent` appartient en réalité à :
- `CrisisEvent`
- `GovernanceProcess`

alors :
- le retyper proprement
- ou créer une relation plus claire entre entités distinctes
- mais ne pas laisser l’ambiguïté

---

## Heuristiques recommandées

### Indices d’ancrage Chap. I / I.2
Mots ou logiques typiques :
- développement infrastructural
- improvisations d’acteurs
- services
- passerelles
- wallets
- pools
- emergence
- altcoins
- surcouches
- usages naissants
- débordement du protocole
- monde Bitcoin redéfini carnavalesquement

### Indices d’ancrage Chap. III
Mots ou logiques typiques :
- crise
- CVE
- attaque
- disclosure
- hard fork
- soft fork
- consensus de crise
- controverse publique
- gouvernance de huis clos
- politique de crises

Ces indices ne doivent pas être mélangés.

---

## Livrables attendus

1. audit des `InfrastructureEvent` mal ancrés
2. correction des `primaryChapter`
3. correction des `primarySection`
4. ajout éventuel de `secondaryChapters`
5. correction du filtre/focus pour respecter l’ancrage principal
6. signalement des cas à retyper en `CrisisEvent` ou `GovernanceProcess`

---

## Critère de réussite

Après correction :

- les `InfrastructureEvent` issus de I.2 réapparaissent principalement dans **Chap. I**
- `Chap. III` cesse d’être envahi par des événements infrastructurels anciens
- le focus `Chap. III -> Gouvern.` montre de la gouvernance, pas du développement infrastructurel
- le graphe redevient fidèle à la logique analytique de la thèse
