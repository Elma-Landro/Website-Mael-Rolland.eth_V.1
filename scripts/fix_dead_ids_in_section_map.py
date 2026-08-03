#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Repare les identifiants morts de `section_entities_map.json`.

La carte a ete generee une fois, a partir d'un graphe <= v81, et jamais
regeneree. Deux refontes du graphe ont depuis fait disparaitre des entites
qu'elle continue de citer : v81->v82 (les doublons de ThesisSection) et
surtout v90->v91 (« refonte ontologique complete »). Aucun de ces
identifiants ne disparait entre v96 et v100 : la migration des sections n'y
est pour rien.

Trois traitements, selon ce que devient l'ancrage :

  SUPPRIMER  le jumeau vivant est DEJA present dans chacune des memes
             sections, avec les memes compteurs. Reecrire l'id creerait un
             doublon dans la meme liste ; supprimer ne perd rien.
  REECRIRE   le vivant est absent des sections concernees. Supprimer
             perdrait l'ancrage ; on reecrit l'id, en FUSIONNANT le compteur
             la ou les deux se rencontrent (on garde le maximum).
  RETIRER    aucun successeur : l'ontologie v100 ne porte plus l'entite du
             tout. On retire la ligne, sans rien rattacher de force.

Les 9 cas qui demandaient un arbitrage de modelisation ont ete tranches
(voir docs/audits/grc20-dette-ancrage-v1.md) : les 8 domaines partent en
RETIRER, l'Omni Layer ambigu en REECRIRE vers le plus proche par le nom.

Usage:
    python3 scripts/fix_dead_ids_in_section_map.py --dry-run
    python3 scripts/fix_dead_ids_in_section_map.py --dedoublonner
