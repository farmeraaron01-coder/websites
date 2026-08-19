import os
OUT="/home/user/websites/seo/statewide-flood-insurance/charts"

TEAL="#0A9B95"; INK="#12283f"; SEC="#4a5a66"; MUT="#7f8d97"; RULE="#dfe4e7"
FONT='-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Helvetica,Arial,sans-serif'

def esc(s): return s.replace("&","&amp;").replace("<","&lt;").replace(">","&gt;")

def bar_chart(state, rows, n_total, fname, desc):
    """rows: [(label, median, n)] sorted desc"""
    W=720; PADL=104; PADR=88; TOP=64; BH=34; GAP=14; BOT=52
    H=TOP+len(rows)*(BH+GAP)-GAP+BOT
    mx=max(r[1] for r in rows); scale=(W-PADL-PADR)/ (mx*1.06)
    t=f"{state} median annual private flood premium by FEMA flood zone"
    p=[]
    p.append(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="100%" height="auto" '
             f'role="img" aria-labelledby="t-{fname} d-{fname}" style="max-width:{W}px;font-family:{FONT}">')
    p.append(f'<title id="t-{fname}">{esc(t)}</title>')
    p.append(f'<desc id="d-{fname}">{esc(desc)}</desc>')
    p.append(f'<text x="0" y="24" font-size="17" font-weight="700" fill="{INK}">{esc(state)} flood insurance cost by zone</text>')
    p.append(f'<text x="0" y="45" font-size="13" fill="{SEC}">Median all-in annual premium, {n_total} properties quoted Feb 2025 – Aug 2026</text>')
    y=TOP
    for label,val,n in rows:
        bw=val*scale
        p.append(f'<text x="{PADL-12}" y="{y+BH/2+5}" text-anchor="end" font-size="14" font-weight="600" fill="{INK}">{esc(label)}</text>')
        p.append(f'<rect x="{PADL}" y="{y}" width="{bw:.1f}" height="{BH}" rx="4" fill="{TEAL}"/>')
        p.append(f'<text x="{PADL+bw+10:.1f}" y="{y+BH/2+1}" font-size="14" font-weight="700" fill="{INK}">${val}</text>')
        p.append(f'<text x="{PADL+bw+10:.1f}" y="{y+BH/2+15}" font-size="11.5" fill="{MUT}">{n} quoted</text>')
        y+=BH+GAP
    p.append(f'<line x1="{PADL}" y1="{TOP-8}" x2="{PADL}" y2="{y-GAP+8}" stroke="{RULE}" stroke-width="1"/>')
    p.append(f'<text x="0" y="{H-16}" font-size="11.5" fill="{MUT}">Statewide Flood Insurance · one row per property · all-in = premium, policy fee and surplus lines taxes</text>')
    p.append('</svg>')
    open(os.path.join(OUT,fname+".svg"),"w").write("\n".join(p))
    return H

