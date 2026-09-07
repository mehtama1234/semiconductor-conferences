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
    adjudicated = rows(root / "dac/data/adjudicated-2026-batch.jsonl") + rows(root / "dac/data/adjudicated-2026-batch-2.jsonl") + rows(root / "dac/data/adjudicated-2026-batch-3.jsonl") + rows(root / "dac/data/adjudicated-2026-batch-4.jsonl") + rows(root / "iccad/data/adjudicated-2025-batch.jsonl") + rows(root / "iccad/data/adjudicated-2025-batch-2.jsonl") + rows(root / "isca/data/adjudicated-2026-batch.jsonl") + rows(root / "isca/data/adjudicated-2026-batch-2.jsonl") + rows(root / "isca/data/adjudicated-2026-batch-3.jsonl") + rows(root / "isca/data/adjudicated-2026-batch-4.jsonl") + rows(root / "isca/data/adjudicated-2026-batch-5.jsonl") + rows(root / "isca/data/adjudicated-2026-batch-6.jsonl") + rows(root / "isca/data/adjudicated-2026-batch-7.jsonl") + rows(root / "isca/data/adjudicated-2026-batch-8.jsonl")
    adjudicated = rows(root / "dac/data/adjudicated-2025-batch.jsonl") + adjudicated
    adjudicated += rows(root / "dac/data/adjudicated-2026-batch-5.jsonl")
    adjudicated += rows(root / "dac/data/adjudicated-2026-batch-6.jsonl")
    adjudicated += rows(root / "dac/data/adjudicated-2026-batch-7.jsonl")
    adjudicated += rows(root / "dac/data/adjudicated-2026-batch-8.jsonl")
    adjudicated += rows(root / "dac/data/adjudicated-2026-batch-9.jsonl")
    adjudicated += rows(root / "dac/data/adjudicated-2026-batch-10.jsonl")
    adjudicated += rows(root / "dac/data/adjudicated-2026-batch-11.jsonl")
    adjudicated += rows(root / "dac/data/adjudicated-2026-batch-12.jsonl")
    adjudicated += rows(root / "dac/data/adjudicated-2026-batch-13.jsonl")
    adjudicated += rows(root / "dac/data/adjudicated-2026-batch-14.jsonl")
    adjudicated += rows(root / "dac/data/adjudicated-2026-batch-15.jsonl")
    adjudicated += rows(root / "dac/data/adjudicated-2026-batch-16.jsonl")
    adjudicated += rows(root / "dac/data/adjudicated-2026-batch-17.jsonl")
    adjudicated += rows(root / "dac/data/adjudicated-2026-batch-18.jsonl")
    adjudicated += rows(root / "dac/data/adjudicated-2026-batch-19.jsonl")
    adjudicated += rows(root / "dac/data/adjudicated-2026-batch-20.jsonl")
    adjudicated += rows(root / "dac/data/adjudicated-2026-batch-21.jsonl")
    adjudicated += rows(root / "dac/data/adjudicated-2026-batch-22.jsonl")
    adjudicated += rows(root / "dac/data/adjudicated-2026-batch-23.jsonl")
    adjudicated += rows(root / "dac/data/adjudicated-2026-batch-24.jsonl")
    adjudicated += rows(root / "dac/data/adjudicated-2026-batch-25.jsonl")
    adjudicated += rows(root / "dac/data/adjudicated-2026-batch-26.jsonl")
    adjudicated += rows(root / "dac/data/adjudicated-2026-batch-27.jsonl")
    adjudicated += rows(root / "dac/data/adjudicated-2026-batch-28.jsonl")
    adjudicated += rows(root / "dac/data/adjudicated-2026-batch-29.jsonl")
    adjudicated += rows(root / "dac/data/adjudicated-2026-batch-30.jsonl")
    adjudicated += rows(root / "dac/data/adjudicated-2026-batch-31.jsonl")
    adjudicated += rows(root / "dac/data/adjudicated-2026-batch-32.jsonl")
    adjudicated += rows(root / "dac/data/adjudicated-2026-batch-33.jsonl")
    adjudicated += rows(root / "dac/data/adjudicated-2026-batch-34.jsonl")
    adjudicated += rows(root / "dac/data/adjudicated-2026-batch-35.jsonl")
    adjudicated += rows(root / "dac/data/adjudicated-2026-batch-36.jsonl")
    adjudicated += rows(root / "dac/data/adjudicated-2026-batch-37.jsonl")
    adjudicated += rows(root / "dac/data/adjudicated-2026-batch-38.jsonl")
    adjudicated += rows(root / "dac/data/adjudicated-2026-batch-39.jsonl")
    adjudicated += rows(root / "dac/data/adjudicated-2026-batch-40.jsonl")
    adjudicated += rows(root / "dac/data/adjudicated-2026-batch-41.jsonl")
    adjudicated += rows(root / "dac/data/adjudicated-2026-batch-42.jsonl")
    adjudicated += rows(root / "dac/data/adjudicated-2026-batch-43.jsonl")
    adjudicated += rows(root / "dac/data/adjudicated-2026-batch-44.jsonl")
    adjudicated += rows(root / "dac/data/adjudicated-2026-batch-45.jsonl")
    adjudicated += rows(root / "dac/data/adjudicated-2026-batch-46.jsonl")
    adjudicated += rows(root / "dac/data/adjudicated-2026-batch-47.jsonl")
    adjudicated += rows(root / "dac/data/adjudicated-2026-batch-48.jsonl")
    adjudicated += rows(root / "dac/data/adjudicated-2026-batch-49.jsonl")
    adjudicated += rows(root / "dac/data/adjudicated-2026-batch-50.jsonl")
    adjudicated += rows(root / "dac/data/adjudicated-2026-batch-51.jsonl")
    adjudicated += rows(root / "dac/data/adjudicated-2026-batch-52.jsonl")
    adjudicated += rows(root / "dac/data/adjudicated-2026-batch-53.jsonl")
    adjudicated += rows(root / "dac/data/adjudicated-2026-batch-54.jsonl")
    adjudicated += rows(root / "isca/data/adjudicated-2026-batch-9.jsonl")
    adjudicated += rows(root / "isca/data/adjudicated-2026-batch-10.jsonl")
    adjudicated += rows(root / "iccad/data/adjudicated-2025-batch-3.jsonl")
    adjudicated += rows(root / "iccad/data/adjudicated-2025-batch-4.jsonl")
    adjudicated += rows(root / "iccad/data/adjudicated-2025-batch-5.jsonl")
    adjudicated += rows(root / "iccad/data/adjudicated-2025-batch-6.jsonl")
    adjudicated += rows(root / "iccad/data/adjudicated-2025-batch-7.jsonl")
    adjudicated += rows(root / "iccad/data/adjudicated-2025-batch-8.jsonl")
    adjudicated += rows(root / "iccad/data/adjudicated-2025-batch-9.jsonl")
    adjudicated += rows(root / "iccad/data/adjudicated-2025-batch-10.jsonl")
    adjudicated += rows(root / "iccad/data/adjudicated-2025-batch-11.jsonl")
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
        "derived_from": ["dac/data/adjudicated-2026-batch.jsonl", "dac/data/adjudicated-2026-batch-2.jsonl", "dac/data/adjudicated-2026-batch-3.jsonl", "dac/data/adjudicated-2026-batch-4.jsonl", "iccad/data/adjudicated-2025-batch.jsonl", "iccad/data/adjudicated-2025-batch-2.jsonl", "isca/data/adjudicated-2026-batch.jsonl", "isca/data/adjudicated-2026-batch-2.jsonl", "isca/data/adjudicated-2026-batch-3.jsonl", "isca/data/adjudicated-2026-batch-4.jsonl", "isca/data/adjudicated-2026-batch-5.jsonl", "isca/data/adjudicated-2026-batch-6.jsonl", "isca/data/adjudicated-2026-batch-7.jsonl", "isca/data/adjudicated-2026-batch-8.jsonl"],
        "themes": sorted(taxonomy["themes"], key=lambda theme: theme["theme_id"]),
    }
    output["derived_from"].append("isca/data/adjudicated-2026-batch-9.jsonl")
    output["derived_from"].append("isca/data/adjudicated-2026-batch-10.jsonl")
    output["derived_from"].append("dac/data/adjudicated-2026-batch-5.jsonl")
    output["derived_from"].append("dac/data/adjudicated-2026-batch-6.jsonl")
    output["derived_from"].append("dac/data/adjudicated-2026-batch-7.jsonl")
    output["derived_from"].append("dac/data/adjudicated-2026-batch-8.jsonl")
    output["derived_from"].append("dac/data/adjudicated-2026-batch-9.jsonl")
    output["derived_from"].append("dac/data/adjudicated-2026-batch-10.jsonl")
    output["derived_from"].append("dac/data/adjudicated-2026-batch-11.jsonl")
    output["derived_from"].append("dac/data/adjudicated-2026-batch-12.jsonl")
    output["derived_from"].append("dac/data/adjudicated-2026-batch-13.jsonl")
    output["derived_from"].append("dac/data/adjudicated-2026-batch-14.jsonl")
    output["derived_from"].append("dac/data/adjudicated-2026-batch-15.jsonl")
    output["derived_from"].append("dac/data/adjudicated-2026-batch-16.jsonl")
    output["derived_from"].append("dac/data/adjudicated-2026-batch-17.jsonl")
    output["derived_from"].append("dac/data/adjudicated-2026-batch-18.jsonl")
    output["derived_from"].append("dac/data/adjudicated-2026-batch-19.jsonl")
    output["derived_from"].append("dac/data/adjudicated-2026-batch-20.jsonl")
    output["derived_from"].append("dac/data/adjudicated-2026-batch-21.jsonl")
    output["derived_from"].append("dac/data/adjudicated-2026-batch-22.jsonl")
    output["derived_from"].append("dac/data/adjudicated-2026-batch-23.jsonl")
    output["derived_from"].append("dac/data/adjudicated-2026-batch-24.jsonl")
    output["derived_from"].append("dac/data/adjudicated-2026-batch-25.jsonl")
    output["derived_from"].append("dac/data/adjudicated-2026-batch-26.jsonl")
    output["derived_from"].append("dac/data/adjudicated-2026-batch-27.jsonl")
    output["derived_from"].append("dac/data/adjudicated-2026-batch-28.jsonl")
    output["derived_from"].append("dac/data/adjudicated-2026-batch-29.jsonl")
    output["derived_from"].append("dac/data/adjudicated-2026-batch-30.jsonl")
    output["derived_from"].append("dac/data/adjudicated-2026-batch-31.jsonl")
    output["derived_from"].append("dac/data/adjudicated-2026-batch-32.jsonl")
    output["derived_from"].append("dac/data/adjudicated-2026-batch-33.jsonl")
    output["derived_from"].append("dac/data/adjudicated-2026-batch-34.jsonl")
    output["derived_from"].append("dac/data/adjudicated-2026-batch-35.jsonl")
    output["derived_from"].append("dac/data/adjudicated-2026-batch-36.jsonl")
    output["derived_from"].append("dac/data/adjudicated-2026-batch-37.jsonl")
    output["derived_from"].append("dac/data/adjudicated-2026-batch-38.jsonl")
    output["derived_from"].append("dac/data/adjudicated-2026-batch-39.jsonl")
    output["derived_from"].append("dac/data/adjudicated-2026-batch-40.jsonl")
    output["derived_from"].append("dac/data/adjudicated-2026-batch-41.jsonl")
    output["derived_from"].append("dac/data/adjudicated-2026-batch-42.jsonl")
    output["derived_from"].append("dac/data/adjudicated-2026-batch-43.jsonl")
    output["derived_from"].append("dac/data/adjudicated-2026-batch-44.jsonl")
    output["derived_from"].append("dac/data/adjudicated-2026-batch-45.jsonl")
    output["derived_from"].append("dac/data/adjudicated-2026-batch-46.jsonl")
    output["derived_from"].append("dac/data/adjudicated-2026-batch-47.jsonl")
    output["derived_from"].append("dac/data/adjudicated-2026-batch-48.jsonl")
    output["derived_from"].append("dac/data/adjudicated-2026-batch-49.jsonl")
    output["derived_from"].append("dac/data/adjudicated-2026-batch-50.jsonl")
    output["derived_from"].append("dac/data/adjudicated-2026-batch-51.jsonl")
    output["derived_from"].append("dac/data/adjudicated-2026-batch-52.jsonl")
    output["derived_from"].append("dac/data/adjudicated-2026-batch-53.jsonl")
    output["derived_from"].append("dac/data/adjudicated-2026-batch-54.jsonl")
    output["derived_from"].append("iccad/data/adjudicated-2025-batch-3.jsonl")
    output["derived_from"].append("iccad/data/adjudicated-2025-batch-4.jsonl")
    output["derived_from"].append("iccad/data/adjudicated-2025-batch-5.jsonl")
    output["derived_from"].append("iccad/data/adjudicated-2025-batch-6.jsonl")
    output["derived_from"].append("iccad/data/adjudicated-2025-batch-7.jsonl")
    output["derived_from"].append("iccad/data/adjudicated-2025-batch-8.jsonl")
    output["derived_from"].append("iccad/data/adjudicated-2025-batch-9.jsonl")
    output["derived_from"].append("iccad/data/adjudicated-2025-batch-10.jsonl")
    output["derived_from"].append("iccad/data/adjudicated-2025-batch-11.jsonl")
    (root / "data/taxonomy-v1-evidence.json").write_text(json.dumps(output, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return {"theme_count": len(output["themes"]), "adjudicated_records": len(adjudicated), "output": "data/taxonomy-v1-evidence.json"}


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    args = parser.parse_args()
    print(json.dumps(build(args.root), indent=2, sort_keys=True))
