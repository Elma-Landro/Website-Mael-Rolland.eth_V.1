#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Applique patch_13 + patch_14 a v99 et produit le graphe candidat v100.

Les deux patchs sont indissociables : patch_13 libere des cles que
patch_14 ne remplit pas, et patch_14 comble des cles que patch_13 laisse
vides. Appliquer l'un sans l'autre laisse le sommaire du site sur des
sections sans noeud. Le script refuse donc de n'en appliquer qu'un.

Il valide avant d'ecrire et echoue bruyamment plutot que de produire un
graphe douteux.

Usage:
    python3 scripts/make_v100_section_migration.py --dry-run
    python3 scripts/make_v100_section_migration.py
"""
import argparse
import collections
import json
import os
import re
import sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from grc20_commun import est_section  # noqa: E402


# Deux familles d'echec, deux codes de sortie. Lire « ECHEC (invocation) »
# dit tout de suite qu'il faut corriger la ligne de commande ou les fichiers
# fournis ; « ECHEC (donnees) » qu'il faut corriger un patch ou le graphe.
# Confondre les deux fait perdre le premier quart d'heure de diagnostic.
CODE_DONNEES = 1
CODE_INVOCATION = 2


def echec(msg, code=CODE_DONNEES):
    famille = 'invocation' if code == CODE_INVOCATION else 'donnees'
    print(f"ECHEC ({famille}) : {msg}", file=sys.stderr)
    sys.exit(code)


def main(argv=None):
    p = argparse.ArgumentParser(
        description="Construit v100 = v99 + patch_13 (renumerotation) + patch_14 (creations).")
    p.add_argument('--source', default=os.path.join(REPO, 'grc20-these-mael-rolland-v99.json'))
    p.add_argument('--migration', default=os.path.join(REPO, 'patch_13_section_migration.json'))
    p.add_argument('--creation', default=os.path.join(REPO, 'patch_14_section_creation.json'))
    p.add_argument('--target', default=os.path.join(REPO, 'grc20-these-mael-rolland-v100.json'))
    p.add_argument('--dry-run', action='store_true')
    args = p.parse_args(argv)

    def lire(chemin, quoi):
        if not os.path.exists(chemin):
            echec(f"{quoi} introuvable : {chemin}", CODE_INVOCATION)
        try:
            with open(chemin, encoding='utf-8') as f:
                return json.load(f)
        except json.JSONDecodeError as err:
            echec(f"{quoi} illisible ({os.path.basename(chemin)}) : {err}",
                  CODE_INVOCATION)
        except OSError as err:
            echec(f"{quoi} inaccessible : {err}", CODE_INVOCATION)

    g = lire(args.source, 'graphe source')
    p13 = lire(args.migration, 'patch de migration')
    p14 = lire(args.creation, 'patch de creation')

    base = os.path.basename(args.source)
    print(f"source : {base} ({len(g['entities'])} entites, {len(g['relations'])} relations)")
    print(f"patch  : {os.path.basename(args.migration)} ({len(p13.get('ops', []))} ops)")
    print(f"patch  : {os.path.basename(args.creation)} "
          f"({len(p14.get('new_entities', []))} entites)")

    for patch, nom in ((p13, args.migration), (p14, args.creation)):
        declare = patch.get('_meta', {}).get('source_graph')
        if declare and declare != base:
            echec(f"{os.path.basename(nom)} declare source_graph={declare}, "
                  f"incompatible avec {base} — verifiez --source, ou regenerez "
                  f"le patch contre ce graphe", CODE_INVOCATION)
    if p13.get('_meta', {}).get('perimetre') != p14.get('_meta', {}).get('perimetre'):
        echec("les deux patchs ne couvrent pas le meme perimetre : "
              f"{p13['_meta'].get('perimetre')} vs {p14['_meta'].get('perimetre')} "
              f"— regenerez-les avec le meme --chapitre", CODE_INVOCATION)

    entites = {e['id']: e for e in g['entities']}
    nom_type = {t['id']: t.get('name') for t in g['types']}
    erreurs = []

    # ---------- validations : patch_13 ----------
    for o in p13.get('ops', []):
        if o['type'] not in ('SET_ATTRIBUTE', 'SET_NAME'):
            erreurs.append(f"operation non supportee : {o['type']}")
            continue
        if o['entityId'] not in entites:
            erreurs.append(f"entite inconnue : {o['entityId']}")
            continue
        e = entites[o['entityId']]
        if not est_section(e, nom_type):
            erreurs.append(f"{o['entityId']} n'est ni ThesisSection ni ChapterSection")
        # Liste blanche : un patch de migration n'a aucune raison d'ecrire
        # ailleurs. `labelFr` en fait partie depuis v106 — c'est lui que
        # `lecteur.html` affiche en tete du panneau, et le laisser derriere
        # faisait diverger le titre affiche du nom du noeud.
        if o['type'] == 'SET_ATTRIBUTE' and o['attributeId'] not in (
                'section_key', 'labelFr', 'labelEn'):
            erreurs.append(f"attribut hors politique : {o['attributeId']}")

    # ---------- validations : patch_14 ----------
    for e in p14.get('new_entities', []):
        if e['id'] in entites:
            erreurs.append(f"identifiant deja present : {e['id']}")
        if not e.get('types') or any(t not in nom_type for t in e['types']):
            erreurs.append(f"type inconnu pour {e['id']}")

    nouveaux_ids = {e['id'] for e in p14.get('new_entities', [])}
    types_rel = {r['id'] for r in g['relation_types']}
    # Toutes les relations ne portent pas d'identifiant : le graphe en compte
    # sans. On indexe celles qui en ont, les seules rebranchables nommement.
    rel_par_id = {r['id']: r for r in g['relations'] if r.get('id')}
    ids_rel = set(rel_par_id)
    for r in p14.get('new_relations', []):
        if r['id'] in ids_rel:
            erreurs.append(f"identifiant de relation deja present : {r['id']}")
        if r['type'] not in types_rel:
            erreurs.append(f"type de relation inconnu : {r['type']}")
        for bout in ('from', 'to'):
            if r[bout] not in entites and r[bout] not in nouveaux_ids:
                erreurs.append(f"relation {r['id']} : {bout} absent ({r[bout]})")

    for rb in p14.get('rewire_relations', []):
        r = rel_par_id.get(rb['relation_id'])
        if not r:
            erreurs.append(f"rebranchement : relation inconnue {rb['relation_id']}")
            continue
        # On verifie que l'etat de depart est bien celui que le patch decrit :
        # rebrancher une relation qui a deja bouge serait ecraser en aveugle.
        if 'to_avant' in rb and r.get('to') != rb['to_avant']:
            erreurs.append(f"rebranchement {rb['relation_id']} : to={r.get('to')}, "
                           f"attendu {rb['to_avant']}")
        if 'from_avant' in rb and r.get('from') != rb['from_avant']:
            erreurs.append(f"rebranchement {rb['relation_id']} : from={r.get('from')}, "
                           f"attendu {rb['from_avant']}")
        for cle in ('to_apres', 'from_apres'):
            if cle in rb and rb[cle] not in entites and rb[cle] not in nouveaux_ids:
                erreurs.append(f"rebranchement {rb['relation_id']} : {cle} absent")

    if erreurs:
        for x in erreurs[:20]:
            print(f"  - {x}")
        echec(f"{len(erreurs)} erreur(s) de validation")

    # ---------- application ----------
    avant_e, avant_r = len(g['entities']), len(g['relations'])
    modifiees = set()
    for o in p13.get('ops', []):
        e = entites[o['entityId']]
        if o['type'] == 'SET_NAME':
            e['name'] = o['value']
        else:
            e.setdefault('attributes', {})[o['attributeId']] = {
                k: v for k, v in o['value'].items()}
        modifiees.add(o['entityId'])

    for nouvelle in p14.get('new_entities', []):
        e = {k: v for k, v in nouvelle.items() if not k.startswith('_')}
        g['entities'].append(e)
        entites[e['id']] = e

    for r in p14.get('new_relations', []):
        g['relations'].append({k: v for k, v in r.items() if not k.startswith('_')})

    for rb in p14.get('rewire_relations', []):
        r = rel_par_id[rb['relation_id']]
        if 'to_apres' in rb:
            r['to'] = rb['to_apres']
        if 'from_apres' in rb:
            r['from'] = rb['from_apres']

    # ---------- verifications d'apres ----------
    cles = collections.Counter()
    for e in g['entities']:
        if not est_section(e, nom_type):
            continue
        k = ((e.get('attributes') or {}).get('section_key') or {}).get('value', '')
        if k:
            cles[k] += 1
    doublons = {k: n for k, n in cles.items() if n > 1}
    if doublons:
        echec(f"section_key en double apres application : {doublons}")

    attendu_r = avant_r + len(p14.get('new_relations', []))
    if len(g['relations']) != attendu_r:
        echec(f"{len(g['relations'])} relations, {attendu_r} attendues")
    attendu = avant_e + len(p14.get('new_entities', []))
    if len(g['entities']) != attendu:
        echec(f"{len(g['entities'])} entites, {attendu} attendues")

    ids = {e['id'] for e in g['entities']}
    casses = [r for r in g['relations'] if r.get('from') not in ids or r.get('to') not in ids]
    avant_casses = 1   # l'orpheline Ostrom, portee et signalee depuis mai 2026
    if len(casses) > avant_casses:
        echec(f"{len(casses)} relations a endpoint absent (attendu {avant_casses})")

    print()
    print(f"entites   : {avant_e} -> {len(g['entities'])} (+{len(g['entities']) - avant_e})")
    print(f"relations : {avant_r} -> {len(g['relations'])} "
          f"(+{len(g['relations']) - avant_r}, {len(p14.get('rewire_relations', []))} rebranchees)")
    print(f"sections modifiees : {len(modifiees)}")

    # Aucun noeud de section ne doit rester sans arete : c'est ce que la CI
    # refuse, et c'est la raison d'etre du cablage d'arborescence.
    relies = set()
    for r in g['relations']:
        relies.add(r.get('from'))
        relies.add(r.get('to'))
    isoles = [e['id'] for e in g['entities'] if e['id'] not in relies]
    if isoles:
        echec(f"{len(isoles)} entite(s) sans aucune relation : {isoles[:5]}")
    print(f"section_key uniques : {len(cles)} — aucun doublon")

    if args.dry_run:
        print("\n--dry-run : rien ecrit.")
        return 0

    # La version se deduit du nom du fichier ecrit. Recopier `space` tel quel
    # est ce qui a laisse v100 a v104 annoncer « v99 » : le graphe mentait sur
    # sa propre version, et la CI le controle desormais.
    espace = g.setdefault('space', {})
    m_v = re.search(r'-(v\d+)\.json$', os.path.basename(args.target))
    if not m_v:
        echec(f"nom de sortie sans numero de version : {os.path.basename(args.target)}",
              CODE_INVOCATION)
    espace['version'] = m_v.group(1)
    espace['entity_count'] = len(g['entities'])
    espace['relation_count'] = len(g['relations'])
    with open(args.target, 'w', encoding='utf-8') as f:
        json.dump(g, f, ensure_ascii=False, indent=2)
    print(f"\ngraphe ecrit : {os.path.relpath(args.target, REPO)}")
    return 0


if __name__ == '__main__':
    sys.exit(main())
