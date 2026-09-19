import json
from pathlib import Path

from scripts.build_cross_conference_atlas import build


ROOT = Path(__file__).resolve().parents[1]


def test_cross_conference_atlas_covers_all_canonical_directions() -> None:
    result = build(ROOT)
    source = json.loads((ROOT / "data/long-term-direction-atlas-v1.json").read_text())
    assert result["schema"] == "cross-conference-direction-atlas.v1"
    assert len(result["directions"]) == len(source["directions"]) == 6
    for row in result["directions"]:
        assert set(row["conference_reference_counts"]) == {"isca", "dac", "iccad"}
        assert set(row["venue_roles"]) == {"isca", "dac", "iccad"}
        assert row["relation_type"]
        assert row["status"] == "provisional_cross_conference_case_evidence"


def test_cross_conference_atlas_preserves_prohibited_inferences() -> None:
    result = json.loads((ROOT / "data/cross-conference-direction-atlas-v1.json").read_text())
    assert "market share" in result["prohibited_inference"]
    assert "rising or declining direction without comparable historical snapshots" in result["prohibited_inference"]
