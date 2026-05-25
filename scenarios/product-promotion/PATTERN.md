---
type: pattern-block
scenario: product-promotion
status: stub — ready for designer to fill
based_on: scenarios/campaign-report/PATTERN.md (reference)
---

# PATTERN · product-promotion

> Stub. Designer fills archetype details per [`reference/03-scenario-define.md`](../../reference/03-scenario-define.md). Reference the mature [`../campaign-report/PATTERN.md`](../campaign-report/PATTERN.md) for prose tone, density-rule wording, and slot-mapping table format. The 9 composition treatments and 6 dominant moves are scenario-agnostic — reuse from the campaign-report PATTERN.md §11.1 and §11.2 verbatim.

A product-promotion page sells **one product, launch, or limited offer**. Its job is to land the value proposition fast, supply enough proof to be trusted, and exit on one CTA — repeated tastefully.

---

## Chapter cadence (5–8 sections)

| # | Chapter | One-line purpose | Required |
|---|---|---|---|
| 1 | **Hero** | Anchors product name, value proposition, hero visual, primary CTA. | required |
| 2 | **Value Pillars** | 3–4 supporting claims that unpack the proposition. | required |
| 3 | **Feature Detail** | One or two features shown with a focal artifact (screenshot, demo, key spec). | required |
| 4 | **Social Proof** | Testimonials, logos, named users, press marks. | required when available |
| 5 | **Proof Moment** | Numbers, badges, or guarantees that earn trust (1 per launch is enough). | optional |
| 6 | **Pricing / Offer** | One pricing presentation, OR one limited-offer countdown — pick one. | required if commerce |
| 7 | **FAQ** | 3–6 questions, answered short. | optional |
| 8 | **Final CTA** | Restate the offer + one button. | required |

<!-- TODO 设计师: 参照 campaign-report/PATTERN.md §11.3 风格,为每个 chapter 写 archetype 段(Trigger / Slots / Treatments / Dominant Move)。Hero/Value Pillars/Feature Detail/Social Proof/Pricing/FAQ/Final CTA 各一段。可借鉴 Linear、Vercel、Stripe、Apple 产品页 archetype 词汇 —— 避免 "Floating Pricing Card" 这类装饰性命名,用结构性命名(Pricing Table / Pricing Spotlight)。 -->

---

## Composition treatments

Reuse the 9 treatments from campaign-report PATTERN §11.1 verbatim (Full-bleed Monolith, Asymmetric Split, Stacked Band, Matrix Grid, Proportion Rail, Offset Frame, Sequence Track, Typographic Field, Annotation Rail).

Favored treatments for product-promotion: **Full-bleed Monolith** for the Hero and Final CTA, **Matrix Grid** for Value Pillars, **Asymmetric Split** for Feature Detail (artifact in wide column, copy in narrow), **Stacked Band** for FAQ. Avoid Proportion Rail (no parts-of-whole story in a single-product page) unless a feature-comparison subsection genuinely calls for it.

---

## Dominant moves

Reuse the 6 dominant moves from campaign-report PATTERN §11.2 verbatim. Disruptive-move budget: **product-promotion tolerates a higher disruptive budget than campaign-report** — one in three sections may lead with a crop / bleed / column-break, because marketing pages earn attention through assertive composition. Still: never more than one dominant move per section.

---

## Rhythm discipline

Reuse the four rules from campaign-report PATTERN §12.2 verbatim. Two scenario-specific notes:

- **CTA cadence** — the primary CTA appears at minimum twice (Hero + Final). Optional third appearance after Pricing. Never inline in the middle of a Value Pillar — interruption breaks reading flow.
- **Single Hero artifact** — the Hero carries one focal visual (product render, key screen, motion loop). Carousel Heroes are banned: the buyer cannot read while pictures change.

---

## Don'ts (additions to the §16 list)

<!-- TODO 设计师: 加 5-8 条 product-promotion 特定 don't。提示:carousel Hero / 多个 primary CTA 颜色 / pricing 上面叠 "limited time" badge 闪动 / FAQ 装手风琴默认全展开 / testimonial 字越大反而越假 / feature grid 超过 6 个变成 spec sheet。 -->
