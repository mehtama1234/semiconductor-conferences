#!/usr/bin/env python3
"""Validate the semiconductor-conference research scaffold and evidence ledgers."""
from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def read_jsonl(path: Path) -> list[dict]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def source_ids(root: Path, conference: str) -> set[str]:
    return {row["source_id"] for row in read_jsonl(root / conference / "data/sources.jsonl")}


def normalized_metadata_rows(rows: list[dict]) -> bool:
    required = {"paper_id", "conference_id", "analysis_edition", "title", "authors", "publisher_url", "collection_date", "access_status", "theme_id", "subtheme_id", "subsubtheme_id", "limits"}
    return bool(rows) and all(required <= row.keys() for row in rows)


def program_rows_valid(rows: list[dict]) -> bool:
    required = {"presentation_id", "conference_id", "title", "program_url", "source_url", "record_status", "evidence_limit"}
    return bool(rows) and all(required <= row.keys() for row in rows)


def validate(root: Path = ROOT) -> dict:
    register = json.loads((root / "data/conference-register.json").read_text(encoding="utf-8"))
    taxonomy = json.loads((root / "data/taxonomy-v0.json").read_text(encoding="utf-8"))
    conferences = register["conferences"]
    checks = {
        "three_conferences_registered": len(conferences) == 3,
        "conference_folders_present": all((root / item["folder"]).is_dir() for item in conferences),
        "taxonomy_has_themes": bool(taxonomy.get("themes")) and len(taxonomy["themes"]) == 10,
        "each_conference_has_source_ledger": all((root / item["folder"] / "data/sources.jsonl").exists() for item in conferences),
        "paper_seed_records_valid": all(row.get("paper_id") and row.get("conference_id") and row.get("title") and row.get("publisher_url") for row in read_jsonl(root / "dac/data/papers.jsonl")),
        "iccad_target_and_fallback_explicit": register["conferences"][2].get("target_edition") == "2026" and register["conferences"][2].get("paper_analysis_edition") == "2025",
        "iccad_2026_availability_check_present": (root / "iccad/reports/2026-availability-check-2026-09-06.md").exists() and "paper corpus was not available" in (root / "iccad/reports/2026-availability-check-2026-09-06.md").read_text(encoding="utf-8"),
        "isca_program_signals_provenanced": all(row.get("source_id") in source_ids(root, "isca") and row.get("record_status") == "program_metadata_only" for row in read_jsonl(root / "isca/data/program-papers.jsonl")),
        "isca_indexed_evidence_is_labeled": all(row.get("source_id") in source_ids(root, "isca") and row.get("evidence_quality") == "secondary_indexed_excerpt" and row.get("adjudication_status") == "pending_primary_verification" for row in read_jsonl(root / "isca/data/indexed-evidence.jsonl")),
        "cross_conference_matrix_is_provisional": (root / "data/cross-conference-matrix-v0.json").exists() and json.loads((root / "data/cross-conference-matrix-v0.json").read_text(encoding="utf-8")).get("status") == "provisional_synthesis",
        "conference_deep_pages_present": all((root / folder / "pages").is_dir() and any((root / folder / "pages").glob("*.md")) for folder in ["isca", "dac", "iccad"]),
        "learning_index_present": (root / "reports/learning-index-v0.md").exists(),
        "taxonomy_coding_guide_present": (root / "reports/taxonomy-coding-guide-v1.md").exists() and "Adjudication boundary tests" in (root / "reports/taxonomy-coding-guide-v1.md").read_text(encoding="utf-8"),
        "adversarial_judge_protocol_present": (root / "reports/adversarial-judge-protocol-v1.md").exists() and "Hostile judge prompt" in (root / "reports/adversarial-judge-protocol-v1.md").read_text(encoding="utf-8"),
        "evidence_summary_present": (root / "reports/evidence-summary-v1.json").exists() and json.loads((root / "reports/evidence-summary-v1.json").read_text(encoding="utf-8")).get("record_count") == 69,
        "adversarial_review_status_is_honest": (root / "reports/adversarial-review-status-v1.md").exists() and "not an independent adversarial LLM judgment" in (root / "reports/adversarial-review-status-v1.md").read_text(encoding="utf-8"),
        "evidence_taxonomy_present": json.loads((root / "data/taxonomy-v1-evidence.json").read_text(encoding="utf-8")).get("taxonomy_version") == "v1-evidence-derived",
        "adversarial_preflight_present": json.loads((root / "reports/adversarial-preflight-v0.json").read_text(encoding="utf-8")).get("judge_mode") == "deterministic_preflight_not_llm",
        "dac_program_signals_provenanced": all(row.get("source_id") in source_ids(root, "dac") and row.get("evidence_status") == "program_signal_only" for row in read_jsonl(root / "dac/data/program-signals.jsonl")),
        "iccad_scope_signals_provenanced": all(row.get("source_id") in source_ids(root, "iccad") and row.get("evidence_status") == "scope_signal_only" for row in read_jsonl(root / "iccad/data/program-signals.jsonl")),
        "iccad_fallback_paper_metadata_present": normalized_metadata_rows(read_jsonl(root / "iccad/data/papers-2025-program.jsonl")) and all(row.get("target_edition") == 2026 and row.get("analysis_edition") == 2025 and row.get("access_status") == "official_fallback_program_pdf_metadata_only" for row in read_jsonl(root / "iccad/data/papers-2025-program.jsonl")),
        "iccad_adjudicated_batch_has_primary_evidence": all(row.get("evidence_source_id") in source_ids(root, "iccad") and row.get("problem") and row.get("method_or_artifact") and row.get("limits") for path in (root / "iccad/data/adjudicated-2025-batch.jsonl", root / "iccad/data/adjudicated-2025-batch-2.jsonl") for row in read_jsonl(path)),
        "isca_normalized_metadata_present": normalized_metadata_rows(read_jsonl(root / "isca/data/papers.jsonl")),
        "isca_program_inventory_present": normalized_metadata_rows(read_jsonl(root / "isca/data/papers-2026-program.jsonl")) and len(read_jsonl(root / "isca/data/papers-2026-program.jsonl")) >= 100 and all(row.get("access_status") == "official_program_metadata_only" for row in read_jsonl(root / "isca/data/papers-2026-program.jsonl")),
        "isca_historical_program_inventory_present": normalized_metadata_rows(read_jsonl(root / "isca/data/papers-2025-program.jsonl")) and len(read_jsonl(root / "isca/data/papers-2025-program.jsonl")) >= 100 and all(row.get("target_edition") == 2025 and row.get("analysis_edition") == 2025 and row.get("access_status") == "official_historical_program_metadata_only" and row.get("record_status") == "historical_program_metadata_only" for row in read_jsonl(root / "isca/data/papers-2025-program.jsonl")),
        "temporal_baseline_present": (root / "reports/temporal-baseline-v1.md").exists() and "No claim that a topic is rising" in (root / "reports/temporal-baseline-v1.md").read_text(encoding="utf-8"),
        "title_shift_candidates_are_labeled": (root / "reports/title-shift-candidates-v1.json").exists() and json.loads((root / "reports/title-shift-candidates-v1.json").read_text(encoding="utf-8")).get("status") == "exploratory_metadata_only" and (root / "reports/title-shift-candidates-v1.md").exists() and "not a" in (root / "reports/title-shift-candidates-v1.md").read_text(encoding="utf-8"),
        "isca_crossref_metadata_reconciled": normalized_metadata_rows(read_jsonl(root / "isca/data/crossref-metadata-2026.jsonl")) and len(read_jsonl(root / "isca/data/crossref-metadata-2026.jsonl")) >= 150 and all(row.get("source_id") in source_ids(root, "isca") and row.get("record_status") == "doi_metadata_only" and row.get("doi") and row.get("publisher_url") for row in read_jsonl(root / "isca/data/crossref-metadata-2026.jsonl")),
        "isca_adjudicated_batch_has_primary_evidence": all(row.get("evidence_source_id") in source_ids(root, "isca") and row.get("evidence_url") and row.get("problem") and row.get("method_or_artifact") and row.get("metrics") and row.get("limits") for path in (root / "isca/data/adjudicated-2026-batch.jsonl", root / "isca/data/adjudicated-2026-batch-2.jsonl", root / "isca/data/adjudicated-2026-batch-3.jsonl", root / "isca/data/adjudicated-2026-batch-4.jsonl", root / "isca/data/adjudicated-2026-batch-5.jsonl", root / "isca/data/adjudicated-2026-batch-6.jsonl") for row in read_jsonl(path)),
        "dac_program_capture_present": program_rows_valid(read_jsonl(root / "dac/data/program-presentations.jsonl")) and all(row.get("record_status") == "program_metadata_only" and row.get("program_url") for row in read_jsonl(root / "dac/data/program-presentations.jsonl")) and normalized_metadata_rows(read_jsonl(root / "dac/data/papers-2026-program.jsonl")),
        "dac_historical_program_inventory_present": normalized_metadata_rows(read_jsonl(root / "dac/data/papers-2025-program.jsonl")) and len(read_jsonl(root / "dac/data/papers-2025-program.jsonl")) >= 400 and all(row.get("target_edition") == 2025 and row.get("analysis_edition") == 2025 and row.get("access_status") == "official_historical_program_metadata_only" and row.get("record_status") == "historical_program_metadata_only" for row in read_jsonl(root / "dac/data/papers-2025-program.jsonl")),
        "dac_historical_evidence_coverage_is_explicit": len(read_jsonl(root / "dac/data/paper-evidence-2025.jsonl")) == len(read_jsonl(root / "dac/data/papers-2025-program.jsonl")) and all(row.get("evidence_source_id") == "dac-2025-presentation-pages" and row.get("capture_status") in {"captured_substantive", "captured_challenge_or_empty", "not_captured_rate_limited"} for row in read_jsonl(root / "dac/data/paper-evidence-2025.jsonl")) and sum(row.get("evidence_status") == "substantive_description" for row in read_jsonl(root / "dac/data/paper-evidence-2025.jsonl")) >= 20,
        "dac_historical_track_baseline_present": (root / "dac/data/track-baseline-2025.json").exists() and json.loads((root / "dac/data/track-baseline-2025.json").read_text(encoding="utf-8")).get("record_count") == 419 and json.loads((root / "dac/data/track-baseline-2025.json").read_text(encoding="utf-8")).get("records_with_track_assignment") == 419,
        "dac_current_track_baseline_present": (root / "dac/data/track-baseline-2026.json").exists() and json.loads((root / "dac/data/track-baseline-2026.json").read_text(encoding="utf-8")).get("record_count") == 543 and json.loads((root / "dac/data/track-baseline-2026.json").read_text(encoding="utf-8")).get("records_with_track_assignment") == 543 and "labels were not present" in json.loads((root / "dac/data/track-baseline-2026.json").read_text(encoding="utf-8")).get("limits", ""),
        "dac_paper_evidence_capture_present": all(row.get("fetch_status") in {"ok", "error"} and row.get("evidence_url") for row in read_jsonl(root / "dac/data/paper-evidence-2026.jsonl")),
        "dac_adjudicated_batch_has_evidence": all(row.get("evidence_url") and row.get("evidence_span") and row.get("problem") and row.get("method_or_artifact") and row.get("limits") for path in (root / "dac/data/adjudicated-2026-batch.jsonl", root / "dac/data/adjudicated-2026-batch-2.jsonl", root / "dac/data/adjudicated-2026-batch-3.jsonl", root / "dac/data/adjudicated-2026-batch-4.jsonl") for row in read_jsonl(path)),
        "dac_theme_triage_is_explicit": all(row.get("triage_status") == "keyword_routing_only" and row.get("classification_confidence") == "not_adjudicated" and row.get("limit") for row in read_jsonl(root / "dac/data/theme-triage-2026.jsonl")),
    }
    return {"contract": "semiconductor-conference-scaffold.v1", "status": "passed" if all(checks.values()) else "failed", "checks": checks, "conference_count": len(conferences), "taxonomy_theme_count": len(taxonomy.get("themes", []))}


if __name__ == "__main__":
    result = validate()
    print(json.dumps(result, indent=2, sort_keys=True))
    raise SystemExit(0 if result["status"] == "passed" else 1)
