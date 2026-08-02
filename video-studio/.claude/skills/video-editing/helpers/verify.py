"""Check a rendered film against what the EDL said it should be.

Every bug this pipeline has shipped produced a valid MP4. Squeezed geometry,
graphics cropped off the frame, captions silently absent, a censor tone half a
second off its word -- all of them exited zero and played fine in a player.
None would have been caught by looking at a log.

So the rule is: trust nothing but the rendered file, and measure it.

Each check here exists because it caught a real defect:

  geometry      A vertical source in a horizontal edit made the concat demuxer
                squeeze every later segment into the first one's dimensions.
  av_lengths    AAC rounds each segment's audio up to a 21ms frame, so the
                picture fell ~21ms further behind at every cut. Twenty cuts,
                half a second.
  channels      Mono lav muxes next to a stereo insert. PCM carries no
                per-packet channel info, so the demuxer read the stereo
                segments at double length and corrupted everything after them.
  drift         The end-to-end consequence of the two above: where a segment
                ACTUALLY lands versus where the EDL put it.
  bleeps        A tone can be present, loud, and on the wrong word.
  captions      A transcript-name mismatch built an SRT with zero cues, and an
                empty SRT then crashed libass.
  music         A bed specified at an absolute -20 dB measured LOUDER than a
                quiet lav. Levels are only meaningful relative to dialogue.
  loudness      Delivery target, so platforms do not re-gain the upload.

Two measurement traps worth knowing, both of which produced false results here:

  Do not input-seek a lossy stream to read a sub-100ms window. `-ss` before
  `-i` lands on the nearest seek point, not where you asked, so a 96ms censor
  tone reads as silence. Decode and `atrim` instead -- slower, correct.

  Do not correlate against a mix that has music in it. A bed at -40 dB is
  inaudible but dominates a loudness envelope, and every correlation collapses
  to noise. Measure timing against the music-free concat.

Usage:
    python helpers/verify.py --edit-dir edit
    python helpers/verify.py --edit-dir edit --final edit/final.mp4
    python helpers/verify.py --edit-dir edit --skip drift    # drift is the slow one
    python helpers/verify.py --edit-dir edit --json
"""

from __future__ import annotations

import argparse
import json
import math
import subprocess
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
import render  # noqa: E402
import sync as S  # noqa: E402

OK, WARN, FAIL = "OK", "WARN", "FAIL"


class Report:
    def __init__(self) -> None:
        self.rows: list[dict] = []

    def add(self, check: str, status: str, detail: str) -> None:
        self.rows.append({"check": check, "status": status, "detail": detail})
        mark = {OK: "  ok  ", WARN: " warn ", FAIL: " FAIL "}[status]
        print(f"[{mark}] {check:<12} {detail}")

    @property
    def failed(self) -> bool:
        return any(r["status"] == FAIL for r in self.rows)


# -------- Probing ------------------------------------------------------------


def probe(path: Path, stream: str, fields: str) -> dict:
    out = subprocess.run(
        ["ffprobe", "-v", "error", "-select_streams", stream,
         "-show_entries", fields, "-of", "json", str(path)],
        capture_output=True, text=True).stdout
    try:
        streams = json.loads(out).get("streams") or [{}]
        return streams[0]
    except (json.JSONDecodeError, IndexError):
        return {}


def decoded_audio_seconds(path: Path, sr: int = 48000) -> float:
    raw = subprocess.run(
        ["ffmpeg", "-v", "error", "-i", str(path), "-vn", "-ac", "1",
         "-ar", str(sr), "-f", "f32le", "-"], capture_output=True).stdout
    return len(raw) // 4 / sr


def counted_frames(path: Path) -> int:
    out = subprocess.run(
        ["ffprobe", "-v", "error", "-select_streams", "v:0", "-count_frames",
         "-show_entries", "stream=nb_read_frames", "-of", "default=nw=1:nk=1",
         str(path)], capture_output=True, text=True).stdout.strip()
    return int(out) if out.isdigit() else 0


