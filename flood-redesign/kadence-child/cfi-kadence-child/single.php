<?php
/**
 * Single article — the 48 posts under /insights/.
 *
 * Uses Kadence's header and footer so the site chrome stays consistent;
 * only the article body is ours.
 */
get_header();
?>
<main id="main" class="cfi-home cfi-interior">
	<?php
	while ( have_posts() ) {
		the_post();
		get_template_part( 'parts/interior' );
	}
	?>
</main>
<?php
get_footer();
