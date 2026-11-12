#!/usr/bin/env python3
"""Turn one lecture into a course-kit page.

Input is either the lecture contract as JSON (see kit/README.md) or the Markdown write-up format
used in a course repo's analysis/lectures/NN.md. Output is one self-contained HTML page that links
kit/tokens.css, kit/boards.css, kit/course.css, kit/charts.js and kit/course.js by relative path.

    python3 kit/render_lecture.py lectures/02.md --out site/lecture-02.html --kit ../kit \
        --course "Stanford AA203" --visuals visuals/02.json

    python3 kit/render_lecture.py lectures/02.md --json      # print the contract and stop

No third-party packages. The write-up's words are kept as they are; this file only lays them out.
"""
from __future__ import annotations
import argparse, html, json, re, sys
from pathlib import Path

KIT = Path(__file__).resolve().parent
sys.path.insert(0, str(KIT))
import kitmath
esc = html.escape

# ----------------------------------------------------------------------------- Markdown -> contract

def _front(text):
    meta = {}
    if text.startswith("---"):
        head, _, text = text[3:].partition("\n---")
        for line in head.strip().splitlines():
            k, _, v = line.partition(":")
            meta[k.strip()] = v.strip()
    return meta, text


def _blocks(lines):
    """Body lines of one section -> list of block dicts, plus point and moments."""
    out, point, moments, i, para, bullets = [], None, [], 0, [], []

    def flush():
        nonlocal para, bullets
        if para:
            out.append({"type": "p", "text": " ".join(para)}); para = []
        if bullets:
            out.append({"type": "list", "items": bullets}); bullets = []

    while i < len(lines):
        ln = lines[i]
        s = ln.strip()
        if s.startswith(":::") and len(s) > 3:
            flush()
            kind, _, title = s[3:].partition(" ")
            body = []
            i += 1
            while i < len(lines) and lines[i].strip() != ":::":
                body.append(lines[i]); i += 1
            body_s = [b.strip() for b in body if b.strip()]
            if kind == "steps":
                out.append({"type": "steps", "items": [b[2:] if b.startswith("- ") else b for b in body_s]})
            elif kind == "eq":
                out.append({"type": "eq", "text": "\n".join(b.rstrip() for b in body if b.strip())})
            elif kind in ("worked", "illustration", "filled"):
                out.append({"type": "worked", "kind": {"worked": "lecture"}.get(kind, kind), "title": title.strip(), "lines": body_s})
            elif kind == "careful":
                out.append({"type": "careful", "text": " ".join(body_s)})
            elif kind == "table":
                rows = [[c.strip() for c in b.split("|")] for b in body_s]
                out.append({"type": "table", "head": rows[0], "rows": rows[1:]})
            elif kind == "figure":
                out.append({"type": "figure", "caption": title.strip(), "svg": "\n".join(body).strip()})
            else:
                out.append({"type": "p", "text": " ".join(body_s)})
        elif s.startswith("point:"):
            flush(); point = s[6:].strip()
        elif s.startswith("moment:"):
            flush(); t, _, txt = s[7:].partition("|"); moments.append({"time": t.strip(), "text": txt.strip()})
        elif s.startswith("- "):
            if para: flush()
            bullets.append(s[2:])
        elif not s:
            flush()
        else:
            if bullets: flush()
            para.append(s)
        i += 1
    flush()
    return out, point, moments


