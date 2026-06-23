# Argos V97 — Correction des relations cassées (15 tronquées supprimées)

**Date** : 23 juin 2026
**Branche** : `codex/create-expand-from-node-planning-documents`
**Graphe source** : `grc20-these-mael-rolland-v96.json` (non modifié)
**Graphe produit** : `grc20-these-mael-rolland-v97.json`
**Script** : `scripts/make_v97_remove_truncated_broken_relations.py`
**Patch documentaire** : `patches/grc20_v97_remove_15_truncated_broken_relations.json`

---

## 1. Résumé exécutif

Le graphe **v96** contenait **16 relations cassées** (endpoint `from` manquant). L'audit Argos V0.1 a révélé que **15 d'entre elles étaient des doublons orphelins** issus d'un bug de troncature d'UUID : le champ `from` avait été écrit avec seulement 16 des 32 caractères hex de l'UUID réel, et pour chacune une relation valide identique existait déjà dans le graphe.

Le graphe **v97** supprime ces **15 relations tronquées** sans aucune perte d'information. Les entités, types, relation types et ops sont strictement inchangés.

**1 relation cassée reste volontairement** : `contributes to` → Ostrom 1990 (from `72d182705407492c`), qui est un orphelin véritable sans doublon et à valeur analytique potentielle. Elle est conservée pour **revue humaine**.

- **v96 reste intact** et n'est pas modifié.
- Le site **n'est pas branché** sur v97.
- La correction est **entièrement réversible**.

---

## 2. Relations supprimées (15)

