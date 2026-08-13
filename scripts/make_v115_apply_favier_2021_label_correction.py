#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Applique patch_candidate_favier_2021_label_correction_v1.json -> v115,
et corrige les 20 libelles denormalises correspondants dans les deux cartes.

CE QUE CE SCRIPT FAIT, ET RIEN D'AUTRE. Il change UN nom, a 21 endroits :

    graphe v115                 7f0f9cc4  `name`         1 emplacement
    entity_section_map.json     7f0f9cc4  `name`         1 emplacement
    section_entities_map.json   7f0f9cc4  `entity_name`  19 emplacements

    « Favier 2021 — Bitcoin et la religion (La voie du Bitcoin) »
 -> « Favier 2021 — Bitcoin et la religion (podcast Parlons Bitcoin) »

Il ne cree aucune entite, aucune relation, ne touche aucun `authored`, aucun
attribut, aucun type, aucune SourceQuote, ne fusionne rien, n'annote aucun
doublon. Toute op qui n'est pas LE `SET_NAME` du lot fige est REFUSEE.

POURQUOI UNE SUBSTITUTION CIBLEE PLUTOT QU'UNE REGENERATION. Le test a blanc
du 2026-08-11 a etabli qu'AUCUN chemin de generation ne rafraichit ce champ :
`build_anchor_weights.py --apply` n'ecrit que `snippet_status` et
`direct_anchor_count`, `fix_dead_ids_in_section_map.py` ne touche le nom qu'en
reparant un identifiant mort, et `entity_section_map.json` n'a aucun script
ecrivain. Ces cartes ne sont pas desynchronisees malgre un pipeline de
synchronisation : elles portent un champ denormalise SANS mecanisme de
synchronisation. Une regeneration serait un no-op et laisserait les 20 lignes
fausses. Arbitrage de l'auteur du 2026-08-11 : substitution ciblee.

STRICT ET DEFENSIF, comme l'arbitrage l'exige. Aucun remplacement global :
chaque emplacement est FIGE ci-dessous, et le script refuse si la cardinalite,
l'identifiant ou l'ancienne valeur ne correspondent pas a l'etat attendu. Le
diff produit EST la preuve de confinement.

Usage:
    python3 scripts/make_v115_apply_favier_2021_label_correction.py --dry-run
    python3 scripts/make_v115_apply_favier_2021_label_correction.py
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
VERSION_SOURCE = 'v114'
VERSION_CIBLE = 'v115'
OPS_ATTENDUES = 1
PLAFOND_NOTE = 1200

ENTITE = '7f0f9cc4c27040a78115b0294fd9bfe1'
NOM_ANCIEN = 'Favier 2021 — Bitcoin et la religion (La voie du Bitcoin)'
NOM_NOUVEAU = 'Favier 2021 — Bitcoin et la religion (podcast Parlons Bitcoin)'

CARTE_ENTITES = 'entity_section_map.json'      # {entity_id: {name, ...}}
CARTE_SECTIONS = 'section_entities_map.json'   # {cle: {entities: [...]}}

# Les 19 emplacements de la seconde carte, FIGES. Un remplacement global
# aurait suffi a produire le meme resultat aujourd'hui — et aurait touche
# demain tout ce qui porterait la meme chaine, sans le dire.
SECTIONS_ATTENDUES = (
    'I.1', 'I.1.1', 'II.1', 'II.1.1', 'II.1.2', 'II.2.1', 'II.2.2', 'II.2.3',
    'III.1', 'III.1.1', 'conclu_aceph', 'conclu_boucs', 'conclu_infra',
    'conclu_resume', 'conclu_theo_mon', 'conclu_traduction',
    'intro_A', 'intro_B', 'intro_C',
)
ATTENDU_CARTE_ENTITES = 1
ATTENDU_CARTE_SECTIONS = len(SECTIONS_ATTENDUES)   # 19
ATTENDU_TOTAL_CARTES = ATTENDU_CARTE_ENTITES + ATTENDU_CARTE_SECTIONS   # 20


