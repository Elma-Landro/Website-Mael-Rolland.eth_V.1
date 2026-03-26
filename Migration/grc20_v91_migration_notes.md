
# GRC-20 v91 migration notes

This package is a name-based migration aid derived from the v90 entity inventory and the prior diagnostic.

## Main objectives
1. Collapse obvious aliases and spelling duplicates.
2. Restore clean distinctions between Person / Institution / Organization / StakeholderCategory / StakeholderGroup.
3. Split the overloaded ActorNonHuman bucket into clearer ontological subtypes.
4. Separate core analytical concepts from technical concepts and slogans.
5. Recenter the graph around **Monétisation** as the organizing concept of the thesis.

## Important implementation rules
- Prefer **merge** over delete when two entities clearly refer to the same referent.
- Preserve previous labels as aliases on the surviving entity.
- Retype only when confidence is high and the target type is ontologically clearer.
- For section titles and mini-claims currently stored as Concept, move them out of the conceptual layer.
- Add explicit category links between empirical collectives and broader stakeholder categories.

## Caution points
- This is not yet ID-based. The implementer must resolve names to entity IDs from the v90 JSON before applying the patch.
- Some entities may need manual review because the inventory alone cannot fully disambiguate them.
- `Organization` can be renamed `Company` if the existing codebase already uses that convention.
- `StakeholderGroup` can remain `ActorGroup` if schema extension is undesirable, but then the category relation becomes mandatory.

## Priority order
1. Duplicate merges
2. Person / Institution / Organization retypes
3. ActorGroup vs StakeholderCategory cleanup
4. ActorNonHuman split
5. Concept hierarchy
6. InfrastructureDomain canonicalization
7. Crisis sequencing harmonization
