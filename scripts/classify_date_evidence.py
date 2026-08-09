#!/usr/bin/env python3
"""Classe le REGIME DE PREUVE de chaque date evenementielle du chantier
chronologie, selon l'arbitrage de Maël Rolland du 2026-08-09 (reponse 10).

L'arbitrage demande d'exiger un `dateSource` avant publication, MAIS de
distinguer quatre regimes plutot que de traiter les 86 dates non adossees
comme un bloc homogene :

    these_verbatim   la date est confirmee MOT POUR MOT par le texte de la these
    source_primaire  la date est confirmee par une source primaire externe
    approximatif     la date elle-meme est grossiere (annee nue, plage, texte libre)
    infere           aucun des trois ci-dessus

CE QUE CE SCRIPT NE FAIT PAS. Il ne juge aucune date vraie ou fausse : il
classe la NATURE de l'appui, pas sa validite. Une date `these_verbatim` peut
etre fausse — le chantier en a trouve (Frontier, Bitcoin-QT, split de chaine
sont des contradictions internes a la these). Et `infere` n'est pas un
reproche : c'est l'aveu qu'on ne sait pas d'ou vient la date.

PRECEDENCE, declaree parce qu'elle est un choix et non une evidence :
    source_primaire > these_verbatim > approximatif > infere
Une source primaire externe l'emporte sur la these parce qu'elle est
verifiable par un tiers. Mais l'arbitrage exige que le statut « confirme par
la these » reste VISIBLE meme quand il n'est pas retenu comme regime
principal : la colonne `confirme_par_these` le porte donc separement, et ne
disparait jamais derriere la precedence.

LECTURE SEULE. N'ecrit que dans le CSV d'adossement, et seulement avec
--write. Ne touche ni graphe, ni carte, ni patch.
"""

import argparse
import csv
import os
import sys
from collections import Counter

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(REPO, 'docs', 'audits', 'data')

ADOSSEMENT = os.path.join(DATA, 'chronology-reference-support-v111.csv')
RECOUPEMENT = os.path.join(DATA, 'chronology-thesis-crosscheck-v111.csv')
EXTERNE = os.path.join(DATA, 'chronology-external-verification-v111.csv')
INVENTAIRE = os.path.join(DATA, 'chronology-date-inventory-v111.csv')

# Statuts du recoupement these valant confirmation verbatim. `accord` est une
# egalite ; `accord_granularite_differente` couvre « debut octobre 2011 » face
# a 2011-10-07 — compatible, donc confirmant. Les autres statuts ne confirment
# rien : `figure_non_verifiable_dans_le_MD` n'est NI confirmation NI refutation.
STATUTS_CONFIRMANTS = frozenset({'accord', 'accord_granularite_differente'})

# Granularites qui rendent la date approximative par elle-meme.
GRANULARITES_GROSSIERES = frozenset({'annee', 'plage', 'indeterminee'})

COLONNES_AJOUTEES = ('regime_de_preuve', 'confirme_par_these', 'motif_regime')


def lire(chemin):
    """Lit un CSV dont le separateur n'est pas uniforme d'un fichier a l'autre.

    Les cinq CSV du chantier ont ete produits par des agents differents : deux
    en virgule, trois en point-virgule. Deviner plutot que declarer serait
    fragile, mais imposer un separateur casserait les fichiers deja verses."""
    with open(chemin, encoding='utf-8') as f:
        tete = f.readline()
    # len(split) plutot que la methode de comptage de str : le balayage
    # lexical de build_properties_registry.py prendrait cet appel de methode
    # pour un acces a l'attribut de graphe homonyme et inscrirait ce script
    # dans son readBy. Supprimer la cause vaut mieux que declarer un faux
    # positif de plus — et cette remarque elle-meme evite d'ecrire le nom.
    sep = ';' if len(tete.split(';')) > len(tete.split(',')) else ','
    with open(chemin, encoding='utf-8', newline='') as f:
        return list(csv.DictReader(f, delimiter=sep)), sep


