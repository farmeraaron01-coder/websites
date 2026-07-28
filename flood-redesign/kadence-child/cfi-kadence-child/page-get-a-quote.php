<?php
/**
 * Get a Quote — dedicated PPC landing page.
 * Applies automatically to the page with slug "get-a-quote".
 *
 * Deliberately standalone: no site nav to wander off through. wp_head()/wp_footer()
 * still run, so analytics, conversion tags, and the theme stylesheet all load.
 */
?><!doctype html>
<html <?php language_attributes(); ?>>
<head>
<meta charset="<?php bloginfo( 'charset' ); ?>">
<meta name="viewport" content="width=device-width, initial-scale=1">
<?php wp_head(); ?>
</head>
<body <?php body_class( 'cfi-home cfi-lp' ); ?>>

<header class="cfi-lp-bar">
	<a class="cfi-lp-brand" href="<?php echo esc_url( home_url( '/' ) ); ?>">
		<img src="<?php echo esc_url( get_stylesheet_directory_uri() . '/assets/img/logo.png' ); ?>" alt="" width="40" height="36">
		<span><b>California</b> Flood Insurance</span>
	</a>
	<a class="cfi-lp-phone" href="tel:<?php echo esc_attr( CFI_PHONE_TEL ); ?>">
		<small>Talk to a licensed specialist</small>
		<?php echo esc_html( CFI_PHONE_DISPLAY ); ?>
	</a>
</header>

<main id="main" class="cfi-lp-main">
	<div class="cfi-lp-grid">
		<section class="cfi-lp-form" aria-label="Flood quote request form">
			<h1>Start your flood quote</h1>
			<p class="cfi-lp-sub">Secure form &middot; about 2 minutes &middot; a licensed specialist compares available options and follows up promptly.</p>
			<div class="cfi-lp-embed">
				<script src="https://www.cognitoforms.com/f/seamless.js" data-key="8nmcIcFF1k6xZNCBaOzZxQ" data-form="5"></script>
			</div>
		</section>

		<aside class="cfi-lp-rail">
			<div class="cfi-lp-card">
				<p class="cfi-lp-stars" aria-label="Rated 4.9 out of 5"><span>&#9733;&#9733;&#9733;&#9733;&#9733;</span> 4.9 &middot; 900+ Google reviews</p>
				<ul class="cfi-qlist">
					<li>Up to 9 private flood markets + NFIP</li>
					<li>40,000+ property owners &amp; businesses helped</li>
					<li>Home, business &amp; HOA / condo</li>
					<li>No obligation, no automated spam</li>
				</ul>
				<p class="cfi-lp-note">We tell you honestly when the NFIP is the better fit. Options vary by property, underwriting eligibility, and carrier availability.</p>
			</div>
			<div class="cfi-lp-card cfi-lp-call">
				<p><b>Prefer to talk it through?</b></p>
				<a class="cfi-btn cfi-btn-cta" href="tel:<?php echo esc_attr( CFI_PHONE_TEL ); ?>">&#9742; <?php echo esc_html( CFI_PHONE_DISPLAY ); ?></a>
				<p class="cfi-lp-hours">Mon&ndash;Fri 8am&ndash;5pm PT</p>
			</div>
		</aside>
	</div>
</main>

<footer class="cfi-lp-foot">
	<span><?php echo esc_html( CFI_LICENSE ); ?> &middot; Independent flood-only agency since 2012</span>
	<span>Coverage is subject to underwriting, policy terms, conditions, and exclusions.</span>
</footer>

<?php wp_footer(); ?>
</body>
</html>
