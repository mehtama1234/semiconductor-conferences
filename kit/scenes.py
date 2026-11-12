#!/usr/bin/env python3
"""Scenes: large explanatory drawings for course pages, in the hand of the owner's boards.

Two sources:
  board(name, labels=None)   one of the boards' own drawings from kit/scenes/board/ (see scenes/index.json),
                             taken as it is; `labels` maps a label number (data-l) to replacement words.
  control_loop(...), landscape(...), message_graph(...), tree_search(...), game_table(...),
  particle_field(...), market(...), pipeline(...)
                             new scenes drawn for lectures, built from the same parts as the boards'
                             engineering sheets: a framed sheet, a ground line, hard-hat figures,
                             callout boxes with leaders, tilted number cards, a dashed rust path.

Every builder returns a Scene: `.svg` (inline SVG, viewBox 1200 wide, text never under 15 units) and
`.key` (the numbered callouts as a list, for the HTML legend under the drawing).
`scene_html(scene, panel=..., chip=..., caption=...)` wraps it in the kit's panel with the phone scroller.

Colours are written as the boards' hex values; course.css maps them to tokens (dark theme included).
"""
import html, json, math, re
from pathlib import Path

KIT = Path(__file__).resolve().parent
INK, MUTE, ESP, PAPER, PAGE, SAND, LINE, RUST, PEACH, TAN, TAUPE, HOLD = (
    "#2B2622", "#5A5047", "#3A2E26", "#FBF7F0", "#F3EDE2", "#ECE4D5", "#D9CDBA", "#9A4A22", "#E3B98F", "#C99A5B", "#C9B9A3", "#8B2E1F")
LAB = "IBM Plex Sans Condensed"; SER = "Source Serif 4"; DIS = "Fraunces"
esc = lambda s: html.escape(str(s), quote=True)
f1 = lambda v: f"{v:.1f}".rstrip("0").rstrip(".")


class Scene:
    def __init__(self, svg, key, title): self.svg, self.key, self.title = svg, key, title
    def __str__(self): return self.svg


def board(name, labels=None):
    """One of the boards' own scenes. labels={3: "new words"} replaces the text numbered data-l="3"."""
    svg = (KIT / "scenes" / "board" / f"{name}.svg").read_text().strip()
    for n, words in (labels or {}).items():
        svg = re.sub(rf'(<text data-l="{int(n)}"[^>]*>).*?(</text>)', lambda m: m.group(1) + esc(words) + m.group(2), svg, count=1, flags=re.S)
    return svg


def board_index():
    return json.loads((KIT / "scenes" / "index.json").read_text())

# ----------------------------------------------------------------------------- the parts

