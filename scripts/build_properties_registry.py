#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Construit grc20-properties-registry-v1.json : le registre des cles
d'attributs d'entites du graphe GRC-20 courant.

Pourquoi ce registre : aucun endroit du depot ne declare les cles
d'attributs. `grc20-publish.mjs` emet la cle brute comme identifiant de
propriete (« a mapper vers un ID de propriete si defini dans le Space »),
ce qui bloque toute publication propre. Ce fichier donne a chaque cle un
identifiant stable, un type de valeur, et un statut d'usage constatable.

Revision du 2026-08-07 (arbitrage de Mael, lot 1 Q2) : la source n'est
plus codee en dur — defaut = le graphe le plus recent du depot,
surchargeable par --source. patch_19 n'est applique en memoire QUE si le
graphe source ne l'a pas deja integre (detection par les donnees : la
presence des cles que ce patch fait disparaitre) — depuis v110 il est
integre, l'etape est donc sans objet et sautee. Les trois cles retirees
par patch_19 restent inscrites au registre comme HISTORIQUE explicite
(status='deprecated', count 0 sur le graphe courant, comptes historiques
v109 dans notes) : une trace d'audit, pas un dechet — c'est l'arbitrage
Q2-b. Un mode --check regenere en memoire et compare au fichier commite
(controle de fraicheur, appele par la CI — arbitrage Q5-a).

Rejouable : meme sortie octet pour octet a re-execution (aucun
horodatage variable ; la date de `_meta` est figee au jour de la
derniere revision du registre).

Usage :
    python3 scripts/build_properties_registry.py
    python3 scripts/build_properties_registry.py --source grc20-these-mael-rolland-v110.json
    python3 scripts/build_properties_registry.py --check
