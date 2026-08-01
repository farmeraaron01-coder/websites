"""Transcribe a video to a word-level, verbatim transcript.

Word-level timing is not a nicety here -- it is the whole basis of the edit.
Every cut point, every filler removal and every caption cue is derived from
word boundaries, so a transcript that only has sentence timings is useless for
this pipeline.

Verbatim matters just as much. A transcript that has tidied away "um", "uh"
and false starts has destroyed the exact signal the editor needs in order to
remove them. Both backends here are configured to keep disfluencies.

Backends
--------
scribe   ElevenLabs Scribe. Hosted, fast, diarizes speakers, tags audio events
         like (laughter). Costs money per minute and needs ELEVENLABS_API_KEY.
         Best quality; the default when a key is present.
whisper  faster-whisper, running locally on the CPU. Free and offline, but
         slower and it will not separate speakers. Whisper also tends to
         "clean up" disfluencies, so this backend feeds it a deliberately
         disfluent initial prompt to keep them in.

Both backends write the SAME schema, so nothing downstream needs to know which
one ran:

    {"language_code": "eng",
     "text": "...",
     "words": [
       {"type": "word",    "text": "Hello", "start": 0.0,  "end": 0.42, "speaker_id": "speaker_0"},
       {"type": "spacing", "text": " ",     "start": 0.42, "end": 0.61},
       ...
     ],
     "_backend": "scribe"}

`spacing` entries are where the silences live -- pack_transcripts.py and the
cut planner both read gaps out of them, so they are load-bearing, not padding.

Cached: if the transcript already exists, the work is skipped entirely. Scribe
in particular costs real money, so never delete transcripts casually.

Usage:
    python helpers/transcribe.py <video>
    python helpers/transcribe.py <video> --backend whisper --model medium.en
    python helpers/transcribe.py <video> --language en --num-speakers 2
    python helpers/transcribe.py <video> --prompt-file vocab.txt
    python helpers/transcribe.py --batch <dir> --workers 4
"""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
import tempfile
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

import requests

SCRIBE_URL = "https://api.elevenlabs.io/v1/speech-to-text"

VIDEO_EXTS = {".mp4", ".mov", ".mkv", ".avi", ".m4v", ".mts", ".m2ts", ".webm"}
AUDIO_EXTS = {".wav", ".aiff", ".aif", ".flac", ".mp3", ".m4a", ".aac", ".ogg", ".opus"}

# Whisper is trained to produce clean, readable text, which means it silently
# drops exactly the disfluencies this pipeline needs to see. Priming it with a
# disfluent prompt shifts its style toward verbatim.
VERBATIM_PROMPT = (
    "Um, so, uh, I mean... this is, like, you know, a really — a really good one. "
    "Uhh, let me, let me try that again."
)


# -------- Shared helpers -----------------------------------------------------


def load_api_key() -> str | None:
    for candidate in [Path(__file__).resolve().parent.parent / ".env",
                      Path(__file__).resolve().parents[3] / ".env",
                      Path(".env")]:
        if candidate.exists():
            for line in candidate.read_text().splitlines():
                line = line.strip()
                if not line or line.startswith("#") or "=" not in line:
                    continue
                k, v = line.split("=", 1)
                if k.strip() == "ELEVENLABS_API_KEY":
                    val = v.strip().strip('"').strip("'")
                    if val:
                        return val
    return os.environ.get("ELEVENLABS_API_KEY") or None


def extract_audio(video_path: Path, dest: Path) -> None:
    subprocess.run(
        ["ffmpeg", "-y", "-v", "error", "-nostdin", "-i", str(video_path),
         "-vn", "-ac", "1", "-ar", "16000", "-c:a", "pcm_s16le", str(dest)],
        check=True,
    )


def add_spacing_entries(words: list[dict]) -> list[dict]:
    """Interleave `spacing` entries into a bare word list.

    Scribe emits these natively; the whisper path has to synthesize them. They
    are how every downstream consumer sees silence, so a transcript without
    them looks like continuous speech and every pause-based decision breaks.
    """
    out: list[dict] = []
    for i, w in enumerate(words):
        out.append(w)
        if i + 1 < len(words):
            gap_start, gap_end = w["end"], words[i + 1]["start"]
            if gap_end > gap_start:
                out.append({"type": "spacing", "text": " ",
                            "start": round(gap_start, 3), "end": round(gap_end, 3)})
    return out


