Tu dois créer ou refondre une vue du graphe intitulée `Qui gouverne réellement ?`.

But :
donner une lecture politique et organisationnelle de la gouvernance des cryptomonnaies.

La vue doit rendre immédiatement lisibles :
- les catégories analytiques ;
- les institutions et organisations ;
- les groupes empiriques ;
- les arènes et processus de gouvernance ;
- les personnes agissantes ;
- les cas et crises révélateurs ;
- les références et sources.

Colonnes obligatoires :
1. Catégories
2. Organisations
3. Groupes
4. Arènes
5. Personnes
6. Cas
7. Réf.

Lignes obligatoires :
1. Pouvoir distribué
2. Coordination
3. Décision
4. Conflit
5. Maintenance
6. Réf.

Mappings :
- StakeholderCategory -> Catégories
- Institution / Organization -> Organisations
- StakeholderGroup -> Groupes
- GovernanceArena / GovernanceProcess / GovernanceConflict / ProtocolProposal -> Arènes
- Person (agissante) -> Personnes
- CrisisEvent / CrisisPhase -> Cas
- Reference / SourceQuote / PrimarySource / Corpus / AcademicWork / Person théorique -> Réf.

Contraintes :
- conserver halos et ambiance du site ;
- `Personnes` doit être distinct de `Réf.` ;
- `Arènes` ne doit pas être absorbée ailleurs ;
- prévoir overrides par entité.
