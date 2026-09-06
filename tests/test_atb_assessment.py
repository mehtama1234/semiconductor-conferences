import json
from math import isclose
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_atb_mismatch_remains_unaccepted():
    r = json.loads((ROOT / "dac/data/atb-primary-assessment-v1.json").read_text())
    assert r["headline_metric_status"] == "withheld_pending_source_reconciliation"
    assert r["independent_review_status"] == "pending"
    assert len(r["identity"]["unresolved_name_pairs"]) == 2
    for check in r["arithmetic_checks"]:
        assert isclose(check["numerator"] / check["denominator"], check["computed_ratio"], rel_tol=1e-12)
        assert check["computed_ratio"] != check["printed_ratio"]
    assert r["config_1_table_rows"][0]["matrix_m_k_n"] != r["config_1_table_rows"][2]["matrix_m_k_n"]
