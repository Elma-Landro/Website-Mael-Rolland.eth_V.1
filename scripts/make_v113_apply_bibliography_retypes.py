#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Applique patch_candidate_bibliographie_retypes_v1.json et produit v113.

CE QUE CE SCRIPT FAIT, ET RIEN D'AUTRE. Sur SIX fiches, il change le type
`Reference` -> `Person`, et sur QUATRE d'entre elles il corrige aussi le
prenom :

    5fc4278b…  Laura DeNardis            Reference -> Person
    b332ace8…  Shinobi (pseudonyme)      Reference -> Person
    ec901513…  Audrey  -> Adli Takkal Bataille   + Reference -> Person
    be8ac286…  Gregor  -> Andreas Loibl          + Reference -> Person
    7cd4cfe4…  Guillaume -> Gerard Drean         + Reference -> Person
    53525938…  Jerome  -> Jacques Favier         + Reference -> Person

Il ne cree aucune entite, aucune relation, aucune SourceQuote. Il ne fusionne
rien, n'annote aucun doublon, ne touche aucun attribut. Toute op qui n'est ni
`SET_TYPES` ni `SET_NAME` est REFUSEE, pas ignoree.

POURQUOI CES SIX FICHES SONT FAUSSES. Elles sont typees `Reference` alors
qu'elles designent des PERSONNES — c'est le residu du lot patch_18, qui avait
retype 21 fiches d'auteur et laisse celles-ci de cote. Et sur quatre d'entre
elles, le graphe attribue un PRENOM INVENTE a une personne reelle et vivante.
Les quatre prenoms cibles sont attestes mot pour mot dans la bibliographie de
la these (`assets/MD/07_bibliographie.md`) :

    Adli TAKKAL BATAILLE   l.476   « FAVIER Jacques et TAKKAL BATAILLE Adli, 2017 »
    Andreas LOIBL          l.756   « LOIBL Andreas, 2014, "Namecoin" »
    Gerard DREAN           l.414   « DREAN Gerard, 2013, "Au-dela de Bitcoin (5)" »
    Jacques FAVIER         l.472   « FAVIER Jacques, 2021 »
    Laura DENARDIS         l.394   (nom deja correct, retypage seul)
    SHINOBI                l.1128  (pseudonyme, nom deja correct)

