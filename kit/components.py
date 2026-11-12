#!/usr/bin/env python3
"""Board parts for course pages: the layouts the owner's boards use again and again, as small HTML builders.

Each function returns markup that needs only the kit's stylesheets (tokens.css, boards.css, course.css, slides.css).
Where a part is a drawing, its geometry is the board's own (noted on each function).

    compare_table(head, rows, pick=2)          comparison table with one column picked out
    ladder(rungs, at=1)                        evidence ladder: rungs from the ground up, the one we stand on marked
    steps_svg(steps, enter=4)                  numbered step boxes joined by arrows (PrSlide02 · the seven steps)
    trail_svg(nodes, above=..., marks=...)     record trail: discs joined by arrows, dashed = not there yet (As0Map)
    role_cards(roles)                          one card per kind of reader (Atom to Answer · Main)
    before_after(before, after)                two panels and an arrow (L&T · FmtBeforeAfter)
    storyboard(frames)                         a strip of 16:9 frames with number, title, note (Sense to Silicon · VdStoryboard)
    big_number(value, label, text, chip)       one number set large
    timeline_band(items)                       dated stops on one line; roadmap(lanes, cols) for bars in lanes
    tile_map(tiles, legend)                    a map of small squares by kind (Control Point Lens · Main)
    meaning_strip(pairs)                       "part of the picture -> what it stands for", under a metaphor scene (L&T Meta boards)
    quote(text, who)                           a pulled quote
    slide(kind, ...)                           1920 x 1080 slides in the boards' slide stylesheet: title, number, compare, diagram, quote
    jump_bar(ideas)                            the sticky ideas bar for long pages on phones
"""
import html
from render_lecture import chip, inline, turn_html, glyph

esc = lambda s: html.escape(str(s), quote=True)
INK, MUTE, ESP, PAPER, PAGE, SAND, LINE, RUST, PEACH, SOFT = "#2b2622", "#5a5047", "#3a2e26", "#fbf7f0", "#f3ede2", "#ece4d5", "#d9cdba", "#9a4a22", "#e3b98f", "#f5e6d3"
# the seven step icons of PrSlide02, 40 x 40, stroke only
ICONS = {
    "product": '<rect x="9" y="5" width="22" height="30" rx="4"/><circle cx="20" cy="14" r="4"/><path d="M14 26h12M14 30h8"/>',
    "budget": '<rect x="5" y="12" width="24" height="16" rx="2"/><path d="M29 17h4v6h-4"/><path d="M9 16v8M13 16v8M17 16v8"/>',
    "model": '<circle cx="8" cy="12" r="3"/><circle cx="8" cy="28" r="3"/><circle cx="20" cy="20" r="3"/><circle cx="32" cy="12" r="3"/><circle cx="32" cy="28" r="3"/><path d="M11 13l6 5M11 27l6-5M23 19l6-5M23 21l6 5"/>',
    "split": '<path d="M6 20h10"/><path d="M16 20l8-9h10M16 20l8 9h10"/><path d="M31 8l3 3-3 3M31 26l3 3-3 3"/>',
    "grid": '<rect x="7" y="7" width="26" height="26" rx="2"/><path d="M7 16h26M7 24h26M16 7v26M24 7v26"/>',
    "scale": '<path d="M20 6v28M10 34h20M8 12h24"/><path d="M8 12l-5 10h10zM32 12l-5 10h10z"/>',
    "check": '<path d="M20 4l13 5v10c0 8-6 13-13 17C13 32 7 27 7 19V9z"/><path d="M14 20l4 4 8-9"/>',
}


def compare_table(head, rows, pick=None, caption=""):
    """head: column titles (first is the row label). rows: lists of cells. pick: index of the column to mark."""
    cls = lambda j: ' class="pick"' if j == pick else ""
    th = "".join(f'<th scope="col"{cls(j)}>{inline(h)}</th>' for j, h in enumerate(head))
    tr = "".join("<tr>" + "".join((f'<th scope="row">{inline(c)}</th>' if j == 0 else f"<td{cls(j)}>{inline(c)}</td>") for j, c in enumerate(r)) + "</tr>" for r in rows)
    cap = f"<caption class=\"ck-sr\">{esc(caption)}</caption>" if caption else ""
    return f'<div class="ck-tw"><table class="ck-cmp">{cap}<thead><tr>{th}</tr></thead><tbody>{tr}</tbody></table></div>'


