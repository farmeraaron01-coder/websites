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

# (source, start, end, beat, note)
BEATS = [
    ("IMG_1839",                  3.70,   7.35, "COLD OPEN",  "you go to war with one of these"),
    ("DJI_20260801120655_0071_D", 11.00,  14.75, "ARRIVAL",    "pulling up to Alberto's, this is the OG"),
    ("DJI_20260801120655_0071_D", 22.05,  30.15, "THE ORDER",  "ham, egg, guacamole and cheese"),
    ("DJI_20260801121728_0076_D", 18.60,  21.45, "THE PRICE",  "it is $15.42"),
    ("DJI_20260801120940_0072_D",  3.90,  19.10, "THE RULE",   "no potatoes / pineapple on a pizza"),
    ("DJI_20260801123019_0078_D", 54.25,  67.80, "THE PLACE",  "wiener schnitzel building, A rating thank God"),
    ("DJI_20260801120655_0071_D", 66.65,  73.95, "PARKING 1",  "the parking lot sucks"),
    ("DJI_20260801120655_0071_D", 78.10,  84.35, "PARKING 2",  "nowhere to go, he's screwed"),
    ("DJI_20260801122117_0077_D", 13.65,  24.30, "UNVEILING",  "all that green is fresh guacamole"),
    ("DJI_20260801122117_0077_D", 56.80,  62.30, "FIRST BITE", "oh snap / holy [bleep] that is good"),
    ("DJI_20260801122117_0077_D", 65.00,  74.95, "THE FOOD",   "right amount of cheese, guac is tremendous"),
    ("DJI_20260801122117_0077_D", 339.25, 345.85, "THE MESS",  "pissing all over me / sign of a good one"),
    ("IMG_1838",                  10.50,  16.10, "MESS 2",     "MULTICAM: selfie angle, so much juice"),
    ("DJI_20260801122117_0077_D", 274.90, 288.85, "SQUAWK BOX","can't hear [bleep] out of it"),
    ("DJI_20260801123019_0078_D", 183.00, 196.30, "TACO BELL", "who would go to a freaking Taco Bell"),
    ("DJI_20260801123727_0080_D",  5.30,  24.95, "THE VERDICT","four Tapatios"),
    ("DJI_20260801123727_0080_D", 25.35,  33.45, "OUTRO",      "signing off, Mr Taco Shop"),
]

# (source, word_start, word_end, word) -- declared in SOURCE time
BLEEPS = [
    ("DJI_20260801122117_0077_D",  61.140,  61.380, "shit"),
    ("DJI_20260801122117_0077_D", 279.540, 279.700, "shit"),
    ("DJI_20260801123019_0078_D", 193.100, 193.320, "shit"),
]

# Cutaways: (after_beat_index, file, src_start, offset_into_beat, duration, note)
BROLL = [
    (5, "DJI_20260801121645_0075_D", 5.80, 1.60, 3.20, "the filthy yellow wall"),
    (5, "DJI_20260801121154_0073_D", 9.60, 5.20, 3.00, "building exterior, crushed wall"),
    (5, "DJI_20260801120655_0071_D", 24.00, 9.00, 3.00, "drive-thru sign and menu board"),
    (13, "DJI_20260801121728_0076_D", 14.50, 3.00, 3.50, "the order window"),
]

# Graphics: (beat_index, offset_into_beat, name, duration)
GRAPHICS = [
    (0, 3.55, "title", 2.40),
    (3, 0.30, "price", 2.30),
    (8, 1.20, "dish", 3.20),
    (15, 5.60, "verdict", 2.20),
]


def main() -> None:
    ranges, offsets, cursor = [], [], 0.0
    for src, a, b, beat, note in BEATS:
        offsets.append(cursor)
        ranges.append({"source": src, "start": round(a, 3), "end": round(b, 3),
                       "beat": beat, "reason": note})
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

    broll = [{"file": SRC.format(f), "src_start": ss,
              "start_in_output": round(offsets[i] + off, 3), "duration": dur,
              "mode": "full", "audio": "mute", "note": note}
             for i, f, ss, off, dur, note in BROLL]

    overlays = [{"file": f"animations/{name}.webm",
                 "start_in_output": round(offsets[i] + off, 3), "duration": dur}
                for i, off, name, dur in GRAPHICS]

    edl = {
        "version": 1,
        "sources": {src: SRC.format(src) for src, *_ in BEATS},
        "ranges": ranges,
        "grade": "auto",
        "broll": broll,
        "overlays": overlays,
        "bleeps": bleeps,
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
