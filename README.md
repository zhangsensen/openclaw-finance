# Financial Multi-Agent System

A production-ready framework for building **multi-agent financial research systems** with [OpenClaw](https://openclaw.ai).

Clone, configure your API keys, and run — 4 specialized agents collaborate on financial research with built-in quality control.

## Why Multi-Agent?

Traditional financial research is linear and error-prone:

```
PM → Analyst → Programmer → Output
     ↑ Information decay at each step
```

Multi-agent approach:
- **Parallel processing**: Multiple specialists work simultaneously
- **Built-in quality control**: A dedicated skeptic agent challenges assumptions
- **Shared context**: All agents access the same knowledge base
- **Traceable decisions**: Every step is logged and auditable

## Architecture

```
┌─────────────────────────────────────────────┐
│                  User Request               │
└──────────────────┬──────────────────────────┘
                   ▼
┌──────────────────────────────────────────────┐
│           Coordinator (Chat Agent)           │
│  • Task decomposition & dispatch             │
│  • Result integration                        │
│  • Health monitoring via heartbeat           │
└──┬──────────┬──────────┬──────────┬─────────┘
   ▼          ▼          ▼          ▼
┌────────┐ ┌────────┐ ┌────────┐ ┌──────────┐
│Engineer│ │Engineer│ │Skeptic │ │Visualizer│
│ (Code) │ │(Linus) │ │  (FP)  │ │ (Vision) │
│        │ │        │ │        │ │          │
│ Data & │ │Parallel│ │Challenge│ │ Charts & │
│Backtest│ │  Load  │ │Validate│ │ Reports  │
│        │ │Balance │ │        │ │          │
└────────┘ └────────┘ └────────┘ └──────────┘
        ▲          ▲          ▲          ▲
        └──────────┴──────────┴──────────┘
                       │
              ┌────────┴────────┐
              │  Knowledge Hub  │
              │ (Shared State)  │
              └─────────────────┘
```

## Quick Start

### Prerequisites

- [OpenClaw](https://openclaw.ai) installed (`npm i -g openclaw`)
- At least one LLM provider API key (OpenAI, ZAI, Bailian, Ollama, etc.)

### 1. Clone & Configure

```bash
git clone https://github.com/zhangsensen/financial-multi-agent-system.git
cd financial-multi-agent-system

# Copy example config
cp examples/openclaw-config-example.json ~/.openclaw/openclaw.json

# Edit with your API keys and model preferences
vim ~/.openclaw/openclaw.json
```

### 2. Set Up Workspace

```bash
# Run the setup script
bash scripts/setup.sh /path/to/your/workspace

# This creates:
# /path/to/your/workspace/
# ├── knowledge_hub/
# ├── memory/
# ├── AGENTS.md
# ├── TOOLS.md
# └── (per-agent dirs with IDENTITY.md + SOUL.md)
```

### 3. Sync Bootstrap Files

```bash
# Sync shared rules to all agent workspaces
bash scripts/sync-bootstrap.sh /path/to/your/workspace

# After sync, restart gateway
openclaw gateway restart
```

### 4. Start Using

Open Telegram, message your coordinator bot:

> "Analyze AAPL with quality checks"

The coordinator will automatically:
1. Spawn Engineer → load price data
2. Spawn Skeptic → prepare analysis checklist
3. Engineer → calculate metrics
4. Skeptic → validate results, check for biases
5. Visualizer → generate report

## Agent Roles

| Agent | Role | Specialty |
|-------|------|-----------|
| **Coordinator** | Task dispatch & integration | Orchestrates other agents, maintains project state |
| **Engineer** (x2) | Data infrastructure | Python/pandas, backtesting, ETL pipelines |
| **Skeptic** | Quality control | Challenge assumptions, bias detection, validation |
| **Visualizer** | Reports & charts | Matplotlib/Plotly, PDF/HTML reports |

See [`agents/`](agents/) for complete identity and behavior files.

## Communication Patterns

### Spawn (Task Delegation)
```javascript
// Coordinator spawns engineer with isolated session
sessions_spawn({
  agentId: "engineer",
  task: "Load and validate AAPL price data from 2023-01-01 to 2025-12-31"
})
```

### A2A Dialogue (Point-to-Point)
```javascript
// Skeptic questions engineer directly
sessions_send({
  sessionKey: "agent:engineer:main",
  message: "Did you exclude stocks with insufficient trading days?",
  timeoutSeconds: 60
})
```

### Deadlock Prevention Rules
1. **Never** call `sessions_send` inside an A2A conversation
2. Only the initiator sends messages
3. Respond with text, not another `sessions_send`

## Memory System (3 Layers)

| Layer | Mechanism | Purpose |
|-------|-----------|---------|
| **Auto-Recall** | LanceDB (vector + BM25) | Automatic context injection, zero manual effort |
| **MEMORY.md** | Markdown file | Project index, hard constraints (<5000 chars) |
| **Daily Notes** | `memory/YYYY-MM-DD.md` | Raw logs, auto-extracted by Layer 1 |

## Knowledge Hub

```
knowledge_hub/
├── agent_coordination/
│   ├── AGENT_OUTPUT_SPEC.md    # Output standards for all agents
│   └── PROJECT_STATE.json      # Current project status (coordinator-only writes)
├── your_project/
│   ├── MARKET_CONTEXT.md       # Market rules & data sources
│   ├── data/                   # Shared data outputs
│   └── reports/                # Generated reports
```

## What to Open Source vs Keep Private

| Open Source (Framework) | Keep Private (Strategy) |
|------------------------|------------------------|
| Agent collaboration patterns | Factor formulas |
| Communication protocols | Strategy parameters |
| Memory system design | Proprietary data sources |
| Heartbeat monitoring | Alpha generation logic |
| Generic templates | Trading signals |

## Project Structure

```
.
├── README.md
├── agents/
│   ├── coordinator/          # Chat agent (orchestrator)
│   │   ├── IDENTITY.md
│   │   └── SOUL.md
│   ├── engineer/             # Code agent (data & backtest)
│   │   ├── IDENTITY.md
│   │   └── SOUL.md
│   ├── skeptic/              # FirstPrinciple agent (validation)
│   │   ├── IDENTITY.md
│   │   └── SOUL.md
│   └── visualizer/           # Vision agent (charts & reports)
│       ├── IDENTITY.md
│       └── SOUL.md
├── knowledge_hub/
│   ├── agent_coordination/
│   │   ├── AGENT_OUTPUT_SPEC.md
│   │   └── PROJECT_STATE.json
│   └── example_project/
│       └── MARKET_CONTEXT.md
├── scripts/
│   ├── setup.sh              # One-time workspace setup
│   └── sync-bootstrap.sh     # Sync shared rules to all agents
├── examples/
│   └── openclaw-config-example.json
├── docs/
│   ├── architecture.md       # Detailed architecture (EN + CN)
│   └── communication.md      # A2A patterns & safety rules
├── AGENTS.md                 # Shared behavioral rules
├── TOOLS.md                  # Shared tool catalog
└── LICENSE
```

## License

MIT

## Credits

Built with [OpenClaw](https://openclaw.ai) — the multi-agent orchestration platform.

Community contributor: [@zhangsensen](https://github.com/zhangsensen)
