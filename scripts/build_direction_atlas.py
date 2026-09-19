"""Build the machine-readable, page-backed long-term direction atlas."""
from __future__ import annotations

import json
from pathlib import Path


PAGE_ROOT = "reports/directions"

# These are deliberately maintained here as the conceptual layer. Paper IDs and
# evidence tiers come from data/technology-direction-evidence-v1.json; they are
# never retyped into the atlas.
DIRECTION_CONFIG = {
    "constraints-become-executable": {
        "source_direction_ids": ["tool-grounded-ai-design-verification"],
        "page": "01-constraints-become-executable.md",
        "first_principle": "A candidate is useful only when executable constraints can reject, repair, or rank it.",
        "page_backed_sources": [
            "reports/directions/01-constraints-become-executable.md",
            "dac/pages/ai-eda-and-accelerator-evidence-batch.md",
            "iccad/pages/topical-capability-map-2025-fallback.md",
            "isca/pages/codo-dataflow-compiler.md",
        ],
        "challenge_direction_number": 1,
        "next_evidence_action": "Compare accepted designs, failed attempts, regressions, checker state, and transfer at equal synthesis, model-call, retry, and wall-clock budgets.",
    },
    "data-movement-as-contract": {
        "source_direction_ids": ["data-movement-as-contract", "workload-specialized-accelerators"],
        "page": "02-data-movement-as-contract.md",
        "first_principle": "Useful computation is constrained by where data is, how far it moves, and what competes for the path.",
        "page_backed_sources": [
            "reports/directions/02-data-movement-as-contract.md",
            "dac/pages/data-movement-memory-and-integration.md",
            "isca/pages/llm-memory-and-wafer-scale-v0.md",
            "isca/pages/memory-ecc-pim-reliability.md",
        ],
        "challenge_direction_number": 2,
        "next_evidence_action": "Sweep resident and nonresident working sets, locality, contention, recall/accuracy, equal capacity/bandwidth, and host/migration overhead.",
    },
    "reliability-security-upstream": {
        "source_direction_ids": ["reliability-security-design-loop"],
        "page": "04-reliability-security-upstream.md",
        "first_principle": "Performance without a declared fault and threat operating envelope is not a complete system result.",
        "page_backed_sources": [
            "reports/directions/04-reliability-security-upstream.md",
            "dac/pages/reliability-security-and-verification.md",
            "isca/pages/memory-ecc-pim-reliability.md",
            "iccad/pages/ai-and-security-evidence-batch.md",
        ],
        "challenge_direction_number": 3,
        "next_evidence_action": "Require threat/fault model, coverage, false negatives, recovery path, and useful performance after protection for each anchor.",
    },
    "physical-reality-in-the-loop": {
        "source_direction_ids": ["physical-integration-optimization-variable"],
        "page": "05-physical-reality-in-the-loop.md",
        "first_principle": "An abstract optimum is irrelevant when the physical system cannot realize it.",
        "page_backed_sources": [
            "reports/directions/05-physical-reality-in-the-loop.md",
            "iccad/pages/topical-capability-map-2025-fallback.md",
            "dac/pages/evidence-batch-3.md",
        ],
        "challenge_direction_number": 4,
        "next_evidence_action": "Compare selected and rejected candidates with held-out higher-fidelity solvers or measurements; report ranking error, violations, and search cost.",
    },
    "closed-loop-design": {
        "source_direction_ids": ["multifidelity-physics-aware-search"],
        "page": "03-closed-loop-design.md",
        "first_principle": "A design loop is only useful when sensing cost, model error, decision latency, and update semantics are explicit.",
        "page_backed_sources": [
            "reports/directions/03-closed-loop-design.md",
            "dac/pages/topical-capability-map-2026.md",
            "iccad/pages/topical-capability-map-2025-fallback.md",
            "reports/direction-challenges-v1.md",
        ],
        "challenge_direction_number": 5,
        "next_evidence_action": "Compare final feasible solutions at equal wall-clock and simulator budgets, including calibration cost, rejected candidates, and out-of-distribution error.",
    },
    "evaluation-as-research": {
        "source_direction_ids": ["tool-grounded-ai-design-verification", "multifidelity-physics-aware-search"],
        "page": "06-evaluation-as-research.md",
        "first_principle": "Every result is a measurement with a task population, evaluator, result, uncertainty, and failure boundary.",
        "page_backed_sources": [
            "reports/directions/06-evaluation-as-research.md",
            "dac/pages/ai-eda-and-accelerator-evidence-batch.md",
            "iccad/pages/ai-and-security-evidence-batch.md",
            "reports/adversarial-judge-protocol-v1.md",
            "reports/direction-challenges-v1.md",
        ],
        "challenge_direction_number": 6,
        "next_evidence_action": "Require each accepted direction claim to carry task population, evaluator version, failure semantics, baseline, budget, and independent review status.",
    },
}


