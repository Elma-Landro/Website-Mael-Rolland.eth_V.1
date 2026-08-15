#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Decode les fichiers de chronologie et en extrait le domaine par la couleur.

Les chronologies n° 6 de la these sont produites par un logiciel de frise
qui enregistre un format texte : des enregistrements separes par `|`, des
champs separes par `:`. Chaque evenement y porte sa **couleur de fond**, et
cette couleur EST le code couleur des 8 domaines de developpement
infrastructurel (chapitre I, l. 251).

  E3:JJ/MM/AAAA:libelle:couleur_texte:couleur_fond:...

La couleur de texte vaut soit un quadruplet ARGB, soit `B` (defaut) — d'ou
l'alternative dans le motif. Sans elle, 105 des 125 enregistrements du
fichier Bitcoin restaient illisibles.

**La correspondance couleur -> domaine n'est pas devinee.** Elle est calibree
sur les evenements dont `domaine_8` est deja code a la main dans le
catalogue v2, apparies par date exacte : le vert donne (i) a 87 %, le bleu
fonce (iv) a 75 %, le rouge (vi) et l'orange (iii) a 100 %. Les trois autres
sont etablies par le contenu, sans ambiguite — le jaune ne contient que du
minage (GPU, Slush Pool, FPGA, ASIC), le bleu clair que de la reglementation
(BCE, Senat, Tracfin, CFTC).

Interet : la grille de codage marque d'un `*` les attributions faites « par
definition, couleur non verifiee dans le texte/figure ». Ce script rend la
figure verifiable, donc permet de lever ces asterisques et de coder les
lignes qui n'ont pas encore de domaine.

Usage:
    python3 scripts/decode_chronologie.py --entree <fichier.bin> [...]
    python3 scripts/decode_chronologie.py --entree a.bin b.bin --csv sortie.csv
"""
import argparse
import collections
import csv
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from grc20_commun import REPO, normalise_appariement  # noqa: E402

RGBA = r'\d{1,3},\d{1,3},\d{1,3},\d{1,3}'
MOTIF = re.compile(rf'^E3:(\d{{2}}/\d{{2}}/\d{{4}}):(.*?):(?:B|{RGBA}):({RGBA}):', re.S)

# Couleur de fond -> domaine de la these. Voir l'en-tete pour la provenance
# de chaque correspondance.
COULEURS = {
    '255,188,241,158': ('i', '#bcf19e', 'vert', 'calibre : 7/8 sur le catalogue'),
    '255,248,252,146': ('ii', '#f8fc92', 'jaune', 'contenu : minage GPU, Slush, FPGA, ASIC'),
    '255,248,216,136': ('iii', '#f8d888', 'orange', 'calibre : 1/1 sur le catalogue'),
    '255,150,180,247': ('iv', '#96b4f7', 'bleu fonce', 'calibre : 3/4 sur le catalogue'),
    '255,157,239,250': ('v', '#9deffa', 'bleu clair', 'contenu : BCE, Senat, Tracfin, CFTC'),
    '255,247,179,179': ('vi', '#f7b3b3', 'rouge', 'calibre : 2/2 sur le catalogue'),
    '255,240,91,155': ('vii', '#f05b9b', 'rose', 'contenu V2.8 : altcoins, Ethereum, Tether, DAO'),
    '255,237,166,247': ('viii', '#eda6f7', 'violet', 'contenu : levees de fonds, vols, faucet'),
}


def decode(chemin, source):
    """-> [{source, date_iso, titre, couleur, domaine, ...}]"""
    with open(chemin, encoding='utf-8') as f:
        brut = f.read()
    out, illisibles = [], 0
    for enr in brut.split('|'):
        if not enr.startswith('E3:'):
            continue
        m = MOTIF.search(enr)
        if not m:
            illisibles += 1
            continue
        j, mo, a = m.group(1).split('/')
        col = m.group(3)
        dom, hexa, nom_couleur, provenance = COULEURS.get(col, ('', '', '', ''))
        out.append({
            'source': source,
            'date_iso': f'{a}-{mo}-{j}',
            'intitule': ' '.join(m.group(2).split()),
            'couleur_rgba': col,
            'couleur_hex': hexa,
            'couleur_nom': nom_couleur,
            'domaine_8': dom,
            'provenance_correspondance': provenance,
        })
    return out, illisibles


def main(argv=None):
    p = argparse.ArgumentParser(description="Decode les chronologies et leurs domaines.")
    p.add_argument('--entree', nargs='+', required=True)
    p.add_argument('--csv', default=None)
    args = p.parse_args(argv)

    tout, total_illisibles = [], 0
    for chemin in args.entree:
        if not os.path.exists(chemin):
            print(f"ECHEC : fichier introuvable : {chemin}", file=sys.stderr)
            return 2
        src = os.path.basename(chemin).split('.')[0][:40]
        lignes, illisibles = decode(chemin, src)
        total_illisibles += illisibles
        print(f"  {os.path.basename(chemin)[:52]:52s} {len(lignes):4d} evenements"
              f"{f', {illisibles} illisibles' if illisibles else ''}")
        tout += lignes

    # Les deux frises partagent des evenements : on dedoublonne sur
    # (date, libelle normalise), en gardant la premiere occurrence.
    vus, uniques = set(), []
    for e in tout:
        cle = (e['date_iso'], normalise_appariement(e['intitule'])[:60])
        if cle in vus:
            continue
        vus.add(cle)
        uniques.append(e)

    print()
    print(f"total : {len(tout)} enregistrements, {len(uniques)} apres dedoublonnage")
    if total_illisibles:
        print(f"ATTENTION : {total_illisibles} enregistrement(s) illisible(s)")
    sans = [e for e in uniques if not e['domaine_8']]
    print(f"  avec domaine : {len(uniques) - len(sans)}   sans : {len(sans)}")
    for e in sans:
        print(f"    couleur non repertoriee {e['couleur_rgba']} — {e['intitule'][:52]}")
    print()
    c = collections.Counter(e['domaine_8'] for e in uniques if e['domaine_8'])
    for k in ('i', 'ii', 'iii', 'iv', 'v', 'vi', 'vii', 'viii'):
        marque = '   <- absent des frises' if k == 'vii' and not c.get(k) else ''
        print(f"  ({k:4s}) {c.get(k, 0):3d}{marque}")

    if args.csv:
        os.makedirs(os.path.dirname(args.csv), exist_ok=True)
        with open(args.csv, 'w', encoding='utf-8', newline='') as f:
            w = csv.DictWriter(f, delimiter=';', fieldnames=list(uniques[0]))
            w.writeheader()
            w.writerows(sorted(uniques, key=lambda e: e['date_iso']))
        print(f"\ncsv ecrit : {os.path.relpath(args.csv, REPO)} ({len(uniques)} lignes)")
    return 0


if __name__ == '__main__':
    sys.exit(main())
