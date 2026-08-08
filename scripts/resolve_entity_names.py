#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Resolveur deterministe de noms d'entites contre le graphe GRC-20 — LECTURE SEULE.

POURQUOI CE SCRIPT EXISTE. Un patch externe a declare « Polycentric
Governance » introuvable dans le graphe. L'entite a444085b la porte
pourtant, mot pour mot, dans son attribut `nameEn` — mais le resolveur qui
avait rendu ce verdict n'interrogeait que `name`. Le graphe v110 porte 115
`nameEn`, 77 `labelEn`, 70 `labelFr` et 30 `aliases` : autant de
denominations que le graphe declare LUI-MEME et qu'un resolveur qui les
ignore transforme en faux negatifs. Une table d'alias externe existe aussi
(`docs/audits/data/entity-alias-table-v1.csv`) : elle reste utile, mais
comme couche COMPLEMENTAIRE pour ce que le graphe ne porte pas lui-meme —
jamais avant lui.

CE QUE CE SCRIPT NE FAIT PAS : il n'ecrit rien dans le graphe, ne cree
aucune entite, n'applique aucun patch. Seul `--report-json` ecrit, a
l'endroit demande. Stdlib uniquement, sortie deterministe (tris explicites
partout, aucun horodatage).

=====================================================================
LA REGLE DE RESOLUTION — ordre STRICT, premier rang qui matche l'emporte
=====================================================================
Toutes les comparaisons se font sur la cle normalisee (voir plus bas), et
toutes sont des egalites EXACTES sur cette cle : aucune approximation
n'entre jamais dans une resolution.

  rang 1  `name`         nom canonique du graphe            confiance haute
  rang 2  `nameEn`       nom anglais declare par le graphe  confiance haute
  rang 3  `labelEn`      libelle anglais declare            confiance haute
  rang 4  `labelFr`      libelle francais declare           confiance haute
  rang 5  `aliases`      alias declare par le graphe        confiance moyenne
  rang 6  `alias-table`  table externe, lignes de confiance
                         haute ou moyenne UNIQUEMENT        confiance de la ligne
  sinon   `not-found`

Le parcours s'arrete au PREMIER rang qui produit au moins un candidat. Il
ne « retombe » pas au rang suivant en cas d'ambiguite : si deux entites
matchent au meme rang, le statut est `ambiguous`, les deux sont listees, et
rien n'est tranche — arbitrer serait une decision d'auteur, pas de script.

Chaque resolution rend le rang qui a matche (`match_rule`), la chaine
exactement matchee (`matched_string`) et un niveau de confiance
(`confidence`).

POURQUOI `aliases` EST GRADE « moyenne » ET LES AUTRES « haute ». Les
rangs 1-4 sont des denominations : une entite a un nom, un nom anglais, un
libelle. Le rang 5 est heterogene — dans v110 il melange gloses
parenthetiques (« Gouvernance duale (CM) »), corrections orthographiques
(« Shaoling Fry ») et variantes multiples separees par « | ». Un match
exact y reste une equivalence editoriale, pas une denomination. Le rang 6
porte la confiance declaree par la ligne du CSV.

POURQUOI LES LIGNES `basse` DE LA TABLE SONT EXCLUES. Elles couvrent
precisement les collisions et les traductions interpretatives : les 30
lignes `basse` de la table v1 portent toutes soit un `collision_with`
renseigne (15), soit une equivalence que la table elle-meme demande de ne
jamais resoudre automatiquement (« ALIAS AMBIGU […] ne jamais resoudre
automatiquement sur cette chaine »). Les admettre ferait de ce resolveur
exactement la machine a faux positifs que la table cherche a eviter.
`--confidences` permet de mesurer l'effet d'un autre choix, jamais de le
rendre par defaut.

