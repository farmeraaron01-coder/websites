# Render internals: why the pipeline is shaped this way

Every entry below is a defect that shipped, produced a **valid MP4 that played
fine**, and exited zero. That is the theme: video bugs do not throw. They render
successfully and are wrong, and the only way to find them is to measure the
finished file.

Read this before debugging a render or changing `render.py`.

## Contents

- [Pipeline order](#pipeline-order)
- [The silent failures](#the-silent-failures)
- [Measuring audio timing without fooling yourself](#measuring-audio-timing-without-fooling-yourself)
- [Why intermediates are PCM in Matroska](#why-intermediates-are-pcm-in-matroska)
- [Timeline clocks](#timeline-clocks)

## Pipeline order

```
per-segment extract (conform + grade + 30ms fades)
  -> lossless concat -> base.mkv
    -> composite: B-roll -> overlays -> subtitles LAST
      -> two-pass loudnorm -> final.mp4
```

The order is load-bearing:

- **Extract then concat, rather than one filtergraph.** A single-pass graph
  re-encodes every frame twice.
- **Subtitles last.** Anything composited after the `subtitles` filter is drawn
  over the captions. The render still succeeds; the captions are simply not in
  the file.
- **B-roll below overlays.** A lower-third has to sit *on* a cutaway, not under
  it.
- **Loudness last**, over the finished mix, so one gain decision covers
  everything.

## The silent failures

### Mixed orientation squeezed the whole film

A vertical phone clip among horizontal footage. The concat demuxer takes the
**first** segment's dimensions and squeezes the rest into them. No warning. If
the vertical clip is first, the entire film comes out portrait with every
horizontal shot distorted.

Fix: pick one canvas for the whole EDL up front, and conform every segment to it
(`conform_filter`). Note `is_portrait_rotated` — a clip can be stored sideways
with a rotation flag, so raw width/height lies about its shape.

### Graphics composited unscaled

`overlay` does not rescale. It pins the graphic at 0,0 and lets the overflow
hang off the frame. Graphics authored at 1920×1080 over a 1280×720 draft lost
their right edge, and anything positioned right or low vanished entirely — a
price chip and a lower-third disappeared with no error.

Fix: overlays are scaled to the base frame.

### Alpha silently discarded

ffmpeg's built-in `vp9` decoder drops the alpha side stream in a WebM. The
graphic arrives as an opaque black rectangle. `libvpx-vp9` keeps it.

Fix: `.webm` overlays get `-c:v libvpx-vp9` explicitly, plus `format=yuva420p`
in the chain so the overlay filter cannot negotiate the alpha plane away.

### Zero captions from a naming mismatch

Transcripts are named after the media they were made *from* — usually the synced
copy (`A001_synced.json`) — while the EDL keys the source `A001`. Looking up by
key found nothing, every segment reported "no transcript", and the SRT came out
empty. An empty SRT then **crashes libass**, and because the composite
subprocess piped stderr and never printed it, the crash was anonymous.

Fixes: look up by the source file's stem first; treat a zero-cue SRT as
no-captions; and always surface ffmpeg's stderr on failure.

### Two independent causes of lip-sync drift

Reported as "audio is off, and the beep missed the word." Measured as a linear
walk: +0.02 s at the first cut growing to **+0.58 s** by the last.

**Cause 1 — video frame quantization.** An encoder emits whole frames, so a
segment's nominal duration rounds up to the frame grid while its audio is cut
sample-exact. The concat advances by the longer stream.

**Cause 2 — AAC frame quantization.** Fixing cause 1 left an identical symptom.
AAC is frame-based (1024 samples, 21.3 ms), so the encoder rounds each segment's
audio *up* to a whole frame and the picture falls ~21 ms further behind at every
cut.

**Cause 3, found while fixing 2 — mixed channel layouts.** Mono lav muxes beside
a stereo generated insert. PCM carries no per-packet channel information, so the
concat demuxer applies the **first** segment's layout to all of them; a stereo
segment read as mono decodes at *double length*. `base.mkv` reported 166.509 s in
its container and decoded to 173.708 s of audio — an excess exactly equal to the
two stereo inserts. Every beat after them sat on a corrupted timeline. AAC had
been masking this; moving to PCM exposed it.

Fixes: frame count decided up front with audio padded to match exactly;
intermediates in PCM; `-ac 2` and `-ar 48000` pinned on every segment.

The lesson is that one symptom had three causes and fixing the first two felt
like success both times. `verify` now measures each layer separately —
per-segment A/V lengths, channel layout, base length, and landing positions — so
a partial fix cannot look complete.

### Absolute music gain buried the dialogue

A bed set to −20 dB measured **louder than the voice**. A conservatively recorded
lav sits near −37 dBFS; a mastered music track sits near −13. The correct value
was −40 dB.

Fixes: music is declared as `under_db` and the renderer measures both signals;
levels use *speech-active* RMS (the loud 30 % of windows), because plain RMS over
dialogue is dominated by the gaps between sentences and understates the voice by
roughly the amount that puts a bed on top of it.

### A gradient that rendered as a hard black bar

`Image.getchannel()` returns a **copy**. Writing to its pixel buffer is
discarded unless `putalpha()` writes it back. The intended soft band rendered as
a letterbox.

### Bleeped audio with the word printed in the caption

The tone masked the word while the burned caption spelled it out in full
uppercase at the same instant — defeating both the joke and ad-safety. Caption
cues overlapping a bleep window are now grawlixed from the same declaration that
places the tone.

## Measuring audio timing without fooling yourself

Both of these produced confident, wrong answers.

**Do not input-seek a lossy stream to read a short window.** `-ss` before `-i`
lands on the nearest seek point, not where you asked. Reading a 96 ms censor tone
this way returns silence, and the conclusion "the bleeps are missing" was wrong.
Decode and `atrim` instead.

**Do not correlate against a mix containing music.** A bed at −40 dB is
inaudible but dominates a loudness envelope. Correlations that read 0.85–1.00
against the music-free concat collapsed to ~0.3 against the final, turning a
clean measurement into noise. Measure timing against `base.mkv`.

**Prefer a search over an assumption.** The decisive test for drift was not
"check the offset at the expected position" but "find where this segment's audio
actually is, anywhere in the film." The first assumes the answer; the second
reveals it.

## Why intermediates are PCM in Matroska

- PCM has no frame quantization, so a segment's audio is sample-exactly as long
  as its video. This is the fix for the AAC drift above.
- Video is still stream-copied through the concat, so there is no extra video
  generation.
- AAC is encoded **once**, at the end, over the finished mix — strictly fewer
  lossy generations than encoding every segment.
- Matroska is used because MP4 handles PCM poorly.

Cost: intermediates are larger. Worth it.

## Timeline clocks

There are two, and they differ:

- **Nominal** — cumulative sums of the EDL's range durations. This is the clock
  an author writes in.
- **Real** — those durations quantized to the frame grid. This is the clock the
  rendered file plays on.

Every output-time feature (bleeps, cutaways, overlays, SFX, music swells, caption
offsets) is authored on the nominal clock and translated to the real one by
`remap_output_time`. Skipping that translation is a 300 ms error over twenty cuts
— enough for a censor tone to beep politely just *before* the word.

Time-gated audio filters have a third trap: the concat demuxer leaves per-segment
gaps in the base audio's **timestamps**, and a `volume` gate fires on the PTS
axis. A gate on gapped base audio and a gate on a continuously generated source
therefore disagree by the accumulated gap. Both legs pass through
`asetpts=N/SR/TB` before any gate, so gates fire on the content axis — the same
axis the final continuous encode presents.
