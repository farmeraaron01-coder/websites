---
name: video-studio
description: Edit raw footage into a finished, delivery-ready video by conversation — sync dual-system/lav audio and multiple cameras, transcribe, cut on the transcript, strip filler words and dead air, add B-roll cutaways, motion graphics, censor bleeps, burned captions, a music bed, colour grading and loudness. Use this whenever the user wants to cut, assemble, sync, trim, caption, grade, bleep, score or finish video from raw files, or mentions footage, takes, a rough cut, an edit, a lav or field recorder, multicam, B-roll, lower thirds, or a YouTube upload — even if they never say the word "edit". Also use it to diagnose a render that came out wrong (squeezed picture, missing graphics, out-of-sync audio, absent captions).
---

# Video studio

You do not watch the video. You **read** it.

Thirty thousand frames described to a model is millions of tokens of noise. The
same footage as a word-level transcript is about 12 KB — and the transcript is
where the editorial decisions actually live: what was said, how cleanly, with
what hesitation, where the pauses fall. Look at pictures only at decision
points, through `timeline_view`, which renders a filmstrip, a waveform and word
labels for one specific range.

Audio is primary. Visuals follow.

## Running the helpers

`cd` into the project directory, then call the launcher by absolute path:

```bash
cd /path/to/project
/path/to/skill/studio ingest footage
/path/to/skill/studio sync --scan footage --mux
/path/to/skill/studio --list        # every helper
```

The launcher finds the helpers; your working directory stays on the project, so
`edit/...` and relative EDL paths resolve. **Getting this backwards is the most
common way to waste a run** — the command appears to succeed, a probe silently
fails to find the source, a fallback kicks in, and you get a valid-but-wrong
file with no error. If a render looks inexplicably wrong, check cwd first.

## The rule that matters most

**Every bug this pipeline has shipped produced a valid MP4 that played fine.**
Squeezed geometry, graphics cropped off-frame, captions silently absent, a
censor tone half a second off its word, audio drifting a half-second out of sync
by the final beat. Every one exited zero.

So: never report a render as done on the strength of an exit code. Run
`studio verify` and look at frames. `references/render-internals.md` documents
each failure, why it is invisible, and the two measurement traps that produced
false "all clear" results — read it before debugging a render or changing
`render.py`.

## Layout

```
<project>/
├── footage/              sources, never modified
├── build_edl.py          the beat list — the edit lives here, not in edl.json
└── edit/
    ├── project.md        session memory; append every session
    ├── synced/           video + good audio, muxed
    ├── transcripts/*.json
    ├── takes_packed.md   phrase-level transcripts: your main reading view
    ├── edl.json          GENERATED — never hand-edit
    ├── clips_graded/     per-segment extracts (PCM in MKV)
    ├── animations/       alpha-channel graphics
    ├── verify/           inspection PNGs
    └── final.mp4
```

## Process

### 1. Inventory

```bash
studio ingest footage
```

Classifies A-roll / B-roll / separate audio and flags variable frame rate, HDR,
rotation metadata and silent tracks. Read the "needs a decision" block: mixed
frame rates and orientations are choices, far cheaper to make now than after a
cut exists.

### 2. Sync — before anything else

```bash
studio sync --scan footage --mux              # camera + recorder pairs
studio sync --multicam footage --plot         # N sources, one timeline
studio sync --scan footage --mux --use-filename-times
```

Quality above ~10 is a clean lock; below 6 the tool refuses to mux.

**Confirm every lock a second way.** Correlation can be confident and wrong. On
one shoot a clip locked 740 seconds off at quality 6.9 and only a cross-check
caught it. Independent checks that cost almost nothing:

- **Filename timestamps.** DJI cameras and mics stamp wall-clock into the name;
  `--use-filename-times` both constrains the search and reports disagreement.
  Phone `creation_time` is *not* usable — it is rewritten on copy, so it reports
  the transfer, not the take.
- **File numbering.** `IMG_1843` cannot precede `IMG_1839`. An ordering that
  contradicts the numbering is a false lock.
- **Direct agreement.** Pearson r of the two loudness envelopes at the claimed
  offset. Above ~0.6 the two mics genuinely heard the same room; ~0.2 means they
  did not, and that source should keep its own audio rather than have a bad lock
  forced onto it.

Clock drift above 50 ppm needs resampling, not a static offset — 250 ppm is
900 ms of walk-off per hour, fine at the top of a take and visibly out by the end.
`--mux` handles it.

If a source has no usable audio, `--multicam --method flash` aligns on a sharp
brightness change instead.

**From here on work from `edit/synced/`, not the originals.**

### 3. Transcribe

```bash
studio transcribe --batch edit/synced --prompt-file vocab.txt
```

ElevenLabs Scribe when `ELEVENLABS_API_KEY` is set, else local whisper. Prefer
Scribe: it diarizes, tags laughter, and is markedly more accurate on proper
nouns. Whisper mangled "hot sauce" into "hot sos" and lost an entire verdict
line on real footage. Put dish names and place names in a vocab file so they
reach the burned captions spelled correctly.

Transcripts are cached and Scribe costs money per minute — never delete one
casually.

### 4. Read

```bash
studio pack_transcripts --edit-dir edit
```

Read `takes_packed.md` **in full** before choosing anything. This is the film.
Alternate takes of the same line are normal and often recorded far apart, so a
partial read will miss the good one.

### 5. Propose the mechanical cuts

```bash
studio autocut --edit-dir edit --source <name>
```

Finds hesitations, stutters and dead air; writes `cut_proposal.md` and a draft
EDL. It is a draft — it knows nothing about which take is better or where a
story sags. Check anything flagged as a discourse marker; "like", "so" and
"actually" are frequently real speech, and cutting them all makes delivery
sound clipped.

