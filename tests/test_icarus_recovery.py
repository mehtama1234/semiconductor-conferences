import json
from pathlib import Path

from scripts.build_evidence_summary import read_jsonl

ROOT = Path(__file__).resolve().parents[1]


def test_icarus_discovery_does_not_promote_evidence_or_acceptance():
    row = json.loads((ROOT / "dac/data/icarus-source-recovery-20260906.json").read_text())
    source = next(r for r in read_jsonl(ROOT / "dac/data/sources.jsonl") if r["source_id"] == row["source_id"])
    draft = next(r for r in read_jsonl(ROOT / "data/temporal-comparative-coding-v1.jsonl") if r["paper_id"] == row["paper_id"])
    assert row["title"] == draft["title"]
    assert row["commit"] in source["url"]
    assert draft["source_tier"] == "official_description"
    assert row["independent_review_status"] == "pending"
    assert row["demo_executed"] is False
    assert row["tree_truncated"] is False
    assert len(row["readme_sha256"]) == 64
    assert row["unresolved"] and row["revisit_conditions"]
