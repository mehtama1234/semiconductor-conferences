import json
from pathlib import Path

from scripts.validate_project import validate


ROOT = Path(__file__).resolve().parents[1]


def test_scaffold_contract_passes() -> None:
    assert validate(ROOT)["status"] == "passed"


def test_dac_seed_records_have_provenance() -> None:
    rows = [json.loads(line) for line in (ROOT / "dac/data/papers.jsonl").read_text().splitlines() if line.strip()]
    assert len(rows) == 3
    assert all(row["doi"] and row["publisher_url"] and row["limits"] for row in rows)


def test_program_signals_are_not_presented_as_paper_adjudications() -> None:
    for path in (
        ROOT / "isca/data/program-papers.jsonl",
        ROOT / "dac/data/program-signals.jsonl",
        ROOT / "iccad/data/program-signals.jsonl",
    ):
        rows = [json.loads(line) for line in path.read_text().splitlines() if line.strip()]
        assert rows
        assert all("limit" in row or "evidence_limit" in row for row in rows)


def test_isca_metadata_rows_preserve_unknown_evidence() -> None:
    rows = [json.loads(line) for line in (ROOT / "isca/data/papers.jsonl").read_text().splitlines() if line.strip()]
    assert len(rows) == 7
    assert all(row["access_status"] == "official_program_metadata_only" for row in rows)
    assert all(row["classification_confidence"] == "hypothesis_only" for row in rows)
    assert all(row["problem"] is None and row["metrics"] == [] for row in rows)


def test_dac_program_records_preserve_program_only_status() -> None:
    rows = [json.loads(line) for line in (ROOT / "dac/data/program-presentations.jsonl").read_text().splitlines() if line.strip()]
    assert len(rows) >= 500
    assert sum(row["event_type"] == "Research Manuscript" for row in rows) >= 500
    assert all(row["record_status"] == "program_metadata_only" for row in rows)
    assert all(row["source_url"].startswith("https://63dac.conference-program.com/") for row in rows)
    papers = [json.loads(line) for line in (ROOT / "dac/data/papers-2026-program.jsonl").read_text().splitlines() if line.strip()]
    assert len(papers) == sum(row["event_type"] == "Research Manuscript" for row in rows)
    assert all(row["classification_confidence"] == "not_classified" for row in papers)
    assert all(row["theme_id"] is None and row["problem"] is None for row in papers)
