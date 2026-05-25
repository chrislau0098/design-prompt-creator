---
scenario: campaign-report
status: shipped
maturity: reference scenario — read this first
---

# Scenario · campaign-report

The campaign-report scenario produces **periodic, data-supported retellings of a campaign, launch, period, or fiscal slice**. It anchors a single primary metric, walks the reader through evidence chapters, and exits on a quiet, attributed close.

This is the Skill's **reference scenario** — its PATTERN, components, and example Slot family were the original case the Skill was built around. New scenarios should read this one first.

## When to use

Pick `campaign-report` when the job is to **explain what happened in numbers over a defined period**. Typical briefs:

- A weekly / monthly / quarterly campaign retrospective.
- An annual or fiscal-year report (a year in review).
- A product-launch wrap-up (week 1, month 1, post-launch).
- A periodic Bitable / spreadsheet view that the team consumes as a narrative, not a dashboard.

## When NOT to use

- A live always-on dashboard with filters and time-range pickers → not a report, it's a tool.
- A single-product marketing landing page (use `product-promotion`).
- A multi-product browse experience (use `product-catalog`).
- A pre-launch sign-up page (use `waitlist`).

## What's in the box

| File | Contents |
|---|---|
| [`PATTERN.md`](PATTERN.md) | §11 archetype library · §12 composition rhythm · §13 section anatomy · §16 don'ts. Page skeleton spec. |
| [`components.md`](components.md) | The complete component contract (Hero, ChapterOpener, KPICell, TimeSeriesChart, TimelineNode, CompareGroup, RankingList, ProportionRing, Annotation, QuoteBlock, Outro, ContentDivider) with props, DOM, variants, adaptive states, and the banned list. |
| [`template.md`](template.md) | Reuses the agnostic [`templates/prompt-template.md`](../../templates/prompt-template.md) as-is. The injection contract lives there. |

## Example styles

Six production styles are shipped at [`../../examples/vibe-view-campaign-report/`](../../examples/vibe-view-campaign-report/). Each is a complete Slot JSON + a rendered Design Prompt md, plus the renderer view that proves Three-Way Sync:

- **Swiss Systematic · Editorial Blue** — light-gray, cobalt accent, ALL CAPS Helvetica Display, dense info-graphic grid. Mood: Systematic / Grid-Driven / Bold-Typographic / Editorial.
- **Theatre Dark** — deep stage palette, single warm accent, scale-jump Hero, dramatic shader. Mood: Theatrical / Confident / Cinematic.
- **Festive Editorial Crimson** — high-chroma red on warm cream, ornamented Display Number, festive flourishes. Mood: Festive / Theatrical / Bold.
- **Brutalist Mono** — black on raw paper, mono-only typography, hard-edged composition, no decoration. Mood: Brutalist / Confident / Editorial.
- **Instrumental Soft** — quiet pastel surfaces, hairline structure, restrained accent. Mood: Quiet / Editorial / Confident.
- **Neue Editorial** — magazine-grade serif Display + sans body, generous spacing, single accent. Mood: Editorial / Quiet / Theatrical.

Browse the six [`slot-examples/`](../../examples/vibe-view-campaign-report/slot-examples/) and the six [`design-prompts/`](../../examples/vibe-view-campaign-report/design-prompts/) to see how Slot variation drives style variation while PATTERN and components stay constant.

## Brief keywords that map well

When extracting a new style for campaign-report, the brief's mood adjectives steer Slot decisions. The campaign-report archetype library responds well to:

- **Emotional tone**: Confident · Theatrical · Editorial · Brutalist · Festive · Instrumental · Quiet · Cinematic · Systematic.
- **Density posture**: Dense info-graphic · Spacious editorial · Theatrical Hero + restrained chapters.
- **Decorative pack** (Slot field): systematic · editorial · instrumental · theatrical · festive.

Avoid briefs that smell like *dashboard*, *tool*, *workflow*, *form*, *catalog*, *promotion* — those route to other scenarios.

## How a new style starts

1. Collect 3–6 reference images that share a coherent visual language.
2. Run the style-extract flow at [`reference/04-style-from-references.md`](../../reference/04-style-from-references.md) → produces a Slot JSON.
3. Inject Slot + agnostic template + this scenario's PATTERN + components → produces the Design Prompt md (via [`reference/05-prompt-generate.md`](../../reference/05-prompt-generate.md)).
4. Render in the Vite renderer and audit Three-Way Sync ([`reference/07-prompt-review.md`](../../reference/07-prompt-review.md)).
5. Iterate ([`reference/08-iterate.md`](../../reference/08-iterate.md)).

The PATTERN and components stay frozen across styles — only the Slot changes.