def band_peak(path: Path, t0: float, t1: float, freq: float | None = None,
              lowpass: float | None = None) -> float:
    """Peak level in a window, decoding rather than seeking.

    Input-seeking a lossy stream to a short window is unreliable; `atrim` on a
    decoded stream lands exactly where asked.
    """
    af = f"atrim=start={max(0.0, t0):.4f}:end={t1:.4f}"
    if freq:
        af += f",bandpass=f={freq}:width_type=h:w=30"
    elif lowpass:
        af += f",lowpass=f={lowpass}"
    raw = subprocess.run(
        ["ffmpeg", "-v", "error", "-i", str(path), "-af", af, "-vn", "-ac", "1",
         "-ar", "48000", "-f", "f32le", "-"], capture_output=True).stdout
    x = np.frombuffer(raw, dtype=np.float32)
    return float(np.abs(x).max()) if len(x) else 0.0


# -------- Checks -------------------------------------------------------------


def check_geometry(rep: Report, clips: list[Path], final: Path | None) -> None:
    dims = {}
    for c in clips:
        st = probe(c, "v:0", "stream=width,height")
        dims.setdefault((st.get("width"), st.get("height")), []).append(c.name)
    if len(dims) > 1:
        listing = "; ".join(f"{w}x{h}: {len(n)} clip(s)" for (w, h), n in dims.items())
        rep.add("geometry", FAIL,
                f"segments disagree on dimensions ({listing}). The concat demuxer "
                f"will force the first one's geometry onto the rest and squeeze them.")
    else:
        (w, h), = dims.keys()
        msg = f"all {len(clips)} segments {w}x{h}"
        if final and final.exists():
            fst = probe(final, "v:0", "stream=width,height")
            msg += f"; final {fst.get('width')}x{fst.get('height')}"
        rep.add("geometry", OK, msg)


def check_channels(rep: Report, clips: list[Path]) -> None:
    layouts = {}
    for c in clips:
        st = probe(c, "a:0", "stream=channels,sample_rate")
        layouts.setdefault((st.get("channels"), st.get("sample_rate")), []).append(c.name)
    if len(layouts) > 1:
        listing = "; ".join(f"{ch}ch@{sr}: {len(n)}" for (ch, sr), n in layouts.items())
        rep.add("channels", FAIL,
                f"segments disagree on audio layout ({listing}). PCM carries no "
                f"per-packet channel info, so the demuxer applies the first "
                f"segment's layout to all of them and mis-reads the others' length.")
    else:
        (ch, sr), = layouts.keys()
        rep.add("channels", OK, f"all segments {ch}ch @ {sr} Hz")


def check_av_lengths(rep: Report, edl: dict, clips: list[Path],
                     durs: list[float]) -> None:
    worst = 0.0
    worst_name = ""
    for c, want in zip(clips, durs):
        v = counted_frames(c) / render.OUT_FPS
        a = decoded_audio_seconds(c)
        if abs(a - v) > worst:
            worst, worst_name = abs(a - v), c.name
    status = OK if worst <= 0.002 else FAIL
    rep.add("av_lengths", status,
            f"worst audio-vs-video length difference {worst * 1000:.1f} ms"
            + (f" ({worst_name})" if worst > 0.002 else "")
            + ("" if status == OK else " -- this accumulates into lip-sync drift"))


def check_base(rep: Report, base: Path, durs: list[float]) -> None:
    want = sum(durs)
    got = decoded_audio_seconds(base)
    container = probe(base, "v:0", "stream=duration").get("duration")
    status = OK if abs(got - want) <= 0.05 else FAIL
    rep.add("base_length", status,
            f"decoded audio {got:.3f}s vs expected {want:.3f}s"
            + ("" if status == OK else
               f" -- a mismatch here means the concat mis-read a segment "
               f"(container says {container})"))


def check_drift(rep: Report, edl: dict, base: Path, clips: list[Path],
                real: list[float]) -> None:
    """Where each segment actually lands inside the concat.

    Measured against base (no music), because a music bed destroys envelope
    correlation even when it is inaudible.
    """
    env = S.envelope(S.decode_mono(base))
    worst, worst_beat = 0.0, ""
    for i, (r, c) in enumerate(zip(edl["ranges"], clips)):
        seg = S.envelope(S.decode_mono(c))
        if len(seg) < 40 or seg.std() < 1e-6:
            continue                      # silent insert: nothing to correlate
        lo = max(0, int((real[i] - 2) * 100))
        hi = min(len(env) - len(seg), int((real[i] + 2) * 100))
        best = (-9.0, 0)
        for st in range(lo, hi + 1):
            w = env[st:st + len(seg)]
            if len(w) < len(seg) or w.std() < 1e-6:
                continue
            cv = float(np.corrcoef(seg, w)[0, 1])
            if cv > best[0]:
                best = (cv, st)
        err = abs(best[1] / 100.0 - real[i])
        if err > worst:
            worst, worst_beat = err, r.get("beat", f"range {i}")
    status = OK if worst <= 0.030 else FAIL
    rep.add("drift", status,
            f"worst segment landing error {worst * 1000:.0f} ms"
            + (f" (at {worst_beat})" if worst > 0.030 else ""))


