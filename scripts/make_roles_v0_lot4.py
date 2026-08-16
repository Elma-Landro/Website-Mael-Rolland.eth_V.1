#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Lot 4 des roles — verse les CINQ roles murs valides par Mael le 16/08/2026.

Ouvert par la decision Mael du 16/08/2026, point 3 : « Je valide les cinq
propositions adossees a des precedents deja codes. A integrer seulement dans
un lot borne, avec preuve que les vocabulaires geles ne changent pas. »

Ce que fait ce script, et RIEN d'autre :
  - il ajoute 5 lignes a docs/research/catalogue-evenements/catalogue-roles-v0.csv
    (76 -> 81), les 76 lignes existantes restant octet pour octet identiques ;
  - il refuse d'ecrire si le moindre controle d'arrivee echoue.

Ce qu'il ne fait PAS : il ne touche pas au catalogue maitre, pas au graphe,
pas aux vocabulaires geles, pas aux trois lignes laissees en diagnostic
(E060, E059, E032), pas au statut d'une seule ligne.

Regle de codage appliquee — ratifiee par Mael le 16/08/2026 (point 1) :
  LE ROLE QUALIFIE LA FONCTION TENUE DANS LA SITUATION, PAS LA GRAMMAIRE DE
  L'ACTE. Une publication, une annonce, une cotation ou une decision ne donne
  pas automatiquement `initiateur`.

Chaque ligne du lot porte, dans sa note, l'ancrage textuel qui la justifie.
Les cinq sont attestees par le chapitre I de la these — et pour trois d'entre
elles, la these oppose elle-meme les deux fonctions, l.289 :
  « de maniere tres indirecte d'abord, par SIMPLE PUBLICATION de donnees de
    prix agregees (Nasdaq fin 2013, suivi par le NYSE en 2015), plus
    directement ensuite, par la CREATION de produit financier specifique par
    des acteurs reconnus (marches futurs par le Chicago Board Option Exchange
    ou le Chicago Mercantile Exchange, courant 2017). »
C'est le partage validateur / initiateur, ecrit dans le texte source.

Usage :
    python3 scripts/make_roles_v0_lot4.py --dry-run
    python3 scripts/make_roles_v0_lot4.py
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

# ---------------------------------------------------------------------------
# Source figee par empreinte : le script refuse de tourner sur autre chose.
# ---------------------------------------------------------------------------
EMPREINTE_SOURCE = '14d1db05088efb9bf3c527a97fc2ab6c2a4ced5b'
LIGNES_AVANT = 76
LIGNES_APRES = 81

# Q7 v1 est GELE et ce lot n'y touche pas : son empreinte doit etre identique
# avant et apres. La grille de roles, elle, a recu le 16/08/2026 un AJOUT de
# guide de codage (aucun role ajoute, renomme ni redefini) : on ne verifie donc
# pas son empreinte mais SON VOCABULAIRE, extrait du tableau du §2.
EMPREINTE_Q7_GELEE = '55bf8d9c5757bd096d9bbe77b78dfe402b61ba1b'

# Vocabulaire GELE de la grille de roles v0 — recopie pour CONTROLER, jamais
# pour decider. Toute divergence avec le tableau du §2 arrete le script.
ROLES_V0 = ['initiateur', 'exploiteur', 'affecte', 'revelateur', 'correcteur',
            'validateur', 'coordinateur', 'opposant', 'observateur',
            'non_applicable', 'incertain']
ACTEURS_V1 = ['core_devs', 'mineurs', 'entrepreneurs_exchanges',
              'institutions_financieres', 'regulateurs_etats',
              'medias_connaissance', 'communautes_forums', 'nd']
CONFIANCES = ['haute', 'moyenne', 'basse']

# ---------------------------------------------------------------------------
# LE LOT — fige dans le code. event_id, actor_id, actor_name, role, confiance,
# note. Aucune ligne n'est ajoutee hors de cette table.
# ---------------------------------------------------------------------------
LOT = [
    ('E073', 'institutions_financieres', 'CBOE et CME', 'initiateur', 'haute',
     "creation d'un produit financier qui n'existait pas (ch.I l.289 : « la CREATION de produit "
     "financier specifique par des acteurs reconnus ») - precedent E052 (Tether Ltd initiateur)"),
    ('E042', 'institutions_financieres', 'Nasdaq', 'validateur', 'moyenne',
     "acceptation institutionnelle sans production (ch.I l.289 : « de maniere tres indirecte "
     "d'abord, par SIMPLE PUBLICATION de donnees de prix agregees ») - precedent E044 (BitGo validateur)"),
    ('E058', 'institutions_financieres', 'NYSE', 'validateur', 'moyenne',
     "meme acte et meme phrase source que E042 (ch.I l.289 : « Nasdaq fin 2013, suivi par le "
     "NYSE en 2015 ») - lecture solidaire des deux lignes"),
    ('E027', 'institutions_financieres', 'PayPal', 'opposant', 'moyenne',
     "retrait de service = blocage agissant, pas une creation - la ligne code elle-meme "
     "liquidite_convertibilite(-) (ch.I n.75 l.609)"),
    ('E037', 'regulateurs_etats', 'Banque centrale europeenne', 'revelateur', 'moyenne',
     "ecrit qui rend visible ET dont l'effet est atteste (ch.I l.289 : « Les premieres "
     "publications et mises en garde (European Central Bank 2012) POUSSENT A L'EMERGENCE de "
     "premiers services de conformite ») - precedent E064"),
]

