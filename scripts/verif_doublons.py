#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verification automatique des doublons + generation du patch GRC20.
Principe : 3 vetos, 2 tests de confirmation, decision par conjonction.
Aucune operation destructive : le patch n'emet que des SET_ATTRIBUTE.

Script en lecture seule sur le graphe : ne le modifie jamais.
Python 3 standard library uniquement (aucune dependance externe).

Usage:
    python3 scripts/verif_doublons.py
    python3 scripts/verif_doublons.py --graph grc20-these-mael-rolland-v97.json
    python3 scripts/verif_doublons.py --out /tmp/rejeu --patch /tmp/rejeu/patch.json

Sorties:
    <out>/doublons-verifies.csv          73 paires, statut + motif de chaque decision
    <out>/dates-verification-externe.csv 5 conflits de dates, preuve et statut
    <patch>                              patch GRC20, SET_ATTRIBUTE uniquement

Les valeurs par defaut pointent vers l'arborescence du depot : le rejeu
regenere les fichiers a l'endroit ou ils sont versionnes, `git diff` fait foi.
"""
import argparse, json, os, re, unicodedata, collections

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

_p = argparse.ArgumentParser(
    description="Verification des doublons d'evenements GRC-20 + generation du patch.",
)
_p.add_argument('--graph', '-g', default=os.path.join(REPO, 'grc20-these-mael-rolland-v97.json'),
                help="Chemin vers le graphe JSON (defaut: grc20-these-mael-rolland-v97.json).")
_p.add_argument('--out', '-o', default=os.path.join(REPO, 'docs', 'audits', 'data'),
                help="Repertoire de sortie des CSV (defaut: docs/audits/data).")
_p.add_argument('--patch', default=os.path.join(REPO, 'patch_10_dedup_events.json'),
                help="Chemin de sortie du patch (defaut: patch_10_dedup_events.json a la racine).")
_args = _p.parse_args()

GRAPH = _args.graph
OUT   = _args.out
PATCH = _args.patch
os.makedirs(OUT, exist_ok=True)

def sa(s):
    s = unicodedata.normalize('NFD', s or '')
    return ''.join(c for c in s if unicodedata.category(c) != 'Mn')

STOP = {'de','du','des','le','la','les','un','une','d','l','en','et','a','au','aux',
        'par','pour','sur','the','of','in','to'}

def toks(s, keep_paren=True):
    s = sa(s).lower().replace('\u2019', "'")
    s = re.sub(r'^infrastructureevent\s*[-\u2014]\s*', '', s)
    if not keep_paren: s = re.sub(r'\(.*?\)', ' ', s)
    s = re.sub(r"[^a-z0-9' ]", ' ', s)
    return set(t for t in s.split() if t and t not in STOP)

def jac(a, b):
    return len(a & b) / len(a | b) if (a and b) else 0.0

def ids_distinctifs(nom):
    n = re.sub(r'^InfrastructureEvent\s*[-\u2014]\s*', '', nom or '')
    acr = set(re.findall(r'\b[A-Z]{2,6}\b', n)) - {'BTC','ETH','USD','BIP','CVE'}
    num = set(re.findall(r'\b\d{3,6}\b', n)) - set(re.findall(r'\b(?:19|20)\d{2}\b', n))
    return acr | num

# ---------- chargement ----------
with open(GRAPH, encoding='utf-8') as f:
    g = json.load(f)
tid = {t['id']: t.get('name') for t in g['types']}
inv = {v: k for k, v in tid.items()}
rtn = {r['id']: r.get('name') for r in g['relation_types']}
rel_out = collections.defaultdict(set)
for r in g['relations']:
    n = rtn.get(r.get('type'), '')
    if n in ('belongs to domain', 'appears in section', 'occurs in'):
        rel_out[r['from']].add((n, r['to']))

def av(e, k):
    a = (e.get('attributes') or {}).get(k)
    return (a.get('value') if a else '') or ''

def norm_date(v):
    v = str(v or '').strip()
    for pat, f in ((r'^(\d{4})-(\d{2})-(\d{2})', lambda m: m.group(0)[:10]),
                   (r'^(\d{2})/(\d{2})/(\d{4})$', lambda m: f'{m.group(3)}-{m.group(2)}-{m.group(1)}'),
                   (r'^(\d{4})-(\d{2})$', lambda m: m.group(0)),
                   (r'^(\d{4})$', lambda m: m.group(0))):
        m = re.match(pat, v)
        if m: return f(m)
    m = re.search(r'\b(19|20)\d{2}\b', v)
    return m.group(0) if m else ''

evts = []
for e in g['entities']:
    ts = [tid.get(t, t) for t in (e.get('types') or [])]
    if not ({'InfrastructureEvent', 'CrisisEvent'} & set(ts)): continue
    evts.append({
        'id': e['id'], 'name': e.get('name', ''),
        'kind': 'CrisisEvent' if 'CrisisEvent' in ts else 'InfrastructureEvent',
        'date': norm_date(av(e, 'date') or av(e, 'year')),
        'cve': av(e, 'cveId') or av(e, 'cveReference'),
        'crisis_no': re.sub(r'\D', '', av(e, 'crisisNumber')),
        'desc': av(e, 'description'), 'chapter': av(e, 'chapter'),
        'nattr': len(e.get('attributes') or {}), 'nrel': len(rel_out.get(e['id'], ())),
    })

# ---------- les 5 tests ----------
def date_compatible(a, b):
    """VETO si les deux dates existent et se contredisent."""
    da, db = a['date'], b['date']
    if not da or not db: return True, 'une date absente'
    if da == db: return True, 'dates identiques'
    if da.startswith(db) or db.startswith(da): return True, 'precisions emboitees'
    return False, f'dates contradictoires ({da} / {db})'

def ids_compatibles(a, b):
    """VETO si CVE, n de crise ou identifiants distinctifs divergent."""
    if a['cve'] and b['cve'] and a['cve'] != b['cve']:
        return False, f"CVE differents ({a['cve']} / {b['cve']})"
    if a['crisis_no'] and b['crisis_no'] and a['crisis_no'] != b['crisis_no']:
        return False, f"n de crise differents ({a['crisis_no']} / {b['crisis_no']})"
    ia, ib = ids_distinctifs(a['name']), ids_distinctifs(b['name'])
    if ia and ib and ia != ib:
        return False, f'identifiants distinctifs divergents ({sorted(ia)} / {sorted(ib)})'
    return True, 'identifiants compatibles'

def type_compatible(a, b):
    """VETO si les deux entites ne sont pas du meme type."""
    return (a['kind'] == b['kind'], 'meme type' if a['kind'] == b['kind'] else 'types differents')

def test_structure(a, b):
    """CONFIRMATION : cibles de relations partagees (domaine, section, arene)."""
    ra, rb = rel_out.get(a['id'], set()), rel_out.get(b['id'], set())
    if not ra or not rb: return 0.0, 'relations absentes'
    return jac(ra, rb), f'{len(ra & rb)} cible(s) commune(s)'

def test_description(a, b):
    if not a['desc'] or not b['desc']: return 0.0, 'description absente'
    return jac(toks(a['desc']), toks(b['desc'])), 'chevauchement de description'

SEUIL_NOM_SUR, SEUIL_NOM_CAND = 0.60, 0.28
resultats = []
for i, a in enumerate(evts):
    for b in evts[i+1:]:
        jn = jac(toks(a['name'], False), toks(b['name'], False))
        if jn < SEUIL_NOM_CAND: continue
        motifs, veto = [], None
        for f in (type_compatible, date_compatible, ids_compatibles):
            ok, m = f(a, b)
            motifs.append(m)
            if not ok: veto = m; break
        if veto:
            statut, raison = 'REJET_AUTO', veto
        else:
            js, ms = test_structure(a, b)
            jd, md = test_description(a, b)
            motifs += [ms, md]
            confirme = (js > 0) or (jd >= 0.30)
            date_forte = a['date'] and a['date'] == b['date'] and len(a['date']) == 10
            if jn >= SEUIL_NOM_SUR and confirme and (date_forte or not (a['date'] and b['date'])):
                statut, raison = 'FUSION_SURE', f'nom {jn:.2f}, structure {js:.2f}, desc {jd:.2f}'
            else:
                statut, raison = 'A_VERIFIER', f'nom {jn:.2f}, structure {js:.2f}, desc {jd:.2f}'
        # canonique = la fiche la mieux dotee
        can, dup = sorted((a, b), key=lambda x: (-x['nattr'], -x['nrel'], x['name']))
        resultats.append({'statut': statut, 'score_nom': round(jn, 2), 'raison': raison,
                          'motifs': ' ; '.join(motifs),
                          'canonique_id': can['id'], 'canonique': can['name'],
                          'doublon_id': dup['id'], 'doublon': dup['name'],
                          'date_can': can['date'], 'date_dup': dup['date']})

ordre = {'FUSION_SURE': 0, 'A_VERIFIER': 1, 'REJET_AUTO': 2}
resultats.sort(key=lambda r: (ordre[r['statut']], -r['score_nom']))

# ---------- corrections de dates verifiees en externe ----------
CORR = [
 {'cle': 'litecoin', 'date_cible': '2011-10-07',
  'statut': 'CONFIRME_EXTERNE',
  'preuve': 'Client publie sur GitHub et bloc de genese mine le 07/10/2011 ; reseau actif le 13/10/2011 '
            '(Wikipedia Litecoin ; CoinMarketCap ; Litecoin Foundation). Le texte de la these (ch.I l.359, '
            '« debut octobre 2011 ») est correct ; la date du graphe (19/11/2011) est erronee.'},
 {'cle': 'frontier', 'date_cible': '2015-07-30',
  'statut': 'CONFIRME_EXTERNE_GRAPHE_DEJA_JUSTE',
  'preuve': "Billet du blog de la Fondation Ethereum date du 30/07/2015 annoncant le bloc de genese et "
            "Frontier ; CoinDesk du 30/07/2015. Le graphe (30/07) est juste ; c'est le texte de la these "
            "(ch.I l.399, 20/07/2015) qui est a corriger."},
 {'cle': 'bitcointalk', 'date_cible': '2009-11-22',
  'statut': 'CONFIRME_EXTERNE_GRAPHE_DEJA_JUSTE',
  'preuve': "Premier message de Nakamoto sur le forum le 22/11/2009 (BitcoinWiki ; Medium ; analyses de "
            "corpus). Un forum SourceForge anterieur, aujourd'hui perdu, l'a precede : le « janvier 2009 » "
            "du ch.I l.113 vise probablement ce forum anterieur, pas Bitcointalk."},
 {'cle': 'newlibertystandard', 'date_cible': None,
  'statut': 'DEUX_EVENEMENTS_DISTINCTS',
  'preuve': "Les deux dates sont exactes et designent deux actes differents : le 05/10/2009, publication du "
            "premier taux BTC/USD (1 $ = 1 309,03 BTC, formule au cout de production) ; le 12/10/2009, "
            "premiere transaction BTC contre fiat (Malmi vend 5 050 BTC pour 5,02 $ via PayPal). "
            "Recommandation : dedoubler l'evenement plutot que d'arbitrer."},
 {'cle': 'bitlaundry', 'date_cible': None,
  'statut': 'NON_TRANCHE',
  'preuve': "Aucune source externe ne donne de date precise : « autour de 2010 » (BitMixList) ; la fiche "
            "Bitcoin Wiki citee par la litterature academique est datee de 2011. Ni le 09/2010 du graphe ni "
            "le 12/2010 de la these (ch.I n.74 l.607) ne sont confirmes. Validation manuelle requise."},
]

# ---------- regroupement transitif des FUSION_SURE ----------
# Une entite ne peut porter qu'un seul duplicateOf. Traiter les paires
# independamment produirait des affectations contradictoires (A -> B puis A -> C,
# derniere ecriture gagnante) et des chaines de doublons. On ferme donc les paires
# par transitivite (union-find) et on n'emet qu'un canonique par grappe.
par_id = {e['id']: e for e in evts}
parent = {}

def trouver(x):
    parent.setdefault(x, x)
    while parent[x] != x:
        parent[x] = parent[parent[x]]
        x = parent[x]
    return x

def unir(a, b):
    ra, rb = trouver(a), trouver(b)
    if ra != rb: parent[ra] = rb

raison_paire = {}
for r in resultats:
    if r['statut'] != 'FUSION_SURE': continue
    unir(r['canonique_id'], r['doublon_id'])
    raison_paire[frozenset((r['canonique_id'], r['doublon_id']))] = r['raison']

grappes = collections.defaultdict(list)
for x in parent: grappes[trouver(x)].append(x)

# Meme regle de canonicite que pour les paires : la fiche la mieux dotee
# (attributs, puis relations, puis nom). Appliquee a la grappe entiere.
def rang(eid):
    e = par_id[eid]
    return (-e['nattr'], -e['nrel'], e['name'])

# ---------- patch (SET_ATTRIBUTE uniquement) ----------
# Format : dialecte de patch_2c_definitions.json — enveloppe `schemaVersion` + `ops`,
# operations `{type, entityId, attributeId, value:{type,value}}`. C'est le dialecte que
# le graphe lui-meme journalise dans sa cle de tete `ops`. Les cles `_comment` sont
# des annotations de tracabilite, ignorables par un applicateur.
ops = []
for membres in sorted(grappes.values(), key=lambda m: sorted(m)):
    if len(membres) < 2: continue
    membres = sorted(membres, key=rang)
    canon = membres[0]
    for dup in membres[1:]:
        raison = raison_paire.get(frozenset((canon, dup)), 'lien transitif dans la grappe')
        ops.append({'type': 'SET_ATTRIBUTE', 'entityId': dup, 'attributeId': 'duplicateOf',
                    'value': {'type': 'TEXT', 'value': canon},
                    '_comment': f"doublon de « {par_id[canon]['name']} » — grappe de "
                                f"{len(membres)} entites — {raison}"})
        ops.append({'type': 'SET_ATTRIBUTE', 'entityId': dup, 'attributeId': 'reviewStatus',
                    'value': {'type': 'TEXT', 'value': 'duplicate-pending-merge'}})

CORR_PAR_CLE = {c['cle']: c for c in CORR}

for e in evts:
    n = sa(e['name']).lower()
    if 'litecoin' in n and e['date'] and e['date'] != '2011-10-07':
        c = CORR_PAR_CLE['litecoin']
        ops.append({'type': 'SET_ATTRIBUTE', 'entityId': e['id'], 'attributeId': 'date',
                    'value': {'type': 'TEXT', 'value': c['date_cible']},
                    '_comment': f"correction ; ancienne valeur « {e['date']} » ; {c['preuve'][:120]}"})
        # Convention etablie en v97 : `dateAuthority` porte une valeur controlee
        # (37 entites : TIMELINE_FIGURE) et la preuve va dans `dateSource`.
        ops.append({'type': 'SET_ATTRIBUTE', 'entityId': e['id'], 'attributeId': 'dateAuthority',
                    'value': {'type': 'TEXT', 'value': 'EXTERNAL_VERIFICATION'}})
        ops.append({'type': 'SET_ATTRIBUTE', 'entityId': e['id'], 'attributeId': 'dateSource',
                    'value': {'type': 'TEXT', 'value': 'Vérification externe 02/08/2026 ; '
                                                       'thèse ch.I l.359'}})

patch = {
    'schemaVersion': 1,
    'description': "Dedoublonnage conservateur des evenements + correction de date verifiee en externe",
    'source_graph': 'grc20-these-mael-rolland-v97.json',
    'generated': '2026-08-02',
    'author': 'Catalogue d evenements (chantier valorisation)',
    'policy': "Aucune suppression, aucune fusion destructive. Les doublons sont MARQUES "
              "(duplicateOf + reviewStatus) et restent interrogeables. La fusion effective reste "
              "une decision humaine posterieure.",
    'ops': ops,
}
with open(PATCH, 'w', encoding='utf-8') as f:
    json.dump(patch, f, ensure_ascii=False, indent=1)

import csv
with open(f'{OUT}/doublons-verifies.csv', 'w', encoding='utf-8', newline='') as f:
    w = csv.DictWriter(f, delimiter=';', fieldnames=['statut','score_nom','raison','motifs',
        'canonique','canonique_id','date_can','doublon','doublon_id','date_dup'])
    w.writeheader()
    for r in resultats: w.writerow({k: r[k] for k in w.fieldnames})

with open(f'{OUT}/dates-verification-externe.csv', 'w', encoding='utf-8', newline='') as f:
    w = csv.DictWriter(f, delimiter=';', fieldnames=['cle','statut','date_cible','preuve'])
    w.writeheader()
    for c in CORR: w.writerow({k: (c[k] or '') for k in w.fieldnames})

c = collections.Counter(r['statut'] for r in resultats)
print('=== VERIFICATION DES DOUBLONS ===')
print('paires candidates examinees :', len(resultats))
for k in ('FUSION_SURE', 'A_VERIFIER', 'REJET_AUTO'): print(f'  {k:14s} {c[k]}')
print()
print('-- FUSION_SURE (entrent dans le patch) --')
for r in resultats:
    if r['statut'] == 'FUSION_SURE':
        print(f"   {r['canonique'][:46]}  <=  {r['doublon'][:46]}   [{r['raison']}]")
print()
print('-- REJET_AUTO (vetos, exclus du patch) --')
for r in resultats:
    if r['statut'] == 'REJET_AUTO':
        print(f"   {r['canonique'][:40]} / {r['doublon'][:40]} -> {r['raison'][:70]}")
print()
print(f'operations dans le patch : {len(ops)}')
