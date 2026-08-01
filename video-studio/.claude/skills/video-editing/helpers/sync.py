"""Align separately-recorded audio and multiple cameras onto one timeline.

Three jobs, one tool:

  dual-system   one camera + one external recorder (lav, shotgun, wireless).
                Finds the offset and muxes the good audio onto the video.
  multicam      N sources (A-cam, B-cam, phone, recorder) aligned to a shared
                master timeline, with the common overlap window computed.
  flash         fallback for sources whose audio is unusable (no mic, wind,
                a silent B-cam). Syncs on a sharp brightness change instead.

Convention used everywhere in this file:

    master_time = source_time + offset

`offset` is the master-timeline position of a source's first frame/sample.

    offset > 0  ->  this source started AFTER master zero; pad its head
    offset < 0  ->  this source started BEFORE master zero; trim its head

For the dual-system case master zero is the camera, so the camera's offset is
0 and the recorder's offset says how to move the audio.

How the audio matching works
----------------------------
1. Decode everything to mono 8 kHz PCM. A scratch mic and a good mic sound very
   different in timbre, but their *loudness over time* tracks the same room.
2. Correlate z-scored 10 ms RMS envelopes with an FFT. This survives the timbre
   mismatch and gives an offset good to ~10 ms.
3. Refine against the raw 8 kHz waveforms inside a +/-120 ms window around the
   coarse peak, landing the offset near 0.2 ms -- far tighter than the ~41 ms
   of a single 24 fps frame.
4. Re-measure in short windows spread across the file. If the residual walks
   between them, the two devices' clocks run at different rates and the audio
   needs resampling, not just shifting.

Knowing the offset leaves an editorial choice about what to actually write:

  conform one to another   `--mux`. The video is untouched and the audio is
                           padded or trimmed to match it exactly. This is what
                           you want for dual-system dialogue.
  crop to the common part  `--multicam --trim`. Every source is cut down to
                           the window where all of them are rolling, so they
                           can be treated as one synchronized set. Tail
                           material outside the window is discarded.
  pad everything           Keep every frame of every source by padding the
                           heads instead of cutting them. Nothing is lost but
                           the files carry dead air. `sync_map.json` records
                           the offsets needed to do this in an NLE.

Usage:
    # dual-system
    python helpers/sync.py <video> <audio>                # measure and report
    python helpers/sync.py <video> <audio> --mux          # write synced MP4
    python helpers/sync.py <video> <audio> --mux --keep-camera-audio
    python helpers/sync.py --scan <dir> --mux             # pair a whole shoot

    # multicam / mixed shoot -> edit/sync_map.json
    python helpers/sync.py --multicam <dir>
    python helpers/sync.py --multicam <dir> --trim        # write aligned copies
    python helpers/sync.py --multicam <dir> --method flash
    python helpers/sync.py --multicam <dir> --plot        # visual confirmation
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
from dataclasses import dataclass, asdict, field
from datetime import datetime
from pathlib import Path

import numpy as np

# 8 kHz keeps speech energy (and plenty of transient detail for the refine
# pass) while making full-length correlation cheap: an hour is 29M samples.
SR = 8000
HOP = 80                  # 10 ms envelope resolution
REFINE_WINDOW_S = 0.120   # search +/-120 ms around the coarse peak
REFINE_CHUNK_S = 24.0     # how much raw audio to use for the refine pass
PROBE_LEN_S = 30.0        # drift-probe window; short enough that drift inside
                          # one window does not smear the correlation peak
N_PROBES = 5
MIN_OVERLAP_S = 15.0      # lags with less overlap than this are not considered
MAX_SHIFT_S = 0.0         # 0 = search every lag; set it when you know roughly
                          # how far apart the devices started rolling
EXPECT_TOLERANCE_S = 30.0 # how far the search may stray from a filename-implied
                          # offset, to absorb clock skew between devices
TRUST_QUALITY = 6.0       # peak-to-sidelobe ratio below which we do not mux
DRIFT_PPM_FLOOR = 50.0    # below this, a static offset is good enough

VIDEO_EXTS = {".mp4", ".mov", ".mkv", ".avi", ".m4v", ".mts", ".m2ts", ".webm", ".mpeg"}
AUDIO_EXTS = {".wav", ".aiff", ".aif", ".flac", ".mp3", ".m4a", ".aac", ".ogg", ".opus"}


# -------- Probing and decoding ----------------------------------------------


def duration_of(path: Path) -> float:
    out = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration",
         "-of", "default=noprint_wrappers=1:nokey=1", str(path)],
        capture_output=True, text=True, check=True,
    )
    try:
        return float(out.stdout.strip())
    except ValueError:
        return 0.0


def has_audio_stream(path: Path) -> bool:
    out = subprocess.run(
        ["ffprobe", "-v", "error", "-select_streams", "a:0",
         "-show_entries", "stream=codec_type",
         "-of", "default=noprint_wrappers=1:nokey=1", str(path)],
        capture_output=True, text=True,
    )
    return out.stdout.strip() == "audio"


def frame_rate_of(path: Path) -> float:
    out = subprocess.run(
        ["ffprobe", "-v", "error", "-select_streams", "v:0",
         "-show_entries", "stream=r_frame_rate",
         "-of", "default=noprint_wrappers=1:nokey=1", str(path)],
        capture_output=True, text=True,
    )
    try:
        num, den = out.stdout.strip().split("/")
        return float(num) / float(den)
    except Exception:
        return 0.0


def filename_timestamp(path: Path) -> datetime | None:
    """Wall-clock start time encoded in a filename, if there is one.

    DJI cameras and DJI wireless mics both stamp the recording start into the
    name, which is a free, independent check on the correlation result:

        DJI_20260801120655_0071_D.MP4          -> 2026-08-01 12:06:55
        TX00_MIC001_20260801_120634_orig.wav   -> 2026-08-01 12:06:34

    Phones generally do not -- an iPhone's MOV `creation_time` is rewritten
    when the file is copied, so it reports the transfer time, not the take.
    Never trust it for sync.
    """
    m = re.search(r"(20\d{6})[_-]?(\d{6})", path.name)
    if not m:
        return None
    try:
        return datetime.strptime(m.group(1) + m.group(2), "%Y%m%d%H%M%S")
    except ValueError:
        return None


def expected_offset(video: Path, audio: Path) -> float | None:
    """Offset implied by the two filenames, or None if either lacks a stamp."""
    tv, ta = filename_timestamp(video), filename_timestamp(audio)
    if tv is None or ta is None:
        return None
    return -(tv - ta).total_seconds()


def decode_mono(path: Path, start: float = 0.0, duration: float | None = None) -> np.ndarray:
    """Decode a slice of any media file to a mono float32 array at SR."""
    cmd = ["ffmpeg", "-v", "error", "-nostdin"]
    if start > 0:
        cmd += ["-ss", f"{start:.3f}"]
    cmd += ["-i", str(path)]
    if duration is not None:
        cmd += ["-t", f"{duration:.3f}"]
    cmd += ["-vn", "-ac", "1", "-ar", str(SR), "-f", "f32le", "-"]

    proc = subprocess.run(cmd, capture_output=True, check=True)
    return np.frombuffer(proc.stdout, dtype=np.float32).copy()


# -------- Correlation --------------------------------------------------------


def envelope(x: np.ndarray) -> np.ndarray:
    """Per-hop RMS in the log domain, z-scored.

    Two microphones in the same room produce very different waveforms but
    near-identical loudness contours, so the envelope is the signal that
    survives a timbre mismatch. The log compresses dynamic range so one loud
    transient -- a door slam, a plate hitting a table -- cannot dominate.
    Z-scoring puts every source on the same scale, which is what makes quality
    numbers comparable between pairs when matching N sources.
    """
    n = len(x) // HOP
    if n == 0:
        return np.zeros(0, dtype=np.float32)
    frames = x[: n * HOP].reshape(n, HOP).astype(np.float64)
    env = np.log1p(np.sqrt((frames ** 2).mean(axis=1)) * 1000.0)
    env -= env.mean()
    std = env.std()
    if std > 0:
        env /= std
    return env.astype(np.float32)


def _xcorr(a: np.ndarray, b: np.ndarray) -> tuple[np.ndarray, int]:
    """Linear cross-correlation of a against b, via FFT.

    Returns (corr, zero_index) where corr[i] corresponds to lag m = i - zero,
    and corr[i] = sum_n a[n] * b[n - m]. A peak at lag m means b lines up with
    a when b is shifted LATER by m samples.
    """
    la, lb = len(a), len(b)
    n = la + lb - 1
    nfft = 1 << (n - 1).bit_length()
    corr = np.fft.irfft(np.fft.rfft(a, nfft) * np.conj(np.fft.rfft(b, nfft)), nfft)
    corr = np.concatenate([corr[-(lb - 1):], corr[:la]]) if lb > 1 else corr[:la]
    return corr, lb - 1


def _normalize_by_overlap(corr: np.ndarray, zero: int, la: int, lb: int,
                          min_overlap: int, max_shift: int = 0,
                          lag_window: tuple[int, int] | None = None) -> np.ndarray:
    """Divide out the overlap taper, then mask lags we refuse to consider.

    A zero-padded FFT correlation sums only over the region where the two
    signals actually overlap, so lags near the edges have fewer terms and are
    systematically smaller. Without this, a long video correlated against a
    short audio file always peaks near zero lag regardless of the truth.

    Two masks then narrow the field. `min_overlap` throws out lags backed by so
    little common audio that the score is noise. `max_shift` (0 = unbounded) is
    the caller asserting the two devices started within that many samples of
    each other -- worth setting whenever you know it, because repetitive
    material (music, a phrase said twice, a looping kitchen hum) can otherwise
    produce a false peak that outscores the true one.
    """
    lags = np.arange(len(corr)) - zero
    counts = np.minimum(la, lb + lags) - np.maximum(0, lags)
    out = np.zeros_like(corr)
    ok = counts >= max(min_overlap, 1)
    if max_shift > 0:
        ok &= np.abs(lags) <= max_shift
    if lag_window is not None:
        ok &= (lags >= lag_window[0]) & (lags <= lag_window[1])
    out[ok] = corr[ok] / np.sqrt(counts[ok])
    return out


def _peak_quality(corr: np.ndarray, peak_idx: int, guard: int) -> float:
    """Peak-to-sidelobe ratio: how far the winner stands above the noise floor.

    A clean, unambiguous alignment scores well above 10. Below ~4 the match is
    guesswork -- usually because the two recordings do not overlap at all, or
    one of them is effectively silent.
    """
    masked = corr.copy()
    masked[max(0, peak_idx - guard) : peak_idx + guard + 1] = 0.0
    floor = float(np.abs(masked).std())
    if floor <= 0:
        return float("inf")
    return float(abs(corr[peak_idx]) / floor)


def _parabolic_vertex(y_prev: float, y_peak: float, y_next: float) -> float:
    """Sub-sample peak position from three points, in samples off the center."""
    denom = y_prev - 2.0 * y_peak + y_next
    if denom == 0:
        return 0.0
    return float(np.clip(0.5 * (y_prev - y_next) / denom, -0.5, 0.5))


def measure_offset(ref_pcm: np.ndarray, other_pcm: np.ndarray,
                   expect: float | None = None,
                   tolerance: float = EXPECT_TOLERANCE_S) -> tuple[float, float]:
    """Return (offset_seconds, quality) for two decoded mono signals.

    offset is the position of other_pcm[0] on ref_pcm's timeline, per the
    convention at the top of this file.

    `expect` constrains the search to within `tolerance` of a known coarse
    alignment. On a long recording the correlator has thousands of candidate
    lags to choose between, and a room full of repeated sounds -- a griddle,
    traffic, the same phrase said twice -- can hand a false peak more support
    than the true one. Pinning the search to a window the answer must lie in
    removes that entire failure mode.
    """
    env_r, env_o = envelope(ref_pcm), envelope(other_pcm)
    if len(env_r) < 8 or len(env_o) < 8:
        return 0.0, 0.0

    corr, zero = _xcorr(env_r, env_o)
    min_overlap_hops = int(min(MIN_OVERLAP_S * SR / HOP,
                               0.25 * min(len(env_r), len(env_o))))
    max_shift_hops = int(MAX_SHIFT_S * SR / HOP)
    window = None
    if expect is not None:
        per_hop = SR / HOP
        window = (int((expect - tolerance) * per_hop),
                  int((expect + tolerance) * per_hop))
    corr = _normalize_by_overlap(corr, zero, len(env_r), len(env_o),
                                 min_overlap_hops, max_shift_hops, window)
    if not corr.any():
        return 0.0, 0.0

    peak = int(np.argmax(corr))
    quality = _peak_quality(corr, peak, guard=max(4, len(corr) // 200))
    # corr peaks at the lag by which `other` must move LATER to match `ref`,
    # which is exactly the offset.
    offset = (peak - zero) * HOP / SR

    return offset + _refine(ref_pcm, other_pcm, offset), quality


def _refine(ref_pcm: np.ndarray, other_pcm: np.ndarray, coarse: float) -> float:
    """Sub-hop correction to a coarse offset, from the raw waveforms."""
    shift = int(round(coarse * SR))
    # Slice the region the coarse offset says is common to both.
    if shift >= 0:
        r = ref_pcm[shift:]
        o = other_pcm[: len(r)]
    else:
        o = other_pcm[-shift:]
        r = ref_pcm[: len(o)]
    n = min(len(r), len(o))
    span = int(REFINE_WINDOW_S * SR)
    if n < span * 6:
        return 0.0

    # A middle chunk -- the edges of a slice are the least reliable part.
    chunk = min(n, int(REFINE_CHUNK_S * SR))
    mid = (n - chunk) // 2
    r, o = r[mid : mid + chunk], o[mid : mid + chunk]

    corr, zero = _xcorr(r - r.mean(), o - o.mean())
    lo, hi = max(0, zero - span), min(len(corr), zero + span + 1)
    peak = int(np.argmax(np.abs(corr[lo:hi]))) + lo
    frac = (_parabolic_vertex(abs(corr[peak - 1]), abs(corr[peak]), abs(corr[peak + 1]))
            if 0 < peak < len(corr) - 1 else 0.0)
    residual = (peak - zero + frac) / SR
    # A peak pinned to the edge of the search window means it found nothing.
    if abs(residual) >= REFINE_WINDOW_S * 0.95:
        return 0.0
    return residual


# -------- Brightness / flash sync (audio-free fallback) ----------------------
#
# When a source has no usable audio -- a silent B-cam, a mic ruined by wind,
# a drone -- the alignment has to come from the picture. Clap once in frame or
# flip a light on at the top of the take and every camera records the same
# sharp brightness step; that step is the sync point.
#
# The detector is the product of the first and second derivative of mean frame
# luma: the first derivative is large for any brightening, the second is large
# only for an ABRUPT one, and the product suppresses slow exposure ramps and
# pans across a window that would otherwise trigger it.

FLASH_METRIC_THRESHOLD = 1000.0
FLASH_SEARCH_S = 60.0   # only look near the top of the take


def brightness_series(video: Path, max_seconds: float = FLASH_SEARCH_S
                      ) -> tuple[np.ndarray, np.ndarray]:
    """Return (times, mean_luma) per frame for the first max_seconds.

    Uses ffmpeg's signalstats rather than OpenCV so the only binary dependency
    stays ffmpeg.
    """
    proc = subprocess.run(
        ["ffmpeg", "-v", "error", "-nostdin", "-t", f"{max_seconds:.2f}",
         "-i", str(video),
         "-vf", "scale=160:-2,signalstats,metadata=print:key=lavfi.signalstats.YAVG:file=-",
         "-an", "-f", "null", "-"],
        capture_output=True, text=True, check=True,
    )
    times: list[float] = []
    values: list[float] = []
    pending_t: float | None = None
    for line in proc.stdout.splitlines():
        m = re.match(r"frame:\s*\d+\s+pts:\s*\d+\s+pts_time:\s*([0-9.]+)", line)
        if m:
            pending_t = float(m.group(1))
            continue
        m = re.search(r"lavfi\.signalstats\.YAVG=([0-9.]+)", line)
        if m and pending_t is not None:
            times.append(pending_t)
            values.append(float(m.group(1)))
            pending_t = None
    return np.array(times), np.array(values)


def find_flash(video: Path, threshold: float = FLASH_METRIC_THRESHOLD
               ) -> tuple[float, float]:
    """Return (time_seconds, metric) of the first abrupt brightening."""
    t, y = brightness_series(video)
    if len(t) < 3:
        return 0.0, 0.0
    d1 = np.diff(y, prepend=y[0])
    d2 = np.diff(d1, prepend=d1[0])
    metric = d1 * d2
    hits = np.flatnonzero(metric >= threshold)
    if len(hits):
        i = int(hits[0])
    else:
        # Nothing cleared the bar -- fall back to the sharpest change there was
        # and let the caller judge it by the metric value.
        i = int(np.argmax(metric))
    return float(t[i]), float(metric[i])


# -------- Dual-system pair ---------------------------------------------------


@dataclass
class SyncResult:
    video: str
    audio: str
    offset_s: float
    quality: float
    drift_ppm: float
    drift_ms_per_hour: float
    video_duration_s: float
    audio_duration_s: float
    filename_offset_s: float | None = None
    probes: list[dict] = field(default_factory=list)

    @property
    def filename_delta(self) -> float | None:
        if self.filename_offset_s is None:
            return None
        return self.offset_s - self.filename_offset_s

    @property
    def confident(self) -> bool:
        return self.quality >= TRUST_QUALITY

    @property
    def needs_resample(self) -> bool:
        # 50 ppm over a 20-minute take is ~60 ms of walk-off, about a frame and
        # a half. Below that, a static offset holds for the length of a take.
        return abs(self.drift_ppm) >= DRIFT_PPM_FLOOR


def probe_starts(overlap_s: float) -> list[float]:
    """Probe start times spread across the common region."""
    usable = overlap_s - PROBE_LEN_S
    if usable < 45.0:
        return []
    return [usable * f for f in np.linspace(0.02, 0.98, N_PROBES)]


def measure_drift(video: Path, audio: Path, offset: float,
                  v_dur: float, a_dur: float) -> tuple[float, float, list[dict]]:
    """Re-measure short windows across the take to detect a clock-rate mismatch.

    Returns (drift_ppm, offset_correction, probes). A flat residual means the
    two devices agree on how long a second is; a sloping one means they do not,
    and the audio has to be resampled rather than just shifted.
    """
    probes: list[dict] = []
    common_start, common_end = max(0.0, offset), min(v_dur, a_dur + offset)
    for t in probe_starts(common_end - common_start):
        v_start = common_start + t
        a_start = v_start - offset
        if a_start < 0 or a_start + PROBE_LEN_S > a_dur or v_start + PROBE_LEN_S > v_dur:
            continue
        pv = decode_mono(video, start=v_start, duration=PROBE_LEN_S)
        pa = decode_mono(audio, start=a_start, duration=PROBE_LEN_S)
        if len(pv) < SR * 5 or len(pa) < SR * 5:
            continue
        residual, q = measure_offset(pv, pa, expect=0.0, tolerance=2.0)
        # Regress against the window MIDPOINT: the correlation peak reports the
        # average alignment over the window, not the alignment at its start.
        probes.append({"video_t": round(v_start + PROBE_LEN_S / 2, 2),
                       "residual_s": round(residual, 4),
                       "quality": round(q, 2)})

    good = [p for p in probes if p["quality"] >= 4.0]
    if len(good) < 2:
        return 0.0, 0.0, probes
    xs = np.array([p["video_t"] for p in good], dtype=float)
    ys = np.array([p["residual_s"] for p in good], dtype=float)
    if xs.max() - xs.min() <= 60.0:
        return 0.0, 0.0, probes
    # residual(t) ~= (rate - 1) * t + (true_offset - measured_offset)
    slope, intercept = np.polyfit(xs, ys, 1)
    return float(slope) * 1e6, float(intercept), probes


def sync_pair(video: Path, audio: Path, verbose: bool = True,
              use_filename_times: bool = False,
              expect_offset: float | None = None,
              tolerance: float = EXPECT_TOLERANCE_S) -> SyncResult:
    if not has_audio_stream(video):
        raise SystemExit(
            f"{video.name} has no audio track. Dual-system sync correlates the "
            f"camera's scratch audio against the good mic -- with no scratch "
            f"track there is nothing to match. Use --multicam --method flash "
            f"for picture-based alignment instead."
        )

    v_dur, a_dur = duration_of(video), duration_of(audio)
    if verbose:
        print(f"sync: {video.name} ({v_dur:.1f}s)  <-  {audio.name} ({a_dur:.1f}s)")

    fn_offset = expected_offset(video, audio)
    # An explicit window always wins over the filename-derived one.
    expect = expect_offset
    if expect is None and use_filename_times and fn_offset is not None:
        expect = fn_offset
    if verbose and expect is not None:
        src = "given" if expect_offset is not None else "filename-implied"
        print(f"  searching within {tolerance:g}s of the {src} {expect:+.1f}s")

    offset, quality = measure_offset(decode_mono(video), decode_mono(audio),
                                     expect=expect, tolerance=tolerance)
    if verbose:
        print(f"  offset {offset:+.3f}s   quality {quality:.1f}")

    # Independent cross-check. Two devices that both stamp wall-clock time into
    # their filenames should agree with the correlation to within their clock
    # skew; a large disagreement means one of the two is wrong, and the
    # correlation is the one to distrust when its quality is also marginal.
    if fn_offset is not None:
        delta = offset - fn_offset
        if verbose:
            if abs(delta) <= 2.0:
                print(f"  filenames agree ({fn_offset:+.1f}s, delta {delta:+.2f}s)")
            else:
                print(f"  DISAGREES with filenames: they imply {fn_offset:+.1f}s, "
                      f"correlation says {offset:+.1f}s (delta {delta:+.1f}s). "
                      f"Re-run with --use-filename-times to constrain the search.")

    drift_ppm, correction, probes = measure_drift(video, audio, offset, v_dur, a_dur)
    offset += correction

    if verbose:
        for p in probes:
            print(f"    probe @{p['video_t']:8.1f}s  residual {p['residual_s']:+.4f}s  "
                  f"q={p['quality']:.1f}")
        if abs(drift_ppm) >= 1.0:
            print(f"  clock drift {drift_ppm:+.1f} ppm "
                  f"({drift_ppm * 3.6:+.0f} ms/hour), refined offset {offset:+.3f}s")

    return SyncResult(
        video=str(video), audio=str(audio),
        offset_s=round(offset, 4), quality=round(quality, 2),
        drift_ppm=round(drift_ppm, 2), drift_ms_per_hour=round(drift_ppm * 3.6, 1),
        video_duration_s=round(v_dur, 3), audio_duration_s=round(a_dur, 3),
        filename_offset_s=(round(fn_offset, 3) if fn_offset is not None else None),
        probes=probes,
    )


def mux(result: SyncResult, out_path: Path, keep_camera_audio: bool = False,
        correct_drift: bool = True, verbose: bool = True) -> Path:
    """Write video + shifted external audio to a new file.

    The video stream is copied, not re-encoded: no generation loss and no
    encode time. Only the audio is touched.
    """
    video, audio = Path(result.video), Path(result.audio)
    out_path.parent.mkdir(parents=True, exist_ok=True)

    af: list[str] = []

    # Rate correction goes FIRST -- it rescales the audio's own timeline, and
    # the offset is expressed on the already-rescaled timeline.
    if correct_drift and result.needs_resample:
        tempo = 1.0 / (1.0 + result.drift_ppm / 1e6)
        af.append(f"atempo={tempo:.9f}")
        if verbose:
            print(f"  correcting {result.drift_ppm:+.1f} ppm clock drift "
                  f"(atempo={tempo:.9f})")

    off = result.offset_s
    if off > 0.0005:
        af.append(f"adelay={off * 1000:.1f}:all=1")
    elif off < -0.0005:
        af += [f"atrim=start={-off:.4f}", "asetpts=PTS-STARTPTS"]

    af.append("aresample=48000:first_pts=0")

    cmd = [
        "ffmpeg", "-y", "-v", "error", "-nostdin",
        "-i", str(video), "-i", str(audio),
        "-filter_complex", f"[1:a]{','.join(af)}[good]",
        "-map", "0:v:0", "-map", "[good]",
    ]
    if keep_camera_audio:
        cmd += ["-map", "0:a:0"]
    cmd += ["-c:v", "copy", "-c:a", "aac", "-b:a", "256k", "-ar", "48000",
            "-shortest", "-movflags", "+faststart"]
    if keep_camera_audio:
        cmd += ["-metadata:s:a:0", "title=External (synced)",
                "-metadata:s:a:1", "title=Camera scratch"]
    cmd += [str(out_path)]

    subprocess.run(cmd, check=True)
    if verbose:
        print(f"  muxed -> {out_path}")
    return out_path


def pair_directory(root: Path) -> list[tuple[Path, Path]]:
    """Match every video to its best-correlating audio file.

    Correlates a 3-minute probe from each video against each audio file and
    keeps the best scorer. With a single audio file this just confirms which
    videos it actually covers.
    """
    videos = sorted(p for p in root.iterdir()
                    if p.is_file() and p.suffix.lower() in VIDEO_EXTS)
    audios = sorted(p for p in root.iterdir()
                    if p.is_file() and p.suffix.lower() in AUDIO_EXTS)
    if not videos:
        raise SystemExit(f"no video files in {root}")
    if not audios:
        raise SystemExit(f"no separate audio files in {root} -- nothing to sync")

    print(f"pairing {len(videos)} video(s) against {len(audios)} audio file(s)\n")
    decoded = {a: decode_mono(a) for a in audios}

    pairs: list[tuple[Path, Path]] = []
    for v in videos:
        if not has_audio_stream(v):
            print(f"  {v.name}: no scratch audio, cannot pair")
            continue
        vp = decode_mono(v, start=0.0, duration=180.0)
        best, best_q = None, 0.0
        for a, ap in decoded.items():
            _, q = measure_offset(vp, ap)
            if q > best_q:
                best, best_q = a, q
        if best is not None and best_q >= 4.0:
            print(f"  {v.name}  <-  {best.name}  (q={best_q:.1f})")
            pairs.append((v, best))
        else:
            print(f"  {v.name}: no confident audio match (best q={best_q:.1f})")
    print()
    return pairs


# -------- Multicam: N sources on one master timeline ------------------------


@dataclass
class SourceSync:
    name: str
    path: str
    kind: str            # "video" or "audio"
    offset_s: float      # master-timeline position of this source's t=0
    quality: float
    duration_s: float
    fps: float
    method: str          # "audio" | "flash" | "reference"

    @property
    def master_start(self) -> float:
        return self.offset_s

    @property
    def master_end(self) -> float:
        return self.offset_s + self.duration_s


def sync_multicam(root: Path, method: str = "audio",
                  reference: str | None = None) -> dict:
    """Align every media file in `root` onto one master timeline.

    Everything is correlated against a single reference source, then the whole
    set is shifted so the earliest source sits at master time 0. The common
    window -- the span where every source is rolling -- is reported separately,
    because that is the only region where you can freely cut between angles.
    """
    files = sorted(p for p in root.iterdir() if p.is_file()
                   and p.suffix.lower() in (VIDEO_EXTS | AUDIO_EXTS))
    if len(files) < 2:
        raise SystemExit(f"need at least 2 media files in {root}, found {len(files)}")

    print(f"multicam sync ({method}): {len(files)} source(s) in {root}\n")

    if method == "flash":
        sources = _sync_by_flash(files)
    else:
        sources = _sync_by_audio(files, reference)

    # Shift so the earliest source starts at master 0.
    earliest = min(s.offset_s for s in sources)
    for s in sources:
        s.offset_s = round(s.offset_s - earliest, 4)

    common_start = max(s.master_start for s in sources)
    common_end = min(s.master_end for s in sources)

    print(f"\n{'source':<34} {'offset':>10} {'duration':>10} {'quality':>8}  method")
    for s in sorted(sources, key=lambda s: s.offset_s):
        print(f"{s.name:<34} {s.offset_s:>+9.3f}s {s.duration_s:>9.2f}s "
              f"{s.quality:>8.1f}  {s.method}")

    if common_end <= common_start:
        print("\n  WARNING: the sources do not all overlap -- there is no window "
              "where every angle is rolling. Cut from the ones that do overlap.")
    else:
        print(f"\ncommon window: {common_start:.3f}s -> {common_end:.3f}s "
              f"({common_end - common_start:.2f}s where every source is rolling)")

    return {
        "version": 1,
        "method": method,
        "master_zero": "earliest source start",
        "common_start_s": round(max(0.0, common_start), 4),
        "common_end_s": round(common_end, 4),
        "sources": [asdict(s) for s in sorted(sources, key=lambda s: s.offset_s)],
    }


def _sync_by_audio(files: list[Path], reference: str | None) -> list[SourceSync]:
    usable = [f for f in files
              if f.suffix.lower() in AUDIO_EXTS or has_audio_stream(f)]
    skipped = [f for f in files if f not in usable]
    for f in skipped:
        print(f"  {f.name}: no audio track, cannot align by sound "
              f"(try --method flash)")
    if len(usable) < 2:
        raise SystemExit("need at least 2 sources with audio for audio sync")

    # The reference is the longest source unless one was named: the longest
    # file is the most likely to overlap everything else.
    if reference:
        ref = next((f for f in usable if f.name == reference or f.stem == reference), None)
        if ref is None:
            raise SystemExit(f"reference {reference!r} is not one of the usable sources")
    else:
        ref = max(usable, key=duration_of)
    print(f"  reference: {ref.name}\n")

    ref_pcm = decode_mono(ref)
    sources: list[SourceSync] = []
    for f in usable:
        dur, fps = duration_of(f), frame_rate_of(f)
        kind = "audio" if f.suffix.lower() in AUDIO_EXTS else "video"
        if f == ref:
            sources.append(SourceSync(f.name, str(f), kind, 0.0, float("inf"),
                                      round(dur, 3), round(fps, 4), "reference"))
            continue
        offset, q = measure_offset(ref_pcm, decode_mono(f))
        print(f"  {f.name:<30} offset {offset:+8.3f}s  q={q:.1f}"
              f"{'   LOW CONFIDENCE' if q < TRUST_QUALITY else ''}")
        sources.append(SourceSync(f.name, str(f), kind, round(offset, 4), round(q, 2),
                                  round(dur, 3), round(fps, 4), "audio"))
    return sources


def _sync_by_flash(files: list[Path]) -> list[SourceSync]:
    videos = [f for f in files if f.suffix.lower() in VIDEO_EXTS]
    if len(videos) < 2:
        raise SystemExit("flash sync needs at least 2 video sources")

    flashes: dict[Path, tuple[float, float]] = {}
    for f in videos:
        t, metric = find_flash(f)
        flashes[f] = (t, metric)
        weak = "   WEAK (no clear flash)" if metric < FLASH_METRIC_THRESHOLD else ""
        print(f"  {f.name:<30} flash at {t:7.3f}s  metric={metric:9.0f}{weak}")

    # Line the flashes up: a source whose flash is later in its own timeline
    # started earlier, so its offset is more negative.
    latest = max(t for t, _ in flashes.values())
    sources: list[SourceSync] = []
    for f, (t, metric) in flashes.items():
        sources.append(SourceSync(
            f.name, str(f), "video", round(latest - t, 4),
            round(min(metric / FLASH_METRIC_THRESHOLD, 99.0), 2),
            round(duration_of(f), 3), round(frame_rate_of(f), 4), "flash",
        ))
    return sources


def trim_to_common(sync_map: dict, out_dir: Path) -> list[Path]:
    """Write a copy of every source trimmed to the common window.

    After this every file starts and ends at the same moment, so a plain
    multi-input ffmpeg command can cut between them with no per-clip offset
    arithmetic.
    """
    start, end = sync_map["common_start_s"], sync_map["common_end_s"]
    if end <= start:
        raise SystemExit("no common window -- nothing to trim to")
    out_dir.mkdir(parents=True, exist_ok=True)
    written: list[Path] = []
    print(f"\ntrimming {len(sync_map['sources'])} source(s) to the common window")
    for s in sync_map["sources"]:
        src = Path(s["path"])
        local_start = start - s["offset_s"]
        out = out_dir / f"{src.stem}_aligned{'.wav' if s['kind'] == 'audio' else '.mp4'}"
        cmd = ["ffmpeg", "-y", "-v", "error", "-nostdin",
               "-ss", f"{local_start:.4f}", "-i", str(src),
               "-t", f"{end - start:.4f}"]
        if s["kind"] == "audio":
            cmd += ["-c:a", "pcm_s24le", "-ar", "48000"]
        else:
            # Re-encode: a stream copy would snap the in-point to the nearest
            # keyframe and throw the alignment away.
            cmd += ["-c:v", "libx264", "-preset", "fast", "-crf", "18",
                    "-pix_fmt", "yuv420p",
                    "-c:a", "aac", "-b:a", "192k", "-ar", "48000",
                    "-movflags", "+faststart"]
        cmd.append(str(out))
        subprocess.run(cmd, check=True)
        print(f"  {out.name}")
        written.append(out)
    return written


def plot_sync_map(sync_map: dict, out_path: Path) -> Path:
    """Draw each source's span on the master timeline, for visual confirmation.

    A sync map is a wall of numbers; one glance at the bars tells you whether
    an angle landed where you expected or a quarter of the way through the take.
    """
    from PIL import Image, ImageDraw

    sources = sync_map["sources"]
    W, ROW, PAD, LABEL = 1600, 46, 28, 340
    H = PAD * 2 + ROW * len(sources) + 40
    img = Image.new("RGB", (W, H), (18, 18, 22))
    d = ImageDraw.Draw(img, "RGBA")

    t_min = min(s["offset_s"] for s in sources)
    t_max = max(s["offset_s"] + s["duration_s"] for s in sources)
    span = max(t_max - t_min, 1e-6)
    plot_w = W - LABEL - PAD

    def x_of(t: float) -> float:
        return LABEL + (t - t_min) / span * plot_w

    # Shade the window where every source is rolling.
    cs, ce = sync_map["common_start_s"], sync_map["common_end_s"]
    if ce > cs:
        d.rectangle([x_of(cs), PAD - 8, x_of(ce), H - PAD - 24],
                    fill=(70, 130, 90, 60))

    for i, s in enumerate(sources):
        y = PAD + i * ROW
        x0, x1 = x_of(s["offset_s"]), x_of(s["offset_s"] + s["duration_s"])
        color = (90, 160, 220) if s["kind"] == "video" else (220, 160, 90)
        if s["quality"] < TRUST_QUALITY and s["method"] != "reference":
            color = (200, 90, 90)
        d.rectangle([x0, y, x1, y + ROW - 14], fill=color + (220,))
        name = s["name"] if len(s["name"]) <= 36 else s["name"][:33] + "..."
        d.text((PAD, y + 6), name, fill=(235, 235, 240))
        d.text((x0 + 6, y + 6), f"{s['offset_s']:+.2f}s", fill=(15, 15, 18))

    # Time ruler
    ruler_y = H - PAD - 18
    d.line([LABEL, ruler_y, W - PAD, ruler_y], fill=(90, 90, 100))
    for k in range(7):
        t = t_min + span * k / 6
        x = x_of(t)
        d.line([x, ruler_y, x, ruler_y + 6], fill=(90, 90, 100))
        d.text((x - 16, ruler_y + 9), f"{t:.1f}s", fill=(150, 150, 160))

    out_path.parent.mkdir(parents=True, exist_ok=True)
    img.save(out_path)
    print(f"sync plot -> {out_path}")
    return out_path


# -------- Main ---------------------------------------------------------------


def main() -> None:
    global MAX_SHIFT_S, MIN_OVERLAP_S

    ap = argparse.ArgumentParser(
        description="Align separately-recorded audio and multiple cameras."
    )
    ap.add_argument("video", type=Path, nargs="?", help="Camera video file")
    ap.add_argument("audio", type=Path, nargs="?", help="External audio file")
    ap.add_argument("--scan", type=Path,
                    help="Dual-system: pair every video with its audio in a directory")
    ap.add_argument("--multicam", type=Path,
                    help="Align every media file in a directory to one master timeline")
    ap.add_argument("--method", choices=("audio", "flash"), default="audio",
                    help="Multicam alignment method (default: audio)")
    ap.add_argument("--reference", help="Multicam: filename to use as the reference")
    ap.add_argument("--trim", action="store_true",
                    help="Multicam: write copies of every source trimmed to the common window")
    ap.add_argument("--plot", action="store_true",
                    help="Multicam: write a PNG of the timeline layout")
    ap.add_argument("--mux", action="store_true",
                    help="Dual-system: write a synced file (video copied, good audio attached)")
    ap.add_argument("-o", "--output", type=Path,
                    help="Output path for --mux (default: <edit>/synced/<stem>_synced.mp4)")
    ap.add_argument("--edit-dir", type=Path,
                    help="Edit directory (default: <media_parent>/edit)")
    ap.add_argument("--keep-camera-audio", action="store_true",
                    help="Keep the camera scratch track as a second audio stream")
    ap.add_argument("--no-drift-correction", action="store_true",
                    help="Report clock drift but do not resample to fix it")
    ap.add_argument("--force", action="store_true",
                    help="Act even when the match quality is below the trust threshold")
    ap.add_argument("--max-shift", type=float, default=MAX_SHIFT_S, metavar="SEC",
                    help="Assume the sources started within SEC of each other. "
                         "0 (default) searches every lag. Set it when you know the "
                         "rough gap -- it rules out false peaks from repetitive audio.")
    ap.add_argument("--expect-offset", type=float, metavar="SEC",
                    help="Constrain the search to within --tolerance of this offset. "
                         "Use when you know roughly where a clip sits -- e.g. from "
                         "file numbering, a slate, or a shot log -- and correlation "
                         "alone is landing on a false peak.")
    ap.add_argument("--tolerance", type=float, default=EXPECT_TOLERANCE_S, metavar="SEC",
                    help=f"Half-width of the --expect-offset window "
                         f"(default {EXPECT_TOLERANCE_S:g})")
    ap.add_argument("--use-filename-times", action="store_true",
                    help="Constrain the search to the offset implied by wall-clock "
                         "timestamps in the filenames (DJI cameras and mics write "
                         "them). Without this the timestamps are still reported as "
                         "a cross-check, just not enforced.")
    ap.add_argument("--min-overlap", type=float, default=MIN_OVERLAP_S, metavar="SEC",
                    help=f"Ignore alignments backed by less than SEC of common audio "
                         f"(default {MIN_OVERLAP_S:g})")
    ap.add_argument("--json", action="store_true", help="Print results as JSON")
    args = ap.parse_args()

    MAX_SHIFT_S, MIN_OVERLAP_S = args.max_shift, args.min_overlap
    correct_drift = not args.no_drift_correction

    if args.multicam:
        root = args.multicam.resolve()
        edit_dir = (args.edit_dir or root / "edit").resolve()
        sync_map = sync_multicam(root, method=args.method, reference=args.reference)
        out = edit_dir / "sync_map.json"
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(json.dumps(sync_map, indent=2))
        print(f"\nsync map -> {out}")
        if args.plot:
            plot_sync_map(sync_map, edit_dir / "verify" / "sync_map.png")
        if args.trim:
            trim_to_common(sync_map, edit_dir / "aligned")
        if args.json:
            print(json.dumps(sync_map, indent=2))
        return

    if args.scan:
        root = args.scan.resolve()
        edit_dir = (args.edit_dir or root / "edit").resolve()
        results = []
        for v, a in pair_directory(root):
            r = sync_pair(v, a, use_filename_times=args.use_filename_times)
            results.append(r)
            if args.mux:
                if r.confident or args.force:
                    mux(r, edit_dir / "synced" / f"{v.stem}_synced.mp4",
                        args.keep_camera_audio, correct_drift)
                else:
                    print(f"  SKIPPED mux: quality {r.quality:.1f} < {TRUST_QUALITY} "
                          f"(re-run with --force to override)")
            print()
        report = edit_dir / "sync_report.json"
        report.parent.mkdir(parents=True, exist_ok=True)
        report.write_text(json.dumps([asdict(r) for r in results], indent=2))
        print(f"sync report -> {report}")
        if args.json:
            print(json.dumps([asdict(r) for r in results], indent=2))
        return

    if not args.video or not args.audio:
        ap.error("give both <video> and <audio>, or use --scan / --multicam <dir>")

    video, audio = args.video.resolve(), args.audio.resolve()
    result = sync_pair(video, audio, use_filename_times=args.use_filename_times,
                       expect_offset=args.expect_offset, tolerance=args.tolerance)

    if not result.confident:
        print(f"\n  WARNING: quality {result.quality:.1f} is below the trust "
              f"threshold of {TRUST_QUALITY}.\n  The files may not overlap, or one "
              f"may be near-silent. Verify before rendering.")

    if args.mux:
        if not result.confident and not args.force:
            raise SystemExit("  refusing to mux an untrusted match; pass --force to override")
        edit_dir = (args.edit_dir or video.parent / "edit").resolve()
        out = args.output or edit_dir / "synced" / f"{video.stem}_synced.mp4"
        mux(result, out.resolve(), args.keep_camera_audio, correct_drift)

    if args.json:
        print(json.dumps(asdict(result), indent=2))


if __name__ == "__main__":
    main()
