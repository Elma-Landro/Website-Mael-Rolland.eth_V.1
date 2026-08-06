#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verifie la coherence de la couche d'ancrage contre un graphe GRC-20.

Chaque artefact du depot est defendable isolement ; aucun n'est verifie contre
un autre. Ce script comble ce trou. Il ne modifie rien.

Artefacts controles :
    entity_section_map.json     entite -> sections (+ extraits)
    section_entities_map.json   section -> entites (consomme par lecteur.html)
    section_overrides.json      entites epinglees par section
    narrative-anchors.json      citations mises en scene
    story-presets.mjs           recits guides (references par NOM, pas par id)

Controles :
    A. tout entity_id des cartes existe dans le graphe
    B. toute cle de section des cartes correspond a une section du graphe
    C. tout id epingle existe ET figure dans la liste de sa section
    D. tout id et tout focusNode de narrative-anchors resout
    E. toute reference de story resout (table d'alias appliquee)
    F. tout allowedRelationTypes de story existe dans relation_types

Les controles E et F delegent la lecture de `story-presets.mjs` a
`scripts/dump_story_presets.mjs` : c'est un module ES, Node sait l'importer,
et le deviner par expressions regulieres est fragile — les apostrophes
typographiques des libelles francais suffisent a fausser l'extraction (mesure :
1 artefact produit, 3 references ratees). Si Node est absent, E et F sont
sautes avec un avertissement ; les autres controles restent valides.

Pourquoi une baseline : la dette existante est connue et documentee. Echouer
sur elle des le premier jour rendrait le controle inutile. La baseline fige
l'existant ; le script n'echoue que sur une *regression*. C'est ce qui rend
une fusion d'entites sure : elle ne peut plus casser une reference en silence.

Usage:
    python3 scripts/check_anchoring.py
    python3 scripts/check_anchoring.py --graph grc20-these-mael-rolland-v98.json
    python3 scripts/check_anchoring.py --write-baseline
    python3 scripts/check_anchoring.py --no-baseline     # dette comprise

Codes de sortie :
    0 = aucune regression
    1 = au moins une regression par rapport a la baseline
    2 = erreur fatale (fichier introuvable, JSON invalide)
