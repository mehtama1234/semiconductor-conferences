"""Gallery sections for kit 2: scenes, more drawings, board parts, slides, maths. Called by build_gallery.gallery()."""
import json, html
from pathlib import Path
import render_lecture as R, scenes as SC, components as C, kitmath as M
KIT = Path(__file__).resolve().parent.parent
esc = html.escape


def sections(add):
    # ---- scenes drawn by the builders
    made = [("control_loop", SC.control_loop(uid="g-loop", cards=[("Target", "25 m/s", "set by the driver"), ("Error", "3 m/s", "25 − 22")]), "scenes.control_loop(plant='car' | 'cart' | 'thermostat', measured=, target=, error=, action=, disturbance=, cards=)"),
            ("landscape", SC.landscape(uid="g-land", cards=[("Step size", "α = 0.3", "x ← x − α f′(x)")]), "scenes.landscape(f=, x0=, alpha=, n=): the steps are computed from f"),
            ("message_graph", SC.message_graph(uid="g-graph"), "scenes.message_graph(nodes=, edges=, messages=)"),
            ("tree_search", SC.tree_search(uid="g-tree"), "scenes.tree_search(tree={label, value, state: path | seen | cut, children})"),
            ("game_table", SC.game_table(uid="g-game"), "scenes.game_table(rows=, cols=, cells=, stable=(row, col))"),
            ("particle_field", SC.particle_field(uid="g-field"), "scenes.particle_field(force=lambda x, y: (fx, fy), start=, v0=): the path is integrated from the rule"),
            ("market", SC.market(uid="g-market"), "scenes.market(sellers=, buyers=): the clearing price is worked out"),
            ("pipeline", SC.pipeline(uid="g-pipe", cards=[("Held back", "20%", "never trained on")]), "scenes.pipeline(stages=[(title, line, line)] * 5)")]
    ex = "".join(SC.scene_html(sc, panel=f"`{name}`", chip="illustration", caption=f"`{use}`") for name, sc, use in made)
    ex += SC.scene_html(SC.control_loop(plant="cart", uid="g-cart", title="Balancing a pole on a cart", measured="Angle: 0.10 rad", target="Target: 0 rad", error="Error: 0.10 rad", action="Push the cart right", disturbance="A slope ahead"),
                        panel="`control_loop(plant='cart')`", caption="The same loop around a cart with a pole. `plant='thermostat'` draws a room with a heater.")
    add("Scenes drawn for a lecture", "<code>scenes.scene_html(scenes.landscape(...), panel, chip, caption)</code>. Eight builders in the hand of the boards' engineering sheets: a framed sheet, a ground line, hard-hat figures, "
        "callout boxes with leaders, tilted number cards, a dashed rust path. Each takes the lecture's own numbers and computes what it draws. On a phone the drawing scrolls inside its box and the numbered key carries the words.", ex,
        "Put one in a lecture with <code>{\"scene\": {\"scene\": \"landscape\", \"args\": {...}}}</code> in the visuals file. See DRAWING.md, “Composing a scene”.")
    # ---- one board scene large, with its meaning strip
    big = R.scene_block({"board": "base-camps-mountain", "panel": "Board scene · `scenes.board('base-camps-mountain')`", "chip": "illustration",
                         "caption": "Taken from the L&T canvas as it is. Pass `labels={n: 'words'}` to replace a label by its number.",
                         "meaning": [("Camps", "the steps of the method, in order"), ("Acclimatising", "evidence gathered before the next step"), ("Turning back", "stopping counts as a result"), ("Summit", "the claim, once every step holds")]})
    big += R.scene_block({"board": "chip-layout", "panel": "Board scene · `scenes.board('chip-layout')`", "chip": "from the lecture", "caption": "The lab's converter layout from Sense to Silicon: 898 shapes on 21 layers.", "min_width": 620})
    idx = SC.board_index(); groups = {}
    for i in idx: groups.setdefault(i["group"], []).append(i)
    titles = {"device": "Devices and cutaways", "place": "Places and sections", "metaphor": "Engineering-sheet metaphors", "storyboard": "Storyboard frames", "steps": "Steps, trails and ladders",
              "map": "Maps, wheels and plans", "beforeafter": "Before and after", "chart": "Drawn charts"}
    grid = ""
    for g, t in titles.items():
        cells = "".join(f'<figure class="sc"><div>{SC.board(i["name"])}</div><figcaption><b>{esc(i["name"])}</b>{esc(i["source"])}</figcaption></figure>' for i in groups.get(g, []))
        grid += f'<h3 class="lab" style="margin:22px 0 10px">{esc(t)} · {len(groups.get(g, []))}</h3><div class="ck-gal sc">{cells}</div>'
    add(f"Scenes taken from the boards · {len(idx)}", "<code>scenes.board(name, labels=None)</code>, or <code>{\"board\": name}</code> in a visuals file. The boards' own large drawings, unchanged: shapes, colours, line weights and words. "
        "<code>scenes/index.json</code> lists each one with its source board and its numbered labels.", big + grid,
        "Board scenes keep the boards' label sizes (10 to 11 units on a 1296-unit sheet). Use them wide, or relabel.")
    # ---- more drawings
    more = json.loads((KIT / "glyphs" / "more.json").read_text())
    cells = "".join(f'<figure><div>{R.glyph("more/" + g["name"])}</div><figcaption>{esc(g["name"])}</figcaption></figure>' for g in more)
    add(f"More drawings and marks · {len(more)}", "<code>R.glyph('more/gear')</code>. A second harvest from all five canvases: product glyphs, bold marks and line icons, each taken as it is and named. "
        "<code>glyphs/more.json</code> lists them with their source board.", f'<div class="ck-gal more">{cells}</div>')
    # ---- board parts
    ex = C.compare_table(["", "Open loop", "Closed loop", "Receding horizon"], [["Uses measurements", "No", "**Every step**", "Every step"], ["Plans ahead", "Whole horizon, once", "No", "A short window, again and again"],
                         ["When the plant is pushed", "Drifts", "**Corrects**", "Corrects and re-plans"]], pick=2)
    add("Comparison table", "<code>components.compare_table(head, rows, pick=2)</code>. One column is picked out with rust edges.", ex)
    ex = C.ladder([{"title": "Stated in the lecture", "text": "The claim, in the lecturer's words.", "chip": "from the lecture"}, {"title": "Worked on paper", "text": "Each step of the algebra filled in.", "chip": "worked out"},
                   {"title": "Checked with numbers", "text": "A small case computed and compared.", "chip": "our check"}, {"title": "Proved in general", "text": "Not done here.", "chip": "missing"}], at=2)
    add("Evidence ladder", "<code>components.ladder(rungs, at=2)</code>. Rungs from the ground up; the rung reached is marked, those above are dashed.", ex)
    st = [{"title": "State the\nproblem", "icon": "product", "dark": True}, {"title": "Write the\ncost", "icon": "budget", "dark": True}, {"title": "Model the\nplant", "icon": "model"}, {"title": "Choose the\nmethod", "icon": "split"},
          {"title": "Solve for\nthe input", "icon": "grid"}, {"title": "Compare the\ncosts", "icon": "scale"}, {"title": "Check and\ndecide", "icon": "check"}]
    ex = f'<figure class="rs-media"><div class="rs-mh"><span>Step row</span>{R.chip("illustration")}</div><div class="rs-mb"><div class="ck-scene-pan bare" style="--min:900px">{C.steps_svg(st, enter=4, enter_note="The method comes in here")}</div></div></figure>'
    ex += f'<figure class="rs-media"><div class="rs-mh"><span>Record trail</span>{R.chip("illustration")}</div><div class="rs-mb"><div class="ck-scene-pan bare" style="--min:900px">' + C.trail_svg(
        [{"name": "Question", "above": "you ask", "there": False}, {"name": "Model", "above": "lecture 1"}, {"name": "Condition", "above": "lecture 2"}, {"name": "Method", "above": "lecture 3"},
         {"name": "Check", "above": "never skipped", "lock": True}, {"name": "Answer", "above": "you decide", "there": False}], heading="Where each part comes from") + "</div></div></figure>"
    add("Step row and record trail", "<code>components.steps_svg(steps, enter=4)</code> (the seven-step row of the presentation boards) and <code>components.trail_svg(nodes)</code> (the record trail of the map board). "
        "Dark boxes come first; the peach box is the step the page is about; a dashed disc is something not there yet.", ex)
    ex = C.role_cards([{"who": "New to the subject", "text": "Start with the question and the opening picture of each lecture.", "href": "#", "go": "Open lecture 1", "icon": "more/graduation-cap"},
                       {"who": "Revising for an exam", "text": "Use the check-yourself questions and the worked ledgers.", "href": "#", "go": "Open the checks", "icon": "more/checklist"},
                       {"who": "Building something", "text": "Go to the method pages and their limits.", "href": "#", "go": "Open the methods", "icon": "more/tool"},
                       {"who": "Teaching it", "text": "Slides and speaker notes are not written yet.", "todo": True, "icon": "more/screen"}])
    add("Role cards", "<code>components.role_cards(roles)</code>. One card per kind of reader; a dashed card says plainly what is not there.", ex)
    ex = C.before_after({"svg": SC.board("before-fabrication"), "kicker": "Illustrative current process", "text": "One-off parts wait: jobs too small to automate are done by hand."},
                        {"svg": SC.board("after-fabrication"), "kicker": "What we would test", "text": "A robot cell is taught each new part; a person checks the part against its drawing."}, labels=("Today", "The idea under test"))
    add("Before and after", "<code>components.before_after(before, after, labels)</code>. Two drawings of the same place and an arrow. Shown with two board scenes.", ex)
    fr = [("frame-v02-product-first", "Product first", "The seven steps appear one by one."), ("frame-v03-parts", "The device, as its parts", "Each part pops in with its number."), ("frame-v04-power-bar", "The bar fills", "What is left is drawn last."),
          ("frame-v07-zoom-chip", "Zoom into the chip", "Four grids, one corner in rust."), ("frame-v09-blanks-targets", "Blanks become targets", "Empty boxes take a number."), ("frame-v12-converter-curve", "The curve draws", "A line traces left to right.")]
    ex = C.storyboard([{"svg": SC.board(n), "title": t, "text": x, "time": f"0:{10 + 12 * i:02d}"} for i, (n, t, x) in enumerate(fr)])
    add("Storyboard strip", "<code>components.storyboard(frames)</code>. Frames in a 16:9 window, numbered, with a title, a line of action and a time. Shown with six of the boards' twelve frames.", ex)
    ex = C.big_number("25 <i>→</i> 16", "One good step", "From (3, 4) with step size 0.1 the function value falls from 25 to 16.", "worked out")
    ex += '<div style="height:16px"></div>' + C.quote("At a lowest point no small allowed move makes things better.", "Lecture 2 · the first-order condition")
    add("Big number and pulled quote", "<code>components.big_number(value, label, text, chip)</code> and <code>components.quote(text, who)</code>.", ex)
    ex = C.timeline_band([{"when": "Lecture 1", "title": "State the problem", "text": "Plant, cost, constraints.", "state": "on"}, {"when": "Lecture 2", "title": "Conditions for a minimum", "text": "Gradients and multipliers."},
                          {"when": "Lecture 3", "title": "Paths, not points", "text": "Calculus of variations."}, {"when": "Lecture 4", "title": "The costate", "text": "Not written yet.", "state": "todo"}])
    ex += '<div style="height:20px"></div>' + C.roadmap(["Week 1", "Week 2", "Week 3", "Week 4"], [{"name": "Theory", "bars": [{"from": 1, "to": 2, "text": "Optimality conditions"}, {"from": 3, "to": 4, "text": "Variations and costates", "kind": "rust"}]},
                                                    {"name": "Practice", "bars": [{"from": 2, "to": 3, "text": "Problem set 1"}, {"from": 4, "to": 4, "text": "Problem set 2", "kind": "soft"}]}])
    add("Timeline band and roadmap lanes", "<code>components.timeline_band(items)</code> and <code>components.roadmap(cols, lanes)</code>. A rust dot is where we are; a dashed dot or bar is planned.", ex)
    tiles = [(f"L{i + 1}", (0, 0, 1, 0, 3, 2, 0, 3, 4, 0, 1, 3, 0, 0, 2, 4)[i]) for i in range(16)]
    ex = C.tile_map(tiles, {0: "Theory", 1: "This page", 2: "Proof", 3: "Example", 4: "Not written"})
    ex += '<div style="height:16px"></div>' + R.scene_block({"board": "breadth-wheel", "panel": "Wheel · `scenes.board('breadth-wheel')`", "chip": "illustration", "caption": "For your own data use the `ring` chart; this is the board's wheel as drawn.", "min_width": 900})
    add("Tile map and wheel", "<code>components.tile_map(tiles, legend)</code>: one square per item, filled by kind. Wheels: the <code>ring</code> chart for data, or a board wheel as a scene.", ex)
    # ---- slides
    cards = [{"label": "The plant", "value": "A cart", "note": "one force, one track", "chip": "from the lecture"}, {"label": "The cost", "value": "∫ u² dt", "note": "effort, added up", "chip": "from the lecture"},
             {"label": "The condition", "value": "∇f = 0", "note": "no move helps", "chip": "worked out"}, {"label": "The answer", "value": "25 → 16", "note": "one step from (3, 4)", "chip": "our check"}]
    sl = [C.slide("title", "Stanford AA203", 1, 5, "Lecture 2 · optimization theory", ("How do you know a point is the lowest?", "No small allowed move makes things better."), "The question and answer of the lecture, in the page's words.", "Lecture 2", cards=cards,
                  lead="At a lowest point the gradient is zero, or it is balanced exactly by the gradients of the constraints."),
          C.slide("number", "Stanford AA203", 2, 5, "One step, worked", ("A small step against the gradient lowers the function.", "One step takes 25 to 16."), "Worked from f(x) = x₁² + x₂² at (3, 4) with α = 0.1.", "Lecture 2", value="16", label="f after one step",
                  text="x moves from (3, 4) to (2.4, 3.2).", cards=[{"label": "Before", "value": "25", "note": "f(3, 4)", "key": True}, {"label": "Step size", "value": "0.1", "note": "α"}, {"label": "Gradient", "value": "(6, 8)", "note": "∇f at (3, 4)"}],
                  band=("So", "the value falls whenever the step is small enough.")),
          C.slide("compare", "Stanford AA203", 3, 5, "Two ways to act", ("Open loop plans once.", "Closed loop looks again at every step."), "Lecture 1.", "Lecture 1",
                  left={"label": "Open loop", "value": "u*(t)", "points": ["Plan the whole input from the start state.", "Never look at the plant again."], "note": "Cheap, and blind to pushes."},
                  right={"label": "Closed loop", "value": "π(x, t)", "points": ["Measure the state.", "Choose the input from what was measured."], "note": "**Corrects** when the plant is pushed."}, band=("Verdict", "use feedback when the plant can be disturbed.")),
          C.slide("diagram", "Stanford AA203", 4, 5, "The method, step by step", ("Start with the problem.", "The method comes in at step 5."), "The seven steps of the course.", "Course map", svg=C.steps_svg(st, enter=4, enter_note="The method comes in here"),
                  cards=[{"label": "First", "title": "Say what is being moved", "note": "**Then:** what it costs.", "svg": R.glyph("course/cart")}, {"label": "Then", "title": "Find where no move helps", "note": "**So:** the gradient is zero.", "svg": R.glyph("course/bowl")},
                         {"label": "Last", "title": "Check the answer", "note": "**Valid answer:** it is not a minimum.", "svg": R.glyph("filled/scale")}]),
          C.slide("quote", "Stanford AA203", 5, 5, "In one line", "", "", "Lecture 2", text=("At a lowest point no small allowed move makes things better.", "Everything else is bookkeeping."), who="The lecture, in one sentence")]
    ex = "".join(f'<div style="margin-bottom:16px">{s}</div>' for s in sl)
    add("Slide layouts in the boards' slide stylesheet", "<code>components.slide(kind, brand, n, total, eyebrow, h1, src, foot, ...)</code> with <code>kind</code> one of <code>title</code>, <code>number</code>, <code>compare</code>, <code>diagram</code>, <code>quote</code>. "
        "The rules are the presentation boards' own (<code>slides.css</code>, generated from <code>boards/slides.css</code>): 1920 × 1080, scaled to the stage by <code>course.js</code>.", ex,
        "The earlier <code>.ck-slide</code> frame still works. These five use the boards' class names (<code>.slide .hdr .top .stage .card .band .collage .cc</code>).")
    # ---- maths
    eqs = [("A fraction and a gradient", "∂f/∂x = (x² + 1)/(2x)"), ("An integral with limits", "J = h(x(t_f), t_f) + ∫ from t₀ to t_f of g(x(t), u(t), t) dt"),
           ("Gradients, sums and conditions on several lines", "∇f(x*) + Σᵢ λᵢ ∇hᵢ(x*) + Σⱼ μⱼ ∇gⱼ(x*) = 0\nμⱼ ≥ 0 for every inequality\nμⱼ = 0 for every inactive inequality"),
           ("A matrix", "ẋ = [[0, 1], [−2, −3]] x + [[0], [1]] u"), ("A root under an integral", "J(x) = ∫ from t₀ to t_f of √(1 + ẋ(t)²) dt"), ("Labelled lines", "Open-loop:    u*(t) = e(x(t₀), t)\nClosed-loop:  u*(t) = π(x(t), t)")]
    ex = "".join(f'<p class="lab" style="margin:14px 0 6px">{esc(t)}</p>{M.eq_html(e)}<p class="ck-cap">Written as <code>{esc(e).replace(chr(10), " ⏎ ")}</code></p>' for t, e in eqs)
    ex += '<p class="lab" style="margin:14px 0 6px">From TeX, on paper</p>' + M.eq_html(tex=r"H(x, u, p, t) = g(x, u, t) + p^{\top} f(x, u, t), \qquad \dot{p} = -\frac{\partial H}{\partial x}", text="H = g + pᵀ f; ṗ = −∂H/∂x").replace('class="ck-eq ck-math"', 'class="ck-eq ck-math light"')
    ex += "<p>" + R.inline(r"Inline maths sits in a sentence: the step \(x^{k+1} = x^k - \alpha \nabla f(x^k)\) lowers \(f\) when \(\alpha\) is small.") + "</p>"
    add("Maths, typeset at build time", "<code>kitmath.eq_html(text)</code> for the lecture formats' plain formulas, <code>kitmath.eq_html(tex=...)</code> for TeX, <code>\\( ... \\)</code> inside any paragraph. "
        "KaTeX runs when the page is built; the reader's browser gets HTML, MathML for screen readers, and fonts from <code>kit/math/fonts</code>. No script, no network.", ex,
        "Every <code>eq</code> block in a lecture goes through this. If Node is missing at build time the plain block is used instead.")
    ex = C.jump_bar([("c1", "Opening band"), ("c2", "Context strip"), ("c3", "Argument rail"), ("c4", "Idea plate")]).replace('class="ck-jump"', 'class="ck-jump show"')
    add("Sticky ideas bar", "<code>components.jump_bar([(anchor, short title)])</code>; <code>render_lecture</code> adds it to every lecture. Hidden on wide screens, where the argument rail does the job. "
        "On phones and tablets it stays at the top; the chip for the idea on screen opens to show its title.", ex)
