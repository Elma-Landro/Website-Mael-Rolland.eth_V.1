#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Lot 5 des roles — verse LA SEULE ligne E060 arbitree par Mael le 16/08/2026.

Mini-lot de finition, ouvert avant le chantier « dossiers de crise ».

Ce que fait ce script, et RIEN d'autre :
  - il ajoute UNE ligne a docs/research/catalogue-evenements/catalogue-roles-v0.csv
    (81 -> 82), les 81 lignes existantes restant octet pour octet identiques.

Ce qu'il ne fait PAS, explicitement :
  - il ne touche pas au `statut_ligne` de E060, qui reste `validee` ;
  - il ne touche a AUCUNE cellule du catalogue maitre ;
  - il ne pose aucun role sur E059 ni sur E032 (diagnostics en cours) ;
  - il ne pose aucun role sur E039, E066, E068, E069 (file de diagnostic,
    explicitement hors perimetre de ce lot) ;
  - il ne touche ni au graphe, ni au site, ni aux vocabulaires geles.

Justification de la ligne, arbitrage Mael du 16/08/2026, point 1 :
opposition strategique « blockchain not bitcoin », portee par la finance
traditionnelle, avec effet de pivot mesure. Les trois conditions de la regle
d'arbitrage sont reunies dans le texte source :
  - contestation ACTIVE — ch.I l.289 : des acteurs financiers « font leur
    publicite » de l'idee que « l'important ne serait pas les UCN » ;
  - acteur A LA SOURCE — ch.I n.86 l.631 : l'idee « emane d'acteurs de la
    finance traditionnelle », slogan « Forget Bitcoin, embrace blockchain » ;
  - EFFET DIRECT sur le cours des choses — ch.I l.289 : « Nombreuses sont les
    entreprises de l'ecosysteme a pivoter vers de nouveaux protocoles ».
Regle appliquee : grille-roles-v0.md §7 — le role qualifie la FONCTION tenue
dans la situation, pas la grammaire de l'acte.

Usage :
    python3 scripts/make_roles_v0_lot5.py --dry-run
    python3 scripts/make_roles_v0_lot5.py
