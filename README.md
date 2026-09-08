<p align="center">
  <h1 align="center">openclaw-finance</h1>
  <p align="center">
    <strong>Multi-agent financial research system built on OpenClaw</strong>
  </p>
  <p align="center">
    <a href="https://openclaw.ai">OpenClaw</a> &middot;
    <a href="docs/architecture.md">Architecture</a> &middot;
    <a href="docs/communication.md">Communication</a> &middot;
    <a href="#quick-start">Quick Start</a>
  </p>
  <p align="center">
    <a href="#中文说明">中文</a> | <a href="#why-multi-agent">English</a>
  </p>
</p>

---

> This framework has been used in a 7-agent Telegram workflow for US and A-share financial research. Verify the current runtime status before relying on it operationally.

Clone. Configure API keys. Run. 4 specialized agents collaborate on financial research with built-in quality control — no single agent can match what a team delivers.

## Why Multi-Agent?

Traditional financial research is linear. Information decays at each handoff:

```
PM → Analyst → Programmer → Output
     ↑ Information decay at each step
```

**openclaw-finance** replaces this with parallel, self-validating agents:

- **Parallel processing** — Multiple specialists work simultaneously
- **Built-in quality control** — A dedicated skeptic challenges every assumption
- **Shared context** — All agents access the same knowledge base in real-time
- **Traceable decisions** — Every step is logged and auditable
- **Self-healing** — Heartbeat monitoring auto-recovers failed agents

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

### Key Design Decisions

| Decision | Why |
|----------|-----|
| **Shared workspace** | Zero-latency knowledge sharing, no sync overhead |
| **Per-agent identity** | Auth isolation + role clarity without file duplication |
| **Bootstrap hooks** | Dynamic identity injection at startup |
| **3-layer memory** | Auto-recall (LanceDB) + manual index (MEMORY.md) + daily logs |
| **Staggered heartbeats** | Avoid thundering herd, 79-120min intervals |

## Agent Roles

| Agent | Role | What It Does |
|-------|------|-------------|
| **Coordinator** | Orchestrator | Decomposes requests, dispatches tasks, integrates results |
| **Engineer** (x2) | Data & Backtest | Python/pandas pipelines, ETL, backtesting, load-balanced pair |
| **Skeptic** | Quality Control | Bias detection, assumption challenging, statistical validation |
| **Visualizer** | Reports & Charts | Matplotlib/Plotly charts, PDF/HTML reports, dashboards |

## Quick Start

### Prerequisites

