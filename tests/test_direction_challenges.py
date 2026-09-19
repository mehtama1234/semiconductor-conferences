import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_challenges_link_original_sources_without_review_promotion():
    ledger = json.loads((ROOT / "data/direction-challenges-v1.json").read_text())
    packets = {r["paper_id"]: r for r in map(json.loads, (ROOT / ledger["source_packet_path"]).read_text().splitlines())}
    directions = json.loads((ROOT / "data/long-term-direction-atlas-v1.json").read_text())
    anchors = {e.get("paper_id") for d in directions["directions"] for e in d["evidence"]}
    assert {c["direction_number"] for c in ledger["cases"]} == set(range(1, 7))
    assert len({c["paper_id"] for c in ledger["cases"]}) == 6
    for case in ledger["cases"]:
        assert case["paper_id"] not in anchors
        packet = packets[case["paper_id"]]
        assert hashlib.sha256(packet["original_source_text"].encode()).hexdigest() == case["source_sha256"]
        assert case["evidence_tier"] == packet["source_tier"] == "official_description"
        assert not packet["independent_verdicts"]
        assert case["qualification"] and case["next_evidence"]
        assert case["failure_condition"]
        assert direction_case_failure_condition(case["paper_id"], directions)
    assert ledger["independent_review_status"] == "pending"


def direction_case_failure_condition(paper_id, directions):
    return any(
        direction.get("challenge", {}).get("paper_id") == paper_id
        and direction.get("challenge", {}).get("failure_condition")
        for direction in directions["directions"]
    )


def test_identity_followup_does_not_claim_alias_resolution():
    ledger = json.loads((ROOT / "data/direction-challenges-v1.json").read_text())
    followup = ledger["identity_followups"][0]
    assert followup["paper_id"] in {case["paper_id"] for case in ledger["cases"]}
    assert followup["status"] == "paper_identity_confirmed_system_alias_unresolved"
    assert len(followup["primary_sources"]) == 2
    assert followup["searches"] and followup["revisit_condition"]
    assert followup["independent_review_status"] == "pending"
