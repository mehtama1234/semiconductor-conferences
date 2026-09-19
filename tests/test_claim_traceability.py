import json
from pathlib import Path

from scripts.build_claim_traceability import build


ROOT = Path(__file__).resolve().parents[1]


def test_claim_traceability_connects_the_end_to_end_chain() -> None:
    result = build()
    assert len(result["directions"]) == 6
    assert all(row["theme_links"] for row in result["directions"])
    assert all(row["subtheme_ids"] for row in result["directions"])
    assert all(row["mechanism_ids"] for row in result["directions"])
    assert all(row["challenge_paper_ids"] for row in result["directions"])
    assert all(not row["unresolved_links"] for row in result["directions"])
    assert all((ROOT / link["page"]).exists() for row in result["directions"] for link in row["theme_links"])
    assert all(row["promotion_gate"].startswith("blocked_") for row in result["directions"])


def test_claim_traceability_report_preserves_uncertainty() -> None:
    data = json.loads((ROOT / "data/claim-traceability-v1.json").read_text())
    assert any("does not prove" in item for item in data["interpretation_limits"])
    report = (ROOT / "reports/claim-traceability-v1.md").read_text()
    assert "End-to-end chains" in report
    assert "promotion gate" in report
    assert "reports/reports" not in report
