#!/usr/bin/env python3
import csv, json, unicodedata
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MIG = ROOT / 'Migration'

TABLE = MIG / 'grc20_v91_migration_table.csv'
BASE_PATCH = MIG / 'grc20_v91_name_based_patch.json'
GRAPH = ROOT / 'grc20-these-mael-rolland-v96.json'
OUTDIR = MIG / 'v97_lots'
OUTDIR.mkdir(exist_ok=True)


def norm(s: str) -> str:
    s = (s or '').strip().lower()
    s = ''.join(c for c in unicodedata.normalize('NFD', s) if unicodedata.category(c) != 'Mn')
    return ' '.join(s.split())

with TABLE.open(newline='', encoding='utf-8') as f:
    ops = list(csv.DictReader(f))
with BASE_PATCH.open(encoding='utf-8') as f:
    base = json.load(f)
with GRAPH.open(encoding='utf-8') as f:
    g = json.load(f)

entities = [e['name'] for e in g['entities'] if 'name' in e]
by_norm = {norm(n): n for n in entities}

for op in ops:
    if op.get('confidence'):
        op['confidence'] = float(op['confidence'])

concept_targets = {'CoreConcept','SecondaryConcept','TechnicalConcept','NativeFormula','ChapterSection','AnalyticClaim'}
lot1 = []
lot2 = []
lot3 = []

for op in ops:
    old_type = op['old_type']
    new_type = op['new_type']
    action = op['action']

    if old_type == 'Concept' or new_type in concept_targets:
        lot1.append(op)
        continue

    if (
        (old_type == 'ActorNonHuman' and new_type in {'InfrastructureService','SoftwareClient'})
        or (new_type == 'StakeholderGroup')
    ):
        lot2.append(op)
        continue

# Add explicit remaining ActorNonHuman split from the user's gap list
explicit_actor_ops = [
    ('AntPool', 'InfrastructureService'),
    ('F2Pool', 'InfrastructureService'),
    ('GHash.io', 'InfrastructureService'),
    ('Slush Pool', 'InfrastructureService'),
    ('BTC Guild', 'InfrastructureService'),
    ('Bitcoin ABC', 'SoftwareClient'),
    ('Bitcoin Knots', 'SoftwareClient'),
    ('Bitcoin Unlimited', 'SoftwareClient'),
]
existing_actor_keys = {(o['old_entity'], o['new_type']) for o in lot2}
for name, target_type in explicit_actor_ops:
    key = (name, target_type)
    if key in existing_actor_keys:
        continue
    lot2.append({
        'old_entity': name,
        'old_type': 'ActorNonHuman',
        'action': 'retype',
        'new_entity': name,
        'new_type': target_type,
        'confidence': 0.99,
        'rationale': 'explicit split from ActorNonHuman remaining backlog',
    })

# Add explicit unresolved alias fixes from user brief
extra_lot1 = [
    {
        'old_entity': 'Nominalisme monétaire non étatiste',
        'old_type': 'Concept',
        'action': 'merge_into',
        'new_entity': 'Nominalisme monetaire non etatiste',
        'new_type': 'Concept',
        'confidence': 0.99,
        'rationale': 'accent canonicalization requested in remaining gaps list',
    },
    {
        'old_entity': 'Politique de crises',
        'old_type': 'Concept',
        'action': 'merge_into',
        'new_entity': 'Politique de crise',
        'new_type': 'Concept',
        'confidence': 0.93,
        'rationale': 'plural/singular canonicalization requested in remaining gaps list',
    },
    {
        'old_entity': 'Ethereum Virtual Machine',
        'old_type': 'Concept',
        'action': 'merge_into',
        'new_entity': 'Ethereum Virtual Machine (EVM)',
        'new_type': 'ConceptTechnical',
        'confidence': 0.98,
        'rationale': 'normalize to canonical labeled entity present in graph',
    },
]

existing_keys = {(o['old_entity'], o['action'], o['new_entity']) for o in lot1}
for op in extra_lot1:
    k = (op['old_entity'], op['action'], op['new_entity'])
    if k not in existing_keys:
        lot1.append(op)

