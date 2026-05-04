# Lesson 2 - Tools and Structured Inputs

## Outcome

By the end of this lesson, you should be able to give an agent real tools it can call, and get structured (typed) output back from a model.

## Core idea

A prompt-only agent can only think. A tool-using agent can **act**.

The model decides *which* tool to call and with *what* inputs. Python runs the tool and hands the result back. The model then decides the next step.

This is what separates a planning agent (Lesson 1) from an acting agent.

## The tool loop

```
User message
    ↓
Model decides: respond OR call a tool
    ↓ (if tool)
Python runs the tool → returns result
    ↓
Model sees result → decides next step
    ↓
Repeat until done → final response
```

## Key concepts

### 1. Tool definition

A tool is just a Python function with a clear name, docstring, and typed inputs. The model reads the docstring to know what the tool does and when to use it.

```python
def read_file(path: str) -> str:
    """Read and return the contents of a file at the given path."""
    return Path(path).read_text()
```

### 2. Tool routing

The model outputs which tool to call and what arguments to pass. This output must be structured (JSON) so Python can parse and execute it reliably.

### 3. Structured output

Instead of free text, you ask the model to respond in a fixed format:

```json
{
  "tool": "read_file",
  "args": { "path": "notes.txt" }
}
```

You parse this and call the right function. If the model says `"tool": "none"` or `"tool": "respond"`, you return its answer to the user.

### 4. Tool safety

- Always validate inputs before running a tool
- Never give an agent tools that can't be undone without a confirm step
- Log every tool call — you need to debug it later

### 5. ReAct pattern

The most common pattern for tool-using agents:

**Re**ason → **Act** → Observe → Reason again

The model writes its reasoning first, then decides the action. This makes it more reliable than jumping straight to a tool call.

## Simple example

### Without tools (Lesson 1 style)

> User: "What files are in my project folder?"
> Agent: "I don't have access to your filesystem, but here's how you could check..."

### With tools (Lesson 2)

> User: "What files are in my project folder?"
> Agent calls `list_files(path=".")` → gets real results → responds with actual list

## Common tools to build first

| Tool | What it does |
|---|---|
| `read_file(path)` | Read a file and return its content |
| `list_files(path)` | List files in a directory |
| `write_file(path, content)` | Write content to a file |
| `run_shell(cmd)` | Run a shell command and return output |
| `web_search(query)` | Search the web and return results |
| `get_time()` | Return current date/time |

Start with the safest, most reversible tools first.

## Design rules

1. **Model decides, Python does** — never let the model run code directly
2. **One tool per function** — keep tools small and focused
3. **Always handle tool errors** — the model must see the error to recover
4. **Limit what tools can touch** — scope them to specific folders or APIs

## Practice

Before the exercises, answer this in your own words:

> "What is the difference between a tool and a prompt?"

## Concept notes

- [[04-memory-vault/concepts/agent-loop]]
- [[04-memory-vault/concepts/tools-vs-prompts]]
- [[04-memory-vault/concepts/react-pattern]]

## After this lesson

- [[01-lessons/02-tools/exercises]]
- [[01-lessons/02-tools/notes]]
- [[02-projects/project-02-tool-agent/README]]
- Previous → [[01-lessons/01-foundations/lesson]]
