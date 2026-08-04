<?php
/**
 * Cognito Forms embeds via shortcode.
 *
 * Five production pages exist only to host an embed — /claims/, /agent-appointment/,
 * /staff-form/, /service-center/, /video/ — so the content migration produced
 * empty bodies for them: the converter strips <script> and <iframe> deliberately,
 * which is correct for the other 81 pages.
 *
 * A shortcode rather than raw markup in post content, because WordPress filters
 * script tags out of content depending on the saving user's capabilities and the
 * editor used — so a pasted embed can silently vanish on a later save. This keeps
 * the markup in the theme, under version control, and identical across both
 * sister sites.
 *
 * Usage:  [cfi_cognito form="31"]
 *         [cfi_cognito form="5" title="Start your flood quote"]
 *
 * The form key is shared across every CFI form; only the number changes.
 * Known forms: 5 = flood quote, 12 = service center, 31 = claims,
 *              34 = agent appointment.
 *
 * ---------------------------------------------------------------------------
 * CONVERSION TRACKING — why this file pushes a dataLayer event
 *
 * The GTM containers currently fire Google Ads conversions from click triggers
 * keyed on the visible text of the clicked element ("Click Text contains
 * Submit Application"). Two problems with that, both live today:
 *
 * 1. THE STAFF FORM COUNTS AS A PAID LEAD. /staff-form/ embeds form 5 — the
 *    same form as the public quote page — and its button carries the same
 *    "Submit Application" label. So every time the office takes a phone call
 *    and types it into the staff form, the click trigger fires and Google Ads
 *    records a conversion. That is precisely the metric pollution the staff
 *    form was given its own noindexed URL to avoid. A form id cannot tell the
 *    two apart; only the page can.
 *
 * 2. IT COUNTS CLICKS, NOT SUBMISSIONS. A click trigger fires when the button
 *    is pressed, including when validation rejects the form and no entry is
 *    ever created. Conversions inflate and Smart Bidding optimises toward
 *    people who fail to complete the form.
 *
 * The fix is an explicit event the page emits only on a genuine, successful
 * submission, carrying what the form was for:
 *
 *   dataLayer.push({
 *     event: 'cfi_form_submit',
 *     cfi_form_id:   '5',
 *     cfi_form_role: 'quote',     // quote | staff | service | claims | appointment
 *     cfi_is_lead:   true         // false for staff intake and service requests
 *   })
 *
 * In GTM: trigger the Ads conversion on Custom Event `cfi_form_submit` with
 * `cfi_is_lead` equal to true, and retire the click triggers. Keep a GA4 event
 * on the same custom event WITHOUT the is_lead condition, so staff volume is
 * still measurable — it just never reaches Ads.
 *
 * Fail-safe direction: role is derived from the form id, but any page whose
 * slug contains "staff" is forced to role=staff and is_lead=false regardless
 * of what the shortcode says. Forgetting the attribute cannot turn staff
 * intake into a paid conversion.
 */

define( 'CFI_COGNITO_KEY', '8nmcIcFF1k6xZNCBaOzZxQ' );

/**
 * What each known form is for, and whether a submission is a marketing lead.
 * Anything unlisted is role=other / is_lead=false: a new form has to be
 * declared here before it can count as a conversion.
 */
function cfi_cognito_roles() {
	return array(
		'5'  => array( 'quote', true ),
		'12' => array( 'service', false ),        // existing policyholder service request
		'31' => array( 'claims', false ),         // existing policyholder reporting a loss
		'34' => array( 'appointment', false ),    // agent asking to be appointed, not a customer
		/*
		 * Used by /contact-us/ on both production sites. Declared so the event
		 * reports role=contact rather than the role=other fallback, which is all
		 * this changes: is_lead stays false, so it cannot reach Ads. Google Ads
		 * does have a historical "Contact_Form_Submission" action on both
		 * brands — if contact enquiries should count as leads again, flip this
		 * to true deliberately rather than by accident.
		 */
		'57' => array( 'contact', false ),
	);
}

