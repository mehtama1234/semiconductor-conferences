"""Drawings, charts and number cards for every page of the semiconductor conference atlas, in the board kit's hand.

What is drawn is the thing each page is about: an accelerator's compute grid fed from memory, a memory ladder,
a chip under fault and attack, a request queue, a design loop with its checkers, a state space with tests and a
proof, a placed and routed block with a timing path, an analog crossbar, a design rewritten through a graph,
and a package cross-section with stacked dies. Each theme scene marks the part a subtheme or paper works on.

Numbers: every count on a card, chart or drawing is counted at build time from data/taxonomy-expanded-v1.json or
data/long-term-direction-atlas-v1.json (chip "counted"), or is quoted from the page's own report (chip "from the
papers"). The few made-up values that drive the interactive charts are listed in ILLUSTRATION, stated with their
formula in the caption, and carry the chip "illustration". scripts/check_drawings.py re-checks every number."""
from __future__ import annotations

import html, json, math, re, sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "kit"))
import render_lecture as R  # noqa: E402
import scenes  # noqa: E402

esc = lambda s: html.escape(str(s), quote=True)
INK, MUTE, ESP, PAPER, SAND, LINE, RUST, PEACH, SOFT, TAN = "#2b2622", "#5a5047", "#3a2e26", "#fbf7f0", "#ece4d5", "#d9cdba", "#9a4a22", "#e3b98f", "#f5e6d3", "#cdbfa9"
F_LAB = 'font-family="IBM Plex Sans Condensed, sans-serif"'
F_SER = 'font-family="Fraunces, Georgia, serif"'

TAX = json.loads((ROOT / "data/taxonomy-expanded-v1.json").read_text(encoding="utf-8"))
ATLAS = json.loads((ROOT / "data/long-term-direction-atlas-v1.json").read_text(encoding="utf-8"))
THEME_BY = {t["theme_id"]: t for t in TAX["themes"]}
SUB, SUB_THEME = {}, {}
for t in TAX["themes"]:
    for s in t["subthemes"]:
        SUB_THEME.setdefault(s["subtheme_id"], t)
        m = SUB.setdefault(s["subtheme_id"], {"label": s["label"], "record_count": 0, "conf": Counter(), "tier": Counter(), "mech": set()})
        m["record_count"] += s["record_count"]
        m["conf"].update(s["conference_counts"])
        m["tier"].update(s["source_tier_counts"])
        m["mech"] |= {x["id"] for x in s["mechanisms"]}


def depth(tier):
    if "official_description" in tier:
        return "desc"
    if any(w in tier for w in ("primary", "preprint", "pdf", "company_author", "full_text")):
        return "full"
    return "abs"


ILLUSTRATION = {100, 10, 0.2, 0.5, 0.1, 0.05, 1.0, 12, 40, 2}   # chart inputs and the quoted example messages, each labelled   # made-up inputs of the interactive charts, each labelled "illustration"


# ------------------------------------------------------------------------------------------- drawing helpers

class Svg:
    def __init__(self, uid, title, w=1000, h=420):
        self.uid, self.w, self.h, self.h0 = uid, w, h, h
        self.out = [f'<svg class="ck-art" viewBox="0 0 {w} {h}" role="img" aria-labelledby="{uid}-t" {F_LAB}><title id="{uid}-t">{esc(title)}</title>',
                    f'<defs><marker id="{uid}-a" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0L10 5 0 10z" fill="{INK}"/></marker>'
                    f'<marker id="{uid}-r" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0L10 5 0 10z" fill="{RUST}"/></marker>'
                    f'<pattern id="{uid}-h" width="8" height="8" patternUnits="userSpaceOnUse" patternTransform="rotate(45)"><path d="M0 0V8" stroke="{TAN}" stroke-width="3"/></pattern></defs>']

    def add(self, s):
        self.out.append(s)
        return self

    def text(self, x, y, s, size=17, fill=INK, anchor="start", weight=None, serif=False, italic=False, spacing=None):
        a = f' text-anchor="{anchor}"' if anchor != "start" else ""
        w = f' font-weight="{weight}"' if weight else ""
        f = f" {F_SER}" if serif else ""
        it = ' font-style="italic"' if italic else ""
        ls = f' letter-spacing="{spacing}"' if spacing else ""
        self.out.append(f'<text x="{x}" y="{y}" font-size="{size}" fill="{fill}"{a}{w}{f}{it}{ls}>{esc(s)}</text>')
        return self

    def arrow(self, d, rust=False, dash=False, width=2):
        self.out.append(f'<path d="{d}" fill="none" stroke="{RUST if rust else INK}" stroke-width="{width}"{" stroke-dasharray=" + chr(34) + "7 6" + chr(34) if dash else ""} marker-end="url(#{self.uid}-{"r" if rust else "a"})"/>')
        return self

    def label(self, x, y, k, a, b="", on=False, anchor="middle"):
        """A station label: number and name in caps, then one or two plain lines."""
        self.text(x, y, k.upper(), 15, RUST if on else INK, anchor, 600, spacing=1)
        if a:
            self.text(x, y + 21, a, 15, INK, anchor)
        if b:
            self.text(x, y + 42, b, 15, MUTE, anchor)
        return self

    def ring(self, x, y, w, h, on):
        """The highlight around the part a subtheme or paper works on."""
        if on:
            self.out.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="12" fill="none" stroke="{RUST}" stroke-width="3" stroke-dasharray="9 6"/>')
        return self

    def note(self, at, lines, name=""):
        """The dark note box under the drawing; the rust ring marks the part it speaks about."""
        y = self.h0 + 14
        self.out.append(f'<rect x="10" y="{y}" width="{self.w - 20}" height="96" rx="8" fill="{ESP}"/>')
        self.out.append(f'<text x="30" y="{y + 28}" font-size="15" fill="{PEACH}" font-weight="600" letter-spacing="1.5">{esc(("Part " + str(at + 1) + " · " + name).upper())} · RINGED ABOVE</text>')
        self.out.append(f'<text x="30" y="{y + 56}" font-size="20" fill="#f3ede2">{esc(lines[0])}</text>')
        if len(lines) > 1:
            self.out.append(f'<text x="30" y="{y + 82}" font-size="20" fill="#f3ede2">{esc(lines[1])}</text>')
        return self

    def finish(self, at, note, name, motto=None, motto_y=None):
        """Without a note: the scene's one-line point in italic. With one: the note box, and the height grows."""
        if note and at is not None:
            self.note(at, note, name)
            h = self.h0 + 120
        else:
            if motto:
                self.text(self.w / 2, motto_y or self.h0 - 14, motto, 18, RUST, "middle", italic=True, serif=True)
            h = self.h0
        self.out[0] = re.sub(r'viewBox="0 0 (\d+) \d+"', lambda m: f'viewBox="0 0 {m.group(1)} {h}"', self.out[0])
        return self.done()

    def done(self):
        return "".join(self.out) + "</svg>"


def _grid(s, x, y, n, m, cw, ch, fill=PAPER, on=None, stroke=INK):
    for i in range(n):
        for j in range(m):
            f = PEACH if on and (i, j) in on else fill
            s.add(f'<rect x="{x + j * cw}" y="{y + i * ch}" width="{cw - 4}" height="{ch - 4}" rx="2" fill="{f}" stroke="{stroke}" stroke-width="1.3"/>')


