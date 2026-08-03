#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Derive l'arborescence canonique des sections depuis les markdown de la these.

Aucun ecrit. Sert de verite terrain avant toute renumerotation du graphe.

Principe : la these numerote elle-meme ses sections. Le corps du chapitre I
l'enonce (l. 99) — « (sect. I.1.1) … (sect. I.1.2) … (sect. I.1.3) » — et
designe ainsi les trois titres de niveau 2 places sous `# I.1`. Le niveau
canonique est donc `##`, pas `###`.

Le script extrait l'arbre des titres, attribue la numerotation a ce niveau,
et confronte le resultat aux ThesisSection du graphe pour produire une table
de correspondance revisable a la main.

Usage:
    python3 scripts/derive_section_tree.py
    python3 scripts/derive_section_tree.py --csv docs/audits/data/section-tree.csv
"""
import argparse
import csv
import json
import os
import re
import sys
import unicodedata

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MD = os.path.join(REPO, 'assets', 'MD')

FICHIERS = [
    ('intro', '00_introduction.md'),
    ('chap1', '01_chapitre_I.md'),
    ('chap2', '02_chapitre_II.md'),
    ('chap3', '03_chapitre_III.md'),
    ('conclu', '04_conclusion.md'),
]


def sans_accents(s):
    s = unicodedata.normalize('NFD', s or '')
    return ''.join(c for c in s if unicodedata.category(c) != 'Mn')


def normalise(s):
    s = sans_accents(s).lower().replace('’', "'")
    s = re.sub(r'[^a-z0-9 ]', ' ', s)
    return ' '.join(s.split())


def titres(chemin):
    """-> [(niveau, texte, ligne)] en ignorant les blocs de code."""
    out = []
    dans_code = False
    with open(chemin, encoding='utf-8') as f:
        for i, brute in enumerate(f, 1):
            if brute.lstrip().startswith('```'):
                dans_code = not dans_code
                continue
            if dans_code:
                continue
            m = re.match(r'^(#{1,6})\s+(.*?)\s*$', brute)
            if m:
                out.append((len(m.group(1)), m.group(2), i))
    return out


def numerote(arbre, cle_chapitre):
    """Attribue la numerotation canonique au niveau `##`.

    Un `#` portant deja un numero (« I.1 Quand Bitcoin… ») le conserve ; ses
    `##` heritent de ce prefixe, numerotes dans l'ordre. Les `#` sans numero
    (introduction, conclusion) recoivent une lettre ou une cle nommee.
    """
    lignes = []
    prefixe_courant = None
    compteur = 0
    for niveau, texte, ligne in arbre:
        m = re.match(r'^((?:[IVX]+\.\d+)|(?:[A-E]))[.)]?\s+(.*)$', texte)
        if niveau == 1:
            if m:
                prefixe_courant = m.group(1)
                titre = m.group(2)
            else:
                prefixe_courant = None
                titre = texte
            compteur = 0
            lignes.append({'niveau': 1, 'cle': prefixe_courant or '',
                           'titre': titre, 'ligne': ligne, 'chapitre': cle_chapitre})
        elif niveau == 2:
            # Un `##` peut porter son propre numero de tete — « I.4 Conclusion du
            # Chapitre I » est une section de rang 1, pas la 4e fille de I.3. Le
            # markdown est irregulier sur ce point ; on suit le libelle.
            m2 = re.match(r'^([IVX]+\.\d+)\s+(.*)$', texte)
            if m2:
                prefixe_courant = m2.group(1)
                compteur = 0
                lignes.append({'niveau': 1, 'cle': m2.group(1), 'titre': m2.group(2),
                               'ligne': ligne, 'chapitre': cle_chapitre,
                               'note': 'h2 portant un numero de tete'})
                continue
            compteur += 1
            if cle_chapitre == 'conclu' and compteur <= len(CLES_CONCLUSION):
                cle = CLES_CONCLUSION[compteur - 1]
            else:
                cle = f'{prefixe_courant}.{compteur}' if prefixe_courant else ''
            lignes.append({'niveau': 2, 'cle': cle, 'titre': texte,
                           'ligne': ligne, 'chapitre': cle_chapitre})
        else:
            lignes.append({'niveau': niveau, 'cle': '', 'titre': texte,
                           'ligne': ligne, 'chapitre': cle_chapitre})
    return lignes


# La conclusion ne porte ni lettre ni numero dans son markdown : ses six
# sections sont nommees. Les cles du graphe leur correspondent deja, dans
# l'ordre du texte. On l'ecrit ici plutot que de le rededuire ailleurs.
CLES_CONCLUSION = [
    'conclu_resume',       # Resume de la these
    'conclu_infra',        # Decrypter la Crypto par l'approche infrastructurelle
    'conclu_aceph',        # De l'acephalisme apolitique des CM...
    'conclu_theo_mon',     # Une integration coherente des CM... theorie monetaire
    'conclu_traduction',   # Un effort de traduction attentif aux... acteurs
    'conclu_boucs',        # Les CM : boucs emissaires commodes...
]


def cles_equivalentes(cle, chapitre):
    """Les conventions de cle du graphe pour une cle canonique donnee.

    Le depot n'a aucun registre de correspondance : le graphe emploie
    `intro_A` / `intro_A_1`, la these ecrit « A. » / « A.1 ». Cette fonction
    est le pont, et le seul endroit ou il est ecrit.
    """
    out = {cle}
    if chapitre == 'intro':
        out.add('intro_' + cle.replace('.', '_'))
    if chapitre == 'conclu':
        out.add(cle)   # deja nommee par CLES_CONCLUSION
    return out


def sections_du_graphe(chemin_graphe):
    with open(chemin_graphe, encoding='utf-8') as f:
        g = json.load(f)
    nom_type = {t['id']: t.get('name') for t in g['types']}
    out = []
    for e in g['entities']:
        if 'ThesisSection' not in [nom_type.get(t, t) for t in (e.get('types') or [])]:
            continue
        a = (e.get('attributes') or {}).get('section_key')
        out.append({
            'id': e['id'],
            'nom': e.get('name', ''),
            'section_key': (a.get('value') if a else '') or '',
        })
    return out


def main(argv=None):
    p = argparse.ArgumentParser(description="Arborescence canonique des sections.")
    p.add_argument('--graph', default=None)
    p.add_argument('--csv', default=None, help="Ecrit la table de correspondance.")
    args = p.parse_args(argv)

    graphe = args.graph
    if not graphe:
        import glob
        c = glob.glob(os.path.join(REPO, 'grc20-these-mael-rolland-v*.json'))
        graphe = max(c, key=lambda f: int(re.search(r'-v(\d+)\.json$', f).group(1)))

    toutes = []
    print('=== arborescence des titres, par fichier ===')
    for cle, nom in FICHIERS:
        chemin = os.path.join(MD, nom)
        if not os.path.exists(chemin):
            print(f'  {nom} : ABSENT')
            continue
        arbre = titres(chemin)
        lignes = numerote(arbre, cle)
        toutes += lignes
        par_niveau = {}
        for l in lignes:
            par_niveau[l['niveau']] = par_niveau.get(l['niveau'], 0) + 1
        numerotees = sum(1 for l in lignes if l['cle'] and l['niveau'] == 2)
        print(f"  {nom:24s} h1 {par_niveau.get(1,0):3d} · h2 {par_niveau.get(2,0):3d} · "
              f"h3 {par_niveau.get(3,0):3d} · h4+ {sum(v for k,v in par_niveau.items() if k>=4):3d}"
              f"   -> {numerotees} sections canoniques (##)")

    canoniques = [l for l in toutes if l['niveau'] == 2 and l['cle']]
    tetes = [l for l in toutes if l['niveau'] == 1 and l['cle']]
    print()
    print(f"sections canoniques au niveau ## : {len(canoniques)}")
    print(f"sections de tete au niveau #     : {len(tetes)}")

    graphe_sections = sections_du_graphe(graphe)
    par_cle = {s['section_key']: s for s in graphe_sections if s['section_key']}
    print(f"ThesisSection dans {os.path.basename(graphe)} : {len(graphe_sections)} "
          f"({len(par_cle)} avec section_key)")
    print()

    print('=== confrontation : cle canonique -> etat dans le graphe ===')
    lignes_csv = []
    for l in tetes + canoniques:
        cle = l['cle']
        g = None
        for variante in cles_equivalentes(cle, l['chapitre']):
            if variante in par_cle:
                g = par_cle[variante]
                break
        if g:
            etat = 'PRESENTE'
            # le titre correspond-il ?
            if normalise(l['titre'])[:40] and normalise(l['titre'])[:40] not in normalise(g['nom']):
                etat = 'PRESENTE_TITRE_DIVERGENT'
        else:
            etat = 'ABSENTE'
        lignes_csv.append({
            'cle_canonique': cle, 'niveau': l['niveau'], 'chapitre': l['chapitre'],
            'titre_md': l['titre'], 'ligne_md': l['ligne'], 'etat': etat,
            'id_graphe': g['id'] if g else '', 'nom_graphe': g['nom'] if g else '',
        })

    cles_can = set()
    for l in tetes + canoniques:
        cles_can |= cles_equivalentes(l['cle'], l['chapitre'])
    for s in graphe_sections:
        if s['section_key'] and s['section_key'] not in cles_can:
            lignes_csv.append({
                'cle_canonique': '', 'niveau': '', 'chapitre': '', 'titre_md': '',
                'ligne_md': '', 'etat': 'GRAPHE_SANS_EQUIVALENT_MD',
                'id_graphe': s['id'], 'nom_graphe': s['nom'],
            })
        elif not s['section_key']:
            lignes_csv.append({
                'cle_canonique': '', 'niveau': '', 'chapitre': '', 'titre_md': '',
                'ligne_md': '', 'etat': 'GRAPHE_SANS_SECTION_KEY',
                'id_graphe': s['id'], 'nom_graphe': s['nom'],
            })

    import collections
    c = collections.Counter(r['etat'] for r in lignes_csv)
    for etat, n in c.most_common():
        print(f'  {n:4d}  {etat}')
    print()
    for r in lignes_csv:
        if r['etat'] == 'ABSENTE':
            print(f"  ABSENTE  {r['cle_canonique']:10s} l.{r['ligne_md']:<5} {r['titre_md'][:64]}")

    if args.csv:
        os.makedirs(os.path.dirname(args.csv), exist_ok=True)
        with open(args.csv, 'w', encoding='utf-8', newline='') as f:
            w = csv.DictWriter(f, delimiter=';', fieldnames=[
                'cle_canonique', 'niveau', 'chapitre', 'titre_md', 'ligne_md',
                'etat', 'id_graphe', 'nom_graphe'])
            w.writeheader()
            w.writerows(lignes_csv)
        print()
        print(f"table ecrite : {os.path.relpath(args.csv, REPO)} ({len(lignes_csv)} lignes)")
    return 0


if __name__ == '__main__':
    sys.exit(main())
