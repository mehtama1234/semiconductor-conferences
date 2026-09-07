import json
from pathlib import Path
from statistics import mean


ROOT = Path(__file__).resolve().parents[1]


def test_hlps_coding_and_packet_preserve_review_boundary():
    from scripts.build_review_packets import build
    from scripts.build_evidence_summary import PATHS

    path = "iccad/data/adjudicated-2025-batch-5.jsonl"
    assert path in PATHS
    row = json.loads((ROOT / path).read_text())
    inventory = {r["paper_id"]: r for r in map(json.loads, (ROOT / "iccad/data/papers-2025-program.jsonl").read_text().splitlines())}
    assert inventory[row["paper_id"]]["title"] == row["title"]
    sources = {r["source_id"]: r for r in map(json.loads, (ROOT / "iccad/data/sources.jsonl").read_text().splitlines())}
    assert sources[row["evidence_source_id"]]["url"] == row["evidence_url"]
    assert row["metrics"] and "headline ratio remains withheld" in row["metrics"][0]
    assert row["independent_review_status"] == "pending"
    assert "unequal-population" in row["limits"] and "cumulative" in row["limits"]
    packets, _ = build(ROOT)
    packet = next(p for p in packets if p["paper_id"] == row["paper_id"])
    assert packet["original_source_text"]
    assert packet["source_text_status"] == "captured_original_abstract"
    assert not packet["independent_verdicts"]
    assert packet["supplementary_researcher_assessments"]


def test_hlps_table_preserves_missing_baseline_and_comparable_denominators():
    record = json.loads((ROOT / "iccad/data/hlps-dse-primary-recovery-v1.json").read_text())
    pdf = record["pdf_verification"]
    cases = pdf["cases"]
    assert len(cases) == 7
    assert len({r["design"] for r in cases}) == 6
    shared = [r for r in cases if r["autobridge_fmax_mhz"] is not None]
    assert len(shared) == 6
    missing = [r for r in cases if r["autobridge_fmax_mhz"] is None]
    assert [(r["design"], r["device"]) for r in missing] == [("MM 10x13", "Alveo U250")]
    all_dse = mean(r["best_dse_fmax_mhz"] for r in cases)
    auto = mean(r["autobridge_fmax_mhz"] for r in shared)
    vitis = mean(r["vitis_fmax_mhz"] for r in cases)
    assert {k: round(v, 2) for k, v in {"vitis": vitis, "autobridge": auto, "dse": all_dse}.items()} == pdf["aggregation"]["reported_mean_fmax_mhz"]
    ratios = pdf["aggregation"]["ratio_of_displayed_case_means_rounded"]
    assert round(all_dse / vitis, 2) == ratios["dse_over_vitis_all_seven"] == 2.42
    assert round(all_dse / auto, 2) == ratios["dse_seven_over_autobridge_six"] == 1.67
    assert round(mean(r["best_dse_fmax_mhz"] for r in shared) / auto, 2) == ratios["dse_over_autobridge_shared_six"] == 1.65
    assert all(r["total_dse_hours"] >= r["hours_through_best_action"] > r["vitis_hours"] for r in cases)
    assert sum(r["total_dse_hours"] > r["hours_through_best_action"] for r in cases) == 5
    assert record["independent_review_status"] == "pending"
