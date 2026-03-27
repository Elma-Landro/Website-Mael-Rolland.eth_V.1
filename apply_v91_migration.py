#!/usr/bin/env python3
"""
GRC-20 v90 → v91 migration script
Applies Migration/grc20_v91_patch_seed.json to grc20-these-mael-rolland-v90.json
Produces grc20-these-mael-rolland-v91.json + grc20_v91_migration_report.json
"""

import json
import uuid
import unicodedata
import re
from copy import deepcopy
from collections import defaultdict

# ── helpers ──────────────────────────────────────────────────────────────────

def new_id():
    return uuid.uuid4().hex

def normalize(s):
    """Lowercase, strip accents, collapse spaces — for fuzzy name matching."""
    s = s.lower().strip()
    s = unicodedata.normalize('NFD', s)
    s = ''.join(c for c in s if unicodedata.category(c) != 'Mn')
    s = re.sub(r'\s+', ' ', s)
    return s

def make_type(name):
    return {
        "id": new_id(),
        "name": name,
        "description": {"type": "TEXT", "value": name, "options": {"language": "en"}}
    }

def make_relation_type(name):
    return {
        "id": new_id(),
        "name": name,
        "description": {"type": "TEXT", "value": name, "options": {"language": "en"}}
    }

def make_relation(rt_id, from_id, to_id):
    return {
        "id": new_id()[:22],
        "type": rt_id,
        "from": from_id,
        "to": to_id,
        "attributes": {}
    }

# ── load ─────────────────────────────────────────────────────────────────────

print("Loading v90 graph...")
with open('grc20-these-mael-rolland-v90.json') as f:
    graph = json.load(f)

with open('Migration/grc20_v91_patch_seed.json') as f:
    seed = json.load(f)

with open('Migration/grc20_v91_name_based_patch.json') as f:
    name_patch = json.load(f)

# ── build indexes ────────────────────────────────────────────────────────────

entities = graph['entities']       # list of entity dicts
relations = graph['relations']     # list of relation dicts
types = graph['types']             # list of type dicts
relation_types = graph['relation_types']  # list of relation-type dicts

type_by_name   = {t['name']: t['id'] for t in types}
type_by_id     = {t['id']: t['name'] for t in types}
rt_by_name     = {rt['name']: rt['id'] for rt in relation_types}
rt_by_id       = {rt['id']: rt['name'] for rt in relation_types}

entity_by_id   = {e['id']: e for e in entities}
# exact name lookup
entity_by_name = {}
entity_by_norm = {}   # normalized
for e in entities:
    entity_by_name[e['name']] = e
    entity_by_norm[normalize(e['name'])] = e

def find_entity(name):
    """Resolve entity name → entity dict (exact then normalized)."""
    if name in entity_by_name:
        return entity_by_name[name]
    n = normalize(name)
    if n in entity_by_norm:
        return entity_by_norm[n]
    return None

def get_or_create_type(name):
    if name in type_by_name:
        return type_by_name[name]
    t = make_type(name)
    types.append(t)
    type_by_name[name] = t['id']
    type_by_id[t['id']] = name
    report['created_types'].append(name)
    return t['id']

def get_or_create_rt(name):
    if name in rt_by_name:
        return rt_by_name[name]
    rt = make_relation_type(name)
    relation_types.append(rt)
    rt_by_name[name] = rt['id']
    rt_by_id[rt['id']] = name
    report['created_relation_types'].append(name)
    return rt['id']

# ── report ───────────────────────────────────────────────────────────────────

report = {
    "from_version": "v90",
    "to_version": "v91",
    "created_types": [],
    "created_relation_types": [],
    "merges_applied": [],
    "merges_failed": [],
    "retypes_applied": [],
    "retypes_failed": [],
    "domains_canonicalized": [],
    "new_relations_added": [],
    "manual_review": [],
    "stats": {}
}

deleted_ids = set()   # entity IDs to remove at end

# ── phase 1 : create new types ───────────────────────────────────────────────

print("Phase 1: creating new types and relation types...")

for type_name in seed['create_types']:
    get_or_create_type(type_name)

for rt_name in seed['create_relations']:
    get_or_create_rt(rt_name)

