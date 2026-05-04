# Agent loop

The simplest agent loop is:

1. Observe
2. Decide
3. Act
4. Observe again

## Why it matters

Without a loop, many systems are just prompt wrappers or workflows.

## Real example

[[02-projects/project-01-goal-planner/README|Project 1]] uses this loop in its brainstorm agent — it observes the Q&A history, decides if it needs more info or is ready to plan, and acts by asking a question or outputting `READY_TO_PLAN`.

## Links

- [[01-lessons/01-foundations/lesson]]
- [[04-memory-vault/concepts/chatbot-vs-workflow-vs-agent]]
- [[04-memory-vault/concepts/memory-vs-state]]
