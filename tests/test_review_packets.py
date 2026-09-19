import json
from pathlib import Path

from scripts.audit_adjudications import audit
from scripts.build_review_packets import build, source_matches

ROOT = Path(__file__).resolve().parents[1]


def test_source_matching_ignores_session_only_and_requires_identity():
    record = {"paper_id": "p", "title": "A paper", "evidence_url": "https://63dac.conference-program.com/?id=RESEARCH108&p=16&sess=old"}
    source = {**record, "evidence_url": "https://63dac.conference-program.com/?id=RESEARCH108&p=16&sess=new"}
    assert source_matches(record, source)
    assert not source_matches(record, {**source, "title": "Different paper"})
    assert not source_matches(record, {**source, "evidence_url": source["evidence_url"].replace("108", "109")})


def test_packets_do_not_promote_summaries_or_leak_synthesis():
    packets, summary = build(ROOT)
    assert summary["packet_count"] == 582
    assert summary["synthesis_anchor_count"] == len(set(summary["synthesis_anchor_ids"]))
    assert summary["independent_review_count"] == 0
    mtia = next(p for p in packets if p["paper_id"] == "isca-2026-program-069")
    assert mtia["original_source_text"]
    assert mtia["source_text_status"] == "captured_original_abstract"
    assert mtia["researcher_summary_not_original_source"]
    assert mtia["evidence_locators"]
    assert all(not p["independent_verdicts"] for p in packets)
    assert all("synthesis_directions" not in p for p in packets)
    assert all(p["original_source_sha256"] for p in packets if p["original_source_text"])


def test_packet_handoff_covers_exact_coded_set_and_has_no_acceptance():
    coded = {
        row["paper_id"]
        for path in sorted(ROOT.glob("*/data/adjudicated-*.jsonl"))
        for row in (json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip())
    }
    packets, _ = build(ROOT)
    assert len(coded) == len(packets) == 582
    assert coded == {packet["paper_id"] for packet in packets}
    assert all(packet["review_status"] == "not_reviewed" and not packet["independent_verdicts"] for packet in packets)


def test_completion_audit_keeps_scientific_gates_open():
    audit = json.loads((ROOT / "reports/completion-audit-v1.json").read_text(encoding="utf-8"))
    assert audit["status"] == "bounded_package_complete_scientific_gates_open"
    statuses = {item["id"]: item["status"] for item in audit["subgoals"]}
    assert statuses["subgoal-5-independent-review"] == "prepared_pending"
    assert statuses["subgoal-6-temporal"] == "insufficient_evidence_explicit"
    assert "Do not mark the overall GOAL complete" in audit["interpretation_gate"]


def test_audit_uses_identity_matched_company_description_for_isca_044():
    result = audit(ROOT)
    recovered = next(p for p in result["checks"] if p["paper_id"] == "isca-2026-program-044")
    assert recovered["evidence_overlap"] is not None
    assert recovered["source_comparison_status"] == "captured_original_text_compared"
    assert recovered["status"] == "pass"
    assert result["review_count"] == 0


def test_new_iccad_mechanisms_keep_original_text_and_objections_separate():
    packets, _ = build(ROOT)
    selected = [p for p in packets if p["paper_id"] in {"iccad-2025-114", "iccad-2025-1142"}]
    assert len(selected) == 2
    for packet in selected:
        assert packet["source_text_status"] == "captured_original_abstract"
        assert packet["original_source_text"]
        assert packet["supplementary_researcher_assessments"]
        assert not packet["independent_verdicts"]


def test_packets_expose_condition_reconciliation_without_promoting_it_to_review():
    packets, summary = build(ROOT)
    mapping = next(p for p in packets if p["paper_id"] == "dac-2026-research535")
    assert summary["condition_context_packet_count"] > 0
    context = mapping["condition_reconciliation_context"]
    assert context["status"] == "direction_atlas_recorded"
    assert context["records"]
    record = context["records"][0]
    assert record["adjudicated"]["condition_status"] == "partial"
    assert record["combined_field_presence"]["condition_status"] == "complete"
    assert record["supplementary"]["evidence_tier"] == "author_preprint"
    assert "not an independent scientific verdict" in context["boundary"]
    assert mapping["review_status"] == "not_reviewed"
    assert mapping["independent_verdicts"] == []

    ordinary = next(p for p in packets if p["paper_id"] == "dac-2026-research004")
    assert ordinary["condition_reconciliation_context"]["status"] == "not_in_direction_atlas"
