import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_longitudinal_protocol_has_all_canonical_direction_gates() -> None:
    protocol = json.loads((ROOT / "data/longitudinal-protocol-v1.json").read_text())
    atlas = json.loads((ROOT / "data/long-term-direction-atlas-v1.json").read_text())
    assert protocol["schema"] == "longitudinal-direction-protocol.v1"
    assert protocol["status"] == "protocol_defined_directional_claims_disabled"
    assert {row["direction_id"] for row in protocol["direction_gates"]} == {
        row["direction_id"] for row in atlas["directions"]
    }
    assert len(protocol["required_comparison_tuple"]) >= 10


def test_longitudinal_protocol_keeps_current_directional_claims_insufficient() -> None:
    protocol = json.loads((ROOT / "data/longitudinal-protocol-v1.json").read_text())
    assert protocol["current_boundary"]["status"] == "insufficient_evidence_for_directional_claims"
    assert "independent verdicts" in protocol["current_boundary"]["reason"]
