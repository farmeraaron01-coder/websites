"""Render a video from an EDL.

The pipeline order is load-bearing, not stylistic:

  1. Per-segment extract with colour grade + 30 ms audio fades baked in.
  2. Lossless `-c copy` concat into base.mp4. Cutting and concatenating in one
     filtergraph instead would re-encode every frame twice.
  3. One composite pass: B-roll cutaways, then animation overlays, then the
     `subtitles` filter LAST -> final.mp4. Every layer is PTS-shifted so its
     frame 0 lands at its output position.
  4. Two-pass loudness normalization to -14 LUFS for social delivery.

Getting step 3's order wrong fails silently: composite anything after the
subtitles and the captions are simply not in the finished file.

EDL schema
----------
    {
      "version": 1,
      "sources": {"A001": "/abs/path/A001.MP4"},
      "ranges": [
        {"source": "A001", "start": 2.42, "end": 6.85,
         "beat": "HOOK", "quote": "...", "reason": "cleanest take"}
      ],
      "grade": "auto",                    | preset name | raw ffmpeg filter
      "broll": [
        {"file": "b_roll/sizzle.MP4",     # cutaway; narration keeps running
         "src_start": 12.4,               # in-point in the B-roll source
         "start_in_output": 34.2,         # where it lands on the cut timeline
         "duration": 3.5,
         "mode": "full",                  | "pip"
         "position": "br",                # pip only: tl|tr|bl|br|center
         "scale": 0.32,                   # pip only: fraction of frame width
         "audio": "duck",                 # mute (default) | duck | full
         "duck_db": -10,                  # how far the narration drops
         "audio_gain_db": 0,              # trim on the insert's own sound
         "speed": 1.0,
         "grade": "warm_cinematic"}
      ],
      "overlays": [
        {"file": "animations/slot_1/render.mp4",
         "start_in_output": 0.0, "duration": 5.0}
      ],
      "subtitles": "master.srt",
      "total_duration_s": 87.4
    }

Relative paths resolve against the EDL's own directory.

Usage:
    python helpers/render.py <edl.json> -o final.mp4
    python helpers/render.py <edl.json> -o preview.mp4 --preview
    python helpers/render.py <edl.json> -o draft.mp4 --draft
    python helpers/render.py <edl.json> -o final.mp4 --build-subtitles
    python helpers/render.py <edl.json> -o cut.mp4 --no-broll --no-subtitles
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path

try:
    from grade import get_preset, auto_grade_for_clip  # same directory
except Exception:
    def get_preset(name: str) -> str:
        return ""

    def auto_grade_for_clip(video, start=0.0, duration=None, verbose=False):  # type: ignore
        return "eq=contrast=1.03:saturation=0.98", {}


# -------- Subtitle style (bold-overlay, proven at 1920×1080 and 1080×1920) --
#
# MarginV is NOT taste — it is a platform safe-zone rule.
# TikTok / IG Reels / Shorts UI (caption, username, music, right-rail actions)
# covers roughly the bottom ~25–30% of a 1080×1920 frame. Captions placed near
# the bottom edge get clipped or obscured by the UI. libass auto-scales the
# render canvas relative to PlayResY=288, so MarginV=90 lands the caption
# baseline roughly 30% up from the bottom on any aspect — clear of the UI on
# every major vertical-video platform. Do not drop this below ~75 without a
# specific reason.
SUB_MARGIN_V_VERTICAL = 90
# Landscape has no app chrome eating the bottom of the frame, and a caption
# lifted 30% up the picture there just floats in the middle of the shot.
SUB_MARGIN_V_LANDSCAPE = 42


def sub_force_style(canvas_w: int, canvas_h: int) -> str:
    margin = SUB_MARGIN_V_VERTICAL if canvas_h > canvas_w else SUB_MARGIN_V_LANDSCAPE
    return (
        "FontName=Helvetica,FontSize=18,Bold=1,"
        "PrimaryColour=&H00FFFFFF,OutlineColour=&H00000000,BackColour=&H00000000,"
        "BorderStyle=1,Outline=2,Shadow=0,"
        f"Alignment=2,MarginV={margin}"
    )


SUB_FORCE_STYLE = sub_force_style(1080, 1920)

# -------- Helpers ------------------------------------------------------------


def run(cmd: list[str], quiet: bool = False) -> None:
    if not quiet:
        print(f"  $ {' '.join(str(c) for c in cmd[:6])}{' …' if len(cmd) > 6 else ''}")
    subprocess.run(cmd, check=True)


def resolve_grade_filter(grade_field: str | None) -> str:
    """The EDL's 'grade' field can be a preset name, a raw ffmpeg filter, or 'auto'.

    Returns the filter string to embed into the per-segment -vf chain.
    For 'auto', returns the sentinel "__AUTO__" which is resolved per-segment.
    """
    if not grade_field:
        return ""
    if grade_field == "auto":
        return "__AUTO__"
    # Preset names are short identifiers, filter strings contain '=' or ','.
    if re.fullmatch(r"[a-zA-Z0-9_\-]+", grade_field):
        try:
            return get_preset(grade_field)
        except KeyError:
            print(f"warning: unknown preset '{grade_field}', using as raw filter")
            return grade_field
    return grade_field


def resolve_path(maybe_path: str, base: Path) -> Path:
    """Resolve a path that may be absolute or relative to `base`."""
    p = Path(maybe_path)
    if p.is_absolute():
        return p
    return (base / p).resolve()


# -------- HDR → SDR tone mapping (HLG / PQ sources) --------------------------
#
# iPhone defaults to HLG HDR in Rec.2020 (and many mirrorless cameras ship PQ).
# If the source is HDR and we only downconvert bit depth (yuv420p10le → yuv420p)
# without tone-mapping, the output is 8-bit but still carries HLG/PQ transfer
# metadata. Players that honor the metadata (screen recorders, most social
# upload re-encodes) interpret 8-bit values in an HDR container and the result
# looks oversaturated / blown out. QuickTime on macOS can hide this locally —
# screen recording and uploaded renders cannot.
#
# Fix: detect HDR via color_transfer and prepend a zscale+tonemap chain to the
# vf graph so the output is clean Rec.709 SDR.

OUT_FPS = 24

HDR_TRANSFERS = {"smpte2084", "arib-std-b67"}  # PQ (HDR10) and HLG

TONEMAP_CHAIN = (
    "zscale=t=linear:npl=100,"
    "format=gbrpf32le,"
    "zscale=p=bt709,"
    "tonemap=tonemap=hable:desat=0,"
    "zscale=t=bt709:m=bt709:r=tv,"
    "format=yuv420p"
)


def is_hdr_source(video: Path) -> bool:
    """Return True if the source uses a PQ or HLG transfer function."""
    try:
        out = subprocess.run(
            ["ffprobe", "-v", "error", "-select_streams", "v:0",
             "-show_entries", "stream=color_transfer",
             "-of", "default=noprint_wrappers=1:nokey=1", str(video)],
            capture_output=True, text=True, check=True,
        )
        return out.stdout.strip() in HDR_TRANSFERS
    except subprocess.CalledProcessError:
        return False


def is_portrait_source(video: Path) -> bool:
    """Return True if the video's height > width (portrait / vertical)."""
    try:
        out = subprocess.run(
            ["ffprobe", "-v", "error", "-select_streams", "v:0",
             "-show_entries", "stream=width,height",
             "-of", "csv=p=0", str(video)],
            capture_output=True, text=True, check=True,
        )
        w, h = map(int, out.stdout.strip().split(","))
        return h > w
    except Exception:
        return False


