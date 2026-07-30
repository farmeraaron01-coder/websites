#!/usr/bin/env python3
"""
CFI content migration: production Divi -> staging Kadence.

For each published production URL: fetch the front end, strip Divi's layout
layer, lift any Key Takeaways block into meta, and upsert onto staging under the
production slug (URLs must not change at launch).

Skipped by design: the homepage and /get-a-quote/, which use bespoke templates
(front-page.php, page-get-a-quote.php) and must not receive migrated body copy.
"""
import json, os, random, re, subprocess, sys, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from divi2html import convert, extract_takeaways

SPW = os.environ['SPW']  # never hardcode; supplied at run time
UA = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36'
STG = 'https://new.californiafloodinsurance.com/wp-json/wp/v2'
SKIP = {'home', 'get-a-quote'}
GUIDE_MIN_WORDS = 400

audit = {r['slug']: r for r in json.load(open('audit.json'))}
inv = json.load(open('inventory.json'))


def api(method, url, payload=None):
    # The host's nginx cache serves cached responses for authenticated /wp-json/
    # GETs, ignoring the no-store, private headers WordPress sends. A stale index
    # read is what made the second pass create 20 "-slug-2" duplicates, so every
    # read carries a unique query string and an explicit no-cache header.
    if method == 'GET':
        url += ('&' if '?' in url else '?') + f'cb={random.randint(1, 10**9)}'
    cmd = ['curl', '-sS', '-u', f'AJFarmer:{SPW}', '-A', UA,
           '-H', 'Cache-Control: no-cache', '-H', 'Pragma: no-cache', '-X', method, url]
    if payload is not None:
        cmd += ['-H', 'Content-Type: application/json', '--data-binary', '@-']
        r = subprocess.run(cmd, input=json.dumps(payload), capture_output=True, text=True)
    else:
        r = subprocess.run(cmd, capture_output=True, text=True)
    try:
        return json.loads(r.stdout)
    except Exception:
        return {'_raw': r.stdout[:300]}


def fetch(url):
    return subprocess.run(['curl', '-sSL', '-A', UA, '--max-time', '45', url],
                          capture_output=True, text=True).stdout


def staging_total(t):
    """Authoritative count from X-WP-Total, used to prove the index is complete."""
    r = subprocess.run(['curl', '-sSI', '-u', f'AJFarmer:{SPW}', '-A', UA,
                        '-H', 'Cache-Control: no-cache',
                        f'{STG}/{t}?per_page=1&status=any&cb={random.randint(1, 10**9)}'],
                       capture_output=True, text=True)
    m = re.search(r'(?im)^x-wp-total:\s*(\d+)', r.stdout)
    return int(m.group(1)) if m else -1


def staging_index():
    """
    Build a slug -> id map, and refuse to run if it looks truncated.

    A silently short index is the one failure mode that corrupts the site
    instead of just erroring: every miss becomes a duplicate. So the count is
    cross-checked against X-WP-Total before any writes happen.
    """
    idx = {}
    for t in ('pages', 'posts'):
        seen, page = 0, 1
        while True:
            d = api('GET', f'{STG}/{t}?per_page=100&page={page}&status=any&_fields=id,slug')
            if not isinstance(d, list) or not d:
                break
            for p in d:
                idx[(t, p['slug'])] = p['id']
            seen += len(d)
            if len(d) < 100:
                break
            page += 1
        total = staging_total(t)
        print(f'  index: {t} indexed={seen} X-WP-Total={total}')
        if total >= 0 and seen < total:
            raise SystemExit(
                f'ABORT: indexed only {seen} of {total} {t}. A truncated index would '
                f'create duplicates instead of updating. Not writing anything.'
            )
    return idx


# Only real zone designations. "flood-zone-map" is an article about map changes,
# not a zone, and the first pass badged it "Flood Zone MAP".
ZONE = re.compile(r'^flood-zone-(a|ae|ah-and-ao|a-and-ae|v-and-ve|ve|x)$', re.I)


def zone_badge(slug, title):
    """Badge label for zone pages only. Cities already say their name in the h1."""
    m = ZONE.match(slug)
    if not m:
        return ''
    raw = m.group(1).replace('-and-', ' & ').replace('-', ' ').upper()
    return f'Flood Zone {raw}' 


def derive_risk(body):
    """
    Read the risk level out of the page's own words rather than asserting one.
    These are regulatory designations, so the page's existing copy is the only
    source used here — nothing is inferred.
    """
    t = re.sub(r'<[^>]+>', ' ', body).lower()
    # Whole body, not a 2,200-char head: Zone V/VE says "highest-hazard
    # designations FEMA assigns" up front and only reaches "high-risk" at char
    # 2,873, so the narrow window returned nothing for the most hazardous zone.
    if re.search(r'high[\s\-]risk|highest[\s\-]hazard', t):
        return 'high'
    if re.search(r'moderate[\s\-]to[\s\-]low|moderate[\s\-]risk', t):
        return 'moderate'
    if re.search(r'low[\s\-]risk|minimal flood hazard', t):
        return 'low'
    return ''


def main():
    idx = staging_index()
    report = []
    for i, it in enumerate(inv, 1):
        slug, kind = it['slug'], it['type']
        if slug in SKIP:
            report.append({'slug': slug, 'action': 'skipped (bespoke template)', 'words': 0})
            continue

        html = fetch(it['link'])
        if not html:
            report.append({'slug': slug, 'action': 'FETCH FAILED', 'words': 0})
            continue
        body = convert(html)
        body, takeaways = extract_takeaways(body)
        words = len(re.sub(r'<[^>]+>', ' ', body).split())
        a = audit.get(slug, {})

        badge = zone_badge(slug, it['title'])
        risk = derive_risk(body) if badge else ''

        meta = {
            '_cfi_takeaways': '\n'.join(re.sub(r'<[^>]+>', '', t).strip() for t in takeaways),
            '_cfi_badge': badge,
            '_cfi_risk': risk,
            'rank_math_title': a.get('title', ''),
            'rank_math_description': a.get('desc', ''),
        }
        payload = {
            'title': it['title'],
            'slug': slug,
            'status': 'publish',
            'content': body,
            'meta': meta,
        }
        if kind == 'pages':
            payload['template'] = 'template-guide.php' if words >= GUIDE_MIN_WORDS else ''

        existing = idx.get((kind, slug))
        if existing:
            res = api('POST', f'{STG}/{kind}/{existing}', payload)
            action = f'updated id={existing}'
        else:
            res = api('POST', f'{STG}/{kind}', payload)
            action = f"created id={res.get('id')}"
        ok = bool(res.get('id'))
        report.append({
            'slug': slug, 'type': kind, 'action': action if ok else f'FAILED {res}',
            'words': words, 'takeaways': len(takeaways), 'badge': badge, 'risk': risk,
            'template': payload.get('template', '(post)'),
        })
        print(f'  [{i:>2}/{len(inv)}] {slug[:42]:42} {words:>5}w  tk={len(takeaways)}  {action}', flush=True)
        time.sleep(0.3)

    json.dump(report, open('migration-report.json', 'w'), indent=1)
    print(f'\n  wrote migration-report.json ({len(report)} rows)')


if __name__ == '__main__':
    main()
