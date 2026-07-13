<?php
/**
 * TASK A2 WORKAROUND v2 — wrap the blog post title in an <h1> on single posts.
 *
 * Verified against the live markup (July 13, 2026): the Theme Builder
 * "All Posts" template renders the title as bare text in a Divi TEXT module —
 *   <div class="et_pb_module et_pb_text et_pb_text_0_tb_body ...">
 *     <div class="et_pb_text_inner">POST TITLE</div>
 *   </div>
 * — no heading tag, no entry-title class (which is why v1 was a no-op).
 *
 * This wraps that title text in an <h1> that inherits every visual style
 * from the existing div, so the page looks identical and gains a real H1.
 * Only runs on single blog posts; skips any page that already has an <h1>;
 * bails out untouched if the markup ever isn't the expected bare text.
 * Fully reversible — deactivate the snippet in WPCode to undo.
 *
 * INSTALL: WPCode → edit the existing "Post title H1" snippet and replace its
 * code with everything below the opening <?php tag (or deactivate the old one
 * and add this as a new PHP snippet, Auto Insert / Frontend Only, Activate).
 * Clear the site cache afterward.
 *
 * REMOVE once the Divi builder works again and the template's title module is
 * replaced with a proper Post Title module set to H1 (or the Text module's
 * content is set to Heading 1).
 */
add_action('template_redirect', function () {
    if (is_admin() || !is_singular('post')) {
        return;
    }
    ob_start(function ($html) {
        // Already has any H1? Leave the page untouched.
        if (preg_match('/<h1[\s>]/i', $html)) {
            return $html;
        }
        // Locate the Theme Builder title text module, then its inner div.
        $module_pos = strpos($html, 'et_pb_text_0_tb_body');
        if ($module_pos === false) {
            return $html;
        }
        $open_marker = '<div class="et_pb_text_inner">';
        $open_pos = strpos($html, $open_marker, $module_pos);
        if ($open_pos === false) {
            return $html;
        }
        $text_start = $open_pos + strlen($open_marker);
        $text_end = strpos($html, '</div>', $text_start);
        if ($text_end === false) {
            return $html;
        }
        $title = substr($html, $text_start, $text_end - $text_start);
        // Expect bare text; if Divi ever nests markup here, do nothing.
        if (trim($title) === '' || strpos($title, '<') !== false) {
            return $html;
        }
        $h1 = '<h1 style="margin:0;padding:0;font:inherit;color:inherit;'
            . 'letter-spacing:inherit;text-transform:inherit;">'
            . $title . '</h1>';
        return substr_replace($html, $h1, $text_start, $text_end - $text_start);
    });
});
