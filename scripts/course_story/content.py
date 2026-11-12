"""The conference story for the semiconductor research atlas (ISCA, DAC, ICCAD): every word, number and picture
that the landing page, the slides, the video and the restyled pages say. Numbers are read from data/*.json at
build time; nothing here is typed in by hand except plain-language wording.

Sources: the repository's own coded paper records (data/taxonomy-expanded-v1.json), the long-term direction atlas
(data/long-term-direction-atlas-v1.json) and the Markdown articles in reports/ and dac/reports/."""
from __future__ import annotations

import json, re, shutil, sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SITE = ROOT / "site"
D = ROOT / "data"
REPO, BRANCH = "semiconductor-conferences", "main"
SITE_URL = f"https://mehtama1234.github.io/{REPO}/"
NAME = "Semiconductor conference atlas"
MARK = "Si"
DECK = "semiconductor-atlas-slides"
VIDEO = "semiconductor-atlas-story"
MANIFEST = False
STORY_PAGES = ["index.html", "course-map.html"]
SKIP_RESTYLE = ["presentation/"]
PUBLISH_EXCLUDE = [r"^styles\.css$", r"^reader\.css$"]
LEGACY_DROP = ["nav.topbar"]
SHORT_TITLES: dict[str, str] = {}


def load(name):
    return json.loads((D / name).read_text(encoding="utf-8"))


TAX = load("taxonomy-expanded-v1.json")
ATLAS = load("long-term-direction-atlas-v1.json")
THEMES = sorted(TAX["themes"], key=lambda t: -t["record_count"])
N_REC, N_SUB, N_THEME, N_MECH = TAX["record_count"], TAX["observed_subtheme_count"], TAX["theme_count"], TAX["mechanism_count"]
CONF, TIER = Counter(), Counter()
SUB_THEME: dict[str, dict] = {}
SUB = {}
for t in TAX["themes"]:  # records are split across theme-subtheme assignments; a subtheme in two themes is merged here
    for s in t["subthemes"]:
        CONF.update(s["conference_counts"])
        TIER.update(s["source_tier_counts"])
        SUB_THEME.setdefault(s["subtheme_id"], t)
        m = SUB.setdefault(s["subtheme_id"], {"subtheme_id": s["subtheme_id"], "label": s["label"], "record_count": 0, "conference_counts": Counter(), "source_tier_counts": Counter()})
        m["record_count"] += s["record_count"]
        m["conference_counts"].update(s["conference_counts"])
        m["source_tier_counts"].update(s["source_tier_counts"])


def depth(tier):
    if "official_description" in tier:
        return "desc"
    if any(w in tier for w in ("primary", "preprint", "pdf", "company_author", "full_text")):
        return "full"
    return "abs"


DEPTH = Counter()
for k, v in TIER.items():
    DEPTH[depth(k)] += v
N_DESC, N_FULL, N_ABS = DEPTH["desc"], DEPTH["full"], DEPTH["abs"]
N_DAC, N_ICCAD, N_ISCA = CONF["dac"], CONF["iccad"], CONF["isca"]
DIRS = ATLAS["directions"]
N_DEEP = len(list((ROOT / "dac/reports").glob("*-primary-*.md")))
TOP3 = THEMES[:3]

DIR_ORDER = ["constraints-become-executable", "data-movement-as-contract", "closed-loop-design", "reliability-security-upstream", "physical-reality-in-the-loop", "evaluation-as-research"]
DIR_FILE = {d: f"directions/{i:02d}-{d.replace('closed-loop-design', 'closed-loop-design')}.html" for i, d in enumerate(DIR_ORDER, 1)}
DIR_SHORT = {
    "constraints-become-executable": "Requirements checked while designing",
    "data-movement-as-contract": "Moving data is the real cost",
    "closed-loop-design": "Measure, then decide the next design",
    "reliability-security-upstream": "Plan for faults and attacks early",
    "physical-reality-in-the-loop": "Heat, wires and power in the loop",
    "evaluation-as-research": "Better ways to measure results",
}
DIR_ICON = {"constraints-become-executable": "checklist", "data-movement-as-contract": "arrows-exchange", "closed-loop-design": "refresh",
            "reliability-security-upstream": "shield-check", "physical-reality-in-the-loop": "temperature", "evaluation-as-research": "ruler"}
DIR_BY = {d["direction_id"]: d for d in DIRS}

BANNER = "A plain-language guide to what ISCA, DAC and ICCAD papers say about chip and computer design · Built from the repository’s own paper records · Not made by the conferences"
BADGES = [f"{N_REC} papers", f"{N_THEME} themes", "Plain words first"]
QUESTION = "What do this year’s chip-design conferences say about where the field is going?"
OG_ALT = f"{NAME}: {N_REC} papers from ISCA, DAC and ICCAD, sorted into {N_THEME} themes and six directions to watch."
SOURCE_LINE = (f"Built from {N_REC} paper records coded from ISCA 2026, DAC 2026 and ICCAD 2025 (ICCAD 2026 papers were not yet public). "
               "Most records come from official program descriptions; see “How deep the reading went”. The papers belong to their authors.")
SHARE_CREDIT = "Say it is an independent reading of public ISCA, DAC and ICCAD programs and papers, not an official conference page, and that most records come from program descriptions."
VIDEO_DESC = "The semiconductor conference atlas as a narrated video of about four minutes, with captions."
NAV = [
    ("The big picture", "index.html", ["index.html"]),
    ("Themes", "themes.html", ["themes.html", "themes/"]),
    ("Subthemes", "subthemes.html", ["subthemes.html", "subthemes/", "explorer.html"]),
    ("Deep reads", "deep-reads.html", ["deep-reads.html", "deep-reads/"]),
    ("What to watch", "directions.html", ["directions.html", "directions/", "comparisons.html", "comparisons/"]),
    ("Slides", "presentation/index.html", ["presentation/"]),
    ("Video", "video/index.html", ["video/"]),
    ("Share", "share/index.html", ["share/"]),
]
START_HREF = "guide/reading-guide-v1.html"
ROOT_LABEL = "Conference atlas"
SECTIONS = [
    {"dir": "themes", "index": "themes.html", "label": "Themes"},
    {"dir": "subthemes", "index": "subthemes.html", "label": "Subthemes"},
    {"dir": "deep-reads", "index": "deep-reads.html", "label": "Deep reads"},
    {"dir": "directions", "index": "directions.html", "label": "What to watch"},
    {"dir": "comparisons", "index": "comparisons.html", "label": "Across the three conferences"},
    {"dir": "guide", "index": "guide.html", "label": "How to read the atlas"},
]

