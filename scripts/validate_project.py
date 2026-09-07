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
    inventory_rows = [
        row
        for path in sorted(root.glob("*/data/papers-*-program.jsonl"))
        for row in read_jsonl(path)
    ]
    queue_rows = read_jsonl(root / "data/research-work-queue.jsonl")
    inventory_ids = {row.get("paper_id") for row in inventory_rows}
    queue_ids = {row.get("paper_id") for row in queue_rows}
    queue_required = {"paper_id", "collection_status", "coding_status", "next_actions", "priority_reasons"}
    coded_rows = [row for path in sorted(root.glob("*/data/adjudicated-*.jsonl")) for row in read_jsonl(path)]
    coded_ids = {row.get("paper_id") for row in coded_rows}
    packet_rows = [json.loads(path.read_text(encoding="utf-8")) for path in sorted((root / "data/review-packets").glob("*.json"))]
    packet_ids = {row.get("paper_id") for row in packet_rows}
    checks = {
        "three_conferences_registered": len(conferences) == 3,
        "conference_folders_present": all((root / item["folder"]).is_dir() for item in conferences),
        "taxonomy_has_themes": bool(taxonomy.get("themes")) and len(taxonomy["themes"]) == 10,
        "each_conference_has_source_ledger": all((root / item["folder"] / "data/sources.jsonl").exists() for item in conferences),
        "paper_seed_records_valid": all(row.get("paper_id") and row.get("conference_id") and row.get("title") and row.get("publisher_url") for row in read_jsonl(root / "dac/data/papers.jsonl")),
        "paper_level_queue_covers_inventory": len(inventory_rows) == 1589 and len(queue_rows) == 1589 and inventory_ids == queue_ids and all(queue_required <= row.keys() for row in queue_rows),
        "full_inventory_theme_routing_is_metadata_only": (root / "reports/inventory-theme-routing-v1.json").exists() and (lambda routing: routing.get("schema") == "inventory-theme-routing.v1" and routing.get("status") == "metadata_only_review_routing" and routing.get("inventory_count") == 1589 and routing.get("routed_count", 0) + routing.get("unrouted_count", 0) == 1589 and "abstract/full-text" in " ".join(routing.get("limits", [])))(json.loads((root / "reports/inventory-theme-routing-v1.json").read_text(encoding="utf-8"))) and (root / "reports/inventory-theme-routing-v1.md").exists(),
        "review_packets_cover_coded_records_without_acceptance": len(coded_rows) == 551 and coded_ids == packet_ids and len(packet_rows) == 551 and all(row.get("review_status") == "not_reviewed" and not row.get("independent_verdicts") for row in packet_rows),
        "completion_audit_is_honest": (root / "reports/completion-audit-v1.json").exists() and json.loads((root / "reports/completion-audit-v1.json").read_text(encoding="utf-8")).get("status") == "bounded_package_complete_scientific_gates_open" and any(item.get("status") == "prepared_pending" for item in json.loads((root / "reports/completion-audit-v1.json").read_text(encoding="utf-8")).get("subgoals", [])),
        "independent_review_handoff_is_honest": (root / "reports/independent-review-handoff-v1.md").exists() and "prepared, not independently reviewed" in (root / "reports/independent-review-handoff-v1.md").read_text(encoding="utf-8") and "zero\nindependent acceptances" in (root / "reports/independent-review-handoff-v1.md").read_text(encoding="utf-8"),
        "package_release_is_bounded": (root / "reports/package-release-v1.md").exists() and "bounded evidence assessment" in (root / "reports/package-release-v1.md").read_text(encoding="utf-8") and "does not support venue-wide prevalence" in (root / "reports/package-release-v1.md").read_text(encoding="utf-8"),
        "review_assignments_are_complete_without_verdicts": (root / "reports/independent-review-assignments-v1.json").exists() and (lambda assignment: assignment.get("packet_count") == 551 and assignment.get("independent_verdict_count") == 0 and len(assignment.get("assignments", [])) == 551 and all(item.get("review_status") == "awaiting_external_review" and not item.get("verdicts") for item in assignment.get("assignments", [])))(json.loads((root / "reports/independent-review-assignments-v1.json").read_text(encoding="utf-8"))),
        "iccad_target_and_fallback_explicit": register["conferences"][2].get("target_edition") == "2026" and register["conferences"][2].get("paper_analysis_edition") == "2025",
        "iccad_2026_availability_check_present": (root / "iccad/reports/2026-availability-check-2026-09-06.md").exists() and "paper corpus was not available" in (root / "iccad/reports/2026-availability-check-2026-09-06.md").read_text(encoding="utf-8"),
        "isca_program_signals_provenanced": all(row.get("source_id") in source_ids(root, "isca") and row.get("record_status") == "program_metadata_only" for row in read_jsonl(root / "isca/data/program-papers.jsonl")),
        "isca_indexed_evidence_is_labeled": all(row.get("source_id") in source_ids(root, "isca") and row.get("evidence_quality") == "secondary_indexed_excerpt" and row.get("adjudication_status") == "pending_primary_verification" for row in read_jsonl(root / "isca/data/indexed-evidence.jsonl")),
        "cross_conference_matrix_is_provisional": (root / "data/cross-conference-matrix-v0.json").exists() and json.loads((root / "data/cross-conference-matrix-v0.json").read_text(encoding="utf-8")).get("status") == "provisional_synthesis",
        "conference_deep_pages_present": all((root / folder / "pages").is_dir() and any((root / folder / "pages").glob("*.md")) for folder in ["isca", "dac", "iccad"]),
        "learning_index_present": (root / "reports/learning-index-v0.md").exists(),
        "reproducibility_manifest_present": (root / "reports/reproducibility-manifest-v1.json").exists() and json.loads((root / "reports/reproducibility-manifest-v1.json").read_text(encoding="utf-8")).get("status") == "dated_package_checkpoint" and len(json.loads((root / "reports/reproducibility-manifest-v1.json").read_text(encoding="utf-8")).get("commands", [])) >= 8 and len(json.loads((root / "reports/reproducibility-manifest-v1.json").read_text(encoding="utf-8")).get("artifact_hashes", [])) >= 25,
        "taxonomy_coding_guide_present": (root / "reports/taxonomy-coding-guide-v1.md").exists() and "Adjudication boundary tests" in (root / "reports/taxonomy-coding-guide-v1.md").read_text(encoding="utf-8"),
        "adversarial_judge_protocol_present": (root / "reports/adversarial-judge-protocol-v1.md").exists() and "Hostile judge prompt" in (root / "reports/adversarial-judge-protocol-v1.md").read_text(encoding="utf-8"),
        "evidence_summary_present": (root / "reports/evidence-summary-v1.json").exists() and json.loads((root / "reports/evidence-summary-v1.json").read_text(encoding="utf-8")).get("record_count") == 551,
        "dysharp_primary_coding_registered": all(row.get("evidence_source_id") in source_ids(root, "isca") and row.get("evidence_url") and row.get("problem") and row.get("method_or_artifact") and row.get("evidence_locators") and row.get("limits") and row.get("independent_review_status") == "pending" for row in read_jsonl(root / "isca/data/adjudicated-2026-batch-9.jsonl")),
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
        "temporal_insufficiency_findings_present": (root / "reports/temporal-insufficiency-v1.json").exists() and json.loads((root / "reports/temporal-insufficiency-v1.json").read_text(encoding="utf-8")).get("status") == "insufficient_evidence_for_directional_claims" and len(json.loads((root / "reports/temporal-insufficiency-v1.json").read_text(encoding="utf-8")).get("findings", [])) == 6 and all(item.get("status") == "insufficient_evidence" for item in json.loads((root / "reports/temporal-insufficiency-v1.json").read_text(encoding="utf-8")).get("findings", [])),
        "title_shift_candidates_are_labeled": (root / "reports/title-shift-candidates-v1.json").exists() and json.loads((root / "reports/title-shift-candidates-v1.json").read_text(encoding="utf-8")).get("status") == "exploratory_metadata_only" and (root / "reports/title-shift-candidates-v1.md").exists() and "not a" in (root / "reports/title-shift-candidates-v1.md").read_text(encoding="utf-8"),
        "isca_crossref_metadata_reconciled": normalized_metadata_rows(read_jsonl(root / "isca/data/crossref-metadata-2026.jsonl")) and len(read_jsonl(root / "isca/data/crossref-metadata-2026.jsonl")) >= 150 and all(row.get("source_id") in source_ids(root, "isca") and row.get("record_status") == "doi_metadata_only" and row.get("doi") and row.get("publisher_url") for row in read_jsonl(root / "isca/data/crossref-metadata-2026.jsonl")),
        "isca_adjudicated_batch_has_primary_evidence": all(row.get("evidence_source_id") in source_ids(root, "isca") and row.get("evidence_url") and row.get("problem") and row.get("method_or_artifact") and row.get("metrics") and row.get("limits") for path in (root / "isca/data/adjudicated-2026-batch.jsonl", root / "isca/data/adjudicated-2026-batch-2.jsonl", root / "isca/data/adjudicated-2026-batch-3.jsonl", root / "isca/data/adjudicated-2026-batch-4.jsonl", root / "isca/data/adjudicated-2026-batch-5.jsonl", root / "isca/data/adjudicated-2026-batch-6.jsonl", root / "isca/data/adjudicated-2026-batch-7.jsonl", root / "isca/data/adjudicated-2026-batch-8.jsonl") for row in read_jsonl(path)),
        "dac_program_capture_present": program_rows_valid(read_jsonl(root / "dac/data/program-presentations.jsonl")) and all(row.get("record_status") == "program_metadata_only" and row.get("program_url") for row in read_jsonl(root / "dac/data/program-presentations.jsonl")) and normalized_metadata_rows(read_jsonl(root / "dac/data/papers-2026-program.jsonl")),
        "dac_historical_program_inventory_present": normalized_metadata_rows(read_jsonl(root / "dac/data/papers-2025-program.jsonl")) and len(read_jsonl(root / "dac/data/papers-2025-program.jsonl")) >= 400 and all(row.get("target_edition") == 2025 and row.get("analysis_edition") == 2025 and row.get("access_status") == "official_historical_program_metadata_only" and row.get("record_status") == "historical_program_metadata_only" for row in read_jsonl(root / "dac/data/papers-2025-program.jsonl")),
        "dac_historical_evidence_coverage_is_explicit": len(read_jsonl(root / "dac/data/paper-evidence-2025.jsonl")) == len(read_jsonl(root / "dac/data/papers-2025-program.jsonl")) and all(row.get("evidence_source_id") == "dac-2025-presentation-pages" and row.get("capture_status") in {"captured_substantive", "captured_challenge_or_empty", "not_captured_rate_limited"} for row in read_jsonl(root / "dac/data/paper-evidence-2025.jsonl")) and sum(row.get("evidence_status") == "substantive_description" for row in read_jsonl(root / "dac/data/paper-evidence-2025.jsonl")) >= 20,
        "dac_historical_track_baseline_present": (root / "dac/data/track-baseline-2025.json").exists() and json.loads((root / "dac/data/track-baseline-2025.json").read_text(encoding="utf-8")).get("record_count") == 419 and json.loads((root / "dac/data/track-baseline-2025.json").read_text(encoding="utf-8")).get("records_with_track_assignment") == 419,
        "dac_current_track_baseline_present": (root / "dac/data/track-baseline-2026.json").exists() and json.loads((root / "dac/data/track-baseline-2026.json").read_text(encoding="utf-8")).get("record_count") == 543 and json.loads((root / "dac/data/track-baseline-2026.json").read_text(encoding="utf-8")).get("records_with_track_assignment") == 543 and "labels were not present" in json.loads((root / "dac/data/track-baseline-2026.json").read_text(encoding="utf-8")).get("limits", ""),
        "dac_paper_evidence_capture_present": all(row.get("fetch_status") in {"ok", "error"} and row.get("evidence_url") for row in read_jsonl(root / "dac/data/paper-evidence-2026.jsonl")),
        "dac_adjudicated_batch_has_evidence": all(row.get("evidence_url") and row.get("evidence_span") and row.get("problem") and row.get("method_or_artifact") and row.get("limits") for path in (root / "dac/data/adjudicated-2026-batch.jsonl", root / "dac/data/adjudicated-2026-batch-2.jsonl", root / "dac/data/adjudicated-2026-batch-3.jsonl", root / "dac/data/adjudicated-2026-batch-4.jsonl", root / "dac/data/adjudicated-2026-batch-5.jsonl", root / "dac/data/adjudicated-2026-batch-6.jsonl", root / "dac/data/adjudicated-2026-batch-7.jsonl", root / "dac/data/adjudicated-2026-batch-8.jsonl", root / "dac/data/adjudicated-2026-batch-9.jsonl", root / "dac/data/adjudicated-2026-batch-10.jsonl", root / "dac/data/adjudicated-2026-batch-11.jsonl", root / "dac/data/adjudicated-2026-batch-12.jsonl", root / "dac/data/adjudicated-2026-batch-13.jsonl", root / "dac/data/adjudicated-2026-batch-14.jsonl", root / "dac/data/adjudicated-2026-batch-15.jsonl", root / "dac/data/adjudicated-2026-batch-16.jsonl", root / "dac/data/adjudicated-2026-batch-17.jsonl", root / "dac/data/adjudicated-2026-batch-18.jsonl", root / "dac/data/adjudicated-2026-batch-19.jsonl", root / "dac/data/adjudicated-2026-batch-20.jsonl", root / "dac/data/adjudicated-2026-batch-21.jsonl", root / "dac/data/adjudicated-2026-batch-22.jsonl", root / "dac/data/adjudicated-2026-batch-23.jsonl", root / "dac/data/adjudicated-2026-batch-24.jsonl", root / "dac/data/adjudicated-2026-batch-25.jsonl", root / "dac/data/adjudicated-2026-batch-26.jsonl", root / "dac/data/adjudicated-2026-batch-27.jsonl", root / "dac/data/adjudicated-2026-batch-28.jsonl", root / "dac/data/adjudicated-2026-batch-29.jsonl", root / "dac/data/adjudicated-2026-batch-30.jsonl", root / "dac/data/adjudicated-2026-batch-31.jsonl", root / "dac/data/adjudicated-2026-batch-32.jsonl", root / "dac/data/adjudicated-2026-batch-33.jsonl", root / "dac/data/adjudicated-2026-batch-34.jsonl", root / "dac/data/adjudicated-2026-batch-35.jsonl", root / "dac/data/adjudicated-2026-batch-36.jsonl", root / "dac/data/adjudicated-2026-batch-37.jsonl", root / "dac/data/adjudicated-2026-batch-38.jsonl", root / "dac/data/adjudicated-2026-batch-39.jsonl", root / "dac/data/adjudicated-2026-batch-40.jsonl", root / "dac/data/adjudicated-2026-batch-41.jsonl", root / "dac/data/adjudicated-2026-batch-42.jsonl") for row in read_jsonl(path)),
        "dac_theme_triage_is_explicit": all(row.get("triage_status") == "keyword_routing_only" and row.get("classification_confidence") == "not_adjudicated" and row.get("limit") for row in read_jsonl(root / "dac/data/theme-triage-2026.jsonl")),
        "dac_batch_43_has_evidence": all(row.get("evidence_url") and row.get("evidence_span") and row.get("problem") and row.get("method_or_artifact") and row.get("limits") for row in read_jsonl(root / "dac/data/adjudicated-2026-batch-43.jsonl")),
        "dac_batch_44_has_evidence": all(row.get("evidence_url") and row.get("evidence_span") and row.get("problem") and row.get("method_or_artifact") and row.get("limits") for row in read_jsonl(root / "dac/data/adjudicated-2026-batch-44.jsonl")),
        "dac_batch_45_has_evidence": all(row.get("evidence_url") and row.get("evidence_span") and row.get("problem") and row.get("method_or_artifact") and row.get("limits") for row in read_jsonl(root / "dac/data/adjudicated-2026-batch-45.jsonl")),
        "dac_batch_46_has_evidence": all(row.get("evidence_url") and row.get("evidence_span") and row.get("problem") and row.get("method_or_artifact") and row.get("limits") for row in read_jsonl(root / "dac/data/adjudicated-2026-batch-46.jsonl")),
        "dac_batch_47_has_evidence": all(row.get("evidence_url") and row.get("evidence_span") and row.get("problem") and row.get("method_or_artifact") and row.get("limits") for row in read_jsonl(root / "dac/data/adjudicated-2026-batch-47.jsonl")),
        "dac_batch_48_has_evidence": all(row.get("evidence_url") and row.get("evidence_span") and row.get("problem") and row.get("method_or_artifact") and row.get("limits") for row in read_jsonl(root / "dac/data/adjudicated-2026-batch-48.jsonl")),
        "dac_batch_49_has_evidence": all(row.get("evidence_url") and row.get("evidence_span") and row.get("problem") and row.get("method_or_artifact") and row.get("limits") for row in read_jsonl(root / "dac/data/adjudicated-2026-batch-49.jsonl")),
        "dac_batch_50_has_evidence": all(row.get("evidence_url") and row.get("evidence_span") and row.get("problem") and row.get("method_or_artifact") and row.get("limits") for row in read_jsonl(root / "dac/data/adjudicated-2026-batch-50.jsonl")),
        "dac_batch_51_has_evidence": all(row.get("evidence_url") and row.get("evidence_span") and row.get("problem") and row.get("method_or_artifact") and row.get("limits") for row in read_jsonl(root / "dac/data/adjudicated-2026-batch-51.jsonl")),
        "dac_batch_52_has_evidence": all(row.get("evidence_url") and row.get("evidence_span") and row.get("problem") and row.get("method_or_artifact") and row.get("limits") for row in read_jsonl(root / "dac/data/adjudicated-2026-batch-52.jsonl")),
    }
    return {"contract": "semiconductor-conference-scaffold.v1", "status": "passed" if all(checks.values()) else "failed", "checks": checks, "conference_count": len(conferences), "taxonomy_theme_count": len(taxonomy.get("themes", []))}


if __name__ == "__main__":
    result = validate()
    print(json.dumps(result, indent=2, sort_keys=True))
    raise SystemExit(0 if result["status"] == "passed" else 1)
