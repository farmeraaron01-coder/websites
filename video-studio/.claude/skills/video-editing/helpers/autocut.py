"""Propose a cut list from a word-level transcript.

This tool does the mechanical part of a first pass: the hesitations, the dead
air, the stutters. It produces a DRAFT EDL and a human-readable report.

It deliberately does not try to do the editorial part. Deciding which of four
takes is the good one, where a story drags, whether a pause is dead air or a
beat the moment needs -- that is judgment, and it belongs to whoever is
reading `takes_packed.md`, not to a word list. Treat the output as a starting
point to review and adjust, never as a finished cut.

Two things it is careful about, because both are easy to get wrong and painful
to notice later:

  Never cut inside a word. Every boundary snaps to a word edge from the
  transcript, so a cut can never clip a syllable.

  Always leave breath. Cuts land in the silence AROUND a removal, with a small
  pad kept on each side, so joins do not sound clipped or rushed.

Usage:
    python helpers/autocut.py --edit-dir <edit> --source <name>
    python helpers/autocut.py --edit-dir <edit> --source <name> --aggressive
    python helpers/autocut.py --edit-dir <edit> --source <name> --max-silence 0.6
    python helpers/autocut.py --edit-dir <edit> --source <name> --no-silence
    python helpers/autocut.py --edit-dir <edit> --all -o edit/edl_draft.json
"""

from __future__ import annotations

import argparse
import json
import re
from dataclasses import dataclass
from pathlib import Path

# Sounds that carry no meaning in any context. Removing these is safe enough
# to do by list.
FILLERS_SAFE = {
    "um", "umm", "ummm", "uh", "uhh", "uhhh", "er", "err", "erm",
    "ah", "ahh", "eh", "mm", "mmm", "hmm", "hm", "mhm", "uhm",
}

# Discourse markers. These are often real speech -- "like" can be a verb, "so"
# can open a sentence properly, "right" can be a question. Only enabled with
# --aggressive, and the report flags every one so they can be checked.
FILLERS_AGGRESSIVE = {"like", "so", "basically", "actually", "literally", "right", "okay"}

# Multi-word hedges, matched as phrases.
FILLER_PHRASES = [
    ("you", "know"), ("i", "mean"), ("kind", "of"), ("sort", "of"),
    ("you", "know", "what", "i", "mean"),
]

# Keep this much room tone on each side of a join. Below ~30 ms the cut sounds
# clipped; above ~200 ms you can hear the hole where the word was.
PAD_S = 0.06
# How far a word-based removal may reach into neighbouring silence. Without a
# cap, removing a filler that happens to sit next to a long pause swallows the
# whole pause and reports it as a filler cut -- which both hides a real
# editorial decision and can delete a beat the moment needed.
MAX_ABSORB_S = 0.35
# Drop kept segments shorter than this -- they read as glitches, not content.
MIN_SEGMENT_S = 0.35
# A pause longer than this is dead air by default.
DEFAULT_MAX_SILENCE_S = 0.7
# Silence left behind after trimming a long pause.
SILENCE_KEEP_S = 0.25


def bare(token: str) -> str:
    """Strip punctuation and case so 'Um,' and 'UM.' both match 'um'.

    ASR emits words with punctuation attached and arbitrary capitalization, so
    comparing raw tokens misses most of what you are looking for.
    """
    return re.sub(r"[^\w']", "", token).lower()


@dataclass
class Removal:
    start: float
    end: float
    kind: str      # "filler" | "silence" | "repeat"
    detail: str

    @property
    def duration(self) -> float:
        return self.end - self.start


def load_words(transcript_path: Path) -> list[dict]:
    data = json.loads(transcript_path.read_text())
    return [w for w in data.get("words", [])
            if w.get("type") == "word" and w.get("start") is not None]


def find_fillers(words: list[dict], aggressive: bool) -> list[Removal]:
    vocab = FILLERS_SAFE | (FILLERS_AGGRESSIVE if aggressive else set())
    tokens = [bare(w.get("text", "")) for w in words]
    removals: list[Removal] = []
    consumed: set[int] = set()

    # Phrases first, longest first, so "you know what i mean" wins over
    # "you know".
    for phrase in sorted(FILLER_PHRASES, key=len, reverse=True):
        if not aggressive and len(phrase) < 3:
            continue
        n = len(phrase)
        for i in range(len(tokens) - n + 1):
            if any(j in consumed for j in range(i, i + n)):
                continue
            if tuple(tokens[i : i + n]) == phrase:
                consumed.update(range(i, i + n))
                removals.append(Removal(
                    words[i]["start"], words[i + n - 1]["end"],
                    "filler", " ".join(phrase)))

    for i, tok in enumerate(tokens):
        if i in consumed or tok not in vocab:
            continue
        consumed.add(i)
        flag = " (discourse marker - check this one)" if tok in FILLERS_AGGRESSIVE else ""
        removals.append(Removal(words[i]["start"], words[i]["end"],
                                "filler", tok + flag))
    return removals


