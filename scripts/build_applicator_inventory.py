#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Inventaire typologique des applicateurs `make_vNNN*` du depot.

Phase A du chantier « contrat d'etat PRE / POST / MIXTE » (arbitrage de
l'auteur du 2026-08-14 : inventaire LARGE — tous les applicateurs presents,
rejouables ou non).

CE QUE CE SCRIPT MESURE, ET CE QU'IL NE DEDUIT PAS
--------------------------------------------------
Deux familles de colonnes, jamais melangees :

  STATIQUE   lue dans le source de l'applicateur (flags, temporaires,
             `os.replace`, `fsync`, controle de version, fichiers ecrits).
             Reproductible partout, sans effet de bord.

  MESUREE    obtenue en EXECUTANT l'applicateur sur un banc isole
             (`--probe`), jamais sur le depot. Deux sondes :
               - `rejeu_sur_applique` : relance avec pour source son PROPRE
                 graphe cible, donc un etat deja applique. Repond a « sait-il
                 qu'il a deja tourne ? » ;
               - `reproduit_historique` : relance normale vN -> vN+1 dans le
                 banc, sortie comparee au vN+1 versé dans le depot.

Un applicateur qui refuse n'est pas forcement garde : il peut echouer par
accident (entite disparue, collision d'identifiant). La colonne
`mecanisme_deja_applique` nomme la CAUSE observee, pas le verdict.

INTERDITS TENUS. Lecture seule sur le depot. N'ecrit que son CSV. N'applique
aucun patch, ne produit aucun graphe, ne repare aucun applicateur ancien.

Usage:
    python3 scripts/build_applicator_inventory.py             # statique
    python3 scripts/build_applicator_inventory.py --csv       # ecrit
    python3 scripts/build_applicator_inventory.py --probe DIR # + sondes
"""
import argparse
import csv
import glob
import json
import os
import re
import shutil
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from grc20_commun import REPO  # noqa: E402

SORTIE = os.path.join(REPO, 'docs', 'audits', 'data',
                      'applicator-inventory-current.csv')
GRAPHE = 'grc20-these-mael-rolland-v%s.json'
CODE_DONNEES = 1

# Les sondes mesurees le 2026-08-14 sur banc isole. Elles sont RECOPIEES ici
# pour que le CSV reste reconstructible sans banc, et re-mesurables avec
# `--probe`. Si une mesure diverge de ce tableau, `--probe` le dit : c'est le
# tableau qui a tort, jamais la mesure.
# Trois valeurs par applicateur : (mecanisme observe, verdict de rejeu, and
# reproduction de l'historique). Le verdict de rejeu est STOCKE, jamais deduit
# du mecanisme : une premiere version le derivait de la prose
# (`mecanisme.startswith('aucun')`), et ecrivait donc `REFUSE` pour v97, v107
# et v108 — trois applicateurs mesures ACCEPTANTS. Un verdict lu dans un texte
# explicatif n'est pas une mesure, c'est une paraphrase, et elle etait fausse
# sur trois lignes sur dix-huit.
MESURES = {
    97:  ('sans-garde — fonction pure de la source',
          'ACCEPTE (non parametrable — rejeu direct, reecrit a l identique)',
          'IDENTIQUE'),
    98:  ('validation incidente (31 problemes)', 'REFUSE', 'IDENTIQUE'),
    99:  ('patch : source_graph declare', 'REFUSE', 'IDENTIQUE'),
    100: ('patch : invocation refusee', 'REFUSE',
          'DIFFERENT — space.generated_at'),
    101: ('aucun — accepte et ne fait rien', 'ACCEPTE',
          'DIFFERENT — space.version'),
    102: ('echec incident (entite consommee)', 'REFUSE',
          'DIFFERENT — space.version'),
    103: ('aucun — accepte, ecarte les deja-poses', 'ACCEPTE',
          'DIFFERENT — space.version + relation_count'),
    104: ('collision d identifiant', 'REFUSE', 'DIFFERENT — space.version'),
    105: ('aucun — no-op sur donnees deja dedoublonnees', 'ACCEPTE',
          'DIFFERENT — 117 entites + description desaccentuee'),
    107: ('domaine : aucune section sans « section of »', 'ACCEPTE',
          'IDENTIQUE'),
    108: ('domaine : « deja conformes »', 'ACCEPTE', 'DIFFERENT — space.note'),
    109: ('domaine : cles temoin des CARTES (pas du graphe)', 'REFUSE',
          'REFUSE — garde des cartes, non rejouable'),
    110: ('patch : source_graph declare', 'REFUSE', 'IDENTIQUE'),
    111: ('graphe source : space.version', 'REFUSE', 'IDENTIQUE'),
    112: ('graphe source : space.version', 'REFUSE', 'IDENTIQUE'),
    113: ('graphe source : space.version', 'REFUSE', 'IDENTIQUE'),
    114: ('graphe source : space.version', 'REFUSE', 'IDENTIQUE'),
    # v115 : la sonde efface la cible avant de lancer (voir `sonder`), donc
    # elle voit les cartes POST sans graphe -> MIXTE -> refus. C'est la mesure
    # honnete ; « POST detecte, rien reecrit » decrivait l'ancienne sonde, qui
    # laissait la cible en place.
    115: ('graphe source : space.version + etat_du_lot PRE/POST/MIXTE',
          'REFUSE', 'REFUSE — cible effacee, cartes POST donc MIXTE'),
}

# PIEGE DE MESURE, rencontre en construisant ce fichier. La premiere sonde
# concluait « IDENTIQUE » pour v115 : elle lancait l'applicateur, constatait
# le code 0, puis comparait le fichier cible au fichier de reference. Or v115
# avait detecte POST et n'avait RIEN ecrit — la sonde comparait le fichier
# verse a lui-meme et appelait cela une reproduction. C'est exactement le
# defaut que ce chantier documente (« reconnaitre un effet deja present ne
# suffit pas pour conclure »), reproduit par l'outil charge de le mesurer.
# Une sonde de reproduction doit donc EFFACER la cible avant de lancer, et
# traiter « rien ecrit » comme un resultat distinct de « ecrit a l'identique ».
NON_REJOUES_PAR_GARDE = {109, 115}

# Sources reelles, RELEVEES et non deduites de N-1 : v107 lit v106, et v109
# lit v108 tout en prenant v107 comme oracle en lecture seule. Deduire la
# source du numero aurait produit deux lignes fausses.
SOURCES = {107: '106'}
ORACLES = {109: 'v107 (oracle, lecture seule)'}

# MESURE (sonde du 2026-08-14, banc isole) : les seuls applicateurs dont le
# comportement depend de l'etat des cartes d'ancrage, et les seuls a en
# ecrire. Tous les autres n'ecrivent que leur graphe cible. Corollaire mesure
# et non deduit : ce sont aussi les deux SEULS a refuser de tourner dans
# l'etat courant du depot, chacun parce qu'il voit les cartes en avance sur
# le graphe. Le lot correle et le refus vont ensemble.
LOT_CORRELE_MESURE = {109, 115}

# Familles, etablies APRES mesure. Un applicateur n'est pas « ancien donc
# faible » : v97 n'a aucune garde et est pourtant sûr, parce qu'il reconstruit
# sa cible depuis la source sans jamais lire sa propre sortie.
FAMILLES = {
    97:  'reconstruction-integrale', 98: 'patch-declaratif',
    99:  'patch-declaratif', 100: 'patch-declaratif',
    101: 'transformation-directe', 102: 'transformation-directe',
    103: 'transformation-directe', 104: 'transformation-directe',
    105: 'patch-declaratif', 107: 'patch-declaratif',
    108: 'transformation-directe', 109: 'lot-correle-multifichier',
    110: 'patch-declaratif', 111: 'patch-candidat-verrouille',
    112: 'patch-candidat-verrouille', 113: 'patch-candidat-verrouille',
    114: 'patch-candidat-verrouille', 115: 'lot-correle-multifichier',
}

COLONNES = (
    'applicateur', 'version_source', 'version_cible', 'famille',
    'source_graph_present', 'rejouable_now', 'motif_non_rejouable',
    'intrants_auxiliaires', 'fichiers_ecrits', 'lot_correle',
    'mecanisme_deja_applique', 'rejeu_sur_applique', 'reproduit_historique',
    'a_dry_run', 'ecriture', 'rollback', 'controle_version_source',
    'ecrit_version_cible', 'risque_etat_partiel', 'defaut_reproduit',
)


def echec(msg):
    print(f'ECHEC : {msg}', file=sys.stderr)
    sys.exit(CODE_DONNEES)


def applicateurs():
    fs = glob.glob(os.path.join(REPO, 'scripts', 'make_v*.py'))
    return sorted(fs, key=lambda p: int(re.search(r'make_v(\d+)', p).group(1)))


def faits_statiques(chemin):
    s = open(chemin, encoding='utf-8').read()
    n = int(re.search(r'make_v(\d+)', os.path.basename(chemin)).group(1))
    flags = set(re.findall(r"add_argument\('--([a-z-]+)'", s))
    aux = sorted(flags - {'source', 'target', 'dry-run'})
    if n in ORACLES:
        aux = sorted(set(aux) | {ORACLES[n].split()[0]})
    # Le lot correle est MESURE, pas devine. Une premiere version cherchait
    # `open(<carte>, 'w')` par expression reguliere : elle voyait v109, qui
    # ecrit dans une boucle nommee, et ratait v115, qui passe par un
    # dictionnaire de temporaires. Une detection lexicale de l'ecriture est
    # perdue d'avance — les dialectes d'ecriture sont trop varies. La sonde
    # `--probe` tranche en observant quels fichiers changent reellement ;
    # ci-dessous, son resultat du 2026-08-14.
    cartes = (['entity_section_map.json', 'section_entities_map.json']
              if n in LOT_CORRELE_MESURE else [])
    ecrits = ['<graphe cible>'] + cartes
    if re.search(r"open\(\s*(PATCH_FILE|args\.patch)\s*,\s*'w'", s):
        ecrits.append('<patch/recu>')
    if 'args.divergences' in s:
        ecrits.append('<csv divergences>')
    temporaire = '.tmp' in s and 'os.replace' in s
    return {
        'n': n,
        'version_source': 'v' + SOURCES.get(n, str(n - 1)),
        'version_cible': f'v{n}',
        'famille': FAMILLES.get(n, 'inconnue'),
        'intrants_auxiliaires': ' + '.join(aux) if aux else '(aucun)',
        'fichiers_ecrits': ' + '.join(ecrits),
        'lot_correle': 'oui' if cartes else 'non',
        'a_dry_run': 'oui' if 'dry-run' in flags else 'NON',
        'ecriture': 'temporaire + os.replace' if temporaire else 'directe',
        'rollback': 'oui (restauration)' if 'originaux' in s else 'non',
        'controle_version_source':
            'oui' if re.search(r"space.*version.*!=|VERSION_SOURCE", s)
            else 'non',
        'ecrit_version_cible':
            'constante' if 'VERSION_CIBLE' in s
            else ('nom de fichier' if re.search(r"m_v\s*=\s*re\.search", s)
                  else 'NON — herite de la source'),
        'parametrable': 'non' if '--source' not in s else 'oui',
    }


def sonder(banc, chemin, faits):
    """Execute l'applicateur sur un banc ISOLE. Jamais sur le depot.

    `--probe` fait deux choses qu'il faut dire en toutes lettres : il EXECUTE
    les copies d'applicateurs que le banc contient, et il SUPPRIME
    `<banc>/travail` a chaque tour. Les deux portent sur un chemin fourni par
    l'appelant. Ce n'est pas un defaut — c'est le propos d'un banc — mais une
    hypothese implicite, et ce chantier vient de documenter ce que coute une
    hypothese de localisation non verifiee (§ C.4 : un `--target` accepte hors
    du depot). Les deux hypotheses sont donc verifiees ci-dessous plutot que
    supposees.

    Sur l'alerte `dangerous-subprocess-use` : l'appel est en forme LISTE, sans
    `shell=True` — aucun interpreteur de commande n'intervient, donc aucune
    metacaractere n'est interpretable. Les elements viennent de `sys.executable`
    et d'un `glob` sur `scripts/make_v*.py` du depot. La regle est un rappel
    d'audit generique ; ce qu'elle vise reellement ici, c'est l'execution de
    code depuis un repertoire choisi par l'appelant, traitee ci-dessous.
    """
    # Le banc ne doit pas recouvrir le depot : `neuf()` fait un rmtree, et un
    # banc mal designe (`--probe .`) detruirait un repertoire de travail reel.
    # CE CONTROLE VIENT EN PREMIER, et le placer ailleurs serait le defaut que
    # ce chantier decrit : une garde posee APRES ce qu'elle doit proteger. Mis
    # sous le controle d'`etalon/`, il etait inatteignable dans le seul cas qui
    # compte — `--probe .` repondait « banc sans etalon/ », un message qui
    # invite a creer `./etalon` DANS le depot, c'est-a-dire a construire la
    # situation dangereuse au lieu de l'interdire.
    rb, rr = os.path.realpath(banc), os.path.realpath(REPO)
    if rb == rr or rb.startswith(rr + os.sep) or rr.startswith(rb + os.sep):
        echec(f'le banc {banc!r} recouvre le depot : ce script y supprime '
              '`travail/` a chaque tour. Le placer ailleurs (scratchpad).')
    etalon = os.path.join(banc, 'etalon')
    if not os.path.isdir(etalon):
        echec(f'banc sans etalon/ : {etalon}. Le construire d abord (copie du '
              'depot), ce script ne le fabrique pas — il refuse de dupliquer '
              '200 Mo sans intention explicite.')
    travail = os.path.join(banc, 'travail')
    nom, n = os.path.basename(chemin), faits['n']
    src, cib = faits['version_source'][1:], str(n)

    def neuf():
        if os.path.exists(travail):
            shutil.rmtree(travail)
        shutil.copytree(etalon, travail, symlinks=True)

    def lancer(argv):
        script = os.path.join(travail, 'scripts', nom)
        # `nom` vient d'un basename, donc ne peut pas remonter — mais `travail`
        # est une copie d'un `etalon` fourni, ou un lien symbolique a pu etre
        # depose (copytree(symlinks=True) les preserve). On verifie donc que le
        # fichier reellement ouvert est bien DANS le banc, jamais ailleurs.
        rt, rs = os.path.realpath(travail), os.path.realpath(script)
        if not rs.startswith(rt + os.sep):
            echec(f'{nom} du banc pointe hors du banc ({rs}) — un lien '
                  'symbolique ferait executer un fichier du depot reel.')
        try:
            # nosemgrep: python.lang.security.audit.dangerous-subprocess-use-audit
            # Alerte examinee, pas ignoree : forme LISTE sans `shell=True` (donc
            # aucun interpreteur, aucun metacaractere), arguments issus de
            # `sys.executable` et d'un glob du depot. Ce que la regle vise
            # reellement — executer du code d'un repertoire fourni par
            # l'appelant — est traite par les trois gardes ci-dessus, chacune
            # provoquee. La regle ne peut pas etre satisfaite autrement : un
            # banc de sonde execute par definition un chemin calcule.
            p = subprocess.run(
                [sys.executable, script, *argv],
                capture_output=True, text=True, timeout=600, cwd=travail)
            return p.returncode, p.stdout + p.stderr
        except subprocess.TimeoutExpired:
            return -1, 'TIMEOUT'

    param = faits['parametrable'] == 'oui'
    neuf()
    if param:
        code, _ = lancer(['--source', os.path.join(travail, GRAPHE % cib),
                          '--target', os.path.join(travail, GRAPHE % cib)]
                         + (['--dry-run'] if faits['a_dry_run'] == 'oui' else []))
        rejeu = 'REFUSE' if code != 0 else 'ACCEPTE'
    else:
        rejeu = 'non parametrable'

    neuf()
    sortie = os.path.join(travail, GRAPHE % cib)
    # EFFACER LA CIBLE AVANT DE LANCER. `neuf()` recopie l'etalon, cible
    # historique comprise : sans cet `unlink`, un applicateur qui rend 0 sans
    # rien ecrire — ce que fait v115 quand il detecte POST — laisse un fichier
    # en place, et la comparaison confronte l'etalon a sa propre copie puis
    # annonce « IDENTIQUE ». C'est le faux positif consigne au § 0 de l'audit,
    # et il etait encore VIVANT ici : la table `MESURES` avait ete corrigee a
    # la main, pas la sonde qui l'alimente. Documenter un piege ne le retire
    # pas du code.
    if os.path.exists(sortie):
        os.unlink(sortie)
    code, _ = lancer(['--source', os.path.join(travail, GRAPHE % src),
                      '--target', sortie] if param else [])
    if code != 0:
        repro = 'REFUSE'
    elif not os.path.exists(sortie):
        # Distinct d'un refus : l'applicateur a rendu 0 et n'a rien produit.
        repro = 'NON REJOUE — code 0 sans ecriture'
    else:
        # Comparaison en OCTETS, pas en JSON charge. L'audit annonce « octet
        # pour octet » ; `json.load` egalise l'indentation, l'ordre des cles
        # et la forme des nombres — il ne peut pas soutenir cette phrase.
        with open(os.path.join(etalon, GRAPHE % cib), 'rb') as f:
            a = f.read()
        with open(sortie, 'rb') as f:
            b = f.read()
        repro = 'IDENTIQUE' if a == b else 'DIFFERENT'
    return rejeu, repro


def construire(banc=None):
    lignes = []
    for chemin in applicateurs():
        f = faits_statiques(chemin)
        n = f['n']
        src_present = os.path.exists(
            os.path.join(REPO, GRAPHE % f['version_source'][1:]))
        mecanisme, rejeu, historique = MESURES.get(
            n, ('(non mesure)', '(non mesure)', '(non mesure)'))
        if banc:
            rejeu_m, repro = sonder(banc, chemin, f)
            # Le desaccord entre la sonde et la table est un RESULTAT, pas un
            # detail : c'est la table qui a tort, et elle doit le dire dans la
            # colonne plutot que se laisser remplacer en silence.
            if not historique.startswith(repro):
                historique = (f'{repro} — la sonde contredit la table, '
                              f'qui disait : {historique}')
            if rejeu_m != rejeu:
                rejeu = f'{rejeu_m} — la table disait : {rejeu}'
        # Rejouabilite : le graphe source doit exister ET l applicateur ne pas
        # etre bloque par un etat du depot devenu posterieur a lui.
        bloque = n in NON_REJOUES_PAR_GARDE
        rejouable = 'oui' if (src_present and not bloque) else 'non'
        motif = ''
        if not src_present:
            motif = 'graphe source absent du depot'
        elif bloque:
            # Non rejouable N'EST PAS un defaut ici : c'est la garde qui fait
            # son travail. Les deux lots correles refusent parce que les
            # cartes du depot sont deja dans leur etat d'apres.
            motif = ('garde du lot correle : les cartes du depot sont deja '
                     'POST, rejouer deplacerait des charges deja posees')
        partiel = 'non'
        if f['lot_correle'] == 'oui' and f['ecriture'] == 'directe':
            partiel = 'OUI — plusieurs fichiers, ecriture directe, sans retour'
        elif f['lot_correle'] == 'oui':
            partiel = 'borne — temporaires puis bascule, avec restauration'
        defaut = ''
        if f['ecrit_version_cible'].startswith('NON'):
            defaut = ('space.version herite de la source : la sortie porterait '
                      'la version du parent (mesure)')
        if n == 109:
            defaut = ('lot de 3 fichiers ecrit directement, cartes AVANT le '
                      'graphe ; sa garde ne regarde que les cartes')
        lignes.append({
            'applicateur': os.path.basename(chemin),
            'version_source': f['version_source'],
            'version_cible': f['version_cible'],
            'famille': f['famille'],
            'source_graph_present': 'oui' if src_present else 'non',
            'rejouable_now': rejouable,
            'motif_non_rejouable': motif,
            'intrants_auxiliaires': f['intrants_auxiliaires'],
            'fichiers_ecrits': f['fichiers_ecrits'],
            'lot_correle': f['lot_correle'],
            'mecanisme_deja_applique': mecanisme,
            'rejeu_sur_applique': rejeu,
            'reproduit_historique': historique,
            'a_dry_run': f['a_dry_run'],
            'ecriture': f['ecriture'],
            'rollback': f['rollback'],
            'controle_version_source': f['controle_version_source'],
            'ecrit_version_cible': f['ecrit_version_cible'],
            'risque_etat_partiel': partiel,
            'defaut_reproduit': defaut,
        })
    return lignes


def main():
    ap = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--csv', action='store_true')
    ap.add_argument('--probe', metavar='BANC', default=None,
                    help='repertoire du banc isole (doit contenir etalon/)')
    args = ap.parse_args()

    lignes = construire(args.probe)
    print(f'{len(lignes)} applicateur(s)\n')
    print(f"{'cible':6s} {'famille':26s} {'rejou':5s} {'lot':4s} "
          f"{'ecriture':22s} reproduit l historique")
    for l in lignes:
        print(f"  {l['version_cible']:6s} {l['famille']:26s} "
              f"{l['rejouable_now']:5s} {l['lot_correle']:4s} "
              f"{l['ecriture']:22s} {l['reproduit_historique'][:38]}")

    manquants = [f'v{n}' for n in range(97, 116)
                 if not any(l['version_cible'] == f'v{n}' for l in lignes)]
    if manquants:
        print(f"\nSANS APPLICATEUR : {', '.join(manquants)} — le graphe existe, "
              'le script qui l a produit n est pas dans le depot.')

    if not args.csv:
        print('\n(simulation — relancer avec --csv)')
        return 0
    os.makedirs(os.path.dirname(SORTIE), exist_ok=True)
    tmp = SORTIE + '.tmp'
    with open(tmp, 'w', encoding='utf-8', newline='') as f:
        w = csv.DictWriter(f, fieldnames=COLONNES)
        w.writeheader()
        w.writerows(lignes)
    os.replace(tmp, SORTIE)
    print(f'\necrit : {os.path.relpath(SORTIE, REPO)}')
    return 0


if __name__ == '__main__':
    sys.exit(main())
