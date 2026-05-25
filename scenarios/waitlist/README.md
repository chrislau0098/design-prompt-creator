---
scenario: waitlist
status: stub — ready for designer to fill
---

# Scenario · waitlist

A waitlist page is a **pre-launch landing for sign-ups** — the product does not yet exist publicly, the visitor cannot buy or use it yet, but they can leave an email to be notified. Its job is to communicate the promise, earn enough trust to give an email, and exit on one focused form.

## When to use

- Pre-launch landing for a new product (waitlist, early access, private beta).
- Invite-only beta sign-up.
- Course / event pre-registration when the offer is not yet purchasable.
- Newsletter standalone landing (a serious newsletter that earns its own page).

## When NOT to use

- The product is buyable now → use `product-promotion`.
- Multi-product browse → use `product-catalog`.
- Periodic data retelling → use `campaign-report`.
- A signup form embedded inside a larger marketing page → that form is a `CtaBlock` inside `product-promotion`, not a whole `waitlist` page.

## Status

**Stub — ready for designer to fill.** Scaffold files:

- [`PATTERN.md`](PATTERN.md) — 6-chapter cadence sketch with `<!-- TODO -->` markers for archetype detail.
- [`components.md`](components.md) — 7 required components named (PromiseHero, WaitlistForm, WhyBlock, ProofBlock, CountdownBlock, FaqCompact, FooterCta), props/DOM/variants to fill.
- [`template.md`](template.md) — points at the agnostic [`templates/prompt-template.md`](../../templates/prompt-template.md); no fork needed yet.

## How to fill

Read [`reference/03-scenario-define.md`](../../reference/03-scenario-define.md) for the scenario-definition workflow. Use [`../campaign-report/`](../campaign-report/) as the prose-tone reference.

Recommended reference material when filling the archetypes: Linear's pre-launch pages (typographic restraint, single form, no decoration), Vercel's product reveal pages (Promise Hero with embedded form), Pitch's waitlist (proof line treatment), Read's waitlist (founder credibility as proof), and Robinhood's original waitlist (countdown done honestly). Inspect rendered HTML and pay attention to **what they did not put on the page** — the discipline of a waitlist is in the omissions.

The key call: waitlist design lives or dies on **patient confidence**. If the page reads loud, urgent, or anxious, it converts worse — visitors trust calm.
