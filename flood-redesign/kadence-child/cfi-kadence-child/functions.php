<?php
/**
 * California Flood Insurance — Kadence child theme.
 *
 * Brand facts used across templates. For StatewideFloodInsurance.com,
 * change these five constants and the palette block at the top of
 * assets/css/tokens.css — nothing else differs between the sister sites.
 */

define( 'CFI_PHONE_DISPLAY', '855-CAL-FLOOD (225-3566)' );
define( 'CFI_PHONE_TEL', '8552253566' );
define( 'CFI_QUOTE_URL', 'https://www.californiafloodinsurance.com/get-a-quote/' );
define( 'CFI_LICENSE', 'CA License #0L75450' );
define( 'CFI_SISTER_NOTE', 'Looking for coverage outside California? <a href="https://www.statewidefloodinsurance.com/">Visit Statewide Flood Insurance</a>.' );

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
	echo '<link rel="preload" href="' . esc_url( $base . 'bricolage.woff2' ) . '" as="font" type="font/woff2" crossorigin>' . "\n";
	echo '<link rel="preload" href="' . esc_url( $base . 'publicsans.woff2' ) . '" as="font" type="font/woff2" crossorigin>' . "\n";
}, 5 );

/* Trim scripts WordPress ships that this site never uses. */
add_action( 'init', function () {
	remove_action( 'wp_head', 'print_emoji_detection_script', 7 );
	remove_action( 'wp_print_styles', 'print_emoji_styles' );
} );
