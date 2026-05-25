---
type: component-spec
scenario: waitlist
status: stub — ready for designer to fill
---

# Component Spec · waitlist

> Stub. Designer fills component details per [`reference/03-scenario-define.md`](../../reference/03-scenario-define.md). Reference [`../campaign-report/components.md`](../campaign-report/components.md) for prose tone (Purpose / Props / DOM / Variants / Adaptive states / Banned).

**Three-library limit**: every component composes from **shadcn/ui**, **motion**, and **paper-shaders** (Promise Hero background only). No form-library beyond shadcn's `Input` / `Button` primitives.

---

## Required Components

### PromiseHero

**Purpose**: Promise Hero archetype. Combines the product promise (one sentence, ≤ 18 words) with the embedded sign-up form. The whole component must fit above the fold at desktop and at mobile.

<!-- TODO 设计师: 写 props (promise / proofLine? / heroVisual? / formProps: { emailPlaceholder / submitLabel / privacyNote / onSubmit }) + DOM (section[data-archetype="promise-hero"] > div.hero-inner > h1.promise + p.proof-line + WaitlistForm + HeroShader) + 变体 (Full-bleed Monolith default / Asymmetric Split with visual in narrow column / Typographic Field for type-only promise) + adaptive states (loading: disable form, show submitting spinner inside button; submitted: replace form with confirmation block in same footprint; error: inline error below input, no toast)。 -->

---

### WaitlistForm

**Purpose**: The sign-up form. **One** email input, **one** submit button, **one** privacy note. That's the whole component — additional fields belong in a post-signup email confirmation flow, not in this form.

<!-- TODO 设计师: 写 props (emailPlaceholder / submitLabel / privacyNote / loading / error / onSubmit(email)) + DOM (form > div.field > input[type="email"] + Button + p.privacy-note) + 变体 (inline-row default / stacked-mobile / outlined-input vs filled-input per pack) + adaptive states (loading: disable input + spinner in button; success: replace form with ConfirmationBlock; error: inline message below input + keep form interactive)。 -->

---

### WhyBlock

**Purpose**: The Why section. 2–3 lines of supporting claim — what makes the promise believable. Typographic, not card-based.

<!-- TODO 设计师: 写 props (claims: Array<string>, 2-3 entries) + DOM (section[data-archetype="why"] > ol.claims > li.claim (each one line, Section Secondary scale)) + 变体 (Typographic Field default / Stacked Band with index numbers) + adaptive states (no claims: omit entire section, do not render empty Why)。Note: 不要 icon,不要 card,3 行排版即可承载。 -->

---

### ProofBlock

**Purpose**: Optional Proof / Social archetype. Founder names, prior work, press marks, named pre-users.

<!-- TODO 设计师: 写 props (proofs: Array<{ kind: 'founder' | 'press' | 'investor' | 'named-user'; label / artifact? }>) + DOM + 变体 (Typographic Field for founder line / Matrix Grid for logo wall / Stacked Band for testimonials) + adaptive states (no proof: omit section entirely — fabricated proof reads worse than no proof)。 -->

---

### CountdownBlock

**Purpose**: Optional Countdown / Capacity archetype. Renders **one** real-time signal: launch date OR remaining slots OR signups-so-far. Never more than one — multiple counters look manipulative.

<!-- TODO 设计师: 写 props (mode: 'date' | 'slots' | 'count' / value / label) + DOM + 变体 (count-up / count-down / static-number-of-the-day) + adaptive states (no data: omit entirely; date passed: replace with "Launching soon" — never let a zeroed countdown stay visible)。 -->

---

### FaqCompact

**Purpose**: Optional FAQ Compact archetype. 3–5 short answers to objections.

<!-- TODO 设计师: 写 props (items: Array<{ question / answer }>, length 3-5) + DOM (Stacked Band of question-answer pairs, NO accordion by default — read time < accordion-click time at this length) + 变体 (always-open default / shadcn Accordion when items > 5) + adaptive states (no items: omit section)。 -->

---

### FooterCta

**Purpose**: Restates the WaitlistForm for visitors who scrolled past the Hero. Same component contract as WaitlistForm, rendered in a Full-bleed Monolith treatment at the page end.

<!-- TODO 设计师: 写 props (复用 WaitlistForm props + heading + subline?) + DOM + 变体 + adaptive states。Note: 不要把 WaitlistForm 渲染第三次 —— Hero + Footer 已经 sufficient。 -->

---

## Banned Components

- Multiple email-input fields requesting name / company / role / phone alongside email — every extra field halves conversion.
- Fake "1,247 people joined today" tickers — manipulative and visitors detect it.
- Default-checked newsletter / marketing-consent checkboxes.
- Multi-step waitlist forms (page 1 of 3) — this is sign-up, not onboarding.
- Modal-trapped forms — if the form requires a click to even appear, that click is a leak.
- Exit-intent popups — desperation reads as desperation.
- Countdown timers that pass zero and keep ticking negative — pick one moment of truth and respect it.
- Confetti / particle effects on successful sign-up — the success message is the success message.

<!-- TODO 设计师: 加更多场景特定 ban,参照 campaign-report/components.md banned list 体例。 -->
