"""Clarity audit of every write-up the reader site shows (CLARITY-BRIEF): each sentence is read for length
(over 20 words), vague words, clichés, and field terms that the page uses before (or without) a plain meaning.

  python3 scripts/clarity_audit.py            # writes analysis/clarity/summary.json and one log per page
  python3 scripts/clarity_audit.py --check    # exits 1 if a banned cliché is present on any page

Quotes, paper titles, table rows and the captured evidence records ("Complete captured evidence") are not
rewritten: they are the papers' own words or the coded records. They are counted separately."""
from __future__ import annotations
import json, re, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "analysis/clarity"
sys.path.insert(0, str(ROOT / "scripts"))
from course_story.glossary import GLOSS  # noqa: E402

SOURCES = (sorted((ROOT / "reports/themes").glob("*.md")) + sorted((ROOT / "reports/observed-subthemes").glob("*.md"))
           + sorted((ROOT / "reports/directions").glob("0*.md")) + sorted((ROOT / "reports/comparisons").glob("*.md"))
           + sorted((ROOT / "dac/reports").glob("*-primary-*.md"))
           + [ROOT / p for p in ["reports/reading-guide-v1.md", "reports/expanded-taxonomy-v1.md", "reports/field-directions-and-hypotheses-v1.md", "reports/research-atlas-index-v1.md",
                                 "reports/direction-review-gate-v1.md", "reports/longitudinal-protocol-v1.md", "reports/research-agenda-v1.md", "reports/evidence-summary-v1.md"]])
VAGUE = ["significant", "significantly", "robust", "efficient", "efficiently", "leverage", "leverages", "various", "improves performance", "plays a key role", "in some sense",
         "state-of-the-art", "substantial", "substantially", "effectively", "seamless", "holistic", "novel"]
CLICHE = ["game-changer", "game changer", "at its heart", "the magic", "unlock", "journey", "delve", "powerful", "landscape of", "paradigm shift", "cutting-edge"]
SKIP_FROM = re.compile(r"^## (Complete captured evidence|Every paper in this subtheme)", re.M)


def sentences(md):
    """Prose sentences only: list items and quoted lines are split apart; tables, headings, code, link lists and
    the captured evidence records are left out."""
    md = SKIP_FROM.split(md)[0]
    md = re.sub(r"```.*?```", "", md, flags=re.S)
    out, buf = [], []

    def flush():
        p = " ".join(buf).strip()
        buf.clear()
        if not p:
            return
        p = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", p)
        p = re.sub(r"`[^`]+`", "X", p)
        for s in re.split(r"(?<=[.?!])\s+(?=[A-Z“\"(])", p):
            if s.strip() and not re.match(r"^[\w\s:,.\-–—’'()]+ — (DAC|ICCAD|ISCA) \d{4}\.?$", s.strip()):
                out.append(s.strip())
    for line in md.splitlines():
        l = re.sub(r"^\s*>\s?", "", line).rstrip()
        if not l.strip() or l.lstrip().startswith(("|", "#", "<")):
            flush(); continue
        m = re.match(r"^\s*(?:[-*]|\d+\.)\s+(.*)", l)
        if m:
            flush(); buf.append(m.group(1)); continue
        buf.append(l.strip())
    flush()
    return out


def audit(path):
    md = path.read_text(encoding="utf-8")
    sents = sentences(md)
    low = SKIP_FROM.split(md)[0].lower()
    long_ = [s for s in sents if len(s.split()) > 20 and not s.startswith("“")]
    vague = sorted({w for w in VAGUE if re.search(rf"\b{re.escape(w)}\b", low)})
    cliche = sorted({w for w in CLICHE if re.search(rf"\b{re.escape(w)}\b", low)})
    terms = sorted({k for k in GLOSS if re.search(GLOSS[k][1], md)})
    return {"page": str(path.relative_to(ROOT)), "sentences": len(sents), "over_20_words": len(long_), "vague_words": vague, "cliches": cliche,
            "field_terms_glossed_on_first_use": terms, "long_examples": long_[:5]}


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    rows = [audit(p) for p in SOURCES if p.exists()]
    total = {k: sum(r[k] for r in rows) for k in ("sentences", "over_20_words")}
    summary = {"pages": len(rows), **total, "pages_with_cliches": [r["page"] for r in rows if r["cliches"]],
               "terms_glossed": sum(len(r["field_terms_glossed_on_first_use"]) for r in rows), "rows": rows}
    (OUT / "summary.json").write_text(json.dumps(summary, indent=1, ensure_ascii=False), encoding="utf-8")
    print(json.dumps({k: v for k, v in summary.items() if k != "rows"}, indent=1))
    if "--check" in sys.argv and summary["pages_with_cliches"]:
        sys.exit(1)


if __name__ == "__main__":
    main()
