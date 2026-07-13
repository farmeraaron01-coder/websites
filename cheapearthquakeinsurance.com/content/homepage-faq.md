# Homepage FAQ Section — CheapEarthquakeInsurance.com

**Where it goes:** on the homepage, below the "Why use CheapEarthquakeInsurance.com?" section and above "Latest News."
**Heading level:** the section title is an H2; each question is an H3.
**Schema:** paste the JSON-LD block at the bottom into a Code/Custom HTML module at the end of the homepage.

---

## Earthquake Insurance Questions, Answered

### How much does earthquake insurance cost in California?

For most California homeowners, earthquake insurance runs between $800 and $3,000+ per year. The biggest price drivers are your distance from active faults, soil type, the age and construction of your home, your dwelling coverage amount, and — most of all — the deductible you choose. Because we quote both the California Earthquake Authority (CEA) and multiple private carriers, we can usually find a meaningfully lower price for the same coverage than any single-company quote.

### Is earthquake insurance worth it if I have a big deductible?

Often, yes — because the deductible is a percentage, not a wall. If your home is insured for $600,000 with a 10% deductible and an earthquake causes $250,000 in damage, you pay $60,000 and insurance covers the remaining $190,000. Without a policy, all $250,000 is yours. Earthquake insurance is catastrophic-loss protection: it exists so a bad earthquake doesn't take your home equity with it.

### Can I get a deductible lower than the CEA offers?

Frequently. CEA deductibles typically run 5–25% of dwelling coverage. Several private earthquake carriers we represent offer deductibles as low as 2.5–5%, higher dwelling limits, and broader personal property coverage. That comparison — CEA vs. private, side by side — is exactly what we do.

### Does commercial property insurance cover earthquakes?

No. Standard commercial property policies exclude earthquake damage, just as homeowners policies do. Commercial earthquake coverage is a separate policy or endorsement — and for many California commercial buildings, lenders require it as a condition of the loan. We quote commercial earthquake for buildings, business personal property, and earthquake-related business interruption.

### Is there a waiting period or can coverage be denied after an earthquake?

Insurers routinely impose a temporary moratorium on new earthquake policies immediately after a significant quake (often around 15–30 days, varying by carrier). Translation: you cannot buy this coverage while the ground is still moving. The time to secure a policy is before the event — quotes are free and take minutes.

### Do renters and condo owners need earthquake insurance?

Yes, and it's usually inexpensive. Renters' earthquake coverage protects belongings and loss of use. For condo owners it's more urgent: your HOA's master policy often carries no earthquake coverage at all, and unit owners can be hit with enormous **loss assessments** to rebuild the structure. Condo earthquake policies with loss assessment coverage are one of the most under-purchased, highest-value policies we write.

---

## FAQPage schema — paste into a Code/Custom HTML module at the bottom of the homepage

```html
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "FAQPage",
  "mainEntity": [
    {
      "@type": "Question",
      "name": "How much does earthquake insurance cost in California?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "Most California homeowners pay between $800 and $3,000+ per year. Price depends on distance from active faults, soil type, home age and construction, dwelling coverage amount, and the deductible selected. Comparing CEA and private carriers side by side usually finds a lower price for equivalent coverage."
      }
    },
    {
      "@type": "Question",
      "name": "Is earthquake insurance worth it with a large percentage deductible?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "Often yes. The deductible is subtracted from the claim, not a barrier to it: on a $600,000 dwelling with a 10% deductible and $250,000 of damage, the homeowner pays $60,000 and insurance pays $190,000. Without coverage the entire loss is out of pocket."
      }
    },
    {
      "@type": "Question",
      "name": "Can I get an earthquake deductible lower than the CEA offers?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "Frequently. CEA deductibles typically run 5–25% of dwelling coverage, while several private California earthquake carriers offer deductibles as low as 2.5–5%, along with higher limits and broader personal property coverage."
      }
    },
    {
      "@type": "Question",
      "name": "Does commercial property insurance cover earthquakes?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "No. Standard commercial property policies exclude earthquake damage. Commercial earthquake coverage is a separate policy or endorsement, and many California commercial lenders require it as a loan condition."
      }
    },
    {
      "@type": "Question",
      "name": "Can I buy earthquake insurance right after an earthquake?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "Usually not immediately. Insurers commonly impose a temporary moratorium on new earthquake policies after a significant quake, often around 15–30 days depending on the carrier. Coverage needs to be in place before an event."
      }
    },
    {
      "@type": "Question",
      "name": "Do renters and condo owners need earthquake insurance?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "Yes. Renters' earthquake coverage protects belongings and loss of use inexpensively. Condo owners face a bigger exposure: HOA master policies often carry no earthquake coverage, leaving unit owners open to large loss assessments — condo earthquake policies with loss assessment coverage address this."
      }
    }
  ]
}
</script>
```