class Sheet:
    """A framed drawing sheet (the boards' engineering-sheet look): border, zone marks, title block."""

    def __init__(self, uid, title, w=1200, h=600, no="", kind="", frame=True, sub="not to scale"):
        self.uid, self.w, self.h, self.title = uid, w, h, title
        self.out, self.key, self.n, self._tb = [], [], 0, None
        u = uid
        self.defs = (
            f'<pattern id="{u}-earth" width="12" height="12" patternUnits="userSpaceOnUse" patternTransform="rotate(45)"><line x1="0" y1="0" x2="0" y2="12" stroke="{MUTE}" stroke-width=".8" opacity=".35"/></pattern>'
            f'<pattern id="{u}-dots" width="9" height="9" patternUnits="userSpaceOnUse"><circle cx="2" cy="2" r="1" fill="{MUTE}" opacity=".45"/><circle cx="6.5" cy="6.5" r=".8" fill="{MUTE}" opacity=".35"/></pattern>'
            f'<pattern id="{u}-grid" width="20" height="20" patternUnits="userSpaceOnUse"><path d="M20 0H0V20" fill="none" stroke="{LINE}" stroke-width=".8"/></pattern>'
            f'<pattern id="{u}-hatch" width="7" height="7" patternUnits="userSpaceOnUse" patternTransform="rotate(45)"><line x1="0" y1="0" x2="0" y2="7" stroke="{INK}" stroke-width=".9" opacity=".5"/></pattern>'
            f'<pattern id="{u}-water" width="40" height="14" patternUnits="userSpaceOnUse"><path d="M0 7q10-6 20 0t20 0" fill="none" stroke="{MUTE}" stroke-width=".9" opacity=".55"/></pattern>'
            + "".join(f'<marker id="{u}-a{k}" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0 0L10 5L0 10z" fill="{c}"/></marker>'
                      for k, c in (("i", INK), ("r", RUST), ("m", MUTE))))
        if frame:
            self.add(f'<rect x="1" y="1" width="{w - 2}" height="{h - 2}" fill="{PAPER}" stroke="{INK}" stroke-width="1.5"/>'
                     f'<rect x="12" y="12" width="{w - 24}" height="{h - 24}" fill="none" stroke="{INK}" stroke-width=".8"/>')
            for i in range(6):
                x = 12 + (w - 24) * (i + .5) / 6
                self.add(f'<path d="M{f1(12 + (w - 24) * i / 6)} 1v11M{f1(12 + (w - 24) * i / 6)} {h - 12}v11" stroke="{INK}" stroke-width=".8"/>')
            self._tb = (kind, no, sub)
        else:
            self.add(f'<rect width="{w}" height="{h}" fill="{PAPER}"/>')

    def add(self, s): self.out.append(s); return self
    def pat(self, name): return f"url(#{self.uid}-{name})"
    def mk(self, k="i"): return f"url(#{self.uid}-a{k})"

    def text(self, x, y, s, kind="body", size=None, anchor="start", fill=None, key=None, weight=None, italic=False, rot=None):
        fam, sz, wt, ls, fl = {"cap": (LAB, 14, 600, 1.2, INK), "lab": (LAB, 15, 600, .2, INK), "body": (SER, 16, 400, 0, MUTE),
                               "num": (DIS, 28, 400, 0, INK), "head": (DIS, 22, 400, 0, INK)}[kind]
        self.n += 1
        a = f' text-anchor="{anchor}"' if anchor != "start" else ""
        r = f' transform="rotate({rot} {f1(x)} {f1(y)})"' if rot else ""
        it = ' font-style="italic"' if italic else ""
        self.add(f'<text data-l="{esc(key or self.n)}" x="{f1(x)}" y="{f1(y)}" font-family="{fam}" font-size="{size or sz}" font-weight="{weight or wt}"'
                 f' letter-spacing="{ls}" fill="{fill or fl}"{a}{it}{r}>{esc(s)}</text>')
        return self

    def lines(self, x, y, rows, kind="body", lh=20, **kw):
        for i, r in enumerate(rows): self.text(x, y + i * lh, r, kind, **kw)

    def ground(self, y, x0=12, x1=None, depth=None, fill="earth"):
        x1 = x1 or self.w - 12; depth = depth or (self.h - 12 - y)
        self.add(f'<rect x="{x0}" y="{y}" width="{x1 - x0}" height="{depth}" fill="{SAND}"/><rect x="{x0}" y="{y}" width="{x1 - x0}" height="{depth}" fill="{self.pat(fill)}"/>'
                 f'<path d="M{x0} {y}H{x1}" stroke="{INK}" stroke-width="2"/>')

    def person(self, x, y, s=1.0, body=PEACH, hat=TAN, face=1, arm=None):
        """A hard-hat figure standing on y, about 78 * s tall, facing right (face=1) or left (-1). arm=(dx, dy) points."""
        g = [f'<g transform="translate({f1(x)} {f1(y)}) scale({f1(s * face)} {f1(s)})" stroke="{INK}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">',
             f'<path d="M-7 -30L-9 0M7 -30L9 0" stroke-width="5" stroke="{ESP}"/>',
             f'<path d="M-13 -58h26l3 30h-32z" fill="{body}"/>',
             f'<circle cx="0" cy="-67" r="9" fill="{PAPER}"/>',
             f'<path d="M-11 -69a11 10 0 0 1 22 0z" fill="{hat}"/><path d="M-13 -69h28"/>']
        if arm: g.append(f'<path d="M12 -52L{arm[0]} {arm[1]}" stroke-width="4" stroke="{ESP}" fill="none"/>')
        g.append("</g>"); self.add("".join(g)); return self

    def callout(self, x, y, w, title, rows, to=None, n=None, rust=False, side="bottom"):
        """A white label box with a caps title, body lines, and a leader ending in a dot at `to`."""
        h = 30 + 20 * len(rows) + 6
        if to:
            sx = min(max(to[0], x + 14), x + w - 14)
            sy = y + h if to[1] > y + h else y
            if side == "left": sx, sy = x, y + h / 2
            if side == "right": sx, sy = x + w, y + h / 2
            self.add(f'<path d="M{f1(sx)} {f1(sy)}L{f1(to[0])} {f1(to[1])}" stroke="{INK}" stroke-width="1.2" fill="none"/><circle cx="{f1(to[0])}" cy="{f1(to[1])}" r="3.5" fill="{INK}"/>')
        self.add(f'<rect x="{f1(x)}" y="{f1(y)}" width="{w}" height="{h}" fill="{PAPER}" stroke="{RUST if rust else INK}" stroke-width="1.2"/>')
        tx = x + 12
        if n is not None:
            self.badge(x + 20, y + 19, n); tx = x + 40
            self.key.append((n, title, " ".join(rows)))
        self.text(tx, y + 23, title.upper(), "cap", fill=RUST if rust else INK)
        self.lines(x + 12, y + 45, rows, "body", size=15)
        return self

    def badge(self, x, y, n, r=12, fill=ESP):
        self.add(f'<circle cx="{f1(x)}" cy="{f1(y)}" r="{r}" fill="{fill}"/>')
        self.text(x, y + 5, n, "lab", size=15, anchor="middle", fill=PAPER, key=f"badge-{n}")

    def card(self, x, y, k, value, note="", rot=-2, w=190, first=False):
        """A tilted number card, as in the boards' opening bands: label, big number, a few words."""
        self.add(f'<g transform="translate({f1(x)} {f1(y)}) rotate({rot})"><rect x="3" y="4" width="{w}" height="96" fill="{INK}" opacity=".12"/>'
                 f'<rect width="{w}" height="96" fill="{PAPER}" stroke="{LINE}" stroke-width="1"/><rect width="{w}" height="{5 if first else 3}" fill="{RUST}"/>')
        self.text(12, 26, k.upper(), "cap", size=14, fill=RUST); self.text(12, 60, value, "num", size=27); self.text(12, 82, note, "lab", size=14, fill=MUTE)
        self.add("</g>"); return self

    def arrow(self, d, k="i", w=2, dash=None, start=False):
        c = {"i": INK, "r": RUST, "m": MUTE}[k]
        da = f' stroke-dasharray="{dash}"' if dash else ""
        ms = f' marker-start="{self.mk(k)}"' if start else ""
        self.add(f'<path d="{d}" fill="none" stroke="{c}" stroke-width="{w}"{da} marker-end="{self.mk(k)}"{ms} stroke-linecap="round" stroke-linejoin="round"/>'); return self

    def done(self, label):
        if self._tb and (self._tb[0] or self._tb[1]):
            kind, no, sub = self._tb; w, h, title = self.w, self.h, self.title
            bw = 600
            self.add(f'<g><rect x="{w - 12 - bw}" y="{h - 12 - 46}" width="{bw}" height="46" fill="{PAPER}" stroke="{INK}" stroke-width="1"/>'
                     f'<path d="M{w - 12 - 96} {h - 58}v46M{w - 12 - bw + 140} {h - 58}v46" stroke="{INK}" stroke-width=".8"/></g>')
            self.text(w - 12 - bw + 10, h - 30, kind.upper(), "cap", size=14, key="sheet-kind", fill=MUTE)
            self.text(w - 12 - bw + 152, h - 28, title if len(title) <= 50 else title[:49].rstrip() + "…", "lab", size=15, key="sheet-title")
            self.text(w - 12 - 84, h - 30, no, "cap", size=14, key="sheet-no")
            self.text(w - 24, 34, sub.upper(), "cap", size=14, anchor="end", fill=MUTE, key="sheet-sub")
        svg = (f'<svg class="kit-scene kit-scene-made" data-scene="{self.uid}" viewBox="0 0 {self.w} {self.h}" role="img" aria-label="{esc(label)}">'
               f'<defs>{self.defs}</defs>{"".join(self.out)}</svg>')
        return Scene(svg, self.key, self.title)


def scene_html(scene, panel="The scene", chip="illustration", caption="", min_width=1120):
    """Panel with header, the drawing in a phone scroller, a numbered key and a caption."""
    from render_lecture import chip as chip_html, inline
    svg = scene.svg if isinstance(scene, Scene) else scene
    key = getattr(scene, "key", [])
    keyh = ('<ol class="ck-scene-key">' + "".join(f'<li value="{n}"><b>{esc(t)}</b> {esc(r)}</li>' for n, t, r in sorted(key)) + "</ol>") if key else ""
    cap = f'<figcaption class="ck-cap">{inline(caption)}</figcaption>' if caption else ""
    return (f'<figure class="rs-media ck-scene"><div class="rs-mh"><span>{inline(panel)}</span>{chip_html(chip)}</div>'
            f'<div class="rs-mb"><div class="ck-scene-pan" tabindex="0" role="group" aria-label="Drawing; scroll sideways on a small screen" style="--min:{min_width}px">{svg}</div>{keyh}{cap}</div></figure>')

# ----------------------------------------------------------------------------- 1. a control loop with a real plant

