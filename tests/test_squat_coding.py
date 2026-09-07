import json
from pathlib import Path

from scripts.build_evidence_summary import PATHS
from scripts.build_review_packets import build

ROOT = Path(__file__).resolve().parents[1]


def test_squat_coding_and_packet_preserve_conditions_and_pending_review():
    path = "iccad/data/adjudicated-2025-batch-4.jsonl"
    assert path in PATHS
    row = json.loads((ROOT / path).read_text())
    sources = {r["source_id"]: r for r in map(json.loads, (ROOT / "iccad/data/sources.jsonl").read_text().splitlines())}
    assert sources[row["evidence_source_id"]]["url"] == row["evidence_url"]
    inventory = {r["paper_id"]: r for r in map(json.loads, (ROOT / "iccad/data/papers-2025-program.jsonl").read_text().splitlines())}
    assert inventory[row["paper_id"]]["title"] == row["title"]
    assert row["analysis_edition"] == 2025 and row["target_edition"] == 2026
    assert row["metrics"] == [] and row["independent_review_status"] == "pending"
    assert "iso-accuracy" in row["limits"] and "rounding" in row["limits"]
    assert row["evidence_locators"]
    packets, _ = build(ROOT)
    packet = next(p for p in packets if p["paper_id"] == row["paper_id"])
    assert packet["original_source_text"]
    assert packet["source_text_status"] == "captured_original_abstract"
    assert not packet["independent_verdicts"]
    assert packet["supplementary_researcher_assessments"]
