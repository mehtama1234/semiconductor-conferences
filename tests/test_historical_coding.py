import json
from pathlib import Path

from scripts.build_evidence_summary import read_jsonl

ROOT = Path(__file__).resolve().parents[1]


def test_historical_drafts_preserve_source_identity_and_uncertainty():
    sources = {r["paper_id"]: r for r in read_jsonl(ROOT / "dac/data/paper-evidence-2025.jsonl")}
    rows = read_jsonl(ROOT / "data/historical-description-coding-v1.jsonl")
    branches = {r["theme_id"]: r["subthemes"] for r in json.loads((ROOT / "data/taxonomy-v1-evidence.json").read_text())["themes"]}
    assert len(rows) == len({r["paper_id"] for r in rows}) == 6
    for row in rows:
        source = sources[row["paper_id"]]
        for key in ["title", "analysis_edition", "evidence_url", "evidence_collection_date", "evidence_source_id"]:
            assert row[key] == source[key]
        assert source["evidence_status"] == "substantive_description"
        assert row["source_locator"]["field"] == "description"
        assert row["source_tier"] == "official_description"
        assert row["subtheme_id"] in branches[row["theme_id"]]
        assert row["subsubtheme_id"] is None  # New mechanism labels are not approved IDs.
        assert row["independent_review_status"] == "pending"
        assert row["limits"] and row["classification_rationale"]
        assert all(metric["condition"] and metric["qualifier"] for metric in row["metrics"])
    by_id = {r["paper_id"]: r for r in rows}
    assert by_id["dac-2025-research002"]["metrics"] == []
    assert by_id["dac-2025-research024"]["metrics"] == []
    assert by_id["dac-2025-research021"]["hardware_or_process_assumptions"] is None
