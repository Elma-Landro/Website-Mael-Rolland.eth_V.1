#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Construit grc20-properties-registry-v1.json : le registre des cles
d'attributs d'entites de grc20-these-mael-rolland-v109.json.

Pourquoi ce registre : aucun endroit du depot ne declare les cles
d'attributs. `grc20-publish.mjs` emet la cle brute comme identifiant de
propriete (« a mapper vers un ID de propriete si defini dans le Space »),
ce qui bloque toute publication propre. Ce fichier donne a chaque cle un
identifiant stable, un type de valeur, et un statut d'usage constatable.

Le registre decrit v109 TEL QU'IL EST, avec une nuance assumee :
patch_19_attribute_normalisation.json (depose, non applique) corrige des
VALEURS, pas des cles — sauf deux renommages (centralArgument →
central_argument, conceptSource → concept_source) et une deduplication
(nomEnquete, absorbee par interviewName). Ces trois cles sont donc gardees
avec status='deprecated' et un champ `supersededBy` qui nomme la cle
survivante. Pour toutes les autres, `valueType`, `language` et
`vocabulary` sont calcules APRES application en memoire de patch_19 :
c'est l'etat normatif vers lequel le graphe converge. `count` et `domain`
restent ceux de v109 tel quel.

Rejouable : meme sortie octet pour octet a re-execution (aucun
horodatage variable ; la date de `_meta` est figee au jour de l'audit).

Usage :
    python3 scripts/build_properties_registry.py
    python3 scripts/build_properties_registry.py --repo .
"""
import argparse
import collections
import glob
import hashlib
import json
import os
import re
import sys

SOURCE = 'grc20-these-mael-rolland-v109.json'
PATCH = 'patch_19_attribute_normalisation.json'
SORTIE = 'grc20-properties-registry-v1.json'
DATE_AUDIT = '2026-08-06'

# Renommages/absorptions portes par patch_19 : la cle depreciee → la cle
# qui la remplace. C'est la seule connaissance non deduite du graphe.
SUPERSEDED_BY = {
    'nomEnquete': 'interviewName',
    'centralArgument': 'central_argument',
    'conceptSource': 'concept_source',
}

# Anomalies constatees, notees sans etre tranchees. Le registre NE fusionne
# rien : il documente.
NOTES = {
    'count': "Collision lexicale avec un identifiant generique frequent en code — "
             "les correspondances readBy sont a lire avec prudence.",

    'description': "Collision avec le champ d'enveloppe `description` de "
                   "l'entite GRC-20 et avec la propriete systeme homonyme de "
                   "grc20-publish.mjs ; les occurrences code comptees dans "
                   "readBy designent le plus souvent l'enveloppe, pas cet "
                   "attribut.",
    'language': "Collision avec la cle d'options `language` de l'enveloppe "
                "de valeur ; readBy surestime donc son usage reel.",
    'type': "Collision avec le champ `type` de l'enveloppe de valeur GRC-20 "
            "et avec le champ `type` des ops ; readBy surestime son usage "
            "reel.",
    'sourceType': "Doublon semantique non tranche avec `regimeDePreuve` "
                  "(66/66 co-portes, valeurs correlees) — non fusionne, "
                  "decision humaine requise.",
    'regimeDePreuve': "Doublon semantique non tranche avec `sourceType` "
                      "(66/66 co-portes, valeurs correlees) — non fusionne, "
                      "decision humaine requise.",
    'order': "Cle mixte : 45 valeurs NUMBER, 4 valeurs TEXT entieres "
             "('0'..'3') hors perimetre du repli tout-TEXT de patch_19 "
             "(point 3) — a convertir lors d'un arbitrage ulterieur.",
    'chapter': "patch_19 replie chap1/chap2/chap3/I sur Chapitre I/II/III ; "
               "« intro » est conserve tel quel (graphie majoritaire : 68 "
               "contre 1 « Introduction générale ») ; les formes composites "
               "(« Chapitre II / Chapitre III », etc.) restent intouchees.",
    'organisateur': "patch_19 supprime 1 valeur vide ; la cle reste active "
                    "(26 porteurs).",
    'sourcePages': "Source de derivation de `sourcePage` (premier numero de "
                   "page) ; porte en plus les pages multiples.",
}


def cle_id(key):
    # usedforsecurity=False : identifiant deterministe, pas de la cryptographie
    # (Python >= 3.9 ; la toolchain du depot est 3.11).
    return hashlib.md5(('grc20-property-v1|' + key).encode('utf-8'),
                       usedforsecurity=False).hexdigest()


def attrs(e):
    a = e.get('attributes')
    return a if isinstance(a, dict) else {}


def appliquer_patch(entites, patch):
    """Applique les ops de patch_19 sur une copie en memoire.

    Un patch malforme doit se VOIR : les ops de type inconnu et celles qui
    visent une entite absente sont comptees et affichees, pas avalees."""
    par_id = {e['id']: e for e in entites}
    inconnues, absentes = 0, 0
    for op in patch.get('ops', []):
        e = par_id.get(op.get('entityId'))
        if e is None:
            absentes += 1
            continue
        a = e.get('attributes')
        if not isinstance(a, dict):
            a = e['attributes'] = {}
        if op['type'] == 'SET_ATTRIBUTE':
            a[op['attributeId']] = op['value']
        elif op['type'] == 'DELETE_ATTRIBUTE':
            a.pop(op['attributeId'], None)
        else:
            inconnues += 1
    if inconnues or absentes:
        print(f"  ATTENTION patch : {inconnues} op(s) de type inconnu, "
              f"{absentes} op(s) vers une entite absente", file=sys.stderr)


def fichiers_code(repo):
    """Fichiers de code scannes pour `status`/`readBy` : *.html, *.js, *.mjs
    du depot entier (hors node_modules et assets/MD) plus tout scripts/.
    Ce script-ci est exclu : il nomme les cles depreciees dans SUPERSEDED_BY et
    se marquerait lui-meme comme lecteur."""
    fs = []
    for pat in ('**/*.html', '**/*.js', '**/*.mjs'):
        fs += glob.glob(os.path.join(repo, pat), recursive=True)
    for pat in ('**/*.py', '**/*.mjs', '**/*.js'):
        fs += glob.glob(os.path.join(repo, 'scripts', pat), recursive=True)
    exclus = (os.sep + 'node_modules' + os.sep,
              os.sep + os.path.join('assets', 'MD') + os.sep)
    moi = os.path.abspath(__file__)
    return sorted(set(
        f for f in fs
        if not any(x in f for x in exclus) and os.path.abspath(f) != moi))


def read_by(cles, repo):
    """Pour chaque cle : fichiers qui la nomment. Le critere est lexical et
    en forme de code — cle entre guillemets ('k', "k", `k`) ou en acces de
    propriete (.k) — pour eviter les faux positifs de la prose des
    commentaires ; il peut encore surcompter les identifiants generiques
    (type, description, language, ...), ce que `notes` signale."""
    textes = {}
    for f in fichiers_code(repo):
        try:
            with open(f, encoding='utf-8', errors='replace') as fh:
                textes[os.path.relpath(f, repo).replace(os.sep, '/')] = fh.read()
        except OSError:
            continue
    res = {}
    for k in cles:
        e = re.escape(k)
        rx = re.compile(
            r'''(['"`])''' + e + r'''\1'''
            r'''|\.''' + e + r'''(?![A-Za-z0-9_$])''')
        res[k] = sorted(f for f, t in textes.items() if rx.search(t))
    return res


def langue_majoritaire(valeurs):
    c = collections.Counter(
        (v.get('options') or {}).get('language')
        for v in valeurs if (v.get('options') or {}).get('language'))
    if not c:
        return None
    top = c.most_common(2)
    if len(top) > 1 and top[0][1] == top[1][1]:
        return None
    return top[0][0]


def type_majoritaire(valeurs, repli=None):
    # `valeurs` peut etre vide (cle videe par patch_19) : dans ce cas le type
    # normatif est celui d'AVANT le patch, pas un IndexError.
    c = collections.Counter(v.get('type') for v in valeurs)
    if not c:
        return type_majoritaire(repli) if repli else None
    return c.most_common(1)[0][0]


def vocabulaire(valeurs, count):
    distincts = {v.get('value') for v in valeurs}
    if count >= 10 and len(distincts) <= 8:
        return sorted(distincts, key=lambda x: (type(x).__name__, str(x)))
    return None


def derive_source_page(entites):
    """`sourcePage` derive de `sourcePages` seulement si le premier numero
    de `sourcePages` correspond dans 100 % des cas."""
    total = ok = 0
    for e in entites:
        a = attrs(e)
        sp = a.get('sourcePage')
        if sp is None:
            continue
        total += 1
        sps = a.get('sourcePages')
        if sps is None:
            continue
        m = re.search(r'\d+', str(sps.get('value', '')))
        v = sp.get('value')
        try:
            v = int(str(v).strip())
        except (TypeError, ValueError):
            continue
        if m and int(m.group(0)) == v:
            ok += 1
    return total > 0 and ok == total


def derive_rauchs_count(entites):
    """`rauchs2016SegmentsCount` derive de `rauchs2016Segments` seulement si
    le compte egale le nombre de segments dans 100 % des cas."""
    total = ok = 0
    for e in entites:
        a = attrs(e)
        c = a.get('rauchs2016SegmentsCount')
        if c is None:
            continue
        total += 1
        s = a.get('rauchs2016Segments')
        if s is None:
            continue
        nseg = len([x for x in str(s.get('value', '')).split(',') if x.strip()])
        try:
            if int(str(c.get('value')).strip()) == nseg:
                ok += 1
        except (TypeError, ValueError):
            continue
    return total > 0 and ok == total


def main(argv=None):
    p = argparse.ArgumentParser(description="Registre des cles d'attributs.")
    p.add_argument('--repo', default=os.path.dirname(
        os.path.dirname(os.path.abspath(__file__))))
    args = p.parse_args(argv)

    with open(os.path.join(args.repo, SOURCE), encoding='utf-8') as fh:
        g = json.load(fh)
    entites = g['entities']

    nom_type = {t['id']: t.get('name', t['id']) for t in g.get('types', [])}

    # etat v109 tel quel
    avant = collections.defaultdict(list)   # cle → [valeur, ...]
    domaines = collections.defaultdict(set)  # cle → {nom de type porteur}
    for e in entites:
        for k, v in attrs(e).items():
            avant[k].append(v)
            for t in (e.get('types') or []):
                domaines[k].add(nom_type.get(t, t))

    # etat apres patch_19 (en memoire, sur copie)
    chemin_patch = os.path.join(args.repo, PATCH)
    apres = avant
    if not os.path.exists(chemin_patch):
        print(f"ECHEC : {PATCH} introuvable — le registre decrirait l'etat "
              f"AVANT patch en se donnant pour l'etat apres.", file=sys.stderr)
        return 2
    if os.path.exists(chemin_patch):
        copie = json.loads(json.dumps(entites))
        with open(chemin_patch, encoding='utf-8') as fh:
            appliquer_patch(copie, json.load(fh))
        apres = collections.defaultdict(list)
        for e in copie:
            for k, v in attrs(e).items():
                apres[k].append(v)

    lecteurs = read_by(set(avant), args.repo)

    derivations = {}
    if derive_source_page(entites):
        derivations['sourcePage'] = ['sourcePages']
    if derive_rauchs_count(entites):
        derivations['rauchs2016SegmentsCount'] = ['rauchs2016Segments']

    entrees = []
    for k in avant:
        count = len(avant[k])
        deprecie = k in SUPERSEDED_BY and not apres.get(k)
        # cle depreciee : valeurs de v109 tel quel ; sinon etat post-patch
        valeurs = avant[k] if deprecie else apres[k]
        if deprecie:
            statut = 'deprecated'
        elif lecteurs[k]:
            statut = 'structural'
        else:
            statut = 'editorial'
        entree = {
            'key': k,
            'id': cle_id(k),
            'valueType': type_majoritaire(valeurs),
            'language': langue_majoritaire(valeurs),
            'domain': sorted(domaines[k]),
            'count': count,
            'status': statut,
            'readBy': lecteurs[k],
            'vocabulary': vocabulaire(valeurs, count),
            'derivedFrom': derivations.get(k),
            'notes': NOTES.get(k, ''),
        }
        if deprecie:
            entree['supersededBy'] = SUPERSEDED_BY[k]
            complement = ("Depreciee par patch_19 (deposee, non appliquee) : "
                          "remplacee par `%s`." % SUPERSEDED_BY[k])
            entree['notes'] = (entree['notes'] + ' ' + complement).strip()
        entrees.append(entree)

    entrees.sort(key=lambda x: (-x['count'], x['key']))

    registre = {
        '_meta': {
            'source_graph': SOURCE,
            'date': DATE_AUDIT,
            'generated_by': 'scripts/build_properties_registry.py',
            'id_scheme': "md5('grc20-property-v1|' + key), 32 hexa minuscules",
            'entry_count': len(entrees),
            'conventions': (
                "Le registre decrit v109 tel qu'il est : `count` et `domain` "
                "sont mesures sur le graphe source. `valueType`, `language` "
                "et `vocabulary` sont calcules apres application en memoire "
                "de patch_19_attribute_normalisation.json (etat normatif) ; "
                "les trois cles que ce patch fait disparaitre restent "
                "inscrites avec status='deprecated' et `supersededBy` nommant "
                "la cle qui les remplace. `language` est la langue "
                "majoritaire des options (null si aucune ou egalite). "
                "`vocabulary` est la liste close des valeurs si <= 8 valeurs "
                "distinctes ET >= 10 porteurs, sinon null. `status` vaut "
                "'structural' si la cle est nommee dans un fichier de code "
                "du depot (*.html, *.js, *.mjs, scripts/ — critere lexical : "
                "cle citee entre guillemets ou en acces de propriete ; ce "
                "script est exclu du balayage car il nomme les cles "
                "depreciees), sinon 'editorial'. `readBy` liste ces "
                "fichiers. `derivedFrom` n'est pose que si la derivation se "
                "verifie dans 100 % des cas sur le graphe."
            ),
        },
        'entries': entrees,
    }
    sortie = os.path.join(args.repo, SORTIE)
    with open(sortie, 'w', encoding='utf-8') as fh:
        json.dump(registre, fh, ensure_ascii=False, indent=2)
        fh.write('\n')
    print('ecrit %s (%d entrees)' % (sortie, len(entrees)))
    stats = collections.Counter(e['status'] for e in entrees)
    print('statuts :', dict(sorted(stats.items())))
    return 0


if __name__ == '__main__':
    sys.exit(main())
