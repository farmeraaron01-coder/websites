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
<style>
#cfi-zt{--zt-line:#d6dbe1;--zt-ink:#1f2933;--zt-mute:#6b7580;margin:1.75rem 0;font-synthesis:none}
#cfi-zt *{box-sizing:border-box}
.zt-card{border:1px solid var(--zt-line);border-radius:14px;background:linear-gradient(180deg,#fbfdff,#f4f7fa);padding:1.4rem;box-shadow:0 1px 2px rgba(16,24,40,.04)}
.zt-h{font-weight:700;font-size:1.05rem;margin:0 0 .2rem;color:var(--zt-ink)}
.zt-sub{margin:0 0 .9rem;font-size:.92rem;color:var(--zt-mute)}
.zt-row{display:flex;gap:.6rem;flex-wrap:wrap}
.zt-row input{flex:1 1 16rem;min-width:0;padding:.85rem .9rem;font-size:1rem;border:1px solid #b9c2cc;border-radius:9px;background:#fff}
.zt-row input:focus{outline:2px solid #0b5cab;outline-offset:1px;border-color:#0b5cab}
.zt-btn{flex:0 0 auto;padding:.85rem 1.5rem;font-size:1rem;font-weight:650;border:0;border-radius:9px;background:#0b5cab;color:#fff;cursor:pointer;transition:background .15s}
.zt-btn:hover{background:#094a8c}.zt-btn:disabled{background:#8fa6bd;cursor:progress}
.zt-status{margin:.75rem 0 0;font-size:.93rem;color:var(--zt-mute);min-height:1.2em}
.zt-priv{margin:.8rem 0 0;font-size:.82rem;color:var(--zt-mute)}
.zt-out{margin-top:1rem}
.zt-res{border-radius:12px;overflow:hidden;border:1px solid var(--zt-line);background:#fff}
.zt-band{padding:.55rem 1.1rem;font-size:.8rem;font-weight:700;letter-spacing:.05em;text-transform:uppercase;color:#fff}
.zt-band.hi{background:#b3261e}.zt-band.lo{background:#1b6b3a}.zt-band.un{background:#5a6672}
.zt-body{padding:1.1rem}
.zt-addr{margin:0 0 .35rem;font-size:.85rem;color:var(--zt-mute)}
.zt-zone{margin:0;font-size:2.1rem;line-height:1.1;font-weight:750;color:var(--zt-ink)}
.zt-desc{margin:.3rem 0 0;color:#4a5560}
.zt-note{margin:.85rem 0 0}
.zt-facts{margin:.9rem 0 0;padding:.75rem .9rem;background:#f6f8fb;border-radius:9px;font-size:.93rem}
.zt-facts div{display:flex;justify-content:space-between;gap:1rem;padding:.15rem 0}
.zt-facts span:last-child{font-weight:650;color:var(--zt-ink)}
.zt-cta{display:inline-block;margin:1rem .5rem 0 0;padding:.8rem 1.35rem;border-radius:9px;background:#0b5cab;color:#fff !important;font-weight:650;text-decoration:none}
.zt-cta.alt{background:#fff;color:#0b5cab !important;border:1.5px solid #0b5cab}
.zt-stale{margin:.9rem 0 0;font-size:.84rem;color:var(--zt-mute);border-top:1px solid var(--zt-line);padding-top:.7rem}
@media(max-width:560px){.zt-btn{flex:1 1 100%}.zt-zone{font-size:1.7rem}}
</style>
<div id="cfi-zt">
	<div class="zt-card">
		<p class="zt-h"><label for="cfi-zt-addr">What flood zone is this address in?</label></p>
		<p class="zt-sub">Checked live against FEMA&rsquo;s National Flood Hazard Layer &mdash; the map lenders and insurers use.</p>
		<div class="zt-row">
			<input id="cfi-zt-addr" type="text" autocomplete="street-address" placeholder="915 I Street, Sacramento, CA 95814">
			<button id="cfi-zt-go" class="zt-btn" type="button">Check this address</button>
		</div>
		<p id="cfi-zt-status" class="zt-status" role="status" aria-live="polite"></p>
		<div id="cfi-zt-result" class="zt-out"></div>
		<p class="zt-priv">Runs in your browser and talks straight to the U.S. Census geocoder and FEMA. Your address is never sent to us.</p>
	</div>
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
	/* Send each zone on to the page that already ranks for it. The tool feeds those
	   pages rather than competing with them. */
	function guide(z){
		z=(z||"").toUpperCase();
		if(z.indexOf("X")===0||z==="B"||z==="C"){ return {u:"/navigating-flood-zone-x/",t:"What Zone X actually means"}; }
		if(z==="AE"||/^A\d/.test(z)){ return {u:"/flood-zone-ae/",t:"What Zone AE means"}; }
		if(z==="AH"||z==="AO"){ return {u:"/flood-zone-ah-and-ao/",t:"What Zones AH and AO mean"}; }
		if(z.indexOf("V")===0){ return {u:"/flood-zone-v-and-ve/",t:"What Zones V and VE mean"}; }
		if(z==="A"||z==="A99"||z==="AR"){ return {u:"/flood-zone-a/",t:"What Zone A means"}; }
		return {u:"/which-flood-zone-requires-flood-insurance/",t:"Which zones require flood insurance"};
	}
	function shell(band,cls,body){
		elR.innerHTML='<div class="zt-res"><div class="zt-band '+cls+'">'+band+'<\/div><div class="zt-body">'+body+'<\/div><\/div>';
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
			shell("Not mapped","un",
				"<p class='zt-zone' style='font-size:1.35rem'>FEMA has no mapped zone here<\/p>"
				+"<p class='zt-note'>Parts of California have never been mapped. That is <strong>not<\/strong> the same as low risk &mdash; it means the hazard was never studied, and carriers treat unmapped addresses differently from one another.<\/p>"
				+"<a class='zt-cta' href='/get-a-quote/'>Have us check this address<\/a>");
			return;
		}
		var zone=z.FLD_ZONE||"unknown", sfha=(z.SFHA_TF==="T"), sub=z.ZONE_SUBTY||"",
			bfe=(z.STATIC_BFE && z.STATIC_BFE!==-9999) ? z.STATIC_BFE : null,
			g=guide(zone), h="";
		h+="<p class='zt-addr'>"+matched+"<\/p>";
		h+="<p class='zt-zone'>Zone "+zone+"<\/p>";
		if(sub){ h+="<p class='zt-desc'>"+sub.toLowerCase().replace(/^./,function(c){return c.toUpperCase();})+"<\/p>"; }
		h+="<div class='zt-facts'>";
		h+="<div><span>Special Flood Hazard Area<\/span><span>"+(sfha?"Yes":"No")+"<\/span><\/div>";
		h+="<div><span>Insurance required by a federally backed lender<\/span><span>"+(sfha?"Yes":"No")+"<\/span><\/div>";
		h+="<div><span>Base flood elevation on the current map<\/span><span>"+(bfe!==null?(bfe+" ft"):"Not published for this zone")+"<\/span><\/div>";
		h+="<\/div>";
		if(sfha){
			h+="<p class='zt-note'><strong>Your lender will require flood insurance here.<\/strong> That is not a choice, but <em>who you buy it from<\/em> is. We quote the federal program and the private market side by side and place whichever is better for the building &mdash; and private policies can also cover temporary housing, which the federal policy never does.<\/p>";
			h+="<a class='zt-cta' href='/get-a-quote/'>Quote both markets for this address<\/a>";
		}else{
			h+="<p class='zt-note'><strong>Nobody is going to make you buy this &mdash; which is exactly why it is worth a minute.<\/strong> Outside the high-risk zone cover is optional and it is cheap: in Zone X we typically place private policies around <strong>$450 a year<\/strong>, all in. And <strong>29%<\/strong> of federal flood claims come from areas rated moderate to low risk, like this one.<\/p>";
			h+="<a class='zt-cta' href='/get-a-quote/'>See the price for this address<\/a>";
		}
		if(g){ h+="<a class='zt-cta alt' href='"+g.u+"'>"+g.t+"<\/a>"; }
		h+="<p class='zt-stale'>This is the FEMA map in effect today. Zones change when FEMA revises a map, and a single property can be redrawn on its own by a Letter of Map Amendment. If a lender or an escrow deadline is riding on this, confirm it at the point of purchase.<\/p>";
		shell(sfha?"High-risk zone &mdash; cover mandatory":"Outside the high-risk zone &mdash; cover optional", sfha?"hi":"lo", h);
	}
	function run(){
		var a=(elA.value||"").trim();
		elR.innerHTML="";
		if(a.length<8){ say("Enter a full street address, including the city and state."); return; }
		elB.disabled=true; say("Locating the address…");
		geocode(a,function(err,d){
			if(err){ elB.disabled=false; say("Could not reach the address service. Try again in a moment, or call us and we will look it up for you."); return; }
			var m=(d && d.result && d.result.addressMatches) || [];
			if(!m.length){
				elB.disabled=false; say("");
				shell("No match","un",
					"<p class='zt-zone' style='font-size:1.35rem'>That address could not be matched<\/p>"
					+"<p class='zt-note'>This is common with new construction, rural routes and PO boxes, and it says nothing about your flood risk. Try adding the ZIP code &mdash; or let us look it up directly.<\/p>"
					+"<a class='zt-cta' href='/get-a-quote/'>Have us check it<\/a>");
				return;
			}
			var c=m[0].coordinates;
			say("Reading FEMA’s flood map…");
			zoneAt(c.x,c.y,function(err2,z){
				elB.disabled=false;
				if(err2){ say("FEMA’s map service did not respond. It has short outages — please try again shortly."); return; }
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
