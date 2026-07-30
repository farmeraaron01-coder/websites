<?php
/**
 * Template Name: CFI Guide (zone / city / long-form page)
 *
 * Selectable from the page editor. Intended for the zone pages, the city
 * pages, and any long-form page that benefits from a table of contents,
 * a takeaways box and a reviewed-by byline.
 *
 * Set these fields on the page to light up the optional blocks:
 *   _cfi_badge       "Flood Zone AE"        → badge above the h1
 *   _cfi_risk        high | moderate | low  → badge colour
 *   _cfi_standfirst  one-line summary       → sits under the h1
 *   _cfi_takeaways   one bullet per line    → the "What to know" box
 *   _cfi_reviewed    YYYY-MM-DD             → byline date (else modified date)
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
