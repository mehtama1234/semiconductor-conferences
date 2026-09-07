import hashlib
import json
from pathlib import Path

import pytest

from scripts.primary_supplements import load, validate
from scripts.build_review_packets import build as build_packets
from scripts.build_draft_review_packets import build as build_drafts
from scripts.build_work_queue import build as build_queue

ROOT = Path(__file__).resolve().parents[1]


def test_supplements_reach_queue_and_both_packet_types_without_promotion():
    supplements = load(ROOT)
    assert set(supplements) == {"dac-2026-research031", "dac-2026-research043", "dac-2026-research046", "dac-2026-research1000", "dac-2026-research1028", "dac-2026-research1054", "dac-2026-research1065", "dac-2026-research108", "dac-2025-research1019"}
    rows, summary, _ = build_queue(ROOT)
    assert summary["supplementary_assessment_paper_count"] == 9
    queue = {r["paper_id"]: r for r in rows}
    packets, coverage = build_packets(ROOT)
    drafts = build_drafts(ROOT)
    assert coverage["supplementary_assessment_packet_count"] == 7
    for paper_id, items in supplements.items():
        assert queue[paper_id]["independent_review_status"] == "pending"
        assert queue[paper_id]["evidence_tier"] == "official_description"
        assert queue[paper_id]["supplementary_assessments"]
        found = [p for p in packets + drafts if p["paper_id"] == paper_id]
        assert found
        for packet in found:
            assert packet["supplementary_researcher_assessments"] == items
            assert packet["review_status"] == "not_reviewed"
            assert not packet["independent_verdicts"]
            assert packet["source_tier"] == "official_description"
            assert packet["original_source_text"]
        for item in items:
            raw = (ROOT / item["path"]).read_bytes()
            assert item["sha256"] == hashlib.sha256(raw).hexdigest()
            assert item["assessment"] == json.loads(raw)
            assert item["content_role"] == "researcher_assessment_not_original_source"


@pytest.mark.parametrize("change,error", [
    ({"paper_id": "wrong"}, "identity"),
    ({"title": "Different title"}, "identity"),
    ({"source_url": "https://example.org/unregistered"}, "registration"),
    ({"independent_review_status": "accepted"}, "boundary"),
    ({"extraction_scope": ""}, "boundary"),
])
def test_invalid_supplement_fails_closed(change, error):
    assessment = json.loads((ROOT / "dac/data/exact-t-primary-assessment-v1.json").read_text())
    paper = {"paper_id": assessment["paper_id"], "title": assessment["title"]}
    source = {"source_id": assessment["source_id"], "url": assessment["source_url"]}
    with pytest.raises(ValueError, match=error):
        validate({**assessment, **change}, paper, source)


def test_strix_conditions_keep_simulation_and_latency_scope_explicit():
    r = json.loads((ROOT / "dac/data/strix-primary-assessment-v1.json").read_text())
    c = r["conditions"]
    assert c["simulation_exception"]["configuration"] == "BF16-I"
    assert c["latency"]["metric"] == "worst-case detection latency"
    assert "correction" in c["latency"]["limit"]
    assert c["slowdown"]["geometric_mean"] < max(c["slowdown"]["range"])
    assert c["baselines"]["budget"] == "area-matched"
    assert c["baselines"]["realm_rollback_limit"] == 1
    assert r["independent_review_status"] == "pending"
    table = r["pdf_verification"]["latency_table"]
    assert set(table["rows"]) == set(c["latency"]["configurations"])
    assert table["missing_configuration"] not in table["rows"]
    assert all(len(row) == len(table["columns"]) for row in table["rows"].values())
    assert max(value for row in table["rows"].values() for value in row) == table["maximum_listed"] < 1
