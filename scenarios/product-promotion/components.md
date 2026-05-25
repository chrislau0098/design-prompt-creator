---
type: component-spec
scenario: product-promotion
status: stub — ready for designer to fill
---

# Component Spec · product-promotion

> Stub. Designer fills component details per [`reference/03-scenario-define.md`](../../reference/03-scenario-define.md). Reference [`../campaign-report/components.md`](../campaign-report/components.md) for prose tone (Purpose / Props / DOM / Variants / Adaptive states / Banned).

**Three-library limit**: every component composes from **shadcn/ui**, **motion**, and **paper-shaders** (Hero or accent background only). Charts use **recharts** only when a Proof Moment needs a chart — not the default.

---

## Required Components

### ProductHero

**Purpose**: Opening anchor. Carries product name, value proposition, hero artifact, primary CTA.

<!-- TODO 设计师: 写 props (productName / proposition / heroArtifact / primaryCta / ...) + DOM (section[data-archetype="product-hero"] > div.hero-inner > h1 + p + Button + HeroArtifact + HeroShader) + 变体 (Full-bleed Monolith / Asymmetric Split with artifact in wide column / Offset Frame with cropped artifact) + adaptive states (loading: skeleton on artifact; empty proposition: refuse to render Hero — Hero needs a proposition)。 -->

---

### ValuePillar

**Purpose**: One claim cell inside the Value Pillars Matrix Grid (typically 3–4 per page).

<!-- TODO 设计师: 写 props (icon? / claim / supportingLine?) + DOM + 变体 (icon-led / claim-led / numbered) + adaptive states。注意:icon 不是必需,纯排版 pillar 更高级 (参考 Linear)。 -->

---

### FeatureBlock

**Purpose**: Feature Detail archetype. One feature shown with a focal artifact (screenshot / motion loop / illustration) plus copy.

<!-- TODO 设计师: 写 props (featureName / artifact / copy / secondaryCta?) + DOM + 变体 (Asymmetric Split default / Stacked Band for motion-loop demos / Full-bleed Monolith for hero feature) + adaptive states。 -->

---

### ProofBlock

**Purpose**: Social Proof archetype. Testimonials, logo wall, named-user marks, press quotes.

<!-- TODO 设计师: 写 props (proofs: Array<{ kind: 'testimonial' | 'logo' | 'press'; ... }>) + DOM + 变体 (Matrix Grid for logo wall / Stacked Band for testimonials / Typographic Field for single-quote hero proof) + adaptive states。 -->

---

### CtaBlock

**Purpose**: Final CTA archetype. Restates the offer + one button. Also rendered inline in the Hero (same component, smaller scale variant).

<!-- TODO 设计师: 写 props (heading / subline? / primaryCta / secondaryCta?) + DOM + 变体 (Hero-inline / Full-bleed final) + adaptive states。Note: never render two CtaBlock with different primary CTA labels — repeat the same CTA verbatim. -->

---

## Optional Components

### PricingTable, CountdownBlock, FaqAccordion

<!-- TODO 设计师: 按需添加 — 见 [`../campaign-report/components.md`](../campaign-report/components.md) 优秀模板。 -->

---

## Banned Components

- Hero carousels — buyer cannot read while pictures change.
- Multiple primary CTA styles on one page — primary is singular, secondary is the only allowed variant.
- Animated price flashing or fake "countdown until midnight" timers without a real deadline.
- FAQ accordion auto-opened on load — defeats the affordance.
- Testimonial avatars at Display Number scale — proof is the words, not the face.

<!-- TODO 设计师: 加场景特定 ban,参照 campaign-report/components.md banned list 体例。 -->
