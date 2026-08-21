# cheapsoberlivinginsurance.com — agency identity, and the schema defects it exposes

Supplied by Aaron 21 Aug 2026. This closes Part 0 decision 6.

---

## The canonical facts

| Field | Value |
|---|---|
| Business name | Cheap Sober Living Insurance |
| Alternate name | CheapSoberLivingInsurance.com |
| Licence | **CA License #0L75450** |
| Street address | **7960 Silverton Ave. #202** |
| City / state / ZIP | San Diego, CA 92126, US |
| Phone | **858-295-7242** (`+1-858-295-7242`) |
| Canonical URL | `https://cheapsoberlivinginsurance.com/` (apex) |
| Hours | Mon–Fri 09:00–17:00 |

### Two suites at one building — this is correct, do not "fix" it

| Suite | Brands |
|---|---|
| **#203** | californiafloodinsurance.com, statewidefloodinsurance.com |
| **#202** | Cheap Sober Living Insurance, Jump Insurance Services, trucking |

The flood sites publishing `#203` while this one publishes `#202` is **not** a
NAP inconsistency to correct. Both suites are real and the split is by brand.

Likewise the phone: the flood brands share `855-225-3566`; sober living has its
own line, `858-295-7242`. **Do not copy the flood number onto this site.**

---

## Defects found on the live site while confirming these

The ChatGPT audit says the site has "zero schema markup — no InsuranceAgency, no
LocalBusiness, nothing." **That is out of date.** Someone has since added a Divi
Code module with JSON-LD. The homepage now emits three blocks, and they conflict.

### 1. Two organization entities, disagreeing on the phone number

| Node | Source | `@id` | telephone |
|---|---|---|---|
| `Organization` | AIOSEO | `…/#organization` | `+18582957242` |
| `InsuranceAgency` + `LocalBusiness` | hand-added Divi Code module | **none** | `+18552253566` |

Two business entities for one site, giving Google two different phone numbers —
one of which (the 855) belongs to the flood brands and is wrong here. This is
the same class of bug as the duplicate `Person` `@id` we fixed on the flood
sites in August.

### 2. The AIOSEO organization name is truncated garbage

```
"name": "Cheap Sober Living Insurance for your"
```

That is the node carrying the site's `#organization` identifier, so it is the
name Google is most likely to read as canonical. It looks like a tagline field
was pulled in and cut off.

**This one is worth fixing today**, independently of the rebuild — it is a
two-minute edit in AIOSEO's Search Appearance settings and it is actively wrong
in the live index.

### 3. The hand-added node has no `@id`

So it cannot be referenced by the `WebPage` node or reconciled with AIOSEO's
organization. It floats.

### 4. The address in schema has no `streetAddress`

Only locality, region and country. The visible footer carries `#202` and a
Google Maps embed for `STE 202`; the structured data omits it entirely.

### 5. The licence number appears in no structured data at all

Neither here nor on the flood sites. Visible-text only.

### 6. Malformed markup: `</script></script>`

The Divi Code module emits a duplicated closing tag. Browsers tolerate it;
it is still broken HTML sitting in the homepage.

---

## How to fix it: one node, configured in Rank Math, not hand-coded

All six defects collapse into a single decision — **stop having two sources of
organization data.**

Once Rank Math is in (Step 1), configure the entity in
**Rank Math → Titles & Meta → Local SEO** rather than pasting JSON-LD into a
Code module:

| Rank Math field | Value |
|---|---|
| Person or Company | **Company** |
| Business type | `InsuranceAgency` (fall back to `LocalBusiness` if the Free build does not offer it) |
| Name | Cheap Sober Living Insurance |
| Street address | 7960 Silverton Ave. #202 |
| Locality / Region / Postcode / Country | San Diego / CA / 92126 / US |
| Phone | +1-858-295-7242 |
| Opening hours | Mon–Fri 09:00–17:00 |

Then **delete the Divi Code module holding the hand-written JSON-LD.** It becomes
redundant the moment Rank Math emits the node, and leaving it in recreates the
two-entity conflict under a new plugin.

Rank Math attaches its node at `…/#organization`, which is the identifier the
`WebPage` node already points to — so the entity graph resolves itself.

### What Rank Math will not do for you

Rank Math has no field for a producer licence number, and schema.org has no
purpose-built property for one. If you want it in structured data, add it as an
`identifier` on the organization node:

```json
"identifier": {
  "@type": "PropertyValue",
  "name": "California Department of Insurance License",
  "value": "0L75450"
}
```

This is worth doing on all three sites, not just this one. It is a genuine
E-E-A-T signal for a regulated profession and none of the three currently
carries it in machine-readable form.

**Regardless of schema, keep `CA License #0L75450` in the visible footer.** That
is what the compliance requirement actually attaches to, and structured data
does not satisfy it.

---

## Corrections needed in the content package

The package was written against assumptions that the live site contradicts:

| Package says | Correct value |
|---|---|
| canonical + schema on `https://www.cheapsoberlivinginsurance.com/` | apex, no `www` |
| `llms.txt`: `Phone: 855-225-3566` | `858-295-7242` |
| `home-page.tsx` org node: no address, no licence | add `#202` address and the licence identifier |

Fix these in the package **before** the build, not after — the phone in
particular will otherwise be pasted onto every page.
