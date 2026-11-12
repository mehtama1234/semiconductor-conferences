#!/usr/bin/env python3
"""Second harvest: small drawings and icons from every board that was read, taken as they are, added to kit/glyphs/more/.

Usage: python3 extract_glyphs2.py s2s=<project dir> a2a=<dir> lt=<dir> bg=<dir> mm=<dir>

A drawing is taken when it is small (under 4 kB), is not already in kit/glyphs (compared shape for shape, ignoring size
attributes) and is not one of the large scenes. Names come from tools/glyph_names2.json (written by hand after looking at
the contact sheet); a drawing without a name there is skipped, so nothing unnamed gets in.
`--sheet out.html` writes the contact sheet of candidates with their keys.
"""
import hashlib, html, json, re, sys
from pathlib import Path
KIT = Path(__file__).resolve().parent.parent
NAMES = json.loads((Path(__file__).parent / "glyph_names2.json").read_text()) if (Path(__file__).parent / "glyph_names2.json").exists() else {}
SRC = {"s2s": "Sense to Silicon", "a2a": "Atom to Answer", "lt": "L&T AI Centre Home Designs", "bg": "Robot Buyer's Guide", "mm": "Murmur to Market"}

def norm(svg):
    body = svg.split(">", 1)[1].rsplit("</svg>", 1)[0]
    return hashlib.sha1(re.sub(r"\s+", "", body).lower().encode()).hexdigest()

def candidates(dirs):
    have = {norm(p.read_text()) for p in (KIT / "glyphs").rglob("*.svg") if "more" not in p.parts}
    seen, out = set(have), []
    for key, d in dirs.items():
        for f in sorted(Path(d).glob("*.dc.html")):
            for i, svg in enumerate(re.findall(r"<svg.*?</svg>", f.read_text(), flags=re.S)):
                head = svg[: svg.find(">")]
                vb = re.search(r'viewBox="([^"]*)"', head)
                if not vb or len(svg) > 4000 or len(svg) < 150 or "<text" in svg and svg.count("<text") > 2: continue
                if "strokeWidth" in svg: continue                      # wireframe boards with broken attributes
                h = norm(svg)
                if h in seen: continue
                seen.add(h)
                lab = re.search(r'aria-label="([^"]*)"', head)
                out.append({"key": f"{key}/{f.name[:-8]}#{i}", "svg": svg, "viewBox": vb.group(1), "label": html.unescape(lab.group(1)) if lab else "", "source": f"{SRC[key]} · {f.name[:-8]}"})
    return out

def clean(svg, name, kind):
    head, rest = svg.split(">", 1)
    stroke = re.search(r'\sstroke="currentColor"', head)
    keep = "".join(m.group(0) for m in re.finditer(r'\s(fill|stroke|stroke-width|stroke-linecap|stroke-linejoin)="[^"]*"', head))
    head = re.sub(r'\s(width|height|class|style|xmlns|fill|stroke|stroke-width|stroke-linecap|stroke-linejoin)="[^"]*"', "", head)
    head = head.replace("<svg", f'<svg class="kit-glyph kit-glyph-{kind}" data-glyph="{name}"', 1) + keep
    if "role=" not in head and "aria-hidden" not in head: head += ' aria-hidden="true"'
    return head + ">" + rest

if __name__ == "__main__":
    args = [a for a in sys.argv[1:] if "=" in a and not a.startswith("--")]
    cands = candidates(dict(a.split("=", 1) for a in args))
    if "--sheet" in sys.argv:
        out = sys.argv[sys.argv.index("--sheet") + 1]
        cells = "".join(f'<figure><div>{c["svg"]}</div><figcaption>{i} {html.escape(NAMES.get(c["key"], ["?", "?"])[1])}</figcaption></figure>' for i, c in enumerate(cands))
        Path(out).write_text('<!doctype html><meta charset="utf-8"><style>body{margin:8px;background:#f3ede2;font:11px sans-serif;display:grid;grid-template-columns:repeat(12,1fr);gap:6px}figure{margin:0;background:#fbf7f0;border:1px solid #ccc}figure div{height:84px;display:flex;align-items:center;justify-content:center;background:#ece4d5;color:#2b2622}svg{max-width:96%;max-height:80px;width:auto;height:auto}figcaption{padding:2px}</style>' + cells)
        Path(out).with_suffix(".json").write_text(json.dumps([[i, c["key"], c["viewBox"], c["label"][:60]] for i, c in enumerate(cands)], ensure_ascii=False))
        print(len(cands), "candidates")
    else:
        d = KIT / "glyphs" / "more"; d.mkdir(exist_ok=True)
        for old in d.glob("*.svg"): old.unlink()
        index = []
        for c in cands:
            if c["key"] not in NAMES: continue
            kind, name = NAMES[c["key"]][:2]
            (d / f"{name}.svg").write_text(clean(c["svg"], name, kind) + "\n")
            index.append({"name": name, "kind": kind, "file": f"more/{name}.svg", "viewBox": c["viewBox"], "label": NAMES[c["key"]][2] if len(NAMES[c["key"]]) > 2 else c["label"], "source": c["source"]})
        (KIT / "glyphs" / "more.json").write_text(json.dumps(index, ensure_ascii=False, indent=1) + "\n")
        print(len(index), "glyphs written to glyphs/more")
