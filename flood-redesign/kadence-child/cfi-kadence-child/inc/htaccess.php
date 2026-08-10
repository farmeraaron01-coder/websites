<?php
/**
 * Server-level rules for static files: cache headers via .htaccess, and keeping
 * the claim PDFs out of search via robots.txt.
 *
 * The robots.txt half lives here rather than with the SEO code because it exists
 * for the same reason as the .htaccess half — these files never reach PHP, so
 * anything that governs them has to be configured rather than rendered. See the
 * filter at the bottom for why a header could not do the job on this host.
 *
 * Why this exists: PageSpeed measured every asset under /wp-content/themes/
 * shipping with no cache headers at all (285 KiB wasted per mobile visit,
 * 2,065 KiB on desktop — the hero video re-downloads every time), while
 * /wp-content/uploads/ already gets max-age=604800 from the host. Static file
 * requests never reach PHP, so the only fix is server config. Editing
 * .htaccess by hand was ruled out, so the theme installs the rules itself via
 * insert_with_markers() — the same core mechanism WP Super Cache and W3TC use.
 *
 * Safety properties:
 *  - insert_with_markers() writes a clearly delimited block
 *    (# BEGIN CFI static asset cache … # END) and never touches anything
 *    outside its own markers, including the WordPress rewrite block.
 *  - Every directive is wrapped in <IfModule>, so a server missing mod_expires
 *    or mod_headers ignores the rules rather than erroring.
 *  - Runs only in wp-admin, only for administrators, and only until it has
 *    succeeded once (tracked in an option). If .htaccess is missing or not
 *    writable it does nothing, silently — the host-level fallback is to hand
 *    CACHE-HEADERS.md to InMotion support.
 *
 * To undo: delete the marker block from .htaccess and the
 * cfi_htaccess_cache_rules option.
 *
 * A year for images/fonts/video is safe because WordPress version-stamps or
 * renames them on change; CSS/JS get a month and carry ?ver= query strings.
 */

/*
 * One constant for the gate and the stamp, because keeping them in step by hand
 * already failed. Up to 1.5.8 the guard tested for 'v3' while the success path
 * wrote 'v4', so the option could never satisfy the guard: every single wp-admin
 * page load re-ran the installer and rewrote .htaccess. Harmless in output —
 * insert_with_markers() is idempotent — but it was an unnecessary write to the
 * file that controls whether the site serves at all, on every admin request.
 *
 * Bump this when the rules below change; both sides move together by
 * construction.
 */
define( 'CFI_HTACCESS_RULES_VERSION', 'v5' );

