import json
from pathlib import Path

from scripts.build_direction_evidence_pages import build


ROOT = Path(__file__).resolve().parents[1]


def test_direction_evidence_pages_cover_atlas_directions() -> None:
    result = build(ROOT)
    atlas = json.loads((ROOT / "data/long-term-direction-atlas-v1.json").read_text())
    assert result["schema"] == "direction-evidence-pages.v1"
    assert len(result["pages"]) == len(atlas["directions"]) + 1
    for relative in result["pages"]:
        assert (ROOT / relative).exists()
        assert (ROOT / relative).read_text().strip()


def test_direction_evidence_pages_preserve_unknown_fields() -> None:
    index = (ROOT / "reports/directions/evidence/README.md").read_text()
    assert "Direction evidence dossiers" in index
    pages = list((ROOT / "reports/directions/evidence").glob("0*-evidence.md"))
    assert len(pages) == 6
    assert any("UNKNOWN" in page.read_text() for page in pages)


def test_direction_dossiers_use_corrected_locator_without_erasing_history() -> None:
    build(ROOT)
    for filename in ('03-closed-loop-design-evidence.md', '06-evaluation-as-research-evidence.md'):
        page = (ROOT / 'reports/directions/evidence' / filename).read_text()
        record = page.split('## NeuroPDE:', 1)[1].split('\n## ', 1)[0]
        current, original = record.split('<details markdown="1">', 1)
        assert 'Equation 10 is squared reference error' in current
        assert 'Sections IV–V, PDF pages 4–8' in current
        assert 'variance below 1e-2' not in current
        assert 'variance below 1e-2' in original
        assert 'Condition review of this correction and independent acceptance remain pending' in current
        import markdown
        rendered = markdown.markdown(record, extensions=['extra'])
        assert '<table>' in rendered.split('<details>', 1)[1]
