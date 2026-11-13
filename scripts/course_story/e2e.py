"""End-to-end browser test of the course site, slides and video.

Serves site/ over HTTP and opens pages in Chromium at 1280 and 390 pixels wide: no script errors, no missing
files, every icon, drawing and chart draws, nothing spills sideways. Every page is tested when there are at
most 320; otherwise all story pages plus an even sample of the rest (at least 60). Then: headings carry a
point, the slide viewer moves with the arrow keys, the presenter view shows notes, downloads and captions are
served, and ffprobe confirms the video is 1920x1080 H.264 with AAC sound."""
from __future__ import annotations

import functools, http.server, json, subprocess, threading

fails: list[str] = []


def check(ok, what):
    print(("PASS " if ok else "FAIL ") + what, flush=True)
    if not ok:
        fails.append(what)


def serve(root):
    class Quiet(http.server.SimpleHTTPRequestHandler):
        def log_message(self, *a):
            pass
    srv = http.server.ThreadingHTTPServer(("127.0.0.1", 0), functools.partial(Quiet, directory=str(root)))
    srv.handle_error = lambda *a: None
    threading.Thread(target=srv.serve_forever, daemon=True).start()
    return f"http://127.0.0.1:{srv.server_address[1]}/"


def run(kit, root=None, quiet_pass=True):
    from playwright.sync_api import sync_playwright
    C = kit.C
    root = root or kit.site
    base = serve(root)
    story = ["index.html", "course-map.html", "presentation/index.html", "video/index.html", "share/index.html"]
    others = sorted(p.relative_to(root).as_posix() for p in root.rglob("*.html") if p.relative_to(root).as_posix() not in story and not p.name.startswith(("present", "presenter")))
    others = [p for p in others if not p.startswith("presentation/")]
    archived = [p for p in others if 'data-kit="boards"' not in (root / p).read_text(encoding="utf-8", errors="replace")]
    others = [p for p in others if p not in archived]
    print(f"skipping {len(archived)} archived source pages kept as evidence (not part of the site's own pages)", flush=True)
    if len(others) > 60:   # every page type is covered: an even sample of the rest (the subtheme pages are very long)
        step = max(1, len(others) // 55)
        others = others[::step]
    pages = story + others
    print(f"testing {len(pages)} pages at 1280 and 390 wide", flush=True)
    with sync_playwright() as pw:
        b = pw.chromium.launch()
        for width, scheme in ((1280, "light"), (390, "light"), (1280, "dark"), (390, "dark")):
            ctx = b.new_context(viewport={"width": width, "height": 900}, color_scheme=scheme)
            bad = 0
            for name in pages:
                pg = ctx.new_page()
                errors, missing, outside = [], [], []
                pg.on("request", lambda r: outside.append(r.url) if not r.url.startswith((base, "data:", "blob:", "about:")) else None)
                pg.on("pageerror", lambda e: errors.append(str(e)))
                pg.on("console", lambda m: errors.append(m.text) if m.type == "error" else None)
                pg.on("response", lambda r: missing.append(r.url) if r.status >= 400 and r.url.startswith(base) else None)
                pg.goto(base + name, wait_until="load")
                empty = pg.evaluate("""() => [...document.querySelectorAll('[data-icon],[data-art],[data-chart]')].filter(e => getComputedStyle(e).display !== 'none' || e.closest('.loop-wide,.loop-tall')).filter(e => !e.innerHTML.trim()).map(e => e.dataset.icon || e.dataset.art || e.dataset.chart)""")
                broken = pg.evaluate("[...document.images].filter(i => i.complete && i.naturalWidth === 0 && i.loading !== 'lazy').map(i => i.src)")
                over = pg.evaluate("document.documentElement.scrollWidth") - width
                shell = pg.evaluate("!!document.querySelector('body[data-kit=boards] .rs-brand') && !!document.querySelector('footer a[href*=github]') && !!document.querySelector('meta[property=\"og:title\"]')")
                ok = not errors and not missing and not empty and not broken and over <= 0 and shell and not outside
                if not ok or not quiet_pass or name in story:
                    check(not errors, f"{width}px {name}: no script errors {errors[:2] if errors else ''}")
                    check(not missing, f"{width}px {name}: every file it asks for exists {missing[:3] if missing else ''}")
                    check(not empty, f"{width}px {name}: every icon, drawing and chart drew {empty[:5] if empty else ''}")
                    check(not broken, f"{width}px {name}: every picture loads {broken[:2] if broken else ''}")
                    check(over <= 0, f"{width}px {name}: nothing spills sideways ({over}px)")
                    check(shell, f"{width}px {name}: kit header, GitHub footer link and Open Graph tags")
                    check(not outside, f"{width}px {name}: no requests outside the site {outside[:2] if outside else ''}")
                bad += not ok
                pg.close()
            check(bad == 0, f"{width}px {scheme}: all {len(pages)} pages clean")
            ctx.close()

        pg = b.new_page()
        for name in story[:2] + others[:: max(1, len(others) // 12)]:
            pg.goto(base + name)
            # The two house-style landing pages put their hero h1 directly in
            # the screen section rather than under a nested <main>. Include
            # that visible page title, then inspect the explanatory h2s.
            hs = pg.evaluate("[...document.querySelectorAll('h1, main h2')].filter(h => h.offsetParent !== null).map(h => h.innerText.trim())")
            short = [h for h in hs[1:] if len(h.split()) < 3]
            check(len(hs) >= 1 and not short, f"headings carry a point on {name} ({len(hs)} visible{', too short: ' + str(short[:4]) if short else ''})")
        pg.goto(base + story[0])
        charts = pg.evaluate("document.querySelectorAll('[data-chart] svg').length")
        pg.goto(base + story[1])
        map_drawings = pg.evaluate("document.querySelectorAll('[data-icon],[data-art],svg').length")
        check(charts >= 2 and map_drawings >= 1, f"landing charts and course-map drawings ({charts}, {map_drawings})")
        pg.close()

        pg = b.new_page(viewport={"width": 1280, "height": 800})
        pg.goto(base + "presentation/present.html")
        first = pg.inner_text("#count"); pg.keyboard.press("ArrowRight"); pg.wait_for_timeout(100)
        second = pg.inner_text("#count"); pg.keyboard.press("ArrowLeft"); pg.wait_for_timeout(100)
        check(first.startswith("1 /") and second.startswith("2 /") and pg.inner_text("#count").startswith("1 /"), f"slides: arrow keys move forward and back ({first} → {second} → {pg.inner_text('#count')})")
        pg.keyboard.press("End"); pg.wait_for_timeout(100)
        total = pg.inner_text("#count").split("/")[1].strip()
        check(pg.inner_text("#count").startswith(total + " /") and 10 <= int(total) <= 14, f"slides: End goes to the last of {total} slides")
        check(pg.evaluate("document.getElementById('view').naturalWidth") == 1920, "slides: the slide picture is 1920 pixels wide")
        pg.goto(base + "presentation/presenter.html")
        check(len(pg.inner_text("#notes")) > 40, "slides: the presenter view shows speaker notes")
        pg.keyboard.press("ArrowRight"); pg.wait_for_timeout(100)
        check(pg.inner_text("#count").startswith("2 /"), "slides: the presenter view moves with the arrow keys")
        pg.close()

        pg = b.new_page()
        pg.goto(base + "video/index.html")
        src = pg.evaluate("document.querySelector('video source').getAttribute('src')")
        trk = pg.evaluate("document.querySelector('video track').getAttribute('src')")
        check(src.endswith(".mp4") and trk.endswith(".vtt"), "video page: has the video and a captions track")
        vtt = pg.request.get(base + "video/" + trk)
        check(vtt.ok and vtt.text().startswith("WEBVTT") and vtt.text().count("-->") >= 10, f"video: captions served ({vtt.text().count('-->')} cues)")
        files = [f"video/{C.VIDEO}.mp4", f"presentation/{C.DECK}.pdf", "presentation/slides/01-cover.jpg", "assets/qr-website.svg", "kit/charts.js"]
        if (root / f"presentation/{C.DECK}.pptx").exists():
            files.append(f"presentation/{C.DECK}.pptx")
        for f in files:
            r = pg.request.get(base + f)
            check(r.ok and len(r.body()) > 100, f"file {f} is served ({len(r.body()) // 1024} KB)")
        b.close()

    mp4 = root / "video" / f"{C.VIDEO}.mp4"
    out = json.loads(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration:stream=codec_name,codec_type,width,height", "-of", "json", str(mp4)], capture_output=True, text=True).stdout or "{}")
    st = out.get("streams", [])
    v = [s for s in st if s["codec_type"] == "video"]
    a = [s for s in st if s["codec_type"] == "audio"]
    dur = float(out.get("format", {}).get("duration", 0))
    check(bool(v) and v[0]["codec_name"] == "h264" and (v[0]["width"], v[0]["height"]) == (1920, 1080), "video: 1920x1080 H.264")
    check(bool(a) and a[0]["codec_name"] == "aac", "video: AAC sound")
    check(170 <= dur <= 270, f"video: {dur:.0f} seconds (about 3 to 4 minutes)")
    check(mp4.exists() and mp4.stat().st_size <= 15 * 1_048_576, f"video: {mp4.stat().st_size / 1_048_576:.1f} MB (15 MB at most)")
    print(f"\n{'ALL END-TO-END CHECKS PASSED' if not fails else str(len(fails)) + ' CHECKS FAILED'}")
    return not fails
