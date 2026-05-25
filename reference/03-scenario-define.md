# 03 · Define a New Scenario

> Adding a new page type (e.g. waitlist, product catalog, product promotion) to the project. A scenario is *the page skeleton* — which chapters exist, which components the page may use, how the prompt is shaped. A scenario is style-agnostic; styles plug in via Slot.

## When to use this step

- The project has only `campaign-report` and someone wants a waitlist page.
- You are forking a scenario because the new page type differs in chapter rhythm (e.g. catalog has no Hero Monolith chapter, just a Peer Set Matrix Grid).
- An MVP scenario stub exists (`scenarios/<name>/` is empty) and you are filling it.

Do **not** use this step for:
- Adding a style to an existing scenario → `04-style-from-references.md`.
- Tweaking which chapters appear *for this report* — that is data-level (the Slot's `_comment` and the actual report content), not scenario-level.

## A scenario is three files

```
scenarios/<scenario-handle>/
├── PATTERN.md          # page skeleton: chapters, archetypes, composition treatments, dominant moves
├── components.md       # the component vocabulary the weak model is allowed to use
└── template.md         # the prompt template with {{slot.path}} placeholders
```

That is it. No code. The template is rendered by `scripts/inject.py` against a Slot JSON to produce the final Design Prompt md.

The MVP reference for what these three files look like:
- `examples/vibe-view-campaign-report/PATTERN-block-enriched-v1.md` — the Campaign Report PATTERN (12 archetypes, 9 composition treatments, dominant move taxonomy).
- `examples/vibe-view-campaign-report/STYLE-Framework-v2-Schema.md` — how PATTERN couples with STYLE (the schema spec).
- `templates/prompt-template.md` — the scenario-agnostic part of the template, ~1100 lines.

## Steps

### 1. Pick a scenario handle

Lowercase, hyphenated, descriptive of *what the page is*, not what it looks like.

- ✓ `campaign-report`, `waitlist`, `product-catalog`, `product-promotion`, `pricing-page`, `case-study`
- ✗ `red-page`, `minimal`, `chris-style`, `v2`

The handle is the directory name and the slug used everywhere downstream.

### 2. Run `scripts/scaffold-scenario.sh`

> *Status:* planned. The expected interface is:

```sh
scripts/scaffold-scenario.sh \
  --handle waitlist \
  --reference-from campaign-report
```

The script copies the three-file shape from `--reference-from` to `scenarios/waitlist/` so you start with a known-good structure, not a blank file. Until shipped, do this by hand:

```sh
SCENARIO=waitlist
mkdir -p scenarios/$SCENARIO
cp examples/vibe-view-campaign-report/PATTERN-block-enriched-v1.md scenarios/$SCENARIO/PATTERN.md
# components.md and template.md you fork from a sibling scenario, then edit
```

### 3. Write `PATTERN.md` — the page skeleton

PATTERN.md describes the page in three axes (this vocabulary is from `examples/.../PATTERN-block-enriched-v1.md`, generalised here):

**A · Archetypes** — what a chapter *says*. Each chapter picks one archetype.

Examples from the Campaign Report: `Hero Monolith` (opening anchor metric), `Time Series` (values over time), `Proportion Field` (parts of whole), `Comparison` (two metrics), `Ranking / List`, `Grouped Metric Cluster`, `Sequence / Timeline`, `Peer Set / Catalog`, `Quote Interstitial`, `Outro Reverent`.

For a Waitlist page the archetypes are different: `Headline + CTA Monolith`, `Social Proof Cluster`, `Feature Strip`, `FAQ`, `Sign-up Form Field`, `Closing Footer`.

**B · Composition Treatments** — how a chapter is *laid out*. Independent of archetype: the same archetype can take different treatments across the page.

The MVP set is style-agnostic: `Full-bleed Monolith`, `Asymmetric Split`, `Stacked Band`, `Matrix Grid`, `Proportion Rail`, `Offset Frame`, `Sequence Track`, `Typographic Field`, `Annotation Rail`. A new scenario may keep all, drop some, or add one — document the choice.

**C · Dominant Move** — the one element that leads the eye in a section. Steady (`scale jump`, `single stroke`, `path reveal`) or disruptive (`crop / bleed`, `offset placement`, `column break`). The page-level *budget* for disruptive moves is also a PATTERN call — Campaign Report budgets ≤ 2 disruptive per page; a Promotion page may budget more.

**Anti-patterns** — at the end of PATTERN.md, list the things this scenario must never become. Examples for Campaign Report: dashboard tile stack with no narrative, donut/pie/ring chart, decorative-only ornament, sloganeering chapter title. A Waitlist's anti-pattern list is different: above-fold without CTA, hero with three competing claims, animated headline.

**No colors. No font weights. No radii. No spacing values.** Those belong to STYLE (the Slot), not PATTERN. PATTERN says "Hero Monolith"; STYLE decides whether that Hero is Cormorant Garamond serif 700 in chromatic crimson or Helvetica 400 in pure white.

### 4. Write `components.md` — the allowed vocabulary

components.md is the **closed list** of components the weak model may use when generating the page. Closing the list is the single biggest leverage on a weak model — three libraries (shadcn, motion, paper-shaders) and a fixed component vocabulary keep doubao-seed-code 2.0 from hallucinating its way into a generic Tailwind landing page.

For each component, write:
- *Name* (PascalCase, what the JSX call looks like).
- *Purpose* (one sentence — what it is for in this scenario).
- *Slots / props* (what data it accepts, in plain English).
- *Composition rule* (when it may appear, when it must not).

Example for Campaign Report `KpiCluster`:

```markdown
**KpiCluster** — Purpose: 2–6 sibling metrics that together evidence one
section claim. Slots: claim · cells (each: label, value, unit, delta).
Composition: must follow Matrix Grid treatment. Must NOT be used as a
free-standing dashboard tile stack (see Anti-patterns).
```

Twelve to twenty components is typical. Resist adding more.

### 5. Write `template.md` — the prompt skeleton with Slot placeholders

template.md is the long md the injector renders. Two layers:

- **Scenario-agnostic prose** — color/typography/spacing/motion rules with `{{atomic.color...}}` placeholders. **Reuse `templates/prompt-template.md` from the Skill.** Do not duplicate the prose; either symlink, copy, or `{{> include}}`-style splice it in.
- **Scenario-specific prose** — chapter list, archetype rules, components vocabulary, anti-patterns. This is what your scenario's template.md contains.

The placeholder syntax (full grammar in `scripts/inject.README.md`):

```
{{path.to.field}}                       — replace
{{#if cond}}…{{/if}}                    — conditional
{{#unless cond}}…{{/unless}}            — inverse
{{#each path}}…{{this}}…{{/each}}       — iteration; @last @first @index available
```

`cond` supports: truthy (`path`), negation (`!path`), equality (`path == "lit"`), inequality (`path != "lit"`). String literals double-quoted. No `&&` / `||` — nest blocks instead.

Per-style conditional blocks are the main reason scenarios fork the template. Example branch from the Campaign Report template:

```
{{#if style_meta.decorative_pack == "festive-royal"}}
SealStamp opens every chapter from chapter 2 onward; Hero (chapter 0) does not
render a SealStamp. GoldenHairline is the only divider on chapter openers and
the Outro. Quote uses CJK brackets `「 」` in primary-gold serif 500.
{{/if}}
```

The scenario's job is to write *its own* per-pack branches when adding a new decorative pack. The Skill's `templates/prompt-template.md` is the shared base.

### 6. Add a Slot for at least one style

A scenario with no style is unusable. Pick any one style — even a Default Sans Light placeholder — and create `src/data/<style-handle>.slot.json` so the injector has something to render. Detail in `04-style-from-references.md`.

### 7. Render a Design Prompt and verify

```sh
python3 scripts/inject.py \
  --slot      src/data/<style-handle>.slot.json \
  --template  scenarios/<scenario-handle>/template.md \
  --out       src/prompts/<style-handle>-<scenario-handle>-v0.1.md
```

The Design Prompt md should be ≤ 620 lines and contain 0 unrendered tokens. If it has unrendered tokens, the template references a path the Slot does not declare — fix the Slot or the template, do not paper over.

### 8. Record the new scenario

In `Round-Log.md` §2 append a round entry describing the new scenario. In §3 update the version snapshot. In `AGENTS.md` add the scenario to the project's scenario list.

## Definition of done

- `scenarios/<handle>/` contains `PATTERN.md` + `components.md` + `template.md`.
- At least one Slot renders against the template with 0 unrendered placeholders.
- The renderer shows the resulting Design Prompt under its Design Prompt tab.
- Round-Log §2 has a new entry for this scenario.

## Pitfalls

- **PATTERN.md with color or font values.** PATTERN is shape; STYLE is surface. If your PATTERN says "Hero uses Cormorant Garamond" you have leaked STYLE into PATTERN.
- **components.md as a wish-list.** The list is *closed*. If a component is on it, the renderer should support it, the template should reference it, and the Slot should configure it. Aspirational components weaken the constraint.
- **Forking the agnostic template before you need to.** Reuse `templates/prompt-template.md` first. Fork only when at least three styles in this scenario need a constraint the agnostic template does not express.
- **Skipping the components anti-pattern list.** What the page should *not* be is often more useful to a weak model than what it should be. Always include 5–10 anti-patterns.
- **Designing the scenario for one client / one style.** The whole point of PATTERN ⊗ STYLE is reusability across N styles. If the scenario locks to a single style, it is not a scenario — it is a one-off page.