def check_bleeps(rep: Report, edl: dict, final: Path,
                 nom: list[float], real: list[float]) -> None:
    bleeps = edl.get("bleeps") or []
    if not bleeps:
        rep.add("bleeps", OK, "none declared")
        return
    bad = []
    for b in bleeps:
        t = render.remap_output_time(float(b["start_in_output"]), nom, real)
        d = float(b["duration"])
        inside = band_peak(final, t + d * 0.2, t + d * 0.8, freq=render.BLEEP_HZ)
        before = band_peak(final, t - 1.2, t - 0.4, freq=render.BLEEP_HZ)
        after = band_peak(final, t + d + 0.4, t + d + 1.2, freq=render.BLEEP_HZ)
        if not (inside > 0.15 and inside > 6 * max(before, after, 1e-6)):
            bad.append(f"{b.get('note', '?')}@{t:.2f}s (in={inside:.2f} "
                       f"ctx={max(before, after):.2f})")
    if bad:
        rep.add("bleeps", FAIL, f"{len(bad)}/{len(bleeps)} not on target: "
                                + "; ".join(bad))
    else:
        rep.add("bleeps", OK, f"all {len(bleeps)} tones inside their windows "
                              f"with clean context either side")


def check_sfx(rep: Report, edl: dict, final: Path,
              nom: list[float], real: list[float]) -> None:
    sfx = edl.get("sfx") or []
    if not sfx:
        rep.add("sfx", OK, "none declared")
        return
    weak = []
    for x in sfx:
        t = render.remap_output_time(float(x["start_in_output"]), nom, real)
        during = band_peak(final, t, t + 0.9, lowpass=300)
        before = band_peak(final, t - 1.2, t - 0.3, lowpass=300)
        if during <= 2.0 * max(before, 1e-6):
            weak.append(f"{Path(x['file']).stem}@{t:.2f}s")
    if weak:
        rep.add("sfx", WARN, f"not clearly audible over context: {', '.join(weak)}")
    else:
        rep.add("sfx", OK, f"all {len(sfx)} present above context")


def check_captions(rep: Report, edit_dir: Path, edl: dict) -> None:
    srt = edit_dir / "master.srt"
    if not srt.exists():
        rep.add("captions", WARN, "no master.srt (rendered without captions?)")
        return
    text = srt.read_text()
    cues = text.count("-->")
    if cues == 0:
        rep.add("captions", FAIL,
                "0 cues -- transcripts were not found for any source. Transcript "
                "files are named after the media they were made from (usually the "
                "synced copy), not after the EDL's source key.")
        return
    leaked = []
    for b in edl.get("bleeps") or []:
        word = (b.get("note") or "").strip().upper()
        if word and word in text.upper():
            leaked.append(word)
    if leaked:
        rep.add("captions", WARN,
                f"{cues} cues, but bleeped word(s) still printed in full: "
                f"{', '.join(sorted(set(leaked)))} -- masking the audio while the "
                f"caption spells it out defeats both the joke and ad-safety")
    else:
        rep.add("captions", OK, f"{cues} cues, no bleeped words printed in full")


def check_music(rep: Report, edl: dict, base: Path, edit_dir: Path) -> None:
    music = edl.get("music")
    if not music or not music.get("file"):
        rep.add("music", OK, "no bed")
        return
    mpath = render.resolve_path(music["file"], edit_dir)
    if not mpath.exists():
        rep.add("music", WARN, f"declared but missing: {mpath}")
        return
    speech = render.speech_active_rms(base)
    track = render.speech_active_rms(mpath)
    if speech <= 0 or track <= 0:
        rep.add("music", WARN, "could not measure levels")
        return
    # An EDL may declare either an absolute `gain_db` or the preferred
    # `under_db`, which render.py resolves against measured levels at render
    # time. Reading gain_db off an under_db EDL yields 0 and a nonsense verdict.
    if "under_db" in music:
        under = float(music["under_db"])
    else:
        under = 20 * math.log10(speech / track) - float(music.get("gain_db", 0.0))
    if under < 8:
        rep.add("music", FAIL,
                f"bed sits only {under:.1f} dB under dialogue -- it will compete "
                f"with the voice. Specify `under_db` (12-18 is a bed) rather than "
                f"an absolute gain: a quiet lav plus a mastered track makes any "
                f"absolute number misleading.")
    else:
        rep.add("music", OK, f"bed {under:.1f} dB under speech-active dialogue")


