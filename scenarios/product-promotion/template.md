---
type: scenario-template
scenario: product-promotion
status: stub — ready for designer to fill
parent_template: ../../templates/prompt-template.md
---

# Template · product-promotion

> **Stub.** This scenario's prompt template is to be filled by the designer per [`reference/03-scenario-define.md`](../../reference/03-scenario-define.md).

## Starting point

The agnostic [`templates/prompt-template.md`](../../templates/prompt-template.md) already encodes the cross-scenario sections (Brand & Style, Colors, Typography, Spacing, Motion, three-library limit, anti-hallucination, anti-slop). **Reuse those sections as-is.**

What needs scenario-specific prose:

- §10 (Components) — reference this scenario's [`components.md`](components.md).
- §11–§13 (PATTERN block) — reference this scenario's [`PATTERN.md`](PATTERN.md) once filled.
- §16 additions — append the product-promotion-specific don'ts from [`PATTERN.md`](PATTERN.md).
- Any product-promotion-specific Hero prose (e.g. how the value-proposition headline is formatted, CTA copy rules, pricing presentation rules) — add as a small `overrides/<style>.md` patch rather than forking the agnostic template.

## Reference scenarios

[`../campaign-report/template.md`](../campaign-report/template.md) — sets the precedent of reusing the agnostic template as-is and keeping scenario-specific prose in PATTERN.md + components.md only. Follow that pattern unless evidence demands otherwise.