print(f"  Created {len(report['created_types'])} types, {len(report['created_relation_types'])} relation types")

# ── phase 2 : merge entities ─────────────────────────────────────────────────

print("Phase 2: merging duplicate entities...")

for op in seed['merge_entities']:
    canonical_name = op['canonical']
    aliases        = op.get('aliases', [])
    confidence     = op.get('confidence', 'strong')

    target = find_entity(canonical_name)
    if target is None:
        report['merges_failed'].append({
            'canonical': canonical_name,
            'reason': 'canonical not found'
        })
        continue

    for alias_name in aliases:
        source = find_entity(alias_name)
        if source is None:
            report['merges_failed'].append({
                'canonical': canonical_name,
                'alias': alias_name,
                'reason': 'alias entity not found'
            })
            continue
        if source['id'] == target['id']:
            continue  # same entity, skip

        src_id = source['id']
        tgt_id = target['id']

        # redirect all relations
        redirected = 0
        for rel in relations:
            if rel['from'] == src_id:
                rel['from'] = tgt_id
                redirected += 1
            if rel['to'] == src_id:
                rel['to'] = tgt_id
                redirected += 1

        # store alias on target
        attrs = target.get('attributes')
        if not isinstance(attrs, dict):
            target['attributes'] = {}
            attrs = target['attributes']
        existing_aliases = attrs.get('aliases', {}).get('value', '') if isinstance(attrs.get('aliases'), dict) else ''
        alias_list = [a.strip() for a in existing_aliases.split('|') if a.strip()] if existing_aliases else []
        if source['name'] not in alias_list:
            alias_list.append(source['name'])
        attrs['aliases'] = {"type": "TEXT", "value": ' | '.join(alias_list), "options": {"language": "fr"}}

        # mark source for deletion
        deleted_ids.add(src_id)

        report['merges_applied'].append({
            'canonical': canonical_name,
            'merged': alias_name,
            'relations_redirected': redirected,
            'confidence': confidence
        })

print(f"  Merges applied: {len(report['merges_applied'])}, failed: {len(report['merges_failed'])}")

# ── phase 3 : retype entities ────────────────────────────────────────────────

print("Phase 3: retyping misclassified entities...")

# Accumulate retypes from both sources (seed primary, name_patch supplement)
retype_ops = []
seen_retype = set()

for op in seed.get('retype_entities', []):
    key = op['entity']
    if key not in seen_retype:
        seen_retype.add(key)
        retype_ops.append(op)

# Supplement from name_based_patch
for op in name_patch.get('operations', []):
    if op['action'] in ('retype', 'keep_promote', 'rename_retype'):
        key = op['old_entity']
        if key not in seen_retype:
            seen_retype.add(key)
            retype_ops.append({
                'entity': op['old_entity'],
                'from': op['old_type'],
                'to': op['new_type'],
                'confidence': 'strong' if op.get('confidence', 0) >= 0.9 else 'interpretive'
            })
    elif op['action'] in ('flag_split', 'flag_attribute'):
        report['manual_review'].append({
            'entity': op['old_entity'],
            'action': op['action'],
            'reason': op.get('rationale', '')
        })

for op in retype_ops:
    entity_name = op['entity']
    new_type_name = op['to']
    confidence = op.get('confidence', 'strong')

    if confidence == 'interpretive':
        report['manual_review'].append({
            'entity': entity_name,
            'action': 'retype_interpretive',
            'from': op.get('from', '?'),
            'to': new_type_name,
            'reason': 'interpretive confidence, needs human review'
        })
        continue

    ent = find_entity(entity_name)
    if ent is None or ent['id'] in deleted_ids:
        report['retypes_failed'].append({'entity': entity_name, 'reason': 'entity not found or deleted'})
        continue

    new_type_id = get_or_create_type(new_type_name)

    old_type_names = [type_by_id.get(tid, tid) for tid in ent.get('types', [])]
    ent['types'] = [new_type_id]

    report['retypes_applied'].append({
        'entity': entity_name,
        'from': old_type_names,
        'to': new_type_name,
        'confidence': confidence
    })

print(f"  Retypes applied: {len(report['retypes_applied'])}, failed: {len(report['retypes_failed'])}")
print(f"  Manual review items: {len(report['manual_review'])}")