"""
import argparse
import collections
import glob
import hashlib
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from grc20_commun import graphe_le_plus_recent  # noqa: E402

PATCH = 'patch_19_attribute_normalisation.json'
SORTIE = 'grc20-properties-registry-v1.json'
DATE_AUDIT = '2026-08-07'

# Renommages/absorptions portes par patch_19 : la cle depreciee → la cle
# qui la remplace. C'est la seule connaissance non deduite du graphe.
SUPERSEDED_BY = {
    'nomEnquete': 'interviewName',
    'centralArgument': 'central_argument',
    'conceptSource': 'concept_source',
}

# HISTORIQUE explicite (arbitrage Q2-b) : quand une cle de SUPERSEDED_BY a
# entierement disparu du graphe source (patch_19 integre), son entree
# subsiste au registre avec ces donnees historiques, mesurees sur v109 —
# la derniere version qui les portait.
HISTORIQUE_DEPRECIEES = {
    'nomEnquete': {'valueType': 'TEXT', 'language': 'fr',
                   'domain': ['PrimarySource'], 'count_v109': 23},
    'centralArgument': {'valueType': 'TEXT', 'language': 'fr',
                        'domain': ['Concept'], 'count_v109': 1},
    'conceptSource': {'valueType': 'TEXT', 'language': 'fr',
                      'domain': ['Method'], 'count_v109': 1},
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
    'pages': "Plage de pages bibliographique (domaine Reference). Collision "
             "lexicale avec l'API pypdf (`lecteur.pages`, `self.pages`) : "
             "scripts/audit_section_page_start.py nomme la chaine sans "
             "jamais lire cet attribut du graphe — il est desormais EXCLU "
             "de `readBy` par EXCLUSIONS_READ_BY, et `status` retrouve sa "
             "valeur juste.",
    'note': "Collision lexicale avec des noms de colonnes de CSV et des "
            "variables locales homonymes. scripts/audit_section_page_start.py "
            "est a ce titre EXCLU de `readBy` par EXCLUSIONS_READ_BY ; "
            "d'autres faux positifs du balayage textuel peuvent subsister.",
    'sourcePages': "Source de derivation de `sourcePage` (premier numero de "
                   "page) ; porte en plus les pages multiples.",
}

# Faux positifs du balayage LEXICAL : le fichier nomme la chaine sans jamais
# lire l'attribut du graphe. `pages` est capte par l'API pypdf
# (`lecteur.pages`, `self.pages`), `note` par des noms de colonnes de CSV.
# Toute entree ajoutee ici doit avoir ete verifiee dans le fichier vise.
EXCLUSIONS_READ_BY = {
    'pages': {'scripts/audit_section_page_start.py'},
    # classify_date_evidence.py ne lit jamais `dateSource` : il joint des CSV
    # entre eux. La chaine n'apparait que dans sa docstring, ou elle enonce
    # l'arbitrage qui a motive le script. Verifie : occurrence unique, l.5.
    'dateSource': {'scripts/classify_date_evidence.py'},
    # make_v112 ne lit NI `duplicateOf` NI `reviewStatus` : il les nomme dans
    # CLES_INTERDITES pour les REFUSER, et les cite en prose pour dire qu'il
    # n'annote aucune identite. Ne pas les exclure ferait dire a `readBy` le
    # contraire exact de ce que fait le script — et sur les deux cles dont le
    # non-ecrit est precisement l'objet de cette version. Verifie ligne a
    # ligne : aucune lecture du graphe sur ces deux cles.
    'duplicateOf': {'scripts/make_v112_apply_chronology_dates_patch.py'},
    'reviewStatus': {'scripts/make_v112_apply_chronology_dates_patch.py'},
    # build_patch_queue_inventory.py ne lit ces deux cles dans AUCUN graphe :
    # « page_start » n'y est qu'un LIBELLE DE FAMILLE de la table FAMILLES
    # (le patch page_start), et « type » y designe le champ d'operation d'un
    # patch (`op.get('type')`), homonyme de l'attribut de graphe. Verifie
    # occurrence par occurrence dans le fichier vise.
    'page_start': {'scripts/build_patch_queue_inventory.py'},
    'type': {'scripts/build_patch_queue_inventory.py'},
    # build_patch_queue_governance.py lit le `_meta` des PATCHS, jamais le
    # graphe : `description` et `status` y sont des champs de carte d'identite
    # de patch, `note` un nom de colonne du CSV produit. Verifie occurrence par
    # occurrence — le script ne touche aucun attribut d'entite.
    'description': {'scripts/build_patch_queue_governance.py'},
    'status': {'scripts/build_patch_queue_governance.py'},
    'note': {'scripts/audit_section_page_start.py',
             'scripts/build_patch_queue_governance.py'},
}

# Scripts d'ENUMERATION, exclus en bloc du balayage `readBy` — meme motif que
# l'auto-exclusion de ce generateur. Un inventaire dont l'objet est de
# parcourir une famille entiere de cles les nomme TOUTES par construction : les
# compter comme lecteurs viderait `status` de son sens. Mesure : sans cette
# exclusion, `audit_chronology_dates.py` faisait basculer 31 cles de
# 'editorial' a 'structural' d'un coup (`closed`, `foundedYear`, `timeStart`,
# `dateInterview`…) alors que RIEN dans le site ni dans la chaine de
# publication ne les lit. L'instrument de mesure contaminait la mesure.
# N'ajouter ici qu'un script dont l'enumeration est le PROPOS, jamais un
# consommateur reel d'attributs.
#
# Chemins RELATIFS AU DEPOT, comme EXCLUSIONS_READ_BY — pas des noms de
# fichier : un basename exclurait aussi un homonyme range ailleurs, qui lui
# pourrait etre un vrai lecteur.
SCRIPTS_ENUMERANTS = frozenset({
    'scripts/audit_chronology_dates.py',
})


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
    se marquerait lui-meme comme lecteur. Meme raison pour les autres scripts
    d'ENUMERATION (SCRIPTS_ENUMERANTS) : un inventaire dont l'objet est de
    parcourir toutes les cles d'une famille les nomme toutes par construction,
    et les compterait comme « lues » alors que rien n'en depend."""
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
        if not any(x in f for x in exclus)
        and os.path.abspath(f) != moi
        and os.path.relpath(f, repo).replace(os.sep, '/')
        not in SCRIPTS_ENUMERANTS))


