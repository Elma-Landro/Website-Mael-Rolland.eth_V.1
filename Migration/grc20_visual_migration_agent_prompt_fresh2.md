Tu dois implémenter une migration visuelle pour la page graphe.

Objectif :
1. améliorer la lisibilité sans casser l’esthétique historique ;
2. conserver les halos et la logique visuelle existante ;
3. séparer clairement deux vues :
   - `Structure de la thèse`
   - `Monétisation des CM`

Contraintes absolues :
- ne pas supprimer `Chap.` ni `Struct.` dans `Structure de la thèse` ;
- ne pas comprimer `Gouvern.`, `Acteurs`, `Concepts`, `Réf./Sources` ;
- les personnes agissantes doivent rester dans `Acteurs` ;
- la colonne `Réf./Sources` doit être visuellement décrochée et lisible ;
- sur mobile, les titres doivent rester compréhensibles au premier coup d’œil.

Vue `Structure de la thèse`
Colonnes :
Chap. / Struct. / Objets / Gouvern. / Acteurs / Concepts / Réf./Sources

Vue `Monétisation des CM`
Colonnes :
Noyau / Émission / Circulation / Accès / Usages / Valorisation / Stabilisation

Prévois :
- mapping type -> colonne ;
- mapping type -> ligne ;
- mécanisme d’overrides par entité ;
- JSON d’overrides initial.
