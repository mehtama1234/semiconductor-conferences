import json
from pathlib import Path

from scripts.build_evidence_summary import read_jsonl

ROOT = Path(__file__).resolve().parents[1]


def test_current_drafts_preserve_identity_and_numeric_disagreement():
    rows = read_jsonl(ROOT / "data/current-description-coding-v1.jsonl")
    sources = {r["paper_id"]: r for r in read_jsonl(ROOT / "dac/data/paper-evidence-2026.jsonl")}
    branches = {r["theme_id"]: r["subthemes"] for r in json.loads((ROOT / "data/taxonomy-v1-evidence.json").read_text())["themes"]}
    assert len(rows) == len({r["paper_id"] for r in rows}) == 85
    for row in rows:
        for key in ["title", "evidence_url", "analysis_edition", "evidence_collection_date"]:
            assert row[key] == sources[row["paper_id"]][key]
        assert row["subtheme_id"] in branches[row["theme_id"]]
        assert row["independent_review_status"] == "pending"
        assert row["subsubtheme_id"] is None
        assert row["limits"]
    atb = next(r for r in rows if r["paper_id"] == "dac-2026-research1000")
    assert atb["metrics"][0]["value"] == 4.54
    assert atb["metrics"][1]["value"] == [4.8, 24.6]
    assert "inconsistency" in atb["metrics"][0]["qualifier"]
    assert all(r["metrics"] == [] for r in rows if r["paper_id"] in {"dac-2026-research1011", "dac-2026-research1095", "dac-2026-research1138", "dac-2026-research1180"})
    noise = next(r for r in rows if r["paper_id"] == "dac-2026-research1152")
    assert "three-class" in noise["metrics"][1]["condition"]
    niaq = next(r for r in rows if r["paper_id"] == "dac-2026-research1200")
    assert "post-synthesis" in niaq["hardware_or_process_assumptions"]
    exquant = next(r for r in rows if r["paper_id"] == "dac-2026-research121")
    assert "percentage points unspecified" in exquant["metrics"][0]["condition"]
    faults = next(r for r in rows if r["paper_id"] == "dac-2026-research1417")
    assert faults["metrics"][0]["qualifier"] == "as low as"
    assert faults["metrics"][1]["value"] == 0.2
    assert "RTL" in faults["metrics"][2]["condition"]
    assert "software" in faults["metrics"][3]["condition"]
    duet = next(r for r in rows if r["paper_id"] == "dac-2026-research1419")
    assert "not fixed uniform precision" in duet["metrics"][0]["condition"]
    pihg = next(r for r in rows if r["paper_id"] == "dac-2026-research1438")
    assert "software" in pihg["metrics"][0]["condition"]
    assert "hardware" in pihg["metrics"][1]["condition"]
    taco = next(r for r in rows if r["paper_id"] == "dac-2026-research1440")
    assert taco["metrics"] == []
    freebit = next(r for r in rows if r["paper_id"] == "dac-2026-research146")
    assert freebit["metrics"] == []
    assert "not a measured FreeBit speedup" in freebit["limits"][0]
    stcg = next(r for r in rows if r["paper_id"] == "dac-2026-research1447")
    assert stcg["metrics"][0]["qualifier"] == "geometric mean"
    assert stcg["metrics"][1]["qualifier"] == "reported"
    avatee = next(r for r in rows if r["paper_id"] == "dac-2026-research1494")
    assert "baseline vulnerability" in avatee["metrics"][1]["qualifier"]
    assert "not an AvaTEE speedup" in avatee["metrics"][1]["condition"]
    ir_power = next(r for r in rows if r["paper_id"] == "dac-2026-research1474")
    assert ir_power["metrics"] == []
