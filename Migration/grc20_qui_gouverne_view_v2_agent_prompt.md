Tu dois corriger la vue `Qui gouverne réellement ?`.

Problème de la version actuelle :
- pas de colonne explicite `Gouvern.`
- pas de colonne `Struct.`
- la vue ne reflète donc ni la structure du manuscrit ni la centralité de la gouvernance dans la thèse

Implémente une matrice 8 × 6.

Colonnes obligatoires :
1. Struct.
2. Gouvern.
3. Catégories
4. Organisations
5. Groupes
6. Arènes
7. Personnes
8. Cas / Réf.

Lignes obligatoires :
1. Problématisation
2. Coordination
3. Décision
4. Conflit
5. Maintenance
6. Sources

Mappings de principe :
- ThesisSection / ChapterSection / Argument / NarrativeCluster -> Struct.
- GovernanceProcess / GovernanceConflict / ProtocolProposal / CrisisPhase -> Gouvern.
- StakeholderCategory -> Catégories
- Institution / Organization -> Organisations
- StakeholderGroup -> Groupes
- GovernanceArena -> Arènes
- Person agissante -> Personnes
- CrisisEvent / Reference / SourceQuote / PrimarySource / Corpus / AcademicWork / auteurs théoriques -> Cas / Réf.

Contraintes absolues :
- ne pas absorber `Gouvern.` dans `Arènes`
- ne pas supprimer `Struct.`
- ne pas envoyer les personnes agissantes en colonne finale
- conserver halos, lisibilité mobile et logique esthétique du site

Exemples d’overrides :
- Gouvernance polycentrique -> Gouvern. / Problématisation
- Gouvernance duale -> Gouvern. / Problématisation
- Politique de crises -> Gouvern. / Maintenance
- II.3 Au-delà de la revendication d'une absence de gouvernance ! -> Struct. / Problématisation
- III.3 Une gouvernance publique d'exception -> Struct. / Conflit
- Peter Wuille -> Personnes / Maintenance
- Greg Maxwell -> Personnes / Décision
- GitHub Bitcoin Core -> Arènes / Maintenance
- Bitcoin-dev Mailing List -> Arènes / Coordination
- CVE-2018-17144 -> Cas / Réf. / Maintenance
- The DAO -> Cas / Réf. / Conflit
- Susan Leigh Star -> Cas / Réf. / Sources
