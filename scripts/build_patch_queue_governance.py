#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Table de GOUVERNANCE de la file de patchs : que faire de chaque artefact.

DIFFERENCE AVEC `build_patch_queue_inventory.py`. L'inventaire repond « ou en
est ce patch dans le graphe ? ». Celui-ci repond « comment le depot doit-il le
traiter ? » — rejouable ou non, preuve figee ou inventaire vivant, candidat a
la CI ou non. Le premier mesure, le second propose une politique.

CE QU'IL NE FAIT PAS. Il ne modifie aucun patch, aucun graphe, aucune policy.
La colonne `recommended_governance_status` est une PROPOSITION : rien n'est
applique tant que l'auteur n'a pas arbitre.

D'OU VIENNENT LES STATUTS. De l'inventaire mesure, jamais de la `policy` du
patch. C'est le point qui a motive ce chantier : trois patchs candidats ont
ete appliques (v111, v112, v113) et portent toujours, par exigence du controle
C03, la mention « CANDIDATE — NOT APPLIED ». Lire cette phrase induit en
erreur ; mesurer le graphe ne trompe pas.

Usage:
    python3 scripts/build_patch_queue_governance.py           # simulation
    python3 scripts/build_patch_queue_governance.py --csv     # ecrit
    python3 scripts/build_patch_queue_governance.py --check   # CI
