#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Applique patch_18 (bibliographie) + patch_19 (attributs) et produit v110.

Deux patchs deposes le 06/08, chacun contre-verifie independamment de son
generateur avant application :

- **patch_18** — 1 coquille de nom (« Danzeis » -> « Danezis », confirmee
  ABSENTE de la bibliographie de la these convertie le meme jour) et
  21 retypages Reference -> Person : des fiches d'auteur sans millesime
  (« Paul Krugman », « Bruno Latour ») qu'aucune citation ne peut jamais
  atteindre, chacune CONFIRMEE par une entree d'auteur de la bibliographie
  (patronyme + prenom). Les 22 entrees de `_meta.skipped` restent Reference :
  4 cas d'homonymie ou de fiche multi-auteurs, et 18 noms que le PDF contredit
  ou ne porte pas — les promouvoir graverait des personnes fausses (details
  dans docs/audits/grc20-bibliographie-reconciliation-v1.md).

- **patch_19** — 384 normalisations mecaniques d'attributs (types GRC-20,
  etiquettes de langue, cles en double a la casse pres, chaine vide), toutes
  decrites par grc20-properties-registry-v1.json, qui devient un invariant
  de CI apres cette application.

Le script refuse d'appliquer l'un sans l'autre : le registre decrit l'etat
APRES patch_19, et la CI le controle — appliquer partiellement laisserait le
graphe courant en echec de son propre invariant.

Usage:
    python3 scripts/make_v110_apply_bib_and_attribute_patches.py --dry-run
    python3 scripts/make_v110_apply_bib_and_attribute_patches.py
