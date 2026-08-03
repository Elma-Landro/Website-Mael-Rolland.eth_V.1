#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Appariement chronologie CSV x graphe GRC-20 : quels evenements manquent ?

Script en lecture seule : ne modifie ni le graphe ni le CSV.
Python 3 standard library uniquement.

Principe : pour chaque ligne du CSV, chercher le meilleur equivalent parmi les
InfrastructureEvent et CrisisEvent de v97, puis classer en quatre categories.
La decision combine trois signaux, jamais un score unique :

  - similarite de libelle (Jaccard sur tokens, hors mots-vides)
  - compatibilite de date (annee, ou emboitement des precisions)
  - ancres distinctives (noms propres, marques, acronymes, nombres)

Les ancres sont decisives : « Lancement de MtGox » et « Premiere bourse
d'echange importante (MtGox) » ont un Jaccard faible mais partagent l'ancre
MtGox. Sans ce signal, l'evenement serait declare manquant a tort.

Categories :
  ALREADY_IN_GRAPH   equivalent clair et date compatible
  POSSIBLE_DUPLICATE equivalent probable, ou date divergente -> revue humaine
  CONFIRMED_MISSING  aucun equivalent, et la ligne CSV est exploitable
  TOO_AMBIGUOUS      donnees CSV trop pauvres pour trancher

Usage:
    python3 scripts/match_chronology_events.py
    python3 scripts/match_chronology_events.py --graph ... --csv ... --out ...
"""
import argparse, csv, json, os, re, sys, collections

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from grc20_commun import REPO, sans_accents  # noqa: E402

_p = argparse.ArgumentParser(description="Appariement chronologie CSV x graphe GRC-20.")
_p.add_argument('--graph', default=os.path.join(REPO, 'grc20-these-mael-rolland-v97.json'))
_p.add_argument('--csv', default=os.path.join(
    REPO, 'docs', 'research', 'catalogue-evenements', 'catalogue-evenements-v1.csv'))
_p.add_argument('--out', default=os.path.join(REPO, 'docs', 'audits', 'data'))
_p.add_argument('--quiet', action='store_true')
args = _p.parse_args()

os.makedirs(args.out, exist_ok=True)

# ---------- normalisation ----------
# `sans_accents` vient de grc20_commun : les trois copies du depot etaient
# identiques au caractere pres.

MOTS_VIDES = {
    'de', 'du', 'des', 'le', 'la', 'les', 'un', 'une', 'd', 'l', 'en', 'et', 'a', 'au',
    'aux', 'par', 'pour', 'sur', 'the', 'of', 'in', 'to', 'premier', 'premiere', 'first',
    'lancement', 'creation', 'publication', 'nouveau', 'nouvelle', 'via', 'vers', 'avec',
    'son', 'sa', 'ses', 'ce', 'cette', 'est', 'sont', 'plus',
}

def tokens(s, garder_parentheses=True):
    s = sans_accents(s).lower().replace('’', "'")
    s = re.sub(r'^infrastructureevent\s*[-—]\s*', '', s)
    s = re.sub(r'^crisisevent\s*[-—]\s*', '', s)
    if not garder_parentheses:
        s = re.sub(r'\(.*?\)', ' ', s)
    s = re.sub(r"[^a-z0-9' ]", ' ', s)
    return set(t for t in s.split() if len(t) > 1 and t not in MOTS_VIDES)

def jaccard(a, b):
    return len(a & b) / len(a | b) if (a and b) else 0.0

# Mots frequents du domaine : trop generiques pour servir d'ancre discriminante.
ANCRES_BANALES = {
    'BTC', 'ETH', 'USD', 'EUR', 'BIP', 'CVE', 'CM', 'DE', 'LA', 'LE', 'ET', 'UN',
    'BITCOIN', 'ETHEREUM', 'CRYPTO', 'BLOCKCHAIN',
}

def ancres(nom):
    """Noms propres, marques, acronymes et nombres distinctifs d'un libelle."""
    n = re.sub(r'^(?:Infrastructure|Crisis)Event\s*[-—]\s*', '', nom or '')
    n = sans_accents(n)
    out = set()
    # acronymes en capitales (MtGox capte par la regle suivante)
    out |= set(re.findall(r'\b[A-Z]{2,6}\b', n))
    # casse interne : MtGox, WikiLeaks, SatoshiDice, BitLaundry, PayPal, CoinMarketCap
    out |= set(re.findall(r'\b[A-Z][a-z]+[A-Z][A-Za-z]*\b', n))
    # mots capitalises d'au moins 4 lettres (noms propres, marques)
    out |= set(re.findall(r'\b[A-Z][a-z]{3,}\b', n))
    # identifiants numeriques hors annees
    out |= set(re.findall(r'\b\d{3,6}\b', n)) - set(re.findall(r'\b(?:19|20)\d{2}\b', n))
    out = {a.upper() for a in out} - ANCRES_BANALES
    # « prefixe + numero » recolle : BIP16 et « BIP 16 » doivent produire la meme
    # ancre, sinon un simple espace suffit a faire echouer l'appariement.
    for pre, num in re.findall(r'\b([A-Za-z]{2,6})[\s\-]?(\d{1,4})\b', n):
        if not re.fullmatch(r'(?:19|20)\d{2}', num):
            out.add(f'{pre.upper()}{num}')
    return out

