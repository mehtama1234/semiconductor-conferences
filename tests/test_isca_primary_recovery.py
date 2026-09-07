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
    assert record["integration_status"] == "recovered_primary_checkpoint_not_yet_in_coded_or_review_packet_ledgers"