def _chip(s, x, y, w, h, label="", pins=True, fill=PAPER):
    if pins:
        for k in range(1, 6):
            px = x + k * w / 6
            s.add(f'<path d="M{px:.0f} {y - 10}V{y}M{px:.0f} {y + h}V{y + h + 10}" stroke="{INK}" stroke-width="2"/>')
    s.add(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="6" fill="{fill}" stroke="{INK}" stroke-width="2"/>')
    if label:
        s.text(x + w / 2, y + h / 2 + 6, label, 16, INK, "middle", 600)


# ------------------------------------------------------------------------------------------- the ten theme scenes
# Each takes at (index of the highlighted part, or None) and note (two short lines said about that part).
# STATIONS[theme] names the parts in order; the subtheme and paper pages pick one.

STATIONS = {
    "architecture-and-accelerators": ["The workload", "Off-chip memory", "On-chip buffers", "The compute grid", "The result"],
    "memory-interconnect-and-storage": ["Core and caches", "Main memory", "Storage", "Chip-to-chip links", "Logic in memory"],
    "power-reliability-and-security": ["A fault", "An attacker", "The protection", "Heat and power", "The cost"],
    "systems-applications-and-workloads": ["Requests", "The scheduler", "Data-centre servers", "Small devices", "The deadline"],
    "ai-assisted-eda": ["The requirement", "The model proposes", "Tools check", "Feedback", "The accepted design"],
    "verification-and-validation": ["The property", "The design", "Tests", "A proof", "A missed bug"],
    "physical-design-and-manufacturing": ["The netlist", "Placement", "Wiring", "Timing", "Manufacture"],
    "analog-mixed-signal-and-emerging-devices": ["Inputs as voltages", "Devices store weights", "Currents add up", "Noise and drift", "The converter"],
    "design-methodology-and-tooling": ["The description", "The graph", "A rewrite", "Same function?", "The cost estimate"],
    "chiplets-3d-and-packaging": ["Split into dies", "Links between dies", "Stacked dies", "The heat path", "The package"],
}


def _start(key, uid, at, title, h0):
    st = STATIONS[key]
    s = Svg(uid, title + (f"; ringed: part {at + 1}, {st[at].lower()}" if at is not None else ""), 1000, h0)
    return s, st, (lambda i: at == i)


def s_accel(uid, at=None, note=None):
    s, st, on = _start("architecture-and-accelerators", uid, at, "An accelerator: a layer's numbers come from off-chip memory through on-chip buffers into a grid of compute units", 330)
    s.ring(10, 24, 172, 270, on(0))
    _grid(s, 30, 54, 4, 3, 26, 26, SOFT)
    s.text(120, 104, "×", 30, INK, "middle")
    _grid(s, 106, 124, 3, 2, 26, 26, SOFT)
    s.label(96, 236, "1 · " + st[0], "a layer of a model", "two grids of numbers", on(0))
    s.ring(196, 24, 180, 270, on(1))
    for k in range(3):
        _chip(s, 222, 52 + k * 52, 128, 34, "DRAM" if k == 1 else "", pins=False, fill=SAND)
    s.label(286, 236, "2 · " + st[1], "big and far away", "slow to reach", on(1))
    s.arrow("M378 120H420", width=4)
    s.text(399, 108, "narrow", 14, MUTE, "middle")
    s.ring(422, 24, 156, 270, on(2))
    for k in range(4):
        s.add(f'<rect x="446" y="{48 + k * 40}" width="108" height="30" rx="3" fill="{PAPER}" stroke="{INK}" stroke-width="1.6"/>'
              f'<path d="M{458 + k * 8} {63 + k * 40}h{60 - k * 10}" stroke="{TAN}" stroke-width="8"/>')
    s.label(500, 236, "3 · " + st[2], "small and near", "fast to reach", on(2))
    s.arrow("M578 90H612", width=3).arrow("M578 150H612", width=3)
    s.ring(612, 16, 226, 278, on(3))
    for i in range(5):
        for j in range(5):
            x, y = 632 + j * 38, 30 + i * 38
            busy = (i + j) % 3 != 2
            s.add(f'<rect x="{x}" y="{y}" width="28" height="28" rx="3" fill="{PEACH if busy else PAPER}" stroke="{INK}" stroke-width="1.4"/>')
            if j < 4:
                s.add(f'<path d="M{x + 29} {y + 14}h8" stroke="{MUTE}" stroke-width="1.4"/>')
            if i < 4:
                s.add(f'<path d="M{x + 14} {y + 29}v8" stroke="{MUTE}" stroke-width="1.4"/>')
    s.label(724, 236, "4 · " + st[3], "each unit passes numbers on", "pale units wait for data", on(3))
    s.arrow("M840 120H866", width=3)
    s.ring(866, 24, 124, 270, on(4))
    s.add(f'<circle cx="928" cy="84" r="32" fill="{PAPER}" stroke="{INK}" stroke-width="2"/><path d="M928 84V62M928 84l15 9" stroke="{RUST}" stroke-width="3" stroke-linecap="round"/>'
          f'<path d="M918 136l-12 26h16l-8 24 24-32h-16l10-18z" fill="{PEACH}" stroke="{INK}" stroke-width="1.6" stroke-linejoin="round"/>')
    s.label(928, 236, "5 · " + st[4], "time and energy", "for the whole layer", on(4))
    return s.finish(at, note, st[at] if at is not None else "", "Adding compute units does not help while the narrow pipe stays narrow.", 322)


def s_memory(uid, at=None, note=None):
    s, st, on = _start("memory-interconnect-and-storage", uid, at, "A memory ladder: core and caches, main memory, storage, links between chips, and logic placed inside memory", 380)
    xs = [100, 300, 500, 700, 900]
    s.ring(10, 20, 180, 280, on(0))
    _chip(s, 30, 46, 140, 120, "", pins=True)
    s.add(f'<rect x="44" y="60" width="52" height="40" fill="{PEACH}" stroke="{INK}"/><text x="70" y="85" font-size="14" text-anchor="middle" fill="{INK}">core</text>'
          f'<rect x="104" y="60" width="54" height="40" fill="{SOFT}" stroke="{INK}"/><text x="131" y="85" font-size="14" text-anchor="middle" fill="{INK}">cache</text>'
          f'<rect x="44" y="108" width="114" height="44" fill="{SOFT}" stroke="{INK}"/><text x="101" y="135" font-size="14" text-anchor="middle" fill="{INK}">bigger cache</text>')
    s.label(xs[0], 236, "1 · " + st[0], "nearest and smallest", "", on(0))
    s.ring(206, 20, 188, 280, on(1))
    for k in range(2):
        y = 46 + k * 60
        s.add(f'<rect x="220" y="{y}" width="160" height="44" rx="3" fill="{SAND}" stroke="{INK}" stroke-width="1.8"/>')
        for c in range(5):
            s.add(f'<rect x="{228 + c * 30}" y="{y + 8}" width="24" height="28" fill="{PAPER}" stroke="{INK}"/>')
    s.label(xs[1], 236, "2 · " + st[1], "memory modules", "", on(1))
    s.ring(406, 20, 188, 280, on(2))
    s.add(f'<rect x="420" y="46" width="160" height="110" rx="10" fill="{PAPER}" stroke="{INK}" stroke-width="2"/><circle cx="500" cy="101" r="36" fill="{SOFT}" stroke="{INK}"/><circle cx="500" cy="101" r="6" fill="{INK}"/>'
          f'<path d="M500 101l30-24" stroke="{RUST}" stroke-width="3"/>')
    s.label(xs[2], 236, "3 · " + st[2], "largest and farthest", "", on(2))
    s.ring(606, 20, 188, 280, on(3))
    for k, (x, y) in enumerate([(624, 46), (724, 46), (624, 130), (724, 130)]):
        _chip(s, x, y, 52, 40, "", pins=False, fill=SAND if k % 2 else PAPER)
    s.add(f'<path d="M676 66H724M676 150H724M650 86V130M750 86V130" stroke="{RUST if on(3) else INK}" stroke-width="3"/>'
          f'<circle cx="700" cy="108" r="15" fill="{PAPER}" stroke="{INK}" stroke-width="2"/><path d="M689 108h22M700 97v22" stroke="{INK}" stroke-width="2"/>')
    s.label(xs[3], 236, "4 · " + st[3], "a switch joins chips", "", on(3))
    s.ring(806, 20, 184, 280, on(4))
    s.add(f'<rect x="826" y="46" width="144" height="70" rx="3" fill="{SAND}" stroke="{INK}" stroke-width="1.8"/>'
          + "".join(f'<rect x="{834 + c * 28}" y="54" width="22" height="26" fill="{PAPER}" stroke="{INK}"/>' for c in range(5))
          + f'<rect x="846" y="88" width="104" height="22" rx="3" fill="{PEACH}" stroke="{INK}" stroke-width="1.6"/><text x="898" y="104" font-size="13" text-anchor="middle" fill="{INK}">logic inside</text>')
    s.label(xs[4], 236, "5 · " + st[4], "send work to the data", "", on(4))
    s.arrow("M60 330H940", width=3)
    s.text(500, 356, "left to right: more room, longer wait, more energy for each byte moved", 16, MUTE, "middle")
    return s.finish(at, note, st[at] if at is not None else "")


def s_protect(uid, at=None, note=None):
    s, st, on = _start("power-reliability-and-security", uid, at, "A chip under a fault and an attack: a particle flips a stored bit, a probe reads the power trace, check bits find the flip, a hot spot builds, and each protection costs time, energy and area", 370)
    s.add(f'<rect x="330" y="40" width="330" height="230" rx="8" fill="{PAPER}" stroke="{INK}" stroke-width="2.4"/>')
    _grid(s, 352, 62, 4, 8, 30, 30, SOFT)
    s.add(f'<rect x="352" y="62" width="26" height="26" rx="2" fill="{RUST}"/><text x="365" y="81" font-size="15" text-anchor="middle" fill="#fbf7f0" font-weight="600">1</text>')
    s.add(f'<rect x="602" y="62" width="40" height="116" rx="3" fill="{PEACH}" stroke="{INK}" stroke-width="1.4"/><text x="622" y="124" font-size="13" text-anchor="middle" fill="{INK}" transform="rotate(-90 622 124)">check bits</text>')
    s.add(f'<ellipse cx="560" cy="226" rx="70" ry="30" fill="{PEACH}" opacity=".85"/><ellipse cx="560" cy="226" rx="38" ry="15" fill="{RUST}" opacity=".7"/>')
    s.ring(10, 20, 300, 150, on(0))
    s.add(f'<path d="M48 52L344 74" stroke="{RUST}" stroke-width="3" stroke-dasharray="3 6"/><circle cx="48" cy="52" r="8" fill="{RUST}"/>')
    s.label(150, 112, "1 · " + st[0], "a stray particle", "flips a stored 0 to 1", on(0))
    s.ring(10, 182, 300, 140, on(1))
    s.add(f'<path d="M330 236H286" stroke="{INK}" stroke-width="2"/><circle cx="280" cy="236" r="8" fill="{PAPER}" stroke="{INK}" stroke-width="2"/>'
          f'<path d="M40 216l20 0 8-20 8 34 8-26 8 18 8-12 8 6 20 0 8-28 8 40 8-24 8 8 20 0" fill="none" stroke="{INK}" stroke-width="2"/>')
    s.label(150, 270, "2 · " + st[1], "reads secrets from", "the power the chip draws", on(1))
    s.ring(594, 52, 56, 136, on(2)).ring(484, 190, 152, 72, on(3))
    s.add(f'<path d="M646 120H700M634 226H700" stroke="{MUTE}" stroke-dasharray="4 4"/>')
    s.label(706, 112, "3 · " + st[2], "extra bits spot a flip", "and fix it", on(2), anchor="start")
    s.label(706, 220, "4 · " + st[3], "a hot spot ages", "the chip faster", on(3), anchor="start")
    s.ring(330, 286, 380, 76, on(4))
    for k, (lab, w) in enumerate([("time", 200), ("energy", 160), ("area", 110)]):
        y = 298 + k * 20
        s.add(f'<rect x="420" y="{y}" width="{w}" height="13" fill="{TAN}"/><rect x="{420 + w}" y="{y}" width="{int(w * 0.18)}" height="13" fill="{RUST}"/>')
        s.text(410, y + 12, lab, 14, MUTE, "end")
    s.label(730, 308, "5 · " + st[4], "rust: what protection adds", "", on(4), anchor="start")
    return s.finish(at, note, st[at] if at is not None else "")


def s_systems(uid, at=None, note=None):
    s, st, on = _start("systems-applications-and-workloads", uid, at, "Requests arrive, wait in a queue, a scheduler sends them to data-centre servers or small devices, and each must finish before its deadline", 330)
    s.ring(10, 20, 176, 268, on(0))
    for k, y in enumerate([36, 96, 156]):
        s.add(f'<rect x="36" y="{y}" width="34" height="50" rx="6" fill="{PAPER}" stroke="{INK}" stroke-width="2"/><circle cx="53" cy="{y + 42}" r="3" fill="{INK}"/>')
        s.add(f'<circle cx="122" cy="{y + 24}" r="12" fill="{PEACH if k != 1 else SOFT}" stroke="{INK}"/><path d="M76 {y + 24}h32" stroke="{INK}" stroke-width="1.6"/>')
    s.label(98, 240, "1 · " + st[0], "each with a deadline", "", on(0))
    s.ring(200, 20, 256, 268, on(1))
    for k in range(6):
        s.add(f'<rect x="{220 + k * 28}" y="104" width="22" height="34" rx="3" fill="{PEACH if k < 2 else PAPER}" stroke="{INK}" stroke-width="1.5"/>')
    s.add(f'<path d="M218 98h170M218 144h170" stroke="{INK}" stroke-width="2"/>')
    s.add(f'<circle cx="418" cy="121" r="22" fill="{SAND}" stroke="{INK}" stroke-width="2"/><path d="M408 121h20M418 111v20" stroke="{INK}" stroke-width="2"/>')
    s.label(328, 240, "2 · " + st[1], "who runs next, and where", "", on(1))
    s.arrow("M440 110C470 70 490 60 506 60").arrow("M440 132C470 172 490 182 506 182")
    s.ring(506, 14, 220, 112, on(2))
    for k in range(3):
        x = 530 + k * 52
        s.add(f'<rect x="{x}" y="28" width="40" height="84" rx="3" fill="{SAND}" stroke="{INK}" stroke-width="1.8"/>' + "".join(f'<path d="M{x + 6} {38 + r * 15}h28" stroke="{INK}" stroke-width="1.4"/>' for r in range(5)))
    s.label(740, 52, "3 · " + st[2], "many requests share", "one machine", on(2), anchor="start")
    s.ring(506, 140, 220, 112, on(3))
    s.add(f'<rect x="540" y="152" width="44" height="86" rx="8" fill="{PAPER}" stroke="{INK}" stroke-width="2"/><rect x="548" y="162" width="28" height="56" fill="{SOFT}"/>'
          f'<rect x="616" y="176" width="80" height="48" rx="6" fill="{PAPER}" stroke="{INK}" stroke-width="2"/><circle cx="634" cy="230" r="8" fill="{INK}"/><circle cx="678" cy="230" r="8" fill="{INK}"/>')
    s.label(740, 182, "4 · " + st[3], "phones, robots, cars", "little power to spare", on(3), anchor="start")
    s.ring(200, 268 - 2, 0, 0, False)
    s.add(f'<circle cx="776" cy="294" r="20" fill="{PAPER}" stroke="{INK}" stroke-width="2"/><path d="M776 294V279M776 294l11 6" stroke="{RUST}" stroke-width="3" stroke-linecap="round"/>')
    s.ring(740, 262, 250, 62, on(4))
    s.label(808, 290, "5 · " + st[4], "", "", on(4), anchor="start")
    s.text(808, 310, "late counts as failed", 15, MUTE)
    return s.finish(at, note, st[at] if at is not None else "", "The slowest few requests decide what users feel.", 318)


def s_aieda(uid, at=None, note=None):
    s, st, on = _start("ai-assisted-eda", uid, at, "A design loop: a requirement goes to a model that proposes hardware code, tools compile, simulate and time it, failures go back as feedback, and only a design that passes every check is accepted", 380)
    s.ring(10, 20, 170, 262, on(0))
    s.add(f'<path d="M40 40h90l24 24v130H40z" fill="{PAPER}" stroke="{INK}" stroke-width="2"/><path d="M130 40v24h24" fill="none" stroke="{INK}" stroke-width="2"/>'
          + "".join(f'<path d="M54 {82 + k * 18}h{70 - (k % 3) * 14}" stroke="{TAN}" stroke-width="5"/>' for k in range(6)))
    s.label(95, 236, "1 · " + st[0], "what the circuit must do", "", on(0))
    s.arrow("M182 120H214")
    s.ring(216, 20, 200, 262, on(1))
    for i, n in enumerate([3, 4, 3]):
        for k in range(n):
            y = 120 + (k - (n - 1) / 2) * 36
            s.add(f'<circle cx="{256 + i * 60}" cy="{y:.0f}" r="11" fill="{PEACH if i == 1 else SOFT}" stroke="{INK}" stroke-width="1.6"/>')
    s.add(f'<path d="M256 84L316 66M256 120L316 138M316 102L376 84M316 138L376 156M256 156L316 174" stroke="{MUTE}" stroke-width="1.2"/>')
    s.label(316, 236, "2 · " + st[1], "code, layout or settings", "", on(1))
    s.arrow("M418 120H452")
    s.ring(454, 20, 290, 262, on(2))
    for k, (lab, ok) in enumerate([("compile", True), ("simulate", True), ("meet timing", False)]):
        y = 40 + k * 56
        s.add(f'<rect x="474" y="{y}" width="170" height="40" rx="5" fill="{PAPER}" stroke="{INK}" stroke-width="1.8"/>')
        s.text(492, y + 26, lab, 17, INK)
        if ok:
            s.add(f'<path d="M668 {y + 20}l9 9 17-19" fill="none" stroke="{INK}" stroke-width="3" stroke-linecap="round"/>')
        else:
            s.add(f'<path d="M670 {y + 10}l20 20M690 {y + 10}l-20 20" stroke="{RUST}" stroke-width="3.4" stroke-linecap="round"/>')
    s.label(599, 236, "3 · " + st[2], "pass or fail, never a guess", "", on(2))
    s.arrow("M746 120H784")
    s.ring(786, 20, 204, 262, on(4))
    _chip(s, 834, 60, 110, 90, "", pins=True)
    s.add(f'<path d="M870 106l12 12 26-28" fill="none" stroke="{INK}" stroke-width="3.4" stroke-linecap="round"/>')
    s.label(888, 236, "5 · " + st[4], "every check passed", "", on(4))
    s.ring(216, 292, 528, 80, on(3))
    s.arrow("M680 180C720 290 620 330 470 330C340 330 316 300 316 286", rust=True, dash=True, width=2.6)
    s.text(470, 318, "4 · " + st[3].upper(), 15, RUST, "middle", 600, spacing=1)
    s.text(470, 360, "which check failed, and where: the next try uses it", 15, MUTE, "middle")
    return s.finish(at, note, st[at] if at is not None else "")


def s_verify(uid, at=None, note=None):
    s, st, on = _start("verification-and-validation", uid, at, "All the states a design can reach: tests visit scattered points, a proof covers a shaded region for one stated property, and a bug can sit where neither reaches", 400)
    s.ring(10, 20, 224, 160, on(0))
    s.add(f'<rect x="30" y="40" width="184" height="70" rx="6" fill="{ESP}"/><text x="122" y="70" font-size="16" text-anchor="middle" fill="#f3ede2">every request</text><text x="122" y="94" font-size="16" text-anchor="middle" fill="#f3ede2">gets an answer</text>')
    s.label(122, 136, "1 · " + st[0], "stated exactly", "", on(0))
    s.ring(10, 196, 224, 160, on(1))
    _chip(s, 52, 222, 140, 66, "design", pins=True)
    s.label(122, 324, "2 · " + st[1], "every state it can reach", "", on(1))
    s.arrow("M236 256C266 248 276 222 292 212")
    s.add(f'<path d="M296 60C376 10 636 20 716 70C786 120 786 270 696 310C596 350 376 340 316 290C256 240 246 110 296 60Z" fill="{PAPER}" stroke="{INK}" stroke-width="2.4"/>')
    s.add(f'<path d="M336 100C386 70 516 72 556 110C586 150 556 220 496 240C426 260 346 230 326 180C316 150 316 120 336 100Z" fill="url(#{uid}-h)" stroke="{RUST if on(3) else INK}" stroke-width="{3 if on(3) else 1.6}"/>')
    import random
    rnd = random.Random(7)
    for _ in range(70):
        x, y = rnd.uniform(320, 740), rnd.uniform(70, 310)
        if ((x - 520) / 230) ** 2 + ((y - 190) / 130) ** 2 < 1 and not (650 < x < 715 and 225 < y < 290):
            s.add(f'<circle cx="{x:.0f}" cy="{y:.0f}" r="4" fill="{RUST if on(2) else INK}"/>')
    s.add(f'<path d="M672 248l20 20M692 248l-20 20" stroke="{RUST}" stroke-width="4" stroke-linecap="round"/><circle cx="682" cy="258" r="22" fill="none" stroke="{RUST}" stroke-width="2"/>')
    s.ring(796, 30, 194, 300, at in (2, 3, 4))
    s.label(812, 70, "3 · " + st[2], "dots: states a test", "actually visited", on(2), anchor="start")
    s.label(812, 160, "4 · " + st[3], "shading: proven", "for the one property", on(3), anchor="start")
    s.label(812, 250, "5 · " + st[4], "the X: a bug that no", "test or proof reached", on(4), anchor="start")
    return s.finish(at, note, st[at] if at is not None else "", "A pass means no failure among the states that were checked.", 386)


def s_physical(uid, at=None, note=None):
    s, st, on = _start("physical-design-and-manufacturing", uid, at, "From connections to geometry: a netlist, cells placed in rows, wires routed between them, a timing path from one register to the next, and a mask for manufacture", 390)
    xs = [96, 330, 600, 0, 884]
    s.ring(10, 16, 172, 268, on(0))
    nodes = [(46, 50), (130, 40), (88, 110), (36, 170), (150, 150), (106, 196)]
    for a, b in [(0, 2), (1, 2), (2, 3), (2, 4), (4, 5), (3, 5)]:
        s.add(f'<path d="M{nodes[a][0]} {nodes[a][1]}L{nodes[b][0]} {nodes[b][1]}" stroke="{MUTE}" stroke-width="1.6"/>')
    for x, y in nodes:
        s.add(f'<rect x="{x - 10}" y="{y - 8}" width="20" height="16" fill="{SOFT}" stroke="{INK}" stroke-width="1.5"/>')
    s.label(xs[0], 240, "1 · " + st[0], "which parts connect", "", on(0))
    s.arrow("M184 120H210")
    s.ring(212, 16, 236, 268, on(1))
    for r in range(6):
        y = 30 + r * 32
        s.add(f'<path d="M226 {y + 28}h208" stroke="{LINE}" stroke-width="1"/>')
        x = 230
        for k in range(5):
            w = [24, 36, 18, 30, 26, 20][(r + k) % 6]
            if x + w > 432:
                break
            s.add(f'<rect x="{x}" y="{y + 4}" width="{w}" height="22" fill="{PEACH if (r, k) in ((1, 1), (4, 3)) else PAPER}" stroke="{INK}" stroke-width="1.3"/>')
            x += w + 12
    s.label(xs[1], 240, "2 · " + st[1], "where each cell sits", "", on(1))
    s.arrow("M450 120H476")
    s.ring(478, 16, 244, 268, on(2))
    s.add(f'<rect x="494" y="30" width="212" height="180" fill="{PAPER}" stroke="{INK}" stroke-width="1.6"/>')
    for d, c in [("M506 52H610V132H690", RUST), ("M516 190V96H676", INK), ("M536 42V202", MUTE), ("M576 202V160H696V70", INK), ("M500 116H570", MUTE)]:
        s.add(f'<path d="{d}" fill="none" stroke="{c}" stroke-width="3"/>')
    s.add(f'<rect x="592" y="122" width="34" height="34" fill="{RUST}" opacity=".25"/>')
    s.label(xs[2], 240, "3 · " + st[2], "room for every wire", "", on(2))
    s.ring(736, 16, 254, 268, on(4))
    s.add(f'<circle cx="864" cy="114" r="74" fill="{SOFT}" stroke="{INK}" stroke-width="2"/>')
    for i in range(-3, 4):
        for j in range(-3, 4):
            x, y = 864 + i * 20, 114 + j * 20
            if (x - 864) ** 2 + (y - 114) ** 2 < 60 ** 2:
                s.add(f'<rect x="{x - 8}" y="{y - 8}" width="16" height="16" fill="{PAPER if (i + j) % 5 else RUST}" stroke="{INK}" stroke-width=".8"/>')
    s.label(864, 240, "5 · " + st[4], "the same layout printed", "many times on a wafer", on(4))
    s.ring(10, 300, 980, 80, on(3))
    s.add(f'<rect x="36" y="316" width="40" height="46" fill="{SAND}" stroke="{INK}" stroke-width="2"/><rect x="520" y="316" width="40" height="46" fill="{SAND}" stroke="{INK}" stroke-width="2"/>')
    for k in range(4):
        x = 126 + k * 96
        s.add(f'<path d="M{x} 322v34l26-17z" fill="{PAPER}" stroke="{INK}" stroke-width="1.8"/>')
    s.add(f'<path d="M76 339H126M152 339H222M248 339H318M344 339H414M440 339H520" stroke="{RUST if on(3) else INK}" stroke-width="2.4"/>')
    s.label(590, 332, "4 · " + st[3], "a signal leaves one register and must reach", "the next before the clock ticks again", on(3), anchor="start")
    return s.finish(at, note, st[at] if at is not None else "")


def s_analog(uid, at=None, note=None):
    s, st, on = _start("analog-mixed-signal-and-emerging-devices", uid, at, "An analog crossbar: input voltages drive the rows, each device's conductance stores a weight, currents add down each column, noise and drift disturb them, and a converter reads the sums back as numbers", 420)
    x0, y0 = 260, 40
    s.ring(10, 20, 220, 250, on(0))
    for i in range(4):
        y = y0 + 20 + i * 50
        s.add(f'<path d="M140 {y}H{x0 + 3 * 90 + 40}" stroke="{INK}" stroke-width="2.4"/>')
        s.add(f'<circle cx="128" cy="{y}" r="13" fill="{PAPER}" stroke="{INK}" stroke-width="2"/><text x="128" y="{y + 5}" font-size="13" text-anchor="middle" fill="{INK}">V{i + 1}</text>')
    s.label(110, 300 - 64, "1 · " + st[0], "numbers go in", "as voltages", on(0))
    s.ring(240, 20, 356, 250, on(1))
    for j in range(4):
        x = x0 + 20 + j * 90
        s.add(f'<path d="M{x} {y0}V{y0 + 236}" stroke="{INK}" stroke-width="2.4"/>')
        for i in range(4):
            y = y0 + 20 + i * 50
            g = (i * 3 + j * 5) % 4
            s.add(f'<rect x="{x - 20}" y="{y - 10}" width="22" height="20" rx="3" fill="{[PAPER, SOFT, PEACH, TAN][g]}" stroke="{INK}" stroke-width="1.4" transform="rotate(-45 {x - 9} {y})"/>')
        s.arrow(f"M{x} {y0 + 236}V{y0 + 262}", rust=True, width=2.4)
        s.add(f'<path d="M{x - 18} {y0 + 268}h36l-18 26z" fill="{SAND}" stroke="{RUST if on(4) else INK}" stroke-width="{2.4 if on(4) else 1.6}"/>')
    s.ring(240, 300, 356, 42, on(4))
    s.label(418, 362, "5 · " + st[4], "reads each column's sum back as a number", "", on(4))
    s.ring(608, 20, 176, 250, on(2))
    s.text(696, 100, "I = Σ V·G", 22, INK, "middle", serif=True, italic=True)
    s.text(696, 126, "for each column", 15, MUTE, "middle")
    s.label(696, 196, "3 · " + st[2], "the wire does", "the adding", on(2))
    s.ring(796, 20, 194, 250, on(3))
    s.add(f'<path d="M812 100c12-20 20 20 32 0s20 20 32 0 20 20 32 0 20 20 32 0" fill="none" stroke="{RUST}" stroke-width="2.4"/>'
          f'<path d="M812 140c20 6 60 12 160 30" fill="none" stroke="{MUTE}" stroke-width="2" stroke-dasharray="5 5"/>')
    s.label(893, 216, "4 · " + st[3], "heat, variation", "and ageing blur it", on(3))
    return s.finish(at, note, st[at] if at is not None else "", "Physics does the sums; its noise sets the accuracy.", 410)


def s_method(uid, at=None, note=None):
    s, st, on = _start("design-methodology-and-tooling", uid, at, "A design rewritten through a graph: a written description becomes a graph of operations, a tool rewrites the graph, a check confirms it computes the same thing, and only then is the cost compared", 320)
    xs = [100, 300, 500, 700, 900]
    s.ring(10, 16, 180, 268, on(0))
    s.add(f'<rect x="22" y="36" width="156" height="150" rx="6" fill="{ESP}"/>')
    for k, line in enumerate(["for i in 0..n:", "  y += a[i]*b[i]", "out = y"]):
        s.add(f'<text x="34" y="{70 + k * 30}" font-size="16" fill="#f3ede2">{esc(line)}</text>')
    s.label(xs[0], 236, "1 · " + st[0], "code a person writes", "", on(0))

    def graph(x, merged=False):
        pts = {"a": (x - 35, 46), "b": (x + 35, 46), "m": (x - 35, 112), "m2": (x + 35, 112), "+": (x, 178)}
        edges = [("a", "m"), ("b", "m"), ("m", "+")] + ([] if merged else [("a", "m2"), ("b", "m2"), ("m2", "+")])
        if merged:
            s.add(f'<path d="M{pts["m"][0] + 14} {pts["m"][1] + 12}C{x + 30} {pts["m"][1] + 20} {x + 26} {pts["+"][1] - 30} {x + 12} {pts["+"][1] - 14}" fill="none" stroke="{MUTE}" stroke-width="1.6"/>')
        for p, q in edges:
            s.add(f'<path d="M{pts[p][0]} {pts[p][1]}L{pts[q][0]} {pts[q][1]}" stroke="{MUTE}" stroke-width="1.6"/>')
        for k, (px, py) in pts.items():
            if merged and k == "m2":
                continue
            lab = {"a": "a", "b": "b", "m": "×", "m2": "×", "+": "+"}[k]
            s.add(f'<circle cx="{px}" cy="{py}" r="18" fill="{PEACH if merged and k == "m" else SOFT}" stroke="{INK}" stroke-width="1.6"/><text x="{px}" y="{py + 6}" font-size="17" text-anchor="middle" fill="{INK}">{lab}</text>')
    for i in range(4):
        s.arrow(f"M{xs[i] + 82} 110H{xs[i + 1] - 82}")
    s.ring(210, 16, 180, 268, on(1))
    graph(xs[1])
    s.label(xs[1], 236, "2 · " + st[1], "operations and their order", "", on(1))
    s.ring(410, 16, 180, 268, on(2))
    graph(xs[2], merged=True)
    s.label(xs[2], 236, "3 · " + st[2], "one multiplier, used twice", "", on(2))
    s.ring(610, 16, 180, 268, on(3))
    s.add(f'<path d="M660 90h80M660 112h80" stroke="{INK}" stroke-width="5"/><text x="700" y="160" font-size="16" text-anchor="middle" fill="{INK}">still equal?</text>')
    s.label(xs[3], 236, "4 · " + st[3], "checked, not assumed", "", on(3))
    s.ring(810, 16, 180, 268, on(4))
    for k, (h, c) in enumerate([(100, TAN), (66, RUST)]):
        s.add(f'<rect x="{864 + k * 44}" y="{180 - h}" width="30" height="{h}" fill="{c}"/>')
    s.add(f'<path d="M850 180h100" stroke="{INK}" stroke-width="2"/>')
    s.text(900, 202, "before · after", 14, MUTE, "middle")
    s.label(xs[4], 236, "5 · " + st[4], "area, time, power", "", on(4))
    return s.finish(at, note, st[at] if at is not None else "", "A tool can only change what the written form lets it see.", 312)


def s_package(uid, at=None, note=None):
    s, st, on = _start("chiplets-3d-and-packaging", uid, at, "A package cut open: two compute dies and a memory stack sit on a thin wiring layer, short links join them, the memory dies are stacked with vertical wires, heat flows up into a heat sink, and the package joins the board", 330)
    s.add(f'<rect x="100" y="40" width="520" height="34" fill="{SAND}" stroke="{INK}" stroke-width="2"/>' + "".join(f'<rect x="{112 + k * 42}" y="14" width="18" height="28" fill="{SAND}" stroke="{INK}" stroke-width="1.4"/>' for k in range(12)))
    for k in range(4):
        s.arrow(f"M{170 + k * 100} 120V84", rust=True, width=2.2)
    for x in (120, 320):
        s.add(f'<rect x="{x}" y="126" width="170" height="54" fill="{PEACH}" stroke="{INK}" stroke-width="2"/><text x="{x + 85}" y="159" font-size="15" text-anchor="middle" fill="{INK}">compute die</text>')
    for k in range(4):
        s.add(f'<rect x="520" y="{102 + k * 20}" width="92" height="18" fill="{SAND if k % 2 else PAPER}" stroke="{INK}" stroke-width="1.6"/>')
    for x in (538, 566, 594):
        s.add(f'<path d="M{x} 104V180" stroke="{RUST if on(2) else INK}" stroke-width="2.4"/>')
    for k in range(22):
        s.add(f'<circle cx="{126 + k * 22}" cy="186" r="5" fill="{INK}"/>')
    s.add(f'<rect x="100" y="192" width="540" height="30" fill="{SOFT}" stroke="{INK}" stroke-width="2"/>')
    s.add(f'<path d="M270 204H340M470 210H540" stroke="{RUST if on(1) else INK}" stroke-width="3"/>')
    s.add(f'<rect x="60" y="226" width="620" height="34" fill="{SAND}" stroke="{INK}" stroke-width="2"/>')
    for k in range(18):
        s.add(f'<circle cx="{90 + k * 33}" cy="270" r="8" fill="{PAPER}" stroke="{INK}" stroke-width="1.6"/>')
    s.add(f'<path d="M20 282H700" stroke="{INK}" stroke-width="4"/>')
    s.ring(110, 116, 390, 72, on(0)).ring(260, 194, 290, 26, on(1)).ring(510, 94, 112, 92, on(2)).ring(90, 6, 540, 76, on(3)).ring(50, 222, 640, 62, on(4))
    rows = [(3, 34, 50), (2, 92, 140), (0, 150, 150), (1, 208, 207), (4, 266, 255)]
    for i, y, ty in rows:
        s.add(f'<path d="M{[500, 550, 620, 630, 690][i]} {ty}H{744}" stroke="{MUTE}" stroke-width="1" stroke-dasharray="3 4"/>')
        a, b = [("1 · " + st[0], "small dies are cheaper to make"), ("2 · " + st[1], "slower than wires on one die"), ("3 · " + st[2], "vertical wires through the stack"),
                ("4 · " + st[3], "heat must escape upward"), ("5 · " + st[4], "joins it all to the board")][i]
        s.text(752, y, a.upper(), 15, RUST if on(i) else INK, "start", 600, spacing=1)
        s.text(752, y + 19, b, 14, MUTE)
    return s.finish(at, note, st[at] if at is not None else "", "Splitting a chip trades making cost for links and heat.", 318)



SCENE = {"architecture-and-accelerators": s_accel, "memory-interconnect-and-storage": s_memory, "power-reliability-and-security": s_protect,
         "systems-applications-and-workloads": s_systems, "ai-assisted-eda": s_aieda, "verification-and-validation": s_verify,
         "physical-design-and-manufacturing": s_physical, "analog-mixed-signal-and-emerging-devices": s_analog,
         "design-methodology-and-tooling": s_method, "chiplets-3d-and-packaging": s_package}


# ------------------------------------------------------------------------------------------- where each subtheme acts
# subtheme id: (part of its theme's scene, two plain lines about what its papers change there). Words ours,
# from each subtheme's report in reports/observed-subthemes/.
SUBNOTE = {
    # architecture and accelerators
    "specialized-accelerators-and-dataflow": (3, "Papers choose the order in which numbers flow through the grid,", "so each unit is fed and fewer numbers make the trip twice."),
    "approximate-and-precision-aware-compute": (3, "Papers use fewer bits per number, or allow small errors,", "and must show the final answer stays good enough."),
    "architecture-software-co-design": (0, "Papers change the program and the hardware together,", "so each is shaped to fit what the other can do well."),
    "sparse-and-irregular-compute": (0, "Many numbers in these workloads are zero or scattered.", "Papers skip the zeros without stalling on the scattered rest."),
    "quantum-architectures-and-control": (4, "A quantum answer also needs ordinary computing to steer and read it.", "Papers count the time for the whole answer, not just the gates."),
    "specialized-ai-accelerators": (3, "Chips built for one family of AI models.", "Papers trade generality for speed on that family."),
    "ai-accelerator-microarchitecture": (2, "Papers redesign the buffers and units inside an AI chip,", "so data waits less between steps."),
    "memory-and-data-movement": (1, "Papers cut trips to off-chip memory,", "which often cost more than the arithmetic itself."),
    "emerging-and-nonvon-neumann-compute": (3, "Papers compute where the data is stored,", "instead of shipping it to separate compute units."),
    "distributed-and-wafer-scale-inference": (1, "One model spread across many chips, or one wafer-sized chip.", "The cost is in passing numbers between the pieces."),
    "edge-ai-and-deployment": (4, "Papers fit AI models onto small, battery-powered devices,", "where energy and memory set the limits."),
    "neuromorphic-and-emerging-architectures": (3, "Hardware that works in spikes, loosely like neurons.", "It saves energy only if the task suits spikes."),
    # memory, interconnect and storage
    "data-movement-and-locality": (0, "Papers keep the numbers that are reused close to the core,", "so fewer trips go down the ladder."),
    "memory-hierarchy-and-persistence": (1, "Papers change how memory levels share data, and how data", "survives a power cut without slowing everything down."),
    "storage-and-data-movement": (2, "Papers speed up the slowest rung, storage,", "or do some work inside the storage device."),
    "memory-compute-and-reliability": (4, "Papers put logic inside memory and ask", "whether the results stay correct as memory cells fail."),
    "processing-in-memory-and-memory-centric-compute": (4, "Papers send the work to the memory chip,", "so large data does not travel to the processor."),
    "storage-and-memory-systems": (2, "Papers redesign how a system stores and finds data,", "and measure the whole system, not one part."),
    "chiplet-and-on-chip-interconnect": (3, "Papers design the wires and switches between chips or blocks,", "where distance and traffic set the delay."),
    "interconnect-and-networking": (3, "Papers change the network that joins processors,", "so messages wait less when many share a path."),
    # power, reliability and security
    "side-channel-and-hardware-security": (1, "Papers find or block leaks through power, timing or shared parts,", "and must say what the attacker can do."),
    "hardware-and-system-security": (2, "Papers add hardware that keeps programs and data apart,", "and must count what that separation costs."),
    "accelerator-reliability": (0, "Papers find which flipped bits in an AI chip change its answer,", "and protect only those, to save cost."),
    "reliable-and-secure-ml": (0, "Papers ask whether an AI model on hardware still answers", "correctly when bits flip or someone tampers."),
    "secure-and-robust-ml": (1, "Papers defend AI hardware against an attacker", "who changes inputs or stored weights."),
    "thermal-and-reliability-modeling": (3, "Papers predict hot spots and wear before the chip is built,", "fast enough to steer early design choices."),
    "privacy-preserving-compute": (2, "Papers compute on data that stays scrambled the whole time.", "The protection is strong; the slowdown is large."),
    "privacy-preserving-computing": (2, "Papers speed up computing on scrambled data,", "so privacy costs less time and energy."),
    "energy-and-thermal-efficiency": (3, "Papers cut energy and heat by changing", "when and how fast each part runs."),
    "reliability-and-fault-tolerance": (0, "Papers keep a system running through faults,", "by detecting them and recovering."),
    "fault-tolerance-and-reliability": (0, "Papers name the faults they handle,", "then show recovery with its cost."),
    "power-integrity-and-reliability": (3, "Papers check that the supply voltage stays steady", "when many parts switch at once."),
    "reliable-and-efficient-compute": (4, "Papers ask how little protection is enough,", "so reliability does not cost more than it saves."),
    "reliable-and-secure-ai-systems": (2, "Papers protect a whole AI system,", "not just one chip, against faults and attacks."),
    "reliable-and-secure-compute": (2, "Papers combine fault and attack protection", "in one design and count the joint cost."),
    # systems, applications and workloads
    "llm-systems-and-runtime": (1, "Papers decide how large language model requests share chips", "and memory, to keep slow replies rare."),
    "multimedia-and-edge-systems": (3, "Papers run video, image and sound work on small devices,", "where each frame has a deadline."),
    "distributed-and-disaggregated-systems": (2, "Papers spread work and memory across many machines,", "and pay for every message between them."),
    "robotics-and-edge-ai": (3, "A robot must sense, decide and move in time.", "Papers fit that loop onto on-board chips."),
    "edge-embedded-and-mobile-systems": (3, "Papers fit work onto phones and small boards,", "where battery and heat are the limits."),
    "datacenter-and-cloud-systems": (2, "Papers make many shared servers do more useful work,", "for the same power and the same deadlines."),
    "embedded-and-edge-systems": (3, "Papers design small computers built into products,", "with tight limits on cost and energy."),
    "real-time-and-networked-systems": (4, "Here a late answer is a wrong answer.", "Papers prove or test that deadlines hold."),
    "biochips-and-specialized-systems": (3, "Chips that handle fluids or biology,", "designed with the same tools as electronics."),
    "bioinformatics-and-scientific-computing": (2, "Papers speed up science workloads, such as reading DNA,", "on special hardware."),
    "confidential-and-trusted-computing": (2, "Papers keep data hidden even from the server's owner,", "and count the slowdown that causes."),
    "scientific-and-engineering-computing": (2, "Papers speed up physics and engineering simulations,", "which run for hours on large machines."),
    "signal-processing-and-sensing": (3, "Papers process sensor signals near the sensor,", "so less raw data has to travel."),
    # AI-assisted EDA
    "learned-design-space-exploration": (1, "A model learns which settings tend to work,", "so fewer slow simulations are needed to find a good design."),
    "learned-eda-and-optimization": (1, "Learned models replace slow steps inside design tools,", "and must match the slow tool's answer."),
    "llm-assisted-design-flows": (1, "A language model writes hardware code or tool scripts.", "Only compilers and simulators decide if it works."),
    "generative-design-and-synthesis": (1, "A model generates circuits or layouts directly.", "Each one still has to pass the same checks."),
    "generative-design-automation": (1, "A model drafts whole design steps.", "Papers ask how often the drafts pass, and at what cost."),
    "graph-learning-for-eda": (1, "Circuits are graphs of parts and wires.", "Models that read graphs predict delay, power or layout."),
    "architecture-modeling-and-exploration": (1, "A model predicts how a processor design will perform,", "so the search tries fewer designs in slow simulation."),
    "verification-and-debugging-tools": (3, "Papers turn a failed check into a pointer", "to the line that caused it."),
    # verification and validation
    "simulation-emulation-and-testing": (2, "Papers run more of the design's behaviour faster,", "on simulators or special hardware, to visit more states."),
    "formal-analysis-and-verification": (3, "Papers prove a property for every input,", "and must keep the proof small enough to finish."),
    "formal-and-functional-verification": (3, "Papers mix proofs with tests,", "covering more states than either alone."),
    "formal-and-equivalence-verification": (3, "Papers prove that two versions of a design", "compute exactly the same thing."),
    "hardware-security-validation": (4, "Papers search for security bugs:", "paths that leak or change data where they should not."),
    "processor-and-rtl-verification": (1, "Papers check processor designs written as code,", "where one wrong line can break every program."),
    "simulation-and-emulation": (2, "Papers make simulation faster,", "so tests reach more states in the same time."),
    "emulation-and-prototyping": (2, "Papers run the design on reprogrammable chips,", "fast enough to boot real software."),
    "physical-verification": (4, "Papers check the final layout against", "the factory's rules before it is made."),
    # physical design and manufacturing
    "placement-routing-and-floorplanning": (1, "Papers decide where blocks and cells go,", "so wires are short and still fit."),
    "process-aware-design": (4, "Papers design with the factory's limits in view,", "so the printed chip matches the drawing."),
    "placement-routing-and-timing": (3, "Papers place and wire with timing in mind,", "so signals arrive before the next clock tick."),
    "manufacturing-and-yield": (4, "Papers raise the share of chips that work", "after they are made."),
    "manufacturing-and-lithography": (4, "Papers fix shapes that print wrongly,", "because the features are smaller than the light used."),
    "partitioning-and-placement": (1, "Papers split a design into parts,", "then place each part to keep links short."),
    "physical-design-and-routing": (2, "Papers find room for every wire", "without breaking spacing rules."),
    "timing-analysis-and-optimization": (3, "Papers compute signal delay faster or more exactly,", "and fix the paths that are too slow."),
    "cell-and-circuit-design": (0, "Papers redesign the small building blocks,", "the cells every larger design is made of."),
    "device-and-process-modeling": (4, "Papers model how transistors behave once made,", "so designs can be checked before making them."),
    "fpga-and-reconfigurable-design": (1, "Papers place and wire designs on reprogrammable chips,", "whose grid of parts is fixed in advance."),
    "manufacturing-monitoring-and-yield": (4, "Papers watch the factory's measurements", "to catch failing chips early."),
    "parasitic-extraction-and-modeling": (2, "Wires add unwanted resistance and capacitance.", "Papers estimate these from the layout, faster."),
    # analog, mixed-signal and emerging devices
    "neuromorphic-quantum-and-non-von-neumann": (1, "Papers compute with new devices: spikes, qubits or light,", "where the device's physics does the work."),
    "analog-compute-in-memory": (2, "Papers let currents do the multiply-and-add inside memory,", "and must keep noise from ruining the answer."),
    "photonic-and-optical-compute": (2, "Papers compute with light instead of current,", "and pay to convert between the two."),
    "quantum-hardware-and-control": (3, "Qubits lose their state quickly.", "Papers design the control that fights that loss."),
    "analog-layout-and-circuit-automation": (1, "Papers automate the drawing of analog circuits,", "where small layout changes shift behaviour."),
    "analog-and-mixed-signal-design": (4, "Papers design circuits where analog meets digital,", "such as the converters that read results."),
    "analog-calibration-and-modeling": (3, "Papers measure and correct drift and variation,", "so analog results stay accurate."),
    "device-modeling-and-simulation": (1, "Papers model new devices so designers can", "simulate them before they exist."),
    "emerging-device-design": (1, "Papers design circuits around new devices,", "and show where the device's limits bite."),
    "emerging-memory-and-devices": (1, "Papers use new memory devices that keep data without power,", "and check how long they last."),
    "analog-and-mixed-signal-synthesis": (1, "Papers generate analog circuit sizes from a goal,", "a task done by hand for decades."),
    "analog-circuit-learning": (1, "A model learns how analog circuits behave,", "to search sizes faster than simulation."),
    "analog-circuit-optimization": (1, "Papers search transistor sizes to meet a goal", "with as few slow simulations as possible."),
    "rf-and-mixed-signal-design": (4, "Papers design radio-frequency circuits,", "where wires and parts behave like antennas."),
    # design methodology and tooling
    "optimization-and-search-methods": (4, "Papers improve the search a tool runs,", "and compare at the same time budget."),
    "graph-and-hypergraph-optimization": (1, "Papers cut or group a design's graph,", "the step under partitioning and placement."),
    "logic-synthesis-and-optimization": (2, "Papers rewrite logic into fewer or faster gates,", "and check it still computes the same thing."),
    "compiler-and-runtime-optimization": (2, "Papers change how programs are translated for hardware,", "so the same hardware does more."),
    "high-level-synthesis-and-compilers": (0, "Papers turn ordinary code into hardware,", "and the way the code is written shapes the result."),
    "synthesis-and-compilation": (2, "Papers translate designs from one form to the next", "while keeping their meaning."),
    "compilation-and-mapping": (2, "Papers map a computation onto fixed hardware,", "choosing which unit does which step."),
    "cross-layer-design-automation": (4, "Papers optimise several design steps together,", "instead of one step at a time."),
    "hardware-generation-and-compilation": (0, "Papers generate hardware from short descriptions,", "so a design can be changed and rebuilt quickly."),
    "power-and-thermal-design": (4, "Papers add power and heat to the cost estimate", "early, while choices are still cheap."),
    "reproducibility-artifacts-and-benchmarks": (3, "Papers release tools and test sets", "so others can check the results."),
    "simulation-and-numerical-methods": (4, "Papers speed up the numerical solvers", "that tools use to estimate costs."),
    # chiplets, 3D and packaging
    "3d-stacking-and-thermal-management": (3, "Stacked dies trap heat in the middle.", "Papers predict temperature and steer work away from hot spots."),
    "3d-integration-and-thermal-management": (2, "Papers decide which circuits go on which layer,", "and where wires cross between layers."),
    "chiplet-system-architecture": (0, "Papers decide how to split a system into dies,", "and what each die should hold."),
    "advanced-packaging-and-interconnect": (1, "Papers design the dense wiring layer", "that joins dies inside the package."),
    "chiplet-interconnects": (1, "Papers make links between dies faster and cheaper,", "since every crossing costs energy."),
    "wafer-scale-and-heterogeneous-integration": (4, "Papers join very different dies, or a whole wafer,", "into one system."),
    "chiplet-partitioning-and-integration": (0, "Papers choose where to cut a design into dies,", "so few signals must cross a cut."),
    "chiplets-and-heterogeneous-integration": (0, "Papers combine dies made in different factories", "or processes in one package."),
    "package-system-co-design": (4, "Papers design the chip and its package together,", "since each limits the other."),
}

# deep reads: file stem -> (theme, part, two lines on what the paper does, what reading the full source found)
DEEP = {
    "atb": ("architecture-and-accelerators", 3, ("Speeds up a matrix step on an AI chip.", "The full paper's Table 2 labels 24.3 ÷ 4.8 as 4.54×; the division gives 5.06."), "preprint"),
    "cannon": ("memory-interconnect-and-storage", 4, ("Puts search logic next to memory on a chip-to-chip link.", "Only the program description and a lab entry were found."), "description"),
    "ctxmem": ("memory-interconnect-and-storage", 3, ("Uses memory joined over a chip-to-chip link.", "Results come from simulation, not a built device."), "description"),
    "exact-t": ("design-methodology-and-tooling", 2, ("Builds quantum circuits from a library of exact pieces.", "The preprint and the description report the metric differently."), "preprint"),
    "flash3d": ("chiplets-3d-and-packaging", 3, ("A fast solver for heat in stacked chips.", "About 2,000 slices fit in one rival model's run time; error size is not given."), "description"),
    "fusedot": ("architecture-and-accelerators", 3, ("Groups repeated multiplications by the same weight.", "No full paper or code was found in the search."), "description"),
    "gemir": ("power-reliability-and-security", 3, ("Predicts voltage drop and wire wear in the power grid together.", "No full paper found, so its reductions stay unconfirmed."), "description"),
    "hlsarchopt": ("design-methodology-and-tooling", 0, ("Tunes code that is turned into hardware.", "The released files hold one example, not the whole method."), "code"),
    "hybrimoe": ("systems-applications-and-workloads", 3, ("Runs a mixture-of-experts model across a CPU and a GPU.", "The preprint gives the hardware, models and cache sizes."), "preprint"),
    "hyper-cim": ("analog-mixed-signal-and-emerging-devices", 1, ("Searches designs for compute-in-memory chips.", "Five macros are reported, not fabrication of every design."), "description"),
    "mappingevolve": ("design-methodology-and-tooling", 2, ("Evolves the rules that map logic to gates.", "It trades one cost for another; it does not win everywhere."), "preprint"),
    "notsotiny": ("ai-assisted-eda", 2, ("A test set for models that write hardware code.", "On timeout the script marks a pass and 100% coverage."), "preprint"),
    "paretopilot": ("ai-assisted-eda", 3, ("Searches settings for code-to-hardware tools.", "The released code samples once; it does not learn from results."), "code"),
    "raf": ("architecture-and-accelerators", 1, ("Removes remote memory accesses on a multi-chip system.", "No remote access does not mean no data movement."), "description"),
    "strix": ("power-reliability-and-security", 2, ("Rethinks fault handling for AI chips at the system level.", "Detecting fast is not the same as correcting in time."), "preprint"),
    "xsearch": ("ai-assisted-eda", 1, ("Searches processor designs with cheap and costly simulators.", "The description reports no numbers or baselines."), "description"),
}


# ------------------------------------------------------------------------------------------- the six directions

def d_sieve(uid):
    """Constraints become executable: candidates fall through checks; rejects carry their reason back to the proposer."""
    s = Svg(uid, "Candidate designs fall through three checks in turn: does it compile, does it behave correctly in simulation, does it meet timing. Rejects slide off with the reason, and the reason goes back to the proposer.", 1000, 470)
    s.add(f'<rect x="60" y="20" width="200" height="70" rx="8" fill="{ESP}"/>')
    s.text(160, 50, "PROPOSER", 15, PEACH, "middle", 600, spacing=1.5).text(160, 74, "a model or a search", 16, "#f3ede2", "middle")
    for k in range(6):
        s.add(f'<rect x="{100 + k * 22}" y="104" width="14" height="14" fill="{PEACH}" stroke="{INK}" stroke-width="1.2"/>')
    meshes = [("1 · Compiles?", "the code is legal hardware", 4), ("2 · Behaves correctly?", "simulation matches the rule", 2), ("3 · Meets timing?", "fast enough for the clock", 1)]
    for i, (h, sub, keep) in enumerate(meshes):
        y = 150 + i * 96
        s.add(f'<path d="M40 {y}H360" stroke="{INK}" stroke-width="3"/>' + "".join(f'<path d="M{50 + j * 20} {y - 6}V{y + 6}" stroke="{INK}" stroke-width="1.4"/>' for j in range(16)))
        s.text(390, y - 4, h.upper(), 16, INK, "start", 600, spacing=1).text(390, y + 18, sub, 15, MUTE)
        for k in range(keep):
            s.add(f'<rect x="{150 + k * 22}" y="{y + 16}" width="14" height="14" fill="{PEACH}" stroke="{INK}" stroke-width="1.2"/>')
        s.add(f'<rect x="640" y="{y - 14}" width="14" height="14" fill="{PAPER}" stroke="{RUST}" stroke-width="1.6"/><path d="M364 {y - 4}C480 {y - 4} 560 {y - 8} 632 {y - 8}" fill="none" stroke="{RUST}" stroke-width="1.6" stroke-dasharray="4 4"/>')
        s.text(664, y - 2, ["“syntax error, line 12”", "“output wrong at step 40”", "“path too slow by a margin”"][i], 16, RUST, "start", italic=True, serif=True)
    s.add(f'<rect x="120" y="436" width="110" height="26" rx="4" fill="{PEACH}" stroke="{INK}" stroke-width="1.6"/>')
    s.text(240, 455, "accepted: passed every check", 16, INK, "start", 600)
    s.arrow("M860 400C960 300 960 60 270 56", rust=True, dash=True, width=2.4)
    s.text(830, 430, "the reason steers the next try", 17, RUST, "middle", italic=True, serif=True)
    s.text(830, 452, "(words in quotes are made-up examples)", 14, MUTE, "middle")
    return s.done()


def d_move(uid):
    """Data movement as the real cost: the same job with data sent to compute, then compute sent to data."""
    s = Svg(uid, "Two ways to run the same job. Left: every number travels from memory to a distant processor and back. Right: a small unit inside memory does the simple steps, and only the short result travels.", 1000, 380)
    for side, x0 in (("left", 20), ("right", 520)):
        near = side == "right"
        s.add(f'<rect x="{x0}" y="20" width="460" height="300" rx="10" fill="{PAPER}" stroke="{LINE}" stroke-width="1.6"/>')
        s.text(x0 + 20, 50, ("Send the data to the work" if not near else "Send the work to the data").upper(), 16, RUST if near else INK, "start", 600, spacing=1)
        _chip(s, x0 + 30, 90, 150, 110, "", pins=False, fill=SAND)
        for r in range(3):
            for c in range(4):
                s.add(f'<rect x="{x0 + 44 + c * 32}" y="{102 + r * 28}" width="24" height="20" fill="{PAPER}" stroke="{INK}"/>')
        s.text(x0 + 105, 224, "memory", 16, INK, "middle")
        _chip(s, x0 + 300, 110, 120, 80, "processor", pins=True)
        if not near:
            for k in range(7):
                s.add(f'<rect x="{x0 + 196 + k * 14}" y="{128 + (k % 2) * 30}" width="10" height="10" fill="{PEACH}" stroke="{INK}"/>')
            s.arrow(f"M{x0 + 186} 146H{x0 + 296}", width=3).arrow(f"M{x0 + 296} 176H{x0 + 186}", width=3)
            s.text(x0 + 230, 270, "many numbers make the long trip, twice", 16, MUTE, "middle")
        else:
            s.add(f'<rect x="{x0 + 46}" y="186" width="118" height="22" rx="3" fill="{PEACH}" stroke="{RUST}" stroke-width="2"/><text x="{x0 + 105}" y="202" font-size="13" text-anchor="middle" fill="{INK}">small unit inside</text>')
            s.add(f'<rect x="{x0 + 236}" y="141" width="10" height="10" fill="{RUST}"/>')
            s.arrow(f"M{x0 + 186} 146H{x0 + 296}", rust=True, width=3)
            s.text(x0 + 230, 270, "only the short result travels", 16, MUTE, "middle")
    s.text(500, 360, "The test: time and energy for the whole job, with every copy counted.", 18, RUST, "middle", italic=True, serif=True)
    return s.done()


def d_wheel(uid):
    """Closed-loop design: measure, learn, decide, recheck, around a meter of simulations spent."""
    s = Svg(uid, "A wheel of four steps around a meter: measure a few designs, learn a fast predictor, decide which design to try next, recheck the winner accurately. The meter in the middle counts every simulation spent.", 1000, 480)
    cx, cy, r = 500, 230, 150
    steps = [("1 · Measure", "simulate a few designs", -90), ("2 · Learn", "fit a fast predictor", 0), ("3 · Decide", "pick the next design", 90), ("4 · Recheck", "confirm the winner", 180)]
    s.add(f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="{TAN}" stroke-width="14"/>')
    for i, (h, sub, a) in enumerate(steps):
        ang = math.radians(a)
        x, y = cx + r * math.cos(ang), cy + r * math.sin(ang)
        s.add(f'<circle cx="{x:.0f}" cy="{y:.0f}" r="30" fill="{PEACH if i != 3 else PAPER}" stroke="{RUST if i == 3 else INK}" stroke-width="2.4"/><text x="{x:.0f}" y="{y + 7:.0f}" font-size="20" text-anchor="middle" fill="{INK}" font-weight="600">{i + 1}</text>')
        tx = x + (0 if a in (-90, 90) else (50 if a == 0 else -50))
        ty = y + (-60 if a == -90 else 56 if a == 90 else -6)
        anc = "middle" if a in (-90, 90) else ("start" if a == 0 else "end")
        s.text(tx, ty, h.upper(), 16, INK, anc, 600, spacing=1).text(tx, ty + 20, sub, 15, MUTE, anc)
    for a in (-45, 45, 135, 225):
        ang = math.radians(a)
        x, y = cx + r * math.cos(ang), cy + r * math.sin(ang)
        s.add(f'<path d="M{x:.0f} {y:.0f}l{-10 * math.sin(ang):.1f} {10 * math.cos(ang):.1f}" stroke="{INK}" stroke-width="3" marker-end="url(#{uid}-a)"/>')
    s.add(f'<path d="M{cx - 60} {cy + 30}A60 60 0 0 1 {cx + 60} {cy + 30}" fill="none" stroke="{INK}" stroke-width="10"/><path d="M{cx - 60} {cy + 30}A60 60 0 0 1 {cx + 30} {cy - 22}" fill="none" stroke="{RUST}" stroke-width="10"/>'
          f'<path d="M{cx} {cy + 30}L{cx + 30} {cy - 14}" stroke="{INK}" stroke-width="3"/><circle cx="{cx}" cy="{cy + 30}" r="6" fill="{INK}"/>')
    s.text(cx, cy + 60, "simulations spent", 15, MUTE, "middle")
    s.text(cx, 466, "A fair claim counts every simulation, including the recheck.", 18, RUST, "middle", italic=True, serif=True)
    return s.done()


def d_shift(uid):
    """Reliability and security upstream: the threat named at the start, not checked at the end."""
    s = Svg(uid, "Two timelines of the same design steps, from requirement to chip. Top: the fault or attack is checked only at the end, when fixing it means redoing steps. Bottom: it is named in the requirement and shapes every step, with its cost shown.", 1000, 360)
    steps = ["Requirement", "Architecture", "Hardware code", "Layout", "Chip"]
    for lane, y in (("old", 90), ("new", 240)):
        s.text(20, y - 50, ("Checked at the end" if lane == "old" else "Named at the start").upper(), 16, RUST if lane == "new" else INK, "start", 600, spacing=1)
        s.add(f'<path d="M40 {y}H960" stroke="{INK}" stroke-width="2.4"/>')
        for i, st in enumerate(steps):
            x = 90 + i * 200
            s.add(f'<circle cx="{x}" cy="{y}" r="12" fill="{PAPER}" stroke="{INK}" stroke-width="2"/>')
            s.text(x, y + 34, st, 15, INK, "middle")
        shield_x = 890 if lane == "old" else 90
        s.add(f'<path d="M{shield_x} {y - 40}l22 8v14c0 14-10 22-22 28-12-6-22-14-22-28v-14z" fill="{PEACH}" stroke="{RUST}" stroke-width="2"/>')
        if lane == "old":
            s.arrow(f"M870 {y - 26}C700 {y - 60} 400 {y - 60} 300 {y - 20}", rust=True, dash=True)
            s.text(600, y - 54, "a late finding sends work back", 15, RUST, "middle", italic=True, serif=True)
        else:
            s.add(f'<path d="M112 {y - 14}H880" stroke="{RUST}" stroke-width="5" opacity=".35"/>')
            s.text(500, y - 22, "the threat model shapes every step; its cost is reported", 15, RUST, "middle", italic=True, serif=True)
    s.text(500, 344, "Protection always costs something. The useful number is correct work done with protection on.", 17, MUTE, "middle")
    return s.done()


def d_heat(uid):
    """Physical reality in the loop: a coarse fast heat estimate steers early choices; a fine accurate check confirms."""
    s = Svg(uid, "Two heat maps of the same chip floorplan. Left: a coarse, fast estimate used while choosing where blocks go. Right: a fine, slow and accurate check of the final layout. The hot corner agrees; the detail differs.", 1000, 400)
    import random
    rnd = random.Random(3)
    def heat(x, y): return max(0.0, 1 - math.hypot(x - 0.75, y - 0.3) * 1.6) + 0.15 * rnd.random()
    cols = [PAPER, SOFT, PEACH, TAN, RUST]
    for panel, x0, n in (("Fast estimate", 40, 6), ("Accurate check", 540, 18)):
        cell = 300 / n
        for i in range(n):
            for j in range(n):
                v = heat((j + .5) / n, (i + .5) / n)
                c = cols[min(4, int(v * 4.2))]
                s.add(f'<rect x="{x0 + j * cell:.1f}" y="{50 + i * cell:.1f}" width="{cell + .3:.1f}" height="{cell + .3:.1f}" fill="{c}"/>')
        s.add(f'<rect x="{x0}" y="50" width="300" height="300" fill="none" stroke="{INK}" stroke-width="2"/>')
        s.text(x0, 34, panel.upper(), 16, INK, "start", 600, spacing=1)
        s.text(x0 + 314, 80, "seconds, coarse" if n == 6 else "hours, fine", 15, MUTE)
        s.text(x0 + 314, 100, "used while choosing" if n == 6 else "used to confirm", 15, MUTE)
    s.arrow("M380 200H530", rust=True, width=3)
    s.text(455, 190, "then", 15, RUST, "middle")
    s.text(500, 386, "Shading: cream is cool, rust is hot. The drawing is an illustration, not a measured chip.", 15, MUTE, "middle")
    return s.done()


def d_bench(uid):
    """Evaluation as research: a score is a task set, a rule for success, a version and a spread."""
    s = Svg(uid, "A benchmark card: a set of tasks, a scoring rule with its version, a result shown with its spread across runs, and a column for an independent repeat that is still empty.", 1000, 380)
    s.add(f'<rect x="30" y="20" width="940" height="290" rx="10" fill="{PAPER}" stroke="{INK}" stroke-width="2"/>')
    heads = [("TASK", 50), ("RULE FOR SUCCESS", 230), ("RESULT, WITH SPREAD", 470), ("REPEATED BY OTHERS?", 780)]
    for h, x in heads:
        s.text(x, 52, h, 14, RUST, "start", 600, spacing=1.2)
    s.add(f'<path d="M30 64H970" stroke="{INK}" stroke-width="1.4"/>')
    rows = [("design A", "passes all tests", .62, .12), ("design B", "passes all tests", .44, .2), ("design C", "meets timing", .8, .06), ("design D", "meets timing", .3, .25)]
    for i, (t, rule, m, sp) in enumerate(rows):
        y = 104 + i * 52
        s.text(50, y, t, 17, INK).text(230, y, rule + " (v2)", 16, MUTE)
        x0 = 470
        s.add(f'<path d="M{x0} {y - 6}H{x0 + 260}" stroke="{LINE}" stroke-width="6" stroke-linecap="round"/>')
        a, b = x0 + 260 * (m - sp), x0 + 260 * (m + sp)
        s.add(f'<path d="M{a:.0f} {y - 6}H{b:.0f}" stroke="{TAN}" stroke-width="6"/><circle cx="{x0 + 260 * m:.0f}" cy="{y - 6}" r="7" fill="{RUST}"/>')
        s.add(f'<rect x="800" y="{y - 20}" width="26" height="26" rx="4" fill="none" stroke="{INK}" stroke-width="1.6" stroke-dasharray="4 3"/>')
    s.text(500, 344, "A score means little without its tasks, its rule, its version and its spread.", 18, RUST, "middle", italic=True, serif=True)
    s.text(500, 368, "(task names and dots are made-up examples)", 14, MUTE, "middle")
    return s.done()


DIR_SCENE = {"constraints-become-executable": d_sieve, "data-movement-as-contract": d_move, "closed-loop-design": d_wheel,
             "reliability-security-upstream": d_shift, "physical-reality-in-the-loop": d_heat, "evaluation-as-research": d_bench}

ROLE = {   # plain words for each conference's role, from the "Venue roles" table of reports/comparisons/<direction>.md
    "constraints-become-executable": ("Dataflow and system rules a compiler can check", "Tools that generate, search and map designs against checks", "Verification and physical-design steps that use the checks"),
    "data-movement-as-contract": ("Traffic between experts, caches and memory near compute", "Memory links, logic in memory and buffering", "Bandwidth tied to placement, heat and the package"),
    "closed-loop-design": ("No direct evidence yet; compiler cases are nearby", "Searches, fast predictors and tool feedback", "How accurate the fast model is, and whether results hold later"),
    "reliability-security-upstream": ("Error correction, interference and heat while running", "Fault fixes, attacks and the cost of protection", "Threat models and how they are checked"),
    "physical-reality-in-the-loop": ("Heat imbalance after work is placed on chips", "Fast heat, package and process models for search", "Placement, process and device checks before sign-off"),
    "evaluation-as-research": ("Released systems and the workloads they run", "Task choice, search budget and what the scorer counts", "Proof state, simulator accuracy and implementation limits"),
}


def venue_refs(d):
    """Evidence references per conference, read from the comparison report's own table."""
    t = (ROOT / f"reports/comparisons/{d}.md").read_text(encoding="utf-8")
    out = {}
    for v in ("ISCA", "DAC", "ICCAD"):
        m = re.search(rf"^\| {v} \|.*\| (\d+) \|\s*$", t, re.M)
        out[v] = int(m.group(1)) if m else 0
    return out


def c_layers(uid, d):
    """Across the three conferences: three layers of the stack, one direction crossing them, each layer's evidence count."""
    refs = venue_refs(d)
    s = Svg(uid, f"Three layers: ISCA at the architecture layer, DAC at the design-tool layer, ICCAD at the algorithm and physical layer. One direction runs through all three. Evidence references: ISCA {refs['ISCA']}, DAC {refs['DAC']}, ICCAD {refs['ICCAD']}.", 1000, 360)
    lay = [("ISCA", "how the computer is organised"), ("DAC", "the tools that build chips"), ("ICCAD", "the algorithms inside the tools")]
    for i, ((v, what), role) in enumerate(zip(lay, ROLE[d])):
        y = 24 + i * 104
        s.add(f'<rect x="20" y="{y}" width="960" height="92" rx="8" fill="{[SOFT, PAPER, SAND][i]}" stroke="{INK}" stroke-width="1.6"/>')
        s.text(40, y + 36, v, 24, INK, "start", 600, serif=True).text(40, y + 62, what, 15, MUTE)
        s.text(330, y + 40, role, 17, INK)
        n = refs[v]
        for k in range(n):
            s.add(f'<rect x="{330 + k * 18}" y="{y + 56}" width="12" height="16" rx="2" fill="{RUST}"/>')
        s.text(330 + max(n, 0) * 18 + 8, y + 70, f"{n} evidence reference{'s' if n != 1 else ''}", 14, MUTE)
    s.add(f'<path d="M940 14V340" stroke="{RUST}" stroke-width="6" opacity=".6"/><path d="M928 330l12 18 12-18" fill="{RUST}"/>')
    return s.done()


# ------------------------------------------------------------------------------------------- evidence depth and shared charts

def depth_ladder(uid, n_desc, n_abs, n_full, n_deep):
    s = Svg(uid, f"A ladder of reading depth: {n_desc} records from program descriptions, {n_abs} from abstracts or reports, {n_full} from full papers or preprints, {n_deep} papers checked in depth, none repeated independently.", 1000, 400)
    rungs = [("Program description only", f"{n_desc}", "a short summary from the conference"), ("Abstract, report or released files", f"{n_abs}", "the claim, rarely the conditions"),
             ("Full paper or preprint", f"{n_full}", "methods, tables and limits"), ("Checked in depth", f"{n_deep}", "a deep-read page each"), ("Repeated independently", "0", "no one has rerun these yet")]
    s.add(f'<path d="M120 390V14M300 390V14" stroke="{INK}" stroke-width="5" stroke-linecap="round"/>')
    for i, (h, v, t) in enumerate(rungs):
        y = 360 - i * 80
        hot = i == 0
        s.add(f'<path d="M120 {y}H300" stroke="{RUST if hot else INK}" stroke-width="{7 if hot else 4}" stroke-linecap="round"/>')
        s.text(210, y - 12, v, 30, RUST if hot else INK, "middle", serif=True)
        s.text(340, y - 14, h, 19, INK, "start", 600).text(340, y + 10, t, 16, MUTE)
    s.text(760, 60, "Each rung up holds fewer papers", 18, RUST, "start", italic=True, serif=True)
    s.text(760, 84, "and says more about each one.", 18, RUST, "start", italic=True, serif=True)
    return s.done()


CAPS = {"ai": "AI", "ml": "ML", "llm": "LLM", "eda": "EDA", "fpga": "FPGA", "rtl": "RTL", "rf": "RF", "3d": "3D", "nonvon": "non-von", "neumann": "Neumann", "edge": "edge"}


def nice(label):
    """Taxonomy labels are stored in lower case: restore the capitals of acronyms."""
    w = label.split(" ")
    return " ".join(CAPS.get(x.lower(), x) if i else (CAPS.get(x.lower(), x[:1].upper() + x[1:])) for i, x in enumerate(w))


def bars(title, desc, items, em=None):
    items = [(nice(k), v) for k, v in items]
    em = nice(em) if em else None
    return {"type": "bars", "title": title, "desc": desc, "max": max(v for _, v in items),
            "items": [{"label": k, "value": v, **({"em": True} if k == em else {})} for k, v in items]}


def roofline_chart():
    """Attainable speed = min(peak, bandwidth × arithmetic intensity). Illustration values: peak 100, bandwidth 10."""
    pts = lambda P, B: [[x / 2, round(min(P, B * x / 2), 2)] for x in range(0, 41)]
    return {"type": "line", "title": "How fast can the compute grid run?",
            "desc": "Speed = the smaller of peak (100) and bandwidth × operations per byte (10 × I). Below 10 operations per byte, memory sets the speed.",
            "x": {"min": 0, "max": 20, "label": "operations done per byte fetched from memory (I)", "ticks": [0, 5, 10, 15, 20]},
            "y": {"min": 0, "max": 110, "label": "operations per second, in units"},
            "series": [{"name": "attainable speed", "points": pts(100, 10), "decimals": 1}],
            "slider": {"label": "Operations per byte", "min": 0, "max": 20, "step": 0.5, "value": 4, "decimals": 1}}


def queue_chart():
    """Waiting time in a single queue, W = 1 / (1 − load) in units of one job's service time (illustration)."""
    pts = [[round(r / 100, 2), round(1 / (1 - r / 100), 2)] for r in range(0, 96, 5)]
    return {"type": "line", "title": "Time in the system as the server gets busier",
            "desc": "Time = service time ÷ (1 − load), for one queue with random arrivals. At load 0.5 a job takes 2 service times; at 0.9 it takes 10.",
            "x": {"min": 0, "max": 1, "label": "load: share of time the server is busy", "ticks": [0, 0.2, 0.4, 0.6, 0.8, 1]},
            "y": {"min": 0, "max": 21, "label": "time in system, in service times"},
            "series": [{"name": "time in system", "points": pts, "decimals": 1}],
            "slider": {"label": "Load", "min": 0, "max": 0.95, "step": 0.05, "value": 0.5, "decimals": 2}}


def tries_chart():
    """Chance that at least one of k tries passes: 1 − (1 − p)^k (illustration p = 0.2 and 0.5)."""
    pts = lambda p: [[k, round(1 - (1 - p) ** k, 3)] for k in range(1, 21)]
    return {"type": "line", "title": "Chance that at least one try passes every check",
            "desc": "Chance = 1 − (1 − p)^k for k tries that each pass with chance p. With p = 0.2, five tries give 0.67.",
            "x": {"min": 1, "max": 20, "label": "number of tries (k)", "ticks": [1, 5, 10, 15, 20]},
            "y": {"min": 0, "max": 1, "label": "chance at least one passes"},
            "series": [{"name": "each try passes 2 times in 10", "points": pts(0.2), "decimals": 2}, {"name": "each try passes 5 times in 10", "points": pts(0.5), "decimals": 2}],
            "slider": {"label": "Tries", "min": 1, "max": 20, "step": 1, "value": 5, "decimals": 0}}


def yield_chart():
    """Share of good dies, Y = e^(−D·A), defect density D = 0.1 per cm² (illustration); one big die vs four quarters."""
    pts = [[a / 2, round(math.exp(-0.1 * a / 2), 3)] for a in range(1, 17)]
    return {"type": "line", "title": "Share of dies that work, by die area",
            "desc": "Share = e^(−D × A), with D = 0.1 defects per cm². An 8 cm² die works 0.45 of the time; a 2 cm² quarter works 0.82 of the time.",
            "x": {"min": 0.5, "max": 8, "label": "die area A, cm²", "ticks": [1, 2, 4, 6, 8]},
            "y": {"min": 0, "max": 1, "label": "share of dies that work"},
            "series": [{"name": "share that work", "points": pts, "decimals": 2}],
            "slider": {"label": "Die area, cm²", "min": 0.5, "max": 8, "step": 0.5, "value": 2, "decimals": 1}}


def slack_chart():
    """Slack = clock period − path delay; delay 0.8 ns (illustration)."""
    pts = [[p / 10, round(p / 10 - 0.8, 2)] for p in range(5, 16)]
    return {"type": "line", "title": "Timing slack as the clock period changes",
            "desc": "Slack = clock period − path delay, with a path delay of 0.8 ns. Below 0.8 ns the slack is negative and the path fails.",
            "x": {"min": 0.5, "max": 1.5, "label": "clock period, ns", "ticks": [0.5, 0.8, 1, 1.5]},
            "y": {"min": -0.3, "max": 0.7, "label": "slack, ns"},
            "series": [{"name": "slack", "points": pts, "decimals": 2}],
            "slider": {"label": "Clock period, ns", "min": 0.5, "max": 1.5, "step": 0.1, "value": 1, "decimals": 1}}


def noise_chart():
    """Distinct levels a reading can tell apart: L = range / (2 × noise) with range 1 V (illustration); bits = log2 L."""
    pts = [[n / 100, round(math.log2(1 / (2 * n / 100)), 2)] for n in range(1, 26)]
    return {"type": "line", "title": "How many bits an analog reading can carry",
            "desc": "Bits = log₂(range ÷ (2 × noise)), with a 1 V range. At 0.05 V of noise that is log₂ 10, about 3.3 bits.",
            "x": {"min": 0.01, "max": 0.25, "label": "noise, volts", "ticks": [0.05, 0.1, 0.15, 0.2, 0.25]},
            "y": {"min": 0, "max": 6, "label": "bits"},
            "series": [{"name": "usable bits", "points": pts, "decimals": 1}],
            "slider": {"label": "Noise, V", "min": 0.01, "max": 0.25, "step": 0.01, "value": 0.05, "decimals": 2}}


THEME_CHART = {"architecture-and-accelerators": (roofline_chart, "Try it: when memory, not arithmetic, sets the speed",
                                                 "Worked out from one formula: speed = the smaller of peak and bandwidth × operations per byte. Peak 100 and bandwidth 10 are made-up units for the illustration."),
               "systems-applications-and-workloads": (queue_chart, "Try it: why a busy server makes everyone wait",
                                                      "Worked out from the single-queue formula: time = service time ÷ (1 − load). The formula assumes random arrivals and one server; it is an illustration, not a paper's result."),
               "ai-assisted-eda": (tries_chart, "Try it: more tries raise the pass rate, and the cost",
                                   "Worked out from 1 − (1 − p)^k. The pass chances 0.2 and 0.5 are made up. A fair comparison counts every try's tool runs."),
               "chiplets-3d-and-packaging": (yield_chart, "Try it: why small dies are cheaper to make",
                                             "Worked out from the simple yield model, share = e^(−D × A). The defect density 0.1 per cm² is a made-up value."),
               "physical-design-and-manufacturing": (slack_chart, "Try it: slack is the time to spare",
                                                     "Worked out from slack = clock period − path delay. The path delay 0.8 ns is a made-up value."),
               "analog-mixed-signal-and-emerging-devices": (noise_chart, "Try it: noise limits how many bits an analog sum holds",
                                                            "Worked out from bits = log₂(range ÷ (2 × noise)). The 1 V range is a made-up value; real converters lose more to other effects."),
               "memory-interconnect-and-storage": (roofline_chart, "Try it: when moving data, not arithmetic, sets the speed",
                                                   "Worked out from speed = the smaller of peak and bandwidth × operations per byte. Peak 100 and bandwidth 10 are made-up units.")}


# ------------------------------------------------------------------------------------------- per page

DIRS = {d["direction_id"]: d for d in ATLAS["directions"]}
DIR_ORDER = ["constraints-become-executable", "data-movement-as-contract", "closed-loop-design", "reliability-security-upstream", "physical-reality-in-the-loop", "evaluation-as-research"]
CONF_NAME = {"dac": "DAC", "iccad": "ICCAD", "isca": "ISCA"}


def scene_panel(svg, panel, chip, caption, min_width=900):
    return {"html": scenes.scene_html(svg, panel, chip, caption, min_width)}


def conf_line(counter):
    return " · ".join(f"{CONF_NAME[k]} {v}" for k, v in sorted(counter.items(), key=lambda kv: -kv[1]))


def theme_visuals(tid, uid):
    t = THEME_BY[tid]
    subs = sorted(t["subthemes"], key=lambda s: -s["record_count"])
    cards = [{"label": "Papers", "value": str(t["record_count"]), "note": "in this theme"},
             {"label": "Subthemes", "value": str(t["subtheme_count"]), "note": "narrower problems"},
             {"label": "Largest subtheme", "value": f"{subs[0]['record_count']} papers", "note": nice(subs[0]["label"])},
             {"label": "Top conference", "value": conf_line(Counter(t["conference_counts"])).split(" · ")[0], "note": "all: " + conf_line(Counter(t["conference_counts"]))}]
    panels = [scene_panel(SCENE[tid](uid), "The problem in one drawing", "our drawing",
                          "Each numbered part is one place where this theme's papers act. The subtheme pages ring the part they work on.")]
    if tid in THEME_CHART:
        f, title, cap = THEME_CHART[tid]
        panels.append({"panel": title, "chip": "illustration", "chart": f(), "caption": cap})
    items = [(s["label"], s["record_count"]) for s in subs[:12]]
    panels.append({"panel": f"Papers in each subtheme, largest {len(items)} of {t['subtheme_count']}", "chip": "counted",
                   "chart": bars("Papers per subtheme", f"{subs[0]['label']} has the most, {subs[0]['record_count']}.", items, em=items[0][0]),
                   "caption": f"Counted from data/taxonomy-expanded-v1.json: {t['record_count']} papers in {t['subtheme_count']} subthemes. A count shows where this sample's papers went, not how important a subject is."})
    return {"cards": cards, "panels": panels}


def page_visuals(rel):
    """{"cards": [...], "panels": [...]} for a page, or {} to fall back on counted cards."""
    stem = rel.rsplit("/", 1)[-1].removesuffix(".html")
    uid = re.sub(r"[^a-z0-9]", "", stem)[:14]
    if rel.startswith("themes/") and stem in THEME_BY:
        return theme_visuals(stem, "t" + uid)
    if rel.startswith("subthemes/") and stem in SUB:
        s, t = SUB[stem], SUB_THEME[stem]
        at, a, b = SUBNOTE[stem]
        dd = Counter()
        for k, v in s["tier"].items():
            dd[depth(k)] += v
        cards = [{"label": "Papers", "value": str(s["record_count"]), "note": conf_line(s["conf"])},
                 {"label": "Read from", "value": f"{dd['desc']} of {s['record_count']}", "note": "short program descriptions"},
                 {"label": "Part it changes", "value": f"Part {at + 1}", "note": STATIONS[t['theme_id']][at]},
                 {"label": "Parent theme", "value": f"{t['record_count']} papers", "note": t["label"]}]
        panels = [scene_panel(SCENE[t["theme_id"]]("s" + uid, at, (a, b)), f"Where these papers act: part {at + 1} of {t['label'].lower()}", "our drawing",
                              f"The drawing shows the whole {t['label'].lower()} problem; the rust ring marks part {at + 1}, {STATIONS[t['theme_id']][at].lower()}. The words in the box are ours, from the explanation below.")]
        items = [(lab, n) for lab, n in (("Program description", dd["desc"]), ("Abstract or report", dd["abs"]), ("Full paper or preprint", dd["full"])) if n]
        panels.append({"panel": f"What the {s['record_count']} paper records were read from", "chip": "counted",
                       "chart": bars("Records by source", f"{dd['desc']} of {s['record_count']} come from the short program description.", items, em="Full paper or preprint" if dd["full"] else None),
                       "caption": "Counted from the source tier of each record in data/taxonomy-expanded-v1.json. A program description gives the claim, rarely the test conditions."})
        return {"cards": cards, "panels": panels}
    if rel.startswith("deep-reads/"):
        key = stem.split("-primary")[0]
        if key in DEEP:
            tid, at, (a, b), got = DEEP[key]
            rung = {"description": "program description", "preprint": "full preprint", "code": "released code"}[got]
            cards = [{"label": "Conference", "value": "DAC 2026", "note": "where it was presented"},
                     {"label": "Deepest source", "value": rung, "note": "found in a bounded search"},
                     {"label": "Part it changes", "value": f"Part {at + 1}", "note": STATIONS[tid][at]},
                     {"label": "Repeated by us", "value": "no", "note": "nothing rerun"}]
            return {"cards": cards, "panels": [scene_panel(SCENE[tid]("d" + uid, at, (a, b)), f"Where this paper acts: part {at + 1} of {THEME_BY[tid]['label'].lower()}", "our drawing",
                    "The rust ring marks the part this paper changes. The first line in the box says what it does; the second says what reading the full source found.")]}
    m = re.match(r"directions/0\d-([a-z-]+)$", rel.removesuffix(".html"))
    if m and m.group(1) in DIRS:
        d = DIRS[m.group(1)]
        ev = d["evidence"]
        conf = Counter(e["conference_id"] for e in ev)
        cards = [{"label": "Evidence papers", "value": str(len(ev)), "note": conf_line(conf)},
                 {"label": "Skills it covers", "value": str(len(d["subskills"])), "note": "named mechanisms"},
                 {"label": "Independent reviews", "value": str(d["independent_review_count"]), "note": "none yet"},
                 {"label": "Status", "value": "hypothesis", "note": "not a measured trend"}]
        panels = [scene_panel(DIR_SCENE[d["direction_id"]]("r" + uid), "The direction in one drawing", "our drawing", d["first_principle"])]
        panels.append({"panel": "Where the evidence papers come from", "chip": "counted",
                       "chart": bars("Evidence papers per conference", f"{len(ev)} papers back this direction.", [(CONF_NAME[k], v) for k, v in sorted(conf.items(), key=lambda kv: -kv[1])]),
                       "caption": "Counted from data/long-term-direction-atlas-v1.json. A paper can back more than one direction."})
        return {"cards": cards, "panels": panels}
    if rel.startswith("comparisons/") and stem in DIRS:
        r = venue_refs(stem)
        cards = [{"label": v, "value": f"{r[v]} refs", "note": "evidence references"} for v in ("ISCA", "DAC", "ICCAD")]
        return {"cards": cards, "panels": [scene_panel(c_layers("c" + uid, stem), "One direction, three layers", "from the papers",
                "Each band is one conference's layer. The rust blocks count the evidence references in the table below; the words are ours, from the same table.")]}
    if rel in ("guide/evidence-summary-v1.html", "guide/reading-guide-v1.html", "guide/research-atlas-index-v1.html", "deep-reads.html"):
        n = TAX["record_count"]
        tiers = Counter()
        for th in TAX["themes"]:
            for s in th["subthemes"]:
                for k, v in s["source_tier_counts"].items():
                    tiers[depth(k)] += v
        n_deep = len(list((ROOT / "dac/reports").glob("*-primary-*.md")))
        cards = [{"label": "Paper records", "value": str(n), "note": "ISCA, DAC, ICCAD"},
                 {"label": "Descriptions only", "value": str(tiers["desc"]), "note": f"of {n} records"},
                 {"label": "Full papers", "value": str(tiers["full"]), "note": "or preprints"},
                 {"label": "Deep reads", "value": str(n_deep), "note": "checked in depth"}]
        return {"cards": cards, "panels": [scene_panel(depth_ladder("g" + uid, tiers["desc"], tiers["abs"], tiers["full"], n_deep), "How deep the reading went", "counted",
                f"Counted from data/taxonomy-expanded-v1.json and dac/reports/: {tiers['desc']} records from program descriptions, {tiers['full']} from full papers or preprints.")]}
    if rel in ("guide/expanded-taxonomy-v1.html", "themes.html", "subthemes.html", "explorer.html"):
        th = sorted(TAX["themes"], key=lambda x: -x["record_count"])
        items = [(x["label"], x["record_count"]) for x in th]
        cards = [{"label": "Themes", "value": str(TAX["theme_count"]), "note": "broad subjects"},
                 {"label": "Subthemes", "value": str(TAX["observed_subtheme_count"]), "note": "narrower problems"},
                 {"label": "Largest theme", "value": f"{th[0]['record_count']} papers", "note": th[0]["label"]},
                 {"label": "Smallest theme", "value": f"{th[-1]['record_count']} papers", "note": th[-1]["label"]}]
        return {"cards": cards, "panels": [{"panel": f"Papers in each of the {TAX['theme_count']} themes", "chip": "counted",
                "chart": bars("Papers per theme", f"{th[0]['label']} leads with {th[0]['record_count']}.", items, em=items[0][0]),
                "caption": f"Counted from data/taxonomy-expanded-v1.json. Each of the {TAX['record_count']} records sits in one theme."}]}
    if rel in ("directions.html", "comparisons.html", "guide/field-directions-and-hypotheses-v1.html", "guide/direction-review-gate-v1.html"):
        items = [(DIRS[d]["label"], len(DIRS[d]["evidence"])) for d in DIR_ORDER]
        cards = [{"label": "Directions", "value": "6", "note": "each a hypothesis"},
                 {"label": "Most evidence", "value": f"{max(v for _, v in items)} papers", "note": max(items, key=lambda kv: kv[1])[0]},
                 {"label": "Least evidence", "value": f"{min(v for _, v in items)} papers", "note": min(items, key=lambda kv: kv[1])[0]},
                 {"label": "Independent reviews", "value": "0", "note": "for every direction"}]
        return {"cards": cards, "panels": [scene_panel(d_wheel("w" + uid), "The common thread: design as a loop", "our drawing",
                "Most directions feed a check, a measurement or a physical limit back into the next design choice."),
                {"panel": "Evidence papers behind each direction", "chip": "counted",
                 "chart": bars("Evidence papers per direction", "A paper can back more than one direction.", items),
                 "caption": "Counted from data/long-term-direction-atlas-v1.json."}]}
    if rel in ("guide/longitudinal-protocol-v1.html", "guide/research-agenda-v1.html"):
        return {"panels": [scene_panel(d_bench("b" + uid), "What a fair comparison needs", "our drawing",
                "A result is comparable across years only when the tasks, the rule for success, its version and the spread are all stated.")]}
    return {}


def hbar_svg(uid, title, items, unit=""):
    """A static bar chart in the boards' hand, for slides (the site uses the kit's live charts)."""
    W, row = 1000, 52
    H = 30 + row * len(items)
    mx = max(v for _, v in items)
    s = Svg(uid, title + ": " + ", ".join(f"{k} {v}" for k, v in items), W, H)
    for i, (k, v) in enumerate(items):
        y = 20 + i * row
        w = 560 * v / mx
        s.text(330, y + 26, k, 20, INK, "end")
        s.add(f'<rect x="346" y="{y + 8}" width="560" height="26" fill="{SAND}"/><rect x="346" y="{y + 8}" width="{w:.0f}" height="26" fill="{RUST if i == 0 else TAN}"/>')
        s.text(352 + w + 8, y + 28, f"{v}{unit}", 20, INK, "start", 600)
    return s.done()