def echec(msg, code=CODE_DONNEES):
    famille = 'invocation' if code == CODE_INVOCATION else 'donnees'
    print(f'ECHEC ({famille}) : {msg}', file=sys.stderr)
    sys.exit(code)


def lire(chemin, quoi):
    if not os.path.exists(chemin):
        echec(f'{quoi} introuvable : {chemin}', CODE_INVOCATION)
    try:
        with open(chemin, encoding='utf-8') as f:
            return json.load(f)
    except (json.JSONDecodeError, OSError) as err:
        echec(f'{quoi} illisible : {err}', CODE_INVOCATION)


def valider_patch(patch):
    meta = patch.get('_meta')
    if not isinstance(meta, dict):
        echec('patch sans `_meta` exploitable')
    # La policy est LUE, jamais ecrite.
    if not str(meta.get('policy', '')).startswith(POLICY_CANDIDAT):
        echec('le patch ne porte pas la politique CANDIDATE attendue')
    if not isinstance(meta.get('arbitrage'), dict):
        echec('le patch ne porte pas son bloc `_meta.arbitrage` : ce lot n a '
              'ete autorise que par l arbitrage du 2026-08-11')

    ops = patch.get('ops')
    if not isinstance(ops, list) or len(ops) != OPS_ATTENDUES:
        echec(f'{len(ops or [])} op(s), {OPS_ATTENDUES} attendue — le lot est '
              'fige dans l applicateur')
    op = ops[0]
    if op.get('type') != 'SET_NAME':
        echec(f'op de type {op.get("type")!r} : ce lot n ecrit qu un SET_NAME. '
              'Aucune relation, aucun attribut, aucun type, aucune creation')
    if op.get('entityId') != ENTITE:
        echec(f'op visant {op.get("entityId")!r}, hors du lot fige')
    if op.get('value') != NOM_NOUVEAU:
        echec(f'op posant {op.get("value")!r} ; le lot approuve declare '
              f'{NOM_NOUVEAU!r} — la FORME a ete arbitree, elle ne se '
              'redecide pas dans un fichier de patch')
    declare = op.get('currentValue')
    if declare is not None and declare != NOM_ANCIEN:
        echec(f'le patch declare une valeur actuelle {declare!r} qui n est pas '
              f'{NOM_ANCIEN!r}')


def emplacements_cartes(carte_entites, carte_sections):
    """-> (emplacements de la 1re carte, de la 2nde) + leur valeur portee.

    Cette fonction LOCALISE et verifie la STRUCTURE ; elle ne juge pas de
    l'etat d'avancement — c'est `etat_du_lot` qui le fait, apres avoir vu
    les 20 emplacements. Les separer est le correctif du 2026-08-12 : la
    version precedente concluait « DEJA APPLIQUE » des la PREMIERE carte,
    sans avoir regarde les 19 autres. Un etat partiel — 1 corrige, 19
    anciens — aurait donc ete declare complet."""
    bloc = carte_entites.get(ENTITE)
    if not isinstance(bloc, dict):
        echec(f'{CARTE_ENTITES} : {ENTITE[:8]} absent ou mal forme')
    ailleurs = [k for k, b in carte_entites.items()
                if isinstance(b, dict) and b.get('name') == NOM_ANCIEN
                and k != ENTITE]
    if ailleurs:
        echec(f'{CARTE_ENTITES} : l ancien libelle est aussi porte par '
              f'{ailleurs} — une substitution ciblee ne peut pas trancher '
              'quelle entite le merite')

    trouves = []
    for cle, b in carte_sections.items():
        for i, ent in enumerate((b or {}).get('entities', [])):
            if ent.get('entity_id') == ENTITE:
                trouves.append((cle, i))
            elif ent.get('entity_name') == NOM_ANCIEN:
                echec(f'{CARTE_SECTIONS} : {cle}[{i}] porte l ancien libelle '
                      f'avec l identifiant {ent.get("entity_id")!r} — un '
                      'autre id porte le meme nom, la substitution ciblee '
                      'refuse de choisir')
    cles = sorted({c for c, _ in trouves})
    if cles != sorted(SECTIONS_ATTENDUES):
        manquantes = sorted(set(SECTIONS_ATTENDUES) - set(cles))
        surnumeraires = sorted(set(cles) - set(SECTIONS_ATTENDUES))
        echec(f'{CARTE_SECTIONS} : sections attendues != trouvees. '
              f'manquantes={manquantes} surnumeraires={surnumeraires}')
    if len(trouves) != ATTENDU_CARTE_SECTIONS:
        echec(f'{CARTE_SECTIONS} : {len(trouves)} emplacement(s), '
              f'{ATTENDU_CARTE_SECTIONS} attendus')
    return [ENTITE], trouves


