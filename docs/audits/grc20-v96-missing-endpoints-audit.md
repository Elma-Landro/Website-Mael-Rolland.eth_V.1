# Audit des endpoints manquants — graphe GRC-20 v96
## 1. Scope de l’audit
- **Mission** : Mission 003 — identifier précisément les relations de `grc20-these-mael-rolland-v96.json` dont au moins un endpoint ne résout pas vers une entité existante.
- **Mode** : Patch / PR documentaire limité, sans modification du graphe.
- **Graphe inspecté** : `grc20-these-mael-rolland-v96.json`.
- **Fichier ajouté** : `docs/audits/grc20-v96-missing-endpoints-audit.md`.
- **Hors périmètre respecté** : pas de création de `v97`, pas de suppression ou création d’entité, pas de modification de relation, pas de modification de `graphe.html`, des scripts ou du déploiement.

## 2. Sources et règles consultées
- `grc20-these-mael-rolland-v96.json` : source effective de l’audit structurel.
- `docs/architecture/schema-vnext.md` : confirme la forme observée du snapshot v96 : `space`, `types`, `relation_types`, `entities`, `relations`, `ops`, avec relations structurées par `from`, `to`, `type`.
- Aucune citation ni claim substantiel de la thèse n’a été ajouté ou vérifié ici : l’audit porte uniquement sur l’intégrité référentielle des endpoints relationnels.

## 3. Synthèse
- **Nombre total de relations inspectées** : 20057.
- **Nombre de relations cassées** : 16.
- **Part des relations cassées** : 0.0798%.
- **Nombre total d’entités inspectées** : 2263.
- **Nombre de types de relations dans v96** : 130.
- **Endpoints manquants uniques** : 13.
- **Relations avec endpoint probablement tronqué à 16 caractères** : 15.
- **Relations sans candidat unique par préfixe dans v96** : 1.

### Types de relations concernés
| Type de relation | Nombre de relations cassées |
|---|---:|
| appears in section | 11 |
| cited in | 4 |
| contributes to | 1 |

### Entités existantes les plus touchées
| Entité existante endpoint | Label | Type d’entité | Nombre de relations cassées incidentes |
|---|---|---|---:|
| `a2c452a77b394a9d836eed0e16ed5851` | Chapitre I - L'émergence du phénomène des cryptomonnaies (CM) : Bitcoin et Ethereum comme infrastructures sociotechniques | Chapter | 6 |
| `89663a261c1545c1941ab7f871314a53` | III.2 Des marques d'une politique de crises : une gouvernance de huis clos routinière | ThesisSection | 4 |
| `38e637cc84f14883b96d064b8e387c0f` | II.2 « Pourtant, elles font monnaie ! » : à l'aune d'un nominalisme « non étatiste » attentif aux usages | ThesisSection | 2 |
| `e3b7d91585004ef7a392934a0b37292f` | Ostrom 1990 | Reference | 1 |
| `df405dcd975b406486a260da72f1ad4a` | Introduction générale | Chapter | 1 |
| `5b5935bc3ede49028b7dfbdaa4f34b6d` | Chapitre II - Dépasser la controverse du statut monétaire des CM par un institutionnalisme intéressé aux usages | Chapter | 1 |
| `21ff5747290e4951a3b0b601ddbbe9d6` | B. La gouvernance des CM dévoilée par leurs crises : un institutionnalisme articulé à une sociologie des sciences et techniques | ThesisSection | 1 |

### Niveau de risque
- **Export** : risque **élevé** si l’exporteur exige que chaque endpoint relationnel existe ; risque **moyen** si les relations invalides sont filtrées silencieusement, car cela introduit une perte non documentée.
- **Story mode** : risque **moyen à élevé** pour les pas narratifs ou expansions dépendant des relations `appears in section`, `cited in` ou `contributes to` ; les nœuds sources manquants empêchent l’expansion ou créent des liens invisibles.
- **Navigation** : risque **moyen** ; les entités de section existantes restent navigables, mais leur voisinage est incomplet et certaines références/concepts/personnes attendus peuvent disparaître des parcours.

