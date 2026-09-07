import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_exact_t_assessment_preserves_identity_and_discrepancy():
    r = json.loads((ROOT / "dac/data/exact-t-primary-assessment-v1.json").read_text())
    program = [json.loads(line) for line in (ROOT / r["identity"]["program_record_path"]).read_text().splitlines()]
    paper = next(p for p in program if p["paper_id"] == r["paper_id"])
    assert paper["title"] == r["title"]
    assert paper["authors"] == r["identity"]["authors"]
    assert r["metric_discrepancy"]["official_description"] == 16
    assert r["metric_discrepancy"]["author_preprint"] == 14.3
    assert r["headline_metric_status"] == "withheld_pending_source_reconciliation"
    assert r["independent_review_status"] == "pending"
    assert all(c["locator"] and c["finding"] for c in r["conditions"])
    sources = [json.loads(line) for line in (ROOT / "dac/data/sources.jsonl").read_text().splitlines()]
    assert any(s["source_id"] == r["source_id"] and s["url"] == r["source_url"] for s in sources)
    directions = json.loads((ROOT / "data/technology-direction-evidence-v1.json").read_text())["directions"]
    refs = [ref for d in directions for ref in d["evidence"] if ref["paper_id"] == r["paper_id"]]
    assert refs
    for ref in refs:
        assert json.loads((ROOT / ref["supplementary_assessment_path"]).read_text()) == r
        assert ref["headline_metric_status"] == r["headline_metric_status"]
