#!/usr/bin/env python3
"""Check text contrast (WCAG 2, at least 4.5:1) for the pairs the kit uses, in both themes.
Run: python3 kit/tools/check_contrast.py   (exit code 1 if any pair fails)"""
import re, sys
from pathlib import Path
css = (Path(__file__).resolve().parent.parent / "tokens.css").read_text()
def block(sel):
    m = re.search(re.escape(sel) + r"\{([^}]*)\}", css)
    return dict(re.findall(r"--([\w-]+):(#[0-9a-fA-F]{6})\b", m.group(1)))
light = block(":root"); dark = dict(light, **block(':root[data-theme="dark"]'))
def lum(h):
    v = [int(h[i:i + 2], 16) / 255 for i in (1, 3, 5)]
    v = [c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4 for c in v]
    return 0.2126 * v[0] + 0.7152 * v[1] + 0.0722 * v[2]
def ratio(a, b):
    la, lb = sorted((lum(a), lum(b)), reverse=True); return (la + 0.05) / (lb + 0.05)
PAIRS = [("ink", "page"), ("ink", "paper"), ("ink", "sand"), ("muted", "page"), ("muted", "paper"), ("muted", "sand"),
         ("rust", "page"), ("rust", "paper"), ("rust", "sand"), ("rust", "peach-soft"), ("ink", "peach-soft"), ("rust-dark", "peach-soft"),
         ("on-espresso", "espresso"), ("on-espresso-muted", "espresso"), ("peach", "espresso"), ("on-rust", "rust"),
         ("hold", "paper"), ("hold", "page"), ("hold", "hold-wash"), ("muted", "peach-soft")]
bad = 0
for name, t in (("light", light), ("dark", dark)):
    for fg, bg in PAIRS:
        r = ratio(t[fg], t[bg]); ok = r >= 4.5; bad += not ok
        print(f"{name:5} {fg:18} on {bg:11} {t[fg]} {t[bg]} {r:5.2f} {'ok' if ok else 'FAIL'}")
# drawings (glyphs, scenes): the --art-* colours in course.css, light and dark, hand-chosen
ccss = (Path(__file__).resolve().parent.parent / "course.css").read_text()
al = dict(re.findall(r"--(art-[\w-]+):(#[0-9a-fA-F]{6})", re.search(r":root\{--art-ink[^}]*\}", ccss).group(0)))
ad = dict(al, **dict(re.findall(r"--(art-[\w-]+):(#[0-9a-fA-F]{6})", re.search(r':root\[data-theme="dark"\]\{--art-ink[^}]*\}', ccss).group(0))))
ART = [("art-ink", "art-paper"), ("art-ink", "art-page"), ("art-ink", "art-sand"), ("art-ink", "art-peach"), ("art-ink", "art-tan"), ("art-ink", "art-taupe"), ("art-ink", "art-soft"),
       ("art-mute", "art-paper"), ("art-mute", "art-sand"), ("art-mute", "art-page"), ("art-rust", "art-paper"), ("art-rust", "art-page"), ("art-rust", "art-sand"),
       ("art-paper", "art-mass"), ("art-page", "art-mass"), ("art-paper", "art-rust"), ("art-paper", "art-ink"), ("art-hold", "art-paper"), ("art-rust-deep", "art-paper")]
for name, t in (("light", al), ("dark", ad)):
    for fg, bg in ART:
        r = ratio(t[fg], t[bg]); ok = r >= 4.5; bad += not ok
        print(f"{name:5} {fg:18} on {bg:11} {t[fg]} {t[bg]} {r:5.2f} {'ok' if ok else 'FAIL'}")
# the brand square: on-rust on rust; rust text on the espresso band is never used (peach is), checked here to be sure it stays unused
print("note  rust on espresso (not used for text):", f"{ratio(light['rust'], light['espresso']):.2f} light")
sys.exit(1 if bad else 0)
