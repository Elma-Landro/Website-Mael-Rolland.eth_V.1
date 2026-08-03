#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Produit v101 = v100 sans les operations orphelines du bloc `ops`.

Le bloc `ops` d'un instantane transporte des operations heritees des patchs
successifs. Dix-neuf d'entre elles posent un attribut `definition` sur des
entites qui n'existent plus — venues de `patch_2c_definitions.json` et
recopiees de v96 jusqu'a v100 sans que rien ne les remarque.

Elles sont inertes : ni le site (`graphe.html`, `lecteur.html`,
`graph-worker.mjs`) ni le pipeline de publication ne lisent ce bloc —
`grc20-publish.mjs` reconstruit ses propres ops depuis `entities` et
`relations`. Les retirer ne change donc aucun comportement ; cela evite
qu'un futur consommateur du bloc herite d'operations invalides.

Le script ne touche a rien d'autre : ni entite, ni relation, ni type.

Usage:
    python3 scripts/make_v101_drop_orphan_ops.py --dry-run
    python3 scripts/make_v101_drop_orphan_ops.py
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


def orphelines(graphe):
    """-> les ops visant une entite absente du graphe."""
    ids = {e['id'] for e in graphe['entities']}
    return [o for o in graphe.get('ops', [])
            if o.get('entityId') and o['entityId'] not in ids]


def main(argv=None):
    p = argparse.ArgumentParser(description="v101 = v100 sans ops orphelines.")
    p.add_argument('--source', default=os.path.join(REPO, 'grc20-these-mael-rolland-v100.json'))
    p.add_argument('--target', default=os.path.join(REPO, 'grc20-these-mael-rolland-v101.json'))
    p.add_argument('--dry-run', action='store_true')
    args = p.parse_args(argv)

    if not os.path.exists(args.source):
        echec(f"graphe source introuvable : {args.source}", 2)
    with open(args.source, encoding='utf-8') as f:
        g = json.load(f)

    mortes = orphelines(g)
    avant = {k: len(v) for k, v in g.items() if isinstance(v, list)}

    print(f"source : {os.path.basename(args.source)}")
    print(f"  ops : {len(g.get('ops', []))} dont {len(mortes)} orpheline(s)")
    par_attr = collections.Counter(o.get('attributeId') for o in mortes)
    for a, n in par_attr.most_common():
        print(f"    {n:3d}  attributeId={a}")

    if not mortes:
        print("  rien a retirer.")
        return 0

    a_retirer = {id(o) for o in mortes}
    g['ops'] = [o for o in g['ops'] if id(o) not in a_retirer]

    # Tout le reste doit etre strictement intact.
    apres = {k: len(v) for k, v in g.items() if isinstance(v, list)}
    for cle in avant:
        attendu = avant[cle] - (len(mortes) if cle == 'ops' else 0)
        if apres[cle] != attendu:
            echec(f"{cle} : {apres[cle]} elements, {attendu} attendus")
    if orphelines(g):
        echec("des ops orphelines subsistent apres filtrage")

    print(f"  ops : {avant['ops']} -> {apres['ops']}")
    print(f"  entites et relations inchangees "
          f"({apres['entities']} / {apres['relations']})")

    if args.dry_run:
        print("--dry-run : rien ecrit.")
        return 0

    with open(args.target, 'w', encoding='utf-8') as f:
        json.dump(g, f, ensure_ascii=False, indent=2)
    print(f"graphe ecrit : {os.path.relpath(args.target, REPO)}")
    return 0


if __name__ == '__main__':
    sys.exit(main())
