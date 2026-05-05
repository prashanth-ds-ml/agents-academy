---
title: CodeMitra
tags: [codemitra, product, local-llm, project, reference]
aliases: [local-codex, CodeMitra project]
---

# CodeMitra

> A local, offline AI coding assistant powered by Ollama.  
> No API keys. No cloud. No data leaves your machine.

**Repo:** [prashanth-ds-ml/local-codex](https://github.com/prashanth-ds-ml/local-codex)  
**Local path:** `C:\Users\prash\Projects\local-codex`

---

## Why it exists

Tools like GitHub Copilot and Claude Code work well because they bundle a model with a system — routing, agents, tools, memory, loops. When you try to replicate that locally with Ollama, the system layer is missing.

CodeMitra builds that system layer on top of open-source models. The insight:

```
Claude Code  = model + routing + agents + tools + memory + loop
CodeMitra    = Ollama models + LangChain + same system, built locally
```

Target user: anyone who wants a capable coding assistant but can't afford monthly subscriptions, or prefers to keep their code 100% private.

---

## What it can do now

- Rich terminal UI (banner, styled panels, agent output)
- Chat about code (`qwen2.5-coder:7b`)
- Filesystem agent — create folders, files, venv, install packages (10 tools)
- Dual-model routing — chat model detects task type, routes to agent model (`qwen3.5:latest`)
- PermissionGuard — workspace sandboxing, command whitelist

---

## Build phases

| Phase | Description | Status |
|---|---|---|
| 1 | Foundation — CLI, config, banner | ✅ Done |
| 2 | Chat core — history, streaming, slash commands | ✅ Done |
| 3 | Filesystem agent — 10 tools, guard, Rich output | ✅ Done |
| 4 | Routing — chat LLM detects intent → delegates | ⚠️ Needs end-to-end test |
| 5 | Code reader agent — read, search, understand codebase | 🔲 Next |
| 6 | Shell agent — run commands, capture output, react | 🔲 Planned |
| 7 | Planner agent — break large tasks, route to sub-agents | 🔲 Planned |
| 8 | Memory — `.codemitra/` session log, cross-session context | 🔲 Planned |

---

## How it connects to Agents Academy

Every project in the academy is a learning prototype for a CodeMitra capability:

```
Academy                          →  CodeMitra
─────────────────────────────────────────────────────────────────
Project 1: Goal Planner          →  Conversation Agent + Planner Agent
Project 2: ReAct Tool Agent      →  Filesystem Agent execution loop
Project 3: Code Reader (next)    →  Phase 5 — Code Reader Agent
Project 4: Memory (planned)      →  Phase 8 — Memory layer
```

Learn the pattern in the sandbox → implement it properly in the product.

---

## Tech stack

- **LLM runtime:** Ollama
- **LLM framework:** LangChain (`langchain-ollama`, `langchain-core`)
- **Terminal UI:** Rich + prompt_toolkit
- **Language:** Python 3.11+
- **Config:** `codemitra.toml`

---

## Multi-agent architecture

```
User
 └── Conversation Agent (qwen2.5-coder:7b)
       └── Planner Agent (qwen3.5:latest)
             ├── Filesystem Agent   ✅ built
             ├── Code Writer Agent  🔨 next
             ├── Code Reader Agent  🔨 next
             ├── Shell Agent        🔨 planned
             └── Reviewer Agent     🔨 planned
```

Each agent has one job. Each uses the model best suited for that job. The user only ever talks to the Conversation Agent.

---

## Key design rules

- Ask before acting on ambiguous requests (never guess)
- Confirm before destructive actions (delete, overwrite)
- Workspace sandboxing — agent can only touch the project folder
- Show a diff/summary before bulk changes
- Run tests before marking a task complete

---

## Guiding principle

> Use the right model for the right job.  
> Build the system that makes imperfect models work together.
