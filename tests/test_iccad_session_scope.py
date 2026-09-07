import copy
import json
from pathlib import Path

import pytest

from scripts.build_iccad_session_scope import map_blocks, apply_scope, apply_title_author_repairs

ROOT = Path(__file__).resolve().parents[1]


def test_session_context_spans_pages_but_rejects_orphan_and_type_conflict():
    sessions = map_blocks([(40, [("Regular research Room", ": Rome"), ("Session Chair(s):", "Chair"), ("1: Paper one", "Authors")]),
                           (41, [("2: Paper two", "Authors"), ("Special Session: Topic Room", ": Athens; Session Chair: Person"), ("20001: Invited Paper: Invited", "Author")])])
    assert len(sessions) == 2
    assert sessions[0]["papers"][1]["program_pdf_page"] == 41
    assert sessions[0]["session_pdf_page"] == 40
    assert sessions[0]["papers"][0]["regular_paper_comparison_eligible"] is True
    assert sessions[1]["papers"][0]["regular_paper_comparison_eligible"] is False
    with pytest.raises(ValueError, match="lacks"):
        map_blocks([(40, [("Regular Room", ": Rome"), ("1: Paper", "Authors")])])
    with pytest.raises(ValueError, match="conflict"):
        map_blocks([(40, [("Regular Room", ": Rome; Session Chair: Person"), ("20001: Invited Paper: Paper", "Authors")])])


def test_title_author_repairs_are_guarded_and_idempotent():
    ledger = json.loads((ROOT / "iccad/data/title-author-repairs-v1.json").read_text())
    records = [{"paper_id": c["paper_id"], **copy.deepcopy(c["before"]), "sentinel": True} for c in ledger["changes"]]
    apply_title_author_repairs(records, ledger)
    once = copy.deepcopy(records)
    apply_title_author_repairs(records, ledger)
    assert records == once and all(row["sentinel"] for row in records)
    assert records[0]["authors"] == ["HsinYing Tsai", "Chung-Kai Wu", "Chih-Cheng Hsu", "Jie-Hong Roland Jiang"]
    records[0]["title"] = "Unexpected source change"
    with pytest.raises(ValueError, match="reviewed boundary"):
        apply_title_author_repairs(records, ledger)


def test_all_numbered_entries_have_matching_scope_not_technical_acceptance():
    ledger = json.loads((ROOT / "iccad/data/session-scope-v1.json").read_text())
    records = [json.loads(line) for line in (ROOT / "iccad/data/papers-2025-program.jsonl").read_text().splitlines()]
    assert ledger["record_count"] == 319 and ledger["regular_session_count"] == 50
    assert ledger["entry_type_counts"] == {"regular_paper": 266, "invited_paper": 43, "student_research_competition_oral": 10}
    before = copy.deepcopy(records)
    apply_scope(records, ledger)
    assert records == before
    assert sum(row["regular_paper_comparison_eligible"] for row in records) == 266
    assert all(row["program_session_title"] and row["program_session_pdf_page"] <= row["program_pdf_page"] for row in records)
    records[0]["title"] = "Wrong identity"
    with pytest.raises(ValueError, match="title identity"):
        apply_scope(records, ledger)
