<?php
/**
 * California Flood Insurance / Statewide Flood Insurance — Kadence child theme.
 *
 * ONE theme serves both sister sites. The brand is detected from the site's
 * home URL at runtime, so the identical theme zip installs on either site and
 * every future fix lands on both — no second copy to drift out of date.
 * Per-brand differences are exactly three surfaces:
 *   1. the constants below,
 *   2. the palette override in assets/css/brand-swfi.css (appended to the
 *      inlined tokens.css when the statewide brand is active),
 *   3. a handful of brand-conditional copy strings in templates, all keyed
 *      off CFI_BRAND.
 * Constant names keep the CFI_ prefix on both brands; renaming them across
 * every template would add churn with no behaviour change.
 */

define( 'CFI_BRAND', false !== strpos( (string) home_url(), 'statewidefloodinsurance' ) ? 'swfi' : 'cfi' );

if ( 'swfi' === CFI_BRAND ) {
	define( 'CFI_SITE_NAME', 'Statewide Flood Insurance' );
	define( 'CFI_PHONE_DISPLAY', '855-225-3566' );  /* no CAL-FLOOD vanity — that is California branding */
	define( 'CFI_PHONE_TEL', '8552253566' );
	define( 'CFI_QUOTE_URL', 'https://statewidefloodinsurance.com/get-a-quote/' );  /* non-www: statewide's canonical host */
	define( 'CFI_LICENSE', 'CA License #0L75450' );
	define( 'CFI_SISTER_NOTE', 'Insuring a California property? <a href="https://californiafloodinsurance.com/">Visit California Flood Insurance</a>.' );
	/* Hostname the tags may fire on, and the containers already running on
	   production. See inc/tags.php. GTM-MZ6RZ94 also appears on statewide
	   production as an orphaned <noscript> with no loader — a leftover from the
	   Divi clone. It is CFI's container and is deliberately not carried over. */
	define( 'CFI_PROD_HOST', 'statewidefloodinsurance.com' );
	define( 'CFI_GTM_ID', 'GTM-PJQ72VK' );
	/*
	 * EMPTY, AND IT MUST STAY EMPTY. Set to 'G-FH3Q6GKNHH' in 1.4.7 and reverted
	 * in 1.4.9 — the reasoning behind filling it in was wrong, and the record is
	 * kept here because the mistake is easy to repeat.
	 *
	 * The claim was that GTM-PJQ72VK holds no Google tag, inferred from its
	 * Urgent warning "Missing Google tags". Reading the published container
	 * settles it: **it holds two Google tags, one of them for G-FH3Q6GKNHH.**
	 * So GA4 was never going to stop at cutover, and printing gtag from the theme
	 * as well would have double-counted every session — two page_view hits,
	 * inflated users, conversion rate halved. Exactly the failure this constant
	 * was left empty to avoid in the first place.
	 *
	 * What the warning actually meant: the container fires Google Ads conversion
	 * tags for AW-1012143191 and has no Google tag for *that* destination. It was
	 * about Ads, not GA4. The same warning exists on GTM-MZ6RZ94 for the same
	 * reason.
	 *
	 * HOW TO CHECK THIS PROPERLY, rather than inferring from a warning — the
	 * published container is public, no credentials needed:
	 *
	 *   curl -s "https://www.googletagmanager.com/gtm.js?id=GTM-PJQ72VK" \
	 *     | grep -o '"function":"__googtag"' | wc -l
	 *
	 * `__googtag` is a Google tag (GA4 configuration); `__gaawe` is a GA4 event
	 * tag; `__awct` is an Ads conversion. Read the container, do not infer it.
	 */
	define( 'CFI_GA4_ID', '' );  /* G-FH3Q6GKNHH — already configured in GTM-PJQ72VK */
	/*
	 * Same widget as CFI staging deliberately: both brands share one Google
	 * Business Profile, and this widget copy is the one already tuned there
	 * (rotate interval 0 so no autoplay CLS, rich snippet off). If statewide
	 * ever needs its own styling, duplicate the widget in Trust Index and
	 * swap this ID — the review pool is unaffected.
	 */
	define( 'CFI_TRUSTINDEX_ID', 'bcdff9477ef19568e30684fd16d' );
	/* The shared GBP is named after the CFI DBA, so that is where a reviews
	   search actually lands. */
	define( 'CFI_GOOGLE_REVIEWS_URL', 'https://www.google.com/search?q=California+Flood+Insurance+Services+reviews' );
} else {
	define( 'CFI_SITE_NAME', 'California Flood Insurance' );
	define( 'CFI_PHONE_DISPLAY', '855-CAL-FLOOD (225-3566)' );
	define( 'CFI_PHONE_TEL', '8552253566' );
	/*
	 * Non-www on both hosts. Production canonicalises to the bare domain
	 * (www.californiafloodinsurance.com 301s to californiafloodinsurance.com,
	 * and its canonical tag agrees), so a www URL here would put a redirect hop
	 * in front of the most important click on the site.
	 */
	define( 'CFI_QUOTE_URL', 'https://californiafloodinsurance.com/get-a-quote/' );
	define( 'CFI_LICENSE', 'CA License #0L75450' );
	define( 'CFI_SISTER_NOTE', 'Looking for coverage outside California? <a href="https://statewidefloodinsurance.com/">Visit Statewide Flood Insurance</a>.' );
	/* See inc/tags.php. These are the containers already live on production —
	   nothing new is created at cutover. */
	define( 'CFI_PROD_HOST', 'californiafloodinsurance.com' );
	define( 'CFI_GTM_ID', 'GTM-MZ6RZ94' );
	/*
	 * EMPTY, and now confirmed correct rather than merely cautious.
	 *
	 * GTM-MZ6RZ94 holds a Google tag for G-3YMN51H7LE — read from the published
	 * container on 4 Aug, not inferred from a warning. GA4 therefore continues
	 * through GTM after cutover, and this must stay empty or every session is
	 * counted twice.
	 *
	 * Leaving it empty pending evidence was the right call. The evidence, when it
	 * finally got read, said do nothing.
	 */
	define( 'CFI_GA4_ID', '' );  /* G-3YMN51H7LE — already configured in GTM-MZ6RZ94 */

	/*
	 * Trust Index review widget.
	 *
	 * Both sister sites are the same parent company and draw from one Google
	 * Business Profile, so the review pool is shared. A widget ID identifies a
	 * *display configuration*, not a review source — duplicating a widget in
	 * Trust Index does not split or copy reviews. So either site may reuse this
	 * ID, or point at its own styled copy of the same feed.
	 *
	 * Set to '' to render the section without the live feed (the rating block
	 * and the "read our reviews on Google" fallback still show).
	 */
	define( 'CFI_TRUSTINDEX_ID', 'bcdff9477ef19568e30684fd16d' );
	define( 'CFI_GOOGLE_REVIEWS_URL', 'https://www.google.com/search?q=California+Flood+Insurance+Services+reviews' );
}

