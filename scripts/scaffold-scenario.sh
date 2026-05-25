#!/usr/bin/env bash
# scaffold-scenario.sh — add a new scenario to an existing project
#
# Usage:
#   ./scaffold-scenario.sh --scenario <name> --project <path>
#
# Example:
#   ./scaffold-scenario.sh --scenario "leaderboard" --project ~/Code/my-report

set -euo pipefail

# ── Defaults ──────────────────────────────────────────────────────────────────
SCENARIO=""
PROJECT=""

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TEMPLATES_DIR="$(cd "$SCRIPT_DIR/../templates" && pwd)"

# ── Argument parsing ──────────────────────────────────────────────────────────
while [[ $# -gt 0 ]]; do
    case "$1" in
        --scenario)
            SCENARIO="$2"
            shift 2
            ;;
        --project)
            PROJECT="$2"
            shift 2
            ;;
        -h|--help)
            echo "Usage: $0 --scenario <name> --project <path>"
            exit 0
            ;;
        *)
            echo "Unknown argument: $1" >&2
            exit 1
            ;;
    esac
done

# ── Validation ────────────────────────────────────────────────────────────────
if [[ -z "$SCENARIO" || -z "$PROJECT" ]]; then
    echo "Error: --scenario and --project are both required." >&2
    echo "Usage: $0 --scenario <name> --project <path>" >&2
    exit 1
fi

if [[ ! -d "$PROJECT" ]]; then
    echo "Error: project directory does not exist: $PROJECT" >&2
    exit 1
fi

SCENARIO_DIR="$PROJECT/scenarios/$SCENARIO"

if [[ -e "$SCENARIO_DIR" ]]; then
    echo "Error: scenario already exists: $SCENARIO_DIR" >&2
    exit 1
fi

TODAY="$(date +%Y-%m-%d)"

# Infer project name from AGENTS.md if present
PROJECT_NAME="$SCENARIO"
if [[ -f "$PROJECT/AGENTS.md" ]]; then
    INFERRED=$(grep -m1 "^project_name:" "$PROJECT/AGENTS.md" 2>/dev/null | sed 's/project_name: *"\{0,1\}//;s/"\{0,1\} *$//' || true)
    if [[ -n "$INFERRED" ]]; then
        PROJECT_NAME="$INFERRED"
    fi
fi

# ── Create scenario directory ─────────────────────────────────────────────────
echo "Creating scenario: $SCENARIO_DIR"
mkdir -p "$SCENARIO_DIR/slot-examples"

# ── Copy templates ─────────────────────────────────────────────────────────────
cp "$TEMPLATES_DIR/prompt-template.md" "$SCENARIO_DIR/prompt-template.md"

cp "$TEMPLATES_DIR/PATTERN.template.md" "$SCENARIO_DIR/PATTERN.md"
sed -i '' \
    -e "s/{{project}}/$PROJECT_NAME/g" \
    -e "s/{{scenario}}/$SCENARIO/g" \
    -e "s/{{created}}/$TODAY/g" \
    "$SCENARIO_DIR/PATTERN.md"

cp "$TEMPLATES_DIR/component-spec.template.md" "$SCENARIO_DIR/component-spec.md"
sed -i '' \
    -e "s/{{project_name}}/$PROJECT_NAME/g" \
    -e "s/{{scenario}}/$SCENARIO/g" \
    -e "s/{{YYYY-MM-DD}}/$TODAY/g" \
    "$SCENARIO_DIR/component-spec.md"

# ── Summary ───────────────────────────────────────────────────────────────────
echo ""
echo "Scenario scaffolded: $SCENARIO_DIR"
echo ""
echo "Files created:"
echo "  $SCENARIO_DIR/prompt-template.md  ← injection template (do not edit)"
echo "  $SCENARIO_DIR/PATTERN.md          ← edit §11-§13 for this scenario's archetypes"
echo "  $SCENARIO_DIR/component-spec.md   ← edit required/optional/banned component lists"
echo "  $SCENARIO_DIR/slot-examples/      ← place .slot.json files here"
echo ""
echo "Next steps:"
echo "  1. Edit PATTERN.md — add scenario-specific archetypes under §11.3"
echo "  2. Edit component-spec.md — update required/optional/banned lists"
echo "  3. Add a style slot:"
echo "       ./scripts/scaffold-style.sh --style <handle> --scenario $SCENARIO --project $PROJECT"
