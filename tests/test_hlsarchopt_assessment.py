import json
from pathlib import Path


def test_stored_hls_estimates_do_not_become_measurements():
    root = Path(__file__).resolve().parents[1]
    assessment = json.loads((root / "dac/data/hlsarchopt-primary-assessment-v1.json").read_text())
    artifact = assessment["artifact"]
    report = artifact["stored_synthesis_report"]
    assert report["evidence_modality"] == "stored_hls_estimate_not_reproduction"
    assert report["interval_cycles"] < report["latency_cycles"]
    assert round(report["latency_cycles"] * report["target_clock_ns"] / 1e6, 3) == report["reported_latency_ms"]
    assert set(report["resources"]) == set(report["available_resources"])
    assert len(report["sha256"]) == len(report["xml_sha256"]) == 64
    assert artifact["execution_status"] == "not_executed"
    assert assessment["independent_review_status"] == "pending"
    assert assessment["headline_metric_status"] == "withheld_pending_fullpaper_conditions"
    recheck = assessment["current_source_recheck"]
    assert recheck["capture_date"] == "2026-09-08"
    assert "11.78x" in " ".join(recheck["official_program_observations"])
    assert "full-model integration" in " ".join(recheck["repository_observations"])
    assert "no full-text PDF" in recheck["full_text_status"]
