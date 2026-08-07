#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Voie C — rend chaque charge d'ancrage a la section dont elle decrit le texte.

LE CONSTAT, verifie deux fois (simulation independante, puis relecture a la
main) : les listes d'ancrage decrivent des PLAGES DE TEXTE, pas des noeuds.
En localisant les 20 056 extraits de `entity_section_map.json` ligne a ligne
dans `assets/MD/`, 18 cles se revelent decalees d'un cran, en correspondance
une-pour-une : la liste rangee sous « II.2.2.c » decrit a 100 % le bloc
« II.2.3 » ; sous « I.2.2 », le bloc « I.2.1 » ; etc.

LA CAUSE : avant les migrations v100/v106, ces cles etaient JUSTES — la cle
« II.2.3 » couvrait le bloc II.2.3. C'est le NOEUD qui etait faux : il portait
un titre de niveau 3. Les migrations ont renomme les noeuds d'apres leur titre
(defendable), et `remap_section_keys.py` a fait suivre les listes (c'etait
l'erreur : elles n'auraient pas du bouger). Consequence : 8 sections du
sommaire paraissaient vides alors que leur contenu existait, sous la cle de la
voisine.

V108 A AGGRAVE LA CHOSE SANS LE SAVOIR : il a realigne l'attribut
`section_key` des relations sur la cle de leur cible — donc ecrase la seule
trace restante de la verite (l'attribut nommait le bloc reel). v107 sert ici
d'oracle pour la retrouver ; la bijection des 18 cles rend de toute facon
l'operation reversible.

CE QUE CE SCRIPT FAIT, en une passe simultanee (5 des 18 cles sont a la fois
source et cible : sequentiel = double deplacement) :
  1. graphe : rebranche le `to` des relations « appears in section » dont
     l'attribut v107 nomme un bloc different de leur cible — vers le noeud qui
     porte AUJOURD'HUI la cle de ce bloc — et realigne l'attribut dessus ;
  2. cartes : renomme les 18 cles de `section_entities_map.json` et
     `entity_section_map.json` sur le bloc que leurs extraits couvrent.

CE QU'IL NE FAIT PAS : il ne recalcule aucun poids (la question du poids
mandataire — voie A — reste entiere et ouverte) ; il ne touche ni aux noeuds,
ni a leurs cles, ni a `section_overrides.json` (aucune de ses cles n'est dans
les 18 — verifie).

Usage:
    python3 scripts/make_v109_realign_anchoring_charges.py --dry-run
    python3 scripts/make_v109_realign_anchoring_charges.py