# ── phase 4 : canonize infrastructure domains ─────────────────────────────────

print("Phase 4: canonicalizing infrastructure domains...")

instantiated_rt_id = get_or_create_rt('instantiatedInProtocol')

for canon_op in seed.get('canonize_infrastructure_domains', []):
    canonical_name = canon_op['canonical']
    to_replace     = canon_op.get('replace', [])

    target = find_entity(canonical_name)
    if target is None:
        # canonical doesn't exist yet — find one of the replaced ones to rename
        for rn in to_replace:
            candidate = find_entity(rn)
            if candidate and candidate['id'] not in deleted_ids:
                candidate['name'] = canonical_name
                target = candidate
                entity_by_name[canonical_name] = target
                entity_by_norm[normalize(canonical_name)] = target
                break

    if target is None:
        report['domains_canonicalized'].append({'canonical': canonical_name, 'status': 'canonical not found'})
        continue

    tgt_id = target['id']

    for rn in to_replace:
        if rn == canonical_name:
            continue
        source = find_entity(rn)
        if source is None or source['id'] in deleted_ids or source['id'] == tgt_id:
            continue
        src_id = source['id']
        redirected = 0
        for rel in relations:
            if rel['from'] == src_id:
                rel['from'] = tgt_id
                redirected += 1
            if rel['to'] == src_id:
                rel['to'] = tgt_id
                redirected += 1
        deleted_ids.add(src_id)
        report['domains_canonicalized'].append({
            'canonical': canonical_name,
            'merged': rn,
            'relations_redirected': redirected
        })

print(f"  Domain canonicalization ops: {len(report['domains_canonicalized'])}")

# ── phase 5 : CrisisPhase DAO → Chap.III via appears_in_section ────────────

print("Phase 5: assigning DAO CrisisPhases to section III...")

# Find section node for chapter III — look for a ThesisSection with name containing 'III'
ts_type_id = type_by_name.get('ThesisSection')
appears_in_rt = rt_by_name.get('appears in section') or rt_by_name.get('appears_in_section')

# find chap III intro section
chap3_section = None
for e in entities:
    if ts_type_id and ts_type_id in e.get('types', []):
        if e['name'] in ('conclu_intro', 'III', 'Chap. III', 'chapitre_III') or e['name'].startswith('III.'):
            chap3_section = e
            break

dao_phases = ['DAO — Bifurcation / Stabilisation', 'DAO — Déclenchement',
              'DAO — Insémination / gestation', 'DAO — Remise en ordre']

if appears_in_rt and chap3_section:
    for phase_name in dao_phases:
        ent = find_entity(phase_name)
        if ent and ent['id'] not in deleted_ids:
            # check if already has a relation
            already = any(r['from'] == ent['id'] and r['type'] == appears_in_rt for r in relations)
            if not already:
                relations.append(make_relation(appears_in_rt, ent['id'], chap3_section['id']))
                report['new_relations_added'].append(f"CrisisPhase DAO → {chap3_section['name']}")
else:
    # just set type to Chap.III via chapter assignment (no section node found)
    report['manual_review'].append({
        'entity': 'DAO CrisisPhases',
        'action': 'assign_section',
        'reason': f'No Chap.III ThesisSection node found (appears_in_rt={appears_in_rt}, chap3={chap3_section})'
    })

# ── phase 6 : create new semantic relations ──────────────────────────────────

print("Phase 6: adding instanceOfCategory and monetization relations...")

# instanceOfCategory relation
inst_rt_id = get_or_create_rt('instanceOfCategory')
org_rt_id = get_or_create_rt('organizes')
rev_rt_id = get_or_create_rt('revealedBy')

instance_links = [
    ('Core Developers (Bitcoin)',   "Développeurs Core (mainteneurs avec accès commit)"),
    ('Core Developers (Ethereum)',  "Développeurs Core (mainteneurs avec accès commit)"),
    ('Mineurs Bitcoin',             "Mineurs et assimilés"),
    ('Pools de minage',             "Mineurs et assimilés"),
    ('Opérateurs de nœuds complets (full nodes)', "Nœuds complets (Full Nodes)"),
    ('Fournisseurs de portefeuilles (wallet providers)', "Fournisseurs de portefeuilles"),
]

