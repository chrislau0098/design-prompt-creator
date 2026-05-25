# 04 · Extract a Style from Reference Images

> Reference images + a short Chris-style brief → one Slot JSON that the renderer and the injector both consume. This is the most aesthetic-judgement-heavy step in the loop — dispatch to Opus, verify with the renderer.

## When to use this step

- A designer hands you 3–6 reference images and a one-paragraph brief ("red, festive, ceremonial, gold accents, serif").
- You want a new variant of an existing pack (Style A festive-royal already exists, you want Style B festive-editorial with the opposite tonal direction).
- An existing Slot needs a substantial refresh because reference images updated (e.g. R-93 chart_ramp green→amber correction is *not* this step — that is `08-iterate.md`).

Do **not** use this step for:
- Tweaking an existing Slot value (color too dark, weight too heavy) → `08-iterate.md`.
- Changing the page skeleton → `03-scenario-define.md`.

## What a Slot is

A Slot JSON is the **single source of truth** for one style. It declares:

1. **`style_meta`** — handle, version, mode (light / dark / chromatic), brand_hue, ground-truth image paths, mood adjectives, proposition (one paragraph), `decorative_pack` enum, `focal_numeral_strategy` enum.
2. **`atomic`** — color tokens (OKLCH triples or LC pairs), typography stacks + scale + tracking + feature settings, spacing scale, radius scale, weight ceiling.
3. **`molecular`** — composition rules that combine atomic tokens (e.g. KPI card padding × radius × bg surface choice).
4. **`hero_shader`** — paper-shaders config (Dithering / GodRays / GrainGradient / MeshGradient) + props.
5. **`dividers`, `ornaments`** — per-pack signature elements (SealStamp, GoldenHairline, ChapterNumeralLarge, etc.).

The full schema spec is in `examples/vibe-view-campaign-report/slot-schema-v0.md`. Read it once end-to-end before extracting your first new style.

Six worked examples live at `examples/vibe-view-campaign-report/slot-examples/`:
- `warm-v1.0.1.slot.json` — editorial pack, light mode, sans, ember accent
- `theatre-v6.7.1.slot.json` — theatrical pack, dark mode, sans, copper accent
- `cool-v0.5.1.slot.json` — instrumental pack, dark mode, sans, blue accent
- `swiss-systematic-blue.slot.json` — systematic pack, light mode, sans 700 caps, cobalt
- `festive-royal-crimson.slot.json` — festive-royal pack, **chromatic** mode, **serif**, gold on crimson
- `festive-editorial-crimson.slot.json` — festive-editorial pack, light mode, sans 800, crimson on ivory

Open both festive Slots side-by-side when designing a new style — they show how the schema handles the two extremes (chromatic+serif and light+sans-800).

## Steps

### 1. Stage the reference images

Group them under `_attachments/style-mood-references/<style-handle>/`. 3–6 images is the right amount: enough variety to triangulate a style, few enough that the agent does not lose the thread.

Each image should be a *whole page* (or a substantial fragment), not a single tile. The weak model is producing pages; the references must show what a page looks like.

Record the absolute paths — Slot stores them in `style_meta.ground_truth_images` for traceability.

### 2. Write the Chris-style brief

One paragraph (max 4–5 sentences). Tonal direction in adjectives. **No values.** Examples that work:

> "Red, festive, ceremonial, Chinese new year feeling. Gold accents on deep crimson. Serif display. Long-scroll. Very particular about every detail."

> "Brutalist editorial red. Western contemporary, not Chinese. Big bold sans on ivory. Display weight 800 in all caps. Hairline dividers, no decoration."

Examples that do **not** work:
- "Use `#A2202B` for primary." → that is a Slot value, not a brief.
- "Mood like Apple but red." → too vague; the agent will invent.
- A 600-word essay. → if the brief is that long, you are designing the Slot in the brief itself.

### 3. Dispatch an Opus sub-agent for extraction

This step is taste-bound — Opus. Sonnet will produce a syntactically valid Slot that misses the mood by a mile.

The sub-agent prompt structure (see `02-roles.md` §How to write a sub-agent prompt):

