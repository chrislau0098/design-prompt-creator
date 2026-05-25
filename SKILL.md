---
name: vibe-page-design-prompt-management
description: Designer / design-engineer workflow to generate, render, review, and iterate high-quality Design Prompts for AI-rendered web pages (campaign report, product promotion, product catalog, waitlist). Use when the team needs to (a) init a project, (b) define a new scenario (PATTERN + Components), (c) extract a style from reference images into a Slot JSON, (d) inject Slot+Template into a Design Prompt md, (e) preview Design System / Report Example in a Vite renderer, (f) verify three-way sync (Prompt ↔ Design System ↔ Report Example) and anti-slop, or (g) iterate on direct visual feedback. Multi-scenario, multi-style, weak-model friendly (doubao-seed-code 2.0, GPT-OSS-20B). Triggers — "新风格", "新场景", "生成 prompt", "三方 sync", "iterate", or slash `/vibe-page-design-prompt-management`.
---

# Vibe Page · Design Prompt Management

A Skill for designers and design engineers who use weak/cheap LLMs (doubao-seed-code 2.0, GPT-OSS-20B, open-source small models) to render production web pages. The Skill turns *reference images + a short brief* into a tight, faithful, low-slop **Design Prompt** that the weak model can follow without inventing or hallucinating.

Output per scenario × per style: one **Slot JSON** (style declaration), one **Design Prompt md** (the brief the weak model sees), and one **Vite renderer view** (the visual truth that humans audit).

---

## Core Ideas

1. **Three-layer architecture**: `PATTERN` (page skeleton, scenario-specific) ⊗ `STYLE` (a Slot JSON, plus a small per-style override pack) ⊗ `TEMPLATE` (one scenario-agnostic md with `{{slot.path}}` placeholders). Inject Slot+Template → final Design Prompt.
2. **Three-Way Sync is sacred**: Design Prompt (what we tell the weak model) ⇄ Design System view (what the Slot declares) ⇄ Report Example view (what actually renders). Any drift = a real bug. Every Slot/Prompt/render change must re-pass the three-way audit.
3. **Patch then verify with rendered proof**: do not trust file-grep after a change. Re-render in the Vite renderer (or browser DOM), eyeball it, then `wc -l` and `grep` for invariants. Sub-agents must return real DOM evidence in their report, never a self-graded "PASS".
4. **Solve at the source, never patch over symptoms**: a too-loud Hero shader → tune `colorFront` lightness, not a `backdrop-filter blur` on top. A filled card looks weak → drop the border, never add one. Each extra layer is debt.
5. **Design Prompt ≤ 620 lines, every word constrains**: weak-model context is precious. No metadata, no few-shot examples, no full code snippets, no historical narrative, no emoji checklists. If you cannot answer "would the output measurably degrade without this sentence?" → cut it.

The full principle index — including the rules above plus seven more (Hero ≠ chapter, weight ≤ 500 baseline, filled-vs-border, Hero shader rules, etc.) — lives in [`reference/99-principles.md`](reference/99-principles.md).

---

## Workflow Overview

Eight steps. Each step has a short `reference/0X-*.md` companion with concrete commands, decision rules, and pitfalls.

```
1. Init project           → reference/01-init.md
2. Define roles           → reference/02-roles.md
3. Define a scenario      → reference/03-scenario-define.md
   (PATTERN + Components)
4. Extract style from     → reference/04-style-from-references.md
   reference images       
   (images → Slot JSON)
5. Generate Design Prompt → reference/05-prompt-generate.md
   (Slot + Template → md, via scripts/inject.py)
6. Render in Vite         → reference/06-design-system-render.md
   (Design System + Report Example views)
7. Review                 → reference/07-prompt-review.md
   (three-way sync + anti-slop + line-count)
8. Iterate                → reference/08-iterate.md
   (feedback → patch chain → re-inject → re-verify)
```

A new project usually starts at step 1; a new style inside an existing project starts at step 4; a feedback-driven change starts at step 8. The `99-principles.md` index is read-only — refer to it any time a design judgement is needed.

---

## Decision Routing

When invoked, decide which step to enter based on what the user says. Default: ask one clarifying question only if the trigger is ambiguous (per global "Auto Mode" — make the reasonable call, they will redirect).

| User intent / trigger keywords | Enter | Tool / script |
|---|---|---|
| "新项目", "init", "scaffold project" | `reference/01-init.md` | `scripts/scaffold-project.sh` (planned) |
| "新场景", "新页面类型", "scenario", "campaign report / waitlist / catalog / promotion" | `reference/03-scenario-define.md` | `scripts/scaffold-scenario.sh` (planned) |
| "新风格", "新配图", "extract style", "from these references" | `reference/04-style-from-references.md` | `scripts/scaffold-style.sh` (planned) |
| "生成 prompt", "重 inject", "render the prompt" | `reference/05-prompt-generate.md` | `scripts/inject.py` |
| "看效果", "render", "open the renderer" | `reference/06-design-system-render.md` | `cd renderer && bun dev` |
| "review", "三方 sync", "anti-slop", "check the prompt" | `reference/07-prompt-review.md` | `scripts/verify-three-way-sync.py` (planned) |
| "iterate", "改一下", "Chris 反馈", feedback screenshots | `reference/08-iterate.md` | n/a — patch chain |
| "原则", "why", "is this slop?" | `reference/99-principles.md` | n/a — reference |
| "派 sub-agent", "should I use Opus or Sonnet?" | `reference/02-roles.md` | n/a — reference |

When in doubt: load the routed reference first, *then* act. Do not try to keep all rules in head — the references are short and self-contained on purpose.

---

## Scenarios

The Skill is multi-scenario. Each scenario lives under `scenarios/<scenario>/` and contains:

