#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Rattache les 4 sections du chapitre I restees hors de l'arborescence.

Trou trouve par une revue hostile le 03/08/2026, et anterieur a elle :
`I.2.2`, `I.3.1`, `I.3.2` et `I.3.3` ne portent **aucune** relation
`section of`. Ce sont les seules des 84 sections du graphe dans ce cas.

L'origine est datable : le cablage d'arborescence a ete introduit par
`make_section_creation_patch.py` pour les sections CREEES aux chapitres II et
III (v106). Il n'a jamais ete retro-applique au chapitre I, migre en v100
avant que le mecanisme n'existe. Et la garde de l'applicateur ne pouvait pas
le voir : elle refuse les entites TOTALEMENT isolees, or ces quatre-la portent
des centaines d'autres relations.

Rien ici n'est un arbitrage. Le motif est deja employe par les 80 autres
sections, a l'identique : chaque section pointe `section of` vers sa parente
ET vers son chapitre, chaque lien ayant sa reciproque `has section`. La place
de `I.3.2` sous `I.3` n'est pas une interpretation, c'est sa numerotation.

Cas particulier de `I.2.2` : elle porte deja `has section` vers son enfant
`I.2.2.b`, donc le lien descendant existe. Seul le lien montant manque.

Usage:
    python3 scripts/make_v107_wire_chapter_I_tree.py --dry-run
    python3 scripts/make_v107_wire_chapter_I_tree.py