/**
 * Territory the business serves. The DBA registered with the California
 * Department of Insurance — California Flood Insurance Services — writes
 * nationwide, so both sister sites claim the same area.
 */
define( 'CFI_AREA_SERVED', 'United States' );

/**
 * Keep the GTM container off the critical path.
 *
 * Measured on the live California homepage the morning after cutover: the
 * container costs 490 KiB and 909 ms of blocking time, holds the main thread for
 * 1,471 ms of script evaluation, and delays the hero image — which is marked
 * `fetchpriority="high"` — by 2.1 seconds. Mobile performance went from 98 on
 * staging, where the host gate kept tags off, to 54 live.
 *
 * Deferring loads the container on first interaction, or on browser idle capped
 * at CFI_TAGS_DELAY_MS. `dataLayer` is an array from the first line of the head,
 * so anything pushed before the container arrives queues and replays — no event
 * is lost. Full reasoning, and the honest trade-off about instant bounces, is in
 * the docblock above the loader in inc/tags.php.
 *
 * Set to false to load in the head immediately, as before 1.5.1.
 */
/*
 * DEFAULT OFF — the deferral was tried twice on 7 Aug and made things worse.
 *
 * 1.5.1 deferred to browser idle with a 2500 ms ceiling: mobile 54 → 66, because
 * Lighthouse waits for network quiet and the ceiling fired inside its window.
 *
 * 1.5.2 went interaction-only. That was worse still: **desktop PSI fell 82 → 72
 * and local mobile TBT rose from 760 ms to 2,550 ms.** The cause is that
 * Lighthouse scrolls the page itself during gathering, to capture full-page
 * screenshots and trigger lazy content. That trips the scroll listener, so the
 * container loads regardless — but now it executes in the middle of the trace
 * rather than before first paint, and mid-trace execution costs more TBT than
 * early execution does.
 *
 * The only trigger set Lighthouse would not trip is pointerdown/keydown/
 * touchstart alone, with no scroll. That is rejected on purpose: a visitor who
 * reads an article and scrolls but never taps would record no pageview at all,
 * which is most readers, and it is plainly gaming the metric rather than making
 * the page faster.
 *
 * So the container loads in the head as it always did, and the honest number is
 * desktop 82 / mobile 60. The code is kept because deferral may still be the
 * right call for CrUX *field* metrics — real visitors are not Lighthouse and do
 * benefit from tags not competing with the hero image. That is worth revisiting
 * once the new site has 28 days of field data, which it will not have until
 * early September.
 *
 * THE ACTUAL FIX IS THE CONTAINER, NOT THE LOADER. GTM-MZ6RZ94 ships 490 KiB of
 * which PSI reports ~198 KiB unused. A lean container is nearer 100 KiB.
 * Trimming it improves lab and field together, loses no data, and needs no
 * cleverness here. ACCOUNTS.md already lists the dead tags.
 */