# ---------------------------------------------------------------- the Markdown articles that become pages
THEME_POINT = {
    "ai-assisted-eda": "a model may propose a design, but only a tool check makes it count",
    "analog-mixed-signal-and-emerging-devices": "when physics does the arithmetic, noise and drift set the accuracy",
    "architecture-and-accelerators": "more arithmetic units help only when data arrives in time",
    "chiplets-3d-and-packaging": "splitting a chip into pieces trades cost for heat and wiring between dies",
    "design-methodology-and-tooling": "how a design is written down decides which choices a tool can see",
    "memory-interconnect-and-storage": "moving data, not computing it, often sets the time and energy",
    "physical-design-and-manufacturing": "placement, wiring, timing and power all push on each other",
    "power-reliability-and-security": "protection has a cost, so the fault or attack must be named first",
    "systems-applications-and-workloads": "judge a system by the useful work users get, not average speed",
    "verification-and-validation": "a check proves only what its stated property and tests cover",
}
THEME_ICON = {
    "ai-assisted-eda": "sparkles", "analog-mixed-signal-and-emerging-devices": "wave-sine", "architecture-and-accelerators": "cpu",
    "chiplets-3d-and-packaging": "stack-2", "design-methodology-and-tooling": "settings", "memory-interconnect-and-storage": "server",
    "physical-design-and-manufacturing": "ruler", "power-reliability-and-security": "shield-check", "systems-applications-and-workloads": "activity",
    "verification-and-validation": "checklist",
}
THEME_BY = {t["theme_id"]: t for t in TAX["themes"]}


def theme_blurb(src, title, default):
    t = THEME_BY.get(src.stem)
    if not t:
        return default
    return f"{t['record_count']} papers in {t['subtheme_count']} subthemes. The point: {THEME_POINT[src.stem]}."


def sub_blurb(src, title, default):
    s = SUB.get(src.stem)
    if not s:
        return default
    c = ", ".join(f"{k.upper()} {v}" for k, v in sorted(s["conference_counts"].items(), key=lambda kv: -kv[1]))
    return f"{s['record_count']} papers ({c}). Part of {SUB_THEME[src.stem]['label'].lower()}."


def sub_index(items):
    by = {}
    for rel, title, blurb in items:
        sid = rel.split("/")[-1][:-5]
        th = SUB_THEME.get(sid)
        by.setdefault(th["theme_id"] if th else "other", []).append((rel, title, blurb, SUB.get(sid, {}).get("record_count", 0)))
    out = []
    for t in THEMES:
        rows = sorted(by.get(t["theme_id"], []), key=lambda r: -r[3])
        if not rows:
            continue
        cards = "".join(f'<article class="card"><h3><a href="{r}">{ttl}</a></h3><p>{b}</p></article>' for r, ttl, b, _ in rows)
        out.append(f'<h2>{t["label"]}: {len(rows)} subthemes, {t["record_count"]} papers</h2><p>The point of this theme: {THEME_POINT[t["theme_id"]]}. <a href="themes/{t["theme_id"]}.html">Read the theme first →</a></p><div class="grid">{cards}</div>')
    return "".join(out)


GUIDE_FILES = ["reports/reading-guide-v1.md", "reports/expanded-taxonomy-v1.md", "reports/field-directions-and-hypotheses-v1.md", "reports/research-atlas-index-v1.md",
               "reports/direction-review-gate-v1.md", "reports/longitudinal-protocol-v1.md", "reports/research-agenda-v1.md", "reports/evidence-summary-v1.md"]
MARKDOWN = [
    {"glob": "reports/themes/*.md", "out": "themes", "index": "themes.html", "skip": ["README.md"], "title": "Themes", "blurb": theme_blurb,
     "intro": f"Ten broad subjects. Each article explains the basic technical problem first, then links to its subthemes and their papers."},
    {"glob": "reports/observed-subthemes/*.md", "out": "subthemes", "index": "subthemes.html", "title": "Subthemes", "blurb": sub_blurb, "index_body": sub_index,
     "intro": f"{N_SUB} narrower problems, grouped by theme. Each page explains the problem step by step, then lists every paper in it with what its source shows and leaves open."},
    {"glob": "dac/reports/*-primary-*.md", "out": "deep-reads", "index": "deep-reads.html", "title": "Deep reads",
     "intro": f"{N_DEEP} papers whose full text, preprint or released files were read and checked against the short program description."},
    {"glob": "reports/directions/0*.md", "out": "directions", "index": "directions.html", "title": "What to watch",
     "intro": "Six directions that recur across the papers. Each is a hypothesis to test, with the evidence for it, the paper that pushes back, and what would disprove it."},
    {"glob": "reports/comparisons/*.md", "out": "comparisons", "index": "comparisons.html", "skip": ["README.md"], "title": "Across the three conferences",
     "intro": "How ISCA, DAC and ICCAD papers meet the same pressure at different layers, and the fair comparison still needed."},
    {"files": GUIDE_FILES, "out": "guide", "index": "guide.html", "title": "How to read the atlas",
     "intro": "Definitions, the full list of subthemes, the field-level hypotheses and the rules used to decide what counts as evidence."},
]


def prebuild(kit):
    """The old one-page atlas becomes explorer.html (kept, restyled); its search reads a copy of the taxonomy."""
    shutil.copyfile(Path(__file__).with_name("explorer-source.html"), SITE / "explorer.html")
    (SITE / "data").mkdir(exist_ok=True)
    shutil.copyfile(D / "taxonomy-expanded-v1.json", SITE / "data" / "taxonomy-expanded-v1.json")


# ---------------------------------------------------------------- course map
MAP_GROUPS = [
    ("Start here: the big picture and how to read it", "Read these first if you are new.",
     ["guide/reading-guide-v1.html", "explorer.html", "guide.html"]),
    ("Read the themes: ten broad subjects", "Each explains the basic technical problem before any paper.", ["themes.html"] + [f"themes/{t['theme_id']}.html" for t in THEMES]),
    ("Go deeper: subthemes and the papers in them", f"{N_SUB} narrower problems, each with every paper and what its source shows.", ["subthemes.html", "deep-reads.html", "guide/expanded-taxonomy-v1.html"]),
    ("See what to watch: six directions and how to test them", "Hypotheses, the papers behind them and what would disprove them.", ["directions.html"] + [DIR_FILE[d] for d in DIR_ORDER] + ["comparisons.html", "guide/field-directions-and-hypotheses-v1.html"]),
    ("How the evidence was gathered and checked", "For reviewers: the rules, the protocol for comparing years, and the work still open.",
     ["guide/research-atlas-index-v1.html", "guide/direction-review-gate-v1.html", "guide/longitudinal-protocol-v1.html", "guide/research-agenda-v1.html", "guide/evidence-summary-v1.html"]),
]
MAP_BLURBS = {
    "guide/reading-guide-v1.html": ("How to read a paper record", "The six questions every paper must answer, and plain definitions of the terms."),
    "explorer.html": ("Search every theme and subtheme", "Type a word to filter the whole taxonomy, then open a subtheme."),
    "guide.html": ("All the reading guides", "Definitions, the full taxonomy, and the evidence rules."),
    "themes.html": ("All ten themes", f"{N_THEME} subjects, largest first in the chart on the big picture."),
    "subthemes.html": ("All subthemes, by theme", f"{N_SUB} subthemes, each with its papers."),
    "deep-reads.html": ("Papers read in full", f"{N_DEEP} papers checked against their full text or released files."),
    "directions.html": ("Six directions to watch", "Each with its evidence, its counter-evidence and its test."),
    "comparisons.html": ("The same direction, three conferences", "How each conference meets the same pressure."),
}
for t in THEMES:
    MAP_BLURBS[f"themes/{t['theme_id']}.html"] = (t["label"], f"{t['record_count']} papers. {THEME_POINT[t['theme_id']][:1].upper() + THEME_POINT[t['theme_id']][1:]}.")
