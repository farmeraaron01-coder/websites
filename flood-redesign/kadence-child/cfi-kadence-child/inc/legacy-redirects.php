<?php
/**
 * 301s for URLs left behind by the pre-Divi mobile subsite.
 *
 * WHY THIS EXISTS
 * `/mobile/contact.php` is the single most valuable 404 on the site. Over 90 days
 * it took **182 impressions at an average position of 14.65**, and on the two head
 * terms the agency is actually chasing it sits at the top of page one:
 *
 *     california flood insurance            53 impressions   position 2.62
 *     flood insurance california            29 impressions   position 1.10
 *     california flood insurance services   16 impressions   position 1.69
 *     ca flood insurance                     6 impressions   position 1.00
 *
 * Every one of those clicked through to a 404. Zero clicks on 138 head-term
 * impressions is not a coincidence — a "Page Not Found" title is what Google was
 * showing, and nobody clicks it. This is the cheapest ranking recovery available:
 * the position already exists and is being thrown away at the door.
 *
 * I called this "optional, low value" twice before pulling the query data. It was
 * the highest-value item on the list both times.
 *
 * WHY THE HOMEPAGE, NOT /contact-us/
 * The filename says contact, so /contact-us/ looks like the obvious target. The
 * query mix says otherwise: roughly 110 of the 138 impressions are general
 * California-flood-insurance head and brand terms, and only about 7 are genuine
 * contact intent (two phone-number searches). Google is not treating this as a
 * contact page; it is treating it as a California flood insurance result.
 *
 * The homepage is also the designated target for those head terms, and it is
 * already competing with /contact-us/ on them — /contact-us/ takes 130 impressions
 * at position 4.38 for "california flood insurance" against the homepage's 1.12.
 * Redirecting here into /contact-us/ would deepen exactly the cannibalisation
 * that needs fixing, so the signal goes where the ranking is wanted.
 *
 * WHY PHP AND NOT .htaccess
 * These paths do not exist on disk, so Apache hands them to WordPress's front
 * controller and WordPress renders the 404 — verified: the response is 404 with
 * the child theme's own "Page Not Found" markup. That means `template_redirect`
 * fires and can answer first, which is preferable to another .htaccess rule:
 * it is version-controlled with the theme, it needs no admin page load to install,
 * and it cannot interact with the WordPress rewrite block the way a hand-written
 * RewriteRule can.
 *
 * Matching is done on the *path only*, lowercased, with the query string dropped,
 * so `/Mobile/Contact.php?utm_source=x` lands too. The redirect is issued only
 * when WordPress has actually decided the URL is a 404, so it can never shadow a
 * real page added at one of these paths later.
 */

/**
 * Legacy path (no query string, lowercase, no trailing slash) => target.
 *
 * Anything under the old /mobile/ tree that WordPress 404s and is not listed
 * explicitly falls through to the homepage via the prefix rule below. That is
 * deliberate: the subsite is gone in its entirety, and a 301 to the homepage is
 * strictly better than a 404 for every one of its URLs.
 */
function cfi_legacy_redirect_map() {
	return array(
		// The head-term earner. See the docblock for why this is not /contact-us/.
		'/mobile/contact.php' => '/',
		// Quote intent is specific enough to deserve its own destination.
		'/mobile/quote.php'   => '/get-a-quote/',
		'/mobile/quote'       => '/get-a-quote/',
		// /mobile/index.php currently 301s to /mobile/, which is itself a 404 —
		// a redirect chain ending nowhere. Naming both kills the chain.
		'/mobile/index.php'   => '/',
		'/mobile'             => '/',
	);
}

/*
 * Priority 1, so this answers before WordPress's own redirect_canonical (which
 * runs on this hook at the default 10).
 *
 * Measured on 1.6.0: /mobile/index.php came back as 301 -> /mobile/ -> / — two
 * hops, because redirect_canonical strips index.php on a 404 before this rule got
 * a look in. It resolved to a 200 either way, which is already far better than the
 * dead end it used to be (/mobile/ was itself a 404), but a single hop is cleaner
 * and costs nothing.
 *
 * is_404() is still reliable at priority 1: template_redirect fires after the main
 * query has run, so the 404 flag is already set. The front-page pagination guard
 * in functions.php calls set_404() on this same hook at priority 10, i.e. after
 * this — which is harmless, because a paginated front page matches nothing in the
 * map and would be skipped anyway.
 */
