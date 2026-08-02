#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Applique patch_11 a v97 et produit le graphe candidat v98.

Calque sur scripts/make_v97_remove_truncated_broken_relations.py : lit vN,
mute en memoire, ecrit vN+1, ne touche jamais au graphe source.

Le patch n'ajoute que des entites et des relations. Aucune entite existante
n'est modifiee, aucune n'est supprimee, aucune relation existante n'est
retiree. Le script echoue bruyamment plutot que d'ecrire un graphe douteux.

Usage:
    python3 scripts/make_v98_add_missing_chronology_events.py
    python3 scripts/make_v98_add_missing_chronology_events.py --dry-run

Codes de sortie :
    0 = v98 ecrit (ou dry-run concluant)
    1 = echec de validation, rien n'a ete ecrit
"""
import argparse, json, os, sys, collections

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

p = argparse.ArgumentParser(description="Construit v98 = v97 + patch_11.")
p.add_argument('--source', default=os.path.join(REPO, 'grc20-these-mael-rolland-v97.json'))
p.add_argument('--patch', default=os.path.join(REPO, 'patch_11_add_missing_chronology_events.json'))
p.add_argument('--target', default=os.path.join(REPO, 'grc20-these-mael-rolland-v98.json'))
p.add_argument('--dry-run', action='store_true',
               help="Valide tout mais n'ecrit pas le graphe candidat.")
args = p.parse_args()

def echec(msg):
    print(f"ECHEC : {msg}", file=sys.stderr)
    sys.exit(1)

# ---------- lecture ----------

for chemin in (args.source, args.patch):
    if not os.path.exists(chemin):
        echec(f"fichier introuvable : {chemin}")

with open(args.source, encoding='utf-8') as f:
    g = json.load(f)
with open(args.patch, encoding='utf-8') as f:
    patch = json.load(f)

nouvelles_entites = patch.get('new_entities', [])
nouvelles_relations = patch.get('new_relations', [])

print(f"source  : {os.path.basename(args.source)} "
      f"({len(g['entities'])} entites, {len(g['relations'])} relations)")
print(f"patch   : {os.path.basename(args.patch)} "
      f"({len(nouvelles_entites)} entites, {len(nouvelles_relations)} relations)")

if patch.get('source_graph') and patch['source_graph'] != os.path.basename(args.source):
    echec(f"le patch declare source_graph={patch['source_graph']}, "
          f"incompatible avec {os.path.basename(args.source)}")

# ---------- validations, avant toute mutation ----------

ids_existants = {e['id'] for e in g['entities']}
types_existants = {t['id'] for t in g['types']}
types_relation = {r['id'] for r in g['relation_types']}
erreurs = []

# 1. Aucun identifiant nouveau ne doit deja exister, ni se repeter.
vus = collections.Counter(e['id'] for e in nouvelles_entites)
for eid, n in vus.items():
    if n > 1:
        erreurs.append(f"identifiant repete dans le patch : {eid} ({n} fois)")
    if eid in ids_existants:
        erreurs.append(f"identifiant deja present dans v97 : {eid}")

# 2. Forme des identifiants : 32 caracteres hexadecimaux minuscules, sans exception
#    dans v97 (verifie sur les 2263 entites).
import re
for e in nouvelles_entites:
    if not re.fullmatch(r'[0-9a-f]{32}', e.get('id', '')):
        erreurs.append(f"identifiant hors convention (32 hex minuscules) : {e.get('id')!r}")

# 3. Les types references doivent exister.
for e in nouvelles_entites:
    if not e.get('types'):
        erreurs.append(f"entite sans type : {e.get('id')}")
    for t in e.get('types', []):
        if t not in types_existants:
            erreurs.append(f"type inconnu {t} sur l'entite {e.get('id')}")

# 4. Champs obligatoires, et forme des valeurs d'attribut.
for e in nouvelles_entites:
    if not e.get('name'):
        erreurs.append(f"entite sans nom : {e.get('id')}")
    for cle, val in (e.get('attributes') or {}).items():
        if not isinstance(val, dict) or 'type' not in val or 'value' not in val:
            erreurs.append(f"attribut malforme {cle} sur {e.get('id')}")
            continue
        # Convention v97 : TEXT porte toujours options.language ;
        # URL, NUMBER et TIME n'ont jamais d'options.
        if val['type'] == 'TEXT':
            lang = (val.get('options') or {}).get('language')
            if lang not in ('fr', 'en'):
                erreurs.append(f"TEXT sans options.language fr/en : {cle} sur {e.get('id')}")
        elif 'options' in val:
            erreurs.append(f"{val['type']} ne doit pas porter d'options : "
                           f"{cle} sur {e.get('id')}")

# 5. Les relations doivent pointer vers des entites qui existeront apres l'ajout.
ids_apres = ids_existants | {e['id'] for e in nouvelles_entites}
for r in nouvelles_relations:
    if r.get('type') not in types_relation:
        erreurs.append(f"relation_type inconnu : {r.get('type')}")
    for bout in ('from', 'to'):
        if r.get(bout) not in ids_apres:
            erreurs.append(f"relation {r.get('id')} : extremite {bout} "
                           f"inexistante ({r.get(bout)})")
    if r.get('id') and not re.fullmatch(r'[0-9a-f]{32}', r['id']):
        erreurs.append(f"identifiant de relation hors convention : {r['id']!r}")

ids_rel_existants = {r['id'] for r in g['relations'] if r.get('id')}
for r in nouvelles_relations:
    if r.get('id') and r['id'] in ids_rel_existants:
        erreurs.append(f"identifiant de relation deja present : {r['id']}")

# 6. Chaque nouvelle entite doit etre reliee : aucun evenement orphelin dans v97.
relies = {r['from'] for r in nouvelles_relations} | {r['to'] for r in nouvelles_relations}
for e in nouvelles_entites:
    if e['id'] not in relies:
        erreurs.append(f"entite orpheline (aucune relation) : {e.get('name')}")

if erreurs:
    for x in erreurs:
        print(f"  - {x}", file=sys.stderr)
    echec(f"{len(erreurs)} probleme(s) de validation — rien n'a ete ecrit")

print("validation : OK")

# ---------- mutation ----------

g['entities'].extend(nouvelles_entites)
g['relations'].extend(nouvelles_relations)

version_precedente = g['space'].get('version', 'v97')
g['space']['version'] = 'v98'
g['space']['note'] = (
    f"V98 — {len(nouvelles_entites)} evenements de la chronologie absents de v97, "
    f"ajoutes avec {len(nouvelles_relations)} relations. Aucune fusion, aucune "
    f"suppression, aucune entite existante modifiee. "
    + g['space'].get('note', '')
)

if args.dry_run:
    print("dry-run : v98 non ecrit")
    sys.exit(0)

with open(args.target, 'w', encoding='utf-8') as f:
    json.dump(g, f, ensure_ascii=False, indent=2)

print(f"cible   : {os.path.basename(args.target)} "
      f"({len(g['entities'])} entites, {len(g['relations'])} relations) "
      f"[{version_precedente} -> v98]")

# ---------- recapitulatif ----------

nom_type = {t['id']: t.get('name') for t in g['types']}
par_type = collections.Counter(
    nom_type.get(t, t) for e in nouvelles_entites for t in e.get('types', []))
print()
print("entites ajoutees par type :")
for k, v in par_type.most_common():
    print(f"  {k:24s} {v}")
nom_rel = {r['id']: r.get('name') for r in g['relation_types']}
par_rel = collections.Counter(nom_rel.get(r['type'], r['type']) for r in nouvelles_relations)
print("relations ajoutees par type :")
for k, v in par_rel.most_common():
    print(f"  {k:24s} {v}")
