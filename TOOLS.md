# Shared Tools Catalog

> This file is synced to all agent workspaces. It defines the available tools and their usage.

## Core Tools

### exec — Run Shell Commands
```
exec("bash command here")
```
Execute any bash command, Python script, or system operation.

### sessions_spawn — Task Delegation
```javascript
sessions_spawn({
  agentId: "engineer",    // target agent ID
  task: "Your task description here"
})
```
Spawns an isolated session for the target agent. Use for:
- Engineering tasks → `engineer` or `linus`
- Validation → `skeptic`
- Visualization → `visualizer`

**Always include context headers in the task:**
```
[PROJECT: project_name]
[WORKSPACE: /absolute/path/to/workspace/knowledge_hub/project_name/]
[MARKET_CONTEXT: Read MARKET_CONTEXT.md first]
```

### sessions_send — A2A Dialogue
```javascript
sessions_send({
  sessionKey: "agent:engineer:main",
  message: "Your question here",
  timeoutSeconds: 60
})
```
Point-to-point dialogue with another agent. Max 5 rounds.

**DEADLOCK PREVENTION:**
- Never call `sessions_send` inside an A2A conversation
- Only the initiator sends; responder replies with text only
- Known session keys: `agent:{id}:main`

## Data Tools (Customize for Your Setup)

### Market Data
Configure your preferred data source. Examples:

```python
# Load local parquet data
import pandas as pd
df = pd.read_parquet("knowledge_hub/project/data/AAPL.parquet")

# Or use an API
from your_data_provider import get_price_data
df = get_price_data("AAPL", start="2023-01-01", end="2025-12-31")
```

### Web Search
```
# Using OpenClaw's built-in web search
mcporter call web-search-prime --query "your search query"
```

## Python Environment

```bash
# Recommended: use uv for dependency management
cd $WORKSPACE_ROOT
uv sync          # Install dependencies
uv run python script.py  # Run with managed environment
```

## Tool Usage Rules

1. **Action first** — Call tools immediately, don't describe what you'll do
2. **Real data only** — Never generate mock data; use actual data sources
3. **Structured output** — Save results as JSON/CSV/Parquet, not plain text
4. **Absolute paths** — Always use WORKSPACE_ROOT-based absolute paths
5. **Verify after write** — Read back files after writing to confirm success
