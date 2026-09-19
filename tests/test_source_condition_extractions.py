import json
from pathlib import Path

from scripts.build_source_condition_extractions import build


ROOT = Path(__file__).resolve().parents[1]


def test_source_condition_extraction_batch_is_source_located() -> None:
    result = build(ROOT)
    rows = [json.loads(line) for line in (ROOT / "data/direction-condition-extractions-v1.jsonl").read_text().splitlines()]
    assert result["schema"] == "source-condition-extraction-batch.v1"
    assert result["record_count"] == len(rows) == 9
    assert all(row["evidence_tier"] == "official_description" for row in rows)
    assert all(row["source_locators"] and row["evidence_url"] for row in rows)
    assert all(row["independent_review_status"] == "pending" for row in rows)
