#!/usr/bin/env python3
"""Write kit/gallery.html: every kit component with a live example and the markup that makes it.

    python3 kit/tools/build_gallery.py
"""
from __future__ import annotations
import json, sys
from pathlib import Path

KIT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(KIT)); sys.path.insert(0, str(KIT / "demo"))
import render_lecture as R  # noqa: E402
import build as D           # noqa: E402  (the demo's drawings double as chart examples)

esc = R.esc


def block(n, name, use, example, note=""):
    return (f'<section class="ck-sec" id="c{n}"><div class="rs-sh"><p class="eb">{n:02d} · component</p><h2 class="rs-h2" style="font-size:28px">{esc(name)}</h2>'
            f'<p class="rs-in" style="font-size:16px">{use}</p></div>{example}' + (f'<p class="ck-cap">{note}</p>' if note else "") + "</section>")


def chart(spec, panel, chip="illustration", caption=""):
    return R.panel_html({"panel": panel, "chip": chip, "chart": spec, "caption": caption})


def dp_grid():
    """Cost-to-go on a 4 x 4 grid, one sweep per frame (each move costs 1; one wall)."""
    Rn, Cn, goal, wall = 4, 4, (3, 3), {(1, 1), (2, 1)}
    INF = 99
    V = [[INF] * Cn for _ in range(Rn)]; V[goal[0]][goal[1]] = 0
    frames = []
    for sweep in range(8):
        cells = []
        for i in range(Rn):
            row = []
            for j in range(Cn):
                if (i, j) in wall: row.append({"s": "wall"}); continue
                if (i, j) == goal: row.append({"v": 0, "s": "goal"}); continue
                best, arrow = INF, None
                for a, (di, dj) in {"r": (0, 1), "d": (1, 0), "l": (0, -1), "u": (-1, 0)}.items():
                    y, x = i + di, j + dj
                    if 0 <= y < Rn and 0 <= x < Cn and (y, x) not in wall and V[y][x] + 1 < best: best, arrow = V[y][x] + 1, a
                row.append({"v": V[i][j], "a": arrow, "s": "path"} if V[i][j] < INF else {"v": "·", "s": "empty"})
            cells.append(row)
        known = sum(1 for i in range(Rn) for j in range(Cn) if V[i][j] < INF and (i, j) not in wall)
        frames.append({"cells": cells, "reads": [{"label": "sweeps done", "value": str(sweep)}, {"label": "states with a known cost", "value": f"{known} of 14"}]})
        W = [r[:] for r in V]
        for i in range(Rn):
            for j in range(Cn):
                if (i, j) in wall or (i, j) == goal: continue
                for di, dj in ((0, 1), (1, 0), (0, -1), (-1, 0)):
                    y, x = i + di, j + dj
                    if 0 <= y < Rn and 0 <= x < Cn and (y, x) not in wall: W[i][j] = min(W[i][j], V[y][x] + 1)
        V = W
    return {"type": "grid", "title": "Cost-to-go on a small grid, filled in sweep by sweep",
            "desc": "A 4 by 4 grid with a goal in one corner and a wall of two cells. Each sweep fills in the states one move further from the goal with their cost and the move to take.",
            "frames": frames, "slider": {"label": "Sweep", "min": 0, "max": 7, "step": 1, "value": 3, "decimals": 0},
            "legend": [{"name": "goal", "cls": "f-rust", "mark": "box"}, {"name": "wall", "cls": "f-esp", "mark": "box"}, {"name": "cost known, with the move to take", "cls": "f-soft s thin s-ink", "mark": "box"}]}


