"""Slides for the course story: each slide is a 1000x563 page in the website's own styles, rendered to a
1920x1080 picture with Playwright, then collected into a PDF, a PowerPoint with speaker notes, a full-screen
viewer (arrow keys) and a presenter view with notes and a timer. Prints OVERFLOW for any slide that does not fit."""
from __future__ import annotations

import shutil

from . import viewers

DECK_CSS = """html,body{margin:0;width:1000px;height:563px;overflow:hidden;background:var(--paper,#F3EDE2)}main#app{margin:0!important;padding:0!important;max-width:none!important;width:1000px}
.deck-slide{width:1000px;height:563px;max-width:none!important;margin:0!important;border:0!important;box-sizing:border-box;padding:30px 44px 38px;display:flex;flex-direction:column;justify-content:center;gap:4px;position:relative;overflow:hidden}
.deck-slide .landing-hero{gap:30px}.deck-slide h1{font-size:34px!important;line-height:1.1;margin:0 0 10px}.deck-slide .landing-hero h1{font-size:40px!important}
.deck-slide .hj-sub{font-size:15px;max-width:640px}.deck-slide .lm-head{margin-bottom:10px;align-items:center}.deck-slide .hj-art{max-width:230px}
.deck-slide .landing-problems{margin:6px 0}.deck-slide .lm-grid{margin-top:8px}.deck-slide .lm-grid li{padding:14px 16px}.deck-slide .lm-grid p{font-size:14px}.deck-slide .lm-grid h3{font-size:17px}
.deck-slide .landing-problems li{padding:14px 16px}.deck-slide .landing-problems .lp-pain,.deck-slide .landing-problems .lp-fix{font-size:14px}
.deck-foot{position:absolute;left:44px;right:44px;bottom:12px;display:flex;justify-content:space-between;font:600 11px/1 system-ui,sans-serif;letter-spacing:.12em;text-transform:uppercase;color:var(--muted)}
.deck-slide .chart-card{grid-template-columns:1.55fr 1fr;padding:12px 16px;gap:18px;align-items:center;margin:6px 0 0}.deck-slide .chart-card svg.chart{max-height:300px;width:100%}.deck-slide .chart-card h3{font-size:20px}.deck-slide .chart-card p{font-size:13px}
.deck-slide .lp-energy{font-size:14px;padding:12px 16px}
.deck-slide ol{grid-template-columns:repeat(3,minmax(0,1fr))!important;overflow:visible!important}.deck-slide .dense4 ol{grid-template-columns:repeat(4,minmax(0,1fr))!important}.deck-slide .dense2 ol{grid-template-columns:repeat(2,minmax(0,1fr))!important}
.deck-slide .found3 h3{font-size:20px}.deck-slide .found3 .lp-pain{font-size:14px}.deck-slide .found3 .lp-pain b{color:var(--ink)}
.deck-slide.dense .landing-problems .lp-pain,.deck-slide.dense .landing-problems .lp-fix{font-size:12.5px;line-height:1.38}.deck-slide.dense .landing-problems h3{font-size:16px}
.deck-slide .method-figure .spot-art,.deck-slide .course-fig .spot-art{width:100%;height:auto}.deck-slide .landing-problems .lp-lead::after{content:none!important}
.deck-slide .landing-art{max-width:330px}.deck-slide .method-figure{max-width:900px;margin:0 auto}.deck-slide .course-fig{margin:4px 0;padding:8px 12px}.deck-slide .course-fig figcaption{font-size:13px}
.deck-slide .loop-tall{display:none!important}.deck-slide .loop-wide{display:block!important}.deck-slide .net-figure{padding:6px 10px;margin:0}.deck-slide .net-figure .spot-art{min-width:0;height:300px;width:auto;max-width:100%;margin:0 auto}.deck-slide .grid4 .lm-grid{grid-template-columns:repeat(4,minmax(0,1fr))}
.deck-slide .grid3 .lm-grid{grid-template-columns:repeat(3,minmax(0,1fr))}.deck-slide .grid3 .lm-grid li{padding:12px 14px}.deck-slide .grid3 .lm-grid h3{font-size:16px}.deck-slide .idea-cards li{padding:10px 14px}.deck-slide .idea-cards p{font-size:14px}.deck-slide .say-back{font-size:18px;margin:8px 0;padding:10px 14px}"""


