#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Compare 5 politiques d'affichage des panneaux du lecteur — DETERMINISTE.

Le lecteur (`lecteur.html`) classe chaque panneau de section : epingles de
`section_overrides.json` d'abord, puis top-12 par score TF-IDF
occurrence_count x log(N/df), bris d'egalite par entity_id croissant
(convention du depot, cf. build_anchor_weights.py --impact). Ce script ne
change RIEN : il simule 5 politiques de classement et mesure ce que chacune
ferait au top-12 de chaque section, par rapport a la politique en vigueur.

LES 5 POLITIQUES :
  legacy          epingles d'abord, puis score legacy decroissant. Reference.
  verified-first  epingles ; puis snippet_status dans {self, self-base} par
                  score legacy ; puis toutes les autres par score legacy.
                  Pur reordonnancement, personne n'est exclu.
  direct-count    epingles ; puis direct_anchor_count >= 1 tries par
                  direct x log(N/dfd) (dfd = nb de sections ou l'entite a
                  direct >= 1) ; puis FALLBACK des restantes (direct 0 ou
                  null) par score legacy — le panneau ne se vide jamais.
  hybrid-cautious epingles ; puis classe de statut croissante (self=0,
                  self-base=1, proxy=2, no-snippet=3), a l'interieur d'une
                  classe par score legacy.
  diagnostic-only ordre strictement identique a legacy (les badges sont une
                  affaire d'interface) — survie 100 % par construction,
                  la ligne sert de temoin.
Tous les tris cassent les egalites par entity_id croissant.

SORTIES :
  - CSV docs/audits/data/panel-policy-impact-v110.csv (separateur ;) :
    une ligne par (section_key, politique), les 5 politiques incluses.
  - Synthese imprimee : survie par politique, sections les plus
    bouleversees, sections pauvres en candidats mesures, places perdues
    par type d'entite.
  - Auto-controle : la variante STRICTE de direct-count (candidats mesures
    seuls, sans fallback) doit reproduire exactement le chiffre de
    build_anchor_weights.py --impact (294/648 sur v110).

CE QUE CE SCRIPT NE FAIT PAS : il ne modifie ni la carte, ni le graphe, ni
les overrides, ni aucun fichier existant. Stdlib uniquement.

Usage:
    python3 scripts/compare_panel_policies.py
    python3 scripts/compare_panel_policies.py --top 12 --csv <chemin>
"""
import argparse
import collections
import csv
import json
import math
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from grc20_commun import REPO, graphe_le_plus_recent  # noqa: E402

SEM = os.path.join(REPO, 'section_entities_map.json')
OVERRIDES = os.path.join(REPO, 'section_overrides.json')
CSV_OUT = os.path.join(REPO, 'docs', 'audits', 'data',
                       'panel-policy-impact-v110.csv')

POLITIQUES = ('diagnostic-only', 'direct-count', 'hybrid-cautious',
              'legacy', 'verified-first')
CLASSE_STATUT = {'self': 0, 'self-base': 1, 'proxy': 2, 'no-snippet': 3}


def charge_json(chemin, quoi):
    """Charge un JSON ou echoue proprement — aucun echec silencieux."""
    if not chemin or not os.path.exists(chemin):
        print(f"ERREUR : {quoi} introuvable : {chemin}", file=sys.stderr)
        sys.exit(2)
    with open(chemin, encoding='utf-8') as f:
        return json.load(f)


def type_premier(graphe):
    """-> {entity_id: nom du premier type}. 'INCONNU' si rien d'exploitable."""
    nom_type = {t['id']: t.get('name', t['id']) for t in graphe.get('types', [])}
    out = {}
    for e in graphe.get('entities', []):
        types = e.get('types') or []
        out[e['id']] = nom_type.get(types[0], types[0]) if types else 'INCONNU'
    return out


def ordonne(reste, cle_tri):
    """Ids de `reste` tries par cle_tri, bris d'egalite entity_id croissant."""
    return [e['entity_id'] for e in sorted(reste, key=cle_tri)]


def top_de(pins, ordre_ids, top):
    """Le panneau : epingles d'abord, puis l'ordre, tronque a `top`."""
    return (list(pins) + ordre_ids)[:top]


def main(argv=None):
    p = argparse.ArgumentParser(
        description="Compare 5 politiques d'affichage des panneaux "
                    "(simulation deterministe, aucun fichier modifie).")
    p.add_argument('--csv', default=CSV_OUT,
                   help="chemin du CSV de sortie (defaut : %(default)s)")
    p.add_argument('--graph', default=None,
                   help="graphe de reference (defaut : le plus recent, "
                        "motif grc20-these-mael-rolland-v(\\d+).json)")
    p.add_argument('--map', default=SEM,
                   help="carte section -> entites (defaut : %(default)s)")
    p.add_argument('--overrides', default=OVERRIDES,
                   help="epingles par section (defaut : %(default)s)")
    p.add_argument('--top', type=int, default=12,
                   help="taille du panneau (defaut : 12)")
    args = p.parse_args(argv)

    sem = charge_json(args.map, 'carte section -> entites')
    ov = charge_json(args.overrides, 'fichier des epingles')
    chemin_graphe = args.graph or graphe_le_plus_recent()
    graphe = charge_json(chemin_graphe, 'graphe de reference')
    type_de = type_premier(graphe)
    top = args.top

    # frequences documentaires — N compte TOUTES les cles de la carte,
    # comme le lecteur et comme build_anchor_weights.py --impact
    N = len(sem)
    df = collections.Counter()
    dfd = collections.Counter()
    for d in sem.values():
        for e in d.get('entities', []):
            df[e['entity_id']] += 1
            if (e.get('direct_anchor_count') or 0) >= 1:
                dfd[e['entity_id']] += 1

    def score_legacy(e):
        return e['occurrence_count'] * math.log(N / (df[e['entity_id']] or 1))

    def score_direct(e):
        d = e.get('direct_anchor_count') or 0
        return d * math.log(N / (dfd[e['entity_id']] or 1))

    # ---------- simulation ----------
    lignes = []          # (section_key, policy, top_size, surv, nouveaux,
    #                       mesures, epingles)
    survie = collections.Counter()       # policy -> survivants cumules
    total = collections.Counter()        # policy -> places legacy cumulees
    pires = collections.defaultdict(list)  # policy -> [(surv, cle, taille)]
    perdus_par_type = collections.defaultdict(collections.Counter)
    surv_strict = tot_strict = 0
    sections_pauvres = 0

    for cle in sorted(sem):
        ents = sem[cle].get('entities', [])
        if not ents:
            continue
        pins = [i for i in (ov.get(cle) or []) if isinstance(i, str)]
        reste = [e for e in ents if e['entity_id'] not in set(pins)]
        mesures = sum(1 for e in ents
                      if (e.get('direct_anchor_count') or 0) >= 1)
        if mesures < 3:
            sections_pauvres += 1

        ordre_legacy = ordonne(reste, lambda e: (-score_legacy(e),
                                                 e['entity_id']))
        panneaux = {
            'legacy': top_de(pins, ordre_legacy, top),
            'diagnostic-only': top_de(pins, ordre_legacy, top),
        }
        # verified-first : reordonnancement, personne n'est exclu
        panneaux['verified-first'] = top_de(pins, ordonne(
            reste, lambda e: (
                0 if e.get('snippet_status') in ('self', 'self-base') else 1,
                -score_legacy(e), e['entity_id'])), top)
        # hybrid-cautious : par classe de statut, puis score legacy
        panneaux['hybrid-cautious'] = top_de(pins, ordonne(
            reste, lambda e: (
                CLASSE_STATUT.get(e.get('snippet_status'), 4),
                -score_legacy(e), e['entity_id'])), top)
        # direct-count : mesures d'abord, puis fallback legacy
        avec_direct = [e for e in reste
                       if (e.get('direct_anchor_count') or 0) >= 1]
        sans_direct = [e for e in reste
                       if (e.get('direct_anchor_count') or 0) < 1]
        ordre_direct = ordonne(avec_direct,
                               lambda e: (-score_direct(e), e['entity_id']))
        panneaux['direct-count'] = top_de(
            pins, ordre_direct + ordonne(
                sans_direct, lambda e: (-score_legacy(e), e['entity_id'])),
            top)

        # auto-controle : variante STRICTE (sans fallback), formule de
        # build_anchor_weights.py --impact — doit donner 294/648 sur v110
        strict = top_de(pins, ordre_direct, top)
        ref = set(panneaux['legacy'])
        surv_strict += len(ref & set(strict))
        tot_strict += len(panneaux['legacy'])

        for pol in POLITIQUES:
            haut = panneaux[pol]
            s = len(ref & set(haut))
            lignes.append((cle, pol, len(haut), s, len(set(haut) - ref),
                           mesures, len(pins)))
            survie[pol] += s
            total[pol] += len(panneaux['legacy'])
            pires[pol].append((s, cle, len(panneaux['legacy'])))
            for eid in ref - set(haut):
                perdus_par_type[pol][type_de.get(eid, 'INCONNU')] += 1

    # ---------- CSV ----------
    dossier = os.path.dirname(args.csv)
    if dossier:
        os.makedirs(dossier, exist_ok=True)
    lignes.sort(key=lambda x: (x[0], x[1]))
    with open(args.csv, 'w', encoding='utf-8', newline='') as f:
        w = csv.writer(f, delimiter=';', lineterminator='\n')
        w.writerow(['section_key', 'policy', 'top12_size',
                    'survivors_vs_legacy', 'new_entrants',
                    'measured_candidates', 'pinned'])
        for ligne in lignes:
            w.writerow([str(c).replace(';', ',') for c in ligne])

    # ---------- synthese ----------
    print(f"graphe : {os.path.relpath(chemin_graphe, REPO)}")
    print(f"sections : {N} · panneaux simules : "
          f"{len(lignes) // len(POLITIQUES)} · top : {top}")
    print(f"csv : {os.path.relpath(args.csv, REPO)}")
    print(f"\nauto-controle direct STRICT (sans fallback, formule --impact) : "
          f"{surv_strict}/{tot_strict} "
          f"({100 * surv_strict // (tot_strict or 1)} %)")
    print(f"sections avec < 3 candidats mesures : {sections_pauvres}")
    for pol in POLITIQUES:
        t = total[pol] or 1
        print(f"\n=== {pol} ===")
        print(f"  survie top-{top} : {survie[pol]}/{total[pol]} "
              f"({100 * survie[pol] // t} %)")
        bouleversees = sorted(pires[pol], key=lambda x: (x[0], x[1]))[:8]
        print("  les 8 sections les plus bouleversees :")
        for s, cle, n in bouleversees:
            print(f"    {cle:20s} survivants {s:2d}/{n:2d}")
        if perdus_par_type[pol]:
            print("  places perdues vs legacy, par type d'entite :")
            for nom, n in perdus_par_type[pol].most_common(5):
                print(f"    {n:4d}  {nom}")
        else:
            print("  places perdues vs legacy : aucune")
    return 0


if __name__ == '__main__':
    sys.exit(main())
