#!/usr/bin/env python3
"""Reconcile capture labels without changing source text, dates, or coding."""
from __future__ import annotations

import argparse
import json
from pathlib import Path


def normalize(row: dict) -> dict:
    if row.get("evidence_status") != "substantive_description":
        return dict(row)
    if not isinstance(row.get("description"), str) or len(row["description"].strip()) < 100:
        raise ValueError(f"Substantive label without description: {row.get('paper_id')}")
    result = dict(row)
    # Retain the inherited inventory labels as provenance, not current access.
    result.setdefault("inventory_origin_labels", {
        key: row.get(key) for key in ["record_status", "access_status", "limits"]
    })
    result.update({
        "record_status": "official_description_captured",
        "access_status": "official_description_available",
        "limits": "Official conference description captured; not full-paper evidence. Technical coding and independent review are separate. Numerical conditions absent from the description remain unknown.",
    })
    return result


def build(root: Path) -> dict:
    outputs = []
    # Validate all inputs before writing either ledger. No fetching or re-dating.
    for year in [2025, 2026]:
        path = root / f"dac/data/paper-evidence-{year}.jsonl"
        rows = [json.loads(line) for line in path.read_text().splitlines() if line.strip()]
        updated = [normalize(row) for row in rows]
        outputs.append((path, updated, sum(a != b for a, b in zip(rows, updated))))
    for path, rows, _ in outputs:
        path.write_text("".join(json.dumps(r, sort_keys=True, ensure_ascii=False) + "\n" for r in rows), encoding="utf-8")
    return {path.name: {"record_count": len(rows), "changed_count": changed} for path, rows, changed in outputs}


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    print(json.dumps(build(parser.parse_args().root), indent=2, sort_keys=True))
