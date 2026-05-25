---
scenario: product-catalog
status: stub — ready for designer to fill
---

# Scenario · product-catalog

A product-catalog page is a **multi-product browse experience** — a structured grid of peers that the visitor scans to pick one. Its job is to give the eye purchase on the set, support filter and sort without overpowering them, and let each card lean on a single focal artifact.

## When to use

- E-commerce product listing (a collection, a category, search results).
- Design resource browse (template gallery, icon set, asset library).
- Multi-model catalog (a brand's product family page).
- Curated content library (course catalog, podcast catalog, article archive).

## When NOT to use

- Selling one product → use `product-promotion`.
- Pre-launch sign-up → use `waitlist`.
- Periodic data retelling → use `campaign-report`.
- A live always-on dashboard with filters as the primary surface → catalog is a *page*, not a tool; build a tool with a tool's design.

## Status

**Stub — ready for designer to fill.** Scaffold files:

- [`PATTERN.md`](PATTERN.md) — 7-chapter cadence sketch with `<!-- TODO -->` markers for archetype detail.
- [`components.md`](components.md) — 6 required components named (CatalogHero, FilterRail, ProductCard, CatalogGrid, Pagination, Outro), props/DOM/variants to fill.
- [`template.md`](template.md) — points at the agnostic [`templates/prompt-template.md`](../../templates/prompt-template.md); no fork needed yet.

## How to fill

Read [`reference/03-scenario-define.md`](../../reference/03-scenario-define.md) for the scenario-definition workflow. Use [`../campaign-report/`](../campaign-report/) as the prose-tone reference.

Recommended reference material when filling the archetypes: Apple's product family pages (clean grid, restrained chrome), Aesop's product catalog (typographic restraint, single artifact per card), MUJI's catalog (peer-set equality, no badge clutter), Are.na's channel browse (minimal card chrome, content-first), and shadcn/ui's component browse (typographic field hero, dense grid).

The key call: catalog design lives or dies on **scan rhythm**. Once you fill the cards, render at least 12 of them at desktop width and squint — if any one card jumps out for the wrong reason, the chrome is over-decorated.
