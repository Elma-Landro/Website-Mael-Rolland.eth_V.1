#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Applique patch_12 a v98 et produit le graphe candidat v99.

Patch de relations uniquement : aucune entite creee, modifiee ou supprimee,
aucune relation existante retiree. Le script valide avant d'ecrire et echoue
bruyamment plutot que de produire un graphe douteux.

Usage:
    python3 scripts/make_v99_wire_maturation_phase.py
    python3 scripts/make_v99_wire_maturation_phase.py --dry-run
"""
import argparse, json, os, re, sys, collections

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

p = argparse.ArgumentParser(description="Construit v99 = v98 + patch_12 (cablage des phases).")
p.add_argument('--source', default=os.path.join(REPO, 'grc20-these-mael-rolland-v98.json'))
p.add_argument('--patch', default=os.path.join(REPO, 'patch_12_wire_maturation_phase.json'))
p.add_argument('--target', default=os.path.join(REPO, 'grc20-these-mael-rolland-v99.json'))
p.add_argument('--dry-run', action='store_true')
args = p.parse_args()

def echec(msg):
    print(f"ECHEC : {msg}", file=sys.stderr)
    sys.exit(1)

for chemin in (args.source, args.patch):
    if not os.path.exists(chemin):
        echec(f"fichier introuvable : {chemin}")

with open(args.source, encoding='utf-8') as f:
    g = json.load(f)
with open(args.patch, encoding='utf-8') as f:
    patch = json.load(f)

meta = patch.get('_meta', {})
nouvelles = patch.get('new_relations', [])

print(f"source  : {os.path.basename(args.source)} "
      f"({len(g['entities'])} entites, {len(g['relations'])} relations)")
print(f"patch   : {os.path.basename(args.patch)} ({len(nouvelles)} relations)")

if meta.get('source_graph') and meta['source_graph'] != os.path.basename(args.source):
    echec(f"le patch declare source_graph={meta['source_graph']}, "
          f"incompatible avec {os.path.basename(args.source)}")
if patch.get('new_entities'):
    echec("ce patch ne doit creer aucune entite")

# ---------- validations ----------

ids = {e['id'] for e in g['entities']}
types_rel = {r['id'] for r in g['relation_types']}
nom_type = {t['id']: t.get('name') for t in g['types']}
erreurs = []

# 1. Forme et unicite des identifiants de relation.
vus = collections.Counter(r.get('id') for r in nouvelles)
for rid, n in vus.items():
    if n > 1:
        erreurs.append(f"identifiant de relation repete dans le patch : {rid} ({n} fois)")
    if not re.fullmatch(r'[0-9a-f]{32}', rid or ''):
        erreurs.append(f"identifiant de relation hors convention : {rid!r}")
existants = {r['id'] for r in g['relations'] if r.get('id')}
for r in nouvelles:
    if r.get('id') in existants:
        erreurs.append(f"identifiant de relation deja present : {r['id']}")

# 2. Extremites resolues et type de relation connu.
for r in nouvelles:
    if r.get('type') not in types_rel:
        erreurs.append(f"relation_type inconnu : {r.get('type')}")
    for bout in ('from', 'to'):
        if r.get(bout) not in ids:
            erreurs.append(f"relation {r.get('id')} : extremite {bout} inexistante ({r.get(bout)})")

# 3. La relation ne doit pas deja exister entre ces deux entites.
paires = {(r.get('from'), r.get('type'), r.get('to')) for r in g['relations']}
for r in nouvelles:
    if (r.get('from'), r.get('type'), r.get('to')) in paires:
        erreurs.append(f"relation deja presente : {r.get('from')} -> {r.get('to')}")

# 4. La source doit etre un evenement, la cible la phase declaree.
cible = (meta.get('target_phase') or {}).get('id')
par_id = {e['id']: e for e in g['entities']}
for r in nouvelles:
    src = par_id.get(r.get('from'))
    if src is not None:
        ts = {nom_type.get(t, t) for t in (src.get('types') or [])}
        if not ({'InfrastructureEvent', 'CrisisEvent'} & ts):
            erreurs.append(f"la source n'est pas un evenement : {src.get('name')} ({ts})")
    if cible and r.get('to') != cible:
        erreurs.append(f"cible inattendue : {r.get('to')} (attendu {cible})")

if erreurs:
    for x in erreurs[:40]:
        print(f"  - {x}", file=sys.stderr)
    echec(f"{len(erreurs)} probleme(s) de validation — rien n'a ete ecrit")

print("validation : OK")

# ---------- mutation ----------

avant = len(g['relations'])
g['relations'].extend(nouvelles)

g['space']['version'] = 'v99'
g['space']['note'] = (
    f"V99 — {len(nouvelles)} relations « occurs in » rattachant les evenements de la "
    f"periode de maturation a la DevelopmentPhase homonyme. Aucune entite creee, "
    f"modifiee ou supprimee. " + g['space'].get('note', '')
)

if args.dry_run:
    print("dry-run : v99 non ecrit")
    sys.exit(0)

with open(args.target, 'w', encoding='utf-8') as f:
    json.dump(g, f, ensure_ascii=False, indent=2)

print(f"cible   : {os.path.basename(args.target)} "
      f"({len(g['entities'])} entites, {avant} -> {len(g['relations'])} relations)")

# ---------- effet sur l'equilibre des phases ----------

rt = {r['id']: r.get('name') for r in g['relation_types']}
PH = {'6414d87541f941a0b428c536ce72e032': 'Phase de preuve de concept',
      '019689c1ce06489a84768c51637eb9ed': 'Phase de peche',
      'eed0b89cd2e740718059c16591f9bfb7': 'Phase de maturation (DevelopmentPhase)',
      '645079ad66ee41b689112d383dd54798': 'Phase de maturation (Concept, doublon)'}
occ = collections.Counter()
for r in g['relations']:
    if r.get('to') in PH and rt.get(r.get('type')) == 'occurs in':
        occ[PH[r['to']]] += 1
print()
print("aretes « occurs in » vers les phases, apres cablage :")
for k in PH.values():
    print(f"  {k:42s} {occ[k]}")
