"""Build a source-grounded supplementary condition extraction batch.

The extracted values are intentionally separate from adjudicated records: they
upgrade discoverability of explicit source text without upgrading evidence tier,
independent review, or full-paper completeness.
"""
from __future__ import annotations

import json
from pathlib import Path


EXTRACTIONS = {
    "dac-2026-research043": {
        "fields": {
            "hardware_or_process_assumptions": "Open-source SoC with an NPU; exact SoC, process, and evaluated device configuration are unspecified in the description.",
            "workload_or_design_corpus": "DNNs and LLMs; exact model suite and fault corpus are unspecified.",
        },
        "locators": ["open-source SoC", "DNNs and LLMs"],
    },
    "dac-2026-research046": {
        "fields": {
            "hardware_or_process_assumptions": "Power-grid EM and static IR-drop analysis; physical design/process configuration is unspecified in the description.",
            "workload_or_design_corpus": "Large-scale power-grid designs; exact design suite is unspecified.",
        },
        "locators": ["large-scale designs", "static IR drop"],
    },
    "dac-2026-research1028": {
        "fields": {
            "hardware_or_process_assumptions": "Byte-addressable CXL interconnect with DRAM–flash hybrid CXL devices; GEM5-based evaluation; exact device model is unspecified.",
        },
        "locators": ["byte-addressable CXL interconnect", "DRAM-Flash hybrid CXL systems", "GEM5-based evaluation"],
    },
    "dac-2026-research1054": {
        "fields": {
            "hardware_or_process_assumptions": "GPU-centric MoE offloading across models and devices; exact GPU devices and deployment configuration are unspecified.",
            "workload_or_design_corpus": "MoE decoding with adversarial prefix embeddings; exact model suite is unspecified.",
        },
        "locators": ["GPU-centric MoE offloading", "Across models/devices"],
    },
    "dac-2026-research1065": {
        "fields": {
            "hardware_or_process_assumptions": "3D integrated-circuit steady-state thermal simulation with complex boundary conditions and fine-grained power maps; process/material geometry is unspecified.",
        },
        "locators": ["3D integrated circuits (ICs)", "complex boundary conditions", "fine-grained power maps"],
    },
    "dac-2026-research108": {
        "fields": {
            "hardware_or_process_assumptions": "Real CXL hardware implementing a near-memory processing architecture; exact CXL device, host, and interconnect configuration are unspecified.",
            "workload_or_design_corpus": "Large-scale vector datasets for approximate nearest-neighbor search.",
        },
        "locators": ["real CXL hardware", "large-scale vector datasets"],
    },
    "dac-2026-research1101": {
        "fields": {
            "hardware_or_process_assumptions": "Fully digital CIM template in 28 nm CMOS with silicon-verified macros; exact foundry/process options and measurement conditions are unspecified.",
            "workload_or_design_corpus": "More than 8,000 silicon-consistent design points and 297 million configurations for hierarchical CIM exploration.",
        },
        "locators": ["28 nm", "silicon-verified", "297M configurations"],
    },
    "dac-2026-research1110": {
        "fields": {
            "hardware_or_process_assumptions": "Synthesizable hardware implementations produced by an HLS flow; target device, clock, resource, and synthesis configuration are unspecified.",
            "workload_or_design_corpus": "AI-model implementations through HLS; exact model suite is unspecified.",
        },
        "locators": ["synthesizable hardware implementations", "High-Level Synthesis (HLS)"],
    },
    "dac-2026-research1113": {
        "fields": {
            "hardware_or_process_assumptions": "Near-memory processing with distributed vault/channel organization; memory technology and device configuration are unspecified.",
            "workload_or_design_corpus": "LLM operators; exact model suite and sequence conditions are unspecified.",
        },
        "locators": ["distributed vault/channel organization", "large language models (LLMs)"],
    },
}


def build(root: Path) -> dict:
    source_path = root / "dac/data/paper-evidence-2026.jsonl"
    source_rows = {}
    for line in source_path.read_text(encoding="utf-8").splitlines():
        row = json.loads(line)
        source_rows[row["paper_id"]] = row

    rows = []
    for paper_id, extraction in EXTRACTIONS.items():
        source = source_rows[paper_id]
        description = source.get("description", "")
        missing_locators = [locator for locator in extraction["locators"] if locator.lower() not in description.lower()]
        if missing_locators:
            raise ValueError(f"Locators not present for {paper_id}: {missing_locators}")
        rows.append(
            {
                "schema": "source-condition-extraction.v1",
                "paper_id": paper_id,
                "conference_id": source["conference_id"],
                "edition": source["analysis_edition"],
                "title": source["title"],
                "evidence_tier": "official_description",
                "evidence_url": source["evidence_url"],
                "source_record": "dac/data/paper-evidence-2026.jsonl",
                "source_locators": extraction["locators"],
                "extracted_fields": extraction["fields"],
                "independent_review_status": "pending",
                "full_paper_status": "not_captured_in_this_batch",
                "limits": "Supplementary extraction from an official conference description; exact configurations and full-paper conditions remain unknown where stated.",
            }
        )
    output = root / "data/direction-condition-extractions-v1.jsonl"
    output.write_text("\n".join(json.dumps(row, sort_keys=True) for row in rows) + "\n", encoding="utf-8")

    lines = [
        "# Source condition extraction batch v1",
        "",
        "This batch extracts explicit workload and hardware/process context from captured DAC 2026 official descriptions. It is supplementary evidence, not a full-paper upgrade or independent review.",
        "",
        "| Paper | Extracted fields | Source tier | Review |",
        "|---|---|---|---|",
    ]
    for row in rows:
        lines.append(f"| `{row['paper_id']}` — {row['title']} | {', '.join(row['extracted_fields'])} | `{row['evidence_tier']}` | `{row['independent_review_status']}` |")
    lines += ["", "## Interpretation boundary", "", "These records make explicit source text discoverable to the condition register. They do not establish exact device configurations, complete experimental conditions, independent reproduction, or acceptance of the associated direction.", ""]
    (root / "reports/source-condition-extraction-batch-v1.md").write_text("\n".join(lines), encoding="utf-8")
    return {"schema": "source-condition-extraction-batch.v1", "status": "supplementary_extraction_pending_review", "record_count": len(rows), "output": "data/direction-condition-extractions-v1.jsonl"}


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    args = parser.parse_args()
    print(json.dumps(build(args.root), indent=2))
