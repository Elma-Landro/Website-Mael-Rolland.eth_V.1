#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Instruit la correction du libelle de la fiche `7f0f9cc4` (Favier 2021).

LECTURE SEULE. Ne modifie aucun graphe, aucune carte, aucun patch. Produit un
tableau de decision et rien d'autre.

LE CONSTAT. La fiche s'appelle « Favier 2021 — Bitcoin et la religion (La voie
du Bitcoin) ». Or l'unique entree Favier 2021 de la bibliographie
(`assets/MD/07_bibliographie.md:472`) donne un PODCAST sur parlonsbitcoin.com,
tandis que « La voie du Bitcoin » est l'editeur de l'entree `:474` (Tulipes,
2017) — laquelle a sa propre fiche, `b84f59ac`, qui porte cet editeur jusque
dans son attribut `title`. Le support de deux entrees distinctes a donc ete
recopie sur la mauvaise.

CE QUI N'EST PAS EN CAUSE. L'identite de l'oeuvre : `:472` est la SEULE entree
Favier 2021 de la bibliographie, son titre et l'URL de son enregistrement
(« bitcoin-et-religion ») concordent avec le libelle de la fiche, et le
chapitre I la cite deux fois sous « (Favier 2021) ». Ce n'est pas la fiche qui
designe la mauvaise oeuvre : c'est son libelle qui lui attribue le mauvais
support.

CE QUE CE SCRIPT REFUSE DE FAIRE. Conclure d'une ressemblance de nom. La
preuve exigee est double et FIGEE ici : le fragment attendu de chaque entree
bibliographique est re-verifie mot pour mot a chaque execution (si la
bibliographie bouge, le script echoue), et l'etat de chaque champ vise est
relu dans le graphe plutot que suppose.

Usage:
    python3 scripts/build_favier_2021_label_correction.py           # simule
    python3 scripts/build_favier_2021_label_correction.py --csv     # ecrit
    python3 scripts/build_favier_2021_label_correction.py --check   # CI
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
# Preuve FIGEE sur v114, comme le releve d'adossement l'est sur v113 : le nom
# est en dur et le script refuse tout autre graphe, plutot que d'y ecrire des
# mesures d'une version qu'il ne decrit pas.
VERSION_FIGEE = 114
SORTIE = os.path.join(REPO, 'docs', 'audits', 'data',
                      f'favier-2021-label-correction-v{VERSION_FIGEE}.csv')

FICHE = '7f0f9cc4c27040a78115b0294fd9bfe1'
FICHE_TULIPES = 'b84f59ace9b6403c88067c46af4c7582'
NOM_ACTUEL = 'Favier 2021 — Bitcoin et la religion (La voie du Bitcoin)'
# Forme PROPOSEE, pas decidee : elle corrige le seul support et ne touche ni
# l'auteur, ni l'annee, ni le titre court. Deux variantes sont posees a
# l'arbitrage dans l'audit ; aucune n'est retenue ici.
NOM_PROPOSE = 'Favier 2021 — Bitcoin et la religion (podcast Parlons Bitcoin)'

# Les champs nommants que le depot connait. On les INSPECTE tous : conclure
# « il n'y a que `name` » sans avoir regarde les autres serait une conclusion
# sur un echantillon non nomme.
CHAMPS_NOMMANTS = ('nameEn', 'labelFr', 'labelEn', 'aliases', 'title')

# Les deux entrees bibliographiques, avec le fragment attendu mot pour mot.
PREUVES = {
    472: 'FAVIER Jacques, 2021, « Le Bitcoin, la religion du XXIe '
         'siècle née des mathématiques',
    474: 'FAVIER Jacques, 2017, « Tulipes », '
         'http://blog.lavoiedubitcoin.info/post/Tulipes',
}

COLONNES = (
    'entity_id', 'entity_label', 'champ_vise', 'valeur_actuelle',
    'valeur_proposee', 'preuve_ligne', 'preuve_verbatim', 'verdict',
    'confidence', 'risque_identifie', 'decision_needed', 'note_de_lecture',
)


