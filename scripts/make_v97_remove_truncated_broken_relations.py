#!/usr/bin/env python3
"""
make_v97_remove_truncated_broken_relations.py

Génère grc20-these-mael-rolland-v97.json depuis v96 en supprimant
uniquement les 15 relations cassées certaines (doublons orphelins
issus d'un bug de troncature d'UUID).

La 16ᵉ relation cassée (contributes to → Ostrom 1990, from 72d182705407492c)
est VOLONTAIREMENT CONSERVÉE pour revue humaine.

Python 3 stdlib uniquement. Ne modifie jamais v96.
"""

import json
import os
import sys

# --- Chemins ---
REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
V96 = os.path.join(REPO, "grc20-these-mael-rolland-v96.json")
V97 = os.path.join(REPO, "grc20-these-mael-rolland-v97.json")
PATCH_FILE = os.path.join(REPO, "patches", "grc20_v97_remove_15_truncated_broken_relations.json")

# --- La relation sensible à CONSERVER (ne JAMAIS supprimer) ---
OSTROM_FROM = "72d182705407492c"


def load_graph(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def is_truncated_broken(rel, entity_id_set):
    """Détecte une relation dont le 'from' est tronqué (16 chars au lieu de 32)
    ET pour laquelle une relation valide identique existe déjà (même type,
    même 'to', 'from' complet qui commence par ces 16 chars)."""
    fid = rel.get("from", "")
    tid = rel.get("to", "")
    rt = rel.get("type", "")

    # Le 'from' doit faire exactement 16 chars hex
    if len(fid) != 16:
        return False
    # Le 'from' ne doit pas exister dans les entités
    if fid in entity_id_set:
        return False
    # Le 'to' doit exister
    if tid not in entity_id_set:
        return False

    # Chercher une relation valide correspondante
    # (même type, même 'to', 'from' de 32 chars commençant par fid)
    return fid  # Retourne le prefix pour recherche externe


def main():
    # --- Charger v96 ---
    if not os.path.exists(V96):
        print(f"ERREUR: v96 introuvable: {V96}", file=sys.stderr)
        sys.exit(1)

    print(f"Lecture de v96: {V96}")
    data = load_graph(V96)
    print(f"  Entités: {len(data['entities'])}")
    print(f"  Relations: {len(data['relations'])}")

    entity_id_set = {e["id"] for e in data["entities"]}
    relations = data["relations"]

    # --- Phase 1 : identifier toutes les relations cassées ---
    all_broken = []
    for idx, rel in enumerate(relations):
        fid = rel.get("from", "")
        tid = rel.get("to", "")
        if fid not in entity_id_set or tid not in entity_id_set:
            all_broken.append((idx, rel))

    print(f"\nRelations cassées détectées: {len(all_broken)}")

    # --- Phase 2 : identifier les 15 tronquées supprimables ---
    # Un 'from' tronqué fait 16 chars hex. Pour chacun, il doit exister
    # une relation valide avec un 'from' complet (32 chars) qui commence
    # par ce préfixe, avec le même type et le même 'to'.
    prefix_to_full = {}  # prefix16 → set de from32 complets valides
    for rel in relations:
        fid = rel.get("from", "")
        if len(fid) == 32 and fid in entity_id_set:
            prefix16 = fid[:16]
            if prefix16 not in prefix_to_full:
                prefix_to_full[prefix16] = set()
            prefix_to_full[prefix16].add(fid)

    to_remove = []
    kept_for_review = []

    for idx, rel in all_broken:
        fid = rel.get("from", "")
        tid = rel.get("to", "")
        rt = rel.get("type", "")

        # Vérifier si c'est la relation sensible Ostrom
        if fid == OSTROM_FROM:
            kept_for_review.append((idx, rel))
            continue

        # Vérifier si c'est une troncature avec doublon valide
        if len(fid) == 16 and fid in prefix_to_full:
            # Vérifier qu'une relation valide existe avec le même type + même to
            valid_exists = False
            for full_from in prefix_to_full[fid]:
                for r2 in relations:
                    if (
                        r2.get("from") == full_from
                        and r2.get("to") == tid
                        and r2.get("type") == rt
                        and r2.get("from") != fid  # pas la relation cassée elle-même
                    ):
                        valid_exists = True
                        break
                if valid_exists:
                    break
            if valid_exists:
                to_remove.append((idx, rel))
                continue

        # Si on arrive ici, c'est une relation cassée non classée
        kept_for_review.append((idx, rel))

    print(f"  À supprimer (doublons tronqués): {len(to_remove)}")
    print(f"  Conservées pour revue humaine: {len(kept_for_review)}")

    # --- Phase 3 : assertions de sécurité ---
    if len(to_remove) != 15:
        print(
            f"\nERREUR FATALE: attendu 15 relations à supprimer, "
            f"trouvé {len(to_remove)}. Abandon.",
            file=sys.stderr,
        )
        sys.exit(1)

    # Vérifier qu'aucune des relations à supprimer n'est la relation Ostrom
    for idx, rel in to_remove:
        if rel.get("from") == OSTROM_FROM:
            print(
                f"\nERREUR FATALE: la relation Ostrom (from={OSTROM_FROM}) "
                f"est dans la liste de suppression ! Abandon.",
                file=sys.stderr,
            )
            sys.exit(1)

    # Vérifier que la relation Ostrom est bien dans kept_for_review
    ostrom_found = any(
        rel.get("from") == OSTROM_FROM for _, rel in kept_for_review
    )
    if not ostrom_found:
        print(
            f"\nERREUR FATALE: la relation Ostrom (from={OSTROM_FROM}) "
            f"n'est pas dans kept_for_review ! Abandon.",
            file=sys.stderr,
        )
        sys.exit(1)

    print("\nAssertions de sécurité: ✓")
    print(f"  15 relations à supprimer: confirmé")
    print(f"  Relation Ostrom conservée: confirmée")

    # --- Phase 4 : créer v97 ---
    indices_to_remove = {idx for idx, _ in to_remove}
    new_relations = [
        rel for idx, rel in enumerate(relations)
        if idx not in indices_to_remove
    ]

    data_v97 = dict(data)
    data_v97["relations"] = new_relations

    # Mettre à jour la métadonnée de version si présente
    if "space" in data_v97 and isinstance(data_v97["space"], dict):
        data_v97["space"]["version"] = "v97"

    print(f"\nÉcriture de v97: {V97}")
    with open(V97, "w", encoding="utf-8") as f:
        json.dump(data_v97, f, indent=2, ensure_ascii=False)

    print(f"  Relations v97: {len(new_relations)}")
    print(f"  Entités v97: {len(data_v97['entities'])} (inchangé)")

    # --- Phase 5 : patch documentaire ---
    os.makedirs(os.path.dirname(PATCH_FILE), exist_ok=True)

    patch = {
        "patch_id": "grc20_v97_remove_15_truncated_broken_relations",
        "source_graph": "grc20-these-mael-rolland-v96.json",
        "target_graph": "grc20-these-mael-rolland-v97.json",
        "operation": "remove_relations",
        "status": "prepared_and_applied_to_v97",
        "reason": (
            "Remove 15 broken duplicate relations caused by truncated/missing "
            "from IDs; keep the sensitive Ostrom contributes-to relation "
            "for human review."
        ),
        "removed_count": len(to_remove),
        "kept_for_human_review_count": len(kept_for_review),
        "removed_relations": [
            {
                "v96_index": idx,
                "relation_id": rel.get("id", "NO_RELATION_ID"),
                "type": rel.get("type", ""),
                "from_truncated": rel.get("from", ""),
                "to": rel.get("to", ""),
                "attributes": rel.get("attributes", []),
                "reason": (
                    "Truncated UUID (16/32 chars) with valid duplicate "
                    "relation already present in graph."
                ),
            }
            for idx, rel in to_remove
        ],
        "kept_for_human_review": [
            {
                "v96_index": idx,
                "relation_id": rel.get("id", "NO_RELATION_ID"),
                "type": rel.get("type", ""),
                "from_missing": rel.get("from", ""),
                "to": rel.get("to", ""),
                "to_label": "",
                "reason": (
                    "Genuine orphan — no matching entity or duplicate found. "
                    "Potential analytical value (contributes to → Ostrom 1990). "
                    "Requires human review to identify the missing source entity."
                ),
            }
            for idx, rel in kept_for_review
        ],
    }

    print(f"\nÉcriture du patch documentaire: {PATCH_FILE}")
    with open(PATCH_FILE, "w", encoding="utf-8") as f:
        json.dump(patch, f, indent=2, ensure_ascii=False)

    # --- Résumé final ---
    print("\n" + "=" * 60)
    print("RÉSUMÉ DE LA TRANSFORMATION v96 → v97")
    print("=" * 60)
    print(f"  Entités:       {len(data['entities'])} → {len(data_v97['entities'])} (inchangé)")
    print(f"  Relations:     {len(data['relations'])} → {len(new_relations)} (-15)")
    print(f"  Types:         {len(data['types'])} (inchangé)")
    print(f"  Relation types:{len(data['relation_types'])} (inchangé)")
    print(f"  Ops:           {len(data.get('ops', []))} (inchangé)")
    print(f"  v96 intact:    ✓")
    print(f"  Ostrom conservé: ✓")


if __name__ == "__main__":
    main()
