"""The research site on the board kit (kit/, vendored from course-concept-library at 9fcb0c2; see kit/VENDORED).
Ported from the topology course repo's scripts/course_story/boards.py (generic parts only).

Two jobs:
  1. install(site): copy the kit's styles, scripts and fonts, plus this site's site.css / site.js, to site/kit/,
     and remove the old house stylesheets and scripts.
  2. page(...): lay out any page body written by the generator with the kit's components: the espresso
     band with the page's question, answer and number cards; kit cards, steps, ledgers, reveal rows; the closing band.
Words are not changed here. This file only lays them out."""
from __future__ import annotations
import html, json, os, re, shutil, sys
from pathlib import Path
from bs4 import BeautifulSoup, NavigableString, Tag

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
KIT = ROOT / "kit"
sys.path.insert(0, str(KIT))
import render_lecture as R  # noqa: E402

esc = lambda s: html.escape(str(s), quote=True)
ALL_COURSES_URL = "https://github.com/mehtama1234/semiconductor-conferences"
KIT_FILES = ["tokens.css", "boards.css", "course.css", "slides.css", "charts.js", "course.js"]


def install(site: Path):
    out = site / "kit"
    if out.exists():
        shutil.rmtree(out)
    (out / "fonts").mkdir(parents=True)
    for f in KIT_FILES:
        shutil.copyfile(KIT / f, out / f)
    for f in (KIT / "fonts").iterdir():
        if f.suffix in (".woff2", ".txt"):
            shutil.copyfile(f, out / "fonts" / f.name)
    for f in ("site.css", "site.js"):
        shutil.copyfile(HERE / "board" / f, out / f)
    (out / "math" / "fonts").mkdir(parents=True)
    shutil.copyfile(KIT / "math" / "katex.min.css", out / "math" / "katex.min.css")
    shutil.copyfile(KIT / "math" / "LICENSE-KaTeX.txt", out / "math" / "LICENSE-KaTeX.txt")
    for f in (KIT / "math" / "fonts").glob("*.woff2"):
        shutil.copyfile(f, out / "math" / "fonts" / f.name)
    # the old house kit: stylesheets, icon scripts and the reused pictures
    a = site / "assets"
    for f in list(a.glob("*.css")) + list(a.glob("*.js")) + list(a.glob("*.woff2")):
        if f.name != "playground.js":
            f.unlink()
    if (a / "page-styles").exists():
        shutil.rmtree(a / "page-styles")


# ----------------------------------------------------------------------------------------- math

SUP = dict(zip("⁰¹²³⁴⁵⁶⁷⁸⁹ⁿᵐᵏⁱ⁺⁻ˡ", "0123456789nmki+−l"))
SUB = dict(zip("₀₁₂₃₄₅₆₇₈₉ₙᵢₖₘ₊₋", "0123456789nikm+−"))


def math_html(s: str) -> str:
    """Plain-text mathematics (as the write-ups store it) set with real layout: italic variables, raised and
    lowered indices, stacked fractions. Words between formulas stay upright."""
    t = html.escape(s, quote=False)
    t = re.sub(r"\^\(([^()]+)\)", lambda m: f"<sup>{m.group(1)}</sup>", t)
    t = re.sub(r"_\{([^{}]+)\}|_([A-Za-z0-9])", lambda m: f"<sub>{m.group(1) or m.group(2)}</sub>", t)
    t = re.sub("[" + "".join(SUP) + "]+", lambda m: "<sup>" + "".join(SUP[c] for c in m.group(0)) + "</sup>", t)
    t = re.sub("[" + "".join(SUB) + "]+", lambda m: "<sub>" + "".join(SUB[c] for c in m.group(0)) + "</sub>", t)
    t = re.sub(r"(?<![\w/.])(\d+|[a-z])/(\d+|[a-z])(?![\w/])", r'<span class="ck-frac"><span>\1</span><span>\2</span></span>', t)

    def var(m):
        w, after = m.group(1), m.group(2)
        if w in ("a", "A", "I") and re.match(r" [a-z]{2,}", after):
            return w + after[:0]
        return f"<var>{w}</var>"
    parts = re.split(r"(<[^>]+>)", t)
    for i, p in enumerate(parts):
        if not p.startswith("<"):
            parts[i] = re.sub(r"(?<![A-Za-zÀ-ÿ’'])([A-Za-zχβΣΓπλδαθφ])(?![A-Za-zÀ-ÿ’'])(?=((?: [a-z]{2,})?))", var, p)
    return "".join(parts)


# ----------------------------------------------------------------------------------------- shell