# -------- Per-segment extraction (Rule 2 + Rule 3) --------------------------


def conform_filter(source: Path, canvas_w: int, canvas_h: int,
                   fit: str = "blur", crop_y: float = 0.5) -> str:
    """Scale a source onto the output canvas, whatever shape it arrived in.

    Every segment MUST come out at exactly the canvas size. The concat demuxer
    cannot join streams of differing dimensions -- it takes the first stream's
    geometry and the rest arrive squeezed, with no error anywhere. A single
    vertical phone clip in an otherwise horizontal edit is enough to do it.

    Two ways to reconcile a mismatch, and the right one depends on the shot:

      blur  letterbox over a blurred, zoomed copy of the frame. Nothing is
            cropped, so it is always safe -- use it when the subject fills the
            tall frame, such as a head-to-waist selfie.
      crop  fill the canvas and cut off the overflow. Stronger and more
            immersive, but it discards most of a vertical frame, so it only
            works when the subject sits inside the surviving band. `crop_y`
            biases which band survives: 0 top, 0.5 centre, 1 bottom.
    """
    try:
        w, h = probe_dimensions(source)
    except Exception:
        w, h = canvas_w, canvas_h
    if is_portrait_rotated(source):
        w, h = h, w

    src_ar, dst_ar = w / max(h, 1), canvas_w / canvas_h
    if abs(src_ar - dst_ar) < 0.02:
        return f"scale={canvas_w}:{canvas_h}"

    if fit == "crop":
        y = f"(ih-oh)*{max(0.0, min(1.0, crop_y)):.3f}"
        return (f"scale={canvas_w}:{canvas_h}:force_original_aspect_ratio=increase,"
                f"crop={canvas_w}:{canvas_h}:(iw-ow)/2:{y}")

    return (
        f"split=2[bg][fg];"
        f"[bg]scale={canvas_w}:{canvas_h}:force_original_aspect_ratio=increase,"
        f"crop={canvas_w}:{canvas_h},gblur=sigma=28[bgb];"
        f"[fg]scale={canvas_w}:{canvas_h}:force_original_aspect_ratio=decrease[fgs];"
        f"[bgb][fgs]overlay=(W-w)/2:(H-h)/2"
    )


def is_portrait_rotated(video: Path) -> bool:
    """True when rotation metadata makes a stored-landscape frame display tall."""
    try:
        out = subprocess.run(
            ["ffprobe", "-v", "error", "-select_streams", "v:0",
             "-show_entries", "stream_side_data=rotation",
             "-of", "default=noprint_wrappers=1:nokey=1", str(video)],
            capture_output=True, text=True, check=True,
        ).stdout.strip().splitlines()
        return bool(out) and int(round(float(out[0]))) % 180 == 90
    except Exception:
        return False


def extract_segment(
    source: Path,
    seg_start: float,
    duration: float,
    grade_filter: str,
    out_path: Path,
    canvas: tuple[int, int],
    preview: bool = False,
    draft: bool = False,
    fit: str = "blur",
    crop_y: float = 0.5,
) -> None:
    """Extract a cut range as its own MP4 with grade + 30ms audio fades baked in.

    `-ss` before `-i` for fast accurate seeking. Every segment is conformed to
    the same canvas so the lossless concat that follows is legal.

    Quality ladder:
      - final (default): libx264 fast CRF 20
      - preview:         libx264 medium CRF 22 (evaluable for QC)
      - draft:           720p-class libx264 ultrafast CRF 28 (cut-point check)
    """
    out_path.parent.mkdir(parents=True, exist_ok=True)
    canvas_w, canvas_h = canvas

    conform = conform_filter(source, canvas_w, canvas_h, fit, crop_y)
    # A conform that needs `split` is a filtergraph, not a linear chain, so the
    # grade has to be appended to its final node rather than comma-joined.
    vf_parts: list[str] = []
    if is_hdr_source(source):
        vf_parts.append(TONEMAP_CHAIN)
    if vf_parts and "split=" in conform:
        # Tone map first, then hand the result to the conform graph.
        vf = ",".join(vf_parts) + "," + conform
    else:
        vf_parts.append(conform)
        vf = ",".join(vf_parts)
    if grade_filter:
        vf = f"{vf},{grade_filter}"

    # The video encoder can only emit whole frames, so a nominal duration
    # gets rounded up and the audio (cut exactly) comes out shorter. Concat
    # advances by file duration, so that mismatch becomes a per-cut timeline
    # slip that accumulates -- 17 cuts cost 300ms, and every bleep, caption
    # and cutaway placed on the nominal clock landed early by that much.
    # Fix: decide the frame count up front, and pad the audio to exactly the
    # duration those frames occupy. The pad is silence landing on the fade-out,
    # so it is inaudible.
    n_frames = max(1, round(duration * OUT_FPS))
    vdur = n_frames / OUT_FPS

    # 30ms audio fades at both edges (Rule 3) — prevent pops
    fade_out_start = max(0.0, duration - 0.03)
    af = (f"afade=t=in:st=0:d=0.03,afade=t=out:st={fade_out_start:.3f}:d=0.03,"
          f"apad")

    if draft:
        preset, crf = "ultrafast", "28"
    elif preview:
        preset, crf = "medium", "22"
    else:
        preset, crf = "fast", "20"

    cmd = [
        "ffmpeg", "-y",
        "-ss", f"{seg_start:.3f}",
        "-i", str(source),
        "-t", f"{vdur:.6f}",
        "-frames:v", str(n_frames),
        "-vf", vf,
        "-af", af,
        "-c:v", "libx264", "-preset", preset, "-crf", crf,
        "-pix_fmt", "yuv420p", "-r", str(OUT_FPS),
        "-c:a", "aac", "-b:a", "192k", "-ar", "48000",
        "-movflags", "+faststart",
        str(out_path),
    ]
    subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)


