import json
import copy
import pytest
from pathlib import Path

from scripts.build_draft_review_packets import build, validate_draft
from scripts.build_evidence_summary import read_jsonl
from scripts.build_review_packets import digest

ROOT = Path(__file__).resolve().parents[1]


def test_draft_packets_are_source_separated_and_reproducible():
    packets = build(ROOT)
    assert packets == read_jsonl(ROOT / "data/draft-review-packets-v1.jsonl")
    assert len(packets) == len({p["paper_id"] for p in packets}) == 466
    assert sum(p["record_under_review"]["analysis_edition"] == 2025 for p in packets) == 24
    for packet in packets:
        assert packet["independent_verdicts"] == []
        assert packet["review_status"] == "not_reviewed"
        assert packet["original_source_sha256"] == digest(packet["original_source_text"])
        assert packet["record_sha256"] == digest(json.dumps(packet["record_under_review"], sort_keys=True, ensure_ascii=False))
        assert packet["original_source_text"] != packet["record_under_review"]["method_or_artifact"]
        assert packet["source_locator"]["field"] == "description"
        assert packet["original_source_id"] == f"dac-{packet['record_under_review']['analysis_edition']}-presentation-pages"


@pytest.mark.parametrize("mutation", ["identity", "edition", "tier", "review", "taxonomy", "limits", "metric"])
def test_draft_builder_rejects_evidence_boundary_regressions(mutation):
    draft = copy.deepcopy(read_jsonl(ROOT / "data/current-description-coding-v1.jsonl")[0])
    source = next(r for r in read_jsonl(ROOT / "dac/data/paper-evidence-2026.jsonl") if r["paper_id"] == draft["paper_id"])
    branches = {r["theme_id"]: r for r in json.loads((ROOT / "data/taxonomy-v1-evidence.json").read_text())["themes"]}
    if mutation == "identity":
        draft["title"] = "Wrong paper"
    elif mutation == "edition":
        draft["analysis_edition"] = 2025
    elif mutation == "tier":
        draft["source_tier"] = "full_paper"
    elif mutation == "review":
        draft["independent_review_status"] = "accepted"
    elif mutation == "taxonomy":
        draft["subtheme_id"] = "nonexistent"
    elif mutation == "limits":
        draft["limits"] = []
    else:
        draft["metrics"][0].pop("condition")
    with pytest.raises(ValueError):
        validate_draft(draft, source, branches)
