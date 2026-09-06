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


def test_isca_program_inventory_is_metadata_only() -> None:
    rows = [json.loads(line) for line in (ROOT / "isca/data/papers-2026-program.jsonl").read_text().splitlines() if line.strip()]
    assert len(rows) >= 100
    assert len({row["paper_id"] for row in rows}) == len(rows)
    assert all(row["access_status"] == "official_program_metadata_only" for row in rows)


def test_isca_historical_inventory_is_separate_and_metadata_only() -> None:
    rows = [json.loads(line) for line in (ROOT / "isca/data/papers-2025-program.jsonl").read_text().splitlines() if line.strip()]
    assert len(rows) == 135
    assert len({row["paper_id"] for row in rows}) == len(rows)
    assert all(row["target_edition"] == 2025 and row["analysis_edition"] == 2025 for row in rows)
    assert all(row["access_status"] == "official_historical_program_metadata_only" for row in rows)
    assert all(row["problem"] is None and row["metrics"] == [] for row in rows)


def test_dac_historical_inventory_is_separate_and_metadata_only() -> None:
    rows = [json.loads(line) for line in (ROOT / "dac/data/papers-2025-program.jsonl").read_text().splitlines() if line.strip()]
    assert len(rows) == 419
    assert len({row["paper_id"] for row in rows}) == len(rows)
    assert all(row["target_edition"] == 2025 and row["analysis_edition"] == 2025 for row in rows)
    assert all(row["access_status"] == "official_historical_program_metadata_only" for row in rows)
    assert all(row["problem"] is None and row["metrics"] == [] for row in rows)


def test_dac_historical_evidence_coverage_is_honest() -> None:
    rows = [json.loads(line) for line in (ROOT / "dac/data/paper-evidence-2025.jsonl").read_text().splitlines() if line.strip()]
    assert len(rows) == 419
    assert sum(row["evidence_status"] == "substantive_description" for row in rows) == 24
    assert sum(row["capture_status"] == "captured_challenge_or_empty" for row in rows) > 0
    assert sum(row["capture_status"] == "not_captured_rate_limited" for row in rows) > 0
    assert all(row["problem"] is None and row["theme_id"] is None for row in rows)


def test_dac_historical_track_baseline_is_program_only() -> None:
    baseline = json.loads((ROOT / "dac/data/track-baseline-2025.json").read_text())
    assert baseline["record_count"] == 419
    assert baseline["records_with_track_assignment"] == 419
    assert baseline["track_counts"]
    assert "not paper abstracts" in baseline["limits"]


def test_dac_current_track_baseline_does_not_invent_label_equivalence() -> None:
    baseline = json.loads((ROOT / "dac/data/track-baseline-2026.json").read_text())
    assert baseline["record_count"] == 543
    assert baseline["records_with_track_assignment"] == 543
    assert baseline["unresolved_track_ids"]
    assert "no 2025 label equivalence is asserted" in baseline["limits"]


def test_isca_crossref_metadata_keeps_technical_claims_unclassified() -> None:
    rows = [json.loads(line) for line in (ROOT / "isca/data/crossref-metadata-2026.jsonl").read_text().splitlines() if line.strip()]
    assert len(rows) >= 150
    assert len({row["paper_id"] for row in rows}) == len(rows)
    assert all(row["doi"] and row["publisher_url"] for row in rows)
    assert all(row["record_status"] == "doi_metadata_only" for row in rows)
    assert all("technical claims" in row["limits"] for row in rows)


def test_isca_adjudicated_batch_has_primary_preprint_evidence() -> None:
    rows = [json.loads(line) for line in (ROOT / "isca/data/adjudicated-2026-batch.jsonl").read_text().splitlines() if line.strip()]
    assert len(rows) == 5
    assert all(row["evidence_url"].startswith("https://arxiv.org/") for row in rows)
    assert all(row["problem"] and row["method_or_artifact"] and row["metrics"] for row in rows)
    assert all(row["classification_confidence"] == "high_primary_preprint" for row in rows)


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


def test_iccad_fallback_keeps_target_and_analysis_editions_distinct() -> None:
    rows = [json.loads(line) for line in (ROOT / "iccad/data/papers-2025-program.jsonl").read_text().splitlines() if line.strip()]
    assert len(rows) >= 250
    assert len({row["doi_or_identifier"] for row in rows}) == len(rows)
    assert all(row["target_edition"] == 2026 and row["analysis_edition"] == 2025 for row in rows)
    assert all(row["classification_confidence"] == "not_classified" for row in rows)


def test_dac_evidence_rows_keep_source_and_status() -> None:
    rows = [json.loads(line) for line in (ROOT / "dac/data/paper-evidence-2026.jsonl").read_text().splitlines() if line.strip()]
    assert len(rows) >= 10
    assert all(row["evidence_url"].startswith("https://63dac.conference-program.com/") for row in rows)
    assert all(row["fetch_status"] in {"ok", "error"} for row in rows)


