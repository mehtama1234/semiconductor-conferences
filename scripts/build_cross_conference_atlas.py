"""Build the structured cross-conference relationship atlas."""
from __future__ import annotations

import json
from collections import Counter
from pathlib import Path


VENUE_ROLES = {
    "constraints-become-executable": {
        "relation_type": "complementary_layering",
        "isca": "Architecture/compiler cases expose executable dataflow and system constraints.",
        "dac": "Design-automation cases provide broad tool-grounded generation, search, and mapping candidates.",
        "iccad": "Fallback cases expose verification, physical-flow, and design-method consequences.",
        "interpretation": "The venues support a shared mechanism of constraint-driven iteration, not one common benchmark or growth rate.",
        "next_comparison": "Match design suites, correctness oracle, synthesis budget, model/API cost, retries, and held-out transfer.",
    },
    "data-movement-as-contract": {
        "relation_type": "same_pressure_different_layer",
        "isca": "Systems and architecture cases expose expert traffic, collectives, KV locality, PIM scheduling, and deployed memory context.",
        "dac": "Memory and accelerator cases expose CXL, near-memory, PIM, buffering, and movement-aware execution mechanisms.",
        "iccad": "Physical-integration cases connect bandwidth and placement to 3D thermal and package constraints.",
        "interpretation": "The shared pressure is movement and contention; mechanisms and quality targets remain heterogeneous.",
        "next_comparison": "Match workload, recall/accuracy, resident set, capacity, bandwidth, topology, migration cost, and tail latency.",
    },
    "reliability-security-upstream": {
        "relation_type": "cross_layer_contract",
        "isca": "Architecture and memory cases expose correction, interference, and thermal behavior during execution.",
        "dac": "Accelerator and design-flow cases expose fault mitigation, physical integrity, attacks, and protection overhead.",
        "iccad": "Security and fallback design cases expose threat-model and validation boundaries, with broader physical-reliability scope.",
        "interpretation": "The venues converge on explicit operating envelopes, but fault, thermal, and threat models cannot be collapsed into one robustness score.",
        "next_comparison": "Match threat/fault model, coverage, false negatives, recovery cost, useful throughput, and availability impact.",
    },
    "physical-reality-in-the-loop": {
        "relation_type": "upstream_physical_feedback",
        "isca": "Selected runtime/system cases expose thermal imbalance and physical effects after mapping.",
        "dac": "Design-automation cases expose fast thermal, package, process, and physical models for search.",
        "iccad": "Physical-design fallback cases provide the deepest placement, process, device, and signoff-oriented evidence.",
        "interpretation": "The layering suggests physical models are becoming decision inputs, but model transfer and manufacturability remain open.",
        "next_comparison": "Compare candidate ranking, constraint violations, held-out high-fidelity evaluation, and search cost across geometry/process changes.",
    },
    "closed-loop-design": {
        "relation_type": "methodological_bridge",
        "isca": "The current selected source map has no direct ISCA evidence reference for this direction; compiler/system cases remain adjacent evidence.",
        "dac": "Search, surrogate, Bayesian, and tool-feedback cases provide the broadest loop inventory.",
        "iccad": "Design-space and physical-model cases expose fidelity, calibration, and downstream feasibility boundaries.",
        "interpretation": "This is a methodological bridge across venues, not evidence that the same adaptive loop dominates any venue.",
        "next_comparison": "Match total wall-clock/evaluation budget, calibration cost, rejected candidates, misranking, and out-of-distribution error.",
    },
    "evaluation-as-research": {
        "relation_type": "measurement_contract",
        "isca": "Artifact and system cases expose execution, workload, and reproducibility boundaries.",
        "dac": "Tool-grounded and benchmark cases expose task selection, search budget, and evaluator semantics.",
        "iccad": "Verification and physical-design cases expose proof state, simulator fidelity, and implementation boundaries.",
        "interpretation": "Evaluation is a cross-venue enabling layer; field direction cannot be inferred until evaluator populations and semantics are matched.",
        "next_comparison": "Require task population, evaluator/tool version, timeout/error semantics, baseline, budget, and independent rerun status.",
    },
}


def build(root: Path) -> dict:
    atlas = json.loads((root / "data/long-term-direction-atlas-v1.json").read_text(encoding="utf-8"))
    directions = []
    for source in atlas["directions"]:
        config = VENUE_ROLES[source["direction_id"]]
        counts = Counter(item["conference_id"] for item in source["evidence"])
        directions.append(
            {
                "direction_id": source["direction_id"],
                "label": source["label"],
                "page": source["page"],
                "relation_type": config["relation_type"],
                "conference_reference_counts": {venue: counts.get(venue, 0) for venue in ("isca", "dac", "iccad")},
                "venue_roles": {venue: config[venue] for venue in ("isca", "dac", "iccad")},
                "interpretation": config["interpretation"],
                "next_comparison": config["next_comparison"],
                "independent_review_count": source["independent_review_count"],
                "status": "provisional_cross_conference_case_evidence",
            }
        )
    result = {
        "schema": "cross-conference-direction-atlas.v1",
        "status": "provisional_cross_conference_synthesis",
        "as_of": atlas["as_of"],
        "source_atlas": "data/long-term-direction-atlas-v1.json",
        "directions": directions,
        "prohibited_inference": [
            "market share",
            "industrial adoption",
            "commercial success",
            "conference-wide ranking",
            "rising or declining direction without comparable historical snapshots",
        ],
    }
    (root / "data/cross-conference-direction-atlas-v1.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    lines = [
        "# Cross-conference direction atlas v1",
        "",
        "This is a structured comparison of what ISCA, DAC, and ICCAD contribute to each canonical direction. It distinguishes complementary layering, shared pressure, methodological bridges, and measurement contracts. It is not a venue ranking or temporal trend report.",
        "",
        "| Direction | Relation | ISCA | DAC | ICCAD | Reviews |",
        "|---|---|---:|---:|---:|---:|",
    ]
    for row in directions:
        counts = row["conference_reference_counts"]
        lines.append(f"| [{row['label']}]({row['page'].replace('reports/', '')}) | `{row['relation_type']}` | {counts['isca']} | {counts['dac']} | {counts['iccad']} | {row['independent_review_count']} |")
    for row in directions:
        lines += ["", f"## {row['label']}", "", f"Relation type: `{row['relation_type']}`.", "", "| Conference | Contribution in the current evidence |", "|---|---|"]
        for venue in ("isca", "dac", "iccad"):
            lines.append(f"| {venue.upper()} | {row['venue_roles'][venue]} |")
        lines += ["", "Interpretation: " + row["interpretation"], "", "Next matched comparison: " + row["next_comparison"], ""]
    lines += ["## Reading boundary", "", "The counts are selected evidence references, not venue prevalence. Evidence tiers are asymmetric, independent reviews are pending, and missing historical descriptions are not negative evidence.", ""]
    (root / "reports/cross-conference-direction-atlas-v1.md").write_text("\n".join(lines), encoding="utf-8")
    return result


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    args = parser.parse_args()
    result = build(args.root)
    print(json.dumps({"status": "built", "directions": len(result["directions"]), "output": "data/cross-conference-direction-atlas-v1.json"}, indent=2))