def frame_quantized_offsets(edl: dict) -> tuple[list[float], list[float], list[float]]:
    """Nominal vs real cumulative segment offsets.

    Authors place features (bleeps, cutaways, overlays, captions) on the
    timeline implied by the EDL's range durations. The rendered timeline is
    those durations quantized to whole frames, so each feature has to be
    translated. Returns (nominal_offsets, real_offsets, real_durations).
    """
    nominal, real, durs = [], [], []
    cn = cr = 0.0
    for r in edl["ranges"]:
        nominal.append(cn)
        real.append(cr)
        d = float(r["end"]) - float(r["start"])
        vd = max(1, round(d * OUT_FPS)) / OUT_FPS
        durs.append(vd)
        cn += d
        cr += vd
    return nominal, real, durs


def remap_output_time(t: float, nominal: list[float], real: list[float]) -> float:
    """Translate a nominal output time onto the frame-quantized timeline."""
    for i in range(len(nominal) - 1, -1, -1):
        if t >= nominal[i] - 1e-6:
            return real[i] + (t - nominal[i])
    return t


def choose_canvas(edl: dict, edit_dir: Path, draft: bool) -> tuple[int, int]:
    """Decide the output geometry once, for the whole edit.

    Taken from the EDL's `canvas` if given, otherwise from whichever
    orientation carries the most screen time. Deciding per-segment is what
    breaks the concat, so this is deliberately a single global choice.
    """
    if edl.get("canvas"):
        w, h = (int(v) for v in str(edl["canvas"]).lower().split("x"))
    else:
        land = tall = 0.0
        for r in edl["ranges"]:
            src = resolve_path(edl["sources"][r["source"]], edit_dir)
            dur = float(r["end"]) - float(r["start"])
            try:
                sw, sh = probe_dimensions(src)
            except Exception:
                continue
            if is_portrait_rotated(src):
                sw, sh = sh, sw
            if sh > sw:
                tall += dur
            else:
                land += dur
        w, h = (1080, 1920) if tall > land else (1920, 1080)
    if draft:
        w, h = (w * 2 // 3) // 2 * 2, (h * 2 // 3) // 2 * 2
    print(f"canvas: {w}x{h}" + ("  (draft scale)" if draft else ""))
    return w, h


def extract_all_segments(
    edl: dict,
    edit_dir: Path,
    preview: bool,
    draft: bool = False,
) -> list[Path]:
    """Extract every EDL range into edit_dir/clips_graded/seg_NN.mp4.
    Returns the ordered list of segment paths.

    If the EDL `grade` is "auto", analyze each segment range with
    `auto_grade_for_clip` and apply a per-segment subtle correction.
    Otherwise, apply the same preset/raw filter to every segment.
    """
    canvas = choose_canvas(edl, edit_dir, draft)
    resolved = resolve_grade_filter(edl.get("grade"))
    is_auto = resolved == "__AUTO__"
    clips_dir = edit_dir / (
        "clips_draft" if draft else ("clips_preview" if preview else "clips_graded")
    )
    clips_dir.mkdir(parents=True, exist_ok=True)

    ranges = edl["ranges"]
    sources = edl["sources"]

    seg_paths: list[Path] = []
    print(f"extracting {len(ranges)} segment(s) → {clips_dir.name}/")
    if is_auto:
        print("  (auto-grade per segment: analyzing each range)")
    for i, r in enumerate(ranges):
        src_name = r["source"]
        src_path = resolve_path(sources[src_name], edit_dir)
        start = float(r["start"])
        end = float(r["end"])
        duration = end - start
        out_path = clips_dir / f"seg_{i:02d}_{src_name}.mp4"

        if is_auto:
            seg_filter, _stats = auto_grade_for_clip(src_path, start=start, duration=duration, verbose=False)
        else:
            seg_filter = resolved

        note = r.get("beat") or r.get("note") or ""
        print(f"  [{i:02d}] {src_name}  {start:7.2f}-{end:7.2f}  ({duration:5.2f}s)  {note}")
        if is_auto:
            print(f"        grade: {seg_filter or '(none)'}")
        extract_segment(src_path, start, duration, seg_filter, out_path,
                        canvas, preview=preview, draft=draft,
                        fit=r.get("fit", "blur"), crop_y=float(r.get("crop_y", 0.5)))
        seg_paths.append(out_path)

    return seg_paths


# -------- Lossless concat ----------------------------------------------------


def concat_segments(segment_paths: list[Path], out_path: Path, edit_dir: Path) -> None:
    """Lossless concat via the concat demuxer. No re-encode."""
    out_path.parent.mkdir(parents=True, exist_ok=True)
    concat_list = edit_dir / "_concat.txt"
    concat_list.write_text("".join(f"file '{p.resolve()}'\n" for p in segment_paths))

    cmd = [
        "ffmpeg", "-y",
        "-f", "concat", "-safe", "0",
        "-i", str(concat_list),
        "-c", "copy",
        "-movflags", "+faststart",
        str(out_path),
    ]
    print(f"concat → {out_path.name}")
    subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)
    concat_list.unlink(missing_ok=True)


# -------- B-roll preparation -------------------------------------------------
#
# B-roll is a cutaway: the voiceover keeps running underneath while the picture
# cuts to something else. That makes it fundamentally different from an
# animation overlay, in three ways the schema has to respect:
#
#   1. It comes from a real source file and needs an in-point (`src_start`),
#      not just a duration.
#   2. It usually keeps the BASE audio, because the whole point is that the
#      narration continues. But for food, machinery, crowds -- anything where
#      the sound IS the shot -- you want its natural audio mixed in under the
#      voice. Hence the `audio` mode.
#   3. It can be full-frame or picture-in-picture.
#
# Each insert is pre-rendered to a normalized clip so the composite pass is a
# plain overlay with no per-clip format surprises.

