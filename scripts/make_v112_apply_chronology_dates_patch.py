#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Applique patch_candidate_chronology_dates_v1.json et produit v112.

CE QUE CE SCRIPT FAIT, ET RIEN D'AUTRE. Il ecrit DEUX valeurs de l'attribut
`date`, sur deux entites qui en portaient deja une, et qui la portaient
fausse :

    ca278d21…  CVE-2014-0160 Heartbleed      04/07/2014  ->  2014-04-07
    0d81bba0…  BitcoinTalk forum created     2010-11-22  ->  2009-11-22

Il ne cree aucune entite, aucune relation, aucune SourceQuote. Il ne fusionne
rien, ne renomme rien, ne retype rien. Il n'ecrit AUCUN `duplicateOf` et
AUCUN `reviewStatus`. Il ne touche a aucune autre date du graphe. Toute op qui
n'est pas un `SET_ATTRIBUTE` sur la cle `date` est REFUSEE, pas ignoree.

POURQUOI CES DEUX VALEURS SONT FAUSSES (chantier chronologie, PR #118,
docs/audits/grc20-chronology-dates-references-lab-v1.md) :

  Heartbleed — la valeur `04/07/2014` est la SEULE du graphe a se lire MM/JJ.
  Sur les 54 valeurs a barres, 26 sont decidables sans convention (un groupe
  > 12) et donnent JJ/MM 26 / MM/JJ 0. L'alerte versionnee de Bitcoin.org
  (`_alerts/2014-04-11-heartbleed.html`, front-matter `date: 2014-04-11`)
  etablit que la reponse est du 11 avril : elle ne peut pas preceder de trois
  mois un evenement du 4 juillet. Arbitrage de l'auteur du 2026-08-09 :
  cellule fausse de la figure « Chronologie n°4 », non seconde convention.

  BitcoinTalk — coquille d'annee, meme jour, meme mois. L'archive Nakamoto
  porte « Date: November 22, 2009 » pour le fil « Welcome to the new Bitcoin
  forum! », et l'attribut `description` de cette fiche meme dit « novembre
  2009 » : elle se contredit.

CE QUE CE SCRIPT REFUSE DE FAIRE, ET POURQUOI C'EST DELIBERE. La fiche
BitcoinTalk `0d81bba0` a tres probablement une jumelle, `06ac37fc`, qui porte
deja la bonne date. Le script n'ecrit NI `duplicateOf` NI `reviewStatus`, et
ne fusionne pas : l'assigner designerait une canonique, or `0d81bba0` a un
degre de 24 contre 22 pour `06ac37fc` — la fiche fausse est la MIEUX reliee.
C'est le piege C5 (grc20-dedup-events-audit-v1.md), et c'est le motif pour
lequel l'auteur refuse par ailleurs la fusion Mining pools. Corriger une date
n'autorise pas a trancher une identite.

LES `options` SONT PRESERVEES — choix declare, pas defaut. Le dialecte du
depot n'exprime qu'un couple `{type, value}`, alors que les deux attributs
vises portent aujourd'hui un `options.language` (`fr` et `en`), semantiquement
vide sur une date. Les RETIRER serait une modification que personne n'a
arbitree, et ferait mentir la promesse « exactement deux valeurs changees ».
Le script reecrit donc la seule cle `value` et laisse `type` et `options`
intacts. Purger les `options.language` des dates est un chantier distinct.

LES ANCIENNES VALEURS SONT VERIFIEES, PAS SUPPOSEES. Chaque op du patch porte
un bloc `_expected` (type, value, options) lu dans v111 au moment de la
redaction. Avant d'ecrire, le script exige que les TROIS champs concordent
avec ce que le graphe source porte reellement. Si le graphe a derive, ils ne
concordent plus et le script refuse. C'est le controle qui empeche de rejouer
un patch sur un graphe qui n'est plus celui qu'il decrit.

LE CONTROLE D'APRES EST EXHAUSTIF. Le resultat n'est pas seulement recompte :
il est compare a la source entite par entite, attribut par attribut, relation
par relation, type par type. Le script n'ecrit que si le diff complet vaut
EXACTEMENT deux valeurs de `date` changees — aucune cle creee ou supprimee,
aucun nom, aucun type, aucune relation, aucune op touchee.

Usage:
    python3 scripts/make_v112_apply_chronology_dates_patch.py --dry-run
    python3 scripts/make_v112_apply_chronology_dates_patch.py
