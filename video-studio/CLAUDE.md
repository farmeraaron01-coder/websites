# Video Studio

Conversation-driven video editing. See `README.md` for the overview.

## Before doing anything

Read `.claude/skills/video-editing/SKILL.md`. It has the process and the
twelve hard rules, each of which corresponds to a failure that is invisible
until someone watches the finished file.

For a Mr Taco Shop episode also read `.claude/skills/food-review/SKILL.md`.

## Environment

- Python venv at `.venv`. Run helpers with `.venv/bin/python`.
- `ffmpeg` and `ffprobe` must be on PATH.
- `ELEVENLABS_API_KEY` lives in `.env` (gitignored). Scribe is the default ASR.

## Standing rules

**Never modify source footage.** Everything generated goes in
`<project>/edit/`. Sources are read-only, always.

**Never delete a transcript.** Scribe costs money per minute and transcripts
are cached by file existence. Deleting one silently re-bills the next run.

**Confirm the cut plan before rendering.** Rendering is cheap; rendering the
wrong film is not. Propose the beat structure and the takes, then wait.

**Cap self-review at three passes.** If something is still wrong after three,
describe it rather than looping.

**Commit the edit, not the media.** EDLs, transcripts and project notes are
committed; footage and renders are gitignored.