def ladder(rungs, at=None):
    """rungs: [{title, text, chip}] from the lowest rung up. at: index of the rung reached; rungs above it are drawn dashed."""
    li = []
    for i, r in enumerate(rungs):
        c = "at" if i == at else "todo" if at is not None and i > at else ""
        li.append(f'<li class="{c}"{" aria-current=\"step\"" if i == at else ""}><b>{inline(r["title"])}</b>{chip(r.get("chip", ""))}<span>{inline(r.get("text", ""))}</span></li>')
    return f'<ol class="ck-ladder">{"".join(li)}</ol>'


def steps_svg(steps, enter=None, start_note="Start here", enter_note="", label=None):
    """PrSlide02's row of step boxes. steps: [{title: "two short lines\\nlike this", icon, dark}]. enter: index of the step picked out in peach."""
    n = len(steps); bw, gap = 214, 33; W = n * bw + (n - 1) * gap
    out = []
    for i, s in enumerate(steps):
        x = i * (bw + gap); on = i == enter; dark = s.get("dark", False)
        fill, stroke = (ESP, ESP) if dark else (SOFT, RUST) if on else (PAPER, ESP)
        fg = PAGE if dark else INK
        out.append(f'<rect x="{x}" y="0" width="{bw}" height="196" rx="10" fill="{fill}" stroke="{stroke}" stroke-width="2"/><circle cx="{x + 38}" cy="40" r="24" fill="{PAGE if dark else ESP}"/>'
                   f'<text x="{x + 38}" y="49" font-family="IBM Plex Sans Condensed" font-size="24" font-weight="600" fill="{ESP if dark else PAGE}" text-anchor="middle">{i + 1}</text>')
        if s.get("icon") in ICONS:
            out.append(f'<g transform="translate({x + 144} 16) scale(1.3)" stroke="{PAGE if dark else RUST if on else ESP}" stroke-width="2.2" fill="none" stroke-linecap="round" stroke-linejoin="round">{ICONS[s["icon"]]}</g>')
        for j, ln in enumerate(s["title"].split("\n")[:3]):
            out.append(f'<text x="{x + 20}" y="{110 + j * 34}" font-family="Fraunces" font-size="28" fill="{fg}">{esc(ln)}</text>')
        if i < n - 1:
            ax = x + bw + 4
            out.append(f'<path d="M{ax} 98h25" stroke="{ESP}" stroke-width="3"/><path d="M{ax + 16} 102.3l9-4.3-9-4.3" stroke="{ESP}" stroke-width="3" stroke-linejoin="round" fill="none"/>')
    notes = [(0, start_note, "start")] + ([(enter, enter_note, "middle")] if enter is not None and enter_note else [])
    for i, note, anchor in notes:
        if not note: continue
        cx = i * (bw + gap) + bw / 2
        out.append(f'<path d="M{cx} 200v16" stroke="{RUST}" stroke-width="3"/><text x="{0 if anchor == "start" else cx}" y="244" font-family="IBM Plex Sans Condensed" font-size="22" font-weight="600" fill="{RUST}" '
                   f'text-anchor="{anchor}" letter-spacing="1.5">{esc(note.upper())}</text>')
    lab = label or "Steps: " + "; ".join(f"{i + 1} {s['title'].replace(chr(10), ' ')}" for i, s in enumerate(steps))
    return f'<svg class="kit-scene" viewBox="0 0 {W} 252" role="img" aria-label="{esc(lab)}" fill="none">{"".join(out)}</svg>'


