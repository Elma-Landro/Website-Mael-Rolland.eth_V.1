#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Ecrit dans chaque patch candidat racine un bloc `_meta` de cycle de vie.

LE PROBLEME QU'IL RESOUT. Le controle C03 de `preflight_candidate_patches.py`
EXIGE que la `policy` d'un candidat commence par « CANDIDATE — NOT APPLIED —
AUTHOR ARBITRATION REQUIRED ». Trois de ces patchs ont pourtant ete appliques
(v111, v112, v113) et portent toujours cette phrase, en toutes lettres. Un
agent qui lit la policy conclut l'inverse de la verite. Ce script ajoute, A
COTE de la policy et sans jamais y toucher, une mention lisible de l'etat reel.

CE QU'IL N'EST PAS. `lifecycleStatus` n'est PAS une source de verite : c'est
une COPIE DATEE d'une mesure faite ailleurs. L'autorite reste le graphe, via
`build_patch_queue_inventory.py` puis `build_patch_queue_governance.py`. C'est
pourquoi ce script ne sait pas ecrire un statut « a la main » : il ne fait que
recopier ce que la table de gouvernance mesure, et `--check` rougit des que la
copie s'ecarte de la mesure. Une declaration qui ne peut pas devenir fausse
sans qu'on le voie n'est pas une source de verite concurrente.

CE QU'IL NE TOUCHE JAMAIS. `ops`, `policy`, et toute cle `_meta` hors de
CLES_LIFECYCLE. La garantie n'est pas une intention : une signature du patch
prive de ces cles est comparee avant / apres, et l'ecriture est refusee si
quoi que ce soit d'autre a bouge.

Usage:
    python3 scripts/build_patch_lifecycle_status.py           # simulation
    python3 scripts/build_patch_lifecycle_status.py --write   # ecrit
    python3 scripts/build_patch_lifecycle_status.py --check   # CI
