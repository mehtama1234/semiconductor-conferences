import json
from pathlib import Path

import pytest

from scripts.normalize_dac_capture_labels import normalize

ROOT = Path(__file__).resolve().parents[1]


def test_capture_labels_preserve_provenance_and_are_idempotent():
    row = {"paper_id": "example", "description": "evidence " * 20,
           "evidence_status": "substantive_description", "record_status": "metadata_only",
           "access_status": "metadata_only", "limits": "inventory only",
           "evidence_collection_date": "2026-09-06", "metrics": [], "problem": None}
    result = normalize(row)
    assert result["record_status"] == "official_description_captured"
    assert result["inventory_origin_labels"]["limits"] == "inventory only"
    assert normalize(result) == result
    assert row["record_status"] == "metadata_only"
    for key in ["description", "evidence_collection_date", "metrics", "problem"]:
        assert row[key] == result[key]
    unavailable = {**row, "evidence_status": "unavailable", "description": None}
    assert normalize(unavailable) == unavailable
    with pytest.raises(ValueError, match="without description"):
        normalize({**row, "description": None})


def test_saved_capture_labels_match_evidence_without_promoting_coding():
    for year, expected in [(2025, 24), (2026, 543)]:
        rows = [json.loads(x) for x in (ROOT / f"dac/data/paper-evidence-{year}.jsonl").read_text().splitlines()]
        captured = [r for r in rows if r["evidence_status"] == "substantive_description"]
        assert len(captured) == expected
        for row in captured:
            assert row == normalize(row)
            assert row["access_status"] == "official_description_available"
            assert "metadata_only" in row["inventory_origin_labels"]["access_status"]
            assert row.get("problem") is None
