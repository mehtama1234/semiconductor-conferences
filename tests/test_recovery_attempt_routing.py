import json
from pathlib import Path

from scripts.build_work_queue import build

ROOT = Path(__file__).resolve().parents[1]


def test_orthrus_coding_is_provenanced_and_review_pending():
    row = json.loads((ROOT / "iccad/data/adjudicated-2025-batch-3.jsonl").read_text())
    sources = {r["source_id"]: r for r in map(json.loads, (ROOT / "iccad/data/sources.jsonl").read_text().splitlines())}
    assert sources[row["evidence_source_id"]]["url"] == row["evidence_url"]
    assert row["independent_review_status"] == "pending"
    assert row["evidence_locators"] and not row["metrics"]
    packet = json.loads((ROOT / "data/review-packets/iccad-2025-437.json").read_text())
    assert packet["original_source_text"]
    assert not packet["independent_verdicts"]


def test_recovery_attempts_are_routed_without_evidence_promotion():
    rows, summary, _ = build(ROOT)
    records = {r["paper_id"]: r for r in rows}
    assert summary["recovery_attempt_paper_count"] == 21
    for pid in ["iccad-2025-1006", "iccad-2025-1008", "iccad-2025-1016", "iccad-2025-1019", "iccad-2025-1022", "iccad-2025-1059", "iccad-2025-1085"]:
        row = records[pid]
        assert row["evidence_tier"] == "program_metadata"
        assert row["coding_status"] == "not_coded"
        assert row["source_recovery_attempts"][0]["evidence_promoted"] is False
        assert row["next_actions"][0] == row["source_recovery_attempts"][-1]["next_action"]


def test_partial_2026_leads_do_not_replace_fallback_or_enter_denominators():
    leads = json.loads((ROOT / "iccad/data/2026-author-discovery-leads.json").read_text())
    assert len(leads["leads"]) == 5
    assert leads["replace_2025_fallback"] is False
    assert leads["status"] == "partial_author_reported_metadata_not_official_inventory"
    rows, summary, _ = build(ROOT)
    assert summary["corpus_counts"]["iccad-2025"] == 319
    assert "iccad-2026" not in summary["corpus_counts"]
    assert all(not (r["conference_id"] == "iccad" and r["analysis_edition"] == 2026) for r in rows)
