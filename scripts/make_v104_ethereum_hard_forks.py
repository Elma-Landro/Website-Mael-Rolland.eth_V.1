#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Ajoute au graphe les hard forks d'Ethereum de la chronologie hors these.

Source : `docs/research/chronologies/Chronologie_des_HF_dEthereum_V1.bin` —
une frise constituee et **verifiee par Mael Rolland**, qui n'a pas ete
mobilisee dans la these.

**Ces evenements ne figurent PAS dans la chronologie n° 6 « carnavalesque »,
et c'est normal.** Celle-ci porte le developpement infrastructurel de
Bitcoin (chapitre I, section I.2), sur la periode 18/07/2008 → debut 2020,
avec le code couleur des 8 domaines. Les hard forks d'Ethereum relevent d'un
autre objet et, pour la moitie d'entre eux, d'une periode posterieure au
perimetre de la these (jusqu'a decembre 2021).

Leur absence de la frise carnavalesque n'est donc **ni un oubli, ni une
lacune du graphe** : c'est une difference de perimetre. Chaque entite creee
le porte explicitement, dans sa description et dans ses attributs de
provenance, pour qu'aucun audit ulterieur ne les signale comme anomalie.

Ce que le script NE fait pas :
  - aucune relation `appears in section` : ces evenements ne sont dans aucune
    section de la these, et leur en attribuer une serait une invention ;
  - aucun rattachement aux 8 domaines : ceux-ci decrivent le developpement
    infrastructurel de BITCOIN (ch. I l. 251), pas celui d'Ethereum ;
  - aucune creation pour les forks deja presents (Olympic, Frontier, DAO
    Fork), qui sont seulement chaines a leurs voisins.

Usage:
    python3 scripts/make_v104_ethereum_hard_forks.py --dry-run
    python3 scripts/make_v104_ethereum_hard_forks.py
"""
import argparse
import hashlib
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from grc20_commun import REPO  # noqa: E402

SEL = 'grc20-ethereum-hard-forks-v1'
ETHEREUM = '2956b3b87db1448f8a2ddde82d39e9c9'

PROVENANCE = ("Chronologie des HF d'Ethereum V1 (M. Rolland) — constituee et "
              "verifiee par l'auteur, non mobilisee dans la these")
HORS_FRISE = ("Cet evenement ne figure pas dans la chronologie n° 6 "
              "« carnavalesque » (ch. I, sect. I.2) : celle-ci couvre le "
              "developpement infrastructurel de Bitcoin jusqu'au debut 2020, "
              "un autre perimetre. Absence attendue, pas une lacune.")

# Coquilles de frappe de la frise, corrigees dans le NOM de l'entite. Le
# libelle source reste intact dans la description : on ne reecrit pas la
# source, on lui donne un nom d'entite juste.
COQUILLES = {'Frontier Thawind': 'Frontier Thawing'}

# Les forks deja presents dans le graphe, sous leur libelle existant.
DEJA = {
    '0': 'Testnet Olympic',
    '1': "Lancement d'Ethereum (Frontier",
    '4': 'Ethereum Hard Fork (juillet 2016)',
}

RGBA = r'\d{1,3},\d{1,3},\d{1,3},\d{1,3}'
MOTIF = re.compile(rf'^E3:(\d{{2}}/\d{{2}}/\d{{4}}):(.*?):(?:B|{RGBA}):({RGBA}):', re.S)


def identifiant(*parts):
    return hashlib.md5((SEL + '|' + '|'.join(parts)).encode('utf-8')).hexdigest()


def echec(msg, code=1):
    print(f"ECHEC : {msg}", file=sys.stderr)
    sys.exit(code)


def lire_frise(chemin):
    """-> [{num, date_iso, nom, detail}] tries par date."""
    with open(chemin, encoding='utf-8') as f:
        brut = f.read()
    out = []
    for enr in brut.split('|'):
        if not enr.startswith('E3:'):
            continue
        m = MOTIF.search(enr)
        if not m:
            continue
        j, mo, a = m.group(1).split('/')
        texte = ' '.join(m.group(2).replace('#deuxpoint#', ':').split())
        num = re.match(r'\[(\d+)\]', texte)
        texte = re.sub(r'^\[\d+\]\s*', '', texte)
        # Le nom du fork est en tete, entre guillemets ou jusqu'au premier
        # marqueur structurel (« Hard Fork », « Block », « (« ).
        nom = re.match(r'^"([^"]+)"', texte)
        if nom:
            nom = nom.group(1)
        else:
            nom = re.split(r'\s+(?:Hard Fork|Block|\(|:)', texte)[0][:60]
        out.append({'num': num.group(1) if num else '',
                    'date_iso': f'{a}-{mo}-{j}',
                    'nom': nom.strip(), 'detail': texte})
    return sorted(out, key=lambda x: x['date_iso'])


def main(argv=None):
    p = argparse.ArgumentParser(description="Ajoute les hard forks d'Ethereum.")
    p.add_argument('--source', default=os.path.join(REPO, 'grc20-these-mael-rolland-v103.json'))
    p.add_argument('--target', default=os.path.join(REPO, 'grc20-these-mael-rolland-v104.json'))
    p.add_argument('--frise', default=os.path.join(
        REPO, 'docs', 'research', 'chronologies',
        'Chronologie_des_HF_dEthereum_V1.bin'))
    p.add_argument('--dry-run', action='store_true')
    args = p.parse_args(argv)

    for chemin, quoi in ((args.source, 'graphe'), (args.frise, 'frise')):
        if not os.path.exists(chemin):
            echec(f"{quoi} introuvable : {chemin}", 2)

    with open(args.source, encoding='utf-8') as f:
        g = json.load(f)
    forks = lire_frise(args.frise)
    if not forks:
        echec("aucun evenement lu dans la frise")

    nom_type = {t['id']: t.get('name') for t in g['types']}
    type_pc = next((t['id'] for t in g['types'] if t.get('name') == 'ProtocolChange'), None)
    if not type_pc:
        echec("le type ProtocolChange est absent du graphe")
    rt = {r.get('name'): r['id'] for r in g['relation_types']}
    for n in ('part of', 'followed by'):
        if n not in rt:
            echec(f"le type de relation « {n} » est absent du graphe")

    E = {e['id']: e for e in g['entities']}
    if ETHEREUM not in E:
        echec(f"le noeud Ethereum est introuvable : {ETHEREUM}")

    # Resolution des forks deja presents, par fragment de libelle.
    def trouve(fragment):
        for e in g['entities']:
            if fragment.lower() in (e.get('name') or '').lower():
                return e['id']
        return None

    avant_e, avant_r = len(g['entities']), len(g['relations'])
    ids_par_num, nouvelles, ignores = {}, [], []

    for f in forks:
        frag = DEJA.get(f['num'])
        if frag:
            eid = trouve(frag)
            if not eid:
                echec(f"fork [{f['num']}] annonce present mais introuvable : {frag}")
            ids_par_num[f['num']] = eid
            ignores.append((f['num'], f['nom'], E[eid].get('name', '')))
            continue

        eid = identifiant('hf', f['num'], f['nom'])
        if eid in E:
            echec(f"identifiant deja present : {eid}")
        ids_par_num[f['num']] = eid
        nom_officiel = COQUILLES.get(f['nom'], f['nom'])
        nouvelles.append({
            'id': eid,
            'name': f"Ethereum Hard Fork — {nom_officiel}",
            'description': {
                'type': 'TEXT',
                'value': f"{f['detail']} — {HORS_FRISE}",
                'options': {'language': 'fr'},
            },
            'types': [type_pc],
            'attributes': {
                'date': {'type': 'TEXT', 'value': f['date_iso'],
                         'options': {'language': 'fr'}},
                'dateAuthority': {'type': 'TEXT', 'value': 'AUTHOR_VERIFIED',
                                  'options': {'language': 'en'}},
                'dateSource': {'type': 'TEXT', 'value': PROVENANCE,
                               'options': {'language': 'fr'}},
                'source': {'type': 'TEXT', 'value': PROVENANCE,
                           'options': {'language': 'fr'}},
                'evidenceStatus': {
                    'type': 'TEXT',
                    'value': 'author-verified — hors chronologie n° 6, hors perimetre de la these',
                    'options': {'language': 'fr'}},
                'protocol': {'type': 'TEXT', 'value': 'Ethereum',
                             'options': {'language': 'fr'}},
            },
        })

    g['entities'].extend(nouvelles)

    relations = []

    def rel(depuis, nom, vers):
        return {'id': identifiant('rel', depuis, nom, vers), 'type': rt[nom],
                'from': depuis, 'to': vers, 'attributes': []}

    # Chaque fork cree appartient au protocole Ethereum.
    for n in nouvelles:
        relations.append(rel(n['id'], 'part of', ETHEREUM))

    # Chainage chronologique de la frise entiere, y compris a travers les
    # forks deja presents : c'est ce qui en fait une chronologie et non une
    # liste. On ne recree pas un chainon deja pose.
    existants = {(r.get('from'), r.get('type'), r.get('to')) for r in g['relations']}
    for a, b in zip(forks, forks[1:]):
        ida, idb = ids_par_num[a['num']], ids_par_num[b['num']]
        if (ida, rt['followed by'], idb) in existants:
            continue
        relations.append(rel(ida, 'followed by', idb))

    ids_rel = {r.get('id') for r in g['relations'] if r.get('id')}
    doublons = [r['id'] for r in relations if r['id'] in ids_rel]
    if doublons:
        echec(f"identifiant(s) de relation deja present(s) : {doublons[:3]}")
    g['relations'].extend(relations)

    # ---------- verifications ----------
    ids = {e['id'] for e in g['entities']}
    casses = [r for r in g['relations']
              if r.get('from') not in ids or r.get('to') not in ids]
    if len(casses) > 1:
        echec(f"{len(casses)} relations a endpoint absent (attendu 1)")
    relies = set()
    for r in g['relations']:
        relies.add(r.get('from'))
        relies.add(r.get('to'))
    isoles = [n['id'] for n in nouvelles if n['id'] not in relies]
    if isoles:
        echec(f"{len(isoles)} entite(s) creee(s) sans relation")

    print(f"source : {os.path.basename(args.source)}")
    print(f"frise  : {os.path.basename(args.frise)} ({len(forks)} hard forks)")
    print()
    print(f"  deja presents, seulement chaines : {len(ignores)}")
    for num, nom, existant in ignores:
        print(f"    [{num:>2s}] {nom[:26]:26s} -> {existant[:44]}")
    print(f"  crees : {len(nouvelles)}")
    for n in nouvelles:
        d = n['attributes']['date']['value']
        print(f"    {d}  {n['name'][:58]}")
    print()
    print(f"  entites   : {avant_e} -> {len(g['entities'])}")
    print(f"  relations : {avant_r} -> {len(g['relations'])} "
          f"({len(nouvelles)} `part of`, "
          f"{len(relations) - len(nouvelles)} `followed by`)")

    if args.dry_run:
        print("\n--dry-run : rien ecrit.")
        return 0

    with open(args.target, 'w', encoding='utf-8') as f:
        json.dump(g, f, ensure_ascii=False, indent=2)
    print(f"\ngraphe ecrit : {os.path.relpath(args.target, REPO)}")
    return 0


if __name__ == '__main__':
    sys.exit(main())
