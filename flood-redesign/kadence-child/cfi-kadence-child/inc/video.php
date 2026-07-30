<?php
/**
 * Video embeds and the video hub.
 *
 * Two shortcodes:
 *
 *   [cfi_video id="vdslGDfJgIQ" title="Private Flood Insurance vs FEMA"
 *              upload="2025-03-14" duration="PT4M12S"]
 *   [cfi_videos]                        — grid of every post in the "videos" category
 *
 * Why a click-to-play facade rather than a plain iframe: a YouTube iframe pulls
 * roughly 600KB–1MB and a lot of JavaScript before anyone presses play. Four of
 * them on one page would undo the performance work outright — the migrated pages
 * currently measure 98 mobile with TBT 0ms. The facade ships one ~15KB thumbnail
 * and only creates the iframe on click, so a page with ten videos costs about the
 * same as a page with none.
 *
 * SEO: each video should live on its own URL with real text around it — that is
 * what earns a video result, not a wall of embeds on one page. The shortcode emits
 * VideoObject JSON-LD for the video it renders. `uploadDate` is required by Google;
 * pass `upload` when the real YouTube publish date is known, otherwise it falls
 * back to the post date, which is when *this page* was published rather than when
 * the video went up. Worth setting properly for anything you want ranking.
 *
 * youtube-nocookie.com is used so nothing is set until the visitor presses play.
 */

/**
 * Single video: facade + VideoObject.
 */
add_shortcode( 'cfi_video', function ( $atts ) {
	$a = shortcode_atts( array(
		'id'       => '',
		'title'    => '',
		'upload'   => '',
		'duration' => '',   // ISO 8601, e.g. PT4M12S
		'desc'     => '',
	), $atts, 'cfi_video' );

	// YouTube ids are 11 chars of [A-Za-z0-9_-]. Reject anything else rather
	// than interpolate it into an iframe URL.
	if ( ! preg_match( '/^[A-Za-z0-9_-]{11}$/', (string) $a['id'] ) ) {
		return current_user_can( 'edit_posts' )
			? '<p><strong>[cfi_video]</strong> needs a valid 11-character YouTube <code>id</code>.</p>'
			: '';
	}

	$vid   = $a['id'];
	$label = $a['title'] !== '' ? $a['title'] : 'video';
	$embed = 'https://www.youtube-nocookie.com/embed/' . $vid . '?rel=0&autoplay=1';
	$thumb = 'https://i.ytimg.com/vi/' . $vid . '/maxresdefault.jpg';
	$fallb = 'https://i.ytimg.com/vi/' . $vid . '/hqdefault.jpg';

	$upload = $a['upload'] !== '' && strtotime( $a['upload'] )
		? gmdate( 'c', strtotime( $a['upload'] ) )
		: get_the_date( 'c' );

	$schema = array(
		'@context'     => 'https://schema.org',
		'@type'        => 'VideoObject',
		'name'         => $a['title'] !== '' ? $a['title'] : get_the_title(),
		'description'  => $a['desc'] !== '' ? $a['desc'] : wp_strip_all_tags( get_the_excerpt() ),
		'thumbnailUrl' => array( $thumb ),
		'uploadDate'   => $upload,
		'embedUrl'     => 'https://www.youtube-nocookie.com/embed/' . $vid,
		'contentUrl'   => 'https://www.youtube.com/watch?v=' . $vid,
	);
	if ( $a['duration'] !== '' ) {
		$schema['duration'] = $a['duration'];
	}

	ob_start();
	?>
	<div class="cfi-video">
		<button type="button" class="cfi-video-play" data-embed="<?php echo esc_url( $embed ); ?>"
			aria-label="<?php echo esc_attr( 'Play video: ' . $label ); ?>">
			<?php /* Never lazy: the facade is the LCP element of a video page.
			   Lazy-loading it measured a 5.9s LCP on the hub. */ ?>
			<img src="<?php echo esc_url( $thumb ); ?>" alt="" width="1280" height="720"
				fetchpriority="high" decoding="async"
				onerror="this.onerror=null;this.src='<?php echo esc_js( $fallb ); ?>'">
			<span class="cfi-video-icon" aria-hidden="true"></span>
			<?php if ( $a['title'] !== '' ) : ?>
				<span class="cfi-video-label"><?php echo esc_html( $a['title'] ); ?></span>
			<?php endif; ?>
		</button>
	</div>
	<script type="application/ld+json"><?php
		echo wp_json_encode( $schema, JSON_UNESCAPED_SLASHES | JSON_UNESCAPED_UNICODE );
	?></script>
	<?php
	return ob_get_clean();
} );

