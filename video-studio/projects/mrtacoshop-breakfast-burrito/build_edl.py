"""Build edl.json for the Alberto's breakfast burrito review.

The beat list below is the edit. Everything else -- output-timeline offsets,
bleep positions, graphic placement -- is derived from it, because hand-typing
cumulative offsets is how you end up with a caption three seconds late and no
idea why.

Bleeps are declared against SOURCE time (where the word actually is in the
original clip) and translated to output time here, so re-ordering a beat can
never orphan a censor tone.
"""

import json
from pathlib import Path

EDIT = Path("edit")
SRC = "synced/{}_synced.mp4"

# Sources that do not live in synced/ (pre-built inserts).
SOURCE_OVERRIDES = {
    "SLOWMO_BITE": "inserts/slowmo_bite.mp4",
}

# (source, start, end, beat, note)
BEATS = [
    ("IMG_1839",                  3.70,   7.35, "COLD OPEN",  "you go to war with one of these"),
    ("SLOWMO_BITE",               0.10,   3.55, "THE BURRITO", "silent slow-mo: raise + interior reveal; title over"),
    ("SLOWMO_BITE",               4.80,   8.55, "THE BITE",    "silent slow-mo: the bite + cheese-strand pull"),
    ("IMG_1837",                  8.10,  15.30, "INTRO",       "FACE: Alberto's is one of the best in San Diego"),
    ("DJI_20260801120655_0071_D", 11.00,  14.75, "ARRIVAL",    "pulling up to Alberto's, this is the OG"),
    ("DJI_20260801120655_0071_D", 22.05,  30.15, "THE ORDER",  "ham, egg, guacamole and cheese"),
    ("DJI_20260801121728_0076_D", 18.60,  21.45, "THE PRICE",  "it is $15.42"),
    ("DJI_20260801120940_0072_D",  3.90,  19.10, "THE RULE",   "no potatoes / pineapple on a pizza"),
    ("IMG_1841",                  42.10,  55.75, "THE PLACE",  "FACE: wiener schnitzel building, A rating thank God"),
    ("DJI_20260801120655_0071_D", 66.65,  73.95, "PARKING 1",  "the parking lot sucks"),
    ("DJI_20260801120655_0071_D", 78.10,  84.35, "PARKING 2",  "nowhere to go, he's screwed"),
    ("IMG_1837",                  16.30,  20.00, "UNVEIL FACE","FACE: here we go, here's the unveiling"),
    ("DJI_20260801122117_0077_D", 19.40,  24.30, "UNVEILING",  "FOOD: all that green is fresh guacamole"),
    ("IMG_1837",                  59.40,  65.00, "FIRST BITE", "FACE: oh snap / holy [bleep] that is good"),
    ("DJI_20260801122117_0077_D", 65.00,  74.95, "THE FOOD",   "FOOD: right amount of cheese, guac is tremendous"),
    ("DJI_20260801122117_0077_D", 339.25, 345.85, "THE MESS",  "pissing all over me / sign of a good one"),
    ("IMG_1838",                  10.50,  16.10, "MESS 2",     "MULTICAM: selfie angle, so much juice"),
    ("IMG_1837",                  277.50, 291.45, "SQUAWK BOX","FACE: can't hear [bleep] out of it"),
    ("DJI_20260801123019_0078_D", 183.00, 196.30, "TACO BELL", "who would go to a freaking Taco Bell"),
    ("DJI_20260801123727_0080_D",  5.30,  24.95, "THE VERDICT","four Tapatios"),
    ("DJI_20260801123727_0080_D", 25.35,  33.45, "OUTRO",      "signing off, Mr Taco Shop"),
]

# (source, word_start, word_end, word) -- declared in SOURCE time
# Declared against whichever angle the beat actually uses. The two 0077 words
# moved to IMG_1837 (its selfie angle, +2.68s into that clip's own clock).
BLEEPS = [
    ("IMG_1837",                   63.820,  64.060, "shit"),
    ("IMG_1837",                  282.220, 282.380, "shit"),
    ("DJI_20260801123019_0078_D", 193.100, 193.320, "shit"),
]

# Beats are addressed BY NAME below. Indices shift every time a beat is
# added; names do not, and a typo fails loudly instead of decorating the
# wrong shot.
def beat_index(name: str) -> int:
    for i, b in enumerate(BEATS):
        if b[3] == name:
            return i
    raise SystemExit(f"no beat named {name!r}")

# Cutaways: (beat_name, file, src_start, offset_into_beat, duration, note)
# A file entry may also be a raw path relative to the edit dir, for sources
# that never needed syncing (muted cutaways).
BROLL = [
    ("TACO BELL", "../footage/IMG_1842.MOV", 3.20, 1.30, 6.60,
     "the slow pan arriving on the Taco Bell next door"),
    ("THE PLACE", "DJI_20260801121645_0075_D", 5.80, 1.60, 3.20, "the filthy yellow wall"),
    ("THE PLACE", "DJI_20260801121154_0073_D", 9.60, 5.20, 3.00, "building exterior, crushed wall"),
    ("THE PLACE", "DJI_20260801120655_0071_D", 24.00, 8.30, 2.20, "drive-thru sign and menu board"),
    ("SQUAWK BOX", "DJI_20260801121728_0076_D", 14.50, 3.00, 3.50, "the order window"),
]