ECRIRE UN NOM DE PERSONNE EST UNE DECISION D'AUTEUR, ET ELLE A ETE PRISE.
La charte reserve a Maël Rolland tout ce qui engrave une affirmation sur une
personne ; le depot en porte le precedent (« Florence Dufy », nom soude de
deux co-auteurs reels, qu'un patch a failli graver). Les six operations ont
ete arbitrees explicitement le 2026-08-09, questions 1 et 2. Ce script ne
decide rien : il execute un lot fige, et refuse tout ce qui s'en ecarte.

LE LOT EST FIGE ICI, VALEURS COMPRISES. Pas seulement les identifiants : le
nom actuel, les types actuels, le nom cible et les types cibles sont tous
reproduits dans LOT_APPROUVE. Un patch retouche entre l'arbitrage et
l'application ne peut donc pas faire ecrire autre chose — c'est la lecon de
la revue de v112, ou figer les seuls ids laissait reecrire la valeur cible.

LE CONTROLE D'APRES EST EXHAUSTIF, sans liste de champs ecrite a la main :
le resultat est compare a la source champ de tete par champ de tete, attribut
par attribut, relation par relation. Le script n'ecrit que si le diff complet
vaut EXACTEMENT les 6 changements de `types` et les 4 changements de `name`
attendus.

Usage:
    python3 scripts/make_v113_apply_bibliography_retypes.py --dry-run
    python3 scripts/make_v113_apply_bibliography_retypes.py
"""
import argparse
import copy
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from grc20_commun import REPO  # noqa: E402

CODE_DONNEES, CODE_INVOCATION = 1, 2

POLICY_CANDIDAT = 'CANDIDATE — NOT APPLIED — AUTHOR ARBITRATION REQUIRED'
VERSION_SOURCE = 'v112'
VERSION_CIBLE = 'v113'
OPS_ATTENDUES = 10
PLAFOND_NOTE = 1200

TYPE_REFERENCE = '51f53c59535b4e22b1dd0d83f6593fe1'
TYPE_PERSON = 'ed738791205548e4b4c187c58be227dc'

# Le lot approuve par l'auteur le 2026-08-09, reproduit EN ENTIER : etat
# attendu dans v112 et etat cible. `nom_cible` a None = retypage pur, la
# fiche porte deja le bon nom et le script REFUSERA de la renommer.
LOT_APPROUVE = {
    '53525938440543a5af359337eeab9823': {
        'nom_actuel': 'Jérôme Favier', 'nom_cible': 'Jacques Favier',
        'types_actuels': [TYPE_REFERENCE], 'types_cibles': [TYPE_PERSON],
    },
    '5fc4278b78704f6c92c3744e2654518a': {
        'nom_actuel': 'Laura DeNardis', 'nom_cible': None,
        'types_actuels': [TYPE_REFERENCE], 'types_cibles': [TYPE_PERSON],
    },
    '7cd4cfe4c8d74aaaaeabcd17ebf11b3a': {
        'nom_actuel': 'Guillaume Dréan', 'nom_cible': 'Gérard Dréan',
        'types_actuels': [TYPE_REFERENCE], 'types_cibles': [TYPE_PERSON],
    },
    'b332ace807b84fe4ab2373b8dc8f4856': {
        'nom_actuel': 'Shinobi (pseudonyme)', 'nom_cible': None,
        'types_actuels': [TYPE_REFERENCE], 'types_cibles': [TYPE_PERSON],
    },
    'be8ac28672e44ef6852fd5b1d80f3b90': {
        'nom_actuel': 'Gregor Loibl', 'nom_cible': 'Andreas Loibl',
        'types_actuels': [TYPE_REFERENCE], 'types_cibles': [TYPE_PERSON],
    },
    'ec901513fae144a0a350e798b0351c6d': {
        'nom_actuel': 'Audrey Takkal Bataille', 'nom_cible': 'Adli Takkal Bataille',
        'types_actuels': [TYPE_REFERENCE], 'types_cibles': [TYPE_PERSON],
    },
}
IDS_ATTENDUS = frozenset(LOT_APPROUVE)


def echec(msg, code=CODE_DONNEES):
    famille = 'invocation' if code == CODE_INVOCATION else 'donnees'
    print(f"ECHEC ({famille}) : {msg}", file=sys.stderr)
    sys.exit(code)


def lire(chemin, quoi):
    if not os.path.exists(chemin):
        echec(f"{quoi} introuvable : {chemin}", CODE_INVOCATION)
    try:
        with open(chemin, encoding='utf-8') as f:
            return json.load(f)
    except (json.JSONDecodeError, OSError) as err:
        echec(f"{quoi} illisible : {err}", CODE_INVOCATION)


def valider_patch(patch):
    """-> plan {entity_id: {'nom': str|None, 'types': list|None}}."""
    meta = patch.get('_meta')
    if not isinstance(meta, dict):
        echec('patch sans `_meta` exploitable')
    if not str(meta.get('policy', '')).startswith(POLICY_CANDIDAT):
        echec('le patch ne porte pas la politique CANDIDATE attendue')

    ops = patch.get('ops')
    if not isinstance(ops, list):
        echec('patch sans liste `ops`')
    if len(ops) != OPS_ATTENDUES:
        echec(f'{len(ops)} op(s) dans le patch, {OPS_ATTENDUES} attendues — '
              'le lot est fige dans l applicateur ; un patch elargi depuis '
              'l arbitrage doit etre re-arbitre, pas applique')

    plan, vus = {}, set()
    for i, op in enumerate(ops):
        if not isinstance(op, dict):
            echec(f'op #{i} n est pas un objet')
        t = op.get('type')
        if t not in ('SET_TYPES', 'SET_NAME'):
            echec(f'op #{i} de type {t!r} : ce lot n ecrit que des SET_TYPES '
                  'et des SET_NAME. Aucun attribut, aucune relation, aucune '
                  'creation, aucune fusion')
        eid = op.get('entityId')
        if eid not in IDS_ATTENDUS:
            echec(f'op #{i} vise l entite {eid!r}, hors du lot fige')
        if (eid, t) in vus:
            echec(f'op #{i} : {t} vise deux fois {eid} — en derniere ecriture '
                  'gagnante, une op serait silencieusement ecrasee')
        vus.add((eid, t))
        approuve = LOT_APPROUVE[eid]
        entree = plan.setdefault(eid, {'nom': None, 'types': None})

        if t == 'SET_NAME':
            if approuve['nom_cible'] is None:
                echec(f'op #{i} renomme {eid}, mais le lot approuve ne prevoit '
                      'AUCUN renommage pour cette fiche : son nom est deja '
                      'juste. Renommer une personne hors arbitrage est '
                      'exactement ce que ce script existe pour empecher')
            valeur = op.get('value') if isinstance(op.get('value'), str) \
                else op.get('name')
            if valeur != approuve['nom_cible']:
                echec(f'op #{i} : nom cible {valeur!r}, le lot approuve declare '
                      f'{approuve["nom_cible"]!r} — ce nom designe une personne '
                      'reelle, il ne se decide pas dans un fichier de patch')
            entree['nom'] = valeur
        else:
            vises = op.get('types') or op.get('value')
            if isinstance(vises, str):
                vises = [vises]
            if list(vises or []) != approuve['types_cibles']:
                echec(f'op #{i} : types cibles {vises!r}, le lot approuve '
                      f'declare {approuve["types_cibles"]!r}')
            entree['types'] = list(vises)

    if set(plan) != IDS_ATTENDUS:
        echec(f'le lot couvre {sorted(plan)}, attendu {sorted(IDS_ATTENDUS)}')
    for eid, approuve in LOT_APPROUVE.items():
        if plan[eid]['types'] is None:
            echec(f'{eid} : aucun SET_TYPES — les 6 retypages sont le coeur du '
                  'lot, aucun ne peut manquer')
        if approuve['nom_cible'] is not None and plan[eid]['nom'] is None:
            echec(f'{eid} : renommage approuve mais absent du patch')
    return plan


def signature(graphe):
    """Etat compare avant/apres. Aucun champ de tete n est enumere en dur."""
    entites = {}
    for e in graphe.get('entities', []):
        attrs = e.get('attributes') or {}
        entites[e['id']] = {
            'champs': {k: json.dumps(v, sort_keys=True, ensure_ascii=False)
                       for k, v in e.items() if k not in ('id', 'attributes')},
            'attributs': {k: json.dumps(v, sort_keys=True, ensure_ascii=False)
                          for k, v in attrs.items()},
        }
    return {
        'entites': entites,
        'relations': json.dumps(graphe.get('relations'), sort_keys=True,
                                ensure_ascii=False),
        'types': json.dumps(graphe.get('types'), sort_keys=True,
                            ensure_ascii=False),
        'relation_types': json.dumps(graphe.get('relation_types'),
                                     sort_keys=True, ensure_ascii=False),
        'ops': json.dumps(graphe.get('ops'), sort_keys=True, ensure_ascii=False),
    }


def diff_exhaustif(avant, apres):
    changements = []
    for bloc in ('relations', 'types', 'relation_types', 'ops'):
        if avant[bloc] != apres[bloc]:
            changements.append(f'bloc `{bloc}` modifie')
    ids_a, ids_b = set(avant['entites']), set(apres['entites'])
    for eid in sorted(ids_a - ids_b):
        changements.append(f'entite supprimee : {eid}')
    for eid in sorted(ids_b - ids_a):
        changements.append(f'entite creee : {eid}')
    for eid in sorted(ids_a & ids_b):
        a, b = avant['entites'][eid], apres['entites'][eid]
        ca, cb = set(a['champs']), set(b['champs'])
        for c in sorted(ca - cb):
            changements.append(f'{eid} : champ de tete `{c}` SUPPRIME')
        for c in sorted(cb - ca):
            changements.append(f'{eid} : champ de tete `{c}` CREE')
        for c in sorted(ca & cb):
            if a['champs'][c] != b['champs'][c]:
                changements.append(f'{eid} : `{c}` modifie')
        aa, ab = set(a['attributs']), set(b['attributs'])
        for k in sorted(aa - ab):
            changements.append(f'{eid} : attribut `{k}` SUPPRIME')
        for k in sorted(ab - aa):
            changements.append(f'{eid} : attribut `{k}` CREE')
        for k in sorted(aa & ab):
            if a['attributs'][k] != b['attributs'][k]:
                changements.append(f'{eid} : attribut `{k}` modifie')
    return changements


def main():
    ap = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--source', default=os.path.join(
        REPO, f'grc20-these-mael-rolland-{VERSION_SOURCE}.json'))
    ap.add_argument('--target', default=os.path.join(
        REPO, f'grc20-these-mael-rolland-{VERSION_CIBLE}.json'))
    ap.add_argument('--patch', default=os.path.join(
        REPO, 'patch_candidate_bibliographie_retypes_v1.json'))
    ap.add_argument('--dry-run', action='store_true')
    args = ap.parse_args()

    patch = lire(args.patch, 'patch candidat')
    graphe = lire(args.source, 'graphe source')
    if (graphe.get('space') or {}).get('version') != VERSION_SOURCE:
        echec(f"le graphe source declare space.version = "
              f"{(graphe.get('space') or {}).get('version')!r} ; cet "
              f"applicateur lit {VERSION_SOURCE}", CODE_INVOCATION)

    plan = valider_patch(patch)
    par_id = {e['id']: e for e in graphe.get('entities', [])}
    noms_pris = {}
    for e in graphe['entities']:
        noms_pris.setdefault(e.get('name'), []).append(e['id'])

    print(f'lot fige : {OPS_ATTENDUES} op(s) sur {len(LOT_APPROUVE)} fiches\n')
    for eid in sorted(plan):
        approuve = LOT_APPROUVE[eid]
        e = par_id.get(eid)
        if e is None:
            echec(f'entite {eid} absente du graphe source')
        if e.get('name') != approuve['nom_actuel']:
            echec(f"{eid} : nom {e.get('name')!r} dans le graphe, le lot "
                  f"attendait {approuve['nom_actuel']!r} — le graphe a derive "
                  'depuis l arbitrage, re-arbitrage requis')
        if list(e.get('types') or []) != approuve['types_actuels']:
            echec(f"{eid} : types {e.get('types')!r}, le lot attendait "
                  f"{approuve['types_actuels']!r}")
        cible_nom = plan[eid]['nom']
        if cible_nom is not None:
            # Un renommage ne doit pas creer d homonyme : le depot a deja vu
            # un resolveur recreer en double une fiche renommee.
            collision = [x for x in noms_pris.get(cible_nom, []) if x != eid]
            if collision:
                echec(f'{eid} : le nom {cible_nom!r} est deja porte par '
                      f'{collision} — renommer creerait un homonyme')
        print(f'  {eid[:8]}  {approuve["nom_actuel"]!r}')
        print('      types  Reference -> Person')
        if cible_nom:
            print(f'      nom    -> {cible_nom!r}')

    if os.path.realpath(args.target) == os.path.realpath(args.source):
        echec('la cible est le graphe SOURCE', CODE_INVOCATION)
    m_v = re.search(r'-(v\d+)\.json$', os.path.basename(args.target))
    if not m_v:
        echec('nom de sortie sans numero de version', CODE_INVOCATION)
    if m_v.group(1) != VERSION_CIBLE:
        echec(f'cible en {m_v.group(1)} : cet applicateur produit '
              f'{VERSION_CIBLE} et rien d autre', CODE_INVOCATION)

    avant = signature(graphe)
    resultat = copy.deepcopy(graphe)
    par_id_res = {e['id']: e for e in resultat['entities']}
    for eid, geste in plan.items():
        if geste['nom'] is not None:
            par_id_res[eid]['name'] = geste['nom']
        par_id_res[eid]['types'] = list(geste['types'])

    apres = signature(resultat)
    changements = diff_exhaustif(avant, apres)
    attendus = set()
    for eid, geste in plan.items():
        attendus.add(f'{eid} : `types` modifie')
        if geste['nom'] is not None:
            attendus.add(f'{eid} : `name` modifie')
    inattendus = [c for c in changements if c not in attendus]

    print(f'\ndiff exhaustif : {len(changements)} changement(s)')
    for c in changements:
        print(f'  {c}')
    if inattendus:
        echec("changement(s) hors lot detecte(s), rien n est ecrit :\n  "
              + '\n  '.join(inattendus))
    if len(changements) != len(attendus):
        echec(f'{len(changements)} changement(s) constate(s), '
              f'{len(attendus)} attendus')

    if args.dry_run:
        print('\n--dry-run : tous les controles ont tourne, y compris le diff '
              "exhaustif. Rien n a ete ecrit.")
        return 0

    espace = resultat.setdefault('space', {})
    espace['version'] = VERSION_CIBLE
    espace['entity_count'] = len(resultat['entities'])
    espace['relation_count'] = len(resultat['relations'])
    tete = (
        "V113 — 6 fiches d auteur retypees Reference -> Person, dont 4 dont le "
        "PRENOM etait faux : Audrey -> Adli Takkal Bataille, Gregor -> Andreas "
        "Loibl, Guillaume -> Gerard Drean, Jerome -> Jacques Favier. Les 4 "
        "prenoms sont attestes dans assets/MD/07_bibliographie.md. Reliquat du "
        "lot patch_18, applique apres arbitrage de l auteur du 2026-08-09. "
        "Aucune fusion, aucun noeud, aucune relation, aucun attribut, aucune "
        "SourceQuote. Doublons et creations bibliographiques restent hors "
        "perimetre. Voir docs/audits/grc20-v113-bibliography-retypes-application.md. ")
    heritee = espace.get('note', '')
    budget = max(0, PLAFOND_NOTE - len(tete))
    if len(heritee) > budget:
        marque = ' […]'
        utile = max(0, budget - len(marque))
        tronquee = heritee[:utile]
        if ' ' in tronquee:
            tronquee = tronquee.rsplit(' ', 1)[0]
        heritee = tronquee + marque
    espace['note'] = tete + heritee
    if len(espace['note']) > PLAFOND_NOTE:
        echec(f"space.note fait {len(espace['note'])} caracteres pour un "
              f'plafond de {PLAFOND_NOTE}')

    temporaire = args.target + '.tmp'
    try:
        with open(temporaire, 'w', encoding='utf-8') as f:
            json.dump(resultat, f, ensure_ascii=False, indent=2)
        os.replace(temporaire, args.target)
    except OSError as err:
        if os.path.exists(temporaire):
            os.unlink(temporaire)
        echec(f'ecriture impossible : {err}')
    print(f'\ngraphe ecrit : {os.path.relpath(args.target, REPO)}')
    return 0


if __name__ == '__main__':
    sys.exit(main())
