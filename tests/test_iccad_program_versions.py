import json
from pathlib import Path

from scripts.compare_iccad_program_versions import compare

ROOT = Path(__file__).resolve().parents[1]


def test_version_comparison_distinguishes_markers_names_and_page_moves():
    old = {"one": {"title": "A title", "authors_with_markers": ["A Person {1}"], "pdf_page": 1},
           "two": {"title": "Other", "authors_with_markers": ["B Person"], "pdf_page": 2}}
    new = {"one": {"title": "A title", "authors_with_markers": ["A Person { 2}"], "pdf_page": 3},
           "added": {"title": "New", "authors_with_markers": ["C Person"], "pdf_page": 4}}
    result = compare(old, new)
    assert result["added_ids"] == ["added"] and result["removed_ids"] == ["two"]
    assert result["author_field_change_count"] == 1 and result["normalized_author_name_change_count"] == 0
    assert result["changes"][0]["changed_fields"] == ["authors_with_markers", "pdf_page"]


def test_program_version_differences_are_routed_without_inventory_overwrite():
    from scripts.build_work_queue import build
    result = json.loads((ROOT / "iccad/data/program-v8-v20-comparison-v1.json").read_text())
    assert result["old_numbered_count"] == result["new_numbered_count"] == 319
    assert result["added_ids"] == result["removed_ids"] == []
    assert result["normalized_title_change_count"] == 0
    assert result["author_field_change_count"] == 5 and result["normalized_author_name_change_count"] == 2
    changes = {r["paper_id"]: r for r in result["changes"]}
    assert len(changes) == 6
    assert changes["iccad-2025-803"]["after"]["pdf_page"] == 114
    rows, _, _ = build(ROOT)
    assert {r["paper_id"] for r in rows if r.get("program_version_review")} == set(changes)
    inventory = {r["paper_id"]: r for r in map(json.loads, (ROOT / "iccad/data/papers-2025-program.jsonl").read_text().splitlines())}
    assert inventory["iccad-2025-20002"]["authors"] == ["Shao-Yun Fang"]
