<?php
/**
 * `[cfi_flood_zone_lookup]` — address to FEMA flood zone, in the visitor's browser.
 *
 * WHY THIS IS A SHORTCODE AND NOT JUST PASTED INTO THE PAGE
 * I tried the page-content route first and it failed on this site. Post content
 * runs through WordPress's content filters, and two of them destroy JavaScript:
 *
 *   wpautop     inserted 38 <p> and </p> tags INSIDE the <script> block
 *   wptexturize entity-encoded every `&&` into `&#038;&#038;`
 *
 * The live page threw "Invalid or unexpected token" three times and the tool did
 * nothing. Nothing in the editor hints at this; it only shows up in the rendered
 * output, which is why it was caught by driving a real browser at the published
 * page rather than by reading the draft.
 *
 * Output from a shortcode callback is not passed back through wpautop, so the
 * script survives intact. That is the whole reason this file exists.
 *
 * THE DATA
 * Two free government endpoints, no key, no registration:
 *
 *   US Census geocoder   address -> lon/lat.   Sends NO CORS header, so this
 *                        uses JSONP. That is not laziness; fetch() is blocked.
 *   FEMA NFHL (ArcGIS)   lon/lat -> zone polygon. Does send CORS, so fetch works.
 *                        Base URL note: hazards.fema.gov/gis/nfhl/... is RETIRED
 *                        and 404s behind an old IBM error page. Live path is
 *                        hazards.fema.gov/arcgis/...
 *
 * PRIVACY, AND IT IS A REAL SELLING POINT
 * Both calls happen in the visitor's browser. The address never reaches our
 * server, so we are not holding property addresses for people who only wanted to
 * check a map. The page says so, and it is true rather than decorative.
 *
 * ZONES ARE NOT PERMANENT — Aaron, 14 Aug 2026
 * FEMA redraws these lines: new studies, levee accreditation and de-accreditation,
 * development changing how water moves. A property in X today can be AE after the
 * next revision, and the reverse happens too. The tool therefore reports the
 * CURRENT EFFECTIVE map and says so on every result, and the page carries the
 * caveat properly rather than in small print. It is not a forecast and it knows
 * nothing about pending revisions or a LOMA/LOMR on an individual property.
 *
 * THREE DISTINCTIONS THE CODE REFUSES TO BLUR
 *   no geocode match  -> say so. Never fall back to a city centroid; a confident
 *                        answer about the wrong building is worse than no answer.
 *   no NFHL polygon   -> "not mapped", NEVER "Zone X". Parts of rural California
 *                        are genuinely unmapped and calling that minimal hazard
 *                        would be false.
 *   outside the SFHA  -> optional, not unnecessary. 29% of NFIP claims come from
 *                        moderate-to-low-risk areas.
 */

defined( 'ABSPATH' ) || exit;

