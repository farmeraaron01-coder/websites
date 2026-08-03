# Mr Taco Shop — Alberto's, Escondido (breakfast burrito)

Shoot: 2026-08-01, 12:06–12:38. Subject: Alberto's Mexican Food, Escondido Blvd.
Channel: mrtacoshop.com. Tone: campy, fast, affectionate. Target: ~2 min max.

## Sources

14 synced sources. All offsets verified — the DJI camera and DJI mics both
stamp wall-clock time into their filenames, and correlation agreed with that
to within 0.1s on 9 of 10 DJI clips.

| Source | Role | On screen |
|---|---|---|
| DJI_0071 (125s) | arrival | drive-thru sign + menu board, red picnic tables, parking lot from car |
| DJI_0072 (41s) | A-roll | him in the car, in line — the potato rant |
| DJI_0073 (28s) | B-roll | building exterior, crushed wall |
| DJI_0074 (15s) | — | mostly unusable, 1 fragment |
| DJI_0075 (26s) | B-roll | the filthy yellow wall — "never been cleaned" |
| DJI_0076 (49s) | B-roll | the order window, Pollo Asado poster |
| DJI_0077 (425s) | A-roll + food | unveiling, bites, cross-sections; turns to face-cam ~300s+ |
| DJI_0078 (207s) | A-roll + food | tortilla, cross-section, Taco Bell bit |
| DJI_0079 (14s) | — | tangent, unusable |
| DJI_0080 (34s) | A-roll | outro at the picnic table, building behind |
| IMG_1836 (25s) | B-roll | "Cheers!" only |
| IMG_1838 (69s) | A-roll | **selfie angle in front of the Alberto's neon sign** |
| IMG_1839 (14s) | A-roll | vertical; "go to war" line |
| IMG_1843 (9s) | B-roll | no speech |

## Key finding: multicam

DJI_0077 and IMG_1838 are **two angles of the same 69 seconds** (12:27:10–
12:28:19). In DJI_0077 that region is 353.8–422.8s; in IMG_1838 it is
0.0–69.0s. Same continuous lav audio underneath both.

That is the cleanest tool available for the brief: cutting between angles
hides every filler removal, so the delivery tightens without a single visible
jump cut.

## Audio

Lav (DJI Mic) covers everything except IMG_1836 and IMG_1843 — a direct
envelope-correlation test put those at r≈0.2 versus r=0.74/0.79 for the two
clips it does cover, so those two keep their phone audio rather than take a
false lock.

## Transcripts

Local Whisper pass only. It is mishearing the proper nouns badly:
Alberto's appears as "Alberdos", "Alibertos", "Elibertos", "alberos";
"guac" became "wok"; "grading" became "Grating". Re-run with Scribe before
building captions — these would burn in verbatim.

## Rejected

- DJI_0074, DJI_0079 — fragments, no usable line.
- IMG_1836, IMG_1843 — no content beyond "Cheers!" and silence. Possible
  cutaway texture only.
- The "Alibertos and Roberto's, I'm not sure who came first" tangent
  (0077 @179–183) — raises a question the video never answers.

## Session 2 — the cut (2026-08-02)

Delivered `edit/final.mp4`: 1920x1080, 2:34 (153.958s = 3695 frames), -14.4 dB
mean / -0.9 dB peak, 215 caption cues, 3 censor bleeps, 4 graphics, 4 B-roll
cutaways. 17 beats; structure in `build_edl.py` (the EDL is generated, never
hand-edited). Packaging in `youtube.md`.

