import json
from pathlib import Path

import pytest

from scripts.build_work_queue import build, unique_index

ROOT = Path(__file__).resolve().parents[1]


def test_queue_preserves_inventory_and_evidence_boundaries():
    rows, summary, _ = build(ROOT)
    by_id = unique_index(rows)
    assert len(rows) == sum(summary["corpus_counts"].values()) == 1589
    assert summary["coded_count"] == 180
    # Secondary CODO is an alias of a primary-backed paper, not a seventh paper.
    codo = by_id["isca-2026-program-002"]
    assert codo["secondary_alias_id"] == "isca-2026-codo"
    assert codo["collection_status"] == "cited_technical_source"
    assert codo["paper_id"] not in summary["secondary_pending_ids"]
    assert len(summary["secondary_pending_ids"]) == 4
    assert by_id["isca-2026-program-158"]["identity_status"] == "missing_title_requires_inventory_review"
    assert not by_id["isca-2026-program-158"]["title_denominator_included"]
    assert summary["eligible_title_counts"]["isca-2026"] == 172
    assert summary["excluded_slot_ids"] == ["isca-2026-program-158"]
    historical = [r for r in rows if r["conference_id"] == "dac" and r["analysis_edition"] == 2025]
    assert sum(r["collection_status"] == "substantive_description" for r in historical) == 23
    assert sum(r["coding_status"] == "technical_draft" for r in historical) == 23
    assert sum(r["coding_status"] == "not_coded" for r in historical) == 395
    assert summary["draft_paper_count"] == 521
    current_dac = [r for r in rows if r["paper_id"].startswith("dac-2026-")]
    assert len(current_dac) == 543
    assert all(r["coding_status"] != "not_coded" for r in current_dac)
    assert "draft_requires_source_depth_and_review" in by_id["dac-2025-research002"]["priority_reasons"]
    reviewed = by_id["dac-2026-research1211"]
    assert reviewed["preliminary_review"] == "revise"
    assert reviewed["independent_review_status"] == "pending"
    assert all(r["independent_review_status"] != "accepted" for r in rows)


def test_duplicate_identity_fails_instead_of_silently_overwriting():
    with pytest.raises(ValueError, match="Duplicate paper ID"):
        unique_index([{"paper_id": "same"}, {"paper_id": "same"}])


def test_queue_covers_every_inventory_record_with_next_action():
    rows, _, _ = build(ROOT)
    inventory = {
        row["paper_id"]
        for path in sorted(ROOT.glob("*/data/papers-*-program.jsonl"))
        for row in (json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip())
    }
    assert len(inventory) == len(rows) == 1589
    assert inventory == {row["paper_id"] for row in rows}
    assert all(row.get("next_actions") and row.get("priority_reasons") for row in rows)