def etat_du_lot(carte_entites, carte_sections, empl_s, graphe_source, cible):
    """-> ('PRE' | 'POST' | 'MIXTE', lignes de detail).

    TROIS etats, pas deux. Le lot porte 20 emplacements de carte ET un
    graphe ; les regarder TOUS avant de conclure est le correctif du
    2026-08-12. La lecon vient de C13 en v114 puis de la premiere version
    de ce script : un controle binaire « ancien / pas ancien » declare
    complet un etat partiel, et c'est le pire des trois cas — celui ou un
    rejeu ecrirait a cote sans que rien ne le signale."""
    porte = [(f'{CARTE_ENTITES}:{ENTITE[:8]}',
              (carte_entites.get(ENTITE) or {}).get('name'))]
    for cle, i in empl_s:
        porte.append((f'{CARTE_SECTIONS}:{cle}[{i}]',
                      carte_sections[cle]['entities'][i].get('entity_name')))

    anciens = [x for x, v in porte if v == NOM_ANCIEN]
    nouveaux = [x for x, v in porte if v == NOM_NOUVEAU]
    autres = [(x, v) for x, v in porte
              if v not in (NOM_ANCIEN, NOM_NOUVEAU)]
    detail = [f'{len(anciens)}/{ATTENDU_TOTAL_CARTES} a l ancienne valeur, '
              f'{len(nouveaux)} a la cible, {len(autres)} autre(s)']

    # Etat du graphe : la cible existe-t-elle, et vaut-elle EXACTEMENT le
    # resultat attendu ? Une v115 absente ou differente compte comme mixte.
    cible_existe = os.path.exists(cible)
    cible_conforme = False
    if cible_existe:
        attendu = copy.deepcopy(graphe_source)
        {x['id']: x for x in attendu['entities']}[ENTITE]['name'] = NOM_NOUVEAU
        with open(cible, encoding='utf-8') as f:
            reelle = json.load(f)
        a, b = signature_graphe(attendu), signature_graphe(reelle)
        cible_conforme = not diff_graphe(a, b)
        detail.append(f'{os.path.basename(cible)} present, conforme au diff '
                      f'canonique attendu : {cible_conforme}')
    else:
        detail.append(f'{os.path.basename(cible)} absent')

    if autres:
        detail += [f'  valeur inattendue en {x} : {v!r}' for x, v in autres[:5]]
        return 'MIXTE', detail
    if len(anciens) == ATTENDU_TOTAL_CARTES and not cible_existe:
        return 'PRE', detail
    if len(nouveaux) == ATTENDU_TOTAL_CARTES and cible_existe and cible_conforme:
        return 'POST', detail
    if anciens and nouveaux:
        detail.append(f'  emplacements encore anciens : {anciens[:6]}')
    return 'MIXTE', detail


def signature_graphe(g):
    entites = {}
    for e in g.get('entities', []):
        attrs = e.get('attributes') or {}
        entites[e['id']] = {
            'champs': {k: json.dumps(v, sort_keys=True, ensure_ascii=False)
                       for k, v in e.items() if k not in ('id', 'attributes')},
            'attributs': {k: json.dumps(v, sort_keys=True, ensure_ascii=False)
                          for k, v in attrs.items()},
        }
    return {
        'entites': entites,
        'ordre': [e['id'] for e in g.get('entities', [])],
        'relations': json.dumps(g.get('relations'), sort_keys=True,
                                ensure_ascii=False),
        'types': json.dumps(g.get('types'), sort_keys=True, ensure_ascii=False),
        'relation_types': json.dumps(g.get('relation_types'), sort_keys=True,
                                     ensure_ascii=False),
        'ops': json.dumps(g.get('ops'), sort_keys=True, ensure_ascii=False),
    }


