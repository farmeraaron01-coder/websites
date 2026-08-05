#!/usr/bin/env python3
"""Compare a live Divi site against its Kadence replacement, and report the differences.

WHY THIS EXISTS
Every defect found on 4 August was found by diffing production against staging with a
script — never by looking at pages. Missing FAQ schema, nine assets that 404 after the
docroot swap, a 1x1 placeholder standing in for a map, a mailto pointing at the wrong
inbox, leftover icon-font glyphs. A person clicking through staging would have passed all
of them, because each page looked fine on its own. They are only visible as a *difference*.

So this turns those one-off checks into one command. Run it before the flip to find what
is missing, and after the flip to prove nothing broke.

USAGE
    python3 preflight.py --live https://statewidefloodinsurance.com \\
                         --new  https://staging.statewidefloodinsurance.com \\
                         [--user 'AJFarmer:app password'] [--limit 0] [--json out.json]

--user is optional and only improves URL discovery on a noindexed staging site. Everything
else works unauthenticated.

WHAT IT CHECKS, worst consequence first
    1. URL parity      — a live URL with no counterpart 404s the moment DNS moves. Needs a
                         redirect or the page. This is the only failure that costs traffic
                         on day one.
    2. Content volume  — a large word-count drop means content did not migrate. This is how
                         a 60KB FAQ page reduced to a 526-byte stub would have been caught.
    3. Broken assets   — every image, script and media file the new page references, fetched.
                         Hot-linked production URLs pass on staging and fail after cutover,
                         so those are reported separately and loudly.
    4. Schema loss     — structured-data @types present live but absent on the new page.
                         Divi code modules do not survive a theme change; this finds what
                         they were carrying.
    5. Interactive     — forms, iframes and maps present live and missing after.
    6. Metadata        — title and meta description present and non-empty.

EXIT STATUS
    0  no findings above the "warn" threshold
    1  at least one finding classified fail

Findings are ranked, not merely listed: a missing URL outranks a missing meta description,
because one loses customers and the other loses a snippet.
"""

from __future__ import annotations

import argparse
import concurrent.futures
import json
import re
import subprocess
import sys
from collections import Counter
from dataclasses import dataclass, field, asdict

UA = ('Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) '
      'Chrome/126.0 Safari/537.36')
TIMEOUT = 60

# Severity ordering, worst first. Used for both sorting and the exit status.
FAIL, WARN, INFO = 'fail', 'warn', 'info'
RANK = {FAIL: 0, WARN: 1, INFO: 2}

# Known-benign differences. A checker that cries wolf gets ignored, and these two
# accounted for 114 of the first run's 174 findings while meaning nothing:
#
#   SiteNavigationElement — Divi's nav plugin emitted it on every page. Google
#   deprecated the type; its absence is not a loss.
#
#   The GTM <noscript> iframe — absent on staging because the theme host-gates
#   tags to the production hostname. That gate is the intended behaviour, so
#   counting it as a missing embed inverts the truth.
BENIGN_SCHEMA = {'SiteNavigationElement'}
IGNORE_IFRAME_HOSTS = ('googletagmanager.com',)


def fetch(url: str, auth: str | None = None, head: bool = False) -> tuple[int, str]:
    """Return (status, body). Cache-busted, because a stale proxy cache reads as a defect."""
    sep = '&' if '?' in url else '?'
    cmd = ['curl', '-sS', '-A', UA, '--max-time', str(TIMEOUT),
           '-w', '\n%{http_code}', f'{url}{sep}_pf=1']
    if head:
        cmd += ['-o', '/dev/null', '-I']
    if auth:
        cmd += ['-u', auth]
    try:
        out = subprocess.run(cmd, capture_output=True, text=True,
                             timeout=TIMEOUT + 30).stdout
    except subprocess.TimeoutExpired:
        return 0, ''
    body, _, code = out.rpartition('\n')
    try:
        return int(code.strip()), body
    except ValueError:
        return 0, body