for d in DIR_ORDER:
    MAP_BLURBS[DIR_FILE[d]] = (DIR_SHORT[d], DIR_BY[d]["first_principle"])
MAP_ICONS = {**{f"themes/{k}.html": v for k, v in THEME_ICON.items()}, **{DIR_FILE[d]: DIR_ICON[d] for d in DIR_ORDER},
             "explorer.html": "search", "deep-reads.html": "microscope", "subthemes.html": "grid-dots", "directions.html": "route", "comparisons.html": "affiliate", "themes.html": "books"}
MAP_DESC = f"Every page of the semiconductor conference atlas, grouped by what you want to do: start, read themes, go deeper, see what to watch, check the evidence."
MAP_H1 = "Every page, grouped by what you want to do"
MAP_SUB = "Start with the big picture if you are new. Come back here to find a theme, a subtheme, a paper read in full or a direction to watch."
MAP_NEW = "the reading guide explains what each paper record says and how far to trust it."
SHARE_EXTRA = [("All themes", "themes.html"), ("All subthemes", "subthemes.html"), ("Papers read in full", "deep-reads.html"), ("Six directions to watch", "directions.html"), ("Search the taxonomy", "explorer.html")]

# ---------------------------------------------------------------- pictures
PATH = [["file-text", "Papers", f"{N_REC} records from ISCA, DAC and ICCAD"], ["books", "Themes", f"{N_THEME} broad subjects"],
        ["grid-dots", "Subthemes", f"{N_SUB} narrower problems, each with its papers"], ["microscope", "Deep reads", f"{N_DEEP} papers checked in full"],
        ["route", "What to watch", "6 directions and the tests that would settle them"]]
FLOWS = {
    "ai-assisted-eda": ("A model proposes a design; tools decide whether it counts.", [["file-text", "Requirement", "what the circuit must do"], ["sparkles", "Model proposes", "code, layout or settings"], ["checklist", "Tools check", "compile, simulate, prove"], ["refresh", "Feedback", "which check failed, where"]], "REPEAT UNTIL EVERY CHECK PASSES"),
    "analog-mixed-signal-and-emerging-devices": ("When a device does the arithmetic, its physics sets the accuracy.", [["math-function", "A number", "stored as a voltage or charge"], ["wave-sine", "Physics computes", "currents add up"], ["alert-triangle", "Noise and drift", "heat, variation, ageing"], ["ruler", "Read back", "converter sets range and resolution"]], ""),
    "architecture-and-accelerators": ("Extra arithmetic helps only when the data arrives in time.", [["activity", "Workload", "the computation to run"], ["server", "Data arrives", "from memory, in order"], ["cpu", "Compute units", "many in parallel"], ["chart-bar", "Result", "time and energy, end to end"]], ""),
    "chiplets-3d-and-packaging": ("Splitting a chip into dies trades cost for wiring and heat.", [["cpu", "One big design", "too large or costly as one die"], ["stack-2", "Split into dies", "side by side or stacked"], ["arrows-exchange", "Links between dies", "slower, costlier than on-chip"], ["temperature", "Heat and power", "checked across the stack"]], ""),
    "design-methodology-and-tooling": ("How a design is written down decides what a tool can change.", [["file-text", "Description", "code or a graph"], ["settings", "Tool transforms", "keeps meaning, changes form"], ["checklist", "Validity check", "is it still the same design?"], ["chart-bar", "Cost estimate", "only then compare speed or area"]], ""),
    "memory-interconnect-and-storage": ("Moving data often costs more time and energy than computing it.", [["server", "Data at rest", "in memory or storage"], ["arrows-exchange", "Move it", "limited bandwidth, distance"], ["cpu", "Or compute near it", "place work where data is"], ["clock", "Time and energy", "count copies and waiting"]], ""),
    "physical-design-and-manufacturing": ("Turning connections into geometry: every step pushes on the others.", [["affiliate", "Connections", "which parts must link"], ["grid-dots", "Placement", "where each part sits"], ["route", "Wiring", "find room for every link"], ["clock", "Timing and power", "checked before manufacture"]], ""),
    "power-reliability-and-security": ("Name the fault or attack first, then pay for the protection.", [["alert-triangle", "Fault or attack", "stated model of what can go wrong"], ["shield-check", "Protection", "detect, correct, avoid"], ["bolt", "Its cost", "time, energy, area"], ["circle-check", "Useful correct work", "measured with protection on"]], ""),
    "systems-applications-and-workloads": ("Judge a system by the useful work its users get done.", [["users", "Requests arrive", "with deadlines"], ["activity", "Workload", "what each request needs"], ["server", "System choice", "hardware and scheduling"], ["clock", "Useful result", "on time, not just on average"]], ""),
    "verification-and-validation": ("A check proves only what its property and tests cover.", [["file-text", "Requirement", "stated precisely"], ["checklist", "Property or test", "what will be checked"], ["search", "Check runs", "simulate or prove"], ["circle-check", "Evidence", "pass, fail, or not covered"]], ""),
    "constraints-become-executable": ("Requirements become checks that steer the next design, not just judge the last one.", [["file-text", "Requirement", "function, area, timing"], ["sparkles", "Candidate", "proposed design"], ["checklist", "Executable check", "rejects, repairs or ranks"], ["refresh", "Next candidate", "uses what failed"]], "REPEAT AT A STATED BUDGET"),
    "data-movement-as-contract": ("Where data sits decides how fast and how cheaply work gets done.", [["server", "Where data is", "near or far"], ["arrows-exchange", "How far it moves", "and what shares the path"], ["cpu", "Where work runs", "near memory or on the host"], ["chart-bar", "End-to-end result", "with copying costs counted"]], ""),
    "closed-loop-design": ("Measure, learn, decide the next design, and count the cost of every step.", [["ruler", "Measure", "simulate or test a candidate"], ["brain", "Learn", "a fast model of results"], ["target", "Decide", "which candidate to try next"], ["checklist", "Recheck", "the winner at full accuracy"]], "REPEAT; COUNT EVERY SIMULATION"),
    "reliability-security-upstream": ("Faults and attacks shape the design from the start, with their cost shown.", [["alert-triangle", "Threat or fault model", "declared up front"], ["shield-check", "Design for it", "ECC, isolation, recovery"], ["bolt", "Pay the cost", "speed and energy lost"], ["circle-check", "Report it", "useful work with protection on"]], ""),
    "physical-reality-in-the-loop": ("Heat, wires and power enter the early design choices, not only the final check.", [["temperature", "Physical limit", "heat, wire delay, power"], ["math-function", "Fast estimate", "used while choosing"], ["target", "Design choice", "made with the estimate"], ["ruler", "Accurate check", "confirms the final design"]], ""),
    "evaluation-as-research": ("How results are measured is becoming research in its own right.", [["users", "Task set", "which designs or inputs"], ["ruler", "Evaluator", "rule for success, version"], ["chart-bar", "Result", "with failures and spread"], ["search", "Independent check", "someone else repeats it"]], ""),
    "deep-read": ("How deep the reading went: most papers only reached the first step.", [["file-text", "Program description", f"{N_DESC} papers"], ["notes", "Abstract or report", f"{N_ABS} papers"], ["books", "Full paper or preprint", f"{N_FULL} papers"], ["search", "Independent repeat", "none yet"]], ""),
}