"""
import argparse
import collections
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from grc20_commun import REPO, graphe_le_plus_recent  # noqa: E402

# Le jumeau vivant couvre deja toutes les sections du mort, compteurs egaux.
SUPPRIMER = {
    '19222ba7434e48048b655809d185c019': '179eaeedc85c47a09b7a4ada23fc825b',
    'abdb06a2683c4822a8ce7973f78a58f0': '596826c3187e4f8cb9034357477eb14c',
    'ad828085274a481f964bc843ee5b5db8': '6c2bbf0e45bc44ffa1d65b186df700c0',
    '9160f2bd7a6a48eea62f51c61c0c8ea9': '5a5684979bf84b37af3771f915f677e2',
    '5c3c493f16c80de9a51750d2089cf873': '22cda34c732d4ed389639be2024b5a18',
    'd3fd5a50d2834bfba881ccd92a167c98': 'e2cdb978bbdd4119aa946a271051a753',
    'cd2b195ab9af4c6b95ff01cda696a074': '06099088d8e14f7c8596a4f9fc8d3193',
    '12242085c21141b2b39a3a93f79854a7': 'acd16826920c47f4afc5e6ea59a3c56a',
}

# Les 6 jumeaux « … Ethereum » des InfrastructureDomain. v90 modelisait des
# domaines par protocole (un generique, un « … Ethereum ») ; v91 n'en garde
# qu'un, rendu agnostique. Les reecrire vers le generique reviendrait a
# affirmer « le segment Ethereum du domaine X » = « le domaine X », donc a
# effacer une partition que v90 posait explicitement. Arbitrage rendu :
# supprimer. L'indice qui a emporte la decision est que ces lignes sont
# generees en bloc — rangs consecutifs dans intro_B, occurrence_count = 2
# partout — donc du remplissage automatique, pas des occurrences reelles.
RETIRER = {
    'f6edb4c437324b699d600e5bff2acf8e',  # Du protocole Ethereum (couche 1 et 2)
    '8d122cfc7b9d4bd88380172edaee9b3a',  # Des services de portefeuille et de paiements Ethereum
    'd79fb4d0604a46af888889cb5ac5bf4b',  # De la sphere d'usage Ethereum
    '748d653bea9f4f20a5abcb6f61949f3d',  # De conformite aux reglementations nationales — Ethereum
    'd80e3f1d494f4257a2d2a63e0051f967',  # De l'information et de la connaissance — Ethereum
    '63def9d54a3d4747add20e5d608e68f0',  # Des Altcoins et tokens — ecosysteme Ethereum
    # Les deux seuls domaines de v90 sans AUCUN survivant en v100. Le Concept
    # homonyme n'en est pas le successeur : les deux coexistaient depuis v81,
    # la these distinguait donc le domaine d'infrastructure et le concept.
    '6b979b61416c4eb288f79f6053924afe',  # De l'activite de traitement des transactions
    '510c14a93e6c423982a96586d1e8bd9c',  # ... Ethereum
}

# Variantes orthographiques et formes longues, disparues a la refonte v91.
REECRIRE = {
    '4707641d2b42439c8ae9f9ed27a20a13': '75bcbab5bf17490bb6a742c27fd29df3',  # Eric -> Erik Voorhees
    'da8137c267234998936731fc2c4d8823': '728bc85a162d4419b31672b06ce8e96a',  # Gregory -> Greg Maxwell
    '7cbdc5b61b6f4dc482d9bc4d707d796f': '23413f9ac38a447495f166eb3ce987d5',  # Willet -> Willett
    'c1aedcf4e18c40198d09624d1de2b0dc': 'a33e5bb3119343a683d93da2e2130f1e',  # Shaoling -> Shaolin Fry
    '1537366704fb42f1ad70f57b0f95d6f0': 'f4b9aff00c1976c266295ed020e3c8e2',  # Mastercoin / Omni Layer
    'eaa89faac45945f6ac1a6ca3fa4088c7': '2af42270c40746e2876a3617ed8f7694',  # OP_RETURN
    'f75e5203926b4cd38bce44c2225bf069': '8db449e7a01f49589f19abd510071e97',  # Theymos
    'bf07dcda83d84da7a0a34452762c5eed': '3ba20dcf685d4e708cd990cb721e409b',  # Empreinte numerique / Hash
    '4c9b3ebf4d344807bd65f386b17d59b7': '49ce14952768472a9fe4c0c8f712e2e9',  # Jeff -> Jeffrey Wilcke
    # Arbitrage rendu. v90 portait 4 noeuds Omni/Mastercoin (2 Protocol,
    # 2 ActorNonHuman), v91 n'en garde qu'un de chaque : rien ne dit lequel
    # des morts va vers lequel des vivants. Choix retenu : le plus proche par
    # le nom, quitte a ce que les deux morts convergent vers la meme cible.
    '5a341f8c7e6141d9a1449b252f4cef89': 'f4b9aff00c1976c266295ed020e3c8e2',  # Omni Layer
}


def echec(msg):
    print(f"ECHEC : {msg}", file=sys.stderr)
    sys.exit(1)


def main(argv=None):
    p = argparse.ArgumentParser(description="Repare les ids morts de la carte.")
    p.add_argument('--graph', default=None)
    p.add_argument('--carte', default=os.path.join(REPO, 'section_entities_map.json'))
    p.add_argument('--dedoublonner', action='store_true',
                   help="Fusionne aussi les doublons deja presents dans la carte "
                        "(meme id liste deux fois dans une meme section).")
    p.add_argument('--dry-run', action='store_true')
    args = p.parse_args(argv)

    chemin = args.graph or graphe_le_plus_recent()
    with open(chemin, encoding='utf-8') as f:
        g = json.load(f)
    vivants = {e['id']: e.get('name', '') for e in g['entities']}
    with open(args.carte, encoding='utf-8') as f:
        sem = json.load(f)

    # Toute cible doit exister : reecrire vers un id mort serait pire que
    # de ne rien faire.
    absentes = [v for v in list(SUPPRIMER.values()) + list(REECRIRE.values())
                if v not in vivants]
    if absentes:
        echec(f"{len(absentes)} cible(s) absente(s) de "
              f"{os.path.basename(chemin)} : {absentes[:3]}")

    # Les suppressions supposent que le jumeau couvre deja tout. On le
    # reverifie ici plutot que de faire confiance a la table.
    def sections_de(eid):
        return {k: e['occurrence_count'] for k, v in sem.items()
                for e in v.get('entities', []) if e['entity_id'] == eid}

    for mort, vif in SUPPRIMER.items():
        manquantes = set(sections_de(mort)) - set(sections_de(vif))
        if manquantes:
            echec(f"{mort[:8]} : le jumeau {vif[:8]} ne couvre pas "
                  f"{sorted(manquantes)} — suppression NON sans perte")

    supprimes = reecrits = fusionnes = 0
    doublons_preexistants = 0
    for cle, bloc in sem.items():
        entites = bloc.get('entities') or []
        # Passe 1 : supprimer et reecrire, en marquant ce qui vient d'une
        # reecriture. On ne fusionne rien ici : le faire au fil de la liste
        # rendrait le resultat dependant de l'ordre — selon que le mort
        # precede ou suit son jumeau vivant, la fusion avait lieu ou non.
        intermediaire = []
        for e in entites:
            eid = e['entity_id']
            if eid in SUPPRIMER or eid in RETIRER:
                supprimes += 1
                continue
            issu_reecriture = eid in REECRIRE
            if issu_reecriture:
                cible = REECRIRE[eid]
                e = dict(e, entity_id=cible, entity_name=vivants[cible])
                reecrits += 1
            intermediaire.append((e, issu_reecriture))

        # Passe 2 : fusionner UNIQUEMENT les groupes qu'une reecriture a
        # rendus multiples. Les doublons deja presents dans la carte sont
        # comptes et laisses intacts — c'est un autre chantier.
        groupes = collections.OrderedDict()
        for e, reecrit in intermediaire:
            groupes.setdefault(e['entity_id'], []).append((e, reecrit))
        neuf = []
        for eid, membres in groupes.items():
            if len(membres) == 1:
                neuf.append(membres[0][0])
                continue
            if any(r for _, r in membres):
                garde = dict(membres[0][0])
                garde['occurrence_count'] = max(e['occurrence_count']
                                                for e, _ in membres)
                fusionnes += len(membres) - 1
                neuf.append(garde)
            elif args.dedoublonner:
                # Doublon deja present dans la carte, sans rapport avec les
                # ids morts. Arbitrage rendu : fusionner, compteur maximum.
                # Sans effet a l'ecran — le lecteur deduplique deja par
                # identifiant — mais la carte cesse de se contredire.
                garde = dict(membres[0][0])
                garde['occurrence_count'] = max(e['occurrence_count']
                                                for e, _ in membres)
                doublons_preexistants += len(membres) - 1
                neuf.append(garde)
            else:
                doublons_preexistants += len(membres) - 1
                neuf.extend(e for e, _ in membres)
        bloc['entities'] = neuf

    restants = {e['entity_id'] for v in sem.values()
                for e in v.get('entities', []) if e['entity_id'] not in vivants}

    print(f"graphe : {os.path.basename(chemin)}")
    print(f"  lignes supprimees      : {supprimes}")
    print(f"  identifiants reecrits  : {reecrits}")
    print(f"  collisions fusionnees  : {fusionnes} (creees par la reecriture)")
    print(f"  ids morts restants     : {len(restants)} (arbitrage humain)")
    etat = "fusionnes" if args.dedoublonner else "SIGNALES, non touches"
    print(f"  doublons preexistants  : {doublons_preexistants} — {etat}")

    if args.dry_run:
        print("--dry-run : rien ecrit.")
        return 0

    with open(args.carte, 'w', encoding='utf-8') as f:
        json.dump(sem, f, ensure_ascii=False, indent=2)
    print(f"ecrit : {os.path.relpath(args.carte, REPO)}")
    return 0


if __name__ == '__main__':
    sys.exit(main())
