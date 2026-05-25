---
scenario: product-promotion
status: stub — ready for designer to fill
---

# Scenario · product-promotion

A product-promotion page sells **one product, launch, or limited offer**. Its job is to land the value proposition fast, supply enough proof to be trusted, and exit on one CTA — repeated tastefully.

## When to use

- A single-product marketing landing page (new product, feature release, app download).
- A launch detail page for an event, course, or limited-edition drop.
- A limited-time offer page (sale, early-bird, bundle).
- A pre-order page when the offer is concrete (price visible, shipping date set).

## When NOT to use

- Pre-launch sign-up with no concrete offer → use `waitlist`.
- Multi-product browse / catalog → use `product-catalog`.
- Periodic data retelling → use `campaign-report`.

## Status

**Stub — ready for designer to fill.** Scaffold files:

- [`PATTERN.md`](PATTERN.md) — 8-chapter cadence sketch with `<!-- TODO -->` markers for archetype detail.
- [`components.md`](components.md) — 5 required components named, props/DOM/variants to fill.
- [`template.md`](template.md) — points at the agnostic [`templates/prompt-template.md`](../../templates/prompt-template.md); no fork needed yet.

## How to fill

Read [`reference/03-scenario-define.md`](../../reference/03-scenario-define.md) for the scenario-definition workflow. Use [`../campaign-report/`](../campaign-report/) as the prose-tone reference — same level of structural detail, same scale of language.

Recommended reference material when filling the archetypes: Linear's product pages (typographic restraint, generous spacing), Vercel's product pages (asymmetric splits, motion accents), Stripe's product pages (proof density, structural clarity), Apple's product pages (Hero artifact treatment, full-bleed compositions). Inspect actual rendered HTML — do not copy decorative chrome wholesale.
