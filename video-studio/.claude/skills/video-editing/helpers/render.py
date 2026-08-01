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
SUB_FORCE_STYLE = (
    "FontName=Helvetica,FontSize=18,Bold=1,"
    "PrimaryColour=&H00FFFFFF,OutlineColour=&H00000000,BackColour=&H00000000,"
    "BorderStyle=1,Outline=2,Shadow=0,"
    "Alignment=2,MarginV=90"
)

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


def extract_segment(
    source: Path,
    seg_start: float,
    duration: float,
    grade_filter: str,
    out_path: Path,
    preview: bool = False,
    draft: bool = False,
) -> None:
    """Extract a cut range as its own MP4 with grade + 30ms audio fades baked in.

    `-ss` before `-i` for fast accurate seeking. Scale to 1080p from 4K.
    Portrait sources (height > width) are scaled by height to preserve orientation.

    Quality ladder:
      - final (default): 1080p libx264 fast CRF 20
      - preview:         1080p libx264 medium CRF 22 (evaluable for QC)
      - draft:           720p libx264 ultrafast CRF 28 (cut-point check only)
    """
    out_path.parent.mkdir(parents=True, exist_ok=True)

    portrait = is_portrait_source(source)
    if draft:
        scale = "scale=-2:1280" if portrait else "scale=1280:-2"
    else:
        scale = "scale=-2:1920" if portrait else "scale=1920:-2"

    vf_parts: list[str] = []
    if is_hdr_source(source):
        vf_parts.append(TONEMAP_CHAIN)
    vf_parts.append(scale)
    if grade_filter:
        vf_parts.append(grade_filter)
    vf = ",".join(vf_parts)

    # 30ms audio fades at both edges (Rule 3) — prevent pops
    fade_out_start = max(0.0, duration - 0.03)
    af = f"afade=t=in:st=0:d=0.03,afade=t=out:st={fade_out_start:.3f}:d=0.03"

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
        "-t", f"{duration:.3f}",
        "-vf", vf,
        "-af", af,
        "-c:v", "libx264", "-preset", preset, "-crf", crf,
        "-pix_fmt", "yuv420p", "-r", "24",
        "-c:a", "aac", "-b:a", "192k", "-ar", "48000",
        "-movflags", "+faststart",
        str(out_path),
    ]
    subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)


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
        extract_segment(src_path, start, duration, seg_filter, out_path, preview=preview, draft=draft)
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


def build_master_srt(edl: dict, edit_dir: Path, out_path: Path) -> None:
    """Build an output-timeline SRT from per-source transcripts.

    - 2-word chunks (break on any punctuation in between)
    - UPPERCASE text
    - Output times computed as word.start - segment_start + segment_offset
    """
    transcripts_dir = edit_dir / "transcripts"
    sources = edl["sources"]

    entries: list[tuple[float, float, str]] = []
    seg_offset = 0.0

    for r in edl["ranges"]:
        src_name = r["source"]
        seg_start = float(r["start"])
        seg_end = float(r["end"])
        seg_duration = seg_end - seg_start

        tr_path = transcripts_dir / f"{src_name}.json"
        if not tr_path.exists():
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
) -> None:
    """Final pass: base -> B-roll -> overlays -> subtitles LAST -> out.

    The layer order is not arbitrary. B-roll replaces the picture, so it goes
    down first; a lower-third or callout has to sit ON the cutaway, not under
    it; and subtitles go last because anything composited after them would
    hide them (Rule 1). Get this order wrong and the failure is silent -- the
    render succeeds and the captions are simply gone.
    """
    broll = broll or []
    has_subs = subtitles_path is not None and subtitles_path.exists()

    if not broll and not overlays and not has_subs:
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

    # --- Layer 2: animation overlays, on top of any cutaway ---
    for i, ov in enumerate(overlays):
        idx += 1
        t, dur = float(ov["start_in_output"]), float(ov["duration"])
        end = t + dur
        chain = f"setpts=PTS-STARTPTS+{t}/TB"
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
        filter_parts.append(
            f"{current}subtitles='{subs_abs}':force_style='{SUB_FORCE_STYLE}'[outv]")
        out_label = "[outv]"
    elif current != "[0:v]":
        filter_parts.append(f"{current}null[outv]")
        out_label = "[outv]"
    else:
        out_label = "[0:v]"

    # --- Audio: mix in B-roll natural sound where asked ---
    audio_label, audio_codec = _build_broll_audio(broll, filter_parts)

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
          f"subtitles: {'yes' if has_subs else 'no'}")
    subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)


