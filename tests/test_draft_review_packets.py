import json
from pathlib import Path

from scripts.build_draft_review_packets import build
from scripts.build_evidence_summary import read_jsonl
from scripts.build_review_packets import digest

ROOT = Path(__file__).resolve().parents[1]


def test_draft_packets_are_source_separated_and_reproducible():
    packets = build(ROOT)
    assert packets == read_jsonl(ROOT / "data/draft-review-packets-v1.jsonl")
    assert len(packets) == len({p["paper_id"] for p in packets}) == 27
    assert sum(p["record_under_review"]["analysis_edition"] == 2025 for p in packets) == 24
    for packet in packets:
        assert packet["independent_verdicts"] == []
        assert packet["review_status"] == "not_reviewed"
        assert packet["original_source_sha256"] == digest(packet["original_source_text"])
        assert packet["record_sha256"] == digest(json.dumps(packet["record_under_review"], sort_keys=True, ensure_ascii=False))
        assert packet["original_source_text"] != packet["record_under_review"]["method_or_artifact"]
        assert packet["source_locator"]["field"] == "description"
