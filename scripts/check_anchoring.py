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
    B. toute cle de section des cartes correspond a un ThesisSection
    C. tout id epingle existe ET figure dans la liste de sa section
    D. tout id et tout focusNode de narrative-anchors resout
    E. toute reference de story resout (table d'alias appliquee)
    F. tout allowedRelationTypes de story existe dans relation_types

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
import argparse, glob, json, os, re, sys, unicodedata, collections

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def plus_recent():
    fichiers = glob.glob(os.path.join(REPO, 'grc20-these-mael-rolland-v*.json'))
    def num(f):
        m = re.search(r'-v(\d+)\.json$', f)
        return int(m.group(1)) if m else -1
    return max(fichiers, key=num) if fichiers else None

p = argparse.ArgumentParser(description="Controle d'integrite de la couche d'ancrage.")
p.add_argument('--graph', '-g', default=None,
               help="Graphe cible (defaut : la version la plus recente presente).")
p.add_argument('--baseline', default=os.path.join(REPO, 'docs', 'audits', 'data',
                                                  'anchoring-baseline.json'))
p.add_argument('--write-baseline', action='store_true',
               help="Fige l'etat courant comme reference et sort en 0.")
p.add_argument('--no-baseline', action='store_true',
               help="Ignore la baseline : echoue sur toute la dette.")
p.add_argument('--quiet', '-q', action='store_true')
args = p.parse_args()

chemin_graphe = args.graph or plus_recent()
if not chemin_graphe or not os.path.exists(chemin_graphe):
    print("ERREUR : aucun graphe trouve. Utilisez --graph.", file=sys.stderr)
    sys.exit(2)

def charger(nom, obligatoire=True):
    c = os.path.join(REPO, nom)
    if not os.path.exists(c):
        if obligatoire:
            print(f"ERREUR : {nom} introuvable.", file=sys.stderr)
            sys.exit(2)
        return None
    try:
        with open(c, encoding='utf-8') as f:
            return json.load(f)
    except json.JSONDecodeError as e:
        print(f"ERREUR : {nom} n'est pas du JSON valide ({e}).", file=sys.stderr)
        sys.exit(2)

with open(chemin_graphe, encoding='utf-8') as f:
    g = json.load(f)

nom_type = {t['id']: t.get('name') for t in g.get('types', [])}
ids = {e['id'] for e in g.get('entities', [])}
noms = {}
for e in g.get('entities', []):
    noms.setdefault(e.get('name'), e['id'])
types_relation = {r.get('name') for r in g.get('relation_types', [])}

def attr(e, k):
    a = (e.get('attributes') or {}).get(k)
    return (a.get('value') if a else '') or ''

cles_section = {}
for e in g.get('entities', []):
    if 'ThesisSection' in [nom_type.get(t, t) for t in (e.get('types') or [])]:
        k = attr(e, 'section_key')
        if k:
            cles_section[k] = e['id']

esm = charger('entity_section_map.json')
sem = charger('section_entities_map.json')
ovr = charger('section_overrides.json', obligatoire=False) or {}
anc = charger('narrative-anchors.json', obligatoire=False) or {}

problemes = []   # (code, categorie, detail)

def signale(code, categorie, detail):
    problemes.append((code, categorie, detail))

# ---------- A. identifiants des cartes ----------
for eid in esm:
    if eid not in ids:
        signale(f'A:esm:{eid}', 'entite de entity_section_map absente du graphe',
                f"{eid} — « {(esm[eid] or {}).get('name', '?')} »")

vus_sem = set()
for cle, bloc in sem.items():
    for ent in (bloc or {}).get('entities', []):
        eid = ent.get('entity_id')
        if eid and eid not in ids and eid not in vus_sem:
            vus_sem.add(eid)
            signale(f'A:sem:{eid}', 'entite de section_entities_map absente du graphe',
                    f"{eid} — « {ent.get('entity_name', '?')} » (section {cle})")

# ---------- B. cles de section ----------
for cle in sem:
    if cle not in cles_section and not cle.endswith('_preamble'):
        signale(f'B:sem:{cle}', 'cle de section_entities_map sans ThesisSection', cle)
for cle in cles_section:
    if cle not in sem:
        signale(f'B:graph:{cle}', 'ThesisSection sans entree dans section_entities_map', cle)

# ---------- C. epinglages ----------
for cle, liste in ovr.items():
    if cle.startswith('_') or not isinstance(liste, list):
        continue
    if cle not in sem:
        signale(f'C:cle:{cle}', 'section epinglee inconnue de section_entities_map', cle)
        continue
    presents = {e.get('entity_id') for e in (sem[cle] or {}).get('entities', [])}
    for eid in liste:
        if eid not in ids:
            signale(f'C:abs:{cle}:{eid}', 'entite epinglee absente du graphe',
                    f"{eid} (section {cle})")
        elif eid not in presents:
            signale(f'C:hors:{cle}:{eid}', 'entite epinglee hors de la liste de sa section',
                    f"{eid} (section {cle})")

# ---------- D. narrative-anchors ----------
for a in anc.get('anchors', []):
    for champ in ('sourceQuoteId', 'primaryEntityId'):
        v = a.get(champ)
        if v and v not in ids:
            signale(f'D:{champ}:{v}', f'narrative-anchors : {champ} non resolu', v)
    for v in (a.get('secondaryEntityIds') or []):
        if v not in ids:
            signale(f'D:sec:{v}', 'narrative-anchors : secondaryEntityId non resolu', v)
    for n in ((a.get('graphScene') or {}).get('focusNodes') or []):
        if n not in noms:
            signale(f'D:focus:{n}', 'narrative-anchors : focusNode non resolu (par nom)', n)

# ---------- E/F. story-presets ----------
def sans_accents(s):
    s = unicodedata.normalize('NFD', s or '')
    return ''.join(c for c in s if unicodedata.category(c) != 'Mn')

def normalise(s):
    return sans_accents(s).lower().replace('’', "'").strip()

par_norme = collections.defaultdict(list)
for n in noms:
    par_norme[normalise(n)].append(n)

chemin_sp = os.path.join(REPO, 'story-presets.mjs')
chemin_sh = os.path.join(REPO, 'graphe.story-helpers.js')
if os.path.exists(chemin_sp):
    src_sp = open(chemin_sp, encoding='utf-8').read()
    alias = {}
    if os.path.exists(chemin_sh):
        m = re.search(r'STORY_FOCUS_ALIASES\s*=\s*\{(.*?)\n\s*\};',
                      open(chemin_sh, encoding='utf-8').read(), re.S)
        if m:
            alias = dict(re.findall(r"'([^']+)'\s*:\s*'([^']+)'", m.group(1)))

    refs = set()
    for bloc in re.findall(r'(?:focusNodes|centralNode)\s*:\s*(\[[^\]]*\]|\'[^\']*\')',
                           src_sp, re.S):
        refs |= set(re.findall(r"'([^']{3,})'", bloc))
    for r in sorted(refs):
        c = alias.get(r, r)
        if c in ids or c in noms or r in ids or r in noms:
            continue
        if par_norme.get(normalise(c)) or par_norme.get(normalise(r)):
            continue
        signale(f'E:focus:{r}', 'story-presets : focusNode non resolu', r)

    for bloc in re.findall(r'allowedRelationTypes\s*:\s*\[([^\]]*)\]', src_sp, re.S):
        for rt in re.findall(r"'([^']+)'", bloc):
            if rt not in types_relation:
                signale(f'F:rel:{rt}', 'story-presets : relation_type inexistant', rt)

# ---------- baseline ----------
codes = {c for c, _, _ in problemes}
base = set()
if not args.no_baseline and os.path.exists(args.baseline):
    with open(args.baseline, encoding='utf-8') as f:
        base = set(json.load(f).get('known', []))

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
    sys.exit(0)

# ---------- rapport ----------
if not args.quiet:
    print(f"graphe   : {os.path.basename(chemin_graphe)} "
          f"({len(ids)} entites, {len(cles_section)} ThesisSection avec section_key)")
    print(f"artefacts: entity_section_map {len(esm)} · section_entities_map {len(sem)} · "
          f"overrides {sum(1 for k in ovr if not k.startswith('_'))} · "
          f"narrative-anchors {len(anc.get('anchors', []))}")
    print()
    # Compter les problemes DISTINCTS (par code), pas les occurrences : un meme
    # type de relation cite dans cinq stories est un probleme, pas cinq.
    cat_par_code = {}
    for c, cat, _ in problemes:
        cat_par_code.setdefault(c, cat)
    par_cat = collections.Counter(cat_par_code.values())
    if par_cat:
        print(f"problemes distincts detectes : {len(cat_par_code)}")
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
    sys.exit(1)

if not args.quiet:
    print("OK — aucune regression.")
sys.exit(0)