def range_chart(rows, fname):
    """rows: [(state, med, p25, p75, n)] sorted desc by median"""
    W=800; PADL=196; PADR=34; TOP=78; RH=21; BOT=58   # PADL includes a value column
    H=TOP+len(rows)*RH+BOT
    mx=max(r[3] for r in rows); axmax=1600
    sc=(W-PADL-PADR)/axmax
    p=[]
    t="Median and typical range of private flood insurance premiums across 27 states"
    d=("Range plot. For each of 27 states a horizontal line spans the middle half of quotes "
       "(25th to 75th percentile) and a dot marks the median. Medians run from $369 in Michigan "
       "to $869 in Connecticut. Alabama has the widest typical range, $539 to $1,592.")
    p.append(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="100%" height="auto" '
             f'role="img" aria-labelledby="t-hub d-hub" style="max-width:{W}px;font-family:{FONT}">')
    p.append(f'<title id="t-hub">{esc(t)}</title><desc id="d-hub">{esc(d)}</desc>')
    p.append(f'<text x="0" y="24" font-size="17" font-weight="700" fill="{INK}">What private flood insurance costs, by state</text>')
    p.append(f'<text x="0" y="45" font-size="13" fill="{SEC}">Median all-in annual premium and the middle half of quotes, 7,165 properties, Feb 2025 – Aug 2026</text>')
    for gx in range(0,axmax+1,400):
        x=PADL+gx*sc
        p.append(f'<line x1="{x:.1f}" y1="{TOP-10}" x2="{x:.1f}" y2="{TOP+len(rows)*RH+4}" stroke="{RULE}" stroke-width="1"/>')
        p.append(f'<text x="{x:.1f}" y="{TOP-18}" text-anchor="middle" font-size="11.5" fill="{MUT}">${gx:,}</text>')
    y=TOP+RH/2
    for st,med,p25,p75,n in rows:
        x1=PADL+p25*sc; x2=PADL+p75*sc; xm=PADL+med*sc
        p.append(f'<text x="{PADL-74}" y="{y+4}" text-anchor="end" font-size="12.5" fill="{INK}">{esc(st)}</text>')
        p.append(f'<text x="{PADL-22}" y="{y+4}" text-anchor="end" font-size="12.5" font-weight="700" fill="{INK}">${med}</text>')
        p.append(f'<line x1="{x1:.1f}" y1="{y:.1f}" x2="{x2:.1f}" y2="{y:.1f}" stroke="{TEAL}" stroke-width="2.5" stroke-linecap="round" opacity="0.42"/>')
        p.append(f'<circle cx="{xm:.1f}" cy="{y:.1f}" r="5" fill="{TEAL}" stroke="#ffffff" stroke-width="2"/>')
        y+=RH
    p.append(f'<line x1="{PADL-16}" y1="{TOP-10}" x2="{PADL-16}" y2="{TOP+len(rows)*RH+4}" stroke="{RULE}" stroke-width="1"/>')
    p.append(f'<text x="0" y="{H-30}" font-size="11.5" fill="{MUT}">Bold figure and dot = median · bar = middle half of quotes (25th–75th percentile) · one row per property</text>')
    p.append(f'<text x="0" y="{H-14}" font-size="11.5" fill="{MUT}">Statewide Flood Insurance · states with at least 50 quoted properties</text>')
    p.append('</svg>')
    open(os.path.join(OUT,fname+".svg"),"w").write("\n".join(p))
    return H

bar_chart("Arizona",[("Zone AE",581,107),("Zone X",568,32),("Zone A",558,36),("Zone AO",464,23)],203,
  "arizona-flood-insurance-cost-by-zone",
  "Horizontal bar chart. Zone AE $581 from 107 properties, Zone X $568 from 32, Zone A $558 from 36, Zone AO $464 from 23. Arizona median across all zones is $547.")
bar_chart("Oklahoma",[("Zone AE",519,47),("Zone A",470,20),("Zone X",372,23)],93,
  "oklahoma-flood-insurance-cost-by-zone",
  "Horizontal bar chart. Zone AE $519 from 47 properties, Zone A $470 from 20, Zone X $372 from 23. Oklahoma median across all zones is $465.")
bar_chart("Texas",[("Zone AE",892,108),("Zone X",614,212),("Zone A",582,32)],367,
  "texas-flood-insurance-cost-by-zone",
  "Horizontal bar chart. Zone AE $892 from 108 properties, Zone X $614 from 212, Zone A $582 from 32. Texas median across all zones is $670.")
bar_chart("Florida",[("Zone AE",895,103),("Zone AH",824,13),("Zone X",617,198),("Zone A",562,24)],342,
  "florida-flood-insurance-cost-by-zone",
  "Horizontal bar chart. Zone AE $895 from 103 properties, Zone AH $824 from 13, Zone X $617 from 198, Zone A $562 from 24. Florida median across all zones is $681.")

hub=[("Connecticut",869,623,1162,134),("Alabama",782,539,1592,99),("Oregon",760,639,883,219),
("New Jersey",748,430,1143,134),("California",719,509,867,3130),("North Carolina",712,486,1069,168),
("Massachusetts",709,478,997,156),("New York",703,472,1168,167),("Colorado",703,465,1168,51),
("Washington",688,483,835,439),("Florida",681,492,984,342),("Alabama_x",0,0,0,0),
("Tennessee",671,475,963,104),("Texas",670,509,970,367),("Hawaii",666,504,933,59),
("Mississippi",656,469,991,53),("Virginia",649,563,880,95),("Ohio",620,475,844,150),
("South Carolina",609,481,921,197),("Louisiana",601,473,1025,57),("Arizona",547,464,800,203),
("Pennsylvania",534,380,799,136),("Missouri",533,473,793,54),("Illinois",518,363,766,115),
("Georgia",510,365,807,152),("New Mexico",469,464,824,52),("Oklahoma",465,350,675,93),
("Michigan",369,359,559,121)]
hub=[r for r in hub if r[0]!="Alabama_x"]
assert len(hub)==27, len(hub)
range_chart(hub,"flood-insurance-cost-by-state-range")
print("wrote", len(os.listdir(OUT)), "files")
