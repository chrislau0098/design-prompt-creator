---
type: scenario-template
scenario: campaign-report
status: shipped
parent_template: ../../templates/prompt-template.md
---

# Template · campaign-report

> The scenario's prompt template. The campaign-report scenario **uses `templates/prompt-template.md` as-is** — the agnostic template already encodes every Design Prompt section campaign-report needs (Brand & Style, Colors, Typography, Spacing, Motion, Components, PATTERN §11–§13, Anti-slop §16, Three-library limit, Anti-hallucination).

The PATTERN block (§11–§13 + §16 additions) lives in [`PATTERN.md`](PATTERN.md). The component contract lives in [`components.md`](components.md). The injector reads both alongside the chosen Slot and the agnostic `templates/prompt-template.md` to produce the final Design Prompt md.

---

## Injection contract

When [`scripts/inject.py`](../../scripts/inject.py) renders a campaign-report Design Prompt:

1. Load the chosen Slot JSON (from `examples/vibe-view-campaign-report/slot-examples/<style>.slot.json` or a fresh extract).
2. Load the agnostic [`templates/prompt-template.md`](../../templates/prompt-template.md) and resolve every `{{slot.path}}` placeholder.
3. Splice the PATTERN block (this scenario's [`PATTERN.md`](PATTERN.md), §11–§13 + §16) into the host file at the §11–§13 / §16 positions. Host file section numbering wins; do not renumber.
4. Reference the [`components.md`](components.md) contract for §10 (Components) — only components listed there may appear in the rendered output.

If a future style demands campaign-report-specific prompt language **beyond** the agnostic template (for example a Hero chapter that needs a scenario-specific eyebrow rule), add a small `overrides/<style>.md` patch next to the Slot file rather than forking this template. Forking creates drift; patches stay reviewable.

---

## Why no scenario-specific prose here

Campaign-report's specificity is encoded in three places, all already covered:

- **PATTERN.md** carries the chapter cadence, archetype catalogue, treatment rules, rhythm discipline, anatomy.
- **components.md** carries the component contract, props, DOM, adaptive states, bans.
- The agnostic template carries the cross-scenario Design Prompt scaffolding (Brand & Style header, Colors, Typography, Spacing, Motion, three-library limit, anti-hallucination block).

Adding more prose here would duplicate one of the three. The reference Design Prompts at [`../../examples/vibe-view-campaign-report/design-prompts/`](../../examples/vibe-view-campaign-report/design-prompts/) (6 styles, all ≤ 620 lines) confirm the agnostic template plus this scenario's PATTERN and components is sufficient.
