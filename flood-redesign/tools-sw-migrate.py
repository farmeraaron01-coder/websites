#!/usr/bin/env python3
"""Statewide migration: production Divi -> staging Kadence. Pages only —
every post is a CFI duplicate and stays behind by decision (July 30)."""
import json, os, random, re, subprocess, sys, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from divi2html import convert, extract_takeaways

SPW = os.environ['SPW']
UA = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36'
STG = 'https://staging.statewidefloodinsurance.com/wp-json/wp/v2'
# home/get-a-quote: bespoke templates. claims/service-center/agent-appointment/
# staff-form: already built with Cognito shortcodes. video: pending decision.
# floodguru: 25w noindexed stub. media: Divi demo placeholder junk.
SKIP = {'home','get-a-quote','claims','service-center','agent-appointment',
        'staff-form','video','floodguru','media'}
GUIDE_MIN_WORDS = 400
SUFFIX = re.compile(r'\s*[-|–]\s*Statewide Flood Insurance\s*$', re.I)

audit = {r['slug']: r for r in json.load(open('audit.json'))}
inv = [i for i in json.load(open('inventory.json')) if i['type'] == 'pages']

def api(method, url, payload=None):
    if method == 'GET':
        url += ('&' if '?' in url else '?') + f'cb={random.randint(1,10**9)}'
    cmd = ['curl','-sS','-u',f'AJFarmer:{SPW}','-A',UA,
           '-H','Cache-Control: no-cache','-H','Pragma: no-cache','-X',method,url]
    if payload is not None:
        cmd += ['-H','Content-Type: application/json','--data-binary','@-']
        r = subprocess.run(cmd, input=json.dumps(payload), capture_output=True, text=True)
    else:
        r = subprocess.run(cmd, capture_output=True, text=True)
    try:
        return json.loads(r.stdout)
    except Exception:
        return {'_raw': r.stdout[:300]}

def fetch(url):
    return subprocess.run(['curl','-sSL','-A',UA,'--max-time','45',url],
                          capture_output=True, text=True).stdout

def staging_total(t):
    r = subprocess.run(['curl','-sSI','-u',f'AJFarmer:{SPW}','-A',UA,
                        '-H','Cache-Control: no-cache',
                        f'{STG}/{t}?per_page=1&status=any&cb={random.randint(1,10**9)}'],
                       capture_output=True, text=True)
    m = re.search(r'(?im)^x-wp-total:\s*(\d+)', r.stdout)
    return int(m.group(1)) if m else -1

def staging_index():
    idx = {}
    for t in ('pages','posts'):
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
        print(f'  index: {t} indexed={seen} X-WP-Total={total}', flush=True)
        if total >= 0 and seen < total:
            raise SystemExit(f'ABORT: indexed only {seen} of {total} {t}.')
    return idx

def main():
    idx = staging_index()
    report = []
    todo = [i for i in inv if i['slug'] not in SKIP]
    print(f'  migrating {len(todo)} pages', flush=True)
    for i, it in enumerate(todo, 1):
        slug = it['slug']
        html = fetch(it['link'])
        if not html:
            report.append({'slug': slug, 'action': 'FETCH FAILED', 'words': 0})
            print(f'  [{i:>2}/{len(todo)}] {slug[:42]:42} FETCH FAILED', flush=True)
            continue
        body = convert(html)
        body, takeaways = extract_takeaways(body)
        words = len(re.sub(r'<[^>]+>',' ',body).split())
        a = audit.get(slug, {})
        title_meta = SUFFIX.sub('', a.get('title',''))
        meta = {
            '_cfi_takeaways': '\n'.join(re.sub(r'<[^>]+>','',t).strip() for t in takeaways),
            '_cfi_badge': '',
            '_cfi_risk': '',
            'rank_math_title': title_meta,
            'rank_math_description': a.get('desc',''),
        }
        payload = {'title': it['title'], 'slug': slug, 'status': 'publish',
                   'content': body, 'meta': meta,
                   'template': 'template-guide.php' if words >= GUIDE_MIN_WORDS else ''}
        existing = idx.get(('pages', slug))
        if existing:
            res = api('POST', f'{STG}/pages/{existing}', payload)
            action = f'updated id={existing}'
        else:
            res = api('POST', f'{STG}/pages', payload)
            action = f"created id={res.get('id')}"
        ok = bool(res.get('id'))
        got_slug = res.get('slug','')
        if ok and got_slug != slug:
            action += f' SLUG-MISMATCH:{got_slug}'
        report.append({'slug': slug, 'action': action if ok else f'FAILED {res}',
                       'words': words, 'takeaways': len(takeaways),
                       'template': payload['template']})
        print(f'  [{i:>2}/{len(todo)}] {slug[:42]:42} {words:>5}w tk={len(takeaways)} {action}', flush=True)
        time.sleep(0.3)
    json.dump(report, open('sw-migration-report.json','w'), indent=1)
    fails = [r for r in report if 'FAILED' in r['action'] or 'MISMATCH' in r['action']]
    print(f'\n  done: {len(report)} rows, {len(fails)} failures')

if __name__ == "__main__":
    main()
