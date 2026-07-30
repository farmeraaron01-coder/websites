<?php
/**
 * Cognito Forms embeds via shortcode.
 *
 * Five production pages exist only to host an embed — /claims/, /agent-appointment/,
 * /staff-form/, /service-center/, /video/ — so the content migration produced
 * empty bodies for them: the converter strips <script> and <iframe> deliberately,
 * which is correct for the other 81 pages.
 *
 * A shortcode rather than raw markup in post content, because WordPress filters
 * script tags out of content depending on the saving user's capabilities and the
 * editor used — so a pasted embed can silently vanish on a later save. This keeps
 * the markup in the theme, under version control, and identical across both
 * sister sites.
 *
 * Usage:  [cfi_cognito form="31"]
 *         [cfi_cognito form="5" title="Start your flood quote"]
 *
 * The form key is shared across every CFI form; only the number changes.
 * Known forms: 5 = flood quote, 12 = service center, 31 = claims.
 */

define( 'CFI_COGNITO_KEY', '8nmcIcFF1k6xZNCBaOzZxQ' );

add_shortcode( 'cfi_cognito', function ( $atts ) {
	$a = shortcode_atts( array(
		'form'  => '',
		'title' => '',
		'key'   => CFI_COGNITO_KEY,
	), $atts, 'cfi_cognito' );

	// Form ids are numeric; refuse anything else rather than echo it into a tag.
	if ( ! preg_match( '/^\d+$/', (string) $a['form'] ) ) {
		return current_user_can( 'edit_posts' )
			? '<p><strong>[cfi_cognito]</strong> needs a numeric <code>form</code> attribute.</p>'
			: '';
	}

	$out = '<div class="cfi-embed">';
	if ( $a['title'] !== '' ) {
		$out .= '<h2 class="cfi-embed-title">' . esc_html( $a['title'] ) . '</h2>';
	}
	$out .= '<script src="https://www.cognitoforms.com/f/seamless.js"'
		. ' data-key="' . esc_attr( $a['key'] ) . '"'
		. ' data-form="' . esc_attr( $a['form'] ) . '"></script>';
	$out .= '<noscript><p>This form needs JavaScript. Call '
		. esc_html( CFI_PHONE_DISPLAY ) . ' and a licensed specialist will help you directly.</p></noscript>';
	$out .= '</div>';

	return $out;
} );
