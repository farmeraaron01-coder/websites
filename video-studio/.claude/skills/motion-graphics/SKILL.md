---
name: motion-graphics
description: Build animated overlays for a video edit — lower thirds, title cards, stamps, price chips, chapter breaks, callouts, kinetic type, charts and diagrams. Renders to alpha video that composites onto the cut. Use when a video needs on-screen graphics, titles, text animation or any designed element that is not footage.
---

# Motion graphics

Graphics are rendered as standalone alpha clips and composited by
`render.py` through the EDL's `overlays` array. They never touch the A-roll,
so a graphic can be rebuilt and re-dropped without re-cutting anything.

## Pick the right tool

**`helpers/graphics.py` — the default.** Local, offline, instant, no
dependencies beyond PIL and ffmpeg. Covers the cards that make up the large
majority of overlays in a talking-head or review video: `lower_third`,
`stamp`, `price`, `title`, `chapter`. Start here. If one of these five shapes
fits, do not reach for anything heavier.

```bash
python helpers/graphics.py lower_third --text "Breakfast Burrito" \
    --sub "chorizo, egg, potato" --duration 3.0 \
    -o edit/animations/slot_1/render.webm

# Or a whole package in one pass, which also prints an EDL fragment
python helpers/graphics.py --spec edit/cards.json --out-dir edit/animations
```

Themes: `campy` (hot yellow on near-black with a chilli-red accent), `clean`,
`salsa`.

**HyperFrames — when the design is the point.** An HTML + CSS + GSAP
composition rendered deterministically through headless Chrome. Reach for it
when you need real layout, web fonts, SVG, gradients, masks, physics, or a
brand system that the five card types cannot express.

```bash
npx --yes hyperframes init my-overlay
# author index.html: a #stage root with data-composition-id / data-width /
# data-height, .clip children carrying data-start / data-duration /
# data-track-index, and one PAUSED GSAP timeline on window.__timelines
npx --yes hyperframes render my-overlay -o render.mov
```

The non-negotiable part of that contract is the **single paused timeline**.
The renderer seeks to each frame rather than playing in real time, so anything
driven by `requestAnimationFrame`, `setTimeout` or wall-clock time renders as a
frozen frame. Everything must be seekable.

It needs Node 22+ and network access on first run. If `npx` cannot reach the
registry, fall back to `graphics.py`.

**Manim — for anything diagrammatic.** Equations, algorithms, charts,
geometric explanation. The vendored `manim-video` skill has the full pipeline
and a large reference library. Overkill for a title card; the right answer for
a genuine explainer.

## Getting a graphic into the cut

Every renderer must produce a **transparent** clip, and the only format that
reliably carries alpha here is **VP9 in WebM** (`yuva420p`). MP4 cannot.

```json
"overlays": [
  {"file": "animations/slot_1/render.webm", "start_in_output": 12.4, "duration": 3.0}
]
```

`render.py` handles the two things that break alpha silently:

- It decodes `.webm` overlays with `libvpx-vp9` explicitly. ffmpeg's built-in
  vp9 decoder discards the alpha side stream and your graphic arrives as a
  black rectangle, with no error.
- It forces `format=yuva420p` into the filter chain so the overlay filter
  cannot negotiate away the alpha plane.

If a graphic shows up as a black box, one of those two is the reason.

`start_in_output` is a position on the **cut** timeline, not on any source
file. Read it off the rendered preview, not off the raw footage.

## Building several at once

Dispatch one sub-agent per graphic, in parallel, never in sequence. Give each
brief:

1. What the graphic says, verbatim.
2. Its exact duration.
3. Canvas size and aspect.
4. The palette and font.
5. The output path — **unique per agent**, so parallel writers cannot collide.
6. The beat it lands on and what the narration is saying underneath.
7. Output format: alpha WebM.
8. "Do not ask questions. If anything is ambiguous, pick the most obvious
   interpretation and proceed."

## Motion craft

**Never linear.** Entrances ease out, exits ease in, anything that should feel
physical overshoots and settles.

```python
def ease_out_cubic(t):  return 1 - (1 - t) ** 3
def ease_out_back(t, s=1.7):
    c3 = s + 1
    return 1 + c3 * (t - 1) ** 3 + s * (t - 1) ** 2
```

**Fast in, faster out.** ~0.35 s entrance, ~0.25 s exit. Slow titles are the
most common reason a cut feels sluggish.

**Move, stop, hold, leave.** An element that keeps drifting while you read it
fights the reading. Idle motion is not life, it is noise.

**Land on the word.** If a graphic pays off a specific spoken word, get that
word's timestamp from the transcript and start the reveal `reveal_duration`
earlier, so the landing frame and the word coincide.

**Respect the caption zone.** Burned captions sit at `MarginV=90`. Nothing
should occupy the lower third unless it replaces the captions there.

**Scarcity.** A stamp that appears once is a punchline. A stamp on every third
line is wallpaper.

## Anti-patterns

- Exporting to MP4 and wondering why the graphic has a black background.
- Animating with `requestAnimationFrame` in a HyperFrames composition.
- Building four graphics sequentially when four sub-agents could do it at once.
- A graphic that says exactly what the narrator is saying at that moment —
  either it adds something or it is clutter.
- Placing a graphic over the caption band.
