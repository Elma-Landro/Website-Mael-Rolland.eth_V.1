#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Applique patch_candidate_bibliography_authorship_v1.json et produit v114.

CE QUE CE SCRIPT FAIT, ET RIEN D'AUTRE. Il ajoute QUATRE relations `authored`,
et aucune autre :

    53525938…  Jacques Favier        -authored->  e19babe5…  Bitcoin, la monnaie acephale
    53525938…  Jacques Favier        -authored->  b84f59ac…  Tulipes
    53525938…  Jacques Favier        -authored->  7f0f9cc4…  Bitcoin et la religion
    ec901513…  Adli Takkal Bataille  -authored->  e19babe5…  Bitcoin, la monnaie acephale

Il ne cree aucune entite, ne modifie aucun nom, aucun type, aucun attribut,
aucune relation existante. Il ne fusionne rien, n'annote aucun doublon, ne
touche aucune SourceQuote. Toute op qui n'est pas un `ADD_RELATION` du lot fige
est REFUSEE, pas ignoree.

POURQUOI CES QUATRE RELATIONS. v113 a retype six fiches d'auteur en `Person`.
Quatre pointent vers leur oeuvre par `authored` ; deux non — Favier et Takkal
Bataille — alors que leurs oeuvres EXISTENT dans le graphe. Chaque paternite
est attestee par une entree de `assets/MD/07_bibliographie.md` qui nomme
l'auteur ET l'oeuvre (l.472, 474, 476), verifiee mot pour mot par
`scripts/build_bibliography_authorship_support.py`.

CE QUI EST DELIBEREMENT ABSENT. La cinquieme paire instruite — DeNardis vers
`e0b40d91` — est REFUSEE : cette fiche decrit la meme entree bibliographique
que `2272e5b8`, qui porte deja son `authored`. En poser un second graverait le
doublon en oeuvre distincte. Elle est nommee dans REFUSEES et le script echoue
si le patch la contient.

ET LE NOM FAUTIF N'EST PAS CORRIGE. La fiche `7f0f9cc4` s'annonce « (La voie du
Bitcoin) » alors que la bibliographie donne un podcast parlonsbitcoin.com.
L'editeur est faux, la paternite ne l'est pas. Corriger le nom serait un
RENOMMAGE, explicitement hors perimetre (arbitrage 3 du 2026-08-10) : ce
script refuse toute modification de `name`.

LE LOT EST FIGE ICI, VALEURS COMPRISES. Pas seulement les identifiants : les
noms attendus des deux extremites, l'id ET le nom du type de relation, et la
preuve bibliographique attendue sont tous reproduits dans LOT_APPROUVE. Un
patch retouche entre l'arbitrage et l'application ne peut donc pas faire
ecrire autre chose — lecon de la revue de v112, ou figer les seuls ids
laissait reecrire la valeur cible.

LE CONTROLE D'APRES EST EXHAUSTIF. Les entites sont comparees champ de tete
par champ de tete et attribut par attribut ; les relations sont comparees
element par element. Le script n'ecrit que si le diff complet vaut EXACTEMENT
quatre relations AJOUTEES, zero supprimee, zero modifiee, et zero changement
d'entite.

Usage:
    python3 scripts/make_v114_apply_bibliography_authorship_relations.py --dry-run
    python3 scripts/make_v114_apply_bibliography_authorship_relations.py
