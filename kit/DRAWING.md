# How to draw a new glyph

The boards have two kinds of drawing. Look at `gallery.html`, section "Drawings", before you start, and copy the nearest one.

## 1. Filled glyph (for a sand tile)

Used on doors, index rows and tiles. Examples: `filled/battery`, `filled/scale`, `course/bowl`.

- **Canvas**: `viewBox="0 0 380 190"`. Keep everything inside a 300 × 150 box centred at (190, 95). The tile supplies the sand background; draw none.
- **Fills, no outlines**: build the subject from three to seven solid shapes.
  - ink `#3a2e26` for the main body and for any bar, axis or pin
  - rust `#9a4a22` for the one part to look at (one shape, or one line)
  - peach `#e3b98f` for the second mass
  - taupe `#cdbfa9` for a third, quieter mass
  - paper `#fbf7f0` or sand `#ece4d5` only for a hole or a pip inside a dark shape
- **Lines** only where the subject is a line (a wire, a path, an arrow shaft): 5 to 6 px, in ink, rust or peach, `fill="none"`. Round or butt ends, not both in one glyph. Arrowheads are filled triangles, about 16 × 18.
- **Corners**: rectangles get `rx` 3 to 8. Circles for joints, pins and dots: radius 9 to 14.
- **No** gradients, shadows, opacity, text (one short italic Fraunces mark at most, as in `filled/tag`), people or photographs.
- Write the hex values above exactly. `course.css` maps those values to tokens, which is how the same file works in the dark theme. A different hex will not be themed.

## 2. Line drawing (for a paper card)

The 41 problem drawings. Examples: `line/dna`, `line/batteries`.

- **Canvas**: `viewBox="0 0 240 150"`, subject inside 20 px margins.
- One group: `fill="none" stroke="#2b2622" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"`.
- **One rust fill**: the single part the question is about gets `fill="#9a4a22" stroke="none"`. Small ink dots (`fill="#2b2622" stroke="none"`) are allowed.
- A ground line or a horizon anchors anything that stands.

## 3. Icons

`viewBox="0 0 24 24"`, stroke only, 1.6 to 1.7 px, round caps and joins, `stroke="currentColor"`. They take the colour of the text beside them.

## What makes it read at 96 px and at 320 px

- **One subject, one accent.** If you need a caption to say which part matters, the rust is in the wrong place.
- **At 96 px wide** a 380-wide glyph is drawn at a quarter size. Nothing thinner than 5 units survives (it becomes about 1.25 px). Gaps between shapes: at least 8 units. No detail smaller than 12 units.
- **At 320 px wide** large flat shapes look empty. Break the biggest mass once: a second tone, a row of pips, a notch. Do not add more than that.
- **Silhouette first.** Fill every shape with ink and look. If the subject is still recognisable, the drawing works.
- Squint test in both themes: open `gallery.html`, switch the theme with the button in the top bar, and check the accent is still the first thing you see.

## Show the mechanism, not the topic

A door glyph may stand for a subject (a bowl for optimisation). A drawing beside an idea must show how the idea works, with the lecture's own numbers: use a chart from `charts.js` (`plane` for geometry, `flow` for a loop, `tree`, `grid`, `line`). Draw a bespoke SVG only when no builder fits, in the chart classes (`cx`, `s s-ink`, `f-rust`, …) so it takes the tokens.

## Adding it

1. Save as `glyphs/course/<name>.svg` with `class="kit-glyph kit-glyph-filled"`, `data-glyph="<name>"`, `role="img"` and an `aria-label` that says what is drawn.
2. Add it to `glyphs/course.json`.
3. Run `python3 kit/tools/build_gallery.py` and look at it at tile size, in both themes.

## Composing a scene

A scene is a large drawing of the thing a lecture keeps coming back to: the cart, the bowl, the table with two players. The boards have two kinds, and the kit has both.

- **Taken from the boards**: `scenes.board("chip-layout")`. 104 of them in `scenes/board/`, listed in `scenes/index.json` and shown in the gallery. Use one when the subject fits. Relabel with `labels={7: "new words"}` (each text carries its number in `data-l`).
- **Drawn for a lecture**: the builders in `scenes.py`. Start from the nearest one. Write a new builder only when none fits, from the parts below.

### The sheet

