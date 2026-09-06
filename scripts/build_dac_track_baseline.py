#!/usr/bin/env python3
"""Build a DAC 2025 program-track baseline from captured official snippets."""
from __future__ import annotations

import argparse
import json
import re
from collections import Counter
from datetime import date
from pathlib import Path


TRACK_LABELS = {
    "ptrack101": "AI1: AI/ML Algorithms",
    "ptrack102": "AI2: AI/ML Application and Infrastructure",
    "ptrack103": "AI3: AI/ML Architecture Design",
    "ptrack104": "AI4: AI/ML System and Platform Design",
    "ptrack105": "DES1: SoC, Heterogeneous, and Reconfigurable Architectures",
    "ptrack106": "DES2A: In-memory and Near-memory Computing Circuits",
    "ptrack107": "DES2B: In-memory and Near-memory Computing Architectures, Applications and Systems",
    "ptrack108": "DES3: Emerging Models of ComputatioN",
    "ptrack109": "DES4: Digital and Analog Circuits",
    "ptrack110": "DES5: Emerging Device and Interconnect Technologies",
    "ptrack111": "DES6: Quantum Computing",
    "ptrack112": "EDA1: Design Methodologies for System-on-Chip and 3D/2.5D System-in Package",
    "ptrack113": "EDA2: Design Verification and Validation",
    "ptrack114": "EDA3: Timing Analysis and Optimization",
    "ptrack115": "EDA4: Power Analysis and Optimization",
    "ptrack116": "EDA5: RTL/Logic Level and High-level Synthesis",
    "ptrack117": "EDA6: Analog CAD, Simulation, Verification and Test",
    "ptrack118": "EDA7: Physical Design and Verification",
    "ptrack119": "EDA8: Design for Manufacturing and Reliability",
    "ptrack120": "EDA9: Design for Test and Silicon Lifecycle Management",
    "ptrack121": "SEC1: AI/ML Security/Privacy",
    "ptrack122": "SEC2: Hardware Security: Primitives & Architecture, Design & Test",
    "ptrack123": "SEC3: Hardware Security: Attack & Defense",
    "ptrack124": "SEC4: Embedded and Cross-Layer Security",
    "ptrack125": "SYS1: Autonomous Systems (Automotive, Robotics, Drones)",
    "ptrack126": "SYS2: Design of Cyber-Physical Systems and IoT",
    "ptrack127": "SYS3: Embedded Software",
    "ptrack128": "SYS4: Embedded System Design Tools and Methodologies",
    "ptrack129": "SYS5: Embedded Memory and Storage Systems",
    "ptrack130": "SYS6: Time-Critical and Fault-Tolerant System Design",
}
PRESENTATION_RE = re.compile(r'<a data-link-type="full-program_all\.program\.presentations\.(RESEARCH[^.]+)\.presentation"')


def collect(root: Path) -> dict:
    track_by_id: dict[str, list[str]] = {}
    for path in sorted((root / "dac/data/raw/program-2025").glob("*.html")):
        source = path.read_text(encoding="utf-8", errors="replace")
        current_tracks: list[str] = []
        token_re = re.compile(r'ptracks="([^"]+)"|' + PRESENTATION_RE.pattern)
        for match in token_re.finditer(source):
            if match.group(1):
                current_tracks = match.group(1).split()
            elif match.group(2):
                track_by_id[match.group(2)] = current_tracks[:]
    rows = []
    for line in (root / "dac/data/papers-2025-program.jsonl").read_text(encoding="utf-8").splitlines():
        row = json.loads(line)
        identifier = row["doi_or_identifier"]
        ids = track_by_id.get(identifier, [])
        rows.append({"paper_id": row["paper_id"], "presentation_id": identifier, "title": row["title"], "track_ids": ids, "track_labels": [TRACK_LABELS.get(item, f"unmapped:{item}") for item in ids]})
    counts = Counter(track for row in rows for track in row["track_ids"] if track in TRACK_LABELS)
    output = root / "dac/data/track-baseline-2025.json"
    output.write_text(json.dumps({"schema": "dac-program-track-baseline.v1", "conference_id": "dac", "edition": 2025, "source_id": "dac-2025-program", "capture_date": date.today().isoformat(), "record_count": len(rows), "records_with_track_assignment": sum(bool(row["track_ids"]) for row in rows), "track_counts": dict(sorted(counts.items())), "track_labels": TRACK_LABELS, "records": rows, "limits": "Provider program-track assignments only; not paper abstracts, technical evidence, prevalence, or causal trend evidence."}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return {"record_count": len(rows), "records_with_track_assignment": sum(bool(row["track_ids"]) for row in rows), "track_count": len(counts), "output": str(output)}


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    args = parser.parse_args()
    print(json.dumps(collect(args.root), indent=2, sort_keys=True))
