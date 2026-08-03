#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Rattache aux 8 domaines les evenements que le catalogue v2 code, et qu'eux seuls codent.

Le catalogue `docs/audits/data/catalogue-evenements-v2-fusion.csv` porte une
colonne `gid` : la jointure vers le graphe est donc EXPLICITE. On ne recourt a
aucun appariement par similarite de libelle — celui du depot produit des faux
positifs visibles (« Premier achat de 2 pizzas » apparie a « Bitcoin Faucet »),
et un rattachement au mauvais domaine serait pire que pas de rattachement.

Sur les 113 lignes joignables (gid + domaine_8), le script ne retient QUE
celles qui apportent une information que le graphe n'a pas :

  ecarte  origine=graphe .......... le domaine vient du mapping GRC-20 : le
                                    reecrire dans le graphe serait circulaire
  ecarte  l'entite a deja un domaine dans le graphe et le CSV le CONFIRME
  ecarte  l'entite a deja un domaine et le CSV le CONTREDIT — divergence
          signalee, jamais tranchee (charte : l'arbitrage revient a Mael)
  retient l'entite n'a AUCUN domaine et le CSV en code un

Le suffixe `*` de `domaine_8` marque une attribution par definition, sans
verification du code couleur de la figure : il est conserve dans le motif de
chaque relation pour que la provenance reste lisible.

Usage:
    python3 scripts/make_v103_wire_events_to_domains.py --dry-run
    python3 scripts/make_v103_wire_events_to_domains.py
"""
import argparse
import collections
import csv
import hashlib
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from grc20_commun import REPO  # noqa: E402

SEL = 'grc20-domaines-evenements-v1'

# Les 8 domaines de la these (chapitre I, l. 251), par leur libelle dans le graphe.
DOMAINES = {
    'i': 'Sphère d’usage',
    'ii': 'Traitement des transactions',
    'iii': 'Services de portefeuille et de paiement',
    'iv': 'Information et connaissance',
    'v': 'Conformité réglementaire',
    'vi': 'Protocole et couche de base',
    'vii': 'Altcoins, tokens et surcouches',
    'viii': '[Résiduel — à reclasser]',
}


def identifiant(*parts):
    return hashlib.md5((SEL + '|' + '|'.join(parts)).encode('utf-8')).hexdigest()


def echec(msg, code=1):
    print(f"ECHEC : {msg}", file=sys.stderr)
    sys.exit(code)


def main(argv=None):
    p = argparse.ArgumentParser(description="Rattache les evenements aux 8 domaines.")
    p.add_argument('--source', default=os.path.join(REPO, 'grc20-these-mael-rolland-v102.json'))
    p.add_argument('--target', default=os.path.join(REPO, 'grc20-these-mael-rolland-v103.json'))
    p.add_argument('--catalogue', default=os.path.join(
        REPO, 'docs', 'audits', 'data', 'catalogue-evenements-v2-fusion.csv'))
    p.add_argument('--divergences', default=os.path.join(
        REPO, 'docs', 'audits', 'data', 'domaines-divergences.csv'))
    p.add_argument('--dry-run', action='store_true')
    args = p.parse_args(argv)

    for chemin, quoi in ((args.source, 'graphe source'), (args.catalogue, 'catalogue')):
        if not os.path.exists(chemin):
            echec(f"{quoi} introuvable : {chemin}", 2)

    with open(args.source, encoding='utf-8') as f:
        g = json.load(f)
    with open(args.catalogue, encoding='utf-8') as f:
        lignes = list(csv.DictReader(f, delimiter=';'))

    E = {e['id']: e for e in g['entities']}
    nom_type = {t['id']: t.get('name') for t in g['types']}
    rt_nom = {r['id']: r.get('name') for r in g['relation_types']}
    type_rel = next((r['id'] for r in g['relation_types']
                     if r.get('name') == 'belongs to domain'), None)
    if not type_rel:
        echec("le type de relation « belongs to domain » est absent du graphe")

    par_nom = {e.get('name'): e['id'] for e in g['entities']
               if 'InfrastructureDomain' in [nom_type.get(t, t) for t in (e.get('types') or [])]}
    manquants = [n for n in DOMAINES.values() if n not in par_nom]
    if manquants:
        echec(f"domaine(s) absent(s) du graphe : {manquants}. "
              "Appliquer d'abord make_v102_restore_domain_ii.py")

    # Domaines deja portes par chaque entite.
    actuel = collections.defaultdict(set)
    id2rom = {par_nom[n]: r for r, n in DOMAINES.items()}
    for r in g['relations']:
        if rt_nom.get(r['type']) == 'belongs to domain' and r.get('to') in id2rom:
            actuel[r['from']].add(id2rom[r['to']])

    ajouts, divergences = [], []
    compte = collections.Counter()
    for l in lignes:
        gid = (l.get('gid') or '').strip()
        brut = (l.get('domaine_8') or '').strip()
        cle = brut.replace('*', '').replace('~', '').strip()
        if not gid or not cle:
            continue
        if gid not in E:
            compte['gid absent du graphe'] += 1
            continue
        if cle not in DOMAINES:
            compte[f'domaine_8 inconnu : {cle}'] += 1
            continue
        if l.get('origine') == 'graphe':
            compte['ecarte : domaine herite du graphe (circulaire)'] += 1
            continue
        if gid in actuel:
            if cle in actuel[gid]:
                compte['ecarte : confirme un domaine deja pose'] += 1
            else:
                compte['ecarte : DIVERGE du graphe — signale, non tranche'] += 1
                divergences.append({
                    'gid': gid, 'entite': E[gid].get('name', ''),
                    'domaine_csv': cle, 'domaine_graphe': '|'.join(sorted(actuel[gid])),
                    'attribution': 'par definition' if '*' in brut else 'code a la main',
                    'source': l.get('source', ''), 'id_catalogue': l.get('id', ''),
                })
            continue
        ajouts.append({
            'id': identifiant('rel', gid, cle),
            'type': type_rel, 'from': gid, 'to': par_nom[DOMAINES[cle]],
            'attributes': [],
            '_comment': f"catalogue v2 {l.get('id', '')} — domaine ({cle}) "
                        f"{'par definition' if '*' in brut else 'code a la main'} — "
                        f"source {l.get('source', '')}",
        })
        compte['RETENU : rattachement nouveau'] += 1

    ids_rel = {r.get('id') for r in g['relations'] if r.get('id')}
    for a in ajouts:
        if a['id'] in ids_rel:
            echec(f"identifiant de relation deja present : {a['id']}")

    print(f"source    : {os.path.basename(args.source)}")
    print(f"catalogue : {os.path.basename(args.catalogue)} ({len(lignes)} lignes)")
    for k, n in sorted(compte.items(), key=lambda x: -x[1]):
        print(f"  {n:4d}  {k}")
    print()
    print(f"=== {len(ajouts)} rattachement(s) a poser ===")
    for a in ajouts:
        print(f"  {E[a['from']].get('name', '')[:46]:46s} -> {E[a['to']].get('name', '')[:34]}")
    print()
    print(f"=== {len(divergences)} divergence(s), signalees et NON tranchees ===")
    for d in divergences:
        print(f"  CSV={d['domaine_csv']:5s} graphe={d['domaine_graphe']:9s} "
              f"[{d['attribution']:16s}] {d['entite'][:40]}")

    avant_r = len(g['relations'])
    g['relations'].extend({k: v for k, v in a.items() if not k.startswith('_')}
                          for a in ajouts)

    ids = {e['id'] for e in g['entities']}
    casses = [r for r in g['relations']
              if r.get('from') not in ids or r.get('to') not in ids]
    if len(casses) > 1:
        echec(f"{len(casses)} relations a endpoint absent (attendu 1)")
    if len(g['relations']) != avant_r + len(ajouts):
        echec("le compte de relations ne correspond pas")

    print()
    print(f"  relations : {avant_r} -> {len(g['relations'])}")
    print(f"  entites   : {len(g['entities'])} (inchange)")

    if args.dry_run:
        print("\n--dry-run : rien ecrit.")
        return 0

    with open(args.target, 'w', encoding='utf-8') as f:
        json.dump(g, f, ensure_ascii=False, indent=2)
    print(f"\ngraphe ecrit : {os.path.relpath(args.target, REPO)}")

    if divergences:
        os.makedirs(os.path.dirname(args.divergences), exist_ok=True)
        with open(args.divergences, 'w', encoding='utf-8', newline='') as f:
            w = csv.DictWriter(f, delimiter=';', fieldnames=list(divergences[0]))
            w.writeheader()
            w.writerows(divergences)
        print(f"divergences ecrites : {os.path.relpath(args.divergences, REPO)}")
    return 0


if __name__ == '__main__':
    sys.exit(main())
