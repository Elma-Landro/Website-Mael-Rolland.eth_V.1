#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Retablit les 8 domaines de developpement de la these dans le graphe.

La these les enonce verbatim (chapitre I, l. 251) :

  (i)    sphere d'usage reelle et financiere        vert
  (ii)   traitement des transactions                jaune   <- segment « minage »
  (iii)  portefeuilles et paiements                 orange  <- « portefeuille » + « mixage »
  (iv)   information et connaissance                bleu fonce
  (v)    conformite aux reglementations nationales  bleu clair
  (vi)   protocole Bitcoin                          rouge
  (vii)  Altcoins                                   rose
  (viii) autres                                     violet

Le graphe en comptait bien huit, mais pas ceux-la.

**Le domaine (ii) n'avait pas disparu : il etait mal type.** Le noeud
« Traitement des transactions » porte le type `Concept` alors qu'il remplit
deja toutes les fonctions d'un domaine — il recoit 30 relations
`belongs to domain` (Mining pools, GHash.io, GPU mining emergence, ASIC
mining introduction...), il `contains segment` « Minage », et « Sphere
d'usage » lui adresse un `drives demand`. Lui ajouter le type
`InfrastructureDomain` le remet dans les huit **avec tous ses rattachements
existants**. En creer un nouveau aurait fabrique un doublon vide a cote d'un
noeud qui fait deja le travail.

Et un intrus occupait la huitieme place : « De la confidentialite et de
l'anonymisation », qui est le segment « mixage » du domaine (iii) et non un
domaine a part entiere. Il est fusionne dans (iii).

Le type `Concept` est CONSERVE : ce noeud est bien les deux a la fois, et le
retirer casserait toute vue qui filtre sur les concepts. Les sept autres
domaines ne portent que `InfrastructureDomain` — l'heterogeneite est
signalee, pas corrigee de force.

Aucun evenement n'est rattache ici : le cablage des evenements du catalogue
aux domaines demande un appariement verifiable, c'est un second temps.

Usage:
    python3 scripts/make_v102_restore_domain_ii.py --dry-run
    python3 scripts/make_v102_restore_domain_ii.py