define( 'CFI_TAGS_DEFER', false );

/**
 * The idle-load ceiling, in milliseconds. **0 means interaction-only.**
 *
 * This one number is a business decision, not a technical one, so the choice is
 * written down rather than buried.
 *
 *   0     Container loads ONLY on the visitor's first pointerdown, keydown,
 *         touchstart, scroll, wheel or mousemove.
 *   2500  Container also loads on browser idle after at most 2.5s.
 *
 * WHY 2500 SCORED BADLY. Measured on the live homepage after 1.5.1 shipped with
 * 2500: mobile performance went 54 → **66**, not the high 80s expected. The
 * reason is that Lighthouse waits for network quiet, so a 2.5s idle ceiling
 * fires comfortably inside its measurement window — GTM still landed, still cost
 * 491 KiB, still burned 660 ms of blocking time. Deferring moved the container
 * later without moving it out.
 *
 * WHY 0 SCORES WELL, AND WHAT THAT DOES AND DOES NOT MEAN. Lighthouse never
 * scrolls or taps, so at 0 the container never loads during a lab run and TBT
 * collapses. Two things are true about that at once and both belong on the
 * record:
 *
 *   Genuine improvement — real visitors load the container only after the page
 *   has already painted, so their LCP and first impression improve for real.
 *   Google ranks on CrUX *field* data, and LCP happens before most interactions,
 *   so this is a real field-metric gain rather than only a lab one.
 *
 *   Partly gaming the metric — the lab number no longer includes a cost real
 *   users still pay the moment they interact. A 490 KiB container is 490 KiB
 *   whichever second it arrives.
 *
 * THE DATA COST. At 0, a visitor who lands and leaves without scrolling,
 * tapping or typing records **no pageview at all**. On mobile that is a thin
 * slice — scroll fires on nearly any real visit — but it is not zero, and GA4
 * sessions will read lower than they did in early August. Conversions are
 * unaffected: submitting a form requires interaction, which loads the container
 * first, and queued dataLayer pushes replay on load either way.
 *
 * THE FIX THAT HELPS EVERYONE. Neither value makes the container smaller. At
 * 490 KiB it is roughly five times a lean container, and ACCOUNTS.md already
 * found dead tags across these properties. Trimming GTM-MZ6RZ94 is the only
 * change here that makes the site faster for a visitor who actually engages.
 */
define( 'CFI_TAGS_DELAY_MS', 0 );

/*
 * Review figures for the business schema. Must stay in step with what the pages
 * actually display — the Trustindex widget and the quote landing page's
 * "4.9 · 900+ Google reviews". Matches what California's live site has emitted
 * for years. See the aggregateRating block in the rank_math/json_ld filter for
 * why this is parity rather than an expectation of review stars.
 */
