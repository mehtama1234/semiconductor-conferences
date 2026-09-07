import copy
import json
from pathlib import Path

import pytest

from scripts.collect_iccad_fallback import apply_src_corrections
from scripts.build_work_queue import build

ROOT = Path(__file__).resolve().parents[1]


def test_src_repair_is_idempotent_scoped_and_matches_inventory():
    ledger = json.loads((ROOT / "iccad/data/src-entry-reconciliation-v1.json").read_text())
    changes = ledger["changes"]
    assert len(changes) == 10
    assert sum(c["before"]["title"] != c["after"]["title"] for c in changes) == 8
    records = [{"paper_id": c["paper_id"], **c["before"], "unchanged": "sentinel"} for c in changes]
    records.append({"paper_id": "unrelated", "title": "Unrelated", "authors": []})
    unrelated = copy.deepcopy(records[-1])
    apply_src_corrections(records, ledger)
    first = copy.deepcopy(records)
    apply_src_corrections(records, ledger)
    assert records == first and records[-1] == unrelated
    inventory = {r["paper_id"]: r for r in map(json.loads, (ROOT / "iccad/data/papers-2025-program.jsonl").read_text().splitlines())}
    for row in records[:-1]:
        assert row["unchanged"] == "sentinel"
        for key in ("title", "authors", "program_entry_type", "regular_paper_comparison_eligible"):
            assert inventory[row["paper_id"]][key] == row[key]
    records[0]["title"] = "Wrong source title"
    with pytest.raises(ValueError):
        apply_src_corrections(records, ledger)


def test_src_entries_remain_in_inventory_but_not_regular_paper_comparisons():
    rows, summary, _ = build(ROOT)
    src = [r for r in rows if r.get("program_entry_type") == "student_research_competition_oral"]
    assert len(src) == summary["explicit_nonregular_entry_count"] == 10
    assert all(r["regular_paper_comparison_eligible"] is False for r in src)
    assert all(r["title_denominator_included"] for r in src)
    assert summary["corpus_counts"]["iccad-2025"] == 276
    gau = next(r for r in src if r["paper_id"] == "iccad-2025-11")
    assert "Lizhou" not in gau["title"]