def normaliser_date(v):
    """-> (iso, precision). Conserve la forme d'origine ailleurs."""
    v = str(v or '').strip()
    if not v:
        return ('', '')
    m = re.match(r'^(\d{4})-(\d{2})-(\d{2})', v)
    if m:
        return (v[:10], 'jour')
    m = re.match(r'^(\d{2})/(\d{2})/(\d{4})$', v)
    if m:
        return (f'{m.group(3)}-{m.group(2)}-{m.group(1)}', 'jour')
    m = re.match(r'^(\d{4})-(\d{2})$', v)
    if m:
        return (v, 'mois')
    m = re.match(r'^(\d{4})$', v)
    if m:
        return (v, 'annee')
    m = re.search(r'\b(19|20)\d{2}\b', v)
    return (m.group(0), 'annee') if m else ('', '')

def dates_compatibles(a, b):
    """Deux dates ne se contredisent pas si l'une prefixe l'autre, ou meme annee."""
    if not a or not b:
        return None                      # indecidable
    if a == b or a.startswith(b) or b.startswith(a):
        return True
    return a[:4] == b[:4]

# ---------- chargement du graphe ----------

with open(args.graph, encoding='utf-8') as f:
    g = json.load(f)

nom_type = {t['id']: t.get('name') for t in g['types']}
nom_rel = {r['id']: r.get('name') for r in g['relation_types']}

degre = collections.Counter()
for r in g['relations']:
    degre[r.get('from')] += 1
    degre[r.get('to')] += 1

def attr(e, k):
    a = (e.get('attributes') or {}).get(k)
    return (a.get('value') if a else '') or ''

TYPES_EVENEMENT = {'InfrastructureEvent', 'CrisisEvent'}

evenements = []   # index 1 : les evenements, cibles d'un ajout eventuel
couverture = []   # index 2 : TOUTES les entites, pour detecter une couverture
                  #           hors typage evenementiel
for e in g['entities']:
    ts = [nom_type.get(t, t) for t in (e.get('types') or [])]
    nom = e.get('name', '')
    desc = attr(e, 'description')
    d, prec = normaliser_date(attr(e, 'date') or attr(e, 'year') or attr(e, 'period'))
    # Le libelle seul ne suffit pas : « Digital Asset Transfer Authority » ne
    # rejoint « Comite interprofessionnel DATA » que par sa description. On
    # indexe donc nom + description.
    fiche = {
        'id': e['id'], 'nom': nom, 'types': ts,
        'date': d, 'precision': prec,
        'toks': tokens(nom, False), 'toks_full': tokens(nom, True),
        'ancres': ancres(nom) | ancres(desc[:400]),
        'toks_desc': tokens(desc[:400], True),
        'desc': desc, 'degre': degre[e['id']],
    }
    couverture.append(fiche)
    if TYPES_EVENEMENT & set(ts):
        fiche = dict(fiche)
        fiche['kind'] = 'CrisisEvent' if 'CrisisEvent' in ts else 'InfrastructureEvent'
        evenements.append(fiche)

# ---------- chargement du CSV ----------

