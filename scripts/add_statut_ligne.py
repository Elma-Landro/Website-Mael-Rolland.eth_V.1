#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Ajoute la colonne `statut_ligne` (arbitrage D4) : catalogue v3-1 -> v3-2.

CE QUE CE SCRIPT FAIT, ET RIEN D'AUTRE. Il lit
`docs/research/catalogue-evenements/catalogue-evenements-v3-1.csv` (fige par
son empreinte git — un fichier source qui a change depuis l'arbitrage est
REFUSE), calcule pour chacune des 345 lignes de donnees UNE valeur du
vocabulaire ferme D4 (`validee` / `chantier` / `a_arbitrer` / `douteuse` /
`exclue`), et ecrit `catalogue-evenements-v3-2.csv` = v3-1 + la seule colonne
`statut_ligne`. Les 29 colonnes d'origine sont recopiees OCTET POUR OCTET
(la ligne brute est conservee, le statut est ajoute en fin de ligne) ; le
CRLF de chaque ligne, derniere comprise, est conserve. Il ne modifie jamais
le fichier source, ne touche ni au graphe, ni au site, ni a aucun autre
fichier.

TABLE DE PASSAGE (BLOC D par 1 du prompt lot 2, prompt archive dans
docs/audits/PROMPT-COWORK-lot2-statut-roles-q7.md) — par PRECEDENCE, la
premiere regle qui matche gagne :

  1. `exclue`     — aucune ligne aujourd'hui (la prehistoire est hors
                    fichier ; la decision D5 de la page d'architecture reste
                    ouverte). L'ensemble est VIDE et le script verifie qu'il
                    le reste.
  2. `a_arbitrer` — E004 (conflit domaine texte iii / figure iv, note
                    `[CHANTIER domaine…]` — bloquee par une decision Mael) ;
                    plus toute divergence de `table-divergences-dates.csv`
                    NON resolue par les corrections validees du 02/08
                    (etat-catalogue-v3-2026-08-05.md par 5). Les quatre
                    resolutions validees sont FIGEES ici avec leurs valeurs
                    attendues et VERIFIEES ligne a ligne dans le fichier :
                    une « resolution » dont la date ne concorde plus n'est
                    pas resolue, la ligne part en `a_arbitrer`.
  3. `douteuse`   — les lignes membres des 13 paires `A_VERIFIER` de
                    `docs/audits/data/doublons-verifies.csv`, jointes par
                    `gid` (recomptees ici : 21 lignes attendues — E001,
                    E035, E041, E049 + 17 lignes G) ; plus E017 BitLaundry
                    (divergence de dates JAMAIS resolue : ni 2010-09 ni
                    2010-12 confirmees — doute EMPIRIQUE, pas decision en
                    attente, d'ou `douteuse` et non `a_arbitrer`).
  4. `chantier`   — toute ligne restante portant `[CHANTIER` dans N'IMPORTE
                    QUELLE colonne (E019 et E081 le portent dans `type_acte`
                    et pas dans `notes` : un filtre sur `notes` seul en
                    manquerait 2 — controle nominal ci-dessous) ; toute
                    ligne a `codage_statut` vide ; toute ligne
                    `propose(lot1)` (les 40 lignes du lot 1 sont a re-coder
                    sous la regle D7, hors perimetre du lot 2).
  5. `validee`    — le reste. Controle : toute ligne qui tombe ici DOIT
                    porter `codage_statut = valide(calibrage)` (D4 exige
                    « sourcee ET codee » — seules les lignes de calibrage y
                    repondent aujourd'hui). Une ligne inattendue fait echouer
                    le script au lieu d'etre validee en silence.

NOTE D'ARCHITECTURE (D14 tranchee de fait) : D4 impose UNE valeur par ligne.
E001 est a la fois marquee `[CHANTIER` et membre d'une paire `A_VERIFIER` :
la precedence la classe `douteuse`. Le script le verifie nominalement.

CONTROLES D'ARRIVEE (tous bloquants, --dry-run les execute TOUS et ne
s'epargne que l'ecriture) :
  - source conforme : empreinte git attendue, 346 lignes physiques CRLF
    (en-tete + 345 donnees), 29 colonnes, en-tete attendu, aucun `\\r` isole ;
  - sortie : 346 lignes, 30 colonnes, en-tete d'origine + `;statut_ligne` ;
  - les 29 colonnes d'origine inchangees, comparees DEUX fois : champ a
    champ (csv) ET par reconstruction — retirer la colonne ajoutee redonne
    le fichier source OCTET POUR OCTET ;
  - CRLF conserve partout, derniere ligne comprise ;
  - aucune ligne sans statut, vocabulaire ferme respecte, ensemble `exclue`
    vide, cas nominaux (E001 douteuse, E004 a_arbitrer, E017 douteuse,
    E019/E081 chantier) ;
  - distribution des statuts affichee, avec le detail des petits ensembles.

Usage:
    python3 scripts/add_statut_ligne.py --dry-run
    python3 scripts/add_statut_ligne.py
"""
import argparse
import csv
import hashlib
import io
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from grc20_commun import REPO  # noqa: E402

CODE_DONNEES, CODE_INVOCATION = 1, 2

DOSSIER_CATALOGUE = os.path.join(REPO, 'docs', 'research',
                                 'catalogue-evenements')
CHEMIN_SOURCE = os.path.join(DOSSIER_CATALOGUE, 'catalogue-evenements-v3-1.csv')
CHEMIN_CIBLE = os.path.join(DOSSIER_CATALOGUE, 'catalogue-evenements-v3-2.csv')
CHEMIN_DOUBLONS = os.path.join(REPO, 'docs', 'audits', 'data',
                               'doublons-verifies.csv')
CHEMIN_DIVERGENCES = os.path.join(DOSSIER_CATALOGUE,
                                  'table-divergences-dates.csv')

# v3-1 est FIGEE : c'est l'etat du catalogue sur lequel les regles ci-dessous
# ont ete arbitrees et verifiees. Un fichier source different (meme d'un
# octet) n'est pas celui-la ; il exige une re-verification, pas une
# application aveugle.
EMPREINTE_SOURCE = '19e788a303c9d74b0feb8c069245fe66db49462b'

COLONNE_AJOUTEE = 'statut_ligne'
VOCABULAIRE = ('validee', 'chantier', 'a_arbitrer', 'douteuse', 'exclue')

LIGNES_PHYSIQUES = 346          # en-tete + 345 lignes de donnees
COLONNES_SOURCE = 29

EN_TETE_ATTENDU = [
    'id', 'origine', 'date', 'precision', 'date_brute', 'nature', 'intitule',
    'phase', 'domaine_8', 'systeme', 'acteur_principal', 'acteur_secondaire',
    'arene', 'type_acte', 'type_acte_2', 'effet_prop_monetaires', 'crise',
    'crisis_no', 'cve', 'fil', 'source', 'source_graphe', 'acteurs_graphe',
    'occurs_in', 'variantes', 'notes', 'gid', 'codage_statut',
    'codage_justif',
]

# --- Regle 2 : lot fige des resolutions de divergences validees le 02/08 ----
# (etat-catalogue-v3-2026-08-05.md par 5). La cle est l'id catalogue de
# `table-divergences-dates.csv`, la valeur la date que v3-1 DOIT porter pour
# que la divergence soit tenue pour resolue.
RESOLUTIONS_VALIDEES = {
    'E005': '2009-11-22',   # Bitcointalk — fonde le 22/11/2009 (verif. ext.)
    'E007': '2009-10-12',   # NewLibertyStandard — premiere transaction 12/10
    'E031': '2011-10-07',   # Litecoin — genese 07/10/2011 (verif. ext. 02/08)
    'E062': '2015-07-30',   # Frontier — 30/07/2015 (le texte l.399 corrige)
}
# Le dedoublement NewLibertyStandard a deux jambes : E007 (transaction 12/10)
# n'est resolu QUE si F001 (premier taux 05/10) existe avec sa date.
DEDOUBLEMENT_F001 = ('F001', '2009-10-05')

# BitLaundry : seule divergence de la table jamais resolue. Doute empirique
# (aucune des deux dates confirmee) -> `douteuse` par la regle 3, PAS
# `a_arbitrer` par la regle 2. Le prompt lot 2 le classe nominalement.
ID_BITLAUNDRY = 'E017'

ID_E004 = 'E004'

# --- Regle 3 : attendus du recomptage des paires A_VERIFIER -----------------
# Recomptes le 15/08/2026 sur doublons-verifies.csv x v3-1. Si le fichier de
# preuve change, le recomptage ne donnera plus cela : le script REFUSE alors
# d'ecrire, parce que la regle aura change de perimetre depuis l'arbitrage.
PAIRES_A_VERIFIER_ATTENDUES = 13
LIGNES_DOUTEUSES_ATTENDUES = 21
LIGNES_E_DOUTEUSES_ATTENDUES = frozenset({'E001', 'E035', 'E041', 'E049'})

# --- Controles nominaux (echec si l'un manque) ------------------------------
CAS_NOMINAUX = {
    'E001': 'douteuse',      # marquee [CHANTIER ET paire A_VERIFIER -> la
                             # precedence tranche D14 : douteuse
    'E004': 'a_arbitrer',    # conflit domaine texte iii / figure iv
    'E017': 'douteuse',      # BitLaundry
    'E019': 'chantier',      # [CHANTIER dans type_acte, pas dans notes
    'E081': 'chantier',      # idem — preuve que le filtre lit TOUTES les
                             # colonnes
}


def echec(msg, code=CODE_DONNEES):
    famille = 'invocation' if code == CODE_INVOCATION else 'donnees'
    print(f'ECHEC ({famille}) : {msg}', file=sys.stderr)
    sys.exit(code)


def empreinte_git(octets):
    """Empreinte blob git (sha1 sur l'en-tete `blob <taille>\\0` + contenu)."""
    h = hashlib.sha1()
    h.update(b'blob %d\x00' % len(octets))
    h.update(octets)
    return h.hexdigest()


def lire_octets(chemin, quoi):
    if not os.path.exists(chemin):
        echec(f'{quoi} introuvable : {chemin}', CODE_INVOCATION)
    with open(chemin, 'rb') as f:
        return f.read()


def analyser_csv(texte):
    """-> lignes de champs, via le module csv (guillemets geres)."""
    return list(csv.reader(io.StringIO(texte), delimiter=';'))


def charger_source(chemin):
    """Lit v3-1, verifie sa conformite, -> (octets, lignes_brutes, champs)."""
    brut = lire_octets(chemin, 'catalogue source')

    reelle = empreinte_git(brut)
    if reelle != EMPREINTE_SOURCE:
        echec(f'empreinte du catalogue source : {reelle}, attendue '
              f'{EMPREINTE_SOURCE} — v3-1 a change depuis l\'arbitrage du '
              f'15/08 ; re-verifier les regles avant de re-figer ce script')

    if not brut.endswith(b'\r\n'):
        echec('le catalogue source ne finit pas par CRLF')
    if brut.count(b'\r') != brut.count(b'\r\n'):
        echec('\\r isole detecte dans le catalogue source')

    lignes = brut[:-2].split(b'\r\n')
    if len(lignes) != LIGNES_PHYSIQUES:
        echec(f'{len(lignes)} lignes physiques dans la source, '
              f'{LIGNES_PHYSIQUES} attendues')
    if any(b'\n' in l for l in lignes):
        echec('\\n nu au milieu d\'une ligne : le decoupage CRLF ne decrit '
              'pas ce fichier')

    champs = analyser_csv(brut.decode('utf-8'))
    if len(champs) != LIGNES_PHYSIQUES:
        echec(f'{len(champs)} enregistrements csv, {LIGNES_PHYSIQUES} '
              'attendus — un champ multi-lignes ? le mode brut ne le '
              'supporterait pas')
    if champs[0] != EN_TETE_ATTENDU:
        echec(f'en-tete inattendu : {champs[0]}')
    largeurs = {len(c) for c in champs}
    if largeurs != {COLONNES_SOURCE}:
        echec(f'largeurs de lignes {sorted(largeurs)}, '
              f'{{{COLONNES_SOURCE}}} attendu')
    return brut, lignes, champs


def lignes_douteuses_par_gid(champs):
    """Joint les paires A_VERIFIER au catalogue par gid. -> ids catalogue."""
    brut = lire_octets(CHEMIN_DOUBLONS, 'doublons-verifies.csv')
    doublons = analyser_csv(brut.decode('utf-8'))
    if doublons[0][:1] != ['statut']:
        echec('doublons-verifies.csv : en-tete inattendu')
    ig = {c: i for i, c in enumerate(doublons[0])}
    for col in ('statut', 'canonique_id', 'doublon_id'):
        if col not in ig:
            echec(f'doublons-verifies.csv : colonne `{col}` absente')

    paires = [r for r in doublons[1:] if r[ig['statut']] == 'A_VERIFIER']
    if len(paires) != PAIRES_A_VERIFIER_ATTENDUES:
        echec(f'{len(paires)} paires A_VERIFIER, '
              f'{PAIRES_A_VERIFIER_ATTENDUES} attendues — le fichier de '
              'preuve a change depuis l\'arbitrage, re-verifier la regle 3')

    gids = set()
    for r in paires:
        gids.add(r[ig['canonique_id']])
        gids.add(r[ig['doublon_id']])

    ic = {c: i for i, c in enumerate(EN_TETE_ATTENDU)}
    ids = set()
    for r in champs[1:]:
        if r[ic['gid']].strip() and r[ic['gid']].strip() in gids:
            ids.add(r[ic['id']])

    if len(ids) != LIGNES_DOUTEUSES_ATTENDUES:
        echec(f'{len(ids)} lignes jointes par gid aux paires A_VERIFIER, '
              f'{LIGNES_DOUTEUSES_ATTENDUES} attendues : {sorted(ids)}')
    lignes_e = {i for i in ids if i.startswith('E')}
    if lignes_e != set(LIGNES_E_DOUTEUSES_ATTENDUES):
        echec(f'lignes E jointes : {sorted(lignes_e)}, attendues '
              f'{sorted(LIGNES_E_DOUTEUSES_ATTENDUES)}')
    return ids


def divergences_non_resolues(champs):
    """Verifie ligne a ligne les resolutions du 02/08. -> ids non resolus."""
    brut = lire_octets(CHEMIN_DIVERGENCES, 'table-divergences-dates.csv')
    table = analyser_csv(brut.decode('utf-8'))
    it = {c: i for i, c in enumerate(table[0])}
    if 'id_cal' not in it:
        echec('table-divergences-dates.csv : colonne `id_cal` absente')

    ic = {c: i for i, c in enumerate(EN_TETE_ATTENDU)}
    dates = {r[ic['id']]: r[ic['date']] for r in champs[1:]}

    non_resolues, verifiees = set(), []
    for r in table[1:]:
        id_cal = r[it['id_cal']]
        if id_cal == ID_BITLAUNDRY:
            # Divergence connue, jamais resolue, classee `douteuse` par la
            # regle 3 (doute empirique) — elle ne passe PAS par a_arbitrer.
            verifiees.append((id_cal, 'douteuse (regle 3, BitLaundry)'))
            continue
        attendue = RESOLUTIONS_VALIDEES.get(id_cal)
        if attendue is None:
            # Divergence hors du lot resolu du 02/08 : non resolue.
            non_resolues.add(id_cal)
            verifiees.append((id_cal, 'NON RESOLUE (hors corrections 02/08)'))
            continue
        portee = dates.get(id_cal)
        if portee != attendue:
            non_resolues.add(id_cal)
            verifiees.append((id_cal, f'NON RESOLUE (porte {portee!r}, '
                                      f'correction validee {attendue!r})'))
            continue
        if id_cal == 'E007':
            # Le dedoublement a deux jambes : F001 doit exister avec sa date.
            f_id, f_date = DEDOUBLEMENT_F001
            if dates.get(f_id) != f_date:
                non_resolues.add(id_cal)
                verifiees.append((id_cal, f'NON RESOLUE ({f_id} ne porte pas '
                                          f'{f_date!r} : dedoublement '
                                          'incomplet)'))
                continue
        verifiees.append((id_cal, f'resolue ({attendue})'))

    print('divergences de dates, verification ligne a ligne :')
    for id_cal, verdict in verifiees:
        print(f'  {id_cal}  {verdict}')
    return non_resolues


def classer(champs, douteuses_gid, a_arbitrer_dates):
    """-> [(id, statut, regle)] dans l'ordre du fichier."""
    ic = {c: i for i, c in enumerate(EN_TETE_ATTENDU)}
    resultat = []
    for r in champs[1:]:
        id_ = r[ic['id']]
        codage = r[ic['codage_statut']].strip()

        if False:                                   # regle 1 — `exclue` :
            statut, regle = 'exclue', 'regle 1'     # ensemble VIDE aujourd'hui
        elif id_ == ID_E004 or id_ in a_arbitrer_dates:
            statut, regle = 'a_arbitrer', 'regle 2'
        elif id_ in douteuses_gid or id_ == ID_BITLAUNDRY:
            statut, regle = 'douteuse', 'regle 3'
        elif any('[CHANTIER' in champ for champ in r):
            statut, regle = 'chantier', 'regle 4 (marqueur [CHANTIER)'
        elif codage == '':
            statut, regle = 'chantier', 'regle 4 (codage_statut vide)'
        elif codage == 'propose(lot1)':
            statut, regle = 'chantier', 'regle 4 (propose(lot1))'
        else:
            if codage != 'valide(calibrage)':
                echec(f'{id_} : codage_statut {codage!r} tombe en regle 5 '
                      'sans etre valide(calibrage) — cas non prevu par la '
                      'table de passage, rien n\'est ecrit')
            statut, regle = 'validee', 'regle 5'
        resultat.append((id_, statut, regle))
    return resultat


def construire_sortie(lignes_brutes, statuts):
    """Ajoute `;statut` a chaque ligne brute. -> octets du fichier cible."""
    sortie = [lignes_brutes[0] + b';' + COLONNE_AJOUTEE.encode('ascii')]
    for brute, (_, statut, _) in zip(lignes_brutes[1:], statuts):
        sortie.append(brute + b';' + statut.encode('ascii'))
    return b'\r\n'.join(sortie) + b'\r\n'


def controles_arrivee(brut_source, champs_source, octets_cible, statuts):
    """Tous les controles d'arrivee du BLOC D par 1. Echec = rien n'est ecrit."""
    # -- structure physique --------------------------------------------------
    if not octets_cible.endswith(b'\r\n'):
        echec('la cible ne finit pas par CRLF')
    if octets_cible.count(b'\r') != octets_cible.count(b'\r\n'):
        echec('\\r isole dans la cible')
    lignes_cible = octets_cible[:-2].split(b'\r\n')
    if len(lignes_cible) != LIGNES_PHYSIQUES:
        echec(f'{len(lignes_cible)} lignes physiques dans la cible, '
              f'{LIGNES_PHYSIQUES} attendues')

    # -- reconstruction : retirer la colonne ajoutee redonne v3-1 a l'octet --
    reconstruit = b'\r\n'.join(l.rsplit(b';', 1)[0] for l in lignes_cible)
    if reconstruit + b'\r\n' != brut_source:
        echec('la cible privee de sa derniere colonne ne redonne PAS la '
              'source octet pour octet')

    # -- champ a champ (csv) -------------------------------------------------
    champs_cible = analyser_csv(octets_cible.decode('utf-8'))
    if champs_cible[0] != EN_TETE_ATTENDU + [COLONNE_AJOUTEE]:
        echec(f'en-tete cible inattendu : {champs_cible[0]}')
    largeurs = {len(c) for c in champs_cible}
    if largeurs != {COLONNES_SOURCE + 1}:
        echec(f'largeurs cible {sorted(largeurs)}, une seule colonne devait '
              'etre ajoutee')
    for i, (av, ap) in enumerate(zip(champs_source, champs_cible)):
        if ap[:COLONNES_SOURCE] != av:
            echec(f'ligne {i + 1} : les 29 colonnes d\'origine different '
                  'champ a champ')

    # -- statuts -------------------------------------------------------------
    for r in champs_cible[1:]:
        if r[COLONNES_SOURCE] not in VOCABULAIRE:
            echec(f'{r[0]} : statut {r[COLONNES_SOURCE]!r} hors vocabulaire '
                  f'ferme {VOCABULAIRE}')
    if len(statuts) != LIGNES_PHYSIQUES - 1:
        echec(f'{len(statuts)} statuts calcules, {LIGNES_PHYSIQUES - 1} '
              'lignes de donnees')

    par_id = {id_: statut for id_, statut, _ in statuts}
    for id_, attendu in sorted(CAS_NOMINAUX.items()):
        if par_id.get(id_) != attendu:
            echec(f'cas nominal {id_} : {par_id.get(id_)!r}, attendu '
                  f'{attendu!r}')
    exclues = [i for i, s, _ in statuts if s == 'exclue']
    if exclues:
        echec(f'{len(exclues)} ligne(s) `exclue` alors que l\'ensemble doit '
              f'etre vide aujourd\'hui : {exclues}')


def afficher_distribution(statuts):
    compte = {v: 0 for v in VOCABULAIRE}
    par_regle = {}
    for _, statut, regle in statuts:
        compte[statut] += 1
        par_regle[regle] = par_regle.get(regle, 0) + 1

    print('\ndistribution `statut_ligne` (345 lignes de donnees) :')
    for v in VOCABULAIRE:
        print(f'  {v:<11} {compte[v]:>4}')
    print('detail par regle :')
    for regle in sorted(par_regle):
        print(f'  {regle:<35} {par_regle[regle]:>4}')

    petits = {'a_arbitrer', 'douteuse', 'exclue'}
    for v in sorted(petits):
        ids = [i for i, s, _ in statuts if s == v]
        if ids:
            print(f'  {v} = {" ".join(sorted(ids))}')
    n_lot1 = sum(1 for _, s, r in statuts
                 if s == 'chantier' and 'propose(lot1)' in r)
    print(f'  rappel : {n_lot1} lignes propose(lot1) classees chantier — a '
          're-coder sous D7, hors perimetre lot 2')
    return compte


def main():
    ap = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--source', default=CHEMIN_SOURCE)
    ap.add_argument('--target', default=CHEMIN_CIBLE)
    ap.add_argument('--dry-run', action='store_true',
                    help='execute TOUS les controles, n\'ecrit rien')
    args = ap.parse_args()

    if os.path.realpath(args.target) == os.path.realpath(args.source):
        echec('la cible est le fichier SOURCE : ce script ecrit une v3-2, '
              'il n\'ecrase jamais la v3-1 qu\'il lit', CODE_INVOCATION)

    brut, lignes_brutes, champs = charger_source(args.source)

    douteuses_gid = lignes_douteuses_par_gid(champs)
    print(f'\npaires A_VERIFIER jointes par gid : '
          f'{len(douteuses_gid)} lignes catalogue\n')
    non_resolues = divergences_non_resolues(champs)

    statuts = classer(champs, douteuses_gid, non_resolues)
    octets_cible = construire_sortie(lignes_brutes, statuts)
    controles_arrivee(brut, champs, octets_cible, statuts)
    compte = afficher_distribution(statuts)

    total = sum(compte.values())
    if total != LIGNES_PHYSIQUES - 1:
        echec(f'{total} statuts distribues, {LIGNES_PHYSIQUES - 1} attendus')

    print(f'\nempreinte git de la cible : {empreinte_git(octets_cible)}')

    if args.dry_run:
        print('--dry-run : tous les controles ont tourne, y compris la '
              'double comparaison des 29 colonnes. Rien n\'a ete ecrit.')
        return 0

    temporaire = args.target + '.tmp'
    try:
        with open(temporaire, 'wb') as f:
            f.write(octets_cible)
        os.replace(temporaire, args.target)
    except OSError as err:
        if os.path.exists(temporaire):
            os.unlink(temporaire)
        echec(f'ecriture impossible : {err}')
    print(f'catalogue ecrit : {os.path.relpath(args.target, REPO)}')
    return 0


if __name__ == '__main__':
    sys.exit(main())