"""
import argparse
import copy
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from grc20_commun import REPO  # noqa: E402

CODE_DONNEES, CODE_INVOCATION = 1, 2

CLE = 'date'
POLICY_CANDIDAT = 'CANDIDATE — NOT APPLIED — AUTHOR ARBITRATION REQUIRED'
VERSION_SOURCE = 'v111'
VERSION_CIBLE = 'v112'
OPS_ATTENDUES = 2

# Plafond du champ `space.note`, TOTAL et non seulement sur l'heritage.
# CLAUDE.md : « Keep `space.note` bounded (~1200 chars) ».
PLAFOND_NOTE = 1200

# Applicateur a USAGE UNIQUE : le lot est FIGE ici, pas seulement declare par
# le patch. Un patch retouche entre l'arbitrage et l'application ne doit pas
# passer parce qu'il aurait mis a jour son propre `op_count`.
#
# ET LE LOT FIGE PORTE LES VALEURS, pas seulement les identifiants. Figer les
# seuls ids laissait passer une reecriture de la valeur CIBLE : un patch
# retouche pouvait ecrire n'importe quelle date sur ces deux fiches, du moment
# que son `_expected` correspondait encore au graphe. C'est exactement ce que
# l'arbitrage de l'auteur a decide, et cela ne doit pas dependre du fichier de
# patch. Les deux operations approuvees sont donc reproduites ici, en entier.
LOT_APPROUVE = {
    # CVE-2014-0160 Heartbleed
    'ca278d213d804294a2c5a672d52808e4': {
        'attendu': {'type': 'TEXT', 'value': '04/07/2014',
                    'options': {'language': 'fr'}},
        'cible': {'type': 'TEXT', 'value': '2014-04-07'},
    },
    # InfrastructureEvent — BitcoinTalk forum created
    '0d81bba0461d49a5af8997a20663d630': {
        'attendu': {'type': 'TEXT', 'value': '2010-11-22',
                    'options': {'language': 'en'}},
        'cible': {'type': 'TEXT', 'value': '2009-11-22'},
    },
}
IDS_ATTENDUS = frozenset(LOT_APPROUVE)

# Cles d'attribut que ce lot n'a PAS le droit d'ecrire, meme si un patch
# retouche les demandait. Nommees pour que le refus soit lisible dans le
# message d'erreur plutot que noye dans un « attribut inattendu ».
CLES_INTERDITES = ('duplicateOf', 'reviewStatus')


def echec(msg, code=CODE_DONNEES):
    famille = 'invocation' if code == CODE_INVOCATION else 'donnees'
    print(f"ECHEC ({famille}) : {msg}", file=sys.stderr)
    sys.exit(code)


def lire(chemin, quoi):
    if not os.path.exists(chemin):
        echec(f"{quoi} introuvable : {chemin}", CODE_INVOCATION)
    try:
        with open(chemin, encoding='utf-8') as f:
            return json.load(f)
    except (json.JSONDecodeError, OSError) as err:
        echec(f"{quoi} illisible : {err}", CODE_INVOCATION)


def valider_patch(patch):
    """-> plan [(entity_id, attendu, cible)]. Refuse plutot que d'ignorer."""
    meta = patch.get('_meta')
    if not isinstance(meta, dict):
        echec("patch sans `_meta` exploitable")
    politique = meta.get('policy', '')
    if not politique.startswith(POLICY_CANDIDAT):
        echec("le patch ne porte pas la politique CANDIDATE attendue : "
              "ce script n'applique que le patch candidat de ce lot")
    if meta.get('source_graph') != f'grc20-these-mael-rolland-{VERSION_SOURCE}.json':
        echec(f"le patch declare source_graph = {meta.get('source_graph')!r} ; "
              f"cet applicateur lit {VERSION_SOURCE} et rien d'autre")

    ops = patch.get('ops')
    if not isinstance(ops, list):
        echec("patch sans liste `ops`")
    if len(ops) != OPS_ATTENDUES:
        echec(f"{len(ops)} op(s) dans le patch, {OPS_ATTENDUES} attendues — "
              "le lot est fige dans l'applicateur ; un patch elargi depuis "
              "l'arbitrage doit etre re-arbitre, pas applique")

    plan, vus = [], set()
    for i, op in enumerate(ops):
        if not isinstance(op, dict):
            echec(f"op #{i} n'est pas un objet")
        if op.get('type') != 'SET_ATTRIBUTE':
            echec(f"op #{i} de type {op.get('type')!r} : ce lot n'ecrit que "
                  "des SET_ATTRIBUTE")
        cle = op.get('attributeId')
        if cle in CLES_INTERDITES:
            echec(f"op #{i} vise `{cle}` : ce lot corrige des dates, il "
                  "n'annote AUCUNE identite. Marquer un doublon designerait "
                  "une canonique, ce qui reste a l'arbitrage de l'auteur")
        if cle != CLE:
            echec(f"op #{i} vise l'attribut {cle!r} : ce lot n'ecrit que `{CLE}`")
        eid = op.get('entityId')
        if eid not in IDS_ATTENDUS:
            echec(f"op #{i} vise l'entite {eid!r}, hors du lot fige — "
                  f"lot attendu : {sorted(IDS_ATTENDUS)}")
        if eid in vus:
            echec(f"l'entite {eid} est visee deux fois : en derniere ecriture "
                  "gagnante, une op serait silencieusement ecrasee")
        vus.add(eid)

        approuve = LOT_APPROUVE[eid]

        attendu = op.get('_expected')
        if not isinstance(attendu, dict):
            echec(f"op #{i} sans bloc `_expected` : l'ancienne valeur doit "
                  "etre declaree pour etre verifiee, jamais supposee")
        for champ in ('type', 'value', 'options'):
            if champ not in attendu:
                echec(f"op #{i} : `_expected` sans `{champ}` — les trois "
                      "champs sont exiges, `options` comprise : c'est elle "
                      "qui garantit qu'aucune option n'est perdue en silence")
        if attendu != approuve['attendu']:
            echec(f"op #{i} : `_expected` = {attendu!r}, le lot approuve "
                  f"declare {approuve['attendu']!r} — le patch a ete retouche "
                  "depuis l'arbitrage, il doit etre re-arbitre, pas applique")

        cible = op.get('value')
        if not isinstance(cible, dict):
            echec(f"op #{i} sans valeur cible exploitable")
        if cible != approuve['cible']:
            echec(f"op #{i} : valeur cible {cible!r}, le lot approuve declare "
                  f"{approuve['cible']!r} — figer les seuls identifiants "
                  "laisserait reecrire la date arbitree ; le lot porte donc "
                  "aussi les valeurs")
        plan.append((eid, attendu, cible))

    if vus != IDS_ATTENDUS:
        echec(f"le lot couvre {sorted(vus)}, attendu {sorted(IDS_ATTENDUS)}")
    return plan


