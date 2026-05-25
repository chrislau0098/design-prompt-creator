---
type: pattern-block
scenario: waitlist
status: stub — ready for designer to fill
based_on: scenarios/campaign-report/PATTERN.md (reference)
---

# PATTERN · waitlist

> Stub. Designer fills archetype details per [`reference/03-scenario-define.md`](../../reference/03-scenario-define.md). Reference the mature [`../campaign-report/PATTERN.md`](../campaign-report/PATTERN.md) for prose tone, density-rule wording, and slot-mapping table format. Reuse the 9 composition treatments and 6 dominant moves verbatim.

A waitlist page is a **pre-launch landing for sign-ups** — the product does not yet exist publicly, the visitor cannot buy or use it yet, but they can leave an email to be notified. Its job is to communicate the promise, earn enough trust to give an email, and exit on one focused form. A waitlist page is **minimal by design** — every section that does not serve sign-up is a section that loses sign-ups.

---

## Chapter cadence (5–6 sections, tight)

| # | Chapter | One-line purpose | Required |
|---|---|---|---|
| 1 | **Promise Hero** | The product promise + the sign-up form. Form lives in the Hero, not below the fold. | required |
| 2 | **Why** | 2–3 lines of supporting claim — what makes the promise believable. | required |
| 3 | **Proof / Social** | Founder names, prior work, press marks, named pre-users — any trust signal that exists. | optional |
| 4 | **Countdown / Capacity** | Launch date OR remaining slots OR signups-so-far — one signal, real, never fabricated. | optional |
| 5 | **FAQ Compact** | 3–5 short answers to objections. | optional |
| 6 | **Footer CTA** | Restates the form for visitors who scrolled past Hero. | required |

<!-- TODO 设计师: 为每个 chapter 写 archetype 段(Trigger / Slots / Treatments / Dominant Move),参照 campaign-report/PATTERN.md §11.3 体例。Promise Hero 是新 archetype(combines Hero Monolith with embedded sign-up form,Slots: promise / proof-line? / email-input / submit-button / privacy-note);Why 走 Typographic Field 或 Stacked Band(3 行);Countdown 是新 archetype(real-time, ticking)。 -->

---

## Composition treatments

Reuse the 9 treatments from campaign-report PATTERN §11.1 verbatim.

Favored treatments for waitlist: **Full-bleed Monolith** for the Promise Hero (one focal block carrying form + promise), **Typographic Field** for the Why section (3 lines is a poem, not a paragraph), **Stacked Band** for FAQ Compact, **Asymmetric Split** is rare in waitlist — too much content for a quiet form. Avoid Matrix Grid entirely (no peer set in a single-product waitlist), avoid Proportion Rail (no parts-of-whole story).

---

## Dominant moves

Reuse the 6 dominant moves from campaign-report PATTERN §11.2 verbatim.

Waitlist-specific note: **the dominant move budget is conservative** — waitlist pages succeed on calm, not on visual aggression. Stick to scale jump and single stroke. One disruptive move (offset placement on the Hero artifact, or a column-break on a Why line) is the ceiling for the whole page.

---

## Rhythm discipline

Reuse the four rules from campaign-report PATTERN §12.2 verbatim. Three scenario-specific notes:

- **Form-first** — the sign-up form is visible on first paint, in the Hero. No scrolling required to find it. The Footer CTA is for visitors who scrolled past, not the primary path.
- **Spacious dominant** — waitlist pages run `spacious` and `medium`; one `dense` section is the maximum (probably FAQ). The page reads as patient confidence.
- **Honest signals only** — every number on the page must be real. No fake "1,247 people joined today" tickers, no inflated countdown timers, no decoy capacity meters. Visitors smell fabrication immediately and never sign up.

---

## Don'ts (additions to the §16 list)

<!-- TODO 设计师: 加 5-8 条 waitlist 特定 don't。提示:fake counter / multiple email fields(name+company+role+phone 直接放弃 50%)/ checkbox 默认勾选订阅 newsletter / "Beta Program · Early Access · Pre-launch · Limited Spots" 四标签同框 / 倒计时归零后还在跳 / form 在 modal 里(visitor 已经看到 page,modal 是过度仪式)/ exit-intent popup。 -->
