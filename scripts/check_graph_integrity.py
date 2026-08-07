#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Integrite structurelle des graphes GRC-20. Ne modifie rien.

Ce controle vivait en Python embarque dans `.github/workflows/check.yml`.
Il en sort pour une raison precise : du code qui n'existe que dans un YAML
ne s'execute qu'en CI, donc ne se verifie jamais avant d'etre pousse. Il a
livre une KeyError sur une ligne d'affichage — `r['missing_from']` au lieu
de `r['problem']` — invisible en local parce que ma simulation reproduisait
la decision, pas l'impression. Un fichier appelable evite cette classe
entiere d'erreur.

Regle : seul le graphe le plus recent est bloquant. Les instantanes geles
sont verifies et rapportes, jamais bloquants — v96 porte 15 endpoints
casses, corriges des v97, et personne ne compte reparer un instantane.

Controle croise avec le registre des proprietes
(grc20-properties-registry-v1.json) : actif seulement si le registre
existe. Toute cle d'attribut d'entite du graphe courant sans entree au
registre est bloquante ; les entrees du registre sans occurrence dans le
graphe sont signalees, jamais bloquantes (les cles depreciees par
patch_19 en font partie par construction).

Usage:
    python3 scripts/check_graph_integrity.py
    python3 scripts/check_graph_integrity.py --repo .

Codes de sortie :
    0 = le graphe courant est sain
    1 = le graphe courant porte au moins un defaut critique