def shell(C, rel, title, description, hero, main, close, head_extra=""):
    b = "../" * rel.count("/")
    url = C.SITE_URL + rel.removesuffix("index.html")
    desc = esc(re.sub(r"\s+", " ", re.sub(r"<[^>]+>", "", description)).strip())
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="theme-color" content="#3a2e26">
<title>{esc(title)}</title>
<meta name="description" content="{desc}">
<meta property="og:type" content="website">
<meta property="og:site_name" content="{esc(C.NAME)}">
<meta property="og:title" content="{esc(title)}">
<meta property="og:description" content="{desc}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{C.SITE_URL}presentation/slides/01-cover.jpg">
<meta property="og:image:width" content="1920">
<meta property="og:image:height" content="1080">
<meta property="og:image:alt" content="{esc(C.OG_ALT)}">
<meta name="twitter:card" content="summary_large_image">
<link rel="canonical" href="{url}">
<link rel="icon" href="{b}assets/icon.svg" type="image/svg+xml">
<link rel="stylesheet" href="{b}kit/tokens.css">
<link rel="stylesheet" href="{b}kit/boards.css">
<link rel="stylesheet" href="{b}kit/course.css">
<link rel="stylesheet" href="{b}kit/slides.css">
<link rel="stylesheet" href="{b}kit/math/katex.min.css">
<link rel="stylesheet" href="{b}kit/site.css">
<script>try{{var t=localStorage.getItem('course-kit-theme');if(t)document.documentElement.setAttribute('data-theme',t)}}catch(e){{}}</script>
{head_extra}</head>
<body data-kit="boards">
<a class="ck-skip" href="#main">Skip to the content</a>
<div class="root">
{hero}
<main id="main" class="ck-main" tabindex="-1">
{main}
</main>
{close}
</div>
<script src="{b}kit/charts.js"></script>
<script src="{b}kit/course.js"></script>
<script src="{b}kit/site.js"></script>
</body>
</html>
"""


def current_nav(C, rel):
    best, n = "", -1
    for label, href, match in C.NAV:
        for m in match:
            if (rel == m or rel.startswith(m)) and len(m) > n:
                best, n = label, len(m)
    return best


def hero(C, rel, eyebrow, h1, lede="", cards=None, extra="", long=None):
    """The espresso band: brand and section links, the page's question with its answer in italic, number cards."""
    b = "../" * rel.count("/")
    cur = current_nav(C, rel)
    nav = "".join(f'<a href="{b}{href}"{" aria-current=page" if label == cur else ""}>{esc(label)}</a>' for label, href, _ in C.NAV)
    side = R.cards_html(cards) if isinstance(cards, list) else (cards or "")
    grid = "rs-hg" if side else "rs-hg solo"
    plain = re.sub(r"<[^>]+>", "", h1)
    long = len(plain) > 120 if long is None else long
    return (f'<header class="rs-hero"><div class="rs-top"><a class="rs-brand" href="{b}index.html"><i>{esc(C.MARK)}</i>{esc(C.NAME)}</a>'
            f'<span class="rs-r"><nav class="ck-nav" aria-label="Main sections of the site">{nav}</nav>'
            f'<button type="button" class="ck-theme" aria-label="Change colour theme">Theme: auto</button></span></div>'
            f'<div class="{grid}"><div><p class="eb">{eyebrow}</p><h1 class="rs-h1{" long" if long else ""}" id="page-title">{h1}</h1>'
            + (f'<p class="rs-lede">{lede}</p>' if lede else "") + extra + f"</div>{side}</div></header>")


def close_band(C, rel, eyebrow, line, prev=None, nxt=None, buttons=()):
    b = "../" * rel.count("/")
    nx = ""
    if prev: nx += f'<a href="{esc(prev[0])}"><span class="rs-k" style="color:var(--peach)">Previous</span><b>{esc(prev[1])}</b></a>'
    if nxt: nx += f'<a class="r" href="{esc(nxt[0])}"><span class="rs-k" style="color:var(--peach)">Next</span><b>{esc(nxt[1])}</b></a>'
    btn = "".join(f'<a class="ck-btn{" pri" if i == 0 else ""}" href="{esc(h)}">{esc(t)}</a>' for i, (h, t) in enumerate(buttons))
    links = "".join(f'<a href="{h}">{t}</a>' for h, t in [(ALL_COURSES_URL, "Source on GitHub"), (b + "index.html", "The big picture"), (b + "course-map.html", "Every page"),
                                                         (b + "presentation/index.html", "Slides"), (b + "video/index.html", "Video"), (b + "share/index.html", "Share")])
    return (f'<footer class="rs-close"><p class="eb">{eyebrow}</p><p class="rs-h2" style="max-width:26em">{line}</p>'
            + (f'<div class="ck-next">{nx}</div>' if nx else "") + (f'<div class="rs-btns">{btn}</div>' if btn else "")
            + f'<p class="rs-src">{C.SOURCE_LINE}</p><p class="ck-footlinks">{links}</p></footer>')


