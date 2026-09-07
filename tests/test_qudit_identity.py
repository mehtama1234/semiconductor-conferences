import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_qudit_identity_resolution_does_not_promote_abstract_to_full_text():
    record = json.loads((ROOT / "iccad/data/qudit-primary-recovery-v1.json").read_text())
    identity = record["identity"]
    mapping = identity["institutional_reconciliation"]
    sources = {r["source_id"]: r for r in map(json.loads, (ROOT / "iccad/data/sources.jsonl").read_text().splitlines())}
    source = sources[mapping["source_id"]]
    assert source["url"] == mapping["url"]
    assert source["title"] == record["title"]
    assert mapping["doi"] == identity["author_linked_doi"]
    assert len(mapping["matched_fields"]) == 3
    assert len(mapping["raw_html_sha256"]) == len(mapping["abstract_sha256"]) == 64
    assert "Architecture" in identity["observed_title"] and "System" in record["title"]
    assert mapping["full_text_recovered"] is False
    assert record["source_tier"] == "author_posted_abstract"
    assert record["independent_review_status"] == "pending"
