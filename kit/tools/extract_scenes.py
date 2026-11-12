#!/usr/bin/env python3
"""Copy the boards' large explanatory drawings into kit/scenes/board/ as inline-SVG partials, unchanged.

Usage: python3 extract_scenes.py s2s=<project dir> a2a=<dir> lt=<dir> bg=<dir> mm=<dir>

Taken as they are: shapes, colours, stroke widths, text. The only edits: fixed width/height dropped,
class="kit-scene" and data-scene added, ids prefixed with the scene name (so two scenes can share a page),
and every <text> numbered with data-l so `scenes.board(name, labels={n: "new words"})` can relabel it.
Colours stay as the boards' hex values; course.css maps them to tokens for the dark theme.
"""
import json, re, sys, html
from pathlib import Path

OUT = Path(__file__).resolve().parent.parent / "scenes"
# canvas board svg-index name group
TABLE = """
s2s Sc4Chip 2 chip-layout device
s2s Sc1Device 1 finger-parts device
s2s PrSlide03 0 finger-parts-slide device
s2s Ch1CameraChallenge 0 camera-on-cable device
s2s Ch5HearingChallenge 0 hearing-aid device
s2s Ch4ConverterChallenge 0 memory-grid-converters device
s2s Ch3DatacentreA 7 gpu-weights-travel device
s2s RvTplConcept 2 crossbar-tile device
s2s PrSlide07 1 four-grids device
s2s Sc4Chip 3 row-voltage chart
s2s PrSlide12 2 row-follows-input chart
s2s An2Power 1 power-waterfall chart
s2s An3Timing 1 timing-ledger chart
s2s An3Timing 2 two-tracks chart
s2s VcCompare 0 products-scatter chart
s2s VcCompare 1 products-sorted chart
s2s PrSlide02 0 seven-steps steps
s2s PrSlide05 0 two-tracks-slide steps
s2s PcBigPicture 1 seven-steps-paths-back steps
s2s WsHowItWorks 17 seven-steps-row steps
s2s VcBridge 0 six-stages steps
s2s VcLadder 0 evidence-ladder steps
s2s VcTrace 0 trace-six-levels steps
s2s PcRipple 4 ripple-chain steps
s2s Cp0Map 0 case-map map
s2s Cp1Bars 0 case-bars chart
s2s VdFrameChip 0 frame-chip-zoom storyboard
s2s VdStoryboard 1 frame-v02-product-first storyboard
s2s VdStoryboard 2 frame-v03-parts storyboard
s2s VdStoryboard 3 frame-v04-power-bar storyboard
s2s VdStoryboard 4 frame-v05-two-tracks storyboard
s2s VdStoryboard 5 frame-v06-model-drops-in storyboard
s2s VdStoryboard 6 frame-v07-zoom-chip storyboard
s2s VdStoryboard 7 frame-v08-layout-draws storyboard
s2s VdStoryboard 8 frame-v09-blanks-targets storyboard
s2s VdStoryboard 9 frame-v10-twin-money storyboard
s2s VdStoryboard 10 frame-v11-does-not-fit storyboard
s2s VdStoryboard 11 frame-v12-converter-curve storyboard
s2s VdStoryboard 12 frame-v13-status storyboard
a2a As0Map 1 record-trail steps
a2a As0Map 2 what-exists steps
a2a As20Domains 1 breadth-wheel map
a2a As20Domains 2 field-map map
a2a As20Domains 12 cases-squares chart
a2a As20Domains 13 checker-tiles chart
a2a As19Insights 1 summary-built steps
a2a As19Insights 2 dot-strip chart
a2a As31TestPlan 1 blind-test-steps steps
a2a As2Landing 3 nine-steps-drafted steps
a2a As3Example 2 two-lattices device
lt L2BatchOfOneScene 0 workshop-section place
lt L2HandoverDay 0 metro-station-section place
lt Answer1 0 three-goals-ground place
lt FmtBeforeAfter 2 before-fabrication beforeafter
lt FmtBeforeAfter 3 after-fabrication beforeafter
lt FmtBeforeAfter 4 before-cooling beforeafter
lt FmtBeforeAfter 5 after-cooling beforeafter
lt FmtBeforeAfter 6 before-report beforeafter
lt FmtBeforeAfter 7 after-report beforeafter
lt FmtDay2028 1 day-0900 storyboard
lt FmtDay2028 2 day-1100 storyboard
lt FmtDay2028 3 day-1400 storyboard
lt FmtDay2028 4 day-1600 storyboard
lt FmtDay2028 5 day-next storyboard
lt FmtSitePlan 0 site-plan-ten-stops map
lt KeepFloorPlan 0 floor-plan map
lt KeepTimeLapse 0 time-lapse-three-dates place
lt AnlMarginFishbone 0 fishbone chart
lt AnlPowersOfTen 0 powers-of-ten place
lt AnlReuseChord 0 chord chart
lt TechRadar 3 radar map
lt L2FactoryFlow 7 reference-flow-seven-stops steps
lt MetaRChess 0 chess-three-phases metaphor
lt MetaRSnakesLadders 0 snakes-and-ladders metaphor
lt MetaRFlywheel 0 two-sites-flywheel metaphor
lt MetaTLoom 0 loom metaphor
lt MetaTPAndID 0 p-and-id metaphor
lt MetaTSingleLine 0 single-line-diagram metaphor
lt MetaTTunnelBoring 0 tunnel-boring-cutaway metaphor
lt MetaAWhyNowBridge 0 bridge-last-span metaphor
lt MetaARentCrane 0 crane-for-hire metaphor
lt MetaAOutcomesTree 0 tree-roots-branches metaphor
lt MetaPSCurve 0 s-curve-site metaphor
lt MetaPBorehole 0 borehole-log metaphor
lt MetaQForecastCone 0 forecast-cone metaphor
lt MetaQLever 0 lever-and-fulcrum metaphor
lt MetaQLayerCake 0 city-layer-cake metaphor
lt MetaRStepwell 0 stepwell-section metaphor
lt MetaTReservoir 0 reservoir-and-canals metaphor
lt MetaTLoadPath 0 load-path-building metaphor
lt MetaBCentreGauge 0 rail-gauge-trains metaphor
lt MetaAMarginRelay 0 relay-handovers metaphor
lt MetaPSieve 0 sieve-stack metaphor
lt MetaTBaseCamps 0 base-camps-mountain metaphor
lt MetaRDabbawala 0 coded-lid-route metaphor
lt Spine01Picture 0 as-built-over-design metaphor
lt Spine08Picture 0 permit-to-work metaphor
bg BgForces 0 six-forces-around map
bg BgPatterns 0 nine-patterns-signals chart
bg BgKit 16 real-vs-sim-by-task chart
bg Main 4 tasks-by-stage chart
mm Main 32 findings-stacked chart
mm MmDecide 14 decision-timeline steps
mm MmUnderstand 14 slope-chart chart
"""
NAMES = {"s2s": "Sense to Silicon", "a2a": "Atom to Answer", "lt": "L&T AI Centre Home Designs", "bg": "Robot Buyer's Guide", "mm": "Murmur to Market"}

