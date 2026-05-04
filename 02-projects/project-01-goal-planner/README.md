# Project 1 - Goal Planner

A two-stage Ollama-powered agent that brainstorms with the user before producing a structured plan.

## What it does

1. **Model picker** — lists all locally available Ollama models at startup; pick by number, name, or Enter for `mistral:latest`
2. **Brainstorm agent** — thinks internally (dim panel + elapsed time), asks only the minimal critical questions it cannot answer itself, loops until it has enough context (`READY_TO_PLAN`)
3. **Planner agent** — uses the full Q&A context to generate a specific, tailored plan streamed live to the terminal

## Output format

- Objective
- Steps (4)
- Risks
- Constraints
- Next action

## Architecture

```
Goal input
  ↓
Brainstorm loop (Ollama call per round)
  ├─ spinner while model thinks
  ├─ dim panel shows internal reasoning
  ├─ bold white shows questions (numbered lines only)
  └─ repeats until READY_TO_PLAN
  ↓
Planner (Ollama call, streams live)
  ↓
Structured plan output
```

## Stack

- `langchain-ollama` + `langchain-core` — LLM chaining
- `rich` — terminal UI (panels, rules, spinner, streaming)
- `ollama` Python client — model listing
- Rule-based fallback if Ollama is unavailable

## Run

```powershell
# from repo root
.venv\Scripts\Activate.ps1
cd 02-projects\project-01-goal-planner
python main.py
```

## What to build next

1. Save plan output to a markdown file
2. Add `--model` CLI flag to skip the picker
3. Let user edit or rate the plan after generation
4. Turn into a real tool-using agent (Phase 2)