def rest_slugs(base: str, auth: str | None) -> list[str]:
    """Collect page and post paths via the REST API, falling back to the sitemap."""
    paths: set[str] = set()
    for kind in ('pages', 'posts'):
        for page in (1, 2, 3):
            url = (f'{base}/wp-json/wp/v2/{kind}?per_page=100&page={page}'
                   f'&_fields=link,status')
            code, body = fetch(url, auth)
            if code != 200:
                break
            try:
                rows = json.loads(body)
            except json.JSONDecodeError:
                break
            if not isinstance(rows, list) or not rows:
                break
            for row in rows:
                link = row.get('link') or ''
                if link.startswith(base):
                    paths.add(link[len(base):] or '/')
    return sorted(paths)


SCHEMA_RE = re.compile(r'<script[^>]*application/ld\+json[^>]*>(.*?)</script>', re.S | re.I)
TYPE_RE = re.compile(r'"@type"\s*:\s*"([A-Za-z]+)"')
ASSET_RE = re.compile(r'(?:src|href)="([^"]+\.(?:png|jpe?g|webp|gif|svg|m4a|mp3|mp4|pdf))"', re.I)
TITLE_RE = re.compile(r'<title[^>]*>(.*?)</title>', re.S | re.I)
DESC_RE = re.compile(r'<meta[^>]+name="description"[^>]+content="([^"]*)"', re.I)


def schema_types(html: str) -> Counter:
    found: Counter = Counter()
    for block in SCHEMA_RE.findall(html):
        try:
            json.loads(block)
        except json.JSONDecodeError:
            # Malformed JSON-LD is itself worth knowing about.
            found['__invalid__'] += 1
            continue
        for t in TYPE_RE.findall(block):
            found[t] += 1
    return found


VIDEO_RE = re.compile(
    r'(?:youtube(?:-nocookie)?\.com/(?:embed/|watch\?v=)|youtu\.be/|player\.vimeo\.com/video/)'
    r'([A-Za-z0-9_-]{6,})', re.I)


def video_ids(html: str) -> set[str]:
    """Video identifiers on the page, however they are embedded."""
    return set(VIDEO_RE.findall(html))


def visible_words(html: str) -> int:
    body = re.sub(r'<(script|style|template)[^>]*>.*?</\1>', ' ', html, flags=re.S | re.I)
    body = re.sub(r'<!--.*?-->', ' ', body, flags=re.S)
    return len(re.sub(r'<[^>]+>', ' ', body).split())


@dataclass
class Finding:
    severity: str
    category: str
    path: str
    detail: str
    extra: dict = field(default_factory=dict)