def course_data(kit):
    flows = {k: {"label": v[0], "steps": v[1], "loop": v[2]} for k, v in FLOWS.items()}
    charts = {}
    for t in TAX["themes"]:
        for me in t["subthemes"]:
            pass
    for t in TAX["themes"]:
        subs = sorted(t["subthemes"], key=lambda s: -s["record_count"])
        charts[f"theme-{t['theme_id']}"] = {"type": "hBars", "caption": f"Papers in each subtheme of {t['label'].lower()}.", "labelW": 260,
                                            "items": [{"label": s["label"][:34] + ("…" if len(s["label"]) > 34 else ""), "value": s["record_count"], "tone": "s0"} for s in subs]}
    return {
        "path": PATH, "pathLabel": "The atlas path: papers, themes, subthemes, deep reads, then what to watch.",
        "flows": flows,
        "charts": {
            "themes": {"type": "hBars", "caption": f"Papers in each theme ({N_REC} papers, each in one theme).", "labelW": 270,
                       "items": [{"label": t["label"], "value": t["record_count"], "tone": "s1" if i < 3 else "s0"} for i, t in enumerate(THEMES)]},
            "confs": {"type": "hBars", "caption": "Papers coded from each conference.", "labelW": 200,
                      "items": [{"label": "DAC 2026", "value": N_DAC, "tone": "s1"}, {"label": "ICCAD 2025", "value": N_ICCAD, "tone": "s0"}, {"label": "ISCA 2026", "value": N_ISCA, "tone": "s0"}]},
            "depth": {"type": "hBars", "caption": "What each paper record was coded from.", "labelW": 250,
                      "items": [{"label": "Program description only", "value": N_DESC, "tone": "s0"}, {"label": "Abstract, report or artifact", "value": N_ABS, "tone": "s0"}, {"label": "Full paper, preprint or author PDF", "value": N_FULL, "tone": "s1"}]},
            "dirs": {"type": "hBars", "caption": "Papers cited as evidence for each direction (a paper can back more than one).", "labelW": 290,
                     "items": [{"label": DIR_SHORT[d], "value": len(DIR_BY[d]["evidence"]), "tone": "s1"} for d in DIR_ORDER]},
            **charts,
        },
    }


# ---------------------------------------------------------------- the story, in one place
T1, T2, T3 = TOP3
SHORT_THEME = {t['theme_id']: t['label'].lower().replace(', and', ' and') for t in TAX['themes']}
SENTENCES = [
    ("1 · The direction", "Chip design is becoming a loop: propose, check, learn, try again.",
     f"Six directions recur across the {N_REC} papers. Most are about feeding checks, measurements and physical limits back into the next design choice.",
     "directions.html", "The six directions"),
    ("2 · The weight", "Accelerators, memory and reliability draw the most papers.",
     f"Largest of {N_THEME} themes: {SHORT_THEME[T1['theme_id']]} ({T1['record_count']}), {SHORT_THEME[T2['theme_id']]} ({T2['record_count']}), {SHORT_THEME[T3['theme_id']]} ({T3['record_count']}).",
     "themes.html", "All ten themes"),
    ("3 · The caution", "Most papers were read from short descriptions, so these are hypotheses.",
     f"{N_DESC} of {N_REC} records come from program descriptions; {N_FULL} from a full paper or preprint. DAC supplies {N_DAC} of the {N_REC}.",
     "deep-reads.html", "Papers read in full"),
]
DOORS = [
    ("books", "Themes", "What are the big subjects?", f'{N_THEME} themes, each explaining the technical problem before any paper. <a href="themes.html">Read the themes →</a>'),
    ("grid-dots", "Subthemes", "Which papers tackle my problem?", f'{N_SUB} narrower problems, each with every paper and what its source shows. <a href="subthemes.html">Find a subtheme →</a>'),
    ("search", "Search", "Can I just search?", 'Type a word to filter every theme, subtheme and method. <a href="explorer.html">Search the atlas →</a>'),
    ("microscope", "Deep reads", "Which papers were read in full?", f'{N_DEEP} papers checked against their full text or released files. <a href="deep-reads.html">See the deep reads →</a>'),
    ("route", "What to watch", "Where is the field going?", 'Six directions, each with its evidence, its counter-evidence and its test. <a href="directions.html">See the directions →</a>'),
    ("help-circle", "How to read it", "How far can I trust a record?", 'Six questions every paper must answer, and plain definitions. <a href="guide/reading-guide-v1.html">Read the guide →</a>'),
    ("presentation", "Slides", "Can I present this?", 'Slides with speaker notes, a presenter view, PDF and PowerPoint. <a href="presentation/index.html">See the slides →</a>'),
    ("player-play", "Video", "Can I just watch it?", 'The slides read aloud, with captions, in about four minutes. <a href="video/index.html">Watch the video →</a>'),
    ("share", "Share", "How do I send this to someone?", 'One link, QR codes and every download. <a href="share/index.html">Share it →</a>'),
]
DEMO = [
    ("0:00 · The question", "Open with the question.", "Open the big picture and read the question at the top.", f"<b>Say:</b> “{QUESTION}”"),
    ("0:30 · Three sentences", "Read the three sentences.", "Scroll to the three sentences and read each with the line under it.", "<b>Say:</b> “Design is becoming a loop; accelerators, memory and reliability lead; and most of this is still hypothesis.”"),
    ("1:30 · One theme", "Show one theme with its picture.", "Open Themes, then memory, interconnect and storage.", "<b>Say:</b> “Moving data often costs more than computing it.”"),
    ("2:30 · One direction", "Show one direction and its test.", "Open What to watch, then the closed-loop direction.", "<b>Say:</b> “Each direction names the result that would disprove it.”"),
    ("3:30 · The caution", "Close on how deep the reading went.", "Back on the big picture, show the chart of what each record was coded from.", f"<b>Say:</b> “Only {N_FULL} of {N_REC} papers were read in full so far.”"),
]


