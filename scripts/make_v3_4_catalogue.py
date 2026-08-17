#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Catalogue v3-3 -> v3-4 — les trois arbitrages Mael du 16/08/2026.

NEUF CELLULES, sur TROIS lignes, et rien d'autre. Le fichier v3-3 est
CONSERVE tel quel : ce script ne l'ecrase jamais, il produit un fichier
nouveau, comme make_v3_3_catalogue.py l'avait fait pour v3-2.

Les trois arbitrages :

  1. E059 <-> G110 sont le meme fait (levee de fonds Coinbase, 2015).
     E059 est CANONIQUE. G110 est classee doublon non canonique selon la
     convention du catalogue — `statut_ligne = douteuse` + note explicite,
     exactement comme G011 et G013 au lot 3. AUCUNE fusion, AUCUN patch
     graphe, AUCUN role sur G110.

  2. E059 — acteur principal corrige vers Coinbase. La source dit
     « L'entreprise Coinbase REALISE la plus grande levee de fonds
     d'alors avec 75 millions de dollars » (ch.I n.90 l.639) : l'agent est
     Coinbase, les financeurs ne sont pas nommes. Les financeurs anonymes
     ne restent donc pas acteur principal. AUCUN role n'est pose.

  3. E032 — `acteur_principal_mode = nd`. C'est une mesure agregee, pas un
     acte situe : le champ `nd` dit que l'absence d'acteur principal est
     INTERPRETEE, pas oubliee (convention r1 du gel du 15/08/2026).

Ce que ce script ne fait PAS : il ne touche pas au graphe, ne produit
aucune v116, ne pose aucun role, ne recode rien d'autre, ne tranche pas
le perimetre R3, et ne fusionne aucune ligne.

Usage :
    python3 scripts/make_v3_4_catalogue.py --dry-run
    python3 scripts/make_v3_4_catalogue.py
