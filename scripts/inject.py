#!/usr/bin/env python3
"""Slot injector — render a Slot JSON against Warm.template.md (or any compatible template).

Template syntax supported:
  {{path.to.field}}                          — field replace (dot notation, .N for array index)
  {{#if cond}}...{{/if}}                     — conditional (truthy / "==" / "!=" / "!" negation)
  {{#unless cond}}...{{/unless}}             — inverse conditional (same cond grammar)
  {{#each path}}...{{/each}}                 — array iteration ({{this}}, @last, @first, @index)
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any


# ──────────────────────────────────────────────────────────────────────────
# Path resolution


CSS_GENERIC_FONT_KEYWORDS = {
    "sans-serif", "serif", "monospace", "cursive", "fantasy",
    "system-ui", "ui-sans-serif", "ui-serif", "ui-monospace",
    "ui-rounded", "-apple-system", "BlinkMacSystemFont", "inherit",
    "initial", "unset", "revert",
}


def _resolve(path: str, scope_stack: list[dict]):
    """Resolve dot-notated path against scope stack (top of stack = innermost each)."""
    parts = path.split(".")
    # Try each scope from innermost to outermost
    for scope in reversed(scope_stack):
        if not isinstance(scope, dict):
            continue
        # Special keys live only in the innermost each scope
        if parts[0] in scope:
            cur: Any = scope[parts[0]]
        else:
            continue
        try:
            for p in parts[1:]:
                if isinstance(cur, list):
                    cur = cur[int(p)]
                elif isinstance(cur, dict):
                    cur = cur[p]
                else:
                    raise KeyError(p)
            return cur
        except (KeyError, IndexError, ValueError):
            continue
    raise KeyError(path)


_MISSING = object()


def _try_resolve(path: str, scope_stack: list[dict]):
    try:
        return _resolve(path, scope_stack)
    except KeyError:
        return _MISSING


# ──────────────────────────────────────────────────────────────────────────
# Tokenizer / Parser


TOKEN_RE = re.compile(
    r"\{\{\s*"
    r"(?P<kind>#if\s+|#unless\s+|#each\s+|/if|/unless|/each|)"
    r"(?P<expr>[^{}]*?)"
    r"\s*\}\}"
)


class Node:
    pass


class TextNode(Node):
    __slots__ = ("text",)

    def __init__(self, text: str):
        self.text = text


class FieldNode(Node):
    __slots__ = ("expr",)

    def __init__(self, expr: str):
        self.expr = expr


class IfNode(Node):
    __slots__ = ("cond", "children", "negate")

    def __init__(self, cond: str, children: list[Node], negate: bool = False):
        self.cond = cond
        self.children = children
        self.negate = negate


class EachNode(Node):
    __slots__ = ("path", "children")

    def __init__(self, path: str, children: list[Node]):
        self.path = path
        self.children = children


def _is_template_token(kind_raw: str, expr: str) -> bool:
    """Decide whether a {{...}} match is a real template token or literal JSX `{{ obj }}`.

    Heuristic: tokens are dot-paths, `this`, `@last`/`@first`/`@index`, or block tags
    (`#if`/`#unless`/`#each`/`/if`/`/unless`/`/each`). JSX inline objects always
    contain a `:` (key:value) and start with a space then identifier. The simplest
    reliable rule:
      - block tags (#if/#unless/#each/closers) → token
      - bare expr matches `[A-Za-z_@][\w.@-]*` (optionally with `== "lit"` / `!= "lit"`
        or `!` negation prefix) → token
      - anything else (JSX inline object literal etc.) → text
    """
    if kind_raw in {"#if", "#unless", "#each", "/if", "/unless", "/each"}:
        return True
    # Bare field: must be a path-like expression
    if not expr:
        return False
    return bool(_FIELD_EXPR_RE.match(expr))


_FIELD_EXPR_RE = re.compile(r"^[@A-Za-z_][@\w.\-]*$")


def tokenize(src: str) -> list[tuple[str, str, int]]:
    """Return list of (kind, expr, pos). 'kind' is one of: text, field, if, unless, each, /if, /unless, /each.

    Non-template `{{...}}` (JSX inline object literals) are absorbed back into text.
    """
    tokens: list[tuple[str, str, int]] = []
    pos = 0
    for m in TOKEN_RE.finditer(src):
        kind_raw = m.group("kind").strip()
        expr = m.group("expr").strip()
        if not _is_template_token(kind_raw, expr):
            # Treat as literal — let the surrounding text absorb it
            continue
        start = m.start()
        if start > pos:
            tokens.append(("text", src[pos:start], pos))
        if kind_raw == "":
            tokens.append(("field", expr, start))
        elif kind_raw == "#if":
            tokens.append(("if", expr, start))
        elif kind_raw == "#unless":
            tokens.append(("unless", expr, start))
        elif kind_raw == "#each":
            tokens.append(("each", expr, start))
        elif kind_raw == "/if":
            tokens.append(("/if", "", start))
        elif kind_raw == "/unless":
            tokens.append(("/unless", "", start))
        elif kind_raw == "/each":
            tokens.append(("/each", "", start))
        else:
            raise SyntaxError(f"Unknown tag {kind_raw!r} at pos {start}")
        pos = m.end()
    if pos < len(src):
        tokens.append(("text", src[pos:], pos))
    return tokens


def parse(tokens: list[tuple[str, str, int]]) -> list[Node]:
    """Build AST from tokens. Returns root list of nodes."""
    idx = [0]

    def line_of(pos: int, src_ref=[None]) -> int:
        # Simple: not super precise but enough for error messages
        return pos  # placeholder; we report token pos

    def parse_block(stop_kinds: set[str]) -> list[Node]:
        out: list[Node] = []
        while idx[0] < len(tokens):
            kind, expr, pos = tokens[idx[0]]
            if kind in stop_kinds:
                return out
            idx[0] += 1
            if kind == "text":
                out.append(TextNode(expr))
            elif kind == "field":
                out.append(FieldNode(expr))
            elif kind == "if":
                children = parse_block({"/if"})
                if idx[0] >= len(tokens) or tokens[idx[0]][0] != "/if":
                    raise SyntaxError(f"Unclosed #if {expr!r} at pos {pos}")
                idx[0] += 1
                out.append(IfNode(expr, children, negate=False))
            elif kind == "unless":
                children = parse_block({"/unless"})
                if idx[0] >= len(tokens) or tokens[idx[0]][0] != "/unless":
                    raise SyntaxError(f"Unclosed #unless {expr!r} at pos {pos}")
                idx[0] += 1
                out.append(IfNode(expr, children, negate=True))
            elif kind == "each":
                children = parse_block({"/each"})
                if idx[0] >= len(tokens) or tokens[idx[0]][0] != "/each":
                    raise SyntaxError(f"Unclosed #each {expr!r} at pos {pos}")
                idx[0] += 1
                out.append(EachNode(expr, children))
            else:
                raise SyntaxError(f"Unexpected close tag {kind!r} at pos {pos}")
        return out

    return parse_block(set())


# ──────────────────────────────────────────────────────────────────────────
# Condition evaluator


COND_CMP_RE = re.compile(r'^(?P<lhs>[^=!]+?)\s*(?P<op>==|!=)\s*(?P<rhs>.+)$')


def _parse_literal(s: str):
    s = s.strip()
    if (s.startswith('"') and s.endswith('"')) or (s.startswith("'") and s.endswith("'")):
        return s[1:-1]
    if s == "null":
        return None
    if s == "true":
        return True
    if s == "false":
        return False
    try:
        if "." in s:
            return float(s)
        return int(s)
    except ValueError:
        return s


def _is_truthy(v: Any) -> bool:
    if v is None or v is False:
        return False
    if v is True:
        return True
    if isinstance(v, (int, float)):
        return v != 0
    if isinstance(v, str):
        return len(v) > 0
    if isinstance(v, (list, tuple, dict)):
        return len(v) > 0
    return bool(v)


def eval_cond(expr: str, scope_stack: list[dict]) -> bool:
    expr = expr.strip()
    # Negation
    if expr.startswith("!"):
        return not eval_cond(expr[1:].strip(), scope_stack)
    # Comparison
    m = COND_CMP_RE.match(expr)
    if m:
        lhs_path = m.group("lhs").strip()
        op = m.group("op")
        rhs_lit = _parse_literal(m.group("rhs").strip())
        lhs_val = _try_resolve(lhs_path, scope_stack)
        if lhs_val is _MISSING:
            lhs_val = None
        result = (lhs_val == rhs_lit)
        return result if op == "==" else not result
    # Truthy
    v = _try_resolve(expr, scope_stack)
    if v is _MISSING:
        return False
    return _is_truthy(v)


# ──────────────────────────────────────────────────────────────────────────
# Renderer


def _fmt_value(v: Any, path: str) -> str:
    """Render a leaf value as a string. None → empty string(避免 "null" 字面拼进 prose / CSS,P0-1 fix 2026-05-21)。
    模板应配合在 null 字段处用 {{#if X}}...{{/if}} 包条件块,以避免空字符串导致语法残破。"""
    if v is None:
        return ""
    if v is True:
        return "true"
    if v is False:
        return "false"
    if isinstance(v, float):
        # Avoid trailing .0 noise but keep precision when meaningful
        if v == int(v) and abs(v) < 1e15:
            # Integer-valued float: drop decimal only if input JSON wrote it as int-looking
            # In practice the SoT shows raw values (e.g. 80, 0.962, 1.6). Use repr-ish.
            text = repr(v)
            if text.endswith(".0"):
                text = text[:-2]
            return text
        return repr(v)
    if isinstance(v, int):
        return str(v)
    if isinstance(v, str):
        return v
    if isinstance(v, list):
        # Array-as-field renders as font-stack-style (CSS comma list)
        return _fmt_font_stack(v)
    if isinstance(v, dict):
        # Dict as field — render JSON. Rare; tooling.paper_shaders.banned never used as field
        return json.dumps(v, ensure_ascii=False)
    return str(v)


def _fmt_font_stack(items: list) -> str:
    """Render array as comma-separated CSS-style list — single-quote font names, leave generic keywords bare."""
    parts: list[str] = []
    for it in items:
        if isinstance(it, str):
            if it in CSS_GENERIC_FONT_KEYWORDS:
                parts.append(it)
            else:
                parts.append(f"'{it}'")
        else:
            parts.append(str(it))
    return ", ".join(parts)


def render(nodes: list[Node], scope_stack: list[dict], verbose: bool = False) -> str:
    out: list[str] = []
    for node in nodes:
        if isinstance(node, TextNode):
            out.append(node.text)
        elif isinstance(node, FieldNode):
            val = _try_resolve(node.expr, scope_stack)
            if val is _MISSING:
                raise KeyError(f"Field {node.expr!r} not found in slot")
            out.append(_fmt_value(val, node.expr))
        elif isinstance(node, IfNode):
            cond = eval_cond(node.cond, scope_stack)
            if node.negate:
                cond = not cond
            if cond:
                out.append(render(node.children, scope_stack, verbose))
        elif isinstance(node, EachNode):
            arr = _try_resolve(node.path, scope_stack)
            if arr is _MISSING:
                raise KeyError(f"Each path {node.path!r} not found in slot")
            if not isinstance(arr, list):
                raise TypeError(f"Each path {node.path!r} is not a list (got {type(arr).__name__})")
            n = len(arr)
            for i, item in enumerate(arr):
                iter_scope = {
                    "this": item,
                    "@index": i,
                    "@first": (i == 0),
                    "@last": (i == n - 1),
                }
                out.append(render(node.children, scope_stack + [iter_scope], verbose))
        else:
            raise TypeError(f"Unknown node {type(node).__name__}")
    return "".join(out)


# ──────────────────────────────────────────────────────────────────────────
# CLI


def inject(slot_path: Path, template_path: Path, out_path: Path, verbose: bool = False) -> str:
    # parse_float=str preserves source literal trailing zeros (e.g. 0.180 stays "0.180")
    slot = json.loads(slot_path.read_text(encoding="utf-8"), parse_float=str)
    template = template_path.read_text(encoding="utf-8")
    tokens = tokenize(template)
    if verbose:
        print(f"[trace] tokens: {len(tokens)}", file=sys.stderr)
    ast = parse(tokens)
    if verbose:
        print(f"[trace] AST nodes: {len(ast)} top-level", file=sys.stderr)
    rendered = render(ast, [slot], verbose=verbose)
    out_path.write_text(rendered, encoding="utf-8")
    if verbose:
        print(f"[trace] wrote {out_path} ({len(rendered)} chars, {rendered.count(chr(10)) + 1} lines)", file=sys.stderr)
    return rendered


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description="Inject Slot JSON into Warm.template.md")
    p.add_argument("--slot", type=Path)
    p.add_argument("--template", type=Path)
    p.add_argument("--out", type=Path)
    p.add_argument("--verbose", action="store_true")
    p.add_argument("--selftest", action="store_true", help="Run self-tests instead of normal injection")
    args = p.parse_args(argv)

    if args.selftest:
        return _run_selftests()

    if not (args.slot and args.template and args.out):
        p.error("--slot, --template, --out are required (unless --selftest)")
    inject(args.slot, args.template, args.out, verbose=args.verbose)
    return 0


# ──────────────────────────────────────────────────────────────────────────
# Self-tests


FRAMEWORK = Path(__file__).resolve().parent.parent
TEMPLATE = FRAMEWORK / "templates" / "Warm.template.md"
SLOT_DIR = FRAMEWORK / "slot-examples"
SOT_DIR = FRAMEWORK.parent / "Warm Restraint Tech"


def _count_unrendered_template_tokens(rendered: str) -> int:
    """Count {{...}} that look like template tokens (path/block tag), not JSX literals."""
    n = 0
    for m in TOKEN_RE.finditer(rendered):
        kind = m.group("kind").strip()
        expr = m.group("expr").strip()
        if _is_template_token(kind, expr):
            n += 1
    return n


def _check_warm(rendered: str) -> dict:
    rep: dict = {}
    rep["lines"] = rendered.count("\n") + 1
    rep["count_story_data"] = rendered.count("This page is a story told in data")
    rep["count_parseDisplayValue"] = rendered.count("parseDisplayValue")
    rep["count_isAnimationActive_false"] = rendered.count("isAnimationActive={false}")
    rep["count_component_constraints"] = rendered.count("## 18. Component Constraints")
    rep["count_oklch_bg"] = rendered.count("oklch(0.962 0.003 80)")
    rep["count_brand_hue"] = rendered.count("--brand-hue: 50")
    rep["count_chart2"] = rendered.count("oklch(0.620 0.130 var(--brand-hue))")
    rep["unrendered_tokens"] = _count_unrendered_template_tokens(rendered)
    rep["pass"] = (
        rep["count_story_data"] == 1
        and rep["count_parseDisplayValue"] >= 5
        and rep["count_isAnimationActive_false"] >= 1
        and rep["count_component_constraints"] == 1
        and rep["count_oklch_bg"] >= 1
        and rep["count_brand_hue"] == 1
        and rep["count_chart2"] == 1
        and rep["unrendered_tokens"] == 0
    )
    return rep


def _check_theatre(rendered: str) -> dict:
    rep: dict = {}
    rep["lines"] = rendered.count("\n") + 1
    rep["count_brand_hue"] = rendered.count("--brand-hue: 42")
    rep["count_chart2"] = rendered.count("oklch(0.530 0.150 var(--brand-hue))")
    rep["count_meshgradient"] = rendered.count("MeshGradient")
    rep["unrendered_tokens"] = _count_unrendered_template_tokens(rendered)
    rep["pass"] = (
        rep["count_brand_hue"] == 1
        and rep["count_chart2"] == 1
        and rep["count_meshgradient"] >= 1
        and rep["unrendered_tokens"] == 0
    )
    return rep


def _check_cool(rendered: str) -> dict:
    rep: dict = {}
    rep["lines"] = rendered.count("\n") + 1
    rep["count_brand_hue"] = rendered.count("--brand-hue: 262")
    rep["count_godrays"] = rendered.count("GodRays")
    rep["unrendered_tokens"] = _count_unrendered_template_tokens(rendered)
    rep["pass"] = (
        rep["count_brand_hue"] == 1
        and rep["count_godrays"] >= 1
        and rep["unrendered_tokens"] == 0
    )
    return rep


def _run_selftests() -> int:
    import tempfile

    results = []
    for name, slot_file, checker, sot_file in [
        ("warm", "warm-v1.0.1.slot.json", _check_warm, "warm-restraint-tech-Design-Prompt-v1.0.1.md"),
        ("theatre", "theatre-v6.7.1.slot.json", _check_theatre, None),
        ("cool", "cool-v0.5.1.slot.json", _check_cool, None),
    ]:
        slot = SLOT_DIR / slot_file
        out = Path(tempfile.gettempdir()) / f"{name}-rendered.md"
        try:
            rendered = inject(slot, TEMPLATE, out, verbose=False)
        except Exception as exc:  # noqa: BLE001
            print(f"[{name}] FAIL: {exc}", file=sys.stderr)
            results.append((name, False, {"error": str(exc)}))
            continue
        rep = checker(rendered)
        if sot_file is not None:
            sot_path = SOT_DIR / sot_file
            if sot_path.exists():
                sot_lines = sot_path.read_text(encoding="utf-8").count("\n") + 1
                rep["sot_lines"] = sot_lines
                rep["line_diff"] = rep["lines"] - sot_lines
        print(f"[{name}] {'PASS' if rep['pass'] else 'FAIL'} {rep}")
        results.append((name, rep["pass"], rep))

    all_pass = all(r[1] for r in results)
    return 0 if all_pass else 1


if __name__ == "__main__":
    sys.exit(main())
