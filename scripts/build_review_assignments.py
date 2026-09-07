#!/usr/bin/env python3
"""Build a deterministic reviewer-assignment manifest without creating verdicts."""
from __future__ import annotations

import argparse
import json
from pathlib import Path


def build(root: Path) -> dict:
    packet_dir = root / "data/review-packets"
    packets = [json.loads(path.read_text(encoding="utf-8")) for path in sorted(packet_dir.glob("*.json"))]
    assignments = []
    for packet in packets:
        assignments.append({
            "paper_id": packet["paper_id"],
            "packet_path": str((Path("data/review-packets") / f"{packet['paper_id']}.json")),
            "reviewer_slots": ["reviewer_a", "reviewer_b"],
            "source_text_status": packet.get("source_text_status"),
            "review_status": "awaiting_external_review",
            "verdicts": [],
        })
    return {
        "schema": "independent-review-assignments.v1",
        "as_of": "2026-09-07",
        "status": "prepared_awaiting_external_review",
        "assignment_policy": "Two independent reviewers per packet; keep source-entailment decisions blind until disagreement resolution.",
        "packet_count": len(assignments),
        "source_capture_required_count": sum(item["source_text_status"] == "original_text_capture_required" for item in assignments),
        "independent_verdict_count": 0,
        "assignments": assignments,
        "limits": [
            "Reviewer slots are placeholders, not claims that reviewers have accepted an assignment.",
            "This manifest creates no scientific verdicts and does not replace the judge protocol.",
        ],
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    args = parser.parse_args()
    output = args.root / "reports/independent-review-assignments-v1.json"
    output.write_text(json.dumps(build(args.root), indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"path": str(output), "packet_count": build(args.root)["packet_count"]}, indent=2))
