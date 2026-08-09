#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Inventorie TOUS les artefacts de patch du depot et etablit leur statut
face au graphe courant. Lecture seule.

POURQUOI CE SCRIPT EXISTE. Le depot accumule des patchs depuis v72. Certains
sont appliques, d'autres attendent un arbitrage, d'autres encore sont des
archives qu'un rejeu naif casserait. L'inventaire de v110
(`candidate-patch-inventory-v1.csv`) est un instantane qui ne dit plus la
verite : deux patchs ont ete appliques depuis, et rien ne le consigne.

CE QU'IL NE FAIT PAS. Il ne modifie aucun patch, n'en supprime aucun, et
n'applique rien. Il ne decide pas non plus : quand la preuve manque, le
statut est `indetermine` et la colonne `preuve` dit ce qui manque.

COMMENT LE STATUT EST ETABLI. Jamais sur la foi d'une declaration du patch.
Pour chaque op lisible, le script regarde le GRAPHE COURANT et demande : la
cible existe-t-elle, et l'effet est-il deja la ? Un patch dont toutes les ops
sont deja realisees est `already_applied` quel que soit ce que sa `policy`
raconte — c'est precisement le cas des deux patchs candidats appliques par
`make_v111` et `make_v112`, qui gardent leur mention CANDIDATE par convention.

Usage:
    python3 scripts/build_patch_queue_inventory.py            # simulation
    python3 scripts/build_patch_queue_inventory.py --csv      # ecrit le CSV
    python3 scripts/build_patch_queue_inventory.py --check    # CI
