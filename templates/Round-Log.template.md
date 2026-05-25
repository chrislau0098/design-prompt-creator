---
type: round-log
project_name: "{{project_name}}"
scenario: "{{scenario}}"
phase: "{{phase}}"
created: "{{YYYY-MM-DD}}"
---

# Round Log · {{project_name}} · {{scenario}}

> Append-only. Latest round at the top of §2. Never edit past rounds.

---

## §1 Core Principles Index

<!-- 12-slot index. Each slot = one principle heading + one-line summary. Fill on project init. -->

1. **Root-cause fix** — solve at the source; never layer masks over problems.
2. **Layer separation** — System Prompt owns data contract; Design Prompt owns visual style; running-env owns runtime base.
3. **Slot drives template** — the Slot JSON is the single source of truth for all style values; prompt-template.md has no hardcoded values.
4. **Three-way sync** — Prompt ornament list, Slot declaration, and Renderer output must match; mismatch = bug.
5. **Line-count discipline** — Design Prompt ≤ 620 lines; verify after every patch.
6. **Unrendered tokens = 0** — any `{{...}}` surviving injection is a blocker; fix in Slot before shipping.
7. **No dual layer** — one focal move per section; one ambient shader per page; no second hot accent.
8. **Treatment variety** — no two consecutive sections share composition treatment or archetype.
9. **Density rhythm** — adjacent sections differ in density; all three tiers appear across the page.
10. **Weight ceiling** — font-weight never exceeds the declared `weight_ceiling` in atomic.typography.
11. **{{Principle_11}}** — {{one-line summary}}
12. **{{Principle_12}}** — {{one-line summary}}

---

## §2 Iteration History

<!-- Newest round first -->

### Round 1 · {{YYYY-MM-DD}} · Init

**Baseline**: none (project start)
**Changed**: scaffolded from templates
**Result**: initial files created

---

<!-- Copy the block below for each new round:

### Round N · {{YYYY-MM-DD}} · {{short label}}

**Baseline**: {{previous version identifier}}
**Changed**:
- {{change 1}}
- {{change 2}}
**Verify**: inject OK / line count {{N}} / unrendered_tokens 0 / three-way sync {{pass|skip}}
**Result**: {{version identifier or description}}
**Chris feedback**: {{feedback summary or "pending"}}

---
-->

---

## §3 Style Genealogy

<!-- Running history of which Slot versions are in use per scenario -->

| Scenario | Style Handle | Slot Version | Status |
|----------|-------------|-------------|--------|
| {{scenario}} | {{style_handle}} | v0.1 | draft |

---

## §4 Open Issues

<!-- Unresolved bugs / decisions. Remove when resolved; add to §2 round log. -->

| # | Issue | Opened | Status |
|---|-------|--------|--------|
| 1 | {{issue_description}} | {{date}} | open |

---

## §5 Current Version Snapshot

<!-- Update after every stable round -->

| Artifact | Path | Version |
|----------|------|---------|
| Schema / Slot | `scenarios/{{scenario}}/slot-examples/{{style_handle}}.slot.json` | {{version}} |
| Template | `scenarios/{{scenario}}/prompt-template.md` | {{version}} |
| PATTERN | `scenarios/{{scenario}}/PATTERN.md` | {{version}} |
| Design Prompt (rendered) | `scenarios/{{scenario}}/Design-Prompt-{{version}}.md` | {{version}} |
| Line count | — | {{N}} lines |