"""
import argparse
import csv
import json
import os
import sys
from collections import Counter

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from grc20_commun import REPO, graphe_le_plus_recent  # noqa: E402
import build_patch_queue_inventory as inventaire  # noqa: E402

CODE_DONNEES, CODE_INVOCATION = 1, 2
# Le nom SUIT le graphe de reference, comme celui de l'inventaire. Le figer a
# « -v113 » faisait exactement ce que l'audit reproche par ailleurs : `--graph
# <ancien> --csv` ecrasait le fichier v113 avec les donnees d'une autre
# version, en silence. Un fichier ne doit pas pouvoir mentir sur ce qu'il decrit.
def sortie_pour(graphe):
    version = os.path.basename(graphe).rsplit('-', 1)[-1].removesuffix('.json')
    return os.path.join(REPO, 'docs', 'audits', 'data',
                        f'patch-queue-governance-cases-{version}.csv')

COLONNES = (
    'artifact_path', 'current_label_or_policy', 'measured_status',
    'ops_total', 'ops_readable', 'ops_applied', 'ops_missing_targets',
    'source_graph_declared', 'current_graph',
    'frozen_evidence_or_live_inventory', 'ci_candidate', 'risk_if_replayed',
    'recommended_governance_status', 'note',
)

# Le preflight ne balaie QUE ce motif : C03 ne s'applique donc qu'aux cinq
# fichiers de la racine qui le portent, jamais aux patchs historiques.
MOTIF_SOUS_C03 = 'patch_candidate_'


def echec(msg, code=CODE_DONNEES):
    famille = 'invocation' if code == CODE_INVOCATION else 'donnees'
    print(f"ECHEC ({famille}) : {msg}", file=sys.stderr)
    sys.exit(code)


def politique_courante(doc):
    m = inventaire.meta_de(doc)
    p = m.get('policy')
    if isinstance(p, str) and p:
        return 'CANDIDATE — NOT APPLIED' if p.startswith(
            'CANDIDATE — NOT APPLIED') else p[:60]
    for cle in ('status', 'patch_id', 'description'):
        v = m.get(cle)
        if isinstance(v, str) and v:
            return f'{cle}={v[:40]}'
    return '(aucune)'


def gouvernance(ligne, sous_c03, applique_par):
    """-> (statut recommande, gele/vivant, candidat CI, risque, note).

    Aucune de ces valeurs ne vient de la `policy` : elles derivent du statut
    MESURE et de la forme du patch."""
    mesure = ligne['statut']
    total = int(ligne['nb_ops'] or 0)
    lisibles = int(ligne['ops_lisibles'] or 0)
    faites = int(ligne['ops_deja_realisees'] or 0)
    absentes = int(ligne['ops_cibles_absentes'] or 0)

    if mesure == 'already_applied':
        if sous_c03:
            return ('candidate_applied', 'evidence_frozen', 'non',
                    'rejeu sans effet, mais la policy ment',
                    f'applique par {applique_par} — la mention CANDIDATE est '
                    'exigee par C03 et ne dit PLUS la verite')
        if absentes:
            return ('archive_partial', 'evidence_frozen', 'non',
                    f'{absentes} cible(s) morte(s) : un rejeu echouerait',
                    f'toutes les {lisibles} op(s) LISIBLES sont faites, mais '
                    f'{absentes} cible(s) n existent plus — « applique » '
                    'sur-promet')
        return ('archive_historical', 'evidence_frozen', 'non',
                'rejeu sans effet', 'lot integre, conserve comme archive')

    if mesure == 'indetermine':
        if lisibles == 0:
            return ('archive_historical', 'evidence_frozen', 'non',
                    'forme non lisible par l outil : effet inconnu',
                    'statut NON etabli — a instruire a la main, jamais a '
                    'rejouer par defaut')
        return ('archive_partial', 'evidence_frozen', 'non',
                f'etat MIXTE {faites}/{lisibles} : un rejeu ecrirait a cote',
                'lot partiellement absorbe ; les ops restantes visent des '
                'cibles mortes ou ont ete remplacees par une migration')

    if mesure == 'blocked_by_missing_applicator':
        return ('blocked_missing_applicator', 'evidence_frozen', 'non',
                'aucun applicateur ne consomme ces ops',
                'CREATE_ENTITY : le contrat interdit de pre-assigner un '
                'entityId, et aucun make_* ne lit ce type d op')

    if mesure == 'still_candidate':
        return ('candidate_active', 'evidence_frozen', 'oui',
                'aucun rejeu : rien n est applique',
                f'0 op realisee sur {lisibles} lisibles — le patch est ENTIER '
                'et ses cibles existent. Ni archive ni applique : il attend un '
                'arbitrage')

    if mesure == 'stale_source_graph_but_preconditions_intact':
        return ('candidate_active', 'evidence_frozen', 'oui',
                'aucun rejeu : rien n est applique',
                f'source declaree {ligne["source_graph_declare"]} perimee, '
                'mais les cibles portent encore leur valeur d origine — '
                'seul cas ou une application reste possible')

    return ('indetermine', 'evidence_frozen', 'non', 'inconnu',
            'statut mesure non reconnu par cette table')


def construire(courant):
    lignes_inv = inventaire.construire(courant)
    # Qui a applique quoi : lu dans les applicateurs du depot, pas devine.
    applique_par = {}
    for chemin in sorted(os.listdir(os.path.join(REPO, 'scripts'))):
        if not chemin.startswith('make_v') or not chemin.endswith('.py'):
            continue
        with open(os.path.join(REPO, 'scripts', chemin), encoding='utf-8') as f:
            texte = f.read()
        for l_inv in lignes_inv:
            if os.path.basename(l_inv['chemin']) in texte:
                applique_par[l_inv['chemin']] = chemin

    sorties = []
    for l_inv in lignes_inv:
        chemin = l_inv['chemin']
        with open(os.path.join(REPO, chemin), encoding='utf-8') as f:
            try:
                doc = json.load(f)
            except json.JSONDecodeError:
                doc = {}
        if not isinstance(doc, dict):
            doc = {}
        sous_c03 = os.path.basename(chemin).startswith(MOTIF_SOUS_C03)
        statut, gele, ci, risque, note = gouvernance(
            l_inv, sous_c03, applique_par.get(chemin, '(aucun applicateur)'))
        sorties.append({
            'artifact_path': chemin,
            'current_label_or_policy': politique_courante(doc),
            'measured_status': l_inv['statut'],
            'ops_total': l_inv['nb_ops'],
            'ops_readable': l_inv['ops_lisibles'],
            'ops_applied': l_inv['ops_deja_realisees'],
            'ops_missing_targets': l_inv['ops_cibles_absentes'],
            'source_graph_declared': l_inv['source_graph_declare'],
            'current_graph': os.path.basename(courant),
            'frozen_evidence_or_live_inventory': gele,
            'ci_candidate': ci,
            'risk_if_replayed': risque,
            'recommended_governance_status': statut,
            'note': note,
        })
    sorties.sort(key=lambda x: x['artifact_path'])
    return sorties


def main():
    ap = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--graph', default=None)
    ap.add_argument('--csv', action='store_true')
    ap.add_argument('--check', action='store_true')
    args = ap.parse_args()
    if args.csv and args.check:
        ap.error('--csv et --check sont exclusifs.')

    courant = args.graph or graphe_le_plus_recent(REPO)
    if not courant:
        echec('aucun graphe numerote dans le depot', CODE_INVOCATION)
    lignes = construire(courant)

    print(f'graphe de reference : {os.path.basename(courant)}')
    print(f'{len(lignes)} artefact(s)\n')
    for statut, n in sorted(Counter(
            ligne['recommended_governance_status'] for ligne in lignes).items()):
        print(f'  {n:3d}  {statut}')
    ci = sum(1 for ligne in lignes if ligne['ci_candidate'] == 'oui')
    print(f'\n  {ci} artefact(s) encore applicable(s) — les seuls que la CI '
          'aurait a surveiller')

    if args.check:
        sortie = sortie_pour(courant)
        if not os.path.exists(sortie):
            print(f'--check : {os.path.relpath(sortie, REPO)} absent.',
                  file=sys.stderr)
            return 1
        with open(sortie, encoding='utf-8', newline='') as f:
            verse = list(csv.DictReader(f, delimiter=';'))
        recalcule = [{k: str(v) for k, v in ligne.items()} for ligne in lignes]
        if verse != recalcule:
            print('--check : le CSV verse differe du CSV recalcule.',
                  file=sys.stderr)
            return 1
        print('\n--check : la table de gouvernance est a jour.')
        return 0

    if not args.csv:
        print('\n(simulation — relancer avec --csv pour ecrire)')
        return 0

    sortie = sortie_pour(courant)
    temporaire = sortie + '.tmp'
    with open(temporaire, 'w', encoding='utf-8', newline='') as f:
        w = csv.DictWriter(f, fieldnames=COLONNES, delimiter=';')
        w.writeheader()
        w.writerows(lignes)
    os.replace(temporaire, sortie)
    print(f'\necrit : {os.path.relpath(sortie, REPO)} ({len(lignes)} lignes)')
    return 0


if __name__ == '__main__':
    sys.exit(main())
