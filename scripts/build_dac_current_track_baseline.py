#!/usr/bin/env python3
"""Preserve DAC 2026 provider track IDs when their labels are unresolved."""
from __future__ import annotations

import argparse
import json
import re
from collections import Counter
from datetime import date
from pathlib import Path


PRESENTATION_RE = re.compile(r'<a data-link-type="full-program_all\.program\.presentations\.(RESEARCH[^.]+)\.presentation"')


def collect(root: Path) -> dict:
    track_by_id: dict[str, list[str]] = {}
    for path in sorted((root / "dac/data/raw/program").glob("*.html")):
        source = path.read_text(encoding="utf-8", errors="replace")
        current_tracks: list[str] = []
        for match in re.finditer(r'ptracks="([^"]+)"|' + PRESENTATION_RE.pattern, source):
            if match.group(1):
                current_tracks = match.group(1).split()
            elif match.group(2):
                track_by_id[match.group(2)] = current_tracks[:]
    rows = []
    for line in (root / "dac/data/papers-2026-program.jsonl").read_text(encoding="utf-8").splitlines():
        row = json.loads(line)
        ids = track_by_id.get(row["doi_or_identifier"].replace("dac-2026-", ""), [])
        rows.append({"paper_id": row["paper_id"], "presentation_id": row["doi_or_identifier"], "title": row["title"], "track_ids": ids})
    counts = Counter(track for row in rows for track in row["track_ids"])
    output = root / "dac/data/track-baseline-2026.json"
    output.write_text(json.dumps({"schema": "dac-program-track-baseline.v1", "conference_id": "dac", "edition": 2026, "source_id": "dac-2026-program", "capture_date": date.today().isoformat(), "record_count": len(rows), "records_with_track_assignment": sum(bool(row["track_ids"]) for row in rows), "track_counts": dict(sorted(counts.items())), "unresolved_track_ids": sorted(counts), "records": rows, "limits": "Captured provider track IDs only; labels were not present in the preserved 2026 snippet responses, so no 2025 label equivalence is asserted. This is not paper-level technical evidence."}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return {"record_count": len(rows), "records_with_track_assignment": sum(bool(row["track_ids"]) for row in rows), "track_count": len(counts), "output": str(output)}


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    args = parser.parse_args()
    print(json.dumps(collect(args.root), indent=2, sort_keys=True))
