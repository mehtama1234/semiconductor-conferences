import json
from pathlib import Path
from collections import defaultdict

from scripts.build_evidence_summary import read_jsonl
from scripts.collect_isca_crossref_metadata import title_key

ROOT = Path(__file__).resolve().parents[1]


def test_temporal_drafts_resolve_to_equivalent_source_tiers():
    rows = read_jsonl(ROOT / "data/temporal-comparative-coding-v1.jsonl")
    sources = {r["paper_id"]: r for year in [2025, 2026] for r in read_jsonl(ROOT / f"dac/data/paper-evidence-{year}.jsonl")}
    taxonomy = json.loads((ROOT / "data/taxonomy-v1-evidence.json").read_text())
    branches = {r["theme_id"]: r["subthemes"] for r in taxonomy["themes"]}
    pairs = defaultdict(set)
    assert len(rows) == len({r["paper_id"] for r in rows})
    for row in rows:
        source = sources[row["paper_id"]]
        assert title_key(source["title"]) == title_key(row["title"])
        assert source["evidence_url"] == row["evidence_url"]
        assert source["evidence_status"] == "substantive_description"
        assert row["analysis_edition"] == source["analysis_edition"]
        assert row["subtheme_id"] in branches[row["theme_id"]]
        assert row["independent_review_status"] == "pending"
        assert row["limits"]
        pairs[row["pair_id"]].add(row["analysis_edition"])
    assert all(editions == {2025, 2026} for editions in pairs.values())
    # An unreported result must remain missing, not become a zero-valued metric.
    assert next(r for r in rows if r["paper_id"] == "dac-2025-research1048")["metrics"] == []
