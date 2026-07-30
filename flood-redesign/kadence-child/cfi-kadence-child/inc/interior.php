<?php
/**
 * Interior pages — the shared engine behind zone pages, city pages and articles.
 *
 * Everything here is content-driven: if a field is empty the block does not
 * render, so a half-migrated page degrades to a plain article rather than
 * showing empty furniture.
 *
 * All meta is registered with show_in_rest so the content migration can
 * populate it over the REST API instead of by hand.
 */

/**
 * Meta this theme owns. Registered on both posts and pages because zone and
 * city content lives in pages while articles live in posts.
 */
add_action( 'init', function () {
	$fields = array(
		// One takeaway per line. Renders the "What to know" box.
		'_cfi_takeaways'   => 'string',
		// Short badge label, e.g. "Flood Zone AE". Empty = no badge.
		'_cfi_badge'       => 'string',
		// high | moderate | low — drives the badge colour only.
		'_cfi_risk'        => 'string',
		// YYYY-MM-DD. Falls back to the modified date when empty.
		'_cfi_reviewed'    => 'string',
		// Optional one-line summary under the h1.
		'_cfi_standfirst'  => 'string',
	);

	foreach ( array( 'post', 'page' ) as $type ) {
		foreach ( $fields as $key => $data_type ) {
			register_post_meta( $type, $key, array(
				'type'              => $data_type,
				'single'            => true,
				'show_in_rest'      => true,
				'sanitize_callback' => 'wp_kses_post',
				'auth_callback'     => function () {
					return current_user_can( 'edit_posts' );
				},
			) );
		}
	}

	/*
	 * Rank Math stores its title and description in post meta but does not
	 * expose them to REST. Registering them here lets the migration write all
	 * 86 titles and descriptions programmatically. Rank Math reads its own keys
	 * normally either way — this only makes them visible to the API.
	 */
	foreach ( array( 'post', 'page' ) as $type ) {
		foreach ( array( 'rank_math_title', 'rank_math_description' ) as $key ) {
			register_post_meta( $type, $key, array(
				'type'          => 'string',
				'single'        => true,
				'show_in_rest'  => true,
				'auth_callback' => function () {
					return current_user_can( 'edit_posts' );
				},
			) );
		}
	}
} );

/**
 * Turn a heading into a stable anchor id.
 */
function cfi_anchor( $text ) {
	$slug = sanitize_title( wp_strip_all_tags( $text ) );
	return $slug ? $slug : 'section';
}

/**
 * Add ids to h2/h3 headings and collect a table of contents in one pass.
 *
 * Deliberately regex rather than DOMDocument: migrated Divi content is not
 * guaranteed to be well-formed, and DOMDocument rewrites the whole document
 * when it repairs it. This only touches the heading tags it matches and leaves
 * everything else byte-identical.
 *
 * @return array{content:string,toc:array}
 */
function cfi_build_toc( $html ) {
	$toc  = array();
	$seen = array();

	$content = preg_replace_callback(
		'#<h([23])([^>]*)>(.*?)</h\1>#is',
		function ( $m ) use ( &$toc, &$seen ) {
			list( , $level, $attrs, $inner ) = $m;

			// Respect an id that already exists rather than fighting it.
			if ( preg_match( '/\bid=["\']([^"\']+)["\']/i', $attrs, $has ) ) {
				$id = $has[1];
			} else {
				$id = cfi_anchor( $inner );
				if ( isset( $seen[ $id ] ) ) {
					$seen[ $id ]++;
					$id .= '-' . $seen[ $id ];
				} else {
					$seen[ $id ] = 1;
				}
				$attrs .= ' id="' . esc_attr( $id ) . '"';
			}

			/*
			 * Decode entities before storing the title. Migrated content is full
			 * of &#8217; and &amp;, and the template escapes on output — so
			 * without decoding here the contents list renders the entity text
			 * literally ("Do I Need Flood Insurance If I&#8217;m…").
			 */
			$title = trim( html_entity_decode( wp_strip_all_tags( $inner ), ENT_QUOTES, 'UTF-8' ) );
			if ( $title !== '' ) {
				$toc[] = array(
					'level' => (int) $level,
					'id'    => $id,
					'title' => $title,
				);
			}

			return '<h' . $level . $attrs . '>' . $inner . '</h' . $level . '>';
		},
		$html
	);

	// A one-item contents list is furniture, not navigation.
	if ( count( $toc ) < 3 ) {
		$toc = array();
	}

	return array(
		'content' => null === $content ? $html : $content,
		'toc'     => $toc,
	);
}

/**
 * Takeaways as an array. One per line in the meta field.
 */
function cfi_takeaways( $post_id ) {
	$raw = (string) get_post_meta( $post_id, '_cfi_takeaways', true );
	if ( '' === trim( $raw ) ) {
		return array();
	}
	$lines = preg_split( '/\r\n|\r|\n/', $raw );
	$lines = array_filter( array_map( 'trim', $lines ) );
	return array_values( $lines );
}

/**
 * The "last reviewed" date shown in the byline. Falls back to the modified
 * date so the block is never blank on migrated content.
 */
function cfi_reviewed_date( $post_id ) {
	$set = trim( (string) get_post_meta( $post_id, '_cfi_reviewed', true ) );
	if ( $set && ( $ts = strtotime( $set ) ) ) {
		return date_i18n( 'F j, Y', $ts );
	}
	return get_the_modified_date( 'F j, Y', $post_id );
}

/**
 * Risk level → the CSS modifier used for the badge colour.
 */
function cfi_risk_class( $post_id ) {
	$risk = strtolower( trim( (string) get_post_meta( $post_id, '_cfi_risk', true ) ) );
	return in_array( $risk, array( 'high', 'moderate', 'low' ), true ) ? $risk : '';
}