define( 'CFI_RATING_VALUE', '4.9' );
define( 'CFI_RATING_COUNT', '900' );

/*
 * Author headshot, as a site-relative path — the same filename is uploaded on
 * both brands, so one constant covers them and inc/schema.php makes it absolute
 * against home_url(). Feeds the Person entity's image property.
 *
 * Chosen by Aaron on 4 Aug from the two in the design-handoff folder. Do NOT
 * point this at the older Divi-era headshot: it is retired, and it lived only on
 * the production domain, so referencing it would break at the docroot swap.
 */
define( 'CFI_AUTHOR_IMAGE', '/wp-content/uploads/2026/08/aaron-farmer-flood-insurance-specialist.jpg' );

/*
 * Foundation-type reference diagram, shown as an expander on the quote page.
 * Same filename on both brands. Relative for the same reason as the headshot.
 *
 * The Divi original opened this in a JavaScript popup window, which mobile
 * browsers block or handle badly — on the page carrying the ad spend. Here it
 * expands inline instead, so nobody leaves a part-filled application.
 */
define( 'CFI_FOUNDATION_IMAGE', '/wp-content/uploads/2026/08/foundation-type-examples.jpg' );

/**
 * Fill the two gaps Rank Math's free tier cannot express on the
 * Organization / LocalBusiness node.
 *
 * 1. areaServed — no UI field exists for it at all.
 * 2. openingHoursSpecification — the free tier emits the older comma-joined
 *    `openingHours` string. Google parses both, so this is robustness rather
 *    than a fix, but the object form is unambiguous.
 *
 * Rank Math stays the single source of truth: the hours are parsed out of
 * whatever it already emitted, so changing them in Local SEO settings still
 * works and nothing is duplicated here. If a line does not parse, the original
 * string is left untouched rather than silently dropped.
 */
add_filter( 'rank_math/json_ld', function ( $data, $jsonld ) {
	foreach ( $data as $key => $node ) {
		if ( empty( $node['@type'] ) ) {
			continue;
		}
		$types = (array) $node['@type'];
		if ( ! array_intersect( $types, array( 'Organization', 'LocalBusiness', 'InsuranceAgency' ) ) ) {
			continue;
		}

		$data[ $key ]['areaServed'] = array(
			'@type' => 'Country',
			'name'  => CFI_AREA_SERVED,
		);

		/*
		 * aggregateRating — restoring parity, with a caveat worth knowing.
		 *
		 * Found 4 Aug by tools/preflight.py: California's live site emits an
		 * InsuranceAgency node carrying aggregateRating 4.9 from 900 reviews, and
		 * the new site emitted none. Rank Math's free tier has no field for it.
		 *
		 * THE CAVEAT: Google has not shown review stars for self-serving
		 * LocalBusiness ratings since 2019, so this almost certainly produces no
		 * rich result. It is added because (a) it matches what production has
		 * emitted for years, so it changes nothing about the site's current
		 * standing, and (b) AI answer engines do read it. It is NOT added on the
		 * expectation of stars returning.
		 *
		 * The figures must keep matching what the page actually shows — the
		 * Trustindex widget renders the real Google reviews, and the quote
		 * landing page states "4.9 · 900+ Google reviews". If those diverge,
		 * update the constants or drop this block; a rating the page cannot
		 * substantiate is the version of this that causes problems.
		 */
		if ( defined( 'CFI_RATING_VALUE' ) && defined( 'CFI_RATING_COUNT' )
			&& CFI_RATING_VALUE && CFI_RATING_COUNT && empty( $node['aggregateRating'] ) ) {
			$data[ $key ]['aggregateRating'] = array(
				'@type'       => 'AggregateRating',
				'ratingValue' => (string) CFI_RATING_VALUE,
				'reviewCount' => (string) CFI_RATING_COUNT,
				'bestRating'  => '5',
			);
		}

		if ( empty( $node['openingHours'] ) ) {
			continue;
		}

		$spec = array();
		foreach ( (array) $node['openingHours'] as $line ) {
			if ( ! preg_match( '/^([A-Za-z,]+)\s+(\d{2}:\d{2})-(\d{2}:\d{2})$/', trim( $line ), $m ) ) {
				$spec = array();
				break;
			}
			$spec[] = array(
				'@type'     => 'OpeningHoursSpecification',
				'dayOfWeek' => array_map( 'trim', explode( ',', $m[1] ) ),
				'opens'     => $m[2],
				'closes'    => $m[3],
			);
		}

		if ( $spec ) {
			$data[ $key ]['openingHoursSpecification'] = $spec;
			unset( $data[ $key ]['openingHours'] );
		}
	}

	return $data;
}, 20, 2 );

