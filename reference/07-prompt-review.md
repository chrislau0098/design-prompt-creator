# 06 · Review the Design Prompt

> The Design Prompt is the artifact the weak model will read. Review it across three axes: **three-way sync** (System ⊆ Prompt ⊆ Slot SoT, with Example as the visual anchor), **anti-slop** (the rubric in `Slop-Taxonomy.md`), and **line economy** (≤ 620 lines, every word constrains).

## When to use this step

- After `05-prompt-generate.md` Step B produced a fresh auto-extracted Design Prompt md from a Chris-confirmed Example.
- After `08-iterate.md` patched a Slot post-confirmation (which forced an Example re-render + re-confirm + Step B re-extract).
- Periodic audit (every Phase end) of all styles, regardless of which one was last touched.

Do **not** use this step for:
- The first creative judgement on whether the style "feels right" — that is `05-design-example-render.md`. Review here is about *invariants and drift*, not taste.
- Reviewing a Step A draft Prompt. Drafts are bootstrap scaffolding; review fires against the Step B final extract only.

## Step 0 · Confirm the Design Example (gate)

Before any of the three review axes run, this step gates on **two** Chris confirmations from earlier in the workflow:

1. **Example confirmation** (from `05-design-example-render.md` step 9) — Chris signed off that the iframe-rendered Example for this style version is the visual target.
2. **Prompt confirmation** (from `05-prompt-generate.md` Step B.3) — Chris signed off that the Opus-extracted Prompt md accurately describes the confirmed Example.

If either is missing, **stop here**. Reviewing a Prompt that Chris has not confirmed wastes the audit and risks blessing drift. Common failure modes that bypass this gate:

- Cowork re-extracts the Prompt after a small Slot tweak without sending the regenerated Example back to Chris for re-confirmation. The new Prompt may describe an Example Chris never saw.
- An iteration round patches the produced md directly (no Step B re-fire) and someone runs the audit assuming the md is the source of truth. The Slot, the Example, and the Prompt have all drifted apart.
- Sub-agent dispatch returns a Prompt md without proof that Chris re-confirmed. Round-Log §2 must show both confirmation timestamps for the current version.

The fix in every case: go back to step 05, re-render the Example for the current Slot version, get Chris confirmation, fire Step B, get Chris confirmation on the Prompt, **then** come here.

## The three review axes

### A · Three-Way Sync

This is Principle 12 in `reference/99-principles.md` and the most-quoted rule in the example project after R-94. Three artifacts describe the same style; under R-101 the relationship is **subset, not equality**.

```
                   Slot JSON  (Source of Truth — atomic + molecular + ornament)
                       │
                       │  Step B auto-extract (Opus, gated on Chris confirm)
                       ↓
                  Design Prompt md
                  (what the weak model reads — describes only what the Example renders)
                       │
                       │  Derivative — System renders what Prompt names
                       ↓
                Design System view
                (atomic + molecular tokens the Prompt actually names)

                Design Example  (iframe rendering of Slot, the visual anchor)
                  ↑ Prompt is extracted from this; System is bounded by this via the Prompt
```

**The subset relationship (System ⊆ Prompt ⊆ Slot):**

- The **Slot** is the full atomic + molecular + ornament SoT. It may declare tokens the current Example does not surface (held in reserve for future Examples).
- The **Prompt** describes only what the confirmed Example actually renders. If the Example does not show an ornament, the Prompt does not name it — even if the Slot declares it.
- The **System view** showcases only what the Prompt names. If the Prompt does not describe a token, the System tab does not surface it as a documented element.

**Hard rules (R-101 update):**

1. Every ornament the Design Prompt names must (a) be declared in the Slot, (b) actually render in the confirmed Example, and (c) appear in the System tab's Ornaments showcase. All three or none.
2. Every visual element in the confirmed Example must be described in the Design Prompt **and** trace back to a Slot field. An element in the Example that has no Slot field is a renderer bug; an element in the Slot that does not appear in the Example is dormant and should be either removed from the Slot or kept silent in the Prompt + System.
3. The System tab may not surface a token that the Prompt does not name. If you see a System entry for "Cinnabar Imprint" but the Prompt's md does not mention `Cinnabar`, either the System tab is showing a dormant Slot field (fix the System filter) or the Prompt is missing a description (fix the Prompt via a Step B re-dispatch).