"""
import argparse
import copy
import hashlib
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from grc20_commun import REPO  # noqa: E402

CODE_DONNEES, CODE_INVOCATION = 1, 2

POLICY_CANDIDAT = 'CANDIDATE — NOT APPLIED — AUTHOR ARBITRATION REQUIRED'
VERSION_SOURCE = 'v113'
VERSION_CIBLE = 'v114'
OPS_ATTENDUES = 4
PLAFOND_NOTE = 1200

ID_AUTHORED = '2d3f43441ee747dda4172f0954a9fadd'
NOM_AUTHORED = 'authored'
# Sel de derivation des identifiants de relation. Meme motif que make_v107 :
# un id DETERMINISTE rend l'applicateur rejouable a l'identique, et --dry-run
# decrit exactement ce qu'une execution reelle ecrirait.
SEL = 'grc20-bibliography-authorship-v1'

# Le lot approuve par l'auteur le 2026-08-10 (arbitrage 1), reproduit EN
# ENTIER : ids des deux extremites, noms attendus de chacune, id ET nom du type
# de relation, preuve bibliographique attendue.
LOT_APPROUVE = (
    {'auteur': '53525938440543a5af359337eeab9823',
     'nom_auteur': 'Jacques Favier',
     'oeuvre': 'e19babe53a3d4f0291ed683b3118e0ef',
     'nom_oeuvre': 'Favier & Takkal Bataille 2017 — Bitcoin la monnaie acéphale',
     'preuve': 'assets/MD/07_bibliographie.md:476'},
    {'auteur': '53525938440543a5af359337eeab9823',
     'nom_auteur': 'Jacques Favier',
     'oeuvre': 'b84f59ace9b6403c88067c46af4c7582',
     'nom_oeuvre': 'Favier 2017 — Tulipes (blog La voie du Bitcoin)',
     'preuve': 'assets/MD/07_bibliographie.md:474'},
    {'auteur': '53525938440543a5af359337eeab9823',
     'nom_auteur': 'Jacques Favier',
     'oeuvre': '7f0f9cc4c27040a78115b0294fd9bfe1',
     'nom_oeuvre': 'Favier 2021 — Bitcoin et la religion (La voie du Bitcoin)',
     'preuve': 'assets/MD/07_bibliographie.md:472'},
    {'auteur': 'ec901513fae144a0a350e798b0351c6d',
     'nom_auteur': 'Adli Takkal Bataille',
     'oeuvre': 'e19babe53a3d4f0291ed683b3118e0ef',
     'nom_oeuvre': 'Favier & Takkal Bataille 2017 — Bitcoin la monnaie acéphale',
     'preuve': 'assets/MD/07_bibliographie.md:476'},
)
PAIRES_APPROUVEES = frozenset((x['auteur'], x['oeuvre']) for x in LOT_APPROUVE)
AUTEURS_APPROUVES = frozenset(x['auteur'] for x in LOT_APPROUVE)
OEUVRES_APPROUVEES = frozenset(x['oeuvre'] for x in LOT_APPROUVE)

# Instruite, puis REFUSEE — nommement, pour qu'un patch elargi la reintroduise
# a visage decouvert plutot qu'en silence.
REFUSEES = {
    ('5fc4278b78704f6c92c3744e2654518a',
     'e0b40d91bb424defaa9acf37536f339e'):
        "DeNardis -> « DeNardis & Musiani 2014 — Governance by Infrastructure » : "
        "cette fiche decrit la MEME entree bibliographique (l.394) que 2272e5b8, "
        "qui porte deja l authored de DeNardis. Poser un second authored "
        "graverait le doublon en oeuvre distincte. A instruire comme doublon, "
        "pas comme paternite manquante.",
}


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


def identifiant(depuis, vers):
    return hashlib.md5(
        f'{SEL}|rel|{depuis}|{NOM_AUTHORED}|{vers}'.encode('utf-8')).hexdigest()


def valider_patch(patch):
    """-> liste des paires (auteur, oeuvre), dans l ordre du lot fige."""
    meta = patch.get('_meta')
    if not isinstance(meta, dict):
        echec('patch sans `_meta` exploitable')
    # La policy est LUE, jamais ecrite : ce script n ouvre le patch qu en
    # lecture. Un candidat qui aurait perdu son marquage n est plus le fichier
    # arbitre, et C03 l aurait deja refuse.
    if not str(meta.get('policy', '')).startswith(POLICY_CANDIDAT):
        echec('le patch ne porte pas la politique CANDIDATE attendue — '
              'policy absente, tronquee ou reecrite')
    if not isinstance(meta.get('arbitrage'), dict):
        echec('le patch ne porte pas son bloc `_meta.arbitrage` : ce lot n a '
              'ete autorise que par l arbitrage du 2026-08-10, et un patch qui '
              'ne le porte plus n est pas celui qui a ete arbitre')

    ops = patch.get('ops')
    if not isinstance(ops, list):
        echec('patch sans liste `ops`')
    if len(ops) != OPS_ATTENDUES:
        echec(f'{len(ops)} op(s) dans le patch, {OPS_ATTENDUES} attendues — le '
              'lot est fige dans l applicateur ; un patch elargi depuis '
              'l arbitrage doit etre re-arbitre, pas applique')

    vues = []
    for i, op in enumerate(ops):
        if not isinstance(op, dict):
            echec(f'op #{i} n est pas un objet')
        if op.get('type') != 'ADD_RELATION':
            echec(f'op #{i} de type {op.get("type")!r} : ce lot n ecrit que des '
                  'ADD_RELATION. Aucune entite, aucun attribut, aucun type, '
                  'aucun nom, aucune suppression')
        depuis, vers = op.get('from'), op.get('to')
        if op.get('relationTypeId') != ID_AUTHORED:
            echec(f'op #{i} : relationTypeId {op.get("relationTypeId")!r}, '
                  f'seul {ID_AUTHORED} (« {NOM_AUTHORED} ») est autorise')
        nom_declare = op.get('relationTypeName')
        if nom_declare is not None and nom_declare != NOM_AUTHORED:
            echec(f'op #{i} : relationTypeName {nom_declare!r} incoherent avec '
                  f'l id, qui designe « {NOM_AUTHORED} »')
        if depuis == vers:
            echec(f'op #{i} : relation de {depuis} vers lui-meme')
        if (depuis, vers) in REFUSEES:
            echec(f'op #{i} : cette paire est REFUSEE. {REFUSEES[(depuis, vers)]}')
        if depuis not in AUTEURS_APPROUVES:
            echec(f'op #{i} : auteur {depuis!r} hors du lot fige — seuls '
                  f'{sorted(AUTEURS_APPROUVES)} sont approuves')
        if vers not in OEUVRES_APPROUVEES:
            echec(f'op #{i} : oeuvre {vers!r} hors du lot fige')
        if (depuis, vers) not in PAIRES_APPROUVEES:
            echec(f'op #{i} : la paire ({depuis[:8]}, {vers[:8]}) n est pas au '
                  'lot approuve — auteur et oeuvre y figurent chacun, mais pas '
                  'ensemble. Une paternite ne se recombine pas')
        if (depuis, vers) in vues:
            echec(f'op #{i} : paire ({depuis[:8]}, {vers[:8]}) proposee deux '
                  'fois — le graphe porterait deux fois le meme fait')
        vues.append((depuis, vers))

    if set(vues) != PAIRES_APPROUVEES:
        manquantes = sorted(PAIRES_APPROUVEES - set(vues))
        echec(f'le patch ne couvre pas le lot approuve ; manque(nt) : '
              f'{manquantes}')
    return vues


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
        'ordre_entites': [e['id'] for e in graphe.get('entities', [])],
        # Les relations sont comparees UNE PAR UNE, en gardant l'ordre : un
        # ajout doit se voir comme un ajout, jamais comme un remplacement.
        'relations': [json.dumps(r, sort_keys=True, ensure_ascii=False)
                      for r in graphe.get('relations', [])],
        'types': json.dumps(graphe.get('types'), sort_keys=True,
                            ensure_ascii=False),
        'relation_types': json.dumps(graphe.get('relation_types'),
                                     sort_keys=True, ensure_ascii=False),
        'ops': json.dumps(graphe.get('ops'), sort_keys=True, ensure_ascii=False),
    }


def diff_exhaustif(avant, apres):
    """-> (changements hors relations, relations ajoutees, supprimees)."""
    changements = []
    for bloc in ('types', 'relation_types', 'ops'):
        if avant[bloc] != apres[bloc]:
            changements.append(f'bloc `{bloc}` modifie')
    if avant['ordre_entites'] != apres['ordre_entites']:
        changements.append('ORDRE des entites modifie')
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

    # Le PREFIXE doit etre intact : les relations existantes gardent leur
    # place et leur contenu, les nouvelles sont ajoutees a la fin. Comparer
    # des ensembles aurait laisse passer une reecriture compensee.
    n = len(avant['relations'])
    if apres['relations'][:n] != avant['relations'][:n]:
        for i, (x, y) in enumerate(zip(avant['relations'],
                                       apres['relations'][:n])):
            if x != y:
                changements.append(
                    f'relation #{i} MODIFIEE en place : {x[:90]} -> {y[:90]}')
    ajoutees = apres['relations'][n:] if len(apres['relations']) > n else []
    supprimees = avant['relations'][len(apres['relations']):] \
        if len(apres['relations']) < n else []
    return changements, ajoutees, supprimees


def main():
    ap = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--source', default=os.path.join(
        REPO, f'grc20-these-mael-rolland-{VERSION_SOURCE}.json'))
    ap.add_argument('--target', default=os.path.join(
        REPO, f'grc20-these-mael-rolland-{VERSION_CIBLE}.json'))
    ap.add_argument('--patch', default=os.path.join(
        REPO, 'patch_candidate_bibliography_authorship_v1.json'))
    ap.add_argument('--dry-run', action='store_true')
    args = ap.parse_args()

    patch = lire(args.patch, 'patch candidat')
    graphe = lire(args.source, 'graphe source')
    if (graphe.get('space') or {}).get('version') != VERSION_SOURCE:
        echec(f'le graphe source declare space.version = '
              f'{(graphe.get("space") or {}).get("version")!r} ; cet '
              f'applicateur lit {VERSION_SOURCE}', CODE_INVOCATION)

    paires = valider_patch(patch)
    par_id = {e['id']: e for e in graphe.get('entities', [])}
    types_relation = {t['id'] for t in graphe.get('relation_types', [])}
    if ID_AUTHORED not in types_relation:
        echec(f'le type de relation {ID_AUTHORED} est absent du graphe source')
    existantes = {(r.get('from'), r.get('to'), r.get('type'))
                  for r in graphe.get('relations', [])}
    ids_relations = {r.get('id') for r in graphe.get('relations', [])
                     if r.get('id')}

    print(f'lot fige : {OPS_ATTENDUES} relation(s) « {NOM_AUTHORED} »\n')
    nouvelles = []
    for approuve in LOT_APPROUVE:
        depuis, vers = approuve['auteur'], approuve['oeuvre']
        for role, eid, nom_attendu in (
                ('auteur', depuis, approuve['nom_auteur']),
                ('oeuvre', vers, approuve['nom_oeuvre'])):
            e = par_id.get(eid)
            if e is None:
                echec(f'{role} {eid} absent du graphe source')
            if e.get('name') != nom_attendu:
                echec(f'{eid} : nom {e.get("name")!r} dans le graphe, le lot '
                      f'attendait {nom_attendu!r} — le graphe a derive depuis '
                      'l arbitrage, re-arbitrage requis')
        if (depuis, vers, ID_AUTHORED) in existantes:
            echec(f'la relation {depuis[:8]} -{NOM_AUTHORED}-> {vers[:8]} '
                  'existe DEJA dans le graphe source : la reposer creerait un '
                  'doublon silencieux, sans collision de nom pour le signaler')
        rid = identifiant(depuis, vers)
        if rid in ids_relations:
            echec(f'l identifiant derive {rid} est deja porte par une relation '
                  'du graphe')
        ids_relations.add(rid)
        nouvelles.append({'id': rid, 'type': ID_AUTHORED,
                          'from': depuis, 'to': vers, 'attributes': []})
        print(f'  {depuis[:8]}  {approuve["nom_auteur"]}')
        print(f'      -{NOM_AUTHORED}-> {vers[:8]}  '
              f'{approuve["nom_oeuvre"][:52]}')
        print(f'      preuve : {approuve["preuve"]}')

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
    resultat['relations'].extend(copy.deepcopy(nouvelles))
    apres = signature(resultat)
    changements, ajoutees, supprimees = diff_exhaustif(avant, apres)

    attendues = {json.dumps(r, sort_keys=True, ensure_ascii=False)
                 for r in nouvelles}
    print(f'\ndiff exhaustif : {len(changements)} changement(s) hors relations, '
          f'{len(ajoutees)} ajoutee(s), {len(supprimees)} supprimee(s)')
    for c in changements:
        print(f'  {c}')
    if changements:
        echec("changement(s) hors relations detecte(s), rien n est ecrit :\n  "
              + '\n  '.join(changements))
    if supprimees:
        echec(f'{len(supprimees)} relation(s) supprimee(s) : ce lot n en '
              'retire aucune')
    if len(ajoutees) != OPS_ATTENDUES:
        echec(f'{len(ajoutees)} relation(s) ajoutee(s), {OPS_ATTENDUES} '
              'attendues')
    if set(ajoutees) != attendues:
        echec('les relations ajoutees ne sont pas celles du lot fige')
    attendu_total = len(graphe['relations']) + OPS_ATTENDUES
    if len(resultat['relations']) != attendu_total:
        echec(f'{len(resultat["relations"])} relations en sortie, '
              f'{attendu_total} attendues')
    if len(resultat['entities']) != len(graphe['entities']):
        echec('le nombre d entites a change')

    if args.dry_run:
        print('\n--dry-run : tous les controles ont tourne, y compris le diff '
              "exhaustif. Rien n a ete ecrit.")
        return 0

    espace = resultat.setdefault('space', {})
    espace['version'] = VERSION_CIBLE
    espace['entity_count'] = len(resultat['entities'])
    espace['relation_count'] = len(resultat['relations'])
    tete = (
        "V114 — 4 relations `authored` ajoutees, et rien d autre. Jacques "
        "Favier (53525938) vers ses 3 oeuvres e19babe5, b84f59ac et 7f0f9cc4 ; "
        "Adli Takkal Bataille (ec901513) vers l ouvrage co-signe e19babe5. Les "
        "deux fiches etaient des Person depuis v113 sans lien vers leur propre "
        "oeuvre. Chaque paternite est attestee dans "
        "assets/MD/07_bibliographie.md (l.472, 474, 476). Applique apres "
        "arbitrage de l auteur du 2026-08-10. Aucune entite creee ou modifiee, "
        "aucun attribut, aucun type, aucun nom, aucune fusion, aucun "
        "duplicateOf, aucune SourceQuote, aucune relation existante touchee. "
        "DeNardis -> e0b40d91 reste REFUSEE (doublon de 2272e5b8), et le nom "
        "fautif de 7f0f9cc4 reste a corriger hors de ce lot. Voir "
        "docs/audits/grc20-v114-bibliography-authorship-application.md. ")
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
