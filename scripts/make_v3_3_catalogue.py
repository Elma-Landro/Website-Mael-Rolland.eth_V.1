#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Lot 3 : integre le recodage des 40 lignes propose(lot1). v3-2 -> v3-3.

CE QUE CE SCRIPT FAIT, ET RIEN D'AUTRE. Il lit
`docs/research/catalogue-evenements/catalogue-evenements-v3-2.csv` (fige par
son empreinte git), applique le LOT FIGE de changements ci-dessous, ajoute
les TROIS colonnes de l'arbitrage A1, et ecrit `catalogue-evenements-v3-3.csv`.

Il ne touche a aucun graphe, aucun patch, aucun site, aucun vocabulaire gele.
Il ne recode AUCUNE ligne hors des 40 `propose(lot1)`.

LE LOT EST FIGE ICI, PAS SEULEMENT DECLARE. Chaque changement porte sa
valeur AVANT attendue : si la source a derive, le script refuse au lieu
d'ecraser. Le diff d'arrivee est compare cellule a cellule au lot fige :
un seul changement hors lot, et rien n'est ecrit.

PROVENANCE DES DECISIONS (verbatim archives) :
  - `docs/audits/arbitrages-lot2-A1-A5-2026-08-15.md` (A1 colonnes dediees)
  - `docs/audits/arbitrages-gel-q7v1-roles-v0-2026-08-15.md` (gel Q7 v1 + r1/r2)
  - reponses M1-M4 du 15/08/2026, inscrites dans
    `docs/audits/etat-lot3-2026-08-15.md` et son addendum
  - proposition ligne a ligne :
    `docs/research/catalogue-evenements/lot3-recodage-propose-lot1.csv`

