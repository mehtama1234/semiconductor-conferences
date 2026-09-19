import json
from pathlib import Path

from scripts.build_subtheme_pages import build


ROOT = Path(__file__).resolve().parents[1]


def test_high_value_subtheme_pages_exist_and_have_evidence() -> None:
    result = build()
    assert len(result["pages"]) == 5
    assert all(page["record_count"] > 0 for page in result["pages"])
    assert all((ROOT / page["page"]).exists() for page in result["pages"])
    assert all(page["direction_ids"] for page in result["pages"])


def test_subtheme_pages_keep_source_and_uncertainty_detail() -> None:
    index = (ROOT / "reports/subthemes/README.md").read_text()
    assert "mechanism layer" in index
    for path in (ROOT / "reports/subthemes").glob("*.md"):
        if path.name == "README.md":
            continue
        text = path.read_text()
        assert "Technical cards" in text
        assert "Evidence tier" in text
        assert "Limits and next evidence" in text
