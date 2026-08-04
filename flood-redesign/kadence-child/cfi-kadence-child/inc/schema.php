<?php
/**
 * FAQPage structured data, generated from the content that is already there.
 *
 * WHY THIS EXISTS — IT FIXES A MIGRATION REGRESSION, NOT A GAP
 * The live Divi sites emit FAQPage structured data on both brands: verified 4
 * Aug on seven statewide state pages and five California pages, all returning a
 * FAQPage node. That schema was hand-written into Divi `et_pb_code` modules —
 * see `statewidefloodinsurance.com-hub/tn-template.txt` in Dropbox for the
 * Tennessee original.
 *
 * A code module has no Kadence equivalent, so the migration carried the Q&A
 * *prose* across and dropped the *markup*. The staging sites emit no FAQPage at
 * all. Cutting over without this file would have silently surrendered FAQ rich
 * results on 77 pages — the kind of loss that shows up as a ranking drift weeks
 * later with no obvious cause.
 *
 * WHAT IT COVERS
 * 77 pages and posts, 302 question and answer pairs, counted from raw content
 * on 4 Aug: 49 items / 176 pairs on statewide (including all 29 state pages),
 * 28 items / 126 pairs on California, whose city and flood-zone pages run five
 * questions each. That is more than Divi ever marked up, because the template's
 * hand-written JSON-LD only ever covered the pages someone remembered to paste
 * it into.
 *
 * WHY IT PARSES INSTEAD OF ASKING THE EDITOR
 * The alternative is an FAQ block, which would mean re-authoring 77 pages by
 * hand and remembering to use the block every time anyone adds a question —
 * which is precisely how the Divi version ended up incomplete. Reading the
 * existing markup is cheaper, harder to get wrong, and self-maintaining: write
 * the content the way it has always been written and the schema follows.
 *
 * WHY RAW CONTENT, NOT RENDERED
 * Running the_content filters this early triggers other plugins' hooks and can
 * recurse. Block markup is HTML with comment delimiters, so stripping the
 * comments from post_content gives the same headings and paragraphs without
 * rendering anything.
 *
 * SAFETY
 * Emits nothing unless it finds at least two complete pairs, so a page with a
 * stray heading cannot produce a one-item FAQPage that Google would flag. This
 * is additive: Rank Math's own graph is untouched.
 *
 * @package cfi-kadence-child
 */

defined( 'ABSPATH' ) || exit;

/**
 * Regex fragments that identify the heading opening a Q&A section.
 *
 * The state pages title theirs per state — "Tennessee flood insurance FAQ" —
 * so this matches a heading that CONTAINS one of these rather than equals it.
 *
 * @return string[] Regex alternatives, matched case-insensitively.
 */
function cfi_faq_headings() {
	return apply_filters(
		'cfi_faq_headings',
		array( 'common questions', 'frequently asked questions', '\bFAQs?\b' )
	);
}

/**
 * Pull question and answer pairs out of a post's content.
 *
 * TWO MARKUP PATTERNS, BECAUSE THE SITES CONTAIN BOTH
 * The articles and claims pages use <h3>Question</h3> followed by prose. The 29
 * state pages, authored from the Divi template, use
 * <p><strong>Question?</strong><br>Answer</p> in a single paragraph. Both are
 * read here so neither body of content needs re-authoring.
 *
 * @param string $raw Raw post_content.
 * @return array<int,array{question:string,answer:string}> Ordered pairs, possibly empty.
 */
function cfi_extract_faq_pairs( $raw ) {
	if ( '' === trim( (string) $raw ) ) {
		return array();
	}

	// Block delimiters are HTML comments; drop them so the headings sit adjacent.
	$html = preg_replace( '/<!--.*?-->/s', '', (string) $raw );

	$pattern = '/<h2[^>]*>[^<]*(?:' . implode( '|', cfi_faq_headings() ) . ')[^<]*<\/h2>/i';

	if ( ! preg_match( $pattern, $html, $m, PREG_OFFSET_CAPTURE ) ) {
		return array();
	}

	// The section runs from that heading to the next H2, or to the end of content.
	$section = substr( $html, $m[0][1] + strlen( $m[0][0] ) );
	if ( preg_match( '/<h2[^>]*>/i', $section, $stop, PREG_OFFSET_CAPTURE ) ) {
		$section = substr( $section, 0, $stop[0][1] );
	}

	$pairs = cfi_faq_pairs_from_headings( $section );

	// Fall back to the state-page paragraph form only if no headings were found.
	if ( empty( $pairs ) ) {
		$pairs = cfi_faq_pairs_from_paragraphs( $section );
	}

	return $pairs;
}