def classer(ligne, par_these, par_externe, granularites):
    """Retourne (regime, confirme_par_these, motif). Aucun effet de bord."""
    eid = ligne.get('entity_id', '')
    cle = ligne.get('cle_date', '')

    confirme_these = par_these.get(eid) in STATUTS_CONFIRMANTS
    primaire = par_externe.get(eid)
    grossiere = granularites.get((eid, cle)) in GRANULARITES_GROSSIERES

    if primaire:
        return ('source_primaire',
                'oui' if confirme_these else 'non',
                f'confirme par source primaire externe ({primaire})')
    if confirme_these:
        return ('these_verbatim', 'oui',
                'confirme mot pour mot par le texte de la these — source '
                'PROVISOIRE : la these est ici juge et partie, et le chantier '
                'a montre qu elle se contredit parfois elle-meme')
    if grossiere:
        return ('approximatif', 'non',
                f'granularite « {granularites.get((eid, cle))} » : la date '
                'elle-meme ne designe pas un jour')
    return ('infere', 'non',
            'aucune confirmation par la these, aucune source primaire, '
            'granularite fine — origine de la date non etablie')


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--write', action='store_true',
                    help="ecrit les colonnes dans le CSV d'adossement "
                         '(par defaut : simule et affiche seulement)')
    ap.add_argument('--check', action='store_true',
                    help='sort 1 si le CSV verse ne porte pas la classification '
                         'a jour ; pour la CI')
    args = ap.parse_args()

    if args.write and args.check:
        ap.error('--write et --check sont exclusifs : --check ne doit jamais '
                 'reparer ce qu il controle.')

    for chemin in (ADOSSEMENT, RECOUPEMENT, EXTERNE, INVENTAIRE):
        if not os.path.exists(chemin):
            print(f'ERREUR : {os.path.relpath(chemin, REPO)} est absent.',
                  file=sys.stderr)
            return 2

    adossement, sep = lire(ADOSSEMENT)
    recoupement, _ = lire(RECOUPEMENT)
    externe, _ = lire(EXTERNE)
    inventaire, _ = lire(INVENTAIRE)

    par_these = {r['entity_id']: r['statut'] for r in recoupement}
    # Seul `confirme` compte, et seulement adosse a une source PRIMAIRE :
    # `indice_unique` est une contrainte de reseau, pas une confirmation, et
    # une source tertiaire ne confirme pas une date (cf. audit § 10).
    par_externe = {
        r['entity_id']: r.get('qualite_source', '')
        for r in externe
        if r.get('statut') == 'confirme' and r.get('qualite_source') == 'primaire'
    }
    granularites = {(r['entity_id'], r['attribute_key']): r['granularity']
                    for r in inventaire}

    volet1 = [l for l in adossement if l.get('volet', '').startswith('1_')]

    regimes, confirmes = Counter(), 0
    sorties = []
    for ligne in adossement:
        if ligne.get('volet', '').startswith('1_'):
            regime, ct, motif = classer(ligne, par_these, par_externe,
                                        granularites)
            regimes[regime] += 1
            if ct == 'oui':
                confirmes += 1
        else:
            # Volet 2 : annees bibliographiques, hors du regime de preuve des
            # dates evenementielles. Laisser vide plutot que d'inventer une
            # classe qui ne veut rien dire pour une reference.
            regime, ct, motif = '', '', 'hors perimetre (volet 2)'
        nouvelle = dict(ligne)
        nouvelle['regime_de_preuve'] = regime
        nouvelle['confirme_par_these'] = ct
        nouvelle['motif_regime'] = motif
        sorties.append(nouvelle)

    print(f'volet 1 : {len(volet1)} dates evenementielles')
    for regime in ('source_primaire', 'these_verbatim', 'approximatif', 'infere'):
        print(f'  {regimes[regime]:4d}  {regime}')
    print(f'  dont confirmees par la these (tous regimes) : {confirmes}')

    # Croisement avec l'adossement declare : c'est le chiffre qui justifie
    # l'arbitrage — combien de dates SANS source declaree sont malgre tout
    # confirmees par la these.
    non_adosse = [l for l in volet1 if l.get('statut') == 'non_adosse']
    croise = sum(1 for l in non_adosse
                 if par_these.get(l.get('entity_id', '')) in STATUTS_CONFIRMANTS)
    print(f'  parmi les {len(non_adosse)} `non_adosse` : {croise} confirmees '
          'par la these — non declarees, mais pas sans fondement')

    entetes = list(adossement[0].keys()) + [c for c in COLONNES_AJOUTEES
                                            if c not in adossement[0]]

    if args.check:
        if all(c in adossement[0] for c in COLONNES_AJOUTEES):
            ecarts = [l for l, n in zip(adossement, sorties)
                      if any(l.get(c) != n[c] for c in COLONNES_AJOUTEES)]
            if not ecarts:
                print('--check : la classification du CSV verse est a jour.')
                return 0
            print(f'--check : {len(ecarts)} ligne(s) divergent de la '
                  'classification recalculee.', file=sys.stderr)
            return 1
        print('--check : le CSV verse ne porte pas encore les colonnes '
              f'{", ".join(COLONNES_AJOUTEES)}.', file=sys.stderr)
        return 1

    if not args.write:
        print('\n(simulation — relancer avec --write pour ecrire les colonnes)')
        return 0

    temporaire = ADOSSEMENT + '.tmp'
    with open(temporaire, 'w', encoding='utf-8', newline='') as f:
        w = csv.DictWriter(f, fieldnames=entetes, delimiter=sep)
        w.writeheader()
        w.writerows(sorties)
    os.replace(temporaire, ADOSSEMENT)
    print(f'\necrit : {os.path.relpath(ADOSSEMENT, REPO)} '
          f'({len(sorties)} lignes, {len(entetes)} colonnes)')
    return 0


if __name__ == '__main__':
    sys.exit(main())
