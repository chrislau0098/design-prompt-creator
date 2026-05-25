#!/usr/bin/env bash
# scaffold-project.sh — create a new design-prompt project from templates
#
# Usage:
#   ./scaffold-project.sh --name <project> --scenario <scenario> --dest <path> [--renderer-repo <url>] [--no-renderer]
#
# Example:
#   ./scaffold-project.sh --name "my-report" --scenario "campaign-report" --dest ~/Documents/my-report
#
# Renderer (preview tool) is cloned to <dest>/design-prompt-management/ by default;
# override with --renderer-repo or skip with --no-renderer.

set -euo pipefail

# ── Defaults ──────────────────────────────────────────────────────────────────
PROJECT_NAME=""
SCENARIO=""
DEST=""
RENDERER_REPO="https://github.com/chrislau0098/design-prompt-management.git"
CLONE_RENDERER=1

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TEMPLATES_DIR="$(cd "$SCRIPT_DIR/../templates" && pwd)"

# ── Argument parsing ──────────────────────────────────────────────────────────
while [[ $# -gt 0 ]]; do
    case "$1" in
        --name)
            PROJECT_NAME="$2"
            shift 2
            ;;
        --scenario)
            SCENARIO="$2"
            shift 2
            ;;
        --dest)
            DEST="$2"
            shift 2
            ;;
        --renderer-repo)
            RENDERER_REPO="$2"
            shift 2
            ;;
        --no-renderer)
            CLONE_RENDERER=0
            shift
            ;;
        -h|--help)
            echo "Usage: $0 --name <project> --scenario <scenario> --dest <path> [--renderer-repo <url>] [--no-renderer]"
            exit 0
            ;;
        *)
            echo "Unknown argument: $1" >&2
            exit 1
            ;;
    esac
done

# ── Validation ────────────────────────────────────────────────────────────────
if [[ -z "$PROJECT_NAME" || -z "$SCENARIO" || -z "$DEST" ]]; then
    echo "Error: --name, --scenario, and --dest are all required." >&2
    echo "Usage: $0 --name <project> --scenario <scenario> --dest <path>" >&2
    exit 1
fi

TODAY="$(date +%Y-%m-%d)"
PROJECT_DIR="$DEST"

if [[ -e "$PROJECT_DIR" ]]; then
    echo "Error: destination already exists: $PROJECT_DIR" >&2
    exit 1
fi

# ── Directory structure ────────────────────────────────────────────────────────
echo "Creating project structure at: $PROJECT_DIR"

mkdir -p "$PROJECT_DIR/scenarios/$SCENARIO/slot-examples"
mkdir -p "$PROJECT_DIR/scripts"

# ── Copy templates ─────────────────────────────────────────────────────────────
# AGENTS.md
cp "$TEMPLATES_DIR/AGENTS.template.md" "$PROJECT_DIR/AGENTS.md"
sed -i '' \
    -e "s/{{project_name}}/$PROJECT_NAME/g" \
    -e "s/{{scenario}}/$SCENARIO/g" \
    -e "s/{{YYYY-MM-DD}}/$TODAY/g" \
    "$PROJECT_DIR/AGENTS.md"

# Round-Log.md
cp "$TEMPLATES_DIR/Round-Log.template.md" "$PROJECT_DIR/Round-Log.md"
sed -i '' \
    -e "s/{{project_name}}/$PROJECT_NAME/g" \
    -e "s/{{scenario}}/$SCENARIO/g" \
    -e "s/{{YYYY-MM-DD}}/$TODAY/g" \
    "$PROJECT_DIR/Round-Log.md"

# Scenario files
cp "$TEMPLATES_DIR/prompt-template.md" \
    "$PROJECT_DIR/scenarios/$SCENARIO/prompt-template.md"

cp "$TEMPLATES_DIR/PATTERN.template.md" \
    "$PROJECT_DIR/scenarios/$SCENARIO/PATTERN.md"
sed -i '' \
    -e "s/{{project}}/$PROJECT_NAME/g" \
    -e "s/{{scenario}}/$SCENARIO/g" \
    -e "s/{{created}}/$TODAY/g" \
    "$PROJECT_DIR/scenarios/$SCENARIO/PATTERN.md"

cp "$TEMPLATES_DIR/component-spec.template.md" \
    "$PROJECT_DIR/scenarios/$SCENARIO/component-spec.md"
sed -i '' \
    -e "s/{{project_name}}/$PROJECT_NAME/g" \
    -e "s/{{scenario}}/$SCENARIO/g" \
    -e "s/{{YYYY-MM-DD}}/$TODAY/g" \
    "$PROJECT_DIR/scenarios/$SCENARIO/component-spec.md"

# Copy inject.py
cp "$SCRIPT_DIR/inject.py" "$PROJECT_DIR/scripts/inject.py"
cp "$SCRIPT_DIR/inject.README.md" "$PROJECT_DIR/scripts/inject.README.md"

