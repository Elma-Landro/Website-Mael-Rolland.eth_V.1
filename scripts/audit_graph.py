#!/usr/bin/env python3
"""
Argos V0 — Audit structurel déterministe du graphe GRC-20.

Script en lecture seule : ne modifie jamais le graphe.
Python 3 standard library uniquement (aucune dépendance externe).

Usage:
    python3 scripts/audit_graph.py
    python3 scripts/audit_graph.py --input grc20-these-mael-rolland-v96.json
    python3 scripts/audit_graph.py --json /tmp/grc20-audit.json
    python3 scripts/audit_graph.py --input ... --json ...

Exit codes:
    0 = aucun problème critique
    1 = au moins un problème critique détecté
    2 = erreur fatale (fichier introuvable, JSON invalide au niveau lecture)

Problèmes critiques:
    - JSON invalide
    - ID d'entité dupliqué
    - relation avec endpoint 'from' manquant
    - relation avec endpoint 'to' manquant
    - entité orpheline stricte (degré 0)

Warnings:
    - types inutilisés / relation types inutilisés
    - pseudo-orphelins (connectés uniquement via 'appears in section')
    - descriptions absentes
    - dominance de 'appears in section'
    - relation types <= 2 occurrences
    - space.id placeholder
    - relations génériques (relatedTo, is_related_to, associated_with)
"""

import argparse
import collections
import glob
import json
import os
import sys


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _entity_type_ids(e):
    """Retourne la liste des type IDs d'une entité (robuste aux formats)."""
    t = e.get("types", [])
    if isinstance(t, list):
        return t
    if isinstance(t, str):
        return [t]
    return []


def _desc_text(e):
    """Extrait le texte de description d'une entité.
    La description peut être: str, {type, value, options}, ou None.
    """
    d = e.get("description")
    if d is None:
        return ""
    if isinstance(d, str):
        return d.strip()
    if isinstance(d, dict):
        v = d.get("value", "")
        if isinstance(v, str):
            return v.strip()
        return str(v).strip()
    return str(d).strip()


# ---------------------------------------------------------------------------
# Audit principal
# ---------------------------------------------------------------------------

