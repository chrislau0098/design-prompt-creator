# 07 · Generate the Design Prompt md

> The Design Prompt is the artifact the weak model (doubao-seed-code 2.0, GPT-OSS-20B, etc.) reads to ship pages. R-101 makes Prompt generation a **two-step** process: a Slot+Template `inject` produces an initial draft early in the project (so the renderer's Design Prompt tab has *something* to display), and an Opus-led **auto-extract** from the Chris-confirmed Design Example produces the frozen, ship-ready md. Step A is bootstrap; Step B is the real Prompt.

## Where this step lives in the new workflow

```
04 style-from-references → Slot JSON drafted
   ↓
[Step A · here] Slot + Template → inject → draft Design Prompt md
   ↓
05 design-example-render → iframe renders Example from Slot
   ↓
08 iterate (loop) → Slot tweaks → re-render Example (Prompt not regenerated)
   ↓
Chris confirms Example is OK  ← HARD GATE
   ↓
[Step B · here] Cowork dispatches Opus → auto-extract Prompt from
                confirmed Slot + Example → final Design Prompt md
   ↓
06 prompt-review → three-way Sync (System ⊆ Prompt), anti-slop, line economy
```

Step A is the **only** Prompt generation event before Chris confirms. Iteration rounds in step 08 do **not** regenerate the Prompt — they tweak the Slot, re-render the Example, and accumulate towards confirmation. Step B fires exactly once per confirmed Example version.

## When to use this step

- **Step A** — right after `04-style-from-references.md` produced a new Slot. Inject once to give the renderer something to show in the Design Prompt tab. The draft is **not** for the weak model yet — it is scaffolding so the Design Prompt tab is not empty during iteration.
- **Step B** — after `05-design-example-render.md` step 9 (Chris confirms the Example). Cowork dispatches Opus to extract the final Prompt from the confirmed Slot + Example. This is the ship-ready md.
- After `03-scenario-define.md` produced a new scenario template — re-inject Step A for each existing Slot. If any of those Slots were already in Chris-confirmed state for the old template, they need Chris re-confirmation against the new template before Step B re-fires.
- After `08-iterate.md` patched a Slot post-confirmation — back to Example render, back to Chris gate, back to Step B.

Do **not** use this step for:
- Hand-editing either the draft or the auto-extracted md (it will be overwritten on the next Step A inject or Step B extract — patch the Slot, the Example, or the template instead). The one exception is `manual_override` for trim, covered below.
- Generating the Prompt before Chris confirms the Example. The whole point of R-101 is that the Prompt is a derivative, not a parallel artifact.

---

## Step A · Slot + Template → draft Prompt (inject)

The initial draft. Carryover from the pre-R-101 workflow with one change: this is now **bootstrap scaffolding**, not the final artifact. The draft fills the renderer's Design Prompt tab during iteration so the tab is not empty, and gives Step B a template-shaped starting point if Opus needs one.

### A.1 The injector contract

`scripts/inject.py` is a 600-line Python 3.10+ script with zero dependencies. It parses a small Handlebars-style template language over a JSON Slot.

```sh
python3 scripts/inject.py \
  --slot      <path/to/slot.json> \
  --template  <path/to/template.md> \
  --out       <path/to/output.md>
  [--verbose]
```

Self-test: `python3 scripts/inject.py --selftest` renders the three reference Slots against `templates/prompt-template.md` and asserts there are zero unrendered tokens. Run this before trusting the script after any edit.

Template syntax (full grammar in `scripts/inject.README.md`):

| Form | Behaviour |
|---|---|
| `{{path.to.field}}` | Field replace, dot notation. `.0` `.1` for array indices. |
| `{{#if cond}}…{{/if}}` | Conditional block. |
| `{{#unless cond}}…{{/unless}}` | Inverse conditional. |
| `{{#each path}}…{{this}}…{{/each}}` | Iteration. Inside: `{{this}}`, `@last`, `@first`, `@index`. |

`cond` supports: truthy (`path`), negation (`!path`), equality (`path == "lit"`), inequality (`path != "lit"`). String literals must be double-quoted. **No `&&` / `||`.** Nest blocks instead.

Behaviours worth knowing:
- JSON parsed with `parse_float=str` — `0.180` stays `0.180`, not `0.18`. Slot files preserve their source precision.
- String arrays render as comma-separated CSS font lists; CSS generic keywords (`sans-serif`, `monospace`, `-apple-system`, etc.) are emitted unquoted; everything else is single-quoted.
- Missing fields raise `KeyError: <path>` — there is no silent fallback. Silent fallbacks make the produced md drift from the Slot.
- JSX inline object literals (`{{ once: true, margin: "..." }}`) are passed through unchanged because the tokenizer only treats `{{ }}` as a token when the expression looks like a path or a block tag.

### A.2 Run inject

```sh
python3 scripts/inject.py \
  --slot      src/data/festive-royal-crimson.slot.json \
  --template  templates/prompt-template.md \
  --out       src/prompts/festive-royal-crimson-Design-Prompt-v0.1-draft.md
```

The draft filename should embed the Slot version and the `-draft` suffix so it does not get confused with a Step B output.

### A.3 Verify the draft

Three quick checks:

```sh
# 0 unrendered tokens
grep -nP '\{\{[^}]+\}\}' src/prompts/<file>-draft.md

# line count (the draft can be a touch over 620 — Step B will tighten it)
wc -l src/prompts/<file>-draft.md

# per-pack signature
grep -c 'SealStamp\|GoldenHairline\|HairlineRule' src/prompts/<file>-draft.md
```

The draft does not need to pass the line-economy ceiling — that is Step B's job. The draft just needs to be valid (zero unrendered tokens) and contain enough of the Slot's signature for the Design Prompt tab to show something coherent.

---

## Step B · Auto-extract Prompt from confirmed Example

The real artifact. Cowork dispatches an Opus sub-agent that reads (a) the confirmed Slot, (b) the scenario's PATTERN.md + components.md, and (c) the confirmed Example (URL + screenshots if Cowork captured them during step 05). The sub-agent produces a Prompt md whose every sentence describes something the Example actually renders.

### B.1 When to fire

Step B fires when **all three** are true:

1. Chris has explicitly confirmed the Example for a specific Slot version (e.g. "OK on festive-royal v0.3").
2. The confirmation is recorded in Round-Log §2 with the Slot version.
3. Cowork has the dispatch context ready (Slot path, PATTERN path, components path, Example URL, optional screenshot paths).

If any of these is missing, do **not** fire. A missed Step A draft is recoverable; an early Step B extract bakes wrong choices into the frozen artifact.

### B.2 The dispatch

Cowork dispatches Opus. The sub-agent prompt is short (under 50 lines) and is the only thing Cowork has to author — the agent does the prose-writing work.

**Sub-agent prompt stub** (Cowork copies this, fills the placeholders, and dispatches):

```
You are an Opus sub-agent. Extract a Design Prompt md from a Chris-confirmed
Design Example.

Inputs (all absolute paths):
- Slot:        <SLOT_PATH>
- Scenario:    <SCENARIO_PATH>/PATTERN.md, <SCENARIO_PATH>/components.md
- Example:     <EXAMPLE_URL>
- Screenshots: <SCREENSHOT_PATHS or "none">
- Template ref (anchor only, do NOT inline its prose): <TEMPLATE_PATH>
- Output:      <OUT_PATH>

Constraints (all hard):
1. Every sentence in the output describes an element that the Example
   actually renders. If the Slot declares a token the Example does not
   surface, the Prompt does NOT name it. (Three-Way Sync: System ⊆ Prompt
   ⊆ Slot SoT.)
2. Output ≤ 620 lines. Aim for 500-580 lines. Every word must constrain.
3. No metadata blocks, no inline source URLs, no "Inspired by", no
   "Last updated", no emoji checklists, no few-shot React/CSS snippets.
   Prose only. (Anti-slop A7 + Principle 11.)
4. Follow PATTERN.md's section order. Use components.md as the closed set of
   allowed components — do not invent new ones.
5. Preserve Slot precision (OKLCH values, font weights) verbatim. Do not
   round, do not paraphrase numbers.
6. Emit YAML frontmatter at the top with: style_name, description,
   slot_version, template_version, extracted_from_example: <EXAMPLE_URL>,
   extracted_at: <ISO date>.

Verify proof to return:
- wc -l <OUT_PATH> (expect ≤ 620)
- grep -c per-pack signature elements (counts you observed in the Example)
- Three-line summary of what the Prompt says about Hero, Charts, Ornaments

Write <OUT_PATH>. Report the verify proof. Do not edit any other file.
```

The placeholders Cowork fills:
- `<SLOT_PATH>` — `src/data/<handle>.slot.json` at the confirmed version.
- `<SCENARIO_PATH>` — `scenarios/<scenario>/`.
- `<EXAMPLE_URL>` — the renderer iframe URL Chris confirmed against (with `?style=<handle>` and `?device=web` or `?device=mobile`, whichever Chris confirmed).
- `<SCREENSHOT_PATHS>` — Cowork-captured screenshots from step 05, or `"none"` if Cowork is dispatching against a live renderer the sub-agent can hit via preview tools.
- `<TEMPLATE_PATH>` — `templates/prompt-template.md` or the scenario fork. The sub-agent reads it for shape but is forbidden from inlining its prose verbatim.
- `<OUT_PATH>` — `src/prompts/<handle>-Design-Prompt-v<N>.md` with the confirmed Slot version embedded in the filename.

### B.3 Chris confirms the final Prompt

After Opus returns the md, Chris reads it. If anything misrepresents the Example — names an ornament that does not render, claims a weight the Example does not show, invents a component — Chris flags it and Cowork either re-dispatches Opus with a delta prompt ("regenerate, but the chart palette is single-hue, not multi-hue") or hand-patches the small drift with a `manual_override` frontmatter flag.

Only after Chris's **second** confirmation (Prompt OK after Example OK) does the md get committed. Until then it lives at `src/prompts/<file>.md` but is treated as candidate.

### B.4 Promote the previous version

Before overwriting `src/prompts/<file>.md`, copy the existing one to `src/prompts-previous/`:

```sh
cp src/prompts/festive-royal-crimson-Design-Prompt-v0.2.md \
   src/prompts-previous/festive-royal-crimson-Design-Prompt-v0.2.md
```

Then commit the new v0.3 alongside the promoted v0.2.

### B.5 Commit

```sh
git add src/prompts/<new file>.md src/prompts-previous/<old file>.md
git commit -m "feat: auto-extract <style> v<N> Prompt from confirmed Example"
```

Round-Log §2 records the confirmed Example version + the extracted Prompt version. §3 updates the version snapshot.

---

## `manual_override` — when to hand-edit the Step B output

The general rule: do not hand-edit the auto-extracted md. The exception is **trim** — when the produced md is over 620 lines and the trim is purely deletions of redundant prose (no semantics change). Example from R-95 #40: Swiss v0.7 (626 lines) → v0.8 (604) by collapsing four redundant bullets in §2 and three Recharts paragraphs in §17.

When hand-editing:

1. Add a frontmatter flag so the next Step B extract does not silently overwrite:
   ```yaml
   manual_override: true
   manual_override_reason: "R-95 #40 trim 626→604, see Round-Log"
   manual_override_date: "2026-05-24"
   ```
2. Diff against the previous produced md and confirm only deletions (or trivial reorderings).
3. Re-run grep verify from Step B.6 — invariants must still pass.
4. Round-Log §2 captures the trim; §3 updates the line count.

Cowork's discipline check before accepting a `manual_override`: would a re-extract after the next Slot change destroy the trim? If yes, the trim must be migrated *into* the template (Step A side) or the auto-extract sub-agent prompt (Step B side), not preserved as a one-off edit. Semantic changes belong upstream.

---

## Definition of done

**Step A draft:**
- `src/prompts/<file>-draft.md` exists with 0 unrendered tokens.
- Renderer Design Prompt tab loads the draft without error.
- Round-Log §3 notes the draft version (so iteration rounds can reference it).

**Step B final:**
- `src/prompts/<file>-v<N>.md` exists, extracted from the confirmed Example.
- Line count ≤ 620 (Principle 11).
- Three-Way Sync passes (`06-prompt-review.md`): System ⊆ Prompt ⊆ Slot SoT.
- Per-pack signature greps return non-zero counts in expected places.
- Previous version is in `src/prompts-previous/` so Diff works.
- Chris has confirmed both the Example **and** the extracted Prompt.
- Round-Log §2 has the extract entry with both confirmation timestamps; §3 updates the version snapshot.

## Frontmatter `description` format (HARD)

Every produced Prompt md carries a single-line YAML `description` in its frontmatter. This field is what downstream routers / catalogs / orchestrators read to decide whether to load THIS prompt vs another style. Keep it user-facing prose (not engineering jargon), and follow this three-part structure:

1. **Visual language thesis** — one sentence opening with the style's core posture (克制 / 浓重 / 仪式感 / 工程感 / 等). List 3–5 grounded constraints (信息层级 / 留白 / 节奏 / 可读性 / 字重 / 等). Close with an integral observation phrased as three adjectives (例如 "干净、现代、专业"). No technical terms (no "OKLCH", no "dial", no "STYLE_PRESETS", no "shader").
2. **Use-case catalog** — "适用于 [N 个典型场景 / 行业 / 页面类型]"。Examples: "产品介绍、品牌官网、作品集、企业展示、服务说明" for a generic web style; "年度复盘、季度战报、增长汇报、运营月报" for a report-oriented style. Aim for 4–6 concrete scenarios.
3. **Fallback / activation rule** — for "default" / 通用基座 type prompts use "在无其他专用主题匹配时，默认使用本主题". For fixed style prompts use a triggering rule like "如果用户提到了'X / Y / Z' 可以用此风格" listing the brand mood / keyword triggers.

Reference example for a default / generic web base:

> 以克制、清晰的视觉语言为基础，强调良好的信息层级、舒适的留白、统一的版式节奏与稳定的可读性，整体呈现干净、现代、专业的网页观感。适用于大多数通用网页设计场景，如产品介绍、品牌官网、作品集、企业展示、服务说明等。在无其他专用主题匹配时，默认使用本主题

Hard requirements:
- Single line (YAML scalar — no `>` or `|` block syntax)
- No 【场景通用基座】/【报告基座】etc. eyebrow prefixes — straight prose only
- No technical terms (`dial` / `STYLE_PRESETS` / `OKLCH` / `shader` / `font_family` / `lightness_shift` 等)
- No version numbers / changelog / "R-XXX 引入" metadata
- ≤ 200 Chinese characters (plus light punctuation); routes need to fit in a console / sidebar / chip
- Periods only between the three parts; final part ends without a period to keep the activation rule looking like a directive

## Pitfalls

- **Firing Step B before Chris confirms.** The whole gate exists to keep the Prompt from baking in pre-confirmation choices. If the renderer's Design Prompt tab needs content during iteration, that is what the Step A draft is for.
- **Skipping the Step A draft because "we'll just wait for Step B".** Then the Design Prompt tab is empty during iteration, the renderer's Diff view has nothing to anchor against on the first Step B fire, and the sub-agent in Step B has no shape reference to lean on.
- **Hand-editing the auto-extracted md without `manual_override`.** Next Step B fire silently overwrites. Hours of trim work disappear without a trace.
- **`KeyError: path.to.field` on Step A inject.** The Slot is missing a required field. Either add it (if needed) or wrap the template usage in `{{#if}}`. Do not silently change the template to read a different field — other Slots break.
- **Smart quotes in template literals.** `'"Cormorant Garamond"'` with U+201D curly quotes breaks JS at runtime. Grep `grep -nP '[‘’“”]' templates/` after any edit; must be 0.
- **Asking Opus to extract without screenshots when the renderer is not live.** If Cowork cannot hit the renderer URL via preview tools at dispatch time, Opus has nothing to ground against. Either start the renderer, or capture screenshots first.
- **Trim that changes semantics.** Hand-edit may delete redundant prose only. If the trim removes a constraint, the change belongs upstream (template or sub-agent prompt), not in the produced md.
- **Re-extracting all six styles when only one Slot changed.** Step B is per-style. The other five did not lose their Chris confirmation just because one was retuned. Re-extract only the style(s) whose Example was re-confirmed.
