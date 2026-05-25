# 08 · Iterate on Feedback

> Feedback arrives as text, screenshots, or an in-person walk-through. Iteration is: classify the feedback, decide the patch site, run the patch chain (Slot → template → re-inject → renderer → verify), and capture the round.

## When to use this step

- Chris (or any designer/PM) gives feedback after a render pass.
- A `07-prompt-review.md` audit produced Blocking or High findings.
- The team agreed to a small tuning round at the end of a phase.

Do **not** use this step for:
- The first creative judgement on a new style (still in `04-style-from-references.md` territory).
- A scenario-shape change (chapters added/removed) → `03-scenario-define.md`.

## Feedback classification

Every feedback comment falls into one of five categories. Picking the right category drives the rest of the patch chain.

### 1 · Pure delete

> "Remove the 'END' text at the bottom of Festive Editorial." (R-93 #28 A2)
> "Drop the border-top under Typographic Field." (R-93 #28 A3)

**Patch site:** renderer (delete the rendering branch) + template (delete the prose that described it) + Slot (no change unless the Slot declared the deleted element).

**Verify:** `mcp__Claude_Preview__preview_eval document.querySelectorAll('.<deleted>').length === 0`.

### 2 · Wording / phrasing alignment

> "The Design Prompt says 'GoldenHairline' but the renderer renders a plain `<hr>`." (R-93 #31 D3 case)
> "Chris said the ornament name should be 'CrimsonBar' not 'crimson-vertical-accent'."

**Patch site:** template (most common — template prose drifts from rendered name) and/or Slot (if the Slot field name itself is misleading). Renderer often unchanged; produced md regenerated.

**Verify:** grep the produced md for the new name; grep the renderer for the data-attribute or class name; both match.

### 3 · Token value change

> "Festive Royal chart_ramp greens are too green at chart-3. Shift the hue toward amber." (R-93 #29 B1)
> "Hero shader colorFront too dark — text unreadable." (R-83 #8)

**Patch site:** Slot (single source of truth for tokens). Then re-inject (so the produced md picks up the new value if it is interpolated) and re-render. Template and renderer often unchanged.

**Verify:** renderer DOM eval `getComputedStyle(el).color` matches the new OKLCH; the affected component looks right in side-by-side audit.

### 4 · Schema extension

> "Festive Royal needs a per-step hue override on chart_ramp because OKLCH single-hue ramp drifts into green." (R-93 #29 B1)
> "Need a new `golden_hairline` divider field on the Slot." (R-94 Stage 6)

**Patch site:** Slot schema (add the optional field), Slot (add the value for the affected style — leave others null), template (read the new field with `{{#if}}` wrapper to stay backward-compatible), renderer (render the new field). Then re-inject all styles to confirm none regress.

**Verify:** schema spec updated; `python3 scripts/inject.py --selftest` passes for all styles; renderer shows the new ornament on the affected style only.

### 5 · Template branch change

> "Editorial template says `font-extrabold (800)` for Hero numbers but R-93 #29 set weight_ceiling to 500 — template branch is now contradictory." (R-95 #41)
> "Add a new per-pack branch for festive-royal Chapter Opener layout."

**Patch site:** template (rewrite the branch). Re-inject affected styles. Renderer often unchanged unless the template now references a renderer attribute that did not exist.

**Verify:** grep the produced md for the old language (should return 0) and the new language (should return > 0); cross-style audit to confirm no neighbour leaked.

## Decision: which patch site changes?

```
Is the change about a value (number, color, OKLCH, font-size)?
  → Slot. Re-inject affected style(s). Re-render.

Is the change about wording (an ornament name, a label, a description)?
  → Template (prose drift) and/or Slot (field name). Re-inject. Re-render.

Is the change about something rendered that the Slot does not capture?
  → Schema extension. Add optional field. Update Slot, template, renderer.

Is the change about a per-pack branch contradiction or addition?
  → Template branch. Re-inject affected styles. Cross-style audit.

Is the change a pure delete?
  → Renderer + template (and Slot if it declared the element).
```

## The full sync chain

Once you have the patch site, run the **sync chain** (R-84 #11 + R-85 #14 — repeated drift was the example project's most-recurring class of bug):

1. Edit the patch site.
2. **If renderer changed inline DATA**: sync the same change to the Slot. Drift between inline and external Slot is the most common drift class.
3. Re-inject the affected style(s): `python3 scripts/inject.py --slot <slot> --template <tpl> --out <new versioned md>`.
4. Promote the previous produced md to `src/prompts-previous/<old file>.md`.
5. Bump the Slot or template `version` if the change was meaningful (not a typo fix).
6. Update Round-Log §3 version snapshot.
7. Run the three reviews from `07-prompt-review.md` (three-way sync, anti-slop greps, line count).
8. Open the renderer and look — DOM verify with `mcp__Claude_Preview__preview_eval` if there is any doubt.
9. Cross-style click-through: did the patch leak to neighbours?
10. Append Round-Log §2 entry: symptom → root cause → patch sites → verify proof → principle if abstractable.

Skipping any of these is the source of most re-work. Step 2 is the single most-missed step; step 9 is the second.

## Worked example: R-93 #29 B1 (chart_ramp green→amber)

1. **Feedback:** "Festive Royal chart-3 is too green."
2. **Classify:** category 3 (token value) — but value alone (`brand_hue` shift) won't work because OKLCH single-hue ramp drifts into green at L 0.40 / hue 80. Escalates to category 4 (schema extension).
3. **Patch sites:**
   - Slot schema: `chart_ramp` items get optional `H` field.
   - Slot file: `festive-royal-crimson.slot.json` gets `H: 75, 55, 40, 25` (gold→amber→orange→red-orange) per step. Other styles' chart_ramp items leave `H` null.
   - Template: read `H ?? brand_hue` per chart step.
   - Renderer: same fallback logic in `lc(v, v.H ?? bh)`.
4. **Sync chain:** edit all four; re-inject Festive Royal v0.2 → v0.3; promote v0.2 to prompts-previous; bump Slot to v0.3; Round-Log §3 update.
5. **Verify:** `preview_eval` `[2,3,4,5].map(i => document.querySelector('[data-festive-royal] .recharts-bar:nth-of-type(' + i + ')').getAttribute('fill'))` returns 4 OKLCH strings, hue progressing 75/55/40/25.
6. **Cross-style:** click through Warm/Theatre/Cool/Swiss/Festive-Editorial — chart_ramp unchanged (the `?? brand_hue` fallback worked).
7. **Round-Log §2** R-93 #29 B1 entry; §3 chart_ramp schema extension noted.
8. **Principle:** "Schema evolves only where used." Generalised in §1 originally; restated in `99-principles.md` Principle 13 (if added).

## `manual_override` — when to bypass the chain

Sometimes feedback is "delete this paragraph from the produced md" and the change is too small to migrate back to the template (or the template version cannot be bumped right now). The escape valve:

1. Hand-edit the produced md.
2. Add frontmatter `manual_override: true` + `manual_override_reason: "<round> <one-line reason>"` + `manual_override_date`.
3. Next re-inject will warn (or skip) on the file. Cowork must consciously decide to overwrite (= migrate the trim back to the template now) or preserve (= update the trim against the new inject output).

Avoid the override for anything beyond pure-deletion trim. Semantic changes belong in the template.

## When sub-agents help

Iteration is often Cowork-direct (one or two sites, tight coupling). Sub-agents earn their keep when:

- The patch touches 5+ files and the diffs are mechanical (sync the same change across all six styles' renderer inline DATA).
- The audit is large (`07-prompt-review.md` cross-style sweep) and the work is grep + classify.

When dispatching, the prompt must include the sync chain steps explicitly. See `02-roles.md` §How to write a sub-agent prompt. R-91 #25 missed mirroring `flex-direction: column` across packs; the counter-prompt for similar future work is "list every CSS rule in pack X's per-pack block and confirm each is mirrored to pack Y" (also in `02-roles.md`).

## Definition of done

- Patch landed at the right site (Slot / template / renderer / produced md trim).
- Sync chain ran end-to-end (inject → promote previous → version bump → snapshot).
- Three-way sync verifies clean for the patched style(s).
- Cross-style click-through shows no neighbour regression.
- Round-Log §2 has the entry; §3 reflects any version bumps; §1 has any new principle if abstractable.

## Pitfalls

- **Classify wrong → patch wrong site.** A wording feedback patched as a token change leaves the wording bug unfixed and adds a new value bug. Read the feedback twice.
- **Skip step 2 of the sync chain.** Renderer inline DATA drift caused R-83, R-84, R-85, R-90 issues. Every renderer inline change pairs with a Slot sync.
- **Patch in the produced md without `manual_override`.** Hours of work vanish on next re-inject.
- **No cross-style audit after a per-pack patch.** Neighbours quietly carry the same regression for weeks until someone notices.
- **Feedback round without a Round-Log entry.** The project's memory is what makes it scale across months. No entry = the lesson is local to your head.
- **Auto-escalate every value tweak to a schema extension.** Sometimes a value tweak is just a value tweak (R-83 colorFront change). Reach for category 4 only when category 3 demonstrably cannot solve it (R-93 #29 chart_ramp).
- **Sub-agent for a 30-minute Cowork-direct patch.** Dispatch overhead is real. Below a 1-hour threshold, do it yourself.

## Sync chain checklist (compact)

Use this as a print-out / mental tick-list at the end of every iteration round. Each item is a known regression source from the example project's Round-Log. Missing any one of these has caused at least one round of rework.

- [ ] **Step 1.** Patch site identified (one of Slot / template / renderer / produced md / schema).
- [ ] **Step 2.** Inline renderer data synced to external Slot. (Most-missed step. R-83, R-84, R-85, R-90 all stumbled here.)
- [ ] **Step 3.** Re-inject ran cleanly: `python3 scripts/inject.py --slot <slot> --template <tpl> --out <new versioned md>` — zero unrendered tokens.
- [ ] **Step 4.** Previous produced md promoted to `prompts-previous/` (so the renderer's diff view works next round).
- [ ] **Step 5.** Slot or template `version` bumped (Slot vX.Y → vX.Y+1 or vX+1.0 for breaking changes).
- [ ] **Step 6.** Round-Log §3 version snapshot updated.
- [ ] **Step 7.** Three-way sync audit passes (Prompt ↔ Slot ↔ rendered DOM) for the patched style.
- [ ] **Step 8.** Anti-slop greps pass (`grep -nE 'filled.*border|fixed.*shader|extrabold.*8[0-9][0-9]' <files>` returns 0).
- [ ] **Step 9.** Line count: produced md ≤ 620 lines (Principle 11).
- [ ] **Step 10.** Cross-style click-through: every other style still renders correctly (no neighbour regression).
- [ ] **Step 11.** Round-Log §2 entry written: symptom → root cause → patch sites → verify proof → principle.

Steps 2 and 10 are the two most-skipped. Steps 7 and 11 are the two most-skimmed.

## Common iteration anti-patterns

A taxonomy of how iteration rounds fail. Each one comes from a specific round in the example project; recognising the shape early saves a round.

**1 · "I patched the pattern — the rest will follow."** No. Each render branch is a separate code path. R-90 #24: festive-royal got the new chapter opener in chapter 1, chapters 2–7 still rendered the default. Enumerate every branch.

**2 · "Sub-agent reported PASS, I'll move on."** No. Cowork's independent verify is non-negotiable. R-87 #18, R-90 #24, R-94 #35 — three rounds, same lesson. See `case-studies.md` Case 4.

**3 · "I edited the produced md by hand because the template is messy."** Dangerous. Hand-edits without `manual_override` frontmatter vanish on next re-inject. If the edit is small and pure-delete, use `manual_override`. If the edit is semantic, push it into the template instead.

**4 · "The CSS pattern in pack X is obvious — pack Y will inherit it."** No. CSS specificity is unforgiving. R-91 #25: festive-editorial inherited `display: flex` from default but missed pack X's `flex-direction: column` override → titles wrapped awkwardly. See `case-studies.md` Case 6.

**5 · "Slot changed, no need to grep template — the injector handles it."** Sometimes. If the change is a *value* the template interpolates (`{{slot.color}}`), yes. If the change is a *constraint* the template duplicates as prose ("weight ≤ 500"), no — grep the template for the old constraint and update it manually. R-95 #41: `weight_ceiling: 500` Slot, template still said `font-extrabold (800)`. See `case-studies.md` Case 9.

**6 · "Fix one alignment, ship."** Multi-dimensional. R-86 #15: fixed line-through-dot, broke dot-vs-title. After any layout fix, screenshot adjacent alignment relations.

**7 · "Token is `--primary`, so it's the brand colour, so red looks right here."** Brand tokens have *semantic* roles (focal numeral, default delta) not *decorative* meanings (red / gold / blue). R-92 #26 issue 2: `--primary` in festive-royal is gold; the Cinnabar Imprint needed a hard-coded red.

**8 · "The wrapper hides the bug — done."** No. R-83 #8: a `backdrop-filter blur` overlay was proposed to mask a too-loud Hero shader. Real fix: tune the shader's `colorFront`. Every wrapper is debt (Principle 1, Principle 8).

**9 · "Sub-agent suggested it, I'll forward it."** No. Cowork is the principle gate (Principle 13). Sub-agents bring red-line patterns from their training — few-shot examples, mission statements, metadata. Pass them through the principles before they land.

**10 · "Demo paths in general docs are fine, readers will figure it out."** They won't. R-97 / Case 11: demo paths leak from example into general Skill prose, then break for every other project using the Skill. Use placeholders in general docs; concrete paths only in the example project.

Each anti-pattern has at least one specific case in `case-studies.md`. Read both together — the principle is in `99-principles.md`, the shape is in `case-studies.md`, the chain is here.