with open(args.csv, encoding='utf-8') as f:
    lignes = list(csv.DictReader(f, delimiter=';'))

for c in lignes:
    c['_date'], c['_prec'] = normaliser_date(c['date'])
    c['_toks'] = tokens(c['intitule'], False)
    c['_toks_full'] = tokens(c['intitule'], True)
    c['_ancres'] = ancres(c['intitule'])

# ---------- appariement ----------

SEUIL_FORT, SEUIL_FAIBLE = 0.50, 0.26

resultats = []
for c in lignes:
    meilleur, score_max, detail = None, 0.0, {}
    for e in evenements:
        jt = max(jaccard(c['_toks'], e['toks']), jaccard(c['_toks_full'], e['toks_full']))
        communes = c['_ancres'] & e['ancres']
        compat = dates_compatibles(c['_date'], e['date'])
        # L'ancre partagee vaut autant qu'un fort recouvrement lexical ;
        # une date compatible la renforce, une date contradictoire la tempere.
        score = jt
        if communes:
            score = max(score, 0.55 + 0.10 * min(len(communes), 3))
            if compat is False:
                score -= 0.18
        if compat is True and jt >= 0.20:
            score += 0.10
        if score > score_max:
            meilleur, score_max = e, score
            detail = {'jaccard': round(jt, 2), 'ancres': sorted(communes), 'date_ok': compat}

    # Le CSV signale lui-meme ses incertitudes par un marqueur [CHANTIER] en note.
    # Quand la reserve porte sur la date ou la localisation textuelle, la ligne
    # n'est pas « suffisamment datee ou situable » : on la remonte telle quelle.
    note = c.get('notes') or ''
    m_ch = re.search(r'\[CHANTIER\s*:?\s*([^\]]*)\]', note)
    reserve = m_ch.group(1).strip() if m_ch else ''
    reserve_date = bool(reserve) and bool(
        re.search(r'date|localisation|situe|indique', reserve, re.I))

    exploitable = (bool(c['_date']) and len(c['_toks']) >= 2 and bool(c['phase'])
                   and not reserve_date)

    # Deuxieme passe, sur TOUTES les entites du graphe. Un fait peut etre porte
    # par un Concept, une PriceWindow, un MediaOutlet ou une Reference sans
    # exister comme evenement. Ne comparer qu'aux evenements produit alors un
    # « manquant » qui n'en est pas un : c'est ce qui a fait echouer la
    # premiere version de ce script sur 10 candidats sur 12.
    couv, couv_score = None, 0.0
    for e in couverture:
        if TYPES_EVENEMENT & set(e['types']):
            continue
        jt = max(jaccard(c['_toks'], e['toks']), jaccard(c['_toks_full'], e['toks_full']))
        jd = jaccard(c['_toks_full'], e['toks_desc'])
        communes = c['_ancres'] & e['ancres']
        s = max(jt, 0.75 * jd)
        if communes:
            s = max(s, 0.45 + 0.10 * min(len(communes), 3))
        if s > couv_score:
            couv, couv_score = e, s
    couverture_type = '|'.join(couv['types']) if (couv and couv_score >= 0.45) else ''
    couverture_nom = couv['nom'] if couverture_type else ''

    if score_max >= SEUIL_FORT:
        if detail.get('date_ok') is False:
            statut = 'POSSIBLE_DUPLICATE'
            motif = (f"libelle proche (jaccard {detail['jaccard']}, ancres "
                     f"{detail['ancres'] or 'aucune'}) mais dates divergentes "
                     f"({c['_date']} / {meilleur['date'] or 'non datee'})")
        else:
            statut = 'ALREADY_IN_GRAPH'
            motif = (f"equivalent clair (jaccard {detail['jaccard']}, ancres "
                     f"{detail['ancres'] or 'aucune'}), dates compatibles")
    elif score_max >= SEUIL_FAIBLE:
        statut = 'POSSIBLE_DUPLICATE'
        motif = (f"equivalent partiel (jaccard {detail['jaccard']}, ancres "
                 f"{detail['ancres'] or 'aucune'}) — revue humaine requise")
    elif not exploitable:
        statut = 'TOO_AMBIGUOUS'
        manque = []
        if not c['_date']:
            manque.append('date non exploitable')
        if len(c['_toks']) < 2:
            manque.append('libelle trop pauvre')
        if not c['phase']:
            manque.append('phase absente')
        if reserve_date:
            manque.append(f'reserve du CSV : {reserve}')
        motif = 'donnees CSV insuffisantes : ' + ', '.join(manque)
    elif couverture_type:
        statut = 'POSSIBLE_DUPLICATE'
        motif = (f"aucun equivalent evenementiel, mais le fait est deja porte par "
                 f"une entite de type {couverture_type} : « {couverture_nom[:52]} » "
                 f"— ajouter un evenement ferait doublon de fond")
    else:
        statut = 'CONFIRMED_MISSING'
        motif = (f"aucun equivalent (meilleur score {round(score_max, 2)} — "
                 f"« {meilleur['nom'][:50] if meilleur else 'aucun'} »), et aucune "
                 f"couverture par un autre type")

    resultats.append({
        'id_csv': c['id'], 'statut': statut, 'score': round(score_max, 2),
        'intitule': c['intitule'], 'date_csv': c['date'], 'date_iso': c['_date'],
        'precision': c['precision'], 'phase': c['phase'], 'nature': c['nature'],
        'crise': c['crise'], 'systeme': c['systeme'], 'domaine_8': c['domaine_8'],
        'source': c['source'], 'reserve_csv': reserve,
        'couverture_type': couverture_type, 'couverture_entite': couverture_nom,
        'entite_graphe': meilleur['nom'] if meilleur else '',
        'id_graphe': meilleur['id'] if meilleur else '',
        'date_graphe': meilleur['date'] if meilleur else '',
        'motif': motif,
    })