# -------- Backend: ElevenLabs Scribe ----------------------------------------


def call_scribe(audio_path: Path, api_key: str, language: str | None = None,
                num_speakers: int | None = None) -> dict:
    data: dict[str, str] = {
        "model_id": "scribe_v1",
        "diarize": "true",
        "tag_audio_events": "true",
        "timestamps_granularity": "word",
    }
    if language:
        data["language_code"] = language
    if num_speakers:
        data["num_speakers"] = str(num_speakers)

    with open(audio_path, "rb") as f:
        resp = requests.post(
            SCRIBE_URL,
            headers={"xi-api-key": api_key},
            files={"file": (audio_path.name, f, "audio/wav")},
            data=data, timeout=1800,
        )
    if resp.status_code != 200:
        raise RuntimeError(f"Scribe returned {resp.status_code}: {resp.text[:500]}")

    payload = resp.json()
    payload["_backend"] = "scribe"
    return payload


# -------- Backend: local faster-whisper -------------------------------------


def call_whisper(audio_path: Path, model_size: str = "small.en",
                 language: str | None = None, prompt: str | None = None,
                 verbose: bool = True) -> dict:
    try:
        from faster_whisper import WhisperModel
    except ImportError:
        sys.exit(
            "faster-whisper is not installed. Either:\n"
            "  uv pip install faster-whisper        # free, local, slower\n"
            "or set ELEVENLABS_API_KEY and use --backend scribe (better quality)."
        )

    if verbose:
        print(f"  loading whisper model {model_size} (first run downloads it)",
              flush=True)
    model = WhisperModel(model_size, device="cpu", compute_type="int8")

    segments, info = model.transcribe(
        str(audio_path),
        language=language,
        word_timestamps=True,
        # Keep the disfluencies: no VAD gating out hesitations, no carrying
        # previous text forward (which pushes it toward tidy prose), and a
        # prompt that models the messy style we want back.
        vad_filter=False,
        condition_on_previous_text=False,
        initial_prompt=prompt or VERBATIM_PROMPT,
        beam_size=5,
    )

    words: list[dict] = []
    text_parts: list[str] = []
    for seg in segments:
        text_parts.append(seg.text)
        for w in (seg.words or []):
            token = w.word.strip()
            if not token:
                continue
            words.append({
                "type": "word", "text": token,
                "start": round(w.start, 3), "end": round(w.end, 3),
                # Whisper does not diarize. Everything is one speaker; if you
                # need real diarization, use the Scribe backend.
                "speaker_id": "speaker_0",
            })
        if verbose and len(words) % 500 < 10:
            print(f"    {len(words)} words...", flush=True)

    return {
        "language_code": getattr(info, "language", language or "eng"),
        "text": "".join(text_parts).strip(),
        "words": add_spacing_entries(words),
        "_backend": f"faster-whisper:{model_size}",
    }


# -------- Orchestration ------------------------------------------------------


def transcribe_one(video: Path, edit_dir: Path, backend: str = "auto",
                   api_key: str | None = None, language: str | None = None,
                   num_speakers: int | None = None, model_size: str = "small.en",
                   prompt: str | None = None, verbose: bool = True) -> Path:
    """Transcribe one media file. Returns the transcript path.

    Cached: an existing transcript is returned untouched.
    """
    transcripts_dir = edit_dir / "transcripts"
    transcripts_dir.mkdir(parents=True, exist_ok=True)
    out_path = transcripts_dir / f"{video.stem}.json"

    if out_path.exists():
        if verbose:
            print(f"cached: {out_path.name}")
        return out_path

    if backend == "auto":
        backend = "scribe" if (api_key or load_api_key()) else "whisper"
        if verbose:
            print(f"  backend: {backend} (auto-selected)")

    t0 = time.time()
    with tempfile.TemporaryDirectory() as tmp:
        audio = Path(tmp) / f"{video.stem}.wav"
        if verbose:
            print(f"  extracting audio from {video.name}", flush=True)
        extract_audio(video, audio)

        if backend == "scribe":
            key = api_key or load_api_key()
            if not key:
                sys.exit("ELEVENLABS_API_KEY not found in .env or environment. "
                         "Use --backend whisper to transcribe locally instead.")
            mb = audio.stat().st_size / (1024 * 1024)
            if verbose:
                print(f"  uploading {audio.name} ({mb:.1f} MB) to Scribe", flush=True)
            payload = call_scribe(audio, key, language, num_speakers)
        elif backend == "whisper":
            payload = call_whisper(audio, model_size, language, prompt, verbose)
        else:
            sys.exit(f"unknown backend: {backend}")

    out_path.write_text(json.dumps(payload, indent=2))

    if verbose:
        kb = out_path.stat().st_size / 1024
        n_words = sum(1 for w in payload.get("words", []) if w.get("type") == "word")
        print(f"  saved: {out_path.name} ({kb:.1f} KB, {n_words} words) "
              f"in {time.time() - t0:.1f}s")
    return out_path


