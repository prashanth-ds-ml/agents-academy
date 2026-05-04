# Lesson 2 Exercises

## Exercise 1 — Define a tool

Write a Python function that could be used as a tool for an agent. Pick one:

- `get_weather(city)` — returns fake/stubbed weather data
- `calculate(expression)` — evaluates a math expression safely
- `get_time()` — returns current date and time

Requirements:
- Clear function name
- Docstring explaining what it does and when to use it
- Type hints on all parameters
- Returns a string (tools always return strings to the model)

## Exercise 2 — Structured output

Write a prompt that asks the model to respond in JSON. The JSON should have:

```json
{
  "tool": "<tool name or 'respond'>",
  "args": { "<key>": "<value>" },
  "reasoning": "<one sentence on why>"
}
```

Test it by sending a few different messages and checking if the model consistently returns valid JSON.

## Exercise 3 — Tool router

Write a Python function `route(model_output: str)` that:

1. Parses the model's JSON output
2. Calls the right tool function with the right args
3. Returns the tool's result as a string
4. Handles JSON parse errors gracefully (returns an error string)

## Mini challenge — Build a 2-tool agent

Build a small agent that has exactly 2 tools:

- `read_file(path)` — reads a text file
- `get_time()` — returns current datetime

Give it a task like: *"What does notes.txt say, and what time is it?"*

The agent should call both tools and combine the results into a final answer.

## Related

- [[01-lessons/02-tools/lesson]]
- [[01-lessons/02-tools/notes]]
- [[02-projects/project-02-tool-agent/README]]