def slide_html(kit, i, total, s):
    C = kit.C
    css = "".join(f'<link rel="stylesheet" href="../../assets/{c}">' for c in ["base.css", "experience.css", "theme-atlas.css", "styles.css", "charts.css", "course.css"])
    js = "".join(f'<script src="../../assets/{j}"></script>' for j in ["course-data.js", "icons.js", "icons-extra.js", "icons-course.js", "art.js", "course-art.js", "charts.js", "course-charts.js", "course-site.js"])
    return f"""<!doctype html><html lang="en"><head><meta charset="utf-8"><title>Slide {i}</title>{css}
<style>{DECK_CSS}</style></head><body><main id="app"><section class="screen active landing deck-slide {s.get('cls', '')}">{s['body']}
<p class="deck-foot"><span>{C.NAME}</span><span>{i} / {total}</span></p></section></main>{js}</body></html>"""


def build_pptx(kit, files, slides):
    from pptx import Presentation
    from pptx.util import Emu
    P = kit.site / "presentation"
    deck = Presentation()
    deck.slide_width, deck.slide_height = Emu(12192000), Emu(6858000)
    deck.core_properties.title = kit.C.NAME
    for name, s in zip(files, slides):
        sl = deck.slides.add_slide(deck.slide_layouts[6])
        pic = sl.shapes.add_picture(str(P / "slides" / f"{name}.jpg"), 0, 0, deck.slide_width, deck.slide_height)
        pic.name = s["alt"][:250]
        pic._element.nvPicPr.cNvPr.set("descr", s["alt"])
        sl.notes_slide.notes_text_frame.text = s["notes"]
    deck.save(P / f"{kit.C.DECK}.pptx")


def build(kit):
    from playwright.sync_api import sync_playwright
    from PIL import Image
    C = kit.C
    slides = C.slides(kit)
    P = kit.site / "presentation"
    src, out = P / "_src", P / "slides"
    src.mkdir(parents=True, exist_ok=True)
    out.mkdir(parents=True, exist_ok=True)
    for old in out.glob("*.jpg"):
        old.unlink()
    files = []
    for i, s in enumerate(slides, 1):
        name = f"{i:02d}-{s['key']}"
        (src / f"{name}.html").write_text(slide_html(kit, i, len(slides), s), encoding="utf-8")
        files.append(name)
    bad = []
    with sync_playwright() as pw:
        b = pw.chromium.launch(args=["--allow-file-access-from-files"])
        pg = b.new_page(viewport={"width": 1000, "height": 563}, device_scale_factor=1.92)
        errs = []
        pg.on("pageerror", lambda e: errs.append(str(e)))
        OVER = """() => { const s = document.querySelector('.deck-slide'); const r = s.getBoundingClientRect();
                const out = [...s.querySelectorAll('h1,h2,h3,p,li,svg,.chart-card,figure')].filter(e => { const b = e.getBoundingClientRect(); return (b.bottom > r.bottom - 26 && !e.closest('.deck-foot')) || b.right > r.right + 1; });
                return s.scrollHeight > s.clientHeight + 1 || s.scrollWidth > s.clientWidth + 1 || out.length > 0 }"""
        for name in files:
            for attempt in range(5):  # a busy machine can crash or stall one page; open the slide again and retry
                try:
                    pg.goto((src / f"{name}.html").as_uri(), timeout=60000)
                    pg.evaluate("document.fonts.ready")
                    pg.wait_for_timeout(250)
                    over = pg.evaluate(OVER)
                    pg.screenshot(path=str(out / f"{name}.png"), timeout=30000)
                    break
                except Exception as ex:
                    print("retry", name, str(ex)[:80], flush=True)
                    try:
                        pg.close()
                    except Exception:
                        pass
                    pg = b.new_page(viewport={"width": 1000, "height": 563}, device_scale_factor=1.92)
                    pg.on("pageerror", lambda e: errs.append(str(e)))
            if over:
                print("OVERFLOW", name)
                bad.append(name)
            Image.open(out / f"{name}.png").convert("RGB").save(out / f"{name}.jpg", quality=86, optimize=True)
            (out / f"{name}.png").unlink()
        b.close()
    if errs:
        print("SCRIPT ERRORS", errs[:3])
    shutil.rmtree(src)  # the slide sources are only needed to draw the pictures
    imgs = [Image.open(out / f"{n}.jpg").convert("RGB") for n in files]
    imgs[0].save(P / f"{C.DECK}.pdf", save_all=True, append_images=imgs[1:], resolution=144)
    build_pptx(kit, files, slides)
    items = [{"src": f"slides/{n}.jpg", "alt": s["alt"], "notes": s["notes"]} for n, s in zip(files, slides)]
    (P / "present.html").write_text(viewers.page(f"Slides · {C.NAME}", "Slide", items, "./", "All slides", True, f"{C.DECK}.pdf", C), encoding="utf-8")
    (P / "presenter.html").write_text(viewers.presenter(items, f"Presenter view · {C.NAME}", C), encoding="utf-8")
    kit.presentation_index(list(zip(files, slides)))
    print("deck:", len(slides), "slides · overflow:", bad or "none")
    return bad
