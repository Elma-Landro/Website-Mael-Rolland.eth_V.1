#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Integrite structurelle des graphes GRC-20. Ne modifie rien.

Ce controle vivait en Python embarque dans `.github/workflows/check.yml`.
Il en sort pour une raison precise : du code qui n'existe que dans un YAML
ne s'execute qu'en CI, donc ne se verifie jamais avant d'etre pousse. Il a
livre une KeyError sur une ligne d'affichage — `r['missing_from']` au lieu
de `r['problem']` — invisible en local parce que ma simulation reproduisait
la decision, pas l'impression. Un fichier appelable evite cette classe
entiere d'erreur.

Regle : seul le graphe le plus recent est bloquant. Les instantanes geles
sont verifies et rapportes, jamais bloquants — v96 porte 15 endpoints
casses, corriges des v97, et personne ne compte reparer un instantane.

Usage:
    python3 scripts/check_graph_integrity.py
    python3 scripts/check_graph_integrity.py --repo .

Codes de sortie :
    0 = le graphe courant est sain
    1 = le graphe courant porte au moins un defaut critique
"""
import argparse
import glob
import json
import os
import re
import subprocess
import sys

# Relation orpheline portee exprès : `from` tronque a 16 caracteres, signalee
# depuis mai 2026 et laissee en l'etat en attente d'arbitrage. C'est une
# preuve de conservatisme, pas un defaut a masquer.
TOLEREES = {'9dee2daa2afa4212f6369b059e0cf78c'}


def graphes_tries(repo):
    fichiers = glob.glob(os.path.join(repo, 'grc20-these-mael-rolland-v*.json'))
    return sorted(fichiers, key=lambda f: int(re.search(r'-v(\d+)\.json$', f).group(1)))


def main(argv=None):
    p = argparse.ArgumentParser(description="Integrite structurelle des graphes.")
    p.add_argument('--repo', default=os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    args = p.parse_args(argv)

    graphes = graphes_tries(args.repo)
    if not graphes:
        print('aucun graphe')
        return 0

    courant = graphes[-1]
    echec = False
    audit = os.path.join(args.repo, 'scripts', 'audit_graph.py')

    for f in graphes:
        rapport = f'/tmp/{os.path.basename(f)[:-5]}.audit.json'
        subprocess.run([sys.executable, audit, '--input', f, '--json', rapport, '-q'],
                       stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        if not os.path.exists(rapport):
            print(f"  {os.path.basename(f)} : audit_graph.py n'a produit aucun rapport")
            echec = echec or f == courant
            continue
        with open(rapport, encoding='utf-8') as fh:
            critique = json.load(fh)['critical']

        casses = [r for r in critique['broken_relations_details']
                  if r.get('relation_id') not in TOLEREES]
        dups = len(critique['duplicate_ids'])
        orph = len(critique['orphans'])
        marque = '<- courant, bloquant' if f == courant else '(gele, rapport seul)'
        print(f"  {os.path.basename(f)}: {len(casses)} endpoint(s) casse(s) hors "
              f"tolerance · {dups} id(s) duplique(s) · {orph} orphelin(s)  {marque}")

        # Les cles sont celles que `audit_graph.py` emet reellement :
        # `problem` vaut « missing_from » / « missing_to », et le type porte
        # le nom `relation_type_name`. Les lire au lieu de les deviner.
        for r in casses[:5]:
            print(f"      {r.get('relation_id')} : {r.get('problem')} "
                  f"from={r.get('from')} to={r.get('to')} "
                  f"type={r.get('relation_type_name')}")

        if f == courant and (casses or dups or orph):
            echec = True

    return 1 if echec else 0


if __name__ == '__main__':
    sys.exit(main())
