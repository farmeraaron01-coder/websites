---
name: video-editing
description: Edit raw footage into a finished video by conversation. Sync dual-system audio and multiple cameras, transcribe, cut on the transcript, strip filler words, drop in B-roll cutaways and motion-graphic overlays, burn captions, colour grade and render to a delivery-ready MP4. Use for any request to cut, assemble, sync, trim, caption, grade or finish video from raw files. Production-correctness rules are hard; everything else is artistic freedom.
---

# Video editing

You do not watch the video. You **read** it.

Thirty thousand frames described to a model is 45 million tokens of noise. The
same footage as a word-level transcript is about 12 KB, and the transcript is
where every editorial decision actually lives: what was said, how cleanly, with
what hesitation, and where the pauses fall. Look at pictures only at decision
points, through `timeline_view.py`, which renders a filmstrip, a waveform and
word labels for one specific range.

Audio is primary. Visuals follow.

## The hard rules

These twelve are not preferences. Each one is a bug that is invisible until
someone watches the finished file.

1. **Subtitles are applied LAST**, after every overlay in the filter chain.
   Composite anything after them and the captions are gone from the render with
   no error.
2. **Extract per segment, then concat with `-c copy`.** A single-pass
   filtergraph re-encodes everything twice.
3. **30 ms audio fades at every cut edge.** Without them, joins pop.
4. **Overlays need `setpts=PTS-STARTPTS+T/TB`** so frame 0 lands at the window
   start rather than at time zero.
5. **Caption times are output-timeline times:**
   `output_time = word.start - segment_start + segment_offset`.
6. **Never cut inside a word.** Snap every boundary to a transcript word edge.
7. **Pad every cut edge.** Working window 30–200 ms; ASR timings drift 50–100 ms.
8. **Word-level verbatim ASR only.** Never phrase mode, never a transcript with
   fillers normalized away — that deletes the exact signal you need to cut on.
9. **Cache transcripts per source.** Scribe costs real money per minute.
10. **Build multiple animations in parallel sub-agents**, never sequentially.
11. **Confirm the strategy before executing.** Rendering is the cheap part;
    rendering the wrong film is not.
12. **All session output lives in `<project>/edit/`.** Source files are never
    modified, moved or renamed.

## Layout

```
<project>/
├── footage/            <- source files, never touched
│   ├── a_roll/
│   ├── b_roll/
│   └── audio/          <- separate recorder files
└── edit/
    ├── project.md          <- session memory; append every session
    ├── sync_map.json       <- multicam offsets on the master timeline
    ├── sync_report.json    <- dual-system offsets, drift, confidence
    ├── synced/             <- video + good audio, muxed
    ├── transcripts/<name>.json
    ├── takes_packed.md     <- phrase-level transcripts: your main reading view
    ├── cut_proposal.md     <- autocut's draft, for review
    ├── edl.json            <- THE cut decisions
    ├── clips_graded/       <- per-segment extracts
    ├── broll_clips/        <- normalized cutaways
    ├── animations/slot_<n>/
    ├── master.srt
    ├── verify/             <- timeline PNGs used for self-review
    ├── preview.mp4
    └── final.mp4
```

## Process

Do these in order. Do not skip to rendering.

### 1. Inventory

```bash
python helpers/ingest.py footage
```

This classifies every file as A-roll, B-roll or separate audio and flags the
four properties that quietly ruin a render if nobody catches them now:
variable frame rate, HDR, rotation metadata, and audio that is effectively
silent. Read the "needs a decision" block before going further — mixed frame
rates and mixed orientations are choices, not errors, and they are much
cheaper to make here than after the cut exists.

### 2. Sync — before anything else

Nothing downstream is meaningful if the audio does not line up with the picture.

```bash
# One camera + one recorder
python helpers/sync.py footage/a_roll/A001.MP4 footage/audio/ZOOM001.WAV --mux

# A whole shoot, paired automatically
python helpers/sync.py --scan footage/a_roll --mux

# Several cameras and recorders on one master timeline
python helpers/sync.py --multicam footage --plot
```

Read the quality number. Above ~10 is a clean lock. Below 6 the tool refuses to
mux and you should look at why — usually the files do not actually overlap, or
one is near-silent. Pass `--max-shift 120` when you know roughly how far apart
the devices started; it rules out false peaks from repetitive audio.

If it reports clock drift above 50 ppm, the two recorders disagree about how
long a second is and the fix is resampling, which `--mux` does automatically.
Do not paper over drift with a static offset — it will look fine at the top of
the take and be visibly out by the end.

If a source has no usable audio at all, `--multicam --method flash` aligns on a
sharp brightness change instead. That only works if there was one; a clap in
frame or a light flicked on at the top of the take is enough.

**From here on, work from the synced files in `edit/synced/`, not the originals.**

### 3. Transcribe

```bash
python helpers/transcribe.py --batch edit/synced
```

Scribe is used automatically when `ELEVENLABS_API_KEY` is set, which it should
be. It diarizes speakers and tags audio events like `(laughter)`, both of which
matter for finding the good moments. Without a key it falls back to local
whisper, which is free and offline but slower and cannot separate speakers.

For proper nouns the model will not know — dish names, a restaurant's name —
pass `--prompt-file` with a list of them. Spelling them right in the transcript
means spelling them right in the burned captions.