def diff_graphe(avant, apres):
    ch = []
    for bloc in ('relations', 'types', 'relation_types', 'ops'):
        if avant[bloc] != apres[bloc]:
            ch.append(f'bloc `{bloc}` modifie')
    if avant['ordre'] != apres['ordre']:
        ch.append('ORDRE des entites modifie')
    a, b = set(avant['entites']), set(apres['entites'])
    for eid in sorted(a - b):
        ch.append(f'entite supprimee : {eid}')
    for eid in sorted(b - a):
        ch.append(f'entite creee : {eid}')
    for eid in sorted(a & b):
        x, y = avant['entites'][eid], apres['entites'][eid]
        for c in sorted(set(x['champs']) | set(y['champs'])):
            if x['champs'].get(c) != y['champs'].get(c):
                ch.append(f'{eid} : `{c}` modifie')
        for k in sorted(set(x['attributs']) | set(y['attributs'])):
            if x['attributs'].get(k) != y['attributs'].get(k):
                ch.append(f'{eid} : attribut `{k}` modifie')
    return ch


def diff_carte(avant, apres, etiquette):
    """Diff textuel ligne a ligne, pour prouver le confinement."""
    a = json.dumps(avant, ensure_ascii=False, indent=2, sort_keys=True).split('\n')
    b = json.dumps(apres, ensure_ascii=False, indent=2, sort_keys=True).split('\n')
    if len(a) != len(b):
        return [f'{etiquette} : le nombre de lignes change ({len(a)} -> '
                f'{len(b)}) — une substitution ciblee ne doit rien ajouter '
                'ni retirer']
    return [f'{etiquette} l.{i + 1} : {x.strip()} -> {y.strip()}'
            for i, (x, y) in enumerate(zip(a, b)) if x != y]