PIP_POSITIONS = {
    "tl": ("{m}", "{m}"),
    "tr": ("main_w-overlay_w-{m}", "{m}"),
    "bl": ("{m}", "main_h-overlay_h-{m}"),
    "br": ("main_w-overlay_w-{m}", "main_h-overlay_h-{m}"),
    "center": ("(main_w-overlay_w)/2", "(main_h-overlay_h)/2"),
}

BROLL_AUDIO_MODES = {"mute", "duck", "full"}


def source_duration(path: Path) -> float:
    try:
        out = subprocess.run(
            ["ffprobe", "-v", "error", "-show_entries", "format=duration",
             "-of", "default=noprint_wrappers=1:nokey=1", str(path)],
            capture_output=True, text=True, check=True,
        )
        return float(out.stdout.strip())
    except Exception:
        return 0.0


def prepare_broll(
    broll: list[dict],
    edit_dir: Path,
    base_width: int,
    base_height: int,
    preview: bool = False,
    draft: bool = False,
) -> list[dict]:
    """Normalize every B-roll insert to a clip that matches the base timeline.

    Returns the insert dicts with a resolved `_clip` path added. Anything that
    cannot be prepared is dropped with a warning rather than failing the whole
    render -- losing one cutaway is better than losing the cut.
    """
    if not broll:
        return []

    clips_dir = edit_dir / ("broll_draft" if draft else "broll_clips")
    clips_dir.mkdir(parents=True, exist_ok=True)
    preset, crf = ("ultrafast", "28") if draft else ("fast", "20")

    prepared: list[dict] = []
    print(f"preparing {len(broll)} B-roll insert(s) -> {clips_dir.name}/")
    for i, b in enumerate(broll):
        src = resolve_path(b["file"], edit_dir)
        if not src.exists():
            print(f"  [{i:02d}] MISSING {src} -- skipping this insert")
            continue

        src_start = float(b.get("src_start", 0.0))
        duration = float(b["duration"])
        speed = float(b.get("speed", 1.0))
        mode = b.get("mode", "full")

        # Reading `duration` seconds of OUTPUT at speed S needs S * duration
        # seconds of source.
        needed = duration * speed
        avail = source_duration(src) - src_start
        if avail <= 0:
            print(f"  [{i:02d}] {src.name}: src_start {src_start:.2f}s is past the "
                  f"end of the file -- skipping")
            continue
        if needed > avail + 0.05:
            print(f"  [{i:02d}] {src.name}: wanted {needed:.2f}s from {src_start:.2f}s "
                  f"but only {avail:.2f}s remain -- trimming the insert")
            needed = avail
            duration = needed / speed

        if mode == "pip":
            scale_frac = float(b.get("scale", 0.32))
            target_w = int(base_width * scale_frac) // 2 * 2
            scale = f"scale={target_w}:-2"
        else:
            # Fill the frame: scale up to cover, then crop off the excess, so a
            # vertical cutaway in a horizontal film does not get pillarboxed.
            scale = (f"scale={base_width}:{base_height}:force_original_aspect_ratio=increase,"
                     f"crop={base_width}:{base_height}")

        vf_parts: list[str] = []
        if is_hdr_source(src):
            vf_parts.append(TONEMAP_CHAIN)
        vf_parts.append(scale)
        if speed != 1.0:
            vf_parts.append(f"setpts={1.0 / speed:.6f}*PTS")
        if b.get("grade"):
            vf_parts.append(resolve_grade_filter(b["grade"]) or "")
        vf = ",".join(p for p in vf_parts if p)

        out_clip = clips_dir / f"broll_{i:02d}_{src.stem}.mp4"
        cmd = [
            "ffmpeg", "-y", "-v", "error", "-nostdin",
            "-ss", f"{src_start:.3f}", "-i", str(src),
            "-t", f"{needed:.3f}",
            "-vf", vf,
            "-c:v", "libx264", "-preset", preset, "-crf", crf,
            "-pix_fmt", "yuv420p", "-r", "24",
        ]
        audio_mode = b.get("audio", "mute")
        if audio_mode not in BROLL_AUDIO_MODES:
            print(f"  [{i:02d}] unknown audio mode {audio_mode!r}, treating as 'mute'")
            audio_mode = "mute"
        if audio_mode == "mute":
            cmd += ["-an"]
        else:
            af = [f"atempo={speed:.6f}"] if speed != 1.0 else []
            af.append("aresample=48000")
            cmd += ["-af", ",".join(af), "-c:a", "aac", "-b:a", "192k", "-ar", "48000"]
        cmd += ["-movflags", "+faststart", str(out_clip)]

        try:
            subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL,
                           stderr=subprocess.PIPE)
        except subprocess.CalledProcessError as exc:
            print(f"  [{i:02d}] {src.name}: ffmpeg failed -- skipping this insert\n"
                  f"        {exc.stderr.decode()[-300:] if exc.stderr else ''}")
            continue

        note = b.get("note", "")
        print(f"  [{i:02d}] {src.name} @{src_start:6.2f}s -> out {b['start_in_output']:6.2f}s "
              f"({duration:4.2f}s, {mode}, audio={audio_mode}) {note}")

        entry = dict(b)
        entry["_clip"] = out_clip
        entry["duration"] = duration
        entry["audio"] = audio_mode
        entry["mode"] = mode
        prepared.append(entry)

    return prepared


def has_alpha(path: Path) -> bool:
    """Does this overlay carry a transparency channel?

    WebM stores VP9 alpha as a side stream flagged by the `alpha_mode` tag, so
    the pixel format alone reports plain yuv420p and tells you nothing. Check
    the tag as well as the pixel format.
    """
    try:
        out = subprocess.run(
            ["ffprobe", "-v", "error", "-select_streams", "v:0",
             "-show_entries", "stream=pix_fmt:stream_tags=alpha_mode",
             "-of", "default=noprint_wrappers=1:nokey=1", str(path)],
            capture_output=True, text=True, check=True,
        ).stdout
    except subprocess.CalledProcessError:
        return False
    fields = [line.strip() for line in out.splitlines() if line.strip()]
    return any(f == "1" for f in fields) or any("a" in f for f in fields
                                                if f.startswith(("yuva", "rgba", "bgra")))


def _overlay_input_args(path: Path) -> list[str]:
    """Input args for an overlay, forcing the alpha-aware decoder for WebM.

    ffmpeg's built-in vp9 decoder silently discards the alpha side stream;
    libvpx-vp9 keeps it. Choosing the wrong one here produces a graphic that
    renders as a black box over the picture -- with no error anywhere.
    """
    if path.suffix.lower() == ".webm":
        return ["-c:v", "libvpx-vp9", "-i", str(path)]
    return ["-i", str(path)]


