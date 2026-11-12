"""Course story kit: builds a course site's landing page, course map, share page, video page and slide index in
the house style (Evidence Atlas, coffee and cream), and restyles the course's existing generated pages into the
same look with clear navigation (start here, previous / next, back to the course map).

The house assets in house/ (base.css, experience.css, theme-atlas.css, styles.css, icons.js, icons-extra.js,
art.js, charts.css, charts.js and the two Fraunces fonts) are copied unchanged from the ASDRP portfolio site.
course.css, course-art.js, course-charts.js, course-site.js and icons-course.js extend them in the same look.

Everything course-specific lives in content.py next to this file. This module only knows how to draw.
"""
from __future__ import annotations

import colorsys, hashlib, html, json, os, re, shutil
from pathlib import Path

from bs4 import BeautifulSoup

HERE = Path(__file__).resolve().parent
HOUSE = HERE / "house"
ALL_COURSES_URL = "https://github.com/mehtama1234/course-concept-library"  # the parent swaps this for the hub's address
CSS = ["base.css", "experience.css", "theme-atlas.css", "styles.css", "charts.css", "course.css"]
JS = ["course-data.js", "icons.js", "icons-extra.js", "icons-course.js", "art.js", "course-art.js", "charts.js", "course-charts.js", "course-site.js"]
MARKER = 'data-house="atlas"'
SERVED = {".html", ".css", ".js", ".json", ".svg", ".png", ".jpg", ".jpeg", ".webp", ".pdf", ".mp4", ".woff2", ".txt", ".csv", ".md", ".vtt"}


def esc(s) -> str:
    return html.escape(str(s), quote=True)


def ic(name: str) -> str:
    return f'<span class="lm-icon" data-icon="{name}"></span>'


# ---------------------------------------------------------------- the readability pass applied to every Markdown page
CALC = re.compile(r"(\d[\d.,]*\s*(?:[×x÷*/+−-]|=|percent|%)\s*\d)|(\d\s*(?:times|divided by)\s*\d)")
EXAMPLE_START = re.compile(r"^(Suppose|For example|For an illustrative|Consider|Imagine|As an illustration|In an illustrative|A worked example)", re.I)
SENT = re.compile(r"(?<=[.?!])\s+(?=[A-Z“\"(\[])")


def digest(html_text: str) -> str:
    """Breaks walls of text into short pieces without changing a word: a long paragraph becomes short
    paragraphs of at most two sentences, and a paragraph that works through numbers (or opens a worked
    illustration) goes into a marked "Worked example" box, so a reader can find the arithmetic at a glance."""
    soup = BeautifulSoup(html_text, "html.parser")
    for p in list(soup.find_all("p")):
        if p.find_parent(["li", "blockquote", "table", "td"]) or p.find(["code", "span"]) and len(p.get_text()) < 60:
            continue
        txt = p.get_text(" ", strip=True)
        arith = len(CALC.findall(txt)) >= 1 and len(re.findall(r"\d", txt)) >= 3
        is_calc = arith or bool(EXAMPLE_START.match(txt))
        inner = p.decode_contents()
        sents = SENT.split(inner) if len(txt.split()) > 45 and "<" not in re.sub(r"</?(a|b|strong|em|i)( [^>]*)?>", "", inner) else [inner]
        chunks = [" ".join(sents[i:i + 2]) for i in range(0, len(sents), 2)] if len(sents) > 2 else [inner]
        new = "".join(f"<p>{c}</p>" for c in chunks)
        if is_calc:
            prev = p.find_previous_sibling()
            if prev is not None and prev.name == "div" and "worked" in (prev.get("class") or []):
                prev.append(BeautifulSoup(new, "html.parser"))
                p.decompose()
                continue
            if arith or len(chunks) == 1:
                new = f'<div class="worked"><p class="lm-k">Worked example</p>{new}</div>'
            else:  # only the opening illustration goes in the box; the comment after it stays in the text
                new = f'<div class="worked"><p class="lm-k">Worked example</p><p>{chunks[0]}</p></div>' + "".join(f"<p>{c}</p>" for c in chunks[1:])
        p.replace_with(BeautifulSoup(new, "html.parser"))
    return str(soup)


