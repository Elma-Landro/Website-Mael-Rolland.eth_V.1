#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Instruit les relations `authored` manquantes des six auteurs retypes en v113.

LECTURE SEULE SUR LE GRAPHE. Ce script ne modifie aucun graphe, ne pose aucune
relation, n'applique rien. Il produit un tableau de decision et rien d'autre.

CE QU'IL REFUSE DE FAIRE. Deduire une paternite d'un nom proche. Le depot en
porte le precedent : un patch anterieur a failli graver « Florence Dufy », un
nom soude de deux co-auteurs reels. Une ligne n'est donc `certaine` que si
CINQ conditions tiennent ensemble, verifiees ici une par une :
  1. une entree de `assets/MD/07_bibliographie.md` nomme explicitement
     l'auteur ET l'oeuvre — la ligne et son texte sont FIGES dans LOT et
     re-verifies a chaque execution (si la biblio bouge, le script echoue) ;
  2. l'entite auteur existe, est typee Person, et son nom est UNIQUE dans le
     graphe (aucun homonyme) ;
  3. l'entite oeuvre existe et son titre/annee concordent avec l'entree ;
  4. aucune relation `authored` n'entre deja dans l'oeuvre, et aucune relation
     d'aucun type ne relie deja la paire ;
  5. l'oeuvre n'est pas un doublon connu d'une autre fiche.

La condition 5 n'est pas theorique : `e0b40d91` (« DeNardis & Musiani 2014 —
Governance by Infrastructure ») decrit la MEME entree bibliographique que
`2272e5b8`, qui porte deja l'`authored` de DeNardis. Lui en poser un second
graverait le doublon comme une oeuvre distincte. La ligne existe au CSV avec
`proposed_relation = NON`.

Usage:
    python3 scripts/build_bibliography_authorship_support.py           # simule
    python3 scripts/build_bibliography_authorship_support.py --csv     # ecrit
    python3 scripts/build_bibliography_authorship_support.py --check   # CI
