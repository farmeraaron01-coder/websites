# jumpins.com — remaining SEO fixes (work order, 20 Aug 2026)

Five tasks. All content needed is inline below — nothing to look up.

## Ground rules

1. **SCOPE: San Diego only.** This site must not promote the Palm Desert office. No Coachella
   Valley geography, no `/palm-desert-office/` links, no Palm Desert phone number (760-610-6145).
   Statewide and county-wide framing is fine — it is the second location specifically that stays out.
2. **Do NOT touch the FAQ sections or FAQPage JSON-LD** on
   `/earthquake-insurance-california-2026/` or `/san-diego-flood-insurance-flood-zones/`. Those are
   done and verified. Leave the two curly-vs-straight apostrophe differences alone — Google
   requires marked-up content to be visible, not byte-identical.
3. **Do NOT redirect or 'validate fix' anything on cheapearthquakeinsurance.com.** Separate site,
   already verified clean.

---

## TASK 1 — Re-paste 15 meta descriptions (Yoast) · ~1 hr · HIGHEST VALUE

**Why:** the current live descriptions are 162–181 characters. Google truncates around 155–160,
so the tail of nearly every one is being cut. Each replacement below is measured and ≤160.

**How:** WP Admin → Pages (or Posts) → edit → Yoast SEO box at the bottom → SEO tab → replace
**SEO title** and **Meta description** → Update.

### Pages (11)