def probe_dimensions(video: Path) -> tuple[int, int]:
    out = subprocess.run(
        ["ffprobe", "-v", "error", "-select_streams", "v:0",
         "-show_entries", "stream=width,height", "-of", "csv=p=0", str(video)],
        capture_output=True, text=True, check=True,
    )
    w, h = out.stdout.strip().split(",")[:2]
    return int(w), int(h)


# -------- Master SRT (Rule 5) ------------------------------------------------


PUNCT_BREAK = set(".,!?;:")


def _srt_timestamp(seconds: float) -> str:
    total_ms = int(round(seconds * 1000))
    h, rem = divmod(total_ms, 3600_000)
    m, rem = divmod(rem, 60_000)
    s, ms = divmod(rem, 1000)
    return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"


def _words_in_range(transcript: dict, t_start: float, t_end: float) -> list[dict]:
    out: list[dict] = []
    for w in transcript.get("words", []):
        if w.get("type") != "word":
            continue
        ws = w.get("start")
        we = w.get("end")
        if ws is None or we is None:
            continue
        if we <= t_start or ws >= t_end:
            continue
        out.append(w)
    return out


def find_transcript(transcripts_dir: Path, src_name: str, src_path: Path) -> Path | None:
    """Locate the transcript for an EDL source.

    Transcripts are named after the media file they were made FROM, which is
    usually the synced copy -- so an EDL keyed "A001" whose file is
    "synced/A001_synced.mp4" has its words in "A001_synced.json". Checking only
    the EDL key silently produces zero captions for every segment.
    """
    for stem in (src_path.stem, src_name):
        p = transcripts_dir / f"{stem}.json"
        if p.exists():
            return p
    return None


def _mask_bleeped(text: str, a: float, b: float,
                  bleeps: list[dict]) -> str:
    """Grawlix a caption cue that overlaps a censor bleep.

    Bleeping the audio while the burned caption prints the word in full
    uppercase defeats both the joke and the ad-safety -- a TV censor masks
    picture and sound together. Keep the first letter, star the rest.
    """
    for bl in bleeps:
        t0 = float(bl["start_in_output"])
        t1 = t0 + float(bl["duration"])
        if b > t0 and a < t1:
            word = (bl.get("note") or "").strip().upper()
            if word:
                masked = word[0] + "*" * max(1, len(word) - 1)
                text = re.sub(re.escape(word), masked, text)
    return text


def build_master_srt(edl: dict, edit_dir: Path, out_path: Path,
                     seg_durations: list[float] | None = None) -> int:
    """Build an output-timeline SRT from per-source transcripts.

    - 2-word chunks (break on any punctuation in between)
    - UPPERCASE text
    - Words under a censor bleep are masked to match the audio
    - Output times computed as word.start - segment_start + segment_offset

    Returns the cue count so the caller can skip the subtitles filter when it
    is zero -- libass errors out on an empty file rather than ignoring it.
    """
    transcripts_dir = edit_dir / "transcripts"
    sources = edl["sources"]

    entries: list[tuple[float, float, str]] = []
    seg_offset = 0.0

    for ri, r in enumerate(edl["ranges"]):
        src_name = r["source"]
        seg_start = float(r["start"])
        seg_end = float(r["end"])
        seg_duration = (seg_durations[ri] if seg_durations
                        else seg_end - seg_start)

        tr_path = find_transcript(transcripts_dir, src_name,
                                  resolve_path(sources[src_name], edit_dir))
        if tr_path is None:
            print(f"  no transcript for {src_name}, skipping captions for this segment")
            seg_offset += seg_duration
            continue

        transcript = json.loads(tr_path.read_text())
        words_in_seg = _words_in_range(transcript, seg_start, seg_end)

        # Group into 2-word chunks, break on punctuation
        chunks: list[list[dict]] = []
        current: list[dict] = []
        for w in words_in_seg:
            text = (w.get("text") or "").strip()
            if not text:
                continue
            current.append(w)
            # Break if the current text ends in punctuation or we hit 2 words
            ends_in_punct = bool(text) and text[-1] in PUNCT_BREAK
            if len(current) >= 2 or ends_in_punct:
                chunks.append(current)
                current = []
        if current:
            chunks.append(current)

        for chunk in chunks:
            local_start = max(seg_start, chunk[0].get("start", seg_start))
            local_end = min(seg_end, chunk[-1].get("end", seg_end))
            out_start = max(0.0, local_start - seg_start) + seg_offset
            out_end = max(0.0, local_end - seg_start) + seg_offset
            if out_end <= out_start:
                out_end = out_start + 0.4
            text = " ".join((w.get("text") or "").strip() for w in chunk)
            text = re.sub(r"\s+", " ", text).strip()
            # Strip trailing punctuation for cleaner uppercase look
            text = text.rstrip(",;:")
            text = text.upper()
            text = _mask_bleeped(text, out_start, out_end, edl.get("bleeps") or [])
            entries.append((out_start, out_end, text))

        seg_offset += seg_duration

    # Sort and write as SRT
    entries.sort(key=lambda e: e[0])
    lines: list[str] = []
    for i, (a, b, t) in enumerate(entries, start=1):
        lines.append(str(i))
        lines.append(f"{_srt_timestamp(a)} --> {_srt_timestamp(b)}")
        lines.append(t)
        lines.append("")
    out_path.write_text("\n".join(lines))
    print(f"master SRT → {out_path.name} ({len(entries)} cues)")
    return len(entries)


# -------- Loudness normalization (social-ready audio) -----------------------


# Social-media standard: -14 LUFS integrated, -1 dBTP peak, LRA 11 LU.
# Matches YouTube / Instagram / TikTok / X / LinkedIn normalization targets.
LOUDNORM_I = -14.0
LOUDNORM_TP = -1.0
LOUDNORM_LRA = 11.0