def landing(kit):
    """The big picture, laid out natively on the board kit."""
    from course_story import boards, visuals as V
    R, esc = boards.R, boards.esc
    me = sys.modules[__name__]
    cards = [{"label": "Papers", "value": str(N_REC), "note": "ISCA, DAC and ICCAD"},
             {"label": "Themes", "value": str(N_THEME), "note": f"{N_SUB} subthemes"},
             {"label": "From DAC", "value": f"{N_DAC} of {N_REC}", "note": "design tools lead"},
             {"label": "Read in full", "value": str(N_FULL), "note": f"{N_DESC} from short descriptions"}]
    h1 = f'{esc(QUESTION)} <i>Toward a loop: propose a design, check it with tools, learn, try again.</i>'
    lede = (f"Three conferences publish much of the new research on how chips and computers are designed, checked and built. "
            f"This atlas sorts {N_REC} of their papers by the problem each one tackles, and explains each problem in plain words.")
    extra = ('<div class="rs-btns" style="margin-top:22px"><a class="ck-btn pri" href="themes.html">Start with the themes</a>'
             '<a class="ck-btn" href="#three">The story in three sentences</a></div>')
    hero = boards.hero(me, "index.html", f"ISCA 2026 · DAC 2026 · ICCAD 2025 · {N_REC} papers", h1, lede, cards, extra, long=True)
    parts = [R.strip_html([{"label": "Who it is for", "value": "engineers, researchers, students, technical leaders"},
                           {"label": "You need", "value": "a rough idea of what a processor and memory are"},
                           {"label": "Each term", "value": "is explained where it first appears"}], "The big picture")]
    three = "".join(f'<article class="card"><p class="rs-k">{a}</p><h3>{h}</h3><p>{e}</p><p class="ck-links"><a href="{href}">{link} →</a></p></article>' for a, h, e, href, link in SENTENCES)
    parts.append('<section class="ck-sec" id="three">' + R.section_head("The whole story", "What is the whole story in three sentences?", "Each sentence stands on its own. The line under it gives the numbers behind it.") + f'<div class="ck-grid g3">{three}</div></section>')
    parts.append('<section class="ck-sec">' + R.section_head("The common thread", "Design is becoming a loop: measure, learn, decide, recheck",
                 "Many papers feed a check, a measurement or a physical limit back into the next design choice. The fair question is what each turn of the loop costs.")
                 + V.scene_panel(V.d_wheel("home-wheel"), "Four steps and a meter", "our drawing", "A fast predictor is only useful if the final design still passes the slow, accurate check. A fair claim counts every simulation, the recheck included.")["html"] + "</section>")
    parts.append('<section class="ck-sec">' + R.section_head("Why data movement matters", "More arithmetic units help only when the data arrives in time",
                 "An accelerator is a chip built to do one kind of work fast. Its compute units sit idle when memory cannot feed them.")
                 + V.scene_panel(V.s_accel("home-accel"), "An accelerator, from memory to result", "our drawing", "Numbers travel from big, far memory (DRAM) through small, near buffers (SRAM) into a grid of units. Pale units are waiting.")["html"]
                 + R.panel_html({"panel": "Try it: when memory, not arithmetic, sets the speed", "chip": "illustration", "chart": V.roofline_chart(),
                                 "caption": "Worked out from one formula: speed = the smaller of peak and bandwidth × operations per byte. Peak 100 and bandwidth 10 are made-up units, not a real chip."}) + "</section>")
    th = [(t["label"], t["record_count"]) for t in THEMES]
    parts.append('<section class="ck-sec">' + R.section_head("Where the papers go", f"Accelerators, memory and reliability draw the most papers",
                 f"Together the top three themes hold {T1['record_count'] + T2['record_count'] + T3['record_count']} of {N_REC} papers. A count shows where this sample's papers went. It is not market share or importance.")
                 + '<div class="ck-pagefig">' + R.panel_html({"panel": f"Papers in each of the {N_THEME} themes", "chip": "counted",
                    "chart": V.bars("Papers per theme", f"{T1['label']} leads with {T1['record_count']}.", th, em=th[0][0]),
                    "caption": f"Counted from data/taxonomy-expanded-v1.json. Each of the {N_REC} records sits in one theme."})
                 + R.panel_html({"panel": "Papers from each conference", "chip": "counted",
                    "chart": V.bars("Papers per conference", f"DAC 2026 gives {N_DAC} of {N_REC}.", [("DAC 2026", N_DAC), ("ICCAD 2025", N_ICCAD), ("ISCA 2026", N_ISCA)], em="DAC 2026"),
                    "caption": f"ICCAD 2026 papers were not public yet, so its {N_ICCAD} papers come from 2025. ISCA adds {N_ISCA} selected architecture papers."}) + "</div></section>")
    dirs = "".join(f'<a class="ck-row" href="{DIR_FILE[d]}"><span class="rs-n">{i}</span><b>{DIR_SHORT[d]}</b><span>{DIR_BY[d]["first_principle"]}</span></a>' for i, d in enumerate(DIR_ORDER, 1))
    parts.append('<section class="ck-sec">' + R.section_head("What to watch", "Six directions, each a hypothesis with a stated test",
                 "None is proven. Each page names the paper that pushes back and the result that would disprove it.") + f'<div class="ck-rows">{dirs}</div></section>')
    parts.append('<section class="ck-sec">' + R.section_head("How sure we are", f"Only {N_FULL} of {N_REC} papers were read from a full paper or preprint",
                 "A program description gives the problem and the claimed method, but rarely the test conditions. So every direction here is a question to test.")
                 + V.scene_panel(V.depth_ladder("home-depth", N_DESC, N_ABS, N_FULL, N_DEEP), "How deep the reading went", "counted", f"Counted from the source of each record: {N_DESC} program descriptions, {N_ABS} abstracts or reports, {N_FULL} full papers or preprints. {N_DEEP} papers have a deep-read page.")["html"] + "</section>")
    rows = "".join(f'<a class="ck-row" href="{h}"><span class="rs-n">{i + 1}</span><b>{q}</b><span>{re.sub("<[^>]+>", "", d).replace(" →", "")}</span></a>' for i, (_, k2, q, d) in enumerate(DOORS) for h in [re.search(r'href="([^"]+)"', d).group(1)])
    parts.append('<section class="ck-sec">' + R.section_head("Where next", "Which question do you have?") + f'<div class="ck-rows">{rows}</div></section>')
    parts.append('<section class="ck-sec"><div class="ck-grid g2"><article class="card"><h3>Built from the repository’s own paper records</h3><p>Every number here is counted from the coded records when the site is built. Each paper card keeps its source link, what the source shows and what it leaves open.</p></article>'
                 '<article class="card warn"><h3>Not an official conference page, and not a ranking</h3><p>A paper count is not market share, adoption or importance. The sample is selected, and most records come from short descriptions.</p></article></div></section>')
    close = boards.close_band(me, "index.html", "The big picture, in one line", "Chip design is turning into a loop of propose, check, learn and try again; most of the evidence is still short descriptions.", None, ("themes.html", "The ten themes"), [("themes.html", "Start with the themes"), ("presentation/index.html", "Slides"), ("video/index.html", "Video")])
    page = boards.shell(me, "index.html", f"{NAME} · what ISCA, DAC and ICCAD say about where chip design is going",
                        f"{QUESTION} {N_REC} papers from ISCA 2026, DAC 2026 and ICCAD 2025 sorted into {N_THEME} themes and {N_SUB} subthemes, with six directions to watch.", hero, "\n".join(parts), close)
    (kit.site / "index.html").write_text(page, encoding="utf-8")