function cfi_flood_zone_lookup_shortcode() {
	ob_start();
	?>
<div id="cfi-zt" style="margin:1.5rem 0;padding:1.25rem;border:1px solid #d6dbe1;border-radius:10px;background:#f8fafc">
	<label for="cfi-zt-addr" style="display:block;font-weight:600;margin-bottom:.4rem">Property address</label>
	<input id="cfi-zt-addr" type="text" autocomplete="street-address" placeholder="915 I Street, Sacramento, CA 95814"
		style="width:100%;padding:.7rem .8rem;font-size:1rem;border:1px solid #b9c2cc;border-radius:6px;box-sizing:border-box">
	<button id="cfi-zt-go" type="button"
		style="margin-top:.7rem;padding:.7rem 1.4rem;font-size:1rem;font-weight:600;border:0;border-radius:6px;background:#0b5cab;color:#fff;cursor:pointer">Look up my flood zone</button>
	<p id="cfi-zt-status" role="status" aria-live="polite" style="margin:.7rem 0 0;font-size:.95rem;color:#4a5560"></p>
	<div id="cfi-zt-result" style="margin-top:1rem"></div>
	<p style="margin:.9rem 0 0;font-size:.85rem;color:#6b7580">Runs in your browser against the U.S. Census geocoder and FEMA's flood map. Your address is not sent to us.</p>
</div>
<script>
(function(){
	var NFHL="https://hazards.fema.gov/arcgis/rest/services/public/NFHL/MapServer",
		LAYER=28,
		elA=document.getElementById("cfi-zt-addr"),
		elB=document.getElementById("cfi-zt-go"),
		elS=document.getElementById("cfi-zt-status"),
		elR=document.getElementById("cfi-zt-result");
	if(!elA||!elB) return;
	function say(m){ elS.textContent=m; }
	function box(html,tone){
		var c = tone==="high" ? "#b3261e" : (tone==="low" ? "#1b6b3a" : "#4a5560");
		elR.innerHTML='<div style="border-left:4px solid '+c+';padding:.9rem 1rem;background:#fff;border-radius:6px">'+html+'<\/div>';
	}
	function geocode(addr,cb){
		var name="cfiZt"+Date.now(), s=document.createElement("script"), done=false;
		function cleanup(){ try{ delete window[name]; }catch(e){ window[name]=undefined; } if(s.parentNode){ s.parentNode.removeChild(s); } }
		window[name]=function(d){ done=true; cleanup(); cb(null,d); };
		s.onerror=function(){ if(!done){ cleanup(); cb(new Error("unreachable")); } };
		setTimeout(function(){ if(!done){ cleanup(); cb(new Error("timeout")); } },15000);
		s.src="https://geocoding.geo.census.gov/geocoder/locations/onelineaddress?address="
			+encodeURIComponent(addr)+"&benchmark=Public_AR_Current&format=jsonp&callback="+name;
		document.body.appendChild(s);
	}
	function zoneAt(lon,lat,cb){
		var u=NFHL+"/"+LAYER+"/query?geometry="+lon+","+lat
			+"&geometryType=esriGeometryPoint&inSR=4326&spatialRel=esriSpatialRelIntersects"
			+"&outFields=FLD_ZONE,ZONE_SUBTY,SFHA_TF,STATIC_BFE&returnGeometry=false&f=json";
		fetch(u).then(function(r){ return r.json(); }).then(function(d){
			cb(null,(d.features && d.features[0]) ? d.features[0].attributes : null);
		}).catch(function(){ cb(new Error("fema")); });
	}
	function render(matched,z){
		if(!z){
			box("<strong>FEMA has no mapped flood zone for this location.<\/strong>"
				+"<p style='margin:.5rem 0 0'>Parts of California are not covered by a current flood map. That is not the same as being low risk — it means the hazard has not been mapped. We can check what a carrier will do with an unmapped address.<\/p>"
				+"<p style='margin:.7rem 0 0'><a href='/get-a-quote/'>Ask us about this address<\/a><\/p>");
			return;
		}
		var zone=z.FLD_ZONE||"unknown",
			sfha=(z.SFHA_TF==="T"),
			sub=z.ZONE_SUBTY||"",
			bfe=(z.STATIC_BFE && z.STATIC_BFE!==-9999) ? z.STATIC_BFE : null,
			h="<p style='margin:0 0 .4rem;font-size:.9rem;color:#6b7580'>"+matched+"<\/p>";
		h+="<p style='margin:0;font-size:1.5rem;font-weight:700'>Flood zone "+zone+"<\/p>";
		if(sub){ h+="<p style='margin:.2rem 0 0;color:#4a5560'>"+sub+"<\/p>"; }
		h+= sfha
			? "<p style='margin:.7rem 0 0'><strong>This is a Special Flood Hazard Area.<\/strong> If the property has a federally backed mortgage, your lender is required to make you carry flood insurance.<\/p>"
			: "<p style='margin:.7rem 0 0'><strong>This is outside the Special Flood Hazard Area.<\/strong> Flood insurance is not federally required here — it is your choice. It is also usually much cheaper, and 29% of NFIP flood claims come from areas like this one.<\/p>";
		if(bfe!==null){ h+="<p style='margin:.5rem 0 0'>Base flood elevation on the current map: <strong>"+bfe+" feet<\/strong>.<\/p>"; }
		h+="<p style='margin:.9rem 0 0;font-size:.9rem;color:#6b7580'>Per FEMA's National Flood Hazard Layer as it stands today. Maps get revised and zones change — see below.<\/p>";
		h+="<p style='margin:.9rem 0 0'><a href='/get-a-quote/' style='font-weight:600'>See what cover costs for this address<\/a><\/p>";
		box(h, sfha ? "high" : "low");
	}
	function run(){
		var a=(elA.value||"").trim();
		elR.innerHTML="";
		if(a.length<8){ say("Enter a full street address, including the city and state."); return; }
		elB.disabled=true; say("Looking up the address…");
		geocode(a,function(err,d){
			if(err){ elB.disabled=false; say("Could not reach the address service. Please try again, or call us and we will check it for you."); return; }
			var m=(d && d.result && d.result.addressMatches) || [];
			if(!m.length){
				elB.disabled=false; say("");
				box("<strong>That address could not be matched.<\/strong>"
					+"<p style='margin:.5rem 0 0'>This happens with new construction, rural routes and PO boxes — it does not mean anything about your flood risk. Try including the ZIP code, or ask us and we will look it up directly.<\/p>"
					+"<p style='margin:.7rem 0 0'><a href='/get-a-quote/'>Have us check it<\/a><\/p>");
				return;
			}
			var c=m[0].coordinates;
			say("Checking FEMA's flood map…");
			zoneAt(c.x,c.y,function(err2,z){
				elB.disabled=false;
				if(err2){ say("FEMA's map service did not respond. It has short outages — please try again shortly."); return; }
				say(""); render(m[0].matchedAddress,z);
			});
		});
	}
	elB.addEventListener("click",run);
	elA.addEventListener("keydown",function(e){ if(e.key==="Enter"){ e.preventDefault(); run(); } });
})();
</script>
	<?php
	return ob_get_clean();
}
add_shortcode( 'cfi_flood_zone_lookup', 'cfi_flood_zone_lookup_shortcode' );