def parse_markdown(text):
    """The analysis/lectures/NN.md format -> the lecture contract (a dict)."""
    meta, body = _front(text)
    doc = {"lecture": int(meta.get("lecture", 0) or 0), "question": meta.get("question", ""), "answer": meta.get("answer", ""),
           "ideas": [], "sources": []}
    sections, cur = [], None
    for ln in body.splitlines():
        m = re.match(r"^# (\w+)(?::\s*(.*))?$", ln)
        if m:
            cur = {"kind": m.group(1), "heading": (m.group(2) or "").strip(), "lines": []}; sections.append(cur)
        elif cur is not None:
            cur["lines"].append(ln)
    for sec in sections:
        kind = sec["kind"]
        if kind == "checks":
            continue  # arithmetic checks are for the course's validator, not for the page
        blocks, point, moments = _blocks(sec["lines"])
        if kind in ("why", "start", "open"):
            doc[kind] = {"heading": sec["heading"], "blocks": blocks}
        elif kind == "idea":
            doc["ideas"].append({"heading": sec["heading"], "point": point, "blocks": blocks, "moments": moments, "drawing": None})
        elif kind == "connects":
            items = []
            for b in blocks:
                for it in b.get("items", []):
                    m = re.match(r"\[(.+?)\]\((.+?)\)\s*\|\s*(.*)", it)
                    items.append({"title": m.group(1), "href": m.group(2), "text": m.group(3)} if m else {"title": it, "href": None, "text": ""})
            doc["connections"] = {"heading": sec["heading"], "items": items}
        elif kind == "check":
            qa, q = [], None
            for ln in sec["lines"]:
                s = ln.strip()
                if s.startswith("Q:"): q = s[2:].strip()
                elif s.startswith("A:") and q: qa.append({"q": q, "a": s[2:].strip()}); q = None
            doc["check"] = {"heading": sec["heading"], "items": qa}
        elif kind == "sources":
            for b in blocks:
                doc["sources"] += b.get("items", [])
    m = re.search(r"https://www\.youtube\.com/watch\?v=[\w-]+", "\n".join(doc["sources"]))
    if m: doc["source_url"] = m.group(0)
    m = re.search(r'"([^"]*Lecture \d+: ([^"]+))"', "\n".join(doc["sources"]))
    if m: doc["title"] = m.group(2).strip()
    return doc

# ----------------------------------------------------------------------------- small helpers

def inline(text, links=None):
    """Bold, italic, code and links. Everything else is escaped."""
    maths = []
    def keep(m):
        maths.append(kitmath.inline_html(m.group(1))); return f"\x00{len(maths) - 1}\x00"
    text = re.sub(r"\\\((.+?)\\\)", keep, text)
    t = esc(text, quote=False)
    t = re.sub(r"`([^`]+)`", r"<code>\1</code>", t)
    t = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", t)
    t = re.sub(r"(?<![\w*])\*([^*\s][^*]*?)\*(?![\w*])", r"<em>\1</em>", t)

    def link(m):
        href = m.group(2)
        if links is not None:
            href = links(href)
            if not href: return m.group(1)
        ext = ' rel="noopener"' if href.startswith("http") else ""
        return f'<a href="{esc(href)}"{ext}>{m.group(1)}</a>'
    t = re.sub(r"\[([^\]]+)\]\(([^)\s]+)\)", link, t)
    return re.sub("\x00(\\d+)\x00", lambda m: maths[int(m.group(1))], t)


def split_turn(heading):
    """Split a heading into its statement and its turn (the part set in italic)."""
    m = re.search(r"[:;] ", heading)
    if m and len(heading) - m.end() >= 12:
        return heading[: m.end() - 1], heading[m.end():]
    i = heading.rfind(", ")
    if i > 12 and len(heading[i + 2:].split()) >= 3:
        return heading[: i + 1], heading[i + 2:]
    return heading, ""


def turn_html(heading):
    a, b = split_turn(heading)
    return esc(a) + (f" <i>{esc(b)}</i>" if b else "")


def short_answer(answer, limit=100):
    """First clause of the answer, in the answer's own words, short enough for the headline."""
    first = re.split(r"; ", answer)[0]
    if len(first) > limit:
        cut = first.rfind(", ", 0, limit)
        if cut > 30: first = first[:cut]
    first = first.rstrip(".,;")
    rest = answer[len(first):].lstrip(" ,;")
    return first + ".", rest


def seconds(t):
    parts = [int(p) for p in t.split(":")]
    s = 0
    for p in parts: s = s * 60 + p
    return s


