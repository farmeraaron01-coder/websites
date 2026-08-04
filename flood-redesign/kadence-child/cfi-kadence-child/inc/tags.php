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
 * What this page is for, in one word, derived from the page itself rather than
 * from the shortcode inside it.
 *
 * Why it cannot come from [cfi_cognito]: shortcodes run while the content is
 * rendered, long after wp_head. The Cognito prefill tag in GTM fires on All
 * Pages and writes hidden fields into the form BEFORE anyone submits, so it
 * needs this value early — hence a slug lookup here rather than reusing the
 * role the shortcode works out later. The two agree because both key off the
 * same slugs.
 *
 * The use case: both flood sites and BOTH staff forms submit the same Cognito
 * form 5, and the prefill tag stamps `SourceWebsite` with the hostname. So a
 * staff-entered lead and a customer-entered lead from the same site are
 * indistinguishable once they reach the rater, Zapier, and InsuredMine.
 * Publishing the page role lets the prefill tag write a "Lead Type" field, so
 * the office can tell its own phone intake apart from real web leads in the CRM
 * — the same separation v1.3.7 gives Google Ads, one layer further down.
 */
function cfi_page_role() {
	$slug = get_queried_object() instanceof WP_Post ? (string) get_queried_object()->post_name : '';
	if ( '' === $slug ) {
		return 'other';
	}
	if ( false !== strpos( $slug, 'staff' ) ) {
		return 'staff';           // checked first: never mislabel staff intake
	}
	$map = array(
		'get-a-quote'       => 'quote',
		'claims'            => 'claims',
		'service-center'    => 'service',
		'agent-appointment' => 'appointment',
	);
	return $map[ $slug ] ?? 'other';
}

/**
 * Page-level context, pushed before the container loads so All Pages tags can
 * read it. Printed regardless of the host gate: it is a local JS object that
 * sends no request, and having it on staging is what makes the tag testable.
 */
add_action( 'wp_head', function () {
	if ( is_admin() ) {
		return;
	}
	?>
<script>window.dataLayer=window.dataLayer||[];window.dataLayer.push({cfi_page_role:<?php echo wp_json_encode( cfi_page_role() ); ?>,cfi_brand:<?php echo wp_json_encode( CFI_BRAND ); ?>});</script>
	<?php
}, 1 );

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
	 * GA4 direct — per brand, and the reasoning here was wrong until 4 Aug.
	 *
	 * This comment used to say GA4 arrives via Site Kit on production. It does
	 * not. Both live sites serve a **hardcoded gtag/js snippet in the Divi
	 * header** — verified in the served HTML, with no Site Kit markers present.
	 * That distinction matters because it changes what happens at cutover: a
	 * plugin would have kept working, and a hardcoded snippet dies with the
	 * theme. GA4 stops collecting the moment the domain moves.
	 *
	 * The container only covers for it if it holds a Google tag. GTM-PJQ72VK
	 * does not — it reports the Urgent warning "Missing Google tags" — so
	 * statewide sets CFI_GA4_ID. California's stays empty until GTM-MZ6RZ94 has
	 * been read, because the failure mode of guessing wrong in that direction is
	 * worse: two configurations means two page_view hits per pageview, inflated
	 * users, and a halved conversion rate.
	 *
	 * See the notes beside each CFI_GA4_ID in functions.php.
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