Toutes sont des doublons tronqués : `from` = 16 chars (préfixe d'un UUID réel de 32 chars), et une relation valide identique (même `type`, même `to`, `from` complet) existe déjà dans le graphe.

| Index v96 | Type | From manquant (16 chars) | Entité réelle correspondante | To valide | Raison de suppression |
|---:|---|---|---|---|---|
| 19455 | appears in section | `0170870141524d46` | Black Hat (Concept) | III.2 Des marques… | Doublon tronqué d'une relation valide existante |
| 19456 | appears in section | `c0c1bec510f54099` | White Hat (Concept) | III.2 Des marques… | Doublon tronqué |
| 19457 | appears in section | `f87e9246cf2b407b` | Consensus distribué (Concept) | Chapitre I | Doublon tronqué |
| 19458 | appears in section | `f07878254e144095` | Logique de sceau (Concept) | Chapitre I | Doublon tronqué |
| 19459 | appears in section | `f07878254e144095` | Logique de sceau (Concept) | II.2 « Pourtant… » | Doublon tronqué |
| 19460 | appears in section | `71908f95dad74d9a` | Logique de signature (Concept) | Chapitre I | Doublon tronqué |
| 19461 | appears in section | `71908f95dad74d9a` | Logique de signature (Concept) | II.2 « Pourtant… » | Doublon tronqué |
| 19462 | appears in section | `2af42270c40746e2` | OP_RETURN (TechnicalConcept) | Chapitre I | Doublon tronqué |
| 19464 | appears in section | `571934eb6d074fb8` | Auryn Macmillan (Person) | III.2 Des marques… | Doublon tronqué |
| 19465 | appears in section | `633ccadaea354e76` | Bill Shihara (Person) | Chapitre I | Doublon tronqué |
| 19466 | appears in section | `20b8c4f053744b01` | Tristan D'Agosta (Person) | Chapitre I | Doublon tronqué |
| 19467 | cited in | `53525938440543a5` | Jérôme Favier (Reference) | Introduction générale | Doublon tronqué |
| 19468 | cited in | `53525938440543a5` | Jérôme Favier (Reference) | Chapitre II | Doublon tronqué |
| 19469 | cited in | `fb692ce5f716443f` | Primavera De Filippi (Reference) | Section B | Doublon tronqué |
| 19470 | cited in | `a985149b43e34a43` | The Filter / Griff Green 2016 (Reference) | III.2 Des marques… | Doublon tronqué |

**Cause racune** : bug de double insertion lors d'une migration — la même relation écrite deux fois, dont une copie au `from` tronqué à 16 caractères.

---

## 3. Relation conservée pour revue humaine (1)

| Index v96 | Type | From manquant | To valide | Label To | Pourquoi conservée |
|---:|---|---|---|---|---|
| 19463 | contributes to | `72d182705407492c` | `e3b7d91585004ef7a392934a0b37292f` | Ostrom 1990 | Voir ci-dessous |

### Pourquoi cette relation n'a pas été supprimée

L'ID `72d182705407492c` ne correspond au préfixe d'**aucune** entité existante dans le graphe. Contrairement aux 15 autres relations cassées, il n'existe **aucun doublon valide** pour celle-ci. Il s'agit d'un véritable orphelin : une entité source a été supprimée, fusionnée ou a vu son UUID régénéré lors d'une migration, sans que la relation pointant vers Ostrom 1990 ne soit nettoyée.

La cible « Ostrom 1990 » (Reference) possède déjà deux relations `contributes to` valides (Social Ecological System, Common Pool Resources). Le lien cassé suggère l'existence d'un **troisième contributeur** disparu — probablement un concept d'analyse institutionnelle (polycentricity, action arena, IAD framework) qui aurait dû être lié à Ostrom 1990.

Cette relation a une **valeur analytique potentielle** : la supprimer effacerait la trace d'un lien conceptuel entre la thèse et le cadre IAD d'Ostrom. La décision doit être prise par un humain qui peut :

1. **Identifier** le concept manquant (demander à Maël s'il reconnaît un lien Ostrom disparu).
2. **Recréer** l'entité et la relation si pertinent.
3. **Supprimer** la relation cassée si le lien n'est pas pertinent.

---

## 4. Validation Argos

### Commandes exécutées

```
python3 scripts/audit_graph.py --input grc20-these-mael-rolland-v96.json --json /tmp/argos-v96.json --quiet
python3 scripts/audit_graph.py --input grc20-these-mael-rolland-v97.json --json /tmp/argos-v97.json --quiet
```

### Résultats

| Métrique | v96 | v97 | Δ |
|---|---:|---:|---|
| Entités | 2 263 | 2 263 | 0 |
| Relations | 20 057 | 20 042 | -15 |
| Types | 55 | 55 | 0 |
| Relation types | 130 | 130 | 0 |
| Ops | 293 | 293 | 0 |
| Relations cassées (`from`) | 16 | 1 | -15 |
| Relations cassées (`to`) | 0 | 0 | 0 |
| Orphelins | 0 | 0 | 0 |

### Relation cassée restante dans v97

```
index: 19455 (nouvel index dans v97)
type: contributes to
from: 72d182705407492c (manquant)
to: e3b7d91585004ef7a392934a0b37292f → "Ostrom 1990"
problem: missing_from
```

### Exit codes

- **v96** : exit 1 (16 relations cassées — critique) ✓
- **v97** : exit 1 (1 relation cassée conservée volontairement — toujours critique) ✓

L'exit code 1 sur v97 est **attendu et correct** : une relation critique est délibérément conservée.

---

## 5. Rollback

Pour revenir intégralement à l'état v96 :

```bash
# 1. Supprimer v97
rm grc20-these-mael-rolland-v97.json

# 2. Le patch documentaire peut rester (il décrit l'opération, n'affecte pas le graphe)
# Mais pour un rollback complet :
rm patches/grc20_v97_remove_15_truncated_broken_relations.json

# 3. Le graphe v96 n'a jamais été modifié — continuer à l'utiliser tel quel.
```

Le fichier `v96` est strictement identique à son état d'origine (vérifié par `git status`).

---

## 6. Prochaines étapes

1. **Revue humaine de la relation Ostrom** — demander à Maël s'il reconnaît un concept lié à Ostrom 1990 qui aurait disparu du graphe.
2. **Décision** : supprimer la relation cassée, la réparer (recréer l'entité), ou la laisser.
3. **Si suppression** : produire v97.1 ou v98 avec la dernière relation cassée retirée → Argos exit 0.
4. **Ne pas brancher le frontend sur v97** avant validation humaine complète.
5. **Prochain patch recommandé** : `scripts/audit_stories.py` (détection des focus nodes non résolus).

---

*Ce rapport est commité avec v97. Le graphe v96 reste intact et canonique jusqu'à décision contraire.*