add_shortcode( 'cfi_cognito', function ( $atts ) {
	$a = shortcode_atts( array(
		'form'  => '',
		'title' => '',
		'key'   => CFI_COGNITO_KEY,
		'role'  => '',   // override the derived role; "staff" is also forced by slug
	), $atts, 'cfi_cognito' );

	// Form ids are numeric; refuse anything else rather than echo it into a tag.
	if ( ! preg_match( '/^\d+$/', (string) $a['form'] ) ) {
		return current_user_can( 'edit_posts' )
			? '<p><strong>[cfi_cognito]</strong> needs a numeric <code>form</code> attribute.</p>'
			: '';
	}

	$roles = cfi_cognito_roles();
	$known = $roles[ (string) $a['form'] ] ?? array( 'other', false );
	$role    = $a['role'] !== '' ? sanitize_key( $a['role'] ) : $known[0];
	$is_lead = ( 'staff' !== $role ) && $known[1];

	/*
	 * Fail-safe: a staff-intake page can never report a marketing lead, whatever
	 * the shortcode was given. Checked against the queried page's slug rather
	 * than the request URI so a query string cannot dodge it.
	 */
	$slug = get_queried_object() instanceof WP_Post ? (string) get_queried_object()->post_name : '';
	if ( false !== strpos( $slug, 'staff' ) ) {
		$role    = 'staff';
		$is_lead = false;
	}

	cfi_cognito_track( $a['form'], $role, $is_lead );

	$out = '<div class="cfi-embed" data-cfi-form="' . esc_attr( $a['form'] ) . '" data-cfi-role="' . esc_attr( $role ) . '">';
	if ( $a['title'] !== '' ) {
		$out .= '<h2 class="cfi-embed-title">' . esc_html( $a['title'] ) . '</h2>';
	}
	$out .= '<script src="https://www.cognitoforms.com/f/seamless.js"'
		. ' data-key="' . esc_attr( $a['key'] ) . '"'
		. ' data-form="' . esc_attr( $a['form'] ) . '"></script>';
	$out .= '<noscript><p>This form needs JavaScript. Call '
		. esc_html( CFI_PHONE_DISPLAY ) . ' and a licensed specialist will help you directly.</p></noscript>';
	$out .= '</div>';

	return $out;
} );

/**
 * Record that a form was rendered on this request, so the footer knows what to
 * report. Static rather than a global: templates that embed a form directly
 * (the PPC landing page) call this too.
 */
function cfi_cognito_track( $form = null, $role = 'other', $is_lead = false ) {
	static $forms = array();
	if ( null === $form ) {
		return $forms;
	}
	$forms[] = array(
		'id'   => (string) $form,
		'role' => (string) $role,
		'lead' => (bool) $is_lead,
	);
	return $forms;
}

/**
 * Emit the submission event.
 *
 * Two detection paths, because one of them is documented and the other is
 * observable:
 *
 *  - Cognito's own event emitter (`Cognito.on('afterSubmit')`) is the correct
 *    hook and fires with the entry, so it only runs on a real submission.
 *  - A MutationObserver watching for Cognito's confirmation node is the
 *    fallback, in case the emitter's event name changes under us. It also only
 *    sees successful submissions, since the confirmation is what replaces the
 *    form after the entry is accepted.
 *
 * Whichever fires first wins; a flag stops the other from reporting the same
 * submission twice.
 */
add_action( 'wp_footer', function () {
	$forms = cfi_cognito_track();
	if ( ! $forms ) {
		return;
	}
	// One event per page describes the page's primary form — the first rendered.
	$f = $forms[0];
	?>
	<script>
	(function () {
		var sent = false;
		var payload = {
			event: 'cfi_form_submit',
			cfi_form_id: <?php echo wp_json_encode( $f['id'] ); ?>,
			cfi_form_role: <?php echo wp_json_encode( $f['role'] ); ?>,
			cfi_is_lead: <?php echo $f['lead'] ? 'true' : 'false'; ?>
		};
		function report(source) {
			if (sent) return;
			sent = true;
			window.dataLayer = window.dataLayer || [];
			payload.cfi_detected_by = source;
			window.dataLayer.push(payload);
		}
		function bindApi() {
			if (!window.Cognito || typeof window.Cognito.on !== 'function') return false;
			try { window.Cognito.on('afterSubmit', function () { report('api'); }); return true; }
			catch (e) { return false; }
		}
		if (!bindApi()) {
			var tries = 0,
				poll = setInterval(function () {
					if (bindApi() || ++tries > 40) clearInterval(poll);
				}, 250);
		}
		if (window.MutationObserver) {
			new MutationObserver(function (muts) {
				for (var i = 0; i < muts.length; i++) {
					var added = muts[i].addedNodes;
					for (var j = 0; j < added.length; j++) {
						var n = added[j];
						if (n.nodeType !== 1) continue;
						var c = String(n.className || '');
						if (c.indexOf('cog-confirmation') > -1 ||
							(n.querySelector && n.querySelector('[class*="cog-confirmation"]'))) {
							report('confirmation');
							return;
						}
					}
				}
			}).observe(document.body, { childList: true, subtree: true });
		}
	})();
	</script>
	<?php
}, 40 );
