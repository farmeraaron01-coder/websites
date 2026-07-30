<?php
/**
 * One-time install of static-asset cache headers into .htaccess.
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

add_action( 'admin_init', function () {
	if ( get_option( 'cfi_htaccess_cache_rules' ) === 'v1' ) {
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
		'</IfModule>',
	);

	if ( insert_with_markers( $path, 'CFI static asset cache', $rules ) ) {
		update_option( 'cfi_htaccess_cache_rules', 'v1', false );
	}
} );
