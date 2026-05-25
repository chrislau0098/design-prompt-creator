# design-prompt-creator

> Claude Code Skill that helps designers and design engineers turn **reference images + a short brief** into a tight, weak-model-friendly **Design Prompt**.

Companion repo: [`design-prompt-management`](https://github.com/chrislau0098/design-prompt-management) — Vite renderer + full library of historical Design Prompts (you PR new prompts there once you generate them with this Skill).

---

## What it does

Given:
- 3–5 ground-truth reference images
- A short emotional brief ("red ceremonial / serif / dramatic")
- A page scenario (campaign report / product promotion / waitlist / catalog / …)

This Skill produces:
- A **Slot JSON** — fully tokenized style declaration (OKLCH colors / typography / motion / ornaments)
- A **Design Prompt md** — the actual brief you hand to a weak LLM (doubao-seed-code 2.0, GPT-OSS-20B, etc.) to render the page
- Optional: clone the renderer repo into your project to preview the Design System and Report Example visually

The workflow is built around three hard constraints sediment from ~3 weeks of iteration on a real production project (R-76 through R-97):

1. **Three-Way Sync** — Prompt ↔ Design System ↔ Report Example must always agree.
2. **Patch then verify with rendered proof** — never trust file grep; re-render and look.
3. **Design Prompt ≤ 620 lines, every word constrains** — weak-model context is precious.

See [`reference/99-principles.md`](reference/99-principles.md) for the full 14-principle index, and [`reference/case-studies.md`](reference/case-studies.md) for 11 real bugs and how to avoid them.

---

## Install

Clone directly into Claude Code's skills folder:

```bash
git clone https://github.com/chrislau0098/design-prompt-creator.git \
  ~/.claude/skills/vibe-page-design-prompt-management
```

That's it. Restart Claude Code (or just keep using it — the skill is hot-loaded). Trigger by:

- **Slash command**: `/vibe-page-design-prompt-management`
- **Natural language**: "新风格" / "新场景" / "生成 prompt" / "三方 sync" / "iterate"

The skill description matches these triggers automatically.

### Dependencies

- Python 3.10+ (stdlib only) — for `scripts/inject.py` and `scripts/verify-three-way-sync.py`
- Bash (macOS / Linux) — for the `scaffold-*.sh` helpers
- Git + `gh` CLI (optional) — for renderer clone and PR flow

---

## Workflow (8 steps)

Each step has a short companion file in `reference/`. The skill loads them on demand — you don't read all 9 reference modules every time.

```
1. Init project           → reference/01-init.md          → scripts/scaffold-project.sh
2. Pick roles             → reference/02-roles.md
3. Define a scenario      → reference/03-scenario-define.md → scripts/scaffold-scenario.sh
   (PATTERN + Components)
4. Extract style from     → reference/04-style-from-references.md → scripts/scaffold-style.sh
   reference images       
5. Generate Design Prompt → reference/05-prompt-generate.md → scripts/inject.py
6. Render in Vite         → reference/06-design-system-render.md
   (Design System + Report Example views)
7. Review                 → reference/07-prompt-review.md  → scripts/verify-three-way-sync.py
   (three-way sync + anti-slop + line-count)
8. Iterate                → reference/08-iterate.md
   (feedback → patch chain → re-inject → re-verify)
```

A new project starts at step 1; a new style inside an existing project starts at step 4; a feedback-driven change starts at step 8.

---

## Quickstart (5 minutes)

```bash
# 1. Scaffold a new project (clones the renderer into ./design-prompt-management/)
bash ~/.claude/skills/vibe-page-design-prompt-management/scripts/scaffold-project.sh \
  --name my-report --scenario campaign-report --dest ~/Documents/my-report

# 2. Add a style (interactive — fill in the Slot JSON it creates)
cd ~/Documents/my-report
./scripts/scaffold-style.sh --style my-first-style --scenario campaign-report --project .

# 3. Inject Slot + Template → Design Prompt
python3 scripts/inject.py \
  --slot scenarios/campaign-report/slot-examples/my-first-style.slot.json \
  --template scenarios/campaign-report/prompt-template.md \
  --out scenarios/campaign-report/my-first-style-Design-Prompt-v0.1.md

# 4. Sync to renderer + preview
./scripts/sync-to-management.sh --scenario campaign-report --style my-first-style
cd design-prompt-management && bun install && bun dev
# Open http://localhost:5173, switch to the "Design Prompt" tab
```

Or just say to Claude Code: **"用 vibe-page-design-prompt-management Skill,这是 5 张参考图 + brief: 红色喜庆 / 衬线 / 大气,场景 campaign-report"** — it will walk you through.

---

## Repo structure

```
design-prompt-creator/
├── SKILL.md                    # Skill main entry (Anthropic Progressive Disclosure model)
├── reference/                  # On-demand reference modules
│   ├── 01-init.md  ... 08-iterate.md
│   ├── 99-principles.md        # 14 principles index
│   └── case-studies.md         # 11 real bug cases (R-83~R-97) — what to avoid
├── templates/                  # PATTERN / Slot / AGENTS / Round-Log / component-spec / prompt
├── scripts/                    # scaffold-{project,scenario,style}.sh + inject.py + verify-three-way-sync.py
└── scenarios/                  # Out-of-box scenarios
    ├── campaign-report/        # MVP, full reference from Vibe view R-76~R-97
    ├── product-promotion/      # stub — fill per reference/03-scenario-define.md
    ├── product-catalog/        # stub
    └── waitlist/               # stub
```

Production examples (6 styles × ~58 historical Design Prompts) live in the companion [`design-prompt-management`](https://github.com/chrislau0098/design-prompt-management) repo under `prompts/vibe-view-campaign-report/`.

---

## Contributing

- **New scenario** (e.g. you want to use this for a podcast landing page): fill in `scenarios/<your-scenario>/{PATTERN.md, components.md}` following `reference/03-scenario-define.md`, then PR.
- **New principle or case study**: edit `reference/99-principles.md` or `reference/case-studies.md` with a real-world bug + how to detect/avoid, then PR.
- **Skill improvements**: SKILL.md / reference/ modules should stay short (200–500 lines each) — every line earns its place.

### Cross-repo experience flow

Real-world bugs and decisions from production work happen in [`design-prompt-management`](https://github.com/chrislau0098/design-prompt-management) projects — they first get recorded round-by-round in that repo's `history/Round-Log-<project>.md` (a project-specific journal, kept under version control with the prompts).

Periodically (every 5–10 rounds, or after a phase wraps), Cowork (Claude Code) abstracts the generalisable lessons from those Round-Log entries into this repo's `reference/case-studies.md` and `reference/99-principles.md`, then PRs them upstream. This keeps the Skill's reference material grounded in real bugs without forcing every project-specific detail into the public Skill.

Trigger conditions for an abstraction pass:
- Cowork notices ≥3 new round entries since last audit, **or**
- a designer flags a recurring issue ("this bug came back"), **or**
- a phase completes (e.g. a new scenario stabilises).

---

## License

MIT