"""
import argparse
import collections
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from grc20_commun import REPO  # noqa: E402

# Le noeud a retyper, et les deux noeuds de la fusion.
DOMAINE_II = '8fc8b0d7aa1a4510acea6831021bb4ac'      # Traitement des transactions
CONFIDENTIALITE = 'f81356a445e6433a9b5f69a85178bae7'  # absorbe
PORTEFEUILLES = '55b5215088664257819b56a918ec67fd'    # absorbeur, domaine (iii)


def echec(msg, code=1):
    print(f"ECHEC : {msg}", file=sys.stderr)
    sys.exit(code)


def main(argv=None):
    p = argparse.ArgumentParser(description="Retablit les 8 domaines de la these.")
    p.add_argument('--source', default=os.path.join(REPO, 'grc20-these-mael-rolland-v101.json'))
    p.add_argument('--target', default=os.path.join(REPO, 'grc20-these-mael-rolland-v102.json'))
    p.add_argument('--dry-run', action='store_true')
    args = p.parse_args(argv)

    if not os.path.exists(args.source):
        echec(f"graphe source introuvable : {args.source}", 2)
    with open(args.source, encoding='utf-8') as f:
        g = json.load(f)

    nom_type = {t['id']: t.get('name') for t in g['types']}
    type_domaine = next((t['id'] for t in g['types']
                         if t.get('name') == 'InfrastructureDomain'), None)
    if not type_domaine:
        echec("le type InfrastructureDomain est absent du graphe")

    E = {e['id']: e for e in g['entities']}
    for eid, quoi in ((DOMAINE_II, 'domaine (ii)'), (CONFIDENTIALITE, 'confidentialite'),
                      (PORTEFEUILLES, 'portefeuilles')):
        if eid not in E:
            echec(f"entite {quoi} introuvable : {eid}")

    rt = {r['id']: r.get('name') for r in g['relation_types']}
    entrantes_avant = sum(1 for r in g['relations']
                          if r.get('to') == DOMAINE_II
                          and rt.get(r['type']) == 'belongs to domain')
    if entrantes_avant == 0:
        echec(f"{DOMAINE_II} ne recoit aucun `belongs to domain` : "
              "ce n'est pas le domaine (ii) attendu")

    avant_e, avant_r = len(g['entities']), len(g['relations'])

    # ---------- 1. retypage du domaine (ii) ----------
    e = E[DOMAINE_II]
    if type_domaine in (e.get('types') or []):
        print("  note : le domaine (ii) porte deja le type InfrastructureDomain")
    else:
        e['types'] = list(e.get('types') or []) + [type_domaine]
    e.setdefault('attributes', {})
    e['attributes']['domain_index'] = {'type': 'TEXT', 'value': 'ii',
                                       'options': {'language': 'fr'}}
    e['attributes']['color'] = {'type': 'TEXT', 'value': 'jaune',
                                'options': {'language': 'fr'}}

    # ---------- 2. fusion confidentialite -> portefeuilles ----------
    # Les relations sont rebranchees avant la disparition du noeud. Celles
    # qui deviendraient reflexives, ou qui existent deja sur l'absorbeur,
    # sont retirees plutot que de creer une boucle ou un doublon.
    rebranchees = reflexives = doublons = 0
    relations, vues = [], set()
    for r in g['relations']:
        f_, t_ = r.get('from'), r.get('to')
        if f_ == CONFIDENTIALITE or t_ == CONFIDENTIALITE:
            r = dict(r)
            if f_ == CONFIDENTIALITE:
                r['from'] = PORTEFEUILLES
            if t_ == CONFIDENTIALITE:
                r['to'] = PORTEFEUILLES
            if r['from'] == r['to']:
                reflexives += 1
                continue
            rebranchees += 1
            cle = (r['from'], r.get('type'), r['to'])
            if cle in vues:
                doublons += 1
                continue
            vues.add(cle)
        else:
            vues.add((f_, r.get('type'), t_))
        relations.append(r)
    g['relations'] = relations
    g['entities'] = [x for x in g['entities'] if x['id'] != CONFIDENTIALITE]

    # ---------- verifications ----------
    ids = {x['id'] for x in g['entities']}
    casses = [r for r in g['relations']
              if r.get('from') not in ids or r.get('to') not in ids]
    if len(casses) > 1:   # l'orpheline Ostrom, portee exprès
        echec(f"{len(casses)} relations a endpoint absent (attendu 1)")
    if CONFIDENTIALITE in ids:
        echec("le noeud absorbe subsiste")

    domaines = [x for x in g['entities']
                if 'InfrastructureDomain' in [nom_type.get(t, t) for t in (x.get('types') or [])]]
    if len(domaines) != 8:
        echec(f"{len(domaines)} InfrastructureDomain apres operation, 8 attendus")

    entrantes = collections.Counter()
    for r in g['relations']:
        entrantes[r.get('to')] += 1
    isoles = [x['id'] for x in domaines if entrantes[x['id']] == 0
              and not any(r.get('from') == x['id'] for r in g['relations'])]
    if isoles:
        echec(f"domaine(s) sans aucune relation : {isoles}")

    print(f"source : {os.path.basename(args.source)}")
    print(f"  domaine (ii) retype : {DOMAINE_II} "
          f"({entrantes_avant} `belongs to domain` conserves)")
    print(f"  fusion confidentialite -> portefeuilles : {rebranchees} rebranchee(s), "
          f"{reflexives} reflexive(s), {doublons} doublon(s) retire(s)")
    print(f"  entites   : {avant_e} -> {len(g['entities'])}")
    print(f"  relations : {avant_r} -> {len(g['relations'])}")
    print()
    print("  les 8 domaines de la these :")
    for x in sorted(domaines, key=lambda y: -entrantes[y['id']]):
        print(f"    [{entrantes[x['id']]:4d} rel.]  {x.get('name', '')[:60]}")

    if args.dry_run:
        print("\n--dry-run : rien ecrit.")
        return 0

    with open(args.target, 'w', encoding='utf-8') as f:
        json.dump(g, f, ensure_ascii=False, indent=2)
    print(f"\ngraphe ecrit : {os.path.relpath(args.target, REPO)}")
    return 0


if __name__ == '__main__':
    sys.exit(main())
