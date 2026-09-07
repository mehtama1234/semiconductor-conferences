import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_uglms_preserves_simulation_setup_and_followup_boundaries():
    row = json.loads((ROOT / "iccad/data/uglms-primary-recovery-v1.json").read_text())
    c = row["conditions"]
    t = c["table_I"]
    assert len(t["resolution_bits"]) == len(t["total_ms"]) == 5
    assert [round(x*t["iterations"]/1000, 1) for x in t["selection_per_iteration_us"]] == t["selection_total_ms"]
    assert all(total >= selection for total, selection in zip(t["total_ms"], t["selection_total_ms"]))
    assert "simulation" in c["evaluation"] and "synthetic" in c["statistical_test"]
    assert "excluded" in c["timing_scope"] and "fixed iterations" in c["termination"]
    assert "2511.11917" in row["identity"]["excluded_followup"]
    assert row["headline_metric_status"].startswith("withheld")
    assert row["independent_review_status"] == "pending"
