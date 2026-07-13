<?php
/**
 * Force the blog post title to render as <h1> on single posts.
 *
 * Why: the Divi Theme Builder "All Posts" template outputs the Post Title
 * module as an <h2 class="entry-title">, and the builder currently times out
 * so the module setting can't be changed in the UI. This rewrites just that
 * one tag in the final HTML, only on single blog posts, and only when the
 * page doesn't already have an <h1> title.
 *
 * Install via WPCode: Code Snippets → Add New → PHP Snippet,
 * insertion = Auto Insert / Frontend Only, then Activate.
 *
 * Remove this snippet once the Divi builder is working again and the
 * Post Title module's "Title Heading Level" is set to H1 properly.
 */
add_action('template_redirect', function () {
    if (is_admin() || !is_singular('post')) {
        return;
    }
    ob_start(function ($html) {
        // Already has an H1 entry title? Leave the page untouched.
        if (preg_match('/<h1[^>]*class="[^"]*entry-title/', $html)) {
            return $html;
        }
        // Find the Divi post-title H2.
        if (!preg_match('/<h2[^>]*class="[^"]*entry-title[^"]*"[^>]*>/', $html, $m, PREG_OFFSET_CAPTURE)) {
            return $html;
        }
        $open_tag = $m[0][0];
        $open_pos = $m[0][1];
        $close_pos = strpos($html, '</h2>', $open_pos);
        if ($close_pos === false) {
            return $html;
        }
        // Replace the closing tag first so the opening tag's offset stays valid.
        $html = substr_replace($html, '</h1>', $close_pos, 5);
        $html = substr_replace($html, substr_replace($open_tag, '<h1', 0, 3), $open_pos, strlen($open_tag));
        return $html;
    });
});