def compare(path: str, live: str, new: str, auth: str | None) -> list[Finding]:
    out: list[Finding] = []
    lcode, lhtml = fetch(live + path)
    ncode, nhtml = fetch(new + path, auth)

    # 1. URL parity — the only finding that costs traffic on day one.
    if lcode == 200 and ncode in (404, 410):
        out.append(Finding(FAIL, 'missing-url', path,
                           f'live {lcode}, new {ncode} — 404s at cutover unless redirected'))
        return out
    if lcode != 200:
        return out  # nothing to compare against
    if ncode != 200:
        out.append(Finding(WARN, 'status', path, f'live 200, new {ncode}'))
        return out

    # 2. Content volume.
    lw, nw = visible_words(lhtml), visible_words(nhtml)
    if lw >= 200 and nw < lw * 0.5:
        out.append(Finding(FAIL, 'content-loss', path,
                           f'{lw} words live vs {nw} new ({100 - nw * 100 // max(lw, 1)}% gone)',
                           {'live_words': lw, 'new_words': nw}))
    elif lw >= 200 and nw < lw * 0.8:
        out.append(Finding(WARN, 'content-thinner', path, f'{lw} words live vs {nw} new',
                           {'live_words': lw, 'new_words': nw}))

    # 3. Assets referenced by the NEW page.
    live_host = live.split('//', 1)[-1].split('/')[0].replace('www.', '')
    for asset in sorted(set(ASSET_RE.findall(nhtml)))[:60]:
        if asset.startswith('data:'):
            continue
        if asset.startswith('/'):
            target, hotlink = new + asset, False
        elif asset.startswith('http'):
            host = asset.split('//', 1)[-1].split('/')[0].replace('www.', '')
            if host != live_host:
                continue  # third-party, not ours to police
            target, hotlink = asset, True
        else:
            continue
        code, _ = fetch(target, head=True)
        if code >= 400:
            out.append(Finding(FAIL, 'broken-asset', path, f'{code} on {asset}'))
        elif hotlink:
            out.append(Finding(FAIL, 'hotlinked-asset', path,
                               f'absolute production URL, will 404 after the swap: {asset}'))

    # A blank placeholder passes an HTTP check but is still a missing image.
    if 'R0lGODlhAQABAAAA' in nhtml:
        out.append(Finding(WARN, 'placeholder-image', path,
                           '1x1 transparent GIF data URI standing in for a real image'))

    # 4. Structured data.
    lt, nt = schema_types(lhtml), schema_types(nhtml)
    if nt.get('__invalid__'):
        out.append(Finding(FAIL, 'invalid-schema', path, 'a JSON-LD block does not parse'))
    lost = {t: c for t, c in lt.items()
            if t != '__invalid__' and t not in BENIGN_SCHEMA and not nt.get(t)}
    if lost:
        sev = FAIL if {'FAQPage', 'Product', 'LocalBusiness'} & set(lost) else WARN
        out.append(Finding(sev, 'schema-loss', path,
                           'types present live, absent new: ' + ', '.join(sorted(lost))))
    if lt.get('Question') and nt.get('Question', 0) < lt['Question']:
        out.append(Finding(WARN, 'fewer-questions', path,
                           f"{lt['Question']} Question nodes live vs {nt.get('Question', 0)} new"))

    # 5. Interactive elements.
    for label, needle in (('cognito form', 'cognitoforms.com'),
                          ('google map', 'google.com/maps/embed')):
        if needle in lhtml and needle not in nhtml:
            out.append(Finding(WARN, 'missing-embed', path, f'{label} present live, absent new'))

    # Count videos by their IDs, not by <iframe>. The new theme uses a click-to-play
    # facade, so a YouTube video that is present and faster reads as a missing iframe
    # if you count tags. Same trap as the seamless Cognito embed replacing an iframe:
    # both are improvements that a naive check reports as losses.
    lv, nv = video_ids(lhtml), video_ids(nhtml)
    gone = lv - nv
    if gone:
        out.append(Finding(WARN, 'missing-video', path,
                           f'{len(gone)} video(s) live and not found new: '
                           + ', '.join(sorted(gone)[:4])))

    # 6. Metadata.
    t = TITLE_RE.search(nhtml)
    if not t or not t.group(1).strip():
        out.append(Finding(WARN, 'no-title', path, 'empty or missing <title>'))
    d = DESC_RE.search(nhtml)
    if not d or not d.group(1).strip():
        out.append(Finding(INFO, 'no-description', path, 'no meta description'))
    elif len(d.group(1)) > 165:
        out.append(Finding(INFO, 'long-description', path,
                           f'{len(d.group(1))} chars, will truncate in results'))
    return out


