# Course kit

One look for every course page, taken from the owner's design boards (Sense to Silicon, Atom to Answer, the L&T AI Centre canvas, Murmur to Market and the Robot Buyer's Guide). A course generator writes content; the kit lays it out.

Open `gallery.html` to see every piece working. Open `demo/index.html` for a small site built with it from four real lectures.

## What is here

| File | What it is |
|---|---|
| `tokens.json` | The Signal Desk UX Kit tokens, copied unchanged from the board canvas. |
| `tokens.css` | Generated from `tokens.json` by `tools/build_tokens.py`: colours for light and dark, type, spacing, and the font faces. |
| `boards/as.css` | The board canvas's own stylesheet, copied unchanged. |
| `boards.css` | Generated from `boards/as.css` by `tools/port_board_css.py`. Same rules; every hex colour replaced by its token so the dark theme works. |
| `course.css` | Makes the board rules fluid (the boards are fixed 1440 and 390 artboards) and adds the course components, all prefixed `ck-`. |
| `course.js` | Theme button, slide scaling, "idea on screen" marker. No dependencies. |
| `charts.js` | Twelve small SVG chart builders in the boards' style. No dependencies. |
| `fonts/` | Fraunces, Source Serif 4 (both with italics) and IBM Plex Sans Condensed 500/600 as woff2, from the `@fontsource` packages, with their licences. |
| `glyphs/` | 297 drawings as inline-SVG partials: 289 taken from the boards as they are (`index.json`, and the second harvest in `more/` listed in `more.json`), 8 drawn for courses in the same hand (`course.json`). |
| `scenes/`, `scenes.py` | 104 large drawings taken from the boards as they are (`scenes.board(name)`), and eight builders for new scenes in the same hand: control loop, landscape, message graph, tree search, game table, particle in a field, market, pipeline. |
| `kitmath.py`, `math/` | Maths typeset at build time with KaTeX (vendored). Pages need only `math/katex.min.css` and its woff2 fonts. |
| `components.py`, `slides.css` | Board parts: comparison table, ladder, step row, record trail, role cards, before/after, storyboard, big number, timeline, roadmap, tile map, quote, five slide layouts, the sticky ideas bar. `slides.css` is generated from the presentation boards' own stylesheet (`boards/slides.css`). |
| `render_lecture.py` | Turns a lecture (JSON contract or Markdown write-up) into a page. |
| `gallery.html` | Every component with a live example (built by `tools/build_gallery.py`). |
| `DRAWING.md` | How to draw a new glyph so it sits beside the boards' own. |
| `demo/` | Landing page, lecture index and four AA203 lectures, built by `demo/build.py`. |

No build step beyond Python 3. No requests leave the page at run time: fonts, styles and scripts are local files.

## How a course generator uses the kit

1. Write each lecture as the contract below (JSON), or as the Markdown write-up format.
2. For each idea, choose a drawing: a chart spec for `charts.js`, a glyph name, or an inline SVG drawn to `DRAWING.md`. Put these in a visuals file. Every number on a drawing must come from the lecture content; say where with the chip.
3. Run `render_lecture.py`. Link the five kit files by relative path (`--kit`).

```
python3 kit/render_lecture.py analysis/lectures/02.md --visuals visuals/02.json \
    --out site/lecture-02.html --kit ../kit --course "Stanford AA203" --mark a.
python3 kit/render_lecture.py analysis/lectures/02.md --json     # print the contract
```

From Python, `render_lecture.render_lecture(doc, kit, course, links, nav)` returns the page; `hero_html`, `strip_html`, `section_head`, `panel_html`, `ledger_html`, `block_html`, `glyph` and `page_shell` build the parts for landing, index and concept pages (see `demo/build.py`).

A page needs this in its head, in this order, and the two scripts at the end of the body:

```html
<link rel="stylesheet" href="kit/tokens.css">
<link rel="stylesheet" href="kit/boards.css">
<link rel="stylesheet" href="kit/course.css">
<link rel="stylesheet" href="kit/slides.css">
<link rel="stylesheet" href="kit/math/katex.min.css">
...
<script src="kit/charts.js"></script>
<script src="kit/course.js"></script>
```

## The content contract for a lecture

`demo/lecture-02.contract.json` is a full, real example. The shape:

```json
{
  "lecture": 2,
  "title": "Optimization Theory",
  "question": "How can you tell that a point is the lowest one, and how do you find such a point?",
  "answer": "At a lowest point no small allowed move makes things better, ...",
  "answer_short": "optional: the clause set in italic in the headline; default is the answer's first clause",
  "cards": [{"label": "A good step", "value": "25 → 16", "note": "from (3, 4) with α = 0.1"}],
  "context": [{"label": "Lecturer", "value": "Marco Pavone"}],
  "why":   {"heading": "…", "blocks": []},
  "start": {"heading": "Where we start: what the reader already has", "blocks": []},
  "ideas": [{
    "heading": "A small step against the gradient always lowers the function",
    "point": "One sentence: the idea's claim.",
    "blocks": [
      {"type": "p", "text": "Reasoning. **bold**, *italic*, `code` and [links](02.html) work."},
      {"type": "steps", "items": ["One step of the argument.", "The next."]},
      {"type": "eq", "text": "x(α) = x − α ∇f(x)"},
      {"type": "eq", "tex": "\\frac{\\partial f}{\\partial x} = 0", "text": "∂f/∂x = 0"},
      {"type": "scene", "scene": "landscape", "args": {"f": [0, 0, 1], "x0": 5, "alpha": 0.1}, "panel": "…", "chip": "worked out", "caption": "…"},
      {"type": "worked", "kind": "lecture | illustration | filled", "title": "…", "lines": ["one line per step", "the result"]},
      {"type": "table", "head": ["…"], "rows": [["…"]]},
      {"type": "list", "items": ["…"]},
      {"type": "careful", "text": "The Be careful line."},
      {"type": "figure", "caption": "…", "svg": "<svg …>"}
    ],
    "drawing": {"panel": "One step from (3, 4)", "chip": "illustration", "chart": {"type": "plane", "…": "…"}, "caption": "…"},
    "moments": [{"time": "27:16", "text": "Where this is said in the lecture."}]
  }],
  "open": {"heading": "…", "blocks": []},
  "connections": {"heading": "…", "items": [{"title": "Lecture 3", "href": "03.html", "text": "why it connects"}]},
  "check": {"heading": "…", "items": [{"q": "…", "a": "…"}]},
  "sources": ["Markdown line per source"],
  "source_url": "https://www.youtube.com/watch?v=…  (makes each moment a link to that time)"
}
```

Rules the layout relies on:

- Headings are sentences that carry the point. A heading is split at its first colon or semicolon, or its last comma; the second part is set in italic. The same goes for `question` and `answer_short` in the opening band.
- At most four cards. Each holds one real number or short formula (about 16 characters) and a note of a few words.
- `drawing` may be one object or a list. Use exactly one of `chart`, `glyph` (`"filled/battery"`), `svg`, or `tiles` (`[{glyph, k, title, text}]`).
- A lecture may have one `scene` (shown after the opening) and each idea may have a `scene` (shown full width under the idea): `{"scene": builder name, "args": {...}}` or `{"board": scene name, "labels": {...}}`, with `panel`, `chip`, `caption` and an optional `meaning` list of pairs. In a visuals file: `"scene": {...}` and `"scenes": {"2": {...}}`.
- An `eq` block's `text` is the plain formula (`∫ from t₀ to t_f of g dt`, `xᵏ⁺¹`, `∂f/∂x`, `[[1, 2], [3, 4]]`); it is typeset by `kitmath`. Give `tex` to set it yourself. Inline maths in any text: `\( ... \)`.
- `chip` is one of: from the lecture, worked out, our check, assumed, illustration, missing.
- `worked.kind`: `lecture` (the lecture's own example), `illustration` (made-up numbers, dashed top edge), `filled` (algebra the write-up filled in).

A visuals file holds the design choices apart from the words: `{"cards": [...], "context": [...], "ideas": {"1": drawing, "2": [drawing, drawing]}}`.

### The Markdown write-up format

`render_lecture.py` also reads `analysis/lectures/NN.md`: front matter (`lecture`, `question`, `answer`), then sections `# why:`, `# start:`, `# idea:` (with `point:` and `moment: time | text` lines), `# open:`, `# connects:`, `# check:` (`Q:` / `A:`), `# sources`. Inside a section, `:::steps`, `:::eq`, `:::worked`, `:::illustration`, `:::filled`, `:::careful`, `:::table` and `:::figure` map to the block types above. A `# checks` section is skipped; it belongs to the course's validator.

## Charts

```html
<div data-chart><script type="application/json">{"type": "line", "title": "…", …}</script></div>
```

or `KitCharts.mount(element, spec)`. Every spec has `type`, `title` (read by screen readers), and may have `desc` (a longer description), `source`, a `slider` (`{label, min, max, step, value, unit, decimals, labels}`) and a `lens` (a row of buttons).

| `type` | Draws | Main fields |
|---|---|---|
| `line` | Lines over x with a slider cursor and one readout per series | `x`, `y`, `series: [{name, points, dots, step}]`, `bands`, `hlines`, `points` |
| `fn` | A function with a marked point, its tangent and slope | `series: [{poly: [c0, c1, …]}]` or `points`, `marker: {tangent, extras}` |
| `steps` | A step function | as `line` |
| `bars` | Horizontal bars with wrapped labels | `items: [{label, value, em}]`, `max`, `unit` |
| `dots` | A dot-matrix table | `cols`, `rows: [{label, cells}]` with 1, 0, `"on"`, `"part"`, `"miss"` |
| `ring` | A wheel: sectors, rings, one dot per item | `sectors: [{label, items: [{label, ring}]}]`, `rings` |
| `payoff` | A 2 × 2 game grid with move arrows | `rows`, `cols`, `cells`, `arrows: [{from, to, who}]` |
| `timeline` | Rows of segments on one time axis | `rows: [{label, note, segments}]`, `ticks` |
| `field` | A vector field x′ = A x + b u with paths | `A`, `b`, `paths: [{from, T}]`; the slider sets u |
| `tree` | A tree: game trees, recursion, a map of methods | `root: {label, note, children, em, dashed}` |
| `grid` | A state grid for dynamic programming | `cells` or `frames: [{cells}]`; cell `{v, a, s}` |
| `plane` | Geometry in data coordinates | `shapes` (circle, ellipse, line, path, poly, arrow, pt, text), `frames` per slider step, `lens.options[].shapes` |
| `flow` | Boxes on a grid joined by arrows | `cols`, `rows`, `nodes`, `edges: [{from, to, route}]`, `lens.options[].subs` |

Charts are drawn at the real pixel width of their box and redrawn when it changes, so text never drops below 13 px. Series differ by line style as well as colour (solid ink, dashed rust, dotted taupe). Sliders are native range inputs; readouts are announced politely to screen readers.

## Rebuilding

```
python3 kit/tools/build_tokens.py          # tokens.json -> tokens.css
python3 kit/tools/port_board_css.py        # boards/as.css -> boards.css
python3 kit/tools/extract_glyphs.py <sense-to-silicon/project> <atom-to-answer/project>   # boards -> glyphs/
python3 kit/tools/extract_scenes.py s2s=<dir> a2a=<dir> lt=<dir> bg=<dir> mm=<dir>     # boards -> scenes/board/
python3 kit/tools/extract_glyphs2.py s2s=<dir> ...   # boards -> glyphs/more/ (names in tools/glyph_names2.json)
python3 kit/tools/port_slide_css.py        # boards/slides.css -> slides.css
python3 kit/tools/build_gallery.py         # gallery.html
python3 kit/tools/check_contrast.py        # every text pair at least 4.5:1, both themes
python3 kit/demo/build.py --lectures <course>/analysis/lectures [--publish <folder>]
```

## Limits

- Board scenes keep the boards' label sizes (10 to 11 units on a 1296-unit sheet); they are pictures to show wide, not phone layouts. The scene builders keep every label at 14 units or more.
- `kitmath.tex_from_plain` converts the lecture formats' usual formulas; it is not a parser for everything. Pass `tex` when it gets one wrong. Node must be installed where pages are built; without it formulas fall back to the plain block.
- The slide layouts use the boards' class names (`.slide .card .step .num` ...) scoped under `.slide`; a few of those names also exist in `boards.css`, so check a new layout in the gallery before relying on it.
- `charts.js` needs JavaScript. Without it each chart shows its title and description.