def answer_h1(question, answer):
    """The headline: the question, then the answer in italic."""
    if not answer:
        return R.turn_html(question)
    q = question if question.rstrip()[-1:] in ".?!:" else question.rstrip() + "."
    return f'{esc(q)} <i>{esc(answer)}</i>'


def first_sentence(text):
    m = re.match(r"(.+?[.?!])(\s+|$)(.*)", text.strip(), re.S)
    return (m.group(1), m.group(3).strip()) if m else (text.strip(), "")


# ----------------------------------------------------------------------------------------- old markup -> kit components

DROP = "[data-art], .hj-art, figure.course-fig, .method-figure, nav.crumbs, a.back-button, .chart-card, span.lm-icon, span.h-icon, [data-icon], li.step-fig, span.step-n, details.contents"
GRID_LISTS = "ul.idea-cards, ul.short-cards, ul.lm-grid, ul.label-cards, ol.landing-demo:not(.qr-row), section.landing-problems > ol, div.grid, div.who-for"


def kitify(soup, root):
    """Rewrite the generator's markup into the kit's components, in place."""
    new = soup.new_tag
    for el in root.select(DROP):
        el.decompose()
    for el in root.select(".lm-top"):
        el.unwrap()
    # steps
    for ol in root.select("ol.lesson-steps, ol.reason"):
        lesson = "lesson-steps" in ol.get("class", [])
        ol["class"] = ["ck-steps"] + (["ck-lesson"] if lesson else [])
        for li in ol.find_all("li", recursive=False):
            if lesson:
                for h in li.select("h2.step-h"):
                    h.name = "h3"; h["class"] = ["ck-step-h"]
            else:
                d = new("div"); d.extend(list(li.contents)); li.clear(); li.append(d)
    for h in root.select("h2.step-h"):
        h["class"] = [c for c in h.get("class", []) if c != "step-h"]
    # worked examples
    for a in root.select("aside.worked"):
        proof = "wu-proof" in a.get("class", [])
        sec = new("section"); sec["class"] = ["ck-ledger"]
        hd = new("header"); h4 = new("h4")
        h3 = a.find("h3")
        if h3: h4.extend(list(h3.contents))
        hd.append(h4)
        chip = BeautifulSoup(R.chip("worked out" if proof else "from the lecture"), "html.parser")
        k = a.find(class_="lm-k")
        if k and not proof and "Worked" not in k.get_text(): chip = BeautifulSoup("", "html.parser")
        hd.append(chip); sec.append(hd)
        ol = new("ol")
        for li in a.select("ol.worked-lines > li"):
            n = new("li"); d = new("div"); d.extend(list(li.contents)); n.append(d); ol.append(n)
        take = a.find(class_="worked-take")
        if take:
            n = new("li"); n["class"] = ["res"]; d = new("div"); d.extend(list(take.contents)); n.append(d); ol.append(n)
        sec.append(ol); a.replace_with(sec)
    for sp in root.select("span.wu-uses"):
        sp["class"] = ["ck-uses"]
    # worked numbers boxed by the readability pass (kit.digest)
    for d in root.select("div.worked"):
        k = d.find(class_="lm-k")
        if k: k.decompose()
        sec = new("section"); sec["class"] = ["ck-ledger"]
        hd = new("header"); h4 = new("h4"); h4.string = "Worked example, with the numbers"; hd.append(h4)
        hd.append(BeautifulSoup(R.chip("from the papers"), "html.parser")); sec.append(hd)
        ol = new("ol")
        for p in d.find_all("p", recursive=False):
            li = new("li"); dv = new("div"); dv.extend(list(p.contents)); li.append(dv); ol.append(li)
        sec.append(ol); d.replace_with(sec)
    # be careful
    for p in root.select("p.careful"):
        p["class"] = ["ck-careful"]
        b = p.find("b")
        if b and b == next((c for c in p.contents if not (isinstance(c, NavigableString) and not c.strip())), None):
            b.string = b.get_text().rstrip(": ")
        else:
            nb = new("b"); nb.string = "Note"; p.insert(0, nb)
    # questions with answers
    n = 0
    for d in root.select("details"):
        s = d.find("summary")
        if not s: continue
        if "answer" in d.get("class", []):
            n += 1
            d["class"] = ["ck-reveal"]
            q = new("span"); q.extend(list(s.contents)); s.clear()
            num = new("span"); num["class"] = ["rs-n"]; num.string = str(n)
            s.append(num); s.append(q)
            body = new("div")
            for c in [c for c in d.contents if c is not s]:
                body.append(c.extract())
            for p in body.find_all("p"): p.unwrap()
            d.append(body)
        else:
            d["class"] = ["ck-fold"]
    # grids of cards
    for ul in root.select(GRID_LISTS):
        items = [c for c in ul.children if isinstance(c, Tag)]
        if not items: continue
        g = new("div"); g["class"] = ["ck-grid", "g3" if len(items) % 3 == 0 or len(items) > 4 else "g2"]
        for li in items:
            art = new("article"); art["class"] = ["card"]
            if li.name in ("li", "div", "article"):
                art.extend(list(li.contents))
            else:
                art.append(li.extract())
            for b in art.find_all("b", recursive=False):   # who-for blocks: a bold label then a paragraph
                b.name = "h3"
            g.append(art)
        ul.replace_with(g)
    for el in root.select("section.screen, article.prose, section.landing-problems, section.landing-more, section.map-group, div.landing-facts, section.lecture, section.fp, div.essay"):
        el.unwrap()
    for p in root.select("p.lm-k, p.lp-k"):
        p["class"] = ["rs-k"]
    for p in root.select("p.lp-pain, p.lp-fix, p.lp-lead, p.lead, p.landing-demo-note, p.landing-note, p.chart-note, p.muted, p.meta, p.moment, p.lp-energy"):
        cls = p.get("class", [])
        p["class"] = ["rs-in"] if ("lp-lead" in cls or "lead" in cls) else ["ck-links"] if "landing-note" in cls else ["rs-ans"] if "lp-fix" in cls else ["mut"]
    # label: text lists
    for ul in root.select("ul.short-lines, ul.wu-where, ul.req-list"):
        ul["class"] = ["ck-kv"]
    # headings
    for h in root.find_all("h2"):
        if h.find_parent(class_="card") or h.find_parent(class_="landing-fact") or h.find_parent("summary"):
            h.name = "h3"; continue
        wrap = new("div"); wrap["class"] = ["rs-sh"]
        text = h.get_text(" ", strip=True)
        h["class"] = ["rs-h2"]
        if not h.find(["a", "code"]):
            h.clear(); h.append(BeautifulSoup(R.turn_html(text), "html.parser"))
        h.wrap(wrap)
    for d in root.select("div.landing-actions"):
        d["class"] = ["rs-btns"]
    for f in root.select("figure.wu-fig"):
        f["class"] = ["ck-fig"]
    for d in root.select("dl.wu-defs"):
        d["class"] = ["ck-defs"]
    return root


