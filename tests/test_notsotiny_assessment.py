import json
from pathlib import Path


def test_notsotiny_timeout_finding_is_not_a_published_score_claim():
    root = Path(__file__).resolve().parents[1]
    assessment = json.loads((root / "dac/data/notsotiny-primary-assessment-v1.json").read_text())
    artifact = assessment["artifact_inspection"]
    assert len(artifact["commit"]) == 40
    assert artifact["timeout_seconds"] == 900
    result = artifact["timeout_result"]
    # Model the inspected aggregation only; do not execute upstream code.
    assert sum(int(r["equiv_passed"]) for r in [result]) == 1
    assert result["equiv_method"] == "timeout" and result["cells_coverage"] == 100
    assert "not a measured inflation" in artifact["limits"]
    assert assessment["independent_review_status"] == "pending"