def gallery(kit=".", home="demo/index.html", phone_src=None):
    v1, v2 = D.visuals_01(), D.visuals_02()
    idx = json.loads((KIT / "glyphs" / "index.json").read_text()) + json.loads((KIT / "glyphs" / "course.json").read_text())
    parts = []
    cards = [{"label": "Components", "value": "17 pieces", "note": "each with a live example"}, {"label": "Drawings", "value": f"{len(idx)} glyphs", "note": "the boards' own, plus 8 new"},
             {"label": "Charts", "value": "12 builders", "note": "data in, SVG out"}, {"label": "Runtime", "value": "0 requests", "note": "fonts and scripts are local"}]
    parts.append(R.hero_html("Course kit · gallery", "k.", "Signal Desk look · from the boards", "Course kit",
                             "Every piece of a course page, shown working. <i>Copy the markup under each one.</i>",
                             "Taken from the Sense to Silicon and Atom to Answer boards: their stylesheet, their drawings, their type and colour tokens.", cards, home=home))
    parts.append('<main id="main" style="display:contents">')
    parts.append(R.strip_html([{"label": "Styles", "value": "`tokens.css`, `boards.css`, `course.css`"}, {"label": "Scripts", "value": "`charts.js`, `course.js`"},
                               {"label": "Generator", "value": "`render_lecture.py`"}, {"label": "Themes", "value": "light and dark"}], "Gallery"))
    n = 0
    def add(name, use, example, note=""):
        nonlocal n; n += 1; parts.append(block(n, name, use, example, note))

    add("Opening band, with number cards and threads", "<code>R.hero_html(brand, mark, right, eyebrow, h1, lede, cards)</code>. The headline's second sentence is the answer, in <code>&lt;i&gt;</code>. Up to four cards, each with one real number; the first has the rust edge.",
        '<div style="margin:0 calc(-1*var(--rs-px))">' + R.hero_html("Stanford AA203", "a.", "Lecture 2 · Optimization Theory", "Lecture 2 · one question, 8 ideas",
                                                                   'How do you find the lowest point? <i>Walk downhill until every slope is zero.</i>', "… and a constraint adds one extra unknown per condition.", v2["cards"]).replace("<header", "<div").replace("</header>", "</div>").replace('class="rs-hero"', 'class="rs-hero" style="margin:0"') + "</div>",
        "This is the band at the top of this page too. On a phone the cards become a two-by-two grid and the threads are dropped.")
    add("Context strip", "<code>R.strip_html([{label, value}], crumb)</code>. What the reader should know about the page before reading it: course, lecturer, where the numbers come from, what is needed.",
        R.strip_html(v2["context"], "Lecture 2 of 4"))
    rail = "".join(f'<li><a href="#c{i + 1}"><span class="lab">Idea {i + 1} of 5</span><span>{t}</span></a></li>' for i, t in enumerate(
        ["At a minimum, no small move can lower the function", "Zero slope is a filter, not a proof", "For a bowl-shaped function, the test settles the global question", "A small step against the gradient always lowers the function", "The Lagrangian turns the constrained test into an ordinary one"]))
    add("Argument rail", "<code>&lt;ol class=\"ck-rail\"&gt;</code>. The lesson's ideas as headings that carry the point, in order. Each links to its plate; the one on screen is marked.",
        f'<ol class="ck-rail">{rail}</ol>')
    plate = ('<section class="ck-plate" style="border-top:0;padding-top:0"><div class="ck-prose"><p class="eb">Idea 4 of 8</p>'
             f'<h2 class="rs-h2">{R.turn_html("A small step against the gradient always lowers the function")}</h2>'
             '<p class="ck-point">Moving a short way opposite the gradient reduces f by about the step size times the squared length of the gradient.</p>'
             '<p>The formula tempts you. A bigger α seems to lower f more. The lecturer asks why not choose α equal to a million. The answer is in the first step. The approximation holds only close to x.</p>'
             + R.block_html({"type": "eq", "text": "x(α) = x − α ∇f(x)"}) + "</div><div class=\"ck-side\">" + R.panel_html(v2["ideas"]["4"]) + "</div></section>")
    add("Idea plate", "<code>&lt;section class=\"ck-plate\"&gt;</code> with <code>.ck-prose</code> and <code>.ck-side</code>. The heading states the idea, the italic line under it is the point, and the panel beside the prose shows the mechanism. The panel stays in view while the prose scrolls.", plate)
    add("Panel with header and source chip", "<code>R.panel_html({panel, chip, glyph | chart | svg | tiles, caption})</code>. A label bar says what the picture is; the chip says where its numbers come from.",
        '<div class="g3">' + R.panel_html({"panel": "A drawing from the boards", "chip": "from the lecture", "glyph": "filled/network", "caption": "A filled glyph in a sand tile."})
        + R.panel_html({"panel": "A line drawing", "chip": "illustration", "glyph": "line/dna", "caption": "One of the 41 problem drawings."})
        + R.panel_html({"panel": "A drawing made for the course", "chip": "our check", "glyph": "course/bowl", "caption": "Drawn for Lecture 2, in the boards' hand."}) + "</div>")
    chips = "".join(f'<span class="t {c}">{t}</span>' for t, c in [("from the lecture", "t-le"), ("worked out", "t-wo"), ("our check", "t-oc"), ("assumed", "t-as"), ("illustration", "t-il"), ("missing", "t-mi"), ("verified", "t-ve"), ("measured", "t-me"), ("simulated", "t-si")])
    add("Evidence chips", "<code>&lt;span class=\"t t-le\"&gt;</code>. The boards' set (assumed, worked out, missing, verified, measured, simulated) plus three a lesson needs: from the lecture, our check, illustration. Each differs by border style as well as colour.",
        f'<div class="tags">{chips}</div>')
    add("Equation, reasoning steps and the Be careful line", "<code>.ck-eq</code>, <code>ol.ck-steps</code>, <code>p.ck-careful</code>. The boards show an equation as a dark block with its words beside it.",
        '<div class="ck-wide">' + R.block_html({"type": "eq", "text": "∇f(x*) + λ₁ ∇h₁(x*) + … + λₘ ∇hₘ(x*) = 0"})
        + R.block_html({"type": "steps", "items": ["**Approximate.** For a small move, f(x* + Δx) ≈ f(x*) + ∇f(x*) · Δx.", "**Use the definition.** At a local minimum, nearby points are no lower.", "**Compare.** The slope is at least zero and at most zero. Only zero is both."]})
        + R.block_html({"type": "careful", "text": "The approximation in the first step only holds for small moves. The whole argument is local. It says nothing about far-away points."}) + "</div>")
    add("Worked-example ledger", "<code>R.ledger_html({title, kind, lines})</code>. One line per step, numbered, with the result line marked. <code>kind</code> sets the chip: lecture, illustration (dashed top edge) or filled (worked out).",
        '<div class="g2">' + R.ledger_html({"kind": "lecture", "title": "The lecture's example: minimise x₁ + x₂ on the circle", "lines": ["Gradient of f: (1, 1). Gradient of h: (2x₁, 2x₂).", "The theorem gives two equations: 1 + 2λx₁ = 0 and 1 + 2λx₂ = 0.", "Two solutions: λ = 1/2 or λ = −1/2.", "The lower cost is −2, so the minimum is at (−1, −1)."]})
        + R.ledger_html({"kind": "illustration", "title": "A good step and a step that is too large", "lines": ["Start at (3, 4). There f = 3² + 4² = 25 and the gradient is (6, 8).", "Step with α = 0.1: new point (2.4, 3.2).", "Formula predicts: 25 − 0.1 × 100 = 15. Actual: 2.4² + 3.2² = 16. Close, and lower."]}) + "</div>")
    add("Check-yourself reveals", "<code>&lt;details class=\"ck-reveal\"&gt;</code>. The question is always visible; the answer opens on click, Enter or Space.",
        '<div style="display:flex;flex-direction:column;gap:10px"><details class="ck-reveal"><summary><span class="rs-n">1</span><span>The function f(x) = x³ has zero slope at x = 0. Is that point a local minimum?</span></summary><div>No. Just to the left of zero the function is negative, so nearby points are lower. Zero slope is necessary, not sufficient.</div></details>'
        '<details class="ck-reveal" open><summary><span class="rs-n">2</span><span>In the six-step derivation, why are two moves needed, one by ε and one by −ε?</span></summary><div>One move only shows the slope is at least zero. The opposite move shows it is at most zero. Both together leave zero as the only value.</div></details></div>')
    add("Lecture index rows", "<code>&lt;a class=\"ck-lec\"&gt;</code>. A drawing, the question, the answer in one line, and where it leads. A lecture not yet written is a dashed row with a missing chip.",
        f'<div><a class="ck-lec" href="#c{n + 1}"><div class="ck-tile">{R.glyph("course/bowl")}</div><div class="q"><span class="rs-k">Lecture 2 · Optimization Theory</span><b>How can you tell that a point is the lowest one, and how do you find such a point?</b></div><p class="a">At a lowest point no small allowed move makes things better, which forces the slopes to zero.</p><span class="go">8 ideas →</span></a>'
        '<div class="ck-lec todo"><div class="ck-tile"></div><div class="q"><span class="rs-k">Lecture 5</span><b>Not written yet</b></div><p class="a">Promised for the next lecture.</p><span class="t t-mi">missing</span></div></div>')
    three = "".join(f"<li><em>{i}</em><b>{b}</b><span>{s}</span></li>" for i, b, s in [(1, "Every method solves one problem.", "A model, constraints and a cost, stated once."), (2, "First for a few numbers.", "The zero-slope test, then constraints."), (3, "Then for a whole curve.", "The same test becomes a differential equation.")])
    tl = "".join(f'<div class="tli"><span class="rs-disc {c}">{k}</span><b>{b}</b><span>{s}</span></div>' for k, c, b, s in [(1, "d", "The problem", "stated"), (2, "d", "A few numbers", "solved"), (3, "", "A whole curve", "this lecture"), (4, "o", "With dynamics", "next")])
    doors = "".join(f'<a class="card ck-door" href="#c{n + 1}"><div class="rs-pic">{R.glyph(g)}</div><p class="rs-k">{k}</p><h3>{h}</h3><p class="rs-ans">{a}</p></a>' for g, k, h, a in [
        ("course/loop", "Lecture 1", "What is the problem?", "One cost number, made small."), ("course/bowl", "Lecture 2", "Where is the lowest point?", "Where every slope is zero."),
        ("course/paths", "Lecture 3", "Which curve is best?", "The one the Euler equation picks."), ("course/costate", "Lecture 4", "What if dynamics tie it down?", "Attach a costate.")])
    add("Course landing sections", "<code>ol.ck-three</code> (the course in three sentences), <code>.tl</code> inside <code>.ck-path</code> (the path, joined by a dashed line; filled disc = done, peach = here, dashed = not yet), and <code>a.card.ck-door</code> (doors, each with its own drawing).",
        f'<ol class="ck-three">{three}</ol><div class="ck-path"><div class="tl" style="--n:4">{tl}</div></div><div class="g4">{doors}</div>')
    concept = ('<div class="ck-concept"><div><article class="card"><p class="rs-k">Concept · from Lecture 2</p><h3 style="font-size:26px">Lagrange multiplier</h3><p class="mut">One extra unknown per constraint, chosen so the cost gradient is built from the constraint gradients.</p></article>'
               + R.block_html({"type": "eq", "text": "∇f(x*) + λ ∇h(x*) = 0"})
               + '<article class="card"><p class="lab">In words</p><p>At a constrained minimum, the gradient of f equals a weighted sum of the constraint gradients, and the weights are new unknowns.</p></article>'
               '<article class="card"><p class="lab">Be careful</p><p>The condition finds stationary points. It does not separate a minimum from a maximum.</p></article>'
               '<article class="card"><p class="lab">Where it returns</p><p>The costate of Lecture 4 is this multiplier attached to the dynamics constraint.</p></article></div><div>'
               + R.panel_html(v2["ideas"]["6"]) + "</div></div>")
    add("Concept page", "<code>.ck-concept</code>: the boards' concept template. Left: the name, the equation, its words, the caution, where it returns. Right: one diagram drawn from a real example.", concept)
    add("Sources list", "<code>ul.ck-sources</code> or <code>p.rs-src</code>. A 2 px rule, then every source the page used, in the label face.",
        '<ul class="ck-sources"><li>Marco Pavone, "Stanford AA203: Optimal and Learning-Based Control, Spring 2026, Lecture 2: Optimization Theory". Stanford Online, YouTube.</li><li>This page was written from the full caption transcript of that video.</li><li>No outside reading was used. The boxes marked as illustrations use made-up numbers to show a step.</li></ul>')
    slide = ('<div class="ck-stage"><article class="ck-slide"><header><span>Stanford AA203 · Lecture 2</span><span>04 / 08</span></header><p class="eb">One step against the gradient</p>'
             '<h2>A small step lowers f. <i>A big one may not.</i></h2><div class="body"><div>' + R.glyph("course/bowl") + '</div><div style="display:flex;flex-direction:column;gap:18px">'
             '<p class="big" style="margin:0">25 → 16</p><p style="margin:0">From (3, 4) with α = 0.1. With α = 1 the step lands at (−3, −4), where f is 25 again.</p><span class="t t-il">illustration</span></div></div>'
             '<footer><span>The formula 25 − α × 100 trusts the slope at the start. Far away it tells you nothing about f.</span><b>How do you find the lowest point?</b></footer></article></div>')
    add("Slide frame, 1920 × 1080", "<code>.ck-stage &gt; article.ck-slide</code>. The slide is laid out at 1920 × 1080 and scaled to its stage by <code>course.js</code>. Same band, same headline with its italic turn, one paper body, a source line.", slide)
    if phone_src:
        add("Phone layout", "Every component above reflows at 390 px: one column, the panel under its prose, cards two by two, rows stacked. This frame shows a demo lecture at phone width.",
            f'<div style="display:flex;justify-content:center"><iframe src="{esc(phone_src)}" title="A demo lecture at phone width" loading="lazy" style="width:390px;max-width:100%;height:760px;border:1.5px solid var(--line-strong);border-radius:22px;background:var(--page)"></iframe></div>')
    # drawings
    kinds = [("line", "The 41 problem drawings (Atom to Answer, As33Gallery): 2.5 px ink outline, one rust fill.", "ln"), ("filled", "Filled glyphs for sand tiles (Sense to Silicon and Atom to Answer boards).", ""),
             ("course", "Drawn for the course kit in the same hand: one per lecture door, one per disturbance model.", ""), ("spot", "Mechanism sketches with labels (Atom to Answer, As20Domains).", ""),
             ("mini", "Small filled marks, 40 and 52 grids (Sense to Silicon, Ch1CameraChallenge).", ""), ("icons", "Line icons on 24 and 40 grids; they take the text colour.", "")]
    gal = ""
    for kind, text, cls in kinds:
        figs = "".join(f'<figure class="{cls}"><div>{(KIT / "glyphs" / g["file"]).read_text()}</div><figcaption>{g["kind"]}/{g["name"]}</figcaption></figure>' for g in idx if g["kind"] == kind)
        gal += f'<p class="lab" style="margin:18px 0 8px">{esc(kind)} · {sum(1 for g in idx if g["kind"] == kind)}</p><p class="ck-cap" style="margin:0 0 10px">{esc(text)}</p><div class="ck-gal">{figs}</div>'
    add("Drawings", "<code>R.glyph('filled/battery')</code> inlines <code>kit/glyphs/filled/battery.svg</code>. The files keep the boards' colours; <code>course.css</code> maps them to tokens, so each one works in the dark theme. How to draw a new one: <code>kit/DRAWING.md</code>.", gal)
    # charts
    ring = {"type": "ring", "title": "Example wheel: topics placed by lecture and by how far each was taken", "desc": "Four sectors, one per lecture. Three rings from the rim inwards: stated, derived, worked through an example.",
            "rings": ["stated", "derived", "worked"],
            "sectors": [{"label": "Lecture 1", "items": [{"label": "Control loop", "ring": 0}, {"label": "Cost", "ring": 0}, {"label": "State", "ring": 2}]},
                        {"label": "Lecture 2", "em": True, "items": [{"label": "Zero gradient", "ring": 1}, {"label": "Gradient step", "ring": 2}, {"label": "Multiplier", "ring": 2, "em": True}]},
                        {"label": "Lecture 3", "items": [{"label": "KKT", "ring": 2}, {"label": "Variation", "ring": 0}, {"label": "Euler equation", "ring": 1}]},
                        {"label": "Lecture 4", "items": [{"label": "Free end", "ring": 2}, {"label": "Hamiltonian", "ring": 0}, {"label": "Costate", "ring": 1, "open": True}]}]}
    payoff = {"type": "payoff", "title": "Hide and seek: who gains in each of the four outcomes", "desc": "The hider picks spot A or B and the seeker opens one. If they match, the seeker gains 1 and the hider loses 1. Otherwise the hider gains 1. In every cell one player wants to move.",
              "rowPlayer": "Hider", "colPlayer": "Seeker", "rows": ["A", "B"], "cols": ["A", "B"], "cells": [[[-1, 1], [1, -1]], [[1, -1], [-1, 1]]],
              "arrows": [{"from": [0, 0], "to": [1, 0], "who": "row"}, {"from": [1, 0], "to": [1, 1], "who": "col"}, {"from": [1, 1], "to": [0, 1], "who": "row"}, {"from": [0, 1], "to": [0, 0], "who": "col"}]}
    dots = {"type": "dots", "title": "The lecture's table of method families as a dot matrix", "desc": "Open-loop is cheap to compute and does not handle surprises. Closed-loop handles surprises and is costly. Model predictive control is close to both strengths.",
            "cols": ["Cheap to compute", "Handles surprises"], "rows": [{"label": "Open-loop", "cells": [1, 0]}, {"label": "Closed-loop", "cells": [0, 1]}, {"label": "Model predictive control", "cells": ["part", "part"], "em": True}],
            "legend": [{"name": "yes", "cls": "f-ink", "mark": "dot"}, {"name": "no", "cls": "f-none s thin s-line", "mark": "dot"}]}
    fib = {"type": "tree", "title": "The calls made by a recursive fib(4)", "desc": "fib(4) calls fib(3) and fib(2). fib(3) calls fib(2) and fib(1). fib(2) is worked out twice.",
           "root": {"label": "fib(4)", "dark": True, "children": [{"label": "fib(3)", "children": [{"label": "fib(2)", "em": True, "note": "worked out here"}, {"label": "fib(1)"}]}, {"label": "fib(2)", "em": True, "note": "and again here"}]}}
    charts = [("line", "Line chart with a slider and readouts", chart(v1["ideas"]["4"][0]["chart"], "type: line")),
              ("fn", "Function plot with a marked point", chart(v2["ideas"]["1"]["chart"], "type: fn")),
              ("bars", "Bar chart with wrapped labels", chart(v1["ideas"]["6"][0]["chart"], "type: bars")),
              ("dots", "Dot-matrix table", chart(dots, "type: dots", "from the lecture")),
              ("ring", "Ring or wheel placement", chart(ring, "type: ring", "illustration", "Example data, to show the form.")),
              ("payoff", "2 × 2 payoff grid with move arrows", chart(payoff, "type: payoff", "from the lecture")),
              ("steps / timeline", "Step function and timeline", chart(v1["ideas"]["8"]["chart"], "type: timeline", "from the lecture") ),
              ("field", "Vector field or phase portrait", chart(v1["ideas"]["4"][1]["chart"], "type: field", "worked out")),
              ("tree", "Tree, for game trees, recursion and maps", chart(fib, "type: tree")),
              ("grid", "State grid, for dynamic programming", chart(dp_grid(), "type: grid", "worked out")),
              ("plane", "Geometry in data coordinates, with frames", chart(v2["ideas"]["7"]["chart"], "type: plane", "from the lecture")),
              ("flow", "Boxes and arrows, with a lens", chart(v1["ideas"]["1"]["chart"], "type: flow", "from the lecture")),
              ("steps", "Step function", chart({"type": "steps", "title": "A control held constant over each step", "desc": "A control signal that changes only at the step times.", "x": {"min": 0, "max": 5, "label": "step k"}, "y": {"min": -2, "max": 2, "label": "control u"},
                                                 "series": [{"name": "control u", "points": [[0, 1.5], [1, 1.5], [2, 0.5], [3, -1], [4, -1.5], [5, -1.5]]}], "slider": {"label": "Step k", "min": 0, "max": 5, "step": 0.5, "value": 2.5, "decimals": 1}}, "type: steps"))]
    cg = '<div class="g2" style="align-items:start">' + "".join(f'<div><p class="lab" style="margin:0 0 8px">{esc(t)}</p>{c}</div>' for _, t, c in charts) + "</div>"
    add("Charts", "<code>&lt;div data-chart&gt;&lt;script type=\"application/json\"&gt;{\"type\": …}&lt;/script&gt;&lt;/div&gt;</code>, or <code>KitCharts.mount(el, spec)</code>. Data, labels and a source tag in; an SVG drawn at the real width of its box out. Series differ by line style as well as colour. Sliders are native range inputs; readouts are announced to screen readers.", cg)
    import gallery2
    gallery2.sections(add)
    parts.append("</main>")
    parts.append('<footer class="rs-close"><p class="eb">Use it</p><p class="rs-h2">Write the lecture as JSON or Markdown. <i>render_lecture.py lays it out.</i></p><p class="rs-small">See kit/README.md for the content contract and kit/DRAWING.md for how to draw a new glyph.</p></footer>')
    return R.page_shell("Course kit gallery", "Every component of the course kit with a live example.", "\n".join(parts), kit)


if __name__ == "__main__":
    (KIT / "gallery.html").write_text(gallery(".", "demo/index.html", "demo/lecture-02.html"))
    print("gallery.html written")
