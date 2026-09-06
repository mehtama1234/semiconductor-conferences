import json
from pathlib import Path

from scripts.build_evidence_summary import read_jsonl

ROOT = Path(__file__).resolve().parents[1]


def test_current_drafts_preserve_identity_and_numeric_disagreement():
    rows = read_jsonl(ROOT / "data/current-description-coding-v1.jsonl")
    sources = {r["paper_id"]: r for r in read_jsonl(ROOT / "dac/data/paper-evidence-2026.jsonl")}
    branches = {r["theme_id"]: r["subthemes"] for r in json.loads((ROOT / "data/taxonomy-v1-evidence.json").read_text())["themes"]}
    assert len(rows) == len({r["paper_id"] for r in rows}) == 4
    for row in rows:
        for key in ["title", "evidence_url", "analysis_edition", "evidence_collection_date"]:
            assert row[key] == sources[row["paper_id"]][key]
        assert row["subtheme_id"] in branches[row["theme_id"]]
        assert row["independent_review_status"] == "pending"
        assert row["subsubtheme_id"] is None
        assert row["limits"]
    atb = next(r for r in rows if r["paper_id"] == "dac-2026-research1000")
    assert atb["metrics"][0]["value"] == 4.54
    assert atb["metrics"][1]["value"] == [4.8, 24.6]
    assert "inconsistency" in atb["metrics"][0]["qualifier"]
    assert all(r["metrics"] == [] for r in rows if r != atb)