### 6. Converse, then propose a structure

Ask what the piece is for, how long, and the one thing a viewer must come away
with. Then propose a beat structure with timecodes and a reason per choice.

**Wait for confirmation before rendering.** Rendering is cheap; rendering the
wrong film is not.

### 7. Generate the EDL from a beat list

Write a small `build_edl.py` in the project that holds the beats and emits
`edl.json`. Never hand-write cumulative offsets — that is how a caption ends up
three seconds late with no clue why. Two properties make later edits safe:

- **Declare bleeps in SOURCE time.** The script converts to output time, so
  re-ordering a beat can never orphan a censor tone.
- **Address cutaways and graphics by beat NAME, not index.** Indices shift on
  every insertion; a name fails loudly on a typo instead of quietly decorating
  the wrong shot.

Schema is documented at the top of `helpers/render.py`.

### 8. Render, then verify, then look

```bash
studio render edit/edl.json -o edit/draft.mp4 --draft      # fast, 720p
studio verify --edit-dir edit --final edit/draft.mp4
studio render edit/edl.json -o edit/final.mp4 --build-subtitles
studio verify --edit-dir edit
```

`verify` measures geometry, per-segment A/V lengths, channel layout, timeline
drift, bleep placement, SFX, captions, music level and delivery loudness. Then
still extract frames at every cut boundary, graphic and bleep and *look* at
them — `verify` cannot see a graphic that is ugly, only one that is absent.

`--reuse-clips` skips re-extraction when only compositing changed (captions,
bleeps, overlays, music). It is unsafe when ranges change.

Cap fix-and-re-render at three passes, then describe what is still wrong.

### 9. Thumbnail

```bash
studio thumbnail --layout face --face edit/thumb/clean.png \
    --headline '$15 BURRITO' --sub '4 Tapatios' --zoom 1.45 -o edit/thumb/A.jpg
```

Three things decide whether a thumbnail works, and only the last is obvious:

- **Pull frames from a caption-free source** (`base.mkv`), or stray sentence
  fragments from the burned captions end up in the poster.
- **Judge it at feed size, not full size.** The helper writes a 168 px proof
  next to every render for exactly this. Text that looks bold at 1280 px turns
  to mush at 168, and a small logo becomes a coloured dot — on the first pass
  here a location kicker and a row of bottles both failed this way and had to
  go or grow.
- **Push in.** A 16:9 source frame gets no crop at all when fitted to a 16:9
  thumbnail, so any dead space in the shot is faithfully preserved. `--zoom`
  is what turns a wide shot into a poster.

Two or three words maximum, and keep the bottom-right corner clear — the
platform stamps the duration there.

### 10. Persist

Append to `edit/project.md`: what was cut and why, which takes were rejected,
the sync offsets, what went wrong. Next session starts there.

## Levels

**Specify music relative to dialogue, never absolutely.** Use `under_db`
(12–18 for a bed) and let the renderer measure both signals. An absolute number
cannot survive real material: a conservatively recorded lav sits near
−37 dBFS while a mastered track sits near −13, so a bed set to a
"quiet-sounding" −20 dB lands *above* the voice. The correct value on one shoot
was −40 dB — twenty decibels from the guess.

Levels are computed from *speech-active* RMS, the loud portion only. Plain RMS
over dialogue is dominated by the gaps between sentences and understates the
voice badly, which is exactly how a bed ends up over it.

## Craft

**Cut on meaning, not on the gap.** A pause before a punchline is the punchline.
Get out of a line the moment it lands — holding every shot two seconds too long
is the most common fault in a first assembly.

**Punchlines belong on the face.** A cutaway running over the payoff line throws
the joke away. Check what is being said underneath every cutaway.

**Cut away on a strong word, not into a pause.** Cutting away in silence reads
as a mistake. Come back before the next idea starts.

**Natural sound is half a cutaway.** `"audio": "duck"` mixes a shot's own sound
under the narration. Silent B-roll is a slideshow.

**Vertical in a horizontal edit:** `fit: "blur"` letterboxes over a blurred copy
and never crops the subject — always safe. `fit: "crop"` fills the frame and is
much stronger when the subject survives the crop; `crop_y` biases which band
survives.

**Graphics are authored at delivery size and scaled to the canvas.** Check them
on a draft: a card positioned bottom-right can vanish entirely at a smaller
canvas, and it will not error.

## Reference files

- `references/render-internals.md` — every silent failure this pipeline has
  had, why the pipeline is shaped the way it is, and how to measure audio
  timing without fooling yourself. **Read before debugging a render.**
- `references/motion-graphics.md` — the card types, alpha-channel requirements,
  and motion rules.
- `references/show-format.md` — the Mr Taco Shop food-review format: beats,
  take selection, B-roll grammar, graphics kit, YouTube packaging. Load when
  cutting a food review.
- `references/manim-video/` — diagrammatic and mathematical animation.

## Helpers

```
ingest             inventory and classify raw footage
sync               dual-system, multicam and flash alignment
transcribe         word-level verbatim ASR (Scribe or local whisper)
pack_transcripts   words -> phrase-level takes_packed.md
autocut            filler / stutter / dead-air cut proposal
timeline_view      filmstrip + waveform + word labels for a range
graphics           alpha motion graphics, offline
thumbnail          YouTube thumbnail from frames of the cut
render             EDL -> finished film
verify             measure the finished film against the EDL
grade              colour presets and per-clip auto grade
```

Each prints usage with `--help`, and each file's docstring explains why it works
the way it does. Read the docstring before changing behaviour — most of the
non-obvious lines are load-bearing.
