#!/usr/bin/env python3
"""
Deploy flood insurance content pages to live WordPress sites via REST API.

Reads HTML files from content/ directory, extracts metadata from comments,
and publishes as WordPress Posts with proper categories and SEO metadata.

SETUP:
  1. Create application passwords in WordPress admin for each site
  2. Set environment variables:
     - CFI_LIVE_USER and CFI_LIVE_PASS for californiafloodinsurance.com
     - SW_LIVE_USER and SW_LIVE_PASS for statewidefloodinsurance.com
  3. Run: python3 deploy-content-posts.py

USAGE:
  Deploy specific page:
    python3 deploy-content-posts.py --file california-flood-insurance-cost-by-zone.html --site cfi

  Deploy all to both sites:
    python3 deploy-content-posts.py

  Dry run (no publishing):
    python3 deploy-content-posts.py --dry-run
"""

import json, urllib.request, base64, os, sys, re, argparse
from pathlib import Path

SITES = {
    'cfi': {
        'url': 'https://californiafloodinsurance.com/wp-json/wp/v2/',
        'user_env': 'CFI_LIVE_USER',
        'pass_env': 'CFI_LIVE_PASS',
        'categories': ['flood-insurance-costs'],  # Adjust as needed
        'description': 'California Flood Insurance'
    },
    'sw': {
        'url': 'https://statewidefloodinsurance.com/wp-json/wp/v2/',
        'user_env': 'SW_LIVE_USER',
        'pass_env': 'SW_LIVE_PASS',
        'categories': ['flood-insurance-costs'],  # Adjust as needed
        'description': 'Statewide Flood Insurance'
    }
}

# Map content files to sites and categories
CONTENT_ROUTING = {
    'california-flood-insurance-cost-by-zone.html': {
        'site': 'cfi',
        'categories': ['flood-insurance-costs'],
        'featured_text': 'California flood insurance pricing by zone — complete breakdown'
    },
    'florida-flood-insurance-cost-rates.html': {
        'site': 'sw',
        'categories': ['flood-insurance-costs'],
        'featured_text': 'Florida flood insurance median cost $561/year'
    },
    'washington-flood-insurance-cost-rates.html': {
        'site': 'sw',
        'categories': ['flood-insurance-costs'],
        'featured_text': 'Washington flood insurance costs by zone'
    },
    'georgia-flood-insurance-cost-rates.html': {
        'site': 'sw',
        'categories': ['flood-insurance-costs'],
        'featured_text': 'Georgia flood insurance pricing'
    },
    'lenders-realtors-flood-insurance-solutions.html': {
        'site': 'sw',
        'categories': ['partnerships', 'flood-insurance-solutions'],
        'featured_text': 'Flood insurance solutions for lenders and realtors'
    }
}

UA = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36'


def extract_metadata(html_content):
    """Extract title, description, and canonical from HTML comment."""
    meta = {}

    # Look for HTML comment block at top
    match = re.search(r'<!--\s*(.*?)\s*-->', html_content, re.DOTALL)
    if match:
        comment = match.group(1)
        # Extract Title
        m = re.search(r'Title:\s*(.+)', comment)
        if m:
            meta['page_title'] = m.group(1).strip()

        # Extract Meta Description
        m = re.search(r'Meta Description:\s*(.+)', comment)
        if m:
            meta['meta_desc'] = m.group(1).strip()

        # Extract Canonical
        m = re.search(r'Canonical:\s*(.+)', comment)
        if m:
            meta['canonical'] = m.group(1).strip()

    return meta


def extract_h1(html_content):
    """Extract the H1 tag text."""
    match = re.search(r'<h1[^>]*>([^<]+)</h1>', html_content)
    return match.group(1).strip() if match else None


def extract_excerpt(html_content):
    """Extract first paragraph as excerpt."""
    match = re.search(r'<p[^>]*>([^<]+)</p>', html_content)
    return match.group(1).strip() if match else None


def extract_body_content(html_content):
    """Remove metadata comment and schema blocks, keep body content."""
    # Remove HTML metadata comment
    content = re.sub(r'<!--\s*(?:PAGE META|Title:|Meta|Canonical)[^-]*-->', '', html_content, flags=re.DOTALL)

    # Remove schema.org JSON-LD blocks
    content = re.sub(r'<script type="application/ld\+json">[^<]*</script>', '', content, flags=re.DOTALL)

    return content.strip()


def get_api_auth(site_key):
    """Get REST API authentication for a site."""
    site = SITES[site_key]
    user = os.environ.get(site['user_env'])
    password = os.environ.get(site['pass_env'])

    if not user or not password:
        raise ValueError(
            f"Missing credentials for {site_key}. Set {site['user_env']} and {site['pass_env']} environment variables."
        )

    auth_str = base64.b64encode(f'{user}:{password}'.encode()).decode()
    return 'Basic ' + auth_str