def signature(graphe):
    """Etat compare avant/apres. Tout ce qui n'est pas `space` y entre.

    Les champs de tete ne sont PAS enumeres en dur. Une premiere version
    projetait sur (name, description, types, attributes) et ratait donc les
    3 entites du graphe qui portent en plus une cle `type` au singulier :
    un controle qui se dit exhaustif ne doit pas dependre d'une liste ecrite
    a la main, qui vieillit des qu'une entite gagne un champ."""
    entites = {}
    for e in graphe.get('entities', []):
        attrs = e.get('attributes') or {}
        autres = {k: json.dumps(v, sort_keys=True, ensure_ascii=False)
                  for k, v in e.items() if k not in ('id', 'attributes')}
        entites[e['id']] = {
            'champs': autres,
            'attributs': {k: json.dumps(v, sort_keys=True, ensure_ascii=False)
                          for k, v in attrs.items()},
        }
    return {
        'entites': entites,
        'relations': json.dumps(graphe.get('relations'), sort_keys=True,
                                ensure_ascii=False),
        'types': json.dumps(graphe.get('types'), sort_keys=True,
                            ensure_ascii=False),
        'relation_types': json.dumps(graphe.get('relation_types'),
                                     sort_keys=True, ensure_ascii=False),
        'ops': json.dumps(graphe.get('ops'), sort_keys=True, ensure_ascii=False),
    }


