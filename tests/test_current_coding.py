import json
from pathlib import Path

from scripts.build_evidence_summary import read_jsonl

ROOT = Path(__file__).resolve().parents[1]


def test_current_drafts_preserve_identity_and_numeric_disagreement():
    rows = read_jsonl(ROOT / "data/current-description-coding-v1.jsonl")
    sources = {r["paper_id"]: r for r in read_jsonl(ROOT / "dac/data/paper-evidence-2026.jsonl")}
    branches = {r["theme_id"]: r["subthemes"] for r in json.loads((ROOT / "data/taxonomy-v1-evidence.json").read_text())["themes"]}
    assert len(rows) == len({r["paper_id"] for r in rows}) == 211
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
    dag = next(r for r in rows if r["paper_id"] == "dac-2026-research1524")
    assert "timing-analysis" in dag["metrics"][0]["condition"]
    assert "measured" in dag["metrics"][1]["metric"]
    pmu = next(r for r in rows if r["paper_id"] == "dac-2026-research1495")
    assert pmu["metrics"][0]["unit"] == "events"
    loha = next(r for r in rows if r["paper_id"] == "dac-2026-research1560")
    assert all(m["metric"] == "throughput improvement" for m in loha["metrics"])
    filco = next(r for r in rows if r["paper_id"] == "dac-2026-research1569")
    assert len(filco["metrics"]) == 1
    assert filco["metrics"][0]["qualifier"] == "jointly reported range"
    slice_moe = next(r for r in rows if r["paper_id"] == "dac-2026-research1582")
    assert "DeepSeek-V2-Lite" in slice_moe["metrics"][0]["condition"]
    assert "Qwen1.5-MoE-A2.7B" in slice_moe["metrics"][1]["condition"]
    assert all(r["metrics"] == [] for r in rows if r["paper_id"] in {"dac-2026-research1587", "dac-2026-research1596"})
    mantis = next(r for r in rows if r["paper_id"] == "dac-2026-research1605")
    assert mantis["metrics"][3]["unit"] == "percentage points"
    assert "MXINT3 x MXINT3" in mantis["metrics"][1]["condition"]
    bayes = next(r for r in rows if r["paper_id"] == "dac-2026-research1610")
    assert bayes["metrics"][1]["unit"] == "percent of baseline power"
    hddb = next(r for r in rows if r["paper_id"] == "dac-2026-research1619")
    assert "random corruption" in hddb["metrics"][0]["condition"]
    prefix = next(r for r in rows if r["paper_id"] == "dac-2026-research1632")
    assert prefix["metrics"][0]["metric"] == "TTFT reduction"
    glasses = next(r for r in rows if r["paper_id"] == "dac-2026-research1691")
    assert glasses["metrics"][1]["value"] == 64
    assert glasses["metrics"][2]["value"] == 11
    assert "1.92" in glasses["metrics"][2]["condition"]
    pmem = next(r for r in rows if r["paper_id"] == "dac-2026-research1664")
    assert "simulator" in pmem["hardware_or_process_assumptions"]
    quantum = next(r for r in rows if r["paper_id"] == "dac-2026-research1709")
    assert "0.001" in quantum["metrics"][0]["condition"]
    assert "0.0005" in quantum["metrics"][1]["condition"]
    masked = next(r for r in rows if r["paper_id"] == "dac-2026-research1732")
    assert masked["metrics"][4]["value"] == 1.32
    epic = next(r for r in rows if r["paper_id"] == "dac-2026-research1741")
    assert epic["metrics"][2]["unit"] == "datasets out of 10"
    l2l = next(r for r in rows if r["paper_id"] == "dac-2026-research1765")
    assert l2l["metrics"][0]["qualifier"] == "up to"
    assert l2l["metrics"][3]["qualifier"] == "average"
    fp = next(r for r in rows if r["paper_id"] == "dac-2026-research1837")
    assert fp["metrics"][3]["qualifier"] == "up to"
    assert "no exact 100x inferred" in fp["limits"][0]
    sparse = next(r for r in rows if r["paper_id"] == "dac-2026-research1839")
    assert "SpInfer" in sparse["metrics"][0]["condition"]
    assert "FlashLLM" in sparse["metrics"][1]["condition"]
    peace = next(r for r in rows if r["paper_id"] == "dac-2026-research1885")
    assert peace["metrics"][1]["unit"] == "GOPS/W"
    assert "efficiency" in peace["metrics"][1]["qualifier"]
    thermal = next(r for r in rows if r["paper_id"] == "dac-2026-research1907")
    assert thermal["metrics"][2]["qualifier"] == "over"
    assert "not a discrepancy" in thermal["limits"][0]
    lidar = next(r for r in rows if r["paper_id"] == "dac-2026-research1960")
    assert lidar["metrics"][0]["metric"] == "retraining speedup"
    ohqs = next(r for r in rows if r["paper_id"] == "dac-2026-research1963")
    assert "not circuit fidelity" in ohqs["limits"][0]
    cache = next(r for r in rows if r["paper_id"] == "dac-2026-research1976")
    assert "no derived 2x" in cache["metrics"][0]["condition"]
    dart = next(r for r in rows if r["paper_id"] == "dac-2026-research2011")
    assert "Verilator" in dart["metrics"][0]["condition"]
    assert "RTLflow" in dart["metrics"][1]["condition"]
    floorplan = next(r for r in rows if r["paper_id"] == "dac-2026-research2048")
    assert "prediction only" in floorplan["metrics"][2]["condition"]
    secure = next(r for r in rows if r["paper_id"] == "dac-2026-research208")
    assert secure["metrics"][3]["value"] == 50
    assert "need not be chance" in secure["limits"][0]
    spmv = next(r for r in rows if r["paper_id"] == "dac-2026-research2105")
    assert len(spmv["metrics"]) == 12
    assert spmv["metrics"][0]["qualifier"] == "average"
    assert spmv["metrics"][1]["qualifier"] == "up to"
    overmind = next(r for r in rows if r["paper_id"] == "dac-2026-research2125")
    assert overmind["metrics"][0]["unit"] == "TOPS/W"
    assert overmind["metrics"][1]["unit"] == "GOPS"
    miter = next(r for r in rows if r["paper_id"] == "dac-2026-research214")
    assert miter["metrics"][0]["metric"] == "unspecified quantity reduction"
    assert miter["metrics"][0]["value"] == 92.1
    assert "does not name" in miter["metrics"][0]["condition"]
    gtx = next(r for r in rows if r["paper_id"] == "dac-2026-research2177")
    assert gtx["metrics"][0]["metric"] == "parasitic inference speedup"
    assert gtx["metrics"][1]["metric"] == "simulation speedup"
    assert "must not be multiplied" in gtx["limits"][0]
    trojan = next(r for r in rows if r["paper_id"] == "dac-2026-research2179")
    assert "percentage points unspecified" in trojan["metrics"][0]["condition"]
    assert trojan["metrics"][1]["qualifier"] == "relative"
    expertflow = next(r for r in rows if r["paper_id"] == "dac-2026-research2199")
    assert "GPU memory only" in expertflow["metrics"][0]["condition"]