# Etat ATTENDU des cinq lignes visees, dans le catalogue maitre. Le script
# refuse d'ecrire si l'une d'elles a bouge depuis le diagnostic du 16/08/2026.
ATTENDU_CATALOGUE = {
    'E073': ('validee', 'institutions_financieres'),
    'E042': ('validee', 'institutions_financieres'),
    'E058': ('validee', 'institutions_financieres'),
    'E027': ('validee', 'institutions_financieres'),
    'E037': ('validee', 'regulateurs_etats'),
}

# Lignes explicitement LAISSEES DE COTE par la decision du 16/08/2026 : le
# script verifie qu'aucune d'elles ne recoit de role, meme par accident.
HORS_LOT = ['E060', 'E059', 'E032']


def empreinte_git(chemin):
    """Empreinte de blob git, sans invoquer git."""
    with open(chemin, 'rb') as fh:
        donnees = fh.read()
    entete = b'blob %d\0' % len(donnees)
    return hashlib.sha1(entete + donnees).hexdigest()


def lire_octets(chemin):
    with open(chemin, 'rb') as fh:
        return fh.read()


def roles_du_document_gele():
    """Extrait les roles du tableau du §2 de grille-roles-v0.md.

    On lit le DOCUMENT plutot que de faire confiance a la constante : c'est le
    document qui fait foi, la constante n'est qu'un controle.
    """
    texte = open(F_GRILLE, encoding='utf-8').read()
    debut = texte.find('## 2. Les rôles')
    if debut < 0:
        raise SystemExit('ARRET : §2 introuvable dans grille-roles-v0.md.')
    fin = texte.find('\n## ', debut + 1)
    bloc = texte[debut:fin if fin > 0 else len(texte)]
    return re.findall(r'^\| `([a-z_]+)` \|', bloc, flags=re.M)


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--dry-run', action='store_true',
                    help="tout controler et tout afficher, sans ecrire")
    args = ap.parse_args()

    echecs = []

    # -- C1 : la source est bien celle du diagnostic -------------------------
    emp = empreinte_git(F_ROLES)
    if emp != EMPREINTE_SOURCE:
        echecs.append('C1 source : empreinte %s, attendue %s — le fichier de roles a bouge.'
                      % (emp, EMPREINTE_SOURCE))

    octets_avant = lire_octets(F_ROLES)
    if b'\x00' in octets_avant:
        echecs.append('C1b source : octet NUL dans le CSV de roles.')
    if not octets_avant.endswith(b'\r\n'):
        echecs.append('C1c source : le CSV ne se termine pas par CRLF.')
    if octets_avant.count(b'\n') != octets_avant.count(b'\r\n'):
        echecs.append('C1d source : le CSV melange LF et CRLF.')

    # -- C2 : le vocabulaire gele n'a pas bouge -----------------------------
    roles_doc = roles_du_document_gele()
    if roles_doc != ROLES_V0:
        echecs.append('C2 vocabulaire : le §2 de la grille declare %r, la constante gelee %r.'
                      % (roles_doc, ROLES_V0))
    emp_q7 = empreinte_git(F_Q7)
    if emp_q7 != EMPREINTE_Q7_GELEE:
        echecs.append('C2b Q7 : empreinte %s, attendue %s — le vocabulaire Q7 v1 a bouge.'
                      % (emp_q7, EMPREINTE_Q7_GELEE))

    # -- C3 : le lot est bien forme -----------------------------------------
    if len(LOT) != 5:
        echecs.append('C3 lot : %d lignes, 5 attendues.' % len(LOT))
    vus = set()
    for (eid, aid, nom, role, conf, note) in LOT:
        if (eid, aid, role) in vus:
            echecs.append('C3b lot : doublon (%s, %s, %s).' % (eid, aid, role))
        vus.add((eid, aid, role))
        if role not in ROLES_V0:
            echecs.append('C3c lot : role %r hors grille v0 sur %s.' % (role, eid))
        if aid not in ACTEURS_V1:
            echecs.append('C3d lot : acteur %r hors typologie v1 sur %s.' % (aid, eid))
        if conf not in CONFIANCES:
            echecs.append('C3e lot : confiance %r invalide sur %s.' % (conf, eid))
        if conf != 'haute' and not note.strip():
            echecs.append('C3f lot : %s en confiance %s sans note — la grille l\'exige.' % (eid, conf))
        for champ, valeur in (('nom', nom), ('note', note)):
            if ';' in valeur or '\r' in valeur or '\n' in valeur or '"' in valeur:
                echecs.append('C3g lot : %s de %s contient un caractere qui casse le CSV.' % (champ, eid))
        if eid in HORS_LOT:
            echecs.append('C3h lot : %s est explicitement HORS LOT (decision du 16/08/2026).' % eid)

    # -- C4 : les cibles existent, sont validees, et n'ont pas deja un role --
    with open(F_CATALOGUE, newline='', encoding='utf-8') as fh:
        catalogue = {e['id']: e for e in csv.DictReader(fh, delimiter=';')}
    with open(F_ROLES, newline='', encoding='utf-8') as fh:
        roles_avant = list(csv.DictReader(fh, delimiter=';'))
    deja = {r['event_id'] for r in roles_avant}

    if len(roles_avant) != LIGNES_AVANT:
        echecs.append('C4 source : %d lignes de role, %d attendues.' % (len(roles_avant), LIGNES_AVANT))
    for (eid, aid, nom, role, conf, note) in LOT:
        e = catalogue.get(eid)
        if e is None:
            echecs.append('C4b cible : %s absente du catalogue maitre.' % eid)
            continue
        attendu = ATTENDU_CATALOGUE.get(eid)
        reel = (e['statut_ligne'].strip(), e['acteur_principal'].strip())
        if attendu != reel:
            echecs.append('C4c cible : %s porte %r, le diagnostic avait mesure %r.' % (eid, reel, attendu))
        if aid != e['acteur_principal'].strip():
            echecs.append('C4d cible : %s — acteur du lot %r != acteur principal du catalogue %r.'
                          % (eid, aid, e['acteur_principal'].strip()))
        if eid in deja:
            echecs.append('C4e cible : %s porte deja un role — ce lot n\'ecrase rien.' % eid)
    for eid in HORS_LOT:
        if eid in deja:
            echecs.append('C4f hors lot : %s porte un role alors qu\'elle doit rester en diagnostic.' % eid)

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
    ajout = tampon.getvalue().encode('utf-8')
    octets_apres = octets_avant + ajout

    # -- C5 : controles de sortie, avant toute ecriture ---------------------
    sortie = []
    if not octets_apres.startswith(octets_avant):
        sortie.append('C5 : les 76 lignes existantes ne sont pas conservees a l\'identique.')
    relu = list(csv.DictReader(io.StringIO(octets_apres.decode('utf-8')), delimiter=';'))
    if len(relu) != LIGNES_APRES:
        sortie.append('C5b : %d lignes en sortie, %d attendues.' % (len(relu), LIGNES_APRES))
    if [dict(r) for r in relu[:LIGNES_AVANT]] != [dict(r) for r in roles_avant]:
        sortie.append('C5c : les 76 lignes anterieures ne se relisent pas a l\'identique.')
    for r in relu:
        if r['role'] not in ROLES_V0:
            sortie.append('C5d : role %r hors grille dans la sortie.' % r['role'])
        if r['confidence'] not in CONFIANCES:
            sortie.append('C5e : confiance %r invalide dans la sortie.' % r['confidence'])
    if octets_apres.count(b'\n') != octets_apres.count(b'\r\n') or not octets_apres.endswith(b'\r\n'):
        sortie.append('C5f : CRLF non conserve en sortie.')
    if b'\x00' in octets_apres:
        sortie.append('C5g : octet NUL en sortie.')

    if sortie:
        print('ARRET — %d controle(s) de sortie en echec :\n' % len(sortie))
        for x in sortie:
            print('  * ' + x)
        return 1

    print('Lot 4 des roles — 5 lignes, %d -> %d' % (LIGNES_AVANT, LIGNES_APRES))
    for (eid, aid, nom, role, conf, note) in LOT:
        print('  + %-5s %-24s %-12s %-8s %s' % (eid, aid, role, conf, nom))
    print('\nTous les controles d\'arrivee et de sortie sont passes.')
    print('Vocabulaires geles : §2 de la grille conforme (11 roles), Q7 v1 empreinte %s inchangee.'
          % EMPREINTE_Q7_GELEE)
    print('Laissees en diagnostic, sans role : %s' % ', '.join(HORS_LOT))

    if args.dry_run:
        print('\n--dry-run : rien n\'a ete ecrit.')
        return 0

    with open(F_ROLES, 'wb') as fh:
        fh.write(octets_apres)
    print('\nEcrit : %s (%d octets)' % (os.path.relpath(F_ROLES, REPO), len(octets_apres)))
    return 0


if __name__ == '__main__':
    sys.exit(main())
