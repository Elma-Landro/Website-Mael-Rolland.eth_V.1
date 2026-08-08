#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Applique patch_candidate_section_page_start_v1.json et produit v111.

CE QUE CE SCRIPT FAIT, ET RIEN D'AUTRE. Il ecrit 16 valeurs de l'attribut
`page_start` sur 16 noeuds de section qui en portaient DEJA une, et qui la
portaient FAUSSE. Il ne cree aucune entite, aucune relation, aucune
SourceQuote ; il ne renomme ni ne retype rien ; il ne remplit aucun
`page_start` absent — les 49 entrees de `_meta.skipped` du patch restent
exactement dans l'etat ou v110 les laisse. Toute op qui n'est pas un
`SET_ATTRIBUTE` sur la cle `page_start` est refusee, pas ignoree.

POURQUOI CES 16 VALEURS SONT FAUSSES (cause etablie par le chantier, PR #116,
docs/audits/grc20-section-page-start-repair-lab-v1.md) : aucun `page_start`
n'a jamais ete modifie entre v96 et v110 ; les renumerotations v100 et v106
ont change la SECTION qu'une cle designe, sans deplacer la valeur, restee
collee au NOEUD. Chacune des 16 valeurs fausses est exactement la page
imprimee de la cle que ce meme noeud portait en v96.

LA VALEUR ANCIENNE EST VERIFIEE, PAS SUPPOSEE. Avant d'ecrire, le script
exige la concordance de TROIS sources independantes pour chaque op :
  1. la valeur que le graphe source porte reellement ;
  2. la valeur ancienne inscrite dans le `_comment` de l'op
     (« page_start 202 -> 190 ») ;
  3. la colonne `page_start_actuel` du CSV de diagnostic, dont la colonne
     `page_imprimee_verifiee` doit par ailleurs egaler la valeur cible.
Si le graphe a derive depuis la redaction du patch, les trois ne concordent
plus et le script refuse d'ecrire. C'est le controle qui empeche de rejouer
un patch sur un graphe qui n'est plus celui qu'il decrit.

LE CONTROLE QUI COMPTE EST EXHAUSTIF. Les verifications d'apres ne se
contentent pas de recompter les entites : le graphe resultat est compare au
graphe source attribut par attribut, entite par entite, relation par
relation. Le script n'ecrit que si le diff complet vaut EXACTEMENT
16 valeurs de `page_start` changees — aucune cle creee, aucune cle
supprimee, aucun nom, aucun type, aucune relation, aucune op touchee.

Usage:
    python3 scripts/make_v111_apply_section_page_start_patch.py --dry-run
    python3 scripts/make_v111_apply_section_page_start_patch.py