# lot3 relations + infra domains
relations = [r for r in base.get('new_relations', []) if r['predicate'] in {'instanceOfCategory','organizes','partOfMonetizationProcess'}]
# Add missing stakeholder relation explicitly expected
relations.extend([
    {'subject': 'Mineurs Bitcoin', 'predicate': 'instanceOfCategory', 'object': 'Mineurs et assimilés'},
    {'subject': 'Pools de minage', 'predicate': 'instanceOfCategory', 'object': 'Mineurs et assimilés'},
    {'subject': 'Opérateurs de nœuds complets', 'predicate': 'instanceOfCategory', 'object': 'Nœuds complets (Full Nodes)'},
    {'subject': 'Fournisseurs de portefeuilles', 'predicate': 'instanceOfCategory', 'object': 'Fournisseurs de portefeuilles'},
])
# dedupe
seen = set(); dedup_rel=[]
for r in relations:
    k=(r['subject'],r['predicate'],r['object'])
    if k in seen: continue
    seen.add(k); dedup_rel.append(r)
relations=dedup_rel

lot3 = {
    'canonical_infrastructure_domains_target': [
        'Protocole et couche de base',
        'Traitement des transactions',
        'Altcoins, tokens et surcouches',
        'Services de portefeuille et de paiement',
        'Conformité réglementaire',
        'Sphère d’usage',
        'Information et connaissance',
        'Monétisation',
        'Gouvernance infrastructurelle'
    ],
    'relations_to_add': relations
}


def exists_name(name: str) -> bool:
    return norm(name) in by_norm

# add resolution hints
for op in lot1 + lot2:
    op['old_entity_exists_v96'] = exists_name(op['old_entity'])
    op['new_entity_exists_v96'] = exists_name(op['new_entity'])

for r in lot3['relations_to_add']:
    r['subject_exists_v96'] = exists_name(r['subject'])
    r['object_exists_v96'] = exists_name(r['object'])

payload_common = {
    'patch_series': 'v97-rollout-split',
    'source_graph': 'grc20-these-mael-rolland-v96.json',
}

lot1_payload = {
    **payload_common,
    'lot': 'LOT-1',
    'title': 'Concept hierarchy + unresolved concept merges',
    'operations': lot1,
}
lot2_payload = {
    **payload_common,
    'lot': 'LOT-2',
    'title': 'ActorNonHuman split + StakeholderGroup completion',
    'operations': lot2,
}
lot3_payload = {
    **payload_common,
    'lot': 'LOT-3',
    'title': 'InfrastructureDomain canonization + missing relation families',
    **lot3,
}

(OUTDIR / 'lot-1-concepts.json').write_text(json.dumps(lot1_payload, ensure_ascii=False, indent=2)+"\n", encoding='utf-8')
(OUTDIR / 'lot-2-actors-stakeholders.json').write_text(json.dumps(lot2_payload, ensure_ascii=False, indent=2)+"\n", encoding='utf-8')
(OUTDIR / 'lot-3-infra-relations.json').write_text(json.dumps(lot3_payload, ensure_ascii=False, indent=2)+"\n", encoding='utf-8')

# Planning doc
concept_unclassified = 0
# Concept type id
type_map = {t['name']: t['id'] for t in g['types']}
concept_id = type_map.get('Concept')
if concept_id:
    concept_unclassified = sum(1 for e in g['entities'] if concept_id in e.get('types', []))

md = f"""# v97 rollout en lots (task-by-task)

Base: `grc20-these-mael-rolland-v96.json`.

## LOT-1 — Hiérarchie des concepts
- Fichier: `Migration/v97_lots/lot-1-concepts.json`
- Contenu: retypes `Concept` vers `CoreConcept`/`SecondaryConcept`/`TechnicalConcept`, slogans vers `NativeFormula`, titres de section vers `ChapterSection`, et fusions manquantes (Nominalisme, EVM, Politique de crise[s]).
- Taille: **{len(lot1)} opérations**.

## LOT-2 — ActorNonHuman + StakeholderGroup
- Fichier: `Migration/v97_lots/lot-2-actors-stakeholders.json`
- Contenu: éclatement d'acteurs non humains vers `InfrastructureService` / `SoftwareClient`, + retypes des groupes attendus vers `StakeholderGroup`.
- Taille: **{len(lot2)} opérations**.

## LOT-3 — InfrastructureDomain + nouvelles relations
- Fichier: `Migration/v97_lots/lot-3-infra-relations.json`
- Contenu: cible de 9 domaines canoniques + ajout des relations `instanceOfCategory`, `organizes`, `partOfMonetizationProcess`.
- Taille: **{len(relations)} relations**.

## État restant (avant application)
- Entités avec type `Concept` encore non hiérarchisé: **{concept_unclassified}**.
- Les 3 lots sont conçus pour être mergés séparément afin d'éviter un diff massif.
"""
(OUTDIR / 'README.md').write_text(md, encoding='utf-8')

print('Generated lots in', OUTDIR)
print('lot1', len(lot1), 'lot2', len(lot2), 'lot3_relations', len(relations))
