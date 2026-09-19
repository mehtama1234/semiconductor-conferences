import json
from pathlib import Path

from scripts.build_direction_condition_register import build


ROOT = Path(__file__).resolve().parents[1]


def test_condition_register_covers_every_atlas_reference() -> None:
    result = build(ROOT)
    atlas = json.loads((ROOT / "data/long-term-direction-atlas-v1.json").read_text())
    assert result["schema"] == "direction-condition-register.v1"
    assert len(result["directions"]) == len(atlas["directions"]) == 6
    for direction, source in zip(result["directions"], atlas["directions"]):
        assert direction["direction_id"] == source["direction_id"]
        expected_count = len(source["evidence"]) + bool(source.get("challenge", {}).get("paper_id"))
        assert direction["paper_count"] == expected_count
        assert all(set(row["available_conditions"]) == set(result["condition_fields"]) for row in direction["papers"])
        assert all(row["condition_status"] in {"complete", "partial"} for row in direction["papers"])
        assert all("supplementary_condition_fields" in row for row in direction["papers"])
        assert all("combined_available_conditions" in row for row in direction["papers"])
        assert all(row["combined_condition_status"] in {"complete", "partial"} for row in direction["papers"])
        assert all("primary_assessment_path" in row for row in direction["papers"])
        assert any(row["role"] == "challenge" for row in direction["papers"])


def test_condition_register_keeps_missingness_and_review_separate() -> None:
    result = json.loads((ROOT / "data/direction-condition-register-v1.json").read_text())
    assert all(row["independent_review_count"] == 0 for row in result["directions"])
    assert any(
        paper["missing_conditions"]
        for direction in result["directions"]
        for paper in direction["papers"]
    )
    assert any("not negative evidence" in item for item in result["interpretation_limits"])
    assert any(row["supplementary_extraction_records"] for row in result["directions"])
    assert any(row["primary_assessment_records"] for row in result["directions"])


