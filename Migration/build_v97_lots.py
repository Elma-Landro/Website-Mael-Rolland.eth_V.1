#!/usr/bin/env python3
"""Build v97 rollout split into mergeable lots.

Data-driven from migration inputs (table + seed patch + v96 graph).
"""

from __future__ import annotations

import argparse
import csv
import json
import unicodedata
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MIG = ROOT / "Migration"
TABLE = MIG / "grc20_v91_migration_table.csv"
BASE_PATCH = MIG / "grc20_v91_name_based_patch.json"
GRAPH = ROOT / "grc20-these-mael-rolland-v96.json"
DEFAULT_OUTDIR = MIG / "v97_lots"


def norm(s: str) -> str:
    s = (s or "").strip().lower()
    s = "".join(c for c in unicodedata.normalize("NFD", s) if unicodedata.category(c) != "Mn")
    return " ".join(s.split())


def build_payloads(include_legacy: bool = True) -> tuple[dict[str, dict], str, tuple[int, int, int, int, int]]:
    with TABLE.open(newline="", encoding="utf-8") as f:
        ops = list(csv.DictReader(f))
    with BASE_PATCH.open(encoding="utf-8") as f:
        base = json.load(f)
    with GRAPH.open(encoding="utf-8") as f:
        g = json.load(f)

    for op in ops:
        if op.get("confidence"):
            op["confidence"] = float(op["confidence"])

    entities = [e["name"] for e in g["entities"] if "name" in e]
    by_norm = {norm(n): n for n in entities}

    def exists_name(name: str) -> bool:
        return norm(name) in by_norm

    payload_common = {
        "patch_series": "v97-rollout-split-6lots",
        "source_graph": "grc20-these-mael-rolland-v96.json",
    }

    concept_targets = {
        "CoreConcept",
        "SecondaryConcept",
        "TechnicalConcept",
        "NativeFormula",
        "ChapterSection",
        "ConceptCore",
        "ConceptSecondary",
        "ConceptTechnical",
    }

    lot1_ops = [
        op
        for op in ops
        if op.get("old_type") == "Concept" or op.get("new_type") in concept_targets
    ]

    late_merge_old_entities = {
        "Nominalisme monetaire non etatiste",
        "Nominalisme monétaire non étatiste",
        "Ethereum Virtual Machine",
        "Ethereum Virtual Machine (EVM)",
        "Politique de crise",
        "Politique de crises",
    }
    lot1_ops = [op for op in lot1_ops if op.get("old_entity") not in late_merge_old_entities]

    explicit_actor_split = {
        ("AntPool", "InfrastructureService"),
        ("F2Pool", "InfrastructureService"),
        ("GHash.io", "InfrastructureService"),
        ("Slush Pool", "InfrastructureService"),
        ("BTC Guild", "InfrastructureService"),
        ("Bitcoin ABC", "SoftwareClient"),
        ("Bitcoin Knots", "SoftwareClient"),
        ("Bitcoin Unlimited", "SoftwareClient"),
    }

    lot2_ops = []
    for op in ops:
        key = (op.get("old_entity"), op.get("new_type"))
        if op.get("old_type") == "ActorNonHuman" and key in explicit_actor_split:
            lot2_ops.append(op)

    seen_lot2 = {(op["old_entity"], op["new_type"]) for op in lot2_ops}
    for entity, new_t in sorted(explicit_actor_split - seen_lot2):
        lot2_ops.append(
            {
                "old_entity": entity,
                "old_type": "ActorNonHuman",
                "action": "retype",
                "new_entity": entity,
                "new_type": new_t,
                "confidence": 0.99,
                "rationale": "explicit split from remaining ActorNonHuman backlog",
            }
        )

    target_stakeholders = {
        "Mineurs Bitcoin",
        "Pools de minage",
        "Opérateurs de nœuds complets",
        "Fournisseurs de portefeuilles",
        "Core Developers (Bitcoin)",
        "Core Developers (Ethereum)",
    }

    lot3_ops = []
    for op in ops:
        if op.get("new_type") == "StakeholderGroup" and op.get("old_entity") in target_stakeholders:
            lot3_ops.append(op)

    seen_lot3 = {op["old_entity"] for op in lot3_ops}
    for entity in sorted(target_stakeholders - seen_lot3):
        lot3_ops.append(
            {
                "old_entity": entity,
                "old_type": "ActorGroup",
                "action": "rename_retype",
                "new_entity": entity,
                "new_type": "StakeholderGroup",
                "confidence": 0.9,
                "rationale": "explicit completion to reach 6+ stakeholder groups",
            }
        )

    lot4 = {
        **payload_common,
        "lot": "LOT-4",
        "title": "InfrastructureDomain canonization (9 canonical domains)",
        "canonical_infrastructure_domains_target": [
            "Protocole et couche de base",
            "Traitement des transactions",
            "Altcoins, tokens et surcouches",
            "Services de portefeuille et de paiement",
            "Conformité réglementaire",
            "Sphère d’usage",
            "Information et connaissance",
            "Monétisation",
            "Gouvernance infrastructurelle",
        ],
    }

    relations = [
        r
        for r in base.get("new_relations", [])
        if r.get("predicate") in {"instanceOfCategory", "organizes", "partOfMonetizationProcess"}
    ]
    relations.extend(
        [
            {"subject": "Mineurs Bitcoin", "predicate": "instanceOfCategory", "object": "Mineurs et assimilés"},
            {"subject": "Pools de minage", "predicate": "instanceOfCategory", "object": "Mineurs et assimilés"},
            {
                "subject": "Opérateurs de nœuds complets",
                "predicate": "instanceOfCategory",
                "object": "Nœuds complets (Full Nodes)",
            },
            {
                "subject": "Fournisseurs de portefeuilles",
                "predicate": "instanceOfCategory",
                "object": "Fournisseurs de portefeuilles",
            },
        ]
    )

    seen_rel = set()
    dedup_rel = []
    for r in relations:
        key = (r["subject"], r["predicate"], r["object"])
        if key in seen_rel:
            continue
        seen_rel.add(key)
        dedup_rel.append(
            {
                "subject": r["subject"],
                "predicate": r["predicate"],
                "object": r["object"],
                "subject_exists_v96": exists_name(r["subject"]),
                "object_exists_v96": exists_name(r["object"]),
            }
        )

    lot6_ops = [
        {
            "old_entity": "Nominalisme monetaire non etatiste",
            "old_type": "Concept",
            "action": "merge_into",
            "new_entity": "Nominalisme monétaire non étatiste",
            "new_type": "Concept",
            "confidence": 0.99,
            "rationale": "accent canonicalization requested",
        },
        {
            "old_entity": "Ethereum Virtual Machine",
            "old_type": "Concept",
            "action": "merge_into",
            "new_entity": "Ethereum Virtual Machine (EVM)",
            "new_type": "ConceptTechnical",
            "confidence": 0.98,
            "rationale": "canonical EVM label normalization requested",
        },
        {
            "old_entity": "Politique de crises",
            "old_type": "Concept",
            "action": "merge_into",
            "new_entity": "Politique de crise",
            "new_type": "Concept",
            "confidence": 0.93,
            "rationale": "singular/plural normalization requested",
        },
    ]

    for _ops in (lot1_ops, lot2_ops, lot3_ops, lot6_ops):
        for op in _ops:
            op["old_entity_exists_v96"] = exists_name(op["old_entity"])
            op["new_entity_exists_v96"] = exists_name(op["new_entity"])

    lot1 = {**payload_common, "lot": "LOT-1", "title": "Concept hierarchy (without deferred missing merges)", "operations": lot1_ops}
    lot2 = {**payload_common, "lot": "LOT-2", "title": "ActorNonHuman split backlog (pools + clients)", "operations": lot2_ops}
    lot3 = {**payload_common, "lot": "LOT-3", "title": "StakeholderGroup completion (6+ groups)", "operations": lot3_ops}
    lot5 = {**payload_common, "lot": "LOT-5", "title": "New relation families", "relations_to_add": dedup_rel}
    lot6 = {**payload_common, "lot": "LOT-6", "title": "Deferred missing merges", "operations": lot6_ops}

    outputs: dict[str, dict] = {
        "lot-1-concept-hierarchy.json": lot1,
        "lot-2-actornonhuman-split.json": lot2,
        "lot-3-stakeholder-groups.json": lot3,
        "lot-4-infrastructure-domain-canon.json": lot4,
        "lot-5-relations.json": lot5,
        "lot-6-missing-merges.json": lot6,
    }

    if include_legacy:
        outputs.update(
            {
                "lot-1-concepts.json": lot1,
                "lot-2-actors-stakeholders.json": {
                    **payload_common,
                    "lot": "LOT-2-LEGACY",
                    "title": "Legacy compatibility bundle: ActorNonHuman + StakeholderGroup",
                    "operations": [*lot2_ops, *lot3_ops],
                },
                "lot-3-infra-relations.json": {
                    **payload_common,
                    "lot": "LOT-3-LEGACY",
                    "title": "Legacy compatibility bundle: InfrastructureDomain + relations",
                    "canonical_infrastructure_domains_target": lot4["canonical_infrastructure_domains_target"],
                    "relations_to_add": dedup_rel,
                },
            }
        )

    type_map = {t["name"]: t["id"] for t in g["types"]}
    concept_id = type_map.get("Concept")
    concept_unclassified = 0
    if concept_id:
        concept_unclassified = sum(1 for e in g["entities"] if concept_id in e.get("types", []))

    md = f"""# v97 rollout en 6 lots (task-by-task)

Base: `grc20-these-mael-rolland-v96.json`.

Objectif: éviter un diff massif en poussant **lot par lot**.

## Ordre de merge recommandé
1. `lot-1-concept-hierarchy.json` — hiérarchie de concepts (hors fusions reportées)
2. `lot-2-actornonhuman-split.json` — split ActorNonHuman restant
3. `lot-3-stakeholder-groups.json` — compléter 6+ StakeholderGroup
4. `lot-4-infrastructure-domain-canon.json` — 9 domaines canoniques
5. `lot-5-relations.json` — nouvelles relations (`instanceOfCategory`, `organizes`, `partOfMonetizationProcess`)
6. `lot-6-missing-merges.json` — fusions manquées (Nominalisme, EVM, Politique de crise[s])

## Tailles générées
- LOT-1: **{len(lot1_ops)} opérations**
- LOT-2: **{len(lot2_ops)} opérations**
- LOT-3: **{len(lot3_ops)} opérations**
- LOT-5: **{len(dedup_rel)} relations**
- LOT-6: **{len(lot6_ops)} opérations**

## État restant (avant application)
- Entités encore typées `Concept` en v96: **{concept_unclassified}**.
"""

    if include_legacy:
        md += """

## Compatibilité (anti-conflits de merge)
- Les anciens noms de fichiers sont aussi générés:
  - `lot-1-concepts.json`
  - `lot-2-actors-stakeholders.json`
  - `lot-3-infra-relations.json`
- Ces fichiers legacy évitent les conflits lorsque d'autres branches modifient encore les anciens paths.
"""

    return outputs, md, (len(lot1_ops), len(lot2_ops), len(lot3_ops), len(dedup_rel), len(lot6_ops))


def write_outputs(outdir: Path, include_legacy: bool) -> tuple[int, int, int, int, int]:
    outdir.mkdir(parents=True, exist_ok=True)
    outputs, readme_text, sizes = build_payloads(include_legacy=include_legacy)
    for filename, payload in outputs.items():
        (outdir / filename).write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    (outdir / "README.md").write_text(readme_text, encoding="utf-8")
    return sizes


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate v97 lots payload files.")
    parser.add_argument("--outdir", type=Path, default=DEFAULT_OUTDIR, help="Output directory for generated lots")
    parser.add_argument("--no-legacy", action="store_true", help="Do not emit legacy compatibility filenames")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    sizes = write_outputs(args.outdir, include_legacy=not args.no_legacy)
    print("Generated lots in", args.outdir)
    print("lot-1", sizes[0], "lot-2", sizes[1], "lot-3", sizes[2], "lot-5", sizes[3], "lot-6", sizes[4])


if __name__ == "__main__":
    main()
