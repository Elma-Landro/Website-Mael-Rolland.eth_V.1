#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Compare 5 politiques d'affichage des panneaux du lecteur — DETERMINISTE,
et FIDELE au pipeline reel de `lecteur.html`.

HISTOIRE DE CE SCRIPT — la premiere version simulait les panneaux sur les
lignes BRUTES de `section_entities_map.json`, avec bris d'egalite par
entity_id partout. Une revue hostile a montre que ce n'etait PAS ce que le
site affiche : le lecteur (1) AGREGE les sections parentes (I.1 ... III.3,
conclu_theo) en sommant les occurrence_count de leurs descendantes, et
(2) trie SANS bris d'egalite — tri stable de JavaScript sur l'ordre de
construction de la liste. Contre-exemple mesure : sur I.2 (parente agregee),
hybrid-cautious conservait reellement 7 places sur 12, la ou l'ancien CSV
annoncait 0. La presente version reproduit le pipeline exact de
`loadGraph()` / `updateGraph()` de `lecteur.html` et a ete validee contre le
navigateur (voir `docs/audits/grc20-panel-policy-lab-v1.md`, section
Revision).

LE PIPELINE REPRODUIT (lecteur.html, mode ?panelLab=1) :
  1. N, df, dfd et TF-IDF calcules sur les lignes BRUTES de la carte
     (N = nombre de cles brutes, AVANT agregation) ;
  2. agregation des parentes (`GRC20Sections.arbreDescendants` de
     `sections.helpers.js`) : pour chaque parente, iteration sur
     [parente, ...descendantes triees], fusion par entity_id — somme des
     occurrence_count, somme des direct_anchor_count non null, meilleur
     snippet_status (`panelLabFusionneLigne`) ; l'ordre de la liste fusionnee
     est l'ordre de PREMIERE apparition (Map JS = dict Python) ;
  3. le score des parentes est RECALCULE apres agregation :
     occurrence_count agrege x log(N/df), avec le df BRUT — c'est ce que fait
     `loadGraph()` l.1344-1347, et c'est ce que `updateGraph()` lit ;
  4. panneau par section : epingles de `section_overrides.json` d'abord,
     puis les non-epinglees triees, tronque a 12
     (`MAX_GRAPH_NODES - epingles`).

