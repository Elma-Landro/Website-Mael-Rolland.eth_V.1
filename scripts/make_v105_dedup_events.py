#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Applique `patch_10_dedup_events.json` et produit v105.

**Ce patch attendait son applicateur depuis le 02/08.** Le depot n'en avait
aucun : `apply_v91_migration.py` est un script v90->v91 dont les entrees ont
disparu de l'arbre, et il ne connait pas `SET_ATTRIBUTE`. C'etait le seul
obstacle technique au chantier de dedoublonnage.

Ce que le patch fait, et surtout ce qu'il ne fait pas : il **marque**
(`duplicateOf` + `reviewStatus = duplicate-pending-merge`) et ne fusionne
rien. Les deux entites d'une paire restent presentes et interrogeables. La
fusion effective est une decision humaine posterieure — c'est ecrit dans sa
`policy`, et c'est ce qui rend son application sure avant tout arbitrage.

Il corrige au passage la date de Litecoin (2011-11-19 -> 2011-10-07), qui
est la contradiction interne la mieux etayee du graphe : la description de
l'entite dit elle-meme « le 7 octobre 2011 ».

**Reserve a porter a l'arbitrage, non tranchee ici** : sur la grappe
« Mining pools », le mecanisme a designe comme canonique l'entite la MOINS
reliee — `Mining pools` (degre 7) est marquee doublon de
`InfrastructureEvent — Mining pools` (degre 4). Le marquage n'est pas
destructif et `reviewStatus` dit precisement « en attente », mais le sens de
cette paire devra etre confirme avant toute fusion.

Le patch declare `source_graph: v97` ; il est applique a v104. Le script
verifie donc que chaque entite visee existe toujours, plutot que de refuser
sur le seul numero de version.

Usage:
    python3 scripts/make_v105_dedup_events.py --dry-run
    python3 scripts/make_v105_dedup_events.py
"""
import argparse
import collections
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from grc20_commun import REPO  # noqa: E402


def echec(msg, code=1):
    print(f"ECHEC : {msg}", file=sys.stderr)
    sys.exit(code)


def main(argv=None):
    p = argparse.ArgumentParser(description="Applique patch_10 et produit v105.")
    p.add_argument('--source', default=os.path.join(REPO, 'grc20-these-mael-rolland-v104.json'))
    p.add_argument('--patch', default=os.path.join(REPO, 'patch_10_dedup_events.json'))
    p.add_argument('--target', default=os.path.join(REPO, 'grc20-these-mael-rolland-v105.json'))
    p.add_argument('--dry-run', action='store_true')
    args = p.parse_args(argv)

    for chemin, quoi in ((args.source, 'graphe source'), (args.patch, 'patch')):
        if not os.path.exists(chemin):
            echec(f"{quoi} introuvable : {chemin}", 2)
    with open(args.source, encoding='utf-8') as f:
        g = json.load(f)
    with open(args.patch, encoding='utf-8') as f:
        patch = json.load(f)

    ops = patch.get('ops') or []
    if not ops:
        echec("le patch ne porte aucune operation")
    E = {e['id']: e for e in g['entities']}

    # --- validations ---
    erreurs = []
    for o in ops:
        if o.get('type') != 'SET_ATTRIBUTE':
            erreurs.append(f"operation non supportee : {o.get('type')}")
            continue
        if o['entityId'] not in E:
            erreurs.append(f"entite absente du graphe : {o['entityId']}")
        v = o.get('value')
        if not isinstance(v, dict) or 'value' not in v:
            erreurs.append(f"valeur mal formee pour {o.get('attributeId')}")
    # Une cible de `duplicateOf` doit exister : pointer un id mort serait pire
    # que de ne rien marquer.
    for o in ops:
        if o.get('attributeId') == 'duplicateOf':
            cible = (o.get('value') or {}).get('value')
            if cible not in E:
                erreurs.append(f"duplicateOf pointe une entite absente : {cible}")
    if erreurs:
        for x in erreurs[:10]:
            print(f"  - {x}")
        echec(f"{len(erreurs)} erreur(s) de validation")

    avant_e, avant_r = len(g['entities']), len(g['relations'])
    deg = collections.Counter()
    for r in g['relations']:
        deg[r.get('from')] += 1
        deg[r.get('to')] += 1

    print(f"source : {os.path.basename(args.source)}")
    print(f"patch  : {os.path.basename(args.patch)} "
          f"(declare source_graph={patch.get('source_graph')})")
    print()

    ecrases = []
    for o in ops:
        e = E[o['entityId']]
        attrs = e.setdefault('attributes', {})
        cle = o['attributeId']
        ancien = attrs.get(cle)
        if ancien is not None:
            ancienne_valeur = ancien.get('value') if isinstance(ancien, dict) else ancien
            ecrases.append((e.get('name', '')[:40], cle, str(ancienne_valeur)[:24]))
        attrs[cle] = {k: v for k, v in o['value'].items()}
        cible = (o['value'] or {}).get('value')
        suffixe = ''
        if cle == 'duplicateOf' and cible in E and deg[o['entityId']] > deg[cible]:
            suffixe = '   <-- canonique MOINS relie, a confirmer'
        print(f"  {cle:14s} {e.get('name', '')[:34]:34s} = "
              f"{E[cible].get('name', '')[:30] if cle == 'duplicateOf' and cible in E else str(cible)[:30]}"
              f"{suffixe}")

    if ecrases:
        print()
        print("  valeurs remplacees :")
        for nom, cle, val in ecrases:
            print(f"    {nom:40s} {cle} : « {val} » -> nouvelle valeur")

    # --- verifications d'apres ---
    if len(g['entities']) != avant_e or len(g['relations']) != avant_r:
        echec("le patch ne doit ni creer ni supprimer d'entite ou de relation")
    marques = [e for e in g['entities'] if (e.get('attributes') or {}).get('duplicateOf')]
    for e in marques:
        if not (e.get('attributes') or {}).get('reviewStatus'):
            echec(f"{e['id']} porte duplicateOf sans reviewStatus")
    # Pas de chaine : une entite canonique ne doit pas etre elle-meme marquee.
    chaines = [e.get('name') for e in marques
               if E.get(e['attributes']['duplicateOf']['value'], {})
               .get('attributes', {}).get('duplicateOf')]
    if chaines:
        print()
        print(f"  ATTENTION : {len(chaines)} marquage(s) en chaine — "
              f"un canonique est lui-meme marque doublon : {chaines}")

    print()
    print(f"  entites   : {avant_e} (inchange)")
    print(f"  relations : {avant_r} (inchange)")
    print(f"  entites marquees duplicateOf : {len(marques)}")

    if args.dry_run:
        print("\n--dry-run : rien ecrit.")
        return 0

    g.setdefault('space', {})['version'] = 'v105'
    g['space']['entity_count'] = len(g['entities'])
    g['space']['relation_count'] = len(g['relations'])
    with open(args.target, 'w', encoding='utf-8') as f:
        json.dump(g, f, ensure_ascii=False, indent=2)
    print(f"\ngraphe ecrit : {os.path.relpath(args.target, REPO)}")
    return 0


if __name__ == '__main__':
    sys.exit(main())
