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
	define( 'CFI_GA4_ID', '' );  /* G-FH3Q6GKNHH — see inc/tags.php before filling this in */
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
	define( 'CFI_GA4_ID', '' );  /* G-3YMN51H7LE — see inc/tags.php before filling this in */

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
