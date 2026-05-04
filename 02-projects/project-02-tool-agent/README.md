# Project 2 - First Tool-Using Agent

This is the next step after Project 1.

Project 1 could **plan** well. Project 2 should **act** by calling real tools from Python.

## Goal

Build a tiny agent with 2 tools and a simple routing loop.

Recommended first tools:

1. `get_time()` - returns the current date and time
2. `read_file(path)` - reads a text file safely

## Target behavior

For a prompt like:

> What does `notes.txt` say, and what time is it?

The agent should:

1. decide which tools are needed
2. return structured JSON
3. call the tools in Python
4. combine the results into one final answer

## Suggested files

- `main.py` - CLI entrypoint
- `tools.py` - the tool functions
- `router.py` - parse JSON and call the right tool
- `notes.txt` - sample file for testing

## Run flow

```powershell
.venv\Scripts\Activate.ps1
cd 02-projects\project-02-tool-agent
python main.py
```

## Definition of done

- 2 working tools
- 1 structured model response format
- graceful handling of JSON parse errors
- a final combined answer shown in the terminal

## Related

- [[01-lessons/02-tools/lesson]]
- [[01-lessons/02-tools/exercises]]
- [[04-memory-vault/concepts/tools-vs-prompts]]
- [[04-memory-vault/concepts/react-pattern]]
