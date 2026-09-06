#!/usr/bin/env python3
"""Extend the provisional taxonomy with subthemes observed in adjudicated records."""
from __future__ import annotations

import argparse
import json
from pathlib import Path


def rows(path: Path) -> list[dict]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def build(root: Path) -> dict:
    taxonomy = json.loads((root / "data/taxonomy-v0.json").read_text(encoding="utf-8"))
    adjudicated = rows(root / "dac/data/adjudicated-2026-batch.jsonl") + rows(root / "dac/data/adjudicated-2026-batch-2.jsonl") + rows(root / "dac/data/adjudicated-2026-batch-3.jsonl") + rows(root / "iccad/data/adjudicated-2025-batch.jsonl") + rows(root / "isca/data/adjudicated-2026-batch.jsonl")
    by_theme = {theme["theme_id"]: theme for theme in taxonomy["themes"]}
    for record in adjudicated:
        theme = by_theme[record["theme_id"]]
        subtheme = record["subtheme_id"]
        if subtheme not in theme["subthemes"]:
            theme["subthemes"].append(subtheme)
        theme.setdefault("subsubthemes", {}).setdefault(subtheme, [])
        if record["subsubtheme_id"] not in theme["subsubthemes"][subtheme]:
            theme["subsubthemes"][subtheme].append(record["subsubtheme_id"])
    for theme in taxonomy["themes"]:
        theme["subthemes"] = sorted(theme["subthemes"])
        for subtheme in theme.get("subsubthemes", {}):
            theme["subsubthemes"][subtheme] = sorted(theme["subsubthemes"][subtheme])
    output = {
        "taxonomy_version": "v1-evidence-derived",
        "status": "provisional_until_full_corpus_adjudication",
        "base_taxonomy": "data/taxonomy-v0.json",
        "derived_from": ["dac/data/adjudicated-2026-batch.jsonl", "dac/data/adjudicated-2026-batch-2.jsonl", "dac/data/adjudicated-2026-batch-3.jsonl", "iccad/data/adjudicated-2025-batch.jsonl", "isca/data/adjudicated-2026-batch.jsonl"],
        "themes": sorted(taxonomy["themes"], key=lambda theme: theme["theme_id"]),
    }
    (root / "data/taxonomy-v1-evidence.json").write_text(json.dumps(output, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return {"theme_count": len(output["themes"]), "adjudicated_records": len(adjudicated), "output": "data/taxonomy-v1-evidence.json"}


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    args = parser.parse_args()
    print(json.dumps(build(args.root), indent=2, sort_keys=True))