for src_name, tgt_name in instance_links:
    src = find_entity(src_name)
    tgt = find_entity(tgt_name)
    if src and tgt and src['id'] not in deleted_ids and tgt['id'] not in deleted_ids:
        already = any(r['from'] == src['id'] and r['to'] == tgt['id'] and r['type'] == inst_rt_id
                      for r in relations)
        if not already:
            relations.append(make_relation(inst_rt_id, src['id'], tgt['id']))
            report['new_relations_added'].append(f"instanceOfCategory: {src_name} → {tgt_name}")

# organizes / revealedBy relations for Monétisation
monetisation = find_entity('Monnetisation') or find_entity('Monétisation') or find_entity('Monnetisation')
if monetisation:
    organizes_objects = ['UCN BTC', 'UCN ETH', 'Passerelle', 'Sphère d\'usage',
                         'Services de portefeuille et de paiement', 'Conformité réglementaire']
    for obj_name in organizes_objects:
        obj = find_entity(obj_name)
        if obj and obj['id'] not in deleted_ids:
            already = any(r['from'] == monetisation['id'] and r['to'] == obj['id'] and r['type'] == org_rt_id
                          for r in relations)
            if not already:
                relations.append(make_relation(org_rt_id, monetisation['id'], obj['id']))
                report['new_relations_added'].append(f"organizes: Monétisation → {obj_name}")

print(f"  New relations added: {len(report['new_relations_added'])}")

# ── phase 7 : create Monétisation des cryptomonnaies core concept ────────────

print("Phase 7: ensuring Monétisation des cryptomonnaies exists as CoreConcept...")

core_concept_type_id = get_or_create_type('CoreConcept')
monetisation_label = 'Monétisation des cryptomonnaies'
if find_entity(monetisation_label) is None:
    new_e = {
        "id": new_id(),
        "name": monetisation_label,
        "description": {"type": "TEXT",
                        "value": "Processus par lequel les UCN Bitcoin et Ethereum acquièrent le statut de monnaie à travers des usages, institutions, passerelles et crises.",
                        "options": {"language": "fr"}},
        "types": [core_concept_type_id],
        "attributes": {}
    }
    entities.append(new_e)
    entity_by_name[monetisation_label] = new_e
    entity_by_norm[normalize(monetisation_label)] = new_e
    report['new_relations_added'].append(f"Created entity: {monetisation_label} (CoreConcept)")
    print(f"  Created: {monetisation_label}")
else:
    print(f"  Already exists: {monetisation_label}")

# ── phase 8 : promote core concepts ─────────────────────────────────────────

print("Phase 8: promoting core/secondary/technical concepts...")

core_concepts = [
    ('Monnetisation', 'CoreConcept'), ('Infrastructure sociotechnique', 'CoreConcept'),
    ('Développement carnavalesque', 'CoreConcept'), ('Gouvernance polycentrique', 'CoreConcept'),
    ('Gouvernance duale', 'CoreConcept'), ('Mise en crise / Remise en ordre', 'CoreConcept'),
    ('Nominalisme monétaire non étatiste', 'CoreConcept'), ('Gouvernance discrète des cryptomonnaies', 'CoreConcept'),
    ('Logique de consensus distribué', 'SecondaryConcept'), ('Interopérabilité de Bitcoin (avec l\'infrastructure financière)', 'SecondaryConcept'),
    ('Nonce', 'TechnicalConcept'), ('Arbre de Merkle', 'TechnicalConcept'),
    ('OP_RETURN', 'TechnicalConcept'), ('Double dépense', 'TechnicalConcept'),
    ('"Not your keys, not your coins"', 'NativeFormula'), ('Code is Law', 'NativeFormula'),
]
for concept_name, target_type in core_concepts:
    ent = find_entity(concept_name)
    if ent and ent['id'] not in deleted_ids:
        tid = get_or_create_type(target_type)
        if tid not in ent.get('types', []):
            ent['types'] = [tid]
            report['retypes_applied'].append({
                'entity': concept_name, 'from': ['Concept'], 'to': target_type, 'confidence': 'strong'
            })

# ── phase 9 : reclassify section titles out of Concept ───────────────────────

print("Phase 9: reclassifying section titles and analytic claims...")