# ---------------------------------------------------------------- the restyled pages
H1 = {
    "themes.html": ("Themes", "Ten themes, each explaining one technical problem before its papers", "Start with any theme; each ends with links to its subthemes and their papers."),
    "subthemes.html": ("Subthemes", f"{N_SUB} subthemes, grouped by theme, each with every paper in it", "The biggest subthemes come first inside each theme."),
    "deep-reads.html": ("Deep reads", f"{N_DEEP} papers read in full, and what the full text changed", "Each page compares the short program description with the full paper, preprint or released files."),
    "directions.html": ("What to watch", "Six directions to watch, each with the result that would disprove it", "Read the problem first, then the evidence, the counter-evidence and the next test."),
    "comparisons.html": ("Across the three conferences", "The same pressure, met at different layers by ISCA, DAC and ICCAD", "A shared pressure is not a shared result: each page names the fair comparison still needed."),
    "guide.html": ("How to read the atlas", "How to read the atlas: definitions, the full taxonomy and the evidence rules", ""),
    "explorer.html": ("Search the atlas", "Search every theme, subtheme and method in one place", "Type a word to filter. Open a subtheme to read its papers."),
}
RELABEL = {
    "Compare the results carefully": "How to compare these papers’ results fairly",
    "Understand the parent subject first": "The bigger theme this belongs to",
    "Complete captured evidence": "Every paper in this subtheme, with what its source shows",
    "What remains to establish": "What is still unproven here",
    "Additional source assessment": "What a closer read of the source added",
    "Venue roles": "What each conference contributes",
    "ICCAD": "What the ICCAD papers add",
    "DAC": "What the DAC papers add",
    "ISCA": "What the ISCA papers add",
    "Required matched fields": "What must match before results can be compared",
    "Paper-level comparison set": "The papers being compared",
    "Next matched comparison": "The next fair comparison to run",
    "Comparative proposition": "The claim being compared across conferences",
    "Current conclusion boundary": "What we can conclude today, and no further",
    "Counterpressure and falsification boundary": "The paper that pushes back, and what would disprove the direction",
    "Establishing a long-term trend": "What it would take to call this a long-term trend",
    "Paper evidence and open conditions": "The papers behind it, and the conditions still unknown",
    "What is actually comparable": "What can fairly be compared",
    "Why the details matter": "Why the details decide the answer",
    "Representative source-backed records": "Papers that show the theme well",
    "Paper cards: what changes and where it stops": "Paper cards: what each paper changes, and where it stops",
    "Evidence status": "How strong the evidence is so far",
    "Released-history countercheck": "What the released history shows when checked against the paper",
    "Claim ladder": "The ladder of claims, from weakest to strongest",
    "Current verdict": "What the protocol concludes today",
    "Theme topology": "How the themes and subthemes fit together",
    "Coverage": "How much of each conference the sample covers",
    "Theme distribution": "How the records spread across themes",
    "Field completeness": "Which record fields are filled in, and which are missing",
    "Limits": "What this evidence summary cannot show",
    "Gate summary": "Which directions passed the review gate, and which did not",
    "Paper-level audit": "What the paper-by-paper audit found",
    "Interpretation boundary": "How far these results can be read",
    "First-principles spine": "The first principles the whole atlas rests on",
    "Canonical directions": "The six directions the atlas tracks",
    "Operating loop": "How the research loop runs, step by step",
    "Evidence boundary": "Where the evidence stops",
    "Work packages": "The work packages still to do",
    "Acceptance rules": "The rules a result must pass to be accepted",
    "Operating boundary": "What this agenda covers, and what it does not",
    "Subthemes and how to study them": "The subthemes in this theme, and how to read them",
}


def relabel(soup, main):
    for h in main.find_all(["h2", "h3"]):
        old = h.get_text(" ", strip=True)
        if old in RELABEL:
            k = soup.new_tag("p")
            k["class"] = "lm-k h-label"
            k.string = old
            h.insert_before(k)
            h.string = RELABEL[old]


def clean_deep(t):
    t = re.sub(r"\s*[—-]\s*2026-\d\d-\d\d$", "", t)
    name = re.split(r"[ :]", t, 1)[0]
    return f"{name}: what reading the full source showed"


def page_hook(kit, rel, soup, main, info):
    if rel in H1:
        info["eyebrow"], info["h1"], info["sub"] = H1[rel]
    m = re.match(r"themes/([a-z0-9-]+)\.html$", rel)
    if m and m.group(1) in THEME_BY:
        t = THEME_BY[m.group(1)]
        info["eyebrow"] = f"Theme · {t['record_count']} papers · {t['subtheme_count']} subthemes"
        pt = THEME_POINT[t['theme_id']]
        info["h1"] = f"What do the {t['record_count']} papers on {t['label'][0].lower() + t['label'][1:] if t['label'][:2] != 'AI' else t['label']} work on?"
        info["sub"] = f"{pt[0].upper() + pt[1:]}. The article explains the problem step by step first. Then it links every subtheme and its papers. Worked numbers are illustrations, not paper results."
    m = re.match(r"subthemes/([a-z0-9-]+)\.html$", rel)
    if m and m.group(1) in SUB:
        s, t = SUB[m.group(1)], SUB_THEME[m.group(1)]
        c = ", ".join(f"{k.upper()} {v}" for k, v in sorted(s["conference_counts"].items(), key=lambda kv: -kv[1]))
        dd = Counter()
        for k2, v in s["source_tier_counts"].items():
            dd[depth(k2)] += v
        info["eyebrow"] = f"Subtheme · {s['record_count']} papers · {t['label']}"
        from course_story import visuals as V
        at, a, b = V.SUBNOTE[m.group(1)]
        info["h1"] = f"What do the {s['record_count']} papers on {s['label'][0].lower() + s['label'][1:]} change?"
        pl = lambda n, one, many: f"{n} {one if n == 1 else many}"
        src = ", ".join(x for x in (pl(dd['desc'], "program description", "program descriptions") if dd['desc'] else "", pl(dd['abs'], "abstract or report", "abstracts or reports") if dd['abs'] else "",
                                    pl(dd['full'], "full paper or preprint", "full papers or preprints") if dd['full'] else "") if x)
        info["sub"] = f"{a} {b} Papers: {c}. Read from: {src}. The explanations come first; every paper’s record follows at the end."
    if rel.startswith("deep-reads/"):
        info["eyebrow"] = "Deep read · a paper checked against its full source"
        from course_story import visuals as V
        key = rel.split("/")[-1].split("-primary")[0]
        name = re.split(r"[ :]", re.sub(r"\s*[—-]\s*2026-\d\d-\d\d$", "", info["h1"]), maxsplit=1)[0]
        info["h1"] = f"What did a closer read of {name} show?"
        if key in V.DEEP:
            a, b = V.DEEP[key][2]
            info["sub"] = f"{b} The paper: {a[0].lower() + a[1:]}"
    m = re.match(r"directions/0\d-([a-z-]+)\.html$", rel)
    if m and m.group(1) in DIR_BY:
        d = m.group(1)
        i = DIR_ORDER.index(d) + 1
        info["eyebrow"] = f"Direction {i} of 6 · a hypothesis, not a measured trend"
        info["sub"] = DIR_BY[d]["first_principle"]
    m = re.match(r"comparisons/([a-z-]+)\.html$", rel)
    if m and m.group(1) in DIR_BY:
        d = m.group(1)
        info["eyebrow"] = "Across the three conferences"
        info["h1"] = f"How do ISCA, DAC and ICCAD each meet “{DIR_SHORT[d].lower()}”?"
        info["sub"] = "Each conference meets it at a different layer of the stack. A shared pressure is not a shared result, so each page names the fair comparison still needed."
    if rel.startswith("guide/"):
        info["eyebrow"] = "How to read the atlas"
    relabel(soup, main)


