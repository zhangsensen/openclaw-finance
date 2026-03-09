# Communication Patterns & Safety Rules

## Overview

Agents communicate through two mechanisms:
1. **sessions_spawn** — Task delegation (one-way, isolated session)
2. **sessions_send** — Direct dialogue (two-way, max 5 rounds)

## sessions_spawn — Task Delegation

### When to Use
- Coordinator dispatching work to specialists
- Any agent delegating a subtask it can't handle

### Syntax
```javascript
sessions_spawn({
  agentId: "engineer",
  task: `
[PROJECT: my_analysis]
[WORKSPACE: /path/to/workspace/knowledge_hub/my_analysis/]
[MARKET_CONTEXT: Read MARKET_CONTEXT.md first]

Load and validate price data for AAPL from 2023-01-01 to 2025-12-31.
Output as parquet to data/E01_aapl_prices.parquet.
Include verification of row count and date range.
`
})
```

### Rules
- Always include project context headers
- Task description should be self-contained (agent may not have prior context)
- Spawned session is isolated — it doesn't share the parent's conversation

### Routing Guide

| Task Type | Route To | Example |
|-----------|----------|---------|
| Data loading | Engineer | "Load AAPL daily prices" |
| Backtesting | Engineer | "Run momentum strategy backtest" |
| ETL pipeline | Engineer / Linus | "Build data cleaning pipeline" |
| Bias check | Skeptic | "Check for survivorship bias" |
| Validation | Skeptic | "Validate backtest statistical significance" |
| Charts | Visualizer | "Generate price trend chart" |
| Reports | Visualizer | "Create PDF analysis report" |
| Integration | Coordinator | (handles internally) |

## sessions_send — Direct Dialogue

### When to Use
- Skeptic questioning Engineer about data quality
- Cross-agent clarification during a project

### Syntax
```javascript
sessions_send({
  sessionKey: "agent:engineer:main",
  message: "Did you account for stock splits in the price data?",
  timeoutSeconds: 60
})
```

### Session Keys
```
agent:coordinator:main
agent:engineer:main
agent:linus:main
agent:skeptic:main
agent:visualizer:main
```

### Safety Rules (CRITICAL)

#### Rule 1: No Nested Sends
```
❌ DEADLOCK:
Agent A → sessions_send → Agent B
Agent B → sessions_send → Agent A    // DEADLOCK!

✓ SAFE:
Agent A → sessions_send → Agent B
Agent B → replies with text           // Agent A receives response
```

#### Rule 2: Only Initiator Sends
The agent who starts the conversation is the only one who calls `sessions_send`. The responder always replies with plain text.

#### Rule 3: Max 5 Rounds
Conversations auto-terminate after 5 ping-pong exchanges. Design your questions to get answers within this limit.

#### Rule 4: Don't Mix Spawn and Send
```
❌ Inside a spawned task: sessions_send(...)   // Don't do this
✓ Inside a spawned task: just do the work      // Complete the task directly
```

## Example Workflow

### Stock Analysis with Quality Control

```
1. User → Coordinator: "Analyze AAPL"

2. Coordinator spawns in parallel:
   → Engineer: "Load AAPL data, calculate metrics"
   → Skeptic: "Prepare validation checklist"

3. Engineer completes → returns data file path
   Skeptic completes → returns checklist

4. Coordinator spawns:
   → Skeptic: "Validate engineer's output at [path], using your checklist"

5. Skeptic validates → returns PASS/FAIL with notes

6. If PASS:
   Coordinator spawns:
   → Visualizer: "Generate report from [data path]"

7. Visualizer completes → returns report path

8. Coordinator → User: "Analysis complete. Report: [path]"
```

## Troubleshooting

### Agent Not Responding
1. Check heartbeat — is the agent healthy?
2. Check if agent is stuck in an A2A deadlock
3. Try spawning a new task instead of sending to existing session

### Deadlock Detected
1. Identify which agent called `sessions_send` inside an A2A conversation
2. Fix the SOUL.md to explicitly forbid nested sends
3. Restart the stuck agents via gateway restart

### Task Timeout
1. Check if the agent has the required data/tools
2. Check if MARKET_CONTEXT.md exists for the project
3. Consider breaking the task into smaller subtasks