class Kit:
    def __init__(self, C):
        self.C = C
        self.site: Path = C.SITE
        self.root: Path = C.ROOT
        self.titles: dict[str, str] = {}
        self.extra_charts: dict = {}

    # ---------------------------------------------------------------- paths and the page shell
    def base(self, rel: str) -> str:
        return "../" * rel.count("/")

    def nav_html(self, rel: str, b: str) -> str:
        cur = self.current_nav(rel)
        out = []
        for label, href, _match in self.C.NAV:
            a = ' aria-current="page"' if label == cur else ""
            out.append(f'<a href="{b}{href}"{a}>{esc(label)}</a>')
        return '<nav class="course-nav" aria-label="Main sections of the course">' + "".join(out) + "</nav>"

    def current_nav(self, rel: str) -> str:
        best, n = "", -1
        for label, href, match in self.C.NAV:
            for m in match:
                if (rel == m or (m.endswith("/") and rel.startswith(m))) and len(m) > n:
                    best, n = label, len(m)
        return best

    def shell(self, rel: str, title: str, description: str, body: str, og_extra: str = "", head_extra: str = "", body_class: str = "") -> str:
        C, b = self.C, self.base(rel)
        url = C.SITE_URL + rel.removesuffix("index.html")
        css = "".join(f'<link rel="stylesheet" href="{b}assets/{c}" />\n  ' for c in CSS)
        js = "".join(f'<script src="{b}assets/{j}"></script>' for j in JS)
        badges = "".join(f'<span class="badge">{esc(x)}</span>' for x in C.BADGES)
        desc = esc(re.sub(r"<[^>]+>", "", description))
        return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <meta name="theme-color" content="#F3ECE1" />
  <title>{esc(title)}</title>
  <meta name="description" content="{desc}" />
  <meta property="og:type" content="website" />
  <meta property="og:site_name" content="{esc(C.NAME)}" />
  <meta property="og:title" content="{esc(title)}" />
  <meta property="og:description" content="{desc}" />
  <meta property="og:url" content="{url}" />
  <meta property="og:image" content="{C.SITE_URL}presentation/slides/01-cover.jpg" />
  <meta property="og:image:width" content="1920" />
  <meta property="og:image:height" content="1080" />
  <meta property="og:image:alt" content="{esc(C.OG_ALT)}" />
  <meta name="twitter:card" content="summary_large_image" />
  <link rel="canonical" href="{url}" />
  {og_extra}<link rel="icon" href="{b}assets/icon.svg" type="image/svg+xml" />
  {css}{head_extra}
</head>
<body class="course-site {body_class}" {MARKER}>
  <aside class="public-demo-banner" aria-label="About this course">{C.BANNER}</aside>
  <a class="skip-link" href="#app">Skip to the page</a>
  <header>
    <a class="brand" href="{b}index.html"><span class="mark" aria-hidden="true">{esc(C.MARK)}</span> {esc(C.NAME)}</a>
    <span class="header-status">{badges}</span>
    <a class="header-link" href="{b}course-map.html">Course map</a>
  </header>
  {self.nav_html(rel, b)}
  <main id="app" tabindex="-1">
{body}
  </main>
  <footer class="course-foot">
    <p>{C.SOURCE_LINE}</p>
    <p class="foot-links"><a href="{ALL_COURSES_URL}">All courses</a><a href="{b}index.html">This course</a><a href="{b}course-map.html">Course map</a><a href="{b}presentation/index.html">Slides</a><a href="{b}video/index.html">Video</a><a href="{b}share/index.html">Share</a></p>
  </footer>
  {js}