def check_internal_links(new: str, paths: list[str], auth: str | None,
                         workers: int) -> list[Finding]:
    """Fetch every internal link on the new site and report the ones that 404.

    WHY THIS IS SEPARATE FROM compare()
    Everything else here diffs a page against its predecessor. This cannot: a link
    that is broken on the new site is usually broken *because* the new site is
    different, so the live version is no help. Added 5 Aug after the page-by-page
    diff passed cleanly while 22 link targets were 404ing — statewide's 29 state
    pages each carried three or four dead "learn more" links inherited from a
    template written against the other brand's URLs. The comparison could not see
    it, because both sites were internally consistent with their own predecessors.
    """
    seen: dict[str, set[str]] = {}
    for path in paths:
        code, html = fetch(new + path, auth)
        if code != 200:
            continue
        for href in re.findall(r'href="(/[^"#?]*)"', html):
            if href.startswith('/wp-content') or href.startswith('//'):
                continue
            seen.setdefault(href, set()).add(path)

    out: list[Finding] = []

    def probe(target: str) -> tuple[str, int]:
        code, _ = fetch(new + target, auth, head=True)
        return target, code

    with concurrent.futures.ThreadPoolExecutor(max_workers=workers) as pool:
        for target, code in pool.map(probe, sorted(seen)):
            if code >= 400:
                srcs = sorted(seen[target])
                where = f'{len(srcs)} page(s)' if len(srcs) > 3 else ', '.join(srcs)
                out.append(Finding(FAIL, 'broken-internal-link', target,
                                   f'{code} — linked from {where}',
                                   {'sources': srcs}))
            elif code in (301, 302, 307, 308):
                out.append(Finding(INFO, 'redirecting-internal-link', target,
                                   f'{code} — an unnecessary hop; link the final URL'))
    return out


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--live', required=True, help='current production base URL, no trailing slash')
    ap.add_argument('--new', required=True, help='replacement base URL, no trailing slash')
    ap.add_argument('--user', help="'user:application password' for the new site (optional)")
    ap.add_argument('--limit', type=int, default=0, help='check only the first N paths (0 = all)')
    ap.add_argument('--workers', type=int, default=6, help='parallel page comparisons')
    ap.add_argument('--json', help='also write findings to this file')
    args = ap.parse_args()

    live, new = args.live.rstrip('/'), args.new.rstrip('/')

    print(f'Discovering URLs on {live} ...', flush=True)
    paths = rest_slugs(live, None)
    print(f'  {len(paths)} paths from the live REST API')
    if args.user:
        extra = [p for p in rest_slugs(new, args.user) if p not in paths]
        if extra:
            print(f'  {len(extra)} additional paths exist only on the new site (not checked '
                  f'for parity, but they are new content, not loss)')
    if not paths:
        print('No URLs discovered — is the REST API reachable?', file=sys.stderr)
        return 1
    if args.limit:
        paths = paths[:args.limit]

    findings: list[Finding] = []
    print(f'Comparing {len(paths)} pages ...', flush=True)
    with concurrent.futures.ThreadPoolExecutor(max_workers=args.workers) as pool:
        futures = {pool.submit(compare, p, live, new, args.user): p for p in paths}
        for i, fut in enumerate(concurrent.futures.as_completed(futures), 1):
            findings.extend(fut.result())
            if i % 10 == 0:
                print(f'  {i}/{len(paths)}', flush=True)

    print('Checking internal links on the new site ...', flush=True)
    findings.extend(check_internal_links(new, paths, args.user, args.workers))

    findings.sort(key=lambda f: (RANK[f.severity], f.category, f.path))

    print('\n' + '=' * 78)
    counts = Counter(f.severity for f in findings)
    print(f'{counts.get(FAIL, 0)} fail · {counts.get(WARN, 0)} warn · {counts.get(INFO, 0)} info')
    print('=' * 78)
    by_cat: dict[str, list[Finding]] = {}
    for f in findings:
        by_cat.setdefault(f'[{f.severity}] {f.category}', []).append(f)
    for cat, group in by_cat.items():
        print(f'\n{cat}  ({len(group)})')
        for f in group[:25]:
            print(f'    {f.path:52} {f.detail}')
        if len(group) > 25:
            print(f'    ... and {len(group) - 25} more')

    if args.json:
        with open(args.json, 'w') as fh:
            json.dump([asdict(f) for f in findings], fh, indent=1)
        print(f'\nWrote {args.json}')

    if not findings:
        print('\nNo differences found.')
    return 1 if counts.get(FAIL) else 0


if __name__ == '__main__':
    sys.exit(main())