"""
import argparse
import collections
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from grc20_commun import REPO  # noqa: E402

CODE_DONNEES, CODE_INVOCATION = 1, 2


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


def main(argv=None):
    p = argparse.ArgumentParser(description="v110 = v109 + patch_18 + patch_19.")
    p.add_argument('--source', default=os.path.join(REPO, 'grc20-these-mael-rolland-v109.json'))
    p.add_argument('--bib', default=os.path.join(REPO, 'patch_18_bibliography_fixes.json'))
    p.add_argument('--attrs', default=os.path.join(REPO, 'patch_19_attribute_normalisation.json'))
    p.add_argument('--registre', default=os.path.join(REPO, 'grc20-properties-registry-v1.json'))
    p.add_argument('--target', default=os.path.join(REPO, 'grc20-these-mael-rolland-v110.json'))
    p.add_argument('--dry-run', action='store_true')
    args = p.parse_args(argv)

    g = lire(args.source, 'graphe source')
    p18 = lire(args.bib, 'patch_18')
    p19 = lire(args.attrs, 'patch_19')
    registre = lire(args.registre, 'registre des proprietes')

    base = os.path.basename(args.source)
    for patch, nom in ((p18, 'patch_18'), (p19, 'patch_19')):
        declare = patch.get('_meta', {}).get('source_graph')
        if declare != base:
            echec(f"{nom} declare source_graph={declare}, incompatible avec {base}",
                  CODE_INVOCATION)

    E = {e['id']: e for e in g['entities']}
    nom_type = {t['id']: t.get('name') for t in g['types']}
    avant_e, avant_r = len(g['entities']), len(g['relations'])
    erreurs = []

    # ---------- validations ----------
    for o in p18.get('ops', []):
        if o['type'] not in ('SET_NAME', 'SET_TYPES'):
            erreurs.append(f"patch_18 : operation non supportee {o['type']}")
        elif o['entityId'] not in E:
            erreurs.append(f"patch_18 : entite inconnue {o['entityId']}")
        elif o['type'] == 'SET_TYPES':
            if any(t not in nom_type for t in o['value']):
                erreurs.append(f"patch_18 : type inconnu pour {o['entityId']}")
    for o in p19.get('ops', []):
        if o['type'] not in ('SET_ATTRIBUTE', 'DELETE_ATTRIBUTE'):
            erreurs.append(f"patch_19 : operation non supportee {o['type']}")
        elif o['entityId'] not in E:
            erreurs.append(f"patch_19 : entite inconnue {o['entityId']}")
        elif o['type'] == 'DELETE_ATTRIBUTE':
            if o['attributeId'] not in (E[o['entityId']].get('attributes') or {}):
                erreurs.append(f"patch_19 : suppression d'un attribut absent "
                               f"{o['attributeId']} sur {o['entityId']}")
    if erreurs:
        for x in erreurs[:15]:
            print(f"  - {x}")
        echec(f"{len(erreurs)} erreur(s) de validation")

    # ---------- application ----------
    doubles_avant = {n for n, c in collections.Counter(
        e['name'].strip().lower() for e in g['entities']
        if 'Person' in [nom_type.get(t, t) for t in e.get('types') or []]).items() if c > 1}
    compte = collections.Counter()
    for o in p18['ops']:
        e = E[o['entityId']]
        if o['type'] == 'SET_NAME':
            compte[f"renomme « {e['name'][:32]} »"] += 1
            e['name'] = o['value']
        else:
            avant = [nom_type.get(t, t) for t in e.get('types') or []]
            e['types'] = list(o['value'])
            compte[f"retype {'+'.join(avant)} -> "
                   f"{'+'.join(nom_type.get(t, t) for t in o['value'])}"] += 1
    for o in p19['ops']:
        e = E[o['entityId']]
        attrs = e.setdefault('attributes', {})
        if o['type'] == 'DELETE_ATTRIBUTE':
            del attrs[o['attributeId']]
            compte[f"supprime {o['attributeId']}"] += 1
        else:
            attrs[o['attributeId']] = {k: v for k, v in o['value'].items()}
            compte[f"normalise {o['attributeId']}"] += 1

    print(f"source : {base}")
    for k, n in sorted(compte.items(), key=lambda x: -x[1]):
        print(f"  {n:4d}  {k}")

    # ---------- verifications d'apres ----------
    if len(g['entities']) != avant_e or len(g['relations']) != avant_r:
        echec("aucune entite ni relation ne devait etre creee ou supprimee")
    # Le registre est l'invariant : toute cle du graphe doit y figurer, et les
    # cles depreciees ne doivent plus exister.
    entrees = registre.get('entries') or registre.get('properties') or []
    reg = {x['key']: x for x in entrees}
    cles = set()
    for e in g['entities']:
        cles |= set(e.get('attributes') or {})
    hors = cles - set(reg)
    if hors:
        echec(f"cles du graphe hors registre apres application : {sorted(hors)[:6]}")
    fantomes = [k for k, x in reg.items()
                if x.get('status') == 'deprecated' and k in cles]
    if fantomes:
        echec(f"cles depreciees encore presentes : {fantomes}")
    # Aucun retypage ne doit avoir CREE d'homonymie Person : on compare a
    # l'etat d'avant patch, pour ne pas echouer sur un doublon preexistant
    # qui ne serait pas de notre fait.
    doubles_apres = {n for n, c in collections.Counter(
        e['name'].strip().lower() for e in g['entities']
        if 'Person' in [nom_type.get(t, t) for t in e.get('types') or []]).items() if c > 1}
    nouveaux_doubles = doubles_apres - doubles_avant
    if nouveaux_doubles:
        echec(f"homonymie Person creee par le retypage : {sorted(nouveaux_doubles)[:5]}")
    print(f"\n  entites : {avant_e} (inchange) · relations : {avant_r} (inchange)")
    print(f"  cles d'attribut : {len(cles)} · toutes au registre · 0 depreciee restante")
    print("  0 homonymie Person creee")

    if args.dry_run:
        print("\n--dry-run : rien ecrit.")
        return 0

    espace = g.setdefault('space', {})
    m_v = re.search(r'-(v\d+)\.json$', os.path.basename(args.target))
    if not m_v:
        echec(f"nom de sortie sans numero de version : {os.path.basename(args.target)}",
              CODE_INVOCATION)
    espace['version'] = m_v.group(1)
    espace['entity_count'] = len(g['entities'])
    espace['relation_count'] = len(g['relations'])
    n_types = sum(1 for o in p18['ops'] if o['type'] == 'SET_TYPES')
    n_noms = sum(1 for o in p18['ops'] if o['type'] == 'SET_NAME')
    # La note heritee est bornee : chaque version prefixait l'historique
    # entier, qui enflait sans limite. L'historique complet vit dans
    # CLAUDE.md ; la note du graphe garde la version courante et un rappel
    # tronque.
    heritee = espace.get('note', '')
    if len(heritee) > 1200:
        heritee = heritee[:1200].rsplit(' ', 1)[0] + ' […]'
    espace['note'] = (f"V110 — bibliographie et attributs : {n_noms} coquille de nom corrigee "
                      f"(Danezis), {n_types} fiches d'auteur retypees Reference -> Person "
                      "(injoignables par citation, confirmees par la bibliographie, zero "
                      "homonymie creee), 384 normalisations d'attributs decrites par "
                      "grc20-properties-registry-v1.json, desormais invariant de CI. "
                      + heritee)
    with open(args.target, 'w', encoding='utf-8') as f:
        json.dump(g, f, ensure_ascii=False, indent=2)
    print(f"\ngraphe ecrit : {os.path.relpath(args.target, REPO)}")
    return 0


if __name__ == '__main__':
    sys.exit(main())
