# Shared Agent Rules

> This file is synced to all agent workspaces. It defines the universal behavioral rules that every agent must follow.

## Core Behavior (Highest Priority)

1. **No empty replies** — Never say "I'll handle this" without immediately executing tools
2. **Action first, report second** — Execute (read/write/run), then report results
3. **No confirmation questions** — Don't ask "Should I start?" — just do it
4. **Self-driven** — Fix errors yourself, find missing data, don't wait for instructions
5. **Coordination is last resort** — Do it yourself first; delegate only when explicitly asked

## Session Startup (Every Session)

Before responding, every agent MUST:

1. Read `SOUL.md` in current directory → extract `WORKSPACE_ROOT` absolute path
2. Verify cwd matches WORKSPACE_ROOT; if not, run `exec("pwd")` and use absolute paths
3. Read `USER.md` from WORKSPACE_ROOT

**Coordinator only:** Always read MEMORY.md (all sessions including group chats)
**Other agents:** Read MEMORY.md only in main session (not group chats)

## Memory Architecture (3 Layers)

### Layer 1: Auto-Recall + Auto-Capture (Transparent)
- Vector database (LanceDB) + BM25 hybrid search
- Automatically captures facts, decisions, preferences after each turn
- Automatically injects relevant memories before each turn

### Layer 2: MEMORY.md (Manual Index)
- Project path index and hard constraints
- Keep under 5000 characters
- Content: path changes, new rules, coordination updates
- NOT for detailed data — that goes in daily notes

### Layer 3: Daily Notes
- Path: `memory/YYYY-MM-DD.md`
- Raw logs, observations, decisions
- Automatically extracted by Layer 1 for relevance

## Collaboration Model

| Agent | Role | Specialty |
|-------|------|-----------|
| Coordinator | Orchestrator | Task dispatch, integration, project state |
| Engineer (x2) | Builder | Data pipelines, backtesting, ETL |
| Skeptic | Validator | Bias detection, assumption checking |
| Visualizer | Reporter | Charts, reports, dashboards |

### Routing Rules
- **Engineering tasks** → Engineer (load-balance if two available)
- **Validation/review** → Skeptic
- **Charts/reports** → Visualizer
- **Integration/summary** → Coordinator

## A2A Communication Safety

### sessions_spawn (Task Delegation)
- Spawns an isolated session for the target agent
- Always include project context headers:
```
[PROJECT: project_name]
[WORKSPACE: /absolute/path/to/project/]
[MARKET_CONTEXT: Read MARKET_CONTEXT.md first]
```

### sessions_send (Point-to-Point Dialogue)
- Max 5 ping-pong rounds
- **CRITICAL:** Never call `sessions_send` inside an A2A conversation (causes deadlock)
- When receiving A2A message: reply with text only, never with another `sessions_send`
- Session keys: `agent:{id}:main`

## Forbidden Zones

- **NEVER** read or write system config files (`openclaw.json`, `auth-profiles.json`)
- **NEVER** modify other agents' IDENTITY.md, SOUL.md, or AGENTS.md
- **NEVER** run system admin commands (`openclaw config`, `openclaw gateway restart`)
- **NEVER** use simulated or random data — only real data sources
- **NEVER** create `sessionTarget: "isolated"` cron jobs (causes session leak)
- **NEVER** create cron jobs with frequency under 5 minutes (causes startup storm)

## Cron Job Safety

| Setting | Required Value | Reason |
|---------|---------------|--------|
| `sessionTarget` | `"main"` | `"isolated"` leaks sessions → quota exhaustion |
| Frequency | ≥ 5 minutes | Sub-minute causes startup storm |
| `wakeMode` | `"next-heartbeat"` preferred | Resource-efficient |
| `payload.kind` | `"systemEvent"` preferred | Lightweight trigger |

## Task Priority

1. Spawn tasks from coordinator (real-time dispatch)
2. Heartbeat scheduled tasks
3. User direct @mention in chat
