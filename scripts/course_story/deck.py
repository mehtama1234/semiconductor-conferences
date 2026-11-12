"""Slides for the course story: each slide is a 1920x1080 page in the board kit's slide frame (kit/components.slide), rendered to a
picture with Playwright, then collected into a PDF, a PowerPoint with speaker notes, a full-screen
viewer (arrow keys) and a presenter view with notes and a timer. Prints OVERFLOW for any slide that does not fit."""
from __future__ import annotations

import shutil

from . import viewers

def slide_html(kit, i, total, s):
    """One slide page: the kit's stylesheets and the boards' slide frame, 1920 x 1080."""
    css = "".join(f'<link rel="stylesheet" href="../../kit/{c}">' for c in ["tokens.css", "boards.css", "course.css", "slides.css", "site.css"])
    return f"""<!doctype html><html lang="en" data-theme="light"><head><meta charset="utf-8"><title>Slide {i}</title>{css}
<style>html,body{{margin:0;width:1920px;height:1080px;overflow:hidden;background:#f3ede2}}.ck-stage{{padding:0!important;margin:0!important;background:none!important}}.ck-stage .slide{{transform:none!important}}</style></head><body data-kit="boards"><div class="deck-slide">{s['body']}</div></body></html>"""


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
        pg = b.new_page(viewport={"width": 1920, "height": 1080}, device_scale_factor=1)
        errs = []
        pg.on("pageerror", lambda e: errs.append(str(e)))
        OVER = """() => { const s = document.querySelector('.slide'); const st = s.querySelector('.stage');
                return s.scrollHeight > s.clientHeight + 1 || s.scrollWidth > s.clientWidth + 1 || (st && st.scrollHeight > st.clientHeight + 2) }"""
        for name in files:
            for attempt in range(5):  # a busy machine can crash or stall one page; open the slide again and retry
                try:
                    pg.goto((src / f"{name}.html").as_uri(), timeout=60000)
                    pg.evaluate("document.fonts.ready")
                    pg.wait_for_timeout(250)
                    over = pg.evaluate(OVER)
                    pg.locator(".slide").screenshot(path=str(out / f"{name}.png"), timeout=30000)
                    break
                except Exception as ex:
                    print("retry", name, str(ex)[:80], flush=True)
                    try:
                        pg.close()
                    except Exception:
                        pass
                    try:
                        pg = b.new_page(viewport={"width": 1920, "height": 1080}, device_scale_factor=1)
                    except Exception:   # the browser itself went down: start a new one
                        b = pw.chromium.launch(args=["--allow-file-access-from-files"])
                        pg = b.new_page(viewport={"width": 1920, "height": 1080}, device_scale_factor=1)
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
