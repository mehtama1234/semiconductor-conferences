import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_direction_review_gate_is_conservative_and_complete() -> None:
    data = json.loads((ROOT / "data/direction-review-gate-v1.json").read_text())
    assert data["status"] == "promotion_blocked_pending_review"
    assert data["independent_review_count"] == 0
    assert len(data["directions"]) == 6
    assert all(direction["promotion_gate"].startswith("blocked_") for direction in data["directions"])
    assert all(direction["anchor_paper_count"] > 0 for direction in data["directions"])
    assert all(paper["packet_path"] for direction in data["directions"] for paper in direction["papers"] if paper["is_synthesis_anchor"])
    assert all("combined_condition_status" in paper for direction in data["directions"] for paper in direction["papers"])
    assert any(
        paper["supplementary_evidence_tier"] == "author_preprint"
        for direction in data["directions"]
        for paper in direction["papers"]
        if paper["paper_id"] == "iccad-2025-1000"
    )
    assert any(
        "Reconcile adjudicated-row gaps with supplementary source-condition fields" in action
        for direction in data["directions"]
        for action in direction["required_actions"]
    )
    assert any("does not rewrite the adjudicated ledger" in item for item in data["interpretation_limits"])


def test_direction_review_gate_report_exists() -> None:
    report = (ROOT / "reports/direction-review-gate-v1.md").read_text()
    assert "Gate summary" in report
    assert "independent verdicts" in report
    assert "blocked" in report
