#!/usr/bin/env python3
"""Validate the initial semiconductor-conference research scaffold."""
from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def read_jsonl(path: Path) -> list[dict]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def validate(root: Path = ROOT) -> dict:
    register = json.loads((root / "data/conference-register.json").read_text(encoding="utf-8"))
    taxonomy = json.loads((root / "data/taxonomy-v0.json").read_text(encoding="utf-8"))
    conferences = register["conferences"]
    checks = {
        "three_conferences_registered": len(conferences) == 3,
        "conference_folders_present": all((root / item["folder"]).is_dir() for item in conferences),
        "taxonomy_has_themes": bool(taxonomy.get("themes")) and len(taxonomy["themes"]) == 10,
        "each_conference_has_source_ledger": all((root / item["folder"] / "data/sources.jsonl").exists() for item in conferences),
        "paper_seed_records_valid": all(row.get("paper_id") and row.get("conference_id") and row.get("title") and row.get("publisher_url") for row in read_jsonl(root / "dac/data/papers.jsonl")),
        "iccad_target_and_fallback_explicit": register["conferences"][2].get("target_edition") == "2026" and register["conferences"][2].get("paper_analysis_edition") == "2025",
    }
    return {"contract": "semiconductor-conference-scaffold.v1", "status": "passed" if all(checks.values()) else "failed", "checks": checks, "conference_count": len(conferences), "taxonomy_theme_count": len(taxonomy.get("themes", []))}


if __name__ == "__main__":
    result = validate()
    print(json.dumps(result, indent=2, sort_keys=True))
    raise SystemExit(0 if result["status"] == "passed" else 1)
