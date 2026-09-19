import json
from pathlib import Path

from scripts.build_expanded_taxonomy import build


ROOT = Path(__file__).resolve().parents[1]


def test_expanded_taxonomy_covers_the_selected_sample() -> None:
    result = build(ROOT)
    assert result["record_count"] == 582
    assert result["theme_count"] == 10
    assert result["observed_subtheme_count"] == 113
    assert result["mechanism_count"] == 577
    assert sum(theme["record_count"] for theme in result["themes"]) == 582
    assert result["theme_subtheme_assignment_count"] == 120


def test_expanded_taxonomy_preserves_provenance_and_expansion_boundary() -> None:
    data = json.loads((ROOT / "data/taxonomy-expanded-v1.json").read_text())
    assert data["status"] == "observed_selected_sample_taxonomy"
    assert data["expanded_subtheme_count"] > 0
    assert all("conference_counts" in theme for theme in data["themes"])
    assert all("source_tier_counts" in subtheme for theme in data["themes"] for subtheme in theme["subthemes"])
    report = (ROOT / "reports/expanded-taxonomy-v1.md").read_text()
    assert "not publication prevalence" in report
    assert "Observed subtheme registry" in report
