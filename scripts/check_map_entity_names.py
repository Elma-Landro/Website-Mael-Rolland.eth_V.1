#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Compare le nom DENORMALISE des cartes d'ancrage au nom canonique du graphe.

LECTURE SEULE, ET SANS CORRECTIF. Ce script ne repare rien et ne construit
aucun mecanisme de synchronisation : il RAPPORTE les divergences. C'est
delibere — le chantier qui decidera quoi faire de ce champ denormalise est
distinct (proprietaire de l'artefact, source de verite, faut-il seulement
persister ce nom, quel mecanisme, faut-il un `--check` en CI).

POURQUOI IL EXISTE. Les deux cartes portent le nom de l'entite A COTE de son
identifiant, et le test a blanc du 2026-08-11 a etabli qu'AUCUN script du
depot ne rafraichit ce champ : `build_anchor_weights.py --apply` n'ecrit que
`snippet_status` et `direct_anchor_count`, `fix_dead_ids_in_section_map.py` ne
touche le nom qu'en reparant un identifiant mort, et `entity_section_map.json`
n'a aucun script ecrivain. Ces cartes ne sont donc pas desynchronisees malgre
un pipeline de synchronisation : elles portent un champ denormalise SANS
mecanisme de synchronisation.

DEUX STRUCTURES, DEUX NOMS DE CHAMP — les confondre ferait rater la moitie du
releve :
    entity_section_map.json   {entity_id: {name, type, sections: [...]}}
    section_entities_map.json {section_key: {entities: [{entity_id,
                                                         entity_name, ...}]}}

Usage:
    python3 scripts/check_map_entity_names.py            # rapport
    python3 scripts/check_map_entity_names.py --json <f> # rapport machine
"""
import argparse
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from grc20_commun import REPO, graphe_le_plus_recent  # noqa: E402

CODE_DIVERGENCE, CODE_INVOCATION = 1, 2

CARTES = (
    ('entity_section_map.json', 'name'),
    ('section_entities_map.json', 'entity_name'),
)


def echec(msg, code=CODE_INVOCATION):
    print(f'ECHEC (invocation) : {msg}', file=sys.stderr)
    sys.exit(code)


def entrees_de(carte, chemin):
    """-> [(emplacement lisible, entity_id, nom denormalise)]."""
    with open(chemin, encoding='utf-8') as f:
        d = json.load(f)
    sorties = []
    if carte == 'entity_section_map.json':
        for eid, bloc in d.items():
            if isinstance(bloc, dict):
                sorties.append((eid[:8], eid, bloc.get('name')))
    else:
        for cle, bloc in d.items():
            for i, ent in enumerate((bloc or {}).get('entities', [])):
                sorties.append((f'{cle}[{i}]', ent.get('entity_id'),
                                ent.get('entity_name')))
    return sorties


def construire(courant):
    with open(courant, encoding='utf-8') as f:
        g = json.load(f)
    canonique = {e['id']: e.get('name') for e in g['entities']}

    rapport = {'graphe': os.path.basename(courant), 'cartes': {}}
    for carte, champ in CARTES:
        chemin = os.path.join(REPO, carte)
        if not os.path.exists(chemin):
            echec(f'carte introuvable : {chemin}')
        entrees = entrees_de(carte, chemin)
        divergences, non_resolus, sans_nom = [], [], 0
        for emplacement, eid, denormalise in entrees:
            if not eid:
                sans_nom += 1
                continue
            if eid not in canonique:
                # Un identifiant que le graphe ne connait pas ne PEUT PAS etre
                # compare : ce n'est pas une divergence de nom, c'est un id
                # mort. Les confondre gonflerait le releve d'un probleme qui
                # a deja son outil (`fix_dead_ids_in_section_map.py`).
                non_resolus.append((emplacement, eid))
                continue
            if denormalise != canonique[eid]:
                divergences.append({
                    'emplacement': emplacement, 'entity_id': eid,
                    'champ': champ,
                    'nom_denormalise': denormalise,
                    'nom_canonique': canonique[eid],
                })
        rapport['cartes'][carte] = {
            'champ': champ,
            'entrees': len(entrees),
            'resolues': len(entrees) - len(non_resolus) - sans_nom,
            'ids_non_resolus': len(non_resolus),
            'sans_entity_id': sans_nom,
            'divergences': sorted(
                divergences, key=lambda x: (x['entity_id'], x['emplacement'])),
        }
    return rapport


def main():
    ap = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--graph', default=None)
    ap.add_argument('--json', default=None, metavar='CHEMIN')
    args = ap.parse_args()

    courant = args.graph or graphe_le_plus_recent(REPO)
    if not courant:
        echec('aucun graphe numerote dans le depot')
    rapport = construire(courant)

    print(f'graphe canonique : {rapport["graphe"]}\n')
    total = 0
    for carte, bloc in rapport['cartes'].items():
        n = len(bloc['divergences'])
        total += n
        print(f'  {carte}  (champ `{bloc["champ"]}`)')
        print(f'    {bloc["entrees"]} entree(s), {bloc["resolues"]} '
              f'resolue(s) dans le graphe, '
              f'{bloc["ids_non_resolus"]} id(s) non resolu(s)')
        print(f'    DIVERGENCES : {n}')
        par_entite = {}
        for d in bloc['divergences']:
            par_entite.setdefault(d['entity_id'], []).append(d)
        for eid, ds in sorted(par_entite.items()):
            print(f'      {eid[:8]}  x{len(ds)}')
            print(f'         carte  : {ds[0]["nom_denormalise"]!r}')
            print(f'         graphe : {ds[0]["nom_canonique"]!r}')
        print()

    print(f'TOTAL : {total} divergence(s) sur '
          f'{sum(b["resolues"] for b in rapport["cartes"].values())} '
          'entree(s) resolue(s)')

    if args.json:
        with open(args.json, 'w', encoding='utf-8') as f:
            json.dump(rapport, f, ensure_ascii=False, indent=2, sort_keys=True)
            f.write('\n')
        print(f'rapport json : {args.json}')

    # Sortie 1 s'il reste une divergence : ce script CONSTATE, il ne juge pas
    # de ce qu'il faut en faire. Le code permet de le cabler plus tard si
    # l'auteur decide que la coherence doit etre un invariant.
    return CODE_DIVERGENCE if total else 0


if __name__ == '__main__':
    sys.exit(main())