def find_repeats(words: list[dict]) -> list[Removal]:
    """Collapse immediate stutters: 'the the the' keeps one 'the'.

    Only exact adjacent repeats of short words, and only when they are butted
    up against each other in time. A deliberate repetition for emphasis
    ("very, very good") has a pause between the words and is left alone.
    """
    removals: list[Removal] = []
    i = 0
    while i < len(words) - 1:
        tok = bare(words[i].get("text", ""))
        if not tok or len(tok) > 5:
            i += 1
            continue
        run_end = i
        while (run_end + 1 < len(words)
               and bare(words[run_end + 1].get("text", "")) == tok
               and words[run_end + 1]["start"] - words[run_end]["end"] < 0.25):
            run_end += 1
        if run_end > i:
            # Keep the LAST one: the final attempt is usually the cleanest and
            # it butts directly against whatever follows.
            removals.append(Removal(words[i]["start"], words[run_end]["start"],
                                    "repeat", f"{tok!r} x{run_end - i + 1}"))
            i = run_end + 1
        else:
            i += 1
    return removals


def find_silences(words: list[dict], max_silence: float) -> list[Removal]:
    """Trim pauses longer than max_silence down to SILENCE_KEEP_S."""
    removals: list[Removal] = []
    for a, b in zip(words, words[1:]):
        gap = b["start"] - a["end"]
        if gap <= max_silence:
            continue
        # Remove from the middle, keeping a little tail on each side so the
        # rhythm still breathes.
        keep_each = SILENCE_KEEP_S / 2
        start, end = a["end"] + keep_each, b["start"] - keep_each
        if end - start > 0.05:
            removals.append(Removal(start, end, "silence", f"{gap:.2f}s pause"))
    return removals


def expand_to_silence(removals: list[Removal], words: list[dict]) -> list[Removal]:
    """Grow each word-based removal outward into the surrounding silence.

    Cutting exactly on a word's own boundaries leaves the pauses that framed it
    on both sides, so removing "um" from "and ... um ... the" produces an
    audible double-pause. Absorbing the neighbouring silence and then keeping a
    small pad makes the join sound like the word was never said.
    """
    starts = [w["start"] for w in words]
    ends = [w["end"] for w in words]
    out: list[Removal] = []
    for r in removals:
        if r.kind == "silence":
            out.append(r)
            continue
        prev_end = max((e for e in ends if e <= r.start + 1e-6), default=r.start)
        next_start = min((s for s in starts if s >= r.end - 1e-6), default=r.end)
        # Reach into the neighbouring gap, but never past MAX_ABSORB_S and
        # never closer than PAD_S to the surviving words on either side. Long
        # pauses stay where they are and get judged as silence on their own
        # merits, not quietly deleted as a side effect of a filler cut.
        new_start = min(r.start, max(prev_end + PAD_S, r.start - MAX_ABSORB_S))
        new_end = max(r.end, min(next_start - PAD_S, r.end + MAX_ABSORB_S))
        out.append(Removal(new_start, new_end, r.kind, r.detail))
    return [r for r in out if r.duration > 0.02]


def merge_removals(removals: list[Removal]) -> list[Removal]:
    if not removals:
        return []
    ordered = sorted(removals, key=lambda r: r.start)
    merged = [ordered[0]]
    for r in ordered[1:]:
        last = merged[-1]
        if r.start <= last.end + 0.02:
            merged[-1] = Removal(last.start, max(last.end, r.end), last.kind,
                                 f"{last.detail} + {r.detail}")
        else:
            merged.append(r)
    return merged


def invert(removals: list[Removal], t_start: float, t_end: float) -> list[tuple[float, float]]:
    keeps: list[tuple[float, float]] = []
    cursor = t_start
    for r in removals:
        if r.start > cursor:
            keeps.append((cursor, min(r.start, t_end)))
        cursor = max(cursor, r.end)
    if cursor < t_end:
        keeps.append((cursor, t_end))
    return [(a, b) for a, b in keeps if b - a >= MIN_SEGMENT_S]


def snap_to_words(keeps: list[tuple[float, float]], words: list[dict]
                  ) -> list[tuple[float, float]]:
    """Never cut inside a word (Rule 6).

    A keep whose edge lands mid-word is pulled outward to that word's own
    boundary, which is always safe: it can only ever include more of a word,
    never half of one.
    """
    out: list[tuple[float, float]] = []
    for a, b in keeps:
        for w in words:
            if w["start"] < a < w["end"]:
                a = w["start"]
            if w["start"] < b < w["end"]:
                b = w["end"]
        out.append((round(a, 3), round(b, 3)))
    return out


def plan_source(transcript: Path, aggressive: bool, max_silence: float | None,
                do_repeats: bool) -> dict:
    words = load_words(transcript)
    if not words:
        return {"source": transcript.stem, "keeps": [], "removals": [], "words": 0}

    removals = find_fillers(words, aggressive)
    if do_repeats:
        removals += find_repeats(words)
    removals = expand_to_silence(removals, words)
    if max_silence is not None:
        removals += find_silences(words, max_silence)
    removals = merge_removals(removals)

    t_start = max(0.0, words[0]["start"] - 0.15)
    t_end = words[-1]["end"] + 0.25
    keeps = snap_to_words(invert(removals, t_start, t_end), words)

    return {
        "source": transcript.stem,
        "words": len(words),
        "span": [round(t_start, 3), round(t_end, 3)],
        "keeps": keeps,
        "removals": [{"start": round(r.start, 3), "end": round(r.end, 3),
                      "kind": r.kind, "detail": r.detail,
                      "duration": round(r.duration, 3)} for r in removals],
    }