# ---------------------------------------------------------------- slides and the narration
def _old_slides(kit):
    k = kit
    out = []

    def slide(key, alt, body, notes, cls=""):
        out.append({"key": key, "alt": alt, "body": body, "notes": notes, "cls": cls})

    def head(eyebrow, title, sub="", art=""):
        a = f'<div class="hj-art" data-art="{art}"></div>' if art else ""
        s = f'<p class="hj-sub">{sub}</p>' if sub else ""
        return f'<div class="lm-head"><div class="hj-heading"><p class="eyebrow">{eyebrow}</p><h1>{title}</h1>{s}</div>{a}</div>'

    def cards(items, cls=""):
        return f'<section class="landing-problems {cls}"><ol>' + "".join(f'<li><p class="lp-k">{a}</p><h3>{h}</h3><p class="lp-pain">{b}</p></li>' for a, h, b in items) + "</ol></section>"

    def flow(slug, sub=""):
        return f'<figure class="course-fig"><div class="loop-wide" data-art="flow:{slug}"></div><figcaption>{sub or FLOWS[slug][0]}</figcaption></figure>'

    art = k.landing_art([("1 · THE PAPERS", f"{N_REC} papers", "ISCA, DAC, ICCAD", "sorted by problem"), ("2 · THE THEMES", f"{N_THEME} subjects", f"{N_SUB} subthemes", "each explained"),
                         ("3 · THE LOOP", "Propose, check", "learn, try again", "with costs counted"), ("4 · THE TEST", "What to watch", "6 directions, each", "with its disproof")])
    slide("cover", QUESTION, f"""<div class="landing-hero"><div class="landing-hero-text"><p class="landing-kicker">ISCA 2026 · DAC 2026 · ICCAD 2025 · {N_REC} papers</p>
<h1>{QUESTION}</h1><p class="landing-try-note">A plain-language atlas of the research, with what each paper shows and leaves open.</p></div>{art}</div>""",
          f"This is an atlas of {N_REC} papers from three chip-design conferences: ISCA, DAC and ICCAD. It asks one question. What do these papers, taken together, say about where chip and computer design is going?")
    slide("three", "The whole story in three sentences.", f"{head('The whole story', 'In three sentences.')}{cards([(a, h, e) for a, h, e, _, _ in SENTENCES], 'found3')}",
          f"Here is the whole story in three sentences. One: chip design is becoming a loop. Propose, check, learn, try again. Two: accelerators, memory and reliability draw the most papers. Three: most papers were read from short descriptions, so these are hypotheses, not proven trends.")
    slide("path", "The atlas in five steps: papers, themes, subthemes, deep reads, what to watch.", f"""{head('How the atlas is built', 'From papers to directions, in five steps.', f'{N_REC} papers, sorted into {N_THEME} themes and {N_SUB} subthemes, a few read in full, then six directions to watch.')}
<div class="method-figure"><div class="loop-wide" data-art="path"></div></div>""",
          f"The atlas works in five steps. Start with {N_REC} paper records. Sort them into {N_THEME} broad themes, then {N_SUB} narrower subthemes, each explained in plain words. Read some papers in full. Then ask which directions keep coming back, and what test would confirm them.")
    slide("confs", f"DAC supplies {N_DAC} of the {N_REC} papers.", f"{head('Where the papers come from', f'DAC is {N_DAC} of {N_REC} papers.')}{k.chart('confs', 'Papers per conference', 'The sample leans toward design automation.', f'ISCA adds {N_ISCA}; ICCAD adds {N_ICCAD}, from its 2025 edition.', 'ICCAD 2026 papers were not yet public.')}",
          f"First, where the papers come from. DAC, the Design Automation Conference, supplies {N_DAC} of the {N_REC}. ISCA, the main computer architecture conference, adds {N_ISCA} selected papers. ICCAD's 2026 papers were not public yet, so {N_ICCAD} come from 2025. So the atlas leans toward design software.")
    slide("themes", f"Accelerators, memory and reliability are the three largest of {N_THEME} themes.", f"{head('Where the attention goes', 'Accelerators, memory and reliability lead.')}{k.chart('themes', 'Papers per theme', f'{T1["label"]}: {T1["record_count"]} papers.', 'A count shows attention in this sample, not importance.', 'Each paper sits in one theme.')}",
          f"Here is where the attention goes. {T1['label']} is the largest theme, with {T1['record_count']} papers. {T2['label']} has {T2['record_count']}. {T3['label']} has {T3['record_count']}. A count shows where this sample spends its attention. It is not a ranking of importance.")
    slide("loop", "Direction: design becomes a loop that checks every candidate and learns from what failed.", f"{head('The common thread', 'Design becomes a loop.')}{flow('constraints-become-executable', 'Checks steer the next attempt, not just judge the last one.')}",
          "The common thread is a loop. A model or a search proposes a design. Tools check it: does it compile, does it simulate correctly, does it meet timing? The check reports what failed, and the next attempt uses that. The hard question is cost: a fair test counts every model call, retry and check.")
    slide("data", "Direction: moving data often costs more than computing it.", f"{head('Data movement', 'Moving data is often the real cost.', 'More arithmetic units help only when the data arrives in time.')}{flow('data-movement-as-contract')}",
          f"The second direction is about data. A chip can have thousands of arithmetic units, but they wait if their inputs cannot arrive in time. So many papers decide where data sits, how far it moves, and whether to compute next to memory. The test is the end-to-end result, with every copy and wait counted.")
    slide("physical", "Directions: physical limits and faults enter the design early.", f"""{head('Physics and protection', 'Heat, wires, faults and attacks move earlier.')}
{k.grid([('temperature', 'Physical reality', 'Heat, wire delay, power', 'Fast physical estimates guide early choices; an accurate check must still confirm the final design.'), ('shield-check', 'Faults and attacks', 'Named before protection', 'Protection costs speed and energy. Report useful correct work with the protection switched on.')])}""",
          "Two more directions move physics and safety earlier. Heat, wire delay and power supply used to be checked at the end. Now fast estimates guide early choices, but the final design still needs an accurate check. Likewise, faults and attacks are named first, and the cost of protection is reported, not hidden.")
    slide("measure", "Direction: how results are measured is becoming research in its own right.", f"{head('Measurement', 'Better ways to measure results.', 'A score depends on the task set, the rule for success and the comparison.')}{flow('evaluation-as-research')}",
          "The last direction is about measurement itself. A score means little without the tasks it was tested on, the rule for success, and the baseline. More papers now build benchmarks and release their tools. The test for this direction is simple: can someone else repeat the result and get the same answer?")
    slide("depth", f"Only {N_FULL} of {N_REC} papers were read from a full paper or preprint.", f"{head('How sure we are', f'{N_DESC} of {N_REC} records come from short descriptions.')}{k.chart('depth', 'What each record was coded from', 'Most records rest on the official program description.', f'{N_DEEP} papers were checked in depth against their full source.', 'So the directions are hypotheses, not measured trends.')}",
          f"Now, how sure can we be? {N_DESC} of the {N_REC} records were coded from the short official program description. Only {N_FULL} come from a full paper, preprint or author PDF. {N_DEEP} papers were checked in depth. So every direction here is a hypothesis to test, not a proven trend.")
    six = [(DIR_ICON[d], f"Direction {i}", DIR_SHORT[d], DIR_BY[d]["first_principle"]) for i, d in enumerate(DIR_ORDER, 1)]
    slide("watch", "Six directions to watch, each with a test that could disprove it.", f"""{head('What to watch', 'Six directions, each with its disproof.')}
<div class="grid3">{k.grid([(a, b, c, '') for a, b, c, _ in six])}</div>""",
          "Here are the six directions to watch. Requirements checked while designing. Data movement as the real cost. Measure, then decide the next design. Faults and attacks planned early. Physical limits in the loop. And better ways to measure. Each page names the paper that pushes back, and the result that would disprove it.", "dense")
    slide("start", "Where to start: themes, subthemes, deep reads and the six directions.", f"""{head('Your turn', 'Start with a theme, then follow its papers.', 'Every page explains the problem before the papers, and says how deep its sources go.')}
<div class="method-figure"><div class="loop-wide" data-art="path"></div></div>""",
          f"To explore it yourself, start with a theme. Each one explains the technical problem in plain words, then links to its subthemes and every paper in them. Check the deep reads for papers read in full. Then open the six directions. Everything is linked from the big picture page.")
    return out