# ── Git init ──────────────────────────────────────────────────────────────────
cd "$PROJECT_DIR"
git init -q
git add .
git commit -q -m "chore: scaffold $PROJECT_NAME · scenario=$SCENARIO · $(date +%Y-%m-%d)"

# ── Clone renderer (preview tool) ─────────────────────────────────────────────
if [[ $CLONE_RENDERER -eq 1 ]]; then
    echo ""
    echo "Cloning renderer (preview tool) → design-prompt-management/ ..."
    git clone -q --depth 1 "$RENDERER_REPO" "$PROJECT_DIR/design-prompt-management" || {
        echo "Warning: renderer clone failed (network? URL?). Project is usable; you can clone manually:" >&2
        echo "  git clone $RENDERER_REPO $PROJECT_DIR/design-prompt-management" >&2
    }
    # 防 nested .git 干扰主项目
    rm -rf "$PROJECT_DIR/design-prompt-management/.git"
    cd "$PROJECT_DIR" && git add design-prompt-management && \
        git commit -q -m "chore: add renderer (design-prompt-management) as nested folder"
fi

# ── Sync helper ───────────────────────────────────────────────────────────────
cat > "$PROJECT_DIR/scripts/sync-to-management.sh" <<'EOF'
#!/usr/bin/env bash
# sync-to-management.sh — copy this project's slot + new Design Prompt md to
# the nested design-prompt-management/prompts/ tree, so the renderer picks them
# up and you can PR them upstream.
#
# Usage:
#   ./scripts/sync-to-management.sh --scenario <name> --style <handle> [--mgmt <path>]
#
# Defaults: --mgmt ./design-prompt-management

set -euo pipefail
SCENARIO=""; STYLE=""; MGMT="./design-prompt-management"
while [[ $# -gt 0 ]]; do
    case "$1" in
        --scenario) SCENARIO="$2"; shift 2;;
        --style)    STYLE="$2"; shift 2;;
        --mgmt)     MGMT="$2"; shift 2;;
        *) echo "Unknown arg: $1" >&2; exit 1;;
    esac
done
[[ -z "$SCENARIO" || -z "$STYLE" ]] && { echo "Usage: $0 --scenario <name> --style <handle> [--mgmt <path>]" >&2; exit 1; }
[[ ! -d "$MGMT" ]] && { echo "Error: renderer not found at $MGMT (clone it first)" >&2; exit 1; }

SRC="scenarios/$SCENARIO/slot-examples/$STYLE.slot.json"
DST_DIR="$MGMT/prompts/$SCENARIO/$STYLE"
mkdir -p "$DST_DIR"
cp "$SRC" "$DST_DIR/slot.json"
echo "✓ slot.json synced"

# Sync any Design-Prompt-vX.md found in scenarios/<scenario>/
shopt -s nullglob
for f in scenarios/"$SCENARIO"/*Design-Prompt-v*.md; do
    [[ -f "$f" ]] || continue
    V=$(basename "$f" | grep -oE 'v[0-9.]+[a-z0-9-]*' | head -1)
    [[ -z "$V" ]] && continue
    cp "$f" "$DST_DIR/$V.md"
    echo "✓ $V.md synced"
done
shopt -u nullglob

echo ""
echo "Next: cd $MGMT && bun dev → preview at http://localhost:5173"
echo "To upstream: fork chrislau0098/design-prompt-management on GitHub, then:"
echo "  cd $MGMT && git remote add fork <your-fork-url> && git checkout -b add-$STYLE && git add prompts/ && git commit -m 'add $STYLE' && git push fork add-$STYLE && gh pr create"
EOF
chmod +x "$PROJECT_DIR/scripts/sync-to-management.sh"

# ── Summary ───────────────────────────────────────────────────────────────────
echo ""
echo "Project scaffolded: $PROJECT_DIR"
echo ""
echo "Next steps:"
echo "  1. Fill AGENTS.md §1 (project definition) and §7 (required reads)"
echo "  2. Edit scenarios/$SCENARIO/PATTERN.md §11-§12 for scenario-specific archetypes"
echo "  3. Run scaffold-style.sh to create your first Slot:"
echo "       ./scripts/scaffold-style.sh --style <handle> --scenario $SCENARIO --project $PROJECT_DIR"
echo "  4. Fill the Slot JSON values (style_meta → atomic → molecular → tooling)"
echo "  5. Run inject.py to render your first Design Prompt:"
echo "       python3 scripts/inject.py --slot scenarios/$SCENARIO/slot-examples/<handle>.slot.json \\"
echo "           --template scenarios/$SCENARIO/prompt-template.md \\"
echo "           --out scenarios/$SCENARIO/<handle>-Design-Prompt-v0.1.md"
echo "  6. Sync to renderer (preview at localhost:5173):"
echo "       ./scripts/sync-to-management.sh --scenario $SCENARIO --style <handle>"
echo "       cd design-prompt-management && bun install && bun dev"
