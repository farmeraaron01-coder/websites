import json, urllib.request, base64, os, sys

UA = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36'
# Credentials come from the environment. Never commit an application password.
AUTH = base64.b64encode(os.environ['CFI_STAGING_AUTH'].encode()).decode()
BASE = 'https://new.californiafloodinsurance.com/wp-json/wp/v2/'
VIDEOS_CAT = 5


def api(path, method='GET', payload=None):
    data = json.dumps(payload).encode() if payload is not None else None
    r = urllib.request.Request(BASE + path, data=data, method=method, headers={
        'User-Agent': UA, 'Authorization': 'Basic ' + AUTH,
        'Content-Type': 'application/json'})
    return json.loads(urllib.request.urlopen(r, timeout=60).read().decode())


POSTS = [
{
 'slug': 'private-flood-insurance-vs-fema',
 'title': 'Private Flood Insurance vs FEMA: What Actually Differs',
 'vid': 'vdslGDfJgIQ',
 'vtitle': 'Private Flood Insurance vs FEMA',
 'vdesc': 'Aaron Farmer explains the practical differences between a private flood policy and an NFIP policy for California homeowners: limits, waiting periods, loss of use, and when the federal program is still the better fit.',
 'rm_title': 'Private Flood Insurance vs FEMA (NFIP) — Video Explainer',
 'rm_desc': 'Video: the real differences between private flood insurance and the NFIP for California homes — limits, waiting periods, loss of use, and when FEMA wins.',
 'standfirst': 'The differences that actually change your outcome are limits, waiting period and loss of use — not the logo on the policy.',
 'excerpt': 'A short explainer on how private flood insurance and the NFIP differ in practice for California homeowners, and the cases where the federal program is still the better choice.',
 'body': '''<p>Most homeowners meet the private flood market for the first time when someone tells them their NFIP renewal went up. The comparison then gets framed as cheaper versus more expensive, which misses most of what matters. The differences that change your outcome are structural.</p>

<h2>The four differences that matter</h2>

<p><strong>Building limits.</strong> The NFIP caps residential building coverage at $250,000 and contents at $100,000. That was a reasonable ceiling when it was set and is not one now — in much of California the cost to rebuild exceeds it outright. Private carriers write well above those caps, which for a lot of homes is the whole argument. If you are already at the NFIP maximum and still underinsured, <a href="/excess-flood-insurance/">excess flood insurance</a> is the other route to the same place.</p>

<p><strong>Waiting period.</strong> A new NFIP policy takes 30 days to take effect, counted from the day you buy it rather than the day the storm arrives. Private carriers are considerably faster — as little as 7 days with some, commonly 10. That gap decides whether a decision made in October is any use in November.</p>

<p><strong>Loss of use.</strong> The NFIP does not pay for you to live somewhere else while your home is repaired. Many private policies do. After a serious flood that is months of rent, and it is the coverage people are most surprised to find they never had. Our guide to <a href="/loss-of-use-coverage-in-flood-insurance/">loss of use in flood insurance</a> goes through how it is triggered.</p>

<p><strong>How the price is built.</strong> NFIP pricing under Risk Rating 2.0 follows your property's own characteristics. Private carriers price on their own models and their own appetite, which is why two quotes on the same house can differ enough to be worth the ten minutes it takes to get both.</p>

<h2>When the NFIP is still the right answer</h2>

<p>Often enough that we would rather say it plainly. If your home has a pre-FIRM subsidised rate, if it has a claims history a private carrier will decline, or if it sits in a community where private appetite is thin, the federal program is your policy and there is no cleverness available. The NFIP also cannot non-renew you the way a private carrier can walk away from a book of business.</p>

<p>We quote both, and part of the job is telling you when the answer is FEMA. If you want the market-structure version of this, <a href="/comparing-the-admitted-vs-non-admitted-insurance-markets/">admitted versus non-admitted markets</a> covers who is actually behind a private flood policy.</p>

<h2>Get both quoted</h2>

<p><a href="/get-a-quote/">Request a quote</a> and we will run the NFIP alongside the private markets available for your address, or call <a href="tel:8552253566">855-CAL-FLOOD (225-3566)</a>. More videos on the <a href="/video/">video hub</a>.</p>''',
},
{
 'slug': 'flood-insurance-carrier-ratings',
 'title': 'Flood Insurance Carrier Ratings: How to Read Them',
 'vid': 'eigEkEsPljA',
 'vtitle': 'Flood Insurance Carrier Rating',
 'vdesc': 'What a carrier financial strength rating actually measures, why Lloyd’s of London syndicates look unfamiliar on a quote, and what to check before you accept a private flood policy.',
 'rm_title': 'Flood Insurance Carrier Ratings Explained — Video',
 'rm_desc': 'Video: what a flood carrier’s financial strength rating measures, how to read a Lloyd’s syndicate, and what to check before accepting a private policy.',
 'standfirst': 'A rating measures one thing: whether the carrier can pay a very bad year. Here is how to read one, and what it does not tell you.',
 'excerpt': 'What carrier financial strength ratings actually measure, why Lloyd’s syndicates look unfamiliar on a quote, and what to check before accepting a private flood policy.',
 'body': '''<p>When a private flood quote comes back with a carrier name nobody recognises, the reasonable reaction is suspicion. The right response is not to dismiss it — it is to read the rating.</p>

<h2>What a rating actually measures</h2>

<p>A financial strength rating from AM Best, S&amp;P or Demotech is an opinion on one question: can this carrier pay claims through a very bad year? It is not a customer service score, it is not a claims-handling score, and it says nothing about whether the policy in front of you is well written. It is solvency, and for flood — a peril that arrives all at once across a whole region — solvency is the thing that matters most.</p>

<p>A-rated or better is the usual bar for a flood carrier, and it is the bar we hold to. Below that the question stops being about price.</p>

<h2>Why Lloyd&rsquo;s looks strange on a quote</h2>

<p>A good share of the private flood market sits with Lloyd&rsquo;s of London syndicates, and a Lloyd&rsquo;s quote does not look like a quote from a household-name insurer. You may see a syndicate number rather than a brand you know.</p>

<p>That unfamiliarity is not a warning sign. Lloyd&rsquo;s carries a market-wide rating and a central fund standing behind the syndicates, which is a different and in some ways stronger structure than a single company balance sheet. It is also why Lloyd&rsquo;s writes risks the domestic admitted market will not touch — which is frequently why your home has a private option at all.</p>

<h2>Admitted, non-admitted, and the guarantee fund</h2>

<p>The distinction people should actually ask about is not the rating but the licence. An admitted carrier is backed by the California Insurance Guarantee Association if it becomes insolvent. A non-admitted, or surplus lines, carrier is not — and a great deal of private flood is written non-admitted, because that is what allows a carrier to price a risk the admitted market has declined.</p>

<p>This is a real trade rather than a hidden catch: you get access and higher limits, and you give up the guarantee fund backstop. It is the reason the rating matters more on a surplus lines policy than on an admitted one. <a href="/comparing-the-admitted-vs-non-admitted-insurance-markets/">Admitted versus non-admitted markets</a> covers the mechanics.</p>

<h2>What to ask before you accept a policy</h2>

<ul>
<li>Who is the carrier, and what is its current financial strength rating?</li>
<li>Is it admitted or surplus lines in California?</li>
<li>Who handles the claim — the carrier, or a third-party administrator?</li>
<li>What are the limits, and what is excluded? See <a href="/what-does-flood-insurance-not-cover/">what flood insurance does not cover</a>.</li>
</ul>

<p>Any broker should answer all four without hesitating. <a href="/get-a-quote/">Request a quote</a> or call <a href="tel:8552253566">855-CAL-FLOOD (225-3566)</a>, and see more on the <a href="/video/">video hub</a>.</p>''',
},
{
 'slug': 'flood-insurance-mortgage-clause',
 'title': 'What Is the Mortgage Clause on a Flood Policy?',
 'vid': '6dMwWQh0ENU',
 'vtitle': 'What is the Mortgage Clause',
 'vdesc': 'The mortgage clause names your lender on the flood policy. What it does, why a wrong loan number stalls a closing, and what to fix when the lender says your coverage is unacceptable.',
 'rm_title': 'The Mortgage Clause on a Flood Insurance Policy — Video',
 'rm_desc': 'Video: what the mortgage clause on a flood policy does, why a wrong loan number stalls closings, and how to fix a lender rejection fast.',
 'standfirst': 'The mortgage clause is the line that names your lender. Get it wrong and the closing stops, however good the policy is.',
 'excerpt': 'What the mortgage clause on a flood policy does, why an incorrect loan number stalls a closing, and how to fix a lender rejection quickly.',
 'body': '''<p>The mortgage clause is the least interesting part of a flood policy and the most common reason a closing stalls. It is the line that names your lender as the party with a financial interest in the property, so that if the home floods the insurer knows the loan holder has to be involved in the claim.</p>

<h2>Why lenders are so particular about it</h2>

<p>A flood policy protects the collateral behind the loan. The lender needs it on file, needs it correct, and needs it to keep existing — which is why the clause carries a notification requirement: the insurer tells the lender before the policy lapses or cancels rather than after.</p>

<p>Three details have to be exactly right, and all three are routinely wrong:</p>

<ul>
<li><strong>The lender&rsquo;s legal name and its successors-and-assigns wording.</strong> Loans get sold. The clause has to survive the sale.</li>
<li><strong>The mailing address for notices</strong> — usually a central servicing address, not the branch you dealt with.</li>
<li><strong>The loan number.</strong> The single most common error, and the one that most often stops a closing.</li>
</ul>

<p>None of these change your coverage. All of them will hold up a funding date, which is why we confirm them against the lender&rsquo;s own instructions rather than what the borrower remembers.</p>

<h2>When the lender rejects the policy</h2>

<p>Sometimes the clause is fine and the lender still says the policy is unacceptable. Usually one of three things:</p>

<p><strong>The amount is too low.</strong> Lenders generally require coverage equal to the lesser of the loan balance, the replacement cost, or the NFIP maximum. <a href="/how-much-flood-insurance-is-required-by-lender/">How much flood insurance a lender requires</a> works through the arithmetic.</p>

<p><strong>The policy is non-admitted and the lender will not accept surplus lines.</strong> Some will not. Federal guidance permits private flood policies that meet the definition of an acceptable private policy, but individual servicers apply their own overlays, and the fix is either a carrier change or a conversation with the servicer.</p>

<p><strong>The effective date does not reach the closing.</strong> This is the waiting period showing up at the worst moment. A new NFIP policy takes 30 days; private carriers can be as fast as 7. On a purchase closing the NFIP waiting period is waived, which is exactly the kind of exception worth knowing before you panic.</p>

<h2>If you are refinancing or buying</h2>

<p>Send us the lender&rsquo;s insurance requirements page and we will issue the policy with the clause already correct. <a href="/get-a-quote/">Request a quote</a> or call <a href="tel:8552253566">855-CAL-FLOOD (225-3566)</a>. If you are still working out whether coverage is required at all, see <a href="/when-is-flood-insurance-required/">when flood insurance is required</a>, and find more explainers on the <a href="/video/">video hub</a>.</p>''',
},
{
 'slug': 'setting-flood-insurance-coverage-limits',
 'title': 'Setting Your Flood Coverage Limits: How Much Is Enough?',
 'vid': 'vAe5wcwwuGY',
 'vtitle': 'How Much Flood Coverage Do I Need',
 'vdesc': 'Why the lender’s minimum is not the right number, how building and contents limits are set, and the two coverages homeowners most often leave off a flood policy.',
 'rm_title': 'How Much Flood Coverage Do I Need? Setting Limits — Video',
 'rm_desc': 'Video: why a lender’s minimum is not the right flood limit, how building and contents coverage are set, and the two coverages people leave off.',
 'standfirst': 'The lender’s minimum protects the loan. Setting the limit to protect the house is a different calculation.',
 'excerpt': 'Why the lender’s minimum is the wrong number to insure to, how building and contents limits get set, and the two coverages most often left off a flood policy.',
 'body': '''<p>Almost every underinsured flood policy we see was set to the lender&rsquo;s minimum. That is not a mistake anyone made carelessly — it is what happens when the only number in the conversation comes from the loan file.</p>

<h2>The lender&rsquo;s number protects the lender</h2>

<p>A servicer typically requires the lesser of the loan balance, the replacement cost, or the NFIP maximum. Notice what that optimises for: the loan being repaid. It has nothing to say about you having a house at the end of the process.</p>

<p>The number that protects you is the cost to rebuild — materials and labour at today&rsquo;s prices, not what you paid and not the market value, which includes land that will not wash away. Rebuild costs have moved a long way since 2021, and a limit set then is very likely low now.</p>

<h2>Building and contents are separate decisions</h2>

<p>Most people buy what the lender demanded, which is building coverage only. Contents is a separate limit and is usually a modest addition to the premium — and it is the part that pays for everything you actually live with. Furniture, appliances, clothing, electronics. Ask for it as a line item rather than assuming it is in there.</p>

<p>Two more that get left off:</p>

<ul>
<li><strong>Loss of use.</strong> The NFIP does not offer it; many private policies do. It is what pays your rent while the house is repaired, and after a serious flood that is months. See <a href="/loss-of-use-coverage-in-flood-insurance/">loss of use coverage</a>.</li>
<li><strong>Basement and below-grade limits.</strong> Coverage below the lowest floor is restricted in ways that surprise people. <a href="/flood-coverage-gaps/">Flood coverage gaps</a> covers where the holes usually are.</li>
</ul>

<h2>Deductibles do real work here</h2>

<p>The deductible is the lever most people forget they have. Raising it can fund a materially higher limit for the same premium, which is usually the better trade: a flood claim large enough to matter will blow through any deductible you would realistically choose, while an inadequate limit caps your recovery permanently.</p>

<p>What it costs to get this right is generally less than expected — a low-risk-zone California home commonly runs about $450 a year in our book. <a href="/how-much-does-flood-insurance-cost/">What flood insurance costs in California</a> goes through the drivers, and <a href="/how-much-flood-insurance-do-i-need/">how much flood insurance you need</a> is the longer written version of this video.</p>

<h2>Have the limits checked</h2>

<p>Send us your current declarations page and we will tell you what it would actually cost to rebuild and whether the limit reaches. <a href="/get-a-quote/">Request a quote</a> or call <a href="tel:8552253566">855-CAL-FLOOD (225-3566)</a>. More on the <a href="/video/">video hub</a>.</p>''',
},
]