def echec(msg, code=CODE_DONNEES):
    famille = 'invocation' if code == CODE_INVOCATION else 'donnees'
    print(f'ECHEC ({famille}) : {msg}', file=sys.stderr)
    sys.exit(code)


def attribut(entite, cle):
    v = (entite.get('attributes') or {}).get(cle)
    if isinstance(v, dict):
        v = v.get('value')
    return v


def construire(courant):
    with open(courant, encoding='utf-8') as f:
        g = json.load(f)
    par_id = {e['id']: e for e in g['entities']}
    with open(BIBLIO, encoding='utf-8') as f:
        biblio = f.read().splitlines()

    for no, fragment in PREUVES.items():
        if no > len(biblio) or fragment not in biblio[no - 1]:
            echec(f'{BIBLIO}:{no} ne contient plus « {fragment[:46]}… » — la '
                  'bibliographie a bouge. Reinstruire plutot que publier une '
                  'preuve qui ne prouve plus rien.')
    # Le sens du chantier tient a ce que les deux entrees ne soient PAS
    # inversees : « lavoiedubitcoin » doit etre a `:474`, et absent de `:472`.
    if 'lavoiedubitcoin' not in biblio[473]:
        echec("l entree :474 ne porte plus l editeur « lavoiedubitcoin » — "
              'toute la demonstration repose sur ce rattachement')
    if 'lavoiedubitcoin' in biblio[471] or 'voie du Bitcoin' in biblio[471]:
        echec("l entree :472 porte « La voie du Bitcoin » : les deux entrees "
              'seraient inversees par rapport a ce que ce chantier suppose. '
              'Ne rien conclure, tout reinstruire.')
    if 'parlonsbitcoin' not in biblio[471]:
        echec("l entree :472 ne porte plus « parlonsbitcoin » — la correction "
              'proposee perd son fondement')

    fiche, tulipes = par_id.get(FICHE), par_id.get(FICHE_TULIPES)
    if fiche is None or tulipes is None:
        echec('fiche 7f0f9cc4 ou b84f59ac absente du graphe', CODE_INVOCATION)
    if fiche.get('name') != NOM_ACTUEL:
        echec(f'7f0f9cc4 porte {fiche.get("name")!r}, le chantier a ete '
              f'instruit sur {NOM_ACTUEL!r} — reinstruire')

    lignes = [{
        'entity_id': FICHE,
        'entity_label': fiche.get('name'),
        'champ_vise': 'name',
        'valeur_actuelle': fiche.get('name'),
        'valeur_proposee': NOM_PROPOSE,
        'preuve_ligne': 'assets/MD/07_bibliographie.md:472',
        'preuve_verbatim': PREUVES[472],
        'verdict': 'a corriger',
        'confidence': 'forte',
        'risque_identifie':
            "aucun sur l identite de l oeuvre ; le risque porte sur la FORME "
            "exacte du libelle, qui reste a arbitrer",
        'decision_needed':
            'corriger le nom ? et sous quelle forme ? (arbitrages 1 et 2)',
        'note_de_lecture':
            ":472 est l UNIQUE entree Favier 2021 de la bibliographie ; le "
            "titre et l URL (« bitcoin-et-religion ») concordent avec le "
            "libelle ; le chapitre I cite deux fois « (Favier 2021) ». Seul "
            "le SUPPORT est faux : « La voie du Bitcoin » appartient a :474.",
    }]

    for cle in CHAMPS_NOMMANTS:
        valeur = attribut(fiche, cle)
        lignes.append({
            'entity_id': FICHE,
            'entity_label': fiche.get('name'),
            'champ_vise': cle,
            'valeur_actuelle': '' if valeur is None else str(valeur),
            'valeur_proposee': '',
            'preuve_ligne': '', 'preuve_verbatim': '',
            'verdict': 'sans objet — champ absent' if valeur is None
                       else 'A INSTRUIRE — champ present',
            'confidence': 'sans objet' if valeur is None else 'indeterminee',
            'risque_identifie': '' if valeur is None
                                else 'un champ nommant non corrige laisserait '
                                     'le libelle faux accessible ailleurs',
            'decision_needed': 'aucune' if valeur is None else 'a arbitrer',
            'note_de_lecture':
                "la fiche ne porte AUCUN attribut : ni title, ni year, ni "
                "label, ni alias. Son seul appui nommant est `name` — c est "
                "aussi pourquoi la correction ne peut porter que sur lui.",
        })

    lignes.append({
        'entity_id': FICHE_TULIPES,
        'entity_label': tulipes.get('name'),
        'champ_vise': 'name + title (temoin)',
        'valeur_actuelle': f'name={tulipes.get("name")!r} ; '
                           f'title={attribut(tulipes, "title")!r}',
        'valeur_proposee': '',
        'preuve_ligne': 'assets/MD/07_bibliographie.md:474',
        'preuve_verbatim': PREUVES[474],
        'verdict': 'NE PAS TOUCHER — correct',
        'confidence': 'forte',
        'risque_identifie':
            "c est ici que « La voie du Bitcoin » est JUSTE ; le corriger des "
            "deux cotes detruirait l information au lieu de la reparer",
        'decision_needed': 'aucune',
        'note_de_lecture':
            "temoin de non-inversion : l editeur est porte par cette fiche "
            "jusque dans son attribut `title`, et l entree :474 donne bien "
            "blog.lavoiedubitcoin.info.",
    })

    # Effet collateral MESURE, pas suppose : les cartes portent le nom a cote
    # de l identifiant, et aucun controle du depot ne verifie leur accord.
    for carte in ('section_entities_map.json', 'entity_section_map.json'):
        chemin = os.path.join(REPO, carte)
        with open(chemin, encoding='utf-8') as f:
            brut = f.read()
        # `len(split) - 1` plutot que la methode de comptage de chaine : son
        # nom est aussi une cle d'attribut du graphe, et l'appel suffirait a
        # inscrire ce script dans son `readBy`. Meme precaution que
        # `classify_date_evidence.py`, pour la meme raison.
        n = len(brut.split(NOM_ACTUEL)) - 1
        lignes.append({
            'entity_id': FICHE,
            'entity_label': fiche.get('name'),
            'champ_vise': f'{carte} → entity_name',
            'valeur_actuelle': f'{n} ligne(s) portant le libelle actuel',
            'valeur_proposee': f'{n} ligne(s) a regenerer si le nom change',
            'preuve_ligne': carte, 'preuve_verbatim': '',
            'verdict': 'collateral — a regenerer dans le meme lot',
            'confidence': 'forte',
            'risque_identifie':
                "AUCUN controle du depot ne detecte la desynchronisation : "
                "verifie en renommant dans le graphe seul, check_anchoring, "
                "build_anchor_weights --check et check_graph_integrity "
                "restent VERTS. La carte garderait le libelle faux en "
                "silence.",
            'decision_needed':
                'inclure la regeneration des cartes au lot ? (arbitrage 3)',
            'note_de_lecture':
                "build_anchor_weights lit `noms.get(eid) or "
                "ent.get('entity_name')` : il PREFERE le graphe et se rabat "
                "sur la carte. L outillage ne serait donc pas trompe — mais "
                "un lecteur humain, si.",
        })
    return lignes


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

    courant = args.graph or os.path.join(
        REPO, f'grc20-these-mael-rolland-v{VERSION_FIGEE}.json')
    if not os.path.exists(courant):
        if args.graph:
            echec(f'graphe explicite introuvable : {courant} (passe via '
                  '--graph)', CODE_INVOCATION)
        echec(f'graphe FIGE introuvable : {courant}', CODE_INVOCATION)
    vue = numero_de_version(courant)
    if vue != VERSION_FIGEE:
        echec(f'ce releve est une preuve FIGEE sur v{VERSION_FIGEE} ; le '
              f'graphe vise est v{vue}. Pour instruire une version '
              'ulterieure, ouvrir un nouveau releve.')

    lignes = construire(courant)
    print(f'graphe de reference : {os.path.basename(courant)}')
    print(f'{len(lignes)} ligne(s)\n')
    for x in lignes:
        print(f"  {x['champ_vise'][:38]:38s} {x['verdict']}")

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
