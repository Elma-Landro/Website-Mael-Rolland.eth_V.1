#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Corrections editoriales sans arbitrage, appliquees a v105 en place.

Regroupees dans le meme instantane que le dedoublonnage plutot que dans un
v106 : le depot porte deja neuf graphes d'environ 10 Mo, et aucune de ces
corrections ne merite sa propre version.

Trois corrections, aucune ne demande de decision :

1. **Prefixe des SourceQuote.** Les 245 citations portent DEUX prefixes a
   parts quasi egales — 132 en « Quote — », 113 en « SourceQuote — ». Un
   lecteur voit les deux cote a cote. On retient « Quote — », majoritaire et
   plus court ; aucun sens n'est perdu, le type porte deja l'information.

2. **Accents.** Le titre de la these s'affiche « Au-dela des codes », et
   `space.description` annonce « issu de la these de doctorat soutenue a
   l'EHESS le 13 decembre 2024 ». Seuls les cas ou la forme accentuee est
   ATTESTEE AILLEURS dans le graphe, ou dans le texte de la these, sont
   corriges — on ne devine aucun accent.

3. **Trois entites sans type.** `Monnaie`, `Monnaie marchandise`,
   `Monnaie dette / Monnaie credit` n'ont aucun type. Ce n'est pas une
   invention a faire mais une perte a reparer : `space.note` documente
   « V90 — 3 new entities: Monnaie (Concept), Monnaie marchandise (TF),
   Monnaie dette/credit (TF) ». TF = TheoreticFramework.

Usage:
    python3 scripts/polish_v105_editorial.py --dry-run
    python3 scripts/polish_v105_editorial.py
"""
import argparse
import collections
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from grc20_commun import REPO  # noqa: E402

# Types perdus, tels que `space.note` les documente.
TYPES_PERDUS = {
    'Monnaie': 'Concept',
    'Monnaie marchandise': 'TheoreticFramework',
    'Monnaie dette / Monnaie crédit': 'TheoreticFramework',
}

# Textes d'en-tete a re-accentuer. Ecrits ici parce qu'aucune regle ne
# devine ou placer un accent — ce sont des corrections nommees, pas une
# transformation automatique.
ENTETE = {
    "Knowledge graph issu de la these de doctorat soutenue a l'EHESS le 13 decembre 2024. "
    "Gouvernance des cryptomonnaies, institutionnalisme monetaire, STS.":
    "Knowledge graph issu de la thèse de doctorat soutenue à l'EHESS le 13 décembre 2024. "
    "Gouvernance des cryptomonnaies, institutionnalisme monétaire, STS.",
}

NOMS = {'Au-dela des codes': 'Au-delà des codes'}


def echec(msg, code=1):
    print(f"ECHEC : {msg}", file=sys.stderr)
    sys.exit(code)


def main(argv=None):
    p = argparse.ArgumentParser(description="Corrections editoriales sur v105.")
    p.add_argument('--graph', default=os.path.join(REPO, 'grc20-these-mael-rolland-v105.json'))
    p.add_argument('--dry-run', action='store_true')
    args = p.parse_args(argv)

    if not os.path.exists(args.graph):
        echec(f"graphe introuvable : {args.graph}", 2)
    with open(args.graph, encoding='utf-8') as f:
        g = json.load(f)

    nom_type = {t['id']: t.get('name') for t in g['types']}
    type_par_nom = {t.get('name'): t['id'] for t in g['types']}
    avant_e, avant_r = len(g['entities']), len(g['relations'])

    # ---------- 1. prefixe des SourceQuote ----------
    prefixes = collections.Counter()
    for e in g['entities']:
        n = e.get('name', '')
        if n.startswith('SourceQuote — '):
            prefixes['SourceQuote — '] += 1
        elif n.startswith('Quote — '):
            prefixes['Quote — '] += 1
    renommes = 0
    for e in g['entities']:
        if e.get('name', '').startswith('SourceQuote — '):
            e['name'] = 'Quote — ' + e['name'][len('SourceQuote — '):]
            renommes += 1

    # ---------- 2. accents ----------
    accentues = 0
    for e in g['entities']:
        if e.get('name') in NOMS:
            e['name'] = NOMS[e['name']]
            accentues += 1
    entete = 0
    space = g.setdefault('space', {})
    if space.get('description') in ENTETE:
        space['description'] = ENTETE[space['description']]
        entete += 1

    # ---------- 3. types perdus ----------
    types_rendus = []
    for e in g['entities']:
        cible = TYPES_PERDUS.get(e.get('name'))
        if not cible or e.get('types'):
            continue
        tid = type_par_nom.get(cible)
        if not tid:
            echec(f"le type « {cible} » n'existe pas dans le graphe")
        e['types'] = [tid]
        types_rendus.append((e.get('name'), cible))

    # ---------- verifications ----------
    if len(g['entities']) != avant_e or len(g['relations']) != avant_r:
        echec("aucune entite ni relation ne devait etre creee ou supprimee")
    sans_type = [e.get('name') for e in g['entities'] if not e.get('types')]
    doublons = [n for n, c in collections.Counter(
        e.get('name') for e in g['entities']).items() if c > 1 and n]

    print(f"graphe : {os.path.basename(args.graph)}")
    print(f"  prefixes SourceQuote avant : {dict(prefixes)}")
    print(f"  renommes en « Quote — »    : {renommes}")
    print(f"  noms re-accentues          : {accentues}")
    print(f"  en-tete re-accentue        : {entete}")
    print(f"  types rendus               : {len(types_rendus)}")
    for n, c in types_rendus:
        print(f"      « {n} » -> {c}")
    print(f"  entites encore sans type   : {len(sans_type)} {sans_type[:3]}")
    if doublons:
        print(f"  ATTENTION : {len(doublons)} nom(s) desormais en double : {doublons[:5]}")

    if args.dry_run:
        print("\n--dry-run : rien ecrit.")
        return 0

    with open(args.graph, 'w', encoding='utf-8') as f:
        json.dump(g, f, ensure_ascii=False, indent=2)
    print(f"\ngraphe reecrit : {os.path.relpath(args.graph, REPO)}")
    return 0


if __name__ == '__main__':
    sys.exit(main())