def control_loop(plant="car", uid="loop", title="The loop around the plant", target="Target: 25 m/s", measured="Measured: 22 m/s",
                 error="Error: 3 m/s", action="Push: more throttle", disturbance="A hill pushes back", cards=None, no="C-01", flat=False, pole=True):
    """A road, a car (or a cart with a pole, or a room with a heater), a sensor, a controller box and the path back."""
    s = Sheet(uid, title, no=no, kind="Control")
    gy = 430
    s.add(f'<rect x="13" y="60" width="1174" height="{gy - 60}" fill="{s.pat("grid")}" opacity=".6"/>')
    if plant == "thermostat":
        s.ground(gy)
        s.add(f'<g stroke="{INK}" stroke-width="2" stroke-linejoin="round"><path d="M430 {gy}V250L610 170L790 250V{gy}" fill="{PAGE}"/><path d="M410 262L610 172L810 262" fill="none" stroke-width="4"/>'
              f'<rect x="690" y="330" width="60" height="{gy - 330}" fill="{PAPER}"/><rect x="470" y="290" width="70" height="60" fill="{PAPER}"/><path d="M505 290v60M470 320h70"/>'
              f'<rect x="560" y="372" width="96" height="46" rx="4" fill="{RUST}"/><path d="M576 372v46M592 372v46M608 372v46M624 372v46M640 372v46" stroke="{PAPER}" stroke-width="1.5"/></g>'
              f'<path d="M580 360c-8-14 8-18 0-32M608 360c-8-14 8-18 0-32M636 360c-8-14 8-18 0-32" fill="none" stroke="{RUST}" stroke-width="2.5" stroke-linecap="round"/>'
              f'<g stroke="{INK}" stroke-width="2"><rect x="596" y="232" width="14" height="52" rx="7" fill="{PAPER}"/><circle cx="603" cy="290" r="11" fill="{RUST}"/><path d="M603 286v-34" stroke="{RUST}" stroke-width="5"/></g>'
              f'<path d="M300 300c40-12 60 12 100 0M300 330c40-12 60 12 100 0" fill="none" stroke="{MUTE}" stroke-width="2" stroke-linecap="round"/>')
        px, py, sx, sy, dx, dy = 608, 395, 603, 258, 350, 315
    else:
        rise = 0 if flat else 70
        hill = f"M12 {gy}H520C640 {gy} 700 {gy - rise} 820 {gy - rise}H1188V588H12Z"
        s.add(f'<path d="{hill}" fill="{SAND}"/><path d="{hill}" fill="{s.pat("earth")}"/><path d="M12 {gy}H520C640 {gy} 700 {gy - rise} 820 {gy - rise}H1188" fill="none" stroke="{INK}" stroke-width="2"/>'
              f'<path d="M30 {gy + 22}h50M110 {gy + 22}h50M190 {gy + 22}h50M270 {gy + 22}h50M350 {gy + 22}h50M430 {gy + 22}h50" stroke="{PAPER}" stroke-width="4"/>')
        if plant == "cart":
            s.add(f'<g stroke="{INK}" stroke-width="2" stroke-linejoin="round"><rect x="330" y="{gy - 62}" width="150" height="40" rx="5" fill="{PEACH}"/>'
                  + (f'<path d="M405 {gy - 62}L445 {gy - 210}" stroke="{RUST}" stroke-width="7" stroke-linecap="round"/><circle cx="445" cy="{gy - 214}" r="14" fill="{RUST}"/>' if pole else "") +
                  f'<circle cx="405" cy="{gy - 62}" r="7" fill="{PAPER}"/><circle cx="362" cy="{gy - 14}" r="14" fill="{ESP}"/><circle cx="448" cy="{gy - 14}" r="14" fill="{ESP}"/></g>'
                  + (f'<path d="M405 {gy - 70}V{gy - 220}" stroke="{MUTE}" stroke-width="1.2" stroke-dasharray="4 4"/><path d="M405 {gy - 170}A100 100 0 0 1 432 {gy - 166}" fill="none" stroke="{INK}" stroke-width="1.5"/>' if pole else
                     f'<path d="M250 {gy - 52}h-50M262 {gy - 36}h-70" stroke="{MUTE}" stroke-width="2" stroke-linecap="round"/>'))
            px, py, sx, sy = 480, gy - 42, (445, gy - 214)[0] if pole else 405, (gy - 214) if pole else gy - 62
        else:
            s.add(f'<g stroke="{INK}" stroke-width="2" stroke-linejoin="round"><path d="M300 {gy - 26}v-30q0-8 10-10l40-6 30-34q5-6 14-6h70q10 0 16 8l22 32 38 8q10 2 10 12v26z" fill="{PEACH}"/>'
                  f'<path d="M390 {gy - 74}l22-26h30v26zM452 {gy - 100}h28l18 26h-46z" fill="{PAPER}"/><circle cx="352" cy="{gy - 20}" r="20" fill="{ESP}"/><circle cx="352" cy="{gy - 20}" r="8" fill="{PAPER}"/>'
                  f'<circle cx="498" cy="{gy - 20}" r="20" fill="{ESP}"/><circle cx="498" cy="{gy - 20}" r="8" fill="{PAPER}"/></g>'
                  f'<path d="M250 {gy - 70}h-50M262 {gy - 50}h-70M250 {gy - 30}h-50" stroke="{MUTE}" stroke-width="2" stroke-linecap="round"/>')
            px, py, sx, sy = 550, gy - 50, 470, gy - 112
        dx, dy = 700, gy - 52
        s.arrow(f"M800 {gy - 150}L716 {gy - 62}" if not flat else f"M800 {gy - 40}H640", "m", 3)
        s.add(f'<g stroke="{INK}" stroke-width="2"><path d="M1040 {gy - rise}V{gy - rise - 120}" stroke-width="4"/><path d="M1040 {gy - rise - 120}h70l-14 16 14 16h-70z" fill="{RUST}"/></g>')
    # controller box and the loop
    s.add(f'<g stroke="{INK}" stroke-width="2"><rect x="470" y="78" width="250" height="84" rx="6" fill="{ESP}"/><rect x="486" y="94" width="60" height="52" rx="3" fill="{PAPER}"/>'
          f'<path d="M494 132l12-18 10 10 12-20 10 12" fill="none" stroke="{RUST}" stroke-width="2.5"/></g>')
    s.text(560, 114, "CONTROLLER", "cap", fill=PEACH, key="controller"); s.text(560, 138, "compares, then acts", "body", size=15, fill=PAGE, key="controller-sub")
    if 480 <= sx <= 710: s.arrow(f"M{sx} {sy - 12}V170", "r", 2.5, dash="8 6")
    else: s.arrow(f"M{sx} {sy - 12}V200Q{sx} 120 {sx + 60 if sx < 420 else 462} 120" + ("" if sx >= 420 else "H462"), "r", 2.5, dash="8 6")
    ax = px + 40
    s.arrow(f"M728 120H{max(ax, 760)}Q{max(ax, 760) + 50} 120 {max(ax, 760) + 50} 170V{py - 60}Q{max(ax, 760) + 50} {py} {px + 16} {py}", "i", 2.5)
    s.add(f'<circle cx="{sx}" cy="{sy}" r="9" fill="{PAPER}" stroke="{RUST}" stroke-width="3"/>')
    s.callout(40, 78, 250, "1 · measure", [measured, "the sensor reads the plant"], to=(sx - 9, sy - 2), rust=True)
    s.callout(40, 196, 250, "2 · compare", [target, error])
    s.arrow("M290 232C360 232 400 190 466 150", "m", 1.5, dash="3 4")
    s.callout(880, 78, 270, "3 · act", [action, "the input the plant feels"], to=(max(ax, 760) + 50, 200), side="left")
    if plant != "thermostat": s.callout(860, gy - 250, 280, "4 · disturbance", [disturbance], to=(760, gy - 108) if not flat else (724, gy - 40), side="left")
    else: s.callout(150, 330, 230, "4 · disturbance", [disturbance], to=(400, 315), side="right")
    s.key += [(1, "Measure", measured), (2, "Compare", f"{target}; {error}"), (3, "Act", action), (4, "Disturbance", disturbance)]
    for i, c in enumerate((cards or [])[:2]):
        s.card(60 + i * 230, 474, c[0], c[1], c[2] if len(c) > 2 else "", rot=(-2, 1.5)[i], first=i == 0)
    return s.done(f"{title}. {measured}. {target}. {error}. {action}. {disturbance}.")

