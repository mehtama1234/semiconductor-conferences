# Changes made to the vendored kit in this repo

To go back into the kit (course-concept-library, branch claude/course-kit):

1. `render_lecture.py`, `CHIPS`: added the chip `our drawing` (dashed, same look as `our check`). Used when a drawing's layout is ours because the captions do not record the lecturer's.
2. `render_lecture.py`, `block_html`: block type `{"type": "html", "html": ...}` passes through markup the course generator has already laid out with kit classes (definition lists, ledgers with a "This uses" line, lecture moments that link to several video parts).
3. `render_lecture.py`, `panel_html`: a panel may carry `{"html": ...}` as its body: a step-through or a switch between cases made of several drawings and their notes.
4. `fonts/latinmodern-math-subset.woff2` (+ licence): a 42 KB subset of Latin Modern Math, used as the last font in each stack so that symbols the text faces lack (∂ ∪ ≈ χ in labels, arrows) do not fall back to a system font.

Course-side additions that could move into the kit (they live in `scripts/course_story/board/site.css`, `site.js` and `scripts/course_story/draw.py`):

- `ck-stepper`: a step-through drawing (Back / Next step) and a switch between named cases, built from static SVG frames; without JavaScript every frame shows with its note.
- `ck-nav`: section links in the espresso top bar; one scrolling row on phones.
- `ck-kv`, `ck-defs`, `ck-sym`, `ck-fold`, `ck-grid`: label/value rows, definitions with an "In symbols" line, folded notes, card grids for generator pages.
- `draw.py`: topology scenes in the boards' hand: paper bands with twists and cuts drawn in space, glued squares and polygons, surfaces with handles and Möbius lids, crossings with signs, vector fields round an equilibrium, a disc mapped into itself, networks, rain on a sphere and a torus.

## Changes made in recsys-kdd-research (on top of the topology repo's copy above)

5. `render_lecture.py`, `CHIPS`: added `from the papers` (same look as `from the lecture`), `from the catalog` (same look as `verified`) and `counted` (same look as `worked out`), for a research site whose numbers come from paper reviews and the paper catalog rather than lectures.
