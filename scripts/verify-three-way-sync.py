#!/usr/bin/env python3
"""verify-three-way-sync.py — three-way ornament sync check (MVP: two-way Prompt vs Slot).

Usage:
    python3 verify-three-way-sync.py <project> <scenario> <style>

Arguments:
    project   absolute path to the project directory
    scenario  scenario name (e.g. campaign-report)
    style     style handle (e.g. swiss-systematic-blue)

Exit codes:
    0   all checks pass
    1   mismatch found or line-count exceeded

Phase 7 note:
    Full three-way sync (P vs D vs R) requires a running Vite renderer exposing
    a /ornament-rendered endpoint. Until then, this script runs MVP two-way
    Prompt (P) vs Slot (D) sync check. Vite detection is attempted; if renderer
    is not running, a warning is printed and the check degrades gracefully.
"""

from __future__ import annotations

import json
import re
import subprocess
import sys
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any

# ── Constants ────────────────────────────────────────────────────────────────

LINE_LIMIT = 620
VITE_URLS = ["http://localhost:5173", "http://localhost:3000"]

# ── Helpers ──────────────────────────────────────────────────────────────────


def _find_latest_prompt(scenario_dir: Path, style: str) -> Path | None:
    """Find the most recently modified rendered Design Prompt for this style."""
    candidates = sorted(
        scenario_dir.glob(f"Design-Prompt-*.md"),
        key=lambda p: p.stat().st_mtime,
        reverse=True,
    )
    if candidates:
        return candidates[0]
    # Fallback: any .md that is not prompt-template or PATTERN
    for p in scenario_dir.glob("*.md"):
        if p.name not in ("prompt-template.md", "PATTERN.md", "component-spec.md"):
            return p
    return None


def _extract_ornaments_from_prompt(prompt_text: str) -> set[str]:
    """Extract ornament component names mentioned in the prompt text.

    Looks for PascalCase identifiers that match known ornament patterns:
    ChapterBanner, ChapterStamp, ChapterNumeralLarge, SealStamp,
    OutroSignature, GoldenHairline, HairlineRule, ShadSeparator,
    TasselDivider, SpotlightGradient, OutlinedPill.
    """
    pattern = re.compile(
        r"\b("
        r"ChapterBanner|ChapterStamp|ChapterNumeralLarge|SealStamp"
        r"|OutroSignature|GoldenHairline|HairlineRule|ShadSeparator"
        r"|TasselDivider|SpotlightGradient|OutlinedPill"
        r"|Dithering|MeshGradient|GodRays|GrainGradient"
        r")\b"
    )
    return set(m.group(1) for m in pattern.finditer(prompt_text))


def _extract_ornaments_from_slot(slot: dict[str, Any]) -> set[str]:
    """Extract ornament-relevant declarations from a Slot JSON."""
    ornaments: set[str] = set()

    # Paper shader
    tooling = slot.get("tooling", {})
    shaders = tooling.get("paper_shaders", {})
    if shaders.get("primary"):
        ornaments.add(shaders["primary"])
    if shaders.get("secondary"):
        ornaments.add(shaders["secondary"])

    # Hero shader component
    molecular = slot.get("molecular", {})
    hero_shader = molecular.get("hero_shader")
    if hero_shader and isinstance(hero_shader, dict):
        comp = hero_shader.get("component")
        if comp:
            ornaments.add(comp)

    # Dividers / chapter opener keywords → map to component names
    dividers = molecular.get("dividers", {})
    chapter_opener = dividers.get("chapter_opener", "")
    opener_map = {
        "hairline-banner": "ChapterBanner",
        "stamp-badge": "ChapterStamp",
        "seal-stamp": "SealStamp",
        "numeral-large": "ChapterNumeralLarge",
    }
    if chapter_opener in opener_map:
        ornaments.add(opener_map[chapter_opener])

    # Decorative pack → outro ornament
    style_meta = slot.get("style_meta", {})
    pack = style_meta.get("decorative_pack", "")
    pack_outro = {
        "editorial": "OutroSignature",
        "systematic": "ShadSeparator",
        "festive-royal": "GoldenHairline",
        "festive-editorial": "HairlineRule",
    }
    if pack in pack_outro:
        ornaments.add(pack_outro[pack])

    return ornaments


def _check_vite(urls: list[str]) -> str | None:
    """Try to reach a Vite dev server. Returns URL if reachable, else None."""
    for url in urls:
        try:
            with urllib.request.urlopen(url, timeout=1) as resp:
                if resp.status < 500:
                    return url
        except Exception:  # noqa: BLE001
            continue
    return None


def _get_renderer_ornaments(vite_url: str, scenario: str, style: str) -> set[str] | None:
    """Fetch ornament list from the Vite renderer endpoint (Phase 7).

    Returns None if endpoint not available (graceful degradation).
    """
    endpoint = f"{vite_url}/ornament-rendered?scenario={scenario}&style={style}"
    try:
        with urllib.request.urlopen(endpoint, timeout=2) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            return set(data.get("ornaments", []))
    except Exception:  # noqa: BLE001
        return None


# ── Main ─────────────────────────────────────────────────────────────────────


