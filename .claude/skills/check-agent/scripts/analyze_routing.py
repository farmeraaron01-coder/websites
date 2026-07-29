#!/usr/bin/env python3
"""Find where inbound calls are being lost on a RingCentral account.

Read-only. Produces a per-number scorecard, leg traces comparing lost vs answered
calls, correctly-measured dead air, and the caller hang-up distribution.

    # which line is losing calls?
    python analyze_routing.py --env /path/to/.env --days 30

    # drill into one number
    python analyze_routing.py --env /path/to/.env --number +18555867467 --days 30

    # drill into one person / AI agent by name or extension
    python analyze_routing.py --env /path/to/.env --agent "Sarah AI"
"""

import argparse
import collections
import os
import sys
from datetime import datetime, timedelta

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from rc_client import RCClient, is_lost, LOST  # noqa: E402

ANSWERED_LEG = {"Accepted", "Call connected"}


def dest(leg):
    t = leg.get("to") or {}
    return (t.get("phoneNumber") or ""), (t.get("extensionNumber") or ""), (t.get("name") or "")


def scorecard(calls, top=14):
    per = collections.defaultdict(lambda: {"t": 0, "a": 0, "l": 0, "route": set()})
    for r in calls:
        to = r.get("to") or {}
        key = to.get("phoneNumber") or f"ext-{to.get('extensionNumber')}"
        p = per[key]
        p["t"] += 1
        p["l" if is_lost(r) else "a"] += 1
        for leg in (r.get("legs") or [])[1:3]:
            n = (leg.get("to") or {}).get("name")
            if n:
                p["route"].add(n)

    print("\n=== PER-NUMBER SCORECARD (inbound) ===")
    print(f"{'NUMBER':17}{'TOTAL':>6}{'ANSW':>6}{'LOST':>6}{'LOST%':>7}   routes to")
    rows = sorted(per.items(), key=lambda kv: -kv[1]["t"])[:top]
    for num, p in rows:
        pct = 100 * p["l"] / p["t"] if p["t"] else 0
        flag = "  <<<" if pct >= 25 and p["t"] >= 10 else ""
        print(f"{num:17}{p['t']:6}{p['a']:6}{p['l']:6}{pct:6.0f}%   "
              f"{', '.join(sorted(p['route']))[:44]}{flag}")
    print("\n  '<<<' marks lines losing >=25% of at least 10 calls.")
    return per


def trace(r, tag):
    frm = (r.get("from") or {}).get("phoneNumber", "?")
    print(f"\n{tag} {r.get('startTime')} result={r.get('result')} "
          f"dur={r.get('duration')}s from {frm}")
    for leg in (r.get("legs") or []):
        pn, ext, name = dest(leg)
        print(f"    {str(leg.get('legType')):15} {str(leg.get('result')):16}"
              f"{str(leg.get('reason') or ''):20} dur={str(leg.get('duration') or 0):>4}s"
              f"  -> {pn} {('ext'+str(ext)) if ext else ''} {name}")


def dead_air(calls, connect_to=None):
    """Dead air = ringing before the connecting leg, counting only legs nobody answered.

    Summing every leg would fold in calls where someone picked up and talked, which
    inflates 'wasted time' and wrongly blames whoever answers most often.
    """
    reached, missed_entirely, waste = [], [], collections.Counter()
    for r in calls:
        pre, hit = 0, False
        for leg in (r.get("legs") or [])[2:]:
            pn, ext, name = dest(leg)
            if connect_to and pn == connect_to:
                hit = True
                break
            if leg.get("result") in ANSWERED_LEG:
                continue                      # real conversation, not dead air
            d = int(leg.get("duration") or 0)
            pre += d
            if d and leg.get("legType") == "PstnToSip":
                waste[f"ext {ext or '?'} {name}".strip()] += d
        (reached if hit else missed_entirely).append((r, pre))

    if connect_to:
        print(f"\n=== HANDOFF TO {connect_to} ===")
        print(f"  reached it:     {len(reached)}")
        print(f"  never got there:{len(missed_entirely)}")
    pres = sorted(p for _, p in reached if p > 0)
    if pres:
        print(f"\n  Dead air before it connects (answered calls only):")
        print(f"    median {pres[len(pres)//2]}s | max {max(pres)}s | "
              f"mean {sum(pres)/len(pres):.0f}s")
    if waste:
        print("\n  Unanswered ring time consumed per extension "
              "(talk time excluded):")
        for k, v in waste.most_common(8):
            print(f"    {k:34} {v:6}s")
    return reached, missed_entirely