GLOSSED: dict[str, list] = {}
GLOSS_SKIP = {"a", "code", "h1", "h2", "h3", "h4", "figure", "svg", "script", "summary", "th", "title", "style", "var", "sup", "sub"}


def gloss(soup, root):
    """First use of each field term on the page gets its plain meaning in brackets (glossary.py), unless the
    same sentence already explains it. Returns the terms glossed, for the clarity log."""
    from course_story.glossary import GLOSS
    pats = {k: re.compile(v[1]) for k, v in GLOSS.items()}
    done, added = set(), []
    for node in list(root.find_all(string=True)):
        if not node.strip() or any(p.name in GLOSS_SKIP or "ck-cards" in (p.get("class") or []) or "ck-gloss" in (p.get("class") or []) for p in node.parents if getattr(p, "name", None)):
            continue
        text = str(node)
        hits = []
        for k, pat in pats.items():
            if k in done:
                continue
            m = pat.search(text)
            if m:
                done.add(k)
                after = text[m.end():m.end() + 60]
                if re.match(r"\s*(\(|,\s+(a|an|the|which|meaning|where)\b|\s+(is|means|refers)\b|:)", after):
                    continue
                hits.append((m.end(), k))
        if not hits:
            continue
        pos, parts = 0, []
        for end, k in sorted(hits):
            parts.append(text[pos:end])
            sp = soup.new_tag("span"); sp["class"] = ["ck-gloss"]; sp.string = f" ({GLOSS[k][0]})"
            parts.append(sp); pos = end
            added.append(k)
        parts.append(text[pos:])
        for x in parts:
            node.insert_before(x if not isinstance(x, str) else NavigableString(x))
        node.extract()
    return added