Every drawn scene is one sheet, `viewBox="0 0 1200 600"`, built with `Sheet(uid, title, no=, kind=)`:

- a paper rectangle with a double border and six zone ticks along the top and bottom edge;
- "NOT TO SCALE" top right; a title block bottom right (kind · title · sheet number), drawn last so it sits over the ground;
- give each scene on a page its own `uid`: pattern and marker ids are prefixed with it.

### Layers, back to front

1. **Field**: a faint grid (`s.pat("grid")`) or dots behind everything. It says "this is a drawing, not a photo".
2. **Ground**: `s.ground(y)`, a sand band with the 45° earth hatch and a 2-unit ink line on top. Anything that stands, stands on this line. A cut through the ground (a hill, a bowl) is the same fill under a 2.5-unit curve.
3. **Things**: flat fills with a 2-unit ink outline. Peach for the main body, tan for wood and hats, taupe for the second mass, espresso for machines and wheels, paper for windows and screens. Rounded joins. No gradients, no shadows except the card's.
4. **The one rust thing**: the part the idea is about (the pole, the chosen branch, the stable cell, the flag at the minimum). One per scene, plus the rust path.
5. **The path**: what moves or flows is a dashed rust line, 2 to 2.5 units, `8 6` dashes, with an arrowhead. What is fixed wiring is a solid ink line.
6. **Figures**: `s.person(x, ground_y, scale, arm=(dx, dy))`. Hard hat, peach body, two ink legs. About 78 units tall at scale 1. They give the size of things and point at what matters. Never a face.
7. **Callouts**: `s.callout(x, y, w, "1 · measure", [lines], to=(x, y))`. A paper box, a caps title, one or two lines of body text, and a 1.2-unit leader ending in a 3.5-unit dot on the thing it names.
8. **Number cards**: `s.card(x, y, "label", "25 → 16", "note", rot=-2)`. The boards' tilted cards: paper, a rust top edge, a soft offset shadow. Tilt alternates −2°, +1.5°. Two or three, on the ground band where nothing else is.
9. **Title block**.

### Depth

There is no perspective. Depth is order and overlap only: the field, then the ground, then far things (smaller, lighter fill), then near things. A table is a side view; a grid lying "on" it is drawn above it as a tilted card joined by two dotted lines. Keep one ground line; a second level is a second line (a shelf, a floor), never a vanishing point.

### Leaders

- Straight lines only, from the nearest edge of the box (`side="left" | "right"`, or top and bottom by default).
- A leader ends in a dot on the object, not near it.
- Leaders do not cross each other. If two would cross, swap the boxes.
- Boxes go in the air (top band, y 62 to 150) or on the ground band. They never cover the rust thing.
- Number the boxes in reading order, "1 · measure", "2 · compare". The same numbers and words are returned in `scene.key` and printed under the drawing, so a phone reader has them without panning.

### Text

- Three sizes: caps labels 14 (IBM Plex Sans Condensed 600, letter-spacing 1.2), body 15 to 16 (Source Serif 4), numbers 20 to 28 (Fraunces). Nothing under 14 units: at page width a unit is about a pixel.
- Text on espresso is page cream `#F3EDE2`, never peach: in the dark theme espresso becomes a cream mass and the cream text becomes dark.
- Every number comes from the lecture or is computed by the builder from a rule the lecture states. `landscape` takes real steepest-descent steps; `particle_field` integrates the force you give it; `market` works out the clearing price. Say which with the panel's chip.

### Colours

Write the boards' hex values (`#2B2622 #3A2E26 #5A5047 #9A4A22 #E3B98F #C99A5B #C9B9A3 #ECE4D5 #F3EDE2 #FBF7F0 #D9CDBA #8B2E1F`). `course.css` maps them to the `--art-*` colours, which have a hand-chosen dark set. A hex outside this list is not themed.

### Putting it on a page

`scenes.scene_html(scene, panel=, chip=, caption=)` gives the panel: header and chip, the drawing in a box that scrolls sideways on a phone (the page itself never does), the numbered key, the caption. Scenes span the full width; do not put one in the side column. Under a metaphor scene add `components.meaning_strip([("part of the picture", "what it stands for")])`, as the boards do.

### Checking it

Render it at 1200 wide and look: is the rust thing the first thing you see; does any box sit on a line or on another box; can you read the smallest text. Then switch the theme and look again.
