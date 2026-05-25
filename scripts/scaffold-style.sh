#!/usr/bin/env bash
# scaffold-style.sh — add a new style Slot to an existing scenario
#
# Usage:
#   ./scaffold-style.sh --style <handle> --scenario <name> --project <path>
#
# Example:
#   ./scaffold-style.sh --style "warm-editorial" --scenario "campaign-report" --project ~/Code/my-report

set -euo pipefail

# ── Defaults ──────────────────────────────────────────────────────────────────
STYLE_HANDLE=""
SCENARIO=""
PROJECT=""

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TEMPLATES_DIR="$(cd "$SCRIPT_DIR/../templates" && pwd)"

# ── Argument parsing ──────────────────────────────────────────────────────────
while [[ $# -gt 0 ]]; do
    case "$1" in
        --style)
            STYLE_HANDLE="$2"
            shift 2
            ;;
        --scenario)
            SCENARIO="$2"
            shift 2
            ;;
        --project)
            PROJECT="$2"
            shift 2
            ;;
        -h|--help)
            echo "Usage: $0 --style <handle> --scenario <name> --project <path>"
            exit 0
            ;;
        *)
            echo "Unknown argument: $1" >&2
            exit 1
            ;;
    esac
done

# ── Validation ────────────────────────────────────────────────────────────────
if [[ -z "$STYLE_HANDLE" || -z "$SCENARIO" || -z "$PROJECT" ]]; then
    echo "Error: --style, --scenario, and --project are all required." >&2
    echo "Usage: $0 --style <handle> --scenario <name> --project <path>" >&2
    exit 1
fi

if [[ ! -d "$PROJECT" ]]; then
    echo "Error: project directory does not exist: $PROJECT" >&2
    exit 1
fi

SCENARIO_DIR="$PROJECT/scenarios/$SCENARIO"
if [[ ! -d "$SCENARIO_DIR" ]]; then
    echo "Error: scenario directory does not exist: $SCENARIO_DIR" >&2
    echo "Run scaffold-scenario.sh first." >&2
    exit 1
fi

SLOT_DIR="$SCENARIO_DIR/slot-examples"
SLOT_PATH="$SLOT_DIR/$STYLE_HANDLE.slot.json"

if [[ -e "$SLOT_PATH" ]]; then
    echo "Error: slot already exists: $SLOT_PATH" >&2
    exit 1
fi

# ── Copy and initialize Slot template ─────────────────────────────────────────
echo "Creating slot: $SLOT_PATH"
mkdir -p "$SLOT_DIR"
cp "$TEMPLATES_DIR/Slot.template.json" "$SLOT_PATH"

# Inject handle and scenario placeholder values using sed
# (Does not fill design values — that's a human/AI task)
sed -i '' \
    -e "s/{{style-handle-kebab}}/$STYLE_HANDLE/g" \
    "$SLOT_PATH"

# ── Summary ───────────────────────────────────────────────────────────────────
echo ""
echo "Slot created: $SLOT_PATH"
echo ""
echo "Fields to fill (in order):"
echo ""
echo "  1. style_meta:"
echo "     - style_name        ← human-readable name, e.g. \"Warm Editorial · Amber\""
echo "     - mode              ← \"light\" or \"dark\""
echo "     - brand_hue         ← OKLCH hue integer (0–360), e.g. 50"
echo "     - mood_adjectives   ← 4 descriptive words"
echo "     - proposition       ← one paragraph: background tone, typography, accent, decoration"
echo "     - decorative_pack   ← editorial | theatrical | instrumental | systematic | festive-royal | festive-editorial"
echo "     - focal_numeral_strategy ← primary_on_neutral | primary_on_primary | foreground_with_primary_signal"
echo ""
echo "  2. atomic.color:"
echo "     - neutral_hue       ← hue for background/surface/border tokens (often = brand_hue)"
echo "     - background / surface_l1..l3 / foreground / foreground_2..3 / border / border_strong"
echo "     - primary (L, C)    ← brand accent lightness + chroma"
echo "     - primary_hl (L, C) ← lighter variant for units/deltas"
echo "     - chart_ramp        ← 4 L/C steps for chart-2 through chart-5"
echo ""
echo "  3. atomic.typography:"
echo "     - sans_stack / display_stack / mono_stack ← font family arrays"
echo "     - weight_ceiling    ← 500 | 600 | 700 | 800"
echo "     - display_number_lg / display_number_mobile / section_primary_lg etc."
echo ""
echo "  4. molecular:"
echo "     - hero_shader       ← null (no WebGL) or { component, props }"
echo "     - hero_geometry.default_treatment ← typographic-field | full-bleed-monolith | asymmetric-split"
echo "     - dividers.chapter_opener ← hairline-banner | stamp-badge | seal-stamp | numeral-large"
echo ""
echo "  5. tooling.paper_shaders.primary ← null or shader component name if hero_shader is set"
echo ""
echo "After filling, verify with:"
echo "  python3 scripts/inject.py \\"
echo "    --slot $SLOT_PATH \\"
echo "    --template $SCENARIO_DIR/prompt-template.md \\"
echo "    --out $SCENARIO_DIR/Design-Prompt-draft.md"
echo ""
echo "Then run:"
echo "  python3 scripts/verify-three-way-sync.py $PROJECT $SCENARIO $STYLE_HANDLE"
