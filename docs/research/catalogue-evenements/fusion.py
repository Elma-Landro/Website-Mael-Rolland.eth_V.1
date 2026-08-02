#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Fusion : graphe GRC20 v97 (site) x catalogue-evenements-v1.csv (calibrage).
Sortie : CSV unifie + table de divergences + rapport."""
import json, csv, re, unicodedata, collections, os

GRAPH = '/home/claude/site/grc20-these-mael-rolland-v97.json'
CAL   = '/mnt/user-data/outputs/catalogue-evenements-v1.csv'
OUT   = '/mnt/user-data/outputs'

# --- 8 domaines de la these (ch.I l.251), verbatim ---
DOM = {
 'i'  : "spheres d'usage reelle et financiere (vert)",
 'ii' : "traitement des transactions (jaune)",
 'iii': "portefeuilles et paiements (orange)",
 'iv' : "information et connaissance (bleu fonce)",
 'v'  : "conformite aux reglementations nationales (bleu clair)",
 'vi' : "protocole Bitcoin (rouge)",
 'vii': "Altcoins (rose)",
 'viii':"autres (violet)",
}
# Correspondance domaines du graphe -> domaines de la these
DOM_MAP = {
 "sphere d'usage": 'i',
 "services de portefeuille et de paiement": 'iii',
 "information et connaissance": 'iv',
 "conformite reglementaire": 'v',
 "protocole et couche de base": 'vi',
 "altcoins, tokens et surcouches": 'vii',
 "de la confidentialite et de l'anonymisation": 'iii',   # mixage -> domaine (iii) l.251
 "[residuel - a reclasser]": 'viii',
}

def strip_acc(s):
    s = unicodedata.normalize('NFD', s or '')
    return ''.join(c for c in s if unicodedata.category(c) != 'Mn')

def norm(s):
    s = strip_acc(s).lower()
    s = s.replace('\u2019', "'").replace('\u2018', "'")
    s = re.sub(r'^infrastructureevent\s*[-\u2014]\s*', '', s)
    s = re.sub(r'\(.*?\)', ' ', s)
    s = re.sub(r"[^a-z0-9' ]", ' ', s)
    stop = {'de','du','des','le','la','les','un','une','d','l','en','et','a','au','aux','par','pour','sur'}
    toks = [t for t in s.split() if t and t not in stop]
    return ' '.join(toks)

MOIS = {'janv':'01','fevr':'02','mars':'03','avri':'04','mai':'05','juin':'06',
        'juil':'07','aout':'08','sept':'09','octo':'10','nove':'11','dece':'12'}

def norm_date(v):
    """-> (date_iso, precision, brut_si_non_parse)"""
    v = str(v or '').strip()
    if not v: return ('', '', '')
    m = re.match(r'^(\d{4})-(\d{2})-(\d{2})', v)
    if m: return (f'{m.group(1)}-{m.group(2)}-{m.group(3)}', 'jour', '')
    m = re.match(r'^(\d{4})-(\d{2})$', v)
    if m: return (v, 'mois', '')
    m = re.match(r'^(\d{2})/(\d{2})/(\d{4})$', v)          # DD/MM/YYYY
    if m: return (f'{m.group(3)}-{m.group(2)}-{m.group(1)}', 'jour', '')
    m = re.match(r'^(\d{1,2})\s+([a-zA-Zeu\u00e9\u00fb\u00e0]+)\.?\s*(\d{4})?', strip_acc(v))
    if m and strip_acc(m.group(2))[:4].lower() in MOIS:
        mo = MOIS[strip_acc(m.group(2))[:4].lower()]
        y = m.group(3)
        if y: return (f'{y}-{mo}-{int(m.group(1)):02d}', 'jour', '')
        return ('', '', v)
    m = re.match(r'^(\d{4})$', v)
    if m: return (v, 'annee', '')
    m = re.search(r'(\d{4})', v)
    if m: return (m.group(1), 'annee', v)
    return ('', '', v)

# ---------- 1. Chargement du graphe ----------
g = json.load(open(GRAPH))
tid = {t['id']: t.get('name') for t in g['types']}
inv = {v: k for k, v in tid.items()}
rtn = {r['id']: r.get('name') for r in g['relation_types']}
ent = {e['id']: e for e in g['entities']}

def av(e, k):
    a = (e.get('attributes') or {}).get(k)
    if not a: return ''
    v = a.get('value')
    return v if isinstance(v, str) else str(v)

def etypes(e): return [tid.get(t, t) for t in (e.get('types') or [])]

targets = collections.defaultdict(lambda: collections.defaultdict(list))
for r in g['relations']:
    n = rtn.get(r.get('type'), '')
    if n in ('belongs to domain', 'mentions actor', 'occurs in', 'appears in section'):
        t = ent.get(r.get('to'))
        if t: targets[r['from']][n].append(t)

rows_g = []
for e in g['entities']:
    ts = etypes(e)
    is_ie, is_ce = 'InfrastructureEvent' in ts, 'CrisisEvent' in ts
    if not (is_ie or is_ce): continue
    date, prec, brut = norm_date(av(e, 'date') or av(e, 'year'))
    tg = targets.get(e['id'], {})
    dom_raw = [t['name'] for t in tg.get('belongs to domain', [])]
    dom = ''
    for dr in dom_raw:
        k = norm_date and strip_acc(dr).lower().replace('\u2019', "'")
        if k in DOM_MAP: dom = DOM_MAP[k]; break
    sect = [t['name'] for t in tg.get('appears in section', [])]
    occ  = [f"{t['name']} [{etypes(t)[0] if etypes(t) else '?'}]" for t in tg.get('occurs in', [])]
    act  = [t['name'] for t in tg.get('mentions actor', [])]
    rows_g.append({
        'gid': e['id'], 'name': e.get('name', ''), 'norm': norm(e.get('name', '')),
        'date': date, 'precision': prec, 'date_brute': brut or av(e, 'date'),
        'kind': 'CrisisEvent' if is_ce else 'InfrastructureEvent',
        'crisis_no': re.sub(r'\D', '', av(e, 'crisisNumber')) if av(e, 'crisisNumber') else '',
        'cve': av(e, 'cveId') or av(e, 'cveReference'),
        'crisis_type': av(e, 'crisisType'), 'exploited': av(e, 'exploited'),
        'wiki': av(e, 'wikiUrl'), 'url': av(e, 'url'),
        'domaine_8': dom, 'domaine_graphe': ' | '.join(dom_raw),
        'chapter': av(e, 'chapter') or av(e, 'source') or av(e, 'thesisLocation'),
        'sections': ' | '.join(sect[:3]), 'occurs_in': ' | '.join(occ[:3]),
        'acteurs_graphe': ' | '.join(act[:4]),
        'dateSource': av(e, 'dateSource'), 'dateAuthority': av(e, 'dateAuthority'),
        'desc': re.sub(r'\s+', ' ', av(e, 'description'))[:400],
    })

# ---------- 2. Dedoublonnage interne au graphe ----------
buckets = collections.defaultdict(list)
for r in rows_g:
    key_date = r['date'][:7] if r['precision'] == 'jour' else r['date']
    buckets[(r['norm'], key_date)].append(r)

def tokset(s): return set(s.split())

def distinctifs(nom):
    """Acronymes majuscules et identifiants numeriques : deux evenements qui n'ont
    pas les memes ne peuvent pas etre fusionnes (CBOE vs CME, CVE-x vs CVE-y)."""
    n = re.sub(r'^InfrastructureEvent\s*[-\u2014]\s*', '', nom or '')
    acr = set(re.findall(r'\b[A-Z]{2,6}\b', n)) - {'BTC', 'ETH', 'USD'}
    num = set(re.findall(r'\b\d{4,6}\b', n)) - set(re.findall(r'\b(?:19|20)\d{2}\b', n))
    return acr | num

def fusionnable(a, b):
    if a['cve'] and b['cve'] and a['cve'] != b['cve']: return False
    if a['crisis_no'] and b['crisis_no'] and a['crisis_no'] != b['crisis_no']: return False
    da, db = distinctifs(a['name']), distinctifs(b['name'])
    if da and db and da != db: return False
    return True

merged, dupes = [], []
seen = set()
for r in rows_g:
    if r['gid'] in seen: continue
    grp = [r]
    for o in rows_g:
        if o['gid'] == r['gid'] or o['gid'] in seen: continue
        if o['kind'] != r['kind']: continue
        if not fusionnable(r, o): continue
        a, b = tokset(r['norm']), tokset(o['norm'])
        if not a or not b: continue
        jac = len(a & b) / len(a | b)
        same_day = r['date'] and r['date'] == o['date']
        if (jac >= 0.6 and (same_day or not (r['date'] and o['date']))) or (jac >= 0.45 and same_day):
            grp.append(o)
    for x in grp: seen.add(x['gid'])
    if len(grp) > 1:
        dupes.append(grp)
        grp.sort(key=lambda x: (x['date'] == '', -len(x['desc'])))
    base = grp[0]
    base['variantes'] = ' /// '.join(x['name'] for x in grp[1:])
    for x in grp[1:]:
        for f in ('domaine_8', 'crisis_no', 'cve', 'chapter', 'sections', 'acteurs_graphe', 'desc'):
            if not base[f] and x[f]: base[f] = x[f]
    merged.append(base)

# ---------- 3. Collision avec le catalogue de calibrage ----------
cal = list(csv.DictReader(open(CAL, encoding='utf-8'), delimiter=';'))
for c in cal: c['norm'] = norm(c['intitule'])

matches, diverg = {}, []
for c in cal:
    best, score = None, 0
    a = tokset(c['norm'])
    for m in merged:
        b = tokset(m['norm'])
        if not a or not b: continue
        j = len(a & b) / len(a | b)
        cy = (c['date'] or '')[:4]; my = (m['date'] or '')[:4]
        if cy and my and cy != my: j -= 0.25
        if j > score: best, score = m, j
    if best and score >= 0.34:
        matches[c['id']] = best['gid']
        cd, md = c['date'], best['date']
        if cd and md and cd != md and not (len(cd) < len(md) and md.startswith(cd)) \
           and not (len(md) < len(cd) and cd.startswith(md)):
            diverg.append({'id_cal': c['id'], 'intitule': c['intitule'],
                           'date_catalogue': cd, 'source_catalogue': c['source'],
                           'date_graphe': md, 'source_graphe': best['dateSource'] or best['dateAuthority'] or best['chapter'],
                           'entite_graphe': best['name']})

gid2cal = {v: k for k, v in matches.items()}

# ---------- 4. CSV unifie ----------
FIELDS = ['id','origine','date','precision','date_brute','nature','intitule','phase','domaine_8',
          'systeme','acteur_principal','acteur_secondaire','arene','type_acte','type_acte_2',
          'effet_prop_monetaires','crise','crisis_no','cve','fil','source','source_graphe',
          'acteurs_graphe','occurs_in','variantes','notes','gid']

def phase(dt):
    if not dt: return ''
    if dt < '2012-04': return 'poc'
    if dt < '2013-11': return 'peche'
    return 'maturation'

out, n = [], 0
for c in cal:
    gid = matches.get(c['id'])
    m = next((x for x in merged if x['gid'] == gid), None) if gid else None
    row = {k: c.get(k, '') for k in FIELDS if k in c}
    row.update({'id': c['id'], 'origine': 'catalogue+graphe' if m else 'catalogue',
                'gid': gid or '', 'date_brute': ''})
    if m:
        row['crisis_no'] = m['crisis_no']; row['cve'] = m['cve']
        row['source_graphe'] = (m['chapter'] + (' ; ' + m['sections'] if m['sections'] else '')).strip(' ;')
        row['acteurs_graphe'] = m['acteurs_graphe']; row['occurs_in'] = m['occurs_in']
        row['variantes'] = m.get('variantes', '')
        if not row.get('domaine_8', '').strip('*') and m['domaine_8']: row['domaine_8'] = m['domaine_8'] + '~'
    out.append(row)

for m in merged:
    if m['gid'] in gid2cal: continue
    n += 1
    out.append({
        'id': f'G{n:03d}', 'origine': 'graphe', 'date': m['date'], 'precision': m['precision'],
        'date_brute': m['date_brute'] if not m['date'] else '', 'nature': 'acte',
        'intitule': re.sub(r'^InfrastructureEvent\s*[-\u2014]\s*', '', m['name']),
        'phase': phase(m['date']), 'domaine_8': m['domaine_8'], 'systeme': '',
        'acteur_principal': '', 'acteur_secondaire': '', 'arene': '',
        'type_acte': '', 'type_acte_2': '', 'effet_prop_monetaires': 'nd',
        'crise': 'oui' if m['kind'] == 'CrisisEvent' else 'non',
        'crisis_no': m['crisis_no'], 'cve': m['cve'], 'fil': '',
        'source': 'graphe v97 (' + (m['chapter'] or 'chapitre nd') + ')',
        'source_graphe': m['sections'], 'acteurs_graphe': m['acteurs_graphe'],
        'occurs_in': m['occurs_in'], 'variantes': m.get('variantes', ''),
        'notes': ('[CHANTIER date non parsee: ' + m['date_brute'] + '] ' if not m['date'] and m['date_brute'] else '')
                 + (m['desc'][:180] if m['desc'] else ''),
        'gid': m['gid'],
    })

out.sort(key=lambda r: (r['date'] or '9999', r['id']))
with open(f'{OUT}/catalogue-evenements-v2-fusion.csv', 'w', encoding='utf-8', newline='') as f:
    w = csv.DictWriter(f, fieldnames=FIELDS, delimiter=';', extrasaction='ignore')
    w.writeheader()
    for r in out: w.writerow({k: r.get(k, '') for k in FIELDS})

with open(f'{OUT}/table-divergences-dates.csv', 'w', encoding='utf-8', newline='') as f:
    w = csv.DictWriter(f, fieldnames=['id_cal','intitule','date_catalogue','source_catalogue',
                                      'date_graphe','source_graphe','entite_graphe'], delimiter=';')
    w.writeheader()
    for r in diverg: w.writerow(r)

# ---------- 5. Rapport ----------
print('=== FUSION ===')
print(f'graphe brut         : {len(rows_g)}  (IE {sum(1 for r in rows_g if r["kind"]=="InfrastructureEvent")} / CE {sum(1 for r in rows_g if r["kind"]=="CrisisEvent")})')
print(f'apres dedoublonnage : {len(merged)}  ({len(rows_g)-len(merged)} fusionnes, {len(dupes)} groupes)')
print(f'apparies au calibrage: {len(matches)} / {len(cal)}')
print(f'TOTAL CSV v2        : {len(out)}')
print(f'divergences de dates: {len(diverg)}')
print()
print('-- couverture des colonnes analytiques a coder --')
for c in ['acteur_principal','arene','type_acte','domaine_8']:
    v = sum(1 for r in out if str(r.get(c,'')).strip())
    print(f'  {c:20s} rempli {v:3d} / {len(out)}  -> a coder {len(out)-v}')
print()
print('-- dates non parsees --')
for r in out:
    if not r['date'] and r.get('date_brute'): print('   ', r['id'], '|', r['intitule'][:60], '|', r['date_brute'][:30])
print()
print('-- groupes de doublons (top 8) --')
for grp in dupes[:8]:
    print('   *', ' /// '.join(x['name'][:58] for x in grp))
print()
print('-- repartition par annee --')
cy = collections.Counter((r['date'] or 'nd')[:4] for r in out)
print('   ', dict(sorted(cy.items())))