LES 5 POLITIQUES :
  legacy          tri STABLE par score decroissant, SANS bris d'egalite —
                  c'est le comparateur canonique de `updateGraph()`, donc la
                  baseline REELLE du site. Les ex aequo gardent l'ordre de
                  construction de la liste du lecteur.
  verified-first  epingles ; puis snippet_status dans {self, self-base} par
                  score legacy ; puis toutes les autres par score legacy.
                  Pur reordonnancement, personne n'est exclu.
  direct-count    epingles ; puis direct_anchor_count >= 1 tries par
                  direct x log(N/dfd) (dfd = nb de sections BRUTES ou
                  l'entite a direct >= 1) ; puis FALLBACK des restantes
                  (direct 0 ou null) par score legacy — jamais vide.
  hybrid-cautious epingles ; puis classe de statut croissante (self=0,
                  self-base=1, proxy=2, no-snippet=3, inconnu=4), a
                  l'interieur d'une classe par score legacy.
  diagnostic-only ordre strictement identique a legacy (les badges sont une
                  affaire d'interface) — survie 100 % par construction.
Seules les politiques EXPERIMENTALES cassent les egalites par entity_id
(comparateurs de `panelLabComparateur` dans lecteur.html) ; `legacy` n'en a
pas — le tri stable suffit a la rendre deterministe.

MISE EN GARDE sur `direct_anchor_count` : c'est une mesure PAUVRE —
occurrences litterales du nom en limites de mots, qui sous-compte les noms
forges, traduits ou bilingues (« Proposition de Soft Fork — The DAO »,
l'appareil « Quote — » du chapitre III comptent 0 sans etre absents). Ne
jamais la lire seule ; croiser avec snippet_status, qui n'est pas non plus
un certificat (cf. grc20-poids-ancrage-v2.md § 5-6).

SORTIES :
  - CSV docs/audits/data/panel-policy-impact-v<N>.csv (separateur ;) — le
    nom est derive de la version du graphe detecte, pour qu'une future v111
    n'ecrase pas silencieusement le CSV v110. Une ligne par
    (section_key, politique), politiques x panneaux du lecteur reel
    (lignes brutes + parentes agregees, conclu_theo inclus).
  - Synthese imprimee : survie par politique, sections les plus
    bouleversees, sections pauvres en candidats mesures, places perdues
    par type d'entite.
  - Auto-controle FORMULE (lignes brutes, HORS simulation lecteur) : la
    variante stricte de direct-count, calculee sur les lignes brutes avec
    bris d'egalite entity_id, doit reproduire exactement le chiffre de
    build_anchor_weights.py --impact (294/648 sur v110). Il valide la
    formule TF-IDF partagee entre les deux scripts, PAS la baseline lecteur.

CE QUE CE SCRIPT NE FAIT PAS : il ne modifie ni la carte, ni le graphe, ni
les overrides, ni aucun fichier existant. Stdlib uniquement.

Usage:
    python3 scripts/compare_panel_policies.py
    python3 scripts/compare_panel_policies.py --top 12 --csv <chemin>
"""
import argparse
import collections
import csv
import json
import math
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from grc20_commun import REPO, graphe_le_plus_recent, numero_de_version  # noqa: E402

SEM = os.path.join(REPO, 'section_entities_map.json')
OVERRIDES = os.path.join(REPO, 'section_overrides.json')
DOSSIER_CSV = os.path.join(REPO, 'docs', 'audits', 'data')

POLITIQUES = ('diagnostic-only', 'direct-count', 'hybrid-cautious',
              'legacy', 'verified-first')
# Rang des statuts — aligne sur PANEL_LAB_RANG_STATUT de lecteur.html.
# Statut inconnu : rang 4, APRES no-snippet (meme convention que la fusion
# des parentes `panelLabFusionneLigne`, `?? 4`).
CLASSE_STATUT = {'self': 0, 'self-base': 1, 'proxy': 2, 'no-snippet': 3}
SEPARATEURS = ('.', '_')
# Valeur attendue de l'auto-controle formule par version de graphe
# (survivants, total), etablie par build_anchor_weights.py --impact au
# --top 12 du lecteur. Le controle ECHOUE si le chiffre devie ; pour une
# nouvelle version, etablir le chiffre avec --impact puis l'ajouter ici.
ATTENDU_FORMULE = {110: (294, 648)}


def charge_json(chemin, quoi):
    """Charge un JSON ou echoue proprement — aucun echec silencieux."""
    if not chemin or not os.path.exists(chemin):
        print(f"ERREUR : {quoi} introuvable : {chemin}", file=sys.stderr)
        sys.exit(2)
    with open(chemin, encoding='utf-8') as f:
        return json.load(f)


def type_premier(graphe):
    """-> {entity_id: nom du premier type}. 'INCONNU' si rien d'exploitable."""
    nom_type = {t['id']: t.get('name', t['id']) for t in graphe.get('types', [])}
    out = {}
    for e in graphe.get('entities', []):
        types = e.get('types') or []
        out[e['id']] = nom_type.get(types[0], types[0]) if types else 'INCONNU'
    return out


# ---------------------------------------------------------------------------
# Reproduction de sections.helpers.js (GRC20Sections) — la lecture des cles
# est ecrite UNE fois cote runtime ; ceci en est la copie de simulation.
# ---------------------------------------------------------------------------
def ancetres(cle):
    """Les ancetres d'une cle, du plus proche au plus lointain.

    « II.1.1.a » -> [« II.1.1 », « II.1 »] ; « conclu_theo_mon » ->
    [« conclu_theo »]. On s'arrete des qu'un ancetre ne porte plus de
    separateur (« II », « intro », « conclu » ne sont pas des sections).
    """
    out = []
    c = cle or ''
    while True:
        i = max(c.rfind(s) for s in SEPARATEURS)
        if i <= 0:
            break
        c = c[:i]
        if not any(s in c for s in SEPARATEURS):
            break
        out.append(c)
    return out


def arbre_descendants(cles):
    """-> {parente: [descendantes triees]}, ordre d'insertion preserve
    (= ordre de premiere apparition en iterant les cles, comme l'objet JS)."""
    arbre = {}
    for cle in cles:
        for a in ancetres(cle):
            arbre.setdefault(a, []).append(cle)
    for a in arbre:
        arbre[a].sort()
    return arbre


# ---------------------------------------------------------------------------
# Reproduction de loadGraph() : agregation des parentes, champs lab fusionnes
# ---------------------------------------------------------------------------
def fusionne_ligne(vu, e):
    """`panelLabFusionneLigne` de lecteur.html : somme des
    direct_anchor_count non null, meilleur snippet_status (inconnu = 4)."""
    if e.get('direct_anchor_count') is not None:
        vu['direct_anchor_count'] = ((vu.get('direct_anchor_count') or 0)
                                     + e['direct_anchor_count'])
    if (CLASSE_STATUT.get(e.get('snippet_status'), 4)
            < CLASSE_STATUT.get(vu.get('snippet_status'), 4)):
        vu['snippet_status'] = e['snippet_status']


def simule_chargement(sem_brut):
    """Reproduit loadGraph() : -> (sec_map post-agregation, tfidf, N, df, dfd).

    N, df, dfd et le TF-IDF des cles brutes sont calcules AVANT l'agregation,
    sur les lignes brutes — exactement comme le lecteur. Les parentes recoivent
    ensuite des lignes fusionnees et un TF-IDF recalcule sur le df brut.
    """
    cles_brutes = list(sem_brut)
    N = len(cles_brutes) or 1
    df = collections.Counter()
    dfd = collections.Counter()
    for d in sem_brut.values():
        for e in d.get('entities', []):
            df[e['entity_id']] += 1
            if (e.get('direct_anchor_count') or 0) >= 1:
                dfd[e['entity_id']] += 1

    # copie de travail : le lecteur mute sectionMap en place, nous aussi
    sec_map = {cle: {'entities': [dict(e) for e in d.get('entities', [])]}
               for cle, d in sem_brut.items()}
    tfidf = {}
    for cle, d in sec_map.items():
        tfidf[cle] = {e['entity_id']:
                      e['occurrence_count'] * math.log(N / (df[e['entity_id']] or 1))
                      for e in d['entities']}

    for parente, enfants in arbre_descendants(cles_brutes).items():
        contributeurs = [c for c in enfants
                         if sec_map.get(c, {}).get('entities')]
        if not contributeurs:
            continue
        cumul = {}   # dict Python = Map JS : ordre de premiere apparition
        for cle in [parente] + contributeurs:
            for e in sec_map.get(cle, {}).get('entities', []):
                vu = cumul.get(e['entity_id'])
                if vu:
                    vu['occurrence_count'] += e['occurrence_count']
                    fusionne_ligne(vu, e)
                else:
                    cumul[e['entity_id']] = dict(e)
        if not cumul:
            continue
        sec_map[parente] = {'entities': list(cumul.values()),
                            '_agrege_de': contributeurs}
        tfidf[parente] = {i: v['occurrence_count'] * math.log(N / (df[i] or 1))
                          for i, v in cumul.items()}
    return sec_map, tfidf, N, df, dfd


# ---------------------------------------------------------------------------
# Reproduction de updateGraph() + panelLabComparateur : les 5 panneaux
# ---------------------------------------------------------------------------
def panneaux_de(ents, scores, pins, top, N, dfd):
    """-> {politique: liste ordonnee du panneau}, pour une section donnee.

    `legacy` : tri STABLE par score decroissant sur l'ordre de la liste du
    lecteur, SANS bris d'egalite — le comparateur canonique de updateGraph()
    ((a,b) => score[b]-score[a], Array.prototype.sort est stable). Les
    politiques experimentales reproduisent panelLabComparateur : elles seules
    cassent les egalites par entity_id.
    """
    pin_set = set(pins)
    reste = [e for e in ents if e['entity_id'] not in pin_set]
    coupe = max(0, top - len(pins))

    def sc(e):
        return scores.get(e['entity_id']) or 0

    def panneau(cle_tri):
        return (list(pins)
                + [e['entity_id'] for e in sorted(reste, key=cle_tri)][:coupe])

    ordre_legacy = panneau(lambda e: -sc(e))          # tri stable, sans bris
    out = {'legacy': ordre_legacy, 'diagnostic-only': list(ordre_legacy)}
    out['verified-first'] = panneau(lambda e: (
        0 if e.get('snippet_status') in ('self', 'self-base') else 1,
        -sc(e), e['entity_id']))
    out['hybrid-cautious'] = panneau(lambda e: (
        CLASSE_STATUT.get(e.get('snippet_status'), 4),
        -sc(e), e['entity_id']))

    def cle_direct(e):
        d = e.get('direct_anchor_count') or 0
        if d >= 1:
            return (0, -(d * math.log(N / (dfd[e['entity_id']] or 1))),
                    e['entity_id'])
        return (1, -sc(e), e['entity_id'])
    out['direct-count'] = panneau(cle_direct)
    return out


def auto_controle_formule(sem_brut, ov, top, N, df, dfd):
    """Auto-controle FORMULE, lignes brutes, HORS simulation lecteur.

    Reproduit build_anchor_weights.py --impact : top-12 legacy AVEC bris
    d'egalite entity_id contre variante direct STRICTE (candidats mesures
    seuls, sans fallback), sur les 54 cles brutes. Valide la formule TF-IDF
    partagee entre les deux scripts — PAS la baseline lecteur, qui elle
    agrege les parentes et trie sans bris d'egalite.
    -> (survivants, total) — attendu 294/648 sur v110.
    """
    surv = tot = 0
    for cle in sorted(sem_brut):
        ents = sem_brut[cle].get('entities', [])
        if not ents:
            continue
        pins = [i for i in (ov.get(cle) or []) if isinstance(i, str)]
        reste = [e for e in ents if e['entity_id'] not in set(pins)]

        def score_legacy(e):
            return e['occurrence_count'] * math.log(N / (df[e['entity_id']] or 1))

        legacy = (pins + [e['entity_id'] for e in
                          sorted(reste, key=lambda e: (-score_legacy(e),
                                                       e['entity_id']))])[:top]
        avec_direct = [e for e in reste
                       if (e.get('direct_anchor_count') or 0) >= 1]
        strict = (pins + [e['entity_id'] for e in sorted(
            avec_direct,
            key=lambda e: (-((e.get('direct_anchor_count') or 0)
                             * math.log(N / (dfd[e['entity_id']] or 1))),
                           e['entity_id']))])[:top]
        surv += len(set(legacy) & set(strict))
        tot += len(legacy)
    return surv, tot


def main(argv=None):
    p = argparse.ArgumentParser(
        description="Compare 5 politiques d'affichage des panneaux du "
                    "lecteur (simulation fidele a lecteur.html, "
                    "deterministe, aucun fichier existant modifie).")
    p.add_argument('--csv', default=None,
                   help="chemin du CSV de sortie (defaut : "
                        "docs/audits/data/panel-policy-impact-v<N>.csv, "
                        "N = version du graphe detecte)")
    p.add_argument('--graph', default=None,
                   help="graphe de reference (defaut : le plus recent, "
                        "motif grc20-these-mael-rolland-v(\\d+).json)")
    p.add_argument('--map', default=SEM,
                   help="carte section -> entites (defaut : %(default)s)")
    p.add_argument('--overrides', default=OVERRIDES,
                   help="epingles par section (defaut : %(default)s)")
    p.add_argument('--top', type=int, default=12,
                   help="taille du panneau (defaut : 12, "
                        "= MAX_GRAPH_NODES du lecteur)")
    args = p.parse_args(argv)

    sem = charge_json(args.map, 'carte section -> entites')
    ov = charge_json(args.overrides, 'fichier des epingles')
    chemin_graphe = args.graph or graphe_le_plus_recent()
    graphe = charge_json(chemin_graphe, 'graphe de reference')
    type_de = type_premier(graphe)
    top = args.top
    version = numero_de_version(chemin_graphe)
    chemin_csv = args.csv or os.path.join(
        DOSSIER_CSV,
        f"panel-policy-impact-v{version if version is not None else 'X'}.csv")

    # ---------- pipeline du lecteur ----------
    sec_map, tfidf, N, df, dfd = simule_chargement(sem)

    # ---------- simulation des panneaux ----------
    lignes = []          # (section_key, policy, top_size, surv, nouveaux,
    #                       mesures, epingles, agregee_de)
    survie = collections.Counter()       # policy -> survivants cumules
    total = collections.Counter()        # policy -> places legacy cumulees
    pires = collections.defaultdict(list)  # policy -> [(surv, cle, taille)]
    perdus_par_type = collections.defaultdict(collections.Counter)
    sections_pauvres = []

    for cle in sorted(sec_map):
        ents = sec_map[cle].get('entities', [])
        if not ents:
            continue
        agregee_de = len(sec_map[cle].get('_agrege_de', []))
        pins = list(ov.get(cle) or [])   # comme le lecteur : liste telle quelle
        mesures = sum(1 for e in ents
                      if (e.get('direct_anchor_count') or 0) >= 1)
        if mesures < 3:
            sections_pauvres.append((cle, mesures))

        panneaux = panneaux_de(ents, tfidf.get(cle, {}), pins, top, N, dfd)
        ref = set(panneaux['legacy'])
        for pol in POLITIQUES:
            haut = panneaux[pol]
            s = len(ref & set(haut))
            lignes.append((cle, pol, len(haut), s, len(set(haut) - ref),
                           mesures, len(pins), agregee_de))
            survie[pol] += s
            total[pol] += len(panneaux['legacy'])
            pires[pol].append((s, cle, len(panneaux['legacy'])))
            for eid in ref - set(haut):
                perdus_par_type[pol][type_de.get(eid, 'INCONNU')] += 1

    # ---------- CSV ----------
    dossier = os.path.dirname(chemin_csv)
    if dossier:
        os.makedirs(dossier, exist_ok=True)
    lignes.sort(key=lambda x: (x[0], x[1]))
    with open(chemin_csv, 'w', encoding='utf-8', newline='') as f:
        w = csv.writer(f, delimiter=';', lineterminator='\n')
        w.writerow(['section_key', 'policy', 'top12_size',
                    'survivors_vs_legacy', 'new_entrants',
                    'measured_candidates', 'pinned', 'aggregated_from'])
        for ligne in lignes:
            w.writerow([str(c).replace(';', ',') for c in ligne])

    # ---------- synthese ----------
    nb_panneaux = len(lignes) // len(POLITIQUES)
    nb_parentes = sum(1 for c in sec_map if sec_map[c].get('_agrege_de'))
    print(f"graphe : {os.path.relpath(chemin_graphe, REPO)}")
    print(f"cles brutes : {N} · panneaux du lecteur simules : {nb_panneaux} "
          f"(dont {nb_parentes} parentes agregees) · top : {top}")
    print(f"csv : {os.path.relpath(chemin_csv, REPO)}")

    surv_strict, tot_strict = auto_controle_formule(sem, ov, top, N, df, dfd)
    print(f"\nauto-controle FORMULE (lignes brutes, bris entity_id, hors "
          f"simulation lecteur) :\n  direct STRICT vs legacy brut : "
          f"{surv_strict}/{tot_strict} ({100 * surv_strict // (tot_strict or 1)} %) "
          f"— doit reproduire build_anchor_weights.py --impact")
    # Le controle est BLOQUANT : un chiffre qui devie signifie que la formule
    # ou les donnees ont change, et la simulation ne vaudrait plus reference.
    # La valeur attendue est versionnee (etablie par build_anchor_weights.py
    # --impact sur la meme version) ; elle n'a de sens qu'au --top du lecteur.
    attendu = ATTENDU_FORMULE.get(version)
    if attendu and top == 12:
        if (surv_strict, tot_strict) != attendu:
            print(f"ECHEC (donnees) : auto-controle formule "
                  f"{surv_strict}/{tot_strict} au lieu de "
                  f"{attendu[0]}/{attendu[1]} attendu pour v{version} — "
                  f"comparer a build_anchor_weights.py --impact avant de se "
                  f"fier a la simulation.", file=sys.stderr)
            return 1
        print(f"  conforme a la valeur attendue v{version} "
              f"({attendu[0]}/{attendu[1]})")
    elif top != 12:
        print("  (controle non bloquant : --top != 12, la valeur de "
              "reference ne s'applique pas)")
    else:
        print(f"  ATTENTION : aucune valeur de reference versionnee pour "
              f"v{version} — etablir le chiffre avec build_anchor_weights.py "
              f"--impact et l'ajouter a ATTENDU_FORMULE.")
    print(f"\nsections avec < 3 candidats mesures : {len(sections_pauvres)} "
          f"({', '.join(f'{c} ({m})' for c, m in sections_pauvres)})")
    for pol in POLITIQUES:
        t = total[pol] or 1
        print(f"\n=== {pol} ===")
        print(f"  survie top-{top} : {survie[pol]}/{total[pol]} "
              f"({100 * survie[pol] // t} %)")
        bouleversees = sorted(pires[pol], key=lambda x: (x[0], x[1]))[:8]
        print("  les 8 sections les plus bouleversees :")
        for s, cle, n in bouleversees:
            print(f"    {cle:20s} survivants {s:2d}/{n:2d}")
        if perdus_par_type[pol]:
            print("  places perdues vs legacy, par type d'entite :")
            for nom, n in perdus_par_type[pol].most_common(5):
                print(f"    {n:4d}  {nom}")
        else:
            print("  places perdues vs legacy : aucune")
    return 0


if __name__ == '__main__':
    sys.exit(main())
