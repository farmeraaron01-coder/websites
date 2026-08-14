"""Address -> FEMA flood zone, using only free government endpoints.

No API key, no registration, no cost, no third-party dependency. Two hops:

  1. US Census Geocoder      address -> longitude, latitude
  2. FEMA NFHL (ArcGIS REST) point   -> flood zone polygon

Measured 14 Aug 2026: about 0.7 seconds per address for both calls together.

THE BASE URL MOVED — this cost an hour
--------------------------------------
Every guide and most older code points at

    https://hazards.fema.gov/gis/nfhl/rest/services/public/NFHL/MapServer

That path now returns 404 behind a Tivoli error page, which looks like a network
problem rather than a retired endpoint. The live service is

    https://hazards.fema.gov/arcgis/rest/services/public/NFHL/MapServer

Layer 28 is "Flood Hazard Zones". Do not hard-code the layer id blindly; this
script resolves it by name so a FEMA reindex does not silently return the wrong
polygons.

WHAT COMES BACK
---------------
    FLD_ZONE    the zone letter: X, A, AE, AH, AO, VE, ...
    ZONE_SUBTY  the qualifier -- "AREA OF MINIMAL FLOOD HAZARD" and similar
    SFHA_TF     "T" or "F". THIS is the field that answers "is cover mandatory
                with a federally backed mortgage", not the letter.
    STATIC_BFE  base flood elevation where one is published (-9999 = none)

TWO THINGS THIS IS FOR
----------------------
1. Zone-tagging our own book, so an X-zone premium figure rests on thousands of
   rows instead of the eleven that currently carry a zone.
2. A public address-lookup tool. The largest query cluster on the site is
   flood-zone lookups (31.4% of impressions), and the top place-name queries are
   literally street addresses -- "525 b street san diego fema flood zone".

PRIVACY, AND IT MATTERS FOR USE 1
---------------------------------
Batch-tagging the book means sending customer property addresses to two federal
services. Census and FEMA are reasonable recipients and the addresses are not
secret, but this is still customer data leaving our systems, and the geocoded
output must be treated exactly like the source file: never committed, never
published below the suppression floor. Only the zone tag is ever aggregated.
"""
import json
import sys
import time
import urllib.parse
import urllib.request

CENSUS = "https://geocoding.geo.census.gov/geocoder/locations/onelineaddress"
NFHL = "https://hazards.fema.gov/arcgis/rest/services/public/NFHL/MapServer"
UA = {"User-Agent": "Mozilla/5.0 (compatible; CFI-zone-lookup)"}
PAUSE = 0.2          # be polite; these are free public services


def _get(url, timeout=60, tries=4):
    delay = 2
    for attempt in range(tries):
        try:
            req = urllib.request.Request(url, headers=UA)
            with urllib.request.urlopen(req, timeout=timeout) as r:
                return json.loads(r.read().decode()), None
        except Exception as e:
            err = str(e)[:70]
            if attempt < tries - 1:
                time.sleep(delay)
                delay *= 2
    return None, err


def hazard_layer_id():
    """Resolve by NAME, not by a hard-coded number. A hard-coded id that silently
    points at the wrong layer after a FEMA reindex would return plausible
    nonsense, which is the worst possible failure for this."""
    d, err = _get(f"{NFHL}?f=json")
    if d is None:
        raise RuntimeError(f"NFHL service unreachable: {err}")
    for l in d.get("layers", []):
        if "flood hazard zone" in l["name"].lower():
            return l["id"]
    raise RuntimeError("no 'Flood Hazard Zones' layer found -- FEMA changed the service")


def geocode(address):
    """Returns (lon, lat, matched_address) or None. The Census geocoder does not
    match every address -- rural routes, very new construction and PO boxes fail.
    A miss is a miss; do not fall back to a city centroid, which would produce a
    confident answer about the wrong place."""
    q = urllib.parse.urlencode({"address": address,
                                "benchmark": "Public_AR_Current", "format": "json"})
    d, _ = _get(f"{CENSUS}/onelineaddress?{q}" if False else f"{CENSUS}?{q}")
    if not d:
        return None
    m = d.get("result", {}).get("addressMatches", [])
    if not m:
        return None
    c = m[0]["coordinates"]
    return c["x"], c["y"], m[0]["matchedAddress"]


def zone_at(lon, lat, layer_id):
    """Returns the zone attributes, or None where FEMA has no mapped polygon.
    'No polygon' is NOT the same as 'Zone X' -- large parts of rural California
    are simply unmapped, and reporting those as minimal hazard would be wrong."""
    q = urllib.parse.urlencode({
        "geometry": f"{lon},{lat}", "geometryType": "esriGeometryPoint", "inSR": "4326",
        "spatialRel": "esriSpatialRelIntersects",
        "outFields": "FLD_ZONE,ZONE_SUBTY,SFHA_TF,STATIC_BFE",
        "returnGeometry": "false", "f": "json"})
    d, _ = _get(f"{NFHL}/{layer_id}/query?{q}")
    if not d:
        return None
    f = d.get("features", [])
    return f[0]["attributes"] if f else None


def lookup(address, layer_id=None):
    lid = layer_id if layer_id is not None else hazard_layer_id()
    g = geocode(address)
    if not g:
        return {"address": address, "status": "no_geocode_match"}
    lon, lat, matched = g
    z = zone_at(lon, lat, lid)
    if not z:
        return {"address": address, "matched": matched, "lat": lat, "lon": lon,
                "status": "not_mapped"}
    bfe = z.get("STATIC_BFE")
    return {
        "address": address, "matched": matched, "lat": lat, "lon": lon,
        "zone": z.get("FLD_ZONE"),
        "subtype": z.get("ZONE_SUBTY"),
        "in_sfha": z.get("SFHA_TF") == "T",
        "base_flood_elevation": None if bfe in (None, -9999) else bfe,
        "status": "ok",
    }


def main():
    if len(sys.argv) < 2:
        print(__doc__.strip().split("\n\n")[0])
        print("\nusage:  flood-zone-lookup.py \"915 I Street, Sacramento, CA\"")
        print("        flood-zone-lookup.py --file addresses.txt > zones.json")
        return 1
    lid = hazard_layer_id()
    if sys.argv[1] == "--file":
        out = []
        for i, line in enumerate(open(sys.argv[2]), 1):
            a = line.strip()
            if not a:
                continue
            out.append(lookup(a, lid))
            time.sleep(PAUSE)
            if i % 50 == 0:
                print(f"  {i} done", file=sys.stderr, flush=True)
        json.dump(out, sys.stdout, indent=1)
    else:
        r = lookup(" ".join(sys.argv[1:]), lid)
        print(json.dumps(r, indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main())
