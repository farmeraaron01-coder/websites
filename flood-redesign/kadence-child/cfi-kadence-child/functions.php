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
	 * FILLED IN 4 AUG, and the condition inc/tags.php set has now been met.
	 *
	 * Today GA4 reaches this site from a gtag snippet hardcoded in the Divi
	 * header — present in the served HTML, no Site Kit involved, nothing to do
	 * with GTM. That snippet dies with the theme at cutover.
	 *
	 * The container cannot cover for it: GTM-PJQ72VK reports the Urgent warning
	 * "Missing Google tags — ... adding a Google tag to your container for each
	 * destination where you're sending data." Its GA4 event tags name
	 * G-FH3Q6GKNHH with no Google tag behind them. So without this constant,
	 * **GA4 stops collecting the moment the domain moves.**
	 *
	 * Setting it here rather than adding a Google tag in GTM is deliberate: a
	 * container change publishes immediately and would double-count every
	 * session on the *live Divi site* alongside its hardcoded snippet. This
	 * constant cannot fire until the new site answers the domain, so there is no
	 * double-count window at all.
	 */
	define( 'CFI_GA4_ID', 'G-FH3Q6GKNHH' );
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
	 * DELIBERATELY STILL EMPTY — one check away from being filled.
	 *
	 * California has the same exposure as statewide: its GA4 also comes from a
	 * hardcoded gtag snippet in the Divi header, so it also stops at cutover.
	 * The difference is evidence. Statewide's container was confirmed to have no
	 * Google tag; GTM-MZ6RZ94 has not been read, and it carries a separate
	 * "missing Google tag" warning about AW-1012143191 that may or may not mean
	 * a GA4 configuration tag exists.
	 *
	 * Filling this in blind is the one change here that could make measurement
	 * worse rather than better: if the container does hold a GA4 configuration
	 * tag, every session gets counted twice — two page_view hits, inflated
	 * users, conversion rate halved.
	 *
	 * TO RESOLVE: in GTM-MZ6RZ94, look for a "Google tag" or GA4 Configuration
	 * tag referencing G-3YMN51H7LE.
	 *   - none        → set this to 'G-3YMN51H7LE' before the flip.
	 *   - one exists  → leave empty; GA4 carries on through GTM.
	 * Either way, confirm real-time GA4 traffic after cutover. This is the
	 * measurement equivalent of the FAQ schema: silent if it breaks.
	 */
	define( 'CFI_GA4_ID', '' );  /* G-3YMN51H7LE — see the note above */

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
	$base = get_stylesheet_directory_uri() . '/assets/fonts/';
	echo '<link rel="preload" href="' . esc_url( $base . 'sourceserif4.woff2' ) . '" as="font" type="font/woff2" crossorigin>' . "\n";
	echo '<link rel="preload" href="' . esc_url( $base . 'inter.woff2' ) . '" as="font" type="font/woff2" crossorigin>' . "\n";

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