# ----------------------------------------------------------------------------- 2. a landscape with a ball rolling to a minimum

def landscape(f=None, xmin=-2.0, xmax=5.0, path=None, x0=4.5, alpha=0.3, n=6, uid="land", title="Rolling downhill to the lowest point",
              labels=None, cards=None, fmt="{:.2f}", no="O-01", minimum=None):
    """A cut through a hillside. f is the height function (a Python function, or polynomial coefficients [c0, c1, c2, ...]); the ball takes n steepest-descent steps of size alpha from x0."""
    if isinstance(f, (list, tuple)):                 # polynomial coefficients, lowest power first (so a JSON visuals file can give f)
        co = list(f); f = lambda x: sum(c * x ** i for i, c in enumerate(co))
    f = f or (lambda x: 0.5 * (x - 1) ** 2 + 0.4)
    if path is None:                      # steepest descent with a numerical slope: x <- x - alpha f'(x)
        path = [x0]
        for _ in range(n): path.append(path[-1] - alpha * (f(path[-1] + 1e-5) - f(path[-1] - 1e-5)) / 2e-5)
    L = {"start": "Start", "step": "each step goes against the slope", "min": "Lowest point: slope is zero", "axis": "height f(x)", "x": "position x"}; L.update(labels or {})
    s = Sheet(uid, title, no=no, kind="Optimization")
    xs = [xmin + (xmax - xmin) * i / 120 for i in range(121)]
    ys = [f(x) for x in xs]; lo, hi = min(ys), max(ys)
    X = lambda x: 90 + (x - xmin) / (xmax - xmin) * 1020
    Y = lambda y: 470 - (y - lo) / (hi - lo or 1) * 330
    pts = " ".join(f"{f1(X(x))},{f1(Y(y))}" for x, y in zip(xs, ys))
    s.add(f'<rect x="13" y="60" width="1174" height="470" fill="{s.pat("grid")}" opacity=".5"/>')
    s.add(f'<polygon points="90,540 {pts} 1110,540" fill="{SAND}"/><polygon points="90,540 {pts} 1110,540" fill="{s.pat("earth")}"/><polyline points="{pts}" fill="none" stroke="{INK}" stroke-width="2.5" stroke-linejoin="round"/>')
    s.add(f'<path d="M90 100V540H1110" fill="none" stroke="{INK}" stroke-width="1.5"/>')
    s.text(78, 96, L["axis"].upper(), "cap", size=14, fill=MUTE, key="axis"); s.text(100, 562, L["x"].upper() + " →", "cap", size=14, fill=MUTE, key="x")
    xm = minimum if minimum is not None else xs[ys.index(lo)]
    s.add(f'<path d="M{f1(X(xm))} {f1(Y(f(xm)))}V540" stroke="{MUTE}" stroke-width="1.2" stroke-dasharray="4 4"/>'
          f'<g stroke="{INK}" stroke-width="2"><path d="M{f1(X(xm))} {f1(Y(f(xm)))}v-64" stroke-width="3"/><path d="M{f1(X(xm))} {f1(Y(f(xm)) - 64)}h44l-10 12 10 12h-44z" fill="{RUST}"/></g>')
    for i, x in enumerate(path):
        cx, cy = X(x), Y(f(x)) - 15
        last = i == len(path) - 1
        if i < len(path) - 1:
            nx, ny = X(path[i + 1]), Y(f(path[i + 1])) - 15
            s.arrow(f"M{f1(cx)} {f1(cy - 20)}Q{f1((cx + nx) / 2)} {f1(min(cy, ny) - 58)} {f1(nx)} {f1(ny - 22)}", "r", 2, dash="6 5")
        s.add(f'<circle cx="{f1(cx)}" cy="{f1(cy)}" r="14" fill="{RUST if i == 0 or last else PAPER}" stroke="{INK if not (i == 0 or last) else RUST}" stroke-width="2"/>')
        s.text(cx, cy + 5, i, "lab", size=14, anchor="middle", fill=PAPER if i == 0 or last else INK, key=f"ball-{i}")
    x0 = path[0]
    right = x0 >= xm                                   # the ball comes down from the right (default layout) or from the left (mirrored)
    mx = lambda x, w: x if right else 1200 - x - w
    sx0, sy0 = X(x0), Y(f(x0)) - 15
    s.callout(sx0 - 300 if right else sx0 + 80, max(70, sy0 - 34), 220, L["start"], [f"x = {fmt.format(x0)}", f"f = {fmt.format(f(x0))}"], to=(sx0 - 16 if right else sx0 + 16, sy0), n=1, side="right" if right else "left")
    a, b2 = path[min(2, len(path) - 1)], path[min(3, len(path) - 1)]
    s.callout(mx(400, 310), 236, 310, "one step", [L["step"]], to=((X(a) + X(b2)) / 2, min(Y(f(a)), Y(f(b2))) - 66), n=2, side="right" if right else "left")
    s.callout(mx(150, 330), 86, 330, "the lowest point", [L["min"], f"after {len(path) - 1} steps: x = {fmt.format(path[-1])}, f = {fmt.format(f(path[-1]))}"], to=(X(xm) - 4, Y(f(xm)) - 70), n=3, rust=True)
    for i, c in enumerate((cards or [])[:2]):
        s.card(mx(700 + i * 205, 190), 438, c[0], c[1], c[2] if len(c) > 2 else "", rot=(-2, 1.5)[i], first=i == 0)
    return s.done(f"{title}: a cut through a hillside; the ball starts at x = {fmt.format(x0)} and stops near x = {fmt.format(path[-1])}.")

# ----------------------------------------------------------------------------- 3. a graph with travelling messages

