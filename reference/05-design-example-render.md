# 05 · Render the Design Example

> Design Example is the **first artifact Chris looks at** — and the gate the rest of the pipeline waits on. It is the visual truth: a real page rendered from the Slot, embedded in the Vite renderer as an iframe so scroll-triggered animations fire naturally, with manual width drag and Web / Mobile preset toggles so the same Slot can be judged across viewports before any Prompt is generated.

## Why Example comes first now

R-101 reversed the old order. Previously: Slot → Prompt → render. The Prompt was the long-lived artifact and the renderer was a downstream check, so drift between what the Prompt said and what Chris actually wanted was discovered late — sometimes after the weak model had already used the Prompt to ship pages.

R-101 inverts the chain. Slot → **Example** → (Chris confirms) → Prompt extracted from the confirmed Example. The Example is where taste and iteration happen; the Prompt is a frozen derivative the weak model reads after Chris has signed off on the visuals. The Design System view is also derivative — it only shows what the Prompt describes (System ⊆ Prompt ⊆ Slot SoT).

This means three things in practice:
- Iteration loop lives at the Example. Most rounds are Slot tweaks → Example re-renders → eyeball → another Slot tweak. No Prompt regen between every micro-change.
- Chris confirming the Example is a **hard gate**. The Prompt auto-extract step (`05-prompt-generate.md` Step B) does not fire until Chris explicitly says the Example is OK.
- The Design System view is a documentation surface, not a design surface. If a token is in the Slot but does not appear in the Example, it should not appear in the System either — System renders what the Prompt names, and Prompt names what the Example shows.

## When to use this step

- Every time you finish step 04 (new Slot) — render Example, look, iterate.
- After any Slot tweak in step 08 iteration — re-render Example, eyeball, decide whether another round of Slot changes is needed or Chris is ready to confirm.
- Before step 06 review and step 07 prompt-generate — both gate on a confirmed Example.

Do **not** use this step for:
- Manual layout tweaks (open the renderer source for those — `renderer/src/views/...`).
- Producing screenshots for a client deck (use the browser dev tools or a screenshot CLI; the renderer is for development).
- Regenerating the Design Prompt md (that is step 07, and only after Chris confirms here).

## The renderer at a glance

Location (example project): `examples/vibe-view-campaign-report/renderer/` (corresponds to `design-prompt-management/` in a scaffolded project — the nested renderer cloned by `scripts/scaffold-project.sh`). React 18 + Vite + TypeScript + Tailwind 3 + shadcn + motion 12 + paper-shaders + recharts.

**View tab order (R-101)**: `Design Example | Design System | Design Prompt`. Example is leftmost because it is what humans look at first; System and Prompt are documentation tabs that exist to verify the Example, not to drive it.

Three views:

1. **Design Example** (default tab) — a sample page rendered from the Slot, with every component the scenario allows. Rendered **inside an iframe** so scroll-triggered animations (`whileInView`, IntersectionObserver, paper-shader autoplay) fire as the user scrolls inside the iframe — independent of the outer renderer's scroll position. Manual width drag handle on the iframe's right edge. Web / Mobile preset buttons in the footer snap the iframe to 1440 / 420 px.
2. **Design System** — atomic tokens (color, type, spacing, radius), molecular composition (KPI card, Quote block), Hero composition variants, Ornaments showcase. **Constrained to what the Prompt describes** — System ⊆ Prompt. If the Slot declares an ornament the Prompt does not name, the System should not surface it.
3. **Design Prompt** — the produced md with Shiki highlight, Copy button, Full / Diff vs Previous tabs, version badge, Updated/Lines/Chars stats, Changelog accordion. **Frozen artifact** — generated only after Chris confirms the Example.

Left sidebar: persistent style picker. Six styles grouped by mode (明亮 / 暗黑 / 彩色). Click a style → all three views switch to its Slot.

Footer: current style version + Web (1440 px) / Mobile (420 px) preset + manual width readout.

## Steps

### 1. Launch the renderer

```sh
cd renderer
bun install   # first time only
bun dev
```

`bun dev` boots Vite on `http://localhost:5173`. The Design Example tab is the default landing view.

### 2. Verify the Example renders

Open:

```
http://localhost:5173/?view=design-example&style=<handle>
```

The iframe should load without console errors. If it 500s, the most common causes are:
- Slot file referenced by handle does not exist (`src/data/<handle>.slot.json` missing or path typo).
- Slot has a schema-invalid field type (`color.primary` should be `{L, C}` object, not array).
- Renderer component does not handle a new `decorative_pack` enum value (add the per-pack branch).

### 3. Scroll inside the iframe to fire animations

The iframe isolates scroll context. Click into the iframe (or scroll-wheel over it) and scroll through the page top-to-bottom. Animations to verify:

- **Hero shader** autoplay on mount.
- **Chapter opener** `whileInView` reveal as each chapter enters the viewport.
- **KPI cluster** counters animating up from zero on first viewport entry.
- **Time series chart** path-draw animation on viewport entry.
- **Footer ornament** reveal at scroll-bottom.