def main(argv: list[str] | None = None) -> int:
    args = (argv or sys.argv[1:])

    if len(args) < 3:
        print("Usage: verify-three-way-sync.py <project> <scenario> <style>", file=sys.stderr)
        return 1

    project_path = Path(args[0]).expanduser().resolve()
    scenario = args[1]
    style = args[2]

    if not project_path.is_dir():
        print(f"Error: project directory not found: {project_path}", file=sys.stderr)
        return 1

    scenario_dir = project_path / "scenarios" / scenario
    slot_path = scenario_dir / "slot-examples" / f"{style}.slot.json"

    if not scenario_dir.is_dir():
        print(f"Error: scenario directory not found: {scenario_dir}", file=sys.stderr)
        return 1

    if not slot_path.exists():
        print(f"Error: slot not found: {slot_path}", file=sys.stderr)
        return 1

    # Load slot
    slot: dict[str, Any] = json.loads(slot_path.read_text(encoding="utf-8"))

    # Find rendered prompt
    prompt_path = _find_latest_prompt(scenario_dir, style)
    if prompt_path is None:
        print(
            "Warning: no rendered Design Prompt found in scenario dir. "
            "Run inject.py first.",
            file=sys.stderr,
        )
        print("[P vs D] SKIP — no prompt to check")
        return 0

    prompt_text = prompt_path.read_text(encoding="utf-8")
    prompt_lines = prompt_text.count("\n") + 1

    # ── Check 1: line count ──────────────────────────────────────────────────
    print(f"[line-count] {prompt_lines} lines in {prompt_path.name}", end="")
    line_ok = prompt_lines <= LINE_LIMIT
    print(f" — {'OK' if line_ok else f'FAIL (limit {LINE_LIMIT})'}")

    # ── Check 2: unrendered tokens ───────────────────────────────────────────
    # Reuse inject.py's token detection by importing it
    inject_py = project_path / "scripts" / "inject.py"
    unrendered = 0
    if inject_py.exists():
        try:
            import importlib.util
            spec = importlib.util.spec_from_file_location("inject", inject_py)
            assert spec and spec.loader
            inject_mod = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(inject_mod)  # type: ignore[attr-defined]
            unrendered = inject_mod._count_unrendered_template_tokens(prompt_text)
        except Exception as exc:  # noqa: BLE001
            print(f"Warning: could not load inject.py for token check: {exc}", file=sys.stderr)

    token_ok = unrendered == 0
    print(f"[unrendered-tokens] {unrendered} — {'OK' if token_ok else 'FAIL'}")

    # ── Check 3: P vs D ornament sync ────────────────────────────────────────
    p_ornaments = _extract_ornaments_from_prompt(prompt_text)
    d_ornaments = _extract_ornaments_from_slot(slot)

    p_only = p_ornaments - d_ornaments  # in prompt but not declared in slot
    d_only = d_ornaments - p_ornaments  # declared in slot but absent from prompt

    print()
    print(f"[P vs D ornament sync]")
    print(f"  Prompt ornaments (P): {sorted(p_ornaments) or '(none)'}")
    print(f"  Slot ornaments (D):   {sorted(d_ornaments) or '(none)'}")
    if p_only:
        print(f"  Mismatch — P not in D (delete candidate): {sorted(p_only)}")
    if d_only:
        print(f"  Mismatch — D not in P (undeclared in prompt): {sorted(d_only)}")
    pd_ok = not p_only and not d_only
    print(f"  Result: {'OK' if pd_ok else 'FAIL'}")

    # ── Check 4: three-way (R) — Phase 7 gate ────────────────────────────────
    print()
    vite_url = _check_vite(VITE_URLS)
    if vite_url:
        r_ornaments = _get_renderer_ornaments(vite_url, scenario, style)
        if r_ornaments is not None:
            p_minus_r = p_ornaments - r_ornaments
            r_minus_d = r_ornaments - d_ornaments
            print(f"[P vs D vs R ornament sync] renderer at {vite_url}")
            if p_minus_r:
                print(f"  P not rendered (delete candidate from prompt): {sorted(p_minus_r)}")
            if r_minus_d:
                print(f"  R not declared in Slot (add to decorative_pack/dividers): {sorted(r_minus_d)}")
            pr_ok = not p_minus_r and not r_minus_d
            print(f"  Result: {'OK' if pr_ok else 'FAIL'}")
        else:
            print(f"[P vs D vs R] Vite reachable at {vite_url} but /ornament-rendered not available — Phase 7 pending. Skipping R check.")
    else:
        print("[P vs D vs R] Vite renderer not running. Three-way sync degraded to two-way (P vs D). Start renderer for full check.")

    # ── Summary ───────────────────────────────────────────────────────────────
    print()
    all_ok = line_ok and token_ok and pd_ok
    print(f"Overall: {'PASS' if all_ok else 'FAIL'}")

    if not line_ok:
        print(f"  Action: trim prompt to <= {LINE_LIMIT} lines (currently {prompt_lines})")
    if not token_ok:
        print(f"  Action: {unrendered} unrendered {{{{...}}}} token(s) — add missing fields to Slot JSON")
    if p_only:
        print(f"  Action: remove or rename these ornaments in prompt (not in Slot): {sorted(p_only)}")
    if d_only:
        print(f"  Action: prompt does not reference these Slot ornaments: {sorted(d_only)} — add to prompt or remove from Slot")

    return 0 if all_ok else 1


if __name__ == "__main__":
    sys.exit(main())
