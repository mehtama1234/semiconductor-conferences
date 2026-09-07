import json
from pathlib import Path

import pytest

from scripts.audit_iccad_program_scope import reconcile

ROOT = Path(__file__).resolve().parents[1]


def test_scope_audit_keeps_invited_student_and_unknown_separate():
    inventory = [{"paper_id": "iccad-2025-11", "program_entry_type": "student_research_competition_oral"}, {"paper_id": "iccad-2025-109"}]
    text = "12:30\n11: Student title\n109: Regular candidate\n20001: Invited Paper: Wrapped\ncontinuation"
    result = reconcile([text], inventory)
    assert result["numbered_heading_count"] == 3
    assert result["omitted_ids"] == ["iccad-2025-20001"]
    assert result["type_counts"] == {"invited_paper": 1, "numbered_entry_type_unresolved": 1, "student_research_competition_oral": 1}
    assert not result["inventory_ids_without_heading"]
    assert result["headings"][-1]["pdf_page"] == 38
    with pytest.raises(ValueError, match="Duplicate"):
        reconcile([text, text], inventory)


def test_retained_program_audit_exposes_four_digit_collector_gap():
    result = json.loads((ROOT / "iccad/data/program-scope-audit-v1.json").read_text())
    assert result["numbered_heading_count"] == 319
    assert result["current_inventory_count"] == 276
    assert result["type_counts"] == {"invited_paper": 43, "numbered_entry_type_unresolved": 266, "student_research_competition_oral": 10}
    assert len(result["omitted_ids"]) == len(set(result["omitted_ids"])) == 43
    assert not result["inventory_ids_without_heading"]
    assert all(row["observed_entry_type"] == "invited_paper" for row in result["headings"] if not row["in_current_inventory"])
    assert result["source_sha256"] == "982ed4265e233552d328139a853209789ed265151302a707c7568a8aa009ffdf"
    from scripts.build_work_queue import build
    _, summary, report = build(ROOT)
    assert summary["known_iccad_inventory_omission_ids"] == result["omitted_ids"]
    assert "43 numbered ICCAD invited-paper entries" in report