**/business-insurance/**

- Title: `Business Insurance California | Commercial Coverage for Every Industry | Jump Insurance`
- Description (150 chars): `Protect your California business with commercial insurance: BOP, workers' comp, cyber, commercial auto and more. Independent agents. Get a free quote.`

**/business-insurance/business-owners-policy/**

- Title: `Business Owners Policy (BOP) California | Bundled Business Insurance | Jump Insurance`
- Description (153 chars): `A Business Owners Policy bundles property and liability coverage in one affordable plan. California BOP specialists. Get the best rate for your business.`

**/business-insurance/workers-compensation/**

- Title: `Workers' Compensation Insurance California | Protect Your Employees | Jump Insurance`
- Description (140 chars): `California law requires workers' comp for most employers. Get compliant coverage that protects your employees and your business. Free quote.`

**/business-insurance/cyber-insurance/**

- Title: `Cyber Insurance for California Businesses | Data Breach & Liability Coverage | Jump Insurance`
- Description (151 chars): `Protect your California business from data breaches, ransomware, and cyber liability. Cyber insurance specialists at Jump Insurance. Get a quote today.`

**/business-insurance/commercial-auto/**

- Title: `Commercial Auto Insurance California | Fleet & Business Vehicle Coverage | Jump Insurance`
- Description (141 chars): `Company cars, vans and trucks need more than a personal auto policy. Commercial auto insurance in California. Free quote from Jump Insurance.`

**/business-insurance/professional-liability/**

- Title: `Professional Liability Insurance California | E&O Coverage | Jump Insurance`
- Description (145 chars): `Errors & Omissions and Professional Liability insurance protects California professionals from costly lawsuits. Independent agents, right policy.`

**/business-insurance/trucking-transportation/**

- Title: `Trucking & Transportation Insurance California | Commercial Truck Coverage | Jump Insurance`
- Description (151 chars): `California trucking insurance for owner-operators, fleets and freight carriers. Specialized commercial truck coverage. Get a quote from Jump Insurance.`

**/personal-insurance/life/**

- Title: `Life Insurance California | Term & Whole Life Policies | Jump Insurance`
- Description (139 chars): `Protect your family's financial future with life insurance in California. Compare term and whole life from top-rated carriers. Free quotes.`

**/contact-us/**

- Title: `Contact Jump Insurance Services | San Diego CA | Get a Free Quote`
- Description (146 chars): `Contact Jump Insurance Services in San Diego at 858-295-7242. Independent agents serving San Diego County and all of California. Get a free quote.`

**/contact-us/san-diego-office/**

- Title: `San Diego Insurance Agency | 7960 Silverton Ave | Jump Insurance Services`
- Description (145 chars): `Visit Jump Insurance at 7960 Silverton Ave STE 202, San Diego 92126. Independent agents for auto, home and business insurance. Call 858-295-7242.`

**/insurance-companies/**

- Title: `Our Insurance Carriers | Top-Rated Companies | Jump Insurance Services`
- Description (144 chars): `Jump Insurance works with top-rated California carriers to find you the best coverage at the lowest price. Independent agents — we work for you.`

> Note on `/contact-us/`: its live title currently reads "San Diego **& Palm Desert** CA".
> The replacement above removes Palm Desert. This is required, not optional.

### Existing posts (4)

**/rate-increases-and-non-renewals-are-the-new-normal/**

- Description (140 chars): `California insurers are raising rates and dropping policies at record levels. Why it's happening, and what you can do to keep your coverage.`

**/impacts-of-inflation-on-home-insurance/**

- Description (140 chars): `Inflation is driving up home insurance costs in California. How rising construction costs affect your premium, and what you can do about it.`

**/what-type-of-insurance-is-best-for-exotic-or-high-value-cars/**

- Description (138 chars): `Exotic and high-value cars need more than a standard auto policy. Which options best protect your classic or luxury vehicle in California.`

**/wildfire-insurance-in-california/**

- Description (145 chars): `California wildfires have changed the home insurance market. How to protect your property, what the FAIR Plan covers, and where to find coverage.`

---

## TASK 2 — Noindex 8 utility pages · ~30 min

**Why:** all of these currently return HTTP 200 with **no robots meta at all**, so they are
indexable and burning crawl budget. None should be in Google.

**How:** for each URL — edit the page → Yoast SEO box → **Advanced** tab →
"Allow search engines to show this page?" → **No** → Update.

- `/slide-anything-popup-preview/`
- `/agent-entered-commercial-fast-app/`
- `/agent-entered-personal-fast-app/`
- `/life-simple-form/`
- `/life-changes-survey/`
- `/commercial-fast-app/`
- `/commercial-renewal-fast-app/`
- `/personal-insurance/home-insurance/home-quote-form/`

**Also:** Yoast SEO → Search Appearance → **Archives** tab → set Author archives and Date
archives to Disabled. Then **Taxonomies** tab → Categories → "Show in search results" → No.

**Verify:** each URL's page source should contain `<meta name="robots" content="noindex...`

---

## TASK 3 — Replace /llms.txt · ~5 min

**Why:** the installed file opens with "San Diego and Palm Desert, California" (scope violation)
and is missing three entries.

**How:** replace the file at the site root (FTP or hosting file manager) so
`https://jumpins.com/llms.txt` serves exactly this:

```
# Jump Insurance Services
> Independent insurance agency in San Diego, California. We help individuals, families, and businesses find the best insurance coverage at the lowest cost from top-rated carriers.

## About
Jump Insurance Services is a full-service independent insurance agency licensed in California. We represent multiple top-rated carriers to find our clients the best coverage and rates for auto, home, life, and business insurance.

## Key Pages

### Personal Insurance
- https://jumpins.com/personal-insurance/auto-insurance/
- https://jumpins.com/personal-insurance/home-insurance/
- https://jumpins.com/personal-insurance/life/
- https://jumpins.com/personal-insurance/earthquake-insurance/
- https://jumpins.com/personal-insurance/flood-insurance/
- https://jumpins.com/personal-insurance/renters/
- https://jumpins.com/personal-insurance/condo-insurance/
- https://jumpins.com/personal-insurance/umbrella/
- https://jumpins.com/personal-insurance/motorcycle/
- https://jumpins.com/personal-insurance/boat-insurance/
- https://jumpins.com/personal-insurance/classic-car-insurance/
- https://jumpins.com/personal-insurance/mexico-auto-insurance/
- https://jumpins.com/personal-insurance/landlord-insurance/
- https://jumpins.com/personal-insurance/vacant-home-insurance/

### Business Insurance
- https://jumpins.com/business-insurance/
- https://jumpins.com/business-insurance/business-owners-policy/
- https://jumpins.com/business-insurance/workers-compensation/
- https://jumpins.com/business-insurance/commercial-auto/
- https://jumpins.com/business-insurance/cyber-insurance/
- https://jumpins.com/business-insurance/professional-liability/
- https://jumpins.com/business-insurance/trucking-transportation/

### Company
- https://jumpins.com/about-our-agency/
- https://jumpins.com/insurance-companies/
- https://jumpins.com/contact-us/san-diego-office/

### Insights
- https://jumpins.com/wildfire-insurance-in-california/
- https://jumpins.com/rate-increases-and-non-renewals-are-the-new-normal/
- https://jumpins.com/impacts-of-inflation-on-home-insurance/
- https://jumpins.com/what-type-of-insurance-is-best-for-exotic-or-high-value-cars/

### Related Sites
- https://www.cheapearthquakeinsurance.com/ — our dedicated California earthquake insurance quoting site
```

**Verify:** load `https://jumpins.com/llms.txt` — must be plain text (not HTML), must say
"in San Diego, California", must contain no `palm-desert` string.

---

## TASK 4 — Security headers + xmlrpc pingback · ~45 min

Two parts. Part A needs hosting/server access; Part B is WP-only.

### Part A — nginx (hand to whoever has server access)

Missing entirely right now: HSTS, X-Content-Type-Options, X-Frame-Options, Referrer-Policy.
Also `server: nginx/1.31.1` is disclosed in every response.

Add inside the main `https://jumpins.com` server block:

```nginx
add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;
add_header X-Content-Type-Options "nosniff" always;
add_header X-Frame-Options "SAMEORIGIN" always;
add_header Referrer-Policy "strict-origin-when-cross-origin" always;
```

And in the `http` block: `server_tokens off;`

Do **not** change the existing redirect rules — the www/http chain is already correct at 1 hop.

### Part B — WPCode snippet (removes xmlrpc pingback, adds header fallbacks)

The xmlrpc pingback link is still in `<head>`. Install **WPCode** (free) → Code Snippets →
Add New → **PHP Snippet** → paste below → set Active → Save.

Do **not** edit the parent Divi theme's `functions.php` — it is overwritten on theme update.

```php
<?php
/**
 * Jump Insurance SEO Fixes
 * Add this via WPCode plugin (Plugins > Code Snippets > Add New > PHP Snippet)
 * OR paste into child theme's functions.php
 *
 * Fixes: viewport user-scalable, xmlrpc pingback, security headers
 */