# Graphics: (beat_name, offset_into_beat, name, duration)
GRAPHICS = [
    ("THE BURRITO", 0.40, "title", 2.80),
    ("THE PRICE", 0.30, "price", 2.30),
    ("UNVEIL FACE", 0.60, "dish", 3.20),
    ("TACO BELL", 2.60, "newsalert", 6.60),   # parody PiP over the outbreak line
    ("THE VERDICT", 5.20, "tapatio_score", 4.40),
]

# Music bed: mixed only when the file exists. Swells fill the silent slow-mo
# beats; everywhere else it sits far under the dialogue.
# The editor's own parody track. Starting at 95s: the opening ~90s is a
# build, and a bed should enter already at tempo.
MUSIC_FILE = "music/pasame_la_salsa.mp3"
MUSIC_START = 95.0


def main() -> None:
    ranges, offsets, cursor = [], [], 0.0
    for src, a, b, beat, note in BEATS:
        offsets.append(cursor)
        r = {"source": src, "start": round(a, 3), "end": round(b, 3),
             "beat": beat, "reason": note}
        # The cold open is a vertical top-down shot of the wrecked burrito.
        # Cropping fills the frame with the guts spilling out, which is a far
        # stronger opening image than the same shot letterboxed.
        if beat == "COLD OPEN":
            r["fit"], r["crop_y"] = "crop", 0.30
        ranges.append(r)
        cursor += b - a
    total = cursor

    # Source time -> output time, for every beat that contains the word.
    bleeps = []
    for src, ws, we, word in BLEEPS:
        for i, (bsrc, a, b, *_ ) in enumerate(BEATS):
            if bsrc == src and a <= ws and we <= b:
                bleeps.append({"start_in_output": round(offsets[i] + (ws - a), 3),
                               "duration": round(we - ws, 3),
                               "coverage": 0.6, "note": word})
                break
        else:
            print(f"  WARNING: bleep for {word!r} at {ws:.2f}s in {src} is not "
                  f"inside any kept range -- it will not be censored")

    broll = [{"file": (f if "/" in f else SRC.format(f)), "src_start": ss,
              "start_in_output": round(offsets[beat_index(bn)] + off, 3),
              "duration": dur, "mode": "full", "audio": "mute", "note": note}
             for bn, f, ss, off, dur, note in BROLL]

    overlays = [{"file": f"animations/{name}.webm",
                 "start_in_output": round(offsets[beat_index(bn)] + off, 3),
                 "duration": dur}
                for bn, off, name, dur in GRAPHICS]

    sfx = [{"file": "sfx/fart.wav",
            "start_in_output": round(offsets[beat_index("TACO BELL")] + 2.70, 3),
            "gain_db": -7.0}]

    music = None
    mpath = EDIT / MUSIC_FILE
    if mpath.exists():
        i0, i1 = beat_index("THE BURRITO"), beat_index("THE BITE")
        music = {"file": MUSIC_FILE, "start": MUSIC_START,
                 # Relative to dialogue, never absolute -- render.py measures
                 # both and works out the gain. 16 dB under is present enough
                 # to mask parking-lot ambience without competing with speech.
                 "under_db": 16.0,
                 "fade_in": 1.2, "fade_out": 3.0,
                 "swells": [{"start": round(offsets[i0], 3),
                             "end": round(offsets[i1] + (BEATS[i1][2] - BEATS[i1][1]), 3),
                             "under_db": 6.0}]}
        print(f"music bed: {MUSIC_FILE} (swell over the slow-mo)")
    else:
        print(f"music bed: none ({MUSIC_FILE} not present)")

    edl = {
        "version": 1,
        "sources": {src: SOURCE_OVERRIDES.get(src, SRC.format(src))
                    for src, *_ in BEATS},
        "ranges": ranges,
        "grade": "auto",
        "broll": broll,
        "overlays": overlays,
        "bleeps": bleeps,
        "music": music,
        "sfx": sfx,
        "total_duration_s": round(total, 2),
    }
    (EDIT / "edl.json").write_text(json.dumps(edl, indent=2))

    print(f"{'#':>2}  {'out':>7}  {'dur':>6}  {'beat':<12} note")
    for i, ((src, a, b, beat, note), o) in enumerate(zip(BEATS, offsets)):
        print(f"{i:>2}  {o:7.2f}  {b - a:6.2f}  {beat:<12} {note}")
    print(f"\ntotal {total:.2f}s  ({int(total // 60)}:{total % 60:04.1f})")
    print(f"bleeps {len(bleeps)}, cutaways {len(broll)}, graphics {len(overlays)}")
    for x in bleeps:
        print(f"  bleep '{x['note']}' at {x['start_in_output']:.2f}s")


if __name__ == "__main__":
    main()
