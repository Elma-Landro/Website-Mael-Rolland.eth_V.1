#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Emet patch_13_section_migration.json. N'ecrit aucun graphe.

Applique les arbitrages rendus :
  - niveau canonique `##`, celui que la these emploie pour se numeroter ;
  - les titres de niveau 3 passent en second rang subordonne (I.1.1.a...) ;
  - les libelles du graphe sont realignes sur ceux de la these — le graphe
    porte des formulations anterieures (« cryptomonnaies » la ou le texte
    ecrit « CM », « Le travail de traduction » la ou il ecrit « Un effort
    de traduction attentif aux et a l'attention des acteurs »).

Le patch ne touche que `section_key` et `name`. Il ne cree, ne fusionne ni
ne supprime aucune entite : les sections manquantes et les 5 noeuds vides
relevent d'un second temps.

Un noeud SANS `section_key` n'est pas traite non plus. Lui en donner une ne
serait pas une migration mais une affectation — acte different, et ici
franchement nuisible : le noeud vide « I.2.1b Un protocole Bitcoin qui
s'adapte » vise le meme titre de la these (l.321) que le noeud I.2.2, qui
porte 177 entites. Le doter d'une cle creerait le doublon que la migration
est censee lever.

Usage:
    python3 scripts/make_section_migration_patch.py
    python3 scripts/make_section_migration_patch.py --chapitre chap1
    python3 scripts/make_section_migration_patch.py --out /tmp/patch.json
"""
import argparse
import collections
import csv
import json
import os
import re
import sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from derive_section_tree import FICHIERS, MD, numerote, titres  # noqa: E402
from plan_section_migration import graphe_le_plus_recent, sans_numero  # noqa: E402

# Arbitrages rendus, cas par cas. Ecrits ici parce qu'aucun appariement
# automatique ne pouvait les trancher : les libelles divergent en formulation,
# pas en numerotation.
GROUPE_A = {            # meme section, libelle reformule -> cle conservee
    'intro_A', 'intro_E', 'conclu_boucs', 'conclu_theo_mon',
    'conclu_traduction', 'I.3.2', 'I.3.3',
}
GROUPE_B = {'I.4', 'II.4', 'III.4'}      # conclusions de chapitre
# En realite de niveau 3. La valeur est la LIGNE du `###` vise dans le
# markdown, quand l'appariement automatique ne suffit pas — et il ne suffit
# pas ici : le graphe ecrit « qui s'adapte : regulations », la these « qui
# s'adapte : DES regulations ». Un mot insere au 34e caractere, et tout
# appariement par prefixe echoue. L'arbitrage etant de toute facon manuel,
# on designe la ligne plutot que de faire semblant de la deviner.
GROUPE_C = {
    'I.2.2': 321,       # 01_chapitre_I.md — 2e ### sous le ## l.297 (I.2.2)
    'II.1.1': None,     # a designer quand le chapitre II sera traite
    'II.1.2': None,
    'II.2.3': None,
    'III.3.4': None,
}

# Le markdown de la these porte des artefacts d'edition : emphase `*...*`,
# apostrophes echappees `\'`, espaces de fin. Ils ont leur place dans le
# texte ; ils n'en ont aucune dans un libelle de noeud.
def nettoie_titre(t):
    t = (t or '').replace("\\'", "'").replace('\\"', '"')
    t = re.sub(r'(\*{1,3})(.+?)\1', r'\2', t)
    return ' '.join(t.split())


def chapitre_de(cle):
    """Rattache une cle du graphe a son fichier markdown."""
    if cle.startswith('intro'):
        return 'intro'
    if cle.startswith('conclu'):
        return 'conclu'
    for prefixe, ch in (('III.', 'chap3'), ('II.', 'chap2'), ('I.', 'chap1')):
        if cle.startswith(prefixe):
            return ch
    return ''


def arbre_md(suffixe_fichier=''):
    """-> (par_cle, par_norme, lignes) sur l'arborescence des titres.

    `suffixe_fichier='_EN'` lit les traductions. Les deux versions portent la
    meme structure de titres — verifie chapitre par chapitre — de sorte que la
    meme cle canonique y designe le meme titre.
    """
    lignes = []
    for ch, f in FICHIERS:
        if suffixe_fichier:
            f = f.replace('.md', suffixe_fichier + '.md')
        p = os.path.join(MD, f)
        if not os.path.exists(p):
            continue
        parent, rang = None, collections.Counter()
        for l in numerote(titres(p), ch):
            l['norm'] = sans_numero(l['titre'])
            if l['niveau'] <= 2:
                parent = l['cle'] if l['niveau'] == 2 else None
            elif l['niveau'] == 3 and parent:
                rang[parent] += 1
                l['parent'], l['suffixe'] = parent, chr(ord('a') + rang[parent] - 1)
            lignes.append(l)
    par_cle = {l['cle']: l for l in lignes if l['cle'] and l['niveau'] <= 2}
    par_norme = collections.defaultdict(list)
    for l in lignes:
        if l['norm']:
            par_norme[l['norm']].append(l)
    return par_cle, par_norme, lignes


def main(argv=None):
    p = argparse.ArgumentParser(description="Patch de migration des sections.")
    p.add_argument('--graph', default=None)
    p.add_argument('--plan', default=os.path.join(REPO, 'docs', 'audits', 'data',
                                                  'section-migration.csv'))
    p.add_argument('--out', default=os.path.join(REPO, 'patch_13_section_migration.json'))
    p.add_argument('--chapitre', default=None, choices=[c for c, _ in FICHIERS],
                   help="Ne traite qu'un fichier de la these. Les autres noeuds "
                        "restent en l'etat et sont comptes dans les collisions.")
    args = p.parse_args(argv)

    chemin = args.graph or graphe_le_plus_recent()
    with open(chemin, encoding='utf-8') as f:
        g = json.load(f)
    entites = {e['id']: e for e in g['entities']}
    with open(args.plan, encoding='utf-8') as f:
        plan = list(csv.DictReader(f, delimiter=';'))

    par_cle, par_norme, lignes_md = arbre_md()
    # Les numeros de ligne se repetent d'un fichier a l'autre : la cle inclut
    # le chapitre, sinon l.321 du chapitre I designerait aussi celle du III.
    par_ligne = {(l['chapitre'], l['ligne']): l for l in lignes_md}

    # Cote anglais, on indexe par cle CANONIQUE — y compris les rangs
    # subordonnes (I.1.1.a) — pour realigner `labelEn` en meme temps que le
    # nom francais. Sans cela le libelle anglais garderait l'ancienne
    # numerotation et une formulation que le francais vient d'abandonner.
    _, _, lignes_en = arbre_md('_EN')
    par_cle_en = {}
    for l in lignes_en:
        if l['niveau'] <= 2 and l['cle']:
            par_cle_en[l['cle']] = l
        elif l.get('parent'):
            par_cle_en[f"{l['parent']}.{l['suffixe']}"] = l

    def apparie(nom):
        n = sans_numero(nom)
        if n in par_norme:
            return par_norme[n]
        return [l for k, ls in par_norme.items()
                if len(n) >= 25 and (n[:45] in k or k[:45] in n) for l in ls]

    ops, decisions, non_resolus = [], [], []

    def libelle(cle, titre):
        """Libelle final : cle + titre de la these, sans reformulation."""
        return f'{cle} {nettoie_titre(titre)}'.strip()

    ecartes = collections.Counter()
    for r in plan:
        cle_act, eid = r['cle_actuelle'], r['id']
        ent = entites.get(eid)
        if not ent:
            ecartes['absent du graphe'] += 1
            continue
        if not cle_act:
            ecartes['sans section_key — affectation, pas migration'] += 1
            continue
        if args.chapitre and chapitre_de(cle_act) != args.chapitre:
            ecartes[f'hors du perimetre --chapitre {args.chapitre}'] += 1
            continue
        cible, titre, motif = None, None, ''

        if cle_act in GROUPE_A or cle_act in GROUPE_B or r['decision'] == 'CONFORME':
            cible = cle_act
            l = par_cle.get(cle_act)
            if l:
                titre, motif = l['titre'], 'libelle realigne sur la these'
            else:
                motif = 'cle conservee, titre introuvable dans le markdown'
        elif r['decision'] == 'RENUMEROTER':
            cible = r['cle_cible']
            l = par_cle.get(cible)
            titre = l['titre'] if l else None
            motif = f"renumerotation {cle_act} -> {cible}"
        elif r['decision'] == 'RETROGRADER' or cle_act in GROUPE_C:
            vise = GROUPE_C.get(cle_act)
            if vise:
                c = [par_ligne[(chapitre_de(cle_act), vise)]]
            else:
                c = [x for x in apparie(ent.get('name', ''))
                     if x['niveau'] >= 3 and x.get('parent')]
            if c and c[0].get('parent'):
                cible = f"{c[0]['parent']}.{c[0]['suffixe']}"
                titre = c[0]['titre']
                motif = (f"second rang subordonne (### l.{c[0]['ligne']}, "
                         f"parent {c[0]['parent']})")
            else:
                non_resolus.append((cle_act, ent.get('name', ''), 'parent introuvable'))
                continue
        else:
            non_resolus.append((cle_act, ent.get('name', ''), r['decision']))
            continue

        nouveau_nom = libelle(cible, titre) if titre else ent.get('name', '')
        change = []
        if cible and cible != cle_act:
            ops.append({'type': 'SET_ATTRIBUTE', 'entityId': eid,
                        'attributeId': 'section_key',
                        'value': {'type': 'TEXT', 'value': cible,
                                  'options': {'language': 'fr'}},
                        '_comment': motif})
            change.append('section_key')
        if nouveau_nom and nouveau_nom != ent.get('name', ''):
            ops.append({'type': 'SET_NAME', 'entityId': eid, 'value': nouveau_nom,
                        '_comment': motif})
            change.append('name')

        # `labelEn` n'existe que sur une partie des sections. On le realigne
        # la ou il existe ; on ne le cree pas la ou il manque — ce serait
        # enrichir, pas migrer.
        label_en = (ent.get('attributes') or {}).get('labelEn')
        l_en = par_cle_en.get(cible) if cible else None
        if label_en and l_en:
            nouveau_en = libelle(cible, l_en['titre'])
            if nouveau_en != label_en.get('value'):
                ops.append({'type': 'SET_ATTRIBUTE', 'entityId': eid,
                            'attributeId': 'labelEn',
                            'value': {'type': 'TEXT', 'value': nouveau_en,
                                      'options': label_en.get('options',
                                                              {'language': 'fr'})},
                            '_comment': motif + ' — libelle anglais realigne'})
                change.append('labelEn')
        decisions.append({'id': eid, 'cle_actuelle': cle_act, 'cle_cible': cible,
                          'nom_avant': ent.get('name', ''), 'nom_apres': nouveau_nom,
                          'change': '+'.join(change) or 'aucun', 'motif': motif})

    # Collisions sur l'etat final — en incluant les noeuds NON traites, qui
    # conservent leur cle actuelle. Ne compter que les traites reproduirait
    # l'angle mort corrige plus tot : une cible peut etre libre entre les
    # renumerotations et tenue par un noeud qu'on a laisse de cote.
    traites = {d['id'] for d in decisions}
    final = {}
    for d in decisions:
        final.setdefault(d['cle_cible'], []).append(d['id'])
    for r in plan:
        if r['id'] not in traites and r['cle_actuelle']:
            final.setdefault(r['cle_actuelle'], []).append(r['id'] + ' (non traite)')
    doublons = {k: v for k, v in final.items() if k and len(v) > 1}

    patch = {
        '_meta': {
            'patch_id': '13',
            'description': "Migration des ThesisSection au niveau canonique ## "
                           "de la these, second rang subordonne, libelles realignes.",
            'source_graph': os.path.basename(chemin),
            'perimetre': args.chapitre or 'toute la these',
            'policy': "Ne modifie que section_key, name et labelEn. Aucune "
                      "entite creee, fusionnee ou supprimee. Aucune relation "
                      "touchee. Les noeuds sans section_key sont laisses en "
                      "l'etat ; labelEn n'est realigne que la ou il existe.",
            'arbitrages': {
                'niveau_canonique': '##, celui que la these emploie (ch. I l.99)',
                'niveau_3': 'second rang subordonne (I.1.1.a, I.1.1.b...)',
                'libelles': 'realignes sur la these ; les reformulations du graphe '
                            'sont abandonnees',
            },
        },
        'ops': ops,
    }
    with open(args.out, 'w', encoding='utf-8') as f:
        json.dump(patch, f, ensure_ascii=False, indent=1)

    c = collections.Counter(d['change'] for d in decisions)
    print(f"graphe    : {os.path.basename(chemin)}")
    print(f"perimetre : {args.chapitre or 'toute la these'}")
    print(f"sections traitees : {len(decisions)} / {len(plan)}")
    for k, n in c.most_common():
        print(f"  {n:4d}  {k}")
    for k, n in ecartes.most_common():
        print(f"  {n:4d}  ecarte : {k}")
    print()
    for d in sorted(decisions, key=lambda d: d['cle_actuelle']):
        fleche = f"{d['cle_actuelle']:10s} -> {d['cle_cible']:10s}"
        print(f"  {fleche} [{d['change']:11s}] {d['nom_apres'][:58]}")
    print()
    print(f"operations : {len(ops)}")
    print(f"collisions sur l'etat final : {doublons or 'AUCUNE'}")
    if non_resolus:
        print(f"non resolus : {len(non_resolus)}")
        for cle, nom, why in non_resolus[:8]:
            print(f"   {cle:16s} [{why}] {nom[:50]}")
    print(f"patch ecrit : {os.path.relpath(args.out, REPO)}")
    return 1 if doublons else 0


if __name__ == '__main__':
    sys.exit(main())
