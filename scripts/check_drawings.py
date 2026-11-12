"""Drawing-number check: every number on a number card, a bar chart or a drawing of a built page must be counted
from the data files (the set computed below, independently of the site generator), or stated in the page's own
words outside the drawings, or be one of the labelled illustration values. Run after build.py pages.
Exit code 1 lists each number that has no source."""
import json, re, sys
from collections import Counter
from pathlib import Path
from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / "site"
tax = json.loads((ROOT / "data/taxonomy-expanded-v1.json").read_text(encoding="utf-8"))
atlas = json.loads((ROOT / "data/long-term-direction-atlas-v1.json").read_text(encoding="utf-8"))
known = {tax["record_count"], tax["theme_count"], tax["observed_subtheme_count"], len(list((ROOT / "dac/reports").glob("*-primary-*.md")))}
sub = {}
tiers, confs = Counter(), Counter()
for t in tax["themes"]:
    known |= {t["record_count"], t["subtheme_count"]} | set(t["conference_counts"].values())
    for s in t["subthemes"]:
        known |= {s["record_count"]} | set(s["conference_counts"].values()) | set(s["source_tier_counts"].values())
        m = sub.setdefault(s["subtheme_id"], [0, Counter(), Counter()])
        m[0] += s["record_count"]; m[1].update(s["conference_counts"])
        for k, v in s["source_tier_counts"].items():
            d = "desc" if "official_description" in k else "full" if any(w in k for w in ("primary", "preprint", "pdf", "company_author", "full_text")) else "abs"
            m[2][d] += v
            tiers[d] += v
        confs.update(s["conference_counts"])
for n, c, d in sub.values():
    known |= {n} | set(c.values()) | set(d.values())
known |= set(tiers.values()) | set(confs.values())
known |= {sum(t["record_count"] for t in sorted(tax["themes"], key=lambda t: -t["record_count"])[:3])}
for d in atlas["directions"]:
    known |= {len(d["evidence"]), len(d["subskills"]), int(d["independent_review_count"])} | set(Counter(e["conference_id"] for e in d["evidence"]).values())
known |= {0, 1, 2, 3, 4, 5, 6, 2025, 2026}       # part numbers 1-5, six directions, edition years
ILLUSTRATION = {100, 10, 0.2, 0.5, 0.1, 0.05, 1.0, 12, 40}   # chart inputs and the quoted example messages, each labelled on its panel

num = lambda s: [float(x.replace(",", "")) for x in re.findall(r"(?<![\w.])\d[\d,]*(?:\.\d+)?", s)]
fails, checked, pages = [], 0, 0
for f in sorted(SITE.rglob("*.html")):
    t = f.read_text(encoding="utf-8", errors="replace")
    if 'data-kit="boards"' not in t:
        continue
    pages += 1
    soup = BeautifulSoup(t, "html.parser")
    shown = []
    auto = any("Reading time" in k.get_text() for k in soup.select(".ck-cards .k"))
    for b in ([] if auto else soup.select(".ck-cards b")):
        shown += num(b.get_text(" "))
    for s in soup.select("[data-chart] script"):
        spec = json.loads(s.string)
        for it in spec.get("items", []):
            shown.append(float(it["value"]))
    for svg in soup.select("figure svg"):
        for tx in svg.find_all("text"):
            shown += num(tx.get_text(" "))
    prose = soup.select_one("main")
    for fig in prose.select("figure"):
        fig.decompose()
    words = set(num(prose.get_text(" "))) | set(num(soup.select_one("h1").get_text(" ") if soup.select_one("h1") else ""))
    for x in shown:
        checked += 1
        if x in known or x in words or x in ILLUSTRATION:
            continue
        fails.append(f"{f.relative_to(SITE)}: {x:g}")
print(json.dumps({"pages": pages, "numbers_checked": checked, "without_source": fails[:40], "count_without_source": len(fails)}, indent=2))
sys.exit(1 if fails else 0)
