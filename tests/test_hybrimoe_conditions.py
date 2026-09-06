import json
from pathlib import Path

from scripts.build_evidence_summary import read_jsonl

ROOT = Path(__file__).resolve().parents[1]


def test_hybrimoe_primary_conditions_are_separate_and_source_linked():
    record = json.loads((ROOT / "dac/data/hybrimoe-primary-conditions-v1.json").read_text())
    source = next(r for r in read_jsonl(ROOT / "dac/data/sources.jsonl") if r["source_id"] == record["source_id"])
    draft = next(r for r in read_jsonl(ROOT / "data/temporal-comparative-coding-v1.jsonl") if r["paper_id"] == record["paper_id"])
    assert record["source_url"] == source["url"]
    assert record["title"] == draft["title"]
    assert record["independent_review_status"] == "pending"
    assert draft["source_tier"] == "official_description"
    assert record["conditions"]["hardware"]["cpu_cores_used"] == 10
    assert all(m["baseline"] == "kTransformers" and m["qualifier"] == "average" and m["locator"] for m in record["metrics"])
    assert record["remaining_unknowns"]
    assert len(record["raw_sha256"]) == 64