def write_report(plans: list[dict], out_path: Path) -> None:
    lines = ["# Cut proposal", "",
             "Draft only. Review every removal before rendering -- especially "
             "anything flagged as a discourse marker, where the word is often "
             "real speech rather than a filler.", ""]
    for p in plans:
        if not p["words"]:
            lines += [f"## {p['source']}", "", "_no transcript words_", ""]
            continue
        original = p["span"][1] - p["span"][0]
        kept = sum(b - a for a, b in p["keeps"])
        by_kind: dict[str, list[dict]] = {}
        for r in p["removals"]:
            by_kind.setdefault(r["kind"], []).append(r)

        lines += [
            f"## {p['source']}", "",
            f"- {p['words']} words, {original:.1f}s of source",
            f"- proposal keeps {kept:.1f}s in {len(p['keeps'])} segment(s) "
            f"({original - kept:.1f}s removed, {100 * (original - kept) / original:.0f}%)",
            "",
        ]
        for kind in ("filler", "repeat", "silence"):
            items = by_kind.get(kind, [])
            if not items:
                continue
            total = sum(i["duration"] for i in items)
            lines += [f"### {kind} ({len(items)} cuts, {total:.1f}s)", ""]
            for r in items[:60]:
                lines.append(f"- `{r['start']:8.2f} - {r['end']:8.2f}`  "
                             f"({r['duration']:.2f}s)  {r['detail']}")
            if len(items) > 60:
                lines.append(f"- _... and {len(items) - 60} more_")
            lines.append("")
    out_path.write_text("\n".join(lines))
    print(f"report -> {out_path}")


def main() -> None:
    ap = argparse.ArgumentParser(description="Propose a cut list from a transcript.")
    ap.add_argument("--edit-dir", type=Path, required=True, help="Edit directory")
    ap.add_argument("--source", help="Transcript stem to plan (default: all)")
    ap.add_argument("--all", action="store_true", help="Plan every transcript")
    ap.add_argument("-o", "--output", type=Path,
                    help="Draft EDL path (default: <edit>/edl_draft.json)")
    ap.add_argument("--aggressive", action="store_true",
                    help="Also cut discourse markers (like, so, basically, actually). "
                         "Every one is flagged in the report -- check them.")
    ap.add_argument("--max-silence", type=float, default=DEFAULT_MAX_SILENCE_S,
                    help=f"Trim pauses longer than this (default {DEFAULT_MAX_SILENCE_S})")
    ap.add_argument("--no-silence", action="store_true",
                    help="Leave pauses alone; only remove fillers and stutters")
    ap.add_argument("--no-repeats", action="store_true",
                    help="Leave stutters alone")
    args = ap.parse_args()

    edit_dir = args.edit_dir.resolve()
    tdir = edit_dir / "transcripts"
    if not tdir.exists():
        raise SystemExit(f"no transcripts directory at {tdir} -- run transcribe.py first")

    if args.source:
        paths = [tdir / f"{args.source}.json"]
        if not paths[0].exists():
            raise SystemExit(f"no transcript for {args.source!r} at {paths[0]}")
    else:
        paths = sorted(tdir.glob("*.json"))
        if not paths:
            raise SystemExit(f"no transcripts in {tdir}")

    max_silence = None if args.no_silence else args.max_silence
    plans = [plan_source(p, args.aggressive, max_silence, not args.no_repeats)
             for p in paths]

    # Draft EDL. Source paths are left as the transcript stem: the editor has
    # to point them at real files, which is a deliberate speed bump before
    # anything gets rendered from an unreviewed proposal.
    ranges = []
    for p in plans:
        for a, b in p["keeps"]:
            ranges.append({"source": p["source"], "start": a, "end": b,
                           "beat": "", "reason": "autocut draft"})
    edl = {
        "version": 1,
        "_draft": "Proposal from autocut.py. Review, reorder and cut down before rendering.",
        "sources": {p["source"]: f"TODO_path_to_{p['source']}" for p in plans},
        "ranges": ranges,
        "grade": "auto",
        "total_duration_s": round(sum(b - a for r in plans for a, b in r["keeps"]), 2),
    }
    out = (args.output or edit_dir / "edl_draft.json").resolve()
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(edl, indent=2))

    for p in plans:
        if not p["words"]:
            continue
        original = p["span"][1] - p["span"][0]
        kept = sum(b - a for a, b in p["keeps"])
        print(f"{p['source']:<28} {original:7.1f}s -> {kept:7.1f}s  "
              f"({len(p['removals'])} cuts, {len(p['keeps'])} segments)")
    print(f"\ndraft EDL -> {out}")
    write_report(plans, edit_dir / "cut_proposal.md")


if __name__ == "__main__":
    main()
