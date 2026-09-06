import json
from pathlib import Path

import pytest

from scripts.normalize_dac_capture_labels import normalize, link_presentation_source

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
            assert row["evidence_source_id"] == f"dac-{year}-presentation-pages"


@pytest.mark.parametrize("mutation", [None, "host", "edition", "paper_id", "registry", "existing_id"])
def test_missing_source_link_requires_exact_registered_presentation(mutation):
    row = {"paper_id": "dac-2026-research004", "conference_id": "dac", "analysis_edition": 2026,
           "evidence_status": "substantive_description", "doi_or_identifier": "RESEARCH004",
           "evidence_url": "https://63dac.conference-program.com/?id=RESEARCH004"}
    registry = {"dac-2026-presentation-pages": {"url": "https://63dac.conference-program.com/"}}
    if mutation == "host":
        row["evidence_url"] = "https://example.com/?id=RESEARCH004"
    elif mutation == "edition":
        row["analysis_edition"] = 2025
    elif mutation == "paper_id":
        row["doi_or_identifier"] = "RESEARCH999"
    elif mutation == "registry":
        registry = {}
    elif mutation == "existing_id":
        row["evidence_source_id"] = "unrelated-source"
    if mutation:
        with pytest.raises(ValueError, match="identity mismatch"):
            link_presentation_source(row, registry)
    else:
        result = link_presentation_source(row, registry)
        assert result["evidence_source_id"] == "dac-2026-presentation-pages"
        assert link_presentation_source(result, registry) == result
