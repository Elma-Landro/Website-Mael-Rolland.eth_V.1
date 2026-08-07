#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Genere section-headings-map.json : cles de section PAR POSITION pour lecteur.html.

Pourquoi : dans les chapitres I-III, les `##` du markdown ne portent aucun
numero (« Du terreau materiel et ideel aux racines de Bitcoin ») — seuls les
`#` en portent (« I.1 Quand Bitcoin definit son monde… »). Le lecteur, qui
derivait la cle de section du TEXTE du titre (`headingToSectionKey`), ne
resolvait donc jamais une sous-section de chapitre : en lisant II.2.3, le
panneau graphe restait sur II.2.

Principe : la these numerote ses sections par ORDRE d'apparition. Ce script
reutilise `scripts/derive_section_tree.py` (titres, numerote) pour attribuer
a chaque titre du markdown sa cle canonique, et ecrit la liste ordonnee des
titres par fichier. Le lecteur resout alors : « n-ieme titre de niveau k du
chapitre courant -> cle du n-ieme titre de niveau k de la carte ».

Cles produites (memes conventions que le graphe, verifie contre ses 84
`section_key`) :
    chapitres I-III   niveaux 1-2 : I.1, I.1.1, … III.4 (numerote)
    introduction      intro_A, intro_A_1, … et rangs 3-4 : intro_B_1a …
                      (lettres attribuees par position sous le `##` parent —
                      exactement ce que produisaient les regex du lecteur)
    conclusion        conclu_resume … conclu_boucs (CLES_CONCLUSION, par
                      position, au niveau qui porte les 6 sections : ## en
                      FR, ### dans la traduction EN)
Les titres sans cle canonique gardent key: "" — le lecteur retombe alors sur
`headingToSectionKey` (preambules, glossaire).

Le texte est normalise par `normalise_appariement` (minuscules, sans accents,
ponctuation -> espace) : le lecteur applique la MEME normalisation cote DOM
pour le controle d'appariement — emphase `*…*`, apostrophes typographiques,
appels de note `[^51]` s'y dissolvent des deux cotes.

Usage:
    python3 scripts/build_section_headings_map.py            # ecrit a la racine
    python3 scripts/build_section_headings_map.py --check    # verifie sans ecrire
"""
import argparse
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from grc20_commun import (  # noqa: E402
    REPO, TYPES_SECTION, graphe_le_plus_recent, normalise_appariement,
)
from derive_section_tree import (  # noqa: E402
    CLES_CONCLUSION, MD, numerote, titres,
)

# Chapitres tels que lecteur.html les nomme (CHAPTERS_DEF), avec le fichier
# charge pour chaque langue et la cle de chapitre attendue par `numerote`.
# Le glossaire n'a pas de sections dans le graphe : pas de carte.
FICHIERS_LECTEUR = [
    # (chapitre lecteur, cle numerote, fichier, langue)
    ('intro', 'intro',  '00_introduction.md',    'fr'),
    ('intro', 'intro',  '00_introduction_EN.md', 'en'),
    ('ch1',   'chap1',  '01_chapitre_I.md',      'fr'),
    ('ch1',   'chap1',  '01_chapitre_I_EN.md',   'en'),
    ('ch2',   'chap2',  '02_chapitre_II.md',     'fr'),
    ('ch2',   'chap2',  '02_chapitre_II_EN.md',  'en'),
    ('ch3',   'chap3',  '03_chapitre_III.md',    'fr'),
    ('ch3',   'chap3',  '03_chapitre_III_EN.md', 'en'),
    ('ccl',   'conclu', '04_conclusion.md',      'fr'),
    ('ccl',   'conclu', '04_conclusion_EN.md',   'en'),
]

LETTRES = 'abcdefghij'


def cles_du_graphe(chemin_graphe):
    """-> ensemble des section_key du graphe (ThesisSection ET ChapterSection)."""
    with open(chemin_graphe, encoding='utf-8') as f:
        g = json.load(f)
    nom_type = {t['id']: t.get('name') for t in g['types']}
    out = set()
    for e in g['entities']:
        types = [nom_type.get(t, t) for t in (e.get('types') or [])]
        if not any(t in TYPES_SECTION for t in types):
            continue
        a = (e.get('attributes') or {}).get('section_key')
        v = (a.get('value') if a else '') or ''
        if v:
            out.add(v)
    return out


def cles_intro(arbre, lignes):
    """Cles du graphe pour l'introduction, rangs 1 a 4, par position.

    Rangs 1-2 : depuis `numerote` ('A' -> intro_A, 'A.1' -> intro_A_1).
    Rangs 3-4 : lettres a, b, c… dans l'ordre d'apparition sous le `##`
    parent — c'est la numerotation que porte le graphe (intro_C_2a…f couvre
    des ### ET des #### entremeles, dans l'ordre du texte).
    """
    out = []
    parent = ''   # cle intro_X_N du ## courant
    lettre = 0
    for (niveau_md, _texte, _ligne), l in zip(arbre, lignes):
        cle = ''
        if niveau_md == 1 and l['cle']:
            cle = 'intro_' + l['cle']
            parent, lettre = '', 0
        elif niveau_md == 2:
            if l['cle']:
                cle = 'intro_' + l['cle'].replace('.', '_')
            parent, lettre = cle, 0
        elif niveau_md in (3, 4) and parent:
            cle = parent + LETTRES[lettre] if lettre < len(LETTRES) else ''
            lettre += 1
        out.append(cle)
    return out


def cles_conclusion(arbre):
    """CLES_CONCLUSION par position, au niveau qui porte les 6 sections.

    Le FR les ecrit en `##` ; la traduction EN en `###` (elle n'a ni # ni ##).
    """
    niveaux = {n for n, _t, _l in arbre}
    niveau_sections = 2 if 2 in niveaux else 3
    out = []
    i = 0
    for niveau_md, _texte, _ligne in arbre:
        cle = ''
        if niveau_md == niveau_sections and i < len(CLES_CONCLUSION):
            cle = CLES_CONCLUSION[i]
            i += 1
        out.append(cle)
    return out


def cles_chapitre(arbre, lignes):
    """Chapitres I-III : la cle de `numerote`, rangs markdown 1-2 seulement.

    Les rangs 3+ (I.1.1.a…) existent dans le graphe mais pas dans
    section_entities_map : les emettre changerait le comportement du lecteur
    (currentSectionKey sans entites associees). On s'arrete au rang 2,
    comme le sommaire de la these.
    """
    out = []
    for (niveau_md, _texte, _ligne), l in zip(arbre, lignes):
        out.append(l['cle'] if niveau_md <= 2 and l['cle'] else '')
    return out


def construit(chemin_graphe):
    graphe_cles = cles_du_graphe(chemin_graphe)
    fichiers = {}
    inconnues = []
    for chapitre, cle_num, nom, langue in FICHIERS_LECTEUR:
        chemin = os.path.join(MD, nom)
        if not os.path.exists(chemin):
            print(f'  ABSENT : {nom}', file=sys.stderr)
            continue
        # Le lecteur ne compte que h1-h4 (les ##### sont retires au rendu,
        # les rangs plus profonds ne sont pas observes).
        arbre = [t for t in titres(chemin) if t[0] <= 4]
        lignes = numerote(arbre, cle_num)
        assert len(lignes) == len(arbre), f'{nom}: numerote a change de forme'
        if chapitre == 'intro':
            cles = cles_intro(arbre, lignes)
        elif chapitre == 'ccl':
            cles = cles_conclusion(arbre)
        else:
            cles = cles_chapitre(arbre, lignes)
        headings = []
        for (niveau_md, texte, ligne), cle in zip(arbre, cles):
            if cle and cle not in graphe_cles:
                inconnues.append((nom, ligne, cle, texte[:60]))
            headings.append({
                'level': niveau_md,
                'line': ligne,
                'text': normalise_appariement(texte),
                'title': texte,
                'key': cle,
            })
        fichiers[nom] = {'chapter': chapitre, 'lang': langue, 'headings': headings}
    return fichiers, inconnues


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    p.add_argument('--graph', default=None)
    p.add_argument('--check', action='store_true', help='verifie sans ecrire')
    p.add_argument('--out', default=os.path.join(REPO, 'section-headings-map.json'))
    args = p.parse_args(argv)

    chemin_graphe = args.graph or graphe_le_plus_recent()
    if not chemin_graphe:
        print('aucun graphe grc20-these-mael-rolland-v*.json a la racine',
              file=sys.stderr)
        return 2

    fichiers, inconnues = construit(chemin_graphe)

    total = sum(len(f['headings']) for f in fichiers.values())
    avec_cle = sum(1 for f in fichiers.values() for h in f['headings'] if h['key'])
    print(f'{len(fichiers)} fichiers, {total} titres, {avec_cle} avec cle canonique')
    for nom, f in fichiers.items():
        n = sum(1 for h in f['headings'] if h['key'])
        print(f"  {nom:26s} {f['chapter']:6s} {len(f['headings']):3d} titres, {n:3d} cles")

    if inconnues:
        print(f'\nERREUR : {len(inconnues)} cle(s) emise(s) absentes du graphe '
              f'({os.path.basename(chemin_graphe)}) :', file=sys.stderr)
        for nom, ligne, cle, texte in inconnues:
            print(f'  {nom} l.{ligne} {cle} — {texte}', file=sys.stderr)
        return 1

    if args.check:
        print('\n--check : rien ecrit.')
        return 0

    doc = {
        '_comment': ('Cles de section par POSITION pour lecteur.html. Genere '
                     'par scripts/build_section_headings_map.py — ne pas '
                     'editer a la main ; regenerer apres tout changement des '
                     'titres de assets/MD/ ou des section_key du graphe.'),
        'generated_by': 'scripts/build_section_headings_map.py',
        'source_graph': os.path.basename(chemin_graphe),
        'files': fichiers,
    }
    with open(args.out, 'w', encoding='utf-8') as f:
        json.dump(doc, f, ensure_ascii=False, indent=1)
        f.write('\n')
    print(f'\necrit : {os.path.relpath(args.out, REPO)}')
    return 0


if __name__ == '__main__':
    sys.exit(main())