def glyph(name):
    """Inline one drawing from kit/glyphs, e.g. glyph('filled/battery')."""
    p = KIT / "glyphs" / (name + ".svg")
    return p.read_text().strip() if p.exists() else f"<!-- missing glyph {esc(name)} -->"


CHIPS = {"from the lecture": "t-le", "worked out": "t-wo", "our check": "t-oc", "assumed": "t-as", "missing": "t-mi",
         "illustration": "t-il", "verified": "t-ve", "our reading": "t-oc", "our drawing": "t-oc",
         "from the papers": "t-le", "from the catalog": "t-ve", "counted": "t-wo"}


def chip(label):
    return f'<span class="t {CHIPS.get(label.lower(), "")}">{esc(label)}</span>' if label else ""

# ----------------------------------------------------------------------------- components

def cards_html(cards):
    """The opening band's tilted number cards and their dashed threads (boards' geometry)."""
    if not cards: return ""
    threads = ['M236 78 C 260 84, 260 128, 284 134', 'M398 198 C 378 238, 196 152, 166 182', 'M240 246 C 264 252, 262 296, 286 302']
    svg = '<svg viewBox="0 0 520 380" aria-hidden="true" preserveAspectRatio="none">' + "".join(f'<path d="{d}"/>' for d in threads[: max(0, len(cards) - 1)]) + "</svg>"
    lis = "".join(f'<li class="ck-card"><p class="k">{i + 1} · {esc(c["label"])}</p><b>{esc(c["value"])}</b><span>{esc(c.get("note", ""))}</span></li>'
                  for i, c in enumerate(cards[:4]))
    return f'<ol class="ck-cards" aria-label="The numbers this page turns on">{svg}{lis}</ol>'


def hero_html(brand, mark, right, eyebrow, h1, lede="", cards=None, extra="", home="index.html", long=False):
    side = cards_html(cards) if isinstance(cards, list) else (cards or "")
    grid = "rs-hg" if side else "rs-hg solo"
    return (f'<header class="rs-hero"><div class="rs-top"><a class="rs-brand" href="{esc(home)}"><i>{esc(mark)}</i>{esc(brand)}</a>'
            f'<span class="rs-r">{esc(right)}<button type="button" class="ck-theme" aria-label="Change colour theme">Theme: auto</button></span></div>'
            f'<div class="{grid}"><div><p class="eb">{esc(eyebrow)}</p><h1 class="rs-h1{" long" if long else ""}">{h1}</h1>'
            + (f'<p class="rs-lede">{lede}</p>' if lede else "") + extra + f"</div>{side}</div></header>")


def strip_html(items, crumb=""):
    if not items: return ""
    sels = "".join(f'<span class="rs-sel"><b>{esc(i["label"])}</b>{inline(i["value"])}</span>' for i in items)
    return f'<nav class="rs-selbar" aria-label="About this page">{sels}' + (f'<span class="rs-crumb">{esc(crumb)}</span>' if crumb else "") + "</nav>"


def section_head(eyebrow, heading, intro="", tag="h2"):
    return (f'<div class="rs-sh"><p class="eb">{esc(eyebrow)}</p><{tag} class="rs-h2">{turn_html(heading)}</{tag}>'
            + (f'<p class="rs-in">{intro}</p>' if intro else "") + "</div>")


def ledger_html(block):
    kind = block.get("kind", "lecture")
    label = {"lecture": "from the lecture", "illustration": "illustration", "filled": "worked out"}.get(kind, kind)
    rows = []
    for i, ln in enumerate(block["lines"]):
        m = re.match(r"^([A-Za-z][^:=−()]{2,33}): (.+)$", ln)
        body = f"<b>{inline(m.group(1))}</b>{inline(m.group(2))}" if m else inline(ln)
        cls = ' class="res"' if i == len(block["lines"]) - 1 else ""
        rows.append(f"<li{cls}><div>{body}</div></li>")
    return (f'<section class="ck-ledger{" il" if kind == "illustration" else ""}"><header><h4>{inline(block["title"])}</h4>{chip(label)}</header>'
            f'<ol>{"".join(rows)}</ol></section>')