/* Interior pages: TOC engine, takeaways, byline, and the REST-visible meta. */
require_once get_stylesheet_directory() . '/inc/interior.php';

/* Mobile tap-to-call bar — the desktop top bar's phone number stops at 1024px. */
require_once get_stylesheet_directory() . '/inc/callbar.php';

/* [cfi_cognito form="31"] — embeds for the pages that exist only to host a form. */
require_once get_stylesheet_directory() . '/inc/cognito.php';

/* [cfi_video] click-to-play facade + VideoObject, and [cfi_videos] for the hub. */
require_once get_stylesheet_directory() . '/inc/video.php';

/* One-time .htaccess cache-header install — see inc/htaccess.php for why. */
require_once get_stylesheet_directory() . '/inc/htaccess.php';

/* GTM / GA4, gated to the production hostname — see inc/tags.php for why. */
require_once get_stylesheet_directory() . '/inc/tags.php';

/* FAQPage JSON-LD, read off the existing Q&A markup — see inc/schema.php for why. */
require_once get_stylesheet_directory() . '/inc/schema.php';

/**
 * tokens.css is inlined into the page rather than enqueued as a file.
 *
 * PSI measured it as a ~450ms render-blocking request on mobile — the largest
 * single member of the six-stylesheet chain that sets the FCP floor. Inlining
 * removes the request entirely; at ~10KB gzipped the payload cost per page is
 * far below the round-trips it saves, and the nginx page cache absorbs the
 * per-request file read.
 *
 * Two details that matter:
 * - The @font-face rules use url(../fonts/…), relative to the CSS file's
 *   location. Inlined into HTML those would resolve against the page URL and
 *   silently break both fonts, so they are rewritten to absolute URLs first.
 * - Comments are stripped at print time only — the file on disk stays fully
 *   documented, the served HTML carries none of it.
 *
 * If the file read ever fails, it falls back to the old enqueue rather than
 * shipping an unstyled page.
 */
add_action( 'wp_enqueue_scripts', function () {
	$path = get_stylesheet_directory() . '/assets/css/tokens.css';
	$css  = is_readable( $path ) ? file_get_contents( $path ) : false;

	/* Statewide: append the palette override so its :root tokens win.
	   Order matters — the override must come after tokens.css. */
	$brand_path = get_stylesheet_directory() . '/assets/css/brand-swfi.css';
	$brand_css  = ( 'swfi' === CFI_BRAND && is_readable( $brand_path ) ) ? file_get_contents( $brand_path ) : '';

	if ( false === $css || '' === trim( $css ) ) {
		wp_enqueue_style(
			'cfi-tokens',
			get_stylesheet_directory_uri() . '/assets/css/tokens.css',
			array(),
			wp_get_theme()->get( 'Version' )
		);
		if ( '' !== $brand_css ) {
			wp_enqueue_style(
				'cfi-brand',
				get_stylesheet_directory_uri() . '/assets/css/brand-swfi.css',
				array( 'cfi-tokens' ),
				wp_get_theme()->get( 'Version' )
			);
		}
		return;
	}

	$css .= "\n" . $brand_css;

	$css = str_replace( 'url(../', 'url(' . get_stylesheet_directory_uri() . '/assets/', $css );
	$css = preg_replace( '~/\*.*?\*/~s', '', $css );
	$css = preg_replace( '~\n{2,}~', "\n", trim( $css ) );

	wp_register_style( 'cfi-tokens', false, array(), null );
	wp_enqueue_style( 'cfi-tokens' );
	wp_add_inline_style( 'cfi-tokens', $css );
}, 20 );

/**
 * Preload the two self-hosted font files so the headline never flashes.
 * These replace any Google Fonts CDN call — do not also enable Google
 * fonts in the Kadence customizer.
 */