def audit_graph(data):
    """Retourne un dict avec tous les résultats de l'audit."""
    r = {}

    entities = data.get("entities", [])
    relations = data.get("relations", [])
    types = data.get("types", [])
    rel_types = data.get("relation_types", [])
    space = data.get("space", {})

    # --- Statistiques globales ---
    r["entities_count"] = len(entities)
    r["relations_count"] = len(relations)
    r["types_count"] = len(types)
    r["relation_types_count"] = len(rel_types)

    # --- Lookups ---
    type_id_to_name = {t["id"]: t["name"] for t in types}
    type_ids_defined = set(type_id_to_name.keys())
    rtype_id_to_name = {rt["id"]: rt["name"] for rt in rel_types}
    rtype_ids_defined = set(rtype_id_to_name.keys())

    entity_ids = [e["id"] for e in entities]
    entity_id_set = set(entity_ids)
    ent_by_id = {e["id"]: e for e in entities}

    # --- 6. IDs d'entités dupliqués ---
    id_counts = collections.Counter(entity_ids)
    r["duplicate_ids"] = {k: v for k, v in id_counts.items() if v > 1}

    # --- 7 & 8. Relations avec endpoint manquant ---
    r["broken_from"] = []
    r["broken_to"] = []
    for rel in relations:
        fid = rel.get("from")
        tid = rel.get("to")
        if fid not in entity_id_set:
            r["broken_from"].append({
                "relation_id": rel.get("id", "?"),
                "missing_from": fid,
                "to": tid,
                "type": rtype_id_to_name.get(rel.get("type"), rel.get("type")),
            })
        if tid not in entity_id_set:
            r["broken_to"].append({
                "relation_id": rel.get("id", "?"),
                "from": fid,
                "missing_to": tid,
                "type": rtype_id_to_name.get(rel.get("type"), rel.get("type")),
            })

    # --- Usage des types d'entités ---
    type_usage = collections.Counter()
    for e in entities:
        for t in _entity_type_ids(e):
            type_usage[t] += 1

    # --- 9. Types définis mais jamais utilisés ---
    r["unused_types"] = sorted(type_ids_defined - set(type_usage.keys()))
    # --- 10. Types utilisés mais non définis ---
    r["undefined_types_used"] = sorted(set(type_usage.keys()) - type_ids_defined)

    # --- Usage des relation types ---
    rtype_usage = collections.Counter()
    for rel in relations:
        rtype_usage[rel.get("type")] += 1

    # --- 11. Relation types définis mais jamais utilisés ---
    r["unused_relation_types"] = sorted(rtype_ids_defined - set(rtype_usage.keys()))
    # --- 12. Relation types utilisés mais non définis ---
    r["undefined_relation_types_used"] = sorted(
        set(rtype_usage.keys()) - rtype_ids_defined
    )

    # --- Degrés (toutes relations) ---
    degree = collections.Counter()
    degree_ais = collections.Counter()  # via 'appears in section'
    degree_other = collections.Counter()

    ais_type_ids = set()
    for rt in rel_types:
        if rt["name"] == "appears in section":
            ais_type_ids.add(rt["id"])

    for rel in relations:
        fid = rel.get("from")
        tid = rel.get("to")
        rt = rel.get("type")
        # On ne compte le degré que sur les endpoints valides
        if fid in entity_id_set:
            degree[fid] += 1
            if rt in ais_type_ids:
                degree_ais[fid] += 1
            else:
                degree_other[fid] += 1
        if tid in entity_id_set:
            degree[tid] += 1
            if rt in ais_type_ids:
                degree_ais[tid] += 1
            else:
                degree_other[tid] += 1

    # --- 13. Orphelins stricts (degré 0) ---
    r["orphans"] = []
    for e in entities:
        if degree[e["id"]] == 0:
            r["orphans"].append({
                "id": e["id"],
                "name": e.get("name", "???"),
                "type": type_id_to_name.get(
                    _entity_type_ids(e)[0], "?"
                ) if _entity_type_ids(e) else "?",
            })

    # --- 14. Pseudo-orphelins (connectés uniquement via 'appears in section') ---
    r["pseudo_orphans"] = []
    for e in entities:
        eid = e["id"]
        if degree[eid] > 0 and degree_other[eid] == 0 and degree_ais[eid] > 0:
            r["pseudo_orphans"].append({
                "id": eid,
                "name": e.get("name", "???"),
                "type": type_id_to_name.get(
                    _entity_type_ids(e)[0], "?"
                ) if _entity_type_ids(e) else "?",
            })

    # --- 15. Entités sans description ---
    r["no_description"] = []
    for e in entities:
        if not _desc_text(e):
            r["no_description"].append({
                "id": e["id"],
                "name": e.get("name", "???"),
                "type": type_id_to_name.get(
                    _entity_type_ids(e)[0], "?"
                ) if _entity_type_ids(e) else "?",
            })

    # --- 16. Relation types utilisés <= 2 fois ---
    sparse_rtypes = []
    for rt_id, count in rtype_usage.items():
        if count <= 2:
            sparse_rtypes.append({
                "id": rt_id,
                "name": rtype_id_to_name.get(rt_id, "?"),
                "count": count,
            })
    sparse_rtypes.sort(key=lambda x: (x["count"], x["name"]))
    r["sparse_relation_types"] = sparse_rtypes

    # --- 17. Dominance de 'appears in section' ---
    ais_total = sum(
        count for rt_id, count in rtype_usage.items() if rt_id in ais_type_ids
    )
    total_rels = len(relations)
    r["appears_in_section_count"] = ais_total
    r["appears_in_section_pct"] = (
        round(ais_total / total_rels * 100, 1) if total_rels else 0
    )

    # --- 18. Relation types génériques ---
    generic_patterns = {"relatedto", "is_related_to", "associated_with"}
    r["generic_relation_types"] = []
    for rt in rel_types:
        name_normalized = rt["name"].lower().replace(" ", "_").replace("-", "_")
        if name_normalized in generic_patterns:
            r["generic_relation_types"].append({
                "id": rt["id"],
                "name": rt["name"],
                "usage_count": rtype_usage.get(rt["id"], 0),
            })
    # Aussi vérifier les types utilisés mais non définis
    for rt_id, count in rtype_usage.items():
        if rt_id not in rtype_ids_defined:
            name_normalized = rt_id.lower().replace(" ", "_").replace("-", "_")
            if name_normalized in generic_patterns:
                r["generic_relation_types"].append({
                    "id": rt_id,
                    "name": rt_id,
                    "usage_count": count,
                })

    # --- 19. space.id placeholder ---
    space_id = space.get("id", "")
    r["space_id"] = space_id
    r["space_id_placeholder"] = (
        "placeholder" in space_id.lower()
        or space_id.startswith("PLACEHOLDER")
        or space_id == ""
    )

    # --- Répartition par type (pour le rapport) ---
    r["type_distribution"] = []
    for t_id, count in type_usage.most_common():
        r["type_distribution"].append({
            "name": type_id_to_name.get(t_id, f"UNDEF({t_id})"),
            "count": count,
            "defined": t_id in type_ids_defined,
        })

    # --- Top relation types (pour le rapport) ---
    r["relation_type_distribution"] = []
    for rt_id, count in rtype_usage.most_common(15):
        r["relation_type_distribution"].append({
            "name": rtype_id_to_name.get(rt_id, f"UNDEF({rt_id})"),
            "count": count,
            "defined": rt_id in rtype_ids_defined,
        })

    return r


