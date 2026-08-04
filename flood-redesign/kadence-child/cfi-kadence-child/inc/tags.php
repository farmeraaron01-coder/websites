<?php
/**
 * Google Tag Manager (and optionally GA4) — brand-scoped, host-gated.
 *
 * WHY THE THEME AND NOT A PLUGIN
 * Production put GA4 in the Site Kit plugin and hand-placed the GTM snippet in
 * the Divi header. Site Kit is not in the new five-plugin stack, so the tags
 * need a home that survives the theme swap and does not add a plugin whose only
 * job is to print eight lines of JavaScript. Keeping them here also means the
 * IDs live next to the other brand constants instead of in a database setting
 * nobody remembers to check.
 *
 * NOTHING NEW IS CREATED AT CUTOVER
 * These are the SAME containers already running on production. A GTM container
 * ID is not bound to a domain — the snippet reports whatever hostname it is
 * loaded on — so moving the site does not require a new container, a new
 * property, or any change inside GTM. History, tags, triggers, and Ads
 * conversions all carry over untouched.
 *
 * THE HOST GATE
 * While the new sites sit on staging hostnames, live tags would send live data:
 * harmless for GA4 pageviews, NOT harmless for Google Ads conversion tags,
 * where one test submission of the quote form counts as a real lead and feeds
 * Smart Bidding a fake conversion. So the snippet prints only on the production
 * hostname. At cutover the hostname becomes the production one and tagging
 * starts by itself — there is no launch step to forget.
 *
 * To verify on staging: append ?cfi_tags=1 while logged in as an administrator.
 * That prints the snippet for that one request so Tag Assistant / GTM Preview
 * can confirm it fires. Logged-out visitors and crawlers can never trip it.
 */

/**
 * Should tagging print for this request?
 */
function cfi_tags_active() {
	if ( is_admin() || wp_doing_ajax() || ( defined( 'REST_REQUEST' ) && REST_REQUEST ) ) {
		return false;
	}

	// Administrator override for verification on a staging hostname.
	if ( isset( $_GET['cfi_tags'] ) && current_user_can( 'manage_options' ) ) {
		return true;
	}

	$host = strtolower( (string) ( $_SERVER['HTTP_HOST'] ?? '' ) );
	$host = preg_replace( '/^www\./', '', $host );
	$host = preg_replace( '/:\d+$/', '', $host );

	return $host === CFI_PROD_HOST;
}

/**
 * GTM loader, plus the GA4 config when one is set. Priority 2 so the container
 * initialises before anything else in the head that might push to dataLayer.
 */
add_action( 'wp_head', function () {
	if ( ! cfi_tags_active() ) {
		return;
	}

	if ( CFI_GTM_ID ) {
		?>
<!-- Google Tag Manager -->
<script>(function(w,d,s,l,i){w[l]=w[l]||[];w[l].push({'gtm.start':new Date().getTime(),event:'gtm.js'});var f=d.getElementsByTagName(s)[0],j=d.createElement(s),dl=l!='dataLayer'?'&l='+l:'';j.async=true;j.src='https://www.googletagmanager.com/gtm.js?id='+i+dl;f.parentNode.insertBefore(j,f);})(window,document,'script','dataLayer','<?php echo esc_js( CFI_GTM_ID ); ?>');</script>
<!-- End Google Tag Manager -->
		<?php
	}

	/*
	 * GA4 direct — OFF by default, and deliberately so.
	 *
	 * On production GA4 arrives via Site Kit, separately from GTM. If the GTM
	 * container ALSO holds a GA4 configuration tag, printing gtag here as well
	 * double-counts every session: two page_view hits per pageview, sessions and
	 * users inflated, conversion rate halved. Which of those is true can only be
	 * answered by opening the container.
	 *
	 * So: leave CFI_GA4_ID empty and let GA4 run through GTM (one tag system,
	 * one place to look). Fill it in ONLY after confirming the container has no
	 * GA4 configuration tag.
	 */
	if ( CFI_GA4_ID ) {
		?>
<script async src="https://www.googletagmanager.com/gtag/js?id=<?php echo rawurlencode( CFI_GA4_ID ); ?>"></script>
<script>window.dataLayer=window.dataLayer||[];function gtag(){dataLayer.push(arguments);}gtag('js',new Date());gtag('config','<?php echo esc_js( CFI_GA4_ID ); ?>');</script>
		<?php
	}
}, 2 );

/**
 * The noscript half of the GTM snippet. Only reaches visitors with JavaScript
 * disabled; Google still expects it present.
 */
add_action( 'wp_body_open', function () {
	if ( ! CFI_GTM_ID || ! cfi_tags_active() ) {
		return;
	}
	?>
<!-- Google Tag Manager (noscript) -->
<noscript><iframe src="https://www.googletagmanager.com/ns.html?id=<?php echo rawurlencode( CFI_GTM_ID ); ?>"
	height="0" width="0" style="display:none;visibility:hidden"></iframe></noscript>
<!-- End Google Tag Manager (noscript) -->
	<?php
}, 1 );

/**
 * Admin notice while tagging is dormant, so nobody concludes from an empty
 * Tag Assistant that the theme lost the snippet.
 */
add_action( 'admin_notices', function () {
	if ( ! current_user_can( 'manage_options' ) || ! CFI_GTM_ID ) {
		return;
	}
	$host = preg_replace( '/^www\./', '', strtolower( (string) ( $_SERVER['HTTP_HOST'] ?? '' ) ) );
	if ( $host === CFI_PROD_HOST ) {
		return;
	}
	printf(
		'<div class="notice notice-info"><p><strong>Tagging is dormant on this hostname.</strong> %s will start printing automatically once the site answers on <code>%s</code>. To test now, open any page with <code>?cfi_tags=1</code> while logged in.</p></div>',
		esc_html( CFI_GTM_ID ),
		esc_html( CFI_PROD_HOST )
	);
} );
