# 01 · Project Initialization

> Bootstrap a new design-prompt project from this Skill template. Output: a fresh project directory wired for the four-step weak-model production loop (scaffold → style → inject → render).

## When to use this step

- Designer or design-engineer is starting fresh: a new product, a new page type, a new client. No prior Slot JSONs, no prior Design Prompts.
- An existing project has drifted past repair (template fork has diverged from the Skill, Round-Log is unrecoverable) and the team wants to re-bootstrap.

Do **not** use this step for:
- Adding a new style to an existing project → go to `04-style-from-references.md`.
- Adding a new page scenario to an existing project → go to `03-scenario-define.md`.

## Goal directory shape

After init the project looks like this (paths are relative to the project root):

```
my-vibe-project/
├── AGENTS.md                    # roles, dispatch rules, paths the agent must know
├── Round-Log.md                 # iteration history + abstracted principles (the project's memory)
├── DESIGN.md                    # the design system Chris/team agreed on (mood, palette, type)
├── src/
│   ├── data/                    # Slot JSONs (one per style) — the truth
│   │   └── README.md
│   ├── prompts/                 # rendered Design Prompt md (one per style × scenario)
│   │   └── README.md
│   └── prompts-previous/        # last-version snapshots, used by the renderer diff view
├── scenarios/                   # per-scenario PATTERN + components + template
│   └── (copied from skill scenarios/)
├── renderer/                    # Vite project, can be a git submodule or copy
├── _attachments/                # reference images grouped by style (style-mood-references/)
└── .gitignore
```

## Steps

### 1. Pick a project root

Convention: keep the project outside the Skill itself. The Skill is the recipe; the project is the meal.

```sh
PROJECT_ROOT=~/Code/my-vibe-project
mkdir -p "$PROJECT_ROOT"
cd "$PROJECT_ROOT"
git init
```

### 2. Run `scripts/scaffold-project.sh`

> *Status:* planned. Until shipped, do the equivalent by hand using the template files in this Skill. The expected interface is:

```sh
scripts/scaffold-project.sh \
  --root  "$PROJECT_ROOT" \
  --name  "My Vibe Project" \
  --owner "Chris"
```

What it does, step by step (so the agent can do it manually if the script is missing):

1. Create the goal directory shape above.
2. Copy `templates/prompt-template.md` from the Skill to `src/prompt-template.md` (the project may fork it; do not edit the Skill copy).
3. Copy `scripts/inject.py` from the Skill to `src/inject.py` (or leave it referenced — the inject contract is stable).
4. Write `AGENTS.md` (see §3 below for the seed content).
5. Write `Round-Log.md` (see §4 below for the seed content).
6. Write `DESIGN.md` — leave it mostly empty; the team writes it during step 04 (style extraction). Seed sections: `## Mood`, `## Palette (OKLCH tokens)`, `## Typography`, `## Spacing & Layout`, `## Motion`, `## Component vocabulary`.
7. Stage and commit: `git add -A && git commit -m "init: scaffold from vibe-page-design-prompt-management"`.

### 3. AGENTS.md seed

`AGENTS.md` is the agent's read-me. It tells the next Cowork session (or sub-agent) where everything is and which rules apply. Minimum seed:

```markdown
# AGENTS.md · My Vibe Project

## Roles
- **Cowork (main, Opus)** — Planner + Architect. Reads feedback, picks the patch site, dispatches sub-agents, verifies output.
- **Sub-agents (Sonnet or Opus, see reference/02-roles.md)** — Engineering or prose work, dispatched with a self-contained prompt.

## Paths
- Project root: `~/Code/my-vibe-project/`
- Slots: `src/data/*.slot.json`
- Rendered prompts: `src/prompts/*.md` (latest), `src/prompts-previous/*.md` (one prior)
- Template: `src/prompt-template.md`
- Injector: `src/inject.py`
- Renderer: `renderer/` (Vite, `bun dev` → http://localhost:5173)
- Round-Log: `Round-Log.md` (iteration history + principles)

## Rules (do not omit)
1. Three-Way Sync (Prompt ↔ Design System ↔ Report Example) is sacred. Any change re-runs the audit.
2. Patch then verify with rendered proof, not file-grep alone.
3. Design Prompt md ≤ 620 lines; trim if it grows past that.
4. Sub-agents must report absolute canonical paths + `ls -la` + key file head, never a self-graded PASS.
5. See `reference/99-principles.md` in the Skill for the full list.
```

### 4. Round-Log.md seed

`Round-Log.md` is the project's permanent memory. It accumulates over months and survives Cowork session resets. Minimum seed:

```markdown
---
type: round-log
project: My Vibe Project
created: YYYY-MM-DD
maintained_by: Cowork
update_pattern: append on every round / issue / patch
---

# Round Log

## §1 Abstracted Principles
(Empty at init. Fill as the team learns. Refer to vibe-page-design-prompt-management/reference/99-principles.md for a starter list — adopt selectively, generalise only what the project actually hits.)

## §2 Iteration History
(Append per round, format: `### Round-NN (YYYY-MM-DD) · phase / theme` → symptom → root cause → fix → verify → principle.)

## §3 Version Snapshot (latest)
- Template: src/prompt-template.md vX.Y
- Slots: (one row per style, with version + last-edit round)
- Prompts: (one row per style × scenario, with filename + line count)
- Renderer: renderer/ commit SHA
```

### 5. Wire the renderer

Either clone the renderer (Vite project) or copy from the Skill example:

```sh
cp -R <skill>/examples/vibe-view-campaign-report/renderer  "$PROJECT_ROOT/renderer"
cd "$PROJECT_ROOT/renderer"
bun install
bun dev
```

The renderer expects `src/data/*.slot.json` to follow the Slot Schema (see `examples/vibe-view-campaign-report/slot-schema-v0.md`). It will render any Slot at `?style=<handle>` once the file exists.

### 6. Commit

```sh
git add -A
git commit -m "init: project structure + AGENTS.md + Round-Log.md seed"
```

## Definition of done

- `ls "$PROJECT_ROOT"` shows all five top-level pieces (`AGENTS.md`, `Round-Log.md`, `DESIGN.md`, `src/`, `renderer/`).
- `cd renderer && bun dev` returns HTTP 200 on `http://localhost:5173`.
- `python3 src/inject.py --selftest` exits 0 (when at least one Slot exists).
- The project is a git repo with one initial commit.
- The first round can start: either step 03 (add a scenario) or step 04 (extract a style from references).

## Pitfalls

- **Editing the Skill's `templates/prompt-template.md` instead of copying it.** Don't. The Skill is shared across projects; the project may fork. After copying, document any divergence in the project's Round-Log §1.
- **Init-time DESIGN.md too detailed.** DESIGN.md is *evidence written by the team after seeing what works*, not a guess up-front. Seed only the section headings.
- **Forgetting `git init`.** Round-Log loses much of its value without commit history to cross-reference.
- **Mixing scenarios into one Slot.** A Slot describes *a style*. Page-shape decisions (which chapters exist, which archetypes) belong in `scenarios/<scenario>/PATTERN.md`, not in the Slot.
- **Copy-paste an example Slot and edit values without understanding the schema.** Read `slot-schema-v0.md` once, end-to-end. The 30 minutes pay back the first time someone adds a new style.