## 4. Relations cassées détaillées
| # index | Relation id | Relation type | from | to | Endpoint manquant | Endpoint existant + label | Type de l’entité existante | Hypothèse de cause | Correction possible | Confiance | Validation humaine requise |
|---:|---|---|---|---|---|---|---|---|---|---|---|
| 19455 | `d65f683129e8e3cf9baea9ab24d5d6eb` | appears in section<br>`f004d0e68f0964e8787d19b350e3ca24` | `0170870141524d46` | `89663a261c1545c1941ab7f871314a53` | from: `0170870141524d46` | to: `89663a261c1545c1941ab7f871314a53` — III.2 Des marques d'une politique de crises : une gouvernance de huis clos routinière | to: ThesisSection | ID obsolète / erreur de génération (ID tronqué à 16 caractères) | remplacer `0170870141524d46` par `0170870141524d469e6c6c6ed9c01620` (`Black Hat`) si la relation est confirmée | élevé | oui |
| 19456 | `0c0b8086cb614819f9bfcec0dafa5bce` | appears in section<br>`f004d0e68f0964e8787d19b350e3ca24` | `c0c1bec510f54099` | `89663a261c1545c1941ab7f871314a53` | from: `c0c1bec510f54099` | to: `89663a261c1545c1941ab7f871314a53` — III.2 Des marques d'une politique de crises : une gouvernance de huis clos routinière | to: ThesisSection | ID obsolète / erreur de génération (ID tronqué à 16 caractères) | remplacer `c0c1bec510f54099` par `c0c1bec510f54099ab608e3488f93223` (`White Hat`) si la relation est confirmée | élevé | oui |
| 19457 | `bd4b971b2742ec4e2b8b7045c5ef3ccd` | appears in section<br>`f004d0e68f0964e8787d19b350e3ca24` | `f87e9246cf2b407b` | `a2c452a77b394a9d836eed0e16ed5851` | from: `f87e9246cf2b407b` | to: `a2c452a77b394a9d836eed0e16ed5851` — Chapitre I - L'émergence du phénomène des cryptomonnaies (CM) : Bitcoin et Ethereum comme infrastructures sociotechniques | to: Chapter | ID obsolète / erreur de génération (ID tronqué à 16 caractères) | remplacer `f87e9246cf2b407b` par `f87e9246cf2b407bb996bf5632733b88` (`Consensus distribué`) si la relation est confirmée | élevé | oui |
| 19458 | `22ede694643bf5af857e7d92b2fecce8` | appears in section<br>`f004d0e68f0964e8787d19b350e3ca24` | `f07878254e144095` | `a2c452a77b394a9d836eed0e16ed5851` | from: `f07878254e144095` | to: `a2c452a77b394a9d836eed0e16ed5851` — Chapitre I - L'émergence du phénomène des cryptomonnaies (CM) : Bitcoin et Ethereum comme infrastructures sociotechniques | to: Chapter | ID obsolète / erreur de génération (ID tronqué à 16 caractères) | remplacer `f07878254e144095` par `f07878254e144095a9644a091f3ef5cb` (`Logique de sceau`) si la relation est confirmée | élevé | oui |
| 19459 | `4e14f846951e84903daf635e595a4d2e` | appears in section<br>`f004d0e68f0964e8787d19b350e3ca24` | `f07878254e144095` | `38e637cc84f14883b96d064b8e387c0f` | from: `f07878254e144095` | to: `38e637cc84f14883b96d064b8e387c0f` — II.2 « Pourtant, elles font monnaie ! » : à l'aune d'un nominalisme « non étatiste » attentif aux usages | to: ThesisSection | ID obsolète / erreur de génération (ID tronqué à 16 caractères) | remplacer `f07878254e144095` par `f07878254e144095a9644a091f3ef5cb` (`Logique de sceau`) si la relation est confirmée | élevé | oui |
| 19460 | `2dac7554e5c235f19e71dfd48580cb8c` | appears in section<br>`f004d0e68f0964e8787d19b350e3ca24` | `71908f95dad74d9a` | `a2c452a77b394a9d836eed0e16ed5851` | from: `71908f95dad74d9a` | to: `a2c452a77b394a9d836eed0e16ed5851` — Chapitre I - L'émergence du phénomène des cryptomonnaies (CM) : Bitcoin et Ethereum comme infrastructures sociotechniques | to: Chapter | ID obsolète / erreur de génération (ID tronqué à 16 caractères) | remplacer `71908f95dad74d9a` par `71908f95dad74d9ab8abdfd19c8b733b` (`Logique de signature`) si la relation est confirmée | élevé | oui |
| 19461 | `8126fb055e2221061fbbcad41a45112f` | appears in section<br>`f004d0e68f0964e8787d19b350e3ca24` | `71908f95dad74d9a` | `38e637cc84f14883b96d064b8e387c0f` | from: `71908f95dad74d9a` | to: `38e637cc84f14883b96d064b8e387c0f` — II.2 « Pourtant, elles font monnaie ! » : à l'aune d'un nominalisme « non étatiste » attentif aux usages | to: ThesisSection | ID obsolète / erreur de génération (ID tronqué à 16 caractères) | remplacer `71908f95dad74d9a` par `71908f95dad74d9ab8abdfd19c8b733b` (`Logique de signature`) si la relation est confirmée | élevé | oui |
| 19462 | `58539588d1f6a155093c9c01705a2318` | appears in section<br>`f004d0e68f0964e8787d19b350e3ca24` | `2af42270c40746e2` | `a2c452a77b394a9d836eed0e16ed5851` | from: `2af42270c40746e2` | to: `a2c452a77b394a9d836eed0e16ed5851` — Chapitre I - L'émergence du phénomène des cryptomonnaies (CM) : Bitcoin et Ethereum comme infrastructures sociotechniques | to: Chapter | ID obsolète / erreur de génération (ID tronqué à 16 caractères) | remplacer `2af42270c40746e2` par `2af42270c40746e2876a3617ed8f7694` (`OP_RETURN`) si la relation est confirmée | élevé | oui |
| 19463 | `9dee2daa2afa4212f6369b059e0cf78c` | contributes to<br>`e279d673d83443bc95f641070d3a012e` | `72d182705407492c` | `e3b7d91585004ef7a392934a0b37292f` | from: `72d182705407492c` | to: `e3b7d91585004ef7a392934a0b37292f` — Ostrom 1990 | to: Reference | entité supprimée ou relation orpheline | retrouver l’entité source de `72d182705407492c` dans les versions antérieures/patches ; sinon supprimer ou réancrer la relation après validation | faible | oui |
| 19464 | `d04e21e114674ea2dc6f6da98b28887c` | appears in section<br>`f004d0e68f0964e8787d19b350e3ca24` | `571934eb6d074fb8` | `89663a261c1545c1941ab7f871314a53` | from: `571934eb6d074fb8` | to: `89663a261c1545c1941ab7f871314a53` — III.2 Des marques d'une politique de crises : une gouvernance de huis clos routinière | to: ThesisSection | ID obsolète / erreur de génération (ID tronqué à 16 caractères) | remplacer `571934eb6d074fb8` par `571934eb6d074fb883382b1e21d66a9b` (`Auryn Macmillan`) si la relation est confirmée | élevé | oui |
| 19465 | `8903672c5563db32d2c6c3a1995b7416` | appears in section<br>`f004d0e68f0964e8787d19b350e3ca24` | `633ccadaea354e76` | `a2c452a77b394a9d836eed0e16ed5851` | from: `633ccadaea354e76` | to: `a2c452a77b394a9d836eed0e16ed5851` — Chapitre I - L'émergence du phénomène des cryptomonnaies (CM) : Bitcoin et Ethereum comme infrastructures sociotechniques | to: Chapter | ID obsolète / erreur de génération (ID tronqué à 16 caractères) | remplacer `633ccadaea354e76` par `633ccadaea354e76a73adf24477ae894` (`Bill Shihara`) si la relation est confirmée | élevé | oui |
| 19466 | `0576eede6a5ecd7ebbd4ba56cc2bcda0` | appears in section<br>`f004d0e68f0964e8787d19b350e3ca24` | `20b8c4f053744b01` | `a2c452a77b394a9d836eed0e16ed5851` | from: `20b8c4f053744b01` | to: `a2c452a77b394a9d836eed0e16ed5851` — Chapitre I - L'émergence du phénomène des cryptomonnaies (CM) : Bitcoin et Ethereum comme infrastructures sociotechniques | to: Chapter | ID obsolète / erreur de génération (ID tronqué à 16 caractères) | remplacer `20b8c4f053744b01` par `20b8c4f053744b0193b295fd719f7d6b` (`Tristan D'Agosta`) si la relation est confirmée | élevé | oui |
| 19467 | `f040b502d65d1175ef583f86d1cfab8f` | cited in<br>`adaac51ada17446785f6d0fdf5b15425` | `53525938440543a5` | `df405dcd975b406486a260da72f1ad4a` | from: `53525938440543a5` | to: `df405dcd975b406486a260da72f1ad4a` — Introduction générale | to: Chapter | ID obsolète / erreur de génération (ID tronqué à 16 caractères) | remplacer `53525938440543a5` par `53525938440543a5af359337eeab9823` (`Jérôme Favier`) si la relation est confirmée | élevé | oui |
| 19468 | `64190d3ebb4bb47f7d79f063690db5d2` | cited in<br>`adaac51ada17446785f6d0fdf5b15425` | `53525938440543a5` | `5b5935bc3ede49028b7dfbdaa4f34b6d` | from: `53525938440543a5` | to: `5b5935bc3ede49028b7dfbdaa4f34b6d` — Chapitre II - Dépasser la controverse du statut monétaire des CM par un institutionnalisme intéressé aux usages | to: Chapter | ID obsolète / erreur de génération (ID tronqué à 16 caractères) | remplacer `53525938440543a5` par `53525938440543a5af359337eeab9823` (`Jérôme Favier`) si la relation est confirmée | élevé | oui |
| 19469 | `98c8b43048f4fff4bbda35109c631909` | cited in<br>`adaac51ada17446785f6d0fdf5b15425` | `fb692ce5f716443f` | `21ff5747290e4951a3b0b601ddbbe9d6` | from: `fb692ce5f716443f` | to: `21ff5747290e4951a3b0b601ddbbe9d6` — B. La gouvernance des CM dévoilée par leurs crises : un institutionnalisme articulé à une sociologie des sciences et techniques | to: ThesisSection | ID obsolète / erreur de génération (ID tronqué à 16 caractères) | remplacer `fb692ce5f716443f` par `fb692ce5f716443fa6bd1d5e28906142` (`Primavera De Filippi`) si la relation est confirmée | élevé | oui |
| 19470 | `2b000439e05165325ab7802dbbdbb382` | cited in<br>`adaac51ada17446785f6d0fdf5b15425` | `a985149b43e34a43` | `89663a261c1545c1941ab7f871314a53` | from: `a985149b43e34a43` | to: `89663a261c1545c1941ab7f871314a53` — III.2 Des marques d'une politique de crises : une gouvernance de huis clos routinière | to: ThesisSection | ID obsolète / erreur de génération (ID tronqué à 16 caractères) | remplacer `a985149b43e34a43` par `a985149b43e34a43990ea270ba314147` (`The Filter / Griff Green 2016 — DAO hack and whitehat response interview`) si la relation est confirmée | élevé | oui |

## 5. Lecture diagnostique
- Les 16 relations cassées ont toutes un endpoint `from` non résolu ; aucun cas `to` manquant n’a été détecté.
- Le motif dominant est un **ID source tronqué à 16 caractères** alors que les IDs d’entités v96 sont majoritairement longs. Pour 15 relations, le préfixe tronqué correspond à une entité v96 unique, ce qui rend une correction mécanique plausible, mais non appliquée ici.
- Une relation (`index 19463`, id `9dee2daa2afa4212f6369b059e0cf78c`) pointe depuis `72d182705407492c`, qui ne correspond à aucun préfixe d’entité v96 ; elle doit être traitée comme relation orpheline ou comme référence à une entité supprimée/absente jusqu’à vérification historique.
- Les relations cassées sont groupées aux index 19455–19470, ce qui suggère un ajout ou patch de fin de fichier partiellement incohérent plutôt qu’une corruption dispersée du graphe.

## 6. Incertitudes restantes
- Le rapport ne vérifie pas si chaque relation est substantiellement justifiée par la thèse ; il vérifie seulement la résolution des endpoints dans v96.
- Les corrections proposées par préfixe unique sont structurellement probables, mais doivent être validées humainement avant modification du graphe, surtout pour éviter de transformer une erreur d’ID en relation sémantiquement fausse.
- Le cas `72d182705407492c` nécessite une recherche dans les versions antérieures du graphe, les patchs sources ou les notes de génération.

## 7. Proposition de prochaine mission corrective — non appliquée
Créer une mission corrective séparée pour produire `grc20-these-mael-rolland-v97.json` à partir de v96, avec :
1. remplacement des 15 endpoints `from` tronqués par leur ID complet unique si validation humaine confirmée ;
2. enquête spécifique sur `72d182705407492c` dans les versions/patches antérieurs ;
3. validation JSON et intégrité référentielle complète après correction ;
4. changelog indiquant explicitement qu’aucune entité ni relation sémantique nouvelle n’est ajoutée si seules les références d’ID sont réparées.