chapter_section_type_id = get_or_create_type('ChapterSection')
analytic_claim_type_id  = get_or_create_type('AnalyticClaim')

section_titles = [
    "II.3 Au\u2011delà de la revendication d'une absence de gouvernance !",
    "III.3 Une gouvernance publique d'exception : le hard fork d'Ethereum consécutif à l'attaque de \"The DAO\"",
    "II.3 Au-delà de la revendication d'une absence de gouvernance !",
]
for title in section_titles:
    ent = find_entity(title)
    if ent and ent['id'] not in deleted_ids:
        ent['types'] = [chapter_section_type_id]
        report['retypes_applied'].append({'entity': title, 'from': ['Concept'], 'to': 'ChapterSection', 'confidence': 'certain'})

analytic_claims = ["W.J. van der Laan — style de mainteneur"]
for claim in analytic_claims:
    ent = find_entity(claim)
    if ent and ent['id'] not in deleted_ids:
        ent['types'] = [analytic_claim_type_id]
        report['retypes_applied'].append({'entity': claim, 'from': ['Concept'], 'to': 'AnalyticClaim', 'confidence': 'strong'})

# ── phase 10 : remove deleted entities ───────────────────────────────────────

print("Phase 10: removing merged entities and cleaning relations...")

before_e = len(entities)
before_r = len(relations)

# Remove self-referential relations created by merge
relations[:] = [r for r in relations if r['from'] != r['to']]
# Remove deleted entities
entities[:] = [e for e in entities if e['id'] not in deleted_ids]
# Remove relations touching deleted entities (shouldn't be any after merge, but safety)
relations[:] = [r for r in relations if r['from'] not in deleted_ids and r['to'] not in deleted_ids]
# Remove duplicate relations (same type+from+to)
seen_rels = set()
unique_rels = []
for r in relations:
    key = (r['type'], r['from'], r['to'])
    if key not in seen_rels:
        seen_rels.add(key)
        unique_rels.append(r)
relations[:] = unique_rels

after_e = len(entities)
after_r = len(relations)

print(f"  Entities: {before_e} → {after_e} (-{before_e - after_e})")
print(f"  Relations: {before_r} → {after_r} (Δ{after_r - before_r:+d})")

# ── stats & save ─────────────────────────────────────────────────────────────

from collections import Counter
type_ids_used = []
for e in entities:
    type_ids_used.extend(e.get('types', []))
type_counts = Counter(type_by_id.get(tid, tid) for tid in type_ids_used)

report['stats'] = {
    'entities_before': before_e,
    'entities_after': after_e,
    'entities_removed': before_e - after_e,
    'relations_before': before_r,
    'relations_after': after_r,
    'relations_delta': after_r - before_r,
    'types_count': len(types),
    'new_types_created': len(report['created_types']),
    'merges_applied': len(report['merges_applied']),
    'retypes_applied': len(report['retypes_applied']),
    'manual_review_items': len(report['manual_review']),
    'entity_type_distribution': dict(type_counts.most_common(40))
}

graph['entities'] = entities
graph['relations'] = relations
graph['types']    = types
graph['relation_types'] = relation_types

output_path = 'grc20-these-mael-rolland-v91.json'
report_path = 'grc20_v91_migration_report.json'

print(f"\nSaving {output_path}...")
with open(output_path, 'w', encoding='utf-8') as f:
    json.dump(graph, f, ensure_ascii=False, separators=(',', ':'))

print(f"Saving {report_path}...")
with open(report_path, 'w', encoding='utf-8') as f:
    json.dump(report, f, ensure_ascii=False, indent=2)

print("\n── MIGRATION COMPLETE ──")
print(f"  Entities: {before_e} → {after_e}")
print(f"  Relations: {before_r} → {after_r}")
print(f"  New types: {len(report['created_types'])}")
print(f"  New relation types: {len(report['created_relation_types'])}")
print(f"  Merges applied: {len(report['merges_applied'])}")
print(f"  Retypes applied: {len(report['retypes_applied'])}")
print(f"  Manual review: {len(report['manual_review'])}")
print(f"\nType distribution (top 20):")
for tname, count in type_counts.most_common(20):
    print(f"  {tname}: {count}")
