#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Preflight des patchs candidats (patch_candidate_*.json) — lecture seule.

Un patch CANDIDAT n'est pas un patch applicable : il attend l'arbitrage de
l'auteur. Ce script verifie qu'un lot de candidats est COHERENT avec le graphe
courant et avec les invariants du depot AVANT que quiconque n'ecrive un
applicateur make_vNNN — c'est la lecon des incidents passes : la chaine de
doublons « Mining pools » (C4) venait de paires traitees independamment
(cf. scripts/verif_doublons.py, qui ferme depuis les grappes par transitivite),
et l'echec d'application de make_v110 venait d'un renommage creant une
homonymie exacte.

CE QUE CE SCRIPT NE FAIT PAS : il n'applique aucun patch, ne modifie ni le
graphe ni aucun fichier existant (seul --report-json ecrit, a l'endroit
demande). Stdlib uniquement. Sortie deterministe : aucun horodatage, tris
stables partout.

LES 13 CONTROLES (codes C01..C13), chacun OK / AVERTISSEMENT / BLOQUANT :
  C01  le JSON parse (sinon BLOQUANT, les autres patchs continuent) ;
  C02  _meta present avec policy, source_graph, patch_id, description ;
  C03  la policy commence par « CANDIDATE — NOT APPLIED — AUTHOR
       ARBITRATION REQUIRED » — un candidat mal marque est refuse ;
  C04  source_graph nomme un graphe du depot ; AVERTISSEMENT si ce n'est
       pas le plus recent (patch depose contre un etat anterieur) ;
  C05  comptes declares (op_count/candidate_count, skipped_count) = reels ;
  C06  toute op visant une entite existante la trouve dans le graphe ;
  C07  ids de types connus du graphe ; coherence id<->nom si typeNames ;
  C08  cles d'attribut posees : absentes du registre -> AVERTISSEMENT
       « extension de registre requise » ; domaine ne couvrant pas les
       types cibles -> AVERTISSEMENT « domaine du registre a etendre » ;
  C09  CREATE_ENTITY : aucun applicateur du depot ne le consomme (balayage
       dynamique de scripts/make_*.py) -> AVERTISSEMENT structurel ;
       BLOQUANT si un entityId est preassigne (l'applicateur futur assigne) ;
  C10  collisions de noms (normalisation casse/espaces) : SET_NAME vers un
       nom deja porte -> BLOQUANT ; CREATE_ENTITY homonyme -> AVERTISSEMENT ;
       collisions entre ops du lot detectees aussi ;
  C11  duplicateOf : cible existante ; AUCUNE chaine A->B->C (ni dans le
       lot, ni via un duplicateOf deja porte par la cible dans le graphe) ;
       au plus UN duplicateOf par entite (invariant de verif_doublons.py) ;
  C12  cross-patch : une meme entite visee par plusieurs patchs du lot
       (retypee ET marquee doublon, par exemple) -> AVERTISSEMENT detaille ;
  C13  ops relationnelles (ADD_RELATION) : extremites existantes et
       distinctes, relationTypeId connu, relationTypeName coherent avec lui,
       et surtout AUCUNE relation deja portee par le graphe ni proposee deux
       fois dans le lot -> BLOQUANT ; aucun applicateur ne consommant
       ADD_RELATION -> AVERTISSEMENT structurel.

CODES DE SORTIE : 0 = aucun BLOQUANT ; 1 = au moins un BLOQUANT sur le lot ;
2 = erreur d'invocation (graphe/registre illisible, --patch introuvable).
Un patch candidat illisible n'est PAS une erreur d'invocation : c'est un
BLOQUANT de son patch (C01), et le preflight continue avec les autres.

Usage:
    python3 scripts/preflight_candidate_patches.py
    python3 scripts/preflight_candidate_patches.py --patch patch_candidate_x.json
    python3 scripts/preflight_candidate_patches.py --report-json /tmp/rapport.json
"""
import argparse
import collections
import glob
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from grc20_commun import (REPO, applicateurs_par_op,  # noqa: E402
                          graphe_le_plus_recent, graphes_tries)

CODE_BLOQUANT, CODE_INVOCATION = 1, 2
OK, AVERT, BLOQ = 'OK', 'AVERTISSEMENT', 'BLOQUANT'

MOTIF_CANDIDAT = 'patch_candidate_*.json'
REGISTRE_DEFAUT = 'grc20-properties-registry-v1.json'
# Prefixe obligatoire de la policy d'un candidat (tirets cadratins U+2014).
PREFIXE_POLICY = 'CANDIDATE — NOT APPLIED — AUTHOR ARBITRATION REQUIRED'
META_REQUIS = ('policy', 'source_graph', 'patch_id', 'description')
OPS_SUR_ENTITE = ('SET_NAME', 'SET_TYPES', 'SET_ATTRIBUTE', 'DELETE_ATTRIBUTE')
# Ops RELATIONNELLES (C13). Elles ne visent pas une entite mais un COUPLE, et
# n'ont donc pas d'`entityId` : les controles bases sur ce champ les ignorent,
# d'ou un controle dedie. La forme reconnue est le dialecte C etendu — type de
# relation par ID, double d'un nom declare et verifie. Les trois formes
# historiques d'ADD_RELATION donnent le type par NOM, ce qui est ambigu ; ce
# validateur n'en reconnait aucune, et c'est deliberé : la FORME d'un patch
# relationnel est un arbitrage reserve a l'auteur (contrat § 4). Reconnaitre
# ici une forme n'est pas la choisir a sa place — c'est rendre verifiable la
# seule qui ait ete proposee, pour qu'il puisse la juger sur pieces.
OPS_RELATION = ('ADD_RELATION',)
OPS_CONNUES = OPS_SUR_ENTITE + ('CREATE_ENTITY',) + OPS_RELATION
ORDRE_STATUT = {OK: 0, AVERT: 1, BLOQ: 2}


def echec_invocation(msg):
    print(f"ECHEC (invocation) : {msg}", file=sys.stderr)
    sys.exit(CODE_INVOCATION)


def lire_json(chemin, quoi):
    """Charge un JSON requis par l'invocation — echec propre sinon."""
    if not chemin or not os.path.exists(chemin):
        echec_invocation(f"{quoi} introuvable : {chemin}")
    try:
        with open(chemin, encoding='utf-8') as f:
            return json.load(f)
    except (json.JSONDecodeError, OSError, UnicodeDecodeError) as err:
        echec_invocation(f"{quoi} illisible : {err}")


def normalise_nom(s):
    """Normalisation casse/espaces SEULEMENT — les accents sont gardes :
    « Orlean » et « Orléan » restent deux noms distincts, ce n'est pas au
    preflight d'en decider."""
    return ' '.join(str(s or '').lower().split())


def valeur_attribut(op):
    """La valeur TEXT d'une op SET_ATTRIBUTE, ou '' si la forme surprend."""
    v = op.get('value')
    if isinstance(v, dict):
        return str(v.get('value') or '')
    return str(v or '')


class Controles:
    """Accumule les lignes de controle d'un patch, dans l'ordre d'emission."""

    def __init__(self):
        self.lignes = []

    def ajoute(self, code, statut, detail):
        self.lignes.append({'code': code, 'statut': statut, 'detail': detail})

    def resume(self):
        c = collections.Counter(x['statut'] for x in self.lignes)
        return {s: c.get(s, 0) for s in (OK, AVERT, BLOQ)}


def controle_meta(c, patch):
    """C02 + C03 + C04 (partie declaration) : la carte d'identite du patch."""
    meta = patch.get('_meta')
    if not isinstance(meta, dict):
        c.ajoute('C02', BLOQ, "_meta absent : un candidat sans carte "
                              "d'identite est refuse")
        return {}
    absents = sorted(k for k in META_REQUIS if not meta.get(k))
    if absents:
        c.ajoute('C02', BLOQ, f"_meta incomplet, champ(s) manquant(s) : "
                              f"{', '.join(absents)}")
    else:
        c.ajoute('C02', OK, "_meta complet (policy, source_graph, patch_id, "
                            "description)")
    mal_types = []
    for cle in ('patch_id', 'description', 'source_graph', 'generated'):
        if cle in meta and not isinstance(meta[cle], str):
            mal_types.append(f"{cle} (chaine attendue)")
    for cle in ('op_count', 'candidate_count', 'skipped_count',
                'entities_touched', 'members_marked', 'families_marked'):
        if cle in meta and not isinstance(meta[cle], int):
            mal_types.append(f"{cle} (entier attendu)")
    if 'skipped' in meta and not isinstance(meta['skipped'], list):
        mal_types.append("skipped (liste attendue)")
    if mal_types:
        c.ajoute('C02', BLOQ, "champ(s) _meta mal type(s) : "
                              + ', '.join(mal_types))
    policy = meta.get('policy')
    if not isinstance(policy, str) or not policy.startswith(PREFIXE_POLICY):
        c.ajoute('C03', BLOQ, "policy ne commence pas par le marquage "
                              f"obligatoire « {PREFIXE_POLICY} » : patch mal "
                              "marque, refuse")
    else:
        c.ajoute('C03', OK, "policy correctement marquee CANDIDATE / NOT "
                            "APPLIED / ARBITRATION REQUIRED")
    return meta


def controle_source_graph(c, meta, graphes_repo, plus_recent):
    """C04 : le patch declare contre quel etat du graphe il a ete construit."""
    declare = meta.get('source_graph')
    if not declare:
        return  # deja bloque par C02
    if declare not in graphes_repo:
        c.ajoute('C04', BLOQ, f"source_graph « {declare} » ne nomme aucun "
                              "graphe present dans le depot")
    elif declare != plus_recent:
        c.ajoute('C04', AVERT, f"source_graph « {declare} » n'est pas le "
                               f"graphe le plus recent ({plus_recent}) : "
                               "patch depose contre un etat anterieur")
    else:
        c.ajoute('C04', OK, f"source_graph = {declare} (graphe le plus recent)")


def controle_comptes(c, meta, ops):
    """C05 : TOUS les comptes declares dans _meta contre les contenus reels.

    Chaque cle presente est verifiee (pas seulement la premiere trouvee :
    un patch declarant op_count juste et candidate_count faux passait).
    Les comptes derives declares par les patchs existants sont recomptes
    aussi : entities_touched, members_marked, families_marked."""
    reels = {
        'op_count': len(ops),
        'candidate_count': len(ops),
        'skipped_count': len(meta.get('skipped') or []),
        'entities_touched': len({op.get('entityId') for op in ops
                                 if op.get('entityId')}),
        'members_marked': len({op.get('entityId') for op in ops
                               if op.get('type') == 'SET_ATTRIBUTE'
                               and op.get('attributeId') == 'duplicateOf'}),
        'families_marked': len({(op.get('value') or {}).get('value')
                                for op in ops
                                if op.get('type') == 'SET_ATTRIBUTE'
                                and op.get('attributeId') == 'duplicateOf'}),
    }
    aucun_compte_ops = True
    for cle in sorted(reels):
        if cle not in meta:
            continue
        if cle in ('op_count', 'candidate_count'):
            aucun_compte_ops = False
        if meta[cle] != reels[cle]:
            c.ajoute('C05', BLOQ, f"{cle} declare {meta[cle]}, "
                                  f"contenu reel {reels[cle]}")
        else:
            c.ajoute('C05', OK, f"{cle} = {meta[cle]} = contenu reel")
    if aucun_compte_ops:
        c.ajoute('C05', AVERT, "aucun compte d'ops declare "
                               "(ni op_count ni candidate_count)")


def controle_forme_ops(c, ops):
    """C06 (forme) : chaque op porte des champs correctement types.

    Verifie AVANT les controles de fond, pour qu'un champ mal type soit un
    BLOQUANT lisible plutot qu'un comportement indefini. La representation
    typee des attributs est celle du contrat : {type, value[, options]}."""
    problemes = []
    for i, op in enumerate(ops):
        t = op.get('type')
        if t is not None and not isinstance(t, str):
            problemes.append(f"op[{i}] : type n'est pas une chaine")
            continue
        eid = op.get('entityId')
        if eid is not None and not isinstance(eid, str):
            problemes.append(f"op[{i}] {t} : entityId n'est pas une chaine")
        if t == 'SET_NAME' and not (isinstance(op.get('value'), str)
                                    and op.get('value')):
            problemes.append(f"op[{i}] SET_NAME : value (chaine non vide) "
                             "requise")
        if t == 'SET_TYPES':
            v = op.get('value')
            if not isinstance(v, list) or not v or any(
                    not isinstance(x, str) for x in v):
                problemes.append(f"op[{i}] SET_TYPES : value (liste non "
                                 "vide de chaines) requise")
        if t in ('SET_ATTRIBUTE', 'DELETE_ATTRIBUTE') and not isinstance(
                op.get('attributeId'), str):
            problemes.append(f"op[{i}] {t} : attributeId (chaine) requis")
        if t == 'SET_ATTRIBUTE':
            v = op.get('value')
            if not isinstance(v, dict) or 'type' not in v or 'value' not in v:
                problemes.append(f"op[{i}] SET_ATTRIBUTE : value doit etre "
                                 "un objet {type, value[, options]}")
        if t in OPS_RELATION:
            for champ in ('from', 'to', 'relationTypeId'):
                if not (isinstance(op.get(champ), str) and op.get(champ)):
                    problemes.append(f"op[{i}] {t} : {champ} (chaine non "
                                     "vide) requis")
            if 'relationTypeName' in op and not isinstance(
                    op['relationTypeName'], str):
                problemes.append(f"op[{i}] {t} : relationTypeName doit etre "
                                 "une chaine")
        if t == 'CREATE_ENTITY':
            if not (isinstance(op.get('name'), str) and op.get('name')):
                problemes.append(f"op[{i}] CREATE_ENTITY : name (chaine non "
                                 "vide) requis")
            ty = op.get('types')
            if not isinstance(ty, list) or not ty or any(
                    not isinstance(x, str) for x in ty):
                problemes.append(f"op[{i}] CREATE_ENTITY : types (liste non "
                                 "vide de chaines) requise")
            attrs = op.get('attributes')
            if attrs is not None and (
                    not isinstance(attrs, dict) or any(
                        not isinstance(v2, dict) or 'type' not in v2
                        or 'value' not in v2 for v2 in attrs.values())):
                problemes.append(f"op[{i}] CREATE_ENTITY : attributes doit "
                                 "associer chaque cle a un objet "
                                 "{type, value[, options]}")
    for m in problemes[:12]:
        c.ajoute('C06', BLOQ, m)
    if len(problemes) > 12:
        c.ajoute('C06', BLOQ, f"... et {len(problemes) - 12} autre(s) "
                              "probleme(s) de forme")
    if not problemes:
        c.ajoute('C06', OK, "forme des ops valide (champs types par "
                            "operation)")


def controle_entites(c, ops, entites):
    """C06 : toute op visant une entite existante doit la trouver."""
    inconnues, malformees, vues = [], [], 0
    for i, op in enumerate(ops):
        if op.get('type') not in OPS_SUR_ENTITE:
            continue
        vues += 1
        eid = op.get('entityId')
        if not eid:
            malformees.append(f"op[{i}] {op.get('type')} sans entityId")
        elif eid not in entites:
            inconnues.append(f"op[{i}] {op.get('type')} -> {eid}")
    for m in malformees:
        c.ajoute('C06', BLOQ, m)
    if inconnues:
        c.ajoute('C06', BLOQ, f"{len(inconnues)} op(s) visent une entite "
                              f"absente du graphe : "
                              f"{' ; '.join(inconnues[:6])}")
    elif not malformees:
        c.ajoute('C06', OK, f"toutes les entites ciblees existent "
                            f"({vues} op(s) verifiees)")
    types_hors_perimetre = sorted(
        {op.get('type') or '(absent)' for op in ops
         if op.get('type') not in OPS_CONNUES})
    if types_hors_perimetre:
        # BLOQUANT, pas avertissement : un candidat dont des ops echappent
        # au perimetre obtiendrait sinon le meme « 0 BLOQUANT » que les
        # patchs entierement verifies — etendre le validateur ou corriger
        # le patch avant de re-passer le preflight.
        c.ajoute('C06', BLOQ, "type(s) d'op hors perimetre du preflight, "
                              f"INVERIFIABLE(S) : "
                              f"{', '.join(types_hors_perimetre)} — "
                              "etendre le validateur ou corriger le patch")


def controle_relations(c, ops, entites, nom_relation, relations_graphe,
                       relations_du_lot, nom_patch, applicateurs):
    """C13 : les ops relationnelles — extremites, type, et DOUBLONS.

    Le controle qui compte est le dernier. Une relation deja portee par le
    graphe, reposee par un patch, est un doublon silencieux : rien ne la
    signale a l'application, et le graphe se met a porter deux fois le meme
    fait. C'est la variante relationnelle de l'incident d'homonymie qui a fait
    echouer make_v110, et elle est plus discrete parce qu'aucun nom ne
    collisionne. On verifie aussi le lot contre lui-meme : deux patchs
    candidats peuvent proposer la meme relation sans se voir."""
    rel_ops = [(i, op) for i, op in enumerate(ops)
               if op.get('type') in OPS_RELATION]
    if not rel_ops:
        c.ajoute('C13', OK, "aucune op relationnelle")
        return
    problemes, verifiees = [], 0
    for i, op in rel_ops:
        depart, arrivee = op.get('from'), op.get('to')
        tid, tnom = op.get('relationTypeId'), op.get('relationTypeName')
        if not (depart and arrivee and tid):
            continue                      # deja BLOQUANT en controle de forme
        verifiees += 1
        for role, eid in (('from', depart), ('to', arrivee)):
            if eid not in entites:
                problemes.append((BLOQ, f"op[{i}] {role} {eid} : entite "
                                        "absente du graphe"))
        if depart == arrivee:
            problemes.append((BLOQ, f"op[{i}] relation de {depart} vers "
                                    "lui-meme"))
        if tid not in nom_relation:
            problemes.append((BLOQ, f"op[{i}] relationTypeId {tid} inconnu "
                                    "du graphe"))
        elif tnom and nom_relation[tid] != tnom:
            problemes.append((BLOQ, f"op[{i}] relationTypeName « {tnom} » "
                                    f"!= nom reel « {nom_relation[tid]} » "
                                    "pour cet id"))
        if (depart, arrivee, tid) in relations_graphe:
            problemes.append((BLOQ, f"op[{i}] la relation existe DEJA dans le "
                                    f"graphe ({depart[:8]} -{tnom or tid}-> "
                                    f"{arrivee[:8]}) : la reposer creerait un "
                                    "doublon silencieux"))
        ailleurs = [p for (p, j) in relations_du_lot.get(
            (depart, arrivee, tid), []) if not (p == nom_patch and j == i)]
        if ailleurs:
            problemes.append((BLOQ, f"op[{i}] la meme relation est proposee "
                                    f"par {', '.join(sorted(set(ailleurs)))}"))
    for statut, detail in sorted(set(problemes),
                                 key=lambda x: (ORDRE_STATUT[x[0]], x[1])):
        c.ajoute('C13', statut, detail)
    if not problemes:
        c.ajoute('C13', OK, f"{verifiees} op(s) relationnelle(s) : extremites "
                            "existantes, type connu et nomme juste, aucune "
                            "relation deja presente ni proposee deux fois")
    # Non bloquant mais structurant : personne ne sait appliquer ces ops.
    if not applicateurs:
        c.ajoute('C13', AVERT, f"{len(rel_ops)} op(s) ADD_RELATION : non "
                               "applicable en l'etat, applicateur dedie "
                               "requis (aucun scripts/make_*.py ne consomme "
                               "ADD_RELATION)")


def controle_types(c, ops, nom_type):
    """C07 : ids de types connus, et coherence id<->nom si typeNames."""
    inconnus, divergences, verifies = [], [], 0
    for i, op in enumerate(ops):
        if op.get('type') == 'SET_TYPES':
            ids = op.get('value') or []
        elif op.get('type') == 'CREATE_ENTITY':
            ids = op.get('types') or []
        else:
            continue
        verifies += 1
        for t in ids:
            if t not in nom_type:
                inconnus.append(f"op[{i}] type inconnu {t}")
        noms_declares = op.get('typeNames')
        if noms_declares:
            noms_reels = [nom_type.get(t, t) for t in ids]
            if noms_reels != list(noms_declares):
                divergences.append(f"op[{i}] typeNames {noms_declares} != "
                                   f"noms reels {noms_reels}")
    if inconnus:
        c.ajoute('C07', BLOQ, f"{len(inconnus)} id(s) de type absents du "
                              f"graphe : {' ; '.join(inconnus[:6])}")
    if divergences:
        c.ajoute('C07', AVERT, f"typeNames divergents des ids : "
                               f"{' ; '.join(divergences[:6])}")
    if not inconnus and not divergences:
        c.ajoute('C07', OK, f"ids de types tous connus du graphe "
                            f"({verifies} op(s) porteuses de types)")


def types_cibles_de(op, entites, nom_type):
    """Les NOMS de types de l'entite que l'op vise (ou creerait)."""
    if op.get('type') == 'CREATE_ENTITY':
        ids = op.get('types') or []
    else:
        e = entites.get(op.get('entityId')) or {}
        ids = e.get('types') or []
    return sorted(nom_type.get(t, t) for t in ids)


def controle_registre(c, ops, registre, entites, nom_type):
    """C08 : les cles d'attribut posees, face au registre des proprietes.

    Un candidat a le DROIT de poser une cle hors registre ou hors domaine —
    mais l'application exigerait d'abord d'etendre le registre (invariant de
    CI depuis v110) : AVERTISSEMENT, jamais BLOQUANT ici."""
    hors_registre = collections.defaultdict(int)
    hors_domaine = {}  # cle -> (nb ops, domaine, types cibles rencontres)
    absents_suppression = []
    poses = 0
    for i, op in enumerate(ops):
        if op.get('type') == 'SET_ATTRIBUTE':
            cles = [op.get('attributeId')]
        elif op.get('type') == 'CREATE_ENTITY':
            cles = sorted(op.get('attributes') or {})
        elif op.get('type') == 'DELETE_ATTRIBUTE':
            e = entites.get(op.get('entityId')) or {}
            if op.get('attributeId') not in (e.get('attributes') or {}):
                absents_suppression.append(
                    f"op[{i}] supprime {op.get('attributeId')} absent de "
                    f"{op.get('entityId')}")
            continue
        else:
            continue
        for cle in cles:
            if not cle:
                continue
            poses += 1
            entree = registre.get(cle)
            if entree is None:
                hors_registre[cle] += 1
                continue
            domaine = entree.get('domain') or []
            # Couverture COMPLETE exigee : une intersection non vide ne
            # suffit pas — chaque type cible doit etre au domaine, sinon
            # le registre resterait partiellement menteur a l'application.
            cibles = types_cibles_de(op, entites, nom_type)
            non_couverts = set(cibles) - set(domaine)
            if domaine and non_couverts:
                n, _, vus = hors_domaine.get(cle, (0, domaine, set()))
                vus = set(vus) | non_couverts
                hors_domaine[cle] = (n + 1, domaine, vus)
    for cle in sorted(hors_registre):
        c.ajoute('C08', AVERT, f"cle « {cle} » absente du registre : "
                               "extension de registre requise avant "
                               f"application ({hors_registre[cle]} op(s))")
    for cle in sorted(hors_domaine):
        n, domaine, vus = hors_domaine[cle]
        c.ajoute('C08', AVERT, f"cle « {cle} » : domaine du registre a "
                               f"etendre — domaine actuel "
                               f"[{', '.join(sorted(domaine))}] ne couvre "
                               f"pas les types cibles "
                               f"[{', '.join(sorted(vus))}] ({n} op(s))")
    for m in absents_suppression:
        c.ajoute('C08', AVERT, m)
    if not hors_registre and not hors_domaine and not absents_suppression:
        c.ajoute('C08', OK, f"cles d'attribut toutes au registre et dans "
                            f"leur domaine ({poses} pose(s))")


def controle_create_entity(c, ops, applicateurs):
    """C09 : CREATE_ENTITY est descriptif — aucun applicateur du depot ne le
    consomme, et un entityId preassigne est interdit par principe."""
    creations = [i for i, op in enumerate(ops)
                 if op.get('type') == 'CREATE_ENTITY']
    if not creations:
        c.ajoute('C09', OK, "aucune op CREATE_ENTITY")
        return
    preassignes = [f"op[{i}] entityId={ops[i]['entityId']}"
                   for i in creations if ops[i].get('entityId')]
    if preassignes:
        c.ajoute('C09', BLOQ, f"CREATE_ENTITY avec entityId preassigne "
                              f"(interdit : l'applicateur futur les "
                              f"assignera) : {' ; '.join(preassignes[:6])}")
    if applicateurs:
        c.ajoute('C09', AVERT, f"{len(creations)} CREATE_ENTITY — "
                               f"applicateur(s) potentiels detectes : "
                               f"{', '.join(applicateurs)} (verifier la "
                               "compatibilite du dialecte)")
    else:
        c.ajoute('C09', AVERT, f"{len(creations)} CREATE_ENTITY : non "
                               "applicable en l'etat, applicateur dedie "
                               "requis (aucun scripts/make_*.py ne consomme "
                               "CREATE_ENTITY)")


def controle_collisions(c, ops, noms_graphe, noms_du_lot, nom_patch):
    """C10 : collisions de noms — contre le graphe, et entre ops du lot.

    Un SET_NAME qui cree une homonymie exacte est BLOQUANT : c'est tres
    exactement le motif d'echec de make_v110 (controle d'homonymie Person).
    Un CREATE_ENTITY homonyme est un AVERTISSEMENT : l'arbitrage peut vouloir
    ce noeud, mais il faut le savoir."""
    problemes = []
    for i, op in enumerate(ops):
        if op.get('type') == 'SET_NAME':
            nom, statut, quoi = op.get('value'), BLOQ, 'SET_NAME'
        elif op.get('type') == 'CREATE_ENTITY':
            nom, statut, quoi = op.get('name'), AVERT, 'CREATE_ENTITY'
        else:
            continue
        n = normalise_nom(nom)
        if not n:
            continue
        porteurs = [x for x in noms_graphe.get(n, [])
                    if x != op.get('entityId')]
        if porteurs:
            problemes.append((statut, f"op[{i}] {quoi} « {nom} » : nom deja "
                                      f"porte dans le graphe par "
                                      f"{', '.join(sorted(porteurs)[:3])}"))
        autres = [(p, j, q) for (p, j, q) in noms_du_lot.get(n, [])
                  if not (p == nom_patch and j == i)]
        if autres:
            grave = BLOQ if (quoi == 'SET_NAME'
                             or any(q == 'SET_NAME' for _, _, q in autres)) \
                else AVERT
            ou = ' ; '.join(f"{p} op[{j}] ({q})" for p, j, q in autres[:4])
            problemes.append((grave, f"op[{i}] {quoi} « {nom} » : meme nom "
                                     f"pose ailleurs dans le lot par {ou}"))
    for statut, detail in sorted(problemes,
                                 key=lambda x: (ORDRE_STATUT[x[0]], x[1])):
        c.ajoute('C10', statut, detail)
    if not problemes:
        c.ajoute('C10', OK, "aucune collision de nom (graphe et lot)")


def controle_duplicate_of(c, ops, entites, dup_du_lot):
    """C11 : les invariants du marquage duplicateOf.

    Une entite porte AU PLUS UN duplicateOf, et aucun canonique n'est
    lui-meme un doublon — ni dans le lot, ni dans le graphe. La chaine
    A->B->C est l'incident historique « Mining pools » (C4) du depot."""
    dup_ops = [(i, op) for i, op in enumerate(ops)
               if op.get('type') == 'SET_ATTRIBUTE'
               and op.get('attributeId') == 'duplicateOf']
    if not dup_ops:
        c.ajoute('C11', OK, "aucune op duplicateOf")
        return
    problemes = []
    par_entite = collections.defaultdict(list)
    for i, op in dup_ops:
        par_entite[op.get('entityId')].append((i, valeur_attribut(op)))
    for eid in sorted(par_entite):
        if len(par_entite[eid]) > 1:
            ou = ', '.join(f"op[{i}] -> {cible}"
                           for i, cible in par_entite[eid])
            problemes.append(f"entite {eid} recoit {len(par_entite[eid])} "
                             f"duplicateOf (au plus UN par entite, invariant "
                             f"de verif_doublons.py) : {ou}")
    for i, op in dup_ops:
        eid, cible = op.get('entityId'), valeur_attribut(op)
        if cible not in entites:
            problemes.append(f"op[{i}] duplicateOf -> cible {cible} absente "
                             "du graphe")
            continue
        if cible == eid:
            problemes.append(f"op[{i}] duplicateOf de {eid} vers lui-meme")
            continue
        if cible in dup_du_lot:
            suite = ', '.join(sorted(dup_du_lot[cible]))
            problemes.append(f"op[{i}] chaine de doublons : {eid} -> {cible} "
                             f"alors que {cible} est lui-meme marque doublon "
                             f"dans le lot (-> {suite}) — incident type "
                             "« Mining pools » C4")
        deja = (entites[cible].get('attributes') or {}).get('duplicateOf')
        if deja:
            v = deja.get('value') if isinstance(deja, dict) else deja
            problemes.append(f"op[{i}] chaine de doublons : {eid} -> {cible} "
                             f"alors que {cible} porte deja duplicateOf -> "
                             f"{v} dans le graphe")
    for detail in sorted(set(problemes)):
        c.ajoute('C11', BLOQ, detail)
    if not problemes:
        c.ajoute('C11', OK, f"{len(dup_ops)} duplicateOf : cibles "
                            "existantes, aucune chaine, un seul marquage "
                            "par entite")


def visees_par(ops):
    """-> {entity_id: roles} des entites qu'un patch vise (cible d'op) ou
    designe comme canonique (cible d'un duplicateOf)."""
    roles = collections.defaultdict(set)
    for op in ops:
        if op.get('type') in OPS_SUR_ENTITE and op.get('entityId'):
            roles[op['entityId']].add(op['type'])
        if op.get('type') in OPS_RELATION:
            # Une relation vise DEUX entites. Les inscrire toutes deux fait
            # apparaitre en C12 le cas « Favier retype par un patch ET relie
            # par un autre » — utile, et invisible autrement.
            for role, cle in (('depart de relation', 'from'),
                              ('arrivee de relation', 'to')):
                if op.get(cle):
                    roles[op[cle]].add(role)
        if (op.get('type') == 'SET_ATTRIBUTE'
                and op.get('attributeId') == 'duplicateOf'):
            cible = valeur_attribut(op)
            if cible:
                roles[cible].add('canonique duplicateOf')
    return roles


def main(argv=None):
    p = argparse.ArgumentParser(
        description="Preflight des patchs candidats (patch_candidate_*.json) "
                    "contre le graphe courant et le registre des proprietes. "
                    "Lecture seule, sortie deterministe. Codes de sortie : "
                    "0 = aucun BLOQUANT, 1 = au moins un BLOQUANT, "
                    "2 = erreur d'invocation.")
    p.add_argument('--patch', action='append', default=None, metavar='FICHIER',
                   help="patch candidat a preflighter (repetable ; defaut : "
                        "tous les patch_candidate_*.json de la racine du "
                        "depot, en ordre trie)")
    p.add_argument('--graph', default=None,
                   help="graphe de reference (defaut : le plus recent, motif "
                        "grc20-these-mael-rolland-v(\\d+).json)")
    p.add_argument('--registry',
                   default=os.path.join(REPO, REGISTRE_DEFAUT),
                   help="registre des proprietes (defaut : %(default)s)")
    p.add_argument('--report-json', default=None, metavar='CHEMIN',
                   help="ecrit en plus un rapport JSON deterministe "
                        "{patch: {controles: [...], resume: {...}}}")
    args = p.parse_args(argv)

    chemin_graphe = args.graph or graphe_le_plus_recent()
    graphe = lire_json(chemin_graphe, 'graphe de reference')
    if not isinstance(graphe.get('entities'), list):
        echec_invocation(f"graphe sans liste d'entites : {chemin_graphe}")
    brut_registre = lire_json(args.registry, 'registre des proprietes')
    entrees = brut_registre.get('entries') or brut_registre.get('properties')
    if not entrees:
        echec_invocation(f"registre sans entrees exploitables : "
                         f"{args.registry}")
    registre = {x['key']: x for x in entrees if x.get('key')}

    entites = {e['id']: e for e in graphe['entities']}
    nom_type = {t['id']: t.get('name') or t['id']
                for t in graphe.get('types', [])}
    noms_graphe = collections.defaultdict(list)
    for e in graphe['entities']:
        noms_graphe[normalise_nom(e.get('name'))].append(e['id'])
    nom_relation = {t['id']: t.get('name') or t['id']
                    for t in graphe.get('relation_types', [])}
    relations_graphe = {(r['from'], r['to'], r['type'])
                        for r in graphe.get('relations', [])}
    graphes_repo = {os.path.basename(x) for x in graphes_tries()}
    plus_recent = os.path.basename(graphe_le_plus_recent() or '')
    # UN seul balayage pour tous les types, partage avec la file de patchs.
    applicateurs = applicateurs_par_op()

    if args.patch:
        chemins = [os.path.abspath(x) for x in args.patch]
        for x in chemins:
            if not os.path.exists(x):
                echec_invocation(f"patch introuvable : {x}")
        chemins.sort(key=os.path.basename)
    else:
        chemins = sorted(glob.glob(os.path.join(REPO, MOTIF_CANDIDAT)),
                         key=os.path.basename)
        if not chemins:
            echec_invocation(f"aucun {MOTIF_CANDIDAT} a la racine du depot "
                             "(et aucun --patch fourni)")

    # ---------- premiere passe : lecture, pour les controles de lot ----------
    patchs = []          # (nom, donnees | None, erreur de parse | None)
    for chemin in chemins:
        nom = os.path.basename(chemin)
        try:
            with open(chemin, encoding='utf-8') as f:
                donnees = json.load(f)
            # Structure minimale AVANT tout controle : un objet, et ops en
            # liste — sinon la suite exploserait en traceback au lieu d'un
            # BLOQUANT propre, et les autres patchs du lot seraient perdus.
            if not isinstance(donnees, dict) or (
                    'ops' in donnees and (
                        not isinstance(donnees['ops'], list)
                        or any(not isinstance(o, dict)
                               for o in donnees['ops']))):
                patchs.append((nom, None, "structure inattendue : le patch "
                                          "doit etre un objet JSON et ops "
                                          "une liste d'objets"))
            else:
                patchs.append((nom, donnees, None))
        except (json.JSONDecodeError, OSError, UnicodeDecodeError) as err:
            patchs.append((nom, None, str(err)))

    noms_du_lot = collections.defaultdict(list)   # nom normalise -> ops du lot
    rel_du_lot = collections.defaultdict(list)    # (from,to,type) -> ops du lot
    dup_du_lot = collections.defaultdict(set)     # entite -> cibles duplicateOf
    visees_lot = collections.defaultdict(dict)    # entite -> {patch: roles}
    for nom, donnees, _ in patchs:
        if donnees is None:
            continue
        ops = donnees.get('ops') or []
        for i, op in enumerate(ops):
            if op.get('type') == 'SET_NAME' and op.get('value'):
                noms_du_lot[normalise_nom(op['value'])].append(
                    (nom, i, 'SET_NAME'))
            if op.get('type') == 'CREATE_ENTITY' and op.get('name'):
                noms_du_lot[normalise_nom(op['name'])].append(
                    (nom, i, 'CREATE_ENTITY'))
            if (op.get('type') in OPS_RELATION and op.get('from')
                    and op.get('to') and op.get('relationTypeId')):
                rel_du_lot[(op['from'], op['to'],
                            op['relationTypeId'])].append((nom, i))
            if (op.get('type') == 'SET_ATTRIBUTE'
                    and op.get('attributeId') == 'duplicateOf'
                    and op.get('entityId')):
                dup_du_lot[op['entityId']].add(valeur_attribut(op))
        for eid, roles in visees_par(ops).items():
            visees_lot[eid][nom] = roles

    # ---------- seconde passe : les 13 controles, patch par patch ----------
    rapport = {}
    for nom, donnees, erreur in patchs:
        c = Controles()
        rapport[nom] = c
        if donnees is None:
            c.ajoute('C01', BLOQ, f"JSON illisible : {erreur}")
            continue
        c.ajoute('C01', OK, 'json valide')
        ops = donnees.get('ops') or []
        meta = controle_meta(c, donnees)
        controle_source_graph(c, meta, graphes_repo, plus_recent)
        controle_forme_ops(c, ops)
        controle_comptes(c, meta, ops)
        controle_entites(c, ops, entites)
        controle_types(c, ops, nom_type)
        controle_registre(c, ops, registre, entites, nom_type)
        controle_create_entity(c, ops, applicateurs['CREATE_ENTITY'])
        controle_collisions(c, ops, noms_graphe, noms_du_lot, nom)
        controle_duplicate_of(c, ops, entites, dup_du_lot)
        controle_relations(c, ops, entites, nom_relation, relations_graphe,
                           rel_du_lot, nom, applicateurs['ADD_RELATION'])
        partages = sorted(eid for eid, par in visees_lot.items()
                          if nom in par and len(par) > 1)
        if partages:
            for eid in partages:
                autres = ' ; '.join(
                    f"{autre} ({', '.join(sorted(roles))})"
                    for autre, roles in sorted(visees_lot[eid].items())
                    if autre != nom)
                ici = ', '.join(sorted(visees_lot[eid][nom]))
                nom_e = (entites.get(eid) or {}).get('name', '?')
                c.ajoute('C12', AVERT, f"entite {eid} « {nom_e} » visee ici "
                                       f"({ici}) ET par {autres}")
        else:
            c.ajoute('C12', OK, "aucune entite partagee avec un autre patch "
                                "du lot")

    # ---------- restitution ----------
    print(f"graphe   : {os.path.relpath(chemin_graphe, REPO)}")
    print(f"registre : {os.path.relpath(args.registry, REPO)}")
    print(f"patchs   : {len(patchs)}")
    total = collections.Counter()
    for nom in sorted(rapport):
        c = rapport[nom]
        print(f"\n=== {nom} ===")
        for ligne in c.lignes:
            print(f"  {ligne['code']}  {ligne['statut']:13s} "
                  f"{ligne['detail']}")
        r = c.resume()
        total.update(r)
        print(f"  resume : {r[OK]} OK / {r[AVERT]} AVERTISSEMENT / "
              f"{r[BLOQ]} BLOQUANT")

    print("\n=== RESUME GLOBAL ===")
    print(f"  {total[OK]} OK / {total[AVERT]} AVERTISSEMENT / "
          f"{total[BLOQ]} BLOQUANT")

    if args.report_json:
        sortie = {nom: {'controles': c.lignes, 'resume': c.resume()}
                  for nom, c in rapport.items()}
        dossier = os.path.dirname(os.path.abspath(args.report_json))
        os.makedirs(dossier, exist_ok=True)
        with open(args.report_json, 'w', encoding='utf-8') as f:
            json.dump(sortie, f, ensure_ascii=False, indent=1, sort_keys=True)
            f.write('\n')
        print(f"  rapport json : {args.report_json}")

    if total[BLOQ]:
        print(f"ECHEC (donnees) : {total[BLOQ]} controle(s) BLOQUANT(s) sur "
              "le lot — arbitrage ou correction requis avant tout "
              "applicateur.", file=sys.stderr)
        return CODE_BLOQUANT
    return 0


if __name__ == '__main__':
    sys.exit(main())
