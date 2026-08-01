"""Inventory a folder of raw footage before touching anything else.

This is step one of every edit. It answers the questions that decide how the
rest of the session goes: what is A-roll, what is B-roll, which files carry
usable sound, and which ones have a property that will quietly ruin the render
if nobody notices it now.

The four that actually bite, in the order they cost you time:

  Variable frame rate. Phones record VFR. Cut it on a fixed-rate timeline
  without conforming and audio drifts away from picture over the length of a
  long clip -- and it looks fine for the first thirty seconds.

  HDR. iPhone shoots HLG by default. Downconvert without tone mapping and the
  upload is blown out, while QuickTime on your own machine shows it correctly,
  so you ship it without seeing the problem.

  Rotation metadata. A clip that plays upright in the Finder can be stored
  sideways with a rotation flag. Filters that run before the flag is applied
  see the sideways frame.

  Silent or near-silent audio. A camera whose mic was off cannot be synced by
  sound, and you want to know that before planning a dual-system workflow
  around it.

Usage:
    python helpers/ingest.py <footage_dir>
    python helpers/ingest.py <footage_dir> --edit-dir <edit>
    python helpers/ingest.py <footage_dir> --no-audio-scan   # faster
    python helpers/ingest.py <footage_dir> --json
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
from dataclasses import dataclass, asdict, field
from pathlib import Path

VIDEO_EXTS = {".mp4", ".mov", ".mkv", ".avi", ".m4v", ".mts", ".m2ts", ".webm", ".mpeg"}
AUDIO_EXTS = {".wav", ".aiff", ".aif", ".flac", ".mp3", ".m4a", ".aac", ".ogg", ".opus"}
HDR_TRANSFERS = {"smpte2084", "arib-std-b67"}

# Below this mean level the track is effectively silence: room tone, a mic that
# was off, or a dead channel. Not syncable, not usable.
SILENT_DBFS = -50.0
# Loudness scan window. Enough to characterise a track without decoding a
# 40-minute file end to end.
AUDIO_SCAN_S = 90.0


@dataclass
class MediaInfo:
    path: str
    name: str
    kind: str                      # "video" | "audio"
    size_mb: float
    duration_s: float
    # video
    width: int = 0
    height: int = 0
    fps: float = 0.0
    avg_fps: float = 0.0
    vfr: bool = False
    codec: str = ""
    pix_fmt: str = ""
    hdr: bool = False
    rotation: int = 0
    # audio
    has_audio: bool = False
    audio_codec: str = ""
    channels: int = 0
    sample_rate: int = 0
    mean_dbfs: float | None = None
    max_dbfs: float | None = None
    # derived
    role: str = ""                 # "a_roll" | "b_roll" | "audio" | "unknown"
    notes: list[str] = field(default_factory=list)

    @property
    def orientation(self) -> str:
        if not self.width:
            return "-"
        w, h = (self.height, self.width) if self.rotation in (90, 270) else (self.width, self.height)
        return "portrait" if h > w else "landscape"

    @property
    def display_res(self) -> str:
        if not self.width:
            return "-"
        w, h = (self.height, self.width) if self.rotation in (90, 270) else (self.width, self.height)
        return f"{w}x{h}"


def ffprobe_json(path: Path) -> dict:
    out = subprocess.run(
        ["ffprobe", "-v", "error", "-print_format", "json",
         "-show_format", "-show_streams", str(path)],
        capture_output=True, text=True,
    )
    if out.returncode != 0:
        return {}
    try:
        return json.loads(out.stdout)
    except json.JSONDecodeError:
        return {}


def parse_rate(value: str | None) -> float:
    if not value or "/" not in value:
        try:
            return float(value) if value else 0.0
        except ValueError:
            return 0.0
    num, den = value.split("/")
    try:
        d = float(den)
        return float(num) / d if d else 0.0
    except ValueError:
        return 0.0


def stream_rotation(stream: dict) -> int:
    """Rotation from either the display matrix or the legacy tag."""
    for sd in stream.get("side_data_list", []) or []:
        if "rotation" in sd:
            try:
                return int(round(float(sd["rotation"]))) % 360
            except (TypeError, ValueError):
                pass
    tag = (stream.get("tags") or {}).get("rotate")
    if tag:
        try:
            return int(float(tag)) % 360
        except ValueError:
            pass
    return 0


def measure_audio(path: Path) -> tuple[float | None, float | None]:
    """Mean and peak level in dBFS over the first AUDIO_SCAN_S."""
    out = subprocess.run(
        ["ffmpeg", "-v", "info", "-nostdin", "-t", str(AUDIO_SCAN_S),
         "-i", str(path), "-af", "volumedetect", "-vn", "-f", "null", "-"],
        capture_output=True, text=True,
    )
    mean = re.search(r"mean_volume:\s*(-?[\d.]+) dB", out.stderr)
    peak = re.search(r"max_volume:\s*(-?[\d.]+) dB", out.stderr)
    return (float(mean.group(1)) if mean else None,
            float(peak.group(1)) if peak else None)


def inspect(path: Path, scan_audio: bool = True) -> MediaInfo | None:
    probe = ffprobe_json(path)
    if not probe:
        return None
    fmt = probe.get("format", {})
    streams = probe.get("streams", [])
    v = next((s for s in streams if s.get("codec_type") == "video"), None)
    a = next((s for s in streams if s.get("codec_type") == "audio"), None)

    # A cover-art JPEG inside an audio file shows up as a video stream.
    if v is not None and v.get("disposition", {}).get("attached_pic"):
        v = None

    info = MediaInfo(
        path=str(path), name=path.name,
        kind="video" if v is not None else "audio",
        size_mb=round(path.stat().st_size / (1024 * 1024), 1),
        duration_s=round(float(fmt.get("duration", 0) or 0), 2),
    )

    if v is not None:
        info.width = int(v.get("width", 0) or 0)
        info.height = int(v.get("height", 0) or 0)
        info.fps = round(parse_rate(v.get("r_frame_rate")), 3)
        info.avg_fps = round(parse_rate(v.get("avg_frame_rate")), 3)
        info.codec = v.get("codec_name", "")
        info.pix_fmt = v.get("pix_fmt", "")
        info.hdr = v.get("color_transfer") in HDR_TRANSFERS
        info.rotation = stream_rotation(v)
        # r_frame_rate is the container's nominal rate; avg_frame_rate is what
        # was actually delivered. A meaningful gap means variable frame rate.
        if info.fps and info.avg_fps and abs(info.fps - info.avg_fps) / info.fps > 0.02:
            info.vfr = True

    if a is not None:
        info.has_audio = True
        info.audio_codec = a.get("codec_name", "")
        info.channels = int(a.get("channels", 0) or 0)
        info.sample_rate = int(a.get("sample_rate", 0) or 0)
        if scan_audio:
            info.mean_dbfs, info.max_dbfs = measure_audio(path)

    classify(info)
    return info


def classify(info: MediaInfo) -> None:
    """Guess the role and record anything that needs a decision."""
    if info.kind == "audio":
        info.role = "audio"
    elif not info.has_audio:
        info.role = "b_roll"
        info.notes.append("no audio track: B-roll, or needs flash sync")
    elif info.mean_dbfs is not None and info.mean_dbfs < SILENT_DBFS:
        info.role = "b_roll"
        info.notes.append(f"audio effectively silent ({info.mean_dbfs:.0f} dBFS): "
                          f"cannot be synced by sound")
    else:
        # A short clip with sound is far more often a cutaway than a piece of
        # to-camera delivery. Flagged, not decided -- the transcript settles it.
        info.role = "b_roll" if info.duration_s < 12 else "a_roll"

    if info.vfr:
        info.notes.append(f"variable frame rate ({info.fps:g} nominal vs "
                          f"{info.avg_fps:g} actual): conform before cutting")
    if info.hdr:
        info.notes.append("HDR source: will be tone-mapped to Rec.709")
    if info.rotation:
        info.notes.append(f"rotation flag {info.rotation}deg")
    if info.has_audio and info.channels == 1:
        info.notes.append("mono audio")
    if info.duration_s and info.duration_s < 2.0:
        info.notes.append("very short clip")


def scan(root: Path, scan_audio: bool = True) -> list[MediaInfo]:
    files = sorted(p for p in root.rglob("*") if p.is_file()
                   and p.suffix.lower() in (VIDEO_EXTS | AUDIO_EXTS))
    if not files:
        raise SystemExit(f"no media files under {root}")
    print(f"inspecting {len(files)} file(s) under {root}"
          f"{'' if scan_audio else ' (skipping audio scan)'}\n")
    out: list[MediaInfo] = []
    for p in files:
        info = inspect(p, scan_audio)
        if info is None:
            print(f"  {p.name}: ffprobe could not read this file -- skipping")
            continue
        out.append(info)
    return out


def report(items: list[MediaInfo]) -> None:
    by_role: dict[str, list[MediaInfo]] = {}
    for i in items:
        by_role.setdefault(i.role, []).append(i)

    for role in ("a_roll", "b_roll", "audio", "unknown"):
        group = by_role.get(role)
        if not group:
            continue
        total = sum(i.duration_s for i in group)
        print(f"\n{role.upper().replace('_', '-')}  "
              f"({len(group)} file(s), {total / 60:.1f} min)")
        print(f"  {'file':<30} {'dur':>8} {'res':>11} {'fps':>7} {'audio':>18}")
        for i in sorted(group, key=lambda x: x.name):
            aud = "-"
            if i.has_audio:
                lvl = f"{i.mean_dbfs:.0f}dB" if i.mean_dbfs is not None else "?"
                aud = f"{i.audio_codec} {i.channels}ch {lvl}"
            name = i.name if len(i.name) <= 30 else i.name[:27] + "..."
            print(f"  {name:<30} {i.duration_s:>7.1f}s {i.display_res:>11} "
                  f"{i.fps:>7.2f} {aud:>18}")
            for note in i.notes:
                print(f"      - {note}")

    # Anything that has to be reconciled across the whole set, rather than
    # per file, gets called out separately.
    videos = [i for i in items if i.kind == "video"]
    print("\n" + "=" * 62)
    total_min = sum(i.duration_s for i in items) / 60
    total_gb = sum(i.size_mb for i in items) / 1024
    print(f"{len(items)} files, {total_min:.1f} min, {total_gb:.2f} GB")

    warnings: list[str] = []
    rates = {round(i.avg_fps or i.fps, 2) for i in videos if i.fps}
    if len(rates) > 1:
        warnings.append(f"mixed frame rates {sorted(rates)}: the render conforms "
                        f"everything to 24 fps, which is fine, but motion from the "
                        f"higher-rate clips will be resampled")
    orients = {i.orientation for i in videos}
    if len(orients) > 1:
        warnings.append(f"mixed orientations {sorted(orients)}: vertical clips are "
                        f"scaled to cover and cropped, so frame the important part "
                        f"centrally or expect to lose the edges")
    if any(i.vfr for i in videos):
        warnings.append("variable frame rate present: conform those clips first")
    if not any(i.role == "audio" for i in items):
        warnings.append("no separate audio files: camera sound is all there is, so "
                        "there is nothing to dual-system sync")
    if not any(i.role == "a_roll" for i in items):
        warnings.append("nothing classified as A-roll: no clip both has real audio "
                        "and runs over 12s, so there may be no spine to cut against")

    if warnings:
        print("\nneeds a decision:")
        for w in warnings:
            print(f"  - {w}")
    print()


def main() -> None:
    ap = argparse.ArgumentParser(description="Inventory raw footage.")
    ap.add_argument("footage", type=Path, help="Directory of source media")
    ap.add_argument("--edit-dir", type=Path,
                    help="Where to write inventory.json (default: <footage>/../edit)")
    ap.add_argument("--no-audio-scan", action="store_true",
                    help="Skip loudness measurement; much faster, but silent "
                         "tracks will not be detected")
    ap.add_argument("--json", action="store_true", help="Print the full JSON")
    args = ap.parse_args()

    root = args.footage.resolve()
    if not root.is_dir():
        raise SystemExit(f"not a directory: {root}")

    items = scan(root, scan_audio=not args.no_audio_scan)
    report(items)

    edit_dir = (args.edit_dir or root.parent / "edit").resolve()
    edit_dir.mkdir(parents=True, exist_ok=True)
    out = edit_dir / "inventory.json"
    out.write_text(json.dumps([asdict(i) for i in items], indent=2))
    print(f"inventory -> {out}")
    if args.json:
        print(json.dumps([asdict(i) for i in items], indent=2))


if __name__ == "__main__":
    main()
