# 06 · Render in the Vite Renderer

> The Vite renderer is the **visual truth** — the thing humans look at to judge whether the Slot, the Design Prompt, and the actual render agree. Three views: Design System (atomic + molecular tokens), Report Example (a sample page rendered from the Slot), Design Prompt (the produced md with Diff and Copy).

## When to use this step

- Every time you finish step 04 (new Slot), step 05 (re-inject prompt), or step 08 (any iteration patch). Open the renderer and look.
- Cross-team review with a designer or PM who does not want to read JSON or md.
- Pair-review with Chris on aesthetic judgements — the renderer is the shared artifact.

Do **not** use this step for:
- Manual layout tweaks (open the renderer source for those — `renderer/src/views/...`).
- Producing screenshots for a client deck (use the browser dev tools or a screenshot CLI; the renderer is for development).

## The renderer at a glance

Location (example project): `examples/vibe-view-campaign-report/renderer/` (corresponds to `design-system-renderer-vite/` in the project itself). React 18 + Vite + TypeScript + Tailwind 3 + shadcn (real shadcn-cli install) + motion 12 + paper-shaders + recharts. Latest renderer state: R-95 #42 ships shadcn `Sidebar` with `SidebarProvider`, all-dark OKLCH theme, Design Prompt tab with `@pierre/diffs` and Shiki highlighting.

Three top-level tabs (the views):

1. **Design System** — atomic tokens (color, type, spacing, radius), molecular composition (KPI card, Quote block), Hero composition variants, Ornaments showcase. This is the Slot, rendered.
2. **Report Example** — a sample report rendered from the Slot, with every component the scenario allows. This is the *page*, rendered.
3. **Design Prompt** — the produced md with Shiki highlight, Copy button, Full / Diff vs Previous tabs, version badge, Updated/Lines/Chars stats, Changelog accordion.

Left sidebar: persistent style picker. Six styles grouped by mode (明亮 / 暗黑 / 彩色). Click a style → all three views switch to its Slot.

Footer: current style version + Web / Mobile segmented control.

## Steps

### 1. Launch the renderer

```sh
cd renderer
bun install   # first time only
bun dev
```

