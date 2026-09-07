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


def test_atb_pdf_verification_has_version_and_page_provenance():
    r = json.loads((ROOT / "dac/data/atb-primary-assessment-v1.json").read_text())
    check = r["pdf_verification"]
    assert check["url"].endswith(r["source_version"])
    assert check["page_number"] == check["page_index"] + 1 == 6
    assert len(check["sha256"]) == 64
    assert all(c in "0123456789abcdef" for c in check["sha256"])
    assert check["review_type"] == "same_agent_source_verification_not_independent_review"
    assert r["version_check"]["versions_listed"] == ["v1"]
    assert r["version_check"]["check_date"] == check["check_date"]
    assert "matched-workload" in r["revisit_condition"]
