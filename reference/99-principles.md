# 99 · Core Principles

> Twelve principles, generalised from the example project's Round-Log §1. Each is a rule of thumb that pays back across many rounds. Read this file at the start of every iteration; refer back when a design judgement is hard.

The principles are not invented from theory. Each one is a scar — a round where the project did the wrong thing, paid the cost, and abstracted the lesson so future rounds skip the cost.

---

## Principle 1 · Solve at the source, never patch over symptoms

The minimum number of layers wins. If element A causes a problem, fix A; never use element B to cover up A.

| Wrong | Right |
|---|---|
| Filled card looks weak → add a border to "anchor" it. | Drop the border. Fill alone separates. |
| Heavy dark line on a panel reads too aggressive → lighten the panel bg to compensate. | Use whisper-thin line instead. Reserve heavy lines for `<hr>` only. |
| Hero shader colorFront too dark → add `backdrop-filter: blur(8px)` overlay to make text readable. | Lower the shader's `colorFront` lightness / chroma directly. |
| Element looks too prominent → add a drop-shadow on a neighbour to balance. | Adjust the element's L value. |

Source: example project R-81 / R-82 / R-83 — three rounds of Chris correcting the same mistake.

---

## Principle 2 · Hero ≠ chapter

Hero is the opening (chapter 0). It is *not* a numbered chapter. So Hero never renders:

- ChapterStamp / chapter number marker.
- Chapter kicker label.
- Per-chapter ornament (SealStamp, ChapterNumeralLarge, etc.).

Hero ornament is reserved for: eyebrow (e.g. "VIBE VIEW · ANNUAL CAMPAIGN"), Display Number, delta, lead paragraph, and the Hero shader.

Source: example project R-83 #9. Cowork added a `ChapterStamp` to the Report Hero because the loop iterated chapters 0..N — chapter 0 is special.

---

## Principle 3 · weight ≤ 500 baseline, signature packs may exceed

Default weight ceiling across all styles: 500. Heavier weights are slop unless the pack explicitly declares them as its signature element. Current signature exceptions:

- Swiss systematic — 700 caps Helvetica is the signature.
- Festive-Royal — 700 serif (Cormorant Garamond) is the signature.
- Festive-Editorial — 800 sans (Helvetica Neue) is the signature.

In `Slop-Taxonomy.md` A3: any 700+ weight outside an explicit signature reads as cheap.

Source: example project Phase B.5; Slot schema v0.3+ added `weight_ceiling` enum 500/600/700/800 with default 500.

---

## Principle 4 · Large radii are not slop

A 16 px card radius does not automatically read as cheap. The Slot's `radius.card_chrome` is the contract; render exactly what it declares. Warm 16, Theatre Double-Bezel, Cool 4, Swiss 0 are all legitimate.

What is slop: inconsistent radii within a single style, or radii that contradict the Slot's `sharp_panel_max_px` constraint.

Source: example project R-81 #3. Cowork applied a blanket "small radius = sharp" rule and overrode Chris's brief.

---

## Principle 5 · Filled elements never carry visible borders

Any element with a non-transparent `background` (`bg-surface-l2`, `bg-surface-l3`, `var(--primary)`, etc.) drops its border. Fill *alone* separates the element from its surroundings; adding a border is redundant and cheap-feeling.

