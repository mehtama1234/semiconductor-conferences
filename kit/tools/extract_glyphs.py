#!/usr/bin/env python3
"""Copy the boards' own drawings into kit/glyphs/ as inline-SVG partials, unchanged.

Usage: python3 extract_glyphs.py <sense-to-silicon/project> <atom-to-answer/project>

The drawings are taken as they are (paths, colours, stroke widths). The only edits are:
the fixed width/height attributes are dropped so CSS can size the drawing, and class="kit-glyph"
plus a data-glyph name are added. Colours stay as the boards' hex values; course.css maps them
to tokens (so the dark theme works) with attribute selectors.
"""
import json, re, sys, html
from pathlib import Path

OUT = Path(__file__).resolve().parent.parent / "glyphs"
LINE_NAMES = """atoms-packed thermoelectric crystals ingot band-gap dissolve-beaker flask-to-tube membrane
cell-ring flask-caution capsules thermometer-peak haze-skyline mosquito bead-chain cells-lens dna
spike-traces warm-sea quake-ripples river-gauge wildfire gas-plume buoy snowmelt volcano sea-ice
glacier range-map coral wheat frost-seedling batteries solar-panel heat-sink detector-tracks sunspots
solar-wind observatory variable-star transit""".split()
FILLED = {  # aria-label prefix -> name (380 x 190 filled glyphs on sand)
    "A battery with most": "battery", "A converter: numbers": "converter", "A balance:": "scale",
    "A stack of research": "documents", "A tag with a question": "tag", "A shield with a tick": "shield",
    "A robot finger": "finger", "A trained model": "network", "Work splitting": "split",
    "A chip seen from above": "chip", "Two copper atoms 2.55": "atoms-scale",
    "A battery cell drawn": "battery-layers", "Side view of a chip": "cold-plate",
}
SPOT = {  # 230 x 150 mechanism sketches from As20Domains
    "Two copper atoms with push": "rerun-check", "A known exact curve": "curve-check",
    "Capacity falling": "held-back", "An answer is locked": "locked-answer", "A box with a movement": "limit-box",
}

def clean(svg, name, kind):
    head, rest = svg.split(">", 1)
    head = re.sub(r'\s(width|height|class|style)="[^"]*"', "", head)
    head = head.replace("<svg", f'<svg class="kit-glyph kit-glyph-{kind}" data-glyph="{name}"', 1)
    if "role=" not in head and "aria-hidden" not in head:
        head += ' aria-hidden="true"'
    return head + ">" + rest

def svgs(path):
    return re.findall(r"<svg.*?</svg>", path.read_text(), flags=re.S)

def label(svg):
    m = re.search(r'aria-label="([^"]*)"', svg[: svg.find(">")])
    return html.unescape(m.group(1)) if m else ""

def main(s2s, a2a):
    s2s, a2a = Path(s2s), Path(a2a)
    index = []
    def save(kind, name, svg, source, lab=None):
        d = OUT / kind; d.mkdir(parents=True, exist_ok=True)
        (d / f"{name}.svg").write_text(clean(svg, name, kind) + "\n")
        vb = re.search(r'viewBox="([^"]*)"', svg).group(1)
        index.append({"name": name, "kind": kind, "file": f"{kind}/{name}.svg", "viewBox": vb,
                      "label": lab if lab is not None else label(svg), "source": source})
    # 1. the 41 line drawings, one per problem
    gal = [s for s in svgs(a2a / "As33Gallery.dc.html") if 'viewBox="0 0 240 150"' in s]
    assert len(gal) == 41 == len(LINE_NAMES), len(gal)
    for name, svg in zip(LINE_NAMES, gal):
        save("line", name, svg, "Atom to Answer · As33Gallery")
    # 2. filled glyphs
    seen = set()
    for board, f in [("Sense to Silicon · WsHome", s2s / "WsHome.dc.html"), ("Atom to Answer · As20Domains", a2a / "As20Domains.dc.html")]:
        for svg in svgs(f):
            lab = label(svg)
            for pre, name in {**FILLED, **SPOT}.items():
                if lab.startswith(pre) and name not in seen:
                    seen.add(name); save("spot" if pre in SPOT else "filled", name, svg, board)
    # 3. unlabelled drawings and icons, named by hand after looking at a contact sheet.
    #    Index = position among the board's unlabelled drawings not already seen on an earlier board.
    picks = {
        "As19Insights": {0: ("icons", "check"), 1: ("icons", "lines"), 2: ("icons", "question"), 3: ("icons", "lock")},
        "As2Landing": {0: ("icons", "pencil"), 1: ("icons", "bars"), 2: ("icons", "open-circle"), 3: ("filled", "signpost"),
                       4: ("filled", "stamp"), 5: ("filled", "bars-compare"), 6: ("icons", "cross"), 7: ("icons", "stamp"),
                       8: ("icons", "database"), 9: ("filled", "atoms-push"), 11: ("filled", "window")},
        "AhConcept": {1: ("filled", "grid-corner"), 2: ("filled", "gauge")},
        "AhLanding": {0: ("filled", "flask"), 1: ("filled", "blocks"), 2: ("filled", "tag-dashed"), 4: ("filled", "crossbar")},
        "Ch1CameraChallenge": {0: ("mini", "pixels"), 1: ("mini", "image"), 2: ("mini", "graph"), 3: ("mini", "play"),
                               4: ("mini", "plug"), 5: ("mini", "cluster"), 6: ("mini", "heat"), 7: ("mini", "sensor"),
                               8: ("mini", "wave"), 9: ("mini", "staircase"), 10: ("mini", "flag"), 11: ("filled", "pixels-to-chip"),
                               12: ("filled", "chip-link"), 13: ("filled", "report"), 14: ("mini", "sliders"),
                               15: ("mini", "cost"), 16: ("mini", "meter")},
        "WsHome": {0: ("icons", "badge"), 1: ("icons", "shield-check"), 2: ("icons", "shield"), 3: ("icons", "nodes"),
                   4: ("icons", "pulse"), 5: ("icons", "chip")},
    }
    sizes = r'viewBox="0 0 (380 190|24 24|40 40|52 52|240 116|280 130|240 130)"'
    got = set()
    files = sorted(list(s2s.glob("*.dc.html")) + list(a2a.glob("*.dc.html")), key=lambda p: (p.parent != a2a, p.name))
    for f in files:
        n = 0
        for s in svgs(f):
            head = s[: s.find(">")]
            if "aria-label" in head or not re.search(sizes, head): continue
            body = s.split(">", 1)[1]
            if body in got: continue
            got.add(body)
            kind_name = picks.get(f.name[:-8], {}).get(n); n += 1
            if kind_name:
                board = ("Sense to Silicon" if f.parent == s2s else "Atom to Answer") + " · " + f.name[:-8]
                save(kind_name[0], kind_name[1], s, board, lab="")
    (OUT / "index.json").write_text(json.dumps(index, indent=1) + "\n")
    print(len(index), "glyphs")

if __name__ == "__main__":
    main(*sys.argv[1:3])