def message_graph(nodes=None, edges=None, messages=None, uid="graph", title="Messages travel along the edges", no="G-01", note="Each node hears only its neighbours"):
    """nodes: {id: (x, y, label, value)} on a 0..10 x 0..5 grid; edges: [(a, b)]; messages: [(a, b, text)] drawn as envelopes part-way along."""
    nodes = nodes or {"a": (1.5, 1.2, "A", "3"), "b": (4.6, 0.8, "B", "5"), "c": (8.2, 1.4, "C", "2"), "d": (3.0, 3.8, "D", "7"), "e": (6.6, 3.9, "E", "4")}
    edges = edges or [("a", "b"), ("b", "c"), ("a", "d"), ("b", "d"), ("b", "e"), ("c", "e"), ("d", "e")]
    messages = messages or [("a", "b", "3"), ("d", "b", "7"), ("e", "b", "4"), ("c", "b", "2")]
    s = Sheet(uid, title, no=no, kind="Graphs")
    P = lambda k: (110 + nodes[k][0] * 98, 170 + nodes[k][1] * 78)
    s.add(f'<rect x="13" y="60" width="1174" height="470" fill="{s.pat("dots")}" opacity=".5"/>')
    for a, b in edges:
        (x1, y1), (x2, y2) = P(a), P(b)
        s.add(f'<path d="M{f1(x1)} {f1(y1)}L{f1(x2)} {f1(y2)}" stroke="{INK}" stroke-width="5"/><path d="M{f1(x1)} {f1(y1)}L{f1(x2)} {f1(y2)}" stroke="{PAPER}" stroke-width="2" stroke-dasharray="10 8"/>')
    for i, (a, b, t) in enumerate(messages):
        (x1, y1), (x2, y2) = P(a), P(b)
        u = 0.52; mx, my = x1 + (x2 - x1) * u, y1 + (y2 - y1) * u
        ang = math.degrees(math.atan2(y2 - y1, x2 - x1)); d = math.hypot(x2 - x1, y2 - y1)
        ox, oy = -(y2 - y1) / d * 26, (x2 - x1) / d * 26
        s.add(f'<g transform="translate({f1(mx + ox)} {f1(my + oy)})"><rect x="-26" y="-18" width="52" height="36" rx="2" fill="{PAPER}" stroke="{RUST}" stroke-width="2"/><path d="M-26 -18L0 -4L26 -18" fill="none" stroke="{RUST}" stroke-width="2"/></g>')
        s.text(mx + ox, my + oy + 13, t, "lab", size=16, anchor="middle", fill=RUST, key=f"msg-{i}")
        s.arrow(f"M{f1(mx + ox + (x2 - x1) / d * 32)} {f1(my + oy + (y2 - y1) / d * 32)}L{f1(mx + ox + (x2 - x1) / d * 64)} {f1(my + oy + (y2 - y1) / d * 64)}", "r", 2.5)
    hub = max(nodes, key=lambda k: sum(1 for m in messages if m[1] == k))
    for k, (gx, gy, lab, val) in nodes.items():
        x, y = P(k); on = k == hub
        s.add(f'<g stroke="{INK}" stroke-width="2"><path d="M{f1(x - 34)} {f1(y + 26)}V{f1(y - 8)}L{f1(x)} {f1(y - 36)}L{f1(x + 34)} {f1(y - 8)}V{f1(y + 26)}Z" fill="{RUST if on else PEACH}"/>'
              f'<rect x="{f1(x + 6)}" y="{f1(y + 2)}" width="18" height="24" fill="{PAPER}"/><path d="M{f1(x + 18)} {f1(y - 24)}v-22" /><circle cx="{f1(x + 18)}" cy="{f1(y - 50)}" r="5" fill="{PAPER}"/></g>')
        s.text(x - 14, y + 18, lab, "lab", size=18, anchor="middle", fill=PAPER if on else INK, key=f"node-{k}")
        s.add(f'<rect x="{f1(x + 40)}" y="{f1(y - 12)}" width="46" height="30" fill="{PAPER}" stroke="{INK}" stroke-width="1.2"/>')
        s.text(x + 63, y + 9, val, "num", size=20, anchor="middle", key=f"val-{k}")
    hx, hy = P(hub)
    s.callout(40, 70, 330, "1 · a message", ["one number, sent along one edge"])
    s.callout(820, 70, 340, "2 · the listening node", [note], to=(hx + 20, hy - 30), rust=True, side="left")
    s.key += [(1, "A message", "one number sent along one edge"), (2, "The listening node", note)]
    return s.done(f"{title}: {len(nodes)} nodes joined by {len(edges)} edges; {len(messages)} messages are on their way to node {nodes[hub][2]}.")

# ----------------------------------------------------------------------------- 4. a tree being searched

def tree_search(tree=None, uid="tree", title="Searching a tree, one branch at a time", no="S-01", labels=None):
    """tree: {"label", "value", "state": "path" | "seen" | "cut" | "", "children": [...]}. The path is rust, cut branches are dashed and sawn off."""
    tree = tree or {"label": "start", "state": "path", "children": [
        {"label": "left", "value": "3", "state": "seen", "children": [{"label": "", "value": "3", "state": "seen"}, {"label": "", "value": "5", "state": "seen"}]},
        {"label": "middle", "value": "6", "state": "path", "children": [{"label": "", "value": "6", "state": "path"}, {"label": "", "value": "9", "state": "seen"}]},
        {"label": "right", "value": "≤ 2", "state": "cut", "children": [{"label": "", "value": "2", "state": "seen"}, {"label": "", "value": "?", "state": "cut"}]}]}
    L = {"path": "The best line found so far", "cut": "Cut: it cannot beat what we have", "seen": "Looked at and scored"}; L.update(labels or {})
    s = Sheet(uid, title, no=no, kind="Search")
    s.ground(500)
    leaves = []
    def count(n): return sum(count(c) for c in n.get("children", [])) or 1
    def place(n, x0, x1, depth):
        n["_x"] = (x0 + x1) / 2; n["_y"] = 470 - depth * 125
        kids = n.get("children", []); tot = count(n); a = x0
        for c in kids:
            w = (x1 - x0) * count(c) / tot; place(c, a, a + w, depth + 1); a += w
    place(tree, 250, 1150, 0)
    def draw(n, depth):
        for c in n.get("children", []):
            st = c.get("state", ""); col = RUST if st == "path" else INK; wd = max(3, 12 - depth * 4) if st != "cut" else 3
            d = f'M{f1(n["_x"])} {f1(n["_y"])}C{f1(n["_x"])} {f1(n["_y"] - 60)} {f1(c["_x"])} {f1(c["_y"] + 70)} {f1(c["_x"])} {f1(c["_y"])}'
            s.add(f'<path d="{d}" fill="none" stroke="{col if st != "cut" else MUTE}" stroke-width="{wd}" stroke-linecap="round"{" stroke-dasharray=\"3 9\"" if st == "cut" else ""}/>')
            if st == "cut":
                mx, my = (n["_x"] + c["_x"]) / 2, (n["_y"] + c["_y"]) / 2 + 5
                s.add(f'<path d="M{f1(mx - 16)} {f1(my - 10)}l8 6-4 6 8 6-4 6 8 6" fill="none" stroke="{HOLD}" stroke-width="2.5"/>')
            draw(c, depth + 1)
    s.add(f'<path d="M{f1(tree["_x"])} 500V470" stroke="{RUST}" stroke-width="14" stroke-linecap="round"/>')
    draw(tree, 0)
    def marks(n, depth):
        st = n.get("state", ""); x, y = n["_x"], n["_y"]
        if n.get("value") is not None:
            r = 24; hw = max(24, len(str(n["value"])) * 6.5 + 14)
            fill = RUST if st == "path" else PAPER if st != "cut" else SAND
            s.add(f'<rect x="{f1(x - hw)}" y="{f1(y - r)}" width="{f1(2 * hw)}" height="{2 * r}" rx="{r}" fill="{fill}" stroke="{RUST if st == "path" else INK}" stroke-width="2"{" stroke-dasharray=\"4 4\"" if st == "cut" else ""}/>')
            s.text(x, y + 7, n["value"], "num", size=20, anchor="middle", fill=PAPER if st == "path" else INK, key=f"v-{len(leaves)}"); leaves.append(n)
        if n.get("label"): s.text(x + max(24, len(str(n.get("value") or "")) * 6.5 + 14) + 10, y + 6, n["label"].upper(), "cap", size=14, fill=MUTE)
        for c in n.get("children", []): marks(c, depth + 1)
    marks(tree, 0)
    s.person(120, 500, 1.15, arm=(40, -78)); s.add(f'<g stroke="{INK}" stroke-width="2"><path d="M168 410v-22" /><rect x="156" y="364" width="24" height="26" rx="3" fill="{PEACH}"/><path d="M160 364a8 8 0 0 1 16 0" fill="none"/></g>')
    def find(n, st):
        if n.get("state") == st and n.get("value") is not None and not n.get("children"): return n
        for c in n.get("children", []):
            r = find(c, st)
            if r: return r
    p, c, sn = find(tree, "path"), find(tree, "cut"), find(tree, "seen")
    if p: s.callout(max(310, min(p["_x"] - 150, 530)), 62, 300, "1 · the best line", [L["path"]], to=(p["_x"], p["_y"] - 28), rust=True)
    if c: s.callout(850, 62, 310, "2 · cut", [L["cut"]], to=(c["_x"], c["_y"] - 28))
    if sn: s.callout(40, 62, 250, "3 · scored", [L["seen"]], to=(sn["_x"] - 6, sn["_y"] - 26))
    s.key += [k for k, show in (((1, "The best line", L["path"]), p), ((2, "Cut", L["cut"]), c), ((3, "Scored", L["seen"]), sn)) if show]
    return s.done(f"{title}. {L['path']}. {L['cut']}.")

