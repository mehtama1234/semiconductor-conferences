import json
from pathlib import Path

from scripts.build_evidence_summary import read_jsonl

ROOT = Path(__file__).resolve().parents[1]


def test_current_drafts_preserve_identity_and_numeric_disagreement():
    rows = read_jsonl(ROOT / "data/current-description-coding-v1.jsonl")
    sources = {r["paper_id"]: r for r in read_jsonl(ROOT / "dac/data/paper-evidence-2026.jsonl")}
    branches = {r["theme_id"]: r["subthemes"] for r in json.loads((ROOT / "data/taxonomy-v1-evidence.json").read_text())["themes"]}
    assert len(rows) == len({r["paper_id"] for r in rows}) == 409
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
    safe = next(r for r in rows if r["paper_id"] == "dac-2026-research2216")
    assert safe["metrics"][2]["metric"] == "area-time product improvement factor"
    assert "not a throughput" in safe["limits"][0]
    mirage = next(r for r in rows if r["paper_id"] == "dac-2026-research2243")
    assert mirage["metrics"][0]["metric"] == "computation reduction factor"
    assert "not measured latency" in mirage["limits"][0]
    voltage = next(r for r in rows if r["paper_id"] == "dac-2026-research2254")
    assert voltage["metrics"][0]["metric"] == "sequence prediction accuracy"
    assert "not per-instruction" in voltage["limits"][0]
    tieranns = next(r for r in rows if r["paper_id"] == "dac-2026-research2268")
    assert tieranns["metrics"] == []
    assert "description names COGA" in tieranns["limits"][0]
    vera = next(r for r in rows if r["paper_id"] == "dac-2026-research2298")
    assert "not absolute task accuracy" in vera["metrics"][0]["condition"]
    assert "one-week" in vera["hardware_or_process_assumptions"]
    assert "simulated" in vera["metrics"][0]["condition"]
    noc = next(r for r in rows if r["paper_id"] == "dac-2026-research2290")
    assert len(noc["metrics"]) == 8
    assert "saved raw HTML" in noc["limits"][0]
    defect = next(r for r in rows if r["paper_id"] == "dac-2026-research2306")
    assert "not independently verified" in defect["metrics"][1]["qualifier"]
    sketch = next(r for r in rows if r["paper_id"] == "dac-2026-research2317")
    assert "naive sketch" in sketch["metrics"][1]["condition"]
    chipmodeler = next(r for r in rows if r["paper_id"] == "dac-2026-research2319")
    assert chipmodeler["metrics"][0]["metric"] == "unspecified performance improvement"
    shortcircuit = next(r for r in rows if r["paper_id"] == "dac-2026-research2329")
    assert "not explicitly versus ABC" in shortcircuit["metrics"][0]["condition"]
    pinn = next(r for r in rows if r["paper_id"] == "dac-2026-research2346")
    assert pinn["metrics"][0]["unit"] == "unspecified error units"
    assert pinn["metrics"][1]["value"] == 21600
    fno = next(r for r in rows if r["paper_id"] == "dac-2026-research2358")
    assert "4x4" in fno["metrics"][0]["condition"]
    assert "3x3" in fno["metrics"][1]["condition"]
    assert fno["metrics"][0]["value"] == 1245550
    metric = next(r for r in rows if r["paper_id"] == "dac-2026-research2347")
    assert "description names MECA-CIM" in metric["limits"][0]
    recon = next(r for r in rows if r["paper_id"] == "dac-2026-research2369")
    assert [m["value"] for m in recon["metrics"]] == [23.5, 18.3]
    assert "not raw execution overhead" in recon["limits"][0]
    ubfp = next(r for r in rows if r["paper_id"] == "dac-2026-research2378")
    assert "EEF is not defined" in ubfp["metrics"][0]["condition"]
    hestia = next(r for r in rows if r["paper_id"] == "dac-2026-research2395")
    assert hestia["metrics"][2]["metric"] == "unspecified scheduler advantage"
    ltminer = next(r for r in rows if r["paper_id"] == "dac-2026-research240")
    assert [m["value"] for m in ltminer["metrics"]] == [[1.1, 652.6], [1.8, 70.3], [3.9, 2050.9], [1.2, 17.3]]
    combnn = next(r for r in rows if r["paper_id"] == "dac-2026-research2425")
    assert "description names RES-BNN" in combnn["limits"][0]
    assert "not a 0.03% reduction" in combnn["metrics"][2]["condition"]
    stitch = next(r for r in rows if r["paper_id"] == "dac-2026-research2443")
    assert [m["value"] for m in stitch["metrics"]] == [19, 61, 56]
    assert "must not be added" in stitch["limits"][0]
    nash = next(r for r in rows if r["paper_id"] == "dac-2026-research2489")
    assert "not achieved traffic reduction" in nash["metrics"][0]["condition"]
    easy = next(r for r in rows if r["paper_id"] == "dac-2026-research2504")
    assert "CPU" in easy["metrics"][0]["condition"]
    assert "GPU" in easy["metrics"][1]["condition"]
    lifu = next(r for r in rows if r["paper_id"] == "dac-2026-research2533")
    assert [m["value"] for m in lifu["metrics"][:6]] == [93.4, 43.6, 95.7, 90.1, 75.0, 78.3]
    assert lifu["metrics"][3]["condition"] == "Rocket"
    detox = next(r for r in rows if r["paper_id"] == "dac-2026-research2536")
    assert all(m["metric"] == "area overhead reduction" for m in detox["metrics"])
    atom = next(r for r in rows if r["paper_id"] == "dac-2026-research2540")
    assert atom["metrics"][0]["value"] == 115
    assert atom["metrics"][0]["unit"] == "microseconds"
    assert "not full imaging/control cycle" in atom["limits"][0]
    reuse = next(r for r in rows if r["paper_id"] == "dac-2026-research2566")
    assert reuse["metrics"][0]["qualifier"] == "average"
    assert "GPU" in reuse["metrics"][1]["condition"]
    arc = next(r for r in rows if r["paper_id"] == "dac-2026-research2631")
    assert "Cell-array level" in arc["metrics"][0]["condition"]
    assert "not evidence of fabricated" in arc["limits"][0]
    deinfer = next(r for r in rows if r["paper_id"] == "dac-2026-research2620")
    assert deinfer["metrics"] == []
    assert "detailed mechanism is insufficient" in deinfer["limits"][0]
    topcell = next(r for r in rows if r["paper_id"] == "dac-2026-research2646")
    assert "7 nm" in topcell["metrics"][0]["condition"]
    pdnet = next(r for r in rows if r["paper_id"] == "dac-2026-research2648")
    assert [m["value"] for m in pdnet["metrics"]] == [29, 10, 4, 19]
    assert "not exhaustive binary outcomes" in pdnet["limits"][0]
    bibnn = next(r for r in rows if r["paper_id"] == "dac-2026-research2698")
    assert bibnn["metrics"][0]["value"] == 11.4
    assert bibnn["metrics"][0]["metric"] == "computing cost retained"
    causal = next(r for r in rows if r["paper_id"] == "dac-2026-research271")
    assert causal["metrics"][0]["metric"] == "hypervolume improvement"
    assert "not 4.12x processor performance" in causal["limits"][0]
    detector = next(r for r in rows if r["paper_id"] == "dac-2026-research2717")
    assert detector["metrics"][4]["metric"] == "end-to-end speedup"
    assert detector["metrics"][4]["value"] == [2.1, 2.5]
    vla = next(r for r in rows if r["paper_id"] == "dac-2026-research2721")
    assert vla["metrics"][0]["metric"] == "success length improvement"
    pangaea = next(r for r in rows if r["paper_id"] == "dac-2026-research2762")
    assert "not achieved reduction" in pangaea["metrics"][0]["condition"]
    assert "bp/microjoule" in pangaea["metrics"][2]["condition"]
    lin = next(r for r in rows if r["paper_id"] == "dac-2026-research2756")
    assert lin["metrics"][3]["metric"] == "CNOT count reduction"
    assert lin["metrics"][3]["qualifier"] == "average"
    crystals = next(r for r in rows if r["paper_id"] == "dac-2026-research2780")
    assert "not correction coverage" in crystals["metrics"][1]["condition"]
    instructions = next(r for r in rows if r["paper_id"] == "dac-2026-research2804")
    assert instructions["metrics"][2]["value"] == 99.8357
    assert "not security-detection recall" in instructions["limits"][0]
    ehpc = next(r for r in rows if r["paper_id"] == "dac-2026-research2817")
    assert "Hardware simulation" in ehpc["metrics"][0]["condition"]
    assert "not identified as circuit silicon overhead" in ehpc["metrics"][2]["condition"]
    isapm = next(r for r in rows if r["paper_id"] == "dac-2026-research2824")
    assert isapm["metrics"][0]["metric"] == "area-time product improvement"
    hydra = next(r for r in rows if r["paper_id"] == "dac-2026-research285")
    assert "reference configuration unspecified" in hydra["metrics"][1]["condition"]
    synchoros = next(r for r in rows if r["paper_id"] == "dac-2026-research2851")
    assert "not automatically 2% worst-case" in synchoros["limits"][0]
    atlas = next(r for r in rows if r["paper_id"] == "dac-2026-research2886")
    assert [m["value"] for m in atlas["metrics"]] == [39, 33]
    assert "Among the 39" in atlas["metrics"][1]["condition"]
    assert "not fixes" in atlas["limits"][0]
    skist = next(r for r in rows if r["paper_id"] == "dac-2026-research293")
    assert [m["value"] for m in skist["metrics"]] == [50, 23.2, 40.3]
    assert "separate 50% maximum" in skist["limits"][0]
    react = next(r for r in rows if r["paper_id"] == "dac-2026-research2947")
    assert "Activation storage only" in react["metrics"][1]["condition"]
    iads = next(r for r in rows if r["paper_id"] == "dac-2026-research2975")
    assert "not the 256-unit prototype" in iads["metrics"][0]["condition"]
    green = next(r for r in rows if r["paper_id"] == "dac-2026-research2970")
    assert "1000-server scale is not established as a physical deployment" in green["limits"][0]
    sram = next(r for r in rows if r["paper_id"] == "dac-2026-research3019")
    assert "not established as 32 independent chips" in sram["limits"][0]
    comac = next(r for r in rows if r["paper_id"] == "dac-2026-research3029")
    assert "not whole-model inference latency" in comac["metrics"][0]["condition"]
    epar = next(r for r in rows if r["paper_id"] == "dac-2026-research3059")
    assert "not perfect prediction of absolute gate error" in epar["limits"][0]
    calibration = next(r for r in rows if r["paper_id"] == "dac-2026-research3087")
    assert "does not prove the neural calibrator is integrated on-chip" in calibration["limits"][0]
    router = next(r for r in rows if r["paper_id"] == "dac-2026-research3129")
    assert router["metrics"][1]["unit"] == "percentage points"
    placement = next(r for r in rows if r["paper_id"] == "dac-2026-research3100")
    assert len(placement["metrics"]) == 16
    assert placement["metrics"][10]["qualifier"] == "geometric mean below"
    gating = next(r for r in rows if r["paper_id"] == "dac-2026-research3154")
    assert gating["metrics"][0]["value"] == -1
    assert "sign ambiguous" in gating["metrics"][0]["qualifier"]
    topgq = next(r for r in rows if r["paper_id"] == "dac-2026-research3214")
    assert "not GNN inference" in topgq["metrics"][0]["condition"]
    specanns = next(r for r in rows if r["paper_id"] == "dac-2026-research343")
    assert "not a measured reduction" in specanns["metrics"][0]["condition"]
    lyra = next(r for r in rows if r["paper_id"] == "dac-2026-research358")
    assert "up to 107x to 3343x" in lyra["metrics"][1]["qualifier"]
    crystal = next(r for r in rows if r["paper_id"] == "dac-2026-research375")
    assert crystal["metrics"] == []
    ddf = next(r for r in rows if r["paper_id"] == "dac-2026-research378")
    assert "proof assumptions were not inspected" in ddf["limits"][0]
    page = next(r for r in rows if r["paper_id"] == "dac-2026-research401")
    assert "not fabricated PAGE modifications" in page["limits"][0]
    chiser = next(r for r in rows if r["paper_id"] == "dac-2026-research399")
    assert "manufacturing-weighted" in chiser["metrics"][0]["metric"]
    ams = next(r for r in rows if r["paper_id"] == "dac-2026-research407")
    assert ams["metrics"][1]["value"] == 4.1
    assert "exceeds" in ams["limits"][0]
    gwrite = next(r for r in rows if r["paper_id"] == "dac-2026-research444")
    assert "not a native hardware implementation" in gwrite["hardware_or_process_assumptions"]
    phantom = next(r for r in rows if r["paper_id"] == "dac-2026-research514")
    assert "not assigned to speed or validity" in phantom["metrics"][0]["condition"]
    scimi = next(r for r in rows if r["paper_id"] == "dac-2026-research462")
    assert "relative versus percentage points unspecified" in scimi["metrics"][1]["qualifier"]
    epicell = next(r for r in rows if r["paper_id"] == "dac-2026-research550")
    assert epicell["metrics"][5]["qualifier"] == "median"
    assert "not silicon validation" in epicell["limits"][0]
    onyx = next(r for r in rows if r["paper_id"] == "dac-2026-research529")
    assert onyx["metrics"] == []