def hangups(calls):
    ds = sorted(int(r.get("duration") or 0) for r in calls if is_lost(r))
    if not ds:
        print("\n=== HANG-UPS === none")
        return ds
    print(f"\n=== CALLER PATIENCE ON LOST CALLS (n={len(ds)}) ===")
    print(f"  {ds}")
    med = ds[len(ds) // 2]
    quick = sum(1 for d in ds if d <= 15)
    print(f"\n  median {med}s | under 15s: {quick} of {len(ds)} "
          f"({100*quick/len(ds):.0f}%)")
    if quick:
        print("  -> Those callers hung up early. Reordering anything LATER in the\n"
              "     ring sequence cannot recover them; only shortening the ring\n"
              "     that comes BEFORE the handoff will.")
    return ds


def by_hour(calls, tz_offset):
    print(f"\n=== HOUR OF DAY (UTC{tz_offset:+d}) ===")
    lost, ans = collections.Counter(), collections.Counter()
    for r in calls:
        try:
            h = (datetime.strptime(r.get("startTime", "")[:19], "%Y-%m-%dT%H:%M:%S")
                 + timedelta(hours=tz_offset)).hour
        except ValueError:
            continue
        (lost if is_lost(r) else ans)[h] += 1
    print("  hour   lost  answered")
    for h in range(24):
        if lost[h] or ans[h]:
            bar = "#" * min(int(lost[h]), 30)
            print(f"  {h:02d}:00 {lost[h]:5} {ans[h]:9}  {bar}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--env", help="path to .env with RC credentials")
    ap.add_argument("--days", type=int, default=30)
    ap.add_argument("--number", help="drill into one inbound number, e.g. +18555867467")
    ap.add_argument("--agent", help="person / AI agent name or extension number")
    ap.add_argument("--connect-to", help="external number the agent answers on")
    ap.add_argument("--tz-offset", type=int, default=-7, help="hours from UTC for display")
    a = ap.parse_args()

    rc = RCClient.from_env(a.env)
    print(f"Authenticated. scopes: {rc.scopes}")

    if a.agent:
        q = a.agent.strip().lower()
        hits = [e for e in rc.extensions()
                if q in (e.get("name") or "").lower()
                or q == str(e.get("extensionNumber"))]
        if not hits:
            sys.exit(f"No extension matching {a.agent!r}.")
        for e in hits:
            print(f"\n=== {e.get('name')} | ext {e.get('extensionNumber')} | "
                  f"type={e.get('type')} | status={e.get('status')} | id={e.get('id')} ===")
            if e.get("status") != "Enabled":
                print("  !! extension is not Enabled — it cannot take calls")
            own = rc.call_log(days=a.days, extension_id=e["id"])
            print(f"  inbound calls on THIS extension, {a.days}d: {len(own)}")
            print("  results:", dict(collections.Counter(r.get("result") for r in own)))
            if not own:
                print("  NOTE: zero calls here does NOT mean the agent is idle. An AI\n"
                      "        voice agent normally answers on its provider's number\n"
                      "        instead. Check the provider (ElevenLabs/Twilio) before\n"
                      "        concluding anything is broken.")
            for r in own[:3]:
                trace(r, "[sample]")

    calls = rc.call_log(days=a.days)
    print(f"\nAccount-wide inbound calls, last {a.days} days: {len(calls)}")
    print("results:", dict(collections.Counter(r.get("result") for r in calls)))
    scorecard(calls)

    if a.number:
        tgt = [r for r in calls if (r.get("to") or {}).get("phoneNumber") == a.number]
        print(f"\n\n########## {a.number}: {len(tgt)} calls / {a.days}d ##########")
        print("results:", dict(collections.Counter(r.get("result") for r in tgt)))
        print("\n---------- LOST (all) ----------")
        for r in [x for x in tgt if is_lost(x)][:12]:
            trace(r, "[LOST]")
        print("\n---------- ANSWERED (for comparison) ----------")
        for r in [x for x in tgt if not is_lost(x)][:3]:
            trace(r, "[ OK ]")
        dead_air(tgt, a.connect_to)
        hangups(tgt)
        by_hour(tgt, a.tz_offset)

    print("\nDone. Read the leg traces above: the difference between a LOST and an\n"
          "OK call on the same number is the diagnosis.")


if __name__ == "__main__":
    main()
