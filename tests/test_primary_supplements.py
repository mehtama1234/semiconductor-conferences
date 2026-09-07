import hashlib
import json
from pathlib import Path

import pytest

from scripts.primary_supplements import load, validate
from scripts.build_review_packets import build as build_packets
from scripts.build_draft_review_packets import build as build_drafts
from scripts.build_work_queue import build as build_queue

ROOT = Path(__file__).resolve().parents[1]


def test_squat_pdf_latency_arithmetic_distinguishes_rounding_uncertainty():
    from decimal import Decimal

    record = json.loads((ROOT / "iccad/data/squat-primary-recovery-v1.json").read_text())
    pdf = record["pdf_verification"]
    mismatches = []
    incompatible = []
    half_step = Decimal("0.005")
    checked = 0
    for name, latencies in pdf["latency_ms_per_token"].items():
        assert len(latencies) == len(pdf["columns"])
        ratios = pdf["reported_speedups_excluding_fp16"][name]
        assert len(ratios) == len(latencies) - 1
        for index, (latency, reported) in enumerate(zip(latencies[1:], ratios), 1):
            baseline, latency, reported = (Decimal(str(value)) for value in (latencies[0], latency, reported))
            checked += 1
            if (baseline / latency).quantize(Decimal("0.01")) != reported:
                mismatches.append((name, pdf["columns"][index]))
            lower = (baseline - half_step) / (latency + half_step)
            upper = (baseline + half_step) / (latency - half_step)
            if lower > reported + half_step or upper < reported - half_step:
                incompatible.append((name, pdf["columns"][index]))
    assert mismatches == [("llama_mobile", "W4A4"), ("gpt2_mobile", "W4A4:8_1:3"), ("gpt2_mobile", "W4A4:8_1:1")]
    assert incompatible == [("gpt2_mobile", "W4A4:8_1:3"), ("gpt2_mobile", "W4A4:8_1:1")]
    analysis = pdf["rounding_analysis"]
    assert checked == analysis["checked_speedup_count"] == 24
    assert len(mismatches) == analysis["strict_displayed_value_mismatch_count"] == 3
    assert analysis["rounding_incompatible_cells"] == [f"{name}/{column}" for name, column in incompatible]
    assert analysis["rounding_compatible_mismatch"]["cell"] == "llama_mobile/W4A4"
    assert pdf["status"] == "original_pdf_confirms_two_rounding_incompatible_ratio_mismatches"
    assert record["independent_review_status"] == "pending"


def test_orthrus_pdf_tradeoff_and_hypervolume_arithmetic():
    row = json.loads((ROOT / "iccad/data/orthrus-primary-recovery-v1.json").read_text())
    figure = row["pdf_verification"]["figure_10_B"]
    assert figure["recharacterized_power"] < figure["original_power"]
    assert figure["recharacterized_delay"] > figure["original_delay"]
    values = row["conditions"]["table_III_HV_times_1e_minus2"]
    assert round(100 * (values["orthrus"] / values["baseline"] - 1), 1) == 33.2
    assert len(row["pdf_verification"]["sha256"]) == 64
    assert row["budget_review"]["unresolved"]
    assert row["independent_review_status"] == "pending"


def test_supplements_reach_queue_and_both_packet_types_without_promotion():
    supplements = load(ROOT)
    iccad_items = supplements.pop("iccad-2025-1")
    orthrus_items = supplements.pop("iccad-2025-437")
    hlps = supplements.pop("iccad-2025-109")[0]["assessment"]
    qudit = supplements.pop("iccad-2025-1094")[0]["assessment"]
    sera = supplements.pop("iccad-2025-1109")[0]["assessment"]
    nimch = supplements.pop("iccad-2025-1111")[0]["assessment"]
    uglms = supplements.pop("iccad-2025-1117")[0]["assessment"]
    assert nimch["source_tier"] == "institutional_abstract"
    assert uglms["source_tier"] == "author_preprint_selected_full_text"
    assert sera["source_tier"] == "author_manuscript_selected_full_text"
    assert len(sera["identity"]["authors"]) == 5
    assert qudit["source_tier"] == "author_posted_abstract"
    assert len(qudit["identity"]["authors"]) == 4
    assert "Architecture" in qudit["identity"]["observed_title"]
    assert "System" in qudit["title"]
    assert len(hlps["identity"]["authors"]) == 13
    assert hlps["headline_metric_status"] == "withheld_pending_table_and_budget_review"
    squat = supplements.pop("iccad-2025-105")[0]["assessment"]
    discrepancy = squat["table_IV_discrepancy"]
    calculated = [round(discrepancy["fp16_latency"] / value, 2) for value in discrepancy["mixed_latencies"]]
    assert calculated == discrepancy["calculated_rounded_speedups"]
    assert calculated != discrepancy["reported_speedups"]
    assert len(squat["identity"]["authors"]) == 12
    assert squat["independent_review_status"] == "pending"
    assert set(supplements) == {"dac-2026-research031", "dac-2026-research043", "dac-2026-research046", "dac-2026-research1000", "dac-2026-research1028", "dac-2026-research1054", "dac-2026-research1065", "dac-2026-research108", "dac-2026-research1101", "dac-2026-research1110", "dac-2026-research1113", "dac-2026-research1182", "dac-2026-research1186", "dac-2026-research535", "dac-2026-research865", "dac-2026-research2760", "dac-2025-research1019"}
    rows, summary, _ = build_queue(ROOT)
    assert summary["supplementary_assessment_paper_count"] == 25
    queue = {r["paper_id"]: r for r in rows}
    packets, coverage = build_packets(ROOT)
    drafts = build_drafts(ROOT)
    assert coverage["supplementary_assessment_packet_count"] == 19
    orthrus_packet = next(p for p in packets if p["paper_id"] == "iccad-2025-437")
    assert orthrus_packet["supplementary_researcher_assessments"] == orthrus_items
    assert orthrus_packet["review_status"] == "not_reviewed"
    assert not orthrus_packet["independent_verdicts"]
    assert queue["iccad-2025-437"]["supplementary_assessments"]
    assert orthrus_items[0]["assessment"]["headline_metric_status"] == "withheld_pending_figure_and_budget_review"
    assert len(orthrus_items[0]["assessment"]["identity"]["authors"]) == 9
    assert queue["iccad-2025-1"]["evidence_tier"] == "program_metadata"
    assert queue["iccad-2025-1"]["supplementary_assessments"]
    assert not [p for p in packets + drafts if p["paper_id"] == "iccad-2025-1"]
    assessment = iccad_items[0]["assessment"]
    assert assessment["source_tier"] == "institutional_technical_report"
    assert assessment["headline_metric_status"] == "institutional_claims_only_not_accepted"
    assert len(assessment["identity"]["authors"]) == 7
    assert assessment["independent_review_status"] == "pending"
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