# ---------------------------------------------------------------------------
# Criticité
# ---------------------------------------------------------------------------

def has_critical_problems(r):
    """Détermine s'il y a au moins un problème critique."""
    return bool(
        r["duplicate_ids"]
        or r["broken_from"]
        or r["broken_to"]
        or r["orphans"]
    )


# ---------------------------------------------------------------------------
# Rapport Markdown
# ---------------------------------------------------------------------------

def render_markdown(r, graph_path):
    lines = []
    w = lines.append

    w(f"# Argos V0 — Audit structurel du graphe GRC-20")
    w(f"")
    w(f"**Fichier audité** : `{graph_path}`")
    w(f"")
    w(f"---")
    w(f"")
    w(f"## Statistiques globales")
    w(f"")
    w(f"| Métrique | Valeur |")
    w(f"| --- | ---: |")
    w(f"| Entités | {r['entities_count']} |")
    w(f"| Relations | {r['relations_count']} |")
    w(f"| Types d'entités (définis) | {r['types_count']} |")
    w(f"| Types de relations (définis) | {r['relation_types_count']} |")
    w(f"")
    w(f"---")
    w(f"")

    # --- Section critique ---
    w(f"## ☠️ Problèmes critiques")
    w(f"")

    # 1. JSON invalide — géré en amont, pas dans r

    # 6. IDs dupliqués
    if r["duplicate_ids"]:
        w(f"### IDs d'entités dupliqués : {len(r['duplicate_ids'])}")
        w(f"")
        for eid, cnt in sorted(r["duplicate_ids"].items(), key=lambda x: -x[1]):
            w(f"- `{eid}` (×{cnt})")
        w(f"")
    else:
        w(f"### IDs dupliqués : 0 ✓")
        w(f"")

    # 7. Relations cassées (from)
    if r["broken_from"]:
        w(f"### Relations avec `from` manquant : {len(r['broken_from'])}")
        w(f"")
        w(f"| # | type | from (manquant) | to |")
        w(f"| --- | --- | --- | --- |")
        for i, br in enumerate(r["broken_from"][:30], 1):
            w(f"| {i} | {br['type']} | `{br['missing_from']}` | "
              f"{br['to'][:40]} |")
        if len(r["broken_from"]) > 30:
            w(f"| ... | *(+{len(r['broken_from']) - 30} autres)* | | |")
        w(f"")
    else:
        w(f"### Relations avec `from` manquant : 0 ✓")
        w(f"")

    # 8. Relations cassées (to)
    if r["broken_to"]:
        w(f"### Relations avec `to` manquant : {len(r['broken_to'])}")
        w(f"")
        w(f"| # | type | from | to (manquant) |")
        w(f"| --- | --- | --- | --- |")
        for i, br in enumerate(r["broken_to"][:30], 1):
            w(f"| {i} | {br['type']} | `{br['from']}` | "
              f"`br['missing_to']` |")
        w(f"")
    else:
        w(f"### Relations avec `to` manquant : 0 ✓")
        w(f"")

    # 13. Orphelins
    if r["orphans"]:
        w(f"### Entités orphelines (degré 0) : {len(r['orphans'])}")
        w(f"")
        for o in r["orphans"][:20]:
            w(f"- [{o['type']}] {o['name']} (`{o['id']}`)")
        w(f"")
    else:
        w(f"### Entités orphelines (degré 0) : 0 ✓")
        w(f"")

    w(f"---")
    w(f"")

    # --- Section warnings ---
    w(f"## ⚠️ Warnings")
    w(f"")

    # 9 & 10. Types
    w(f"### Types d'entités")
    w(f"")
    w(f"- Définis mais **jamais utilisés** : "
      f"{len(r['unused_types'])}")
    if r["unused_types"]:
        names = [type_id_to_name_short(r, t) for t in r["unused_types"]]
        w(f"  - {', '.join(names)}")
    w(f"- Utilisés mais **non définis** : "
      f"{len(r['undefined_types_used'])}")
    if r["undefined_types_used"]:
        w(f"  - {', '.join(r['undefined_types_used'])}")
    w(f"")

    # 11 & 12. Relation types
    w(f"### Types de relations")
    w(f"")
    w(f"- Définis mais **jamais utilisés** : "
      f"{len(r['unused_relation_types'])}")
    if r["unused_relation_types"]:
        names = [rtype_id_to_name_short(r, t)
                 for t in r["unused_relation_types"]]
        w(f"  - {', '.join(names)}")
    w(f"- Utilisés mais **non définis** : "
      f"{len(r['undefined_relation_types_used'])}")
    if r["undefined_relation_types_used"]:
        w(f"  - {', '.join(r['undefined_relation_types_used'])}")
    w(f"")

    # 14. Pseudo-orphelins
    w(f"### Pseudo-orphelins (connectés uniquement via "
      f"'appears in section') : {len(r['pseudo_orphans'])}")
    w(f"")
    if r["pseudo_orphans"]:
        for po in r["pseudo_orphans"][:15]:
            w(f"- [{po['type']}] {po['name']}")
        if len(r["pseudo_orphans"]) > 15:
            w(f"- *(+{len(r['pseudo_orphans']) - 15} autres)*")
    w(f"")

    # 15. Descriptions absentes
    w(f"### Entités sans description : {len(r['no_description'])}")
    w(f"")
    if r["no_description"]:
        # Regrouper par type
        by_type = collections.Counter(e["type"] for e in r["no_description"])
        w(f"Par type :")
        w(f"")
        w(f"| Type | Sans description |")
        w(f"| --- | ---: |")
        for t, c in by_type.most_common():
            w(f"| {t} | {c} |")
    w(f"")

    # 16. Relation types rares
    w(f"### Types de relations utilisés ≤ 2 fois : "
      f"{len(r['sparse_relation_types'])}")
    w(f"")
    if r["sparse_relation_types"]:
        w(f"| Type | Occurrences |")
        w(f"| --- | ---: |")
        for s in r["sparse_relation_types"][:20]:
            w(f"| {s['name']} | {s['count']} |")
        if len(r["sparse_relation_types"]) > 20:
            w(f"| *(+{len(r['sparse_relation_types']) - 20} autres)* | |")
    w(f"")

    # 17. Dominance appears in section
    w(f"### Dominance de 'appears in section'")
    w(f"")
    w(f"- **{r['appears_in_section_count']}** relations "
      f"(sur {r['relations_count']}) = "
      f"**{r['appears_in_section_pct']}%**")
    w(f"")

    # 18. Relations génériques
    w(f"### Relations génériques (relatedTo, is_related_to, "
      f"associated_with)")
    w(f"")
    if r["generic_relation_types"]:
        for g in r["generic_relation_types"]:
            w(f"- `{g['name']}` ({g['usage_count']} occurrences)")
    else:
        w(f"Aucune ✓")
    w(f"")

    # 19. space.id
    w(f"### `space.id`")
    w(f"")
    w(f"- Valeur : `{r['space_id']}`")
    if r["space_id_placeholder"]:
        w(f"- ⚠️ **PLACEHOLDER** — non conforme GRC-20")
    else:
        w(f"- ✓ semble valide")
    w(f"")

    w(f"---")
    w(f"")
    w(f"## Top 10 — Types d'entités")
    w(f"")
    w(f"| # | Type | Entités |")
    w(f"| --- | --- | ---: |")
    for i, t in enumerate(r["type_distribution"][:10], 1):
        status = "" if t["defined"] else " ✗"
        w(f"| {i} | {t['name']}{status} | {t['count']} |")
    w(f"")

    w(f"## Top 10 — Types de relations")
    w(f"")
    w(f"| # | Type | Relations |")
    w(f"| --- | --- | ---: |")
    for i, t in enumerate(r["relation_type_distribution"][:10], 1):
        status = "" if t["defined"] else " ✗"
        w(f"| {i} | {t['name']}{status} | {t['count']} |")
    w(f"")

    # --- Verdict ---
    w(f"---")
    w(f"")
    if has_critical_problems(r):
        w(f"## ☠️ VERDIT : PROBLÈMES CRITIQUES DÉTECTÉS (exit 1)")
    else:
        w(f"## ✓ VERDIT : AUCUN PROBLÈME CRITIQUE (exit 0)")
    w(f"")

    return "\n".join(lines)


