import json
import re

from tools import TOOL_MAP, SAFE_TOOLS, CONFIRM_TOOLS


def parse_react_step(response: str) -> dict:
    """
    Parse one ReAct step from model output.

    Returns one of:
      {"type": "action", "thought": str, "tool": str, "args": dict}
      {"type": "final",  "thought": str, "answer": str}
      {"type": "error",  "raw": str}
    """
    thought = ""

    # Extract Thought block
    if "Thought:" in response:
        thought_start = response.index("Thought:") + len("Thought:")
        rest = response[thought_start:]
        for marker in ["Action:", "Final Answer:"]:
            if marker in rest:
                thought = rest[: rest.index(marker)].strip()
                break
        else:
            thought = rest.strip()

    # Final Answer
    if "Final Answer:" in response:
        fa_start = response.index("Final Answer:") + len("Final Answer:")
        return {"type": "final", "thought": thought, "answer": response[fa_start:].strip()}

    # Action with JSON
    if "Action:" in response:
        action_start = response.index("Action:") + len("Action:")
        action_text = response[action_start:].strip()
        json_match = re.search(r"\{.*\}", action_text, re.DOTALL)
        if json_match:
            try:
                action_json = json.loads(json_match.group())
                tool = action_json.get("tool", "").strip()
                args = action_json.get("args", {})
                if tool:
                    return {"type": "action", "thought": thought, "tool": tool, "args": args}
            except json.JSONDecodeError:
                pass

    return {"type": "error", "raw": response.strip()}


def call_tool(tool_name: str, args: dict) -> str:
    """Call a tool by name with given args. Returns result string."""
    if tool_name not in TOOL_MAP:
        available = ", ".join(TOOL_MAP.keys())
        return f"Unknown tool '{tool_name}'. Available: {available}"
    try:
        return TOOL_MAP[tool_name](**args)
    except TypeError as e:
        return f"Wrong arguments for '{tool_name}': {e}"
    except Exception as e:
        return f"Tool error in '{tool_name}': {e}"


def needs_confirm(tool_name: str) -> bool:
    return tool_name in CONFIRM_TOOLS


def format_args(args: dict) -> str:
    """Format args dict for display, truncating long values."""
    parts = []
    for k, v in args.items():
        v_str = repr(v)
        if len(v_str) > 60:
            v_str = v_str[:57] + "..."
        parts.append(f"{k}={v_str}")
    return ", ".join(parts)