- `PATTERN.md` — page skeleton (chapters, archetypes, composition treatments, dominant moves). Scenario-specific.
- `components.md` — the components the weak model is allowed to use (e.g. KPI cluster, Time Series, Sequence Track).
- `template.md` — the scenario's prompt template, with `{{slot.path}}` placeholders. The injector renders this with the chosen Slot.

| Scenario | Status | Notes |
|---|---|---|
| `campaign-report` | **MVP shipped** — full reference example at `examples/vibe-view-campaign-report/` with 6 styles, 6 production Design Prompts, Vite renderer, Round-Log §1 12 principles distilled. | The reference scenario. Read it first. |
| `product-promotion` | stub | Phase 6 sub-agent fills. |
| `product-catalog` | stub | Phase 6 sub-agent fills. |
| `waitlist` | stub | Phase 6 sub-agent fills. |

**Scenario-agnostic vs scenario-specific:**

- *Agnostic* — sits in `templates/prompt-template.md`: color/typography/spacing/motion CSS variables, weight ceilings, anti-slop language, the per-pack ornament condition switches.
- *Specific* — sits in `scenarios/<scenario>/{PATTERN.md, components.md, template.md}`: which chapters exist, what each chapter says, which archetypes the page may pick from.

Adding a new scenario = write its PATTERN + components, then either reuse `templates/prompt-template.md` as-is or fork it. Do not pollute the agnostic template with scenario-specific prose.

---

## Dependencies

| Dependency | Version | Used for |
|---|---|---|
| Python | 3.10+ (stdlib only) | `scripts/inject.py` |
| Vite renderer | bundled at `renderer/design-system-renderer-vite/` | preview the rendered styles |
| Bun | 1.0+ | run the renderer (`bun install && bun dev`) |
| Claude Code | latest | drives the workflow; supports `Opus` for prose / `Sonnet` for engineering — see `reference/02-roles.md` |
| `@pierre/diffs` | inside renderer | shows Design Prompt diff vs previous version |
| `paper-shaders`, `motion`, `shadcn/ui`, `recharts` | inside renderer | the three-library limit imposed on weak models |

The renderer is self-contained. No external services, no API keys. Bring-your-own weak model for actually generating pages from the produced Design Prompt md.

---

## Repository Layout

```
vibe-page-design-prompt-management/
├── SKILL.md                            # this file (≤ 500 lines, the entry)
├── reference/
│   ├── 01-init.md                      # new project bootstrap
│   ├── 02-roles.md                     # Cowork main agent + sub-agent dispatch rules
│   ├── 03-scenario-define.md           # PATTERN + Components for a new scenario
│   ├── 04-style-from-references.md     # reference images → Slot JSON
│   ├── 05-prompt-generate.md           # Slot + Template → Design Prompt md
│   ├── 06-design-system-render.md      # launch Vite renderer, three views
│   ├── 07-prompt-review.md             # three-way sync + anti-slop + line count
│   ├── 08-iterate.md                   # feedback → patch chain → re-verify
│   └── 99-principles.md                # 12 core principles (generalised from Round-Log §1)
├── templates/
│   └── prompt-template.md              # scenario-agnostic, Slot-driven prompt template
├── scripts/
│   ├── inject.py                       # Slot + template → md renderer (Python 3.10+)
│   └── inject.README.md                # CLI usage + syntax cheat-sheet
├── scenarios/
│   ├── campaign-report/                # MVP scenario
│   ├── product-promotion/              # stub (Phase 6)
│   ├── product-catalog/                # stub (Phase 6)
│   └── waitlist/                       # stub (Phase 6)
├── examples/
│   └── vibe-view-campaign-report/      # real production example, 6 styles, Round-Log, Slop Taxonomy
└── docs/                               # cross-cutting design specs (Schema, Slop Taxonomy, etc.)
```

Two reading orders work:
- *Top-down* — read SKILL.md → pick a step → read the matching `reference/0X-*.md` → act.
- *Bottom-up* — `examples/vibe-view-campaign-report/Round-Log.md` (§1 principles + a few rounds) → `templates/prompt-template.md` first 100 lines → `scripts/inject.py` API → then SKILL.md for navigation.

---

## Conventions

- **One file = one responsibility.** SKILL.md routes; references explain; scripts do; templates parameterise.
- **No emoji checklists, no metadata blocks, no inline source URLs in produced prompts.** These are the weak-model context-killers (see principles 11 and 12 in `reference/99-principles.md`).
- **Absolute paths in agent dispatch.** Worktree CWD ≠ Edit/Write destination — always pass canonical absolute paths to sub-agents and ask them to report `ls -la <produced path>` as verify proof.
- **Version everything that lands.** Slot files carry `version: vX.Y`; Design Prompt md filenames embed the version; Round-Log §5 holds the latest-version snapshot. The renderer pins to specific versions via `src/data/*.slot.json`.
- **Don't grow the surface area.** Adding a scenario or a style is fine. Adding a new top-level concept (a fourth view, a second injector, a parallel schema) requires a written reason in the project's Round-Log.

---

## When NOT to use this Skill

- You are designing a single one-off page in Figma and a human will hand-code it. This Skill exists to make *weak LLMs* produce pages — not to replace a designer + a strong frontend engineer.
- You need brand identity / logo / marketing asset work. Use `ckm-design` or `ckm-brand` instead.
- You need to *audit* an existing live site for visual quality. Use `design-review` or `critique`.
- You want to ship raw HTML from a description without the Slot/Template machinery. Use `design-html` instead.

This Skill is specifically for: *recurring* page production at *high visual quality* with *cheap models*, where the Design Prompt is the long-lived artifact and the renderer is the truth.
