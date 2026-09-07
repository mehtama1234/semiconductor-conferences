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


def test_exact_t_figures_preserve_variant_and_counterexample():
    r = json.loads((ROOT / "dac/data/exact-t-primary-assessment-v1.json").read_text())
    pdf = r["pdf_verification"]
    assert pdf["page_number"] == 6
    assert len(pdf["sha256"]) == 64
    variants = pdf["figure_8"]["multiplier_t_count_change_percent"]
    assert variants == {"k_lut_mapper": -6.9, "bilinear_mapper": -14.3}
    case = pdf["figure_9_counterexample"]
    assert case["ours"] > case["qrom"] == case["select_swap"]
    artifact = r["artifact_inspection"]
    assert artifact["url"].endswith(artifact["commit"])
    assert "scripts/lib/qasm_simulate.py" in artifact["inspected_paths"]
    smoke = artifact["smoke_test"]
    assert smoke["build_exit_code"] == smoke["mapper_exit_code"] == 0
    assert smoke["status"] == "build_and_qasm_emission_only"
    assert len(smoke["output_sha256"]) == 64
