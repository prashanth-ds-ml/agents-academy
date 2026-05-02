# Project 1 - Goal Planner

This first mini-project is intentionally simple.

It is **not** a full agent yet. It helps you see the difference between:

- a plain response
- a structured workflow
- the beginning of agent thinking

## Goal

Take a user goal and return:

1. objective
2. steps
3. risks
4. constraints
5. next action

## Lesson note

This project does **not** use Ollama yet.

It is intentionally rule-based so you can learn:

- structured output
- goal-aware logic
- why structure alone is still not a full agent

The output now shows a visible **Model** line to make that explicit.

## Run

```powershell
python main.py
```

## Practice ideas

1. Change the questions it asks.
2. Add another goal-aware case, like a study planner or blog writer.
3. Add a "what should happen next?" section.
4. Later, turn it into a real tool-using agent.
