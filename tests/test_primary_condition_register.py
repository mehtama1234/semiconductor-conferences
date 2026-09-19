import json
from pathlib import Path

from scripts.build_primary_condition_register import build


ROOT = Path(__file__).resolve().parents[1]


def test_primary_condition_register_surfaces_existing_assessments() -> None:
    result = build(ROOT)
    rows = [json.loads(line) for line in (ROOT / "data/primary-condition-assessments-v1.jsonl").read_text().splitlines()]
    assert result["schema"] == "primary-condition-assessment-register.v1"
    assert result["record_count"] == len(rows) == 5
    assert all(row["assessment_path"] and row["source_url"] for row in rows)
    assert all(row["independent_review_status"] == "pending" for row in rows)
    assert any(row["condition_payload"] for row in rows)
