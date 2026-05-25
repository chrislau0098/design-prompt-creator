# 05 · Generate the Design Prompt md

> Slot + template → final Design Prompt md, via `scripts/inject.py`. The output is the artifact the weak model (doubao-seed-code 2.0, GPT-OSS-20B, etc.) actually reads. Get this right and the rest of the pipeline coasts; get it wrong and every iteration fights you.

## When to use this step

- After `04-style-from-references.md` produced a new Slot — render its first Design Prompt.
- After `03-scenario-define.md` produced a new scenario template — render each existing Slot against it.
- After `08-iterate.md` patched a Slot, the template, or both — re-render every affected style.

Do **not** use this step for:
- Editing the produced md by hand (it will be overwritten on the next inject — patch the Slot or template instead). The one exception is `manual_override` for trim, covered below.

## The injector contract

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

`cond` supports: truthy (`path`), negation (`!path`), equality (`path == "lit"`), inequality (`path != "lit"`). String literals must be double-quoted. **No `&&` / `||`.** Nest blocks instead — see the festive-royal template branches in `templates/prompt-template.md` for the nesting pattern.

Behaviours worth knowing:
- JSON parsed with `parse_float=str` — `0.180` stays `0.180`, not `0.18`. Slot files preserve their source precision.
- String arrays render as comma-separated CSS font lists; CSS generic keywords (`sans-serif`, `monospace`, `-apple-system`, etc.) are emitted unquoted; everything else is single-quoted.
- Missing fields raise `KeyError: <path>` — there is no silent fallback. This is intentional: silent fallbacks make the produced md drift from the Slot.
- JSX inline object literals (`{{ once: true, margin: "..." }}`) are passed through unchanged because the tokenizer only treats `{{ }}` as a token when the expression looks like a path or a block tag.

## Steps

### 1. Pick the Slot and the template

The Slot is `src/data/<style-handle>.slot.json`. The template is usually:
- `scenarios/<scenario-handle>/template.md` (scenario-forked), or
- `templates/prompt-template.md` (the agnostic base, when the scenario does not fork).

If both exist, the scenario-specific template wins.

### 2. Run inject

```sh
python3 scripts/inject.py \
  --slot      src/data/festive-royal-crimson.slot.json \
  --template  templates/prompt-template.md \
  --out       src/prompts/festive-royal-crimson-Design-Prompt-v0.3.md
```

The output filename should embed the Slot version and (optionally) the scenario handle. Versioned filenames make Round-Log §3 snapshot easy and let the renderer's diff view compare against the previous version under `src/prompts-previous/`.

### 3. Verify the produced md

Three checks, in order:

**A · 0 unrendered tokens**

```sh
grep -nP '\{\{[^}]+\}\}' src/prompts/<file>.md
```

If anything matches that is not a JSX inline object literal (something with `:` inside), the template references a Slot path that does not exist. Fix the Slot or wrap the template usage in `{{#if}}…{{/if}}`. Never silently change the field path.

**B · line count ≤ 620**

```sh
wc -l src/prompts/<file>.md
```