Decisions:
- Cold open = IMG_1839 torn-burrito shot, crop fit (crop_y 0.30), caption over.
- Verdict beat recovered by Scribe ("four Tapatios... the food is too freaking
  good") — Whisper had garbled it entirely.
- Bleep gag: 1kHz tone over middle 60% of each word, captions grawlixed to
  match (S***). Three instances.
- "gypped" line avoided by using the "trust me, you're gonna get plenty" take.
- Multicam cut DJI_0077 -> IMG_1838 inside THE MESS beat.

Render bugs found by inspection this session (all produced valid MP4s):
1. Mixed-orientation concat squeeze -> global canvas + conform (blur/crop).
2. Overlays composited unscaled -> scaled to base frame.
3. Caption margin was vertical-video tuned -> aspect-aware.
4. SRT built 0 cues (transcript name mismatch) -> stem lookup + skip-if-empty.
5. Timeline drift: frame rounding (+300ms/17 cuts) -> frame-exact segments,
   features remapped to quantized clock.
6. Audio pts gaps from concat -> asetpts=N/SR/TB before all time-gated filters.

Trust nothing but the rendered file. Measure with decode-then-trim, never
input-seek AAC to sub-100ms windows.

## Session 3 — sync repair, effects, 1080p delivery (2026-08-02)

Note flagged from the review: *"the voice sync is off. the beep didnt hapen on
holy shit... its off on lots of the video."* Two further causes behind the same
symptom, on top of the six above — and both earlier fixes had felt like
success:

7. **AAC frame quantization.** Intermediates were AAC-in-MP4; AAC rounds each
   segment up to a whole 1024-sample frame, so picture fell ~21 ms further
   behind at every cut. Intermediates are now PCM in Matroska.
8. **Mixed channel layouts.** Exposed by fixing 7: PCM carries no per-packet
   channel info, so the concat demuxer applied the *first* segment's layout to
   all. `base.mkv` reported 166.509 s and decoded to 173.708 s — the excess was
   exactly the two stereo generated inserts, read as mono at double length.
   Every beat after them sat on a corrupted timeline. `-ac 2 -ar 48000` pinned
   on every segment.

Final measured worst timeline drift: **5 ms** (was 580 ms). All three bleeps
confirmed on their words by content-location search, not by assumption.

Added this session, per notes:
- `SLOWMO_BITE` from IMG_1837 — the bite *and* the burrito interior, which the
  earlier cut was missing (the face did not appear early enough).
- Tapatio score card rebuilt from the real bottle image, four across, centred,
  +1 s. Bottles had overlapped because spacing came from the raw icon width and
  ignored the rotation bbox plus shadow padding; `spacing` 1.85.
- TACO BELL beat: KTLA breaking-news parody PiP (corner), slow pan to the Taco
  Bell from the iPhone footage, fart SFX at +2.70 (measured 3.6x over context).
- Music bed: the editor's own parody track "Pásame la Salsa" from 95 s, 16 dB
  under **speech-active** dialogue. An absolute -20 dB had measured *louder*
  than the voice; `under_db` is the only sane way to specify this.

Delivered `AlbertosBreakfastBurrito_1080p.mp4` — 2:46 (166.5 s), -16.5 dB mean
/ -0.9 dB peak, 226 caption cues (3 masked, 0 unmasked profanity), 9/9 verify.
Handed over in five bit-exact parts; recombined length 116,542,215 bytes,
MD5 E22C1B94F493049213F486C623A422BF, confirmed on the far end.

## Session 4 — thumbnail, logo, packaging correction (2026-08-03)

Two factual corrections from the review, both now baked into the skill so they
cannot recur:

- **The $15.42 is the order total and included an orange soda.** Every
  price-led title and the description had treated it as the burrito's price.
  Rewritten; `youtube.md` now says so explicitly, and the chapter reads
  "The order (burrito plus an orange soda, $15.42)".
- **The score does not belong on the poster.** Titles, thumbnails and the
  chapter name all gave away "4 Tapatios" — which is the one thing a viewer
  stays to the end for. Everything now poses the question instead:
  "HOW MANY TAPATIOS?".

`assets/albertos_logo.png` — the real roofline sign, keyed out of
`footage/IMG_1843.MOV` at t=4.0 s. Sky keys off trivially (`(B-R) > 26 & B >
105`); the roof does not, because it is the same red as the sign and rust
streaks running down from the letters connect the two into one component, so a
connected-component filter cannot separate them. What works: the roof is a
straight edge, and climbing each column upward from the bottom while the pixel
stays opaque finds that edge and nothing else. The points fit a line to a few
px; cut on it. (`scipy.ndimage.binary_closing` needs `border_value=1` here —
the default erodes away the bottom row, which is exactly where the measurement
has to happen.)

Thumbnails: `edit/thumb/A_face.{png,jpg}` (bite at 0:08, 1.45x, logo top left,
two-line yellow hook) and `B_split.{png,jpg}` (torn burrito | bite, red "HOW
MANY" over giant "TAPATIOS?", logo top right on the neon). A is the stronger.
Both verified on the 168 px feed-size proof, which is where thumbnails actually
fail.

`thumbnail.py` gained `--logo/--logo-scale/--logo-pos` (white halo over a soft
shadow, so a keyed cutout survives landing on any frame), `--head-y`, and `|`
as an explicit line break in `--headline` — one word per line reads as a list,
two short words on a line read as a phrase.