"""
import argparse
import csv
import glob
import json
import os
import sys
from collections import Counter

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from grc20_commun import REPO, graphe_le_plus_recent  # noqa: E402

CODE_DONNEES, CODE_INVOCATION = 1, 2
SORTIE = os.path.join(REPO, 'docs', 'audits', 'data',
                      'patch-application-queue-v112.csv')

COLONNES = (
    'chemin', 'famille', 'source_graph_declare', 'cible', 'nb_ops',
    'types_ops', 'ops_lisibles', 'ops_deja_realisees', 'ops_cibles_absentes',
    'statut', 'preuve', 'prochain_geste',
)

# Familles, par prefixe de nom de fichier. Deliberement grossier : la famille
# sert a grouper la lecture, pas a decider.
FAMILLES = (
    ('patch_candidate_bibliographie_retypes', 'bibliographie-retypages'),
    ('patch_candidate_bibliographie_duplicates', 'bibliographie-doublons'),
    ('patch_candidate_bibliographie_missing_nodes', 'bibliographie-creations'),
    ('patch_candidate_chronology_dates', 'chronologie'),
    ('patch_candidate_section_page_start', 'page_start'),
    ('patch_18_bibliography', 'bibliographie-historique'),
    ('patch_19_attribute', 'normalisation-attributs'),
    ('patch_10_dedup', 'doublons-evenements'),
    ('patch_11_add_missing', 'chronologie-historique'),
    ('patch_12_wire', 'chronologie-historique'),
    ('patch_13_section', 'sections'),
    ('patch_14_section', 'sections'),
    ('patch_15_section', 'sections'),
    ('patch_16_section', 'sections'),
    ('patch_17_wire', 'sections'),
    ('patch_2a_sourcequote', 'sourcequote-historique'),
    ('patch_2b_central', 'arguments'),
    ('patch_2c_definitions', 'definitions'),
    ('patch_1a_', 'ancrage-historique'),
    ('patch_1b_', 'ancrage-historique'),
    ('patch_3a_', 'sections-historique'),
    ('patch_4', 'ancrage-historique'),
    ('patch_5', 'ancrage-historique'),
    ('patch_batch', 'ancrage-historique'),
)

# Conteneurs d'operations rencontres dans les six dialectes du depot.
CONTENEURS = ('ops', 'operations', 'relations', 'new_relations',
              'new_entities', 'rewire_relations', 'update_entities')


def echec(msg, code=CODE_DONNEES):
    famille = 'invocation' if code == CODE_INVOCATION else 'donnees'
    print(f"ECHEC ({famille}) : {msg}", file=sys.stderr)
    sys.exit(code)


def famille_de(chemin):
    base = os.path.basename(chemin)
    for prefixe, nom in FAMILLES:
        if base.startswith(prefixe):
            return nom
    if 'anchor_overrides' in base:
        return 'ancrage-archive'
    if 'remove_15_truncated' in base:
        return 'reparation-relations'
    return 'indetermine'


def meta_de(doc):
    m = doc.get('_meta')
    return m if isinstance(m, dict) else doc


def source_declaree(doc):
    m = meta_de(doc)
    for cle in ('source_graph', 'base_graph', 'graph_version', 'graph'):
        v = m.get(cle) or doc.get(cle)
        if isinstance(v, str) and v:
            return v
    return ''


def ops_de(doc):
    """-> (liste d'ops, nom du conteneur). Ne devine pas : si plusieurs
    conteneurs coexistent, on les concatene et on le dit dans `types_ops`."""
    trouvees, noms = [], []
    for c in CONTENEURS:
        v = doc.get(c)
        if isinstance(v, list) and v:
            trouvees.extend(v)
            noms.append(f'{c}[{len(v)}]')
    return trouvees, '+'.join(noms)


OPS_CONNUES = frozenset({
    'SET_ATTRIBUTE', 'DELETE_ATTRIBUTE', 'SET_NAME', 'SET_TYPES',
    'ADD_RELATION', 'REMOVE_RELATION', 'CREATE_ENTITY',
})


def type_op(op, conteneur_relation=False):
    if not isinstance(op, dict):
        return '(non-objet)'
    # PIEGE DU DEPOT : dans les dialectes `relations` / `new_relations`, la cle
    # `type` ne porte PAS un type d'operation mais l'IDENTIFIANT DU TYPE DE
    # RELATION. La lire comme un type d'op rendait ces 8 patchs illisibles
    # (0 op lisible sur 500), donc `indetermine` a tort.
    if {'from', 'to'} <= set(op):
        return 'ADD_RELATION(implicite)'
    for cle in ('type', 'op', 'operation'):
        v = op.get(cle)
        if isinstance(v, str) and v in OPS_CONNUES:
            return v
    for cle in ('type', 'op', 'operation'):
        v = op.get(cle)
        if isinstance(v, str):
            return v
    # Les dialectes `relations` / `new_relations` n'ont pas de champ de type :
    # l'operation EST un ajout de relation.
    if conteneur_relation or {'from', 'to'} <= set(op):
        return 'ADD_RELATION(implicite)'
    if 'id' in op and 'name' in op:
        return 'CREATE_ENTITY(implicite)'
    return '(sans type)'


def effet_realise(op, par_id, types_par_nom, relations=None):
    """-> True / False / None (indecidable). Regarde le GRAPHE, pas le patch."""
    if not isinstance(op, dict):
        return None
    t = type_op(op)

    # Dialectes HISTORIQUES, sans champ de type. Ils sont majoritaires dans le
    # depot (patch_1a a patch_batch3) et les ignorer laissait 20 artefacts sur
    # 30 en `indetermine` — un inventaire qui ne sait rien n'aide personne.
    if t == 'ADD_RELATION(implicite)' and relations is not None:
        src = op.get('from') or op.get('from_entity') or op.get('from_entity_id')
        dst = op.get('to') or op.get('to_entity') or op.get('to_entity_id')
        typ = op.get('type') or op.get('relation_type')
        if not (src and dst):
            return None
        # Le type peut etre un identifiant OU un nom de relation ; on accepte
        # les deux, et on se rabat sur (source, cible) quand il est absent.
        cles = {(src, dst, typ), (src, dst, types_par_nom.get(typ))}
        if any(c in relations for c in cles):
            return True
        return (src, dst) in {(a, b) for a, b, _ in relations} if typ is None \
            else False
    if t == 'CREATE_ENTITY(implicite)':
        return op.get('id') in par_id
    if t == 'ADD_RELATION' and relations is not None:
        src = op.get('from_entity_id') or op.get('from')
        dst = op.get('to_entity_id') or op.get('to')
        if not (src and dst):
            return None
        return (src, dst) in {(a, b) for a, b, _ in relations}
    if t == 'REMOVE_RELATION' and relations is not None:
        src = op.get('from_entity_id') or op.get('from')
        dst = op.get('to_entity_id') or op.get('to')
        if not (src and dst):
            return None
        return (src, dst) not in {(a, b) for a, b, _ in relations}
    eid = op.get('entityId') or op.get('entity_id') or op.get('id')
    if t == 'SET_ATTRIBUTE':
        e = par_id.get(eid)
        if e is None:
            return None
        cle = op.get('attributeId') or op.get('attribute_name')
        val = op.get('value')
        attendu = val.get('value') if isinstance(val, dict) else val
        actuel = (e.get('attributes') or {}).get(cle)
        actuel = actuel.get('value') if isinstance(actuel, dict) else actuel
        return actuel == attendu
    if t == 'DELETE_ATTRIBUTE':
        e = par_id.get(eid)
        if e is None:
            return None
        cle = op.get('attributeId') or op.get('attribute_name')
        return cle not in (e.get('attributes') or {})
    if t == 'SET_NAME':
        e = par_id.get(eid)
        if e is None:
            return None
        return e.get('name') == (op.get('value') or op.get('name'))
    if t == 'SET_TYPES':
        e = par_id.get(eid)
        if e is None:
            return None
        vises = op.get('types') or op.get('value') or []
        if isinstance(vises, str):
            vises = [vises]
        return set(e.get('types') or []) == set(vises)
    return None


def statut_de(chemin, doc, ops, par_id, types_par_nom, courant, relations):
    """-> (statut, preuve, geste, compteurs). Le statut vient du graphe."""
    lisibles = deja = absentes = 0
    for op in ops:
        e = effet_realise(op, par_id, types_par_nom, relations)
        if e is None:
            eid = (op.get('entityId') or op.get('entity_id') or op.get('id')
                   if isinstance(op, dict) else None)
            if eid is not None and eid not in par_id:
                absentes += 1
            continue
        lisibles += 1
        if e:
            deja += 1

    src = source_declaree(doc)
    base = os.path.basename(chemin)
    politique = str(meta_de(doc).get('policy', ''))
    candidat = 'CANDIDATE' in politique

    cree = sum(1 for op in ops
               if isinstance(op, dict)
               and type_op(op) in ('CREATE_ENTITY', 'CREATE_ENTITY(implicite)'))
    if cree and cree == len(ops) and deja == 0:
        return ('blocked_by_missing_applicator',
                f"{cree} op(s) CREATE_ENTITY et rien d'autre : AUCUN "
                "applicateur du depot ne consomme ce type d'op, et le contrat "
                "des patchs candidats interdit de pre-assigner un `entityId`",
                'ecrire un applicateur ET arbitrer la politique de creation',
                (lisibles, deja, absentes))

    if lisibles == 0:
        return ('indetermine',
                f"aucune op lisible par ce script ({len(ops)} op(s), dialecte "
                "sans type explicite ou sans cible resoluble) — statut NON "
                "etabli, a instruire a la main",
                'lecture manuelle avant toute reprise',
                (lisibles, deja, absentes))

    if deja == lisibles:
        preuve = (f"{deja}/{lisibles} op(s) lisibles ont deja leur effet dans "
                  f"{courant}")
        if candidat:
            return ('already_applied',
                    preuve + " — le patch garde sa mention CANDIDATE par "
                    "convention du depot (C03 du preflight l'exige), ce qui "
                    "ne dit PAS qu'il est en attente",
                    'documenter comme applique ; ne pas rejouer',
                    (lisibles, deja, absentes))
        return ('already_applied', preuve, 'ne pas rejouer',
                (lisibles, deja, absentes))

    if deja == 0 and absentes > 0 and absentes >= len(ops) / 2:
        return ('dangerous_do_not_apply',
                f"{absentes} cible(s) absente(s) du graphe courant sur "
                f"{len(ops)} op(s) : un rejeu naif echouerait ou ecrirait a "
                "cote",
                'archive — ne pas rejouer',
                (lisibles, deja, absentes))

    if deja == 0:
        if src and src != os.path.basename(courant):
            return ('stale_source_graph_but_preconditions_intact',
                    f"aucune op realisee ; source declaree {src} != courant "
                    f"{os.path.basename(courant)} ; les {lisibles} cible(s) "
                    "lisibles existent et portent encore leur valeur d'origine",
                    'verifier les preconditions puis arbitrer',
                    (lisibles, deja, absentes))
        return ('still_candidate',
                f"aucune des {lisibles} op(s) lisibles n'est realisee dans "
                f"{os.path.basename(courant)}",
                'arbitrage auteur requis',
                (lisibles, deja, absentes))

    return ('indetermine',
            f"{deja}/{lisibles} op(s) realisees : etat MIXTE, ni applique ni "
            "intact — le patch a pu etre partiellement absorbe",
            'instruire op par op avant toute reprise',
            (lisibles, deja, absentes))


def construire(courant):
    g = json.load(open(courant, encoding='utf-8'))
    par_id = {e['id']: e for e in g['entities']}
    types_par_nom = {t['name']: t['id'] for t in g['types']}
    types_par_nom.update({t['name']: t['id'] for t in g['relation_types']})
    relations = {(r['from'], r['to'], r['type']) for r in g['relations']}

    chemins = sorted(glob.glob(os.path.join(REPO, 'patch*.json')))
    chemins += sorted(glob.glob(os.path.join(REPO, 'patches', '**', '*.json'),
                                recursive=True))
    lignes = []
    for chemin in chemins:
        rel = os.path.relpath(chemin, REPO)
        try:
            doc = json.load(open(chemin, encoding='utf-8'))
        except (json.JSONDecodeError, OSError) as err:
            lignes.append({
                'chemin': rel, 'famille': famille_de(rel),
                'source_graph_declare': '', 'cible': '', 'nb_ops': 0,
                'types_ops': '', 'ops_lisibles': 0, 'ops_deja_realisees': 0,
                'ops_cibles_absentes': 0, 'statut': 'indetermine',
                'preuve': f'illisible : {err}',
                'prochain_geste': 'reparer ou archiver',
            })
            continue
        if not isinstance(doc, dict):
            doc = {'ops': doc}
        ops, conteneurs = ops_de(doc)
        compte = Counter(type_op(op) for op in ops)
        statut, preuve, geste, (lis, deja, abs_) = statut_de(
            rel, doc, ops, par_id, types_par_nom, courant, relations)
        m = meta_de(doc)
        lignes.append({
            'chemin': rel,
            'famille': famille_de(rel),
            'source_graph_declare': source_declaree(doc),
            'cible': str(m.get('target_graph') or ''),
            'nb_ops': len(ops),
            'types_ops': ' | '.join(f'{k}={v}' for k, v in sorted(compte.items())),
            'ops_lisibles': lis,
            'ops_deja_realisees': deja,
            'ops_cibles_absentes': abs_,
            'statut': statut,
            'preuve': preuve + (f' [conteneurs {conteneurs}]' if conteneurs else ''),
            'prochain_geste': geste,
        })
    lignes.sort(key=lambda x: x['chemin'])
    return lignes


def main():
    ap = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--graph', default=None)
    ap.add_argument('--csv', action='store_true')
    ap.add_argument('--check', action='store_true')
    args = ap.parse_args()
    if args.csv and args.check:
        ap.error('--csv et --check sont exclusifs : --check ne repare pas ce '
                 "qu'il controle.")

    courant = args.graph or graphe_le_plus_recent(REPO)
    if not courant:
        echec('aucun graphe numerote dans le depot', CODE_INVOCATION)
    lignes = construire(courant)

    print(f'graphe de reference : {os.path.basename(courant)}')
    print(f'{len(lignes)} artefact(s) inventorie(s)\n')
    for statut, n in sorted(Counter(l['statut'] for l in lignes).items()):
        print(f'  {n:3d}  {statut}')

    if args.check:
        if not os.path.exists(SORTIE):
            print(f'--check : {os.path.relpath(SORTIE, REPO)} absent.',
                  file=sys.stderr)
            return 1
        with open(SORTIE, encoding='utf-8', newline='') as f:
            verse = list(csv.DictReader(f, delimiter=';'))
        recalcule = [{k: str(v) for k, v in l.items()} for l in lignes]
        if verse != recalcule:
            print('--check : le CSV verse differe du CSV recalcule.',
                  file=sys.stderr)
            return 1
        print('\n--check : l inventaire verse est a jour.')
        return 0

    if not args.csv:
        print('\n(simulation — relancer avec --csv pour ecrire)')
        return 0

    temporaire = SORTIE + '.tmp'
    with open(temporaire, 'w', encoding='utf-8', newline='') as f:
        w = csv.DictWriter(f, fieldnames=COLONNES, delimiter=';')
        w.writeheader()
        w.writerows(lignes)
    os.replace(temporaire, SORTIE)
    print(f'\necrit : {os.path.relpath(SORTIE, REPO)} ({len(lignes)} lignes)')
    return 0


if __name__ == '__main__':
    sys.exit(main())