ORDRE = {'CONFIRMED_MISSING': 0, 'POSSIBLE_DUPLICATE': 1, 'TOO_AMBIGUOUS': 2,
         'ALREADY_IN_GRAPH': 3}
resultats.sort(key=lambda r: (ORDRE[r['statut']], r['id_csv']))

CHAMPS = ['id_csv', 'statut', 'score', 'intitule', 'date_csv', 'date_iso', 'precision',
          'phase', 'nature', 'crise', 'systeme', 'domaine_8', 'entite_graphe',
          'id_graphe', 'date_graphe', 'couverture_type', 'couverture_entite',
          'motif', 'reserve_csv', 'source']

with open(os.path.join(args.out, 'chronology-events-classification.csv'), 'w',
          encoding='utf-8', newline='') as f:
    w = csv.DictWriter(f, fieldnames=CHAMPS, delimiter=';')
    w.writeheader()
    for r in resultats:
        w.writerow({k: r[k] for k in CHAMPS})

# ---------- rapport ----------

if not args.quiet:
    c_statut = collections.Counter(r['statut'] for r in resultats)
    print('=== APPARIEMENT CHRONOLOGIE x GRAPHE v97 ===')
    print(f"lignes CSV            : {len(lignes)}")
    print(f"evenements du graphe  : {len(evenements)} "
          f"(IE {sum(1 for e in evenements if e['kind'] == 'InfrastructureEvent')} / "
          f"CE {sum(1 for e in evenements if e['kind'] == 'CrisisEvent')})")
    print()
    for k in ORDRE:
        print(f"  {k:20s} {c_statut[k]}")
    print()
    print('-- CONFIRMED_MISSING par phase --')
    par_phase = collections.Counter(
        r['phase'] for r in resultats if r['statut'] == 'CONFIRMED_MISSING')
    for k in ('poc', 'peche', 'maturation'):
        print(f"  {k:12s} {par_phase[k]}")
    print()
    print('-- CONFIRMED_MISSING (detail) --')
    for r in resultats:
        if r['statut'] == 'CONFIRMED_MISSING':
            print(f"   {r['id_csv']} [{r['phase']:10s}] {r['date_iso'] or '????':10s} "
                  f"{r['intitule'][:58]}")
    print()
    print('-- POSSIBLE_DUPLICATE (detail) --')
    for r in resultats:
        if r['statut'] == 'POSSIBLE_DUPLICATE':
            print(f"   {r['id_csv']} [{r['phase']:10s}] {r['intitule'][:44]}")
            print(f"        -> {r['entite_graphe'][:66]}")