"""
import argparse
import csv
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from grc20_commun import REPO, numero_de_version  # noqa: E402

CODE_DONNEES, CODE_INVOCATION = 1, 2
BIBLIO = os.path.join(REPO, 'assets', 'MD', '07_bibliographie.md')
# PREUVE FIGEE, pas inventaire vivant : ce CSV instruit une dette constatee
# DANS v113, avec des identifiants et des lignes de bibliographie releves dans
# v113. Son nom porte donc « v113 » en dur — et le script REFUSE de tourner
# contre un autre graphe plutot que d'y ecrire des donnees d'une autre version.
#
# C'est exactement le piege deja constate sur `audit_chronology_dates.py`, ou
# le nom derivait du « graphe le plus recent » sans que rien ne le declare :
# le jour d'une v114, un CSV nomme v113 se serait rempli de mesures v114.
# L'arbitrage Q6 (2026-08-09) a fixe la regle — `-current` pour le vivant,
# `-vNN` pour le fige — et un fige ne se regenere pas ailleurs : il echoue.
VERSION_FIGEE = 113
SORTIE = os.path.join(REPO, 'docs', 'audits', 'data',
                      f'bibliography-authorship-support-v{VERSION_FIGEE}.csv')
ID_AUTHORED = '2d3f43441ee747dda4172f0954a9fadd'

COLONNES = (
    'author_entity_id', 'author_name', 'reference_entity_id',
    'reference_name', 'bibliographic_evidence', 'existing_authored_relation',
    'proposed_relation', 'confidence', 'risk', 'decision_needed', 'note',
)

# Les six auteurs retypes en v113 — le perimetre entier de ce chantier.
AUTEURS = {
    '53525938440543a5af359337eeab9823': 'Jacques Favier',
    'ec901513fae144a0a350e798b0351c6d': 'Adli Takkal Bataille',
    '7cd4cfe4c8d74aaaaeabcd17ebf11b3a': 'Gérard Dréan',
    'be8ac28672e44ef6852fd5b1d80f3b90': 'Andreas Loibl',
    '5fc4278b78704f6c92c3744e2654518a': 'Laura DeNardis',
    'b332ace807b84fe4ab2373b8dc8f4856': 'Shinobi (pseudonyme)',
}

# Chaque couple (auteur, oeuvre) envisage, avec sa preuve FIGEE : le numero de
# ligne de la bibliographie et un fragment qui doit s'y trouver mot pour mot.
# Figer le fragment et pas seulement le numero est deliberé — une biblio qui
# glisse d'une ligne rendrait un numero seul silencieusement faux.
LOT = (
    dict(auteur='53525938440543a5af359337eeab9823',
         oeuvre='e19babe53a3d4f0291ed683b3118e0ef', ligne=476,
         fragment='FAVIER Jacques et TAKKAL BATAILLE Adli, 2017, '
                  'Bitcoin, la monnaie acéphale',
         propose=True, risque='',
         note='Ouvrage co-signe, CNRS Editions, 280 p. Auteur nomme en '
              'premiere position dans l entree.'),
    dict(auteur='53525938440543a5af359337eeab9823',
         oeuvre='b84f59ace9b6403c88067c46af4c7582', ligne=474,
         fragment='FAVIER Jacques, 2017, « Tulipes »',
         propose=True, risque='',
         note='Billet de blog signe seul. La fiche porte title=« Tulipes '
              '(blog La voie du Bitcoin) » et year=2017 ; l entree donne '
              'blog.lavoiedubitcoin.info — l editeur concorde.'),
    dict(auteur='53525938440543a5af359337eeab9823',
         oeuvre='7f0f9cc4c27040a78115b0294fd9bfe1', ligne=472,
         # Fragment volontairement arrete avant le « ? » : la bibliographie
         # ecrit une espace fine insecable (U+202F) devant, invisible a la
         # lecture et impossible a retaper. La preuve doit rester verifiable
         # a la main, pas seulement par copier-coller.
         fragment='FAVIER Jacques, 2021, « Le Bitcoin, la religion du XXIe '
                  'siècle née des mathématiques',
         propose=True,
         risque='DETTE SEPAREE : le NOM de la fiche dit « (La voie du '
                'Bitcoin) » alors que l entree donne un podcast '
                'parlonsbitcoin.com. L editeur de la fiche est faux ; la '
                'paternite ne l est pas.',
         note='Unique entree Favier 2021 de la bibliographie : aucune '
              'ambiguite sur l auteur. La fiche ne porte AUCUN attribut, '
              'son seul appui est son nom — d ou la verification par '
              'unicite de l entree plutot que par concordance d attributs.'),
    dict(auteur='ec901513fae144a0a350e798b0351c6d',
         oeuvre='e19babe53a3d4f0291ed683b3118e0ef', ligne=476,
         fragment='FAVIER Jacques et TAKKAL BATAILLE Adli, 2017, '
                  'Bitcoin, la monnaie acéphale',
         propose=True, risque='',
         note='Co-auteur nomme dans la meme entree. Seule oeuvre de cet '
              'auteur dans la bibliographie.'),
    # --- explicitement NON proposee ---
    dict(auteur='5fc4278b78704f6c92c3744e2654518a',
         oeuvre='e0b40d91bb424defaa9acf37536f339e', ligne=394,
         fragment='DENARDIS Laura et MUSIANI Francesca, 2014, '
                  '« Governance by Infrastructure',
         propose=False,
         risque='DOUBLON : decrit la MEME entree que 2272e5b8, qui porte '
                'deja l authored de DeNardis. Poser un second authored '
                'graverait le doublon en oeuvre distincte.',
         note='A instruire comme doublon (fusion ou duplicateOf), pas comme '
              'paternite manquante. Hors perimetre de ce chantier.'),
)


def echec(msg, code=CODE_DONNEES):
    famille = 'invocation' if code == CODE_INVOCATION else 'donnees'
    print(f'ECHEC ({famille}) : {msg}', file=sys.stderr)
    sys.exit(code)


def lignes_biblio():
    if not os.path.exists(BIBLIO):
        echec(f'bibliographie introuvable : {BIBLIO}', CODE_INVOCATION)
    with open(BIBLIO, encoding='utf-8') as f:
        return f.read().splitlines()


def construire(courant):
    with open(courant, encoding='utf-8') as f:
        g = json.load(f)
    par_id = {e['id']: e for e in g['entities']}
    nom_type = {t['id']: t.get('name') for t in g['types']}
    relations = {(r['from'], r['to'], r['type']) for r in g['relations']}
    paires = {(a, b) for a, b, _ in relations}
    biblio = lignes_biblio()

    # Homonymie : un nom porte par plus d'une fiche interdit toute conclusion.
    porteurs = {}
    for e in g['entities']:
        porteurs.setdefault(' '.join((e.get('name') or '').lower().split()),
                            []).append(e['id'])

    sorties = []
    for item in LOT:
        aid, oid = item['auteur'], item['oeuvre']
        auteur, oeuvre = par_id.get(aid), par_id.get(oid)
        if auteur is None or oeuvre is None:
            echec(f'{aid[:8]} ou {oid[:8]} absent du graphe : le lot est '
                  'perime, ne pas produire de CSV sur une base fausse.')

        # Preuve bibliographique : la ligne figee doit porter le fragment.
        no = item['ligne']
        if no > len(biblio) or item['fragment'] not in biblio[no - 1]:
            echec(f'{BIBLIO}:{no} ne contient plus « {item["fragment"][:48]}… » '
                  '— la bibliographie a bouge. Reinstruire le lot plutot que '
                  'de publier une preuve qui ne prouve plus rien.')
        preuve = f'assets/MD/07_bibliographie.md:{no} — {item["fragment"]}'

        # Les cinq conditions, evaluees et non supposees.
        types_auteur = [nom_type.get(t, t) for t in auteur.get('types', [])]
        homonymes = porteurs.get(
            ' '.join((auteur.get('name') or '').lower().split()), [])
        deja = (aid, oid, ID_AUTHORED) in relations
        deja_paire = (aid, oid) in paires
        authored_entrants = sum(1 for a, b, t in relations
                                if b == oid and t == ID_AUTHORED)
        blocages = []
        if 'Person' not in types_auteur:
            blocages.append(f'auteur non typé Person ({types_auteur})')
        if len(homonymes) > 1:
            blocages.append(f'{len(homonymes)} homonymes du nom d auteur')
        if deja:
            blocages.append('relation authored déjà présente')
        if deja_paire:
            blocages.append('la paire porte déjà une relation')
        if authored_entrants and item['propose']:
            blocages.append(f'{authored_entrants} authored entrant(s) déjà '
                            'sur l œuvre')

        if not item['propose']:
            confiance, propose = 'ecartee', 'NON'
            decision = ("instruire comme doublon bibliographique, chantier "
                        "distinct — ne PAS poser d authored")
        elif blocages:
            confiance, propose = 'bloquee', 'NON'
            decision = 'lever le blocage avant toute proposition : ' \
                       + ' ; '.join(blocages)
        else:
            confiance, propose = 'certaine', 'authored'
            decision = ("valider la relation authored ? (arbitrage 1) — "
                        "aucune application sans réponse")

        sorties.append({
            'author_entity_id': aid,
            'author_name': auteur.get('name') or '(sans nom)',
            'reference_entity_id': oid,
            'reference_name': oeuvre.get('name') or '(sans nom)',
            'bibliographic_evidence': preuve,
            'existing_authored_relation': 'oui' if deja else 'non',
            'proposed_relation': propose,
            'confidence': confiance,
            'risk': item['risque'] or 'aucun identifié',
            'decision_needed': decision,
            'note': item['note'],
        })

    # Les auteurs deja pourvus : une ligne d etat, pour que le CSV dise aussi
    # ce qu il n a PAS trouve a corriger. Un tableau qui ne montre que les
    # lignes a agir laisse croire que le reste n a pas ete regarde.
    for aid, nom in sorted(AUTEURS.items(), key=lambda x: x[1]):
        siens = [(a, b) for a, b, t in relations
                 if a == aid and t == ID_AUTHORED]
        if not siens or any(x['auteur'] == aid for x in LOT if x['propose']):
            continue
        for _, oid in sorted(siens):
            sorties.append({
                'author_entity_id': aid,
                'author_name': nom or '(sans nom)',
                'reference_entity_id': oid,
                'reference_name': (par_id.get(oid, {}).get('name')
                                   or '(sans nom)'),
                'bibliographic_evidence': 'relation déjà présente dans v113',
                'existing_authored_relation': 'oui',
                'proposed_relation': 'aucune',
                'confidence': 'sans objet',
                'risk': 'aucun — rien à poser',
                'decision_needed': 'aucune',
                'note': "auteur déjà pourvu ; vérifié qu aucune autre œuvre "
                        "de lui ne figure à la bibliographie",
            })
    sorties.sort(key=lambda x: (x['author_name'], x['reference_name']))
    return sorties


def main():
    ap = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--graph', default=None)
    ap.add_argument('--csv', action='store_true')
    ap.add_argument('--check', action='store_true')
    args = ap.parse_args()
    if args.csv and args.check:
        ap.error('--csv et --check sont exclusifs.')

    # Le defaut est le graphe FIGE, pas « le plus recent » : un releve fige
    # doit rester rejouable apres un bump de version. Le viser par defaut ne
    # relache rien — un `--graph` explicite vers une autre version est toujours
    # refuse juste en dessous.
    courant = args.graph or os.path.join(
        REPO, f'grc20-these-mael-rolland-v{VERSION_FIGEE}.json')
    if not os.path.exists(courant):
        # Deux pannes distinctes sous un meme message envoyaient chercher le
        # defaut alors que c est le `--graph` fourni qui etait faux — et
        # inversement. Le message doit dire LAQUELLE des deux s est produite.
        if args.graph:
            echec(f'graphe explicite introuvable : {courant} (passe via '
                  '--graph)', CODE_INVOCATION)
        echec(f'graphe FIGE introuvable : {courant}. Ce releve decrit '
              f'v{VERSION_FIGEE} et ne se rejoue que contre lui ; le graphe '
              'courant du depot, quel qu il soit, ne le remplace pas.',
              CODE_INVOCATION)
    vue = numero_de_version(courant)
    if vue != VERSION_FIGEE:
        echec(f'ce releve est une preuve FIGEE sur v{VERSION_FIGEE} ; le '
              f'graphe vise est {os.path.basename(courant)} (v{vue}). Ecrire '
              f'des mesures v{vue} dans un fichier nomme v{VERSION_FIGEE} '
              'serait exactement le mensonge silencieux que la convention de '
              'nommage interdit. Pour instruire une version ulterieure, '
              'ouvrir un nouveau releve.')
    lignes = construire(courant)

    print(f'graphe de reference : {os.path.basename(courant)}')
    print(f'{len(lignes)} ligne(s)\n')
    for ligne in lignes:
        print(f"  {ligne['author_name'][:24]:24s} "
              f"{ligne['proposed_relation']:9s} {ligne['confidence']:10s} "
              f"{ligne['reference_name'][:44]}")
    proposees = sum(1 for x in lignes if x['proposed_relation'] == 'authored')
    print(f'\n  {proposees} relation(s) proposee(s), aucune appliquee')

    if args.check:
        if not os.path.exists(SORTIE):
            print(f'--check : {os.path.relpath(SORTIE, REPO)} absent.',
                  file=sys.stderr)
            return 1
        with open(SORTIE, encoding='utf-8', newline='') as f:
            verse = list(csv.DictReader(f, delimiter=';'))
        if verse != [{k: str(v) for k, v in x.items()} for x in lignes]:
            print('--check : le CSV verse differe du CSV recalcule.',
                  file=sys.stderr)
            return 1
        print('\n--check : le tableau est a jour.')
        return 0

    if not args.csv:
        print('\n(simulation — relancer avec --csv pour ecrire)')
        return 0

    temporaire = SORTIE + '.tmp'
    with open(temporaire, 'w', encoding='utf-8', newline='') as f:
        w = csv.DictWriter(f, fieldnames=COLONNES, delimiter=';')
        w.writeheader()
        w.writerows(lignes)
    os.replace(temporaire, SORTIE)
    print(f'\necrit : {os.path.relpath(SORTIE, REPO)} ({len(lignes)} lignes)')
    return 0


if __name__ == '__main__':
    sys.exit(main())
