<?php
/**
 * Interior layout — shared by single.php (articles) and the Guide page template
 * (zone pages, city pages).
 *
 * The h1 comes from this template, never from the content. That is deliberate:
 * 19 pages on the production site have no h1 at all, including every city page
 * and two zone pages, because Divi authors started at h2. Owning the h1 here
 * makes that defect structurally impossible to migrate.
 */

$post_id    = get_the_ID();
$theme_uri  = get_stylesheet_directory_uri();
$badge      = trim( (string) get_post_meta( $post_id, '_cfi_badge', true ) );
$risk       = cfi_risk_class( $post_id );
$standfirst = trim( (string) get_post_meta( $post_id, '_cfi_standfirst', true ) );
$takeaways  = cfi_takeaways( $post_id );

$built = cfi_build_toc( apply_filters( 'the_content', get_the_content() ) );
?>
<article class="cfi-doc" id="post-<?php echo (int) $post_id; ?>">

	<header class="cfi-doc-head">
		<div class="cfi-wrap">
			<?php if ( function_exists( 'rank_math_the_breadcrumbs' ) ) : ?>
				<nav class="cfi-crumbs" aria-label="Breadcrumb"><?php rank_math_the_breadcrumbs(); ?></nav>
			<?php endif; ?>

			<?php if ( $badge ) : ?>
				<p class="cfi-badge<?php echo $risk ? ' is-' . esc_attr( $risk ) : ''; ?>">
					<?php echo esc_html( $badge ); ?>
					<?php if ( $risk ) : ?><span><?php echo esc_html( ucfirst( $risk ) ); ?> risk</span><?php endif; ?>
				</p>
			<?php endif; ?>

			<h1><?php the_title(); ?></h1>

			<?php if ( $standfirst ) : ?>
				<p class="cfi-standfirst"><?php echo esc_html( $standfirst ); ?></p>
			<?php endif; ?>

			<div class="cfi-byline">
				<img src="<?php echo esc_url( $theme_uri . '/assets/img/aaron.jpg' ); ?>"
				     alt="" width="80" height="100" loading="lazy" decoding="async">
				<p>
					Reviewed by <b>Aaron J. Farmer</b>, licensed flood specialist
					<span><?php echo esc_html( CFI_LICENSE ); ?>
					&middot; Last reviewed <?php echo esc_html( cfi_reviewed_date( $post_id ) ); ?></span>
				</p>
			</div>
		</div>
	</header>

	<div class="cfi-wrap cfi-doc-grid">
		<div class="cfi-doc-body">

			<?php if ( $takeaways ) : ?>
				<aside class="cfi-takeaways" aria-labelledby="cfi-tk">
					<h2 id="cfi-tk">What to know</h2>
					<ul>
						<?php foreach ( $takeaways as $line ) : ?>
							<li><?php echo wp_kses_post( $line ); ?></li>
						<?php endforeach; ?>
					</ul>
				</aside>
			<?php endif; ?>

			<?php if ( $built['toc'] ) : ?>
				<nav class="cfi-toc" aria-labelledby="cfi-toc-h">
					<h2 id="cfi-toc-h">On this page</h2>
					<ol>
						<?php foreach ( $built['toc'] as $item ) : ?>
							<li class="lvl-<?php echo (int) $item['level']; ?>">
								<a href="#<?php echo esc_attr( $item['id'] ); ?>"><?php echo esc_html( $item['title'] ); ?></a>
							</li>
						<?php endforeach; ?>
					</ol>
				</nav>
			<?php endif; ?>

			<div class="cfi-prose">
				<?php echo $built['content']; // Already through the_content filters. ?>
			</div>

			<section class="cfi-doc-cta">
				<h2>Get a flood quote for your property</h2>
				<p>A licensed specialist compares available private markets and the NFIP, then explains the options in plain English &mdash; including when the NFIP is the better fit.</p>
				<p class="cfi-doc-cta-row">
					<a class="cfi-btn cfi-btn-cta" href="<?php echo esc_url( CFI_QUOTE_URL ); ?>">Start my quote</a>
					<a class="cfi-btn cfi-btn-ghost" href="tel:<?php echo esc_attr( CFI_PHONE_TEL ); ?>">&#9742; <?php echo esc_html( CFI_PHONE_DISPLAY ); ?></a>
				</p>
			</section>
		</div>

		<aside class="cfi-doc-rail">
			<div class="cfi-rail-card cfi-rail-quote">
				<p class="cfi-rail-stars" aria-label="Rated 4.9 out of 5">
					<span>&#9733;&#9733;&#9733;&#9733;&#9733;</span> 4.9 &middot; 900+ Google reviews
				</p>
				<p><b>Not sure which coverage applies to your property?</b></p>
				<a class="cfi-btn cfi-btn-cta" href="<?php echo esc_url( CFI_QUOTE_URL ); ?>">Start my quote</a>
				<a class="cfi-rail-tel" href="tel:<?php echo esc_attr( CFI_PHONE_TEL ); ?>"><?php echo esc_html( CFI_PHONE_DISPLAY ); ?></a>
				<p class="cfi-rail-hours">Mon&ndash;Fri 7:30am&ndash;5pm PT</p>
			</div>

			<?php
			$related = new WP_Query( array(
				'post_type'           => array( 'post', 'page' ),
				'posts_per_page'      => 5,
				'post__not_in'        => array( $post_id ),
				'orderby'             => 'modified',
				'ignore_sticky_posts' => true,
				'no_found_rows'       => true,
				'meta_query'          => array(
					array( 'key' => '_cfi_badge', 'compare' => 'EXISTS' ),
				),
			) );
			if ( $related->have_posts() ) : ?>
				<div class="cfi-rail-card">
					<h2 class="cfi-rail-h">Related guides</h2>
					<ul class="cfi-rail-links">
						<?php while ( $related->have_posts() ) : $related->the_post(); ?>
							<li><a href="<?php the_permalink(); ?>"><?php the_title(); ?></a></li>
						<?php endwhile; ?>
					</ul>
				</div>
			<?php endif; wp_reset_postdata(); ?>
		</aside>
	</div>
</article>