"""
import argparse
import collections
import csv
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from grc20_commun import REPO, TYPES_SECTION  # noqa: E402

CODE_DONNEES, CODE_INVOCATION = 1, 2

CLE = 'page_start'
POLICY_CANDIDAT = 'CANDIDATE — NOT APPLIED — AUTHOR ARBITRATION REQUIRED'
VERSION_CIBLE = 'v111'
OPS_ATTENDUES = 16

# Applicateur a USAGE UNIQUE : le lot est fige ici, pas seulement declare
# par le patch. Un patch retouche entre l'arbitrage et l'application ne
# doit pas passer parce qu'il aurait mis a jour son propre op_count.
IDS_ATTENDUS = frozenset({
    '0420e53c4c8fd12fef6dcee451a50f61',
    '0b521ac19a2f5ee0cdd07d7460ebdfd0',
    '1168d4e0c868c27a81ac371cb6879359',
    '439782308b5dedb9c5da7022bc2b82ef',
    '4ec3224a44f06315d26d3cac111e5efc',
    '515088f012136277d7375fa65d7a3e3f',
    '5a82e90b2cc17baf91baa9102bd48034',
    '7b3312fed875cffb74320f0a579763c7',
    '97eb62676b0052c4ab3652fc2bd15535',
    '9fbdbbc3f81ee08fb89b5c5dfbcd2929',
    'ac859fd14006e379e55373d31090b6c6',
    'd93cb2ceee6dea674fecc4f44d113643',
    'da7e8dda9cacdb8cddfbab73bb6ecd0b',
    'eda05ae2f601e62bf53294a2be373d2a',
    'f34ad8e32d22d905708d07fc6f0e8150',
    'f8a8acbfa05a53c07498346df21f6808',
})
MOTIF_COMMENT = re.compile(r'page_start\s+(\d+)\s*->\s*(\d+)')


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


def lire_csv(chemin, quoi):
    if not os.path.exists(chemin):
        echec(f"{quoi} introuvable : {chemin} — la preuve enregistree fait "
              "partie de la chaine de verification, le script ne s'en passe pas",
              CODE_INVOCATION)
    try:
        with open(chemin, encoding='utf-8') as f:
            return list(csv.DictReader(f, delimiter=';'))
    except OSError as err:
        echec(f"{quoi} illisible : {err}", CODE_INVOCATION)


def entier(valeur):
    """-> int, ou None. Accepte l'entier, la chaine d'entier, et le vide."""
    if valeur is None:
        return None
    if isinstance(valeur, bool):
        return None
    if isinstance(valeur, int):
        return valeur
    texte = str(valeur).strip()
    return int(texte) if re.fullmatch(r'-?\d+', texte) else None


def valeur_attribut(attribut):
    """Le graphe porte {type, value} ; on tolere la valeur nue en lecture."""
    if isinstance(attribut, dict) and 'value' in attribut:
        return attribut.get('value')
    return attribut


def nom_des_types(graphe):
    return {t['id']: t.get('name') or t['id'] for t in graphe['types']}


def diff_attributs(avant, apres):
    """Diff exhaustif entre deux graphes. -> (changes, crees, supprimes, autres).

    `changes`  : [(entityId, cle, valeur_avant, valeur_apres)]
    `crees`    : [(entityId, cle)]   `supprimes` : [(entityId, cle)]
    `autres`   : messages libres sur tout ce qui n'est pas un attribut
                 d'entite (identite, nom, types, relations, ops, types du
                 graphe, espace).
    """
    changes, crees, supprimes, autres = [], [], [], []

    A = {e['id']: e for e in avant['entities']}
    B = {e['id']: e for e in apres['entities']}
    if set(A) != set(B):
        autres.append("jeu d'entites modifie : "
                      f"+{len(set(B) - set(A))} / -{len(set(A) - set(B))}")
    for eid in set(A) & set(B):
        a, b = A[eid], B[eid]
        for champ in set(a) | set(b):
            if champ == 'attributes':
                continue
            if a.get(champ) != b.get(champ):
                autres.append(f"entite {eid[:8]} : champ « {champ} » modifie")
        aa = a.get('attributes') or {}
        ba = b.get('attributes') or {}
        for cle in set(aa) - set(ba):
            supprimes.append((eid, cle))
        for cle in set(ba) - set(aa):
            crees.append((eid, cle))
        for cle in set(aa) & set(ba):
            if aa[cle] != ba[cle]:
                changes.append((eid, cle, aa[cle], ba[cle]))

    RA = {r.get('id'): r for r in avant['relations']}
    RB = {r.get('id'): r for r in apres['relations']}
    if len(avant['relations']) != len(apres['relations']):
        autres.append(f"nombre de relations : {len(avant['relations'])} -> "
                      f"{len(apres['relations'])}")
    if set(RA) != set(RB):
        autres.append("jeu d'identifiants de relations modifie")
    for rid in set(RA) & set(RB):
        if RA[rid] != RB[rid]:
            autres.append(f"relation {str(rid)[:8]} modifiee")

    for champ in ('types', 'relation_types', 'ops', 'space'):
        if avant.get(champ) != apres.get(champ):
            autres.append(f"bloc « {champ} » modifie")
    return changes, crees, supprimes, autres


def main(argv=None):
    p = argparse.ArgumentParser(
        description="v111 = v110 + patch_candidate_section_page_start_v1 "
                    "(16 corrections de `page_start`, rien d'autre).")
    p.add_argument('--source', default=os.path.join(
        REPO, 'grc20-these-mael-rolland-v110.json'))
    p.add_argument('--patch', default=os.path.join(
        REPO, 'patch_candidate_section_page_start_v1.json'))
    p.add_argument('--csv', default=os.path.join(
        REPO, 'docs', 'audits', 'data',
        'section-page-start-diagnostic-v110.csv'),
        help="Preuve enregistree : colonnes `page_start_actuel` et "
             "`page_imprimee_verifiee`, contre-verification independante du "
             "`_comment` de chaque op.")
    p.add_argument('--registre', default=os.path.join(
        REPO, 'grc20-properties-registry-v1.json'))
    p.add_argument('--target', default=os.path.join(
        REPO, 'grc20-these-mael-rolland-v111.json'))
    p.add_argument('--dry-run', action='store_true')
    args = p.parse_args(argv)

    # Deux lectures independantes du meme fichier : l'une est mutee, l'autre
    # reste le temoin d'avant. Un deepcopy ferait le meme travail ; relire
    # garantit en plus que le temoin n'a partage aucun objet avec le mute.
    g = lire(args.source, 'graphe source')
    temoin = lire(args.source, 'graphe source (temoin)')
    patch = lire(args.patch, 'patch candidat')
    registre = lire(args.registre, 'registre des proprietes')
    lignes_csv = lire_csv(args.csv, 'CSV de diagnostic')

    base = os.path.basename(args.source)
    meta = patch.get('_meta') or {}
    if meta.get('source_graph') != base:
        echec(f"le patch declare source_graph={meta.get('source_graph')}, "
              f"incompatible avec {base}", CODE_INVOCATION)
    if not (meta.get('policy') or '').startswith(POLICY_CANDIDAT):
        echec("le patch n'est pas marque CANDIDATE / NOT APPLIED / "
              "ARBITRATION REQUIRED : ce n'est pas le fichier attendu",
              CODE_INVOCATION)

    ops = patch.get('ops') or []
    # Le lot doit etre EXACTEMENT celui qui a ete arbitre : nombre d'ops et
    # jeu d'entites visees, verifies contre les constantes de ce script et
    # non contre ce que le patch declare de lui-meme.
    if len(ops) != OPS_ATTENDUES:
        echec(f"le patch porte {len(ops)} op(s), {OPS_ATTENDUES} attendues : "
              "ce n'est pas le lot arbitre", CODE_INVOCATION)
    vises = [(o or {}).get('entityId') for o in ops]
    if len(set(vises)) != len(vises):
        vus = collections.Counter(vises)
        doubles = sorted(x for x, n in vus.items() if n > 1)
        echec(f"entite(s) visee(s) plus d'une fois : {doubles} — une seule "
              "correction par noeud", CODE_INVOCATION)
    if set(vises) != IDS_ATTENDUS:
        manquants = sorted(IDS_ATTENDUS - set(vises))
        intrus = sorted(set(vises) - IDS_ATTENDUS)
        echec(f"jeu d'entites visees different de celui arbitre — "
              f"manquantes : {[x[:8] for x in manquants]} · "
              f"intruses : {[x[:8] for x in intrus]}", CODE_INVOCATION)
    E = {e['id']: e for e in g['entities']}
    nom_type = nom_des_types(g)
    avant_e, avant_r = len(g['entities']), len(g['relations'])
    csv_par_id = {(ligne.get('entity_id') or '').strip(): ligne
                  for ligne in lignes_csv}
    erreurs = []

    # ---------- validations, op par op ----------
    # Aucune op n'est ignoree : ce qui n'est pas exactement un SET_ATTRIBUTE
    # sur `page_start`, vers une entite vivante, fait echouer le script.
    plan = []          # [(entityId, ancienne, nouvelle, cle_section)]
    for i, o in enumerate(ops):
        ref = f"op #{i + 1}"
        if o.get('type') != 'SET_ATTRIBUTE':
            erreurs.append(f"{ref} : operation refusee « {o.get('type')} » "
                           "(seul SET_ATTRIBUTE est accepte)")
            continue
        if o.get('attributeId') != CLE:
            erreurs.append(f"{ref} : attribut refuse « {o.get('attributeId')} » "
                           f"(seul {CLE} est accepte)")
            continue
        eid = o.get('entityId')
        if eid not in E:
            erreurs.append(f"{ref} : entite absente du graphe ({eid})")
            continue
        entite = E[eid]
        ref = f"op #{i + 1} ({eid[:8]})"
        types = [nom_type.get(t, t) for t in entite.get('types') or []]
        if not any(t in TYPES_SECTION for t in types):
            erreurs.append(f"{ref} : la cible n'est pas une section "
                           f"({'+'.join(types) or 'sans type'}) — hors du "
                           "domaine declare au registre")
            continue

        valeur = o.get('value')
        if not isinstance(valeur, dict) or valeur.get('type') != 'NUMBER':
            erreurs.append(f"{ref} : valeur cible mal formee (attendu "
                           "{{type: NUMBER, value: entier}})")
            continue
        nouvelle = entier(valeur.get('value'))
        if nouvelle is None:
            erreurs.append(f"{ref} : valeur cible non entiere "
                           f"({valeur.get('value')!r})")
            continue

        attrs = entite.get('attributes') or {}
        if CLE not in attrs:
            erreurs.append(f"{ref} : l'entite ne porte AUCUN {CLE} — ce patch "
                           "repare des valeurs presentes, il n'en cree pas")
            continue
        courant = attrs[CLE]
        if not isinstance(courant, dict) or courant.get('type') != 'NUMBER':
            erreurs.append(f"{ref} : {CLE} du graphe n'est pas de type NUMBER "
                           f"({courant!r}) — le patch ne change que le nombre")
            continue
        ancienne = entier(valeur_attribut(courant))
        if ancienne is None:
            erreurs.append(f"{ref} : {CLE} du graphe non entier ({courant!r})")
            continue

        # source 2 : la valeur ancienne inscrite dans le commentaire de l'op
        m = MOTIF_COMMENT.search(o.get('_comment') or '')
        if not m:
            erreurs.append(f"{ref} : le _comment ne declare pas « page_start "
                           "X -> Y », la valeur ancienne attendue est "
                           "inverifiable")
            continue
        c_ancienne, c_nouvelle = int(m.group(1)), int(m.group(2))
        # source 3 : la preuve enregistree
        ligne = csv_par_id.get(eid)
        if ligne is None:
            erreurs.append(f"{ref} : aucune ligne dans "
                           f"{os.path.basename(args.csv)}")
            continue
        csv_ancienne = entier(ligne.get('page_start_actuel'))
        csv_verifiee = entier(ligne.get('page_imprimee_verifiee'))
        statut = (ligne.get('statut') or '').strip()

        if not (ancienne == c_ancienne == csv_ancienne):
            erreurs.append(
                f"{ref} : valeur ancienne discordante — graphe {ancienne}, "
                f"_comment {c_ancienne}, CSV {csv_ancienne} : le graphe a "
                "derive depuis la redaction du patch, application refusee")
            continue
        if not (nouvelle == c_nouvelle == csv_verifiee):
            erreurs.append(
                f"{ref} : valeur cible discordante — patch {nouvelle}, "
                f"_comment {c_nouvelle}, CSV {csv_verifiee}")
            continue
        if statut != 'incoherent':
            erreurs.append(f"{ref} : le CSV classe ce noeud « {statut} » et "
                           "non « incoherent » — hors perimetre de reparation")
            continue
        if ancienne == nouvelle:
            erreurs.append(f"{ref} : op sans effet ({ancienne} -> {nouvelle})")
            continue

        cle_section = valeur_attribut((entite.get('attributes') or {})
                                      .get('section_key')) or ''
        plan.append((eid, ancienne, nouvelle, str(cle_section)))

    declare = meta.get('op_count')
    if declare is not None and declare != len(ops):
        erreurs.append(f"_meta.op_count = {declare} != {len(ops)} ops reelles")
    if len({o.get('entityId') for o in ops}) != len(ops):
        erreurs.append("une entite est visee par plusieurs ops : le patch "
                       "s'ecraserait lui-meme")
    if not erreurs and len(plan) != len(ops):
        erreurs.append(f"{len(plan)} op(s) retenues sur {len(ops)} : le script "
                       "n'applique jamais un patch partiellement")

    if erreurs:
        for x in erreurs[:20]:
            print(f"  - {x}", file=sys.stderr)
        echec(f"{len(erreurs)} erreur(s) de validation — rien n'a ete ecrit")

    # ---------- application ----------
    for eid, _ancienne, nouvelle, _cle in plan:
        E[eid]['attributes'][CLE] = {'type': 'NUMBER', 'value': nouvelle}

    print(f"source : {base}")
    print(f"patch  : {os.path.basename(args.patch)} "
          f"({len(ops)} op(s), {len(meta.get('skipped') or [])} skipped)")
    print(f"\n{len(plan)} corrections de {CLE} :")
    for eid, ancienne, nouvelle, cle in sorted(plan, key=lambda x: x[1]):
        print(f"  {cle or eid[:8]:<12s} {ancienne:>4d} -> {nouvelle:<4d} "
              f"(ecart {ancienne - nouvelle:+d})   {eid[:8]}")

    # ---------- verifications d'apres ----------
    attendu = {(eid, CLE): (a, n) for eid, a, n, _ in plan}
    changes, crees, supprimes, autres = diff_attributs(temoin, g)

    if autres:
        for x in autres[:10]:
            print(f"  - {x}", file=sys.stderr)
        echec(f"{len(autres)} modification(s) hors attributs d'entite : ce "
              "patch ne touche ni entite, ni relation, ni type, ni op")
    if crees or supprimes:
        echec(f"cles d'attribut creees ({len(crees)}) ou supprimees "
              f"({len(supprimes)}) : le patch ne fait qu'ecraser des valeurs")
    if len(changes) != len(plan):
        for eid, cle, a, b in changes[:10]:
            print(f"  - {eid[:8]} {cle} : {a} -> {b}", file=sys.stderr)
        echec(f"{len(changes)} attribut(s) modifie(s) dans tout le graphe, "
              f"{len(plan)} attendus")
    for eid, cle, a, b in changes:
        if (eid, cle) not in attendu:
            echec(f"attribut modifie hors plan : {eid[:8]} / {cle}")
        a_att, n_att = attendu[(eid, cle)]
        if entier(valeur_attribut(a)) != a_att or \
                entier(valeur_attribut(b)) != n_att:
            echec(f"valeur inattendue sur {eid[:8]} : {a} -> {b} "
                  f"(attendu {a_att} -> {n_att})")
        if not isinstance(b, dict) or b.get('type') != 'NUMBER':
            echec(f"type de valeur altere sur {eid[:8]} : {b!r}")

    if len(g['entities']) != avant_e or len(g['relations']) != avant_r:
        echec("aucune entite ni relation ne devait etre creee ou supprimee")

    # Les 49 `skipped` : inchanges. 48 ne portent aucun page_start et ne
    # doivent toujours pas en porter (aucune completion) ; le 49e (`ambigu`)
    # garde la valeur que v110 lui donne.
    temoin_E = {e['id']: e for e in temoin['entities']}
    remplis, alteres, inconnus = [], [], []
    for s in meta.get('skipped') or []:
        eid = s.get('entityId')
        if eid not in E:
            inconnus.append(eid)
            continue
        av = (temoin_E[eid].get('attributes') or {}).get(CLE)
        ap = (E[eid].get('attributes') or {}).get(CLE)
        if av is None and ap is not None:
            remplis.append(eid)
        elif av != ap:
            alteres.append(eid)
    if remplis:
        echec(f"completion detectee sur {len(remplis)} noeud(s) `skipped` : "
              f"{[x[:8] for x in remplis[:5]]}")
    if alteres:
        echec(f"{len(alteres)} noeud(s) `skipped` alteres : "
              f"{[x[:8] for x in alteres[:5]]}")
    if inconnus:
        echec(f"{len(inconnus)} entityId de `skipped` absents du graphe : "
              f"{[str(x)[:8] for x in inconnus[:5]]}")

    # Le registre reste l'invariant, comme depuis v110.
    entrees = registre.get('entries') or registre.get('properties') or []
    reg = {x['key']: x for x in entrees}
    cles = set()
    for e in g['entities']:
        cles |= set(e.get('attributes') or {})
    hors = cles - set(reg)
    if hors:
        echec(f"cles du graphe hors registre : {sorted(hors)[:6]}")
    fantomes = [k for k, x in reg.items()
                if x.get('status') == 'deprecated' and k in cles]
    if fantomes:
        echec(f"cles depreciees encore presentes : {fantomes}")

    porteurs = collections.Counter()
    for e in g['entities']:
        if CLE in (e.get('attributes') or {}):
            for t in e.get('types') or []:
                porteurs[nom_type.get(t, t)] += 1
    porteurs_avant = collections.Counter()
    for e in temoin['entities']:
        if CLE in (e.get('attributes') or {}):
            for t in e.get('types') or []:
                porteurs_avant[nom_type.get(t, t)] += 1
    if porteurs != porteurs_avant:
        echec(f"les porteurs de {CLE} ont change : {porteurs_avant} -> "
              f"{porteurs} (le registre serait a etendre)")

    print(f"\n  entites : {avant_e} (inchange) · relations : {avant_r} (inchange)")
    print(f"  diff exhaustif : {len(changes)} attribut(s) modifie(s), "
          "0 cree, 0 supprime, 0 changement hors attributs")
    print("  types, relation_types, ops, space : identiques")
    print(f"  skipped : {len(meta.get('skipped') or [])} noeuds inchanges, "
          "0 completion")
    print(f"  porteurs de {CLE} : "
          f"{dict(porteurs)} (inchanges) · toutes cles au registre")

    if args.dry_run:
        print("\n--dry-run : rien ecrit.")
        return 0

    if os.path.realpath(args.target) == os.path.realpath(args.source):
        echec("la cible est le graphe SOURCE : ce script ecrit une nouvelle "
              "version, il n'ecrase jamais celle qu'il lit", CODE_INVOCATION)
    espace = g.setdefault('space', {})
    m_v = re.search(r'-(v\d+)\.json$', os.path.basename(args.target))
    if not m_v:
        echec("nom de sortie sans numero de version : "
              f"{os.path.basename(args.target)}", CODE_INVOCATION)
    if m_v.group(1) != VERSION_CIBLE:
        echec(f"cible en {m_v.group(1)} : cet applicateur produit "
              f"{VERSION_CIBLE} et rien d'autre", CODE_INVOCATION)
    espace['version'] = m_v.group(1)
    espace['entity_count'] = len(g['entities'])
    espace['relation_count'] = len(g['relations'])
    # Note bornee, comme depuis v110 : l'historique complet vit dans CLAUDE.md.
    heritee = espace.get('note', '')
    if len(heritee) > 1200:
        heritee = heritee[:1200].rsplit(' ', 1)[0] + ' […]'
    espace['note'] = (
        f"V111 — page_start des sections : {len(plan)} valeurs corrigees sur "
        "les 16 noeuds diagnostiques incoherents contre les PDF imprimes de la "
        "these (page_start repair lab, PR #116 ; patch candidat "
        "patch_candidate_section_page_start_v1.json applique apres arbitrage de "
        "l'auteur). Sequelle des renumerotations v100/v106 : la valeur avait "
        "suivi le noeud, la cle avait change de section. Aucune completion : "
        "les 49 noeuds sans page_start etabli restent vides. Aucune "
        "SourceQuote, aucun lien, aucune cle de section touchee. " + heritee)

    # Ecriture ATOMIQUE : un json.dump interrompu laisserait un graphe
    # tronque a la place de la cible. On serialise a cote, puis on remplace.
    temporaire = args.target + '.tmp'
    try:
        with open(temporaire, 'w', encoding='utf-8') as f:
            json.dump(g, f, ensure_ascii=False, indent=2)
        os.replace(temporaire, args.target)
    except OSError as err:
        if os.path.exists(temporaire):
            os.unlink(temporaire)
        echec(f"ecriture impossible : {err}")
    print(f"\ngraphe ecrit : {os.path.relpath(args.target, REPO)}")
    return 0


if __name__ == '__main__':
    sys.exit(main())