- [OpenClaw](https://openclaw.ai) installed (`npm i -g openclaw`)
- At least one LLM API key (OpenAI, Qwen, GLM, Ollama, etc.)

### 1. Clone & Configure

```bash
git clone https://github.com/zhangsensen/openclaw-finance.git
cd openclaw-finance

# Copy example config and add your API keys
cp examples/openclaw-config-example.json ~/.openclaw/openclaw.json
vim ~/.openclaw/openclaw.json
```

### 2. Set Up Workspace

```bash
bash scripts/setup.sh /path/to/your/workspace
```

This creates the full workspace structure with agent identities, shared rules, and knowledge hub.

### 3. Start

```bash
openclaw gateway restart
```

Open Telegram, message your coordinator bot:

> "Analyze AAPL with quality checks"

The system automatically:
1. **Engineer** loads price data
2. **Skeptic** prepares validation checklist
3. **Engineer** calculates metrics
4. **Skeptic** validates results (survivorship bias, look-ahead bias, etc.)
5. **Visualizer** generates report
6. **Coordinator** delivers integrated output

### Try the Demo Locally

```bash
cd examples/stock-analysis
pip install pandas numpy
python run_analysis.py --stock AAPL
```

## Communication Patterns

### Spawn — Task Delegation
```javascript
sessions_spawn({
  agentId: "engineer",
  task: "Load and validate AAPL price data from 2023-01-01 to 2025-12-31"
})
```

### A2A — Point-to-Point Dialogue
```javascript
sessions_send({
  sessionKey: "agent:engineer:main",
  message: "Did you exclude stocks with insufficient trading days?",
  timeoutSeconds: 60
})
```

### Safety Rules
- Never call `sessions_send` inside an A2A conversation (causes deadlock)
- Max 5 ping-pong rounds per dialogue
- Respond with text, never with another `sessions_send`

See [docs/communication.md](docs/communication.md) for complete patterns.

## Memory System

| Layer | Mechanism | Effort |
|-------|-----------|--------|
| **Auto-Recall** | LanceDB vector + BM25 hybrid | Zero (automatic) |
| **MEMORY.md** | Project index + hard rules | Low (manual, <5000 chars) |
| **Daily Notes** | `memory/YYYY-MM-DD.md` | Medium (raw logs, auto-extracted) |

## Project Structure

```
openclaw-finance/
├── agents/
│   ├── coordinator/     # Orchestrator identity & rules
│   ├── engineer/        # Data engineer identity & rules
│   ├── skeptic/         # Quality controller identity & rules
│   └── visualizer/      # Chart/report generator identity & rules
├── knowledge_hub/
│   ├── agent_coordination/   # Output specs + project state
│   └── example_project/      # Template with MARKET_CONTEXT.md
├── scripts/
│   ├── setup.sh              # One-command workspace setup
│   └── sync-bootstrap.sh     # Sync rules across agents
├── examples/
│   ├── openclaw-config-example.json
│   └── stock-analysis/       # Runnable demo
├── docs/
│   ├── architecture.md       # Deep dive (EN + CN)
│   └── communication.md      # A2A patterns & safety
├── AGENTS.md                 # Shared behavioral rules
├── TOOLS.md                  # Shared tool catalog
└── LICENSE                   # MIT
```

## Open Source Boundary

| Open Source (This Repo) | Keep Private (Your Work) |
|------------------------|------------------------|
| Agent collaboration patterns | Factor formulas |
| Communication protocols | Strategy parameters |
| Memory system design | Proprietary data sources |
| Heartbeat monitoring | Alpha generation logic |
| Bootstrap templates | Trading signals |

---

## 中文说明

### openclaw-finance 是什么？

基于 [OpenClaw](https://openclaw.ai) 的**多 Agent 金融研究框架**。4 个专业 Agent 协作完成金融研究，内置质量控制。

**已在生产环境验证** — 7 个 Agent 7x24 小时运行在 Telegram 上，覆盖美股和 A 股市场研究。

### 核心设计

- **共享工作区** — 所有 Agent 访问同一个知识库，零延迟
- **身份隔离** — 每个 Agent 有独立的 IDENTITY.md 和 SOUL.md
- **三层记忆** — 自动回忆（LanceDB）+ 手动索引（MEMORY.md）+ 每日笔记
- **安全机制** — 心跳监控、死锁预防、配置文件锁定

### Agent 分工

| Agent | 角色 | 职责 |
|-------|------|------|
| **协调者** | 调度中心 | 任务分解、结果整合、健康监控 |
| **工程师** (x2) | 数据基建 | Python 数据管道、回测引擎、ETL |
| **质疑者** | 质量控制 | 挑战假设、偏差检测、统计验证 |
| **可视化** | 报告图表 | Matplotlib/Plotly 图表、PDF/HTML 报告 |

### 快速开始

```bash
git clone https://github.com/zhangsensen/openclaw-finance.git
cd openclaw-finance
cp examples/openclaw-config-example.json ~/.openclaw/openclaw.json
# 编辑配置，填入你的 API key 和工作区路径
bash scripts/setup.sh /path/to/your/workspace
openclaw gateway restart
```

详细架构文档见 [docs/architecture.md](docs/architecture.md)（含完整中文版）。

### 为什么多 Agent？

传统金融研究是线性的，信息在传递中逐级衰减。多 Agent 方案实现**并行处理 + 内置质控 + 共享上下文 + 决策可追溯**。

一个 Agent 做不到的事，一个团队可以。

---

## Contributing

Issues and PRs welcome. Please keep the framework/strategy boundary — this repo is for the orchestration framework, not for trading strategies.

## License

MIT

## Credits

Built with [OpenClaw](https://openclaw.ai) | Author: [@zhangsensen](https://github.com/zhangsensen)
