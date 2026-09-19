import json
from pathlib import Path

from scripts.build_direction_atlas import build


ROOT = Path(__file__).resolve().parents[1]


def test_direction_atlas_is_page_backed_and_preserves_source_evidence() -> None:
    result = build(ROOT)
    source = json.loads((ROOT / "data/technology-direction-evidence-v1.json").read_text())
    assert result["schema"] == "long-term-direction-atlas.v1"
    assert result["status"] == "provisional_page_backed_mechanism_atlas"
    assert len(result["directions"]) == len(source["directions"]) == 6

    source_by_id = {row["direction_id"]: row for row in source["directions"]}
    for direction in result["directions"]:
        assert (ROOT / direction["page"]).exists()
        assert direction["page_backed_sources"]
        assert all((ROOT / path).exists() for path in direction["page_backed_sources"])
        expected_ids = []
        for source_id in direction["source_direction_ids"]:
            for row in source_by_id[source_id]["evidence"]:
                if row["paper_id"] not in expected_ids:
                    expected_ids.append(row["paper_id"])
        assert [row["paper_id"] for row in direction["evidence"]] == expected_ids
        assert direction["challenge"]["paper_id"]
        assert direction["challenge"]["source_url"].startswith("https://")
        assert direction["challenge"]["failure_condition"]
        assert direction["independent_review_count"] == 0


def test_direction_writeups_expose_canonical_counterpressure() -> None:
    from scripts.build_direction_writeups import build

    atlas = json.loads((ROOT / "data/long-term-direction-atlas-v1.json").read_text())
    build(ROOT)
    for direction in atlas["directions"]:
        page = (ROOT / direction["page"]).read_text()
        challenge = direction["challenge"]
        assert "## Counterpressure and falsification boundary" in page
        assert challenge["paper_id"] in page
        assert challenge["source_url"] in page
        assert challenge["failure_condition"] in page


def test_direction_atlas_records_uncertainty_as_status_not_acceptance() -> None:
    result = json.loads((ROOT / "data/long-term-direction-atlas-v1.json").read_text())
    assert all(row["status"] == "provisional_mechanism_hypothesis" for row in result["directions"])
    assert all(row["independent_review_count"] == 0 for row in result["directions"])
    assert any("Temporal claims require comparable editions" in item for item in result["interpretation_limits"])
