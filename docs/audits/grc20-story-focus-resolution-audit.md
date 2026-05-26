# Audit de résolution des focus nodes Story — v96

## 1. Scope

- **Fichiers lus** : `story-presets.mjs`, `graphe.story-helpers.js`, `grc20-these-mael-rolland-v96.json`.
- **Fichiers non modifiés** : `story-presets.mjs`, `narrative-anchors.json`, `graphe.html`, scripts runtime.
- **Méthode** : reproduction de la logique runtime `resolveStoryFocusNodes` : alias `STORY_FOCUS_ALIASES`, recherche par ID, nom exact, puis nom normalisé sans accents.

## 2. Synthèse

- **Stories inspectées** : 5.
- **Occurrences de `focusNodes` inspectées** : 167.
- **Labels de focus uniques** : 90.
- **Occurrences résolues** : 167.
- **Occurrences non résolues** : 0.
- **Occurrences résolues via alias runtime** : 46.
- **Collisions normalisées détectées** : 0.

**Constat principal** : aucun focus label de `story-presets.mjs` ne reste non résolu avec la logique runtime actuelle. Les non-résolutions signalées dans des passes antérieures semblent avoir été absorbées par la table `STORY_FOCUS_ALIASES` et/ou par les noms actuellement présents dans v96.

## 3. Table de résolution par label de focus