"""
import argparse
import glob
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from grc20_commun import REPO, graphe_le_plus_recent  # noqa: E402
import build_patch_queue_governance as gouv  # noqa: E402

CODE_DONNEES, CODE_INVOCATION = 1, 2

# Le preflight ne balaie que ce motif a la racine : le perimetre de ce script
# est EXACTEMENT celui de C03, ni plus ni moins. Les patchs historiques
# (`patch_1a`, `new_relations_patch.json`, `patches/**`) ne sont pas soumis a
# C03 et ne recoivent donc rien — les reecrire falsifierait une archive.
MOTIF = 'patch_candidate_*.json'

# Les SEULES cles que ce script a le droit d'ecrire. Tout le reste du fichier
# est verifie identique avant / apres.
CLES_LIFECYCLE = (
    'lifecycleStatus', 'lifecycleGeneratedBy', 'measuredAgainstGraph',
    'measuredStatus', 'appliedBy', 'appliedInGraph', 'appliedInPR',
    'ledgerEntry', 'noteForAgents',
)

# Vocabulaire arrete par l'auteur (arbitrage Q2 du 2026-08-09, PR #121). Un
# statut mesure hors de cette liste n'est PAS traduit d'office : le script
# echoue. Un patch candidat racine qui se mesurerait `archive_historical`
# serait une anomalie a instruire, pas une valeur a recopier.
VOCABULAIRE = (
    'candidate_applied', 'blocked_author_arbitration',
    'blocked_missing_applicator', 'candidate_active', 'candidate_superseded',
    'dangerous_do_not_replay', 'indetermine',
)

NOTES = {
    'candidate_applied':
        "APPLIQUE. Ne pas rejouer : les ops de ce fichier ont deja leur effet "
        "dans le graphe courant. La `policy` ci-dessus dit « NOT APPLIED » "
        "parce que le controle C03 l exige, pas parce que c est vrai. "
        "Autorite : le graphe, puis docs/audits/data/"
        "patch-queue-governance-cases-current.csv, puis "
        "patch-application-ledger.json — jamais la policy, jamais ce champ.",
    'blocked_author_arbitration':
        "NON APPLIQUE, et techniquement applicable n est PAS mur. Les cibles "
        "existent et les preconditions tiennent, mais l arbitrage de l auteur "
        "n a pas ete rendu : a reauditer avant tout chantier d application "
        "(arbitrage Q7 du 2026-08-09). Ce champ ne vaut pas feu vert.",
    'blocked_missing_applicator':
        "NON APPLICABLE EN L ETAT. Aucun applicateur du depot ne consomme ces "
        "ops, et le contrat de patch interdit de pre-assigner un entityId sur "
        "une creation. Ecrire l applicateur est un chantier a part entiere, "
        "distinct de l arbitrage scientifique sur le contenu.",
}


def echec(msg, code=CODE_DONNEES):
    famille = 'invocation' if code == CODE_INVOCATION else 'donnees'
    print(f'ECHEC ({famille}) : {msg}', file=sys.stderr)
    sys.exit(code)


def signature(doc):
    """Le patch prive des cles de cycle de vie, en JSON canonique.

    Sert de preuve que rien d autre n a bouge. On enumere TOUTES les cles de
    tete et TOUTES les cles de `_meta` plutot que de projeter sur une liste
    choisie : une signature qui ne regarde que ce qu on pense avoir touche ne
    prouve rien (defaut deja rencontre sur make_v112)."""
    copie = json.loads(json.dumps(doc))
    meta = copie.get('_meta')
    if isinstance(meta, dict):
        for cle in CLES_LIFECYCLE:
            meta.pop(cle, None)
    return json.dumps(copie, ensure_ascii=False, sort_keys=True)


def ledger_par_patch():
    chemin = os.path.join(REPO, 'patch-application-ledger.json')
    if not os.path.exists(chemin):
        return {}
    with open(chemin, encoding='utf-8') as f:
        doc = json.load(f)
    return {e['patch']: e for e in doc.get('applications', [])}


def bloc_pour(nom, ligne_gouv, entree_ledger, courant):
    """Le bloc `_meta` de cycle de vie d un patch — entierement DERIVE."""
    statut = ligne_gouv['recommended_governance_status']
    if statut not in VOCABULAIRE:
        echec(f'{nom} : statut mesure « {statut} » hors du vocabulaire arrete '
              f'par l auteur ({", ".join(VOCABULAIRE)}). Un candidat racine '
              'qui se mesure ainsi est une anomalie a instruire, pas une '
              'valeur a recopier d office.')
    if statut not in NOTES:
        echec(f'{nom} : aucune note redigee pour le statut « {statut} » — '
              'un champ noteForAgents vide serait pire que pas de champ.')
    bloc = {
        'lifecycleStatus': statut,
        'lifecycleGeneratedBy': 'scripts/build_patch_lifecycle_status.py',
        'measuredAgainstGraph': os.path.basename(courant),
        'measuredStatus': ligne_gouv['measured_status'],
    }
    if entree_ledger:
        bloc['appliedBy'] = entree_ledger['applicator']
        bloc['appliedInGraph'] = (
            f"grc20-these-mael-rolland-{entree_ledger['applied_version']}.json")
        bloc['appliedInPR'] = entree_ledger['pr']
        bloc['ledgerEntry'] = 'patch-application-ledger.json'
    elif statut == 'candidate_applied':
        # Un patch mesure applique sans entree au ledger : c est exactement le
        # trou de memoire que le ledger existe pour combler. On refuse de le
        # masquer par un bloc d apparence complete.
        echec(f'{nom} : mesure `candidate_applied` mais ABSENT du ledger. '
              'Renseigner patch-application-ledger.json avant de declarer un '
              'cycle de vie.')
    bloc['noteForAgents'] = NOTES[statut]
    return bloc


def construire(courant):
    """-> [(nom, chemin, doc d origine, bloc a ecrire)], trie par nom."""
    par_chemin = {ligne['artifact_path']: ligne
                  for ligne in gouv.construire(courant)}
    ledger = ledger_par_patch()
    sorties = []
    for chemin in sorted(glob.glob(os.path.join(REPO, MOTIF))):
        nom = os.path.basename(chemin)
        if nom not in par_chemin:
            echec(f'{nom} est un candidat racine mais ne figure pas dans la '
                  'table de gouvernance : le cycle de vie ne peut pas etre '
                  'derive d une mesure absente.')
        with open(chemin, encoding='utf-8') as f:
            doc = json.load(f)
        if not isinstance(doc.get('_meta'), dict):
            echec(f'{nom} : _meta absent ou mal forme — C02 le refuserait '
                  'deja ; ce script ne le repare pas.')
        sorties.append((nom, chemin, doc,
                        bloc_pour(nom, par_chemin[nom], ledger.get(nom),
                                  courant)))
    return sorties


def ecrire(chemin, doc, bloc):
    """Ecriture atomique, apres preuve que seul le bloc a bouge."""
    avant = signature(doc)
    neuf = json.loads(json.dumps(doc))
    meta = neuf['_meta']
    for cle in CLES_LIFECYCLE:          # reecrit en position stable, en fin
        meta.pop(cle, None)             # de _meta, quel que soit l existant
    meta.update(bloc)
    if signature(neuf) != avant:
        echec(f'{os.path.basename(chemin)} : la signature du patch prive des '
              'cles de cycle de vie a change — une op, une value ou la policy '
              'aurait bouge. Ecriture refusee.')
    temporaire = chemin + '.tmp'
    with open(temporaire, 'w', encoding='utf-8') as f:
        json.dump(neuf, f, ensure_ascii=False, indent=2)
        f.write('\n')
    os.replace(temporaire, chemin)


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
    if not courant:
        echec('aucun graphe numerote dans le depot', CODE_INVOCATION)
    lignes = construire(courant)

    print(f'graphe de reference : {os.path.basename(courant)}')
    print(f'{len(lignes)} patch(s) candidat(s) racine\n')
    for nom, _, _, bloc in lignes:
        applique = bloc.get('appliedInGraph', '—')
        print(f"  {nom[:50]:50s} {bloc['lifecycleStatus']:28s} {applique}")

    if args.check:
        perimes = []
        for nom, _, doc, bloc in lignes:
            actuel = {c: doc['_meta'][c] for c in CLES_LIFECYCLE
                      if c in doc['_meta']}
            if actuel != bloc:
                perimes.append(nom)
        if perimes:
            print('\n--check : declaration PERIMEE ou absente sur '
                  f"{len(perimes)} patch(s) : {', '.join(perimes)}\n"
                  '  La mesure fait autorite, pas la declaration : relancer '
                  '--write.', file=sys.stderr)
            return 1
        print('\n--check : chaque lifecycleStatus declare egale la mesure.')
        return 0

    if not args.write:
        print('\n(simulation — relancer avec --write pour ecrire)')
        return 0

    touches = 0
    for nom, chemin, doc, bloc in lignes:
        actuel = {c: doc['_meta'][c] for c in CLES_LIFECYCLE
                  if c in doc['_meta']}
        if actuel == bloc:
            continue
        ecrire(chemin, doc, bloc)
        touches += 1
    print(f'\necrit : {touches} patch(s) mis a jour, '
          f'{len(lignes) - touches} deja a jour')
    return 0


if __name__ == '__main__':
    sys.exit(main())