def block_html(b, links=None):
    t = b["type"]
    if t == "p": return f"<p>{inline(b['text'], links)}</p>"
    if t == "list": return "<ul>" + "".join(f"<li>{inline(i, links)}</li>" for i in b["items"]) + "</ul>"
    if t == "steps": return '<ol class="ck-steps">' + "".join(f"<li><div>{inline(i, links)}</div></li>" for i in b["items"]) + "</ol>"
    if t == "eq": return kitmath.eq_html(b.get("text"), tex=b.get("tex"))
    if t == "scene": return scene_block(b)
    if t == "worked": return ledger_html(b)
    if t == "careful": return f'<p class="ck-careful"><b>Be careful</b>{inline(b["text"], links)}</p>'
    if t == "table":
        head = "".join(f'<th scope="col">{inline(c)}</th>' for c in b["head"])
        rows = "".join("<tr>" + "".join((f'<th scope="row" style="background:none;color:var(--ink);text-transform:none;letter-spacing:0;font:600 15px/1.4 var(--font-body)">{inline(c)}</th>' if j == 0 else f"<td>{inline(c)}</td>") for j, c in enumerate(r)) + "</tr>" for r in b["rows"])
        return f'<div class="ck-tw"><table><thead><tr>{head}</tr></thead><tbody>{rows}</tbody></table></div>'
    if t == "html": return b["html"]          # local: a block the course generator has already laid out with kit classes
    if t == "figure": return panel_html({"panel": "Figure", "chip": "from the lecture", "svg": b["svg"], "caption": b["caption"]})
    return ""


def scene_block(d):
    """A scene from kit/scenes.py: {"scene": builder name, "args": {...}} or {"board": name, "labels": {...}}; plus panel, chip, caption, meaning."""
    import scenes
    sc = scenes.BUILDERS[d["scene"]](**d.get("args", {})) if d.get("scene") else scenes.board(d["board"], d.get("labels"))
    out = scenes.scene_html(sc, d.get("panel", "The scene"), d.get("chip", "illustration"), d.get("caption", ""), d.get("min_width", 1120 if d.get("scene") else 1000))
    if d.get("meaning"):
        strip = '<ul class="ck-meaning" aria-label="Reading the picture">' + "".join(f"<li><b>{esc(a)}</b><span>{inline(b)}</span></li>" for a, b in d["meaning"]) + "</ul>"
        out = out.replace("</div></figure>", strip + "</div></figure>")
    return out