/**
 * Preconnect to YouTube's image CDN on pages that will fetch thumbnails.
 * The first-row thumbs are the hub's LCP candidates, and without this the
 * connection setup (DNS + TCP + TLS) to i.ytimg.com sits on the critical path.
 * Printed only where a video shortcode exists, so the other ~90 pages carry
 * no extra hint.
 */
add_action( 'wp_head', function () {
	global $post;
	if ( ! $post ) {
		return;
	}
	$c = (string) $post->post_content;
	if ( has_shortcode( $c, 'cfi_video' ) || has_shortcode( $c, 'cfi_videos' ) ) {
		echo '<link rel="preconnect" href="https://i.ytimg.com" crossorigin>' . "\n";
	}
}, 4 );

/**
 * One tiny script for every facade on the page, printed only when one exists.
 */
add_action( 'wp_footer', function () {
	global $post;
	if ( ! $post || ! has_shortcode( (string) $post->post_content, 'cfi_video' ) ) {
		return;
	}
	?>
	<script>
	document.addEventListener('click', function (e) {
		var b = e.target.closest('.cfi-video-play');
		if (!b) return;
		var f = document.createElement('iframe');
		f.src = b.dataset.embed;
		f.title = b.getAttribute('aria-label').replace(/^Play video: /, '');
		f.allow = 'accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture; web-share';
		f.allowFullscreen = true;
		f.loading = 'eager';
		b.parentNode.replaceChild(f, b);
		f.focus();
	});
	</script>
	<?php
}, 30 );

/**
 * Video hub: a grid of every published post in the "videos" category.
 *
 * Cards link to the individual video pages rather than embedding here, because
 * one video per URL with supporting text is what earns a video result.
 */
add_shortcode( 'cfi_videos', function ( $atts ) {
	$a = shortcode_atts( array(
		'category' => 'videos',
		'limit'    => 24,
	), $atts, 'cfi_videos' );

	$q = new WP_Query( array(
		'post_type'           => 'post',
		'category_name'       => $a['category'],
		'posts_per_page'      => (int) $a['limit'],
		'ignore_sticky_posts' => true,
		'no_found_rows'       => true,
	) );

	if ( ! $q->have_posts() ) {
		wp_reset_postdata();
		return current_user_can( 'edit_posts' )
			? '<p><strong>[cfi_videos]</strong> found no published posts in the &ldquo;'
				. esc_html( $a['category'] ) . '&rdquo; category yet.</p>'
			: '';
	}

	ob_start();
	echo '<div class="cfi-video-grid">';
	$i = 0;
	while ( $q->have_posts() ) {
		$q->the_post();
		$i++;
		// Pull the first video id out of the post so the card can show its thumbnail.
		$vid = '';
		if ( preg_match( '/\[cfi_video[^\]]*id=["\']([A-Za-z0-9_-]{11})["\']/', get_the_content(), $m ) ) {
			$vid = $m[1];
		}
		?>
		<a class="cfi-video-card" href="<?php the_permalink(); ?>">
			<?php if ( $vid ) :
				/* The first row holds the page's LCP image — lazy-loading it
				   measured LCP 5.9s vs the sub-3s the rest of the site gets.
				   Everything below the first row stays lazy. */
				$eager = $i <= 3; ?>
				<img src="<?php echo esc_url( 'https://i.ytimg.com/vi/' . $vid . '/mqdefault.jpg' ); ?>"
					alt="" width="320" height="180" decoding="async"
					<?php echo $eager ? 'fetchpriority="high"' : 'loading="lazy"'; ?>>
			<?php endif; ?>
			<span class="cfi-video-card-title"><?php the_title(); ?></span>
		</a>
		<?php
	}
	echo '</div>';
	wp_reset_postdata();
	return ob_get_clean();
} );