# ----------------------------------------------------------------------------- 5. a game table with two players

def game_table(rows=("Cooperate", "Defect"), cols=("Cooperate", "Defect"), cells=(("3, 3", "0, 5"), ("5, 0", "1, 1")), stable=(1, 1),
               players=("Row player", "Column player"), uid="game", title="Two players, one table", no="M-01", note="Neither gains by moving alone"):
    """Two figures at a table seen from the side; the pay-off grid lies on the table top, drawn tilted like a card; the stable cell is rust."""
    s = Sheet(uid, title, no=no, kind="Games")
    s.ground(500, fill="dots")
    s.add(f'<g stroke="{INK}" stroke-width="2"><rect x="330" y="372" width="540" height="18" fill="{TAN}"/><path d="M370 390V500M830 390V500" stroke-width="8" stroke="{ESP}"/><path d="M350 430H850" stroke-width="3"/></g>')
    s.person(250, 500, 1.6, arm=(46, -44)); s.person(950, 500, 1.6, body=TAUPE, face=-1, arm=(46, -44))
    s.text(250, 548, players[0].upper(), "cap", anchor="middle", key="p1"); s.text(950, 548, players[1].upper(), "cap", anchor="middle", key="p2")
    # the grid, tilted on the table top
    gx, gy, cw, ch = 400, 110, 190, 96
    s.add(f'<g transform="rotate(-1.5 600 230)"><rect x="{gx - 8}" y="{gy - 44}" width="{cw * 2 + 30}" height="{ch * 2 + 62}" fill="{INK}" opacity=".12" transform="translate(4 5)"/><rect x="{gx - 12}" y="{gy - 48}" width="{cw * 2 + 30}" height="{ch * 2 + 62}" fill="{PAPER}" stroke="{LINE}"/>')
    for j, c in enumerate(cols): s.text(gx + cw * (j + .5), gy - 20, c.upper(), "cap", size=14, anchor="middle", fill=MUTE, key=f"col-{j}")
    for i, r in enumerate(rows):
        for j in range(len(cols)):
            on = (i, j) == tuple(stable)
            s.add(f'<rect x="{gx + cw * j}" y="{gy + ch * i}" width="{cw - 6}" height="{ch - 6}" fill="{RUST if on else SAND}" stroke="{INK}" stroke-width="{2 if on else 1}"/>')
            s.text(gx + cw * j + (cw - 6) / 2, gy + ch * i + 44, cells[i][j], "num", size=30, anchor="middle", fill=PAPER if on else INK, key=f"cell-{i}-{j}")
            s.text(gx + cw * j + (cw - 6) / 2, gy + ch * i + 72, r, "lab", size=14, anchor="middle", fill=PAPER if on else MUTE, key=f"row-{i}-{j}")
    s.add("</g>")
    sx, sy = gx + cw * stable[1] + cw / 2, gy + ch * stable[0] + ch / 2
    s.add(f'<path d="M{gx + 100} 372L{gx + 60} {gy + ch * 2 + 12}M{gx + cw * 2 - 80} 372L{gx + cw * 2 - 40} {gy + ch * 2 + 12}" stroke="{MUTE}" stroke-width="1.2" stroke-dasharray="4 4"/>')
    s.arrow(f"M300 395C330 330 360 300 {gx - 20} {gy + ch * stable[0] + 40}", "m", 2, dash="6 5")
    s.arrow(f"M900 395C870 330 850 300 {gx + cw * 2 + 22} {gy + ch * stable[0] + 40}", "m", 2, dash="6 5")
    s.callout(60, 96, 250, "1 · each chooses alone", [f"{players[0]} picks a row", f"{players[1]} picks a column"])
    s.callout(880, 96, 270, "2 · where they settle", [note, f"pay-offs {cells[stable[0]][stable[1]]}"], to=(sx + 60, sy), rust=True, side="left")
    s.key += [(1, "Each chooses alone", f"{players[0]} picks a row; {players[1]} picks a column"), (2, "Where they settle", f"{note}: pay-offs {cells[stable[0]][stable[1]]}")]
    return s.done(f"{title}: {players[0]} and {players[1]} at a table with a {len(rows)} by {len(cols)} pay-off grid; the stable cell pays {cells[stable[0]][stable[1]]}.")

# ----------------------------------------------------------------------------- 6. a particle path under a force field

