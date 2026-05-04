# Next Steps

When you reopen the vault, start here.

## Resume Project 1

Project 1 is working. To pick up:

```powershell
cd 02-projects\project-01-goal-planner
.venv\Scripts\Activate.ps1   # from repo root first
python main.py
```

- Choose a model at startup (number or Enter for mistral:latest)
- Enter any goal — the brainstorm agent will ask only what it needs, then produce a plan

### What to improve next on Project 1

1. Save the generated plan to a markdown file automatically
2. Let the user rate or edit the plan after generation
3. Add a `--model` CLI flag so model can be passed without the interactive picker
4. Explore using `qwen2.5-coder` or `gemma4` for better plan quality

## Lesson 1 (still pending)

1. Complete [[01-lessons/01-foundations/exercises]]
2. Write one concept note in `04-memory-vault/concepts/`
3. Fill in [[04-memory-vault/reflections/week-01]]
4. Expand [[05-blog/drafts/2026-05-02-learning-agents-in-public]]

## Phase 2 prep

When Lesson 1 is done, move to:

- Lesson 2: Tools and structured inputs
- Project 2: first real tool-using agent (file reader, web search, or similar)
- Begin Ollama + LangGraph integration

## Rule for smooth learning

Never finish a session without:

- one exercise attempt
- one memory note
- one reflection update