def build(root: Path) -> dict:
    evidence_payload = json.loads(
        (root / "data/technology-direction-evidence-v1.json").read_text(encoding="utf-8")
    )
    challenge_payload = json.loads(
        (root / "data/direction-challenges-v1.json").read_text(encoding="utf-8")
    )
    challenge_packets = {
        row["paper_id"]: row
        for row in (
            json.loads(line)
            for line in (root / challenge_payload["source_packet_path"]).read_text(encoding="utf-8").splitlines()
            if line.strip()
        )
    }
    challenges = {row["direction_number"]: row for row in challenge_payload["cases"]}

    directions = []
    source_by_id = {source["direction_id"]: source for source in evidence_payload["directions"]}
    for direction_id, config in DIRECTION_CONFIG.items():
        challenge = challenges[config["challenge_direction_number"]]
        challenge_packet = challenge_packets.get(challenge["paper_id"], {})
        page_path = root / config["page_backed_sources"][0]
        if not page_path.exists():
            raise ValueError(f"Missing canonical direction page: {page_path}")
        evidence = []
        seen_papers = set()
        for source_direction_id in config["source_direction_ids"]:
            source = source_by_id[source_direction_id]
            for item in source.get("evidence", []):
                if item["paper_id"] in seen_papers:
                    continue
                seen_papers.add(item["paper_id"])
                evidence.append(
                    {
                        "paper_id": item["paper_id"],
                        "conference_id": item["conference_id"],
                        "edition": item["analysis_edition"],
                        "evidence_tier": item["evidence_tier"],
                        "source_direction_id": source_direction_id,
                        "mapping_review_status": item.get("mapping_review_status", "not_recorded"),
                        "headline_metric_status": item.get("headline_metric_status", "not_recorded"),
                    }
                )
        directions.append(
            {
                "direction_id": direction_id,
                "label": direction_id.replace("-", " ").title(),
                "source_direction_ids": config["source_direction_ids"],
                "page": f"{PAGE_ROOT}/{config['page']}",
                "first_principle": config["first_principle"],
                "subskills": source.get("subskills", []),
                "evidence": evidence,
                "challenge": {
                    "paper_id": challenge["paper_id"],
                    "evidence_tier": challenge["evidence_tier"],
                    "source_url": challenge_packet.get("original_source_url"),
                "relation": challenge["relation"],
                "qualification": challenge["qualification"],
                "failure_condition": challenge["failure_condition"],
                "next_evidence": challenge["next_evidence"],
                },
                "page_backed_sources": config["page_backed_sources"],
                "next_evidence_action": config["next_evidence_action"],
                "limits": " ".join(source_by_id[source_id].get("limits", "") for source_id in config["source_direction_ids"]),
                "status": "provisional_mechanism_hypothesis",
                "independent_review_count": sum(
                    item.get("mapping_review_status") == "independent_reviewed"
                    for item in evidence
                ),
            }
        )

    result = {
        "schema": "long-term-direction-atlas.v1",
        "status": "provisional_page_backed_mechanism_atlas",
        "as_of": evidence_payload.get("as_of"),
        "source_evidence_map": "data/technology-direction-evidence-v1.json",
        "source_challenge_map": "data/direction-challenges-v1.json",
        "directions": directions,
        "interpretation_limits": [
            "Direction counts are selected evidence references, not prevalence or market share.",
            "A primary, artifact, company, or author source is not independent validation.",
            "Challenge cases add counterpressure; they do not falsify a direction without matched evidence.",
            "Temporal claims require comparable editions, evidence tiers, missingness analysis, and independent review.",
        ],
    }
    output = root / "data/long-term-direction-atlas-v1.json"
    output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return result


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    args = parser.parse_args()
    built = build(args.root)
    print(json.dumps({"status": "built", "directions": len(built["directions"]), "output": "data/long-term-direction-atlas-v1.json"}, indent=2))