def main():
    ap = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--source', default=os.path.join(
        REPO, f'grc20-these-mael-rolland-{VERSION_SOURCE}.json'))
    ap.add_argument('--target', default=os.path.join(
        REPO, f'grc20-these-mael-rolland-{VERSION_CIBLE}.json'))
    ap.add_argument('--patch', default=os.path.join(
        REPO, 'patch_candidate_favier_2021_label_correction_v1.json'))
    ap.add_argument('--dry-run', action='store_true')
    args = ap.parse_args()

    patch = lire(args.patch, 'patch candidat')
    graphe = lire(args.source, 'graphe source')
    if (graphe.get('space') or {}).get('version') != VERSION_SOURCE:
        echec(f'le graphe source declare space.version = '
              f'{(graphe.get("space") or {}).get("version")!r} ; cet '
              f'applicateur lit {VERSION_SOURCE}', CODE_INVOCATION)
    valider_patch(patch)

    par_id = {e['id']: e for e in graphe.get('entities', [])}
    e = par_id.get(ENTITE)
    if e is None:
        echec(f'entite {ENTITE} absente du graphe source')
    if e.get('name') != NOM_ANCIEN:
        echec(f'{ENTITE[:8]} porte {e.get("name")!r}, le lot attendait '
              f'{NOM_ANCIEN!r} — le graphe a derive depuis l arbitrage')
    homonymes = [x['id'] for x in graphe['entities']
                 if x.get('name') == NOM_NOUVEAU and x['id'] != ENTITE]
    if homonymes:
        echec(f'le nom cible est deja porte par {homonymes} — renommer '
              'creerait un homonyme')

    chemin_ce = os.path.join(REPO, CARTE_ENTITES)
    chemin_cs = os.path.join(REPO, CARTE_SECTIONS)
    carte_e = lire(chemin_ce, CARTE_ENTITES)
    carte_s = lire(chemin_cs, CARTE_SECTIONS)
    # Les deux cartes ne se terminent PAS par un saut de ligne. Ecrire le
    # notre en ajoutait un, et le diff portait alors deux lignes de plus par
    # fichier — une modification collateral, minuscule mais reelle, sur des
    # fichiers ou la consigne est « rien d autre que les substitutions ».
    fins = {}
    for chemin in (chemin_ce, chemin_cs):
        with open(chemin, encoding='utf-8') as f:
            fins[chemin] = '\n' if f.read().endswith('\n') else ''
    empl_e, empl_s = emplacements_cartes(carte_e, carte_s)

    # --- classification en TROIS etats, avant toute autre verification ---
    etat, detail = etat_du_lot(carte_e, carte_s, empl_s, graphe, args.target)
    print(f'etat du lot : {etat}')
    for d in detail:
        print(f'  {d}')
    if etat == 'POST':
        print('\nDEJA APPLIQUE — les 20 emplacements portent la cible et '
              f'{os.path.basename(args.target)} vaut exactement le diff '
              'canonique attendu. Rien a rejouer ; lire son etat dans le '
              'graphe, la file vivante puis le ledger.')
        return 0
    if etat != 'PRE':
        echec('etat MIXTE ou INCOHERENT : le lot n est ni entierement a '
              'appliquer ni entierement applique. C est le cas le plus '
              'dangereux — un rejeu ecrirait a cote sans qu aucune collision '
              'ne le signale. Instruire a la main.\n  ' + '\n  '.join(detail))

    print(f'\nlot fige : 1 SET_NAME + {ATTENDU_TOTAL_CARTES} libelles '
          'denormalises\n')
    print(f'  {NOM_ANCIEN!r}\n  -> {NOM_NOUVEAU!r}\n')
    print(f'  graphe               : {ENTITE[:8]} `name`')
    print(f'  {CARTE_ENTITES:26s}: {len(empl_e)} emplacement `name`')
    print(f'  {CARTE_SECTIONS:26s}: {len(empl_s)} emplacements `entity_name`')

    if os.path.realpath(args.target) == os.path.realpath(args.source):
        echec('la cible est le graphe SOURCE', CODE_INVOCATION)
    m_v = re.search(r'-(v\d+)\.json$', os.path.basename(args.target))
    if not m_v or m_v.group(1) != VERSION_CIBLE:
        echec(f'cet applicateur produit {VERSION_CIBLE} et rien d autre',
              CODE_INVOCATION)

    # ---------- mutation en memoire ----------
    avant_g = signature_graphe(graphe)
    resultat = copy.deepcopy(graphe)
    {x['id']: x for x in resultat['entities']}[ENTITE]['name'] = NOM_NOUVEAU
    apres_g = signature_graphe(resultat)

    neuf_e = copy.deepcopy(carte_e)
    neuf_e[ENTITE]['name'] = NOM_NOUVEAU
    neuf_s = copy.deepcopy(carte_s)
    for cle, i in empl_s:
        neuf_s[cle]['entities'][i]['entity_name'] = NOM_NOUVEAU

    # ---------- preuves separees ----------
    ch_g = diff_graphe(avant_g, apres_g)
    attendu_g = [f'{ENTITE} : `name` modifie']
    print(f'\n--- PREUVE 1 : changement canonique ({len(ch_g)} changement) ---')
    for c in ch_g:
        print(f'  {c}')
    if ch_g != attendu_g:
        echec('le diff du graphe ne vaut pas exactement le renommage attendu :'
              f'\n  {ch_g}')

    d_e = diff_carte(carte_e, neuf_e, CARTE_ENTITES)
    d_s = diff_carte(carte_s, neuf_s, CARTE_SECTIONS)
    print(f'\n--- PREUVE 2 : {len(d_e) + len(d_s)} ligne(s) denormalisee(s) ---')
    for x in d_e + d_s:
        print(f'  {x[:150]}')
    if len(d_e) != ATTENDU_CARTE_ENTITES:
        echec(f'{CARTE_ENTITES} : {len(d_e)} ligne(s) changee(s), '
              f'{ATTENDU_CARTE_ENTITES} attendue')
    if len(d_s) != ATTENDU_CARTE_SECTIONS:
        echec(f'{CARTE_SECTIONS} : {len(d_s)} ligne(s) changee(s), '
              f'{ATTENDU_CARTE_SECTIONS} attendues')
    for x in d_e + d_s:
        if NOM_ANCIEN not in x or NOM_NOUVEAU not in x:
            echec(f'une ligne changee ne porte pas la substitution attendue :'
                  f'\n  {x[:200]}')

    # ---------- preuve 3 : rien d autre ----------
    reste_e = sum(1 for b in neuf_e.values()
                  if isinstance(b, dict) and b.get('name') == NOM_ANCIEN)
    reste_s = sum(1 for b in neuf_s.values()
                  for x in (b or {}).get('entities', [])
                  if x.get('entity_name') == NOM_ANCIEN)
    inchangees_s = sum(len((b or {}).get('entities', []))
                       for b in neuf_s.values()) - ATTENDU_CARTE_SECTIONS
    print('\n--- PREUVE 3 : absence de tout autre effet ---')
    print(f'  entites du graphe        : {len(graphe["entities"])} -> '
          f'{len(resultat["entities"])}')
    print(f'  relations du graphe      : {len(graphe["relations"])} -> '
          f'{len(resultat["relations"])}')
    print(f'  ancien libelle restant   : {reste_e + reste_s}')
    print(f'  lignes de carte intactes : {inchangees_s} '
          f'(sur {inchangees_s + ATTENDU_CARTE_SECTIONS})')
    if reste_e or reste_s:
        echec('l ancien libelle subsiste quelque part')
    if len(resultat['entities']) != len(graphe['entities']) or \
            len(resultat['relations']) != len(graphe['relations']):
        echec('le nombre d entites ou de relations a change')

    if args.dry_run:
        print('\n--dry-run : tous les controles ont tourne, y compris les '
              "trois preuves. Rien n a ete ecrit.")
        return 0

    espace = resultat.setdefault('space', {})
    espace['version'] = VERSION_CIBLE
    espace['entity_count'] = len(resultat['entities'])
    espace['relation_count'] = len(resultat['relations'])
    tete = (
        "V115 — 1 libelle corrige, et rien d autre. La fiche 7f0f9cc4 "
        "attribuait l item Favier 2021 au blog « La voie du Bitcoin » alors "
        "que l unique entree Favier 2021 de la bibliographie "
        "(assets/MD/07_bibliographie.md:472) donne un podcast "
        "parlonsbitcoin.com ; « La voie du Bitcoin » est l editeur de "
        "l entree :474 (Tulipes), qui a sa propre fiche b84f59ac. L identite "
        "de l oeuvre n etait pas en cause, seul son support. Applique apres "
        "arbitrage de l auteur du 2026-08-11 (forme A). Les 20 libelles "
        "denormalises des cartes d ancrage sont corrigés dans le meme lot par "
        "substitution ciblee : aucun chemin de generation ne rafraichit ce "
        "champ. Aucune entite creee, aucune relation, aucun authored, aucun "
        "attribut, aucun type, aucune fusion, aucune SourceQuote. Voir "
        "docs/audits/grc20-v115-favier-2021-label-application.md. ")
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
        echec(f'space.note fait {len(espace["note"])} caracteres pour un '
              f'plafond de {PLAFOND_NOTE}')

    for chemin, donnees in ((args.target, resultat), (chemin_ce, neuf_e),
                            (chemin_cs, neuf_s)):
        temporaire = chemin + '.tmp'
        try:
            with open(temporaire, 'w', encoding='utf-8') as f:
                json.dump(donnees, f, ensure_ascii=False, indent=2)
                f.write(fins.get(chemin, ''))
            os.replace(temporaire, chemin)
        except OSError as err:
            if os.path.exists(temporaire):
                os.unlink(temporaire)
            echec(f'ecriture impossible : {err}')
        print(f'ecrit : {os.path.relpath(chemin, REPO)}')
    return 0


if __name__ == '__main__':
    sys.exit(main())
