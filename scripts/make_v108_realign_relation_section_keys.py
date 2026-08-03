#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Realigne le `section_key` porte par les relations sur leur cible reelle.

**Sequelle des migrations v100 et v106, et elle est de mon fait.**

Une cle de section vit a TROIS endroits dans ce depot :
  1. l'attribut `section_key` de l'entite section ;
  2. les cartes d'ancrage (`entity_section_map.json`, `section_entities_map.json`,
     `section_overrides.json`) ;
  3. **l'attribut `section_key` porte par chaque relation `appears in section`.**

Les migrations ont renumerote (1) et remappe (2). Personne n'a jamais touche (3),
et aucun controle ne la regarde : `check_graph_integrity.py` ne lit pas les
attributs de relation, `check_anchoring.py` ne lit que les cartes. Resultat :
3 970 relations declarent une cle qui ne nomme plus leur propre cible —
« II.2.3 » pour une relation qui pointe la section « II.2.2.c ».

Ce n'est pas un arbitrage. L'attribut est **denormalise** : il redit la cle de
la cible, laquelle est portee par la cible elle-meme. La verite est du cote de
la relation `to`, pas de l'attribut. On realigne l'attribut sur elle.

Le script ne touche a RIEN d'autre : ni `page_approx`, ni les relations dont la
cible n'est pas une section, ni celles qui n'ont pas d'attribut.

Usage:
    python3 scripts/make_v108_realign_relation_section_keys.py --dry-run
    python3 scripts/make_v108_realign_relation_section_keys.py
"""
import argparse
import collections
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from grc20_commun import REPO, est_section  # noqa: E402

CODE_DONNEES, CODE_INVOCATION = 1, 2


def echec(msg, code=CODE_DONNEES):
    famille = 'invocation' if code == CODE_INVOCATION else 'donnees'
    print(f"ECHEC ({famille}) : {msg}", file=sys.stderr)
    sys.exit(code)


def main(argv=None):
    p = argparse.ArgumentParser(
        description="Realigne section_key des relations sur leur cible.")
    p.add_argument('--source', default=os.path.join(REPO, 'grc20-these-mael-rolland-v107.json'))
    p.add_argument('--target', default=os.path.join(REPO, 'grc20-these-mael-rolland-v108.json'))
    p.add_argument('--dry-run', action='store_true')
    args = p.parse_args(argv)

    if not os.path.exists(args.source):
        echec(f"graphe source introuvable : {args.source}", CODE_INVOCATION)
    with open(args.source, encoding='utf-8') as f:
        g = json.load(f)

    nom_type = {t['id']: t.get('name') for t in g['types']}
    E = {e['id']: e for e in g['entities']}
    cle_de = {}
    for e in g['entities']:
        if est_section(e, nom_type):
            k = ((e.get('attributes') or {}).get('section_key') or {}).get('value')
            if k:
                cle_de[e['id']] = k

    avant_e, avant_r = len(g['entities']), len(g['relations'])
    corriges, deja, sans_cle, cible_non_section = 0, 0, 0, 0
    mouvements = collections.Counter()

    for r in g['relations']:
        attrs = r.get('attributes')
        if not isinstance(attrs, dict) or 'section_key' not in attrs:
            continue
        vraie = cle_de.get(r.get('to'))
        if not vraie:
            # La cible n'est pas une section : l'attribut ne peut pas etre
            # realigne, et decider quoi en faire est un arbitrage. On compte,
            # on ne touche pas.
            cible_non_section += 1
            continue
        val = attrs['section_key']
        actuelle = val.get('value') if isinstance(val, dict) else val
        if actuelle is None:
            sans_cle += 1
            continue
        if actuelle == vraie:
            deja += 1
            continue
        mouvements[(actuelle, vraie)] += 1
        if isinstance(val, dict):
            val['value'] = vraie
        else:
            attrs['section_key'] = {'type': 'TEXT', 'value': vraie,
                                    'options': {'language': 'fr'}}
        corriges += 1

    print(f"source : {os.path.basename(args.source)}")
    print(f"  relations portant un section_key      : {corriges + deja + cible_non_section + sans_cle}")
    print(f"  deja conformes                        : {deja}")
    print(f"  REALIGNEES sur leur cible             : {corriges}")
    print(f"  cible non-section, laissees en l'etat : {cible_non_section}")
    if sans_cle:
        print(f"  valeur absente, laissees en l'etat    : {sans_cle}")
    print()
    for (a, b), n in mouvements.most_common(20):
        print(f"    {n:5d}  « {a} » -> « {b} »")
    if len(mouvements) > 20:
        print(f"    … et {len(mouvements) - 20} autre(s) correspondance(s)")

    # --- verifications d'apres ---
    if len(g['entities']) != avant_e or len(g['relations']) != avant_r:
        echec("aucune entite ni relation ne devait etre creee ou supprimee")
    restants = 0
    for r in g['relations']:
        attrs = r.get('attributes')
        if not isinstance(attrs, dict) or 'section_key' not in attrs:
            continue
        vraie = cle_de.get(r.get('to'))
        val = attrs['section_key']
        actuelle = val.get('value') if isinstance(val, dict) else val
        if vraie and actuelle != vraie:
            restants += 1
    if restants:
        echec(f"{restants} relation(s) portent encore une cle perimee")
    print(f"\n  cles perimees restantes : 0")

    if args.dry_run:
        print("\n--dry-run : rien ecrit.")
        return 0

    espace = g.setdefault('space', {})
    m_v = re.search(r'-(v\d+)\.json$', os.path.basename(args.target))
    if not m_v:
        echec(f"nom de sortie sans numero de version : {os.path.basename(args.target)}",
              CODE_INVOCATION)
    espace['version'] = m_v.group(1)
    espace['entity_count'] = len(g['entities'])
    espace['relation_count'] = len(g['relations'])
    espace['note'] = (f"V108 — {corriges} relations « appears in section » portaient un "
                      f"attribut section_key perime, sequelle des migrations v100 et "
                      f"v106 : les cles avaient ete renumerotees sur les entites et "
                      f"remappees dans les cartes, jamais sur les relations. "
                      + espace.get('note', ''))
    with open(args.target, 'w', encoding='utf-8') as f:
        json.dump(g, f, ensure_ascii=False, indent=2)
    print(f"\ngraphe ecrit : {os.path.relpath(args.target, REPO)}")
    return 0


if __name__ == '__main__':
    sys.exit(main())