/**
 * Read <h3>Question</h3> + following prose pairs.
 *
 * @param string $section FAQ section markup.
 * @return array<int,array{question:string,answer:string}>
 */
function cfi_faq_pairs_from_headings( $section ) {
	if ( ! preg_match_all( '/<h3[^>]*>(.*?)<\/h3>(.*?)(?=<h3[^>]*>|$)/is', $section, $found, PREG_SET_ORDER ) ) {
		return array();
	}

	$pairs = array();
	foreach ( $found as $pair ) {
		$question = cfi_faq_text( $pair[1] );
		$answer   = cfi_faq_text( $pair[2] );

		// A heading with no prose under it is a subheading, not a question.
		if ( '' === $question || '' === $answer ) {
			continue;
		}

		$pairs[] = compact( 'question', 'answer' );
	}

	return $pairs;
}

/**
 * Read <p><strong>Question?</strong><br>Answer</p> pairs.
 *
 * The trailing question mark is required deliberately. The state pages follow
 * their FAQ with an author box whose first paragraph also opens with <strong>,
 * and requiring "?" excludes it without needing to know the box is there.
 *
 * @param string $section FAQ section markup.
 * @return array<int,array{question:string,answer:string}>
 */
function cfi_faq_pairs_from_paragraphs( $section ) {
	$pattern = '/<p[^>]*>\s*<strong>\s*([^<]*\?)\s*<\/strong>\s*(?:<br\s*\/?>\s*)+(.*?)<\/p>/is';

	if ( ! preg_match_all( $pattern, $section, $found, PREG_SET_ORDER ) ) {
		return array();
	}

	$pairs = array();
	foreach ( $found as $pair ) {
		$question = cfi_faq_text( $pair[1] );
		$answer   = cfi_faq_text( $pair[2] );

		if ( '' === $question || '' === $answer ) {
			continue;
		}

		$pairs[] = compact( 'question', 'answer' );
	}

	return $pairs;
}

/**
 * Reduce a fragment of post content to the plain text schema wants.
 *
 * @param string $html Content fragment.
 * @return string Decoded, tag-free, single-spaced text.
 */
function cfi_faq_text( $html ) {
	$text = wp_strip_all_tags( (string) $html, true );
	$text = html_entity_decode( $text, ENT_QUOTES | ENT_HTML5, 'UTF-8' );

	// Non-breaking spaces survive decoding and would otherwise stay in the JSON.
	$text = str_replace( "\xc2\xa0", ' ', $text );

	return trim( preg_replace( '/\s+/', ' ', $text ) );
}

/**
 * Print FAQPage JSON-LD for the current singular view.
 *
 * @return void
 */
function cfi_print_faq_schema() {
	if ( ! is_singular() || is_feed() ) {
		return;
	}

	$post = get_queried_object();
	if ( ! $post instanceof WP_Post ) {
		return;
	}

	$pairs = cfi_extract_faq_pairs( $post->post_content );

	// One question is not an FAQ, and Google treats a single-item FAQPage as thin.
	if ( count( $pairs ) < 2 ) {
		return;
	}

	$entities = array();
	foreach ( $pairs as $pair ) {
		$entities[] = array(
			'@type'          => 'Question',
			'name'           => $pair['question'],
			'acceptedAnswer' => array(
				'@type' => 'Answer',
				'text'  => $pair['answer'],
			),
		);
	}

	$graph = array(
		'@context'   => 'https://schema.org',
		'@type'      => 'FAQPage',
		'@id'        => get_permalink( $post ) . '#faq',
		'mainEntity' => $entities,
	);

	printf(
		"<script type=\"application/ld+json\">%s</script>\n",
		wp_json_encode( $graph, JSON_UNESCAPED_SLASHES | JSON_UNESCAPED_UNICODE )
	);
}
add_action( 'wp_head', 'cfi_print_faq_schema', 20 );