</body>
</html>
"""

    def write(self, rel: str, title: str, description: str, body: str, **kw) -> None:
        p = self.site / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(self.shell(rel, title, description, body, **kw), encoding="utf-8")

    # ---------------------------------------------------------------- building blocks (same markup as the house pages)
    def heading(self, back, eyebrow, title, sub, art="", crumbs=""):
        a = f'<div class="hj-art" data-art="{esc(art)}"></div>' if art else ""
        bb = f'<a class="back-button" href="{back[0]}">← <span>{esc(back[1])}</span></a>' if back else ""
        s = f'<p class="hj-sub">{sub}</p>' if sub else ""
        return f'<div class="lm-head"><div class="hj-heading">{crumbs}{bb}<p class="eyebrow">{eyebrow}</p><h1 id="page-title">{title}</h1>{s}</div>{a}</div>'

    def chart(self, cid, kicker, title, text, note):
        return f'<div class="chart-card"><div data-chart="{cid}"></div><div><p class="lm-k">{kicker}</p><h3>{title}</h3><p>{text}</p><p class="chart-note">{note}</p></div></div>'

    def grid(self, items):
        return '<ul class="lm-grid">' + "".join(f'<li><div class="lm-top">{ic(i)}<p class="lm-k">{k}</p></div><h3>{h}</h3><p>{p}</p></li>' for i, k, h, p in items) + "</ul>"

    def cards(self, items, label="Cards"):
        return f'<ol aria-label="{esc(label)}" tabindex="0">' + "".join(f'<li><p class="lp-k">{k}</p><h3>{h}</h3><p class="lp-pain">{a}</p>{f"<p class=lp-fix>{b}</p>" if b else ""}</li>' for k, h, a, b in items) + "</ol>"

    def bridge(self, label, text, href, link):
        return f'<section class="landing-problems answer bridge"><p class="lp-energy"><b>{label}</b> {text} <a href="{href}">{link} →</a></p></section>'

    def section_head(self, sid, title, lead, art=""):
        a = f'<div class="hj-art" data-art="{art}"></div>' if art else ""
        return f'<div class="lm-head"><div><h2 class="landing-subhead" id="{sid}">{title}</h2><p class="lp-lead">{lead}</p></div>{a}</div>'

    def figure(self, wide, tall, caption, cls="course-fig"):
        t = f'<div class="loop-tall" data-art="{tall}"></div>' if tall else ""
        return f'<figure class="{cls}"><div class="loop-wide" data-art="{wide}"></div>{t}<figcaption>{caption}</figcaption></figure>'

    def landing_art(self, cards):
        """Four tilted cards like the house landing collage: [(kicker, title, line1, line2)]."""
        pos = [(14, 18, -2), (234, 66, 2), (18, 214, 1.5), (238, 236, -2)]
        out = ['<svg class="landing-art" viewBox="0 0 440 400" aria-hidden="true" focusable="false">',
               '<path class="la-line" d="M210 96 C 228 100, 222 120, 236 122"/><path class="la-line" d="M318 170 C 300 214, 250 204, 214 232"/><path class="la-line" d="M216 304 C 226 304, 228 302, 238 302"/>']
        for i, (k, t, a, b2) in enumerate(cards[:4]):
            x, y, r = pos[i]
            ink = " la-ink" if i == 2 else ""
            top = '<rect class="la-top" width="196" height="5"/>' if i == 0 else ""
            out.append(f'<g class="la-card{ink}" transform="translate({x} {y}) rotate({r})"><rect width="196" height="{116 if i > 1 else 104}"/>{top}<text class="la-kick" x="14" y="26">{esc(k)}</text><text class="la-title" x="14" y="56">{esc(t)}</text><text class="la-small" x="14" y="80">{esc(a)}</text><text class="la-small" x="14" y="96">{esc(b2)}</text></g>')
        out.append("</svg>")
        return "".join(out)

    def link_title(self, rel):
        return self.titles.get(rel) or rel

    # ---------------------------------------------------------------- assets
    def copy_assets(self):
        a = self.site / "assets"
        a.mkdir(parents=True, exist_ok=True)
        for f in HOUSE.iterdir():
            shutil.copyfile(f, a / f.name)
        self.write_data()

    def write_data(self):
        a = self.site / "assets"
        data = self.C.course_data(self)
        data.setdefault("charts", {}).update(self.extra_charts)
        (a / "course-data.js").write_text("// Written by scripts/course_story at build time from the course's own analysis files.\nwindow.CourseData = " + json.dumps(data, ensure_ascii=False) + ";\n", encoding="utf-8")
        (a / "icon.svg").write_text(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 192 192"><rect width="192" height="192" rx="42" fill="#9A4A22"/><text x="96" y="130" text-anchor="middle" font-family="Georgia,serif" font-size="{112 if len(self.C.MARK) < 3 else 80}" fill="#FBF6EE">{esc(self.C.MARK)}</text></svg>', encoding="utf-8")

    # ---------------------------------------------------------------- course notes written in Markdown
    def render_markdown(self):
        """Turns each course Markdown file listed in content.MARKDOWN into a plain page under site/, plus an index
        page for each group. The restyle pass then gives them the house layout like every other page.
        The .md files stay the source; links between them are rewritten to the new pages."""
        import markdown
        C = self.C
        made = {}
        srcs = lambda g: [self.root / f for f in g["files"]] if "files" in g else sorted(self.root.glob(g["glob"]))
        for g in C.MARKDOWN:
            for src in srcs(g):
                if src.name in g.get("skip", []):
                    continue
                made[src.resolve()] = f'{g["out"]}/{g.get("name", lambda s: s.stem)(src)}.html'
        for g in C.MARKDOWN:
            items = []
            for src in srcs(g):
                if src.resolve() not in made:
                    continue
                rel = made[src.resolve()]
                text = src.read_text(encoding="utf-8")
                body = digest(markdown.markdown(text, extensions=["tables", "fenced_code", "sane_lists"]))
                def fix(m, src=src, rel=rel):
                    href, frag = m.group(1), m.group(2) or ""
                    if re.match(r"[a-z]+:", href):
                        return m.group(0)
                    tgt = (src.parent / href).resolve()
                    if tgt in made:
                        return f'href="{os.path.relpath(made[tgt], os.path.dirname(rel))}{frag}"'
                    if tgt.exists():
                        return f'href="https://github.com/mehtama1234/{C.REPO}/blob/{C.BRANCH}/{tgt.relative_to(self.root).as_posix()}{frag}"'
                    return 'href="#"'
                body = re.sub(r'href="([^"#]*)(#[^"]*)?"', lambda m: m.group(0) if not m.group(1) else fix(m), body)
                m = re.search(r"<h1>(.*?)</h1>", body, re.S)
                title = re.sub(r"<[^>]+>", "", m.group(1)) if m else src.stem.replace("-", " ").title()
                if not m:
                    body = f"<h1>{esc(title)}</h1>" + body
                p1 = re.search(r"<p>(.*?)</p>", body, re.S)
                blurb = re.sub(r"<[^>]+>", "", p1.group(1))[:220] if p1 else ""
                if g.get("blurb"):
                    blurb = g["blurb"](src, title, blurb)
                src_note = f'<p class="meta">Written as <a href="https://github.com/mehtama1234/{C.REPO}/blob/{C.BRANCH}/{src.relative_to(self.root).as_posix()}">{esc(src.relative_to(self.root).as_posix())}</a> in the course repository.</p>'
                out = self.site / rel
                out.parent.mkdir(parents=True, exist_ok=True)
                out.write_text(f"<!doctype html><html lang=\"en\"><head><meta charset=\"utf-8\"><title>{esc(title)} · {esc(C.NAME)}</title></head><body><main>{body}{src_note}</main></body></html>", encoding="utf-8")
                items.append((rel, title, blurb))
            if g.get("index_body"):
                (self.site / g["index"]).write_text(f"<!doctype html><html lang=\"en\"><head><meta charset=\"utf-8\"><title>{esc(g['title'])} · {esc(C.NAME)}</title></head><body><main><h1>{esc(g['title'])}</h1><p>{g['intro']}</p>{g['index_body'](items)}</main></body></html>", encoding="utf-8")
                continue
            cards = "".join(f'<article class="card"><h3><a href="{os.path.relpath(r, os.path.dirname(g["index"]) or ".")}">{esc(t)}</a></h3><p>{esc(b)}</p></article>' for r, t, b in items)
            (self.site / g["index"]).write_text(f"<!doctype html><html lang=\"en\"><head><meta charset=\"utf-8\"><title>{esc(g['title'])} · {esc(C.NAME)}</title></head><body><main><h1>{esc(g['title'])}</h1><p>{g['intro']}</p><div class=\"grid\">{cards}</div></main></body></html>", encoding="utf-8")
        return len(made)

    # ---------------------------------------------------------------- restyling the existing pages
    @staticmethod
    def recolor(text: str) -> str:
        """Moves any colour written into an old page onto the house palette, by lightness."""
        def swap(m):
            h = m.group(1)
            if len(h) == 3:
                h = "".join(c * 2 for c in h)
            r, g, b = (int(h[i:i + 2], 16) / 255 for i in (0, 2, 4))
            l, s = colorsys.rgb_to_hls(r, g, b)[1:]
            if l > 0.93:
                return "#FBF7F0"
            if l > 0.82:
                return "#F5E6D3" if s > 0.25 else "#ECE4D5"
            if l > 0.62:
                return "#CDBFA9"
            if l < 0.28:
                return "#2B2622"
            if s < 0.15:
                return "#5A5047"
            return "#9A4A22" if l < 0.5 else "#B9764A"
        return re.sub(r"#([0-9a-fA-F]{6}|[0-9a-fA-F]{3})\b", swap, text)

    def legacy_style(self, css: str) -> str:
        css = self.recolor(css)
        for old, new in (("var(--accent)", "var(--rust)"), ("var(--card)", "var(--surface)"), ("var(--text)", "var(--ink)"), ("var(--bg)", "var(--paper)")):
            css = css.replace(old, new)
        # The old pages styled bare h1/h2/body/main; inside the house shell those rules must not reach the frame.
        css = re.sub(r"(^|[}\s,])(body|main|header|nav)(\s*[{,])", r"\1.prose-legacy-\2\3", css)
        return css

    @staticmethod
    def in_section(s, rel: str) -> bool:
        if "prefix" in s:
            return "/" not in rel and rel.startswith(s["prefix"]) and rel != s["index"]
        return rel.startswith(s["dir"] + "/")

    def section_of(self, rel: str):
        for s in self.C.SECTIONS:
            if self.in_section(s, rel):
                return s
        return None

    def orders(self, pages: list[str]) -> dict[str, list[str]]:
        """Reading order inside each folder, taken from the order its index page links to the pages."""
        out = {}
        for s in self.C.SECTIONS:
            idx = self.site / s["index"]
            seen = []
            if idx.exists():
                for href in re.findall(r'href="([^"#]+)', idx.read_text(encoding="utf-8")):
                    href = os.path.normpath(os.path.join(os.path.dirname(s["index"]), href)).replace("\\", "/")
                    if self.in_section(s, href) and href.endswith(".html") and href not in seen and href in pages:
                        seen.append(href)
            rest = sorted(p for p in pages if self.in_section(s, p) and p not in seen)
            for p in rest:  # an unlisted page goes right after the listed page it extends (x-deep.html after x.html)
                stem = p[:-5]
                host = max((q for q in seen if stem.startswith(q[:-5])), key=len, default=None)
                seen.insert(seen.index(host) + 1 if host else len(seen), p)
            out[s.get("dir") or s["prefix"]] = seen
        root_order = [h for _, _, hrefs in self.C.MAP_GROUPS for h in hrefs if "/" not in h]
        out[""] = root_order
        return out

    def restyle_all(self):
        C = self.C
        story = set(C.STORY_PAGES)
        pages = sorted(p.relative_to(self.site).as_posix() for p in self.site.rglob("*.html"))
        pages = [p for p in pages if p not in story and not p.startswith(("presentation/index.html", "video/index.html", "share/index.html")) and not any(p.startswith(x) for x in C.SKIP_RESTYLE)]
        raw = {p: (self.site / p).read_text(encoding="utf-8") for p in pages}
        for p, t in raw.items():
            m = re.search(r"<h1[^>]*>(.*?)</h1>", t, re.S)
            self.titles[p] = C.SHORT_TITLES.get(p) or (re.sub(r"<[^>]+>|\s+", " ", m.group(1)).strip() if m else p)
        order = self.orders(pages)
        n = 0
        for p in pages:
            if MARKER in raw[p]:
                continue
            (self.site / p).write_text(self.restyle(p, raw[p], order), encoding="utf-8")
            n += 1
        return n

    def restyle(self, rel: str, raw: str, order) -> str:
        C = self.C
        soup = BeautifulSoup(raw, "html.parser")
        title = soup.title.get_text().strip() if soup.title else self.titles[rel]
        styles = "".join(f"<style>{self.legacy_style(s.get_text())}</style>" for s in (soup.head.find_all("style") if soup.head else []))
        main = soup.find("main") or soup.body
        for sel in C.LEGACY_DROP:
            for el in main.select(sel):
                el.decompose()
        h1 = main.find("h1")
        h1_text = h1.get_text(" ", strip=True) if h1 else self.titles[rel]
        if h1:
            h1.decompose()
        info = {"eyebrow": "", "h1": h1_text, "sub": "", "art": "", "top": "", "title": title}
        sec = self.section_of(rel)
        info["eyebrow"] = sec["label"] if sec else C.ROOT_LABEL
        C.page_hook(self, rel, soup, main, info)
        self.section_icons(soup, main)
        self.term_cards(soup, main)
        # recolour inline colours inside the old content (SVG fills, style attributes)
        content = self.recolor(main.decode_contents())
        b = self.base(rel)
        # breadcrumb and previous / next
        if sec:
            back = (b + sec["index"], sec["label"])
            seq = order.get(sec.get("dir") or sec["prefix"], [])
            crumbs = f'<nav class="crumbs" aria-label="You are here"><a href="{b}course-map.html">Course map</a><span aria-hidden="true">›</span><a href="{b}{sec["index"]}">{esc(sec["label"])}</a></nav>'
        else:
            back = (b + "course-map.html", "Course map")
            seq = order.get("", [])
            crumbs = ""
        prev = nxt = None
        if rel in seq:
            i = seq.index(rel)
            prev = seq[i - 1] if i > 0 else None
            nxt = seq[i + 1] if i + 1 < len(seq) else None
        def pg(target, kind, cls):
            if not target:
                return f'<span class="{cls} empty"></span>'
            return f'<a class="{cls}" href="{os.path.relpath(target, os.path.dirname(rel) or ".")}"><span class="pg-k">{kind}</span><span class="pg-t">{esc(self.titles.get(target, target))}</span></a>'
        pager = f'<nav class="pager" aria-label="Previous and next">{pg(prev, "← Previous", "prev")}<a class="map" href="{back[0]}"><span class="pg-k">Back to</span><span class="pg-t">{esc(back[1])}</span></a>{pg(nxt, "Next →", "next")}</nav>'
        head = self.heading(back, esc(info["eyebrow"]), info["h1"] if "<" in info["h1"] else esc(info["h1"]), info["sub"], info["art"], crumbs)
        body = f"""    <section class="screen active landing legacy-page" aria-labelledby="page-title">
{head}
{info["top"]}
      <article class="prose">
{content}
      </article>
      {pager}
    </section>"""
        desc = info.get("desc") or re.sub(r"\s+", " ", BeautifulSoup(info["sub"] or content[:1500], "html.parser").get_text(" ")).strip()[:200]
        return self.shell(rel, title, desc, body, head_extra=styles)

    ICON_WORDS = [("lecture", "player-play"), ("video", "player-play"), ("transcript", "file-text"), ("source", "file-text"), ("evidence", "file-text"),
                  ("fail", "alert-triangle"), ("wrong", "alert-triangle"), ("mistake", "alert-triangle"), ("warning", "alert-triangle"), ("break", "alert-triangle"), ("limit", "alert-triangle"),
                  ("test", "checklist"), ("check", "checklist"), ("question", "help-circle"), ("example", "pencil-check"), ("case", "pencil-check"),
                  ("formula", "math-function"), ("equation", "math-function"), ("math", "math-function"), ("derivation", "math-function"),
                  ("picture", "chart-dots"), ("diagram", "chart-dots"), ("sketch", "chart-dots"), ("map", "map"), ("connect", "affiliate"), ("related", "link"), ("read", "books"),
                  ("problem", "target"), ("idea", "bulb"), ("plain", "message-circle"), ("words", "message-circle"), ("step", "route"), ("route", "route"), ("field", "world"), ("domain", "world"),
                  ("data", "chart-bar"), ("train", "refresh"), ("learn", "school"), ("file", "folder"), ("why", "help-circle"), ("how", "route")]

    def term_cards(self, soup, main):
        """A list whose items read "Term: explanation" becomes a grid of small cards, so long pages break into pieces."""
        for ul in main.find_all("ul"):
            lis = ul.find_all("li", recursive=False)
            if len(lis) < 3 or ul.find_parent(["nav", "details"]) or ul.get("class"):
                continue
            parts = []
            for li in lis:
                txt = li.decode_contents()
                m = re.match(r"\s*(?:<strong>|<b>)?([^<:]{2,60}?)(?:</strong>|</b>)?\s*:\s*(.+)$", txt, re.S)
                if not m or len(m.group(1).split()) > 8:
                    parts = None
                    break
                parts.append((m.group(1).strip(), m.group(2).strip()))
            if not parts:
                continue
            new = BeautifulSoup('<ul class="idea-cards">' + "".join(f'<li><p class="lm-k">{h}</p><p>{b}</p></li>' for h, b in parts) + "</ul>", "html.parser")
            ul.replace_with(new)

    def section_icons(self, soup, main):
        """Puts a house-style line icon beside every section heading, chosen from the words in the heading."""
        for h in main.find_all("h2"):
            if h.find(class_="h-icon"):
                continue
            words = h.get_text(" ", strip=True).lower()
            name = next((i for w, i in self.ICON_WORDS if w in words), "bulb")
            if name == "folder":
                name = "file-text"
            span = soup.new_tag("span")
            span["class"] = "lm-icon h-icon"
            span["data-icon"] = name
            span["aria-hidden"] = "true"
            h.insert(0, span)

    # ---------------------------------------------------------------- folding long drill sections on a page
    @staticmethod
    def fold(soup, container, keep, summary_k, summary_t, summary_more):
        """Moves every h2 section of `container` whose heading is not in `keep` into one closed details block
        at the end, closed until the reader opens it."""
        kids = list(container.children)
        sections, cur = [], None
        for k in kids:
            if getattr(k, "name", None) == "h2":
                cur = [k]
                sections.append(cur)
            elif cur is not None:
                cur.append(k)
        moved = [s for s in sections if s[0].get_text(" ", strip=True) not in keep]
        if not moved:
            return 0
        det = soup.new_tag("details")
        det["class"] = "drills"
        summ = soup.new_tag("summary")
        summ.append(BeautifulSoup(f'<p class="lm-k">{summary_k}</p><strong>{summary_t}</strong><span class="drill-more">{summary_more.format(n=len(moved))}</span>', "html.parser"))
        det.append(summ)
        bodyd = soup.new_tag("div")
        bodyd["class"] = "drill-body"
        det.append(bodyd)
        for s in moved:
            for el in s:
                el.extract()
                bodyd.append(el)
        container.append(det)
        return len(moved)

    # ---------------------------------------------------------------- the story pages
    def video_page(self):
        C = self.C
        return self.write("video/index.html", f"Video · {C.NAME}", C.VIDEO_DESC, f"""    <section class="screen active landing" aria-labelledby="page-title">
{self.heading(('../index.html', 'The big picture'), 'The video', 'The whole course, read aloud in about four minutes', 'The slides with their speaker notes read aloud, with captions you can turn on. The words are the same as on the slides and the website.', 'trio:presentation,player-play,share')}
      <video controls preload="metadata" playsinline poster="../presentation/slides/01-cover.jpg" style="width:100%;height:auto;border:1px solid var(--line);border-radius:var(--radius-card);background:#000">
        <source src="{C.VIDEO}.mp4" type="video/mp4">
        <track kind="captions" src="{C.VIDEO}.vtt" srclang="en" label="English" default>
      </video>
      <div class="landing-actions" style="margin-top:18px"><a class="button secondary" href="{C.VIDEO}.mp4" download>Download the video</a><a class="button secondary" href="{C.VIDEO}.vtt" download>Download the captions</a><a class="button secondary" href="../presentation/index.html">See the slides</a></div>
      <div class="landing-facts"><div class="landing-fact landing-fact-not"><h2>The voice is a computer voice reading the notes</h2><p>So anyone can rebuild the video from the course files. It follows the source course but is not made by its teachers.</p></div><div class="landing-fact"><h2>Share it with one link</h2><p>Send this page’s link, or download the video and captions. <a href="../share/index.html">Everything to share</a>.</p></div></div>
    </section>""", og_extra=f'<meta property="og:video" content="{C.SITE_URL}video/{C.VIDEO}.mp4" />\n  <meta property="og:video:type" content="video/mp4" />\n  <meta property="og:video:width" content="1920" />\n  <meta property="og:video:height" content="1080" />\n  ')

    def size(self, rel):
        f = self.site / rel
        return f"{f.stat().st_size / 1_048_576:.1f} MB" if f.exists() else "made with the slides"

    def n_slides(self):
        return len(list((self.site / "presentation/slides").glob("*.jpg")))

    def share_page(self):
        C, D = self.C, self.C.DECK

        def qr(name, label, href):
            return f'<li><a href="{href}"><img src="../assets/qr-{name}.svg" alt="QR code for {label}" width="180" height="180" style="width:100%;max-width:180px;background:#fff;border:1px solid var(--line);border-radius:var(--radius-card);padding:8px"></a><strong>{label}</strong><span>Point a phone camera at it.</span></li>'
        ns = self.n_slides() or "The"
        self.write("share/index.html", f"Share · {C.NAME}", f"Everything to share or present {C.NAME}: one link, a five-minute walkthrough, QR codes, slides, video and every download.", f"""    <section class="screen active landing" aria-labelledby="page-title">
{self.heading(('../index.html', 'The big picture'), 'Share', 'Everything you need to share or present this course, on one page', 'One link to send, a five-minute walkthrough, codes for phones in the room, and every file to download.', 'trio:share,qrcode,download')}
      <section class="landing-problems answer"><p class="lp-energy"><b>To share it, send one link:</b> <a href="../index.html">the big picture</a> <span>Everything else, including the slides, the video and every lesson, is linked from there. Once hosted, the address is {C.SITE_URL.removeprefix("https://")}</span></p></section>
      <section class="landing-problems" id="demo" aria-labelledby="demo-title">
        <h2 class="landing-subhead" id="demo-title">Walk someone through the course in five minutes</h2>
        <p class="lp-lead">One step per part of the story. Or skip the talking and play the video.</p>
        {self.cards(C.DEMO, label='Walkthrough steps')}
      </section>
      <section class="landing-more" aria-labelledby="present-title">
        {self.section_head('present-title', 'Pick the format that fits the room', 'The same story in every format.', 'trio:presentation,player-play,share')}
        {self.grid([
            ('presentation', 'Slides, full screen', f'{ns} slides', '<a href="../presentation/present.html">Present</a> with the arrow keys, or open the <a href="../presentation/presenter.html">presenter view</a> for notes and a timer.'),
            ('player-play', 'Video', 'Narrated, with captions', '<a href="../video/index.html">Play it here</a>, or download it below.'),
            ('home', 'Website', 'The big picture first', '<a href="../index.html">Start at the big picture</a>; every page links to the next step.'),
        ])}
      </section>
      <h2 class="landing-subhead">Codes for phones in the room</h2><p class="landing-demo-note">They point to the hosted address, {C.SITE_URL.removeprefix("https://")}, so they work once the site is published there.</p>
      <ol class="landing-demo qr-row" aria-label="QR codes" tabindex="0">
        {qr('website', 'Website', '../index.html')}{qr('slides', 'Slides', '../presentation/index.html')}{qr('video', 'Video', '../video/index.html')}{qr('share', 'This page', 'index.html')}
      </ol>
      <section class="landing-more" aria-labelledby="dl-title">
        {self.section_head('dl-title', 'Download a file to send, print or play offline', 'Files you can attach, upload, or open with no internet.')}
        {self.grid([
            ('presentation', 'Slides', 'PowerPoint, with speaker notes', f'<a href="../presentation/{D}.pptx" download>Download</a> ({self.size(f"presentation/{D}.pptx")}). Opens in PowerPoint, Keynote and Google Slides.'),
            ('file-text', 'Slides', 'PDF', f'<a href="../presentation/{D}.pdf" download>Download</a> ({self.size(f"presentation/{D}.pdf")}). For printing or sending.'),
            ('player-play', 'Video', 'MP4, full HD', f'<a href="../video/{C.VIDEO}.mp4" download>Download</a> ({self.size(f"video/{C.VIDEO}.mp4")}). Captions: <a href="../video/{C.VIDEO}.vtt" download>VTT file</a>.'),
            ('books', 'Every page', 'The course map', '<a href="../course-map.html">Every lesson and reference page</a>, grouped by what you want to do.'),
        ])}
      </section>
      <section class="landing-more" aria-labelledby="links-title">
        {self.section_head('links-title', 'Every link in one list', 'Copy any of these.')}
        <p class="landing-note">{''.join(f'<a href="{h}">{t}</a>' for t, h in [('The big picture', '../index.html'), ('Course map', '../course-map.html'), ('Slides', '../presentation/index.html'), ('Present full screen', '../presentation/present.html'), ('Presenter view', '../presentation/presenter.html'), ('Video', '../video/index.html'), ('All courses', ALL_COURSES_URL)] + [(t, '../' + h) for t, h in C.SHARE_EXTRA])}</p>
      </section>
      <div class="landing-facts">
        <div class="landing-fact"><h2>Every page is tested before it is shared</h2><p>Every page is opened in a browser at laptop and phone width: no errors, no missing files, nothing spilling sideways. The slide viewer, the presenter notes and the video are checked too.</p></div>
        <div class="landing-fact landing-fact-not"><h2>Say where it comes from</h2><p>{C.SHARE_CREDIT}</p></div>
      </div>
    </section>""")

    def course_map(self):
        C = self.C
        groups = []
        for title, lead, hrefs in C.MAP_GROUPS:
            items = []
            for h in hrefs:
                t, d = C.MAP_BLURBS.get(h, (self.titles.get(h, h), ""))
                items.append(f'<li><div class="lm-top">{ic(C.MAP_ICONS.get(h, "file-text"))}<p class="lm-k">{esc(h.removesuffix(".html").replace("-", " "))}</p></div><h3><a href="{h}">{esc(t)}</a></h3><p>{d}</p></li>')
            gid = re.sub(r"[^a-z0-9]+", "-", title.lower()).strip("-")[:40]
            groups.append(f'<section class="map-group" aria-labelledby="{gid}"><h2 class="landing-subhead" id="{gid}">{title}</h2><p class="lp-lead">{lead}</p><ul class="lm-grid">{"".join(items)}</ul></section>')
        self.write("course-map.html", f"Course map · {C.NAME}", C.MAP_DESC, f"""    <section class="screen active landing" aria-labelledby="page-title">
{self.heading(('index.html', 'The big picture'), 'Course map', C.MAP_H1, C.MAP_SUB, 'trio:map,route,books')}
{''.join(groups)}
      {self.bridge('New here?', C.MAP_NEW, C.START_HREF, 'Start here')}
    </section>""")

    def presentation_index(self, slides):
        C = self.C
        figs = "".join(f'<li><a href="present.html#{i}"><img src="slides/{n}.jpg" alt="Slide {i}: {esc(s["alt"])}" loading="{"eager" if i < 3 else "lazy"}" width="1920" height="1080" style="width:100%;height:auto;border:1px solid var(--line);border-radius:var(--radius-card)"></a><strong>{i} · {esc(s["alt"])}</strong></li>' for i, (n, s) in enumerate(slides, 1))
        self.write("presentation/index.html", f"Slides · {C.NAME}", f"The {len(slides)} slides for {C.NAME}, with speaker notes, a presenter view, PDF and PowerPoint.", f"""    <section class="screen active landing" aria-labelledby="page-title">
{self.heading(('../index.html', 'The big picture'), 'The slides', f'The whole course in {len(slides)} slides, ready to present', 'Built from the same words, charts and drawings as the website. Present full screen, open the presenter view with speaker notes, or download the PDF or PowerPoint.', 'trio:presentation,player-play,share')}
      <div class="landing-actions"><a class="button primary" href="present.html">Present <span aria-hidden="true">→</span></a><a class="button secondary" href="presenter.html">Presenter view with notes</a><a class="button secondary" href="{C.DECK}.pdf" download>Download PDF</a><a class="button secondary" href="{C.DECK}.pptx" download>Download PowerPoint</a><a class="button secondary" href="../video/index.html">Watch the video</a></div>
      <h2 class="landing-subhead">All {len(slides)} slides, each with its headline</h2><ol class="landing-demo deck-list" aria-label="All slides" tabindex="0">{figs}</ol>
    </section>""")

    def manifest(self):
        if not self.C.MANIFEST:
            return
        items = sorted(p.relative_to(self.root).as_posix() for p in self.site.rglob("*.html"))
        mp = self.site / "page-manifest.json"
        old = json.loads(mp.read_text()) if mp.exists() else []
        if isinstance(old, list) and old and not str(old[0]).startswith("site/"):
            items = [i.removeprefix("site/") for i in items]
        mp.write_text(json.dumps(items, indent=2) + "\n", encoding="utf-8")

    # ---------------------------------------------------------------- the publish folder
    def publish(self):
        C = self.C
        out = self.root / "publish"
        if out.exists():
            shutil.rmtree(out)
        raw = f"https://github.com/mehtama1234/{C.REPO}/raw/{C.BRANCH}/{self.site.relative_to(self.root).as_posix()}/"
        files, total = 0, 0
        for f in sorted(self.site.rglob("*")):
            if not f.is_file():
                continue
            rel = f.relative_to(self.site).as_posix()
            if f.suffix.lower() not in SERVED or any(re.search(x, rel) for x in C.PUBLISH_EXCLUDE):
                continue
            dst = out / rel
            dst.parent.mkdir(parents=True, exist_ok=True)
            if f.suffix == ".html":
                t = f.read_text(encoding="utf-8")
                t = re.sub(r'href="([^"]+\.pptx)"', lambda m: f'href="{raw}{os.path.normpath(os.path.join(os.path.dirname(rel), m.group(1))).replace(os.sep, "/")}"', t)
                dst.write_text(t, encoding="utf-8")
            else:
                shutil.copyfile(f, dst)
            files += 1
            total += dst.stat().st_size
        return out, files, total
