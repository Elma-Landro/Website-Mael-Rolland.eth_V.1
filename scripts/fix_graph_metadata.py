#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Realigne les metadonnees `space` de chaque graphe sur son nom de fichier.

Les scripts de construction v100 a v104 recopiaient le bloc `space` du
graphe source sans le mettre a jour : les cinq portent `version = "v99"` et
un `generated_at` du 28/03. Les instantanes v96 a v99 sont corrects — le
defaut a ete introduit dans la serie de cette session.

Une metadonnee fausse n'est pas anodine ici : `space` est ce que le pipeline
GRC-20 publie on-chain. Un graphe annonce v99 alors qu'il porte 2 282
entites induit en erreur tout consommateur.

`space.id` n'est PAS touche : il vaut `PLACEHOLDER_DEPLOY_ON_GEO_XYZ` et sa
valeur reelle depend d'un espace GRC-20 que seul l'auteur peut creer.

Usage:
    python3 scripts/fix_graph_metadata.py --dry-run
    python3 scripts/fix_graph_metadata.py
"""
import argparse
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from grc20_commun import REPO, graphes_tries, numero_de_version  # noqa: E402


def main(argv=None):
    p = argparse.ArgumentParser(description="Realigne space.version sur le nom de fichier.")
    p.add_argument('--repo', default=REPO)
    p.add_argument('--dry-run', action='store_true')
    args = p.parse_args(argv)

    corriges = 0
    for chemin in graphes_tries(args.repo):
        n = numero_de_version(chemin)
        attendu = f'v{n}'
        with open(chemin, encoding='utf-8') as f:
            g = json.load(f)
        space = g.setdefault('space', {})
        actuel = space.get('version')
        if actuel == attendu:
            print(f"  OK   {os.path.basename(chemin)[-9:]:>9s}  {actuel}")
            continue

        print(f"  FIX  {os.path.basename(chemin)[-9:]:>9s}  {actuel} -> {attendu} "
              f"({len(g['entities'])} entites, {len(g['relations'])} relations)")
        space['version'] = attendu
        # `generated_at` datait le graphe source ; on le laisse porter la
        # verite de ce fichier-ci sans inventer d'horodatage : on retire la
        # valeur trompeuse plutot que d'en fabriquer une fausse.
        if space.get('generated_at') and n >= 100:
            space['generated_at_source'] = space.pop('generated_at')
        space['entity_count'] = len(g['entities'])
        space['relation_count'] = len(g['relations'])
        corriges += 1

        if not args.dry_run:
            with open(chemin, 'w', encoding='utf-8') as f:
                json.dump(g, f, ensure_ascii=False, indent=2)

    print()
    print(f"{corriges} graphe(s) a corriger" if args.dry_run
          else f"{corriges} graphe(s) corrige(s)")
    return 0


if __name__ == '__main__':
    sys.exit(main())
