# Slot Injector

Renders a Slot JSON against a template (e.g. `Warm.template.md`) → final Design Prompt.

## Run

```sh
python3 inject.py \
  --slot   ../slot-examples/warm-v1.0.1.slot.json \
  --template ../templates/Warm.template.md \
  --out    /tmp/warm-rendered.md
```

`--verbose` prints token / AST / output stats to stderr.

## Self-test

```sh
python3 inject.py --selftest
```

Renders all 3 slot examples (`warm` / `theatre` / `cool`) against `Warm.template.md`, writes to `/tmp/<style>-rendered.md`, asserts verbatim segments, token values, and zero unrendered template tokens (JSX `{{ ... }}` literals are excluded from the check).

## Template syntax

| Form                                | Behavior                                           |
| ----------------------------------- | -------------------------------------------------- |
| `{{path.to.field}}`                 | Field replace (dot notation, `.N` for array index) |
| `{{#if cond}}…{{/if}}`              | Conditional block                                  |
| `{{#unless cond}}…{{/unless}}`      | Inverse conditional                                |
| `{{#each path}}…{{/each}}`          | Iteration; inside: `{{this}}` `@last` `@first` `@index` |

`cond` supports: truthy (`path`), negation (`!path`), equality (`path == "lit"`), inequality (`path != "lit"`). String literals must be double-quoted.

## Notes

- JSON parsed with `parse_float=str` to preserve source literal trailing zeros (`0.180` stays `0.180`, not `0.18`).
- String arrays (e.g. `sans_stack`) rendered as comma-separated CSS font lists; CSS generic keywords (`sans-serif`, `monospace`, `-apple-system`, …) emitted unquoted, others single-quoted.
- Literal JSX inline objects (`{{ once: true, margin: "..." }}`) are passed through unchanged. The tokenizer accepts a `{{...}}` only when the expression looks like a path (`[@A-Za-z_][@\w.\-]*`) or a block tag (`#if` / `#unless` / `#each` / closers).
- Missing fields raise `KeyError: <path>` — no silent fallback.

## Files

- `inject.py` — entry point (Python 3.11+ stdlib only)
