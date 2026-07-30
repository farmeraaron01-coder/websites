<?php
/**
 * Mobile tap-to-call bar.
 *
 * Kadence swaps to its mobile header below 1024px, and the top bar — the only
 * place the phone number lives persistently — is part of the desktop header.
 * Measured: the top bar renders at 1025px and above, and has zero height below
 * that. So on every phone and tablet there was no persistent phone number,
 * which is backwards for an agency where calls convert.
 *
 * Rendered from the theme rather than a Customizer element because Kadence Free
 * permits only one HTML element across the whole header, and that slot is spent
 * on the top bar. This also keeps it in version control.
 */

add_action( 'wp_footer', function () {
	// The quote landing page is deliberately distraction-free and already leads
	// with a phone CTA in its rail; a second fixed bar would compete with the form.
	if ( is_page( 'get-a-quote' ) ) {
		return;
	}
	?>
	<div class="cfi-callbar" role="complementary" aria-label="Contact options">
		<a class="cfi-callbar-tel" href="tel:<?php echo esc_attr( CFI_PHONE_TEL ); ?>">
			<span aria-hidden="true">&#9742;</span> Call now
		</a>
		<a class="cfi-callbar-quote" href="<?php echo esc_url( CFI_QUOTE_URL ); ?>">
			Start my quote
		</a>
	</div>
	<?php
}, 20 );