def test_dac_adjudicated_batch_has_cited_technical_fields() -> None:
    rows = []
    for path in (ROOT / "dac/data/adjudicated-2026-batch.jsonl", ROOT / "dac/data/adjudicated-2026-batch-2.jsonl", ROOT / "dac/data/adjudicated-2026-batch-3.jsonl", ROOT / "dac/data/adjudicated-2026-batch-4.jsonl"):
        rows.extend(json.loads(line) for line in path.read_text().splitlines() if line.strip())
    assert len(rows) == 49
    assert all(row["evidence_url"] and row["evidence_span"] for row in rows)
    assert all(row["problem"] and row["method_or_artifact"] and row["metrics"] for row in rows)


def test_dac_theme_triage_is_not_final_adjudication() -> None:
    rows = [json.loads(line) for line in (ROOT / "dac/data/theme-triage-2026.jsonl").read_text().splitlines() if line.strip()]
    assert len(rows) == 543
    assert all(row["triage_status"] == "keyword_routing_only" for row in rows)
    assert all(row["classification_confidence"] == "not_adjudicated" for row in rows)


def test_isca_indexed_excerpts_are_not_final_evidence() -> None:
    rows = [json.loads(line) for line in (ROOT / "isca/data/indexed-evidence.jsonl").read_text().splitlines() if line.strip()]
    assert len(rows) == 5
    assert all(row["evidence_quality"] == "secondary_indexed_excerpt" for row in rows)
    assert all(row["adjudication_status"] == "pending_primary_verification" for row in rows)


def test_cross_conference_matrix_preserves_evidence_asymmetry() -> None:
    matrix = json.loads((ROOT / "data/cross-conference-matrix-v0.json").read_text())
    assert matrix["status"] == "provisional_synthesis"
    assert len(matrix["rows"]) >= 5
    assert "industrial adoption" in matrix["prohibited_inference"]
    assert "ICCAD has official 2026 CFP scope" in (ROOT / "reports/cross-conference-direction-v0.md").read_text()


def test_each_conference_has_a_deep_page() -> None:
    for conference in ("isca", "dac", "iccad"):
        pages = list((ROOT / conference / "pages").glob("*.md"))
        assert pages
        assert any(len(page.read_text()) > 500 for page in pages)


def test_iccad_batch_keeps_2025_fallback_label() -> None:
    rows = [json.loads(line) for line in (ROOT / "iccad/data/adjudicated-2025-batch.jsonl").read_text().splitlines() if line.strip()]
    assert len(rows) == 5
    assert all(row["target_edition"] == 2026 and row["analysis_edition"] == 2025 for row in rows)
    assert all("primary" in row["classification_confidence"] for row in rows)


def test_learning_index_links_the_three_workstreams() -> None:
    text = (ROOT / "reports/learning-index-v0.md").read_text()
    for marker in ("DAC 2026", "ISCA 2026", "ICCAD 2026 / 2025 fallback", "Cross-conference direction synthesis"):
        assert marker in text


def test_detailed_taxonomy_and_adversarial_protocol_exist() -> None:
    taxonomy = (ROOT / "reports/taxonomy-coding-guide-v1.md").read_text()
    protocol = (ROOT / "reports/adversarial-judge-protocol-v1.md").read_text()
    assert "Observed sub-subskills" in taxonomy
    assert "Adjudication boundary tests" in taxonomy
    assert "Hostile judge prompt" in protocol
    assert '"decision": "accept|revise|reject"' in protocol


def test_evidence_summary_is_explicitly_non_prevalence() -> None:
    summary = json.loads((ROOT / "reports/evidence-summary-v1.json").read_text())
    assert summary["record_count"] == 59
    assert "not a conference prevalence estimate" in summary["selection_warning"]
    assert summary["unreviewed_adversarial_judge_count"] == 59


def test_adversarial_pre_review_is_labeled_as_non_independent() -> None:
    rows = [json.loads(line) for line in (ROOT / "reports/adversarial-review-batch-2.jsonl").read_text().splitlines() if line.strip()]
    assert len(rows) == 10
    assert all(row["judge_mode"] == "same_model_adversarial_pre_review" for row in rows)
    assert all(row["decision"] == "revise" for row in rows)
    assert "not an independent adversarial LLM judgment" in (ROOT / "reports/adversarial-review-status-v1.md").read_text()


def test_evidence_taxonomy_contains_adjudicated_specificity() -> None:
    taxonomy = json.loads((ROOT / "data/taxonomy-v1-evidence.json").read_text())
    all_subsub = [value for theme in taxonomy["themes"] for values in theme.get("subsubthemes", {}).values() for value in values]
    assert "gpu-power-thermal-transformer-side-channel-leakage" in all_subsub
    assert "silicon-calibrated-hierarchical-cim-exploration" in all_subsub


def test_adversarial_preflight_is_explicit_about_its_limits() -> None:
    audit = json.loads((ROOT / "reports/adversarial-preflight-v0.json").read_text())
    assert audit["judge_mode"] == "deterministic_preflight_not_llm"
    assert audit["record_count"] == 59
    assert audit["limits"]


def test_temporal_baseline_refuses_unsupported_directional_claims() -> None:
    report = (ROOT / "reports/temporal-baseline-v1.md").read_text()
    assert "135 papers" in report and "173 papers" in report
    assert "No claim that a topic is rising" in report