def shortcode(p):
    return ('[cfi_video id="%s" title="%s" desc="%s"]' % (p['vid'], p['vtitle'], p['vdesc'].replace('"', '&quot;')))


created = []
for p in POSTS:
    existing = api('posts?slug=%s&status=any,publish,draft&_fields=id,slug' % p['slug'])
    content = shortcode(p) + "\n\n" + p['body']
    payload = {
        'slug': p['slug'],
        'title': p['title'],
        'content': content,
        'excerpt': p['excerpt'],
        'status': 'publish',
        'categories': [VIDEOS_CAT],
        'author': 1,
        'meta': {
            'rank_math_title': p['rm_title'],
            'rank_math_description': p['rm_desc'],
            '_cfi_standfirst': p['standfirst'],
        },
    }
    if existing:
        pid = existing[0]['id']
        r = api('posts/%d' % pid, 'POST', payload)
        action = 'updated'
    else:
        r = api('posts', 'POST', payload)
        action = 'created'
    created.append((action, r['id'], r['link'], len(p['rm_desc'])))
    print('%-8s id=%-5s %s  (meta desc %d chars)' % (action, r['id'], r['link'], len(p['rm_desc'])))

print()
print('videos category count now:',
      [c['count'] for c in api('categories?slug=videos&_fields=count')])
