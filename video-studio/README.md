# Video Studio

A conversation-driven video editing studio. Drop raw footage and raw audio in a
project folder, describe what you want, and it syncs, transcribes, cuts,
removes filler, drops in B-roll and graphics, captions, grades and renders.

Built for the **Mr Taco Shop** food reviews ([mrtacoshop.com](https://www.mrtacoshop.com)).

## The idea

The model does not watch the video. It **reads** it.

Describing 30,000 frames to a language model is tens of millions of tokens of
noise. The same footage as a word-level transcript is about 12 KB — and the
transcript is where the editorial decisions actually live: what was said, how
cleanly, with what hesitation, and where the pauses fall. Pictures get looked
at only at decision points, through a rendered filmstrip-plus-waveform view of
one specific range.

Audio is primary. Visuals follow.

## Quick start

```bash
# One-time
uv venv .venv && uv pip install --python .venv/bin/python -e .
cp .env.example .env      # add your ELEVENLABS_API_KEY
apt-get install -y ffmpeg # or brew install ffmpeg

# Per episode
mkdir -p projects/<episode>/footage/{a_roll,b_roll,audio}
# ...drop files in, then just say what you want.
```

Then talk to it: *"cut these into a five-minute breakfast burrito review."*

## Pipeline

```
sync ──> transcribe ──> read ──> propose cuts ──> confirm ──> EDL ──> render ──> self-review
                                                                                     │
                                                                    issue? fix and re-render (max 3)
```

| Stage | Tool | What it does |
|---|---|---|
| Inventory | `ingest.py` | Classifies footage and flags VFR, HDR, rotation and silent audio before they cost you a render |
| Sync | `sync.py` | Aligns separate audio recorders and multiple cameras to one timeline, sub-millisecond, including clock-drift correction |
| Transcribe | `transcribe.py` | Word-level verbatim ASR via ElevenLabs Scribe, or local whisper offline |
| Read | `pack_transcripts.py` | Words into phrase-level takes — the main reading view |
| Plan | `autocut.py` | Proposes filler, stutter and dead-air cuts for review |
| Inspect | `timeline_view.py` | Filmstrip + waveform + word labels for one range |
| Graphics | `graphics.py` | Alpha-channel motion graphics, offline, no browser |
| Render | `render.py` | EDL to finished file: extract, grade, concat, B-roll, overlays, captions, loudness |

## What it handles

**Dual-system sound.** Camera plus a lav or field recorder with no timecode.
Correlates the loudness envelopes of the two microphones, refines against the
raw waveforms, and lands the offset near 0.2 ms — far tighter than the ~41 ms
of a single frame. On synthetic tests with a known offset it recovers it
exactly.

**Clock drift.** Two recorders rarely agree on how long a second is. A 250 ppm
mismatch is 900 ms of walk-off per hour: fine at the top of a take, visibly out
by the end. Drift is measured across five probes and corrected by resampling,
not by a static offset.

**Multicam.** N sources on one master timeline with the common overlap window
computed, plus a PNG of the layout for visual confirmation.

**No usable audio.** Flash sync aligns on a sharp brightness change instead —
a clap in frame or a light flicked on at the top of the take.

**Filler removal.** Verbatim transcripts keep every "um" as a timed word, so
they can be cut precisely. The tool proposes; the editor decides.

**B-roll.** Cutaways with the narration running underneath, full-frame or
picture-in-picture, with the shot's natural sound mixed in under the voice at a
chosen duck depth.

**Motion graphics.** Lower thirds, title cards, stamps, price chips and
chapter breaks rendered locally as alpha video. Nothing to install, no network.

**Delivery.** Loudness normalized to −14 LUFS to match what YouTube, Instagram
and TikTok normalize to, and HDR sources tone-mapped to Rec.709 — without that,
iPhone footage looks blown out after upload even though it looked fine locally.

## Layout

```
video-studio/
├── .claude/skills/
│   ├── video-editing/      the master editing skill + all helpers
│   ├── motion-graphics/    overlay authoring
│   ├── food-review/        the Mr Taco Shop show format
│   └── manim-video/        diagrammatic animation
└── projects/<episode>/
    ├── footage/            sources, never modified
    │   ├── a_roll/  b_roll/  audio/
    └── edit/               everything generated
```

Footage and renders are gitignored. The EDL, transcripts and project notes are
committed — those *are* the edit, and they are small.

## Credits

Built on ideas from three open-source projects:

- [browser-use/video-use](https://github.com/browser-use/video-use) — the
  read-don't-watch architecture, the EDL format, the render pipeline order and
  the production-correctness rules. The core of this studio.
- [heygen-com/hyperframes](https://github.com/heygen-com/hyperframes) — the
  motion-graphics approach and the transcript-driven cut-list model.
- [freemocap/skelly_synchronize](https://github.com/freemocap/skelly_synchronize)
  — N-way multicam lag normalization and brightness-flash sync.
- [hamzanalbantoglu/flexible_audio_video_sync](https://github.com/hamzanalbantoglu/flexible_audio_video_sync)
  and [KnurpsBram/shign](https://github.com/KnurpsBram/shign) — bounded lag
  search and the pad/crop/conform alignment taxonomy.