**Drift symptoms** (taken from R-93 #31 D3 audit, re-framed for R-101):
- Design Prompt names `GoldenHairline` as the chapter divider. Slot declares `divider.golden_hairline`. The confirmed Example renders a plain `<hr>` instead. → Drift (Example does not match what Prompt says; either re-render the Example until it matches Slot, or re-extract the Prompt to describe the actual Example).
- Slot has `chart_ramp` of 4 hue values. Design Prompt describes single-hue ramp. Confirmed Example renders Tailwind default palette. → Drift (all three artifacts disagree; the Example is the visual anchor, decide what Chris actually confirmed and re-sync from there).
- Confirmed Example renders a `Cinnabar Imprint` ornament at Hero. Slot has no `cinnabar` field. Design Prompt does not mention it. → Drift (renderer is rendering something the Slot does not capture — a renderer bug; either add the Slot field and re-extract the Prompt, or remove the ornament from the renderer).
- Slot declares `divider.cinnabar_bar`. The confirmed Example does not render it. Prompt correctly omits it. System tab surfaces "Cinnabar Bar" anyway. → Not drift in the Prompt, but the System tab is over-surfacing (it should only show what Prompt names). Fix the System filter.

**Verify proof:**

```sh
# planned script: scripts/verify-three-way-sync.py
python3 scripts/verify-three-way-sync.py \
  --slot      src/data/<handle>.slot.json \
  --prompt    src/prompts/<file>.md \
  --renderer  http://localhost:5173/?style=<handle>&view=report
```

Until the script ships, do the audit manually:

1. List every ornament / component in the Design Prompt (`grep -i 'SealStamp\|HairlineRule\|...'`).
2. Cross-reference against the Slot's `dividers`, `ornaments`, `hero_shader` fields — each named element in the Prompt must trace to a Slot field.
3. Open the Design Example iframe and `document.querySelectorAll('[data-seal-stamp]')` etc. — each Prompt-named element must appear with a non-zero count in the Example. Every Example element should map back to a Prompt sentence; if not, the Prompt is incomplete.
4. Open the Design System tab — each entry should appear in the Prompt's prose. If System surfaces a Slot field the Prompt does not name, the System filter is too loose.

Any mismatch → patch the lagging artifact. The decision rule under R-101: **the Slot is the SoT, the Example is the visual anchor, the Prompt describes the confirmed Example, the System surfaces what the Prompt names**. If the Prompt drifts from the Example, re-fire Step B from the confirmed Slot version (do not hand-edit the Prompt unless it is pure-deletion trim). If the Example drifts from the Slot, fix the renderer (this is a renderer bug, not a Prompt bug). If the Slot itself is wrong, fix it, re-render the Example, get Chris re-confirmation, then re-fire Step B.

### B · Anti-slop

The example project's `Slop-Taxonomy.md` (located at `examples/vibe-view-campaign-report/Slop-Taxonomy.md`) is the cross-style anti-slop rubric. Distilled from R-81 #4, R-82 #5, R-89 #22, and accumulating Chris feedback. Categories:

- **A1 · Generic AI visual tropes** — purple gradients, glassmorphism, backdrop-filter blur ≥ 3 px, nested cards, drop shadows on every panel.
- **A2 · Filled element with visible border** — `bg-surface-l2 + border 1px solid var(--border)` on the same element. Applies to cards, list items, nav items, sidebar items (R-89 #22 extension). Filled + border = redundant. Choose one.
- **A3 · Weight ≥ 700 outside an explicit signature pack** — Swiss IBM 700 caps is the signature; festive-royal 700 serif is the signature; festive-editorial 800 sans is the signature. Anywhere else, ≥ 700 reads as cheap.
- **A4 · Hero shader contrast patched at the wrong layer** — a `backdrop-filter`, `mask`, or `gradient overlay` placed *over* the Hero shader to make text readable. Solve at the shader (`colorFront` lightness/chroma) instead.
- **A5 · Decorative-only ornament** — an ornament that does not encode structure. The hairline that opens a chapter is structural; the swirl that "looks nice" is slop.
- **A6 · Chart palette outside brand hue family** — Tailwind defaults, library rainbow, brand-hue swap mid-page.
- **A7 · Few-shot examples or full code snippets inside the Design Prompt md** — context-killer for weak models.
- **A8 · Smart quotes in JS string literals** — `'"Cormorant"'` with U+201C / U+201D. Breaks at runtime (R-90 #24).

**Verify proof (greps):**

```sh
PROMPT=src/prompts/<file>.md

# A1 visual tropes
grep -nE 'glassmorph|backdrop-filter:\s*blur\([3-9]|nested-card|drop-shadow.*0 8px' "$PROMPT"

# A2 filled + border (find suspicious patterns in renderer CSS too)
grep -nE 'bg-surface-l[23].*border\s+\d+px|border-left:\s*\dpx solid var\(--primary\).*active' renderer/src/**/*.css

# A3 weight ceiling violation (allow per-pack exceptions)
grep -nE 'font-(bold|extrabold|black)' "$PROMPT" | grep -v 'festive-royal\|festive-editorial\|swiss\|systematic'

# A4 shader overlay (look in renderer)
grep -nE '\.rep-hero[\.-].*(backdrop-filter|::after.*background.*gradient)' renderer/src/**/*.css

# A7 few-shot / code-fence presence
grep -cE '^```(jsx|tsx|html)' "$PROMPT"  # ≤ 5 typical; > 10 = too many snippets

# A8 smart quotes in JS templates
grep -nP '[‘’“”]' renderer/src/**/*.ts renderer/src/**/*.tsx
```

The A1, A2, A4, A8 detectors should all return 0 lines after a clean review. A3 returns the per-pack exceptions only. A7 stays under 5 code blocks.

### C · Line economy

The hard ceiling is 620 lines (Principle 11). Above that, the weak model's context budget hurts. Trim playbook:

1. **Delete pure deletions first.** Hand-edit the produced md with `manual_override: true` for trim that is purely redundant prose. R-95 #40 did exactly this: Swiss 626 → 604, Festive Royal 666 → 611, Festive Editorial 677 → 620. The deletions were §2 redundant color rule bullets, §6 repeated whileInView prose, §17 Recharts paragraph collapse, decorative blank lines.

2. **Migrate trim back to the template.** If a trim survives one re-inject cycle without regressing, the same prose should be removed from the template so the trim is permanent — not preserved as a hand-edit.

3. **Question every `{{#if}}` branch.** A per-pack branch that runs for every style with the same content is dead weight; pull it out of the branch. A branch that runs for one style with a long unique prose may be overkill — what is the shortest sentence that conveys the constraint?

4. **Snippets vs prose.** Five-line React snippets in the prompt usually translate worse than one prose sentence ("ChapterOpener uses HairlineRule as the top row and ChapterNumeralLarge + chapter title on the baseline row"). Convert snippets to prose where possible.

5. **Cut metadata, source URLs, "Inspired by", "Last updated".** None of these constrain the weak model. They occupy precious context. Strict zero tolerance.

**Verify proof:**

```sh
wc -l src/prompts/*.md
# all should be ≤ 620
```

## Steps

### 1. Run the three verify scripts (or do their manual equivalents)

In sequence:
- Three-way sync verify (manual or `scripts/verify-three-way-sync.py` planned).
- Anti-slop greps for A1–A8.
- `wc -l`.

Capture the outputs in a scratch buffer. The whole pass should take 5–10 minutes per style.

### 2. Classify findings

Each finding lands in one of four buckets:

- **Blocking** — A1, A2, A4, A8 detector hits; three-way drift on a named pack ornament; > 620 lines. Must fix before the prompt is considered shipped.
- **High** — A3 violation in an unsigned pack; A6 chart palette; line count 600–620 (warning band).
- **Medium** — A5 decorative ornament that is structural-adjacent (judgement call); cross-style cosmetic difference.
- **Low** — A7 code blocks ≤ 5 (acceptable); minor renderer console warning.

### 3. Patch (or route to `08-iterate.md`)

Blocking + High → patch immediately. Decide the patch site (Slot / template / renderer / produced md trim) per `08-iterate.md` decision table, then re-inject and re-verify.

Medium + Low → log in Round-Log §2 as a candidate for a future round. Do not let them block the current round.

### 4. Cross-style audit

After patching one style, run the same greps across all six. A1 / A2 are commonly global (e.g. a shared CSS class regression); finding them in style #1 means they probably exist in styles #2–#6 too.

### 5. Update Round-Log

§2 entry summarising findings + patches. §3 update version snapshot if any Slot / template / md version bumped.

## Definition of done

- Three-way sync: 0 drift for the audited style(s).
- Anti-slop greps: 0 hits in A1, A2, A4, A8.
- Line count ≤ 620.
- All Blocking + High findings patched and re-verified.
- Round-Log §2 captures the review pass.

## Pitfalls

- **Trusting one detector.** Each grep catches a fraction of the rubric. Run all eight in A; do not assume "A1 was clean last week, so I will skip it this week".
- **Patching the produced md when the bug is in the template.** A re-inject overwrites the patch. If the bug is structural (a per-pack branch missing), fix the template.
- **Three-way sync interpreted as "make all three agree to whatever the renderer shows".** The Slot is the source of truth. The renderer renders what the Slot declares. The prompt describes what the Slot declares. If the renderer is wrong, fix the renderer to match the Slot — not the other way around.
- **Anti-slop applied unilaterally without checking the per-pack signature exception.** Swiss is supposed to have 700-weight caps. Festive-Royal is supposed to have 700-weight serif. Filter the grep output by the pack's signature exemption before treating it as a violation.
- **Trim without `manual_override` flag.** Next re-inject silently destroys hours of trim work. The flag is the contract.
- **Six-style audit collapsed to one.** A regression in style #4 was introduced in week N; week N+3 catches it in style #4 only and patches just that style. The other five may carry the same regression. Always cross-style sweep.
