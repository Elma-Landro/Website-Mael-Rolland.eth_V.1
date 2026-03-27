You must revise the thesis-structure visualization without destroying the historical reading that the user already validated.

CRITICAL RULE:
Do not replace the current chapter-based matrix.
Augment it.

TARGET FOR `Structure de la thèse`:
Restore and preserve these columns exactly:
1. Chap.
2. Struct.
3. Objets
4. Acteurs
5. Concepts
6. Evén.
7. Réf.

Do not remove `Chap.` or `Struct.`.
Do not flatten the old color system.
Do not suppress the chapter glow / halo aesthetics.

IMPLEMENTATION GOAL:
Keep the original visual immediacy, but encode the refined ontology INSIDE the existing columns.

COLUMN RULES:
- `Acteurs` includes, in this vertical order:
  - StakeholderCategory
  - Institution / Organization
  - StakeholderGroup / ActorGroup
  - empirically embodied Person
- `Réf.` includes:
  - AcademicWork
  - Reference
  - Corpus
  - SourceQuote
  - PrimarySource
  - Method
  - Person only when primary role = theoretical/source reference
- `Concepts` includes:
  - CoreConcept high
  - SecondaryConcept
  - TechnicalConcept
  - NativeFormula lower
- `Objets` includes:
  - Protocol
  - MonetaryObject
  - SoftwareClient
  - CodeRepository
  - SmartContract
  - PlatformService
  - InfrastructureService
  - HardwareDevice
  - Marketplace
- `Evén.` includes:
  - CrisisEvent
  - CrisisPhase
  - GovernanceConflict
  - GovernanceProcess
  - ProtocolProposal
  - InfrastructureEvent

VISUAL RULES:
- Keep strong chapter colors.
- Keep chapter halos.
- Ensure column titles are readable at a glance.
- Prefer horizontal or low-angle labels over steep diagonals.
- Add subtle internal sub-bands in `Acteurs` and `Concepts`, but do not clutter.
- `Multi.` line must stay visible for transversal entities.

MANDATORY OVERRIDES IN `Acteurs`:
Peter Wuille
Greg Maxwell
Gregory Maxwell
Adam Back
W.J. van der Laan
Jihan Wu
Vitalik Buterin
Gavin Wood
Vlad Zamfir
Roger Ver

MANDATORY OVERRIDES IN `Réf.`:
Susan Leigh Star
Geoffrey Bowker
Thomas Hughes
André Orléan
Michel Aglietta
Bruno Théret
Viviana Zelizer
Keith Hart

MANDATORY HIGH PLACEMENT IN `Concepts`:
Monétisation
Infrastructure sociotechnique
Gouvernance polycentrique
Gouvernance duale
Développement carnavalesque
Mise en crise
Remise en ordre
Nominalisme monétaire non étatiste

ALSO REBUILD `Monétisation` VIEW:
Make it immediately legible with these column titles:
1. Noyau
2. Mécanismes
3. Médiations
4. Acteurs
5. Cas
6. Réf.

These labels must be large and readable without zooming.
Do not leave the columns implicit.

SUCCESS CONDITION:
At first glance, the user must still recognize the old beautiful thesis matrix, but now with better ontological readability.