**This applies to every filled element**, not just cards:
- Cards. ✓
- Sidebar items in their active state. ✓ (R-89 #22 — a sub-agent argued "active indicator is not a card double-decoration", Chris ruled it slop anyway.)
- Nav buttons.
- List items.
- Pills with a fill.

Source: example project R-81 #4 + R-89 #22.

---

## Principle 6 · Heavy / dark-saturated borders only as dividers

A `1px solid var(--foreground)` border on a card overwhelms the panel and reads as cheap. Heavy/dark borders are reserved for:

- `<hr>` page dividers.
- Chapter hairlines (the line that closes a chapter).
- Section breaks between major regions.

Card borders, when present at all, stay at `var(--border)` whisper-thin (≤ 12% alpha).

Source: example project R-82 #5. Cowork used heavy borders on cards "for editorial gravity"; Chris flagged it as slop.

---

## Principle 7 · Hero must contain a shader

The Hero is the page's visual basis. Every style declares a Hero shader from the paper-shaders library (or a documented equivalent):

- Warm → GrainGradient (warm ember breath).
- Theatre → MeshGradient (theatrical color depth).
- Cool → GodRays (cool light shafts).
- Swiss → Dithering (Swiss-systematic neutral pattern).
- Festive-Royal → GrainGradient (deep red grain breath with gold highlights).
- Festive-Editorial → GrainGradient (red corners blur on ivory).

Replacing the shader with a static CSS background (`background: linear-gradient(...)`) hollows out the style's identity. The shader is non-negotiable.

Source: example project R-82 #6. Swiss originally used a static dot-grid; Chris asked for Dithering shader.

---

## Principle 8 · Tune shader props, never wrap a shader

If a Hero shader causes an accessibility or readability problem, adjust *its* props (`colorFront`, `colorBack`, `size`, `opacity`, `speed`). Never:

- Add a `div` mask over the shader.
- Add a `backdrop-filter: blur(...)` on top of the shader.
- Add a `linear-gradient` overlay.

Each wrapper is a layer of debt. The shader is the source; everything else is a hack. (Principle 1 in shader-specific form.)

Source: example project R-83 #8. Cowork accepted a sub-agent's `backdrop mask` fix; Chris rejected it and demanded the source fix.

---

## Principle 9 · Patch then verify with rendered proof

A `grep -c` on the file you just edited does not prove the change is live. The renderer (or the weak model's actual output) is the truth. Always:

1. **Enumerate all render paths.** A patch to one render branch leaves N others unpatched (R-87 #18 ShadCard children, R-90 #24 chapter opener × 7).
2. **Sync inline data with external Slot.** Drift between `renderer/src/data/<slot>.slot.json` and any inline copy is the most-recurring bug class (R-84 #11).
3. **Verify multi-dimensional alignment.** Fixing A may break B. R-86 #15 fixed "line passes through dot" but broke "dot aligns with title" — the fix has a trade-off you must look for.
4. **Re-render and look.** `mcp__Claude_Preview__preview_eval` for DOM evidence; eyes for taste.

Source: example project R-84 #11 + R-86 #15 + R-90 #24. The same lesson re-learned three times before it stuck.

---

## Principle 10 · Hero shader containers never use `position: fixed`

`<canvas>` / SVG containers for Hero shaders (GrainGradient, MeshGradient, GodRays, Dithering) use `position: absolute` inside `.rep-hero { position: relative }`. Never `position: fixed`.

`position: fixed` historically breaks:
- z-index control (fights the rest of the page).
- Scroll behaviour (shader detaches from Hero).
- iframe embedding (shader renders against the wrong viewport).

`position: fixed` is reserved for viewport-level overlays (modal, nav) — never Hero decoration.

Source: example project R-93 #30 C1. Chris repeatedly debugged the same z-index bug across rounds before the principle was abstracted.

---

## Principle 11 · Design Prompt ≤ 620 lines, every word constrains

Weak models (doubao-seed-code 2.0, GPT-OSS-20B, similar) have precious context. The Design Prompt is the artifact they read.

- Hard ceiling: **620 lines** (was 600 in early R-91; relaxed to 620 in R-95 #40 to allow Festive packs).
- Every sentence answers "would the output measurably degrade without this?". If no, cut it.
- **Strict zero tolerance:**
  - Metadata (Source provenance, Last updated, Inspired by, inline `(source: ...)`).
  - Few-shot examples (`## Example` sections, full code snippets).
  - Emoji checklists (✅ / ❌ / 🚫 — use the words "do" / "don't" instead).
  - Historical narrative ("In v0.2 we tried X, but Chris said...").
  - Decorative repetition.

Source: example project R-93 #30 C2, then R-95 #40 trim round. Chris's Memory files (`feedback_prompt_md_no_metadata.md`, `feedback_prompt_md_no_emoji_checklist.md`, `feedback_prompt_md_minimize_code.md`, `feedback_prompt_engineering_concise.md`) accumulate the long form.

---

## Principle 12 · Three-Way Sync: Prompt ↔ Design System ↔ Report Example

Three artifacts describe one style; they must agree:

```
Design Prompt md   ⇄   Design System view   ⇄   Report Example view
(what we tell the      (what the Slot           (what actually
 weak model)           declares)                renders in browser)
```

**Hard rules:**

1. Every ornament the Design Prompt names → declared in Slot → rendered in Report Example.
2. Every token the Slot declares → described in Design Prompt → used in Report Example.
3. Every element rendered in Report Example → comes from Slot → described in Design Prompt.

**Any change in any of the three:** re-audit all three. Drift = a real bug, not a cosmetic mismatch.

**Source-of-truth rule:** the Slot is the truth. The renderer renders the Slot; the prompt describes the Slot. If two of three disagree with the Slot, fix them — do not edit the Slot to match a temporary state of the other two.

Source: example project R-93 #31 D3 audit found the most-painful drift class — Warm/Theatre/Cool/Swiss prompts named four ornaments that the renderer never rendered. R-94 Stage 6 cleaned the drift; R-95 #41 caught a fresh contradiction (template said 800-weight while Slot said 500).

---

## Principle 13 · Cowork filters sub-agent patches through the principles

When a sub-agent proposes a patch — CSS rules, prompt prose, schema fields — Cowork does *not* paste-through to the produced artifact. Cowork is the gate. Every sub-agent suggestion must pass the twelve principles in this file before it lands.

The failure mode: sub-agents have deep specialty knowledge (React, CSS, Tailwind) but no memory of this project's principles. They will propose `✅ correct / ❌ wrong` few-shot examples, full code snippets, prose mission statements, "Inspired by" attributions — every red line in Principle 11 — because their training pulls those patterns. Cowork pasting through = the red line lands.

**The discipline.** When reviewing a sub-agent patch:

1. Read the patch against Principle 11 (the strictest principle for prompt md). If the patch adds metadata / few-shot / emoji checklist / full snippet, transform it to prose before forwarding.
2. Read the patch against Principle 1 + 8. If the patch adds a layer to compensate for a flaw, push back and ask for a source-level fix instead.
3. Read the patch against Principle 12. If the patch changes one of {Slot, template, renderer}, audit the other two.

The "delete vs add" trap. After catching a violation, Cowork sometimes over-corrects into "delete everything the sub-agent proposed". Wrong. The rule is *necessity*: keep what is necessary, drop what is not, regardless of whether the line is a deletion or an addition.

Source: example project R-79 — Cowork forwarded a Coder sub-agent's `✅ / ❌` double example into the produced md; three Principle 11 violations landed before Chris caught it. R-79b: Cowork over-corrected with "delete only, never add" — Chris ruled that wrong too.

---

## Principle 14 · Rendered evidence beats self-graded "PASS"

A sub-agent reporting "all six styles PASS" is *not* verification. The only verification that counts is rendered evidence — DOM counts, screenshots, `wc -l`, `grep -c` from Cowork's own run.

A sub-agent self-grade is a *summary*; it compresses what they think they did. Compression discards exactly the bugs you care about: the chapter you missed, the inline data you forgot to sync, the `:not()` exclusion you didn't update.

**The discipline.**

- Sub-agent prompts must demand rendered proof (`02-roles.md` §D). DOM eval counts. `ls -la <canonical path>`. `wc -l` before and after. Anti-slop grep with expected count.
- Cowork's verify pass re-runs the same commands independently — never trusts the sub-agent's output alone.
- When Slop Taxonomy detectors fire, the violation stands. Sub-agent arguments do not override Blocking findings (R-87 #18 → R-89 #22, twice burned).
- When the verify path is ambiguous (canonical vs worktree), verify on the *destination*, not the CWD (R-94 #35).

Source: example project R-87 #18, R-89 #22, R-90 #24, R-94 #35 — four rounds where a "PASS" report hid a real bug. The principle hardened only after the fourth.

---

## How to use this file

- **Start of every iteration round** — re-read this file (it is short on purpose). Re-loading the principles in working memory prevents re-learning them the hard way.
- **When a design feedback is ambiguous** — find the principle that applies. Chris's "this feels off" usually maps to one of the twelve.
- **When you are tempted to add a layer** — Principle 1 is doing 80% of the work in this skill. Re-read it.
- **When abstracting a new lesson from your project's Round-Log §1** — check whether one of these twelve already covers it. If so, your project's principle is a *specialisation* (e.g. "Principle 1 in shader-specific form" — that is Principle 8). If not, write a new one with the same shape (rule, table of wrong/right, source round).

The principles are generalised here. Each project's Round-Log §1 will accumulate its own specialisations as it runs.
