#!/usr/bin/env python3
"""Smoke tests for Migration/build_v97_lots.py outputs."""

from __future__ import annotations

import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUTDIR = ROOT / "Migration" / "v97_lots"


def load_json(path: Path) -> dict:
    with path.open(encoding="utf-8") as f:
        return json.load(f)


def test_generator_outputs() -> None:
    subprocess.run(["python3", "Migration/build_v97_lots.py"], cwd=ROOT, check=True)

    expected_files = {
        "lot-1-concept-hierarchy.json",
        "lot-2-actornonhuman-split.json",
        "lot-3-stakeholder-groups.json",
        "lot-4-infrastructure-domain-canon.json",
        "lot-5-relations.json",
        "lot-6-missing-merges.json",
        # legacy compatibility bundles
        "lot-1-concepts.json",
        "lot-2-actors-stakeholders.json",
        "lot-3-infra-relations.json",
    }

    produced = {p.name for p in OUTDIR.glob("*.json")}
    missing = expected_files - produced
    assert not missing, f"Missing generated files: {sorted(missing)}"

    lot2 = load_json(OUTDIR / "lot-2-actornonhuman-split.json")
    lot2_names = {op["old_entity"] for op in lot2["operations"]}
    assert {
        "AntPool",
        "F2Pool",
        "GHash.io",
        "Slush Pool",
        "BTC Guild",
        "Bitcoin ABC",
        "Bitcoin Knots",
        "Bitcoin Unlimited",
    }.issubset(lot2_names)

    lot3 = load_json(OUTDIR / "lot-3-stakeholder-groups.json")
    assert len(lot3["operations"]) >= 6

    lot6 = load_json(OUTDIR / "lot-6-missing-merges.json")
    merges = {(op["old_entity"], op["new_entity"]) for op in lot6["operations"]}
    assert ("Nominalisme monetaire non etatiste", "Nominalisme monétaire non étatiste") in merges
    assert ("Ethereum Virtual Machine", "Ethereum Virtual Machine (EVM)") in merges
    assert ("Politique de crises", "Politique de crise") in merges


if __name__ == "__main__":
    test_generator_outputs()
    print("OK: test_build_v97_lots")