CE QUI CHANGE, PAR FAMILLE (compte exact verifie a l'arrivee) :
  A. `statut_ligne` .......... 34 lignes (30 -> validee, 4 -> douteuse ;
                               6 restent `chantier`, non comptees)
  B. `codage_statut` ......... 30 lignes `propose(lot1)` -> `valide(lot3)`
                               (les 10 autres GARDENT `propose(lot1)` : une
                               ligne non validee ne se declare pas codee)
  C. `effet_prop_monetaires` . 22 lignes `nd` -> effet Q7 v1.
                               LES LIGNES `chantier` ET `douteuse` N'EN
                               RECOIVENT AUCUN — D4 : une ligne non validee
                               n'exporte pas de donnee stabilisee. Leurs
                               effets proposes restent dans le fichier de
                               travail du lot 3, qui en garde la trace.
  D. corrections mesurees .... G032 date (arbitrage v112 : Heartbleed est du
                               2014-04-07) ; G006 date + precision (mars 2013,
                               enonce du wiki) ; G011 acteur principal
                               (fermeture reglementaire = regulateurs_etats,
                               le gabarit du lot 1 avait laisse core_devs) ;
                               G013 sous M1 (voir ci-dessous)
  E. colonnes A1 ............. `acteur_principal_mode`, `acteur_principal_id`,
                               `acteur_principal_nom` creees, vides partout
                               SAUF sur les 40 lignes du lot
  F. `notes` / `codage_justif`  la trace des corrections D, sur les seules
                               lignes concernees, dont les notes sont vides
                               dans la source (verifie)

M1 — G013 EST UN LANCEMENT, PAS UNE CRISE (arbitrage du 15/08/2026) :
`crise` oui -> non, `type_acte` incident -> innovation_protocolaire (grille de
codage v1 : « lancements de protocoles inclus »), `fil` crises-protocolaires
-> genese (le fil que porte deja E003, meme fait). Le doublon est SIGNALE et
non fusionne : E003 (texte, calibrage) et G063 (graphe) decrivent le meme
bloc de genese ; le dedoublonnage verifie avait classe G013 <-> G063 en
REJET_AUTO (types differents). G013 part donc en `douteuse`, comme les autres
doublons du lot. Aucune fusion, aucun patch graphe.

M2 — E015 EST CANONIQUE : G001 reste `douteuse` et ne recoit ni effet ni
role au maitre. E015 n'est pas touchee par ce lot (elle est hors des 40).

CONTROLES D'ARRIVEE (tous bloquants ; --dry-run les execute TOUS) :
  - source conforme : empreinte, 346 lignes CRLF, 30 colonnes, en-tete attendu ;
  - sortie : 346 lignes, 33 colonnes, en-tete = source + les 3 colonnes A1 ;
  - diff cellule a cellule EXACTEMENT egal au lot fige (99 cellules) ;
  - aucune ligne hors des 40 modifiee, sur AUCUNE colonne ;
  - les 3 colonnes A1 sont vides partout sauf sur les 40 ;
  - vocabulaires : `statut_ligne` dans D4, effets dans Q7 v1 gele (9 dimensions,
    signe obligatoire, `±` toujours accompagne d'une note), modes dans A1 ;
  - CRLF conserve partout, derniere ligne comprise ;
  - distribution des statuts affichee, avant et apres.

Usage:
    python3 scripts/make_v3_3_catalogue.py --dry-run
    python3 scripts/make_v3_3_catalogue.py
"""
import argparse
import csv
import hashlib
import io
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from grc20_commun import REPO  # noqa: E402

CODE_DONNEES, CODE_INVOCATION = 1, 2

DOSSIER = os.path.join(REPO, 'docs', 'research', 'catalogue-evenements')
CHEMIN_SOURCE = os.path.join(DOSSIER, 'catalogue-evenements-v3-2.csv')
CHEMIN_CIBLE = os.path.join(DOSSIER, 'catalogue-evenements-v3-3.csv')

EMPREINTE_SOURCE = '1b4b3aa4f74df0829ffbb149d22814e11e4324d5'
LIGNES_PHYSIQUES = 346
COLONNES_SOURCE = 30

COLONNES_A1 = ('acteur_principal_mode', 'acteur_principal_id',
               'acteur_principal_nom')

# Vocabulaires GELES — recopies pour etre verifies, jamais pour etre modifies.
VOC_STATUT = ('validee', 'chantier', 'a_arbitrer', 'douteuse', 'exclue')
VOC_DIMENSIONS = ('usage_paiement', 'valorisation', 'unite_compte_etalon',
                  'liquidite_convertibilite', 'conf_methodique',
                  'conf_hierarchique', 'conf_ethique', 'fongibilite',
                  'integrite_monnayage')
VOC_MODE = ('initiateur', 'entite_affectee', 'systeme_protocole',
            'a_arbitrer', 'nd')
MOTIF_EFFET = re.compile(r'^([a-z_]+)\((\+|-|±)\)$')

# Entites du graphe v115, resolues sur name + nameEn + labelEn + labelFr +
# aliases (jamais `name` seul : CLAUDE.md, piege des faux negatifs).
ENT_BITCOIN = 'd35d720e1fa24d9fbe665a90ac0abc73'   # Protocol — Bitcoin
ENT_COREBTC = '7b29b0d2d8404396bbaa5742e07d8f21'   # Core Developers (Bitcoin)
ENT_NAKAMOTO = '10960c9c308b4a3dad7ff86a20a1d2b5'  # Person — Satoshi Nakamoto

PROTO = (ENT_BITCOIN, 'protocole Bitcoin')

# --- LOT FIGE ---------------------------------------------------------------
# id -> (statut_final, mode, id_entite, nom, effet_ou_None)
# `effet` a None = la ligne ne recoit AUCUN effet au maitre (chantier ou
# douteuse). Ce n'est pas un oubli : c'est la regle D4.
LOT = {
    # -- 30 lignes validees ------------------------------------------------
    'G003': ('validee', 'systeme_protocole', *PROTO, 'integrite_monnayage(±)'),
    'G006': ('validee', 'systeme_protocole', *PROTO,
             'integrite_monnayage(-) conf_methodique(-)'),
    'G007': ('validee', 'initiateur', ENT_COREBTC, 'Core Developers (Bitcoin)',
             'integrite_monnayage(+)'),
    'G010': ('validee', 'systeme_protocole', *PROTO, None),
    'G014': ('validee', 'systeme_protocole', *PROTO, 'conf_methodique(±)'),
    'G015': ('validee', 'systeme_protocole', *PROTO, 'conf_methodique(±)'),
    'G016': ('validee', 'systeme_protocole', *PROTO,
             'conf_methodique(-) usage_paiement(-)'),
    'G017': ('validee', 'systeme_protocole', *PROTO, None),
    'G018': ('validee', 'systeme_protocole', *PROTO, 'conf_methodique(±)'),
    'G019': ('validee', 'systeme_protocole', *PROTO, 'conf_methodique(±)'),
    'G020': ('validee', 'systeme_protocole', *PROTO, 'conf_methodique(±)'),
    'G021': ('validee', 'systeme_protocole', *PROTO, 'conf_methodique(±)'),
    'G022': ('validee', 'systeme_protocole', *PROTO, 'conf_methodique(±)'),
    'G023': ('validee', 'systeme_protocole', *PROTO, 'conf_methodique(±)'),
    'G024': ('validee', 'systeme_protocole', *PROTO, 'conf_methodique(±)'),
    'G025': ('validee', 'systeme_protocole', *PROTO, None),
    'G026': ('validee', 'systeme_protocole', *PROTO, 'conf_methodique(±)'),
    'G027': ('validee', 'systeme_protocole', *PROTO, None),
    'G028': ('validee', 'systeme_protocole', *PROTO, 'integrite_monnayage(±)'),
    'G029': ('validee', 'systeme_protocole', *PROTO, 'conf_methodique(±)'),
    'G030': ('validee', 'systeme_protocole', *PROTO, 'integrite_monnayage(±)'),
    'G031': ('validee', 'systeme_protocole', *PROTO, 'conf_methodique(±)'),
    'G033': ('validee', 'initiateur', ENT_COREBTC, 'Core Developers (Bitcoin)',
             'conf_methodique(-)'),
    'G034': ('validee', 'systeme_protocole', *PROTO, 'conf_methodique(±)'),
    'G035': ('validee', 'initiateur', ENT_COREBTC, 'Core Developers (Bitcoin)',
             None),
    'G036': ('validee', 'initiateur', ENT_COREBTC, 'Core Developers (Bitcoin)',
             None),
    'G037': ('validee', 'systeme_protocole', *PROTO, None),
    'G039': ('validee', 'systeme_protocole', *PROTO, 'integrite_monnayage(±)'),
    'G040': ('validee', 'systeme_protocole', *PROTO, 'conf_methodique(±)'),
    'G042': ('validee', 'initiateur', ENT_COREBTC, 'Core Developers (Bitcoin)',
             None),
    # -- 4 douteuses (doublons ou validite contestee) ----------------------
    'G001': ('douteuse', 'systeme_protocole', *PROTO, None),   # M2 : E015 canonique
    'G008': ('douteuse', 'systeme_protocole', *PROTO, None),   # statut conteste
    'G011': ('douteuse', 'initiateur', '', 'FBI', None),       # doublon multiple
    'G013': ('douteuse', 'initiateur', ENT_NAKAMOTO, 'Satoshi Nakamoto', None),
    # -- 6 chantiers maintenus ---------------------------------------------
    'G004': ('chantier', 'systeme_protocole', *PROTO, None),
    'G005': ('chantier', 'systeme_protocole', *PROTO, None),
    'G009': ('chantier', 'systeme_protocole', *PROTO, None),
    'G032': ('chantier', 'systeme_protocole', *PROTO, None),
    'G038': ('chantier', 'initiateur', '', 'partisans UASF', None),
    'G041': ('chantier', 'systeme_protocole', *PROTO, None),
}

# --- Corrections mesurees : (colonne, avant attendu, apres) ------------------
# Les notes visees sont VIDES dans la source (verifie a l'execution) : ces
# ecritures ne recouvrent rien.
CORRECTIONS = {
    'G032': [
        ('date', '2014-07-04', '2014-04-07'),
        ('notes', '', 'date corrigee sous l arbitrage v112 (Heartbleed = '
                      '2014-04-07 ; le 04/07 etait la seule lecture MM/JJ du '
                      'graphe) — lot 3'),
    ],
    'G006': [
        ('date', '2013', '2013-03'),
        ('precision', 'annee', 'mois'),
        ('notes', '', 'mars 2013 (BIP-50) — precision portee depuis l enonce '
                      'du wiki des crises, lot 3'),
    ],
    'G011': [
        ('acteur_principal', 'core_devs', 'regulateurs_etats'),
        ('notes', '', 'doublon du meme fait avec E041, G052, G054 et F021 — '
                      'signale, non fusionne (lot 3)'),
        ('codage_justif',
         'wiki des crises (ch.III l.181-249) via graphe v97 : '
         'crisisType=Fermeture réglementaire — saisie par les autorités ; '
         'bogue decouvert/corrige par les devs (precedent E015) ; '
         'traitement en depot de code',
         'wiki des crises (ch.III l.181-249) via graphe v97 : '
         'crisisType=Fermeture réglementaire — saisie par les autorités. '
         'Lot 3 : acteur principal corrige en regulateurs_etats (le gabarit '
         'du lot 1 avait applique le motif « bogue corrige par les devs », '
         'sans objet pour une saisie judiciaire) ; effet nd'),
    ],
    'G013': [
        ('crise', 'oui', 'non'),
        ('type_acte', 'incident', 'innovation_protocolaire'),
        ('fil', 'crises-protocolaires', 'genese'),
        ('notes', '', 'M1 (15/08/2026) : Genesis est un lancement, pas une '
                      'crise — crise=non, acte de genese protocolaire. '
                      'Doublon signale et non fusionne avec E003 (texte, '
                      'calibrage) et G063 (graphe)'),
        ('codage_justif',
         'wiki des crises (ch.III l.181-249) via graphe v97 : '
         'crisisType=GENESIS — Lancement du protocole ; bogue '
         'decouvert/corrige par les devs (precedent E015) ; '
         'traitement en depot de code',
         'arbitrage M1 du 15/08/2026 : le crisisType=GENESIS du wiki ne fait '
         'pas de cette ligne une crise analytique. Lancement du protocole '
         '(innovation_protocolaire, grille v1 : « lancements de protocoles '
         'inclus ») ; initiateur S. Nakamoto ; effet nd'),
    ],
}

CODAGE_AVANT = 'propose(lot1)'
CODAGE_APRES = 'valide(lot3)'

# Attendus d'arrivee, comptes a la main depuis le lot ci-dessus et re-verifies
# par le script. Si l'un diverge, rien n'est ecrit.
ATTENDU_STATUT = 34          # 30 validee + 4 douteuse (6 chantier inchanges)
ATTENDU_CODAGE = 30
ATTENDU_EFFETS = 22
ATTENDU_CELLULES = 99        # total du diff, colonnes A1 exclues


def echec(msg, code=CODE_DONNEES):
    famille = 'invocation' if code == CODE_INVOCATION else 'donnees'
    print(f'ECHEC ({famille}) : {msg}', file=sys.stderr)
    sys.exit(code)


def empreinte_git(octets):
    h = hashlib.sha1()
    h.update(b'blob %d\x00' % len(octets))
    h.update(octets)
    return h.hexdigest()


def analyser(texte):
    return list(csv.reader(io.StringIO(texte), delimiter=';'))


def charger_source(chemin):
    if not os.path.exists(chemin):
        echec(f'catalogue source introuvable : {chemin}', CODE_INVOCATION)
    brut = open(chemin, 'rb').read()
    reelle = empreinte_git(brut)
    if reelle != EMPREINTE_SOURCE:
        echec(f'empreinte du catalogue source : {reelle}, attendue '
              f'{EMPREINTE_SOURCE} — v3-2 a change ; le lot fige ci-dessous '
              'decrit un autre fichier, il doit etre re-verifie')
    if not brut.endswith(b'\r\n') or brut.count(b'\r') != brut.count(b'\r\n'):
        echec('CRLF non conforme dans la source')
    lignes = brut[:-2].split(b'\r\n')
    if len(lignes) != LIGNES_PHYSIQUES:
        echec(f'{len(lignes)} lignes physiques, {LIGNES_PHYSIQUES} attendues')
    champs = analyser(brut.decode('utf-8'))
    if len(champs) != LIGNES_PHYSIQUES:
        echec('un champ multi-lignes ? le decoupage CRLF ne decrit pas ce '
              'fichier')
    if {len(c) for c in champs} != {COLONNES_SOURCE}:
        echec(f'largeurs de lignes heterogenes ou != {COLONNES_SOURCE}')
    if champs[0][-1] != 'statut_ligne':
        echec(f'derniere colonne source inattendue : {champs[0][-1]!r}')
    for col in COLONNES_A1:
        if col in champs[0]:
            echec(f'la colonne {col!r} existe deja dans la source : ce lot la '
                  'cree, il ne la remplit pas')
    return brut, champs


def valider_lot(champs, ix):
    """Verifie le lot fige CONTRE la source, avant toute ecriture."""
    par_id = {r[ix['id']]: r for r in champs[1:]}
    if len(LOT) != 40:
        echec(f'{len(LOT)} lignes au lot fige, 40 attendues')
    for cid, (statut, mode, eid, nom, effet) in sorted(LOT.items()):
        r = par_id.get(cid)
        if r is None:
            echec(f'{cid} absente de la source')
        if r[ix['codage_statut']] != CODAGE_AVANT:
            echec(f'{cid} : codage_statut {r[ix["codage_statut"]]!r}, '
                  f'{CODAGE_AVANT!r} attendu — cette ligne n appartient pas '
                  'au lot 1')
        if r[ix['statut_ligne']] != 'chantier':
            echec(f'{cid} : statut_ligne {r[ix["statut_ligne"]]!r}, toutes '
                  'les lignes du lot partent de `chantier`')
        if statut not in VOC_STATUT:
            echec(f'{cid} : statut {statut!r} hors vocabulaire D4')
        if mode not in VOC_MODE:
            echec(f'{cid} : mode {mode!r} hors vocabulaire A1')
        if effet is not None:
            if statut != 'validee':
                echec(f'{cid} : un effet est pose sur une ligne {statut!r} — '
                      'D4 : seule une ligne validee porte de la donnee '
                      'stabilisee au maitre')
            if r[ix['effet_prop_monetaires']] != 'nd':
                echec(f'{cid} : effet source {r[ix["effet_prop_monetaires"]]!r}'
                      ' — ce lot n ecrase aucun effet deja code')
            for jeton in effet.split(' '):
                m = MOTIF_EFFET.match(jeton)
                if not m or m.group(1) not in VOC_DIMENSIONS:
                    echec(f'{cid} : effet {jeton!r} hors vocabulaire Q7 v1 '
                          'gele (dimension inconnue ou signe manquant)')
        if eid and not re.fullmatch(r'[0-9a-f]{32}', eid):
            echec(f'{cid} : identifiant d entite mal forme : {eid!r}')
    # Les corrections visent-elles bien des lignes du lot, aux valeurs dites ?
    for cid, ops in sorted(CORRECTIONS.items()):
        if cid not in LOT:
            echec(f'correction sur {cid}, hors des 40 lignes du lot')
        for col, avant, _apres in ops:
            if col not in ix:
                echec(f'{cid} : colonne {col!r} inconnue')
            if par_id[cid][ix[col]] != avant:
                echec(f'{cid}.{col} vaut {par_id[cid][ix[col]]!r} dans la '
                      f'source, le lot attendait {avant!r} — la source a '
                      'derive, re-verifier avant d appliquer')


def appliquer(champs, ix):
    """-> (lignes de champs en sortie, diff [(id, colonne, avant, apres)])."""
    entete = list(champs[0]) + list(COLONNES_A1)
    sortie, diff = [entete], []
    for r in champs[1:]:
        cid = r[ix['id']]
        neuf = list(r)
        if cid in LOT:
            statut, mode, eid, nom, effet = LOT[cid]
            if neuf[ix['statut_ligne']] != statut:
                diff.append((cid, 'statut_ligne', neuf[ix['statut_ligne']],
                             statut))
                neuf[ix['statut_ligne']] = statut
            if statut == 'validee':
                diff.append((cid, 'codage_statut', neuf[ix['codage_statut']],
                             CODAGE_APRES))
                neuf[ix['codage_statut']] = CODAGE_APRES
            if effet is not None:
                diff.append((cid, 'effet_prop_monetaires',
                             neuf[ix['effet_prop_monetaires']], effet))
                neuf[ix['effet_prop_monetaires']] = effet
            for col, avant, apres in CORRECTIONS.get(cid, []):
                diff.append((cid, col, avant, apres))
                neuf[ix[col]] = apres
            neuf += [mode, eid, nom]
        else:
            neuf += ['', '', '']
        sortie.append(neuf)
    return sortie, diff


def controles_arrivee(champs_src, sortie, diff, ix):
    n_col = COLONNES_SOURCE + len(COLONNES_A1)
    if sortie[0] != list(champs_src[0]) + list(COLONNES_A1):
        echec('en-tete de sortie inattendu')
    if {len(r) for r in sortie} != {n_col}:
        echec(f'largeurs de sortie heterogenes ou != {n_col}')
    if len(sortie) != LIGNES_PHYSIQUES:
        echec(f'{len(sortie)} lignes en sortie, {LIGNES_PHYSIQUES} attendues')

    # -- diff reel, recalcule cellule a cellule (jamais la liste declaree) ---
    reel = []
    for avant, apres in zip(champs_src[1:], sortie[1:]):
        cid = avant[ix['id']]
        for col, i in ix.items():
            if avant[i] != apres[i]:
                reel.append((cid, col, avant[i], apres[i]))
        for k, col in enumerate(COLONNES_A1):
            val = apres[COLONNES_SOURCE + k]
            if cid not in LOT and val != '':
                echec(f'{cid} : {col} non vide sur une ligne hors lot')
    declare = sorted(diff)
    if sorted(reel) != declare:
        manquants = [c for c in declare if c not in reel]
        surnumeraires = [c for c in reel if c not in declare]
        echec('le diff constate ne correspond pas au lot declare : '
              f'{len(manquants)} manquant(s), {len(surnumeraires)} hors lot — '
              f'exemples : {(manquants + surnumeraires)[:3]}')
    hors_lot = {c for c, *_ in reel} - set(LOT)
    if hors_lot:
        echec(f'lignes modifiees hors des 40 du lot : {sorted(hors_lot)}')

    # -- comptes par famille ------------------------------------------------
    par_col = {}
    for _cid, col, _a, _b in reel:
        par_col[col] = par_col.get(col, 0) + 1
    attendus = {'statut_ligne': ATTENDU_STATUT, 'codage_statut': ATTENDU_CODAGE,
                'effet_prop_monetaires': ATTENDU_EFFETS}
    for col, n in attendus.items():
        if par_col.get(col, 0) != n:
            echec(f'{par_col.get(col, 0)} changement(s) sur {col}, {n} attendu(s)')
    if len(reel) != ATTENDU_CELLULES:
        echec(f'{len(reel)} cellules modifiees, {ATTENDU_CELLULES} attendues')

    # -- vocabulaires geles, sur TOUT le fichier de sortie -------------------
    for r in sortie[1:]:
        if r[ix['statut_ligne']] not in VOC_STATUT:
            echec(f'{r[0]} : statut hors vocabulaire D4')
        eff = r[ix['effet_prop_monetaires']].strip()
        if eff and eff != 'nd':
            for jeton in eff.split(' '):
                m = MOTIF_EFFET.match(jeton)
                if not m or m.group(1) not in VOC_DIMENSIONS:
                    echec(f'{r[0]} : effet {jeton!r} hors Q7 v1 gele')
        mode = r[COLONNES_SOURCE]
        if mode and mode not in VOC_MODE:
            echec(f'{r[0]} : mode {mode!r} hors vocabulaire A1')
        # r2 (gel du 15/08) : un `±` doit etre accompagne d'une note.
        if '±' in eff and not (r[ix['notes']].strip()
                               or r[ix['codage_justif']].strip()):
            echec(f'{r[0]} : effet ambivalent sans note — r2 exige la note')
    return par_col


def serialiser(sortie):
    tampon = io.StringIO()
    w = csv.writer(tampon, delimiter=';', lineterminator='\r\n',
                   quoting=csv.QUOTE_MINIMAL)
    w.writerows(sortie)
    return tampon.getvalue().encode('utf-8')


def distribution(champs, ix):
    d = {}
    for r in champs[1:]:
        s = r[ix['statut_ligne']]
        d[s] = d.get(s, 0) + 1
    return d


def main():
    ap = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--source', default=CHEMIN_SOURCE)
    ap.add_argument('--target', default=CHEMIN_CIBLE)
    ap.add_argument('--dry-run', action='store_true')
    args = ap.parse_args()

    if os.path.realpath(args.target) == os.path.realpath(args.source):
        echec('la cible est la source : ce script ecrit une v3-3, il '
              'n ecrase jamais la v3-2', CODE_INVOCATION)

    brut, champs = charger_source(args.source)
    ix = {c: i for i, c in enumerate(champs[0])}

    valider_lot(champs, ix)
    sortie, diff = appliquer(champs, ix)
    par_col = controles_arrivee(champs, sortie, diff, ix)
    octets = serialiser(sortie)

    if not octets.endswith(b'\r\n') or octets.count(b'\r') != octets.count(b'\r\n'):
        echec('CRLF non conforme en sortie')

    print(f'lot fige : 40 lignes, {len(diff)} cellules modifiees\n')
    print('changements par colonne :')
    for col in sorted(par_col):
        print(f'  {col:<24} {par_col[col]:>3}')
    print('\ndistribution `statut_ligne` :')
    av, ap_ = distribution(champs, ix), distribution(sortie, ix)
    for s in VOC_STATUT:
        a, b = av.get(s, 0), ap_.get(s, 0)
        fleche = '' if a == b else f'   ({b - a:+d})'
        print(f'  {s:<11} {a:>4} -> {b:>4}{fleche}')
    print(f'\nempreinte git de la cible : {empreinte_git(octets)}')
    print(f'taille : {len(octets)} octets')

    if args.dry_run:
        print('\n--dry-run : tous les controles ont tourne, diff cellule a '
              'cellule compris. Rien n a ete ecrit.')
        return 0

    tmp = args.target + '.tmp'
    try:
        with open(tmp, 'wb') as f:
            f.write(octets)
        os.replace(tmp, args.target)
    except OSError as err:
        if os.path.exists(tmp):
            os.unlink(tmp)
        echec(f'ecriture impossible : {err}')
    print(f'\ncatalogue ecrit : {os.path.relpath(args.target, REPO)}')
    return 0


if __name__ == '__main__':
    sys.exit(main())
