# ReAct Pattern

## What it is

**Re**ason + **Act** — a pattern where the model writes its reasoning before deciding on an action.

Introduced in the paper *"ReAct: Synergizing Reasoning and Acting in Language Models"* (2022).

## The loop

```
Thought: [model explains what it's doing and why]
Action: [tool name + args]
Observation: [tool result returned by Python]
Thought: [model reasons over the result]
Action: [next tool or respond]
...
Final Answer: [response to user]
```

## Why it works

- Forces the model to slow down and reason before acting
- The `Thought` step catches obvious mistakes before they become tool calls
- The `Observation` step grounds the model in real results
- Much easier to debug than black-box tool calls

## Simple example

```
User: What files are in the project folder and which is the largest?

Thought: I need to list the files first, then check their sizes.
Action: list_files(path=".")
Observation: ["main.py", "README.md", "data.json"]

Thought: Now I need the size of each file.
Action: get_file_size(path="data.json")
Observation: 48291 bytes

Thought: data.json is likely the largest. I can confirm and answer.
Final Answer: There are 3 files. data.json is the largest at ~47KB.
```

## When to use it

- Any agent that calls more than one tool per task
- When you need the model's reasoning to be auditable
- When tool call errors need graceful recovery

## Related

- [[04-memory-vault/concepts/tools-vs-prompts]]
- [[04-memory-vault/concepts/agent-loop]]
- [[01-lessons/02-tools/lesson]]