### 4. Pack and read

```bash
python helpers/pack_transcripts.py --edit-dir edit
```

Read `takes_packed.md` in full. This is the film. Note where the good takes
are, where the story actually starts, which line is the real hook, and which
sections are dead.

### 5. Propose the mechanical cuts

```bash
python helpers/autocut.py --edit-dir edit --source A001_synced
```

This finds the hesitations, stutters and dead air and writes
`cut_proposal.md` plus a draft EDL. **It is a draft.** It knows nothing about
which take is better or where the story sags. Read the report and check
anything flagged as a discourse marker — "like", "so" and "actually" are
frequently real speech, and cutting them all makes delivery sound clipped.

Use `--aggressive` only when the speaker is genuinely hedge-heavy.

### 6. Converse, then propose a structure

Ask what the piece is for, who it is for, how long it should run and what the
one thing a viewer must come away with is. Then propose a beat structure and
the specific takes that fill each beat, with timecodes and a reason per choice.

**Wait for confirmation before executing.** This is rule 11.

For long or multi-angle material, dispatch a sub-agent to select takes. Give it
the packed transcript, the beat structure and this output contract:

```json
[{"source": "A001", "start": 2.42, "end": 6.85, "beat": "HOOK",
  "quote": "...", "reason": "cleanest delivery, stops before the slip at 38.46"}]
```

### 7. Write the EDL

The full schema is documented at the top of `helpers/render.py`. The parts that
matter most:

- `ranges` — the A-roll cut, in order. This is the spine.
- `broll` — cutaways. The narration keeps running underneath, so use these to
  cover a jump cut, show what is being described, or give the eye somewhere to
  go during a long line. `audio: "duck"` mixes the cutaway's natural sound in
  under the voice; for anything where the sound *is* the shot, that is the
  difference between a slideshow and a film.
- `overlays` — rendered motion graphics, composited above B-roll.
- `grade` — `"auto"` analyses each segment and applies a bounded correction.

Choose cut points from the transcript. Silences of 400 ms or more are the
cleanest. 150–400 ms is usable but check it visually. Under 150 ms is
mid-phrase and unsafe.

### 8. Preview, then look at it

```bash
python helpers/render.py edit/edl.json -o edit/draft.mp4 --draft
```

Then actually inspect the result at every cut boundary:

```bash
python helpers/timeline_view.py edit/draft.mp4 <t-1.5> <t+1.5>
```

You are looking for: a visual jump or flash at the seam; a waveform spike that
means a pop got past the fades; a caption hidden behind an overlay (rule 1
broken); an overlay showing the wrong frames (rule 4 broken). Also sample the
first two seconds, the last two seconds and two or three points in the middle,
and `ffprobe` the duration against the EDL's expected total.

Fix and re-render. **Cap this at three passes**, then stop and describe what is
still wrong rather than looping.

### 9. Finish

```bash
python helpers/render.py edit/edl.json -o edit/final.mp4 --build-subtitles
```

Loudness normalization to −14 LUFS runs by default and matches what YouTube,
Instagram and TikTok normalize to. HDR sources (iPhone shoots HLG by default)
are tone-mapped to Rec.709 automatically — without that the upload looks blown
out even though it looked fine locally in QuickTime.

### 10. Persist

Append to `edit/project.md`: what was cut and why, which takes were rejected,
the sync offsets, anything that went wrong. The next session starts by reading
that file.

## Craft notes

**Cutting.** Cut on the meaning, not the gap. A pause before a punchline is
the punchline. Get out of a line the moment it lands — the most common fault
in a first assembly is holding every shot two seconds too long.

**B-roll.** Cut away *on* a strong word, not during a pause; cutting away in
silence reads as a mistake. Come back to the face before the next idea starts.
Three to five seconds is usually right; under one second is a flash frame and
over eight the viewer forgets who is talking.

**Captions.** The default style is two-word uppercase chunks with `MarginV=90`.
That margin is a platform rule, not taste: the bottom quarter of a vertical
frame is covered by app UI. Do not drop it below ~75.

**Grading.** The goal is clean, not graded. `auto` targets a normal-looking
image and clamps itself to small corrections. Reach for a preset only when
there is a reason.

## Anti-patterns

- Rendering before the strategy is confirmed.
- Cutting from unsynced sources because the offset "looked small".
- Running Whisper when a Scribe key is available — it normalizes fillers away.
- Trusting `autocut.py` output without reading the report.
- Overlaying a graphic and then wondering where the captions went.
- Re-transcribing a source that already has a cached transcript.
- Building animations one at a time instead of in parallel sub-agents.

## Helpers

```
ingest.py           inventory and classify raw footage
sync.py             dual-system, multicam and flash alignment
transcribe.py       word-level verbatim ASR (Scribe or local whisper)
pack_transcripts.py words -> phrase-level takes_packed.md
autocut.py          filler / stutter / dead-air cut proposal
timeline_view.py    filmstrip + waveform + word labels for a time range
render.py           EDL -> extract, grade, concat, B-roll, overlays, subs, loudnorm
grade.py            colour presets and per-clip auto grade
```

Every one prints its own usage with `--help`, and each file's docstring
explains why it works the way it does. Read the docstring before changing
behaviour.
