import json
from pathlib import Path


def test_dysharp_recovery_matches_program_without_claiming_integration():
    root = Path(__file__).resolve().parents[1]
    record = json.loads((root / "isca/data/dysharp-recovery-v1.json").read_text())
    inventory = {r["paper_id"]: r for r in map(json.loads, (root / "isca/data/papers-2026-program.jsonl").read_text().splitlines())}
    paper = inventory[record["paper_id"]]
    assert paper["title"] == record["title"]
    assert paper["authors"] == record["authors"] and len(record["authors"]) == 13
    assert record["metrics"] == []
    assert record["independent_review_status"] == "pending"
    assert record["integration_status"] == "coded_primary_record_review_packet_prepared_source_text_capture_pending"
    coding = json.loads((root / "isca/data/adjudicated-2026-batch-9.jsonl").read_text())
    packet = json.loads((root / "data/review-packets/isca-2026-program-058.json").read_text())
    assert coding["paper_id"] == record["paper_id"] == packet["paper_id"]
    assert coding["metrics"] == [] and "training" in coding["workload_or_benchmark"]
    assert packet["source_text_status"] == "original_text_capture_required"
    assert not packet["independent_verdicts"]
