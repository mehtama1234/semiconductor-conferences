import json
from pathlib import Path

import pytest

from scripts.collect_iccad_invited import invited_from_blocks

ROOT = Path(__file__).resolve().parents[1]


def test_bold_title_boundary_handles_single_and_wrapped_authors():
    rows = invited_from_blocks([
        ("20001: Invited Paper: A title\nwith a continuation", "\nSingle Author\nUniversity, Country\n12:00"),
        ("20002: Invited Paper: Another title", "First Author {1}, Second\nAuthor {2}\n{1} First University; {2} Other University"),
        ("Special Session: A label", "Not a paper"),
    ], 59)
    assert len(rows) == 2
    assert rows[0]["title"] == "A title with a continuation"
    assert rows[0]["authors"] == ["Single Author"]
    assert rows[1]["authors"] == ["First Author {1}", "Second Author {2}"]
    assert all(row["regular_paper_comparison_eligible"] is False for row in rows)
    with pytest.raises(ValueError, match="Missing invited author"):
        invited_from_blocks([("20001: Invited Paper: Title", "{1} University")], 59)


def test_reviewed_unmarked_name_wrap_rejects_changed_boundary():
    body = "Gauthaman Murali, Archana\nPandey, Another Author,\nTanay Karnik\nIntel, United States"
    row = invited_from_blocks([("20043: Invited Paper: A title", body)], 105)[0]
    assert row["authors"] == ["Gauthaman Murali", "Archana Pandey", "Another Author", "Tanay Karnik"]
    with pytest.raises(ValueError, match="reviewed author boundary"):
        invited_from_blocks([("20043: Invited Paper: A title", body.replace("Pandey", "Other"))], 105)


def test_invited_inventory_is_complete_for_audited_ids_not_technical_coding():
    rows = {r["paper_id"]: r for r in map(json.loads, (ROOT / "iccad/data/papers-2025-program.jsonl").read_text().splitlines()) if r.get("program_entry_type") == "invited_paper"}
    audit = json.loads((ROOT / "iccad/data/program-scope-audit-v1.json").read_text())
    expected = {r["paper_id"] for r in audit["headings"] if r["observed_entry_type"] == "invited_paper"}
    assert set(rows) == expected and len(rows) == 43
    assert all(row["authors"] and row["title"] and not row["regular_paper_comparison_eligible"] and not row["metrics"] and row["theme_id"] is None for row in rows.values())
    assert len(rows["iccad-2025-20043"]["authors"]) == 12
    assert rows["iccad-2025-20043"]["authors"][4] == "Archana Pandey"
    assert rows["iccad-2025-20044"]["authors"] == ["Tim Kogel"]
    assert len(rows["iccad-2025-20035"]["authors"]) == 7
