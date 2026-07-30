<?php
/**
 * California Flood Insurance — Kadence child theme.
 *
 * Brand facts used across templates. For StatewideFloodInsurance.com,
 * change the constants below and the palette block at the top of
 * assets/css/tokens.css — nothing else differs between the sister sites.
 */

define( 'CFI_PHONE_DISPLAY', '855-CAL-FLOOD (225-3566)' );
define( 'CFI_PHONE_TEL', '8552253566' );
define( 'CFI_QUOTE_URL', 'https://www.californiafloodinsurance.com/get-a-quote/' );
define( 'CFI_LICENSE', 'CA License #0L75450' );
define( 'CFI_SISTER_NOTE', 'Looking for coverage outside California? <a href="https://www.statewidefloodinsurance.com/">Visit Statewide Flood Insurance</a>.' );

/**
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

add_action( 'wp_enqueue_scripts', function () {
	wp_enqueue_style(
		'cfi-tokens',
		get_stylesheet_directory_uri() . '/assets/css/tokens.css',
		array(),
		wp_get_theme()->get( 'Version' )
	);
} );

/**
 * Preload the two self-hosted font files so the headline never flashes.
 * These replace any Google Fonts CDN call — do not also enable Google
 * fonts in the Kadence customizer.
 */
add_action( 'wp_head', function () {
	$base = get_stylesheet_directory_uri() . '/assets/fonts/';
	echo '<link rel="preload" href="' . esc_url( $base . 'sourceserif4.woff2' ) . '" as="font" type="font/woff2" crossorigin>' . "\n";
	echo '<link rel="preload" href="' . esc_url( $base . 'inter.woff2' ) . '" as="font" type="font/woff2" crossorigin>' . "\n";
}, 5 );

/* Trim scripts WordPress ships that this site never uses. */
add_action( 'init', function () {
	remove_action( 'wp_head', 'print_emoji_detection_script', 7 );
	remove_action( 'wp_print_styles', 'print_emoji_styles' );
} );
