<?php
/**
 * Jump Insurance SEO Fixes
 * Add this via WPCode plugin (Plugins > Code Snippets > Add New > PHP Snippet)
 * OR paste into child theme's functions.php
 *
 * Fixes: viewport user-scalable, xmlrpc pingback, security headers
 */

// 1. Fix viewport meta — remove user-scalable=0 restriction (WCAG 1.4.4)
add_filter( 'language_attributes', 'jumpins_fix_viewport', 10, 1 );
function jumpins_fix_viewport( $output ) {
    // Divi sets viewport via theme — override with a proper tag
    add_action( 'wp_head', 'jumpins_viewport_meta', 1 );
    return $output;
}
function jumpins_viewport_meta() {
    // Remove any existing viewport meta Divi outputs and replace with accessible version
    echo '<meta name="viewport" content="width=device-width, initial-scale=1.0">' . "\n";
}
// Remove Divi's viewport output to avoid duplication
add_action( 'after_setup_theme', function() {
    remove_action( 'wp_head', 'et_add_viewport_meta' );
});

// 2. Remove xmlrpc pingback link from <head>
remove_action( 'wp_head', 'xmlrpc_rsd' );
remove_action( 'wp_head', 'wp_generator' );  // Also hide WP version

// 3. Disable XML-RPC pingbacks entirely (keep REST API working)
add_filter( 'xmlrpc_methods', function( $methods ) {
    unset( $methods['pingback.ping'] );
    unset( $methods['pingback.extensions.getPingbacks'] );
    return $methods;
});

// 4. Add security headers
add_action( 'send_headers', 'jumpins_security_headers' );
function jumpins_security_headers() {
    if ( headers_sent() ) return;
    header( 'X-Content-Type-Options: nosniff' );
    header( 'X-Frame-Options: SAMEORIGIN' );
    header( 'Referrer-Policy: strict-origin-when-cross-origin' );
    header( 'X-XSS-Protection: 1; mode=block' );
    header( 'Permissions-Policy: camera=(), microphone=(), geolocation=(self)' );
}

// 5. Remove WordPress version from all outputs
add_filter( 'the_generator', '__return_empty_string' );
remove_action( 'wp_head', 'wp_generator' );