"""
import argparse
import collections
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from grc20_commun import REPO, est_section  # noqa: E402

# La bijection cle-portee-aujourd'hui -> bloc reellement couvert par sa charge.
# C'est l'INVERSE exact du remap cumule des migrations v100 (5 cles) et v106
# (13 cles). Etablie par localisation des extraits (7 cas sur 8 a 100 %, le
# 8e — III.2.1 — a 99,6 % en localisation fine), puis re-verifiee a la main.
CHARGE_VERS_BLOC = {
    'I.1.1.a': 'I.1.1',   'I.1.1.b': 'I.1.2',   'I.1.2': 'I.1.3',
    'I.2.2': 'I.2.1',     'I.2.2.b': 'I.2.2',
    'II.1.1.a': 'II.1.1', 'II.1.1.b': 'II.1.2',
    'II.2.2.a': 'II.2.1', 'II.2.2.b': 'II.2.2', 'II.2.2.c': 'II.2.3',
    'II.3.1.a': 'II.3.1', 'II.3.1.b': 'II.3.2', 'II.3.2': 'II.3.3',
    'III.1.1.a': 'III.1.1', 'III.1.1.b': 'III.1.2',
    'III.1.2.a': 'III.2.1', 'III.1.2.b': 'III.2.2', 'III.2.1': 'III.2.3',
}

CODE_DONNEES, CODE_INVOCATION = 1, 2


def echec(msg, code=CODE_DONNEES):
    famille = 'invocation' if code == CODE_INVOCATION else 'donnees'
    print(f"ECHEC ({famille}) : {msg}", file=sys.stderr)
    sys.exit(code)


def attr_val(attrs, cle):
    if isinstance(attrs, dict):
        v = attrs.get(cle)
        return v.get('value') if isinstance(v, dict) else v
    return None


def main(argv=None):
    p = argparse.ArgumentParser(description="Voie C : realigne les charges d'ancrage.")
    p.add_argument('--source', default=os.path.join(REPO, 'grc20-these-mael-rolland-v108.json'))
    p.add_argument('--oracle', default=os.path.join(REPO, 'grc20-these-mael-rolland-v107.json'),
                   help="Graphe AVANT v108 : ses attributs de relation nomment "
                        "encore le bloc reel.")
    p.add_argument('--target', default=os.path.join(REPO, 'grc20-these-mael-rolland-v109.json'))
    p.add_argument('--dry-run', action='store_true')
    args = p.parse_args(argv)

    for chemin, quoi in ((args.source, 'graphe source'), (args.oracle, 'graphe oracle')):
        if not os.path.exists(chemin):
            echec(f"{quoi} introuvable : {chemin}", CODE_INVOCATION)
    with open(args.source, encoding='utf-8') as f:
        g = json.load(f)
    with open(args.oracle, encoding='utf-8') as f:
        oracle = json.load(f)

    # Verification de coherence : la bijection doit etre... une bijection.
    if len(set(CHARGE_VERS_BLOC.values())) != len(CHARGE_VERS_BLOC):
        echec("la table charge->bloc n'est pas injective")

    nom_type = {t['id']: t.get('name') or t['id'] for t in g['types']}
    rt_id = {r.get('name'): r['id'] for r in g['relation_types']}
    if 'appears in section' not in rt_id:
        echec("type de relation « appears in section » absent")
    T_APP = rt_id['appears in section']

    id_de_cle = {}
    for e in g['entities']:
        if est_section(e, nom_type):
            k = attr_val(e.get('attributes'), 'section_key')
            if k:
                if k in id_de_cle:
                    echec(f"cle de section en double dans le graphe : {k}")
                id_de_cle[k] = e['id']
    manquantes = [b for b in CHARGE_VERS_BLOC.values() if b not in id_de_cle]
    if manquantes:
        echec(f"blocs cibles sans noeud : {manquantes}")

    # L'oracle : attribut section_key de v107, par identifiant de relation.
    verite = {}
    for r in oracle['relations']:
        if r.get('type') == T_APP and r.get('id'):
            v = attr_val(r.get('attributes'), 'section_key')
            if v:
                verite[r['id']] = v

    cle_de_id = {v: k for k, v in id_de_cle.items()}
    avant_e, avant_r = len(g['entities']), len(g['relations'])

    rebranchees = collections.Counter()
    conformes, sans_oracle, hors_table = 0, 0, 0
    for r in g['relations']:
        if r.get('type') != T_APP:
            continue
        cible_cle = cle_de_id.get(r.get('to'))
        bloc = verite.get(r.get('id'))
        if bloc is None:
            sans_oracle += 1
            continue
        if bloc == cible_cle:
            conformes += 1
            continue
        # L'attribut v107 nomme un autre bloc que la cible : la cible actuelle
        # est l'effet du renommage des noeuds. On rebranche vers le noeud qui
        # porte aujourd'hui la cle du bloc. Garde-fou : le mouvement doit etre
        # celui de la bijection — tout autre ecart est une anomalie a refuser,
        # pas a « corriger » en silence.
        if CHARGE_VERS_BLOC.get(cible_cle) != bloc:
            hors_table += 1
            continue
        r['to'] = id_de_cle[bloc]
        attrs = r.setdefault('attributes', {})
        if isinstance(attrs, dict):
            attrs['section_key'] = {'type': 'TEXT', 'value': bloc,
                                    'options': {'language': 'fr'}}
        rebranchees[(cible_cle, bloc)] += 1

    print(f"source : {os.path.basename(args.source)} · oracle : {os.path.basename(args.oracle)}")
    print(f"  relations rebranchees vers leur bloc reel : {sum(rebranchees.values())}")
    for (a, b), n in rebranchees.most_common(20):
        print(f"      {n:5d}  noeud « {a} » -> noeud « {b} »")
    print(f"  deja conformes (bloc == cible)            : {conformes}")
    print(f"  sans oracle v107 (laisses en l'etat)      : {sans_oracle}")
    if hors_table:
        echec(f"{hors_table} relation(s) dont l'ecart ne suit pas la bijection "
              f"— a examiner avant toute application")

    # ---------- les cartes, en remap SIMULTANE ----------
    # Garde d'idempotence : 5 des 18 cles sont a la fois source et cible.
    # Rejouer le script sur des cartes deja converties re-deplacerait le lot
    # fraichement pose (« I.2.2 », devenu la charge de l'ex-« I.2.2.b »,
    # repartirait vers « I.2.1 »). On exige la presence d'une cle qui
    # n'existe QUE dans l'etat pre-conversion.
    with open(os.path.join(REPO, 'section_entities_map.json'), encoding='utf-8') as f:
        _sem_avant = json.load(f)
    temoins = [k for k in CHARGE_VERS_BLOC if k not in CHARGE_VERS_BLOC.values()]
    if not any(k in _sem_avant for k in temoins):
        echec("les cartes semblent DEJA converties (aucune cle temoin "
              f"pre-conversion presente : {temoins[:4]}...) — rejouer ce "
              "script re-deplacerait les charges fraichement posees")
    remaps = {}
    for fichier in ('section_entities_map.json', 'entity_section_map.json'):
        chemin = os.path.join(REPO, fichier)
        with open(chemin, encoding='utf-8') as f:
            data = json.load(f)
        n = 0
        if fichier == 'section_entities_map.json':
            nouveau = {}
            for k, v in data.items():
                nk = CHARGE_VERS_BLOC.get(k, k)
                if nk != k:
                    n += 1
                if nk in nouveau:
                    echec(f"collision de cles dans {fichier} : {nk}")
                nouveau[nk] = v
            remaps[fichier] = (nouveau, n)
        else:
            for _eid, rec in data.items():
                for s in rec.get('sections', []):
                    nk = CHARGE_VERS_BLOC.get(s.get('section_key'))
                    if nk:
                        s['section_key'] = nk
                        n += 1
            remaps[fichier] = (data, n)
        print(f"  {fichier:28s} : {n} remappage(s)")

    with open(os.path.join(REPO, 'section_overrides.json'), encoding='utf-8') as f:
        ov = json.load(f)
    touchees = [k for k in ov if k in CHARGE_VERS_BLOC]
    if touchees:
        echec(f"section_overrides.json porte des cles de la bijection : {touchees}")

    # ---------- verifications d'apres ----------
    if len(g['entities']) != avant_e or len(g['relations']) != avant_r:
        echec("aucune entite ni relation ne devait etre creee ou supprimee")
    for r in g['relations']:
        if r.get('type') != T_APP:
            continue
        b = attr_val(r.get('attributes'), 'section_key')
        c = cle_de_id.get(r.get('to'))
        if b and c and b != c:
            echec(f"relation {r.get('id')} : attribut {b} != cible {c} apres application")
    sem_nouveau = remaps['section_entities_map.json'][0]
    vides = [k for k in ('I.1.3', 'I.2.1', 'II.1.2', 'II.2.1', 'II.2.3',
                         'II.3.3', 'III.2.2', 'III.2.3')
             if not (sem_nouveau.get(k) or {}).get('entities')]
    if vides:
        echec(f"sections censees etre remplies encore vides : {vides}")
    print("  les 8 sections du sommaire jadis vides portent desormais une liste : OK")

    if args.dry_run:
        print("\n--dry-run : rien ecrit.")
        return 0

    for fichier, (data, _) in remaps.items():
        with open(os.path.join(REPO, fichier), 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(f"  ecrit : {fichier}")

    espace = g.setdefault('space', {})
    m_v = re.search(r'-(v\d+)\.json$', os.path.basename(args.target))
    if not m_v:
        echec(f"nom de sortie sans numero de version : {os.path.basename(args.target)}",
              CODE_INVOCATION)
    espace['version'] = m_v.group(1)
    espace['entity_count'] = len(g['entities'])
    espace['relation_count'] = len(g['relations'])
    espace['note'] = (f"V109 — voie C : {sum(rebranchees.values())} relations « appears in "
                      f"section » rebranchees vers la section dont leur charge decrit "
                      f"reellement le texte (18 cles decalees d'un cran par les migrations "
                      f"v100/v106 ; extraits localises a 100 % dans le bloc voisin). "
                      f"L'attribut section_key des relations redevient exact — v108 l'avait "
                      f"aligne sur des cibles alors erronees. Aucun poids recalcule. "
                      + (lambda h: h[:1200].rsplit(' ', 1)[0] + ' […]' if len(h) > 1200 else h)(espace.get('note', '')))
    with open(args.target, 'w', encoding='utf-8') as f:
        json.dump(g, f, ensure_ascii=False, indent=2)
    print(f"\ngraphe ecrit : {os.path.relpath(args.target, REPO)}")
    return 0


if __name__ == '__main__':
    sys.exit(main())