def test_condition_register_ingests_conference_local_full_paper_extraction() -> None:
    result = build(ROOT)
    papers = [
        paper
        for direction in result["directions"]
        for paper in direction["papers"]
        if paper["paper_id"] == "iccad-2025-1027"
    ]
    assert papers
    assert all("hardware_or_process_assumptions" in paper["supplementary_condition_fields"] for paper in papers)
    assert all(paper["supplementary_evidence_tier"] == "author_preprint" for paper in papers)
    assert all(paper["supplementary_source_locators"] for paper in papers)
    assert all(paper["supplementary_review_status"] == "pending" for paper in papers)

    codo = [
        paper
        for direction in result["directions"]
        for paper in direction["papers"]
        if paper["paper_id"] == "isca-2026-program-002"
    ]
    assert codo
    assert all("workload_or_design_corpus" in paper["supplementary_condition_fields"] for paper in codo)
    assert all(paper["supplementary_evidence_tier"] == "author_preprint" for paper in codo)

    cosm = [
        paper
        for direction in result["directions"]
        for paper in direction["papers"]
        if paper["paper_id"] == "isca-2026-program-003"
    ]
    assert cosm
    assert all("hardware_or_process_assumptions" in paper["supplementary_condition_fields"] for paper in cosm)
    assert all("workload_or_design_corpus" in paper["supplementary_condition_fields"] for paper in cosm)
    assert all(paper["supplementary_evidence_tier"] == "author_preprint" for paper in cosm)
    assert all(paper["supplementary_source_locators"] for paper in cosm)

    cerberus = [
        paper
        for direction in result["directions"]
        for paper in direction["papers"]
        if paper["paper_id"] == "isca-2026-program-004"
    ]
    assert cerberus
    assert all("hardware_or_process_assumptions" in paper["supplementary_condition_fields"] for paper in cerberus)
    assert all("workload_or_design_corpus" in paper["supplementary_condition_fields"] for paper in cerberus)
    assert all(paper["supplementary_evidence_tier"] == "author_preprint" for paper in cerberus)
    assert all(paper["supplementary_source_locators"] for paper in cerberus)

    pudghost = [
        paper
        for direction in result["directions"]
        for paper in direction["papers"]
        if paper["paper_id"] == "isca-2026-program-024"
    ]
    assert pudghost
    assert all(paper["supplementary_evidence_tier"] == "author_preprint" for paper in pudghost)
    assert all(paper["supplementary_review_status"] == "pending" for paper in pudghost)
    assert all("Abstract: 96 real DDR4 chips from 12 modules" in paper["supplementary_source_locators"] for paper in pudghost)

    cassandra = [
        paper
        for direction in result["directions"]
        for paper in direction["papers"]
        if paper["paper_id"] == "isca-2026-program-006"
    ]
    assert cassandra
    assert all("hardware_or_process_assumptions" in paper["supplementary_condition_fields"] for paper in cassandra)
    assert all("workload_or_design_corpus" in paper["supplementary_condition_fields"] for paper in cassandra)
    assert all(paper["supplementary_evidence_tier"] == "author_preprint" for paper in cassandra)
    assert all("Sections VI-A to VI-D; Tables III-V" in paper["supplementary_source_locators"] for paper in cassandra)

    disdp = [
        paper
        for direction in result["directions"]
        for paper in direction["papers"]
        if paper["paper_id"] == "isca-2026-program-155"
    ]
    assert disdp
    assert all("hardware_or_process_assumptions" in paper["supplementary_condition_fields"] for paper in disdp)
    assert all("workload_or_design_corpus" in paper["supplementary_condition_fields"] for paper in disdp)
    assert all(paper["supplementary_evidence_tier"] == "author_preprint" for paper in disdp)
    assert all("Sections IV-F to IV-I; Tables VIII-IX" in paper["supplementary_source_locators"] for paper in disdp)

    patterns = [
        paper
        for direction in result["directions"]
        for paper in direction["papers"]
        if paper["paper_id"] == "isca-2026-program-005"
    ]
    assert patterns
    assert all("workload_or_design_corpus" in paper["supplementary_condition_fields"] for paper in patterns)
    assert all(paper["supplementary_evidence_tier"] == "author_preprint" for paper in patterns)
    assert all(paper["supplementary_source_locators"] for paper in patterns)

    mapping = [
        paper
        for direction in result["directions"]
        for paper in direction["papers"]
        if paper["paper_id"] == "dac-2026-research535"
    ]
    assert mapping
    assert all("hardware_or_process_assumptions" in paper["supplementary_condition_fields"] for paper in mapping)
    assert all("workload_or_design_corpus" in paper["supplementary_condition_fields"] for paper in mapping)
    assert all(paper["supplementary_evidence_tier"] == "author_preprint" for paper in mapping)

    pareto = [
        paper
        for direction in result["directions"]
        for paper in direction["papers"]
        if paper["paper_id"] == "dac-2026-research865"
    ]
    assert pareto
    assert all("hardware_or_process_assumptions" in paper["supplementary_condition_fields"] for paper in pareto)
    assert all("workload_or_design_corpus" in paper["supplementary_condition_fields"] for paper in pareto)
    assert all(paper["supplementary_evidence_tier"] == "public_research_artifact" for paper in pareto)

    exact_t = [
        paper
        for direction in result["directions"]
        for paper in direction["papers"]
        if paper["paper_id"] == "dac-2026-research031"
    ]
    assert exact_t
    assert all("hardware_or_process_assumptions" in paper["supplementary_condition_fields"] for paper in exact_t)
    assert all("workload_or_design_corpus" in paper["supplementary_condition_fields"] for paper in exact_t)
    assert all(paper["supplementary_evidence_tier"] == "author_preprint" for paper in exact_t)

    energon = [
        paper
        for direction in result["directions"]
        for paper in direction["papers"]
        if paper["paper_id"] == "iccad-2025-1000"
    ]
    assert energon
    assert all("hardware_or_process_assumptions" in paper["supplementary_condition_fields"] for paper in energon)
    assert all("workload_or_design_corpus" in paper["supplementary_condition_fields"] for paper in energon)
    assert all(paper["supplementary_evidence_tier"] == "author_preprint" for paper in energon)
    assert all("hardware" not in paper["combined_missing_conditions"] for paper in energon)