def measure_loudness(video_path: Path) -> dict[str, str] | None:
    """Run ffmpeg loudnorm first pass and parse the JSON measurement.

    Returns a dict with measured_i, measured_tp, measured_lra, measured_thresh,
    target_offset, or None if measurement failed.
    """
    filter_str = (
        f"loudnorm=I={LOUDNORM_I}:TP={LOUDNORM_TP}:LRA={LOUDNORM_LRA}:print_format=json"
    )
    cmd = [
        "ffmpeg", "-y", "-hide_banner", "-nostats",
        "-i", str(video_path),
        "-af", filter_str,
        "-vn", "-f", "null", "-",
    ]
    proc = subprocess.run(cmd, capture_output=True, text=True)
    # loudnorm prints the JSON to stderr at the end of the run
    stderr = proc.stderr

    # Find the JSON block — loudnorm output contains a `{ ... }` block
    start = stderr.rfind("{")
    end = stderr.rfind("}")
    if start == -1 or end == -1 or end <= start:
        return None
    try:
        data = json.loads(stderr[start : end + 1])
    except json.JSONDecodeError:
        return None
    needed = {"input_i", "input_tp", "input_lra", "input_thresh", "target_offset"}
    if not needed.issubset(data.keys()):
        return None
    return data


def apply_loudnorm_two_pass(
    input_path: Path,
    output_path: Path,
    preview: bool = False,
) -> bool:
    """Run two-pass loudnorm on input_path, write normalized copy to output_path.

    Returns True on success, False if measurement failed (caller should fall
    back to copying the input unchanged).

    In preview mode, skips the measurement pass and uses a one-pass approximation
    for speed. Final mode always does the proper two-pass.
    """
    if preview:
        # One-pass approximation — faster, slightly less accurate.
        filter_str = f"loudnorm=I={LOUDNORM_I}:TP={LOUDNORM_TP}:LRA={LOUDNORM_LRA}"
        cmd = [
            "ffmpeg", "-y", "-hide_banner", "-nostats",
            "-i", str(input_path),
            "-c:v", "copy",
            "-af", filter_str,
            "-c:a", "aac", "-b:a", "192k", "-ar", "48000",
            "-movflags", "+faststart",
            str(output_path),
        ]
        print(f"  loudnorm (1-pass preview) → {output_path.name}")
        subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)
        return True

    # Full two-pass
    print(f"  loudnorm pass 1: measuring {input_path.name}")
    measurement = measure_loudness(input_path)
    if measurement is None:
        print("  loudnorm measurement failed — falling back to 1-pass")
        return apply_loudnorm_two_pass(input_path, output_path, preview=True)

    print(f"    measured: I={measurement['input_i']} LUFS  "
          f"TP={measurement['input_tp']}  LRA={measurement['input_lra']}")

    filter_str = (
        f"loudnorm=I={LOUDNORM_I}:TP={LOUDNORM_TP}:LRA={LOUDNORM_LRA}"
        f":measured_I={measurement['input_i']}"
        f":measured_TP={measurement['input_tp']}"
        f":measured_LRA={measurement['input_lra']}"
        f":measured_thresh={measurement['input_thresh']}"
        f":offset={measurement['target_offset']}"
        f":linear=true"
    )
    cmd = [
        "ffmpeg", "-y", "-hide_banner", "-nostats",
        "-i", str(input_path),
        "-c:v", "copy",
        "-af", filter_str,
        "-c:a", "aac", "-b:a", "192k", "-ar", "48000",
        "-movflags", "+faststart",
        str(output_path),
    ]
    print(f"  loudnorm pass 2: normalizing → {output_path.name}")
    subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)
    return True


# -------- Final compositing (Rule 1 + Rule 4) -------------------------------


def build_final_composite(
    base_path: Path,
    overlays: list[dict],
    subtitles_path: Path | None,
    out_path: Path,
    edit_dir: Path,
    broll: list[dict] | None = None,
    bleeps: list[dict] | None = None,
    total_duration: float = 0.0,
) -> None:
    """Final pass: base -> B-roll -> overlays -> subtitles LAST -> out.

    The layer order is not arbitrary. B-roll replaces the picture, so it goes
    down first; a lower-third or callout has to sit ON the cutaway, not under
    it; and subtitles go last because anything composited after them would
    hide them (Rule 1). Get this order wrong and the failure is silent -- the
    render succeeds and the captions are simply gone.
    """
    broll, bleeps = broll or [], bleeps or []
    has_subs = subtitles_path is not None and subtitles_path.exists()

    if not broll and not overlays and not has_subs and not bleeps:
        run(["ffmpeg", "-y", "-i", str(base_path), "-c", "copy", str(out_path)], quiet=True)
        return

    # Input order: base, then B-roll clips, then animation overlays.
    inputs: list[str] = ["-i", str(base_path)]
    for b in broll:
        inputs += ["-i", str(b["_clip"])]
    alpha_overlay: list[bool] = []
    for ov in overlays:
        ov_path = resolve_path(ov["file"], edit_dir)
        inputs += _overlay_input_args(ov_path)
        alpha_overlay.append(has_alpha(ov_path))

    # The censor tone is a generated source, added last so it cannot shift the
    # indices the video filter graph already refers to.
    tone_idx = None
    if bleeps:
        tone_idx = 1 + len(broll) + len(overlays)
        inputs += ["-f", "lavfi", "-t", f"{max(total_duration, 1.0):.3f}",
                   "-i", f"sine=frequency={BLEEP_HZ}:sample_rate=48000"]

    filter_parts: list[str] = []
    current = "[0:v]"
    idx = 0

    # --- Layer 1: B-roll cutaways ---
    for b in broll:
        idx += 1
        t, dur = float(b["start_in_output"]), float(b["duration"])
        end = t + dur
        # Rule 4: shift PTS so the clip's frame 0 lands at its output position.
        filter_parts.append(f"[{idx}:v]setpts=PTS-STARTPTS+{t}/TB[bv{idx}]")
        if b.get("mode") == "pip":
            pos = b.get("position", "br")
            if pos not in PIP_POSITIONS:
                print(f"  unknown pip position {pos!r}, using 'br'")
                pos = "br"
            margin = "main_w*0.03"
            xe, ye = (e.format(m=margin) for e in PIP_POSITIONS[pos])
            xy = f":x={xe}:y={ye}"
        else:
            xy = ""
        filter_parts.append(
            f"{current}[bv{idx}]overlay=enable='between(t,{t:.3f},{end:.3f})'{xy}[v{idx}]"
        )
        current = f"[v{idx}]"

    base_w, base_h = probe_dimensions(base_path)

    # --- Layer 2: animation overlays, on top of any cutaway ---
    for i, ov in enumerate(overlays):
        idx += 1
        t, dur = float(ov["start_in_output"]), float(ov["duration"])
        end = t + dur
        chain = f"setpts=PTS-STARTPTS+{t}/TB"
        # Full-frame graphics are authored once at delivery size, but a draft
        # renders at a smaller canvas. `overlay` does not rescale -- it pins the
        # graphic at 0,0 and lets the excess hang off the frame, so an oversized
        # card silently loses its right edge and anything positioned to the
        # right or bottom disappears entirely.
        ow, oh = probe_dimensions(resolve_path(ov["file"], edit_dir))
        if ov.get("scale_to_frame", True) and (ow, oh) != (base_w, base_h):
            chain += f",scale={base_w}:{base_h}"
        if alpha_overlay[i]:
            # Force the alpha-carrying format through explicitly. Without it
            # the overlay filter can negotiate a format with no alpha plane and
            # the graphic arrives as an opaque rectangle.
            chain += ",format=yuva420p"
        filter_parts.append(f"[{idx}:v]{chain}[ov{idx}]")
        filter_parts.append(
            f"{current}[ov{idx}]overlay=enable='between(t,{t:.3f},{end:.3f})'[v{idx}]"
        )
        current = f"[v{idx}]"

    # --- Layer 3: subtitles, always last ---
    if has_subs:
        subs_abs = str(subtitles_path.resolve()).replace(":", r"\:").replace("'", r"\'")
        style = sub_force_style(base_w, base_h)
        filter_parts.append(
            f"{current}subtitles='{subs_abs}':force_style='{style}'[outv]")
        out_label = "[outv]"
    elif current != "[0:v]":
        filter_parts.append(f"{current}null[outv]")
        out_label = "[outv]"
    else:
        out_label = "[0:v]"

    # --- Audio: B-roll natural sound, then censor tones ---
    audio_label, audio_codec = _build_audio_chain(broll, bleeps, filter_parts, tone_idx)

    cmd = [
        "ffmpeg", "-y", *inputs,
        "-filter_complex", ";".join(filter_parts),
        "-map", out_label, "-map", audio_label,
        "-c:v", "libx264", "-preset", "fast", "-crf", "18",
        "-pix_fmt", "yuv420p",
        *audio_codec,
        "-movflags", "+faststart",
        str(out_path),
    ]
    print(f"compositing -> {out_path.name}")
    print(f"  b-roll: {len(broll)}, overlays: {len(overlays)}, "
          f"bleeps: {len(bleeps)}, subtitles: {'yes' if has_subs else 'no'}")
    proc = subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)
    if proc.returncode != 0:
        # A failure here is always a filter-graph problem; the message is the
        # only way to know WHICH filter, so burying it costs a whole debug loop.
        tail = proc.stderr.decode(errors="replace")[-2000:] if proc.stderr else ""
        raise SystemExit(f"composite ffmpeg failed (exit {proc.returncode}):\n{tail}")