"""

import argparse
import csv
import hashlib
import io
import os
import sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DOSSIER = os.path.join(REPO, 'docs', 'research', 'catalogue-evenements')
F_SOURCE = os.path.join(DOSSIER, 'catalogue-evenements-v3-3.csv')
F_CIBLE = os.path.join(DOSSIER, 'catalogue-evenements-v3-4.csv')
F_ROLES = os.path.join(DOSSIER, 'catalogue-roles-v0.csv')

EMPREINTE_SOURCE = '7a87a37d9e05d7cbe096ece8d436506812ef68a4'
LIGNES = 345          # hors en-tete
COLONNES = 33

# Entite d'acteur resolue au graphe v115, sur name + nameEn + labelEn +
# labelFr + aliases. Type `Organization`, nom « Coinbase ». Ecartees
# explicitement : `Coinbase Commerce` (c660948f, un SERVICE) et
# l'InfrastructureEvent de la levee (7cda4562, l'EVENEMENT, pas l'acteur).
ENT_COINBASE = '8991d9f05d234b6d876d16334f60af63'

# Vocabulaires GELES — recopies pour CONTROLER la sortie, jamais pour decider.
STATUTS_D4 = {'validee', 'chantier', 'douteuse', 'a_arbitrer', 'exclue'}
MODES_A1 = {'', 'initiateur', 'entite_affectee', 'systeme_protocole', 'a_arbitrer', 'nd'}
ACTEURS_V1 = {'', 'core_devs', 'mineurs', 'entrepreneurs_exchanges',
              'institutions_financieres', 'regulateurs_etats',
              'medias_connaissance', 'communautes_forums', 'nd'}

# ---------------------------------------------------------------------------
# LE LOT — fige. id -> colonne -> (valeur ATTENDUE avant, valeur APRES).
# Le script recalcule le diff cellule a cellule et refuse d'ecrire s'il
# diverge d'un seul element de cette table.
# ---------------------------------------------------------------------------
NOTE_G110_AJOUT = (
    " · Doublon du meme fait avec E059, qui est CANONIQUE (arbitrage du 16/08/2026) "
    "— signale, non fusionne. Aucune fusion graphe, aucun patch, aucun role sur cette ligne."
)
NOTE_E032_AJOUT = (
    " · Seuil / serie agregee : l'intitule melange un fait date (entree du capital-risque en 2012) "
    "et une serie annuelle agregee (2012-2015, ch.I n.90 l.639). acteur_principal_mode = nd dit que "
    "l'absence d'acteur principal est interpretee, pas oubliee. Scission possible, non faite (16/08/2026)."
)

LOT = {
    # --- 1. E059 : acteur principal corrige vers Coinbase -------------------
    'E059': {
        'acteur_principal':      ('institutions_financieres', 'entrepreneurs_exchanges'),
        'acteur_secondaire':     ('entrepreneurs_exchanges', 'institutions_financieres'),
        'acteur_principal_mode': ('', 'initiateur'),
        'acteur_principal_id':   ('', ENT_COINBASE),
        'acteur_principal_nom':  ('', 'Coinbase'),
    },
    # --- 2. G110 : doublon non canonique ------------------------------------
    'G110': {
        'statut_ligne': ('chantier', 'douteuse'),
        'notes': ("Coinbase s'impose comme principale plateforme d'echange. Levee de fonds record "
                  "de 75M$ (2015). Indicateur off-chain de la croissance Bitcoin (comptes utilisateurs, Annexe n°2).",
                  "Coinbase s'impose comme principale plateforme d'echange. Levee de fonds record "
                  "de 75M$ (2015). Indicateur off-chain de la croissance Bitcoin (comptes utilisateurs, Annexe n°2)."
                  + NOTE_G110_AJOUT),
    },
    # --- 3. E032 : seuil, mode nd -------------------------------------------
    'E032': {
        'acteur_principal_mode': ('', 'nd'),
        'notes': ('annee a cheval poc/peche - phase indicative',
                  'annee a cheval poc/peche - phase indicative' + NOTE_E032_AJOUT),
    },
}

ATTENDU_CELLULES = 9
ATTENDU_LIGNES = 3

# Lignes qui ne doivent recevoir AUCUN role dans ce lot ni le suivant.
SANS_ROLE = ['E059', 'E032', 'G110', 'E039', 'E066', 'E068', 'E069']

# Etat attendu, hors lot, des lignes voisines — controle de non-contagion.
# Valeurs MESUREES dans v3-3, pas supposees : une premiere redaction de ce
# garde-fou declarait E003 sans acteur principal, et le controle C5 a
# arrete le script — la ligne porte `core_devs`. Le garde-fou a fait son
# travail sur son propre auteur.
INTACTES_ATTENDUES = {
    'E060': ('validee', 'institutions_financieres'),   # lot 5, ne bouge pas
    'E003': ('validee', 'core_devs'),                   # jumelle de G013, hors sujet
}


def empreinte_git(chemin):
    with open(chemin, 'rb') as fh:
        d = fh.read()
    return hashlib.sha1(b'blob %d\0' % len(d) + d).hexdigest()


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--dry-run', action='store_true', help='tout controler, sans ecrire')
    args = ap.parse_args()
    echecs = []

    # -- C1 : la source est bien v3-3 ---------------------------------------
    emp = empreinte_git(F_SOURCE)
    if emp != EMPREINTE_SOURCE:
        echecs.append('C1 : source %s, attendue %s — v3-3 a bouge.' % (emp, EMPREINTE_SOURCE))
    with open(F_SOURCE, 'rb') as fh:
        octets_src = fh.read()
    if b'\x00' in octets_src:
        echecs.append('C1b : octet NUL dans la source.')
    if octets_src.count(b'\n') != octets_src.count(b'\r\n') or not octets_src.endswith(b'\r\n'):
        echecs.append('C1c : CRLF non conforme dans la source.')
    if os.path.exists(F_CIBLE):
        echecs.append('C1d : %s existe deja — ce script n\'ecrase jamais.' % os.path.basename(F_CIBLE))

    lignes = list(csv.reader(io.StringIO(octets_src.decode('utf-8')), delimiter=';'))
    entete = lignes[0]
    if len(lignes) - 1 != LIGNES or len(entete) != COLONNES:
        echecs.append('C1e : %d lignes x %d colonnes, %d x %d attendues.'
                      % (len(lignes) - 1, len(entete), LIGNES, COLONNES))
    idx = {c: i for i, c in enumerate(entete)}
    par_id = {l[idx['id']]: l for l in lignes[1:]}

    # -- C2 : le lot est bien forme et ses valeurs AVANT sont exactes -------
    n_cellules = sum(len(v) for v in LOT.values())
    if n_cellules != ATTENDU_CELLULES or len(LOT) != ATTENDU_LIGNES:
        echecs.append('C2 : %d cellules sur %d lignes, %d sur %d attendues.'
                      % (n_cellules, len(LOT), ATTENDU_CELLULES, ATTENDU_LIGNES))
    for eid, cellules in LOT.items():
        if eid not in par_id:
            echecs.append('C2b : %s absente de la source.' % eid)
            continue
        for col, (avant, apres) in cellules.items():
            if col not in idx:
                echecs.append('C2c : colonne %r inconnue.' % col)
                continue
            reel = par_id[eid][idx[col]]
            if reel != avant:
                echecs.append('C2d : %s.%s vaut %r, le lot attendait %r.' % (eid, col, reel, avant))
            if avant == apres:
                echecs.append('C2e : %s.%s — avant et apres identiques.' % (eid, col))
            for v in (avant, apres):
                if ';' in v or '\r' in v or '\n' in v:
                    echecs.append('C2f : %s.%s contient un caractere qui casse le CSV.' % (eid, col))

    # -- C3 : les valeurs APRES respectent les vocabulaires geles ----------
    for eid, cellules in LOT.items():
        for col, (avant, apres) in cellules.items():
            if col == 'statut_ligne' and apres not in STATUTS_D4:
                echecs.append('C3 : statut %r hors D4 sur %s.' % (apres, eid))
            if col == 'acteur_principal_mode' and apres not in MODES_A1:
                echecs.append('C3b : mode %r hors A1 sur %s.' % (apres, eid))
            if col in ('acteur_principal', 'acteur_secondaire') and apres not in ACTEURS_V1:
                echecs.append('C3c : acteur %r hors typologie v1 sur %s.' % (apres, eid))
    # une ligne ne peut pas porter le meme type en principal et en secondaire
    for eid in LOT:
        if eid not in par_id:
            continue
        pr = dict(LOT[eid]).get('acteur_principal', (None, par_id[eid][idx['acteur_principal']]))[1]
        se = dict(LOT[eid]).get('acteur_secondaire', (None, par_id[eid][idx['acteur_secondaire']]))[1]
        if pr and pr == se:
            echecs.append('C3d : %s porte %r en principal ET en secondaire.' % (eid, pr))

    # -- C4 : aucune des lignes protegees ne porte de role ------------------
    with open(F_ROLES, newline='', encoding='utf-8') as fh:
        avec_role = {r['event_id'] for r in csv.DictReader(fh, delimiter=';')}
    for eid in SANS_ROLE:
        if eid in avec_role:
            echecs.append('C4 : %s porte un role alors qu\'elle doit rester sans.' % eid)

    # -- C5 : les lignes voisines sont bien dans l'etat attendu -------------
    for eid, (statut, acteur) in INTACTES_ATTENDUES.items():
        if eid in par_id:
            reel = (par_id[eid][idx['statut_ligne']], par_id[eid][idx['acteur_principal']])
            if reel != (statut, acteur):
                echecs.append('C5 : %s porte %r, attendu %r.' % (eid, reel, (statut, acteur)))

    if echecs:
        print('ARRET — %d controle(s) d\'arrivee en echec :\n' % len(echecs))
        for x in echecs:
            print('  * ' + x)
        return 1

    # -- Production ---------------------------------------------------------
    sortie = [list(entete)] + [list(l) for l in lignes[1:]]
    for ligne in sortie[1:]:
        eid = ligne[idx['id']]
        if eid in LOT:
            for col, (avant, apres) in LOT[eid].items():
                ligne[idx[col]] = apres

    buf = io.StringIO()
    w = csv.writer(buf, delimiter=';', lineterminator='\r\n', quoting=csv.QUOTE_MINIMAL)
    for l in sortie:
        w.writerow(l)
    octets_out = buf.getvalue().encode('utf-8')

    # -- C6 : diff RECALCULE, compare au lot declare ------------------------
    ctrl = []
    apres_lignes = list(csv.reader(io.StringIO(octets_out.decode('utf-8')), delimiter=';'))
    if len(apres_lignes) != len(lignes) or apres_lignes[0] != entete:
        ctrl.append('C6 : forme de la sortie alteree.')
    diff = {}
    for a, b in zip(lignes[1:], apres_lignes[1:]):
        if a[idx['id']] != b[idx['id']]:
            ctrl.append('C6b : ordre des lignes altere.')
            break
        for i, (x, y) in enumerate(zip(a, b)):
            if x != y:
                diff.setdefault(a[idx['id']], {})[entete[i]] = (x, y)
    declare = {e: {c: v for c, v in cs.items()} for e, cs in LOT.items()}
    if diff != declare:
        ctrl.append('C6c : le diff mesure diverge du lot declare.\n     mesure  : %r\n     declare : %r'
                    % (diff, declare))
    n_diff = sum(len(v) for v in diff.values())
    if n_diff != ATTENDU_CELLULES:
        ctrl.append('C6d : %d cellules modifiees, %d attendues.' % (n_diff, ATTENDU_CELLULES))

    # -- C7 : vocabulaires geles tenus sur TOUT le fichier, pas seulement le lot
    for l in apres_lignes[1:]:
        if l[idx['statut_ligne']] not in STATUTS_D4:
            ctrl.append('C7 : statut %r hors D4 sur %s.' % (l[idx['statut_ligne']], l[idx['id']]))
        if l[idx['acteur_principal_mode']] not in MODES_A1:
            ctrl.append('C7b : mode %r hors A1 sur %s.' % (l[idx['acteur_principal_mode']], l[idx['id']]))

    # -- C8 : forme des octets ---------------------------------------------
    if octets_out.count(b'\n') != octets_out.count(b'\r\n') or not octets_out.endswith(b'\r\n'):
        ctrl.append('C8 : CRLF non conserve en sortie.')
    if b'\x00' in octets_out:
        ctrl.append('C8b : octet NUL en sortie.')

    if ctrl:
        print('ARRET — %d controle(s) de sortie en echec :\n' % len(ctrl))
        for x in ctrl:
            print('  * ' + x)
        return 1

    print('Catalogue v3-3 -> v3-4 — %d cellules sur %d lignes' % (n_diff, len(diff)))
    for eid in ('E059', 'G110', 'E032'):
        print('  %s :' % eid)
        for col, (a, b) in sorted(diff[eid].items()):
            court = lambda s: (s[:58] + '…') if len(s) > 58 else s
            print('      %-24s %r -> %r' % (col, court(a), court(b)))
    print('\nTous les controles sont passes.')
    print('v3-3 CONSERVEE, empreinte %s — ce script ne l\'ecrase jamais.' % EMPREINTE_SOURCE[:8])
    print('Sans role, verifie : %s' % ', '.join(SANS_ROLE))

    if args.dry_run:
        print('\n--dry-run : rien n\'a ete ecrit.')
        return 0

    with open(F_CIBLE, 'wb') as fh:
        fh.write(octets_out)
    print('\nEcrit : %s (%d octets)' % (os.path.relpath(F_CIBLE, REPO), len(octets_out)))
    return 0


if __name__ == '__main__':
    sys.exit(main())
