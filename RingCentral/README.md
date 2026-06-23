# RingCentral Recording Downloader

Downloads **all call recordings** from your RingCentral account and saves them to
a local folder (e.g. your Google Drive), organized by agent and date:

```
<OUTPUT_DIR>/
  Jane Smith (ext 101)/
    2026-06-21/
      2026-06-21_143205_Inbound_+15551234567_<recordingId>.mp3
    2026-06-22/
      ...
  John Doe (ext 102)/
    ...
  recordings_manifest.csv      <- log of everything (date, agent, numbers, file)
```

- **Scope:** entire account (every extension/user).
- **Grouped by:** the internal agent/extension that handled the call.
- **Format:** whatever RingCentral serves (normally MP3), saved unchanged.
- **Window:** last **60 days** by default (RingCentral only retains ~90 days).
- **Resumable:** files already on disk are skipped, so you can re-run it anytime.

## 1. Prerequisites

- Python 3.8+ installed.
- A RingCentral app with **JWT auth** enabled and the **Read Call Log** and
  **Read Call Recording** (a.k.a. *ReadCallLog*) permissions. Because we pull the
  whole account, the JWT must belong to a user with **admin / company call log**
  access.
- A **JWT credential** string generated in the RingCentral developer console
  (https://developers.ringcentral.com → your app → *Credentials* → *Add JWT*).

## 2. Install

```powershell
cd "C:\Users\AaronFarmer\Farmer Agency Dropbox\Aaron Farmer\Claude CoWork Files\RingCentral"
pip install -r requirements.txt
```

## 3. Configure

Create your `.env` file (see `.env.example` for the template). The script reads
this path by default:

```
C:\Users\AaronFarmer\Farmer Agency Dropbox\Aaron Farmer\Claude CoWork Files\RingCentral\.env
```

Required keys: `RC_CLIENT_ID`, `RC_CLIENT_SECRET`, `RC_JWT`.
Set `RC_OUTPUT_DIR` to your Google Drive folder, e.g. `G:\My Drive\RingCentral Recordings`.

> The script also accepts common alternate names (e.g. `RINGCENTRAL_CLIENT_ID`),
> so if your `.env` already uses those, it will still work.

## 4. Run

```powershell
python download_recordings.py
```

It will authenticate, list the account call log in monthly chunks, and download
each recording. Progress prints to the console; a full `recordings_manifest.csv`
is written into the output folder.

If it stops (rate limit, network, Ctrl+C), just run it again — it picks up where
it left off.

## Notes & tuning

- **Rate limits:** RingCentral throttles the call-log API hard (~10 req/min). The
  script paces itself (`SECONDS_BETWEEN_CALLS`) and honors `429 Retry-After`
  responses. Pulling a busy 60-day account can take a while — that's normal.
- **Change the window:** set `RC_LOOKBACK_DAYS` in `.env` (max useful ~90).
- **Sandbox vs production:** set `RC_SERVER_URL` accordingly.
- **Group by customer instead of agent:** ask and this can be switched to fold by
  the external party instead.