"""

import argparse
import csv
import hashlib
import io
import os
import re
import sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DOSSIER = os.path.join(REPO, 'docs', 'research', 'catalogue-evenements')
F_ROLES = os.path.join(DOSSIER, 'catalogue-roles-v0.csv')
F_CATALOGUE = os.path.join(DOSSIER, 'catalogue-evenements-v3-3.csv')
F_GRILLE = os.path.join(DOSSIER, 'grille-roles-v0.md')
F_Q7 = os.path.join(DOSSIER, 'vocabulaire-q7-v1-proposition.md')

EMPREINTE_SOURCE = 'b6e7deeaccc5280ec30eca2f73bc23e9b357c236'   # sortie du lot 4
EMPREINTE_Q7_GELEE = '55bf8d9c5757bd096d9bbe77b78dfe402b61ba1b'
EMPREINTE_CATALOGUE = '7a87a37d9e05d7cbe096ece8d436506812ef68a4'
LIGNES_AVANT = 81
LIGNES_APRES = 82

# Vocabulaire GELE du §2 — recopie pour CONTROLER, jamais pour decider.
ROLES_V0 = ['initiateur', 'exploiteur', 'affecte', 'revelateur', 'correcteur',
            'validateur', 'coordinateur', 'opposant', 'observateur',
            'non_applicable', 'incertain']
ACTEURS_V1 = ['core_devs', 'mineurs', 'entrepreneurs_exchanges',
              'institutions_financieres', 'regulateurs_etats',
              'medias_connaissance', 'communautes_forums', 'nd']
CONFIANCES = ['haute', 'moyenne', 'basse']

# ---------------------------------------------------------------------------
# LE LOT — une ligne, figee. event_id, actor_id, actor_name, role, conf, note.
# actor_name reste VIDE : la source designe une categorie (« des acteurs de la
# finance traditionnelle »), pas un agent nomme. Blythe Masters / JP Morgan n'y
# figure qu'a titre d'exemple (« en l'espece ») : la nommer seule retrecirait
# l'acteur au-dela de ce que dit le texte.
# ---------------------------------------------------------------------------
LOT = [
    ('E060', 'institutions_financieres', '', 'opposant', 'moyenne',
     "opposition strategique « blockchain not bitcoin » — l'idee emane "
     "d'acteurs de la finance traditionnelle (ch.I n.86 l.631, slogan "
     "« Forget Bitcoin, embrace blockchain »), ils en « font leur publicite » "
     "et l'effet est mesure : « nombreuses sont les entreprises de "
     "l'ecosysteme a pivoter » (ch.I l.289). Arbitrage du 16/08/2026"),
]

# Etat ATTENDU de E060 au catalogue maitre. Le script refuse d'ecrire si la
# ligne a bouge — et en particulier si son statut n'est plus `validee`.
ATTENDU_E060 = {
    'statut_ligne': 'validee',
    'acteur_principal': 'institutions_financieres',
    'type_acte': 'qualification_publique',
    'arene': 'presse_medias',
}

# Lignes que ce lot ne doit toucher sous aucun pretexte.
HORS_LOT = ['E059', 'E032', 'E039', 'E066', 'E068', 'E069']


def empreinte_git(chemin):
    with open(chemin, 'rb') as fh:
        donnees = fh.read()
    return hashlib.sha1(b'blob %d\0' % len(donnees) + donnees).hexdigest()


def roles_du_document_gele():
    """Lit les roles du §2 de la grille — le document fait foi, pas la constante."""
    texte = open(F_GRILLE, encoding='utf-8').read()
    debut = texte.find('## 2. Les rôles')
    if debut < 0:
        raise SystemExit('ARRET : §2 introuvable dans grille-roles-v0.md.')
    fin = texte.find('\n## ', debut + 1)
    return re.findall(r'^\| `([a-z_]+)` \|', texte[debut:fin if fin > 0 else len(texte)], flags=re.M)


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--dry-run', action='store_true', help='tout controler, sans ecrire')
    args = ap.parse_args()
    echecs = []

    # -- C1 : source et catalogue sont bien ceux du lot 4 -------------------
    emp = empreinte_git(F_ROLES)
    if emp != EMPREINTE_SOURCE:
        echecs.append('C1 : empreinte du CSV de roles %s, attendue %s.' % (emp, EMPREINTE_SOURCE))
    emp_cat = empreinte_git(F_CATALOGUE)
    if emp_cat != EMPREINTE_CATALOGUE:
        echecs.append('C1b : le catalogue maitre a bouge (%s).' % emp_cat)
    with open(F_ROLES, 'rb') as fh:
        octets_avant = fh.read()
    if b'\x00' in octets_avant:
        echecs.append('C1c : octet NUL dans le CSV de roles.')
    if not octets_avant.endswith(b'\r\n') or octets_avant.count(b'\n') != octets_avant.count(b'\r\n'):
        echecs.append('C1d : CRLF non conforme dans le CSV source.')

    # -- C2 : les vocabulaires geles n'ont pas bouge ------------------------
    roles_doc = roles_du_document_gele()
    if roles_doc != ROLES_V0:
        echecs.append('C2 : le §2 de la grille declare %r, la constante gelee %r.' % (roles_doc, ROLES_V0))
    emp_q7 = empreinte_git(F_Q7)
    if emp_q7 != EMPREINTE_Q7_GELEE:
        echecs.append('C2b : Q7 v1 a bouge (%s).' % emp_q7)

    # -- C3 : le lot est bien forme ----------------------------------------
    if len(LOT) != 1:
        echecs.append('C3 : %d ligne(s), 1 attendue.' % len(LOT))
    for (eid, aid, nom, role, conf, note) in LOT:
        if role not in ROLES_V0:
            echecs.append('C3b : role %r hors grille v0.' % role)
        if aid not in ACTEURS_V1:
            echecs.append('C3c : acteur %r hors typologie v1.' % aid)
        if conf not in CONFIANCES:
            echecs.append('C3d : confiance %r invalide.' % conf)
        if conf != 'haute' and not note.strip():
            echecs.append('C3e : %s sans note en confiance %s.' % (eid, conf))
        for champ, valeur in (('nom', nom), ('note', note)):
            if ';' in valeur or '"' in valeur or '\r' in valeur or '\n' in valeur:
                echecs.append('C3f : %s de %s casse le CSV.' % (champ, eid))
        if eid in HORS_LOT:
            echecs.append('C3g : %s est hors lot.' % eid)

    # -- C4 : la cible existe, son statut n'a pas bouge, elle n'a pas de role
    with open(F_CATALOGUE, newline='', encoding='utf-8') as fh:
        catalogue = {e['id']: e for e in csv.DictReader(fh, delimiter=';')}
    with open(F_ROLES, newline='', encoding='utf-8') as fh:
        roles_avant = list(csv.DictReader(fh, delimiter=';'))
    deja = {r['event_id'] for r in roles_avant}

    if len(roles_avant) != LIGNES_AVANT:
        echecs.append('C4 : %d lignes de role, %d attendues.' % (len(roles_avant), LIGNES_AVANT))
    e060 = catalogue.get('E060')
    if e060 is None:
        echecs.append('C4b : E060 absente du catalogue.')
    else:
        for champ, attendu in ATTENDU_E060.items():
            if e060[champ].strip() != attendu:
                echecs.append('C4c : E060.%s = %r, attendu %r — la ligne a bouge.'
                              % (champ, e060[champ].strip(), attendu))
    if 'E060' in deja:
        echecs.append('C4d : E060 porte deja un role — ce lot n\'ecrase rien.')
    for eid in HORS_LOT:
        if eid in deja:
            echecs.append('C4e : %s porte un role alors qu\'elle doit rester sans.' % eid)

    if echecs:
        print('ARRET — %d controle(s) d\'arrivee en echec :\n' % len(echecs))
        for x in echecs:
            print('  * ' + x)
        return 1

    # -- Production ---------------------------------------------------------
    tampon = io.StringIO()
    w = csv.writer(tampon, delimiter=';', lineterminator='\r\n', quoting=csv.QUOTE_MINIMAL)
    for ligne in LOT:
        w.writerow(list(ligne))
    octets_apres = octets_avant + tampon.getvalue().encode('utf-8')

    # -- C5 : controles de sortie ------------------------------------------
    sortie = []
    if not octets_apres.startswith(octets_avant):
        sortie.append('C5 : les 81 lignes existantes ne sont pas conservees a l\'identique.')
    relu = list(csv.DictReader(io.StringIO(octets_apres.decode('utf-8')), delimiter=';'))
    if len(relu) != LIGNES_APRES:
        sortie.append('C5b : %d lignes en sortie, %d attendues.' % (len(relu), LIGNES_APRES))
    if [dict(r) for r in relu[:LIGNES_AVANT]] != [dict(r) for r in roles_avant]:
        sortie.append('C5c : les 81 lignes anterieures ne se relisent pas a l\'identique.')
    for r in relu:
        if r['role'] not in ROLES_V0:
            sortie.append('C5d : role %r hors grille dans la sortie.' % r['role'])
        if r['confidence'] not in CONFIANCES:
            sortie.append('C5e : confiance %r invalide dans la sortie.' % r['confidence'])
    if octets_apres.count(b'\n') != octets_apres.count(b'\r\n') or not octets_apres.endswith(b'\r\n'):
        sortie.append('C5f : CRLF non conserve.')
    if b'\x00' in octets_apres:
        sortie.append('C5g : octet NUL en sortie.')
    for eid in HORS_LOT:
        if any(r['event_id'] == eid for r in relu):
            sortie.append('C5h : %s a recu un role — interdit par ce lot.' % eid)

    if sortie:
        print('ARRET — %d controle(s) de sortie en echec :\n' % len(sortie))
        for x in sortie:
            print('  * ' + x)
        return 1

    print('Lot 5 des roles — 1 ligne, %d -> %d' % (LIGNES_AVANT, LIGNES_APRES))
    for (eid, aid, nom, role, conf, note) in LOT:
        print('  + %-5s %-24s %-10s %s' % (eid, aid, role, conf))
    print('\nControles passes. E060 conserve son statut : %s.' % ATTENDU_E060['statut_ligne'])
    print('Vocabulaires geles : §2 conforme (11 roles), Q7 v1 %s, catalogue maitre %s — inchanges.'
          % (EMPREINTE_Q7_GELEE[:8], EMPREINTE_CATALOGUE[:8]))
    print('Restent sans role, verifie : %s' % ', '.join(HORS_LOT))

    if args.dry_run:
        print('\n--dry-run : rien n\'a ete ecrit.')
        return 0

    with open(F_ROLES, 'wb') as fh:
        fh.write(octets_apres)
    print('\nEcrit : %s (%d octets)' % (os.path.relpath(F_ROLES, REPO), len(octets_apres)))
    return 0


if __name__ == '__main__':
    sys.exit(main())