LA CONFIANCE NE SUFFIT PAS : LES INTERDICTIONS EXPLICITES DE LA TABLE.
Filtrer sur `confidence` seul laisserait passer des lignes que la table
INTERDIT elle-meme de resoudre automatiquement, dans sa colonne `notes` —
et elles ne sont pas toutes `basse` : dans la table v1, 11 lignes `haute`
et 2 lignes `moyenne` portent « ne jamais resoudre sur ce seul jeton »
(BIP, DAO, DEX, EIP, IMF, PoS, PoW, SegWit, STS, UASF, CM) ou « cible
arbitree a la main, ne pas resoudre automatiquement » (« Absence de
gouvernance », « Bourse d'échange »). Trois d'entre elles sont employees
telles quelles par le lot SourceQuote : les resoudre automatiquement serait
faire dire a la table le contraire de ce qu'elle ecrit.

Le rang 6 ecarte donc toute ligne dont `notes` porte le marqueur
« ne jamais/pas resoudre » (detection deterministe : regex
`ne (jamais|pas) resoudre` sur les notes normalisees). Le nom concerne
n'est PAS resolu : il ressort `not-found`, en portant le champ
`table_interdictions` qui nomme la ligne ecartee, sa cible et sa note —
pour qu'un humain tranche en connaissance de cause plutot que de decouvrir
un faux positif plus tard. `--ignore-table-interdictions` permet de MESURER
ce que ces lignes changeraient ; ce n'est jamais un mode d'exploitation.

=====================================================================
NORMALISATION — une seule, appliquee des deux cotes
=====================================================================
`normalise_cle` = `grc20_commun.normalise_doux` (minuscules, accents
deplies, apostrophe U+2019 -> droite) + repli des AUTRES apostrophes
typographiques (U+2018, U+02BC, U+2032, U+00B4) + reduction des espaces
(`split()`/`join`, ce qui absorbe aussi l'espace insecable U+00A0 et
l'espace fine U+202F).

La ponctuation est GARDEE, contrairement a `normalise_appariement`. C'est
delibere : « ASIC (matériel de minage) » et « ASIC » doivent rester deux
chaines distinctes — c'est la table d'alias, avec sa confiance et ses
`collision_with`, qui dit si l'une renvoie a l'autre, pas une normalisation
qui les ecraserait en silence.

=====================================================================
FORME REELLE DE `aliases` DANS v110 — constatee, pas supposee
=====================================================================
Les 30 valeurs sont des CHAINES uniques (`{type: TEXT, value: <str>}`),
jamais des listes. Trois portent le separateur « | » (« Double dépense
(double spend) | Problème de double dépense »). Le script decoupe sur
« | » et sur lui seul.

Il ne decoupe NI sur la virgule NI sur les parentheses, bien qu'une valeur
soit visiblement une enumeration a la virgule (fb0eeba9 : « Blocksize War,
bloc size debate, guerre des blocs »). Motif : la virgule est aussi interne
a des denominations legitimes (« Limitation de taille des blocs (1 Mo,
Bitcoin) »), et decouper sur la parenthese fabriquerait des formes courtes
que personne n'a declarees. Limite assumee et mesurable : « Blocksize War »
seul ne resout pas au rang 5. C'est exactement le genre de manque que la
table externe couvre — et elle le couvre.

=====================================================================
LE FUZZY EST UNE PISTE, JAMAIS UNE RESOLUTION
=====================================================================
Quand aucun rang ne matche, le script liste les denominations les plus
proches (difflib, ratio sur la cle normalisee, meilleur ratio par entite,
tri (-ratio, entity_id, denomination)). Ces candidats sont estampilles
`PISTE` : ils ne sont jamais promus en resolution, ne comptent dans aucun
total de resolutions, et n'existent que pour qu'un humain tranche. C'est la
lecon de l'incident « Florence Dufy » : une approximation plausible engravee
sans verification est une erreur, pas une resolution.

=====================================================================
ENTREES ACCEPTEES PAR --from-json (detection dans cet ordre)
=====================================================================
  1. une LISTE de chaines                     -> les chaines
  2. une LISTE d'objets                       -> leur champ `name`
  3. un OBJET portant une liste sous l'une des cles `names`,
     `entity_names`, `quote_supports_entity_names`  -> cette liste
     (chaines ou objets a champ `name`)
  4. un OBJET portant `operations` (inventaire SourceQuote) -> les
     `operations[].target_entities[].name`, dans l'ordre du fichier
Toute autre forme est une erreur d'invocation (code 2), jamais un silence.

CODES DE SORTIE : 0 = la resolution a tourne (meme avec des `not-found` :
un nom introuvable est un resultat, pas une panne) ; 2 = erreur
d'invocation (graphe/table/entree illisible ou de forme inattendue).

Usage:
    python3 scripts/resolve_entity_names.py --name "Polycentric Governance"
    python3 scripts/resolve_entity_names.py --from-json noms.json --no-alias-table
    python3 scripts/resolve_entity_names.py --name X --report-json /tmp/r.json
"""
import argparse
import collections
import csv
import difflib
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from grc20_commun import REPO, graphe_le_plus_recent, normalise_doux  # noqa: E402

CODE_INVOCATION = 2

# Rangs portes par le graphe lui-meme, dans l'ordre d'interrogation.
RANGS_GRAPHE = ('name', 'nameEn', 'labelEn', 'labelFr', 'aliases')
RANG_TABLE = 'alias-table'
RANGS = RANGS_GRAPHE + (RANG_TABLE,)

CONFIANCE_PAR_RANG = {
    'name': 'haute',
    'nameEn': 'haute',
    'labelEn': 'haute',
    'labelFr': 'haute',
    'aliases': 'moyenne',   # cf. docstring : rang heterogene
}

SEPARATEUR_ALIAS = '|'
TABLE_DEFAUT = os.path.join(REPO, 'docs', 'audits', 'data',
                            'entity-alias-table-v1.csv')
CONFIANCES_ADMISES = ('haute', 'moyenne')   # jamais `basse` — cf. docstring

# Marqueur d'interdiction porte par la colonne `notes` de la table. Teste
# sur les notes NORMALISEES (donc sans accents et en minuscules), ce qui
# couvre « resoudre » comme « résoudre ». Cf. docstring.
MARQUEUR_INTERDICTION = re.compile(r'ne (?:jamais|pas) resoudre')

# Apostrophes typographiques que `normalise_doux` ne replie pas.
APOSTROPHES = ('‘', 'ʼ', '′', '´')

CLES_LISTES_NOMS = ('names', 'entity_names', 'quote_supports_entity_names')

FUZZY_SEUIL_DEFAUT = 0.60
FUZZY_MAX_DEFAUT = 5


def echec_invocation(msg):
    print(f"ECHEC (invocation) : {msg}", file=sys.stderr)
    sys.exit(CODE_INVOCATION)


def lire_json(chemin, quoi):
    if not chemin or not os.path.exists(chemin):
        echec_invocation(f"{quoi} introuvable : {chemin}")
    try:
        with open(chemin, encoding='utf-8') as f:
            return json.load(f)
    except (json.JSONDecodeError, OSError, UnicodeDecodeError) as err:
        echec_invocation(f"{quoi} illisible : {err}")


def normalise_cle(s):
    """La cle de comparaison, appliquee des deux cotes. Cf. docstring."""
    s = str(s or '')
    for a in APOSTROPHES:
        s = s.replace(a, "'")
    return ' '.join(normalise_doux(s).split())


def valeur_texte(attribut):
    """La valeur d'un attribut GRC-20, qu'il soit {type, value} ou brut."""
    if isinstance(attribut, dict):
        return str(attribut.get('value') or '')
    return str(attribut or '')


def variantes_alias(valeur):
    """Decoupe la chaine `aliases` sur « | » — et sur lui seul (docstring)."""
    return [x.strip() for x in valeur.split(SEPARATEUR_ALIAS) if x.strip()]


def denominations_du_graphe(graphe):
    """-> [(rang, cle_normalisee, chaine_source, entity_id)], tri deterministe.

    Une entite peut apparaitre plusieurs fois : une ligne par denomination
    qu'elle declare, sur chacun des cinq rangs du graphe.
    """
    sorties = []
    for e in graphe.get('entities') or []:
        eid = e.get('id')
        if not eid:
            continue
        attrs = e.get('attributes') or {}
        for rang in RANGS_GRAPHE:
            brut = e.get('name') if rang == 'name' else attrs.get(rang)
            if brut is None:
                continue
            valeur = valeur_texte(brut)
            if not valeur.strip():
                continue
            morceaux = (variantes_alias(valeur) if rang == 'aliases'
                        else [valeur.strip()])
            for morceau in morceaux:
                cle = normalise_cle(morceau)
                if cle:
                    sorties.append((rang, cle, morceau, eid))
    sorties.sort(key=lambda x: (RANGS.index(x[0]), x[1], x[3], x[2]))
    return sorties


def index_du_graphe(denominations):
    """-> {rang: {cle: [(entity_id, chaine_source), ...]}} — listes triees."""
    index = {rang: collections.defaultdict(list) for rang in RANGS_GRAPHE}
    for rang, cle, source, eid in denominations:
        paires = index[rang][cle]
        if (eid, source) not in paires:
            paires.append((eid, source))
    for rang in index:
        for cle in index[rang]:
            index[rang][cle].sort()
    return index


def interdite(notes):
    """La ligne porte-t-elle l'interdiction explicite de la table ? (docstring)"""
    return bool(MARQUEUR_INTERDICTION.search(normalise_cle(notes)))


def charge_table_alias(chemin, confiances, honorer_interdictions=True):
    """-> (index, interdits, compteurs).

    `index`    : {cle: [(entity_id, alias, confiance, alias_kind)]} exploitable ;
    `interdits`: {cle: [(entity_id, alias, confiance, notes)]} — lignes de
                 confiance admise mais que la table interdit de resoudre ;
                 elles ne resolvent rien, elles sont RAPPORTEES.
    Le CSV est ';'-separe, en-tete obligatoire.
    """
    if not os.path.exists(chemin):
        echec_invocation(f"table d'alias introuvable : {chemin}")
    index = collections.defaultdict(list)
    interdits = collections.defaultdict(list)
    compteurs = collections.Counter()
    try:
        with open(chemin, encoding='utf-8', newline='') as f:
            lecteur = csv.DictReader(f, delimiter=';')
            requis = {'entity_id', 'alias', 'confidence'}
            if not requis.issubset(set(lecteur.fieldnames or [])):
                echec_invocation(
                    f"table d'alias sans les colonnes requises "
                    f"{sorted(requis)} : {chemin}")
            for ligne in lecteur:
                compteurs['lues'] += 1
                confiance = (ligne.get('confidence') or '').strip()
                if confiance not in confiances:
                    continue
                eid = (ligne.get('entity_id') or '').strip()
                alias = (ligne.get('alias') or '').strip()
                cle = normalise_cle(alias)
                if not eid or not cle:
                    continue
                notes = (ligne.get('notes') or '').strip()
                if honorer_interdictions and interdite(notes):
                    compteurs['interdites'] += 1
                    entree = (eid, alias, confiance, notes)
                    if entree not in interdits[cle]:
                        interdits[cle].append(entree)
                    continue
                compteurs['retenues'] += 1
                entree = (eid, alias, confiance,
                          (ligne.get('alias_kind') or '').strip())
                if entree not in index[cle]:
                    index[cle].append(entree)
    except (OSError, UnicodeDecodeError, csv.Error) as err:
        echec_invocation(f"table d'alias illisible : {err}")
    for cle in index:
        index[cle].sort()
    for cle in interdits:
        interdits[cle].sort()
    return index, interdits, compteurs


def carte_entites(graphe):
    """-> ({id: entite}, {id: nom_de_type})."""
    entites = {e['id']: e for e in (graphe.get('entities') or []) if e.get('id')}
    nom_type = {t['id']: t.get('name') or t['id']
                for t in (graphe.get('types') or []) if t.get('id')}
    return entites, nom_type


def decrit(eid, entites, nom_type):
    e = entites.get(eid) or {}
    return {
        'entity_id': eid,
        'entity_name': e.get('name'),
        'entity_types': sorted(nom_type.get(t, t) for t in (e.get('types') or [])),
    }


def pistes_fuzzy(cle, denominations, entites, nom_type, seuil, maximum):
    """Les denominations du graphe les plus proches — PISTES, pas resolutions.

    Meilleur ratio par entite ; tri (-ratio, entity_id, denomination) pour
    que deux executions rendent exactement la meme liste.
    """
    if not cle:
        return []
    apparieur = difflib.SequenceMatcher()
    apparieur.set_seq2(cle)
    meilleur = {}
    for rang, cle_deno, source, eid in denominations:
        apparieur.set_seq1(cle_deno)
        if apparieur.real_quick_ratio() < seuil or \
                apparieur.quick_ratio() < seuil:
            continue
        ratio = apparieur.ratio()
        if ratio < seuil:
            continue
        courant = meilleur.get(eid)
        candidat = (round(ratio, 4), rang, source, cle_deno)
        if courant is None or candidat[0] > courant[0] or (
                candidat[0] == courant[0] and (candidat[1], candidat[2])
                < (courant[1], courant[2])):
            meilleur[eid] = candidat
    lignes = []
    for eid, (ratio, rang, source, cle_deno) in meilleur.items():
        ligne = decrit(eid, entites, nom_type)
        ligne.update({
            'note': 'PISTE — NON RESOLU, arbitrage humain requis',
            'matched_denomination': source,
            'denomination_rule': rang,
            'ratio': ratio,
            'contains': cle in cle_deno or cle_deno in cle,
        })
        lignes.append(ligne)
    lignes.sort(key=lambda x: (-x['ratio'], x['entity_id'],
                               x['matched_denomination']))
    return lignes[:maximum]


def resout_un(nom, index_graphe, index_table, entites, nom_type,
              interdits_table=None):
    """La regle, rang par rang. -> dict de resolution (sans les pistes)."""
    cle = normalise_cle(nom)
    base = {'name': nom, 'normalized': cle}
    if not cle:
        base.update({'status': 'not-found', 'match_rule': 'not-found',
                     'confidence': None,
                     'reason': 'nom vide apres normalisation'})
        return base
    for rang in RANGS_GRAPHE:
        paires = index_graphe[rang].get(cle)
        if not paires:
            continue
        candidats = []
        for eid, source in paires:
            c = decrit(eid, entites, nom_type)
            c['matched_string'] = source
            candidats.append(c)
        ids = {c['entity_id'] for c in candidats}
        if len(ids) == 1:
            base.update({'status': 'resolved', 'match_rule': rang,
                         'confidence': CONFIANCE_PAR_RANG[rang]})
            base.update(candidats[0])
            base['name'] = nom          # `decrit` n'ecrase pas la demande
            return base
        base.update({'status': 'ambiguous', 'match_rule': rang,
                     'confidence': None, 'candidates': candidats,
                     'reason': f"{len(ids)} entites portent cette chaine au "
                               f"rang {rang} — aucune n'est tranchee ici"})
        return base
    entrees = index_table.get(cle) if index_table is not None else None
    if entrees:
        candidats = []
        for eid, alias, confiance, genre in entrees:
            c = decrit(eid, entites, nom_type)
            c.update({'matched_string': alias, 'table_confidence': confiance,
                      'alias_kind': genre})
            candidats.append(c)
        ids = {c['entity_id'] for c in candidats}
        if len(ids) == 1:
            base.update({'status': 'resolved', 'match_rule': RANG_TABLE,
                         'confidence': candidats[0]['table_confidence']})
            base.update(candidats[0])
            base['name'] = nom
            return base
        base.update({'status': 'ambiguous', 'match_rule': RANG_TABLE,
                     'confidence': None, 'candidates': candidats,
                     'reason': f"{len(ids)} entites portent cet alias dans la "
                               "table (confiance haute/moyenne) — non tranche"})
        return base
    bloquees = (interdits_table or {}).get(cle)
    if bloquees:
        base['table_interdictions'] = [
            {'entity_id': eid,
             'entity_name': (entites.get(eid) or {}).get('name'),
             'alias': alias, 'table_confidence': confiance, 'notes': notes,
             'note': "LIGNE ECARTEE — la table interdit de resoudre "
                     "automatiquement sur cette chaine ; arbitrage humain"}
            for eid, alias, confiance, notes in bloquees]
        base.update({'status': 'not-found', 'match_rule': 'not-found',
                     'confidence': None,
                     'reason': "aucun rang du graphe ne porte cette chaine ; "
                               "la table la porte mais INTERDIT de la resoudre "
                               "automatiquement"})
        return base
    base.update({'status': 'not-found', 'match_rule': 'not-found',
                 'confidence': None,
                 'reason': 'aucun rang ne porte cette chaine'})
    return base


def noms_depuis_json(donnees, chemin):
    """Extrait la liste de noms d'un --from-json. Cf. docstring (4 formes)."""
    def nom_de(x):
        if isinstance(x, str):
            return x
        if isinstance(x, dict) and isinstance(x.get('name'), str):
            return x['name']
        return None

    if isinstance(donnees, list):
        noms = [nom_de(x) for x in donnees]
        if any(n is None for n in noms):
            echec_invocation(f"{chemin} : liste dont un element n'est ni une "
                             "chaine ni un objet a champ `name`")
        return noms
    if isinstance(donnees, dict):
        for cle in CLES_LISTES_NOMS:
            if isinstance(donnees.get(cle), list):
                noms = [nom_de(x) for x in donnees[cle]]
                if any(n is None for n in noms):
                    echec_invocation(f"{chemin} : `{cle}` contient un element "
                                     "ni chaine ni objet a champ `name`")
                return noms
        if isinstance(donnees.get('operations'), list):
            noms = []
            for op in donnees['operations']:
                if not isinstance(op, dict):
                    continue
                for cible in (op.get('target_entities') or []):
                    n = nom_de(cible)
                    if n is not None:
                        noms.append(n)
            if noms:
                return noms
            echec_invocation(f"{chemin} : `operations` present mais aucun "
                             "`target_entities[].name` exploitable")
    echec_invocation(f"{chemin} : forme non reconnue — attendu une liste de "
                     f"noms, une liste d'objets a champ `name`, un objet "
                     f"portant {' / '.join(CLES_LISTES_NOMS)}, ou un objet "
                     "portant `operations` (inventaire SourceQuote)")


def ligne_lisible(r):
    """Une ligne de sortie par nom demande."""
    marque = {'resolved': 'RESOLU', 'ambiguous': 'AMBIGU',
              'not-found': 'INTROUVABLE'}[r['status']]
    tete = f"  {marque:11s} {r['match_rule']:12s} « {r['name']} »"
    if r['status'] == 'resolved':
        types = ', '.join(r['entity_types']) or '(sans type)'
        return (f"{tete}\n"
                f"      -> {r['entity_id']} « {r['entity_name']} » [{types}]"
                f"  (matche : « {r['matched_string']} », confiance "
                f"{r['confidence']})")
    if r['status'] == 'ambiguous':
        lignes = [tete, f"      {r['reason']}"]
        for c in r['candidates']:
            lignes.append(f"      ? {c['entity_id']} « {c['entity_name']} » "
                          f"(matche : « {c['matched_string']} »)")
        return '\n'.join(lignes)
    lignes = [tete]
    for b in r.get('table_interdictions') or []:
        lignes.append(f"      ECARTEE (table) {b['entity_id']} "
                      f"« {b['entity_name']} » ~ « {b['alias']} » "
                      f"[{b['table_confidence']}] : {b['notes']}")
    for p in r.get('fuzzy_hints') or []:
        lignes.append(f"      PISTE ({p['ratio']:.2f}, {p['denomination_rule']}) "
                      f"{p['entity_id']} « {p['entity_name']} » "
                      f"~ « {p['matched_denomination']} »")
    if not (r.get('fuzzy_hints') or []):
        lignes.append("      aucune piste au-dessus du seuil")
    return '\n'.join(lignes)


def main(argv=None):
    p = argparse.ArgumentParser(
        description="Resout des noms d'entites contre le graphe GRC-20, en "
                    "interrogeant les denominations que le graphe declare "
                    "lui-meme (name, nameEn, labelEn, labelFr, aliases) AVANT "
                    "la table d'alias externe. Lecture seule, sortie "
                    "deterministe. Codes de sortie : 0 = la resolution a "
                    "tourne (des not-found restent un resultat), 2 = erreur "
                    "d'invocation.",
        epilog="Ordre strict des rangs : name > nameEn > labelEn > labelFr > "
               "aliases > alias-table (lignes de confiance haute/moyenne "
               "seulement) > not-found. Plusieurs entites au meme rang => "
               "`ambiguous`, jamais d'arbitrage automatique. Le fuzzy des "
               "not-found est une PISTE pour un humain, jamais une resolution.")
    p.add_argument('--name', action='append', default=None, metavar='CHAINE',
                   help="nom a resoudre (repetable ; combinable avec "
                        "--from-json)")
    p.add_argument('--from-json', default=None, metavar='FICHIER',
                   help="fichier JSON de noms : liste de chaines, liste "
                        "d'objets a champ `name`, objet portant `names` / "
                        "`entity_names` / `quote_supports_entity_names`, ou "
                        "objet portant `operations` (inventaire SourceQuote, "
                        "-> operations[].target_entities[].name)")
    p.add_argument('--graph', default=None, metavar='FICHIER',
                   help="graphe de reference (defaut : le plus recent du "
                        "depot)")
    p.add_argument('--alias-table', default=TABLE_DEFAUT, metavar='FICHIER',
                   help="table d'alias externe, CSV ';'-separe "
                        "(defaut : %(default)s)")
    p.add_argument('--no-alias-table', action='store_true',
                   help="n'interroge QUE les denominations du graphe (rangs "
                        "1-5) : mesure ce que le graphe resout seul")
    p.add_argument('--confidences', default=','.join(CONFIANCES_ADMISES),
                   metavar='LISTE',
                   help="confiances admises de la table externe, separees par "
                        "des virgules (defaut : %(default)s). `basse` couvre "
                        "collisions et traductions interpretatives : ne "
                        "l'ajouter que pour MESURER, jamais pour resoudre")
    p.add_argument('--ignore-table-interdictions', action='store_true',
                   help="admet les lignes de la table qui portent « ne "
                        "jamais/pas resoudre » dans leurs notes. POUR MESURER "
                        "SEULEMENT : ces lignes sont ecartees par defaut "
                        "parce que la table interdit elle-meme de les "
                        "resoudre automatiquement")
    p.add_argument('--fuzzy-seuil', type=float, default=FUZZY_SEUIL_DEFAUT,
                   metavar='R', help="ratio minimal des pistes affichees pour "
                                     "un not-found (defaut : %(default)s)")
    p.add_argument('--fuzzy-max', type=int, default=FUZZY_MAX_DEFAUT,
                   metavar='N', help="nombre maximal de pistes par not-found "
                                     "(defaut : %(default)s ; 0 = aucune)")
    p.add_argument('--report-json', default=None, metavar='CHEMIN',
                   help="ecrit en plus un rapport JSON deterministe "
                        "{graph, alias_table, summary, resolutions[]}")
    args = p.parse_args(argv)

    demandes = list(args.name or [])
    if args.from_json:
        demandes += noms_depuis_json(
            lire_json(args.from_json, "fichier --from-json"), args.from_json)
    if not demandes:
        echec_invocation("aucun nom a resoudre : fournir --name et/ou "
                         "--from-json")

    chemin_graphe = args.graph or graphe_le_plus_recent()
    if not chemin_graphe:
        echec_invocation("aucun graphe grc20-these-mael-rolland-v*.json "
                         "dans le depot (et aucun --graph fourni)")
    graphe = lire_json(chemin_graphe, 'graphe de reference')
    if not isinstance(graphe.get('entities'), list):
        echec_invocation(f"graphe sans liste d'entites : {chemin_graphe}")

    entites, nom_type = carte_entites(graphe)
    denominations = denominations_du_graphe(graphe)
    index_graphe = index_du_graphe(denominations)

    confiances = tuple(x.strip() for x in args.confidences.split(',')
                       if x.strip())
    if not confiances:
        echec_invocation("--confidences ne retient aucune valeur")
    if args.no_alias_table:
        index_table, interdits_table, compteurs_table = None, None, \
            collections.Counter()
    else:
        index_table, interdits_table, compteurs_table = charge_table_alias(
            args.alias_table, confiances,
            honorer_interdictions=not args.ignore_table_interdictions)

    # Une resolution par nom DISTINCT (chaine exacte), dans l'ordre de
    # premiere apparition ; `occurrences` garde la trace des repetitions.
    occurrences = collections.Counter(demandes)
    vus, ordre = set(), []
    for n in demandes:
        if n not in vus:
            vus.add(n)
            ordre.append(n)

    resolutions = []
    for nom in ordre:
        r = resout_un(nom, index_graphe, index_table, entites, nom_type,
                      interdits_table)
        r['occurrences'] = occurrences[nom]
        if r['status'] == 'not-found' and args.fuzzy_max > 0:
            r['fuzzy_hints'] = pistes_fuzzy(r['normalized'], denominations,
                                            entites, nom_type,
                                            args.fuzzy_seuil, args.fuzzy_max)
        resolutions.append(r)

    par_regle = collections.Counter(r['match_rule'] for r in resolutions)
    par_regle_refs = collections.Counter()
    for r in resolutions:
        par_regle_refs[r['match_rule']] += r['occurrences']
    par_statut = collections.Counter(r['status'] for r in resolutions)
    par_statut_refs = collections.Counter()
    for r in resolutions:
        par_statut_refs[r['status']] += r['occurrences']

    print(f"graphe       : {os.path.relpath(chemin_graphe, REPO)}")
    if index_table is None:
        print("table alias  : DESACTIVEE (--no-alias-table) — rangs 1-5 seuls")
    else:
        print(f"table alias  : {os.path.relpath(args.alias_table, REPO)} "
              f"({compteurs_table['retenues']}/{compteurs_table['lues']} "
              f"lignes retenues, confiances {'/'.join(confiances)}, "
              f"{compteurs_table['interdites']} ecartee(s) par leur propre "
              f"note « ne jamais/pas resoudre »"
              + (" — HONORAGE DESACTIVE" if args.ignore_table_interdictions
                 else "") + ")")
    print(f"noms         : {len(demandes)} demande(s), {len(ordre)} distinct(s)")
    print()
    for r in resolutions:
        print(ligne_lisible(r))

    print("\n=== RESUME (noms distincts / references) ===")
    for regle in RANGS + ('not-found',):
        if par_regle.get(regle):
            print(f"  {regle:12s} {par_regle[regle]:4d} / "
                  f"{par_regle_refs[regle]:4d}")
    print("  ---")
    for statut in ('resolved', 'ambiguous', 'not-found'):
        print(f"  {statut:12s} {par_statut.get(statut, 0):4d} / "
              f"{par_statut_refs.get(statut, 0):4d}")

    if args.report_json:
        sortie = {
            'graph': os.path.basename(chemin_graphe),
            'alias_table': (None if index_table is None
                            else os.path.relpath(args.alias_table, REPO)),
            'alias_table_confidences': (None if index_table is None
                                        else list(confiances)),
            'alias_table_lines': (None if index_table is None else {
                'read': compteurs_table['lues'],
                'usable': compteurs_table['retenues'],
                'refused_by_their_own_note': compteurs_table['interdites'],
                'interdictions_honoured': not args.ignore_table_interdictions,
            }),
            'rule_order': list(RANGS) + ['not-found'],
            'summary': {
                'names_requested': len(demandes),
                'names_distinct': len(ordre),
                'by_rule_distinct': dict(sorted(par_regle.items())),
                'by_rule_references': dict(sorted(par_regle_refs.items())),
                'by_status_distinct': dict(sorted(par_statut.items())),
                'by_status_references': dict(sorted(par_statut_refs.items())),
            },
            'resolutions': resolutions,
        }
        dossier = os.path.dirname(os.path.abspath(args.report_json))
        if dossier:
            os.makedirs(dossier, exist_ok=True)
        with open(args.report_json, 'w', encoding='utf-8') as f:
            json.dump(sortie, f, ensure_ascii=False, indent=1, sort_keys=True)
            f.write('\n')
        print(f"\nrapport json : {args.report_json}")
    return 0


if __name__ == '__main__':
    sys.exit(main())
