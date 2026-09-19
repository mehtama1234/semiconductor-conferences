import json
from pathlib import Path

from scripts.build_cross_conference_comparisons import build


ROOT = Path(__file__).resolve().parents[1]


def test_cross_conference_comparison_dossiers_cover_directions() -> None:
    result = build()
    assert len(result["dossiers"]) == 6
    assert all(item["reference_count"] > 0 for item in result["dossiers"])
    assert all(item["promotion_gate"].startswith("blocked_") for item in result["dossiers"])
    assert (ROOT / "reports/comparisons/README.md").exists()


def test_comparison_dossiers_preserve_comparability_boundary() -> None:
    data = json.loads((ROOT / "data/cross-conference-comparison-dossiers-v1.json").read_text())
    for item in data["dossiers"]:
        text = (ROOT / item["page"]).read_text()
        assert "What is actually comparable" in text
        assert "Current conclusion boundary" in text
        assert "source tier" in text


def test_corrections_do_not_inherit_complete_condition_status() -> None:
    result = build()
    affected = [r for r in result['dossiers'] if 'iccad-2025-130' in r['corrected_reference_ids']]
    assert len(affected) == 2
    for row in affected:
        text = (ROOT / row['page']).read_text()
        paper = next(line for line in text.splitlines() if line.startswith('| `iccad-2025-130`'))
        assert 'correction_pending_condition_review' in paper
        assert 'https://arxiv.org/pdf/2507.04677v1' in paper
        assert '`complete`' not in paper
        assert 'historical condition status `complete`' in text
        assert row['promotion_gate'].startswith('blocked_')
