#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Qualifie chaque ligne d'ancrage : d'ou vient son poids, et que vaut-il ?

LE PROBLEME (etabli par grc20-ancrage-poids-mandataires-v1.md) :
`occurrence_count` n'est pas un comptage de presence textuelle de l'entite.
C'est un nombre d'enregistrements dans `entity_section_map.json`, produit par
un appariement par mots-cles mandataires : 571 entites sur 1 171 partagent
leur signature d'occurrences avec une autre — 230 portent les occurrences du
mot « Bitcoin ». Le classement des panneaux de `lecteur.html` repose dessus.

CE QUE CE SCRIPT FAIT — deux champs NOUVEAUX, `occurrence_count` INTACT :

  `weightStatus` — une CLASSIFICATION, pas une mesure. Chaque ligne
  (section, entite) est qualifiee par la preuve que la carte porte deja,
  ses extraits (`snippet`) :
      'self'        le nom de l'entite figure dans au moins un extrait de
                    cette section — le poids compte bien l'entite ;
      'proxy'       des extraits existent mais aucun ne contient le nom —
                    le poids compte un autre terme (mandataire) ;
      'no-snippet'  aucun extrait pour ce couple (lignes issues de la
                    reconstruction v81 ou de reparations) — invérifiable.

  `directAnchorCount` — la seule MESURE ajoutee, et la plus pauvre possible :
  nombre d'occurrences du nom littéral de l'entite dans le texte de la
  section (corps du bloc + definitions des notes qui y sont appelees),
  insensible casse/accents/apostrophes, en LIMITES DE MOTS. La regle
  historique (§ 1.3 de l'audit) comptait en sous-chaine ; la limite de mots
  s'en ecarte deliberement : la sous-chaine comptait « Mist » dans
  « administration ». `null` quand la plage de la section n'est pas
  derivable (cles *_preamble sans bloc, glossaire).

CE QUE CE SCRIPT NE FAIT PAS : il ne change AUCUN classement (le lecteur
continue de lire `occurrence_count`), ne touche pas au graphe (la dette vit
dans la carte, pas dans le graphe — un patch de graphe l'y importerait), ne
supprime rien, n'invente aucun score compose. Retenir un autre classement
est un arbitrage d'auteur.

Usage:
    python3 scripts/build_anchor_weights.py              # diagnostic CSV seul
    python3 scripts/build_anchor_weights.py --apply      # + champs dans la carte
    python3 scripts/build_anchor_weights.py --check      # la carte est-elle a jour ?
"""
import argparse
import collections
import json
import os
import re
import sys
import unicodedata

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from grc20_commun import REPO  # noqa: E402

GRAPHE = os.path.join(REPO, 'grc20-these-mael-rolland-v110.json')
CARTE_TITRES = os.path.join(REPO, 'section-headings-map.json')
SEM = os.path.join(REPO, 'section_entities_map.json')
ESM = os.path.join(REPO, 'entity_section_map.json')
CSV_OUT = os.path.join(REPO, 'docs', 'audits', 'data',
                       'poids-ancrage-diagnostic-v110.csv')
MD = os.path.join(REPO, 'assets', 'MD')

# fichiers FR porteurs de blocs (le glossaire n'a pas de carte de titres)
FICHIERS_FR = ['00_introduction.md', '01_chapitre_I.md', '02_chapitre_II.md',
               '03_chapitre_III.md', '04_conclusion.md']
PREAMBULES = {'intro_preamble': '00_introduction.md',
              'ch1_preamble': '01_chapitre_I.md',
              'ch2_preamble': '02_chapitre_II.md',
              'ch3_preamble': '03_chapitre_III.md',
              'ccl_preamble': '04_conclusion.md'}


def norm(s):
    s = unicodedata.normalize('NFD', s or '')
    s = ''.join(c for c in s if unicodedata.category(c) != 'Mn')
    s = s.lower().replace('’', "'")
    return ' '.join(re.sub(r"[^a-z0-9' ]", ' ', s).split())


def plages():
    """-> {section_key: (fichier, ligne_debut, ligne_fin_exclue)} pour les
    cles derivables d'un bloc de titres FR. La plage va du titre au titre
    suivant de niveau <= au sien ; les preambules vont du debut de fichier au
    premier titre porteur de cle."""
    with open(CARTE_TITRES, encoding='utf-8') as f:
        carte = json.load(f)
    out = {}
    for fichier in FICHIERS_FR:
        heads = carte['files'].get(fichier, {}).get('headings', [])
        chemin = os.path.join(MD, fichier)
        n_lignes = sum(1 for _ in open(chemin, encoding='utf-8'))
        for i, h in enumerate(heads):
            if not h.get('key'):
                continue
            fin = n_lignes + 1
            for h2 in heads[i + 1:]:
                if h2['level'] <= h['level']:
                    fin = h2['line']
                    break
            out[h['key']] = (fichier, h['line'], fin)
        if heads:
            premier = min(h['line'] for h in heads if h.get('key'))
            for cle, f2 in PREAMBULES.items():
                if f2 == fichier:
                    out[cle] = (fichier, 1, premier)
    return out


def texte_de_plage(fichier, debut, fin, cache={}):
    """Corps du bloc + definitions des notes de bas de page qui y sont
    appelees. Les notes vivent en bloc terminal : une plage de lignes n'en
    contient aucune, il faut suivre les appels [^n]."""
    if fichier not in cache:
        cache[fichier] = open(os.path.join(MD, fichier),
                              encoding='utf-8').read().split('\n')
    lignes = cache[fichier]
    corps = [l for l in lignes[debut - 1:fin - 1]
             if not re.match(r'\[\^[^\]]+\]:', l)]
    corps_txt = '\n'.join(corps)
    appels = set(re.findall(r'\[\^([^\]]+)\](?!:)', corps_txt))
    notes = [l for l in lignes
             if (m := re.match(r'\[\^([^\]]+)\]:', l)) and m.group(1) in appels]
    return corps_txt + '\n' + '\n'.join(notes)


def main(argv=None):
    p = argparse.ArgumentParser(description="Qualifie les poids d'ancrage.")
    p.add_argument('--apply', action='store_true',
                   help="ecrit weightStatus/directAnchorCount dans la carte")
    p.add_argument('--check', action='store_true',
                   help="echoue si la carte n'est pas a jour")
    p.add_argument('--csv', default=CSV_OUT)
    args = p.parse_args(argv)

    with open(SEM, encoding='utf-8') as f:
        sem = json.load(f)
    with open(ESM, encoding='utf-8') as f:
        esm = json.load(f)
    with open(GRAPHE, encoding='utf-8') as f:
        g = json.load(f)
    noms = {e['id']: e.get('name', '') for e in g['entities']}

    # extraits par (entite, section), et signatures completes par entite
    extraits = collections.defaultdict(list)
    signature = {}
    for eid, rec in esm.items():
        sig = []
        for s in rec.get('sections', []):
            extraits[(eid, s.get('section_key'))].append(s.get('snippet') or '')
            sig.append((s.get('section_key'), s.get('snippet') or ''))
        signature[eid] = frozenset(sig)
    partagees = collections.Counter(signature.values())

    P = plages()
    textes_norm = {}
    for cle, (f2, a, b) in P.items():
        textes_norm[cle] = ' ' + norm(texte_de_plage(f2, a, b)) + ' '

    lignes_csv = []
    stats = collections.Counter()
    for cle in sem:
        for ent in sem[cle].get('entities', []):
            eid = ent['entity_id']
            nom = noms.get(eid) or ent.get('entity_name', '')
            nn = norm(nom)
            snips = extraits.get((eid, cle), [])
            if not snips:
                statut = 'no-snippet'
            elif nn and any(nn in norm(sn) for sn in snips):
                statut = 'self'
            else:
                statut = 'proxy'
            direct = None
            if cle in textes_norm and nn:
                direct = len(re.findall(r'(?<![a-z0-9])' + re.escape(nn) +
                                        r'(?![a-z0-9])', textes_norm[cle]))
            stats[statut] += 1
            lignes_csv.append((cle, eid, nom, ent.get('occurrence_count'),
                               statut, direct))
            ent_maj = {'weightStatus': statut, 'directAnchorCount': direct}
            if args.apply or args.check:
                ent['_maj'] = ent_maj

    # ---------- CSV ----------
    os.makedirs(os.path.dirname(args.csv), exist_ok=True)
    if not args.check:
        with open(args.csv, 'w', encoding='utf-8') as f:
            f.write('section_key;entity_id;entity_name;occurrence_count;'
                    'weightStatus;directAnchorCount\n')
            for cle, eid, nom, occ, st, d in lignes_csv:
                nom_csv = (nom or '').replace(';', ',')
                f.write(f'{cle};{eid};{nom_csv};{occ};{st};'
                        f'{"" if d is None else d}\n')

    sig_part = sum(1 for s, n in partagees.items() if n > 1 for _ in range(n))
    print(f"lignes de carte : {len(lignes_csv)}")
    for k, n in stats.most_common():
        print(f"  {n:6d}  {k}")
    print(f"entites partageant leur signature complete : "
          f"{sum(n for s, n in partagees.items() if n > 1)} / {len(signature)}")
    print(f"plages derivees : {len(P)} cles (sans plage : "
          f"{sorted(set(sem) - set(P))})")
    if not args.check:
        print(f"csv : {os.path.relpath(args.csv, REPO)}")

    # ---------- application / controle ----------
    if args.apply or args.check:
        change = 0
        for cle in sem:
            for ent in sem[cle].get('entities', []):
                maj = ent.pop('_maj')
                for k, v in maj.items():
                    if ent.get(k) != v:
                        ent[k] = v
                        change += 1
        if args.check:
            with open(SEM, encoding='utf-8') as f:
                disque = json.load(f)
            if disque != sem:
                print(f"--check : {change} champ(s) de poids perime(s) — "
                      f"relancer avec --apply.", file=sys.stderr)
                return 1
            print("--check : la carte est a jour.")
            return 0
        with open(SEM, 'w', encoding='utf-8') as f:
            json.dump(sem, f, ensure_ascii=False, indent=2)
        print(f"carte ecrite : {change} champ(s) poses/mis a jour, "
              f"occurrence_count INTACT")
    return 0


if __name__ == '__main__':
    sys.exit(main())
