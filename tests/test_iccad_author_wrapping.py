from scripts.collect_iccad_fallback import extract_program_lines


def test_numbered_author_wrapping_stops_at_affiliations():
    rows = extract_program_lines([
        "1: A paper", "First Author {1}, Yuan", "Wang {4}, Last Author {1}",
        "{1} A University, China; {4} Another University, China", "",
        "8: Another paper", "First Author {1}, Final Author", "{1}, Extra Author {2}",
        "{1} University, China", "{2} Other University, China", "",
    ])
    assert rows[0]["authors"] == ["First Author {1}", "Yuan Wang {4}", "Last Author {1}"]
    assert rows[1]["authors"] == ["First Author {1}", "Final Author {1}", "Extra Author {2}"]


def test_unnumbered_continuation_and_affiliation_boundary():
    rows = extract_program_lines([
        "1: A paper", "First Author, Second Author,", "Third Author",
        "University, Country", "An affiliation continuation {1}", "",
    ])
    assert rows[0]["authors"] == ["First Author", "Second Author", "Third Author"]


def test_repaired_inventory_known_official_examples():
    import json
    from pathlib import Path
    root = Path(__file__).resolve().parents[1]
    records = {r["paper_id"]: r for r in map(json.loads, (root / "iccad/data/papers-2025-program.jsonl").read_text().splitlines())}
    assert len(records) == 276
    assert len(records["iccad-2025-1"]["authors"]) == 7
    assert records["iccad-2025-1"]["authors"][-2:] == ["Yuan Wang {4}", "Xiyuan Tang {1}"]
    assert len(records["iccad-2025-1006"]["authors"]) == 10
    assert len(records["iccad-2025-8"]["authors"]) == 9
