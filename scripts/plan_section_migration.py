#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Construit le plan de renumerotation des ThesisSection. N'ecrit aucun graphe.

Constat qui rend la migration faisable : les noeuds du graphe portent les BONS
libelles et les mauvaises cles. Le decalage vient de ce que des titres de
niveau 3 ont ete numerotes comme des sous-sections de niveau 2. On peut donc
retrouver la position reelle de chaque noeud en appariant son libelle a l'arbre
des titres du markdown, plutot qu'en se fiant a sa cle.

Chaque noeud recoit une decision :
    RENUMEROTER   son libelle correspond a un titre `##` -> nouvelle cle
    CONFORME      il porte deja la bonne cle
    RETROGRADER   son libelle correspond a un `###` -> sous le niveau canonique
    RETIRER       aucun contenu attache et aucun equivalent dans le texte
    ARBITRER      apparie mais ambigu, ou sans equivalent alors qu'il porte du contenu

Usage:
    python3 scripts/plan_section_migration.py
    python3 scripts/plan_section_migration.py --csv docs/audits/data/section-migration.csv
"""
import argparse
import collections
import csv
import glob
import json
import os
import re
import sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from derive_section_tree import (  # noqa: E402
    FICHIERS, MD, cles_equivalentes, normalise, numerote, titres,
)


def graphe_le_plus_recent():
    c = glob.glob(os.path.join(REPO, 'grc20-these-mael-rolland-v*.json'))
    return max(c, key=lambda f: int(re.search(r'-v(\d+)\.json$', f).group(1)))


def sans_numero(t):
    """« I.1.1 — Une monnaie frappee… » -> « une monnaie frappee… »"""
    t = re.sub(r'^\s*(?:[IVX]+\.[\d.]+|[A-E]\.[\d.]*|[A-E])\s*[—\-–.)]*\s*', '', t or '')
    return normalise(t)


def main(argv=None):
    p = argparse.ArgumentParser(description="Plan de renumerotation des sections.")
    p.add_argument('--graph', default=None)
    p.add_argument('--csv', default=None)
    args = p.parse_args(argv)

    chemin = args.graph or graphe_le_plus_recent()
    with open(chemin, encoding='utf-8') as f:
        g = json.load(f)

    nom_type = {t['id']: t.get('name') for t in g['types']}
    rt = {r['id']: r.get('name') for r in g['relation_types']}
    entrants = collections.Counter()
    for r in g['relations']:
        if rt.get(r.get('type')) == 'appears in section':
            entrants[r['to']] += 1

    noeuds = []
    for e in g['entities']:
        ts = [nom_type.get(t, t) for t in (e.get('types') or [])]
        if 'ThesisSection' not in ts and 'ChapterSection' not in ts:
            continue
        a = (e.get('attributes') or {}).get('section_key')
        noeuds.append({
            'id': e['id'], 'nom': e.get('name', ''),
            'cle_actuelle': (a.get('value') if a else '') or '',
            'types': '|'.join(ts), 'contenu': entrants[e['id']],
        })

    # arbre des titres du markdown
    titres_md = []
    for cle_ch, fichier in FICHIERS:
        chemin_md = os.path.join(MD, fichier)
        if not os.path.exists(chemin_md):
            continue
        for l in numerote(titres(chemin_md), cle_ch):
            l['norm'] = sans_numero(l['titre'])
            titres_md.append(l)

    par_norme = collections.defaultdict(list)
    for l in titres_md:
        if l['norm']:
            par_norme[l['norm']].append(l)

    def apparie(nom):
        n = sans_numero(nom)
        if not n:
            return []
        if n in par_norme:
            return par_norme[n]
        # repli : inclusion dans un sens ou dans l'autre, sur un prefixe long
        out = []
        for cle, lignes in par_norme.items():
            if len(n) >= 25 and (n[:45] in cle or cle[:45] in n):
                out += lignes
        return out

    plan = []
    for nd in noeuds:
        cands = apparie(nd['nom'])
        exacts = [c for c in cands if c['niveau'] in (1, 2)]
        profonds = [c for c in cands if c['niveau'] >= 3]

        if len(exacts) == 1:
            c = exacts[0]
            attendue = sorted(cles_equivalentes(c['cle'], c['chapitre']))
            if nd['cle_actuelle'] in attendue:
                decision, cible, motif = 'CONFORME', nd['cle_actuelle'], ''
            else:
                pref = [k for k in attendue if k != c['cle']] or attendue
                decision, cible = 'RENUMEROTER', pref[0]
                motif = f"libelle apparie au titre l.{c['ligne']} (niveau {c['niveau']})"
        elif len(exacts) > 1:
            decision, cible = 'ARBITRER', ''
            motif = ('libelle appariable a ' + str(len(exacts)) + ' titres : '
                     + ', '.join(f"l.{c['ligne']}" for c in exacts[:4]))
        elif profonds:
            c = profonds[0]
            decision, cible = 'RETROGRADER', ''
            motif = (f"libelle apparie a un titre de niveau {c['niveau']} "
                     f"(l.{c['ligne']}) — sous le niveau canonique")
        elif nd['contenu'] == 0:
            decision, cible, motif = 'RETIRER', '', 'aucun contenu attache, aucun titre correspondant'
        else:
            decision, cible = 'ARBITRER', ''
            motif = f"aucun titre correspondant, mais {nd['contenu']} entites attachees"

        plan.append({
            'id': nd['id'], 'cle_actuelle': nd['cle_actuelle'], 'cle_cible': cible,
            'decision': decision, 'contenu': nd['contenu'], 'types': nd['types'],
            'nom_graphe': nd['nom'], 'motif': motif,
        })

    plan.sort(key=lambda r: ({'RENUMEROTER': 0, 'ARBITRER': 1, 'RETROGRADER': 2,
                              'RETIRER': 3, 'CONFORME': 4}[r['decision']],
                             r['cle_actuelle']))

    c = collections.Counter(r['decision'] for r in plan)
    print(f"graphe : {os.path.basename(chemin)} — {len(plan)} sections examinees")
    print()
    for d in ('CONFORME', 'RENUMEROTER', 'RETROGRADER', 'RETIRER', 'ARBITRER'):
        print(f"  {c[d]:4d}  {d}")
    print()
    print('=== a renumeroter ===')
    for r in plan:
        if r['decision'] == 'RENUMEROTER':
            print(f"  {r['cle_actuelle']:12s} -> {r['cle_cible']:12s} "
                  f"[{r['contenu']:4d} ent.] {r['nom_graphe'][:52]}")
    print()
    print('=== a arbitrer ===')
    for r in plan:
        if r['decision'] == 'ARBITRER':
            print(f"  {r['cle_actuelle']:12s} [{r['contenu']:4d} ent.] "
                  f"{r['nom_graphe'][:46]}")
            print(f"                 {r['motif'][:88]}")

    # Deux collisions distinctes, et la seconde est celle qui compte : une cle
    # cible peut etre LIBRE entre les renumerotations et pourtant DEJA OCCUPEE
    # par un noeud existant. Ne verifier que la premiere donne une fausse
    # assurance — c'est l'erreur que ce controle repare.
    collisions = collections.Counter(r['cle_cible'] for r in plan
                                     if r['decision'] == 'RENUMEROTER' and r['cle_cible'])
    entre_cibles = {k: n for k, n in collisions.items() if n > 1}

    occupees = {r['cle_actuelle']: r for r in plan if r['cle_actuelle']}
    bloquees = []
    for r in plan:
        if r['decision'] != 'RENUMEROTER' or not r['cle_cible']:
            continue
        tenant = occupees.get(r['cle_cible'])
        if tenant and tenant['id'] != r['id']:
            bloquees.append((r, tenant))

    print()
    print(f"collisions entre cibles      : {entre_cibles or 'aucune'}")
    print(f"cibles deja occupees         : {len(bloquees)}")
    for r, tenant in bloquees:
        print(f"  {r['cle_actuelle']:9s} -> {r['cle_cible']:9s} tenue par "
              f"« {tenant['nom_graphe'][:44]} » [{tenant['decision']}]")
    if bloquees:
        print()
        print("  => la renumerotation n'est PAS applicable seule : chaque cle cible")
        print("     doit d'abord etre liberee par la decision de son tenant.")
        print("     La migration est atomique.")

    if args.csv:
        os.makedirs(os.path.dirname(args.csv), exist_ok=True)
        with open(args.csv, 'w', encoding='utf-8', newline='') as f:
            w = csv.DictWriter(f, delimiter=';', fieldnames=[
                'decision', 'cle_actuelle', 'cle_cible', 'contenu', 'types',
                'id', 'nom_graphe', 'motif'])
            w.writeheader()
            w.writerows(plan)
        print(f"plan ecrit : {os.path.relpath(args.csv, REPO)} ({len(plan)} lignes)")
    return 0


if __name__ == '__main__':
    sys.exit(main())