def type_id_to_name_short(r, t_id):
    """Nom court d'un type d'entité (pour les listes)."""
    for t in r.get("_types_lookup", []):
        pass
    # On n'a pas accès direct, on reconstitue depuis type_distribution
    # Mais unused_types sont par définition absents de type_distribution.
    # On retourne l'ID brut.
    return t_id


def rtype_id_to_name_short(r, rt_id):
    """Nom court d'un type de relation (pour les listes)."""
    # Pareil : unused_relation_types sont absents du distribution.
    return rt_id


# ---------------------------------------------------------------------------
# Rapport JSON machine-readable
# ---------------------------------------------------------------------------

def build_json_report(r, graph_path, json_ok=True):
    return {
        "graph_file": graph_path,
        "json_valid": json_ok,
        "summary": {
            "entities": r["entities_count"],
            "relations": r["relations_count"],
            "types_defined": r["types_count"],
            "relation_types_defined": r["relation_types_count"],
            "types_used": len(r["type_distribution"]),
            "relation_types_used": len(r["relation_type_distribution"]),
        },
        "critical": {
            "duplicate_ids": r["duplicate_ids"],
            "broken_from": r["broken_from"],
            "broken_to": r["broken_to"],
            "orphans": r["orphans"],
        },
        "warnings": {
            "unused_types_count": len(r["unused_types"]),
            "unused_types": r["unused_types"],
            "undefined_types_used": r["undefined_types_used"],
            "unused_relation_types_count": len(r["unused_relation_types"]),
            "unused_relation_types": r["unused_relation_types"],
            "undefined_relation_types_used": r["undefined_relation_types_used"],
            "pseudo_orphans_count": len(r["pseudo_orphans"]),
            "pseudo_orphans": r["pseudo_orphans"],
            "no_description_count": len(r["no_description"]),
            "sparse_relation_types_count": len(r["sparse_relation_types"]),
            "sparse_relation_types": r["sparse_relation_types"],
            "appears_in_section_count": r["appears_in_section_count"],
            "appears_in_section_pct": r["appears_in_section_pct"],
            "generic_relation_types": r["generic_relation_types"],
            "space_id": r["space_id"],
            "space_id_placeholder": r["space_id_placeholder"],
        },
        "has_critical": has_critical_problems(r),
    }


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def find_default_graph():
    """Trouve le graphe v*.json le plus récent dans le répertoire courant."""
    patterns = [
        "grc20-these-mael-rolland-v*.json",
        "grc20-these-mael-rolland*.json",
    ]
    candidates = []
    for pat in patterns:
        candidates.extend(glob.glob(pat))
    if not candidates:
        return None
    # Trier par numéro de version (extraction du N dans vN.json)
    def version_key(path):
        import re
        m = re.search(r"-v(\d+)\.json$", path)
        return int(m.group(1)) if m else 0
    candidates.sort(key=version_key, reverse=True)
    return candidates[0]