add_action( 'wp_head', function () {
	/*
	 * Filenames carry a version suffix and MUST match the two @font-face rules
	 * in assets/css/tokens.css. Fonts are served immutable for a year (see
	 * inc/htaccess.php), so a changed font at an unchanged URL never reaches a
	 * returning visitor. New bytes always mean a new filename — bump it in both
	 * places. The reasoning is written out in full in tokens.css.
	 */
	$base = get_stylesheet_directory_uri() . '/assets/fonts/';
	echo '<link rel="preload" href="' . esc_url( $base . 'sourceserif4-v2.woff2' ) . '" as="font" type="font/woff2" crossorigin>' . "\n";
	echo '<link rel="preload" href="' . esc_url( $base . 'inter-v2.woff2' ) . '" as="font" type="font/woff2" crossorigin>' . "\n";

	/*
	 * Preload the hero poster on the front page only — it is the LCP element.
	 * PageSpeed Insights measured its LCP breakdown as 70ms TTFB, 460ms resource
	 * load *delay*, 530ms load, 210ms render: the delay was the largest single
	 * component, because the image sits inside a <picture> that the browser only
	 * discovers after the six render-blocking stylesheets resolve.
	 *
	 * type="image/webp" means browsers without WebP support skip the hint rather
	 * than fetching something they cannot use, and only the WebP is preloaded so
	 * the JPEG fallback is never double-downloaded.
	 */
	if ( is_front_page() ) {
		echo '<link rel="preload" as="image" href="'
			. esc_url( get_stylesheet_directory_uri() . '/assets/media/hero-poster.webp' )
			. '" type="image/webp" fetchpriority="high">' . "\n";
	}
}, 5 );

/* Trim scripts WordPress ships that this site never uses. */
add_action( 'init', function () {
	remove_action( 'wp_head', 'print_emoji_detection_script', 7 );
	remove_action( 'wp_print_styles', 'print_emoji_styles' );
} );

/**
 * 404 out-of-range pagination on the static front page.
 *
 * FOUND 10 Aug in Search Console's Page indexing report on California: 440 URLs
 * under "Soft 404". The site has 62 URLs in its sitemap and its Divi predecessor
 * had 86, so a four-figure count of non-indexed URLs cannot come from real pages.
 * Probing the live site found an unbounded URL space:
 *
 *   /page/2/  /page/99/  /page/500/  → all HTTP 200, all serving the homepage,
 *                                      all emitting robots "index"
 *
 * A static front page has no pagination, so every one of those is a distinct
 * indexable URL returning identical content. Googlebot can enumerate them
 * forever, and "200 with content that isn't the requested resource" is precisely
 * what earns a Soft 404 verdict. The canonical does point at `/`, which is why
 * this leaked as Soft 404 rather than as duplicate content, but a canonical is a
 * hint — it does not stop the crawl, and crawl spent here is crawl not spent on
 * the 62 pages that matter.
 *
 * SCOPED TO THE FRONT PAGE DELIBERATELY, AND VERIFIED BEFORE WRITING. Real
 * pagination elsewhere already behaves correctly and must not be touched:
 *
 *   /insights/page/2/                         → 200, correct     (leave alone)
 *   /insights/page/9/                         → 404, correct     (WP handles it)
 *   /category/flood-insurance-guides/page/2/  → 200, correct     (leave alone)
 *
 * WordPress 404s an over-range *archive* on its own because the main query comes
 * back empty. It does not do so on a static front page, because that query asks
 * for one page by ID and finds it whatever `paged` says. So the narrow condition
 * is the whole bug, and a broader guard keyed on max_num_pages would risk
 * breaking the archives above — the main query on a static page reports
 * max_num_pages of 1 even when a loop inside the template has more.
 *
 * `paged` is the archive-pagination var. Post-internal pagination from
 * <!--nextpage--> uses `page`, which this leaves untouched.
 */
add_action( 'template_redirect', function () {
	if ( ! is_front_page() || is_feed() || (int) get_query_var( 'paged' ) < 2 ) {
		return;
	}

	global $wp_query;
	$wp_query->set_404();
	status_header( 404 );
	nocache_headers();
} );
