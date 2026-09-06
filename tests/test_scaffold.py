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