"""
import argparse
import hashlib
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from grc20_commun import REPO, est_section  # noqa: E402

# Meme sel que `make_section_creation_patch.py` : rejouer la generation doit
# redonner les memes identifiants, et un lien deja cree ailleurs doit se
# reconnaitre plutot que se dedoubler.
SEL = 'grc20-section-migration-v1'

CODE_DONNEES, CODE_INVOCATION = 1, 2


def echec(msg, code=CODE_DONNEES):
    famille = 'invocation' if code == CODE_INVOCATION else 'donnees'
    print(f"ECHEC ({famille}) : {msg}", file=sys.stderr)
    sys.exit(code)


def identifiant(*parts):
    return hashlib.md5((SEL + '|' + '|'.join(parts)).encode('utf-8')).hexdigest()


def main(argv=None):
    p = argparse.ArgumentParser(description="Cable les 4 sections orphelines du chapitre I.")
    p.add_argument('--source', default=os.path.join(REPO, 'grc20-these-mael-rolland-v106.json'))
    p.add_argument('--patch', default=os.path.join(REPO, 'patch_17_wire_chapter_I_tree.json'))
    p.add_argument('--target', default=os.path.join(REPO, 'grc20-these-mael-rolland-v107.json'))
    p.add_argument('--dry-run', action='store_true')
    args = p.parse_args(argv)

    if not os.path.exists(args.source):
        echec(f"graphe source introuvable : {args.source}", CODE_INVOCATION)
    with open(args.source, encoding='utf-8') as f:
        g = json.load(f)

    nom_type = {t['id']: t.get('name') for t in g['types']}
    rt_id = {r.get('name'): r['id'] for r in g['relation_types']}
    for nom in ('section of', 'has section'):
        if nom not in rt_id:
            echec(f"type de relation « {nom} » absent du graphe")

    E = {e['id']: e for e in g['entities']}
    cle_de, id_de = {}, {}
    for e in g['entities']:
        if not est_section(e, nom_type):
            continue
        k = ((e.get('attributes') or {}).get('section_key') or {}).get('value')
        if k:
            cle_de[e['id']], id_de[k] = k, e['id']

    chapitre_de_section = {}
    for r in g['relations']:
        if r.get('type') != rt_id['section of']:
            continue
        cible = E.get(r.get('to'))
        if cible and 'Chapter' in [nom_type.get(t, t) for t in (cible.get('types') or [])]:
            k = cle_de.get(r.get('from'))
            if k:
                # « I.2.1 » -> « I. » : le chapitre se lit sur le prefixe
                chapitre_de_section.setdefault(k.split('.')[0], r['to'])

    # Les sections sans aucun `section of`. On ne vise pas une liste ecrite en
    # dur : on constate l'absence, pour que le script reste juste si le graphe
    # change.
    sortants = {r['from'] for r in g['relations'] if r.get('type') == rt_id['section of']}
    orphelines = sorted(k for k, i in id_de.items() if i not in sortants)
    if not orphelines:
        print("aucune section sans « section of » — rien a faire.")
        return 0

    existantes = {(r.get('type'), r.get('from'), r.get('to')) for r in g['relations']}
    nouvelles, ignorees, refus = [], [], []

    def lien(depuis, nom, vers):
        t = rt_id[nom]
        if (t, depuis, vers) in existantes:
            ignorees.append((cle_de.get(depuis, depuis), nom, cle_de.get(vers, vers)))
            return
        existantes.add((t, depuis, vers))
        nouvelles.append({'id': identifiant('rel', depuis, nom, vers),
                          'type': t, 'from': depuis, 'to': vers, 'attributes': []})

    for k in orphelines:
        i = id_de[k]
        parente = id_de.get(k.rsplit('.', 1)[0]) if '.' in k else None
        chapitre = chapitre_de_section.get(k.split('.')[0])
        if not parente and not chapitre:
            refus.append((k, 'ni parente ni chapitre identifiables'))
            continue
        for cible in (parente, chapitre):
            if not cible:
                refus.append((k, 'parente ou chapitre introuvable'))
                continue
            lien(i, 'section of', cible)
            lien(cible, 'has section', i)

    print(f"source : {os.path.basename(args.source)}")
    print(f"sections sans « section of » : {len(orphelines)} — {', '.join(orphelines)}")
    print(f"relations a creer  : {len(nouvelles)}")
    for r in nouvelles:
        f_, t_ = cle_de.get(r['from']) or E[r['from']]['name'][:34], \
                 cle_de.get(r['to']) or E[r['to']]['name'][:34]
        nom = 'section of' if r['type'] == rt_id['section of'] else 'has section'
        print(f"    {f_:12s} --{nom:12s}--> {t_}")
    if ignorees:
        print(f"deja presentes, non dupliquees : {len(ignorees)}")
        for a, n, b in ignorees:
            print(f"    {a:12s} --{n:12s}--> {b}")
    if refus:
        echec(f"{len(refus)} section(s) non cablables : {refus}")

    # --- verifications d'apres ---
    avant_e, avant_r = len(g['entities']), len(g['relations'])
    ids = set(E)
    for r in nouvelles:
        if r['from'] not in ids or r['to'] not in ids:
            echec(f"relation {r['id']} : endpoint absent")
    if len({r['id'] for r in nouvelles}) != len(nouvelles):
        echec("identifiants de relation en double dans le lot")

    patch = {
        '_meta': {
            'patch_id': '17',
            'description': "Cable les sections du chapitre I restees hors de "
                           "l'arborescence section of / has section.",
            'source_graph': os.path.basename(args.source),
            'policy': "Ne cree que des relations section of / has section, sur le "
                      "motif reciproque deja employe par les 80 autres sections. "
                      "Aucune entite creee, modifiee ou supprimee. Aucun attribut "
                      "touche. Aucune relation existante retiree.",
        },
        'new_relations': nouvelles,
    }
    if args.dry_run:
        print("\n--dry-run : ni patch ni graphe ecrits.")
        return 0

    with open(args.patch, 'w', encoding='utf-8') as f:
        json.dump(patch, f, ensure_ascii=False, indent=1)
    print(f"\npatch ecrit  : {os.path.relpath(args.patch, REPO)}")

    g['relations'].extend(nouvelles)
    if len(g['entities']) != avant_e:
        echec("aucune entite ne devait etre creee ou supprimee")
    if len(g['relations']) != avant_r + len(nouvelles):
        echec("compte de relations inattendu")
    espace = g.setdefault('space', {})
    espace['version'] = 'v107'
    espace['entity_count'] = len(g['entities'])
    espace['relation_count'] = len(g['relations'])
    espace['note'] = ("V107 — 4 sections du chapitre I (I.2.2, I.3.1, I.3.2, I.3.3) "
                      "rattachees a leur parente et a leur chapitre : elles etaient "
                      "les seules des 84 sans aucune relation « section of ». "
                      + espace.get('note', ''))
    with open(args.target, 'w', encoding='utf-8') as f:
        json.dump(g, f, ensure_ascii=False, indent=2)
    print(f"graphe ecrit : {os.path.relpath(args.target, REPO)}  "
          f"({avant_r} -> {len(g['relations'])} relations)")
    return 0


if __name__ == '__main__':
    sys.exit(main())