// 1. Fix viewport meta — remove user-scalable=0 restriction (WCAG 1.4.4)
add_filter( 'language_attributes', 'jumpins_fix_viewport', 10, 1 );
function jumpins_fix_viewport( $output ) {
    // Divi sets viewport via theme — override with a proper tag
    add_action( 'wp_head', 'jumpins_viewport_meta', 1 );
    return $output;
}
function jumpins_viewport_meta() {
    // Remove any existing viewport meta Divi outputs and replace with accessible version
    echo '<meta name="viewport" content="width=device-width, initial-scale=1.0">' . "\n";
}
// Remove Divi's viewport output to avoid duplication
add_action( 'after_setup_theme', function() {
    remove_action( 'wp_head', 'et_add_viewport_meta' );
});

// 2. Remove xmlrpc pingback link from <head>
remove_action( 'wp_head', 'xmlrpc_rsd' );
remove_action( 'wp_head', 'wp_generator' );  // Also hide WP version

// 3. Disable XML-RPC pingbacks entirely (keep REST API working)
add_filter( 'xmlrpc_methods', function( $methods ) {
    unset( $methods['pingback.ping'] );
    unset( $methods['pingback.extensions.getPingbacks'] );
    return $methods;
});

// 4. Add security headers
add_action( 'send_headers', 'jumpins_security_headers' );
function jumpins_security_headers() {
    if ( headers_sent() ) return;
    header( 'X-Content-Type-Options: nosniff' );
    header( 'X-Frame-Options: SAMEORIGIN' );
    header( 'Referrer-Policy: strict-origin-when-cross-origin' );
    header( 'X-XSS-Protection: 1; mode=block' );
    header( 'Permissions-Policy: camera=(), microphone=(), geolocation=(self)' );
}

// 5. Remove WordPress version from all outputs
add_filter( 'the_generator', '__return_empty_string' );
remove_action( 'wp_head', 'wp_generator' );
```

Note: the viewport fix in that snippet is already live by other means. It is idempotent — if it
causes a duplicate `<meta name="viewport">` tag, delete the `jumpins_fix_viewport` /
`jumpins_viewport_meta` functions and the `after_setup_theme` block, and keep the rest.

**Verify:** DevTools → Network → response headers show `strict-transport-security` and
`x-content-type-options: nosniff`; page source no longer contains `pingback`.

---

## TASK 5 — Add an H1 to one page · ~10 min

`/business-insurance/trucking-transportation/` renders **zero** `<h1>` tags. Every other business
insurance page has exactly one. Add one as the page's first heading:

```html
<h1>Trucking &amp; Transportation Insurance in California</h1>
```

Check whether this page is Divi Builder or classic editor first — posts on this site are classic
editor, but the business insurance pages are Divi-built. If Divi, set the existing top text
module's heading tag to H1 rather than adding raw markup.

**Verify:** page source contains exactly one `<h1>`.

---

## Final check when all five are done

- [ ] `https://jumpins.com/llms.txt` — plain text, no "Palm Desert"
- [ ] `/contact-us/` title has no "Palm Desert"
- [ ] All 15 meta descriptions ≤160 chars in page source
- [ ] All 8 utility pages show `noindex` in source
- [ ] Response headers include `strict-transport-security` + `x-content-type-options`
- [ ] No `pingback` string in homepage source
- [ ] `/business-insurance/trucking-transportation/` has one `<h1>`
- [ ] Earthquake + flood-zones FAQ sections still intact and unchanged
- [ ] GSC → submit `sitemap_index.xml`, request re-index on the pages touched