add_action( 'admin_init', function () {
	if ( get_option( 'cfi_htaccess_cache_rules' ) === CFI_HTACCESS_RULES_VERSION ) {
		return;
	}
	if ( ! current_user_can( 'manage_options' ) ) {
		return;
	}

	require_once ABSPATH . 'wp-admin/includes/file.php';
	require_once ABSPATH . 'wp-admin/includes/misc.php';

	if ( ! function_exists( 'insert_with_markers' ) || ! function_exists( 'get_home_path' ) ) {
		return;
	}

	$path = get_home_path() . '.htaccess';
	if ( ! file_exists( $path ) || ! wp_is_writable( $path ) ) {
		return;
	}

	$rules = array(
		'<IfModule mod_expires.c>',
		'  ExpiresActive On',
		'  ExpiresByType image/webp              "access plus 1 year"',
		'  ExpiresByType image/jpeg              "access plus 1 year"',
		'  ExpiresByType image/png               "access plus 1 year"',
		'  ExpiresByType image/svg+xml           "access plus 1 year"',
		'  ExpiresByType video/mp4               "access plus 1 year"',
		'  ExpiresByType font/woff2              "access plus 1 year"',
		'  ExpiresByType text/css               "access plus 1 month"',
		'  ExpiresByType application/javascript "access plus 1 month"',
		'</IfModule>',
		'<IfModule mod_headers.c>',
		'  <FilesMatch "\.(webp|jpe?g|png|svg|mp4|woff2)$">',
		'    Header set Cache-Control "public, max-age=31536000, immutable"',
		'  </FilesMatch>',
		'  <FilesMatch "\.(css|js)$">',
		'    Header set Cache-Control "public, max-age=2592000"',
		'  </FilesMatch>',
		/*
		 * Downloadable PDFs (claim checklists, prep guides) are deliverables, not
		 * search assets. Two reasons to keep them out of the index: a PDF result
		 * carries no navigation, no CTA and no phone number, so it converts far
		 * worse than the page holding the same content; and the two sister brands
		 * ship the same documents with different logos, which would otherwise have
		 * them competing with each other. The pages are the indexable version.
		 */
		'  <FilesMatch "\.pdf$">',
		'    Header set X-Robots-Tag "noindex, noarchive"',
		'    Header set Cache-Control "public, max-age=2592000"',
		'  </FilesMatch>',
		'</IfModule>',
		/*
		 * Deny readme / license / changelog files. Added 1.5.9, from the Search
		 * Console investigation on 10 Aug.
		 *
		 * WordPress and almost every plugin ship these, and they state exact
		 * versions. Measured on California that day: Rank Math's readme.txt
		 * returned `Stable tag: 1.0.275`. An exact plugin version is the first
		 * step of a targeted-exploit search — look up the version, look up its
		 * known issues, skip the reconnaissance entirely.
		 *
		 * Turning off directory listings (cPanel -> Indexes, done the same day)
		 * stopped anyone *browsing* to these files. It does nothing about a direct
		 * request for a known filename, and `readme.txt` is the first filename
		 * anyone tries. This is the half of that fix that actually closes it.
		 *
		 * Safe to automate, unlike the rest of `california-hardening.conf`:
		 *  - `Require` is guarded by <IfModule mod_authz_core.c>, so a server
		 *    without it ignores the block rather than erroring.
		 *  - It contains no `Options` directive. A bare `Options` line returns 500
		 *    for the entire site where AllowOverride forbids it, which is why the
		 *    listings fix went through cPanel by hand and this does not.
		 *  - Nothing on a live site reads these files over HTTP. WordPress gets
		 *    plugin version data from the .org API, not by fetching readme.txt.
		 *
		 * STEP 2 of that file is deliberately NOT here. It rewrites requests under
		 * /wp-includes/ to 404, which interacts with WordPress's own rewrite block
		 * and needs one exception (wp-tinymce.php) to avoid breaking the editor.
		 * That belongs in a change someone watches, on its own day.
		 */
		'<IfModule mod_authz_core.c>',
		'  <FilesMatch "^(readme|README|license|LICENSE|changelog|CHANGELOG)\.(txt|html|md)$">',
		'    Require all denied',
		'  </FilesMatch>',
		'</IfModule>',
	);

	if ( insert_with_markers( $path, 'CFI static asset cache', $rules ) ) {
		update_option( 'cfi_htaccess_cache_rules', CFI_HTACCESS_RULES_VERSION, false );
	}
} );

/**
 * Keep the claim PDFs out of search — via robots.txt, because on this host no
 * header can reach them.
 *
 * What was measured (4 Aug, both staging sites):
 *  - A missing file under /wp-content/themes/ returns WordPress's own 404 page,
 *    and theme assets carry the Cache-Control the block above sets. That path
 *    goes through Apache, so .htaccess works there.
 *  - A missing file under /wp-content/uploads/ returns *nginx's* 404 page, and
 *    uploads carry max-age=604800 from the host rather than anything set here.
 *    nginx serves that directory straight off disk.
 *
 * So requests for the PDFs never reach Apache, and no amount of .htaccess —
 * root or per-directory — can add X-Robots-Tag to them. v1.3.5 through v1.3.9
 * were writing a rule that could not fire. The FilesMatch above is left in
 * place because it is correct for any PDF served from a path Apache does own,
 * but it is not what keeps the claim documents out of the index.
 *
 * robots.txt is the mechanism that works without the host's help. Honest limit:
 * Disallow prevents crawling, not indexing — a disallowed URL that is linked
 * can still appear as a bare result with no snippet. That is acceptable here,
 * because the goal is that the PDF never competes with the page holding the
 * same content, and an uncrawled PDF has no content to rank.
 *
 * The complete fix is one line of nginx (`add_header X-Robots-Tag "noindex,
 * noarchive"` on the uploads location) — worth bundling into the same InMotion
 * ticket as the /wp-json/ cache exclusion. Until then, this stands on its own.
 *
 * No trailing `$`: leaving it off also covers cache-busted and tracking-suffixed
 * URLs such as …/guide.pdf?utm_source=email.
 */
add_filter( 'robots_txt', function ( $output ) {
	$rule = "\n# Claim PDFs are deliverables, not search results — the pages hold the same content.\nDisallow: /wp-content/uploads/*.pdf\n";

	// Append inside the existing "User-agent: *" group rather than after the
	// Sitemap line, so the directive belongs to a group crawlers are reading.
	if ( false !== strpos( $output, 'Disallow: /wp-admin/' ) ) {
		return str_replace(
			"Disallow: /wp-admin/",
			"Disallow: /wp-admin/" . rtrim( $rule ),
			$output
		);
	}
	return $output . $rule;
}, 20 );
