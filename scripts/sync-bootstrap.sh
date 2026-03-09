#!/bin/bash
# Sync shared bootstrap files (AGENTS.md, TOOLS.md) to all agent workspaces
# Usage: bash sync-bootstrap.sh /path/to/workspace [agent_id]

set -e

WORKSPACE="${1:?Usage: bash sync-bootstrap.sh /path/to/workspace [agent_id]}"
SCRIPT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
SINGLE_AGENT="${2:-}"

# Agent workspace mapping
declare -A AGENT_DIRS=(
  [coordinator]="$WORKSPACE"
  [engineer]="$WORKSPACE/../workspace-engineer"
  [linus]="$WORKSPACE/../workspace-linus"
  [skeptic]="$WORKSPACE/../workspace-skeptic"
  [visualizer]="$WORKSPACE/../workspace-visualizer"
)

sync_agent() {
  local agent="$1"
  local dir="${AGENT_DIRS[$agent]}"

  if [ ! -d "$dir" ]; then
    echo "  ⚠ Skipping $agent — directory not found: $dir"
    return
  fi

  # AGENTS.md: coordinator gets the chat variant (MEMORY.md always loaded)
  if [ "$agent" = "coordinator" ]; then
    # Coordinator reads MEMORY.md in all sessions
    cp "$SCRIPT_DIR/AGENTS.md" "$dir/AGENTS.md"
    # Patch: coordinator always reads MEMORY.md
    sed -i.bak 's/Read MEMORY.md only in main session/Read MEMORY.md in ALL sessions (coordinator override)/g' "$dir/AGENTS.md"
    rm -f "$dir/AGENTS.md.bak"
  else
    cp "$SCRIPT_DIR/AGENTS.md" "$dir/AGENTS.md"
  fi

  # TOOLS.md: identical for all agents
  cp "$SCRIPT_DIR/TOOLS.md" "$dir/TOOLS.md"

  echo "  ✓ $agent synced"
}

echo "Syncing bootstrap files..."

if [ -n "$SINGLE_AGENT" ]; then
  if [ -z "${AGENT_DIRS[$SINGLE_AGENT]+x}" ]; then
    echo "Error: Unknown agent '$SINGLE_AGENT'"
    echo "Available: ${!AGENT_DIRS[*]}"
    exit 1
  fi
  sync_agent "$SINGLE_AGENT"
else
  for agent in "${!AGENT_DIRS[@]}"; do
    sync_agent "$agent"
  done
fi

echo ""
echo "Sync complete!"
echo ""
echo "Next steps:"
echo "  1. openclaw gateway restart"
echo "  2. Send /reset to each agent in Telegram"