def panel_html(d):
    """One labelled panel (boards: .rs-media): header bar, source chip, a drawing, a caption."""
    if d.get("scene") or d.get("board"): return scene_block(d)
    if d.get("tiles"):
        tiles = "".join(f'<article class="card"><div class="rs-pic">{glyph(t["glyph"]) if t.get("glyph") else t.get("svg", "")}</div>'
                        f'<p class="rs-k">{esc(t.get("k", ""))}</p><h3>{esc(t["title"])}</h3><p class="mut">{inline(t.get("text", ""))}</p></article>' for t in d["tiles"])
        inner = f'<div class="ck-tiles" style="--n:{d.get("cols", len(d["tiles"]))}">{tiles}</div>'
        if d.get("panel"):
            cap = f'<figcaption class="ck-cap">{inline(d["caption"])}</figcaption>' if d.get("caption") else ""
            return (f'<figure class="rs-media"><div class="rs-mh"><span>{inline(d["panel"])}</span>{chip(d.get("chip", ""))}</div>'
                    f'<div class="rs-mb">{inner}{cap}</div></figure>')
        return inner
    body = ""
    if d.get("chart"):
        spec = json.dumps(d["chart"], ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")
        fallback = esc(d["chart"].get("title", "")) + (". " + esc(d["chart"]["desc"]) if d["chart"].get("desc") else "")
        body = f'<div data-chart><script type="application/json">{spec}</script><noscript><p class="ck-cap">{fallback}</p></noscript></div>'
    elif d.get("html"):                       # local: a step-through or switch built by the course (several drawings and their notes)
        body = d["html"]
    elif d.get("glyph"):
        body = f'<div class="ck-tile" style="--w:{d.get("width", 300)}px">{glyph(d["glyph"])}</div>'
    elif d.get("svg"):
        svg = d["svg"]
        if "class=" not in svg[: svg.find(">")]:
            svg = svg.replace("<svg", '<svg class="ck-art"', 1)
        body = f'<div class="ck-tile" style="background:transparent;padding:4px 0;--w:{d.get("width", 520)}px">{svg}</div>' if not d.get("tile") else f'<div class="ck-tile" style="--w:{d.get("width", 300)}px">{svg}</div>'
    cap = f'<figcaption class="ck-cap">{inline(d["caption"])}</figcaption>' if d.get("caption") else ""
    return (f'<figure class="rs-media"><div class="rs-mh"><span>{inline(d.get("panel", "Drawing"))}</span>{chip(d.get("chip", ""))}</div>'
            f'<div class="rs-mb">{body}{cap}</div></figure>')


def idea_html(idea, n, total, links=None, video=None):
    fig_blocks = [b for b in idea["blocks"] if b["type"] == "figure"]
    drawings = idea.get("drawing")
    drawings = [] if not drawings else drawings if isinstance(drawings, list) else [drawings]
    prose_blocks = [b for b in idea["blocks"] if b["type"] != "figure"]
    if drawings:
        for d, fb in zip(drawings, fig_blocks):          # keep the write-up's caption with the redrawn figure
            d.setdefault("caption", fb["caption"])
        side = "".join(panel_html(d) for d in drawings)
    else:
        side = "".join(block_html(b) for b in fig_blocks)
    moments = ""
    if idea.get("moments"):
        rows = []
        for m in idea["moments"]:
            tm = (f'<a href="{esc(video)}&amp;t={seconds(m["time"])}s" rel="noopener" aria-label="Watch from {esc(m["time"])}">{esc(m["time"])}</a>'
                  if video else f'<span class="tm">{esc(m["time"])}</span>')
            rows.append(f"<li>{tm}<span>{inline(m['text'])}</span></li>")
        moments = f'<p class="lab" style="margin-top:8px">In the lecture</p><ul class="ck-moments">{"".join(rows)}</ul>'
    head = (f'<p class="eb">Idea {n} of {total}</p><h2 class="rs-h2">{turn_html(idea["heading"])}</h2>'
            + (f'<p class="ck-point">{inline(idea["point"])}</p>' if idea.get("point") else ""))
    prose = head + "".join(block_html(b, links) for b in prose_blocks) + moments
    wide = scene_block(idea["scene"]) if idea.get("scene") else ""
    if side:
        return f'<section class="ck-plate" id="idea-{n}"><div class="ck-prose">{prose}</div><div class="ck-side">{side}</div>{wide}</section>'
    return f'<section class="ck-plate" id="idea-{n}" style="grid-template-columns:minmax(0,1fr)"><div class="ck-prose">{prose}</div>{wide}</section>'


def page_shell(title, description, body, kit="../kit", extra_head=""):
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(title)}</title>
<meta name="description" content="{esc(description)}">
<link rel="stylesheet" href="{kit}/tokens.css">
<link rel="stylesheet" href="{kit}/boards.css">
<link rel="stylesheet" href="{kit}/course.css">
<link rel="stylesheet" href="{kit}/slides.css">
<link rel="stylesheet" href="{kit}/math/katex.min.css">
<script>try{{var t=localStorage.getItem('course-kit-theme');if(t)document.documentElement.setAttribute('data-theme',t)}}catch(e){{}}</script>
{extra_head}</head>
<body>
<a class="ck-skip" href="#main">Skip to the content</a>
<div class="root">
{body}
</div>
<script src="{kit}/charts.js"></script>
<script src="{kit}/course.js"></script>
</body>
</html>
"""

# ----------------------------------------------------------------------------- the lecture page

def render_lecture(doc, kit="../kit", course=None, links=None, nav=None):
    """doc: the lecture contract. course: {'title','mark','short'}. links: href -> href or None.
    nav: {'prev': {'href','title','text'}, 'next': {...}, 'index': href}."""
    course = course or {}
    nav = nav or {}
    n = doc.get("lecture", 0)
    short, rest = (doc["answer_short"], doc.get("answer_rest", "")) if doc.get("answer_short") else short_answer(doc["answer"])
    h1 = f'{esc(doc["question"])} <i>{esc(short)}</i>'
    lede = ("… " + esc(rest)) if rest else ""
    ideas = doc.get("ideas", [])
    title = doc.get("title") or f"Lecture {n}"
    parts = [hero_html(course.get("title", "Course"), course.get("mark", "c."), f"Lecture {n} · {title}",
                       f"Lecture {n} · one question, {len(ideas)} ideas", h1, lede, doc.get("cards"),
                       home=nav.get("home", "index.html"), long=len(doc["question"]) + len(short) > 120)]
    parts.append('<main id="main" style="display:contents">')
    parts.append(strip_html(doc.get("context"), f"Lecture {n}" + (f" of {course['count']}" if course.get("count") else "")))
    why, start = doc.get("why"), doc.get("start")
    if why or start:
        left = (section_head("Why this lecture", why["heading"]) + '<div class="ck-prose" style="margin-top:16px">' + "".join(block_html(b, links) for b in why["blocks"]) + "</div>") if why else ""
        right = (f'<aside class="card" aria-label="Where we start"><p class="rs-k">Where we start</p><h3>{esc(start["heading"])}</h3>'
                 + "".join(block_html(b, links) for b in start["blocks"]) + "</aside>") if start else ""
        parts.append(f'<section class="ck-concept ck-intro"><div>{left}</div><div>{right}</div></section>')
    if doc.get("scene"):
        parts.append('<section class="ck-sec" aria-label="The running example">' + scene_block(doc["scene"]) + "</section>")
    if ideas:
        jump = "".join(f'<li><a href="#idea-{i + 1}"><i>{i + 1}</i><span>{esc(split_turn(idea["heading"])[0])}</span></a></li>' for i, idea in enumerate(ideas))
        parts.append(f'<nav class="ck-jump" aria-label="Jump to an idea"><b>Ideas</b><ol>{jump}</ol></nav>')
        rail = "".join(f'<li><a href="#idea-{i + 1}"><span class="lab">Idea {i + 1} of {len(ideas)}</span><span>{esc(idea["heading"])}</span></a></li>' for i, idea in enumerate(ideas))
        parts.append(f'<nav aria-label="The argument, idea by idea"><p class="eb" style="margin:8px 0 12px">The argument</p><ol class="ck-rail" style="--n:{len(ideas) if len(ideas) <= 5 else (len(ideas) + 1) // 2}">{rail}</ol></nav>')
        for i, idea in enumerate(ideas):
            parts.append(idea_html(idea, i + 1, len(ideas), links, doc.get("source_url")))
    if doc.get("open"):
        o = doc["open"]
        parts.append('<section class="ck-sec">' + section_head("Still open", o["heading"]) + '<div class="ck-open">' + "".join(block_html(b, links) for b in o["blocks"]) + "</div></section>")
    if doc.get("check"):
        c = doc["check"]
        qs = "".join(f'<details class="ck-reveal"><summary><span class="rs-n">{i + 1}</span><span>{inline(q["q"])}</span></summary><div>{inline(q["a"])}</div></details>' for i, q in enumerate(c["items"]))
        parts.append('<section class="ck-sec">' + section_head("Check yourself", c["heading"]) + f'<div style="display:flex;flex-direction:column;gap:10px">{qs}</div></section>')
    if doc.get("connections"):
        c = doc["connections"]
        rows = []
        for i, it in enumerate(c["items"]):
            href = links(it["href"]) if (links and it.get("href")) else it.get("href")
            inner = f'<span class="rs-n">{i + 1}</span><b>{esc(it["title"])}</b><span>{inline(it["text"])}</span>'
            rows.append(f'<a class="ck-row" href="{esc(href)}">{inner}</a>' if href else f'<div class="ck-row">{inner}</div>')
        parts.append('<section class="ck-sec">' + section_head("Connections", c["heading"]) + f'<div class="ck-rows">{"".join(rows)}</div></section>')
    if doc.get("sources"):
        parts.append('<section class="ck-sec" aria-label="Sources"><p class="eb">Sources</p><ul class="ck-sources">' + "".join(f"<li>{inline(s)}</li>" for s in doc["sources"]) + "</ul></section>")
    parts.append("</main>")
    nx = ""
    if nav.get("prev"): nx += f'<a href="{esc(nav["prev"]["href"])}"><span class="rs-k" style="color:var(--peach)">Previous</span><b>{esc(nav["prev"]["title"])}</b><span>{esc(nav["prev"].get("text", ""))}</span></a>'
    if nav.get("next"): nx += f'<a class="r" href="{esc(nav["next"]["href"])}"><span class="rs-k" style="color:var(--peach)">Next</span><b>{esc(nav["next"]["title"])}</b><span>{esc(nav["next"].get("text", ""))}</span></a>'
    idx = f'<div class="rs-btns"><a class="ck-btn" href="{esc(nav["index"])}">All lectures</a></div>' if nav.get("index") else ""
    parts.append(f'<footer class="rs-close"><p class="eb">Lecture {n}, in one line</p><p class="rs-h2" style="max-width:26em">{esc(doc["answer"])}</p>'
                 + (f'<div class="ck-next">{nx}</div>' if nx else "") + idx + "</footer>")
    return page_shell(f"Lecture {n}: {title}", doc["question"], "\n".join(parts), kit)


def apply_visuals(doc, vis):
    """Merge a visuals file into the contract: cards, context, answer_short and one drawing per idea."""
    for k in ("cards", "context", "answer_short", "answer_rest", "title", "scene"):
        if k in vis: doc[k] = vis[k]
    for key, d in (vis.get("ideas") or {}).items():
        i = int(key) - 1
        if 0 <= i < len(doc["ideas"]): doc["ideas"][i]["drawing"] = d
    for key, d in (vis.get("scenes") or {}).items():
        i = int(key) - 1
        if 0 <= i < len(doc["ideas"]): doc["ideas"][i]["scene"] = d
    return doc


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("source", help="lecture .md (write-up format) or .json (contract)")
    ap.add_argument("--out", help="HTML file to write (default: print)")
    ap.add_argument("--kit", default="../kit", help="relative path from the page to the kit folder")
    ap.add_argument("--course", default="Course", help="course name for the top line")
    ap.add_argument("--mark", default="c.", help="one letter and a full stop for the brand square")
    ap.add_argument("--visuals", help="JSON with cards, context and one drawing per idea")
    ap.add_argument("--json", action="store_true", help="print the contract as JSON and stop")
    a = ap.parse_args(argv)
    src = Path(a.source)
    doc = json.loads(src.read_text()) if src.suffix == ".json" else parse_markdown(src.read_text())
    if a.visuals: apply_visuals(doc, json.loads(Path(a.visuals).read_text()))
    if a.json:
        print(json.dumps(doc, ensure_ascii=False, indent=1)); return
    page = render_lecture(doc, a.kit, {"title": a.course, "mark": a.mark})
    if a.out: Path(a.out).write_text(page)
    else: sys.stdout.write(page)


if __name__ == "__main__":
    main()