def particle_field(force=None, start=(1.0, 4.0), v0=(1.6, 0.0), dt=0.05, steps=150, uid="field", title="A path bent by a field", no="P-01",
                   xr=(0, 10), yr=(0, 6), labels=None, target=None):
    """force(x, y) -> (fx, fy). The path is integrated here (semi-implicit Euler), so what is drawn is what the rule gives."""
    force = force or (lambda x, y: (0.0, -0.9))
    L = {"start": "Released here", "field": "The field pushes the same way everywhere", "path": "The path the rule gives", "end": "Lands here"}; L.update(labels or {})
    s = Sheet(uid, title, no=no, kind="Dynamics")
    X = lambda x: 80 + (x - xr[0]) / (xr[1] - xr[0]) * 1040
    Y = lambda y: 520 - (y - yr[0]) / (yr[1] - yr[0]) * 440
    s.add(f'<rect x="80" y="80" width="1040" height="440" fill="{PAGE}" stroke="{INK}" stroke-width="1.5"/><rect x="80" y="80" width="1040" height="440" fill="{s.pat("grid")}"/>')
    for i in range(11):
        for j in range(6):
            x, y = xr[0] + (xr[1] - xr[0]) * (i + .5) / 11, yr[0] + (yr[1] - yr[0]) * (j + .5) / 6
            fx, fy = force(x, y); m = math.hypot(fx, fy) or 1; k = 26 * min(1, m) / m
            s.arrow(f"M{f1(X(x) - fx * k / 2)} {f1(Y(y) + fy * k / 2)}L{f1(X(x) + fx * k / 2)} {f1(Y(y) - fy * k / 2)}", "m", 1.6)
    x, y = start; vx, vy = v0; pts = [(x, y)]
    for _ in range(steps):
        fx, fy = force(x, y); vx += fx * dt; vy += fy * dt; x += vx * dt; y += vy * dt
        if not (xr[0] <= x <= xr[1] and yr[0] <= y <= yr[1]): break
        pts.append((x, y))
    s.add(f'<polyline points="{" ".join(f"{f1(X(a))},{f1(Y(b))}" for a, b in pts)}" fill="none" stroke="{RUST}" stroke-width="4" stroke-linecap="round" stroke-linejoin="round"/>')
    for i in range(0, len(pts), max(1, len(pts) // 6)):
        s.add(f'<circle cx="{f1(X(pts[i][0]))}" cy="{f1(Y(pts[i][1]))}" r="6" fill="{PAPER}" stroke="{RUST}" stroke-width="2.5"/>')
    sx, sy = X(pts[0][0]), Y(pts[0][1]); ex, ey = X(pts[-1][0]), Y(pts[-1][1])
    s.add(f'<circle cx="{f1(sx)}" cy="{f1(sy)}" r="15" fill="{RUST}" stroke="{INK}" stroke-width="2"/><circle cx="{f1(ex)}" cy="{f1(ey)}" r="15" fill="{ESP}"/>')
    s.arrow(f"M{f1(sx)} {f1(sy)}L{f1(sx + v0[0] * 50)} {f1(sy - v0[1] * 50)}", "i", 3)
    if target: s.add(f'<g stroke="{INK}" stroke-width="2"><path d="M{f1(X(target[0]))} {f1(Y(target[1]))}v-56" stroke-width="3"/><path d="M{f1(X(target[0]))} {f1(Y(target[1]) - 56)}h40l-9 11 9 11h-40z" fill="{RUST}"/></g>')
    mid = pts[len(pts) // 2]
    s.callout(sx - 60, sy + 50, 230, "1 · start", [L["start"], f"speed ({v0[0]:g}, {v0[1]:g})"], to=(sx, sy + 18))
    s.callout(X(mid[0]) + 40, Y(mid[1]) - 130, 300, "2 · the path", [L["path"]], to=(X(mid[0]) + 6, Y(mid[1]) - 6), rust=True)
    s.callout(820, 96, 290, "3 · the field", [L["field"]], to=None)
    s.callout(min(ex + 50, 850), max(ey - 120, 300), 260, "4 · end", [L["end"], f"({pts[-1][0]:.2f}, {pts[-1][1]:.2f}) after {len(pts) - 1} steps"], to=(ex + 12, ey - 10), side="left")
    s.key += [(1, "Start", f"{L['start']}, speed ({v0[0]:g}, {v0[1]:g})"), (2, "The path", L["path"]), (3, "The field", L["field"]), (4, "End", f"{L['end']}: ({pts[-1][0]:.2f}, {pts[-1][1]:.2f})")]
    sc = s.done(f"{title}: a particle released at ({start[0]:g}, {start[1]:g}) follows a curved path to ({pts[-1][0]:.2f}, {pts[-1][1]:.2f}).")
    sc.path = pts; return sc

# ----------------------------------------------------------------------------- 7. a market with buyers and sellers

def market(sellers=(("Seller A", 4), ("Seller B", 6), ("Seller C", 9)), buyers=(("Buyer 1", 10), ("Buyer 2", 7), ("Buyer 3", 5)), price=None,
           uid="market", title="Buyers and sellers meet at one price", no="E-01", unit="$"):
    """Stalls on the left (each seller's lowest price), buyers on the right (each buyer's highest price), a price board between them.
    The clearing price is worked out here: the midpoint of the last pair that still trades."""
    S = sorted(sellers, key=lambda t: t[1]); B = sorted(buyers, key=lambda t: -t[1])
    k = sum(1 for a, b in zip(S, B) if b[1] >= a[1])
    if price is None: price = (S[k - 1][1] + B[k - 1][1]) / 2 if k else None
    s = Sheet(uid, title, no=no, kind="Markets")
    s.ground(480, fill="dots")
    for i, (name, ask) in enumerate(S):
        x = 70 + i * 150; on = i < k
        s.add(f'<g stroke="{INK}" stroke-width="2" stroke-linejoin="round"><path d="M{x} 480V330M{x + 120} 480V330" stroke-width="4"/><path d="M{x - 12} 330h144l-14-40h-116z" fill="{RUST if on else TAUPE}"/>'
              f'<path d="M{x + 22} 290v40M{x + 60} 290v40M{x + 98} 290v40" stroke="{PAPER}" stroke-width="2"/><rect x="{x}" y="420" width="120" height="14" fill="{TAN}"/>'
              f'<circle cx="{x + 30}" cy="410" r="10" fill="{PEACH}"/><circle cx="{x + 56}" cy="410" r="10" fill="{PEACH}"/><circle cx="{x + 43}" cy="394" r="10" fill="{PEACH}"/></g>')
        s.person(x + 92, 480, .9)
        s.add(f'<rect x="{x + 14}" y="232" width="92" height="46" fill="{PAPER}" stroke="{INK}" stroke-width="1.2"/>')
        s.text(x + 60, 252, name.upper(), "cap", size=14, anchor="middle", fill=MUTE, key=f"seller-{i}"); s.text(x + 60, 272, f"≥ {unit}{ask:g}", "lab", size=16, anchor="middle", key=f"ask-{i}")
    for i, (name, bid) in enumerate(B):
        x = 760 + i * 140; on = i < k
        s.person(x + 40, 480, 1.25, body=PEACH if on else TAUPE, face=-1, arm=(34, -30))
        s.add(f'<g stroke="{INK}" stroke-width="2"><path d="M{x - 18} 428h30l-5 26h-20z" fill="{TAN}"/><path d="M{x - 14} 428a11 12 0 0 1 22 0" fill="none"/></g>')
        s.add(f'<rect x="{x - 6}" y="322" width="92" height="46" fill="{PAPER}" stroke="{INK}" stroke-width="1.2"/>')
        s.text(x + 40, 342, name.upper(), "cap", size=14, anchor="middle", fill=MUTE, key=f"buyer-{i}"); s.text(x + 40, 362, f"≤ {unit}{bid:g}", "lab", size=16, anchor="middle", key=f"bid-{i}")
    s.add(f'<g stroke="{INK}" stroke-width="2"><path d="M600 480V250" stroke-width="5"/><rect x="520" y="150" width="160" height="104" fill="{ESP}"/></g>')
    s.text(600, 180, "PRICE TODAY", "cap", size=14, anchor="middle", fill=PEACH, key="board"); s.text(600, 226, f"{unit}{price:g}" if price is not None else "no trade", "num", size=40, anchor="middle", fill=PAGE, key="price")
    if k:
        s.arrow(f"M{70 + (k - 1) * 150 + 130} 380C520 360 620 400 {760 - 30} 430", "r", 2.5, dash="8 6")
    s.callout(60, 76, 300, "1 · sellers", ["each has a lowest price", f"{k} of {len(S)} sell at {unit}{price:g}" if k else "none can sell"])
    s.callout(840, 76, 300, "2 · buyers", ["each has a highest price", f"{k} of {len(B)} buy at {unit}{price:g}" if k else "none will buy"])
    s.callout(420, 76, 360, "3 · one price", [f"{k} trades happen; one more would lose money" if k < min(len(S), len(B)) else f"all {k} pairs trade"], to=(600, 150), rust=True)
    s.key += [(1, "Sellers", f"lowest prices {', '.join(f'{unit}{a:g}' for _, a in S)}"), (2, "Buyers", f"highest prices {', '.join(f'{unit}{b:g}' for _, b in B)}"),
              (3, "One price", f"{unit}{price:g} clears {k} trades" if k else "no price clears a trade")]
    sc = s.done(f"{title}: {len(S)} sellers and {len(B)} buyers; {k} trades at {unit}{price:g}." if k else f"{title}: no trade.")
    sc.price, sc.trades = price, k; return sc

# ----------------------------------------------------------------------------- 8. a pipeline from data to model to decision

def pipeline(stages=None, uid="pipe", title="From data to a model to a decision", no="L-01", cards=None):
    """A plant on a ground line: a store of data, a sieve that cleans it, a machine that fits the model, a gauge that tests it, a person who decides.
    stages: five (caps title, line 1, line 2) triples; the default words name each part."""
    stages = stages or [("Data", "what was recorded", "rows, images, logs"), ("Clean", "drop what is broken", "split off a test set"), ("Fit", "adjust the model", "to lower the error"),
                        ("Test", "score on held-back data", "never the training rows"), ("Decide", "a person acts", "on the checked answer")]
    s = Sheet(uid, title, no=no, kind="Learning")
    gy = 430; s.ground(gy)
    s.add(f'<g stroke="{INK}" stroke-width="2"><rect x="60" y="{gy - 26}" width="1010" height="12" fill="{TAUPE}"/>' + "".join(f'<circle cx="{80 + i * 66}" cy="{gy - 8}" r="8" fill="{PAPER}"/>' for i in range(16)) + "</g>")
    # 1 data silo
    s.add(f'<g stroke="{INK}" stroke-width="2" stroke-linejoin="round"><path d="M80 {gy - 26}V230q60-40 120 0V{gy - 26}z" fill="{PEACH}"/><path d="M80 270q60 30 120 0M80 320q60 30 120 0M80 370q60 30 120 0" fill="none"/>'
          f'<path d="M200 300h46v60" fill="none" stroke-width="6"/></g>' + "".join(f'<rect x="{232 + (i % 2) * 14}" y="{gy - 48 - (i // 2) * 14}" width="12" height="12" fill="{RUST if i == 3 else TAN}" stroke="{INK}"/>' for i in range(4)))
    # 2 sieve
    s.add(f'<g stroke="{INK}" stroke-width="2"><path d="M310 250h130l-24 74h-82z" fill="{PAPER}"/><path d="M322 286h106" stroke-dasharray="5 4"/><path d="M334 324v40h82v-40" fill="none"/>'
          f'<path d="M440 300h40v70" fill="none" stroke="{MUTE}" stroke-dasharray="4 4"/><rect x="462" y="370" width="36" height="{gy - 26 - 370}" fill="{SAND}"/></g>'
          + "".join(f'<rect x="{352 + i * 18}" y="{gy - 44}" width="12" height="12" fill="{TAN}" stroke="{INK}"/>' for i in range(3)))
    # 3 the machine that fits
    s.add(f'<g stroke="{INK}" stroke-width="2" stroke-linejoin="round"><rect x="540" y="230" width="200" height="{gy - 26 - 230}" rx="6" fill="{ESP}"/><rect x="560" y="250" width="160" height="92" rx="3" fill="{PAPER}"/>'
          f'<path d="M572 272l30 40 24-18 30 26 52-56" fill="none" stroke="{RUST}" stroke-width="3"/><circle cx="590" cy="372" r="14" fill="{PEACH}"/><path d="M590 372l8-9"/><circle cx="640" cy="372" r="14" fill="{PEACH}"/><path d="M640 372l-3-12"/>'
          f'<path d="M700 230v-36h-30" fill="none" stroke-width="5"/><path d="M660 180c-8-12 6-16 0-28M676 176c-8-12 6-16 0-28" fill="none" stroke="{MUTE}"/></g>')
    # 4 the gauge
    s.add(f'<g stroke="{INK}" stroke-width="2"><path d="M850 {gy - 26}V330" stroke-width="5"/><circle cx="850" cy="290" r="52" fill="{PAPER}"/><path d="M812 304A40 40 0 0 1 888 304" fill="none" stroke="{MUTE}" stroke-width="8"/>'
          f'<path d="M866 268A40 40 0 0 1 888 304" fill="none" stroke="{RUST}" stroke-width="8"/><path d="M850 300L874 272" stroke-width="4" stroke-linecap="round"/><circle cx="850" cy="300" r="6" fill="{INK}"/></g>')
    # 5 the person and the signpost
    s.person(1010, gy, 1.3, arm=(40, -70))
    s.add(f'<g stroke="{INK}" stroke-width="2"><path d="M1110 {gy}V250" stroke-width="5"/><path d="M1110 262h56l12 14-12 14h-56z" fill="{RUST}"/><path d="M1110 306h-50l-12 14 12 14h50z" fill="{PEACH}"/></g>')
    xs = [60, 290, 520, 760, 950]; ws = [200, 210, 220, 180, 200]; tos = [(140, 232), (375, 250), (640, 230), (850, 240), (1010, gy - 100)]
    for i, (t, a, b) in enumerate(stages[:5]):
        s.callout(xs[i], 78, ws[i], f"{i + 1} · {t}", [a, b], to=tos[i], rust=i == 2)
        s.key.append((i + 1, t, f"{a}; {b}"))
        if i < 4: s.arrow(f"M{xs[i] + ws[i] + 4} 110H{xs[i + 1] - 6}", "r", 2)
    for i, c in enumerate((cards or [])[:3]):
        s.card(70 + i * 215, 438, c[0], c[1], c[2] if len(c) > 2 else "", rot=(-2, 1.5, -1)[i], first=i == 0)
    return s.done(f"{title}: " + "; ".join(f"{i + 1} {t}, {a}" for i, (t, a, b) in enumerate(stages[:5])) + ".")


BUILDERS = {"control_loop": control_loop, "landscape": landscape, "message_graph": message_graph, "tree_search": tree_search,
            "game_table": game_table, "particle_field": particle_field, "market": market, "pipeline": pipeline}

if __name__ == "__main__":
    import sys
    out = Path(sys.argv[1] if len(sys.argv) > 1 else ".")
    for name, fn in BUILDERS.items():
        (out / f"{name}.svg").write_text(fn().svg.replace("<svg ", '<svg xmlns="http://www.w3.org/2000/svg" ', 1))
        print(name)