def auto_cards(root, extra=None):
    """Number cards for a page with no designed ones: what the page itself holds, counted."""
    text = root.get_text(" ", strip=True)
    words = len(text.split())
    cards = list(extra or [])
    n_cards = len(root.select(".card")); n_q = len(root.select(".ck-reveal")); n_h = len(root.select("h2")); n_rows = len(root.select("tbody tr, .ck-tw tr")) or 0
    lect = sorted(set(int(x) for x in re.findall(r'lecture-(\d\d)\.html', str(root))))
    if n_cards >= 3: cards.append({"label": "On this page", "value": f"{n_cards} cards", "note": "each one stands alone"})
    if n_q: cards.append({"label": "Check yourself", "value": f"{n_q} questions", "note": "each with a model answer"})
    if len(lect) >= 2: cards.append({"label": "Lectures", "value": f"{len(lect)} linked", "note": f"lecture {lect[0]} to lecture {lect[-1]}"})
    if n_h >= 3 and len(cards) < 3: cards.append({"label": "Sections", "value": f"{n_h} parts", "note": "each heading states its point"})
    if n_rows >= 4 and len(cards) < 3: cards.append({"label": "Table", "value": f"{n_rows} rows", "note": "one per case"})
    cards.append({"label": "Reading time", "value": f"{max(1, round(words / 200))} min", "note": f"{words:,} words at 200 a minute"})
    return cards[:4]


def page(kit, rel, title, description, body, og_extra="", head_extra=""):
    """Lay out one page body from the generator on the kit. Called for every page that is not built natively."""
    C = kit.C
    soup = BeautifulSoup(body, "html.parser")
    b = "../" * rel.count("/")
    hd = soup.select_one(".lm-head, .landing-hero")
    eyebrow, h1, sub = C.ROOT_LABEL, title, ""
    if hd:
        e = hd.select_one(".eyebrow, .landing-kicker"); h = hd.find("h1"); s = hd.select_one(".hj-sub, .landing-lede")
        eyebrow = e.decode_contents() if e else eyebrow
        h1 = h.get_text(" ", strip=True) if h else title
        sub = s.decode_contents() if s else ""
        hd.decompose()
    pager = soup.select_one("nav.pager")
    prev = nxt = None
    back = None
    if pager:
        for a in pager.find_all("a"):
            t = a.select_one(".pg-t").get_text(" ", strip=True) if a.select_one(".pg-t") else a.get_text(" ", strip=True)
            cls = a.get("class", [])
            if "prev" in cls: prev = (a["href"], t)
            elif "next" in cls: nxt = (a["href"], t)
            elif "map" in cls: back = (a["href"], t)
        pager.decompose()
    kitify(soup, soup)
    glossed = gloss(soup, soup)
    if glossed:
        GLOSSED[rel] = glossed
    info = getattr(kit, "page_extra", {}).get(rel) or {}
    if not info:
        from course_story import visuals
        info = visuals.page_visuals(rel)
    plain_sub = re.sub(r"<[^>]+>", "", sub).strip()
    if "?" in h1 and plain_sub:
        ans, rest = first_sentence(plain_sub); head_h1 = answer_h1(h1, ans); lede = esc(rest)
    elif plain_sub and len(h1) + len(first_sentence(plain_sub)[0]) < 150 and "<a" not in sub:
        ans, rest = first_sentence(plain_sub); head_h1 = answer_h1(h1, ans); lede = esc(rest)
    else:
        head_h1 = R.turn_html(h1); lede = sub
    cards = info.get("cards") or auto_cards(soup)
    top = ""
    if info.get("panels"):
        figs = [p["html"] if p.get("html", "").startswith("<figure") else R.panel_html(p) for p in info["panels"]]
        wide = any("ck-scene" in f for f in figs) or len(figs) == 1
        top = f'<section class="ck-pagefig{" ck-wide" if wide else ""}">' + "".join(figs) + "</section>"
    crumb = [{"label": "You are here", "value": f"[Every page]({b}course-map.html)" + (f" › [{back[1]}]({back[0]})" if back and "course-map" not in back[0] else "")}]
    strip = R.strip_html(crumb, re.sub(r"<[^>]+>", "", eyebrow))
    main = strip + top + f'<div class="ck-doc">{soup.decode()}</div>'
    one, _ = first_sentence(plain_sub) if plain_sub else (h1, "")
    close = close_band(C, rel, "This page, in one line", esc(one), prev, nxt, [(back[0], "Back to " + back[1])] if back else [(b + "course-map.html", "Course map")])
    return shell(C, rel, title, description, hero(C, rel, eyebrow, head_h1, lede, cards), main, close, head_extra=og_extra + head_extra)


# ----------------------------------------------------------------------------------------- lecture pages from the write-ups


def components_roles(roles):
    sys.path.insert(0, str(KIT))
    import components
    return components.role_cards(roles)
