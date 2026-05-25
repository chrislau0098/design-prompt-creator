# 02 · Roles and Sub-agent Dispatch

> Who does what. When the main Cowork agent should do the work directly, when to dispatch a sub-agent, and how to write the sub-agent prompt so the result comes back with real verify proof — not a self-graded "PASS".

## The two roles

### Cowork (main session)

- **Model**: Opus (Anthropic, latest 4.x).
- **Job**: Planner and Architect. Receives feedback, decides what changes (Slot? template? renderer? produced md?), assembles the patch chain, dispatches sub-agents, **verifies their output independently** before reporting back.
- **Owns**: AGENTS.md, Round-Log.md, the three-way sync audit, the decision on whether to re-inject, the decision on whether a sub-agent's report is trustworthy.
- **Does not own**: doing every CSS tweak by hand (delegate), writing every Slot field (delegate), running every inject (delegate when the work is mechanical).

### Sub-agents (dispatched per task)

- **Model**: Opus for prose / Design Prompt text / template design / complex judgement. Sonnet for engineering / sync / verify / mechanical refactor.
- **Job**: Execute one bounded task with a self-contained prompt. Report back with verify proof in the structure Cowork requested.
- **Owns**: the work in their patch site, the verify evidence in their report.
- **Does not own**: the decision about *what* to change (Cowork decides), the three-way sync audit (Cowork verifies after).

## Model selection — Opus vs Sonnet

The rule comes from the example project's Round-86: pick the smaller model when the task is mechanical, the bigger model when the task asks for prose taste or hard judgement. Bullet form:

**Use Opus for:**
- Writing or editing a Design Prompt md (the weak model reads this — prose quality matters).
- Designing or rewriting `templates/prompt-template.md`.
- Extracting a style Slot from reference images (vision + semantic mapping is a taste call).
- Auditing three-way sync — calling out drift requires understanding the design intent, not just diffing strings.
- Resolving a Chris-style ambiguous feedback ("feels off", "looks slop") — needs an aesthetic judgement.

**Use Sonnet for:**
- HTML/CSS mechanical changes that have a clear before/after spec.
- Running `python3 inject.py` and reporting line counts / unrendered tokens.
- Syncing one source of truth to another (Slot → renderer inline data, template version bumps).
- Adding a component to the renderer when the spec is already a written CSS block.
- Refactors with explicit grep targets ("change every `bg-surface-l2 + border` to `bg-surface-l2` and report the line numbers").

Sonnet is faster and cheaper. Default to it for engineering. Only escalate to Opus when the work is taste-bound.

## When the main agent does the work directly

Skip the sub-agent when:

- The change is **one or two files** and **under ~30 minutes** for a human.
- The change touches **multiple coupled systems** (Slot + template + renderer + produced md) and the cross-system reasoning would be lost in handoff.
- The change is a **judgement call you cannot delegate** (e.g. "is this signature ornament the right one?").
- A **prior sub-agent** has already failed twice on the same task — the third try is on you.

The example project's Round-92 (festive-royal Cinnabar + festive-editorial Crimson Bar) was a Cowork-direct case: two ornaments, tightly coupled to Slot tokens + renderer + template, where R-90/R-91 had shown sub-agents struggle to mirror existing per-pack CSS overrides across packs.

## How to write a sub-agent prompt

The prompt must be self-contained — the sub-agent has no memory of your conversation. Include all of:

### A · Identity and bound
```
You are sub-agent X (model: Sonnet, engineering task) under Cowork (R-NN, project ...).
Your task: <one sentence>.
Out of scope: <what you must NOT touch>.
```

### B · Inputs — paths and lines, not summaries
```
Read first:
- /abs/path/to/Round-Log.md §1 + most recent round
- /abs/path/to/templates/prompt-template.md lines L-L
- /abs/path/to/src/data/<style>.slot.json
```

Use **absolute paths**. Sub-agents in worktrees have their CWD reset between bash calls; relative paths break silently.

### C · What to change, concretely
```
Patch sites:
1. <abs path> — <what + why, 1-2 sentences>
2. ...
```

Avoid "improve" / "polish" / "make it better". State the diff. If you cannot state the diff, you do not have a sub-agent task — you have a Cowork task.

### D · Verify proof requirements (do not skip)

This is the part that fails most often. The example project's R-94 #35 and R-87 #18 are both about Cowork accepting a sub-agent's self-grade and finding real drift later. Always require **rendered evidence**:

```
Verify proof you must return:
1. ls -la <each produced file or directory> — full output
2. wc -l <each produced md> + grep -c '<invariant>' <file> for each invariant
3. cat -n <key file> lines L-L showing the actual changed lines
4. (for renderer work) curl http://localhost:5173 returns 200 + DOM evidence
   via mcp__Claude_Preview__preview_eval `document.querySelectorAll(...)` count
5. Anti-slop grep: grep -nE '<pattern>' <files> with EXPECTED count
```

### E · Report format
```
Report in this structure (under 800 words):
- Files changed: <list>
- Lines added / removed: <wc -l before vs after>
- Verify proof: <pasted output of each item in §D>
- Pitfalls hit: <anything tricky you decided>
- Open questions for Cowork: <if any>
```

### F · Discipline reminder
```
- Do not invent file paths. If a path does not exist, ls its parent and report what is there.
- Do not self-grade "PASS" without the §D evidence. A bare "all good" report = rejected.
- If you get stuck, report cleanly. Do not hallucinate work you did not do.
```

## After a sub-agent returns

Cowork **always** does an independent verify pass — never trusts the sub-agent's report alone. Minimum:

1. `ls -la <produced path>` yourself.
2. `wc -l <produced files>` yourself.
3. Grep for the same invariants you asked the sub-agent to grep — confirm the counts match.
4. For renderer work: open the renderer (or use Claude Preview) and look at the result. The example project's R-95 sub-agent reports trended trustworthy *after* Cowork ran the same DOM eval and confirmed the numbers matched.
5. If there is a mismatch, **report the mismatch in Round-Log §2**; do not silently re-dispatch.

## Common failure modes and counter-prompts

| Failure | Counter |
|---|---|
| Sub-agent patches one render path, leaves N others unpatched (R-87 ShadCard children bug, R-90 chapter opener × 7). | "Enumerate every render path. Grep `function render.*<thing>` and list line numbers. Patch each one." |
| Sub-agent copies a CSS pattern from one pack to another but drops a critical rule (R-91 missed `flex-direction: column` mirror). | "When mirroring pack X's CSS to pack Y, list every CSS rule in X's per-pack block and confirm each is mirrored." |
| Sub-agent self-grades "all 6 styles PASS" without DOM verify (R-94 #35, R-90 #24). | Require `mcp__Claude_Preview__preview_eval document.querySelectorAll(...).length` numbers in the report. |
| Sub-agent uses smart-quotes by accident in JS strings (R-90 fontFamily bug). | `grep -nP '[‘’“”]' <files>` must return 0. |
| Sub-agent writes to its worktree CWD instead of canonical path (Cowork R-94 #35 misjudgement). | Always pass absolute canonical paths. Sub-agent reports `ls -la <abs canonical path>` to prove the destination. |

## When to escalate vs continue

- One sub-agent failure → re-dispatch with a tighter prompt (add a §D verify-proof item that covers the missed case).
- Two failures on the same task → Cowork does it directly.
- A failure that exposes a missing principle → add the principle to the project's Round-Log §1, then dispatch.

## Canonical path vs worktree CWD

A subtle trap: a sub-agent's bash CWD lives inside its worktree (`.claude/worktrees/<agent-id>/`), but its Edit/Write calls with **absolute paths** write to the canonical project root (`/Users/.../Code/<project>/...`). The worktree boundary is *not* a sandbox for Edit/Write.

What this means in practice:

- Always pass absolute canonical paths in the dispatch prompt — never `./src/...` or `projects/...`. The sub-agent's relative path resolves to the worktree CWD, which is the wrong place.
- The sub-agent's verify report must include `ls -la <absolute canonical path>` — proving the destination is correct.
- Cowork's verify must `ls -la <absolute canonical path>`. Running `ls` in the worktree CWD shows only the small subset mirrored there — and you will mistakenly conclude "sub-agent hallucinated" when the work actually landed in canonical and is fine.
- If the work has multiple destinations (e.g. produced md to `examples/<scenario>/<style>/...md` *and* renderer slot to `renderer/src/data/<style>.slot.json`), each destination gets its own `ls -la` line.

The example project's R-94 #35 is the canonical lesson: Cowork looked at the worktree CWD, saw only `node_modules + bun.lock`, and accused the sub-agent of fabricating 95 % of the work. The work was real — at the canonical Vite project path. The cost was an unnecessary re-dispatch and a real loss of trust in a sub-agent who had executed cleanly.

## Model selection rationale (extended)

The Opus / Sonnet split is not about "smart" vs "dumb". It is about *which kind of failure* each model tends toward, and which kind of failure costs the project the most.

- **Sonnet's failure mode**: mechanical correctness on the requested patch, blindness to neighbouring drift. Sonnet completes the task as written and stops. If the task spec was incomplete, the gaps stay open. This is exactly right for engineering tasks where Cowork wrote a tight spec.
- **Opus's failure mode**: re-deciding what the task is, sometimes against the brief. Opus reads the principles, notices a smell, and proposes a wider fix. This is exactly right for taste tasks where Cowork wrote an ambiguous brief on purpose.

When the brief is *concrete* (paths, line numbers, before/after CSS), Sonnet's "do exactly this" discipline ships faster and cheaper. When the brief is *aesthetic* ("the Hero shader feels wrong"), Opus's "let me re-examine the principle" is what you want.

A practical rule from the example project's Round-94 / 95: when in doubt, draft the brief and ask yourself — "could I write this as a 20-line diff?". If yes, Sonnet. If the answer needs prose explanation, Opus.

## Common failure modes — extended

The table in the section above lists the most common; here is the full catalogue from the example project, with the counter-prompt:

| Failure | Counter-prompt clause |
|---|---|
| Sub-agent's `ls` shows the worktree CWD, not the canonical destination, and they report "I'm not sure where this landed". | "Always Edit/Write at absolute canonical paths. Report `ls -la <abs path>` for each destination." |
| Sub-agent argues a Slop Taxonomy violation is "actually fine" with a context-specific explanation. | "Slop Taxonomy violations are Blocking. Do not argue — fix or stop." |
| Sub-agent grep-counts the right number but the rendered DOM disagrees. | "Pair every `grep -c` with `mcp__Claude_Preview__preview_eval document.querySelectorAll(...).length`. Numbers must agree." |
| Sub-agent fixes A's geometry, breaks B's geometry, doesn't notice. | "After any layout fix, screenshot the patched element and three neighbours. Report each." |
| Sub-agent leaks demo paths into general Skill prose. | "If the file is in `reference/` or `templates/`, no path may reference `examples/<scenario>/`. Use placeholders." |
| Sub-agent uses brand token `var(--primary)` for a decorative element. | "Before using a brand token in a new ornament, grep the Slot for the pack's actual OKLCH. Verify the semantic match." |

The principle behind these: a sub-agent prompt is only as strong as the failure modes you anticipated. Each new failure you discover earns its place in the prompt for the next dispatch.
