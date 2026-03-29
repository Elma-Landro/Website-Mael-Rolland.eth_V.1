#!/usr/bin/env python3
"""Build a 6-lot rollout plan for v97 ontology patching.

Goal: split changes into small, mergeable batches to avoid oversized diffs.
"""

import json
import unicodedata
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
GRAPH = ROOT / "grc20-these-mael-rolland-v96.json"
OUTDIR = ROOT / "Migration" / "v97_lots"
OUTDIR.mkdir(exist_ok=True)


def norm(s: str) -> str:
    s = (s or "").strip().lower()
    s = "".join(c for c in unicodedata.normalize("NFD", s) if unicodedata.category(c) != "Mn")
    return " ".join(s.split())


with GRAPH.open(encoding="utf-8") as f:
    g = json.load(f)

entities = [e.get("name", "") for e in g.get("entities", []) if e.get("name")]
by_norm = {norm(n): n for n in entities}


def exists_name(name: str) -> bool:
    return norm(name) in by_norm


payload_common = {
    "patch_series": "v97-rollout-split-6lots",
    "source_graph": "grc20-these-mael-rolland-v96.json",
}

# LOT-1 — hierarchy moves only (core gap)
lot1_ops = [
    # ConceptTechnical (~15)
    ("UTXO", "Concept", "ConceptTechnical"),
    ("Nonce", "Concept", "ConceptTechnical"),
    ("OP_RETURN", "Concept", "ConceptTechnical"),
    ("SHA-256", "Concept", "ConceptTechnical"),
    ("SegWit", "Concept", "ConceptTechnical"),
    ("EVM", "Concept", "ConceptTechnical"),
    ("Ethereum Virtual Machine (EVM)", "Concept", "ConceptTechnical"),
    ("Gas (Ethereum)", "Concept", "ConceptTechnical"),
    ("Proof of Work (PoW)", "Concept", "ConceptTechnical"),
    ("Proof of Stake (PoS)", "Concept", "ConceptTechnical"),
    ("Mempool", "Concept", "ConceptTechnical"),
    ("Fork", "Concept", "ConceptTechnical"),
    ("Hard Fork", "Concept", "ConceptTechnical"),
    ("Soft Fork", "Concept", "ConceptTechnical"),
    ("Double dépense (double spend)", "Concept", "ConceptTechnical"),
    # ConceptSecondary (~10)
    ("Ossification du protocole", "Concept", "ConceptSecondary"),
    ("Délégation et recentralisation", "Concept", "ConceptSecondary"),
    ("Gouvernance polycentrique", "Concept", "ConceptSecondary"),
    ("Gouvernance duale", "Concept", "ConceptSecondary"),
    ("Infrastructure sociotechnique", "Concept", "ConceptSecondary"),
    ("Interopérabilité", "Concept", "ConceptSecondary"),
    ("Capture réglementaire", "Concept", "ConceptSecondary"),
    ("Effets de réseau", "Concept", "ConceptSecondary"),
    ("Politique de crise", "Concept", "ConceptSecondary"),
    ("Logique de consensus distribué", "Concept", "ConceptSecondary"),
    # NativeFormula (~5)
    ("Be your own bank", "Concept", "NativeFormula"),
    ("Don’t trust, verify", "Concept", "NativeFormula"),
    ("Code is law", "Concept", "NativeFormula"),
    ("Not your keys, not your coins", "Concept", "NativeFormula"),
    ("In code we trust", "Concept", "NativeFormula"),
    # ChapterSection (~5)
    ("Introduction", "Concept", "ChapterSection"),
    ("Cadre théorique", "Concept", "ChapterSection"),
    ("Méthodologie", "Concept", "ChapterSection"),
    ("Analyse comparative BTC/ETH", "Concept", "ChapterSection"),
    ("Conclusion", "Concept", "ChapterSection"),
]

lot1 = {
    **payload_common,
    "lot": "LOT-1",
    "title": "Hiérarchie des concepts (ConceptTechnical/ConceptSecondary/NativeFormula/ChapterSection)",
    "operations": [
        {
            "old_entity": name,
            "old_type": old_t,
            "action": "rename_retype",
            "new_entity": name,
            "new_type": new_t,
            "confidence": 0.75,
            "rationale": "split hierarchy to reduce unclassified Concept backlog",
            "old_entity_exists_v96": exists_name(name),
            "new_entity_exists_v96": exists_name(name),
        }
        for (name, old_t, new_t) in lot1_ops
    ],
}

# LOT-2 — remaining ActorNonHuman split
lot2_ops = [
    ("AntPool", "InfrastructureService"),
    ("F2Pool", "InfrastructureService"),
    ("GHash.io", "InfrastructureService"),
    ("Slush Pool", "InfrastructureService"),
    ("BTC Guild", "InfrastructureService"),
    ("Bitcoin ABC", "SoftwareClient"),
    ("Bitcoin Knots", "SoftwareClient"),
    ("Bitcoin Unlimited", "SoftwareClient"),
]

