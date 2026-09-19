import json
from pathlib import Path

from scripts.build_research_agenda import build


ROOT = Path(__file__).resolve().parents[1]


def test_research_agenda_has_dependencies_and_gates() -> None:
    result = build()
    assert len(result["agenda"]) == 11
    assert result["current_gate"]["independent_review_count"] == 0
    assert any(item["status"] == "awaiting_external_review" for item in result["agenda"])
    assert any(item["status"] == "disabled_until_gates_pass" for item in result["agenda"])
    assert all(item["acceptance"] and item["evidence"] for item in result["agenda"])


def test_research_agenda_report_is_reader_facing() -> None:
    report = (ROOT / "reports/research-agenda-v1.md").read_text()
    assert "Acceptance rules" in report
    assert "independent verdicts" in report
    assert "prepared packet is not a verdict" in report
