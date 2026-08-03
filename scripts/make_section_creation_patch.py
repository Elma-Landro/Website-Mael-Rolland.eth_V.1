#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Emet patch_14_section_creation.json. N'ecrit aucun graphe.

Cree les `ThesisSection` canoniques que le graphe n'a jamais eues. Elles se
reperent a ce qu'aucun noeud ne les porte APRES la renumerotation de
patch_13 — et a ce que le sommaire de `graphe.html` les annonce deja, page
comprise. Sans elles, la renumerotation troque une erreur silencieuse (une
entree du sommaire qui surligne le mauvais noeud) contre un trou visible
(une entree qui n'en surligne aucun).

Ce que porte un noeud cree : ce qui se derive du texte, rien d'autre. Titre
francais et anglais depuis les markdown, page depuis le sommaire, position
dans l'arborescence. Aucun `summary`, aucun `central_argument` : les
resumer serait ecrire a la place de l'auteur.

Les nouveaux noeuds ne recoivent **aucune relation de contenu** : le
contenu de ces sections n'est pas represente dans le graphe, et le
rattacher demande des preuves, pas une generation. C'est un constat
d'audit, pas un manque a combler ici.

Ils recoivent en revanche leur **place dans l'arborescence**, qui n'est pas
une interpretation : le graphe emploie deja un motif reciproque
`section of` / `has section`, chaque sous-section pointant sa section
parente ET son chapitre. On le reproduit a l'identique.

Corollaire que la creation des parents rend visible : les sous-sections de
second rang (`I.1.1.a`, `I.1.1.b`, `I.2.2.b`) pointaient `section of` vers
`I.1` / `I.2` — leur grand-parent — parce que leur vraie parente n'existait
pas. Elles deviendraient soeurs du noeud dont elles sont filles. Le patch
les rebranche sur leur parente immediate. C'est la seule chose qu'il
modifie d'existant, et elle decoule directement de la creation.

Usage:
    python3 scripts/make_section_creation_patch.py --chapitre chap1
"""
import argparse
import collections
import hashlib
import json
import os
import re
import sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from derive_section_tree import FICHIERS  # noqa: E402
from make_section_migration_patch import arbre_md, chapitre_de, nettoie_titre  # noqa: E402
from grc20_commun import est_section  # noqa: E402
from plan_section_migration import graphe_le_plus_recent  # noqa: E402

# Meme convention que patch_11 : md5(sel + '|' + '|'.join(parts)), 32 hex
# minuscules. Rejouer la generation redonne les memes identifiants.
SEL = 'grc20-section-migration-v1'

TYPE_THESIS_SECTION = '4674ab9a271a425b9d5ba06504d32b9c'

NOM_CHAPITRE = {'chap1': 'Chapitre I', 'chap2': 'Chapitre II',
                'chap3': 'Chapitre III', 'intro': 'Introduction',
                'conclu': 'Conclusion'}


def identifiant(*parts):
    return hashlib.md5((SEL + '|' + '|'.join(parts)).encode('utf-8')).hexdigest()


def pages_du_sommaire(chemin_html):
    """-> {section_key: page} lu dans le sommaire de graphe.html.

    Le sommaire est la seule source de pagination du depot pour ces
    sections ; il porte deja l'arborescence canonique.
    """
    out = {}
    with open(chemin_html, encoding='utf-8') as f:
        for ligne in f:
            m = re.search(r'data-section-key="([^"]+)"', ligne)
            if not m:
                continue
            p = re.search(r'class="toc-page">p\.\s*(\d+)', ligne)
            if p:
                out[m.group(1)] = int(p.group(1))
    return out


def cles_occupees_apres(graphe, patch_migration):
    """Les section_key tenues une fois patch_13 applique."""
    with open(graphe, encoding='utf-8') as f:
        g = json.load(f)
    nom_type = {t['id']: t.get('name') for t in g['types']}
    entites = {e['id']: e for e in g['entities']}
    occ = {}
    for e in g['entities']:
        # Les deux types de section, pas seulement `ThesisSection` : sans cela
        # III.3 (unique `ChapterSection`) passe pour absente et se fait
        # recreer en double.
        if not est_section(e, nom_type):
            continue
        k = ((e.get('attributes') or {}).get('section_key') or {}).get('value', '')
        if k:
            occ[k] = e['id']
    if not os.path.exists(patch_migration):
        return occ, g
    with open(patch_migration, encoding='utf-8') as f:
        p = json.load(f)
    deplaces = [o for o in p.get('ops', [])
                if o['type'] == 'SET_ATTRIBUTE' and o['attributeId'] == 'section_key']

    # Un patch qui vise une entite absente du graphe signale une derive entre
    # les deux — patch regenere contre une version, applique contre une autre.
    # Echouer nommement vaut mieux qu'un KeyError nu, et bien mieux que de
    # sauter l'operation en silence : la cle qu'elle devait liberer resterait
    # occupee, et le calcul des sections manquantes serait faux sans le dire.
    inconnues = [o['entityId'] for o in deplaces if o['entityId'] not in entites]
    if inconnues:
        raise ValueError(
            f"{os.path.basename(patch_migration)} vise {len(inconnues)} entite(s) "
            f"absente(s) de {os.path.basename(graphe)} : {', '.join(inconnues[:5])}"
            f"{'…' if len(inconnues) > 5 else ''}. Le patch et le graphe ont derive.")

    for o in deplaces:
        vieux = ((entites[o['entityId']].get('attributes') or {})
                 .get('section_key') or {}).get('value', '')
        occ.pop(vieux, None)
    for o in deplaces:
        occ[o['value']['value']] = o['entityId']
    return occ, g


def main(argv=None):
    p = argparse.ArgumentParser(description="Creation des sections canoniques manquantes.")
    p.add_argument('--graph', default=None)
    p.add_argument('--migration', default=os.path.join(REPO, 'patch_13_section_migration.json'))
    p.add_argument('--out', default=os.path.join(REPO, 'patch_14_section_creation.json'))
    p.add_argument('--chapitre', default=None,
                   help="Liste de fichiers de la these, separes par des virgules "
                        f"({', '.join(c for c, _ in FICHIERS)}).")
    args = p.parse_args(argv)
    connus = {c for c, _ in FICHIERS}
    perimetre = {c.strip() for c in args.chapitre.split(',')} if args.chapitre else None
    if perimetre and not perimetre <= connus:
        print(f"chapitre(s) inconnu(s) : {sorted(perimetre - connus)}", file=sys.stderr)
        return 2

    # Le graphe de reference est celui que patch_13 declare, PAS le plus
    # recent : une fois v100 produit, le prendre reviendrait a lire le
    # resultat et a ne rien trouver a creer.
    chemin = args.graph
    if not chemin and os.path.exists(args.migration):
        with open(args.migration, encoding='utf-8') as f:
            declare = json.load(f).get('_meta', {}).get('source_graph')
        if declare and os.path.exists(os.path.join(REPO, declare)):
            chemin = os.path.join(REPO, declare)
    chemin = chemin or graphe_le_plus_recent()
    try:
        occ, g = cles_occupees_apres(chemin, args.migration)
    except ValueError as err:
        print(f"ECHEC (donnees) : {err}", file=sys.stderr)
        return 1

    _, _, lignes_fr = arbre_md()
    _, _, lignes_en = arbre_md('_EN')
    en_par_cle = {l['cle']: l for l in lignes_en if l['niveau'] <= 2 and l['cle']}
    pages = pages_du_sommaire(os.path.join(REPO, 'graphe.html'))

    manquantes = []
    for l in lignes_fr:
        if l['niveau'] > 2 or not l['cle']:
            continue
        if perimetre and l['chapitre'] not in perimetre:
            continue
        if l['cle'] in occ:
            continue
        manquantes.append(l)

    nouvelles = []
    for l in manquantes:
        cle = l['cle']
        titre = nettoie_titre(l['titre'])
        eid = identifiant('section', l['chapitre'], cle)
        attrs = {
            'section_key': {'type': 'TEXT', 'value': cle,
                            'options': {'language': 'fr'}},
            # Numerote, comme `name` et comme les `labelFr` deja presents sur
            # les sections a cle numerique (I.4, II.1, III.3...). C'est
            # `labelFr` que `lecteur.html` affiche en tete du panneau : sans
            # le numero, la section creee y perdait son rang.
            'labelFr': {'type': 'TEXT', 'value': f'{cle} {titre}',
                        'options': {'language': 'fr'}},
            'chapter': {'type': 'TEXT', 'value': NOM_CHAPITRE.get(l['chapitre'], ''),
                        'options': {'language': 'fr'}},
            # Le contenu de la section n'est pas rattache : le dire dans la
            # donnee, pas seulement dans un rapport.
            'evidenceStatus': {'type': 'TEXT',
                               'value': 'thesis section — structure only, content not yet anchored',
                               'options': {'language': 'en'}},
        }
        l_en = en_par_cle.get(cle)
        if l_en:
            attrs['labelEn'] = {'type': 'TEXT',
                                'value': f'{cle} {nettoie_titre(l_en["titre"])}',
                                'options': {'language': 'en'}}
        if cle in pages:
            attrs['page_start'] = {'type': 'NUMBER', 'value': str(pages[cle])}

        nouvelles.append({
            'id': eid,
            'name': f'{cle} {titre}',
            'description': {
                'type': 'TEXT',
                'value': (f'Section canonique de la these ({NOM_CHAPITRE.get(l["chapitre"], "")}, '
                          f'titre de niveau 2 a la ligne {l["ligne"]} de '
                          f'{dict(FICHIERS)[l["chapitre"]]}). Son contenu n\'est pas '
                          f'encore rattache au graphe.'),
                'options': {'language': 'fr'},
            },
            'types': [TYPE_THESIS_SECTION],
            'attributes': attrs,
            '_comment': f"absente du graphe ; annoncee par le sommaire de graphe.html",
        })

    # ---------- place dans l'arborescence ----------
    nom_type = {t['id']: t.get('name') for t in g['types']}
    rt_id = {r.get('name'): r['id'] for r in g['relation_types']}
    for nom_rel in ('section of', 'has section'):
        if nom_rel not in rt_id:
            print(f"ECHEC : type de relation « {nom_rel} » absent du graphe")
            return 1

    # occ : cle -> id, etat APRES patch_13, plus les creations de ce patch
    occ_apres = dict(occ)
    occ_apres.update({n['attributes']['section_key']['value']: n['id'] for n in nouvelles})

    # le chapitre auquel rattacher, tel que le graphe le nomme deja
    chapitre_id = {}
    for r in g['relations']:
        if rt_id.get('section of') != r['type']:
            continue
        cible = next((e for e in g['entities'] if e['id'] == r['to']), None)
        if cible and 'Chapter' in [nom_type.get(t, t) for t in (cible.get('types') or [])]:
            src = next((e for e in g['entities'] if e['id'] == r['from']), None)
            k = ((src.get('attributes') or {}).get('section_key') or {}).get('value', '') if src else ''
            if k:
                chapitre_id[chapitre_de(k)] = r['to']

    def rel(depuis, nom_rel, vers):
        return {'id': identifiant('rel', depuis, nom_rel, vers),
                'type': rt_id[nom_rel], 'from': depuis, 'to': vers, 'attributes': []}

    relations = []
    for n in nouvelles:
        cle = n['attributes']['section_key']['value']
        ch = chapitre_de(cle)
        parente = cle.rsplit('.', 1)[0]
        for cible in (occ_apres.get(parente), chapitre_id.get(ch)):
            if cible and cible != n['id']:
                relations.append(rel(n['id'], 'section of', cible))
                relations.append(rel(cible, 'has section', n['id']))

    # ---------- rebranchement des seconds rangs ----------
    # Une cle « I.1.1.a » a pour parente « I.1.1 » ; tant que celle-ci
    # n'existait pas, la relation pointait le grand-parent.
    sections_du_graphe = {e['id']: ((e.get('attributes') or {}).get('section_key') or {}).get('value', '')
                          for e in g['entities']
                          if 'ThesisSection' in [nom_type.get(t, t) for t in (e.get('types') or [])]}
    # apres patch_13 les cles ont bouge : on relit l'etat d'apres
    id_vers_cle = {v: k for k, v in occ_apres.items()}
    rebranchements = []
    for cle, eid in occ_apres.items():
        if cle.count('.') < 2 or not cle[-1].isalpha():
            continue
        parente = cle.rsplit('.', 1)[0]
        pid = occ_apres.get(parente)
        if not pid:
            continue
        for r in g['relations']:
            if r['type'] == rt_id['section of'] and r['from'] == eid \
                    and r['to'] in sections_du_graphe and r['to'] != pid:
                rebranchements.append({
                    'relation_id': r['id'], 'from': eid,
                    'to_avant': r['to'], 'to_apres': pid,
                    '_comment': f"{cle} pointait {id_vers_cle.get(r['to'], r['to'])}, "
                                f"son grand-parent ; sa parente {parente} existe desormais",
                })
            if r['type'] == rt_id['has section'] and r['to'] == eid \
                    and r['from'] in sections_du_graphe and r['from'] != pid:
                rebranchements.append({
                    'relation_id': r['id'], 'to': eid,
                    'from_avant': r['from'], 'from_apres': pid,
                    '_comment': f"reciproque de « {cle} section of {parente} »",
                })

    doublons = [n['id'] for n in nouvelles if n['id'] in {e['id'] for e in g['entities']}]
    compteur = collections.Counter(n['id'] for n in nouvelles)
    collisions = [k for k, v in compteur.items() if v > 1]

    m_id = re.match(r'patch_(\d+)', os.path.basename(args.out))
    if not m_id:
        print(f"ECHEC (invocation) : --out doit se nommer patch_<numero>_... , "
              f"recu {os.path.basename(args.out)}", file=sys.stderr)
        return 2
    patch = {
        '_meta': {
            # Deduit du nom de sortie, comme dans le generateur de migration :
            # le meme script sert plusieurs paliers, et deux patchs ne peuvent
            # pas porter le meme numero. patch_16 a porte « 14 » jusqu'au
            # 03/08/2026, herite de patch_14 par copie.
            'patch_id': m_id.group(1),
            'description': "Creation des ThesisSection canoniques absentes du graphe.",
            'source_graph': os.path.basename(chemin),
            'depends_on': os.path.basename(args.migration),
            'perimetre': args.chapitre or 'toute la these',
            'policy': "Ajout d'entites et de leur place dans l'arborescence. Aucune "
                      "entite existante modifiee, aucune fusion, aucune suppression, "
                      "aucune relation retiree. Seule exception declaree : les "
                      "rebranchements ci-dessous, qui redirigent des relations "
                      "`section of` / `has section` existantes vers la parente "
                      "immediate desormais creee.",
            'id_derivation': f"md5('{SEL}|' + '|'.join(parts)) -> 32 hex minuscules. "
                             "parts = ('section', chapitre, cle_canonique). Deterministe.",
            'contenu': "Titre FR/EN depuis les markdown, page depuis le sommaire de "
                       "graphe.html, position dans l'arborescence. Ni summary ni "
                       "central_argument : les rediger serait ecrire a la place de l'auteur.",
        },
        'new_entities': nouvelles,
        'new_relations': relations,
        'rewire_relations': rebranchements,
    }

    print(f"graphe    : {os.path.basename(chemin)}")
    print(f"perimetre : {args.chapitre or 'toute la these'}")
    print(f"sections canoniques sans noeud apres patch_13 : {len(nouvelles)}")
    for n in nouvelles:
        pg = n['attributes'].get('page_start', {}).get('value', '—')
        print(f"  {n['id']}  p.{pg:>4}  {n['name'][:62]}")
    print(f"relations d'arborescence creees : {len(relations)}")
    print(f"relations rebranchees sur la parente immediate : {len(rebranchements)}")
    for rb in rebranchements:
        print(f"    {rb['_comment'][:88]}")
    if doublons:
        print(f"ECHEC : identifiant deja present dans le graphe : {doublons}")
        return 1
    if collisions:
        print(f"ECHEC : identifiants derives en collision : {collisions}")
        return 1

    with open(args.out, 'w', encoding='utf-8') as f:
        json.dump(patch, f, ensure_ascii=False, indent=1)
    print(f"patch ecrit : {os.path.relpath(args.out, REPO)}")
    return 0


if __name__ == '__main__':
    sys.exit(main())