"""
import argparse
import glob
import json
import os
import re
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from grc20_commun import TYPES_SECTION  # noqa: E402

# Relation orpheline portee exprès : `from` tronque a 16 caracteres, signalee
# depuis mai 2026 et laissee en l'etat en attente d'arbitrage. C'est une
# preuve de conservatisme, pas un defaut a masquer.
TOLEREES = {'9dee2daa2afa4212f6369b059e0cf78c'}

# Registre des cles d'attributs d'entites (genere par
# scripts/build_properties_registry.py). Le controle croise n'existe que si
# ce fichier existe : sans registre, rien n'est verifie ni bloque.
REGISTRE = 'grc20-properties-registry-v1.json'


def charger_registre(repo):
    chemin = os.path.join(repo, REGISTRE)
    if not os.path.exists(chemin):
        return None
    with open(chemin, encoding='utf-8') as fh:
        return json.load(fh)


def cles_attributs_entites(g):
    cles = set()
    for e in g.get('entities', []):
        a = e.get('attributes')
        if isinstance(a, dict):
            cles.update(a)
    return cles


def graphes_tries(repo):
    fichiers = glob.glob(os.path.join(repo, 'grc20-these-mael-rolland-v*.json'))
    return sorted(fichiers, key=lambda f: int(re.search(r'-v(\d+)\.json$', f).group(1)))


def main(argv=None):
    p = argparse.ArgumentParser(description="Integrite structurelle des graphes.")
    p.add_argument('--repo', default=os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    args = p.parse_args(argv)

    graphes = graphes_tries(args.repo)
    if not graphes:
        print('aucun graphe')
        return 0

    courant = graphes[-1]
    echec = False
    audit = os.path.join(args.repo, 'scripts', 'audit_graph.py')
    registre = charger_registre(args.repo)
    cles_registre, cles_depreciees = set(), set()
    if registre:
        cles_registre = {en['key'] for en in registre.get('entries', [])}
        cles_depreciees = {en['key'] for en in registre.get('entries', [])
                           if en.get('status') == 'deprecated'}

    for f in graphes:
        rapport = f'/tmp/{os.path.basename(f)[:-5]}.audit.json'
        subprocess.run([sys.executable, audit, '--input', f, '--json', rapport, '-q'],
                       stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        if not os.path.exists(rapport):
            print(f"  {os.path.basename(f)} : audit_graph.py n'a produit aucun rapport")
            echec = echec or f == courant
            continue
        with open(rapport, encoding='utf-8') as fh:
            critique = json.load(fh)['critical']

        casses = [r for r in critique['broken_relations_details']
                  if r.get('relation_id') not in TOLEREES]
        dups = len(critique['duplicate_ids'])
        orph = len(critique['orphans'])

        # Le bloc `ops` transporte des operations heritees des patchs
        # successifs. Personne ne le lisait, donc personne ne le verifiait :
        # 19 SET_ATTRIBUTE visant des entites disparues ont voyage de v96
        # jusqu'a v100 sans etre vues. `audit_graph.py` ne l'inspecte pas.
        with open(f, encoding='utf-8') as fh:
            g = json.load(fh)
        ids_entites = {e['id'] for e in g.get('entities', [])}
        ops_mortes = [o for o in g.get('ops', [])
                      if o.get('entityId') and o['entityId'] not in ids_entites]

        # Les metadonnees `space` sont ce que le pipeline GRC-20 publie
        # on-chain. Les scripts de construction v100 a v104 recopiaient le
        # bloc du graphe source sans le mettre a jour : les cinq annoncaient
        # « v99 ». Un graphe qui ment sur sa propre version trompe tout
        # consommateur, et rien ne le verifiait.
        m = re.search(r'-v(\d+)\.json$', f)
        attendu = f'v{m.group(1)}' if m else None
        version = (g.get('space') or {}).get('version')
        version_ok = version == attendu

        # Une cle de section vit a TROIS endroits : sur l'entite section, dans
        # les cartes d'ancrage, et dans l'attribut `section_key` porte par
        # chaque relation `appears in section`. Les migrations v100 et v106 ont
        # renumerote le premier et remappe le second ; personne n'a jamais
        # touche le troisieme, et aucun controle ne le regardait — celui-ci ne
        # lit pas les attributs de relation, `check_anchoring.py` ne lit que
        # les cartes. 3 970 relations ont ainsi declare une cle qui ne nommait
        # plus leur propre cible. L'attribut est denormalise : la verite est du
        # cote de `to`, et l'ecart se constate sans arbitrage.
        nom_type = {t['id']: t.get('name') or t['id'] for t in g.get('types', [])}
        cle_de = {}
        for e in g.get('entities', []):
            noms = [nom_type.get(t, t) for t in (e.get('types') or [])]
            if any(t in noms for t in TYPES_SECTION):
                k = ((e.get('attributes') or {}).get('section_key') or {}).get('value')
                if k:
                    cle_de[e['id']] = k
        cles_perimees = []
        for r in g.get('relations', []):
            attrs = r.get('attributes')
            if not isinstance(attrs, dict) or 'section_key' not in attrs:
                continue
            vraie = cle_de.get(r.get('to'))
            val = attrs['section_key']
            portee = val.get('value') if isinstance(val, dict) else val
            if vraie and portee and portee != vraie:
                cles_perimees.append((r.get('id'), portee, vraie))

        # Le registre des proprietes decrit le graphe courant (depuis v110,
        # patch_19 applique : trois cles disparues y sont gardees en
        # status='deprecated' avec leur champ supersededBy). Deux sens de
        # controle :
        #   - toute cle d'attribut d'entite du graphe courant doit avoir une
        #     entree au registre — bloquant, mais UNIQUEMENT si le registre
        #     existe, et jamais pour les instantanes geles ;
        #   - une entree du registre absente du graphe est signalee, jamais
        #     bloquante : les cles depreciees sont VOUEES a disparaitre du
        #     graphe des que patch_19 sera applique, et bloquer la-dessus
        #     interdirait d'appliquer le patch que le registre documente.
        hors_registre, absentes = [], []
        if registre:
            cles_graphe = cles_attributs_entites(g)
            hors_registre = sorted(cles_graphe - cles_registre)
            absentes = sorted(cles_registre - cles_graphe - cles_depreciees)

        marque = '<- courant, bloquant' if f == courant else '(gele, rapport seul)'
        reg_txt = ''
        if registre:
            reg_txt = f" · {len(hors_registre)} cle(s) hors registre"
        print(f"  {os.path.basename(f)}: {len(casses)} endpoint(s) casse(s) hors "
              f"tolerance · {dups} id(s) duplique(s) · {orph} orphelin(s) · "
              f"{len(ops_mortes)} op(s) orpheline(s) · "
              f"version {'OK' if version_ok else f'FAUSSE ({version})'} · "
              f"{len(cles_perimees)} cle(s) de relation perimee(s)"
              f"{reg_txt}  {marque}")
        # Detail seulement pour le graphe bloquant : les instantanes geles
        # portent tous les memes 19, et les lister cinq fois rendrait la
        # sortie CI illisible pour un etat que personne ne compte reparer.
        if f == courant:
            for rid, portee, vraie in cles_perimees[:5]:
                print(f"      relation {rid} : section_key « {portee} » "
                      f"mais la cible est « {vraie} »")
            for o in ops_mortes[:5]:
                print(f"      op {o.get('type')} {o.get('attributeId')} "
                      f"-> entite absente {o.get('entityId')}")
            for k in hors_registre[:5]:
                print(f"      cle d'attribut « {k} » absente du registre "
                      f"{REGISTRE}")
            # Rapport seul, jamais bloquant : entrees du registre que le
            # graphe courant ne porte plus (ou pas encore).
            if absentes:
                print(f"      {len(absentes)} entree(s) du registre sans "
                      f"occurrence dans le graphe courant (signale, non "
                      f"bloquant) : {', '.join(absentes[:5])}"
                      f"{' ...' if len(absentes) > 5 else ''}")
            if registre:
                disparues = sorted(cles_depreciees - cles_graphe)
                if disparues:
                    print(f"      {len(disparues)} cle(s) depreciee(s) deja "
                          f"sorties du graphe (attendu apres patch_19) : "
                          f"{', '.join(disparues)}")

        # Les cles sont celles que `audit_graph.py` emet reellement :
        # `problem` vaut « missing_from » / « missing_to », et le type porte
        # le nom `relation_type_name`. Les lire au lieu de les deviner.
        for r in casses[:5]:
            print(f"      {r.get('relation_id')} : {r.get('problem')} "
                  f"from={r.get('from')} to={r.get('to')} "
                  f"type={r.get('relation_type_name')}")

        if f == courant and (casses or dups or orph or ops_mortes or not version_ok
                             or cles_perimees or hors_registre):
            echec = True

    return 1 if echec else 0


if __name__ == '__main__':
    sys.exit(main())