| Focus label | Story concernée | Résolution exacte ou absence | Collisions éventuelles | Candidat d’ID canonique | Niveau de confiance |
|---|---|---|---|---|---|
| A. La gouvernance des cryptomonnaies : construction de notre objet de recherche | Structure de la thèse (`structure-these`) | nom exact → `0fcc7028560c47cc9b82309f469b700c` — A. La gouvernance des cryptomonnaies : construction de notre objet de recherche | aucune | `0fcc7028560c47cc9b82309f469b700c` | élevé |
| All Core Dev Meetings (Ethereum) | Qui gouverne réellement ? (`qui-gouverne-reellement`) | nom exact → `8a76b0da92254d76a4a330ddb8b40e4c` — All Core Dev Meetings (Ethereum) | aucune | `8a76b0da92254d76a4a330ddb8b40e4c` | élevé |
| Altcoins | Structure de la thèse (`structure-these`) | nom exact → `d0cecb8402c045fb9c1cf6d0337d1630` — Altcoins | aucune | `d0cecb8402c045fb9c1cf6d0337d1630` | élevé |
| Awemany | Fil de preuves (`fil-de-preuves`) | nom exact → `2cc2e87266524c59bfd887bd0280661a` — Awemany | aucune | `2cc2e87266524c59bfd887bd0280661a` | élevé |
| Bitcoin | Crises (`crises`)<br>Fil de preuves (`fil-de-preuves`)<br>Structure de la thèse (`structure-these`) | nom exact → `d35d720e1fa24d9fbe665a90ac0abc73` — Bitcoin | aucune | `d35d720e1fa24d9fbe665a90ac0abc73` | élevé |
| Bitcoin Core (repo) | Crises (`crises`)<br>Fil de preuves (`fil-de-preuves`)<br>Qui gouverne réellement ? (`qui-gouverne-reellement`)<br>Structure de la thèse (`structure-these`) | nom exact → `5d6203275f6a40ddb8ede1d7c01cad1e` — Bitcoin Core (repo) | aucune | `5d6203275f6a40ddb8ede1d7c01cad1e` | élevé |
| Bitcoin CVE 2018-17144 | Crises (`crises`)<br>Fil de preuves (`fil-de-preuves`)<br>Structure de la thèse (`structure-these`) | nom exact → `db9a125c4c7a4d03bd19d3dc8c474a9e` — Bitcoin CVE 2018-17144 | aucune | `db9a125c4c7a4d03bd19d3dc8c474a9e` | élevé |
| Bitcoin-dev Mailing List | Qui gouverne réellement ? (`qui-gouverne-reellement`) | nom exact → `263da28a75204bb6aeb86da63f7d20c0` — Bitcoin-dev Mailing List | aucune | `263da28a75204bb6aeb86da63f7d20c0` | élevé |
| Bitcointalk Forum | Qui gouverne réellement ? (`qui-gouverne-reellement`) | nom exact → `cf551a2d86db4f11b8cf620b71c2a5c2` — Bitcointalk Forum | aucune | `cf551a2d86db4f11b8cf620b71c2a5c2` | élevé |
| C.2. Stratégie d'accès et matériaux de terrain récoltés | Structure de la thèse (`structure-these`) | nom exact → `4615956ddad16a1de0c360886fa0932f` — C.2. Stratégie d'accès et matériaux de terrain récoltés | aucune | `4615956ddad16a1de0c360886fa0932f` | élevé |
| Carbon Vote (DAO Fork, juin-juillet 2016) | Qui gouverne réellement ? (`qui-gouverne-reellement`) | nom exact → `22ad3d8ee30544a48c02a1a83fa99413` — Carbon Vote (DAO Fork, juin-juillet 2016) | aucune | `22ad3d8ee30544a48c02a1a83fa99413` | élevé |
| Chaîne d'intermédiation sociotechnique | Structure de la thèse (`structure-these`) | nom exact → `1395e56e2f364df4a4add424b87613a3` — Chaîne d'intermédiation sociotechnique | aucune | `1395e56e2f364df4a4add424b87613a3` | élevé |
| Code is Law | Crises (`crises`)<br>Fil de preuves (`fil-de-preuves`)<br>Qui gouverne réellement ? (`qui-gouverne-reellement`) | nom exact → `d337ebdb9be74af2b5324f472235f095` — Code is Law | aucune | `d337ebdb9be74af2b5324f472235f095` | élevé |
| Code Source Ouvert | Fil de preuves (`fil-de-preuves`) | nom exact → `7bfdb4a56f1d40d9aa63f3ad11e44b44` — Code Source Ouvert | aucune | `7bfdb4a56f1d40d9aa63f3ad11e44b44` | élevé |
| Communaute de paiement / Groupe monetaire | Fil de preuves (`fil-de-preuves`)<br>Structure de la thèse (`structure-these`) | nom exact → `92b00fd0ab9049cea901c66a63c8fc1f` — Communaute de paiement / Groupe monetaire | aucune | `92b00fd0ab9049cea901c66a63c8fc1f` | élevé |
| Communauté de paiement | Monétisation des cryptomonnaies (`monetisation-cryptos`) | alias exact → `92b00fd0ab9049cea901c66a63c8fc1f` — Communaute de paiement / Groupe monetaire | aucune | `92b00fd0ab9049cea901c66a63c8fc1f` | élevé |
| Confiance | Monétisation des cryptomonnaies (`monetisation-cryptos`) | alias exact → `9e63b6e996b3416dbcc1a94f8ff0ae50` — Confiance monetaire | aucune | `9e63b6e996b3416dbcc1a94f8ff0ae50` | élevé |
| Consensus global | Crises (`crises`) | alias exact → `73b638dd42ef432fbc15fe98026e65e3` — Gouvernance publique et ouverte | aucune | `73b638dd42ef432fbc15fe98026e65e3` | élevé |
| Consensus local | Crises (`crises`) | alias exact → `a22f20aea49d4f86ab927e9c71d0a850` — Gouvernance de huis clos | aucune | `a22f20aea49d4f86ab927e9c71d0a850` | élevé |
| Consensus social | Crises (`crises`)<br>Qui gouverne réellement ? (`qui-gouverne-reellement`) | nom exact → `24e5eafb0b1e46e6a06b390f9ff579aa` — Consensus social | aucune | `24e5eafb0b1e46e6a06b390f9ff579aa` | élevé |
| Convertibilité | Monétisation des cryptomonnaies (`monetisation-cryptos`) | alias exact → `f36a2cc8e26542cf990b587e13d4f178` — Dilemme de la poule et de l'œuf (bootstrapping monétaire) | aucune | `f36a2cc8e26542cf990b587e13d4f178` | élevé |
| Core Developers (Bitcoin) | Fil de preuves (`fil-de-preuves`) | nom exact → `7b29b0d2d8404396bbaa5742e07d8f21` — Core Developers (Bitcoin) | aucune | `7b29b0d2d8404396bbaa5742e07d8f21` | élevé |
| Core Developers (Ethereum) | Qui gouverne réellement ? (`qui-gouverne-reellement`) | nom exact → `c5f0d6a944544c3c93bdd731dbc83096` — Core Developers (Ethereum) | aucune | `c5f0d6a944544c3c93bdd731dbc83096` | élevé |
| Crise de vulnérabilité | Crises (`crises`) | nom exact → `68c6592878a34164a5a37edc8c49382d` — Crise de vulnérabilité | aucune | `68c6592878a34164a5a37edc8c49382d` | élevé |
| Crise d’évolution | Crises (`crises`) | alias exact → `5cf3c3e7fefd424280ef88908b0add9b` — Crise d'évolution | aucune | `5cf3c3e7fefd424280ef88908b0add9b` | élevé |
| Crises | Crises (`crises`) | alias exact → `923f4b0fd9894482a767e69a115b2799` — Crises comme épreuves d’explicitation | aucune | `923f4b0fd9894482a767e69a115b2799` | élevé |
| Crises comme épreuves d’explicitation | Fil de preuves (`fil-de-preuves`)<br>Structure de la thèse (`structure-these`) | nom exact → `923f4b0fd9894482a767e69a115b2799` — Crises comme épreuves d’explicitation | aucune | `923f4b0fd9894482a767e69a115b2799` | élevé |
| Critiques chartalistes | Monétisation des cryptomonnaies (`monetisation-cryptos`) | alias exact → `fc76177e8cc9b4a6dff45672173edc07` — Théorie chartaliste | aucune | `fc76177e8cc9b4a6dff45672173edc07` | élevé |
| Critiques instrumentales | Monétisation des cryptomonnaies (`monetisation-cryptos`) | alias exact → `f07c8415a468b6c900bd14b3cefa24fb` — II.1.1 — Critiques instrumentales fondées sur les fonctions monétaires canoniques | aucune | `f07c8415a468b6c900bd14b3cefa24fb` | élevé |
| cryptomonnaie | Fil de preuves (`fil-de-preuves`)<br>Monétisation des cryptomonnaies (`monetisation-cryptos`)<br>Structure de la thèse (`structure-these`) | nom exact → `bed4df005c7ce36030703bd68cb521d1` — cryptomonnaie | aucune | `bed4df005c7ce36030703bd68cb521d1` | élevé |
| Dette | Monétisation des cryptomonnaies (`monetisation-cryptos`) | alias exact → `27360a2100034d8b869844e64dc869c5` — Monnaie dette / Monnaie crédit | aucune | `27360a2100034d8b869844e64dc869c5` | élevé |
| Discretion contrainte | Structure de la thèse (`structure-these`) | nom exact → `afc0d50c564647839eaf83ccbae5a463` — Discretion contrainte | aucune | `afc0d50c564647839eaf83ccbae5a463` | élevé |
| Divulgation responsable | Fil de preuves (`fil-de-preuves`) | nom exact → `2f54deb5da1440c8bdd5ca16dbc8c647` — Divulgation responsable | aucune | `2f54deb5da1440c8bdd5ca16dbc8c647` | élevé |
| Développement carnavalesque | Structure de la thèse (`structure-these`) | nom exact → `a34001a6571f4fdf8ae13d5e3b64587b` — Développement carnavalesque | aucune | `a34001a6571f4fdf8ae13d5e3b64587b` | élevé |
| Développeurs Core (mainteneurs avec accès commit) | Qui gouverne réellement ? (`qui-gouverne-reellement`) | nom exact → `8d48bd51752d4c838a92d08261e1fe13` — Développeurs Core (mainteneurs avec accès commit) | aucune | `8d48bd51752d4c838a92d08261e1fe13` | élevé |
| Esprit communautaire | Crises (`crises`) | alias exact → `26edc95bf98c4de399f95486dcd3ceb4` — Esprit du code vs Lettre du code | aucune | `26edc95bf98c4de399f95486dcd3ceb4` | élevé |
| Ethereum | Crises (`crises`)<br>Fil de preuves (`fil-de-preuves`)<br>Structure de la thèse (`structure-these`) | nom exact → `2956b3b87db1448f8a2ddde82d39e9c9` — Ethereum | aucune | `2956b3b87db1448f8a2ddde82d39e9c9` | élevé |
| Ethereum Classic | Crises (`crises`) | alias exact → `5ea44d21a07d4d13a6f1d6677936b8e7` — Ethereum Classic (ETHC) | aucune | `5ea44d21a07d4d13a6f1d6677936b8e7` | élevé |
| Ethereum DAO Hard Fork | Crises (`crises`) | alias exact → `e2cdb978bbdd4119aa946a271051a753` — Ethereum Hard Fork (juillet 2016) | aucune | `e2cdb978bbdd4119aa946a271051a753` | élevé |
| Ethereum Hard Fork (juillet 2016) | Structure de la thèse (`structure-these`) | nom exact → `e2cdb978bbdd4119aa946a271051a753` — Ethereum Hard Fork (juillet 2016) | aucune | `e2cdb978bbdd4119aa946a271051a753` | élevé |
| Ethnographie | Structure de la thèse (`structure-these`) | nom exact → `f788033ee36c478d8fbe59d5e3825d95` — Ethnographie | aucune | `f788033ee36c478d8fbe59d5e3825d95` | élevé |
| Fonctions monétaires | Monétisation des cryptomonnaies (`monetisation-cryptos`) | alias exact → `f07c8415a468b6c900bd14b3cefa24fb` — II.1.1 — Critiques instrumentales fondées sur les fonctions monétaires canoniques | aucune | `f07c8415a468b6c900bd14b3cefa24fb` | élevé |
| GitHub Bitcoin Core | Qui gouverne réellement ? (`qui-gouverne-reellement`) | nom exact → `344699b9593049aab807def5c05579cc` — GitHub Bitcoin Core | aucune | `344699b9593049aab807def5c05579cc` | élevé |
| Gouvernance de huis clos | Crises (`crises`)<br>Fil de preuves (`fil-de-preuves`)<br>Structure de la thèse (`structure-these`) | nom exact → `a22f20aea49d4f86ab927e9c71d0a850` — Gouvernance de huis clos | aucune | `a22f20aea49d4f86ab927e9c71d0a850` | élevé |
| Gouvernance des cryptomonnaies | Crises (`crises`) | alias exact → `0fcc7028560c47cc9b82309f469b700c` — A. La gouvernance des cryptomonnaies : construction de notre objet de recherche | aucune | `0fcc7028560c47cc9b82309f469b700c` | élevé |
| Gouvernance duale | Crises (`crises`)<br>Fil de preuves (`fil-de-preuves`)<br>Qui gouverne réellement ? (`qui-gouverne-reellement`)<br>Structure de la thèse (`structure-these`) | nom exact → `a432cc76f9ea4e949e374476082b89ab` — Gouvernance duale | aucune | `a432cc76f9ea4e949e374476082b89ab` | élevé |
| Gouvernance polycentrique | Crises (`crises`)<br>Fil de preuves (`fil-de-preuves`)<br>Monétisation des cryptomonnaies (`monetisation-cryptos`)<br>Qui gouverne réellement ? (`qui-gouverne-reellement`)<br>Structure de la thèse (`structure-these`) | nom exact → `a444085b9b2d4ea1aa734f7e25db6a6c` — Gouvernance polycentrique | aucune | `a444085b9b2d4ea1aa734f7e25db6a6c` | élevé |
| Gouvernance publique | Crises (`crises`) | alias exact → `73b638dd42ef432fbc15fe98026e65e3` — Gouvernance publique et ouverte | aucune | `73b638dd42ef432fbc15fe98026e65e3` | élevé |
| Gouvernance publique et ouverte | Structure de la thèse (`structure-these`) | nom exact → `73b638dd42ef432fbc15fe98026e65e3` — Gouvernance publique et ouverte | aucune | `73b638dd42ef432fbc15fe98026e65e3` | élevé |
| Hard Fork | Crises (`crises`) | nom exact → `a8108e74b9d9483bb66d929e347fd7bd` — Hard Fork | aucune | `a8108e74b9d9483bb66d929e347fd7bd` | élevé |
| II.3 Au‑delà de la revendication d’une absence de gouvernance ! | Fil de preuves (`fil-de-preuves`)<br>Qui gouverne réellement ? (`qui-gouverne-reellement`) | nom exact → `d622d318825741cda43212d7831a88c7` — II.3 Au‑delà de la revendication d’une absence de gouvernance ! | aucune | `d622d318825741cda43212d7831a88c7` | élevé |
| Infrastructure sociotechnique | Fil de preuves (`fil-de-preuves`) | nom exact → `e1a7b06839404dbdacba7f00782a5450` — Infrastructure sociotechnique | aucune | `e1a7b06839404dbdacba7f00782a5450` | élevé |
| Infrastructures de marché | Monétisation des cryptomonnaies (`monetisation-cryptos`) | alias exact → `f6c7446fa0fe4f318142a09f4848f84f` — Infrastructure monétaire crypto-monétaire | aucune | `f6c7446fa0fe4f318142a09f4848f84f` | élevé |
| Institutionnalisme intéressé aux usages | Structure de la thèse (`structure-these`) | nom exact → `21107fb980daa17e698237df5d7daa2f` — Institutionnalisme intéressé aux usages | aucune | `21107fb980daa17e698237df5d7daa2f` | élevé |
| Institutionnalisme Monetaire Francophone (IMF) | Structure de la thèse (`structure-these`) | nom exact → `2e24bde03cad4d56b1c0c012d7cf1e57` — Institutionnalisme Monetaire Francophone (IMF) | aucune | `2e24bde03cad4d56b1c0c012d7cf1e57` | élevé |
| Institutions | Monétisation des cryptomonnaies (`monetisation-cryptos`) | alias exact → `2e24bde03cad4d56b1c0c012d7cf1e57` — Institutionnalisme Monetaire Francophone (IMF) | aucune | `2e24bde03cad4d56b1c0c012d7cf1e57` | élevé |
| Intermédiation | Monétisation des cryptomonnaies (`monetisation-cryptos`) | alias exact → `1395e56e2f364df4a4add424b87613a3` — Chaîne d'intermédiation sociotechnique | aucune | `1395e56e2f364df4a4add424b87613a3` | élevé |
| Liquidité | Monétisation des cryptomonnaies (`monetisation-cryptos`) | alias exact → `1457c3a130204346b3e3919b88fd10f3` — Concept — Liquidité du marché Bitcoin | aucune | `1457c3a130204346b3e3919b88fd10f3` | élevé |
| Mise en crise | Crises (`crises`) | alias exact → `586e00d1ca15450ca9b25fe4595bc662` — Mise en crise / Remise en ordre | aucune | `586e00d1ca15450ca9b25fe4595bc662` | élevé |
| Monetary Institutionalism FR (IMF) | Monétisation des cryptomonnaies (`monetisation-cryptos`) | alias exact → `2e24bde03cad4d56b1c0c012d7cf1e57` — Institutionnalisme Monetaire Francophone (IMF) | aucune | `2e24bde03cad4d56b1c0c012d7cf1e57` | élevé |
| Monnaie | Monétisation des cryptomonnaies (`monetisation-cryptos`) | nom exact → `e94facdafe5a431e83e96a6060c5c862` — Monnaie | aucune | `e94facdafe5a431e83e96a6060c5c862` | élevé |
| Monétisation | Monétisation des cryptomonnaies (`monetisation-cryptos`) | alias exact → `de6da7fa28334c408e51269ba447a482` — Monétisation des cryptomonnaies | aucune | `de6da7fa28334c408e51269ba447a482` | élevé |
| Monétisation des cryptomonnaies | Structure de la thèse (`structure-these`) | nom exact → `de6da7fa28334c408e51269ba447a482` — Monétisation des cryptomonnaies | aucune | `de6da7fa28334c408e51269ba447a482` | élevé |
| Neutralité de la monnaie | Qui gouverne réellement ? (`qui-gouverne-reellement`) | nom exact → `ef3943810af1439d8380f4986b125303` — Neutralité de la monnaie | aucune | `ef3943810af1439d8380f4986b125303` | élevé |
| Nominalisme non étatiste | Monétisation des cryptomonnaies (`monetisation-cryptos`) | alias exact → `c4ff6f8bb34a4bc4acf61ebb16943bde` — Nominalisme monetaire non etatiste | aucune | `c4ff6f8bb34a4bc4acf61ebb16943bde` | élevé |
| Paiement | Monétisation des cryptomonnaies (`monetisation-cryptos`) | alias exact → `202442f070694e70a001e5cdb1b03fe0` — Systeme de paiement | aucune | `202442f070694e70a001e5cdb1b03fe0` | élevé |
| Passerelles | Monétisation des cryptomonnaies (`monetisation-cryptos`) | alias exact → `16f9e7387f55457b80450f5add3707ef` — Services Marchands & Passerelles | aucune | `16f9e7387f55457b80450f5add3707ef` | élevé |
| Patch | Crises (`crises`) | alias exact → `73712fc1060c48fc8bcc52b1dee2137c` — CVE-2018-17144 — Remise en ordre par patch | aucune | `73712fc1060c48fc8bcc52b1dee2137c` | élevé |
| Pull Request (PR) | Qui gouverne réellement ? (`qui-gouverne-reellement`) | nom exact → `9e9eac4d98ca4d27892e19d17415a7b7` — Pull Request (PR) | aucune | `9e9eac4d98ca4d27892e19d17415a7b7` | élevé |
| Remise en ordre | Crises (`crises`) | alias exact → `586e00d1ca15450ca9b25fe4595bc662` — Mise en crise / Remise en ordre | aucune | `586e00d1ca15450ca9b25fe4595bc662` | élevé |
| Responsible disclosure | Crises (`crises`) | alias exact → `018cb3c562674948be30d910d68359c3` — Responsible Disclosure | aucune | `018cb3c562674948be30d910d68359c3` | élevé |
| Règle comme cristallisation normative située | Structure de la thèse (`structure-these`) | nom exact → `615f6147214c43ab830a98ca866779c3` — Règle comme cristallisation normative située | aucune | `615f6147214c43ab830a98ca866779c3` | élevé |
| Règle contre discrétion (Rules vs Discretion) | Structure de la thèse (`structure-these`) | nom exact → `0c0929e6ef0140ad855052b0dd078f00` — Règle contre discrétion (Rules vs Discretion) | aucune | `0c0929e6ef0140ad855052b0dd078f00` | élevé |
| Satoshi Nakamoto | Structure de la thèse (`structure-these`) | nom exact → `10960c9c308b4a3dad7ff86a20a1d2b5` — Satoshi Nakamoto | aucune | `10960c9c308b4a3dad7ff86a20a1d2b5` | élevé |
| Services Marchands & Passerelles | Structure de la thèse (`structure-these`) | nom exact → `16f9e7387f55457b80450f5add3707ef` — Services Marchands & Passerelles | aucune | `16f9e7387f55457b80450f5add3707ef` | élevé |
| Smart Contracts | Structure de la thèse (`structure-these`) | nom exact → `0509d0c5196545e2aece85e595fe55c5` — Smart Contracts | aucune | `0509d0c5196545e2aece85e595fe55c5` | élevé |
| Sociology of Science & Technology (STS) | Structure de la thèse (`structure-these`) | nom exact → `af85409fa95f43adb9fc7ece46ed4b15` — Sociology of Science & Technology (STS) | aucune | `af85409fa95f43adb9fc7ece46ed4b15` | élevé |
| Souveraineté monétaire | Monétisation des cryptomonnaies (`monetisation-cryptos`) | alias exact → `f018e4490ac24705a1017203d60a97d1` — Souverainete monetaire | aucune | `f018e4490ac24705a1017203d60a97d1` | élevé |
| Space of Rule / Space of Discretion | Crises (`crises`)<br>Structure de la thèse (`structure-these`) | nom exact → `fba623af07644327b873a59e0a9b2f97` — Space of Rule / Space of Discretion | aucune | `fba623af07644327b873a59e0a9b2f97` | élevé |
| Statut monétaire des cryptomonnaies | Monétisation des cryptomonnaies (`monetisation-cryptos`) | nom exact → `805879ef12780478a182ee9ce35257f9` — Statut monétaire des cryptomonnaies | aucune | `805879ef12780478a182ee9ce35257f9` | élevé |
| Syllogisme libéral-techniciste | Fil de preuves (`fil-de-preuves`)<br>Structure de la thèse (`structure-these`) | nom exact → `c0e67b8798b946019cd324b2cce929ed` — Syllogisme libéral-techniciste | aucune | `c0e67b8798b946019cd324b2cce929ed` | élevé |
| The DAO | Crises (`crises`)<br>Structure de la thèse (`structure-these`) | nom exact → `ed7b68eeb3114b32a7ab0baabd62cc5a` — The DAO | aucune | `ed7b68eeb3114b32a7ab0baabd62cc5a` | élevé |
| Thèse centrale (infrastructures, crises, gouvernance polycentrique) | Crises (`crises`)<br>Monétisation des cryptomonnaies (`monetisation-cryptos`)<br>Structure de la thèse (`structure-these`) | nom exact → `a4bbdf3c65394e31bcbb33cc00c64303` — Thèse centrale (infrastructures, crises, gouvernance polycentrique) | aucune | `a4bbdf3c65394e31bcbb33cc00c64303` | élevé |
| UCN BTC | Monétisation des cryptomonnaies (`monetisation-cryptos`)<br>Structure de la thèse (`structure-these`) | nom exact → `c74c47caffc64382b31bc5eb221b7db7` — UCN BTC | aucune | `c74c47caffc64382b31bc5eb221b7db7` | élevé |
| UCN ETH | Monétisation des cryptomonnaies (`monetisation-cryptos`)<br>Structure de la thèse (`structure-these`) | nom exact → `b5d5510775234885a665faa665ee6960` — UCN ETH | aucune | `b5d5510775234885a665faa665ee6960` | élevé |
| Usage en compte | Monétisation des cryptomonnaies (`monetisation-cryptos`) | alias exact → `c622e5a68f014acaaad86e7cb080ec1b` — Archetypal monetary functions | aucune | `c622e5a68f014acaaad86e7cb080ec1b` | élevé |
| Usage en paiement | Monétisation des cryptomonnaies (`monetisation-cryptos`) | alias exact → `202442f070694e70a001e5cdb1b03fe0` — Systeme de paiement | aucune | `202442f070694e70a001e5cdb1b03fe0` | élevé |
| Usages monétaires | Monétisation des cryptomonnaies (`monetisation-cryptos`) | alias exact → `5b5935bc3ede49028b7dfbdaa4f34b6d` — Chapitre II - Dépasser la controverse du statut monétaire des CM par un institutionnalisme intéressé aux usages | aucune | `5b5935bc3ede49028b7dfbdaa4f34b6d` | élevé |
| Vitalik Buterin | Structure de la thèse (`structure-these`) | nom exact → `bf653891dd9e4c1cbf23f40e4609f55b` — Vitalik Buterin | aucune | `bf653891dd9e4c1cbf23f40e4609f55b` | élevé |
| Épreuve d’explicitation de la monnaie | Monétisation des cryptomonnaies (`monetisation-cryptos`) | alias exact → `c6fadcf486a54b64ad07f6652e49fb53` — Quote — CM comme épreuve d’explicitation de la monnaie | aucune | `c6fadcf486a54b64ad07f6652e49fb53` | élevé |

## 4. Risques et limites

- L’audit vérifie la résolution des labels vers des entités v96 ; il ne vérifie pas que chaque focus est scientifiquement optimal pour le récit.
- Les alias runtime sont efficaces mais masquent une dette éditoriale : plusieurs labels narratifs ne correspondent pas directement aux noms canoniques du graphe.
- Aucune modification n’est proposée ici dans `story-presets.mjs` : un alignement éventuel des labels doit rester une future PR runtime/documentée.