def trail_svg(nodes, heading="", label=None):
    """As0Map's record trail. nodes: [{name, above, there: True | False, lock: False}]. A disc that is not there yet is dashed rust."""
    n = len(nodes); step = 160; W = 140 + (n - 1) * step
    out = [f'<text x="20" y="34" font-family="IBM Plex Sans Condensed" font-weight="600" font-size="14" letter-spacing="1.4" fill="{MUTE}">{esc(heading.upper())}</text>'] if heading else []
    for i, nd in enumerate(nodes):
        cx = 70 + i * step
        if i < n - 1: out.append(f'<path d="M{cx + 30} 170H{cx + 130}" stroke="{RUST}" stroke-width="2"/><path d="M{cx + 124} 164l8 6-8 6z" fill="{RUST}"/>')
        out.append(f'<circle cx="{cx}" cy="170" r="30" fill="{ESP}"/>' if nd.get("there", True) else f'<circle cx="{cx}" cy="170" r="30" fill="{PAPER}" stroke="{RUST}" stroke-width="2.5" stroke-dasharray="6 4"/>')
        out.append(f'<text x="{cx}" y="177" font-family="IBM Plex Sans Condensed" font-weight="600" font-size="18" fill="{PEACH if nd.get("there", True) else RUST}" text-anchor="middle">{i + 1}</text>'
                   f'<text x="{cx}" y="228" font-family="Fraunces" font-size="18" fill="{INK}" text-anchor="middle">{esc(nd["name"])}</text>')
        if nd.get("above"):
            lock = nd.get("lock")
            w = max(100, 9 * len(nd["above"]) + 26)
            out.append(f'<path d="M{cx} 92V140" stroke="{RUST}" stroke-width="1.5" stroke-dasharray="2 4"/>'
                       + (f'<rect x="{cx - w / 2}" y="58" width="{w}" height="34" rx="17" fill="#f4e1d8" stroke="#8b2e1f" stroke-width="1.5"/>' if lock else f'<rect x="{cx - w / 2}" y="58" width="{w}" height="34" rx="17" fill="{PEACH}"/>')
                       + f'<text x="{cx}" y="80" font-family="IBM Plex Sans Condensed" font-weight="600" font-size="14" fill="{"#8b2e1f" if lock else INK}" text-anchor="middle">{esc(nd["above"])}</text>')
    lab = label or "Trail: " + ", ".join(f"{nd['name']} ({'exists' if nd.get('there', True) else 'not yet'})" for nd in nodes)
    return f'<svg class="kit-scene" viewBox="0 0 {W} 250" role="img" aria-label="{esc(lab)}">{"".join(out)}</svg>'


def role_cards(roles):
    """roles: [{who, text, href, go, icon: glyph name, todo: False}]."""
    out = []
    for r in roles:
        disc = f'<div class="disc" aria-hidden="true">{glyph(r["icon"])}</div>' if r.get("icon") else ""
        body = f'{disc}<p class="eb">{esc(r["who"])}</p><p>{inline(r["text"])}</p>'
        if r.get("todo"): out.append(f'<div class="todo">{body}{chip("missing")}</div>')
        elif r.get("href"): out.append(f'<a href="{esc(r["href"])}">{body}<span class="go">{esc(r.get("go", "Open"))}</span></a>')
        else: out.append(f"<div>{body}</div>")
    return f'<div class="ck-roles">{"".join(out)}</div>'


def before_after(before, after, labels=("Before", "After")):
    """before, after: {svg, kicker, text}. The drawing may be a board scene (scenes.board('before-fabrication'))."""
    def fig(d, cls, lab):
        return (f'<figure class="{cls}"><b>{esc(lab)}</b><div>{d.get("svg", "")}</div>'
                f'<figcaption><small>{esc(d.get("kicker", ""))}</small>{inline(d.get("text", ""))}</figcaption></figure>')
    return f'<div class="ck-ba">{fig(before, "before", labels[0])}<i aria-hidden="true">→</i>{fig(after, "after", labels[1])}</div>'


def storyboard(frames):
    """frames: [{svg, title, text, time}]. Each drawing is shown in a 16:9 window and numbered V01, V02, ..."""
    li = "".join(f'<li><div>{f.get("svg", "")}</div><b>{inline(f["title"])}</b><span>{inline(f.get("text", ""))}</span>' + (f'<small>{esc(f["time"])}</small>' if f.get("time") else "") + "</li>" for f in frames)
    return f'<ol class="ck-board">{li}</ol>'


def big_number(value, label, text="", chip_label="", neg=False):
    return (f'<div class="ck-bignum{" neg" if neg else ""}"><b>{value}</b><div><p class="lab">{esc(label)}</p>'
            + (f"<p>{inline(text)}</p>" if text else "") + chip(chip_label) + "</div></div>")


def timeline_band(items):
    """items: [{when, title, text, state: "" | "on" | "todo"}]."""
    li = "".join(f'<li class="{i.get("state", "")}"><span class="when">{esc(i["when"])}</span><b>{inline(i["title"])}</b><span>{inline(i.get("text", ""))}</span></li>' for i in items)
    return f'<ol class="ck-band" style="--n:{len(items)}">{li}</ol>'