# How far the narration drops under a B-roll insert's natural sound. -10 dB is
# about a third of the level: the sizzle reads clearly and the voice still wins.
DEFAULT_DUCK_DB = -10.0


def _build_broll_audio(broll: list[dict], filter_parts: list[str]) -> tuple[str, list[str]]:
    """Return (audio_map_label, codec_args) for the composite command.

    With no B-roll audio there is nothing to do and the base track is copied
    through untouched -- no re-encode, no quality loss. Otherwise the base is
    ducked during each insert and the inserts are mixed in on top.
    """
    voiced = [b for b in broll if b.get("audio") in ("duck", "full")]
    if not voiced:
        return "0:a", ["-c:a", "copy"]

    # Duck (or fully mute) the base under each insert. Chained `volume` filters
    # with `enable` windows only act inside their own window.
    base_chain: list[str] = []
    for b in voiced:
        t, end = float(b["start_in_output"]), float(b["start_in_output"]) + float(b["duration"])
        if b["audio"] == "full":
            gain = 0.0
        else:
            gain = 10 ** (float(b.get("duck_db", DEFAULT_DUCK_DB)) / 20.0)
        base_chain.append(f"volume=enable='between(t,{t:.3f},{end:.3f})':volume={gain:.4f}")
    filter_parts.append(f"[0:a]{','.join(base_chain)}[baseduck]")

    mix_labels = ["[baseduck]"]
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

    # normalize=0 is essential: amix's default divides every input by the input
    # count, which would silently drop the narration by 6 dB per cutaway.
    filter_parts.append(
        f"{''.join(mix_labels)}amix=inputs={len(mix_labels)}:duration=first:"
        f"dropout_transition=0:normalize=0[outa]"
    )
    return "[outa]", ["-c:a", "aac", "-b:a", "256k", "-ar", "48000"]


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
    segment_paths = extract_all_segments(
        edl, edit_dir, preview=args.preview, draft=args.draft
    )

    # 2. Concat → base
    if args.draft:
        base_name = "base_draft.mp4"
    elif args.preview:
        base_name = "base_preview.mp4"
    else:
        base_name = "base.mp4"
    base_path = edit_dir / base_name
    concat_segments(segment_paths, base_path, edit_dir)

    # 3. Subtitles: build if requested, resolve final path
    subs_path: Path | None = None
    if not args.no_subtitles:
        if args.build_subtitles:
            subs_path = edit_dir / "master.srt"
            build_master_srt(edl, edit_dir, subs_path)
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
    if args.no_loudnorm:
        build_final_composite(base_path, overlays, subs_path, out_path, edit_dir, broll)
    else:
        tmp_composite = out_path.with_suffix(".prenorm.mp4")
        build_final_composite(base_path, overlays, subs_path, tmp_composite,
                              edit_dir, broll)
        print("loudness normalization → social-ready (-14 LUFS / -1 dBTP / LRA 11)")
        apply_loudnorm_two_pass(tmp_composite, out_path, preview=args.draft)
        tmp_composite.unlink(missing_ok=True)

    size_mb = out_path.stat().st_size / (1024 * 1024)
    print(f"\ndone: {out_path} ({size_mb:.1f} MB)")


if __name__ == "__main__":
    main()
