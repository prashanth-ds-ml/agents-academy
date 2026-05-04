# Tools vs Prompts

## The core difference

A **prompt** asks the model to *think* about something.  
A **tool** lets the model *do* something.

## Prompts

- Live entirely inside the model's context window
- Can hallucinate — the model makes up results it can't verify
- Fast, no side effects
- Good for: reasoning, summarising, classifying, planning

## Tools

- Python functions the model can call by name
- Results are real — file contents, API responses, current time
- Can have side effects (writing files, sending requests)
- Good for: reading data, taking actions, getting ground truth

## Why this matters

Without tools, an agent that says "I searched the web and found..." is lying — it has no web access. It's just predicting what a search result might say.

With tools, the agent calls a real search function, gets real results, and reasons over them.

## The rule

> Use a prompt when the model already knows enough to answer.  
> Use a tool when the model needs real-world data or needs to take an action.

## Related

- [[04-memory-vault/concepts/agent-loop]]
- [[04-memory-vault/concepts/react-pattern]]
- [[01-lessons/02-tools/lesson]]