/**
 * URLs merged into another page, where the ORIGINAL STILL EXISTS.
 *
 * Different from the map above, and the difference matters. Those paths 404 —
 * nothing serves them, so redirecting on `is_404()` is safe and self-limiting.
 * A merged page is still published, so it never 404s and that rule would never
 * fire. These have to be matched on the path itself.
 *
 * WHY MERGE RATHER THAN LEAVE BOTH
 * `/flood-insurance-rates/` and `/how-much-does-flood-insurance-cost/` were two
 * pages answering one question. Measured over twelve months in Search Console:
 * 102 of the rates page's 132 queries also ranked on the cost page, and on
 * nearly every shared query the cost page ranked better — "cost of flood
 * insurance" sat at position 70 on rates against 21 on cost. Only 30 queries
 * were unique to the rates page, worth 52 impressions in a year.
 *
 * The two pages also disagreed. The rates page published "about $780 per year"
 * as the California average and "as low as roughly $350" for Zone X, neither
 * sourced. The cost page publishes a measured NFIP median of $1,244. Two live
 * pages contradicting each other on price is a worse problem than the ranking
 * split, given we are publishing premium figures as a licensed agency.
 *
 * KEEP THIS LIST SHORT. Every entry makes a published page unreachable, which
 * is easy to do by accident and invisible afterwards. Remove the entry and the
 * page comes straight back — that is the intended undo.
 */
function cfi_merged_redirect_map() {
	// HOST-GATED ON PURPOSE. Both brands share this child theme, so an entry here
	// applies to every site running it. The rates/cost merge was decided on
	// California's Search Console data -- 102 of 132 overlapping queries, the cost
	// page ranking better on nearly all of them -- and none of that evidence says
	// anything about statewide. Uploading 1.6.3 to both sites duly turned statewide's
	// /flood-insurance-rates/ into a two-hop chain through a page that itself
	// redirects. No traffic was lost (both had zero impressions in twelve months),
	// but a decision made for one brand should not quietly bind the other.
	$host = strtolower( wp_parse_url( home_url(), PHP_URL_HOST ) ?? '' );
	$maps = array(
		'californiafloodinsurance.com' => array(
			'/flood-insurance-rates' => '/how-much-does-flood-insurance-cost/',
		),
	);
	foreach ( $maps as $brand => $map ) {
		if ( false !== strpos( $host, $brand ) ) {
			return $map;
		}
	}
	return array();
}

add_action( 'template_redirect', function () {
	$path = wp_parse_url( $_SERVER['REQUEST_URI'] ?? '', PHP_URL_PATH );
	if ( ! is_string( $path ) || '' === $path ) {
		return;
	}
	$path = strtolower( rtrim( $path, '/' ) );
	if ( '' === $path ) {
		return;
	}

	$target = cfi_merged_redirect_map()[ $path ] ?? null;
	if ( null === $target ) {
		return;
	}

	// Never redirect a path to itself. Cheap guard against a typo in the map
	// turning into a loop that takes the page down with no obvious cause.
	if ( rtrim( $target, '/' ) === $path ) {
		return;
	}

	wp_safe_redirect( home_url( $target ), 301 );
	exit;
}, 1 );

add_action( 'template_redirect', function () {
	// Only ever act on something WordPress has already resolved to a 404. This is
	// what makes the rule safe to leave in place permanently.
	if ( ! is_404() ) {
		return;
	}

	$path = wp_parse_url( $_SERVER['REQUEST_URI'] ?? '', PHP_URL_PATH );
	if ( ! is_string( $path ) || '' === $path ) {
		return;
	}
	$path = strtolower( rtrim( $path, '/' ) );
	if ( '' === $path ) {
		return;
	}

	$map    = cfi_legacy_redirect_map();
	$target = $map[ $path ] ?? null;

	// Catch-all for the rest of the retired subsite.
	if ( null === $target && 0 === strpos( $path, '/mobile/' ) ) {
		$target = '/';
	}

	if ( null === $target ) {
		return;
	}

	wp_safe_redirect( home_url( $target ), 301 );
	exit;
}, 1 );
