# Week 1 Reflection

## What I learned

- The difference between a chatbot, workflow, and agent — see [[04-memory-vault/concepts/chatbot-vs-workflow-vs-agent]]
- How the agent loop works — see [[04-memory-vault/concepts/agent-loop]]
- How to connect Ollama to a Python project using `langchain-ollama`
- Built [[02-projects/project-01-goal-planner/README|Project 1]]: a two-stage brainstorm + plan agent
- How to structure prompts to get reliable, parseable output from a local LLM
- The difference between streaming and invoke — streaming feels alive, invoke is easier to parse
- How a REPL loop turns a one-shot script into a real interactive tool
- Slash commands (`/save`, `/model`, `/new`) make a CLI feel professional

## What confused me

- Local LLMs don't always follow prompt structure perfectly — needed filtering and fallbacks
- Knowing when the agent has "enough context" is fuzzy — had to prompt the model to self-decide
- Rich terminal formatting took trial and error to get looking clean

## What I want to build next

- A tool-using agent — one that can actually read files, search the web, run code
- Project 2: an agent with real tools, not just prompts

## Related

- [[01-lessons/01-foundations/lesson]]
- [[01-lessons/01-foundations/exercises]]
- [[04-memory-vault/concepts/memory-vs-state]]
