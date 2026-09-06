#!/usr/bin/env python3
"""Materialize the DAC 2025 detail-page attempt without hiding access failures."""
from __future__ import annotations

import argparse
import html
import json
import re
from datetime import date
from pathlib import Path

from scripts.normalize_dac_capture_labels import normalize


TAG_RE = re.compile(r"<[^>]+>")
SPACE_RE = re.compile(r"\s+")


def clean(fragment: str) -> str:
    return SPACE_RE.sub(" ", html.unescape(TAG_RE.sub(" ", fragment))).strip()


def main(root: Path) -> dict:
    metadata = [json.loads(line) for line in (root / "dac/data/papers-2025-program.jsonl").read_text(encoding="utf-8").splitlines() if line.strip()]
    raw_dir = root / "dac/data/raw/presentations-2025"
    results = []
    for row in metadata:
        raw_path = raw_dir / f"{row['doi_or_identifier']}.html"
        result = {
            **row,
            "evidence_source_id": "dac-2025-presentation-pages",
            "evidence_url": row["program_url"],
            "evidence_collection_date": date.today().isoformat(),
            "evidence_spans": [],
            "description": None,
        }
        if not raw_path.exists():
            result.update({"capture_status": "not_captured_rate_limited", "evidence_status": "unavailable"})
        else:
            source = raw_path.read_text(encoding="utf-8", errors="replace")
            match = re.search(r'<span class="abstract">(.*?)</span>', source, re.S)
            if match and len(clean(match.group(1))) >= 100:
                description = clean(match.group(1))
                result.update({
                    "capture_status": "captured_substantive",
                    "evidence_status": "substantive_description",
                    "description": description,
                    "evidence_spans": [{"field": "description", "text": description}],
                })
            else:
                result.update({"capture_status": "captured_challenge_or_empty", "evidence_status": "unavailable"})
        results.append(normalize(result))
    output = root / "dac/data/paper-evidence-2025.jsonl"
    with output.open("w", encoding="utf-8") as handle:
        for row in results:
            handle.write(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n")
    counts = {status: sum(row["capture_status"] == status for row in results) for status in {row["capture_status"] for row in results}}
    return {"record_count": len(results), "status_counts": counts, "substantive_count": sum(row["evidence_status"] == "substantive_description" for row in results), "output": str(output)}


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    args = parser.parse_args()
    print(json.dumps(main(args.root), indent=2, sort_keys=True))
