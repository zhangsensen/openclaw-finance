# openclaw-finance — Architecture Guide

## Overview

This system uses a **shared workspace** architecture where all agents access the same knowledge base while maintaining isolated identities.

```
Shared Workspace (all agents read/write)
├── knowledge_hub/          # Shared project data & outputs
├── memory/                 # Shared daily notes
├── AGENTS.md               # Shared behavioral rules
├── TOOLS.md                # Shared tool catalog
├── USER.md                 # User context
└── MEMORY.md               # Project index

Per-Agent Directories (identity isolation)
├── workspace-engineer/
│   ├── IDENTITY.md         # Engineer identity
│   └── SOUL.md             # Engineer rules
├── workspace-skeptic/
│   ├── IDENTITY.md
│   └── SOUL.md
└── ...
```

### Why Shared Workspace?

- **Zero-latency knowledge sharing** — All agents see the same data immediately
- **No sync overhead** — No need to copy files between agents
- **Single source of truth** — One knowledge_hub, one memory system

### Why Per-Agent Identity?

- **Auth isolation** — Each agent has its own session and credentials
- **Role clarity** — IDENTITY.md and SOUL.md define distinct behaviors
- **Safe modification** — Changing one agent's identity doesn't affect others

## Bootstrap Hook System

When an agent starts, OpenClaw's `agent:bootstrap` hook injects the correct IDENTITY.md and SOUL.md from the agent's per-agent directory into the shared workspace session.

```
agent:bootstrap event
  → hook reads agent ID
  → copies IDENTITY.md from workspace-{id}/
  → copies SOUL.md from workspace-{id}/
  → agent sees its own identity in the shared workspace
```

## Communication Flow

### Spawn (One-to-Many)
```
Coordinator → sessions_spawn(engineer, task)
           → sessions_spawn(skeptic, task)
           → sessions_spawn(visualizer, task)
```
Each spawn creates an **isolated session**. The target agent works independently and returns results.

### A2A Send (One-to-One)
```
Skeptic → sessions_send(agent:engineer:main, question)
       ← Engineer replies with text
       → Skeptic follows up (max 5 rounds)
```

### Deadlock Prevention
```
❌ Agent A sends to Agent B → Agent B sends to Agent A (DEADLOCK)
✓ Agent A sends to Agent B → Agent B replies with text (SAFE)
```

## Three-Layer Memory

```
┌─────────────────────────────────────────┐
│  Layer 1: Auto-Recall (LanceDB)        │
│  • Vector + BM25 hybrid search         │
│  • Automatic capture & injection       │
│  • Zero manual effort                  │
├─────────────────────────────────────────┤
│  Layer 2: MEMORY.md                    │
│  • Project index & hard rules          │
│  • <5000 chars                         │
│  • Coordinator: all sessions           │
│  • Others: main session only           │
├─────────────────────────────────────────┤
│  Layer 3: Daily Notes                  │
│  • memory/YYYY-MM-DD.md               │
│  • Raw logs & observations             │
│  • Auto-extracted by Layer 1           │
└─────────────────────────────────────────┘
```

## Heartbeat Monitoring

Stagger heartbeat intervals to avoid thundering herd:

| Agent | Interval | Reason |
|-------|----------|--------|
| Coordinator | 90m | Most frequent — monitors others |
| Engineer | 100m | |
| Linus | 95m | Offset from Engineer |
| Skeptic | 110m | Less frequent — reactive role |
| Visualizer | 120m | Least frequent — triggered by tasks |

## Safety Architecture

### Forbidden Zones
- System config files (openclaw.json) — locked with `chflags uchg` on macOS
- Other agents' identity files
- System admin commands

### Cron Safety
- Always `sessionTarget: "main"` (never `"isolated"`)
- Minimum 5-minute intervals
- Prefer `wakeMode: "next-heartbeat"` for efficiency

---

# 架构指南（中文版）

## 概述

本系统采用**共享工作区**架构：所有 agent 访问同一个知识库，同时保持独立身份。

## 核心设计

### 为什么共享工作区？
- **零延迟知识共享** — 所有 agent 立即看到相同数据
- **无同步开销** — 不需要在 agent 之间复制文件
- **单一数据源** — 一个 knowledge_hub，一套记忆系统

### 为什么隔离身份？
- **认证隔离** — 每个 agent 有独立的会话和凭证
- **角色清晰** — IDENTITY.md 和 SOUL.md 定义不同行为
- **安全修改** — 改一个 agent 的身份不影响其他人

## 通信模式

### Spawn（一对多委派）
协调者将任务分发给专家 agent，每个任务在独立会话中执行。

### A2A Send（一对一对话）
agent 之间直接对话，最多 5 轮，严禁嵌套调用（会死锁）。

## 三层记忆系统

1. **自动回忆**（LanceDB 向量数据库）— 自动捕获和注入，无需手动
2. **MEMORY.md** — 项目索引和硬性约定，<5000 字符
3. **每日笔记** — 原始日志，被第一层自动提取

## 安全机制

- 系统配置文件用 OS 级别文件锁保护
- 禁止跨 agent 修改身份文件
- Cron 任务严格限制频率和会话类型
