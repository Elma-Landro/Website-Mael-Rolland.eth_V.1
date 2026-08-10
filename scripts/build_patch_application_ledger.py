#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Construit `patch-application-ledger.json` : la MEMOIRE D'APPLICATION.

Arbitrage de l'auteur du 2026-08-09, Q3. Le partage des roles est le suivant,
et il faut l'avoir en tete pour lire ce fichier :

    le PATCH   est l'objet de PROPOSITION — sa `policy` dit ce qu'il etait
               au moment de sa redaction, jamais ce qu'il est devenu ;
    le LEDGER  est la memoire d'APPLICATION — qui a applique quoi, quand,
               vers quelle version, avec quel resultat mesure ;
    le GRAPHE  est la PREUVE FINALE — en cas de desaccord, c'est lui qui
               tranche, et ce script le lui demande a chaque execution.

Le ledger n'est donc PAS une source de verite autonome : chaque ligne porte
un `measured` relu dans le graphe courant. Si un jour le ledger dit
« applique » et que la mesure dit 0/10, c'est le ledger qui a tort.

Lecture seule sur le graphe et les patchs. N'ecrit que son propre fichier.

Usage:
    python3 scripts/build_patch_application_ledger.py           # simulation
    python3 scripts/build_patch_application_ledger.py --write
    python3 scripts/build_patch_application_ledger.py --check   # CI
"""
import argparse
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from grc20_commun import REPO, graphe_le_plus_recent  # noqa: E402
import build_patch_queue_inventory as inventaire  # noqa: E402

SORTIE = os.path.join(REPO, 'patch-application-ledger.json')
CODE_DONNEES = 1


def echec(msg):
    print(f'ECHEC (donnees) : {msg}', file=sys.stderr)
    sys.exit(CODE_DONNEES)

# Applications connues, ecrites a la main parce qu'elles portent ce qu'aucun
# fichier ne sait : la PR et le commit qui les ont portees. Le reste (ops
# attendues, ops appliquees, statut) est MESURE a chaque execution.
APPLICATIONS = (
    {'patch': 'patch_candidate_section_page_start_v1.json',
     'applicator': 'scripts/make_v111_apply_section_page_start_patch.py',
     'source_version': 'v110', 'applied_version': 'v111',
     'pr': 117, 'date': '2026-08-08'},
    {'patch': 'patch_candidate_chronology_dates_v1.json',
     'applicator': 'scripts/make_v112_apply_chronology_dates_patch.py',
     'source_version': 'v111', 'applied_version': 'v112',
     'pr': 119, 'date': '2026-08-09'},
    {'patch': 'patch_candidate_bibliographie_retypes_v1.json',
     'applicator': 'scripts/make_v113_apply_bibliography_retypes.py',
     'source_version': 'v112', 'applied_version': 'v113',
     'pr': 120, 'date': '2026-08-09'},
)


def construire(courant):
    par_chemin = {ligne['chemin']: ligne
                  for ligne in inventaire.construire(courant)}
    entrees = []
    for app in APPLICATIONS:
        # Un patch absent de l'inventaire ne doit PAS retomber sur `{}` : le
        # ledger ecrirait alors 0/0 `inconnu` — un bloc `measured` d'apparence
        # normale, qui dit « rien de mesure » exactement comme il dirait « rien
        # d'applique ». C'est le defaut que ce fichier existe pour corriger,
        # reproduit a l'interieur de lui-meme. Chemin faux, fichier supprime,
        # exclusion trop large : tout cela doit se voir bruyamment.
        if app['patch'] not in par_chemin:
            echec(f"{app['patch']} est declare applique mais absent de "
                  "l inventaire — chemin errone, fichier supprime, ou capte "
                  'par une exclusion. Le ledger refuse de mesurer a vide.')
        ligne = par_chemin[app['patch']]
        chemin = os.path.join(REPO, app['patch'])
        declaree = ''
        if os.path.exists(chemin):
            with open(chemin, encoding='utf-8') as f:
                meta = inventaire.meta_de(json.load(f))
            declaree = str(meta.get('policy', ''))[:48]
        entrees.append({
            'patch': app['patch'],
            'applicator': app['applicator'],
            'source_version': app['source_version'],
            'applied_version': app['applied_version'],
            'pr': app['pr'],
            'date': app['date'],
            'policy_declared': declaree,
            'measured': {
                'graph': os.path.basename(courant),
                'ops_total': int(ligne.get('nb_ops') or 0),
                'ops_readable': int(ligne.get('ops_lisibles') or 0),
                'ops_applied': int(ligne.get('ops_deja_realisees') or 0),
                'ops_missing_targets': int(ligne.get('ops_cibles_absentes') or 0),
                'status': ligne.get('statut', 'inconnu'),
            },
        })
    return {
        '_meta': {
            'purpose': "Memoire d'application des patchs. Le patch propose, "
                       'le ledger se souvient, le GRAPHE prouve. En cas de '
                       'desaccord, le graphe tranche.',
            'arbitration': "Maël Rolland, 2026-08-09, Q3",
            'generated_by': 'scripts/build_patch_application_ledger.py',
            'warning': "La `policy` d'un patch applique reste « CANDIDATE — "
                       'NOT APPLIED » : C03 l exige. Cette phrase est '
                       'historiquement fausse apres application. Lire le '
                       'statut dans le graphe, la file vivante, puis ce '
                       'ledger — jamais dans la policy.',
        },
        'applications': entrees,
    }


def main():
    ap = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--graph', default=None)
    ap.add_argument('--write', action='store_true')
    ap.add_argument('--check', action='store_true')
    args = ap.parse_args()
    if args.write and args.check:
        ap.error('--write et --check sont exclusifs.')

    courant = args.graph or graphe_le_plus_recent(REPO)
    ledger = construire(courant)
    for e in ledger['applications']:
        m = e['measured']
        print(f"  {e['patch'][:52]:52s} {e['applied_version']} PR#{e['pr']} "
              f"-> {m['ops_applied']}/{m['ops_readable']} {m['status']}")

    if args.check:
        if not os.path.exists(SORTIE):
            print(f'--check : {os.path.basename(SORTIE)} absent.',
                  file=sys.stderr)
            return 1
        with open(SORTIE, encoding='utf-8') as f:
            if json.load(f) != ledger:
                print('--check : le ledger verse differe du ledger recalcule.',
                      file=sys.stderr)
                return 1
        print('\n--check : le ledger est a jour.')
        return 0

    if not args.write:
        print('\n(simulation — relancer avec --write)')
        return 0
    temporaire = SORTIE + '.tmp'
    with open(temporaire, 'w', encoding='utf-8') as f:
        json.dump(ledger, f, ensure_ascii=False, indent=2)
        f.write('\n')
    os.replace(temporaire, SORTIE)
    print(f'\necrit : {os.path.basename(SORTIE)}')
    return 0


if __name__ == '__main__':
    sys.exit(main())