def transcribe_batch(root: Path, edit_dir: Path, workers: int = 4, **kw) -> list[Path]:
    """Transcribe every media file in a directory.

    Scribe is network-bound so it parallelizes well. Local whisper is
    CPU-bound, so the worker count is forced to 1 there -- running several
    copies of the model just thrashes.
    """
    files = sorted(p for p in root.iterdir() if p.is_file()
                   and p.suffix.lower() in (VIDEO_EXTS | AUDIO_EXTS))
    if not files:
        raise SystemExit(f"no media files in {root}")

    backend = kw.get("backend", "auto")
    if backend == "auto":
        backend = "scribe" if load_api_key() else "whisper"
        kw["backend"] = backend
    if backend == "whisper" and workers > 1:
        print("  local whisper is CPU-bound; running sequentially")
        workers = 1

    print(f"transcribing {len(files)} file(s) with {workers} worker(s), "
          f"backend={backend}\n")
    done: list[Path] = []
    with ThreadPoolExecutor(max_workers=workers) as pool:
        futures = {pool.submit(transcribe_one, f, edit_dir, **kw): f for f in files}
        for fut in as_completed(futures):
            src = futures[fut]
            try:
                done.append(fut.result())
            except Exception as exc:
                print(f"  FAILED {src.name}: {exc}")
    print(f"\n{len(done)}/{len(files)} transcribed -> {edit_dir / 'transcripts'}")
    return done


def main() -> None:
    ap = argparse.ArgumentParser(
        description="Transcribe to a word-level verbatim transcript.")
    ap.add_argument("video", type=Path, nargs="?", help="Media file to transcribe")
    ap.add_argument("--batch", type=Path, help="Transcribe every media file in a directory")
    ap.add_argument("--edit-dir", type=Path,
                    help="Edit output directory (default: <media_parent>/edit)")
    ap.add_argument("--backend", choices=("auto", "scribe", "whisper"), default="auto",
                    help="auto picks scribe when ELEVENLABS_API_KEY is set, else whisper")
    ap.add_argument("--model", default="small.en", dest="model_size",
                    help="whisper model size: tiny.en, base.en, small.en, medium.en, "
                         "large-v3 (default small.en)")
    ap.add_argument("--language", help="ISO language code, e.g. 'en'. Omit to auto-detect.")
    ap.add_argument("--num-speakers", type=int,
                    help="Scribe only: speaker count when known, improves diarization")
    ap.add_argument("--prompt", help="whisper only: initial prompt to bias spelling/style")
    ap.add_argument("--prompt-file", type=Path,
                    help="whisper only: read the initial prompt from a file "
                         "(use for proper nouns and dish names)")
    ap.add_argument("--workers", type=int, default=4, help="Batch parallelism")
    args = ap.parse_args()

    prompt = args.prompt
    if args.prompt_file:
        prompt = args.prompt_file.read_text().strip()

    common = dict(backend=args.backend, language=args.language,
                  num_speakers=args.num_speakers, model_size=args.model_size,
                  prompt=prompt)

    if args.batch:
        root = args.batch.resolve()
        edit_dir = (args.edit_dir or root / "edit").resolve()
        transcribe_batch(root, edit_dir, workers=args.workers, **common)
        return

    if not args.video:
        ap.error("give a <video>, or use --batch <dir>")
    video = args.video.resolve()
    if not video.exists():
        sys.exit(f"not found: {video}")
    edit_dir = (args.edit_dir or video.parent / "edit").resolve()
    transcribe_one(video, edit_dir, **common)


if __name__ == "__main__":
    main()