"""
import argparse
import collections
import json
import os
import re
import shutil
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from grc20_commun import (  # noqa: E402,F401
    REPO, est_section, graphe_le_plus_recent, normalise_doux, sans_accents,
)

BASELINE_DEFAUT = os.path.join(REPO, 'docs', 'audits', 'data', 'anchoring-baseline.json')


# ---------------------------------------------------------------- utilitaires

# Ici la ponctuation compte : on compare des noms d'entites, ou « CM : boucs »
# et « CM boucs » ne doivent pas se confondre. C'est la variante douce, celle
# qui n'ecrase pas la ponctuation — a ne pas confondre avec celle de
# derive_section_tree, qui l'ecrase pour apparier des titres.
normalise = normalise_doux


def charger_json(chemin, obligatoire=True):
    if not os.path.exists(chemin):
        if obligatoire:
            raise FileNotFoundError(chemin)
        return None
    with open(chemin, encoding='utf-8') as f:
        return json.load(f)


def index_graphe(graphe):
    """-> (ids, noms, cles_section, types_relation) depuis un graphe charge."""
    nom_type = {t['id']: t.get('name') for t in graphe.get('types', [])}
    ids = {e['id'] for e in graphe.get('entities', [])}
    noms = {}
    for e in graphe.get('entities', []):
        noms.setdefault(e.get('name'), e['id'])
    types_relation = {r.get('name') for r in graphe.get('relation_types', [])}

    cles_section = {}
    for e in graphe.get('entities', []):
        # Les deux types de section : III.3 est l'unique `ChapterSection` du
        # graphe et passait pour absente, d'ou le B:sem:III.3 de la baseline.
        if est_section(e, nom_type):
            a = (e.get('attributes') or {}).get('section_key')
            cle = (a.get('value') if a else '') or ''
            if cle:
                cles_section[cle] = e['id']
    return ids, noms, cles_section, types_relation


def lire_story_presets(repo=REPO):
    """Delegue a Node la lecture de story-presets.mjs.

    -> (presets | None, raison). `raison` est vide en cas de succes, et
    porte sinon le motif exact. Le retour nu ne suffisait pas : un
    story-presets.mjs casse, un plantage de Node et une table d'alias
    illisible produisaient tous `None`, donc le meme message a l'ecran —
    alors qu'une table d'alias vide transforme des references parfaitement
    resolues en fausses regressions `E:focus:`. L'operateur doit pouvoir
    distinguer les trois.
    """
    node = shutil.which('node')
    if not node:
        return None, 'Node introuvable dans le PATH'
    helper = os.path.join(repo, 'scripts', 'dump_story_presets.mjs')
    if not os.path.exists(helper):
        return None, f'{os.path.relpath(helper, REPO)} absent'

    # Aucune des trois valeurs ne vient d'une entree externe : `node` est
    # resolu par shutil.which, `helper` est derive de __file__, `repo` est
    # une constante ou un chemin passe en ligne de commande par l'operateur
    # qui execute deja ce script. Pas de shell, liste d'arguments explicite.
    commande = [node, helper, '--repo', repo]
    try:
        r = subprocess.run(commande, capture_output=True, text=True,  # noqa: S603
                           timeout=60, shell=False)
    except subprocess.TimeoutExpired:
        return None, 'le lecteur Node a depasse 60 s'
    except OSError as err:
        return None, f'lancement impossible : {err}'

    erreur = (r.stderr or '').strip()
    if r.returncode != 0:
        return None, f'Node a echoue (code {r.returncode}) : {erreur or "sans message"}'
    if not r.stdout.strip():
        return None, f'sortie vide{" ; " + erreur if erreur else ""}'
    try:
        presets = json.loads(r.stdout)
    except json.JSONDecodeError as err:
        return None, f'sortie illisible : {err}'

    # Une table d'alias vide *par echec* ne se voit pas autrement : le
    # helper la signale explicitement.
    if not presets.get('aliasesOk', True):
        return presets, f'table d\'alias illisible — {erreur or "motif non precise"}'
    return presets, ''


# ------------------------------------------------------------------ controles

def collecter_problemes(graphe, esm, sem, ovr, anc, presets):
    """-> liste de (code, categorie, detail). Aucun effet de bord."""
    ids, noms, cles_section, types_relation = index_graphe(graphe)
    problemes = []

    def signale(code, categorie, detail):
        problemes.append((code, categorie, detail))

    # A. identifiants des cartes
    for eid, bloc in (esm or {}).items():
        if eid not in ids:
            signale(f'A:esm:{eid}', 'entite de entity_section_map absente du graphe',
                    f"{eid} — « {(bloc or {}).get('name', '?')} »")

    vus = set()
    for cle, bloc in (sem or {}).items():
        for ent in (bloc or {}).get('entities', []):
            eid = ent.get('entity_id')
            if eid and eid not in ids and eid not in vus:
                vus.add(eid)
                signale(f'A:sem:{eid}', 'entite de section_entities_map absente du graphe',
                        f"{eid} — « {ent.get('entity_name', '?')} » (section {cle})")

    # B. cles de section
    for cle in (sem or {}):
        if cle not in cles_section and not cle.endswith('_preamble'):
            signale(f'B:sem:{cle}', 'cle de section_entities_map sans section dans le graphe', cle)
    for cle in cles_section:
        if cle not in (sem or {}):
            signale(f'B:graph:{cle}', 'section du graphe sans entree dans section_entities_map',
                    cle)

    # C. epinglages
    for cle, liste in (ovr or {}).items():
        if cle.startswith('_') or not isinstance(liste, list):
            continue
        if cle not in (sem or {}):
            signale(f'C:cle:{cle}', 'section epinglee inconnue de section_entities_map', cle)
            continue
        presents = {e.get('entity_id') for e in (sem[cle] or {}).get('entities', [])}
        for eid in liste:
            if eid not in ids:
                signale(f'C:abs:{cle}:{eid}', 'entite epinglee absente du graphe',
                        f"{eid} (section {cle})")
            elif eid not in presents:
                signale(f'C:hors:{cle}:{eid}',
                        'entite epinglee hors de la liste de sa section',
                        f"{eid} (section {cle})")

    # D. narrative-anchors
    for a in (anc or {}).get('anchors', []):
        for champ in ('sourceQuoteId', 'primaryEntityId'):
            v = a.get(champ)
            if v and v not in ids:
                signale(f'D:{champ}:{v}', f'narrative-anchors : {champ} non resolu', v)
        for v in (a.get('secondaryEntityIds') or []):
            if v not in ids:
                signale(f'D:sec:{v}', 'narrative-anchors : secondaryEntityId non resolu', v)
        for n in ((a.get('graphScene') or {}).get('focusNodes') or []):
            if n not in noms:
                signale(f'D:focus:{n}', 'narrative-anchors : focusNode non resolu (par nom)',
                        n)

    # E / F. stories — seulement si Node a pu lire le module
    if presets:
        par_norme = collections.defaultdict(list)
        for n in noms:
            par_norme[normalise(n)].append(n)
        alias = presets.get('aliases') or {}

        for r in presets.get('focusRefs', []):
            c = alias.get(r, r)
            if c in ids or c in noms or r in ids or r in noms:
                continue
            if par_norme.get(normalise(c)) or par_norme.get(normalise(r)):
                continue
            signale(f'E:focus:{r}', 'story-presets : focusNode non resolu', r)

        # `allowedRelationTypes` est une liste BLANCHE : un nom mort y retire
        # silencieusement des aretes qu'on croyait montrer. graphe.html le
        # compare apres `canonicalizeRelationName` — minuscules PUIS
        # suppression de tout non-alphanumerique — donc « part of » et
        # « partOf » s'y confondent.
        canon = {re.sub(r'[^a-z0-9]', '', t.lower()) for t in types_relation}
        for rt in presets.get('allowedRelationTypes', []):
            if re.sub(r'[^a-z0-9]', '', rt.lower()) not in canon:
                signale(f'F:rel:{rt}', 'story-presets : relation_type inexistant', rt)

        # Les listes d'ossature et de masquage passent, elles, par
        # `normalizeRelationName` : minuscules SANS suppression des espaces.
        # « partOf » n'y vaut donc PAS « part of ». Ce controle manquait, et
        # ce que la mesure a montre en le posant : les quatre jetons de
        # `backboneRelationTypes` sont morts, y compris le defaut code en dur
        # dans graphe.html (l.5502) — `hideBackbone` ne masque donc rien.
        noms_relation = {t.lower() for t in types_relation}
        for cle in ('backboneRelationTypes', 'hideRelationTypes', 'showRelationTypes'):
            for rt in presets.get(cle, []):
                if rt.lower() not in noms_relation:
                    signale(f'F:{cle}:{rt}',
                            f'story-presets : {cle} inexistant', rt)

    return problemes


# ----------------------------------------------------------------------- main

def main(argv=None):
    p = argparse.ArgumentParser(description="Controle d'integrite de la couche d'ancrage.")
    p.add_argument('--graph', '-g', default=None,
                   help="Graphe cible (defaut : la version la plus recente presente).")
    p.add_argument('--baseline', default=BASELINE_DEFAUT)
    p.add_argument('--write-baseline', action='store_true',
                   help="Fige l'etat courant comme reference et sort en 0.")
    p.add_argument('--no-baseline', action='store_true',
                   help="Ignore la baseline : echoue sur toute la dette.")
    p.add_argument('--quiet', '-q', action='store_true')
    args = p.parse_args(argv)

    chemin_graphe = args.graph or graphe_le_plus_recent()
    if not chemin_graphe or not os.path.exists(chemin_graphe):
        print("ERREUR : aucun graphe trouve. Utilisez --graph.", file=sys.stderr)
        return 2

    try:
        graphe = charger_json(chemin_graphe)
        esm = charger_json(os.path.join(REPO, 'entity_section_map.json'))
        sem = charger_json(os.path.join(REPO, 'section_entities_map.json'))
        ovr = charger_json(os.path.join(REPO, 'section_overrides.json'), False) or {}
        anc = charger_json(os.path.join(REPO, 'narrative-anchors.json'), False) or {}
    except FileNotFoundError as e:
        print(f"ERREUR : {e} introuvable.", file=sys.stderr)
        return 2
    except json.JSONDecodeError as e:
        print(f"ERREUR : JSON invalide ({e}).", file=sys.stderr)
        return 2

    presets, raison_presets = lire_story_presets()
    problemes = collecter_problemes(graphe, esm, sem, ovr, anc, presets)

    # Un meme code peut etre signale plusieurs fois : on compte les problemes
    # DISTINCTS, jamais les occurrences. Trois audits de ce depot se sont deja
    # contredits pour avoir melange les deux.
    cat_par_code = {}
    for code, cat, _ in problemes:
        cat_par_code.setdefault(code, cat)
    codes = set(cat_par_code)

    base = set()
    if not args.no_baseline and os.path.exists(args.baseline):
        base = set((charger_json(args.baseline) or {}).get('known', []))

    regressions = sorted(codes - base)
    resolus = sorted(base - codes)

    if args.write_baseline:
        os.makedirs(os.path.dirname(args.baseline), exist_ok=True)
        with open(args.baseline, 'w', encoding='utf-8') as f:
            json.dump({
                '_comment': "Dette d'ancrage connue au moment du gel. Le controle "
                            "n'echoue que sur les codes ABSENTS de cette liste. "
                            "Retirer un code ici quand il est reellement corrige.",
                'graph': os.path.basename(chemin_graphe),
                'count': len(codes),
                'known': sorted(codes),
            }, f, ensure_ascii=False, indent=1)
        print(f"baseline ecrite : {len(codes)} problemes figes "
              f"({os.path.relpath(args.baseline, REPO)})")
        return 0

    if not args.quiet:
        _, _, cles_section, _ = index_graphe(graphe)
        print(f"graphe   : {os.path.basename(chemin_graphe)} "
              f"({len(graphe.get('entities', []))} entites, "
              f"{len(cles_section)} sections avec section_key)")
        print(f"artefacts: entity_section_map {len(esm)} · section_entities_map {len(sem)} · "
              f"overrides {sum(1 for k in ovr if not k.startswith('_'))} · "
              f"narrative-anchors {len(anc.get('anchors', []))}")
        if presets:
            print(f"stories  : {presets['stories']} recits, {presets['steps']} etapes, "
                  f"{len(presets['focusRefs'])} references, "
                  f"{len(presets['aliases'])} alias (lus via Node)")
            if raison_presets:
                print(f"           ATTENTION : {raison_presets}")
        else:
            print(f"stories  : NON VERIFIEES — {raison_presets}")
        print()
        par_cat = collections.Counter(cat_par_code.values())
        if par_cat:
            print(f"problemes distincts detectes : {len(codes)}")
            for cat, n in par_cat.most_common():
                print(f"  {n:5d}  {cat}")
        else:
            print("aucun probleme detecte.")
        print()
        if base:
            print(f"baseline : {len(base)} problemes connus")
            if resolus:
                print(f"  {len(resolus)} corriges depuis le gel — pensez a rafraichir "
                      f"la baseline (--write-baseline)")

    if regressions:
        print()
        print(f"REGRESSION : {len(regressions)} probleme(s) absent(s) de la baseline")
        detail = {c: (cat, det) for c, cat, det in problemes}
        for c in regressions[:30]:
            cat, det = detail[c]
            print(f"  - [{cat}] {det}")
        if len(regressions) > 30:
            print(f"  … et {len(regressions) - 30} autres")
        return 1

    if not args.quiet:
        print("OK — aucune regression.")
    return 0


if __name__ == '__main__':
    sys.exit(main())
