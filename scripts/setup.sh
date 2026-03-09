#!/bin/bash
# Setup script for Financial Multi-Agent System
# Usage: bash setup.sh /path/to/your/workspace

set -e

WORKSPACE="${1:?Usage: bash setup.sh /path/to/your/workspace}"
SCRIPT_DIR="$(cd "$(dirname "$0")/.." && pwd)"

echo "Setting up Financial Multi-Agent System..."
echo "Workspace: $WORKSPACE"
echo "Source: $SCRIPT_DIR"
echo ""

# Create shared workspace structure
mkdir -p "$WORKSPACE"/{memory,knowledge_hub/agent_coordination}

# Copy shared files
cp "$SCRIPT_DIR/AGENTS.md" "$WORKSPACE/AGENTS.md"
cp "$SCRIPT_DIR/TOOLS.md" "$WORKSPACE/TOOLS.md"
cp "$SCRIPT_DIR/knowledge_hub/agent_coordination/AGENT_OUTPUT_SPEC.md" "$WORKSPACE/knowledge_hub/agent_coordination/"
cp "$SCRIPT_DIR/knowledge_hub/agent_coordination/PROJECT_STATE.json" "$WORKSPACE/knowledge_hub/agent_coordination/"

# Create per-agent workspace directories
declare -A AGENTS=(
  [coordinator]="workspace"
  [engineer]="workspace-engineer"
  [linus]="workspace-linus"
  [skeptic]="workspace-skeptic"
  [visualizer]="workspace-visualizer"
)

for agent in "${!AGENTS[@]}"; do
  dir="${AGENTS[$agent]}"
  if [ "$dir" = "workspace" ]; then
    target="$WORKSPACE"
  else
    target="$WORKSPACE/../$dir"
    mkdir -p "$target"
  fi

  # Copy agent identity files
  cp "$SCRIPT_DIR/agents/$agent/IDENTITY.md" "$target/IDENTITY.md"
  cp "$SCRIPT_DIR/agents/$agent/SOUL.md" "$target/SOUL.md"

  # Replace WORKSPACE_ROOT placeholder
  sed -i.bak "s|__WORKSPACE_ROOT__|$WORKSPACE|g" "$target/SOUL.md"
  rm -f "$target/SOUL.md.bak"

  echo "  ✓ $agent → $target"
done

# Create empty USER.md
cat > "$WORKSPACE/USER.md" << 'EOF'
# User Context

## About You
- Name: [Your name]
- Role: [Your role, e.g., "Quantitative Researcher"]
- Preferences: [Communication style, timezone, etc.]

## Notes
- [Add any context that helps agents understand your needs]
EOF

# Create empty MEMORY.md
cat > "$WORKSPACE/MEMORY.md" << 'EOF'
# Memory

## Project Index
- [Add project paths and key references here]

## Hard Rules
- [Add constraints that all agents must follow]

## Notes
- Keep this file under 5000 characters
- Use as an index, not for detailed data
EOF

echo ""
echo "Setup complete!"
echo ""
echo "Next steps:"
echo "  1. Edit $WORKSPACE/USER.md with your info"
echo "  2. Copy examples/openclaw-config-example.json to ~/.openclaw/openclaw.json"
echo "  3. Edit openclaw.json with your API keys and workspace path"
echo "  4. Run: openclaw gateway restart"