lot2 = {
    **payload_common,
    "lot": "LOT-2",
    "title": "ActorNonHuman → InfrastructureService / SoftwareClient",
    "operations": [
        {
            "old_entity": name,
            "old_type": "ActorNonHuman",
            "action": "retype",
            "new_entity": name,
            "new_type": new_t,
            "confidence": 0.99,
            "rationale": "explicit remaining split requested",
            "old_entity_exists_v96": exists_name(name),
            "new_entity_exists_v96": exists_name(name),
        }
        for (name, new_t) in lot2_ops
    ],
}

# LOT-3 — StakeholderGroup completion (6+)
lot3_ops = [
    "Mineurs Bitcoin",
    "Pools de minage",
    "Opérateurs de nœuds complets",
    "Fournisseurs de portefeuilles",
    "Core Developers (Bitcoin)",
    "Core Developers (Ethereum)",
]

lot3 = {
    **payload_common,
    "lot": "LOT-3",
    "title": "Complétion StakeholderGroup (6 collectifs minimum)",
    "operations": [
        {
            "old_entity": name,
            "old_type": "ActorGroup",
            "action": "rename_retype",
            "new_entity": name,
            "new_type": "StakeholderGroup",
            "confidence": 0.9,
            "rationale": "separate empirical collectives from analytical categories",
            "old_entity_exists_v96": exists_name(name),
            "new_entity_exists_v96": exists_name(name),
        }
        for name in lot3_ops
    ],
}

# LOT-4 — canonical InfrastructureDomain target only
lot4 = {
    **payload_common,
    "lot": "LOT-4",
    "title": "Canonisation InfrastructureDomain (9 domaines cibles)",
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

# LOT-5 — missing relation families
relations = [
    ("Core Developers (Bitcoin)", "instanceOfCategory", "Développeurs Core"),
    ("Core Developers (Ethereum)", "instanceOfCategory", "Développeurs Core"),
    ("Mineurs Bitcoin", "instanceOfCategory", "Mineurs et assimilés"),
    ("Pools de minage", "instanceOfCategory", "Mineurs et assimilés"),
    ("Opérateurs de nœuds complets", "instanceOfCategory", "Nœuds complets (Full Nodes)"),
    ("Fournisseurs de portefeuilles", "instanceOfCategory", "Fournisseurs de portefeuilles"),
    ("Monétisation", "organizes", "UCN BTC"),
    ("Monétisation", "organizes", "UCN ETH"),
    ("Monétisation", "partOfMonetizationProcess", "Passerelle (gateway / on-off ramp)"),
    ("Monétisation", "partOfMonetizationProcess", "Services de portefeuille et de paiement"),
]

lot5 = {
    **payload_common,
    "lot": "LOT-5",
    "title": "Ajout des nouvelles familles de relations",
    "relations_to_add": [
        {
            "subject": s,
            "predicate": p,
            "object": o,
            "subject_exists_v96": exists_name(s),
            "object_exists_v96": exists_name(o),
        }
        for (s, p, o) in relations
    ],
}

# LOT-6 — unresolved merges
lot6_merges = [
    ("Nominalisme monetaire non etatiste", "Nominalisme monétaire non étatiste"),
    ("Ethereum Virtual Machine", "Ethereum Virtual Machine (EVM)"),
    ("Politique de crises", "Politique de crise"),
]

lot6 = {
    **payload_common,
    "lot": "LOT-6",
    "title": "Fusions manquées restantes (normalisation finale)",
    "operations": [
        {
            "old_entity": old,
            "old_type": "Concept",
            "action": "merge_into",
            "new_entity": new,
            "new_type": "Concept",
            "confidence": 0.95,
            "rationale": "fix unresolved merge from the non-implemented checklist",
            "old_entity_exists_v96": exists_name(old),
            "new_entity_exists_v96": exists_name(new),
        }
        for (old, new) in lot6_merges
    ],
}

outputs = {
    "lot-1-concept-hierarchy.json": lot1,
    "lot-2-actornonhuman-split.json": lot2,
    "lot-3-stakeholder-groups.json": lot3,
    "lot-4-infrastructure-domain-canon.json": lot4,
    "lot-5-relations.json": lot5,
    "lot-6-missing-merges.json": lot6,
}

for filename, payload in outputs.items():
    (OUTDIR / filename).write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

# README for merge sequencing
md = """# v97 rollout en 6 lots (task-by-task)

Base: `grc20-these-mael-rolland-v96.json`.

Objectif: éviter le dépassement de taille de diff en poussant **lot par lot**.

## Ordre de merge recommandé
1. `lot-1-concept-hierarchy.json` — hiérarchie des concepts (gros backlog)
2. `lot-2-actornonhuman-split.json` — ActorNonHuman résiduels
3. `lot-3-stakeholder-groups.json` — compléter 6+ StakeholderGroup
4. `lot-4-infrastructure-domain-canon.json` — 9 domaines canoniques
5. `lot-5-relations.json` — nouvelles relations (`instanceOfCategory`, `organizes`, `partOfMonetizationProcess`)
6. `lot-6-missing-merges.json` — fusions manquées finales

## Notes
- Chaque lot est indépendant et volontairement petit.
- Les champs `*_exists_v96` servent à vérifier rapidement la présence des labels dans la base v96.
"""
(OUTDIR / "README.md").write_text(md, encoding="utf-8")

print("Generated 6 lot files in", OUTDIR)
for filename in outputs:
    print("-", filename)