def slides(kit):
    """The deck in the boards' slide frame (kit/components.slide). Narration (notes) is unchanged from the house deck."""
    sys.path.insert(0, str(ROOT / "kit"))
    import components as K
    import render_lecture
    from course_story import visuals as V
    R_glyph = render_lecture.glyph
    old = {s["key"]: s for s in _old_slides(kit)}
    keys = ["cover", "three", "path", "confs", "themes", "loop", "data", "physical", "measure", "depth", "watch", "start"]
    n, src = len(keys), "Counted from the repository’s paper records"
    fit = lambda svg, h=560: svg.replace('class="ck-art"', f'class="ck-art" style="width:100%;height:{h}px;display:block"', 1)
    B = NAME
    body = {
        "cover": K.slide("title", B, 1, n, f"ISCA 2026 · DAC 2026 · ICCAD 2025 · {N_REC} papers", (QUESTION, ""),
                         lead="Toward a loop: propose a design, check it with tools, learn, try again.", src="An independent reading of public programs and papers",
                         cards=[{"label": "Papers", "value": str(N_REC), "note": "ISCA, DAC and ICCAD"}, {"label": "Themes", "value": str(N_THEME), "note": f"{N_SUB} subthemes"},
                                {"label": "From DAC", "value": f"{N_DAC} of {N_REC}", "note": "design tools lead"}, {"label": "Read in full", "value": str(N_FULL), "note": f"{N_DESC} from short descriptions"}]),
        "three": K.slide("number", B, 2, n, "The whole story", ("In three sentences.", "Each stands alone."), value=str(N_REC), label="papers behind three sentences",
                         text="Design becomes a loop; accelerators, memory and reliability lead; most evidence is still short descriptions.",
                         cards=[{"label": a, "value": v, "note": h} for (a, h, e, _, _), v in zip(SENTENCES, ["A loop", "Three lead", "Hypotheses"])], src=src),
        "path": K.slide("diagram", B, 3, n, "How the atlas is built", ("From papers to directions,", "and how deep each was read."), svg=fit(V.depth_ladder("sl-depth0", N_DESC, N_ABS, N_FULL, N_DEEP), 600), src=src),
        "confs": K.slide("number", B, 4, n, "Where the papers come from", (f"DAC is {N_DAC} of {N_REC} papers.", "The atlas leans toward design tools."), value=str(N_DAC), label="papers from DAC 2026",
                         text=f"ISCA 2026 adds {N_ISCA} selected architecture papers. ICCAD 2026 papers were not public yet, so {N_ICCAD} come from ICCAD 2025.",
                         cards=[{"label": "DAC 2026", "value": str(N_DAC), "note": "design automation", "key": True}, {"label": "ICCAD 2025", "value": str(N_ICCAD), "note": "design algorithms"}, {"label": "ISCA 2026", "value": str(N_ISCA), "note": "computer architecture"}], src=src),
        "themes": K.slide("diagram", B, 5, n, "Where the attention goes", ("Accelerators, memory and reliability", "lead."), svg=fit(V.s_accel("sl-accel"), 330),
                          cards=[{"svg": R_glyph(g).replace("<svg", "<svg style=\"height:110px;width:auto\"", 1), "label": f"{t['record_count']} papers", "title": t["label"], "note": THEME_POINT[t["theme_id"]][:1].upper() + THEME_POINT[t["theme_id"]][1:] + "."} for t, g in zip(TOP3, ["more/chip-bold", "more/memory-module", "more/shield-tick"])], src=src),
        "loop": K.slide("diagram", B, 6, n, "The common thread", ("Design becomes a loop.", "Checks steer the next try."), svg=fit(V.d_sieve("sl-sieve"), 700), src="Our drawing; the quoted messages are made-up examples"),
        "data": K.slide("diagram", B, 7, n, "Data movement", ("Moving data is often", "the real cost."), svg=fit(V.d_move("sl-move"), 640), src="Our drawing"),
        "physical": K.slide("compare", B, 8, n, "Physics and protection", ("Heat, wires, faults and attacks", "move earlier."),
                            left={"label": "Physical reality", "value": "Heat, wires, power", "points": ["A fast estimate guides early choices.", "An accurate check confirms the final design."], "note": "The fast model must agree with the slow one where it matters."},
                            right={"label": "Faults and attacks", "value": "Named first", "points": ["The threat or fault is stated in the requirement.", "Its cost is shown with protection on."], "note": "Useful correct work, not raw speed."},
                            band=("The test", "Does the early estimate still hold after the full, accurate check?"), src="Our reading of directions 4 and 5"),
        "measure": K.slide("diagram", B, 9, n, "Measurement", ("Better ways", "to measure results."), svg=fit(V.d_bench("sl-bench"), 620), src="Our drawing; task names are made-up examples"),
        "depth": K.slide("number", B, 10, n, "How sure we are", (f"{N_DESC} of {N_REC} records", "come from short descriptions."), value=str(N_FULL), label="papers read from a full paper or preprint",
                         text=f"A program description gives the problem and the claim, rarely the test conditions. {N_DEEP} papers were checked in depth. None was repeated independently.",
                         cards=[{"label": "Descriptions", "value": str(N_DESC), "note": "short program text", "key": True}, {"label": "Abstracts, reports", "value": str(N_ABS), "note": "the claim"}, {"label": "Full papers", "value": str(N_FULL), "note": "methods and limits"}, {"label": "Deep reads", "value": str(N_DEEP), "note": "a page each"}], src=src),
        "watch": K.slide("diagram", B, 11, n, "What to watch", ("Six directions,", "each with its disproof."),
                         svg=fit(V.hbar_svg("sl-dirs", "Evidence papers per direction", [(DIR_SHORT[d], len(DIR_BY[d]["evidence"])) for d in DIR_ORDER]), 560), src="Evidence papers per direction, counted from data/long-term-direction-atlas-v1.json"),
        "start": K.slide("quote", B, 12, n, "Your turn", ("Start with a theme,", "then follow its papers."), text=("Every page explains the problem before the papers,", "and says how deep its sources go."), who=SITE_URL),
    }
    out = []
    for kk in keys:
        o = old[kk]
        out.append({"key": kk, "alt": o["alt"], "notes": o["notes"], "body": body[kk], "cls": ""})
    return out


def spoken(text):
    t = text.replace("ISCA", "isska").replace("ICCAD", "eye cad").replace("DAC", "dack").replace("EDA", "E D A").replace("PDF", "P D F")
    t = re.sub(r"(\d+)%", r"\1 percent", t)
    return t