def main():
    parser = argparse.ArgumentParser(
        description="Argos V0 — Audit structurel déterministe du graphe GRC-20.",
    )
    parser.add_argument(
        "--input", "-i",
        help="Chemin vers le graphe JSON (défaut: version la plus récente).",
    )
    parser.add_argument(
        "--json",
        help="Chemin de sortie pour le rapport JSON machine-readable.",
    )
    parser.add_argument(
        "--quiet", "-q",
        action="store_true",
        help="Supprime le rapport Markdown sur stdout (utile avec --json).",
    )
    args = parser.parse_args()

    # Déterminer le graphe à auditer
    graph_path = args.input or find_default_graph()
    if not graph_path:
        print("Erreur : aucun graphe trouvé. Utilisez --input.", file=sys.stderr)
        sys.exit(2)
    if not os.path.exists(graph_path):
        print(f"Erreur : fichier introuvable : {graph_path}", file=sys.stderr)
        sys.exit(2)

    # --- 1. Validité JSON ---
    try:
        with open(graph_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        json_ok = True
    except (json.JSONDecodeError, IOError) as e:
        # JSON invalide = critique
        print(f"# Argos V0 — ERREUR FATALE", file=sys.stderr)
        print(f"", file=sys.stderr)
        print(f"Fichier : `{graph_path}`", file=sys.stderr)
        print(f"Erreur de parsing JSON : {e}", file=sys.stderr)
        # Rapport JSON d'erreur si demandé
        if args.json:
            err_report = {
                "graph_file": graph_path,
                "json_valid": False,
                "error": str(e),
                "has_critical": True,
            }
            with open(args.json, "w", encoding="utf-8") as out:
                json.dump(err_report, out, indent=2, ensure_ascii=False)
        sys.exit(1)

    # --- Audit ---
    r = audit_graph(data)

    # --- Rapport Markdown ---
    if not args.quiet:
        md = render_markdown(r, graph_path)
        print(md)

    # --- Rapport JSON ---
    if args.json:
        jr = build_json_report(r, graph_path, json_ok=json_ok)
        with open(args.json, "w", encoding="utf-8") as out:
            json.dump(jr, out, indent=2, ensure_ascii=False)
        if not args.quiet:
            print(f"\n*Rapport JSON écrit : `{args.json}`*\n")

    # --- Exit code ---
    if has_critical_problems(r):
        sys.exit(1)
    else:
        sys.exit(0)


if __name__ == "__main__":
    main()