def check_loudness(rep: Report, final: Path) -> None:
    err = subprocess.run(
        ["ffmpeg", "-v", "info", "-nostdin", "-i", str(final),
         "-af", "volumedetect", "-vn", "-f", "null", "-"],
        capture_output=True, text=True).stderr
    mean = peak = None
    for line in err.splitlines():
        if "mean_volume:" in line:
            mean = float(line.split("mean_volume:")[1].split("dB")[0])
        if "max_volume:" in line:
            peak = float(line.split("max_volume:")[1].split("dB")[0])
    if mean is None:
        rep.add("loudness", WARN, "could not measure")
        return
    status = OK if (-24 < mean < -10 and (peak or 0) <= -0.3) else WARN
    rep.add("loudness", status,
            f"mean {mean:.1f} dB, peak {peak:.1f} dB"
            + ("" if status == OK else " -- outside the usual delivery window"))


# -------- Main ---------------------------------------------------------------

CHECKS = ("geometry", "channels", "av_lengths", "base_length", "drift",
          "bleeps", "sfx", "captions", "music", "loudness")


def main() -> None:
    ap = argparse.ArgumentParser(description="Verify a rendered film against its EDL.")
    ap.add_argument("--edit-dir", type=Path, default=Path("edit"))
    ap.add_argument("--final", type=Path, help="Rendered file (default: <edit>/final.mp4)")
    ap.add_argument("--skip", nargs="*", default=[], choices=CHECKS,
                    help="Checks to skip; `drift` is by far the slowest")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()

    edit_dir = args.edit_dir.resolve()
    edl_path = edit_dir / "edl.json"
    if not edl_path.exists():
        sys.exit(f"no EDL at {edl_path}")
    edl = json.loads(edl_path.read_text())
    final = (args.final or edit_dir / "final.mp4").resolve()

    clips = sorted((edit_dir / "clips_graded").glob("seg_*.mkv"))
    if not clips:
        clips = sorted((edit_dir / "clips_graded").glob("seg_*.mp4"))
    base = next((edit_dir / n for n in ("base.mkv", "base.mp4")
                 if (edit_dir / n).exists()), None)

    nom, real, durs = render.frame_quantized_offsets(edl)
    rep = Report()
    print(f"verifying {final.name} against {edl_path.name}\n")

    def want(name: str) -> bool:
        return name not in args.skip

    if clips:
        if want("geometry"):
            check_geometry(rep, clips, final)
        if want("channels"):
            check_channels(rep, clips)
        if want("av_lengths"):
            check_av_lengths(rep, edl, clips, durs)
    else:
        rep.add("segments", WARN, "no extracted segments found; "
                                  "geometry/channel/length checks skipped")
    if base:
        if want("base_length"):
            check_base(rep, base, durs)
        if clips and want("drift"):
            check_drift(rep, edl, base, clips, real)
        if want("music"):
            check_music(rep, edl, base, edit_dir)
    else:
        rep.add("base", WARN, "no base.mkv/base.mp4; drift and music checks skipped")

    if final.exists():
        if want("bleeps"):
            check_bleeps(rep, edl, final, nom, real)
        if want("sfx"):
            check_sfx(rep, edl, final, nom, real)
        if want("loudness"):
            check_loudness(rep, final)
    else:
        rep.add("final", FAIL, f"no rendered file at {final}")
    if want("captions"):
        check_captions(rep, edit_dir, edl)

    n_fail = sum(1 for r in rep.rows if r["status"] == FAIL)
    n_warn = sum(1 for r in rep.rows if r["status"] == WARN)
    print(f"\n{len(rep.rows)} checks: {len(rep.rows) - n_fail - n_warn} ok, "
          f"{n_warn} warn, {n_fail} fail")
    if args.json:
        print(json.dumps(rep.rows, indent=2))
    sys.exit(1 if rep.failed else 0)


if __name__ == "__main__":
    main()
