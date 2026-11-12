#!/usr/bin/env python3
"""Builds the course story in the house style. Run from the repository root:

  python3 scripts/course_story/build.py pages          # assets, landing, course map, restyled pages, share and video pages
  python3 scripts/course_story/build.py qr             # QR codes for the share page (needs qrcode)
  python3 scripts/course_story/build.py deck           # slides, PDF, PowerPoint, viewers (needs Playwright)
  python3 scripts/course_story/build.py video <tts>    # narrated video (needs Kokoro models and ffmpeg)
  python3 scripts/course_story/build.py publish        # publish/: only the file types the host serves
  python3 scripts/course_story/build.py e2e            # end-to-end browser test of site/
  python3 scripts/course_story/build.py all <tts>      # everything above, in order

The course's own generator calls build_pages() at the end of its build, so a normal rebuild keeps the style."""
from __future__ import annotations

import json, os, re, sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from course_story import content as C  # noqa: E402
from course_story.kit import Kit  # noqa: E402


def build_pages() -> Kit:
    kit = Kit(C)
    kit.copy_assets()
    if hasattr(C, "prebuild"):
        C.prebuild(kit)
    md = kit.render_markdown() if getattr(C, "MARKDOWN", None) else 0
    n = kit.restyle_all()
    kit.write_data()
    kit.course_map()
    C.landing(kit)
    kit.share_page()
    kit.video_page()
    if (kit.site / "presentation/slides").exists() and kit.n_slides():
        files = sorted(p.stem for p in (kit.site / "presentation/slides").glob("*.jpg"))
        slides = C.slides(kit)
        if len(files) == len(slides):
            kit.presentation_index(list(zip(files, slides)))
    kit.manifest()
    from course_story import boards
    if boards.GLOSSED:
        (kit.root / "analysis/clarity").mkdir(parents=True, exist_ok=True)
        (kit.root / "analysis/clarity/glossed-terms.json").write_text(json.dumps(dict(sorted(boards.GLOSSED.items())), indent=1), encoding="utf-8")
    print(f"course story pages built · {md} Markdown notes rendered · {n} existing pages restyled")
    return kit


def make_qr(kit):
    import qrcode, qrcode.image.svg
    links = {"website": C.SITE_URL, "slides": C.SITE_URL + "presentation/", "video": C.SITE_URL + "video/", "share": C.SITE_URL + "share/"}
    for name, url in links.items():
        img = qrcode.make(url, image_factory=qrcode.image.svg.SvgPathImage, box_size=10, border=2)
        (kit.site / "assets" / f"qr-{name}.svg").write_text(img.to_string(encoding="unicode").replace('fill="#000000"', 'fill="#2B2622"'))
    print("QR codes →", ", ".join(links.values()))


def check_publish(out):
    bad = []
    for f in out.rglob("*.html"):
        for href in re.findall(r'(?:href|src)="([^"#?]+)', f.read_text(encoding="utf-8")):
            if re.match(r"[a-z]+:", href) or href.startswith("//"):
                continue
            t = (f.parent / href)
            if href.endswith("/"):
                t = t / "index.html"
            if not t.exists():
                bad.append(f"{f.relative_to(out)} → {href}")
    return bad


def main():
    what = sys.argv[1] if len(sys.argv) > 1 else "pages"
    tts = sys.argv[2] if len(sys.argv) > 2 else os.environ.get("KOKORO_DIR", "")
    kit = Kit(C)
    if what in ("pages", "all"):
        kit = build_pages()
    if what in ("qr", "all"):
        make_qr(kit)
    if what == "deck":
        kit = build_pages()
    if what in ("deck", "all"):
        from course_story import deck
        deck.build(kit)
        kit = build_pages()
    if what in ("video", "all"):
        from course_story import video
        video.build(kit, tts)
        kit = build_pages()
    if what in ("publish", "all"):
        out, n, size = kit.publish()
        bad = check_publish(out)
        big = [p for p in out.rglob("*") if p.is_file() and p.stat().st_size > 15 * 1_048_576]
        print(f"publish/: {n} files, {size / 1_048_576:.1f} MB · broken links: {len(bad)} · files over 15 MB: {len(big)}")
        for x in bad[:20]:
            print("  BROKEN", x)
        if bad or big:
            sys.exit(1)
    if what in ("e2e", "all"):
        from course_story import e2e
        sys.exit(0 if e2e.run(kit) else 1)


if __name__ == "__main__":
    main()