# How far the narration drops under a B-roll insert's natural sound. -10 dB is
# about a third of the level: the sizzle reads clearly and the voice still wins.
DEFAULT_DUCK_DB = -10.0

# Broadcast censor tone. 1 kHz is the television standard.
BLEEP_HZ = 1000
BLEEP_LEVEL = 0.30              # ~-10 dBFS: unmissable without being painful
BLEEP_COVERAGE = 0.6            # fraction of the word the tone actually covers


def _bleep_windows(bleeps: list[dict]) -> list[tuple[float, float]]:
    """Turn word spans into the spans the tone actually covers.

    A real broadcast censor is always slightly late and slightly short, so you
    catch the front and tail of the word around the tone. Covering only the
    middle `coverage` fraction reproduces that, which is both funnier and more
    legible than a clean full-word mute -- the viewer hears enough to know
    exactly what was said.
    """
    out: list[tuple[float, float]] = []
    for b in bleeps:
        start, dur = float(b["start_in_output"]), float(b["duration"])
        cov = float(b.get("coverage", BLEEP_COVERAGE))
        margin = dur * (1.0 - cov) / 2.0
        a, z = start + margin, start + dur - margin
        if z > a:
            out.append((a, z))
    return out


def _between_expr(windows: list[tuple[float, float]]) -> str:
    return "+".join(f"between(t,{a:.3f},{z:.3f})" for a, z in windows)


def _build_audio_chain(broll: list[dict], bleeps: list[dict],
                       filter_parts: list[str], tone_idx: int | None
                       ) -> tuple[str, list[str]]:
    """Return (audio_map_label, codec_args) for the composite command.

    With nothing to do the base track is copied through untouched -- no
    re-encode, no quality loss.
    """
    voiced = [b for b in broll if b.get("audio") in ("duck", "full")]
    if not voiced and not bleeps:
        return "0:a", ["-c:a", "copy"]

    # Rebase the audio onto a continuous sample-count clock before ANY
    # time-gated filter. The concat demuxer leaves per-segment gaps in the
    # base audio's timestamps, and a `between(t,...)` gate fires on the pts
    # axis -- so without this, gates on the base audio and gates on generated
    # sources (which are continuous) disagree by the accumulated gap, and
    # every censor tone lands early by ~one AAC frame per preceding cut.
    filter_parts.append("[0:a]asetpts=N/SR/TB[a0cont]")
    current = "[a0cont]"

    if voiced:
        # Duck (or fully mute) the base under each insert. A `volume` filter
        # with an `enable` window only acts inside that window.
        base_chain = []
        for b in voiced:
            t = float(b["start_in_output"])
            end = t + float(b["duration"])
            gain = 0.0 if b["audio"] == "full" else \
                10 ** (float(b.get("duck_db", DEFAULT_DUCK_DB)) / 20.0)
            base_chain.append(
                f"volume=enable='between(t,{t:.3f},{end:.3f})':volume={gain:.4f}")
        filter_parts.append(f"{current}{','.join(base_chain)}[baseduck]")
        current = "[baseduck]"

        mix_labels = [current]
        for i, b in enumerate(broll, start=1):
            if b.get("audio") not in ("duck", "full"):
                continue
            t = float(b["start_in_output"])
            gain_db = float(b.get("audio_gain_db", 0.0))
            af = [f"adelay={t * 1000:.1f}:all=1"] if t > 0 else []
            if gain_db:
                af.append(f"volume={gain_db:.2f}dB")
            af.append("aresample=48000")
            filter_parts.append(f"[{i}:a]{','.join(af)}[ba{i}]")
            mix_labels.append(f"[ba{i}]")

        # normalize=0 is essential: amix's default divides every input by the
        # input count, which would silently drop the narration by 6 dB per
        # cutaway.
        filter_parts.append(
            f"{''.join(mix_labels)}amix=inputs={len(mix_labels)}:duration=first:"
            f"dropout_transition=0:normalize=0[premix]")
        current = "[premix]"

    if bleeps and tone_idx is not None:
        windows = _bleep_windows(bleeps)
        if windows:
            expr = _between_expr(windows)
            # `enable` is the wrong tool here: outside its window the filter is
            # bypassed, which would leave the tone at full level everywhere.
            # A per-frame volume EXPRESSION gates properly in both directions.
            filter_parts.append(
                f"{current}volume='if({expr},0,1)':eval=frame[censored]")
            filter_parts.append(
                f"[{tone_idx}:a]asetpts=N/SR/TB,"
                f"volume='if({expr},{BLEEP_LEVEL},0)':eval=frame[tone]")
            filter_parts.append(
                "[censored][tone]amix=inputs=2:duration=first:normalize=0[outa]")
            current = "[outa]"

    return current, ["-c:a", "aac", "-b:a", "256k", "-ar", "48000"]