If an animation fires once on initial mount but does not re-fire when you scroll back to the top and down again, that is expected (motion's `once: true` default). If an animation never fires at all, check the renderer's IntersectionObserver root — it should be the iframe's document, not the outer window.

### 4. Manual width drag

Grab the iframe's right edge and drag. The iframe width updates live, and any container-query-based responsive rules inside the page fire as the width crosses breakpoints (`.report-frame` container queries — R-94 Stage 4). This is the fastest way to find layout that breaks between desktop and mobile without committing to either preset.

Watch for:
- Hero composition that holds at 1440 but goes one-column at < 800.
- Chart legends that wrap awkwardly between 600 and 800.
- Sidebar collapse / disclosure that fires at the wrong breakpoint.

### 5. Web / Mobile preset toggle

Footer buttons snap the iframe to:
- **Web** — 1440 px wide.
- **Mobile** — 420 px wide.

Always look at both before confirming. A page that reads beautifully at desktop and breaks at mobile (or vice versa) is half-shipped. The most-recurring small bug in the example project is Web-only audit; mobile is the second look.

### 6. Side-by-side audit against the references

Open the reference images (from `_attachments/style-mood-references/<handle>/`) in one window, the renderer Example tab in another. Score, in your head:

- **Hero shader** matches the references' opening field? (Most impactful — get this right first.)
- **Chart colors** in a single hue family, not pastel-rainbow?
- **Font weights** consistent with the brief and the pack signature?
- **Dividers / chapter markers** match the pack's signature elements?
- **Composition** at section level — does Hero Monolith look like Hero Monolith? Does Time Series feel like the references?

Capture deltas as Round-Log §2 candidate entries. Do not patch yet — finish the audit, then go to `08-iterate.md` to tune the Slot, then come back here and re-render.

### 7. DOM-level verify (when you do not trust your eyes)

Open the dev tools console (inside the iframe, not the outer page):

```js
// per-pack signature element counts
document.querySelectorAll('[data-seal-stamp]').length
document.querySelectorAll('.rep-chapter-num.festive-editorial').length

// chart palette in hue family
[...document.querySelectorAll('[fill]')].map(el => getComputedStyle(el).fill)
```

For sub-agent verify proof (per `02-roles.md`), use `mcp__Claude_Preview__preview_eval` against the iframe's URL. The example project's R-90 #24 fix relied on the eval approach — `querySelectorAll('[data-festive-royal] .rep-chapter-opener .seal-stamp').length === 7` caught a sub-agent's "all chapters PASS" claim that was actually 1/7.

### 8. Cross-style sanity

After patching one style, click through all six in the sidebar. If a global change leaked (e.g. you accidentally edited `.rep-hero` instead of `.rep-hero.festive-royal`), another style will show the regression. R-87 #18 and R-92 #26 both started this way — a single-pack patch broke a neighbour.

### 9. Chris confirms (the gate)

When Chris says "OK" / "this is the one" / "confirmed" on the Example for a given style + version, that triggers step 07 prompt-generate Step B (Cowork dispatches Opus to extract the Prompt from the confirmed Slot + Example). Until that moment, the Prompt is either absent or a stale draft from a previous round.

Record the confirmation in Round-Log §2 with the Slot version at the time. The auto-extracted Prompt's filename will embed that version.

## Definition of done

- `bun dev` returns HTTP 200 on `http://localhost:5173`.
- Design Example tab renders the iframe without console errors for the style you just touched.
- Scroll-triggered animations fire correctly inside the iframe.
- Manual width drag works smoothly across the 420–1440 range.
- Web and Mobile presets both render without breaking.
- Cross-style click-through shows no neighbour regressions.
- Chris (or whoever owns taste for the style) has confirmed the Example.

## Pitfalls

- **Generating the Prompt before Chris confirms.** The Prompt is a derivative. Generating it early means you regenerate every iteration round, and the Round-Log §3 snapshot churns. Wait for the gate.
- **Editing renderer source without committing.** The renderer is the truth for the Example. If you patched it to make a Slot look right, you have either (a) found a real renderer bug, in which case commit + Round-Log it; or (b) papered over a Slot bug, in which case revert the renderer and fix the Slot.
- **Looking only at the System tab.** System view may look fine while Example breaks (e.g. a pack signature shows in the showcase but not in the actual report). Example is the truth; System is documentation.
- **Ignoring console warnings inside the iframe.** Recharts `dataKey` warnings, motion `prefers-reduced-motion` warnings, and React `key` warnings all eventually become render bugs. Treat them as P2 issues to capture in Round-Log §2.
- **Web/Mobile drift.** Forgetting Mobile audit is the example project's most-recurring small bug. Make it a checklist item every render pass.
- **Treating the iframe as production-ready.** It is a development surface. It is faster to load, easier to inspect, and more honest than a deployed page — but it is not the page. The weak model produces the page from the Design Prompt md; the iframe just helps Chris judge whether the Slot is ready for Prompt extraction.

## Scenario extension — when the renderer needs to learn a new scenario

The current renderer's Design Example view is hard-coded for Campaign Report. Adding a new scenario (waitlist, catalog) requires forking the renderer:

- Add a `?scenario=<handle>` URL param.
- Fork `src/views/design-example/` per scenario, or compose from per-component primitives.
- Wire a top-level scenario picker (above the sidebar style picker, or to the right of view tabs).

R-98+ goal in the example project's backlog is "scenario-aware renderer" — until then, treat the renderer as Campaign-Report-shaped for one scenario at a time. Multi-scenario renderer is on the roadmap; do not block style work waiting for it.