def read_by(cles, repo):
    """Pour chaque cle : fichiers qui la nomment. Le critere est lexical et
    en forme de code — cle entre guillemets ('k', "k", `k`) ou en acces de
    propriete (.k) — pour eviter les faux positifs de la prose des
    commentaires ; il peut encore surcompter les identifiants generiques
    (type, description, language, ...), ce que `notes` signale.

    Les faux positifs constates fichier par fichier sont retires apres
    detection via EXCLUSIONS_READ_BY : une exclusion nominative et
    verifiable, pas un assouplissement du critere."""
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
        exclus = EXCLUSIONS_READ_BY.get(k, ())
        res[k] = sorted(f for f, t in textes.items()
                        if rx.search(t) and f not in exclus)
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
    p.add_argument('--source', default=None,
                   help="graphe source (defaut : le plus recent du depot)")
    p.add_argument('--check', action='store_true',
                   help="regenere en memoire et compare au registre commite "
                        "— echoue (code 1) s'ils divergent (fraicheur, CI)")
    args = p.parse_args(argv)

    chemin_source = args.source or graphe_le_plus_recent(args.repo)
    if not os.path.isabs(chemin_source):
        candidat = os.path.join(args.repo, chemin_source)
        if os.path.exists(candidat):
            chemin_source = candidat
    if not os.path.exists(chemin_source):
        print(f"ECHEC : graphe source introuvable : {chemin_source}",
              file=sys.stderr)
        return 2
    source_nom = os.path.basename(chemin_source)
    with open(chemin_source, encoding='utf-8') as fh:
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

    # patch_19 : applique en memoire SEULEMENT si le graphe source ne l'a
    # pas deja integre. Detection par les donnees, pas par le numero de
    # version : les cles que ce patch fait disparaitre sont-elles encore
    # portees ? (v109 : oui ; v110 et suivants : non, patch integre par
    # make_v110 — l'appliquer une seconde fois serait sans objet.)
    patch_integre = not any(k in avant for k in SUPERSEDED_BY)
    apres = avant
    if not patch_integre:
        chemin_patch = os.path.join(args.repo, PATCH)
        if not os.path.exists(chemin_patch):
            print(f"ECHEC : {PATCH} introuvable — le registre decrirait "
                  f"l'etat AVANT patch en se donnant pour l'etat apres.",
                  file=sys.stderr)
            return 2
        copie = json.loads(json.dumps(entites))
        with open(chemin_patch, encoding='utf-8') as fh:
            appliquer_patch(copie, json.load(fh))
        apres = collections.defaultdict(list)
        for e in copie:
            for k, v in attrs(e).items():
                apres[k].append(v)

    # les cles depreciees participent au balayage readBy meme quand elles
    # ont quitte le graphe : un code qui les nomme encore doit se voir.
    lecteurs = read_by(set(avant) | set(SUPERSEDED_BY), args.repo)

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

    # HISTORIQUE explicite (arbitrage Q2-b) : les cles retirees du graphe
    # par patch_19 restent inscrites, comme trace d'audit.
    if patch_integre:
        for k in sorted(HISTORIQUE_DEPRECIEES):
            if k in avant:
                continue
            h = HISTORIQUE_DEPRECIEES[k]
            entrees.append({
                'key': k,
                'id': cle_id(k),
                'valueType': h['valueType'],
                'language': h['language'],
                'domain': list(h['domain']),
                'count': 0,
                'status': 'deprecated',
                'readBy': lecteurs.get(k, []),
                'vocabulary': None,
                'derivedFrom': None,
                'notes': (f"Cle historique, retiree du graphe par patch_19 "
                          f"(integre depuis v110) : remplacee par "
                          f"`{SUPERSEDED_BY[k]}`. Comptes historiques v109 : "
                          f"{h['count_v109']} porteur(s), domaine "
                          f"{'/'.join(h['domain'])}. Conservee au registre "
                          f"comme trace d'audit (arbitrage Q2-b du "
                          f"2026-08-07)."),
                'supersededBy': SUPERSEDED_BY[k],
            })

    entrees.sort(key=lambda x: (-x['count'], x['key']))

    registre = {
        '_meta': {
            'source_graph': source_nom,
            'date': DATE_AUDIT,
            'generated_by': 'scripts/build_properties_registry.py',
            'id_scheme': "md5('grc20-property-v1|' + key), 32 hexa minuscules",
            'entry_count': len(entrees),
            'conventions': (
                "Le registre decrit le graphe source tel qu'il est : "
                "`count` et `domain` sont mesures sur lui. Si le graphe "
                "source n'a pas encore integre "
                "patch_19_attribute_normalisation.json (detection par les "
                "donnees), `valueType`, `language` et `vocabulary` sont "
                "calcules apres application en memoire de ce patch (etat "
                "normatif) ; sinon l'etape est sans objet. Les trois cles "
                "que ce patch a retirees restent inscrites avec "
                "status='deprecated', count 0, `supersededBy` nommant la "
                "cle qui les remplace et leurs comptes historiques v109 "
                "dans `notes` — trace d'audit explicite (arbitrage Q2-b du "
                "2026-08-07). `language` est la langue "
                "majoritaire des options (null si aucune ou egalite). "
                "`vocabulary` est la liste close des valeurs si <= 8 valeurs "
                "distinctes ET >= 10 porteurs, sinon null. `status` vaut "
                "'structural' si la cle est nommee dans un fichier de code "
                "du depot (*.html, *.js, *.mjs, scripts/ — critere lexical : "
                "cle citee entre guillemets ou en acces de propriete ; ce "
                "script est exclu du balayage car il nomme les cles "
                "depreciees, et les scripts d'ENUMERATION le sont pour la "
                "meme raison, cf. SCRIPTS_ENUMERANTS — un inventaire qui "
                "parcourt une famille entiere de cles les nomme toutes par "
                "construction et les rendrait 'structural' sans que rien "
                "n'en depende ; les faux positifs constates fichier par "
                "fichier sont retires apres detection, cf. "
                "EXCLUSIONS_READ_BY dans le generateur), sinon 'editorial'. "
                "`readBy` liste ces "
                "fichiers. `derivedFrom` n'est pose que si la derivation se "
                "verifie dans 100 % des cas sur le graphe."
            ),
        },
        'entries': entrees,
    }
    sortie = os.path.join(args.repo, SORTIE)
    if args.check:
        if not os.path.exists(sortie):
            print(f"ECHEC : registre commite introuvable : {sortie}",
                  file=sys.stderr)
            return 2
        with open(sortie, encoding='utf-8') as fh:
            disque = json.load(fh)
        if disque != registre:
            print("--check : le registre commite N'EST PAS la sortie du "
                  "generateur sur le graphe courant — regenerer avec "
                  "scripts/build_properties_registry.py (fraicheur, "
                  "arbitrage Q5-a).", file=sys.stderr)
            return 1
        print("--check : le registre est a jour "
              f"({len(entrees)} entrees, source {source_nom}).")
        return 0
    with open(sortie, 'w', encoding='utf-8') as fh:
        json.dump(registre, fh, ensure_ascii=False, indent=2)
        fh.write('\n')
    print('ecrit %s (%d entrees, source %s)' % (sortie, len(entrees),
                                                source_nom))
    stats = collections.Counter(e['status'] for e in entrees)
    print('statuts :', dict(sorted(stats.items())))
    return 0


if __name__ == '__main__':
    sys.exit(main())