Hard ceiling 620 (was 600 in early R-91, relaxed in R-95 #40). Above 620 = trim the template or the Slot — see `07-prompt-review.md` for the trim playbook. Below 500 = check that you have not accidentally hollowed out a per-pack conditional branch.

**C · per-pack signature integrity**

Each `decorative_pack` should leave its signature elements in the output. Grep examples (adapt the literals to your pack):

```sh
# festive-royal: SealStamp + GoldenHairline + 700-weight serif
grep -c 'SealStamp\|GoldenHairline\|font-bold' src/prompts/festive-royal-*.md

# festive-editorial: ChapterNumeralLarge + HairlineRule + 800 sans
grep -c 'ChapterNumeralLarge\|HairlineRule\|font-extrabold' src/prompts/festive-editorial-*.md
```

Counts that drop unexpectedly between versions usually mean a template trim removed a per-pack branch by accident. Re-inject the previous Slot version, diff the two outputs, and locate the regression.

### 4. Update version metadata

The renderer's Design Prompt tab reads frontmatter from the produced md:

```yaml
---
style_name: "Festive Royal · Crimson Gold"
description: "..."
template_version: v0.5.2 (R-94 Stage 6 three-way sync · ...)
---
```

The injector populates `style_name` and `description` from the Slot. `template_version` is a manual string in the template's frontmatter — bump it whenever the template changes meaningfully.

For per-prompt version + changelog (consumed by the renderer's Diff view), keep a sibling JSON or inline frontmatter that the renderer reads. The example project uses inline metadata in the renderer's `src/data/prompts/` md files with `updated_at`, `version`, and a `changelog: [{date, note}]` array — see `examples/vibe-view-campaign-report/` Round-95 #42 for the convention.

### 5. Promote the previous version

Before overwriting `src/prompts/<file>.md`, copy the existing one to `src/prompts-previous/` so the renderer's Diff view has a comparison anchor:

```sh
cp src/prompts/festive-royal-crimson-Design-Prompt-v0.2.md \
   src/prompts-previous/festive-royal-crimson-Design-Prompt-v0.2.md
```

Then run inject to produce v0.3.

### 6. Re-test the renderer

```sh
cd renderer && bun dev
# open http://localhost:5173?style=festive-royal-crimson&view=design-prompt
```

The Design Prompt tab should show the rendered md with Shiki syntax highlighting, the Copy button, the Diff vs Previous tab populated, and the Changelog accordion at the top. If the diff is empty, you forgot step 5.

### 7. Commit

```sh
git add src/prompts/<new file>.md src/prompts-previous/<old file>.md
git commit -m "feat: re-inject <style> v<N>"
```

## `manual_override` — when to hand-edit the produced md

The general rule: do not hand-edit the produced md. The exception is **trim** — when the produced md is over 620 lines and the trim is purely deletions of redundant prose (no semantics change). Example from R-95 #40: Swiss v0.7 (626 lines) → v0.8 (604) by collapsing four redundant bullets in §2 and three Recharts paragraphs in §17.

When hand-editing:

1. Add a frontmatter flag so the next inject does not silently overwrite:
   ```yaml
   manual_override: true
   manual_override_reason: "R-95 #40 trim 626→604, see Round-Log"
   manual_override_date: "2026-05-24"
   ```
2. Diff against the previous produced md and confirm only deletions (or trivial reorderings).
3. Re-run grep verify from step 3 — invariants must still pass.
4. Round-Log §2 captures the trim; §3 updates the line count.

The Cowork main agent's discipline check before accepting a `manual_override`: would a re-inject after the next Slot change destroy the trim? If yes, the trim must be migrated *into* the template (delete the redundant prose at the template level), not preserved as a one-off edit. R-95 #40 trim is acceptable because it was content-redundancy; if a future Slot change adds a new constraint, the new sentence belongs in the template and the trim stays valid below it.

## Definition of done

- `src/prompts/<file>-v<N>.md` exists with 0 unrendered tokens.
- Line count ≤ 620.
- Per-pack signature greps return non-zero counts in the expected places.
- Previous version is in `src/prompts-previous/` so Diff works.
- Renderer Design Prompt tab loads cleanly.
- Round-Log §2 has the re-inject entry; §3 updates the version snapshot.

## Pitfalls

- **`KeyError: path.to.field` on inject.** The Slot is missing a required field. Either add it (if needed) or wrap the template usage in `{{#if}}`. Do not silently change the template to read a different field — other Slots break.
- **Smart quotes in template literals.** `'"Cormorant Garamond"'` with U+201D curly quotes breaks JS at runtime. The example project hit this in R-90 #24 fontFamily. Grep `grep -nP '[‘’“”]' templates/` after any edit; must be 0.
- **Re-injecting all six Slots when you only changed one Slot.** Wastes time and pollutes diff history. Re-inject only the affected style(s). If the template changed, re-inject all.
- **Skipping the `prompts-previous/` copy.** The renderer's Diff view goes blank. Worse, you lose the anchor for trim verification on the next round.
- **Hand-editing the produced md without `manual_override`.** Next inject silently overwrites. Hours of trim work disappear without a trace.
- **Trim that changes semantics.** Hand-edit may delete redundant prose only. If the trim removes a constraint ("Don't apply weight above 500"), you have weakened the prompt — that change belongs in the template + Slot, with a Round-Log entry.