```
You are sub-agent (Opus, style extraction).
Task: extract a new Slot JSON for handle <slug>.

Inputs:
- Brief: <paragraph>
- Reference images (read with vision):
  * /abs/path/img1.jpg
  * /abs/path/img2.jpg
  * /abs/path/img3.jpg
- Schema spec: /abs/path/examples/.../slot-schema-v0.md
- Nearest sibling style (start from this): /abs/path/slot-examples/<closest>.slot.json
- Two existing Slots to triangulate against: <list>

Output:
- /abs/path/src/data/<slug>.slot.json (full Slot, schema-valid)
- A 200-word `evidence_chain` field in style_meta justifying every major
  choice (brand_hue, mode, decorative_pack, hero_shader pick, typeface_class,
  primary_focal_strategy) back to a specific image.

Discipline:
- mood_adjectives are 4-5 short adjectives, not a sentence.
- ground_truth_signature is one line, English.
- Do not invent fields that are not in the schema spec. Use null where a
  field is optional and absent.
- Round all OKLCH values to 3 decimal places.

Verify proof:
- python3 scripts/inject.py --slot <produced slot> --template templates/prompt-template.md --out /tmp/<slug>.md
- wc -l /tmp/<slug>.md
- grep -c '{{' /tmp/<slug>.md  (must be 0 — no unrendered tokens)
- Report which schema fields you used null for and why.
```

### 4. Verify the Slot renders cleanly

The injector is the first gate. If `python3 scripts/inject.py --slot src/data/<slug>.slot.json --template templates/prompt-template.md --out /tmp/<slug>.md` raises `KeyError`, the Slot is missing a field the template requires. Fix in this order:

1. Add the missing Slot field (if it is genuinely required for this style).
2. Wrap the template usage in `{{#if path}}…{{/if}}` (if the field is genuinely optional and this style does not use it).
3. Never silently change the template to read from a different field — that breaks the other styles.

Then check the produced md has 0 unrendered `{{ }}` tokens:

```sh
grep -nP '\{\{[^}]+\}\}' /tmp/<slug>.md | grep -v 'once: true' | grep -v 'margin:'
```

(The grep excludes JSX inline object literals, which the injector deliberately passes through.)

### 5. Add the Slot to the renderer

Copy or symlink to `renderer/src/data/<slug>.slot.json`. The renderer auto-discovers `src/data/*.slot.json`. Open `http://localhost:5173?style=<slug>&view=design-system` and `?view=report` — both should render without console errors and the visual should match the brief.

### 6. First aesthetic judgement pass

Open the renderer side-by-side with the reference images. Ask:

- Does Hero shader look like the references' opening field? (Often the single most-impactful judgement.)
- Are the chart colors in a single hue family, not pastel-rainbow?
- Are font weights consistent with the brief? (festive-royal serif 700, festive-editorial sans 800.)
- Do the dividers / chapter markers match the pack's signature elements?

If the answer is "close but…", capture the gap as a Round-Log §2 entry and iterate via `08-iterate.md`. The Slot does not need to be perfect at extraction — it needs to be in the right neighbourhood.

### 7. Lock the version and commit

```sh
git add src/data/<slug>.slot.json _attachments/style-mood-references/<slug>/
git commit -m "feat: extract <slug> Slot v0.1 from references"
```

In Round-Log §3 add a row: `<handle>: src/data/<slug>.slot.json v0.1 (round NN)`.

## Definition of done

- Slot file exists at `src/data/<slug>.slot.json` and is schema-valid.
- Reference images live under `_attachments/style-mood-references/<slug>/`.
- `python3 scripts/inject.py` renders the Slot against the template with 0 unrendered tokens.
- Renderer shows the Slot under Design System + Report Example views.
- Round-Log §2 has an entry; §3 has the version snapshot row.
- The result is *in the right neighbourhood* of the references (not perfect — that is iteration's job).

## Pitfalls

- **Sonnet sub-agent for style extraction.** Will produce a valid Slot that misses the mood. Always Opus.
- **Brief contains values.** A brief is direction; a Slot is values. Mixing them removes the agent's leverage.
- **No `evidence_chain`.** Without a written justification, six rounds later nobody remembers why brand_hue is 25 and not 28. Always require the sub-agent to write it.
- **Picking the wrong nearest-sibling.** Starting from a sibling Slot is fine; starting from one whose mood is opposite means the agent's diff is enormous and the result inherits the wrong defaults. Pick the closest neighbour, not the loudest.
- **Inventing schema fields.** The schema is closed. If a style "needs" a new field, propose a schema extension first (with `_comment` documenting the new field and a Round-Log entry), then add it to the schema, then to one Slot. Do not add ad-hoc fields scattered across Slots.
- **Skipping the renderer judgement pass.** A schema-valid Slot can still produce a page that does not look like the references. The Slot is the spec; the renderer is the truth. Always look.
- **Re-extracting from references when you should be iterating.** If the existing Slot is 80% right, do not throw it out. Open `08-iterate.md` and patch the specific tokens that are off.