def diff_exhaustif(avant, apres):
    """-> liste des changements constates. Vide = graphes identiques."""
    changements = []
    for bloc in ('relations', 'types', 'relation_types', 'ops'):
        if avant[bloc] != apres[bloc]:
            changements.append(f'bloc `{bloc}` modifie')

    ids_a, ids_b = set(avant['entites']), set(apres['entites'])
    for eid in sorted(ids_a - ids_b):
        changements.append(f'entite supprimee : {eid}')
    for eid in sorted(ids_b - ids_a):
        changements.append(f'entite creee : {eid}')

    for eid in sorted(ids_a & ids_b):
        a, b = avant['entites'][eid], apres['entites'][eid]
        champs_a, champs_b = set(a['champs']), set(b['champs'])
        for champ in sorted(champs_a - champs_b):
            changements.append(f'{eid} : champ de tete `{champ}` SUPPRIME')
        for champ in sorted(champs_b - champs_a):
            changements.append(f'{eid} : champ de tete `{champ}` CREE')
        for champ in sorted(champs_a & champs_b):
            if a['champs'][champ] != b['champs'][champ]:
                changements.append(f'{eid} : `{champ}` modifie')
        cles_a, cles_b = set(a['attributs']), set(b['attributs'])
        for k in sorted(cles_a - cles_b):
            changements.append(f'{eid} : attribut `{k}` SUPPRIME')
        for k in sorted(cles_b - cles_a):
            changements.append(f'{eid} : attribut `{k}` CREE')
        for k in sorted(cles_a & cles_b):
            if a['attributs'][k] != b['attributs'][k]:
                changements.append(
                    f'{eid} : `{k}` {a["attributs"][k]} -> {b["attributs"][k]}')
    return changements