def main(args):
    dirs = dict(a.split("=", 1) for a in args)
    index, cache = [], {}
    for line in TABLE.strip().splitlines():
        key, board, idx, name, group = line.split()
        if key not in dirs: continue
        f = Path(dirs[key]) / f"{board}.dc.html"
        if not f.exists(): print("missing", f.name); continue
        if f not in cache: cache[f] = re.findall(r"<svg.*?</svg>", f.read_text(), flags=re.S)
        svg = cache[f][int(idx)]
        head, rest = svg.split(">", 1)
        lab = re.search(r'aria-label="([^"]*)"', head)
        lab = html.unescape(lab.group(1)) if lab else name.replace("-", " ")
        vb = re.search(r'viewBox="([^"]*)"', head).group(1)
        head = re.sub(r'\s(width|height|class|style|xmlns)="[^"]*"', "", head)
        head = head.replace("<svg", f'<svg class="kit-scene" data-scene="{name}"', 1)
        if "role=" not in head: head += f' role="img" aria-label="{html.escape(lab, quote=True)}"'
        ids = set(re.findall(r'\sid="([^"]+)"', rest))
        for i in sorted(ids, key=len, reverse=True):
            rest = re.sub(rf'(\sid=")({re.escape(i)})(")', rf'\g<1>{name}-\2\3', rest)
            rest = rest.replace(f"url(#{i})", f"url(#{name}-{i})").replace(f'href="#{i}"', f'href="#{name}-{i}"')
        n = [0]; labels = []
        def tag(m):
            n[0] += 1; labels.append(html.unescape(re.sub(r"<[^>]+>", "", m.group(2))).strip())
            return f'<text data-l="{n[0]}"{m.group(1)}>{m.group(2)}</text>'
        rest = re.sub(r"<text([^>]*)>(.*?)</text>", tag, rest, flags=re.S)
        sizes = [float(x) for x in re.findall(r'font-size[=:]"?\s*([\d.]+)', rest)]
        d = OUT / "board"; d.mkdir(parents=True, exist_ok=True)
        (d / f"{name}.svg").write_text(head + ">" + rest + "\n")
        index.append({"name": name, "group": group, "file": f"board/{name}.svg", "viewBox": vb, "label": lab,
                      "source": f"{NAMES[key]} · {board}", "labels": labels, "min_text": min(sizes) if sizes else None})
    (OUT / "index.json").write_text(json.dumps(index, ensure_ascii=False, indent=1) + "\n")
    print(len(index), "scenes", sum((OUT / i["file"]).stat().st_size for i in index) // 1024, "KB")

if __name__ == "__main__":
    main(sys.argv[1:])