def roadmap(cols, lanes):
    """cols: column titles. lanes: [{name, bars: [{from, to, text, kind: "" | "rust" | "soft"}]}], columns counted from 1."""
    out = ['<div class="h"></div>'] + [f'<div class="h">{esc(c)}</div>' for c in cols]
    for ln in lanes:
        out.append(f'<div class="r">{esc(ln["name"])}</div>')
        col = 1
        for b in sorted(ln["bars"], key=lambda b: b["from"]):
            for _ in range(col, b["from"]): out.append("<div></div>")
            out.append(f'<div class="bar {b.get("kind", "")}" style="grid-column:span {b["to"] - b["from"] + 1}"><span>{inline(b["text"])}</span></div>'); col = b["to"] + 1
        for _ in range(col, len(cols) + 1): out.append("<div></div>")
    return f'<div class="ck-lanes" style="--n:{len(cols)}" role="group" aria-label="Roadmap">{"".join(out)}</div>'


def tile_map(tiles, legend=None):
    """tiles: [(name, kind)] with kind 0 to 4. legend: {kind: words}."""
    li = "".join(f'<li class="k{k}">{esc(n)}</li>' for n, k in tiles)
    lg = ""
    if legend:
        lg = '<ul class="ck-legend" style="margin-top:10px">' + "".join(f'<li><span class="ck-tilemap" style="display:inline-grid;grid-template-columns:16px"><span class="k{k}" style="display:block;width:16px;height:16px;border:1.3px solid var(--art-ink);background:var(--art-{("peach", "rust", "mass", "sand", "paper")[k]})"></span></span><span>{esc(w)}</span></li>' for k, w in legend.items()) + "</ul>"
    return f'<ul class="ck-tilemap">{li}</ul>{lg}'


def meaning_strip(pairs):
    return '<ul class="ck-meaning" aria-label="Reading the picture">' + "".join(f"<li><b>{esc(a)}</b><span>{inline(b)}</span></li>" for a, b in pairs) + "</ul>"


def quote(text, who=""):
    return f'<blockquote class="ck-quote"><p>{inline(text)}</p>' + (f"<footer>{esc(who)}</footer>" if who else "") + "</blockquote>"


def jump_bar(ideas, label="Ideas"):
    """ideas: [(anchor id, short title)]. Sticky on phones and tablets; course.js marks the idea on screen."""
    li = "".join(f'<li><a href="#{esc(a)}"><i>{i + 1}</i><span>{esc(t)}</span></a></li>' for i, (a, t) in enumerate(ideas))
    return f'<nav class="ck-jump" aria-label="Jump to an idea"><b>{esc(label)}</b><ol>{li}</ol></nav>'

# ----------------------------------------------------------------------------- slides (boards' slide stylesheet)

def _h(h1):
    """A heading: one string (split like every kit heading) or a pair (plain part, italic part)."""
    if isinstance(h1, (tuple, list)): return f"{esc(h1[0])} <em>{esc(h1[1])}</em>"
    return turn_html(h1).replace("<i>", "<em>").replace("</i>", "</em>")


def _frame(body, brand, n, total, eyebrow, h1, src="", foot="", dark=False, big=False):
    return (f'<div class="ck-stage{"" if dark else " lt"}"><div class="slide{" dark" if dark else ""}" data-slide="{n}"><div class="hdr"><span class="lt">{esc(brand)}</span><span>{n:02d} / {total:02d}</span></div>'
            f'<div class="top"><p class="eb">{esc(eyebrow)}</p><h2 class="{"hx" if big else "h1"}">{_h(h1)}</h2></div>'
            f'<div class="stage">{body}</div><div class="foot"><p class="src">{inline(src)}</p><p class="pn">{esc(foot)}</p></div></div></div>')