# -------- Main ---------------------------------------------------------------


def main() -> None:
    ap = argparse.ArgumentParser(description="Render a video from an EDL")
    ap.add_argument("edl", type=Path, help="Path to edl.json")
    ap.add_argument("-o", "--output", type=Path, required=True, help="Output video path")
    ap.add_argument(
        "--preview",
        action="store_true",
        help="Preview mode: 1080p, medium, CRF 22 — evaluable for QC, faster than final.",
    )
    ap.add_argument(
        "--draft",
        action="store_true",
        help="Draft mode: 720p, ultrafast, CRF 28 — cut-point verification only.",
    )
    ap.add_argument(
        "--build-subtitles",
        action="store_true",
        help="Build master.srt from transcripts + EDL offsets before compositing",
    )
    ap.add_argument(
        "--no-subtitles",
        action="store_true",
        help="Skip subtitles even if the EDL references one",
    )
    ap.add_argument(
        "--no-loudnorm",
        action="store_true",
        help="Skip audio loudness normalization. Default is on (-14 LUFS, -1 dBTP, LRA 11).",
    )
    ap.add_argument(
        "--reuse-clips",
        action="store_true",
        help="Reuse already-extracted segment and B-roll clips instead of "
             "re-encoding them. Only safe when the EDL's ranges and broll are "
             "unchanged since the last run -- compositing-only changes "
             "(captions, bleeps, overlays) qualify.",
    )
    ap.add_argument(
        "--no-broll",
        action="store_true",
        help="Skip B-roll cutaways even if the EDL defines them (checks the A-roll cut).",
    )
    args = ap.parse_args()

    edl_path = args.edl.resolve()
    if not edl_path.exists():
        sys.exit(f"edl not found: {edl_path}")

    edl = json.loads(edl_path.read_text())
    edit_dir = edl_path.parent
    out_path = args.output.resolve()

    # 1. Extract per-segment (auto-grade per range if EDL grade is "auto")
    clips_dir = edit_dir / (
        "clips_draft" if args.draft else ("clips_preview" if args.preview else "clips_graded")
    )
    if args.reuse_clips and clips_dir.is_dir():
        segment_paths = sorted(clips_dir.glob("seg_*.mp4"))
        if len(segment_paths) == len(edl["ranges"]):
            print(f"reusing {len(segment_paths)} extracted segment(s) from {clips_dir.name}/")
        else:
            print(f"--reuse-clips: found {len(segment_paths)} clips for "
                  f"{len(edl['ranges'])} ranges -- re-extracting")
            segment_paths = extract_all_segments(
                edl, edit_dir, preview=args.preview, draft=args.draft)
    else:
        segment_paths = extract_all_segments(
            edl, edit_dir, preview=args.preview, draft=args.draft)

    # 2. Concat → base
    if args.draft:
        base_name = "base_draft.mp4"
    elif args.preview:
        base_name = "base_preview.mp4"
    else:
        base_name = "base.mp4"
    base_path = edit_dir / base_name
    concat_segments(segment_paths, base_path, edit_dir)

    # 2b. Translate every output-time feature onto the frame-quantized
    # timeline the segments actually occupy. Skipping this is a 300ms drift
    # by the end of a 17-cut film, and a censor bleep misses its word.
    nominal_offs, real_offs, real_durs = frame_quantized_offsets(edl)
    for coll in ("broll", "overlays", "bleeps"):
        for item in edl.get(coll) or []:
            item["start_in_output"] = round(
                remap_output_time(float(item["start_in_output"]),
                                  nominal_offs, real_offs), 4)

    # 3. Subtitles: build if requested, resolve final path
    subs_path: Path | None = None
    if not args.no_subtitles:
        if args.build_subtitles:
            subs_path = edit_dir / "master.srt"
            if build_master_srt(edl, edit_dir, subs_path, real_durs) == 0:
                print("  0 cues built — rendering without captions")
                subs_path = None
        elif edl.get("subtitles"):
            subs_path = resolve_path(edl["subtitles"], edit_dir)
            if not subs_path.exists():
                print(f"warning: subtitles path in EDL does not exist: {subs_path}")
                subs_path = None

    # 4. Prepare B-roll cutaways against the base's actual dimensions
    overlays = edl.get("overlays") or []
    broll: list[dict] = []
    if edl.get("broll") and not args.no_broll:
        base_w, base_h = probe_dimensions(base_path)
        broll = prepare_broll(edl["broll"], edit_dir, base_w, base_h,
                              preview=args.preview, draft=args.draft)

    # 5. Composite (B-roll + overlays + subtitles LAST) → pre-loudnorm path
    bleeps = edl.get("bleeps") or []
    total = sum(real_durs)
    if args.no_loudnorm:
        build_final_composite(base_path, overlays, subs_path, out_path, edit_dir,
                              broll, bleeps, total)
    else:
        tmp_composite = out_path.with_suffix(".prenorm.mp4")
        build_final_composite(base_path, overlays, subs_path, tmp_composite,
                              edit_dir, broll, bleeps, total)
        print("loudness normalization → social-ready (-14 LUFS / -1 dBTP / LRA 11)")
        apply_loudnorm_two_pass(tmp_composite, out_path, preview=args.draft)
        tmp_composite.unlink(missing_ok=True)

    size_mb = out_path.stat().st_size / (1024 * 1024)
    print(f"\ndone: {out_path} ({size_mb:.1f} MB)")


if __name__ == "__main__":
    main()
