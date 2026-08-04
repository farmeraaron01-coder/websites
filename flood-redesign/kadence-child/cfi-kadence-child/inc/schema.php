<?php
/**
 * FAQPage structured data, generated from the content that is already there.
 *
 * WHY THIS EXISTS
 * Twenty-nine pages and posts across the two sites carry an H2 reading "Common
 * questions" followed by H3 questions and paragraph answers — 107 question and
 * answer pairs in total, counted from raw post content on 4 Aug (36 on
 * statewide, 71 on California, whose city and flood-zone pages run five
 * questions each). None of it was marked up, so Google and the AI answer
 * engines had to infer the Q&A relationship from heading levels alone. Marking
 * it up makes the same content eligible for FAQ rich results and gives the
 * answer engines an unambiguous parse.
 *
 * WHY IT PARSES INSTEAD OF ASKING THE EDITOR
 * The alternative is an FAQ block, which would mean re-authoring the Q&A
 * section on twenty pages by hand and remembering to use the block every time
 * anyone adds a question. The existing markup is already perfectly regular, so
 * reading it is both cheaper and harder to get wrong. Write the content the way
 * it has always been written and the schema follows automatically.
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
 * Headings that mark the start of a question-and-answer section.
 *
 * @return string[] Lower-case heading texts, matched exactly after trimming.
 */
function cfi_faq_headings() {
	return apply_filters(
		'cfi_faq_headings',
		array( 'common questions', 'frequently asked questions', 'faq', 'faqs' )
	);
}

/**
 * Pull question and answer pairs out of a post's content.
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

	$headings = array_map( 'preg_quote', cfi_faq_headings() );
	$pattern  = '/<h2[^>]*>\s*(?:' . implode( '|', $headings ) . ')\s*:?\s*<\/h2>/i';

	if ( ! preg_match( $pattern, $html, $m, PREG_OFFSET_CAPTURE ) ) {
		return array();
	}

	// The FAQ section runs from that heading to the next H2, or to the end.
	$section = substr( $html, $m[0][1] + strlen( $m[0][0] ) );
	$next_h2 = preg_match( '/<h2[^>]*>/i', $section, $stop, PREG_OFFSET_CAPTURE )
		? substr( $section, 0, $stop[0][1] )
		: $section;

	// Each question owns everything up to the following question.
	if ( ! preg_match_all( '/<h3[^>]*>(.*?)<\/h3>(.*?)(?=<h3[^>]*>|$)/is', $next_h2, $found, PREG_SET_ORDER ) ) {
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

		$pairs[] = array(
			'question' => $question,
			'answer'   => $answer,
		);
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