def api_call(site_key, path, method='GET', payload=None):
    """Make REST API call with error handling."""
    site = SITES[site_key]
    url = site['url'] + path
    auth = get_api_auth(site_key)

    headers = {
        'User-Agent': UA,
        'Authorization': auth,
        'Content-Type': 'application/json'
    }

    data = json.dumps(payload).encode() if payload else None

    try:
        req = urllib.request.Request(url, data=data, method=method, headers=headers)
        response = urllib.request.urlopen(req, timeout=60)
        return json.loads(response.read().decode())
    except urllib.error.HTTPError as e:
        error_body = e.read().decode()
        try:
            error_json = json.loads(error_body)
            raise Exception(f"API Error {e.code}: {error_json.get('message', error_body)}")
        except json.JSONDecodeError:
            raise Exception(f"API Error {e.code}: {error_body}")


def generate_slug(filename):
    """Convert filename to WordPress slug."""
    slug = filename.replace('.html', '')
    slug = slug.replace('_', '-')
    return slug.lower()


def find_category_id(site_key, category_slug):
    """Look up category by slug and return its ID."""
    try:
        result = api_call(site_key, f'categories?slug={category_slug}&_fields=id')
        if isinstance(result, list) and result:
            return result[0]['id']
    except Exception as e:
        print(f"  Warning: Could not find category '{category_slug}': {e}")
    return None


def publish_post(site_key, content_file, routing_config, dry_run=False):
    """Publish a content file as a WordPress post."""
    content_path = Path(__file__).parent.parent / 'content' / content_file

    if not content_path.exists():
        return {'status': 'FAILED', 'reason': f'File not found: {content_path}'}

    with open(content_path, 'r', encoding='utf-8') as f:
        html_content = f.read()

    # Extract metadata
    meta = extract_metadata(html_content)
    h1 = extract_h1(html_content)
    excerpt = extract_excerpt(html_content)
    body_content = extract_body_content(html_content)
    slug = generate_slug(content_file)

    # Build post payload
    payload = {
        'slug': slug,
        'title': meta.get('page_title', h1 or 'Untitled'),
        'content': body_content,
        'excerpt': excerpt or meta.get('meta_desc', ''),
        'status': 'publish',
        'author': 1,
        'meta': {
            'rank_math_title': meta.get('page_title', ''),
            'rank_math_description': meta.get('meta_desc', ''),
        }
    }

    # Add categories if available
    category_ids = []
    for cat_slug in routing_config.get('categories', []):
        cat_id = find_category_id(site_key, cat_slug)
        if cat_id:
            category_ids.append(cat_id)

    if category_ids:
        payload['categories'] = category_ids

    if dry_run:
        return {
            'status': 'DRY-RUN',
            'slug': slug,
            'title': payload['title'],
            'categories': category_ids,
            'excerpt': payload['excerpt'][:80] + '...'
        }

    # Check if post already exists
    try:
        existing = api_call(site_key, f'posts?slug={slug}&status=any&_fields=id')
        if isinstance(existing, list) and existing:
            # Update existing post
            post_id = existing[0]['id']
            result = api_call(site_key, f'posts/{post_id}', 'POST', payload)
            return {
                'status': 'UPDATED',
                'id': result.get('id'),
                'link': result.get('link'),
                'slug': result.get('slug')
            }
    except Exception as e:
        print(f"    Error checking for existing post: {e}")

    # Create new post
    try:
        result = api_call(site_key, 'posts', 'POST', payload)
        return {
            'status': 'CREATED',
            'id': result.get('id'),
            'link': result.get('link'),
            'slug': result.get('slug')
        }
    except Exception as e:
        return {'status': 'FAILED', 'reason': str(e)}


def main():
    parser = argparse.ArgumentParser(description='Deploy flood insurance content to WordPress')
    parser.add_argument('--file', help='Deploy specific file only')
    parser.add_argument('--site', choices=['cfi', 'sw'], help='Deploy to specific site only')
    parser.add_argument('--dry-run', action='store_true', help='Preview without publishing')
    args = parser.parse_args()

    files_to_deploy = CONTENT_ROUTING.keys()
    if args.file:
        if args.file in CONTENT_ROUTING:
            files_to_deploy = [args.file]
        else:
            print(f"Error: {args.file} not in routing config")
            sys.exit(1)

    print(f"\nDeploying flood insurance content pages {'(DRY-RUN)' if args.dry_run else ''}...\n")

    results = []
    for filename in files_to_deploy:
        routing = CONTENT_ROUTING[filename]
        site = routing['site']

        if args.site and args.site != site:
            continue

        print(f"  {filename:50} → {SITES[site]['description']}")

        result = publish_post(site, filename, routing, dry_run=args.dry_run)

        if result['status'] == 'DRY-RUN':
            print(f"    {result['status']}: {result['title']}")
            if result.get('categories'):
                print(f"    Categories: {result['categories']}")
        elif result['status'] in ['CREATED', 'UPDATED']:
            print(f"    {result['status']:7} id={result['id']} {result['link']}")
        else:
            print(f"    {result['status']:7} {result.get('reason', 'Unknown error')}")

        results.append({'file': filename, **result})

    if not args.dry_run:
        print(f"\n  Summary: {sum(1 for r in results if r['status'] in ['CREATED', 'UPDATED'])} published, "
              f"{sum(1 for r in results if r['status'] == 'FAILED')} failed")


if __name__ == '__main__':
    main()
