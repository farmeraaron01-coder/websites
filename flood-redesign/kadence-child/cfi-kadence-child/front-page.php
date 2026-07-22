<?php
/**
 * Front page — California Flood Insurance.
 * Coded template per owner decision (no page builder). Header and footer
 * come from the Kadence header/footer builder; everything between is here.
 */
get_header();
$theme_uri = get_stylesheet_directory_uri();
?>
<main id="primary" class="cfi-home">

	<!-- Hero: raindrop video (desktop) / poster frame (mobile, reduced motion) -->
	<section class="cfi-hero">
		<div class="bg" aria-hidden="true">
			<img src="<?php echo esc_url( $theme_uri . '/assets/media/hero-poster.jpg' ); ?>" alt="" width="1280" height="720" fetchpriority="high">
			<video autoplay muted loop playsinline preload="metadata" poster="<?php echo esc_url( $theme_uri . '/assets/media/hero-poster.jpg' ); ?>">
				<source src="<?php echo esc_url( $theme_uri . '/assets/media/raindrops-hero.mp4' ); ?>" type="video/mp4">
			</video>
		</div>
		<div class="cfi-wrap">
			<div>
				<p class="cfi-eyebrow eyebrow-light">California-based &middot; Flood-focused &middot; Est. 2012</p>
				<h1>California floods.<br>Your premium <em>shouldn&rsquo;t.</em></h1>
				<p class="sub">We compare <strong>up to nine private flood markets, plus the NFIP</strong> when appropriate &mdash; and explain the tradeoffs in plain English, including when the federal program is your better fit. Options vary by property, eligibility, and carrier availability.</p>
				<div class="ctas">
					<a class="cfi-btn cfi-btn-cta" href="<?php echo esc_url( CFI_QUOTE_URL ); ?>">Start my quote</a>
					<a class="cfi-btn cfi-btn-ghost" href="tel:<?php echo esc_attr( CFI_PHONE_TEL ); ?>">&#9742; <?php echo esc_html( CFI_PHONE_DISPLAY ); ?></a>
				</div>
				<div class="cfi-chips">
					<span class="cfi-chip"><span class="star">&#9733;&#9733;&#9733;&#9733;&#9733;</span> 4.9 &middot; 900+ Google reviews</span>
					<span class="cfi-chip">40,000+ properties helped</span>
					<span class="cfi-chip"><?php echo esc_html( CFI_LICENSE ); ?></span>
				</div>
			</div>

			<aside class="cfi-qcard">
				<span class="ribbon">No obligation</span>
				<h2>Get a personalized flood quote</h2>
				<p class="qsub">Tell us about your property on our secure quote page. A licensed specialist compares available options and follows up promptly.</p>
				<ul class="cfi-qlist">
					<li>About 2 minutes to complete</li>
					<li>Up to 9 private flood markets + NFIP</li>
					<li>Home, business &amp; HOA / condo</li>
					<li>No obligation, no automated spam</li>
				</ul>
				<a class="cfi-btn cfi-btn-cta" href="<?php echo esc_url( CFI_QUOTE_URL ); ?>">Start My Quote &rarr;</a>
				<p class="cfi-qmicro">Prefer to talk? <a href="tel:<?php echo esc_attr( CFI_PHONE_TEL ); ?>">Call <?php echo esc_html( CFI_PHONE_DISPLAY ); ?></a></p>
				<div class="cfi-qtrust">
					<span><b>&#9733; 4.9</b> Google</span>
					<span><b>40,000+</b> helped</span>
					<span><b>Est.</b> 2012</span>
				</div>
			</aside>
		</div>
	</section>

	<!-- Markets bar -->
	<div class="cfi-markets">
		<div class="cfi-wrap">
			<span class="m-label">One request, compared across:</span>
			<span class="mk nfip">FEMA / NFIP</span>
			<span class="mk">Up to 9 private flood markets</span>
			<span class="m-note">Options vary by property, underwriting eligibility &amp; carrier availability</span>
		</div>
	</div>

	<!-- Process flow -->
	<section class="cfi-sec">
		<div class="cfi-wrap">
			<div class="cfi-sec-head">
				<p class="cfi-eyebrow">What to expect</p>
				<h2>What happens after you click Start My Quote.</h2>
				<p>No mystery, no phone tree &mdash; here&rsquo;s the actual timeline.</p>
			</div>
			<div class="cfi-flow">
				<div class="cfi-flow-row">
					<span class="cfi-flow-when">First 2 minutes</span>
					<div class="cfi-flow-body">
						<h3>Tell us about the property</h3>
						<p>Complete the secure quote request online, or call and we&rsquo;ll take it down for you. No obligation either way.</p>
					</div>
				</div>
				<div class="cfi-flow-row">
					<span class="cfi-flow-when">Same business day</span>
					<div class="cfi-flow-body">
						<h3>A licensed specialist compares your options</h3>
						<p>We review up to nine private flood markets plus the NFIP where appropriate, then walk you through price, limits, exclusions, waiting periods, and what your lender needs &mdash; including when the federal program is your better fit.</p>
					</div>
				</div>
				<div class="cfi-flow-row">
					<span class="cfi-flow-when">When you say go</span>
					<div class="cfi-flow-body">
						<h3>Choose, bind, and we handle the paperwork</h3>
						<p>Pay online or have us bill your mortgage company; we send your lender everything they need. Coverage begins after carrier approval, binding confirmation, and payment &mdash; often the same day.</p>
					</div>
				</div>
			</div>
		</div>
	</section>

	<!-- Coverage -->
	<section class="cfi-sec" id="coverage" style="background:var(--cfi-mist)">
		<div class="cfi-wrap">
			<div class="cfi-sec-head">
				<p class="cfi-eyebrow">Coverage</p>
				<h2>Flood is all we do &mdash; for every kind of property.</h2>
			</div>
			<div class="cfi-covers">
				<article class="cfi-cover">
					<span class="ic"><svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M3 10.5 12 3l9 7.5"/><path d="M5 9.5V21h14V9.5"/></svg></span>
					<h3>Residential flood</h3>
					<ul>
						<li>NFIP + private markets, quoted together</li>
						<li>Building, contents &amp; loss-of-use options</li>
						<li>Satisfies every lender requirement</li>
					</ul>
					<a href="/residential/">Explore residential &rarr;</a>
				</article>
				<article class="cfi-cover">
					<span class="ic"><svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M4 21V7l8-4 8 4v14"/><path d="M9 9h1M9 13h1M14 9h1M14 13h1"/><path d="M4 21h16"/></svg></span>
					<h3>Commercial flood</h3>
					<ul>
						<li>Buildings, inventory &amp; business income</li>
						<li>Excess layers above NFIP caps</li>
						<li>Multi-location portfolios welcome</li>
					</ul>
					<a href="/commercial/">Explore commercial &rarr;</a>
				</article>
				<article class="cfi-cover">
					<span class="ic"><svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M3 21V9l6-4 6 4"/><path d="M15 21V9l6-4v16"/><path d="M7 12h1M7 16h1M11 12h1M11 16h1"/></svg></span>
					<h3>Condo &amp; HOA (RCBAP)</h3>
					<ul>
						<li>Master policies for associations</li>
						<li>Gap coverage for unit owners</li>
						<li>Board-ready proposals &amp; comparisons</li>
					</ul>
					<a href="/hoa-master-flood-policies/">RCBAP review &rarr;</a>
				</article>
			</div>
		</div>
	</section>

	<!-- Private vs NFIP -->
	<section class="cfi-sec cfi-compare">
		<div class="cfi-wrap">
			<div class="cfi-sec-head">
				<p class="cfi-eyebrow">Independent advice</p>
				<h2>Private flood or NFIP? We compare both &mdash; honestly.</h2>
				<p>There is no one-size-fits-all answer. We look at your property, lender requirements, limits, and budget &mdash; then tell you plainly when the federal program is the better fit.</p>
			</div>
			<div class="cfi-compare-grid">
				<div>
					<div class="cfi-bignum">9<span style="color:var(--cfi-accent-bright)">+</span>NFIP<small>up to nine private flood markets, plus the NFIP when appropriate</small></div>
					<p class="note">Many clients save when we compare. Pricing varies by property, carrier, coverage, and eligibility &mdash; so we show you the tradeoffs, not just a number.</p>
				</div>
				<table class="cfi-rates">
					<caption>Typical differences we walk you through. NFIP figures per FEMA program rules; private terms vary by carrier and eligibility.</caption>
					<thead>
						<tr><th>What we compare</th><th class="num">NFIP</th><th class="num">Private flood</th></tr>
					</thead>
					<tbody>
						<tr><td>Building limit (home)</td><td class="num">$250,000 cap</td><td class="num hi">Higher limits often available</td></tr>
						<tr><td>Waiting period</td><td class="num">Typically 30 days</td><td class="num hi">Varies &mdash; often shorter</td></tr>
						<tr><td>Loss of use / living expenses</td><td class="num">Not covered</td><td class="num hi">Sometimes available</td></tr>
						<tr><td>Replacement-cost options</td><td class="num">Limited</td><td class="num hi">Broader options exist</td></tr>
					</tbody>
				</table>
			</div>
		</div>
	</section>

	<!-- Zones + premium factors -->
	<section class="cfi-sec cfi-zones">
		<div class="cfi-wrap">
			<div class="z-grid">
				<div>
					<p class="cfi-eyebrow">Flood zones, demystified</p>
					<h2 style="font-size:clamp(28px,3.4vw,40px);margin:10px 0 14px">Told you&rsquo;re in a flood zone? Start with your zone&rsquo;s guide.</h2>
					<p style="color:var(--cfi-ink-2)">Most people land here because a lender or escrow officer just named their zone. Every zone has a plain-English guide: what it means, whether coverage is required, and what drives your price.</p>
					<div class="cfi-zchips">
						<?php
						/* Adjust slugs to match the live zone-guide URLs. */
						$zones = array(
							'Zone X'               => '/flood-zone-x/',
							'Zone A'               => '/flood-zone-a/',
							'Zone AE'              => '/flood-zone-ae/',
							'Zones AH &amp; AO'    => '/flood-zones-ah-ao/',
							'Zones V &amp; VE'     => '/flood-zones-v-ve/',
							'Base Flood Elevation' => '/base-flood-elevation-bfe/',
							'Lender requirements'  => '/lender-requirements/',
						);
						foreach ( $zones as $label => $url ) {
							echo '<a class="cfi-zchip" href="' . esc_url( $url ) . '">' . wp_kses_post( $label ) . '</a>';
						}
						?>
					</div>
				</div>
				<div class="cfi-price-card">
					<h3>What actually decides your premium</h3>
					<p class="pc-sub">In plain English &mdash; no jargon required.</p>
					<ol>
						<li><span><b>Your flood zone</b> &mdash; the risk level FEMA assigns your address</span></li>
						<li><span><b>Your building</b> &mdash; rebuild cost, foundation, and first-floor height</span></li>
						<li><span><b>Your choices</b> &mdash; coverage limits and the deductible you pick</span></li>
						<li><span><b>The carrier</b> &mdash; the same house prices very differently market to market</span></li>
					</ol>
					<p class="pc-note"><b>Number 4 is why people call us.</b> We compare up to nine private markets plus the NFIP, so you see your best available price &mdash; not one company&rsquo;s take-it-or-leave-it rate.</p>
				</div>
			</div>
		</div>
	</section>

	<!-- Reviews: swap placeholders for a verified Google reviews feed at launch -->
	<section class="cfi-sec cfi-reviews">
		<div class="cfi-wrap">
			<div class="cfi-sec-head">
				<p class="cfi-eyebrow">Reviews</p>
				<h2>4.9 across 900+ Google reviews. Now on the page.</h2>
			</div>
			<div class="cfi-rev-grid">
				<div class="cfi-rev">
					<span class="stars" aria-label="5 stars">&#9733;&#9733;&#9733;&#9733;&#9733;</span>
					<blockquote>&ldquo;Placeholder &mdash; pull three current verified reviews from the Google profile before launch.&rdquo;</blockquote>
					<cite>M. G. <span>Sacramento &middot; Google review</span></cite>
				</div>
				<div class="cfi-rev">
					<span class="stars" aria-label="5 stars">&#9733;&#9733;&#9733;&#9733;&#9733;</span>
					<blockquote>&ldquo;Placeholder &mdash; pull three current verified reviews from the Google profile before launch.&rdquo;</blockquote>
					<cite>D. R. <span>Long Beach &middot; Google review</span></cite>
				</div>
				<div class="cfi-rev">
					<span class="stars" aria-label="5 stars">&#9733;&#9733;&#9733;&#9733;&#9733;</span>
					<blockquote>&ldquo;Placeholder &mdash; pull three current verified reviews from the Google profile before launch.&rdquo;</blockquote>
					<cite>S. T. <span>San Jose &middot; Google review</span></cite>
				</div>
			</div>
		</div>
	</section>

	<!-- Expert / E-E-A-T -->
	<section class="cfi-sec cfi-expert">
		<div class="cfi-wrap">
			<div class="x-grid">
				<img class="cfi-xphoto" src="<?php echo esc_url( $theme_uri . '/assets/img/aaron.png' ); ?>" alt="Aaron J. Farmer, founder of California Flood Insurance" width="132" height="132" loading="lazy">
				<div>
					<p class="cfi-eyebrow">Talk to a flood expert, not a call tree</p>
					<h2 style="font-size:clamp(24px,3vw,32px);margin:10px 0 12px">Every quote is reviewed by a licensed flood specialist.</h2>
					<p style="color:var(--cfi-ink-2);max-width:62ch">Aaron J. Farmer has worked in insurance since 1996 and specialized in flood since 2012, helping 40,000+ property owners and businesses. The specialist who reviews your quote is the same team your lender and escrow officer will talk to &mdash; and the same team that writes and reviews our guides.</p>
					<div class="cfi-xcreds">
						<span class="cfi-xcred"><?php echo esc_html( CFI_LICENSE ); ?></span>
						<span class="cfi-xcred">29+ years in insurance</span>
						<span class="cfi-xcred">Flood-focused since 2012</span>
						<span class="cfi-xcred">NFIP &amp; private markets</span>
					</div>
				</div>
			</div>
		</div>
	</section>

	<!-- Guides: latest four posts -->
	<section class="cfi-sec" style="padding-top:0">
		<div class="cfi-wrap">
			<div class="cfi-sec-head">
				<p class="cfi-eyebrow">Guides &amp; resources</p>
				<h2>Answers first. Sales pitch never.</h2>
			</div>
			<div class="cfi-guides-grid">
				<?php
				$guides = new WP_Query( array( 'posts_per_page' => 4, 'ignore_sticky_posts' => true, 'no_found_rows' => true ) );
				if ( $guides->have_posts() ) :
					while ( $guides->have_posts() ) :
						$guides->the_post();
						$cat = get_the_category();
						?>
						<article class="cfi-guide">
							<span class="g-tag"><?php echo $cat ? esc_html( $cat[0]->name ) : 'Guide'; ?></span>
							<h3><?php the_title(); ?></h3>
							<p>By <?php the_author(); ?> &middot; Updated <?php the_modified_date( 'M Y' ); ?></p>
							<a href="<?php the_permalink(); ?>">Read the guide &rarr;</a>
						</article>
						<?php
					endwhile;
					wp_reset_postdata();
				endif;
				?>
			</div>
		</div>
	</section>

	<!-- CTA band -->
	<section class="cfi-ctaband">
		<div class="cfi-wrap">
			<div>
				<h2>Know your options before the next storm.</h2>
				<p>The secure quote request takes about two minutes &mdash; online any time, or a licensed specialist at <b><?php echo esc_html( CFI_PHONE_DISPLAY ); ?></b>, Mon&ndash;Fri 8&ndash;5 PT.</p>
			</div>
			<a class="cfi-btn cfi-btn-cta" href="<?php echo esc_url( CFI_QUOTE_URL ); ?>">Start my quote</a>
		</div>
	</section>

</main>
<?php get_footer(); ?>