def slide(kind, brand="Course", n=1, total=1, eyebrow="", h1="", src="", foot="", **k):
    """kind: "title" (lead + four tilted cards, PrSlide01), "number" (one big number + cards), "compare" (two cards and a verdict band),
    "diagram" (a drawing in a media frame + three picture cards, PrSlide02), "quote"."""
    if kind == "title":
        pos = [(0, 0, -2.2), (470, 50, 1.8), (30, 290, 1.2), (500, 330, -1.6)]
        cards = "".join(f'<div class="cc" style="left:{x}px;top:{y}px;width:404px;height:216px;transform:rotate({r}deg)"><p class="lab">{i + 1} · {esc(c["label"])}</p>'
                        f'<p class="mid" style="font-size:46px">{esc(c["value"])}</p><p class="m">{esc(c.get("note", ""))}</p>{chip(c.get("chip", ""))}</div>' for i, (c, (x, y, r)) in enumerate(zip(k.get("cards", []), pos)))
        threads = ('<svg aria-hidden="true" width="920" height="560" viewBox="0 0 920 560" style="position:absolute;left:0;top:0" fill="none"><path d="M394 131C444 120 430 90 480 161" stroke="#e3b98f" stroke-width="3" stroke-dasharray="8 8"/>'
                   '<path d="M864 181C914 170 -10 330 40 401" stroke="#e3b98f" stroke-width="3" stroke-dasharray="8 8"/><path d="M424 421C474 410 460 370 510 441" stroke="#e3b98f" stroke-width="3" stroke-dasharray="8 8"/></svg>')
        body = (f'<div class="row" style="gap:64px;flex:1;align-items:center"><div class="col" style="flex:1;gap:24px"><p class="lead" style="font-style:italic;font-family:Fraunces,Georgia,serif;font-size:32px">{inline(k.get("lead", ""))}</p></div>'
                f'<div class="collage" style="flex:none;width:920px;height:540px">{threads}{cards}</div></div>')
        return _frame(body, brand, n, total, eyebrow, h1, src, foot, dark=True, big=True)
    if kind == "number":
        cards = "".join(f'<div class="card{" key" if c.get("key") else ""}"><p class="lab">{esc(c["label"])}</p><p class="mid">{esc(c["value"])}</p><p class="m">{inline(c.get("note", ""))}</p>{chip(c.get("chip", ""))}</div>' for c in k.get("cards", []))
        body = (f'<div class="row" style="gap:64px;align-items:flex-end"><p class="huge">{k["value"]}</p><div class="col" style="flex:1;padding-bottom:28px"><p class="lab">{esc(k.get("label", ""))}</p>'
                f'<p class="p">{inline(k.get("text", ""))}</p></div></div><div class="g{max(2, min(5, len(k.get("cards", [])) or 3))}">{cards}</div>'
                + (f'<div class="band"><b>{esc(k["band"][0])}</b><span>{inline(k["band"][1])}</span></div>' if k.get("band") else ""))
        return _frame(body, brand, n, total, eyebrow, h1, src, foot, dark=k.get("dark", False))
    if kind == "compare":
        def side(c, cls):
            rows = "".join(f'<div class="step"><span class="bul{" r" if cls == "key" else " o"}">{i + 1}</span><p class="p">{inline(t)}</p></div>' for i, t in enumerate(c.get("points", [])))
            return f'<div class="card {cls}" style="gap:18px"><p class="lab">{esc(c["label"])}</p><p class="mid">{esc(c["value"])}</p>{rows}<p class="ans">{inline(c.get("note", ""))}</p></div>'
        body = (f'<div class="vs" style="flex:1">{side(k["left"], "")}<i aria-hidden="true">vs</i>{side(k["right"], "key")}</div>'
                + (f'<div class="band"><b>{esc(k["band"][0])}</b><span>{inline(k["band"][1])}</span></div>' if k.get("band") else ""))
        return _frame(body, brand, n, total, eyebrow, h1, src, foot)
    if kind == "diagram":
        cards = "".join(f'<div class="card ill"><div class="pic">{c.get("svg", "")}</div><div class="body"><p class="lab">{esc(c["label"])}</p><p class="h3">{inline(c["title"])}</p><p class="ans">{inline(c.get("note", ""))}</p></div></div>' for c in k.get("cards", []))
        body = f'<figure class="media" style="padding:20px 24px">{k.get("svg", "")}</figure>' + (f'<div class="g3">{cards}</div>' if cards else "")
        return _frame(body, brand, n, total, eyebrow, h1, src, foot)
    if kind == "quote":
        body = (f'<div class="col" style="flex:1;justify-content:center;gap:36px"><p class="q">{_h(k["text"])}</p>'
                f'<p class="lab" style="color:var(--peach)">{esc(k.get("who", ""))}</p></div>')
        return _frame(body, brand, n, total, eyebrow, h1, src, foot, dark=True)
    raise ValueError(kind)
