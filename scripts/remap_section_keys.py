#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Repercute la renumerotation de patch_13 sur les cartes d'ancrage.

`section_key` est la cle de jointure entre le graphe et trois fichiers que
`lecteur.html` charge. Renumeroter le graphe sans les remapper les
desynchronise : le lecteur cherche des sections qui n'existent plus.

Le remappage est **simultane**, jamais sequentiel. Appliquer `I.2.1 ->
I.2.2` puis `I.2.2 -> I.2.2.b` deplacerait deux fois le meme lot : ce que
la premiere regle vient d'ecrire, la seconde le reprend. On lit l'ancien
etat, on ecrit le nouveau, sans jamais relire ce qu'on vient d'ecrire.

La table de correspondance n'est pas saisie ici : elle est **derivee de
patch_13**, seule source de verite. Un patch modifie, un remappage qui
suit.

Usage:
    python3 scripts/remap_section_keys.py --dry-run
    python3 scripts/remap_section_keys.py
"""
import argparse
import collections
import json
import os
import re
import sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

CARTES = ['section_entities_map.json', 'section_overrides.json', 'entity_section_map.json']


def echec(msg):
    print(f"ECHEC : {msg}", file=sys.stderr)
    sys.exit(1)


def table_de_correspondance(chemin_patch, chemin_graphe):
    """-> {ancienne_cle: nouvelle_cle}, lue dans patch_13 et le graphe source."""
    with open(chemin_patch, encoding='utf-8') as f:
        patch = json.load(f)
    with open(chemin_graphe, encoding='utf-8') as f:
        g = json.load(f)
    entites = {e['id']: e for e in g['entities']}
    remap = {}
    for o in patch.get('ops', []):
        if o['type'] != 'SET_ATTRIBUTE' or o['attributeId'] != 'section_key':
            continue
        ancienne = ((entites[o['entityId']].get('attributes') or {})
                    .get('section_key') or {}).get('value', '')
        if ancienne:
            remap[ancienne] = o['value']['value']
    return remap


def remappe(valeur, remap):
    return remap.get(valeur, valeur)


def main(argv=None):
    p = argparse.ArgumentParser(description="Repercute patch_13 sur les cartes d'ancrage.")
    p.add_argument('--patch', default=os.path.join(REPO, 'patch_13_section_migration.json'))
    p.add_argument('--graph', default=os.path.join(REPO, 'grc20-these-mael-rolland-v99.json'),
                   help="Le graphe AVANT migration : il porte les anciennes cles.")
    p.add_argument('--dry-run', action='store_true')
    args = p.parse_args(argv)

    remap = table_de_correspondance(args.patch, args.graph)
    if not remap:
        echec("aucune renumerotation dans le patch — rien a remapper")

    # Une cible ne doit pas etre elle-meme une source non traitee : ce serait
    # le signe que le patch n'est pas clos sur lui-meme.
    for ancienne, nouvelle in remap.items():
        if nouvelle in remap and remap[nouvelle] != nouvelle:
            print(f"  note : {ancienne} -> {nouvelle}, lui-meme deplace vers "
                  f"{remap[nouvelle]} — remappage simultane obligatoire")

    print("table de correspondance :")
    for a, b in sorted(remap.items()):
        print(f"  {a:10s} -> {b}")
    print()

    # --- le remappage a-t-il DEJA ete applique ? ---
    # Ce controle n'est pas une precaution de principe : ce remappage n'est
    # PAS idempotent. `I.1.2` et `I.2.2` sont a la fois cibles et sources
    # (I.1.3 -> I.1.2 et I.1.2 -> I.1.1.b). Le rejouer deplacerait une
    # seconde fois ce que la premiere passe vient d'ecrire, et melangerait
    # silencieusement des milliers d'epinglages.
    #
    # On le detecte par les cibles PURES — celles qui ne sont source de rien.
    # Leur presence dans les cartes ne peut venir que d'un remappage deja fait.
    cibles_pures = {b for b in remap.values() if b not in remap}
    deja = []
    for nom in CARTES:
        chemin = os.path.join(REPO, nom)
        if not os.path.exists(chemin):
            continue
        with open(chemin, encoding='utf-8') as f:
            contenu = f.read()
        presentes = sorted(c for c in cibles_pures if f'"{c}"' in contenu)
        if presentes:
            deja.append((nom, presentes))
    if deja:
        print("Le remappage semble DEJA applique :")
        for nom, presentes in deja:
            print(f"  {nom} porte deja {', '.join(presentes)}")
        echec("ce remappage n'est pas idempotent — le rejouer deplacerait une "
              "seconde fois les cles qui sont a la fois cible et source "
              f"({', '.join(sorted(k for k in remap if k in remap.values()))}). "
              "Repartez des cartes d'avant migration (git checkout) si vous "
              "voulez le rejouer.")


    # On opere sur le TEXTE, pas sur l'objet re-serialise. Re-serialiser
    # reecrirait les 127 000 lignes des cartes pour cinq cles changees, et
    # detruirait la mise en forme manuelle de section_overrides.json (lignes
    # vides entre les entrees). Un diff doit montrer ce qui change.
    #
    # Les deux motifs sont disjoints, verifie sur les fichiers : les cartes
    # indexees par section ne contiennent aucun `"section_key"`, et
    # entity_section_map n'a aucune cle de tete de section.
    # Chaque motif repose sur un invariant precis. Ils ne sont pas seulement
    # commentes : ils sont VERIFIES a l'execution, plus bas, contre le fichier
    # reel. Une reindentation du depot, ou l'apparition d'un `section_key`
    # imbrique, ferait echouer le controle au lieu de corrompre les donnees.
    MOTIFS = {
        # Invariant : les cles de section sont les cles de PREMIER niveau,
        # donc indentees de deux espaces exactement, et le fichier ne
        # contient aucun champ `"section_key"` imbrique.
        'section_entities_map.json': re.compile(r'(?m)^(  ")([^"]+)(":)'),
        'section_overrides.json': re.compile(r'(?m)^(  ")([^"]+)(":)'),
        # Invariant symetrique : les cles de section n'apparaissent QUE comme
        # valeur d'un champ `section_key`, jamais comme cle de premier niveau
        # (celles-ci sont des identifiants d'entite).
        'entity_section_map.json': re.compile(r'("section_key":\s*")([^"]+)(")'),
    }

    # Les deux formes doivent rester disjointes : si un fichier indexe par
    # section se mettait a porter des `section_key`, ou l'inverse, le motif
    # choisi manquerait la moitie des occurrences — silencieusement.
    ATTENDU_SECTION_KEY = {
        'section_entities_map.json': False,
        'section_overrides.json': False,
        'entity_section_map.json': True,
    }

    total = collections.Counter()
    ecritures = []

    for nom in CARTES:
        chemin = os.path.join(REPO, nom)
        if not os.path.exists(chemin):
            print(f"  {nom:28s} ABSENT")
            continue
        with open(chemin, encoding='utf-8') as f:
            texte = f.read()

        # --- verification des invariants, avant toute substitution ---
        porte_section_key = '"section_key"' in texte
        if porte_section_key != ATTENDU_SECTION_KEY[nom]:
            echec(f"{nom} : invariant rompu — le fichier "
                  f"{'porte' if porte_section_key else 'ne porte pas'} de champ "
                  f"`section_key`, l'inverse de ce que le motif suppose. "
                  f"Le format a change ; le remappage manquerait des occurrences.")

        objet_avant = json.loads(texte)
        if not ATTENDU_SECTION_KEY[nom]:
            # Les cles de premier niveau doivent TOUTES etre atteignables par
            # le motif : sinon l'indentation n'est pas celle qu'on croit.
            vues = {m.group(2) for m in MOTIFS[nom].finditer(texte)}
            manquantes = set(objet_avant) - vues
            if manquantes:
                echec(f"{nom} : {len(manquantes)} cle(s) de premier niveau hors "
                      f"de portee du motif ({sorted(manquantes)[:3]}). "
                      f"L'indentation du fichier n'est plus celle attendue.")

        touches = [0]

        def substitue(m, touches=touches):
            cible = remappe(m.group(2), remap)
            if cible != m.group(2):
                touches[0] += 1
            return m.group(1) + cible + m.group(3)

        neuf = MOTIFS[nom].sub(substitue, texte)

        # Le texte reste-t-il du JSON, et dit-il ce qu'on croit ?
        try:
            objet = json.loads(neuf)
        except json.JSONDecodeError as err:
            echec(f"{nom} : le remappage produit du JSON invalide ({err})")
        attendu = {remappe(k, remap) if nom != 'entity_section_map.json' else k
                   for k in json.loads(texte)}
        if set(objet) != attendu:
            echec(f"{nom} : le jeu de cles obtenu ne correspond pas a l'attendu")

        total[nom] = touches[0]
        ecritures.append((chemin, neuf))
        print(f"  {nom:28s} {touches[0]:5d} remappage(s)")

    print()
    print(f"total : {sum(total.values())} remappages")

    if args.dry_run:
        print("--dry-run : rien ecrit.")
        return 0

    for chemin, texte in ecritures:
        with open(chemin, 'w', encoding='utf-8') as f:
            f.write(texte)
        print(f"  ecrit : {os.path.basename(chemin)}")
    return 0


if __name__ == '__main__':
    sys.exit(main())