def main():
    defaut_source = os.path.join(
        REPO, f'grc20-these-mael-rolland-{VERSION_SOURCE}.json')
    defaut_cible = os.path.join(
        REPO, f'grc20-these-mael-rolland-{VERSION_CIBLE}.json')
    defaut_patch = os.path.join(REPO, 'patch_candidate_chronology_dates_v1.json')

    ap = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--source', default=defaut_source)
    ap.add_argument('--target', default=defaut_cible)
    ap.add_argument('--patch', default=defaut_patch)
    ap.add_argument('--dry-run', action='store_true',
                    help='verifie tout et affiche le plan, sans rien ecrire')
    args = ap.parse_args()

    patch = lire(args.patch, 'patch candidat')
    graphe = lire(args.source, 'graphe source')

    espace_source = graphe.get('space') or {}
    if espace_source.get('version') != VERSION_SOURCE:
        echec(f"le graphe source declare space.version = "
              f"{espace_source.get('version')!r} ; cet applicateur lit "
              f"{VERSION_SOURCE}", CODE_INVOCATION)

    plan = valider_patch(patch)
    par_id = {e['id']: e for e in graphe.get('entities', [])}

    # --- concordance des anciennes valeurs, AVANT toute mutation ------------
    print(f'lot fige : {OPS_ATTENDUES} op(s) sur la cle `{CLE}`\n')
    for eid, attendu, cible in plan:
        entite = par_id.get(eid)
        if entite is None:
            echec(f"entite {eid} absente du graphe source")
        actuel = (entite.get('attributes') or {}).get(CLE)
        if not isinstance(actuel, dict):
            echec(f"{eid} ne porte pas d'attribut `{CLE}` exploitable : ce lot "
                  "corrige des valeurs existantes, il n'en cree aucune")
        for champ in ('type', 'value'):
            if actuel.get(champ) != attendu.get(champ):
                echec(f"{eid} : `{CLE}.{champ}` vaut {actuel.get(champ)!r} dans "
                      f"le graphe, le patch attendait {attendu.get(champ)!r} — "
                      "le graphe a derive depuis la redaction du patch, "
                      "re-arbitrage requis")
        if (actuel.get('options') or {}) != (attendu.get('options') or {}):
            echec(f"{eid} : `{CLE}.options` vaut {actuel.get('options')!r}, le "
                  f"patch attendait {attendu.get('options')!r}")
        if actuel.get('value') == cible.get('value'):
            echec(f"{eid} : la valeur cible est deja en place — le patch a "
                  "deja ete applique, ou il ne decrit pas ce graphe")
        print(f'  {eid[:8]}  {entite.get("name", "")[:52]}')
        print(f'      `{CLE}` {actuel["value"]!r} -> {cible["value"]!r}')
        print(f'      options preservees : {actuel.get("options") or {}}')

    if os.path.realpath(args.target) == os.path.realpath(args.source):
        echec("la cible est le graphe SOURCE : ce script ecrit une nouvelle "
              "version, il n'ecrase jamais celle qu'il lit", CODE_INVOCATION)
    m_v = re.search(r'-(v\d+)\.json$', os.path.basename(args.target))
    if not m_v:
        echec("nom de sortie sans numero de version : "
              f"{os.path.basename(args.target)}", CODE_INVOCATION)
    if m_v.group(1) != VERSION_CIBLE:
        echec(f"cible en {m_v.group(1)} : cet applicateur produit "
              f"{VERSION_CIBLE} et rien d'autre", CODE_INVOCATION)

    avant = signature(graphe)
    resultat = copy.deepcopy(graphe)
    par_id_res = {e['id']: e for e in resultat['entities']}

    # --- mutation : la cle `value` SEULE ------------------------------------
    for eid, _attendu, cible in plan:
        attribut = par_id_res[eid]['attributes'][CLE]
        attribut['value'] = cible['value']

    apres = signature(resultat)
    changements = diff_exhaustif(avant, apres)
    attendus = {f'{eid} : `{CLE}` '
                f'{avant["entites"][eid]["attributs"][CLE]} -> '
                f'{apres["entites"][eid]["attributs"][CLE]}'
                for eid, _a, _c in plan}
    inattendus = [c for c in changements if c not in attendus]

    print(f'\ndiff exhaustif : {len(changements)} changement(s)')
    for c in changements:
        print(f'  {c}')
    if inattendus:
        echec("changement(s) hors lot detecte(s), rien n'est ecrit :\n  "
              + '\n  '.join(inattendus))
    if len(changements) != OPS_ATTENDUES:
        echec(f"{len(changements)} changement(s) constate(s), "
              f"{OPS_ATTENDUES} attendus")

    espace = resultat.setdefault('space', {})
    espace['version'] = VERSION_CIBLE
    espace['entity_count'] = len(resultat['entities'])
    espace['relation_count'] = len(resultat['relations'])
    # BORNE GLOBALE, pas seulement sur l'heritage. CLAUDE.md demande une note
    # d'environ 1200 caracteres ; v110/v111 la laissaient croitre (1513, 1703)
    # parce que le troncage ne portait que sur la partie heritee et que le
    # preambule neuf s'ajoutait par-dessus. On borne ici le TOTAL : la note
    # est un resume, l'historique complet vit dans CLAUDE.md et dans l'audit.
    tete = (
        "V112 — deux dates corrigees : Heartbleed CVE-2014-0160 "
        "(04/07/2014 -> 2014-04-07) et BitcoinTalk forum created "
        "(2010-11-22 -> 2009-11-22, coquille d'annee). Patch candidat "
        "patch_candidate_chronology_dates_v1.json applique apres arbitrage de "
        "l'auteur ; chantier chronologie PR #118. Rien d'autre n'a bouge. "
        "Aucun duplicateOf : le doublon BitcoinTalk (0d81bba0 / 06ac37fc) "
        "reste une dette, et v112 leve le veto de date qui l'ecartait du "
        "dedoublonnage automatique — voir "
        "docs/audits/grc20-v112-chronology-dates-application.md. ")
    heritee = espace.get('note', '')
    budget = max(0, PLAFOND_NOTE - len(tete))
    if len(heritee) > budget:
        # Le suffixe est RESERVE avant la decoupe. Sans cela, `rsplit` peut ne
        # rien retirer (quand la coupe tombe pile sur une espace) et les quatre
        # caracteres de « […] » debordent le plafond. La note actuelle faisait
        # 1200 par chance, pas par construction.
        marque = ' […]'
        utile = max(0, budget - len(marque))
        tronquee = heritee[:utile]
        if ' ' in tronquee:
            tronquee = tronquee.rsplit(' ', 1)[0]
        heritee = tronquee + marque
    espace['note'] = tete + heritee
    if len(espace['note']) > PLAFOND_NOTE:
        echec(f"space.note fait {len(espace['note'])} caracteres pour un "
              f"plafond de {PLAFOND_NOTE} : le bornage a echoue, rien n'est "
              "ecrit")

    # --dry-run sort ICI, et pas plus tot : un essai a blanc qui s'arreterait
    # avant la mutation et le diff ne verifierait que la lecture du patch. Tout
    # ce qui precede — validation de la cible, mutation en memoire, diff
    # exhaustif, refus des changements hors lot — a donc deja tourne, et la
    # seule chose que --dry-run evite est l'ecriture du fichier.
    if args.dry_run:
        print("\n--dry-run : tous les controles ont tourne, "
              "y compris le diff exhaustif. Rien n'a ete ecrit.")
        return 0

    temporaire = args.target + '.tmp'
    try:
        with open(temporaire, 'w', encoding='utf-8') as f:
            json.dump(resultat, f, ensure_ascii=False, indent=2)
        os.replace(temporaire, args.target)
    except OSError as err:
        if os.path.exists(temporaire):
            os.unlink(temporaire)
        echec(f"ecriture impossible : {err}")
    print(f'\ngraphe ecrit : {os.path.relpath(args.target, REPO)}')
    return 0


if __name__ == '__main__':
    sys.exit(main())