`bun dev` boots Vite on `http://localhost:5173`. Production build for QA: `bun run build` (currently ~2.16 MB bundle, gzip 649 KB — R-95 #43 lists dynamic-import-shiki as the bundle-reduction candidate).

### 2. Verify the three views render

Open in order:

```
http://localhost:5173/?view=design-system&style=<handle>
http://localhost:5173/?view=report&style=<handle>
http://localhost:5173/?view=design-prompt&style=<handle>
```

Each should load without console errors. If a view 500s, the most common causes are:
- Slot file referenced by handle does not exist (`src/data/<handle>.slot.json` missing or path typo).
- Slot has a schema-invalid field type (`color.primary` should be `{L, C}` object, not array).
- Renderer component does not handle a new `decorative_pack` enum value (add the per-pack branch).

### 3. Side-by-side audit against the references

Open the reference images (from `_attachments/style-mood-references/<handle>/`) in one window, the renderer in another. Score, in your head:

- **Hero shader** matches the references' opening field? (Most impactful — get this right first.)
- **Chart colors** in a single hue family, not pastel-rainbow?
- **Font weights** consistent with the brief and the pack signature?
- **Dividers / chapter markers** match the pack's signature elements?
- **Composition** at section level — does Hero Monolith look like Hero Monolith? Does Time Series feel like the references?

Capture deltas as Round-Log §2 candidate entries. Do not patch yet — finish the audit, then go to `08-iterate.md`.

### 4. DOM-level verify (when you do not trust your eyes)

Open the dev tools console:

```js
// per-pack signature element counts
document.querySelectorAll('[data-seal-stamp]').length
document.querySelectorAll('.rep-chapter-num.festive-editorial').length

// chart palette in hue family
[...document.querySelectorAll('[fill]')].map(el => getComputedStyle(el).fill)
```

For sub-agent verify proof (per `02-roles.md`), use `mcp__Claude_Preview__preview_eval`. The example project's R-90 #24 fix relied on the eval approach — `querySelectorAll('[data-festive-royal] .rep-chapter-opener .seal-stamp').length === 7` caught a sub-agent's "all chapters PASS" claim that was actually 1/7.

### 5. The Design Prompt tab as a review artifact

The Design Prompt tab is not just "the md but pretty". It is the audit surface:

- **Full / Diff vs Previous** tabs let you see what changed between the last produced md and the current one. If your re-inject produced a six-line diff, the change was small; if it produced a 200-line diff, something bigger happened — read it before assuming intent.
- **Line count** in the header stat group. If it crept past 620, you have a trim job.
- **Changelog accordion** at the top of the md. Each round you re-inject, prepend an entry: `{date, note}` summarising the round. The renderer renders the first entry with an accent left line and a "Latest" badge.

### 6. Web / Mobile toggle

The footer's segmented control switches `?device=web` / `?device=mobile`. Mobile applies `max-width: 420px` to the report frame *and* (since R-94 Stage 4) container queries fire on `.report-frame` so mobile typography / spacing kicks in correctly without depending on outer viewport.

When auditing: always look at both. A page that reads beautifully at desktop and breaks at mobile (or vice versa) is half-shipped.

### 7. Cross-style sanity

After patching one style, click through all six in the sidebar. If a global change leaked (e.g. you accidentally edited `.rep-hero` instead of `.rep-hero.festive-royal`), another style will show the regression. R-87 #18 and R-92 #26 both started this way — a single-pack patch broke a neighbour.

## Scenario extension — when the renderer needs to learn a new scenario

The current renderer's Report Example view is hard-coded for Campaign Report. Adding a new scenario (waitlist, catalog) requires forking the renderer:

- Add a `?scenario=<handle>` URL param.
- Fork `src/views/report-example/` per scenario, or compose from per-component primitives.
- Wire a top-level scenario picker (above the sidebar style picker, or to the right of view tabs).

R-98+ goal in the example project's backlog is "scenario-aware renderer" — until then, treat the renderer as Campaign-Report-shaped for one scenario at a time. Multi-scenario renderer is on the roadmap; do not block style work waiting for it.

## Definition of done

- `bun dev` returns HTTP 200 on `http://localhost:5173`.
- All three views render for the style you just touched.
- DOM verify counts match the expected pack signatures.
- Web *and* Mobile both render without breaking.
- Cross-style click-through shows no neighbour regressions.
- Design Prompt tab Diff view shows the expected delta (not a surprise 200-line diff).

## Pitfalls

- **Editing renderer source without committing.** The renderer is the truth. If you patched it to make a Slot look right, you have either (a) found a real renderer bug, in which case commit + Round-Log it; or (b) papered over a Slot bug, in which case revert the renderer and fix the Slot.
- **Trusting one view in isolation.** Design System view may look fine while Report Example breaks (e.g. a pack signature shows in the showcase but not in the actual report). Always look at all three.
- **Ignoring console warnings.** Recharts `dataKey` warnings, motion `prefers-reduced-motion` warnings, and React `key` warnings all eventually become render bugs. Treat them as P2 issues to capture in Round-Log §2.
- **Web/Mobile drift.** Forgetting Mobile audit is the example project's most-recurring small bug. Make it a checklist item every render pass.
- **Bundle size creep.** Each new Slot is ~10 KB, each new ornament component is ~2 KB. Watch `bun run build` size between rounds; if it crosses a budget, schedule a Round to dynamic-import (the R-95 #43 candidate is `@pierre/diffs` and full-Shiki).
- **Treating the renderer as production-ready.** It is a development tool. It is faster to load, easier to inspect, and more honest than a deployed page — but it is not the page. The weak model produces the page from the Design Prompt md; the renderer just helps humans judge whether that md is the right md.
